"""Public M5 Account authenticator and password lifecycle API."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.auth.api import AuthenticatedSessionResponse
from dante.auth.authenticator_lifecycle import (
    AuthenticatorLifecycleService,
    MultiAuthenticatorLifecycleService,
)
from dante.auth.contracts import AuthenticationMethods, AuthError, PasskeyMethod
from dante.auth.dependencies import (
    get_auth_lifecycle_service,
    get_auth_provider_flow_runtime,
    get_auth_service,
    get_authenticator_lifecycle_service,
)
from dante.auth.m5_http import (
    COMMON_M5_PROBLEM_RESPONSES,
    authenticated_response,
    required_session,
    set_session_cookie,
    translate_m5_auth_error,
)
from dante.auth.provider_flow_runtime import ProviderFlowRuntime
from dante.auth.service import AuthService

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
ProviderRuntimeDependency = Annotated[ProviderFlowRuntime, Depends(get_auth_provider_flow_runtime)]


class AuthenticationProviderMethodResponse(BaseModel):
    """Safe provider authenticator metadata for Security/settings surfaces."""

    model_config = ConfigDict(extra="forbid")

    external_identity_ref: UUID
    provider_code: str
    provider_email_address: str | None
    provider_email_private: bool | None


class PasskeyMethodResponse(BaseModel):
    """Safe passkey management metadata without credential/public-key/user-handle disclosure."""

    model_config = ConfigDict(extra="forbid")

    passkey_credential_ref: UUID
    label: str
    transports: tuple[str, ...]
    backup_eligible: bool
    backup_state: bool
    created_at: datetime
    last_used_at: datetime | None


class AuthenticationMethodsResponse(BaseModel):
    """Current Account-wide direct-authenticator and recovery-channel inventory."""

    model_config = ConfigDict(extra="forbid")

    password_established: bool
    providers: tuple[AuthenticationProviderMethodResponse, ...]
    passkeys: tuple[PasskeyMethodResponse, ...]
    active_passkey_count: int = Field(ge=0)
    recovery_eligible_email_count: int = Field(ge=0)


class PasswordEstablishRequest(BaseModel):
    """Establish the first PasswordCredential for the authenticated Account."""

    model_config = ConfigDict(extra="forbid")

    new_password: str = Field(min_length=1, max_length=4096)


def _passkey_method_response(method: PasskeyMethod) -> PasskeyMethodResponse:
    return PasskeyMethodResponse(
        passkey_credential_ref=method.passkey_credential_ref,
        label=method.label,
        transports=method.transports,
        backup_eligible=method.backup_eligible,
        backup_state=method.backup_state,
        created_at=method.created_at,
        last_used_at=method.last_used_at,
    )


def _methods_response(
    methods: AuthenticationMethods,
    *,
    passkeys: tuple[PasskeyMethod, ...],
) -> AuthenticationMethodsResponse:
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
        passkeys=tuple(_passkey_method_response(passkey) for passkey in passkeys),
        active_passkey_count=methods.active_passkey_count,
        recovery_eligible_email_count=methods.recovery_eligible_email_count,
    )


@router.get(
    "/methods",
    operation_id="auth_get_authentication_methods",
    response_model=AuthenticationMethodsResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def get_authentication_methods(
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    authenticator_service: AuthenticatorLifecycleDependency,
    runtime: ProviderRuntimeDependency,
) -> AuthenticationMethodsResponse:
    """Return safe Account-wide authenticator inventory for the admitted AuthSession."""
    admitted, _cookie_value = await required_session(
        request=request,
        response=response,
        auth_service=auth_service,
        require_csrf=False,
    )
    try:
        methods = await authenticator_service.authentication_methods(admitted=admitted)
        passkeys = (
            await runtime.passkey_service.list_passkeys(admitted=admitted)
            if runtime.passkey_service is not None
            else ()
        )
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc
    return _methods_response(methods, passkeys=passkeys)


@router.post(
    "/password/establish",
    operation_id="auth_establish_password",
    response_model=AuthenticatedSessionResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def establish_password(
    payload: PasswordEstablishRequest,
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    lifecycle_service: MultiAuthenticatorLifecycleDependency,
) -> AuthenticatedSessionResponse:
    """Establish the first password and rotate the bearer on the same AuthSession."""
    admitted, cookie_value = await required_session(
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
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc

    set_session_cookie(
        response,
        issued.session_secret.get_secret_value(),
        max_age_seconds=lifecycle_service.session_cookie_max_age_seconds,
    )
    return authenticated_response(issued)


@router.delete(
    "/password",
    operation_id="auth_remove_password",
    response_model=AuthenticatedSessionResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def remove_password(
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    lifecycle_service: MultiAuthenticatorLifecycleDependency,
) -> AuthenticatedSessionResponse:
    """Remove the password only when Account-wide anti-lockout remains satisfied."""
    admitted, cookie_value = await required_session(
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
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc

    set_session_cookie(
        response,
        issued.session_secret.get_secret_value(),
        max_age_seconds=lifecycle_service.session_cookie_max_age_seconds,
    )
    return authenticated_response(issued)
