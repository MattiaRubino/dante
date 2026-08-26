"""Executable contract tests for DANTE bootstrap settings."""

from pathlib import Path

import pytest
from pydantic import SecretStr, ValidationError

from dante.platform.config.database import DatabaseSettings
from dante.platform.config.settings import Environment, Settings

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
)


def _database_settings() -> DatabaseSettings:
    return DatabaseSettings(
        host="127.0.0.1",
        port=5432,
        name="dante",
        user="dante_runtime",
        password=SecretStr("test-runtime-secret"),
    )


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


def test_explicit_settings_are_valid_for_application_injection() -> None:
    settings = Settings(
        env=Environment.DEV,
        release_sha="abcdef123456",
        build_id="build-42",
        debug=False,
        database=_database_settings(),
    )

    assert settings.env is Environment.DEV
    assert settings.release_sha == "abcdef123456"
    assert settings.build_id == "build-42"
    assert settings.database.user == "dante_runtime"


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
        )


def test_settings_are_immutable_after_bootstrap() -> None:
    settings = Settings(
        env=Environment.LOCAL,
        release_sha="local",
        build_id="local",
        debug=False,
        database=_database_settings(),
    )

    with pytest.raises(ValidationError, match="frozen"):
        settings.debug = True  # type: ignore[misc]  # deliberate runtime immutability probe


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
        "DANTE_DATABASE__PASSWORD=dotenv-secret\n",
        encoding="utf-8",
    )

    with pytest.raises(ValidationError, match="env"):
        Settings()
