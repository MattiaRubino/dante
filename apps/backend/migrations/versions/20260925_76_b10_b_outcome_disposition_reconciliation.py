"""B10-B: reconcile Outcome persistence to the approved disposition model.

Revision ID: 20260925_76
Revises: 20260925_75

Revision 75 was published before the already-prepared B10-B SQLAlchemy
mapping checkpoint was visible in the branch history. Its temporary
(vocabulary,result) shape is therefore repaired forward-only rather than
rewritten.

No public HTTP/application capability can write revision-75 Outcome rows. This
migration nevertheless fails closed if any temporary Outcome data exists,
then rebuilds the empty substrate to the approved model:

* exactly one stable Outcome owner per Actual;
* one immutable contextual disposition state per correction;
* every disposition state pinned to the exact Actual realization MaterialState
  it describes;
* explicit accepted-current history;
* idempotency receipts distinct from Outcome identity.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260925_76"
down_revision: str | None = "20260925_75"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"

_WRITE_SIGNATURE = (
    "dante.record_self_actual_outcome("
    "uuid,text,text,uuid,uuid,uuid,uuid,uuid,text)"
)
_READ_SIGNATURE = "dante.get_self_actual_outcome(uuid,uuid)"
_HISTORY_SIGNATURE = "dante.list_self_outcome_history(uuid,uuid)"
_HELPER_SIGNATURE = "dante._outcome_actual_owned(uuid,uuid)"


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def upgrade() -> None:
    # Revision 75 had no application/API caller. Refuse to reinterpret data if
    # anything nevertheless reached that transient persistence shape.
    _sql(
        r"""
DO $guard$
BEGIN
  IF EXISTS (SELECT 1 FROM dante.outcome LIMIT 1)
     OR EXISTS (SELECT 1 FROM dante.outcome_result_state LIMIT 1)
     OR EXISTS (SELECT 1 FROM dante.outcome_result_current_history LIMIT 1)
     OR EXISTS (SELECT 1 FROM dante.outcome_result_operation LIMIT 1)
     OR EXISTS (
       SELECT 1
         FROM dante.scoped_address
        WHERE scoped_family='outcome'
        LIMIT 1
     )
     OR EXISTS (
       SELECT 1
         FROM dante.material_state_address
        WHERE facet_code='outcome.result'
        LIMIT 1
     ) THEN
    RAISE EXCEPTION
      'B10-B revision 75 temporary Outcome rows exist; refusing automatic semantic reinterpretation';
  END IF;
