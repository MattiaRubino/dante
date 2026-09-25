"""B09-B repair: qualify Event column references inside authoring functions.

Revision ID: 20260925_68
Revises: 20260925_67

`_67` names PL/pgSQL OUT columns `event_ref`, `participant_person_ref`,
`requirement_code`, and `established_at`. Unqualified references to those
names are ambiguous under `#variable_conflict error`. This revision replaces
the two Event Participation function bodies. Signatures, grants, and object
counts stay the same.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260925_68"
down_revision: str | None = "20260925_67"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"


def _sql(statement: str) -> None:
    op.execute(sa.text(statement))


def upgrade() -> None:
    """Replace the ambiguous Event Participation function bodies."""
    _sql(
        r"""
CREATE OR REPLACE FUNCTION dante.set_self_event_expected_participation(
  requested_self_person_ref uuid,
  requested_operation_id text,
  requested_intent_fingerprint text,
  requested_event_ref uuid,
  requested_participant_person_ref uuid,
  requested_requirement_code text,
  requested_expected_requirement_code text
) RETURNS TABLE(
  event_ref uuid,
  participant_person_ref uuid,
  requirement_code text,
  established_at timestamptz,
  replayed boolean
)
LANGUAGE plpgsql
SECURITY DEFINER
VOLATILE
PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
DECLARE
  normalized_operation_id text := btrim(requested_operation_id);
  previous_fingerprint text;
  previous_event_ref uuid;
  previous_person_ref uuid;
  previous_requirement text;
  previous_accepted_at timestamptz;
  current_requirement text;
  current_found boolean;
  recorded_at timestamptz := statement_timestamp();
