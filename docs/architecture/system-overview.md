# DANTE System Overview

- **Status:** CURRENT ARCHITECTURE / IMPLEMENTATION-BOUNDARY OVERVIEW
- **Last reconciled:** 2026-08-26
- **Backend foundation:** CP1–CP6 CLOSED / integrated / directly validated
- **Current PostgreSQL:** 18.6
- **Current Alembic head:** `20260826_08`
- **Current product work:** Access frontend active and unmerged on `feature/access-frontend`

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

Logical hardenings `WL-H01..WL-H12` remain active implementation contracts.

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
CP2 LOCAL PostgreSQL foundation                 CLOSED / DIRECT QA PASS
CP3 persistence/migrations/privileges           CLOSED / DIRECT QA PASS
CP4 CI enforcement                              CLOSED / DIRECT REMOTE QA PASS
CP5 integrated scaffold QA                      CLOSED / DIRECT INTEGRATED QA PASS
Backend scaffold integration PR #24             MERGED
CP6 concrete PostgreSQL database                CLOSED / DIRECT QA / INTEGRATED VIA PR #42
```

Current technical baseline:

```text
Python 3.14.x
uv
FastAPI
SQLAlchemy async
psycopg 3
Alembic
PostgreSQL 18.6
schema dante
owner / migrator / runtime role separation
explicit application transaction ownership
real PostgreSQL acceptance testing
```

The earlier CP2/CP3 PostgreSQL 18.4 runs remain exact historical phase-time evidence. Patch maintenance inside PostgreSQL major line 18 does not reopen the architecture.

## 4. Canonical persistence authority

```text
PostgreSQL 18 major family
SOLE CANONICAL PERSISTENCE / MATERIAL-HISTORY AUTHORITY

current repository/runtime patch
18.6

current Alembic head
20260826_08
```

Current concrete topology:

```text
68 tables
5 ordinary views
14 integrity routines
75 triggers
95 physical indexes
68 foreign keys
120 named CHECK constraints
0 custom enum/domain
0 sequences
0 materialized views
0 RLS policies
```

Selected PostgreSQL capability envelope remains bounded by the accepted Physical/technical decisions, including PostGIS, pgvector, native FTS, `pg_trgm`, `unaccent`, `pg_stat_statements` and a trigger-based PgBouncer activation posture.

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

Current PostgreSQL rules preserve:

```text
homogeneous NativeRef
→ direct FK

genuinely heterogeneous NativeRef
→ bounded native-address anchor

MaterialStateRef
→ stable PostgreSQL UUID address
→ bounded material-state address/control
→ exact owner + facet
→ owner-specific material-state row
→ explicit current accepted-state binding where required
```

Provider revisions, MVCC tokens, timestamps and ETags do not become MaterialStateRef.

## 6. CP6 — Concrete PostgreSQL Database

CP6 is complete. It converted the closed Domain + Logical + Physical model into the concrete DANTE PostgreSQL database and then validated the result directly.

Closure state:

```text
CP6-00 COMPLETE
CP6-01 CLOSED / GATE 01 PASS
CP6-02 CLOSED / GATE 02 PASS
CP6-03 CLOSED / GATE 03 PASS
CP6-04 CLOSED / MATERIALIZATION PASS
CP6-05 CLOSED / DIRECT QA PASS
CP6 CLOSED / CONCRETE POSTGRESQL DATABASE PASS
```

Durable acceptance evidence:

- `docs/development/backend-cp6-05-whole-database-qa.md`
- `docs/database/README.md`
- `docs/database/dictionary/README.md`
- `docs/decisions/ADR-010-postgresql-persistence-constitution.md`

The former CP6 blueprint/materialization sequence is historical execution evidence. It is not a current next-step plan.

## 7. Boundary to product verticals

Database materialization is not the same thing as product-vertical application implementation.

Post-CP6 product verticals own, where applicable:

```text
application use cases
application services
business persistence adapters encoding application behavior
business API routes
frontend behavior
product workflow orchestration
```

They consume the already-materialized canonical database. A later real requirement may evolve the DB normally, but accepted schema/semantic invariants are not casually reopened.

Current state:

```text
Access frontend
ACTIVE / UNMERGED on feature/access-frontend

first dedicated post-CP6 backend product vertical
NOT STARTED
```

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

Generic frontend foundation/materialization is already closed and integrated. Product verticals proceed on bounded branches under their own gates.

## 9. Offline / specialist capabilities

Selected Physical targets remain activation-triggered rather than automatically enabled everywhere.

```text
PowerSync + encrypted SQLite      offline/sync consumer required
PgBouncer                         real connection-pressure value
PostgreSQL outbox                 real Class-A async requirement
Restate                           real Class-B durable workflow
Cloudflare R2                     real ContentArtifact byte flow
pgBackRest + S3                   recovery/production boundary or rehearsal
OR-Tools                          solver-backed capability
```

A PostgreSQL-native structure required by the canonical schema may exist without activating the surrounding runtime/product capability.

## 10. Transactions / migrations / privileges

Current durable posture:

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

Migration/evolution, idempotency, material-state and privilege doctrine is governed by the accepted PostgreSQL Constitution and the real Alembic/mapping implementation.

## 11. Current direct database evidence

Final CP6 acceptance established, among other gates:

```text
uv lock/sync                     PASS
Ruff format/check                PASS
mypy                             PASS
non-PostgreSQL backend tests     PASS
backend build                    PASS
real PostgreSQL selected tests   PASS
schema/topology checks           PASS
security/ACL checks              PASS
Database Dictionary checks       PASS
restart/health                   PASS
persistent volume retained       PASS
```

The accepted implementation/database evidence is the CP6 closure package, not older pre-materialization foundation runs.

## 12. Current non-claims

```text
FIRST POST-CP6 BACKEND PRODUCT VERTICAL   NOT IMPLEMENTED
SEMANTIC HG BLANKET PASS                  NO
RESTORE/PITR PRODUCTION REHEARSAL         NOT CLAIMED BY CP6
POWERSYNC PRODUCT DIRECT TEST             ONLY WHEN ACTIVATED BY A REAL VERTICAL
RESTATE DIRECT TEST                       ONLY WHEN ACTIVATED BY A REAL WORKFLOW
PRODUCTION DEPLOYMENT                     NOT IMPLIED BY LOCAL/CI DATABASE CLOSURE
```

## 13. Testing / CI

GitHub Actions remains repository-wide CI/CD authority.

Protected `main` currently requires:

```text
Backend CI Gate
Dependency Review
Frontend CI Gate
```

Required-check names come from real emitted contexts and repository rules, not guessed prose.

Historical successful runs remain evidence for the exact commit/environment on which they executed. Current claims require current evidence appropriate to the affected scope.

## 14. Environments / developer posture

Exactly:

```text
LOCAL → DEV → UAT → PROD
```

Environments are runtime contexts, not Git branches.

Canonical backend semantics remain Linux. Windows development uses the authoritative WSL-backed checkout; divergent Windows/WSL source clones are forbidden.

## 15. Current execution posture

```text
DOMAIN MODEL          CLOSED
LOGICAL MODEL         CLOSED
PHYSICAL MODEL        CLOSED
BACKEND FOUNDATION    CLOSED
CP6 DATABASE          CLOSED / INTEGRATED
FRONTEND FOUNDATION   CLOSED / INTEGRATED
ACCESS FRONTEND       ACTIVE / UNMERGED
```

Current general repository status is owned by `docs/PROJECT-STATUS.md`; branch-local product work is owned by the relevant workstream documentation and executable branch truth.
