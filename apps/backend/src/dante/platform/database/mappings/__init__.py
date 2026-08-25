"""Registered SQLAlchemy mappings for the materialized DANTE schema."""

from sqlalchemy import Table

from . import addressing, identity

MAPPED_TABLES: tuple[Table, ...] = (
    identity.PersonRow.__table__,
    identity.LivingReferentRow.__table__,
    identity.AssetRow.__table__,
    identity.PlaceRow.__table__,
    identity.ContentArtifactRow.__table__,
    identity.CollectiveRow.__table__,
    identity.PossibilityRow.__table__,
    identity.GoalRow.__table__,
    identity.PlanRow.__table__,
    identity.ActivityRow.__table__,
    identity.EventRow.__table__,
    identity.RoutineRow.__table__,
    identity.OccurrenceRow.__table__,
    identity.SessionRow.__table__,
    identity.ObservationRow.__table__,
    addressing.NativeAddressRow.__table__,
)

__all__ = ["MAPPED_TABLES"]
