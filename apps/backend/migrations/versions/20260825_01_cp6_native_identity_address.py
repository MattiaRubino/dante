"""Materialize CP6-M01 native identity shells and NativeAddress.

Revision ID: 20260825_01
Revises: 20260820_01
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20260825_01"
down_revision: str | None = "20260820_01"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_DANTE_SCHEMA = "dante"
_RUNTIME_ROLE = "dante_runtime"
_MIGRATOR_ROLE = "dante_migrator"

_IDENTITY_TABLES: tuple[tuple[str, str], ...] = (
    ("person", "person_ref"),
    ("living_referent", "living_referent_ref"),
    ("asset", "asset_ref"),
    ("place", "place_ref"),
    ("content_artifact", "content_artifact_ref"),
    ("collective", "collective_ref"),
    ("possibility", "possibility_ref"),
    ("goal", "goal_ref"),
    ("plan", "plan_ref"),
    ("activity", "activity_ref"),
    ("event", "event_ref"),
    ("routine", "routine_ref"),
    ("occurrence", "occurrence_ref"),
    ("session", "session_ref"),
    ("observation", "observation_ref"),
)

_M1_TABLES = tuple(table_name for table_name, _ in _IDENTITY_TABLES) + ("native_address",)

_OWNER_FAMILIES = (
    "'person','living_referent','asset','place','content_artifact',"
    "'collective','possibility','goal','plan','activity','event',"
    "'routine','occurrence','session','observation'"
)


def _require_p0_security_preflight() -> None:
    """Fail before business DDL unless the live database proves the P0 envelope."""
    connection = op.get_bind()
    posture = connection.exec_driver_sql(
        """
        WITH owner_role AS (
            SELECT oid
            FROM pg_roles
            WHERE rolname = 'dante_owner'
        ),
        dante_schema AS (
            SELECT n.oid, n.nspowner, n.nspacl
            FROM pg_namespace AS n
            WHERE n.nspname = 'dante'
        ),
        current_database_acl AS (
            SELECT d.datdba, d.datacl
            FROM pg_database AS d
            WHERE d.datname = current_database()
        ),
        global_function_acl AS (
            SELECT COALESCE(
                (
                    SELECT defaults.defaclacl
                    FROM pg_default_acl AS defaults
                    CROSS JOIN owner_role
                    WHERE defaults.defaclrole = owner_role.oid
                      AND defaults.defaclnamespace = 0
                      AND defaults.defaclobjtype = 'f'
                ),
                acldefault('f', owner_role.oid)
            ) AS acl
            FROM owner_role
        ),
        global_type_acl AS (
            SELECT COALESCE(
                (
                    SELECT defaults.defaclacl
                    FROM pg_default_acl AS defaults
                    CROSS JOIN owner_role
                    WHERE defaults.defaclrole = owner_role.oid
                      AND defaults.defaclnamespace = 0
                      AND defaults.defaclobjtype = 'T'
                ),
                acldefault('T', owner_role.oid)
            ) AS acl
            FROM owner_role
        )
        SELECT
            (
                SELECT roles.rolname = 'dante_owner'
                FROM dante_schema
                JOIN pg_roles AS roles ON roles.oid = dante_schema.nspowner
            ),
            NOT EXISTS (
                SELECT 1
                FROM dante_schema
                CROSS JOIN LATERAL aclexplode(
                    COALESCE(
                        dante_schema.nspacl,
                        acldefault('n', dante_schema.nspowner)
                    )
                ) AS acl
                WHERE acl.grantee = 0
                  AND acl.privilege_type IN ('USAGE', 'CREATE')
            ),
            has_schema_privilege('dante_runtime', 'dante', 'USAGE'),
            NOT has_schema_privilege('dante_runtime', 'dante', 'CREATE'),
            NOT pg_has_role('dante_runtime', 'dante_owner', 'MEMBER'),
            NOT EXISTS (
                SELECT 1
                FROM current_database_acl
                CROSS JOIN LATERAL aclexplode(
                    COALESCE(
                        current_database_acl.datacl,
                        acldefault('d', current_database_acl.datdba)
                    )
                ) AS acl
                WHERE acl.grantee = 0
                  AND acl.privilege_type IN ('CONNECT', 'TEMPORARY')
            ),
            NOT EXISTS (
                SELECT 1
                FROM pg_default_acl AS defaults
                JOIN pg_roles AS owner
                  ON owner.oid = defaults.defaclrole
                LEFT JOIN pg_namespace AS namespace
                  ON namespace.oid = defaults.defaclnamespace
                CROSS JOIN LATERAL aclexplode(defaults.defaclacl) AS acl
                JOIN pg_roles AS grantee
                  ON grantee.oid = acl.grantee
                WHERE owner.rolname = 'dante_owner'
                  AND grantee.rolname = 'dante_runtime'
                  AND (
                      defaults.defaclnamespace = 0
                      OR namespace.nspname = 'dante'
                  )
                  AND defaults.defaclobjtype IN ('r', 'S', 'T', 'f')
            ),
            NOT EXISTS (
                SELECT 1
                FROM global_function_acl
                CROSS JOIN LATERAL aclexplode(global_function_acl.acl) AS acl
                WHERE acl.grantee = 0
                  AND acl.privilege_type = 'EXECUTE'
            ),
            NOT EXISTS (
                SELECT 1
                FROM global_type_acl
                CROSS JOIN LATERAL aclexplode(global_type_acl.acl) AS acl
                WHERE acl.grantee = 0
                  AND acl.privilege_type = 'USAGE'
            ),
            NOT has_table_privilege(
                'dante_runtime',
                'dante.alembic_version',
                'SELECT'
            )
        """
    ).one()

    if tuple(posture) != (True,) * 10:
        raise RuntimeError(
            "CP6-M01 requires P0 provisioning/security hardening before business DDL"
        )


def _create_identity_table(table_name: str, column_name: str) -> None:
    op.create_table(
        table_name,
        sa.Column(column_name, postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint(column_name, name=op.f(f"pk_{table_name}")),
        sa.CheckConstraint(
            f"uuid_extract_version({column_name}) IS NOT DISTINCT FROM 7",
            name=op.f(f"ck_{table_name}_uuidv7"),
        ),
        schema=_DANTE_SCHEMA,
    )


def _deny_runtime_access_to_new_relations() -> None:
    for table_name in _M1_TABLES:
        op.execute(
            sa.text(
                "REVOKE ALL PRIVILEGES ON TABLE "
                f"{_DANTE_SCHEMA}.{table_name} "
                f"FROM PUBLIC, {_RUNTIME_ROLE}, {_MIGRATOR_ROLE}"
            )
        )


def upgrade() -> None:
    """Create exactly the CP6-M01 16-table business surface."""
    _require_p0_security_preflight()

    for table_name, column_name in _IDENTITY_TABLES:
        _create_identity_table(table_name, column_name)

    op.create_table(
        "native_address",
        sa.Column("native_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("owner_family", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("native_ref", name=op.f("pk_native_address")),
        sa.CheckConstraint(
            f"owner_family IN ({_OWNER_FAMILIES})",
            name=op.f("ck_native_address_owner_family"),
        ),
        schema=_DANTE_SCHEMA,
    )

    _deny_runtime_access_to_new_relations()


def downgrade() -> None:
    """Return from CP6-M01 to the immutable CP3 technical baseline."""
    for table_name in reversed(_M1_TABLES):
        op.drop_table(table_name, schema=_DANTE_SCHEMA)
