"""Materialize CP6-M05 core integrity routines, triggers and current views.

Revision ID: 20260825_05
Revises: 20260825_04
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260825_05"
down_revision: str | None = "20260825_04"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_DANTE_SCHEMA = "dante"
_RUNTIME_ROLE = "dante_runtime"
_MIGRATOR_ROLE = "dante_migrator"
_OWNER_ROLE = "dante_owner"

_ROUTINES = (
    "enforce_native_address_owner",
    "enforce_scoped_address_owner",
    "enforce_native_ref_eligibility",
    "enforce_material_state_totality",
    "enforce_current_material_state_binding",
    "enforce_current_history_equivalence",
    "enforce_owner_creation_completeness",
    "enforce_schedule_placement_totality",
    "enforce_actual_realization_basis",
    "enforce_session_timing_totality",
    "enforce_session_pause_consistency",
    "enforce_recurrence_aggregate_integrity",
    "validate_iana_timezone",
)

_VIEWS = (
    "schedule_current_placement",
    "actual_current_realization",
    "session_current_timing",
    "routine_current_recurrence",
    "event_current_recurrence",
)

_IMMEDIATE_TRIGGERS = (
    ("trg_native_address_owner_binding", "native_address", "INSERT OR UPDATE OF native_ref, owner_family", "enforce_native_address_owner"),
    ("trg_scoped_address_owner_binding", "scoped_address", "INSERT OR UPDATE OF scoped_ref, scoped_family", "enforce_scoped_address_owner"),
    ("trg_schedule_native_ref", "schedule", "INSERT OR UPDATE OF subject_native_ref", "enforce_native_ref_eligibility"),
    ("trg_actual_native_ref", "actual", "INSERT OR UPDATE OF subject_native_ref", "enforce_native_ref_eligibility"),
    ("trg_native_current_material_state_current_binding", "native_current_material_state", "INSERT OR UPDATE OF native_owner_ref, facet_code, material_state_ref", "enforce_current_material_state_binding"),
    ("trg_scoped_current_material_state_current_binding", "scoped_current_material_state", "INSERT OR UPDATE OF scoped_owner_ref, facet_code, material_state_ref", "enforce_current_material_state_binding"),
    ("trg_actual_realization_timing_actual_basis", "actual_realization_timing", "INSERT OR UPDATE", "enforce_actual_realization_basis"),
    ("trg_actual_realization_session_basis_actual_basis", "actual_realization_session_basis", "INSERT OR UPDATE", "enforce_actual_realization_basis"),
    ("trg_schedule_placement_named_zone_state_iana_timezone", "schedule_placement_named_zone_state", "INSERT OR UPDATE OF extent_code, starts_local_at, ends_local_at, zone_id, resolved_start_at, resolved_end_at", "validate_iana_timezone"),
    ("trg_routine_recurrence_boundary_state_iana_timezone", "routine_recurrence_boundary_state", "INSERT OR UPDATE OF boundary_kind, local_value, zone_id, resolved_at", "validate_iana_timezone"),
    ("trg_event_recurrence_boundary_state_iana_timezone", "event_recurrence_boundary_state", "INSERT OR UPDATE OF boundary_kind, local_value, zone_id, resolved_at", "validate_iana_timezone"),
    ("trg_routine_recurrence_calendar_state_iana_timezone", "routine_recurrence_calendar_state", "INSERT OR UPDATE OF clock_basis_code, zone_id", "validate_iana_timezone"),
    ("trg_event_recurrence_calendar_state_iana_timezone", "event_recurrence_calendar_state", "INSERT OR UPDATE OF clock_basis_code, zone_id", "validate_iana_timezone"),
    ("trg_routine_recurrence_quota_state_iana_timezone", "routine_recurrence_quota_state", "INSERT OR UPDATE OF frame_code, zone_id", "validate_iana_timezone"),
    ("trg_event_recurrence_quota_state_iana_timezone", "event_recurrence_quota_state", "INSERT OR UPDATE OF frame_code, zone_id", "validate_iana_timezone"),
)

_DEFERRED_TRIGGERS = (
    ("ctrg_material_state_address_state_totality", "material_state_address", "INSERT OR UPDATE OR DELETE", "enforce_material_state_totality"),
    ("ctrg_schedule_placement_state_state_totality", "schedule_placement_state", "INSERT OR UPDATE OR DELETE", "enforce_material_state_totality"),
    ("ctrg_actual_realization_state_state_totality", "actual_realization_state", "INSERT OR UPDATE OR DELETE", "enforce_material_state_totality"),
    ("ctrg_session_timing_state_state_totality", "session_timing_state", "INSERT OR UPDATE OR DELETE", "enforce_material_state_totality"),
    ("ctrg_routine_recurrence_state_state_totality", "routine_recurrence_state", "INSERT OR UPDATE OR DELETE", "enforce_material_state_totality"),
    ("ctrg_event_recurrence_state_state_totality", "event_recurrence_state", "INSERT OR UPDATE OR DELETE", "enforce_material_state_totality"),
    ("ctrg_schedule_placement_current_history_current_history", "schedule_placement_current_history", "INSERT OR UPDATE OR DELETE", "enforce_current_history_equivalence"),
    ("ctrg_actual_realization_current_history_current_history", "actual_realization_current_history", "INSERT OR UPDATE OR DELETE", "enforce_current_history_equivalence"),
    ("ctrg_session_timing_current_history_current_history", "session_timing_current_history", "INSERT OR UPDATE OR DELETE", "enforce_current_history_equivalence"),
    ("ctrg_routine_recurrence_current_history_current_history", "routine_recurrence_current_history", "INSERT OR UPDATE OR DELETE", "enforce_current_history_equivalence"),
    ("ctrg_event_recurrence_current_history_current_history", "event_recurrence_current_history", "INSERT OR UPDATE OR DELETE", "enforce_current_history_equivalence"),
    ("ctrg_native_current_material_state_current_history", "native_current_material_state", "INSERT OR UPDATE OR DELETE", "enforce_current_history_equivalence"),
    ("ctrg_scoped_current_material_state_current_history", "scoped_current_material_state", "INSERT OR UPDATE OR DELETE", "enforce_current_history_equivalence"),
    ("ctrg_schedule_owner_complete", "schedule", "INSERT", "enforce_owner_creation_completeness"),
    ("ctrg_actual_owner_complete", "actual", "INSERT", "enforce_owner_creation_completeness"),
    ("ctrg_session_owner_complete", "session", "INSERT", "enforce_owner_creation_completeness"),
    ("ctrg_routine_owner_complete", "routine", "INSERT", "enforce_owner_creation_completeness"),
    ("ctrg_schedule_placement_state_placement_payload", "schedule_placement_state", "INSERT OR UPDATE OR DELETE", "enforce_schedule_placement_totality"),
    ("ctrg_schedule_placement_date_state_placement_payload", "schedule_placement_date_state", "INSERT OR UPDATE OR DELETE", "enforce_schedule_placement_totality"),
    ("ctrg_schedule_placement_floating_local_state_placement_payload", "schedule_placement_floating_local_state", "INSERT OR UPDATE OR DELETE", "enforce_schedule_placement_totality"),
    ("ctrg_schedule_placement_named_zone_state_placement_payload", "schedule_placement_named_zone_state", "INSERT OR UPDATE OR DELETE", "enforce_schedule_placement_totality"),
    ("ctrg_schedule_placement_absolute_state_placement_payload", "schedule_placement_absolute_state", "INSERT OR UPDATE OR DELETE", "enforce_schedule_placement_totality"),
    ("ctrg_session_timing_state_timing_payload", "session_timing_state", "INSERT OR UPDATE OR DELETE", "enforce_session_timing_totality"),
    ("ctrg_session_timing_absolute_timing_payload", "session_timing_absolute", "INSERT OR UPDATE OR DELETE", "enforce_session_timing_totality"),
    ("ctrg_session_timing_elapsed_timing_payload", "session_timing_elapsed", "INSERT OR UPDATE OR DELETE", "enforce_session_timing_totality"),
    ("ctrg_session_timing_pause_pause_consistency", "session_timing_pause", "INSERT OR UPDATE OR DELETE", "enforce_session_pause_consistency"),
    ("ctrg_session_timing_absolute_pause_consistency", "session_timing_absolute", "INSERT OR UPDATE OR DELETE", "enforce_session_pause_consistency"),
    ("ctrg_routine_recurrence_state_recurrence", "routine_recurrence_state", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_event_recurrence_state_recurrence", "event_recurrence_state", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_routine_recurrence_boundary_state_recurrence", "routine_recurrence_boundary_state", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_event_recurrence_boundary_state_recurrence", "event_recurrence_boundary_state", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_routine_recurrence_calendar_state_recurrence", "routine_recurrence_calendar_state", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_event_recurrence_calendar_state_recurrence", "event_recurrence_calendar_state", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_routine_recurrence_calendar_wall_time_recurrence", "routine_recurrence_calendar_wall_time", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_event_recurrence_calendar_wall_time_recurrence", "event_recurrence_calendar_wall_time", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_routine_recurrence_calendar_weekday_recurrence", "routine_recurrence_calendar_weekday", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_event_recurrence_calendar_weekday_recurrence", "event_recurrence_calendar_weekday", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_routine_recurrence_calendar_month_day_recurrence", "routine_recurrence_calendar_month_day", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_event_recurrence_calendar_month_day_recurrence", "event_recurrence_calendar_month_day", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_routine_recurrence_calendar_ordinal_weekday_recurrence", "routine_recurrence_calendar_ordinal_weekday", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_event_recurrence_calendar_ordinal_weekday_recurrence", "event_recurrence_calendar_ordinal_weekday", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_routine_recurrence_calendar_year_month_day_recurrence", "routine_recurrence_calendar_year_month_day", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_event_recurrence_calendar_year_month_day_recurrence", "event_recurrence_calendar_year_month_day", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_routine_recurrence_elapsed_state_recurrence", "routine_recurrence_elapsed_state", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_event_recurrence_elapsed_state_recurrence", "event_recurrence_elapsed_state", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_routine_recurrence_quota_state_recurrence", "routine_recurrence_quota_state", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_event_recurrence_quota_state_recurrence", "event_recurrence_quota_state", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_routine_recurrence_cyclic_state_recurrence", "routine_recurrence_cyclic_state", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_event_recurrence_cyclic_state_recurrence", "event_recurrence_cyclic_state", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_routine_recurrence_cycle_position_recurrence", "routine_recurrence_cycle_position", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
    ("ctrg_event_recurrence_cycle_position_recurrence", "event_recurrence_cycle_position", "INSERT OR UPDATE OR DELETE", "enforce_recurrence_aggregate_integrity"),
)

_CHECK_REPAIRS = (
    (
        "session_timing_absolute",
        "ck_session_timing_absolute_end_precision",
        "(ended_at IS NULL AND end_precision_code IS NULL) OR "
        "(ended_at IS NOT NULL AND end_precision_code IS NOT NULL "
        "AND isfinite(ended_at) "
        "AND end_precision_code IN ('exact','approximate','rounded'))",
        "(ended_at IS NULL AND end_precision_code IS NULL) OR "
        "(ended_at IS NOT NULL AND isfinite(ended_at) "
        "AND end_precision_code IN ('exact','approximate','rounded'))",
    ),
    (
        "routine_recurrence_calendar_state",
        "ck_routine_recurrence_calendar_state_step_unit",
        "(pattern_code='anchor_step' AND step_unit_code IS NOT NULL "
        "AND step_unit_code IN ('day','week','month','year')) OR "
        "(pattern_code<>'anchor_step' AND step_unit_code IS NULL)",
        "(pattern_code='anchor_step' AND step_unit_code IN ('day','week','month','year')) OR "
        "(pattern_code<>'anchor_step' AND step_unit_code IS NULL)",
    ),
    (
        "event_recurrence_calendar_state",
        "ck_event_recurrence_calendar_state_step_unit",
        "(pattern_code='anchor_step' AND step_unit_code IS NOT NULL "
        "AND step_unit_code IN ('day','week','month','year')) OR "
        "(pattern_code<>'anchor_step' AND step_unit_code IS NULL)",
        "(pattern_code='anchor_step' AND step_unit_code IN ('day','week','month','year')) OR "
        "(pattern_code<>'anchor_step' AND step_unit_code IS NULL)",
    ),
    (
        "routine_recurrence_quota_state",
        "ck_routine_recurrence_quota_state_week_start",
        "(period_unit_code='week' AND week_start IS NOT NULL "
        "AND week_start BETWEEN 1 AND 7) OR "
        "(period_unit_code<>'week' AND week_start IS NULL)",
        "(period_unit_code='week' AND week_start BETWEEN 1 AND 7) OR "
        "(period_unit_code<>'week' AND week_start IS NULL)",
    ),
    (
        "event_recurrence_quota_state",
        "ck_event_recurrence_quota_state_week_start",
        "(period_unit_code='week' AND week_start IS NOT NULL "
        "AND week_start BETWEEN 1 AND 7) OR "
        "(period_unit_code<>'week' AND week_start IS NULL)",
        "(period_unit_code='week' AND week_start BETWEEN 1 AND 7) OR "
        "(period_unit_code<>'week' AND week_start IS NULL)",
    ),
    (
        "routine_recurrence_elapsed_state",
        "ck_routine_recurrence_elapsed_state_elapsed_positive",
        "elapsed_seconds NOT IN ('NaN'::numeric,'Infinity'::numeric,'-Infinity'::numeric) "
        "AND elapsed_seconds > 0 AND elapsed_seconds = trunc(elapsed_seconds, 6)",
        "elapsed_seconds NOT IN ('NaN'::numeric,'Infinity'::numeric,'-Infinity'::numeric) "
        "AND elapsed_seconds > 0",
    ),
    (
        "event_recurrence_elapsed_state",
        "ck_event_recurrence_elapsed_state_elapsed_positive",
        "elapsed_seconds NOT IN ('NaN'::numeric,'Infinity'::numeric,'-Infinity'::numeric) "
        "AND elapsed_seconds > 0 AND elapsed_seconds = trunc(elapsed_seconds, 6)",
        "elapsed_seconds NOT IN ('NaN'::numeric,'Infinity'::numeric,'-Infinity'::numeric) "
        "AND elapsed_seconds > 0",
    ),
)


def _sql(statement: str) -> None:
    op.execute(sa.text(statement))


def _replace_checks(*, repaired: bool) -> None:
    for table, name, final_expression, old_expression in _CHECK_REPAIRS:
        expression = final_expression if repaired else old_expression
        _sql(f"ALTER TABLE dante.{table} DROP CONSTRAINT {name}")
        _sql(
            f"ALTER TABLE dante.{table} ADD CONSTRAINT {name} "
            f"CHECK ({expression})"
        )


def _create_routine(name: str, body: str) -> None:
    _sql(
        f"""
        CREATE FUNCTION dante.{name}() RETURNS trigger
        LANGUAGE plpgsql
        SECURITY INVOKER
        VOLATILE
        PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        {body}
        $function$
        """
    )
    _sql(f"ALTER FUNCTION dante.{name}() OWNER TO {_OWNER_ROLE}")
    _sql(
        f"REVOKE ALL PRIVILEGES ON FUNCTION dante.{name}() "
        f"FROM PUBLIC, {_RUNTIME_ROLE}, {_MIGRATOR_ROLE}"
    )


def _create_routines() -> None:
    _create_routine(
        "enforce_native_address_owner",
        r"""
