"""B09-B: guarded Responsibility and expected Participation authoring.

Revision ID: 20260925_67
Revises: 20260925_66

The B09-A relation tables stay default-deny. Every mutation goes through a
bounded SECURITY DEFINER capability that checks self ownership of the subject,
admissibility of the referenced Person, and the caller's expected current
holder. `_self_referenceable_person` is the single seam a later Person-referent
slice widens; today only the caller's own self Person is referenceable.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260925_67"
down_revision: str | None = "20260925_66"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"

_RESPONSIBILITY_SIGNATURE = "uuid,text,text,uuid,uuid,uuid"
_PARTICIPATION_SIGNATURE = "uuid,text,text,uuid,uuid,text,text"

_CAPABILITIES = (
    ("set_self_activity_responsibility", _RESPONSIBILITY_SIGNATURE),
    ("set_self_event_responsibility", _RESPONSIBILITY_SIGNATURE),
    ("set_self_event_expected_participation", _PARTICIPATION_SIGNATURE),
    ("get_self_activity_responsibility", "uuid,uuid"),
    ("get_self_event_responsibility", "uuid,uuid"),
    ("list_self_event_expected_participation", "uuid,uuid"),
)


def _sql(statement: str) -> None:
    op.execute(sa.text(statement))


def _responsibility_operation_table(subject: str) -> None:
    table = f"{subject}_responsibility_operation"
    op.create_table(
        table,
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column(f"{subject}_ref", sa.Uuid(), nullable=False),
        sa.Column("responsible_person_ref", sa.Uuid(), nullable=True),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("self_person_ref", "operation_id", name=op.f(f"pk_{table}")),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name=f"fk_{subject}_responsibility_op_self_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            [f"{subject}_ref"],
            [f"{_SCHEMA}.{subject}.{subject}_ref"],
            name=f"fk_{subject}_responsibility_op_subject",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["responsible_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name=f"fk_{subject}_responsibility_op_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f(f"ck_{table}_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f(f"ck_{table}_fingerprint"),
        ),
        schema=_SCHEMA,
    )


def _participation_operation_table() -> None:
    table = "event_expected_participation_operation"
    op.create_table(
        table,
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("event_ref", sa.Uuid(), nullable=False),
        sa.Column("participant_person_ref", sa.Uuid(), nullable=False),
        sa.Column("requirement_code", sa.Text(), nullable=True),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("self_person_ref", "operation_id", name=op.f(f"pk_{table}")),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name="fk_event_expected_participation_op_self_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["event_ref"],
            [f"{_SCHEMA}.event.event_ref"],
            name="fk_event_expected_participation_op_event",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["participant_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name="fk_event_expected_participation_op_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f(f"ck_{table}_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f(f"ck_{table}_fingerprint"),
        ),
        sa.CheckConstraint(
            "requirement_code IS NULL OR requirement_code IN ('required','optional')",
            name=op.f(f"ck_{table}_requirement"),
        ),
        schema=_SCHEMA,
    )


def _referenceable_person() -> None:
    """One seam for Person admissibility; a later referent slice widens only this."""
    _sql(
        r"""
CREATE FUNCTION dante._self_referenceable_person(
  requested_self_person_ref uuid,
  requested_person_ref uuid
) RETURNS boolean
LANGUAGE sql
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT requested_person_ref IS NOT NULL
     AND requested_person_ref = requested_self_person_ref
     AND EXISTS (
       SELECT 1 FROM dante.person WHERE person_ref = requested_self_person_ref
     );
$function$
"""
    )


def _responsibility_capability(subject: str, descriptor: str) -> str:
    table = f"{subject}_responsibility"
    operation = f"{table}_operation"
    return rf"""
