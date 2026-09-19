"""SQLAlchemy mappings for governed B04-D Schedule movement."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKeyConstraint, Index, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef


class ScheduleMoveProposalRow(Base):
    """Immutable confirmation proposal; it is not an accepted Schedule effect."""

    __tablename__ = "schedule_move_proposal"
    __table_args__ = (
        ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_schedule_move_proposal_self_person", match="SIMPLE",
            onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False,
        ),
        ForeignKeyConstraint(
            ["schedule_ref"], ["dante.schedule.schedule_ref"],
            name="fk_schedule_move_proposal_schedule", match="SIMPLE",
            onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False,
        ),
        ForeignKeyConstraint(
            ["expected_placement_material_state_ref"],
            ["dante.schedule_placement_state.material_state_ref"],
            name="fk_schedule_move_proposal_expected_placement", match="SIMPLE",
            onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False,
        ),
        ForeignKeyConstraint(
            ["schedule_ref", "movement_policy_material_state_ref"],
            [
                "dante.schedule_movement_policy_state.schedule_ref",
                "dante.schedule_movement_policy_state.material_state_ref",
            ],
            name="fk_schedule_move_proposal_policy_state", match="SIMPLE",
            onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False,
        ),
        CheckConstraint("uuid_extract_version(proposal_ref) IS NOT DISTINCT FROM 7", name="uuidv7"),
        CheckConstraint(
            "isfinite(starts_at) AND isfinite(ends_at) AND ends_at > starts_at",
            name="interval",
        ),
        CheckConstraint("isfinite(created_at)", name="created_at"),
        Index("ix_schedule_move_proposal_schedule_ref", "schedule_ref"),
    )

    proposal_ref: Mapped[UUID] = mapped_column(primary_key=True)
    self_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    schedule_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    expected_placement_material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    movement_policy_material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ScheduleMoveRequestOperationRow(Base):
    """Idempotency receipt for direct commit or pending-confirmation request."""

    __tablename__ = "schedule_move_request_operation"
    __table_args__ = (
        ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_schedule_move_request_operation_self_person", match="SIMPLE",
            onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False,
        ),
        ForeignKeyConstraint(
            ["schedule_ref"], ["dante.schedule.schedule_ref"],
            name="fk_schedule_move_request_operation_schedule", match="SIMPLE",
            onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False,
        ),
        ForeignKeyConstraint(
            ["expected_placement_material_state_ref"],
            ["dante.schedule_placement_state.material_state_ref"],
            name="fk_schedule_move_request_operation_expected_placement", match="SIMPLE",
            onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False,
        ),
        ForeignKeyConstraint(
            ["schedule_ref", "movement_policy_material_state_ref"],
            [
                "dante.schedule_movement_policy_state.schedule_ref",
                "dante.schedule_movement_policy_state.material_state_ref",
            ],
            name="fk_schedule_move_request_operation_policy_state", match="SIMPLE",
            onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False,
        ),
        ForeignKeyConstraint(
            ["proposal_ref"], ["dante.schedule_move_proposal.proposal_ref"],
            name="fk_schedule_move_request_operation_proposal", match="SIMPLE",
            onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False,
        ),
        ForeignKeyConstraint(
            ["resulting_placement_material_state_ref"],
            ["dante.schedule_placement_state.material_state_ref"],
            name="fk_schedule_move_request_operation_resulting_placement", match="SIMPLE",
            onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False,
        ),
        UniqueConstraint("proposal_ref", name="uq_schedule_move_request_operation_proposal_ref"),
        UniqueConstraint(
            "resulting_placement_material_state_ref",
            name="uq_schedule_move_request_operation_resulting_placement",
        ),
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        CheckConstraint(
            "isfinite(starts_at) AND isfinite(ends_at) AND ends_at > starts_at",
            name="interval",
        ),
        CheckConstraint(
            "(result_kind='committed' AND proposal_ref IS NULL AND resulting_placement_material_state_ref IS NOT NULL) OR "
            "(result_kind='pending_confirmation' AND proposal_ref IS NOT NULL AND resulting_placement_material_state_ref IS NULL)",
            name="result_shape",
        ),
        Index("ix_schedule_move_request_operation_schedule_ref", "schedule_ref"),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    schedule_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    expected_placement_material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    movement_policy_material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    result_kind: Mapped[str] = mapped_column(Text, nullable=False)
    proposal_ref: Mapped[UUID | None] = mapped_column(nullable=True)
    resulting_placement_material_state_ref: Mapped[MaterialStateRef | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ScheduleMoveAcceptOperationRow(Base):
    """Receipt proving one proposal was explicitly accepted into Schedule truth."""

    __tablename__ = "schedule_move_accept_operation"
    __table_args__ = (
        ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_schedule_move_accept_operation_self_person", match="SIMPLE",
            onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False,
        ),
        ForeignKeyConstraint(
            ["proposal_ref"], ["dante.schedule_move_proposal.proposal_ref"],
            name="fk_schedule_move_accept_operation_proposal", match="SIMPLE",
            onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False,
        ),
        ForeignKeyConstraint(
            ["schedule_ref"], ["dante.schedule.schedule_ref"],
            name="fk_schedule_move_accept_operation_schedule", match="SIMPLE",
            onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False,
        ),
        ForeignKeyConstraint(
            ["resulting_placement_material_state_ref"],
            ["dante.schedule_placement_state.material_state_ref"],
            name="fk_schedule_move_accept_operation_resulting_placement", match="SIMPLE",
            onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False,
        ),
        UniqueConstraint("proposal_ref", name="uq_schedule_move_accept_operation_proposal_ref"),
        UniqueConstraint(
            "resulting_placement_material_state_ref",
            name="uq_schedule_move_accept_operation_resulting_placement",
        ),
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    proposal_ref: Mapped[UUID] = mapped_column(nullable=False)
    schedule_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    resulting_placement_material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
