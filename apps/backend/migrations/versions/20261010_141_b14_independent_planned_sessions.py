"""B14: independently executable planned Sessions without enabling main Activity clock.

No new Session hierarchy table. Clone the existing B08 guarded Start capability
for trusted owner-only planned provenance and keep the original generic Start
capture-policy guard intact. _118 validates planned owner identity before call.
"""
from collections.abc import Sequence

from alembic import op

revision: str = "20261010_141"
down_revision: str | None = "20261010_140"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    for sql in (_PLANNED_START, _PLANNED_WRAPPER, _OPTIONAL_MAIN, _PANEL_OWNER):
        bind.exec_driver_sql(sql)
    signature = "dante.start_self_session_for_planned(uuid,text,text,uuid,uuid,text,uuid)"
    bind.exec_driver_sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
    # Crucially, the cloned primitive is NOT executable by the runtime or
    # PUBLIC. Only the existing owner-guarded planned wrapper may invoke it.
    bind.exec_driver_sql(
        f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator"
    )


def downgrade() -> None:
    raise RuntimeError("Owner-only planned Session provenance is forward-only")


_PLANNED_START = r"""
DO $migration$
DECLARE definition text;
BEGIN
  SELECT pg_get_functiondef(
    'dante.start_self_session(uuid,text,text,uuid,uuid,text,uuid)'::regprocedure
  ) INTO definition;
  IF definition IS NULL
     OR strpos(definition, 'start_self_session(')=0
     OR strpos(definition, 'IF requested_subject_family=''activity'' THEN')=0
     OR strpos(definition, 'session_execution_policy_live_required')=0 THEN
    RAISE EXCEPTION 'Unexpected B08 main Session Start contract';
  END IF;
  definition := replace(definition,'start_self_session(','start_self_session_for_planned(');
  definition := replace(
    definition, 'IF requested_subject_family=''activity'' THEN',
    'IF FALSE AND requested_subject_family=''activity'' THEN'
  );
  EXECUTE definition;
END;
$migration$;
"""


_PLANNED_WRAPPER = r"""
DO $migration$
DECLARE definition text;
BEGIN
  SELECT pg_get_functiondef(
    'dante.start_self_planned_activity_session(uuid,text,text,uuid,uuid,uuid,uuid)'::regprocedure
  ) INTO definition;
  IF definition IS NULL OR
     strpos(definition,'dante.start_self_session(')=0 THEN
    RAISE EXCEPTION 'Unexpected linked planned Session start contract';
  END IF;
  definition := replace(definition,'dante.start_self_session(',
    'dante.start_self_session_for_planned(');
  EXECUTE definition;
END;
$migration$;
"""


_OPTIONAL_MAIN = r"""
DO $migration$
DECLARE definition text;
        anchor text := '    IF NOT result.replayed AND NOT EXISTS (';
BEGIN
  SELECT pg_get_functiondef(
    'dante.start_self_planned_activity_session(uuid,text,text,uuid,uuid,uuid,uuid)'::regprocedure
  ) INTO definition;
  IF strpos(definition,anchor)=0 THEN
    RAISE EXCEPTION 'Unexpected planned Session hierarchy contract';
  END IF;
  definition := replace(definition,anchor,'
    IF NOT result.replayed AND EXISTS (
      SELECT 1 FROM dante.get_self_activity_execution_policy(
        requested_self_person_ref,requested_activity_ref
      ) policy WHERE policy.mode_code IN (''live'',''record_and_live'')
    ) AND NOT EXISTS (');
  EXECUTE definition;
END;
$migration$;
"""


_PANEL_OWNER = r"""
DO $migration$
DECLARE definition text;
        owner_source text :=
          'SELECT a.activity_ref,policy.mode_code FROM owned_activities a';
        owner_replacement text :=
          'SELECT a.activity_ref,CASE WHEN policy.mode_code IN (''disabled'',''record'') ' ||
          'THEN ''internal_only'' ELSE policy.mode_code END AS mode_code ' ||
          'FROM owned_activities a';
        predicate text :=
          'WHERE policy.mode_code IN (''live'',''record_and_live'')';
        replacement text :=
          'WHERE (policy.mode_code IN (''live'',''record_and_live'') ' ||
          'OR EXISTS (SELECT 1 FROM dante.activity_schedule_role planned ' ||
          'WHERE planned.activity_ref=a.activity_ref AND planned.role_code=''planned'' ' ||
          'AND planned.retired_at IS NULL))';
BEGIN
  SELECT pg_get_functiondef(
    'dante.list_self_session_panel_inputs(uuid)'::regprocedure
  ) INTO definition;
  IF strpos(definition,owner_source)=0 OR strpos(definition,predicate)=0 THEN
    RAISE EXCEPTION 'Unexpected B14 Session desk owner contract';
  END IF;
  definition := replace(definition,owner_source,owner_replacement);
  definition := replace(definition,predicate,replacement);
  EXECUTE definition;
END;
$migration$;
"""