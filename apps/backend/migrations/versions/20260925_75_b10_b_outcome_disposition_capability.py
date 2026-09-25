"""B10-B: materialize contextual Outcome disposition over explicit Actual truth.

Revision ID: 20260925_75
Revises: 20260925_74

Outcome is a scoped result/disposition for one explicit Actual.  This migration
intentionally does not introduce a universal Outcome taxonomy: disposition_code
is a normalized contextual code, while PostgreSQL pins every accepted Outcome
state to the exact current Actual realization MaterialState on which it rests.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260925_75"
down_revision: str | None = "20260925_74"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def upgrade() -> None:
    """Install one bounded, self-scoped Outcome path without inferring results."""
    # Extend the shared scoped/material dispatchers rather than introducing a
    # parallel current-state engine.
    op.drop_constraint(
        op.f("ck_scoped_address_scoped_family"),
        "scoped_address",
        schema=_SCHEMA,
        type_="check",
    )
    op.create_check_constraint(
        op.f("ck_scoped_address_scoped_family"),
        "scoped_address",
        "scoped_family IN ('schedule','actual','temporal_constraint','outcome')",
        schema=_SCHEMA,
    )

    op.drop_constraint(
        op.f("ck_material_state_address_facet_code"),
        "material_state_address",
        schema=_SCHEMA,
        type_="check",
    )
    op.create_check_constraint(
        op.f("ck_material_state_address_facet_code"),
        "material_state_address",
        "facet_code IN ("
        "'schedule.placement','schedule.movement_policy','actual.realization',"
        "'session.timing','routine.recurrence','event.recurrence',"
        "'temporal_constraint.rule','outcome.disposition')",
        schema=_SCHEMA,
    )

    op.drop_constraint(
        op.f("ck_scoped_current_material_state_facet_code"),
        "scoped_current_material_state",
        schema=_SCHEMA,
        type_="check",
    )
    op.create_check_constraint(
        op.f("ck_scoped_current_material_state_facet_code"),
        "scoped_current_material_state",
        "facet_code IN ("
        "'schedule.placement','actual.realization','temporal_constraint.rule',"
        "'outcome.disposition')",
        schema=_SCHEMA,
    )

    op.create_table(
        "outcome",
        sa.Column("outcome_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("actual_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("outcome_ref", name=op.f("pk_outcome")),
        sa.UniqueConstraint("actual_ref", name=op.f("uq_outcome_actual_ref")),
        sa.UniqueConstraint(
            "outcome_ref", "actual_ref", name=op.f("uq_outcome_ref_actual_ref")
        ),
        sa.CheckConstraint(
            "uuid_extract_version(outcome_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_outcome_uuidv7"),
        ),
        sa.ForeignKeyConstraint(
            ["actual_ref"],
            [f"{_SCHEMA}.actual.actual_ref"],
            name=op.f("fk_outcome_actual_ref_actual"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        schema=_SCHEMA,
    )

    op.create_table(
        "outcome_disposition_state",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("outcome_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "actual_realization_material_state_ref",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column("disposition_code", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref", name=op.f("pk_outcome_disposition_state")
        ),
        sa.UniqueConstraint(
            "outcome_ref",
            "material_state_ref",
            name=op.f("uq_outcome_disposition_state_outcome_material"),
        ),
        sa.CheckConstraint(
            "disposition_code=btrim(disposition_code) AND disposition_code<>'' "
            "AND char_length(disposition_code)<=120 "
            "AND disposition_code ~ '^[a-z0-9][a-z0-9._:-]*$'",
            name=op.f("ck_outcome_disposition_state_code"),
        ),
        sa.ForeignKeyConstraint(
            ["material_state_ref"],
            [f"{_SCHEMA}.material_state_address.material_state_ref"],
            name=op.f("fk_outcome_disposition_state_state_address"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["outcome_ref"],
            [f"{_SCHEMA}.outcome.outcome_ref"],
            name=op.f("fk_outcome_disposition_state_outcome_ref_outcome"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["actual_realization_material_state_ref"],
            [f"{_SCHEMA}.actual_realization_state.material_state_ref"],
            name=op.f("fk_outcome_disposition_state_actual_realization"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_outcome_disposition_state_outcome_ref",
        "outcome_disposition_state",
        ["outcome_ref"],
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_outcome_disposition_state_actual_realization",
        "outcome_disposition_state",
        ["actual_realization_material_state_ref"],
        schema=_SCHEMA,
    )

    op.create_table(
        "outcome_disposition_current_history",
        sa.Column("outcome_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("current_from_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_until_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "outcome_ref",
            "current_from_at",
            name=op.f("pk_outcome_disposition_current_history"),
        ),
        sa.CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at>current_from_at))",
            name=op.f("ck_outcome_disposition_current_history_interval"),
        ),
        sa.ForeignKeyConstraint(
            ["outcome_ref", "material_state_ref"],
            [
                f"{_SCHEMA}.outcome_disposition_state.outcome_ref",
                f"{_SCHEMA}.outcome_disposition_state.material_state_ref",
            ],
            name=op.f("fk_outcome_disposition_current_history_state"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ux_outcome_disposition_current_history_open",
        "outcome_disposition_current_history",
        ["outcome_ref"],
        unique=True,
        schema=_SCHEMA,
        postgresql_where=sa.text("current_until_at IS NULL"),
    )
    op.create_index(
        "ix_outcome_disposition_current_history_material_state_ref",
        "outcome_disposition_current_history",
        ["material_state_ref"],
        schema=_SCHEMA,
    )

    op.create_table(
        "outcome_disposition_operation",
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("actual_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("outcome_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "actual_realization_material_state_ref",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column("expected_material_state_ref", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("resulting_material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            name=op.f("pk_outcome_disposition_operation"),
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f("ck_outcome_disposition_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_outcome_disposition_operation_fingerprint"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name=op.f("fk_outcome_disposition_operation_self_person"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["outcome_ref", "actual_ref"],
            [f"{_SCHEMA}.outcome.outcome_ref", f"{_SCHEMA}.outcome.actual_ref"],
            name=op.f("fk_outcome_disposition_operation_outcome_actual"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["actual_realization_material_state_ref"],
            [f"{_SCHEMA}.actual_realization_state.material_state_ref"],
            name=op.f("fk_outcome_disposition_operation_actual_realization"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["outcome_ref", "expected_material_state_ref"],
            [
                f"{_SCHEMA}.outcome_disposition_state.outcome_ref",
                f"{_SCHEMA}.outcome_disposition_state.material_state_ref",
            ],
            name=op.f("fk_outcome_disposition_operation_expected_state"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["outcome_ref", "resulting_material_state_ref"],
            [
                f"{_SCHEMA}.outcome_disposition_state.outcome_ref",
                f"{_SCHEMA}.outcome_disposition_state.material_state_ref",
            ],
            name=op.f("fk_outcome_disposition_operation_resulting_state"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.UniqueConstraint(
            "resulting_material_state_ref",
            name=op.f("uq_outcome_disposition_operation_resulting_state"),
        ),
        schema=_SCHEMA,
    )

    # Bounded shared integrity dispatchers gain exactly the Outcome branch.
    _sql(
        r"""
