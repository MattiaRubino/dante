"""Process-scoped M5 provider-flow runtime reusing accepted Auth resources."""

from dataclasses import dataclass

from dante.auth.google import GoogleTokenVerifier
from dante.auth.lifecycle import KeyedRateLimiter
from dante.auth.lifecycle_runtime import AuthLifecycleRuntime
from dante.auth.proofs import ProviderEnrollmentOtpCodec
from dante.auth.provider_flow import ProviderFlowLimiters, ProviderFlowService
from dante.auth.service import AuthRuntime
from dante.platform.config.auth import AuthSettings
from dante.platform.database.runtime import DatabaseRuntime


@dataclass(frozen=True, slots=True)
class ProviderFlowRuntime:
    """M5 provider application service; shared resources remain owned by parent runtimes."""

    service: ProviderFlowService


def create_provider_flow_runtime(
    *,
    settings: AuthSettings,
    database_runtime: DatabaseRuntime,
    auth_runtime: AuthRuntime,
    lifecycle_runtime: AuthLifecycleRuntime,
) -> ProviderFlowRuntime:
    """Build provider flow capabilities without creating duplicate network/email resources."""
    max_keys = settings.provider_rate_max_keys
    limiters = ProviderFlowLimiters(
        begin=KeyedRateLimiter(
            capacity=settings.provider_begin_rate_capacity,
            window_seconds=settings.provider_begin_rate_window_seconds,
            max_keys=max_keys,
        ),
        complete=KeyedRateLimiter(
            capacity=settings.provider_complete_rate_capacity,
            window_seconds=settings.provider_complete_rate_window_seconds,
            max_keys=max_keys,
        ),
        enrollment=KeyedRateLimiter(
            capacity=settings.provider_enrollment_rate_capacity,
            window_seconds=settings.provider_enrollment_rate_window_seconds,
            max_keys=max_keys,
        ),
    )
    service = ProviderFlowService(
        session_factory=database_runtime.session_factory,
        settings=settings,
        google_verifier=GoogleTokenVerifier(
            settings=settings.provider,
            provider_runtime=auth_runtime.provider_runtime,
        ),
        otp_codec=ProviderEnrollmentOtpCodec(
            key_ring=settings.signup_otp_key_bytes,
            current_key_id=settings.signup_otp_current_key_id,
        ),
        email_delivery=lifecycle_runtime.email_dispatcher,
        limiters=limiters,
    )
    return ProviderFlowRuntime(service=service)
