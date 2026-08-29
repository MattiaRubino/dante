"""Executable contract tests for DANTE bootstrap settings."""

from base64 import urlsafe_b64encode
from pathlib import Path

import pytest
from pydantic import SecretStr, ValidationError

from dante.platform.config.auth import AuthSettings, SmtpSecurity
from dante.platform.config.database import DatabaseSettings
from dante.platform.config.settings import Environment, Settings

_TEST_PEPPER_KEY_ID = "test-password-v1"
_TEST_OTP_KEY_ID = "test-signup-otp-v1"
_MISSING_PEPPER_KEY_ID = "missing"


def _secret(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


_TEST_PEPPER = _secret(b"p" * 32)
_TEST_CSRF_KEY = _secret(b"c" * 32)
_TEST_OTP_KEY = _secret(b"o" * 32)

_DANTE_ENVIRONMENT_VARIABLES = (
    "DANTE_ENV",
    "DANTE_RELEASE_SHA",
    "DANTE_BUILD_ID",
    "DANTE_DEBUG",
    "DANTE_DATABASE__HOST",
    "DANTE_DATABASE__PORT",
    "DANTE_DATABASE__NAME",
    "DANTE_DATABASE__USER",
    "DANTE_DATABASE__PASSWORD",
    "DANTE_DATABASE__CONNECT_TIMEOUT_SECONDS",
    "DANTE_DATABASE__POOL_SIZE",
    "DANTE_DATABASE__MAX_OVERFLOW",
    "DANTE_DATABASE__POOL_TIMEOUT_SECONDS",
    "DANTE_DATABASE__READINESS_TIMEOUT_SECONDS",
    "DANTE_AUTH__CANONICAL_WEB_ORIGIN",
    "DANTE_AUTH__PASSWORD_CURRENT_PEPPER_KEY_ID",
    "DANTE_AUTH__PASSWORD_PEPPERS",
    "DANTE_AUTH__CSRF_KEY",
    "DANTE_AUTH__SIGNUP_OTP_CURRENT_KEY_ID",
    "DANTE_AUTH__SIGNUP_OTP_KEYS",
    "DANTE_AUTH__SMTP_HOST",
    "DANTE_AUTH__SMTP_PORT",
    "DANTE_AUTH__SMTP_SECURITY",
    "DANTE_AUTH__SMTP_USERNAME",
    "DANTE_AUTH__SMTP_PASSWORD",
    "DANTE_AUTH__SMTP_FROM_ADDRESS",
    "DANTE_AUTH__SMTP_TIMEOUT_SECONDS",
    "DANTE_AUTH__EMAIL_QUEUE_CAPACITY",
    "DANTE_AUTH__EMAIL_WORKER_COUNT",
    "DANTE_AUTH__EMAIL_SHUTDOWN_DRAIN_SECONDS",
    "DANTE_AUTH__SESSION_MAX_AGE_SECONDS",
    "DANTE_AUTH__SESSION_IDLE_TIMEOUT_SECONDS",
    "DANTE_AUTH__RECENT_AUTH_WINDOW_SECONDS",
    "DANTE_AUTH__SIGNUP_LIFETIME_SECONDS",
    "DANTE_AUTH__SIGNUP_OTP_LIFETIME_SECONDS",
    "DANTE_AUTH__SIGNUP_RESEND_COOLDOWN_SECONDS",
    "DANTE_AUTH__RECOVERY_LIFETIME_SECONDS",
    "DANTE_AUTH__RECOVERY_RESPONSE_FLOOR_SECONDS",
    "DANTE_AUTH__KDF_MAX_CONCURRENCY",
    "DANTE_AUTH__KDF_MAX_QUEUE_DEPTH",
    "DANTE_AUTH__KDF_QUEUE_TIMEOUT_SECONDS",
    "DANTE_AUTH__SIGNIN_RATE_CAPACITY",
    "DANTE_AUTH__SIGNIN_RATE_WINDOW_SECONDS",
    "DANTE_AUTH__SIGNIN_RATE_MAX_KEYS",
    "DANTE_AUTH__SIGNUP_RATE_CAPACITY",
    "DANTE_AUTH__SIGNUP_RATE_WINDOW_SECONDS",
    "DANTE_AUTH__SIGNUP_SOURCE_RATE_CAPACITY",
    "DANTE_AUTH__SIGNUP_SOURCE_RATE_WINDOW_SECONDS",
    "DANTE_AUTH__RECOVERY_RATE_CAPACITY",
    "DANTE_AUTH__RECOVERY_RATE_WINDOW_SECONDS",
    "DANTE_AUTH__RECOVERY_SOURCE_RATE_CAPACITY",
    "DANTE_AUTH__RECOVERY_SOURCE_RATE_WINDOW_SECONDS",
    "DANTE_AUTH__REAUTH_RATE_CAPACITY",
    "DANTE_AUTH__REAUTH_RATE_WINDOW_SECONDS",
    "DANTE_AUTH__LIFECYCLE_RATE_MAX_KEYS",
    "DANTE_AUTH__HIBP_BASE_URL",
    "DANTE_AUTH__HIBP_TIMEOUT_SECONDS",
    "DANTE_AUTH__HIBP_MAX_RESPONSE_BYTES",
    "DANTE_AUTH__HIBP_MAX_CONNECTIONS",
)


def _database_settings() -> DatabaseSettings:
    return DatabaseSettings(
        host="127.0.0.1",
        port=5432,
        name="dante",
        user="dante_runtime",
        password=SecretStr("test-runtime-secret"),
    )


def _auth_settings(
    *,
    canonical_web_origin: str = "https://dante.test",
    hibp_base_url: str = "https://api.pwnedpasswords.com",
    smtp_security: SmtpSecurity = SmtpSecurity.STARTTLS,
) -> AuthSettings:
    return AuthSettings(
        canonical_web_origin=canonical_web_origin,
        password_current_pepper_key_id=_TEST_PEPPER_KEY_ID,
        password_peppers={_TEST_PEPPER_KEY_ID: SecretStr(_TEST_PEPPER)},
        csrf_key=SecretStr(_TEST_CSRF_KEY),
        signup_otp_current_key_id=_TEST_OTP_KEY_ID,
        signup_otp_keys={_TEST_OTP_KEY_ID: SecretStr(_TEST_OTP_KEY)},
        smtp_host="smtp.dante.test",
        smtp_port=587,
        smtp_security=smtp_security,
        smtp_from_address="no-reply@dante.test",
        kdf_max_concurrency=2,
        kdf_max_queue_depth=4,
        signin_rate_capacity=10,
        signin_rate_window_seconds=60,
        hibp_base_url=hibp_base_url,
    )


def _required_m4_auth_kwargs() -> dict[str, object]:
    return {
        "signup_otp_current_key_id": _TEST_OTP_KEY_ID,
        "signup_otp_keys": {_TEST_OTP_KEY_ID: SecretStr(_TEST_OTP_KEY)},
        "smtp_host": "smtp.dante.test",
        "smtp_from_address": "no-reply@dante.test",
    }


def _clear_dante_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    for variable_name in _DANTE_ENVIRONMENT_VARIABLES:
        monkeypatch.delenv(variable_name, raising=False)


def _set_valid_local_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_dante_environment(monkeypatch)
    monkeypatch.setenv("DANTE_ENV", "local")
    monkeypatch.setenv("DANTE_RELEASE_SHA", "local")
    monkeypatch.setenv("DANTE_BUILD_ID", "local")
    monkeypatch.setenv("DANTE_DEBUG", "false")
    monkeypatch.setenv("DANTE_DATABASE__HOST", "127.0.0.1")
    monkeypatch.setenv("DANTE_DATABASE__NAME", "dante")
    monkeypatch.setenv("DANTE_DATABASE__USER", "dante_runtime")
    monkeypatch.setenv("DANTE_DATABASE__PASSWORD", "test-runtime-secret")
    monkeypatch.setenv("DANTE_AUTH__CANONICAL_WEB_ORIGIN", "https://dante.test")
    monkeypatch.setenv("DANTE_AUTH__PASSWORD_CURRENT_PEPPER_KEY_ID", _TEST_PEPPER_KEY_ID)
    monkeypatch.setenv(
        "DANTE_AUTH__PASSWORD_PEPPERS",
        '{"test-password-v1":"' + _TEST_PEPPER + '"}',
    )
    monkeypatch.setenv("DANTE_AUTH__CSRF_KEY", _TEST_CSRF_KEY)
    monkeypatch.setenv("DANTE_AUTH__SIGNUP_OTP_CURRENT_KEY_ID", _TEST_OTP_KEY_ID)
    monkeypatch.setenv(
        "DANTE_AUTH__SIGNUP_OTP_KEYS",
        '{"test-signup-otp-v1":"' + _TEST_OTP_KEY + '"}',
    )
    monkeypatch.setenv("DANTE_AUTH__SMTP_HOST", "127.0.0.1")
    monkeypatch.setenv("DANTE_AUTH__SMTP_PORT", "1025")
    monkeypatch.setenv("DANTE_AUTH__SMTP_SECURITY", "plain")
    monkeypatch.setenv("DANTE_AUTH__SMTP_FROM_ADDRESS", "no-reply@dante.test")
    monkeypatch.setenv("DANTE_AUTH__KDF_MAX_CONCURRENCY", "2")
    monkeypatch.setenv("DANTE_AUTH__KDF_MAX_QUEUE_DEPTH", "4")
    monkeypatch.setenv("DANTE_AUTH__SIGNIN_RATE_CAPACITY", "10")
    monkeypatch.setenv("DANTE_AUTH__SIGNIN_RATE_WINDOW_SECONDS", "60")


def test_valid_local_environment_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_valid_local_environment(monkeypatch)

    settings = Settings()

    assert settings.env is Environment.LOCAL
    assert settings.release_sha == "local"
    assert settings.build_id == "local"
    assert settings.debug is False
    assert settings.database.host == "127.0.0.1"
    assert settings.database.port == 5432
    assert settings.database.name == "dante"
    assert settings.database.user == "dante_runtime"
    assert settings.database.connect_timeout_seconds == 5
    assert settings.database.pool_size == 5
    assert settings.database.max_overflow == 10
    assert settings.database.pool_timeout_seconds == 30.0
    assert settings.database.readiness_timeout_seconds == 2.0
    assert settings.auth.canonical_web_origin == "https://dante.test"
    assert settings.auth.kdf_max_concurrency == 2
    assert settings.auth.kdf_max_queue_depth == 4
    assert settings.auth.session_max_age_seconds == 2_592_000
    assert settings.auth.recent_auth_window_seconds == 600
    assert settings.auth.smtp_security is SmtpSecurity.PLAIN
    assert settings.auth.password_pepper_bytes[_TEST_PEPPER_KEY_ID] == b"p" * 32
    assert settings.auth.signup_otp_key_bytes[_TEST_OTP_KEY_ID] == b"o" * 32
    assert settings.auth.csrf_key_bytes == b"c" * 32


def test_explicit_settings_are_valid_for_application_injection() -> None:
    settings = Settings(
        env=Environment.DEV,
        release_sha="abcdef123456",
        build_id="build-42",
        debug=False,
        database=_database_settings(),
        auth=_auth_settings(),
    )

    assert settings.env is Environment.DEV
    assert settings.release_sha == "abcdef123456"
    assert settings.build_id == "build-42"
    assert settings.database.user == "dante_runtime"
    assert settings.auth.password_current_pepper_key_id == _TEST_PEPPER_KEY_ID


@pytest.mark.parametrize(
    "invalid_user",
    ["postgres", "dante_owner", "dante_migrator", "custom_runtime"],
)
def test_runtime_database_identity_is_fixed_to_dante_runtime(invalid_user: str) -> None:
    with pytest.raises(ValidationError, match="dante_runtime"):
        DatabaseSettings(
            host="127.0.0.1",
            port=5432,
            name="dante",
            user=invalid_user,  # type: ignore[arg-type]
            password=SecretStr("test-runtime-secret"),
        )


def test_environment_rejects_non_runtime_database_identity(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_valid_local_environment(monkeypatch)
    monkeypatch.setenv("DANTE_DATABASE__USER", "dante_migrator")

    with pytest.raises(ValidationError, match=r"database.*user|dante_runtime"):
        Settings()


def test_missing_auth_secret_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_valid_local_environment(monkeypatch)
    monkeypatch.delenv("DANTE_AUTH__CSRF_KEY")

    with pytest.raises(ValidationError, match=r"auth.*csrf_key|csrf_key"):
        Settings()


def test_missing_signup_otp_secret_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_valid_local_environment(monkeypatch)
    monkeypatch.delenv("DANTE_AUTH__SIGNUP_OTP_KEYS")

    with pytest.raises(ValidationError, match=r"auth.*signup_otp_keys|signup_otp_keys"):
        Settings()


def test_auth_secrets_are_redacted(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_valid_local_environment(monkeypatch)

    settings = Settings()
    rendered = repr(settings)

    assert _TEST_PEPPER not in rendered
    assert _TEST_CSRF_KEY not in rendered
    assert _TEST_OTP_KEY not in rendered
    assert str(settings.auth.csrf_key) == "**********"


def test_unknown_current_pepper_key_is_rejected() -> None:
    with pytest.raises(ValidationError, match="password_current_pepper_key_id"):
        AuthSettings(
            canonical_web_origin="https://dante.test",
            password_current_pepper_key_id=_MISSING_PEPPER_KEY_ID,
            password_peppers={"v1": SecretStr(_TEST_PEPPER)},
            csrf_key=SecretStr(_TEST_CSRF_KEY),
            kdf_max_concurrency=1,
            signin_rate_capacity=10,
            signin_rate_window_seconds=60,
            **_required_m4_auth_kwargs(),
        )


@pytest.mark.parametrize(
    "bad_secret",
    [
        _secret(b"x" * 31),
        _TEST_PEPPER + "=",
        _secret(b"\xfb" * 32).replace("-", "+").replace("_", "/"),
    ],
)
def test_password_pepper_requires_exact_canonical_32_byte_base64url(
    bad_secret: str,
) -> None:
    with pytest.raises(ValidationError, match=r"password_peppers|Base64URL|32 bytes"):
        AuthSettings(
            canonical_web_origin="https://dante.test",
            password_current_pepper_key_id=_TEST_PEPPER_KEY_ID,
            password_peppers={_TEST_PEPPER_KEY_ID: SecretStr(bad_secret)},
            csrf_key=SecretStr(_TEST_CSRF_KEY),
            kdf_max_concurrency=1,
            signin_rate_capacity=10,
            signin_rate_window_seconds=60,
            **_required_m4_auth_kwargs(),
        )


def test_auth_keys_require_cross_purpose_separation() -> None:
    with pytest.raises(ValidationError, match="distinct"):
        AuthSettings(
            canonical_web_origin="https://dante.test",
            password_current_pepper_key_id=_TEST_PEPPER_KEY_ID,
            password_peppers={_TEST_PEPPER_KEY_ID: SecretStr(_TEST_PEPPER)},
            csrf_key=SecretStr(_TEST_CSRF_KEY),
            signup_otp_current_key_id=_TEST_OTP_KEY_ID,
            signup_otp_keys={_TEST_OTP_KEY_ID: SecretStr(_TEST_PEPPER)},
            smtp_host="smtp.dante.test",
            smtp_from_address="no-reply@dante.test",
            kdf_max_concurrency=1,
            signin_rate_capacity=10,
            signin_rate_window_seconds=60,
        )


def test_auth_origin_normalizes_case_and_default_https_port() -> None:
    settings = _auth_settings(canonical_web_origin="HTTPS://DANTE.TEST:443/")

    assert settings.canonical_web_origin == "https://dante.test"


def test_remote_environment_requires_https_auth_boundaries() -> None:
    with pytest.raises(ValidationError, match="HTTPS"):
        Settings(
            env=Environment.PROD,
            release_sha="abcdef123456",
            build_id="build-42",
            debug=False,
            database=_database_settings(),
            auth=_auth_settings(canonical_web_origin="http://dante.test"),
        )


def test_remote_environment_rejects_plain_smtp() -> None:
    with pytest.raises(ValidationError, match="SMTP"):
        Settings(
            env=Environment.PROD,
            release_sha="abcdef123456",
            build_id="build-42",
            debug=False,
            database=_database_settings(),
            auth=_auth_settings(smtp_security=SmtpSecurity.PLAIN),
        )


def test_missing_environment_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_valid_local_environment(monkeypatch)
    monkeypatch.delenv("DANTE_ENV")

    with pytest.raises(ValidationError, match="env"):
        Settings()


def test_unknown_environment_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_valid_local_environment(monkeypatch)
    monkeypatch.setenv("DANTE_ENV", "staging")

    with pytest.raises(ValidationError, match="env"):
        Settings()


@pytest.mark.parametrize("variable_name", ["DANTE_RELEASE_SHA", "DANTE_BUILD_ID"])
def test_missing_identity_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
    variable_name: str,
) -> None:
    _set_valid_local_environment(monkeypatch)
    monkeypatch.delenv(variable_name)

    with pytest.raises(ValidationError, match=r"release_sha|build_id"):
        Settings()


@pytest.mark.parametrize("variable_name", ["DANTE_RELEASE_SHA", "DANTE_BUILD_ID"])
def test_blank_identity_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
    variable_name: str,
) -> None:
    _set_valid_local_environment(monkeypatch)
    monkeypatch.setenv(variable_name, "   ")

    with pytest.raises(ValidationError, match=r"release_sha|build_id"):
        Settings()


def test_missing_database_password_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_valid_local_environment(monkeypatch)
    monkeypatch.delenv("DANTE_DATABASE__PASSWORD")

    with pytest.raises(ValidationError, match=r"database.*password|password"):
        Settings()


def test_database_secret_is_redacted_in_configuration_repr(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_valid_local_environment(monkeypatch)

    settings = Settings()

    assert "test-runtime-secret" not in repr(settings)
    assert "test-runtime-secret" not in repr(settings.database)
    assert str(settings.database.password) == "**********"


def test_production_debug_is_rejected() -> None:
    with pytest.raises(ValidationError, match="DANTE_DEBUG"):
        Settings(
            env=Environment.PROD,
            release_sha="abcdef123456",
            build_id="build-42",
            debug=True,
            database=_database_settings(),
            auth=_auth_settings(),
        )


@pytest.mark.parametrize("env", [Environment.DEV, Environment.UAT, Environment.PROD])
@pytest.mark.parametrize(
    ("release_sha", "build_id"),
    [
        ("local", "build-42"),
        ("abcdef123456", "local"),
    ],
)
def test_remote_environments_reject_local_identity_markers(
    env: Environment,
    release_sha: str,
    build_id: str,
) -> None:
    with pytest.raises(ValidationError, match=r"DANTE_(RELEASE_SHA|BUILD_ID)"):
        Settings(
            env=env,
            release_sha=release_sha,
            build_id=build_id,
            debug=False,
            database=_database_settings(),
            auth=_auth_settings(),
        )


def test_settings_are_immutable_after_bootstrap() -> None:
    settings = Settings(
        env=Environment.LOCAL,
        release_sha="local",
        build_id="local",
        debug=False,
        database=_database_settings(),
        auth=_auth_settings(smtp_security=SmtpSecurity.PLAIN),
    )

    with pytest.raises(ValidationError, match="frozen"):
        settings.debug = True  # type: ignore[misc]


def test_dotenv_local_is_not_loaded_implicitly(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _clear_dante_environment(monkeypatch)
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env.local").write_text(
        "DANTE_ENV=local\n"
        "DANTE_RELEASE_SHA=local\n"
        "DANTE_BUILD_ID=local\n"
        "DANTE_DEBUG=false\n"
        "DANTE_DATABASE__HOST=127.0.0.1\n"
        "DANTE_DATABASE__NAME=dante\n"
        "DANTE_DATABASE__USER=dante_runtime\n"
        "DANTE_DATABASE__PASSWORD=dotenv-secret\n"
        "DANTE_AUTH__CANONICAL_WEB_ORIGIN=https://dante.test\n"
        "DANTE_AUTH__PASSWORD_CURRENT_PEPPER_KEY_ID=test-password-v1\n"
        'DANTE_AUTH__PASSWORD_PEPPERS={"test-password-v1":"' + _TEST_PEPPER + '"}\n'
        "DANTE_AUTH__CSRF_KEY=" + _TEST_CSRF_KEY + "\n"
        "DANTE_AUTH__SIGNUP_OTP_CURRENT_KEY_ID=test-signup-otp-v1\n"
        'DANTE_AUTH__SIGNUP_OTP_KEYS={"test-signup-otp-v1":"' + _TEST_OTP_KEY + '"}\n'
        "DANTE_AUTH__SMTP_HOST=127.0.0.1\n"
        "DANTE_AUTH__SMTP_PORT=1025\n"
        "DANTE_AUTH__SMTP_SECURITY=plain\n"
        "DANTE_AUTH__SMTP_FROM_ADDRESS=no-reply@dante.test\n"
        "DANTE_AUTH__KDF_MAX_CONCURRENCY=2\n"
        "DANTE_AUTH__KDF_MAX_QUEUE_DEPTH=4\n"
        "DANTE_AUTH__SIGNIN_RATE_CAPACITY=10\n"
        "DANTE_AUTH__SIGNIN_RATE_WINDOW_SECONDS=60\n",
        encoding="utf-8",
    )

    with pytest.raises(ValidationError, match="env"):
        Settings()
