"""LR-12 Life Area product-profile rows (not Domain NativeRef owners)."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKeyConstraint, Index, Text
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
