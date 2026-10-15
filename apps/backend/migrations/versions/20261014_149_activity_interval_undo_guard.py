"""Keep generic Schedule Undo outside coordinated Activity interval changes.

Revision ID: 20261014_149
Revises: 20261014_148

The application rejects direct revision and unschedule, but a coordinated
interval removal leaves an ordinary unschedule receipt. Its generic Undo must
not restore that interval outside the Activity replan and Session decision.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261014_149"
down_revision: str | None = "20261014_148"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


_ANCHOR = """            IF EXISTS (
                SELECT 1 FROM dante.scoped_current_material_state AS current"""

_GUARD = """            -- Serialize against planned Session Start before the Undo check.
            PERFORM 1 FROM dante.activity_intention AS activity
              JOIN dante.schedule AS owned
                ON owned.subject_native_ref=activity.activity_ref
             WHERE owned.schedule_ref=requested_schedule_ref
               AND activity.self_person_ref=requested_self_person_ref
             FOR UPDATE OF activity;
            IF EXISTS (
                SELECT 1 FROM dante.schedule AS owned
                JOIN dante.activity_intention AS activity
                  ON activity.activity_ref=owned.subject_native_ref
                 AND activity.self_person_ref=requested_self_person_ref
                JOIN dante.get_self_activity_schedule_roles(
                  requested_self_person_ref, ARRAY[activity.activity_ref]
                ) AS purpose ON purpose.schedule_ref=owned.schedule_ref
                WHERE owned.schedule_ref=requested_schedule_ref
                  AND (purpose.role_code='interval'
                       OR (purpose.role_code='envelope' AND (
                           EXISTS (
                               SELECT 1 FROM dante.get_self_activity_schedule_roles(
                                 requested_self_person_ref, ARRAY[activity.activity_ref]
                               ) AS sibling WHERE sibling.role_code='interval'
                           ) OR EXISTS (
                               SELECT 1 FROM dante.list_self_subject_sessions(
                                 requested_self_person_ref, activity.activity_ref
                               )
                           )
                       )))
            ) THEN
                RAISE EXCEPTION USING ERRCODE='23514',
                    CONSTRAINT='schedule_activity_interval_requires_replan',
                    MESSAGE='Activity interval Undo requires a coordinated Activity replan';
            END IF;

"""


def upgrade() -> None:
    bind = op.get_bind()
    signature = "dante.undo_self_schedule_unschedule_any(uuid,text,text,uuid,text,uuid)"
    definition = bind.exec_driver_sql(
        f"SELECT pg_get_functiondef('{signature}'::regprocedure)"
    ).scalar_one()
    if definition.count(_ANCHOR) != 1 or "schedule_activity_interval_requires_replan" in definition:
        raise RuntimeError("Unexpected Schedule Undo contract; review the forward guard")
    # CREATE OR REPLACE keeps the existing owner and exact EXECUTE grants.
    bind.exec_driver_sql(definition.replace(_ANCHOR, _GUARD + _ANCHOR).replace("%", "%%"))


def downgrade() -> None:
    raise RuntimeError("Coordinated Activity interval Undo guard is forward-only")
