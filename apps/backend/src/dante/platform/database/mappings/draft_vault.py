"""Inert temporal draft configurations; these rows are not Activities or Events."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import BigInteger, CheckConstraint, DateTime, Text, text
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
