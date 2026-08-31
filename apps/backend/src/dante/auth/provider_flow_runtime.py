"""Process-scoped M5 provider-flow runtime reusing accepted Auth resources."""

from dataclasses import dataclass

from dante.auth.apple import (
    AppleClientSecretSigner,
    AppleNotificationVerifier,
    AppleProtocolClient,
    AppleTokenVerifier,
)
from dante.auth.apple_flow import AppleFlowService
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
    """M5 provider application services; parent runtimes own shared resources."""

    service: ProviderFlowService | None
    apple_service: AppleFlowService | None


def create_provider_flow_runtime(
    *,
    settings: AuthSettings,
    database_runtime: DatabaseRuntime,
    auth_runtime: AuthRuntime,
    lifecycle_runtime: AuthLifecycleRuntime,
) -> ProviderFlowRuntime:
    """Build enabled provider flows without duplicate network/crypto/email ownership."""
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
    otp_codec = ProviderEnrollmentOtpCodec(
        key_ring=settings.signup_otp_key_bytes,
        current_key_id=settings.signup_otp_current_key_id,
    )

    google_service = (
        ProviderFlowService(
            session_factory=database_runtime.session_factory,
            settings=settings,
            google_verifier=GoogleTokenVerifier(
                settings=settings.provider,
                provider_runtime=auth_runtime.provider_runtime,
            ),
            otp_codec=otp_codec,
            email_delivery=lifecycle_runtime.email_dispatcher,
            limiters=limiters,
        )
        if settings.provider.google.enabled
        else None
    )

    apple_service: AppleFlowService | None = None
    apple = settings.provider.apple
    if apple.enabled:
        if (
            apple.client_id is None
            or apple.team_id is None
            or apple.key_id is None
            or apple.client_private_key_pem is None
            or auth_runtime.apple_grant_cipher is None
        ):
            raise RuntimeError("enabled Apple authentication lost validated runtime configuration")
        signer = AppleClientSecretSigner(
            team_id=apple.team_id,
            key_id=apple.key_id,
            client_id=apple.client_id,
            private_key_pem=apple.client_private_key_pem,
        )
        protocol_client = AppleProtocolClient(
            settings=settings.provider,
            provider_runtime=auth_runtime.provider_runtime,
            signer=signer,
        )
        token_verifier = AppleTokenVerifier(
            settings=settings.provider,
            provider_runtime=auth_runtime.provider_runtime,
        )
        apple_service = AppleFlowService(
            session_factory=database_runtime.session_factory,
            settings=settings,
            token_verifier=token_verifier,
            notification_verifier=AppleNotificationVerifier(
                settings=settings.provider,
                provider_runtime=auth_runtime.provider_runtime,
            ),
            protocol_client=protocol_client,
            grant_cipher=auth_runtime.apple_grant_cipher,
            otp_codec=otp_codec,
            email_delivery=lifecycle_runtime.email_dispatcher,
            limiters=limiters,
        )

    return ProviderFlowRuntime(service=google_service, apple_service=apple_service)