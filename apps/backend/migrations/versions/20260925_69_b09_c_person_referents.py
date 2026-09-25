"""B09-C: self-scoped, non-Account Person referents for temporal roles.

Revision ID: 20260925_69
Revises: 20260925_68

The Person is native identity; the owner's display label is local presentation.
Only bounded capabilities may create or rename a referent. No Account,
invitation, response or Actual Participation is inferred.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260925_69"
down_revision: str | None = "20260925_68"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _sql(statement: str) -> None:
    op.execute(sa.text(statement))


_CREATE = r"""
CREATE FUNCTION dante.create_self_person_referent(
  requested_self_person_ref uuid,
  requested_operation_id text,
  requested_fingerprint text,
  requested_person_ref uuid,
  requested_display_label text
) RETURNS TABLE(person_ref uuid, display_label text, revision bigint, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
DECLARE
  op_id text := btrim(requested_operation_id);
  label text := btrim(requested_display_label);
  receipt record;
  created_at timestamptz := statement_timestamp();
BEGIN
  IF op_id IS NULL OR op_id = '' OR char_length(op_id) > 200
     OR requested_fingerprint IS NULL
     OR requested_fingerprint !~ '^[0-9a-f]{64}$'
     OR label IS NULL OR label = '' OR char_length(label) > 100
     OR uuid_extract_version(requested_person_ref) IS DISTINCT FROM 7 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='person_referent_invalid_input', MESSAGE='Invalid Person referent request';
  END IF;
  PERFORM pg_advisory_xact_lock(
    hashtextextended(requested_self_person_ref::text || '|person-referent|' || op_id,0)
  );
  SELECT o.intent_fingerprint, o.person_ref, o.display_label, o.resulting_revision,
         o.operation_kind INTO receipt
    FROM dante.person_referent_operation AS o
   WHERE o.self_person_ref=requested_self_person_ref AND o.operation_id=op_id;
  IF FOUND THEN
    IF receipt.intent_fingerprint <> requested_fingerprint
       OR receipt.operation_kind <> 'create'
       OR receipt.display_label <> label THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        CONSTRAINT='person_referent_operation_reused',
        MESSAGE='Person referent operation id reused';
    END IF;
    RETURN QUERY SELECT receipt.person_ref, receipt.display_label,
                        receipt.resulting_revision, true;
    RETURN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM dante.account_application_context AS a
                  WHERE a.self_person_ref=requested_self_person_ref) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='person_referent_self_unavailable', MESSAGE='Self Person unavailable';
  END IF;
  INSERT INTO dante.person(person_ref) VALUES(requested_person_ref);
  INSERT INTO dante.native_address(native_ref,owner_family)
    VALUES(requested_person_ref,'person');
  INSERT INTO dante.person_referent_catalog(
    self_person_ref,person_ref,display_label,revision,created_at,updated_at
  ) VALUES(requested_self_person_ref,requested_person_ref,label,1,created_at,created_at);
  INSERT INTO dante.person_referent_operation(
    self_person_ref,operation_id,intent_fingerprint,operation_kind,
    person_ref,display_label,resulting_revision,accepted_at
  ) VALUES(requested_self_person_ref,op_id,requested_fingerprint,'create',
           requested_person_ref,label,1,created_at);
  RETURN QUERY SELECT requested_person_ref,label,1::bigint,false;
END;
$function$
"""

_LIST = r"""
CREATE FUNCTION dante.list_self_person_referents(requested_self_person_ref uuid)
RETURNS TABLE(person_ref uuid, display_label text, revision bigint)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT r.person_ref,r.display_label,r.revision
    FROM dante.person_referent_catalog AS r
   WHERE r.self_person_ref=requested_self_person_ref
   ORDER BY r.display_label,r.person_ref;
