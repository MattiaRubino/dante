# ruff: noqa: S608
"""B05-B typed actor-local primary Life Area assignment for Activity and Event.

Revision ID: 20260920_46
Revises: 20260920_45
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260920_46"
down_revision: str | None = "20260920_45"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"


def _execute(sql: str) -> None:
    op.execute(sa.text(sql))


def _assignment_tables() -> None:
    for subject, subject_table, subject_column in (
        ("activity", "activity", "activity_ref"),
        ("event", "event", "event_ref"),
    ):
        assignment = f"{subject}_life_area_assignment"
        operation = f"{subject}_life_area_assignment_operation"
        op.create_table(
            assignment,
            sa.Column(f"{subject}_ref", sa.Uuid(), nullable=False),
            sa.Column("self_person_ref", sa.Uuid(), nullable=False),
            sa.Column("life_area_ref", sa.Uuid(), nullable=False),
            sa.Column("revision", sa.BigInteger(), nullable=False),
            sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=False),
            sa.PrimaryKeyConstraint(
                "self_person_ref", f"{subject}_ref", name=op.f(f"pk_{assignment}")
            ),
            sa.ForeignKeyConstraint(
                [f"{subject}_ref"],
                [f"dante.{subject_table}.{subject_column}"],
                name=f"fk_{assignment}_{subject}_ref_{subject_table}",
                onupdate="NO ACTION",
                ondelete="NO ACTION",
                deferrable=False,
            ),
            sa.ForeignKeyConstraint(
                ["self_person_ref"],
                ["dante.person.person_ref"],
                name=f"fk_{assignment}_self_person_ref_person",
                onupdate="NO ACTION",
                ondelete="NO ACTION",
                deferrable=False,
            ),
            sa.ForeignKeyConstraint(
                ["life_area_ref"],
                ["dante.life_area.life_area_ref"],
                name=f"fk_{assignment}_life_area_ref_life_area",
                onupdate="NO ACTION",
                ondelete="NO ACTION",
                deferrable=False,
            ),
            sa.CheckConstraint("revision>=1", name=op.f(f"ck_{assignment}_revision")),
            schema="dante",
        )
        op.create_index(
            f"ix_{assignment}_self_person_life_area",
            assignment,
            ["self_person_ref", "life_area_ref", f"{subject}_ref"],
            schema="dante",
        )
        op.create_table(
            operation,
            sa.Column("self_person_ref", sa.Uuid(), nullable=False),
            sa.Column("operation_id", sa.Text(), nullable=False),
            sa.Column("intent_fingerprint", sa.Text(), nullable=False),
            sa.Column(f"{subject}_ref", sa.Uuid(), nullable=False),
            sa.Column("life_area_ref", sa.Uuid(), nullable=False),
            sa.Column("expected_revision", sa.BigInteger(), nullable=False),
            sa.Column("accepted_revision", sa.BigInteger(), nullable=False),
            sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
            sa.PrimaryKeyConstraint(
                "self_person_ref", "operation_id", name=op.f(f"pk_{operation}")
            ),
            sa.ForeignKeyConstraint(
                [f"{subject}_ref"],
                [f"dante.{subject_table}.{subject_column}"],
                name=(
                    "fk_activity_area_assignment_op_activity_ref_activity"
                    if subject == "activity"
                    else f"fk_{operation}_{subject}_ref_{subject_table}"
                ),
                onupdate="NO ACTION",
                ondelete="NO ACTION",
                deferrable=False,
            ),
            sa.ForeignKeyConstraint(
                ["self_person_ref"],
                ["dante.person.person_ref"],
                name=(
                    "fk_activity_area_assignment_op_self_person_ref_person"
                    if subject == "activity"
                    else f"fk_{operation}_self_person_ref_person"
                ),
                onupdate="NO ACTION",
                ondelete="NO ACTION",
                deferrable=False,
            ),
            sa.ForeignKeyConstraint(
                ["life_area_ref"],
                ["dante.life_area.life_area_ref"],
                name=(
                    "fk_activity_area_assignment_op_life_area_ref_life_area"
                    if subject == "activity"
                    else f"fk_{operation}_life_area_ref_life_area"
                ),
                onupdate="NO ACTION",
                ondelete="NO ACTION",
                deferrable=False,
            ),
            sa.CheckConstraint(
                "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
                name=op.f(f"ck_{operation}_operation_id"),
            ),
            sa.CheckConstraint(
                "intent_fingerprint ~ '^[0-9a-f]{64}$'",
                name=op.f(f"ck_{operation}_fingerprint"),
            ),
            sa.CheckConstraint(
                "expected_revision>=0", name=op.f(f"ck_{operation}_expected_revision")
            ),
            sa.CheckConstraint(
                "accepted_revision=expected_revision+1",
                name=op.f(f"ck_{operation}_accepted_revision"),
            ),
            schema="dante",
        )


def _assignment_function(subject: str, descriptor_table: str, ref_column: str) -> str:
    assignment = f"{subject}_life_area_assignment"
    operation = f"{subject}_life_area_assignment_operation"
    return f"""
        CREATE FUNCTION dante.assign_self_{subject}_life_area(
            requested_self_person_ref uuid,
            requested_operation_id text,
            requested_intent_fingerprint text,
            requested_{subject}_ref uuid,
            requested_life_area_ref uuid,
            requested_expected_revision bigint
        )
        RETURNS TABLE(life_area_ref uuid, assignment_revision bigint, assigned_at timestamptz,
                      replayed boolean)
        LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        #variable_conflict error
        DECLARE
            normalized_operation_id text := btrim(requested_operation_id);
            previous_fingerprint text;
            previous_{subject}_ref uuid;
            previous_life_area_ref uuid;
            previous_expected_revision bigint;
            previous_accepted_revision bigint;
            previous_accepted_at timestamptz;
            current_revision bigint;
            recorded_at timestamptz := statement_timestamp();
        BEGIN
            IF normalized_operation_id IS NULL OR normalized_operation_id='' OR char_length(normalized_operation_id)>200
               OR requested_intent_fingerprint IS NULL
               OR requested_intent_fingerprint !~ '^[0-9a-f]{{64}}$'
               OR requested_expected_revision IS NULL OR requested_expected_revision<0 THEN
                RAISE EXCEPTION USING ERRCODE='23514',
                    MESSAGE='Life Area assignment command rejected';
            END IF;
            PERFORM 1 FROM dante.person WHERE person_ref=requested_self_person_ref FOR UPDATE;
            IF NOT FOUND OR NOT EXISTS (
                SELECT 1 FROM dante.account_application_context
                 WHERE self_person_ref=requested_self_person_ref
            ) THEN
                RAISE EXCEPTION USING ERRCODE='23503',
                    MESSAGE='Life Area assignment self context rejected';
            END IF;
            SELECT receipt.intent_fingerprint,receipt.{subject}_ref,receipt.life_area_ref,
                   receipt.expected_revision,receipt.accepted_revision,receipt.accepted_at
              INTO previous_fingerprint,previous_{subject}_ref,previous_life_area_ref,
                   previous_expected_revision,previous_accepted_revision,previous_accepted_at
              FROM dante.{operation} AS receipt
             WHERE receipt.self_person_ref=requested_self_person_ref
               AND receipt.operation_id=normalized_operation_id;
            IF FOUND THEN
                IF previous_fingerprint<>requested_intent_fingerprint
                   OR previous_{subject}_ref<>requested_{subject}_ref
                   OR previous_life_area_ref<>requested_life_area_ref
                   OR previous_expected_revision<>requested_expected_revision THEN
                    RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_{operation}',
                        MESSAGE='Life Area assignment operation id reused with different intent';
                END IF;
                RETURN QUERY SELECT previous_life_area_ref,previous_accepted_revision,
                                    previous_accepted_at,true;
                RETURN;
            END IF;
            IF NOT EXISTS (
                SELECT 1 FROM dante.{descriptor_table}
                 WHERE {ref_column}=requested_{subject}_ref
                   AND self_person_ref=requested_self_person_ref
            ) THEN
                RAISE EXCEPTION USING ERRCODE='23503',
                    CONSTRAINT='fk_{assignment}_{subject}_ref_{subject}',
                    MESSAGE='Planning item is unavailable in current self scope';
            END IF;
            IF NOT EXISTS (
                SELECT 1 FROM dante.life_area AS target
                 WHERE target.life_area_ref=requested_life_area_ref
                   AND target.self_person_ref=requested_self_person_ref
                   AND target.archived=false
            ) THEN
                RAISE EXCEPTION USING ERRCODE='23503',
                    CONSTRAINT='life_area_assignment_target_unavailable',
                    MESSAGE='Life Area target is unavailable or archived';
            END IF;
            SELECT assignment.revision INTO current_revision
              FROM dante.{assignment} AS assignment
             WHERE assignment.self_person_ref=requested_self_person_ref
               AND assignment.{subject}_ref=requested_{subject}_ref FOR UPDATE;
            IF NOT FOUND THEN
                IF requested_expected_revision<>0 THEN
                    RAISE EXCEPTION USING ERRCODE='23514',
                        CONSTRAINT='life_area_assignment_revision_conflict',
                        MESSAGE='Life Area assignment does not match expected unassigned state';
                END IF;
                INSERT INTO dante.{assignment}(
                    {subject}_ref,self_person_ref,life_area_ref,revision,assigned_at
                ) VALUES (
                    requested_{subject}_ref,requested_self_person_ref,requested_life_area_ref,1,recorded_at
                );
                INSERT INTO dante.{operation}(
                    self_person_ref,operation_id,intent_fingerprint,{subject}_ref,life_area_ref,
                    expected_revision,accepted_revision,accepted_at
                ) VALUES (
                    requested_self_person_ref,normalized_operation_id,requested_intent_fingerprint,
                    requested_{subject}_ref,requested_life_area_ref,0,1,recorded_at
                );
                RETURN QUERY SELECT requested_life_area_ref,1::bigint,recorded_at,false;
                RETURN;
            END IF;
            IF current_revision<>requested_expected_revision THEN
                RAISE EXCEPTION USING ERRCODE='23514',
                    CONSTRAINT='life_area_assignment_revision_conflict',
                    MESSAGE='Life Area assignment state changed';
            END IF;
            IF EXISTS (
                SELECT 1 FROM dante.{assignment} AS current_assignment
                 WHERE current_assignment.self_person_ref=requested_self_person_ref
                   AND current_assignment.{subject}_ref=requested_{subject}_ref
                   AND current_assignment.life_area_ref=requested_life_area_ref
            ) THEN
                RAISE EXCEPTION USING ERRCODE='23514',
                    CONSTRAINT='life_area_assignment_no_change',
                    MESSAGE='Life Area assignment already targets this area';
            END IF;
            UPDATE dante.{assignment}
               SET life_area_ref=requested_life_area_ref,revision=current_revision+1,assigned_at=recorded_at
             WHERE self_person_ref=requested_self_person_ref
               AND {subject}_ref=requested_{subject}_ref;
            INSERT INTO dante.{operation}(
                self_person_ref,operation_id,intent_fingerprint,{subject}_ref,life_area_ref,
                expected_revision,accepted_revision,accepted_at
            ) VALUES (
                requested_self_person_ref,normalized_operation_id,requested_intent_fingerprint,
                requested_{subject}_ref,requested_life_area_ref,current_revision,current_revision+1,recorded_at
            );
            RETURN QUERY SELECT requested_life_area_ref,current_revision+1,recorded_at,false;
        END;
        $function$;
    """


def upgrade() -> None:
    """Create exact typed relations; retained legacy items remain explicitly unassigned."""
    _assignment_tables()
    _execute(_assignment_function("activity", "activity_intention", "activity_ref"))
    _execute(_assignment_function("event", "event_expectation", "event_ref"))
    _execute(r"""
        CREATE FUNCTION dante.create_self_activity_in_life_area(
            requested_self_person_ref uuid, requested_operation_id text,
            requested_intent_fingerprint text, requested_activity_ref uuid,
            requested_title text, requested_life_area_ref uuid
        )
        RETURNS TABLE(activity_ref uuid, title text, created_at timestamptz,
                      life_area_ref uuid, assignment_revision bigint, replayed boolean)
        LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            created_ref uuid;
            created_title text;
            created_at_value timestamptz;
            create_replayed boolean;
            assigned_area_ref uuid;
            assigned_revision bigint;
            assignment_replayed boolean;
            assigned_at_value timestamptz;
        BEGIN
            SELECT created.activity_ref,created.title,created.created_at,created.replayed
              INTO created_ref,created_title,created_at_value,create_replayed
              FROM dante.create_self_activity(
                  requested_self_person_ref,requested_operation_id,requested_intent_fingerprint,
                  requested_activity_ref,requested_title
              ) AS created;
            SELECT assigned.life_area_ref,assigned.assignment_revision,assigned.assigned_at,assigned.replayed
              INTO assigned_area_ref,assigned_revision,assigned_at_value,assignment_replayed
              FROM dante.assign_self_activity_life_area(
                  requested_self_person_ref,requested_operation_id,requested_intent_fingerprint,
                  created_ref,requested_life_area_ref,0
              ) AS assigned;
            IF create_replayed IS DISTINCT FROM assignment_replayed THEN
                RAISE EXCEPTION USING ERRCODE='XX001',
                    MESSAGE='Activity creation and Life Area assignment replay diverged';
            END IF;
            RETURN QUERY SELECT created_ref,created_title,created_at_value,assigned_area_ref,
                                assigned_revision,create_replayed;
        END;
        $function$;
    """)
    _execute(r"""
        CREATE FUNCTION dante.create_self_event_with_agenda_in_life_area(
            requested_self_person_ref uuid, requested_operation_id text,
            requested_intent_fingerprint text, requested_event_ref uuid,
            requested_title text, requested_agenda_parts text[], requested_life_area_ref uuid
        )
        RETURNS TABLE(event_ref uuid, title text, created_at timestamptz, agenda_revision bigint,
                      agenda_parts text[], life_area_ref uuid, assignment_revision bigint,
                      replayed boolean)
        LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            created_ref uuid;
            created_title text;
            created_at_value timestamptz;
            created_agenda_revision bigint;
            created_agenda_parts text[];
            create_replayed boolean;
            assigned_area_ref uuid;
            assigned_revision bigint;
            assignment_replayed boolean;
            assigned_at_value timestamptz;
        BEGIN
            SELECT created.event_ref,created.title,created.created_at,created.agenda_revision,
                   created.agenda_parts,created.replayed
              INTO created_ref,created_title,created_at_value,created_agenda_revision,
                   created_agenda_parts,create_replayed
              FROM dante.create_self_event_with_agenda(
                  requested_self_person_ref,requested_operation_id,requested_intent_fingerprint,
                  requested_event_ref,requested_title,requested_agenda_parts
              ) AS created;
            SELECT assigned.life_area_ref,assigned.assignment_revision,assigned.assigned_at,assigned.replayed
              INTO assigned_area_ref,assigned_revision,assigned_at_value,assignment_replayed
              FROM dante.assign_self_event_life_area(
                  requested_self_person_ref,requested_operation_id,requested_intent_fingerprint,
                  created_ref,requested_life_area_ref,0
              ) AS assigned;
            IF create_replayed IS DISTINCT FROM assignment_replayed THEN
                RAISE EXCEPTION USING ERRCODE='XX001',
                    MESSAGE='Event creation and Life Area assignment replay diverged';
            END IF;
            RETURN QUERY SELECT created_ref,created_title,created_at_value,created_agenda_revision,
                                created_agenda_parts,assigned_area_ref,assigned_revision,create_replayed;
        END;
        $function$;
    """)
    _execute(r"""
        CREATE FUNCTION dante.list_self_life_area_assignments(requested_self_person_ref uuid)
        RETURNS TABLE(subject_kind text, subject_native_ref uuid, life_area_ref uuid,
                      assignment_revision bigint, assigned_at timestamptz)
        LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
            SELECT 'activity'::text,assignment.activity_ref,assignment.life_area_ref,
                   assignment.revision,assignment.assigned_at
             FROM dante.activity_life_area_assignment AS assignment
             WHERE assignment.self_person_ref=requested_self_person_ref
               AND EXISTS (
                   SELECT 1 FROM dante.account_application_context
                    WHERE self_person_ref=requested_self_person_ref
               )
            UNION ALL
            SELECT 'event'::text,assignment.event_ref,assignment.life_area_ref,
                   assignment.revision,assignment.assigned_at
             FROM dante.event_life_area_assignment AS assignment
             WHERE assignment.self_person_ref=requested_self_person_ref
               AND EXISTS (
                   SELECT 1 FROM dante.account_application_context
                    WHERE self_person_ref=requested_self_person_ref
               )
             ORDER BY 1,2;
        $function$;
    """)
    _execute(r"""
        CREATE FUNCTION dante.list_self_unassigned_life_area_items(requested_self_person_ref uuid)
        RETURNS TABLE(subject_kind text, subject_native_ref uuid, title text, created_at timestamptz)
        LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
            SELECT 'activity'::text,intention.activity_ref,intention.title,intention.created_at
             FROM dante.activity_intention AS intention
             WHERE intention.self_person_ref=requested_self_person_ref
               AND EXISTS (
                   SELECT 1 FROM dante.account_application_context
                    WHERE self_person_ref=requested_self_person_ref
               )
               AND NOT EXISTS (
                   SELECT 1 FROM dante.activity_life_area_assignment AS assignment
                    WHERE assignment.self_person_ref=requested_self_person_ref
                      AND assignment.activity_ref=intention.activity_ref
               )
            UNION ALL
            SELECT 'event'::text,expectation.event_ref,expectation.title,expectation.created_at
             FROM dante.event_expectation AS expectation
             WHERE expectation.self_person_ref=requested_self_person_ref
               AND EXISTS (
                   SELECT 1 FROM dante.account_application_context
                    WHERE self_person_ref=requested_self_person_ref
               )
               AND NOT EXISTS (
                   SELECT 1 FROM dante.event_life_area_assignment AS assignment
                    WHERE assignment.self_person_ref=requested_self_person_ref
                      AND assignment.event_ref=expectation.event_ref
               )
             ORDER BY 1,4,2;
        $function$;
    """)
    for signature in (
        "dante.assign_self_activity_life_area(uuid,text,text,uuid,uuid,bigint)",
        "dante.assign_self_event_life_area(uuid,text,text,uuid,uuid,bigint)",
        "dante.create_self_activity_in_life_area(uuid,text,text,uuid,text,uuid)",
        "dante.create_self_event_with_agenda_in_life_area(uuid,text,text,uuid,text,text[],uuid)",
        "dante.list_self_life_area_assignments(uuid)",
        "dante.list_self_unassigned_life_area_items(uuid)",
    ):
        _execute(f"ALTER FUNCTION {signature} OWNER TO {_OWNER}")
        _execute(
            f"REVOKE ALL PRIVILEGES ON FUNCTION {signature} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
        _execute(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}")
    for signature in (
        "dante.create_self_activity(uuid,text,text,uuid,text)",
        "dante.create_self_event(uuid,text,text,uuid,text)",
        "dante.create_self_event_with_agenda(uuid,text,text,uuid,text,text[])",
    ):
        _execute(
            f"REVOKE ALL PRIVILEGES ON FUNCTION {signature} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
    for table in (
        "activity_life_area_assignment",
        "event_life_area_assignment",
        "activity_life_area_assignment_operation",
        "event_life_area_assignment_operation",
    ):
        _execute(
            f"REVOKE ALL PRIVILEGES ON TABLE dante.{table} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )


def downgrade() -> None:
    """Never erase accepted actor-local assignment evidence in place."""
    raise RuntimeError("B05-B primary assignment requires a reviewed forward migration")
