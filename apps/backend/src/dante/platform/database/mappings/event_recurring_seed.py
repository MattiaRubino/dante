"""Canonical first Event to future recurrence source association."""

from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import NativeRef


class EventRecurringSeedRow(Base):
    __tablename__ = "event_recurring_seed"
    __table_args__ = (
        UniqueConstraint("source_event_ref", name="uq_event_recurring_seed_source"),
        UniqueConstraint("first_occurrence_ref", name="uq_event_recurring_seed_occurrence"),
        Index(
            "ix_event_recurring_seed_pending_first",
            "self_person_ref",
            "source_event_ref",
            postgresql_where=text("first_occurrence_ref IS NULL"),
        ),
        CheckConstraint(
            "(legacy_repaired_at IS NULL AND legacy_exclusion_ref IS NULL "
            "AND legacy_exclusion_operation_id IS NULL AND legacy_exclusion_fingerprint IS NULL "
            "AND legacy_exclusion_accepted_at IS NULL) OR "
            "(legacy_repaired_at IS NOT NULL AND first_occurrence_ref IS NOT NULL "
            "AND legacy_exclusion_ref IS NOT NULL AND legacy_exclusion_operation_id IS NOT NULL "
            "AND legacy_exclusion_fingerprint IS NOT NULL "
            "AND legacy_exclusion_accepted_at IS NOT NULL)",
            name="ck_event_recurring_seed_legacy_proof",
        ),
        ForeignKeyConstraint(
            ["event_ref"],
            ["dante.event_expectation.event_ref"],
            name="fk_event_recurring_seed_event",
        ),
        ForeignKeyConstraint(
            ["source_event_ref"],
            ["dante.event_expectation.event_ref"],
            name="fk_event_recurring_seed_source",
        ),
        ForeignKeyConstraint(
            ["first_occurrence_ref"],
            ["dante.occurrence.occurrence_ref"],
            name="fk_event_recurring_seed_occurrence",
        ),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_event_recurring_seed_person",
        ),
    )

    event_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    source_event_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    self_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    first_occurrence_ref: Mapped[NativeRef | None] = mapped_column(nullable=True)
    legacy_exclusion_ref: Mapped[NativeRef | None] = mapped_column(nullable=True)
    legacy_exclusion_operation_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    legacy_exclusion_fingerprint: Mapped[str | None] = mapped_column(Text, nullable=True)
    legacy_exclusion_accepted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    legacy_repaired_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
