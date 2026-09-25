"""B09-A: minimal canonical Responsibility / expected Participation relations.

Revision ID: 20260925_66
Revises: 20260924_65
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260925_66"
down_revision: str | None = "20260924_65"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"


def _fk(column: str, table: str, target_column: str, name: str) -> sa.ForeignKeyConstraint:
    return sa.ForeignKeyConstraint(
        [column],
        [f"{_SCHEMA}.{table}.{target_column}"],
        name=name,
        onupdate="NO ACTION",
        ondelete="NO ACTION",
        deferrable=False,
    )


def upgrade() -> None:
    """Activate only the direct/current B09-A relation subset; guarded mutation arrives in B09-B."""
    op.create_table(
        "event_expected_participation",
        sa.Column("event_ref", sa.Uuid(), nullable=False),
        sa.Column("participant_person_ref", sa.Uuid(), nullable=False),
        sa.Column("requirement_code", sa.Text(), nullable=False),
        sa.Column("established_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "event_ref",
            "participant_person_ref",
            name=op.f("pk_event_expected_participation"),
        ),
        _fk(
            "event_ref",
            "event",
            "event_ref",
            "fk_event_expected_participation_event",
        ),
        _fk(
            "participant_person_ref",
            "person",
            "person_ref",
            "fk_event_expected_participation_participant_person",
        ),
        sa.CheckConstraint(
            "requirement_code IN ('required','optional')",
            name=op.f("ck_event_expected_participation_requirement"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_event_expected_participation_person_event",
        "event_expected_participation",
        ["participant_person_ref", "event_ref"],
        schema=_SCHEMA,
    )

    op.create_table(
        "activity_responsibility",
        sa.Column("activity_ref", sa.Uuid(), nullable=False),
        sa.Column("responsible_person_ref", sa.Uuid(), nullable=False),
        sa.Column("established_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("activity_ref", name=op.f("pk_activity_responsibility")),
        _fk(
            "activity_ref",
            "activity",
            "activity_ref",
            "fk_activity_responsibility_activity",
        ),
        _fk(
            "responsible_person_ref",
            "person",
            "person_ref",
            "fk_activity_responsibility_person",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_activity_responsibility_person_activity",
        "activity_responsibility",
        ["responsible_person_ref", "activity_ref"],
        schema=_SCHEMA,
    )

    op.create_table(
        "event_responsibility",
        sa.Column("event_ref", sa.Uuid(), nullable=False),
        sa.Column("responsible_person_ref", sa.Uuid(), nullable=False),
        sa.Column("established_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("event_ref", name=op.f("pk_event_responsibility")),
        _fk(
            "event_ref",
            "event",
            "event_ref",
            "fk_event_responsibility_event",
        ),
        _fk(
            "responsible_person_ref",
            "person",
            "person_ref",
            "fk_event_responsibility_person",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_event_responsibility_person_event",
        "event_responsibility",
        ["responsible_person_ref", "event_ref"],
        schema=_SCHEMA,
    )


def downgrade() -> None:
    raise RuntimeError("B09-A is forward-only; restore from a controlled database backup.")
