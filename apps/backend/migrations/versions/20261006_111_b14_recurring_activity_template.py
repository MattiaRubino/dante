"""B14 complete recurring Activity template inheritance."""
from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op

revision: str = "20261006_111"
down_revision: str | None = "20261006_110"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

def upgrade() -> None:
    op.add_column("routine_occurrence_policy", sa.Column(
        "activity_template", sa.dialects.postgresql.JSONB(), nullable=False,
        server_default=sa.text("'{}'::jsonb")), schema="dante")
    op.create_check_constraint(
        "ck_routine_occurrence_policy_activity_template",
        "routine_occurrence_policy", "jsonb_typeof(activity_template)='object'",
        schema="dante")
    op.create_table(
        "routine_occurrence_activity_instance",
        sa.Column("occurrence_ref", sa.Uuid(), nullable=False),
        sa.Column("activity_ref", sa.Uuid(), nullable=False),
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("occurrence_ref", name="pk_routine_occurrence_activity_instance"),
        sa.UniqueConstraint("activity_ref", name="uq_routine_occurrence_activity_instance_activity"),
        sa.ForeignKeyConstraint(["occurrence_ref"], ["dante.occurrence.occurrence_ref"],
                                name="fk_routine_occurrence_activity_instance_occurrence"),
        sa.ForeignKeyConstraint(["activity_ref"], ["dante.activity_intention.activity_ref"],
                                name="fk_routine_occurrence_activity_instance_activity"),
        sa.ForeignKeyConstraint(["self_person_ref"], ["dante.person.person_ref"],
                                name="fk_routine_occurrence_activity_instance_person"),
        schema="dante")
    bind = op.get_bind()
    bind.exec_driver_sql("DROP FUNCTION dante.get_self_routine_occurrence_policy(uuid,uuid)")
    bind.exec_driver_sql(GET_POLICY)
    bind.exec_driver_sql(SET_POLICY)
    bind.exec_driver_sql(BIND_INSTANCE)
    bind.exec_driver_sql(LIST_INSTANCES)
    bind.exec_driver_sql("REVOKE ALL ON dante.routine_occurrence_activity_instance FROM PUBLIC,dante_runtime,dante_migrator")
    for signature in (
        "get_self_routine_occurrence_policy(uuid,uuid)",
        "set_self_routine_occurrence_policy(uuid,uuid,integer,integer,jsonb)",
        "bind_self_routine_occurrence_activity(uuid,uuid,uuid)",
        "list_self_routine_occurrence_activities(uuid,uuid[])"):
        bind.exec_driver_sql(f"REVOKE ALL ON FUNCTION dante.{signature} FROM PUBLIC,dante_runtime,dante_migrator")
        bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")

def downgrade() -> None:
    raise RuntimeError("20261006_111 is forward-only")

GET_POLICY = r"""
CREATE FUNCTION dante.get_self_routine_occurrence_policy(uuid,uuid)
RETURNS TABLE(duration_minutes integer,reminder_lead_minutes integer,
              activity_template jsonb,created_at timestamptz)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $$
SELECT p.duration_minutes,p.reminder_lead_minutes,p.activity_template,p.created_at
FROM dante.routine_occurrence_policy p
JOIN dante.routine_intention r ON r.routine_ref=p.routine_ref
WHERE p.self_person_ref=$1 AND p.routine_ref=$2 AND r.self_person_ref=$1
$$;
"""

