"""Five canonical relation/current/history/operation mappings for B13-B."""

from datetime import datetime

from sqlalchemy import (
    Boolean,
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
from dante.platform.database.references import NativeRef, ScopedRecordRef


class PlanDependencyRow(Base):
    __tablename__ = "plan_dependency"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(dependency_ref) IS NOT DISTINCT FROM 7", name="uuidv7"
        ),
        CheckConstraint(
            "prerequisite_step_ref<>dependent_step_ref AND "
            "prerequisite_activity_ref<>dependent_activity_ref",
            name="distinct_endpoints",
        ),
        CheckConstraint(
            "purpose_code='dependent_activity_admissibility'",
            name="purpose",
        ),
        UniqueConstraint("plan_ref", "dependency_ref", name="uq_plan_dependency_plan"),
        ForeignKeyConstraint(
            ["plan_ref"], ["dante.plan_intention.plan_ref"], name="fk_plan_dependency_plan"
        ),
        ForeignKeyConstraint(
            ["plan_ref", "prerequisite_step_ref"],
            ["dante.plan_step.plan_ref", "dante.plan_step.step_ref"],
            name="fk_plan_dependency_prerequisite_step",
        ),
        ForeignKeyConstraint(
            ["plan_ref", "dependent_step_ref"],
            ["dante.plan_step.plan_ref", "dante.plan_step.step_ref"],
            name="fk_plan_dependency_dependent_step",
        ),
        ForeignKeyConstraint(
            ["prerequisite_activity_ref"],
            ["dante.activity.activity_ref"],
            name="fk_plan_dependency_prerequisite_activity",
        ),
        ForeignKeyConstraint(
            ["dependent_activity_ref"],
            ["dante.activity.activity_ref"],
            name="fk_plan_dependency_dependent_activity",
        ),
        Index("ix_plan_dependency_plan", "plan_ref"),
    )

    dependency_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    plan_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    prerequisite_step_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    prerequisite_activity_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    dependent_step_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    dependent_activity_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    purpose_code: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PlanDependencyStateRow(Base):
    __tablename__ = "plan_dependency_state"
    __table_args__ = (
        CheckConstraint("uuid_extract_version(state_ref) IS NOT DISTINCT FROM 7", name="uuidv7"),
        CheckConstraint(
            "(qualifier_code='actual_occurred' AND disposition_code IS NULL) OR "
            "(qualifier_code='outcome_code' AND disposition_code IS NOT NULL AND "
            "disposition_code=btrim(disposition_code) AND "
            "char_length(disposition_code) BETWEEN 1 AND 120 AND "
            "disposition_code ~ '^[a-z0-9][a-z0-9._:-]*$')",
            name="qualifier",
        ),
        UniqueConstraint("dependency_ref", "state_ref", name="uq_plan_dependency_state_owner"),
        ForeignKeyConstraint(
            ["dependency_ref"],
            ["dante.plan_dependency.dependency_ref"],
            name="fk_plan_dependency_state_owner",
        ),
        Index("ix_plan_dependency_state_owner", "dependency_ref"),
    )

    state_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    dependency_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    qualifier_code: Mapped[str] = mapped_column(Text, nullable=False)
    disposition_code: Mapped[str | None] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PlanDependencyCurrentStateRow(Base):
    __tablename__ = "plan_dependency_current_state"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dependency_ref", "state_ref"],
            ["dante.plan_dependency_state.dependency_ref", "dante.plan_dependency_state.state_ref"],
            name="fk_plan_dependency_current_state",
        ),
    )

    dependency_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    state_ref: Mapped[NativeRef] = mapped_column(nullable=False)


class PlanDependencyCurrentHistoryRow(Base):
    __tablename__ = "plan_dependency_current_history"
    __table_args__ = (
        CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at>current_from_at))",
            name="interval",
        ),
        ForeignKeyConstraint(
            ["dependency_ref", "state_ref"],
            ["dante.plan_dependency_state.dependency_ref", "dante.plan_dependency_state.state_ref"],
            name="fk_plan_dependency_current_history_state",
        ),
        Index(
            "ux_plan_dependency_current_history_open",
            "dependency_ref",
            unique=True,
            postgresql_where=text("current_until_at IS NULL"),
        ),
    )

    dependency_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    state_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    current_from_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    current_until_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class PlanDependencyOperationRow(Base):
    __tablename__ = "plan_dependency_operation"
    __table_args__ = (
        UniqueConstraint("state_ref", name="uq_plan_dependency_operation_state"),
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name="id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_plan_dependency_operation_person",
        ),
        ForeignKeyConstraint(
            ["dependency_ref", "state_ref"],
            ["dante.plan_dependency_state.dependency_ref", "dante.plan_dependency_state.state_ref"],
            name="fk_plan_dependency_operation_state",
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    dependency_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    state_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
