"""Typed application contracts for DANTE Access/Auth."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from pydantic import SecretStr


class AuthError(Exception):
    """Base class for expected Access/Auth application failures."""


class InvalidCredentialsError(AuthError):
    """Submitted credentials did not authenticate an Account."""


class AccountUnavailableError(AuthError):
    """A correctly proven Account is not currently available for authentication."""


class PasswordCompromisedError(AuthError):
    """The correctly proven/new password is known compromised and cannot be accepted."""


class AuthInputError(AuthError):
    """One public Auth field violates the bounded request contract."""

    def __init__(
        self,
        *,
        pointer: str,
        code: str,
        detail: str,
        parameters: dict[str, int] | None = None,
    ) -> None:
        super().__init__("invalid authentication input")
        self.pointer = pointer
        self.code = code
        self.detail = detail
        self.parameters = parameters


class SigninRateLimitedError(AuthError):
    """Process-local ingress guard refused another password attempt."""

    def __init__(self, retry_after_seconds: int) -> None:
        super().__init__("signin rate limited")
        self.retry_after_seconds = retry_after_seconds


class LifecycleRateLimitedError(AuthError):
    """A bounded M4 lifecycle ingress guard refused more work."""

    def __init__(self, *, code: str, retry_after_seconds: int) -> None:
        super().__init__("auth lifecycle rate limited")
        self.code = code
        self.retry_after_seconds = retry_after_seconds


class SignupResendCooldownError(AuthError):
    """The same signup challenge requested OTP rotation too quickly."""

    def __init__(self, retry_after_seconds: int) -> None:
        super().__init__("signup resend cooldown active")
        self.retry_after_seconds = retry_after_seconds


class VerificationInvalidOrExpiredError(AuthError):
    """Signup reference/code is invalid, expired or otherwise no longer usable."""


class VerificationAttemptsExhaustedError(AuthError):
    """The current issued six-digit OTP exhausted its online guess budget."""


class RecoveryInvalidOrExpiredError(AuthError):
    """Password recovery proof is invalid, expired, superseded or consumed."""


class ReauthenticationRequiredError(AuthError):
    """Current AuthSession lacks sufficiently recent authentication evidence."""


class EmailDeliveryUnavailableError(AuthError):
    """The bounded email dispatch boundary cannot safely admit another message."""


class AuthServiceUnavailableError(AuthError):
    """A local/dependency boundary cannot safely complete the operation."""

    def __init__(self, *, retryable: bool) -> None:
        super().__init__("authentication service unavailable")
        self.retryable = retryable


class KdfCapacityUnavailableError(AuthServiceUnavailableError):
    """Bounded password worker capacity is saturated."""

    def __init__(self) -> None:
        super().__init__(retryable=True)


class AuthIntegrityError(RuntimeError):
    """Stored/configured security state violates an internal invariant."""


@dataclass(frozen=True, slots=True)
class Principal:
    """Request-scoped security context. This is not a persisted Domain Actor."""

    account_ref: UUID
    auth_session_ref: UUID
    authenticated_at: datetime
    recent_auth_at: datetime


@dataclass(frozen=True, slots=True)
class IssuedSession:
    """Committed/reconciled AuthSession plus transient client-only secrets."""

    principal: Principal
    expires_at: datetime
    session_secret: SecretStr
    csrf_token: SecretStr


@dataclass(frozen=True, slots=True)
class AdmittedSession:
    """Server-authoritative session admission result for one request."""

    principal: Principal
    expires_at: datetime
    csrf_token: SecretStr


@dataclass(frozen=True, slots=True)
class SignupCreated:
    """Public non-secret metadata for one pending password signup."""

    signup_ref: UUID
    signup_expires_at: datetime
    verification_expires_at: datetime


@dataclass(frozen=True, slots=True)
class ExistingAccountSignupResult:
    """Mailbox ownership was proven but a canonical Account already owns the email."""


@dataclass(frozen=True, slots=True)
class RecoveryValidation:
    """Non-consuming public recovery-proof validation result."""

    valid: bool
