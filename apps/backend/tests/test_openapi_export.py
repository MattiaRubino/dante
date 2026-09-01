from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from dante.bootstrap.openapi_export import openapi_document, render_openapi


def test_committed_openapi_snapshot_matches_governed_export() -> None:
    """Fail CI when backend contract changes without regenerating the client source."""
    repo_root = Path(__file__).resolve().parents[3]
    snapshot_path = repo_root / "packages" / "api-client" / "openapi" / "dante-v1.openapi.json"

    committed = json.loads(snapshot_path.read_text(encoding="utf-8"))

    assert committed == openapi_document()


def test_openapi_render_is_byte_deterministic() -> None:
    """Two fresh exports must be byte-identical, not merely schema-equivalent."""
    assert render_openapi() == render_openapi()


def test_m5_password_and_method_contract_is_frozen_and_security_annotated() -> None:
    document = openapi_document()
    paths = cast(dict[str, Any], document["paths"])

    methods = cast(dict[str, Any], cast(dict[str, Any], paths["/api/v1/auth/methods"])["get"])
    establish = cast(
        dict[str, Any],
        cast(dict[str, Any], paths["/api/v1/auth/password/establish"])["post"],
    )
    remove = cast(dict[str, Any], cast(dict[str, Any], paths["/api/v1/auth/password"])["delete"])

    assert methods["operationId"] == "auth_get_authentication_methods"
    assert establish["operationId"] == "auth_establish_password"
    assert remove["operationId"] == "auth_remove_password"

    assert methods["security"] == [{"DanteSessionCookie": []}]
    for operation in (establish, remove):
        assert operation["security"] == [{"DanteSessionCookie": []}]
        browser_security = cast(dict[str, Any], operation["x-dante-browser-security"])
        assert browser_security["origin"] == {
            "owner": "browser",
            "required": True,
            "must_equal": "canonical_web_origin",
        }
        assert browser_security["sec_fetch_site"] == {
            "owner": "browser",
            "required": True,
            "required_value": "same-origin",
        }
        assert browser_security["client_header"] == {
            "owner": "web_transport",
            "name": "X-Dante-Client",
            "required": True,
            "required_value": "web",
        }
        assert browser_security["csrf_header"] == {
            "owner": "web_transport",
            "name": "X-Dante-CSRF",
            "required": True,
        }

        success = cast(dict[str, Any], cast(dict[str, Any], operation["responses"])["200"])
        headers = cast(dict[str, Any], success["headers"])
        assert cast(dict[str, Any], headers["Cache-Control"])["schema"] == {
            "type": "string",
            "const": "no-store",
        }
        assert "X-Request-ID" in headers
        assert "Set-Cookie" in headers
