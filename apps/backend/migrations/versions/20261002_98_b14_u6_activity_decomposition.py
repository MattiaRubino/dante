"""B14-U6: bounded direct Activity decomposition with current-state history."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261002_98"
down_revision: str | None = "20261002_97"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def upgrade() -> None:
    op.create_table(
        "activity_decomposition",
        sa.Column("decomposition_ref", sa.Uuid(), nullable=False),
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("parent_activity_ref", sa.Uuid(), nullable=False),
        sa.Column("child_activity_ref", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("decomposition_ref", name="pk_activity_decomposition"),
        sa.CheckConstraint(
            "uuid_extract_version(decomposition_ref) IS NOT DISTINCT FROM 7",
            name="ck_activity_decomposition_uuidv7",
        ),
        sa.CheckConstraint(
            "parent_activity_ref<>child_activity_ref", name="ck_activity_decomposition_distinct"
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_activity_decomposition_person",
        ),
        sa.ForeignKeyConstraint(
            ["parent_activity_ref"],
            ["dante.activity_intention.activity_ref"],
            name="fk_activity_decomposition_parent",
        ),
        sa.ForeignKeyConstraint(
            ["child_activity_ref"],
            ["dante.activity_intention.activity_ref"],
            name="fk_activity_decomposition_child",
        ),
        schema="dante",
    )
    op.create_index(
        "ix_activity_decomposition_parent",
        "activity_decomposition",
        ["parent_activity_ref"],
        schema="dante",
    )
    op.create_index(
        "ix_activity_decomposition_child",
        "activity_decomposition",
        ["child_activity_ref"],
        schema="dante",
    )
    op.create_table(
        "activity_decomposition_state",
        sa.Column("state_ref", sa.Uuid(), nullable=False),
        sa.Column("decomposition_ref", sa.Uuid(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("requirement_code", sa.Text(), nullable=False),
        sa.Column("presentation_order", sa.Integer(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("state_ref", name="pk_activity_decomposition_state"),
        sa.UniqueConstraint(
            "decomposition_ref", "state_ref", name="uq_activity_decomposition_state_owner"
        ),
        sa.CheckConstraint(
            "uuid_extract_version(state_ref) IS NOT DISTINCT FROM 7",
            name="ck_activity_decomposition_state_uuidv7",
        ),
        sa.CheckConstraint(
            "requirement_code IN ('required','optional')",
            name="ck_activity_decomposition_state_requirement",
        ),
        sa.CheckConstraint("presentation_order>0", name="ck_activity_decomposition_state_order"),
        sa.CheckConstraint(
            "isfinite(recorded_at)", name="ck_activity_decomposition_state_recorded_at"
        ),
        sa.ForeignKeyConstraint(
            ["decomposition_ref"],
            ["dante.activity_decomposition.decomposition_ref"],
            name="fk_activity_decomposition_state_relation",
        ),
        schema="dante",
    )
    op.create_index(
        "ix_activity_decomposition_state_relation",
        "activity_decomposition_state",
        ["decomposition_ref"],
        schema="dante",
    )
    op.create_table(
        "activity_decomposition_current_history",
        sa.Column("decomposition_ref", sa.Uuid(), nullable=False),
        sa.Column("state_ref", sa.Uuid(), nullable=False),
        sa.Column("current_from_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_until_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "decomposition_ref", "current_from_at", name="pk_activity_decomposition_current_history"
        ),
        sa.CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR (isfinite(current_until_at) AND current_until_at>current_from_at))",
            name="ck_activity_decomposition_current_history_interval",
        ),
        sa.ForeignKeyConstraint(
            ["decomposition_ref", "state_ref"],
            [
                "dante.activity_decomposition_state.decomposition_ref",
                "dante.activity_decomposition_state.state_ref",
            ],
            name="fk_activity_decomposition_current_history_state",
        ),
        schema="dante",
    )
    op.create_index(
        "ux_activity_decomposition_current_history_open",
        "activity_decomposition_current_history",
        ["decomposition_ref"],
        unique=True,
        schema="dante",
        postgresql_where=sa.text("current_until_at IS NULL"),
    )
    op.create_index(
        "ix_activity_decomposition_current_history_state",
        "activity_decomposition_current_history",
        ["state_ref"],
        schema="dante",
    )
    op.create_table(
        "activity_decomposition_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("decomposition_ref", sa.Uuid(), nullable=False),
        sa.Column("state_ref", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref", "operation_id", name="pk_activity_decomposition_operation"
        ),
        sa.UniqueConstraint("state_ref", name="uq_activity_decomposition_operation_state"),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND char_length(operation_id) BETWEEN 1 AND 200",
            name="ck_activity_decomposition_operation_id",
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name="ck_activity_decomposition_operation_fingerprint",
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_activity_decomposition_operation_person",
        ),
        sa.ForeignKeyConstraint(
            ["decomposition_ref", "state_ref"],
            [
                "dante.activity_decomposition_state.decomposition_ref",
                "dante.activity_decomposition_state.state_ref",
            ],
            name="fk_activity_decomposition_operation_state",
        ),
        schema="dante",
    )
    _sql("""
