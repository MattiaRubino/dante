> **CURRENT MAIN + CP6 RECONCILIATION — 2026-08-26**
> Protected `main` anchor imported by this alignment is `87fe668c2ade78b17e0326d635e4d7a67920ae8a`. Its post-merge truth is preserved: frontend materialization/integration is **CLOSED / INTEGRATED via PR #28**, deterministic Frontend CI compatibility repair is integrated via PR #37, and the clean Home B2 v27 React handoff is integrated via PR #36. The main-only frontend contracts, fixtures, tokens and pre-production guard remain byte-identical to that protected-main anchor.
> Backend CP6 is independently **CLOSED / CONCRETE POSTGRESQL DATABASE PASS**. Accepted implementation HEAD is `22bbc078391d52c43665474bf465593d6225106e`; closure-documentation branch anchor before this alignment is `8c33c897ff57cfff9130fe00db1854470aa06bb5`; persistent LOCAL PostgreSQL 18.6 is at Alembic `20260826_08`; verified topology remains `68 tables / 5 views / 14 routines / 75 triggers / 95 indexes / 68 FKs / 120 CHECKs`.
> This overlay supersedes only contradictory **current status, routing, branch and next-step prose** later in this file. Historical evidence, accepted architecture, frontend product contracts, failed-run/repair evidence and phase-time records remain historical truth and are not rewritten. The aligned feature branch is only a candidate for protected-main integration: **no final merge into `main` is authorized by this overlay**. Protected-main integration still requires the normal PR, current-head required checks and a separate final merge gate.

> **CURRENT INTEGRATION RECONCILIATION — 2026-08-24**  
> Protected `main` includes the closed frontend materialization via merged PR #28. Frontend materialization is **CLOSED / PASS / INTEGRATED**; any later text that still says it proceeds independently on `feature/frontend-materialization` is pre-merge status. Backend `feature/logical-postgresql` is current with `main` and remains CP6-03 ACTIVE with Checkpoint J / DB-U23 CLOSED, active Database Reference Parts 1–8, `DB-U08 / DB-U15 / DB-U21` OPEN, exact next block = **FINAL ACTUAL POSTGRESQL OBJECT INVENTORY**, Gate 03 not earned, CP6-04 not authorized. This banner supersedes only contradictory status/routing text below.  

# DANTE System Overview

- Status: **CURRENT ARCHITECTURE / IMPLEMENTATION-BOUNDARY OVERVIEW**
- Current backend progression: **CP1–CP5 CLOSED / INTEGRATED / DIRECT QA PASS; CP6 ACTIVE; CP6-01 CLOSED / GATE 01 PASS; CP6-02 CLOSED / GATE 02 PASS; CP6-03 ACTIVE / CHECKPOINT J + DB-U23 CLOSED / FINAL ACTUAL POSTGRESQL OBJECT INVENTORY NEXT**
- Current CP6 branch: `feature/logical-postgresql`
- Current PostgreSQL technical patch: **18.6 / DIRECT REMOTE FOUNDATION REGRESSION PASS**

## 1. Product and authority

DANTE is a personal operating system whose canonical truth represents real life over time while preserving authority, provenance, uncertainty and distinctions between intention, execution and outcome.

Compass: **Understand life. Shape what comes next.**

Implementation consumes closed Product/Domain/Logical/Physical models and closed engineering foundations. Framework or storage convenience does not redefine accepted semantics.

Core invariants include:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
provider state != canonical DANTE state
derived projection != canonical truth
absence/unknown != false
MaterialStateRef != ETag/MVCC/provider revision
idempotency != semantic identity
AI/solver output != accepted canonical effect
client local state != canonical accepted effect
```

`WL-H01..WL-H12` remain active.

## 2. Repository / application topology

One product monorepo:

```text
DANTE repository
│
├── apps/backend
├── apps/web
├── apps/mobile
├── packages
├── infra
├── tooling
├── tests/system
├── docs
├── prototypes
└── .github
```

Backend accepted internal shape:

```text
apps/backend/src/dante
├── bootstrap
├── kernel
├── platform
└── modules/<capability>
    ├── domain
    ├── application
    ├── ports
    └── adapters
        ├── inbound/http
        └── outbound/persistence|integrations
