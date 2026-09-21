# ruff: noqa: S608
"""B06-A: Routine source core and typed product organization.

Routine is a self-owned recurrence source.  It is deliberately neither an
Activity nor a recurrence state nor an occurrence: those joins begin in B06-B
and B06-C respectively.

Revision ID: 20260921_49
Revises: 20260921_48
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260921_49"
down_revision: str | None = "20260921_48"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _sql(value: str) -> None:
    op.execute(sa.text(value))


def _fk(column: str, target: str, name: str) -> sa.ForeignKeyConstraint:
    return sa.ForeignKeyConstraint(
        [column],
        [f"dante.{target}.{ 'person_ref' if target == 'person' else column}"],
        name=name,
        onupdate="NO ACTION",
        ondelete="NO ACTION",
        deferrable=False,
    )


def upgrade() -> None:
    op.create_table(
        "routine_intention",
        sa.Column("routine_ref", sa.Uuid(), nullable=False),
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("lifecycle_state", sa.Text(), nullable=False),
        sa.Column("source_revision", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("lifecycle_changed_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("routine_ref", name=op.f("pk_routine_intention")),
        _fk("routine_ref", "routine", "fk_routine_intention_routine"),
        _fk("self_person_ref", "person", "fk_routine_intention_person"),
        sa.CheckConstraint(
            "title=btrim(title) AND title<>'' AND char_length(title)<=300",
            name=op.f("ck_routine_intention_title"),
        ),
        sa.CheckConstraint(
            "lifecycle_state IN ('active','paused','ended')",
            name=op.f("ck_routine_intention_lifecycle"),
        ),
        sa.CheckConstraint("source_revision>=1", name=op.f("ck_routine_intention_revision")),
        schema="dante",
    )
    op.create_index(
        "ix_routine_intention_self_person_created",
        "routine_intention",
        ["self_person_ref", "created_at", "routine_ref"],
        schema="dante",
    )
    op.create_table(
        "routine_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("routine_ref", sa.Uuid(), nullable=False),
        sa.Column("kind", sa.Text(), nullable=False),
        sa.Column("expected_source_revision", sa.BigInteger(), nullable=False),
        sa.Column("accepted_source_revision", sa.BigInteger(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("self_person_ref", "operation_id", name=op.f("pk_routine_operation")),
        _fk("self_person_ref", "person", "fk_routine_operation_person"),
        _fk("routine_ref", "routine", "fk_routine_operation_routine"),
        sa.CheckConstraint("operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200", name=op.f("ck_routine_operation_id")),
        sa.CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name=op.f("ck_routine_operation_fingerprint")),
        sa.CheckConstraint("kind IN ('create','rename','pause','resume','end')", name=op.f("ck_routine_operation_kind")),
        sa.CheckConstraint("expected_source_revision>=0", name=op.f("ck_routine_operation_expected")),
        sa.CheckConstraint("accepted_source_revision=expected_source_revision+1", name=op.f("ck_routine_operation_accepted")),
        schema="dante",
    )
    op.create_table(
        "routine_life_area_assignment",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("routine_ref", sa.Uuid(), nullable=False),
        sa.Column("life_area_ref", sa.Uuid(), nullable=False),
        sa.Column("revision", sa.BigInteger(), nullable=False),
        sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("self_person_ref", "routine_ref", name=op.f("pk_routine_life_area_assignment")),
        _fk("self_person_ref", "person", "fk_routine_life_area_assignment_person"),
        _fk("routine_ref", "routine", "fk_routine_life_area_assignment_routine"),
        _fk("life_area_ref", "life_area", "fk_routine_life_area_assignment_life_area"),
        sa.CheckConstraint("revision>=1", name=op.f("ck_routine_life_area_assignment_revision")),
        schema="dante",
    )
    op.create_index("ix_routine_life_area_assignment_self_person_life_area", "routine_life_area_assignment", ["self_person_ref", "life_area_ref", "routine_ref"], schema="dante")
    op.create_table(
        "routine_life_area_assignment_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("routine_ref", sa.Uuid(), nullable=False),
        sa.Column("life_area_ref", sa.Uuid(), nullable=False),
        sa.Column("expected_revision", sa.BigInteger(), nullable=False),
        sa.Column("accepted_revision", sa.BigInteger(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("self_person_ref", "operation_id", name=op.f("pk_routine_life_area_assignment_operation")),
        _fk("self_person_ref", "person", "fk_routine_area_op_person"),
        _fk("routine_ref", "routine", "fk_routine_area_op_routine"),
        _fk("life_area_ref", "life_area", "fk_routine_area_op_life_area"),
        sa.CheckConstraint("operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200", name=op.f("ck_routine_area_op_id")),
        sa.CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name=op.f("ck_routine_area_op_fingerprint")),
        sa.CheckConstraint("expected_revision>=0", name=op.f("ck_routine_area_op_expected")),
        sa.CheckConstraint("accepted_revision=expected_revision+1", name=op.f("ck_routine_area_op_accepted")),
        schema="dante",
    )
    op.create_table(
        "routine_tag",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("routine_ref", sa.Uuid(), nullable=False),
        sa.Column("tag_ref", sa.Uuid(), nullable=False),
        sa.Column("attached_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("self_person_ref", "routine_ref", "tag_ref", name=op.f("pk_routine_tag")),
        _fk("self_person_ref", "person", "fk_routine_tag_person"),
        _fk("routine_ref", "routine", "fk_routine_tag_routine"),
        _fk("tag_ref", "product_tag", "fk_routine_tag_tag"),
        schema="dante",
    )
    op.create_index("ix_routine_tag_self_person_tag", "routine_tag", ["self_person_ref", "tag_ref", "routine_ref"], schema="dante")
    op.create_table(
        "routine_tag_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("routine_ref", sa.Uuid(), nullable=False),
        sa.Column("tag_ref", sa.Uuid(), nullable=False),
        sa.Column("attached", sa.Boolean(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("self_person_ref", "operation_id", name=op.f("pk_routine_tag_operation")),
        _fk("self_person_ref", "person", "fk_routine_tag_op_person"),
        _fk("routine_ref", "routine", "fk_routine_tag_op_routine"),
        _fk("tag_ref", "product_tag", "fk_routine_tag_op_tag"),
        sa.CheckConstraint("operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200", name=op.f("ck_routine_tag_op_id")),
        sa.CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name=op.f("ck_routine_tag_op_fingerprint")),
        schema="dante",
    )

    _sql(_CREATE_ROUTINE)
    _sql(_MUTATE_ROUTINE)
    _sql(_ASSIGN_AREA)
    _sql(_SET_TAG)
    _sql(_LIST_ROUTINES)
    _sql(_LIST_TAGS)
    _sql(_LIST_ITEM_TAGS)
    for function in ("create_self_routine", "mutate_self_routine", "assign_self_routine_life_area", "set_self_routine_tag", "list_self_routines", "list_self_routine_tags"):
        _sql(f"REVOKE ALL ON FUNCTION dante.{function} FROM PUBLIC")
        _sql(f"GRANT EXECUTE ON FUNCTION dante.{function} TO dante_runtime")


def downgrade() -> None:
    for function in ("list_self_routine_tags", "list_self_routines", "set_self_routine_tag", "assign_self_routine_life_area", "mutate_self_routine", "create_self_routine"):
        _sql(f"DROP FUNCTION IF EXISTS dante.{function} CASCADE")
    for table in ("routine_tag_operation", "routine_tag", "routine_life_area_assignment_operation", "routine_life_area_assignment", "routine_operation", "routine_intention"):
        op.drop_table(table, schema="dante")


_CREATE_ROUTINE = r'''
CREATE FUNCTION dante.create_self_routine(
    requested_self_person_ref uuid, requested_operation_id text,
    requested_intent_fingerprint text, requested_routine_ref uuid,
    requested_title text, requested_life_area_ref uuid, requested_tag_refs uuid[]
) RETURNS TABLE(routine_ref uuid, source_revision bigint, life_area_assignment_revision bigint,
                accepted_at timestamptz, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path = pg_catalog, dante, pg_temp AS $function$
#variable_conflict error
DECLARE
    key text := btrim(requested_operation_id); label text := btrim(requested_title);
    previous record; recorded_at timestamptz := statement_timestamp();
BEGIN
    IF key IS NULL OR key='' OR char_length(key)>200 OR label IS NULL OR label='' OR char_length(label)>300
       OR requested_intent_fingerprint IS NULL OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$'
       OR uuid_extract_version(requested_routine_ref) IS DISTINCT FROM 7 THEN
        RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Routine create command rejected';
    END IF;
    IF requested_tag_refs IS NOT NULL AND cardinality(requested_tag_refs)<>cardinality(ARRAY(SELECT DISTINCT value FROM unnest(requested_tag_refs) AS value)) THEN
        RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Routine create tags must be unique';
    END IF;
    PERFORM 1 FROM dante.person WHERE person_ref=requested_self_person_ref FOR UPDATE;
    IF NOT FOUND OR NOT EXISTS (SELECT 1 FROM dante.account_application_context WHERE self_person_ref=requested_self_person_ref) THEN
        RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Routine self context unavailable';
    END IF;
    SELECT * INTO previous FROM dante.routine_operation WHERE self_person_ref=requested_self_person_ref AND operation_id=key;
    IF FOUND THEN
        IF previous.intent_fingerprint<>requested_intent_fingerprint OR previous.kind<>'create' THEN
            RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_routine_operation', MESSAGE='Routine operation id reused';
        END IF;
        RETURN QUERY SELECT previous.routine_ref,previous.accepted_source_revision,1::bigint,previous.accepted_at,true; RETURN;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM dante.life_area WHERE life_area_ref=requested_life_area_ref AND self_person_ref=requested_self_person_ref AND archived=false) THEN
        RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='routine_life_area_unavailable', MESSAGE='Routine Life Area unavailable';
    END IF;
    IF requested_tag_refs IS NOT NULL AND EXISTS (
        SELECT 1 FROM unnest(requested_tag_refs) AS wanted(tag_ref) LEFT JOIN dante.product_tag AS tag
        ON tag.tag_ref=wanted.tag_ref AND tag.self_person_ref=requested_self_person_ref AND tag.archived=false
        WHERE tag.tag_ref IS NULL
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='routine_tag_unavailable', MESSAGE='Routine Tag unavailable';
    END IF;
    INSERT INTO dante.routine(routine_ref) VALUES(requested_routine_ref);
    INSERT INTO dante.routine_intention(routine_ref,self_person_ref,title,lifecycle_state,source_revision,created_at,updated_at,lifecycle_changed_at)
    VALUES(requested_routine_ref,requested_self_person_ref,label,'active',1,recorded_at,recorded_at,recorded_at);
    INSERT INTO dante.routine_life_area_assignment(self_person_ref,routine_ref,life_area_ref,revision,assigned_at)
    VALUES(requested_self_person_ref,requested_routine_ref,requested_life_area_ref,1,recorded_at);
    INSERT INTO dante.routine_tag(self_person_ref,routine_ref,tag_ref,attached_at)
    SELECT requested_self_person_ref,requested_routine_ref,tag_ref,recorded_at FROM unnest(COALESCE(requested_tag_refs,ARRAY[]::uuid[])) AS tags(tag_ref);
    INSERT INTO dante.routine_operation(self_person_ref,operation_id,intent_fingerprint,routine_ref,kind,expected_source_revision,accepted_source_revision,accepted_at)
    VALUES(requested_self_person_ref,key,requested_intent_fingerprint,requested_routine_ref,'create',0,1,recorded_at);
    RETURN QUERY SELECT requested_routine_ref,1::bigint,1::bigint,recorded_at,false;
END;
$function$;
'''

_MUTATE_ROUTINE = r'''
CREATE FUNCTION dante.mutate_self_routine(
    requested_self_person_ref uuid, requested_operation_id text, requested_intent_fingerprint text,
    requested_routine_ref uuid, requested_expected_source_revision bigint, requested_kind text,
    requested_title text
) RETURNS TABLE(routine_ref uuid, source_revision bigint, lifecycle_state text, accepted_at timestamptz, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path = pg_catalog, dante, pg_temp AS $function$
#variable_conflict error
DECLARE
    key text := btrim(requested_operation_id); label text := btrim(requested_title);
    prior record; current_row record; recorded_at timestamptz := statement_timestamp();
BEGIN
    IF key IS NULL OR key='' OR char_length(key)>200 OR requested_intent_fingerprint IS NULL OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$'
       OR requested_expected_source_revision IS NULL OR requested_expected_source_revision<1
       OR requested_kind NOT IN ('rename','pause','resume','end')
       OR (requested_kind='rename' AND (label IS NULL OR label='' OR char_length(label)>300))
       OR (requested_kind<>'rename' AND requested_title IS NOT NULL) THEN
        RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Routine mutation command rejected';
    END IF;
    PERFORM 1 FROM dante.person WHERE person_ref=requested_self_person_ref FOR UPDATE;
    IF NOT FOUND OR NOT EXISTS (SELECT 1 FROM dante.account_application_context WHERE self_person_ref=requested_self_person_ref) THEN
        RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Routine self context unavailable';
    END IF;
    SELECT * INTO prior FROM dante.routine_operation WHERE self_person_ref=requested_self_person_ref AND operation_id=key;
    IF FOUND THEN
        IF prior.intent_fingerprint<>requested_intent_fingerprint OR prior.routine_ref<>requested_routine_ref OR prior.kind<>requested_kind OR prior.expected_source_revision<>requested_expected_source_revision THEN
            RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_routine_operation', MESSAGE='Routine operation id reused';
        END IF;
        SELECT lifecycle_state INTO current_row FROM dante.routine_intention WHERE routine_ref=requested_routine_ref;
        RETURN QUERY SELECT prior.routine_ref,prior.accepted_source_revision,current_row.lifecycle_state,prior.accepted_at,true; RETURN;
    END IF;
    SELECT * INTO current_row FROM dante.routine_intention WHERE routine_ref=requested_routine_ref AND self_person_ref=requested_self_person_ref FOR UPDATE;
    IF NOT FOUND THEN RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='routine_unavailable', MESSAGE='Routine unavailable'; END IF;
    IF current_row.source_revision<>requested_expected_source_revision
       OR (requested_kind='rename' AND current_row.title=label)
       OR (requested_kind='pause' AND current_row.lifecycle_state<>'active')
       OR (requested_kind='resume' AND current_row.lifecycle_state<>'paused')
       OR (requested_kind='end' AND current_row.lifecycle_state='ended') THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='routine_source_conflict', MESSAGE='Routine source state changed';
    END IF;
    UPDATE dante.routine_intention SET title=CASE WHEN requested_kind='rename' THEN label ELSE title END,
      lifecycle_state=CASE WHEN requested_kind='pause' THEN 'paused' WHEN requested_kind='resume' THEN 'active' WHEN requested_kind='end' THEN 'ended' ELSE lifecycle_state END,
      source_revision=source_revision+1,updated_at=recorded_at,
      lifecycle_changed_at=CASE WHEN requested_kind IN ('pause','resume','end') THEN recorded_at ELSE lifecycle_changed_at END
      WHERE routine_ref=requested_routine_ref;
    INSERT INTO dante.routine_operation(self_person_ref,operation_id,intent_fingerprint,routine_ref,kind,expected_source_revision,accepted_source_revision,accepted_at)
    VALUES(requested_self_person_ref,key,requested_intent_fingerprint,requested_routine_ref,requested_kind,requested_expected_source_revision,requested_expected_source_revision+1,recorded_at);
    SELECT lifecycle_state INTO current_row FROM dante.routine_intention WHERE routine_ref=requested_routine_ref;
    RETURN QUERY SELECT requested_routine_ref,requested_expected_source_revision+1,current_row.lifecycle_state,recorded_at,false;
END;
$function$;
'''

_ASSIGN_AREA = r'''
CREATE FUNCTION dante.assign_self_routine_life_area(
 requested_self_person_ref uuid, requested_operation_id text, requested_intent_fingerprint text,
 requested_routine_ref uuid, requested_life_area_ref uuid, requested_expected_revision bigint
) RETURNS TABLE(life_area_ref uuid, assignment_revision bigint, assigned_at timestamptz, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE SET search_path = pg_catalog, dante, pg_temp AS $function$
#variable_conflict error
DECLARE key text:=btrim(requested_operation_id); prior record; current_row record; recorded_at timestamptz:=statement_timestamp();
BEGIN
 IF key IS NULL OR key='' OR char_length(key)>200 OR requested_intent_fingerprint IS NULL OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$' OR requested_expected_revision IS NULL OR requested_expected_revision<1 THEN RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Routine Life Area command rejected'; END IF;
 PERFORM 1 FROM dante.person WHERE person_ref=requested_self_person_ref FOR UPDATE;
 IF NOT FOUND OR NOT EXISTS(SELECT 1 FROM dante.account_application_context WHERE self_person_ref=requested_self_person_ref) THEN RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Routine self context unavailable'; END IF;
 SELECT * INTO prior FROM dante.routine_life_area_assignment_operation WHERE self_person_ref=requested_self_person_ref AND operation_id=key;
 IF FOUND THEN IF prior.intent_fingerprint<>requested_intent_fingerprint OR prior.routine_ref<>requested_routine_ref OR prior.life_area_ref<>requested_life_area_ref OR prior.expected_revision<>requested_expected_revision THEN RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_routine_life_area_assignment_operation', MESSAGE='Routine Life Area operation id reused'; END IF; RETURN QUERY SELECT prior.life_area_ref,prior.accepted_revision,prior.accepted_at,true; RETURN; END IF;
 IF NOT EXISTS(SELECT 1 FROM dante.routine_intention WHERE routine_ref=requested_routine_ref AND self_person_ref=requested_self_person_ref) THEN RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='routine_unavailable', MESSAGE='Routine unavailable'; END IF;
 IF NOT EXISTS(SELECT 1 FROM dante.life_area WHERE life_area_ref=requested_life_area_ref AND self_person_ref=requested_self_person_ref AND archived=false) THEN RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='routine_life_area_unavailable', MESSAGE='Routine Life Area unavailable'; END IF;
 SELECT * INTO current_row FROM dante.routine_life_area_assignment WHERE self_person_ref=requested_self_person_ref AND routine_ref=requested_routine_ref FOR UPDATE;
 IF current_row.revision<>requested_expected_revision OR current_row.life_area_ref=requested_life_area_ref THEN RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='routine_life_area_conflict', MESSAGE='Routine Life Area state changed'; END IF;
 UPDATE dante.routine_life_area_assignment SET life_area_ref=requested_life_area_ref,revision=revision+1,assigned_at=recorded_at WHERE self_person_ref=requested_self_person_ref AND routine_ref=requested_routine_ref;
 INSERT INTO dante.routine_life_area_assignment_operation VALUES(requested_self_person_ref,key,requested_intent_fingerprint,requested_routine_ref,requested_life_area_ref,requested_expected_revision,requested_expected_revision+1,recorded_at);
 RETURN QUERY SELECT requested_life_area_ref,requested_expected_revision+1,recorded_at,false;
END;
$function$;
'''

_SET_TAG = r'''
CREATE FUNCTION dante.set_self_routine_tag(
 requested_self_person_ref uuid, requested_operation_id text, requested_intent_fingerprint text,
 requested_routine_ref uuid, requested_tag_ref uuid, requested_attached boolean
) RETURNS TABLE(attached boolean, accepted_at timestamptz, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE SET search_path = pg_catalog, dante, pg_temp AS $function$
#variable_conflict error
DECLARE key text:=btrim(requested_operation_id); prior record; exists_now boolean; recorded_at timestamptz:=statement_timestamp();
BEGIN
 IF key IS NULL OR key='' OR char_length(key)>200 OR requested_intent_fingerprint IS NULL OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$' OR requested_attached IS NULL THEN RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Routine Tag command rejected'; END IF;
 PERFORM 1 FROM dante.person WHERE person_ref=requested_self_person_ref FOR UPDATE;
 IF NOT FOUND OR NOT EXISTS(SELECT 1 FROM dante.account_application_context WHERE self_person_ref=requested_self_person_ref) THEN RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Routine self context unavailable'; END IF;
 SELECT * INTO prior FROM dante.routine_tag_operation WHERE self_person_ref=requested_self_person_ref AND operation_id=key;
 IF FOUND THEN IF prior.intent_fingerprint<>requested_intent_fingerprint OR prior.routine_ref<>requested_routine_ref OR prior.tag_ref<>requested_tag_ref OR prior.attached<>requested_attached THEN RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_routine_tag_operation', MESSAGE='Routine Tag operation id reused'; END IF; RETURN QUERY SELECT prior.attached,prior.accepted_at,true; RETURN; END IF;
 IF NOT EXISTS(SELECT 1 FROM dante.routine_intention WHERE routine_ref=requested_routine_ref AND self_person_ref=requested_self_person_ref) THEN RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='routine_unavailable', MESSAGE='Routine unavailable'; END IF;
 IF NOT EXISTS(SELECT 1 FROM dante.product_tag WHERE tag_ref=requested_tag_ref AND self_person_ref=requested_self_person_ref AND (requested_attached=false OR archived=false)) THEN RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='routine_tag_unavailable', MESSAGE='Routine Tag unavailable'; END IF;
 SELECT EXISTS(SELECT 1 FROM dante.routine_tag WHERE self_person_ref=requested_self_person_ref AND routine_ref=requested_routine_ref AND tag_ref=requested_tag_ref) INTO exists_now;
 IF exists_now=requested_attached THEN RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='routine_tag_no_change', MESSAGE='Routine Tag already has requested state'; END IF;
 IF requested_attached THEN INSERT INTO dante.routine_tag VALUES(requested_self_person_ref,requested_routine_ref,requested_tag_ref,recorded_at); ELSE DELETE FROM dante.routine_tag WHERE self_person_ref=requested_self_person_ref AND routine_ref=requested_routine_ref AND tag_ref=requested_tag_ref; END IF;
 INSERT INTO dante.routine_tag_operation VALUES(requested_self_person_ref,key,requested_intent_fingerprint,requested_routine_ref,requested_tag_ref,requested_attached,recorded_at);
 RETURN QUERY SELECT requested_attached,recorded_at,false;
END;
$function$;
'''

_LIST_ROUTINES = r'''
CREATE FUNCTION dante.list_self_routines(requested_self_person_ref uuid)
RETURNS TABLE(routine_ref uuid,title text,lifecycle_state text,source_revision bigint,created_at timestamptz,updated_at timestamptz,lifecycle_changed_at timestamptz,life_area_ref uuid,life_area_assignment_revision bigint,life_area_assigned_at timestamptz)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE SET search_path = pg_catalog, dante, pg_temp AS $function$
 SELECT source.routine_ref,source.title,source.lifecycle_state,source.source_revision,source.created_at,source.updated_at,source.lifecycle_changed_at,area.life_area_ref,area.revision,area.assigned_at
 FROM dante.routine_intention AS source JOIN dante.routine_life_area_assignment AS area ON area.routine_ref=source.routine_ref AND area.self_person_ref=source.self_person_ref
 WHERE source.self_person_ref=requested_self_person_ref ORDER BY source.created_at,source.routine_ref
$function$;
'''

_LIST_TAGS = r'''
CREATE FUNCTION dante.list_self_routine_tags(requested_self_person_ref uuid)
RETURNS TABLE(routine_ref uuid,tag_ref uuid,attached_at timestamptz)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE SET search_path = pg_catalog, dante, pg_temp AS $function$
 SELECT routine_ref,tag_ref,attached_at FROM dante.routine_tag WHERE self_person_ref=requested_self_person_ref ORDER BY routine_ref,attached_at,tag_ref
$function$;
'''

_LIST_ITEM_TAGS = r'''
CREATE OR REPLACE FUNCTION dante.list_self_item_tags(requested_self_person_ref uuid)
RETURNS TABLE(subject_kind text, subject_native_ref uuid, tag_ref uuid, attached_at timestamptz)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE SET search_path = pg_catalog, dante, pg_temp AS $function$
 SELECT 'activity'::text,edge.activity_ref,edge.tag_ref,edge.attached_at FROM dante.activity_tag AS edge
  WHERE edge.self_person_ref=requested_self_person_ref AND EXISTS(SELECT 1 FROM dante.account_application_context WHERE self_person_ref=requested_self_person_ref)
 UNION ALL
 SELECT 'event'::text,edge.event_ref,edge.tag_ref,edge.attached_at FROM dante.event_tag AS edge
  WHERE edge.self_person_ref=requested_self_person_ref AND EXISTS(SELECT 1 FROM dante.account_application_context WHERE self_person_ref=requested_self_person_ref)
 UNION ALL
 SELECT 'routine'::text,edge.routine_ref,edge.tag_ref,edge.attached_at FROM dante.routine_tag AS edge
  WHERE edge.self_person_ref=requested_self_person_ref AND EXISTS(SELECT 1 FROM dante.account_application_context WHERE self_person_ref=requested_self_person_ref)
 ORDER BY 1,2,3
$function$;
'''
