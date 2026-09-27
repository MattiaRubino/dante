"""B11-C: self-personal configuration for an exact-start accepted Schedule.

Revision ID: 20260927_86
Revises: 20260927_85

Reminder state is append-only. Its due time is derived from the currently
accepted Schedule placement; this migration adds no notification delivery.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260927_86"
down_revision: str | None = "20260927_85"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def _function_definition(name: str) -> str:
    definition = op.get_bind().exec_driver_sql(
        """SELECT pg_get_functiondef(routine.oid)
             FROM pg_proc AS routine
             JOIN pg_namespace AS namespace ON namespace.oid=routine.pronamespace
            WHERE namespace.nspname='dante' AND routine.proname=%s
              AND routine.pronargs=0""",
        (name,),
    ).scalar_one()
    if not isinstance(definition, str):
        raise RuntimeError(f"B11-C integrity function {name} is unavailable")
    return definition


def _replace_once(definition: str, old: str, new: str, *, label: str) -> str:
    if definition.count(old) != 1:
        raise RuntimeError(f"B11-C {label} integrity patch point did not match once")
    return definition.replace(old, new)


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
        "'outcome_reconciliation','schedule_reminder')",
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
        "'confirmation.attestation','outcome.reconciliation',"
        "'schedule_reminder.configuration')",
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
        "'outcome.reconciliation','schedule_reminder.configuration')",
        schema=_SCHEMA,
    )

    op.create_table(
        "schedule_reminder",
        sa.Column("reminder_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("schedule_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("reminder_ref", name=op.f("pk_schedule_reminder")),
        sa.UniqueConstraint(
            "self_person_ref", "schedule_ref", name=op.f("uq_schedule_reminder_self_schedule")
        ),
        sa.CheckConstraint(
            "uuid_extract_version(reminder_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_schedule_reminder_uuidv7"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"], [f"{_SCHEMA}.person.person_ref"],
            name=op.f("fk_schedule_reminder_person"),
        ),
        sa.ForeignKeyConstraint(
            ["schedule_ref"], [f"{_SCHEMA}.schedule.schedule_ref"],
            name=op.f("fk_schedule_reminder_schedule"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_schedule_reminder_schedule", "schedule_reminder", ["schedule_ref"], schema=_SCHEMA
    )

    op.create_table(
        "schedule_reminder_configuration_state",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("reminder_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("lead_minutes", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref", name=op.f("pk_schedule_reminder_configuration_state")
        ),
        sa.UniqueConstraint(
            "reminder_ref", "material_state_ref",
            name=op.f("uq_schedule_reminder_configuration_state_owner_state"),
        ),
        sa.CheckConstraint(
            "lead_minutes BETWEEN 0 AND 10080",
            name=op.f("ck_schedule_reminder_configuration_state_lead"),
        ),
        sa.ForeignKeyConstraint(
            ["material_state_ref"], [f"{_SCHEMA}.material_state_address.material_state_ref"],
            name=op.f("fk_schedule_reminder_configuration_state_address"),
        ),
        sa.ForeignKeyConstraint(
            ["reminder_ref"], [f"{_SCHEMA}.schedule_reminder.reminder_ref"],
            name=op.f("fk_schedule_reminder_configuration_state_reminder"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_schedule_reminder_configuration_state_reminder",
        "schedule_reminder_configuration_state", ["reminder_ref"], schema=_SCHEMA,
    )

    op.create_table(
        "schedule_reminder_current_history",
        sa.Column("reminder_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("current_from_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_until_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "reminder_ref", "current_from_at",
            name=op.f("pk_schedule_reminder_current_history"),
        ),
        sa.CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at>current_from_at))",
            name=op.f("ck_schedule_reminder_current_history_interval"),
        ),
        sa.ForeignKeyConstraint(
            ["reminder_ref", "material_state_ref"],
            [f"{_SCHEMA}.schedule_reminder_configuration_state.reminder_ref",
             f"{_SCHEMA}.schedule_reminder_configuration_state.material_state_ref"],
            name=op.f("fk_schedule_reminder_current_history_state"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ux_schedule_reminder_current_history_open",
        "schedule_reminder_current_history", ["reminder_ref"], unique=True,
        schema=_SCHEMA, postgresql_where=sa.text("current_until_at IS NULL"),
    )
    op.create_index(
        "ix_schedule_reminder_current_history_state",
        "schedule_reminder_current_history", ["material_state_ref"], schema=_SCHEMA,
    )

    op.create_table(
        "schedule_reminder_operation",
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("reminder_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("schedule_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("expected_material_state_ref", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("resulting_material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref", "operation_id", name=op.f("pk_schedule_reminder_operation")
        ),
        sa.UniqueConstraint(
            "resulting_material_state_ref", name=op.f("uq_schedule_reminder_operation_state")
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f("ck_schedule_reminder_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_schedule_reminder_operation_fingerprint"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"], [f"{_SCHEMA}.person.person_ref"],
            name=op.f("fk_schedule_reminder_operation_person"),
        ),
        sa.ForeignKeyConstraint(
            ["reminder_ref"], [f"{_SCHEMA}.schedule_reminder.reminder_ref"],
            name=op.f("fk_schedule_reminder_operation_reminder"),
        ),
        sa.ForeignKeyConstraint(
            ["schedule_ref"], [f"{_SCHEMA}.schedule.schedule_ref"],
            name=op.f("fk_schedule_reminder_operation_schedule"),
        ),
        sa.ForeignKeyConstraint(
            ["reminder_ref", "resulting_material_state_ref"],
            [f"{_SCHEMA}.schedule_reminder_configuration_state.reminder_ref",
             f"{_SCHEMA}.schedule_reminder_configuration_state.material_state_ref"],
            name=op.f("fk_schedule_reminder_operation_result_state"),
        ),
        schema=_SCHEMA,
    )

    _sql(
        r"""
