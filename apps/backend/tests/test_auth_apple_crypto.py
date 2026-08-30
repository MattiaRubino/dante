"""Focused M5-B Apple grant AEAD tests."""

from uuid import uuid7

import pytest
from pydantic import SecretStr

from dante.auth.apple_crypto import AppleGrantCipher, AppleGrantCryptoError


def test_apple_grant_round_trip_and_rotation() -> None:
    grant_ref = uuid7()
    old_key = b"a" * 32
    new_key = b"b" * 32
    old = AppleGrantCipher(key_ring={"v1": old_key}, current_key_id="v1")
    encrypted = old.encrypt(
        plaintext=SecretStr("refresh-token"),
        grant_ref=grant_ref,
        client_id="com.dante.web",
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
        client_id="com.dante.web",
    )
    assert decrypted.get_secret_value() == "refresh-token"


def test_apple_grant_aad_mismatch_fails() -> None:
    grant_ref = uuid7()
    cipher = AppleGrantCipher(key_ring={"v1": b"a" * 32}, current_key_id="v1")
    encrypted = cipher.encrypt(
        plaintext=SecretStr("refresh-token"),
        grant_ref=grant_ref,
        client_id="com.dante.web",
    )
    with pytest.raises(AppleGrantCryptoError):
        cipher.decrypt(
            key_id=encrypted.key_id,
            nonce=encrypted.nonce,
            ciphertext=encrypted.ciphertext,
            grant_ref=grant_ref,
            client_id="different-client",
        )
