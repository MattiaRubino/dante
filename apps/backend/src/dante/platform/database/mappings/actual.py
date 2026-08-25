"""SQLAlchemy row mappings for the Actual family materialized so far."""

from sqlalchemy import CheckConstraint, ForeignKeyConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import NativeRef, ScopedRecordRef


class ActualRow(Base):
    """Persistence row for dante.actual; not a Domain model class."""

    __tablename__ = "actual"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(actual_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        ForeignKeyConstraint(
            ["subject_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_actual_subject_native_ref_native_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index("ix_actual_subject_native_ref", "subject_native_ref"),
    )

    actual_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    subject_native_ref: Mapped[NativeRef] = mapped_column(nullable=False)
