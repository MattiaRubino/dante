"""Actor-local product Tag catalog, typed secondary edges and acceptance receipts."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import NativeRef


def _fk(column: str, table: str, constraint: str) -> ForeignKeyConstraint:
    target = "person_ref" if table == "person" else column
    return ForeignKeyConstraint(
        [column],
        [f"dante.{table}.{target}"],
        name=constraint,
        ondelete="NO ACTION",
        onupdate="NO ACTION",
        deferrable=False,
    )


class ProductTagRow(Base):
    """An application organization label, never a native Domain identity."""

    __tablename__ = "product_tag"
    __table_args__ = (
        _fk("self_person_ref", "person", "fk_product_tag_self_person_ref_person"),
        CheckConstraint("uuid_extract_version(tag_ref) IS NOT DISTINCT FROM 7", name="uuidv7"),
        CheckConstraint("name=btrim(name) AND name<>'' AND char_length(name)<=100", name="name"),
        CheckConstraint("revision>=1", name="revision"),
        Index("ix_product_tag_self_person_created", "self_person_ref", "created_at", "tag_ref"),
    )

    tag_ref: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    self_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    archived: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ProductTagOperationRow(Base):
    """Immutable actor-local create/rename/archive receipt."""

    __tablename__ = "product_tag_operation"
    __table_args__ = (
        _fk("self_person_ref", "person", "fk_product_tag_operation_person"),
        _fk("tag_ref", "product_tag", "fk_product_tag_operation_tag"),
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name="id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        CheckConstraint("kind IN ('create','rename','archive')", name="kind"),
        CheckConstraint("expected_revision>=0", name="expected"),
        CheckConstraint("accepted_revision=expected_revision+1", name="accepted"),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    tag_ref: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    kind: Mapped[str] = mapped_column(Text, nullable=False)
    expected_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    accepted_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ActivityTagRow(Base):
    """Current many-valued Tag association for one self Activity."""

    __tablename__ = "activity_tag"
    __table_args__ = (
        _fk("self_person_ref", "person", "fk_activity_tag_person"),
        _fk("activity_ref", "activity", "fk_activity_tag_activity"),
        _fk("tag_ref", "product_tag", "fk_activity_tag_tag"),
        Index("ix_activity_tag_self_person_tag", "self_person_ref", "tag_ref", "activity_ref"),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    activity_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    tag_ref: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    attached_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EventTagRow(Base):
    """Current many-valued Tag association for one self Event."""

    __tablename__ = "event_tag"
    __table_args__ = (
        _fk("self_person_ref", "person", "fk_event_tag_person"),
        _fk("event_ref", "event", "fk_event_tag_event"),
        _fk("tag_ref", "product_tag", "fk_event_tag_tag"),
        Index("ix_event_tag_self_person_tag", "self_person_ref", "tag_ref", "event_ref"),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    event_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    tag_ref: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    attached_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ActivityTagOperationRow(Base):
    """Immutable Activity attach/detach receipt independent of current edge."""

    __tablename__ = "activity_tag_operation"
    __table_args__ = (
        _fk("self_person_ref", "person", "fk_activity_tag_operation_person"),
        _fk("activity_ref", "activity", "fk_activity_tag_operation_activity"),
        _fk("tag_ref", "product_tag", "fk_activity_tag_operation_tag"),
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name="id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    activity_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    tag_ref: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    attached: Mapped[bool] = mapped_column(Boolean, nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EventTagOperationRow(Base):
    """Immutable Event attach/detach receipt independent of current edge."""

    __tablename__ = "event_tag_operation"
    __table_args__ = (
        _fk("self_person_ref", "person", "fk_event_tag_operation_person"),
        _fk("event_ref", "event", "fk_event_tag_operation_event"),
        _fk("tag_ref", "product_tag", "fk_event_tag_operation_tag"),
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name="id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    event_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    tag_ref: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    attached: Mapped[bool] = mapped_column(Boolean, nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
