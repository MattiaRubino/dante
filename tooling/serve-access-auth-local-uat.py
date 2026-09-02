from __future__ import annotations

import importlib.util
import logging
import os
from collections.abc import Callable
from pathlib import Path
from types import ModuleType

import psycopg
from dante.platform.config.auth import AuthSettings, SmtpSecurity
from dante.platform.config.auth_provider import (
    AuthProviderSettings,
    GoogleProviderSettings,
    WebAuthnSettings,
)
from psycopg import sql
from pydantic import SecretStr

_CORE_PATH = Path(__file__).with_name("serve-access-auth-stack.py")
_UAT_WEB_ORIGIN = "https://localhost:4173"
_GOOGLE_CLIENT_ID_ENV = "DANTE_UAT_GOOGLE_CLIENT_ID"
_ENABLE_GOOGLE_ENV = "DANTE_UAT_ENABLE_GOOGLE"
_ENABLE_WEBAUTHN_ENV = "DANTE_UAT_ENABLE_WEBAUTHN"
_ENABLE_REAL_SMTP_ENV = "DANTE_UAT_ENABLE_REAL_SMTP"
_SMTP_HOST_ENV = "DANTE_UAT_SMTP_HOST"
_SMTP_PORT_ENV = "DANTE_UAT_SMTP_PORT"
_SMTP_SECURITY_ENV = "DANTE_UAT_SMTP_SECURITY"
_SMTP_USERNAME_ENV = "DANTE_UAT_SMTP_USERNAME"
_SMTP_PASSWORD_ENV = "DANTE_UAT_SMTP_PASSWORD"
_SMTP_FROM_ADDRESS_ENV = "DANTE_UAT_SMTP_FROM_ADDRESS"
_ACCOUNT_EMAIL_ENV = "DANTE_UAT_ACCOUNT_EMAIL"
_TLS_CERT_ENV = "DANTE_UAT_TLS_CERT"
_TLS_KEY_ENV = "DANTE_UAT_TLS_KEY"
_TRUE_VALUES = frozenset({"1", "true", "yes", "on"})
_FALSE_VALUES = frozenset({"0", "false", "no", "off"})
_REAL_SMTP_ENV_NAMES = (
    _SMTP_HOST_ENV,
    _SMTP_PORT_ENV,
    _SMTP_SECURITY_ENV,
    _SMTP_USERNAME_ENV,
    _SMTP_PASSWORD_ENV,
    _SMTP_FROM_ADDRESS_ENV,
)
_REQUIRED_EXTENSIONS: tuple[tuple[str, str | None], ...] = (
    ("postgis", "3.6.4"),
    ("vector", "0.8.6"),
    ("pg_trgm", None),
    ("unaccent", None),
    ("pg_stat_statements", None),
)
_LOGGER = logging.getLogger("dante.access_auth_uat")


def _load_core() -> ModuleType:
    spec = importlib.util.spec_from_file_location("dante_access_auth_uat_core", _CORE_PATH)
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


def _required_trimmed_env(name: str) -> str:
    raw = os.environ.get(name)
    if raw is None or not raw or raw.strip() != raw or any(
        character in raw for character in "\r\n"
    ):
        raise RuntimeError(f"{name} must be non-blank, trimmed and single-line.")
    return raw


def _real_smtp_overrides(*, enabled: bool) -> dict[str, object]:
    configured = tuple(name for name in _REAL_SMTP_ENV_NAMES if name in os.environ)
    if not enabled:
        if configured:
            raise RuntimeError(
                "Real SMTP settings were supplied without explicit opt-in. Set "
                f"{_ENABLE_REAL_SMTP_ENV}=true or remove: {', '.join(configured)}."
            )
        return {}

    host = _required_trimmed_env(_SMTP_HOST_ENV)
    from_address = _required_trimmed_env(_SMTP_FROM_ADDRESS_ENV)

    port_raw = os.environ.get(_SMTP_PORT_ENV, "587")
    try:
        port = int(port_raw)
    except ValueError as exc:
        raise RuntimeError(f"{_SMTP_PORT_ENV} must be an integer TCP port.") from exc
    if not 1 <= port <= 65_535:
        raise RuntimeError(f"{_SMTP_PORT_ENV} must be within 1..65535.")

    security_raw = os.environ.get(_SMTP_SECURITY_ENV, SmtpSecurity.STARTTLS.value)
    try:
        security = SmtpSecurity(security_raw.strip().casefold())
    except ValueError as exc:
        supported = ", ".join(mode.value for mode in SmtpSecurity)
        raise RuntimeError(
            f"{_SMTP_SECURITY_ENV} must be one of: {supported}."
        ) from exc

    username_raw = os.environ.get(_SMTP_USERNAME_ENV)
    password_raw = os.environ.get(_SMTP_PASSWORD_ENV)
    if (username_raw is None) != (password_raw is None):
        raise RuntimeError(
            f"{_SMTP_USERNAME_ENV} and {_SMTP_PASSWORD_ENV} must be supplied together."
        )

    username: str | None = None
    password: SecretStr | None = None
    if username_raw is not None and password_raw is not None:
        username = _required_trimmed_env(_SMTP_USERNAME_ENV)
        if not password_raw or any(character in password_raw for character in "\r\n"):
            raise RuntimeError(
                f"{_SMTP_PASSWORD_ENV} must be non-blank and single-line."
            )
        password = SecretStr(password_raw)

    return {
        "smtp_host": host,
        "smtp_port": port,
        "smtp_security": security,
        "smtp_username": username,
        "smtp_password": password,
        "smtp_from_address": from_address,
        "smtp_timeout_seconds": 10.0,
    }


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
                    statement += sql.SQL(" VERSION {}").format(sql.Literal(expected_version))
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
    smtp_overrides: dict[str, object],
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
        payload = settings.model_dump(mode="python")
        payload.update(
            {
                "canonical_web_origin": _UAT_WEB_ORIGIN,
                "provider": provider,
                **smtp_overrides,
            }
        )
        return AuthSettings.model_validate(payload)

    return build


