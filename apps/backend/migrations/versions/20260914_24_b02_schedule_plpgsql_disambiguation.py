"""Resolve B02 Schedule PL/pgSQL output-column ambiguity.

Revision ID: 20260914_24
Revises: 20260914_23
Create Date: 2026-09-14
"""

from __future__ import annotations

import re

import sqlalchemy as sa
from alembic import op

revision = "20260914_24"
down_revision = "20260914_23"
branch_labels = None
depends_on = None

_REVISE_SIGNATURE = (
    "dante.revise_self_floating_schedule("
    "uuid,text,text,uuid,uuid,uuid,timestamp without time zone,timestamp without time zone)"
)
_UNSCHEDULE_SIGNATURE = "dante.unschedule_self_schedule(uuid,text,text,uuid,uuid)"
_UNDO_SIGNATURE = "dante.undo_self_schedule_unschedule(uuid,text,text,uuid,text,uuid)"
_EXPECTED_REWRITES = {
    _REVISE_SIGNATURE: 1,
    _UNSCHEDULE_SIGNATURE: 1,
    _UNDO_SIGNATURE: 3,
}

_DIRECTIVE_RE = re.compile(
    r"(?m)^[ \t]*#variable_conflict (?:error|use_variable|use_column)[ \t]*\n"
)
_BODY_MARKER_RE = re.compile(r"(AS \$[^$]*\$\n)", re.MULTILINE)

_UPDATE_UNQUALIFIED_RE = re.compile(
    r"UPDATE\s+dante\.schedule_placement_current_history\s+"
    r"SET\s+current_until_at\s*=\s*recorded_at\s+"
    r"WHERE\s+schedule_ref\s*=\s*requested_schedule_ref\s+"
    r"AND\s+material_state_ref\s*=\s*current_material_state_ref\s+"
    r"AND\s+current_until_at\s+IS\s+NULL\s*;",
    re.IGNORECASE,
)
_UPDATE_QUALIFIED_RE = re.compile(
    r"UPDATE\s+dante\.schedule_placement_current_history\s+AS\s+history\s+"
    r"SET\s+current_until_at\s*=\s*recorded_at\s+"
    r"WHERE\s+history\.schedule_ref\s*=\s*requested_schedule_ref\s+"
    r"AND\s+history\.material_state_ref\s*=\s*current_material_state_ref\s+"
    r"AND\s+history\.current_until_at\s+IS\s+NULL\s*;",
    re.IGNORECASE,
)

_UNDO_OPEN_UNQUALIFIED_RE = re.compile(
    r"FROM\s+dante\.schedule_placement_current_history\s+"
    r"WHERE\s+schedule_ref\s*=\s*requested_schedule_ref\s+"
    r"AND\s+current_until_at\s+IS\s+NULL",
    re.IGNORECASE,
)
_UNDO_OPEN_QUALIFIED_RE = re.compile(
    r"FROM\s+dante\.schedule_placement_current_history\s+AS\s+history\s+"
    r"WHERE\s+history\.schedule_ref\s*=\s*requested_schedule_ref\s+"
    r"AND\s+history\.current_until_at\s+IS\s+NULL",
    re.IGNORECASE,
)

_UNDO_BASIS_UNQUALIFIED_RE = re.compile(
    r"FROM\s+dante\.schedule_placement_current_history\s+"
    r"WHERE\s+schedule_ref\s*=\s*requested_schedule_ref\s+"
    r"AND\s+material_state_ref\s*=\s*original_material_state_ref\s+"
    r"AND\s+current_until_at\s*=\s*unscheduled_at",
    re.IGNORECASE,
)
_UNDO_BASIS_QUALIFIED_RE = re.compile(
    r"FROM\s+dante\.schedule_placement_current_history\s+AS\s+history\s+"
    r"WHERE\s+history\.schedule_ref\s*=\s*requested_schedule_ref\s+"
    r"AND\s+history\.material_state_ref\s*=\s*original_material_state_ref\s+"
    r"AND\s+history\.current_until_at\s*=\s*unscheduled_at",
    re.IGNORECASE,
)

_UNDO_LATER_UNQUALIFIED_RE = re.compile(
    r"FROM\s+dante\.schedule_placement_current_history\s+"
    r"WHERE\s+schedule_ref\s*=\s*requested_schedule_ref\s+"
    r"AND\s+current_from_at\s*>=\s*unscheduled_at",
    re.IGNORECASE,
)
_UNDO_LATER_QUALIFIED_RE = re.compile(
    r"FROM\s+dante\.schedule_placement_current_history\s+AS\s+history\s+"
    r"WHERE\s+history\.schedule_ref\s*=\s*requested_schedule_ref\s+"
    r"AND\s+history\.current_from_at\s*>=\s*unscheduled_at",
    re.IGNORECASE,
)

_UPDATE_QUALIFIED_SQL = """UPDATE dante.schedule_placement_current_history AS history
                           SET current_until_at = recorded_at
                         WHERE history.schedule_ref = requested_schedule_ref
                           AND history.material_state_ref = current_material_state_ref
                           AND history.current_until_at IS NULL;"""
