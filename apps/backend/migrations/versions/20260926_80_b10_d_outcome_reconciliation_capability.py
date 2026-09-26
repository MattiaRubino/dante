"""B10-D: materialize Outcome-scoped reconciliation and exact evidence pinning.

Revision ID: 20260926_80
Revises: 20260925_79

Reconciliation is a narrowly scoped workflow record for one exact Outcome
disposition MaterialState and one purpose. It does not replace Outcome,
Confirmation, Verification or Authority, and it never rewrites prior evidence.
The Outcome owner is the only resolver in this first slice.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260926_80"
down_revision: str | None = "20260925_79"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"

_HELPER_SIGNATURE = "dante._reconciliation_outcome_owned(uuid,uuid)"
_WRITE_SIGNATURE = (
    "dante.record_self_outcome_reconciliation("
    "uuid,text,text,uuid,uuid,uuid,uuid,uuid,text,text,uuid[],uuid[],text[])"
)
_READ_SIGNATURE = "dante.list_self_outcome_reconciliations(uuid,uuid)"
_HISTORY_SIGNATURE = "dante.list_self_outcome_reconciliation_history(uuid,uuid)"

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
        "'schedule','actual','temporal_constraint','outcome','confirmation',"
        "'outcome_reconciliation')",
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
        "'confirmation.attestation','outcome.reconciliation')",
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
        "'outcome.disposition','confirmation.attestation',"
        "'outcome.reconciliation')",
        schema=_SCHEMA,
    )

    op.create_table(
        "outcome_reconciliation",
        sa.Column("reconciliation_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("outcome_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "outcome_disposition_material_state_ref",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column("purpose_code", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "reconciliation_ref",
            name=op.f("pk_outcome_reconciliation"),
        ),
        sa.CheckConstraint(
            "uuid_extract_version(reconciliation_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_outcome_reconciliation_uuidv7"),
        ),
        sa.CheckConstraint(
            _CODE_CONTRACT.format(column="purpose_code"),
            name=op.f("ck_outcome_reconciliation_purpose"),
        ),
        sa.UniqueConstraint(
            "outcome_disposition_material_state_ref",
            "purpose_code",
            name=op.f("uq_outcome_reconciliation_target_purpose"),
        ),
        sa.UniqueConstraint(
            "reconciliation_ref",
            "outcome_ref",
            name=op.f("uq_outcome_reconciliation_ref_outcome"),
        ),
        sa.UniqueConstraint(
            "reconciliation_ref",
            "outcome_ref",
            "outcome_disposition_material_state_ref",
            "purpose_code",
            name=op.f("uq_outcome_reconciliation_identity"),
        ),
        sa.ForeignKeyConstraint(
            ["outcome_ref"],
            [f"{_SCHEMA}.outcome.outcome_ref"],
            name=op.f("fk_outcome_reconciliation_outcome"),
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
            name=op.f("fk_outcome_reconciliation_outcome_disposition"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_outcome_reconciliation_outcome_ref",
        "outcome_reconciliation",
        ["outcome_ref"],
        unique=False,
        schema=_SCHEMA,
    )

    op.create_table(
        "outcome_reconciliation_state",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("reconciliation_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("action_code", sa.Text(), nullable=False),
        sa.Column("resolved_by_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_outcome_reconciliation_state"),
        ),
        sa.UniqueConstraint(
            "reconciliation_ref",
            "material_state_ref",
            name=op.f("uq_outcome_reconciliation_state_owner_material"),
        ),
        sa.CheckConstraint(
            "action_code IN ('unresolved','select','accept_multiple','defer','escalate')",
            name=op.f("ck_outcome_reconciliation_state_action"),
        ),
        sa.ForeignKeyConstraint(
            ["material_state_ref"],
            [f"{_SCHEMA}.material_state_address.material_state_ref"],
            name=op.f("fk_outcome_reconciliation_state_address"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["reconciliation_ref"],
            [f"{_SCHEMA}.outcome_reconciliation.reconciliation_ref"],
            name=op.f("fk_outcome_reconciliation_state_owner"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["resolved_by_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name=op.f("fk_outcome_reconciliation_state_resolver"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_outcome_reconciliation_state_owner",
        "outcome_reconciliation_state",
        ["reconciliation_ref"],
        unique=False,
        schema=_SCHEMA,
    )

    op.create_table(
        "outcome_reconciliation_evidence",
        sa.Column("reconciliation_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "reconciliation_material_state_ref",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column("confirmation_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "confirmation_attestation_material_state_ref",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column("role_code", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "reconciliation_material_state_ref",
            "confirmation_ref",
            "confirmation_attestation_material_state_ref",
            name=op.f("pk_outcome_reconciliation_evidence"),
        ),
        sa.CheckConstraint(
            "role_code IN ('considered','selected')",
            name=op.f("ck_outcome_reconciliation_evidence_role"),
        ),
        sa.ForeignKeyConstraint(
            ["reconciliation_ref", "reconciliation_material_state_ref"],
            [
                f"{_SCHEMA}.outcome_reconciliation_state.reconciliation_ref",
                f"{_SCHEMA}.outcome_reconciliation_state.material_state_ref",
            ],
            name=op.f("fk_outcome_reconciliation_evidence_state"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["confirmation_ref", "confirmation_attestation_material_state_ref"],
            [
                f"{_SCHEMA}.confirmation_attestation_state.confirmation_ref",
                f"{_SCHEMA}.confirmation_attestation_state.material_state_ref",
            ],
            name=op.f("fk_outcome_reconciliation_evidence_confirmation_state"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_outcome_reconciliation_evidence_confirmation_state",
        "outcome_reconciliation_evidence",
        ["confirmation_attestation_material_state_ref"],
        unique=False,
        schema=_SCHEMA,
    )

    op.create_table(
        "outcome_reconciliation_current_history",
        sa.Column("reconciliation_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("current_from_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_until_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "reconciliation_ref",
            "current_from_at",
            name=op.f("pk_outcome_reconciliation_current_history"),
        ),
        sa.CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at>current_from_at))",
            name=op.f("ck_outcome_reconciliation_current_history_interval"),
        ),
        sa.ForeignKeyConstraint(
            ["reconciliation_ref", "material_state_ref"],
            [
                f"{_SCHEMA}.outcome_reconciliation_state.reconciliation_ref",
                f"{_SCHEMA}.outcome_reconciliation_state.material_state_ref",
            ],
            name=op.f("fk_outcome_reconciliation_current_history_state"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ux_outcome_reconciliation_current_history_open",
        "outcome_reconciliation_current_history",
        ["reconciliation_ref"],
        unique=True,
        schema=_SCHEMA,
        postgresql_where=sa.text("current_until_at IS NULL"),
    )
    op.create_index(
        "ix_outcome_reconciliation_current_history_material_state_ref",
        "outcome_reconciliation_current_history",
        ["material_state_ref"],
        unique=False,
        schema=_SCHEMA,
    )

    op.create_table(
        "outcome_reconciliation_operation",
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("reconciliation_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("outcome_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "outcome_disposition_material_state_ref",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
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
            name=op.f("pk_outcome_reconciliation_operation"),
        ),
        sa.UniqueConstraint(
            "resulting_material_state_ref",
            name=op.f("uq_outcome_reconciliation_operation_resulting_state"),
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f("ck_outcome_reconciliation_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_outcome_reconciliation_operation_fingerprint"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name=op.f("fk_outcome_reconciliation_operation_self_person"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            [
                "reconciliation_ref",
                "outcome_ref",
                "outcome_disposition_material_state_ref",
                "purpose_code",
            ],
            [
                f"{_SCHEMA}.outcome_reconciliation.reconciliation_ref",
                f"{_SCHEMA}.outcome_reconciliation.outcome_ref",
                f"{_SCHEMA}.outcome_reconciliation.outcome_disposition_material_state_ref",
                f"{_SCHEMA}.outcome_reconciliation.purpose_code",
            ],
            name=op.f("fk_outcome_reconciliation_operation_identity"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["reconciliation_ref", "expected_material_state_ref"],
            [
                f"{_SCHEMA}.outcome_reconciliation_state.reconciliation_ref",
                f"{_SCHEMA}.outcome_reconciliation_state.material_state_ref",
            ],
            name=op.f("fk_outcome_reconciliation_operation_expected_state"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["reconciliation_ref", "resulting_material_state_ref"],
            [
                f"{_SCHEMA}.outcome_reconciliation_state.reconciliation_ref",
                f"{_SCHEMA}.outcome_reconciliation_state.material_state_ref",
            ],
            name=op.f("fk_outcome_reconciliation_operation_resulting_state"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        schema=_SCHEMA,
    )

    _sql(
        r"""
