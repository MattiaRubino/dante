"""Cross-source proof for the provisioning-owned PostgreSQL observer boundary."""

from __future__ import annotations

import json
from pathlib import Path

from dante.platform.database.provisioning import OBSERVER_ROLE

_REPO_ROOT = Path(__file__).resolve().parents[3]
_EXPECTED_ROLES = ["dante_owner", "dante_migrator", "dante_runtime", "dante_observer"]


def test_observer_blueprint_dictionary_provisioning_and_collector_are_reconciled() -> None:
    """Prove every applicable representation; roles intentionally have no ORM mapping."""
    blueprint = (
        _REPO_ROOT / "docs" / "database" / "dante-postgresql-database-part-12.md"
    ).read_text(encoding="utf-8")
    scope = json.loads(
        (_REPO_ROOT / "docs" / "database" / "dictionary" / "scope.json").read_text(encoding="utf-8")
    )
    schema = json.loads(
        (
            _REPO_ROOT / "docs" / "database" / "dictionary" / "schema" / "scope-v1.schema.json"
        ).read_text(encoding="utf-8")
    )
    alloy = (_REPO_ROOT / "infra" / "observability" / "alloy" / "config.alloy").read_text(
        encoding="utf-8"
    )

    schema_roles = schema["properties"]["technical_foundation"]["properties"]["roles"]["const"]
    assert OBSERVER_ROLE == "dante_observer"
    assert scope["technical_foundation"]["roles"] == _EXPECTED_ROLES
    assert schema_roles == _EXPECTED_ROLES
    assert "<!-- DANTE-OBSERVABILITY-OBSERVER-CONTRACT v1 -->" in blueprint
    assert "pg_read_all_stats → dante_observer" in blueprint
    assert "SQLAlchemy mapping and Alembic migration are explicitly **not applicable**" in blueprint
    assert 'prometheus.relabel "postgres_privacy_budget"' in alloy
    assert "forward_to      = [prometheus.relabel.postgres_privacy_budget.receiver]" in alloy
    assert "pg_long_running_transactions.*" in alloy
    assert "include_query = true" not in alloy
    assert '"stat_statements",' not in alloy
    assert "stat_statements {" not in alloy
