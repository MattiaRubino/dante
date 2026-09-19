"""Fix B04-D Schedule move acceptance replay qualification.

Revision ID: 20260919_39
Revises: 20260919_38
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260919_39"
down_revision: str | None = "20260919_38"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_OWNER = "dante_owner"
_MIGRATOR = "dante_migrator"
_RUNTIME = "dante_runtime"
_ACCEPT_SIGNATURE = (
    "dante.accept_self_absolute_schedule_move_proposal("
    "uuid,text,text,uuid,uuid)"
)


def _execute(sql: str) -> None:
    op.execute(sa.text(sql))


def upgrade() -> None:
    """Remove the PL/pgSQL output-column ambiguity from acceptance replay."""
    _execute(
        r"""
        CREATE OR REPLACE FUNCTION dante.accept_self_absolute_schedule_move_proposal(
            requested_self_person_ref uuid,
            requested_operation_id text,
            requested_intent_fingerprint text,
            requested_proposal_ref uuid,
            requested_resulting_placement_material_state_ref uuid
        )
        RETURNS TABLE(
            proposal_ref uuid,
            schedule_ref uuid,
            subject_native_ref uuid,
            previous_placement_material_state_ref uuid,
            placement_material_state_ref uuid,
            created_at timestamptz,
            replayed boolean
        )
        LANGUAGE plpgsql
        SECURITY DEFINER
        VOLATILE
        PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            normalized_operation_id text := btrim(requested_operation_id);
            proposal record;
            subject_ref uuid;
            current_placement_ref uuid;
            policy_ref uuid;
            automation_code text;
            acceptance_code text;
            recorded_at timestamptz := statement_timestamp();
            existing record;
        BEGIN
            IF normalized_operation_id='' OR char_length(normalized_operation_id)>200 THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Schedule move acceptance operation id rejected';
            END IF;
            IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Schedule move acceptance fingerprint rejected';
            END IF;
            IF uuid_extract_version(requested_proposal_ref) IS DISTINCT FROM 7
               OR uuid_extract_version(requested_resulting_placement_material_state_ref) IS DISTINCT FROM 7 THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Schedule move acceptance reference rejected';
            END IF;

            SELECT operation.* INTO existing
              FROM dante.schedule_move_accept_operation AS operation
             WHERE operation.self_person_ref=requested_self_person_ref
               AND operation.operation_id=normalized_operation_id;
            IF FOUND THEN
                IF existing.intent_fingerprint IS DISTINCT FROM requested_intent_fingerprint
                   OR existing.proposal_ref IS DISTINCT FROM requested_proposal_ref THEN
                    RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_schedule_move_accept_operation',
                        MESSAGE='Schedule move acceptance operation id reused with different intent';
                END IF;
                SELECT schedule_row.subject_native_ref INTO subject_ref
                  FROM dante.schedule AS schedule_row
                 WHERE schedule_row.schedule_ref=existing.schedule_ref;
                SELECT proposal_row.expected_placement_material_state_ref
                  INTO current_placement_ref
                  FROM dante.schedule_move_proposal AS proposal_row
                 WHERE proposal_row.proposal_ref=existing.proposal_ref;
                RETURN QUERY SELECT existing.proposal_ref,existing.schedule_ref,subject_ref,
                    current_placement_ref,existing.resulting_placement_material_state_ref,
                    existing.created_at,true;
                RETURN;
            END IF;

            SELECT proposal_row.* INTO proposal
              FROM dante.schedule_move_proposal AS proposal_row
             WHERE proposal_row.proposal_ref=requested_proposal_ref
               AND proposal_row.self_person_ref=requested_self_person_ref
             FOR UPDATE;
            IF NOT FOUND THEN
                RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='schedule_move_proposal_not_found',
                    MESSAGE='Schedule move proposal not found in self scope';
            END IF;

            PERFORM pg_advisory_xact_lock(hashtextextended(proposal.schedule_ref::text,0));
            SELECT schedule_row.subject_native_ref
              INTO subject_ref
              FROM dante.schedule AS schedule_row
              JOIN dante.native_address AS address
                ON address.native_ref=schedule_row.subject_native_ref
             WHERE schedule_row.schedule_ref=proposal.schedule_ref
               AND (
                    (address.owner_family='activity' AND EXISTS (
                        SELECT 1 FROM dante.activity_intention AS activity
                         WHERE activity.activity_ref=schedule_row.subject_native_ref
                           AND activity.self_person_ref=requested_self_person_ref
                    ))
                    OR
                    (address.owner_family='event' AND EXISTS (
                        SELECT 1 FROM dante.event_expectation AS event_row
                         WHERE event_row.event_ref=schedule_row.subject_native_ref
                           AND event_row.self_person_ref=requested_self_person_ref
                    ))
               );
            IF NOT FOUND THEN
                RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='schedule_move_schedule_not_found',
                    MESSAGE='Schedule move proposal target left self scope';
            END IF;

            SELECT current.material_state_ref INTO current_placement_ref
              FROM dante.scoped_current_material_state AS current
              JOIN dante.schedule_placement_state AS placement
                ON placement.material_state_ref=current.material_state_ref
               AND placement.schedule_ref=proposal.schedule_ref
             WHERE current.scoped_owner_ref=proposal.schedule_ref
               AND current.facet_code='schedule.placement'
             FOR UPDATE OF current;
            IF NOT FOUND OR current_placement_ref IS DISTINCT FROM proposal.expected_placement_material_state_ref THEN
                RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='schedule_move_expected_state',
                    MESSAGE='Schedule move proposal basis is stale';
            END IF;

            SELECT history.material_state_ref,state.automatic_movement_code,state.acceptance_path_code
              INTO policy_ref,automation_code,acceptance_code
              FROM dante.schedule_movement_policy_current_history AS history
              JOIN dante.schedule_movement_policy_state AS state
                ON state.schedule_ref=history.schedule_ref
               AND state.material_state_ref=history.material_state_ref
             WHERE history.schedule_ref=proposal.schedule_ref
               AND history.current_until_at IS NULL
             FOR UPDATE OF history;
            IF NOT FOUND OR policy_ref IS DISTINCT FROM proposal.movement_policy_material_state_ref
               OR automation_code IS DISTINCT FROM 'automatic'
               OR acceptance_code IS DISTINCT FROM 'confirmation_required' THEN
                RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='schedule_move_policy_state',
                    MESSAGE='Schedule move proposal Movement Policy basis is stale';
            END IF;

            IF EXISTS (
                SELECT 1 FROM dante.schedule_move_accept_operation AS accepted
                 WHERE accepted.proposal_ref=requested_proposal_ref
            ) THEN
                RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='uq_schedule_move_accept_operation_proposal_ref',
                    MESSAGE='Schedule move proposal was already accepted';
            END IF;

            PERFORM dante.assert_absolute_schedule_move_hard_admissible(
                subject_ref,proposal.starts_at,proposal.ends_at
            );
            recorded_at := dante.apply_governed_absolute_schedule_move(
                proposal.schedule_ref,
                proposal.expected_placement_material_state_ref,
                requested_resulting_placement_material_state_ref,
                proposal.starts_at,
                proposal.ends_at,
                recorded_at
            );
            PERFORM dante.assert_absolute_schedule_move_hard_admissible(
                subject_ref,proposal.starts_at,proposal.ends_at
            );

            INSERT INTO dante.schedule_move_accept_operation(
                self_person_ref,operation_id,intent_fingerprint,proposal_ref,schedule_ref,
                resulting_placement_material_state_ref,created_at
            ) VALUES (
                requested_self_person_ref,normalized_operation_id,requested_intent_fingerprint,
                requested_proposal_ref,proposal.schedule_ref,
                requested_resulting_placement_material_state_ref,recorded_at
            );
            RETURN QUERY SELECT requested_proposal_ref,proposal.schedule_ref,subject_ref,
                proposal.expected_placement_material_state_ref,
                requested_resulting_placement_material_state_ref,recorded_at,false;
        END;
        $function$
        """
    )
    _execute(f"ALTER FUNCTION {_ACCEPT_SIGNATURE} OWNER TO {_OWNER}")
    _execute(
        f"REVOKE ALL PRIVILEGES ON FUNCTION {_ACCEPT_SIGNATURE} "
        f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
    )
    _execute(f"GRANT EXECUTE ON FUNCTION {_ACCEPT_SIGNATURE} TO {_RUNTIME}")


def downgrade() -> None:
    """Refuse reintroduction of the ambiguous replay implementation."""
    raise RuntimeError(
        "B04-D acceptance replay fix downgrade is intentionally refused; "
        "do not restore the ambiguous PL/pgSQL implementation"
    )