CREATE FUNCTION dante.get_self_activity_decomposition(
    requested_self_person_ref uuid, requested_parent_activity_ref uuid
) RETURNS TABLE(
    decomposition_ref uuid, parent_activity_ref uuid, child_activity_ref uuid,
    child_title text, state_ref uuid, requirement_code text,
    presentation_order integer, current_from_at timestamptz
) LANGUAGE sql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
    SELECT relation.decomposition_ref,relation.parent_activity_ref,
           relation.child_activity_ref,child.title,history.state_ref,
           state.requirement_code,state.presentation_order,history.current_from_at
      FROM dante.activity_decomposition AS relation
      JOIN dante.activity_decomposition_current_history AS history
        ON history.decomposition_ref=relation.decomposition_ref AND history.current_until_at IS NULL
      JOIN dante.activity_decomposition_state AS state
        ON state.decomposition_ref=relation.decomposition_ref AND state.state_ref=history.state_ref
      JOIN dante.activity_intention AS child
        ON child.activity_ref=relation.child_activity_ref
     WHERE relation.parent_activity_ref=requested_parent_activity_ref
       AND relation.self_person_ref=requested_self_person_ref
       AND state.active
       AND EXISTS (SELECT 1 FROM dante.activity_intention AS parent
                    WHERE parent.activity_ref=requested_parent_activity_ref
                      AND parent.self_person_ref=requested_self_person_ref)
     ORDER BY state.presentation_order,relation.decomposition_ref
$function$;
""")
    _sql("""
