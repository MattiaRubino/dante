"""B14-U6: truthful retrospective B08 Session capture for an Activity."""

from collections.abc import Sequence
from hashlib import md5

import sqlalchemy as sa
from alembic import op

revision: str = "20261002_101"
down_revision: str | None = "20261002_100"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # _97 supplied names already prefixed for Alembic's ck_<table> convention.
    for table, suffix in (
        ("activity_execution_policy_state", "uuidv7"),
        ("activity_execution_policy_state", "mode"),
        ("activity_execution_policy_state", "recorded_at"),
        ("activity_execution_policy_current_history", "interval"),
        ("activity_execution_policy_operation", "id"),
        ("activity_execution_policy_operation", "fingerprint"),
    ):
        accepted = f"ck_{table}_{suffix}"
        expanded = f"ck_{table}_{accepted}"
        old = (
            expanded if len(expanded) <= 63
            else f"{expanded[:55]}_{md5(expanded.encode(), usedforsecurity=False).hexdigest()[-4:]}"
        )
        op.execute(f"ALTER TABLE dante.{table} RENAME CONSTRAINT {old} TO {accepted}")

    op.create_table(
        "session_manual_record_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("session_ref", sa.Uuid(), nullable=False),
        sa.Column("subject_native_ref", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref", "operation_id", name="pk_session_manual_record_operation"
        ),
        sa.UniqueConstraint("session_ref", name="uq_session_manual_record_operation_session_ref"),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200", name="operation_id",
        ),
        sa.CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        sa.ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_session_manual_record_operation_person",
        ),
        sa.ForeignKeyConstraint(
            ["session_ref"], ["dante.session.session_ref"],
            name="fk_session_manual_record_operation_session",
        ),
        schema="dante",
    )
    bind = op.get_bind()
    bind.exec_driver_sql("""
CREATE FUNCTION dante.record_self_activity_session(
    requested_self_person_ref uuid,
    requested_operation_id text,
    requested_intent_fingerprint text,
    requested_session_ref uuid,
    requested_material_state_ref uuid,
    requested_activity_ref uuid,
    requested_started_at timestamptz,
    requested_ended_at timestamptz
) RETURNS TABLE(
    session_ref uuid, subject_native_ref uuid, timing_material_state_ref uuid,
    started_at timestamptz, ended_at timestamptz, replayed boolean
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE
    prior record;
    recorded_at timestamptz := statement_timestamp();
BEGIN
    IF requested_operation_id IS NULL OR requested_operation_id<>btrim(requested_operation_id)
       OR char_length(requested_operation_id) NOT BETWEEN 1 AND 200
       OR requested_intent_fingerprint IS NULL
       OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$'
       OR uuid_extract_version(requested_session_ref) IS DISTINCT FROM 7
       OR uuid_extract_version(requested_material_state_ref) IS DISTINCT FROM 7
       OR requested_started_at IS NULL OR requested_ended_at IS NULL
       OR NOT isfinite(requested_started_at) OR NOT isfinite(requested_ended_at)
       OR requested_started_at>=requested_ended_at
       OR requested_ended_at>recorded_at THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='session_manual_record_invalid',
          MESSAGE='Retrospective Session timing or identity rejected';
    END IF;
    PERFORM 1 FROM dante.activity_intention AS activity
     WHERE activity.activity_ref=requested_activity_ref
       AND activity.self_person_ref=requested_self_person_ref FOR SHARE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
          CONSTRAINT='session_manual_record_owner_unavailable',
          MESSAGE='Activity is not owned by this self';
    END IF;

    PERFORM pg_advisory_xact_lock(hashtextextended(
        requested_self_person_ref::text || ':manual-session:' || requested_operation_id, 0
    ));
    SELECT * INTO prior FROM dante.session_manual_record_operation AS receipt
     WHERE receipt.self_person_ref=requested_self_person_ref
       AND receipt.operation_id=requested_operation_id;
    IF FOUND THEN
        IF prior.intent_fingerprint IS DISTINCT FROM requested_intent_fingerprint
           OR prior.subject_native_ref IS DISTINCT FROM requested_activity_ref THEN
            RAISE EXCEPTION USING ERRCODE='23505',
              CONSTRAINT='session_manual_record_operation_reused',
              MESSAGE='Manual Session operation id was reused';
        END IF;
        RETURN QUERY SELECT subject.session_ref,subject.subject_native_ref,
               current.material_state_ref,timing.started_at,timing.ended_at,true
          FROM dante.session_execution_subject AS subject
          JOIN dante.session_timing_current_history AS current
            ON current.session_ref=subject.session_ref AND current.current_until_at IS NULL
          JOIN dante.session_timing_absolute AS timing
            ON timing.material_state_ref=current.material_state_ref
         WHERE subject.session_ref=prior.session_ref;
        RETURN;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM dante.activity_execution_policy_current_history AS current
        JOIN dante.activity_execution_policy_state AS state
          ON state.activity_ref=current.activity_ref AND state.state_ref=current.state_ref
        WHERE current.activity_ref=requested_activity_ref
          AND current.current_until_at IS NULL
          AND state.mode_code IN ('record','record_and_live')
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='session_manual_record_policy_required',
          MESSAGE='Manual Session capture is disabled for this Activity';
    END IF;

    INSERT INTO dante.session(session_ref) VALUES(requested_session_ref);
    INSERT INTO dante.native_address(native_ref,owner_family)
    VALUES(requested_session_ref,'session');
    INSERT INTO dante.material_state_address(material_state_ref,native_owner_ref,facet_code)
    VALUES(requested_material_state_ref,requested_session_ref,'session.timing');
    INSERT INTO dante.session_timing_state(material_state_ref,session_ref,timing_form_code)
    VALUES(requested_material_state_ref,requested_session_ref,'absolute');
    INSERT INTO dante.session_timing_absolute(
        material_state_ref,started_at,start_precision_code,ended_at,end_precision_code
    ) VALUES(requested_material_state_ref,requested_started_at,'exact',
             requested_ended_at,'exact');
    INSERT INTO dante.native_current_material_state(
        native_owner_ref,facet_code,material_state_ref
    ) VALUES(requested_session_ref,'session.timing',requested_material_state_ref);
    INSERT INTO dante.session_timing_current_history(
        session_ref,material_state_ref,current_from_at
    ) VALUES(requested_session_ref,requested_material_state_ref,recorded_at);
    INSERT INTO dante.session_execution_subject(session_ref,subject_native_ref)
    VALUES(requested_session_ref,requested_activity_ref);
    INSERT INTO dante.session_manual_record_operation(
        self_person_ref,operation_id,intent_fingerprint,
        session_ref,subject_native_ref,created_at
    ) VALUES(requested_self_person_ref,requested_operation_id,requested_intent_fingerprint,
             requested_session_ref,requested_activity_ref,recorded_at);
    RETURN QUERY SELECT requested_session_ref,requested_activity_ref,
           requested_material_state_ref,requested_started_at,requested_ended_at,false;
END;
$function$;
""")
    signature = "dante.record_self_activity_session(uuid,text,text,uuid,uuid,uuid,timestamptz,timestamptz)"
    bind.exec_driver_sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
    bind.exec_driver_sql(
        f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator"
    )
    bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")
    bind.exec_driver_sql(
        "REVOKE ALL ON TABLE dante.session_manual_record_operation "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )


def downgrade() -> None:
    raise RuntimeError("B14-U6 retrospective Session requires a reviewed forward migration")