```

FastAPI is an inbound adapter/process host. SQLAlchemy/provider/runtime objects stay outside Domain identity. Capability boundaries are behavior/cohesion based, not one owner/table/route per module.

## 3. Backend technical foundation

```text
CP1 process/config foundation                   CLOSED / DIRECT QA PASS
CP2 LOCAL PostgreSQL 18.4                       CLOSED / DIRECT QA PASS / HISTORICAL EXACT
CP3 persistence/migrations/privileges 18.4      CLOSED / DIRECT QA PASS / HISTORICAL EXACT
CP4 CI enforcement                              CLOSED / DIRECT REMOTE QA PASS
CP5 integrated scaffold QA                      CLOSED / DIRECT INTEGRATED QA PASS
PR #24                                          MERGED / POST-MERGE CI PASS
PostgreSQL 18.6 technical refresh               APPLIED
PostgreSQL 18.6 foundation regression           DIRECT REMOTE QA PASS
```

CP3 already materializes:

```text
SQLAlchemy async
psycopg 3
Alembic
schema dante
owner / migrator / runtime role separation
explicit transaction ownership
real PostgreSQL acceptance harness
```

It deliberately started with no DANTE business persistence mapping. CP6 now builds that concrete database from the closed model.

## 4. Canonical persistence authority

```text
PostgreSQL 18 major family
SOLE CANONICAL PERSISTENCE / MATERIAL-HISTORY AUTHORITY

Physical phase-time exact patch   18.4
CP2/CP3 original direct evidence  18.4 / historical exact
current technical patch           18.6
18.6 technical regression         DIRECT REMOTE QA PASS
```

Selected PostgreSQL capabilities remain PostGIS 3.6.4, pgvector 0.8.6, native FTS, `pg_trgm`, `unaccent`, `pg_stat_statements` and bounded PgBouncer posture.

Accepted relational thesis:

```text
owner-specific canonical families
+ owner-specific material-state/history families
+ specific typed relation families
+ bounded technical address/control structures only where genuine heterogeneous addressing requires them
+ separate provider / derived / runtime concerns
```

Rejected globally:

```text
universal Entity / Thing
universal Relationship / generic edge
canonical EAV/property bag
universal event ontology
universal Fact/Version semantic payload root
JSONB required-semantic escape hatch
```

## 5. Reference / material-state architecture

Reference families remain distinct:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

Closed PostgreSQL rules:

```text
homogeneous NativeRef
→ direct FK

genuinely heterogeneous NativeRef
→ bounded native-address anchor

MaterialStateRef
→ PostgreSQL uuid / UUIDv7 stable address
→ bounded material-state address/control
→ exact owner + facet
→ owner-specific material-state row
→ explicit current accepted-state binding where required
```

Provider revisions, MVCC tokens, timestamps and ETags do not become MaterialStateRef.

## 6. CP6 — Concrete PostgreSQL Database

CP6's current execution scope is owned by:

`docs/workstreams/logical-postgresql.md`

CP6 does **not** repeat Domain, Logical or Physical modeling.

Closed checkpoints:

```text
CP6-00  COMPLETE
CP6-01  CLOSED / GATE 01 PASS
CP6-02  CLOSED / GATE 02 PASS
```

Current remaining sequence:

```text
CP6-03
WHOLE DANTE DATABASE BLUEPRINT
CURRENT: Checkpoint J / DB-U23 closed
NEXT: Final Actual PostgreSQL Object Inventory
DB-U08 / DB-U15 / DB-U21 remain open
second full tombstone audit required before Gate 03
        ↓
