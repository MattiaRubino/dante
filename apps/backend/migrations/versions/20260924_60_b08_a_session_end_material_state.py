"""B08-A repair: Session END replaces immutable timing MaterialState.

Revision ID: 20260924_60
Revises: 20260924_59

The CP6 Session timing payload is a MaterialState payload and is not a mutable
runtime record.  END therefore creates a new session.timing MaterialState,
advances current/history atomically, and records the exact produced state in
the idempotency receipt.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260924_60"
down_revision: str | None = "20260924_59"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"
_OLD_SIGNATURE = "dante.end_self_session(uuid,text,text,uuid,uuid)"
_NEW_SIGNATURE = "dante.end_self_session(uuid,text,text,uuid,uuid,uuid)"


def _sql(statement: str) -> None:
    op.execute(sa.text(statement))


def _repair_existing_end_receipts() -> None:
    """Split any _58 in-place END into historical open + current ended states."""
    _sql(
        r"""
DO $repair$
DECLARE
  receipt record;
  previous_started_at timestamptz;
  previous_start_precision text;
  previous_ended_at timestamptz;
  previous_end_precision text;
  repaired_state uuid;
  affected integer;
BEGIN
  FOR receipt IN
    SELECT self_person_ref, operation_id, session_ref,
           expected_material_state_ref, created_at
      FROM dante.session_end_operation
     ORDER BY created_at, self_person_ref, operation_id
  LOOP
    SELECT absolute_timing.started_at,
           absolute_timing.start_precision_code,
           absolute_timing.ended_at,
           absolute_timing.end_precision_code
      INTO STRICT previous_started_at, previous_start_precision,
                  previous_ended_at, previous_end_precision
      FROM dante.session_timing_absolute AS absolute_timing
     WHERE absolute_timing.material_state_ref = receipt.expected_material_state_ref;

    IF previous_ended_at IS NULL OR previous_end_precision IS NULL THEN
      RAISE EXCEPTION USING ERRCODE='55000',
        MESSAGE='B08-A _60 repair refused: legacy end receipt has no ended timing payload';
    END IF;

    repaired_state := uuidv7();

    INSERT INTO dante.material_state_address(
      material_state_ref, native_owner_ref, facet_code
    ) VALUES (
      repaired_state, receipt.session_ref, 'session.timing'
    );
    INSERT INTO dante.session_timing_state(
      material_state_ref, session_ref, timing_form_code
    ) VALUES (
      repaired_state, receipt.session_ref, 'absolute'
    );
    INSERT INTO dante.session_timing_absolute(
      material_state_ref, started_at, start_precision_code,
      ended_at, end_precision_code
    ) VALUES (
      repaired_state, previous_started_at, previous_start_precision,
      previous_ended_at, previous_end_precision
    );
    INSERT INTO dante.session_timing_pause(
      material_state_ref, paused_at, pause_precision_code,
      resumed_at, resume_precision_code
    )
    SELECT repaired_state, pause.paused_at, pause.pause_precision_code,
           pause.resumed_at, pause.resume_precision_code
      FROM dante.session_timing_pause AS pause
     WHERE pause.material_state_ref = receipt.expected_material_state_ref;

    -- Migration-only repair of the _58 mutable payload. Runtime never updates
    -- Session timing payloads after this revision.
    UPDATE dante.session_timing_absolute
       SET ended_at = NULL,
           end_precision_code = NULL
     WHERE material_state_ref = receipt.expected_material_state_ref;

    UPDATE dante.native_current_material_state
       SET material_state_ref = repaired_state
     WHERE native_owner_ref = receipt.session_ref
       AND facet_code = 'session.timing'
       AND material_state_ref = receipt.expected_material_state_ref;
    GET DIAGNOSTICS affected = ROW_COUNT;
    IF affected <> 1 THEN
      RAISE EXCEPTION USING ERRCODE='55000',
        MESSAGE='B08-A _60 repair refused: legacy current binding is inconsistent';
    END IF;

    UPDATE dante.session_timing_current_history
       SET current_until_at = previous_ended_at
     WHERE session_ref = receipt.session_ref
       AND material_state_ref = receipt.expected_material_state_ref
       AND current_until_at IS NULL;
    GET DIAGNOSTICS affected = ROW_COUNT;
    IF affected <> 1 THEN
      RAISE EXCEPTION USING ERRCODE='55000',
        MESSAGE='B08-A _60 repair refused: legacy current history is inconsistent';
    END IF;

    INSERT INTO dante.session_timing_current_history(
      session_ref, material_state_ref, current_from_at
    ) VALUES (
      receipt.session_ref, repaired_state, previous_ended_at
    );

    UPDATE dante.session_end_operation
       SET resulting_material_state_ref = repaired_state
     WHERE self_person_ref = receipt.self_person_ref
       AND operation_id = receipt.operation_id;
  END LOOP;
