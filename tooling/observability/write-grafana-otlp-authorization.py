#!/usr/bin/env python3
"""Atomically materialize Alloy's private Grafana Cloud OTLP authorization header."""

from __future__ import annotations

import argparse
import base64
import os
import stat
import sys
from dataclasses import dataclass
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_ENV_FILE = _REPO_ROOT / "infra" / "observability" / ".env.local"
_DEFAULT_TOKEN_FILE = _REPO_ROOT / "infra" / "compose" / "secrets" / "grafana_cloud_api_key.local"
_DEFAULT_OUTPUT = (
    _REPO_ROOT / "infra" / "compose" / "secrets" / "grafana_cloud_otlp_authorization.local"
)


@dataclass(frozen=True, slots=True)
class GrafanaCloudOtlpCredentials:
    """Non-displayable credentials required by the Grafana OTLP gateway."""

    instance_id: str
    api_token: str

    def authorization_header(self) -> str:
        """Render one RFC 7617 Basic authorization value without logging it."""
        material = f"{self.instance_id}:{self.api_token}".encode()
        encoded = base64.b64encode(material).decode("ascii")
        return f"Basic {encoded}"


def _otlp_instance_id(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"missing LOCAL observability environment file: {path}")

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("GRAFANA_CLOUD_OTLP_USERNAME="):
            candidate = line.partition("=")[2].strip()
            if candidate.isdecimal() and candidate != "0":
                return candidate
            break
    raise ValueError("GRAFANA_CLOUD_OTLP_USERNAME must be a non-zero numeric instance ID")


def _api_token(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"missing Grafana Cloud API token file: {path}")
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode & 0o007:
        raise PermissionError(f"{path} must not be readable by others")
    value = path.read_text(encoding="utf-8")
    if not value or value.endswith(("\n", "\r")) or any(character.isspace() for character in value):
        raise ValueError(
            f"{path} must contain one whitespace-free token without a trailing newline"
        )
    return value


def _atomic_collector_secret_write(path: Path, value: str) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    descriptor: int | None = None
    try:
        descriptor = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
            0o640,
        )
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as stream:
            descriptor = None
            stream.write(value)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(path)
        path.chmod(0o640)
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        if descriptor is not None:
            os.close(descriptor)
        temporary.unlink(missing_ok=True)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Write Alloy's Grafana Cloud OTLP authorization header as a LOCAL secret.",
    )
    parser.add_argument("--env-file", type=Path, default=_DEFAULT_ENV_FILE)
    parser.add_argument("--api-token-file", type=Path, default=_DEFAULT_TOKEN_FILE)
    parser.add_argument("--output", type=Path, default=_DEFAULT_OUTPUT)
    return parser


def main() -> None:
    """Build the derived header without exposing it in argv, stdout or shell history."""
    arguments = _parser().parse_args()
    credentials = GrafanaCloudOtlpCredentials(
        instance_id=_otlp_instance_id(arguments.env_file.resolve()),
        api_token=_api_token(arguments.api_token_file.resolve()),
    )
    _atomic_collector_secret_write(
        arguments.output.resolve(),
        credentials.authorization_header(),
    )
    sys.stderr.write(f"Wrote private Grafana OTLP authorization: {arguments.output.resolve()}\n")


if __name__ == "__main__":
    main()
