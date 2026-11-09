"""Reject inclusive series writes when the selected Occurrence is protected.

Revision ID: 20261109_183
Revises: 20261109_182

The existing preview and Python planner already enumerate protected future
instances. This database admission guard is the final authority for selected
instances with running/paused/finished Sessions, recorded Objectives, skipped
state or local edits. The `only_this` and `from_next` scopes remain legal.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261109_183"
down_revision: str | None = "20261109_182"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_GUARD = r"""
CREATE FUNCTION dante.enforce_selected_occurrence_series_protection()
RETURNS trigger
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
BEGIN
    IF NEW.scope_code='this_and_following'
       AND dante.get_self_occurrence_edit_protection(
           NEW.self_person_ref, NEW.selected_occurrence_ref
       ) IS NOT NULL THEN
        RAISE EXCEPTION
          'Selected protected Occurrence requires from-next scope'
          USING ERRCODE='23505',
                CONSTRAINT='occurrence_edit_selected_protected';
    END IF;
    RETURN NEW;
END;
$function$;
"""


def upgrade() -> None:
    bind = op.get_bind()
    bind.exec_driver_sql(_GUARD)
    bind.exec_driver_sql(
        "ALTER FUNCTION dante.enforce_selected_occurrence_series_protection() "
        "OWNER TO dante_owner"
    )
    bind.exec_driver_sql(
        "REVOKE ALL ON FUNCTION dante.enforce_selected_occurrence_series_protection() "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )
    bind.exec_driver_sql(
        "CREATE TRIGGER tr_occurrence_profile_edit_protected_selected "
        "BEFORE INSERT ON dante.occurrence_profile_edit "
        "FOR EACH ROW EXECUTE FUNCTION "
        "dante.enforce_selected_occurrence_series_protection()"
    )


def downgrade() -> None:
    raise RuntimeError("Selected Occurrence protection is forward-only")
