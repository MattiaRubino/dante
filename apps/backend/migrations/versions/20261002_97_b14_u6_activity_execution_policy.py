"""B14-U6: explicit, self-scoped Activity Session capture policy.

The policy is independent of B04 Session duration constraints. Its accepted
state is historical; only the guarded capability can change it.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261002_97"
down_revision: str | None = "20261002_96"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def upgrade() -> None:
    op.create_table(
        "activity_execution_policy",
        sa.Column("activity_ref", sa.Uuid(), nullable=False),
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("activity_ref", name="pk_activity_execution_policy"),
        sa.ForeignKeyConstraint(
            ["activity_ref"], ["dante.activity_intention.activity_ref"],
            name="fk_activity_execution_policy_activity",
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_activity_execution_policy_person",
        ),
        schema="dante",
    )
    op.create_index(
        "ix_activity_execution_policy_self", "activity_execution_policy",
        ["self_person_ref"], schema="dante",
    )
    op.create_table(
        "activity_execution_policy_state",
        sa.Column("state_ref", sa.Uuid(), nullable=False),
        sa.Column("activity_ref", sa.Uuid(), nullable=False),
        sa.Column("mode_code", sa.Text(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("state_ref", name="pk_activity_execution_policy_state"),
        sa.UniqueConstraint(
            "activity_ref", "state_ref", name="uq_activity_execution_policy_state_owner",
        ),
        sa.CheckConstraint(
            "uuid_extract_version(state_ref) IS NOT DISTINCT FROM 7",
            name="ck_activity_execution_policy_state_uuidv7",
        ),
        sa.CheckConstraint(
            "mode_code IN ('disabled','record','live','record_and_live')",
            name="ck_activity_execution_policy_state_mode",
        ),
        sa.CheckConstraint(
            "isfinite(recorded_at)", name="ck_activity_execution_policy_state_recorded_at",
        ),
        sa.ForeignKeyConstraint(
            ["activity_ref"], ["dante.activity_execution_policy.activity_ref"],
            name="fk_activity_execution_policy_state_owner",
        ),
        schema="dante",
    )
    op.create_index(
        "ix_activity_execution_policy_state_owner", "activity_execution_policy_state",
        ["activity_ref"], schema="dante",
    )
    op.create_table(
        "activity_execution_policy_current_history",
        sa.Column("activity_ref", sa.Uuid(), nullable=False),
        sa.Column("state_ref", sa.Uuid(), nullable=False),
        sa.Column("current_from_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_until_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "activity_ref", "current_from_at",
            name="pk_activity_execution_policy_current_history",
        ),
        sa.CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at>current_from_at))",
            name="ck_activity_execution_policy_current_history_interval",
        ),
        sa.ForeignKeyConstraint(
            ["activity_ref", "state_ref"],
            ["dante.activity_execution_policy_state.activity_ref",
             "dante.activity_execution_policy_state.state_ref"],
            name="fk_activity_execution_policy_current_history_state",
        ),
        schema="dante",
    )
    op.create_index(
        "ux_activity_execution_policy_current_history_open",
        "activity_execution_policy_current_history", ["activity_ref"],
        unique=True, schema="dante",
        postgresql_where=sa.text("current_until_at IS NULL"),
    )
    op.create_index(
        "ix_activity_execution_policy_current_history_state",
        "activity_execution_policy_current_history", ["state_ref"], schema="dante",
    )
    op.create_table(
        "activity_execution_policy_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("activity_ref", sa.Uuid(), nullable=False),
        sa.Column("state_ref", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref", "operation_id", name="pk_activity_execution_policy_operation",
        ),
        sa.UniqueConstraint(
            "state_ref", name="uq_activity_execution_policy_operation_state",
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND char_length(operation_id) BETWEEN 1 AND 200",
            name="ck_activity_execution_policy_operation_id",
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name="ck_activity_execution_policy_operation_fingerprint",
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_activity_execution_policy_operation_person",
        ),
        sa.ForeignKeyConstraint(
            ["activity_ref", "state_ref"],
            ["dante.activity_execution_policy_state.activity_ref",
             "dante.activity_execution_policy_state.state_ref"],
            name="fk_activity_execution_policy_operation_state",
        ),
        schema="dante",
    )

    # Existing U4 Session controls were exposed only for an active B08-C
    # duration rule. Preserve that user-visible capability explicitly once;
    # future policy changes never infer their value from constraints.
    _sql("""
