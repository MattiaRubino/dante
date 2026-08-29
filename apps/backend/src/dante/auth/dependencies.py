"""FastAPI and pre-routing Web security dependencies for Access/Auth."""

from typing import cast

from fastapi import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from dante.auth.lifecycle import AuthLifecycleService
from dante.auth.lifecycle_runtime import AuthLifecycleRuntime
from dante.auth.service import AuthRuntime, AuthService
from dante.auth.sessions import WEB_CLIENT_HEADER_NAME, WEB_CLIENT_HEADER_VALUE
from dante.platform.http.problem import ProblemError, problem_response_for_scope

_M4_JSON_POST_PATHS = frozenset(
    {
        "/api/v1/auth/signup",
        "/api/v1/auth/signup/verify",
        "/api/v1/auth/signup/resend",
        "/api/v1/auth/recovery",
        "/api/v1/auth/recovery/validate",
        "/api/v1/auth/reset-password",
        "/api/v1/auth/reauthenticate",
    }
)


def get_auth_service(request: Request) -> AuthService:
    """Resolve the process-scoped M3 AuthService installed by lifespan."""
    auth_runtime = cast(AuthRuntime, request.app.state.auth_runtime)
    return auth_runtime.service


def get_auth_lifecycle_service(request: Request) -> AuthLifecycleService:
    """Resolve the process-scoped M4 AuthLifecycleService installed by lifespan."""
    lifecycle_runtime = cast(AuthLifecycleRuntime, request.app.state.auth_lifecycle_runtime)
    return lifecycle_runtime.service


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


class BrowserAuthSecurityMiddleware:
    """Fail closed on Web Auth mutations before request-body parsing."""

    def __init__(self, app: ASGIApp, *, canonical_web_origin: str) -> None:
        self._app = app
        self._canonical_web_origin = canonical_web_origin

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        method = str(scope.get("method", "")).upper()
        path = str(scope.get("path", ""))
        protected_json_post = method == "POST" and (
            path == "/api/v1/auth/signin" or path in _M4_JSON_POST_PATHS
        )
        protected_logout = method == "DELETE" and path == "/api/v1/auth/session"
        if not (protected_json_post or protected_logout):
            await self._app(scope, receive, send)
            return

        if (
            single_header_value(scope, "Origin") != self._canonical_web_origin
            or single_header_value(scope, "Sec-Fetch-Site") != "same-origin"
            or single_header_value(scope, WEB_CLIENT_HEADER_NAME) != WEB_CLIENT_HEADER_VALUE
        ):
            response = problem_response_for_scope(
                scope,
                ProblemError(
                    status=403,
                    code="security.csrf_failed",
                    category="security",
                    title="Request rejected",
                    detail="The request could not satisfy the browser security policy.",
                ),
            )
            await response(scope, receive, send)
            return

        if protected_json_post:
            content_type = single_header_value(scope, "Content-Type")
            media_type = (
                content_type.split(";", 1)[0].strip().lower() if content_type is not None else None
            )
            if media_type != "application/json":
                response = problem_response_for_scope(
                    scope,
                    ProblemError(
                        status=400,
                        code="request.malformed",
                        category="validation",
                        title="Malformed request",
                        detail="The request must use application/json.",
                    ),
                )
                await response(scope, receive, send)
                return

        await self._app(scope, receive, send)
