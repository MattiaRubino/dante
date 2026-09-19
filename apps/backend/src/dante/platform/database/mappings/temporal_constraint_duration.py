"""SQLAlchemy mapping for the B04-E planned Schedule duration rule payload."""

from sqlalchemy import BigInteger, CheckConstraint, ForeignKeyConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import MaterialStateRef


class TemporalConstraintDurationStateRow(Base):
    """Typed exact-duration payload for one Temporal Constraint MaterialState."""

    __tablename__ = "temporal_constraint_duration_state"
    __table_args__ = (
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.temporal_constraint_state.material_state_ref"],
            name="fk_temporal_constraint_duration_state_constraint_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        CheckConstraint(
            "duration_kind_code IN ('minimum','maximum')",
            name="kind",
        ),
        CheckConstraint(
            "duration_microseconds > 0",
            name="positive",
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    duration_kind_code: Mapped[str] = mapped_column(Text, nullable=False)
    duration_microseconds: Mapped[int] = mapped_column(BigInteger, nullable=False)