CREATE OR REPLACE FUNCTION dante.enforce_scoped_address_owner()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
VOLATILE
PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
DECLARE owner_exists boolean := false;
BEGIN
  CASE NEW.scoped_family
    WHEN 'schedule' THEN SELECT EXISTS (SELECT 1 FROM dante.schedule WHERE schedule_ref=NEW.scoped_ref) INTO owner_exists;
    WHEN 'actual' THEN SELECT EXISTS (SELECT 1 FROM dante.actual WHERE actual_ref=NEW.scoped_ref) INTO owner_exists;
    WHEN 'temporal_constraint' THEN SELECT EXISTS (SELECT 1 FROM dante.temporal_constraint WHERE constraint_ref=NEW.scoped_ref) INTO owner_exists;
    WHEN 'outcome' THEN SELECT EXISTS (SELECT 1 FROM dante.outcome WHERE outcome_ref=NEW.scoped_ref) INTO owner_exists;
    ELSE owner_exists:=false;
  END CASE;
  IF NOT owner_exists THEN
    RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
      MESSAGE='scoped address owner binding rejected', DETAIL='scoped address must resolve to the declared bounded owner family';
  END IF;
  RETURN NEW;
END;
$function$
"""
    )

    _sql(
        r"""
CREATE OR REPLACE FUNCTION dante.enforce_material_state_totality()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
VOLATILE
PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
DECLARE
  state_ref uuid;
  a record;
  schedule_n integer;
  movement_n integer;
  actual_n integer;
  session_n integer;
  routine_n integer;
  event_n integer;
  constraint_n integer;
  outcome_n integer;
  owner_ok boolean := false;
