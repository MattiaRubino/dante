# DANTE System Overview

- Status: **CURRENT ARCHITECTURE / IMPLEMENTATION-BOUNDARY OVERVIEW**
- Current backend progression: **CP1–CP5 CLOSED / INTEGRATED / DIRECT QA PASS; CP6 Concrete Persistence Readiness ACTIVE; CP6-01 CLOSED / GATE 01 PASS; CP6-02 ACTIVE / CANDIDATE / PRE-CLOSURE / GATE 02 NOT PASSED**
- Current CP6 branch: `feature/logical-postgresql`
- Current PostgreSQL technical patch: **18.6 / DIRECT REMOTE FOUNDATION REGRESSION PASS**

## 1. Product and authority

DANTE is a personal operating system whose canonical truth represents real life over time while preserving authority, provenance, uncertainty and distinctions between intention, execution and outcome.

Compass: **Understand life. Shape what comes next.**

Implementation consumes closed Product/Domain/Logical/Physical models, closed Engineering Foundation and closed Frontend Engineering Foundation. Current implementation work must consume those authorities rather than reinterpret them for framework or storage convenience.

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

## 2. Repository/application topology

One product monorepo with accepted ownership:

```text
DANTE repository
│
├── apps/backend
│   └── capability-first modular monolith
│
├── apps/web
│   └── React DOM/Vite client; feature-first
│
├── apps/mobile
│   └── Expo/React Native client; feature-first
│
├── packages
│   └── only genuine multi-consumer contracts/artifacts
│
├── infra
│   └── LOCAL/future remote infrastructure definitions
│
├── tooling
├── tests/system
├── docs
├── prototypes
└── .github
```

Paths are materialized only when real content exists. Production implementation continues in the existing repository; a new production repo is not planned.

## 3. Backend architecture and current foundation

Accepted internal shape:

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

Current backend foundation truth:

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

CP3 already materializes SQLAlchemy async, psycopg 3, Alembic, schema `dante`, role separation, explicit transaction ownership and real PostgreSQL acceptance. It deliberately contains no business persistence mapping.

The CP6 PostgreSQL 18.6 refresh does not change that architecture. It reuses and directly re-proves the existing foundation on the current maintenance patch.

## 4. Frontend architecture

Web and Mobile are sibling governed clients with platform-specific renderers and selective shared semantics.

Web conceptual internals:

```text
bootstrap
routes
features
ui
platform
config
```

Mobile conceptual internals:

```text
app/          Expo Router adapters
src/bootstrap
src/features
src/ui
src/platform
src/config
```

Structural rules:

- feature-first;
- routes/navigation are thin adapters;
- public-API-only cross-boundary imports;
- feature dependency cycles forbidden;
- Web/Mobile do not import each other's private implementation;
- UI/platform layers do not depend upward on feature internals;
- no generic shared/common/utils dumping grounds;
- production never imports prototypes;
- architecture rules become executable checks when materialized.

Shared packages are extracted only for real multi-consumer semantics. Shared client cores remain framework-free by default and never own backend/domain authority.

Frontend production materialization proceeds under its own bounded workstream and may run in parallel with backend CP6. Its direct-validation status is governed by the frontend workstream/current project status, not by historical scaffold wording in this overview.

## 5. Canonical persistence and client data authority

```text
PostgreSQL 18 major family
SOLE CANONICAL PERSISTENCE / MATERIAL-HISTORY AUTHORITY

Physical phase-time exact patch   18.4
CP2/CP3 original direct evidence  18.4 / historical exact
current technical patch           18.6
18.6 technical regression         DIRECT REMOTE QA PASS
```

Selected DB capabilities remain PostGIS 3.6.4, pgvector 0.8.6, native FTS, pg_trgm, unaccent, pg_stat_statements and bounded PgBouncer posture.

Frontend Data Authority Matrix:

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

An offline operation crosses staging → upload → backend accept/reject → reconciliation. Local arrival/staging does not define semantic truth.

## 6. Concrete persistence boundary — CP6