DECLARE
    owner_exists boolean := false;
BEGIN
    CASE NEW.owner_family
        WHEN 'person' THEN SELECT EXISTS (SELECT 1 FROM dante.person WHERE person_ref=NEW.native_ref) INTO owner_exists;
        WHEN 'living_referent' THEN SELECT EXISTS (SELECT 1 FROM dante.living_referent WHERE living_referent_ref=NEW.native_ref) INTO owner_exists;
        WHEN 'asset' THEN SELECT EXISTS (SELECT 1 FROM dante.asset WHERE asset_ref=NEW.native_ref) INTO owner_exists;
        WHEN 'place' THEN SELECT EXISTS (SELECT 1 FROM dante.place WHERE place_ref=NEW.native_ref) INTO owner_exists;
        WHEN 'content_artifact' THEN SELECT EXISTS (SELECT 1 FROM dante.content_artifact WHERE content_artifact_ref=NEW.native_ref) INTO owner_exists;
        WHEN 'collective' THEN SELECT EXISTS (SELECT 1 FROM dante.collective WHERE collective_ref=NEW.native_ref) INTO owner_exists;
        WHEN 'possibility' THEN SELECT EXISTS (SELECT 1 FROM dante.possibility WHERE possibility_ref=NEW.native_ref) INTO owner_exists;
        WHEN 'goal' THEN SELECT EXISTS (SELECT 1 FROM dante.goal WHERE goal_ref=NEW.native_ref) INTO owner_exists;
        WHEN 'plan' THEN SELECT EXISTS (SELECT 1 FROM dante.plan WHERE plan_ref=NEW.native_ref) INTO owner_exists;
        WHEN 'activity' THEN SELECT EXISTS (SELECT 1 FROM dante.activity WHERE activity_ref=NEW.native_ref) INTO owner_exists;
        WHEN 'event' THEN SELECT EXISTS (SELECT 1 FROM dante.event WHERE event_ref=NEW.native_ref) INTO owner_exists;
        WHEN 'routine' THEN SELECT EXISTS (SELECT 1 FROM dante.routine WHERE routine_ref=NEW.native_ref) INTO owner_exists;
        WHEN 'occurrence' THEN SELECT EXISTS (SELECT 1 FROM dante.occurrence WHERE occurrence_ref=NEW.native_ref) INTO owner_exists;
        WHEN 'session' THEN SELECT EXISTS (SELECT 1 FROM dante.session WHERE session_ref=NEW.native_ref) INTO owner_exists;
        WHEN 'observation' THEN SELECT EXISTS (SELECT 1 FROM dante.observation WHERE observation_ref=NEW.native_ref) INTO owner_exists;
        ELSE owner_exists := false;
    END CASE;
    IF NOT owner_exists THEN
        RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='native address owner binding rejected', DETAIL='native address must resolve to the declared bounded owner family';
    END IF;
    RETURN NEW;
