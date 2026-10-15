"""Scoped and serialized hard deletion of recurring Activity/Event truth.

Revision ID: 20261015_152
Revises: 20261015_151

Bounded owner-scoped capabilities: no runtime direct table DELETE.
The only retained single-instance residue is the technical Occurrence skip
required to prevent deterministic rematerialization; the recurrence source
and sibling instances remain. Whole-series deletion removes the native source,
generated Activities and all Occurrence descendants.

These capabilities are candidates pending real PostgreSQL, browser and
concurrency acceptance performed on the user's WSL environment.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261015_152"
down_revision: str | None = "20261015_151"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_GRAPH = r"""
CREATE FUNCTION dante.delete_self_temporal_root_graph(
    requested_actor uuid, requested_root uuid, requested_kind text
) RETURNS integer
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $lifecycle$
#variable_conflict error
DECLARE
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
    source uuid;
BEGIN
    IF requested_kind='routine' THEN
        PERFORM 1 FROM dante.routine_intention AS owned
         WHERE owned.routine_ref=requested_root
           AND owned.self_person_ref=requested_actor
         FOR UPDATE;
    ELSIF requested_kind='event' THEN
        PERFORM 1 FROM dante.event_expectation AS owned
         WHERE owned.event_ref=requested_root
           AND owned.self_person_ref=requested_actor
         FOR UPDATE;
    ELSIF requested_kind='event_occurrence_content' THEN
        SELECT generation.source_native_ref INTO source
          FROM dante.occurrence_generation AS generation
          JOIN dante.event_expectation AS owned
            ON owned.event_ref=generation.source_native_ref
           AND owned.self_person_ref=requested_actor
         WHERE generation.occurrence_ref=requested_root
         FOR UPDATE OF generation,owned;
    ELSE
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='temporal_hard_invalid_scope',
          MESSAGE='Invalid temporal graph kind';
    END IF;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
          CONSTRAINT='temporal_hard_unavailable',
          MESSAGE='Temporal graph not owned';
    END IF;

    DROP TABLE IF EXISTS pg_temp.dante_lifecycle_targets;
    DROP TABLE IF EXISTS pg_temp.dante_lifecycle_tables;
    CREATE TEMP TABLE dante_lifecycle_targets (
       relation_oid oid NOT NULL,
       tuple_id tid NOT NULL,
       PRIMARY KEY(relation_oid,tuple_id)
    ) ON COMMIT DROP;

    IF requested_kind IN ('routine','event') THEN
        INSERT INTO pg_temp.dante_lifecycle_targets
        SELECT 'dante.native_address'::regclass, address.ctid
          FROM dante.native_address AS address
         WHERE address.native_ref=requested_root
        ON CONFLICT DO NOTHING;
        IF requested_kind='routine' THEN
            INSERT INTO pg_temp.dante_lifecycle_targets
            SELECT 'dante.routine'::regclass, owned.ctid
              FROM dante.routine AS owned
             WHERE owned.routine_ref=requested_root
            ON CONFLICT DO NOTHING;
        ELSE
            INSERT INTO pg_temp.dante_lifecycle_targets
            SELECT 'dante.event'::regclass, owned.ctid
              FROM dante.event AS owned
             WHERE owned.event_ref=requested_root
            ON CONFLICT DO NOTHING;
        END IF;

        -- Objective subject references are polymorphic (no native FK).
        INSERT INTO pg_temp.dante_lifecycle_targets
        SELECT 'dante.temporal_objective'::regclass, objective.ctid
          FROM dante.temporal_objective AS objective
         WHERE objective.self_person_ref=requested_actor
           AND (
                (objective.subject_kind=requested_kind AND
                 objective.subject_native_ref=requested_root)
                OR
                (objective.subject_kind='occurrence' AND EXISTS(
                   SELECT 1 FROM dante.occurrence_generation AS generation
                    WHERE generation.source_native_ref=requested_root
                      AND generation.occurrence_ref=objective.subject_native_ref
                ))
           )
        ON CONFLICT DO NOTHING;
    ELSE
        -- Retain only the durable Occurrence provenance and skip receipt.
        -- Its Schedule/Actual/Objective and descendants are product content.
        INSERT INTO pg_temp.dante_lifecycle_targets
        SELECT 'dante.schedule'::regclass, schedule.ctid
          FROM dante.schedule AS schedule
         WHERE schedule.subject_native_ref=requested_root
        ON CONFLICT DO NOTHING;
        INSERT INTO pg_temp.dante_lifecycle_targets
        SELECT 'dante.actual'::regclass, actual.ctid
          FROM dante.actual AS actual
         WHERE actual.subject_native_ref=requested_root
        ON CONFLICT DO NOTHING;
        INSERT INTO pg_temp.dante_lifecycle_targets
        SELECT 'dante.temporal_objective'::regclass, objective.ctid
          FROM dante.temporal_objective AS objective
         WHERE objective.self_person_ref=requested_actor
           AND objective.subject_kind='occurrence'
           AND objective.subject_native_ref=requested_root
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
$lifecycle$;"""

_PREVIEW = r"""
CREATE FUNCTION dante.get_self_temporal_hard_delete_fingerprint(
  requested_actor uuid, requested_ref uuid, requested_scope text
) RETURNS text
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $preview$
DECLARE source uuid; instance uuid; body text; activity_state text; occurrence_state text;
        objective_state text; schedule_state text; event_version bigint;
