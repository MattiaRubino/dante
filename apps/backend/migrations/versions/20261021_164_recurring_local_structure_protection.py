"""Protect post-materialization Activity structure from series propagation.

The binding is the completion marker: setup writes finish before it; subsequent
role, Objective, capture, Reality or Reminder changes are individual edits.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261021_164"
down_revision: str | None = "20261021_163"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.get_bind().execute(sa.text(_PROTECTION))


def downgrade() -> None:
    raise RuntimeError("20261021_164 is forward-only")


_PROTECTION = r"""
CREATE OR REPLACE FUNCTION dante.get_self_occurrence_edit_protection(
    actor uuid, requested_occurrence uuid
) RETURNS text
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $$
#variable_conflict error
DECLARE owned record; linked_activity uuid; binding_created_at timestamptz;
BEGIN
    SELECT * INTO owned FROM dante.get_self_occurrence(actor,requested_occurrence);
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='occurrence_edit_unavailable',
            MESSAGE='Occurrence outside self scope';
    END IF;
    SELECT link.activity_ref,link.created_at INTO linked_activity,binding_created_at
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
        SELECT 1 FROM dante.activity_schedule_role role
          JOIN dante.schedule_establish_operation established
            ON established.schedule_ref=role.schedule_ref
         WHERE role.activity_ref=linked_activity
           AND established.created_at>binding_created_at
    ) OR EXISTS (
        SELECT 1 FROM dante.activity_schedule_role role
         WHERE role.activity_ref=linked_activity
           AND role.retired_at>binding_created_at
    ) OR EXISTS (
        SELECT 1 FROM dante.activity_execution_policy_current_history history
         WHERE history.activity_ref=linked_activity
           AND history.current_from_at>binding_created_at
    ) OR EXISTS (
        SELECT 1 FROM dante.activity_outcome_review_policy_current_history history
         WHERE history.activity_ref=linked_activity
           AND history.current_from_at>binding_created_at
    ) OR EXISTS (
        SELECT 1 FROM dante.activity_decomposition relation
         WHERE relation.parent_activity_ref=linked_activity
           AND relation.created_at>binding_created_at
    ) OR EXISTS (
        SELECT 1 FROM dante.temporal_objective objective
         WHERE objective.subject_native_ref=linked_activity
           AND (objective.created_at>binding_created_at
                OR objective.retired_at>binding_created_at)
    ) OR EXISTS (
        SELECT 1 FROM dante.schedule_reminder_operation reminder
          JOIN dante.activity_schedule_role role
            ON role.schedule_ref=reminder.schedule_ref
         WHERE role.activity_ref=linked_activity
           AND reminder.created_at>binding_created_at
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
         WHERE obj.subject_native_ref IN (linked_activity,requested_occurrence)
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