CREATE FUNCTION dante._self_schedule_reminder_owned(
  requested_self_person_ref uuid, requested_schedule_ref uuid
) RETURNS boolean
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT EXISTS (
    SELECT 1 FROM dante.schedule AS schedule_row
    JOIN dante.native_address AS address
      ON address.native_ref=schedule_row.subject_native_ref
    WHERE schedule_row.schedule_ref=requested_schedule_ref
      AND (
        (address.owner_family='activity' AND EXISTS (
          SELECT 1 FROM dante.activity_intention AS intention
          WHERE intention.activity_ref=schedule_row.subject_native_ref
            AND intention.self_person_ref=requested_self_person_ref
        )) OR
        (address.owner_family='event' AND EXISTS (
          SELECT 1 FROM dante.event_expectation AS expectation
          WHERE expectation.event_ref=schedule_row.subject_native_ref
            AND expectation.self_person_ref=requested_self_person_ref
        )) OR
        (address.owner_family='occurrence' AND EXISTS (
          SELECT 1 FROM dante.occurrence_generation AS generation
          WHERE generation.occurrence_ref=schedule_row.subject_native_ref
            AND (
              EXISTS (SELECT 1 FROM dante.routine_intention AS routine
                WHERE routine.routine_ref=generation.source_native_ref
                  AND routine.self_person_ref=requested_self_person_ref)
              OR EXISTS (SELECT 1 FROM dante.event_expectation AS expectation
                WHERE expectation.event_ref=generation.source_native_ref
                  AND expectation.self_person_ref=requested_self_person_ref)
            )
        ))
      )
  );
$function$
"""
    )
    _sql(
        r"""
