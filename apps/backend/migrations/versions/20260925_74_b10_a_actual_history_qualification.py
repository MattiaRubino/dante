"""B10-A: qualify Actual current-history correction and reconcile FK name.

Revision ID: 20260925_74
Revises: 20260925_73

The canonical family-aware Actual writer introduced by `_73` still contained
one unqualified `actual_ref` reference while its RETURNS TABLE contract exposes
an output column with the same name. PostgreSQL therefore rejected correction
writes with `42702` / AmbiguousColumn. This forward repair qualifies that one
current-history predicate without changing the capability contract.

The B10-A operation receipt FK name declared in `_70` also exceeded the
PostgreSQL identifier budget and was compiler-shortened. Rename it to a stable,
explicit <=63-character identifier so Dictionary, SQLAlchemy and live catalog
can agree exactly.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260925_74"
down_revision: str | None = "20260925_73"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


_WRITE_SIGNATURE = (
    "dante.record_self_actual_realization("
    "uuid,text,text,text,uuid,uuid,uuid,uuid,boolean,text,"
    "timestamptz,timestamptz,uuid[],uuid[])"
)
_OLD_RECEIPT_SUBJECT_FK = (
    "fk_actual_realization_operation_subject_native_ref_nati_9ab6"
)
_NEW_RECEIPT_SUBJECT_FK = (
    "fk_actual_realization_operation_subject_native_ref_native"
)


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def upgrade() -> None:
    # `_73` is the sole predecessor, so patch its exact function definition and
    # fail closed if that expected source is not present.
    _sql(
        rf"""
DO $repair$
DECLARE
  function_definition text;
  old_fragment constant text := 'WHERE actual_ref=resolved_actual_ref';
  new_fragment constant text :=
    'WHERE actual_realization_current_history.actual_ref=resolved_actual_ref';
BEGIN
  SELECT pg_get_functiondef('{_WRITE_SIGNATURE}'::regprocedure)
    INTO function_definition;

  IF function_definition IS NULL
     OR strpos(function_definition, old_fragment)=0 THEN
    RAISE EXCEPTION
      'B10-A Actual writer source no longer matches the expected _73 definition';
  END IF;

  function_definition := replace(
    function_definition,
    old_fragment,
    new_fragment
  );

  IF strpos(function_definition, old_fragment)<>0 THEN
    RAISE EXCEPTION
      'B10-A Actual writer ambiguity repair did not eliminate the source fragment';
  END IF;

  EXECUTE function_definition;
END;
$repair$;
"""
    )

    _sql(f"ALTER FUNCTION {_WRITE_SIGNATURE} OWNER TO dante_owner")
    _sql(
        f"REVOKE ALL ON FUNCTION {_WRITE_SIGNATURE} "
        "FROM PUBLIC, dante_runtime, dante_migrator"
    )
    _sql(f"GRANT EXECUTE ON FUNCTION {_WRITE_SIGNATURE} TO dante_runtime")

    _sql(
        "ALTER TABLE dante.actual_realization_operation "
        f"RENAME CONSTRAINT {_OLD_RECEIPT_SUBJECT_FK} "
        f"TO {_NEW_RECEIPT_SUBJECT_FK}"
    )


def downgrade() -> None:
    raise RuntimeError(
        "B10-A Actual history qualification repair downgrade is intentionally refused; "
        "use a separately reviewed forward migration"
    )
