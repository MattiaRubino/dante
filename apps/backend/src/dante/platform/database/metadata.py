"""Canonical SQLAlchemy metadata for DANTE-owned PostgreSQL objects."""

from typing import Any, ClassVar

from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase

from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef

DANTE_SCHEMA = "dante"

NAMING_CONVENTION: dict[str, str] = {
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
}


class Base(DeclarativeBase):
    """Shared persistence base; mapped rows remain private to capability adapters."""

    metadata = MetaData(schema=DANTE_SCHEMA, naming_convention=NAMING_CONVENTION)
    type_annotation_map: ClassVar[dict[Any, Any]] = {
        NativeRef: PGUUID(as_uuid=True),
        ScopedRecordRef: PGUUID(as_uuid=True),
        MaterialStateRef: PGUUID(as_uuid=True),
    }
