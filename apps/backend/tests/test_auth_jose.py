"""Focused M5-B JOSE boundary tests."""

from __future__ import annotations

import json
from base64 import urlsafe_b64encode

import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from dante.auth.jose import JoseBoundaryError, parse_compact_header, verify_compact_jwt


def _b64url(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _segment(value: dict[str, object]) -> str:
    raw = json.dumps(value, separators=(",", ":"), sort_keys=True).encode()
    return _b64url(raw)


def _token(header: dict[str, object]) -> str:
    return f"{_segment(header)}.e30.signature"


def _unsigned_integer(value: int) -> str:
    size = max(1, (value.bit_length() + 7) // 8)
    return _b64url(value.to_bytes(size, "big"))


def _signed_rs256_token(
    *,
    private_key: rsa.RSAPrivateKey,
    kid: str,
    claims: dict[str, object],
) -> str:
    header_segment = _segment({"alg": "RS256", "kid": kid, "typ": "JWT"})
    claims_segment = _segment(claims)
    signing_input = f"{header_segment}.{claims_segment}".encode("ascii")
    signature = private_key.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
    return f"{header_segment}.{claims_segment}.{_b64url(signature)}"


def _public_jwk(private_key: rsa.RSAPrivateKey, *, kid: str) -> dict[str, str]:
    numbers = private_key.public_key().public_numbers()
    return {
        "kty": "RSA",
        "kid": kid,
        "use": "sig",
        "alg": "RS256",
        "n": _unsigned_integer(numbers.n),
        "e": _unsigned_integer(numbers.e),
    }


@pytest.mark.parametrize(
    "header",
    [
        {"alg": "none", "kid": "k"},
        {"alg": "HS256", "kid": "k"},
        {"alg": "ES256", "kid": "k"},
        {"alg": "RS256", "kid": "k", "jku": "https://evil.test/jwks"},
        {"alg": "RS256", "kid": "k", "jwk": {"kty": "RSA"}},
        {"alg": "RS256", "kid": "k", "x5u": "https://evil.test/cert"},
        {"alg": "RS256", "kid": "k", "x5c": ["certificate"]},
        {"alg": "RS256", "kid": "k", "crit": ["exp"]},
        {"alg": "RS256", "kid": "k", "b64": False},
        {"alg": "RS256", "kid": "k", "enc": "A256GCM"},
    ],
)
def test_rejects_untrusted_jose_header_controls(header: dict[str, object]) -> None:
    with pytest.raises(JoseBoundaryError):
        parse_compact_header(
            _token(header),
            allowed_algorithms=("RS256",),
            max_token_bytes=16_384,
            max_header_bytes=4_096,
        )


def test_duplicate_protected_header_member_is_rejected() -> None:
    duplicate_header = _b64url(b'{"alg":"RS256","alg":"RS256","kid":"k"}')
    with pytest.raises(JoseBoundaryError, match="duplicate JOSE"):
        parse_compact_header(
            f"{duplicate_header}.e30.signature",
            allowed_algorithms=("RS256",),
            max_token_bytes=16_384,
            max_header_bytes=4_096,
        )


def test_accepts_exact_rs256_header_boundary() -> None:
    admitted = parse_compact_header(
        _token({"alg": "RS256", "kid": "provider-key", "typ": "JWT"}),
        allowed_algorithms=("RS256",),
        max_token_bytes=16_384,
        max_header_bytes=4_096,
    )
    assert admitted.alg == "RS256"
    assert admitted.kid == "provider-key"


def test_generated_rsa_rs256_token_verifies_with_trusted_public_jwk() -> None:
    private_key = rsa.generate_private_key(public_exponent=65_537, key_size=2_048)
    kid = "provider-key"
    claims = {"sub": "provider-subject", "nonce": "test-nonce"}
    token = _signed_rs256_token(private_key=private_key, kid=kid, claims=claims)

    verified = verify_compact_jwt(
        token,
        trusted_jwks={"keys": [_public_jwk(private_key, kid=kid)]},
        allowed_algorithms=("RS256",),
        max_token_bytes=16_384,
        max_header_bytes=4_096,
    )

    assert verified.header["alg"] == "RS256"
    assert verified.header["kid"] == kid
    assert verified.claims == claims


def test_rs256_signature_tampering_is_rejected() -> None:
    private_key = rsa.generate_private_key(public_exponent=65_537, key_size=2_048)
    kid = "provider-key"
    token = _signed_rs256_token(
        private_key=private_key,
        kid=kid,
        claims={"sub": "provider-subject"},
    )
    header, _claims, signature = token.split(".")
    tampered_claims = _segment({"sub": "attacker-subject"})

    with pytest.raises(JoseBoundaryError, match="signature verification failed"):
        verify_compact_jwt(
            f"{header}.{tampered_claims}.{signature}",
            trusted_jwks={"keys": [_public_jwk(private_key, kid=kid)]},
            allowed_algorithms=("RS256",),
            max_token_bytes=16_384,
            max_header_bytes=4_096,
        )
