# ruff: noqa: S608
"""B06-C: canonical bounded Occurrence checkpoint and scope.

Revision ID: 20260922_55
Revises: 20260922_54

The checkpoint is an explicit mutating command.  A read never expands a
Recurrence.  All writes remain behind self-scoped SECURITY DEFINER
capabilities and CP6 Role-13 remains the final coordinate/provenance guard.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260922_55"
down_revision: str | None = "20260922_54"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"


def _sql(statement: str) -> None:
    op.execute(sa.text(statement))


def _deny_table(name: str) -> None:
    _sql(f"REVOKE ALL PRIVILEGES ON TABLE dante.{name} FROM PUBLIC,{_RUNTIME},{_MIGRATOR}")


def _retire_direct_generation_writes() -> None:
    """Make the patched historical-state validator reachable only via B06-C commands."""
    for table in (
        "occurrence_generation",
        "occurrence_generation_calendar",
        "occurrence_generation_elapsed",
        "occurrence_generation_quota",
        "occurrence_generation_cyclic",
    ):
        _sql(f"REVOKE ALL PRIVILEGES ON TABLE dante.{table} FROM {_RUNTIME},{_MIGRATOR}")


def _create_tables() -> None:
    op.create_table(
        "occurrence_checkpoint_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("source_native_ref", sa.Uuid(), nullable=False),
        sa.Column("source_family", sa.Text(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date_exclusive", sa.Date(), nullable=False),
        sa.Column("effective_zone_id", sa.Text(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            name=op.f("pk_occurrence_checkpoint_operation"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_occurrence_checkpoint_operation_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["source_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_occurrence_checkpoint_operation_source",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f("ck_occurrence_checkpoint_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_occurrence_checkpoint_operation_fingerprint"),
        ),
        sa.CheckConstraint(
            "source_family IN ('routine','event')",
            name=op.f("ck_occurrence_checkpoint_operation_source_family"),
        ),
        sa.CheckConstraint(
            "isfinite(start_date) AND isfinite(end_date_exclusive) "
            "AND end_date_exclusive>start_date "
            "AND end_date_exclusive-start_date<=62",
            name=op.f("ck_occurrence_checkpoint_operation_range"),
        ),
        sa.CheckConstraint(
            "effective_zone_id=btrim(effective_zone_id) "
            "AND effective_zone_id<>'' AND char_length(effective_zone_id)<=200",
            name=op.f("ck_occurrence_checkpoint_operation_zone"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_occurrence_checkpoint_operation_source_range",
        "occurrence_checkpoint_operation",
        ["source_native_ref", "start_date", "end_date_exclusive", "accepted_at"],
        schema=_SCHEMA,
    )

    op.create_table(
        "occurrence_checkpoint_result",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("occurrence_ref", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            "occurrence_ref",
            name=op.f("pk_occurrence_checkpoint_result"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref", "operation_id"],
            [
                "dante.occurrence_checkpoint_operation.self_person_ref",
                "dante.occurrence_checkpoint_operation.operation_id",
            ],
            name="fk_occurrence_checkpoint_result_operation",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["occurrence_ref"],
            ["dante.occurrence.occurrence_ref"],
            name="fk_occurrence_checkpoint_result_occurrence",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_occurrence_checkpoint_result_occurrence",
        "occurrence_checkpoint_result",
        ["occurrence_ref"],
        schema=_SCHEMA,
    )

    op.create_table(
        "occurrence_extra_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("source_native_ref", sa.Uuid(), nullable=False),
        sa.Column("source_family", sa.Text(), nullable=False),
        sa.Column("occurrence_ref", sa.Uuid(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            name=op.f("pk_occurrence_extra_operation"),
        ),
        sa.UniqueConstraint(
            "occurrence_ref",
            name=op.f("uq_occurrence_extra_operation_occurrence"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_occurrence_extra_operation_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["source_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_occurrence_extra_operation_source",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["occurrence_ref"],
            ["dante.occurrence.occurrence_ref"],
            name="fk_occurrence_extra_operation_occurrence",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f("ck_occurrence_extra_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_occurrence_extra_operation_fingerprint"),
        ),
        sa.CheckConstraint(
            "source_family IN ('routine','event')",
            name=op.f("ck_occurrence_extra_operation_source_family"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_occurrence_extra_operation_source_accepted",
        "occurrence_extra_operation",
        ["source_native_ref", "accepted_at"],
        schema=_SCHEMA,
    )

    op.create_table(
        "occurrence_skip",
        sa.Column("occurrence_ref", sa.Uuid(), nullable=False),
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("skipped_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("occurrence_ref", name=op.f("pk_occurrence_skip")),
        sa.UniqueConstraint(
            "self_person_ref",
            "operation_id",
            name=op.f("uq_occurrence_skip_operation"),
        ),
        sa.ForeignKeyConstraint(
            ["occurrence_ref"],
            ["dante.occurrence.occurrence_ref"],
            name="fk_occurrence_skip_occurrence",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_occurrence_skip_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f("ck_occurrence_skip_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_occurrence_skip_fingerprint"),
        ),
        sa.CheckConstraint(
            "reason IS NULL OR (reason=btrim(reason) AND reason<>'' AND char_length(reason)<=500)",
            name=op.f("ck_occurrence_skip_reason"),
        ),
        schema=_SCHEMA,
    )

    op.create_table(
        "occurrence_exclusion",
        sa.Column("exclusion_ref", sa.Uuid(), nullable=False),
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("source_native_ref", sa.Uuid(), nullable=False),
        sa.Column("governing_recurrence_state_ref", sa.Uuid(), nullable=False),
        sa.Column("family_code", sa.Text(), nullable=False),
        sa.Column("generated_date", sa.Date(), nullable=True),
        sa.Column("generated_wall_time", sa.Time(timezone=False), nullable=True),
        sa.Column("expected_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("position_index", sa.Integer(), nullable=True),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "exclusion_ref",
            name=op.f("pk_occurrence_exclusion"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_occurrence_exclusion_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["source_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_occurrence_exclusion_source",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["governing_recurrence_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_occurrence_exclusion_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "uuid_extract_version(exclusion_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_occurrence_exclusion_uuidv7"),
        ),
        sa.CheckConstraint(
            "family_code IN ('calendar_wall_clock','elapsed_interval','cyclic_positional')",
            name=op.f("ck_occurrence_exclusion_family"),
        ),
        sa.CheckConstraint(
            "(family_code='calendar_wall_clock' AND generated_date IS NOT NULL "
            "AND expected_at IS NULL AND position_index IS NULL) OR "
            "(family_code='elapsed_interval' AND generated_date IS NULL "
            "AND generated_wall_time IS NULL AND expected_at IS NOT NULL "
            "AND position_index IS NULL) OR "
            "(family_code='cyclic_positional' AND generated_date IS NOT NULL "
            "AND generated_wall_time IS NULL AND expected_at IS NULL "
            "AND position_index IS NOT NULL)",
            name=op.f("ck_occurrence_exclusion_coordinate"),
        ),
        sa.CheckConstraint(
            "generated_date IS NULL OR isfinite(generated_date)",
            name=op.f("ck_occurrence_exclusion_date"),
        ),
        sa.CheckConstraint(
            "expected_at IS NULL OR isfinite(expected_at)",
            name=op.f("ck_occurrence_exclusion_instant"),
        ),
        sa.CheckConstraint(
            "position_index IS NULL OR position_index>=0",
            name=op.f("ck_occurrence_exclusion_position"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_occurrence_exclusion_source_state",
        "occurrence_exclusion",
        ["source_native_ref", "governing_recurrence_state_ref", "family_code"],
        schema=_SCHEMA,
    )
    _sql(
        "CREATE UNIQUE INDEX uq_occurrence_exclusion_calendar "
        "ON dante.occurrence_exclusion "
        "(source_native_ref,governing_recurrence_state_ref,generated_date,generated_wall_time) "
        "NULLS NOT DISTINCT WHERE family_code='calendar_wall_clock'"
    )
    _sql(
        "CREATE UNIQUE INDEX uq_occurrence_exclusion_elapsed "
        "ON dante.occurrence_exclusion "
        "(source_native_ref,governing_recurrence_state_ref,expected_at) "
        "WHERE family_code='elapsed_interval'"
    )
    _sql(
        "CREATE UNIQUE INDEX uq_occurrence_exclusion_cyclic "
        "ON dante.occurrence_exclusion "
        "(source_native_ref,governing_recurrence_state_ref,generated_date,position_index) "
        "WHERE family_code='cyclic_positional'"
    )

    op.create_table(
        "occurrence_exclusion_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("exclusion_ref", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            name=op.f("pk_occurrence_exclusion_operation"),
        ),
        sa.UniqueConstraint(
            "exclusion_ref",
            name=op.f("uq_occurrence_exclusion_operation_ref"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_occurrence_exclusion_operation_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["exclusion_ref"],
            ["dante.occurrence_exclusion.exclusion_ref"],
            name="fk_occurrence_exclusion_operation_exclusion",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f("ck_occurrence_exclusion_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_occurrence_exclusion_operation_fingerprint"),
        ),
        schema=_SCHEMA,
    )

    for table in (
        "occurrence_checkpoint_operation",
        "occurrence_checkpoint_result",
        "occurrence_extra_operation",
        "occurrence_skip",
        "occurrence_exclusion",
        "occurrence_exclusion_operation",
    ):
        _deny_table(table)


def _scope_predicate(prefix: str, owner: str) -> str:
    table = "routine_intention" if prefix == "routine" else "event_expectation"
    return (
        f"EXISTS (SELECT 1 FROM dante.{table} s "
        f"WHERE s.{owner}=requested_source_ref "
        "AND s.self_person_ref=requested_self_person_ref)"
    )


def _source_locks(prefix: str) -> str:
    current_ns, generation_ns = (4, 6) if prefix == "routine" else (5, 7)
    return rf"""
  PERFORM pg_catalog.pg_advisory_xact_lock(
    ({current_ns}::bigint << 56) |
    ((get_byte(d.digest,0)::bigint << 48) | (get_byte(d.digest,1)::bigint << 40) |
     (get_byte(d.digest,2)::bigint << 32) | (get_byte(d.digest,3)::bigint << 24) |
     (get_byte(d.digest,4)::bigint << 16) | (get_byte(d.digest,5)::bigint << 8) |
      get_byte(d.digest,6)::bigint)
  ) FROM (SELECT sha256(convert_to('dante-lock-v2','UTF8') || uuid_send(requested_source_ref)) AS digest) d;
  PERFORM pg_catalog.pg_advisory_xact_lock(
    ({generation_ns}::bigint << 56) |
    ((get_byte(d.digest,0)::bigint << 48) | (get_byte(d.digest,1)::bigint << 40) |
     (get_byte(d.digest,2)::bigint << 32) | (get_byte(d.digest,3)::bigint << 24) |
     (get_byte(d.digest,4)::bigint << 16) | (get_byte(d.digest,5)::bigint << 8) |
      get_byte(d.digest,6)::bigint)
  ) FROM (SELECT sha256(convert_to('dante-lock-v2','UTF8') || uuid_send(requested_source_ref)) AS digest) d;
