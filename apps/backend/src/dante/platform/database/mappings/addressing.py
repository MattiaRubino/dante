"""SQLAlchemy row mappings for CP6 addressing/control tables materialized so far."""

from sqlalchemy import CheckConstraint, ForeignKeyConstraint, Index, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef


class NativeAddressRow(Base):
    """Bounded NativeRef address dispatcher; not a semantic superclass."""

    __tablename__ = "native_address"
    __table_args__ = (
        CheckConstraint(
            "owner_family IN ('person','living_referent','asset','place','content_artifact','collective','possibility','goal','plan','activity','event','routine','occurrence','session','observation')",
            name="owner_family",
        ),
    )

    native_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    owner_family: Mapped[str] = mapped_column(Text, nullable=False)


class ScopedAddressRow(Base):
    """Bounded ScopedRecordRef address dispatcher for Schedule and Actual."""

    __tablename__ = "scoped_address"
    __table_args__ = (
        CheckConstraint(
            "scoped_family IN ('schedule','actual')",
            name="scoped_family",
        ),
    )

    scoped_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    scoped_family: Mapped[str] = mapped_column(Text, nullable=False)


class MaterialStateAddressRow(Base):
    """Address one immutable MaterialStateRef to exactly one owner space and facet."""

    __tablename__ = "material_state_address"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(material_state_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint(
            "num_nonnulls(native_owner_ref, scoped_owner_ref) = 1",
            name="one_owner",
        ),
        CheckConstraint(
            "facet_code IN ('schedule.placement','actual.realization','session.timing','routine.recurrence','event.recurrence')",
            name="facet_code",
        ),
        ForeignKeyConstraint(
            ["native_owner_ref"],
            ["dante.native_address.native_ref"],
            name="fk_material_state_address_native_owner_ref_native_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["scoped_owner_ref"],
            ["dante.scoped_address.scoped_ref"],
            name="fk_material_state_address_scoped_owner_ref_scoped_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ix_material_state_address_native_owner_ref_facet_code",
            "native_owner_ref",
            "facet_code",
            postgresql_where=text("native_owner_ref IS NOT NULL"),
        ),
        Index(
            "ix_material_state_address_scoped_owner_ref_facet_code",
            "scoped_owner_ref",
            "facet_code",
            postgresql_where=text("scoped_owner_ref IS NOT NULL"),
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    native_owner_ref: Mapped[NativeRef | None] = mapped_column(nullable=True)
    scoped_owner_ref: Mapped[ScopedRecordRef | None] = mapped_column(nullable=True)
    facet_code: Mapped[str] = mapped_column(Text, nullable=False)


class NativeCurrentMaterialStateRow(Base):
    """Shared native-owner current MaterialState binding; not a direct runtime surface."""

    __tablename__ = "native_current_material_state"
    __table_args__ = (
        UniqueConstraint(
            "material_state_ref",
            name="uq_native_current_material_state_material_state_ref",
        ),
        CheckConstraint(
            "facet_code IN ('session.timing','routine.recurrence','event.recurrence')",
            name="facet_code",
        ),
        ForeignKeyConstraint(
            ["native_owner_ref"],
            ["dante.native_address.native_ref"],
            name="fk_native_current_material_state_owner_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_native_current_material_state_state_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    native_owner_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    facet_code: Mapped[str] = mapped_column(Text, primary_key=True)
    material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)


class ScopedCurrentMaterialStateRow(Base):
    """Shared scoped-owner current MaterialState binding; not a direct runtime surface."""

    __tablename__ = "scoped_current_material_state"
    __table_args__ = (
        UniqueConstraint(
            "material_state_ref",
            name="uq_scoped_current_material_state_material_state_ref",
        ),
        CheckConstraint(
            "facet_code IN ('schedule.placement','actual.realization')",
            name="facet_code",
        ),
        ForeignKeyConstraint(
            ["scoped_owner_ref"],
            ["dante.scoped_address.scoped_ref"],
            name="fk_scoped_current_material_state_owner_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_scoped_current_material_state_state_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    scoped_owner_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    facet_code: Mapped[str] = mapped_column(Text, primary_key=True)
    material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
