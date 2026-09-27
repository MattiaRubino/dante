"""SQLAlchemy rows for the bounded B11-C personal Schedule Reminder family."""

from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKeyConstraint, Index, Integer, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef


class ScheduleReminderRow(Base):
    """Stable self-personal Reminder identity attached to one Schedule."""

    __tablename__ = "schedule_reminder"
    __table_args__ = (
        CheckConstraint("uuid_extract_version(reminder_ref) IS NOT DISTINCT FROM 7", name="uuidv7"),
        UniqueConstraint("self_person_ref", "schedule_ref", name="uq_schedule_reminder_self_schedule"),
        ForeignKeyConstraint(["self_person_ref"], ["dante.person.person_ref"], name="fk_schedule_reminder_person"),
        ForeignKeyConstraint(["schedule_ref"], ["dante.schedule.schedule_ref"], name="fk_schedule_reminder_schedule"),
        Index("ix_schedule_reminder_schedule", "schedule_ref"),
    )

    reminder_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    self_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    schedule_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)


class ScheduleReminderConfigurationStateRow(Base):
    """Append-only enabled/lead MaterialState, never a copied due timestamp."""

    __tablename__ = "schedule_reminder_configuration_state"
    __table_args__ = (
        UniqueConstraint("reminder_ref", "material_state_ref", name="uq_schedule_reminder_configuration_state_owner_state"),
        CheckConstraint("lead_minutes BETWEEN 0 AND 10080", name="lead"),
        ForeignKeyConstraint(["material_state_ref"], ["dante.material_state_address.material_state_ref"], name="fk_schedule_reminder_configuration_state_address"),
        ForeignKeyConstraint(["reminder_ref"], ["dante.schedule_reminder.reminder_ref"], name="fk_schedule_reminder_configuration_state_reminder"),
        Index("ix_schedule_reminder_configuration_state_reminder", "reminder_ref"),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    reminder_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False)
    lead_minutes: Mapped[int] = mapped_column(Integer, nullable=False)


class ScheduleReminderCurrentHistoryRow(Base):
    """Explicit accepted-current episodes, distinct from latest inserted state."""

    __tablename__ = "schedule_reminder_current_history"
    __table_args__ = (
        CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at>current_from_at))",
            name="interval",
        ),
        ForeignKeyConstraint(
            ["reminder_ref", "material_state_ref"],
            ["dante.schedule_reminder_configuration_state.reminder_ref", "dante.schedule_reminder_configuration_state.material_state_ref"],
            name="fk_schedule_reminder_current_history_state",
        ),
        Index("ux_schedule_reminder_current_history_open", "reminder_ref", unique=True, postgresql_where=text("current_until_at IS NULL")),
        Index("ix_schedule_reminder_current_history_state", "material_state_ref"),
    )

    reminder_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    current_from_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    current_until_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ScheduleReminderOperationRow(Base):
    """Self-scoped idempotency receipt, not Reminder identity."""

    __tablename__ = "schedule_reminder_operation"
    __table_args__ = (
        CheckConstraint("operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200", name="id"),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        UniqueConstraint("resulting_material_state_ref", name="uq_schedule_reminder_operation_state"),
        ForeignKeyConstraint(["self_person_ref"], ["dante.person.person_ref"], name="fk_schedule_reminder_operation_person"),
        ForeignKeyConstraint(["reminder_ref"], ["dante.schedule_reminder.reminder_ref"], name="fk_schedule_reminder_operation_reminder"),
        ForeignKeyConstraint(["schedule_ref"], ["dante.schedule.schedule_ref"], name="fk_schedule_reminder_operation_schedule"),
        ForeignKeyConstraint(
            ["reminder_ref", "resulting_material_state_ref"],
            ["dante.schedule_reminder_configuration_state.reminder_ref", "dante.schedule_reminder_configuration_state.material_state_ref"],
            name="fk_schedule_reminder_operation_result_state",
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    reminder_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    schedule_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    expected_material_state_ref: Mapped[MaterialStateRef | None] = mapped_column(nullable=True)
    resulting_material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
