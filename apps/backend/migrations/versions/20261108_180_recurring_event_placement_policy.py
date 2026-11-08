"""Add immutable recurring Event placement protection to initial source policy.

Forward-only: previously accepted Event policies remain unlocked. The V3
functions reuse the canonical V2 source ownership and replay contract.

Revision ID: 20261108_180
Revises: 20261108_179
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261108_180"
down_revision: str | None = "20261108_179"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "event_occurrence_policy",
        sa.Column("placement_protected", sa.Boolean(), nullable=False, server_default=sa.false()),
        schema="dante",
    )
    connection = op.get_bind()
    connection.exec_driver_sql(_SET_V3)
    connection.exec_driver_sql(_GET_V3)
    for signature in (
        "set_self_event_occurrence_policy_v3(uuid,uuid,text,integer,integer,integer,text,jsonb,boolean)",
        "get_self_event_occurrence_policy_v3(uuid,uuid)",
    ):
        connection.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
        connection.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION dante.{signature} FROM PUBLIC,dante_runtime,dante_migrator"
        )
        connection.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("20261108_180 is forward-only")


_SET_V3 = r"""
CREATE FUNCTION dante.set_self_event_occurrence_policy_v3(
    requested_actor uuid,
    requested_event uuid,
    requested_kind text,
    requested_minutes integer,
    requested_days integer,
    requested_reminder integer,
    requested_reality text,
    requested_objectives jsonb,
    requested_protection boolean
) RETURNS TABLE(
    placement_kind text,
    duration_minutes integer,
    duration_days integer,
    reminder_lead_minutes integer,
    reality_mode text,
    objectives jsonb,
    placement_protected boolean,
    created_at timestamptz,
    replayed boolean
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
DECLARE
    accepted record;
    prior_protection boolean;
BEGIN
    IF requested_protection IS NULL THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='event_occurrence_policy_invalid',
          MESSAGE='Recurring Event placement protection must be boolean';
    END IF;

    -- V2 retains the authoritative owner check and immutable intent.
    -- V3 stages the new flag in that same transaction on first creation.
    SELECT * INTO accepted
      FROM dante.set_self_event_occurrence_policy_v2(
        requested_actor,requested_event,requested_kind,requested_minutes,
        requested_days,requested_reminder,requested_reality,requested_objectives);

    IF accepted.replayed THEN
        SELECT p.placement_protected INTO prior_protection
          FROM dante.event_occurrence_policy AS p
         WHERE p.self_person_ref=requested_actor
           AND p.event_ref=requested_event FOR UPDATE;
        IF prior_protection IS DISTINCT FROM requested_protection THEN
            RAISE EXCEPTION USING ERRCODE='23505',
              CONSTRAINT='pk_event_occurrence_policy',
              MESSAGE='Recurring Event placement intent differs on replay';
        END IF;
    ELSIF requested_protection THEN
        UPDATE dante.event_occurrence_policy AS p
           SET placement_protected=true
         WHERE p.self_person_ref=requested_actor
           AND p.event_ref=requested_event;
    END IF;

    RETURN QUERY SELECT
        accepted.placement_kind,accepted.duration_minutes,accepted.duration_days,
        accepted.reminder_lead_minutes,accepted.reality_mode,accepted.objectives,
        requested_protection,accepted.created_at,accepted.replayed;
END;
$function$;
"""


_GET_V3 = r"""
CREATE FUNCTION dante.get_self_event_occurrence_policy_v3(uuid,uuid)
RETURNS TABLE(
    placement_kind text,
    duration_minutes integer,
    duration_days integer,
    reminder_lead_minutes integer,
    reality_mode text,
    objectives jsonb,
    placement_protected boolean,
    created_at timestamptz
)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
SELECT p.placement_kind,p.duration_minutes,p.duration_days,
       p.reminder_lead_minutes,p.reality_mode,p.objectives,
       p.placement_protected,p.created_at
  FROM dante.event_occurrence_policy AS p
  JOIN dante.event_expectation AS e ON e.event_ref=p.event_ref
 WHERE p.self_person_ref=$1 AND p.event_ref=$2 AND e.self_person_ref=$1
$function$;
"""