WITH legacy AS (
    SELECT DISTINCT activity.activity_ref, activity.self_person_ref
      FROM dante.activity_intention AS activity
      JOIN dante.temporal_constraint AS constraint_owner
        ON constraint_owner.subject_native_ref=activity.activity_ref
      JOIN dante.temporal_constraint_current_history AS current_rule
        ON current_rule.constraint_ref=constraint_owner.constraint_ref
       AND current_rule.current_until_at IS NULL
      JOIN dante.temporal_constraint_state AS state
        ON state.constraint_ref=constraint_owner.constraint_ref
       AND state.material_state_ref=current_rule.material_state_ref
     WHERE state.family_code='duration'
       AND state.constrained_facet_code='session.active_duration'
), seeded AS (
    SELECT legacy.activity_ref,legacy.self_person_ref,uuidv7() AS state_ref,
           statement_timestamp() AS recorded_at
      FROM legacy
), owners AS (
    INSERT INTO dante.activity_execution_policy(activity_ref,self_person_ref,created_at)
    SELECT activity_ref,self_person_ref,recorded_at FROM seeded
    RETURNING activity_ref
), states AS (
    INSERT INTO dante.activity_execution_policy_state(
        state_ref,activity_ref,mode_code,recorded_at
    ) SELECT seeded.state_ref,seeded.activity_ref,'live',seeded.recorded_at
      FROM seeded JOIN owners USING (activity_ref)
    RETURNING state_ref,activity_ref,recorded_at
)
INSERT INTO dante.activity_execution_policy_current_history(
    activity_ref,state_ref,current_from_at,current_until_at
)
SELECT activity_ref,state_ref,recorded_at,NULL FROM states;
""")

    _sql("""
CREATE FUNCTION dante.get_self_activity_execution_policy(
    requested_self_person_ref uuid, requested_activity_ref uuid
) RETURNS TABLE(state_ref uuid, mode_code text, current_from_at timestamptz)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
    SELECT history.state_ref,
           COALESCE(state.mode_code,'disabled') AS mode_code,
           history.current_from_at
      FROM dante.activity_intention AS activity
 LEFT JOIN dante.activity_execution_policy_current_history AS history
        ON history.activity_ref=activity.activity_ref
       AND history.current_until_at IS NULL
 LEFT JOIN dante.activity_execution_policy_state AS state
        ON state.activity_ref=activity.activity_ref
       AND state.state_ref=history.state_ref
     WHERE activity.activity_ref=requested_activity_ref
       AND activity.self_person_ref=requested_self_person_ref
$function$;
""")
    _sql("""
