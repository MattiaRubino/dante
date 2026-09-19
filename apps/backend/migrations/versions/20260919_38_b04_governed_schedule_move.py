"""Activate governed B04-D automatic Schedule movement and confirmation proposals.

Revision ID: 20260919_38
Revises: 20260919_37
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260919_38"
down_revision: str | None = "20260919_37"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_MIGRATOR = "dante_migrator"
_RUNTIME = "dante_runtime"
_ASSERT_SIGNATURE = "dante.assert_absolute_schedule_move_hard_admissible(uuid,timestamptz,timestamptz)"
_APPLY_SIGNATURE = "dante.apply_governed_absolute_schedule_move(uuid,uuid,uuid,timestamptz,timestamptz,timestamptz)"
_REQUEST_SIGNATURE = (
    "dante.request_self_absolute_schedule_move("
    "uuid,text,text,uuid,uuid,timestamptz,timestamptz,uuid,uuid)"
)
_ACCEPT_SIGNATURE = (
    "dante.accept_self_absolute_schedule_move_proposal("
    "uuid,text,text,uuid,uuid)"
)


def _execute(sql: str) -> None:
    op.execute(sa.text(sql))


def upgrade() -> None:
    """Install the non-bypassable B04-D automatic-move acceptance boundary."""
    op.create_table(
        "schedule_move_proposal",
        sa.Column("proposal_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("schedule_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("expected_placement_material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("movement_policy_material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("proposal_ref", name=op.f("pk_schedule_move_proposal")),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name="fk_schedule_move_proposal_self_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["schedule_ref"],
            [f"{_SCHEMA}.schedule.schedule_ref"],
            name="fk_schedule_move_proposal_schedule",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["expected_placement_material_state_ref"],
            [f"{_SCHEMA}.schedule_placement_state.material_state_ref"],
            name="fk_schedule_move_proposal_expected_placement",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["schedule_ref", "movement_policy_material_state_ref"],
            [
                f"{_SCHEMA}.schedule_movement_policy_state.schedule_ref",
                f"{_SCHEMA}.schedule_movement_policy_state.material_state_ref",
            ],
            name="fk_schedule_move_proposal_policy_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "uuid_extract_version(proposal_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_schedule_move_proposal_uuidv7"),
        ),
        sa.CheckConstraint(
            "isfinite(starts_at) AND isfinite(ends_at) AND ends_at > starts_at",
            name=op.f("ck_schedule_move_proposal_interval"),
        ),
        sa.CheckConstraint("isfinite(created_at)", name=op.f("ck_schedule_move_proposal_created_at")),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_schedule_move_proposal_schedule_ref",
        "schedule_move_proposal",
        ["schedule_ref"],
        unique=False,
        schema=_SCHEMA,
    )

    op.create_table(
        "schedule_move_request_operation",
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("schedule_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("expected_placement_material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("movement_policy_material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("result_kind", sa.Text(), nullable=False),
        sa.Column("proposal_ref", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("resulting_placement_material_state_ref", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            name=op.f("pk_schedule_move_request_operation"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name="fk_schedule_move_request_operation_self_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["schedule_ref"],
            [f"{_SCHEMA}.schedule.schedule_ref"],
            name="fk_schedule_move_request_operation_schedule",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["expected_placement_material_state_ref"],
            [f"{_SCHEMA}.schedule_placement_state.material_state_ref"],
            name="fk_schedule_move_request_operation_expected_placement",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["schedule_ref", "movement_policy_material_state_ref"],
            [
                f"{_SCHEMA}.schedule_movement_policy_state.schedule_ref",
                f"{_SCHEMA}.schedule_movement_policy_state.material_state_ref",
            ],
            name="fk_schedule_move_request_operation_policy_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["proposal_ref"],
            [f"{_SCHEMA}.schedule_move_proposal.proposal_ref"],
            name="fk_schedule_move_request_operation_proposal",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["resulting_placement_material_state_ref"],
            [f"{_SCHEMA}.schedule_placement_state.material_state_ref"],
            name="fk_schedule_move_request_operation_resulting_placement",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.UniqueConstraint("proposal_ref", name=op.f("uq_schedule_move_request_operation_proposal_ref")),
        sa.UniqueConstraint(
            "resulting_placement_material_state_ref",
            name=op.f("uq_schedule_move_request_operation_resulting_placement"),
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name=op.f("ck_schedule_move_request_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_schedule_move_request_operation_fingerprint"),
        ),
        sa.CheckConstraint(
            "isfinite(starts_at) AND isfinite(ends_at) AND ends_at > starts_at",
            name=op.f("ck_schedule_move_request_operation_interval"),
        ),
        sa.CheckConstraint(
            "(result_kind='committed' AND proposal_ref IS NULL AND resulting_placement_material_state_ref IS NOT NULL) OR "
            "(result_kind='pending_confirmation' AND proposal_ref IS NOT NULL AND resulting_placement_material_state_ref IS NULL)",
            name=op.f("ck_schedule_move_request_operation_result_shape"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_schedule_move_request_operation_schedule_ref",
        "schedule_move_request_operation",
        ["schedule_ref"],
        unique=False,
        schema=_SCHEMA,
    )

    op.create_table(
        "schedule_move_accept_operation",
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("proposal_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("schedule_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("resulting_placement_material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            name=op.f("pk_schedule_move_accept_operation"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name="fk_schedule_move_accept_operation_self_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["proposal_ref"],
            [f"{_SCHEMA}.schedule_move_proposal.proposal_ref"],
            name="fk_schedule_move_accept_operation_proposal",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["schedule_ref"],
            [f"{_SCHEMA}.schedule.schedule_ref"],
            name="fk_schedule_move_accept_operation_schedule",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["resulting_placement_material_state_ref"],
            [f"{_SCHEMA}.schedule_placement_state.material_state_ref"],
            name="fk_schedule_move_accept_operation_resulting_placement",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.UniqueConstraint("proposal_ref", name=op.f("uq_schedule_move_accept_operation_proposal_ref")),
        sa.UniqueConstraint(
            "resulting_placement_material_state_ref",
            name=op.f("uq_schedule_move_accept_operation_resulting_placement"),
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name=op.f("ck_schedule_move_accept_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_schedule_move_accept_operation_fingerprint"),
        ),
        schema=_SCHEMA,
    )

    _execute(
        r"""
        CREATE FUNCTION dante.assert_absolute_schedule_move_hard_admissible(
            requested_subject_native_ref uuid,
            requested_starts_at timestamptz,
            requested_ends_at timestamptz
        )
        RETURNS void
        LANGUAGE plpgsql
        SECURITY DEFINER
        STABLE
        PARALLEL SAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            rule record;
            satisfied boolean;
        BEGIN
            IF requested_starts_at IS NULL OR requested_ends_at IS NULL
               OR NOT isfinite(requested_starts_at) OR NOT isfinite(requested_ends_at)
               OR requested_ends_at <= requested_starts_at THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='schedule_move_not_evaluable',
                    MESSAGE='Automatic Schedule move candidate is not an evaluable absolute interval';
            END IF;

            FOR rule IN
                SELECT state.family_code,
                       state.constrained_facet_code,
                       boundary.boundary_kind_code,
                       boundary.temporal_form_code AS boundary_form,
                       boundary_payload.boundary_at,
                       window_state.relationship_code,
                       window_state.temporal_form_code AS window_form,
                       window_payload.starts_at AS window_starts_at,
                       window_payload.ends_at AS window_ends_at
                  FROM dante.temporal_constraint AS constraint_row
                  JOIN dante.scoped_current_material_state AS current
                    ON current.scoped_owner_ref=constraint_row.constraint_ref
                   AND current.facet_code='temporal_constraint.rule'
                  JOIN dante.temporal_constraint_state AS state
                    ON state.constraint_ref=constraint_row.constraint_ref
                   AND state.material_state_ref=current.material_state_ref
                  LEFT JOIN dante.temporal_constraint_boundary_state AS boundary
                    ON boundary.material_state_ref=state.material_state_ref
                  LEFT JOIN dante.temporal_constraint_boundary_absolute_state AS boundary_payload
                    ON boundary_payload.material_state_ref=state.material_state_ref
                  LEFT JOIN dante.temporal_constraint_window_state AS window_state
                    ON window_state.material_state_ref=state.material_state_ref
                  LEFT JOIN dante.temporal_constraint_window_absolute_state AS window_payload
                    ON window_payload.material_state_ref=state.material_state_ref
                 WHERE constraint_row.subject_native_ref=requested_subject_native_ref
                   AND state.strength_code='hard'
            LOOP
                satisfied := NULL;
                IF rule.family_code='boundary' THEN
                    IF rule.boundary_form IS DISTINCT FROM 'absolute' OR rule.boundary_at IS NULL THEN
                        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='schedule_move_not_evaluable',
                            MESSAGE='Current hard Temporal Constraint cannot be evaluated for automatic movement';
                    END IF;
                    IF rule.boundary_kind_code='earliest_start'
                       AND rule.constrained_facet_code='schedule.start' THEN
                        satisfied := requested_starts_at >= rule.boundary_at;
                    ELSIF rule.boundary_kind_code='latest_start'
                       AND rule.constrained_facet_code='schedule.start' THEN
                        satisfied := requested_starts_at <= rule.boundary_at;
                    ELSIF rule.boundary_kind_code='latest_completion'
                       AND rule.constrained_facet_code='schedule.completion' THEN
                        satisfied := requested_ends_at <= rule.boundary_at;
                    ELSE
                        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='schedule_move_not_evaluable',
                            MESSAGE='Current hard Temporal Constraint boundary is outside the B04-D evaluator';
                    END IF;
                ELSIF rule.family_code='window' THEN
                    IF rule.window_form IS DISTINCT FROM 'absolute'
                       OR rule.window_starts_at IS NULL OR rule.window_ends_at IS NULL THEN
                        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='schedule_move_not_evaluable',
                            MESSAGE='Current hard Temporal Constraint window cannot be evaluated for automatic movement';
                    END IF;
                    IF rule.relationship_code='start_within'
                       AND rule.constrained_facet_code='schedule.start' THEN
                        satisfied := requested_starts_at >= rule.window_starts_at
                                     AND requested_starts_at <= rule.window_ends_at;
                    ELSIF rule.relationship_code='completion_within'
                       AND rule.constrained_facet_code='schedule.completion' THEN
                        satisfied := requested_ends_at >= rule.window_starts_at
                                     AND requested_ends_at <= rule.window_ends_at;
                    ELSIF rule.relationship_code='full_placement_contained'
                       AND rule.constrained_facet_code='schedule.placement' THEN
                        satisfied := requested_starts_at >= rule.window_starts_at
                                     AND requested_ends_at <= rule.window_ends_at;
                    ELSIF rule.relationship_code='placement_overlaps'
                       AND rule.constrained_facet_code='schedule.placement' THEN
                        satisfied := requested_starts_at < rule.window_ends_at
                                     AND requested_ends_at > rule.window_starts_at;
                    ELSE
                        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='schedule_move_not_evaluable',
                            MESSAGE='Current hard Temporal Constraint window relation is outside the B04-D evaluator';
                    END IF;
                ELSE
                    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='schedule_move_not_evaluable',
                        MESSAGE='Current hard Temporal Constraint family is outside the B04-D evaluator';
                END IF;

                IF satisfied IS DISTINCT FROM true THEN
                    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='schedule_move_hard_constraint_violation',
                        MESSAGE='Automatic Schedule move violates a current hard Temporal Constraint';
                END IF;
            END LOOP;
        END;
        $function$
        """
    )
    _execute(f"ALTER FUNCTION {_ASSERT_SIGNATURE} OWNER TO {_OWNER}")

    _execute(
        r"""
        CREATE FUNCTION dante.apply_governed_absolute_schedule_move(
            requested_schedule_ref uuid,
            requested_expected_material_state_ref uuid,
            requested_resulting_material_state_ref uuid,
            requested_starts_at timestamptz,
            requested_ends_at timestamptz,
            requested_recorded_at timestamptz
        )
        RETURNS timestamptz
        LANGUAGE plpgsql
        SECURITY DEFINER
        VOLATILE
        PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            current_state_ref uuid;
            current_from_at timestamptz;
            effective_at timestamptz;
        BEGIN
            SELECT current.material_state_ref, history.current_from_at
              INTO current_state_ref,current_from_at
              FROM dante.scoped_current_material_state AS current
              JOIN dante.schedule_placement_state AS placement
                ON placement.material_state_ref=current.material_state_ref
               AND placement.schedule_ref=requested_schedule_ref
              JOIN dante.schedule_placement_current_history AS history
                ON history.schedule_ref=requested_schedule_ref
               AND history.material_state_ref=current.material_state_ref
               AND history.current_until_at IS NULL
             WHERE current.scoped_owner_ref=requested_schedule_ref
               AND current.facet_code='schedule.placement'
             FOR UPDATE OF current,history;
            IF NOT FOUND OR current_state_ref IS DISTINCT FROM requested_expected_material_state_ref THEN
                RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='schedule_move_expected_state',
                    MESSAGE='Automatic Schedule move basis is stale';
            END IF;

            effective_at := GREATEST(requested_recorded_at, current_from_at + interval '1 microsecond');
            PERFORM dante.insert_schedule_placement_payload(
                requested_resulting_material_state_ref,
                requested_schedule_ref,
                jsonb_build_object(
                    'kind','absolute_interval',
                    'starts_at',requested_starts_at,
                    'ends_at',requested_ends_at
                )
            );
            UPDATE dante.schedule_placement_current_history AS history
               SET current_until_at=effective_at
             WHERE history.schedule_ref=requested_schedule_ref
               AND history.material_state_ref=requested_expected_material_state_ref
               AND history.current_until_at IS NULL;
            IF NOT FOUND THEN
                RAISE EXCEPTION USING ERRCODE='XX001', MESSAGE='Schedule move lost current placement history';
            END IF;
            UPDATE dante.scoped_current_material_state AS current
               SET material_state_ref=requested_resulting_material_state_ref
             WHERE current.scoped_owner_ref=requested_schedule_ref
               AND current.facet_code='schedule.placement'
               AND current.material_state_ref=requested_expected_material_state_ref;
            IF NOT FOUND THEN
                RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='schedule_move_expected_state',
                    MESSAGE='Automatic Schedule move basis changed during mutation';
            END IF;
            INSERT INTO dante.schedule_placement_current_history(
                schedule_ref,material_state_ref,current_from_at,current_until_at
            ) VALUES (
                requested_schedule_ref,requested_resulting_material_state_ref,effective_at,NULL
            );
            RETURN effective_at;
        END;
        $function$
        """
    )
    _execute(f"ALTER FUNCTION {_APPLY_SIGNATURE} OWNER TO {_OWNER}")

    _execute(
        r"""
        CREATE FUNCTION dante.request_self_absolute_schedule_move(
            requested_self_person_ref uuid,
            requested_operation_id text,
            requested_intent_fingerprint text,
            requested_schedule_ref uuid,
            requested_expected_placement_material_state_ref uuid,
            requested_starts_at timestamptz,
            requested_ends_at timestamptz,
            requested_proposal_ref uuid,
            requested_resulting_placement_material_state_ref uuid
        )
        RETURNS TABLE(
            schedule_ref uuid,
            subject_native_ref uuid,
            movement_policy_material_state_ref uuid,
            result_kind text,
            proposal_ref uuid,
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
            subject_ref uuid;
            current_placement_ref uuid;
            policy_ref uuid;
            automation_code text;
            acceptance_code text;
            recorded_at timestamptz := statement_timestamp();
            existing record;
        BEGIN
            IF normalized_operation_id='' OR char_length(normalized_operation_id)>200 THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Schedule move operation id rejected';
            END IF;
            IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Schedule move fingerprint rejected';
            END IF;
            IF uuid_extract_version(requested_schedule_ref) IS DISTINCT FROM 7
               OR uuid_extract_version(requested_expected_placement_material_state_ref) IS DISTINCT FROM 7
               OR uuid_extract_version(requested_proposal_ref) IS DISTINCT FROM 7
               OR uuid_extract_version(requested_resulting_placement_material_state_ref) IS DISTINCT FROM 7 THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Schedule move reference rejected';
            END IF;
            IF requested_starts_at IS NULL OR requested_ends_at IS NULL
               OR NOT isfinite(requested_starts_at) OR NOT isfinite(requested_ends_at)
               OR requested_ends_at <= requested_starts_at THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='schedule_move_not_evaluable',
                    MESSAGE='Automatic Schedule move candidate is not an evaluable absolute interval';
            END IF;

            SELECT operation.* INTO existing
              FROM dante.schedule_move_request_operation AS operation
             WHERE operation.self_person_ref=requested_self_person_ref
               AND operation.operation_id=normalized_operation_id;
            IF FOUND THEN
                IF existing.intent_fingerprint IS DISTINCT FROM requested_intent_fingerprint
                   OR existing.schedule_ref IS DISTINCT FROM requested_schedule_ref
                   OR existing.expected_placement_material_state_ref IS DISTINCT FROM requested_expected_placement_material_state_ref
                   OR existing.starts_at IS DISTINCT FROM requested_starts_at
                   OR existing.ends_at IS DISTINCT FROM requested_ends_at THEN
                    RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_schedule_move_request_operation',
                        MESSAGE='Schedule move operation id reused with different intent';
                END IF;
                SELECT schedule_row.subject_native_ref INTO subject_ref
                  FROM dante.schedule AS schedule_row
                 WHERE schedule_row.schedule_ref=existing.schedule_ref;
                RETURN QUERY SELECT existing.schedule_ref,subject_ref,
                    existing.movement_policy_material_state_ref,existing.result_kind,
                    existing.proposal_ref,existing.resulting_placement_material_state_ref,
                    existing.created_at,true;
                RETURN;
            END IF;

            PERFORM pg_advisory_xact_lock(hashtextextended(requested_schedule_ref::text,0));
            SELECT schedule_row.subject_native_ref
              INTO subject_ref
              FROM dante.schedule AS schedule_row
              JOIN dante.native_address AS address
                ON address.native_ref=schedule_row.subject_native_ref
             WHERE schedule_row.schedule_ref=requested_schedule_ref
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
                    MESSAGE='Automatic Schedule move self scope rejected';
            END IF;

            SELECT current.material_state_ref INTO current_placement_ref
              FROM dante.scoped_current_material_state AS current
              JOIN dante.schedule_placement_state AS placement
                ON placement.material_state_ref=current.material_state_ref
               AND placement.schedule_ref=requested_schedule_ref
             WHERE current.scoped_owner_ref=requested_schedule_ref
               AND current.facet_code='schedule.placement'
             FOR UPDATE OF current;
            IF NOT FOUND OR current_placement_ref IS DISTINCT FROM requested_expected_placement_material_state_ref THEN
                RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='schedule_move_expected_state',
                    MESSAGE='Automatic Schedule move basis is stale';
            END IF;

            SELECT history.material_state_ref,state.automatic_movement_code,state.acceptance_path_code
              INTO policy_ref,automation_code,acceptance_code
              FROM dante.schedule_movement_policy_current_history AS history
              JOIN dante.schedule_movement_policy_state AS state
                ON state.schedule_ref=history.schedule_ref
               AND state.material_state_ref=history.material_state_ref
             WHERE history.schedule_ref=requested_schedule_ref
               AND history.current_until_at IS NULL
             FOR UPDATE OF history;
            IF NOT FOUND THEN
                RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='schedule_move_policy_not_found',
                    MESSAGE='Automatic Schedule move requires a current Movement Policy';
            END IF;
            IF automation_code IS DISTINCT FROM 'automatic' THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='schedule_move_automation_blocked',
                    MESSAGE='Current Movement Policy blocks automatic movement';
            END IF;

            PERFORM dante.assert_absolute_schedule_move_hard_admissible(
                subject_ref,requested_starts_at,requested_ends_at
            );

            IF acceptance_code='direct' THEN
                recorded_at := dante.apply_governed_absolute_schedule_move(
                    requested_schedule_ref,
                    requested_expected_placement_material_state_ref,
                    requested_resulting_placement_material_state_ref,
                    requested_starts_at,
                    requested_ends_at,
                    recorded_at
                );
                PERFORM dante.assert_absolute_schedule_move_hard_admissible(
                    subject_ref,requested_starts_at,requested_ends_at
                );
                INSERT INTO dante.schedule_move_request_operation(
                    self_person_ref,operation_id,intent_fingerprint,schedule_ref,
                    expected_placement_material_state_ref,movement_policy_material_state_ref,
                    starts_at,ends_at,result_kind,proposal_ref,
                    resulting_placement_material_state_ref,created_at
                ) VALUES (
                    requested_self_person_ref,normalized_operation_id,requested_intent_fingerprint,
                    requested_schedule_ref,requested_expected_placement_material_state_ref,policy_ref,
                    requested_starts_at,requested_ends_at,'committed',NULL,
                    requested_resulting_placement_material_state_ref,recorded_at
                );
                RETURN QUERY SELECT requested_schedule_ref,subject_ref,policy_ref,'committed'::text,
                    NULL::uuid,requested_resulting_placement_material_state_ref,recorded_at,false;
                RETURN;
            ELSIF acceptance_code='confirmation_required' THEN
                INSERT INTO dante.schedule_move_proposal(
                    proposal_ref,self_person_ref,schedule_ref,
                    expected_placement_material_state_ref,movement_policy_material_state_ref,
                    starts_at,ends_at,created_at
                ) VALUES (
                    requested_proposal_ref,requested_self_person_ref,requested_schedule_ref,
                    requested_expected_placement_material_state_ref,policy_ref,
                    requested_starts_at,requested_ends_at,recorded_at
                );
                INSERT INTO dante.schedule_move_request_operation(
                    self_person_ref,operation_id,intent_fingerprint,schedule_ref,
                    expected_placement_material_state_ref,movement_policy_material_state_ref,
                    starts_at,ends_at,result_kind,proposal_ref,
                    resulting_placement_material_state_ref,created_at
                ) VALUES (
                    requested_self_person_ref,normalized_operation_id,requested_intent_fingerprint,
                    requested_schedule_ref,requested_expected_placement_material_state_ref,policy_ref,
                    requested_starts_at,requested_ends_at,'pending_confirmation',requested_proposal_ref,
                    NULL,recorded_at
                );
                RETURN QUERY SELECT requested_schedule_ref,subject_ref,policy_ref,
                    'pending_confirmation'::text,requested_proposal_ref,NULL::uuid,recorded_at,false;
                RETURN;
            END IF;

            RAISE EXCEPTION USING ERRCODE='XX001', MESSAGE='Movement Policy acceptance path is outside B04-D';
        END;
        $function$
        """
    )
    _execute(f"ALTER FUNCTION {_REQUEST_SIGNATURE} OWNER TO {_OWNER}")

    _execute(
        r"""
        CREATE FUNCTION dante.accept_self_absolute_schedule_move_proposal(
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
                SELECT expected_placement_material_state_ref INTO current_placement_ref
                  FROM dante.schedule_move_proposal
                 WHERE proposal_ref=existing.proposal_ref;
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

    for table in (
        "schedule_move_proposal",
        "schedule_move_request_operation",
        "schedule_move_accept_operation",
    ):
        _execute(
            f"REVOKE ALL PRIVILEGES ON TABLE dante.{table} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )

    for signature in (_ASSERT_SIGNATURE, _APPLY_SIGNATURE):
        _execute(
            f"REVOKE ALL PRIVILEGES ON FUNCTION {signature} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
    for signature in (_REQUEST_SIGNATURE, _ACCEPT_SIGNATURE):
        _execute(
            f"REVOKE ALL PRIVILEGES ON FUNCTION {signature} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
        _execute(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}")


def downgrade() -> None:
    """Fail closed because proposals and accepted effects are canonical history."""
    raise RuntimeError(
        "B04-D governed Schedule move downgrade is intentionally refused; use a separately "
        "reviewed forward migration to retire the capability without erasing proposal/effect history"
    )