CREATE FUNCTION dante._reconciliation_outcome_owned(
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
CREATE FUNCTION dante.record_self_outcome_reconciliation(
  requested_self_person_ref uuid,
  requested_operation_id text,
  requested_intent_fingerprint text,
  requested_outcome_ref uuid,
  requested_outcome_disposition_material_state_ref uuid,
  requested_reconciliation_ref uuid,
  requested_material_state_ref uuid,
  requested_expected_material_state_ref uuid,
  requested_purpose_code text,
  requested_action_code text,
  requested_confirmation_refs uuid[],
  requested_confirmation_state_refs uuid[],
  requested_evidence_role_codes text[]
) RETURNS TABLE(
  reconciliation_ref uuid,
  outcome_ref uuid,
  outcome_disposition_material_state_ref uuid,
  purpose_code text,
  material_state_ref uuid,
  action_code text,
  resolved_by_person_ref uuid,
  evidence jsonb,
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
  receipt_reconciliation_ref uuid;
  receipt_outcome_ref uuid;
  receipt_outcome_state_ref uuid;
  receipt_state_ref uuid;
  resolved_reconciliation_ref uuid;
  current_reconciliation_state_ref uuid;
  current_from timestamptz;
  recorded_at timestamptz := statement_timestamp();
  evidence_count integer := COALESCE(array_length(requested_confirmation_refs, 1), 0);
  confirmation_state_count integer := COALESCE(array_length(requested_confirmation_state_refs, 1), 0);
  role_count integer := COALESCE(array_length(requested_evidence_role_codes, 1), 0);
  selected_count integer := 0;
  valid_evidence_count integer := 0;
BEGIN
  IF normalized_operation_id='' OR char_length(normalized_operation_id)>200 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_outcome_reconciliation_operation_operation_id',
      MESSAGE='Reconciliation operation id rejected';
  END IF;
  IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_outcome_reconciliation_operation_fingerprint',
      MESSAGE='Reconciliation operation fingerprint rejected';
  END IF;
  IF requested_purpose_code<>btrim(requested_purpose_code)
     OR requested_purpose_code=''
     OR char_length(requested_purpose_code)>120
     OR requested_purpose_code !~ '^[a-z0-9][a-z0-9._:-]*$' THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_outcome_reconciliation_purpose',
      MESSAGE='Reconciliation purpose code rejected';
  END IF;
  IF requested_action_code NOT IN (
       'unresolved','select','accept_multiple','defer','escalate'
     ) THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_outcome_reconciliation_state_action',
      MESSAGE='Reconciliation action rejected';
  END IF;
  IF uuid_extract_version(requested_reconciliation_ref) IS DISTINCT FROM 7
     OR uuid_extract_version(requested_material_state_ref) IS DISTINCT FROM 7 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      MESSAGE='Reconciliation reference rejected';
  END IF;
  IF evidence_count<>confirmation_state_count OR evidence_count<>role_count THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='reconciliation_evidence_shape_invalid',
      MESSAGE='Reconciliation evidence arrays must have equal cardinality';
  END IF;

  IF NOT dante._reconciliation_outcome_owned(
       requested_self_person_ref,
       requested_outcome_ref
     ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='reconciliation_outcome_unavailable',
      MESSAGE='Reconciliation Outcome unavailable';
  END IF;

  IF NOT EXISTS (
    SELECT 1
      FROM dante.outcome_disposition_state AS state
     WHERE state.outcome_ref=requested_outcome_ref
       AND state.material_state_ref=requested_outcome_disposition_material_state_ref
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='reconciliation_outcome_unavailable',
      MESSAGE='Reconciliation Outcome target unavailable';
  END IF;

  IF EXISTS (
    SELECT 1
      FROM unnest(
        requested_confirmation_refs,
        requested_confirmation_state_refs,
        requested_evidence_role_codes
      ) AS item(confirmation_ref, confirmation_state_ref, role_code)
     WHERE item.confirmation_ref IS NULL
        OR item.confirmation_state_ref IS NULL
        OR item.role_code IS NULL
        OR item.role_code NOT IN ('considered','selected')
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_outcome_reconciliation_evidence_role',
      MESSAGE='Reconciliation evidence rejected';
  END IF;

  IF (
    SELECT count(*)
      FROM (
        SELECT item.confirmation_ref, item.confirmation_state_ref
          FROM unnest(
            requested_confirmation_refs,
            requested_confirmation_state_refs,
            requested_evidence_role_codes
          ) AS item(confirmation_ref, confirmation_state_ref, role_code)
         GROUP BY item.confirmation_ref, item.confirmation_state_ref
      ) AS distinct_item
  )<>evidence_count THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='reconciliation_evidence_duplicate',
      MESSAGE='Reconciliation evidence contains duplicates';
  END IF;

  SELECT count(*) FILTER (WHERE item.role_code='selected')
    INTO selected_count
    FROM unnest(
      requested_confirmation_refs,
      requested_confirmation_state_refs,
      requested_evidence_role_codes
    ) AS item(confirmation_ref, confirmation_state_ref, role_code);

  IF (requested_action_code='select' AND selected_count<>1)
     OR (requested_action_code='accept_multiple' AND selected_count<2)
     OR (requested_action_code IN ('unresolved','defer','escalate') AND selected_count<>0) THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='reconciliation_action_evidence_invalid',
      MESSAGE='Reconciliation selected evidence does not match action';
  END IF;

  SELECT count(*)
    INTO valid_evidence_count
    FROM unnest(
      requested_confirmation_refs,
      requested_confirmation_state_refs,
      requested_evidence_role_codes
    ) AS item(confirmation_ref, confirmation_state_ref, role_code)
    JOIN dante.confirmation AS confirmation
      ON confirmation.confirmation_ref=item.confirmation_ref
     AND confirmation.outcome_ref=requested_outcome_ref
     AND confirmation.outcome_disposition_material_state_ref
           =requested_outcome_disposition_material_state_ref
    JOIN dante.confirmation_attestation_state AS state
      ON state.confirmation_ref=item.confirmation_ref
     AND state.material_state_ref=item.confirmation_state_ref;

  IF valid_evidence_count<>evidence_count THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='reconciliation_evidence_unavailable',
      MESSAGE='Reconciliation evidence does not belong to the exact Outcome state';
  END IF;

  PERFORM pg_advisory_xact_lock(
    hashtextextended(
      requested_self_person_ref::text || ':reconciliation-op:' || normalized_operation_id,
      0
    )
  );

  SELECT operation.intent_fingerprint,
         operation.reconciliation_ref,
         operation.outcome_ref,
         operation.outcome_disposition_material_state_ref,
         operation.resulting_material_state_ref
    INTO existing_fingerprint,
         receipt_reconciliation_ref,
         receipt_outcome_ref,
         receipt_outcome_state_ref,
         receipt_state_ref
    FROM dante.outcome_reconciliation_operation AS operation
   WHERE operation.self_person_ref=requested_self_person_ref
     AND operation.operation_id=normalized_operation_id;

  IF FOUND THEN
    IF existing_fingerprint<>requested_intent_fingerprint
       OR receipt_outcome_ref<>requested_outcome_ref
       OR receipt_outcome_state_ref<>requested_outcome_disposition_material_state_ref THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        CONSTRAINT='reconciliation_operation_reused',
        MESSAGE='Reconciliation operation id reused with different intent';
    END IF;
    RETURN QUERY
    SELECT owner.reconciliation_ref,
           owner.outcome_ref,
           owner.outcome_disposition_material_state_ref,
           owner.purpose_code,
           state.material_state_ref,
           state.action_code,
           state.resolved_by_person_ref,
           COALESCE((
             SELECT jsonb_agg(
               jsonb_build_object(
                 'confirmation_ref', evidence_row.confirmation_ref,
                 'confirmation_attestation_material_state_ref',
                   evidence_row.confirmation_attestation_material_state_ref,
                 'role_code', evidence_row.role_code
               ) ORDER BY evidence_row.confirmation_ref,
                          evidence_row.confirmation_attestation_material_state_ref
             )
               FROM dante.outcome_reconciliation_evidence AS evidence_row
              WHERE evidence_row.reconciliation_ref=owner.reconciliation_ref
                AND evidence_row.reconciliation_material_state_ref=state.material_state_ref
           ), '[]'::jsonb),
           true
      FROM dante.outcome_reconciliation AS owner
      JOIN dante.outcome_reconciliation_state AS state
        ON state.reconciliation_ref=owner.reconciliation_ref
     WHERE owner.reconciliation_ref=receipt_reconciliation_ref
       AND state.material_state_ref=receipt_state_ref;
    RETURN;
  END IF;

  PERFORM pg_advisory_xact_lock(
    hashtextextended(
      'reconciliation-target:'
      || requested_outcome_disposition_material_state_ref::text
      || ':'
      || requested_purpose_code,
      0
    )
  );

  SELECT owner.reconciliation_ref
    INTO resolved_reconciliation_ref
    FROM dante.outcome_reconciliation AS owner
   WHERE owner.outcome_disposition_material_state_ref
           =requested_outcome_disposition_material_state_ref
     AND owner.purpose_code=requested_purpose_code
   LIMIT 1;

  IF resolved_reconciliation_ref IS NULL THEN
    IF requested_expected_material_state_ref IS NOT NULL THEN
      RAISE EXCEPTION USING ERRCODE='40001',
        CONSTRAINT='reconciliation_current_conflict',
        MESSAGE='Reconciliation expected current state does not exist';
    END IF;

    resolved_reconciliation_ref:=requested_reconciliation_ref;
    INSERT INTO dante.outcome_reconciliation(
      reconciliation_ref,
      outcome_ref,
      outcome_disposition_material_state_ref,
      purpose_code
    ) VALUES (
      resolved_reconciliation_ref,
      requested_outcome_ref,
      requested_outcome_disposition_material_state_ref,
      requested_purpose_code
    );

    INSERT INTO dante.scoped_address(scoped_ref, scoped_family)
    VALUES (resolved_reconciliation_ref, 'outcome_reconciliation');
  ELSE
    SELECT current.material_state_ref,
           history.current_from_at
      INTO current_reconciliation_state_ref, current_from
      FROM dante.scoped_current_material_state AS current
      JOIN dante.outcome_reconciliation_current_history AS history
        ON history.reconciliation_ref=resolved_reconciliation_ref
       AND history.material_state_ref=current.material_state_ref
       AND history.current_until_at IS NULL
     WHERE current.scoped_owner_ref=resolved_reconciliation_ref
       AND current.facet_code='outcome.reconciliation'
     FOR UPDATE OF history;

    IF current_reconciliation_state_ref IS DISTINCT FROM requested_expected_material_state_ref THEN
      RAISE EXCEPTION USING ERRCODE='40001',
        CONSTRAINT='reconciliation_current_conflict',
        MESSAGE='Reconciliation expected current state is stale';
    END IF;
  END IF;

  IF current_from IS NOT NULL AND recorded_at<=current_from THEN
    recorded_at:=current_from + interval '1 microsecond';
  END IF;

  INSERT INTO dante.material_state_address(
    material_state_ref, scoped_owner_ref, facet_code
  ) VALUES (
    requested_material_state_ref,
    resolved_reconciliation_ref,
    'outcome.reconciliation'
  );

  INSERT INTO dante.outcome_reconciliation_state(
    material_state_ref,
    reconciliation_ref,
    action_code,
    resolved_by_person_ref
  ) VALUES (
    requested_material_state_ref,
    resolved_reconciliation_ref,
    requested_action_code,
    requested_self_person_ref
  );

  INSERT INTO dante.outcome_reconciliation_evidence(
    reconciliation_ref,
    reconciliation_material_state_ref,
    confirmation_ref,
    confirmation_attestation_material_state_ref,
    role_code
  )
  SELECT resolved_reconciliation_ref,
         requested_material_state_ref,
         item.confirmation_ref,
         item.confirmation_state_ref,
         item.role_code
    FROM unnest(
      requested_confirmation_refs,
      requested_confirmation_state_refs,
      requested_evidence_role_codes
    ) AS item(confirmation_ref, confirmation_state_ref, role_code);

  IF current_reconciliation_state_ref IS NULL THEN
    INSERT INTO dante.scoped_current_material_state(
      scoped_owner_ref, facet_code, material_state_ref
    ) VALUES (
      resolved_reconciliation_ref,
      'outcome.reconciliation',
      requested_material_state_ref
    );
  ELSE
    UPDATE dante.outcome_reconciliation_current_history
       SET current_until_at=recorded_at
     WHERE outcome_reconciliation_current_history.reconciliation_ref
             =resolved_reconciliation_ref
       AND current_until_at IS NULL;

    UPDATE dante.scoped_current_material_state
       SET material_state_ref=requested_material_state_ref
     WHERE scoped_owner_ref=resolved_reconciliation_ref
       AND facet_code='outcome.reconciliation';
  END IF;

  INSERT INTO dante.outcome_reconciliation_current_history(
    reconciliation_ref, material_state_ref, current_from_at
  ) VALUES (
    resolved_reconciliation_ref,
    requested_material_state_ref,
    recorded_at
  );

  INSERT INTO dante.outcome_reconciliation_operation(
    self_person_ref,
    operation_id,
    intent_fingerprint,
    reconciliation_ref,
    outcome_ref,
    outcome_disposition_material_state_ref,
    purpose_code,
    expected_material_state_ref,
    resulting_material_state_ref,
    created_at
  ) VALUES (
    requested_self_person_ref,
    normalized_operation_id,
    requested_intent_fingerprint,
    resolved_reconciliation_ref,
    requested_outcome_ref,
    requested_outcome_disposition_material_state_ref,
    requested_purpose_code,
    requested_expected_material_state_ref,
    requested_material_state_ref,
    recorded_at
  );

  RETURN QUERY
  SELECT resolved_reconciliation_ref,
         requested_outcome_ref,
         requested_outcome_disposition_material_state_ref,
         requested_purpose_code,
         requested_material_state_ref,
         requested_action_code,
         requested_self_person_ref,
         COALESCE((
           SELECT jsonb_agg(
             jsonb_build_object(
               'confirmation_ref', evidence_row.confirmation_ref,
               'confirmation_attestation_material_state_ref',
                 evidence_row.confirmation_attestation_material_state_ref,
               'role_code', evidence_row.role_code
             ) ORDER BY evidence_row.confirmation_ref,
                        evidence_row.confirmation_attestation_material_state_ref
           )
             FROM dante.outcome_reconciliation_evidence AS evidence_row
            WHERE evidence_row.reconciliation_ref=resolved_reconciliation_ref
              AND evidence_row.reconciliation_material_state_ref=requested_material_state_ref
         ), '[]'::jsonb),
         false;
END;
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.list_self_outcome_reconciliations(
  requested_self_person_ref uuid,
  requested_outcome_ref uuid
) RETURNS TABLE(
  reconciliation_ref uuid,
  outcome_ref uuid,
  outcome_disposition_material_state_ref uuid,
  purpose_code text,
  material_state_ref uuid,
  action_code text,
  resolved_by_person_ref uuid,
  evidence jsonb
)
LANGUAGE plpgsql
SECURITY DEFINER
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
BEGIN
  IF NOT dante._reconciliation_outcome_owned(
       requested_self_person_ref,
       requested_outcome_ref
     ) THEN
    RETURN;
  END IF;

  RETURN QUERY
  SELECT owner.reconciliation_ref,
         owner.outcome_ref,
         owner.outcome_disposition_material_state_ref,
         owner.purpose_code,
         state.material_state_ref,
         state.action_code,
         state.resolved_by_person_ref,
         COALESCE((
           SELECT jsonb_agg(
             jsonb_build_object(
               'confirmation_ref', evidence_row.confirmation_ref,
               'confirmation_attestation_material_state_ref',
                 evidence_row.confirmation_attestation_material_state_ref,
               'role_code', evidence_row.role_code
             ) ORDER BY evidence_row.confirmation_ref,
                        evidence_row.confirmation_attestation_material_state_ref
           )
             FROM dante.outcome_reconciliation_evidence AS evidence_row
            WHERE evidence_row.reconciliation_ref=owner.reconciliation_ref
              AND evidence_row.reconciliation_material_state_ref=state.material_state_ref
         ), '[]'::jsonb)
    FROM dante.outcome_reconciliation AS owner
    JOIN dante.scoped_current_material_state AS current
      ON current.scoped_owner_ref=owner.reconciliation_ref
     AND current.facet_code='outcome.reconciliation'
    JOIN dante.outcome_reconciliation_state AS state
      ON state.reconciliation_ref=owner.reconciliation_ref
     AND state.material_state_ref=current.material_state_ref
   WHERE owner.outcome_ref=requested_outcome_ref
   ORDER BY owner.reconciliation_ref ASC;
END;
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.list_self_outcome_reconciliation_history(
  requested_self_person_ref uuid,
  requested_reconciliation_ref uuid
) RETURNS TABLE(
  reconciliation_ref uuid,
  outcome_ref uuid,
  outcome_disposition_material_state_ref uuid,
  purpose_code text,
  material_state_ref uuid,
  action_code text,
  resolved_by_person_ref uuid,
  evidence jsonb,
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
      FROM dante.outcome_reconciliation AS owner
     WHERE owner.reconciliation_ref=requested_reconciliation_ref
       AND dante._reconciliation_outcome_owned(
         requested_self_person_ref,
         owner.outcome_ref
       )
  ) THEN
    RETURN;
  END IF;

  RETURN QUERY
  SELECT owner.reconciliation_ref,
         owner.outcome_ref,
         owner.outcome_disposition_material_state_ref,
         owner.purpose_code,
         state.material_state_ref,
         state.action_code,
         state.resolved_by_person_ref,
         COALESCE((
           SELECT jsonb_agg(
             jsonb_build_object(
               'confirmation_ref', evidence_row.confirmation_ref,
               'confirmation_attestation_material_state_ref',
                 evidence_row.confirmation_attestation_material_state_ref,
               'role_code', evidence_row.role_code
             ) ORDER BY evidence_row.confirmation_ref,
                        evidence_row.confirmation_attestation_material_state_ref
           )
             FROM dante.outcome_reconciliation_evidence AS evidence_row
            WHERE evidence_row.reconciliation_ref=owner.reconciliation_ref
              AND evidence_row.reconciliation_material_state_ref=state.material_state_ref
         ), '[]'::jsonb),
         history.current_from_at,
         history.current_until_at
    FROM dante.outcome_reconciliation AS owner
    JOIN dante.outcome_reconciliation_current_history AS history
      ON history.reconciliation_ref=owner.reconciliation_ref
    JOIN dante.outcome_reconciliation_state AS state
      ON state.reconciliation_ref=owner.reconciliation_ref
     AND state.material_state_ref=history.material_state_ref
   WHERE owner.reconciliation_ref=requested_reconciliation_ref
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
            SELECT EXISTS (SELECT 1 FROM dante.schedule WHERE schedule_ref=NEW.scoped_ref)
              INTO owner_exists;
        WHEN 'actual' THEN
            SELECT EXISTS (SELECT 1 FROM dante.actual WHERE actual_ref=NEW.scoped_ref)
              INTO owner_exists;
        WHEN 'temporal_constraint' THEN
            SELECT EXISTS (
                SELECT 1 FROM dante.temporal_constraint WHERE constraint_ref=NEW.scoped_ref
            ) INTO owner_exists;
        WHEN 'outcome' THEN
            SELECT EXISTS (SELECT 1 FROM dante.outcome WHERE outcome_ref=NEW.scoped_ref)
              INTO owner_exists;
        WHEN 'confirmation' THEN
            SELECT EXISTS (
                SELECT 1 FROM dante.confirmation WHERE confirmation_ref=NEW.scoped_ref
            ) INTO owner_exists;
        WHEN 'outcome_reconciliation' THEN
            SELECT EXISTS (
                SELECT 1
                  FROM dante.outcome_reconciliation
                 WHERE reconciliation_ref=NEW.scoped_ref
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
    reconciliation_n integer;
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
      (SELECT count(*) FROM dante.confirmation_attestation_state WHERE material_state_ref=state_ref),
      (SELECT count(*) FROM dante.outcome_reconciliation_state WHERE material_state_ref=state_ref)
      INTO schedule_n,movement_n,actual_n,session_n,routine_n,event_n,constraint_n,
           outcome_n,confirmation_n,reconciliation_n;

    IF a.facet_code='temporal_constraint.rule' THEN
        SELECT EXISTS (
            SELECT 1 FROM dante.temporal_constraint_state AS s
            JOIN dante.scoped_address AS x
              ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='temporal_constraint'
            WHERE s.material_state_ref=state_ref
              AND s.constraint_ref=a.scoped_owner_ref AND a.native_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND constraint_n=1
          AND schedule_n+movement_n+actual_n+session_n+routine_n+event_n+
              outcome_n+confirmation_n+reconciliation_n=0;
    ELSIF a.facet_code='schedule.placement' THEN
        SELECT EXISTS (
            SELECT 1 FROM dante.schedule_placement_state AS s
            JOIN dante.scoped_address AS x
              ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='schedule'
            WHERE s.material_state_ref=state_ref
              AND s.schedule_ref=a.scoped_owner_ref AND a.native_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND schedule_n=1
          AND movement_n+actual_n+session_n+routine_n+event_n+constraint_n+
              outcome_n+confirmation_n+reconciliation_n=0;
    ELSIF a.facet_code='schedule.movement_policy' THEN
        SELECT EXISTS (
            SELECT 1 FROM dante.schedule_movement_policy_state AS s
            JOIN dante.scoped_address AS x
              ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='schedule'
            WHERE s.material_state_ref=state_ref
              AND s.schedule_ref=a.scoped_owner_ref AND a.native_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND movement_n=1
          AND schedule_n+actual_n+session_n+routine_n+event_n+constraint_n+
              outcome_n+confirmation_n+reconciliation_n=0;
    ELSIF a.facet_code='actual.realization' THEN
        SELECT EXISTS (
            SELECT 1 FROM dante.actual_realization_state AS s
            JOIN dante.scoped_address AS x
              ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='actual'
            WHERE s.material_state_ref=state_ref
              AND s.actual_ref=a.scoped_owner_ref AND a.native_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND actual_n=1
          AND schedule_n+movement_n+session_n+routine_n+event_n+constraint_n+
              outcome_n+confirmation_n+reconciliation_n=0;
    ELSIF a.facet_code='session.timing' THEN
        SELECT EXISTS (
            SELECT 1 FROM dante.session_timing_state AS s
            JOIN dante.native_address AS x
              ON x.native_ref=a.native_owner_ref AND x.owner_family='session'
            WHERE s.material_state_ref=state_ref
              AND s.session_ref=a.native_owner_ref AND a.scoped_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND session_n=1
          AND schedule_n+movement_n+actual_n+routine_n+event_n+constraint_n+
              outcome_n+confirmation_n+reconciliation_n=0;
    ELSIF a.facet_code='routine.recurrence' THEN
        SELECT EXISTS (
            SELECT 1 FROM dante.routine_recurrence_state AS s
            JOIN dante.native_address AS x
              ON x.native_ref=a.native_owner_ref AND x.owner_family='routine'
            WHERE s.material_state_ref=state_ref
              AND s.routine_ref=a.native_owner_ref AND a.scoped_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND routine_n=1
          AND schedule_n+movement_n+actual_n+session_n+event_n+constraint_n+
              outcome_n+confirmation_n+reconciliation_n=0;
    ELSIF a.facet_code='event.recurrence' THEN
        SELECT EXISTS (
            SELECT 1 FROM dante.event_recurrence_state AS s
            JOIN dante.native_address AS x
              ON x.native_ref=a.native_owner_ref AND x.owner_family='event'
            WHERE s.material_state_ref=state_ref
              AND s.event_ref=a.native_owner_ref AND a.scoped_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND event_n=1
          AND schedule_n+movement_n+actual_n+session_n+routine_n+constraint_n+
              outcome_n+confirmation_n+reconciliation_n=0;
    ELSIF a.facet_code='outcome.disposition' THEN
        SELECT EXISTS (
            SELECT 1 FROM dante.outcome_disposition_state AS s
            JOIN dante.scoped_address AS x
              ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='outcome'
            WHERE s.material_state_ref=state_ref
              AND s.outcome_ref=a.scoped_owner_ref AND a.native_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND outcome_n=1
          AND schedule_n+movement_n+actual_n+session_n+routine_n+event_n+
              constraint_n+confirmation_n+reconciliation_n=0;
    ELSIF a.facet_code='confirmation.attestation' THEN
        SELECT EXISTS (
            SELECT 1 FROM dante.confirmation_attestation_state AS s
            JOIN dante.scoped_address AS x
              ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='confirmation'
            WHERE s.material_state_ref=state_ref
              AND s.confirmation_ref=a.scoped_owner_ref AND a.native_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND confirmation_n=1
          AND schedule_n+movement_n+actual_n+session_n+routine_n+event_n+
              constraint_n+outcome_n+reconciliation_n=0;
    ELSIF a.facet_code='outcome.reconciliation' THEN
        SELECT EXISTS (
            SELECT 1 FROM dante.outcome_reconciliation_state AS s
            JOIN dante.scoped_address AS x
              ON x.scoped_ref=a.scoped_owner_ref
             AND x.scoped_family='outcome_reconciliation'
            WHERE s.material_state_ref=state_ref
              AND s.reconciliation_ref=a.scoped_owner_ref
              AND a.native_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND reconciliation_n=1
          AND schedule_n+movement_n+actual_n+session_n+routine_n+event_n+
              constraint_n+outcome_n+confirmation_n=0;
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
        "outcome_reconciliation",
        "outcome_reconciliation_state",
        "outcome_reconciliation_evidence",
        "outcome_reconciliation_current_history",
        "outcome_reconciliation_operation",
    ):
        _sql(
            "REVOKE ALL PRIVILEGES ON TABLE "
            f"{_SCHEMA}.{table_name} "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )


def downgrade() -> None:
    raise RuntimeError(
        "B10-D reconciliation capability downgrade is intentionally refused; "
        "use a separately reviewed forward migration"
    )
