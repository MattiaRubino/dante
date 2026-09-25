"""B10-A: guarded self-scoped Actual realization authoring and reads.

Revision ID: 20260925_70
Revises: 20260925_69

The CP6 Actual owner/state/timing/basis/current-history substrate is already
canonical. This revision does not remodel Actual. It activates one bounded,
idempotent, self-scoped capability over that substrate.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260925_70"
down_revision: str | None = "20260925_69"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def upgrade() -> None:
    """Activate Actual realization without changing the CP6 ontology."""
    op.create_table(
        "actual_realization_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("actual_ref", sa.Uuid(), nullable=False),
        sa.Column("subject_native_ref", sa.Uuid(), nullable=False),
        sa.Column("expected_material_state_ref", sa.Uuid(), nullable=True),
        sa.Column("resulting_material_state_ref", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f("ck_actual_realization_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_actual_realization_operation_fingerprint"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name=op.f("fk_actual_realization_operation_self_person_ref_person"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["actual_ref"],
            [f"{_SCHEMA}.actual.actual_ref"],
            name=op.f("fk_actual_realization_operation_actual_ref_actual"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["subject_native_ref"],
            [f"{_SCHEMA}.native_address.native_ref"],
            name=op.f("fk_actual_realization_operation_subject_native_ref_native_address"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["resulting_material_state_ref"],
            [f"{_SCHEMA}.actual_realization_state.material_state_ref"],
            name=op.f("fk_actual_realization_operation_resulting_state"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            name=op.f("pk_actual_realization_operation"),
        ),
        sa.UniqueConstraint(
            "resulting_material_state_ref",
            name=op.f("uq_actual_realization_operation_resulting_state"),
        ),
        schema=_SCHEMA,
    )

    _sql(
        r"""