CREATE FUNCTION dante.set_self_{table}(
  requested_self_person_ref uuid,
  requested_operation_id text,
  requested_intent_fingerprint text,
  requested_{subject}_ref uuid,
  requested_responsible_person_ref uuid,
  requested_expected_responsible_person_ref uuid
) RETURNS TABLE(
  subject_native_ref uuid,
  responsible_person_ref uuid,
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
  previous_subject_ref uuid;
  previous_person_ref uuid;
  previous_accepted_at timestamptz;
  current_person_ref uuid;
  current_found boolean;
  recorded_at timestamptz := statement_timestamp();
BEGIN
  IF normalized_operation_id = '' OR char_length(normalized_operation_id) > 200 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_{operation}_operation_id',
      MESSAGE='Responsibility operation id rejected';
  END IF;
  IF requested_intent_fingerprint !~ '^[0-9a-f]{{64}}$' THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_{operation}_fingerprint',
      MESSAGE='Responsibility operation fingerprint rejected';
  END IF;

  PERFORM pg_advisory_xact_lock(
    hashtextextended(
      requested_self_person_ref::text || ':{table}:' || normalized_operation_id, 0
    )
  );

  SELECT receipt.intent_fingerprint, receipt.{subject}_ref,
         receipt.responsible_person_ref, receipt.accepted_at
    INTO previous_fingerprint, previous_subject_ref,
         previous_person_ref, previous_accepted_at
    FROM dante.{operation} AS receipt
   WHERE receipt.self_person_ref = requested_self_person_ref
     AND receipt.operation_id = normalized_operation_id;
  IF FOUND THEN
    IF previous_fingerprint <> requested_intent_fingerprint
       OR previous_subject_ref <> requested_{subject}_ref THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        CONSTRAINT='responsibility_operation_reused',
        MESSAGE='Responsibility operation id reused with different intent';
    END IF;
    RETURN QUERY
    SELECT previous_subject_ref, previous_person_ref, previous_accepted_at, true;
    RETURN;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM dante.{descriptor}
     WHERE {subject}_ref = requested_{subject}_ref
       AND self_person_ref = requested_self_person_ref
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='responsibility_subject_unavailable',
      MESSAGE='Responsibility subject is unavailable in current self scope';
  END IF;

  IF requested_responsible_person_ref IS NOT NULL
     AND NOT dante._self_referenceable_person(
       requested_self_person_ref, requested_responsible_person_ref
     ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='responsibility_person_unavailable',
      MESSAGE='Responsible Person is not referenceable by this actor';
  END IF;

  SELECT relation.responsible_person_ref, true
    INTO current_person_ref, current_found
    FROM dante.{table} AS relation
   WHERE relation.{subject}_ref = requested_{subject}_ref
   FOR UPDATE;
  IF NOT FOUND THEN
    current_person_ref := NULL;
    current_found := false;
  END IF;

  IF current_person_ref IS DISTINCT FROM requested_expected_responsible_person_ref THEN
    RAISE EXCEPTION USING ERRCODE='40001',
      CONSTRAINT='responsibility_expected_holder_conflict',
      MESSAGE='Responsibility holder changed since it was read';
  END IF;
  IF current_person_ref IS NOT DISTINCT FROM requested_responsible_person_ref THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='responsibility_no_change',
      MESSAGE='Responsibility already matches the requested holder';
  END IF;

  IF requested_responsible_person_ref IS NULL THEN
    DELETE FROM dante.{table} WHERE {subject}_ref = requested_{subject}_ref;
  ELSIF current_found THEN
    UPDATE dante.{table}
       SET responsible_person_ref = requested_responsible_person_ref,
           established_at = recorded_at
     WHERE {subject}_ref = requested_{subject}_ref;
  ELSE
    INSERT INTO dante.{table}(
      {subject}_ref, responsible_person_ref, established_at
    ) VALUES (
      requested_{subject}_ref, requested_responsible_person_ref, recorded_at
    );
  END IF;

  INSERT INTO dante.{operation}(
    self_person_ref, operation_id, intent_fingerprint, {subject}_ref,
    responsible_person_ref, accepted_at
  ) VALUES (
    requested_self_person_ref, normalized_operation_id, requested_intent_fingerprint,
    requested_{subject}_ref, requested_responsible_person_ref, recorded_at
  );

  RETURN QUERY
  SELECT requested_{subject}_ref, requested_responsible_person_ref, recorded_at, false;
END;
$function$
"""


def _participation_capability() -> str:
    return r"""
CREATE FUNCTION dante.set_self_event_expected_participation(
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
    SELECT 1 FROM dante.event_expectation
     WHERE event_ref = requested_event_ref
       AND self_person_ref = requested_self_person_ref
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
    DELETE FROM dante.event_expected_participation
     WHERE event_ref = requested_event_ref
       AND participant_person_ref = requested_participant_person_ref;
  ELSIF current_found THEN
    UPDATE dante.event_expected_participation
       SET requirement_code = requested_requirement_code,
           established_at = recorded_at
     WHERE event_ref = requested_event_ref
       AND participant_person_ref = requested_participant_person_ref;
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


def _responsibility_read(subject: str, descriptor: str) -> str:
    table = f"{subject}_responsibility"
    return rf"""
CREATE FUNCTION dante.get_self_{table}(
  requested_self_person_ref uuid,
  requested_{subject}_ref uuid
) RETURNS TABLE(
  subject_native_ref uuid,
  responsible_person_ref uuid,
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
    SELECT 1 FROM dante.{descriptor}
     WHERE {subject}_ref = requested_{subject}_ref
       AND self_person_ref = requested_self_person_ref
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='responsibility_subject_unavailable',
      MESSAGE='Responsibility subject is unavailable in current self scope';
  END IF;
  RETURN QUERY
  SELECT relation.{subject}_ref,
         relation.responsible_person_ref,
         relation.established_at
    FROM dante.{table} AS relation
   WHERE relation.{subject}_ref = requested_{subject}_ref;
END;
$function$
"""


def _participation_read() -> str:
    return r"""
CREATE FUNCTION dante.list_self_event_expected_participation(
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
    SELECT 1 FROM dante.event_expectation
     WHERE event_ref = requested_event_ref
       AND self_person_ref = requested_self_person_ref
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


def upgrade() -> None:
    """Add bounded authoring over the B09-A relations; tables stay default-deny."""
    _responsibility_operation_table("activity")
    _responsibility_operation_table("event")
    _participation_operation_table()

    _referenceable_person()
    _sql(_responsibility_capability("activity", "activity_intention"))
    _sql(_responsibility_capability("event", "event_expectation"))
    _sql(_participation_capability())
    _sql(_responsibility_read("activity", "activity_intention"))
    _sql(_responsibility_read("event", "event_expectation"))
    _sql(_participation_read())

    helper = f"{_SCHEMA}._self_referenceable_person(uuid,uuid)"
    _sql(f"ALTER FUNCTION {helper} OWNER TO {_OWNER}")
    _sql(f"REVOKE ALL ON FUNCTION {helper} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}")
    for name, signature in _CAPABILITIES:
        qualified = f"{_SCHEMA}.{name}({signature})"
        _sql(f"ALTER FUNCTION {qualified} OWNER TO {_OWNER}")
        _sql(f"REVOKE ALL ON FUNCTION {qualified} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}")
        _sql(f"GRANT EXECUTE ON FUNCTION {qualified} TO {_RUNTIME}")

    for table in (
        "activity_responsibility_operation",
        "event_responsibility_operation",
        "event_expected_participation_operation",
    ):
        _sql(f"REVOKE ALL ON TABLE {_SCHEMA}.{table} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}")


def downgrade() -> None:
    """Refuse rollback once authored Responsibility or Participation exists."""
    _sql(
        r"""
DO $block$
BEGIN
  IF EXISTS (SELECT 1 FROM dante.activity_responsibility_operation)
     OR EXISTS (SELECT 1 FROM dante.event_responsibility_operation)
     OR EXISTS (SELECT 1 FROM dante.event_expected_participation_operation) THEN
    RAISE EXCEPTION USING ERRCODE='55000', MESSAGE='B09-B downgrade refused';
  END IF;
END;
$block$
"""
    )
    for name, signature in _CAPABILITIES:
        _sql(f"DROP FUNCTION IF EXISTS {_SCHEMA}.{name}({signature})")
    _sql(f"DROP FUNCTION IF EXISTS {_SCHEMA}._self_referenceable_person(uuid,uuid)")
    op.drop_table("event_expected_participation_operation", schema=_SCHEMA)
    op.drop_table("event_responsibility_operation", schema=_SCHEMA)
    op.drop_table("activity_responsibility_operation", schema=_SCHEMA)
