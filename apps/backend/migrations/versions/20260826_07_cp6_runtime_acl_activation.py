"""Activate CP6-M07 exact runtime ACLs and runtime-compatible Role-13 locking.

Revision ID: 20260826_07
Revises: 20260826_06
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260826_07"
down_revision: str | None = "20260826_06"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_RUNTIME_ROLE = "dante_runtime"
_MIGRATOR_ROLE = "dante_migrator"

_ALL_TABLES = (
    "person", "living_referent", "asset", "place", "content_artifact", "collective",
    "possibility", "goal", "plan", "activity", "event", "routine", "occurrence",
    "session", "observation", "native_address", "scoped_address", "material_state_address",
    "native_current_material_state", "scoped_current_material_state", "schedule",
    "schedule_placement_state", "schedule_placement_date_state",
    "schedule_placement_floating_local_state", "schedule_placement_named_zone_state",
    "schedule_placement_absolute_state", "schedule_placement_current_history", "actual",
    "actual_realization_state", "actual_realization_timing", "actual_realization_session_basis",
    "actual_realization_current_history", "session_timing_state", "session_timing_absolute",
    "session_timing_elapsed", "session_timing_pause", "session_timing_current_history",
    "routine_recurrence_state", "routine_recurrence_boundary_state",
    "routine_recurrence_calendar_state", "routine_recurrence_calendar_wall_time",
    "routine_recurrence_calendar_weekday", "routine_recurrence_calendar_month_day",
    "routine_recurrence_calendar_ordinal_weekday", "routine_recurrence_calendar_year_month_day",
    "routine_recurrence_elapsed_state", "routine_recurrence_quota_state",
    "routine_recurrence_cyclic_state", "routine_recurrence_cycle_position",
    "routine_recurrence_current_history", "event_recurrence_state",
    "event_recurrence_boundary_state", "event_recurrence_calendar_state",
    "event_recurrence_calendar_wall_time", "event_recurrence_calendar_weekday",
    "event_recurrence_calendar_month_day", "event_recurrence_calendar_ordinal_weekday",
    "event_recurrence_calendar_year_month_day", "event_recurrence_elapsed_state",
    "event_recurrence_quota_state", "event_recurrence_cyclic_state",
    "event_recurrence_cycle_position", "event_recurrence_current_history",
    "occurrence_generation", "occurrence_generation_calendar", "occurrence_generation_elapsed",
    "occurrence_generation_quota", "occurrence_generation_cyclic",
)

_NO_INSERT_TABLES = {
    "person", "living_referent", "asset", "place", "content_artifact", "collective",
    "possibility", "goal", "plan", "activity", "event", "observation",
    "native_current_material_state", "scoped_current_material_state",
}

_HISTORY_INSERT_COLUMNS = {
    "schedule_placement_current_history": ("schedule_ref", "material_state_ref", "current_from_at"),
    "actual_realization_current_history": ("actual_ref", "material_state_ref", "current_from_at"),
    "session_timing_current_history": ("session_ref", "material_state_ref", "current_from_at"),
    "routine_recurrence_current_history": ("routine_ref", "material_state_ref", "current_from_at"),
    "event_recurrence_current_history": ("event_ref", "material_state_ref", "current_from_at"),
}

_TABLE_INSERT = tuple(
    table for table in _ALL_TABLES
    if table not in _NO_INSERT_TABLES and table not in _HISTORY_INSERT_COLUMNS
)

_VIEW_ACL = {
    "schedule_current_placement": ("scoped_owner_ref", True),
    "actual_current_realization": ("scoped_owner_ref", True),
    "session_current_timing": ("native_owner_ref", False),
    "routine_current_recurrence": ("native_owner_ref", False),
    "event_current_recurrence": ("native_owner_ref", False),
}

_ROUTINES = (
    "enforce_native_address_owner", "enforce_scoped_address_owner",
    "enforce_native_ref_eligibility", "enforce_material_state_totality",
    "enforce_current_material_state_binding", "enforce_current_history_equivalence",
    "enforce_owner_creation_completeness", "enforce_schedule_placement_totality",
    "enforce_actual_realization_basis", "enforce_session_timing_totality",
    "enforce_session_pause_consistency", "enforce_recurrence_aggregate_integrity",
    "enforce_occurrence_generation_integrity", "validate_iana_timezone",
)

_ROUTINE_OWNER_LOCK = (
    "PERFORM 1 FROM dante.routine WHERE routine_ref=g.source_native_ref FOR UPDATE;"
)
_EVENT_OWNER_LOCK = (
    "PERFORM 1 FROM dante.event WHERE event_ref=g.source_native_ref FOR UPDATE;"
)
_ROUTINE_ADVISORY_BOUNDARY = (
    "NULL; -- CP6-M07: Part-14 advisory locks are acquired by the accepted operation boundary for Routine generation"
)
_EVENT_ADVISORY_BOUNDARY = (
    "NULL; -- CP6-M07: Part-14 advisory locks are acquired by the accepted operation boundary for Event generation"
)


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def _replace_role13_fragment(old: str, new: str) -> None:
    connection = op.get_bind()
    definition = connection.exec_driver_sql(
        """
        SELECT pg_get_functiondef(p.oid)
        FROM pg_proc AS p
        JOIN pg_namespace AS n ON n.oid = p.pronamespace
        WHERE n.nspname = 'dante'
          AND p.proname = 'enforce_occurrence_generation_integrity'
          AND p.pronargs = 0
        """
    ).scalar_one()
    if definition.count(old) != 1:
        raise RuntimeError("Role-13 owner-lock fragment did not match exactly once")
    connection.exec_driver_sql(definition.replace(old, new))


def _repair_role13_for_runtime_acl() -> None:
    _replace_role13_fragment(_ROUTINE_OWNER_LOCK, _ROUTINE_ADVISORY_BOUNDARY)
    _replace_role13_fragment(_EVENT_OWNER_LOCK, _EVENT_ADVISORY_BOUNDARY)
    _sql("ALTER FUNCTION dante.enforce_occurrence_generation_integrity() OWNER TO dante_owner")
    _sql(
        "REVOKE ALL PRIVILEGES ON FUNCTION dante.enforce_occurrence_generation_integrity() "
        "FROM PUBLIC, dante_runtime, dante_migrator"
    )


def _restore_m6_role13_owner_lock() -> None:
    _replace_role13_fragment(_ROUTINE_ADVISORY_BOUNDARY, _ROUTINE_OWNER_LOCK)
    _replace_role13_fragment(_EVENT_ADVISORY_BOUNDARY, _EVENT_OWNER_LOCK)
    _sql("ALTER FUNCTION dante.enforce_occurrence_generation_integrity() OWNER TO dante_owner")
    _sql(
        "REVOKE ALL PRIVILEGES ON FUNCTION dante.enforce_occurrence_generation_integrity() "
        "FROM PUBLIC, dante_runtime, dante_migrator"
    )


def _activate_exact_acl() -> None:
    if len(_ALL_TABLES) != 68:
        raise RuntimeError("M7 table ACL manifest must contain exactly 68 tables")
    if len(_NO_INSERT_TABLES) != 14:
        raise RuntimeError("M7 no-INSERT set must contain exactly 14 tables")
    if len(_HISTORY_INSERT_COLUMNS) != 5:
        raise RuntimeError("M7 history INSERT set must contain exactly 5 tables")
    if len(_TABLE_INSERT) != 49:
        raise RuntimeError("M7 table-level INSERT set must contain exactly 49 tables")
    if len(_VIEW_ACL) != 5 or len(_ROUTINES) != 14:
        raise RuntimeError("M7 view/routine ACL manifests are not canonical")

    for table in _ALL_TABLES:
        _sql(
            f"REVOKE ALL PRIVILEGES ON TABLE dante.{table} "
            f"FROM PUBLIC, {_RUNTIME_ROLE}, {_MIGRATOR_ROLE}"
        )
        _sql(f"GRANT SELECT ON TABLE dante.{table} TO {_RUNTIME_ROLE}")

    for table in _TABLE_INSERT:
        _sql(f"GRANT INSERT ON TABLE dante.{table} TO {_RUNTIME_ROLE}")

    for table, columns in _HISTORY_INSERT_COLUMNS.items():
        owner_column, material_column, from_column = columns
        _sql(
            f"GRANT INSERT ({owner_column}, {material_column}, {from_column}) "
            f"ON TABLE dante.{table} TO {_RUNTIME_ROLE}"
        )
        _sql(
            f"GRANT UPDATE (current_until_at) ON TABLE dante.{table} "
            f"TO {_RUNTIME_ROLE}"
        )

    for view, (owner_column, delete_allowed) in _VIEW_ACL.items():
        _sql(
            f"REVOKE ALL PRIVILEGES ON TABLE dante.{view} "
            f"FROM PUBLIC, {_RUNTIME_ROLE}, {_MIGRATOR_ROLE}"
        )
        _sql(f"GRANT SELECT ON TABLE dante.{view} TO {_RUNTIME_ROLE}")
        _sql(
            f"GRANT INSERT ({owner_column}, material_state_ref) "
            f"ON TABLE dante.{view} TO {_RUNTIME_ROLE}"
        )
        _sql(
            f"GRANT UPDATE (material_state_ref) ON TABLE dante.{view} "
            f"TO {_RUNTIME_ROLE}"
        )
        if delete_allowed:
            _sql(f"GRANT DELETE ON TABLE dante.{view} TO {_RUNTIME_ROLE}")

    for routine in _ROUTINES:
        _sql(
            f"REVOKE ALL PRIVILEGES ON FUNCTION dante.{routine}() "
            f"FROM PUBLIC, {_RUNTIME_ROLE}, {_MIGRATOR_ROLE}"
        )

    _sql(
        "REVOKE ALL PRIVILEGES ON TABLE dante.alembic_version "
        "FROM PUBLIC, dante_runtime"
    )


def _deactivate_business_acl() -> None:
    for table in _ALL_TABLES:
        _sql(
            f"REVOKE ALL PRIVILEGES ON TABLE dante.{table} "
            f"FROM {_RUNTIME_ROLE}"
        )
    for view in _VIEW_ACL:
        _sql(
            f"REVOKE ALL PRIVILEGES ON TABLE dante.{view} "
            f"FROM {_RUNTIME_ROLE}"
        )


def upgrade() -> None:
    """Activate the final CP6 runtime capability matrix."""
    _repair_role13_for_runtime_acl()
    _activate_exact_acl()


def downgrade() -> None:
    """Return to the M6 deny-by-default runtime posture."""
    _deactivate_business_acl()
    _restore_m6_role13_owner_lock()