CREATE FUNCTION dante._activity_decomposition_contained(
    requested_parent_ref uuid, requested_child_ref uuid,
    replacement_schedule_ref uuid DEFAULT NULL, replacement_state_ref uuid DEFAULT NULL
) RETURNS boolean LANGUAGE sql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
WITH active_placement AS (
    SELECT schedule.subject_native_ref,current.material_state_ref
      FROM dante.schedule AS schedule
      JOIN dante.schedule_current_placement AS current
        ON current.scoped_owner_ref=schedule.schedule_ref
     WHERE schedule.subject_native_ref IN (requested_parent_ref,requested_child_ref)
       AND schedule.schedule_ref IS DISTINCT FROM replacement_schedule_ref
    UNION ALL
    SELECT schedule.subject_native_ref,replacement_state_ref
      FROM dante.schedule AS schedule
     WHERE replacement_state_ref IS NOT NULL
       AND schedule.schedule_ref=replacement_schedule_ref
       AND schedule.subject_native_ref IN (requested_parent_ref,requested_child_ref)
), envelope AS (
    SELECT placement.subject_native_ref,
           COALESCE(absolute.starts_at,zoned.resolved_start_at) AS starts_at,
           COALESCE(absolute.ends_at,zoned.resolved_end_at) AS ends_at,
           dates.date_span
      FROM active_placement AS placement
      JOIN dante.schedule_placement_state AS state
        ON state.material_state_ref=placement.material_state_ref
      LEFT JOIN dante.schedule_placement_absolute_state AS absolute
        ON absolute.material_state_ref=state.material_state_ref
       AND absolute.extent_code='interval'
      LEFT JOIN dante.schedule_placement_named_zone_state AS zoned
        ON zoned.material_state_ref=state.material_state_ref
       AND zoned.extent_code='interval'
      LEFT JOIN dante.schedule_placement_date_state AS dates
        ON dates.material_state_ref=state.material_state_ref
), parent_envelope AS (
    SELECT starts_at,ends_at,date_span
      FROM envelope WHERE subject_native_ref=requested_parent_ref
    UNION ALL
    -- An unplaced parent can admit a timed child only through an accepted,
    -- finite, hard full-placement window. A placed parent uses its Schedule.
    SELECT max(payload.starts_at),min(payload.ends_at),NULL::daterange
      FROM dante.temporal_constraint AS constraint_row
      JOIN dante.scoped_current_material_state AS current_rule
        ON current_rule.scoped_owner_ref=constraint_row.constraint_ref
       AND current_rule.facet_code='temporal_constraint.rule'
      JOIN dante.temporal_constraint_state AS rule
        ON rule.constraint_ref=constraint_row.constraint_ref
       AND rule.material_state_ref=current_rule.material_state_ref
      JOIN dante.temporal_constraint_window_state AS window_rule
        ON window_rule.material_state_ref=rule.material_state_ref
      JOIN dante.temporal_constraint_window_absolute_state AS payload
        ON payload.material_state_ref=window_rule.material_state_ref
     WHERE constraint_row.subject_native_ref=requested_parent_ref
       AND rule.strength_code='hard'
       AND rule.constrained_facet_code='schedule.placement'
       AND window_rule.relationship_code='full_placement_contained'
       AND window_rule.temporal_form_code='absolute'
       AND NOT EXISTS (
           SELECT 1 FROM envelope AS placed_parent
            WHERE placed_parent.subject_native_ref=requested_parent_ref
       )
    HAVING count(*)>0 AND max(payload.starts_at)<min(payload.ends_at)
)
SELECT NOT EXISTS (
    SELECT 1 FROM envelope AS child
     WHERE child.subject_native_ref=requested_child_ref
       AND NOT EXISTS (
           SELECT 1 FROM parent_envelope AS parent
            WHERE (
                  (child.starts_at IS NOT NULL AND child.ends_at IS NOT NULL
                   AND parent.starts_at IS NOT NULL AND parent.ends_at IS NOT NULL
                   AND parent.starts_at<=child.starts_at AND child.ends_at<=parent.ends_at)
                  OR (child.date_span IS NOT NULL AND parent.date_span IS NOT NULL
                      AND child.date_span <@ parent.date_span)
              )
       )
)
$function$;
""")
    _sql("""
CREATE FUNCTION dante.enforce_activity_decomposition_schedule()
RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
DECLARE
    schedule_subject uuid;
    relation record;
    changed_schedule uuid;
    changed_state uuid;
BEGIN
    IF TG_OP='DELETE' THEN
        changed_schedule:=OLD.scoped_owner_ref;
        changed_state:=NULL;
    ELSE
        changed_schedule:=NEW.scoped_owner_ref;
        changed_state:=NEW.material_state_ref;
    END IF;
    IF (CASE WHEN TG_OP='DELETE' THEN OLD.facet_code ELSE NEW.facet_code END)
       IS DISTINCT FROM 'schedule.placement' THEN
        IF TG_OP='DELETE' THEN RETURN OLD; END IF;
        RETURN NEW;
    END IF;
    SELECT schedule.subject_native_ref INTO schedule_subject
      FROM dante.schedule AS schedule WHERE schedule.schedule_ref=changed_schedule;
    IF schedule_subject IS NULL THEN
        IF TG_OP='DELETE' THEN RETURN OLD; END IF;
        RETURN NEW;
    END IF;

    -- Use the same deterministic Activity row order as relation mutation.
    PERFORM 1 FROM dante.activity_intention AS activity
     WHERE activity.activity_ref=schedule_subject
        OR activity.activity_ref IN (
            SELECT CASE WHEN edge.parent_activity_ref=schedule_subject
                        THEN edge.child_activity_ref ELSE edge.parent_activity_ref END
              FROM dante.activity_decomposition AS edge
              JOIN dante.activity_decomposition_current_history AS current_edge
                ON current_edge.decomposition_ref=edge.decomposition_ref
               AND current_edge.current_until_at IS NULL
              JOIN dante.activity_decomposition_state AS edge_state
                ON edge_state.decomposition_ref=edge.decomposition_ref
               AND edge_state.state_ref=current_edge.state_ref
             WHERE edge_state.active
               AND schedule_subject IN (edge.parent_activity_ref,edge.child_activity_ref)
        )
     ORDER BY activity.activity_ref FOR SHARE;

    FOR relation IN
        SELECT edge.parent_activity_ref,edge.child_activity_ref
          FROM dante.activity_decomposition AS edge
          JOIN dante.activity_decomposition_current_history AS current_edge
            ON current_edge.decomposition_ref=edge.decomposition_ref
           AND current_edge.current_until_at IS NULL
          JOIN dante.activity_decomposition_state AS edge_state
            ON edge_state.decomposition_ref=edge.decomposition_ref
           AND edge_state.state_ref=current_edge.state_ref
         WHERE edge_state.active
           AND schedule_subject IN (edge.parent_activity_ref,edge.child_activity_ref)
    LOOP
        IF NOT dante._activity_decomposition_contained(
            relation.parent_activity_ref,relation.child_activity_ref,
            changed_schedule,changed_state
        ) THEN
            RAISE EXCEPTION USING ERRCODE='23514',
                CONSTRAINT='activity_decomposition_temporal_containment',
                MESSAGE='Child Schedule is outside its parent envelope';
        END IF;
    END LOOP;
    IF TG_OP='DELETE' THEN RETURN OLD; END IF;
    RETURN NEW;
