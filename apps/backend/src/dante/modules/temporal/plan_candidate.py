"""B12-B read-only, single-Activity candidate search over current self Plan truth."""

from __future__ import annotations

import asyncio
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Literal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.modules.temporal.movement_policy import (
    MovementPolicyApplication,
    MovementPolicyNotFoundError,
    MovementPolicyView,
)
from dante.modules.temporal.plan_candidate_solver import (
    CENTER_INDEX,
    GRID_SIZE,
    MAX_SECONDS_PER_SOLVE,
    MODEL_VERSION,
    SOLVER_VERSION,
    SolverStatus,
    select_nearby_indices,
)
from dante.modules.temporal.plan_conflict import (
    ConstraintFinding,
    DependencyFinding,
    PlacementBasis,
    PlanConflictApplication,
    PlanConflictStateError,
)
from dante.modules.temporal.temporal_constraint import (
    AbsoluteIntervalPlacement,
    TemporalConstraintApplication,
    TemporalConstraintView,
    evaluate_current_constraint_snapshot,
)
from dante.platform.database.references import NativeRef, ScopedRecordRef

GRID_MINUTES = 15
BasisStatus = Literal["supported", "unknown", "blocked", "unsupported"]


class PlanCandidateNotFoundError(LookupError):
    """The self Person cannot inspect the requested Plan/Step."""


@dataclass(frozen=True, slots=True)
class CandidateInterval:
    starts_at: datetime
    ends_at: datetime
    grid_index: int
    soft_findings: tuple[ConstraintFinding, ...]


