"""B08-A repair: bind Session start to the requested subject family.

Revision ID: 20260924_59
Revises: 20260924_58

The HTTP surface distinguishes Activity and Occurrence start commands.  The
bounded PostgreSQL capability must enforce that same distinction rather than
accepting either family for either endpoint.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260924_59"
down_revision: str | None = "20260924_58"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"
_OLD_SIGNATURE = "dante.start_self_session(uuid,text,text,uuid,uuid,uuid)"
_NEW_SIGNATURE = "dante.start_self_session(uuid,text,text,uuid,uuid,text,uuid)"


def _sql(statement: str) -> None:
    op.execute(sa.text(statement))


def _create_family_bound_start() -> None:
    _sql(
        r"""
CREATE FUNCTION dante.start_self_session(
  requested_self_person_ref uuid,
  requested_operation_id text,
  requested_intent_fingerprint text,
  requested_session_ref uuid,
  requested_material_state_ref uuid,
  requested_subject_family text,
  requested_subject_native_ref uuid
) RETURNS TABLE(
  session_ref uuid,
  subject_native_ref uuid,
  timing_material_state_ref uuid,
  started_at timestamptz,
  ended_at timestamptz,
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
  existing_fingerprint text;
  existing_session_ref uuid;
  recorded_at timestamptz := statement_timestamp();
  actual_subject_family text;
BEGIN
  IF requested_subject_family IS NULL
     OR requested_subject_family NOT IN ('activity', 'occurrence') THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='session_subject_family_invalid',
      MESSAGE='Session subject family rejected';
  END IF;

  SELECT address.owner_family
    INTO actual_subject_family
    FROM dante.native_address AS address
   WHERE address.native_ref = requested_subject_native_ref;

  IF NOT EXISTS (
    SELECT 1 FROM dante.person WHERE person_ref = requested_self_person_ref
  ) OR actual_subject_family IS DISTINCT FROM requested_subject_family
     OR NOT dante._session_subject_owned(
       requested_self_person_ref, requested_subject_native_ref
     ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='session_subject_unavailable',
      MESSAGE='Session subject unavailable';
  END IF;
  IF normalized_operation_id = '' OR char_length(normalized_operation_id) > 200 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_session_start_operation_operation_id',
      MESSAGE='Session operation id rejected';
  END IF;
  IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_session_start_operation_fingerprint',
      MESSAGE='Session operation fingerprint rejected';
  END IF;
  IF uuid_extract_version(requested_session_ref) IS DISTINCT FROM 7
     OR uuid_extract_version(requested_material_state_ref) IS DISTINCT FROM 7 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      MESSAGE='Session reference rejected';
  END IF;

  PERFORM pg_advisory_xact_lock(
    hashtextextended(requested_self_person_ref::text || ':' || normalized_operation_id, 0)
  );

  SELECT operation.intent_fingerprint, operation.session_ref
    INTO existing_fingerprint, existing_session_ref
    FROM dante.session_start_operation AS operation
   WHERE operation.self_person_ref = requested_self_person_ref
     AND operation.operation_id = normalized_operation_id;
  IF FOUND THEN
    IF existing_fingerprint <> requested_intent_fingerprint THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        CONSTRAINT='session_operation_reused',
        MESSAGE='Session operation id reused with different intent';
    END IF;
    RETURN QUERY
    SELECT subject.session_ref,
           subject.subject_native_ref,
           timing.material_state_ref,
           absolute_timing.started_at,
           absolute_timing.ended_at,
           true
      FROM dante.session_execution_subject AS subject
      JOIN dante.session_timing_current_history AS timing
        ON timing.session_ref = subject.session_ref
       AND timing.current_until_at IS NULL
      JOIN dante.session_timing_absolute AS absolute_timing
        ON absolute_timing.material_state_ref = timing.material_state_ref
     WHERE subject.session_ref = existing_session_ref;
    RETURN;
  END IF;

  INSERT INTO dante.session(session_ref) VALUES (requested_session_ref);
  INSERT INTO dante.native_address(native_ref, owner_family)
  VALUES (requested_session_ref, 'session');
  INSERT INTO dante.material_state_address(material_state_ref, native_owner_ref, facet_code)
  VALUES (requested_material_state_ref, requested_session_ref, 'session.timing');
  INSERT INTO dante.session_timing_state(material_state_ref, session_ref, timing_form_code)
  VALUES (requested_material_state_ref, requested_session_ref, 'absolute');
  INSERT INTO dante.session_timing_absolute(
    material_state_ref, started_at, start_precision_code
  ) VALUES (requested_material_state_ref, recorded_at, 'exact');
  INSERT INTO dante.native_current_material_state(
    native_owner_ref, facet_code, material_state_ref
  ) VALUES (requested_session_ref, 'session.timing', requested_material_state_ref);
  INSERT INTO dante.session_timing_current_history(
    session_ref, material_state_ref, current_from_at
  ) VALUES (requested_session_ref, requested_material_state_ref, recorded_at);
  INSERT INTO dante.session_execution_subject(session_ref, subject_native_ref)
  VALUES (requested_session_ref, requested_subject_native_ref);
  INSERT INTO dante.session_start_operation(
    self_person_ref, operation_id, intent_fingerprint, session_ref,
    subject_native_ref, created_at
  ) VALUES (
    requested_self_person_ref, normalized_operation_id, requested_intent_fingerprint,
    requested_session_ref, requested_subject_native_ref, recorded_at
  );

  RETURN QUERY
  SELECT requested_session_ref, requested_subject_native_ref,
         requested_material_state_ref, recorded_at, NULL::timestamptz, false;
END;
$function$
"""
    )
    _sql(f"ALTER FUNCTION {_NEW_SIGNATURE} OWNER TO {_OWNER}")
    _sql(f"REVOKE ALL ON FUNCTION {_NEW_SIGNATURE} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}")
    _sql(f"GRANT EXECUTE ON FUNCTION {_NEW_SIGNATURE} TO {_RUNTIME}")


def upgrade() -> None:
    """Replace the permissive start signature with an exact-family capability."""
    _create_family_bound_start()
    _sql(f"REVOKE ALL ON FUNCTION {_OLD_SIGNATURE} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}")
    _sql(f"DROP FUNCTION {_OLD_SIGNATURE}")


def downgrade() -> None:
    """Refuse to restore the permissive start contract after B08-A repair."""
    raise RuntimeError(
        "B08-A _59 is forward-only: downgrading would restore a Session subject-family contract that is known to be invalid"
    )
