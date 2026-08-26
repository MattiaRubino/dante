"""SQLAlchemy Core handles for bounded M5 current-facet views.

These objects are deliberately isolated from ``Base.metadata``.  PostgreSQL/Alembic
own the view DDL; the handles exist only for explicit Core DML/query construction.
"""

from sqlalchemy import Column, MetaData, Table, Text
from sqlalchemy.dialects.postgresql import UUID

VIEW_METADATA = MetaData()

schedule_current_placement = Table(
    "schedule_current_placement",
    VIEW_METADATA,
    Column("scoped_owner_ref", UUID(as_uuid=True), nullable=False),
    Column("facet_code", Text, nullable=False),
    Column("material_state_ref", UUID(as_uuid=True), nullable=False),
    schema="dante",
)

actual_current_realization = Table(
    "actual_current_realization",
    VIEW_METADATA,
    Column("scoped_owner_ref", UUID(as_uuid=True), nullable=False),
    Column("facet_code", Text, nullable=False),
    Column("material_state_ref", UUID(as_uuid=True), nullable=False),
    schema="dante",
)

session_current_timing = Table(
    "session_current_timing",
    VIEW_METADATA,
    Column("native_owner_ref", UUID(as_uuid=True), nullable=False),
    Column("facet_code", Text, nullable=False),
    Column("material_state_ref", UUID(as_uuid=True), nullable=False),
    schema="dante",
)

routine_current_recurrence = Table(
    "routine_current_recurrence",
    VIEW_METADATA,
    Column("native_owner_ref", UUID(as_uuid=True), nullable=False),
    Column("facet_code", Text, nullable=False),
    Column("material_state_ref", UUID(as_uuid=True), nullable=False),
    schema="dante",
)

event_current_recurrence = Table(
    "event_current_recurrence",
    VIEW_METADATA,
    Column("native_owner_ref", UUID(as_uuid=True), nullable=False),
    Column("facet_code", Text, nullable=False),
    Column("material_state_ref", UUID(as_uuid=True), nullable=False),
    schema="dante",
)

CURRENT_VIEW_TABLES: tuple[Table, ...] = (
    schedule_current_placement,
    actual_current_realization,
    session_current_timing,
    routine_current_recurrence,
    event_current_recurrence,
)

__all__ = [
    "CURRENT_VIEW_TABLES",
    "VIEW_METADATA",
    "actual_current_realization",
    "event_current_recurrence",
    "routine_current_recurrence",
    "schedule_current_placement",
    "session_current_timing",
]
