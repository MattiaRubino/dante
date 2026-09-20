"""LR-12 Life Area product-profile rows (not Domain NativeRef owners)."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import NativeRef


class LifeAreaRow(Base):
    """One self-scoped application profile; not an LR-01 identity."""

    __tablename__ = "life_area"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(life_area_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint(
            "name=btrim(name) AND name<>'' AND char_length(name)<=100",
            name="name",
        ),
        CheckConstraint("revision>=1", name="revision"),
        CheckConstraint("sort_order>=0", name="sort_order"),
        CheckConstraint(
            "icon_code IS NULL OR (char_length(icon_code)<=40 AND icon_code ~ '^[a-z][a-z0-9_-]*$')",
            name="icon_code",
        ),
        CheckConstraint("color_code IS NULL OR color_code ~ '^#[0-9A-F]{6}$'", name="color_code"),
        UniqueConstraint(
            "self_person_ref",
            "sort_order",
            name="uq_life_area_self_person_sort_order",
            deferrable=True,
            initially="DEFERRED",
        ),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_life_area_self_person_ref_person",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index("ix_life_area_self_person_created", "self_person_ref", "created_at", "life_area_ref"),
    )

    life_area_ref: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    self_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    sort_order: Mapped[int] = mapped_column(BigInteger, nullable=False)
    archived: Mapped[bool] = mapped_column(Boolean, nullable=False)
    hidden: Mapped[bool] = mapped_column(Boolean, nullable=False)
    icon_code: Mapped[str | None] = mapped_column(Text)
    color_code: Mapped[str | None] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class LifeAreaCreateOperationRow(Base):
    """Immutable creation receipt scoped to the actor's self Person and key."""

    __tablename__ = "life_area_create_operation"
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
            name="fk_life_area_create_operation_self_person_ref_person",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["life_area_ref"],
            ["dante.life_area.life_area_ref"],
            name="fk_life_area_create_operation_life_area_ref_life_area",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    life_area_ref: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class LifeAreaMutationOperationRow(Base):
    """Immutable self-scoped lifecycle mutation or reorder receipt."""

    __tablename__ = "life_area_mutation_operation"
    __table_args__ = (
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        CheckConstraint(
            "mutation_kind IN ('rename','visibility','archive','appearance','reorder')", name="kind"
        ),
        CheckConstraint(
            "(mutation_kind='reorder' AND life_area_ref IS NULL AND accepted_revision IS NULL) OR (mutation_kind<>'reorder' AND life_area_ref IS NOT NULL AND accepted_revision>=2)",
            name="shape",
        ),
        CheckConstraint("affected_count>=0", name="count"),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_life_area_mutation_operation_self_person_ref_person",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["life_area_ref"],
            ["dante.life_area.life_area_ref"],
            name="fk_life_area_mutation_operation_life_area_ref_life_area",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    mutation_kind: Mapped[str] = mapped_column(Text, nullable=False)
    life_area_ref: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True))
    accepted_revision: Mapped[int | None] = mapped_column(BigInteger)
    affected_count: Mapped[int] = mapped_column(Integer, nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
