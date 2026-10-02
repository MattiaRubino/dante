"""Accepted-current Activity Session capture policy persistence rows."""

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


class ActivityExecutionPolicyRow(Base):
    __tablename__ = "activity_execution_policy"
    __table_args__ = (
        ForeignKeyConstraint(
            ["activity_ref"], ["dante.activity_intention.activity_ref"],
            name="fk_activity_execution_policy_activity",
        ),
        ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_activity_execution_policy_person",
        ),
        Index("ix_activity_execution_policy_self", "self_person_ref"),
    )

    activity_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    self_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ActivityExecutionPolicyStateRow(Base):
    __tablename__ = "activity_execution_policy_state"
    __table_args__ = (
        CheckConstraint("uuid_extract_version(state_ref) IS NOT DISTINCT FROM 7", name="uuidv7"),
        CheckConstraint(
            "mode_code IN ('disabled','record','live','record_and_live')", name="mode"
        ),
        CheckConstraint("isfinite(recorded_at)", name="recorded_at"),
        UniqueConstraint("activity_ref", "state_ref", name="uq_activity_execution_policy_state_owner"),
        ForeignKeyConstraint(
            ["activity_ref"], ["dante.activity_execution_policy.activity_ref"],
            name="fk_activity_execution_policy_state_owner",
        ),
        Index("ix_activity_execution_policy_state_owner", "activity_ref"),
    )

    state_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    activity_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    mode_code: Mapped[str] = mapped_column(Text, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ActivityExecutionPolicyCurrentHistoryRow(Base):
    __tablename__ = "activity_execution_policy_current_history"
    __table_args__ = (
        CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at>current_from_at))",
            name="interval",
        ),
        ForeignKeyConstraint(
            ["activity_ref", "state_ref"],
            ["dante.activity_execution_policy_state.activity_ref",
             "dante.activity_execution_policy_state.state_ref"],
            name="fk_activity_execution_policy_current_history_state",
        ),
        Index(
            "ux_activity_execution_policy_current_history_open", "activity_ref",
            unique=True, postgresql_where=text("current_until_at IS NULL"),
        ),
        Index("ix_activity_execution_policy_current_history_state", "state_ref"),
    )

    activity_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    state_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    current_from_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    current_until_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ActivityExecutionPolicyOperationRow(Base):
    __tablename__ = "activity_execution_policy_operation"
    __table_args__ = (
        CheckConstraint(
            "operation_id=btrim(operation_id) AND char_length(operation_id) BETWEEN 1 AND 200",
            name="id",
        ),
        CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"
        ),
        UniqueConstraint("state_ref", name="uq_activity_execution_policy_operation_state"),
        ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_activity_execution_policy_operation_person",
        ),
        ForeignKeyConstraint(
            ["activity_ref", "state_ref"],
            ["dante.activity_execution_policy_state.activity_ref",
             "dante.activity_execution_policy_state.state_ref"],
            name="fk_activity_execution_policy_operation_state",
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    activity_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    state_ref: Mapped[NativeRef] = mapped_column(nullable=False)
