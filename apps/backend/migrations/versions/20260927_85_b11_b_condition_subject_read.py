"""B11-B: read an existing actual-realization condition by its typed subject.

Revision ID: 20260927_85
Revises: 20260927_84

The B11-B Condition has stable canonical identity per self/subject/family.  The
browser needs a bounded read of that existing canonical intent after reload;
it must not create another Condition merely to recover its identity.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260927_85"
down_revision: str | None = "20260927_84"
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
CREATE FUNCTION dante.find_self_actual_realization_condition(
  requested_self_person_ref uuid,
  requested_subject_family text,
  requested_subject_native_ref uuid
) RETURNS TABLE(
  condition_ref uuid,
  subject_family text,
  subject_native_ref uuid,
  family_code text,
  created_at timestamptz
)
LANGUAGE sql
SECURITY DEFINER
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT intent.condition_ref,intent.subject_family,intent.subject_native_ref,
         intent.family_code,intent.created_at
    FROM dante.conditional_temporal_intent AS intent
   WHERE intent.self_person_ref=requested_self_person_ref
     AND intent.subject_family=requested_subject_family
     AND intent.subject_native_ref=requested_subject_native_ref
     AND intent.family_code='actual_realization';
$function$
"""
    )
    _sql(
        "ALTER FUNCTION dante.find_self_actual_realization_condition(uuid,text,uuid) "
        f"OWNER TO {_OWNER}"
    )
    _sql(
        "REVOKE ALL ON FUNCTION dante.find_self_actual_realization_condition(uuid,text,uuid) "
        f"FROM PUBLIC,{_MIGRATOR}"
    )
    _sql(
        "GRANT EXECUTE ON FUNCTION dante.find_self_actual_realization_condition(uuid,text,uuid) "
        f"TO {_RUNTIME}"
    )


def downgrade() -> None:
    raise RuntimeError("B11-B migration is forward-only.")
