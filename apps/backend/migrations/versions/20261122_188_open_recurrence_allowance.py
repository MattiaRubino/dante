"""Persist owner-scoped renewal decisions for open calendar series."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261122_188"
down_revision: str | None = "20261118_187"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "open_recurrence_allowance",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("owner_code", sa.Text(), nullable=False),
        sa.Column("source_ref", sa.Uuid(), nullable=False),
        sa.Column("epoch_state_ref", sa.Uuid(), nullable=False),
        sa.Column("allowed_count", sa.Integer(), nullable=False),
        sa.Column("declined", sa.Boolean(), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref", "owner_code", "source_ref", name=op.f("pk_open_recurrence_allowance")
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name=op.f("fk_open_recurrence_allowance_person"),
        ),
        sa.ForeignKeyConstraint(
            ["source_ref"],
            ["dante.native_address.native_ref"],
            name=op.f("fk_open_recurrence_allowance_source"),
        ),
        sa.CheckConstraint(
            "owner_code IN ('routine','event')", name=op.f("ck_open_recurrence_allowance_owner")
        ),
        sa.CheckConstraint(
            "allowed_count >= 730 AND allowed_count % 730 = 0",
            name=op.f("ck_open_recurrence_allowance_count"),
        ),
        sa.CheckConstraint("revision >= 0", name=op.f("ck_open_recurrence_allowance_revision")),
        schema="dante",
    )
    op.create_table(
        "open_recurrence_allowance_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("owner_code", sa.Text(), nullable=False),
        sa.Column("source_ref", sa.Uuid(), nullable=False),
        sa.Column("expected_state_ref", sa.Uuid(), nullable=False),
        sa.Column("expected_revision", sa.Integer(), nullable=False),
        sa.Column("decision", sa.Text(), nullable=False),
        sa.Column("accepted_count", sa.Integer(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref", "operation_id", name=op.f("pk_open_recurrence_allowance_operation")
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref", "owner_code", "source_ref"],
            [
                "dante.open_recurrence_allowance.self_person_ref",
                "dante.open_recurrence_allowance.owner_code",
                "dante.open_recurrence_allowance.source_ref",
            ],
            name=op.f("fk_open_recurrence_allowance_operation_allowance"),
        ),
        sa.CheckConstraint(
            "decision IN ('extend','decline')",
            name=op.f("ck_open_recurrence_allowance_operation_decision"),
        ),
        sa.CheckConstraint(
            "length(operation_id) BETWEEN 1 AND 200",
            name=op.f("ck_open_recurrence_allowance_operation_id"),
        ),
        schema="dante",
    )
    for table in ("open_recurrence_allowance", "open_recurrence_allowance_operation"):
        op.execute(f"ALTER TABLE dante.{table} OWNER TO dante_owner")
        op.execute(f"REVOKE ALL ON TABLE dante.{table} FROM PUBLIC, dante_runtime, dante_migrator")
    op.execute(
        sa.text("""
        CREATE FUNCTION dante.get_self_open_recurrence_allowance(actor uuid, owner text, source uuid)
        RETURNS TABLE (material_state_ref uuid, epoch_state_ref uuid, allowed_count integer, declined boolean, revision integer)
        LANGUAGE plpgsql SECURITY DEFINER STABLE SET search_path = pg_catalog, dante, pg_temp
        AS $body$
        BEGIN
            IF owner = 'routine' THEN
                IF NOT EXISTS (SELECT 1 FROM dante.routine_intention WHERE routine_ref = source AND self_person_ref = actor) THEN RETURN; END IF;
                RETURN QUERY SELECT h.material_state_ref, epoch.material_state_ref, coalesce(a.allowed_count, 730), coalesce(a.declined, false), coalesce(a.revision, 0)
                  FROM dante.routine_recurrence_current_history h
                  JOIN dante.routine_recurrence_state s ON s.material_state_ref = h.material_state_ref AND s.family_code = 'calendar_wall_clock' AND s.range_kind = 'open'
                  JOIN LATERAL (
                    SELECT previous.material_state_ref
                      FROM dante.routine_recurrence_current_history previous
                      JOIN dante.routine_recurrence_state previous_state ON previous_state.material_state_ref = previous.material_state_ref
                     WHERE previous.routine_ref = source
                       AND previous_state.family_code = 'calendar_wall_clock' AND previous_state.range_kind = 'open'
                       AND previous.current_from_at > coalesce((
                         SELECT max(cutover.current_from_at)
                           FROM dante.routine_recurrence_current_history cutover
                           JOIN dante.routine_recurrence_state cutover_state ON cutover_state.material_state_ref = cutover.material_state_ref
                          WHERE cutover.routine_ref = source
                            AND (cutover_state.family_code <> 'calendar_wall_clock' OR cutover_state.range_kind <> 'open')
                       ), '-infinity'::timestamptz)
                     ORDER BY previous.current_from_at LIMIT 1
                  ) epoch ON true
                  LEFT JOIN dante.open_recurrence_allowance a ON a.self_person_ref = actor AND a.owner_code = owner AND a.source_ref = source AND a.epoch_state_ref = epoch.material_state_ref
                 WHERE h.routine_ref = source AND h.current_until_at IS NULL;
            ELSIF owner = 'event' THEN
                IF NOT EXISTS (SELECT 1 FROM dante.event_expectation WHERE event_ref = source AND self_person_ref = actor) THEN RETURN; END IF;
                RETURN QUERY SELECT h.material_state_ref, epoch.material_state_ref, coalesce(a.allowed_count, 730), coalesce(a.declined, false), coalesce(a.revision, 0)
                  FROM dante.event_recurrence_current_history h
                  JOIN dante.event_recurrence_state s ON s.material_state_ref = h.material_state_ref AND s.family_code = 'calendar_wall_clock' AND s.range_kind = 'open'
                  JOIN LATERAL (
                    SELECT previous.material_state_ref
                      FROM dante.event_recurrence_current_history previous
                      JOIN dante.event_recurrence_state previous_state ON previous_state.material_state_ref = previous.material_state_ref
                     WHERE previous.event_ref = source
                       AND previous_state.family_code = 'calendar_wall_clock' AND previous_state.range_kind = 'open'
                       AND previous.current_from_at > coalesce((
                         SELECT max(cutover.current_from_at)
                           FROM dante.event_recurrence_current_history cutover
                           JOIN dante.event_recurrence_state cutover_state ON cutover_state.material_state_ref = cutover.material_state_ref
                          WHERE cutover.event_ref = source
                            AND (cutover_state.family_code <> 'calendar_wall_clock' OR cutover_state.range_kind <> 'open')
                       ), '-infinity'::timestamptz)
                     ORDER BY previous.current_from_at LIMIT 1
                  ) epoch ON true
                  LEFT JOIN dante.open_recurrence_allowance a ON a.self_person_ref = actor AND a.owner_code = owner AND a.source_ref = source AND a.epoch_state_ref = epoch.material_state_ref
                 WHERE h.event_ref = source AND h.current_until_at IS NULL;
            END IF;
        END $body$
    """)
    )
    op.execute(
        sa.text("""
        CREATE FUNCTION dante.get_self_open_recurrence_allowance_operation(actor uuid, request_operation text)
        RETURNS TABLE (owner_code text, source_ref uuid, expected_state_ref uuid, expected_revision integer, decision text)
        LANGUAGE sql SECURITY DEFINER STABLE SET search_path = pg_catalog, dante, pg_temp
        AS $body$
            SELECT o.owner_code, o.source_ref, o.expected_state_ref, o.expected_revision, o.decision
              FROM dante.open_recurrence_allowance_operation o
             WHERE o.self_person_ref = actor AND o.operation_id = request_operation
        $body$
    """)
    )
    op.execute(
        sa.text("""
        CREATE FUNCTION dante.decide_self_open_recurrence_allowance(
            actor uuid, owner text, source uuid, expected_state uuid,
            expected_revision integer, request_operation text, request_decision text
        ) RETURNS TABLE (allowed_count integer, declined boolean, revision integer, replayed boolean)
        LANGUAGE plpgsql SECURITY DEFINER VOLATILE SET search_path = pg_catalog, dante, pg_temp
        AS $body$
        DECLARE existing dante.open_recurrence_allowance_operation%ROWTYPE;
                current_state uuid;
                epoch_state uuid;
                current_count integer;
                current_declined boolean;
                current_revision integer;
        BEGIN
            IF request_operation IS NULL OR length(request_operation) NOT BETWEEN 1 AND 200
               OR request_decision NOT IN ('extend', 'decline') THEN
                RAISE EXCEPTION USING ERRCODE = '23514', CONSTRAINT = 'open_recurrence_allowance_invalid';
            END IF;
            IF owner = 'routine' THEN
                PERFORM 1 FROM dante.routine_intention WHERE routine_ref = source AND self_person_ref = actor FOR UPDATE;
            ELSIF owner = 'event' THEN
                PERFORM 1 FROM dante.event_expectation WHERE event_ref = source AND self_person_ref = actor FOR UPDATE;
            ELSE
                RETURN;
            END IF;
            IF NOT FOUND THEN RETURN; END IF;
            SELECT * INTO existing FROM dante.open_recurrence_allowance_operation
             WHERE self_person_ref = actor AND operation_id = request_operation;
            IF FOUND THEN
                IF existing.owner_code <> owner OR existing.source_ref <> source OR existing.expected_state_ref <> expected_state
                   OR existing.expected_revision <> expected_revision OR existing.decision <> request_decision THEN
                    RAISE EXCEPTION USING ERRCODE = '23505', CONSTRAINT = 'open_recurrence_allowance_operation_reused';
                END IF;
                RETURN QUERY SELECT existing.accepted_count, existing.decision = 'decline', existing.expected_revision + 1, true;
                RETURN;
            END IF;
            SELECT a.material_state_ref, a.epoch_state_ref INTO current_state, epoch_state
              FROM dante.get_self_open_recurrence_allowance(actor, owner, source) a;
            IF current_state IS NULL OR current_state <> expected_state THEN
                RAISE EXCEPTION USING ERRCODE = '40001', CONSTRAINT = 'open_recurrence_allowance_state_conflict';
            END IF;
            INSERT INTO dante.open_recurrence_allowance(self_person_ref, owner_code, source_ref, epoch_state_ref, allowed_count, declined, revision)
                 VALUES(actor, owner, source, epoch_state, 730, false, 0)
                 ON CONFLICT (self_person_ref, owner_code, source_ref) DO UPDATE
                     SET epoch_state_ref = excluded.epoch_state_ref, allowed_count = 730, declined = false, revision = 0
                   WHERE open_recurrence_allowance.epoch_state_ref IS DISTINCT FROM excluded.epoch_state_ref;
            SELECT a.allowed_count, a.declined, a.revision INTO current_count, current_declined, current_revision
              FROM dante.open_recurrence_allowance a
             WHERE a.self_person_ref = actor AND a.owner_code = owner AND a.source_ref = source FOR UPDATE;
            IF current_revision <> expected_revision OR current_declined OR current_count > 2147482917 THEN
                RAISE EXCEPTION USING ERRCODE = '40001', CONSTRAINT = 'open_recurrence_allowance_state_conflict';
            END IF;
            IF request_decision = 'extend' THEN current_count := current_count + 730; END IF;
            UPDATE dante.open_recurrence_allowance a SET allowed_count = current_count,
                   declined = request_decision = 'decline', revision = current_revision + 1
             WHERE a.self_person_ref = actor AND a.owner_code = owner AND a.source_ref = source;
            INSERT INTO dante.open_recurrence_allowance_operation VALUES
                (actor, request_operation, owner, source, expected_state, expected_revision, request_decision, current_count, clock_timestamp());
            RETURN QUERY SELECT current_count, request_decision = 'decline', current_revision + 1, false;
        END $body$
    """)
    )
    for name, signature in (
        ("get_self_open_recurrence_allowance", "uuid,text,uuid"),
        ("get_self_open_recurrence_allowance_operation", "uuid,text"),
        ("decide_self_open_recurrence_allowance", "uuid,text,uuid,uuid,integer,text,text"),
    ):
        op.execute(f"ALTER FUNCTION dante.{name}({signature}) OWNER TO dante_owner")
        op.execute(f"REVOKE ALL ON FUNCTION dante.{name}({signature}) FROM PUBLIC")
        op.execute(f"GRANT EXECUTE ON FUNCTION dante.{name}({signature}) TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("Forward-only Dante migration")
