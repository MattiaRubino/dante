"""Typed application contracts for DANTE Access/Auth."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any
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
    """A bounded Auth lifecycle ingress guard refused more work."""

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


class ProviderTransactionInvalidOrExpiredError(AuthError):
    """Provider transaction capability is invalid, expired, claimed or mismatched."""


class ProviderProofInvalidError(AuthError):
    """External provider evidence did not satisfy DANTE's trust contract."""


class ProviderIdentityConflictError(AuthError):
    """A provider identity is durably bound to a different DANTE Account."""


class ProviderReconciliationPendingError(AuthError):
    """A provider single-use/mutation operation has an intentionally unretried ambiguous result."""


class ProviderEnrollmentInvalidOrExpiredError(AuthError):
    """Provider enrollment continuation state is unavailable or expired."""


class ProviderEnrollmentVerificationInvalidOrExpiredError(AuthError):
    """Provider enrollment mailbox proof is invalid or expired."""


class ProviderEnrollmentAttemptsExhaustedError(AuthError):
    """Provider enrollment mailbox proof exhausted its online guess budget."""


class ProviderLinkInvalidOrExpiredError(AuthError):
    """Provider-first link continuation state is unavailable, expired or consumed."""


class ProviderLinkAccountMismatchError(AuthError):
    """Provider-first link state targets a different authenticated Account."""


class PasswordAlreadyEstablishedError(AuthError):
    """The Account already has a current PasswordCredential."""


class AuthenticatorRemovalBlockedError(AuthError):
    """Removing an authenticator would violate the Account anti-lockout invariant."""


class AuthStateChangedError(AuthError):
    """Security state changed after the caller formed its intended mutation."""


class PasskeyChallengeInvalidOrExpiredError(AuthError):
    """WebAuthn ceremony state is invalid, expired, claimed or mismatched."""


class PasskeyVerificationFailedError(AuthError):
    """WebAuthn registration/assertion evidence failed the frozen verification policy."""


class PasskeyAlreadyRegisteredError(AuthError):
    """A WebAuthn credential id is already lifetime-bound in DANTE."""


class PasskeyNotFoundError(AuthError):
    """The requested current passkey is absent from the authenticated Account."""


class ProviderUnavailableError(AuthError):
    """External provider trust material/service is temporarily unavailable."""

    def __init__(self, *, retryable: bool) -> None:
        super().__init__("provider unavailable")
        self.retryable = retryable


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


class ProviderPurpose(StrEnum):
    """Security intent bound into one provider transaction."""

    SIGN_IN = "sign_in"
    LINK = "link"
    REAUTHENTICATE = "reauthenticate"


class ProviderReturnTarget(StrEnum):
    """Bounded post-provider application destination."""

    ACCESS = "access"
    SECURITY = "security"


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


@dataclass(frozen=True, slots=True)
class ProviderAuthenticationBegun:
    """Transient capabilities for one server-authoritative provider transaction."""

    external_auth_transaction_ref: UUID
    state: SecretStr
    nonce: SecretStr
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class ProviderAuthenticated:
    """Provider proof converged on a committed canonical DANTE AuthSession."""

    session: IssuedSession


@dataclass(frozen=True, slots=True)
class ProviderLinkRequired:
    """Verified provider evidence collided with an existing DANTE Account."""

    external_link_challenge_ref: UUID
    continuation_secret: SecretStr
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class ProviderEnrollmentRequired:
    """Provider evidence requires DANTE mailbox proof before Account creation."""

    external_signup_ref: UUID
    continuation_secret: SecretStr
    expires_at: datetime
    email_address: str | None
    verification_expires_at: datetime | None


@dataclass(frozen=True, slots=True)
class ProviderLinkState:
    """Safe provider-first link metadata after continuation-capability validation."""

    external_link_challenge_ref: UUID
    provider_code: str
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class AuthenticationProviderMethod:
    """One active provider authenticator exposed without provider subject/security secrets."""

    external_identity_ref: UUID
    provider_code: str
    provider_email_address: str | None
    provider_email_private: bool | None


@dataclass(frozen=True, slots=True)
class AuthenticationMethods:
    """Current Account-wide authenticator inventory for security/settings surfaces."""

    password_established: bool
    providers: tuple[AuthenticationProviderMethod, ...]
    active_passkey_count: int
    recovery_eligible_email_count: int


@dataclass(frozen=True, slots=True)
class PasskeyMethod:
    """Safe active-passkey projection for Security/settings management surfaces."""

    passkey_credential_ref: UUID
    label: str
    transports: tuple[str, ...]
    backup_eligible: bool
    backup_state: bool
    created_at: datetime
    last_used_at: datetime | None


@dataclass(frozen=True, slots=True)
class PasskeyCeremonyBegun:
    """Public WebAuthn options plus one non-secret durable ceremony reference."""

    webauthn_challenge_ref: UUID
    options: dict[str, Any]
    expires_at: datetime


type ProviderAuthenticationResult = (
    ProviderAuthenticated | ProviderLinkRequired | ProviderEnrollmentRequired
)

type ProviderEnrollmentResult = ProviderAuthenticated | ProviderLinkRequired
