"""Owner-scoped selectable recurring Event Occurrence identities.

Revision ID: 20261015_156
Revises: 20261015_155

A recurring Event uses one Event source and separately addressable
Occurrences, so the Inspector cannot treat source id as selected instance id.
This bounded read capability exposes current materialized Occurrences without
granting runtime table SELECT or allowing source/instance identity confusion.
"""
from collections.abc import Sequence

from alembic import op

revision: str = "20261015_156"
down_revision: str | None = "20261015_155"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_CHOICES = r"""
CREATE FUNCTION dante.list_self_event_deletion_occurrences(
    requested_actor uuid, requested_event uuid
) RETURNS TABLE(
    occurrence_ref uuid, schedule_ref uuid, display_label text
)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $choices$
    SELECT generation.occurrence_ref,
           schedule.schedule_ref,
           COALESCE(
               zoned.starts_local_at::text,
               floating.starts_local_at::text,
               upper(dates.date_span)::text,
               generation.occurrence_ref::text
           ) AS display_label
      FROM dante.event_expectation AS owned
      JOIN dante.occurrence_generation AS generation
        ON generation.source_native_ref=owned.event_ref
      LEFT JOIN dante.occurrence_skip AS skipped
        ON skipped.occurrence_ref=generation.occurrence_ref
      LEFT JOIN dante.schedule AS schedule
        ON schedule.subject_native_ref=generation.occurrence_ref
      LEFT JOIN dante.schedule_current_placement AS current
        ON current.scoped_owner_ref=schedule.schedule_ref
      LEFT JOIN dante.schedule_placement_named_zone_state AS zoned
        ON zoned.material_state_ref=current.material_state_ref
      LEFT JOIN dante.schedule_placement_floating_local_state AS floating
        ON floating.material_state_ref=current.material_state_ref
      LEFT JOIN dante.schedule_placement_date_state AS dates
        ON dates.material_state_ref=current.material_state_ref
     WHERE owned.event_ref=requested_event
       AND owned.self_person_ref=requested_actor
       AND skipped.occurrence_ref IS NULL
     ORDER BY display_label DESC,generation.occurrence_ref DESC
     LIMIT 1000
$choices$;
"""


def upgrade() -> None:
    db = op.get_bind()
    db.exec_driver_sql(_CHOICES)
    name = "dante.list_self_event_deletion_occurrences(uuid,uuid)"
    db.exec_driver_sql(f"ALTER FUNCTION {name} OWNER TO dante_owner")
    db.exec_driver_sql(
        f"REVOKE ALL ON FUNCTION {name} FROM PUBLIC,dante_migrator,dante_runtime"
    )
    db.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {name} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("Scoped recurring Event choice is forward-only")
