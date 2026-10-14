"""Grant bounded, owner-scoped Activity lifecycle mutations over the FK graph.

Revision ID: 20261014_148
Revises: 20261014_147

Keep does not mutate execution. Delete validates an expected CAS fingerprint and
removes dependent history within the caller's existing transaction, using the
forward-only lifecycle graph capability from _147. No client table privileges.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261014_148"
down_revision: str | None = "20261014_147"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


_HASH = r"""
CREATE FUNCTION dante.get_self_activity_session_impact_hash(
    requested_actor uuid, requested_activity uuid
) RETURNS text
LANGUAGE sql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $lifecycle$
    SELECT encode(
        pg_catalog.sha256(pg_catalog.convert_to(
            COALESCE(pg_catalog.string_agg(
                sessions.session_ref::text || ':' ||
                sessions.timing_material_state_ref::text || ':' ||
                CASE WHEN sessions.ended_at IS NOT NULL THEN 'conclusa'
                     WHEN runtime.paused THEN 'in pausa'
                     ELSE 'in corso'
                END,
                ';' ORDER BY sessions.session_ref
            ),''),'UTF8'
        )), 'hex'
    )
    FROM dante.list_self_subject_sessions(
        requested_actor,requested_activity
    ) AS sessions
    LEFT JOIN LATERAL dante.get_self_session_runtime_metrics(
        requested_actor,sessions.session_ref,sessions.timing_material_state_ref
    ) AS runtime ON true
    WHERE EXISTS (
        SELECT 1 FROM dante.get_self_activity_profile(
            requested_actor,requested_activity
        )
    );
$lifecycle$;
"""


_SESSIONS = r"""
CREATE FUNCTION dante.delete_self_activity_sessions(
    requested_actor uuid, requested_activity uuid, expected_fingerprint text
) RETURNS integer
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $lifecycle$
DECLARE current_fingerprint text;
BEGIN
    -- Root and native-address locks serialize the Activity's Session relation
    -- with concurrent Start; the outer API uses SERIALIZABLE for all other
    -- accepted concurrent history transitions.
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
    current_fingerprint := dante.get_self_activity_session_impact_hash(
        requested_actor,requested_activity
    );
    IF expected_fingerprint IS NULL OR
       current_fingerprint IS DISTINCT FROM expected_fingerprint THEN
        RAISE EXCEPTION USING ERRCODE='23505',
            CONSTRAINT='activity_lifecycle_stale',
            MESSAGE='Session attempts changed since confirmation';
    END IF;
    RETURN dante.delete_self_activity_lifecycle_graph(
        requested_actor,requested_activity,'sessions',NULL
    );
END;
$lifecycle$;
"""


_NAMED = r"""
CREATE FUNCTION dante.delete_self_named_activity_session(
    requested_actor uuid, requested_activity uuid, requested_schedule uuid,
    expected_fingerprint text
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
    current_fingerprint := dante.get_self_activity_session_impact_hash(
        requested_actor,requested_activity
    );
    IF expected_fingerprint IS NULL OR
       current_fingerprint IS DISTINCT FROM expected_fingerprint THEN
        RAISE EXCEPTION USING ERRCODE='23505',
            CONSTRAINT='activity_lifecycle_stale',
            MESSAGE='Session attempts changed since confirmation';
    END IF;
    RETURN dante.delete_self_activity_lifecycle_graph(
        requested_actor,requested_activity,'named',requested_schedule
    );
END;
$lifecycle$;
"""


_ACTIVITY = r"""
CREATE FUNCTION dante.delete_self_activity_hard(
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
    RETURN dante.delete_self_activity_lifecycle_graph(
        requested_actor,requested_activity,'activity',NULL
    );
END;
$lifecycle$;
"""


def upgrade() -> None:
    bind = op.get_bind()
    for statement in (_HASH, _SESSIONS, _NAMED, _ACTIVITY):
        bind.exec_driver_sql(statement)
    signatures = (
        "get_self_activity_session_impact_hash(uuid,uuid)",
        "delete_self_activity_sessions(uuid,uuid,text)",
        "delete_self_named_activity_session(uuid,uuid,uuid,text)",
        "delete_self_activity_hard(uuid,uuid,text)",
    )
    for signature in signatures:
        name = f"dante.{signature}"
        bind.exec_driver_sql(f"ALTER FUNCTION {name} OWNER TO dante_owner")
        bind.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION {name} FROM PUBLIC,dante_runtime,dante_migrator"
        )
        bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {name} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("Hard Activity and Session lifecycle is forward-only")
