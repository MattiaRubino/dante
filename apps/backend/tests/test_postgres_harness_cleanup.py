"""Regression coverage for disposable PostgreSQL Docker cleanup."""

from __future__ import annotations

import pytest

from tests.integration import conftest as harness


def test_disposable_cluster_cleanup_removes_only_its_dedicated_volume(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Every acceptance cluster teardown releases image-declared data storage."""
    calls: list[tuple[tuple[str, ...], bool]] = []

    def record(*args: str, check: bool = True) -> None:
        calls.append((args, check))

    monkeypatch.setattr(harness, "_docker", record)

    harness._remove_disposable_cluster(
        "dante-pytest-9c85a4a83d21", "dante-pytest-volume-2d6cf2b2c696"
    )

    assert calls == [
        (("rm", "--force", "--volumes", "dante-pytest-9c85a4a83d21"), False),
        (("volume", "rm", "--force", "dante-pytest-volume-2d6cf2b2c696"), False),
    ]


def test_disposable_cluster_volume_is_explicitly_labelled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Future recovery can select test data without matching LOCAL volumes."""
    calls: list[tuple[tuple[str, ...], bool]] = []

    def record(*args: str, check: bool = True) -> None:
        calls.append((args, check))

    monkeypatch.setattr(harness, "_docker", record)

    harness._create_disposable_volume("dante-pytest-volume-2d6cf2b2c696")

    assert calls == [
        (
            (
                "volume",
                "create",
                "--label",
                "dante.test.scope=postgres-acceptance",
                "dante-pytest-volume-2d6cf2b2c696",
            ),
            True,
        )
    ]
