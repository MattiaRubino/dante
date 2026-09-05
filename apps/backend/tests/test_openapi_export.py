from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from dante.bootstrap.openapi_export import openapi_document, render_openapi

_EXPECTED_M5_OPERATIONS = {
    ("/api/v1/auth/methods", "get"): "auth_get_authentication_methods",
    ("/api/v1/auth/password/establish", "post"): "auth_establish_password",
    ("/api/v1/auth/password", "delete"): "auth_remove_password",
    ("/api/v1/auth/google/begin", "post"): "auth_begin_google_authentication",
    ("/api/v1/auth/google/complete", "post"): "auth_complete_google_authentication",
    ("/api/v1/auth/apple/begin", "post"): "auth_begin_apple_authentication",
    ("/api/v1/auth/apple/callback", "post"): "auth_handle_apple_callback",
    ("/api/v1/auth/apple/notifications", "post"): "auth_process_apple_notification",
    ("/api/v1/auth/provider-enrollment", "get"): "auth_get_provider_enrollment",
    (
        "/api/v1/auth/provider-enrollment/email",
        "post",
    ): "auth_set_provider_enrollment_email",
    (
        "/api/v1/auth/provider-enrollment/verify",
        "post",
    ): "auth_verify_provider_enrollment",
    (
        "/api/v1/auth/provider-enrollment/resend",
        "post",
    ): "auth_resend_provider_enrollment_verification",
    ("/api/v1/auth/provider-link", "get"): "auth_get_provider_link",
    ("/api/v1/auth/provider-link/confirm", "post"): "auth_confirm_provider_link",
    (
        "/api/v1/auth/providers/{external_identity_ref}",
        "delete",
    ): "auth_unlink_provider",
    (
        "/api/v1/auth/passkeys/registration/begin",
        "post",
    ): "auth_begin_passkey_registration",
    (
        "/api/v1/auth/passkeys/registration/complete",
        "post",
    ): "auth_complete_passkey_registration",
    (
        "/api/v1/auth/passkeys/authentication/begin",
        "post",
    ): "auth_begin_passkey_authentication",
    (
        "/api/v1/auth/passkeys/authentication/complete",
        "post",
    ): "auth_complete_passkey_authentication",
    (
        "/api/v1/auth/passkeys/reauthentication/begin",
        "post",
    ): "auth_begin_passkey_reauthentication",
    (
        "/api/v1/auth/passkeys/reauthentication/complete",
        "post",
    ): "auth_complete_passkey_reauthentication",
    (
        "/api/v1/auth/passkeys/{passkey_credential_ref}",
        "patch",
    ): "auth_update_passkey",
    (
        "/api/v1/auth/passkeys/{passkey_credential_ref}",
        "delete",
    ): "auth_remove_passkey",
}


def _operation(document: dict[str, Any], path: str, method: str) -> dict[str, Any]:
    paths = cast(dict[str, Any], document["paths"])
    return cast(dict[str, Any], cast(dict[str, Any], paths[path])[method])


def test_committed_openapi_snapshot_matches_governed_export() -> None:
    """Fail CI when backend contract changes without regenerating the client source."""
    repo_root = Path(__file__).resolve().parents[3]
    snapshot_path = repo_root / "packages" / "api-client" / "openapi" / "dante-v1.openapi.json"

    committed = json.loads(snapshot_path.read_text(encoding="utf-8"))

    assert committed == openapi_document()


def test_openapi_render_is_byte_deterministic() -> None:
    """Two fresh exports must be byte-identical, not merely schema-equivalent."""
    assert render_openapi() == render_openapi()


def test_complete_m5_operation_inventory_and_operation_ids_are_frozen() -> None:
    document = openapi_document()

    for (path, method), operation_id in _EXPECTED_M5_OPERATIONS.items():
        assert _operation(document, path, method)["operationId"] == operation_id


def test_m5_security_authorities_are_explicit_and_non_interchangeable() -> None:
    document = openapi_document()
    components = cast(dict[str, Any], document["components"])
    security_schemes = cast(dict[str, Any], components["securitySchemes"])

    assert security_schemes["DanteSessionCookie"]["name"] == "__Host-dante-session"
    assert security_schemes["DanteProviderLinkCookie"]["name"] == "__Host-dante-provider-link"
    assert (
        security_schemes["DanteProviderEnrollmentCookie"]["name"]
        == "__Host-dante-provider-enrollment"
    )

    assert _operation(document, "/api/v1/auth/methods", "get")["security"] == [
        {"DanteSessionCookie": []}
    ]
    assert _operation(document, "/api/v1/auth/provider-enrollment", "get")["security"] == [
        {"DanteProviderEnrollmentCookie": []}
    ]
    assert _operation(document, "/api/v1/auth/provider-link", "get")["security"] == [
        {"DanteProviderLinkCookie": []}
    ]
    assert _operation(document, "/api/v1/auth/provider-link/confirm", "post")["security"] == [
        {"DanteSessionCookie": [], "DanteProviderLinkCookie": []}
    ]

    for path in ("/api/v1/auth/google/begin", "/api/v1/auth/apple/begin"):
        operation = _operation(document, path, "post")
        assert operation["security"] == [{}, {"DanteSessionCookie": []}]
        browser = cast(dict[str, Any], operation["x-dante-browser-security"])
        assert browser["csrf_header"]["required_when"] == "purpose is link or reauthenticate"