END;
""",
    )
    _create_routine(
        "enforce_scoped_address_owner",
        r"""
DECLARE
    owner_exists boolean := false;
BEGIN
    CASE NEW.scoped_family
        WHEN 'schedule' THEN SELECT EXISTS (SELECT 1 FROM dante.schedule WHERE schedule_ref=NEW.scoped_ref) INTO owner_exists;
        WHEN 'actual' THEN SELECT EXISTS (SELECT 1 FROM dante.actual WHERE actual_ref=NEW.scoped_ref) INTO owner_exists;
        ELSE owner_exists := false;
    END CASE;
    IF NOT owner_exists THEN
        RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='scoped address owner binding rejected', DETAIL='scoped address must resolve to the declared bounded owner family';
    END IF;
    RETURN NEW;
END;
""",
    )
    _create_routine(
        "enforce_native_ref_eligibility",
        r"""
DECLARE
    ref_value uuid;
    family text;
    admitted boolean := false;
BEGIN
    IF TG_TABLE_NAME='schedule' THEN
        ref_value := NEW.subject_native_ref;
    ELSIF TG_TABLE_NAME='actual' THEN
        ref_value := NEW.subject_native_ref;
    ELSIF TG_TABLE_NAME='occurrence_generation' THEN
        ref_value := NEW.source_native_ref;
    ELSE
        RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='native reference consumer is not in the bounded dispatcher';
    END IF;
    SELECT owner_family INTO family FROM dante.native_address WHERE native_ref=ref_value;
    IF TG_TABLE_NAME IN ('schedule','actual') THEN
        admitted := family IN ('activity','event','occurrence');
    ELSE
        admitted := family IN ('routine','event');
    END IF;
    IF family IS NULL OR NOT admitted THEN
        RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='native reference family rejected', DETAIL='consumer admits only its frozen NativeRef owner families';
    END IF;
    RETURN NEW;
END;
""",
    )
    _create_routine(
        "enforce_material_state_totality",
        r"""
DECLARE
    state_ref uuid;
    a record;
    schedule_n integer; actual_n integer; session_n integer; routine_n integer; event_n integer;
    owner_ok boolean := false;
BEGIN
    state_ref := CASE WHEN TG_OP='DELETE' THEN OLD.material_state_ref ELSE NEW.material_state_ref END;
    SELECT material_state_ref,native_owner_ref,scoped_owner_ref,facet_code INTO a
      FROM dante.material_state_address WHERE material_state_ref=state_ref;
    IF NOT FOUND THEN
        IF TG_OP='DELETE' THEN RETURN OLD; END IF; RETURN NEW;
    END IF;
    SELECT (SELECT count(*) FROM dante.schedule_placement_state WHERE material_state_ref=state_ref),
           (SELECT count(*) FROM dante.actual_realization_state WHERE material_state_ref=state_ref),
           (SELECT count(*) FROM dante.session_timing_state WHERE material_state_ref=state_ref),
           (SELECT count(*) FROM dante.routine_recurrence_state WHERE material_state_ref=state_ref),
           (SELECT count(*) FROM dante.event_recurrence_state WHERE material_state_ref=state_ref)
      INTO schedule_n,actual_n,session_n,routine_n,event_n;

    IF a.facet_code='schedule.placement' THEN
        SELECT EXISTS (SELECT 1 FROM dante.schedule_placement_state s JOIN dante.scoped_address x ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='schedule' WHERE s.material_state_ref=state_ref AND s.schedule_ref=a.scoped_owner_ref AND a.native_owner_ref IS NULL) INTO owner_ok;
        owner_ok := owner_ok AND schedule_n=1 AND actual_n+session_n+routine_n+event_n=0;
    ELSIF a.facet_code='actual.realization' THEN
        SELECT EXISTS (SELECT 1 FROM dante.actual_realization_state s JOIN dante.scoped_address x ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='actual' WHERE s.material_state_ref=state_ref AND s.actual_ref=a.scoped_owner_ref AND a.native_owner_ref IS NULL) INTO owner_ok;
        owner_ok := owner_ok AND actual_n=1 AND schedule_n+session_n+routine_n+event_n=0;
    ELSIF a.facet_code='session.timing' THEN
        SELECT EXISTS (SELECT 1 FROM dante.session_timing_state s JOIN dante.native_address x ON x.native_ref=a.native_owner_ref AND x.owner_family='session' WHERE s.material_state_ref=state_ref AND s.session_ref=a.native_owner_ref AND a.scoped_owner_ref IS NULL) INTO owner_ok;
        owner_ok := owner_ok AND session_n=1 AND schedule_n+actual_n+routine_n+event_n=0;
    ELSIF a.facet_code='routine.recurrence' THEN
        SELECT EXISTS (SELECT 1 FROM dante.routine_recurrence_state s JOIN dante.native_address x ON x.native_ref=a.native_owner_ref AND x.owner_family='routine' WHERE s.material_state_ref=state_ref AND s.routine_ref=a.native_owner_ref AND a.scoped_owner_ref IS NULL) INTO owner_ok;
        owner_ok := owner_ok AND routine_n=1 AND schedule_n+actual_n+session_n+event_n=0;
    ELSIF a.facet_code='event.recurrence' THEN
        SELECT EXISTS (SELECT 1 FROM dante.event_recurrence_state s JOIN dante.native_address x ON x.native_ref=a.native_owner_ref AND x.owner_family='event' WHERE s.material_state_ref=state_ref AND s.event_ref=a.native_owner_ref AND a.scoped_owner_ref IS NULL) INTO owner_ok;
        owner_ok := owner_ok AND event_n=1 AND schedule_n+actual_n+session_n+routine_n=0;
    END IF;
    IF NOT owner_ok THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='material state totality rejected', DETAIL='MaterialState address, bounded owner family, facet and payload must form one exact live state';
    END IF;
    IF TG_OP='DELETE' THEN RETURN OLD; END IF; RETURN NEW;
END;
""",
    )
    _create_routine(
        "enforce_current_material_state_binding",
        r"""
DECLARE
    ok boolean;
