from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import psycopg
from psycopg import sql

_CORE_PATH = Path(__file__).with_name("serve-access-auth-stack.py")
_REQUIRED_EXTENSIONS: tuple[tuple[str, str | None], ...] = (
    ("postgis", "3.6.4"),
    ("vector", "0.8.6"),
    ("pg_trgm", None),
    ("unaccent", None),
    ("pg_stat_statements", None),
)


def _load_core() -> ModuleType:
    spec = importlib.util.spec_from_file_location("dante_access_auth_stack_core", _CORE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load the Access/Auth full-stack harness core.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _extension_guard(database_name: str):
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
                statement = sql.SQL("CREATE EXTENSION IF NOT EXISTS {}") .format(
                    sql.Identifier(extension_name)
                )
                if expected_version is not None:
                    statement += sql.SQL(" VERSION {}") .format(
                        sql.Literal(expected_version)
                    )
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


def main() -> None:
    core = _load_core()
    database_name = getattr(core, "_DATABASE_NAME", None)
    if not isinstance(database_name, str) or not database_name:
        raise RuntimeError("Access/Auth harness core does not expose its database name.")

    core._create_extensions = _extension_guard(database_name)
    core.main()


if __name__ == "__main__":
    main()
