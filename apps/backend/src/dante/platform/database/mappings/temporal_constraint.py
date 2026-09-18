"""SQLAlchemy row mappings for the B04-A Temporal Constraint canonical core."""

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
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef


class TemporalConstraintRow(Base):
    """Stable scoped identity for one independently revisable Temporal Constraint."""

    __tablename__ = "temporal_constraint"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(constraint_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        ForeignKeyConstraint(
            ["subject_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_temporal_constraint_subject_native_ref_native_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint(
            "constraint_ref",
            "subject_native_ref",
            name="uq_temporal_constraint_ref_subject",
        ),
        Index("ix_temporal_constraint_subject_native_ref", "subject_native_ref"),
    )

    constraint_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    subject_native_ref: Mapped[NativeRef] = mapped_column(nullable=False)


class TemporalConstraintStateRow(Base):
    """Immutable MaterialState envelope for one typed Temporal Constraint rule."""

    __tablename__ = "temporal_constraint_state"
    __table_args__ = (
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_temporal_constraint_state_material_state_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["constraint_ref"],
            ["dante.temporal_constraint.constraint_ref"],
            name="fk_temporal_constraint_state_constraint_ref_temporal_constraint",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint(
            "constraint_ref",
            "material_state_ref",
            name="uq_temporal_constraint_state_constraint_material",
        ),
        CheckConstraint("family_code='boundary'", name="family"),
        CheckConstraint("strength_code IN ('hard','soft')", name="strength"),
        CheckConstraint(
            "constrained_facet_code='schedule.start'",
            name="constrained_facet",
        ),
        Index("ix_temporal_constraint_state_constraint_ref", "constraint_ref"),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    constraint_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    family_code: Mapped[str] = mapped_column(Text, nullable=False)
    strength_code: Mapped[str] = mapped_column(Text, nullable=False)
    constrained_facet_code: Mapped[str] = mapped_column(Text, nullable=False)


class TemporalConstraintBoundaryStateRow(Base):
    """Typed B04-A boundary-rule discriminator."""

    __tablename__ = "temporal_constraint_boundary_state"
    __table_args__ = (
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.temporal_constraint_state.material_state_ref"],
            name="fk_temporal_constraint_boundary_state_constraint_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        CheckConstraint("boundary_kind_code='earliest_start'", name="kind"),
        CheckConstraint("temporal_form_code='absolute'", name="temporal_form"),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    boundary_kind_code: Mapped[str] = mapped_column(Text, nullable=False)
    temporal_form_code: Mapped[str] = mapped_column(Text, nullable=False)


class TemporalConstraintBoundaryAbsoluteStateRow(Base):
    """Absolute-instant value for the first complete B04-A boundary rule."""

    __tablename__ = "temporal_constraint_boundary_absolute_state"
    __table_args__ = (
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.temporal_constraint_boundary_state.material_state_ref"],
            name="fk_temporal_constraint_boundary_absolute_state_boundary_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        CheckConstraint("isfinite(boundary_at)", name="finite"),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    boundary_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class TemporalConstraintCurrentHistoryRow(Base):
    """Append-retained currentness episodes for one Temporal Constraint."""

    __tablename__ = "temporal_constraint_current_history"
    __table_args__ = (
        ForeignKeyConstraint(
            ["constraint_ref", "material_state_ref"],
            [
                "dante.temporal_constraint_state.constraint_ref",
                "dante.temporal_constraint_state.material_state_ref",
            ],
            name="fk_temporal_constraint_current_history_constraint_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at > current_from_at))",
            name="interval",
        ),
        Index(
            "ux_temporal_constraint_current_history_open",
            "constraint_ref",
            unique=True,
            postgresql_where=text("current_until_at IS NULL"),
        ),
        Index(
            "ix_temporal_constraint_current_history_material_state_ref",
            "material_state_ref",
        ),
    )

    constraint_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    current_from_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        primary_key=True,
    )
    current_until_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class TemporalConstraintMutationOperationRow(Base):
    """Immutable idempotency receipt for B04-A create/revise/retire effects."""

    __tablename__ = "temporal_constraint_mutation_operation"
    __table_args__ = (
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_temporal_constraint_mutation_operation_self_person_ref_person",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["constraint_ref", "subject_native_ref"],
            [
                "dante.temporal_constraint.constraint_ref",
                "dante.temporal_constraint.subject_native_ref",
            ],
            name="fk_temporal_constraint_mutation_operation_constraint_subject",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["constraint_ref", "expected_material_state_ref"],
            [
                "dante.temporal_constraint_state.constraint_ref",
                "dante.temporal_constraint_state.material_state_ref",
            ],
            name="fk_temporal_constraint_mutation_operation_expected_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["constraint_ref", "resulting_material_state_ref"],
            [
                "dante.temporal_constraint_state.constraint_ref",
                "dante.temporal_constraint_state.material_state_ref",
            ],
            name="fk_temporal_constraint_mutation_operation_resulting_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name="fingerprint",
        ),
        CheckConstraint(
            "mutation_kind IN ('create','revise','retire')",
            name="kind",
        ),
        CheckConstraint(
            "(mutation_kind='create' AND expected_material_state_ref IS NULL "
            "AND resulting_material_state_ref IS NOT NULL) OR "
            "(mutation_kind='revise' AND expected_material_state_ref IS NOT NULL "
            "AND resulting_material_state_ref IS NOT NULL) OR "
            "(mutation_kind='retire' AND expected_material_state_ref IS NOT NULL "
            "AND resulting_material_state_ref IS NULL)",
            name="state_shape",
        ),
        Index(
            "ix_temporal_constraint_mutation_operation_constraint_ref",
            "constraint_ref",
        ),
        Index(
            "ux_temporal_constraint_mutation_operation_resulting_state",
            "resulting_material_state_ref",
            unique=True,
            postgresql_where=text("resulting_material_state_ref IS NOT NULL"),
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    mutation_kind: Mapped[str] = mapped_column(Text, nullable=False)
    constraint_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    subject_native_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    expected_material_state_ref: Mapped[MaterialStateRef | None] = mapped_column(nullable=True)
    resulting_material_state_ref: Mapped[MaterialStateRef | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
