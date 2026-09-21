# ruff: noqa: S608
"""B06-A repair: qualify Routine SQL against PL/pgSQL output variables.

The B06-A functions deliberately use ``#variable_conflict error``.  Their
``RETURNS TABLE`` field names are therefore PL/pgSQL variables too; every
same-named relation column must be qualified.  This forward-only repair
removes the ambiguous Routine source and Life Area statements rather than
weakening that guardrail.

Revision ID: 20260921_51
Revises: 20260921_50
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260921_51"
down_revision: str | None = "20260921_50"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    for statement in (_MUTATE_ROUTINE, _ASSIGN_LIFE_AREA):
        op.execute(sa.text(statement))


def downgrade() -> None:
    raise RuntimeError("B06-A SQL qualification repair requires a reviewed forward migration")


_MUTATE_ROUTINE = r'''
CREATE OR REPLACE FUNCTION dante.mutate_self_routine(
    requested_self_person_ref uuid, requested_operation_id text, requested_intent_fingerprint text,
    requested_routine_ref uuid, requested_expected_source_revision bigint, requested_kind text,
    requested_title text
) RETURNS TABLE(routine_ref uuid, source_revision bigint, lifecycle_state text, accepted_at timestamptz, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path = pg_catalog, dante, pg_temp AS $function$
#variable_conflict error
DECLARE
    key text := btrim(requested_operation_id);
    label text := btrim(requested_title);
    prior dante.routine_operation%ROWTYPE;
    current_source dante.routine_intention%ROWTYPE;
    recorded_at timestamptz := statement_timestamp();
BEGIN
    IF key IS NULL OR key='' OR char_length(key)>200
       OR requested_intent_fingerprint IS NULL OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$'
       OR requested_expected_source_revision IS NULL OR requested_expected_source_revision<1
       OR requested_kind NOT IN ('rename','pause','resume','end')
       OR (requested_kind='rename' AND (label IS NULL OR label='' OR char_length(label)>300))
       OR (requested_kind<>'rename' AND requested_title IS NOT NULL) THEN
        RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Routine mutation command rejected';
    END IF;
    PERFORM 1 FROM dante.person AS person
      WHERE person.person_ref=requested_self_person_ref FOR UPDATE;
    IF NOT FOUND OR NOT EXISTS (
        SELECT 1 FROM dante.account_application_context AS application_context
          WHERE application_context.self_person_ref=requested_self_person_ref
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Routine self context unavailable';
    END IF;
    SELECT receipt.* INTO prior
      FROM dante.routine_operation AS receipt
     WHERE receipt.self_person_ref=requested_self_person_ref
       AND receipt.operation_id=key;
    IF FOUND THEN
        IF prior.intent_fingerprint<>requested_intent_fingerprint
           OR prior.routine_ref<>requested_routine_ref
           OR prior.kind<>requested_kind
           OR prior.expected_source_revision<>requested_expected_source_revision THEN
            RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_routine_operation',
                MESSAGE='Routine operation id reused';
        END IF;
        SELECT source.* INTO current_source
          FROM dante.routine_intention AS source
         WHERE source.routine_ref=requested_routine_ref;
        RETURN QUERY SELECT prior.routine_ref, prior.accepted_source_revision,
                            current_source.lifecycle_state, prior.accepted_at, true;
        RETURN;
    END IF;
    SELECT source.* INTO current_source
      FROM dante.routine_intention AS source
     WHERE source.routine_ref=requested_routine_ref
       AND source.self_person_ref=requested_self_person_ref
     FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='routine_unavailable',
            MESSAGE='Routine unavailable';
    END IF;
    IF current_source.source_revision<>requested_expected_source_revision
       OR (requested_kind='rename' AND current_source.title=label)
       OR (requested_kind='pause' AND current_source.lifecycle_state<>'active')
       OR (requested_kind='resume' AND current_source.lifecycle_state<>'paused')
       OR (requested_kind='end' AND current_source.lifecycle_state='ended') THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='routine_source_conflict',
            MESSAGE='Routine source state changed';
    END IF;
    UPDATE dante.routine_intention AS source
       SET title=CASE WHEN requested_kind='rename' THEN label ELSE source.title END,
           lifecycle_state=CASE
               WHEN requested_kind='pause' THEN 'paused'
               WHEN requested_kind='resume' THEN 'active'
               WHEN requested_kind='end' THEN 'ended'
               ELSE source.lifecycle_state
           END,
           source_revision=source.source_revision+1,
           updated_at=recorded_at,
           lifecycle_changed_at=CASE
               WHEN requested_kind IN ('pause','resume','end') THEN recorded_at
               ELSE source.lifecycle_changed_at
           END
     WHERE source.routine_ref=requested_routine_ref;
    INSERT INTO dante.routine_operation(
        self_person_ref, operation_id, intent_fingerprint, routine_ref, kind,
        expected_source_revision, accepted_source_revision, accepted_at
    ) VALUES (
        requested_self_person_ref, key, requested_intent_fingerprint, requested_routine_ref,
        requested_kind, requested_expected_source_revision,
        requested_expected_source_revision+1, recorded_at
    );
    SELECT source.* INTO current_source
      FROM dante.routine_intention AS source
     WHERE source.routine_ref=requested_routine_ref;
    RETURN QUERY SELECT requested_routine_ref, requested_expected_source_revision+1,
                        current_source.lifecycle_state, recorded_at, false;
END;
$function$;
'''


_ASSIGN_LIFE_AREA = r'''
CREATE OR REPLACE FUNCTION dante.assign_self_routine_life_area(
    requested_self_person_ref uuid, requested_operation_id text, requested_intent_fingerprint text,
    requested_routine_ref uuid, requested_life_area_ref uuid, requested_expected_revision bigint
) RETURNS TABLE(life_area_ref uuid, assignment_revision bigint, assigned_at timestamptz, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path = pg_catalog, dante, pg_temp AS $function$
#variable_conflict error
DECLARE
    key text := btrim(requested_operation_id);
    prior dante.routine_life_area_assignment_operation%ROWTYPE;
    current_assignment dante.routine_life_area_assignment%ROWTYPE;
    recorded_at timestamptz := statement_timestamp();
BEGIN
    IF key IS NULL OR key='' OR char_length(key)>200
       OR requested_intent_fingerprint IS NULL OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$'
       OR requested_expected_revision IS NULL OR requested_expected_revision<1 THEN
        RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Routine Life Area command rejected';
    END IF;
    PERFORM 1 FROM dante.person AS person
      WHERE person.person_ref=requested_self_person_ref FOR UPDATE;
    IF NOT FOUND OR NOT EXISTS (
        SELECT 1 FROM dante.account_application_context AS application_context
          WHERE application_context.self_person_ref=requested_self_person_ref
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Routine self context unavailable';
    END IF;
    SELECT receipt.* INTO prior
      FROM dante.routine_life_area_assignment_operation AS receipt
     WHERE receipt.self_person_ref=requested_self_person_ref
       AND receipt.operation_id=key;
    IF FOUND THEN
        IF prior.intent_fingerprint<>requested_intent_fingerprint
           OR prior.routine_ref<>requested_routine_ref
           OR prior.life_area_ref<>requested_life_area_ref
           OR prior.expected_revision<>requested_expected_revision THEN
            RAISE EXCEPTION USING ERRCODE='23505',
                CONSTRAINT='pk_routine_life_area_assignment_operation',
                MESSAGE='Routine Life Area operation id reused';
        END IF;
        RETURN QUERY SELECT prior.life_area_ref, prior.accepted_revision, prior.accepted_at, true;
        RETURN;
    END IF;
    IF NOT EXISTS (
        SELECT 1 FROM dante.routine_intention AS source
         WHERE source.routine_ref=requested_routine_ref
           AND source.self_person_ref=requested_self_person_ref
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='routine_unavailable',
            MESSAGE='Routine unavailable';
    END IF;
    IF NOT EXISTS (
        SELECT 1 FROM dante.life_area AS area
         WHERE area.life_area_ref=requested_life_area_ref
           AND area.self_person_ref=requested_self_person_ref
           AND area.archived=false
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='routine_life_area_unavailable',
            MESSAGE='Routine Life Area unavailable';
    END IF;
    SELECT assignment.* INTO current_assignment
      FROM dante.routine_life_area_assignment AS assignment
     WHERE assignment.self_person_ref=requested_self_person_ref
       AND assignment.routine_ref=requested_routine_ref
     FOR UPDATE;
    IF NOT FOUND
       OR current_assignment.revision<>requested_expected_revision
       OR current_assignment.life_area_ref=requested_life_area_ref THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='routine_life_area_conflict',
            MESSAGE='Routine Life Area state changed';
    END IF;
    UPDATE dante.routine_life_area_assignment AS assignment
       SET life_area_ref=requested_life_area_ref,
           revision=assignment.revision+1,
           assigned_at=recorded_at
     WHERE assignment.self_person_ref=requested_self_person_ref
       AND assignment.routine_ref=requested_routine_ref;
    INSERT INTO dante.routine_life_area_assignment_operation(
        self_person_ref, operation_id, intent_fingerprint, routine_ref, life_area_ref,
        expected_revision, accepted_revision, accepted_at
    ) VALUES (
        requested_self_person_ref, key, requested_intent_fingerprint, requested_routine_ref,
        requested_life_area_ref, requested_expected_revision,
        requested_expected_revision+1, recorded_at
    );
    RETURN QUERY SELECT requested_life_area_ref, requested_expected_revision+1, recorded_at, false;
END;
$function$;
'''