The active backend boundary is **CP6 — Concrete Persistence Readiness**.

```text
CP6-00
COMPLETE

CP6-01
CLOSED / GATE 01 PASS

CP6-02
POSTGRESQL PERSISTENCE CONSTITUTION
ACTIVE / CANDIDATE / PRE-CLOSURE
GATE 02 NOT PASSED
```

CP6-01 closure authority:

`docs/development/backend-cp6-01-concrete-persistence-coverage-closure.md`

CP6-02 candidate authority:

`docs/development/backend-cp6-02-postgresql-persistence-constitution.md`

The CP6-02 technology-refresh boundary is now directly proved:

```text
PostgreSQL 18.6 image build         PASS
PostGIS 3.6.4                       PASS
pgvector 0.8.6                      PASS
Backend Quality                     SUCCESS / 32 fast tests PASS
Backend PostgreSQL                  SUCCESS / 18 PostgreSQL tests PASS
Backend CI Gate                     SUCCESS
run                                 32568664940
HEAD                                ec3dc795b5e044daa3a77723c94a1b4b5b92865c
release-note impact                 PASS / NO CURRENT POST-UPGRADE ACTION
```

What remains before Gate 02:

```text
final independent whole-Constitution review
separate formal Gate 02 closure write
```

CP6 does not repeat Domain, Logical or Physical modeling. It consumes those closed authorities and must finish with:

```text
CONCRETE POSTGRESQL FOUNDATION
CLOSED / READY

VERTICAL #1
SELECTED
EXACTLY DESIGNED
READY FOR IMPLEMENTATION
```

CP6 does **not** implement Vertical #1.

Not authorized inside CP6:

```text
Vertical #1 business Alembic migrations
Vertical #1 SQLAlchemy business mappings
Vertical #1 persistence adapter
application use case
business API
speculative shared table/primitive created only to obtain direct proof
```

The first business implementation begins only in the separately authorized post-CP6 vertical phase.

## 7. Offline/sync

Selected Physical target remains PowerSync + encrypted SQLite bounded local state.

Mobile activates that path when a real offline/sync implementation requires it. Web remains online-first unless a separately accepted need activates a broader local/sync path.

Local client databases are identity scoped; cross-account local-data leakage is forbidden.

PowerSync/logical replication is not active in the current backend. When it is activated, PostgreSQL maintenance review must include then-current logical-decoding policy, including `output_plugin_libraries` introduced in PostgreSQL 18.6.

## 8. UI/shared semantics

Web owns a DANTE UI layer over selected Web primitives/styling. Mobile owns a separate DANTE Native UI layer. Shared semantic design tokens may intentionally render differently per platform.

`@dante/i18n` is framework-free; app bootstrap wires React integration/platform detection/persistence.

`@dante/time` owns Temporal-based semantic time handling.

## 9. Configuration/secrets

Backend uses typed pydantic-settings fail-fast configuration.

Frontend public config is typed/validated and contains no secrets.

Web runtime config is versioned and validated so one SPA artifact can be promoted across environments where the delivery platform permits. An app-coupled Cloudflare Worker may serve bounded bootstrap config but is not a DANTE BFF/business backend.

Remote secret posture remains workload identity → provider secret manager → least privilege → rotation/revocation/audit, with GitHub OIDC preferred where supported.

## 10. Environments

Exactly:

```text
LOCAL → DEV → UAT → PROD
```

They are runtime contexts, not Git branches.

## 11. Async/durable/object/recovery/solver

Class A async target: PostgreSQL transactional outbox + bounded worker, materialized only on real Class-A need.

Class B: Restate selected/dormant until a real Class-B workflow.

ContentArtifact raw bytes: private Cloudflare R2 when activated; PostgreSQL owns authority/metadata.

Recovery: pgBackRest + WAL/PITR + AWS S3 accepted target at recovery boundary.

Solver: OR-Tools CP-SAT; `UNKNOWN != INFEASIBLE`; solver output remains candidate until governed acceptance.

## 12. Observability