BEGIN
  state_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.material_state_ref ELSE NEW.material_state_ref END;
  SELECT material_state_ref,native_owner_ref,scoped_owner_ref,facet_code INTO a
    FROM dante.material_state_address WHERE material_state_ref=state_ref;
  IF NOT FOUND THEN
    IF TG_OP='DELETE' THEN RETURN OLD; END IF;
    RETURN NEW;
  END IF;
  SELECT
    (SELECT count(*) FROM dante.schedule_placement_state WHERE material_state_ref=state_ref),
    (SELECT count(*) FROM dante.schedule_movement_policy_state WHERE material_state_ref=state_ref),
    (SELECT count(*) FROM dante.actual_realization_state WHERE material_state_ref=state_ref),
    (SELECT count(*) FROM dante.session_timing_state WHERE material_state_ref=state_ref),
    (SELECT count(*) FROM dante.routine_recurrence_state WHERE material_state_ref=state_ref),
    (SELECT count(*) FROM dante.event_recurrence_state WHERE material_state_ref=state_ref),
    (SELECT count(*) FROM dante.temporal_constraint_state WHERE material_state_ref=state_ref),
    (SELECT count(*) FROM dante.outcome_disposition_state WHERE material_state_ref=state_ref)
  INTO schedule_n,movement_n,actual_n,session_n,routine_n,event_n,constraint_n,outcome_n;

  IF a.facet_code='schedule.placement' THEN
    SELECT EXISTS (SELECT 1 FROM dante.schedule_placement_state s JOIN dante.scoped_address x ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='schedule' WHERE s.material_state_ref=state_ref AND s.schedule_ref=a.scoped_owner_ref AND a.native_owner_ref IS NULL) INTO owner_ok;
    owner_ok:=owner_ok AND schedule_n=1 AND movement_n+actual_n+session_n+routine_n+event_n+constraint_n+outcome_n=0;
  ELSIF a.facet_code='schedule.movement_policy' THEN
    SELECT EXISTS (SELECT 1 FROM dante.schedule_movement_policy_state s JOIN dante.scoped_address x ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='schedule' WHERE s.material_state_ref=state_ref AND s.schedule_ref=a.scoped_owner_ref AND a.native_owner_ref IS NULL) INTO owner_ok;
    owner_ok:=owner_ok AND movement_n=1 AND schedule_n+actual_n+session_n+routine_n+event_n+constraint_n+outcome_n=0;
  ELSIF a.facet_code='actual.realization' THEN
    SELECT EXISTS (SELECT 1 FROM dante.actual_realization_state s JOIN dante.scoped_address x ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='actual' WHERE s.material_state_ref=state_ref AND s.actual_ref=a.scoped_owner_ref AND a.native_owner_ref IS NULL) INTO owner_ok;
    owner_ok:=owner_ok AND actual_n=1 AND schedule_n+movement_n+session_n+routine_n+event_n+constraint_n+outcome_n=0;
  ELSIF a.facet_code='session.timing' THEN
    SELECT EXISTS (SELECT 1 FROM dante.session_timing_state s JOIN dante.native_address x ON x.native_ref=a.native_owner_ref AND x.owner_family='session' WHERE s.material_state_ref=state_ref AND s.session_ref=a.native_owner_ref AND a.scoped_owner_ref IS NULL) INTO owner_ok;
    owner_ok:=owner_ok AND session_n=1 AND schedule_n+movement_n+actual_n+routine_n+event_n+constraint_n+outcome_n=0;
  ELSIF a.facet_code='routine.recurrence' THEN
    SELECT EXISTS (SELECT 1 FROM dante.routine_recurrence_state s JOIN dante.native_address x ON x.native_ref=a.native_owner_ref AND x.owner_family='routine' WHERE s.material_state_ref=state_ref AND s.routine_ref=a.native_owner_ref AND a.scoped_owner_ref IS NULL) INTO owner_ok;
    owner_ok:=owner_ok AND routine_n=1 AND schedule_n+movement_n+actual_n+session_n+event_n+constraint_n+outcome_n=0;
  ELSIF a.facet_code='event.recurrence' THEN
    SELECT EXISTS (SELECT 1 FROM dante.event_recurrence_state s JOIN dante.native_address x ON x.native_ref=a.native_owner_ref AND x.owner_family='event' WHERE s.material_state_ref=state_ref AND s.event_ref=a.native_owner_ref AND a.scoped_owner_ref IS NULL) INTO owner_ok;
    owner_ok:=owner_ok AND event_n=1 AND schedule_n+movement_n+actual_n+session_n+routine_n+constraint_n+outcome_n=0;
  ELSIF a.facet_code='temporal_constraint.rule' THEN
    SELECT EXISTS (SELECT 1 FROM dante.temporal_constraint_state s JOIN dante.scoped_address x ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='temporal_constraint' WHERE s.material_state_ref=state_ref AND s.constraint_ref=a.scoped_owner_ref AND a.native_owner_ref IS NULL) INTO owner_ok;
    owner_ok:=owner_ok AND constraint_n=1 AND schedule_n+movement_n+actual_n+session_n+routine_n+event_n+outcome_n=0;
  ELSIF a.facet_code='outcome.disposition' THEN
    SELECT EXISTS (SELECT 1 FROM dante.outcome_disposition_state s JOIN dante.scoped_address x ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='outcome' WHERE s.material_state_ref=state_ref AND s.outcome_ref=a.scoped_owner_ref AND a.native_owner_ref IS NULL) INTO owner_ok;
    owner_ok:=owner_ok AND outcome_n=1 AND schedule_n+movement_n+actual_n+session_n+routine_n+event_n+constraint_n=0;
  END IF;
  IF NOT owner_ok THEN
    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
      MESSAGE='material state totality rejected', DETAIL='MaterialState address, bounded owner family, facet and payload must form one exact live state';
  END IF;
  IF TG_OP='DELETE' THEN RETURN OLD; END IF;
  RETURN NEW;
