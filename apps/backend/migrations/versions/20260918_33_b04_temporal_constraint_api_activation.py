"""Activate B04-A API-safe replay and least-privilege current-rule reads.

Revision ID: 20260918_33
Revises: 20260918_32
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260918_33"
down_revision: str | None = "20260918_32"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_OWNER = "dante_owner"
_MIGRATOR = "dante_migrator"
_RUNTIME = "dante_runtime"

_MUTATE_SIGNATURE = (
    "dante.mutate_self_absolute_earliest_start_constraint("
    "uuid,text,text,text,uuid,uuid,uuid,uuid,text,timestamp with time zone)"
)

_PRE_A5_REPLAY = r"""            IF FOUND THEN
                IF existing_fingerprint<>requested_intent_fingerprint
                   OR existing_kind<>requested_mutation_kind
                   OR existing_constraint_ref<>requested_constraint_ref
                   OR existing_subject_ref<>requested_subject_native_ref
                   OR existing_expected_ref IS DISTINCT FROM requested_expected_material_state_ref
                   OR existing_result_ref IS DISTINCT FROM requested_resulting_material_state_ref THEN
                    RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_temporal_constraint_mutation_operation', MESSAGE='Temporal Constraint operation id reused with different intent';
                END IF;"""

_A5_REPLAY = r"""            IF FOUND THEN
                IF existing_fingerprint<>requested_intent_fingerprint
                   OR existing_kind<>requested_mutation_kind
                   OR existing_subject_ref<>requested_subject_native_ref
                   OR (
                        requested_mutation_kind<>'create'
                        AND existing_constraint_ref<>requested_constraint_ref
                   )
                   OR (
                        requested_mutation_kind<>'create'
                        AND existing_expected_ref IS DISTINCT FROM requested_expected_material_state_ref
                   ) THEN
                    RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_temporal_constraint_mutation_operation', MESSAGE='Temporal Constraint operation id reused with different intent';
                END IF;"""

_READ_TABLES = (
    "temporal_constraint",
    "temporal_constraint_state",
    "temporal_constraint_boundary_state",
    "temporal_constraint_boundary_absolute_state",
)

_PRIVATE_TABLES = (
    "temporal_constraint_current_history",
    "temporal_constraint_mutation_operation",
)


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def _activate_retry_safe_replay() -> None:
    connection = op.get_bind()
    definition = connection.exec_driver_sql(
        """
        SELECT pg_get_functiondef(p.oid)
        FROM pg_proc AS p
        JOIN pg_namespace AS n ON n.oid = p.pronamespace
        WHERE n.nspname = 'dante'
          AND p.proname = 'mutate_self_absolute_earliest_start_constraint'
          AND p.pronargs = 10
        """
    ).scalar_one()
    if definition.count(_PRE_A5_REPLAY) != 1:
        raise RuntimeError(
            "B04-A mutation replay hardening expected the pre-A5 replay fragment exactly once"
        )
    connection.exec_driver_sql(
        definition.replace(_PRE_A5_REPLAY, _A5_REPLAY).replace("%", "%%")
    )
    _sql(f"ALTER FUNCTION {_MUTATE_SIGNATURE} OWNER TO {_OWNER}")
    _sql(
        f"REVOKE ALL PRIVILEGES ON FUNCTION {_MUTATE_SIGNATURE} "
        f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
    )
    _sql(f"GRANT EXECUTE ON FUNCTION {_MUTATE_SIGNATURE} TO {_RUNTIME}")


def _activate_current_rule_reads() -> None:
    for table in _READ_TABLES:
        _sql(f"GRANT SELECT ON TABLE dante.{table} TO {_RUNTIME}")
    for table in _PRIVATE_TABLES:
        _sql(f"REVOKE ALL PRIVILEGES ON TABLE dante.{table} FROM {_RUNTIME}")


def upgrade() -> None:
    """Activate the narrow persistence capabilities required by the B04-A API."""
    _activate_retry_safe_replay()
    _activate_current_rule_reads()


def downgrade() -> None:
    """Refuse restoration of an API-unsafe replay contract."""
    raise RuntimeError(
        "B04-A API activation downgrade is intentionally refused; use a separately "
        "reviewed forward migration"
    )