BEGIN
    IF TG_TABLE_NAME='native_current_material_state' THEN
        SELECT EXISTS (
            SELECT 1 FROM dante.material_state_address a
            WHERE a.material_state_ref=NEW.material_state_ref
              AND a.native_owner_ref=NEW.native_owner_ref
              AND a.scoped_owner_ref IS NULL
              AND a.facet_code=NEW.facet_code
        ) INTO ok;
    ELSE
        SELECT EXISTS (
            SELECT 1 FROM dante.material_state_address a
            WHERE a.material_state_ref=NEW.material_state_ref
              AND a.scoped_owner_ref=NEW.scoped_owner_ref
              AND a.native_owner_ref IS NULL
              AND a.facet_code=NEW.facet_code
        ) INTO ok;
    END IF;
    IF NOT ok THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='current material-state binding rejected', DETAIL='current binding must select a MaterialState in the same owner address space and facet';
    END IF;
    RETURN NEW;
END;
""",
    )
    _create_routine(
        "enforce_current_history_equivalence",
        r"""
DECLARE
    owner_ref uuid;
    facet text;
    history_table text;
    overlap_exists boolean := false;
    open_count integer := 0;
    current_state uuid;
    open_state uuid;
BEGIN
    IF TG_TABLE_NAME LIKE '%_current_history' THEN
        IF TG_OP='INSERT' AND NEW.current_until_at IS NOT NULL THEN
            RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                MESSAGE='current-history insert rejected', DETAIL='a currentness episode must begin open';
        END IF;
        IF TG_OP='UPDATE' THEN
            IF TG_TABLE_NAME='schedule_placement_current_history' AND
               (NEW.schedule_ref IS DISTINCT FROM OLD.schedule_ref OR NEW.material_state_ref IS DISTINCT FROM OLD.material_state_ref OR NEW.current_from_at IS DISTINCT FROM OLD.current_from_at) THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA, MESSAGE='current-history identity mutation rejected';
            ELSIF TG_TABLE_NAME='actual_realization_current_history' AND
               (NEW.actual_ref IS DISTINCT FROM OLD.actual_ref OR NEW.material_state_ref IS DISTINCT FROM OLD.material_state_ref OR NEW.current_from_at IS DISTINCT FROM OLD.current_from_at) THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA, MESSAGE='current-history identity mutation rejected';
            ELSIF TG_TABLE_NAME='session_timing_current_history' AND
               (NEW.session_ref IS DISTINCT FROM OLD.session_ref OR NEW.material_state_ref IS DISTINCT FROM OLD.material_state_ref OR NEW.current_from_at IS DISTINCT FROM OLD.current_from_at) THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA, MESSAGE='current-history identity mutation rejected';
            ELSIF TG_TABLE_NAME='routine_recurrence_current_history' AND
               (NEW.routine_ref IS DISTINCT FROM OLD.routine_ref OR NEW.material_state_ref IS DISTINCT FROM OLD.material_state_ref OR NEW.current_from_at IS DISTINCT FROM OLD.current_from_at) THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA, MESSAGE='current-history identity mutation rejected';
            ELSIF TG_TABLE_NAME='event_recurrence_current_history' AND
               (NEW.event_ref IS DISTINCT FROM OLD.event_ref OR NEW.material_state_ref IS DISTINCT FROM OLD.material_state_ref OR NEW.current_from_at IS DISTINCT FROM OLD.current_from_at) THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA, MESSAGE='current-history identity mutation rejected';
            END IF;
            IF OLD.current_until_at IS NOT NULL AND NEW.current_until_at IS DISTINCT FROM OLD.current_until_at THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='current-history closure mutation rejected', DETAIL='a closed currentness episode cannot be reopened or moved';
            END IF;
            IF OLD.current_until_at IS NULL AND NEW.current_until_at IS NOT NULL AND
               (NOT isfinite(NEW.current_until_at) OR NEW.current_until_at<=NEW.current_from_at) THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA, MESSAGE='current-history closure rejected';
            END IF;
        END IF;
    END IF;

    IF TG_TABLE_NAME='schedule_placement_current_history' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.schedule_ref ELSE NEW.schedule_ref END; facet:='schedule.placement'; history_table:='schedule';
    ELSIF TG_TABLE_NAME='actual_realization_current_history' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.actual_ref ELSE NEW.actual_ref END; facet:='actual.realization'; history_table:='actual';
    ELSIF TG_TABLE_NAME='session_timing_current_history' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.session_ref ELSE NEW.session_ref END; facet:='session.timing'; history_table:='session';
    ELSIF TG_TABLE_NAME='routine_recurrence_current_history' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.routine_ref ELSE NEW.routine_ref END; facet:='routine.recurrence'; history_table:='routine';
    ELSIF TG_TABLE_NAME='event_recurrence_current_history' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.event_ref ELSE NEW.event_ref END; facet:='event.recurrence'; history_table:='event';
    ELSIF TG_TABLE_NAME='native_current_material_state' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.native_owner_ref ELSE NEW.native_owner_ref END; facet:=CASE WHEN TG_OP='DELETE' THEN OLD.facet_code ELSE NEW.facet_code END; history_table:=split_part(facet,'.',1);
    ELSE owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.scoped_owner_ref ELSE NEW.scoped_owner_ref END; facet:=CASE WHEN TG_OP='DELETE' THEN OLD.facet_code ELSE NEW.facet_code END; history_table:=split_part(facet,'.',1);
    END IF;

    IF history_table='schedule' THEN
        SELECT EXISTS (SELECT 1 FROM dante.schedule_placement_current_history a JOIN dante.schedule_placement_current_history b ON a.schedule_ref=b.schedule_ref AND (a.schedule_ref,a.current_from_at)<>(b.schedule_ref,b.current_from_at) WHERE a.schedule_ref=owner_ref AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at) AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)) INTO overlap_exists;
        SELECT count(*) INTO open_count FROM dante.schedule_placement_current_history WHERE schedule_ref=owner_ref AND current_until_at IS NULL; SELECT material_state_ref INTO open_state FROM dante.schedule_placement_current_history WHERE schedule_ref=owner_ref AND current_until_at IS NULL LIMIT 1;
        SELECT material_state_ref INTO current_state FROM dante.scoped_current_material_state WHERE scoped_owner_ref=owner_ref AND facet_code=facet;
    ELSIF history_table='actual' THEN
        SELECT EXISTS (SELECT 1 FROM dante.actual_realization_current_history a JOIN dante.actual_realization_current_history b ON a.actual_ref=b.actual_ref AND (a.actual_ref,a.current_from_at)<>(b.actual_ref,b.current_from_at) WHERE a.actual_ref=owner_ref AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at) AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)) INTO overlap_exists;
        SELECT count(*) INTO open_count FROM dante.actual_realization_current_history WHERE actual_ref=owner_ref AND current_until_at IS NULL; SELECT material_state_ref INTO open_state FROM dante.actual_realization_current_history WHERE actual_ref=owner_ref AND current_until_at IS NULL LIMIT 1;
        SELECT material_state_ref INTO current_state FROM dante.scoped_current_material_state WHERE scoped_owner_ref=owner_ref AND facet_code=facet;
    ELSIF history_table='session' THEN
        SELECT EXISTS (SELECT 1 FROM dante.session_timing_current_history a JOIN dante.session_timing_current_history b ON a.session_ref=b.session_ref AND (a.session_ref,a.current_from_at)<>(b.session_ref,b.current_from_at) WHERE a.session_ref=owner_ref AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at) AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)) INTO overlap_exists;
        SELECT count(*) INTO open_count FROM dante.session_timing_current_history WHERE session_ref=owner_ref AND current_until_at IS NULL; SELECT material_state_ref INTO open_state FROM dante.session_timing_current_history WHERE session_ref=owner_ref AND current_until_at IS NULL LIMIT 1;
        SELECT material_state_ref INTO current_state FROM dante.native_current_material_state WHERE native_owner_ref=owner_ref AND facet_code=facet;
    ELSIF history_table='routine' THEN
        SELECT EXISTS (SELECT 1 FROM dante.routine_recurrence_current_history a JOIN dante.routine_recurrence_current_history b ON a.routine_ref=b.routine_ref AND (a.routine_ref,a.current_from_at)<>(b.routine_ref,b.current_from_at) WHERE a.routine_ref=owner_ref AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at) AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)) INTO overlap_exists;
        SELECT count(*) INTO open_count FROM dante.routine_recurrence_current_history WHERE routine_ref=owner_ref AND current_until_at IS NULL; SELECT material_state_ref INTO open_state FROM dante.routine_recurrence_current_history WHERE routine_ref=owner_ref AND current_until_at IS NULL LIMIT 1;
        SELECT material_state_ref INTO current_state FROM dante.native_current_material_state WHERE native_owner_ref=owner_ref AND facet_code=facet;
    ELSIF history_table='event' THEN
        SELECT EXISTS (SELECT 1 FROM dante.event_recurrence_current_history a JOIN dante.event_recurrence_current_history b ON a.event_ref=b.event_ref AND (a.event_ref,a.current_from_at)<>(b.event_ref,b.current_from_at) WHERE a.event_ref=owner_ref AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at) AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)) INTO overlap_exists;
        SELECT count(*) INTO open_count FROM dante.event_recurrence_current_history WHERE event_ref=owner_ref AND current_until_at IS NULL; SELECT material_state_ref INTO open_state FROM dante.event_recurrence_current_history WHERE event_ref=owner_ref AND current_until_at IS NULL LIMIT 1;
        SELECT material_state_ref INTO current_state FROM dante.native_current_material_state WHERE native_owner_ref=owner_ref AND facet_code=facet;
    ELSE
        IF TG_OP='DELETE' THEN RETURN OLD; END IF; RETURN NEW;
    END IF;

    IF overlap_exists OR open_count>1 OR current_state IS DISTINCT FROM open_state OR ((current_state IS NULL) <> (open_count=0)) THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='current-history equivalence rejected', DETAIL='history episodes must not overlap and the sole open episode must equal the current binding';
    END IF;
    IF TG_OP='DELETE' THEN RETURN OLD; END IF; RETURN NEW;