CREATE FUNCTION dante._schedule_reminder_start(requested_schedule_ref uuid)
RETURNS timestamptz
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT CASE
           WHEN placement.temporal_form_code='absolute'
             AND absolute_state.extent_code='interval' THEN absolute_state.starts_at
           WHEN placement.temporal_form_code='named_zone_local'
             AND named_state.extent_code='interval' THEN named_state.resolved_start_at
           ELSE NULL
         END
    FROM dante.schedule_current_placement AS current
    JOIN dante.schedule_placement_state AS placement
      ON placement.schedule_ref=requested_schedule_ref
     AND placement.material_state_ref=current.material_state_ref
    LEFT JOIN dante.schedule_placement_absolute_state AS absolute_state
      ON absolute_state.material_state_ref=placement.material_state_ref
    LEFT JOIN dante.schedule_placement_named_zone_state AS named_state
      ON named_state.material_state_ref=placement.material_state_ref
   WHERE current.scoped_owner_ref=requested_schedule_ref;
$function$
"""
    )
    _sql(
        r"""
CREATE FUNCTION dante.get_self_schedule_reminder(
  requested_self_person_ref uuid, requested_schedule_ref uuid
) RETURNS TABLE(
  reminder_ref uuid, schedule_ref uuid, material_state_ref uuid,
  enabled boolean, lead_minutes integer, schedule_starts_at timestamptz,
  due_at timestamptz, disposition_code text
)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT owner.reminder_ref,owner.schedule_ref,state.material_state_ref,
         state.enabled,state.lead_minutes,start_at.value,
         CASE WHEN state.enabled AND start_at.value IS NOT NULL
           THEN start_at.value - make_interval(mins=>state.lead_minutes)
           ELSE NULL END,
         CASE WHEN NOT state.enabled OR start_at.value IS NULL THEN 'unavailable'
              WHEN start_at.value - make_interval(mins=>state.lead_minutes)
                     <= statement_timestamp() THEN 'due'
              ELSE 'pending' END
    FROM dante.schedule_reminder AS owner
    JOIN dante.scoped_current_material_state AS current
      ON current.scoped_owner_ref=owner.reminder_ref
     AND current.facet_code='schedule_reminder.configuration'
    JOIN dante.schedule_reminder_configuration_state AS state
      ON state.reminder_ref=owner.reminder_ref
     AND state.material_state_ref=current.material_state_ref
    JOIN dante.schedule_reminder_current_history AS history
      ON history.reminder_ref=owner.reminder_ref
     AND history.material_state_ref=current.material_state_ref
     AND history.current_until_at IS NULL
    CROSS JOIN LATERAL (SELECT dante._schedule_reminder_start(owner.schedule_ref) AS value)
      AS start_at
   WHERE owner.self_person_ref=requested_self_person_ref
     AND owner.schedule_ref=requested_schedule_ref
     AND dante._self_schedule_reminder_owned(requested_self_person_ref,owner.schedule_ref);
$function$
"""
    )
    _sql(
        r"""
