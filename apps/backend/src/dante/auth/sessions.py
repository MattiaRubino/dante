"""Opaque AuthSession secret, verifier, cookie and CSRF primitives."""

import hmac
import secrets
from base64 import b64decode, urlsafe_b64encode
from binascii import Error as BinasciiError
from hashlib import sha256
from uuid import UUID

from pydantic import SecretStr

SESSION_COOKIE_NAME = "__Host-dante-session"
CSRF_HEADER_NAME = "X-Dante-CSRF"
WEB_CLIENT_HEADER_NAME = "X-Dante-Client"
WEB_CLIENT_HEADER_VALUE = "web"

_SESSION_SECRET_BYTES = 32
_CSRF_CONTEXT = b"dante.csrf.v1\x00"


class AmbiguousSessionCookieError(ValueError):
    """More than one session-cookie value was supplied on one request."""


def _encode_urlsafe(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def generate_session_secret() -> SecretStr:
    """Generate one canonical unpadded 256-bit CSPRNG bearer secret."""
    return SecretStr(_encode_urlsafe(secrets.token_bytes(_SESSION_SECRET_BYTES)))


def decode_session_secret(value: str) -> bytes | None:
    """Decode only the canonical unpadded Base64URL form of one 256-bit secret."""
    try:
        raw_ascii = value.encode("ascii")
    except UnicodeEncodeError:
        return None

    padding = b"=" * (-len(raw_ascii) % 4)
    try:
        decoded = b64decode(raw_ascii + padding, altchars=b"-_", validate=True)
    except BinasciiError, ValueError:
        return None

    if len(decoded) != _SESSION_SECRET_BYTES:
        return None
    if _encode_urlsafe(decoded) != value:
        return None
    return decoded


def session_cookie_value(
    raw_headers: list[tuple[bytes, bytes]],
) -> str | None:
    """Return exactly one session cookie and reject duplicate-name ambiguity."""
    values: list[str] = []
    for raw_name, raw_value in raw_headers:
        if raw_name.lower() != b"cookie":
            continue
        try:
            cookie_header = raw_value.decode("latin-1")
        except UnicodeDecodeError:
            continue
        for raw_pair in cookie_header.split(";"):
            name, separator, value = raw_pair.strip().partition("=")
            if separator and name == SESSION_COOKIE_NAME:
                values.append(value)

    if len(values) > 1:
        raise AmbiguousSessionCookieError("duplicate session cookie")
    return values[0] if values else None


def session_secret_verifier_from_raw(raw_secret: bytes) -> bytes:
    """Derive the indexed PostgreSQL verifier for one random bearer secret."""
    return sha256(raw_secret).digest()


def session_secret_verifier(secret: SecretStr) -> bytes:
    """Derive a verifier from a generated SecretStr bearer value."""
    raw = decode_session_secret(secret.get_secret_value())
    if raw is None:
        raise ValueError("generated session secret violated its encoding contract")
    return session_secret_verifier_from_raw(raw)


def derive_csrf_token(
    *,
    csrf_key: bytes,
    auth_session_ref: UUID,
    secret_verifier: bytes,
) -> SecretStr:
    """Derive an unpredictable session-bound synchronizer token without DB state."""
    message = _CSRF_CONTEXT + auth_session_ref.bytes + secret_verifier
    return SecretStr(_encode_urlsafe(hmac.digest(csrf_key, message, "sha256")))


def csrf_token_matches(expected: SecretStr, supplied: str | None) -> bool:
    """Compare a supplied CSRF token without timing-sensitive string equality."""
    if supplied is None:
        return False
    return hmac.compare_digest(expected.get_secret_value(), supplied)