CREATE FUNCTION dante.set_self_activity_execution_policy(
    requested_self_person_ref uuid, requested_operation_id text,
    requested_intent_fingerprint text, requested_activity_ref uuid,
    requested_state_ref uuid, requested_mode_code text,
    requested_expected_state_ref uuid
) RETURNS TABLE(state_ref uuid, mode_code text, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
DECLARE
    prior dante.activity_execution_policy_operation%ROWTYPE;
    current_state uuid;
    previous_from timestamptz;
    accepted_at timestamptz;
BEGIN
    IF requested_operation_id IS NULL OR requested_operation_id<>btrim(requested_operation_id)
       OR char_length(requested_operation_id) NOT BETWEEN 1 AND 200
       OR requested_intent_fingerprint IS NULL
       OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$'
       OR requested_mode_code IS NULL
       OR requested_mode_code NOT IN ('disabled','record','live','record_and_live')
       OR uuid_extract_version(requested_state_ref) IS DISTINCT FROM 7 THEN
        RAISE EXCEPTION USING ERRCODE='23514',
            CONSTRAINT='activity_execution_policy_invalid',
            MESSAGE='Activity execution policy command rejected';
    END IF;

    -- One Activity lock serializes the absent-owner case as well as corrections.
    PERFORM 1 FROM dante.activity_intention AS activity
     WHERE activity.activity_ref=requested_activity_ref
       AND activity.self_person_ref=requested_self_person_ref FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='activity_execution_policy_owner_unavailable',
            MESSAGE='Activity is not owned by this self';
    END IF;

    SELECT * INTO prior FROM dante.activity_execution_policy_operation AS operation
     WHERE operation.self_person_ref=requested_self_person_ref
       AND operation.operation_id=requested_operation_id;
    IF FOUND THEN
        IF prior.intent_fingerprint IS DISTINCT FROM requested_intent_fingerprint
           OR prior.activity_ref IS DISTINCT FROM requested_activity_ref THEN
            RAISE EXCEPTION USING ERRCODE='23505',
                CONSTRAINT='activity_execution_policy_operation_reused',
                MESSAGE='Activity execution policy operation was reused';
        END IF;
        RETURN QUERY SELECT prior.state_ref, state.mode_code, true
          FROM dante.activity_execution_policy_state AS state
         WHERE state.state_ref=prior.state_ref;
        RETURN;
    END IF;

    SELECT history.state_ref, history.current_from_at
      INTO current_state, previous_from
      FROM dante.activity_execution_policy_current_history AS history
     WHERE history.activity_ref=requested_activity_ref
       AND history.current_until_at IS NULL;
    IF current_state IS DISTINCT FROM requested_expected_state_ref THEN
        RAISE EXCEPTION USING ERRCODE='40001',
            CONSTRAINT='activity_execution_policy_current_conflict',
            MESSAGE='Activity execution policy state changed';
    END IF;

    accepted_at:=statement_timestamp();
    IF previous_from IS NOT NULL AND accepted_at<=previous_from THEN
        accepted_at:=previous_from + interval '1 microsecond';
    END IF;
    INSERT INTO dante.activity_execution_policy(activity_ref,self_person_ref,created_at)
    VALUES(requested_activity_ref,requested_self_person_ref,accepted_at)
    ON CONFLICT (activity_ref) DO NOTHING;
    INSERT INTO dante.activity_execution_policy_state(
        state_ref,activity_ref,mode_code,recorded_at
    ) VALUES(requested_state_ref,requested_activity_ref,requested_mode_code,accepted_at);
    IF current_state IS NOT NULL THEN
        UPDATE dante.activity_execution_policy_current_history AS history
           SET current_until_at=accepted_at
         WHERE history.activity_ref=requested_activity_ref
           AND history.current_until_at IS NULL;
    END IF;
    INSERT INTO dante.activity_execution_policy_current_history(
        activity_ref,state_ref,current_from_at,current_until_at
    ) VALUES(requested_activity_ref,requested_state_ref,accepted_at,NULL);
    INSERT INTO dante.activity_execution_policy_operation(
        self_person_ref,operation_id,intent_fingerprint,activity_ref,state_ref
    ) VALUES(requested_self_person_ref,requested_operation_id,
             requested_intent_fingerprint,requested_activity_ref,requested_state_ref);
    RETURN QUERY SELECT requested_state_ref, requested_mode_code, false;
END;
$function$;
""")
    for signature in (
        "dante.get_self_activity_execution_policy(uuid,uuid)",
        "dante.set_self_activity_execution_policy(uuid,text,text,uuid,uuid,text,uuid)",
    ):
        _sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
        _sql(f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator")
        _sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")
    for table in (
        "activity_execution_policy", "activity_execution_policy_state",
        "activity_execution_policy_current_history", "activity_execution_policy_operation",
    ):
        _sql(f"REVOKE ALL ON TABLE dante.{table} FROM PUBLIC,dante_runtime,dante_migrator")

    # Keep B08 replay independent of a later policy correction. For a new live
    # Start, serialize with policy changes on the Activity owner row.
    bind = op.get_bind()
    definition = bind.exec_driver_sql(
        "SELECT pg_get_functiondef(p.oid) FROM pg_proc AS p "
        "JOIN pg_namespace AS n ON n.oid=p.pronamespace "
        "WHERE n.nspname='dante' AND p.proname='start_self_session' "
        "AND oidvectortypes(p.proargtypes)="
        "'uuid, text, text, uuid, uuid, text, uuid'"
    ).scalar_one()
    marker = "  INSERT INTO dante.session(session_ref) VALUES (requested_session_ref);"
    if definition.count(marker) != 1:
        raise RuntimeError("B14-U6 B08 Start admission patch point unavailable")
    guard = """
  IF requested_subject_family='activity' THEN
    PERFORM 1 FROM dante.activity_intention AS intention
     WHERE intention.activity_ref=requested_subject_native_ref
       AND intention.self_person_ref=requested_self_person_ref FOR SHARE;
    IF NOT EXISTS (
      SELECT 1 FROM dante.activity_execution_policy_current_history AS history
      JOIN dante.activity_execution_policy_state AS state
        ON state.activity_ref=history.activity_ref
       AND state.state_ref=history.state_ref
     WHERE history.activity_ref=requested_subject_native_ref
       AND history.current_until_at IS NULL
       AND state.mode_code IN ('live','record_and_live')
    ) THEN
      RAISE EXCEPTION USING ERRCODE='23514',
        CONSTRAINT='session_execution_policy_live_required',
        MESSAGE='Live Session capture is disabled for this Activity';
    END IF;
  END IF;

"""
    bind.exec_driver_sql(definition.replace(marker, guard + marker).replace("%", "%%"))


def downgrade() -> None:
    raise RuntimeError("B14-U6 execution policy requires a reviewed forward migration")
