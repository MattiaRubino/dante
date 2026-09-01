# DANTE System Overview

- **Status:** CURRENT ARCHITECTURE / IMPLEMENTATION-BOUNDARY OVERVIEW
- **Last reconciled:** 2026-09-01
- **Backend foundation:** CP1–CP6 CLOSED / integrated / directly validated
- **Current PostgreSQL:** 18.6
- **Current Alembic head:** `20260830_09`
- **Current product work:** full Access/Auth vertical active and unmerged on `feature/access-auth`; AI architecture active in AI-02.1 v0.3 design/reengineering on `feature/ai-architecture`

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

The AI architecture is currently layered across three branch-local documents:

```text
docs/architecture/dante-ai-foundation.md
→ AI-00 inherited/derived semantic baseline

docs/architecture/ai-production-engineering-state-of-the-art-2026.md
→ external production-engineering research / NON-DANTE-DECISION

docs/architecture/dante-ai-02-1-intelligence-reengineering.md
→ current ACTIVE AI-02.1 v0.3 reengineering checkpoint / NOT CLOSED
```

AI-02.1 does not supersede AI-00. It pressure-tests and refines architecture responsibilities while preserving the accepted semantic baseline.

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

AI-02.1 responsibility boxes are not automatic deployable services and do not alter this accepted modular-monolith posture. Exact future implementation placement remains open.

## 3. Backend technical foundation

```text
CP1 process/config foundation                   CLOSED / DIRECT QA PASS
CP2 LOCAL PostgreSQL foundation                 CLOSED / DIRECT QA PASS
CP3 persistence/migrations/privileges           CLOSED / DIRECT QA PASS
CP4 CI enforcement                              CLOSED / DIRECT REMOTE QA PASS
CP5 integrated scaffold QA                      CLOSED / DIRECT INTEGRATED QA PASS
Backend scaffold integration PR #24             MERGED
CP6 concrete PostgreSQL database                CLOSED / DIRECT QA / INTEGRATED VIA PR #42
PostgreSQL Recovery evolution                   CLOSED / LOCAL DIRECT QA / INTEGRATED VIA PR #47
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

The earlier CP2/CP3 PostgreSQL 18.4 runs and the pre-Recovery `20260826_08` database shape remain exact historical phase-time evidence. Patch maintenance inside PostgreSQL major line 18 and the bounded Recovery lifecycle evolution do not reopen the selected architecture.

## 4. Canonical persistence authority

```text
PostgreSQL 18 major family
SOLE CANONICAL PERSISTENCE / MATERIAL-HISTORY AUTHORITY

current repository/runtime patch
18.6

current Alembic head
20260830_09
```

Current concrete topology:

```text
69 tables
5 ordinary views
15 integrity routines
76 triggers
97 physical indexes
69 foreign keys
123 named CHECK constraints
0 custom enum/domain
0 sequences
0 materialized views
0 RLS policies
```

The current exact Database System of Record is `docs/database/README.md` plus the Database Dictionary and executable Alembic/SQLAlchemy/PostgreSQL truth. The post-CP6 Recovery evolution adds the bounded MaterialState retirement/anti-resurrection contract; it does not create a second canonical persistence surface.

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

AI work inherits the same boundary. Conversation state, embeddings, provider threads, agent/runtime journals, scenario overlays, ChangeSets, BasisManifests, work-lineage metadata or generated summaries do not become canonical DANTE truth by convenience.

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

For consequential operations, expected material state remains the semantic concurrency basis. A stale AI/tool/scenario request must conflict/re-read/re-evaluate/reconcile rather than silently overwrite newer accepted state.

AI-02.1 v0.3 additionally allows dependency-aware invalidation through a runtime/evidence `BasisManifest`; this does not replace owner-specific MaterialState or create a generic canonical version root.

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

The later Recovery evolution is current protected-main truth and is governed by the Database System of Record, current Alembic head `20260830_09`, current Dictionary, operator runbook and recovery harnesses.

## 7. Boundary to product / AI verticals

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

Current bounded branch-local state includes:

```text
Full Access/Auth product vertical
ACTIVE / UNMERGED on feature/access-auth

AI architecture
ACTIVE / AI-02.1 DESIGN + REENGINEERING on feature/ai-architecture
NO BACKEND / DB / PROVIDER IMPLEMENTATION CLAIMED
```

AI-00 remains the semantic baseline. Production-engineering research remains evidence. AI-02.1 is the active architecture pressure-test and has now recorded a v0.3 responsibility map after two pressure-test rounds, but the phase is explicitly **NOT CLOSED** pending the final kill-test and remaining acceptance work.

### AI-02.1 v0.3 responsibility map

The current reengineering checkpoint distinguishes:

```text
Interaction Edge
→ Interaction Session
→ Work Intake
→ Execution Kernel

Execution Kernel may compose:
- Semantic Query / Projection Gateway
- Context Engine
- Simulation / Hypothetical State Workspace
- BasisManifest / dependency validity
- model reasoning through ModelTarget + HarnessProfile
- deterministic compute
- solver
- capability runtime
- verifier / auditor
- ChangeSet / EffectGraph
- governed Effect Runtime

