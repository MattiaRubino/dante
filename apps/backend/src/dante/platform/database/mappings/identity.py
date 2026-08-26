"""SQLAlchemy row mappings for the fifteen CP6 native identity shells."""

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import NativeRef


class PersonRow(Base):
    """Persistence row for dante.person; not a Domain model class."""

    __tablename__ = "person"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(person_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
    )

    person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)


class LivingReferentRow(Base):
    """Persistence row for dante.living_referent; not a Domain model class."""

    __tablename__ = "living_referent"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(living_referent_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
    )

    living_referent_ref: Mapped[NativeRef] = mapped_column(primary_key=True)


class AssetRow(Base):
    """Persistence row for dante.asset; not a Domain model class."""

    __tablename__ = "asset"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(asset_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
    )

    asset_ref: Mapped[NativeRef] = mapped_column(primary_key=True)


class PlaceRow(Base):
    """Persistence row for dante.place; not a Domain model class."""

    __tablename__ = "place"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(place_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
    )

    place_ref: Mapped[NativeRef] = mapped_column(primary_key=True)


class ContentArtifactRow(Base):
    """Persistence row for dante.content_artifact; not a Domain model class."""

    __tablename__ = "content_artifact"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(content_artifact_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
    )

    content_artifact_ref: Mapped[NativeRef] = mapped_column(primary_key=True)


class CollectiveRow(Base):
    """Persistence row for dante.collective; not a Domain model class."""

    __tablename__ = "collective"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(collective_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
    )

    collective_ref: Mapped[NativeRef] = mapped_column(primary_key=True)


class PossibilityRow(Base):
    """Persistence row for dante.possibility; not a Domain model class."""

    __tablename__ = "possibility"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(possibility_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
    )

    possibility_ref: Mapped[NativeRef] = mapped_column(primary_key=True)


class GoalRow(Base):
    """Persistence row for dante.goal; not a Domain model class."""

    __tablename__ = "goal"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(goal_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
    )

    goal_ref: Mapped[NativeRef] = mapped_column(primary_key=True)


class PlanRow(Base):
    """Persistence row for dante.plan; not a Domain model class."""

    __tablename__ = "plan"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(plan_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
    )

    plan_ref: Mapped[NativeRef] = mapped_column(primary_key=True)


class ActivityRow(Base):
    """Persistence row for dante.activity; not a Domain model class."""

    __tablename__ = "activity"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(activity_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
    )

    activity_ref: Mapped[NativeRef] = mapped_column(primary_key=True)


class EventRow(Base):
    """Persistence row for dante.event; not a Domain model class."""

    __tablename__ = "event"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(event_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
    )

    event_ref: Mapped[NativeRef] = mapped_column(primary_key=True)


class RoutineRow(Base):
    """Persistence row for dante.routine; not a Domain model class."""

    __tablename__ = "routine"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(routine_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
    )

    routine_ref: Mapped[NativeRef] = mapped_column(primary_key=True)


class OccurrenceRow(Base):
    """Persistence row for dante.occurrence; not a Domain model class."""

    __tablename__ = "occurrence"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(occurrence_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
    )

    occurrence_ref: Mapped[NativeRef] = mapped_column(primary_key=True)


class SessionRow(Base):
    """Persistence row for dante.session; not a Domain model class."""

    __tablename__ = "session"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(session_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
    )

    session_ref: Mapped[NativeRef] = mapped_column(primary_key=True)


class ObservationRow(Base):
    """Persistence row for dante.observation; not a Domain model class."""

    __tablename__ = "observation"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(observation_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
    )

    observation_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
