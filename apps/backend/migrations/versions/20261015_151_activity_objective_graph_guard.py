"""Close the polymorphic Objective gap in Activity lifecycle deletion.

Revision ID: 20261015_151
Revises: 20261015_150

A normal FK graph cannot find dante.temporal_objective by subject_native_ref:
that column is a polymorphic identity rather than a native_address FK.
Seed the owner-scoped Objective roots before the existing bounded FK closure.
No runtime table DELETE privileges are added. This is a candidate and still
requires complete real-PostgreSQL graph proof before extending recurring delete.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261015_151"
down_revision: str | None = "20261015_150"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_GRAPH_DELETE = r"""
CREATE OR REPLACE FUNCTION dante.delete_self_activity_lifecycle_graph(
    requested_actor uuid,
    requested_activity uuid,
    requested_scope text,
    requested_named_schedule uuid DEFAULT NULL
) RETURNS integer
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $lifecycle$
#variable_conflict error
DECLARE
    owned record;
    dependency record;
    source_table record;
    address_table record;
    selected_table oid;
    primary_column text;
    matching_condition text;
    added integer;
    total_added integer;
    deleted_count integer := 0;
    cycle_tables text;
BEGIN
    IF requested_scope NOT IN ('sessions','named','activity')
       OR requested_scope IS NULL
       OR (requested_scope='named' AND requested_named_schedule IS NULL)
       OR (requested_scope<>'named' AND requested_named_schedule IS NOT NULL) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
            CONSTRAINT='activity_lifecycle_invalid_scope',
            MESSAGE='Invalid Activity lifecycle deletion scope';
    END IF;

    SELECT * INTO owned FROM dante.activity_intention AS activity
     WHERE activity.activity_ref=requested_activity
       AND activity.self_person_ref=requested_actor
       AND activity.retired_at IS NULL
     FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='activity_lifecycle_unavailable',
            MESSAGE='Activity unavailable for lifecycle operation';
    END IF;

    -- The native-address FK locks prevent a new Activity Session being linked
    -- to this owner while its existing attempts are being selected for deletion.
    PERFORM 1 FROM dante.native_address AS address
     WHERE address.native_ref=requested_activity FOR UPDATE;
    IF requested_scope='named' THEN
        PERFORM 1 FROM dante.activity_schedule_role AS role
         WHERE role.schedule_ref=requested_named_schedule
           AND role.activity_ref=requested_activity
           AND role.role_code='planned'
           AND role.retired_at IS NULL FOR UPDATE;
        IF NOT FOUND THEN
            RAISE EXCEPTION USING ERRCODE='23503',
                CONSTRAINT='activity_lifecycle_named_unavailable',
                MESSAGE='Named Session does not belong to this Activity';
        END IF;
    END IF;

    -- The temporary tables are recreated for each bounded call, including
    -- multiple named removals within one transaction. They are never supplied
    -- by the caller and cannot name arbitrary database rows.
    DROP TABLE IF EXISTS pg_temp.dante_lifecycle_targets;
    DROP TABLE IF EXISTS pg_temp.dante_lifecycle_tables;
    CREATE TEMP TABLE dante_lifecycle_targets (
        relation_oid oid NOT NULL,
        tuple_id tid NOT NULL,
        PRIMARY KEY(relation_oid,tuple_id)
    ) ON COMMIT DROP;

    IF requested_scope='activity' THEN
        INSERT INTO pg_temp.dante_lifecycle_targets
        SELECT 'dante.native_address'::regclass, address.ctid
          FROM dante.native_address AS address
         WHERE address.native_ref=requested_activity
        ON CONFLICT DO NOTHING;
        INSERT INTO pg_temp.dante_lifecycle_targets
        SELECT 'dante.activity'::regclass, activity.ctid
          FROM dante.activity AS activity
         WHERE activity.activity_ref=requested_activity
        ON CONFLICT DO NOTHING;
    END IF;

    -- Session is a NativeRef root, not a child FK of Activity. Seed it
    -- explicitly through the authenticated Activity execution-subject edge.
    -- A named configuration removes only its own linked attempts.
    PERFORM 1 FROM dante.session AS real
      JOIN dante.session_execution_subject AS subject
        ON subject.session_ref=real.session_ref
     WHERE subject.subject_native_ref=requested_activity
       AND (requested_scope<>'named'
            OR EXISTS (
                SELECT 1 FROM dante.session_planned_schedule_link AS linked
                 WHERE linked.session_ref=real.session_ref
                   AND linked.schedule_ref=requested_named_schedule
            ))
     FOR UPDATE OF real;

    INSERT INTO pg_temp.dante_lifecycle_targets
    SELECT 'dante.session'::regclass, real.ctid
      FROM dante.session AS real
      JOIN dante.session_execution_subject AS subject
        ON subject.session_ref=real.session_ref
     WHERE subject.subject_native_ref=requested_activity
       AND (requested_scope<>'named'
            OR EXISTS (
                SELECT 1 FROM dante.session_planned_schedule_link AS linked
                 WHERE linked.session_ref=real.session_ref
                   AND linked.schedule_ref=requested_named_schedule
            ))
    ON CONFLICT DO NOTHING;

    INSERT INTO pg_temp.dante_lifecycle_targets
    SELECT 'dante.native_address'::regclass, address.ctid
      FROM dante.native_address AS address
      JOIN dante.session_execution_subject AS subject
        ON subject.session_ref=address.native_ref
     WHERE subject.subject_native_ref=requested_activity
       AND (requested_scope<>'named'
            OR EXISTS (
                SELECT 1 FROM dante.session_planned_schedule_link AS linked
                 WHERE linked.session_ref=subject.session_ref
                   AND linked.schedule_ref=requested_named_schedule
            ))
    ON CONFLICT DO NOTHING;

    -- Accepted Actual evidence tied to the deleted attempts cannot remain
    -- with a dangling Session basis. Delete its owned Actual graph as a unit.
    -- An Actual on a different Activity is NOT silently removed: its retained
    -- FK will refuse the operation and the entire transaction rolls back.
    INSERT INTO pg_temp.dante_lifecycle_targets
    SELECT DISTINCT 'dante.actual'::regclass, actual.ctid
      FROM dante.actual AS actual
      JOIN dante.actual_realization_state AS state
        ON state.actual_ref=actual.actual_ref
      JOIN dante.actual_realization_session_basis AS basis
        ON basis.actual_material_state_ref=state.material_state_ref
      JOIN dante.session_execution_subject AS subject
        ON subject.session_ref=basis.session_ref
     WHERE actual.subject_native_ref=requested_activity
       AND subject.subject_native_ref=requested_activity
       AND (requested_scope<>'named'
            OR EXISTS (
                SELECT 1 FROM dante.session_planned_schedule_link AS linked
                 WHERE linked.session_ref=subject.session_ref
                   AND linked.schedule_ref=requested_named_schedule
            ))
    ON CONFLICT DO NOTHING;

    IF requested_scope='named' THEN
        INSERT INTO pg_temp.dante_lifecycle_targets
        SELECT 'dante.schedule'::regclass, schedule.ctid
          FROM dante.schedule AS schedule
         WHERE schedule.schedule_ref=requested_named_schedule
        ON CONFLICT DO NOTHING;
        INSERT INTO pg_temp.dante_lifecycle_targets
        SELECT 'dante.scoped_address'::regclass, address.ctid
          FROM dante.scoped_address AS address
         WHERE address.scoped_ref=requested_named_schedule
        ON CONFLICT DO NOTHING;
    END IF;

    -- Some Activity-owned domain records use polymorphic subject identities:
    -- their subject_native_ref is not an FK into native_address. Seed them
    -- explicitly, otherwise an FK-only descendant closure can leave Objectives
    -- of a hard-deleted Activity behind.
    IF requested_scope='activity' THEN
        INSERT INTO pg_temp.dante_lifecycle_targets(relation_oid,tuple_id)
        SELECT 'dante.temporal_objective'::regclass, objective.ctid
          FROM dante.temporal_objective AS objective
         WHERE objective.subject_kind='activity'
           AND objective.subject_native_ref=requested_activity
           AND objective.self_person_ref=requested_actor
        ON CONFLICT DO NOTHING;
    END IF;

    -- Traverse only real dante-schema foreign-key descendants of the selected
    -- roots. Never walk an outbound FK into a shared Person, Life Area or
    -- unrelated owner. Promote the single-column identity of each selected
    -- object to its native/scoped/material address when such an address exists.
    LOOP
        total_added := 0;
        FOR dependency IN
            SELECT fk.conrelid AS child_oid,
                   fk.confrelid AS parent_oid,
                   fk.conkey,
                   fk.confkey
              FROM pg_catalog.pg_constraint AS fk
              JOIN pg_catalog.pg_class AS child ON child.oid=fk.conrelid
              JOIN pg_catalog.pg_namespace AS ns ON ns.oid=child.relnamespace
             WHERE fk.contype='f'
               AND ns.nspname='dante'
               AND EXISTS (
                   SELECT 1 FROM pg_temp.dante_lifecycle_targets AS target
                    WHERE target.relation_oid=fk.confrelid
               )
        LOOP
            SELECT string_agg(
                format('child.%I = parent.%I', ca.attname, pa.attname),
                ' AND ' ORDER BY columns.ordinal
            ) INTO matching_condition
              FROM unnest(dependency.conkey,dependency.confkey)
                   WITH ORDINALITY AS columns(child_attnum,parent_attnum,ordinal)
              JOIN pg_catalog.pg_attribute AS ca
                ON ca.attrelid=dependency.child_oid
               AND ca.attnum=columns.child_attnum
              JOIN pg_catalog.pg_attribute AS pa
                ON pa.attrelid=dependency.parent_oid
               AND pa.attnum=columns.parent_attnum;
            IF matching_condition IS NULL THEN
                RAISE EXCEPTION 'Unresolvable lifecycle FK';
            END IF;
            EXECUTE format(
                'INSERT INTO pg_temp.dante_lifecycle_targets(relation_oid,tuple_id)
                 SELECT %s,child.ctid FROM %s AS child
                 JOIN %s AS parent ON %s
                 JOIN pg_temp.dante_lifecycle_targets AS selected
                   ON selected.relation_oid=%s AND selected.tuple_id=parent.ctid
                 ON CONFLICT DO NOTHING',
                dependency.child_oid, dependency.child_oid::regclass,
                dependency.parent_oid::regclass, matching_condition,
                dependency.parent_oid
            );
            GET DIAGNOSTICS added=ROW_COUNT;
            total_added := total_added + added;
        END LOOP;

        FOR source_table IN
            SELECT DISTINCT target.relation_oid
              FROM pg_temp.dante_lifecycle_targets AS target
        LOOP
            SELECT attribute.attname INTO primary_column
              FROM pg_catalog.pg_index AS pk
              JOIN pg_catalog.pg_attribute AS attribute
                ON attribute.attrelid=pk.indrelid
               AND attribute.attnum=pk.indkey[0]
             WHERE pk.indrelid=source_table.relation_oid
               AND pk.indisprimary AND pk.indnkeyatts=1
               AND attribute.atttypid='pg_catalog.uuid'::regtype;
            IF primary_column IS NULL THEN CONTINUE; END IF;
            FOR address_table IN
                SELECT address.relation_oid,address.ref_column FROM (
                    VALUES
                        ('dante.native_address'::regclass::oid,'native_ref'),
                        ('dante.scoped_address'::regclass::oid,'scoped_ref'),
                        ('dante.material_state_address'::regclass::oid,'material_state_ref')
                ) AS address(relation_oid,ref_column)
            LOOP
                IF address_table.relation_oid=source_table.relation_oid THEN
                    CONTINUE;
                END IF;
                EXECUTE format(
                    'INSERT INTO pg_temp.dante_lifecycle_targets(relation_oid,tuple_id)
                     SELECT %s,address.ctid FROM %s AS address
                     JOIN %s AS item ON item.%I=address.%I
                     JOIN pg_temp.dante_lifecycle_targets AS selected
                       ON selected.relation_oid=%s AND selected.tuple_id=item.ctid
                     ON CONFLICT DO NOTHING',
                    address_table.relation_oid, address_table.relation_oid::regclass,
                    source_table.relation_oid::regclass, primary_column,
                    address_table.ref_column, source_table.relation_oid
                );
                GET DIAGNOSTICS added=ROW_COUNT;
                total_added := total_added + added;
            END LOOP;
        END LOOP;
        EXIT WHEN total_added=0;
    END LOOP;

    CREATE TEMP TABLE dante_lifecycle_tables (
        relation_oid oid PRIMARY KEY
    ) ON COMMIT DROP;
    INSERT INTO pg_temp.dante_lifecycle_tables
    SELECT DISTINCT relation_oid FROM pg_temp.dante_lifecycle_targets;

    -- Physical table order is a reverse FK topological order. A participating
    -- cycle is unsupported: fail closed without disabling constraints/triggers.
    WHILE EXISTS(SELECT 1 FROM pg_temp.dante_lifecycle_tables) LOOP
        SELECT candidate.relation_oid INTO selected_table
          FROM pg_temp.dante_lifecycle_tables AS candidate
         WHERE NOT EXISTS (
             SELECT 1 FROM pg_catalog.pg_constraint AS fk
               JOIN pg_temp.dante_lifecycle_tables AS dependent
                 ON dependent.relation_oid=fk.conrelid
              WHERE fk.contype='f'
                AND fk.confrelid=candidate.relation_oid
                AND fk.conrelid<>candidate.relation_oid
         )
         ORDER BY candidate.relation_oid LIMIT 1;
        IF NOT FOUND THEN
            SELECT string_agg(relation_oid::regclass::text,', ')
              INTO cycle_tables FROM pg_temp.dante_lifecycle_tables;
            RAISE EXCEPTION USING ERRCODE='23514',
                CONSTRAINT='activity_lifecycle_unsupported_cycle',
                MESSAGE='Cannot safely delete cyclic lifecycle references: '||cycle_tables;
        END IF;
        EXECUTE format(
            'DELETE FROM %s AS item WHERE EXISTS (
               SELECT 1 FROM pg_temp.dante_lifecycle_targets AS selected
                WHERE selected.relation_oid=%s AND selected.tuple_id=item.ctid)',
            selected_table::regclass, selected_table
        );
        GET DIAGNOSTICS added=ROW_COUNT;
        deleted_count := deleted_count + added;
        DELETE FROM pg_temp.dante_lifecycle_tables
         WHERE relation_oid=selected_table;
    END LOOP;

    RETURN deleted_count;
END;
$lifecycle$;
"""


def upgrade() -> None:
    db = op.get_bind()
    db.exec_driver_sql(_GRAPH_DELETE.replace("%", "%%"))
    signature = "dante.delete_self_activity_lifecycle_graph(uuid,uuid,text,uuid)"
    db.exec_driver_sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
    db.exec_driver_sql(
        f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator"
    )


def downgrade() -> None:
    raise RuntimeError("Objective-aware lifecycle deletion is forward-only")
