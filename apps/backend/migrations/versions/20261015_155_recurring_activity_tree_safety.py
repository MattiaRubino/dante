"""Use one bounded, shared-child-safe Activity subtree authority for recurring deletes.

Revision ID: 20261015_155
Revises: 20261015_154

Never let recurring deletion bypass one-off Activity subtree invariants.
Only one owner-checked deletion code path handles child identities, CAS and
transactional rollback. Does not change executable runtime grants or catalog
topology: this is an existing function replacement, forward only.
"""
from collections.abc import Sequence

from alembic import op

revision: str = "20261015_155"
down_revision: str | None = "20261015_154"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_DELETE = r"""
CREATE OR REPLACE FUNCTION dante.delete_self_temporal_hard(
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
      -- Reuse the single canonical, owner-checked Activity subtree deleter,
      -- including its external/shared-child rejection and depth guard.
      -- Do not maintain a second weaker recursive deletion implementation.
      affected:=affected+dante.delete_self_activity_tree(
          requested_actor,generated.activity_ref
      );
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
    db = op.get_bind()
    db.exec_driver_sql(_DELETE.replace("%", "%%"))
    name = "dante.delete_self_temporal_hard(uuid,uuid,text,text)"
    db.exec_driver_sql(f"ALTER FUNCTION {name} OWNER TO dante_owner")


def downgrade() -> None:
    raise RuntimeError("Shared-safe recursive Activity hard deletion is forward-only")
