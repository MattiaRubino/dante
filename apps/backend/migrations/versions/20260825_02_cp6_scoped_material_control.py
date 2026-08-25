"""Materialize CP6-M02 scoped owners and MaterialState/current controls.

Revision ID: 20260825_02
Revises: 20260825_01
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20260825_02"
down_revision: str | None = "20260825_01"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_DANTE_SCHEMA = "dante"
_RUNTIME_ROLE = "dante_runtime"
_MIGRATOR_ROLE = "dante_migrator"

_M2_TABLES = (
    "scoped_address",
    "schedule",
    "actual",
    "material_state_address",
    "native_current_material_state",
    "scoped_current_material_state",
)

_SCOPED_FAMILIES = "'schedule','actual'"
_MATERIAL_FACETS = (
    "'schedule.placement','actual.realization','session.timing',"
    "'routine.recurrence','event.recurrence'"
)
_NATIVE_CURRENT_FACETS = "'session.timing','routine.recurrence','event.recurrence'"
_SCOPED_CURRENT_FACETS = "'schedule.placement','actual.realization'"


def _fk(
    local_columns: list[str],
    remote_columns: list[str],
    *,
    name: str,
) -> sa.ForeignKeyConstraint:
    return sa.ForeignKeyConstraint(
        local_columns,
        remote_columns,
        name=op.f(name),
        match="SIMPLE",
        onupdate="NO ACTION",
        ondelete="NO ACTION",
        deferrable=False,
    )


def _deny_runtime_access_to_new_relations() -> None:
    for table_name in _M2_TABLES:
        op.execute(
            sa.text(
                "REVOKE ALL PRIVILEGES ON TABLE "
                f"{_DANTE_SCHEMA}.{table_name} "
                f"FROM PUBLIC, {_RUNTIME_ROLE}, {_MIGRATOR_ROLE}"
            )
        )


def upgrade() -> None:
    """Create exactly the CP6-M02 six-table scoped/material-control surface."""
    op.create_table(
        "scoped_address",
        sa.Column("scoped_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("scoped_family", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("scoped_ref", name=op.f("pk_scoped_address")),
        sa.CheckConstraint(
            f"scoped_family IN ({_SCOPED_FAMILIES})",
            name=op.f("ck_scoped_address_scoped_family"),
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "schedule",
        sa.Column("schedule_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("subject_native_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("schedule_ref", name=op.f("pk_schedule")),
        sa.CheckConstraint(
            "uuid_extract_version(schedule_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_schedule_uuidv7"),
        ),
        _fk(
            ["subject_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_schedule_subject_native_ref_native_address",
        ),
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ix_schedule_subject_native_ref",
        "schedule",
        ["subject_native_ref"],
        unique=False,
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "actual",
        sa.Column("actual_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("subject_native_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("actual_ref", name=op.f("pk_actual")),
        sa.CheckConstraint(
            "uuid_extract_version(actual_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_actual_uuidv7"),
        ),
        _fk(
            ["subject_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_actual_subject_native_ref_native_address",
        ),
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ix_actual_subject_native_ref",
        "actual",
        ["subject_native_ref"],
        unique=False,
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "material_state_address",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("native_owner_ref", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("scoped_owner_ref", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("facet_code", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_material_state_address"),
        ),
        sa.CheckConstraint(
            "uuid_extract_version(material_state_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_material_state_address_uuidv7"),
        ),
        sa.CheckConstraint(
            "num_nonnulls(native_owner_ref, scoped_owner_ref) = 1",
            name=op.f("ck_material_state_address_one_owner"),
        ),
        sa.CheckConstraint(
            f"facet_code IN ({_MATERIAL_FACETS})",
            name=op.f("ck_material_state_address_facet_code"),
        ),
        _fk(
            ["native_owner_ref"],
            ["dante.native_address.native_ref"],
            name="fk_material_state_address_native_owner_ref_native_address",
        ),
        _fk(
            ["scoped_owner_ref"],
            ["dante.scoped_address.scoped_ref"],
            name="fk_material_state_address_scoped_owner_ref_scoped_address",
        ),
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ix_material_state_address_native_owner_ref_facet_code",
        "material_state_address",
        ["native_owner_ref", "facet_code"],
        unique=False,
        schema=_DANTE_SCHEMA,
        postgresql_where=sa.text("native_owner_ref IS NOT NULL"),
    )
    op.create_index(
        "ix_material_state_address_scoped_owner_ref_facet_code",
        "material_state_address",
        ["scoped_owner_ref", "facet_code"],
        unique=False,
        schema=_DANTE_SCHEMA,
        postgresql_where=sa.text("scoped_owner_ref IS NOT NULL"),
    )

    op.create_table(
        "native_current_material_state",
        sa.Column("native_owner_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("facet_code", sa.Text(), nullable=False),
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "native_owner_ref",
            "facet_code",
            name=op.f("pk_native_current_material_state"),
        ),
        sa.UniqueConstraint(
            "material_state_ref",
            name=op.f("uq_native_current_material_state_material_state_ref"),
        ),
        sa.CheckConstraint(
            f"facet_code IN ({_NATIVE_CURRENT_FACETS})",
            name=op.f("ck_native_current_material_state_facet_code"),
        ),
        _fk(
            ["native_owner_ref"],
            ["dante.native_address.native_ref"],
            name="fk_native_current_material_state_owner_address",
        ),
        _fk(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_native_current_material_state_state_address",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "scoped_current_material_state",
        sa.Column("scoped_owner_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("facet_code", sa.Text(), nullable=False),
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "scoped_owner_ref",
            "facet_code",
            name=op.f("pk_scoped_current_material_state"),
        ),
        sa.UniqueConstraint(
            "material_state_ref",
            name=op.f("uq_scoped_current_material_state_material_state_ref"),
        ),
        sa.CheckConstraint(
            f"facet_code IN ({_SCOPED_CURRENT_FACETS})",
            name=op.f("ck_scoped_current_material_state_facet_code"),
        ),
        _fk(
            ["scoped_owner_ref"],
            ["dante.scoped_address.scoped_ref"],
            name="fk_scoped_current_material_state_owner_address",
        ),
        _fk(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_scoped_current_material_state_state_address",
        ),
        schema=_DANTE_SCHEMA,
    )

    _deny_runtime_access_to_new_relations()


def downgrade() -> None:
    """Return from CP6-M02 to the closed CP6-M01 schema."""
    for table_name in reversed(_M2_TABLES):
        op.drop_table(table_name, schema=_DANTE_SCHEMA)
