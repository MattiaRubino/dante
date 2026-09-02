from __future__ import annotations

import importlib.util
import os
from collections.abc import Callable
from pathlib import Path
from types import ModuleType

import psycopg
from dante.platform.config.auth import AuthSettings
from dante.platform.config.auth_provider import (
    AuthProviderSettings,
    GoogleProviderSettings,
    WebAuthnSettings,
)
from psycopg import sql

_CORE_PATH = Path(__file__).with_name("serve-access-auth-stack.py")
_UAT_WEB_ORIGIN = "https://localhost:4173"
_GOOGLE_CLIENT_ID_ENV = "DANTE_UAT_GOOGLE_CLIENT_ID"
_ENABLE_GOOGLE_ENV = "DANTE_UAT_ENABLE_GOOGLE"
_ENABLE_WEBAUTHN_ENV = "DANTE_UAT_ENABLE_WEBAUTHN"
_ACCOUNT_EMAIL_ENV = "DANTE_UAT_ACCOUNT_EMAIL"
_TLS_CERT_ENV = "DANTE_UAT_TLS_CERT"
_TLS_KEY_ENV = "DANTE_UAT_TLS_KEY"
_TRUE_VALUES = frozenset({"1", "true", "yes", "on"})
_FALSE_VALUES = frozenset({"0", "false", "no", "off"})
_REQUIRED_EXTENSIONS: tuple[tuple[str, str | None], ...] = (
    ("postgis", "3.6.4"),
    ("vector", "0.8.6"),
    ("pg_trgm", None),
    ("unaccent", None),
    ("pg_stat_statements", None),
)


def _load_core() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "dante_access_auth_uat_core", _CORE_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load the Access/Auth full-stack harness core.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _enabled(name: str) -> bool:
    raw = os.environ.get(name, "false")
    value = raw.strip().casefold()
    if value in _TRUE_VALUES:
        return True
    if value in _FALSE_VALUES:
        return False
    raise RuntimeError(f"{name} must be one of true/false, 1/0, yes/no or on/off.")


def _google_client_id(*, enabled: bool) -> str | None:
    raw = os.environ.get(_GOOGLE_CLIENT_ID_ENV)
    if raw is None:
        if enabled:
            raise RuntimeError(
                f"{_GOOGLE_CLIENT_ID_ENV} is required when {_ENABLE_GOOGLE_ENV}=true."
            )
        return None

    if not raw or raw.strip() != raw or any(character in raw for character in "\r\n"):
        raise RuntimeError(f"{_GOOGLE_CLIENT_ID_ENV} must be non-blank and trimmed.")
    return raw


def _extension_guard(database_name: str) -> Callable[..., None]:
    def ensure_extensions(*, port: int, password: str) -> None:
        with psycopg.connect(
            host="127.0.0.1",
            port=port,
            dbname=database_name,
            user="postgres",
            password=password,
            autocommit=True,
        ) as connection:
            for extension_name, expected_version in _REQUIRED_EXTENSIONS:
                statement = sql.SQL("CREATE EXTENSION IF NOT EXISTS {}").format(
                    sql.Identifier(extension_name)
                )
                if expected_version is not None:
                    statement += sql.SQL(" VERSION {}").format(
                        sql.Literal(expected_version)
                    )
                connection.execute(statement)

                row = connection.execute(
                    "SELECT extversion FROM pg_extension WHERE extname = %s",
                    (extension_name,),
                ).fetchone()
                if row is None:
                    raise RuntimeError(
                        f"Required PostgreSQL extension is unavailable: {extension_name}"
                    )
                if expected_version is not None and row[0] != expected_version:
                    raise RuntimeError(
                        "PostgreSQL extension version mismatch: "
                        f"{extension_name} expected {expected_version}, got {row[0]}"
                    )

    return ensure_extensions


def _auth_settings_override(
    original: Callable[[str, int], AuthSettings],
    *,
    google_enabled: bool,
    google_client_id: str | None,
    webauthn_enabled: bool,
) -> Callable[[str, int], AuthSettings]:
    def build(hibp_base_url: str, smtp_port: int) -> AuthSettings:
        settings = original(hibp_base_url, smtp_port)
        provider = AuthProviderSettings(
            google=GoogleProviderSettings(
                enabled=google_enabled,
                client_id=google_client_id,
            ),
            webauthn=WebAuthnSettings(
                enabled=webauthn_enabled,
                rp_id="localhost",
                rp_name="DANTE",
                expected_origins=(_UAT_WEB_ORIGIN,),
            ),
        )
        return settings.model_copy(
            update={
                "canonical_web_origin": _UAT_WEB_ORIGIN,
                "provider": provider,
            }
        )

    return build


