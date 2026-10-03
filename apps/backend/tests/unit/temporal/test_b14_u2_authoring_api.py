"""Contract-level tests for the B14-U2 authoring API surface."""

from datetime import datetime
from uuid import uuid7

import pytest
from pydantic import ValidationError

from dante.modules.temporal.authoring_api import (
    AcceptedFloatingLocalPlacementResponse,
    AuthorActivityRequest,
    AuthorEventRequest,
    AuthoringLifeAreaRequest,
    router,
)


def test_u2_authoring_routes_have_stable_operation_ids() -> None:
    operations = {
        route.path: getattr(route, "operation_id", None)
        for route in router.routes
        if getattr(route, "path", None) is not None
    }
    assert operations == {
        "/api/v1/temporal/authoring/activities": "temporal_author_activity",
        "/api/v1/temporal/authoring/events": "temporal_author_event",
    }


def test_activity_authoring_accepts_real_unassigned_state() -> None:
    payload = AuthorActivityRequest.model_validate(
        {
            "operation_id": "u2:activity:unassigned",
            "title": "Passeggiata",
            "description": "Lungo il fiume",
            "location": "Lungofiume",
            "item_color_code": "#12abef",
            "placement": {
                "kind": "floating_local_interval",
                "starts_local_at": "2026-09-30T23:30:00",
                "ends_local_at": "2026-10-02T01:00:00",
            },
        }
    )
    assert payload.life_area is None
    assert payload.item_color_code == "#12abef"
    assert payload.placement is not None
    assert payload.placement.starts_local_at == datetime(2026, 9, 30, 23, 30)
    assert payload.placement.ends_local_at == datetime(2026, 10, 2, 1, 0)


def test_activity_authoring_accepts_only_positive_session_minimum() -> None:
    payload = AuthorActivityRequest.model_validate(
        {
            "operation_id": "u6:session-minimum",
            "title": "Workshop",
            "minimum_session_duration_microseconds": 1_500_000_000,
        }
    )
    assert payload.minimum_session_duration_microseconds == 1_500_000_000
    with pytest.raises(ValidationError):
        AuthorActivityRequest.model_validate(
            {
                "operation_id": "u6:session-minimum",
                "title": "Workshop",
                "minimum_session_duration_microseconds": 0,
            }
        )


def test_event_authoring_exposes_same_location_description_and_organization_shape() -> None:
    payload = AuthorEventRequest.model_validate(
        {
            "operation_id": "u2:event:new-area",
            "title": "Workshop",
            "description": "Decisioni di progetto",
            "location": "Sala A",
            "life_area": {"new_name": "Studio", "color_code": "#8A4FFF"},
            "agenda_parts": ["Revisione", "Decisioni"],
        }
    )
    assert payload.location == "Sala A"
    assert payload.life_area is not None
    assert payload.life_area.new_name == "Studio"
    assert payload.agenda_parts == ["Revisione", "Decisioni"]


def test_life_area_intent_cannot_select_and_create_at_the_same_time() -> None:
    with pytest.raises(ValidationError):
        AuthoringLifeAreaRequest.model_validate(
            {"life_area_ref": str(uuid7()), "new_name": "Studio"}
        )
    with pytest.raises(ValidationError):
        AuthoringLifeAreaRequest.model_validate({"color_code": "#8A4FFF"})


def test_accepted_schedule_response_keeps_explicit_multiday_boundaries() -> None:
    response = AcceptedFloatingLocalPlacementResponse(
        starts_local_at=datetime(2026, 9, 30, 23, 30),
        ends_local_at=datetime(2026, 10, 2, 1, 0),
    )
    assert response.kind == "floating_local_interval"
    assert response.starts_local_at.date().isoformat() == "2026-09-30"
    assert response.ends_local_at.date().isoformat() == "2026-10-02"