END;
$function$;
""")
    _sql("""
CREATE TRIGGER trg_scoped_current_activity_decomposition
BEFORE INSERT OR UPDATE OR DELETE ON dante.scoped_current_material_state
FOR EACH ROW EXECUTE FUNCTION dante.enforce_activity_decomposition_schedule()
""")
    _sql("""
CREATE FUNCTION dante.enforce_activity_decomposition_parent_window()
RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
DECLARE
    constraint_owner uuid;
    child_owner uuid;
BEGIN
    IF (CASE WHEN TG_OP='DELETE' THEN OLD.facet_code ELSE NEW.facet_code END)
       IS DISTINCT FROM 'temporal_constraint.rule' THEN
        IF TG_OP='DELETE' THEN RETURN OLD; END IF;
        RETURN NEW;
    END IF;
    SELECT rule.subject_native_ref INTO constraint_owner
      FROM dante.temporal_constraint AS rule
     WHERE rule.constraint_ref=(CASE WHEN TG_OP='DELETE'
                                     THEN OLD.scoped_owner_ref ELSE NEW.scoped_owner_ref END);
    IF constraint_owner IS NOT NULL THEN
        FOR child_owner IN
            SELECT relation.child_activity_ref
              FROM dante.activity_decomposition AS relation
              JOIN dante.activity_decomposition_current_history AS history
                ON history.decomposition_ref=relation.decomposition_ref
               AND history.current_until_at IS NULL
              JOIN dante.activity_decomposition_state AS state
                ON state.decomposition_ref=relation.decomposition_ref
               AND state.state_ref=history.state_ref
             WHERE relation.parent_activity_ref=constraint_owner AND state.active
        LOOP
            IF NOT dante._activity_decomposition_contained(constraint_owner,child_owner) THEN
                RAISE EXCEPTION USING ERRCODE='23514',
                    CONSTRAINT='activity_decomposition_temporal_containment',
                    MESSAGE='Parent rule would strand a placed child Activity';
            END IF;
        END LOOP;
    END IF;
    IF TG_OP='DELETE' THEN RETURN OLD; END IF;
    RETURN NEW;
END;
$function$;
""")
    _sql("""
CREATE TRIGGER trg_scoped_current_activity_decomposition_window
AFTER INSERT OR UPDATE OR DELETE ON dante.scoped_current_material_state
FOR EACH ROW EXECUTE FUNCTION dante.enforce_activity_decomposition_parent_window()
""")
    _sql("""
