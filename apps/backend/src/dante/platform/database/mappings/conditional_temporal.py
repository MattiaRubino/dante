"""SQLAlchemy row mappings for the B11-B conditional temporal family."""

from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKeyConstraint, Index, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef


class ConditionalTemporalIntentRow(Base):
    """Stable self-scoped Condition intent; operation id is not its identity."""

    __tablename__ = "conditional_temporal_intent"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(condition_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint(
            "subject_family IN ('activity','event','occurrence')",
            name="subject_family",
        ),
        CheckConstraint(
            "family_code='actual_realization'",
            name="family",
        ),
        CheckConstraint("isfinite(created_at)", name="created_at"),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_conditional_temporal_intent_person",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["subject_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_conditional_temporal_intent_subject",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint(
            "self_person_ref",
            "subject_native_ref",
            "family_code",
            name="uq_conditional_temporal_intent_subject_family",
        ),
        Index(
            "ix_conditional_temporal_intent_subject",
            "self_person_ref",
            "subject_family",
            "subject_native_ref",
        ),
    )

    condition_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    self_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    subject_family: Mapped[str] = mapped_column(Text, nullable=False)
    subject_native_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    family_code: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ConditionalTemporalEvaluationRow(Base):
    """Immutable condition evaluation pinned to exact Actual evidence when known."""

    __tablename__ = "conditional_temporal_evaluation"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(evaluation_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint(
            "result_code IN ('satisfied','not_satisfied','indeterminate')",
            name="result",
        ),
        CheckConstraint(
            "(result_code='satisfied' AND disposition_code='allow') OR "
            "(result_code IN ('not_satisfied','indeterminate') AND disposition_code='withhold')",
            name="disposition",
        ),
        CheckConstraint(
            "(result_code='indeterminate' AND actual_ref IS NULL AND "
            "actual_realization_material_state_ref IS NULL) OR "
            "(result_code<>'indeterminate' AND actual_ref IS NOT NULL AND "
            "actual_realization_material_state_ref IS NOT NULL)",
            name="evidence_shape",
        ),
        CheckConstraint("isfinite(evaluated_at)", name="evaluated_at"),
        ForeignKeyConstraint(
            ["condition_ref"],
            ["dante.conditional_temporal_intent.condition_ref"],
            name="fk_conditional_temporal_evaluation_condition",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["actual_ref"],
            ["dante.actual.actual_ref"],
            name="fk_conditional_temporal_evaluation_actual",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["actual_realization_material_state_ref"],
            ["dante.actual_realization_state.material_state_ref"],
            name="fk_conditional_temporal_evaluation_actual_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ix_conditional_temporal_evaluation_condition_time",
            "condition_ref",
            "evaluated_at",
            "evaluation_ref",
        ),
        Index(
            "ix_conditional_temporal_evaluation_actual_state",
            "actual_realization_material_state_ref",
        ),
    )

    evaluation_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    condition_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    result_code: Mapped[str] = mapped_column(Text, nullable=False)
    disposition_code: Mapped[str] = mapped_column(Text, nullable=False)
    actual_ref: Mapped[ScopedRecordRef | None] = mapped_column(nullable=True)
    actual_realization_material_state_ref: Mapped[MaterialStateRef | None] = mapped_column(
        nullable=True
    )
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ConditionalTemporalOperationRow(Base):
    """Immutable create/evaluate idempotency receipt."""

    __tablename__ = "conditional_temporal_operation"
    __table_args__ = (
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        CheckConstraint("operation_kind IN ('create','evaluate')", name="kind"),
        CheckConstraint(
            "(operation_kind='create' AND evaluation_ref IS NULL) OR "
            "(operation_kind='evaluate' AND evaluation_ref IS NOT NULL)",
            name="result_shape",
        ),
        CheckConstraint("isfinite(created_at)", name="created_at"),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_conditional_temporal_operation_person",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["condition_ref"],
            ["dante.conditional_temporal_intent.condition_ref"],
            name="fk_conditional_temporal_operation_condition",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["evaluation_ref"],
            ["dante.conditional_temporal_evaluation.evaluation_ref"],
            name="fk_conditional_temporal_operation_evaluation",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint(
            "evaluation_ref",
            name="uq_conditional_temporal_operation_evaluation",
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    operation_kind: Mapped[str] = mapped_column(Text, nullable=False)
    condition_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    evaluation_ref: Mapped[ScopedRecordRef | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