END;
$function$
"""
    )

    _sql(
        r"""
CREATE OR REPLACE FUNCTION dante.enforce_current_history_equivalence()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
VOLATILE
PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
DECLARE
  owner_ref uuid;
  facet text;
  history_table text;
  overlap_exists boolean := false;
  open_count integer := 0;
  current_state uuid;
  open_state uuid;
BEGIN
  IF TG_TABLE_NAME LIKE '%_current_history' AND TG_OP='INSERT' AND NEW.current_until_at IS NOT NULL THEN
    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
      MESSAGE='current-history insertion rejected', DETAIL='new history episodes must begin open';
  END IF;

  IF TG_TABLE_NAME='schedule_placement_current_history' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.schedule_ref ELSE NEW.schedule_ref END; facet:='schedule.placement'; history_table:='schedule';
  ELSIF TG_TABLE_NAME='actual_realization_current_history' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.actual_ref ELSE NEW.actual_ref END; facet:='actual.realization'; history_table:='actual';
  ELSIF TG_TABLE_NAME='session_timing_current_history' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.session_ref ELSE NEW.session_ref END; facet:='session.timing'; history_table:='session';
  ELSIF TG_TABLE_NAME='routine_recurrence_current_history' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.routine_ref ELSE NEW.routine_ref END; facet:='routine.recurrence'; history_table:='routine';
  ELSIF TG_TABLE_NAME='event_recurrence_current_history' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.event_ref ELSE NEW.event_ref END; facet:='event.recurrence'; history_table:='event';
  ELSIF TG_TABLE_NAME='temporal_constraint_current_history' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.constraint_ref ELSE NEW.constraint_ref END; facet:='temporal_constraint.rule'; history_table:='temporal_constraint';
  ELSIF TG_TABLE_NAME='outcome_disposition_current_history' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.outcome_ref ELSE NEW.outcome_ref END; facet:='outcome.disposition'; history_table:='outcome';
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
  ELSIF history_table='temporal_constraint' THEN
    SELECT EXISTS (SELECT 1 FROM dante.temporal_constraint_current_history a JOIN dante.temporal_constraint_current_history b ON a.constraint_ref=b.constraint_ref AND (a.constraint_ref,a.current_from_at)<>(b.constraint_ref,b.current_from_at) WHERE a.constraint_ref=owner_ref AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at) AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)) INTO overlap_exists;
    SELECT count(*) INTO open_count FROM dante.temporal_constraint_current_history WHERE constraint_ref=owner_ref AND current_until_at IS NULL; SELECT material_state_ref INTO open_state FROM dante.temporal_constraint_current_history WHERE constraint_ref=owner_ref AND current_until_at IS NULL LIMIT 1;
    SELECT material_state_ref INTO current_state FROM dante.scoped_current_material_state WHERE scoped_owner_ref=owner_ref AND facet_code=facet;
  ELSIF history_table='outcome' THEN
    SELECT EXISTS (SELECT 1 FROM dante.outcome_disposition_current_history a JOIN dante.outcome_disposition_current_history b ON a.outcome_ref=b.outcome_ref AND (a.outcome_ref,a.current_from_at)<>(b.outcome_ref,b.current_from_at) WHERE a.outcome_ref=owner_ref AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at) AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)) INTO overlap_exists;
    SELECT count(*) INTO open_count FROM dante.outcome_disposition_current_history WHERE outcome_ref=owner_ref AND current_until_at IS NULL; SELECT material_state_ref INTO open_state FROM dante.outcome_disposition_current_history WHERE outcome_ref=owner_ref AND current_until_at IS NULL LIMIT 1;
    SELECT material_state_ref INTO current_state FROM dante.scoped_current_material_state WHERE scoped_owner_ref=owner_ref AND facet_code=facet;
  ELSE
    IF TG_OP='DELETE' THEN RETURN OLD; END IF;
    RETURN NEW;
  END IF;

  IF overlap_exists OR open_count>1 OR current_state IS DISTINCT FROM open_state OR ((current_state IS NULL)<>(open_count=0)) THEN
    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
      MESSAGE='current-history equivalence rejected', DETAIL='history episodes must not overlap and the sole open episode must equal the current binding';
  END IF;
  IF TG_OP='DELETE' THEN RETURN OLD; END IF;
  RETURN NEW;
