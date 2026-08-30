"""Focused M5-B provider runtime/configuration proof."""

from base64 import urlsafe_b64encode

import pytest
from pydantic import SecretStr, ValidationError

from dante.auth.proofs import FlowProofPurpose, issue_flow_proof, flow_proof_matches
from dante.platform.config.auth_provider import AuthProviderSettings, AppleProviderSettings


def _secret(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def test_provider_defaults_are_disabled_and_canonical() -> None:
    settings = AuthProviderSettings()
    assert settings.google.enabled is False
    assert settings.apple.enabled is False
    assert settings.webauthn.enabled is False
    assert settings.google.issuer == "https://accounts.google.com"
    assert settings.apple.issuer == "https://appleid.apple.com"


def test_apple_grant_key_must_be_exactly_256_bits() -> None:
    with pytest.raises(ValidationError):
        AppleProviderSettings(
            grant_encryption_current_key_id="v1",
            grant_encryption_keys={"v1": SecretStr(_secret(b"short"))},
        )


def test_flow_proofs_are_purpose_separated() -> None:
    proof = issue_flow_proof(FlowProofPurpose.PROVIDER_STATE)
    raw = proof.secret.get_secret_value()
    assert flow_proof_matches(
        purpose=FlowProofPurpose.PROVIDER_STATE,
        encoded_secret=raw,
        expected_verifier=proof.verifier,
    )
    assert not flow_proof_matches(
        purpose=FlowProofPurpose.PROVIDER_LINK,
        encoded_secret=raw,
        expected_verifier=proof.verifier,
    )
