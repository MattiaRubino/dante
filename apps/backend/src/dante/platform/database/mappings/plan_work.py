"""Canonical B13-A Plan work structure persistence mappings."""

from datetime import datetime

from sqlalchemy import (
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


class PlanIntentionRow(Base):
    __tablename__ = "plan_intention"
    __table_args__ = (
        ForeignKeyConstraint(["plan_ref"], ["dante.plan.plan_ref"], name="fk_plan_intention_plan"),
        ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"], name="fk_plan_intention_person"
        ),
        Index("ix_plan_intention_self", "self_person_ref"),
    )

    plan_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    self_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PlanStepRow(Base):
    __tablename__ = "plan_step"
    __table_args__ = (
        CheckConstraint("uuid_extract_version(step_ref) IS NOT DISTINCT FROM 7", name="uuidv7"),
        UniqueConstraint("plan_ref", "step_ref", name="uq_plan_step_owner"),
        ForeignKeyConstraint(
            ["plan_ref"], ["dante.plan_intention.plan_ref"], name="fk_plan_step_plan"
        ),
        Index("ix_plan_step_plan", "plan_ref"),
    )

    step_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    plan_ref: Mapped[NativeRef] = mapped_column(nullable=False)


class PlanWorkStateRow(Base):
    __tablename__ = "plan_work_state"
    __table_args__ = (
        CheckConstraint("uuid_extract_version(state_ref) IS NOT DISTINCT FROM 7", name="uuidv7"),
        CheckConstraint(
            "title=btrim(title) AND title<>'' AND char_length(title)<=300", name="title"
        ),
        UniqueConstraint("plan_ref", "state_ref", name="uq_plan_work_state_owner"),
        ForeignKeyConstraint(
            ["plan_ref"], ["dante.plan_intention.plan_ref"], name="fk_plan_work_state_plan"
        ),
        Index("ix_plan_work_state_plan", "plan_ref"),
    )

    state_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    plan_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PlanStepInStateRow(Base):
    __tablename__ = "plan_step_in_state"
    __table_args__ = (
        UniqueConstraint("state_ref", "position", name="uq_plan_step_in_state_position"),
        CheckConstraint("position>=0 AND position<1000", name="position"),
        CheckConstraint(
            "title=btrim(title) AND title<>'' AND char_length(title)<=300", name="title"
        ),
        ForeignKeyConstraint(
            ["plan_ref", "state_ref"],
            ["dante.plan_work_state.plan_ref", "dante.plan_work_state.state_ref"],
            name="fk_plan_step_in_state_work",
        ),
        ForeignKeyConstraint(
            ["plan_ref", "step_ref"],
            ["dante.plan_step.plan_ref", "dante.plan_step.step_ref"],
            name="fk_plan_step_in_state_step",
        ),
        ForeignKeyConstraint(
            ["activity_ref"],
            ["dante.activity.activity_ref"],
            name="fk_plan_step_in_state_activity",
        ),
        Index(
            "ux_plan_step_in_state_activity",
            "state_ref",
            "activity_ref",
            unique=True,
            postgresql_where=text("activity_ref IS NOT NULL"),
        ),
    )

    state_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    plan_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    step_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    activity_ref: Mapped[NativeRef | None] = mapped_column(nullable=True)


class PlanCurrentWorkStateRow(Base):
    __tablename__ = "plan_current_work_state"
    __table_args__ = (
        ForeignKeyConstraint(
            ["plan_ref", "state_ref"],
            ["dante.plan_work_state.plan_ref", "dante.plan_work_state.state_ref"],
            name="fk_plan_current_work_state_state",
        ),
    )

    plan_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    state_ref: Mapped[NativeRef] = mapped_column(nullable=False)


class PlanWorkCurrentHistoryRow(Base):
    __tablename__ = "plan_work_current_history"
    __table_args__ = (
        CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at>current_from_at))",
            name="interval",
        ),
        ForeignKeyConstraint(
            ["plan_ref", "state_ref"],
            ["dante.plan_work_state.plan_ref", "dante.plan_work_state.state_ref"],
            name="fk_plan_work_current_history_state",
        ),
        Index(
            "ux_plan_work_current_history_open",
            "plan_ref",
            unique=True,
            postgresql_where=text("current_until_at IS NULL"),
        ),
    )

    plan_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    state_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    current_from_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    current_until_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class PlanWorkOperationRow(Base):
    __tablename__ = "plan_work_operation"
    __table_args__ = (
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name="id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        UniqueConstraint("state_ref", name="uq_plan_work_operation_state"),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_plan_work_operation_person",
        ),
        ForeignKeyConstraint(
            ["plan_ref", "state_ref"],
            ["dante.plan_work_state.plan_ref", "dante.plan_work_state.state_ref"],
            name="fk_plan_work_operation_state",
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    plan_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    state_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
