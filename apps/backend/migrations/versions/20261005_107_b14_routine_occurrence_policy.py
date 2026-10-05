"""B14: Routine occurrence placement/reminder policy for manual recurring Activity Create.

The policy is source intent, not Schedule truth. Each materialized Occurrence
still receives its own Schedule and, when configured, its own B11-C Reminder.

Revision ID: 20261005_107
Revises: 20261005_106
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261005_107"
down_revision: str | None = "20261005_106"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _sql(value: str) -> None:
    op.execute(sa.text(value))


def upgrade() -> None:
    op.create_table(
        "routine_occurrence_policy",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("routine_ref", sa.Uuid(), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("reminder_lead_minutes", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref", "routine_ref", name="pk_routine_occurrence_policy"
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_routine_occurrence_policy_person",
            ondelete="NO ACTION",
            onupdate="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["routine_ref"],
            ["dante.routine.routine_ref"],
            name="fk_routine_occurrence_policy_routine",
            ondelete="NO ACTION",
            onupdate="NO ACTION",
        ),
        sa.CheckConstraint(
            "duration_minutes BETWEEN 1 AND 525600",
            name="ck_routine_occurrence_policy_duration",
        ),
        sa.CheckConstraint(
            "reminder_lead_minutes IS NULL OR reminder_lead_minutes BETWEEN 0 AND 10080",
            name="ck_routine_occurrence_policy_reminder",
        ),
        schema="dante",
    )
    op.create_index(
        "ix_routine_occurrence_policy_routine",
        "routine_occurrence_policy",
        ["routine_ref", "self_person_ref"],
        unique=True,
        schema="dante",
    )

    _sql(_SET_POLICY)
    _sql(_GET_POLICY)
    for name, signature in (
        ("set_self_routine_occurrence_policy", "uuid,uuid,integer,integer"),
        ("get_self_routine_occurrence_policy", "uuid,uuid"),
    ):
        _sql(f"REVOKE ALL ON FUNCTION dante.{name}({signature}) FROM PUBLIC")
        _sql(f"GRANT EXECUTE ON FUNCTION dante.{name}({signature}) TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError(
        "20261005_107 is forward-only after Routine occurrence policy becomes authoring truth"
    )


_SET_POLICY = r'''
CREATE FUNCTION dante.set_self_routine_occurrence_policy(
    requested_self_person_ref uuid,
    requested_routine_ref uuid,
    requested_duration_minutes integer,
    requested_reminder_lead_minutes integer
) RETURNS TABLE(duration_minutes integer, reminder_lead_minutes integer, created_at timestamptz, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE
    prior dante.routine_occurrence_policy%ROWTYPE;
    recorded_at timestamptz := statement_timestamp();
BEGIN
    IF requested_duration_minutes IS NULL
       OR requested_duration_minutes NOT BETWEEN 1 AND 525600
       OR (requested_reminder_lead_minutes IS NOT NULL
           AND requested_reminder_lead_minutes NOT BETWEEN 0 AND 10080)
    THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='routine_occurrence_policy_invalid',
          MESSAGE='Routine occurrence policy rejected';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM dante.routine_intention AS routine
         WHERE routine.routine_ref=requested_routine_ref
           AND routine.self_person_ref=requested_self_person_ref
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23503',
          CONSTRAINT='routine_occurrence_policy_routine_unavailable',
          MESSAGE='Routine occurrence policy source unavailable';
    END IF;

    SELECT * INTO prior
      FROM dante.routine_occurrence_policy
     WHERE self_person_ref=requested_self_person_ref
       AND routine_ref=requested_routine_ref;
    IF FOUND THEN
        IF prior.duration_minutes<>requested_duration_minutes
           OR prior.reminder_lead_minutes IS DISTINCT FROM requested_reminder_lead_minutes
        THEN
            RAISE EXCEPTION USING ERRCODE='23505',
              CONSTRAINT='pk_routine_occurrence_policy',
              MESSAGE='Routine occurrence policy already exists with different intent';
        END IF;
        RETURN QUERY SELECT prior.duration_minutes,prior.reminder_lead_minutes,prior.created_at,true;
        RETURN;
    END IF;

    INSERT INTO dante.routine_occurrence_policy(
        self_person_ref,routine_ref,duration_minutes,reminder_lead_minutes,created_at
    ) VALUES(
        requested_self_person_ref,requested_routine_ref,requested_duration_minutes,
        requested_reminder_lead_minutes,recorded_at
    );
    RETURN QUERY SELECT requested_duration_minutes,requested_reminder_lead_minutes,recorded_at,false;
END;
$function$;
'''

_GET_POLICY = r'''
CREATE FUNCTION dante.get_self_routine_occurrence_policy(
    requested_self_person_ref uuid,
    requested_routine_ref uuid
) RETURNS TABLE(duration_minutes integer, reminder_lead_minutes integer, created_at timestamptz)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
SELECT policy.duration_minutes,policy.reminder_lead_minutes,policy.created_at
  FROM dante.routine_occurrence_policy AS policy
  JOIN dante.routine_intention AS routine ON routine.routine_ref=policy.routine_ref
 WHERE policy.self_person_ref=requested_self_person_ref
   AND policy.routine_ref=requested_routine_ref
   AND routine.self_person_ref=requested_self_person_ref
$function$;
'''