def _tls_material_override(core: ModuleType) -> Callable[[Path], tuple[Path, Path]]:
    def material(directory: Path) -> tuple[Path, Path]:
        cert_value = os.environ.get(_TLS_CERT_ENV)
        key_value = os.environ.get(_TLS_KEY_ENV)
        if (cert_value is None) != (key_value is None):
            raise RuntimeError(f"{_TLS_CERT_ENV} and {_TLS_KEY_ENV} must be supplied together.")
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


def _log_configuration(
    *,
    google_enabled: bool,
    webauthn_enabled: bool,
    seed_email: str,
    seed_password: str,
    smtp_overrides: dict[str, object],
) -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    _LOGGER.info("DANTE Access/Auth local real-UAT configuration")
    _LOGGER.info("  origin          : %s", _UAT_WEB_ORIGIN)
    _LOGGER.info("  Google          : %s", "enabled" if google_enabled else "disabled")
    _LOGGER.info("  Apple           : disabled (registered-domain UAT only)")
    _LOGGER.info("  WebAuthn/passkey: %s", "enabled" if webauthn_enabled else "disabled")
    if smtp_overrides:
        _LOGGER.info(
            "  email transport : real SMTP %s:%s (%s)",
            smtp_overrides["smtp_host"],
            smtp_overrides["smtp_port"],
            smtp_overrides["smtp_security"],
        )
    else:
        _LOGGER.info("  email transport : loopback SMTP capture")
    _LOGGER.info("  seeded email    : %s", seed_email)
    _LOGGER.info("  seeded password : %s", seed_password)
    if os.environ.get(_TLS_CERT_ENV) is None:
        _LOGGER.info(
            "  TLS             : ephemeral self-signed localhost certificate; "
            "use DANTE_UAT_TLS_CERT/DANTE_UAT_TLS_KEY for a locally trusted certificate"
        )
    else:
        _LOGGER.info("  TLS             : caller-supplied certificate/key")
    _LOGGER.info("  database        : disposable PostgreSQL 18.6; Ctrl-C destroys this UAT state")


def main() -> None:
    core = _load_core()
    google_enabled = _enabled(_ENABLE_GOOGLE_ENV)
    webauthn_enabled = _enabled(_ENABLE_WEBAUTHN_ENV)
    real_smtp_enabled = _enabled(_ENABLE_REAL_SMTP_ENV)
    if not google_enabled and not webauthn_enabled and not real_smtp_enabled:
        raise RuntimeError(
            "Enable at least one real UAT surface with "
            f"{_ENABLE_GOOGLE_ENV}=true, {_ENABLE_WEBAUTHN_ENV}=true or "
            f"{_ENABLE_REAL_SMTP_ENV}=true."
        )

    google_client_id = _google_client_id(enabled=google_enabled)
    smtp_overrides = _real_smtp_overrides(enabled=real_smtp_enabled)
    if google_enabled:
        if google_client_id is None:
            raise RuntimeError("Google client ID validation lost enabled configuration.")
        os.environ["VITE_DANTE_GOOGLE_CLIENT_ID"] = google_client_id
    else:
        os.environ.pop("VITE_DANTE_GOOGLE_CLIENT_ID", None)
    os.environ["VITE_DANTE_APPLE_ENABLED"] = "false"
    os.environ["VITE_DANTE_PASSKEY_ENABLED"] = "true" if webauthn_enabled else "false"

    database_name = getattr(core, "_DATABASE_NAME", None)
    if not isinstance(database_name, str) or not database_name:
        raise RuntimeError("Access/Auth harness core does not expose its disposable database name.")

    core._WEB_ORIGIN = _UAT_WEB_ORIGIN
    core._create_extensions = _extension_guard(database_name)
    core._auth_settings = _auth_settings_override(
        core._auth_settings,
        google_enabled=google_enabled,
        google_client_id=google_client_id,
        webauthn_enabled=webauthn_enabled,
        smtp_overrides=smtp_overrides,
    )
    core._generate_tls_material = _tls_material_override(core)
    seed_email = _seed_email(core)
    seed_password = getattr(core, "_PASSWORD", None)
    if not isinstance(seed_password, str) or not seed_password:
        raise RuntimeError("Access/Auth harness core does not expose its seed password.")

    _log_configuration(
        google_enabled=google_enabled,
        webauthn_enabled=webauthn_enabled,
        seed_email=seed_email,
        seed_password=seed_password,
        smtp_overrides=smtp_overrides,
    )
    core.main()


if __name__ == "__main__":
    main()