END;
""",
    )
    _create_routine(
        "enforce_owner_creation_completeness",
        r"""
DECLARE
    owner_ref uuid;
    ok boolean := false;
BEGIN
    IF TG_TABLE_NAME='schedule' THEN owner_ref:=NEW.schedule_ref; SELECT EXISTS (SELECT 1 FROM dante.scoped_current_material_state WHERE scoped_owner_ref=owner_ref AND facet_code='schedule.placement') INTO ok;
    ELSIF TG_TABLE_NAME='actual' THEN owner_ref:=NEW.actual_ref; SELECT EXISTS (SELECT 1 FROM dante.scoped_current_material_state WHERE scoped_owner_ref=owner_ref AND facet_code='actual.realization') INTO ok;
    ELSIF TG_TABLE_NAME='session' THEN owner_ref:=NEW.session_ref; SELECT EXISTS (SELECT 1 FROM dante.native_current_material_state WHERE native_owner_ref=owner_ref AND facet_code='session.timing') INTO ok;
    ELSIF TG_TABLE_NAME='routine' THEN owner_ref:=NEW.routine_ref; SELECT EXISTS (SELECT 1 FROM dante.native_current_material_state WHERE native_owner_ref=owner_ref AND facet_code='routine.recurrence') INTO ok;
    ELSIF TG_TABLE_NAME='occurrence' THEN owner_ref:=NEW.occurrence_ref; SELECT EXISTS (SELECT 1 FROM dante.occurrence_generation WHERE occurrence_ref=owner_ref) INTO ok;
    ELSE ok:=false;
    END IF;
    IF NOT ok THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='semantic owner creation incomplete', DETAIL='the owner requires its frozen companion/current contract by commit';
    END IF;
    RETURN NEW;
END;
""",
    )
    _create_routine(
        "enforce_schedule_placement_totality",
        r"""
DECLARE
    state_ref uuid;
    form text;
    date_n int; floating_n int; named_n int; absolute_n int;
BEGIN
    state_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.material_state_ref ELSE NEW.material_state_ref END;
    SELECT temporal_form_code INTO form FROM dante.schedule_placement_state WHERE material_state_ref=state_ref;
    IF NOT FOUND THEN IF TG_OP='DELETE' THEN RETURN OLD; END IF; RETURN NEW; END IF;
    SELECT (SELECT count(*) FROM dante.schedule_placement_date_state WHERE material_state_ref=state_ref),
           (SELECT count(*) FROM dante.schedule_placement_floating_local_state WHERE material_state_ref=state_ref),
           (SELECT count(*) FROM dante.schedule_placement_named_zone_state WHERE material_state_ref=state_ref),
           (SELECT count(*) FROM dante.schedule_placement_absolute_state WHERE material_state_ref=state_ref)
      INTO date_n,floating_n,named_n,absolute_n;
    IF date_n+floating_n+named_n+absolute_n<>1 OR
       (form='date_span' AND date_n<>1) OR (form='floating_local' AND floating_n<>1) OR
       (form='named_zone_local' AND named_n<>1) OR (form='absolute' AND absolute_n<>1) THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='Schedule placement payload rejected', DETAIL='exactly one typed payload must match temporal_form_code';
    END IF;
    IF TG_OP='DELETE' THEN RETURN OLD; END IF; RETURN NEW;
END;
""",
    )
    _create_routine(
        "enforce_actual_realization_basis",
        r"""
DECLARE
    state_ref uuid;
    occurred boolean;
    ok boolean := true;
BEGIN
    IF TG_TABLE_NAME='actual_realization_timing' THEN state_ref:=NEW.material_state_ref; ELSE state_ref:=NEW.actual_material_state_ref; END IF;
    SELECT realization_occurred INTO occurred FROM dante.actual_realization_state WHERE material_state_ref=state_ref;
    IF occurred IS DISTINCT FROM true THEN ok:=false; END IF;
    IF ok AND TG_TABLE_NAME='actual_realization_session_basis' THEN
        SELECT EXISTS (
          SELECT 1 FROM dante.session_timing_state s
          JOIN dante.material_state_address a ON a.material_state_ref=s.material_state_ref
          WHERE s.material_state_ref=NEW.session_timing_material_state_ref
            AND s.session_ref=NEW.session_ref
            AND a.native_owner_ref=NEW.session_ref AND a.scoped_owner_ref IS NULL AND a.facet_code='session.timing'
        ) INTO ok;
    END IF;
    IF NOT ok THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='Actual realization basis rejected', DETAIL='timing/basis require a realized state and exact historical Session timing-state ownership';
    END IF;
    RETURN NEW;
END;
""",
    )
    _create_routine(
        "enforce_session_timing_totality",
        r"""
DECLARE state_ref uuid; form text; absolute_n int; elapsed_n int;
BEGIN
    state_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.material_state_ref ELSE NEW.material_state_ref END;
    SELECT timing_form_code INTO form FROM dante.session_timing_state WHERE material_state_ref=state_ref;
    IF NOT FOUND THEN IF TG_OP='DELETE' THEN RETURN OLD; END IF; RETURN NEW; END IF;
    SELECT (SELECT count(*) FROM dante.session_timing_absolute WHERE material_state_ref=state_ref),
           (SELECT count(*) FROM dante.session_timing_elapsed WHERE material_state_ref=state_ref)
      INTO absolute_n,elapsed_n;
    IF absolute_n+elapsed_n<>1 OR (form='absolute' AND absolute_n<>1) OR (form='elapsed_only' AND elapsed_n<>1) THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='Session timing payload rejected', DETAIL='exactly one typed timing payload must match timing_form_code';
    END IF;
    IF TG_OP='DELETE' THEN RETURN OLD; END IF; RETURN NEW;
END;
""",
    )
    _create_routine(
        "enforce_session_pause_consistency",
        r"""
DECLARE state_ref uuid; started timestamptz; ended timestamptz; bad boolean;
BEGIN
    state_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.material_state_ref ELSE NEW.material_state_ref END;
    SELECT started_at,ended_at INTO started,ended FROM dante.session_timing_absolute WHERE material_state_ref=state_ref;
    IF NOT FOUND THEN IF TG_OP='DELETE' THEN RETURN OLD; END IF; RETURN NEW; END IF;
    SELECT EXISTS (
      SELECT 1 FROM dante.session_timing_pause p
      WHERE p.material_state_ref=state_ref AND (
        p.paused_at < started OR
        (ended IS NOT NULL AND (p.paused_at>=ended OR p.resumed_at IS NULL OR p.resumed_at>ended))
      )
    ) OR EXISTS (
      SELECT 1 FROM dante.session_timing_pause a
      JOIN dante.session_timing_pause b ON a.material_state_ref=b.material_state_ref AND a.paused_at<b.paused_at
      WHERE a.material_state_ref=state_ref AND (a.resumed_at IS NULL OR a.resumed_at>b.paused_at)
    ) INTO bad;
    IF bad THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='Session pause consistency rejected', DETAIL='pause intervals must be contained, non-overlapping and no pause may remain open after Session end';
    END IF;
    IF TG_OP='DELETE' THEN RETURN OLD; END IF; RETURN NEW;
