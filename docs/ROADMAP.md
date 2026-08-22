# DANTE Roadmap

- Status: **CURRENT**
- Current backend workstream: `feature/logical-postgresql` — **CP6 Concrete Persistence Readiness ACTIVE / DESIGN-FIRST**

## Completed architecture / design sequence

```text
Product / North Star
        CURRENT
          ↓
Domain Model
        CLOSED
          ↓
Logical Model
        CLOSED / 57 OF 57 / WL-H01..WL-H12
          ↓
Pre-Physical Repository & Architecture Coherence
        CLOSED
          ↓
Physical Model / Target Selection
        CLOSED / SELECTED / ACCEPTED
        PostgreSQL 18.4 canonical primary
          ↓
Engineering Foundation v0
        CLOSED / ACCEPTED
          ↓
Frontend Engineering Foundation
        CLOSED / ACCEPTED / FINAL REVIEW PASS
        INTEGRATED VIA PR #22
```

Architecture closure remains distinct from implementation/direct validation.

## Active workstreams

### Backend CP6 — Concrete Persistence Readiness — ACTIVE

Branch:

`feature/logical-postgresql`

CP6 is the bounded transition from the closed Domain/Logical/Physical architecture and closed CP1–CP5 technical backend foundation into a concrete reusable PostgreSQL persistence foundation.

It is **design/readiness**, not Vertical #1 business implementation.

Current sequence:

```text
CP6-00
Authority Reconstruction & Scope Freeze
COMPLETE
        ↓
CP6-01
Concrete Persistence Coverage Map
CLOSED / GATE 01 PASS
        ↓
CP6-02
PostgreSQL Persistence Constitution
NEXT / NOT STARTED
        ↓
CP6-03
Concrete Relational Topology
+ Implementation Dependency DAG
+ Vertical Decomposition
        ↓
CP6-04
Vertical #1 Selection
        ↓
CP6-05
Vertical #1 Exact Persistence Design
        ↓
CP6-06
PostgreSQL Foundation Direct Readiness Proof
only where genuinely executable without speculative business structures
        ↓
CP6-07
Whole Persistence Readiness / Clean-Room QA
        ↓
CP6 CLOSED
```

CP6-01 closure authority:

`docs/development/backend-cp6-01-concrete-persistence-coverage-closure.md`

CP6 must end at:

```text
CONCRETE POSTGRESQL FOUNDATION
CLOSED / READY

VERTICAL #1
SELECTED
EXACTLY DESIGNED
READY FOR IMPLEMENTATION
```

The following belong to the **separate post-CP6 Vertical #1 implementation phase**, not CP6:

```text
business Alembic migration(s)
business SQLAlchemy mappings
persistence adapter
application use case
business API
vertical end-to-end implementation
```

Do not create speculative shared tables/primitives merely to produce direct-proof evidence inside CP6.

### Frontend production materialization — ACTIVE

Branch:

`feature/frontend-materialization`

The closed Frontend Foundation is being materialized under its own bounded workstream. Direct frontend PASS is earned only by its real carried validations; active branch status is not evidence by itself.

Frontend and backend may progress in parallel through separate worktrees. Shared repository/global documentation must be reconciled to the newest current truth rather than restoring stale phase-time status.

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

One immediate full-suite rerun after the dedicated PostgreSQL suite encountered a transient Docker Desktop/WSL `/forwards/expose` HTTP 500 during disposable-container port forwarding. The diagnostic container was removed and the next clean full suite passed 50/50, so no backend/test-harness change was justified.

## Backend scaffold integration evidence

```text
pre-merge main                          ff46eb16b971b1fde96eef9047b09faa02e1a5db
feature/backend-scaffold final HEAD     46b775bfbfc4747daff341d973df133646dbd0c8
PR #24                                  MERGED
merge commit                            41680497c94b0c2f4830679b93f8eb6f1d543f8d
Backend CI push-main run                32502330955 SUCCESS
```

Post-merge readback proved protected `main` contains the scaffold. No concrete business schema was included in that integration.

## CP6 implementation boundary

The PostgreSQL technical substrate already exists through CP2/CP3:

```text
LOCAL PostgreSQL 18.4
selected extension envelope
SQLAlchemy 2 async
psycopg 3
Alembic
schema dante
owner/migrator/runtime role separation
real PostgreSQL acceptance harness
explicit transaction ownership
```

CP6 therefore does **not** need to reselect the database or rebuild technical persistence infrastructure. It must turn the closed semantic/Physical contracts into reusable concrete relational rules, then exactly design the first vertical.

CP6-01 has completed the whole-model persistence coverage and staging map. CP6-02 is now the active next checkpoint and must close the reusable PostgreSQL constitution without leaking into business DDL.

CP6 does not mechanically translate 57 Logical concepts into 57 tables/modules/services.

## Post-CP6 product vertical implementation

After CP6 closes, the first selected vertical proceeds through a separately authorized implementation phase:

```text
CP6 exact Vertical #1 design
        ↓
business migration(s)
        ↓
SQLAlchemy business mapping
        ↓
persistence adapter
        ↓
application behavior
        ↓
API boundary where required
        ↓
frontend consumption where required
        ↓
direct PostgreSQL / system acceptance
```

The exact selected vertical is not assumed in advance; CP6-03/04 determines it from topology and dependencies.

## Capability-triggered Physical implementation

Activate specialist components only at real requirements:

```text
PowerSync + encrypted SQLite
→ real offline/multi-device implementation

PostgreSQL transactional outbox
→ real Class-A async requirement

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

CodeQL remains a separate explicitly authorized boundary. CP6 does not silently activate it.

## Remote environments

```text
LOCAL
→ current implementation context

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
CP3 TECHNICAL QA != BUSINESS-SEMANTIC HG PASS
CLIENT LOCAL STATE != CANONICAL EFFECT AUTHORITY
ENVIRONMENT != GIT BRANCH
WORKFLOW EXISTS != TRUSTED CHECK
TRUSTED CHECK != REQUIRED CHECK UNTIL CALIBRATED
CLOSED FEATURE BRANCH != INTEGRATED MAIN UNTIL VERIFIED MERGE
CP6 READY FOR IMPLEMENTATION != VERTICAL ALREADY IMPLEMENTED
```

Continue from durable contracts/handoffs rather than redesigning closed decisions from conversation memory.