"""Focused M5-B WebAuthn RP/origin policy tests."""

from fido2.webauthn import (
    AttestationConveyancePreference,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)

from dante.auth.webauthn import WebAuthnPolicy
from dante.platform.config.auth_provider import WebAuthnSettings


def test_webauthn_policy_is_exact_and_phishing_resistant() -> None:
    policy = WebAuthnPolicy.from_settings(
        WebAuthnSettings(
            enabled=True,
            rp_id="dante.test",
            rp_name="DANTE",
            expected_origins=("https://dante.test",),
        )
    )
    assert policy.rp_id == "dante.test"
    assert policy.origin_allowed("https://dante.test")
    assert not policy.origin_allowed("https://evil.dante.test")
    assert policy.resident_key is ResidentKeyRequirement.REQUIRED
    assert policy.user_verification is UserVerificationRequirement.REQUIRED
    assert policy.attestation is AttestationConveyancePreference.NONE
