"""B10-C: materialize contextual Confirmation substrate and guarded capability.

Revision ID: 20260925_79
Revises: 20260925_78

Confirmation is a distinct attestation owner. It is optional, actor-scoped and
pinned to one exact Outcome disposition MaterialState. 0..N Confirmation owners
may exist for the same target. Contrasting Confirmations from different actors
remain representable. Outcome correction does not transfer an existing
Confirmation onto a later Outcome MaterialState.

ScopedAddress family `confirmation` and MaterialState facet
`confirmation.attestation` are required by this model. Owner-dispatch and
MaterialState totality are extended in this same revision so Confirmation is
admitted without a later repair.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260925_79"
down_revision: str | None = "20260925_78"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"

_HELPER_SIGNATURE = "dante._confirmation_outcome_owned(uuid,uuid)"
_WRITE_SIGNATURE = (
    "dante.record_self_outcome_confirmation("
    "uuid,text,text,uuid,uuid,uuid,uuid,uuid,text,text)"
)
_READ_SIGNATURE = "dante.list_self_outcome_confirmations(uuid,uuid)"
_HISTORY_SIGNATURE = "dante.list_self_confirmation_history(uuid,uuid)"

_CODE_CONTRACT = (
    "{column}=btrim({column}) AND {column}<>'' "
    "AND char_length({column})<=120 "
    "AND {column} ~ '^[a-z0-9][a-z0-9._:-]*$'"
)


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def upgrade() -> None:
    op.drop_constraint(
        op.f("ck_scoped_address_scoped_family"),
        "scoped_address",
        schema=_SCHEMA,
        type_="check",
    )
    op.create_check_constraint(
        op.f("ck_scoped_address_scoped_family"),
        "scoped_address",
        "scoped_family IN ("
        "'schedule','actual','temporal_constraint','outcome','confirmation')",
        schema=_SCHEMA,
    )

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
        "'temporal_constraint.rule','outcome.disposition',"
        "'confirmation.attestation')",
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
        "'outcome.disposition','confirmation.attestation')",
        schema=_SCHEMA,
    )

    op.create_table(
        "confirmation",
        sa.Column("confirmation_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("outcome_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "outcome_disposition_material_state_ref",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column("confirmer_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("purpose_code", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("confirmation_ref", name=op.f("pk_confirmation")),
        sa.CheckConstraint(
            "uuid_extract_version(confirmation_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_confirmation_uuidv7"),
        ),
        sa.CheckConstraint(
            _CODE_CONTRACT.format(column="purpose_code"),
            name=op.f("ck_confirmation_purpose"),
        ),
        sa.UniqueConstraint(
            "outcome_disposition_material_state_ref",
            "confirmer_person_ref",
            "purpose_code",
            name=op.f("uq_confirmation_target_actor_purpose"),
        ),
        sa.UniqueConstraint(
            "confirmation_ref",
            "outcome_ref",
            name=op.f("uq_confirmation_ref_outcome"),
        ),
        sa.ForeignKeyConstraint(
            ["outcome_ref"],
            [f"{_SCHEMA}.outcome.outcome_ref"],
            name=op.f("fk_confirmation_outcome_ref_outcome"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["outcome_ref", "outcome_disposition_material_state_ref"],
            [
                f"{_SCHEMA}.outcome_disposition_state.outcome_ref",
                f"{_SCHEMA}.outcome_disposition_state.material_state_ref",
            ],
            name=op.f("fk_confirmation_outcome_disposition"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["confirmer_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name=op.f("fk_confirmation_confirmer_person"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_confirmation_outcome_ref",
        "confirmation",
        ["outcome_ref"],
        unique=False,
        schema=_SCHEMA,
    )

    op.create_table(
        "confirmation_attestation_state",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("confirmation_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("stance_code", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_confirmation_attestation_state"),
        ),
        sa.UniqueConstraint(
            "confirmation_ref",
            "material_state_ref",
            name=op.f("uq_confirmation_attestation_state_confirmation_material"),
        ),
        sa.CheckConstraint(
            _CODE_CONTRACT.format(column="stance_code"),
            name=op.f("ck_confirmation_attestation_state_stance"),
        ),
        sa.ForeignKeyConstraint(
            ["material_state_ref"],
            [f"{_SCHEMA}.material_state_address.material_state_ref"],
            name=op.f("fk_confirmation_attestation_state_state_address"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["confirmation_ref"],
            [f"{_SCHEMA}.confirmation.confirmation_ref"],
            name=op.f("fk_confirmation_attestation_state_confirmation"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_confirmation_attestation_state_confirmation_ref",
        "confirmation_attestation_state",
        ["confirmation_ref"],
        unique=False,
        schema=_SCHEMA,
    )

    op.create_table(
        "confirmation_attestation_current_history",
        sa.Column("confirmation_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("current_from_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_until_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "confirmation_ref",
            "current_from_at",
            name=op.f("pk_confirmation_attestation_current_history"),
        ),
        sa.CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at>current_from_at))",
            name=op.f("ck_confirmation_attestation_current_history_interval"),
        ),
        sa.ForeignKeyConstraint(
            ["confirmation_ref", "material_state_ref"],
            [
                f"{_SCHEMA}.confirmation_attestation_state.confirmation_ref",
                f"{_SCHEMA}.confirmation_attestation_state.material_state_ref",
            ],
            name=op.f("fk_confirmation_attestation_current_history_state"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ux_confirmation_attestation_current_history_open",
        "confirmation_attestation_current_history",
        ["confirmation_ref"],
        unique=True,
        schema=_SCHEMA,
        postgresql_where=sa.text("current_until_at IS NULL"),
    )
    op.create_index(
        "ix_confirmation_attestation_current_history_material_state_ref",
        "confirmation_attestation_current_history",
        ["material_state_ref"],
        unique=False,
        schema=_SCHEMA,
    )

    op.create_table(
        "confirmation_attestation_operation",
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("confirmation_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("outcome_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "outcome_disposition_material_state_ref",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column("confirmer_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("purpose_code", sa.Text(), nullable=False),
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
            name=op.f("pk_confirmation_attestation_operation"),
        ),
        sa.UniqueConstraint(
            "resulting_material_state_ref",
            name=op.f("uq_confirmation_attestation_operation_resulting_state"),
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f("ck_confirmation_attestation_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_confirmation_attestation_operation_fingerprint"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name=op.f("fk_confirmation_attestation_operation_self_person"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["confirmation_ref", "outcome_ref"],
            [f"{_SCHEMA}.confirmation.confirmation_ref", f"{_SCHEMA}.confirmation.outcome_ref"],
            name=op.f("fk_confirmation_attestation_operation_confirmation_outcome"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["outcome_disposition_material_state_ref"],
            [f"{_SCHEMA}.outcome_disposition_state.material_state_ref"],
            name=op.f("fk_confirmation_attestation_operation_outcome_disposition"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["confirmation_ref", "expected_material_state_ref"],
            [
                f"{_SCHEMA}.confirmation_attestation_state.confirmation_ref",
                f"{_SCHEMA}.confirmation_attestation_state.material_state_ref",
            ],
            name=op.f("fk_confirmation_attestation_operation_expected_state"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["confirmation_ref", "resulting_material_state_ref"],
            [
                f"{_SCHEMA}.confirmation_attestation_state.confirmation_ref",
                f"{_SCHEMA}.confirmation_attestation_state.material_state_ref",
            ],
            name=op.f("fk_confirmation_attestation_operation_resulting_state"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        schema=_SCHEMA,
    )

    _sql(
        r"""
