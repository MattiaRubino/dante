"""B06-D: admit self-owned Occurrences to the shared Schedule capabilities.

Revision ID: 20260922_56
Revises: 20260922_55
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260922_56"
down_revision: str | None = "20260922_55"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"


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
        raise RuntimeError(f"B06-D Schedule capability {name} is unavailable")
    return value


def _replace_once(definition: str, old: str, new: str, *, label: str) -> str:
    if definition.count(old) != 1:
        raise RuntimeError(f"B06-D {label} patch point did not match exactly once")
    return definition.replace(old, new)


def _install(definition: str, *, name: str, signature: str) -> None:
    connection = op.get_bind()
    connection.exec_driver_sql(definition.replace("%", "%%"))
    connection.exec_driver_sql(f"ALTER FUNCTION dante.{name}({signature}) OWNER TO {_OWNER}")
    connection.exec_driver_sql(
        f"REVOKE ALL PRIVILEGES ON FUNCTION dante.{name}({signature}) "
        f"FROM PUBLIC,{_RUNTIME},{_MIGRATOR}"
    )
    connection.exec_driver_sql(
        f"GRANT EXECUTE ON FUNCTION dante.{name}({signature}) TO {_RUNTIME}"
    )


_SUBJECT_EVENT_BRANCH = """                       OR
                       (address.owner_family='event' AND EXISTS (
                           SELECT 1 FROM dante.event_expectation AS expectation
                            WHERE expectation.event_ref=requested_subject_native_ref
                              AND expectation.self_person_ref=requested_self_person_ref
                       ))"""

_SUBJECT_OCCURRENCE_BRANCH = """                       OR
                       (address.owner_family='occurrence' AND EXISTS (
                           SELECT 1
                             FROM dante.occurrence_generation AS generation
                            WHERE generation.occurrence_ref=requested_subject_native_ref
                              AND (
                                  EXISTS (
                                      SELECT 1 FROM dante.routine_intention AS routine
                                       WHERE routine.routine_ref=generation.source_native_ref
                                         AND routine.self_person_ref=requested_self_person_ref
                                  )
                                  OR EXISTS (
                                      SELECT 1 FROM dante.event_expectation AS expectation
                                       WHERE expectation.event_ref=generation.source_native_ref
                                         AND expectation.self_person_ref=requested_self_person_ref
                                  )
                              )
                       ))"""

_SCHEDULE_EVENT_BRANCH_COMPACT = """                   OR
                   (address.owner_family='event' AND EXISTS (
                       SELECT 1 FROM dante.event_expectation AS expectation
                        WHERE expectation.event_ref=schedule_row.subject_native_ref
                          AND expectation.self_person_ref=requested_self_person_ref
                   ))"""

_SCHEDULE_OCCURRENCE_BRANCH_COMPACT = """                   OR
                   (address.owner_family='occurrence' AND EXISTS (
                       SELECT 1
                         FROM dante.occurrence_generation AS generation
                        WHERE generation.occurrence_ref=schedule_row.subject_native_ref
                          AND (
                              EXISTS (
                                  SELECT 1 FROM dante.routine_intention AS routine
                                   WHERE routine.routine_ref=generation.source_native_ref
                                     AND routine.self_person_ref=requested_self_person_ref
                              )
                              OR EXISTS (
                                  SELECT 1 FROM dante.event_expectation AS expectation
                                   WHERE expectation.event_ref=generation.source_native_ref
                                     AND expectation.self_person_ref=requested_self_person_ref
                              )
                          )
                   ))"""

_SCHEDULE_EVENT_BRANCH_EXPANDED = """                            OR (
                                address.owner_family = 'event'
                                AND EXISTS (
                                    SELECT 1
                                      FROM dante.event_expectation AS expectation
                                     WHERE expectation.event_ref = schedule_row.subject_native_ref
                                       AND expectation.self_person_ref = requested_self_person_ref
                                )
                            )"""

_SCHEDULE_OCCURRENCE_BRANCH_EXPANDED = """                            OR (
                                address.owner_family = 'occurrence'
                                AND EXISTS (
                                    SELECT 1
                                      FROM dante.occurrence_generation AS generation
                                     WHERE generation.occurrence_ref =
                                           schedule_row.subject_native_ref
                                       AND (
                                           EXISTS (
                                               SELECT 1
                                                 FROM dante.routine_intention AS routine
                                                WHERE routine.routine_ref =
                                                      generation.source_native_ref
                                                  AND routine.self_person_ref =
                                                      requested_self_person_ref
                                           )
                                           OR EXISTS (
                                               SELECT 1
                                                 FROM dante.event_expectation AS expectation
                                                WHERE expectation.event_ref =
                                                      generation.source_native_ref
                                                  AND expectation.self_person_ref =
                                                      requested_self_person_ref
                                           )
                                       )
                                )
                            )"""


def upgrade() -> None:
    """Widen only Schedule authorization; placement/history semantics stay unchanged."""
    establish = _definition("establish_self_schedule_placement", 7)
    establish = _replace_once(
        establish,
        _SUBJECT_EVENT_BRANCH,
        _SUBJECT_EVENT_BRANCH + "\n" + _SUBJECT_OCCURRENCE_BRANCH,
        label="establish ownership",
    )
    establish = _replace_once(
        establish,
        "RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Schedule self scope rejected';",
        "RAISE EXCEPTION USING ERRCODE='23503', "
        "CONSTRAINT='schedule_establish_subject_not_found', "
        "MESSAGE='Schedule self scope rejected';",
        label="establish not-found diagnostic",
    )
    _install(
        establish,
        name="establish_self_schedule_placement",
        signature="uuid,text,text,uuid,uuid,uuid,jsonb",
    )

    revise = _definition("revise_self_schedule_placement", 7)
    revise = _replace_once(
        revise,
        _SCHEDULE_EVENT_BRANCH_COMPACT,
        _SCHEDULE_EVENT_BRANCH_COMPACT + "\n" + _SCHEDULE_OCCURRENCE_BRANCH_COMPACT,
        label="revise ownership",
    )
    _install(
        revise,
        name="revise_self_schedule_placement",
        signature="uuid,text,text,uuid,uuid,uuid,jsonb",
    )

    for name, argument_count, signature in (
        ("unschedule_self_schedule", 5, "uuid,text,text,uuid,uuid"),
        ("undo_self_schedule_unschedule_any", 6, "uuid,text,text,uuid,text,uuid"),
    ):
        definition = _definition(name, argument_count)
        definition = _replace_once(
            definition,
            _SCHEDULE_EVENT_BRANCH_EXPANDED,
            _SCHEDULE_EVENT_BRANCH_EXPANDED
            + "\n"
            + _SCHEDULE_OCCURRENCE_BRANCH_EXPANDED,
            label=f"{name} ownership",
        )
        _install(definition, name=name, signature=signature)


def downgrade() -> None:
    """Fail closed because deployed Occurrence Schedule history must stay operable."""
    raise RuntimeError(
        "20260922_56 is forward-only after Occurrence subjects enter shared Schedule history"
    )
