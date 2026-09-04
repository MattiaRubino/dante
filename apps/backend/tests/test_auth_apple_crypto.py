"""Focused M5-B/M5-D Apple grant AEAD tests."""

from uuid import uuid7

import pytest
from pydantic import SecretStr

from dante.auth.apple_crypto import AppleGrantCipher, AppleGrantCryptoError

_SUBJECT = "apple-subject-123"
_CLIENT_ID = "com.dante.web"


def test_apple_grant_round_trip_and_rotation() -> None:
    grant_ref = uuid7()
    old_key = b"a" * 32
    new_key = b"b" * 32
    old = AppleGrantCipher(key_ring={"v1": old_key}, current_key_id="v1")
    encrypted = old.encrypt(
        plaintext=SecretStr("refresh-token"),
        grant_ref=grant_ref,
        subject=_SUBJECT,
        client_id=_CLIENT_ID,
    )
    rotated = AppleGrantCipher(
        key_ring={"v1": old_key, "v2": new_key},
        current_key_id="v2",
    )
    decrypted = rotated.decrypt(
        key_id=encrypted.key_id,
        nonce=encrypted.nonce,
        ciphertext=encrypted.ciphertext,
        grant_ref=grant_ref,
        subject=_SUBJECT,
        client_id=_CLIENT_ID,
    )
    assert decrypted.get_secret_value() == "refresh-token"


@pytest.mark.parametrize(
    ("subject", "client_id"),
    [
        ("different-subject", _CLIENT_ID),
        (_SUBJECT, "different-client"),
    ],
)
def test_apple_grant_aad_identity_mismatch_fails(subject: str, client_id: str) -> None:
    grant_ref = uuid7()
    cipher = AppleGrantCipher(key_ring={"v1": b"a" * 32}, current_key_id="v1")
    encrypted = cipher.encrypt(
        plaintext=SecretStr("refresh-token"),
        grant_ref=grant_ref,
        subject=_SUBJECT,
        client_id=_CLIENT_ID,
    )
    with pytest.raises(AppleGrantCryptoError):
        cipher.decrypt(
            key_id=encrypted.key_id,
            nonce=encrypted.nonce,
            ciphertext=encrypted.ciphertext,
            grant_ref=grant_ref,
            subject=subject,
            client_id=client_id,
        )


def test_apple_grant_unknown_key_id_fails_closed() -> None:
    grant_ref = uuid7()
    cipher = AppleGrantCipher(key_ring={"v1": b"a" * 32}, current_key_id="v1")
    encrypted = cipher.encrypt(
        plaintext=SecretStr("refresh-token"),
        grant_ref=grant_ref,
        subject=_SUBJECT,
        client_id=_CLIENT_ID,
    )

    with pytest.raises(AppleGrantCryptoError, match="unknown encryption key"):
        cipher.decrypt(
            key_id="retired-or-invalid",
            nonce=encrypted.nonce,
            ciphertext=encrypted.ciphertext,
            grant_ref=grant_ref,
            subject=_SUBJECT,
            client_id=_CLIENT_ID,
        )


def test_apple_grant_ciphertext_tampering_fails_authentication() -> None:
    grant_ref = uuid7()
    cipher = AppleGrantCipher(key_ring={"v1": b"a" * 32}, current_key_id="v1")
    encrypted = cipher.encrypt(
        plaintext=SecretStr("refresh-token"),
        grant_ref=grant_ref,
        subject=_SUBJECT,
        client_id=_CLIENT_ID,
    )
    tampered = bytearray(encrypted.ciphertext)
    tampered[-1] ^= 1

    with pytest.raises(AppleGrantCryptoError, match="authentication failed"):
        cipher.decrypt(
            key_id=encrypted.key_id,
            nonce=encrypted.nonce,
            ciphertext=bytes(tampered),
            grant_ref=grant_ref,
            subject=_SUBJECT,
            client_id=_CLIENT_ID,
        )