_UPDATE_UNQUALIFIED_SQL = """UPDATE dante.schedule_placement_current_history
                           SET current_until_at = recorded_at
                         WHERE schedule_ref = requested_schedule_ref
                           AND material_state_ref = current_material_state_ref
                           AND current_until_at IS NULL;"""
_UNDO_OPEN_QUALIFIED_SQL = """FROM dante.schedule_placement_current_history AS history
                             WHERE history.schedule_ref = requested_schedule_ref
                               AND history.current_until_at IS NULL"""
_UNDO_OPEN_UNQUALIFIED_SQL = """FROM dante.schedule_placement_current_history
                             WHERE schedule_ref = requested_schedule_ref
                               AND current_until_at IS NULL"""
_UNDO_BASIS_QUALIFIED_SQL = """FROM dante.schedule_placement_current_history AS history
                             WHERE history.schedule_ref = requested_schedule_ref
                               AND history.material_state_ref = original_material_state_ref
                               AND history.current_until_at = unscheduled_at"""
_UNDO_BASIS_UNQUALIFIED_SQL = """FROM dante.schedule_placement_current_history
                             WHERE schedule_ref = requested_schedule_ref
                               AND material_state_ref = original_material_state_ref
                               AND current_until_at = unscheduled_at"""
_UNDO_LATER_QUALIFIED_SQL = """FROM dante.schedule_placement_current_history AS history
                             WHERE history.schedule_ref = requested_schedule_ref
                               AND history.current_from_at >= unscheduled_at"""
_UNDO_LATER_UNQUALIFIED_SQL = """FROM dante.schedule_placement_current_history
                             WHERE schedule_ref = requested_schedule_ref
                               AND current_from_at >= unscheduled_at"""


def _function_definition(signature: str) -> str:
    definition = op.get_bind().execute(
        sa.text("SELECT pg_get_functiondef(to_regprocedure(:signature))"),
        {"signature": signature},
    ).scalar_one_or_none()
    if definition is None:
        raise RuntimeError(f"B02 function is missing: {signature}")
    return str(definition)


def _install(definition: str) -> None:
    op.get_bind().exec_driver_sql(definition)


def _with_strict_disambiguation(signature: str, definition: str) -> str:
    definition = _DIRECTIVE_RE.sub("", definition)
    definition, marker_count = _BODY_MARKER_RE.subn(
        r"\1#variable_conflict error\n", definition, count=1
    )
    if marker_count != 1:
        raise RuntimeError(f"B02 function body marker not found: {signature}")

    rewrites = 0
    definition, count = _UPDATE_UNQUALIFIED_RE.subn(
        _UPDATE_QUALIFIED_SQL, definition
    )
    rewrites += count
    definition, count = _UNDO_OPEN_UNQUALIFIED_RE.subn(
        _UNDO_OPEN_QUALIFIED_SQL, definition
    )
    rewrites += count
    definition, count = _UNDO_BASIS_UNQUALIFIED_RE.subn(
        _UNDO_BASIS_QUALIFIED_SQL, definition
    )
    rewrites += count
    definition, count = _UNDO_LATER_UNQUALIFIED_RE.subn(
        _UNDO_LATER_QUALIFIED_SQL, definition
    )
    rewrites += count

    expected = _EXPECTED_REWRITES[signature]
    if rewrites != expected:
        raise RuntimeError(
            f"B02 PL/pgSQL disambiguation drift for {signature}: "
            f"expected {expected} rewrites, got {rewrites}"
        )
    return definition


def _without_strict_disambiguation(signature: str, definition: str) -> str:
    definition, directive_count = _DIRECTIVE_RE.subn("", definition)
    if directive_count != 1:
        raise RuntimeError(
            f"B02 PL/pgSQL directive drift for {signature}: "
            f"expected 1 directive, got {directive_count}"
        )

    rewrites = 0
    definition, count = _UPDATE_QUALIFIED_RE.subn(
        _UPDATE_UNQUALIFIED_SQL, definition
    )
    rewrites += count
    definition, count = _UNDO_OPEN_QUALIFIED_RE.subn(
        _UNDO_OPEN_UNQUALIFIED_SQL, definition
    )
    rewrites += count
    definition, count = _UNDO_BASIS_QUALIFIED_RE.subn(
        _UNDO_BASIS_UNQUALIFIED_SQL, definition
    )
    rewrites += count
    definition, count = _UNDO_LATER_QUALIFIED_RE.subn(
        _UNDO_LATER_UNQUALIFIED_SQL, definition
    )
    rewrites += count

    expected = _EXPECTED_REWRITES[signature]
    if rewrites != expected:
        raise RuntimeError(
            f"B02 PL/pgSQL downgrade drift for {signature}: "
            f"expected {expected} rewrites, got {rewrites}"
        )
    return definition


def upgrade() -> None:
    """Qualify ambiguous history columns under strict PL/pgSQL handling."""
    for signature in _EXPECTED_REWRITES:
        _install(_with_strict_disambiguation(signature, _function_definition(signature)))


def downgrade() -> None:
    """Restore the immediately preceding function definitions."""
    for signature in _EXPECTED_REWRITES:
        _install(
            _without_strict_disambiguation(signature, _function_definition(signature))
        )
