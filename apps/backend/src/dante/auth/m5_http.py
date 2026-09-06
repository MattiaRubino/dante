"""Shared HTTP boundary primitives for public M5 Access/Auth routes."""

from __future__ import annotations

import math
from datetime import UTC, datetime
from typing import Any

from fastapi import Request, Response

from dante.auth.api import AuthenticatedSessionResponse
from dante.auth.contracts import (
    AccountUnavailableError,
    AdmittedSession,
    AuthenticatorRemovalBlockedError,
    AuthInputError,
    AuthServiceUnavailableError,
    AuthStateChangedError,
    EmailDeliveryUnavailableError,
    IssuedSession,
    LifecycleRateLimitedError,
    PasskeyAlreadyRegisteredError,
    PasskeyChallengeInvalidOrExpiredError,
    PasskeyNotFoundError,
    PasskeyVerificationFailedError,
    PasswordAlreadyEstablishedError,
    PasswordCompromisedError,
    ProviderEnrollmentAttemptsExhaustedError,
    ProviderEnrollmentInvalidOrExpiredError,
    ProviderEnrollmentVerificationInvalidOrExpiredError,
    ProviderIdentityConflictError,
    ProviderLinkAccountMismatchError,
    ProviderLinkInvalidOrExpiredError,
    ProviderProofInvalidError,
    ProviderReconciliationPendingError,
    ProviderTransactionInvalidOrExpiredError,
    ProviderUnavailableError,
    ReauthenticationRequiredError,
    SignupResendCooldownError,
)
from dante.auth.dependencies import single_header_value
from dante.auth.service import AuthService
from dante.auth.sessions import (
    CSRF_HEADER_NAME,
    SESSION_COOKIE_NAME,
    AmbiguousSessionCookieError,
    csrf_token_matches,
    session_cookie_value,
)
from dante.platform.http.problem import ProblemDetails, ProblemError, ProblemFieldError

PROVIDER_LINK_COOKIE_NAME = "__Host-dante-provider-link"
PROVIDER_ENROLLMENT_COOKIE_NAME = "__Host-dante-provider-enrollment"

COMMON_M5_PROBLEM_RESPONSES: dict[int | str, dict[str, Any]] = {
    400: {"model": ProblemDetails},
    401: {"model": ProblemDetails},
    403: {"model": ProblemDetails},
    404: {"model": ProblemDetails},
    409: {"model": ProblemDetails},
    422: {"model": ProblemDetails},
    429: {"model": ProblemDetails},
    500: {"model": ProblemDetails},
    503: {"model": ProblemDetails},
}


class AmbiguousFlowCookieError(ValueError):
    """More than one value was supplied for one security flow cookie."""


def set_session_cookie(
    response: Response,
    secret: str,
    *,
    max_age_seconds: int,
) -> None:
    """Set the canonical opaque host-only AuthSession bearer cookie."""
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=secret,
        max_age=max_age_seconds,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
    )


def clear_session_cookie(response: Response) -> None:
    """Clear the canonical AuthSession bearer cookie without widening attributes."""
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
    )


def set_flow_cookie(
    response: Response,
    *,
    name: str,
    continuation_secret: str,
    expires_at: datetime,
) -> None:
    """Set one raw continuation capability with lifetime bounded by backing state."""
    remaining = math.ceil((expires_at - datetime.now(UTC)).total_seconds())
    if remaining <= 0:
        clear_flow_cookie(response, name=name)
        return
    response.set_cookie(
        key=name,
        value=continuation_secret,
        max_age=remaining,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
    )


def clear_flow_cookie(response: Response, *, name: str) -> None:
    """Clear one exact M5 continuation cookie."""
    response.delete_cookie(
        key=name,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
    )


def flow_cookie_value(request: Request, *, name: str) -> str | None:
    """Return exactly one flow-cookie value and fail closed on duplicate names."""
    values: list[str] = []
    for raw_name, raw_value in request.scope.get("headers", []):
        if raw_name.lower() != b"cookie":
            continue
        cookie_header = raw_value.decode("latin-1")
        for raw_pair in cookie_header.split(";"):
            candidate_name, separator, value = raw_pair.strip().partition("=")
            if separator and candidate_name == name:
                values.append(value)
    if len(values) > 1:
        raise AmbiguousFlowCookieError("duplicate flow cookie")
    return values[0] if values else None


def source_context(request: Request) -> str:
    """Return bounded abuse-control context; this is never identity authority."""
    client = request.client
    return client.host if client is not None and client.host else "unknown"


def authentication_required() -> ProblemError:
    return ProblemError(
        status=401,
        code="auth.authentication_required",
        category="authentication",
        title="Authentication required",
        detail="A valid authenticated session is required.",
    )


def csrf_failed() -> ProblemError:
    return ProblemError(
        status=403,
        code="security.csrf_failed",
        category="security",
        title="Request rejected",
        detail="The request could not satisfy the browser security policy.",
    )


