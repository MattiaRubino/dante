"""Public M5 Account authenticator and password lifecycle API."""

from __future__ import annotations

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.auth.api import AuthenticatedSessionResponse
from dante.auth.authenticator_lifecycle import (
    AuthenticatorLifecycleService,
    MultiAuthenticatorLifecycleService,
)
from dante.auth.contracts import (
    AccountUnavailableError,
    AdmittedSession,
    AuthenticationMethods,
    AuthenticatorRemovalBlockedError,
    AuthInputError,
    AuthServiceUnavailableError,
    AuthStateChangedError,
    IssuedSession,
    PasswordAlreadyEstablishedError,
    PasswordCompromisedError,
    ReauthenticationRequiredError,
)
from dante.auth.dependencies import (
    get_auth_lifecycle_service,
    get_auth_service,
    get_authenticator_lifecycle_service,
    single_header_value,
)
from dante.auth.service import AuthService
from dante.auth.sessions import (
    CSRF_HEADER_NAME,
    SESSION_COOKIE_NAME,
    AmbiguousSessionCookieError,
    csrf_token_matches,
    session_cookie_value,
)
from dante.platform.http.problem import ProblemDetails, ProblemError, ProblemFieldError

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]
MultiAuthenticatorLifecycleDependency = Annotated[
    MultiAuthenticatorLifecycleService,
    Depends(get_auth_lifecycle_service),
]
AuthenticatorLifecycleDependency = Annotated[
    AuthenticatorLifecycleService,
    Depends(get_authenticator_lifecycle_service),
]


class AuthenticationProviderMethodResponse(BaseModel):
    """Safe provider authenticator metadata for Security/settings surfaces."""

    model_config = ConfigDict(extra="forbid")

    external_identity_ref: UUID
    provider_code: str
    provider_email_address: str | None
    provider_email_private: bool | None


class AuthenticationMethodsResponse(BaseModel):
    """Current Account-wide direct-authenticator and recovery-channel inventory."""

    model_config = ConfigDict(extra="forbid")

    password_established: bool
    providers: tuple[AuthenticationProviderMethodResponse, ...]
    active_passkey_count: int = Field(ge=0)
    recovery_eligible_email_count: int = Field(ge=0)


class PasswordEstablishRequest(BaseModel):
    """Establish the first PasswordCredential for the authenticated Account."""

    model_config = ConfigDict(extra="forbid")

    new_password: str = Field(min_length=1, max_length=4096)


