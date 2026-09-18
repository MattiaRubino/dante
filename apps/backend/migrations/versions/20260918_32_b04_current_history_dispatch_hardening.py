"""Harden the shared current-history dispatcher for heterogeneous owner keys.

Revision ID: 20260918_32
Revises: 20260918_31
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260918_32"
down_revision: str | None = "20260918_31"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Dispatch by history table before dereferencing its owner-specific key."""
    op.execute(
        sa.text(
            r"""
            CREATE OR REPLACE FUNCTION dante.enforce_current_history_equivalence()
            RETURNS trigger
            LANGUAGE plpgsql
            SECURITY INVOKER
            VOLATILE
            PARALLEL UNSAFE
            SET search_path = pg_catalog, dante, pg_temp
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
                IF TG_TABLE_NAME LIKE '%_current_history' THEN
                    IF TG_OP='INSERT' AND NEW.current_until_at IS NOT NULL THEN
                        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                            MESSAGE='current-history insert rejected', DETAIL='a currentness episode must begin open';
                    END IF;
                    IF TG_OP='UPDATE' THEN
                        IF TG_TABLE_NAME='schedule_placement_current_history' THEN
                            IF NEW.schedule_ref IS DISTINCT FROM OLD.schedule_ref
                               OR NEW.material_state_ref IS DISTINCT FROM OLD.material_state_ref
                               OR NEW.current_from_at IS DISTINCT FROM OLD.current_from_at THEN
                                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                                    MESSAGE='current-history identity mutation rejected';
                            END IF;
                        ELSIF TG_TABLE_NAME='actual_realization_current_history' THEN
                            IF NEW.actual_ref IS DISTINCT FROM OLD.actual_ref
                               OR NEW.material_state_ref IS DISTINCT FROM OLD.material_state_ref
                               OR NEW.current_from_at IS DISTINCT FROM OLD.current_from_at THEN
                                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                                    MESSAGE='current-history identity mutation rejected';
                            END IF;
                        ELSIF TG_TABLE_NAME='session_timing_current_history' THEN
                            IF NEW.session_ref IS DISTINCT FROM OLD.session_ref
                               OR NEW.material_state_ref IS DISTINCT FROM OLD.material_state_ref
                               OR NEW.current_from_at IS DISTINCT FROM OLD.current_from_at THEN
                                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                                    MESSAGE='current-history identity mutation rejected';
                            END IF;
                        ELSIF TG_TABLE_NAME='routine_recurrence_current_history' THEN
                            IF NEW.routine_ref IS DISTINCT FROM OLD.routine_ref
                               OR NEW.material_state_ref IS DISTINCT FROM OLD.material_state_ref
                               OR NEW.current_from_at IS DISTINCT FROM OLD.current_from_at THEN
                                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                                    MESSAGE='current-history identity mutation rejected';
                            END IF;
                        ELSIF TG_TABLE_NAME='event_recurrence_current_history' THEN
                            IF NEW.event_ref IS DISTINCT FROM OLD.event_ref
                               OR NEW.material_state_ref IS DISTINCT FROM OLD.material_state_ref
                               OR NEW.current_from_at IS DISTINCT FROM OLD.current_from_at THEN
                                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                                    MESSAGE='current-history identity mutation rejected';
                            END IF;
                        ELSIF TG_TABLE_NAME='temporal_constraint_current_history' THEN
                            IF NEW.constraint_ref IS DISTINCT FROM OLD.constraint_ref
                               OR NEW.material_state_ref IS DISTINCT FROM OLD.material_state_ref
                               OR NEW.current_from_at IS DISTINCT FROM OLD.current_from_at THEN
                                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                                    MESSAGE='current-history identity mutation rejected';
                            END IF;
                        END IF;

                        IF OLD.current_until_at IS NOT NULL
                           AND NEW.current_until_at IS DISTINCT FROM OLD.current_until_at THEN
                            RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                                MESSAGE='current-history closure mutation rejected', DETAIL='a closed currentness episode cannot be reopened or moved';
                        END IF;
                        IF OLD.current_until_at IS NULL
                           AND NEW.current_until_at IS NOT NULL
                           AND (NOT isfinite(NEW.current_until_at) OR NEW.current_until_at<=NEW.current_from_at) THEN
                            RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                                MESSAGE='current-history closure rejected';
                        END IF;
                    END IF;
                END IF;

                IF TG_TABLE_NAME='schedule_placement_current_history' THEN
                    owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.schedule_ref ELSE NEW.schedule_ref END;
                    facet:='schedule.placement';
                    history_table:='schedule';
                ELSIF TG_TABLE_NAME='actual_realization_current_history' THEN
                    owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.actual_ref ELSE NEW.actual_ref END;
                    facet:='actual.realization';
                    history_table:='actual';
                ELSIF TG_TABLE_NAME='session_timing_current_history' THEN
                    owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.session_ref ELSE NEW.session_ref END;
                    facet:='session.timing';
                    history_table:='session';
                ELSIF TG_TABLE_NAME='routine_recurrence_current_history' THEN
                    owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.routine_ref ELSE NEW.routine_ref END;
                    facet:='routine.recurrence';
                    history_table:='routine';
                ELSIF TG_TABLE_NAME='event_recurrence_current_history' THEN
                    owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.event_ref ELSE NEW.event_ref END;
                    facet:='event.recurrence';
                    history_table:='event';
                ELSIF TG_TABLE_NAME='temporal_constraint_current_history' THEN
                    owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.constraint_ref ELSE NEW.constraint_ref END;
                    facet:='temporal_constraint.rule';
                    history_table:='temporal_constraint';
                ELSIF TG_TABLE_NAME='native_current_material_state' THEN
                    owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.native_owner_ref ELSE NEW.native_owner_ref END;
                    facet:=CASE WHEN TG_OP='DELETE' THEN OLD.facet_code ELSE NEW.facet_code END;
                    history_table:=split_part(facet,'.',1);
                ELSE
                    owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.scoped_owner_ref ELSE NEW.scoped_owner_ref END;
                    facet:=CASE WHEN TG_OP='DELETE' THEN OLD.facet_code ELSE NEW.facet_code END;
                    history_table:=split_part(facet,'.',1);
                END IF;

                IF history_table='schedule' THEN
                    SELECT EXISTS (SELECT 1 FROM dante.schedule_placement_current_history a JOIN dante.schedule_placement_current_history b ON a.schedule_ref=b.schedule_ref AND (a.schedule_ref,a.current_from_at)<>(b.schedule_ref,b.current_from_at) WHERE a.schedule_ref=owner_ref AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at) AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)) INTO overlap_exists;
                    SELECT count(*) INTO open_count FROM dante.schedule_placement_current_history WHERE schedule_ref=owner_ref AND current_until_at IS NULL;
                    SELECT material_state_ref INTO open_state FROM dante.schedule_placement_current_history WHERE schedule_ref=owner_ref AND current_until_at IS NULL LIMIT 1;
                    SELECT material_state_ref INTO current_state FROM dante.scoped_current_material_state WHERE scoped_owner_ref=owner_ref AND facet_code=facet;
                ELSIF history_table='actual' THEN
                    SELECT EXISTS (SELECT 1 FROM dante.actual_realization_current_history a JOIN dante.actual_realization_current_history b ON a.actual_ref=b.actual_ref AND (a.actual_ref,a.current_from_at)<>(b.actual_ref,b.current_from_at) WHERE a.actual_ref=owner_ref AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at) AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)) INTO overlap_exists;
                    SELECT count(*) INTO open_count FROM dante.actual_realization_current_history WHERE actual_ref=owner_ref AND current_until_at IS NULL;
                    SELECT material_state_ref INTO open_state FROM dante.actual_realization_current_history WHERE actual_ref=owner_ref AND current_until_at IS NULL LIMIT 1;
                    SELECT material_state_ref INTO current_state FROM dante.scoped_current_material_state WHERE scoped_owner_ref=owner_ref AND facet_code=facet;
                ELSIF history_table='session' THEN
                    SELECT EXISTS (SELECT 1 FROM dante.session_timing_current_history a JOIN dante.session_timing_current_history b ON a.session_ref=b.session_ref AND (a.session_ref,a.current_from_at)<>(b.session_ref,b.current_from_at) WHERE a.session_ref=owner_ref AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at) AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)) INTO overlap_exists;
                    SELECT count(*) INTO open_count FROM dante.session_timing_current_history WHERE session_ref=owner_ref AND current_until_at IS NULL;
                    SELECT material_state_ref INTO open_state FROM dante.session_timing_current_history WHERE session_ref=owner_ref AND current_until_at IS NULL LIMIT 1;
                    SELECT material_state_ref INTO current_state FROM dante.native_current_material_state WHERE native_owner_ref=owner_ref AND facet_code=facet;
                ELSIF history_table='routine' THEN
                    SELECT EXISTS (SELECT 1 FROM dante.routine_recurrence_current_history a JOIN dante.routine_recurrence_current_history b ON a.routine_ref=b.routine_ref AND (a.routine_ref,a.current_from_at)<>(b.routine_ref,b.current_from_at) WHERE a.routine_ref=owner_ref AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at) AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)) INTO overlap_exists;
                    SELECT count(*) INTO open_count FROM dante.routine_recurrence_current_history WHERE routine_ref=owner_ref AND current_until_at IS NULL;
                    SELECT material_state_ref INTO open_state FROM dante.routine_recurrence_current_history WHERE routine_ref=owner_ref AND current_until_at IS NULL LIMIT 1;
                    SELECT material_state_ref INTO current_state FROM dante.native_current_material_state WHERE native_owner_ref=owner_ref AND facet_code=facet;
                ELSIF history_table='event' THEN
                    SELECT EXISTS (SELECT 1 FROM dante.event_recurrence_current_history a JOIN dante.event_recurrence_current_history b ON a.event_ref=b.event_ref AND (a.event_ref,a.current_from_at)<>(b.event_ref,b.current_from_at) WHERE a.event_ref=owner_ref AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at) AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)) INTO overlap_exists;
                    SELECT count(*) INTO open_count FROM dante.event_recurrence_current_history WHERE event_ref=owner_ref AND current_until_at IS NULL;
                    SELECT material_state_ref INTO open_state FROM dante.event_recurrence_current_history WHERE event_ref=owner_ref AND current_until_at IS NULL LIMIT 1;
                    SELECT material_state_ref INTO current_state FROM dante.native_current_material_state WHERE native_owner_ref=owner_ref AND facet_code=facet;
                ELSIF history_table='temporal_constraint' THEN
                    SELECT EXISTS (SELECT 1 FROM dante.temporal_constraint_current_history a JOIN dante.temporal_constraint_current_history b ON a.constraint_ref=b.constraint_ref AND (a.constraint_ref,a.current_from_at)<>(b.constraint_ref,b.current_from_at) WHERE a.constraint_ref=owner_ref AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at) AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)) INTO overlap_exists;
                    SELECT count(*) INTO open_count FROM dante.temporal_constraint_current_history WHERE constraint_ref=owner_ref AND current_until_at IS NULL;
                    SELECT material_state_ref INTO open_state FROM dante.temporal_constraint_current_history WHERE constraint_ref=owner_ref AND current_until_at IS NULL LIMIT 1;
                    SELECT material_state_ref INTO current_state FROM dante.scoped_current_material_state WHERE scoped_owner_ref=owner_ref AND facet_code=facet;
                ELSE
                    IF TG_OP='DELETE' THEN RETURN OLD; END IF;
                    RETURN NEW;
                END IF;

                IF overlap_exists OR open_count>1 OR current_state IS DISTINCT FROM open_state OR ((current_state IS NULL) <> (open_count=0)) THEN
                    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                        MESSAGE='current-history equivalence rejected', DETAIL='history episodes must not overlap and the sole open episode must equal the current binding';
                END IF;
                IF TG_OP='DELETE' THEN RETURN OLD; END IF;
                RETURN NEW;
            END;
            $function$
            """
        )
    )


def downgrade() -> None:
    """Refuse standalone removal of shared current-history integrity hardening."""
    raise RuntimeError(
        "B04-A current-history dispatch hardening downgrade is intentionally refused; "
        "use a separately reviewed forward migration"
    )
