"""Bounded direct Activity relation, immutable states and operation receipts."""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import NativeRef


class ActivityDecompositionRow(Base):
    __tablename__ = "activity_decomposition"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(decomposition_ref) IS NOT DISTINCT FROM 7", name="uuidv7"
        ),
        CheckConstraint("parent_activity_ref<>child_activity_ref", name="distinct"),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_activity_decomposition_person",
        ),
        ForeignKeyConstraint(
            ["parent_activity_ref"],
            ["dante.activity_intention.activity_ref"],
            name="fk_activity_decomposition_parent",
        ),
        ForeignKeyConstraint(
            ["child_activity_ref"],
            ["dante.activity_intention.activity_ref"],
            name="fk_activity_decomposition_child",
        ),
        Index("ix_activity_decomposition_parent", "parent_activity_ref"),
        Index("ix_activity_decomposition_child", "child_activity_ref"),
    )

    decomposition_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    self_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    parent_activity_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    child_activity_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ActivityDecompositionStateRow(Base):
    __tablename__ = "activity_decomposition_state"
    __table_args__ = (
        CheckConstraint("uuid_extract_version(state_ref) IS NOT DISTINCT FROM 7", name="uuidv7"),
        CheckConstraint("requirement_code IN ('required','optional')", name="requirement"),
        CheckConstraint("presentation_order>0", name="order"),
        CheckConstraint("isfinite(recorded_at)", name="recorded_at"),
        UniqueConstraint(
            "decomposition_ref", "state_ref", name="uq_activity_decomposition_state_owner"
        ),
        ForeignKeyConstraint(
            ["decomposition_ref"],
            ["dante.activity_decomposition.decomposition_ref"],
            name="fk_activity_decomposition_state_relation",
        ),
        Index("ix_activity_decomposition_state_relation", "decomposition_ref"),
    )

    state_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    decomposition_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    requirement_code: Mapped[str] = mapped_column(Text, nullable=False)
    presentation_order: Mapped[int] = mapped_column(Integer, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ActivityDecompositionCurrentHistoryRow(Base):
    __tablename__ = "activity_decomposition_current_history"
    __table_args__ = (
        CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR (isfinite(current_until_at) AND current_until_at>current_from_at))",
            name="interval",
        ),
        ForeignKeyConstraint(
            ["decomposition_ref", "state_ref"],
            [
                "dante.activity_decomposition_state.decomposition_ref",
                "dante.activity_decomposition_state.state_ref",
            ],
            name="fk_activity_decomposition_current_history_state",
        ),
        Index(
            "ux_activity_decomposition_current_history_open",
            "decomposition_ref",
            unique=True,
            postgresql_where=text("current_until_at IS NULL"),
        ),
        Index("ix_activity_decomposition_current_history_state", "state_ref"),
    )

    decomposition_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    state_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    current_from_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    current_until_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ActivityDecompositionOperationRow(Base):
    __tablename__ = "activity_decomposition_operation"
    __table_args__ = (
        CheckConstraint(
            "operation_id=btrim(operation_id) AND char_length(operation_id) BETWEEN 1 AND 200",
            name="id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        UniqueConstraint("state_ref", name="uq_activity_decomposition_operation_state"),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_activity_decomposition_operation_person",
        ),
        ForeignKeyConstraint(
            ["decomposition_ref", "state_ref"],
            [
                "dante.activity_decomposition_state.decomposition_ref",
                "dante.activity_decomposition_state.state_ref",
            ],
            name="fk_activity_decomposition_operation_state",
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    decomposition_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    state_ref: Mapped[NativeRef] = mapped_column(nullable=False)
