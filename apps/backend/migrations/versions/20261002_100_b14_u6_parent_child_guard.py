"""B14-U6: accepted parent child admission and explicit Actual acknowledgement."""

import re
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261002_100"
down_revision: str | None = "20261002_99"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def upgrade() -> None:
    op.create_table(
        "activity_decomposition_policy",
        sa.Column("activity_ref", sa.Uuid(), nullable=False),
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("activity_ref", name="pk_activity_decomposition_policy"),
        sa.ForeignKeyConstraint(
            ["activity_ref"], ["dante.activity_intention.activity_ref"],
            name="fk_activity_decomposition_policy_activity",
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_activity_decomposition_policy_person",
        ),
        schema="dante",
    )
    op.create_index(
        "ix_activity_decomposition_policy_self", "activity_decomposition_policy",
        ["self_person_ref"], schema="dante",
    )
    op.create_table(
        "activity_decomposition_policy_state",
        sa.Column("state_ref", sa.Uuid(), nullable=False),
        sa.Column("activity_ref", sa.Uuid(), nullable=False),
        sa.Column("mode_code", sa.Text(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("state_ref", name="pk_activity_decomposition_policy_state"),
        sa.UniqueConstraint(
            "activity_ref", "state_ref", name="uq_activity_decomposition_policy_state_owner",
        ),
        sa.CheckConstraint(
            "uuid_extract_version(state_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        sa.CheckConstraint(
            "mode_code IN ('none','confirm','block')",
            name="mode",
        ),
        sa.CheckConstraint(
            "isfinite(recorded_at)", name="recorded_at",
        ),
        sa.ForeignKeyConstraint(
            ["activity_ref"], ["dante.activity_decomposition_policy.activity_ref"],
            name="fk_activity_decomposition_policy_state_owner",
        ),
        schema="dante",
    )
    op.create_index(
        "ix_activity_decomposition_policy_state_owner", "activity_decomposition_policy_state",
        ["activity_ref"], schema="dante",
    )
    op.create_table(
        "activity_decomposition_policy_current_history",
        sa.Column("activity_ref", sa.Uuid(), nullable=False),
        sa.Column("state_ref", sa.Uuid(), nullable=False),
        sa.Column("current_from_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_until_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "activity_ref", "current_from_at",
            name="pk_activity_decomposition_policy_current_history",
        ),
        sa.CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at>current_from_at))",
            name="interval",
        ),
        sa.ForeignKeyConstraint(
            ["activity_ref", "state_ref"],
            ["dante.activity_decomposition_policy_state.activity_ref",
             "dante.activity_decomposition_policy_state.state_ref"],
            name="fk_activity_decomposition_policy_current_history_state",
        ),
        schema="dante",
    )
    op.create_index(
        "ux_activity_decomposition_policy_current_history_open",
        "activity_decomposition_policy_current_history", ["activity_ref"],
        unique=True, schema="dante",
        postgresql_where=sa.text("current_until_at IS NULL"),
    )
    op.create_index(
        "ix_activity_decomposition_policy_current_history_state",
        "activity_decomposition_policy_current_history", ["state_ref"], schema="dante",
    )
    op.create_table(
        "activity_decomposition_policy_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("activity_ref", sa.Uuid(), nullable=False),
        sa.Column("state_ref", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref", "operation_id", name="pk_activity_decomposition_policy_operation",
        ),
        sa.UniqueConstraint(
            "state_ref", name="uq_activity_decomposition_policy_operation_state",
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND char_length(operation_id) BETWEEN 1 AND 200",
            name="id",
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name="fingerprint",
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_activity_decomposition_policy_operation_person",
        ),
        sa.ForeignKeyConstraint(
            ["activity_ref", "state_ref"],
            ["dante.activity_decomposition_policy_state.activity_ref",
             "dante.activity_decomposition_policy_state.state_ref"],
            name="fk_activity_decomposition_policy_operation_state",
        ),
        schema="dante",
    )
    op.create_table(
        "activity_parent_actual_acknowledgement",
        sa.Column("material_state_ref", sa.Uuid(), nullable=False),
        sa.Column("activity_ref", sa.Uuid(), nullable=False),
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("acknowledged_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref", name="pk_activity_parent_actual_acknowledgement"
        ),
        sa.CheckConstraint(
            "uuid_extract_version(material_state_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        sa.ForeignKeyConstraint(
            ["activity_ref"], ["dante.activity_intention.activity_ref"],
            name="fk_activity_parent_actual_acknowledgement_activity",
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_activity_parent_actual_acknowledgement_person",
        ),
        schema="dante",
    )
    op.create_index(
        "ix_activity_parent_actual_acknowledgement_activity",
        "activity_parent_actual_acknowledgement", ["activity_ref"], schema="dante",
    )

    _sql("""
CREATE FUNCTION dante.get_self_activity_decomposition_policy(
    requested_self_person_ref uuid, requested_activity_ref uuid
) RETURNS TABLE(state_ref uuid, mode_code text, current_from_at timestamptz)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
    SELECT history.state_ref,
           COALESCE(state.mode_code,'none') AS mode_code,
           history.current_from_at
      FROM dante.activity_intention AS activity
 LEFT JOIN dante.activity_decomposition_policy_current_history AS history
        ON history.activity_ref=activity.activity_ref
       AND history.current_until_at IS NULL
 LEFT JOIN dante.activity_decomposition_policy_state AS state
        ON state.activity_ref=activity.activity_ref
       AND state.state_ref=history.state_ref
     WHERE activity.activity_ref=requested_activity_ref
       AND activity.self_person_ref=requested_self_person_ref
$function$;
""")
    _sql("""
CREATE FUNCTION dante.set_self_activity_decomposition_policy(
    requested_self_person_ref uuid, requested_operation_id text,
    requested_intent_fingerprint text, requested_activity_ref uuid,
    requested_state_ref uuid, requested_mode_code text,
    requested_expected_state_ref uuid
) RETURNS TABLE(state_ref uuid, mode_code text, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
DECLARE
    prior record;
    current_state uuid;
    previous_from timestamptz;
    accepted_at timestamptz;
BEGIN
    IF requested_operation_id IS NULL OR requested_operation_id<>btrim(requested_operation_id)
       OR char_length(requested_operation_id) NOT BETWEEN 1 AND 200
       OR requested_intent_fingerprint IS NULL
       OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$'
       OR requested_mode_code IS NULL
       OR requested_mode_code NOT IN ('none','confirm','block')
       OR uuid_extract_version(requested_state_ref) IS DISTINCT FROM 7 THEN
        RAISE EXCEPTION USING ERRCODE='23514',
            CONSTRAINT='activity_decomposition_policy_invalid',
            MESSAGE='Activity execution policy command rejected';
    END IF;

    -- One Activity lock serializes the absent-owner case as well as corrections.
    PERFORM 1 FROM dante.activity_intention AS activity
     WHERE activity.activity_ref=requested_activity_ref
       AND activity.self_person_ref=requested_self_person_ref FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='activity_decomposition_policy_owner_unavailable',
            MESSAGE='Activity is not owned by this self';
    END IF;

    SELECT * INTO prior FROM dante.activity_decomposition_policy_operation AS operation
     WHERE operation.self_person_ref=requested_self_person_ref
       AND operation.operation_id=requested_operation_id;
    IF FOUND THEN
        IF prior.intent_fingerprint IS DISTINCT FROM requested_intent_fingerprint
           OR prior.activity_ref IS DISTINCT FROM requested_activity_ref THEN
            RAISE EXCEPTION USING ERRCODE='23505',
                CONSTRAINT='activity_decomposition_policy_operation_reused',
                MESSAGE='Activity execution policy operation was reused';
        END IF;
        RETURN QUERY SELECT prior.state_ref, state.mode_code, true
          FROM dante.activity_decomposition_policy_state AS state
         WHERE state.state_ref=prior.state_ref;
        RETURN;
    END IF;

    SELECT history.state_ref, history.current_from_at
      INTO current_state, previous_from
      FROM dante.activity_decomposition_policy_current_history AS history
     WHERE history.activity_ref=requested_activity_ref
       AND history.current_until_at IS NULL;
    IF current_state IS DISTINCT FROM requested_expected_state_ref THEN
        RAISE EXCEPTION USING ERRCODE='40001',
            CONSTRAINT='activity_decomposition_policy_current_conflict',
            MESSAGE='Activity execution policy state changed';
    END IF;

    accepted_at:=statement_timestamp();
    IF previous_from IS NOT NULL AND accepted_at<=previous_from THEN
        accepted_at:=previous_from + interval '1 microsecond';
    END IF;
    INSERT INTO dante.activity_decomposition_policy(activity_ref,self_person_ref,created_at)
    VALUES(requested_activity_ref,requested_self_person_ref,accepted_at)
    ON CONFLICT (activity_ref) DO NOTHING;
    INSERT INTO dante.activity_decomposition_policy_state(
        state_ref,activity_ref,mode_code,recorded_at
    ) VALUES(requested_state_ref,requested_activity_ref,requested_mode_code,accepted_at);
    IF current_state IS NOT NULL THEN
        UPDATE dante.activity_decomposition_policy_current_history AS history
           SET current_until_at=accepted_at
         WHERE history.activity_ref=requested_activity_ref
           AND history.current_until_at IS NULL;
    END IF;
    INSERT INTO dante.activity_decomposition_policy_current_history(
        activity_ref,state_ref,current_from_at,current_until_at
    ) VALUES(requested_activity_ref,requested_state_ref,accepted_at,NULL);
    INSERT INTO dante.activity_decomposition_policy_operation(
        self_person_ref,operation_id,intent_fingerprint,activity_ref,state_ref
    ) VALUES(requested_self_person_ref,requested_operation_id,
             requested_intent_fingerprint,requested_activity_ref,requested_state_ref);
    RETURN QUERY SELECT requested_state_ref, requested_mode_code, false;
END;
$function$;
""")
    for signature in (
        "dante.get_self_activity_decomposition_policy(uuid,uuid)",
        "dante.set_self_activity_decomposition_policy(uuid,text,text,uuid,uuid,text,uuid)",
    ):
        _sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
        _sql(f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator")
        _sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")
    for table in (
        "activity_decomposition_policy", "activity_decomposition_policy_state",
        "activity_decomposition_policy_current_history", "activity_decomposition_policy_operation",
        "activity_parent_actual_acknowledgement",
    ):
        _sql(f"REVOKE ALL ON TABLE dante.{table} FROM PUBLIC,dante_runtime,dante_migrator")

    _sql("""
CREATE FUNCTION dante.acknowledge_self_parent_actual(
    requested_self_person_ref uuid, requested_operation_id text,
    requested_activity_ref uuid, requested_material_state_ref uuid
) RETURNS void LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
BEGIN
    IF requested_operation_id IS NULL OR requested_operation_id<>btrim(requested_operation_id)
       OR char_length(requested_operation_id) NOT BETWEEN 1 AND 200
       OR uuid_extract_version(requested_material_state_ref) IS DISTINCT FROM 7 THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='activity_parent_ack_invalid', MESSAGE='Parent acknowledgement rejected';
    END IF;
    PERFORM pg_advisory_xact_lock(hashtextextended(
        requested_self_person_ref::text || ':actual-op:' || requested_operation_id, 0
    ));
    PERFORM 1 FROM dante.activity_intention AS activity
     WHERE activity.activity_ref=requested_activity_ref
       AND activity.self_person_ref=requested_self_person_ref FOR SHARE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
          CONSTRAINT='activity_parent_ack_owner_unavailable',
          MESSAGE='Activity is not owned by this self';
    END IF;
    -- A replay already has its original receipt; the proposed new state is unused.
    IF EXISTS (SELECT 1 FROM dante.actual_realization_operation AS receipt
        WHERE receipt.self_person_ref=requested_self_person_ref
          AND receipt.operation_id=requested_operation_id) THEN
        RETURN;
    END IF;
    INSERT INTO dante.activity_parent_actual_acknowledgement(
        material_state_ref,activity_ref,self_person_ref,acknowledged_at
    ) VALUES (requested_material_state_ref,requested_activity_ref,
              requested_self_person_ref,statement_timestamp());
END;
$function$;
""")
    signature = "dante.acknowledge_self_parent_actual(uuid,text,uuid,uuid)"
    _sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
    _sql(f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator")
    _sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")

    # The B10 capability is the actual admission point. Patch its exact source
    # forward, after replay detection and before creating a new Actual state.
    definition = op.get_bind().exec_driver_sql(
        "SELECT pg_get_functiondef('dante.record_self_actual_realization("
        "uuid,text,text,text,uuid,uuid,uuid,uuid,boolean,text,"
        "timestamptz,timestamptz,uuid[],uuid[])'::regprocedure)"
    ).scalar_one()
    matches = list(re.finditer(
        r"\bIF\s+current_from\s+IS\s+NOT\s+NULL\s+AND\s+recorded_at\s*<=\s*current_from\s+THEN",
        definition, flags=re.IGNORECASE,
    ))
    if len(matches) != 1:
        raise RuntimeError("B14-U6 B10 parent Actual admission patch point unavailable")
    guard = """
  IF requested_subject_family='activity' AND requested_realization_occurred THEN
    PERFORM 1 FROM dante.activity_intention AS intention
     WHERE intention.activity_ref=requested_subject_native_ref
       AND intention.self_person_ref=requested_self_person_ref FOR SHARE;
    IF EXISTS (
      SELECT 1 FROM dante.activity_decomposition AS relation
      JOIN dante.activity_decomposition_current_history AS history
        ON history.decomposition_ref=relation.decomposition_ref
       AND history.current_until_at IS NULL
      JOIN dante.activity_decomposition_state AS state
        ON state.decomposition_ref=relation.decomposition_ref
       AND state.state_ref=history.state_ref
      LEFT JOIN dante.actual AS child_actual
        ON child_actual.subject_native_ref=relation.child_activity_ref
      LEFT JOIN dante.scoped_current_material_state AS child_current
        ON child_current.scoped_owner_ref=child_actual.actual_ref
       AND child_current.facet_code='actual.realization'
      LEFT JOIN dante.actual_realization_state AS child_state
        ON child_state.actual_ref=child_actual.actual_ref
       AND child_state.material_state_ref=child_current.material_state_ref
     WHERE relation.parent_activity_ref=requested_subject_native_ref
       AND relation.self_person_ref=requested_self_person_ref
       AND state.active AND state.requirement_code='required'
       AND child_state.realization_occurred IS DISTINCT FROM true
    ) THEN
      IF EXISTS (
        SELECT 1 FROM dante.activity_decomposition_policy_current_history AS policy_history
        JOIN dante.activity_decomposition_policy_state AS policy_state
          ON policy_state.activity_ref=policy_history.activity_ref
         AND policy_state.state_ref=policy_history.state_ref
        WHERE policy_history.activity_ref=requested_subject_native_ref
          AND policy_history.current_until_at IS NULL
          AND policy_state.mode_code='block'
      ) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='activity_parent_actual_blocked',
          MESSAGE='Required child Activity has unresolved realization';
      END IF;
      IF EXISTS (
        SELECT 1 FROM dante.activity_decomposition_policy_current_history AS policy_history
        JOIN dante.activity_decomposition_policy_state AS policy_state
          ON policy_state.activity_ref=policy_history.activity_ref
         AND policy_state.state_ref=policy_history.state_ref
        WHERE policy_history.activity_ref=requested_subject_native_ref
          AND policy_history.current_until_at IS NULL
          AND policy_state.mode_code='confirm'
      ) AND NOT EXISTS (
        SELECT 1 FROM dante.activity_parent_actual_acknowledgement AS acknowledgement
        WHERE acknowledgement.material_state_ref=requested_material_state_ref
          AND acknowledgement.activity_ref=requested_subject_native_ref
          AND acknowledgement.self_person_ref=requested_self_person_ref
      ) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='activity_parent_actual_ack_required',
          MESSAGE='Explicit acknowledgement of unresolved required children is required';
      END IF;
    END IF;
  END IF;

"""
    patched = definition[:matches[0].start()] + guard + definition[matches[0].start():]
    op.get_bind().exec_driver_sql(patched.replace("%", "%%"))


def downgrade() -> None:
    raise RuntimeError("B14-U6 parent child guard requires a reviewed forward migration")
