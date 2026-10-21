"""Preserve recurring planned Session names and first local Life Area assignments.

Historical planned names lacked an edit receipt. Existing recurring rows are
conservatively classified as legacy-unknown; new local renames are marked as
local edits. Neither can be silently overwritten by a later series revision.
Distinguish an Activity's create-time Life Area assignment from a later first
assignment, which otherwise has the same zero expected revision.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261021_163"
down_revision: str | None = "20261019_162"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "activity_schedule_role",
        sa.Column("name_exception_reason", sa.Text(), nullable=True),
        schema="dante",
    )
    db = op.get_bind()
    db.exec_driver_sql(
        "ALTER TABLE dante.activity_schedule_role "
        "ADD CONSTRAINT ck_activity_schedule_role_name_exception "
        "CHECK (name_exception_reason IS NULL OR "
        "(role_code='planned' AND name_exception_reason IN ('local_edit','legacy_unknown')))"
    )
    db.exec_driver_sql(
        "UPDATE dante.activity_schedule_role AS role "
        "SET name_exception_reason='legacy_unknown' "
        "FROM dante.routine_occurrence_activity_instance AS link "
        "WHERE role.activity_ref=link.activity_ref AND role.role_code='planned' "
        "AND role.name_exception_reason IS NULL"
    )
    db.execute(sa.text(_REVISE_PLANNED_NAME))
    db.execute(sa.text(_PROTECTION))


def downgrade() -> None:
    raise RuntimeError("20261021_163 is forward-only")


_REVISE_PLANNED_NAME = r"""
CREATE OR REPLACE FUNCTION dante.revise_self_planned_session_name(
 actor uuid, requested_activity uuid, requested_schedule uuid,
 expected_name text, new_name text
) RETURNS TABLE(schedule_ref uuid,display_name text,replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE existing record; recurring_source uuid;
BEGIN
 IF new_name IS NOT NULL AND
    (new_name<>btrim(new_name) OR new_name='' OR char_length(new_name)>300) THEN
   RAISE EXCEPTION USING ERRCODE='23514',
     CONSTRAINT='activity_planned_name_invalid',MESSAGE='Invalid planned Session label';
 END IF;
 -- Serialize a local override against the series preview/accept source lock.
 SELECT occurrence.source_native_ref INTO recurring_source
   FROM dante.routine_occurrence_activity_instance AS link
   JOIN dante.occurrence_generation AS occurrence
     ON occurrence.occurrence_ref=link.occurrence_ref
  WHERE link.activity_ref=requested_activity AND link.self_person_ref=actor;
 IF recurring_source IS NOT NULL THEN
   PERFORM 1 FROM dante.routine_intention source
    WHERE source.routine_ref=recurring_source AND source.self_person_ref=actor
    FOR UPDATE;
 END IF;
 PERFORM 1 FROM dante.activity_intention a
  WHERE a.activity_ref=requested_activity AND a.self_person_ref=actor
    AND a.retired_at IS NULL FOR UPDATE;
 IF NOT FOUND THEN
   RAISE EXCEPTION USING ERRCODE='23503',
    CONSTRAINT='activity_planned_name_unavailable',MESSAGE='Activity not found';
 END IF;
 SELECT * INTO existing FROM dante.activity_schedule_role r
  WHERE r.activity_ref=requested_activity AND r.schedule_ref=requested_schedule
   AND r.role_code='planned' AND r.retired_at IS NULL FOR UPDATE;
 IF NOT FOUND THEN
   RAISE EXCEPTION USING ERRCODE='23503',
    CONSTRAINT='activity_planned_name_unavailable',MESSAGE='Planned row not found';
 END IF;
 IF existing.display_name IS NOT DISTINCT FROM new_name THEN
   RETURN QUERY SELECT requested_schedule,new_name,true;
   RETURN;
 END IF;
 IF existing.display_name IS DISTINCT FROM expected_name THEN
   RAISE EXCEPTION USING ERRCODE='23505',
    CONSTRAINT='activity_planned_name_stale',MESSAGE='Planned Session label changed';
 END IF;
 UPDATE dante.activity_schedule_role AS r
    SET display_name=new_name,
        name_exception_reason=COALESCE(r.name_exception_reason,'local_edit')
  WHERE r.schedule_ref=requested_schedule AND r.activity_ref=requested_activity;
 RETURN QUERY SELECT requested_schedule,new_name,false;
END
$function$;
"""


_PROTECTION = r"""
CREATE OR REPLACE FUNCTION dante.get_self_occurrence_edit_protection(
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
           AND (edit.expected_revision>0 OR NOT EXISTS (
               SELECT 1 FROM dante.activity_create_operation creation
                WHERE creation.activity_ref=linked_activity
                  AND creation.self_person_ref=actor
                  AND creation.operation_id=edit.operation_id
           ))
    ) OR EXISTS (
        SELECT 1 FROM dante.temporal_objective obj
          JOIN dante.temporal_objective_definition_revision edit
            ON edit.objective_ref=obj.objective_ref
         WHERE obj.subject_native_ref=linked_activity
    ) OR EXISTS (
        SELECT 1 FROM dante.activity_schedule_role role
         WHERE role.activity_ref=linked_activity
           AND role.role_code='planned'
           AND role.name_exception_reason='local_edit'
    ) OR EXISTS (
        SELECT 1 FROM dante.activity_decomposition relation
          JOIN dante.activity_intention child
            ON child.activity_ref=relation.child_activity_ref
         WHERE relation.parent_activity_ref=linked_activity
           AND child.profile_revision>0
    ) THEN
        RETURN 'local_change';
    END IF;
    IF EXISTS (
        SELECT 1 FROM dante.activity_schedule_role role
         WHERE role.activity_ref=linked_activity
           AND role.role_code='planned'
           AND role.name_exception_reason='legacy_unknown'
    ) THEN
        RETURN 'legacy_unknown';
    END IF;
    RETURN NULL;
END;
$$;
"""
