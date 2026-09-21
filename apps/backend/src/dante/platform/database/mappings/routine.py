"""B06-A Routine source core; recurrence and occurrence remain separate."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import BigInteger, Boolean, CheckConstraint, DateTime, ForeignKeyConstraint, Index, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import NativeRef


def _fk(column: str, table: str, name: str) -> ForeignKeyConstraint:
    return ForeignKeyConstraint([column], [f"dante.{table}.{ 'person_ref' if table == 'person' else column}"], name=name, onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False)


class RoutineIntentionRow(Base):
    """Current Routine source metadata and lifecycle, not a recurrence state."""
    __tablename__ = "routine_intention"
    __table_args__ = (
        _fk("routine_ref", "routine", "fk_routine_intention_routine"),
        _fk("self_person_ref", "person", "fk_routine_intention_person"),
        CheckConstraint("title=btrim(title) AND title<>'' AND char_length(title)<=300", name="title"),
        CheckConstraint("lifecycle_state IN ('active','paused','ended')", name="lifecycle"),
        CheckConstraint("source_revision>=1", name="revision"),
        Index("ix_routine_intention_self_person_created", "self_person_ref", "created_at", "routine_ref"),
    )
    routine_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    self_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    lifecycle_state: Mapped[str] = mapped_column(Text, nullable=False)
    source_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    lifecycle_changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RoutineOperationRow(Base):
    __tablename__ = "routine_operation"
    __table_args__ = (
        _fk("self_person_ref", "person", "fk_routine_operation_person"), _fk("routine_ref", "routine", "fk_routine_operation_routine"),
        CheckConstraint("operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200", name="id"),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        CheckConstraint("kind IN ('create','rename','pause','resume','end')", name="kind"),
        CheckConstraint("expected_source_revision>=0", name="expected"), CheckConstraint("accepted_source_revision=expected_source_revision+1", name="accepted"),
    )
    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    routine_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    kind: Mapped[str] = mapped_column(Text, nullable=False)
    expected_source_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    accepted_source_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RoutineLifeAreaAssignmentRow(Base):
    __tablename__ = "routine_life_area_assignment"
    __table_args__ = (_fk("self_person_ref", "person", "fk_routine_life_area_assignment_person"), _fk("routine_ref", "routine", "fk_routine_life_area_assignment_routine"), _fk("life_area_ref", "life_area", "fk_routine_life_area_assignment_life_area"), CheckConstraint("revision>=1", name="revision"), Index("ix_routine_life_area_assignment_self_person_life_area", "self_person_ref", "life_area_ref", "routine_ref"))
    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    routine_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    life_area_ref: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RoutineLifeAreaAssignmentOperationRow(Base):
    __tablename__ = "routine_life_area_assignment_operation"
    __table_args__ = (_fk("self_person_ref", "person", "fk_routine_area_op_person"), _fk("routine_ref", "routine", "fk_routine_area_op_routine"), _fk("life_area_ref", "life_area", "fk_routine_area_op_life_area"), CheckConstraint("operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200", name="id"), CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"), CheckConstraint("expected_revision>=0", name="expected"), CheckConstraint("accepted_revision=expected_revision+1", name="accepted"))
    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    routine_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    life_area_ref: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    expected_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    accepted_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RoutineTagRow(Base):
    __tablename__ = "routine_tag"
    __table_args__ = (_fk("self_person_ref", "person", "fk_routine_tag_person"), _fk("routine_ref", "routine", "fk_routine_tag_routine"), _fk("tag_ref", "product_tag", "fk_routine_tag_tag"), Index("ix_routine_tag_self_person_tag", "self_person_ref", "tag_ref", "routine_ref"))
    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    routine_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    tag_ref: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    attached_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RoutineTagOperationRow(Base):
    __tablename__ = "routine_tag_operation"
    __table_args__ = (_fk("self_person_ref", "person", "fk_routine_tag_op_person"), _fk("routine_ref", "routine", "fk_routine_tag_op_routine"), _fk("tag_ref", "product_tag", "fk_routine_tag_op_tag"), CheckConstraint("operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200", name="id"), CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"))
    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    routine_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    tag_ref: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    attached: Mapped[bool] = mapped_column(Boolean, nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
