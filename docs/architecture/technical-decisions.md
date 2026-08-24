> **CURRENT INTEGRATION RECONCILIATION — 2026-08-24**  
> Frontend materialization is now **CLOSED / PASS / INTEGRATED into protected `main` via PR #28**. Later decision text that still says frontend materialization is active is preserved pre-merge wording and is superseded only on status, not on the technical decisions themselves. Backend CP6 remains **CP6-03 ACTIVE** on `feature/logical-postgresql`, current with `main`, with Checkpoint J / DB-U23 CLOSED, Parts 1–8 active, `DB-U08 / DB-U15 / DB-U21` OPEN, exact next block = **FINAL ACTUAL POSTGRESQL OBJECT INVENTORY**, Gate 03 not earned, CP6-04 not authorized.  

# DANTE Technical Decisions

- Status: **CURRENT DECISION REGISTER**

This file summarizes current accepted technical decisions. Detailed rationale and constraints live in linked Domain/Logical/Physical/Engineering/Frontend Foundation sources and ADRs.

## TD-01 — Canonical persistence

**ACCEPTED**

```text
PostgreSQL 18 major family
sole canonical persistence + material-history authority

Physical exact phase-time patch   18.4 / HISTORICAL
CP2 / CP3 original direct patch   18.4 / HISTORICAL EXACT
current repository patch          18.6
18.6 foundation regression        DIRECT REMOTE QA PASS
```

Patch maintenance inside PostgreSQL 18 does not reopen the selected architecture and does not rewrite historical 18.4 evidence.

No separate graph/vector/search/event-store database is canonical by default.

## TD-02 — PostgreSQL capability envelope

**ACCEPTED**

Selected target:

- PostGIS 3.6.4;
- pgvector 0.8.6;
- native FTS;
- pg_trgm;
- unaccent;
- pg_stat_statements;
- PgBouncer 1.25.2.

The current repository-owned PostgreSQL 18.6 image preserves the selected PostGIS/pgvector envelope. PgBouncer activation remains tied to concrete validation.

## TD-03 — Offline/sync

**ACCEPTED TARGET / NOT IMPLEMENTED**

PowerSync + encrypted SQLite bounded local state.

```text
SQLite != canonical truth
PowerSync arrival order != conflict resolution
offline capability = operation-specific
local pending mutation != canonical accepted effect
consequential offline mutation → backend governance/revalidation → PostgreSQL
```

Frontend Data Authority Matrix further qualifies client ownership without changing Physical authority.

## TD-04 — Async/durable work

**ACCEPTED**

Class A: PostgreSQL transactional outbox + bounded worker.

Class B: Restate selected, initially dormant; activate at first real Class-B durable workflow.

## TD-05 — Object bytes

**ACCEPTED TARGET / NOT IMPLEMENTED**

Cloudflare R2 Standard, private, EU jurisdiction, raw bytes only. PostgreSQL owns ContentArtifact authority/metadata/provenance/visibility/retention/hash/locator semantics.

## TD-06 — Recovery

**ACCEPTED TARGET / INITIALLY DORMANT**

```text
pgBackRest 2.59.0
+ AWS S3 Standard eu-south-1
+ Versioning/Object Lock GOVERNANCE posture
+ WAL/PITR
```

Recovery copies remain noncanonical and anti-resurrection obligations remain active.

## TD-07 — Solver

**ACCEPTED TARGET / NOT IMPLEMENTED**

OR-Tools CP-SAT. `UNKNOWN != INFEASIBLE`. Solver output remains candidate/derived until governed acceptance.

## TD-08 — Observability

**ACCEPTED TARGET**

Backend: OpenTelemetry + Grafana Alloy + Grafana Cloud EU + pg_stat_statements.

Frontend: Sentry selected behind bounded Web/Mobile observability adapters when activated.

Operational telemetry is privacy-minimized and noncanonical.

## TD-09 — Repository strategy and root ownership

**ACCEPTED**

One DANTE product monorepo; keep current repository.

Accepted root ownership reserves:

```text
apps/
  backend/
  web/
  mobile/
packages/
infra/
tooling/
tests/system/
docs/
prototypes/
.github/
```

Paths are created only when real content exists. No empty ceremonial tree.

`infra/` owns infrastructure definitions, never business logic. Production apps do not import prototypes.

## TD-10 — Backend architecture

**ACCEPTED**

Capability-first modular monolith.

- no 57 owners → 57 modules mechanical translation;
- no generic CRUD `Repository[T]` semantic model;
- no BaseService/service locator/global DB session;
- Domain/application meaning independent of FastAPI/SQLAlchemy/provider SDK identity;
- explicit composition root;
- private module implementation is not a public interface;
- cross-module ACID transaction allowed when semantics require it.

## TD-11 — Frontend application architecture

**ACCEPTED / FRONTEND FOUNDATION FINAL REVIEW PASS / INTEGRATED VIA PR #22**

