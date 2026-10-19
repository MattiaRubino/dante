"""Preserve protected future Occurrences during scoped profile propagation.

A following metadata correction records exceptions at acceptance. The
immutable exclusion snapshot prevents its policy read from subsequently
leaking metadata into already modified or recorded future instances.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261019_161"
down_revision: str | None = "20261019_160"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "occurrence_profile_edit",
        sa.Column(
            "excluded_occurrence_refs",
            sa.ARRAY(sa.Uuid()),
            nullable=False,
            server_default=sa.text("'{}'::uuid[]"),
        ),
        schema="dante",
    )
    op.drop_constraint(
        "ck_occurrence_profile_edit_scope", "occurrence_profile_edit", schema="dante"
    )
    op.create_check_constraint(
        "ck_occurrence_profile_edit_scope",
        "occurrence_profile_edit",
        "scope_code IN ('only_this','this_and_following','from_next')",
        schema="dante",
    )
    db = op.get_bind()
    db.execute(sa.text(_PROTECTION))
    db.exec_driver_sql(
        "ALTER FUNCTION dante.get_self_occurrence_edit_protection(uuid,uuid) OWNER TO dante_owner"
    )
    db.exec_driver_sql(
        "REVOKE ALL ON FUNCTION dante.get_self_occurrence_edit_protection(uuid,uuid) "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )
    db.exec_driver_sql(
        "GRANT EXECUTE ON FUNCTION dante.get_self_occurrence_edit_protection(uuid,uuid) "
        "TO dante_runtime"
    )
    db.execute(sa.text(_PROFILE_PATCH))
    db.execute(sa.text(_ACCEPT_EDIT))
    db.execute(sa.text(_PREVIEW))
    db.execute(sa.text(_PREVIEWED_ACCEPT))
    for signature in (
        "get_self_occurrence_profile_edit_preview(uuid,uuid,text,text)",
        "accept_self_occurrence_profile_edit_previewed(uuid,uuid,text,bigint,uuid,text,text,jsonb,text)",
    ):
        db.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
        db.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION dante.{signature} FROM PUBLIC,dante_runtime,dante_migrator"
        )
        db.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("20261019_161 is forward-only")


_PROTECTION = r"""
CREATE FUNCTION dante.get_self_occurrence_edit_protection(
    actor uuid, requested_occurrence uuid
) RETURNS text
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $$
#variable_conflict error
DECLARE owned record; linked_activity uuid;
BEGIN
    SELECT * INTO owned FROM dante.get_self_occurrence(actor,requested_occurrence);
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='occurrence_edit_unavailable',
            MESSAGE='Occurrence outside self scope';
    END IF;
    SELECT link.activity_ref INTO linked_activity
      FROM dante.routine_occurrence_activity_instance link
     WHERE link.self_person_ref=actor AND link.occurrence_ref=requested_occurrence;
    IF EXISTS (
        SELECT 1 FROM dante.actual a
         WHERE a.subject_native_ref IN (requested_occurrence,linked_activity)
    ) OR EXISTS (
        SELECT 1 FROM dante.session_execution_subject s
         WHERE s.subject_native_ref IN (requested_occurrence,linked_activity)
    ) OR EXISTS (
        SELECT 1 FROM dante.temporal_objective obj
          JOIN dante.temporal_objective_observation obs
            ON obs.objective_ref=obj.objective_ref
         WHERE obj.subject_native_ref IN (requested_occurrence,linked_activity)
    ) OR EXISTS (
        SELECT 1 FROM dante.activity_decomposition relation
          JOIN dante.session_execution_subject s
            ON s.subject_native_ref=relation.child_activity_ref
         WHERE relation.parent_activity_ref=linked_activity
    ) OR EXISTS (
        SELECT 1 FROM dante.activity_decomposition relation
          JOIN dante.actual a ON a.subject_native_ref=relation.child_activity_ref
         WHERE relation.parent_activity_ref=linked_activity
    ) OR EXISTS (
        SELECT 1 FROM dante.activity_decomposition relation
          JOIN dante.temporal_objective obj
            ON obj.subject_native_ref=relation.child_activity_ref
          JOIN dante.temporal_objective_observation obs
            ON obs.objective_ref=obj.objective_ref
         WHERE relation.parent_activity_ref=linked_activity
    ) THEN
        RETURN 'registration';
    END IF;
    IF owned.skipped THEN RETURN 'skipped'; END IF;
    IF EXISTS (
        SELECT 1 FROM dante.occurrence_profile_edit edit
         WHERE edit.source_native_ref=owned.source_native_ref
           AND edit.selected_occurrence_ref=requested_occurrence
           AND edit.scope_code='only_this'
    ) OR EXISTS (
        SELECT 1 FROM dante.activity_intention activity
         WHERE activity.activity_ref=linked_activity
           AND activity.profile_revision>0
    ) OR EXISTS (
        SELECT 1 FROM dante.schedule schedule
          JOIN dante.schedule_revision_operation revision
            ON revision.schedule_ref=schedule.schedule_ref
         WHERE schedule.subject_native_ref IN (requested_occurrence,linked_activity)
    ) OR EXISTS (
        SELECT 1 FROM dante.activity_life_area_assignment_operation edit
         WHERE edit.activity_ref=linked_activity
           AND edit.expected_revision>0
    ) OR EXISTS (
        SELECT 1 FROM dante.temporal_objective obj
          JOIN dante.temporal_objective_definition_revision edit
            ON edit.objective_ref=obj.objective_ref
         WHERE obj.subject_native_ref=linked_activity
    ) OR EXISTS (
        SELECT 1 FROM dante.activity_decomposition relation
          JOIN dante.activity_intention child
            ON child.activity_ref=relation.child_activity_ref
         WHERE relation.parent_activity_ref=linked_activity
           AND child.profile_revision>0
    ) THEN
        RETURN 'local_change';
    END IF;
    RETURN NULL;
