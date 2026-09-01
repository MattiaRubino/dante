"""Public M5 Google/Apple/provider-continuation Access/Auth API."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, TypedDict
from urllib.parse import parse_qsl
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, ConfigDict, Field

from dante.auth.apple_flow import AppleAuthorizationCancelledError, AppleFlowService
from dante.auth.contracts import (
    AdmittedSession,
    AuthError,
    ProviderAuthenticated,
    ProviderAuthenticationBegun,
    ProviderAuthenticationResult,
    ProviderEnrollmentInvalidOrExpiredError,
    ProviderEnrollmentRequired,
    ProviderEnrollmentResult,
    ProviderLinkInvalidOrExpiredError,
    ProviderLinkRequired,
    ProviderPurpose,
    ProviderReturnTarget,
    ProviderUnavailableError,
)
from dante.auth.dependencies import get_auth_provider_flow_runtime, get_auth_service
from dante.auth.m5_http import (
    COMMON_M5_PROBLEM_RESPONSES,
    PROVIDER_ENROLLMENT_COOKIE_NAME,
    PROVIDER_LINK_COOKIE_NAME,
    AmbiguousFlowCookieError,
    authenticated_response,
    clear_flow_cookie,
    flow_cookie_value,
    required_session,
    set_flow_cookie,
    set_session_cookie,
    source_context,
    translate_m5_auth_error,
)
from dante.auth.provider_continuation import ProviderEnrollmentContinuation
from dante.auth.provider_flow import ProviderFlowService
from dante.auth.provider_flow_runtime import ProviderFlowRuntime
from dante.auth.service import AuthService
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]
ProviderRuntimeDependency = Annotated[ProviderFlowRuntime, Depends(get_auth_provider_flow_runtime)]

_FIXED_RETURN_TARGETS: dict[ProviderReturnTarget, str] = {
    ProviderReturnTarget.ACCESS: "/",
    ProviderReturnTarget.SECURITY: "/security",
}
_APPLE_FORM_FIELDS = frozenset({"state", "code", "id_token", "user", "error"})
_APPLE_FORM_MAX_LENGTHS = {
    "state": 256,
    "code": 4096,
    "id_token": 32768,
    "user": 8192,
    "error": 256,
}


class _AppleCallbackForm(TypedDict):
    state: str
    code: str | None
    id_token: str | None
    user: str | None
    error: str | None


class ProviderBeginRequest(BaseModel):
    """Begin one provider transaction for an explicit frozen security purpose."""

    model_config = ConfigDict(extra="forbid")

    purpose: ProviderPurpose
    return_target: ProviderReturnTarget


class GoogleAuthenticationBegunResponse(BaseModel):
    """Transient Google capabilities that the browser adapter must keep in memory only."""

    model_config = ConfigDict(extra="forbid")

    external_auth_transaction_ref: UUID
    state: str
    nonce: str
    expires_at: datetime


class GoogleAuthenticationCompleteRequest(BaseModel):
    """Complete one exact Google transaction using provider-returned credential evidence."""

    model_config = ConfigDict(extra="forbid")

    external_auth_transaction_ref: UUID
    state: str = Field(min_length=1, max_length=256)
    credential: str = Field(min_length=1, max_length=32768)


class AppleAuthenticationBegunResponse(BaseModel):
    """Server-authored Apple authorization URL for one persisted transaction."""

    model_config = ConfigDict(extra="forbid")

    authorization_url: str
    expires_at: datetime


class AppleNotificationRequest(BaseModel):
    """Signed Apple server-notification envelope; claims are trusted only after verification."""

    model_config = ConfigDict(extra="forbid")

    payload: str = Field(min_length=1, max_length=32768)


class ProviderAuthenticatedResponse(BaseModel):
    """Provider authentication converged on canonical DANTE AuthSession truth."""

    model_config = ConfigDict(extra="forbid")

    outcome: Literal["authenticated"] = "authenticated"
    authenticated: Literal[True] = True
    account_ref: UUID
    auth_session_ref: UUID
    recent_auth_at: datetime
    expires_at: datetime
    csrf_token: str


class ProviderLinkRequiredResponse(BaseModel):
    """Safe metadata for an explicit provider-first Account-link continuation."""

    model_config = ConfigDict(extra="forbid")

    outcome: Literal["link_required"] = "link_required"
    external_link_challenge_ref: UUID
    expires_at: datetime


class ProviderEnrollmentRequiredResponse(BaseModel):
    """Safe metadata for provider enrollment without exposing its continuation capability."""

    model_config = ConfigDict(extra="forbid")

    outcome: Literal["enrollment_required"] = "enrollment_required"
    external_signup_ref: UUID
    expires_at: datetime
    email_address: str | None
    verification_expires_at: datetime | None


ProviderAuthenticationResponse = (
    ProviderAuthenticatedResponse
    | ProviderLinkRequiredResponse
    | ProviderEnrollmentRequiredResponse
)
ProviderEnrollmentVerificationResponse = (
    ProviderAuthenticatedResponse | ProviderLinkRequiredResponse
)


class ProviderEnrollmentEmailRequest(BaseModel):
    """Set or replace the DANTE-owned mailbox proof target for provider enrollment."""

    model_config = ConfigDict(extra="forbid")

    email: str = Field(min_length=1, max_length=320)


class ProviderEnrollmentVerificationRequest(BaseModel):
    """Present the six-digit DANTE mailbox proof for the current provider enrollment."""

    model_config = ConfigDict(extra="forbid")

    code: str = Field(pattern=r"^[0-9]{6}$")


class ProviderEnrollmentResendRequest(BaseModel):
    """Explicit empty command body for resend under the flow-cookie continuation."""

    model_config = ConfigDict(extra="forbid")


class ProviderLinkConfirmRequest(BaseModel):
    """Explicit empty confirmation body; authority comes from session, CSRF and flow cookie."""

    model_config = ConfigDict(extra="forbid")


class ProviderLinkResponse(BaseModel):
    """Safe provider-link metadata without Account target or provider subject disclosure."""

    model_config = ConfigDict(extra="forbid")

    external_link_challenge_ref: UUID
    provider_code: str
    expires_at: datetime


def _google_service(runtime: ProviderFlowRuntime) -> ProviderFlowService:
    service = runtime.service
    if service is None:
        raise ProviderUnavailableError(retryable=False)
    return service


def _apple_service(runtime: ProviderFlowRuntime) -> AppleFlowService:
    service = runtime.apple_service
    if service is None:
        raise ProviderUnavailableError(retryable=False)
    return service


def _required_flow_cookie(request: Request, *, name: str, enrollment: bool) -> str:
    error: AuthError = (
        ProviderEnrollmentInvalidOrExpiredError()
        if enrollment
        else ProviderLinkInvalidOrExpiredError()
    )
    try:
        value = flow_cookie_value(request, name=name)
    except AmbiguousFlowCookieError as exc:
        raise translate_m5_auth_error(error) from exc
    if value is None:
        raise translate_m5_auth_error(error)
    return value


async def _begin_session_context(
    *,
    payload: ProviderBeginRequest,
    request: Request,
    response: Response,
    auth_service: AuthService,
) -> tuple[AdmittedSession | None, str | None]:
    if payload.purpose is ProviderPurpose.SIGN_IN:
        return None, None
    admitted, cookie = await required_session(
        request=request,
        response=response,
        auth_service=auth_service,
        require_csrf=True,
    )
    return admitted, cookie


def _provider_authenticated(result: ProviderAuthenticated) -> ProviderAuthenticatedResponse:
    session = authenticated_response(result.session)
    return ProviderAuthenticatedResponse(**session.model_dump())


def _provider_enrollment(result: ProviderEnrollmentRequired) -> ProviderEnrollmentRequiredResponse:
    return ProviderEnrollmentRequiredResponse(
        external_signup_ref=result.external_signup_ref,
        expires_at=result.expires_at,
        email_address=result.email_address,
        verification_expires_at=result.verification_expires_at,
    )


def _provider_link(result: ProviderLinkRequired) -> ProviderLinkRequiredResponse:
    return ProviderLinkRequiredResponse(
        external_link_challenge_ref=result.external_link_challenge_ref,
        expires_at=result.expires_at,
    )


def _apply_provider_result_cookies(
    *,
    result: ProviderAuthenticationResult | ProviderEnrollmentResult,
    response: Response,
    auth_service: AuthService,
) -> None:
    if isinstance(result, ProviderAuthenticated):
        clear_flow_cookie(response, name=PROVIDER_LINK_COOKIE_NAME)
        clear_flow_cookie(response, name=PROVIDER_ENROLLMENT_COOKIE_NAME)
        set_session_cookie(
            response,
            result.session.session_secret.get_secret_value(),
            max_age_seconds=auth_service.session_cookie_max_age_seconds,
        )
        return
    if isinstance(result, ProviderLinkRequired):
        clear_flow_cookie(response, name=PROVIDER_ENROLLMENT_COOKIE_NAME)
        set_flow_cookie(
            response,
            name=PROVIDER_LINK_COOKIE_NAME,
            continuation_secret=result.continuation_secret.get_secret_value(),
            expires_at=result.expires_at,
        )
        return
    if isinstance(result, ProviderEnrollmentRequired):
        clear_flow_cookie(response, name=PROVIDER_LINK_COOKIE_NAME)
        set_flow_cookie(
            response,
            name=PROVIDER_ENROLLMENT_COOKIE_NAME,
            continuation_secret=result.continuation_secret.get_secret_value(),
            expires_at=result.expires_at,
        )
        return
    raise TypeError("unexpected provider authentication result")


def _provider_result_response(
    result: ProviderAuthenticationResult,
) -> ProviderAuthenticationResponse:
    if isinstance(result, ProviderAuthenticated):
        return _provider_authenticated(result)
    if isinstance(result, ProviderLinkRequired):
        return _provider_link(result)
    if isinstance(result, ProviderEnrollmentRequired):
        return _provider_enrollment(result)
    raise TypeError("unexpected provider authentication result")


def _provider_enrollment_result_response(
    result: ProviderEnrollmentResult,
) -> ProviderEnrollmentVerificationResponse:
    if isinstance(result, ProviderAuthenticated):
        return _provider_authenticated(result)
    if isinstance(result, ProviderLinkRequired):
        return _provider_link(result)
    raise TypeError("unexpected provider enrollment result")


async def _resolve_enrollment(
    *,
    request: Request,
    runtime: ProviderFlowRuntime,
) -> tuple[ProviderEnrollmentContinuation, str]:
    secret = _required_flow_cookie(
        request,
        name=PROVIDER_ENROLLMENT_COOKIE_NAME,
        enrollment=True,
    )
    try:
        continuation = await runtime.continuation_service.resolve_enrollment(secret)
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc
    return continuation, secret


async def _inspect_enrollment(
    *,
    runtime: ProviderFlowRuntime,
    continuation: ProviderEnrollmentContinuation,
    secret: str,
) -> ProviderEnrollmentRequired:
    try:
        if continuation.provider_code == "google":
            return await _google_service(runtime).inspect_provider_enrollment(
                external_signup_ref=continuation.external_signup_ref,
                continuation_secret=secret,
            )
        if continuation.provider_code == "apple":
            return await _apple_service(runtime).inspect_provider_enrollment(
                external_signup_ref=continuation.external_signup_ref,
                continuation_secret=secret,
            )
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc
    raise RuntimeError("provider continuation owns unsupported provider")


def _parse_apple_form(raw_body: bytes) -> _AppleCallbackForm:
    try:
        encoded = raw_body.decode("utf-8", errors="strict")
        pairs = parse_qsl(
            encoded,
            keep_blank_values=True,
            strict_parsing=True,
            encoding="utf-8",
            errors="strict",
            max_num_fields=len(_APPLE_FORM_FIELDS),
        )
    except (UnicodeDecodeError, ValueError) as exc:
        raise ProblemError(
            status=400,
            code="request.malformed",
            category="validation",
            title="Malformed request",
            detail="The Apple callback form could not be parsed safely.",
        ) from exc

    values: dict[str, str] = {}
    for key, value in pairs:
        if key not in _APPLE_FORM_FIELDS or key in values:
            raise ProblemError(
                status=400,
                code="request.malformed",
                category="validation",
                title="Malformed request",
                detail="The Apple callback form contains unsupported or duplicate fields.",
            )
        if len(value) > _APPLE_FORM_MAX_LENGTHS[key]:
            raise ProblemError(
                status=400,
                code="request.malformed",
                category="validation",
                title="Malformed request",
                detail="The Apple callback form exceeds the accepted field bounds.",
            )
        values[key] = value

    state = values.get("state")
    if state is None or not state:
        raise ProblemError(
            status=400,
            code="request.malformed",
            category="validation",
            title="Malformed request",
            detail="The Apple callback omitted its required state.",
        )
    return {
        "state": state,
        "code": values.get("code") or None,
        "id_token": values.get("id_token") or None,
        "user": values.get("user") or None,
        "error": values.get("error") or None,
    }


@router.post(
    "/google/begin",
    operation_id="auth_begin_google_authentication",
    response_model=GoogleAuthenticationBegunResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def begin_google_authentication(
    payload: ProviderBeginRequest,
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    runtime: ProviderRuntimeDependency,
) -> GoogleAuthenticationBegunResponse:
    admitted, session_secret = await _begin_session_context(
        payload=payload,
        request=request,
        response=response,
        auth_service=auth_service,
    )
    try:
        begun: ProviderAuthenticationBegun = await _google_service(runtime).begin_google(
            purpose=payload.purpose,
            return_target=payload.return_target,
            source_context=source_context(request),
            admitted=admitted,
            presented_session_secret=session_secret,
        )
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc
    return GoogleAuthenticationBegunResponse(
        external_auth_transaction_ref=begun.external_auth_transaction_ref,
        state=begun.state.get_secret_value(),
        nonce=begun.nonce.get_secret_value(),
        expires_at=begun.expires_at,
    )


@router.post(
    "/google/complete",
    operation_id="auth_complete_google_authentication",
    response_model=ProviderAuthenticationResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def complete_google_authentication(
    payload: GoogleAuthenticationCompleteRequest,
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    runtime: ProviderRuntimeDependency,
) -> ProviderAuthenticationResponse:
    try:
        result = await _google_service(runtime).complete_google(
            external_auth_transaction_ref=payload.external_auth_transaction_ref,
            state=payload.state,
            credential=payload.credential,
            source_context=source_context(request),
        )
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc
    _apply_provider_result_cookies(result=result, response=response, auth_service=auth_service)
    return _provider_result_response(result)


@router.post(
    "/apple/begin",
    operation_id="auth_begin_apple_authentication",
    response_model=AppleAuthenticationBegunResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def begin_apple_authentication(
    payload: ProviderBeginRequest,
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    runtime: ProviderRuntimeDependency,
) -> AppleAuthenticationBegunResponse:
    admitted, session_secret = await _begin_session_context(
        payload=payload,
        request=request,
        response=response,
        auth_service=auth_service,
    )
    try:
        begun = await _apple_service(runtime).begin_apple(
            purpose=payload.purpose,
            return_target=payload.return_target,
            source_context=source_context(request),
            admitted=admitted,
            presented_session_secret=session_secret,
        )
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc
    return AppleAuthenticationBegunResponse(
        authorization_url=begun.authorization_url,
        expires_at=begun.expires_at,
    )


@router.post(
    "/apple/callback",
    operation_id="auth_handle_apple_callback",
    status_code=303,
    response_model=None,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def handle_apple_callback(
    request: Request,
    auth_service: AuthServiceDependency,
    runtime: ProviderRuntimeDependency,
) -> RedirectResponse:
    form = _parse_apple_form(await request.body())
    state = form["state"]
    try:
        return_target = await runtime.continuation_service.resolve_apple_return_target(state)
        result = await _apple_service(runtime).complete_apple(
            state=state,
            code=form["code"],
            id_token=form["id_token"],
            user=form["user"],
            error=form["error"],
            source_context=source_context(request),
        )
    except AppleAuthorizationCancelledError:
        return RedirectResponse(url=_FIXED_RETURN_TARGETS[return_target], status_code=303)
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc

    redirect = RedirectResponse(url=_FIXED_RETURN_TARGETS[return_target], status_code=303)
    _apply_provider_result_cookies(result=result, response=redirect, auth_service=auth_service)
    return redirect


@router.post(
    "/apple/notifications",
    operation_id="auth_process_apple_notification",
    status_code=204,
    response_model=None,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def process_apple_notification(
    payload: AppleNotificationRequest,
    runtime: ProviderRuntimeDependency,
) -> None:
    try:
        await _apple_service(runtime).process_notification(payload.payload)
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc


@router.get(
    "/provider-enrollment",
    operation_id="auth_get_provider_enrollment",
    response_model=ProviderEnrollmentRequiredResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def get_provider_enrollment(
    request: Request,
    runtime: ProviderRuntimeDependency,
) -> ProviderEnrollmentRequiredResponse:
    continuation, secret = await _resolve_enrollment(request=request, runtime=runtime)
    result = await _inspect_enrollment(runtime=runtime, continuation=continuation, secret=secret)
    return _provider_enrollment(result)


@router.post(
    "/provider-enrollment/email",
    operation_id="auth_set_provider_enrollment_email",
    response_model=ProviderEnrollmentRequiredResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def set_provider_enrollment_email(
    payload: ProviderEnrollmentEmailRequest,
    request: Request,
    response: Response,
    runtime: ProviderRuntimeDependency,
) -> ProviderEnrollmentRequiredResponse:
    continuation, secret = await _resolve_enrollment(request=request, runtime=runtime)
    try:
        if continuation.provider_code == "google":
            result = await _google_service(runtime).set_provider_enrollment_email(
                external_signup_ref=continuation.external_signup_ref,
                continuation_secret=secret,
                email=payload.email,
                source_context=source_context(request),
            )
        elif continuation.provider_code == "apple":
            result = await _apple_service(runtime).set_provider_enrollment_email(
                external_signup_ref=continuation.external_signup_ref,
                continuation_secret=secret,
                email=payload.email,
                source_context=source_context(request),
            )
        else:
            raise RuntimeError("provider continuation owns unsupported provider")
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc
    set_flow_cookie(
        response,
        name=PROVIDER_ENROLLMENT_COOKIE_NAME,
        continuation_secret=result.continuation_secret.get_secret_value(),
        expires_at=result.expires_at,
    )
    return _provider_enrollment(result)


@router.post(
    "/provider-enrollment/resend",
    operation_id="auth_resend_provider_enrollment_verification",
    response_model=ProviderEnrollmentRequiredResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def resend_provider_enrollment_verification(
    _payload: ProviderEnrollmentResendRequest,
    request: Request,
    response: Response,
    runtime: ProviderRuntimeDependency,
) -> ProviderEnrollmentRequiredResponse:
    continuation, secret = await _resolve_enrollment(request=request, runtime=runtime)
    try:
        if continuation.provider_code == "google":
            result = await _google_service(runtime).resend_provider_enrollment_verification(
                external_signup_ref=continuation.external_signup_ref,
                continuation_secret=secret,
                source_context=source_context(request),
            )
        elif continuation.provider_code == "apple":
            result = await _apple_service(runtime).resend_provider_enrollment_verification(
                external_signup_ref=continuation.external_signup_ref,
                continuation_secret=secret,
                source_context=source_context(request),
            )
        else:
            raise RuntimeError("provider continuation owns unsupported provider")
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc
    set_flow_cookie(
        response,
        name=PROVIDER_ENROLLMENT_COOKIE_NAME,
        continuation_secret=result.continuation_secret.get_secret_value(),
        expires_at=result.expires_at,
    )
    return _provider_enrollment(result)


@router.post(
    "/provider-enrollment/verify",
    operation_id="auth_verify_provider_enrollment",
    response_model=ProviderEnrollmentVerificationResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def verify_provider_enrollment(
    payload: ProviderEnrollmentVerificationRequest,
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    runtime: ProviderRuntimeDependency,
) -> ProviderEnrollmentVerificationResponse:
    continuation, secret = await _resolve_enrollment(request=request, runtime=runtime)
    try:
        if continuation.provider_code == "google":
            result = await _google_service(runtime).verify_provider_enrollment(
                external_signup_ref=continuation.external_signup_ref,
                continuation_secret=secret,
                code=payload.code,
                source_context=source_context(request),
            )
        elif continuation.provider_code == "apple":
            result = await _apple_service(runtime).verify_provider_enrollment(
                external_signup_ref=continuation.external_signup_ref,
                continuation_secret=secret,
                code=payload.code,
                source_context=source_context(request),
            )
        else:
            raise RuntimeError("provider continuation owns unsupported provider")
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc
    _apply_provider_result_cookies(result=result, response=response, auth_service=auth_service)
    return _provider_enrollment_result_response(result)


@router.get(
    "/provider-link",
    operation_id="auth_get_provider_link",
    response_model=ProviderLinkResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def get_provider_link(
    request: Request,
    runtime: ProviderRuntimeDependency,
) -> ProviderLinkResponse:
    secret = _required_flow_cookie(request, name=PROVIDER_LINK_COOKIE_NAME, enrollment=False)
    try:
        continuation = await runtime.continuation_service.resolve_link(secret)
        result = await runtime.authenticator_service.inspect_provider_link(
            external_link_challenge_ref=continuation.external_link_challenge_ref,
            continuation_secret=secret,
        )
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc
    return ProviderLinkResponse(
        external_link_challenge_ref=result.external_link_challenge_ref,
        provider_code=result.provider_code,
        expires_at=result.expires_at,
    )


@router.post(
    "/provider-link/confirm",
    operation_id="auth_confirm_provider_link",
    response_model=ProviderAuthenticatedResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def confirm_provider_link(
    _payload: ProviderLinkConfirmRequest,
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    runtime: ProviderRuntimeDependency,
) -> ProviderAuthenticatedResponse:
    admitted, session_secret = await required_session(
        request=request,
        response=response,
        auth_service=auth_service,
        require_csrf=True,
    )
    secret = _required_flow_cookie(request, name=PROVIDER_LINK_COOKIE_NAME, enrollment=False)
    try:
        continuation = await runtime.continuation_service.resolve_link(secret)
        issued = await runtime.authenticator_service.confirm_provider_link(
            admitted=admitted,
            presented_session_secret=session_secret,
            external_link_challenge_ref=continuation.external_link_challenge_ref,
            continuation_secret=secret,
        )
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc
    clear_flow_cookie(response, name=PROVIDER_LINK_COOKIE_NAME)
    set_session_cookie(
        response,
        issued.session_secret.get_secret_value(),
        max_age_seconds=auth_service.session_cookie_max_age_seconds,
    )
    session = authenticated_response(issued)
    return ProviderAuthenticatedResponse(**session.model_dump())


@router.delete(
    "/providers/{external_identity_ref}",
    operation_id="auth_unlink_provider",
    response_model=ProviderAuthenticatedResponse,
    responses=COMMON_M5_PROBLEM_RESPONSES,
)
async def unlink_provider(
    external_identity_ref: UUID,
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    runtime: ProviderRuntimeDependency,
) -> ProviderAuthenticatedResponse:
    admitted, session_secret = await required_session(
        request=request,
        response=response,
        auth_service=auth_service,
        require_csrf=True,
    )
    try:
        issued = await runtime.authenticator_service.unlink_provider(
            admitted=admitted,
            presented_session_secret=session_secret,
            external_identity_ref=external_identity_ref,
        )
    except AuthError as exc:
        raise translate_m5_auth_error(exc) from exc
    set_session_cookie(
        response,
        issued.session_secret.get_secret_value(),
        max_age_seconds=auth_service.session_cookie_max_age_seconds,
    )
    session = authenticated_response(issued)
    return ProviderAuthenticatedResponse(**session.model_dump())
