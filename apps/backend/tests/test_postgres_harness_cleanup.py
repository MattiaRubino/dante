"""Regression coverage for disposable PostgreSQL Docker cleanup."""

from __future__ import annotations

import subprocess

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


def test_disposable_cluster_retries_forwarding_error_on_new_port(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A Created test container is removed before retrying on another port."""
    calls: list[tuple[str, ...]] = []
    ports = iter((49889, 49890))

    def docker(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        del check
        calls.append(args)
        if args[0] == "run" and sum(call[0] == "run" for call in calls) == 1:
            return subprocess.CompletedProcess(
                args,
                125,
                "",
                "ports are not available: /forwards/expose returned unexpected status: 500",
            )
        return subprocess.CompletedProcess(args, 0, "created", "")

    monkeypatch.setattr(harness, "_docker", docker)
    monkeypatch.setattr(harness, "_available_loopback_port", lambda: next(ports))

    port = harness._start_disposable_postgres(
        "dante-pytest-9c85a4a83d21",
        "dante-pytest-volume-2d6cf2b2c696",
        "test-password",
    )

    assert port == 49890
    assert [call[0] for call in calls] == ["run", "rm", "run"]
    assert calls[1] == ("rm", "--force", "dante-pytest-9c85a4a83d21")
    assert "127.0.0.1:49889:5432" in calls[0]
    assert "127.0.0.1:49890:5432" in calls[2]
