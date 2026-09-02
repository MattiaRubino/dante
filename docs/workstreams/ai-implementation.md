# DANTE AI Implementation Workstream

- **Status:** ACTIVE / I0 VALIDATION PENDING
- **Branch:** `feature/ai-architecture`
- **Started:** 2026-09-02
- **Architecture authority:** `../architecture/dante-ai-implementation-baseline-final.md`
- **Post-AI05 acceptance:** `../architecture/dante-ai-post05-final-mega-acceptance.md`
- **Current implementation step:** I0 — repository/application ownership + architecture-test skeleton
- **Current code checkpoint:** `3019b9a97650c50bcc04d33769e79a7d0c75d28e`
- **Implementation claim:** C1 architecture-boundary checks materialized and hardened; I0 NOT CLOSED until repository gates execute cleanly
- **Provider/model/SDK:** OPEN / EVIDENCE-DRIVEN
- **Database/Alembic change:** NONE
- **Production activation:** NONE

Repository truth and executable tests outrank this workstream record.

## 1. Purpose

This workstream turns the accepted DANTE Intelligence architecture into production code without weakening Product/Domain/Logical/Physical/PostgreSQL or AI-02..AI-05 contracts.

The final implementation baseline owns architecture. This file records only current implementation state and the next executable gate.

## 2. Current phase — I0

I0 establishes executable architecture boundaries before Search or Intelligence behavior is implemented.

Current materialization:

```text
apps/backend/tests/unit/test_architecture_boundaries.py
```

The checker currently enforces:

```text
runtime dependencies remain at the accepted pre-provider baseline
Search cannot directly import Intelligence
Search cannot reach Intelligence through an indirect internal dependency path
Intelligence can directly consume Search only through Search public/contracts surfaces
Intelligence cannot indirectly reach private Search implementation
Intelligence cannot import SQLAlchemy or dante.platform.database
Search DB/SQLAlchemy access is restricted to its outbound persistence adapter namespace
FastAPI is restricted to inbound adapters inside Search/Intelligence
production capability modules cannot import eval tooling
forbidden universal AI abstractions EntityRef / Repository / UnitOfWork / entity_id are rejected
```

Implementation properties:

```text
Python stdlib only: ast + tomllib
no production dependency
no dev dependency
no runtime code path
source AST parsed once per test process via functools.cache
internal DANTE import graph resolved from actual source modules
relative and absolute imports normalized
indirect-path failures report the dependency path
```

No empty `modules/search` or `modules/intelligence` package is created at I0. Those paths materialize only when I1/I2 add real implementation content.

## 3. Architecture-testing technology posture

Current 2026 tooling such as Import Linter can enforce forbidden/protected/layer/independence contracts and supports Python 3.14. DANTE does not add it at I0 because the accepted rules are currently small enough to enforce with a deterministic stdlib checker and no additional supply-chain surface.

Re-evaluate a dedicated dependency-graph tool when:

```text
module-graph scale makes the checker materially harder to maintain
cycle/layer diagnostics need richer graph reporting
additional contracts make custom code larger or riskier than the dependency
benchmarking shows a dedicated tool is more reliable at acceptable CI cost
```

Adoption remains evidence-driven rather than stylistic.

## 4. I0 validation gate

I0 may be marked PASS only after the real branch/worktree executes the normal backend gates against the current code checkpoint.

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

The normal repository backend contract also retains the real PostgreSQL acceptance suite. I0 introduces no AI database fixture and no DB/Alembic change.

## 5. Current evidence

Completed:

```text
implementation-entry write gate verified at 5e2c67559670b2bc5780fbcdb3c1aae90975e5ca
initial C1 architecture test commit a6e769c8f79beea6dd531beb899b44cffb699da5
transitive dependency-graph hardening commit 3019b9a97650c50bcc04d33769e79a7d0c75d28e
readback exact
checker syntax compiled independently
synthetic positive baseline PASS
synthetic negative cases caught:
  Search -> Intelligence relative import
  Search -> bridge -> Intelligence indirect path
  Intelligence -> private Search direct import
  Intelligence -> bridge -> private Search indirect path
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

No GitHub Actions run is attached because the existing workflow triggers on protected-main push, pull request to main or manual dispatch, not an ordinary feature-branch push.

## 6. Engineering quality posture

Implementation optimizes for:

```text
correctness before convenience
explicit ownership before abstraction
fail-closed authority/security boundaries
bounded deterministic behavior before provider/model dependence
minimal dependency and supply-chain surface
strict typing and small public APIs
immutable/value-oriented contracts where appropriate
no hidden global mutable state
no blocking request-path I/O disguised as async
bounded deadlines/cancellation/retry behavior
telemetry != audit != canonical truth
performance measured at material boundaries rather than guessed micro-optimization
```

FastAPI process-scoped resources continue to use the existing `lifespan` model. Existing PostgreSQL runtime/pool behavior is unchanged by I0.

## 7. Next step

```text
FIRST: execute and close the real I0 backend gate
THEN: I1 — Search public contracts / eligibility / family registry / deterministic shell
```

I1 must not add a provider dependency, database migration, FTS/vector activation or production HTTP activation.
