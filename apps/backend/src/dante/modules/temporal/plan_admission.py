"""B12-C reviewed single-candidate admission through guarded PostgreSQL B04-D."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, cast
from uuid import UUID, uuid7

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.sql.elements import TextClause

from dante.modules.temporal.plan_candidate import PlanCandidateApplication, PlanCandidateView
from dante.platform.database.references import NativeRef


class PlanAdmissionStaleError(RuntimeError):
    """The reviewed evidence or candidate is no longer current."""


class PlanAdmissionBlockedError(RuntimeError):
    """Current policy or hard rule blocks this single move."""


class PlanAdmissionNotFoundError(LookupError):
    """Reviewed Plan/Step or pending proposal is unavailable in self scope."""


class PlanAdmissionReuseError(RuntimeError):
    """The operation id was reused for a different review intent."""


@dataclass(frozen=True, slots=True)
class ReviewedMove:
    plan_ref: UUID
    step_ref: UUID
    plan_state_ref: UUID
    schedule_ref: UUID
    schedule_state_ref: UUID
    policy_state_ref: UUID
    basis_fingerprint: str
    starts_at: datetime
    ends_at: datetime
    operation_id: str


@dataclass(frozen=True, slots=True)
class AdmissionResult:
    kind: Literal["committed", "pending_confirmation"]
    schedule_ref: UUID
    proposal_ref: UUID | None
    placement_state_ref: UUID | None
    replayed: bool


_REQUEST = text("""
SELECT * FROM dante.request_self_plan_candidate_move(
  :self_ref,:operation_id,:fingerprint,:plan_ref,:step_ref,:plan_state_ref,
  :schedule_ref,:schedule_state_ref,:policy_state_ref,:starts_at,:ends_at,
  CAST(:dependencies AS jsonb),CAST(:constraints AS jsonb),:proposal_ref,:resulting_ref,:replay_only
)
""")
_ACCEPT = text("""
SELECT * FROM dante.accept_self_plan_candidate_move(
  :self_ref,:operation_id,:fingerprint,:plan_ref,:step_ref,:plan_state_ref,
  :schedule_ref,:schedule_state_ref,:policy_state_ref,
  CAST(:dependencies AS jsonb),CAST(:constraints AS jsonb),:proposal_ref,:replay_only
)
""")


def _fingerprint(review: ReviewedMove, proposal_ref: UUID | None = None) -> str:
    payload = {
        "plan": str(review.plan_ref), "step": str(review.step_ref),
        "plan_state": str(review.plan_state_ref), "schedule": str(review.schedule_ref),
        "schedule_state": str(review.schedule_state_ref), "policy": str(review.policy_state_ref),
        "basis": review.basis_fingerprint,
        "interval": [review.starts_at.isoformat(), review.ends_at.isoformat()],
        "proposal": str(proposal_ref) if proposal_ref else None,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _error(exc: DBAPIError) -> Exception:
    origin = exc.orig
    code = getattr(origin, "sqlstate", None)
    name = getattr(getattr(origin, "diag", None), "constraint_name", None)
    if name == "candidate_receipt_absent":
        return PlanAdmissionNotFoundError("No prior operation receipt.")
    if name in {"schedule_move_automation_blocked", "schedule_move_hard_constraint_violation",
                "schedule_move_not_evaluable"}:
        return PlanAdmissionBlockedError("Policy or hard Temporal Constraint blocks the move.")
    if name in {
        "schedule_move_expected_state", "schedule_move_policy_state",
        "uq_schedule_move_accept_operation_proposal_ref",
    } or code in {"40001", "40P01", "23514"}:
        return PlanAdmissionStaleError("Reviewed evidence changed. Refresh and choose again.")
    if code == "23505":
        return PlanAdmissionReuseError("Operation id already belongs to a different review.")
    if code == "23503":
        return PlanAdmissionNotFoundError("Plan or pending proposal unavailable.")
    return PlanAdmissionStaleError("Reviewed move could not be admitted safely.")


def _basis(view: PlanCandidateView) -> tuple[str, str]:
    dependencies = json.dumps([
        [str(item.dependency_ref), str(item.state_ref), str(item.prerequisite_step_ref),
         str(item.dependent_step_ref),
         item.evaluation_code, str(item.actual_material_state_ref)
         if item.actual_material_state_ref else None,
         str(item.outcome_material_state_ref) if item.outcome_material_state_ref else None]
        for item in sorted(view.all_dependencies, key=lambda item: item.dependency_ref)
    ], separators=(",", ":"))
    constraints = json.dumps([
        [str(ref), str(state) if state else None]
        for ref, state in sorted(view.constraint_states)
    ], separators=(",", ":"))
    return dependencies, constraints


class PlanAdmissionApplication:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._candidates = PlanCandidateApplication(session_factory)

    async def _execute(self, sql: TextClause, values: dict[str, object]) -> dict[str, object]:
        try:
            async with self._session_factory() as session, session.begin():
                result = (await session.execute(sql, values)).mappings().one()
                return dict(result)
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise PlanAdmissionStaleError("Move transaction could not complete safely.") from exc

    async def _current(self, self_ref: NativeRef, review: ReviewedMove) -> PlanCandidateView:
        view = await self._candidates.search(
            self_person_ref=self_ref, plan_ref=review.plan_ref,
            step_ref=review.step_ref, expected_state_ref=review.plan_state_ref,
        )
        if (
            view.basis_fingerprint != review.basis_fingerprint
            or view.placement is None
            or view.placement.schedule_ref != review.schedule_ref
            or view.placement.material_state_ref != review.schedule_state_ref
            or view.movement_policy_material_state_ref != review.policy_state_ref
            or view.basis_status != "supported" or view.solver_status != "OPTIMAL"
            or not any(item.starts_at == review.starts_at and item.ends_at == review.ends_at
                       for item in view.candidates)
        ):
            raise PlanAdmissionStaleError("Candidate or evidence changed. Search again.")
        if view.movement_policy_status != "automatic":
            raise PlanAdmissionBlockedError("Current Movement Policy blocks this move.")
        return view

    async def request(self, *, self_ref: NativeRef, review: ReviewedMove) -> AdmissionResult:
        values: dict[str, object] = {
            "self_ref": self_ref, "operation_id": review.operation_id,
            "fingerprint": _fingerprint(review), "plan_ref": review.plan_ref,
            "step_ref": review.step_ref, "plan_state_ref": review.plan_state_ref,
            "schedule_ref": review.schedule_ref, "schedule_state_ref": review.schedule_state_ref,
            "policy_state_ref": review.policy_state_ref,
            "starts_at": review.starts_at, "ends_at": review.ends_at,
            "dependencies": "[]", "constraints": "[]",
            "proposal_ref": uuid7(), "resulting_ref": uuid7(), "replay_only": True,
        }
        try:
            row = await self._execute(_REQUEST, values)
        except PlanAdmissionNotFoundError as exc:
            if str(exc) != "No prior operation receipt.":
                raise
            current = await self._current(self_ref, review)
            values["dependencies"], values["constraints"] = _basis(current)
            values["replay_only"] = False
            row = await self._execute(_REQUEST, values)
        return AdmissionResult(
            kind=cast(Literal["committed", "pending_confirmation"], str(row["result_kind"])),
            schedule_ref=UUID(str(row["schedule_ref"])),
            proposal_ref=UUID(str(row["proposal_ref"])) if row["proposal_ref"] else None,
            placement_state_ref=UUID(str(row["placement_material_state_ref"]))
            if row["placement_material_state_ref"] else None,
            replayed=bool(row["replayed"]),
        )

    async def accept(
        self, *, self_ref: NativeRef, review: ReviewedMove, proposal_ref: UUID,
    ) -> AdmissionResult:
        values: dict[str, object] = {
            "self_ref": self_ref, "operation_id": review.operation_id,
            "fingerprint": _fingerprint(review, proposal_ref),
            "plan_ref": review.plan_ref, "step_ref": review.step_ref,
            "plan_state_ref": review.plan_state_ref,
            "schedule_ref": review.schedule_ref, "schedule_state_ref": review.schedule_state_ref,
            "policy_state_ref": review.policy_state_ref,
            "dependencies": "[]", "constraints": "[]",
            "proposal_ref": proposal_ref, "replay_only": True,
        }
        try:
            row = await self._execute(_ACCEPT, values)
        except PlanAdmissionNotFoundError as exc:
            if str(exc) != "No prior operation receipt.":
                raise
            current = await self._current(self_ref, review)
            values["dependencies"], values["constraints"] = _basis(current)
            values["replay_only"] = False
            row = await self._execute(_ACCEPT, values)
        return AdmissionResult(
            kind="committed", schedule_ref=UUID(str(row["schedule_ref"])),
            proposal_ref=proposal_ref,
            placement_state_ref=UUID(str(row["placement_material_state_ref"])),
            replayed=bool(row["replayed"]),
        )
