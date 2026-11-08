"""Keep scoped profile metadata on the regenerated selected Occurrence.

Revision ID: 20261108_181
Revises: 20261108_180

This-and-following includes the selected date even if editing the recurrence
creates a different physical Occurrence identity or shifts the wall time.
From-next remains strictly after the selected instant. Protected exceptions
continue to use the accepted exclusion inventory; previous dates are not
retroactively modified.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261108_181"
down_revision: str | None = "20261108_180"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


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
           WHEN edits.scope_code='this_and_following'
                AND NOT requested_occurrence=ANY(edits.excluded_occurrence_refs) THEN
               (
                   dante.occurrence_edit_coordinate_instant(
                       actor,requested_occurrence,edits.effective_zone_id
                   ) > GREATEST(edits.anchor_at,edits.accepted_at)
                   OR (
                       dante.occurrence_edit_coordinate_instant(
                           actor,requested_occurrence,edits.effective_zone_id
                       ) AT TIME ZONE edits.effective_zone_id
                   )::date = (
                       edits.anchor_at AT TIME ZONE edits.effective_zone_id
                   )::date
               )
           WHEN edits.scope_code='from_next'
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


def upgrade() -> None:
    connection = op.get_bind()
    connection.execute(sa.text(_PROFILE_PATCH))
    signature = "dante.get_self_occurrence_profile_patch(uuid,uuid)"
    connection.exec_driver_sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
    connection.exec_driver_sql(
        f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator"
    )
    connection.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("Profile edit history and selected-boundary semantics are forward-only")