END;
$guard$;
"""
    )

    # Remove only the public/private routines introduced by revision 75.
    _sql(
        "DROP FUNCTION dante.record_self_actual_outcome("
        "uuid,text,text,uuid,text,uuid,uuid,uuid,text,text)"
    )
    _sql("DROP FUNCTION dante.get_self_actual_outcome(uuid,uuid,text)")
    _sql("DROP FUNCTION dante.list_self_outcome_history(uuid,uuid)")
    _sql("DROP FUNCTION dante._outcome_actual_owned(uuid,uuid)")

    # No rows are allowed above, so replacing the temporary schema is safe and
    # preserves the forward-only Alembic history.
    op.drop_table("outcome_result_operation", schema=_SCHEMA)
    op.drop_table("outcome_result_current_history", schema=_SCHEMA)
    op.drop_table("outcome_result_state", schema=_SCHEMA)
    op.drop_table("outcome", schema=_SCHEMA)

    op.drop_constraint(
        op.f("ck_material_state_address_facet_code"),
        "material_state_address",
        schema=_SCHEMA,
        type_="check",
    )
    op.create_check_constraint(
        op.f("ck_material_state_address_facet_code"),
        "material_state_address",
        "facet_code IN ("
        "'schedule.placement','schedule.movement_policy','actual.realization',"
        "'session.timing','routine.recurrence','event.recurrence',"
        "'temporal_constraint.rule','outcome.disposition')",
        schema=_SCHEMA,
    )

    op.drop_constraint(
        op.f("ck_scoped_current_material_state_facet_code"),
        "scoped_current_material_state",
        schema=_SCHEMA,
        type_="check",
    )
    op.create_check_constraint(
        op.f("ck_scoped_current_material_state_facet_code"),
        "scoped_current_material_state",
        "facet_code IN ("
        "'schedule.placement','actual.realization','temporal_constraint.rule',"
        "'outcome.disposition')",
        schema=_SCHEMA,
    )

    op.create_table(
        "outcome",
        sa.Column("outcome_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("actual_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("outcome_ref", name=op.f("pk_outcome")),
        sa.CheckConstraint(
            "uuid_extract_version(outcome_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_outcome_uuidv7"),
        ),
        sa.UniqueConstraint(
            "actual_ref",
            name=op.f("uq_outcome_actual_ref"),
        ),
        sa.UniqueConstraint(
            "outcome_ref",
            "actual_ref",
            name=op.f("uq_outcome_ref_actual_ref"),
        ),
        sa.ForeignKeyConstraint(
            ["actual_ref"],
            [f"{_SCHEMA}.actual.actual_ref"],
            name=op.f("fk_outcome_actual_ref_actual"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        schema=_SCHEMA,
    )

    op.create_table(
        "outcome_disposition_state",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("outcome_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "actual_realization_material_state_ref",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column("disposition_code", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_outcome_disposition_state"),
        ),
        sa.UniqueConstraint(
            "outcome_ref",
            "material_state_ref",
            name=op.f("uq_outcome_disposition_state_outcome_material"),
        ),
        sa.CheckConstraint(
            "disposition_code=btrim(disposition_code) AND disposition_code<>'' "
            "AND char_length(disposition_code)<=120 "
            "AND disposition_code ~ '^[a-z0-9][a-z0-9._:-]*$'",
            name=op.f("ck_outcome_disposition_state_code"),
        ),
        sa.ForeignKeyConstraint(
            ["material_state_ref"],
            [f"{_SCHEMA}.material_state_address.material_state_ref"],
            name=op.f("fk_outcome_disposition_state_state_address"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["outcome_ref"],
            [f"{_SCHEMA}.outcome.outcome_ref"],
            name=op.f("fk_outcome_disposition_state_outcome_ref_outcome"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["actual_realization_material_state_ref"],
            [f"{_SCHEMA}.actual_realization_state.material_state_ref"],
            name=op.f("fk_outcome_disposition_state_actual_realization"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_outcome_disposition_state_outcome_ref",
        "outcome_disposition_state",
        ["outcome_ref"],
        unique=False,
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_outcome_disposition_state_actual_realization",
        "outcome_disposition_state",
        ["actual_realization_material_state_ref"],
        unique=False,
        schema=_SCHEMA,
    )

    op.create_table(
        "outcome_disposition_current_history",
        sa.Column("outcome_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("current_from_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_until_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "outcome_ref",
            "current_from_at",
            name=op.f("pk_outcome_disposition_current_history"),
        ),
        sa.CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at>current_from_at))",
            name=op.f("ck_outcome_disposition_current_history_interval"),
        ),
        sa.ForeignKeyConstraint(
            ["outcome_ref", "material_state_ref"],
            [
                f"{_SCHEMA}.outcome_disposition_state.outcome_ref",
                f"{_SCHEMA}.outcome_disposition_state.material_state_ref",
            ],
            name=op.f("fk_outcome_disposition_current_history_state"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ux_outcome_disposition_current_history_open",
        "outcome_disposition_current_history",
        ["outcome_ref"],
        unique=True,
        schema=_SCHEMA,
        postgresql_where=sa.text("current_until_at IS NULL"),
    )
    op.create_index(
        "ix_outcome_disposition_current_history_material_state_ref",
        "outcome_disposition_current_history",
        ["material_state_ref"],
        unique=False,
        schema=_SCHEMA,
    )

    op.create_table(
        "outcome_disposition_operation",
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("actual_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("outcome_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "actual_realization_material_state_ref",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "expected_material_state_ref",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
        sa.Column(
            "resulting_material_state_ref",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            name=op.f("pk_outcome_disposition_operation"),
        ),
        sa.UniqueConstraint(
            "resulting_material_state_ref",
            name=op.f("uq_outcome_disposition_operation_resulting_state"),
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f("ck_outcome_disposition_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_outcome_disposition_operation_fingerprint"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name=op.f("fk_outcome_disposition_operation_self_person"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["outcome_ref", "actual_ref"],
            [f"{_SCHEMA}.outcome.outcome_ref", f"{_SCHEMA}.outcome.actual_ref"],
            name=op.f("fk_outcome_disposition_operation_outcome_actual"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["actual_realization_material_state_ref"],
            [f"{_SCHEMA}.actual_realization_state.material_state_ref"],
            name=op.f("fk_outcome_disposition_operation_actual_realization"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["outcome_ref", "expected_material_state_ref"],
            [
                f"{_SCHEMA}.outcome_disposition_state.outcome_ref",
                f"{_SCHEMA}.outcome_disposition_state.material_state_ref",
            ],
            name=op.f("fk_outcome_disposition_operation_expected_state"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["outcome_ref", "resulting_material_state_ref"],
            [
                f"{_SCHEMA}.outcome_disposition_state.outcome_ref",
                f"{_SCHEMA}.outcome_disposition_state.material_state_ref",
            ],
            name=op.f("fk_outcome_disposition_operation_resulting_state"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        schema=_SCHEMA,
    )

    _sql(
        r"""
