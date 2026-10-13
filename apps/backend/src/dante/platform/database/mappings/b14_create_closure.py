"""SQLAlchemy row mappings for B14 Create-closure persistence families."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    Numeric,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import conv

from dante.platform.database.metadata import Base


class RoutineOccurrencePolicyRow(Base):
    __tablename__ = "routine_occurrence_policy"

    __table_args__ = (
        CheckConstraint("duration_minutes BETWEEN 1 AND 525600", name=conv("ck_routine_occurrence_policy_ck_routine_occurrence_poli_a9a0")),
        CheckConstraint("reminder_lead_minutes IS NULL OR reminder_lead_minutes BETWEEN 0 AND 10080", name=conv("ck_routine_occurrence_policy_ck_routine_occurrence_poli_3020")),
        CheckConstraint("jsonb_typeof(activity_template)='object'", name=conv("ck_routine_occurrence_policy_ck_routine_occurrence_poli_3426")),
        ForeignKeyConstraint(["self_person_ref"], ["dante.person.person_ref"], name="fk_routine_occurrence_policy_person", match="SIMPLE", onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False),
        ForeignKeyConstraint(["routine_ref"], ["dante.routine.routine_ref"], name="fk_routine_occurrence_policy_routine", match="SIMPLE", onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False),
        Index("ix_routine_occurrence_policy_routine", "routine_ref", unique=False),
    )

    self_person_ref: Mapped[UUID] = mapped_column(primary_key=True)
    routine_ref: Mapped[UUID] = mapped_column(primary_key=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    reminder_lead_minutes: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    activity_template: Mapped[dict[str, object]] = mapped_column(
        JSONB, nullable=False, server_default=text("'{}'::jsonb")
    )


class SchedulePlacementLockRow(Base):
    __tablename__ = "schedule_placement_lock"

    __table_args__ = (
        CheckConstraint("revision >= 1", name=conv("ck_schedule_placement_lock_ck_schedule_placement_lock_revision")),
        ForeignKeyConstraint(["schedule_ref"], ["dante.schedule.schedule_ref"], name="fk_schedule_placement_lock_schedule", match="SIMPLE", onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False),
        ForeignKeyConstraint(["self_person_ref"], ["dante.person.person_ref"], name="fk_schedule_placement_lock_person", match="SIMPLE", onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False),
    )

    schedule_ref: Mapped[UUID] = mapped_column(primary_key=True)
    self_person_ref: Mapped[UUID] = mapped_column(nullable=False)
    locked: Mapped[bool] = mapped_column(Boolean, nullable=False)
    revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RoutineOccurrenceActivityInstanceRow(Base):
    __tablename__ = "routine_occurrence_activity_instance"

    __table_args__ = (
        ForeignKeyConstraint(["occurrence_ref"], ["dante.occurrence.occurrence_ref"], name="fk_routine_occurrence_activity_instance_occurrence", match="SIMPLE", onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False),
        ForeignKeyConstraint(["activity_ref"], ["dante.activity_intention.activity_ref"], name="fk_routine_occurrence_activity_instance_activity", match="SIMPLE", onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False),
        ForeignKeyConstraint(["self_person_ref"], ["dante.person.person_ref"], name="fk_routine_occurrence_activity_instance_person", match="SIMPLE", onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False),
        UniqueConstraint("activity_ref", name="uq_routine_occurrence_activity_instance_activity"),
    )

    occurrence_ref: Mapped[UUID] = mapped_column(primary_key=True)
    activity_ref: Mapped[UUID] = mapped_column(nullable=False)
    self_person_ref: Mapped[UUID] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EventOccurrencePolicyRow(Base):
    __tablename__ = "event_occurrence_policy"

    __table_args__ = (
        CheckConstraint("placement_kind IN ('timed','all_day')", name=conv("ck_event_occurrence_policy_ck_event_occurrence_policy_p_04ad")),
        CheckConstraint("(placement_kind='timed' AND duration_minutes BETWEEN 1 AND 525600 AND duration_days IS NULL) OR (placement_kind='all_day' AND duration_days BETWEEN 1 AND 3660 AND duration_minutes IS NULL AND reminder_lead_minutes IS NULL)", name=conv("ck_event_occurrence_policy_ck_event_occurrence_policy_duration")),
        CheckConstraint("reminder_lead_minutes IS NULL OR reminder_lead_minutes BETWEEN 0 AND 10080", name=conv("ck_event_occurrence_policy_ck_event_occurrence_policy_reminder")),
        CheckConstraint("reality_mode IN ('manual','review_on_end','auto_confirm_outcome')", name=conv("ck_event_occurrence_policy_ck_event_occurrence_policy_r_afc5")),
        CheckConstraint("jsonb_typeof(objectives)='array'", name=conv("ck_event_occurrence_policy_ck_event_occurrence_policy_o_9019")),
        ForeignKeyConstraint(["self_person_ref"], ["dante.person.person_ref"], name="fk_event_occurrence_policy_person", match="SIMPLE", onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False),
        ForeignKeyConstraint(["event_ref"], ["dante.event_expectation.event_ref"], name="fk_event_occurrence_policy_event", match="SIMPLE", onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False),
        Index("ix_event_occurrence_policy_event", "event_ref", unique=False),
    )

    self_person_ref: Mapped[UUID] = mapped_column(primary_key=True)
    event_ref: Mapped[UUID] = mapped_column(primary_key=True)
    placement_kind: Mapped[str] = mapped_column(Text, nullable=False)
    duration_minutes: Mapped[int | None] = mapped_column(Integer)
    duration_days: Mapped[int | None] = mapped_column(Integer)
    reminder_lead_minutes: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    reality_mode: Mapped[str] = mapped_column(
        Text, nullable=False, server_default=text("'manual'")
    )
    objectives: Mapped[list[dict[str, object]]] = mapped_column(
        JSONB, nullable=False, server_default=text("'[]'::jsonb")
    )


class RealityReviewPolicyRow(Base):
    __tablename__ = "reality_review_policy"

    __table_args__ = (
        CheckConstraint("subject_kind IN ('activity','event','occurrence')", name=conv("ck_reality_review_policy_ck_reality_review_policy_subject_kind")),
        ForeignKeyConstraint(["self_person_ref"], ["dante.person.person_ref"], name="fk_reality_review_policy_person", match="SIMPLE", onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False),
        Index("ix_reality_review_policy_self", "self_person_ref", "subject_kind", unique=False),
    )

    subject_kind: Mapped[str] = mapped_column(Text, primary_key=True)
    subject_native_ref: Mapped[UUID] = mapped_column(primary_key=True)
    self_person_ref: Mapped[UUID] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RealityReviewPolicyStateRow(Base):
    __tablename__ = "reality_review_policy_state"

    __table_args__ = (
        CheckConstraint("uuid_extract_version(state_ref) IS NOT DISTINCT FROM 7", name=conv("ck_reality_review_policy_state_ck_reality_review_policy_9aac")),
        CheckConstraint("mode_code IN ('manual','review_on_end','auto_confirm_outcome')", name=conv("ck_reality_review_policy_state_ck_reality_review_policy_f186")),
        CheckConstraint("isfinite(recorded_at)", name=conv("ck_reality_review_policy_state_ck_reality_review_policy_cb4e")),
        ForeignKeyConstraint(["subject_kind", "subject_native_ref"], ["dante.reality_review_policy.subject_kind", "dante.reality_review_policy.subject_native_ref"], name="fk_reality_review_policy_state_owner", match="SIMPLE", onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False),
        UniqueConstraint("subject_kind", "subject_native_ref", "state_ref", name="uq_reality_review_policy_state_owner"),
    )

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
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    retirement_operation_id: Mapped[str | None] = mapped_column(Text)
    retirement_fingerprint: Mapped[str | None] = mapped_column(Text)


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
        CheckConstraint("revision>=1", name="positive"),
        CheckConstraint(
            "operation_id=btrim(operation_id) AND "
            "char_length(operation_id) BETWEEN 1 AND 200",
            name="operation",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        CheckConstraint(
            "result_kind IN ('boolean','quantity','qualitative','range')",
            name="kind",
        ),
        CheckConstraint(
            "label=btrim(label) AND label<>'' AND "
            "char_length(label)<=300 AND presentation_order BETWEEN 0 AND 999",
            name="label",
        ),
        CheckConstraint("isfinite(accepted_at)", name="time"),
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
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        CheckConstraint(
            "label=btrim(label) AND label<>'' "
            "AND char_length(label)<=300 AND presentation_order BETWEEN 0 AND 999",
            name="label",
        ),
    )
