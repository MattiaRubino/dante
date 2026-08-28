"""Public M3 Access/Auth application-intent API."""

from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.auth.contracts import (
    AccountUnavailableError,
    AdmittedSession,
    AuthInputError,
    AuthServiceUnavailableError,
    InvalidCredentialsError,
    IssuedSession,
    PasswordCompromisedError,
    SigninRateLimitedError,
)
from dante.auth.dependencies import get_auth_service, single_header_value
from dante.auth.service import AuthService
from dante.auth.sessions import (
    CSRF_HEADER_NAME,
    SESSION_COOKIE_NAME,
    AmbiguousSessionCookieError,
    csrf_token_matches,
    session_cookie_value,
)
from dante.platform.http.problem import (
    ProblemDetails,
    ProblemError,
    ProblemFieldError,
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]


class SignInRequest(BaseModel):
    """Bounded first-party email/password signin request."""

    model_config = ConfigDict(extra="forbid")

    email: str = Field(min_length=1, max_length=320)
    password: str = Field(min_length=1, max_length=4096)


class AuthenticatedSessionResponse(BaseModel):
    """Authenticated bootstrap/session representation."""

    model_config = ConfigDict(extra="forbid")

    authenticated: Literal[True] = True
    account_ref: UUID
    auth_session_ref: UUID
    recent_auth_at: datetime
    expires_at: datetime
    csrf_token: str


class UnauthenticatedSessionResponse(BaseModel):
    """Unauthenticated bootstrap representation."""

    model_config = ConfigDict(extra="forbid")

    authenticated: Literal[False] = False


SessionResponse = AuthenticatedSessionResponse | UnauthenticatedSessionResponse

_PROBLEM_RESPONSES: dict[int | str, dict[str, Any]] = {
    400: {"model": ProblemDetails},
    401: {"model": ProblemDetails},
    403: {"model": ProblemDetails},
    422: {"model": ProblemDetails},
    429: {"model": ProblemDetails},
    500: {"model": ProblemDetails},
    503: {"model": ProblemDetails},
}


def _set_session_cookie(
    response: Response,
    secret: str,
    *,
    max_age_seconds: int,
) -> None:
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=secret,
        max_age=max_age_seconds,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
    )


def _clear_session_cookie(response: Response) -> None:
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
    )


def _authenticated_response(
    session: IssuedSession | AdmittedSession,
) -> AuthenticatedSessionResponse:
    return AuthenticatedSessionResponse(
        account_ref=session.principal.account_ref,
        auth_session_ref=session.principal.auth_session_ref,
        recent_auth_at=session.principal.recent_auth_at,
        expires_at=session.expires_at,
        csrf_token=session.csrf_token.get_secret_value(),
    )


def _session_cookie(request: Request) -> str | None:
    raw_headers = list(request.scope.get("headers", []))
    return session_cookie_value(raw_headers)


def _translate_auth_error(exc: Exception) -> ProblemError:
    if isinstance(exc, AuthInputError):
        return ProblemError(
            status=422,
            code="request.validation_failed",
            category="validation",
            title="Request validation failed",
            detail="One or more request fields are invalid.",
            errors=[
                ProblemFieldError(
                    pointer=exc.pointer,
                    code=exc.code,
                    detail=exc.detail,
                    parameters=exc.parameters,
                )
            ],
        )
    if isinstance(exc, InvalidCredentialsError):
        return ProblemError(
            status=401,
            code="auth.invalid_credentials",
            category="authentication",
            title="Authentication failed",
            detail="The supplied credentials could not be accepted.",
        )
    if isinstance(exc, AccountUnavailableError):
        return ProblemError(
            status=403,
            code="auth.account_unavailable",
            category="authentication",
            title="Account unavailable",
            detail="The authenticated account is not currently available.",
        )
    if isinstance(exc, PasswordCompromisedError):
        return ProblemError(
            status=403,
            code="auth.password_compromised",
            category="authentication",
            title="Password reset required",
            detail="This password cannot be used to open a new session.",
        )
    if isinstance(exc, SigninRateLimitedError):
        return ProblemError(
            status=429,
            code="rate_limit.exceeded",
            category="rate_limit",
            title="Too many attempts",
            detail="Too many authentication attempts were received.",
            retryable=True,
            headers={"Retry-After": str(exc.retry_after_seconds)},
        )
    if isinstance(exc, AuthServiceUnavailableError):
        return ProblemError(
            status=503,
            code="service.unavailable",
            category="service",
            title="Service unavailable",
            detail="Authentication is temporarily unavailable.",
            retryable=exc.retryable,
        )
    raise TypeError("unexpected Auth error translation")