def _tls_material_override(core: ModuleType) -> Callable[[Path], tuple[Path, Path]]:
    def material(directory: Path) -> tuple[Path, Path]:
        cert_value = os.environ.get(_TLS_CERT_ENV)
        key_value = os.environ.get(_TLS_KEY_ENV)
        if (cert_value is None) != (key_value is None):
            raise RuntimeError(
                f"{_TLS_CERT_ENV} and {_TLS_KEY_ENV} must be supplied together."
            )
        if cert_value is not None and key_value is not None:
            cert_path = Path(cert_value).expanduser().resolve()
            key_path = Path(key_value).expanduser().resolve()
            if not cert_path.is_file():
                raise RuntimeError(f"UAT TLS certificate does not exist: {cert_path}")
            if not key_path.is_file():
                raise RuntimeError(f"UAT TLS key does not exist: {key_path}")
            return cert_path, key_path

        cert_path = directory / "dante-uat-cert.pem"
        key_path = directory / "dante-uat-key.pem"
        run = getattr(core, "_run", None)
        if not callable(run):
            raise RuntimeError("Access/Auth harness core does not expose its command runner.")
        run(
            [
                "openssl",
                "req",
                "-x509",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-keyout",
                str(key_path),
                "-out",
                str(cert_path),
                "-days",
                "1",
                "-subj",
                "/CN=localhost",
                "-addext",
                "subjectAltName=DNS:localhost,IP:127.0.0.1",
            ]
        )
        return cert_path, key_path

    return material


def _seed_email(core: ModuleType) -> str:
    configured = os.environ.get(_ACCOUNT_EMAIL_ENV)
    if configured is None:
        current = getattr(core, "_EMAIL", None)
        if not isinstance(current, str) or not current:
            raise RuntimeError("Access/Auth harness core does not expose its seed email.")
        return current
    if not configured or configured.strip() != configured:
        raise RuntimeError(f"{_ACCOUNT_EMAIL_ENV} must be non-blank and trimmed.")
    core._EMAIL = configured
    return configured


def main() -> None:
    core = _load_core()
    google_enabled = _enabled(_ENABLE_GOOGLE_ENV)
    webauthn_enabled = _enabled(_ENABLE_WEBAUTHN_ENV)
    if not google_enabled and not webauthn_enabled:
        raise RuntimeError(
            "Enable at least one real UAT surface with "
            f"{_ENABLE_GOOGLE_ENV}=true or {_ENABLE_WEBAUTHN_ENV}=true."
        )

    google_client_id = _google_client_id(enabled=google_enabled)
    if google_enabled:
        if google_client_id is None:
            raise RuntimeError("Google client ID validation lost enabled configuration.")
        os.environ["VITE_DANTE_GOOGLE_CLIENT_ID"] = google_client_id
    else:
        os.environ.pop("VITE_DANTE_GOOGLE_CLIENT_ID", None)

    database_name = getattr(core, "_DATABASE_NAME", None)
    if not isinstance(database_name, str) or not database_name:
        raise RuntimeError(
            "Access/Auth harness core does not expose its disposable database name."
        )

    core._WEB_ORIGIN = _UAT_WEB_ORIGIN
    core._create_extensions = _extension_guard(database_name)
    core._auth_settings = _auth_settings_override(
        core._auth_settings,
        google_enabled=google_enabled,
        google_client_id=google_client_id,
        webauthn_enabled=webauthn_enabled,
    )
    core._generate_tls_material = _tls_material_override(core)
    seed_email = _seed_email(core)
    seed_password = getattr(core, "_PASSWORD", None)
    if not isinstance(seed_password, str) or not seed_password:
        raise RuntimeError("Access/Auth harness core does not expose its seed password.")

    print("DANTE Access/Auth local real-UAT configuration")
    print(f"  origin          : {_UAT_WEB_ORIGIN}")
    print(f"  Google          : {'enabled' if google_enabled else 'disabled'}")
    print(f"  WebAuthn/passkey: {'enabled' if webauthn_enabled else 'disabled'}")
    print(f"  seeded email    : {seed_email}")
    print(f"  seeded password : {seed_password}")
    if os.environ.get(_TLS_CERT_ENV) is None:
        print(
            "  TLS             : ephemeral self-signed localhost certificate; "
            "use DANTE_UAT_TLS_CERT/DANTE_UAT_TLS_KEY for a locally trusted certificate"
        )
    else:
        print("  TLS             : caller-supplied certificate/key")
    print("  database        : disposable PostgreSQL 18.6; Ctrl-C destroys this UAT state")

    core.main()


if __name__ == "__main__":
    main()
