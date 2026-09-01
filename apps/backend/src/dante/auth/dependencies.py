"""FastAPI and pre-routing Web security dependencies for Access/Auth."""

from typing import cast

from fastapi import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from dante.auth.lifecycle import AuthLifecycleService
from dante.auth.lifecycle_runtime import AuthLifecycleRuntime
from dante.auth.provider_flow_runtime import ProviderFlowRuntime
from dante.auth.service import AuthRuntime, AuthService
from dante.auth.sessions import WEB_CLIENT_HEADER_NAME, WEB_CLIENT_HEADER_VALUE
from dante.platform.http.problem import ProblemError, problem_response_for_scope

_AUTH_API_PATH = "/api/v1/auth"
_AUTH_MUTATION_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})
_JSON_BODY_METHODS = frozenset({"POST", "PUT", "PATCH"})
_EXTERNAL_AUTH_INGRESS = frozenset(
    {
        ("POST", "/api/v1/auth/apple/callback"),
        ("POST", "/api/v1/auth/apple/notifications"),
    }
)
_DEFAULT_MAX_AUTH_REQUEST_BODY_BYTES = 64 * 1024


def get_auth_service(request: Request) -> AuthService:
    """Resolve the process-scoped M3 AuthService installed by lifespan."""
    auth_runtime = cast(AuthRuntime, request.app.state.auth_runtime)
    return auth_runtime.service


def get_auth_lifecycle_service(request: Request) -> AuthLifecycleService:
    """Resolve the process-scoped M4 AuthLifecycleService installed by lifespan."""
    lifecycle_runtime = cast(AuthLifecycleRuntime, request.app.state.auth_lifecycle_runtime)
    return lifecycle_runtime.service


def get_auth_provider_flow_runtime(request: Request) -> ProviderFlowRuntime:
    """Resolve the process-scoped M5 provider/authenticator runtime installed by lifespan."""
    return cast(ProviderFlowRuntime, request.app.state.auth_provider_flow_runtime)


def single_header_value(scope: Scope, name: str) -> str | None:
    """Return one exact raw ASGI header value; duplicates fail closed."""
    expected_name = name.casefold().encode("ascii")
    raw_headers = cast(list[tuple[bytes, bytes]], scope.get("headers", []))
    values = [raw_value for raw_name, raw_value in raw_headers if raw_name.lower() == expected_name]
    if len(values) != 1:
        return None
    try:
        return values[0].decode("latin-1")
    except UnicodeDecodeError:
        return None


def _is_auth_mutation(method: str, path: str) -> bool:
    return method in _AUTH_MUTATION_METHODS and (
        path == _AUTH_API_PATH or path.startswith(f"{_AUTH_API_PATH}/")
    )


def _problem(
    scope: Scope,
    *,
    status: int,
    code: str,
    title: str,
    detail: str,
) -> ASGIApp:
    return cast(
        ASGIApp,
        problem_response_for_scope(
            scope,
            ProblemError(
                status=status,
                code=code,
                category="validation" if status != 403 else "security",
                title=title,
                detail=detail,
            ),
        ),
    )


def _content_length(scope: Scope) -> int | None:
    raw_headers = cast(list[tuple[bytes, bytes]], scope.get("headers", []))
    values = [value for name, value in raw_headers if name.lower() == b"content-length"]
    if not values:
        return None
    if len(values) != 1:
        raise ValueError("ambiguous Content-Length")
    raw_value = values[0]
    if not raw_value or any(byte < 48 or byte > 57 for byte in raw_value):
        raise ValueError("noncanonical Content-Length")
    try:
        return int(raw_value)
    except ValueError as exc:
        raise ValueError("invalid Content-Length") from exc


class AuthRequestBodyLimitMiddleware:
    """Bound Auth mutation bodies before framework parsing or application allocation."""

    def __init__(
        self,
        app: ASGIApp,
        *,
        max_body_bytes: int = _DEFAULT_MAX_AUTH_REQUEST_BODY_BYTES,
    ) -> None:
        if max_body_bytes < 1:
            raise ValueError("Auth request body bound must be positive")
        self._app = app
        self._max_body_bytes = max_body_bytes

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        method = str(scope.get("method", "")).upper()
        path = str(scope.get("path", ""))
        if not _is_auth_mutation(method, path):
            await self._app(scope, receive, send)
            return

        try:
            declared_length = _content_length(scope)
        except ValueError:
            response = _problem(
                scope,
                status=400,
                code="request.malformed",
                title="Malformed request",
                detail="The request has an invalid Content-Length header.",
            )
            await response(scope, receive, send)
            return

        if declared_length is not None and declared_length > self._max_body_bytes:
            response = _problem(
                scope,
                status=413,
                code="request.payload_too_large",
                title="Request too large",
                detail="The authentication request exceeds the accepted payload bound.",
            )
            await response(scope, receive, send)
            return

        buffered = bytearray()
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            if message["type"] != "http.request":
                response = _problem(
                    scope,
                    status=400,
                    code="request.malformed",
                    title="Malformed request",
                    detail="The authentication request body could not be read safely.",
                )
                await response(scope, receive, send)
                return

            chunk = message.get("body", b"")
            if len(chunk) > self._max_body_bytes - len(buffered):
                response = _problem(
                    scope,
                    status=413,
                    code="request.payload_too_large",
                    title="Request too large",
                    detail="The authentication request exceeds the accepted payload bound.",
                )
                await response(scope, receive, send)
                return
            buffered.extend(chunk)
            if not message.get("more_body", False):
                break

        if declared_length is not None and declared_length != len(buffered):
            response = _problem(
                scope,
                status=400,
                code="request.malformed",
                title="Malformed request",
                detail="The request body does not match its declared Content-Length.",
            )
            await response(scope, receive, send)
            return

        body = bytes(buffered)
        replayed = False

        async def replay_receive() -> Message:
            nonlocal replayed
            if replayed:
                return {"type": "http.disconnect"}
            replayed = True
            return {"type": "http.request", "body": body, "more_body": False}

        await self._app(scope, replay_receive, send)


class BrowserAuthSecurityMiddleware:
    """Fail closed on first-party Web Auth mutations before request-body parsing."""

    def __init__(self, app: ASGIApp, *, canonical_web_origin: str) -> None:
        self._app = app
        self._canonical_web_origin = canonical_web_origin

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        method = str(scope.get("method", "")).upper()
        path = str(scope.get("path", ""))
        if not _is_auth_mutation(method, path) or (method, path) in _EXTERNAL_AUTH_INGRESS:
            await self._app(scope, receive, send)
            return

        if (
            single_header_value(scope, "Origin") != self._canonical_web_origin
            or single_header_value(scope, "Sec-Fetch-Site") != "same-origin"
            or single_header_value(scope, WEB_CLIENT_HEADER_NAME) != WEB_CLIENT_HEADER_VALUE
        ):
            response = _problem(
                scope,
                status=403,
                code="security.csrf_failed",
                title="Request rejected",
                detail="The request could not satisfy the browser security policy.",
            )
            await response(scope, receive, send)
            return

        if method in _JSON_BODY_METHODS:
            content_type = single_header_value(scope, "Content-Type")
            media_type = (
                content_type.split(";", 1)[0].strip().lower() if content_type is not None else None
            )
            if media_type != "application/json":
                response = _problem(
                    scope,
                    status=400,
                    code="request.malformed",
                    title="Malformed request",
                    detail="The request must use application/json.",
                )
                await response(scope, receive, send)
                return

        await self._app(scope, receive, send)
