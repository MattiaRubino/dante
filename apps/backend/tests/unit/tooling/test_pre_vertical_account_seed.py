"""Unit tests for LOCAL/DEV pre-vertical seed safety and secret configuration."""

from base64 import urlsafe_b64encode
from pathlib import Path

import pytest
from tooling.pre_vertical_foundation.account_seed import (
    SeedConfigurationError,
    database_target_from_environment,
    password_pepper_configuration_from_environment,
    read_local_secret,
    require_seed_environment,
)

_RUNTIME_PASSWORD = "runtime-secret"  # noqa: S105 - synthetic configuration fixture
_ACCOUNT_PASSWORD = "correct horse battery staple"  # noqa: S105 - synthetic fixture


def _canonical_secret(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def test_seed_environment_accepts_only_local_and_dev() -> None:
    assert require_seed_environment("local") == "local"
    assert require_seed_environment(" DEV ") == "dev"

    for value in (None, "", "uat", "prod", "production"):
        with pytest.raises(SeedConfigurationError):
            require_seed_environment(value)


def test_database_target_requires_canonical_runtime_identity() -> None:
    environ = {
        "DANTE_ENV": "local",
        "DANTE_DATABASE__HOST": "127.0.0.1",
        "DANTE_DATABASE__NAME": "dante",
        "DANTE_DATABASE__USER": "dante_runtime",
        "DANTE_DATABASE__PASSWORD": _RUNTIME_PASSWORD,
    }

    target = database_target_from_environment(environ)
    assert target.host == "127.0.0.1"
    assert target.port == 5432
    assert target.name == "dante"

    invalid = dict(environ)
    invalid["DANTE_DATABASE__USER"] = "postgres"
    with pytest.raises(SeedConfigurationError, match="dante_runtime"):
        database_target_from_environment(invalid)


def test_password_pepper_configuration_requires_canonical_32_byte_base64url() -> None:
    encoded = _canonical_secret(b"p" * 32)
    environ = {
        "DANTE_AUTH__PASSWORD_CURRENT_PEPPER_KEY_ID": "local-password-v1",
        "DANTE_AUTH__PASSWORD_PEPPERS": ('{"local-password-v1":"' + encoded + '"}'),
    }

    current, ring = password_pepper_configuration_from_environment(environ)
    assert current == "local-password-v1"
    assert ring == {"local-password-v1": b"p" * 32}

    malformed = dict(environ)
    malformed["DANTE_AUTH__PASSWORD_PEPPERS"] = '{"local-password-v1":"not-canonical"}'  # noqa: S105 - deliberately malformed synthetic fixture
    with pytest.raises(SeedConfigurationError):
        password_pepper_configuration_from_environment(malformed)


def test_local_secret_requires_ignored_style_single_line_file(tmp_path: Path) -> None:
    secret_file = tmp_path / "dogfood_password.local"
    secret_file.write_text(f"{_ACCOUNT_PASSWORD}\n", encoding="utf-8")
    assert read_local_secret(secret_file) == _ACCOUNT_PASSWORD

    wrong_suffix = tmp_path / "dogfood_password.txt"
    wrong_suffix.write_text("secret", encoding="utf-8")
    with pytest.raises(SeedConfigurationError, match=r"\.local"):
        read_local_secret(wrong_suffix)

    multiline = tmp_path / "multiline.local"
    multiline.write_text("one\ntwo\n", encoding="utf-8")
    with pytest.raises(SeedConfigurationError, match="exactly one"):
        read_local_secret(multiline)
