#!/usr/bin/env python3
"""Atomically materialize Alloy's least-privilege PostgreSQL observer DSN."""

from __future__ import annotations

import argparse
import getpass
import os
import stat
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_PASSWORD_FILE = (
    _REPO_ROOT / "infra" / "compose" / "secrets" / "dante_observer_password.local"
)
_DEFAULT_OUTPUT = _REPO_ROOT / "infra" / "compose" / "secrets" / "dante_observer_dsn.local"


@dataclass(frozen=True, slots=True)
class ObserverConnection:
    """Validated local collector connection coordinates."""

    host: str
    port: int
    database: str
    user: str
    sslmode: str

    def dsn(self, password: str) -> str:
        """Render one RFC 3986-safe libpq URI without logging it."""
        authority = (
            f"{quote(self.user, safe='')}:{quote(password, safe='')}@{self.host}:{self.port}"
        )
        return (
            f"postgresql://{authority}/{quote(self.database, safe='')}"
            f"?sslmode={quote(self.sslmode, safe='')}"
        )


def _non_blank(value: str) -> str:
    candidate = value.strip()
    if not candidate or any(character.isspace() for character in candidate):
        raise argparse.ArgumentTypeError("value must be non-blank and whitespace-free")
    return candidate


def _port(value: str) -> int:
    candidate = int(value)
    if not 1 <= candidate <= 65_535:
        raise argparse.ArgumentTypeError("port must be between 1 and 65535")
    return candidate


def _password(path: Path) -> str:
    if path.exists():
        mode = stat.S_IMODE(path.stat().st_mode)
        if mode & 0o077:
            raise PermissionError(f"{path} must not be readable by group or others")
        value = path.read_text(encoding="utf-8")
        if value.endswith(("\n", "\r")):
            raise ValueError(f"{path} must not contain a trailing newline")
    else:
        value = getpass.getpass("dante_observer password: ")

    if not 16 <= len(value) <= 1_024 or any(ord(character) < 0x20 for character in value):
        raise ValueError("observer password must be 16-1024 printable characters")
    return value


def _atomic_collector_secret_write(path: Path, value: str) -> None:
    """Write a LOCAL collector secret readable by its supplementary host group."""
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
        os.replace(temporary, path)
        os.chmod(path, 0o640, follow_symlinks=False)
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
        description=(
            "Write Alloy's dante_observer DSN as a mode-0640 LOCAL Docker secret."
        ),
    )
    parser.add_argument("--host", type=_non_blank, default="postgres")
    parser.add_argument("--port", type=_port, default=5432)
    parser.add_argument("--database", type=_non_blank, default="dante")
    parser.add_argument("--user", type=_non_blank, default="dante_observer")
    parser.add_argument(
        "--sslmode",
        choices=("disable", "require", "verify-ca", "verify-full"),
        default="disable",
    )
    parser.add_argument("--password-file", type=Path, default=_DEFAULT_PASSWORD_FILE)
    parser.add_argument("--output", type=Path, default=_DEFAULT_OUTPUT)
    return parser


def main() -> None:
    """Build the secret without putting credentials in argv, stdout or shell history."""
    arguments = _parser().parse_args()
    connection = ObserverConnection(
        host=arguments.host,
        port=arguments.port,
        database=arguments.database,
        user=arguments.user,
        sslmode=arguments.sslmode,
    )
    _atomic_collector_secret_write(
        arguments.output.resolve(),
        connection.dsn(_password(arguments.password_file.resolve())),
    )
    print(f"Wrote private observer DSN: {arguments.output.resolve()}")


if __name__ == "__main__":
    main()
