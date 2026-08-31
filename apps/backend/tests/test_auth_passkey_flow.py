"""Focused pure/application proof for M5-F passkey lifecycle rules."""

from datetime import UTC, datetime
from uuid import uuid7

import pytest
from pydantic import ValidationError

from dante.auth.contracts import AuthInputError, PasskeyVerificationFailedError
from dante.auth.passkey_flow import PasskeyFlowService
from dante.auth.proofs import FlowProofPurpose, flow_proof_verifier_from_raw
from dante.auth.webauthn import WebAuthnAssertionEvidence
from dante.platform.config.auth_provider import WebAuthnSettings
from dante.platform.database.mappings.auth import PasskeyCredentialRow


def _credential(*, sign_count: int = 8, backup_eligible: bool = True) -> PasskeyCredentialRow:
    now = datetime.now(UTC)
    return PasskeyCredentialRow(
        passkey_credential_ref=uuid7(),
        account_ref=uuid7(),
        credential_id=b"credential-id",
        credential_public_key=b"cose-key",
        cose_algorithm=-7,
        sign_count=sign_count,
        backup_eligible=backup_eligible,
        backup_state=False,
        transports=[],
        label="Laptop",
        status_code="active",
        created_at=now,
        updated_at=now,
        last_used_at=None,
        revoked_at=None,
        revocation_reason_code=None,
    )


def _assertion(*, sign_count: int, backup_eligible: bool = True) -> WebAuthnAssertionEvidence:
    return WebAuthnAssertionEvidence(
        credential_id=b"credential-id",
        user_handle=b"u" * 32,
        sign_count=sign_count,
        backup_eligible=backup_eligible,
        backup_state=True,
        challenge=b"a" * 32,
        origin="https://dante.test",
    )


def test_webauthn_challenge_lifetime_is_capped_at_five_minutes() -> None:
    with pytest.raises(ValidationError, match="five minutes"):
        WebAuthnSettings(challenge_lifetime_seconds=301)


def test_passkey_label_and_transport_hints_are_bounded_without_freezing_vocabulary() -> None:
    assert PasskeyFlowService._normalize_label("My security key") == "My security key"
    assert PasskeyFlowService._normalize_transports(("usb", "hybrid", "future-transport")) == (
        "usb",
        "hybrid",
        "future-transport",
    )
    assert PasskeyFlowService._normalize_transports(("usb", "usb")) == ("usb",)

    with pytest.raises(AuthInputError):
        PasskeyFlowService._normalize_label(" passkey ")
    with pytest.raises(AuthInputError):
        PasskeyFlowService._normalize_transports(tuple(str(index) for index in range(9)))


def test_raw_webauthn_challenge_verifier_is_exact_width_and_purpose_separated() -> None:
    challenge = b"x" * 32
    webauthn = flow_proof_verifier_from_raw(
        purpose=FlowProofPurpose.WEBAUTHN_CHALLENGE,
        raw_secret=challenge,
    )
    provider = flow_proof_verifier_from_raw(
        purpose=FlowProofPurpose.PROVIDER_STATE,
        raw_secret=challenge,
    )

    assert webauthn is not None
    assert provider is not None
    assert webauthn != provider
    assert flow_proof_verifier_from_raw(
        purpose=FlowProofPurpose.WEBAUTHN_CHALLENGE,
        raw_secret=b"x" * 31,
    ) is None


def test_verified_assertion_never_decreases_counter_and_updates_current_backup_state() -> None:
    credential = _credential(sign_count=8)
    mutation_at = datetime.now(UTC)

    PasskeyFlowService._apply_assertion_state(
        credential,
        evidence=_assertion(sign_count=3),
        mutation_at=mutation_at,
    )

    assert credential.sign_count == 8
    assert credential.backup_state is True
    assert credential.last_used_at == mutation_at
    assert credential.updated_at == mutation_at


def test_assertion_cannot_change_immutable_backup_eligibility() -> None:
    credential = _credential(backup_eligible=False)

    with pytest.raises(PasskeyVerificationFailedError):
        PasskeyFlowService._apply_assertion_state(
            credential,
            evidence=_assertion(sign_count=9, backup_eligible=True),
            mutation_at=datetime.now(UTC),
        )
