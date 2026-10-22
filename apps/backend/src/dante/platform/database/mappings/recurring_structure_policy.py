"""Immutable source structure snapshots for recurring series revisions."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import conv

from dante.platform.database.metadata import Base


class RecurringStructurePolicyRevisionRow(Base):
    __tablename__ = "recurring_structure_policy_revision"
    __table_args__ = (
        UniqueConstraint(
            "self_person_ref",
            "operation_id",
            name="uq_recurring_structure_policy_revision_operation",
        ),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_recurring_structure_policy_revision_person",
        ),
        ForeignKeyConstraint(
            ["source_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_recurring_structure_policy_revision_source",
        ),
        ForeignKeyConstraint(
            ["recurrence_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_recurring_structure_policy_revision_state",
        ),
        CheckConstraint(
            "owner_kind IN ('routine','event')",
            name=conv("ck_recurring_structure_policy_revision_owner"),
        ),
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name=conv("ck_recurring_structure_policy_revision_operation"),
        ),
        CheckConstraint(
            "jsonb_typeof(structure_snapshot)='object' AND structure_snapshot<>'{}'::jsonb",
            name=conv("ck_recurring_structure_policy_revision_snapshot"),
        ),
        Index("ix_recurring_structure_policy_revision_source", "source_native_ref", "accepted_at"),
    )

    recurrence_state_ref: Mapped[UUID] = mapped_column(primary_key=True)
    self_person_ref: Mapped[UUID] = mapped_column(nullable=False)
    source_native_ref: Mapped[UUID] = mapped_column(nullable=False)
    owner_kind: Mapped[str] = mapped_column(Text, nullable=False)
    operation_id: Mapped[str] = mapped_column(Text, nullable=False)
    previous_state_ref: Mapped[UUID] = mapped_column(nullable=False)
    request_hash: Mapped[str] = mapped_column(Text, nullable=False)
    preview_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    superseded_count: Mapped[int] = mapped_column(Integer, nullable=False)
    protected_count: Mapped[int] = mapped_column(Integer, nullable=False)
    structure_snapshot: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RecurringOccurrenceSupersessionRow(Base):
    """Retired clean planning identity; its historic graph is retained."""

    __tablename__ = "recurring_occurrence_supersession"
    __table_args__ = (
        UniqueConstraint(
            "self_person_ref",
            "operation_id",
            name="uq_recurring_occurrence_supersession_operation",
        ),
        ForeignKeyConstraint(
            ["occurrence_ref"],
            ["dante.occurrence.occurrence_ref"],
            name="fk_recurring_occurrence_supersession_occurrence",
        ),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_recurring_occurrence_supersession_person",
        ),
        ForeignKeyConstraint(
            ["source_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_recurring_occurrence_supersession_source",
        ),
        ForeignKeyConstraint(
            ["replacement_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_recurring_occurrence_supersession_state",
        ),
        Index("ix_recurring_occurrence_supersession_source", "source_native_ref"),
    )

    occurrence_ref: Mapped[UUID] = mapped_column(primary_key=True)
    self_person_ref: Mapped[UUID] = mapped_column(nullable=False)
    source_native_ref: Mapped[UUID] = mapped_column(nullable=False)
    replacement_state_ref: Mapped[UUID] = mapped_column(nullable=False)
    operation_id: Mapped[str] = mapped_column(Text, nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
