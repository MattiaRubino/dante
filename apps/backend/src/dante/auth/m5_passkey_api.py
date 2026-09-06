"""Public M5 WebAuthn/passkey Access/Auth API."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from dante.auth.api import AuthenticatedSessionResponse
from dante.auth.contracts import AuthError, PasskeyCeremonyBegun, ProviderUnavailableError
from dante.auth.dependencies import (
    get_auth_provider_flow_runtime,
    get_auth_service,
    single_header_value,
)
from dante.auth.m5_http import (
    COMMON_M5_PROBLEM_RESPONSES,
    authenticated_response,
    required_session,
    set_session_cookie,
    source_context,
    translate_m5_auth_error,
)
from dante.auth.passkey_flow import PasskeyFlowService
from dante.auth.provider_flow_runtime import ProviderFlowRuntime
from dante.auth.service import AuthService
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/auth/passkeys", tags=["auth"])

AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]
ProviderRuntimeDependency = Annotated[ProviderFlowRuntime, Depends(get_auth_provider_flow_runtime)]

_Base64Url = Annotated[str, Field(min_length=1, max_length=32768, pattern=r"^[A-Za-z0-9_-]+$")]
_Transport = Annotated[str, Field(min_length=1, max_length=32)]


class PasskeyBeginRequest(BaseModel):
    """Explicit empty command body for a browser-owned WebAuthn ceremony begin."""

    model_config = ConfigDict(extra="forbid")


class RegistrationAuthenticatorResponse(BaseModel):
    """Bounded browser registration evidence consumed by python-fido2."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    client_data_json: _Base64Url = Field(alias="clientDataJSON")
    attestation_object: _Base64Url = Field(alias="attestationObject")


class AssertionAuthenticatorResponse(BaseModel):
    """Bounded browser assertion evidence consumed by python-fido2."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    client_data_json: _Base64Url = Field(alias="clientDataJSON")
    authenticator_data: _Base64Url = Field(alias="authenticatorData")
    signature: _Base64Url
    user_handle: _Base64Url | None = Field(default=None, alias="userHandle")


class RegistrationCredential(BaseModel):
    """Exact WebAuthn registration credential shape admitted by the M5 adapter."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    credential_id: _Base64Url = Field(alias="id")
    raw_id: _Base64Url = Field(alias="rawId")
    credential_type: Literal["public-key"] = Field(alias="type")
    response: RegistrationAuthenticatorResponse
    authenticator_attachment: str | None = Field(
        default=None,
        alias="authenticatorAttachment",
        max_length=64,
    )
    client_extension_results: dict[str, JsonValue] = Field(
        default_factory=dict,
        alias="clientExtensionResults",
    )