GATE 03
        ↓
CP6-04
WHOLE DANTE DATABASE MATERIALIZATION
        ↓
CP6-05
WHOLE DATABASE DIRECT QA + CP6 CLOSURE
        ↓
POST-CP6
FIRST PRODUCT VERTICAL APPLICATION PHASE
```

This replaces the earlier process plan that put Vertical #1 selection/design inside CP6 and prohibited all business-database materialization.

The closed CP6-02 Constitution remains technical authority. Only its old process/staging prose is superseded where it conflicts with the current workstream.

### CP6-03 — blueprint

The active Database Architecture & Reference is one canonical authority across `docs/database/dante-postgresql-database.md` and Parts 2–8. Checkpoint J repaired the first total pre-freeze audit and closed `DB-U23`; the final actual PostgreSQL object inventory itself is not yet frozen.

CP6-03 derives, for the full closed model where applicable:

```text
concrete tables/families
columns + PostgreSQL types
PK / FK / reference-family integrity
UNIQUE / CHECK / EXCLUDE / temporal constraints
NativeRef / ScopedRecordRef / MaterialStateRef topology
current-state bindings
owner-specific history/material-state topology
specific relation topology
provider / derived DB structures already required
provenance/governance persistence structures
structural indexes
privilege posture
SQLAlchemy mapping plan
implementation/migration dependency DAG
real PostgreSQL test plan
```

Exact remaining design order:

```text
Final Actual PostgreSQL Object Inventory
→ DB-U08 exact names
→ DB-U15 exact index matrix
→ DB-U21 exact object privilege matrix
→ migration/materialization DAG
→ SQLAlchemy mapping plan
→ Database Dictionary readiness
→ direct PostgreSQL proof plan
→ SECOND FULL TOMBSTONE AUDIT FROM ZERO
→ Gate 03
```

### CP6-04 — materialization

After Gate 03 **and a separate explicit materialization gate**, CP6 may materially implement the approved DANTE database through exact write gates:

```text
Alembic business-schema migrations
DANTE business tables
bounded address/control structures
owner-specific canonical and history tables
specific relation tables
constraints / indexes
SQLAlchemy database mappings
object ownership / grants
real PostgreSQL DB tests
```

### CP6-05 — direct QA / closure

CP6-05 proves the materialized DB against the closed model and blueprint using real PostgreSQL where PostgreSQL semantics are involved.

CP6 closes only when the DANTE database is:

```text
BLUEPRINT COMPLETE
MATERIALIZED TO MAXIMUM NON-SPECULATIVE EXTENT
MIGRATED
MAPPED
DIRECTLY TESTED
QA CLEAN
```

## 7. Boundary to first product vertical

Database materialization is not the same thing as first-product-vertical application implementation.

Out of CP6:

```text
first-product-vertical application use cases
application services
product persistence adapters that encode application behavior
business API routes
frontend behavior
product workflow orchestration
```

The first product vertical starts only after CP6 closes and consumes the already-materialized database. A later real requirement may evolve the DB normally, but determinable schema is not postponed by default.

## 8. Frontend / client data authority

Frontend Data Authority Matrix remains:

```text
canonical accepted state/effect   backend + PostgreSQL
synced local projection           PowerSync/SQLite noncanonical
offline pending mutation          local staging only
offline acceptance                backend governance/conflict checks
remote request state              TanStack Query + typed API
online governed command           FastAPI/backend
form draft                        TanStack Form
component transient               React
cross-tree transient              Zustand only when justified
```

Local arrival/staging never defines canonical truth.

Frontend production materialization proceeds independently on `feature/frontend-materialization`.

## 9. Offline / specialist capabilities

Selected Physical targets remain bounded by real activation triggers.

```text
PowerSync + encrypted SQLite      offline/sync consumer required
PgBouncer                         real connection-pressure value
PostgreSQL outbox                 real Class-A async requirement
Restate                           real Class-B durable workflow
Cloudflare R2                     real ContentArtifact byte flow
pgBackRest + S3                   recovery/production boundary or rehearsal
OR-Tools                          solver-backed capability
```

A PostgreSQL-native DB structure required by the concrete DANTE schema may be materialized in CP6 without automatically activating the surrounding runtime/product capability.

## 10. Transactions / migrations / privileges

Frozen CP3 posture remains:

```text
one AsyncEngine per process
one async_sessionmaker per process
one AsyncSession per application operation
autobegin=False
autoflush=True
expire_on_commit=False
outer application operation owns transaction
adapter may flush / never implicit commit
READ COMMITTED default
one Alembic DAG / one canonical head
metadata.create_all() not deployment authority

