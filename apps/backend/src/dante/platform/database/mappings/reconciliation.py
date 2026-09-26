"""SQLAlchemy row mappings for the B10-D Outcome reconciliation family."""

from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKeyConstraint, Index, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef


class OutcomeReconciliationRow(Base):
    """Stable reconciliation owner for one Outcome state and one purpose."""

    __tablename__ = "outcome_reconciliation"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(reconciliation_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint(
            "purpose_code=btrim(purpose_code) AND purpose_code<>'' "
            "AND char_length(purpose_code)<=120 "
            "AND purpose_code ~ '^[a-z0-9][a-z0-9._:-]*$'",
            name="purpose",
        ),
        UniqueConstraint(
            "outcome_disposition_material_state_ref",
            "purpose_code",
            name="uq_outcome_reconciliation_target_purpose",
        ),
        UniqueConstraint(
            "reconciliation_ref",
            "outcome_ref",
            name="uq_outcome_reconciliation_ref_outcome",
        ),
        UniqueConstraint(
            "reconciliation_ref",
            "outcome_ref",
            "outcome_disposition_material_state_ref",
            "purpose_code",
            name="uq_outcome_reconciliation_identity",
        ),
        ForeignKeyConstraint(
            ["outcome_ref"],
            ["dante.outcome.outcome_ref"],
            name="fk_outcome_reconciliation_outcome",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["outcome_ref", "outcome_disposition_material_state_ref"],
            [
                "dante.outcome_disposition_state.outcome_ref",
                "dante.outcome_disposition_state.material_state_ref",
            ],
            name="fk_outcome_reconciliation_outcome_disposition",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index("ix_outcome_reconciliation_outcome_ref", "outcome_ref"),
    )

    reconciliation_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    outcome_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    outcome_disposition_material_state_ref: Mapped[MaterialStateRef] = mapped_column(
        nullable=False
    )
    purpose_code: Mapped[str] = mapped_column(Text, nullable=False)


class OutcomeReconciliationStateRow(Base):
    """Immutable accepted reconciliation action for one reconciliation owner."""

    __tablename__ = "outcome_reconciliation_state"
    __table_args__ = (
        CheckConstraint(
            "action_code IN ('unresolved','select','accept_multiple','defer','escalate')",
            name="action",
        ),
        UniqueConstraint(
            "reconciliation_ref",
            "material_state_ref",
            name="uq_outcome_reconciliation_state_owner_material",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_outcome_reconciliation_state_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["reconciliation_ref"],
            ["dante.outcome_reconciliation.reconciliation_ref"],
            name="fk_outcome_reconciliation_state_owner",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["resolved_by_person_ref"],
            ["dante.person.person_ref"],
            name="fk_outcome_reconciliation_state_resolver",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index("ix_outcome_reconciliation_state_owner", "reconciliation_ref"),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    reconciliation_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    action_code: Mapped[str] = mapped_column(Text, nullable=False)
    resolved_by_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)


class OutcomeReconciliationEvidenceRow(Base):
    """Exact Confirmation attestation MaterialState pinned as reconciliation evidence."""

    __tablename__ = "outcome_reconciliation_evidence"
    __table_args__ = (
        CheckConstraint("role_code IN ('considered','selected')", name="role"),
        ForeignKeyConstraint(
            ["reconciliation_ref", "reconciliation_material_state_ref"],
            [
                "dante.outcome_reconciliation_state.reconciliation_ref",
                "dante.outcome_reconciliation_state.material_state_ref",
            ],
            name="fk_outcome_reconciliation_evidence_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["confirmation_ref", "confirmation_attestation_material_state_ref"],
            [
                "dante.confirmation_attestation_state.confirmation_ref",
                "dante.confirmation_attestation_state.material_state_ref",
            ],
            name="fk_outcome_reconciliation_evidence_confirmation_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ix_outcome_reconciliation_evidence_confirmation_state",
            "confirmation_attestation_material_state_ref",
        ),
    )

    reconciliation_material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    confirmation_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    confirmation_attestation_material_state_ref: Mapped[MaterialStateRef] = mapped_column(
        primary_key=True
    )
    reconciliation_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    role_code: Mapped[str] = mapped_column(Text, nullable=False)


class OutcomeReconciliationCurrentHistoryRow(Base):
    """Explicit accepted-current history for reconciliation state."""

    __tablename__ = "outcome_reconciliation_current_history"
    __table_args__ = (
        CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at>current_from_at))",
            name="interval",
        ),
        ForeignKeyConstraint(
            ["reconciliation_ref", "material_state_ref"],
            [
                "dante.outcome_reconciliation_state.reconciliation_ref",
                "dante.outcome_reconciliation_state.material_state_ref",
            ],
            name="fk_outcome_reconciliation_current_history_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ux_outcome_reconciliation_current_history_open",
            "reconciliation_ref",
            unique=True,
            postgresql_where=text("current_until_at IS NULL"),
        ),
        Index(
            "ix_outcome_reconciliation_current_history_material_state_ref",
            "material_state_ref",
        ),
    )

    reconciliation_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    current_from_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    current_until_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class OutcomeReconciliationOperationRow(Base):
    """Immutable idempotency receipt; operation id is never reconciliation identity."""

    __tablename__ = "outcome_reconciliation_operation"
    __table_args__ = (
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_outcome_reconciliation_operation_self_person",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            [
                "reconciliation_ref",
                "outcome_ref",
                "outcome_disposition_material_state_ref",
                "purpose_code",
            ],
            [
                "dante.outcome_reconciliation.reconciliation_ref",
                "dante.outcome_reconciliation.outcome_ref",
                "dante.outcome_reconciliation.outcome_disposition_material_state_ref",
                "dante.outcome_reconciliation.purpose_code",
            ],
            name="fk_outcome_reconciliation_operation_identity",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["reconciliation_ref", "expected_material_state_ref"],
            [
                "dante.outcome_reconciliation_state.reconciliation_ref",
                "dante.outcome_reconciliation_state.material_state_ref",
            ],
            name="fk_outcome_reconciliation_operation_expected_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["reconciliation_ref", "resulting_material_state_ref"],
            [
                "dante.outcome_reconciliation_state.reconciliation_ref",
                "dante.outcome_reconciliation_state.material_state_ref",
            ],
            name="fk_outcome_reconciliation_operation_resulting_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint(
            "resulting_material_state_ref",
            name="uq_outcome_reconciliation_operation_resulting_state",
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    reconciliation_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    outcome_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    outcome_disposition_material_state_ref: Mapped[MaterialStateRef] = mapped_column(
        nullable=False
    )
    purpose_code: Mapped[str] = mapped_column(Text, nullable=False)
    expected_material_state_ref: Mapped[MaterialStateRef | None] = mapped_column(nullable=True)
    resulting_material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