END;
$$;
"""


_PROFILE_PATCH = r"""
CREATE OR REPLACE FUNCTION dante.get_self_occurrence_profile_patch(
    actor uuid, requested_occurrence uuid
) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $$
#variable_conflict error
DECLARE bound_source uuid; combined jsonb;
BEGIN
    SELECT o.source_native_ref INTO bound_source
      FROM dante.get_self_occurrence(actor,requested_occurrence) o;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='occurrence_edit_unavailable',
            MESSAGE='Occurrence outside self scope';
    END IF;
    SELECT jsonb_object_agg(field.key,field.value ORDER BY edits.revision)
      INTO combined
      FROM dante.occurrence_profile_edit edits
      CROSS JOIN LATERAL jsonb_each(edits.profile_patch) field
     WHERE edits.self_person_ref=actor
       AND edits.source_native_ref=bound_source
       AND CASE
           WHEN edits.selected_occurrence_ref=requested_occurrence
                AND edits.scope_code<>'from_next' THEN TRUE
           WHEN edits.scope_code IN ('this_and_following','from_next')
                AND NOT requested_occurrence=ANY(edits.excluded_occurrence_refs) THEN
               dante.occurrence_edit_coordinate_instant(
                   actor,requested_occurrence,edits.effective_zone_id
               ) > GREATEST(edits.anchor_at,edits.accepted_at)
           ELSE FALSE
       END;
    RETURN COALESCE(combined,'{}'::jsonb);
