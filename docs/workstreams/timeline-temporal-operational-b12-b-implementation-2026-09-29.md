# B12-B — bounded candidate search — implementation checkpoint

- **Status:** implementation checkpoint superseded by the proven B12-B closure
- **Closure evidence:** `timeline-temporal-operational-b12-b-closure-2026-09-29.md`
- **Scope:** `timeline-temporal-operational-b12-b-scope-2026-09-29.md`
- **DB head:** `20260929_92`; no migration
- **Acceptance cadence:** automated B12-B proof here; integrated real-app walkthrough in B12-D

The authenticated Home Plan diagnosis offers “Cerca alternative vicine” beside a linked Step with one current absolute Schedule. The read-only endpoint searches 97 possible starts within ±12 hours, spaced 15 minutes apart, excluding the accepted start, with the original duration fixed. It returns at most three distinct intervals. B04 evaluates current hard and soft Temporal Constraints once per interval from one self-scoped constraint snapshot. OR-Tools 9.15 CP-SAT selects the closest allowed starts with deterministic earlier-start tie breaking. No candidate becomes a Schedule, Proposal or Decision.

The response carries the exact Plan and Schedule MaterialState basis, active qualified Dependency evidence, current Constraint MaterialState references, Movement Policy MaterialState or missing status, horizon, duration, solver version/configuration/status and `capacity_evaluated=false`. A reread of Plan/Dependency/Schedule, Constraints and Movement Policy rejects changed evidence. Unlinked or unsupported placement, uncertain/unsatisfied prerequisite, hard not-evaluable input, bounded infeasibility and solver unknown remain distinct. The UI explicitly says that availability and capacity were not assessed and has no apply action.

## Local checks already run in the implementation worktree

| Check | Result |
| --- | --- |
| OR-Tools finite-grid unit tests and OpenAPI contract | 7 passed |
| Focused Plan UI tests | 3 passed / 2 files |
| Web and generated-client typechecks | PASS / PASS |
| Ruff changed B12-B backend files | PASS |
| Focused mypy on three new backend modules | PASS |

The full backend mypy tree reported pre-existing errors in other temporal modules and one existing Constraint typing path; this checkpoint does not claim a whole-tree mypy pass. The user subsequently passed the focused PostgreSQL/catalog gate; see the closure evidence. No CI or GitHub Actions evidence is claimed.

## Focused user-run gate (completed)

From the repository root, pull `feature/timeline-temporal-operational`, then run:

```bash
cd apps/backend
uv run --locked pytest -q --no-cov --tb=short -m postgres \
  tests/integration/temporal/test_b12_b_plan_candidate.py \
  tests/integration/temporal/test_b12_a_plan_conflict.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py \
  tests/integration/database/test_b11_catalog_reconciliation_probe.py
```

The user ran the generated-source check, two typechecks, focused web tests, API contract/unit tests, Ruff and this PostgreSQL/catalog gate from the same checkout. Exact results are in the B12-B closure. The real-app proof remains at B12-D immediately before parent B12 closure.
