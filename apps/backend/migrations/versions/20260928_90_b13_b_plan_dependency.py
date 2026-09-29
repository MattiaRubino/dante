"""B13-B: qualified, self-owned Plan Dependency and accepted-current history.

The relation is LR-03, scoped to a Plan. Its endpoints retain their Step and
Activity identity. All writes serialize on plan_intention, including the
forward repair of Plan structure replacement below.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260928_90"
down_revision: str | None = "20260928_89"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


_READ_COLUMNS = """
  dependency_ref uuid, plan_ref uuid,
  prerequisite_step_ref uuid, prerequisite_activity_ref uuid,
  dependent_step_ref uuid, dependent_activity_ref uuid,
  purpose_code text, state_ref uuid, qualifier_code text, disposition_code text,
  active boolean, recorded_at timestamptz, evaluation_code text,
  actual_material_state_ref uuid, outcome_material_state_ref uuid
"""

_READ_QUERY = """
  SELECT owner.dependency_ref,owner.plan_ref,
         owner.prerequisite_step_ref,owner.prerequisite_activity_ref,
         owner.dependent_step_ref,owner.dependent_activity_ref,owner.purpose_code,
         state.state_ref,state.qualifier_code,state.disposition_code,
         state.active,state.recorded_at,
         CASE
           WHEN NOT state.active OR current.state_ref IS DISTINCT FROM state.state_ref
             THEN NULL::text
           WHEN state.qualifier_code='actual_occurred' THEN
             CASE WHEN actual_state.material_state_ref IS NULL THEN 'unknown'
                  WHEN actual_state.realization_occurred THEN 'satisfied'
                  ELSE 'unsatisfied' END
           WHEN outcome_state.material_state_ref IS NULL
             OR outcome_state.actual_realization_material_state_ref
                  IS DISTINCT FROM actual_state.material_state_ref THEN 'unknown'
           WHEN outcome_state.disposition_code=state.disposition_code THEN 'satisfied'
           ELSE 'unsatisfied'
         END,
         actual_state.material_state_ref,outcome_state.material_state_ref
    FROM dante.plan_dependency AS owner
    JOIN dante.plan_intention AS plan ON plan.plan_ref=owner.plan_ref
    JOIN dante.plan_dependency_state AS state
      ON state.dependency_ref=owner.dependency_ref
    JOIN dante.plan_dependency_current_state AS current
      ON current.dependency_ref=owner.dependency_ref
    LEFT JOIN LATERAL (
      SELECT actual.actual_ref FROM dante.actual AS actual
       WHERE actual.subject_native_ref=owner.prerequisite_activity_ref
         AND (SELECT count(*) FROM dante.actual AS candidate
               WHERE candidate.subject_native_ref=owner.prerequisite_activity_ref)=1
    ) AS actual_owner ON true
    LEFT JOIN dante.actual_current_realization AS actual_current
      ON actual_current.scoped_owner_ref=actual_owner.actual_ref
    LEFT JOIN dante.actual_realization_state AS actual_state
      ON actual_state.actual_ref=actual_owner.actual_ref
     AND actual_state.material_state_ref=actual_current.material_state_ref
    LEFT JOIN dante.outcome AS outcome_owner
      ON outcome_owner.actual_ref=actual_owner.actual_ref
    LEFT JOIN dante.scoped_current_material_state AS outcome_current
      ON outcome_current.scoped_owner_ref=outcome_owner.outcome_ref
     AND outcome_current.facet_code='outcome.disposition'
    LEFT JOIN dante.outcome_disposition_state AS outcome_state
      ON outcome_state.outcome_ref=outcome_owner.outcome_ref
     AND outcome_state.material_state_ref=outcome_current.material_state_ref
   WHERE plan.self_person_ref=requested_self_person_ref
