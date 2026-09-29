"""Bounded, deterministic CP-SAT selector over prevalidated absolute intervals."""

from __future__ import annotations

from dataclasses import dataclass
from importlib.metadata import version
from typing import Literal

from ortools.sat.python import cp_model

SolverStatus = Literal["OPTIMAL", "FEASIBLE", "INFEASIBLE", "MODEL_INVALID", "UNKNOWN"]
MODEL_VERSION = "b12b-fixed-duration-grid-v1"
SOLVER_VERSION = version("ortools")
GRID_SIZE = 97
CENTER_INDEX = 48
MAX_SECONDS_PER_SOLVE = 0.5


@dataclass(frozen=True, slots=True)
class CandidateSelection:
    status: SolverStatus
    indices: tuple[int, ...]


def select_nearby_indices(
    allowed: tuple[int, ...], *, limit: int = 3, max_seconds: float = MAX_SECONDS_PER_SOLVE
) -> CandidateSelection:
    """Choose closest allowed grid positions; a non-optimal result cannot certify ordering."""
    if not 1 <= limit <= 3 or not 0 < max_seconds <= MAX_SECONDS_PER_SOLVE:
        raise ValueError("Candidate solver bounds are invalid.")
    if tuple(sorted(set(allowed))) != allowed or any(not 0 <= item < GRID_SIZE for item in allowed):
        raise ValueError("Candidate grid indices are invalid.")
    if not allowed:
        return CandidateSelection("INFEASIBLE", ())

    model = cp_model.CpModel()
    position = model.new_int_var(0, GRID_SIZE - 1, "start_grid_index")
    distance = model.new_int_var(0, CENTER_INDEX, "shift_grid_steps")
    model.add_allowed_assignments([position], [[value] for value in allowed])
    model.add_abs_equality(distance, position - CENTER_INDEX)
    model.minimize(distance * GRID_SIZE + position)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 0
    solver.parameters.max_time_in_seconds = max_seconds

    results: list[int] = []
    for _ in range(limit):
        status = solver.solve(model)
        if status == cp_model.OPTIMAL:
            chosen = solver.value(position)
            results.append(chosen)
            model.add(position != chosen)
        elif status == cp_model.INFEASIBLE:
            return CandidateSelection("OPTIMAL" if results else "INFEASIBLE", tuple(results))
        elif status == cp_model.FEASIBLE:
            return CandidateSelection("FEASIBLE", tuple(results))
        elif status == cp_model.MODEL_INVALID:
            return CandidateSelection("MODEL_INVALID", ())
        else:
            return CandidateSelection("UNKNOWN", ())
    return CandidateSelection("OPTIMAL", tuple(results))
