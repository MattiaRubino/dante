"""B05-C real PostgreSQL Tag lifecycle and typed, actor-local many-to-many proof."""

from __future__ import annotations

from typing import Any

import psycopg
import pytest
from fastapi.testclient import TestClient
from tests.integration.temporal.test_b01_activity_core import (
    _CANONICAL_ORIGIN,
    _auth_settings,
    _base_headers,
    _seed_account,
    _settings,
    _signin,
)
from tests.integration.temporal.test_b05_primary_life_area_assignment import _seed_self

from dante.auth.sessions import CSRF_HEADER_NAME
from dante.bootstrap.app import create_app
from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.event import TemporalEventApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.product_tag import (
    ProductTagApplication,
    ProductTagConflictError,
    ProductTagOperationReuseError,
    ProductTagUnavailableError,
)
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres
pytest_plugins = ("tests.integration.temporal.test_b01_activity_core",)


@pytest.mark.asyncio
async def test_secondary_tags_are_many_valued_independent_and_actor_local(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    tags = ProductTagApplication(runtime.session_factory)
    areas = LifeAreaApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    events = TemporalEventApplication(runtime.session_factory)
    try:
        area = (await areas.create(self_person_ref=alice, operation_id="area", name="Studio")).area
        activity = (
            await activities.create_activity(
                self_person_ref=alice,
                operation_id="activity",
                title="Leggere",
                life_area_ref=area.life_area_ref,
            )
        ).activity
        event = (
            await events.create_event(
                self_person_ref=alice,
                operation_id="event",
                title="Incontro",
                life_area_ref=area.life_area_ref,
            )
        ).event
        first, replayed = await tags.create(
            self_person_ref=alice, operation_id="tag:first", name=" Studio "
        )
        assert first.name == "Studio"
        assert first.revision == 1
        assert not replayed
        replay, replayed = await tags.create(
            self_person_ref=alice, operation_id="tag:first", name="Studio"
        )
        assert replay == first
        assert replayed
        second, _ = await tags.create(
            self_person_ref=alice, operation_id="tag:second", name="Studio"
        )
        bob_tag, _ = await tags.create(self_person_ref=bob, operation_id="tag:first", name="Studio")
        assert len({area.life_area_ref, first.tag_ref, second.tag_ref, bob_tag.tag_ref}) == 4
        assert len(await tags.list(self_person_ref=alice)) == 2
        assert len(await tags.list(self_person_ref=bob)) == 1
        with pytest.raises(ProductTagOperationReuseError):
            await tags.create(self_person_ref=alice, operation_id="tag:first", name="Altro")

        first_edge = await tags.set_item_tag(
            self_person_ref=alice,
            operation_id="attach:a:1",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
            tag_ref=first.tag_ref,
            attached=True,
        )
        assert first_edge.attached
        assert not first_edge.replayed
        assert (
            await tags.set_item_tag(
                self_person_ref=alice,
                operation_id="attach:a:1",
                subject_kind="activity",
                subject_native_ref=activity.activity_ref,
                tag_ref=first.tag_ref,
                attached=True,
            )
        ).replayed
        await tags.set_item_tag(
            self_person_ref=alice,
            operation_id="attach:a:2",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
            tag_ref=second.tag_ref,
            attached=True,
        )
        await tags.set_item_tag(
            self_person_ref=alice,
            operation_id="attach:e:1",
            subject_kind="event",
            subject_native_ref=event.event_ref,
            tag_ref=first.tag_ref,
            attached=True,
        )
        assert len(await tags.list_edges(self_person_ref=alice)) == 3
        assert await tags.list_edges(self_person_ref=bob) == ()
        with pytest.raises(ProductTagUnavailableError):
            await tags.set_item_tag(
                self_person_ref=bob,
                operation_id="foreign-item",
                subject_kind="activity",
                subject_native_ref=activity.activity_ref,
                tag_ref=bob_tag.tag_ref,
                attached=True,
            )
        with pytest.raises(ProductTagUnavailableError):
            await tags.set_item_tag(
                self_person_ref=alice,
                operation_id="foreign-tag",
                subject_kind="activity",
                subject_native_ref=activity.activity_ref,
                tag_ref=bob_tag.tag_ref,
                attached=True,
            )
        with pytest.raises(ProductTagConflictError):
            await tags.set_item_tag(
                self_person_ref=alice,
                operation_id="duplicate-attach",
                subject_kind="activity",
                subject_native_ref=activity.activity_ref,
                tag_ref=first.tag_ref,
                attached=True,
            )
        with pytest.raises(ProductTagOperationReuseError):
            await tags.set_item_tag(
                self_person_ref=alice,
                operation_id="attach:a:1",
                subject_kind="activity",
                subject_native_ref=activity.activity_ref,
                tag_ref=second.tag_ref,
                attached=True,
            )

        renamed = await tags.mutate(
            self_person_ref=alice,
            operation_id="rename",
            tag_ref=first.tag_ref,
            expected_revision=1,
            kind="rename",
            name="Lettura",
        )
        assert renamed.accepted_revision == 2
        assert not renamed.replayed
        assert (
            await tags.mutate(
                self_person_ref=alice,
                operation_id="rename",
                tag_ref=first.tag_ref,
                expected_revision=1,
                kind="rename",
                name="Lettura",
            )
        ).replayed
        with pytest.raises(ProductTagConflictError):
            await tags.mutate(
                self_person_ref=alice,
                operation_id="stale",
                tag_ref=first.tag_ref,
                expected_revision=1,
                kind="archive",
            )
        archived = await tags.mutate(
            self_person_ref=alice,
            operation_id="archive",
            tag_ref=first.tag_ref,
            expected_revision=2,
            kind="archive",
        )
        assert archived.accepted_revision == 3
        assert (
            await tags.mutate(
                self_person_ref=alice,
                operation_id="rename",
                tag_ref=first.tag_ref,
                expected_revision=1,
                kind="rename",
                name="Lettura",
            )
        ).replayed
        assert len(await tags.list_edges(self_person_ref=alice)) == 3
        assert next(
            t for t in await tags.list(self_person_ref=alice) if t.tag_ref == first.tag_ref
        ).archived
        detached = await tags.set_item_tag(
            self_person_ref=alice,
            operation_id="detach:a:1",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
            tag_ref=first.tag_ref,
            attached=False,
        )
        assert not detached.attached
        assert len(await tags.list_edges(self_person_ref=alice)) == 2
        with pytest.raises(ProductTagUnavailableError):
            await tags.set_item_tag(
                self_person_ref=alice,
                operation_id="archived-new",
                subject_kind="activity",
                subject_native_ref=activity.activity_ref,
                tag_ref=first.tag_ref,
                attached=True,
            )
        assert (
            await tags.set_item_tag(
                self_person_ref=alice,
                operation_id="detach:a:1",
                subject_kind="activity",
                subject_native_ref=activity.activity_ref,
                tag_ref=first.tag_ref,
                attached=False,
            )
        ).replayed
        assert (
            await activities.get_activity(self_person_ref=alice, activity_ref=activity.activity_ref)
        ).life_area_ref == area.life_area_ref
        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute(
                "SELECT count(*) FROM dante.native_address WHERE native_ref=%s", (first.tag_ref,)
            ).fetchone() == (0,)
            assert connection.execute(
                "SELECT count(*) FROM dante.activity_tag_operation WHERE self_person_ref=%s",
                (alice,),
            ).fetchone() == (3,)
    finally:
        await runtime.dispose()


def test_secondary_tag_runtime_acl_is_bounded(migrated_database: Any) -> None:
    with psycopg.connect(
        host=migrated_database.cluster.host,
        port=migrated_database.cluster.port,
        dbname=migrated_database.name,
        user=migrated_database.cluster.admin_user,
        password=migrated_database.cluster.admin_password,
    ) as connection:
        for table in (
            "product_tag",
            "product_tag_operation",
            "activity_tag",
            "event_tag",
            "activity_tag_operation",
            "event_tag_operation",
        ):
            assert connection.execute(
                "SELECT has_table_privilege('dante_runtime',%s,'SELECT'), "
                "has_table_privilege('dante_runtime',%s,'INSERT')",
                (f"dante.{table}", f"dante.{table}"),
            ).fetchone() == (False, False)
        for signature in (
            "dante.create_self_product_tag(uuid,text,text,uuid,text)",
            "dante.mutate_self_product_tag(uuid,text,text,uuid,bigint,text,text)",
            "dante.list_self_product_tags(uuid)",
            "dante.set_self_activity_tag(uuid,text,text,uuid,uuid,boolean)",
            "dante.set_self_event_tag(uuid,text,text,uuid,uuid,boolean)",
            "dante.list_self_item_tags(uuid)",
        ):
            assert connection.execute(
                "SELECT has_function_privilege('dante_runtime',%s,'EXECUTE')", (signature,)
            ).fetchone() == (True,)


def test_secondary_tag_authenticated_api_create_attach_list_archive_detach(
    migrated_database: Any, activity_hibp_stub_url: str
) -> None:
    email = "b05.tags@example.com"
    _seed_account(migrated_database, _auth_settings(activity_hibp_stub_url), email)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))
    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, email)
        mutating = {**_base_headers(), CSRF_HEADER_NAME: csrf}
        no_csrf = client.post(
            "/api/v1/temporal/tags",
            json={"operation_id": "invalid", "name": "Segreto"},
            headers=_base_headers(),
        )
        assert no_csrf.status_code == 403
        area = client.post(
            "/api/v1/temporal/life-areas",
            json={"operation_id": "b05c:api:area", "name": "Studio"},
            headers=mutating,
        )
        assert area.status_code == 201
        created = client.post(
            "/api/v1/temporal/activities",
            json={
                "operation_id": "b05c:api:activity",
                "title": "Leggere",
                "life_area_ref": area.json()["life_area_ref"],
            },
            headers=mutating,
        )
        assert created.status_code == 201
        item_ref = created.json()["activity_ref"]
        tag = client.post(
            "/api/v1/temporal/tags",
            json={"operation_id": "b05c:api:create", "name": " Lettura "},
            headers=mutating,
        )
        assert tag.status_code == 201
        tag_ref = tag.json()["tag_ref"]
        replay = client.post(
            "/api/v1/temporal/tags",
            json={"operation_id": "b05c:api:create", "name": "Lettura"},
            headers=mutating,
        )
        assert replay.status_code == 200
        assert replay.json()["tag_ref"] == tag_ref
        attach_path = f"/api/v1/temporal/activities/{item_ref}/tags/{tag_ref}/attach"
        attached = client.post(
            attach_path, json={"operation_id": "b05c:api:attach"}, headers=mutating
        )
        assert attached.status_code == 200
        assert attached.json()["attached"] is True
        assignments = client.get("/api/v1/temporal/tags/assignments", headers=_base_headers())
        assert assignments.status_code == 200
        assert [
            (row["subject_kind"], row["subject_native_ref"], row["tag_ref"])
            for row in assignments.json()
        ] == [("activity", item_ref, tag_ref)]
        renamed = client.put(
            f"/api/v1/temporal/tags/{tag_ref}/name",
            json={"operation_id": "b05c:api:rename", "expected_revision": 1, "name": "Libri"},
            headers=mutating,
        )
        assert renamed.status_code == 200
        archived = client.post(
            f"/api/v1/temporal/tags/{tag_ref}/archive",
            json={"operation_id": "b05c:api:archive", "expected_revision": 2},
            headers=mutating,
        )
        assert archived.status_code == 200
        catalog = client.get("/api/v1/temporal/tags", headers=_base_headers())
        assert catalog.status_code == 200
        assert catalog.json()[0]["archived"] is True
        detached = client.post(
            f"/api/v1/temporal/activities/{item_ref}/tags/{tag_ref}/detach",
            json={"operation_id": "b05c:api:detach"},
            headers=mutating,
        )
        assert detached.status_code == 200
        assert detached.json()["attached"] is False
        assert client.get("/api/v1/temporal/tags/assignments", headers=_base_headers()).json() == []
