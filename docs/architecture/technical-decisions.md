# DANTE Technical Decisions

- Status: **CURRENT DECISION REGISTER**

This file summarizes accepted technical decisions and later direct materialization qualifications. Detailed rationale/evidence remains in the linked Domain/Logical/Physical/Engineering/Frontend Foundation sources, ADRs and workstream handoffs.

A later directly validated implementation qualification overrides older version-specific design wording without automatically reopening the underlying architecture.

## TD-01 — Canonical persistence

**ACCEPTED**

PostgreSQL 18.4 is the sole canonical persistence and material-history authority.

## TD-02 — PostgreSQL capability envelope

**ACCEPTED / PARTLY MATERIALIZED**

Selected: PostGIS 3.6.4, pgvector 0.8.6, native FTS, `pg_trgm`, `unaccent`, `pg_stat_statements`, PgBouncer 1.25.2 target posture.

The LOCAL backend scaffold directly materialized/validated the PostgreSQL 18.4 extension envelope except PgBouncer activation, which remains bounded to a concrete need.

## TD-03 — Offline/sync

**ACCEPTED TARGET / NOT PRODUCT-MATERIALIZED**

PowerSync + encrypted SQLite bounded local state. Local projection/pending state is noncanonical; consequential acceptance remains backend/PostgreSQL-governed and operation-specific.

## TD-04 — Async/durable work

**ACCEPTED**

Class A: PostgreSQL transactional outbox + bounded worker. Class B: Restate selected/dormant until a real durable-workflow requirement.

## TD-05 — Object bytes

**ACCEPTED TARGET / NOT IMPLEMENTED**

Private Cloudflare R2 for ContentArtifact bytes when activated; PostgreSQL remains authority for metadata/provenance/visibility/retention/hash/locator semantics.

## TD-06 — Recovery

**ACCEPTED TARGET / DORMANT**

pgBackRest + WAL/PITR + AWS S3 `eu-south-1` recovery posture. Recovery copies remain noncanonical.

## TD-07 — Solver

**ACCEPTED TARGET / NOT IMPLEMENTED**

OR-Tools CP-SAT. `UNKNOWN != INFEASIBLE`; solver output remains candidate/derived until governed acceptance.

## TD-08 — Observability

**ACCEPTED TARGET**

Backend target: OpenTelemetry + Grafana Alloy + Grafana Cloud EU + pg_stat_statements. Frontend target: Sentry behind bounded adapters when activated.

## TD-09 — Repository strategy and root ownership

**ACCEPTED / MATERIALIZED**

One DANTE monorepo with ownership under:

```text
apps/backend
apps/web
apps/mobile
packages
infra
tooling
tests/system
docs
prototypes
.github
```

Paths exist only for real content. Production never imports prototypes.

## TD-10 — Backend architecture

**ACCEPTED / SCAFFOLD MATERIALIZED**

Capability-first modular monolith; no mechanical 57-owner mapping, universal CRUD repository, BaseService/service locator/global DB session. Domain/application semantics remain independent of FastAPI/SQLAlchemy/provider identity. CP1-CP5 scaffold is directly validated and integrated via PR #24.

## TD-11 — Frontend application architecture

**ACCEPTED / MATERIALIZED AT FOUNDATION SCOPE**

```text
apps/web     React DOM + Vite + TanStack Router
apps/mobile  React Native + Expo + Expo Router
```

Feature-first, thin route/navigation adapters, public-API-only cross-boundary use, acyclic dependencies, app-local UI/platform ownership, no Web<->Mobile private imports, no production->prototypes imports.

Current dependency-cruiser evidence: **36 modules / 45 dependencies / 0 violations**.

## TD-12 — Frontend language/toolchain

**ACCEPTED / DIRECTLY QUALIFIED**

```text
Node          24.19.0
TypeScript    6.0.3 strict
pnpm          11.22.0
Turborepo     2.10.11
```

pnpm isolated layout remains preferred; no hoisting/nodeLinker workaround is authorized without evidence. The integration branch adds `minimumReleaseAge = 1440` minutes.

## TD-13 — Frontend data/state authority

**ACCEPTED**

```text
canonical accepted state/effect   backend + PostgreSQL
synced local projection           PowerSync/SQLite when activated
offline pending mutation          local staging only
offline acceptance                backend governance/conflict checks
remote request state              TanStack Query + typed API when activated
form draft                        TanStack Form when activated
component transient               React
cross-tree transient              Zustand only when justified
```

No universal frontend `Repository<T>`.

## TD-14 — Frontend offline posture

**ACCEPTED / DORMANT UNTIL CONSUMED**

Mobile may activate PowerSync + encrypted SQLite at the first real offline operation. Web is online-first; PowerSync Web and PWA/service-worker behavior remain dormant.

## TD-15 — Frontend API/codegen

**ACCEPTED / NOT MATERIALIZED**

FastAPI OpenAPI -> Orval -> React-free/auth-storage-agnostic `@dante/api-client` only when real product OpenAPI exists. Generated transport must be deterministic/drift-checked where committed.

## TD-16 — Frontend UI/tokens/i18n/time

**ACCEPTED / PARTLY MATERIALIZED**

Materialized shared semantics:

```text
@dante/design-tokens   DTCG/Terrazzo-backed
@dante/i18n            i18next 26.3.6; IT primary/fallback, EN secondary
@dante/time            temporal-polyfill 1.0.4
```