BEGIN
  IF requested_scope IN ('activity_instance','activity_series') THEN
    SELECT g.source_native_ref,link.occurrence_ref INTO source,instance
      FROM dante.routine_occurrence_activity_instance AS link
      JOIN dante.occurrence_generation AS g ON g.occurrence_ref=link.occurrence_ref
      JOIN dante.routine_intention AS owned
        ON owned.routine_ref=g.source_native_ref
       AND owned.self_person_ref=requested_actor
      JOIN dante.activity_intention AS activity
        ON activity.activity_ref=link.activity_ref
       AND activity.self_person_ref=requested_actor
       AND activity.retired_at IS NULL
     WHERE link.activity_ref=requested_ref;
  ELSIF requested_scope='event_once' THEN
    SELECT owned.event_ref INTO source
      FROM dante.event_expectation AS owned
     WHERE owned.event_ref=requested_ref AND owned.self_person_ref=requested_actor
       AND NOT EXISTS (
         SELECT 1 FROM dante.event_recurrence_state AS recurrence
          WHERE recurrence.event_ref=owned.event_ref
       );
  ELSIF requested_scope='event_instance' THEN
    SELECT generation.source_native_ref INTO source
      FROM dante.occurrence_generation AS generation
      JOIN dante.event_expectation AS owned
        ON owned.event_ref=generation.source_native_ref
       AND owned.self_person_ref=requested_actor
     WHERE generation.occurrence_ref=requested_ref
       AND NOT EXISTS (
          SELECT 1 FROM dante.occurrence_skip AS skipped
           WHERE skipped.occurrence_ref=requested_ref
       );
    instance:=requested_ref;
  ELSIF requested_scope='event_series' THEN
    SELECT owned.event_ref INTO source FROM dante.event_expectation AS owned
     WHERE owned.event_ref=requested_ref AND owned.self_person_ref=requested_actor;
    IF source IS NULL THEN
      SELECT generation.source_native_ref INTO source
        FROM dante.occurrence_generation AS generation
        JOIN dante.event_expectation AS owned
          ON owned.event_ref=generation.source_native_ref
         AND owned.self_person_ref=requested_actor
       WHERE generation.occurrence_ref=requested_ref;
    END IF;
  ELSE
    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='temporal_hard_invalid_scope';
  END IF;
  IF source IS NULL THEN
    RAISE EXCEPTION USING ERRCODE='23503',CONSTRAINT='temporal_hard_unavailable';
  END IF;
  IF requested_scope LIKE 'activity_%' THEN
    SELECT COALESCE(string_agg(
      activity.activity_ref::text||':'||activity.profile_revision::text||':'||
      COALESCE(dante.get_self_activity_session_impact_hash(
        requested_actor,activity.activity_ref),'missing'),
      ';' ORDER BY activity.activity_ref),'')
      INTO activity_state
      FROM dante.activity_intention AS activity
     WHERE activity.self_person_ref=requested_actor
       AND activity.retired_at IS NULL
       AND (
          (requested_scope='activity_instance' AND activity.activity_ref=requested_ref)
          OR (requested_scope='activity_series' AND
          (EXISTS(
             SELECT 1 FROM dante.routine_occurrence_activity_instance AS link
             JOIN dante.occurrence_generation AS generation
               ON generation.occurrence_ref=link.occurrence_ref
             WHERE generation.source_native_ref=source
               AND link.activity_ref=activity.activity_ref
          ) OR EXISTS (
             SELECT 1 FROM dante.activity_create_operation AS receipt
             JOIN dante.occurrence_generation AS generation
               ON receipt.operation_id='b14:occurrence-activity:'||
                    generation.occurrence_ref::text
             WHERE generation.source_native_ref=source
               AND receipt.activity_ref=activity.activity_ref
               AND receipt.self_person_ref=requested_actor
          )))
       );
  ELSE
    SELECT dante.get_self_event_profile_revision(requested_actor,source)
       INTO event_version;
    activity_state:=COALESCE(event_version::text,'missing');
  END IF;
  SELECT COALESCE(string_agg(
      generation.occurrence_ref::text||':'||
      COALESCE(skip.skipped_at::text,'active'),
      ';' ORDER BY generation.occurrence_ref),'')
    INTO occurrence_state
    FROM dante.occurrence_generation AS generation
    LEFT JOIN dante.occurrence_skip AS skip
      ON skip.occurrence_ref=generation.occurrence_ref
   WHERE generation.source_native_ref=source
     AND (instance IS NULL OR generation.occurrence_ref=instance);
  SELECT COALESCE(string_agg(
      objective.objective_ref::text||':'||COALESCE(objective.retired_at::text,'active'),
      ';' ORDER BY objective.objective_ref),'')
    INTO objective_state
    FROM dante.temporal_objective AS objective
   WHERE objective.self_person_ref=requested_actor AND
    ((requested_scope='activity_instance' AND
      objective.subject_kind='activity' AND objective.subject_native_ref=requested_ref)
     OR (requested_scope='activity_series' AND objective.subject_kind='activity'
      AND EXISTS(
         SELECT 1 FROM dante.routine_occurrence_activity_instance AS link
         JOIN dante.occurrence_generation AS g ON g.occurrence_ref=link.occurrence_ref
         WHERE g.source_native_ref=source AND link.activity_ref=objective.subject_native_ref
      ))
     OR (requested_scope='event_once' AND objective.subject_kind='event'
         AND objective.subject_native_ref=source)
     OR (requested_scope='event_instance' AND objective.subject_kind='occurrence'
         AND objective.subject_native_ref=instance)
     OR (requested_scope='event_series' AND
        (objective.subject_kind='event' AND objective.subject_native_ref=source
         OR objective.subject_kind='occurrence' AND EXISTS(
            SELECT 1 FROM dante.occurrence_generation AS g
             WHERE g.source_native_ref=source
               AND g.occurrence_ref=objective.subject_native_ref
         ))));
  SELECT COALESCE(string_agg(
      schedule.schedule_ref::text,
      ';' ORDER BY schedule.schedule_ref),'')
    INTO schedule_state FROM dante.schedule AS schedule
   WHERE (requested_scope='event_once' AND schedule.subject_native_ref=source)
      OR (requested_scope='event_instance' AND schedule.subject_native_ref=instance)
      OR (requested_scope='event_series' AND
         (schedule.subject_native_ref=source OR EXISTS(
            SELECT 1 FROM dante.occurrence_generation AS g
            WHERE g.source_native_ref=source AND g.occurrence_ref=schedule.subject_native_ref
         )));
  body:=requested_scope||':'||requested_ref::text||':'||source::text||':'||
        COALESCE(activity_state,'')||':'||COALESCE(occurrence_state,'')||':'||
        COALESCE(objective_state,'')||':'||COALESCE(schedule_state,'');
  RETURN encode(pg_catalog.sha256(pg_catalog.convert_to(body,'UTF8')),'hex');