Backend target: OpenTelemetry + Grafana Alloy + Grafana Cloud EU + pg_stat_statements.

Frontend: Sentry behind bounded app/platform observability adapters when activated.

All observability is privacy-minimized operational telemetry, never canonical history or a shadow personal-data store.

## 13. Testing/CI/release

GitHub Actions is repository-wide primary CI/CD authority.

Backend validation is risk-layered and includes a real PostgreSQL lane. Protected `main` requires the accepted backend aggregate gate and dependency review checks.

Current PostgreSQL 18.6 evidence was earned through a real `workflow_dispatch` run, not inferred from workflow existence:

```text
run                  32568664940
Backend Quality      SUCCESS
Backend PostgreSQL   SUCCESS
Backend CI Gate      SUCCESS
```

The fast and PostgreSQL lanes cover the current 50-test corpus as 32 + 18 tests. This must not be misreported as a single full-`pytest` invocation.

Frontend validation progressively covers lint/dependency/cycle boundaries, strict TS, unit/component, generated drift, Web E2E, Mobile tests and release/device validation for activated targets.

Architecture/design closure remains distinct from direct implementation validation.

## 14. Developer posture

Canonical backend semantics remain Linux. Primary Windows posture is one authoritative WSL-backed repository checkout with JetBrains/PyCharm UI on Windows as desired.

Frontend keeps one authoritative checkout; WSL↔Windows Metro/ADB specifics are a direct-validation tooling adapter. Divergent Windows/WSL source clones are forbidden.

## 15. Current direct-evidence boundary

```text
BACKEND SCAFFOLD CP1–CP5       CLOSED / DIRECT QA PASS / INTEGRATED
POSTGRESQL 18.4                HISTORICAL PHYSICAL/CP2/CP3 EXACT EVIDENCE
POSTGRESQL 18.6                CURRENT TECHNICAL PATCH
18.6 FOUNDATION REGRESSION     DIRECT REMOTE QA PASS
CP3 TECHNICAL PERSISTENCE      DIRECT QA PASS
DANTE SCHEMA / ALEMBIC BASE    MATERIALIZED / DIRECT QA PASS
CP6-01 COVERAGE GATE           CLOSED / GATE 01 PASS
CP6-02 CONSTITUTION            ACTIVE / CANDIDATE / GATE 02 NOT PASSED
CONCRETE BUSINESS DB SCHEMA    NOT IMPLEMENTED
VERTICAL #1                    NOT IMPLEMENTED
SEMANTIC HG DIRECT PASS        0 unless an actual qualifying business scenario executes
PSV                            only per exact executed selected-stack artifact
RESTORE/PITR REHEARSAL         NOT RUN
```

The old Physical phase statement `DATABASE DEPLOYMENT NOT STARTED` is historical phase-time evidence and is superseded for current technical implementation status by CP2/CP3 and the later 18.6 regression. Technical QA does not convert business-semantic HG/PSV into PASS.

## 16. Current backend sequence

```text
CP6-00 authority reconstruction
COMPLETE
        ↓
CP6-01 concrete persistence coverage
CLOSED / GATE 01 PASS
        ↓
CP6-02 PostgreSQL Persistence Constitution
ACTIVE / CANDIDATE / PRE-CLOSURE
18.6 TECHNICAL REGRESSION PASS
FINAL INDEPENDENT REVIEW NEXT
GATE 02 NOT PASSED
        ↓
CP6-03 Concrete Relational Topology
       + Implementation Dependency DAG
       + Vertical Decomposition
       STARTS ONLY AFTER GATE 02 PASS
        ↓
CP6-04 Vertical #1 selection
        ↓
CP6-05 Vertical #1 exact persistence design
        ↓
CP6-06 PostgreSQL foundation direct readiness proof
       only where non-speculative and genuinely executable
        ↓
CP6-07 whole persistence readiness / clean-room QA
        ↓
CP6 CLOSED
        ↓
SEPARATE POST-CP6 PHASE
Vertical #1 implementation
```

Current durable backend authority: `docs/workstreams/logical-postgresql.md`.