Platform boundary:

```text
apps/web     React DOM + Vite + TanStack Router
apps/mobile  React Native + Expo + Expo Router
```

Structural rules:

- feature-first Web/Mobile architecture;
- route/navigation files are thin adapters;
- bootstrap/router consume other layers only through public APIs;
- feature dependency cycles are forbidden;
- Web and Mobile never import each other's private/platform implementation;
- app-local `ui/` and `platform/` boundaries;
- production never imports `prototypes/`;
- architecture rules become executable lint/package/cycle checks during materialization.

Shared-package policy:

- only real multi-consumer packages;
- initial real candidates: `@dante/design-tokens`, `@dante/i18n`, `@dante/time`;
- API client only when real OpenAPI exists;
- shared feature package only after real Web+Mobile reuse;
- framework-free shared cores by default;
- shared frontend logic never owns canonical Domain/AuthZ/conflict/persistence/accepted-effect authority.

## TD-12 — Frontend language/toolchain

**ACCEPTED / INTEGRATED VIA PR #22**

```text
Node 24 LTS
TypeScript 6.0.x strict
pnpm 11
Turborepo 2.x
```

pnpm isolated layout is preferred/direct-validation-required. Evidence-driven `nodeLinker: hoisted` fallback is allowed without reopening the architecture.

Turbo orchestrates the JS/frontend task graph only; GitHub Actions remains repository-wide CI/CD authority.

## TD-13 — Frontend data/state authority

**ACCEPTED / INTEGRATED VIA PR #22**

Data Authority Matrix:

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

Feature UI uses feature data/model boundaries rather than direct HTTP/PowerSync/query-cache/storage ownership. No universal frontend `Repository<T>`.

## TD-14 — Frontend offline posture

**ACCEPTED / INTEGRATED VIA PR #22**

Mobile activates PowerSync + encrypted SQLite when materialized, initially app-owned under the Mobile platform sync boundary.

Web baseline is online-first. PowerSync Web local DB is available/dormant.

Browser PWA/service-worker offline behavior is dormant/not baseline and requires explicit design before activation.

Local mobile data is identity-scoped; cross-account local-data leakage is forbidden.

## TD-15 — Frontend API/codegen

**ACCEPTED / INTEGRATED VIA PR #22**

FastAPI OpenAPI → Orval 8 → React-free/auth-storage-agnostic `@dante/api-client` when real OpenAPI exists.

Generated transport source is deterministic, committed where runtime/reviewability requires it and drift checked. Generated Query ownership is not forced onto PowerSync-backed reads.

## TD-16 — Frontend UI/tokens/i18n/time

**ACCEPTED / INTEGRATED VIA PR #22**

Web UI: DANTE layer over Radix + Tailwind/CSS variables + Motion where required.

Mobile UI: DANTE RN layer over StyleSheet/Reanimated/Gesture Handler.

One DTCG-compatible semantic token source produces platform outputs; shared token meaning does not require identical pixel values.

`@dante/i18n` is framework-free; app bootstrap wires React integration/detection/persistence.

`@dante/time` owns Temporal-based semantic time handling; JavaScript `Date` is not the universal DANTE time type.

## TD-17 — Frontend Web runtime config/delivery

**ACCEPTED / INTEGRATED VIA PR #22**

Web supports one immutable SPA artifact promoted across environments where the platform permits, with versioned Zod-validated public runtime configuration.

Cloudflare Workers Static Assets remains selected Web delivery target. An app-coupled Worker may serve bounded bootstrap config such as `/client-config` but is not a DANTE BFF/business backend.

## TD-18 — Mobile build/release

**ACCEPTED / INTEGRATED VIA PR #22**

EAS Build/Submit/Update selected. EAS Workflows optional/dormant because GitHub Actions remains primary orchestration.

Android and iOS are supported architectural targets; signed/device/store gates apply when each platform is activated for release.

## TD-19 — Backend language/runtime

**ACCEPTED**

```text
Python 3.14.x
initial pin 3.14.7
uv
apps/backend/src/dante
Ruff
mypy strict
pytest
Hypothesis
```

## TD-20 — Developer OS/workflow

**ACCEPTED / FRONTEND QUALIFIED**

Backend canonical semantics: Linux. Primary Windows posture uses one authoritative WSL-backed repository checkout with PyCharm/JetBrains supported.

Frontend keeps the same single-checkout posture. WSL↔Windows Metro/ADB mechanics are a tooling adapter requiring direct validation, not a product architecture invariant.

No divergent Windows/WSL source-tree clones or shared cross-OS node_modules environment.

## TD-21 — LOCAL container/persistence toolkit

**ACCEPTED**

Backend process direct in WSL/Linux for normal reload/debug; Docker Compose owns LOCAL stateful dependencies; future backend deployable uses OCI packaging.

