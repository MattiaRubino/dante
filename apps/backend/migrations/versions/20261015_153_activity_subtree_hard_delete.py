"""Atomic one-off Activity subtree hard deletion (without archived child Activity).

Revision ID: 20261015_153
Revises: 20261015_152

Scope checked, bounded by depth, rejects shared descendants, then deletes
every independent child Activity identity deepest-first. The original owner
and Session CAS in delete_self_activity_hard remain intact.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261015_153"
down_revision: str | None = "20261015_152"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TREE = r"""
CREATE FUNCTION dante.delete_self_activity_tree(
    requested_actor uuid, requested_activity uuid
) RETURNS integer
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $tree$
#variable_conflict error
DECLARE
    node record;
    affected integer:=0;
BEGIN
    PERFORM 1 FROM dante.activity_intention AS owned
     WHERE owned.activity_ref=requested_activity
       AND owned.self_person_ref=requested_actor
       AND owned.retired_at IS NULL
     FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='activity_lifecycle_unavailable';
    END IF;

    DROP TABLE IF EXISTS pg_temp.dante_delete_activity_tree;
    CREATE TEMP TABLE dante_delete_activity_tree(
        activity_ref uuid PRIMARY KEY,
        depth integer NOT NULL
    ) ON COMMIT DROP;
    INSERT INTO pg_temp.dante_delete_activity_tree(activity_ref,depth)
    WITH RECURSIVE descendants(activity_ref,depth,path) AS (
        SELECT requested_activity,0,ARRAY[requested_activity]
        UNION ALL
        SELECT connection.child_activity_ref, descendants.depth+1,
               descendants.path||connection.child_activity_ref
          FROM descendants
          JOIN dante.activity_decomposition AS connection
            ON connection.parent_activity_ref=descendants.activity_ref
           AND connection.self_person_ref=requested_actor
         WHERE descendants.depth<32
           AND NOT connection.child_activity_ref=ANY(descendants.path)
    )
    SELECT descendants.activity_ref,MAX(descendants.depth)
      FROM descendants
     GROUP BY descendants.activity_ref;

    -- No silent truncation and no deletion of shared descendants.
    IF EXISTS (
      SELECT 1 FROM pg_temp.dante_delete_activity_tree AS entry
      JOIN dante.activity_decomposition AS linked
        ON linked.parent_activity_ref=entry.activity_ref
       AND linked.self_person_ref=requested_actor
      WHERE entry.depth>=32
    ) OR EXISTS (
      SELECT 1 FROM dante.activity_decomposition AS linked
      JOIN pg_temp.dante_delete_activity_tree AS entry
        ON entry.activity_ref=linked.child_activity_ref
      WHERE entry.depth>0
        AND NOT EXISTS(
          SELECT 1 FROM pg_temp.dante_delete_activity_tree AS parent
           WHERE parent.activity_ref=linked.parent_activity_ref
        )
    ) THEN
      RAISE EXCEPTION USING ERRCODE='23514',
         CONSTRAINT='activity_lifecycle_external_child',
         MESSAGE='Activity subtree exceeds depth or includes a shared child';
    END IF;

    FOR node IN
      SELECT activity_ref FROM pg_temp.dante_delete_activity_tree
       ORDER BY depth DESC,activity_ref
    LOOP
       affected:=affected+dante.delete_self_activity_lifecycle_graph(
           requested_actor,node.activity_ref,'activity',NULL
       );
    END LOOP;
    RETURN affected;
END;
$tree$;"""

_ACTIVITY = r"""
CREATE OR REPLACE FUNCTION dante.delete_self_activity_hard(
    requested_actor uuid, requested_activity uuid, expected_fingerprint text
) RETURNS integer
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $lifecycle$
DECLARE current_fingerprint text;
BEGIN
    PERFORM 1 FROM dante.activity_intention AS activity
      WHERE activity.activity_ref=requested_activity
        AND activity.self_person_ref=requested_actor
        AND activity.retired_at IS NULL
      FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='activity_lifecycle_unavailable',
            MESSAGE='Activity unavailable';
    END IF;
    PERFORM 1 FROM dante.native_address AS address
     WHERE address.native_ref=requested_activity FOR UPDATE;
    -- The recurring source can rematerialize this instance after a bare
    -- Activity delete. Require an explicit Occurrence-scoped operation.
    IF EXISTS (
        SELECT 1 FROM dante.routine_occurrence_activity_instance AS link
         WHERE link.activity_ref=requested_activity
           AND link.self_person_ref=requested_actor
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
            CONSTRAINT='activity_lifecycle_recurring_scope_required',
            MESSAGE='Recurring Activity requires an Occurrence-scoped deletion';
    END IF;
    current_fingerprint := dante.get_self_activity_session_impact_hash(
        requested_actor,requested_activity
    );
    IF expected_fingerprint IS NULL OR
       current_fingerprint IS DISTINCT FROM expected_fingerprint THEN
        RAISE EXCEPTION USING ERRCODE='23505',
            CONSTRAINT='activity_lifecycle_stale',
            MESSAGE='Session attempts changed since confirmation';
    END IF;
    RETURN dante.delete_self_activity_tree(requested_actor,requested_activity);
END;
$lifecycle$;
"""


def upgrade() -> None:
    db = op.get_bind()
    db.exec_driver_sql(_TREE)
    db.exec_driver_sql(_ACTIVITY)
    name = "dante.delete_self_activity_tree(uuid,uuid)"
    db.exec_driver_sql(f"ALTER FUNCTION {name} OWNER TO dante_owner")
    db.exec_driver_sql(f"REVOKE ALL ON FUNCTION {name} FROM PUBLIC,dante_migrator,dante_runtime")
    # Existing guarded public command retains its original runtime grant.
    db.exec_driver_sql(
        "ALTER FUNCTION dante.delete_self_activity_hard(uuid,uuid,text) OWNER TO dante_owner"
    )


def downgrade() -> None:
    raise RuntimeError("Bounded Activity subtree hard-delete is forward-only")