"""


def upgrade() -> None:
    op.drop_constraint(
        "ck_scoped_address_scoped_family", "scoped_address", schema=_SCHEMA, type_="check"
    )
    op.create_check_constraint(
        "ck_scoped_address_scoped_family",
        "scoped_address",
        "scoped_family IN ("
        "'schedule','actual','temporal_constraint','outcome','confirmation',"
        "'outcome_reconciliation','schedule_reminder','plan_dependency')",
        schema=_SCHEMA,
    )

    op.create_table(
        "plan_dependency",
        sa.Column("dependency_ref", sa.Uuid(), primary_key=True),
        sa.Column("plan_ref", sa.Uuid(), nullable=False),
        sa.Column("prerequisite_step_ref", sa.Uuid(), nullable=False),
        sa.Column("prerequisite_activity_ref", sa.Uuid(), nullable=False),
        sa.Column("dependent_step_ref", sa.Uuid(), nullable=False),
        sa.Column("dependent_activity_ref", sa.Uuid(), nullable=False),
        sa.Column("purpose_code", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "uuid_extract_version(dependency_ref) IS NOT DISTINCT FROM 7",
            name="ck_plan_dependency_uuidv7",
        ),
        sa.CheckConstraint(
            "prerequisite_step_ref<>dependent_step_ref AND "
            "prerequisite_activity_ref<>dependent_activity_ref",
            name="ck_plan_dependency_distinct_endpoints",
        ),
        sa.CheckConstraint(
            "purpose_code='dependent_activity_admissibility'",
            name="ck_plan_dependency_purpose",
        ),
        sa.UniqueConstraint("plan_ref", "dependency_ref", name="uq_plan_dependency_plan"),
        sa.ForeignKeyConstraint(
            ["plan_ref"],
            ["dante.plan_intention.plan_ref"],
            name="fk_plan_dependency_plan",
        ),
        sa.ForeignKeyConstraint(
            ["plan_ref", "prerequisite_step_ref"],
            ["dante.plan_step.plan_ref", "dante.plan_step.step_ref"],
            name="fk_plan_dependency_prerequisite_step",
        ),
        sa.ForeignKeyConstraint(
            ["plan_ref", "dependent_step_ref"],
            ["dante.plan_step.plan_ref", "dante.plan_step.step_ref"],
            name="fk_plan_dependency_dependent_step",
        ),
        sa.ForeignKeyConstraint(
            ["prerequisite_activity_ref"],
            ["dante.activity.activity_ref"],
            name="fk_plan_dependency_prerequisite_activity",
        ),
        sa.ForeignKeyConstraint(
            ["dependent_activity_ref"],
            ["dante.activity.activity_ref"],
            name="fk_plan_dependency_dependent_activity",
        ),
        schema=_SCHEMA,
    )
    op.create_index("ix_plan_dependency_plan", "plan_dependency", ["plan_ref"], schema=_SCHEMA)
    op.create_table(
        "plan_dependency_state",
        sa.Column("state_ref", sa.Uuid(), primary_key=True),
        sa.Column("dependency_ref", sa.Uuid(), nullable=False),
        sa.Column("qualifier_code", sa.Text(), nullable=False),
        sa.Column("disposition_code", sa.Text(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "uuid_extract_version(state_ref) IS NOT DISTINCT FROM 7",
            name="ck_plan_dependency_state_uuidv7",
        ),
        sa.CheckConstraint(
            "(qualifier_code='actual_occurred' AND disposition_code IS NULL) OR "
            "(qualifier_code='outcome_code' AND disposition_code IS NOT NULL AND "
            "disposition_code=btrim(disposition_code) AND "
            "char_length(disposition_code) BETWEEN 1 AND 120 AND "
            "disposition_code ~ '^[a-z0-9][a-z0-9._:-]*$')",
            name="ck_plan_dependency_state_qualifier",
        ),
        sa.UniqueConstraint("dependency_ref", "state_ref", name="uq_plan_dependency_state_owner"),
        sa.ForeignKeyConstraint(
            ["dependency_ref"],
            ["dante.plan_dependency.dependency_ref"],
            name="fk_plan_dependency_state_owner",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_plan_dependency_state_owner",
        "plan_dependency_state",
        ["dependency_ref"],
        schema=_SCHEMA,
    )
    op.create_table(
        "plan_dependency_current_state",
        sa.Column("dependency_ref", sa.Uuid(), primary_key=True),
        sa.Column("state_ref", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dependency_ref", "state_ref"],
            ["dante.plan_dependency_state.dependency_ref", "dante.plan_dependency_state.state_ref"],
            name="fk_plan_dependency_current_state",
        ),
        schema=_SCHEMA,
    )
    op.create_table(
        "plan_dependency_current_history",
        sa.Column("dependency_ref", sa.Uuid(), nullable=False),
        sa.Column("state_ref", sa.Uuid(), nullable=False),
        sa.Column("current_from_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_until_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "dependency_ref",
            "current_from_at",
            name="pk_plan_dependency_current_history",
        ),
        sa.CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at>current_from_at))",
            name="ck_plan_dependency_current_history_interval",
        ),
        sa.ForeignKeyConstraint(
            ["dependency_ref", "state_ref"],
            ["dante.plan_dependency_state.dependency_ref", "dante.plan_dependency_state.state_ref"],
            name="fk_plan_dependency_current_history_state",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ux_plan_dependency_current_history_open",
        "plan_dependency_current_history",
        ["dependency_ref"],
        unique=True,
        schema=_SCHEMA,
        postgresql_where=sa.text("current_until_at IS NULL"),
    )
    op.create_table(
        "plan_dependency_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("dependency_ref", sa.Uuid(), nullable=False),
        sa.Column("state_ref", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref", "operation_id", name="pk_plan_dependency_operation"
        ),
        sa.UniqueConstraint("state_ref", name="uq_plan_dependency_operation_state"),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name="ck_plan_dependency_operation_id",
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name="ck_plan_dependency_operation_fingerprint",
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_plan_dependency_operation_person",
        ),
        sa.ForeignKeyConstraint(
            ["dependency_ref", "state_ref"],
            ["dante.plan_dependency_state.dependency_ref", "dante.plan_dependency_state.state_ref"],
            name="fk_plan_dependency_operation_state",
        ),
        schema=_SCHEMA,
    )

    owner_definition = (
        op.get_bind()
        .exec_driver_sql("""
        SELECT pg_get_functiondef(p.oid) FROM pg_proc AS p
        JOIN pg_namespace AS n ON n.oid=p.pronamespace
        WHERE n.nspname='dante' AND p.proname='enforce_scoped_address_owner'
          AND p.pronargs=0
    """)
        .scalar_one()
    )
    owner_anchor = "        ELSE\n            owner_exists := false;"
    if owner_definition.count(owner_anchor) != 1:
        raise RuntimeError("B13-B scoped owner patch point is unavailable")
    owner_case = """        WHEN 'plan_dependency' THEN
            SELECT EXISTS (
                SELECT 1 FROM dante.plan_dependency
                 WHERE dependency_ref=NEW.scoped_ref
            ) INTO owner_exists;
        ELSE
            owner_exists := false;"""
    _sql(owner_definition.replace(owner_anchor, owner_case).replace("%", "%%"))

    _sql(f"""
