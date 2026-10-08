"""SQLAlchemy row mappings for B14 Create-closure persistence families."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import (
    BigInteger, Boolean, CheckConstraint, DateTime, ForeignKeyConstraint,
    Integer, Numeric, Text, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base


class RoutineOccurrencePolicyRow(Base):
    __tablename__ = "routine_occurrence_policy"

    self_person_ref: Mapped[UUID] = mapped_column(primary_key=True)
    routine_ref: Mapped[UUID] = mapped_column(primary_key=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    reminder_lead_minutes: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    activity_template: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)


class SchedulePlacementLockRow(Base):
    __tablename__ = "schedule_placement_lock"

    schedule_ref: Mapped[UUID] = mapped_column(primary_key=True)
    self_person_ref: Mapped[UUID] = mapped_column(nullable=False)
    locked: Mapped[bool] = mapped_column(Boolean, nullable=False)
    revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RoutineOccurrenceActivityInstanceRow(Base):
    __tablename__ = "routine_occurrence_activity_instance"

    occurrence_ref: Mapped[UUID] = mapped_column(primary_key=True)
    activity_ref: Mapped[UUID] = mapped_column(nullable=False)
    self_person_ref: Mapped[UUID] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EventOccurrencePolicyRow(Base):
    __tablename__ = "event_occurrence_policy"

    self_person_ref: Mapped[UUID] = mapped_column(primary_key=True)
    event_ref: Mapped[UUID] = mapped_column(primary_key=True)
    placement_kind: Mapped[str] = mapped_column(Text, nullable=False)
    duration_minutes: Mapped[int | None] = mapped_column(Integer)
    duration_days: Mapped[int | None] = mapped_column(Integer)
    reminder_lead_minutes: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    reality_mode: Mapped[str] = mapped_column(Text, nullable=False)
    objectives: Mapped[list[dict[str, object]]] = mapped_column(JSONB, nullable=False)


class RealityReviewPolicyRow(Base):
    __tablename__ = "reality_review_policy"

    subject_kind: Mapped[str] = mapped_column(Text, primary_key=True)
    subject_native_ref: Mapped[UUID] = mapped_column(primary_key=True)
    self_person_ref: Mapped[UUID] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RealityReviewPolicyStateRow(Base):
    __tablename__ = "reality_review_policy_state"

    state_ref: Mapped[UUID] = mapped_column(primary_key=True)
    subject_kind: Mapped[str] = mapped_column(Text, nullable=False)
    subject_native_ref: Mapped[UUID] = mapped_column(nullable=False)
    mode_code: Mapped[str] = mapped_column(Text, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RealityReviewPolicyCurrentHistoryRow(Base):
    __tablename__ = "reality_review_policy_current_history"

    subject_kind: Mapped[str] = mapped_column(Text, primary_key=True)
    subject_native_ref: Mapped[UUID] = mapped_column(primary_key=True)
    state_ref: Mapped[UUID] = mapped_column(nullable=False)
    current_from_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    current_until_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class RealityReviewPolicyOperationRow(Base):
    __tablename__ = "reality_review_policy_operation"

    self_person_ref: Mapped[UUID] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    subject_kind: Mapped[str] = mapped_column(Text, nullable=False)
    subject_native_ref: Mapped[UUID] = mapped_column(nullable=False)
    state_ref: Mapped[UUID] = mapped_column(nullable=False)


class TemporalObjectiveRow(Base):
    __tablename__ = "temporal_objective"

    objective_ref: Mapped[UUID] = mapped_column(primary_key=True)
    self_person_ref: Mapped[UUID] = mapped_column(nullable=False)
    subject_kind: Mapped[str] = mapped_column(Text, nullable=False)
    subject_native_ref: Mapped[UUID] = mapped_column(nullable=False)
    label: Mapped[str] = mapped_column(Text, nullable=False)
    result_kind: Mapped[str] = mapped_column(Text, nullable=False)
    comparator_code: Mapped[str | None] = mapped_column(Text)
    target_value: Mapped[Decimal | None] = mapped_column(Numeric)
    target_min: Mapped[Decimal | None] = mapped_column(Numeric)
    target_max: Mapped[Decimal | None] = mapped_column(Numeric)
    unit_code: Mapped[str | None] = mapped_column(Text)
    presentation_order: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class TemporalObjectiveCreateOperationRow(Base):
    __tablename__ = "temporal_objective_create_operation"

    self_person_ref: Mapped[UUID] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    objective_ref: Mapped[UUID] = mapped_column(nullable=False)


class TemporalObjectiveObservationRow(Base):
    __tablename__ = "temporal_objective_observation"

    observation_ref: Mapped[UUID] = mapped_column(primary_key=True)
    objective_ref: Mapped[UUID] = mapped_column(nullable=False)
    observed_boolean: Mapped[bool | None] = mapped_column(Boolean)
    observed_numeric: Mapped[Decimal | None] = mapped_column(Numeric)
    qualitative_code: Mapped[str | None] = mapped_column(Text)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class TemporalObjectiveEvaluationStateRow(Base):
    __tablename__ = "temporal_objective_evaluation_state"

    state_ref: Mapped[UUID] = mapped_column(primary_key=True)
    objective_ref: Mapped[UUID] = mapped_column(nullable=False)
    observation_ref: Mapped[UUID] = mapped_column(nullable=False)
    assessment_code: Mapped[str] = mapped_column(Text, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class TemporalObjectiveEvaluationCurrentHistoryRow(Base):
    __tablename__ = "temporal_objective_evaluation_current_history"

    objective_ref: Mapped[UUID] = mapped_column(primary_key=True)
    state_ref: Mapped[UUID] = mapped_column(nullable=False)
    current_from_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    current_until_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class TemporalObjectiveResultOperationRow(Base):
    __tablename__ = "temporal_objective_result_operation"

    self_person_ref: Mapped[UUID] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    objective_ref: Mapped[UUID] = mapped_column(nullable=False)
    observation_ref: Mapped[UUID] = mapped_column(nullable=False)
    state_ref: Mapped[UUID] = mapped_column(nullable=False)

class TemporalObjectiveDefinitionRevisionRow(Base):
    __tablename__ = "temporal_objective_definition_revision"

    objective_ref: Mapped[UUID] = mapped_column(primary_key=True)
    revision: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    self_person_ref: Mapped[UUID] = mapped_column(nullable=False)
    operation_id: Mapped[str] = mapped_column(Text, nullable=False)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    label: Mapped[str] = mapped_column(Text, nullable=False)
    result_kind: Mapped[str] = mapped_column(Text, nullable=False)
    comparator_code: Mapped[str | None] = mapped_column(Text)
    target_value: Mapped[Decimal | None] = mapped_column(Numeric)
    target_min: Mapped[Decimal | None] = mapped_column(Numeric)
    target_max: Mapped[Decimal | None] = mapped_column(Numeric)
    unit_code: Mapped[str | None] = mapped_column(Text)
    presentation_order: Mapped[int] = mapped_column(Integer, nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    applied_evaluation_state_ref: Mapped[UUID | None] = mapped_column()
    applied_assessment_code: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        UniqueConstraint(
            "self_person_ref", "operation_id",
            name="uq_temporal_objective_definition_operation",
        ),
        ForeignKeyConstraint(
            ["objective_ref"], ["dante.temporal_objective.objective_ref"],
            name="fk_temporal_objective_definition_objective",
        ),
        ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_temporal_objective_definition_person",
        ),
        CheckConstraint("revision>=1", name="revision_positive"),
        CheckConstraint(
            "operation_id=btrim(operation_id) AND "
            "char_length(operation_id) BETWEEN 1 AND 200",
            name="revision_operation",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}", name="revision_fingerprint"),
        CheckConstraint(
            "result_kind IN ('boolean','quantity','qualitative','range')",
            name="revision_kind",
        ),
        CheckConstraint(
            "label=btrim(label) AND label<>'' AND "
            "char_length(label)<=300 AND presentation_order BETWEEN 0 AND 999",
            name="revision_label",
        ),
        CheckConstraint("isfinite(accepted_at)", name="revision_time"),
    )
", name="revision_fingerprint"),
        CheckConstraint(
            "result_kind IN ('boolean','quantity','qualitative','range')",
            name="revision_kind",
        ),
        CheckConstraint(
            "label=btrim(label) AND label<>'' AND "
            "char_length(label)<=300 AND presentation_order BETWEEN 0 AND 999",
            name="revision_label",
        ),
        CheckConstraint("isfinite(accepted_at)", name="revision_time"),
    )

class TemporalObjectiveSeriesEditRow(Base):
    __tablename__ = "temporal_objective_series_edit"

    self_person_ref: Mapped[UUID] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    source_native_ref: Mapped[UUID] = mapped_column(nullable=False)
    selected_objective_ref: Mapped[UUID] = mapped_column(nullable=False)
    selected_occurrence_ref: Mapped[UUID] = mapped_column(nullable=False)
    template_slot: Mapped[int] = mapped_column(Integer, nullable=False)
    revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    expected_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    expected_recurrence_state_ref: Mapped[UUID | None] = mapped_column()
    selected_definition_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    effective_zone_id: Mapped[str] = mapped_column(Text, nullable=False)
    anchor_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    label: Mapped[str] = mapped_column(Text, nullable=False)
    result_kind: Mapped[str] = mapped_column(Text, nullable=False)
    comparator_code: Mapped[str | None] = mapped_column(Text)
    target_value: Mapped[Decimal | None] = mapped_column(Numeric)
    target_min: Mapped[Decimal | None] = mapped_column(Numeric)
    target_max: Mapped[Decimal | None] = mapped_column(Numeric)
    unit_code: Mapped[str | None] = mapped_column(Text)
    presentation_order: Mapped[int] = mapped_column(Integer, nullable=False)
    applied_evaluation_state_ref: Mapped[UUID | None] = mapped_column()
    applied_assessment_code: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        UniqueConstraint(
            "source_native_ref", "template_slot", "revision",
            name="uq_temporal_objective_series_edit_revision",
        ),
        ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_temporal_objective_series_edit_person",
        ),
        ForeignKeyConstraint(
            ["source_native_ref"], ["dante.native_address.native_ref"],
            name="fk_temporal_objective_series_edit_source",
        ),
        ForeignKeyConstraint(
            ["selected_objective_ref"], ["dante.temporal_objective.objective_ref"],
            name="fk_temporal_objective_series_edit_objective",
        ),
        ForeignKeyConstraint(
            ["selected_occurrence_ref"], ["dante.occurrence.occurrence_ref"],
            name="fk_temporal_objective_series_edit_occurrence",
        ),
        CheckConstraint(
            "template_slot BETWEEN 0 AND 99 AND revision>=1 "
            "AND expected_revision>=0 AND selected_definition_revision>=1",
            name="revision",
        ),
        CheckConstraint(
            "operation_id=btrim(operation_id) AND "
            "char_length(operation_id) BETWEEN 1 AND 200",
            name="operation",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}", name="fingerprint"),
        CheckConstraint(
            "label=btrim(label) AND label<>'' "
            "AND char_length(label)<=300 AND presentation_order BETWEEN 0 AND 999",
            name="label",
        ),
    )
", name="fingerprint"),
        CheckConstraint(
            "label=btrim(label) AND label<>'' "
            "AND char_length(label)<=300 AND presentation_order BETWEEN 0 AND 999",
            name="label",
        ),
    )
