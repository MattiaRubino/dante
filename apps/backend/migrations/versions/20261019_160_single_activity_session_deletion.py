"""Delete one owned Activity Session without removing its configuration.

Revision ID: 20261019_160
Revises: 20261015_159

The existing bounded FK graph remains the only deletion engine. Extend its
root selection to one Session and expose a guarded owner/CAS wrapper.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261019_160"
down_revision: str | None = "20261015_159"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


_SINGLE = r"""
CREATE FUNCTION dante.delete_self_activity_session_attempt(
    requested_actor uuid, requested_activity uuid, requested_session uuid,
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
       AND activity.retired_at IS NULL FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='activity_lifecycle_unavailable',
            MESSAGE='Activity unavailable';
    END IF;
    PERFORM 1 FROM dante.native_address AS address
     WHERE address.native_ref=requested_activity FOR UPDATE;
    PERFORM 1 FROM dante.session AS real
      JOIN dante.session_execution_subject AS subject
        ON subject.session_ref=real.session_ref
     WHERE subject.subject_native_ref=requested_activity
       AND real.session_ref=requested_session
     FOR UPDATE OF real;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='activity_lifecycle_session_unavailable',
            MESSAGE='Session unavailable in this Activity';
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
        requested_actor,requested_activity,'single',requested_session
    );
END;
$lifecycle$;
"""


def upgrade() -> None:
    db = op.get_bind()
    signature = "dante.delete_self_activity_lifecycle_graph(uuid,uuid,text,uuid)"
    definition = db.exec_driver_sql(
        "SELECT pg_get_functiondef(%s::regprocedure)", (signature,)
    ).scalar_one()
    replacements = (
        (
            "requested_scope NOT IN ('sessions','named','activity')",
            "requested_scope NOT IN ('sessions','named','single','activity')",
            1,
        ),
        (
            "requested_scope='named' AND requested_named_schedule IS NULL",
            "requested_scope IN ('named','single') AND requested_named_schedule IS NULL",
            1,
        ),
        (
            "requested_scope<>'named' AND requested_named_schedule IS NOT NULL",
            "requested_scope NOT IN ('named','single') AND requested_named_schedule IS NOT NULL",
            1,
        ),
    )
    for old, new, count in replacements:
        if definition.count(old) != count:
            raise RuntimeError(f"Unexpected lifecycle graph definition: {old}")
        definition = definition.replace(old, new)
    predicate = "requested_scope<>'named'\n            OR EXISTS ("
    if definition.count(predicate) != 4:
        raise RuntimeError("Unexpected Session root selection in lifecycle graph")
    for alias in ("real", "real", "subject", "subject"):
        definition = definition.replace(
            predicate,
            "requested_scope NOT IN ('named','single')\n"
            f"            OR (requested_scope='single' AND {alias}.session_ref=requested_named_schedule)\n"
            "            OR EXISTS (",
            1,
        )
    db.exec_driver_sql(definition.replace("%", "%%"))
    db.exec_driver_sql(_SINGLE)
    name = "dante.delete_self_activity_session_attempt(uuid,uuid,uuid,text)"
    db.exec_driver_sql(f"ALTER FUNCTION {name} OWNER TO dante_owner")
    db.exec_driver_sql(f"REVOKE ALL ON FUNCTION {name} FROM PUBLIC,dante_runtime,dante_migrator")
    db.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {name} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("Activity Session deletion is forward-only")
