"""B14-M1: append-only accepted occurrence profile edits (single or following).

Read-only B06 authority remains unchanged. A selected occurrence is always in
scope. The other past occurrences are never rewritten. A following edit also
applies to future occurrences generated after acceptance via a dated policy.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261008_123"
down_revision: str | None = "20261008_122"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

def upgrade() -> None:
    op.create_table(
        "occurrence_profile_edit",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("source_native_ref", sa.Uuid(), nullable=False),
        sa.Column("selected_occurrence_ref", sa.Uuid(), nullable=False),
        sa.Column("revision", sa.BigInteger(), nullable=False),
        sa.Column("expected_revision", sa.BigInteger(), nullable=False),
        sa.Column("expected_recurrence_state_ref", sa.Uuid()),
        sa.Column("scope_code", sa.Text(), nullable=False),
        sa.Column("effective_zone_id", sa.Text(), nullable=False),
        sa.Column("anchor_at", sa.DateTime(timezone=True)),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("profile_patch", JSONB(), nullable=False),
        sa.PrimaryKeyConstraint("self_person_ref","operation_id",
                                name="pk_occurrence_profile_edit"),
        sa.UniqueConstraint("source_native_ref","revision",
                            name="uq_occurrence_profile_edit_source_revision"),
        sa.ForeignKeyConstraint(["self_person_ref"],["dante.person.person_ref"],
                                name="fk_occurrence_profile_edit_person"),
        sa.ForeignKeyConstraint(["source_native_ref"],["dante.native_address.native_ref"],
                                name="fk_occurrence_profile_edit_source"),
        sa.ForeignKeyConstraint(["selected_occurrence_ref"],["dante.occurrence.occurrence_ref"],
                                name="fk_occurrence_profile_edit_occurrence"),
        sa.CheckConstraint("revision>=1 AND expected_revision>=0",
                           name="ck_occurrence_profile_edit_revision"),
        sa.CheckConstraint("operation_id=btrim(operation_id) AND operation_id<>'' "
                           "AND char_length(operation_id)<=200",
                           name="ck_occurrence_profile_edit_operation"),
        sa.CheckConstraint("scope_code IN ('only_this','this_and_following')",
                           name="ck_occurrence_profile_edit_scope"),
        sa.CheckConstraint("jsonb_typeof(profile_patch)='object' AND "
                           "profile_patch<>'{}'::jsonb",
                           name="ck_occurrence_profile_edit_patch"),
        schema="dante"
    )
    db=op.get_bind()
    db.exec_driver_sql("ALTER TABLE dante.occurrence_profile_edit OWNER TO dante_owner")
    db.exec_driver_sql("REVOKE ALL ON dante.occurrence_profile_edit "
                       "FROM PUBLIC,dante_runtime,dante_migrator")
    for ddl in (_COORDINATE_INSTANT,_PROFILE_PATCH,_ACCEPT_EDIT):
        db.execute(sa.text(ddl))
    for signature in (
        "occurrence_edit_coordinate_instant(uuid,uuid,text)",
        "get_self_occurrence_profile_patch(uuid,uuid)",
        "accept_self_occurrence_profile_edit(uuid,uuid,text,bigint,uuid,text,text,jsonb)",
    ):
        db.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
        db.exec_driver_sql(f"REVOKE ALL ON FUNCTION dante.{signature} "
                           "FROM PUBLIC,dante_runtime,dante_migrator")
        db.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")

def downgrade() -> None:
    raise RuntimeError("Accepted occurrence edit history is forward-only")


_COORDINATE_INSTANT = r"""
CREATE FUNCTION dante.occurrence_edit_coordinate_instant(
    actor uuid, requested_occurrence uuid, effective_zone text
) RETURNS timestamptz
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $$
#variable_conflict error
DECLARE coord record; civil timestamp; resolved timestamptz; zone text;
BEGIN
    IF effective_zone IS NULL OR effective_zone<>btrim(effective_zone)
       OR effective_zone='' OR char_length(effective_zone)>200
       OR NOT EXISTS(SELECT 1 FROM pg_catalog.pg_timezone_names z
                     WHERE z.name=effective_zone) THEN
        RAISE EXCEPTION USING ERRCODE='22023',
            CONSTRAINT='occurrence_edit_invalid_zone',
            MESSAGE='Invalid effective timezone';
    END IF;
    SELECT * INTO coord FROM dante.get_self_occurrence(actor,requested_occurrence);
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='occurrence_edit_unavailable',
            MESSAGE='Occurrence outside self scope';
    END IF;
    IF coord.origin_code='explicit_extra' THEN RETURN NULL; END IF;
    IF coord.resolved_at IS NOT NULL THEN RETURN coord.resolved_at; END IF;
    IF coord.expected_at IS NOT NULL THEN RETURN coord.expected_at; END IF;
    IF coord.clock_basis_code='named_zone' THEN
        RAISE EXCEPTION USING ERRCODE='22023',
            CONSTRAINT='occurrence_edit_unresolved_zone',
            MESSAGE='Unresolved named-zone coordinate';
    END IF;
    IF coord.generated_date IS NOT NULL THEN
        civil:=coord.generated_date+COALESCE(coord.generated_wall_time,'00:00'::time);
        zone:=CASE WHEN coord.clock_basis_code='absolute_utc' THEN 'UTC'
                   ELSE effective_zone END;
    ELSIF coord.period_start_date IS NOT NULL THEN
        civil:=coord.period_start_date::timestamp; zone:=effective_zone;
    ELSE
        RAISE EXCEPTION USING ERRCODE='22023',
            CONSTRAINT='occurrence_edit_unordered_coordinate',
            MESSAGE='Unordered Occurrence coordinate';
    END IF;
    resolved:=civil AT TIME ZONE zone;
    IF (resolved AT TIME ZONE zone) IS DISTINCT FROM civil THEN
        RAISE EXCEPTION USING ERRCODE='22023',
            CONSTRAINT='occurrence_edit_dst_gap',
            MESSAGE='Invalid local DST time';
    END IF;
    RETURN resolved;
END;
$$;
"""
