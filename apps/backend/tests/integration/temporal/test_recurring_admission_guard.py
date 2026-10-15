"""PostgreSQL admission guard: a skipped Routine Occurrence cannot spawn an Activity."""

from __future__ import annotations

from datetime import date
from typing import Any

import psycopg
import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from tests.integration.temporal.test_primary_life_area_assignment import _seed_self
from tests.integration.temporal.test_recurring_event_create import _daily_named_zone

from dante.modules.temporal.authoring import (
    TemporalAuthoringApplication,
    TemporalAuthoringPersistenceError,
)
from dante.modules.temporal.occurrence import OccurrenceApplication
from dante.modules.temporal.recurring_authoring import RecurringAuthoringApplication
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_skipped_recurring_activity_admission_denies_creation_and_binding(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        recurring = await RecurringAuthoringApplication(runtime.session_factory).create_routine(
            self_person_ref=actor,
            operation_id="guarded-generation:source",
            title="Controllo di generazione",
            life_area_intent=None,
            recurrence=_daily_named_zone(),
        )
        occurrences = OccurrenceApplication(runtime.session_factory)
        checkpoint = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=actor,
            source_ref=recurring.source_ref,
            operation_id="guarded-generation:checkpoint",
            start_date=date(2026, 10, 6),
            end_date_exclusive=date(2026, 10, 7),
            effective_zone_id="Europe/Rome",
        )
        assert len(checkpoint.occurrences) == 1
        occurrence = checkpoint.occurrences[0].occurrence_ref
        accepted = await occurrences.skip(
            self_person_ref=actor,
            occurrence_ref=occurrence,
            operation_id="guarded-generation:skip",
            reason="Istanza eliminata",
        )
        assert accepted.occurrence.skipped

        authoring = TemporalAuthoringApplication(runtime.session_factory)
        # The public Create API must still admit normal, non-generated Activities.
        independent = await authoring.create_activity(
            self_person_ref=actor,
            operation_id="guarded-generation:ordinary",
            title="Activity indipendente",
        )
        generated_operation = f"b14:occurrence-activity:{occurrence}"
        with pytest.raises(TemporalAuthoringPersistenceError):
            await authoring.create_activity(
                self_person_ref=actor,
                operation_id=generated_operation,
                title="Attività ricomparsa",
            )

        async with runtime.session_factory() as session, session.begin():
            with pytest.raises(DBAPIError) as refused:
                await session.execute(
                    text(
                        "SELECT * FROM dante.bind_self_routine_occurrence_activity("
                        ":actor,:occurrence,:activity)"
                    ),
                    {
                        "actor": actor,
                        "occurrence": occurrence,
                        "activity": independent.item.subject_native_ref,
                    },
                )
            assert (
                getattr(getattr(refused.value.orig, "diag", None), "constraint_name", None)
                == "routine_occurrence_activity_instance_unavailable"
            )

        # Count with owner privileges: runtime must not receive direct access
        # to Activity creation receipts merely for test introspection.
        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute(
                "SELECT count(*) FROM dante.activity_create_operation "
                "WHERE self_person_ref=%s AND operation_id=%s",
                (actor, generated_operation),
            ).fetchone() == (0,)
            assert connection.execute(
                "SELECT count(*) FROM dante.routine_occurrence_activity_instance "
                "WHERE occurrence_ref=%s",
                (occurrence,),
            ).fetchone() == (0,)
    finally:
        await runtime.dispose()
