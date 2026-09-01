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
_FIRST_PARTY_BROWSER_MUTATIONS = (
    ("/api/v1/auth/signin", "post"),
    ("/api/v1/auth/signup", "post"),
    ("/api/v1/auth/signup/verify", "post"),
    ("/api/v1/auth/signup/resend", "post"),
    ("/api/v1/auth/recovery", "post"),
    ("/api/v1/auth/recovery/validate", "post"),
    ("/api/v1/auth/reset-password", "post"),
    ("/api/v1/auth/reauthenticate", "post"),
    ("/api/v1/auth/session", "delete"),
    ("/api/v1/auth/password/establish", "post"),
    ("/api/v1/auth/password", "delete"),
    ("/api/v1/auth/google/begin", "post"),
    ("/api/v1/auth/google/complete", "post"),
    ("/api/v1/auth/apple/begin", "post"),
    ("/api/v1/auth/provider-enrollment/email", "post"),
    ("/api/v1/auth/provider-enrollment/verify", "post"),
    ("/api/v1/auth/provider-enrollment/resend", "post"),
    ("/api/v1/auth/provider-link/confirm", "post"),
    ("/api/v1/auth/providers/{external_identity_ref}", "delete"),
    ("/api/v1/auth/passkeys/registration/begin", "post"),
    ("/api/v1/auth/passkeys/registration/complete", "post"),
    ("/api/v1/auth/passkeys/authentication/begin", "post"),
    ("/api/v1/auth/passkeys/authentication/complete", "post"),
    ("/api/v1/auth/passkeys/reauthentication/begin", "post"),
    ("/api/v1/auth/passkeys/reauthentication/complete", "post"),
    ("/api/v1/auth/passkeys/{passkey_credential_ref}", "patch"),
    ("/api/v1/auth/passkeys/{passkey_credential_ref}", "delete"),
)
_AUTHENTICATED_OPERATIONS = (
    ("/api/v1/auth/methods", "get"),
    ("/api/v1/auth/reauthenticate", "post"),
    ("/api/v1/auth/password/establish", "post"),
    ("/api/v1/auth/password", "delete"),
    ("/api/v1/auth/providers/{external_identity_ref}", "delete"),
    ("/api/v1/auth/passkeys/registration/begin", "post"),
    ("/api/v1/auth/passkeys/registration/complete", "post"),
    ("/api/v1/auth/passkeys/reauthentication/begin", "post"),
    ("/api/v1/auth/passkeys/reauthentication/complete", "post"),
    ("/api/v1/auth/passkeys/{passkey_credential_ref}", "patch"),
    ("/api/v1/auth/passkeys/{passkey_credential_ref}", "delete"),
)
_AUTHENTICATED_CSRF_MUTATIONS = tuple(
    operation for operation in _AUTHENTICATED_OPERATIONS if operation[1] != "get"
)
_PROVIDER_BEGIN_OPERATIONS = (
    ("/api/v1/auth/google/begin", "post"),
    ("/api/v1/auth/apple/begin", "post"),
)
_PROVIDER_ENROLLMENT_OPERATIONS = (
    ("/api/v1/auth/provider-enrollment", "get"),
    ("/api/v1/auth/provider-enrollment/email", "post"),
    ("/api/v1/auth/provider-enrollment/verify", "post"),
    ("/api/v1/auth/provider-enrollment/resend", "post"),
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
    for schema_name in ("SignupAuthenticatedResponse", "ExistingAccountSignupResponse"):
        _require_literal_discriminator(
            schemas,
            schema_name=schema_name,
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
    for schema_name in (
        "ProviderAuthenticatedResponse",
        "ProviderLinkRequiredResponse",
        "ProviderEnrollmentRequiredResponse",
    ):
        _require_literal_discriminator(
            schemas,
            schema_name=schema_name,
            property_name="outcome",
        )
    _require_literal_discriminator(
        schemas,
        schema_name="ProviderAuthenticatedResponse",
        property_name="authenticated",
    )


def _response_header(description: str, *, const: str | None = None) -> dict[str, Any]:
    schema: dict[str, Any] = {"type": "string"}
    if const is not None:
        schema["const"] = const
    return {"description": description, "schema": schema}


def _add_response_header(
    document: dict[str, Any],
    *,
    path: str,
    method: str,
    status: str,
    name: str,
    description: str,
) -> None:
    operation = _operation(document, path, method)
    response = cast(dict[str, Any], cast(dict[str, Any], operation["responses"])[status])
    headers = cast(dict[str, Any], response.setdefault("headers", {}))
    headers[name] = _response_header(description)


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

    session_cookie_successes = (
        ("/api/v1/auth/signin", "post", "200", "Establishes a new AuthSession bearer."),
        ("/api/v1/auth/signup/verify", "post", "200", "May establish a new AuthSession bearer."),
        ("/api/v1/auth/reauthenticate", "post", "200", "Rotates the same AuthSession bearer."),
        ("/api/v1/auth/password/establish", "post", "200", "Rotates the same AuthSession bearer."),
        ("/api/v1/auth/password", "delete", "200", "Rotates the same AuthSession bearer."),
        (
            "/api/v1/auth/provider-link/confirm",
            "post",
            "200",
            "Rotates the same AuthSession bearer.",
        ),
        (
            "/api/v1/auth/providers/{external_identity_ref}",
            "delete",
            "200",
            "Rotates the same AuthSession bearer.",
        ),
        (
            "/api/v1/auth/passkeys/registration/complete",
            "post",
            "200",
            "Rotates the same AuthSession bearer.",
        ),
        (
            "/api/v1/auth/passkeys/authentication/complete",
            "post",
            "200",
            "Establishes a new AuthSession bearer.",
        ),
        (
            "/api/v1/auth/passkeys/reauthentication/complete",
            "post",
            "200",
            "Rotates the same AuthSession bearer.",
        ),
        (
            "/api/v1/auth/passkeys/{passkey_credential_ref}",
            "delete",
            "200",
            "Rotates the same AuthSession bearer.",
        ),
    )
    for path, method, status, description in session_cookie_successes:
        _add_response_header(
            document,
            path=path,
            method=method,
            status=status,
            name="Set-Cookie",
            description=f"{description} Cookie: __Host-dante-session.",
        )

    for path, method, status in (
        ("/api/v1/auth/google/complete", "post", "200"),
        ("/api/v1/auth/provider-enrollment/verify", "post", "200"),
    ):
        _add_response_header(
            document,
            path=path,
            method=method,
            status=status,
            name="Set-Cookie",
            description=(
                "Outcome-dependent AuthSession or provider continuation cookie; continuation secrets "
                "never appear in JSON."
            ),
        )

    for path in (
        "/api/v1/auth/provider-enrollment/email",
        "/api/v1/auth/provider-enrollment/resend",
    ):
        _add_response_header(
            document,
            path=path,
            method="post",
            status="200",
            name="Set-Cookie",
            description="Refreshes the bounded __Host-dante-provider-enrollment capability cookie.",
        )

    _add_response_header(
        document,
        path="/api/v1/auth/apple/callback",
        method="post",
        status="303",
        name="Set-Cookie",
        description=(
            "Outcome-dependent AuthSession or provider continuation cookie; continuation secrets "
            "never enter the redirect URL."
        ),
    )
    _add_response_header(
        document,
        path="/api/v1/auth/apple/callback",
        method="post",
        status="303",
        name="Location",
        description="Fixed DANTE destination selected only from stored bounded return_target_code.",
    )

    for path, method, status, description in (
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
    ):
        _add_response_header(
            document,
            path=path,
            method=method,
            status=status,
            name="Set-Cookie",
            description=description,
        )

    get_session = _operation(document, "/api/v1/auth/session", "get")
    get_200 = cast(dict[str, Any], cast(dict[str, Any], get_session["responses"])["200"])
    get_headers = cast(dict[str, Any], get_200.setdefault("headers", {}))
    get_headers["Set-Cookie"] = _response_header(
        "May clear an invalid or expired __Host-dante-session cookie."
    )

    get_methods = _operation(document, "/api/v1/auth/methods", "get")
    methods_401 = cast(dict[str, Any], cast(dict[str, Any], get_methods["responses"])["401"])
    methods_401_headers = cast(dict[str, Any], methods_401.setdefault("headers", {}))
    methods_401_headers["Set-Cookie"] = _response_header(
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


def _csrf_browser_policy(browser_policy: dict[str, Any]) -> dict[str, Any]:
    return {
        **browser_policy,
        "csrf_header": {
            "owner": "web_transport",
            "name": "X-Dante-CSRF",
            "required": True,
        },
    }


def _annotate_apple_form_post(document: dict[str, Any]) -> None:
    operation = _operation(document, "/api/v1/auth/apple/callback", "post")
    operation["requestBody"] = {
        "required": True,
        "content": {
            "application/x-www-form-urlencoded": {
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["state"],
                    "properties": {
                        "state": {"type": "string", "minLength": 1, "maxLength": 256},
                        "code": {"type": "string", "maxLength": 4096},
                        "id_token": {"type": "string", "maxLength": 32768},
                        "user": {"type": "string", "maxLength": 8192},
                        "error": {"type": "string", "maxLength": 256},
                    },
                }
            }
        },
    }
    operation["x-dante-external-ingress"] = {
        "browser_proof_exception": True,
        "required_media_type": "application/x-www-form-urlencoded",
        "authority": "server-side state verifier and provider proof",
    }
    _operation(document, "/api/v1/auth/apple/notifications", "post")["x-dante-external-ingress"] = {
        "browser_proof_exception": True,
        "required_media_type": "application/json",
        "authority": "Apple-signed notification JWS verification",
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
    security_schemes["DanteProviderLinkCookie"] = {
        "type": "apiKey",
        "in": "cookie",
        "name": "__Host-dante-provider-link",
        "description": "Opaque high-entropy provider-link continuation capability.",
    }
    security_schemes["DanteProviderEnrollmentCookie"] = {
        "type": "apiKey",
        "in": "cookie",
        "name": "__Host-dante-provider-enrollment",
        "description": "Opaque high-entropy provider-enrollment continuation capability.",
    }

    browser_policy = _browser_policy()
    for path, method in _FIRST_PARTY_BROWSER_MUTATIONS:
        _operation(document, path, method)["x-dante-browser-security"] = browser_policy

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

    for path, method in _AUTHENTICATED_OPERATIONS:
        _operation(document, path, method)["security"] = [{"DanteSessionCookie": []}]

    csrf_policy = _csrf_browser_policy(browser_policy)
    for path, method in _AUTHENTICATED_CSRF_MUTATIONS:
        _operation(document, path, method)["x-dante-browser-security"] = csrf_policy

    for path, method in _PROVIDER_BEGIN_OPERATIONS:
        operation = _operation(document, path, method)
        operation["security"] = [{}, {"DanteSessionCookie": []}]
        operation["x-dante-browser-security"] = {
            **browser_policy,
            "session_cookie": {
                "required_when": "purpose is link or reauthenticate",
            },
            "csrf_header": {
                "owner": "web_transport",
                "name": "X-Dante-CSRF",
                "required_when": "purpose is link or reauthenticate",
            },
        }

    for path, method in _PROVIDER_ENROLLMENT_OPERATIONS:
        _operation(document, path, method)["security"] = [{"DanteProviderEnrollmentCookie": []}]

    provider_link = _operation(document, "/api/v1/auth/provider-link", "get")
    provider_link["security"] = [{"DanteProviderLinkCookie": []}]

    provider_link_confirm = _operation(document, "/api/v1/auth/provider-link/confirm", "post")
    provider_link_confirm["security"] = [{"DanteSessionCookie": [], "DanteProviderLinkCookie": []}]


def _harden_contract(document: dict[str, Any]) -> dict[str, Any]:
    _normalize_problem_media_types(document)
    _require_discriminators(document)
    _annotate_auth_response_headers(document)
    _annotate_browser_security(document)
    _annotate_apple_form_post(document)
    return document


def openapi_document() -> dict[str, Any]:
    """Return the governed product OpenAPI document without running FastAPI lifespan."""
    document = create_app(_export_settings()).openapi()
    return _harden_contract(document)


def render_openapi() -> str:
    """Render stable JSON ordering for reviewable generated-source diffs."""
    return (
        json.dumps(
            openapi_document(),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


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
