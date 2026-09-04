"""Public DANTE Access/Auth application-intent API."""

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
    EmailDeliveryUnavailableError,
    ExistingAccountSignupResult,
    InvalidCredentialsError,
    IssuedSession,
    LifecycleRateLimitedError,
    PasswordCompromisedError,
    ReauthenticationRequiredError,
    RecoveryInvalidOrExpiredError,
    SigninRateLimitedError,
    SignupResendCooldownError,
    VerificationAttemptsExhaustedError,
    VerificationInvalidOrExpiredError,
)
from dante.auth.dependencies import (
    get_auth_lifecycle_service,
    get_auth_service,
    single_header_value,
)
from dante.auth.lifecycle import AuthLifecycleService
from dante.auth.service import AuthService
from dante.auth.sessions import (
    CSRF_HEADER_NAME,
    SESSION_COOKIE_NAME,
    AmbiguousSessionCookieError,
    csrf_token_matches,
    decode_session_secret,
    session_cookie_value,
    session_secret_verifier_from_raw,
)
from dante.platform.http.problem import (
    ProblemDetails,
    ProblemError,
    ProblemFieldError,
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]
AuthLifecycleServiceDependency = Annotated[
    AuthLifecycleService,
    Depends(get_auth_lifecycle_service),
]


class SignInRequest(BaseModel):
    """Bounded first-party email/password signin request."""

    model_config = ConfigDict(extra="forbid")

    email: str = Field(min_length=1, max_length=320)
    password: str = Field(min_length=1, max_length=4096)


class SignupRequest(BaseModel):
    """Begin one isolated password-signup challenge without creating an Account."""

    model_config = ConfigDict(extra="forbid")

    email: str = Field(min_length=1, max_length=320)
    password: str = Field(min_length=1, max_length=4096)


class SignupVerificationRequest(BaseModel):
    """Present one six-digit OTP for a specific public signup reference."""

    model_config = ConfigDict(extra="forbid")

    signup_ref: UUID
    code: str = Field(pattern=r"^[0-9]{6}$")


class SignupResendRequest(BaseModel):
    """Rotate the OTP owned by one pending signup challenge."""

    model_config = ConfigDict(extra="forbid")

    signup_ref: UUID


class PasswordRecoveryRequest(BaseModel):
    """Request neutral password-recovery delivery semantics for one email."""

    model_config = ConfigDict(extra="forbid")

    email: str = Field(min_length=1, max_length=320)


class PasswordRecoveryValidationRequest(BaseModel):
    """Validate one high-entropy recovery bearer without consuming it."""

    model_config = ConfigDict(extra="forbid")

    password_recovery_ref: UUID
    secret: str = Field(min_length=1, max_length=128)


class PasswordResetRequest(BaseModel):
    """Consume one recovery proof and establish a replacement password."""

    model_config = ConfigDict(extra="forbid")

    password_recovery_ref: UUID
    secret: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=1, max_length=4096)


class ReauthenticateRequest(BaseModel):
    """Present fresh password evidence for the current AuthSession."""

    model_config = ConfigDict(extra="forbid")

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


class SignupAuthenticatedResponse(AuthenticatedSessionResponse):
    """Successful verified signup plus the newly established AuthSession."""

    outcome: Literal["authenticated"] = "authenticated"


class ExistingAccountSignupResponse(BaseModel):
    """Mailbox proof succeeded but that canonical email already belongs to an Account."""

    model_config = ConfigDict(extra="forbid")

    outcome: Literal["existing_account"] = "existing_account"


class SignupCreatedResponse(BaseModel):
    """Public non-secret metadata for one pending signup challenge."""

    model_config = ConfigDict(extra="forbid")

    verification_required: Literal[True] = True
    signup_ref: UUID
    signup_expires_at: datetime
    verification_expires_at: datetime


class RecoveryAcceptedResponse(BaseModel):
    """Neutral recovery-initiation acknowledgement."""

    model_config = ConfigDict(extra="forbid")

    accepted: Literal[True] = True


class RecoveryValidationResponse(BaseModel):
    """Non-consuming public recovery-proof validation result."""

    model_config = ConfigDict(extra="forbid")

    valid: bool


class UnauthenticatedSessionResponse(BaseModel):
    """Unauthenticated bootstrap representation."""

    model_config = ConfigDict(extra="forbid")

    authenticated: Literal[False] = False


SessionResponse = AuthenticatedSessionResponse | UnauthenticatedSessionResponse
SignupVerificationResponse = SignupAuthenticatedResponse | ExistingAccountSignupResponse

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


def _signup_authenticated_response(session: IssuedSession) -> SignupAuthenticatedResponse:
    authenticated = _authenticated_response(session)
    return SignupAuthenticatedResponse(**authenticated.model_dump())


def _signup_created_response(created: Any) -> SignupCreatedResponse:
    return SignupCreatedResponse(
        signup_ref=created.signup_ref,
        signup_expires_at=created.signup_expires_at,
        verification_expires_at=created.verification_expires_at,
    )