@dataclass(frozen=True, slots=True)
class PlanCandidateView:
    plan_ref: UUID
    plan_state_ref: UUID
    step_ref: UUID
    step_title: str
    activity_ref: UUID | None
    placement: PlacementBasis | None
    dependencies: tuple[DependencyFinding, ...]
    all_dependencies: tuple[DependencyFinding, ...]
    constraint_states: tuple[tuple[UUID, UUID | None], ...]
    movement_policy_material_state_ref: UUID | None
    movement_policy_status: Literal["automatic", "blocked", "missing"]
    basis_status: BasisStatus
    reason_code: str
    solver_status: SolverStatus | None
    candidates: tuple[CandidateInterval, ...]
    horizon_starts_at: datetime | None
    horizon_ends_at: datetime | None
    duration_microseconds: int | None
    grid_minutes: int = GRID_MINUTES
    grid_size: int = GRID_SIZE
    max_seconds_per_solve: float = MAX_SECONDS_PER_SOLVE
    model_version: str = MODEL_VERSION
    solver_version: str = SOLVER_VERSION
    capacity_evaluated: bool = False

    @property
    def basis_fingerprint(self) -> str:
        """Stable review token for the exact current evidence and finite model result."""
        placement = self.placement
        payload = {
            "plan": str(self.plan_ref), "state": str(self.plan_state_ref),
            "step": str(self.step_ref), "activity": str(self.activity_ref),
            "schedule": None if placement is None else [
                str(placement.schedule_ref), str(placement.material_state_ref),
                placement.temporal_form_code,
                placement.starts_at.isoformat() if placement.starts_at else None,
                placement.ends_at.isoformat() if placement.ends_at else None,
            ],
            "dependencies": [[
                str(item.dependency_ref), str(item.state_ref),
                str(item.prerequisite_step_ref), str(item.dependent_step_ref),
                item.qualifier_code,
                item.evaluation_code, str(item.actual_material_state_ref),
                str(item.outcome_material_state_ref), item.cycle,
            ] for item in self.all_dependencies],
            "constraints": [[str(ref), str(state)] for ref, state in self.constraint_states],
            "policy": [str(self.movement_policy_material_state_ref), self.movement_policy_status],
            "status": [self.basis_status, self.solver_status],
            "model": [self.model_version, self.solver_version, self.grid_minutes, self.grid_size],
            "horizon": [str(self.horizon_starts_at), str(self.horizon_ends_at),
                        self.duration_microseconds],
            "candidates": [[item.starts_at.isoformat(), item.ends_at.isoformat()]
                           for item in self.candidates],
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _constraint_basis(
    values: list[TemporalConstraintView],
) -> tuple[tuple[UUID, UUID | None], ...]:
    return tuple(
        (item.constraint_ref, item.current_rule.material_state_ref if item.current_rule else None)
        for item in values
    )


class PlanCandidateApplication:
    """Read material truth, solve a tiny finite model, and verify the read basis again."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._plans = PlanConflictApplication(session_factory)
        self._constraints = TemporalConstraintApplication(session_factory)
        self._policies = MovementPolicyApplication(session_factory)

    async def _policy(
        self, *, self_person_ref: NativeRef, placement: PlacementBasis | None
    ) -> MovementPolicyView | None:
        if placement is None:
            return None
        try:
            return await self._policies.get_policy(
                self_person_ref=self_person_ref,
                schedule_ref=ScopedRecordRef(placement.schedule_ref),
            )
        except MovementPolicyNotFoundError:
            return None

    async def search(
        self, *, self_person_ref: NativeRef, plan_ref: UUID,
        step_ref: UUID, expected_state_ref: UUID,
    ) -> PlanCandidateView:
        diagnosis = await self._plans.inspect(
            self_person_ref=self_person_ref, plan_ref=plan_ref,
            expected_state_ref=expected_state_ref,
        )
        step = next((item for item in diagnosis.steps if item.step_ref == step_ref), None)
        if step is None:
            raise PlanCandidateNotFoundError("Plan Step unavailable.")
        placement = step.placements[0] if len(step.placements) == 1 else None
        policy = await self._policy(self_person_ref=self_person_ref, placement=placement)
        policy_status: Literal["automatic", "blocked", "missing"] = (
            policy.rule.automatic_movement if policy else "missing"
        )

        basis_status: BasisStatus = "supported"
        reason = "supported_rules_only"
        if step.activity_ref is None or len(step.placements) != 1 or placement is None:
            basis_status, reason = "unsupported", "linked_absolute_schedule_required"
        elif placement.temporal_form_code != "absolute" or (
            placement.starts_at is None or placement.ends_at is None
        ):
            basis_status, reason = "unsupported", "absolute_interval_required"
        elif any(item.cycle or item.evaluation_code in {"unknown", None}
                 for item in step.dependencies):
            basis_status, reason = "unknown", "prerequisite_unknown"
        elif any(item.evaluation_code == "unsatisfied" for item in step.dependencies):
            basis_status, reason = "blocked", "prerequisite_unsatisfied"

        constraints: list[TemporalConstraintView] = []
        candidates: tuple[CandidateInterval, ...] = ()
        solver_status: SolverStatus | None = None
        horizon_start: datetime | None = None
        horizon_end: datetime | None = None
        duration_us: int | None = None
        if (
            basis_status == "supported" and placement is not None
            and placement.starts_at is not None and placement.ends_at is not None
            and step.activity_ref is not None
        ):
            constraints = await self._constraints.list_constraints_by_subject(
                self_person_ref=self_person_ref,
                subject_native_ref=NativeRef(step.activity_ref),
            )
            duration = placement.ends_at - placement.starts_at
            duration_us = (duration.days * 86_400 + duration.seconds) * 1_000_000 + duration.microseconds
            horizon_start = placement.starts_at - timedelta(hours=12)
            horizon_end = placement.starts_at + timedelta(hours=12)
            options: dict[int, tuple[ConstraintFinding, ...]] = {}
            incomplete = False
            for index in range(GRID_SIZE):
                if index == CENTER_INDEX:
                    continue  # The current placement is a baseline, never an alternative.
                start = horizon_start + timedelta(minutes=index * GRID_MINUTES)
                assessment = evaluate_current_constraint_snapshot(
                    subject_native_ref=NativeRef(step.activity_ref),
                    placement=AbsoluteIntervalPlacement(start, start + duration),
                    constraints=constraints,
                )
                if assessment.hard_set_status == "undetermined" or assessment.status == "not_evaluable":
                    incomplete = True
                    continue
                if assessment.hard_set_status != "feasible" or assessment.status == "inadmissible":
                    continue
                options[index] = tuple(ConstraintFinding(
                    constraint_ref=item.constraint_ref,
                    material_state_ref=item.material_state_ref,
                    strength=item.strength,
                    evaluation=item.evaluation,
                    reason_code=item.reason_code,
                ) for item in assessment.items if item.strength == "soft")
            if incomplete:
                basis_status, reason, solver_status = "unknown", "hard_rule_not_evaluable", "UNKNOWN"
            else:
                selection = await asyncio.to_thread(select_nearby_indices, tuple(options))
                solver_status = selection.status
                candidates = tuple(CandidateInterval(
                    starts_at=horizon_start + timedelta(minutes=index * GRID_MINUTES),
                    ends_at=horizon_start + timedelta(minutes=index * GRID_MINUTES) + duration,
                    grid_index=index, soft_findings=options[index],
                ) for index in selection.indices)
                if selection.status == "INFEASIBLE":
                    reason = "no_fixed_duration_grid_candidate"
                elif selection.status in {"UNKNOWN", "MODEL_INVALID"}:
                    reason = "solver_unresolved"

        refreshed = await self._plans.inspect(
            self_person_ref=self_person_ref, plan_ref=plan_ref,
            expected_state_ref=expected_state_ref,
        )
        current_step = next((item for item in refreshed.steps if item.step_ref == step_ref), None)
        if current_step != step:
            raise PlanConflictStateError("Plan candidate basis changed. Retry.")
        if step.activity_ref is not None and horizon_start is not None:
            current_constraints = await self._constraints.list_constraints_by_subject(
                self_person_ref=self_person_ref,
                subject_native_ref=NativeRef(step.activity_ref),
            )
            if current_constraints != constraints:
                raise PlanConflictStateError("Temporal Constraints changed. Retry.")
        if await self._policy(self_person_ref=self_person_ref, placement=placement) != policy:
            raise PlanConflictStateError("Movement Policy changed. Retry.")
        return PlanCandidateView(
            plan_ref=plan_ref, plan_state_ref=expected_state_ref,
            step_ref=step_ref, step_title=step.title, activity_ref=step.activity_ref,
            placement=placement, dependencies=step.dependencies,
            all_dependencies=tuple(item for current in diagnosis.steps
                                   for item in current.dependencies),
            constraint_states=_constraint_basis(constraints),
            movement_policy_material_state_ref=policy.material_state_ref if policy else None,
            movement_policy_status=policy_status,
            basis_status=basis_status, reason_code=reason, solver_status=solver_status,
            candidates=candidates, horizon_starts_at=horizon_start,
            horizon_ends_at=horizon_end, duration_microseconds=duration_us,
        )