dante_owner      NOLOGIN
dante_migrator   LOGIN NOINHERIT + bounded SET ROLE
dante_runtime    LOGIN NOINHERIT / runtime DML posture
```

CP6-02's transaction, idempotency, migration and privilege doctrine remains closed and applies to the real database materialized in CP6-04.

## 11. Current direct evidence

```text
Backend CI run                32568664940
workflow event                workflow_dispatch
executed HEAD                 ec3dc795b5e044daa3a77723c94a1b4b5b92865c
PostgreSQL 18.6 image         PASS
PostGIS 3.6.4                 PASS
pgvector 0.8.6                PASS
Backend Quality               SUCCESS / 32 tests PASS
Backend PostgreSQL            SUCCESS / 18 tests PASS
Backend CI Gate               SUCCESS
current corpus                50 / 50 covered across mandatory lanes
release-note impact           PASS / NO CURRENT POST-UPGRADE ACTION
```

This proves the technical PostgreSQL foundation before DANTE business-database materialization. It does not pre-prove later schema or semantic scenarios.

## 12. Current non-claims

```text
DANTE BUSINESS DATABASE        NOT YET MATERIALIZED
FIRST PRODUCT VERTICAL         NOT IMPLEMENTED
SEMANTIC HG BLANKET PASS       NO
REAL V1→V2 DB EVOLUTION        NOT RUN
RESTORE/PITR REHEARSAL         NOT RUN
POWERSYNC DIRECT TEST          NOT RUN
RESTATE DIRECT TEST            NOT RUN
PRODUCTION DEPLOYMENT          NOT STARTED
```

## 13. Testing / CI

GitHub Actions remains repository-wide CI/CD authority.

Protected `main` requires the accepted backend aggregate gate and dependency review checks. Current PostgreSQL evidence was earned through a real `workflow_dispatch`, not inferred from workflow existence.

The 32 fast + 18 PostgreSQL lanes cover the current 50-test corpus; they are not represented as one single 50-test `pytest` invocation.

## 14. Environments / developer posture

Exactly:

```text
LOCAL → DEV → UAT → PROD
```

Environments are runtime contexts, not Git branches.

Canonical backend semantics remain Linux. Windows development uses the authoritative WSL-backed checkout; divergent Windows/WSL source clones are forbidden.

## 15. Current backend sequence

```text
CP6-00
COMPLETE
        ↓
CP6-01
CLOSED / GATE 01 PASS
        ↓
CP6-02
CLOSED / GATE 02 PASS
        ↓
CP6-03
WHOLE DANTE DATABASE BLUEPRINT
ACTIVE
CHECKPOINT J / DB-U23 CLOSED
FINAL ACTUAL POSTGRESQL OBJECT INVENTORY NEXT
        ↓
GATE 03
NOT YET EARNED
        ↓
CP6-04
WHOLE DANTE DATABASE MATERIALIZATION
        ↓
CP6-05
WHOLE DATABASE DIRECT QA + CP6 CLOSURE
        ↓
POST-CP6
FIRST PRODUCT VERTICAL APPLICATION PHASE
```

Current durable backend execution authority: `docs/workstreams/logical-postgresql.md`.
