"""Append-only, self-scoped per-Occurrence and following-future profile edits."""

from datetime import datetime
from typing import Any

from sqlalchemy import (
    ARRAY,
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import NativeRef


class OccurrenceProfileEditRow(Base):
    __tablename__ = "occurrence_profile_edit"
    __table_args__ = (
        UniqueConstraint(
            "source_native_ref",
            "revision",
            name="uq_occurrence_profile_edit_source_revision",
        ),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_occurrence_profile_edit_person",
        ),
        ForeignKeyConstraint(
            ["source_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_occurrence_profile_edit_source",
        ),
        ForeignKeyConstraint(
            ["selected_occurrence_ref"],
            ["dante.occurrence.occurrence_ref"],
            name="fk_occurrence_profile_edit_occurrence",
        ),
        CheckConstraint(
            "revision>=1 AND expected_revision>=0", name="revision"
        ),
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200", name="operation"
        ),
        CheckConstraint(
            "scope_code IN ('only_this','this_and_following')", name="scope"
        ),
        CheckConstraint(
            "jsonb_typeof(profile_patch)='object' AND "
            "profile_patch<>'{}'::jsonb", name="patch"
        ),
    )
    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    source_native_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    selected_occurrence_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    expected_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    expected_recurrence_state_ref: Mapped[NativeRef | None] = mapped_column()
    scope_code: Mapped[str] = mapped_column(Text, nullable=False)
    effective_zone_id: Mapped[str] = mapped_column(Text, nullable=False)
    anchor_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    accepted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    profile_patch: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    target_occurrence_refs: Mapped[list[NativeRef]] = mapped_column(
        ARRAY(Base.metadata.tables["dante.occurrence"].c.occurrence_ref.type),
        nullable=False,
    )
