"""Materialize recovery-safe MaterialState retirement and anti-resurrection guards.

Revision ID: 20260830_09
Revises: 20260826_08
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20260830_09"
down_revision: str | None = "20260826_08"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_DANTE_SCHEMA = "dante"
_OWNER_ROLE = "dante_owner"
_MIGRATOR_ROLE = "dante_migrator"
_RUNTIME_ROLE = "dante_runtime"

_ROUTINE = "enforce_material_state_retirement"

_SCHEDULE_BASE = r"""    IF date_n+floating_n+named_n+absolute_n<>1 OR
       (form='date_span' AND date_n<>1) OR (form='floating_local' AND floating_n<>1) OR
       (form='named_zone_local' AND named_n<>1) OR (form='absolute' AND absolute_n<>1) THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='Schedule placement payload rejected', DETAIL='exactly one typed payload must match temporal_form_code';
    END IF;"""

_SCHEDULE_RETIREMENT = r"""    IF EXISTS (SELECT 1 FROM dante.material_state_retirement WHERE material_state_ref=state_ref) THEN
        IF date_n+floating_n+named_n+absolute_n<>0 THEN
            RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                MESSAGE='retired Schedule placement payload rejected', DETAIL='retired MaterialState keeps its envelope/reference continuity but no placement payload';
        END IF;
    ELSIF date_n+floating_n+named_n+absolute_n<>1 OR
       (form='date_span' AND date_n<>1) OR (form='floating_local' AND floating_n<>1) OR
       (form='named_zone_local' AND named_n<>1) OR (form='absolute' AND absolute_n<>1) THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='Schedule placement payload rejected', DETAIL='exactly one typed payload must match temporal_form_code';
    END IF;"""

_SESSION_BASE = r"""    IF absolute_n+elapsed_n<>1 OR (form='absolute' AND absolute_n<>1) OR (form='elapsed_only' AND elapsed_n<>1) THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='Session timing payload rejected', DETAIL='exactly one typed timing payload must match timing_form_code';
    END IF;"""

_SESSION_RETIREMENT = r"""    IF EXISTS (SELECT 1 FROM dante.material_state_retirement WHERE material_state_ref=state_ref) THEN
        IF absolute_n+elapsed_n<>0 THEN
            RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                MESSAGE='retired Session timing payload rejected', DETAIL='retired MaterialState keeps its envelope/reference continuity but no timing payload';
        END IF;
    ELSIF absolute_n+elapsed_n<>1 OR (form='absolute' AND absolute_n<>1) OR (form='elapsed_only' AND elapsed_n<>1) THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='Session timing payload rejected', DETAIL='exactly one typed timing payload must match timing_form_code';
    END IF;"""

_ACTUAL_BASE = r"""    IF TG_TABLE_NAME='actual_realization_timing' THEN state_ref:=NEW.material_state_ref; ELSE state_ref:=NEW.actual_material_state_ref; END IF;
    SELECT realization_occurred INTO occurred FROM dante.actual_realization_state WHERE material_state_ref=state_ref;"""

_ACTUAL_RETIREMENT = r"""    IF TG_TABLE_NAME='actual_realization_timing' THEN state_ref:=NEW.material_state_ref; ELSE state_ref:=NEW.actual_material_state_ref; END IF;
    IF EXISTS (SELECT 1 FROM dante.material_state_retirement WHERE material_state_ref=state_ref) THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='retired Actual realization payload rejected', DETAIL='retired MaterialState may not regain timing/session-basis payload';
    END IF;
    SELECT realization_occurred INTO occurred FROM dante.actual_realization_state WHERE material_state_ref=state_ref;"""

_RECURRENCE_BASE = r"""    state_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.material_state_ref ELSE NEW.material_state_ref END;
    IF TG_TABLE_NAME LIKE 'routine_recurrence_%' THEN prefix:='routine'; ELSE prefix:='event'; END IF;

    IF prefix='routine' THEN"""

_RECURRENCE_RETIREMENT = r"""    state_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.material_state_ref ELSE NEW.material_state_ref END;
    IF TG_TABLE_NAME LIKE 'routine_recurrence_%' THEN prefix:='routine'; ELSE prefix:='event'; END IF;

    IF EXISTS (SELECT 1 FROM dante.material_state_retirement WHERE material_state_ref=state_ref) THEN
      IF prefix='routine' THEN
        SELECT EXISTS (
          SELECT 1 FROM dante.routine_recurrence_boundary_state WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.routine_recurrence_calendar_state WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.routine_recurrence_calendar_wall_time WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.routine_recurrence_calendar_weekday WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.routine_recurrence_calendar_month_day WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.routine_recurrence_calendar_ordinal_weekday WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.routine_recurrence_calendar_year_month_day WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.routine_recurrence_elapsed_state WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.routine_recurrence_quota_state WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.routine_recurrence_cyclic_state WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.routine_recurrence_cycle_position WHERE material_state_ref=state_ref
        ) INTO bad;
      ELSE
        SELECT EXISTS (
          SELECT 1 FROM dante.event_recurrence_boundary_state WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.event_recurrence_calendar_state WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.event_recurrence_calendar_wall_time WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.event_recurrence_calendar_weekday WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.event_recurrence_calendar_month_day WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.event_recurrence_calendar_ordinal_weekday WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.event_recurrence_calendar_year_month_day WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.event_recurrence_elapsed_state WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.event_recurrence_quota_state WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.event_recurrence_cyclic_state WHERE material_state_ref=state_ref
          UNION ALL SELECT 1 FROM dante.event_recurrence_cycle_position WHERE material_state_ref=state_ref
        ) INTO bad;
      END IF;
      IF bad THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
          MESSAGE='retired Recurrence payload rejected', DETAIL='retired MaterialState keeps its recurrence envelope/reference continuity but no recurrence payload/selectors';
      END IF;
      IF TG_OP='DELETE' THEN RETURN OLD; END IF; RETURN NEW;
    END IF;

    IF prefix='routine' THEN"""


def _replace_routine_fragment(name: str, old: str, new: str, *, failure: str) -> None:
    connection = op.get_bind()
    definition = connection.exec_driver_sql(
        """
        SELECT pg_get_functiondef(p.oid)
        FROM pg_proc AS p
        JOIN pg_namespace AS n ON n.oid = p.pronamespace
        WHERE n.nspname = 'dante'
          AND p.proname = %s
          AND p.pronargs = 0
        """,
        (name,),
    ).scalar_one()
    if definition.count(old) != 1:
        raise RuntimeError(failure)
    connection.exec_driver_sql(definition.replace(old, new).replace("%", "%%"))
    connection.exec_driver_sql(f"ALTER FUNCTION dante.{name}() OWNER TO {_OWNER_ROLE}")
    connection.exec_driver_sql(
        f"REVOKE ALL PRIVILEGES ON FUNCTION dante.{name}() "
        f"FROM PUBLIC, {_RUNTIME_ROLE}, {_MIGRATOR_ROLE}"
    )


def _create_retirement_routine() -> None:
    op.execute(
        sa.text(
            r"""
            CREATE FUNCTION dante.enforce_material_state_retirement()
            RETURNS trigger
            LANGUAGE plpgsql
            SECURITY INVOKER
            VOLATILE
            PARALLEL UNSAFE
            SET search_path = pg_catalog, dante, pg_temp
            AS $function$
            DECLARE
                state_ref uuid;
                facet text;
                payload_exists boolean := false;
            BEGIN
                IF TG_OP='UPDATE' OR TG_OP='DELETE' THEN
                    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME,
                        TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                        MESSAGE='MaterialState retirement is immutable',
                        DETAIL='retirement/tombstone rows are append-only and may not be rewritten or removed';
                END IF;

                state_ref:=NEW.material_state_ref;
                SELECT facet_code INTO facet
                  FROM dante.material_state_address
                 WHERE material_state_ref=state_ref;
                IF NOT FOUND THEN
                    RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT=TG_NAME,
                        TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                        MESSAGE='MaterialState retirement has no address',
                        DETAIL='retirement requires an existing MaterialStateRef address/envelope';
                END IF;

                IF facet='schedule.placement' THEN
                    SELECT EXISTS (
                      SELECT 1 FROM dante.schedule_placement_date_state WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.schedule_placement_floating_local_state WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.schedule_placement_named_zone_state WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.schedule_placement_absolute_state WHERE material_state_ref=state_ref
                    ) INTO payload_exists;
                ELSIF facet='actual.realization' THEN
                    SELECT EXISTS (
                      SELECT 1 FROM dante.actual_realization_timing WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.actual_realization_session_basis WHERE actual_material_state_ref=state_ref
                    ) INTO payload_exists;
                ELSIF facet='session.timing' THEN
                    SELECT EXISTS (
                      SELECT 1 FROM dante.session_timing_absolute WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.session_timing_elapsed WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.session_timing_pause WHERE material_state_ref=state_ref
                    ) INTO payload_exists;
                ELSIF facet='routine.recurrence' THEN
                    SELECT EXISTS (
                      SELECT 1 FROM dante.routine_recurrence_boundary_state WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.routine_recurrence_calendar_state WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.routine_recurrence_calendar_wall_time WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.routine_recurrence_calendar_weekday WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.routine_recurrence_calendar_month_day WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.routine_recurrence_calendar_ordinal_weekday WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.routine_recurrence_calendar_year_month_day WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.routine_recurrence_elapsed_state WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.routine_recurrence_quota_state WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.routine_recurrence_cyclic_state WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.routine_recurrence_cycle_position WHERE material_state_ref=state_ref
                    ) INTO payload_exists;
                ELSIF facet='event.recurrence' THEN
                    SELECT EXISTS (
                      SELECT 1 FROM dante.event_recurrence_boundary_state WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.event_recurrence_calendar_state WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.event_recurrence_calendar_wall_time WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.event_recurrence_calendar_weekday WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.event_recurrence_calendar_month_day WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.event_recurrence_calendar_ordinal_weekday WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.event_recurrence_calendar_year_month_day WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.event_recurrence_elapsed_state WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.event_recurrence_quota_state WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.event_recurrence_cyclic_state WHERE material_state_ref=state_ref
                      UNION ALL SELECT 1 FROM dante.event_recurrence_cycle_position WHERE material_state_ref=state_ref
                    ) INTO payload_exists;
                ELSE
                    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME,
                        TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                        MESSAGE='MaterialState retirement facet rejected',
                        DETAIL='retirement may target only a materialized DANTE MaterialState facet';
                END IF;

                IF payload_exists THEN
                    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME,
                        TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                        MESSAGE='MaterialState retirement payload rejected',
                        DETAIL='a committed retirement must retain reference/history continuity while protected payload is absent';
                END IF;
                RETURN NEW;
            END;
            $function$
            """
        )
    )
    op.execute(sa.text(f"ALTER FUNCTION dante.{_ROUTINE}() OWNER TO {_OWNER_ROLE}"))
    op.execute(
        sa.text(
            f"REVOKE ALL PRIVILEGES ON FUNCTION dante.{_ROUTINE}() "
            f"FROM PUBLIC, {_RUNTIME_ROLE}, {_MIGRATOR_ROLE}"
        )
    )


def upgrade() -> None:
    """Install the canonical retirement/tombstone row and anti-resurrection guards."""
    op.create_table(
        "material_state_retirement",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("retirement_code", sa.Text(), nullable=False),
        sa.Column("retired_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("recovery_suppression_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("material_state_ref", name=op.f("pk_material_state_retirement")),
        sa.UniqueConstraint(
            "recovery_suppression_ref",
            name=op.f("uq_material_state_retirement_recovery_suppression_ref"),
        ),
        sa.CheckConstraint(
            "retirement_code IN ('redacted','unavailable')",
            name=op.f("ck_material_state_retirement_retirement_code"),
        ),
        sa.CheckConstraint(
            "isfinite(retired_at)",
            name=op.f("ck_material_state_retirement_retired_at"),
        ),
        sa.CheckConstraint(
            "uuid_extract_version(recovery_suppression_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_material_state_retirement_recovery_suppression_uuidv7"),
        ),
        sa.ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name=op.f("fk_material_state_retirement_material_state_ref_material_state_address"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        schema=_DANTE_SCHEMA,
    )
    op.execute(sa.text("ALTER TABLE dante.material_state_retirement OWNER TO dante_owner"))
    op.execute(
        sa.text(
            "REVOKE ALL PRIVILEGES ON TABLE dante.material_state_retirement "
            "FROM PUBLIC, dante_runtime, dante_migrator"
        )
    )
    op.execute(sa.text("GRANT SELECT ON TABLE dante.material_state_retirement TO dante_runtime"))

    _create_retirement_routine()
    op.execute(
        sa.text(
            "CREATE CONSTRAINT TRIGGER ctrg_material_state_retirement_integrity "
            "AFTER INSERT OR UPDATE OR DELETE ON dante.material_state_retirement "
            "DEFERRABLE INITIALLY DEFERRED FOR EACH ROW "
            "EXECUTE FUNCTION dante.enforce_material_state_retirement()"
        )
    )

    _replace_routine_fragment(
        "enforce_schedule_placement_totality",
        _SCHEDULE_BASE,
        _SCHEDULE_RETIREMENT,
        failure="recovery retirement Schedule totality insertion point did not match exactly once",
    )
    _replace_routine_fragment(
        "enforce_actual_realization_basis",
        _ACTUAL_BASE,
        _ACTUAL_RETIREMENT,
        failure="recovery retirement Actual basis insertion point did not match exactly once",
    )
    _replace_routine_fragment(
        "enforce_session_timing_totality",
        _SESSION_BASE,
        _SESSION_RETIREMENT,
        failure="recovery retirement Session totality insertion point did not match exactly once",
    )
    _replace_routine_fragment(
        "enforce_recurrence_aggregate_integrity",
        _RECURRENCE_BASE,
        _RECURRENCE_RETIREMENT,
        failure="recovery retirement Recurrence insertion point did not match exactly once",
    )


def downgrade() -> None:
    """Remove the recovery retirement capability and restore exact pre-CP06 validators."""
    _replace_routine_fragment(
        "enforce_recurrence_aggregate_integrity",
        _RECURRENCE_RETIREMENT,
        _RECURRENCE_BASE,
        failure="recovery retirement Recurrence rollback point did not match exactly once",
    )
    _replace_routine_fragment(
        "enforce_session_timing_totality",
        _SESSION_RETIREMENT,
        _SESSION_BASE,
        failure="recovery retirement Session rollback point did not match exactly once",
    )
    _replace_routine_fragment(
        "enforce_actual_realization_basis",
        _ACTUAL_RETIREMENT,
        _ACTUAL_BASE,
        failure="recovery retirement Actual rollback point did not match exactly once",
    )
    _replace_routine_fragment(
        "enforce_schedule_placement_totality",
        _SCHEDULE_RETIREMENT,
        _SCHEDULE_BASE,
        failure="recovery retirement Schedule rollback point did not match exactly once",
    )

    op.execute(sa.text("DROP TRIGGER ctrg_material_state_retirement_integrity ON dante.material_state_retirement"))
    op.execute(sa.text("DROP FUNCTION dante.enforce_material_state_retirement()"))
    op.drop_table("material_state_retirement", schema=_DANTE_SCHEMA)
