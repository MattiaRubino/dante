"""Strict provider compact-JWS admission and trusted-JWK verification."""

from __future__ import annotations

import json
from base64 import b64decode, urlsafe_b64encode
from binascii import Error as BinasciiError
from dataclasses import dataclass
from typing import Any

from joserfc import jwt
from joserfc.jwk import KeySet

_FORBIDDEN_KEY_HEADERS = frozenset({"jku", "jwk", "x5u", "x5c"})
_FORBIDDEN_ALGORITHM_PREFIXES = ("HS",)


class JoseBoundaryError(ValueError):
    """Provider token failed DANTE's cryptographic/header trust boundary."""


@dataclass(frozen=True, slots=True)
class CompactJwtHeader:
    alg: str
    kid: str
    typ: str | None
    raw: dict[str, Any]


@dataclass(frozen=True, slots=True)
class VerifiedCompactJwt:
    header: dict[str, Any]
    claims: dict[str, Any]


def _json_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise JoseBoundaryError("duplicate JOSE protected-header member")
        result[key] = value
    return result


def _decode_canonical_segment(
    segment: str,
    *,
    maximum_bytes: int,
    label: str,
) -> bytes:
    if not segment or "=" in segment:
        raise JoseBoundaryError("compact-JWS segment must use unpadded Base64URL")
    try:
        encoded = segment.encode("ascii")
        decoded = b64decode(encoded + b"=" * (-len(encoded) % 4), altchars=b"-_", validate=True)
    except (UnicodeEncodeError, BinasciiError, ValueError) as exc:
        raise JoseBoundaryError("compact-JWS segment is not canonical Base64URL") from exc
    if len(decoded) > maximum_bytes:
        raise JoseBoundaryError(f"{label} exceeds configured bound")
    if urlsafe_b64encode(decoded).rstrip(b"=").decode("ascii") != segment:
        raise JoseBoundaryError("compact-JWS segment is not canonical Base64URL")
    return decoded


def parse_compact_header(
    token: str,
    *,
    allowed_algorithms: tuple[str, ...],
    max_token_bytes: int,
    max_header_bytes: int,
) -> CompactJwtHeader:
    """Admit only the exact compact-JWS header subset DANTE governs."""
    try:
        token_bytes = token.encode("ascii")
    except UnicodeEncodeError as exc:
        raise JoseBoundaryError("provider token must be ASCII") from exc
    if len(token_bytes) > max_token_bytes:
        raise JoseBoundaryError("provider token exceeds configured bound")
    segments = token.split(".")
    if len(segments) != 3 or any(not segment for segment in segments):
        raise JoseBoundaryError("provider token must be a three-segment compact JWS")

    protected = _decode_canonical_segment(
        segments[0],
        maximum_bytes=max_header_bytes,
        label="JOSE protected header",
    )
    _decode_canonical_segment(
        segments[1],
        maximum_bytes=max_token_bytes,
        label="JOSE payload",
    )
    _decode_canonical_segment(
        segments[2],
        maximum_bytes=max_token_bytes,
        label="JOSE signature",
    )

    try:
        header = json.loads(protected, object_pairs_hook=_json_no_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise JoseBoundaryError("JOSE protected header is not a JSON object") from exc
    if not isinstance(header, dict):
        raise JoseBoundaryError("JOSE protected header must be a JSON object")
    if _FORBIDDEN_KEY_HEADERS.intersection(header):
        raise JoseBoundaryError("token-controlled JOSE key resolution is forbidden")
    if "enc" in header:
        raise JoseBoundaryError("JWE is forbidden at the provider ID-token boundary")
    if "crit" in header:
        raise JoseBoundaryError("JOSE crit extensions are not admitted")
    if header.get("b64") is False:
        raise JoseBoundaryError("JOSE b64=false is not admitted")
    alg = header.get("alg")
    if not isinstance(alg, str) or alg == "none" or alg.startswith(_FORBIDDEN_ALGORITHM_PREFIXES):
        raise JoseBoundaryError("unsigned/HMAC provider tokens are forbidden")
    if alg not in allowed_algorithms:
        raise JoseBoundaryError("provider token algorithm is outside the configured allowlist")
    kid = header.get("kid")
    if not isinstance(kid, str) or not kid or len(kid) > 256 or kid.strip() != kid:
        raise JoseBoundaryError("provider token requires one bounded canonical kid")
    typ = header.get("typ")
    if typ is not None and typ != "JWT":
        raise JoseBoundaryError("provider token typ, when present, must be JWT")
    return CompactJwtHeader(alg=alg, kid=kid, typ=typ, raw=header)


def verify_compact_jwt(
    token: str,
    *,
    trusted_jwks: dict[str, Any],
    allowed_algorithms: tuple[str, ...],
    max_token_bytes: int,
    max_header_bytes: int,
) -> VerifiedCompactJwt:
    """Verify a compact JWT against caller-supplied trusted public JWK material."""
    admitted = parse_compact_header(
        token,
        allowed_algorithms=allowed_algorithms,
        max_token_bytes=max_token_bytes,
        max_header_bytes=max_header_bytes,
    )
    keys = trusted_jwks.get("keys")
    if not isinstance(keys, list):
        raise JoseBoundaryError("trusted JWKS must contain a keys array")
    matching = [key for key in keys if isinstance(key, dict) and key.get("kid") == admitted.kid]
    if len(matching) != 1:
        raise JoseBoundaryError("trusted JWKS does not contain exactly one admitted kid")
    try:
        key_set = KeySet.import_key_set({"keys": matching})
        decoded = jwt.decode(token, key_set, algorithms=list(allowed_algorithms))
    except Exception as exc:  # library exceptions are deliberately normalized at this boundary
        raise JoseBoundaryError("provider token signature verification failed") from exc
    header = dict(decoded.header)
    claims = dict(decoded.claims)
    return VerifiedCompactJwt(header=header, claims=claims)
