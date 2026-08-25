"""SQLAlchemy row mappings for CP6 addressing/control tables materialized so far."""

from sqlalchemy import CheckConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import NativeRef


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
