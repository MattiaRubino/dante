"""Inert temporal draft configurations; these rows are not Activities or Events."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Index, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base


class TemporalDraftVaultRow(Base):
    __tablename__ = "temporal_draft_vault"
    __table_args__ = (
        CheckConstraint("subject_kind IN ('activity','event')", name="kind"),
        CheckConstraint("length(title) <= 300", name="title"),
        CheckConstraint(
            "jsonb_typeof(payload) = 'object' AND octet_length(payload::text) <= 131072",
            name="payload",
        ),
        CheckConstraint("revision >= 1", name="revision"),
    )

    draft_ref: Mapped[UUID] = mapped_column(primary_key=True)
    owner_person_ref: Mapped[UUID] = mapped_column(nullable=False)
    subject_kind: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    revision: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("1"))
    last_operation_id: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("clock_timestamp()"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("clock_timestamp()"),
    )


class TemporalObjectiveInputDraftRow(Base):
    """Owned, provisional Objective value: never canonical Observation until confirmed."""

    __tablename__ = "temporal_objective_input_draft"
    __table_args__ = (
        CheckConstraint(
            "jsonb_typeof(payload)='object' AND octet_length(payload::text)<=4096",
            name="payload",
        ),
        CheckConstraint("revision>=1", name="revision"),
        CheckConstraint(
            "(confirmed_at IS NULL AND confirmed_operation_id IS NULL AND "
            "observation_ref IS NULL AND evaluation_state_ref IS NULL AND "
            "assessment_code IS NULL) OR "
            "(confirmed_at IS NOT NULL AND confirmed_operation_id IS NOT NULL AND "
            "observation_ref IS NOT NULL AND evaluation_state_ref IS NOT NULL AND "
            "assessment_code IS NOT NULL)",
            name="confirmed",
        ),
        Index(
            "ix_temporal_objective_input_draft_owner",
            "owner_person_ref", text("updated_at DESC"), "objective_ref",
        ),
    )

    objective_ref: Mapped[UUID] = mapped_column(
        ForeignKey(
            "dante.temporal_objective.objective_ref",
            name="fk_temporal_objective_input_draft_objective",
        ), primary_key=True,
    )
    owner_person_ref: Mapped[UUID] = mapped_column(nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    revision: Mapped[int] = mapped_column(
        BigInteger, nullable=False, server_default=text("1"),
    )
    last_operation_id: Mapped[str] = mapped_column(Text, nullable=False)
    confirmed_operation_id: Mapped[str | None] = mapped_column(Text)
    observation_ref: Mapped[UUID | None] = mapped_column()
    evaluation_state_ref: Mapped[UUID | None] = mapped_column()
    assessment_code: Mapped[str | None] = mapped_column(Text)
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("clock_timestamp()"),
    )