END;
$repair$
"""
    )


def _create_immutable_end() -> None:
    _sql(
        r"""
CREATE FUNCTION dante.end_self_session(
  requested_self_person_ref uuid,
  requested_operation_id text,
  requested_intent_fingerprint text,
  requested_session_ref uuid,
  requested_expected_material_state_ref uuid,
  requested_resulting_material_state_ref uuid
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
  existing_resulting_state uuid;
  current_state uuid;
  current_started_at timestamptz;
  current_start_precision text;
  current_ended_at timestamptz;
  recorded_at timestamptz := statement_timestamp();
  subject_ref uuid;
  affected integer;
BEGIN
  IF normalized_operation_id = '' OR char_length(normalized_operation_id) > 200 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_session_end_operation_operation_id',
      MESSAGE='Session operation id rejected';
  END IF;
  IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_session_end_operation_fingerprint',
      MESSAGE='Session operation fingerprint rejected';
  END IF;
  IF uuid_extract_version(requested_resulting_material_state_ref) IS DISTINCT FROM 7
     OR requested_resulting_material_state_ref = requested_expected_material_state_ref THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='session_end_resulting_state_invalid',
      MESSAGE='Session resulting timing state rejected';
  END IF;

  PERFORM pg_advisory_xact_lock(
    hashtextextended(
      requested_self_person_ref::text || ':end:' || normalized_operation_id, 0
    )
  );

  SELECT operation.intent_fingerprint,
         operation.session_ref,
         operation.resulting_material_state_ref
    INTO existing_fingerprint, existing_session_ref, existing_resulting_state
    FROM dante.session_end_operation AS operation
   WHERE operation.self_person_ref = requested_self_person_ref
     AND operation.operation_id = normalized_operation_id;
  IF FOUND THEN
    IF existing_fingerprint <> requested_intent_fingerprint
       OR existing_session_ref <> requested_session_ref THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        CONSTRAINT='session_operation_reused',
        MESSAGE='Session operation id reused with different intent';
    END IF;
    RETURN QUERY
    SELECT subject.session_ref,
           subject.subject_native_ref,
           existing_resulting_state,
           absolute_timing.started_at,
           absolute_timing.ended_at,
           true
      FROM dante.session_execution_subject AS subject
      JOIN dante.session_timing_absolute AS absolute_timing
        ON absolute_timing.material_state_ref = existing_resulting_state
     WHERE subject.session_ref = existing_session_ref;
    RETURN;
  END IF;

  SELECT subject.subject_native_ref INTO subject_ref
    FROM dante.session_execution_subject AS subject
   WHERE subject.session_ref = requested_session_ref;
  IF NOT FOUND OR NOT dante._session_subject_owned(
    requested_self_person_ref, subject_ref
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='session_subject_unavailable',
      MESSAGE='Session subject unavailable';
  END IF;

  PERFORM pg_advisory_xact_lock(hashtextextended(requested_session_ref::text, 0));

  SELECT timing.material_state_ref,
         absolute_timing.started_at,
         absolute_timing.start_precision_code,
         absolute_timing.ended_at
    INTO current_state, current_started_at, current_start_precision, current_ended_at
    FROM dante.session_timing_current_history AS timing
    JOIN dante.session_timing_absolute AS absolute_timing
      ON absolute_timing.material_state_ref = timing.material_state_ref
   WHERE timing.session_ref = requested_session_ref
     AND timing.current_until_at IS NULL
   FOR UPDATE OF timing, absolute_timing;

  IF current_state IS DISTINCT FROM requested_expected_material_state_ref
     OR current_ended_at IS NOT NULL
     OR recorded_at <= current_started_at THEN
    RAISE EXCEPTION USING ERRCODE='40001',
      CONSTRAINT='session_end_conflict',
      MESSAGE='Session end conflicts with current timing';
  END IF;

  INSERT INTO dante.material_state_address(
    material_state_ref, native_owner_ref, facet_code
  ) VALUES (
    requested_resulting_material_state_ref, requested_session_ref, 'session.timing'
  );
  INSERT INTO dante.session_timing_state(
    material_state_ref, session_ref, timing_form_code
  ) VALUES (
    requested_resulting_material_state_ref, requested_session_ref, 'absolute'
  );
  INSERT INTO dante.session_timing_absolute(
    material_state_ref, started_at, start_precision_code,
    ended_at, end_precision_code
  ) VALUES (
    requested_resulting_material_state_ref, current_started_at,
    current_start_precision, recorded_at, 'exact'
  );
  INSERT INTO dante.session_timing_pause(
    material_state_ref, paused_at, pause_precision_code,
    resumed_at, resume_precision_code
  )
  SELECT requested_resulting_material_state_ref,
         pause.paused_at, pause.pause_precision_code,
         pause.resumed_at, pause.resume_precision_code
    FROM dante.session_timing_pause AS pause
   WHERE pause.material_state_ref = current_state;

  UPDATE dante.native_current_material_state
     SET material_state_ref = requested_resulting_material_state_ref
   WHERE native_owner_ref = requested_session_ref
     AND facet_code = 'session.timing'
     AND material_state_ref = current_state;
  GET DIAGNOSTICS affected = ROW_COUNT;
  IF affected <> 1 THEN
    RAISE EXCEPTION USING ERRCODE='40001',
      CONSTRAINT='session_end_conflict',
      MESSAGE='Session end conflicts with current timing';
  END IF;

  UPDATE dante.session_timing_current_history
     SET current_until_at = recorded_at
   WHERE session_ref = requested_session_ref
     AND material_state_ref = current_state
     AND current_until_at IS NULL;
  GET DIAGNOSTICS affected = ROW_COUNT;
  IF affected <> 1 THEN
    RAISE EXCEPTION USING ERRCODE='40001',
      CONSTRAINT='session_end_conflict',
      MESSAGE='Session end conflicts with current timing';
  END IF;

  INSERT INTO dante.session_timing_current_history(
    session_ref, material_state_ref, current_from_at
  ) VALUES (
    requested_session_ref, requested_resulting_material_state_ref, recorded_at
  );

  INSERT INTO dante.session_end_operation(
    self_person_ref, operation_id, intent_fingerprint, session_ref,
    expected_material_state_ref, resulting_material_state_ref, created_at
  ) VALUES (
    requested_self_person_ref, normalized_operation_id, requested_intent_fingerprint,
    requested_session_ref, requested_expected_material_state_ref,
    requested_resulting_material_state_ref, recorded_at
  );

  RETURN QUERY
  SELECT requested_session_ref, subject_ref,
         requested_resulting_material_state_ref,
         current_started_at, recorded_at, false;
END;
$function$
"""
    )
    _sql(f"ALTER FUNCTION {_NEW_SIGNATURE} OWNER TO {_OWNER}")
    _sql(f"REVOKE ALL ON FUNCTION {_NEW_SIGNATURE} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}")
    _sql(f"GRANT EXECUTE ON FUNCTION {_NEW_SIGNATURE} TO {_RUNTIME}")


def upgrade() -> None:
    """Replace mutable END with immutable timing-state replacement semantics."""
    op.add_column(
        "session_end_operation",
        sa.Column("resulting_material_state_ref", sa.Uuid(), nullable=True),
        schema="dante",
    )
    _repair_existing_end_receipts()
    op.alter_column(
        "session_end_operation",
        "resulting_material_state_ref",
        existing_type=sa.Uuid(),
        nullable=False,
        schema="dante",
    )
    op.create_foreign_key(
        "fk_session_end_operation_resulting_state_address",
        "session_end_operation",
        "material_state_address",
        ["resulting_material_state_ref"],
        ["material_state_ref"],
        source_schema="dante",
        referent_schema="dante",
        onupdate="NO ACTION",
        ondelete="NO ACTION",
    )

    _create_immutable_end()
    _sql(f"REVOKE ALL ON FUNCTION {_OLD_SIGNATURE} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}")
    _sql(f"DROP FUNCTION {_OLD_SIGNATURE}")


def downgrade() -> None:
    """Refuse to restore the known-invalid mutable Session END contract."""
    raise RuntimeError(
        "B08-A _60 is forward-only: downgrading would restore in-place Session timing mutation"
    )
