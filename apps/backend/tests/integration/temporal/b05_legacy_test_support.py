"""Preserve pre-B05 behavioral tests while supplying B05's required real organization."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid7

import psycopg
from fastapi.testclient import TestClient

from dante.platform.database.references import NativeRef


def ensure_test_life_area(database: Any, actor: NativeRef) -> UUID:
    """Create/replay a real actor-local area, including context for old Person-only seeds."""
    account_ref = uuid7()
    fingerprint = hashlib.sha256(
        json.dumps(
            {"version": 1, "name": "Legacy regression"},
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode()
    ).hexdigest()
    with psycopg.connect(
        **database.connection_kwargs("dante_migrator", database.cluster.migrator_password)
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        present = connection.execute(
            "SELECT 1 FROM dante.account_application_context WHERE self_person_ref=%s",
            (actor,),
        ).fetchone()
        if present is None:
            connection.execute(
                "INSERT INTO dante.account(account_ref,status_code,created_at,disabled_at) "
                "VALUES (%s,'active',%s,NULL)",
                (account_ref, datetime.now(UTC)),
            )
            connection.execute(
                "INSERT INTO dante.account_application_context("
                "account_ref,self_person_ref,timezone_mode,fixed_zone_id) "
                "VALUES (%s,%s,'follow_device',NULL)",
                (account_ref, actor),
            )
        return UUID(
            str(
                connection.execute(
                    "SELECT life_area_ref FROM dante.create_self_life_area(%s,%s,%s,%s,%s)",
                    (
                        actor,
                        "b05b:legacy-regression-area",
                        fingerprint,
                        uuid7(),
                        "Legacy regression",
                    ),
                ).fetchone()[0]
            )
        )


def api_test_life_area(client: TestClient, headers: dict[str, str]) -> str:
    """Use the public catalog endpoint for existing B01/B03 HTTP regression flows."""
    response = client.post(
        "/api/v1/temporal/life-areas",
        json={"operation_id": "b05b:api-regression-area", "name": "Legacy regression"},
        headers=headers,
    )
    assert response.status_code in {200, 201}
    return str(response.json()["life_area_ref"])
