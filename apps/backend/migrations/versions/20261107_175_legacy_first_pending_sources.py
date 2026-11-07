"""Inventory pending first Event bindings without a per-Event transaction.

Revision ID: 20261107_175
Revises: 20261107_174
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261107_175"
down_revision: str | None = "20261107_174"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_index(
        "ix_event_recurring_seed_pending_first",
        "event_recurring_seed",
        ["self_person_ref", "source_event_ref"],
        schema="dante",
        unique=False,
        postgresql_where=sa.text("first_occurrence_ref IS NULL"),
    )
    connection = op.get_bind()
    connection.exec_driver_sql(_PENDING)
    signature = "list_self_event_pending_first_sources(uuid)"
    connection.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
    connection.exec_driver_sql(
        f"REVOKE ALL ON FUNCTION dante.{signature} FROM PUBLIC,dante_runtime,dante_migrator"
    )
    connection.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("20261107_175 is forward-only")


_PENDING = r"""
CREATE FUNCTION dante.list_self_event_pending_first_sources(actor uuid)
RETURNS TABLE(source_event_ref uuid)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
    SELECT seed.source_event_ref
      FROM dante.event_recurring_seed AS seed
      JOIN dante.event_expectation AS original
        ON original.event_ref=seed.event_ref
       AND original.self_person_ref=actor
      JOIN dante.event_expectation AS recurring
        ON recurring.event_ref=seed.source_event_ref
       AND recurring.self_person_ref=actor
      JOIN dante.event_recurrence_current_history AS active
        ON active.event_ref=seed.source_event_ref
       AND active.current_until_at IS NULL
     WHERE seed.self_person_ref=actor
       AND seed.first_occurrence_ref IS NULL
       -- A changed recurrence state or a missing historical exclusion is
       -- not repairable. Do not reopen an expensive SERIALIZABLE transaction
       -- for those permanently ineligible sources on every Timeline load.
       AND EXISTS (
           SELECT 1
             FROM dante.occurrence_exclusion AS excluded
             JOIN dante.occurrence_exclusion_operation AS provenance
               ON provenance.exclusion_ref=excluded.exclusion_ref
              AND provenance.self_person_ref=actor
            WHERE excluded.self_person_ref=actor
              AND excluded.source_native_ref=seed.source_event_ref
              AND excluded.governing_recurrence_state_ref=active.material_state_ref
              AND excluded.family_code='calendar_wall_clock'
              AND provenance.operation_id
                  ~ '^b06d:existing-event-first:[0-9a-f]{64}$'
       )
     ORDER BY seed.source_event_ref
$function$;
"""
