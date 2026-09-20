# ruff: noqa: S608
"""B05-C: actor-local product Tags and typed Activity/Event secondary edges.

Revision ID: 20260920_47
Revises: 20260920_46
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260920_47"
down_revision: str | None = "20260920_46"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _sql(statement: str) -> None:
    op.execute(sa.text(statement))


def _foreign_key(column: str, target: str, name: str) -> sa.ForeignKeyConstraint:
    target_column = "person_ref" if target == "person" else column
    return sa.ForeignKeyConstraint(
        [column],
        [f"dante.{target}.{target_column}"],
        name=name,
        onupdate="NO ACTION",
        ondelete="NO ACTION",
        deferrable=False,
    )


def _tables() -> None:
    op.create_table(
        "product_tag",
        sa.Column("tag_ref", sa.Uuid(), nullable=False),
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("revision", sa.BigInteger(), nullable=False),
        sa.Column("archived", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("tag_ref", name=op.f("pk_product_tag")),
        _foreign_key("self_person_ref", "person", "fk_product_tag_self_person_ref_person"),
        sa.CheckConstraint(
            "uuid_extract_version(tag_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_product_tag_uuidv7"),
        ),
        sa.CheckConstraint(
            "name=btrim(name) AND name<>'' AND char_length(name)<=100",
            name=op.f("ck_product_tag_name"),
        ),
        sa.CheckConstraint("revision>=1", name=op.f("ck_product_tag_revision")),
        schema="dante",
    )
    op.create_index(
        "ix_product_tag_self_person_created",
        "product_tag",
        ["self_person_ref", "created_at", "tag_ref"],
        schema="dante",
    )
    op.create_table(
        "product_tag_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("tag_ref", sa.Uuid(), nullable=False),
        sa.Column("kind", sa.Text(), nullable=False),
        sa.Column("expected_revision", sa.BigInteger(), nullable=False),
        sa.Column("accepted_revision", sa.BigInteger(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref", "operation_id", name=op.f("pk_product_tag_operation")
        ),
        _foreign_key("self_person_ref", "person", "fk_product_tag_operation_person"),
        _foreign_key("tag_ref", "product_tag", "fk_product_tag_operation_tag"),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name=op.f("ck_product_tag_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_product_tag_operation_fingerprint"),
        ),
        sa.CheckConstraint(
            "kind IN ('create','rename','archive')", name=op.f("ck_product_tag_operation_kind")
        ),
        sa.CheckConstraint("expected_revision>=0", name=op.f("ck_product_tag_operation_expected")),
        sa.CheckConstraint(
            "accepted_revision=expected_revision+1", name=op.f("ck_product_tag_operation_accepted")
        ),
        schema="dante",
    )
    for kind in ("activity", "event"):
        edge = f"{kind}_tag"
        receipt = f"{kind}_tag_operation"
        op.create_table(
            edge,
            sa.Column("self_person_ref", sa.Uuid(), nullable=False),
            sa.Column(f"{kind}_ref", sa.Uuid(), nullable=False),
            sa.Column("tag_ref", sa.Uuid(), nullable=False),
            sa.Column("attached_at", sa.DateTime(timezone=True), nullable=False),
            sa.PrimaryKeyConstraint(
                "self_person_ref", f"{kind}_ref", "tag_ref", name=op.f(f"pk_{edge}")
            ),
            _foreign_key("self_person_ref", "person", f"fk_{edge}_person"),
            _foreign_key(f"{kind}_ref", kind, f"fk_{edge}_{kind}"),
            _foreign_key("tag_ref", "product_tag", f"fk_{edge}_tag"),
            schema="dante",
        )
        op.create_index(
            f"ix_{edge}_self_person_tag",
            edge,
            ["self_person_ref", "tag_ref", f"{kind}_ref"],
            schema="dante",
        )
        op.create_table(
            receipt,
            sa.Column("self_person_ref", sa.Uuid(), nullable=False),
            sa.Column("operation_id", sa.Text(), nullable=False),
            sa.Column("intent_fingerprint", sa.Text(), nullable=False),
            sa.Column(f"{kind}_ref", sa.Uuid(), nullable=False),
            sa.Column("tag_ref", sa.Uuid(), nullable=False),
            sa.Column("attached", sa.Boolean(), nullable=False),
            sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
            sa.PrimaryKeyConstraint("self_person_ref", "operation_id", name=op.f(f"pk_{receipt}")),
            _foreign_key("self_person_ref", "person", f"fk_{receipt}_person"),
            _foreign_key(f"{kind}_ref", kind, f"fk_{receipt}_{kind}"),
            _foreign_key("tag_ref", "product_tag", f"fk_{receipt}_tag"),
            sa.CheckConstraint(
                "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
                name=op.f(f"ck_{receipt}_id"),
            ),
            sa.CheckConstraint(
                "intent_fingerprint ~ '^[0-9a-f]{64}$'", name=op.f(f"ck_{receipt}_fingerprint")
            ),
            schema="dante",
        )


_CREATE = r"""
CREATE FUNCTION dante.create_self_product_tag(
    requested_self_person_ref uuid, requested_operation_id text,
    requested_intent_fingerprint text, requested_tag_ref uuid, requested_name text
)
RETURNS TABLE(tag_ref uuid, accepted_revision bigint, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path = pg_catalog, dante, pg_temp
AS $function$
#variable_conflict error
DECLARE
    key text := btrim(requested_operation_id);
    label text := btrim(requested_name);
    prior record;
    recorded_at timestamptz := statement_timestamp();
BEGIN
    IF key IS NULL OR key='' OR char_length(key)>200
       OR requested_intent_fingerprint IS NULL OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$'
       OR label IS NULL OR label='' OR char_length(label)>100 THEN
        RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Tag create command rejected';
    END IF;
    PERFORM 1 FROM dante.person WHERE person_ref=requested_self_person_ref FOR UPDATE;
    IF NOT FOUND OR NOT EXISTS (SELECT 1 FROM dante.account_application_context WHERE self_person_ref=requested_self_person_ref) THEN
        RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Tag self context unavailable';
    END IF;
    SELECT r.intent_fingerprint,r.tag_ref,r.kind,r.expected_revision INTO prior
      FROM dante.product_tag_operation AS r
     WHERE r.self_person_ref=requested_self_person_ref AND r.operation_id=key;
    IF FOUND THEN
        IF prior.intent_fingerprint<>requested_intent_fingerprint OR prior.kind<>'create' OR prior.expected_revision<>0 THEN
            RAISE EXCEPTION USING ERRCODE='23505',CONSTRAINT='pk_product_tag_operation',MESSAGE='Tag operation id reused';
        END IF;
        RETURN QUERY SELECT prior.tag_ref,1::bigint,true;
        RETURN;
    END IF;
    IF uuid_extract_version(requested_tag_ref) IS DISTINCT FROM 7 THEN
        RAISE EXCEPTION USING ERRCODE='23514',CONSTRAINT='ck_product_tag_uuidv7',MESSAGE='Tag reference rejected';
    END IF;
    INSERT INTO dante.product_tag(tag_ref,self_person_ref,name,revision,archived,created_at,updated_at)
    VALUES(requested_tag_ref,requested_self_person_ref,label,1,false,recorded_at,recorded_at);
    INSERT INTO dante.product_tag_operation(self_person_ref,operation_id,intent_fingerprint,tag_ref,kind,expected_revision,accepted_revision,accepted_at)
    VALUES(requested_self_person_ref,key,requested_intent_fingerprint,requested_tag_ref,'create',0,1,recorded_at);
    RETURN QUERY SELECT requested_tag_ref,1::bigint,false;
END;
$function$;
"""


_MUTATE = r"""
CREATE FUNCTION dante.mutate_self_product_tag(
    requested_self_person_ref uuid, requested_operation_id text,
    requested_intent_fingerprint text, requested_tag_ref uuid,
    requested_expected_revision bigint, requested_kind text, requested_name text
)
RETURNS TABLE(tag_ref uuid, accepted_revision bigint, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path = pg_catalog, dante, pg_temp
AS $function$
#variable_conflict error
DECLARE
    key text := btrim(requested_operation_id);
    label text := btrim(requested_name);
    prior record;
    current_tag record;
    recorded_at timestamptz := statement_timestamp();
BEGIN
    IF key IS NULL OR key='' OR char_length(key)>200
       OR requested_intent_fingerprint IS NULL OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$'
       OR requested_expected_revision IS NULL OR requested_expected_revision<1
       OR requested_kind IS NULL OR requested_kind NOT IN ('rename','archive')
       OR (requested_kind='rename' AND (label IS NULL OR label='' OR char_length(label)>100))
       OR (requested_kind='archive' AND requested_name IS NOT NULL) THEN
        RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Tag mutation command rejected';
    END IF;
    PERFORM 1 FROM dante.person WHERE person_ref=requested_self_person_ref FOR UPDATE;
    IF NOT FOUND OR NOT EXISTS (SELECT 1 FROM dante.account_application_context WHERE self_person_ref=requested_self_person_ref) THEN
        RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Tag self context unavailable';
    END IF;
    SELECT r.intent_fingerprint,r.tag_ref,r.kind,r.expected_revision,r.accepted_revision INTO prior
      FROM dante.product_tag_operation AS r
     WHERE r.self_person_ref=requested_self_person_ref AND r.operation_id=key;
    IF FOUND THEN
        IF prior.intent_fingerprint<>requested_intent_fingerprint OR prior.tag_ref<>requested_tag_ref
           OR prior.kind<>requested_kind OR prior.expected_revision<>requested_expected_revision THEN
            RAISE EXCEPTION USING ERRCODE='23505',CONSTRAINT='pk_product_tag_operation',MESSAGE='Tag operation id reused';
        END IF;
        RETURN QUERY SELECT prior.tag_ref,prior.accepted_revision,true;
        RETURN;
    END IF;
    SELECT t.revision,t.name,t.archived INTO current_tag
      FROM dante.product_tag AS t
     WHERE t.tag_ref=requested_tag_ref AND t.self_person_ref=requested_self_person_ref FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',CONSTRAINT='product_tag_unavailable',MESSAGE='Tag unavailable';
    END IF;
    IF current_tag.revision<>requested_expected_revision OR current_tag.archived
       OR (requested_kind='rename' AND current_tag.name=label) THEN
        RAISE EXCEPTION USING ERRCODE='23514',CONSTRAINT='product_tag_revision_conflict',MESSAGE='Tag state changed';
    END IF;
    UPDATE dante.product_tag AS t
       SET name=CASE WHEN requested_kind='rename' THEN label ELSE t.name END,
           archived=(requested_kind='archive'),revision=t.revision+1,updated_at=recorded_at
     WHERE t.tag_ref=requested_tag_ref;
    INSERT INTO dante.product_tag_operation(self_person_ref,operation_id,intent_fingerprint,tag_ref,kind,expected_revision,accepted_revision,accepted_at)
    VALUES(requested_self_person_ref,key,requested_intent_fingerprint,requested_tag_ref,requested_kind,requested_expected_revision,requested_expected_revision+1,recorded_at);
    RETURN QUERY SELECT requested_tag_ref,requested_expected_revision+1,false;
END;
$function$;
"""


def _set_tag(kind: str) -> str:
    descriptor = "activity_intention" if kind == "activity" else "event_expectation"
    return f"""
CREATE FUNCTION dante.set_self_{kind}_tag(
    requested_self_person_ref uuid, requested_operation_id text,
    requested_intent_fingerprint text, requested_{kind}_ref uuid,
    requested_tag_ref uuid, requested_attached boolean
)
RETURNS TABLE(attached boolean, accepted_at timestamptz, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path = pg_catalog, dante, pg_temp
AS $function$
#variable_conflict error
DECLARE
    key text := btrim(requested_operation_id);
    prior record;
    exists_now boolean;
    recorded_at timestamptz := statement_timestamp();
BEGIN
    IF key IS NULL OR key='' OR char_length(key)>200
       OR requested_intent_fingerprint IS NULL OR requested_intent_fingerprint !~ '^[0-9a-f]{{64}}$'
       OR requested_attached IS NULL THEN
        RAISE EXCEPTION USING ERRCODE='23514',MESSAGE='Tag association command rejected';
    END IF;
    PERFORM 1 FROM dante.person WHERE person_ref=requested_self_person_ref FOR UPDATE;
    IF NOT FOUND OR NOT EXISTS (SELECT 1 FROM dante.account_application_context WHERE self_person_ref=requested_self_person_ref) THEN
        RAISE EXCEPTION USING ERRCODE='23503',MESSAGE='Tag self context unavailable';
    END IF;
    SELECT r.intent_fingerprint,r.{kind}_ref,r.tag_ref,r.attached,r.accepted_at INTO prior
      FROM dante.{kind}_tag_operation AS r
     WHERE r.self_person_ref=requested_self_person_ref AND r.operation_id=key;
    IF FOUND THEN
        IF prior.intent_fingerprint<>requested_intent_fingerprint OR prior.{kind}_ref<>requested_{kind}_ref
           OR prior.tag_ref<>requested_tag_ref OR prior.attached<>requested_attached THEN
            RAISE EXCEPTION USING ERRCODE='23505',CONSTRAINT='pk_{kind}_tag_operation',MESSAGE='Tag operation id reused';
        END IF;
        RETURN QUERY SELECT prior.attached,prior.accepted_at,true;
        RETURN;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM dante.{descriptor} AS item
                   WHERE item.{kind}_ref=requested_{kind}_ref AND item.self_person_ref=requested_self_person_ref) THEN
        RAISE EXCEPTION USING ERRCODE='23503',CONSTRAINT='{kind}_tag_item_unavailable',MESSAGE='Planning item unavailable';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM dante.product_tag AS t
                    WHERE t.tag_ref=requested_tag_ref AND t.self_person_ref=requested_self_person_ref
                      AND (requested_attached=false OR t.archived=false)) THEN
        RAISE EXCEPTION USING ERRCODE='23503',CONSTRAINT='product_tag_unavailable',MESSAGE='Tag unavailable or archived';
    END IF;
    SELECT EXISTS (SELECT 1 FROM dante.{kind}_tag AS edge
                    WHERE edge.self_person_ref=requested_self_person_ref AND edge.{kind}_ref=requested_{kind}_ref
                      AND edge.tag_ref=requested_tag_ref) INTO exists_now;
    IF exists_now=requested_attached THEN
        RAISE EXCEPTION USING ERRCODE='23514',CONSTRAINT='{kind}_tag_no_change',MESSAGE='Tag association did not change';
    END IF;
    IF requested_attached THEN
        INSERT INTO dante.{kind}_tag(self_person_ref,{kind}_ref,tag_ref,attached_at)
        VALUES(requested_self_person_ref,requested_{kind}_ref,requested_tag_ref,recorded_at);
    ELSE
        DELETE FROM dante.{kind}_tag AS edge
         WHERE edge.self_person_ref=requested_self_person_ref AND edge.{kind}_ref=requested_{kind}_ref
           AND edge.tag_ref=requested_tag_ref;
    END IF;
    INSERT INTO dante.{kind}_tag_operation(self_person_ref,operation_id,intent_fingerprint,{kind}_ref,tag_ref,attached,accepted_at)
    VALUES(requested_self_person_ref,key,requested_intent_fingerprint,requested_{kind}_ref,requested_tag_ref,requested_attached,recorded_at);
    RETURN QUERY SELECT requested_attached,recorded_at,false;
END;
$function$;
"""


def upgrade() -> None:
    """Create non-owning product labels and independent many-valued typed edges."""
    _tables()
    _sql(_CREATE)
    _sql(_MUTATE)
    for kind in ("activity", "event"):
        _sql(_set_tag(kind))
    _sql(r"""
        CREATE FUNCTION dante.list_self_product_tags(requested_self_person_ref uuid)
        RETURNS TABLE(tag_ref uuid, name text, revision bigint, archived boolean,
                      created_at timestamptz, updated_at timestamptz)
        LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
            SELECT t.tag_ref,t.name,t.revision,t.archived,t.created_at,t.updated_at
              FROM dante.product_tag AS t
             WHERE t.self_person_ref=requested_self_person_ref
               AND EXISTS (SELECT 1 FROM dante.account_application_context
                            WHERE self_person_ref=requested_self_person_ref)
             ORDER BY t.created_at,t.tag_ref;
        $function$;
    """)
    _sql(r"""
        CREATE FUNCTION dante.list_self_item_tags(requested_self_person_ref uuid)
        RETURNS TABLE(subject_kind text, subject_native_ref uuid, tag_ref uuid, attached_at timestamptz)
        LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
            SELECT 'activity'::text,edge.activity_ref,edge.tag_ref,edge.attached_at
              FROM dante.activity_tag AS edge
             WHERE edge.self_person_ref=requested_self_person_ref
               AND EXISTS (SELECT 1 FROM dante.account_application_context WHERE self_person_ref=requested_self_person_ref)
            UNION ALL
            SELECT 'event'::text,edge.event_ref,edge.tag_ref,edge.attached_at
              FROM dante.event_tag AS edge
             WHERE edge.self_person_ref=requested_self_person_ref
               AND EXISTS (SELECT 1 FROM dante.account_application_context WHERE self_person_ref=requested_self_person_ref)
             ORDER BY 1,2,3;
        $function$;
    """)
    for signature in (
        "dante.create_self_product_tag(uuid,text,text,uuid,text)",
        "dante.mutate_self_product_tag(uuid,text,text,uuid,bigint,text,text)",
        "dante.list_self_product_tags(uuid)",
        "dante.set_self_activity_tag(uuid,text,text,uuid,uuid,boolean)",
        "dante.set_self_event_tag(uuid,text,text,uuid,uuid,boolean)",
        "dante.list_self_item_tags(uuid)",
    ):
        _sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
        _sql(
            f"REVOKE ALL PRIVILEGES ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator"
        )
        _sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")
    for name in (
        "product_tag",
        "product_tag_operation",
        "activity_tag",
        "event_tag",
        "activity_tag_operation",
        "event_tag_operation",
    ):
        _sql(
            f"REVOKE ALL PRIVILEGES ON TABLE dante.{name} FROM PUBLIC,dante_runtime,dante_migrator"
        )


def downgrade() -> None:
    """Never erase accepted Tag commands and associations by downgrading."""
    raise RuntimeError("B05-C Tags require a reviewed forward migration")