END;
""",
    )
    _create_routine(
        "enforce_recurrence_aggregate_integrity",
        r"""
DECLARE
    state_ref uuid;
    prefix text;
    family text; range_kind_value text; expected_n int;
    calendar_n int; elapsed_n int; quota_n int; cyclic_n int;
    pattern text; interval_n int; clock_basis text; step_unit text;
    weekday_n int; monthday_n int; ordinal_n int; yearmonthday_n int; walltime_n int;
    pattern_anchor_n int; effective_from_n int; effective_until_n int;
    anchor_kind text; anchor_date date;
    from_kind text; until_kind text; from_zone text; until_zone text;
    from_inclusive boolean; until_inclusive boolean;
    from_date date; until_date date; from_local timestamp; until_local timestamp;
    from_instant timestamptz; until_instant timestamptz;
    calendar_zone text;
    period_unit text; period_span_value int; week_start_value int;
    cycle_length_value int; position_n int; min_pos int; max_pos int;
    bad boolean := false;
BEGIN
    state_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.material_state_ref ELSE NEW.material_state_ref END;
    IF TG_TABLE_NAME LIKE 'routine_recurrence_%' THEN prefix:='routine'; ELSE prefix:='event'; END IF;

    IF prefix='routine' THEN
      SELECT family_code,range_kind,expected_occurrence_count INTO family,range_kind_value,expected_n FROM dante.routine_recurrence_state WHERE material_state_ref=state_ref;
      IF NOT FOUND THEN IF TG_OP='DELETE' THEN RETURN OLD; END IF; RETURN NEW; END IF;
      SELECT (SELECT count(*) FROM dante.routine_recurrence_calendar_state WHERE material_state_ref=state_ref),
             (SELECT count(*) FROM dante.routine_recurrence_elapsed_state WHERE material_state_ref=state_ref),
             (SELECT count(*) FROM dante.routine_recurrence_quota_state WHERE material_state_ref=state_ref),
             (SELECT count(*) FROM dante.routine_recurrence_cyclic_state WHERE material_state_ref=state_ref),
             (SELECT count(*) FROM dante.routine_recurrence_boundary_state WHERE material_state_ref=state_ref AND boundary_role='pattern_anchor'),
             (SELECT count(*) FROM dante.routine_recurrence_boundary_state WHERE material_state_ref=state_ref AND boundary_role='effective_from'),
             (SELECT count(*) FROM dante.routine_recurrence_boundary_state WHERE material_state_ref=state_ref AND boundary_role='effective_until')
        INTO calendar_n,elapsed_n,quota_n,cyclic_n,pattern_anchor_n,effective_from_n,effective_until_n;
    ELSE
      SELECT family_code,range_kind,expected_occurrence_count INTO family,range_kind_value,expected_n FROM dante.event_recurrence_state WHERE material_state_ref=state_ref;
      IF NOT FOUND THEN IF TG_OP='DELETE' THEN RETURN OLD; END IF; RETURN NEW; END IF;
      SELECT (SELECT count(*) FROM dante.event_recurrence_calendar_state WHERE material_state_ref=state_ref),
             (SELECT count(*) FROM dante.event_recurrence_elapsed_state WHERE material_state_ref=state_ref),
             (SELECT count(*) FROM dante.event_recurrence_quota_state WHERE material_state_ref=state_ref),
             (SELECT count(*) FROM dante.event_recurrence_cyclic_state WHERE material_state_ref=state_ref),
             (SELECT count(*) FROM dante.event_recurrence_boundary_state WHERE material_state_ref=state_ref AND boundary_role='pattern_anchor'),
             (SELECT count(*) FROM dante.event_recurrence_boundary_state WHERE material_state_ref=state_ref AND boundary_role='effective_from'),
             (SELECT count(*) FROM dante.event_recurrence_boundary_state WHERE material_state_ref=state_ref AND boundary_role='effective_until')
        INTO calendar_n,elapsed_n,quota_n,cyclic_n,pattern_anchor_n,effective_from_n,effective_until_n;
    END IF;
    IF calendar_n+elapsed_n+quota_n+cyclic_n<>1 OR
       (family='calendar_wall_clock' AND calendar_n<>1) OR (family='elapsed_interval' AND elapsed_n<>1) OR
       (family='quota_per_period' AND quota_n<>1) OR (family='cyclic_positional' AND cyclic_n<>1) THEN bad:=true; END IF;
    IF range_kind_value='until_boundary' AND effective_until_n<>1 THEN bad:=true;
    ELSIF range_kind_value IN ('open','expected_count') AND effective_until_n<>0 THEN bad:=true; END IF;
    IF range_kind_value='expected_count' AND (family='quota_per_period' OR effective_from_n<>1 OR expected_n IS NULL OR expected_n<=0) THEN bad:=true; END IF;

    IF prefix='routine' THEN
      SELECT boundary_kind,zone_id,inclusive,date_value,local_value,instant_value INTO from_kind,from_zone,from_inclusive,from_date,from_local,from_instant FROM dante.routine_recurrence_boundary_state WHERE material_state_ref=state_ref AND boundary_role='effective_from';
      SELECT boundary_kind,zone_id,inclusive,date_value,local_value,instant_value INTO until_kind,until_zone,until_inclusive,until_date,until_local,until_instant FROM dante.routine_recurrence_boundary_state WHERE material_state_ref=state_ref AND boundary_role='effective_until';
    ELSE
      SELECT boundary_kind,zone_id,inclusive,date_value,local_value,instant_value INTO from_kind,from_zone,from_inclusive,from_date,from_local,from_instant FROM dante.event_recurrence_boundary_state WHERE material_state_ref=state_ref AND boundary_role='effective_from';
      SELECT boundary_kind,zone_id,inclusive,date_value,local_value,instant_value INTO until_kind,until_zone,until_inclusive,until_date,until_local,until_instant FROM dante.event_recurrence_boundary_state WHERE material_state_ref=state_ref AND boundary_role='effective_until';
    END IF;
    IF effective_from_n=1 AND effective_until_n=1 AND from_kind IS DISTINCT FROM until_kind THEN bad:=true; END IF;
    IF effective_from_n=1 AND effective_until_n=1 AND from_kind=until_kind THEN
      IF from_kind='date' AND (from_date>until_date OR (from_date=until_date AND NOT (from_inclusive AND until_inclusive))) THEN bad:=true;
      ELSIF from_kind IN ('floating_local','named_zone_local') AND (from_local>until_local OR (from_local=until_local AND NOT (from_inclusive AND until_inclusive))) THEN bad:=true;
      ELSIF from_kind='absolute_instant' AND (from_instant>until_instant OR (from_instant=until_instant AND NOT (from_inclusive AND until_inclusive))) THEN bad:=true; END IF;
    END IF;

    IF family='calendar_wall_clock' THEN
      IF prefix='routine' THEN
        SELECT pattern_code,interval_count,clock_basis_code,step_unit_code INTO pattern,interval_n,clock_basis,step_unit FROM dante.routine_recurrence_calendar_state WHERE material_state_ref=state_ref;
        SELECT (SELECT count(*) FROM dante.routine_recurrence_calendar_weekday WHERE material_state_ref=state_ref),(SELECT count(*) FROM dante.routine_recurrence_calendar_month_day WHERE material_state_ref=state_ref),(SELECT count(*) FROM dante.routine_recurrence_calendar_ordinal_weekday WHERE material_state_ref=state_ref),(SELECT count(*) FROM dante.routine_recurrence_calendar_year_month_day WHERE material_state_ref=state_ref),(SELECT count(*) FROM dante.routine_recurrence_calendar_wall_time WHERE material_state_ref=state_ref) INTO weekday_n,monthday_n,ordinal_n,yearmonthday_n,walltime_n;
        SELECT boundary_kind,date_value INTO anchor_kind,anchor_date FROM dante.routine_recurrence_boundary_state WHERE material_state_ref=state_ref AND boundary_role='pattern_anchor';
      ELSE
        SELECT pattern_code,interval_count,clock_basis_code,step_unit_code INTO pattern,interval_n,clock_basis,step_unit FROM dante.event_recurrence_calendar_state WHERE material_state_ref=state_ref;
        SELECT (SELECT count(*) FROM dante.event_recurrence_calendar_weekday WHERE material_state_ref=state_ref),(SELECT count(*) FROM dante.event_recurrence_calendar_month_day WHERE material_state_ref=state_ref),(SELECT count(*) FROM dante.event_recurrence_calendar_ordinal_weekday WHERE material_state_ref=state_ref),(SELECT count(*) FROM dante.event_recurrence_calendar_year_month_day WHERE material_state_ref=state_ref),(SELECT count(*) FROM dante.event_recurrence_calendar_wall_time WHERE material_state_ref=state_ref) INTO weekday_n,monthday_n,ordinal_n,yearmonthday_n,walltime_n;
        SELECT boundary_kind,date_value INTO anchor_kind,anchor_date FROM dante.event_recurrence_boundary_state WHERE material_state_ref=state_ref AND boundary_role='pattern_anchor';
      END IF;
      IF prefix='routine' THEN SELECT zone_id INTO calendar_zone FROM dante.routine_recurrence_calendar_state WHERE material_state_ref=state_ref; ELSE SELECT zone_id INTO calendar_zone FROM dante.event_recurrence_calendar_state WHERE material_state_ref=state_ref; END IF;
      IF effective_from_n=1 THEN
        IF clock_basis='floating_local' AND from_kind NOT IN ('date','floating_local') THEN bad:=true;
        ELSIF clock_basis='named_zone' AND from_kind NOT IN ('date','named_zone_local','absolute_instant') THEN bad:=true;
        ELSIF clock_basis='absolute_utc' AND from_kind NOT IN ('date','absolute_instant') THEN bad:=true; END IF;
        IF walltime_n=0 AND from_kind<>'date' THEN bad:=true; END IF;
        IF from_kind='named_zone_local' AND from_zone IS DISTINCT FROM calendar_zone THEN bad:=true; END IF;
      END IF;
      IF effective_until_n=1 THEN
        IF clock_basis='floating_local' AND until_kind NOT IN ('date','floating_local') THEN bad:=true;
        ELSIF clock_basis='named_zone' AND until_kind NOT IN ('date','named_zone_local','absolute_instant') THEN bad:=true;
        ELSIF clock_basis='absolute_utc' AND until_kind NOT IN ('date','absolute_instant') THEN bad:=true; END IF;
        IF walltime_n=0 AND until_kind<>'date' THEN bad:=true; END IF;
        IF until_kind='named_zone_local' AND until_zone IS DISTINCT FROM calendar_zone THEN bad:=true; END IF;
      END IF;
      IF pattern='daily' AND weekday_n+monthday_n+ordinal_n+yearmonthday_n<>0 THEN bad:=true;
      ELSIF pattern='weekly_weekdays' AND (weekday_n<1 OR monthday_n+ordinal_n+yearmonthday_n<>0) THEN bad:=true;
      ELSIF pattern='monthly_month_days' AND (monthday_n<1 OR weekday_n+ordinal_n+yearmonthday_n<>0) THEN bad:=true;
      ELSIF pattern='monthly_ordinal_weekdays' AND (ordinal_n<1 OR weekday_n+monthday_n+yearmonthday_n<>0) THEN bad:=true;
      ELSIF pattern='yearly_month_days' AND (yearmonthday_n<1 OR weekday_n+monthday_n+ordinal_n<>0) THEN bad:=true;
      ELSIF pattern='anchor_step' AND weekday_n+monthday_n+ordinal_n+yearmonthday_n<>0 THEN bad:=true; END IF;
      IF pattern='anchor_step' THEN IF pattern_anchor_n<>1 OR anchor_kind<>'date' THEN bad:=true; END IF;
      ELSE IF interval_n=1 AND pattern_anchor_n<>0 THEN bad:=true; ELSIF interval_n>1 AND (pattern_anchor_n<>1 OR anchor_kind<>'date') THEN bad:=true; END IF; END IF;
    ELSIF family='elapsed_interval' THEN
      IF pattern_anchor_n<>0 THEN bad:=true; END IF;
      IF (effective_from_n=1 AND from_kind<>'absolute_instant') OR (effective_until_n=1 AND until_kind<>'absolute_instant') THEN bad:=true; END IF;
    ELSIF family='quota_per_period' THEN
      IF range_kind_value='expected_count' THEN bad:=true; END IF;
      IF prefix='routine' THEN SELECT period_unit_code,period_span,week_start INTO period_unit,period_span_value,week_start_value FROM dante.routine_recurrence_quota_state WHERE material_state_ref=state_ref; SELECT boundary_kind,date_value INTO anchor_kind,anchor_date FROM dante.routine_recurrence_boundary_state WHERE material_state_ref=state_ref AND boundary_role='pattern_anchor';
      ELSE SELECT period_unit_code,period_span,week_start INTO period_unit,period_span_value,week_start_value FROM dante.event_recurrence_quota_state WHERE material_state_ref=state_ref; SELECT boundary_kind,date_value INTO anchor_kind,anchor_date FROM dante.event_recurrence_boundary_state WHERE material_state_ref=state_ref AND boundary_role='pattern_anchor'; END IF;
      IF period_span_value=1 AND pattern_anchor_n<>0 THEN bad:=true; ELSIF period_span_value>1 AND (pattern_anchor_n<>1 OR anchor_kind<>'date') THEN bad:=true; END IF;
      IF pattern_anchor_n=1 THEN
        IF period_unit='week' AND extract(isodow from anchor_date)::int<>week_start_value THEN bad:=true;
        ELSIF period_unit='month' AND extract(day from anchor_date)::int<>1 THEN bad:=true;
        ELSIF period_unit='year' AND (extract(month from anchor_date)::int<>1 OR extract(day from anchor_date)::int<>1) THEN bad:=true; END IF;
      END IF;
      IF (effective_from_n=1 AND (from_kind<>'date' OR from_inclusive IS DISTINCT FROM true)) OR (effective_until_n=1 AND (until_kind<>'date' OR until_inclusive IS DISTINCT FROM false)) THEN bad:=true; END IF;
      IF effective_from_n=1 THEN
        IF period_unit='week' AND extract(isodow from from_date)::int<>week_start_value THEN bad:=true;
        ELSIF period_unit='month' AND extract(day from from_date)::int<>1 THEN bad:=true;
        ELSIF period_unit='year' AND (extract(month from from_date)::int<>1 OR extract(day from from_date)::int<>1) THEN bad:=true; END IF;
        IF period_span_value>1 THEN
          IF period_unit='day' AND mod((from_date-anchor_date),period_span_value)<>0 THEN bad:=true;
          ELSIF period_unit='week' AND mod((from_date-anchor_date),7*period_span_value)<>0 THEN bad:=true;
          ELSIF period_unit='month' AND mod(((extract(year from from_date)::int-extract(year from anchor_date)::int)*12 + extract(month from from_date)::int-extract(month from anchor_date)::int),period_span_value)<>0 THEN bad:=true;
          ELSIF period_unit='year' AND mod(extract(year from from_date)::int-extract(year from anchor_date)::int,period_span_value)<>0 THEN bad:=true; END IF;
        END IF;
      END IF;
      IF effective_until_n=1 THEN
        IF period_unit='week' AND extract(isodow from until_date)::int<>week_start_value THEN bad:=true;
        ELSIF period_unit='month' AND extract(day from until_date)::int<>1 THEN bad:=true;
        ELSIF period_unit='year' AND (extract(month from until_date)::int<>1 OR extract(day from until_date)::int<>1) THEN bad:=true; END IF;
        IF period_span_value>1 THEN
          IF period_unit='day' AND mod((until_date-anchor_date),period_span_value)<>0 THEN bad:=true;
          ELSIF period_unit='week' AND mod((until_date-anchor_date),7*period_span_value)<>0 THEN bad:=true;
          ELSIF period_unit='month' AND mod(((extract(year from until_date)::int-extract(year from anchor_date)::int)*12 + extract(month from until_date)::int-extract(month from anchor_date)::int),period_span_value)<>0 THEN bad:=true;
          ELSIF period_unit='year' AND mod(extract(year from until_date)::int-extract(year from anchor_date)::int,period_span_value)<>0 THEN bad:=true; END IF;
        END IF;
      END IF;
    ELSIF family='cyclic_positional' THEN
      IF prefix='routine' THEN SELECT cycle_length INTO cycle_length_value FROM dante.routine_recurrence_cyclic_state WHERE material_state_ref=state_ref; SELECT count(*),min(position_index),max(position_index) INTO position_n,min_pos,max_pos FROM dante.routine_recurrence_cycle_position WHERE material_state_ref=state_ref; SELECT boundary_kind INTO anchor_kind FROM dante.routine_recurrence_boundary_state WHERE material_state_ref=state_ref AND boundary_role='pattern_anchor';
      ELSE SELECT cycle_length INTO cycle_length_value FROM dante.event_recurrence_cyclic_state WHERE material_state_ref=state_ref; SELECT count(*),min(position_index),max(position_index) INTO position_n,min_pos,max_pos FROM dante.event_recurrence_cycle_position WHERE material_state_ref=state_ref; SELECT boundary_kind INTO anchor_kind FROM dante.event_recurrence_boundary_state WHERE material_state_ref=state_ref AND boundary_role='pattern_anchor'; END IF;
      IF pattern_anchor_n<>1 OR anchor_kind<>'date' OR position_n<>cycle_length_value OR min_pos<>0 OR max_pos<>cycle_length_value-1 THEN bad:=true; END IF;
      IF (effective_from_n=1 AND from_kind<>'date') OR (effective_until_n=1 AND until_kind<>'date') THEN bad:=true; END IF;
    END IF;
    IF bad THEN
      RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
        MESSAGE='Recurrence aggregate rejected', DETAIL='owner-bound recurrence must satisfy its frozen family, selector, phase, range and cyclic aggregate contract';
    END IF;
    IF TG_OP='DELETE' THEN RETURN OLD; END IF; RETURN NEW;