CREATE FUNCTION dante._outcome_actual_owned(
  requested_self_person_ref uuid,
  requested_actual_ref uuid
) RETURNS boolean
LANGUAGE sql
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT EXISTS (
    SELECT 1
      FROM dante.actual AS owner
      JOIN dante.native_address AS subject_address
        ON subject_address.native_ref=owner.subject_native_ref
     WHERE owner.actual_ref=requested_actual_ref
       AND subject_address.owner_family IN ('activity','event','occurrence')
       AND dante._actual_subject_owned_as(
         requested_self_person_ref,
         subject_address.owner_family,
         owner.subject_native_ref
       )
  );
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.record_self_actual_outcome(
  requested_self_person_ref uuid,
  requested_operation_id text,
  requested_intent_fingerprint text,
  requested_actual_ref uuid,
  requested_actual_realization_material_state_ref uuid,
  requested_outcome_ref uuid,
  requested_material_state_ref uuid,
  requested_expected_material_state_ref uuid,
  requested_disposition_code text
) RETURNS TABLE(
  outcome_ref uuid,
  actual_ref uuid,
  actual_realization_material_state_ref uuid,
  material_state_ref uuid,
  disposition_code text,
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
  receipt_outcome_ref uuid;
  receipt_actual_ref uuid;
  receipt_actual_state_ref uuid;
  receipt_state_ref uuid;
  resolved_outcome_ref uuid;
  current_actual_state_ref uuid;
  current_outcome_state_ref uuid;
  current_from timestamptz;
  recorded_at timestamptz := statement_timestamp();
BEGIN
  IF normalized_operation_id='' OR char_length(normalized_operation_id)>200 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_outcome_disposition_operation_operation_id',
      MESSAGE='Outcome operation id rejected';
  END IF;
  IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_outcome_disposition_operation_fingerprint',
      MESSAGE='Outcome operation fingerprint rejected';
  END IF;
  IF requested_disposition_code<>btrim(requested_disposition_code)
     OR requested_disposition_code=''
     OR char_length(requested_disposition_code)>120
     OR requested_disposition_code !~ '^[a-z0-9][a-z0-9._:-]*$' THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_outcome_disposition_state_code',
      MESSAGE='Outcome disposition code rejected';
  END IF;
  IF uuid_extract_version(requested_outcome_ref) IS DISTINCT FROM 7
     OR uuid_extract_version(requested_material_state_ref) IS DISTINCT FROM 7 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      MESSAGE='Outcome reference rejected';
  END IF;

  PERFORM pg_advisory_xact_lock(
    hashtextextended(
      requested_self_person_ref::text || ':outcome-op:' || normalized_operation_id,
      0
    )
  );

  SELECT operation.intent_fingerprint,
         operation.outcome_ref,
         operation.actual_ref,
         operation.actual_realization_material_state_ref,
         operation.resulting_material_state_ref
    INTO existing_fingerprint,
         receipt_outcome_ref,
         receipt_actual_ref,
         receipt_actual_state_ref,
         receipt_state_ref
    FROM dante.outcome_disposition_operation AS operation
   WHERE operation.self_person_ref=requested_self_person_ref
     AND operation.operation_id=normalized_operation_id;

  IF FOUND THEN
    IF existing_fingerprint<>requested_intent_fingerprint
       OR receipt_actual_ref<>requested_actual_ref
       OR receipt_actual_state_ref<>requested_actual_realization_material_state_ref THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        CONSTRAINT='outcome_operation_reused',
        MESSAGE='Outcome operation id reused with different intent';
    END IF;
    RETURN QUERY
    SELECT owner.outcome_ref,
           owner.actual_ref,
           state.actual_realization_material_state_ref,
           state.material_state_ref,
           state.disposition_code,
           true
      FROM dante.outcome AS owner
      JOIN dante.outcome_disposition_state AS state
        ON state.outcome_ref=owner.outcome_ref
     WHERE owner.outcome_ref=receipt_outcome_ref
       AND state.material_state_ref=receipt_state_ref;
    RETURN;
  END IF;

  IF NOT dante._outcome_actual_owned(
       requested_self_person_ref,
       requested_actual_ref
     ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='outcome_actual_unavailable',
      MESSAGE='Outcome Actual unavailable';
  END IF;

  SELECT current.material_state_ref
    INTO current_actual_state_ref
    FROM dante.scoped_current_material_state AS current
    JOIN dante.actual_realization_state AS state
      ON state.actual_ref=requested_actual_ref
     AND state.material_state_ref=current.material_state_ref
   WHERE current.scoped_owner_ref=requested_actual_ref
     AND current.facet_code='actual.realization';

  IF current_actual_state_ref IS NULL
     OR current_actual_state_ref<>requested_actual_realization_material_state_ref THEN
    RAISE EXCEPTION USING ERRCODE='40001',
      CONSTRAINT='outcome_actual_current_conflict',
      MESSAGE='Outcome Actual realization basis is not current';
  END IF;

  PERFORM pg_advisory_xact_lock(
    hashtextextended('outcome-actual:' || requested_actual_ref::text, 0)
  );

  SELECT owner.outcome_ref
    INTO resolved_outcome_ref
    FROM dante.outcome AS owner
   WHERE owner.actual_ref=requested_actual_ref
   LIMIT 1;

  IF resolved_outcome_ref IS NULL THEN
    IF requested_expected_material_state_ref IS NOT NULL THEN
      RAISE EXCEPTION USING ERRCODE='40001',
        CONSTRAINT='outcome_current_conflict',
        MESSAGE='Outcome expected current state does not exist';
    END IF;

    resolved_outcome_ref:=requested_outcome_ref;
    INSERT INTO dante.outcome(outcome_ref, actual_ref)
    VALUES (resolved_outcome_ref, requested_actual_ref);

    INSERT INTO dante.scoped_address(scoped_ref, scoped_family)
    VALUES (resolved_outcome_ref, 'outcome');
  ELSE
    SELECT current.material_state_ref,
           history.current_from_at
      INTO current_outcome_state_ref, current_from
      FROM dante.scoped_current_material_state AS current
      JOIN dante.outcome_disposition_current_history AS history
        ON history.outcome_ref=resolved_outcome_ref
       AND history.material_state_ref=current.material_state_ref
       AND history.current_until_at IS NULL
     WHERE current.scoped_owner_ref=resolved_outcome_ref
       AND current.facet_code='outcome.disposition'
     FOR UPDATE OF history;

    IF current_outcome_state_ref IS DISTINCT FROM requested_expected_material_state_ref THEN
      RAISE EXCEPTION USING ERRCODE='40001',
        CONSTRAINT='outcome_current_conflict',
        MESSAGE='Outcome expected current state is stale';
    END IF;
  END IF;

  IF current_from IS NOT NULL AND recorded_at<=current_from THEN
    recorded_at:=current_from + interval '1 microsecond';
  END IF;

  INSERT INTO dante.material_state_address(
    material_state_ref, scoped_owner_ref, facet_code
  ) VALUES (
    requested_material_state_ref,
    resolved_outcome_ref,
    'outcome.disposition'
  );

  INSERT INTO dante.outcome_disposition_state(
    material_state_ref,
    outcome_ref,
    actual_realization_material_state_ref,
    disposition_code
  ) VALUES (
    requested_material_state_ref,
    resolved_outcome_ref,
    requested_actual_realization_material_state_ref,
    requested_disposition_code
  );

  IF current_outcome_state_ref IS NULL THEN
    INSERT INTO dante.scoped_current_material_state(
      scoped_owner_ref, facet_code, material_state_ref
    ) VALUES (
      resolved_outcome_ref,
      'outcome.disposition',
      requested_material_state_ref
    );
  ELSE
    UPDATE dante.outcome_disposition_current_history
       SET current_until_at=recorded_at
     WHERE outcome_disposition_current_history.outcome_ref=resolved_outcome_ref
       AND current_until_at IS NULL;

    UPDATE dante.scoped_current_material_state
       SET material_state_ref=requested_material_state_ref
     WHERE scoped_owner_ref=resolved_outcome_ref
       AND facet_code='outcome.disposition';
  END IF;

  INSERT INTO dante.outcome_disposition_current_history(
    outcome_ref, material_state_ref, current_from_at
  ) VALUES (
    resolved_outcome_ref,
    requested_material_state_ref,
    recorded_at
  );

  INSERT INTO dante.outcome_disposition_operation(
    self_person_ref,
    operation_id,
    intent_fingerprint,
    actual_ref,
    outcome_ref,
    actual_realization_material_state_ref,
    expected_material_state_ref,
    resulting_material_state_ref,
    created_at
  ) VALUES (
    requested_self_person_ref,
    normalized_operation_id,
    requested_intent_fingerprint,
    requested_actual_ref,
    resolved_outcome_ref,
    requested_actual_realization_material_state_ref,
    requested_expected_material_state_ref,
    requested_material_state_ref,
    recorded_at
  );

  RETURN QUERY
  SELECT resolved_outcome_ref,
         requested_actual_ref,
         requested_actual_realization_material_state_ref,
         requested_material_state_ref,
         requested_disposition_code,
         false;
END;
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.get_self_actual_outcome(
  requested_self_person_ref uuid,
  requested_actual_ref uuid
) RETURNS TABLE(
  outcome_ref uuid,
  actual_ref uuid,
  actual_realization_material_state_ref uuid,
  material_state_ref uuid,
  disposition_code text
)
LANGUAGE plpgsql
SECURITY DEFINER
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
BEGIN
  IF NOT dante._outcome_actual_owned(
       requested_self_person_ref,
       requested_actual_ref
     ) THEN
    RETURN;
  END IF;

  RETURN QUERY
  SELECT owner.outcome_ref,
         owner.actual_ref,
         state.actual_realization_material_state_ref,
         state.material_state_ref,
         state.disposition_code
    FROM dante.outcome AS owner
    JOIN dante.scoped_current_material_state AS current
      ON current.scoped_owner_ref=owner.outcome_ref
     AND current.facet_code='outcome.disposition'
    JOIN dante.outcome_disposition_state AS state
      ON state.outcome_ref=owner.outcome_ref
     AND state.material_state_ref=current.material_state_ref
   WHERE owner.actual_ref=requested_actual_ref;
END;
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.list_self_outcome_history(
  requested_self_person_ref uuid,
  requested_outcome_ref uuid
) RETURNS TABLE(
  outcome_ref uuid,
  actual_ref uuid,
  actual_realization_material_state_ref uuid,
  material_state_ref uuid,
  disposition_code text,
  current_from_at timestamptz,
  current_until_at timestamptz
)
LANGUAGE plpgsql
SECURITY DEFINER
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
BEGIN
  IF NOT EXISTS (
    SELECT 1
      FROM dante.outcome AS owner
     WHERE owner.outcome_ref=requested_outcome_ref
       AND dante._outcome_actual_owned(
         requested_self_person_ref,
         owner.actual_ref
       )
  ) THEN
    RETURN;
  END IF;

  RETURN QUERY
  SELECT owner.outcome_ref,
         owner.actual_ref,
         state.actual_realization_material_state_ref,
         state.material_state_ref,
         state.disposition_code,
         history.current_from_at,
         history.current_until_at
    FROM dante.outcome AS owner
    JOIN dante.outcome_disposition_current_history AS history
      ON history.outcome_ref=owner.outcome_ref
    JOIN dante.outcome_disposition_state AS state
      ON state.outcome_ref=owner.outcome_ref
     AND state.material_state_ref=history.material_state_ref
   WHERE owner.outcome_ref=requested_outcome_ref
   ORDER BY history.current_from_at ASC;
END;
$function$
"""
    )

    for signature in (
        _HELPER_SIGNATURE,
        _WRITE_SIGNATURE,
        _READ_SIGNATURE,
        _HISTORY_SIGNATURE,
    ):
        _sql(f"ALTER FUNCTION {signature} OWNER TO {_OWNER}")
        _sql(
            f"REVOKE ALL ON FUNCTION {signature} "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )

    for signature in (
        _WRITE_SIGNATURE,
        _READ_SIGNATURE,
        _HISTORY_SIGNATURE,
    ):
        _sql(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}")

    for table_name in (
        "outcome",
        "outcome_disposition_state",
        "outcome_disposition_current_history",
        "outcome_disposition_operation",
    ):
        _sql(
            "REVOKE ALL PRIVILEGES ON TABLE "
            f"{_SCHEMA}.{table_name} "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )


def downgrade() -> None:
    raise RuntimeError(
        "B10-B Outcome disposition reconciliation downgrade is intentionally refused; "
        "use a separately reviewed forward migration"
    )
