"""M1-B: bounded, self-owned materialized Occurrence inventory for edits.

This is a read-only capability. Existing B06 get_self_occurrence owns the
authorization and typed Occurrence projection. A future scope mutation MUST
re-read under a source CAS lock and revise the future source template; this
inventory does not authorize writes or enumerate unmaterialized future items.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261008_122"
down_revision: str | None = "20261008_121"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SIGNATURE = "list_self_recurrence_edit_occurrences(uuid,uuid)"


def upgrade() -> None:
    db = op.get_bind()
    db.exec_driver_sql("""
CREATE FUNCTION dante.list_self_recurrence_edit_occurrences(
    requested_self_person_ref uuid,
    requested_selected_occurrence_ref uuid
)
RETURNS TABLE(
    occurrence_ref uuid,
    source_native_ref uuid,
    governing_recurrence_state_ref uuid,
    origin_code text,
    family_code text,
    generated_date date,
    generated_wall_time time,
    clock_basis_code text,
    zone_id text,
    resolved_at timestamptz,
    expected_at timestamptz,
    period_start_date date,
    period_end_date_exclusive date,
    frame_code text,
    quota_zone_id text,
    position_index integer,
    skipped boolean,
    skip_reason text,
    skipped_at timestamptz
)
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE bound_source_ref uuid;
BEGIN
    -- The B06 self-scoped function is the single existing ownership gate.
    -- This also works for a selected Routine-materialized Activity's
    -- governing Occurrence as well as a recurring Event Occurrence.
    SELECT picked.source_native_ref INTO bound_source_ref
      FROM dante.get_self_occurrence(
          requested_self_person_ref,requested_selected_occurrence_ref
      ) AS picked;
    IF bound_source_ref IS NULL THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='recurrence_edit_occurrence_unavailable',
            MESSAGE='Selected Occurrence unavailable in self scope';
    END IF;

    -- No browser-window truncation: scan *all* accepted materialized
    -- Occurrences of that source, including skipped and scheduled rows.
    -- Exceeding the bound fails; an incomplete result is never returned.
    IF (
        SELECT count(*)
          FROM (
            SELECT 1
              FROM dante.occurrence_generation AS candidate
             WHERE candidate.source_native_ref=bound_source_ref
             LIMIT 10001
          ) AS bounded
    ) > 10000 THEN
        RAISE EXCEPTION USING ERRCODE='22023',
            CONSTRAINT='recurrence_edit_inventory_limit',
            MESSAGE='More than 10000 materialized Occurrences; cannot preview safely';
    END IF;

    RETURN QUERY
    SELECT item.*
      FROM dante.occurrence_generation AS generation
      CROSS JOIN LATERAL dante.get_self_occurrence(
          requested_self_person_ref,generation.occurrence_ref
      ) AS item
     WHERE generation.source_native_ref=bound_source_ref
     ORDER BY item.occurrence_ref;
END;
$function$;
""")
    db.exec_driver_sql(
        f"ALTER FUNCTION dante.{_SIGNATURE} OWNER TO dante_owner"
    )
    db.exec_driver_sql(
        f"REVOKE ALL ON FUNCTION dante.{_SIGNATURE} "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )
    db.exec_driver_sql(
        f"GRANT EXECUTE ON FUNCTION dante.{_SIGNATURE} TO dante_runtime"
    )


def downgrade() -> None:
    raise RuntimeError(
        "20261008_122 is forward-only; edit-inventory authority requires review"
    )
