"""B14: align Routine organization with optional-Life-Area Activity Create.

A Routine remains a distinct recurring source. Absence of a Life Area assignment
is now a legitimate organization state, matching the U2 product boundary.

Revision ID: 20261005_108
Revises: 20261005_107
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261005_108"
down_revision: str | None = "20261005_107"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _definition(name: str, argument_count: int) -> str:
    value = op.get_bind().exec_driver_sql(
        """
        SELECT pg_get_functiondef(routine.oid)
          FROM pg_proc AS routine
          JOIN pg_namespace AS namespace ON namespace.oid=routine.pronamespace
         WHERE namespace.nspname='dante'
           AND routine.proname=%s
           AND routine.pronargs=%s
        """,
        (name, argument_count),
    ).scalar_one()
    if not isinstance(value, str):
        raise RuntimeError(f"B14 Routine capability {name} is unavailable")
    return value


def _replace_once(definition: str, old: str, new: str, *, label: str) -> str:
    if definition.count(old) != 1:
        raise RuntimeError(f"B14 {label} patch point did not match exactly once")
    return definition.replace(old, new)


def _install(definition: str, *, name: str, signature: str) -> None:
    connection = op.get_bind()
    connection.exec_driver_sql(definition.replace("%", "%%"))
    connection.exec_driver_sql(f"ALTER FUNCTION dante.{name}({signature}) OWNER TO dante_owner")
    connection.exec_driver_sql(
        f"REVOKE ALL PRIVILEGES ON FUNCTION dante.{name}({signature}) "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )
    connection.exec_driver_sql(
        f"GRANT EXECUTE ON FUNCTION dante.{name}({signature}) TO dante_runtime"
    )


def upgrade() -> None:
    create = _definition("create_self_routine", 9)
    create = _replace_once(
        create,
        "IF NOT EXISTS (SELECT 1 FROM dante.life_area WHERE life_area_ref=requested_life_area_ref AND self_person_ref=requested_self_person_ref AND archived=false) THEN\n        RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='routine_life_area_unavailable', MESSAGE='Routine Life Area unavailable';\n    END IF;",
        "IF requested_life_area_ref IS NOT NULL AND NOT EXISTS (SELECT 1 FROM dante.life_area WHERE life_area_ref=requested_life_area_ref AND self_person_ref=requested_self_person_ref AND archived=false) THEN\n        RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='routine_life_area_unavailable', MESSAGE='Routine Life Area unavailable';\n    END IF;",
        label="optional Life Area availability",
    )
    create = _replace_once(
        create,
        "INSERT INTO dante.routine_life_area_assignment(self_person_ref,routine_ref,life_area_ref,revision,assigned_at)\n    VALUES(requested_self_person_ref,requested_routine_ref,requested_life_area_ref,1,recorded_at);",
        "IF requested_life_area_ref IS NOT NULL THEN\n        INSERT INTO dante.routine_life_area_assignment(self_person_ref,routine_ref,life_area_ref,revision,assigned_at)\n        VALUES(requested_self_person_ref,requested_routine_ref,requested_life_area_ref,1,recorded_at);\n    END IF;",
        label="optional Life Area insert",
    )
    create = _replace_once(
        create,
        "RETURN QUERY SELECT previous.routine_ref,previous.accepted_source_revision,1::bigint,previous.accepted_at,true; RETURN;",
        "RETURN QUERY SELECT previous.routine_ref,previous.accepted_source_revision,\n            COALESCE((SELECT revision FROM dante.routine_life_area_assignment WHERE self_person_ref=requested_self_person_ref AND routine_ref=previous.routine_ref),0)::bigint,\n            previous.accepted_at,true; RETURN;",
        label="replay assignment revision",
    )
    create = _replace_once(
        create,
        "RETURN QUERY SELECT requested_routine_ref,1::bigint,1::bigint,recorded_at,false;",
        "RETURN QUERY SELECT requested_routine_ref,1::bigint,\n        CASE WHEN requested_life_area_ref IS NULL THEN 0::bigint ELSE 1::bigint END,recorded_at,false;",
        label="create assignment revision",
    )
    _install(
        create,
        name="create_self_routine",
        signature="uuid,text,text,uuid,text,uuid,uuid[],date,time without time zone",
    )

    listing = _definition("list_self_routines", 1)
    listing = _replace_once(
        listing,
        "FROM dante.routine_intention AS source JOIN dante.routine_life_area_assignment AS area ON area.routine_ref=source.routine_ref AND area.self_person_ref=source.self_person_ref",
        "FROM dante.routine_intention AS source LEFT JOIN dante.routine_life_area_assignment AS area ON area.routine_ref=source.routine_ref AND area.self_person_ref=source.self_person_ref",
        label="Routine Life Area listing join",
    )
    _install(listing, name="list_self_routines", signature="uuid")


def downgrade() -> None:
    raise RuntimeError(
        "20261005_108 is forward-only after optional Routine organization becomes valid"
    )