@router.post(
    "/signin",
    operation_id="auth_sign_in",
    response_model=AuthenticatedSessionResponse,
    responses=_PROBLEM_RESPONSES,
)
async def sign_in(
    payload: SignInRequest,
    request: Request,
    response: Response,
    service: AuthServiceDependency,
) -> AuthenticatedSessionResponse:
    """Authenticate email/password and establish one new independent AuthSession."""
    try:
        issued = await service.sign_in(
            email=payload.email,
            password=payload.password,
            request_id=str(request.state.request_id),
        )
    except (
        AccountUnavailableError,
        AuthInputError,
        AuthServiceUnavailableError,
        InvalidCredentialsError,
        PasswordCompromisedError,
        SigninRateLimitedError,
    ) as exc:
        raise _translate_auth_error(exc) from exc

    _set_session_cookie(
        response,
        issued.session_secret.get_secret_value(),
        max_age_seconds=service.session_cookie_max_age_seconds,
    )
    return _authenticated_response(issued)


@router.get(
    "/session",
    operation_id="auth_get_session",
    response_model=SessionResponse,
    responses={
        500: {"model": ProblemDetails},
        503: {"model": ProblemDetails},
    },
)
async def get_session(
    request: Request,
    response: Response,
    service: AuthServiceDependency,
) -> SessionResponse:
    """Return authoritative current Web session state without user activity."""
    try:
        cookie_value = _session_cookie(request)
    except AmbiguousSessionCookieError:
        _clear_session_cookie(response)
        return UnauthenticatedSessionResponse()

    try:
        admitted = await service.admit_session(cookie_value)
    except AuthServiceUnavailableError as exc:
        raise _translate_auth_error(exc) from exc

    if admitted is None:
        if cookie_value is not None:
            _clear_session_cookie(response)
        return UnauthenticatedSessionResponse()

    return _authenticated_response(admitted)


@router.delete(
    "/session",
    operation_id="auth_log_out",
    status_code=204,
    response_model=None,
    responses={
        403: {"model": ProblemDetails},
        500: {"model": ProblemDetails},
        503: {"model": ProblemDetails},
    },
)
async def log_out(
    request: Request,
    response: Response,
    service: AuthServiceDependency,
) -> None:
    """Idempotently revoke the current valid AuthSession and clear its cookie."""
    try:
        cookie_value = _session_cookie(request)
    except AmbiguousSessionCookieError as exc:
        raise ProblemError(
            status=403,
            code="security.csrf_failed",
            category="security",
            title="Request rejected",
            detail="The request could not satisfy the browser security policy.",
        ) from exc

    try:
        admitted = await service.admit_session(cookie_value)
    except AuthServiceUnavailableError as exc:
        raise _translate_auth_error(exc) from exc

    if admitted is None:
        _clear_session_cookie(response)
        return

    if not csrf_token_matches(
        admitted.csrf_token,
        single_header_value(request.scope, CSRF_HEADER_NAME),
    ):
        raise ProblemError(
            status=403,
            code="security.csrf_failed",
            category="security",
            title="Request rejected",
            detail="The request could not satisfy the browser security policy.",
        )

    try:
        await service.log_out(admitted.principal.auth_session_ref)
    except AuthServiceUnavailableError as exc:
        raise _translate_auth_error(exc) from exc

    _clear_session_cookie(response)
