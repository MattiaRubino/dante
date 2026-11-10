"""The disposable two-worker browser stack has an isolated DB pool budget."""

from __future__ import annotations

import runpy
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

import pytest
from pydantic import SecretStr

from dante.platform.config.database import DatabaseSettings


@pytest.fixture(scope="module")
def harness_override() -> Any:
    script = Path(__file__).resolve().parents[5] / "tooling" / "run-access-auth-stack.py"
    definitions = runpy.run_path(str(script))
    return definitions["_runtime_database_pool_override"]


@dataclass(frozen=True, slots=True)
class _CopyableSettings:
    database: DatabaseSettings

    def model_copy(self, *, update: dict[str, DatabaseSettings]) -> _CopyableSettings:
        return replace(self, database=update["database"])


def _baseline() -> _CopyableSettings:
    database = DatabaseSettings(
        host="127.0.0.1",
        name="dante_e2e",
        user="dante_runtime",
        password=SecretStr("test-only"),
        pool_size=5,
        max_overflow=5,
        pool_timeout_seconds=5.0,
    )

    return _CopyableSettings(database)


@pytest.mark.parametrize(
    ("workers", "expected"),
    [
        ("1", (5, 5, 5.0)),
        ("2", (10, 10, 15.0)),
    ],
)
def test_e2e_pool_budget_depends_only_on_browser_worker_count(
    monkeypatch: pytest.MonkeyPatch,
    harness_override: Any,
    workers: str,
    expected: tuple[int, int, float],
) -> None:
    baseline = _baseline()
    monkeypatch.setenv("DANTE_E2E_PER_STACK_WORKERS", workers)

    def original(**_kwargs: object) -> _CopyableSettings:
        return baseline

    settings = harness_override(original)(
        port=5432, runtime_password="only-test", auth_settings=object()
    )
    assert (
        settings.database.pool_size,
        settings.database.max_overflow,
        settings.database.pool_timeout_seconds,
    ) == expected
    assert (
        baseline.database.pool_size,
        baseline.database.max_overflow,
        baseline.database.pool_timeout_seconds,
    ) == (5, 5, 5.0)
    if workers == "1":
        assert settings is baseline
    else:
        assert settings is not baseline


@pytest.mark.parametrize("workers", ["0", "3", "auto", "-1"])
def test_e2e_pool_budget_rejects_unsupported_worker_counts(
    monkeypatch: pytest.MonkeyPatch,
    harness_override: Any,
    workers: str,
) -> None:
    monkeypatch.setenv("DANTE_E2E_PER_STACK_WORKERS", workers)

    def original(**_kwargs: object) -> _CopyableSettings:
        return _baseline()

    build = harness_override(original)
    with pytest.raises(RuntimeError, match="must be 1 or 2"):
        build(port=5432, runtime_password="only-test", auth_settings=object())