END;
$function$
"""
    )

    _sql(
        r"""
CREATE OR REPLACE FUNCTION dante.enforce_owner_creation_completeness()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
VOLATILE
PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
DECLARE owner_ref uuid; ok boolean := false;
BEGIN
  IF TG_TABLE_NAME='schedule' THEN owner_ref:=NEW.schedule_ref; SELECT EXISTS (SELECT 1 FROM dante.scoped_current_material_state WHERE scoped_owner_ref=owner_ref AND facet_code='schedule.placement') INTO ok;
  ELSIF TG_TABLE_NAME='actual' THEN owner_ref:=NEW.actual_ref; SELECT EXISTS (SELECT 1 FROM dante.scoped_current_material_state WHERE scoped_owner_ref=owner_ref AND facet_code='actual.realization') INTO ok;
  ELSIF TG_TABLE_NAME='temporal_constraint' THEN owner_ref:=NEW.constraint_ref; SELECT EXISTS (SELECT 1 FROM dante.scoped_current_material_state WHERE scoped_owner_ref=owner_ref AND facet_code='temporal_constraint.rule') INTO ok;
  ELSIF TG_TABLE_NAME='outcome' THEN owner_ref:=NEW.outcome_ref; SELECT EXISTS (SELECT 1 FROM dante.scoped_current_material_state WHERE scoped_owner_ref=owner_ref AND facet_code='outcome.disposition') INTO ok;
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
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.enforce_outcome_disposition_basis()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
VOLATILE
PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
DECLARE expected_actual_ref uuid;
BEGIN
  SELECT owner.actual_ref INTO expected_actual_ref
    FROM dante.outcome AS owner
   WHERE owner.outcome_ref=NEW.outcome_ref;
  IF expected_actual_ref IS NULL OR NOT EXISTS (
    SELECT 1 FROM dante.actual_realization_state AS realization
     WHERE realization.material_state_ref=NEW.actual_realization_material_state_ref
       AND realization.actual_ref=expected_actual_ref
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
      MESSAGE='Outcome Actual basis rejected', DETAIL='Outcome disposition must reference a realization state of its exact Actual';
  END IF;
  RETURN NEW;
END;
$function$
"""
    )

    _sql(
        "CREATE TRIGGER trg_outcome_disposition_state_actual_basis "
        "BEFORE INSERT OR UPDATE ON dante.outcome_disposition_state "
        "FOR EACH ROW EXECUTE FUNCTION dante.enforce_outcome_disposition_basis()"
    )
    _sql(
        "CREATE CONSTRAINT TRIGGER ctrg_outcome_disposition_state_state_totality "
        "AFTER INSERT OR UPDATE OR DELETE ON dante.outcome_disposition_state "
        "DEFERRABLE INITIALLY DEFERRED FOR EACH ROW "
        "EXECUTE FUNCTION dante.enforce_material_state_totality()"
    )
    _sql(
        "CREATE CONSTRAINT TRIGGER ctrg_outcome_disposition_current_history_current_history "
        "AFTER INSERT OR UPDATE OR DELETE ON dante.outcome_disposition_current_history "
        "DEFERRABLE INITIALLY DEFERRED FOR EACH ROW "
        "EXECUTE FUNCTION dante.enforce_current_history_equivalence()"
    )
    _sql(
        "CREATE CONSTRAINT TRIGGER ctrg_outcome_owner_complete "
        "AFTER INSERT ON dante.outcome DEFERRABLE INITIALLY DEFERRED FOR EACH ROW "
        "EXECUTE FUNCTION dante.enforce_owner_creation_completeness()"
    )

    _sql(
        r"""
CREATE VIEW dante.outcome_current_disposition AS
SELECT current.scoped_owner_ref,
       current.material_state_ref,
       state.actual_realization_material_state_ref,
       state.disposition_code
  FROM dante.scoped_current_material_state AS current
  JOIN dante.scoped_address AS scoped
    ON scoped.scoped_ref=current.scoped_owner_ref
   AND scoped.scoped_family='outcome'
  JOIN dante.outcome_disposition_state AS state
    ON state.outcome_ref=current.scoped_owner_ref
   AND state.material_state_ref=current.material_state_ref
 WHERE current.facet_code='outcome.disposition'
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante._outcome_actual_owned(
  requested_self_person_ref uuid,
  requested_actual_ref uuid
) RETURNS boolean
LANGUAGE sql
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT EXISTS (
    SELECT 1
      FROM dante.actual AS owner
     WHERE owner.actual_ref=requested_actual_ref
       AND dante._actual_subject_owned(
         requested_self_person_ref,
         owner.subject_native_ref
       )
  );
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.record_self_actual_outcome(
  requested_self_person_ref uuid,
  requested_operation_id text,
  requested_intent_fingerprint text,
  requested_outcome_ref uuid,
  requested_material_state_ref uuid,
  requested_actual_ref uuid,
  requested_actual_realization_material_state_ref uuid,
  requested_expected_material_state_ref uuid,
  requested_disposition_code text
) RETURNS TABLE(
  outcome_ref uuid,
  actual_ref uuid,
  material_state_ref uuid,
  actual_realization_material_state_ref uuid,
  disposition_code text,
  replayed boolean
)
LANGUAGE plpgsql
SECURITY DEFINER
VOLATILE
PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
DECLARE
  normalized_operation_id text:=btrim(requested_operation_id);
  normalized_disposition text:=btrim(requested_disposition_code);
  existing_fingerprint text;
  receipt_outcome_ref uuid;
  receipt_actual_ref uuid;
  receipt_state_ref uuid;
  resolved_outcome_ref uuid;
  current_actual_state_ref uuid;
  current_outcome_state_ref uuid;
  current_from timestamptz;
  recorded_at timestamptz:=statement_timestamp();
BEGIN
  IF NOT dante._outcome_actual_owned(requested_self_person_ref, requested_actual_ref) THEN
    RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='outcome_actual_unavailable', MESSAGE='Outcome Actual unavailable';
  END IF;
  IF normalized_operation_id='' OR char_length(normalized_operation_id)>200 THEN
    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_outcome_disposition_operation_operation_id', MESSAGE='Outcome operation id rejected';
  END IF;
  IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_outcome_disposition_operation_fingerprint', MESSAGE='Outcome operation fingerprint rejected';
  END IF;
  IF normalized_disposition='' OR char_length(normalized_disposition)>120 OR normalized_disposition !~ '^[a-z0-9][a-z0-9._:-]*$' THEN
    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_outcome_disposition_state_code', MESSAGE='Outcome disposition code rejected';
  END IF;
  IF uuid_extract_version(requested_outcome_ref) IS DISTINCT FROM 7 OR uuid_extract_version(requested_material_state_ref) IS DISTINCT FROM 7 THEN
    RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Outcome reference rejected';
  END IF;

  PERFORM pg_advisory_xact_lock(hashtextextended(requested_self_person_ref::text || ':outcome-op:' || normalized_operation_id,0));
  SELECT operation.intent_fingerprint,operation.outcome_ref,operation.actual_ref,operation.resulting_material_state_ref
    INTO existing_fingerprint,receipt_outcome_ref,receipt_actual_ref,receipt_state_ref
    FROM dante.outcome_disposition_operation AS operation
   WHERE operation.self_person_ref=requested_self_person_ref
     AND operation.operation_id=normalized_operation_id;
  IF FOUND THEN
    IF existing_fingerprint<>requested_intent_fingerprint OR receipt_actual_ref<>requested_actual_ref THEN
      RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='outcome_operation_reused', MESSAGE='Outcome operation id reused with different intent';
    END IF;
    RETURN QUERY
    SELECT state.outcome_ref, owner.actual_ref, state.material_state_ref,
           state.actual_realization_material_state_ref, state.disposition_code, true
      FROM dante.outcome_disposition_state AS state
      JOIN dante.outcome AS owner ON owner.outcome_ref=state.outcome_ref
     WHERE state.outcome_ref=receipt_outcome_ref
       AND state.material_state_ref=receipt_state_ref;
    RETURN;
  END IF;

  SELECT current.material_state_ref INTO current_actual_state_ref
    FROM dante.scoped_current_material_state AS current
    JOIN dante.actual_realization_state AS realization
      ON realization.actual_ref=requested_actual_ref
     AND realization.material_state_ref=current.material_state_ref
   WHERE current.scoped_owner_ref=requested_actual_ref
     AND current.facet_code='actual.realization'
   FOR SHARE OF current;
  IF current_actual_state_ref IS NULL THEN
    RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='outcome_actual_unavailable', MESSAGE='Outcome requires a current Actual realization';
  END IF;
  IF current_actual_state_ref IS DISTINCT FROM requested_actual_realization_material_state_ref THEN
    RAISE EXCEPTION USING ERRCODE='40001', CONSTRAINT='outcome_actual_changed', MESSAGE='Outcome Actual realization basis is stale';
  END IF;

  PERFORM pg_advisory_xact_lock(hashtextextended('outcome-actual:' || requested_actual_ref::text,0));
  SELECT owner.outcome_ref INTO resolved_outcome_ref
    FROM dante.outcome AS owner
   WHERE owner.actual_ref=requested_actual_ref;
  IF resolved_outcome_ref IS NULL THEN
    IF requested_expected_material_state_ref IS NOT NULL THEN
      RAISE EXCEPTION USING ERRCODE='40001', CONSTRAINT='outcome_current_conflict', MESSAGE='Outcome expected current state does not exist';
    END IF;
    resolved_outcome_ref:=requested_outcome_ref;
    INSERT INTO dante.outcome(outcome_ref,actual_ref) VALUES (resolved_outcome_ref,requested_actual_ref);
    INSERT INTO dante.scoped_address(scoped_ref,scoped_family) VALUES (resolved_outcome_ref,'outcome');
  ELSE
    SELECT current.material_state_ref,history.current_from_at
      INTO current_outcome_state_ref,current_from
      FROM dante.scoped_current_material_state AS current
      JOIN dante.outcome_disposition_current_history AS history
        ON history.outcome_ref=resolved_outcome_ref
       AND history.material_state_ref=current.material_state_ref
       AND history.current_until_at IS NULL
     WHERE current.scoped_owner_ref=resolved_outcome_ref
       AND current.facet_code='outcome.disposition'
     FOR UPDATE OF history;
    IF current_outcome_state_ref IS DISTINCT FROM requested_expected_material_state_ref THEN
      RAISE EXCEPTION USING ERRCODE='40001', CONSTRAINT='outcome_current_conflict', MESSAGE='Outcome expected current disposition is stale';
    END IF;
  END IF;

  IF current_from IS NOT NULL AND recorded_at<=current_from THEN recorded_at:=current_from+interval '1 microsecond'; END IF;

  INSERT INTO dante.material_state_address(material_state_ref,scoped_owner_ref,facet_code)
  VALUES (requested_material_state_ref,resolved_outcome_ref,'outcome.disposition');
  INSERT INTO dante.outcome_disposition_state(material_state_ref,outcome_ref,actual_realization_material_state_ref,disposition_code)
  VALUES (requested_material_state_ref,resolved_outcome_ref,requested_actual_realization_material_state_ref,normalized_disposition);

  IF current_outcome_state_ref IS NULL THEN
    INSERT INTO dante.scoped_current_material_state(scoped_owner_ref,facet_code,material_state_ref)
    VALUES (resolved_outcome_ref,'outcome.disposition',requested_material_state_ref);
  ELSE
    UPDATE dante.outcome_disposition_current_history SET current_until_at=recorded_at
     WHERE outcome_ref=resolved_outcome_ref AND current_until_at IS NULL;
    UPDATE dante.scoped_current_material_state SET material_state_ref=requested_material_state_ref
     WHERE scoped_owner_ref=resolved_outcome_ref AND facet_code='outcome.disposition';
  END IF;
  INSERT INTO dante.outcome_disposition_current_history(outcome_ref,material_state_ref,current_from_at)
  VALUES (resolved_outcome_ref,requested_material_state_ref,recorded_at);
  INSERT INTO dante.outcome_disposition_operation(
    self_person_ref,operation_id,intent_fingerprint,actual_ref,outcome_ref,
    actual_realization_material_state_ref,expected_material_state_ref,
    resulting_material_state_ref,created_at
  ) VALUES (
    requested_self_person_ref,normalized_operation_id,requested_intent_fingerprint,
    requested_actual_ref,resolved_outcome_ref,requested_actual_realization_material_state_ref,
    requested_expected_material_state_ref,requested_material_state_ref,recorded_at
  );

  RETURN QUERY SELECT resolved_outcome_ref,requested_actual_ref,requested_material_state_ref,
    requested_actual_realization_material_state_ref,normalized_disposition,false;
END;
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.get_self_actual_outcome(
  requested_self_person_ref uuid,
  requested_actual_ref uuid
) RETURNS TABLE(
  outcome_ref uuid,
  actual_ref uuid,
  material_state_ref uuid,
  actual_realization_material_state_ref uuid,
  disposition_code text
)
LANGUAGE plpgsql
SECURITY DEFINER
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
DECLARE current_actual_state_ref uuid; outcome_actual_state_ref uuid;
BEGIN
  IF NOT dante._outcome_actual_owned(requested_self_person_ref,requested_actual_ref) THEN RETURN; END IF;
  SELECT current.material_state_ref INTO current_actual_state_ref
    FROM dante.scoped_current_material_state AS current
   WHERE current.scoped_owner_ref=requested_actual_ref AND current.facet_code='actual.realization';
  RETURN QUERY
  SELECT owner.outcome_ref,owner.actual_ref,state.material_state_ref,
         state.actual_realization_material_state_ref,state.disposition_code
    FROM dante.outcome AS owner
    JOIN dante.outcome_current_disposition AS current ON current.scoped_owner_ref=owner.outcome_ref
    JOIN dante.outcome_disposition_state AS state
      ON state.outcome_ref=owner.outcome_ref AND state.material_state_ref=current.material_state_ref
   WHERE owner.actual_ref=requested_actual_ref;
  IF FOUND THEN
    SELECT state.actual_realization_material_state_ref INTO outcome_actual_state_ref
      FROM dante.outcome AS owner
      JOIN dante.outcome_current_disposition AS current ON current.scoped_owner_ref=owner.outcome_ref
      JOIN dante.outcome_disposition_state AS state ON state.outcome_ref=owner.outcome_ref AND state.material_state_ref=current.material_state_ref
     WHERE owner.actual_ref=requested_actual_ref;
    IF current_actual_state_ref IS NULL OR outcome_actual_state_ref IS DISTINCT FROM current_actual_state_ref THEN
      RAISE EXCEPTION USING ERRCODE='40001', CONSTRAINT='outcome_actual_changed', MESSAGE='Outcome no longer matches the current Actual realization';
    END IF;
  END IF;
END;
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.list_self_outcome_history(
  requested_self_person_ref uuid,
  requested_outcome_ref uuid
) RETURNS TABLE(
  outcome_ref uuid,
  actual_ref uuid,
  material_state_ref uuid,
  actual_realization_material_state_ref uuid,
  disposition_code text,
  current_from_at timestamptz,
  current_until_at timestamptz
)
LANGUAGE sql
SECURITY DEFINER
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT owner.outcome_ref,owner.actual_ref,state.material_state_ref,
         state.actual_realization_material_state_ref,state.disposition_code,
         history.current_from_at,history.current_until_at
    FROM dante.outcome AS owner
    JOIN dante.outcome_disposition_state AS state ON state.outcome_ref=owner.outcome_ref
    JOIN dante.outcome_disposition_current_history AS history
      ON history.outcome_ref=owner.outcome_ref AND history.material_state_ref=state.material_state_ref
   WHERE owner.outcome_ref=requested_outcome_ref
     AND dante._outcome_actual_owned(requested_self_person_ref,owner.actual_ref)
   ORDER BY history.current_from_at DESC;
$function$
"""
    )

    # New Outcome relations remain behind SECURITY DEFINER routines.
    for relation in (
        "outcome",
        "outcome_disposition_state",
        "outcome_disposition_current_history",
        "outcome_disposition_operation",
    ):
        _sql(f"ALTER TABLE dante.{relation} OWNER TO {_OWNER}")
        _sql(f"REVOKE ALL ON TABLE dante.{relation} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}")

    _sql("ALTER VIEW dante.outcome_current_disposition OWNER TO dante_owner")
    _sql("REVOKE ALL ON dante.outcome_current_disposition FROM PUBLIC, dante_runtime, dante_migrator")

    signatures = (
        "dante._outcome_actual_owned(uuid,uuid)",
        "dante.enforce_outcome_disposition_basis()",
        "dante.record_self_actual_outcome(uuid,text,text,uuid,uuid,uuid,uuid,uuid,text)",
        "dante.get_self_actual_outcome(uuid,uuid)",
        "dante.list_self_outcome_history(uuid,uuid)",
    )
    for signature in signatures:
        _sql(f"ALTER FUNCTION {signature} OWNER TO {_OWNER}")
        _sql(f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}")
    for signature in signatures[2:]:
        _sql(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}")


def downgrade() -> None:
    raise RuntimeError(
        "B10-B Outcome downgrade is intentionally refused; use a separately reviewed forward migration"
    )