CREATE FUNCTION dante._actual_subject_owned(
  requested_self_person_ref uuid,
  requested_subject_native_ref uuid
) RETURNS boolean
LANGUAGE sql
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT EXISTS (
    SELECT 1
      FROM dante.activity_intention AS activity
     WHERE activity.activity_ref=requested_subject_native_ref
       AND activity.self_person_ref=requested_self_person_ref
  ) OR EXISTS (
    SELECT 1
      FROM dante.event_expectation AS event
     WHERE event.event_ref=requested_subject_native_ref
       AND event.self_person_ref=requested_self_person_ref
  ) OR EXISTS (
    SELECT 1
      FROM dante.occurrence_generation AS generation
     WHERE generation.occurrence_ref=requested_subject_native_ref
       AND (
         EXISTS (
           SELECT 1
             FROM dante.routine_intention AS routine
            WHERE routine.routine_ref=generation.source_native_ref
              AND routine.self_person_ref=requested_self_person_ref
         ) OR EXISTS (
           SELECT 1
             FROM dante.event_expectation AS source_event
            WHERE source_event.event_ref=generation.source_native_ref
              AND source_event.self_person_ref=requested_self_person_ref
         )
       )
  );
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.record_self_actual_realization(
  requested_self_person_ref uuid,
  requested_operation_id text,
  requested_intent_fingerprint text,
  requested_actual_ref uuid,
  requested_material_state_ref uuid,
  requested_subject_native_ref uuid,
  requested_expected_material_state_ref uuid,
  requested_realization_occurred boolean,
  requested_extent_code text,
  requested_started_at timestamptz,
  requested_ended_at timestamptz,
  requested_session_refs uuid[],
  requested_session_timing_material_state_refs uuid[]
) RETURNS TABLE(
  actual_ref uuid,
  subject_native_ref uuid,
  material_state_ref uuid,
  realization_occurred boolean,
  extent_code text,
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
  receipt_actual_ref uuid;
  receipt_subject_ref uuid;
  receipt_state_ref uuid;
  resolved_actual_ref uuid;
  current_state_ref uuid;
  current_from timestamptz;
  recorded_at timestamptz := statement_timestamp();
  matching_actual_count integer := 0;
  basis_count integer := COALESCE(cardinality(requested_session_refs), 0);
  timing_basis_count integer := COALESCE(cardinality(requested_session_timing_material_state_refs), 0);
  basis_index integer;
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM dante.person AS person
     WHERE person.person_ref=requested_self_person_ref
  ) OR NOT dante._actual_subject_owned(
    requested_self_person_ref, requested_subject_native_ref
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='actual_subject_unavailable',
      MESSAGE='Actual subject unavailable';
  END IF;

  IF normalized_operation_id='' OR char_length(normalized_operation_id)>200 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_actual_realization_operation_operation_id',
      MESSAGE='Actual operation id rejected';
  END IF;
  IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='ck_actual_realization_operation_fingerprint',
      MESSAGE='Actual operation fingerprint rejected';
  END IF;
  IF uuid_extract_version(requested_actual_ref) IS DISTINCT FROM 7
     OR uuid_extract_version(requested_material_state_ref) IS DISTINCT FROM 7 THEN
    RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Actual reference rejected';
  END IF;

  IF basis_count<>timing_basis_count THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='actual_session_basis_pairing',
      MESSAGE='Actual Session basis arrays must have equal cardinality';
  END IF;

  IF requested_realization_occurred IS NOT TRUE THEN
    IF requested_extent_code IS NOT NULL OR requested_started_at IS NOT NULL
       OR requested_ended_at IS NOT NULL OR basis_count<>0 THEN
      RAISE EXCEPTION USING ERRCODE='23514',
        CONSTRAINT='actual_non_realization_payload',
        MESSAGE='Known non-realization cannot carry timing or Session bases';
    END IF;
  ELSE
    IF requested_extent_code IS NULL THEN
      IF requested_started_at IS NOT NULL OR requested_ended_at IS NOT NULL THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='actual_realization_timing_shape',
          MESSAGE='Actual timing extent is required when timing is supplied';
      END IF;
    ELSIF requested_extent_code IN ('instant','start_only') THEN
      IF requested_started_at IS NULL OR requested_ended_at IS NOT NULL
         OR NOT isfinite(requested_started_at) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='actual_realization_timing_shape',
          MESSAGE='Actual timing payload rejected';
      END IF;
    ELSIF requested_extent_code='interval' THEN
      IF requested_started_at IS NULL OR requested_ended_at IS NULL
         OR NOT isfinite(requested_started_at) OR NOT isfinite(requested_ended_at)
         OR requested_ended_at<=requested_started_at THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='actual_realization_timing_shape',
          MESSAGE='Actual timing interval rejected';
      END IF;
    ELSE
      RAISE EXCEPTION USING ERRCODE='23514',
        CONSTRAINT='actual_realization_timing_shape',
        MESSAGE='Actual timing extent rejected';
    END IF;
  END IF;

  PERFORM pg_advisory_xact_lock(
    hashtextextended(requested_self_person_ref::text || ':actual-op:' || normalized_operation_id, 0)
  );

  SELECT operation.intent_fingerprint,
         operation.actual_ref,
         operation.subject_native_ref,
         operation.resulting_material_state_ref
    INTO existing_fingerprint, receipt_actual_ref, receipt_subject_ref, receipt_state_ref
    FROM dante.actual_realization_operation AS operation
   WHERE operation.self_person_ref=requested_self_person_ref
     AND operation.operation_id=normalized_operation_id;

  IF FOUND THEN
    IF existing_fingerprint<>requested_intent_fingerprint
       OR receipt_subject_ref<>requested_subject_native_ref THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        CONSTRAINT='actual_operation_reused',
        MESSAGE='Actual operation id reused with different intent';
    END IF;
    RETURN QUERY
    SELECT state.actual_ref,
           owner.subject_native_ref,
           state.material_state_ref,
           state.realization_occurred,
           timing.extent_code,
           timing.started_at,
           timing.ended_at,
           true
      FROM dante.actual_realization_state AS state
      JOIN dante.actual AS owner ON owner.actual_ref=state.actual_ref
      LEFT JOIN dante.actual_realization_timing AS timing
        ON timing.material_state_ref=state.material_state_ref
     WHERE state.actual_ref=receipt_actual_ref
       AND state.material_state_ref=receipt_state_ref;
    RETURN;
  END IF;

  PERFORM pg_advisory_xact_lock(
    hashtextextended('actual-subject:' || requested_subject_native_ref::text, 0)
  );

  SELECT count(*) INTO matching_actual_count
    FROM dante.actual AS owner
   WHERE owner.subject_native_ref=requested_subject_native_ref;
  IF matching_actual_count>1 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='actual_subject_ambiguous',
      MESSAGE='Actual subject has more than one realization owner';
  END IF;

  SELECT owner.actual_ref INTO resolved_actual_ref
    FROM dante.actual AS owner
   WHERE owner.subject_native_ref=requested_subject_native_ref
   LIMIT 1;

  IF resolved_actual_ref IS NULL THEN
    IF requested_expected_material_state_ref IS NOT NULL THEN
      RAISE EXCEPTION USING ERRCODE='40001',
        CONSTRAINT='actual_current_conflict',
        MESSAGE='Actual expected current state does not exist';
    END IF;
    resolved_actual_ref:=requested_actual_ref;
    INSERT INTO dante.scoped_address(scoped_ref, scoped_family)
    VALUES (resolved_actual_ref, 'actual');
    INSERT INTO dante.actual(actual_ref, subject_native_ref)
    VALUES (resolved_actual_ref, requested_subject_native_ref);
  ELSE
    SELECT current.material_state_ref, history.current_from_at
      INTO current_state_ref, current_from
      FROM dante.scoped_current_material_state AS current
      JOIN dante.actual_realization_current_history AS history
        ON history.actual_ref=resolved_actual_ref
       AND history.material_state_ref=current.material_state_ref
       AND history.current_until_at IS NULL
     WHERE current.scoped_owner_ref=resolved_actual_ref
       AND current.facet_code='actual.realization'
     FOR UPDATE OF history;

    IF current_state_ref IS DISTINCT FROM requested_expected_material_state_ref THEN
      RAISE EXCEPTION USING ERRCODE='40001',
        CONSTRAINT='actual_current_conflict',
        MESSAGE='Actual expected current state is stale';
    END IF;
  END IF;

  IF current_from IS NOT NULL AND recorded_at<=current_from THEN
    recorded_at:=current_from + interval '1 microsecond';
  END IF;

  IF basis_count>0 THEN
    FOR basis_index IN 1..basis_count LOOP
      IF NOT EXISTS (
        SELECT 1
          FROM dante.session_execution_subject AS subject
          JOIN dante.session_timing_state AS timing_state
            ON timing_state.session_ref=subject.session_ref
           AND timing_state.material_state_ref=requested_session_timing_material_state_refs[basis_index]
         WHERE subject.session_ref=requested_session_refs[basis_index]
           AND subject.subject_native_ref=requested_subject_native_ref
      ) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='actual_session_basis_subject',
          MESSAGE='Actual Session basis is not exact evidence for this subject';
      END IF;
    END LOOP;
  END IF;

  INSERT INTO dante.material_state_address(
    material_state_ref, scoped_owner_ref, facet_code
  ) VALUES (
    requested_material_state_ref, resolved_actual_ref, 'actual.realization'
  );
  INSERT INTO dante.actual_realization_state(
    material_state_ref, actual_ref, realization_occurred
  ) VALUES (
    requested_material_state_ref, resolved_actual_ref, requested_realization_occurred
  );

  IF requested_extent_code IS NOT NULL THEN
    INSERT INTO dante.actual_realization_timing(
      material_state_ref, extent_code, started_at, ended_at
    ) VALUES (
      requested_material_state_ref, requested_extent_code,
      requested_started_at, requested_ended_at
    );
  END IF;

  IF basis_count>0 THEN
    FOR basis_index IN 1..basis_count LOOP
      INSERT INTO dante.actual_realization_session_basis(
        actual_material_state_ref, session_ref, session_timing_material_state_ref
      ) VALUES (
        requested_material_state_ref,
        requested_session_refs[basis_index],
        requested_session_timing_material_state_refs[basis_index]
      );
    END LOOP;
  END IF;

  IF current_state_ref IS NULL THEN
    INSERT INTO dante.scoped_current_material_state(
      scoped_owner_ref, facet_code, material_state_ref
    ) VALUES (
      resolved_actual_ref, 'actual.realization', requested_material_state_ref
    );
  ELSE
    UPDATE dante.actual_realization_current_history
       SET current_until_at=recorded_at
     WHERE actual_ref=resolved_actual_ref
       AND current_until_at IS NULL;
    UPDATE dante.scoped_current_material_state
       SET material_state_ref=requested_material_state_ref
     WHERE scoped_owner_ref=resolved_actual_ref
       AND facet_code='actual.realization';
  END IF;

  INSERT INTO dante.actual_realization_current_history(
    actual_ref, material_state_ref, current_from_at
  ) VALUES (
    resolved_actual_ref, requested_material_state_ref, recorded_at
  );

  INSERT INTO dante.actual_realization_operation(
    self_person_ref, operation_id, intent_fingerprint,
    actual_ref, subject_native_ref, expected_material_state_ref,
    resulting_material_state_ref, created_at
  ) VALUES (
    requested_self_person_ref, normalized_operation_id, requested_intent_fingerprint,
    resolved_actual_ref, requested_subject_native_ref, requested_expected_material_state_ref,
    requested_material_state_ref, recorded_at
  );

  RETURN QUERY
  SELECT resolved_actual_ref,
         requested_subject_native_ref,
         requested_material_state_ref,
         requested_realization_occurred,
         requested_extent_code,
         requested_started_at,
         requested_ended_at,
         false;
END;
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.get_self_subject_actual(
  requested_self_person_ref uuid,
  requested_subject_native_ref uuid
) RETURNS TABLE(
  actual_ref uuid,
  subject_native_ref uuid,
  material_state_ref uuid,
  realization_occurred boolean,
  extent_code text,
  started_at timestamptz,
  ended_at timestamptz
)
LANGUAGE plpgsql
SECURITY DEFINER
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
DECLARE
  matching_actual_count integer;
BEGIN
  IF NOT dante._actual_subject_owned(
    requested_self_person_ref, requested_subject_native_ref
  ) THEN
    RETURN;
  END IF;
  SELECT count(*) INTO matching_actual_count
    FROM dante.actual AS owner
   WHERE owner.subject_native_ref=requested_subject_native_ref;
  IF matching_actual_count>1 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='actual_subject_ambiguous',
      MESSAGE='Actual subject has more than one realization owner';
  END IF;
  RETURN QUERY
  SELECT owner.actual_ref,
         owner.subject_native_ref,
         state.material_state_ref,
         state.realization_occurred,
         timing.extent_code,
         timing.started_at,
         timing.ended_at
    FROM dante.actual AS owner
    JOIN dante.actual_current_realization AS current
      ON current.scoped_owner_ref=owner.actual_ref
    JOIN dante.actual_realization_state AS state
      ON state.actual_ref=owner.actual_ref
     AND state.material_state_ref=current.material_state_ref
    LEFT JOIN dante.actual_realization_timing AS timing
      ON timing.material_state_ref=state.material_state_ref
   WHERE owner.subject_native_ref=requested_subject_native_ref;
END;
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.list_self_actual_history(
  requested_self_person_ref uuid,
  requested_actual_ref uuid
) RETURNS TABLE(
  actual_ref uuid,
  subject_native_ref uuid,
  material_state_ref uuid,
  realization_occurred boolean,
  extent_code text,
  started_at timestamptz,
  ended_at timestamptz,
  current_from_at timestamptz,
  current_until_at timestamptz
)
LANGUAGE sql
SECURITY DEFINER
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT owner.actual_ref,
         owner.subject_native_ref,
         state.material_state_ref,
         state.realization_occurred,
         timing.extent_code,
         timing.started_at,
         timing.ended_at,
         history.current_from_at,
         history.current_until_at
    FROM dante.actual AS owner
    JOIN dante.actual_realization_state AS state
      ON state.actual_ref=owner.actual_ref
    JOIN dante.actual_realization_current_history AS history
      ON history.actual_ref=owner.actual_ref
     AND history.material_state_ref=state.material_state_ref
    LEFT JOIN dante.actual_realization_timing AS timing
      ON timing.material_state_ref=state.material_state_ref
   WHERE owner.actual_ref=requested_actual_ref
     AND dante._actual_subject_owned(
       requested_self_person_ref, owner.subject_native_ref
     )
   ORDER BY history.current_from_at DESC;
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.list_self_actual_session_bases(
  requested_self_person_ref uuid,
  requested_actual_ref uuid,
  requested_material_state_ref uuid
) RETURNS TABLE(
  session_ref uuid,
  session_timing_material_state_ref uuid
)
LANGUAGE sql
SECURITY DEFINER
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT basis.session_ref, basis.session_timing_material_state_ref
    FROM dante.actual AS owner
    JOIN dante.actual_realization_state AS state
      ON state.actual_ref=owner.actual_ref
    JOIN dante.actual_realization_session_basis AS basis
      ON basis.actual_material_state_ref=state.material_state_ref
   WHERE owner.actual_ref=requested_actual_ref
     AND state.material_state_ref=requested_material_state_ref
     AND dante._actual_subject_owned(
       requested_self_person_ref, owner.subject_native_ref
     )
   ORDER BY basis.session_ref;
$function$
"""
    )

    # The public capability owns consequential Actual writes. Keep raw Actual
    # mutation unavailable to the runtime role; existing CP6 reads remain valid.
    for table in (
        "actual",
        "actual_realization_state",
        "actual_realization_timing",
        "actual_realization_session_basis",
        "actual_realization_current_history",
        "actual_realization_operation",
    ):
        _sql(f"REVOKE INSERT, UPDATE, DELETE ON TABLE dante.{table} FROM {_RUNTIME}")
    _sql("REVOKE INSERT, UPDATE, DELETE ON TABLE dante.actual_current_realization FROM dante_runtime")

    signatures = (
        "dante._actual_subject_owned(uuid,uuid)",
        "dante.record_self_actual_realization(uuid,text,text,uuid,uuid,uuid,uuid,boolean,text,timestamptz,timestamptz,uuid[],uuid[])",
        "dante.get_self_subject_actual(uuid,uuid)",
        "dante.list_self_actual_history(uuid,uuid)",
        "dante.list_self_actual_session_bases(uuid,uuid,uuid)",
    )
    for signature in signatures:
        _sql(f"ALTER FUNCTION {signature} OWNER TO {_OWNER}")
        _sql(f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}")
    for signature in signatures[1:]:
        _sql(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}")

    _sql("ALTER TABLE dante.actual_realization_operation OWNER TO dante_owner")
    _sql("REVOKE ALL ON TABLE dante.actual_realization_operation FROM PUBLIC, dante_runtime, dante_migrator")
    _sql("GRANT SELECT ON TABLE dante.actual_realization_operation TO dante_migrator")


def downgrade() -> None:
    """Refuse destructive rollback of a published capability migration."""
    raise RuntimeError(
        "B10-A Actual realization capability downgrade is intentionally refused; "
        "use a separately reviewed forward migration"
    )