END;
$$;
"""

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
        IF patch_key NOT IN ('title','description','location','color_code')
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
                OR (patch_value #>> '{}') !~ '^#[0-9A-F]{6}$')) THEN
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

_PREVIEW = r"""
CREATE FUNCTION dante.get_self_occurrence_profile_edit_preview(
    actor uuid, selected_ref uuid, requested_scope text, requested_zone text
) RETURNS TABLE(
    source_native_ref uuid, edit_revision bigint, recurrence_state_ref uuid,
    selected_protection text, target_occurrence_refs uuid[],
    protected_occurrences jsonb, fingerprint text
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $$
#variable_conflict error
DECLARE selected record; candidate record; anchor timestamptz;
        accepted timestamptz; instant timestamptz; protection text;
        targets uuid[]; protected jsonb:='[]'::jsonb;
        source_snapshot jsonb; policy_snapshot jsonb;
BEGIN
    IF requested_scope NOT IN ('only_this','this_and_following','from_next')
       OR requested_scope IS NULL THEN
        RAISE EXCEPTION USING ERRCODE='22023',
            CONSTRAINT='occurrence_edit_invalid',MESSAGE='Invalid edit scope';
    END IF;
    SELECT * INTO selected FROM dante.get_self_occurrence(actor,selected_ref);
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='occurrence_edit_unavailable',MESSAGE='Occurrence outside self scope';
    END IF;
    source_native_ref:=selected.source_native_ref;
    SELECT to_jsonb(r) INTO source_snapshot FROM dante.routine_intention r
     WHERE r.routine_ref=source_native_ref AND r.self_person_ref=actor;
    IF FOUND THEN
        SELECT to_jsonb(p) INTO policy_snapshot FROM dante.routine_occurrence_policy p
         WHERE p.routine_ref=source_native_ref AND p.self_person_ref=actor;
    ELSE
        SELECT to_jsonb(e) INTO source_snapshot FROM dante.event_expectation e
         WHERE e.event_ref=source_native_ref AND e.self_person_ref=actor;
        SELECT to_jsonb(p) INTO policy_snapshot FROM dante.event_occurrence_policy p
         WHERE p.event_ref=source_native_ref AND p.self_person_ref=actor;
    END IF;
    SELECT state.edit_revision,state.recurrence_state_ref
      INTO edit_revision,recurrence_state_ref
      FROM dante.get_self_occurrence_edit_revision(actor,selected_ref) state;
    selected_protection:=dante.get_self_occurrence_edit_protection(actor,selected_ref);
    accepted:=clock_timestamp();
    targets:=CASE WHEN requested_scope='from_next' THEN ARRAY[]::uuid[]
                  ELSE ARRAY[selected_ref] END;
    IF requested_scope<>'only_this' THEN
        IF selected.origin_code<>'recurrence_generated' THEN
            RAISE EXCEPTION USING ERRCODE='22023',
                CONSTRAINT='occurrence_edit_not_generated',
                MESSAGE='Following scope requires generated selected instance';
        END IF;
        anchor:=dante.occurrence_edit_coordinate_instant(actor,selected_ref,requested_zone);
        FOR candidate IN
            SELECT * FROM dante.list_self_recurrence_edit_occurrences(actor,selected_ref)
        LOOP
            IF candidate.occurrence_ref=selected_ref
               OR candidate.origin_code<>'recurrence_generated' THEN CONTINUE; END IF;
            instant:=dante.occurrence_edit_coordinate_instant(
                actor,candidate.occurrence_ref,requested_zone
            );
            IF instant<=GREATEST(anchor,accepted) THEN CONTINUE; END IF;
            protection:=dante.get_self_occurrence_edit_protection(
                actor,candidate.occurrence_ref
            );
            IF protection IS NOT NULL THEN
                protected:=protected || jsonb_build_array(jsonb_build_object(
                    'occurrence_ref',candidate.occurrence_ref,
                    'reason',protection,'expected_at',instant
                ));
            ELSE
                targets:=array_append(targets,candidate.occurrence_ref);
            END IF;
        END LOOP;
    END IF;
    target_occurrence_refs:=targets;
    protected_occurrences:=protected;
    fingerprint:=md5(jsonb_build_object(
        'source',source_native_ref,'revision',edit_revision,
        'source_snapshot',source_snapshot,'policy_snapshot',policy_snapshot,
        'recurrence',recurrence_state_ref,'selected',selected_ref,
        'scope',requested_scope,'targets',targets,'protected',protected
    )::text);
    RETURN NEXT;
END;
$$;
"""

_PREVIEWED_ACCEPT = r"""
CREATE FUNCTION dante.accept_self_occurrence_profile_edit_previewed(
    actor uuid, selected_ref uuid, requested_operation text,
    requested_expected_revision bigint, requested_expected_state uuid,
    requested_scope text, requested_zone text, requested_patch jsonb,
    expected_fingerprint text
) RETURNS TABLE(
    revision bigint, source_native_ref uuid, selected_occurrence_ref uuid,
    target_occurrence_refs uuid[], accepted_at timestamptz, replayed boolean,
    excluded_occurrence_refs uuid[]
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $$
#variable_conflict error
DECLARE source_ref uuid; is_routine boolean; plan record; accepted record;
        existing dante.occurrence_profile_edit%ROWTYPE;
        saved_exclusions uuid[]; preview_exclusions uuid[];
BEGIN
    SELECT o.source_native_ref INTO source_ref
      FROM dante.get_self_occurrence(actor,selected_ref) o;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='occurrence_edit_unavailable',MESSAGE='Occurrence outside self scope';
    END IF;
    SELECT EXISTS (
        SELECT 1 FROM dante.routine_intention r
         WHERE r.routine_ref=source_ref AND r.self_person_ref=actor
    ) INTO is_routine;
    IF is_routine THEN
        PERFORM 1 FROM dante.routine_intention r
         WHERE r.routine_ref=source_ref AND r.self_person_ref=actor FOR UPDATE;
    ELSE
        PERFORM 1 FROM dante.event_expectation e
         WHERE e.event_ref=source_ref AND e.self_person_ref=actor FOR UPDATE;
        IF NOT FOUND THEN
            RAISE EXCEPTION USING ERRCODE='23503',
                CONSTRAINT='occurrence_edit_unavailable',MESSAGE='Source outside self scope';
        END IF;
    END IF;
    SELECT * INTO existing FROM dante.occurrence_profile_edit edit
     WHERE edit.self_person_ref=actor AND edit.operation_id=requested_operation;
    IF FOUND THEN
        SELECT * INTO accepted FROM dante.accept_self_occurrence_profile_edit(
            actor,selected_ref,requested_operation,requested_expected_revision,
            requested_expected_state,requested_scope,requested_zone,requested_patch
        );
        revision:=accepted.revision;
        source_native_ref:=accepted.source_native_ref;
        selected_occurrence_ref:=accepted.selected_occurrence_ref;
        target_occurrence_refs:=accepted.target_occurrence_refs;
        accepted_at:=accepted.accepted_at;
        replayed:=accepted.replayed;
        excluded_occurrence_refs:=existing.excluded_occurrence_refs;
        RETURN NEXT; RETURN;
    END IF;
    SELECT * INTO plan FROM dante.get_self_occurrence_profile_edit_preview(
        actor,selected_ref,requested_scope,requested_zone
    );
    IF expected_fingerprint IS NULL OR plan.fingerprint<>expected_fingerprint
       OR plan.edit_revision<>requested_expected_revision
       OR plan.recurrence_state_ref IS DISTINCT FROM requested_expected_state THEN
        RAISE EXCEPTION USING ERRCODE='23505',
            CONSTRAINT='occurrence_edit_preview_stale',
            MESSAGE='Preview changed before acceptance';
    END IF;
    IF requested_scope='this_and_following' AND plan.selected_protection='registration' THEN
        RAISE EXCEPTION USING ERRCODE='23505',
            CONSTRAINT='occurrence_edit_selected_facts',
            MESSAGE='Recorded selected instance requires from-next scope';
    END IF;
    SELECT * INTO accepted FROM dante.accept_self_occurrence_profile_edit(
        actor,selected_ref,requested_operation,requested_expected_revision,
        requested_expected_state,requested_scope,requested_zone,requested_patch
    );
    SELECT edit.excluded_occurrence_refs INTO saved_exclusions
      FROM dante.occurrence_profile_edit edit
     WHERE edit.self_person_ref=actor AND edit.operation_id=requested_operation;
    SELECT COALESCE(array_agg((entry->>'occurrence_ref')::uuid ORDER BY ordinal),
                    ARRAY[]::uuid[])
      INTO preview_exclusions
      FROM jsonb_array_elements(plan.protected_occurrences) WITH ORDINALITY AS item(entry,ordinal);
    IF accepted.target_occurrence_refs<>plan.target_occurrence_refs
       OR saved_exclusions<>preview_exclusions THEN
        RAISE EXCEPTION USING ERRCODE='23505',
            CONSTRAINT='occurrence_edit_preview_stale',
            MESSAGE='Affected instances changed during acceptance';
    END IF;
    revision:=accepted.revision;
    source_native_ref:=accepted.source_native_ref;
    selected_occurrence_ref:=accepted.selected_occurrence_ref;
    target_occurrence_refs:=accepted.target_occurrence_refs;
    accepted_at:=accepted.accepted_at;
    replayed:=accepted.replayed;
    excluded_occurrence_refs:=saved_exclusions;
    RETURN NEXT;
END;
$$;
"""
