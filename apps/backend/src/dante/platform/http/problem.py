"""RFC 9457 Problem Details, request correlation and Auth cache policy."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any
from uuid import uuid7

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

_LOGGER = logging.getLogger(__name__)


class ProblemFieldError(BaseModel):
    """Stable bounded field error surfaced to first-party clients."""

    model_config = ConfigDict(extra="forbid")

    pointer: str
    code: str
    detail: str
    parameters: dict[str, int] | None = None


class ProblemDetails(BaseModel):
    """DANTE RFC 9457 public error contract."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    problem_type: str = Field(alias="type")
    title: str
    status: int
    detail: str
    code: str
    category: str
    request_id: str
    retryable: bool
    errors: list[ProblemFieldError] | None = None


class ProblemError(Exception):
    """Expected public API problem without internal exception disclosure."""

    def __init__(
        self,
        *,
        status: int,
        code: str,
        category: str,
        title: str,
        detail: str,
        retryable: bool = False,
        errors: list[ProblemFieldError] | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(code)
        self.status = status
        self.code = code
        self.category = category
        self.title = title
        self.detail = detail
        self.retryable = retryable
        self.errors = errors
        self.headers = headers or {}


def ensure_request_id(scope: Scope) -> str:
    """Return/create the server-authoritative public support identifier."""
    state = scope.get("state")
    if state is None:
        state = {}
        scope["state"] = state

    existing = state.get("request_id")
    if existing is not None:
        return str(existing)

    request_id = str(uuid7())
    state["request_id"] = request_id
    return request_id


def _problem_type(code: str) -> str:
    return f"urn:dante:problem:{code}"


def _payload(problem: ProblemError, *, request_id: str) -> dict[str, Any]:
    body: dict[str, Any] = {
        "type": _problem_type(problem.code),
        "title": problem.title,
        "status": problem.status,
        "detail": problem.detail,
        "code": problem.code,
        "category": problem.category,
        "request_id": request_id,
        "retryable": problem.retryable,
    }
    if problem.errors is not None:
        body["errors"] = [
            field_error.model_dump(exclude_none=True)
            for field_error in problem.errors
        ]
    return body


def problem_response(request: Request, problem: ProblemError) -> JSONResponse:
    """Serialize one safe RFC 9457 problem."""
    request_id = ensure_request_id(request.scope)
    headers = {**problem.headers, "X-Request-ID": request_id}
    return JSONResponse(
        status_code=problem.status,
        content=_payload(problem, request_id=request_id),
        headers=headers,
        media_type="application/problem+json",
    )


def problem_response_for_scope(scope: Scope, problem: ProblemError) -> JSONResponse:
    """Serialize a problem from pre-routing ASGI policy middleware."""
    request_id = ensure_request_id(scope)
    headers = {
        **problem.headers,
        "X-Request-ID": request_id,
        "Cache-Control": "no-store",
    }
    return JSONResponse(
        status_code=problem.status,
        content=_payload(problem, request_id=request_id),
        headers=headers,
        media_type="application/problem+json",
    )


class RequestContextMiddleware:
    """Pure-ASGI request ID and Auth no-store policy."""

    def __init__(self, app: ASGIApp) -> None:
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        request_id = ensure_request_id(scope)
        path = str(scope.get("path", ""))

        async def send_with_headers(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers["X-Request-ID"] = request_id
                if path.startswith("/api/v1/auth/"):
                    headers["Cache-Control"] = "no-store"
            await send(message)

        await self._app(scope, receive, send_with_headers)


def _validation_field_error(error: Mapping[str, Any]) -> ProblemFieldError:
    location = error.get("loc", ())
    body_parts = (
        [str(part) for part in location[1:]]
        if location and location[0] == "body"
        else []
    )
    pointer = "/" + "/".join(
        part.replace("~", "~0").replace("/", "~1")
        for part in body_parts
    )
    if not body_parts:
        pointer = "/"

    error_type = str(error.get("type", ""))
    raw_context = error.get("ctx")
    context = raw_context if isinstance(raw_context, Mapping) else {}

    if error_type == "missing":
        return ProblemFieldError(
            pointer=pointer,
            code="required",
            detail="This field is required.",
        )
    if error_type == "string_too_short":
        minimum = int(context.get("min_length", 0))
        return ProblemFieldError(
            pointer=pointer,
            code="too_short",
            detail="The value does not meet the minimum length.",
            parameters={"minimum": minimum},
        )
    if error_type == "string_too_long":
        maximum = int(context.get("max_length", 0))
        return ProblemFieldError(
            pointer=pointer,
            code="too_long",
            detail="The value exceeds the maximum length.",
            parameters={"maximum": maximum},
        )
    return ProblemFieldError(
        pointer=pointer,
        code="invalid_value",
        detail="The supplied value is not valid.",
    )


def install_problem_handlers(app: FastAPI) -> None:
    """Install stable validation/expected/unexpected error boundaries."""

    async def handle_problem(request: Request, exc: Exception) -> JSONResponse:
        if not isinstance(exc, ProblemError):
            raise TypeError("registered problem handler received unexpected exception")
        return problem_response(request, exc)

    async def handle_validation(request: Request, exc: Exception) -> JSONResponse:
        if not isinstance(exc, RequestValidationError):
            raise TypeError("registered validation handler received unexpected exception")

        errors = exc.errors()
        if any(str(error.get("type", "")) == "json_invalid" for error in errors):
            return problem_response(
                request,
                ProblemError(
                    status=400,
                    code="request.malformed",
                    category="validation",
                    title="Malformed request",
                    detail="The request body is not valid JSON.",
                ),
            )

        return problem_response(
            request,
            ProblemError(
                status=422,
                code="request.validation_failed",
                category="validation",
                title="Request validation failed",
                detail="One or more request fields are invalid.",
                errors=[_validation_field_error(error) for error in errors],
            ),
        )

    async def handle_unexpected(request: Request, exc: Exception) -> JSONResponse:
        request_id = ensure_request_id(request.scope)
        _LOGGER.error(
            "internal.unexpected request_id=%s exception_type=%s",
            request_id,
            type(exc).__name__,
        )
        problem = ProblemError(
            status=500,
            code="internal.unexpected",
            category="internal",
            title="Unexpected server error",
            detail="The server could not complete the request.",
        )
        return problem_response(request, problem)

    app.add_exception_handler(ProblemError, handle_problem)
    app.add_exception_handler(RequestValidationError, handle_validation)
    app.add_exception_handler(Exception, handle_unexpected)
