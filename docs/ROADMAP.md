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
        PostgreSQL 18 major family canonical
        exact Physical phase-time patch 18.4
          ↓
Engineering Foundation v0
        CLOSED / ACCEPTED
          ↓
Frontend Engineering Foundation
        CLOSED / ACCEPTED / FINAL REVIEW PASS
        INTEGRATED VIA PR #22
```

Architecture closure remains distinct from implementation/direct validation. PostgreSQL patch maintenance within accepted major line 18 does not reopen the Physical selection.

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
CLOSED / GATE 02 PASS
PostgreSQL 18.6 technical refresh DIRECT REMOTE QA PASS
        ↓
CP6-03
Concrete Relational Topology
+ Implementation Dependency DAG
+ Vertical Decomposition
NEXT / NOT STARTED
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

CP6-02 closed Constitution:

`docs/development/backend-cp6-02-postgresql-persistence-constitution.md`

CP6-02 closure authority:

`docs/development/backend-cp6-02-postgresql-persistence-constitution-closure.md`

Retained CP6-02 technical evidence:

```text
PostgreSQL architecture              major 18
Physical/CP2/CP3 exact evidence      18.4 / historical
current technical patch              18.6
configuration refresh                APPLIED
Backend CI run                       32568664940
executed HEAD                        ec3dc795b5e044daa3a77723c94a1b4b5b92865c
Backend Quality                      SUCCESS / 32 fast tests PASS
Backend PostgreSQL                   SUCCESS / 18 PostgreSQL tests PASS
Backend CI Gate                      SUCCESS
18.6 release-note impact             PASS / NO CURRENT POST-UPGRADE ACTION
```

The immediate next action is **CP6-03 read/research/design-first**. Gate 02 closes global PostgreSQL doctrine; it does not authorize business DDL, business mappings/adapters or Vertical #1 implementation.

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
ORIGINAL POSTGRESQL 18.4 EVIDENCE

CP3 persistence/migrations/privileges/real PostgreSQL
CLOSED / DIRECT QA PASS
ORIGINAL POSTGRESQL 18.4 EVIDENCE

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

## Historical CP5 closure evidence

CP5 re-proved the integrated scaffold against the then-current PostgreSQL 18.4 image without adding business schema or changing backend source:

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

The PostgreSQL technical substrate already exists through CP2/CP3 and has now been re-proved on the current maintenance patch:

```text
PostgreSQL architecture             major 18
Physical exact patch                18.4 / phase-time
CP2/CP3 original LOCAL envelope     18.4 / historical direct PASS
current LOCAL/CI envelope           18.6 / direct remote regression PASS
selected extension envelope         PostGIS 3.6.4 + pgvector 0.8.6 + native capabilities
SQLAlchemy 2 async
psycopg 3
Alembic
schema dante
owner/migrator/runtime role separation
real PostgreSQL acceptance harness
explicit transaction ownership
```

CP6 therefore does **not** need to reselect the database or rebuild technical persistence infrastructure. It must turn the closed semantic/Physical contracts into reusable concrete relational rules, then exactly design the first vertical.

CP6-01 closed the whole-model persistence coverage and staging map. CP6-02 has now **closed the reusable PostgreSQL Constitution at Gate 02** after the 18.6 technical reproof, external benchmark, independent review, repair and targeted clean verification. CP6-03 now consumes that closed doctrine to build the concrete relational family topology, dependency DAG and vertical decomposition.

CP6 does not mechanically translate 57 Logical concepts into 57 tables/modules/services.

## PostgreSQL 18.6 maintenance evidence

CP6 updated only the PostgreSQL patch-level technical envelope from 18.4 to 18.6; it did not change the selected major family or business schema.

```text
run                                  32568664940
HEAD                                 ec3dc795b5e044daa3a77723c94a1b4b5b92865c
PostgreSQL image build               PASS
PostgreSQL 18.6 exact harness        PASS
PostGIS 3.6.4                        PASS
pgvector 0.8.6                       PASS
Backend Quality                      SUCCESS
fast tests                           32/32 PASS
Backend PostgreSQL                   SUCCESS
PostgreSQL tests                     18/18 PASS
Backend CI Gate                      SUCCESS
complete test corpus                 50/50 across the two mandatory lanes
```

Release-note impact review: **PASS / NO CURRENT POST-UPGRADE ACTION**. Current DANTE has no custom logical-decoding output plugin, `pgcrypto`, business GIN index, `btree_gist` or `ltree` object requiring 18.6-specific cleanup. Future PowerSync/logical-replication activation must review `output_plugin_libraries` and then-current PostgreSQL maintenance notes.

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
→ at activation, re-check PostgreSQL logical-replication/output_plugin_libraries requirements

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
POSTGRESQL PATCH REFRESH != PHYSICAL ARCHITECTURE REOPEN
HISTORICAL 18.4 EVIDENCE != CURRENT 18.6 RUNTIME CLAIM
CLIENT LOCAL STATE != CANONICAL EFFECT AUTHORITY
ENVIRONMENT != GIT BRANCH
WORKFLOW EXISTS != TRUSTED CHECK
TRUSTED CHECK != REQUIRED CHECK UNTIL CALIBRATED
CLOSED FEATURE BRANCH != INTEGRATED MAIN UNTIL VERIFIED MERGE
CP6 READY FOR IMPLEMENTATION != VERTICAL ALREADY IMPLEMENTED
```

Continue from durable contracts/handoffs rather than redesigning closed decisions from conversation memory.