Cross-cutting:
- policy / Authority / AuthZ / Consent / Visibility
- information flow
- provider eligibility
- autonomy
- proactivity / attention + attention budgeting
- causal lineage / oscillation guard
- work lineage / supersession / run durability
- artifacts
- result / disclosure / cumulative inference protection
- control plane
- resource governance
- observability
- audit / execution evidence
- evals
```

These are responsibility boundaries, not new Domain owners and not one-service-per-box deployment instructions.

### Interaction / Run / supersession distinction

```text
Interaction Session != Run != Worker
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
```

A conversation may contain multiple Runs. A durable Run may outlive the UI Session when its own work contract legitimately requires that behavior. A newer scoped intention may supersede pending work in an older Run without fabricating rollback of already-performed effects or cancelling unrelated independent work.

### DANTE-native / open-world composition

The same intelligence surface may combine:

```text
DANTE-native structured state / planning / effects
+
open-world explanation / research / documents / code / multimodal reasoning
```

without transferring canonical state or Authority to the model/provider.

### Scenario, basis and compound-change distinction

Hypothetical scenarios are derived/transient overlays over a material-state/source basis, not current truth. `BasisManifest` is runtime/evidence metadata for validity and dependency-aware recomputation. A selected scenario may lead to a governed ChangeSet, but the ChangeSet does not replace individual effect governance or cross-system reconciliation.

### Context vs disclosure

The architecture distinguishes:

```text
Context Projection
= what a reasoning operation may consume for a purpose

Disclosure Projection
= what representation a recipient may receive
```

Round II additionally requires bounded protection against cumulative/cross-query inference where individually safe responses could compose into protected information. This preserves privacy/Visibility semantics without creating a second semantic truth.

### Revocable Run validity

Authorization, Consent, Visibility and source/data eligibility may need revalidation at consequential boundaries. Permission at Run start is not perpetual permission to retrieve, disclose, persist derived material or execute future effects after relevant revocation/change.

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

The future AI interaction surface must preserve the same authority boundary: chat/UI state may express draft, candidate, streaming, hypothetical, superseded or pending state without pretending that state is an accepted canonical effect.

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

For AI, Restate/outbox/pgvector/OR-Tools/provider capabilities remain trigger-based: selection in the target architecture does not mean every AI request should activate them.

Research challengers remain challengers until a real DANTE workload creates evidence to reopen the smallest relevant choice.

## 10. Transactions / migrations / privileges

Current durable posture:

```text
one AsyncEngine per process
one async_sessionmaker per process
one AsyncSession per app operation
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

Future AI tool execution must pass through application/domain mutation contracts rather than receiving direct unrestricted database mutation authority.

A compound AI-generated ChangeSet may coordinate multiple application effects, but does not expand their transaction/authority boundaries. Cross-provider all-or-nothing semantics must not be fabricated where they do not exist.

Cancelling/superseding a Run does not itself undo an effect already dispatched outside DANTE; such effects remain subject to truthful verification/reconciliation/compensation semantics.

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

The later integrated Recovery workstream directly proved the bounded recovery/retirement/anti-resurrection contract in LOCAL, including whole CP07 rehearsal and database-local reopen. Remote backup/cloud recovery remains unactivated/not claimed. Exact current evidence belongs to `docs/database/README.md` and the recovery runbook/harnesses.

Current AI-00 / research / AI-02.1 work is documentation/design only and makes no runtime QA claim.

## 12. Current non-claims

```text
FULL ACCESS/AUTH PRODUCT VERTICAL       NOT CLAIMED CLOSED
DANTE AI-02.1                           ACTIVE / v0.3 / NOT CLOSED
DANTE AI RUNTIME                        NOT IMPLEMENTED
AI MODEL / PROVIDER                     NOT SELECTED
AI AGENT SDK / ORCHESTRATOR             NOT SELECTED
AI CONVERSATION / MEMORY DB SCHEMA      NOT DESIGNED OR MATERIALIZED
AI-02.1 RESPONSIBILITY BOUNDARIES        NOT IMPLEMENTED AS SERVICES/MODULES BY THIS DOC
AI-03 CONTEXT / RETRIEVAL / MEMORY      NOT STARTED
SEMANTIC HG BLANKET PASS                NO
REMOTE BACKUP PROVIDER                  TBD / NOT ACTIVATED
PRODUCTION/CLOUD RECOVERY               NOT CLAIMED
POWERSYNC PRODUCT DIRECT TEST           ONLY WHEN ACTIVATED BY A REAL VERTICAL
RESTATE DIRECT TEST                     ONLY WHEN ACTIVATED BY A REAL WORKFLOW
PRODUCTION DEPLOYMENT                   NOT IMPLIED BY LOCAL/CI DATABASE CLOSURE
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

Future AI implementation will require its own direct evidence for model/tool/runtime/security behavior; documentation or provider feature claims will not constitute PASS.

Before AI-02.1 can close at architecture level, its current v0.3 responsibility model must survive the final kill-test combining cumulative disclosure inference, work supersession, causal loops, revocation, dependency-local staleness, partial external effects, crash/recovery and attention pressure rather than only isolated happy paths.

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
POSTGRESQL RECOVERY   LOCAL PASS / CLOSED / INTEGRATED
FRONTEND FOUNDATION   CLOSED / INTEGRATED
ACCESS/AUTH VERTICAL  ACTIVE / UNMERGED
AI ARCHITECTURE       ACTIVE / AI-02.1 REENGINEERING / UNMERGED
AI-02.1               v0.3 / ROUND I + II COMPLETE / FINAL KILL-TEST REQUIRED / NOT CLOSED
AI-03                 NOT STARTED / BLOCKED UNTIL AI-02.1 ACCEPTANCE
```

Current general repository status is owned by `docs/PROJECT-STATUS.md`; branch-local product/architecture work is owned by the relevant durable documentation and executable branch truth.
