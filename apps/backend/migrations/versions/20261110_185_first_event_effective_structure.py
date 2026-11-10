"""Keep the converted first Event current across series revisions.

A converted Event's original physical Schedule belongs to the linked first
Occurrence, like the linked first Activity of a Routine. The materialized
Occurrence's original governing state remains historical; subsequent accepted
series revisions can update its *effective* structure without replacing that
Occurrence or manufacturing a local-only override (which would protect it from
future series edits). The current first-structure state is owner-scoped and
CAS-checked inside the source-locked series-accept transaction.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261110_185"
down_revision: str | None = "20261110_184"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


_SET = r"""
CREATE FUNCTION dante.advance_self_event_recurring_first_structure(
    actor uuid, requested_source uuid, requested_first uuid,
    requested_previous_state uuid, requested_new_state uuid
) RETURNS void
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE current_state uuid; owned dante.event_recurring_seed%ROWTYPE;
BEGIN
    PERFORM pg_advisory_xact_lock(hashtextextended(
        'dante:recurrence-materialization:' || requested_source::text,0));
    SELECT * INTO owned
      FROM dante.event_recurring_seed seed
     WHERE seed.source_event_ref=requested_source
       AND seed.self_person_ref=actor
       AND seed.first_occurrence_ref=requested_first
     FOR UPDATE;
    IF NOT FOUND OR NOT EXISTS (
        SELECT 1 FROM dante.event_expectation e
         WHERE e.event_ref=owned.event_ref AND e.self_person_ref=actor
    ) OR NOT EXISTS (
        SELECT 1 FROM dante.event_expectation e
         WHERE e.event_ref=requested_source AND e.self_person_ref=actor
    ) OR NOT EXISTS (
        SELECT 1 FROM dante.get_self_recurring_structure_policy_revision(
            actor,'event',requested_source,requested_new_state
        )
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='event_recurring_first_structure_unavailable',
            MESSAGE='Converted first Event structure is unavailable';
    END IF;
    SELECT h.material_state_ref INTO current_state
      FROM dante.event_recurrence_current_history h
     WHERE h.event_ref=requested_source AND h.current_until_at IS NULL;
    IF current_state IS DISTINCT FROM requested_new_state
       OR NOT EXISTS (
         SELECT 1 FROM dante.event_recurrence_state old_state
          WHERE old_state.event_ref=requested_source
            AND old_state.material_state_ref=requested_previous_state
       )
       OR (
         owned.effective_structure_state_ref IS NOT NULL
         AND owned.effective_structure_state_ref<>requested_previous_state
         AND NOT EXISTS (
           SELECT 1 FROM dante.event_recurrence_state existing
            WHERE existing.material_state_ref=owned.effective_structure_state_ref
              AND existing.event_ref=requested_source
         )
       ) THEN
        RAISE EXCEPTION USING ERRCODE='23505',
            CONSTRAINT='event_recurring_first_structure_stale',
            MESSAGE='Converted first Event recurrence state changed';
    END IF;
    UPDATE dante.event_recurring_seed seed
       SET effective_structure_state_ref=requested_new_state
     WHERE seed.event_ref=owned.event_ref
       AND seed.self_person_ref=actor
       AND seed.first_occurrence_ref=requested_first;
END;
$function$;
"""


_GET = r"""
CREATE FUNCTION dante.get_self_event_recurring_first_structure(
    actor uuid, requested_first uuid
) RETURNS TABLE(source_event_ref uuid, effective_structure_state_ref uuid)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
    SELECT seed.source_event_ref,seed.effective_structure_state_ref
      FROM dante.event_recurring_seed seed
      JOIN dante.event_expectation original
        ON original.event_ref=seed.event_ref
       AND original.self_person_ref=actor
      JOIN dante.event_expectation source
        ON source.event_ref=seed.source_event_ref
       AND source.self_person_ref=actor
     WHERE seed.self_person_ref=actor
       AND seed.first_occurrence_ref=requested_first
$function$;
"""


def upgrade() -> None:
    db = op.get_bind()
    db.exec_driver_sql(
        "ALTER TABLE dante.event_recurring_seed "
        "ADD COLUMN effective_structure_state_ref uuid"
    )
    db.exec_driver_sql(
        "ALTER TABLE dante.event_recurring_seed "
        "ADD CONSTRAINT fk_event_recurring_seed_effective_structure "
        "FOREIGN KEY(effective_structure_state_ref) "
        "REFERENCES dante.material_state_address(material_state_ref)"
    )
    for definition in (_SET, _GET):
        db.exec_driver_sql(definition.replace("%", "%%"))
    for signature in (
        "advance_self_event_recurring_first_structure(uuid,uuid,uuid,uuid,uuid)",
        "get_self_event_recurring_first_structure(uuid,uuid)",
    ):
        db.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
        db.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION dante.{signature} "
            "FROM PUBLIC,dante_runtime,dante_migrator"
        )
        db.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("20261110_185 is forward-only")
