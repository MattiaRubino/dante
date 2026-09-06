"""Typed application contracts for authenticated DANTE context resolution."""

from dataclasses import dataclass

from dante.auth.contracts import Principal
from dante.platform.database.references import NativeRef
from dante.platform.time import TimeZonePolicy


@dataclass(frozen=True, slots=True)
class DanteContext:
    """Request-scoped DANTE context derived from an authenticated Principal."""

    principal: Principal
    self_person_ref: NativeRef
    timezone_policy: TimeZonePolicy
    effective_zone_id: str
