"""Real PostgreSQL proof for opaque M5 provider continuation capability resolution."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid7

import pytest

from dante.auth.contracts import (
    ProviderEnrollmentInvalidOrExpiredError,
    ProviderLinkInvalidOrExpiredError,
)
from dante.auth.proofs import FlowProofPurpose, issue_flow_proof
from dante.auth.provider_continuation import ProviderContinuationService
from dante.platform.config.auth_provider import GOOGLE_ISSUER
from dante.platform.database.mappings.auth import (
    AccountRow,
    EmailIdentityRow,
    ExternalLinkChallengeRow,
    ExternalSignupChallengeRow,
)
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_opaque_provider_continuations_resolve_server_side_by_purpose(
    migrated_database: object,
) -> None:
    runtime = create_database_runtime(migrated_database.runtime_settings())  # type: ignore[attr-defined]
    service = ProviderContinuationService(session_factory=runtime.session_factory)
    now = datetime.now(UTC)
    account_ref = uuid7()
    email_ref = uuid7()
    signup_ref = uuid7()
    link_ref = uuid7()
    enrollment = issue_flow_proof(FlowProofPurpose.PROVIDER_ENROLLMENT)
    link = issue_flow_proof(FlowProofPurpose.PROVIDER_LINK)

    try:
        async with runtime.session_factory() as session, session.begin():
            session.add_all(
                [
                    AccountRow(
                        account_ref=account_ref,
                        status_code="active",
                        created_at=now,
                        disabled_at=None,
                    ),
                    EmailIdentityRow(
                        email_identity_ref=email_ref,
                        account_ref=account_ref,
                        address="continuation@example.com",
                        comparison_key="continuation@example.com",
                        created_at=now,
                        verified_at=now,
                        recovery_restriction_code=None,
                        recovery_restriction_observed_at=None,
                    ),
                    ExternalSignupChallengeRow(
                        external_signup_ref=signup_ref,
                        provider_code="google",
                        issuer=GOOGLE_ISSUER,
                        subject="continuation-enrollment",
                        provider_email_address=None,
                        provider_email_private=None,
                        apple_auth_grant_ref=None,
                        continuation_verifier=enrollment.verifier,
                        email_address=None,
                        email_comparison_key=None,
                        otp_verifier=None,
                        otp_key_id=None,
                        verification_issued_at=None,
                        verification_expires_at=None,
                        failed_verification_attempts=0,
                        bootstrap_display_name=None,
                        bootstrap_given_name=None,
                        bootstrap_family_name=None,
                        bootstrap_picture_url=None,
                        bootstrap_locale=None,
                        created_at=now,
                        updated_at=now,
                        expires_at=now + timedelta(minutes=10),
                    ),
                    ExternalLinkChallengeRow(
                        external_link_challenge_ref=link_ref,
                        target_account_ref=account_ref,
                        target_email_identity_ref=email_ref,
                        provider_code="google",
                        issuer=GOOGLE_ISSUER,
                        subject="continuation-link",
                        provider_email_address=None,
                        provider_email_private=None,
                        apple_auth_grant_ref=None,
                        continuation_verifier=link.verifier,
                        created_at=now,
                        expires_at=now + timedelta(minutes=10),
                    ),
                ]
            )

        enrollment_state = await service.resolve_enrollment(enrollment.secret.get_secret_value())
        assert enrollment_state.external_signup_ref == signup_ref
        assert enrollment_state.provider_code == "google"

        link_state = await service.resolve_link(link.secret.get_secret_value())
        assert link_state.external_link_challenge_ref == link_ref
        assert link_state.provider_code == "google"

        with pytest.raises(ProviderEnrollmentInvalidOrExpiredError):
            await service.resolve_enrollment(link.secret.get_secret_value())
        with pytest.raises(ProviderLinkInvalidOrExpiredError):
            await service.resolve_link(enrollment.secret.get_secret_value())
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_expired_continuation_is_not_resolved(
    migrated_database: object,
) -> None:
    runtime = create_database_runtime(migrated_database.runtime_settings())  # type: ignore[attr-defined]
    service = ProviderContinuationService(session_factory=runtime.session_factory)
    now = datetime.now(UTC)
    proof = issue_flow_proof(FlowProofPurpose.PROVIDER_ENROLLMENT)

    try:
        async with runtime.session_factory() as session, session.begin():
            session.add(
                ExternalSignupChallengeRow(
                    external_signup_ref=uuid7(),
                    provider_code="google",
                    issuer=GOOGLE_ISSUER,
                    subject="expired-continuation",
                    provider_email_address=None,
                    provider_email_private=None,
                    apple_auth_grant_ref=None,
                    continuation_verifier=proof.verifier,
                    email_address=None,
                    email_comparison_key=None,
                    otp_verifier=None,
                    otp_key_id=None,
                    verification_issued_at=None,
                    verification_expires_at=None,
                    failed_verification_attempts=0,
                    bootstrap_display_name=None,
                    bootstrap_given_name=None,
                    bootstrap_family_name=None,
                    bootstrap_picture_url=None,
                    bootstrap_locale=None,
                    created_at=now - timedelta(minutes=20),
                    updated_at=now - timedelta(minutes=20),
                    expires_at=now - timedelta(minutes=10),
                )
            )

        with pytest.raises(ProviderEnrollmentInvalidOrExpiredError):
            await service.resolve_enrollment(proof.secret.get_secret_value())
    finally:
        await runtime.dispose()
