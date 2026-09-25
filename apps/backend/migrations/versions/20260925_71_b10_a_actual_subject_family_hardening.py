"""B10-A: bind Actual authoring/read capability to the exact subject family.

Revision ID: 20260925_71
Revises: 20260925_70

Revision 70 activated the guarded Actual capability over the canonical CP6
substrate. This forward-only hardening makes the route family part of the
PostgreSQL authority boundary so an Activity NativeRef cannot be accepted
through the Event or Occurrence capability (and vice versa).
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260925_71"
down_revision: str | None = "20260925_70"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"


def _sql(statement: str) -> None:
    op.execute(sa.text(statement))


def upgrade() -> None:
    _sql(
        r"""
CREATE FUNCTION dante._actual_subject_owned_as(
  requested_self_person_ref uuid,
  requested_subject_family text,
  requested_subject_native_ref uuid
) RETURNS boolean
LANGUAGE sql
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT CASE requested_subject_family
    WHEN 'activity' THEN EXISTS (
      SELECT 1
        FROM dante.activity_intention AS activity
       WHERE activity.activity_ref=requested_subject_native_ref
         AND activity.self_person_ref=requested_self_person_ref
    )
    WHEN 'event' THEN EXISTS (
      SELECT 1
        FROM dante.event_expectation AS event
       WHERE event.event_ref=requested_subject_native_ref
         AND event.self_person_ref=requested_self_person_ref
    )
    WHEN 'occurrence' THEN EXISTS (
      SELECT 1
        FROM dante.occurrence_generation AS generation
       WHERE generation.occurrence_ref=requested_subject_native_ref
         AND (
           EXISTS (
             SELECT 1
               FROM dante.routine_intention AS routine
              WHERE routine.routine_ref=generation.source_native_ref
                AND routine.self_person_ref=requested_self_person_ref
           ) OR EXISTS (
             SELECT 1
               FROM dante.event_expectation AS source_event
              WHERE source_event.event_ref=generation.source_native_ref
                AND source_event.self_person_ref=requested_self_person_ref
           )
         )
    )
    ELSE false
  END;
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.record_self_actual_realization(
  requested_self_person_ref uuid,
  requested_subject_family text,
  requested_operation_id text,
  requested_intent_fingerprint text,
  requested_actual_ref uuid,
  requested_material_state_ref uuid,
  requested_subject_native_ref uuid,
  requested_expected_material_state_ref uuid,
  requested_realization_occurred boolean,
  requested_extent_code text,
  requested_started_at timestamptz,
  requested_ended_at timestamptz,
  requested_session_refs uuid[],
  requested_session_timing_material_state_refs uuid[]
) RETURNS TABLE(
  actual_ref uuid,
  subject_native_ref uuid,
  material_state_ref uuid,
  realization_occurred boolean,
  extent_code text,
  started_at timestamptz,
  ended_at timestamptz,
  replayed boolean
)
LANGUAGE plpgsql
SECURITY DEFINER
VOLATILE
PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
BEGIN
  IF requested_subject_family NOT IN ('activity','event','occurrence')
     OR NOT dante._actual_subject_owned_as(
       requested_self_person_ref,
       requested_subject_family,
       requested_subject_native_ref
     ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='actual_subject_family_unavailable',
      MESSAGE='Actual subject unavailable for requested family';
  END IF;

  RETURN QUERY
  SELECT result.actual_ref,
         result.subject_native_ref,
         result.material_state_ref,
         result.realization_occurred,
         result.extent_code,
         result.started_at,
         result.ended_at,
         result.replayed
    FROM dante.record_self_actual_realization(
      requested_self_person_ref,
      requested_operation_id,
      requested_intent_fingerprint,
      requested_actual_ref,
      requested_material_state_ref,
      requested_subject_native_ref,
      requested_expected_material_state_ref,
      requested_realization_occurred,
      requested_extent_code,
      requested_started_at,
      requested_ended_at,
      requested_session_refs,
      requested_session_timing_material_state_refs
    ) AS result;
END;
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.get_self_subject_actual(
  requested_self_person_ref uuid,
  requested_subject_family text,
  requested_subject_native_ref uuid
) RETURNS TABLE(
  actual_ref uuid,
  subject_native_ref uuid,
  material_state_ref uuid,
  realization_occurred boolean,
  extent_code text,
  started_at timestamptz,
  ended_at timestamptz
)
LANGUAGE plpgsql
SECURITY DEFINER
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
BEGIN
  IF requested_subject_family NOT IN ('activity','event','occurrence')
     OR NOT dante._actual_subject_owned_as(
       requested_self_person_ref,
       requested_subject_family,
       requested_subject_native_ref
     ) THEN
    RETURN;
  END IF;

  RETURN QUERY
  SELECT result.actual_ref,
         result.subject_native_ref,
         result.material_state_ref,
         result.realization_occurred,
         result.extent_code,
         result.started_at,
         result.ended_at
    FROM dante.get_self_subject_actual(
      requested_self_person_ref,
      requested_subject_native_ref
    ) AS result;
END;
$function$
"""
    )

    old_write = (
        "dante.record_self_actual_realization(uuid,text,text,uuid,uuid,uuid,uuid,boolean,text,timestamptz,timestamptz,uuid[],uuid[])"
    )
    old_read = "dante.get_self_subject_actual(uuid,uuid)"
    new_write = (
        "dante.record_self_actual_realization(uuid,text,text,text,uuid,uuid,uuid,uuid,boolean,text,timestamptz,timestamptz,uuid[],uuid[])"
    )
    new_read = "dante.get_self_subject_actual(uuid,text,uuid)"
    helper = "dante._actual_subject_owned_as(uuid,text,uuid)"

    for signature in (helper, new_write, new_read):
        _sql(f"ALTER FUNCTION {signature} OWNER TO {_OWNER}")
        _sql(f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}")

    # The generic revision-70 functions remain internal implementation details;
    # runtime callers must prove the exact public subject family at PostgreSQL.
    _sql(f"REVOKE ALL ON FUNCTION {old_write} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}")
    _sql(f"REVOKE ALL ON FUNCTION {old_read} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}")
    _sql(f"GRANT EXECUTE ON FUNCTION {new_write} TO {_RUNTIME}")
    _sql(f"GRANT EXECUTE ON FUNCTION {new_read} TO {_RUNTIME}")


def downgrade() -> None:
    raise RuntimeError(
        "B10-A Actual subject-family hardening downgrade is intentionally refused; "
        "use a separately reviewed forward migration"
    )