CREATE FUNCTION dante.get_self_plan_dependency(
  requested_self_person_ref uuid, requested_plan_ref uuid,
  requested_dependency_ref uuid, requested_state_ref uuid DEFAULT NULL
) RETURNS TABLE({_READ_COLUMNS})
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  {_READ_QUERY}
     AND owner.plan_ref=requested_plan_ref
     AND owner.dependency_ref=requested_dependency_ref
     AND state.state_ref=COALESCE(requested_state_ref,current.state_ref);
$function$
""")
    _sql(f"""
CREATE FUNCTION dante.list_self_plan_dependencies(
  requested_self_person_ref uuid, requested_plan_ref uuid
) RETURNS TABLE({_READ_COLUMNS})
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  {_READ_QUERY}
     AND owner.plan_ref=requested_plan_ref
     AND state.state_ref=current.state_ref
   ORDER BY owner.created_at,owner.dependency_ref;
$function$
""")
    _sql("""
CREATE FUNCTION dante.list_self_plan_dependency_history(
  requested_self_person_ref uuid, requested_plan_ref uuid,
  requested_dependency_ref uuid
) RETURNS TABLE(
  state_ref uuid, qualifier_code text, disposition_code text, active boolean,
  recorded_at timestamptz, current_from_at timestamptz,
  current_until_at timestamptz
) LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT state.state_ref,state.qualifier_code,state.disposition_code,state.active,
         state.recorded_at,history.current_from_at,history.current_until_at
    FROM dante.plan_dependency AS owner
    JOIN dante.plan_intention AS plan ON plan.plan_ref=owner.plan_ref
    JOIN dante.plan_dependency_current_history AS history
      ON history.dependency_ref=owner.dependency_ref
    JOIN dante.plan_dependency_state AS state
      ON state.dependency_ref=owner.dependency_ref
     AND state.state_ref=history.state_ref
   WHERE plan.self_person_ref=requested_self_person_ref
     AND owner.plan_ref=requested_plan_ref
     AND owner.dependency_ref=requested_dependency_ref
   ORDER BY history.current_from_at;
$function$
""")
    _sql("""
