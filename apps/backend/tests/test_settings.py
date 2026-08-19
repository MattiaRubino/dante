"""Executable contract tests for DANTE bootstrap settings."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from dante.platform.config.settings import Environment, Settings

_DANTE_ENVIRONMENT_VARIABLES = (
    "DANTE_ENV",
    "DANTE_RELEASE_SHA",
    "DANTE_BUILD_ID",
    "DANTE_DEBUG",
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


def test_valid_local_environment_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_valid_local_environment(monkeypatch)

    settings = Settings()

    assert settings.env is Environment.LOCAL
    assert settings.release_sha == "local"
    assert settings.build_id == "local"
    assert settings.debug is False


def test_explicit_settings_are_valid_for_application_injection() -> None:
    settings = Settings(
        env=Environment.DEV,
        release_sha="abcdef123456",
        build_id="build-42",
        debug=False,
    )

    assert settings.env is Environment.DEV
    assert settings.release_sha == "abcdef123456"
    assert settings.build_id == "build-42"


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


def test_production_debug_is_rejected() -> None:
    with pytest.raises(ValidationError, match="DANTE_DEBUG"):
        Settings(
            env=Environment.PROD,
            release_sha="abcdef123456",
            build_id="build-42",
            debug=True,
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
        )


def test_settings_are_immutable_after_bootstrap() -> None:
    settings = Settings(
        env=Environment.LOCAL,
        release_sha="local",
        build_id="local",
        debug=False,
    )

    with pytest.raises(ValidationError, match="frozen"):
        settings.debug = True


def test_dotenv_local_is_not_loaded_implicitly(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _clear_dante_environment(monkeypatch)
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env.local").write_text(
        "DANTE_ENV=local\nDANTE_RELEASE_SHA=local\nDANTE_BUILD_ID=local\nDANTE_DEBUG=false\n",
        encoding="utf-8",
    )

    with pytest.raises(ValidationError, match="env"):
        Settings()