def translate_m5_auth_error(exc: Exception) -> ProblemError:
    """Translate accepted M5 application failures to stable RFC 9457 semantics."""
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
    if isinstance(exc, ProviderTransactionInvalidOrExpiredError):
        return ProblemError(
            status=401,
            code="auth.provider_transaction_invalid_or_expired",
            category="authentication",
            title="Provider transaction rejected",
            detail="The provider authentication transaction is invalid or expired.",
        )
    if isinstance(exc, ProviderProofInvalidError):
        return ProblemError(
            status=401,
            code="auth.provider_proof_invalid",
            category="authentication",
            title="Provider proof rejected",
            detail="The provider authentication proof could not be accepted.",
        )
    if isinstance(exc, ProviderLinkInvalidOrExpiredError):
        return ProblemError(
            status=401,
            code="auth.provider_link_invalid_or_expired",
            category="authentication",
            title="Provider link expired",
            detail="The provider-link continuation is invalid or expired.",
        )
    if isinstance(exc, ProviderLinkAccountMismatchError):
        return ProblemError(
            status=409,
            code="auth.provider_link_account_mismatch",
            category="conflict",
            title="Provider link target changed",
            detail="The provider-link continuation does not target this authenticated account.",
        )
    if isinstance(exc, ProviderIdentityConflictError):
        return ProblemError(
            status=409,
            code="auth.provider_identity_conflict",
            category="conflict",
            title="Provider identity conflict",
            detail="The provider identity cannot be attached to this account.",
        )
    if isinstance(exc, ProviderReconciliationPendingError):
        return ProblemError(
            status=503,
            code="auth.provider_reconciliation_pending",
            category="dependency",
            title="Provider reconciliation pending",
            detail="The provider operation could not be concluded safely yet.",
            retryable=False,
        )
    if isinstance(exc, ProviderEnrollmentInvalidOrExpiredError):
        return ProblemError(
            status=401,
            code="auth.provider_enrollment_invalid_or_expired",
            category="authentication",
            title="Provider enrollment expired",
            detail="The provider-enrollment continuation is invalid or expired.",
        )
    if isinstance(
        exc,
        (
            ProviderEnrollmentVerificationInvalidOrExpiredError,
            ProviderEnrollmentAttemptsExhaustedError,
        ),
    ):
        return ProblemError(
            status=401,
            code="auth.provider_enrollment_verification_invalid_or_expired",
            category="authentication",
            title="Provider enrollment verification rejected",
            detail="The provider-enrollment verification proof is invalid or expired.",
        )
    if isinstance(exc, PasskeyChallengeInvalidOrExpiredError):
        return ProblemError(
            status=401,
            code="auth.passkey_challenge_invalid_or_expired",
            category="authentication",
            title="Passkey challenge rejected",
            detail="The passkey ceremony challenge is invalid or expired.",
        )
    if isinstance(exc, PasskeyVerificationFailedError):
        return ProblemError(
            status=401,
            code="auth.passkey_verification_failed",
            category="authentication",
            title="Passkey verification failed",
            detail="The passkey response could not be verified.",
        )
    if isinstance(exc, PasskeyAlreadyRegisteredError):
        return ProblemError(
            status=409,
            code="auth.passkey_already_registered",
            category="conflict",
            title="Passkey already registered",
            detail="This passkey is already lifetime-bound in DANTE.",
        )
    if isinstance(exc, PasskeyNotFoundError):
        return ProblemError(
            status=404,
            code="auth.passkey_not_found",
            category="authentication",
            title="Passkey not found",
            detail="The requested active passkey is not available for this account.",
        )
    if isinstance(exc, ProviderUnavailableError):
        return ProblemError(
            status=503,
            code="dependency.provider_unavailable",
            category="dependency",
            title="Provider unavailable",
            detail="The requested authentication provider is unavailable.",
            retryable=exc.retryable,
        )
    if isinstance(exc, LifecycleRateLimitedError):
        return ProblemError(
            status=429,
            code=exc.code,
            category="rate_limit",
            title="Too many attempts",
            detail="Too many authentication requests were received.",
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
    raise TypeError("unexpected M5 Auth error translation")


async def required_session(
    *,
    request: Request,
    response: Response,
    auth_service: AuthService,
    require_csrf: bool,
) -> tuple[AdmittedSession, str]:
    """Admit canonical session authority and optionally require session-bound CSRF."""
    try:
        cookie_value = session_cookie_value(list(request.scope.get("headers", [])))
    except AmbiguousSessionCookieError as exc:
        if require_csrf:
            raise csrf_failed() from exc
        clear_session_cookie(response)
        raise authentication_required() from exc

    try:
        admitted = await auth_service.admit_session(cookie_value)
    except AuthServiceUnavailableError as exc:
        raise translate_m5_auth_error(exc) from exc
    if admitted is None or cookie_value is None:
        clear_session_cookie(response)
        raise authentication_required()

    if require_csrf and not csrf_token_matches(
        admitted.csrf_token,
        single_header_value(request.scope, CSRF_HEADER_NAME),
    ):
        raise csrf_failed()

    return admitted, cookie_value


def authenticated_response(
    session: IssuedSession | AdmittedSession,
) -> AuthenticatedSessionResponse:
    """Project canonical session state without exposing the bearer secret."""
    return AuthenticatedSessionResponse(
        account_ref=session.principal.account_ref,
        auth_session_ref=session.principal.auth_session_ref,
        recent_auth_at=session.principal.recent_auth_at,
        expires_at=session.expires_at,
        csrf_token=session.csrf_token.get_secret_value(),
    )
