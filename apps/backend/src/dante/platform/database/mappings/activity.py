"""SQLAlchemy rows for canonical Activity persistence."""

from datetime import datetime

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKeyConstraint, Index, Text
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import NativeRef


class ActivityIntentionRow(Base):
    """Durable actionable-intention descriptor for one personal Activity."""

    __tablename__ = "activity_intention"
    __table_args__ = (
        CheckConstraint("profile_revision >= 0", name="profile_revision"),
        CheckConstraint("(retired_at IS NULL) = (retired_operation_id IS NULL)", name="retired_pair"),
        CheckConstraint(
            "title=btrim(title) AND title<>'' AND char_length(title)<=300",
            name="title",
        ),
        CheckConstraint(
            "description IS NULL OR (description=btrim(description) AND description<>'')",
            name="description",
        ),
        CheckConstraint(
            "location IS NULL OR (location=btrim(location) AND location<>'')",
            name="location",
        ),
        CheckConstraint(
            "color_code IS NULL OR color_code ~ '^#[0-9A-F]{6}$'",
            name="color_code",
        ),
        ForeignKeyConstraint(
            ["activity_ref"],
            ["dante.activity.activity_ref"],
            name="fk_activity_intention_activity_ref_activity",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_activity_intention_self_person_ref_person",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ix_activity_intention_self_person_created",
            "self_person_ref",
            "created_at",
            "activity_ref",
        ),
    )

    activity_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    self_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[str | None] = mapped_column(Text, nullable=True)
    color_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    profile_revision: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default="0")
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    retired_operation_id: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ActivityCreateOperationRow(Base):
    """Idempotency receipt for one self-scoped CreateActivity operation."""

    __tablename__ = "activity_create_operation"
    __table_args__ = (
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name="fingerprint",
        ),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_activity_create_operation_self_person_ref_person",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["activity_ref"],
            ["dante.activity.activity_ref"],
            name="fk_activity_create_operation_activity_ref_activity",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    activity_ref: Mapped[NativeRef] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
