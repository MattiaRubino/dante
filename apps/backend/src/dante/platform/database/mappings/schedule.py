"""SQLAlchemy row mappings for the Schedule family materialized so far."""

from sqlalchemy import CheckConstraint, ForeignKeyConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import NativeRef, ScopedRecordRef


class ScheduleRow(Base):
    """Persistence row for dante.schedule; not a Domain model class."""

    __tablename__ = "schedule"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(schedule_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        ForeignKeyConstraint(
            ["subject_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_schedule_subject_native_ref_native_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index("ix_schedule_subject_native_ref", "subject_native_ref"),
    )

    schedule_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    subject_native_ref: Mapped[NativeRef] = mapped_column(nullable=False)