_COMMON_PROBLEM_RESPONSES: dict[int | str, dict[str, Any]] = {
    401: {"model": ProblemDetails},
    403: {"model": ProblemDetails},
    500: {"model": ProblemDetails},
    503: {"model": ProblemDetails},
}
_PASSWORD_MUTATION_PROBLEM_RESPONSES: dict[int | str, dict[str, Any]] = {
    400: {"model": ProblemDetails},
    **_COMMON_PROBLEM_RESPONSES,
    409: {"model": ProblemDetails},
    422: {"model": ProblemDetails},
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


def _session_cookie(request: Request) -> str | None:
    raw_headers = list(request.scope.get("headers", []))
    return session_cookie_value(raw_headers)


def _authentication_required() -> ProblemError:
    return ProblemError(
        status=401,
        code="auth.authentication_required",
        category="authentication",
        title="Authentication required",
        detail="A valid authenticated session is required.",
    )


def _csrf_failed() -> ProblemError:
    return ProblemError(
        status=403,
        code="security.csrf_failed",
        category="security",
        title="Request rejected",
        detail="The request could not satisfy the browser security policy.",
    )


def _translate_m5_auth_error(exc: Exception) -> ProblemError:
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
            title="Password not accepted",
            detail="This password cannot be accepted by the current security policy.",
        )
    if isinstance(exc, ReauthenticationRequiredError):
        return ProblemError(
            status=401,
            code="auth.reauthentication_required",
            category="authentication",
            title="Reauthentication required",
            detail="Fresh authentication evidence is required for this operation.",
        )
    if isinstance(exc, PasswordAlreadyEstablishedError):
        return ProblemError(
            status=409,
            code="auth.password_already_established",
            category="conflict",
            title="Password already established",
            detail="The authenticated account already has a password authenticator.",
        )
    if isinstance(exc, AuthenticatorRemovalBlockedError):
        return ProblemError(
            status=409,
            code="auth.authenticator_removal_blocked",
            category="conflict",
            title="Authenticator removal blocked",
            detail="Removing this authenticator would violate the account access policy.",
        )
    if isinstance(exc, AuthStateChangedError):
        return ProblemError(
            status=409,
            code="conflict.state_changed",
            category="conflict",
            title="Authentication state changed",
            detail="Authentication state changed before the operation could be committed.",
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
    raise TypeError("unexpected M5 Auth error translation")


async def _required_session(
    *,
    request: Request,
    response: Response,
    auth_service: AuthService,
    require_csrf: bool,
) -> tuple[AdmittedSession, str]:
    try:
        cookie_value = _session_cookie(request)
    except AmbiguousSessionCookieError as exc:
        if require_csrf:
            raise _csrf_failed() from exc
        _clear_session_cookie(response)
        raise _authentication_required() from exc

    try:
        admitted = await auth_service.admit_session(cookie_value)
    except AuthServiceUnavailableError as exc:
        raise _translate_m5_auth_error(exc) from exc
    if admitted is None or cookie_value is None:
        _clear_session_cookie(response)
        raise _authentication_required()

    if require_csrf and not csrf_token_matches(
        admitted.csrf_token,
        single_header_value(request.scope, CSRF_HEADER_NAME),
    ):
        raise _csrf_failed()

    return admitted, cookie_value


def _authenticated_response(session: IssuedSession) -> AuthenticatedSessionResponse:
    return AuthenticatedSessionResponse(
        account_ref=session.principal.account_ref,
        auth_session_ref=session.principal.auth_session_ref,
        recent_auth_at=session.principal.recent_auth_at,
        expires_at=session.expires_at,
        csrf_token=session.csrf_token.get_secret_value(),
    )


def _methods_response(methods: AuthenticationMethods) -> AuthenticationMethodsResponse:
    return AuthenticationMethodsResponse(
        password_established=methods.password_established,
        providers=tuple(
            AuthenticationProviderMethodResponse(
                external_identity_ref=provider.external_identity_ref,
                provider_code=provider.provider_code,
                provider_email_address=provider.provider_email_address,
                provider_email_private=provider.provider_email_private,
            )
            for provider in methods.providers
        ),
        active_passkey_count=methods.active_passkey_count,
        recovery_eligible_email_count=methods.recovery_eligible_email_count,
    )


@router.get(
    "/methods",
    operation_id="auth_get_authentication_methods",
    response_model=AuthenticationMethodsResponse,
    responses=_COMMON_PROBLEM_RESPONSES,
)
async def get_authentication_methods(
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    authenticator_service: AuthenticatorLifecycleDependency,
) -> AuthenticationMethodsResponse:
    """Return safe Account-wide authenticator inventory for the admitted AuthSession."""
    admitted, _cookie_value = await _required_session(
        request=request,
        response=response,
        auth_service=auth_service,
        require_csrf=False,
    )
    try:
        methods = await authenticator_service.authentication_methods(admitted=admitted)
    except (AccountUnavailableError, AuthServiceUnavailableError) as exc:
        raise _translate_m5_auth_error(exc) from exc
    return _methods_response(methods)


@router.post(
    "/password/establish",
    operation_id="auth_establish_password",
    response_model=AuthenticatedSessionResponse,
    responses=_PASSWORD_MUTATION_PROBLEM_RESPONSES,
)
async def establish_password(
    payload: PasswordEstablishRequest,
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    lifecycle_service: MultiAuthenticatorLifecycleDependency,
) -> AuthenticatedSessionResponse:
    """Establish the first password and rotate the bearer on the same AuthSession."""
    admitted, cookie_value = await _required_session(
        request=request,
        response=response,
        auth_service=auth_service,
        require_csrf=True,
    )
    try:
        issued = await lifecycle_service.establish_password(
            admitted=admitted,
            presented_session_secret=cookie_value,
            new_password=payload.new_password,
        )
    except (
        AccountUnavailableError,
        AuthInputError,
        AuthServiceUnavailableError,
        AuthStateChangedError,
        PasswordAlreadyEstablishedError,
        PasswordCompromisedError,
        ReauthenticationRequiredError,
    ) as exc:
        raise _translate_m5_auth_error(exc) from exc

    _set_session_cookie(
        response,
        issued.session_secret.get_secret_value(),
        max_age_seconds=lifecycle_service.session_cookie_max_age_seconds,
    )
    return _authenticated_response(issued)


@router.delete(
    "/password",
    operation_id="auth_remove_password",
    response_model=AuthenticatedSessionResponse,
    responses={
        **_COMMON_PROBLEM_RESPONSES,
        409: {"model": ProblemDetails},
    },
)
async def remove_password(
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    lifecycle_service: MultiAuthenticatorLifecycleDependency,
) -> AuthenticatedSessionResponse:
    """Remove the password only when Account-wide anti-lockout remains satisfied."""
    admitted, cookie_value = await _required_session(
        request=request,
        response=response,
        auth_service=auth_service,
        require_csrf=True,
    )
    try:
        issued = await lifecycle_service.remove_password(
            admitted=admitted,
            presented_session_secret=cookie_value,
        )
    except (
        AccountUnavailableError,
        AuthServiceUnavailableError,
        AuthStateChangedError,
        AuthenticatorRemovalBlockedError,
        ReauthenticationRequiredError,
    ) as exc:
        raise _translate_m5_auth_error(exc) from exc

    _set_session_cookie(
        response,
        issued.session_secret.get_secret_value(),
        max_age_seconds=lifecycle_service.session_cookie_max_age_seconds,
    )
    return _authenticated_response(issued)