def test_authenticated_m5_mutations_are_csrf_annotated() -> None:
    document = openapi_document()
    authenticated_mutations = (
        ("/api/v1/auth/password/establish", "post"),
        ("/api/v1/auth/password", "delete"),
        ("/api/v1/auth/provider-link/confirm", "post"),
        ("/api/v1/auth/providers/{external_identity_ref}", "delete"),
        ("/api/v1/auth/passkeys/registration/begin", "post"),
        ("/api/v1/auth/passkeys/registration/complete", "post"),
        ("/api/v1/auth/passkeys/reauthentication/begin", "post"),
        ("/api/v1/auth/passkeys/reauthentication/complete", "post"),
        ("/api/v1/auth/passkeys/{passkey_credential_ref}", "patch"),
        ("/api/v1/auth/passkeys/{passkey_credential_ref}", "delete"),
    )

    for path, method in authenticated_mutations:
        operation = _operation(document, path, method)
        browser = cast(dict[str, Any], operation["x-dante-browser-security"])
        assert browser["origin"] == {
            "owner": "browser",
            "required": True,
            "must_equal": "canonical_web_origin",
        }
        assert browser["sec_fetch_site"]["required_value"] == "same-origin"
        assert browser["client_header"]["required_value"] == "web"
        assert browser["csrf_header"] == {
            "owner": "web_transport",
            "name": "X-Dante-CSRF",
            "required": True,
        }


def test_apple_external_ingress_is_explicit_and_form_post_is_bounded() -> None:
    document = openapi_document()
    callback = _operation(document, "/api/v1/auth/apple/callback", "post")
    notification = _operation(document, "/api/v1/auth/apple/notifications", "post")

    callback_ingress = cast(dict[str, Any], callback["x-dante-external-ingress"])
    assert callback_ingress == {
        "browser_proof_exception": True,
        "required_media_type": "application/x-www-form-urlencoded",
        "authority": "server-side state verifier and provider proof",
    }
    request_body = cast(dict[str, Any], callback["requestBody"])
    content = cast(dict[str, Any], request_body["content"])
    form = cast(dict[str, Any], content["application/x-www-form-urlencoded"])
    schema = cast(dict[str, Any], form["schema"])
    assert schema["additionalProperties"] is False
    assert schema["required"] == ["state"]
    assert set(cast(dict[str, Any], schema["properties"])) == {
        "state",
        "code",
        "id_token",
        "user",
        "error",
    }

    assert notification["x-dante-external-ingress"] == {
        "browser_proof_exception": True,
        "required_media_type": "application/json",
        "authority": "Apple-signed notification JWS verification",
    }


def test_provider_success_discriminators_and_problem_media_type_are_governed() -> None:
    document = openapi_document()
    components = cast(dict[str, Any], document["components"])
    schemas = cast(dict[str, Any], components["schemas"])

    for schema_name in (
        "ProviderAuthenticatedResponse",
        "ProviderLinkRequiredResponse",
        "ProviderEnrollmentRequiredResponse",
    ):
        schema = cast(dict[str, Any], schemas[schema_name])
        assert "outcome" in cast(list[str], schema["required"])
    authenticated = cast(dict[str, Any], schemas["ProviderAuthenticatedResponse"])
    assert "authenticated" in cast(list[str], authenticated["required"])

    google_complete = _operation(document, "/api/v1/auth/google/complete", "post")
    problem = cast(dict[str, Any], cast(dict[str, Any], google_complete["responses"])["401"])
    assert "application/problem+json" in cast(dict[str, Any], problem["content"])


def test_all_m5_successes_advertise_no_store_and_request_id() -> None:
    document = openapi_document()
    for path, method in _EXPECTED_M5_OPERATIONS:
        operation = _operation(document, path, method)
        responses = cast(dict[str, Any], operation["responses"])
        success_status = next(status for status in responses if status.startswith(("2", "3")))
        success = cast(dict[str, Any], responses[success_status])
        headers = cast(dict[str, Any], success["headers"])
        assert cast(dict[str, Any], headers["Cache-Control"])["schema"] == {
            "type": "string",
            "const": "no-store",
        }
        assert "X-Request-ID" in headers
