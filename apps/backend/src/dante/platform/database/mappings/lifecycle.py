"""SQLAlchemy mappings for MaterialState retirement and recovery suppression linkage."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKeyConstraint, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import MaterialStateRef


class MaterialStateRetirementRow(Base):
    """Append-only tombstone preserving MaterialStateRef continuity after payload retirement."""

    __tablename__ = "material_state_retirement"
    __table_args__ = (
        UniqueConstraint(
            "recovery_suppression_ref",
            name="uq_material_state_retirement_recovery_suppression_ref",
        ),
        CheckConstraint(
            "retirement_code IN ('redacted','unavailable')",
            name="retirement_code",
        ),
        CheckConstraint("isfinite(retired_at)", name="retired_at"),
        CheckConstraint(
            "uuid_extract_version(recovery_suppression_ref) IS NOT DISTINCT FROM 7",
            name="recovery_suppression_uuidv7",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_material_state_retirement_material_state_ref_material_state_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    retirement_code: Mapped[str] = mapped_column(Text, nullable=False)
    retired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    recovery_suppression_ref: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        nullable=False,
    )