class AssertionCredential(BaseModel):
    """Exact WebAuthn assertion credential shape admitted by the M5 adapter."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    credential_id: _Base64Url = Field(alias="id")
    raw_id: _Base64Url = Field(alias="rawId")
    credential_type: Literal["public-key"] = Field(alias="type")
    response: AssertionAuthenticatorResponse
    authenticator_attachment: str | None = Field(
        default=None,
        alias="authenticatorAttachment",
        max_length=64,
    )
    client_extension_results: dict[str, JsonValue] = Field(
        default_factory=dict,
        alias="clientExtensionResults",
    )


class PasskeyCeremonyResponse(BaseModel):
    """Public browser WebAuthn options plus one non-secret durable ceremony reference."""

    model_config = ConfigDict(extra="forbid")

    webauthn_challenge_ref: UUID
    options: dict[str, JsonValue]
    expires_at: datetime


class PasskeyRegistrationCompleteRequest(BaseModel):
    """Complete resident passkey registration against one exact persisted challenge."""

    model_config = ConfigDict(extra="forbid")

    webauthn_challenge_ref: UUID
    response: RegistrationCredential
    label: str = Field(min_length=1, max_length=100)
    transports: tuple[_Transport, ...] = Field(default=(), max_length=8)


class PasskeyAuthenticationCompleteRequest(BaseModel):
    """Complete username-less passkey authentication."""

    model_config = ConfigDict(extra="forbid")

    webauthn_challenge_ref: UUID
    response: AssertionCredential


class PasskeyReauthenticationCompleteRequest(BaseModel):
    """Complete passkey reauthentication on the exact current AuthSession."""

    model_config = ConfigDict(extra="forbid")

    webauthn_challenge_ref: UUID
    response: AssertionCredential


class PasskeyUpdateRequest(BaseModel):
    """Update only user-facing passkey label metadata."""

    model_config = ConfigDict(extra="forbid")

    label: str = Field(min_length=1, max_length=100)


def _passkey_service(runtime: ProviderFlowRuntime) -> PasskeyFlowService:
    service = runtime.passkey_service
    if service is None:
        raise ProviderUnavailableError(retryable=False)
    return service


def _origin(request: Request) -> str:
    origin = single_header_value(request.scope, "Origin")
    if origin is None:
        raise ProblemError(
            status=403,
            code="security.csrf_failed",
            category="security",
            title="Request rejected",
            detail="The request could not satisfy the browser security policy.",
        )
    return origin


def _ceremony_response(begun: PasskeyCeremonyBegun) -> PasskeyCeremonyResponse:
    return PasskeyCeremonyResponse(
        webauthn_challenge_ref=begun.webauthn_challenge_ref,
        options=begun.options,
        expires_at=begun.expires_at,
    )


def _wire_registration(response: RegistrationCredential) -> dict[str, Any]:
    return response.model_dump(mode="json", by_alias=True, exclude_none=True)


def _wire_assertion(response: AssertionCredential) -> dict[str, Any]:
    return response.model_dump(mode="json", by_alias=True, exclude_none=True)


@router.post(
    "/registration/begin",
    operation_id="auth_begin_passkey_registration",
    response_model=PasskeyCeremonyResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def begin_passkey_registration(
    _payload: PasskeyBeginRequest,
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    runtime: ProviderRuntimeDependency,
) -> PasskeyCeremonyResponse:
    admitted, session_secret = await required_session(
        request=request,
        response=response,
        auth_service=auth_service,
        require_csrf=True,
    )
    try:
        begun = await _passkey_service(runtime).begin_registration(
            admitted=admitted,
            presented_session_secret=session_secret,
            expected_origin=_origin(request),
        )
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc
    return _ceremony_response(begun)


@router.post(
    "/registration/complete",
    operation_id="auth_complete_passkey_registration",
    response_model=AuthenticatedSessionResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def complete_passkey_registration(
    payload: PasskeyRegistrationCompleteRequest,
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    runtime: ProviderRuntimeDependency,
) -> AuthenticatedSessionResponse:
    admitted, session_secret = await required_session(
        request=request,
        response=response,
        auth_service=auth_service,
        require_csrf=True,
    )
    try:
        issued = await _passkey_service(runtime).complete_registration(
            admitted=admitted,
            presented_session_secret=session_secret,
            webauthn_challenge_ref=payload.webauthn_challenge_ref,
            response=_wire_registration(payload.response),
            label=payload.label,
            transports=payload.transports,
        )
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc
    set_session_cookie(
        response,
        issued.session_secret.get_secret_value(),
        max_age_seconds=auth_service.session_cookie_max_age_seconds,
    )
    return authenticated_response(issued)


@router.post(
    "/authentication/begin",
    operation_id="auth_begin_passkey_authentication",
    response_model=PasskeyCeremonyResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def begin_passkey_authentication(
    _payload: PasskeyBeginRequest,
    request: Request,
    runtime: ProviderRuntimeDependency,
) -> PasskeyCeremonyResponse:
    try:
        begun = await _passkey_service(runtime).begin_authentication(
            expected_origin=_origin(request),
            source_context=source_context(request),
        )
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc
    return _ceremony_response(begun)


@router.post(
    "/authentication/complete",
    operation_id="auth_complete_passkey_authentication",
    response_model=AuthenticatedSessionResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def complete_passkey_authentication(
    payload: PasskeyAuthenticationCompleteRequest,
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    runtime: ProviderRuntimeDependency,
) -> AuthenticatedSessionResponse:
    try:
        issued = await _passkey_service(runtime).complete_authentication(
            webauthn_challenge_ref=payload.webauthn_challenge_ref,
            response=_wire_assertion(payload.response),
            source_context=source_context(request),
        )
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc
    set_session_cookie(
        response,
        issued.session_secret.get_secret_value(),
        max_age_seconds=auth_service.session_cookie_max_age_seconds,
    )
    return authenticated_response(issued)


@router.post(
    "/reauthentication/begin",
    operation_id="auth_begin_passkey_reauthentication",
    response_model=PasskeyCeremonyResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def begin_passkey_reauthentication(
    _payload: PasskeyBeginRequest,
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    runtime: ProviderRuntimeDependency,
) -> PasskeyCeremonyResponse:
    admitted, session_secret = await required_session(
        request=request,
        response=response,
        auth_service=auth_service,
        require_csrf=True,
    )
    try:
        begun = await _passkey_service(runtime).begin_reauthentication(
            admitted=admitted,
            presented_session_secret=session_secret,
            expected_origin=_origin(request),
        )
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc
    return _ceremony_response(begun)


@router.post(
    "/reauthentication/complete",
    operation_id="auth_complete_passkey_reauthentication",
    response_model=AuthenticatedSessionResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def complete_passkey_reauthentication(
    payload: PasskeyReauthenticationCompleteRequest,
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    runtime: ProviderRuntimeDependency,
) -> AuthenticatedSessionResponse:
    admitted, session_secret = await required_session(
        request=request,
        response=response,
        auth_service=auth_service,
        require_csrf=True,
    )
    try:
        issued = await _passkey_service(runtime).complete_reauthentication(
            admitted=admitted,
            presented_session_secret=session_secret,
            webauthn_challenge_ref=payload.webauthn_challenge_ref,
            response=_wire_assertion(payload.response),
        )
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc
    set_session_cookie(
        response,
        issued.session_secret.get_secret_value(),
        max_age_seconds=auth_service.session_cookie_max_age_seconds,
    )
    return authenticated_response(issued)


@router.patch(
    "/{passkey_credential_ref}",
    operation_id="auth_update_passkey",
    status_code=204,
    response_model=None,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def update_passkey(
    passkey_credential_ref: UUID,
    payload: PasskeyUpdateRequest,
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    runtime: ProviderRuntimeDependency,
) -> None:
    admitted, session_secret = await required_session(
        request=request,
        response=response,
        auth_service=auth_service,
        require_csrf=True,
    )
    try:
        await _passkey_service(runtime).update_label(
            admitted=admitted,
            presented_session_secret=session_secret,
            passkey_credential_ref=passkey_credential_ref,
            label=payload.label,
        )
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc


@router.delete(
    "/{passkey_credential_ref}",
    operation_id="auth_remove_passkey",
    response_model=AuthenticatedSessionResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def remove_passkey(
    passkey_credential_ref: UUID,
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    runtime: ProviderRuntimeDependency,
) -> AuthenticatedSessionResponse:
    admitted, session_secret = await required_session(
        request=request,
        response=response,
        auth_service=auth_service,
        require_csrf=True,
    )
    try:
        issued = await _passkey_service(runtime).remove_passkey(
            admitted=admitted,
            presented_session_secret=session_secret,
            passkey_credential_ref=passkey_credential_ref,
        )
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc
    set_session_cookie(
        response,
        issued.session_secret.get_secret_value(),
        max_age_seconds=auth_service.session_cookie_max_age_seconds,
    )
    return authenticated_response(issued)
