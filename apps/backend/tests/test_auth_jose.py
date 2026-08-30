"""Focused M5-B JOSE boundary tests."""

import json
from base64 import urlsafe_b64encode

import pytest

from dante.auth.jose import JoseBoundaryError, parse_compact_header


def _segment(value: dict[str, object]) -> str:
    raw = json.dumps(value, separators=(",", ":")).encode()
    return urlsafe_b64encode(raw).rstrip(b"=").decode()


def _token(header: dict[str, object]) -> str:
    return f"{_segment(header)}.e30.signature"


@pytest.mark.parametrize(
    "header",
    [
        {"alg": "none", "kid": "k"},
        {"alg": "HS256", "kid": "k"},
        {"alg": "ES256", "kid": "k"},
        {"alg": "RS256", "kid": "k", "jku": "https://evil.test/jwks"},
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


def test_accepts_exact_rs256_header_boundary() -> None:
    admitted = parse_compact_header(
        _token({"alg": "RS256", "kid": "provider-key", "typ": "JWT"}),
        allowed_algorithms=("RS256",),
        max_token_bytes=16_384,
        max_header_bytes=4_096,
    )
    assert admitted.alg == "RS256"
    assert admitted.kid == "provider-key"
