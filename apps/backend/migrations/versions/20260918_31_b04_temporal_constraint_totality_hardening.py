"""Harden B04-A MaterialState family exclusivity before acceptance.

Revision ID: 20260918_31
Revises: 20260918_30
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260918_31"
down_revision: str | None = "20260918_30"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Count Temporal Constraint state in every MaterialState exclusivity branch."""
    op.execute(
        sa.text(
            r"""
            CREATE OR REPLACE FUNCTION dante.enforce_material_state_totality()
            RETURNS trigger
            LANGUAGE plpgsql
            SECURITY INVOKER
            VOLATILE
            PARALLEL UNSAFE
            SET search_path = pg_catalog, dante, pg_temp
            AS $function$
            DECLARE
                state_ref uuid;
                a record;
                schedule_n integer;
                actual_n integer;
                session_n integer;
                routine_n integer;
                event_n integer;
                constraint_n integer;
                owner_ok boolean := false;
            BEGIN
                state_ref := CASE WHEN TG_OP='DELETE' THEN OLD.material_state_ref ELSE NEW.material_state_ref END;
                SELECT material_state_ref,native_owner_ref,scoped_owner_ref,facet_code INTO a
                  FROM dante.material_state_address WHERE material_state_ref=state_ref;
                IF NOT FOUND THEN
                    IF TG_OP='DELETE' THEN RETURN OLD; END IF;
                    RETURN NEW;
                END IF;
                SELECT (SELECT count(*) FROM dante.schedule_placement_state WHERE material_state_ref=state_ref),
                       (SELECT count(*) FROM dante.actual_realization_state WHERE material_state_ref=state_ref),
                       (SELECT count(*) FROM dante.session_timing_state WHERE material_state_ref=state_ref),
                       (SELECT count(*) FROM dante.routine_recurrence_state WHERE material_state_ref=state_ref),
                       (SELECT count(*) FROM dante.event_recurrence_state WHERE material_state_ref=state_ref),
                       (SELECT count(*) FROM dante.temporal_constraint_state WHERE material_state_ref=state_ref)
                  INTO schedule_n,actual_n,session_n,routine_n,event_n,constraint_n;

                IF a.facet_code='temporal_constraint.rule' THEN
                    SELECT EXISTS (
                        SELECT 1
                          FROM dante.temporal_constraint_state AS s
                          JOIN dante.scoped_address AS x
                            ON x.scoped_ref=a.scoped_owner_ref
                           AND x.scoped_family='temporal_constraint'
                         WHERE s.material_state_ref=state_ref
                           AND s.constraint_ref=a.scoped_owner_ref
                           AND a.native_owner_ref IS NULL
                    ) INTO owner_ok;
                    owner_ok := owner_ok AND constraint_n=1
                        AND schedule_n+actual_n+session_n+routine_n+event_n=0;
                ELSIF a.facet_code='schedule.placement' THEN
                    SELECT EXISTS (SELECT 1 FROM dante.schedule_placement_state s JOIN dante.scoped_address x ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='schedule' WHERE s.material_state_ref=state_ref AND s.schedule_ref=a.scoped_owner_ref AND a.native_owner_ref IS NULL) INTO owner_ok;
                    owner_ok := owner_ok AND schedule_n=1 AND actual_n+session_n+routine_n+event_n+constraint_n=0;
                ELSIF a.facet_code='actual.realization' THEN
                    SELECT EXISTS (SELECT 1 FROM dante.actual_realization_state s JOIN dante.scoped_address x ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='actual' WHERE s.material_state_ref=state_ref AND s.actual_ref=a.scoped_owner_ref AND a.native_owner_ref IS NULL) INTO owner_ok;
                    owner_ok := owner_ok AND actual_n=1 AND schedule_n+session_n+routine_n+event_n+constraint_n=0;
                ELSIF a.facet_code='session.timing' THEN
                    SELECT EXISTS (SELECT 1 FROM dante.session_timing_state s JOIN dante.native_address x ON x.native_ref=a.native_owner_ref AND x.owner_family='session' WHERE s.material_state_ref=state_ref AND s.session_ref=a.native_owner_ref AND a.scoped_owner_ref IS NULL) INTO owner_ok;
                    owner_ok := owner_ok AND session_n=1 AND schedule_n+actual_n+routine_n+event_n+constraint_n=0;
                ELSIF a.facet_code='routine.recurrence' THEN
                    SELECT EXISTS (SELECT 1 FROM dante.routine_recurrence_state s JOIN dante.native_address x ON x.native_ref=a.native_owner_ref AND x.owner_family='routine' WHERE s.material_state_ref=state_ref AND s.routine_ref=a.native_owner_ref AND a.scoped_owner_ref IS NULL) INTO owner_ok;
                    owner_ok := owner_ok AND routine_n=1 AND schedule_n+actual_n+session_n+event_n+constraint_n=0;
                ELSIF a.facet_code='event.recurrence' THEN
                    SELECT EXISTS (SELECT 1 FROM dante.event_recurrence_state s JOIN dante.native_address x ON x.native_ref=a.native_owner_ref AND x.owner_family='event' WHERE s.material_state_ref=state_ref AND s.event_ref=a.native_owner_ref AND a.scoped_owner_ref IS NULL) INTO owner_ok;
                    owner_ok := owner_ok AND event_n=1 AND schedule_n+actual_n+session_n+routine_n+constraint_n=0;
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
    )


def downgrade() -> None:
    """Refuse standalone removal of an integrity hardening from the B04-A candidate."""
    raise RuntimeError(
        "B04-A totality hardening downgrade is intentionally refused; "
        "use a separately reviewed forward migration"
    )
