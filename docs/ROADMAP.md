# DANTE Roadmap

- Status: **CURRENT**

## Completed architecture / design sequence

```text
Product / North Star
        CURRENT
          ↓
Domain Model
        CLOSED
          ↓
Logical Model
        CLOSED
          ↓
Pre-Physical Repository & Architecture Coherence
        CLOSED
          ↓
Physical Model / Target Selection
        CLOSED / ACCEPTED
          ↓
Engineering Foundation v0
        CLOSED / ACCEPTED
          ↓
Frontend Engineering Foundation
        CLOSED / ACCEPTED / FINAL REVIEW PASS
        INTEGRATED VIA PR #22
```

Architecture closure remains distinct from implementation/direct validation.

## Active implementation workstreams

### Frontend production materialization — ACTIVE

Branch:

`feature/frontend-materialization`

The closed Frontend Foundation is being materialized under its own bounded workstream. Direct frontend PASS is earned only by the real carried validations; active branch status is not evidence by itself.

Frontend and backend may progress in parallel through separate worktrees. Shared repository/global documentation must be reconciled semantically when either workstream integrates.

### Backend production scaffold — ACTIVE

Branch:

`feature/backend-scaffold`

Current checkpoint truth:

```text
CP1 Python/process/config
CLOSED / DIRECT QA PASS

CP2 reproducible LOCAL PostgreSQL
CLOSED / DIRECT QA PASS

CP3 persistence/migrations/privileges/real PostgreSQL
CLOSED / DIRECT QA PASS

CP4 quality / CI enforcement
CLOSED / DIRECT REMOTE QA PASS

CP5 full scaffold QA / closure
NEXT
```

## CP4 closure evidence

Materialized:

```text
Backend CI
├── Backend Quality
├── Backend PostgreSQL
└── Backend CI Gate

Dependency Review
└── separate repository-wide workflow

Dependabot
├── uv
└── GitHub Actions
```

Real PR #24 calibration:

```text
M5 GREEN
Backend Quality       SUCCESS
Backend PostgreSQL    SUCCESS
Backend CI Gate       SUCCESS
Dependency Review     SUCCESS

M6 DELIBERATE RED
Backend Quality       FAILURE
Backend PostgreSQL    SUCCESS
Backend CI Gate       FAILURE
Dependency Review     FAILURE

M7 RECOVERY GREEN
Backend Quality       SUCCESS
Backend PostgreSQL    SUCCESS
Backend CI Gate       SUCCESS
Dependency Review     SUCCESS
```

M6 proved that the aggregate gate fails when a mandatory upstream job fails while PostgreSQL remains independently diagnostic. Dependency Review failed for an intentional deny rule against a real dependency already visible from `apps/backend/uv.lock`; no vulnerable package was introduced.

Protected `main` now requires:

```text
Backend CI Gate
Dependency Review
```

The ruleset also requires the PR branch to be up to date with protected `main` before merge. Both checks are selected from source GitHub Actions.

Repository owner enabled the Actions full-length-SHA requirement. The current connector cannot directly read that setting; it remains explicitly classified as owner-applied / connector-unverifiable.

## Immediate backend sequence

### 1. CP5 full scaffold QA / closure

CP5 is now the only next backend checkpoint.

It should re-prove the integrated scaffold as a whole without adding business schema:

- exact current branch/main relation;
- clean locked uv bootstrap;
- Python 3.14.7;
- backend process startup;
- `/health/live` and readiness behavior;
- Ruff format/lint;
- mypy strict;
- backend pytest;
- package build;
- canonical `dante-postgres-local:18.4` rebuild;
- PostgreSQL 18.4 + selected extensions;
- SQLAlchemy/psycopg async connection;
- Alembic base → head and drift expectations;
- real PostgreSQL integration harness;
- protected-main required CI contexts remain emitted and green;
- current repository safety/ruleset truth remains coherent.

CP5 must not become a disguised domain/business implementation phase.

### 2. Backend scaffold integration

PR #24 is the active backend integration PR. It must not be merged until a separate explicit merge gate is approved and the relevant required checks are green on the actual merge candidate.

### 3. Concrete Logical → PostgreSQL implementation

Only after scaffold closure:

```text
consume closed Logical owner/ref/invariant contracts
        ↓
propose concrete physical mapping
        ↓
review schema/constraints/indexes/history semantics
        ↓
Alembic migration(s)
        ↓
real PostgreSQL tests
        ↓
persistence/application vertical slice
```

Do not mechanically translate 57 Logical owners into 57 tables/modules/services.

## Product vertical slices

Production product surfaces begin only after the relevant frontend/backend foundations, scaffolds and contracts exist. Prototype UX remains evidence/oracle; production implementation follows accepted feature/data/UI boundaries.

## Capability-triggered Physical implementation

Activate specialist components only at real requirements:

```text
PowerSync + encrypted SQLite
→ real offline/multi-device implementation

R2
→ real ContentArtifact byte flow

OR-Tools
→ solver-backed planning capability

Restate
→ first real Class-B durable workflow

pgBackRest + AWS S3
→ recovery/production boundary or real recovery rehearsal
```

## CodeQL boundary

CodeQL remains a separate post-backend-main activation boundary. CP4 closure does not authorize a custom CodeQL workflow or required CodeQL check.

## Remote environments

```text
LOCAL
→ current implementation boundary

DEV
→ activate when shared remote integration provides real value

UAT
→ activate for real release candidates

PROD
→ activate only at production readiness
```

Backend hosting/compute, IaC and remote sizing remain deliberate decisions at the first real remote-infrastructure boundary.

## Persistent rules

```text
SELECTED ARCHITECTURE != IMPLEMENTED COMPONENT
DOCUMENTATION PASS != DIRECT IMPLEMENTATION PASS
CLIENT LOCAL STATE != CANONICAL EFFECT AUTHORITY
ENVIRONMENT != GIT BRANCH
WORKFLOW EXISTS != TRUSTED CHECK
TRUSTED CHECK != REQUIRED CHECK UNTIL CALIBRATED
```

Continue from durable contracts/handoffs rather than redesigning closed decisions from conversation memory.