"""B12-A read-only diagnosis of a self-owned Plan's current supported truth."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from sqlalchemy import bindparam, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.modules.temporal.plan_dependency import PlanDependencyApplication
from dante.modules.temporal.plan_work import PlanWorkApplication
from dante.modules.temporal.temporal_constraint import (
    AbsoluteIntervalPlacement,
    TemporalConstraintApplication,
)
from dante.platform.database.references import NativeRef

_MAX_STEPS = 20
_MAX_DEPENDENCIES = 40

_PLACEMENTS = text(
    """
    SELECT schedule.subject_native_ref AS activity_ref,
           schedule.schedule_ref,
           current.material_state_ref,
           placement.temporal_form_code,
           absolute.starts_at,
           absolute.ends_at
      FROM dante.schedule AS schedule
      JOIN dante.activity_intention AS activity
        ON activity.activity_ref = schedule.subject_native_ref
       AND activity.self_person_ref = :self_ref
      JOIN dante.schedule_current_placement AS current
        ON current.scoped_owner_ref = schedule.schedule_ref
      JOIN dante.schedule_placement_state AS placement
        ON placement.schedule_ref = schedule.schedule_ref
       AND placement.material_state_ref = current.material_state_ref
      LEFT JOIN dante.schedule_placement_absolute_state AS absolute
        ON absolute.material_state_ref = placement.material_state_ref
     WHERE schedule.subject_native_ref IN :activity_refs
     ORDER BY schedule.subject_native_ref, schedule.schedule_ref
     LIMIT 41
    """
).bindparams(bindparam("activity_refs", expanding=True))


class PlanConflictNotFoundError(LookupError):
    """The self Person cannot read this Plan."""


class PlanConflictInputError(ValueError):
    """The requested Plan exceeds this bounded diagnostic profile."""


class PlanConflictStateError(RuntimeError):
    """The Plan changed during inspection or no longer matches the UI basis."""


@dataclass(frozen=True, slots=True)
class PlacementBasis:
    schedule_ref: UUID
    material_state_ref: UUID
    temporal_form_code: str
    starts_at: datetime | None
    ends_at: datetime | None


@dataclass(frozen=True, slots=True)
class ConstraintFinding:
    constraint_ref: UUID
    material_state_ref: UUID
    strength: str
    evaluation: str
    reason_code: str


@dataclass(frozen=True, slots=True)
class DependencyFinding:
    dependency_ref: UUID
    state_ref: UUID
    prerequisite_step_ref: UUID
    dependent_step_ref: UUID
    qualifier_code: str
    evaluation_code: str | None
    actual_material_state_ref: UUID | None
    outcome_material_state_ref: UUID | None
    cycle: bool


@dataclass(frozen=True, slots=True)
class StepDiagnosis:
    step_ref: UUID
    title: str
    activity_ref: UUID | None
    placements: tuple[PlacementBasis, ...]
    constraints: tuple[ConstraintFinding, ...]
    constraint_status: str | None
    hard_set_status: str | None
    dependencies: tuple[DependencyFinding, ...]
    diagnostics: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PlanDiagnosis:
    plan_ref: UUID
    plan_state_ref: UUID
    title: str
    steps: tuple[StepDiagnosis, ...]
    capacity_evaluated: bool = False


class PlanConflictApplication:
    """Compose existing guarded truth without producing candidate or effect rows."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._plans = PlanWorkApplication(session_factory)
        self._dependencies = PlanDependencyApplication(session_factory)
        self._constraints = TemporalConstraintApplication(session_factory)

    async def _placements(
        self, *, self_person_ref: NativeRef, activity_refs: tuple[UUID, ...]
    ) -> dict[UUID, tuple[PlacementBasis, ...]]:
        if not activity_refs:
            return {}
        try:
            async with self._session_factory() as session, session.begin():
                rows = (
                    (await session.execute(
                        _PLACEMENTS,
                        {"self_ref": self_person_ref, "activity_refs": activity_refs},
                    )).mappings().all()
                )
        except SQLAlchemyError as exc:
            raise PlanConflictStateError("Current Schedule could not be read.") from exc
        if len(rows) > 40:
            raise PlanConflictInputError("This diagnosis supports at most 40 current Schedules.")
        result: dict[UUID, list[PlacementBasis]] = {}
        for row in rows:
            result.setdefault(row["activity_ref"], []).append(PlacementBasis(
                schedule_ref=row["schedule_ref"],
                material_state_ref=row["material_state_ref"],
                temporal_form_code=row["temporal_form_code"],
                starts_at=row["starts_at"],
                ends_at=row["ends_at"],
            ))
        return {ref: tuple(items) for ref, items in result.items()}

    async def inspect(
        self, *, self_person_ref: NativeRef, plan_ref: UUID, expected_state_ref: UUID
    ) -> PlanDiagnosis:
        plan = await self._plans.get(self_person_ref=self_person_ref, plan_ref=plan_ref)
        if plan is None:
            raise PlanConflictNotFoundError("Self Plan unavailable.")
        if plan.state_ref != expected_state_ref:
            raise PlanConflictStateError("Plan current state changed. Reload the Plan.")
        if len(plan.steps) > _MAX_STEPS:
            raise PlanConflictInputError("This diagnosis supports at most 20 Steps per Plan.")

        relations = tuple(item for item in await self._dependencies.list(
            self_person_ref=self_person_ref, plan_ref=plan_ref
        ) if item.active)
        if len(relations) > _MAX_DEPENDENCIES:
            raise PlanConflictInputError("This diagnosis supports at most 40 active Dependencies.")
        refs = tuple(dict.fromkeys(
            step.activity_ref for step in plan.steps if step.activity_ref is not None
        ))
        placements = await self._placements(self_person_ref=self_person_ref, activity_refs=refs)
        steps: list[StepDiagnosis] = []
        for step in plan.steps:
            current = placements.get(step.activity_ref, ()) if step.activity_ref else ()
            findings = tuple(DependencyFinding(
                dependency_ref=item.dependency_ref,
                state_ref=item.state_ref,
                prerequisite_step_ref=item.prerequisite_step_ref,
                dependent_step_ref=item.dependent_step_ref,
                qualifier_code=item.qualifier_code,
                evaluation_code=item.evaluation_code,
                actual_material_state_ref=item.actual_material_state_ref,
                outcome_material_state_ref=item.outcome_material_state_ref,
                cycle=item.cycle,
            ) for item in relations if item.dependent_step_ref == step.step_ref)
            codes: list[str] = []
            rules: tuple[ConstraintFinding, ...] = ()
            constraint_status: str | None = None
            hard_set_status: str | None = None
            if step.activity_ref is None:
                codes.append("unlinked_step")
            elif not current:
                codes.append("unknown_basis")
            elif len(current) != 1:
                codes.append("multiple_current_placements")
            elif current[0].temporal_form_code != "absolute" or (
                current[0].starts_at is None or current[0].ends_at is None
            ):
                codes.append("unsupported_placement")
            else:
                assessment = await self._constraints.evaluate_constraints(
                    self_person_ref=self_person_ref,
                    subject_native_ref=NativeRef(step.activity_ref),
                    placement=AbsoluteIntervalPlacement(
                        starts_at=current[0].starts_at, ends_at=current[0].ends_at
                    ),
                )
                constraint_status = assessment.status
                hard_set_status = assessment.hard_set_status
                rules = tuple(ConstraintFinding(
                    constraint_ref=item.constraint_ref,
                    material_state_ref=item.material_state_ref,
                    strength=item.strength,
                    evaluation=item.evaluation,
                    reason_code=item.reason_code,
                ) for item in assessment.items)
                if any(
                    item.strength == "hard" and item.evaluation == "violated" for item in rules
                ):
                    codes.append("known_hard_violation")
                if assessment.status == "not_evaluable" or assessment.hard_set_status != "feasible":
                    codes.append("unknown_basis")
            if any(item.cycle for item in findings):
                codes.append("dependency_cycle")
            if any(item.evaluation_code == "unsatisfied" for item in findings):
                codes.append("blocked_prerequisite")
            if any(item.evaluation_code in {"unknown", None} for item in findings):
                codes.append("unknown_basis")
            if not codes:
                codes.append("no_known_conflict_in_supported_rules")
            steps.append(StepDiagnosis(
                step_ref=step.step_ref, title=step.title, activity_ref=step.activity_ref,
                placements=current, constraints=rules, dependencies=findings,
                constraint_status=constraint_status, hard_set_status=hard_set_status,
                diagnostics=tuple(dict.fromkeys(codes)),
            ))

        refreshed = await self._plans.get(self_person_ref=self_person_ref, plan_ref=plan_ref)
        if refreshed is None or refreshed.state_ref != plan.state_ref:
            raise PlanConflictStateError("Plan changed during diagnosis. Reload and retry.")
        current_relations = tuple(item for item in await self._dependencies.list(
            self_person_ref=self_person_ref, plan_ref=plan_ref
        ) if item.active)
        if current_relations != relations:
            raise PlanConflictStateError("Dependencies changed during diagnosis. Retry.")
        if await self._placements(self_person_ref=self_person_ref, activity_refs=refs) != placements:
            raise PlanConflictStateError("Schedule changed during diagnosis. Retry.")
        return PlanDiagnosis(
            plan_ref=plan.plan_ref, plan_state_ref=plan.state_ref,
            title=plan.title, steps=tuple(steps),
        )
