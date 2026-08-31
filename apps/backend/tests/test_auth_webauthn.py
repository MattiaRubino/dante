"""Focused M5 WebAuthn RP/origin and real cryptographic verification tests."""

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from fido2.cose import ES256
from fido2.utils import sha256, websafe_encode
from fido2.webauthn import (
    Aaguid,
    AttestationConveyancePreference,
    AttestationObject,
    AttestedCredentialData,
    AuthenticatorData,
    CollectedClientData,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)

from dante.auth.webauthn import WebAuthnPolicy
from dante.platform.config.auth_provider import WebAuthnSettings

_RP_ID = "dante.test"
_ORIGIN = "https://dante.test"


def _policy() -> WebAuthnPolicy:
    return WebAuthnPolicy.from_settings(
        WebAuthnSettings(
            enabled=True,
            rp_id=_RP_ID,
            rp_name="DANTE",
            expected_origins=(_ORIGIN,),
        )
    )


def _registration_response(
    *,
    challenge: bytes,
    credential_id: bytes,
    public_key: ES256,
    backup_eligible: bool = True,
) -> dict[str, object]:
    credential = AttestedCredentialData.create(Aaguid.NONE, credential_id, public_key)
    flags = AuthenticatorData.FLAG.UP | AuthenticatorData.FLAG.UV | AuthenticatorData.FLAG.AT
    if backup_eligible:
        flags |= AuthenticatorData.FLAG.BE
    auth_data = AuthenticatorData.create(
        sha256(_RP_ID.encode("ascii")),
        flags,
        0,
        credential,
    )
    attestation = AttestationObject.create("none", auth_data, {})
    client_data = CollectedClientData.create(
        CollectedClientData.TYPE.CREATE,
        challenge,
        _ORIGIN,
    )
    encoded_id = websafe_encode(credential_id)
    return {
        "id": encoded_id,
        "rawId": encoded_id,
        "type": "public-key",
        "response": {
            "clientDataJSON": client_data.b64,
            "attestationObject": websafe_encode(attestation),
        },
    }


def _authentication_response(
    *,
    challenge: bytes,
    credential_id: bytes,
    user_handle: bytes,
    private_key: ec.EllipticCurvePrivateKey,
    counter: int,
    backed_up: bool,
) -> dict[str, object]:
    flags = AuthenticatorData.FLAG.UP | AuthenticatorData.FLAG.UV | AuthenticatorData.FLAG.BE
    if backed_up:
        flags |= AuthenticatorData.FLAG.BS
    auth_data = AuthenticatorData.create(
        sha256(_RP_ID.encode("ascii")),
        flags,
        counter,
    )
    client_data = CollectedClientData.create(
        CollectedClientData.TYPE.GET,
        challenge,
        _ORIGIN,
    )
    signature = private_key.sign(
        auth_data + client_data.hash,
        ec.ECDSA(hashes.SHA256()),
    )
    encoded_id = websafe_encode(credential_id)
    return {
        "id": encoded_id,
        "rawId": encoded_id,
        "type": "public-key",
        "response": {
            "clientDataJSON": client_data.b64,
            "authenticatorData": websafe_encode(auth_data),
            "signature": websafe_encode(signature),
            "userHandle": websafe_encode(user_handle),
        },
    }


def test_webauthn_policy_is_exact_and_phishing_resistant() -> None:
    policy = _policy()

    assert policy.rp_id == _RP_ID
    assert policy.origin_allowed(_ORIGIN)
    assert not policy.origin_allowed("https://evil.dante.test")
    assert policy.resident_key is ResidentKeyRequirement.REQUIRED
    assert policy.user_verification is UserVerificationRequirement.REQUIRED
    assert policy.attestation is AttestationConveyancePreference.NONE


def test_webauthn_registration_and_assertion_use_real_fido2_verification() -> None:
    policy = _policy()
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = ES256.from_cryptography_key(private_key.public_key())
    credential_id = b"credential-id-0001"
    user_handle = b"u" * 32
    registration_challenge = b"r" * 32

    registration_response = _registration_response(
        challenge=registration_challenge,
        credential_id=credential_id,
        public_key=public_key,
    )
    parsed_registration = policy.parse_registration(registration_response)
    evidence = policy.verify_registration(
        response=registration_response,
        expected_challenge=registration_challenge,
    )

    assert parsed_registration.challenge == registration_challenge
    assert parsed_registration.origin == _ORIGIN
    assert evidence.credential_id == credential_id
    assert evidence.cose_algorithm == ES256.ALGORITHM
    assert evidence.backup_eligible is True
    assert evidence.backup_state is False

    assertion_challenge = b"a" * 32
    assertion_response = _authentication_response(
        challenge=assertion_challenge,
        credential_id=credential_id,
        user_handle=user_handle,
        private_key=private_key,
        counter=7,
        backed_up=True,
    )
    parsed_assertion = policy.parse_authentication(assertion_response)
    assertion = policy.verify_authentication(
        response=assertion_response,
        expected_challenge=assertion_challenge,
        credential_id=credential_id,
        public_key_cose=evidence.public_key_cose,
        cose_algorithm=evidence.cose_algorithm,
    )

    assert parsed_assertion.user_handle == user_handle
    assert assertion.credential_id == credential_id
    assert assertion.sign_count == 7
    assert assertion.backup_eligible is True
    assert assertion.backup_state is True
