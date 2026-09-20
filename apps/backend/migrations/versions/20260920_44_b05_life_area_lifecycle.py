"""Complete B05-A Life Area profile lifecycle and actor-local ordering.

Revision ID: 20260920_44
Revises: 20260920_43
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260920_44"
down_revision: str | None = "20260920_43"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"
_CREATE = "dante.create_self_life_area(uuid,text,text,uuid,text)"
_LIST = "dante.list_self_life_areas(uuid)"
_MUTATE = "dante.mutate_self_life_area(uuid,text,text,uuid,bigint,text,text,boolean,text,text)"
_REORDER = "dante.reorder_self_life_areas(uuid,text,text,uuid[],bigint[])"


def _execute(sql: str) -> None:
    op.execute(sa.text(sql))


def upgrade() -> None:
    """Extend the profile, retain older rows and expose bounded lifecycle commands."""
    op.add_column(
        "life_area",
        sa.Column("revision", sa.BigInteger(), nullable=False, server_default="1"),
        schema="dante",
    )
    op.add_column(
        "life_area", sa.Column("sort_order", sa.BigInteger(), nullable=True), schema="dante"
    )
    op.add_column(
        "life_area",
        sa.Column("archived", sa.Boolean(), nullable=False, server_default=sa.false()),
        schema="dante",
    )
    op.add_column(
        "life_area",
        sa.Column("hidden", sa.Boolean(), nullable=False, server_default=sa.false()),
        schema="dante",
    )
    op.add_column("life_area", sa.Column("icon_code", sa.Text(), nullable=True), schema="dante")
    op.add_column("life_area", sa.Column("color_code", sa.Text(), nullable=True), schema="dante")
    op.add_column(
        "life_area",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("statement_timestamp()"),
        ),
        schema="dante",
    )
    _execute("""
        WITH ranked AS (
            SELECT life_area_ref,
                   row_number() OVER (PARTITION BY self_person_ref ORDER BY created_at,life_area_ref)-1 AS rank
              FROM dante.life_area
        )
        UPDATE dante.life_area AS area SET sort_order=ranked.rank
          FROM ranked WHERE ranked.life_area_ref=area.life_area_ref
    """)
    op.alter_column("life_area", "sort_order", nullable=False, schema="dante")
    op.create_check_constraint(
        op.f("ck_life_area_revision"), "life_area", "revision>=1", schema="dante"
    )
    op.create_check_constraint(
        op.f("ck_life_area_sort_order"), "life_area", "sort_order>=0", schema="dante"
    )
    op.create_check_constraint(
        op.f("ck_life_area_icon_code"),
        "life_area",
        "icon_code IS NULL OR (char_length(icon_code)<=40 AND icon_code ~ '^[a-z][a-z0-9_-]*$')",
        schema="dante",
    )
    op.create_check_constraint(
        op.f("ck_life_area_color_code"),
        "life_area",
        "color_code IS NULL OR color_code ~ '^#[0-9A-F]{6}$'",
        schema="dante",
    )
    op.create_unique_constraint(
        "uq_life_area_self_person_sort_order",
        "life_area",
        ["self_person_ref", "sort_order"],
        schema="dante",
        deferrable=True,
        initially="DEFERRED",
    )
    op.create_table(
        "life_area_mutation_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("mutation_kind", sa.Text(), nullable=False),
        sa.Column("life_area_ref", sa.Uuid(), nullable=True),
        sa.Column("accepted_revision", sa.BigInteger(), nullable=True),
        sa.Column("affected_count", sa.Integer(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref", "operation_id", name="pk_life_area_mutation_operation"
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_life_area_mutation_operation_self_person_ref_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["life_area_ref"],
            ["dante.life_area.life_area_ref"],
            name="fk_life_area_mutation_operation_life_area_ref_life_area",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name=op.f("ck_life_area_mutation_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_life_area_mutation_operation_fingerprint"),
        ),
        sa.CheckConstraint(
            "mutation_kind IN ('rename','visibility','archive','appearance','reorder')",
            name=op.f("ck_life_area_mutation_operation_kind"),
        ),
        sa.CheckConstraint(
            "(mutation_kind='reorder' AND life_area_ref IS NULL AND accepted_revision IS NULL) "
            "OR (mutation_kind<>'reorder' AND life_area_ref IS NOT NULL AND accepted_revision>=2)",
            name=op.f("ck_life_area_mutation_operation_shape"),
        ),
        sa.CheckConstraint("affected_count>=0", name="ck_life_area_mutation_operation_count"),
        schema="dante",
    )

    # The output shape changes, so this routine must be replaced by a forward migration.
    _execute(f"DROP FUNCTION {_LIST}")
    _execute(r"""
        CREATE FUNCTION dante.list_self_life_areas(requested_self_person_ref uuid)
        RETURNS TABLE(life_area_ref uuid, name text, created_at timestamptz,
                      revision bigint, sort_order bigint, archived boolean, hidden boolean,
                      icon_code text, color_code text, updated_at timestamptz)
        LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
            SELECT area.life_area_ref, area.name, area.created_at,
                   area.revision, area.sort_order, area.archived, area.hidden,
                   area.icon_code, area.color_code, area.updated_at
              FROM dante.life_area AS area
             WHERE area.self_person_ref=requested_self_person_ref
               AND EXISTS (
                   SELECT 1 FROM dante.account_application_context
                   WHERE self_person_ref=requested_self_person_ref
               )
             ORDER BY area.sort_order, area.life_area_ref;
        $function$
    """)
    _execute(r"""
        CREATE OR REPLACE FUNCTION dante.create_self_life_area(
            requested_self_person_ref uuid, requested_operation_id text,
            requested_intent_fingerprint text, requested_life_area_ref uuid,
            requested_name text
        )
        RETURNS TABLE(life_area_ref uuid, name text, created_at timestamptz, replayed boolean)
        LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            normalized_operation_id text := btrim(requested_operation_id);
            normalized_name text := btrim(requested_name);
            existing_fingerprint text;
            existing_ref uuid;
            next_order bigint;
            recorded_at timestamptz := statement_timestamp();
        BEGIN
            IF normalized_operation_id IS NULL OR normalized_operation_id=''
               OR char_length(normalized_operation_id)>200 THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_life_area_create_operation_operation_id',
                    MESSAGE='Life Area operation id rejected';
            END IF;
            IF requested_intent_fingerprint IS NULL
               OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_life_area_create_operation_fingerprint',
                    MESSAGE='Life Area fingerprint rejected';
            END IF;
            IF normalized_name IS NULL OR normalized_name=''
               OR char_length(normalized_name)>100 THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_life_area_name',
                    MESSAGE='Life Area name rejected';
            END IF;
            IF uuid_extract_version(requested_life_area_ref) IS DISTINCT FROM 7 THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_life_area_uuidv7',
                    MESSAGE='Life Area reference rejected';
            END IF;
            IF NOT EXISTS (
                SELECT 1 FROM dante.account_application_context
                 WHERE self_person_ref=requested_self_person_ref
            ) THEN
                RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Life Area self context rejected';
            END IF;
            PERFORM 1 FROM dante.person WHERE person_ref=requested_self_person_ref FOR UPDATE;
            IF NOT FOUND THEN
                RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Life Area self context rejected';
            END IF;
            SELECT operation.intent_fingerprint, operation.life_area_ref
              INTO existing_fingerprint, existing_ref
              FROM dante.life_area_create_operation AS operation
             WHERE operation.self_person_ref=requested_self_person_ref
               AND operation.operation_id=normalized_operation_id;
            IF FOUND THEN
                IF existing_fingerprint<>requested_intent_fingerprint THEN
                    RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_life_area_create_operation',
                        MESSAGE='Life Area operation id reused with different intent';
                END IF;
                RETURN QUERY
                SELECT area.life_area_ref, area.name, area.created_at, true
                  FROM dante.life_area AS area
                 WHERE area.life_area_ref=existing_ref
                   AND area.self_person_ref=requested_self_person_ref;
                IF NOT FOUND THEN
                    RAISE EXCEPTION USING ERRCODE='XX001', MESSAGE='Life Area receipt lost its profile';
                END IF;
                RETURN;
            END IF;
            SELECT COALESCE(MAX(area.sort_order)+1,0) INTO next_order
              FROM dante.life_area AS area WHERE area.self_person_ref=requested_self_person_ref;
            INSERT INTO dante.life_area(
                life_area_ref,self_person_ref,name,created_at,updated_at,
                revision,sort_order,archived,hidden
            ) VALUES (
                requested_life_area_ref,requested_self_person_ref,normalized_name,recorded_at,
                recorded_at,1,next_order,false,false
            );
            INSERT INTO dante.life_area_create_operation(
                self_person_ref,operation_id,intent_fingerprint,life_area_ref,created_at
            ) VALUES (
                requested_self_person_ref,normalized_operation_id,requested_intent_fingerprint,
                requested_life_area_ref,recorded_at
            );
            RETURN QUERY SELECT requested_life_area_ref,normalized_name,recorded_at,false;
        END;
        $function$
    """)
    _execute(r"""
        CREATE FUNCTION dante.mutate_self_life_area(
            requested_self_person_ref uuid, requested_operation_id text,
            requested_intent_fingerprint text, requested_life_area_ref uuid,
            requested_expected_revision bigint, requested_kind text,
            requested_name text, requested_hidden boolean,
            requested_icon_code text, requested_color_code text
        )
        RETURNS TABLE(accepted_revision bigint, replayed boolean)
        LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            normalized_operation_id text := btrim(requested_operation_id);
            normalized_name text := btrim(requested_name);
            normalized_icon text := btrim(requested_icon_code);
            normalized_color text := upper(btrim(requested_color_code));
            previous_fingerprint text;
            previous_kind text;
            previous_ref uuid;
            previous_revision bigint;
            current_area dante.life_area%ROWTYPE;
            recorded_at timestamptz := statement_timestamp();
        BEGIN
            IF normalized_operation_id IS NULL OR normalized_operation_id=''
               OR char_length(normalized_operation_id)>200
               OR requested_intent_fingerprint IS NULL
               OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Life Area mutation operation rejected';
            END IF;
            IF requested_kind NOT IN ('rename','visibility','archive','appearance')
               OR requested_kind IS NULL OR requested_expected_revision IS NULL
               OR requested_expected_revision<1 THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Life Area mutation kind or revision rejected';
            END IF;
            IF (requested_kind='rename' AND
                (normalized_name IS NULL OR normalized_name=''
                 OR char_length(normalized_name)>100 OR requested_hidden IS NOT NULL
                 OR requested_icon_code IS NOT NULL OR requested_color_code IS NOT NULL))
               OR (requested_kind='visibility' AND
                (requested_hidden IS NULL OR requested_name IS NOT NULL
                 OR requested_icon_code IS NOT NULL OR requested_color_code IS NOT NULL))
               OR (requested_kind='archive' AND
                (requested_hidden IS NOT NULL OR requested_name IS NOT NULL
                 OR requested_icon_code IS NOT NULL OR requested_color_code IS NOT NULL))
               OR (requested_kind='appearance' AND
                (requested_name IS NOT NULL OR requested_hidden IS NOT NULL
                 OR (normalized_icon IS NOT NULL AND
                     (char_length(normalized_icon)>40 OR normalized_icon !~ '^[a-z][a-z0-9_-]*$'))
                 OR (normalized_color IS NOT NULL AND normalized_color !~ '^#[0-9A-F]{6}$'))) THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Life Area mutation payload rejected';
            END IF;
            IF NOT EXISTS (
                SELECT 1 FROM dante.account_application_context
                 WHERE self_person_ref=requested_self_person_ref
            ) THEN
                RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Life Area self context rejected';
            END IF;
            PERFORM 1 FROM dante.person WHERE person_ref=requested_self_person_ref FOR UPDATE;
            IF NOT FOUND THEN
                RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Life Area self context rejected';
            END IF;
            SELECT operation.intent_fingerprint,operation.mutation_kind,
                   operation.life_area_ref,operation.accepted_revision
              INTO previous_fingerprint,previous_kind,previous_ref,previous_revision
              FROM dante.life_area_mutation_operation AS operation
             WHERE operation.self_person_ref=requested_self_person_ref
               AND operation.operation_id=normalized_operation_id;
            IF FOUND THEN
                IF previous_fingerprint<>requested_intent_fingerprint
                   OR previous_kind<>requested_kind OR previous_ref<>requested_life_area_ref THEN
                    RAISE EXCEPTION USING ERRCODE='23505',
                        CONSTRAINT='pk_life_area_mutation_operation',
                        MESSAGE='Life Area operation id reused with different intent';
                END IF;
                RETURN QUERY SELECT previous_revision,true;
                RETURN;
            END IF;
            SELECT * INTO current_area FROM dante.life_area AS area
             WHERE area.life_area_ref=requested_life_area_ref
               AND area.self_person_ref=requested_self_person_ref FOR UPDATE;
            IF NOT FOUND THEN
                RAISE EXCEPTION USING ERRCODE='23503',
                    CONSTRAINT='fk_life_area_mutation_operation_life_area_ref_life_area',
                    MESSAGE='Life Area unavailable in current self scope';
            END IF;
            IF current_area.revision<>requested_expected_revision THEN
                RAISE EXCEPTION USING ERRCODE='23514',
                    CONSTRAINT='life_area_expected_revision', MESSAGE='Life Area state changed';
            END IF;
            IF (requested_kind='rename' AND current_area.name=normalized_name)
               OR (requested_kind='visibility' AND current_area.hidden=requested_hidden)
               OR (requested_kind='archive' AND current_area.archived)
               OR (requested_kind='appearance'
                   AND current_area.icon_code IS NOT DISTINCT FROM normalized_icon
                   AND current_area.color_code IS NOT DISTINCT FROM normalized_color) THEN
                RAISE EXCEPTION USING ERRCODE='23514',
                    CONSTRAINT='life_area_no_change', MESSAGE='Life Area mutation has no new effect';
            END IF;
            UPDATE dante.life_area AS area
               SET name=CASE WHEN requested_kind='rename' THEN normalized_name ELSE area.name END,
                   hidden=CASE WHEN requested_kind='visibility' THEN requested_hidden ELSE area.hidden END,
                   archived=CASE WHEN requested_kind='archive' THEN true ELSE area.archived END,
                   icon_code=CASE WHEN requested_kind='appearance' THEN normalized_icon ELSE area.icon_code END,
                   color_code=CASE WHEN requested_kind='appearance' THEN normalized_color ELSE area.color_code END,
                   revision=area.revision+1,
                   updated_at=recorded_at
             WHERE area.life_area_ref=requested_life_area_ref;
            INSERT INTO dante.life_area_mutation_operation(
                self_person_ref,operation_id,intent_fingerprint,mutation_kind,
                life_area_ref,accepted_revision,affected_count,accepted_at
            ) VALUES (
                requested_self_person_ref,normalized_operation_id,requested_intent_fingerprint,
                requested_kind,requested_life_area_ref,current_area.revision+1,1,recorded_at
            );
            RETURN QUERY SELECT current_area.revision+1,false;
        END;
        $function$
    """)
    _execute(r"""
        CREATE FUNCTION dante.reorder_self_life_areas(
            requested_self_person_ref uuid, requested_operation_id text,
            requested_intent_fingerprint text, requested_area_refs uuid[],
            requested_expected_revisions bigint[]
        )
        RETURNS TABLE(affected_count integer, replayed boolean)
        LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            normalized_operation_id text := btrim(requested_operation_id);
            previous_fingerprint text;
            previous_kind text;
            previous_count integer;
            total_count bigint;
            matching_count bigint;
            requested_count integer;
            changed_count integer;
        BEGIN
            IF normalized_operation_id IS NULL OR normalized_operation_id=''
               OR char_length(normalized_operation_id)>200
               OR requested_intent_fingerprint IS NULL
               OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$'
               OR requested_area_refs IS NULL OR requested_expected_revisions IS NULL
               OR cardinality(requested_area_refs)<>cardinality(requested_expected_revisions)
               OR array_position(requested_area_refs,NULL) IS NOT NULL
               OR array_position(requested_expected_revisions,NULL) IS NOT NULL THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Life Area reorder payload rejected';
            END IF;
            IF NOT EXISTS (
                SELECT 1 FROM dante.account_application_context
                 WHERE self_person_ref=requested_self_person_ref
            ) THEN
                RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Life Area self context rejected';
            END IF;
            PERFORM 1 FROM dante.person WHERE person_ref=requested_self_person_ref FOR UPDATE;
            IF NOT FOUND THEN
                RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Life Area self context rejected';
            END IF;
            SELECT operation.intent_fingerprint,operation.mutation_kind,operation.affected_count
              INTO previous_fingerprint,previous_kind,previous_count
              FROM dante.life_area_mutation_operation AS operation
             WHERE operation.self_person_ref=requested_self_person_ref
               AND operation.operation_id=normalized_operation_id;
            IF FOUND THEN
                IF previous_fingerprint<>requested_intent_fingerprint OR previous_kind<>'reorder' THEN
                    RAISE EXCEPTION USING ERRCODE='23505',
                        CONSTRAINT='pk_life_area_mutation_operation',
                        MESSAGE='Life Area operation id reused with different intent';
                END IF;
                RETURN QUERY SELECT previous_count,true;
                RETURN;
            END IF;
            requested_count:=cardinality(requested_area_refs);
            SELECT count(*) INTO total_count FROM dante.life_area AS area
             WHERE area.self_person_ref=requested_self_person_ref;
            SELECT count(*) INTO matching_count
              FROM unnest(requested_area_refs,requested_expected_revisions)
                   AS requested(life_area_ref,expected_revision)
              JOIN dante.life_area AS area
                ON area.life_area_ref=requested.life_area_ref
               AND area.self_person_ref=requested_self_person_ref
               AND area.revision=requested.expected_revision;
            IF total_count<>requested_count OR matching_count<>requested_count
               OR (SELECT count(DISTINCT refs.ref) FROM unnest(requested_area_refs) AS refs(ref))<>requested_count THEN
                RAISE EXCEPTION USING ERRCODE='23514',
                    CONSTRAINT='life_area_order_conflict',
                    MESSAGE='Life Area order was based on stale or incomplete catalog truth';
            END IF;
            UPDATE dante.life_area AS area
               SET sort_order=requested.ordinal-1,
                   revision=area.revision+1,
                   updated_at=statement_timestamp()
              FROM unnest(requested_area_refs) WITH ORDINALITY AS requested(life_area_ref,ordinal)
             WHERE area.life_area_ref=requested.life_area_ref
               AND area.self_person_ref=requested_self_person_ref
               AND area.sort_order IS DISTINCT FROM requested.ordinal-1;
            GET DIAGNOSTICS changed_count=ROW_COUNT;
            INSERT INTO dante.life_area_mutation_operation(
                self_person_ref,operation_id,intent_fingerprint,mutation_kind,
                life_area_ref,accepted_revision,affected_count,accepted_at
            ) VALUES (
                requested_self_person_ref,normalized_operation_id,requested_intent_fingerprint,
                'reorder',NULL,NULL,changed_count,statement_timestamp()
            );
            RETURN QUERY SELECT changed_count,false;
        END;
        $function$
    """)
    for signature in (_CREATE, _LIST, _MUTATE, _REORDER):
        _execute(f"ALTER FUNCTION {signature} OWNER TO {_OWNER}")
        _execute(
            f"REVOKE ALL PRIVILEGES ON FUNCTION {signature} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
        _execute(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}")
    _execute(
        f"REVOKE ALL PRIVILEGES ON TABLE dante.life_area_mutation_operation FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
    )


def downgrade() -> None:
    """Never discard accepted profile mutations or resurrect an older create path."""
    raise RuntimeError("B05-A lifecycle downgrade requires a separate reviewed forward migration")
