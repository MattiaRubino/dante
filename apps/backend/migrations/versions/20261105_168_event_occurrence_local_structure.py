"""Store bounded Event-only local structure in the versioned Occurrence edit.

The existing owner-checked, source-locked Occurrence edit remains the single
CAS and replay boundary. A local Event patch can carry its own Agenda, Life
Area and expected participants without modifying the recurring Event source.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261105_168"
down_revision: str | None = "20261104_167"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.get_bind().execute(sa.text(_ACCEPT_EDIT))
    op.get_bind().execute(sa.text(_RETIRE))


def downgrade() -> None:
    raise RuntimeError("20261105_168 is forward-only")


_ACCEPT_EDIT = r"""
CREATE OR REPLACE FUNCTION dante.accept_self_occurrence_profile_edit(
    actor uuid, selected_ref uuid, requested_operation text,
    requested_expected_revision bigint, requested_expected_state uuid,
    requested_scope text, requested_zone text, requested_patch jsonb
) RETURNS TABLE(
    revision bigint, source_native_ref uuid, selected_occurrence_ref uuid,
    target_occurrence_refs uuid[], accepted_at timestamptz, replayed boolean
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $$
#variable_conflict error
DECLARE anchor_row record;
        existing dante.occurrence_profile_edit%ROWTYPE;
        source_ref uuid; is_routine boolean; current_revision bigint;
        current_state uuid; anchor timestamptz; accepted timestamptz;
        candidate record; instant timestamptz;
        targets uuid[]; excluded uuid[]:=ARRAY[]::uuid[];
        patch_key text; patch_value jsonb;
BEGIN
    IF requested_operation IS NULL OR requested_operation<>btrim(requested_operation)
       OR requested_operation='' OR char_length(requested_operation)>200
       OR requested_expected_revision IS NULL OR requested_expected_revision<0
       OR requested_scope IS NULL
       OR requested_scope NOT IN ('only_this','this_and_following','from_next')
       OR requested_patch IS NULL OR jsonb_typeof(requested_patch)<>'object'
       OR requested_patch='{}'::jsonb THEN
        RAISE EXCEPTION USING ERRCODE='22023',
            CONSTRAINT='occurrence_edit_invalid',
            MESSAGE='Invalid scoped edit request';
    END IF;
    FOR patch_key,patch_value IN SELECT key,value FROM jsonb_each(requested_patch) LOOP
        IF (patch_key='event_local' AND (
               requested_scope<>'only_this'
               OR jsonb_typeof(patch_value)<>'object'
               OR patch_value='{}'::jsonb
               OR CASE WHEN jsonb_typeof(patch_value)='object' THEN
                   (SELECT array_agg(field.key ORDER BY field.key)
                      FROM jsonb_object_keys(patch_value) AS field(key))
                   IS DISTINCT FROM ARRAY['agenda_parts','expected_participants','life_area_ref']::text[]
                  ELSE TRUE END
           ))
           OR (patch_key<>'event_local' AND (
               patch_key NOT IN ('title','description','location','color_code')
           OR (patch_key='title' AND (
               jsonb_typeof(patch_value)<>'string'
               OR btrim(patch_value #>> '{}')=''
               OR char_length(patch_value #>> '{}')>300
               OR btrim(patch_value #>> '{}')<>(patch_value #>> '{}')))
           OR (patch_key IN ('description','location') AND
               patch_value<>'null'::jsonb AND (
                  jsonb_typeof(patch_value)<>'string'
                  OR btrim(patch_value #>> '{}')=''
                  OR btrim(patch_value #>> '{}')<>(patch_value #>> '{}')))
           OR (patch_key='color_code' AND patch_value<>'null'::jsonb AND
               (jsonb_typeof(patch_value)<>'string'
                OR (patch_value #>> '{}') !~ '^#[0-9A-F]{6}$')))) THEN
            RAISE EXCEPTION USING ERRCODE='22023',
                CONSTRAINT='occurrence_edit_invalid_patch',
                MESSAGE='Unsupported or invalid editable metadata field';
        END IF;
    END LOOP;
    SELECT * INTO anchor_row FROM dante.get_self_occurrence(actor,selected_ref);
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='occurrence_edit_unavailable',
            MESSAGE='Selected occurrence outside self scope';
    END IF;
    source_ref:=anchor_row.source_native_ref;
    SELECT EXISTS (
        SELECT 1 FROM dante.routine_intention r
         WHERE r.routine_ref=source_ref AND r.self_person_ref=actor
    ) INTO is_routine;
    IF is_routine AND requested_patch ? 'event_local' THEN
        RAISE EXCEPTION USING ERRCODE='22023',
            CONSTRAINT='occurrence_edit_invalid_patch',
            MESSAGE='Event local structure cannot be assigned to a Routine';
    END IF;
    IF requested_patch ? 'event_local' THEN
        IF jsonb_typeof(requested_patch #> '{event_local,agenda_parts}')<>'array'
           OR jsonb_typeof(requested_patch #> '{event_local,expected_participants}')<>'array'
           OR jsonb_typeof(requested_patch #> '{event_local,life_area_ref}') NOT IN ('string','null')
           OR jsonb_array_length(requested_patch #> '{event_local,agenda_parts}')>100
           OR jsonb_array_length(requested_patch #> '{event_local,expected_participants}')>100
           OR EXISTS (
               SELECT 1 FROM jsonb_array_elements(requested_patch #> '{event_local,agenda_parts}') AS part(value)
                WHERE jsonb_typeof(part.value)<>'string'
                   OR char_length(part.value #>> '{}') NOT BETWEEN 1 AND 1000
                   OR btrim(part.value #>> '{}')<>(part.value #>> '{}')
           ) OR EXISTS (
               SELECT 1 FROM jsonb_array_elements(requested_patch #> '{event_local,expected_participants}') AS participant(value)
                WHERE jsonb_typeof(participant.value)<>'object'
                   OR participant.value->>'requirement_code' IS NULL
                   OR participant.value->>'requirement_code' NOT IN ('required','optional')
                   OR participant.value->>'person_ref' IS NULL
                   OR (SELECT count(*) FROM jsonb_object_keys(participant.value))<>2
           ) OR (
               SELECT count(*)<>count(DISTINCT participant.value->>'person_ref')
                 FROM jsonb_array_elements(requested_patch #> '{event_local,expected_participants}') AS participant(value)
           ) THEN
            RAISE EXCEPTION USING ERRCODE='22023',
                CONSTRAINT='occurrence_edit_invalid_patch',
                MESSAGE='Invalid local Event structure';
        END IF;
        IF EXISTS (
            SELECT 1
              FROM jsonb_array_elements(requested_patch #> '{event_local,expected_participants}') AS participant(value)
             WHERE participant.value->>'person_ref'<>'self'
               AND NOT EXISTS (
                   SELECT 1 FROM dante.list_self_person_referents(actor) AS person
                    WHERE person.person_ref::text=participant.value->>'person_ref'
               )
        ) OR (
            requested_patch #> '{event_local,life_area_ref}'<>'null'::jsonb
            AND NOT EXISTS (
                SELECT 1 FROM dante.list_self_life_areas(actor) AS area
                 WHERE area.life_area_ref::text=requested_patch #>> '{event_local,life_area_ref}'
            )
        ) THEN
            RAISE EXCEPTION USING ERRCODE='23503',
                CONSTRAINT='occurrence_edit_unavailable',
                MESSAGE='Event local policy references another owner';
        END IF;
    END IF;
    IF is_routine THEN
        PERFORM 1 FROM dante.routine_intention r
         WHERE r.routine_ref=source_ref AND r.self_person_ref=actor FOR UPDATE;
    ELSE
        PERFORM 1 FROM dante.event_expectation e
         WHERE e.event_ref=source_ref AND e.self_person_ref=actor FOR UPDATE;
        IF NOT FOUND THEN
            RAISE EXCEPTION USING ERRCODE='23503',
                CONSTRAINT='occurrence_edit_unavailable',
                MESSAGE='Source outside self scope';
        END IF;
    END IF;
    SELECT * INTO existing FROM dante.occurrence_profile_edit e
     WHERE e.self_person_ref=actor AND e.operation_id=requested_operation;
    IF FOUND THEN
        IF existing.selected_occurrence_ref<>selected_ref
           OR existing.expected_revision<>requested_expected_revision
           OR existing.expected_recurrence_state_ref IS DISTINCT FROM requested_expected_state
           OR existing.scope_code<>requested_scope
           OR existing.effective_zone_id IS DISTINCT FROM requested_zone
           OR existing.profile_patch IS DISTINCT FROM requested_patch THEN
            RAISE EXCEPTION USING ERRCODE='23505',
                CONSTRAINT='pk_occurrence_profile_edit',
                MESSAGE='Operation reused for different scoped edit';
        END IF;
        revision:=existing.revision;
        source_native_ref:=existing.source_native_ref;
        selected_occurrence_ref:=existing.selected_occurrence_ref;
        target_occurrence_refs:=existing.target_occurrence_refs;
        accepted_at:=existing.accepted_at;
        replayed:=true;
        RETURN NEXT; RETURN;
    END IF;
    SELECT COALESCE(MAX(e.revision),0) INTO current_revision
      FROM dante.occurrence_profile_edit e
     WHERE e.source_native_ref=source_ref;
    IF current_revision<>requested_expected_revision THEN
        RAISE EXCEPTION USING ERRCODE='23505',
            CONSTRAINT='occurrence_edit_stale',
            MESSAGE='Source edit revision changed';
    END IF;
    -- Block concurrent Recurrence state replacement until acceptance commits.
    IF is_routine THEN
        PERFORM 1 FROM dante.routine_recurrence_current_history h
         WHERE h.routine_ref=source_ref AND h.current_until_at IS NULL
         FOR SHARE;
        SELECT material_state_ref INTO current_state
          FROM dante.get_self_routine_recurrence(actor,source_ref);
    ELSE
        PERFORM 1 FROM dante.event_recurrence_current_history h
         WHERE h.event_ref=source_ref AND h.current_until_at IS NULL
         FOR SHARE;
        SELECT material_state_ref INTO current_state
          FROM dante.get_self_event_recurrence(actor,source_ref);
    END IF;
    IF current_state IS DISTINCT FROM requested_expected_state THEN
        RAISE EXCEPTION USING ERRCODE='23505',
            CONSTRAINT='occurrence_edit_recurrence_stale',
            MESSAGE='Recurrence changed since preview';
    END IF;
    accepted:=clock_timestamp();
    targets:=CASE WHEN requested_scope='from_next' THEN ARRAY[]::uuid[]
                  ELSE ARRAY[selected_ref] END;
    IF requested_scope IN ('this_and_following','from_next') THEN
        IF anchor_row.origin_code<>'recurrence_generated' THEN
            RAISE EXCEPTION USING ERRCODE='22023',
                CONSTRAINT='occurrence_edit_not_generated',
                MESSAGE='Following scope requires a generated selected instance';
        END IF;
        anchor:=dante.occurrence_edit_coordinate_instant(actor,selected_ref,requested_zone);
        IF requested_scope='this_and_following'
           AND dante.get_self_occurrence_edit_protection(actor,selected_ref)='registration' THEN
            RAISE EXCEPTION USING ERRCODE='23505',
                CONSTRAINT='occurrence_edit_selected_facts',
                MESSAGE='Recorded selected instance requires from-next scope';
        END IF;
    ELSE
        anchor:=NULL;
    END IF;

    -- This is the same fully materialized, bounded inventory as M1-B.
    -- Its SELECT and all validations happen within this one source lock.
    FOR candidate IN
        SELECT * FROM dante.list_self_recurrence_edit_occurrences(actor,selected_ref)
    LOOP
        IF requested_scope='only_this'
           OR candidate.occurrence_ref=selected_ref
           OR candidate.origin_code<>'recurrence_generated' THEN
            CONTINUE;
        END IF;
        instant:=dante.occurrence_edit_coordinate_instant(
            actor,candidate.occurrence_ref,requested_zone
        );
        IF instant<=GREATEST(anchor,accepted) THEN CONTINUE; END IF;
        IF dante.get_self_occurrence_edit_protection(
            actor,candidate.occurrence_ref
        ) IS NOT NULL THEN
            excluded:=array_append(excluded,candidate.occurrence_ref);
            CONTINUE;
        END IF;
        targets:=array_append(targets,candidate.occurrence_ref);
    END LOOP;
    INSERT INTO dante.occurrence_profile_edit(
        self_person_ref,operation_id,source_native_ref,selected_occurrence_ref,
        revision,expected_revision,expected_recurrence_state_ref,scope_code,
        effective_zone_id,anchor_at,accepted_at,profile_patch,
        target_occurrence_refs,excluded_occurrence_refs
    ) VALUES (
        actor,requested_operation,source_ref,selected_ref,
        current_revision+1,current_revision,current_state,requested_scope,
        requested_zone,anchor,accepted,requested_patch,targets,excluded
    );
    revision:=current_revision+1;
    source_native_ref:=source_ref;
    selected_occurrence_ref:=selected_ref;
    target_occurrence_refs:=targets;
    accepted_at:=accepted;
    replayed:=false;
    RETURN NEXT;
END;
$$;
"""

_RETIRE = r"""CREATE OR REPLACE FUNCTION dante.retire_self_temporal_objective(
    actor uuid, requested_objective uuid, requested_operation text,
    requested_fingerprint text, requested_revision bigint
) RETURNS TABLE(objective_ref uuid, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE owned record; current_definition record; bound_source uuid;
BEGIN
    IF requested_operation IS NULL OR requested_operation<>btrim(requested_operation)
       OR char_length(requested_operation) NOT BETWEEN 1 AND 200
       OR requested_fingerprint IS NULL
       OR requested_fingerprint !~ '^[0-9a-f]{64}$'
       OR requested_revision IS NULL OR requested_revision < 0 THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='temporal_objective_retirement_invalid',
          MESSAGE='Invalid retirement command';
    END IF;
    -- Serialize Activity local exceptions with source-wide reconciliation.
    SELECT generation.source_native_ref INTO bound_source
      FROM dante.temporal_objective AS item
      JOIN dante.temporal_objective_create_operation AS origin
        ON origin.objective_ref=item.objective_ref
       AND origin.self_person_ref=item.self_person_ref
      JOIN dante.routine_occurrence_activity_instance AS binding
        ON binding.activity_ref=item.subject_native_ref
       AND binding.self_person_ref=item.self_person_ref
      JOIN dante.occurrence_generation AS generation
        ON generation.occurrence_ref=binding.occurrence_ref
     WHERE item.objective_ref=requested_objective
       AND item.self_person_ref=actor
       AND left(origin.operation_id,char_length('b14:objective:'))='b14:objective:';
    IF bound_source IS NULL THEN
        SELECT generation.source_native_ref INTO bound_source
          FROM dante.temporal_objective AS item
          JOIN dante.occurrence_generation AS generation
            ON generation.occurrence_ref=item.subject_native_ref
         WHERE item.objective_ref=requested_objective
           AND item.self_person_ref=actor
           AND item.subject_kind='occurrence';
    END IF;
    IF bound_source IS NOT NULL THEN
        PERFORM pg_advisory_xact_lock(hashtextextended(
            'dante:recurrence-materialization:'||bound_source::text,0));
    END IF;
    SELECT * INTO owned FROM dante.temporal_objective AS item
     WHERE item.objective_ref=requested_objective AND item.self_person_ref=actor
       AND item.subject_kind IN ('activity','event','occurrence')
       AND dante._actual_subject_owned_as(actor,item.subject_kind,item.subject_native_ref)
     FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
          CONSTRAINT='temporal_objective_unavailable',
          MESSAGE='Objective unavailable';
    END IF;
    IF owned.subject_kind='event' AND EXISTS (
        SELECT 1 FROM dante.event_recurrence_state AS recurrence
         WHERE recurrence.event_ref=owned.subject_native_ref
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='temporal_objective_retirement_source_unsupported',
          MESSAGE='Recurring Event source requires a scoped edit';
    END IF;
    IF owned.retired_at IS NOT NULL THEN
        IF owned.retirement_operation_id=requested_operation
           AND owned.retirement_fingerprint=requested_fingerprint THEN
            RETURN QUERY SELECT requested_objective,true;
            RETURN;
        END IF;
        RAISE EXCEPTION USING ERRCODE='23505',
          CONSTRAINT='temporal_objective_retirement_stale',
          MESSAGE='Objective was already retired';
    END IF;
    SELECT * INTO current_definition
      FROM dante.get_self_temporal_objective_definition(actor,requested_objective);
    IF NOT FOUND OR current_definition.definition_revision<>requested_revision THEN
        RAISE EXCEPTION USING ERRCODE='40001',
          CONSTRAINT='temporal_objective_retirement_stale',
          MESSAGE='Objective definition changed';
    END IF;
    IF EXISTS(
        SELECT 1 FROM dante.temporal_objective_observation AS observation
         WHERE observation.objective_ref=requested_objective
    ) OR EXISTS(
        SELECT 1 FROM dante.temporal_objective_evaluation_state AS evaluation
         WHERE evaluation.objective_ref=requested_objective
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23505',
          CONSTRAINT='temporal_objective_retirement_recorded',
          MESSAGE='An Objective with recorded results cannot be retired';
    END IF;
    IF owned.subject_kind='activity' AND EXISTS (
        SELECT 1 FROM dante.temporal_objective_create_operation AS origin
         WHERE origin.objective_ref=requested_objective
           AND origin.self_person_ref=actor
           AND left(origin.operation_id,char_length('b14:objective:'))='b14:objective:'
    ) AND NOT EXISTS (
        SELECT 1 FROM dante.routine_occurrence_activity_instance AS binding
         WHERE binding.self_person_ref=actor
           AND binding.activity_ref=owned.subject_native_ref
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='temporal_objective_retirement_source_unsupported',
          MESSAGE='Unbound recurring Objective cannot be locally retired';
    END IF;
    UPDATE dante.temporal_objective AS item
       SET retired_at=clock_timestamp(),
           retirement_operation_id=requested_operation,
           retirement_fingerprint=requested_fingerprint
     WHERE item.objective_ref=requested_objective AND item.self_person_ref=actor;
    RETURN QUERY SELECT requested_objective,false;
END;
$function$;"""
