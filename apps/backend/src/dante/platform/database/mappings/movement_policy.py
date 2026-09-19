"""SQLAlchemy row mappings for the B04-D Schedule Movement Policy core."""

from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKeyConstraint, Index, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef


class ScheduleMovementPolicyStateRow(Base):
    """Immutable MaterialState for self-governed accepted-Schedule movement."""

    __tablename__ = "schedule_movement_policy_state"
    __table_args__ = (
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_schedule_movement_policy_state_material_state_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["schedule_ref"],
            ["dante.schedule.schedule_ref"],
            name="fk_schedule_movement_policy_state_schedule",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint(
            "schedule_ref",
            "material_state_ref",
            name="uq_schedule_movement_policy_state_schedule_material",
        ),
        CheckConstraint(
            "automatic_movement_code IN ('blocked','automatic')",
            name="automatic_movement",
        ),
        CheckConstraint(
            "acceptance_path_code IN ('direct','confirmation_required')",
            name="acceptance_path",
        ),
        CheckConstraint(
            "automatic_movement_code='automatic' OR acceptance_path_code='direct'",
            name="blocked_shape",
        ),
        Index("ix_schedule_movement_policy_state_schedule_ref", "schedule_ref"),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    schedule_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    automatic_movement_code: Mapped[str] = mapped_column(Text, nullable=False)
    acceptance_path_code: Mapped[str] = mapped_column(Text, nullable=False)


class ScheduleMovementPolicyCurrentHistoryRow(Base):
    """Append-retained currentness episodes for one Schedule Movement Policy."""

    __tablename__ = "schedule_movement_policy_current_history"
    __table_args__ = (
        ForeignKeyConstraint(
            ["schedule_ref", "material_state_ref"],
            [
                "dante.schedule_movement_policy_state.schedule_ref",
                "dante.schedule_movement_policy_state.material_state_ref",
            ],
            name="fk_schedule_movement_policy_current_history_state",
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
            "ux_schedule_movement_policy_current_history_open",
            "schedule_ref",
            unique=True,
            postgresql_where=text("current_until_at IS NULL"),
        ),
        Index(
            "ix_schedule_movement_policy_current_history_material_state_ref",
            "material_state_ref",
        ),
    )

    schedule_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    current_from_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    current_until_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ScheduleMovementPolicyMutationOperationRow(Base):
    """Immutable idempotency receipt for create/revise/retire policy effects."""

    __tablename__ = "schedule_movement_policy_mutation_operation"
    __table_args__ = (
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_schedule_movement_policy_mutation_operation_self_person",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["schedule_ref"],
            ["dante.schedule.schedule_ref"],
            name="fk_schedule_movement_policy_mutation_operation_schedule",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["schedule_ref", "expected_material_state_ref"],
            [
                "dante.schedule_movement_policy_state.schedule_ref",
                "dante.schedule_movement_policy_state.material_state_ref",
            ],
            name="fk_schedule_movement_policy_mutation_operation_expected_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["schedule_ref", "resulting_material_state_ref"],
            [
                "dante.schedule_movement_policy_state.schedule_ref",
                "dante.schedule_movement_policy_state.material_state_ref",
            ],
            name="fk_schedule_movement_policy_mutation_operation_resulting_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        CheckConstraint("mutation_kind IN ('create','revise','retire')", name="kind"),
        CheckConstraint(
            "(mutation_kind='create' AND expected_material_state_ref IS NULL "
            "AND resulting_material_state_ref IS NOT NULL "
            "AND automatic_movement_code IS NOT NULL AND acceptance_path_code IS NOT NULL) OR "
            "(mutation_kind='revise' AND expected_material_state_ref IS NOT NULL "
            "AND resulting_material_state_ref IS NOT NULL "
            "AND automatic_movement_code IS NOT NULL AND acceptance_path_code IS NOT NULL) OR "
            "(mutation_kind='retire' AND expected_material_state_ref IS NOT NULL "
            "AND resulting_material_state_ref IS NULL "
            "AND automatic_movement_code IS NULL AND acceptance_path_code IS NULL)",
            name="shape",
        ),
        Index("ix_schedule_movement_policy_mutation_operation_schedule_ref", "schedule_ref"),
        Index(
            "ux_schedule_movement_policy_mutation_operation_resulting_state",
            "resulting_material_state_ref",
            unique=True,
            postgresql_where=text("resulting_material_state_ref IS NOT NULL"),
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    mutation_kind: Mapped[str] = mapped_column(Text, nullable=False)
    schedule_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    expected_material_state_ref: Mapped[MaterialStateRef | None] = mapped_column(nullable=True)
    resulting_material_state_ref: Mapped[MaterialStateRef | None] = mapped_column(nullable=True)
    automatic_movement_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    acceptance_path_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