CREATE FUNCTION dante._confirmation_outcome_owned(
  requested_self_person_ref uuid,
  requested_outcome_ref uuid
) RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT EXISTS (
    SELECT 1
      FROM dante.outcome AS owner
     WHERE owner.outcome_ref=requested_outcome_ref
       AND dante._outcome_actual_owned(
         requested_self_person_ref,
         owner.actual_ref
       )
  );
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.record_self_outcome_confirmation(
  requested_self_person_ref uuid,
  requested_operation_id text,
  requested_intent_fingerprint text,
  requested_outcome_ref uuid,
  requested_outcome_disposition_material_state_ref uuid,
  requested_confirmation_ref uuid,
  requested_material_state_ref uuid,
  requested_expected_material_state_ref uuid,
  requested_purpose_code text,
  requested_stance_code text
) RETURNS TABLE(
  confirmation_ref uuid,
  outcome_ref uuid,
  outcome_disposition_material_state_ref uuid,
  confirmer_person_ref uuid,
  purpose_code text,
  material_state_ref uuid,
  stance_code text,
  confirmer_is_self boolean,
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
  receipt_confirmation_ref uuid;
  receipt_outcome_ref uuid;
  receipt_outcome_state_ref uuid;
  receipt_state_ref uuid;
  resolved_confirmation_ref uuid;
  current_confirmation_state_ref uuid;
  current_from timestamptz;
  recorded_at timestamptz := statement_timestamp();
  target_exists boolean := false;
BEGIN
  IF normalized_operation_id='' OR char_length(normalized_operation_id)>200 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_confirmation_attestation_operation_operation_id',
      MESSAGE='Confirmation operation id rejected';
  END IF;
  IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_confirmation_attestation_operation_fingerprint',
      MESSAGE='Confirmation operation fingerprint rejected';
  END IF;
  IF requested_purpose_code<>btrim(requested_purpose_code)
     OR requested_purpose_code=''
     OR char_length(requested_purpose_code)>120
     OR requested_purpose_code !~ '^[a-z0-9][a-z0-9._:-]*$' THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_confirmation_purpose',
      MESSAGE='Confirmation purpose code rejected';
  END IF;
  IF requested_stance_code<>btrim(requested_stance_code)
     OR requested_stance_code=''
     OR char_length(requested_stance_code)>120
     OR requested_stance_code !~ '^[a-z0-9][a-z0-9._:-]*$' THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_confirmation_attestation_state_stance',
      MESSAGE='Confirmation stance code rejected';
  END IF;
  IF uuid_extract_version(requested_confirmation_ref) IS DISTINCT FROM 7
     OR uuid_extract_version(requested_material_state_ref) IS DISTINCT FROM 7 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      MESSAGE='Confirmation reference rejected';
  END IF;

  PERFORM pg_advisory_xact_lock(
    hashtextextended(
      requested_self_person_ref::text || ':confirmation-op:' || normalized_operation_id,
      0
    )
  );

  SELECT operation.intent_fingerprint,
         operation.confirmation_ref,
         operation.outcome_ref,
         operation.outcome_disposition_material_state_ref,
         operation.resulting_material_state_ref
    INTO existing_fingerprint,
         receipt_confirmation_ref,
         receipt_outcome_ref,
         receipt_outcome_state_ref,
         receipt_state_ref
    FROM dante.confirmation_attestation_operation AS operation
   WHERE operation.self_person_ref=requested_self_person_ref
     AND operation.operation_id=normalized_operation_id;

  IF FOUND THEN
    IF existing_fingerprint<>requested_intent_fingerprint
       OR receipt_outcome_ref<>requested_outcome_ref
       OR receipt_outcome_state_ref<>requested_outcome_disposition_material_state_ref THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        CONSTRAINT='confirmation_operation_reused',
        MESSAGE='Confirmation operation id reused with different intent';
    END IF;
    RETURN QUERY
    SELECT owner.confirmation_ref,
           owner.outcome_ref,
           owner.outcome_disposition_material_state_ref,
           owner.confirmer_person_ref,
           owner.purpose_code,
           state.material_state_ref,
           state.stance_code,
           true,
           true
      FROM dante.confirmation AS owner
      JOIN dante.confirmation_attestation_state AS state
        ON state.confirmation_ref=owner.confirmation_ref
     WHERE owner.confirmation_ref=receipt_confirmation_ref
       AND state.material_state_ref=receipt_state_ref;
    RETURN;
  END IF;

  SELECT EXISTS (
    SELECT 1
      FROM dante.outcome_disposition_state AS state
     WHERE state.outcome_ref=requested_outcome_ref
       AND state.material_state_ref=requested_outcome_disposition_material_state_ref
  ) INTO target_exists;

  IF NOT target_exists THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='confirmation_outcome_unavailable',
      MESSAGE='Confirmation Outcome target unavailable';
  END IF;

  PERFORM pg_advisory_xact_lock(
    hashtextextended(
      'confirmation-target:'
      || requested_outcome_disposition_material_state_ref::text
      || ':'
      || requested_self_person_ref::text
      || ':'
      || requested_purpose_code,
      0
    )
  );

  SELECT owner.confirmation_ref
    INTO resolved_confirmation_ref
    FROM dante.confirmation AS owner
   WHERE owner.outcome_disposition_material_state_ref
           =requested_outcome_disposition_material_state_ref
     AND owner.confirmer_person_ref=requested_self_person_ref
     AND owner.purpose_code=requested_purpose_code
   LIMIT 1;

  IF resolved_confirmation_ref IS NULL THEN
    IF requested_expected_material_state_ref IS NOT NULL THEN
      RAISE EXCEPTION USING ERRCODE='40001',
        CONSTRAINT='confirmation_current_conflict',
        MESSAGE='Confirmation expected current state does not exist';
    END IF;

    resolved_confirmation_ref:=requested_confirmation_ref;
    INSERT INTO dante.confirmation(
      confirmation_ref,
      outcome_ref,
      outcome_disposition_material_state_ref,
      confirmer_person_ref,
      purpose_code
    ) VALUES (
      resolved_confirmation_ref,
      requested_outcome_ref,
      requested_outcome_disposition_material_state_ref,
      requested_self_person_ref,
      requested_purpose_code
    );

    INSERT INTO dante.scoped_address(scoped_ref, scoped_family)
    VALUES (resolved_confirmation_ref, 'confirmation');
  ELSE
    SELECT current.material_state_ref,
           history.current_from_at
      INTO current_confirmation_state_ref, current_from
      FROM dante.scoped_current_material_state AS current
      JOIN dante.confirmation_attestation_current_history AS history
        ON history.confirmation_ref=resolved_confirmation_ref
       AND history.material_state_ref=current.material_state_ref
       AND history.current_until_at IS NULL
     WHERE current.scoped_owner_ref=resolved_confirmation_ref
       AND current.facet_code='confirmation.attestation'
     FOR UPDATE OF history;

    IF current_confirmation_state_ref IS DISTINCT FROM requested_expected_material_state_ref THEN
      RAISE EXCEPTION USING ERRCODE='40001',
        CONSTRAINT='confirmation_current_conflict',
        MESSAGE='Confirmation expected current state is stale';
    END IF;
  END IF;

  IF current_from IS NOT NULL AND recorded_at<=current_from THEN
    recorded_at:=current_from + interval '1 microsecond';
  END IF;

  INSERT INTO dante.material_state_address(
    material_state_ref, scoped_owner_ref, facet_code
  ) VALUES (
    requested_material_state_ref,
    resolved_confirmation_ref,
    'confirmation.attestation'
  );

  INSERT INTO dante.confirmation_attestation_state(
    material_state_ref,
    confirmation_ref,
    stance_code
  ) VALUES (
    requested_material_state_ref,
    resolved_confirmation_ref,
    requested_stance_code
  );

  IF current_confirmation_state_ref IS NULL THEN
    INSERT INTO dante.scoped_current_material_state(
      scoped_owner_ref, facet_code, material_state_ref
    ) VALUES (
      resolved_confirmation_ref,
      'confirmation.attestation',
      requested_material_state_ref
    );
  ELSE
    UPDATE dante.confirmation_attestation_current_history
       SET current_until_at=recorded_at
     WHERE confirmation_attestation_current_history.confirmation_ref
             =resolved_confirmation_ref
       AND current_until_at IS NULL;

    UPDATE dante.scoped_current_material_state
       SET material_state_ref=requested_material_state_ref
     WHERE scoped_owner_ref=resolved_confirmation_ref
       AND facet_code='confirmation.attestation';
  END IF;

  INSERT INTO dante.confirmation_attestation_current_history(
    confirmation_ref, material_state_ref, current_from_at
  ) VALUES (
    resolved_confirmation_ref,
    requested_material_state_ref,
    recorded_at
  );

  INSERT INTO dante.confirmation_attestation_operation(
    self_person_ref,
    operation_id,
    intent_fingerprint,
    confirmation_ref,
    outcome_ref,
    outcome_disposition_material_state_ref,
    confirmer_person_ref,
    purpose_code,
    expected_material_state_ref,
    resulting_material_state_ref,
    created_at
  ) VALUES (
    requested_self_person_ref,
    normalized_operation_id,
    requested_intent_fingerprint,
    resolved_confirmation_ref,
    requested_outcome_ref,
    requested_outcome_disposition_material_state_ref,
    requested_self_person_ref,
    requested_purpose_code,
    requested_expected_material_state_ref,
    requested_material_state_ref,
    recorded_at
  );

  RETURN QUERY
  SELECT resolved_confirmation_ref,
         requested_outcome_ref,
         requested_outcome_disposition_material_state_ref,
         requested_self_person_ref,
         requested_purpose_code,
         requested_material_state_ref,
         requested_stance_code,
         true,
         false;
END;
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.list_self_outcome_confirmations(
  requested_self_person_ref uuid,
  requested_outcome_ref uuid
) RETURNS TABLE(
  confirmation_ref uuid,
  outcome_ref uuid,
  outcome_disposition_material_state_ref uuid,
  confirmer_person_ref uuid,
  purpose_code text,
  material_state_ref uuid,
  stance_code text,
  confirmer_is_self boolean
)
LANGUAGE plpgsql
SECURITY DEFINER
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
BEGIN
  IF NOT dante._confirmation_outcome_owned(
       requested_self_person_ref,
       requested_outcome_ref
     ) THEN
    RETURN;
  END IF;

  RETURN QUERY
  SELECT owner.confirmation_ref,
         owner.outcome_ref,
         owner.outcome_disposition_material_state_ref,
         owner.confirmer_person_ref,
         owner.purpose_code,
         state.material_state_ref,
         state.stance_code,
         owner.confirmer_person_ref=requested_self_person_ref
    FROM dante.confirmation AS owner
    JOIN dante.scoped_current_material_state AS current
      ON current.scoped_owner_ref=owner.confirmation_ref
     AND current.facet_code='confirmation.attestation'
    JOIN dante.confirmation_attestation_state AS state
      ON state.confirmation_ref=owner.confirmation_ref
     AND state.material_state_ref=current.material_state_ref
   WHERE owner.outcome_ref=requested_outcome_ref
   ORDER BY owner.confirmation_ref ASC;
END;
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.list_self_confirmation_history(
  requested_self_person_ref uuid,
  requested_confirmation_ref uuid
) RETURNS TABLE(
  confirmation_ref uuid,
  outcome_ref uuid,
  outcome_disposition_material_state_ref uuid,
  confirmer_person_ref uuid,
  purpose_code text,
  material_state_ref uuid,
  stance_code text,
  confirmer_is_self boolean,
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
      FROM dante.confirmation AS owner
     WHERE owner.confirmation_ref=requested_confirmation_ref
       AND (
         owner.confirmer_person_ref=requested_self_person_ref
         OR dante._confirmation_outcome_owned(
           requested_self_person_ref,
           owner.outcome_ref
         )
       )
  ) THEN
    RETURN;
  END IF;

  RETURN QUERY
  SELECT owner.confirmation_ref,
         owner.outcome_ref,
         owner.outcome_disposition_material_state_ref,
         owner.confirmer_person_ref,
         owner.purpose_code,
         state.material_state_ref,
         state.stance_code,
         owner.confirmer_person_ref=requested_self_person_ref,
         history.current_from_at,
         history.current_until_at
    FROM dante.confirmation AS owner
    JOIN dante.confirmation_attestation_current_history AS history
      ON history.confirmation_ref=owner.confirmation_ref
    JOIN dante.confirmation_attestation_state AS state
      ON state.confirmation_ref=owner.confirmation_ref
     AND state.material_state_ref=history.material_state_ref
   WHERE owner.confirmation_ref=requested_confirmation_ref
   ORDER BY history.current_from_at ASC;
END;
$function$
"""
    )

    _sql(
        r"""
CREATE OR REPLACE FUNCTION dante.enforce_scoped_address_owner()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
VOLATILE
PARALLEL UNSAFE
SET search_path = pg_catalog, dante, pg_temp
AS $function$
DECLARE
    owner_exists boolean := false;
BEGIN
    CASE NEW.scoped_family
        WHEN 'schedule' THEN
            SELECT EXISTS (
                SELECT 1
                  FROM dante.schedule
                 WHERE schedule_ref=NEW.scoped_ref
            ) INTO owner_exists;
        WHEN 'actual' THEN
            SELECT EXISTS (
                SELECT 1
                  FROM dante.actual
                 WHERE actual_ref=NEW.scoped_ref
            ) INTO owner_exists;
        WHEN 'temporal_constraint' THEN
            SELECT EXISTS (
                SELECT 1
                  FROM dante.temporal_constraint
                 WHERE constraint_ref=NEW.scoped_ref
            ) INTO owner_exists;
        WHEN 'outcome' THEN
            SELECT EXISTS (
                SELECT 1
                  FROM dante.outcome
                 WHERE outcome_ref=NEW.scoped_ref
            ) INTO owner_exists;
        WHEN 'confirmation' THEN
            SELECT EXISTS (
                SELECT 1
                  FROM dante.confirmation
                 WHERE confirmation_ref=NEW.scoped_ref
            ) INTO owner_exists;
        ELSE
            owner_exists := false;
    END CASE;

    IF NOT owner_exists THEN
        RAISE EXCEPTION USING
            ERRCODE='23503',
            CONSTRAINT=TG_NAME,
            TABLE=TG_TABLE_NAME,
            SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='scoped address owner binding rejected',
            DETAIL='scoped address must resolve to the declared bounded owner family';
    END IF;

    RETURN NEW;
END;
$function$
"""
    )

    _sql(
        r"""
CREATE OR REPLACE FUNCTION dante.enforce_material_state_totality()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
VOLATILE
PARALLEL UNSAFE
SET search_path = pg_catalog, dante, pg_temp
AS $function$
DECLARE
    state_ref uuid;
    a record;
    schedule_n integer;
    movement_n integer;
    actual_n integer;
    session_n integer;
    routine_n integer;
    event_n integer;
    constraint_n integer;
    outcome_n integer;
    confirmation_n integer;
    owner_ok boolean := false;
BEGIN
    state_ref := CASE WHEN TG_OP='DELETE' THEN OLD.material_state_ref ELSE NEW.material_state_ref END;

    SELECT material_state_ref,native_owner_ref,scoped_owner_ref,facet_code
      INTO a
      FROM dante.material_state_address
     WHERE material_state_ref=state_ref;

    IF NOT FOUND THEN
        IF TG_OP='DELETE' THEN RETURN OLD; END IF;
        RETURN NEW;
    END IF;

    SELECT
      (SELECT count(*) FROM dante.schedule_placement_state WHERE material_state_ref=state_ref),
      (SELECT count(*) FROM dante.schedule_movement_policy_state WHERE material_state_ref=state_ref),
      (SELECT count(*) FROM dante.actual_realization_state WHERE material_state_ref=state_ref),
      (SELECT count(*) FROM dante.session_timing_state WHERE material_state_ref=state_ref),
      (SELECT count(*) FROM dante.routine_recurrence_state WHERE material_state_ref=state_ref),
      (SELECT count(*) FROM dante.event_recurrence_state WHERE material_state_ref=state_ref),
      (SELECT count(*) FROM dante.temporal_constraint_state WHERE material_state_ref=state_ref),
      (SELECT count(*) FROM dante.outcome_disposition_state WHERE material_state_ref=state_ref),
      (SELECT count(*) FROM dante.confirmation_attestation_state WHERE material_state_ref=state_ref)
      INTO schedule_n,movement_n,actual_n,session_n,routine_n,event_n,constraint_n,outcome_n,confirmation_n;

    IF a.facet_code='temporal_constraint.rule' THEN
        SELECT EXISTS (
            SELECT 1
              FROM dante.temporal_constraint_state AS s
              JOIN dante.scoped_address AS x
                ON x.scoped_ref=a.scoped_owner_ref
               AND x.scoped_family='temporal_constraint'
             WHERE s.material_state_ref=state_ref
               AND s.constraint_ref=a.scoped_owner_ref
               AND a.native_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND constraint_n=1
            AND schedule_n+movement_n+actual_n+session_n+routine_n+event_n+outcome_n+confirmation_n=0;

    ELSIF a.facet_code='schedule.placement' THEN
        SELECT EXISTS (
            SELECT 1
              FROM dante.schedule_placement_state AS s
              JOIN dante.scoped_address AS x
                ON x.scoped_ref=a.scoped_owner_ref
               AND x.scoped_family='schedule'
             WHERE s.material_state_ref=state_ref
               AND s.schedule_ref=a.scoped_owner_ref
               AND a.native_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND schedule_n=1
            AND movement_n+actual_n+session_n+routine_n+event_n+constraint_n+outcome_n+confirmation_n=0;

    ELSIF a.facet_code='schedule.movement_policy' THEN
        SELECT EXISTS (
            SELECT 1
              FROM dante.schedule_movement_policy_state AS s
              JOIN dante.scoped_address AS x
                ON x.scoped_ref=a.scoped_owner_ref
               AND x.scoped_family='schedule'
             WHERE s.material_state_ref=state_ref
               AND s.schedule_ref=a.scoped_owner_ref
               AND a.native_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND movement_n=1
            AND schedule_n+actual_n+session_n+routine_n+event_n+constraint_n+outcome_n+confirmation_n=0;

    ELSIF a.facet_code='actual.realization' THEN
        SELECT EXISTS (
            SELECT 1
              FROM dante.actual_realization_state AS s
              JOIN dante.scoped_address AS x
                ON x.scoped_ref=a.scoped_owner_ref
               AND x.scoped_family='actual'
             WHERE s.material_state_ref=state_ref
               AND s.actual_ref=a.scoped_owner_ref
               AND a.native_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND actual_n=1
            AND schedule_n+movement_n+session_n+routine_n+event_n+constraint_n+outcome_n+confirmation_n=0;

    ELSIF a.facet_code='session.timing' THEN
        SELECT EXISTS (
            SELECT 1
              FROM dante.session_timing_state AS s
              JOIN dante.native_address AS x
                ON x.native_ref=a.native_owner_ref
               AND x.owner_family='session'
             WHERE s.material_state_ref=state_ref
               AND s.session_ref=a.native_owner_ref
               AND a.scoped_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND session_n=1
            AND schedule_n+movement_n+actual_n+routine_n+event_n+constraint_n+outcome_n+confirmation_n=0;

    ELSIF a.facet_code='routine.recurrence' THEN
        SELECT EXISTS (
            SELECT 1
              FROM dante.routine_recurrence_state AS s
              JOIN dante.native_address AS x
                ON x.native_ref=a.native_owner_ref
               AND x.owner_family='routine'
             WHERE s.material_state_ref=state_ref
               AND s.routine_ref=a.native_owner_ref
               AND a.scoped_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND routine_n=1
            AND schedule_n+movement_n+actual_n+session_n+event_n+constraint_n+outcome_n+confirmation_n=0;

    ELSIF a.facet_code='event.recurrence' THEN
        SELECT EXISTS (
            SELECT 1
              FROM dante.event_recurrence_state AS s
              JOIN dante.native_address AS x
                ON x.native_ref=a.native_owner_ref
               AND x.owner_family='event'
             WHERE s.material_state_ref=state_ref
               AND s.event_ref=a.native_owner_ref
               AND a.scoped_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND event_n=1
            AND schedule_n+movement_n+actual_n+session_n+routine_n+constraint_n+outcome_n+confirmation_n=0;

    ELSIF a.facet_code='outcome.disposition' THEN
        SELECT EXISTS (
            SELECT 1
              FROM dante.outcome_disposition_state AS s
              JOIN dante.scoped_address AS x
                ON x.scoped_ref=a.scoped_owner_ref
               AND x.scoped_family='outcome'
             WHERE s.material_state_ref=state_ref
               AND s.outcome_ref=a.scoped_owner_ref
               AND a.native_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND outcome_n=1
            AND schedule_n+movement_n+actual_n+session_n+routine_n+event_n+constraint_n+confirmation_n=0;

    ELSIF a.facet_code='confirmation.attestation' THEN
        SELECT EXISTS (
            SELECT 1
              FROM dante.confirmation_attestation_state AS s
              JOIN dante.scoped_address AS x
                ON x.scoped_ref=a.scoped_owner_ref
               AND x.scoped_family='confirmation'
             WHERE s.material_state_ref=state_ref
               AND s.confirmation_ref=a.scoped_owner_ref
               AND a.native_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND confirmation_n=1
            AND schedule_n+movement_n+actual_n+session_n+routine_n+event_n+constraint_n+outcome_n=0;
    END IF;

    IF NOT owner_ok THEN
        RAISE EXCEPTION USING
            ERRCODE='23514',
            CONSTRAINT=TG_NAME,
            TABLE=TG_TABLE_NAME,
            SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='material state totality rejected',
            DETAIL='MaterialState address, bounded owner family, facet and payload must form one exact live state';
    END IF;

    IF TG_OP='DELETE' THEN RETURN OLD; END IF;
    RETURN NEW;
END;
$function$
"""
    )

    _sql("ALTER FUNCTION dante.enforce_scoped_address_owner() OWNER TO dante_owner")
    _sql("REVOKE ALL ON FUNCTION dante.enforce_scoped_address_owner() FROM PUBLIC")
    _sql("REVOKE ALL ON FUNCTION dante.enforce_scoped_address_owner() FROM dante_runtime")
    _sql("REVOKE ALL ON FUNCTION dante.enforce_scoped_address_owner() FROM dante_migrator")

    _sql("ALTER FUNCTION dante.enforce_material_state_totality() OWNER TO dante_owner")
    _sql("REVOKE ALL ON FUNCTION dante.enforce_material_state_totality() FROM PUBLIC")
    _sql("REVOKE ALL ON FUNCTION dante.enforce_material_state_totality() FROM dante_runtime")
    _sql("REVOKE ALL ON FUNCTION dante.enforce_material_state_totality() FROM dante_migrator")

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
        _HELPER_SIGNATURE,
        _WRITE_SIGNATURE,
        _READ_SIGNATURE,
        _HISTORY_SIGNATURE,
    ):
        _sql(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}")

    for table_name in (
        "confirmation",
        "confirmation_attestation_state",
        "confirmation_attestation_current_history",
        "confirmation_attestation_operation",
    ):
        _sql(
            "REVOKE ALL PRIVILEGES ON TABLE "
            f"{_SCHEMA}.{table_name} "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )


def downgrade() -> None:
    raise RuntimeError(
        "B10-C Confirmation capability downgrade is intentionally refused; "
        "use a separately reviewed forward migration"
    )