SET_POLICY = r"""
CREATE FUNCTION dante.set_self_routine_occurrence_policy(uuid,uuid,integer,integer,jsonb)
RETURNS TABLE(duration_minutes integer,reminder_lead_minutes integer,
              activity_template jsonb,created_at timestamptz,replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $$
DECLARE prior dante.routine_occurrence_policy%ROWTYPE;
        template jsonb:=COALESCE($5,'{}'::jsonb);
        ts timestamptz:=statement_timestamp();
BEGIN
 IF $3 IS NULL OR $3 NOT BETWEEN 1 AND 525600
    OR ($4 IS NOT NULL AND $4 NOT BETWEEN 0 AND 10080)
    OR jsonb_typeof(template)<>'object'
    OR (template<>'{}'::jsonb AND template->>'version'<>'1') THEN
   RAISE EXCEPTION USING ERRCODE='23514',CONSTRAINT='routine_occurrence_policy_invalid';
 END IF;
 IF NOT EXISTS(SELECT 1 FROM dante.routine_intention r
               WHERE r.routine_ref=$2 AND r.self_person_ref=$1) THEN
   RAISE EXCEPTION USING ERRCODE='23503',CONSTRAINT='routine_occurrence_policy_routine_unavailable';
 END IF;
 SELECT * INTO prior FROM dante.routine_occurrence_policy p
  WHERE p.self_person_ref=$1 AND p.routine_ref=$2 FOR UPDATE;
 IF FOUND THEN
   IF prior.duration_minutes<>$3 OR prior.reminder_lead_minutes IS DISTINCT FROM $4
      OR prior.activity_template IS DISTINCT FROM template THEN
     RAISE EXCEPTION USING ERRCODE='23505',CONSTRAINT='pk_routine_occurrence_policy';
   END IF;
   RETURN QUERY SELECT prior.duration_minutes,prior.reminder_lead_minutes,
                       prior.activity_template,prior.created_at,true; RETURN;
 END IF;
 INSERT INTO dante.routine_occurrence_policy(
   self_person_ref,routine_ref,duration_minutes,reminder_lead_minutes,activity_template,created_at)
 VALUES($1,$2,$3,$4,template,ts);
 RETURN QUERY SELECT $3,$4,template,ts,false;
END $$;
"""

BIND_INSTANCE = r"""
CREATE FUNCTION dante.bind_self_routine_occurrence_activity(uuid,uuid,uuid)
RETURNS TABLE(occurrence_ref uuid,activity_ref uuid,created_at timestamptz,replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $$
DECLARE prior dante.routine_occurrence_activity_instance%ROWTYPE;
        ts timestamptz:=statement_timestamp();
BEGIN
 IF NOT EXISTS(
   SELECT 1 FROM dante.occurrence_generation g
   JOIN dante.routine_intention r ON r.routine_ref=g.source_native_ref
   WHERE g.occurrence_ref=$2 AND r.self_person_ref=$1)
 OR NOT EXISTS(
   SELECT 1 FROM dante.activity_intention a
   WHERE a.activity_ref=$3 AND a.self_person_ref=$1) THEN
   RAISE EXCEPTION USING ERRCODE='23503',CONSTRAINT='routine_occurrence_activity_instance_unavailable';
 END IF;
 SELECT * INTO prior FROM dante.routine_occurrence_activity_instance b
  WHERE b.occurrence_ref=$2 FOR UPDATE;
 IF FOUND THEN
   IF prior.activity_ref IS DISTINCT FROM $3 OR prior.self_person_ref IS DISTINCT FROM $1 THEN
     RAISE EXCEPTION USING ERRCODE='23505',CONSTRAINT='routine_occurrence_activity_instance_conflict';
   END IF;
   RETURN QUERY SELECT prior.occurrence_ref,prior.activity_ref,prior.created_at,true; RETURN;
 END IF;
 INSERT INTO dante.routine_occurrence_activity_instance(
   occurrence_ref,activity_ref,self_person_ref,created_at) VALUES($2,$3,$1,ts);
 RETURN QUERY SELECT $2,$3,ts,false;
END $$;
"""

LIST_INSTANCES = r"""
CREATE FUNCTION dante.list_self_routine_occurrence_activities(uuid,uuid[])
RETURNS TABLE(occurrence_ref uuid,activity_ref uuid,created_at timestamptz)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $$
SELECT b.occurrence_ref,b.activity_ref,b.created_at
FROM dante.routine_occurrence_activity_instance b
JOIN dante.activity_intention a ON a.activity_ref=b.activity_ref
WHERE b.self_person_ref=$1 AND a.self_person_ref=$1 AND b.occurrence_ref=ANY($2)
ORDER BY b.occurrence_ref
$$;
""
