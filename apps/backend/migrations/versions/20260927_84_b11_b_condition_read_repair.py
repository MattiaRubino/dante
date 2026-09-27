"""B11-B: repair the conditional-intent read function.

Revision ID: 20260927_84
Revises: 20260927_83

Revisions 82 and 83 are published and immutable. Replace the B11-B read
function with the same bounded contract expressed as qualified PL/pgSQL and
re-assert its owner/execute boundary.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260927_84"
down_revision: str | None = "20260927_83"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def upgrade() -> None:
    _sql(
        r"""
CREATE OR REPLACE FUNCTION dante.get_self_actual_realization_condition(
  requested_self_person_ref uuid,
  requested_condition_ref uuid
) RETURNS TABLE(
  condition_ref uuid,
  subject_family text,
  subject_native_ref uuid,
  family_code text,
  created_at timestamptz
)
LANGUAGE plpgsql
SECURITY DEFINER
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
BEGIN
  RETURN QUERY
  SELECT intent.condition_ref,
         intent.subject_family,
         intent.subject_native_ref,
         intent.family_code,
         intent.created_at
    FROM dante.conditional_temporal_intent AS intent
   WHERE intent.condition_ref=requested_condition_ref
     AND intent.self_person_ref=requested_self_person_ref
     AND intent.family_code='actual_realization';
END;
$function$
"""
    )

    signature = "dante.get_self_actual_realization_condition(uuid,uuid)"
    _sql(f"ALTER FUNCTION {signature} OWNER TO {_OWNER}")
    _sql(f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,{_MIGRATOR}")
    _sql(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}")


def downgrade() -> None:
    raise RuntimeError("B11-B read repair is forward-only.")