CREATE FUNCTION dante.configure_self_schedule_reminder(
  requested_self_person_ref uuid, requested_operation_id text,
  requested_intent_fingerprint text, requested_schedule_ref uuid,
  requested_expected_material_state_ref uuid, requested_reminder_ref uuid,
  requested_material_state_ref uuid, requested_enabled boolean,
  requested_lead_minutes integer
) RETURNS TABLE(
  reminder_ref uuid, schedule_ref uuid, material_state_ref uuid,
  enabled boolean, lead_minutes integer, schedule_starts_at timestamptz,
  due_at timestamptz, disposition_code text, replayed boolean
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
DECLARE
  normalized_operation_id text := btrim(requested_operation_id);
  recorded_at timestamptz := statement_timestamp();
  existing_fingerprint text;
  existing_schedule_ref uuid;
  existing_reminder_ref uuid;
  existing_state_ref uuid;
  current_reminder_ref uuid;
  current_state_ref uuid;
  current_from timestamptz;
BEGIN
  IF normalized_operation_id IS NULL OR normalized_operation_id=''
     OR char_length(normalized_operation_id)>200
     OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$'
     OR requested_enabled IS NULL OR requested_lead_minutes NOT BETWEEN 0 AND 10080
     OR uuid_extract_version(requested_reminder_ref) IS DISTINCT FROM 7
     OR uuid_extract_version(requested_material_state_ref) IS DISTINCT FROM 7 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='schedule_reminder_input', MESSAGE='Reminder configuration rejected';
  END IF;

  PERFORM pg_advisory_xact_lock(hashtextextended(
    'schedule_reminder:'||requested_self_person_ref::text||':'||requested_schedule_ref::text,0
  ));
  PERFORM pg_advisory_xact_lock(hashtextextended(
    'schedule_reminder_operation:'||requested_self_person_ref::text||':'||normalized_operation_id,0
  ));

  SELECT operation.intent_fingerprint,operation.schedule_ref,
         operation.reminder_ref,operation.resulting_material_state_ref
    INTO existing_fingerprint,existing_schedule_ref,existing_reminder_ref,existing_state_ref
    FROM dante.schedule_reminder_operation AS operation
   WHERE operation.self_person_ref=requested_self_person_ref
     AND operation.operation_id=normalized_operation_id;
  IF FOUND THEN
    IF existing_fingerprint<>requested_intent_fingerprint
       OR existing_schedule_ref<>requested_schedule_ref THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        CONSTRAINT='schedule_reminder_operation_reused',
        MESSAGE='Reminder operation id reused for different intent';
    END IF;
    RETURN QUERY SELECT prior.reminder_ref,prior_owner.schedule_ref,
      prior.material_state_ref,prior.enabled,prior.lead_minutes,
      dante._schedule_reminder_start(prior_owner.schedule_ref),
      CASE WHEN prior.enabled AND dante._schedule_reminder_start(prior_owner.schedule_ref) IS NOT NULL
        THEN dante._schedule_reminder_start(prior_owner.schedule_ref)
             - make_interval(mins=>prior.lead_minutes) ELSE NULL END,
      CASE WHEN NOT prior.enabled OR dante._schedule_reminder_start(prior_owner.schedule_ref) IS NULL
             THEN 'unavailable'::text
           WHEN dante._schedule_reminder_start(prior_owner.schedule_ref)
                - make_interval(mins=>prior.lead_minutes) <= statement_timestamp()
             THEN 'due'::text ELSE 'pending'::text END,
      true
      FROM dante.schedule_reminder AS prior_owner
      JOIN dante.schedule_reminder_configuration_state AS prior
        ON prior.reminder_ref=prior_owner.reminder_ref
      WHERE prior_owner.reminder_ref=existing_reminder_ref
        AND prior_owner.schedule_ref=existing_schedule_ref
        AND prior.material_state_ref=existing_state_ref;
    IF NOT FOUND THEN
      RAISE EXCEPTION USING ERRCODE='XX001', MESSAGE='Reminder operation lost canonical state';
    END IF;
    RETURN;
  END IF;

  IF NOT dante._self_schedule_reminder_owned(requested_self_person_ref,requested_schedule_ref)
     OR dante._schedule_reminder_start(requested_schedule_ref) IS NULL THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='schedule_reminder_schedule_unavailable',
      MESSAGE='Exact-start self Schedule unavailable for Reminder';
  END IF;

  SELECT owner.reminder_ref INTO current_reminder_ref
    FROM dante.schedule_reminder AS owner
   WHERE owner.self_person_ref=requested_self_person_ref
     AND owner.schedule_ref=requested_schedule_ref;

  IF current_reminder_ref IS NULL THEN
    IF requested_expected_material_state_ref IS NOT NULL THEN
      RAISE EXCEPTION USING ERRCODE='40001',
        CONSTRAINT='schedule_reminder_current_conflict',
        MESSAGE='Reminder expected state does not exist';
    END IF;
    current_reminder_ref:=requested_reminder_ref;
    INSERT INTO dante.schedule_reminder(reminder_ref,self_person_ref,schedule_ref)
    VALUES (current_reminder_ref,requested_self_person_ref,requested_schedule_ref);
    INSERT INTO dante.scoped_address(scoped_ref,scoped_family)
    VALUES (current_reminder_ref,'schedule_reminder');
  ELSE
    SELECT current.material_state_ref,history.current_from_at
      INTO current_state_ref,current_from
      FROM dante.scoped_current_material_state AS current
      JOIN dante.schedule_reminder_current_history AS history
        ON history.reminder_ref=current_reminder_ref
       AND history.material_state_ref=current.material_state_ref
       AND history.current_until_at IS NULL
     WHERE current.scoped_owner_ref=current_reminder_ref
       AND current.facet_code='schedule_reminder.configuration'
     FOR UPDATE OF history;
    IF current_state_ref IS DISTINCT FROM requested_expected_material_state_ref THEN
      RAISE EXCEPTION USING ERRCODE='40001',
        CONSTRAINT='schedule_reminder_current_conflict',
        MESSAGE='Reminder expected current state is stale';
    END IF;
  END IF;

  IF current_from IS NOT NULL AND recorded_at<=current_from THEN
    recorded_at:=current_from + interval '1 microsecond';
  END IF;
  INSERT INTO dante.material_state_address(
    material_state_ref,scoped_owner_ref,facet_code
  ) VALUES (
    requested_material_state_ref,current_reminder_ref,'schedule_reminder.configuration'
  );
  INSERT INTO dante.schedule_reminder_configuration_state(
    material_state_ref,reminder_ref,enabled,lead_minutes
  ) VALUES (
    requested_material_state_ref,current_reminder_ref,requested_enabled,requested_lead_minutes
  );

  IF current_state_ref IS NULL THEN
    INSERT INTO dante.scoped_current_material_state(
      scoped_owner_ref,facet_code,material_state_ref
    ) VALUES (current_reminder_ref,'schedule_reminder.configuration',requested_material_state_ref);
  ELSE
    UPDATE dante.schedule_reminder_current_history
       SET current_until_at=recorded_at
     WHERE schedule_reminder_current_history.reminder_ref=current_reminder_ref
       AND current_until_at IS NULL;
    UPDATE dante.scoped_current_material_state
       SET material_state_ref=requested_material_state_ref
     WHERE scoped_owner_ref=current_reminder_ref
       AND facet_code='schedule_reminder.configuration';
  END IF;
  INSERT INTO dante.schedule_reminder_current_history(
    reminder_ref,material_state_ref,current_from_at
  ) VALUES (current_reminder_ref,requested_material_state_ref,recorded_at);

  INSERT INTO dante.schedule_reminder_operation(
    self_person_ref,operation_id,intent_fingerprint,reminder_ref,schedule_ref,
    expected_material_state_ref,resulting_material_state_ref,created_at
  ) VALUES (
    requested_self_person_ref,normalized_operation_id,requested_intent_fingerprint,
    current_reminder_ref,requested_schedule_ref,requested_expected_material_state_ref,
    requested_material_state_ref,recorded_at
  );

  RETURN QUERY SELECT result.reminder_ref,result.schedule_ref,result.material_state_ref,
    result.enabled,result.lead_minutes,result.schedule_starts_at,result.due_at,
    result.disposition_code,false
    FROM dante.get_self_schedule_reminder(
      requested_self_person_ref,requested_schedule_ref
    ) AS result;
END;
$function$
"""
    )

    owner_definition = _replace_once(
        _function_definition("enforce_scoped_address_owner"),
        "        ELSE\n            owner_exists := false;",
        """        WHEN 'schedule_reminder' THEN
            SELECT EXISTS (
                SELECT 1 FROM dante.schedule_reminder
                 WHERE reminder_ref=NEW.scoped_ref
            ) INTO owner_exists;
        ELSE
            owner_exists := false;""",
        label="scoped owner",
    )
    _sql(owner_definition.replace("%", "%%"))

    totality_definition = _replace_once(
        _function_definition("enforce_material_state_totality"),
        "    IF a.facet_code='temporal_constraint.rule' THEN",
        """    IF a.facet_code='schedule_reminder.configuration' THEN
        SELECT EXISTS (
            SELECT 1 FROM dante.schedule_reminder_configuration_state AS s
            JOIN dante.scoped_address AS x
              ON x.scoped_ref=a.scoped_owner_ref
             AND x.scoped_family='schedule_reminder'
            WHERE s.material_state_ref=state_ref
              AND s.reminder_ref=a.scoped_owner_ref
              AND a.native_owner_ref IS NULL
        ) INTO owner_ok;
        owner_ok := owner_ok AND (
            SELECT count(*) FROM dante.schedule_reminder_configuration_state
             WHERE material_state_ref=state_ref
        )=1 AND (
            (SELECT count(*) FROM dante.schedule_placement_state WHERE material_state_ref=state_ref)
          + (SELECT count(*) FROM dante.schedule_movement_policy_state WHERE material_state_ref=state_ref)
          + (SELECT count(*) FROM dante.actual_realization_state WHERE material_state_ref=state_ref)
          + (SELECT count(*) FROM dante.session_timing_state WHERE material_state_ref=state_ref)
          + (SELECT count(*) FROM dante.routine_recurrence_state WHERE material_state_ref=state_ref)
          + (SELECT count(*) FROM dante.event_recurrence_state WHERE material_state_ref=state_ref)
          + (SELECT count(*) FROM dante.temporal_constraint_state WHERE material_state_ref=state_ref)
          + (SELECT count(*) FROM dante.outcome_disposition_state WHERE material_state_ref=state_ref)
          + (SELECT count(*) FROM dante.confirmation_attestation_state WHERE material_state_ref=state_ref)
          + (SELECT count(*) FROM dante.outcome_reconciliation_state WHERE material_state_ref=state_ref)
        )=0;
        IF NOT owner_ok THEN
            RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME,
              TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
              MESSAGE='Reminder MaterialState totality rejected';
        END IF;
        IF TG_OP='DELETE' THEN RETURN OLD; END IF;
        RETURN NEW;
    END IF;

    IF a.facet_code='temporal_constraint.rule' THEN""",
        label="material state totality",
    )
    _sql(totality_definition.replace("%", "%%"))

    _sql(
        """CREATE CONSTRAINT TRIGGER ctrg_schedule_reminder_configuration_state_totality
           AFTER INSERT OR UPDATE OR DELETE
           ON dante.schedule_reminder_configuration_state
           DEFERRABLE INITIALLY DEFERRED FOR EACH ROW
           EXECUTE FUNCTION dante.enforce_material_state_totality()"""
    )

    for signature in (
        "dante._self_schedule_reminder_owned(uuid,uuid)",
        "dante._schedule_reminder_start(uuid)",
        "dante.get_self_schedule_reminder(uuid,uuid)",
        "dante.configure_self_schedule_reminder(uuid,text,text,uuid,uuid,uuid,uuid,boolean,integer)",
        "dante.enforce_scoped_address_owner()",
        "dante.enforce_material_state_totality()",
    ):
        _sql(f"ALTER FUNCTION {signature} OWNER TO {_OWNER}")
        _sql(f"REVOKE ALL PRIVILEGES ON FUNCTION {signature} FROM PUBLIC,{_MIGRATOR},{_RUNTIME}")
    for signature in (
        "dante.get_self_schedule_reminder(uuid,uuid)",
        "dante.configure_self_schedule_reminder(uuid,text,text,uuid,uuid,uuid,uuid,boolean,integer)",
    ):
        _sql(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}")

    for table in (
        "schedule_reminder", "schedule_reminder_configuration_state",
        "schedule_reminder_current_history", "schedule_reminder_operation",
    ):
        _sql(f"ALTER TABLE dante.{table} OWNER TO {_OWNER}")
        _sql(f"REVOKE ALL PRIVILEGES ON TABLE dante.{table} FROM PUBLIC,{_MIGRATOR},{_RUNTIME}")


def downgrade() -> None:
    raise RuntimeError("B11-C migration is forward-only.")