"""


def _begin_checkpoint_function(prefix: str, owner: str) -> str:
    scope = _scope_predicate(prefix, owner)
    active_guard = (
        """
  PERFORM 1 FROM dante.routine_intention r
   WHERE r.routine_ref=requested_source_ref
     AND r.self_person_ref=requested_self_person_ref FOR UPDATE;
  IF NOT EXISTS (
    SELECT 1 FROM dante.routine_intention r
     WHERE r.routine_ref=requested_source_ref
       AND r.self_person_ref=requested_self_person_ref
       AND r.lifecycle_state='active'
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='routine_occurrence_source_inactive',
      MESSAGE='Inactive Routine cannot generate Occurrences';
  END IF;
"""
        if prefix == "routine"
        else ""
    )
    return rf"""
CREATE FUNCTION dante.begin_self_{prefix}_occurrence_checkpoint(
  requested_self_person_ref uuid, requested_operation_id text,
  requested_intent_fingerprint text, requested_source_ref uuid,
  requested_start_date date, requested_end_date_exclusive date,
  requested_effective_zone_id text
) RETURNS TABLE(accepted_at timestamptz, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE
  key text := btrim(requested_operation_id);
  zone_value text := btrim(requested_effective_zone_id);
  prior record;
  recorded_at timestamptz := statement_timestamp();
BEGIN
  IF key IS NULL OR key='' OR char_length(key)>200
     OR requested_intent_fingerprint IS NULL
     OR requested_intent_fingerprint !~ '^[0-9a-f]{{64}}$'
     OR requested_start_date IS NULL OR requested_end_date_exclusive IS NULL
     OR NOT isfinite(requested_start_date) OR NOT isfinite(requested_end_date_exclusive)
     OR requested_end_date_exclusive<=requested_start_date
     OR requested_end_date_exclusive-requested_start_date>62
     OR zone_value IS NULL OR zone_value='' OR char_length(zone_value)>200
     OR NOT EXISTS (SELECT 1 FROM pg_timezone_names z WHERE z.name=zone_value)
  THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_occurrence_checkpoint_operation_range',
      MESSAGE='Occurrence checkpoint rejected';
  END IF;
  IF NOT {scope} THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='{prefix}_occurrence_source_unavailable',
      MESSAGE='Occurrence source unavailable';
  END IF;
  PERFORM pg_advisory_xact_lock(hashtextextended(
    requested_self_person_ref::text || ':' || key,0));
{_source_locks(prefix)}
  PERFORM 1 FROM dante.native_current_material_state n
   WHERE n.native_owner_ref=requested_source_ref
     AND n.facet_code='{prefix}.recurrence' FOR UPDATE;
  IF NOT FOUND THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='{prefix}_occurrence_recurrence_unavailable',
      MESSAGE='Occurrence Recurrence unavailable';
  END IF;

  SELECT * INTO prior FROM dante.occurrence_checkpoint_operation o
   WHERE o.self_person_ref=requested_self_person_ref AND o.operation_id=key;
  IF FOUND THEN
    IF prior.intent_fingerprint<>requested_intent_fingerprint
       OR prior.source_native_ref<>requested_source_ref
       OR prior.source_family<>'{prefix}'
       OR prior.start_date<>requested_start_date
       OR prior.end_date_exclusive<>requested_end_date_exclusive
       OR prior.effective_zone_id<>zone_value THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        CONSTRAINT='pk_occurrence_checkpoint_operation',
        MESSAGE='Occurrence checkpoint operation id reused';
    END IF;
    RETURN QUERY SELECT prior.accepted_at,true;
    RETURN;
  END IF;
{active_guard}

  INSERT INTO dante.occurrence_checkpoint_operation(
    self_person_ref,operation_id,intent_fingerprint,source_native_ref,
    source_family,start_date,end_date_exclusive,effective_zone_id,accepted_at
  ) VALUES (
    requested_self_person_ref,key,requested_intent_fingerprint,
    requested_source_ref,'{prefix}',requested_start_date,
    requested_end_date_exclusive,zone_value,recorded_at
  );
  RETURN QUERY SELECT recorded_at,false;
END;
$function$;
"""


def _history_function(prefix: str, owner: str) -> str:
    scope = _scope_predicate(prefix, owner)
    return rf"""
CREATE FUNCTION dante.list_self_{prefix}_recurrence_history(
  requested_self_person_ref uuid, requested_source_ref uuid
) RETURNS TABLE(
  material_state_ref uuid, current_from_at timestamptz, current_until_at timestamptz,
  family_code text, range_kind text, expected_occurrence_count integer,
  effective_from_date date, effective_until_date date,
  effective_from_instant timestamptz, effective_until_instant timestamptz,
  calendar_pattern_code text, calendar_interval_count integer,
  calendar_clock_basis_code text, calendar_zone_id text,
  calendar_step_unit_code text, calendar_pattern_anchor_date date,
  calendar_wall_times time[], calendar_weekdays smallint[],
  calendar_month_days smallint[], calendar_ordinal_weekdays smallint[],
  calendar_ordinals smallint[], calendar_year_months smallint[],
  calendar_year_month_days smallint[],
  dst_nonexistent_local_time_policy text, dst_ambiguous_local_time_policy text,
  elapsed_seconds numeric, elapsed_anchor_mode_code text, elapsed_anchor_at timestamptz,
  quota_count integer, quota_period_unit_code text, quota_period_span integer,
  quota_frame_code text, quota_zone_id text, quota_week_start smallint,
  cyclic_cycle_length integer, cyclic_position_unit_code text,
  cyclic_pattern_anchor_date date, cyclic_generates_expected boolean[]
)
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
BEGIN
  IF NOT {scope} THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='{prefix}_occurrence_source_unavailable',
      MESSAGE='Occurrence source unavailable';
  END IF;
  RETURN QUERY
  SELECT s.material_state_ref,h.current_from_at,h.current_until_at,
    s.family_code,s.range_kind,s.expected_occurrence_count,
    bf.date_value,bu.date_value,bf.instant_value,bu.instant_value,
    c.pattern_code,c.interval_count,c.clock_basis_code,c.zone_id,c.step_unit_code,ba.date_value,
    ARRAY(SELECT w.wall_time FROM dante.{prefix}_recurrence_calendar_wall_time w WHERE w.material_state_ref=s.material_state_ref ORDER BY w.wall_time),
    ARRAY(SELECT w.weekday_number FROM dante.{prefix}_recurrence_calendar_weekday w WHERE w.material_state_ref=s.material_state_ref ORDER BY w.weekday_number),
    ARRAY(SELECT m.month_day FROM dante.{prefix}_recurrence_calendar_month_day m WHERE m.material_state_ref=s.material_state_ref ORDER BY m.month_day),
    ARRAY(SELECT o.weekday_number FROM dante.{prefix}_recurrence_calendar_ordinal_weekday o WHERE o.material_state_ref=s.material_state_ref ORDER BY o.weekday_number,o.ordinal),
    ARRAY(SELECT o.ordinal FROM dante.{prefix}_recurrence_calendar_ordinal_weekday o WHERE o.material_state_ref=s.material_state_ref ORDER BY o.weekday_number,o.ordinal),
    ARRAY(SELECT y.month_number FROM dante.{prefix}_recurrence_calendar_year_month_day y WHERE y.material_state_ref=s.material_state_ref ORDER BY y.month_number,y.month_day),
    ARRAY(SELECT y.month_day FROM dante.{prefix}_recurrence_calendar_year_month_day y WHERE y.material_state_ref=s.material_state_ref ORDER BY y.month_number,y.month_day),
    d.nonexistent_local_time_policy,d.ambiguous_local_time_policy,
    e.elapsed_seconds,e.anchor_mode_code,e.anchor_at,
    q.quota_count,q.period_unit_code,q.period_span,q.frame_code,q.zone_id,q.week_start,
    cy.cycle_length,cy.position_unit_code,ba.date_value,
    ARRAY(SELECT p.generates_expected FROM dante.{prefix}_recurrence_cycle_position p WHERE p.material_state_ref=s.material_state_ref ORDER BY p.position_index)
  FROM dante.{prefix}_recurrence_state s
  JOIN dante.{prefix}_recurrence_current_history h
    ON h.{owner}=s.{owner} AND h.material_state_ref=s.material_state_ref
  LEFT JOIN dante.{prefix}_recurrence_boundary_state bf ON bf.material_state_ref=s.material_state_ref AND bf.boundary_role='effective_from'
  LEFT JOIN dante.{prefix}_recurrence_boundary_state bu ON bu.material_state_ref=s.material_state_ref AND bu.boundary_role='effective_until'
  LEFT JOIN dante.{prefix}_recurrence_boundary_state ba ON ba.material_state_ref=s.material_state_ref AND ba.boundary_role='pattern_anchor'
  LEFT JOIN dante.{prefix}_recurrence_calendar_state c ON c.material_state_ref=s.material_state_ref
  LEFT JOIN dante.{prefix}_recurrence_calendar_dst_policy d ON d.material_state_ref=s.material_state_ref
  LEFT JOIN dante.{prefix}_recurrence_elapsed_state e ON e.material_state_ref=s.material_state_ref
  LEFT JOIN dante.{prefix}_recurrence_quota_state q ON q.material_state_ref=s.material_state_ref
  LEFT JOIN dante.{prefix}_recurrence_cyclic_state cy ON cy.material_state_ref=s.material_state_ref
  WHERE s.{owner}=requested_source_ref
  ORDER BY h.current_from_at,s.material_state_ref;
END;
$function$;
"""


_OCCURRENCE_COLUMNS = """
  occurrence_ref uuid, source_native_ref uuid,
  governing_recurrence_state_ref uuid, origin_code text, family_code text,
  generated_date date, generated_wall_time time,
  clock_basis_code text, zone_id text, resolved_at timestamptz,
  expected_at timestamptz, period_start_date date,
  period_end_date_exclusive date, frame_code text,
  quota_zone_id text, position_index integer,
  skipped boolean, skip_reason text, skipped_at timestamptz
"""


def _occurrence_select(where_sql: str) -> str:
    return f"""
  SELECT g.occurrence_ref,g.source_native_ref,g.governing_recurrence_state_ref,
    g.origin_code,s.family_code,c.generated_date,c.generated_wall_time,
    c.clock_basis_code,c.zone_id,c.resolved_at,e.expected_at,
    q.period_start_date,q.period_end_date_exclusive,q.frame_code,q.zone_id,
    cy.position_index,(sk.occurrence_ref IS NOT NULL),sk.reason,sk.skipped_at
  FROM dante.occurrence_generation g
  LEFT JOIN dante.routine_recurrence_state rs
    ON rs.material_state_ref=g.governing_recurrence_state_ref
  LEFT JOIN dante.event_recurrence_state es
    ON es.material_state_ref=g.governing_recurrence_state_ref
  LEFT JOIN LATERAL (SELECT COALESCE(rs.family_code,es.family_code) AS family_code) s ON true
  LEFT JOIN dante.occurrence_generation_calendar c ON c.occurrence_ref=g.occurrence_ref
  LEFT JOIN dante.occurrence_generation_elapsed e ON e.occurrence_ref=g.occurrence_ref
  LEFT JOIN dante.occurrence_generation_quota q ON q.occurrence_ref=g.occurrence_ref
  LEFT JOIN dante.occurrence_generation_cyclic cy ON cy.occurrence_ref=g.occurrence_ref
  LEFT JOIN dante.occurrence_skip sk ON sk.occurrence_ref=g.occurrence_ref
  {where_sql}
"""


def _get_occurrence_function() -> str:
    return f"""
CREATE FUNCTION dante.get_self_occurrence(
  requested_self_person_ref uuid, requested_occurrence_ref uuid
) RETURNS TABLE({_OCCURRENCE_COLUMNS})
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
{_occurrence_select("WHERE g.occurrence_ref=requested_occurrence_ref AND (EXISTS (SELECT 1 FROM dante.routine_intention r WHERE r.routine_ref=g.source_native_ref AND r.self_person_ref=requested_self_person_ref) OR EXISTS (SELECT 1 FROM dante.event_expectation v WHERE v.event_ref=g.source_native_ref AND v.self_person_ref=requested_self_person_ref))")}
$function$;
"""


def _checkpoint_results_function(prefix: str, owner: str) -> str:
    scope = _scope_predicate(prefix, owner)
    where = (
        "JOIN dante.occurrence_checkpoint_result cr "
        "ON cr.occurrence_ref=g.occurrence_ref "
        "WHERE cr.self_person_ref=requested_self_person_ref "
        "AND cr.operation_id=btrim(requested_operation_id) "
        "AND g.source_native_ref=requested_source_ref "
        "ORDER BY g.occurrence_ref"
    )
    return f"""
CREATE FUNCTION dante.get_self_{prefix}_occurrence_checkpoint_result(
  requested_self_person_ref uuid, requested_operation_id text,
  requested_source_ref uuid
) RETURNS TABLE({_OCCURRENCE_COLUMNS})
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
BEGIN
  IF NOT {scope} OR NOT EXISTS (
    SELECT 1 FROM dante.occurrence_checkpoint_operation o
     WHERE o.self_person_ref=requested_self_person_ref
       AND o.operation_id=btrim(requested_operation_id)
       AND o.source_native_ref=requested_source_ref
       AND o.source_family='{prefix}'
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='{prefix}_occurrence_checkpoint_unavailable',
      MESSAGE='Occurrence checkpoint unavailable';
  END IF;
  RETURN QUERY
{_occurrence_select(where)};
END;
$function$;
"""


def _materialize_function(prefix: str, owner: str) -> str:
    scope = _scope_predicate(prefix, owner)
    state_table = f"{prefix}_recurrence_state"
    history_table = f"{prefix}_recurrence_current_history"
    return rf"""
CREATE FUNCTION dante.materialize_self_{prefix}_occurrence_candidate(
  requested_self_person_ref uuid, requested_operation_id text,
  requested_source_ref uuid, requested_governing_state_ref uuid,
  requested_family_code text,
  requested_generated_date date, requested_generated_wall_time time,
  requested_clock_basis_code text, requested_zone_id text,
  requested_resolved_at timestamptz, requested_expected_at timestamptz,
  requested_period_start_date date, requested_period_end_date_exclusive date,
  requested_frame_code text, requested_quota_zone_id text,
  requested_position_index integer
) RETURNS TABLE(occurrence_ref uuid, created boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE
  receipt record;
  state_accepted_at timestamptz;
  candidate_local_date date;
  candidate_instant timestamptz;
  found_ref uuid;
  new_ref uuid;
BEGIN
  IF NOT {scope} THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='{prefix}_occurrence_source_unavailable',
      MESSAGE='Occurrence source unavailable';
  END IF;
  SELECT * INTO receipt FROM dante.occurrence_checkpoint_operation o
   WHERE o.self_person_ref=requested_self_person_ref
     AND o.operation_id=btrim(requested_operation_id)
     AND o.source_native_ref=requested_source_ref
     AND o.source_family='{prefix}';
  IF NOT FOUND THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='{prefix}_occurrence_checkpoint_unavailable',
      MESSAGE='Occurrence checkpoint unavailable';
  END IF;
{_source_locks(prefix)}
  PERFORM 1 FROM dante.native_current_material_state n
   WHERE n.native_owner_ref=requested_source_ref
     AND n.facet_code='{prefix}.recurrence' FOR UPDATE;
  IF NOT EXISTS (
    SELECT 1 FROM dante.{state_table} s
     WHERE s.material_state_ref=requested_governing_state_ref
       AND s.{owner}=requested_source_ref
       AND s.family_code=requested_family_code
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='{prefix}_occurrence_governing_state',
      MESSAGE='Occurrence governing state rejected';
  END IF;

  SELECT h.current_from_at INTO state_accepted_at
    FROM dante.{history_table} h
   WHERE h.{owner}=requested_source_ref
     AND h.material_state_ref=requested_governing_state_ref;
  IF state_accepted_at IS NULL THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='{prefix}_occurrence_governing_state',
      MESSAGE='Occurrence governing history rejected';
  END IF;

  candidate_local_date := COALESCE(
    CASE
      WHEN requested_family_code='calendar_wall_clock'
           AND requested_resolved_at IS NOT NULL
      THEN (requested_resolved_at AT TIME ZONE receipt.effective_zone_id)::date
      WHEN requested_family_code='calendar_wall_clock'
           AND requested_clock_basis_code='absolute_utc'
           AND requested_generated_wall_time IS NOT NULL
      THEN ((requested_generated_date+requested_generated_wall_time)
            AT TIME ZONE 'UTC' AT TIME ZONE receipt.effective_zone_id)::date
      WHEN requested_family_code IN ('calendar_wall_clock','cyclic_positional')
      THEN requested_generated_date
      WHEN requested_family_code='quota_per_period'
      THEN requested_period_start_date
      WHEN requested_family_code='elapsed_interval'
      THEN (requested_expected_at AT TIME ZONE receipt.effective_zone_id)::date
      ELSE NULL
    END
  );
  candidate_instant := COALESCE(
    requested_resolved_at,requested_expected_at,
    CASE
      WHEN requested_generated_date IS NOT NULL
      THEN (requested_generated_date + COALESCE(requested_generated_wall_time,time '00:00'))
           AT TIME ZONE CASE WHEN requested_clock_basis_code='named_zone'
                             THEN requested_zone_id
                             WHEN requested_clock_basis_code='absolute_utc'
                             THEN 'UTC' ELSE receipt.effective_zone_id END
      WHEN requested_period_start_date IS NOT NULL
      THEN requested_period_start_date::timestamp AT TIME ZONE receipt.effective_zone_id
      ELSE NULL
    END
  );
  IF (requested_family_code='quota_per_period' AND NOT (
        requested_period_start_date<receipt.end_date_exclusive
        AND requested_period_end_date_exclusive>receipt.start_date
      )) OR (requested_family_code<>'quota_per_period' AND NOT (
        candidate_local_date>=receipt.start_date
        AND candidate_local_date<receipt.end_date_exclusive
      )) THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='{prefix}_occurrence_checkpoint_range',
      MESSAGE='Occurrence candidate is outside checkpoint range';
  END IF;
  IF EXISTS (
    SELECT 1
      FROM dante.{history_table} later
      JOIN dante.{prefix}_recurrence_boundary_state b
        ON b.material_state_ref=later.material_state_ref
       AND b.boundary_role='effective_from'
     WHERE later.{owner}=requested_source_ref
       AND (later.current_from_at,later.material_state_ref)>
           (state_accepted_at,requested_governing_state_ref)
       AND ((b.date_value IS NOT NULL AND candidate_local_date>=b.date_value)
         OR (b.instant_value IS NOT NULL AND candidate_instant>=b.instant_value))
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='{prefix}_occurrence_effective_state',
      MESSAGE='Occurrence state is superseded at this coordinate';
  END IF;

  IF EXISTS (
    SELECT 1 FROM dante.occurrence_exclusion x
     WHERE x.source_native_ref=requested_source_ref
       AND x.governing_recurrence_state_ref=requested_governing_state_ref
       AND x.family_code=requested_family_code
       AND x.generated_date IS NOT DISTINCT FROM requested_generated_date
       AND x.generated_wall_time IS NOT DISTINCT FROM requested_generated_wall_time
       AND x.expected_at IS NOT DISTINCT FROM requested_expected_at
       AND x.position_index IS NOT DISTINCT FROM requested_position_index
  ) THEN
    -- Structural exclusion means this civil/instant coordinate never becomes
    -- an Occurrence.  Returning zero rows is intentional and remains distinct
    -- from materialize-then-skip.
    RETURN;
  END IF;

  IF requested_family_code='calendar_wall_clock' THEN
    SELECT g.occurrence_ref INTO found_ref
      FROM dante.occurrence_generation g
      JOIN dante.occurrence_generation_calendar c USING(occurrence_ref)
     WHERE g.source_native_ref=requested_source_ref
       AND g.governing_recurrence_state_ref=requested_governing_state_ref
       AND c.generated_date=requested_generated_date
       AND c.generated_wall_time IS NOT DISTINCT FROM requested_generated_wall_time
       AND c.clock_basis_code=requested_clock_basis_code
       AND c.zone_id IS NOT DISTINCT FROM requested_zone_id
     ORDER BY g.occurrence_ref LIMIT 1;
  ELSIF requested_family_code='elapsed_interval' THEN
    SELECT g.occurrence_ref INTO found_ref
      FROM dante.occurrence_generation g
      JOIN dante.occurrence_generation_elapsed e USING(occurrence_ref)
     WHERE g.source_native_ref=requested_source_ref
       AND g.governing_recurrence_state_ref=requested_governing_state_ref
       AND e.expected_at=requested_expected_at
     ORDER BY g.occurrence_ref LIMIT 1;
  ELSIF requested_family_code='cyclic_positional' THEN
    SELECT g.occurrence_ref INTO found_ref
      FROM dante.occurrence_generation g
      JOIN dante.occurrence_generation_cyclic c USING(occurrence_ref)
     WHERE g.source_native_ref=requested_source_ref
       AND g.governing_recurrence_state_ref=requested_governing_state_ref
       AND c.generated_date=requested_generated_date
       AND c.position_index=requested_position_index
     ORDER BY g.occurrence_ref LIMIT 1;
  ELSIF requested_family_code='quota_per_period' THEN
    SELECT g.occurrence_ref INTO found_ref
      FROM dante.occurrence_generation g
      JOIN dante.occurrence_generation_quota q USING(occurrence_ref)
     WHERE g.source_native_ref=requested_source_ref
       AND g.governing_recurrence_state_ref=requested_governing_state_ref
       AND q.period_start_date=requested_period_start_date
       AND q.period_end_date_exclusive=requested_period_end_date_exclusive
       AND NOT EXISTS (
         SELECT 1 FROM dante.occurrence_checkpoint_result cr
          WHERE cr.self_person_ref=requested_self_person_ref
            AND cr.operation_id=btrim(requested_operation_id)
            AND cr.occurrence_ref=g.occurrence_ref
       )
     ORDER BY g.occurrence_ref LIMIT 1;
  ELSE
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='{prefix}_occurrence_family',
      MESSAGE='Occurrence family rejected';
  END IF;

  IF found_ref IS NULL THEN
    new_ref := uuidv7();
    INSERT INTO dante.occurrence(occurrence_ref) VALUES(new_ref);
    INSERT INTO dante.native_address(native_ref,owner_family)
      VALUES(new_ref,'occurrence');
    INSERT INTO dante.occurrence_generation(
      occurrence_ref,source_native_ref,governing_recurrence_state_ref,origin_code
    ) VALUES(new_ref,requested_source_ref,requested_governing_state_ref,'recurrence_generated');
    IF requested_family_code='calendar_wall_clock' THEN
      INSERT INTO dante.occurrence_generation_calendar(
        occurrence_ref,generated_date,generated_wall_time,clock_basis_code,zone_id,resolved_at
      ) VALUES(new_ref,requested_generated_date,requested_generated_wall_time,
        requested_clock_basis_code,requested_zone_id,requested_resolved_at);
    ELSIF requested_family_code='elapsed_interval' THEN
      INSERT INTO dante.occurrence_generation_elapsed(occurrence_ref,expected_at)
        VALUES(new_ref,requested_expected_at);
    ELSIF requested_family_code='quota_per_period' THEN
      INSERT INTO dante.occurrence_generation_quota(
        occurrence_ref,period_start_date,period_end_date_exclusive,frame_code,zone_id
      ) VALUES(new_ref,requested_period_start_date,requested_period_end_date_exclusive,
        requested_frame_code,requested_quota_zone_id);
    ELSE
      INSERT INTO dante.occurrence_generation_cyclic(
        occurrence_ref,generated_date,position_index
      ) VALUES(new_ref,requested_generated_date,requested_position_index);
    END IF;
    found_ref := new_ref;
  END IF;

  INSERT INTO dante.occurrence_checkpoint_result(
    self_person_ref,operation_id,occurrence_ref
  ) VALUES(requested_self_person_ref,btrim(requested_operation_id),found_ref)
  ON CONFLICT DO NOTHING;
  RETURN QUERY SELECT found_ref,(new_ref IS NOT NULL);
END;
$function$;
"""


def _extra_function(prefix: str, owner: str) -> str:
    scope = _scope_predicate(prefix, owner)
    active_guard = (
        """
  PERFORM 1 FROM dante.routine_intention r
   WHERE r.routine_ref=requested_source_ref
     AND r.self_person_ref=requested_self_person_ref FOR UPDATE;
  IF NOT EXISTS (
    SELECT 1 FROM dante.routine_intention r
     WHERE r.routine_ref=requested_source_ref
       AND r.self_person_ref=requested_self_person_ref
       AND r.lifecycle_state='active'
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='routine_occurrence_source_inactive',
      MESSAGE='Inactive Routine cannot accept an extra Occurrence';
  END IF;
"""
        if prefix == "routine"
        else ""
    )
    return rf"""
CREATE FUNCTION dante.create_self_{prefix}_extra_occurrence(
  requested_self_person_ref uuid, requested_operation_id text,
  requested_intent_fingerprint text, requested_source_ref uuid
) RETURNS TABLE(occurrence_ref uuid, accepted_at timestamptz, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE
  key text := btrim(requested_operation_id);
  prior record; new_ref uuid; recorded_at timestamptz:=statement_timestamp();
BEGIN
  IF key IS NULL OR key='' OR char_length(key)>200
     OR requested_intent_fingerprint IS NULL
     OR requested_intent_fingerprint !~ '^[0-9a-f]{{64}}$' THEN
    RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Extra Occurrence rejected';
  END IF;
  IF NOT {scope} THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='{prefix}_occurrence_source_unavailable',
      MESSAGE='Occurrence source unavailable';
  END IF;
  PERFORM pg_advisory_xact_lock(hashtextextended(
    requested_self_person_ref::text || ':' || key,0));
{_source_locks(prefix)}
  PERFORM 1 FROM dante.native_current_material_state n
   WHERE n.native_owner_ref=requested_source_ref
     AND n.facet_code='{prefix}.recurrence' FOR UPDATE;
  IF NOT FOUND THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='{prefix}_occurrence_recurrence_unavailable',
      MESSAGE='Occurrence Recurrence unavailable';
  END IF;
  SELECT * INTO prior FROM dante.occurrence_extra_operation o
   WHERE o.self_person_ref=requested_self_person_ref AND o.operation_id=key;
  IF FOUND THEN
    IF prior.intent_fingerprint<>requested_intent_fingerprint
       OR prior.source_native_ref<>requested_source_ref
       OR prior.source_family<>'{prefix}' THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        CONSTRAINT='pk_occurrence_extra_operation',
        MESSAGE='Extra Occurrence operation id reused';
    END IF;
    RETURN QUERY SELECT prior.occurrence_ref,prior.accepted_at,true;
    RETURN;
  END IF;
{active_guard}
  new_ref:=uuidv7();
  INSERT INTO dante.occurrence(occurrence_ref) VALUES(new_ref);
  INSERT INTO dante.native_address(native_ref,owner_family) VALUES(new_ref,'occurrence');
  INSERT INTO dante.occurrence_generation(
    occurrence_ref,source_native_ref,governing_recurrence_state_ref,origin_code
  ) VALUES(new_ref,requested_source_ref,NULL,'explicit_extra');
  INSERT INTO dante.occurrence_extra_operation(
    self_person_ref,operation_id,intent_fingerprint,source_native_ref,
    source_family,occurrence_ref,accepted_at
  ) VALUES(requested_self_person_ref,key,requested_intent_fingerprint,
    requested_source_ref,'{prefix}',new_ref,recorded_at);
  RETURN QUERY SELECT new_ref,recorded_at,false;
END;
$function$;
"""


def _exclusion_function(prefix: str, owner: str) -> str:
    scope = _scope_predicate(prefix, owner)
    return rf"""
CREATE FUNCTION dante.exclude_self_{prefix}_occurrence_coordinate(
  requested_self_person_ref uuid, requested_operation_id text,
  requested_intent_fingerprint text, requested_source_ref uuid,
  requested_governing_state_ref uuid, requested_family_code text,
  requested_generated_date date, requested_generated_wall_time time,
  requested_expected_at timestamptz, requested_position_index integer
) RETURNS TABLE(exclusion_ref uuid, accepted_at timestamptz, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE
  key text:=btrim(requested_operation_id); prior record;
  new_ref uuid; recorded_at timestamptz:=statement_timestamp();
BEGIN
  IF key IS NULL OR key='' OR char_length(key)>200
     OR requested_intent_fingerprint IS NULL
     OR requested_intent_fingerprint !~ '^[0-9a-f]{{64}}$'
     OR requested_family_code NOT IN ('calendar_wall_clock','elapsed_interval','cyclic_positional')
  THEN RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Occurrence exclusion rejected'; END IF;
  IF NOT {scope} OR NOT EXISTS (
    SELECT 1 FROM dante.{prefix}_recurrence_state s
     WHERE s.material_state_ref=requested_governing_state_ref
       AND s.{owner}=requested_source_ref
       AND s.family_code=requested_family_code
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='{prefix}_occurrence_governing_state',
      MESSAGE='Occurrence exclusion source unavailable';
  END IF;
  PERFORM pg_advisory_xact_lock(hashtextextended(
    requested_self_person_ref::text || ':' || key,0));
{_source_locks(prefix)}
  SELECT * INTO prior FROM dante.occurrence_exclusion_operation o
   WHERE o.self_person_ref=requested_self_person_ref AND o.operation_id=key;
  IF FOUND THEN
    IF prior.intent_fingerprint<>requested_intent_fingerprint OR NOT EXISTS (
      SELECT 1 FROM dante.occurrence_exclusion x
       WHERE x.exclusion_ref=prior.exclusion_ref
         AND x.source_native_ref=requested_source_ref
         AND x.governing_recurrence_state_ref=requested_governing_state_ref
         AND x.family_code=requested_family_code
         AND x.generated_date IS NOT DISTINCT FROM requested_generated_date
         AND x.generated_wall_time IS NOT DISTINCT FROM requested_generated_wall_time
         AND x.expected_at IS NOT DISTINCT FROM requested_expected_at
         AND x.position_index IS NOT DISTINCT FROM requested_position_index
    ) THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        CONSTRAINT='pk_occurrence_exclusion_operation',
        MESSAGE='Occurrence exclusion operation id reused';
    END IF;
    RETURN QUERY SELECT prior.exclusion_ref,
      (SELECT x.accepted_at FROM dante.occurrence_exclusion x WHERE x.exclusion_ref=prior.exclusion_ref),true;
    RETURN;
  END IF;
  IF EXISTS (
    SELECT 1 FROM dante.occurrence_generation g
    LEFT JOIN dante.occurrence_generation_calendar c USING(occurrence_ref)
    LEFT JOIN dante.occurrence_generation_elapsed e USING(occurrence_ref)
    LEFT JOIN dante.occurrence_generation_cyclic cy USING(occurrence_ref)
    WHERE g.source_native_ref=requested_source_ref
      AND g.governing_recurrence_state_ref=requested_governing_state_ref
      AND ((requested_family_code='calendar_wall_clock'
            AND c.generated_date=requested_generated_date
            AND c.generated_wall_time IS NOT DISTINCT FROM requested_generated_wall_time)
        OR (requested_family_code='elapsed_interval' AND e.expected_at=requested_expected_at)
        OR (requested_family_code='cyclic_positional'
            AND cy.generated_date=requested_generated_date
            AND cy.position_index=requested_position_index))
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='occurrence_exclusion_materialized_conflict',
      MESSAGE='Materialized Occurrence cannot become a structural exclusion';
  END IF;
  new_ref:=uuidv7();
  INSERT INTO dante.occurrence_exclusion(
    exclusion_ref,self_person_ref,source_native_ref,
    governing_recurrence_state_ref,family_code,generated_date,
    generated_wall_time,expected_at,position_index,accepted_at
  ) VALUES(new_ref,requested_self_person_ref,requested_source_ref,
    requested_governing_state_ref,requested_family_code,requested_generated_date,
    requested_generated_wall_time,requested_expected_at,
    requested_position_index,recorded_at);
  INSERT INTO dante.occurrence_exclusion_operation(
    self_person_ref,operation_id,intent_fingerprint,exclusion_ref
  ) VALUES(requested_self_person_ref,key,requested_intent_fingerprint,new_ref);
  RETURN QUERY SELECT new_ref,recorded_at,false;
END;
$function$;
"""


_SKIP_FUNCTION = r"""
CREATE FUNCTION dante.skip_self_occurrence(
  requested_self_person_ref uuid, requested_operation_id text,
  requested_intent_fingerprint text, requested_occurrence_ref uuid,
  requested_reason text
) RETURNS TABLE(occurrence_ref uuid, skipped_at timestamptz, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE
  key text:=btrim(requested_operation_id);
  reason_value text:=NULLIF(btrim(requested_reason),'');
  prior record; source_ref uuid; recorded_at timestamptz:=statement_timestamp();
BEGIN
  IF key IS NULL OR key='' OR char_length(key)>200
     OR requested_intent_fingerprint IS NULL
     OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$'
     OR (reason_value IS NOT NULL AND char_length(reason_value)>500) THEN
    RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Occurrence skip rejected';
  END IF;
  SELECT g.source_native_ref INTO source_ref FROM dante.occurrence_generation g
   WHERE g.occurrence_ref=requested_occurrence_ref
     AND (EXISTS (SELECT 1 FROM dante.routine_intention r
                   WHERE r.routine_ref=g.source_native_ref
                     AND r.self_person_ref=requested_self_person_ref)
       OR EXISTS (SELECT 1 FROM dante.event_expectation e
                   WHERE e.event_ref=g.source_native_ref
                     AND e.self_person_ref=requested_self_person_ref));
  IF source_ref IS NULL THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='occurrence_unavailable', MESSAGE='Occurrence unavailable';
  END IF;
  PERFORM pg_advisory_xact_lock(hashtextextended(
    requested_self_person_ref::text || ':' || key,0));
  SELECT * INTO prior FROM dante.occurrence_skip s
   WHERE s.self_person_ref=requested_self_person_ref AND s.operation_id=key;
  IF FOUND THEN
    IF prior.intent_fingerprint<>requested_intent_fingerprint
       OR prior.occurrence_ref<>requested_occurrence_ref
       OR prior.reason IS DISTINCT FROM reason_value THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        CONSTRAINT='uq_occurrence_skip_operation',
        MESSAGE='Occurrence skip operation id reused';
    END IF;
    RETURN QUERY SELECT prior.occurrence_ref,prior.skipped_at,true;
    RETURN;
  END IF;
  IF EXISTS (SELECT 1 FROM dante.occurrence_skip s
              WHERE s.occurrence_ref=requested_occurrence_ref) THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='pk_occurrence_skip', MESSAGE='Occurrence already skipped';
  END IF;
  INSERT INTO dante.occurrence_skip(
    occurrence_ref,self_person_ref,operation_id,intent_fingerprint,reason,skipped_at
  ) VALUES(requested_occurrence_ref,requested_self_person_ref,key,
    requested_intent_fingerprint,reason_value,recorded_at);
  RETURN QUERY SELECT requested_occurrence_ref,recorded_at,false;
END;
$function$;
"""


def _patch_role13_history() -> None:
    """Allow retained governing states; B06-C capabilities validate effective state."""
    connection = op.get_bind()
    definition = connection.exec_driver_sql(
        """
        SELECT pg_get_functiondef(p.oid)
        FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
        WHERE n.nspname='dante'
          AND p.proname='enforce_occurrence_generation_integrity'
          AND p.pronargs=0
        """
    ).scalar_one()
    old = """        IF current_state IS DISTINCT FROM g.governing_recurrence_state_ref THEN
            bad := true;
        END IF;"""
    new = """        -- B06-C: an accepted Occurrence retains its exact historical governing
        -- state.  The self-scoped materialization capability validates coordinate-time
        -- effective-state precedence while this trigger continues to validate owner,
        -- family, payload, range, uniqueness and quota cardinality.
        NULL;"""
    if definition.count(old) != 1:
        raise RuntimeError("B06-C Role-13 historical-state patch point did not match once")
    old_detail = (
        "origin, current governing recurrence state and exact generated coordinate "
        "must satisfy the frozen Role-13 contract"
    )
    new_detail = (
        "origin, exact historical governing recurrence state and generated coordinate "
        "must satisfy the frozen Role-13 contract"
    )
    if definition.count(old_detail) != 1:
        raise RuntimeError("B06-C Role-13 diagnostic patch point did not match once")
    patched = definition.replace(old, new).replace(old_detail, new_detail)
    connection.exec_driver_sql(patched.replace("%", "%%"))
    connection.exec_driver_sql(
        "ALTER FUNCTION dante.enforce_occurrence_generation_integrity() OWNER TO dante_owner"
    )
    connection.exec_driver_sql(
        "REVOKE ALL PRIVILEGES ON FUNCTION dante.enforce_occurrence_generation_integrity() "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )


def _secure_function(name: str, signature: str, *, runtime_execute: bool = True) -> None:
    _sql(f"ALTER FUNCTION dante.{name}({signature}) OWNER TO {_OWNER}")
    _sql(
        f"REVOKE ALL PRIVILEGES ON FUNCTION dante.{name}({signature}) "
        f"FROM PUBLIC,{_RUNTIME},{_MIGRATOR}"
    )
    if runtime_execute:
        _sql(f"GRANT EXECUTE ON FUNCTION dante.{name}({signature}) TO {_RUNTIME}")


def _create_functions() -> None:
    for prefix, owner in (("routine", "routine_ref"), ("event", "event_ref")):
        _sql(_begin_checkpoint_function(prefix, owner))
        _sql(_history_function(prefix, owner))
        _sql(_checkpoint_results_function(prefix, owner))
        _sql(_materialize_function(prefix, owner))
        _sql(_extra_function(prefix, owner))
        _sql(_exclusion_function(prefix, owner))

        _secure_function(
            f"begin_self_{prefix}_occurrence_checkpoint",
            "uuid,text,text,uuid,date,date,text",
        )
        _secure_function(f"list_self_{prefix}_recurrence_history", "uuid,uuid")
        _secure_function(f"get_self_{prefix}_occurrence_checkpoint_result", "uuid,text,uuid")
        _secure_function(
            f"materialize_self_{prefix}_occurrence_candidate",
            "uuid,text,uuid,uuid,text,date,time,text,text,timestamptz,timestamptz,date,date,text,text,integer",
        )
        _secure_function(f"create_self_{prefix}_extra_occurrence", "uuid,text,text,uuid")
        _secure_function(
            f"exclude_self_{prefix}_occurrence_coordinate",
            "uuid,text,text,uuid,uuid,text,date,time,timestamptz,integer",
        )

    _sql(_GET_OCCURRENCE_FUNCTION)
    _sql(_SKIP_FUNCTION)
    _secure_function("get_self_occurrence", "uuid,uuid")
    _secure_function("skip_self_occurrence", "uuid,text,text,uuid,text")


# Render once so psycopg sees plain DDL, not a Python function object.
_GET_OCCURRENCE_FUNCTION = _get_occurrence_function()


def upgrade() -> None:
    _create_tables()
    _patch_role13_history()
    _retire_direct_generation_writes()
    _create_functions()


def downgrade() -> None:
    raise RuntimeError("B06-C Occurrence checkpoint requires a reviewed forward migration")