BEGIN
  IF normalized_operation_id = '' OR char_length(normalized_operation_id) > 200 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_event_expected_participation_operation_operation_id',
      MESSAGE='Participation operation id rejected';
  END IF;
  IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_event_expected_participation_operation_fingerprint',
      MESSAGE='Participation operation fingerprint rejected';
  END IF;
  IF requested_requirement_code IS NOT NULL
     AND requested_requirement_code NOT IN ('required','optional') THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_event_expected_participation_requirement',
      MESSAGE='Expected Participation requirement rejected';
  END IF;

  PERFORM pg_advisory_xact_lock(
    hashtextextended(
      requested_self_person_ref::text || ':participation:' || normalized_operation_id, 0
    )
  );

  SELECT receipt.intent_fingerprint, receipt.event_ref,
         receipt.participant_person_ref, receipt.requirement_code, receipt.accepted_at
    INTO previous_fingerprint, previous_event_ref,
         previous_person_ref, previous_requirement, previous_accepted_at
    FROM dante.event_expected_participation_operation AS receipt
   WHERE receipt.self_person_ref = requested_self_person_ref
     AND receipt.operation_id = normalized_operation_id;
  IF FOUND THEN
    IF previous_fingerprint <> requested_intent_fingerprint
       OR previous_event_ref <> requested_event_ref
       OR previous_person_ref <> requested_participant_person_ref THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        CONSTRAINT='participation_operation_reused',
        MESSAGE='Participation operation id reused with different intent';
    END IF;
    RETURN QUERY
    SELECT previous_event_ref, previous_person_ref, previous_requirement,
           previous_accepted_at, true;
    RETURN;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM dante.event_expectation AS expectation
     WHERE expectation.event_ref = requested_event_ref
       AND expectation.self_person_ref = requested_self_person_ref
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='participation_event_unavailable',
      MESSAGE='Event is unavailable in current self scope';
  END IF;

  IF NOT dante._self_referenceable_person(
    requested_self_person_ref, requested_participant_person_ref
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='participation_person_unavailable',
      MESSAGE='Participant Person is not referenceable by this actor';
  END IF;

  SELECT participation.requirement_code, true
    INTO current_requirement, current_found
    FROM dante.event_expected_participation AS participation
   WHERE participation.event_ref = requested_event_ref
     AND participation.participant_person_ref = requested_participant_person_ref
   FOR UPDATE;
  IF NOT FOUND THEN
    current_requirement := NULL;
    current_found := false;
  END IF;

  IF current_requirement IS DISTINCT FROM requested_expected_requirement_code THEN
    RAISE EXCEPTION USING ERRCODE='40001',
      CONSTRAINT='participation_expected_requirement_conflict',
      MESSAGE='Expected Participation changed since it was read';
  END IF;
  IF current_requirement IS NOT DISTINCT FROM requested_requirement_code THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='participation_no_change',
      MESSAGE='Expected Participation already matches the requested value';
  END IF;

  IF requested_requirement_code IS NULL THEN
    DELETE FROM dante.event_expected_participation AS participation
     WHERE participation.event_ref = requested_event_ref
       AND participation.participant_person_ref = requested_participant_person_ref;
  ELSIF current_found THEN
    UPDATE dante.event_expected_participation AS participation
       SET requirement_code = requested_requirement_code,
           established_at = recorded_at
     WHERE participation.event_ref = requested_event_ref
       AND participation.participant_person_ref = requested_participant_person_ref;
  ELSE
    INSERT INTO dante.event_expected_participation(
      event_ref, participant_person_ref, requirement_code, established_at
    ) VALUES (
      requested_event_ref, requested_participant_person_ref,
      requested_requirement_code, recorded_at
    );
  END IF;

  INSERT INTO dante.event_expected_participation_operation(
    self_person_ref, operation_id, intent_fingerprint, event_ref,
    participant_person_ref, requirement_code, accepted_at
  ) VALUES (
    requested_self_person_ref, normalized_operation_id, requested_intent_fingerprint,
    requested_event_ref, requested_participant_person_ref,
    requested_requirement_code, recorded_at
  );

  RETURN QUERY
  SELECT requested_event_ref, requested_participant_person_ref,
         requested_requirement_code, recorded_at, false;
END;
$function$
"""
    )
    _sql(
        r"""
CREATE OR REPLACE FUNCTION dante.list_self_event_expected_participation(
  requested_self_person_ref uuid,
  requested_event_ref uuid
) RETURNS TABLE(
  event_ref uuid,
  participant_person_ref uuid,
  requirement_code text,
  established_at timestamptz
)
LANGUAGE plpgsql
SECURITY DEFINER
STABLE
PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM dante.event_expectation AS expectation
     WHERE expectation.event_ref = requested_event_ref
       AND expectation.self_person_ref = requested_self_person_ref
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='participation_event_unavailable',
      MESSAGE='Event is unavailable in current self scope';
  END IF;
  RETURN QUERY
  SELECT participation.event_ref,
         participation.participant_person_ref,
         participation.requirement_code,
         participation.established_at
    FROM dante.event_expected_participation AS participation
   WHERE participation.event_ref = requested_event_ref
   ORDER BY participation.requirement_code, participation.participant_person_ref;
END;
$function$
"""
    )
    for name, signature in (
        (
            "set_self_event_expected_participation",
            "uuid,text,text,uuid,uuid,text,text",
        ),
        ("list_self_event_expected_participation", "uuid,uuid"),
    ):
        qualified = f"{_SCHEMA}.{name}({signature})"
        _sql(f"ALTER FUNCTION {qualified} OWNER TO {_OWNER}")
        _sql(f"REVOKE ALL ON FUNCTION {qualified} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}")
        _sql(f"GRANT EXECUTE ON FUNCTION {qualified} TO {_RUNTIME}")


def downgrade() -> None:
    """Refuse rollback of a body-only repair that does not remove objects."""
    _sql(
        "DO $block$ BEGIN RAISE EXCEPTION USING ERRCODE='55000', "
        "MESSAGE='B09-B column-qualification downgrade refused'; END; $block$"
    )