Persistence toolkit:

```text
SQLAlchemy 2.0 stable
psycopg 3
Alembic
```

Async DB I/O at technical boundaries; Domain/application sync/pure by default; application boundary owns transaction.

## TD-22 — Migration/copy/recovery governance

**ACCEPTED / QUALIFIED BY CP6-02 CONSTITUTION**

- Alembic revision history = deployment schema-change authority;
- autogenerate candidate only;
- applied revisions immutable;
- schema drift tested;
- risk review + PostgreSQL staged/online techniques;
- expand → migrate → contract;
- large backfills bounded/resumable/idempotent;
- separated DB privilege classes;
- non-transactional PostgreSQL DDL isolated explicitly when required;
- `pg_dump`/`pg_restore` logical-copy role distinct from pgBackRest/WAL/PITR recovery;
- raw PROD → DEV forbidden by default;
- PostgreSQL major upgrade is a separate platform operation.

Detailed current PostgreSQL persistence/migration doctrine is governed by ADR-010 and the closed CP6-02 Constitution.

## TD-23 — Environment/config/secrets

**ACCEPTED**

Exactly:

```text
LOCAL
DEV
UAT
PROD
```

Environment != Git branch.

Backend uses typed fail-fast pydantic-settings and remote workload identity/secret-manager/OIDC posture.

Frontend tool-specific profiles/channels map to the same four contexts. Client config is public and never contains secrets.

## TD-24 — Testing/CI/supply chain

**ACCEPTED**

GitHub Actions primary CI/CD.

Backend uses risk-layered unit/application/property/architecture/real-PostgreSQL/migration/concurrency/provider/API/privacy/release validation.

Frontend uses co-located unit/component tests, app-level Web E2E/Mobile Maestro, strict type/boundary/cycle checks and higher-cost release validation only where applicable.

Required-check names are never guessed; activate only after real stable emitted contexts are observed.

Protected workflows use least privilege and immutable Action SHA pinning. Supply-chain controls activate with real artifacts/manifests/capabilities; production artifact provenance/SBOM applies at release boundary.

## TD-25 — Cloud/IaC and current next boundary

**PARTLY DEFERRED / CURRENT HANDOFF**

Backend compute provider, IaC engine, registry and remote sizing remain deliberately deferred until first remote infrastructure.

Frontend Foundation is **CLOSED / ACCEPTED / integrated via PR #22**. Frontend materialization is already **ACTIVE** on `feature/frontend-materialization` under its own bounded workstream.

Backend production scaffold CP1–CP5 is **CLOSED / INTEGRATED IN PROTECTED main / DIRECT QA PASS**.

Current backend boundary:

```text
feature/logical-postgresql
CP6 Concrete PostgreSQL Database ACTIVE
CP6-01 CLOSED / GATE 01 PASS
CP6-02 CLOSED / GATE 02 PASS
CP6-03 ACTIVE / WHOLE DANTE DATABASE BLUEPRINT
CHECKPOINT J / DB-U23 CLOSED
FINAL ACTUAL POSTGRESQL OBJECT INVENTORY NEXT
DB-U08 / DB-U15 / DB-U21 OPEN
SECOND FULL TOMBSTONE AUDIT REQUIRED BEFORE GATE 03
GATE 03 NOT YET EARNED
→ CP6-04 WHOLE DANTE DATABASE MATERIALIZATION only after Gate 03 + separate explicit authorization
→ CP6-05 WHOLE DATABASE DIRECT QA + CP6 CLOSURE
→ first product vertical only after CP6
```

## TD-26 — PostgreSQL Persistence Constitution

**ACCEPTED / CROSS-CUTTING**

DANTE accepts the reusable PostgreSQL persistence doctrine closed by CP6-02.

ADR authority:

`docs/decisions/ADR-010-postgresql-persistence-constitution.md`

Detailed normative authority:

`docs/development/backend-cp6-02-postgresql-persistence-constitution.md`

The durable consequences include stable UUID/reference addressing, bounded heterogeneous anchors, material-state/current-history separation, typed relation/constraint doctrine, transaction/concurrency/idempotency rules, migration/evolution posture and owner/migrator/runtime privilege separation. The technical decision register intentionally does not duplicate the full Constitution.

## Selected technologies not to reintroduce casually

Closed Physical/Engineering/Frontend selections exclude or do not select as current defaults, among others: separate graph/vector/search/event-store canonical databases; Redis/Valkey/Kafka/RabbitMQ/NATS/Debezium by default; universal event sourcing; Temporal/DBOS/Celery default workflow stack; Zero/Electric/CRDT canonical authority; Next.js for the authenticated DANTE Web app; Flutter/React Native Web universal renderer; Nx baseline; Redux as default state authority; browser PowerSync TanStack adapter alpha; generic PWA/service-worker offline baseline.

Reopen only with materially changed requirements/evidence and explicit scope.