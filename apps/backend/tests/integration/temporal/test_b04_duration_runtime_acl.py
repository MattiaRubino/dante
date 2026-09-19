"""Behavioral ACL proof for the B04-E runtime duration read surface."""

from __future__ import annotations

from typing import Any

import psycopg
import pytest


@pytest.mark.postgres
def test_b04_e_runtime_can_read_duration_current_rule_payload_table(
    migrated_database: Any,
) -> None:
    """Runtime reads only the typed duration table required by current-rule reads."""
    with psycopg.connect(
        **migrated_database.connection_kwargs(
            "dante_runtime",
            migrated_database.cluster.runtime_password,
        )
    ) as connection:
        rows = connection.execute(
            "SELECT material_state_ref FROM dante.temporal_constraint_duration_state LIMIT 0"
        ).fetchall()
        assert rows == []

        for private_table in (
            "temporal_constraint_current_history",
            "temporal_constraint_mutation_operation",
        ):
            with pytest.raises(psycopg.errors.InsufficientPrivilege):
                connection.execute(
                    f"SELECT * FROM dante.{private_table} LIMIT 0"
                ).fetchall()
            connection.rollback()