def _session_cookie(request: Request) -> str | None:
    raw_headers = list(request.scope.get("headers", []))
    return session_cookie_value(raw_headers)


def _source_context(request: Request) -> str:
    """Return a bounded process-local abuse-control source, never an identity authority."""
    client = request.client
    return client.host if client is not None and client.host else "unknown"


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
            title="Password not accepted",
            detail="This password cannot be accepted by the current security policy.",
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
    if isinstance(exc, LifecycleRateLimitedError):
        return ProblemError(
            status=429,
            code=exc.code,
            category="rate_limit",
            title="Too many attempts",
            detail="Too many authentication lifecycle requests were received.",
            retryable=True,
            headers={"Retry-After": str(exc.retry_after_seconds)},
        )
    if isinstance(exc, SignupResendCooldownError):
        return ProblemError(
            status=429,
            code="auth.signup_resend_cooldown",
            category="rate_limit",
            title="Verification code recently sent",
            detail="A new verification code cannot be sent yet.",
            retryable=True,
            headers={"Retry-After": str(exc.retry_after_seconds)},
        )
    if isinstance(exc, VerificationAttemptsExhaustedError):
        return ProblemError(
            status=429,
            code="auth.verification_attempts_exhausted",
            category="rate_limit",
            title="Verification attempts exhausted",
            detail="The current verification code can no longer be used.",
        )
    if isinstance(exc, VerificationInvalidOrExpiredError):
        return ProblemError(
            status=401,
            code="auth.verification_invalid_or_expired",
            category="authentication",
            title="Verification failed",
            detail="The verification proof is invalid or expired.",
        )
    if isinstance(exc, RecoveryInvalidOrExpiredError):
        return ProblemError(
            status=401,
            code="auth.recovery_invalid_or_expired",
            category="authentication",
            title="Recovery proof rejected",
            detail="The recovery proof is invalid or expired.",
        )
    if isinstance(exc, ReauthenticationRequiredError):
        return ProblemError(
            status=401,
            code="auth.reauthentication_required",
            category="authentication",
            title="Reauthentication required",
            detail="Fresh authentication evidence is required for this operation.",
        )
    if isinstance(exc, EmailDeliveryUnavailableError):
        return ProblemError(
            status=503,
            code="auth.email_delivery_unavailable",
            category="dependency",
            title="Email delivery unavailable",
            detail="The email delivery boundary cannot safely accept the request right now.",
            retryable=True,
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


@router.post(
    "/signup",
    operation_id="auth_begin_signup",
    response_model=SignupCreatedResponse,
    responses=_PROBLEM_RESPONSES,
)
async def begin_signup(
    payload: SignupRequest,
    request: Request,
    service: AuthLifecycleServiceDependency,
) -> SignupCreatedResponse:
    """Create a bounded pending signup challenge without creating canonical Account state."""
    try:
        created = await service.create_signup(
            email=payload.email,
            password=payload.password,
            source_context=_source_context(request),
        )
    except (
        AuthInputError,
        AuthServiceUnavailableError,
        EmailDeliveryUnavailableError,
        LifecycleRateLimitedError,
        PasswordCompromisedError,
    ) as exc:
        raise _translate_auth_error(exc) from exc
    return _signup_created_response(created)


@router.post(
    "/signup/verify",
    operation_id="auth_verify_signup",
    response_model=SignupVerificationResponse,
    responses=_PROBLEM_RESPONSES,
)
async def verify_signup(
    payload: SignupVerificationRequest,
    response: Response,
    service: AuthLifecycleServiceDependency,
) -> SignupVerificationResponse:
    """Consume one mailbox OTP and establish a new Account or safe existing-account outcome."""
    try:
        result = await service.verify_signup(
            signup_ref=payload.signup_ref,
            code=payload.code,
        )
    except (
        AuthServiceUnavailableError,
        VerificationAttemptsExhaustedError,
        VerificationInvalidOrExpiredError,
    ) as exc:
        raise _translate_auth_error(exc) from exc

    if isinstance(result, ExistingAccountSignupResult):
        return ExistingAccountSignupResponse()

    _set_session_cookie(
        response,
        result.session_secret.get_secret_value(),
        max_age_seconds=service.session_cookie_max_age_seconds,
    )
    return _signup_authenticated_response(result)


@router.post(
    "/signup/resend",
    operation_id="auth_resend_signup_verification",
    response_model=SignupCreatedResponse,
    responses=_PROBLEM_RESPONSES,
)
async def resend_signup_verification(
    payload: SignupResendRequest,
    request: Request,
    service: AuthLifecycleServiceDependency,
) -> SignupCreatedResponse:
    """Rotate the OTP for one pending signup reference without clobbering sibling challenges."""
    try:
        created = await service.resend_signup_verification(
            signup_ref=payload.signup_ref,
            source_context=_source_context(request),
        )
    except (
        AuthServiceUnavailableError,
        EmailDeliveryUnavailableError,
        LifecycleRateLimitedError,
        SignupResendCooldownError,
        VerificationInvalidOrExpiredError,
    ) as exc:
        raise _translate_auth_error(exc) from exc
    return _signup_created_response(created)


@router.post(
    "/recovery",
    operation_id="auth_request_password_recovery",
    status_code=202,
    response_model=RecoveryAcceptedResponse,
    responses=_PROBLEM_RESPONSES,
)
async def request_password_recovery(
    payload: PasswordRecoveryRequest,
    request: Request,
    service: AuthLifecycleServiceDependency,
) -> RecoveryAcceptedResponse:
    """Return neutral accepted semantics for both eligible and ineligible email state."""
    try:
        await service.request_password_recovery(
            email=payload.email,
            source_context=_source_context(request),
        )
    except (
        AuthInputError,
        AuthServiceUnavailableError,
        EmailDeliveryUnavailableError,
        LifecycleRateLimitedError,
    ) as exc:
        raise _translate_auth_error(exc) from exc
    return RecoveryAcceptedResponse()


@router.post(
    "/recovery/validate",
    operation_id="auth_validate_password_recovery",
    response_model=RecoveryValidationResponse,
    responses=_PROBLEM_RESPONSES,
)
async def validate_password_recovery(
    payload: PasswordRecoveryValidationRequest,
    service: AuthLifecycleServiceDependency,
) -> RecoveryValidationResponse:
    """Validate a recovery proof without consuming it or mutating Account state."""
    try:
        validation = await service.validate_password_recovery(
            password_recovery_ref=payload.password_recovery_ref,
            secret=payload.secret,
        )
    except AuthServiceUnavailableError as exc:
        raise _translate_auth_error(exc) from exc
    return RecoveryValidationResponse(valid=validation.valid)


@router.post(
    "/reset-password",
    operation_id="auth_reset_password",
    status_code=204,
    response_model=None,
    responses=_PROBLEM_RESPONSES,
)
async def reset_password(
    payload: PasswordResetRequest,
    response: Response,
    service: AuthLifecycleServiceDependency,
) -> None:
    """Consume recovery proof, replace PasswordCredential and revoke every AuthSession."""
    try:
        await service.reset_password(
            password_recovery_ref=payload.password_recovery_ref,
            secret=payload.secret,
            new_password=payload.new_password,
        )
    except (
        AuthInputError,
        AuthServiceUnavailableError,
        PasswordCompromisedError,
        RecoveryInvalidOrExpiredError,
    ) as exc:
        raise _translate_auth_error(exc) from exc
    _clear_session_cookie(response)


@router.post(
    "/reauthenticate",
    operation_id="auth_reauthenticate",
    response_model=AuthenticatedSessionResponse,
    responses=_PROBLEM_RESPONSES,
)
async def reauthenticate(
    payload: ReauthenticateRequest,
    request: Request,
    response: Response,
    auth_service: AuthServiceDependency,
    lifecycle_service: AuthLifecycleServiceDependency,
) -> AuthenticatedSessionResponse:
    """Refresh recent authentication on the same AuthSession and rotate its bearer secret."""
    try:
        cookie_value = _session_cookie(request)
    except AmbiguousSessionCookieError as exc:
        raise _csrf_failed() from exc

    try:
        admitted = await auth_service.admit_session(cookie_value)
    except AuthServiceUnavailableError as exc:
        raise _translate_auth_error(exc) from exc
    if admitted is None or cookie_value is None:
        _clear_session_cookie(response)
        raise _authentication_required()

    if not csrf_token_matches(
        admitted.csrf_token,
        single_header_value(request.scope, CSRF_HEADER_NAME),
    ):
        raise _csrf_failed()

    raw_secret = decode_session_secret(cookie_value)
    if raw_secret is None:
        _clear_session_cookie(response)
        raise _authentication_required()
    presented_verifier = session_secret_verifier_from_raw(raw_secret)

    try:
        issued = await lifecycle_service.reauthenticate(
            admitted=admitted,
            presented_session_verifier=presented_verifier,
            password=payload.password,
            source_context=_source_context(request),
            request_id=str(request.state.request_id),
        )
    except (
        AccountUnavailableError,
        AuthInputError,
        AuthServiceUnavailableError,
        InvalidCredentialsError,
        LifecycleRateLimitedError,
        PasswordCompromisedError,
    ) as exc:
        raise _translate_auth_error(exc) from exc

    _set_session_cookie(
        response,
        issued.session_secret.get_secret_value(),
        max_age_seconds=lifecycle_service.session_cookie_max_age_seconds,
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
        raise _csrf_failed() from exc

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
        raise _csrf_failed()

    try:
        await service.log_out(admitted.principal.auth_session_ref)
    except AuthServiceUnavailableError as exc:
        raise _translate_auth_error(exc) from exc

    _clear_session_cookie(response)
