"""SQLAlchemy mapping for the authenticated DANTE application context."""

from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKeyConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import NativeRef


class AccountApplicationContextRow(Base):
    """Current application context for one Account; Account and Person remain distinct."""

    __tablename__ = "account_application_context"
    __table_args__ = (
        CheckConstraint(
            "timezone_mode IN ('follow_device','fixed')",
            name="timezone_mode",
        ),
        CheckConstraint(
            "(timezone_mode='follow_device' AND fixed_zone_id IS NULL) OR "
            "(timezone_mode='fixed' AND fixed_zone_id IS NOT NULL "
            "AND fixed_zone_id=btrim(fixed_zone_id) AND fixed_zone_id<>'' "
            "AND char_length(fixed_zone_id)<=255 "
            "AND fixed_zone_id !~ '^[+-]([0-9]{2}|[0-9]{4}|[0-9]{2}:[0-9]{2})$')",
            name="timezone_policy",
        ),
        ForeignKeyConstraint(
            ["account_ref"],
            ["dante.account.account_ref"],
            name="fk_account_application_context_account_ref_account",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_account_application_context_self_person_ref_person",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    account_ref: Mapped[UUID] = mapped_column(primary_key=True)
    self_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    timezone_mode: Mapped[str] = mapped_column(Text, nullable=False)
    fixed_zone_id: Mapped[str | None] = mapped_column(Text, nullable=True)
