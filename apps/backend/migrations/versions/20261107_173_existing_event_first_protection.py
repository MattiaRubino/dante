"""Protect factual and local edits on a seeded first Event Occurrence.

Revision ID: 20261107_173
Revises: 20261107_172

This only extends the existing self-scoped protection function. No existing
Occurrence, historical Event, seed, exclusion or materialized state is updated.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261107_173"
down_revision: str | None = "20261107_172"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.get_bind().exec_driver_sql(_PROTECTION)


def downgrade() -> None:
    raise RuntimeError("20261107_173 is forward-only")


_PROTECTION = r"""
CREATE OR REPLACE FUNCTION dante.get_self_occurrence_edit_protection(
    actor uuid, requested_occurrence uuid
) RETURNS text
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $$
#variable_conflict error
DECLARE owned record; linked_activity uuid; binding_created_at timestamptz;
        first_event uuid; first_seed_at timestamptz;
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
    -- The first Event is a physical, pre-existing Event, not a duplicate
    -- schedule materialized below this Occurrence. Examine its factual and
    -- local edit history before allowing any source-level reconciliation.
    SELECT linked.first_event_ref INTO first_event
      FROM dante.get_self_event_recurring_first_by_occurrence(
          actor,requested_occurrence
      ) AS linked;
    IF first_event IS NOT NULL THEN
        SELECT seed.accepted_at INTO first_seed_at
          FROM dante.event_recurring_seed AS seed
         WHERE seed.self_person_ref=actor
           AND seed.event_ref=first_event
           AND seed.first_occurrence_ref=requested_occurrence;
        IF first_seed_at IS NULL THEN
            RETURN 'legacy_unknown';
        END IF;
        IF EXISTS (
            SELECT 1 FROM dante.actual a
             WHERE a.subject_native_ref IN (requested_occurrence,first_event)
        ) OR EXISTS (
            SELECT 1 FROM dante.session_execution_subject s
             WHERE s.subject_native_ref IN (requested_occurrence,first_event)
        ) OR EXISTS (
            SELECT 1 FROM dante.temporal_objective obj
              JOIN dante.temporal_objective_observation obs
                ON obs.objective_ref=obj.objective_ref
             WHERE obj.subject_native_ref IN (requested_occurrence,first_event)
        ) THEN
            RETURN 'registration';
        END IF;
        IF EXISTS (
            SELECT 1 FROM dante.event_profile_revision revision
             WHERE revision.event_ref=first_event
               AND revision.revised_at>first_seed_at
        ) OR EXISTS (
            SELECT 1 FROM dante.event_agenda_mutation_operation agenda
             WHERE agenda.event_ref=first_event
               AND agenda.created_at>first_seed_at
        ) OR EXISTS (
            SELECT 1 FROM dante.event_expected_participation_operation participation
             WHERE participation.event_ref=first_event
               AND participation.accepted_at>first_seed_at
        ) OR EXISTS (
            SELECT 1 FROM dante.event_life_area_assignment_operation area
             WHERE area.event_ref=first_event
               AND area.accepted_at>first_seed_at
        ) OR EXISTS (
            SELECT 1 FROM dante.schedule schedule
              JOIN dante.schedule_revision_operation revision
                ON revision.schedule_ref=schedule.schedule_ref
             WHERE schedule.subject_native_ref=first_event
               AND revision.created_at>first_seed_at
        ) OR EXISTS (
            SELECT 1 FROM dante.schedule schedule
              JOIN dante.schedule_reminder_operation reminder
                ON reminder.schedule_ref=schedule.schedule_ref
             WHERE schedule.subject_native_ref=first_event
               AND reminder.created_at>first_seed_at
        ) OR EXISTS (
            SELECT 1 FROM dante.temporal_objective objective
             WHERE objective.subject_native_ref=first_event
               AND (objective.created_at>first_seed_at
                    OR objective.retired_at>first_seed_at)
        ) THEN
            RETURN 'local_change';
        END IF;
    END IF;
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