The design-time selection of `@js-temporal/polyfill` is qualified by the later directly validated `temporal-polyfill 1.0.4` implementation. JavaScript `Date` is not the universal DANTE time semantic.

Web/Mobile visual components remain platform-specific; shared token meaning does not imply identical pixels.

## TD-17 — Frontend Web runtime config/delivery

**ACCEPTED TARGET / NOT ACTIVATED**

Immutable SPA promotion with versioned validated public runtime config where the platform permits. Cloudflare delivery remains selected, not active. No second DANTE business backend/BFF is introduced.

## TD-18 — Mobile build/release

**ACCEPTED TARGET / NOT RELEASE-ACTIVATED**

EAS Build/Submit/Update selected. Android direct emulator/runtime evidence exists; signed release/store and iOS direct release validation remain activation-triggered.

## TD-19 — Backend language/runtime

**ACCEPTED / MATERIALIZED**

Python 3.14.x (current scaffold 3.14.7), uv 0.12.5 exact project requirement, Ruff, mypy strict, pytest/Hypothesis, `apps/backend/src/dante`.

## TD-20 — Developer OS/workflow

**ACCEPTED / FRONTEND + BACKEND QUALIFIED**

Linux/WSL is the authoritative source/tooling environment; Windows may host JetBrains/browser/Android emulator. No divergent Windows/WSL source clones or cross-OS `node_modules`.

## TD-21 — LOCAL container/persistence toolkit

**ACCEPTED / MATERIALIZED**

Backend direct in WSL for normal reload/debug; Docker Compose for LOCAL stateful dependencies. SQLAlchemy 2.0 stable + psycopg 3 + Alembic; async DB I/O at technical boundaries and application-owned transactions.

## TD-22 — Migration/copy/recovery governance

**ACCEPTED**

Alembic revision history is schema-change authority; autogenerate is candidate only; revisions immutable after application; expand/migrate/contract and bounded backfills; separated DB privileges; logical copy distinct from recovery; raw PROD -> DEV forbidden by default.

## TD-23 — Environment/config/secrets

**ACCEPTED**

Exactly `LOCAL -> DEV -> UAT -> PROD`. Environment != Git branch. Backend uses typed fail-fast config. Frontend shipped config is public and never secret.

## TD-24 — Testing/CI/supply chain

**ACCEPTED / MATERIALIZED AT CURRENT SCOPE**

GitHub Actions is primary CI/CD.

Backend: calibrated `Backend CI Gate`, real PostgreSQL path, protected-main required checks.

Frontend materialized:

```text
strict TS
architecture checks
generated drift
10 unit tests
Web production build + Chromium E2E
Expo compatibility
Android Hermes bundle smoke
Android emulator runtime evidence
tracked + untracked repository cleanliness
Frontend CI
Frontend CI Gate
```

`Frontend CI Gate` completed real-green, controlled deliberate-red, mandatory failure propagation, exact restore and recovery-green calibration. Its protected-main promotion is **OWNER-CONFIRMED APPLIED / DIRECT API READBACK UNAVAILABLE** because the available connector cannot directly read the repository ruleset.

Dependency Review remains fail-closed at `moderate+`. Three exact transitive tooling advisories are temporarily allowed until review/removal conditions in the active integration handoff are satisfied.

## TD-25 — Current implementation/integration boundary

**CURRENT HANDOFF**

Backend CP1-CP5 scaffold is integrated. Frontend FM-00..FM-07 is closed/pass. PR #28 is READY and remains the active integration boundary until protected-main merge is verified.

```text
CURRENT
exact current PR #28 head
-> hosted CI green
-> current with main
-> mergeable / review-thread clean
-> separate protected-main merge authorization

BACKEND NEXT
Concrete Logical -> PostgreSQL in a fresh bounded workstream
```

The directly observed pre-reconciliation PR head `bdd6e08cbca4c19989502235855d52a620d29fb5` satisfied the current/mergeable/thread-clean and full hosted-CI gates. Any later documentation-only head must independently satisfy them before merge authorization.

## TD-26 — Materialization qualification precedence

**ACCEPTED**

Version-sensitive design selections are qualified by later direct materialization evidence without reopening unrelated architecture.

Current authoritative qualified implementation details:

```text
Temporal implementation    temporal-polyfill 1.0.4
Gesture Handler            2.32.0 under Expo SDK 57
Web E2E directory          apps/web/e2e/
Mobile React               19.2.3 under Expo compatibility
Web React / React DOM      19.2.8 / 19.2.8
```

The known React/react-dom workspace peer diagnostic remains non-blocking because Expo compatibility directly passes for the Mobile baseline. Do not suppress or force version alignment without new evidence.

## TD-27 — Future capability activation

**ACCEPTED OPERATING RULE**

Capabilities that large applications commonly use are not installed ceremonially. Their trigger register lives in `../workstreams/frontend-materialization-integration.md` and covers first product vertical, first UI/design-system surface, first form, first remote API, first offline operation, shared deployment, Mobile release, post-integration security, pre-PROD maturity and scale-triggered infrastructure.

## Selected technologies not to reintroduce casually

Current architecture does not select as defaults: separate canonical graph/vector/search/event-store databases; Redis/Valkey/Kafka/RabbitMQ/NATS/Debezium by default; universal event sourcing; generic workflow stacks; Next.js for the authenticated DANTE Web app; Flutter/React Native Web universal renderer; Nx baseline; Redux as default state authority; generic browser offline/PWA baseline.

Reopen only with materially changed requirements/evidence and explicit scope.
