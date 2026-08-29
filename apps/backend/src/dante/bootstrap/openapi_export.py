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
from dante.platform.config.auth import AuthSettings, SmtpSecurity
from dante.platform.config.database import DatabaseSettings
from dante.platform.config.settings import Environment, Settings

_EXPORT_PEPPER_KEY_ID = "openapi-password-v1"
_EXPORT_OTP_KEY_ID = "openapi-signup-otp-v1"
_HTTP_METHODS = frozenset({"get", "post", "put", "patch", "delete", "options", "head", "trace"})
_PROBLEM_SCHEMA_REF = "#/components/schemas/ProblemDetails"
_M4_POST_PATHS = (
    "/api/v1/auth/signup",
    "/api/v1/auth/signup/verify",
    "/api/v1/auth/signup/resend",
    "/api/v1/auth/recovery",
    "/api/v1/auth/recovery/validate",
    "/api/v1/auth/reset-password",
    "/api/v1/auth/reauthenticate",
)


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
            signup_otp_current_key_id=_EXPORT_OTP_KEY_ID,
            signup_otp_keys={
                _EXPORT_OTP_KEY_ID: SecretStr(_secret(b"o" * 32)),
            },
            smtp_host="127.0.0.1",
            smtp_port=1025,
            smtp_security=SmtpSecurity.PLAIN,
            smtp_from_address="no-reply@dante.test",
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


def _require_literal_discriminator(
    schemas: dict[str, Any],
    *,
    schema_name: str,
    property_name: str,
) -> None:
    schema = cast(dict[str, Any], schemas[schema_name])
    properties = cast(dict[str, Any], schema["properties"])
    discriminator = cast(dict[str, Any], properties[property_name])
    discriminator.pop("default", None)
    required = list(cast(list[str], schema.get("required", [])))
    if property_name not in required:
        required.append(property_name)
    schema["required"] = sorted(required)


def _require_discriminators(document: dict[str, Any]) -> None:
    """Keep default-valued wire discriminators mandatory in generated validators."""
    components = cast(dict[str, Any], document["components"])
    schemas = cast(dict[str, Any], components["schemas"])
    for schema_name in ("AuthenticatedSessionResponse", "UnauthenticatedSessionResponse"):
        _require_literal_discriminator(
            schemas,
            schema_name=schema_name,
            property_name="authenticated",
        )
    _require_literal_discriminator(
        schemas,
        schema_name="SignupAuthenticatedResponse",
        property_name="outcome",
    )
    _require_literal_discriminator(
        schemas,
        schema_name="ExistingAccountSignupResponse",
        property_name="outcome",
    )
    _require_literal_discriminator(
        schemas,
        schema_name="SignupCreatedResponse",
        property_name="verification_required",
    )
    _require_literal_discriminator(
        schemas,
        schema_name="RecoveryAcceptedResponse",
        property_name="accepted",
    )


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
            for status, response_value in responses.items():
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
                if status == "429":
                    headers["Retry-After"] = _response_header(
                        "Minimum delay before another equivalent attempt is useful when supplied."
                    )

    cookie_successes = (
        (
            "/api/v1/auth/signin",
            "post",
            "200",
            "Establishes the host-only HttpOnly Secure __Host-dante-session cookie.",
        ),
        (
            "/api/v1/auth/signup/verify",
            "post",
            "200",
            "May establish __Host-dante-session only for the authenticated signup outcome.",
        ),
        (
            "/api/v1/auth/reauthenticate",
            "post",
            "200",
            "Rotates the bearer on the same AuthSession through __Host-dante-session.",
        ),
        (
            "/api/v1/auth/reset-password",
            "post",
            "204",
            "Defensively clears any current __Host-dante-session cookie after recovery reset.",
        ),
        (
            "/api/v1/auth/session",
            "delete",
            "204",
            "Clears the current __Host-dante-session cookie.",
        ),
    )
    for path, method, status, description in cookie_successes:
        operation = _operation(document, path, method)
        response = cast(dict[str, Any], cast(dict[str, Any], operation["responses"])[status])
        headers = cast(dict[str, Any], response.setdefault("headers", {}))
        headers["Set-Cookie"] = _response_header(description)

    get_session = _operation(document, "/api/v1/auth/session", "get")
    get_200 = cast(dict[str, Any], cast(dict[str, Any], get_session["responses"])["200"])
    get_headers = cast(dict[str, Any], get_200.setdefault("headers", {}))
    get_headers["Set-Cookie"] = _response_header(
        "May clear an invalid or expired __Host-dante-session cookie."
    )


def _browser_policy() -> dict[str, Any]:
    return {
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


def _annotate_browser_security(document: dict[str, Any]) -> None:
    """Record browser-managed ingress rules without generating forbidden browser headers."""
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

    browser_policy = _browser_policy()
    _operation(document, "/api/v1/auth/signin", "post")["x-dante-browser-security"] = browser_policy
    for path in _M4_POST_PATHS:
        _operation(document, path, "post")["x-dante-browser-security"] = browser_policy

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

    reauth = _operation(document, "/api/v1/auth/reauthenticate", "post")
    reauth["security"] = [{"DanteSessionCookie": []}]
    reauth["x-dante-browser-security"] = {
        **browser_policy,
        "csrf_header": {
            "owner": "web_transport",
            "name": "X-Dante-CSRF",
            "required": True,
        },
    }


def _harden_contract(document: dict[str, Any]) -> dict[str, Any]:
    _normalize_problem_media_types(document)
    _require_discriminators(document)
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
