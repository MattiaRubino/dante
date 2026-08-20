# DANTE Technical Decisions

- Status: **CURRENT DECISION REGISTER**

This file summarizes current accepted technical decisions. Detailed rationale and constraints live in linked Domain/Logical/Physical/Engineering/Frontend Foundation sources and ADRs.

## TD-01 — Canonical persistence

**ACCEPTED**

```text
PostgreSQL 18.4
sole canonical persistence + material-history authority
```

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

Full selected extension envelope is installed/enabled from the first LOCAL PostgreSQL baseline when materialized. PgBouncer activation remains tied to concrete validation.

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

**ACCEPTED IN ACTIVE FRONTEND WORKSTREAM / PENDING MAIN INTEGRATION**

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

**ACCEPTED IN ACTIVE FRONTEND WORKSTREAM / PENDING MAIN INTEGRATION**

```text
Node 24 LTS
TypeScript 6.0.x strict
pnpm 11
Turborepo 2.x
```

pnpm isolated layout is preferred/direct-validation-required. Evidence-driven `nodeLinker: hoisted` fallback is allowed without reopening the architecture.

Turbo orchestrates the JS/frontend task graph only; GitHub Actions remains repository-wide CI/CD authority.

## TD-13 — Frontend data/state authority

**ACCEPTED IN ACTIVE FRONTEND WORKSTREAM / PENDING MAIN INTEGRATION**

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

**ACCEPTED IN ACTIVE FRONTEND WORKSTREAM / PENDING MAIN INTEGRATION**

Mobile activates PowerSync + encrypted SQLite when materialized, initially app-owned under the Mobile platform sync boundary.

Web baseline is online-first. PowerSync Web local DB is available/dormant.

Browser PWA/service-worker offline behavior is dormant/not baseline and requires explicit design before activation.

Local mobile data is identity-scoped; cross-account local-data leakage is forbidden.

## TD-15 — Frontend API/codegen

**ACCEPTED IN ACTIVE FRONTEND WORKSTREAM / PENDING MAIN INTEGRATION**

FastAPI OpenAPI → Orval 8 → React-free/auth-storage-agnostic `@dante/api-client` when real OpenAPI exists.

Generated transport source is deterministic, committed where runtime/reviewability requires it and drift checked. Generated Query ownership is not forced onto PowerSync-backed reads.

## TD-16 — Frontend UI/tokens/i18n/time

**ACCEPTED IN ACTIVE FRONTEND WORKSTREAM / PENDING MAIN INTEGRATION**

Web UI: DANTE layer over Radix + Tailwind/CSS variables + Motion where required.

Mobile UI: DANTE RN layer over StyleSheet/Reanimated/Gesture Handler.

One DTCG-compatible semantic token source produces platform outputs; shared token meaning does not require identical pixel values.

`@dante/i18n` is framework-free; app bootstrap wires React integration/detection/persistence.

`@dante/time` owns Temporal-based semantic time handling; JavaScript `Date` is not the universal DANTE time type.

## TD-17 — Frontend Web runtime config/delivery

**ACCEPTED IN ACTIVE FRONTEND WORKSTREAM / PENDING MAIN INTEGRATION**

Web supports one immutable SPA artifact promoted across environments where the platform permits, with versioned Zod-validated public runtime configuration.

Cloudflare Workers Static Assets remains selected Web delivery target. An app-coupled Worker may serve bounded bootstrap config such as `/client-config` but is not a DANTE BFF/business backend.

## TD-18 — Mobile build/release

**ACCEPTED IN ACTIVE FRONTEND WORKSTREAM / PENDING MAIN INTEGRATION**

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

**ACCEPTED**

- Alembic revision history = deployment schema-change authority;
- autogenerate candidate only;
- applied revisions immutable;
- schema drift tested;
- risk review + PostgreSQL staged/online techniques;
- expand → migrate → contract;
- large backfills bounded/resumable/idempotent;
- separated DB privilege classes;
- `pg_dump`/`pg_restore` logical-copy role distinct from pgBackRest/WAL/PITR recovery;
- raw PROD → DEV forbidden by default;
- PostgreSQL major upgrade is a separate platform operation.

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

Current frontend sequence on `feature/frontend-foundation`:

```text
finish Passo 3 clean review
→ if blockers == 0 record Frontend Foundation design/architecture closure
→ prepare protected-main integration
→ after integration open new production frontend materialization scope
→ run direct validations progressively
```

Backend production scaffold remains a separate **NOT STARTED** workstream and is not silently authorized by Frontend Foundation.

## Selected technologies not to reintroduce casually

Closed Physical/Engineering/Frontend selections exclude or do not select as current defaults, among others: separate graph/vector/search/event-store canonical databases; Redis/Valkey/Kafka/RabbitMQ/NATS/Debezium by default; universal event sourcing; Temporal/DBOS/Celery default workflow stack; Zero/Electric/CRDT canonical authority; Next.js for the authenticated DANTE Web app; Flutter/React Native Web universal renderer; Nx baseline; Redux as default state authority; browser PowerSync TanStack adapter alpha; generic PWA/service-worker offline baseline.

Reopen only with materially changed requirements/evidence and explicit scope.
