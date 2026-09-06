"""Process-scoped Auth lifecycle runtime built on accepted security resources."""

from __future__ import annotations

from dataclasses import dataclass

from dante.auth.authenticator_lifecycle import MultiAuthenticatorLifecycleService
from dante.auth.email_delivery import UnavailableEmailDelivery
from dante.auth.email_runtime import EmailPlatformRuntime
from dante.auth.lifecycle import KeyedRateLimiter, LifecycleLimiters
from dante.auth.passwords import HibpPasswordChecker
from dante.auth.proofs import SignupOtpCodec
from dante.auth.service import AuthRuntime
from dante.platform.config.auth import AuthSettings
from dante.platform.database.runtime import DatabaseRuntime


@dataclass(slots=True)
class AuthLifecycleRuntime:
    """Auth lifecycle service; durable email workers remain owned by bootstrap."""

    service: MultiAuthenticatorLifecycleService
    email_platform: EmailPlatformRuntime | None

    async def aclose(self) -> None:
        """Lifecycle owns no delivery worker resources of its own."""
        return


async def create_auth_lifecycle_runtime(
    *,
    settings: AuthSettings,
    database_runtime: DatabaseRuntime,
    auth_runtime: AuthRuntime,
    email_platform: EmailPlatformRuntime | None = None,
) -> AuthLifecycleRuntime:
    """Construct lifecycle capabilities without creating a second email-delivery path."""
    breach_checker = HibpPasswordChecker(
        client=auth_runtime.http_client,
        max_response_bytes=settings.hibp_max_response_bytes,
    )
    otp_codec = SignupOtpCodec(
        key_ring=settings.signup_otp_key_bytes,
        current_key_id=settings.signup_otp_current_key_id,
    )
    max_keys = settings.lifecycle_rate_max_keys
    limiters = LifecycleLimiters(
        signup_email=KeyedRateLimiter(
            capacity=settings.signup_rate_capacity,
            window_seconds=settings.signup_rate_window_seconds,
            max_keys=max_keys,
        ),
        signup_source=KeyedRateLimiter(
            capacity=settings.signup_source_rate_capacity,
            window_seconds=settings.signup_source_rate_window_seconds,
            max_keys=max_keys,
        ),
        recovery_email=KeyedRateLimiter(
            capacity=settings.recovery_rate_capacity,
            window_seconds=settings.recovery_rate_window_seconds,
            max_keys=max_keys,
        ),
        recovery_source=KeyedRateLimiter(
            capacity=settings.recovery_source_rate_capacity,
            window_seconds=settings.recovery_source_rate_window_seconds,
            max_keys=max_keys,
        ),
        reauth=KeyedRateLimiter(
            capacity=settings.reauth_rate_capacity,
            window_seconds=settings.reauth_rate_window_seconds,
            max_keys=max_keys,
        ),
    )
    service = MultiAuthenticatorLifecycleService(
        session_factory=database_runtime.session_factory,
        settings=settings,
        password_kdf=auth_runtime.password_kdf,
        breach_checker=breach_checker,
        otp_codec=otp_codec,
        email_delivery=UnavailableEmailDelivery(),
        limiters=limiters,
        email_outbox=(email_platform.outbox if email_platform is not None else None),
        email_wake=(email_platform.wake if email_platform is not None else None),
    )
    return AuthLifecycleRuntime(
        service=service,
        email_platform=email_platform,
    )
