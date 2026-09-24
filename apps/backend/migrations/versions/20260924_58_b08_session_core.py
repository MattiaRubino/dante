"""B08-A: self-scoped Session start, read, and end for Activity and Occurrence.

Revision ID: 20260924_58
Revises: 20260923_57

Session identity and timing stay the CP6 substrate. This revision adds only the
typed execution subject and the bounded start/read/end capabilities.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260924_58"
down_revision: str | None = "20260923_57"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"


def _sql(statement: str) -> None:
    op.execute(sa.text(statement))


def upgrade() -> None:
    """Add Session subject binding and start/read/end capabilities."""
    op.create_table(
        "session_execution_subject",
        sa.Column("session_ref", sa.Uuid(), nullable=False),
        sa.Column("subject_native_ref", sa.Uuid(), nullable=False),
        sa.CheckConstraint(
            "uuid_extract_version(session_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_session_execution_subject_session_uuidv7"),
        ),
        sa.CheckConstraint(
            "uuid_extract_version(subject_native_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_session_execution_subject_subject_uuidv7"),
        ),
        sa.ForeignKeyConstraint(
            ["session_ref"],
            [f"{_SCHEMA}.session.session_ref"],
            name=op.f("fk_session_execution_subject_session_ref_session"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["subject_native_ref"],
            [f"{_SCHEMA}.native_address.native_ref"],
            name=op.f("fk_session_execution_subject_subject_native_ref_native_address"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.PrimaryKeyConstraint("session_ref", name=op.f("pk_session_execution_subject")),
        schema=_SCHEMA,
    )
    op.create_table(
        "session_start_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("session_ref", sa.Uuid(), nullable=False),
        sa.Column("subject_native_ref", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f("ck_session_start_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_session_start_operation_fingerprint"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name=op.f("fk_session_start_operation_self_person_ref_person"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["session_ref"],
            [f"{_SCHEMA}.session.session_ref"],
            name=op.f("fk_session_start_operation_session_ref_session"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            name=op.f("pk_session_start_operation"),
        ),
        sa.UniqueConstraint(
            "session_ref",
            name=op.f("uq_session_start_operation_session_ref"),
        ),
        schema=_SCHEMA,
    )
    op.create_table(
        "session_end_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("session_ref", sa.Uuid(), nullable=False),
        sa.Column("expected_material_state_ref", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f("ck_session_end_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_session_end_operation_fingerprint"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name=op.f("fk_session_end_operation_self_person_ref_person"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["session_ref"],
            [f"{_SCHEMA}.session.session_ref"],
            name=op.f("fk_session_end_operation_session_ref_session"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            name=op.f("pk_session_end_operation"),
        ),
        sa.UniqueConstraint(
            "session_ref",
            name=op.f("uq_session_end_operation_session_ref"),
        ),
        schema=_SCHEMA,
    )
    _sql(
        r"""
CREATE FUNCTION dante.enforce_session_execution_subject()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
VOLATILE
PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
DECLARE
  family text;
BEGIN
  SELECT address.owner_family INTO family
    FROM dante.native_address AS address
   WHERE address.native_ref = NEW.subject_native_ref;
  IF family IS NULL OR family NOT IN ('activity', 'occurrence') THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_session_execution_subject_family',
      MESSAGE='Session execution subject must be an Activity or Occurrence';
  END IF;
  RETURN NEW;
END;
$function$
"""
    )
    _sql(
        """
CREATE CONSTRAINT TRIGGER ctrg_session_execution_subject_family
AFTER INSERT OR UPDATE ON dante.session_execution_subject
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE FUNCTION dante.enforce_session_execution_subject()
"""
    )
    _sql(
        r"""