$function$
"""

_RENAME = r"""
CREATE FUNCTION dante.rename_self_person_referent(
  requested_self_person_ref uuid,
  requested_operation_id text,
  requested_fingerprint text,
  requested_person_ref uuid,
  requested_expected_revision bigint,
  requested_display_label text
) RETURNS TABLE(person_ref uuid, display_label text, revision bigint, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
DECLARE
  op_id text := btrim(requested_operation_id);
  label text := btrim(requested_display_label);
  receipt record;
  current_label text;
  current_revision bigint;
  accepted_at timestamptz := statement_timestamp();
BEGIN
  IF op_id IS NULL OR op_id = '' OR char_length(op_id) > 200
     OR requested_fingerprint IS NULL
     OR requested_fingerprint !~ '^[0-9a-f]{64}$'
     OR label IS NULL OR label = '' OR char_length(label) > 100
     OR requested_expected_revision IS NULL OR requested_expected_revision < 1 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='person_referent_invalid_input', MESSAGE='Invalid Person referent request';
  END IF;
  PERFORM pg_advisory_xact_lock(
    hashtextextended(requested_self_person_ref::text || '|person-referent|' || op_id,0)
  );
  SELECT o.intent_fingerprint,o.person_ref,o.display_label,o.resulting_revision,
         o.operation_kind INTO receipt
    FROM dante.person_referent_operation AS o
   WHERE o.self_person_ref=requested_self_person_ref AND o.operation_id=op_id;
  IF FOUND THEN
    IF receipt.intent_fingerprint <> requested_fingerprint
       OR receipt.operation_kind <> 'rename'
       OR receipt.person_ref <> requested_person_ref
       OR receipt.resulting_revision <> requested_expected_revision+1
       OR receipt.display_label <> label THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        CONSTRAINT='person_referent_operation_reused',
        MESSAGE='Person referent operation id reused';
    END IF;
    RETURN QUERY SELECT receipt.person_ref,receipt.display_label,
                        receipt.resulting_revision,true;
    RETURN;
  END IF;
  SELECT c.display_label,c.revision INTO current_label,current_revision
    FROM dante.person_referent_catalog AS c
   WHERE c.self_person_ref=requested_self_person_ref
     AND c.person_ref=requested_person_ref FOR UPDATE;
  IF NOT FOUND THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='person_referent_unavailable', MESSAGE='Person referent unavailable';
  END IF;
  IF current_revision <> requested_expected_revision THEN
    RAISE EXCEPTION USING ERRCODE='40001',
      CONSTRAINT='person_referent_revision_conflict', MESSAGE='Person referent changed';
  END IF;
  IF current_label = label THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='person_referent_no_change', MESSAGE='Display label unchanged';
  END IF;
  UPDATE dante.person_referent_catalog AS c
     SET display_label=label,revision=c.revision+1,updated_at=accepted_at
   WHERE c.self_person_ref=requested_self_person_ref
     AND c.person_ref=requested_person_ref;
  INSERT INTO dante.person_referent_operation(
    self_person_ref,operation_id,intent_fingerprint,operation_kind,
    person_ref,display_label,resulting_revision,accepted_at
  ) VALUES(requested_self_person_ref,op_id,requested_fingerprint,'rename',
           requested_person_ref,label,current_revision+1,accepted_at);
  RETURN QUERY SELECT requested_person_ref,label,current_revision+1,false;
END;
$function$
"""

_ADMISSIBLE = r"""
CREATE OR REPLACE FUNCTION dante._self_referenceable_person(
  requested_self_person_ref uuid,requested_person_ref uuid
) RETURNS boolean
LANGUAGE sql STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT requested_person_ref IS NOT NULL
    AND (requested_person_ref=requested_self_person_ref
         OR EXISTS(
           SELECT 1 FROM dante.person_referent_catalog AS c
            WHERE c.self_person_ref=requested_self_person_ref
              AND c.person_ref=requested_person_ref
         ))
    AND EXISTS(SELECT 1 FROM dante.person AS p
                WHERE p.person_ref=requested_person_ref);
$function$
"""


def upgrade() -> None:
    op.create_table(
        "person_referent_catalog",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("person_ref", sa.Uuid(), nullable=False),
        sa.Column("display_label", sa.Text(), nullable=False),
        sa.Column("revision", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("self_person_ref","person_ref",name=op.f("pk_person_referent_catalog")),
        sa.ForeignKeyConstraint(["self_person_ref"],["dante.person.person_ref"],
                                name=op.f("fk_person_referent_catalog_self_person")),
        sa.ForeignKeyConstraint(["person_ref"],["dante.person.person_ref"],
                                name=op.f("fk_person_referent_catalog_person")),
        sa.CheckConstraint("btrim(display_label)<>'' AND char_length(display_label)<=100",
                           name=op.f("ck_person_referent_catalog_label")),
        sa.CheckConstraint("revision>=1",name=op.f("ck_person_referent_catalog_revision")),
        schema="dante",
    )
    op.create_table(
        "person_referent_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("operation_kind", sa.Text(), nullable=False),
        sa.Column("person_ref", sa.Uuid(), nullable=False),
        sa.Column("display_label", sa.Text(), nullable=False),
        sa.Column("resulting_revision", sa.BigInteger(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("self_person_ref","operation_id",name=op.f("pk_person_referent_operation")),
        sa.ForeignKeyConstraint(["self_person_ref","person_ref"],
                                ["dante.person_referent_catalog.self_person_ref",
                                 "dante.person_referent_catalog.person_ref"],
                                name=op.f("fk_person_referent_operation_catalog")),
        sa.CheckConstraint("operation_id=btrim(operation_id) AND operation_id<>'' "
                           "AND char_length(operation_id)<=200",
                           name=op.f("ck_person_referent_operation_id")),
        sa.CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'",
                           name=op.f("ck_person_referent_operation_fingerprint")),
        sa.CheckConstraint("operation_kind IN ('create','rename')",
                           name=op.f("ck_person_referent_operation_kind")),
        sa.CheckConstraint("btrim(display_label)<>'' AND char_length(display_label)<=100",
                           name=op.f("ck_person_referent_operation_label")),
        sa.CheckConstraint("resulting_revision>=1",
                           name=op.f("ck_person_referent_operation_revision")),
        schema="dante",
    )
    _sql(_CREATE)
    _sql(_LIST)
    _sql(_RENAME)
    _sql(_ADMISSIBLE)
    for signature in (
        "create_self_person_referent(uuid,text,text,uuid,text)",
        "list_self_person_referents(uuid)",
        "rename_self_person_referent(uuid,text,text,uuid,bigint,text)",
    ):
        _sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
        _sql(f"REVOKE ALL ON FUNCTION dante.{signature} FROM PUBLIC,dante_runtime,dante_migrator")
        _sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")
    _sql("ALTER FUNCTION dante._self_referenceable_person(uuid,uuid) OWNER TO dante_owner")
    _sql("REVOKE ALL ON FUNCTION dante._self_referenceable_person(uuid,uuid) "
         "FROM PUBLIC,dante_runtime,dante_migrator")
    for table in ("person_referent_catalog","person_referent_operation"):
        _sql(f"REVOKE ALL ON TABLE dante.{table} FROM PUBLIC,dante_runtime,dante_migrator")


def downgrade() -> None:
    _sql("""DO $block$ BEGIN
      IF EXISTS(SELECT 1 FROM dante.person_referent_catalog)
        OR EXISTS(SELECT 1 FROM dante.person_referent_operation) THEN
        RAISE EXCEPTION USING ERRCODE='55000',MESSAGE='B09-C downgrade refused';
      END IF;
    END $block$""")
    _sql("""CREATE OR REPLACE FUNCTION dante._self_referenceable_person(
      requested_self_person_ref uuid,requested_person_ref uuid) RETURNS boolean
      LANGUAGE sql STABLE PARALLEL SAFE
      SET search_path=pg_catalog,dante,pg_temp AS $function$
      SELECT requested_person_ref IS NOT NULL
        AND requested_person_ref=requested_self_person_ref
        AND EXISTS(SELECT 1 FROM dante.person
                    WHERE person_ref=requested_self_person_ref);
      $function$""")
    _sql("DROP FUNCTION dante.rename_self_person_referent(uuid,text,text,uuid,bigint,text)")
    _sql("DROP FUNCTION dante.list_self_person_referents(uuid)")
    _sql("DROP FUNCTION dante.create_self_person_referent(uuid,text,text,uuid,text)")
    op.drop_table("person_referent_operation",schema="dante")
    op.drop_table("person_referent_catalog",schema="dante")
