"""Process-scoped M4 Auth lifecycle runtime built on the accepted M3 security resources."""

from __future__ import annotations

from dataclasses import dataclass

from dante.auth.email_delivery import SmtpEmailDispatcher
from dante.auth.lifecycle import AuthLifecycleService, KeyedRateLimiter, LifecycleLimiters
from dante.auth.passwords import HibpPasswordChecker
from dante.auth.proofs import SignupOtpCodec
from dante.auth.service import AuthRuntime
from dante.platform.config.auth import AuthSettings
from dante.platform.database.runtime import DatabaseRuntime


@dataclass(slots=True)
class AuthLifecycleRuntime:
    """M4 lifecycle service plus the process-owned email dispatcher it exclusively owns."""

    service: AuthLifecycleService
    email_dispatcher: SmtpEmailDispatcher

    async def aclose(self) -> None:
        """Drain admitted email work before shared M3 Auth resources are disposed."""
        await self.email_dispatcher.aclose()


async def create_auth_lifecycle_runtime(
    *,
    settings: AuthSettings,
    database_runtime: DatabaseRuntime,
    auth_runtime: AuthRuntime,
) -> AuthLifecycleRuntime:
    """Construct M4 lifecycle capabilities while reusing M3 KDF/HIBP transport resources."""
    email_dispatcher = SmtpEmailDispatcher(settings=settings)
    await email_dispatcher.start()
    try:
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
        service = AuthLifecycleService(
            session_factory=database_runtime.session_factory,
            settings=settings,
            password_kdf=auth_runtime.password_kdf,
            breach_checker=breach_checker,
            otp_codec=otp_codec,
            email_delivery=email_dispatcher,
            limiters=limiters,
        )
        return AuthLifecycleRuntime(
            service=service,
            email_dispatcher=email_dispatcher,
        )
    except BaseException:
        await email_dispatcher.aclose()
        raise
