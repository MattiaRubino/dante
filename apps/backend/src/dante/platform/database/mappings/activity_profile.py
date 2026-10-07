"""Append-only authored Activity profile revisions."""

from datetime import datetime
from typing import Any

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import NativeRef


class ActivityProfileRevisionRow(Base):
    __tablename__ = "activity_profile_revision"
    __table_args__ = (
        ForeignKeyConstraint(
            ["activity_ref"], ["dante.activity_intention.activity_ref"],
            name="fk_activity_profile_revision_activity",
        ),
        ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_activity_profile_revision_person",
        ),
        UniqueConstraint("self_person_ref", "operation_id", name="uq_activity_profile_revision_operation"),
        CheckConstraint("revision >= 1", name="positive"),
    )

    activity_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    revision: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    self_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    operation_id: Mapped[str] = mapped_column(Text, nullable=False)
    previous_profile: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    current_profile: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    revised_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
