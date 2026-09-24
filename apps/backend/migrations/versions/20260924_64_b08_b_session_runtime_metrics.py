"""Complete B08-B Session runtime metrics and paused-END guard.

Revision ID: 20260924_64
Revises: 20260924_63
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260924_64"
down_revision: str | None = "20260924_63"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"
_END_SIGNATURE = "dante.end_self_session(uuid,text,text,uuid,uuid,uuid)"
_METRICS_SIGNATURE = "dante.get_self_session_runtime_metrics(uuid,uuid,uuid)"


def _sql(statement: str) -> None:
    op.execute(sa.text(statement))


def upgrade() -> None:
    """Expose fact-derived durations and require resume before END."""
    _sql(
        r"""
CREATE OR REPLACE FUNCTION dante.end_self_session(
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
     OR recorded_at <= current_started_at
     OR EXISTS (
       SELECT 1
         FROM dante.session_timing_pause AS pause
        WHERE pause.material_state_ref = current_state
          AND pause.resumed_at IS NULL
     ) THEN
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

  UPDATE dante.session_timing_current_history AS history
     SET current_until_at = recorded_at
   WHERE history.session_ref = requested_session_ref
     AND history.material_state_ref = current_state
     AND history.current_until_at IS NULL;
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
$function$;

CREATE FUNCTION dante.get_self_session_runtime_metrics(
  requested_self_person_ref uuid,
  requested_session_ref uuid,
  requested_material_state_ref uuid
) RETURNS TABLE(
  paused boolean,
  evaluated_at timestamptz,
  elapsed_seconds numeric,
  paused_seconds numeric,
  active_seconds numeric
)
LANGUAGE sql
SECURITY DEFINER
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
WITH selected AS (
  SELECT absolute_timing.started_at,
         absolute_timing.ended_at,
         history.current_until_at,
         history.material_state_ref,
         COALESCE(
           absolute_timing.ended_at,
           history.current_until_at,
           statement_timestamp()
         ) AS effective_end,
         statement_timestamp() AS statement_at
    FROM dante.session_execution_subject AS subject
    JOIN dante.session_timing_state AS timing_state
      ON timing_state.session_ref = subject.session_ref
    JOIN dante.session_timing_absolute AS absolute_timing
      ON absolute_timing.material_state_ref = timing_state.material_state_ref
    JOIN dante.session_timing_current_history AS history
      ON history.session_ref = subject.session_ref
     AND history.material_state_ref = timing_state.material_state_ref
   WHERE subject.session_ref = requested_session_ref
     AND timing_state.material_state_ref = requested_material_state_ref
     AND dante._session_subject_owned(
       requested_self_person_ref, subject.subject_native_ref
     )
), measured AS (
  SELECT selected.*,
         GREATEST(
           EXTRACT(EPOCH FROM (selected.effective_end - selected.started_at)),
           0::numeric
         ) AS elapsed_value,
         COALESCE(
           (
             SELECT SUM(
               GREATEST(
                 EXTRACT(
                   EPOCH FROM (
                     LEAST(
                       COALESCE(pause.resumed_at, selected.effective_end),
                       selected.effective_end
                     ) - pause.paused_at
                   )
                 ),
                 0::numeric
               )
             )
               FROM dante.session_timing_pause AS pause
              WHERE pause.material_state_ref = selected.material_state_ref
                AND pause.paused_at < selected.effective_end
           ),
           0::numeric
         ) AS paused_value
    FROM selected
)
SELECT measured.ended_at IS NULL
       AND measured.current_until_at IS NULL
       AND EXISTS (
         SELECT 1
           FROM dante.session_timing_pause AS open_pause
          WHERE open_pause.material_state_ref = measured.material_state_ref
            AND open_pause.resumed_at IS NULL
       ) AS paused,
       CASE
         WHEN measured.ended_at IS NOT NULL THEN measured.ended_at
         WHEN measured.current_until_at IS NOT NULL THEN measured.current_until_at
         ELSE measured.statement_at
       END AS evaluated_at,
       measured.elapsed_value AS elapsed_seconds,
       LEAST(measured.paused_value, measured.elapsed_value) AS paused_seconds,
       GREATEST(
         measured.elapsed_value - LEAST(measured.paused_value, measured.elapsed_value),
         0::numeric
       ) AS active_seconds
  FROM measured;
$function$;
"""
    )

    _sql(f"ALTER FUNCTION {_END_SIGNATURE} OWNER TO {_OWNER}")
    _sql(
        f"REVOKE ALL ON FUNCTION {_END_SIGNATURE} "
        f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
    )
    _sql(f"GRANT EXECUTE ON FUNCTION {_END_SIGNATURE} TO {_RUNTIME}")

    _sql(f"ALTER FUNCTION {_METRICS_SIGNATURE} OWNER TO {_OWNER}")
    _sql(
        f"REVOKE ALL ON FUNCTION {_METRICS_SIGNATURE} "
        f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
    )
    _sql(f"GRANT EXECUTE ON FUNCTION {_METRICS_SIGNATURE} TO {_RUNTIME}")


def downgrade() -> None:
    raise RuntimeError(
        "B08-B _64 is forward-only: Session runtime metrics and transition guards are canonical"
    )