CREATE FUNCTION dante._session_subject_owned(
  requested_self_person_ref uuid,
  requested_subject_native_ref uuid
) RETURNS boolean
LANGUAGE sql
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT EXISTS (
    SELECT 1 FROM dante.activity_intention AS intention
     WHERE intention.activity_ref = requested_subject_native_ref
       AND intention.self_person_ref = requested_self_person_ref
  ) OR EXISTS (
    SELECT 1 FROM dante.occurrence_generation AS generation
     WHERE generation.occurrence_ref = requested_subject_native_ref
       AND (
         EXISTS (
           SELECT 1 FROM dante.routine_intention AS routine
            WHERE routine.routine_ref = generation.source_native_ref
              AND routine.self_person_ref = requested_self_person_ref
         ) OR EXISTS (
           SELECT 1 FROM dante.event_expectation AS event
            WHERE event.event_ref = generation.source_native_ref
              AND event.self_person_ref = requested_self_person_ref
         )
       )
  );
$function$
"""
    )
    _sql(
        r"""
CREATE FUNCTION dante.start_self_session(
  requested_self_person_ref uuid,
  requested_operation_id text,
  requested_intent_fingerprint text,
  requested_session_ref uuid,
  requested_material_state_ref uuid,
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
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM dante.person WHERE person_ref = requested_self_person_ref
  ) OR NOT dante._session_subject_owned(
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
    _sql(
        r"""
CREATE FUNCTION dante.end_self_session(
  requested_self_person_ref uuid,
  requested_operation_id text,
  requested_intent_fingerprint text,
  requested_session_ref uuid,
  requested_expected_material_state_ref uuid
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
  current_state uuid;
  current_ended_at timestamptz;
  recorded_at timestamptz := statement_timestamp();
  subject_ref uuid;
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

  PERFORM pg_advisory_xact_lock(
    hashtextextended(
      requested_self_person_ref::text || ':end:' || normalized_operation_id, 0
    )
  );

  SELECT operation.intent_fingerprint, operation.session_ref
    INTO existing_fingerprint, existing_session_ref
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

  SELECT timing.material_state_ref, absolute_timing.ended_at
    INTO current_state, current_ended_at
    FROM dante.session_timing_current_history AS timing
    JOIN dante.session_timing_absolute AS absolute_timing
      ON absolute_timing.material_state_ref = timing.material_state_ref
   WHERE timing.session_ref = requested_session_ref
     AND timing.current_until_at IS NULL
   FOR UPDATE OF absolute_timing;
  IF current_state IS DISTINCT FROM requested_expected_material_state_ref
     OR current_ended_at IS NOT NULL THEN
    RAISE EXCEPTION USING ERRCODE='40001',
      CONSTRAINT='session_end_conflict',
      MESSAGE='Session end conflicts with current timing';
  END IF;

  UPDATE dante.session_timing_absolute
     SET ended_at = recorded_at,
         end_precision_code = 'exact'
   WHERE material_state_ref = current_state
     AND ended_at IS NULL;
  INSERT INTO dante.session_end_operation(
    self_person_ref, operation_id, intent_fingerprint, session_ref,
    expected_material_state_ref, created_at
  ) VALUES (
    requested_self_person_ref, normalized_operation_id, requested_intent_fingerprint,
    requested_session_ref, requested_expected_material_state_ref, recorded_at
  );

  RETURN QUERY
  SELECT requested_session_ref, subject_ref, current_state,
         absolute_timing.started_at, recorded_at, false
    FROM dante.session_timing_absolute AS absolute_timing
   WHERE absolute_timing.material_state_ref = current_state;
END;
$function$
"""
    )
    _sql(
        r"""
CREATE FUNCTION dante.list_self_subject_sessions(
  requested_self_person_ref uuid,
  requested_subject_native_ref uuid
) RETURNS TABLE(
  session_ref uuid,
  subject_native_ref uuid,
  timing_material_state_ref uuid,
  started_at timestamptz,
  ended_at timestamptz
)
LANGUAGE plpgsql
SECURITY DEFINER
STABLE
PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
BEGIN
  IF NOT dante._session_subject_owned(
    requested_self_person_ref, requested_subject_native_ref
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='session_subject_unavailable',
      MESSAGE='Session subject unavailable';
  END IF;
  RETURN QUERY
  SELECT subject.session_ref,
         subject.subject_native_ref,
         timing.material_state_ref,
         absolute_timing.started_at,
         absolute_timing.ended_at
    FROM dante.session_execution_subject AS subject
    JOIN dante.session_timing_current_history AS timing
      ON timing.session_ref = subject.session_ref
     AND timing.current_until_at IS NULL
    JOIN dante.session_timing_absolute AS absolute_timing
      ON absolute_timing.material_state_ref = timing.material_state_ref
   WHERE subject.subject_native_ref = requested_subject_native_ref
   ORDER BY absolute_timing.started_at, subject.session_ref;
END;
$function$
"""
    )
    _sql(
        r"""
CREATE FUNCTION dante.get_self_session(
  requested_self_person_ref uuid,
  requested_session_ref uuid
) RETURNS TABLE(
  session_ref uuid,
  subject_native_ref uuid,
  timing_material_state_ref uuid,
  started_at timestamptz,
  ended_at timestamptz
)
LANGUAGE plpgsql
SECURITY DEFINER
STABLE
PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
DECLARE
  subject_ref uuid;
BEGIN
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
  RETURN QUERY
  SELECT subject.session_ref,
         subject.subject_native_ref,
         timing.material_state_ref,
         absolute_timing.started_at,
         absolute_timing.ended_at
    FROM dante.session_execution_subject AS subject
    JOIN dante.session_timing_current_history AS timing
      ON timing.session_ref = subject.session_ref
     AND timing.current_until_at IS NULL
    JOIN dante.session_timing_absolute AS absolute_timing
      ON absolute_timing.material_state_ref = timing.material_state_ref
   WHERE subject.session_ref = requested_session_ref;
END;
$function$
"""
    )
    for signature in (
        "dante.enforce_session_execution_subject()",
        "dante._session_subject_owned(uuid,uuid)",
        "dante.start_self_session(uuid,text,text,uuid,uuid,uuid)",
        "dante.end_self_session(uuid,text,text,uuid,uuid)",
        "dante.list_self_subject_sessions(uuid,uuid)",
        "dante.get_self_session(uuid,uuid)",
    ):
        _sql(f"ALTER FUNCTION {signature} OWNER TO {_OWNER}")
        _sql(f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}")
    for signature in (
        "dante.start_self_session(uuid,text,text,uuid,uuid,uuid)",
        "dante.end_self_session(uuid,text,text,uuid,uuid)",
        "dante.list_self_subject_sessions(uuid,uuid)",
        "dante.get_self_session(uuid,uuid)",
    ):
        _sql(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}")
    for table in (
        "session_execution_subject",
        "session_start_operation",
        "session_end_operation",
    ):
        _sql(f"REVOKE ALL ON TABLE dante.{table} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}")


def downgrade() -> None:
    """Refuse rollback once a Session subject exists."""
    _sql(
        r"""
DO $block$
BEGIN
  IF EXISTS (SELECT 1 FROM dante.session_execution_subject) THEN
    RAISE EXCEPTION USING ERRCODE='55000', MESSAGE='B08-A downgrade refused';
  END IF;
END;
$block$
"""
    )
    for signature in (
        "dante.get_self_session(uuid,uuid)",
        "dante.list_self_subject_sessions(uuid,uuid)",
        "dante.end_self_session(uuid,text,text,uuid,uuid)",
        "dante.start_self_session(uuid,text,text,uuid,uuid,uuid)",
        "dante._session_subject_owned(uuid,uuid)",
    ):
        _sql(f"DROP FUNCTION IF EXISTS {signature}")
    _sql("DROP TRIGGER IF EXISTS ctrg_session_execution_subject_family ON dante.session_execution_subject")
    _sql("DROP FUNCTION IF EXISTS dante.enforce_session_execution_subject()")
    op.drop_table("session_end_operation", schema=_SCHEMA)
    op.drop_table("session_start_operation", schema=_SCHEMA)
    op.drop_table("session_execution_subject", schema=_SCHEMA)
