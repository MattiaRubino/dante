"""Deterministic offline OpenAPI export for governed first-party client generation."""

from __future__ import annotations

import argparse
import json
from base64 import urlsafe_b64encode
from collections.abc import Sequence
from pathlib import Path
from typing import Any, cast

from pydantic import SecretStr

from dante.bootstrap.app import create_app
from dante.platform.config.auth import AuthSettings
from dante.platform.config.database import DatabaseSettings
from dante.platform.config.settings import Environment, Settings

_EXPORT_PEPPER_KEY_ID = "openapi-v1"
_HTTP_METHODS = frozenset({"get", "post", "put", "patch", "delete", "options", "head", "trace"})
_PROBLEM_SCHEMA_REF = "#/components/schemas/ProblemDetails"


def _secret(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _export_settings() -> Settings:
    """Build synthetic validated settings without live services or production secrets."""
    return Settings(
        env=Environment.LOCAL,
        release_sha="openapi",
        build_id="openapi",
        debug=False,
        database=DatabaseSettings(
            host="127.0.0.1",
            name="dante_openapi",
            user="dante_runtime",
            password=SecretStr("openapi-export-does-not-connect"),
        ),
        auth=AuthSettings(
            canonical_web_origin="https://dante.test",
            password_current_pepper_key_id=_EXPORT_PEPPER_KEY_ID,
            password_peppers={
                _EXPORT_PEPPER_KEY_ID: SecretStr(_secret(b"p" * 32)),
            },
            csrf_key=SecretStr(_secret(b"c" * 32)),
            kdf_max_concurrency=1,
            signin_rate_capacity=10,
            signin_rate_window_seconds=60.0,
        ),
    )


def _operation(document: dict[str, Any], path: str, method: str) -> dict[str, Any]:
    paths = cast(dict[str, Any], document["paths"])
    path_item = cast(dict[str, Any], paths[path])
    return cast(dict[str, Any], path_item[method])


def _normalize_problem_media_types(document: dict[str, Any]) -> None:
    """Describe RFC 9457 responses with their actual runtime media type."""
    paths = cast(dict[str, Any], document["paths"])
    for path_item_value in paths.values():
        path_item = cast(dict[str, Any], path_item_value)
        for method, operation_value in path_item.items():
            if method not in _HTTP_METHODS or not isinstance(operation_value, dict):
                continue
            operation = cast(dict[str, Any], operation_value)
            responses = cast(dict[str, Any], operation.get("responses", {}))
            for response_value in responses.values():
                if not isinstance(response_value, dict):
                    continue
                response = cast(dict[str, Any], response_value)
                content = response.get("content")
                if not isinstance(content, dict):
                    continue
                media_types = cast(dict[str, Any], content)
                json_content = media_types.get("application/json")
                if not isinstance(json_content, dict):
                    continue
                schema = cast(dict[str, Any], json_content).get("schema")
                if isinstance(schema, dict) and schema.get("$ref") == _PROBLEM_SCHEMA_REF:
                    media_types["application/problem+json"] = media_types.pop("application/json")


def _require_session_discriminators(document: dict[str, Any]) -> None:
    """Make the response discriminator explicit even though Pydantic supplies its value."""
    components = cast(dict[str, Any], document["components"])
    schemas = cast(dict[str, Any], components["schemas"])
    for schema_name in ("AuthenticatedSessionResponse", "UnauthenticatedSessionResponse"):
        schema = cast(dict[str, Any], schemas[schema_name])
        properties = cast(dict[str, Any], schema["properties"])
        authenticated = cast(dict[str, Any], properties["authenticated"])
        authenticated.pop("default", None)
        required = list(cast(list[str], schema.get("required", [])))
        if "authenticated" not in required:
            required.append("authenticated")
        schema["required"] = sorted(required)


def _response_header(description: str, *, const: str | None = None) -> dict[str, Any]:
    schema: dict[str, Any] = {"type": "string"}
    if const is not None:
        schema["const"] = const
    return {"description": description, "schema": schema}


def _annotate_auth_response_headers(document: dict[str, Any]) -> None:
    """Document response metadata enforced by the Auth request-context boundary."""
    paths = cast(dict[str, Any], document["paths"])
    for path, path_item_value in paths.items():
        if not path.startswith("/api/v1/auth/"):
            continue
        path_item = cast(dict[str, Any], path_item_value)
        for method, operation_value in path_item.items():
            if method not in _HTTP_METHODS or not isinstance(operation_value, dict):
                continue
            operation = cast(dict[str, Any], operation_value)
            responses = cast(dict[str, Any], operation.get("responses", {}))
            for response_value in responses.values():
                if not isinstance(response_value, dict):
                    continue
                response = cast(dict[str, Any], response_value)
                headers = cast(dict[str, Any], response.setdefault("headers", {}))
                headers["X-Request-ID"] = _response_header(
                    "Server-authoritative non-secret request correlation identifier."
                )
                headers["Cache-Control"] = _response_header(
                    "Auth responses are never cacheable by shared or browser caches.",
                    const="no-store",
                )

    signin = _operation(document, "/api/v1/auth/signin", "post")
    signin_200 = cast(dict[str, Any], cast(dict[str, Any], signin["responses"])["200"])
    signin_headers = cast(dict[str, Any], signin_200.setdefault("headers", {}))
    signin_headers["Set-Cookie"] = _response_header(
        "May establish the host-only HttpOnly Secure __Host-dante-session cookie."
    )

    get_session = _operation(document, "/api/v1/auth/session", "get")
    get_200 = cast(dict[str, Any], cast(dict[str, Any], get_session["responses"])["200"])
    get_headers = cast(dict[str, Any], get_200.setdefault("headers", {}))
    get_headers["Set-Cookie"] = _response_header(
        "May clear an invalid or expired __Host-dante-session cookie."
    )

    logout = _operation(document, "/api/v1/auth/session", "delete")
    logout_204 = cast(dict[str, Any], cast(dict[str, Any], logout["responses"])["204"])
    logout_headers = cast(dict[str, Any], logout_204.setdefault("headers", {}))
    logout_headers["Set-Cookie"] = _response_header(
        "Clears the current __Host-dante-session cookie."
    )

    signin_429 = cast(dict[str, Any], cast(dict[str, Any], signin["responses"])["429"])
    rate_headers = cast(dict[str, Any], signin_429.setdefault("headers", {}))
    rate_headers["Retry-After"] = _response_header(
        "Minimum delay before another signin attempt is useful."
    )


def _annotate_browser_security(document: dict[str, Any]) -> None:
    """Record browser-managed ingress rules without generating forbidden request headers."""
    components = cast(dict[str, Any], document["components"])
    security_schemes = cast(dict[str, Any], components.setdefault("securitySchemes", {}))
    security_schemes["DanteSessionCookie"] = {
        "type": "apiKey",
        "in": "cookie",
        "name": "__Host-dante-session",
        "description": (
            "Opaque host-only HttpOnly Secure AuthSession bearer cookie; browser transport owns it."
        ),
    }

    browser_policy: dict[str, Any] = {
        "origin": {
            "owner": "browser",
            "required": True,
            "must_equal": "canonical_web_origin",
        },
        "sec_fetch_site": {
            "owner": "browser",
            "required": True,
            "required_value": "same-origin",
        },
        "client_header": {
            "owner": "web_transport",
            "name": "X-Dante-Client",
            "required": True,
            "required_value": "web",
        },
    }

    signin = _operation(document, "/api/v1/auth/signin", "post")
    signin["x-dante-browser-security"] = browser_policy

    get_session = _operation(document, "/api/v1/auth/session", "get")
    get_session["security"] = [{}, {"DanteSessionCookie": []}]

    logout = _operation(document, "/api/v1/auth/session", "delete")
    logout["security"] = [{}, {"DanteSessionCookie": []}]
    logout["x-dante-browser-security"] = {
        **browser_policy,
        "csrf_header": {
            "owner": "web_transport",
            "name": "X-Dante-CSRF",
            "required_when": "valid_auth_session_admitted",
        },
    }


def _harden_contract(document: dict[str, Any]) -> dict[str, Any]:
    _normalize_problem_media_types(document)
    _require_session_discriminators(document)
    _annotate_auth_response_headers(document)
    _annotate_browser_security(document)
    return document


def openapi_document() -> dict[str, Any]:
    """Return the governed product OpenAPI document without running FastAPI lifespan."""
    document = create_app(_export_settings()).openapi()
    return _harden_contract(document)


def render_openapi() -> str:
    """Render stable JSON ordering for reviewable generated-source diffs."""
    return json.dumps(
        openapi_document(),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def write_openapi(target: Path) -> None:
    """Write one deterministic OpenAPI snapshot to the requested repository path."""
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_openapi(), encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    args = parser.parse_args(argv)
    write_openapi(args.target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