END;
""",
    )
    _create_routine(
        "validate_iana_timezone",
        r"""
DECLARE zone_value text; local_start timestamp; local_end timestamp; resolved_start timestamptz; resolved_end timestamptz; ok boolean;
BEGIN
    IF TG_TABLE_NAME='schedule_placement_named_zone_state' THEN zone_value:=NEW.zone_id; local_start:=NEW.starts_local_at; local_end:=NEW.ends_local_at; resolved_start:=NEW.resolved_start_at; resolved_end:=NEW.resolved_end_at;
    ELSIF TG_TABLE_NAME IN ('routine_recurrence_boundary_state','event_recurrence_boundary_state') THEN IF NEW.boundary_kind<>'named_zone_local' THEN RETURN NEW; END IF; zone_value:=NEW.zone_id; local_start:=NEW.local_value; resolved_start:=NEW.resolved_at;
    ELSIF TG_TABLE_NAME IN ('routine_recurrence_calendar_state','event_recurrence_calendar_state') THEN IF NEW.clock_basis_code<>'named_zone' THEN RETURN NEW; END IF; zone_value:=NEW.zone_id;
    ELSIF TG_TABLE_NAME IN ('routine_recurrence_quota_state','event_recurrence_quota_state') THEN IF NEW.frame_code<>'named_zone' THEN RETURN NEW; END IF; zone_value:=NEW.zone_id;
    ELSIF TG_TABLE_NAME='occurrence_generation_calendar' THEN IF NEW.clock_basis_code<>'named_zone' THEN RETURN NEW; END IF; zone_value:=NEW.zone_id; IF NEW.generated_wall_time IS NOT NULL THEN local_start:=NEW.generated_date+NEW.generated_wall_time; resolved_start:=NEW.resolved_at; END IF;
    ELSIF TG_TABLE_NAME='occurrence_generation_quota' THEN IF NEW.frame_code<>'named_zone' THEN RETURN NEW; END IF; zone_value:=NEW.zone_id;
    ELSE RETURN NEW; END IF;
    SELECT EXISTS (SELECT 1 FROM pg_catalog.pg_timezone_names WHERE name=zone_value) INTO ok;
    IF NOT ok THEN RAISE EXCEPTION USING ERRCODE='22023', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA, MESSAGE='IANA timezone rejected', DETAIL='zone identifier is not in PostgreSQL tzdb vocabulary'; END IF;
    IF local_start IS NOT NULL AND resolved_start IS NOT NULL AND (resolved_start AT TIME ZONE zone_value) IS DISTINCT FROM local_start THEN
      RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA, MESSAGE='named-zone resolution rejected', DETAIL='resolved instant must round-trip to the stored local coordinate and zone';
    END IF;
    IF local_end IS NOT NULL AND resolved_end IS NOT NULL AND (resolved_end AT TIME ZONE zone_value) IS DISTINCT FROM local_end THEN
      RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA, MESSAGE='named-zone end resolution rejected', DETAIL='resolved end must round-trip to the stored local coordinate and zone';
    END IF;
    RETURN NEW;
