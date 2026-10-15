"""Include polymorphic Reality policies in owned hard-deletion graphs.

Revision ID: 20261015_158
Revises: 20261015_157

Policy subjects have no FK to NativeRef/Occurrence. Replace only the known
forward-migrated function bodies; unexpected prior definitions fail migration.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261015_158"
down_revision: str | None = "20261015_157"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _replace_function(signature: str, old: str, new: str) -> None:
    db = op.get_bind()
    definition = db.exec_driver_sql(
        "SELECT pg_get_functiondef(%s::regprocedure)", (signature,)
    ).scalar_one()
    if definition.count(old) != 1 or new in definition:
        raise RuntimeError(f"Unexpected hard-delete function body: {signature}")
    db.exec_driver_sql(definition.replace(old, new).replace("%", "%%"))


def upgrade() -> None:
    _replace_function(
        "dante.delete_self_activity_lifecycle_graph(uuid,uuid,text,uuid)",
        "    -- Traverse only real dante-schema foreign-key descendants of the selected",
        """    -- The policy's subject is polymorphic, like the Objective: no FK
    -- connects it to the Activity native address. Its history and operation
    -- receipts are ordinary FK descendants of this selected root.
    IF requested_scope='activity' THEN
        INSERT INTO pg_temp.dante_lifecycle_targets(relation_oid,tuple_id)
        SELECT 'dante.reality_review_policy'::regclass, policy.ctid
          FROM dante.reality_review_policy AS policy
         WHERE policy.subject_kind='activity'
           AND policy.subject_native_ref=requested_activity
           AND policy.self_person_ref=requested_actor
        ON CONFLICT DO NOTHING;
    END IF;

    -- Traverse only real dante-schema foreign-key descendants of the selected""",
    )
    _replace_function(
        "dante.delete_self_temporal_root_graph(uuid,uuid,text)",
        "    -- Traverse only real dante-schema foreign-key descendants of the selected",
        """    -- Event/Occurrence Reality policy uses a polymorphic subject key,
    -- so FK traversal alone cannot discover this owner-scoped root.
    INSERT INTO pg_temp.dante_lifecycle_targets(relation_oid,tuple_id)
    SELECT 'dante.reality_review_policy'::regclass, policy.ctid
      FROM dante.reality_review_policy AS policy
     WHERE policy.self_person_ref=requested_actor
       AND (
         (requested_kind='event' AND
           ((policy.subject_kind='event' AND policy.subject_native_ref=requested_root)
            OR (policy.subject_kind='occurrence' AND EXISTS (
              SELECT 1 FROM dante.occurrence_generation AS generation
               WHERE generation.source_native_ref=requested_root
                 AND generation.occurrence_ref=policy.subject_native_ref
            ))))
         OR (requested_kind='event_occurrence_content'
             AND policy.subject_kind='occurrence'
             AND policy.subject_native_ref=requested_root)
       )
    ON CONFLICT DO NOTHING;

    -- Traverse only real dante-schema foreign-key descendants of the selected""",
    )
    _replace_function(
        "dante.get_self_temporal_hard_delete_fingerprint(uuid,uuid,text)",
        "objective_state text; schedule_state text; event_version bigint;",
        "objective_state text; schedule_state text; policy_state text; event_version bigint;",
    )
    _replace_function(
        "dante.get_self_temporal_hard_delete_fingerprint(uuid,uuid,text)",
        "  body:=requested_scope||':'||requested_ref::text||':'||source::text||':'||",
        """  SELECT COALESCE(string_agg(
      policy.subject_kind||':'||policy.subject_native_ref::text||':'||
      COALESCE(current.state_ref::text,'none'),
      ';' ORDER BY policy.subject_kind,policy.subject_native_ref),'')
    INTO policy_state
    FROM dante.reality_review_policy AS policy
    LEFT JOIN dante.reality_review_policy_current_history AS current
      ON current.subject_kind=policy.subject_kind
     AND current.subject_native_ref=policy.subject_native_ref
     AND current.current_until_at IS NULL
   WHERE policy.self_person_ref=requested_actor
     AND (
       (requested_scope='activity_instance' AND policy.subject_kind='activity'
        AND policy.subject_native_ref=requested_ref)
       OR (requested_scope='activity_series' AND policy.subject_kind='activity'
         AND EXISTS (
           SELECT 1 FROM dante.routine_occurrence_activity_instance AS link
           JOIN dante.occurrence_generation AS g
             ON g.occurrence_ref=link.occurrence_ref
           WHERE g.source_native_ref=source
             AND link.activity_ref=policy.subject_native_ref
         ))
       OR (requested_scope='event_once' AND policy.subject_kind='event'
           AND policy.subject_native_ref=source)
       OR (requested_scope='event_instance' AND policy.subject_kind='occurrence'
           AND policy.subject_native_ref=instance)
       OR (requested_scope='event_series' AND
           ((policy.subject_kind='event' AND policy.subject_native_ref=source)
            OR (policy.subject_kind='occurrence' AND EXISTS (
              SELECT 1 FROM dante.occurrence_generation AS g
               WHERE g.source_native_ref=source
                 AND g.occurrence_ref=policy.subject_native_ref
            ))))
     );
  body:=requested_scope||':'||requested_ref::text||':'||source::text||':'||""",
    )
    _replace_function(
        "dante.get_self_temporal_hard_delete_fingerprint(uuid,uuid,text)",
        "COALESCE(objective_state,'')||':'||COALESCE(schedule_state,'');",
        "COALESCE(objective_state,'')||':'||COALESCE(schedule_state,'')||':'||COALESCE(policy_state,'');",
    )


def downgrade() -> None:
    raise RuntimeError("Owned Reality policy hard deletion is forward-only")
