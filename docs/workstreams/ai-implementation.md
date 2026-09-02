# DANTE AI Implementation Workstream

- **Status:** ACTIVE / I0 VALIDATION PENDING
- **Branch:** `feature/ai-architecture`
- **Started:** 2026-09-02
- **Architecture authority:** `../architecture/dante-ai-implementation-baseline-final.md`
- **Post-AI05 acceptance:** `../architecture/dante-ai-post05-final-mega-acceptance.md`
- **Current implementation step:** I0 — repository/application ownership + architecture-test skeleton
- **Current code checkpoint:** `a6e769c8f79beea6dd531beb899b44cffb699da5`
- **Implementation claim:** C1 architecture-boundary checks materialized; I0 NOT CLOSED until repository gates execute cleanly
- **Provider/model/SDK:** OPEN / EVIDENCE-DRIVEN
- **Database/Alembic change:** NONE
- **Production activation:** NONE

Repository truth and executable tests outrank this workstream record.

## 1. Purpose

This workstream turns the accepted DANTE Intelligence architecture into production code without weakening the Product/Domain/Logical/Physical/PostgreSQL or AI-02..AI-05 contracts.

The current implementation order is governed by the final baseline. This file records only present implementation state and the next executable gate; it is not a second architecture specification.

## 2. Current phase — I0

I0 establishes executable architecture boundaries before Search or Intelligence behavior is implemented.

Current materialization:

```text
apps/backend/tests/unit/test_architecture_boundaries.py
```

The test currently enforces:

```text
runtime dependency set remains at the accepted pre-provider baseline
Search cannot import Intelligence
Intelligence can consume Search only through Search public/contracts surfaces
Intelligence cannot import SQLAlchemy or dante.platform.database
Search DB/SQLAlchemy access is restricted to its outbound persistence adapter namespace
FastAPI is restricted to inbound adapters inside Search/Intelligence
production capability modules cannot import eval tooling
forbidden universal AI abstractions such as EntityRef / Repository / UnitOfWork / entity_id are rejected
```

The checker uses only Python stdlib `ast` + `tomllib`, caches source parsing for the test process and adds zero production-runtime overhead.

No empty `modules/search` or `modules/intelligence` package was created at I0. Those paths materialize only when I1/I2 add real implementation content.

## 3. Why no architecture-test framework yet

Current 2026 tooling such as Import Linter can enforce forbidden/protected/layer/independence contracts and supports Python 3.14. I0 deliberately does not add it yet because the accepted boundaries can currently be enforced with a small deterministic stdlib checker and no new dependency.

Reconsider a dedicated dependency-graph tool when one of these becomes true:

```text
indirect dependency paths become materially difficult to review
module graph size makes the stdlib checker hard to maintain
cycle/layer diagnostics need richer graph reporting
custom boundary logic becomes larger than the dependency it avoids
```

Adoption remains evidence-driven rather than stylistic.

## 4. I0 validation gate

I0 may be marked PASS only after the real branch/worktree executes the normal backend gates against the materialized commit.

Required fast gate:

```text
cd apps/backend
uv lock --check
uv sync --locked
uv run --locked ruff format --check .
uv run --locked ruff check .
uv run --locked mypy
uv run --locked pytest tests/unit/test_architecture_boundaries.py -vv
uv run --locked pytest -m "not postgres"
uv build
```

The repository-wide backend contract also retains the real PostgreSQL acceptance suite. Because I0 changes no DB/runtime behavior, no special AI database fixture is introduced; existing PostgreSQL gates must remain green before broader integration.

## 5. Current evidence

Completed:

```text
branch write gate verified at 5e2c67559670b2bc5780fbcdb3c1aae90975e5ca
C1 commit created at a6e769c8f79beea6dd531beb899b44cffb699da5
readback exact
PRE-SCOPE..HEAD diff = one added architecture-test file only
checker syntax compiled independently
synthetic negative cases confirmed for:
  Search -> Intelligence relative import
  Intelligence -> private Search import
  Intelligence -> SQLAlchemy
  Search application -> DB runtime
  FastAPI inside Intelligence core
  universal EntityRef introduction
  provider runtime dependency addition
```

Not yet claimed:

```text
ruff PASS on real worktree
mypy PASS on real worktree
pytest PASS on real worktree
build PASS on real worktree
PostgreSQL suite PASS at this checkpoint
I0 CLOSED
```

No GitHub Actions run is attached to the C1 commit because the existing workflow triggers on protected-main push, pull request to main, or manual dispatch rather than ordinary feature-branch push.

## 6. Quality posture

Implementation must optimize for:

```text
correctness before convenience
explicit ownership before abstraction
fail-closed authority/security boundaries
bounded deterministic behavior before provider/model dependence
minimal dependency surface
strict typing
small public APIs
immutable/value-oriented contracts where appropriate
no hidden global mutable state
no request-path blocking I/O disguised as async
bounded time/deadline/cancellation behavior
observability without turning telemetry into audit/canonical truth
performance measured at material boundaries rather than micro-optimized by guess
```

FastAPI process-scoped resources continue to use the existing `lifespan` ownership model. Existing PostgreSQL runtime/pool behavior is not changed by I0.

## 7. Next step

```text
FIRST: close I0 only after the real backend gate passes
THEN: I1 — Search public contracts / eligibility / family registry / deterministic shell
```

I1 must not add a provider dependency, database migration, FTS/vector activation or production HTTP activation.
