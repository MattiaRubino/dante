"""B14: actor-owned inert draft vault, independent of Activity/Event/Schedule."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261009_134"
down_revision: str | None = "20261009_133"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    for statement in (_TABLE, _SAVE, _LIST, _RETIRE):
        bind.execute(sa.text(statement))
    bind.exec_driver_sql(
        "CREATE INDEX ix_temporal_draft_vault_owner_updated "
        "ON dante.temporal_draft_vault(owner_person_ref, updated_at DESC, draft_ref)"
    )
    bind.exec_driver_sql("ALTER TABLE dante.temporal_draft_vault OWNER TO dante_owner")
    bind.exec_driver_sql(
        "REVOKE ALL ON TABLE dante.temporal_draft_vault "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )
    for signature in (
        "save_self_temporal_draft(uuid,uuid,text,bigint,text,text,jsonb)",
        "list_self_temporal_drafts(uuid)",
        "retire_self_temporal_draft(uuid,uuid,bigint)",
    ):
        bind.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
        bind.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION dante.{signature} "
            "FROM PUBLIC,dante_runtime,dante_migrator"
        )
        bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("Draft vault state requires a reviewed forward migration")


_TABLE = r"""
CREATE TABLE dante.temporal_draft_vault (
    draft_ref uuid CONSTRAINT pk_temporal_draft_vault PRIMARY KEY,
    owner_person_ref uuid NOT NULL,
    subject_kind text NOT NULL
        CONSTRAINT ck_temporal_draft_vault_kind
        CHECK (subject_kind IN ('activity','event')),
    title text NOT NULL
        CONSTRAINT ck_temporal_draft_vault_title
        CHECK (length(title) <= 300),
    payload jsonb NOT NULL
        CONSTRAINT ck_temporal_draft_vault_payload
        CHECK (jsonb_typeof(payload) = 'object'
               AND octet_length(payload::text) <= 131072),
    revision bigint NOT NULL DEFAULT 1
        CONSTRAINT ck_temporal_draft_vault_revision CHECK (revision >= 1),
    last_operation_id text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    updated_at timestamptz NOT NULL DEFAULT clock_timestamp()
);
"""

_SAVE = r"""
CREATE FUNCTION dante.save_self_temporal_draft(
    actor uuid, requested_draft uuid, operation_id text, expected_revision bigint,
    requested_kind text, requested_title text, requested_payload jsonb
) RETURNS TABLE(
    draft_ref uuid, subject_kind text, title text, payload jsonb,
    revision bigint, created_at timestamptz, updated_at timestamptz
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE
SET search_path = pg_catalog,dante,pg_temp
AS $function$
DECLARE previous dante.temporal_draft_vault%ROWTYPE;
BEGIN
    IF actor IS NULL OR requested_draft IS NULL
       OR operation_id IS NULL OR length(operation_id) NOT BETWEEN 1 AND 200
       OR requested_kind NOT IN ('activity','event')
       OR requested_title IS NULL OR length(requested_title) > 300
       OR requested_payload IS NULL
       OR jsonb_typeof(requested_payload) <> 'object'
       OR octet_length(requested_payload::text) > 131072 THEN
        RAISE EXCEPTION 'invalid draft payload' USING ERRCODE = '22023';
    END IF;
    SELECT * INTO previous FROM dante.temporal_draft_vault AS d
      WHERE d.draft_ref = requested_draft FOR UPDATE;
    IF NOT FOUND THEN
        IF expected_revision IS NOT NULL THEN
            RAISE EXCEPTION 'draft version changed' USING ERRCODE = '40001';
        END IF;
        INSERT INTO dante.temporal_draft_vault AS d (
            draft_ref, owner_person_ref, subject_kind, title, payload, last_operation_id
        ) VALUES (
            requested_draft, actor, requested_kind, requested_title,
            requested_payload, operation_id
        );
    ELSE
        IF previous.owner_person_ref <> actor THEN
            RAISE EXCEPTION 'draft not found' USING ERRCODE = '42501';
        END IF;
        IF previous.last_operation_id = operation_id
           AND previous.subject_kind = requested_kind
           AND previous.title = requested_title
           AND previous.payload = requested_payload THEN
            RETURN QUERY SELECT d.draft_ref,d.subject_kind,d.title,d.payload,
                                d.revision,d.created_at,d.updated_at
              FROM dante.temporal_draft_vault d WHERE d.draft_ref = requested_draft;
            RETURN;
        END IF;
        IF previous.last_operation_id = operation_id THEN
            RAISE EXCEPTION 'draft operation reused' USING ERRCODE = '23505';
        END IF;
        IF previous.revision IS DISTINCT FROM expected_revision THEN
            RAISE EXCEPTION 'draft version changed' USING ERRCODE = '40001';
        END IF;
        UPDATE dante.temporal_draft_vault AS d
           SET subject_kind = requested_kind,
               title = requested_title,
               payload = requested_payload,
               revision = d.revision + 1,
               last_operation_id = operation_id,
               updated_at = clock_timestamp()
         WHERE d.draft_ref = requested_draft;
    END IF;
    RETURN QUERY SELECT d.draft_ref,d.subject_kind,d.title,d.payload,
                        d.revision,d.created_at,d.updated_at
      FROM dante.temporal_draft_vault d WHERE d.draft_ref = requested_draft;
END;
$function$;
"""

_LIST = r"""
CREATE FUNCTION dante.list_self_temporal_drafts(actor uuid)
RETURNS TABLE(
    draft_ref uuid, subject_kind text, title text, payload jsonb,
    revision bigint, created_at timestamptz, updated_at timestamptz
)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path = pg_catalog,dante,pg_temp
AS $function$
    SELECT d.draft_ref,d.subject_kind,d.title,d.payload,
           d.revision,d.created_at,d.updated_at
      FROM dante.temporal_draft_vault d
     WHERE d.owner_person_ref = actor
     ORDER BY d.updated_at DESC,d.draft_ref;
$function$;
"""

_RETIRE = r"""
CREATE FUNCTION dante.retire_self_temporal_draft(
    actor uuid, requested_draft uuid, expected_revision bigint
) RETURNS boolean
LANGUAGE plpgsql SECURITY DEFINER VOLATILE
SET search_path = pg_catalog,dante,pg_temp
AS $function$
DECLARE deleted uuid;
BEGIN
    DELETE FROM dante.temporal_draft_vault d
     WHERE d.owner_person_ref = actor AND d.draft_ref = requested_draft
       AND d.revision = expected_revision
     RETURNING d.draft_ref INTO deleted;
    IF deleted IS NULL THEN
        RAISE EXCEPTION 'draft missing or version changed' USING ERRCODE = '40001';
    END IF;
    RETURN TRUE;
END;
$function$;