CREATE FUNCTION dante.set_self_activity_decomposition(
    requested_self_person_ref uuid, requested_operation_id text,
    requested_intent_fingerprint text, requested_decomposition_ref uuid,
    requested_parent_activity_ref uuid, requested_child_activity_ref uuid,
    requested_state_ref uuid, requested_active boolean,
    requested_requirement_code text, requested_presentation_order integer,
    requested_expected_state_ref uuid
) RETURNS TABLE(decomposition_ref uuid, state_ref uuid, active boolean, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
DECLARE
    prior record;
    owner record;
    owner_present boolean;
    current_state uuid;
    currently_active boolean;
    previous_from timestamptz;
    accepted_at timestamptz;
BEGIN
    IF requested_operation_id IS NULL OR requested_operation_id<>btrim(requested_operation_id)
       OR char_length(requested_operation_id) NOT BETWEEN 1 AND 200
       OR requested_intent_fingerprint IS NULL OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$'
       OR uuid_extract_version(requested_decomposition_ref) IS DISTINCT FROM 7
       OR uuid_extract_version(requested_state_ref) IS DISTINCT FROM 7
       OR requested_parent_activity_ref IS NULL OR requested_child_activity_ref IS NULL
       OR requested_parent_activity_ref=requested_child_activity_ref
       OR requested_active IS NULL
       OR requested_requirement_code IS NULL
       OR requested_requirement_code NOT IN ('required','optional')
       OR requested_presentation_order IS NULL OR requested_presentation_order<=0 THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='activity_decomposition_invalid',
            MESSAGE='Activity decomposition command rejected';
    END IF;

    -- The two Activity rows serialize competing parents, depth changes and attach/detach.
    PERFORM 1 FROM dante.activity_intention AS activity
     WHERE activity.activity_ref IN (requested_parent_activity_ref,requested_child_activity_ref)
       AND activity.self_person_ref=requested_self_person_ref
     ORDER BY activity.activity_ref FOR UPDATE;
    IF (SELECT count(*) FROM dante.activity_intention AS activity
         WHERE activity.activity_ref IN (requested_parent_activity_ref,requested_child_activity_ref)
           AND activity.self_person_ref=requested_self_person_ref)<>2 THEN
        RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='activity_decomposition_owner_unavailable',
            MESSAGE='Parent or child Activity unavailable';
    END IF;

    SELECT * INTO prior FROM dante.activity_decomposition_operation AS operation
     WHERE operation.self_person_ref=requested_self_person_ref
       AND operation.operation_id=requested_operation_id;
    IF FOUND THEN
        IF prior.intent_fingerprint IS DISTINCT FROM requested_intent_fingerprint
           OR (requested_expected_state_ref IS NOT NULL
               AND prior.decomposition_ref IS DISTINCT FROM requested_decomposition_ref) THEN
            RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='activity_decomposition_operation_reused',
                MESSAGE='Activity decomposition operation was reused';
        END IF;
        RETURN QUERY SELECT prior.decomposition_ref,prior.state_ref,state.active,true
          FROM dante.activity_decomposition_state AS state WHERE state.state_ref=prior.state_ref;
        RETURN;
    END IF;

    SELECT * INTO owner FROM dante.activity_decomposition AS relation
     WHERE relation.decomposition_ref=requested_decomposition_ref;
    owner_present:=FOUND;
    IF FOUND THEN
        IF owner.self_person_ref IS DISTINCT FROM requested_self_person_ref
           OR owner.parent_activity_ref IS DISTINCT FROM requested_parent_activity_ref
           OR owner.child_activity_ref IS DISTINCT FROM requested_child_activity_ref THEN
            RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='activity_decomposition_relation_unavailable',
                MESSAGE='Activity decomposition relation unavailable';
        END IF;
    ELSIF requested_expected_state_ref IS NOT NULL OR NOT requested_active THEN
        RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='activity_decomposition_relation_unavailable',
            MESSAGE='Activity decomposition relation unavailable';
    END IF;

    SELECT history.state_ref,state.active,history.current_from_at
      INTO current_state,currently_active,previous_from
      FROM dante.activity_decomposition_current_history AS history
      JOIN dante.activity_decomposition_state AS state ON state.state_ref=history.state_ref
     WHERE history.decomposition_ref=requested_decomposition_ref AND history.current_until_at IS NULL;
    IF current_state IS DISTINCT FROM requested_expected_state_ref THEN
        RAISE EXCEPTION USING ERRCODE='40001', CONSTRAINT='activity_decomposition_current_conflict',
            MESSAGE='Activity decomposition state changed';
    END IF;
    IF current_state IS NOT NULL AND NOT currently_active AND requested_active THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='activity_decomposition_retired',
            MESSAGE='Retired relation cannot be reactivated';
    END IF;

    IF requested_active THEN
        IF EXISTS (
            SELECT 1 FROM dante.activity_decomposition AS relation
            JOIN dante.activity_decomposition_current_history AS history
              ON history.decomposition_ref=relation.decomposition_ref AND history.current_until_at IS NULL
            JOIN dante.activity_decomposition_state AS state
              ON state.decomposition_ref=relation.decomposition_ref AND state.state_ref=history.state_ref
           WHERE state.active AND relation.decomposition_ref<>requested_decomposition_ref
             AND relation.child_activity_ref=requested_child_activity_ref
        ) OR EXISTS (
            SELECT 1 FROM dante.activity_decomposition AS relation
            JOIN dante.activity_decomposition_current_history AS history
              ON history.decomposition_ref=relation.decomposition_ref AND history.current_until_at IS NULL
            JOIN dante.activity_decomposition_state AS state
              ON state.decomposition_ref=relation.decomposition_ref AND state.state_ref=history.state_ref
           WHERE state.active AND (relation.child_activity_ref=requested_parent_activity_ref
                OR relation.parent_activity_ref=requested_child_activity_ref)
        ) THEN
            RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='activity_decomposition_depth_or_parent',
                MESSAGE='Activity decomposition parent or depth conflict';
        END IF;
        IF NOT dante._activity_decomposition_contained(
            requested_parent_activity_ref,requested_child_activity_ref
        ) THEN
            RAISE EXCEPTION USING ERRCODE='23514',
                CONSTRAINT='activity_decomposition_temporal_containment',
                MESSAGE='Child Schedule is outside its parent envelope';
        END IF;
    END IF;
    accepted_at:=statement_timestamp();
    IF previous_from IS NOT NULL AND accepted_at<=previous_from THEN
        accepted_at:=previous_from + interval '1 microsecond';
    END IF;
    IF NOT owner_present THEN
        INSERT INTO dante.activity_decomposition(
            decomposition_ref,self_person_ref,parent_activity_ref,child_activity_ref,created_at
        ) VALUES(requested_decomposition_ref,requested_self_person_ref,
                 requested_parent_activity_ref,requested_child_activity_ref,accepted_at);
    END IF;
    INSERT INTO dante.activity_decomposition_state(
        state_ref,decomposition_ref,active,requirement_code,presentation_order,recorded_at
    ) VALUES(requested_state_ref,requested_decomposition_ref,requested_active,
             requested_requirement_code,requested_presentation_order,accepted_at);
    IF current_state IS NOT NULL THEN
        UPDATE dante.activity_decomposition_current_history AS history
           SET current_until_at=accepted_at
         WHERE history.decomposition_ref=requested_decomposition_ref AND history.current_until_at IS NULL;
    END IF;
    INSERT INTO dante.activity_decomposition_current_history(
        decomposition_ref,state_ref,current_from_at,current_until_at
    ) VALUES(requested_decomposition_ref,requested_state_ref,accepted_at,NULL);
    INSERT INTO dante.activity_decomposition_operation(
        self_person_ref,operation_id,intent_fingerprint,decomposition_ref,state_ref
    ) VALUES(requested_self_person_ref,requested_operation_id,
             requested_intent_fingerprint,requested_decomposition_ref,requested_state_ref);
    RETURN QUERY SELECT requested_decomposition_ref,requested_state_ref,requested_active,false;
END;
$function$;
""")
    for signature in (
        "dante.get_self_activity_decomposition(uuid,uuid)",
        "dante._activity_decomposition_contained(uuid,uuid,uuid,uuid)",
        "dante.enforce_activity_decomposition_schedule()",
        "dante.enforce_activity_decomposition_parent_window()",
        "dante.set_self_activity_decomposition(uuid,text,text,uuid,uuid,uuid,uuid,boolean,text,integer,uuid)",
    ):
        _sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
        _sql(f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator")
        if signature.startswith(("dante.get_self", "dante.set_self")):
            _sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")
    for table in (
        "activity_decomposition",
        "activity_decomposition_state",
        "activity_decomposition_current_history",
        "activity_decomposition_operation",
    ):
        _sql(f"REVOKE ALL ON TABLE dante.{table} FROM PUBLIC,dante_runtime,dante_migrator")


def downgrade() -> None:
    raise RuntimeError("B14-U6 decomposition requires a reviewed forward migration")