END;
$preview$;"""

_DELETE = r"""
CREATE FUNCTION dante.delete_self_temporal_hard(
 requested_actor uuid, requested_ref uuid, requested_scope text,
 expected_fingerprint text
) RETURNS integer
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $deletion$
DECLARE source uuid; occurrence uuid; generated record; child record;
        affected integer:=0; current_fingerprint text; exclusion_operation text;
        has_target boolean;
BEGIN
  IF requested_scope IN ('activity_instance','activity_series') THEN
    SELECT g.source_native_ref,link.occurrence_ref INTO source,occurrence
      FROM dante.routine_occurrence_activity_instance AS link
      JOIN dante.occurrence_generation AS g ON g.occurrence_ref=link.occurrence_ref
      JOIN dante.routine_intention AS owned
        ON owned.routine_ref=g.source_native_ref
       AND owned.self_person_ref=requested_actor
     WHERE link.activity_ref=requested_ref;
  ELSIF requested_scope IN ('event_once','event_series') THEN
    SELECT owned.event_ref INTO source
      FROM dante.event_expectation AS owned
     WHERE owned.event_ref=requested_ref AND owned.self_person_ref=requested_actor;
    IF source IS NULL AND requested_scope='event_series' THEN
      SELECT g.source_native_ref INTO source
        FROM dante.occurrence_generation AS g
        JOIN dante.event_expectation AS owned
          ON owned.event_ref=g.source_native_ref
         AND owned.self_person_ref=requested_actor
       WHERE g.occurrence_ref=requested_ref;
    END IF;
  ELSIF requested_scope='event_instance' THEN
    SELECT g.source_native_ref INTO source
      FROM dante.occurrence_generation AS g
      JOIN dante.event_expectation AS owned
        ON owned.event_ref=g.source_native_ref
       AND owned.self_person_ref=requested_actor
     WHERE g.occurrence_ref=requested_ref;
    occurrence:=requested_ref;
  ELSE
    RAISE EXCEPTION USING ERRCODE='23514',CONSTRAINT='temporal_hard_invalid_scope';
  END IF;
  IF source IS NULL THEN
    RAISE EXCEPTION USING ERRCODE='23503',CONSTRAINT='temporal_hard_unavailable';
  END IF;

  -- All producer materialization of this source holds the same advisory lock
  -- until its Activity/Event instance payload and binding are finished.
  PERFORM pg_advisory_xact_lock(hashtextextended(
    'dante:recurrence-materialization:'||source::text,0
  ));
  IF requested_scope LIKE 'activity_%' THEN
    PERFORM 1 FROM dante.routine_intention AS owned
     WHERE owned.routine_ref=source AND owned.self_person_ref=requested_actor
     FOR UPDATE;
  ELSE
    PERFORM 1 FROM dante.event_expectation AS owned
     WHERE owned.event_ref=source AND owned.self_person_ref=requested_actor
     FOR UPDATE;
  END IF;
  IF NOT FOUND THEN
    RAISE EXCEPTION USING ERRCODE='23503',CONSTRAINT='temporal_hard_unavailable';
  END IF;

  current_fingerprint:=dante.get_self_temporal_hard_delete_fingerprint(
      requested_actor,requested_ref,requested_scope
  );
  IF expected_fingerprint IS NULL OR
     expected_fingerprint IS DISTINCT FROM current_fingerprint THEN
    RAISE EXCEPTION USING ERRCODE='23505',CONSTRAINT='temporal_hard_stale',
       MESSAGE='Recurring deletion confirmation is stale';
  END IF;
  IF requested_scope IN ('activity_instance','event_instance') THEN
    -- A technical skip receipt remains to prevent occurrence resurrection.
    exclusion_operation:='temporal:hard-delete:'||occurrence::text;
    PERFORM 1 FROM dante.skip_self_occurrence(
      requested_actor,exclusion_operation,
      encode(pg_catalog.sha256(pg_catalog.convert_to(exclusion_operation,'UTF8')),'hex'),
      occurrence,'Eliminazione definitiva istanza'
    );
    affected:=affected+1; -- The durable exclusion is one accepted mutation.
  END IF;

  IF requested_scope IN ('activity_instance','activity_series') THEN
    FOR generated IN
      SELECT DISTINCT activity.activity_ref
        FROM dante.activity_intention AS activity
       WHERE activity.self_person_ref=requested_actor
         AND activity.retired_at IS NULL
         AND (
           EXISTS (
             SELECT 1 FROM dante.routine_occurrence_activity_instance AS linked
             JOIN dante.occurrence_generation AS g
               ON g.occurrence_ref=linked.occurrence_ref
             WHERE linked.activity_ref=activity.activity_ref
               AND g.source_native_ref=source
               AND (requested_scope='activity_series' OR g.occurrence_ref=occurrence)
           )
           OR EXISTS (
             SELECT 1 FROM dante.activity_create_operation AS created
             JOIN dante.occurrence_generation AS g
               ON created.operation_id='b14:occurrence-activity:'||g.occurrence_ref::text
             WHERE created.activity_ref=activity.activity_ref
               AND created.self_person_ref=requested_actor
               AND g.source_native_ref=source
               AND (requested_scope='activity_series' OR g.occurrence_ref=occurrence)
           )
         )
       ORDER BY activity.activity_ref
    LOOP
      -- Delete descendants deepest-first. Ordinary schedule/session deletion
      -- cannot account for their independent Activity native identities.
      FOR child IN
        WITH RECURSIVE subtree(activity_ref,depth,path) AS (
          SELECT generated.activity_ref,0,ARRAY[generated.activity_ref]
          UNION ALL
          SELECT d.child_activity_ref,subtree.depth+1,
                 subtree.path||d.child_activity_ref
            FROM subtree
            JOIN dante.activity_decomposition AS d
              ON d.parent_activity_ref=subtree.activity_ref
             AND d.self_person_ref=requested_actor
           WHERE subtree.depth<32
             AND NOT d.child_activity_ref=ANY(subtree.path)
        )
        SELECT activity_ref,MAX(depth) AS depth
          FROM subtree
         GROUP BY activity_ref
         ORDER BY depth DESC,activity_ref
      LOOP
        IF EXISTS(
           SELECT 1 FROM dante.activity_intention AS owned
            WHERE owned.activity_ref=child.activity_ref
              AND owned.self_person_ref=requested_actor
              AND owned.retired_at IS NULL
        ) THEN
          affected:=affected+dante.delete_self_activity_lifecycle_graph(
            requested_actor,child.activity_ref,'activity',NULL
          );
        END IF;
      END LOOP;
    END LOOP;
  END IF;

  IF requested_scope='activity_series' THEN
    affected:=affected+dante.delete_self_temporal_root_graph(
       requested_actor,source,'routine'
    );
  ELSIF requested_scope='event_once' OR requested_scope='event_series' THEN
    affected:=affected+dante.delete_self_temporal_root_graph(
       requested_actor,source,'event'
    );
  ELSIF requested_scope='event_instance' THEN
    affected:=affected+dante.delete_self_temporal_root_graph(
       requested_actor,occurrence,'event_occurrence_content'
    );
  END IF;
  RETURN affected;
END;
$deletion$;"""


def upgrade() -> None:
    bind = op.get_bind()
    for statement in (_GRAPH, _PREVIEW, _DELETE):
        bind.exec_driver_sql(statement.replace("%", "%%"))
    for signature in (
        "delete_self_temporal_root_graph(uuid,uuid,text)",
        "get_self_temporal_hard_delete_fingerprint(uuid,uuid,text)",
        "delete_self_temporal_hard(uuid,uuid,text,text)",
    ):
        name = f"dante.{signature}"
        bind.exec_driver_sql(f"ALTER FUNCTION {name} OWNER TO dante_owner")
        bind.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION {name} FROM PUBLIC,dante_migrator,dante_runtime"
        )
        if signature != "delete_self_temporal_root_graph(uuid,uuid,text)":
            bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {name} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("Atomic recurring temporal deletion is forward-only")
