"""Executable M4 contracts for signup OTP and password-recovery proof primitives."""

from uuid import uuid7

import pytest

from dante.auth.contracts import AuthIntegrityError
from dante.auth.proofs import (
    SignupOtpCodec,
    issue_recovery_proof,
    recovery_secret_matches,
    recovery_secret_verifier,
)


def test_signup_otp_is_six_digits_and_bound_to_one_signup_reference() -> None:
    codec = SignupOtpCodec(key_ring={"otp-v1": b"o" * 32}, current_key_id="otp-v1")
    signup_ref = uuid7()
    issued = codec.issue(signup_ref)
    raw_code = issued.code.get_secret_value()

    assert len(raw_code) == 6
    assert raw_code.isascii()
    assert raw_code.isdigit()
    assert len(issued.verifier) == 32
    assert codec.matches(
        signup_ref=signup_ref,
        submitted_code=raw_code,
        expected_verifier=issued.verifier,
        key_id=issued.key_id,
    )
    assert not codec.matches(
        signup_ref=uuid7(),
        submitted_code=raw_code,
        expected_verifier=issued.verifier,
        key_id=issued.key_id,
    )


def test_signup_otp_rejects_noncanonical_input_and_unknown_stored_key() -> None:
    codec = SignupOtpCodec(key_ring={"otp-v1": b"o" * 32}, current_key_id="otp-v1")
    signup_ref = uuid7()
    issued = codec.issue(signup_ref)

    for invalid in ("12345", "1234567", "\uff11\uff12\uff13\uff14\uff15\uff16", "12a456"):
        assert not codec.matches(
            signup_ref=signup_ref,
            submitted_code=invalid,
            expected_verifier=issued.verifier,
            key_id=issued.key_id,
        )

    with pytest.raises(AuthIntegrityError, match="unknown OTP key"):
        codec.matches(
            signup_ref=signup_ref,
            submitted_code=issued.code.get_secret_value(),
            expected_verifier=issued.verifier,
            key_id="retired-missing-key",
        )


def test_recovery_proof_is_canonical_256_bit_single_bearer_material() -> None:
    issued = issue_recovery_proof()
    secret = issued.secret.get_secret_value()

    assert len(issued.verifier) == 32
    assert len(secret) == 43
    assert "=" not in secret
    assert recovery_secret_verifier(secret) == issued.verifier
    assert recovery_secret_matches(secret, issued.verifier)


def test_recovery_proof_rejects_encoding_aliases_and_mutation() -> None:
    issued = issue_recovery_proof()
    secret = issued.secret.get_secret_value()
    replacement = "A" if secret[-1] != "A" else "B"
    mutated = secret[:-1] + replacement

    assert recovery_secret_verifier(secret + "=") is None
    assert recovery_secret_verifier("é" + secret[1:]) is None
    assert not recovery_secret_matches(mutated, issued.verifier)
