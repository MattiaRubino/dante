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

### Backend production scaffold — CLOSED / INTEGRATED

Historical implementation branch:

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
CLOSED / DIRECT INTEGRATED QA PASS

PR #24
MERGED INTO PROTECTED main
POST-MERGE BACKEND CI PASS
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

Protected `main` requires:

```text
Backend CI Gate
Dependency Review
```

The ruleset also requires the PR branch to be up to date with protected `main` before merge. Both checks are selected from source GitHub Actions.

Repository owner enabled the Actions full-length-SHA requirement. The current connector cannot directly read that setting; it remains explicitly classified as owner-applied / connector-unverifiable.

## CP5 closure evidence

CP5 re-proved the integrated scaffold without adding business schema or changing backend source:

```text
exact branch / current-main relation       PASS
uv 0.12.5                                  PASS
Python 3.14.7                               PASS
locked dependency bootstrap                PASS
Ruff format/lint                           PASS
mypy strict                                PASS
fast pytest                                32/32 PASS
package build                              PASS
canonical PostgreSQL image rebuild         PASS
PostgreSQL acceptance                      18/18 PASS
full backend pytest                        50/50 PASS
full-run coverage                          97.42% evidence only
LOCAL PostgreSQL healthy                   PASS
explicit database provisioning             PASS
real Uvicorn factory startup               PASS
/health/live                               200 PASS
/health/ready                              200 PASS
CP4 required remote workflows              SUCCESS on CP5 PRE-SCOPE
```

One immediate full-suite rerun after the dedicated PostgreSQL suite encountered a Docker Desktop/WSL `/forwards/expose` HTTP 500 during disposable-container port forwarding. The created diagnostic container was removed and the next clean full suite passed 50/50, so no backend/test-harness change was justified.

## Backend scaffold integration evidence

```text
pre-merge main                          ff46eb16b971b1fde96eef9047b09faa02e1a5db
feature/backend-scaffold final HEAD     46b775bfbfc4747daff341d973df133646dbd0c8
PR #24                                  MERGED
merge commit / protected main           41680497c94b0c2f4830679b93f8eb6f1d543f8d
Backend CI push-main run                32502330955 SUCCESS
```

The merge commit has the expected prior-main and final-feature parents. Post-merge readback proved protected `main` contains the scaffold. No CodeQL activation, ruleset mutation, frontend mutation or concrete business schema was included in the merge operation.

## Immediate backend sequence

### 1. Concrete Logical → PostgreSQL implementation

The production backend scaffold is now closed and verified on protected `main`. The next backend boundary is concrete Logical → PostgreSQL mapping through a fresh bounded workstream/gate.

The first step is **not** to create all tables mechanically. It is to consume the closed Logical owner/ref/invariant contracts plus the accepted Physical PostgreSQL posture and propose a coherent concrete mapping.

```text
consume closed Logical owner/ref/invariant contracts
        ↓
consume accepted Physical PostgreSQL constraints
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

### 2. Product vertical slices

Once the first concrete persistence mapping exists, product work proceeds vertically rather than by completing every layer in isolation:

```text
user capability
→ required canonical data
→ domain/application behavior
→ PostgreSQL mapping + migration
→ persistence adapter
→ API boundary
→ frontend consumption
→ end-to-end acceptance
```

Frontend materialization may continue in parallel on its separate worktree.

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

CodeQL remains a separate post-backend-main activation boundary. Backend scaffold integration does not authorize a custom CodeQL workflow or required CodeQL check.

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
CLOSED FEATURE BRANCH != INTEGRATED MAIN UNTIL VERIFIED MERGE
```

Backend scaffold now satisfies the final rule: its protected-main merge and post-merge CI were directly verified.

Continue from durable contracts/handoffs rather than redesigning closed decisions from conversation memory.