END;
""",
    )


def _create_immediate_trigger(name: str, table: str, event_sql: str, routine: str) -> None:
    _sql(
        f"CREATE TRIGGER {name} BEFORE {event_sql} ON dante.{table} "
        f"FOR EACH ROW EXECUTE FUNCTION dante.{routine}()"
    )


def _create_deferred_trigger(name: str, table: str, event_sql: str, routine: str) -> None:
    _sql(
        f"CREATE CONSTRAINT TRIGGER {name} AFTER {event_sql} ON dante.{table} "
        "DEFERRABLE INITIALLY DEFERRED FOR EACH ROW "
        f"EXECUTE FUNCTION dante.{routine}()"
    )


def _create_triggers() -> None:
    if len(_IMMEDIATE_TRIGGERS) != 15 or len(_DEFERRED_TRIGGERS) != 51:
        raise RuntimeError("M5 trigger manifest must be exactly 15 immediate + 51 deferred")
    for item in _IMMEDIATE_TRIGGERS:
        _create_immediate_trigger(*item)
    for item in _DEFERRED_TRIGGERS:
        _create_deferred_trigger(*item)

def _create_views() -> None:
    specs = (
        ("schedule_current_placement","scoped_current_material_state","scoped_owner_ref","schedule.placement"),
        ("actual_current_realization","scoped_current_material_state","scoped_owner_ref","actual.realization"),
        ("session_current_timing","native_current_material_state","native_owner_ref","session.timing"),
        ("routine_current_recurrence","native_current_material_state","native_owner_ref","routine.recurrence"),
        ("event_current_recurrence","native_current_material_state","native_owner_ref","event.recurrence"),
    )
    for view,base,owner_column,facet in specs:
        _sql(
            f"CREATE VIEW dante.{view} WITH (security_invoker=false, security_barrier=false) AS "
            f"SELECT {owner_column}, facet_code, material_state_ref FROM dante.{base} "
            f"WHERE facet_code='{facet}' WITH LOCAL CHECK OPTION"
        )
        _sql(f"ALTER VIEW dante.{view} ALTER COLUMN facet_code SET DEFAULT '{facet}'")
        _sql(f"ALTER VIEW dante.{view} OWNER TO {_OWNER_ROLE}")
        _sql(f"REVOKE ALL PRIVILEGES ON TABLE dante.{view} FROM PUBLIC, {_RUNTIME_ROLE}, {_MIGRATOR_ROLE}")


def upgrade() -> None:
    """Install the M5 integrity/current-view layer without activating runtime DML."""
    _replace_checks(repaired=True)
    _create_routines()
    _create_triggers()
    _create_views()


def downgrade() -> None:
    """Return exactly to the historical CP6-M04 surface."""
    for view in reversed(_VIEWS):
        _sql(f"DROP VIEW dante.{view}")
    for name, table, _, _ in reversed(_DEFERRED_TRIGGERS):
        _sql(f"DROP TRIGGER {name} ON dante.{table}")
    for name, table, _, _ in reversed(_IMMEDIATE_TRIGGERS):
        _sql(f"DROP TRIGGER {name} ON dante.{table}")
    for routine in reversed(_ROUTINES):
        _sql(f"DROP FUNCTION dante.{routine}()")
    _replace_checks(repaired=False)
