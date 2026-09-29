"""B13-C: immutable Plan Step execution intent in the existing Plan revision."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260929_91"
down_revision: str | None = "20260928_90"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _replace_function(name: str, args: str, transform: object) -> None:
    bind = op.get_bind()
    definition = bind.exec_driver_sql(
        "SELECT pg_get_functiondef(p.oid) FROM pg_proc AS p "
        "JOIN pg_namespace AS n ON n.oid=p.pronamespace "
        "WHERE n.nspname='dante' AND p.proname=%s "
        "AND oidvectortypes(p.proargtypes)=%s", (name, args)
    ).scalar_one()
    updated = transform(definition)
    if updated == definition:
        raise RuntimeError(f"B13-C {name} patch point unavailable")
    bind.exec_driver_sql(updated.replace("%", "%%"))


def _one(source: str, old: str, new: str) -> str:
    if source.count(old) != 1:
        raise RuntimeError(f"B13-C expected one patch point: {old[:60]}")
    return source.replace(old, new)


def _json(source: str) -> str:
    return _one(
        source, "'title',item.title,'activity_ref',item.activity_ref",
        "'title',item.title,'activity_ref',item.activity_ref,"
        "'divisible',item.divisible,'max_planned_slices',item.max_planned_slices,"
        "'merge_compatible',item.merge_compatible,"
        "'execution_strength_code',item.execution_strength_code",
    )


def _replace_work(source: str) -> str:
    source = _one(
        source, "'title',snapshot.title,'activity_ref',snapshot.activity_ref",
        "'title',snapshot.title,'activity_ref',snapshot.activity_ref,"
        "'divisible',snapshot.divisible,"
        "'max_planned_slices',snapshot.max_planned_slices,"
        "'merge_compatible',snapshot.merge_compatible,"
        "'execution_strength_code',snapshot.execution_strength_code",
    )
    source = _one(source, "  item_title text;", "  item_title text;\n"
                  "  item_divisible boolean;\n  item_max integer;\n"
                  "  item_merge boolean;\n  item_strength text;")
    source = _one(
        source,
        "OR (item - 'step_ref' - 'title' - 'activity_ref')<>'{}'::jsonb",
        "OR (item ? 'divisible' AND jsonb_typeof(item->'divisible') NOT IN ('boolean','null'))\n"
        "       OR (item ? 'max_planned_slices' AND jsonb_typeof(item->'max_planned_slices') "
        "NOT IN ('number','null'))\n"
        "       OR (item ? 'merge_compatible' AND jsonb_typeof(item->'merge_compatible') "
        "NOT IN ('boolean','null'))\n"
        "       OR (item ? 'execution_strength_code' AND "
        "jsonb_typeof(item->'execution_strength_code') NOT IN ('string','null'))\n"
        "       OR (item - 'step_ref' - 'title' - 'activity_ref' - 'divisible' "
        "- 'max_planned_slices' - 'merge_compatible' "
        "- 'execution_strength_code')<>'{}'::jsonb",
    )
    source = _one(
        source, "    item_title:=btrim(item->>'title');",
        "    item_title:=btrim(item->>'title');\n"
        "    item_divisible:=(item->>'divisible')::boolean;\n"
        "    item_merge:=(item->>'merge_compatible')::boolean;\n"
        "    item_strength:=item->>'execution_strength_code';\n"
        "    BEGIN\n      item_max:=(item->>'max_planned_slices')::integer;\n"
        "    EXCEPTION WHEN invalid_text_representation OR numeric_value_out_of_range THEN\n"
        "      RAISE EXCEPTION USING ERRCODE='23514',MESSAGE='Plan execution limit rejected';\n"
        "    END;\n"
        "    IF NOT COALESCE(((item_divisible IS NULL AND item_merge IS NULL\n"
        "             AND item_max IS NULL AND item_strength IS NULL) OR\n"
        "            (item_activity IS NOT NULL AND item_divisible IS NOT NULL\n"
        "             AND item_merge IS NOT NULL\n"
        "             AND item_strength IN ('hard','soft')\n"
        "             AND (item_max IS NULL OR item_max BETWEEN 1 AND 100)\n"
        "             AND ((item_divisible AND (item_max IS NULL OR item_max>=2))\n"
        "                  OR (NOT item_divisible AND item_max=1 AND NOT item_merge)))),false) THEN\n"
        "      RAISE EXCEPTION USING ERRCODE='23514',MESSAGE='Plan execution policy rejected';\n"
        "    END IF;",
    )
    return _one(
        source,
        "state_ref,plan_ref,step_ref,position,title,activity_ref\n    ) VALUES (\n"
        "      requested_state_ref,requested_plan_ref,item_ref,item_position,item_title,item_activity",
        "state_ref,plan_ref,step_ref,position,title,activity_ref,\n"
        "      divisible,max_planned_slices,merge_compatible,execution_strength_code\n"
        "    ) VALUES (\n"
        "      requested_state_ref,requested_plan_ref,item_ref,item_position,item_title,item_activity,\n"
        "      item_divisible,item_max,item_merge,item_strength",
    )


def upgrade() -> None:
    for column in (
        sa.Column("divisible", sa.Boolean(), nullable=True),
        sa.Column("max_planned_slices", sa.Integer(), nullable=True),
        sa.Column("merge_compatible", sa.Boolean(), nullable=True),
        sa.Column("execution_strength_code", sa.Text(), nullable=True),
    ):
        op.add_column("plan_step_in_state", column, schema="dante")
    op.create_check_constraint(
        "ck_plan_step_in_state_execution_policy", "plan_step_in_state",
        "COALESCE(((divisible IS NULL AND max_planned_slices IS NULL AND merge_compatible IS NULL "
        "AND execution_strength_code IS NULL) OR "
        "(activity_ref IS NOT NULL AND divisible IS NOT NULL AND merge_compatible IS NOT NULL "
        "AND execution_strength_code IN ('hard','soft') "
        "AND (max_planned_slices IS NULL OR max_planned_slices BETWEEN 1 AND 100) "
        "AND ((divisible AND (max_planned_slices IS NULL OR max_planned_slices>=2)) "
        "OR (NOT divisible AND max_planned_slices=1 AND NOT merge_compatible)))),false)",
        schema="dante",
    )
    _replace_function("get_self_plan_work", "uuid, uuid", _json)
    _replace_function("replace_self_plan_work", "uuid, text, text, uuid, uuid, uuid, text, jsonb", _replace_work)


def downgrade() -> None:
    raise RuntimeError("B13-C execution policy is forward-only.")
