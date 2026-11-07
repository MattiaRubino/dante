"""Canonical first Event to future recurrence source association."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import NativeRef


class EventRecurringSeedRow(Base):
    __tablename__ = "event_recurring_seed"
    __table_args__ = (
        UniqueConstraint("source_event_ref", name="uq_event_recurring_seed_source"),
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
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_event_recurring_seed_person",
        ),
    )

    event_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    source_event_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    self_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