CREATE FUNCTION dante.write_self_plan_dependency(
  requested_self_person_ref uuid, requested_operation_id text,
  requested_fingerprint text, requested_plan_ref uuid,
  requested_dependency_ref uuid, requested_expected_state_ref uuid,
  requested_state_ref uuid, requested_prerequisite_step_ref uuid,
  requested_dependent_step_ref uuid, requested_qualifier_code text,
  requested_disposition_code text, requested_active boolean
) RETURNS TABLE(dependency_ref uuid, state_ref uuid, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
DECLARE
  op_id text := btrim(requested_operation_id);
  prior_fingerprint text;
  prior_dependency uuid;
  prior_state uuid;
  existing_plan uuid;
  existing_pre_step uuid;
  existing_dep_step uuid;
  pre_activity uuid;
  dep_activity uuid;
  current_state uuid;
  current_active boolean;
  current_from timestamptz;
  stamp timestamptz := statement_timestamp();
BEGIN
  IF op_id IS NULL OR op_id='' OR char_length(op_id)>200
     OR requested_fingerprint !~ '^[0-9a-f]{64}$'
     OR uuid_extract_version(requested_dependency_ref) IS DISTINCT FROM 7
     OR uuid_extract_version(requested_state_ref) IS DISTINCT FROM 7
     OR requested_prerequisite_step_ref=requested_dependent_step_ref
     OR requested_active IS NULL
     OR NOT (
       (requested_qualifier_code='actual_occurred'
        AND requested_disposition_code IS NULL)
       OR (requested_qualifier_code='outcome_code'
        AND requested_disposition_code IS NOT NULL
        AND requested_disposition_code=btrim(requested_disposition_code)
        AND char_length(requested_disposition_code) BETWEEN 1 AND 120
        AND requested_disposition_code ~ '^[a-z0-9][a-z0-9._:-]*$')
     ) THEN
    RAISE EXCEPTION USING ERRCODE='23514',MESSAGE='Plan Dependency input rejected';
  END IF;
  PERFORM pg_advisory_xact_lock(hashtextextended(
    'plan_dependency_operation:'||requested_self_person_ref::text||':'||op_id,0
  ));
  SELECT receipt.intent_fingerprint,receipt.dependency_ref,receipt.state_ref
    INTO prior_fingerprint,prior_dependency,prior_state
    FROM dante.plan_dependency_operation AS receipt
   WHERE receipt.self_person_ref=requested_self_person_ref
     AND receipt.operation_id=op_id;
  IF FOUND THEN
    IF prior_fingerprint<>requested_fingerprint THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        MESSAGE='Plan Dependency operation id reused with different intent';
    END IF;
    RETURN QUERY SELECT prior_dependency,prior_state,true;
    RETURN;
  END IF;
  PERFORM 1 FROM dante.plan_intention AS plan
   WHERE plan.plan_ref=requested_plan_ref
     AND plan.self_person_ref=requested_self_person_ref FOR UPDATE;
  IF NOT FOUND THEN
    RAISE EXCEPTION USING ERRCODE='23503',MESSAGE='Self Plan unavailable';
  END IF;
  SELECT step.activity_ref INTO pre_activity
    FROM dante.plan_current_work_state AS current
    JOIN dante.plan_step_in_state AS step ON step.state_ref=current.state_ref
   WHERE current.plan_ref=requested_plan_ref
     AND step.plan_ref=requested_plan_ref
     AND step.step_ref=requested_prerequisite_step_ref;
  SELECT step.activity_ref INTO dep_activity
    FROM dante.plan_current_work_state AS current
    JOIN dante.plan_step_in_state AS step ON step.state_ref=current.state_ref
   WHERE current.plan_ref=requested_plan_ref
     AND step.plan_ref=requested_plan_ref
     AND step.step_ref=requested_dependent_step_ref;
  IF pre_activity IS NULL OR dep_activity IS NULL
     OR pre_activity=dep_activity
     OR NOT EXISTS (
       SELECT 1 FROM dante.activity_intention AS activity
        WHERE activity.activity_ref=pre_activity
          AND activity.self_person_ref=requested_self_person_ref
     )
     OR NOT EXISTS (
       SELECT 1 FROM dante.activity_intention AS activity
        WHERE activity.activity_ref=dep_activity
          AND activity.self_person_ref=requested_self_person_ref
     ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      MESSAGE='Plan Dependency endpoints unavailable';
  END IF;
  SELECT owner.plan_ref,owner.prerequisite_step_ref,owner.dependent_step_ref
    INTO existing_plan,existing_pre_step,existing_dep_step
    FROM dante.plan_dependency AS owner
   WHERE owner.dependency_ref=requested_dependency_ref;
  IF requested_expected_state_ref IS NULL THEN
    IF existing_plan IS NOT NULL OR NOT requested_active THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        MESSAGE='Plan Dependency create conflict';
    END IF;
    IF (SELECT count(*) FROM dante.plan_dependency AS owner
         WHERE owner.plan_ref=requested_plan_ref)>=1000 THEN
      RAISE EXCEPTION USING ERRCODE='23514',
        MESSAGE='Plan Dependency limit reached';
    END IF;
  ELSE
    IF existing_plan IS DISTINCT FROM requested_plan_ref
       OR existing_pre_step IS DISTINCT FROM requested_prerequisite_step_ref
       OR existing_dep_step IS DISTINCT FROM requested_dependent_step_ref
       OR NOT EXISTS (
         SELECT 1 FROM dante.plan_dependency AS owner
          WHERE owner.dependency_ref=requested_dependency_ref
            AND owner.prerequisite_activity_ref=pre_activity
            AND owner.dependent_activity_ref=dep_activity
       ) THEN
      RAISE EXCEPTION USING ERRCODE='23503',
        MESSAGE='Plan Dependency binding unavailable';
    END IF;
    SELECT current.state_ref,state.active,history.current_from_at
      INTO current_state,current_active,current_from
      FROM dante.plan_dependency_current_state AS current
      JOIN dante.plan_dependency_state AS state
        ON state.dependency_ref=current.dependency_ref
       AND state.state_ref=current.state_ref
      JOIN dante.plan_dependency_current_history AS history
        ON history.dependency_ref=current.dependency_ref
       AND history.state_ref=current.state_ref
       AND history.current_until_at IS NULL
     WHERE current.dependency_ref=requested_dependency_ref FOR UPDATE OF current,history;
    IF current_state IS DISTINCT FROM requested_expected_state_ref THEN
      RAISE EXCEPTION USING ERRCODE='40001',
        MESSAGE='Plan Dependency current state conflict';
    END IF;
    IF NOT current_active THEN
      RAISE EXCEPTION USING ERRCODE='23514',
        MESSAGE='Retired Plan Dependency cannot be revised';
    END IF;
    IF stamp<=current_from THEN stamp:=current_from+interval '1 microsecond'; END IF;
  END IF;
  IF requested_active AND EXISTS (
    SELECT 1 FROM dante.plan_dependency AS other
    JOIN dante.plan_dependency_current_state AS binding
      ON binding.dependency_ref=other.dependency_ref
    JOIN dante.plan_dependency_state AS state
      ON state.dependency_ref=other.dependency_ref
     AND state.state_ref=binding.state_ref
    WHERE other.plan_ref=requested_plan_ref
      AND other.dependency_ref<>requested_dependency_ref
      AND other.prerequisite_step_ref=requested_prerequisite_step_ref
      AND other.dependent_step_ref=requested_dependent_step_ref
      AND state.active
      AND state.qualifier_code=requested_qualifier_code
      AND state.disposition_code IS NOT DISTINCT FROM requested_disposition_code
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23505',
      MESSAGE='Duplicate active Plan Dependency';
  END IF;
  IF requested_expected_state_ref IS NULL THEN
    INSERT INTO dante.plan_dependency(
      dependency_ref,plan_ref,prerequisite_step_ref,prerequisite_activity_ref,
      dependent_step_ref,dependent_activity_ref,purpose_code,created_at
    ) VALUES (
      requested_dependency_ref,requested_plan_ref,
      requested_prerequisite_step_ref,pre_activity,
      requested_dependent_step_ref,dep_activity,'dependent_activity_admissibility',stamp
    );
    INSERT INTO dante.scoped_address(scoped_ref,scoped_family)
    VALUES(requested_dependency_ref,'plan_dependency');
  ELSE
    UPDATE dante.plan_dependency_current_history AS history
       SET current_until_at=stamp
     WHERE history.dependency_ref=requested_dependency_ref
       AND history.current_until_at IS NULL;
  END IF;
  INSERT INTO dante.plan_dependency_state(
    state_ref,dependency_ref,qualifier_code,disposition_code,active,recorded_at
  ) VALUES (
    requested_state_ref,requested_dependency_ref,
    requested_qualifier_code,requested_disposition_code,requested_active,stamp
  );
  IF requested_expected_state_ref IS NULL THEN
    INSERT INTO dante.plan_dependency_current_state(dependency_ref,state_ref)
    VALUES(requested_dependency_ref,requested_state_ref);
  ELSE
    UPDATE dante.plan_dependency_current_state AS current
       SET state_ref=requested_state_ref
     WHERE current.dependency_ref=requested_dependency_ref;
  END IF;
  INSERT INTO dante.plan_dependency_current_history(
    dependency_ref,state_ref,current_from_at
  ) VALUES(requested_dependency_ref,requested_state_ref,stamp);
  INSERT INTO dante.plan_dependency_operation(
    self_person_ref,operation_id,intent_fingerprint,
    dependency_ref,state_ref,created_at
  ) VALUES (
    requested_self_person_ref,op_id,requested_fingerprint,
    requested_dependency_ref,requested_state_ref,stamp
  );
  RETURN QUERY SELECT requested_dependency_ref,requested_state_ref,false;
END;
$function$
""")

    # Patch the live accepted function, not a published migration. Fail closed
    # if the expected B13-A repair is not installed exactly once.
    definition = (
        op.get_bind()
        .exec_driver_sql("""
        SELECT pg_get_functiondef(p.oid) FROM pg_proc AS p
        JOIN pg_namespace AS n ON n.oid=p.pronamespace
        WHERE n.nspname='dante' AND p.proname='replace_self_plan_work'
          AND oidvectortypes(p.proargtypes)='uuid, text, text, uuid, uuid, uuid, text, jsonb'
    """)
        .scalar_one()
    )
    anchor = "UPDATE dante.plan_current_work_state AS current"
    if definition.count(anchor) != 1:
        raise RuntimeError("B13-B Plan replacement guard patch point is unavailable")
    guard = """
  IF EXISTS (
    SELECT 1 FROM dante.plan_dependency AS relation
    JOIN dante.plan_dependency_current_state AS binding
      ON binding.dependency_ref=relation.dependency_ref
    JOIN dante.plan_dependency_state AS condition
      ON condition.dependency_ref=relation.dependency_ref
     AND condition.state_ref=binding.state_ref
    WHERE relation.plan_ref=requested_plan_ref AND condition.active
      AND (
        NOT EXISTS (
          SELECT 1 FROM dante.plan_step_in_state AS step
          WHERE step.state_ref=requested_state_ref
            AND step.step_ref=relation.prerequisite_step_ref
            AND step.activity_ref=relation.prerequisite_activity_ref
        )
        OR NOT EXISTS (
          SELECT 1 FROM dante.plan_step_in_state AS step
          WHERE step.state_ref=requested_state_ref
            AND step.step_ref=relation.dependent_step_ref
            AND step.activity_ref=relation.dependent_activity_ref
        )
      )
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      MESSAGE='Active Plan Dependency endpoint cannot be removed or relinked';
  END IF;
  """
    _sql(definition.replace(anchor, guard + anchor))

    for name, args in (
        ("get_self_plan_dependency", "uuid,uuid,uuid,uuid"),
        ("list_self_plan_dependencies", "uuid,uuid"),
        ("list_self_plan_dependency_history", "uuid,uuid,uuid"),
        (
            "write_self_plan_dependency",
            "uuid,text,text,uuid,uuid,uuid,uuid,uuid,uuid,text,text,boolean",
        ),
    ):
        _sql(f"ALTER FUNCTION dante.{name}({args}) OWNER TO dante_owner")
        _sql(f"REVOKE ALL ON FUNCTION dante.{name}({args}) FROM PUBLIC,{_RUNTIME},{_MIGRATOR}")
        _sql(f"GRANT EXECUTE ON FUNCTION dante.{name}({args}) TO {_RUNTIME}")
    for name in (
        "plan_dependency",
        "plan_dependency_state",
        "plan_dependency_current_state",
        "plan_dependency_current_history",
        "plan_dependency_operation",
    ):
        _sql(f"ALTER TABLE dante.{name} OWNER TO dante_owner")
        _sql(f"REVOKE ALL ON TABLE dante.{name} FROM PUBLIC,{_RUNTIME},{_MIGRATOR}")


def downgrade() -> None:
    raise RuntimeError("B13-B Plan Dependency is forward-only.")
