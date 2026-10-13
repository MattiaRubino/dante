"""Behavioral ACL proof for the B04-C runtime window read surface."""

from __future__ import annotations

from typing import Any

import psycopg
import pytest
from psycopg import sql


@pytest.mark.postgres
def test_b04_c_runtime_can_read_window_current_rule_payload_tables(
    migrated_database: Any,
) -> None:
    """Runtime reads the two typed window tables used by Get/List/Evaluate."""
    with psycopg.connect(
        **migrated_database.connection_kwargs(
            "dante_runtime",
            migrated_database.cluster.runtime_password,
        )
    ) as connection:
        for table in (
            "temporal_constraint_window_state",
            "temporal_constraint_window_absolute_state",
        ):
            rows = connection.execute(
                sql.SQL("SELECT material_state_ref FROM dante.{} LIMIT 0").format(
                    sql.Identifier(table)
                )
            ).fetchall()
            assert rows == []
