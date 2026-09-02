# DANTE Technical Decisions

- **Status:** CURRENT DECISION REGISTER
- **Last reconciled:** 2026-09-02

This file summarizes current accepted technical decisions. Detailed rationale and constraints live in linked Domain/Logical/Physical/Engineering/Frontend Foundation sources and ADRs. Historical phase-time status does not override later closure/integration evidence.

Branch-local AI architecture is tracked here only as **current unmerged design context**, not promoted into an accepted implementation technology decision by this register. AI-02.1 v0.5 and AI-03 Context/Retrieval/Memory are structurally accepted responsibility contracts; AI-04 Productionization Architecture is current while concrete provider/model/runtime/retrieval/persistence activation choices remain evidence-driven and open unless explicitly selected below.

## TD-01 — Canonical persistence

**ACCEPTED**

```text
PostgreSQL 18 major family
sole canonical persistence + material-history authority

Physical exact phase-time patch         18.4 / HISTORICAL
CP2 / CP3 original direct patch         18.4 / HISTORICAL EXACT
current repository patch                18.6
historical pre-Recovery Alembic head    20260826_08
current protected-main Alembic head     20260830_09
```

Current protected-main topology:

```text
69 tables
5 views
15 routines
76 triggers
97 physical indexes
69 foreign keys
123 CHECK constraints
```

Patch maintenance inside PostgreSQL 18 does not reopen selected architecture and does not rewrite historical 18.4 evidence.

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
- PgBouncer 1.25.2 target posture.

Current repository-owned PostgreSQL 18.6 image preserves the selected PostGIS/pgvector envelope. PgBouncer activation remains tied to concrete validation/need.

The existence of native FTS / `pg_trgm` / `pgvector` capability does **not** constitute AI retrieval activation, index design or a production provider/runtime choice. AI-03C closed an exact-before-ANN, consumer-triggered materialization posture; actual FTS/vector/index activation remains direct-evidence work under later production/implementation gates.

## TD-03 — Offline/sync

**ACCEPTED TARGET / OPERATION-SPECIFIC ACTIVATION**

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

Durability is workload/semantics-driven, not a synonym for long elapsed time.

AI-03C further distinguishes durable technical coordination/binding state from Class-B durable execution and from canonical Domain truth. One-shot invalidation delivery cannot be the only convergence mechanism for activated derived systems.

## TD-05 — Object bytes

**ACCEPTED TARGET / TRIGGER-BASED ACTIVATION**

Cloudflare R2 Standard, private, EU jurisdiction, raw bytes only. PostgreSQL owns ContentArtifact authority/metadata/provenance/visibility/retention/hash/locator semantics.

## TD-06 — Recovery

**ACCEPTED PHYSICAL TARGET / CURRENT LOCAL IMPLEMENTATION QUALIFIED**

Historical Physical recovery target selected:

```text
pgBackRest 2.59.0
+ AWS S3 Standard eu-south-1
+ Versioning/Object Lock GOVERNANCE posture
+ WAL/PITR
```

Current implementation truth after Recovery integration:

```text
pgBackRest LOCAL recovery   IMPLEMENTED / DIRECTLY REHEARSED / INTEGRATED VIA PR #47
CP01–CP07                   LOCAL PASS / CLOSED
remote backup provider      TBD / NOT ACTIVATED
production/cloud recovery   NOT CLAIMED
```

The historical S3 target remains valid phase-time Physical selection evidence. It is **not** a statement that a remote production provider is currently activated.

Recovery copies remain noncanonical and anti-resurrection obligations remain active.

AI-03 inherits and hardens this rule: durable embeddings/summaries/indexes/caches/provider-state derivatives cannot regain semantic eligibility merely because old bytes reappear after restore. Recomputable derived state is non-serving until rebuilt or explicitly reconciled against current authority; runtime/provider/derived recovery cannot outrun canonical PostgreSQL recovery/reconciliation readiness.

## TD-07 — Solver

**ACCEPTED TARGET / TRIGGER-BASED ACTIVATION**

OR-Tools CP-SAT.

```text
UNKNOWN != INFEASIBLE
solver output != accepted canonical effect
```

Activate for real solver-backed capabilities rather than ordinary deterministic work that does not need it.

## TD-08 — Observability

**ACCEPTED TARGET**

Backend: OpenTelemetry + Grafana Alloy + Grafana Cloud EU + pg_stat_statements.

Frontend: Sentry selected behind bounded Web/Mobile observability adapters when activated.

Operational telemetry is privacy-minimized and noncanonical.

```text
TELEMETRY != AUDIT
```

AI traces/prompts/ContextManifests/tool results are not automatically safe to export merely because an observability backend exists; purpose/privacy/redaction rules remain applicable.

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

AI-02.1 and AI-03 responsibility boundaries do not imply one microservice/container per box or one module/table per Context/Retrieval/Memory contract. Any future extraction requires measured evidence.

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

pnpm isolated layout is preferred/direct-validation-required. Evidence-driven `nodeLinker: hoisted` fallback is allowed without reopening architecture.

Turbo orchestrates JS/frontend task graph only; GitHub Actions remains repository-wide CI/CD authority.

## TD-13 — Frontend data/state authority

**ACCEPTED / INTEGRATED VIA PR #22**

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

Feature UI uses feature data/model boundaries rather than direct HTTP/PowerSync/query-cache/storage ownership. No universal frontend `Repository[T]`.

## TD-14 — Frontend offline posture

**ACCEPTED / INTEGRATED VIA PR #22**

Mobile activates PowerSync + encrypted SQLite when materialized for a capability that needs it, initially app-owned under Mobile platform sync boundary.

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

No divergent Windows/WSL source-tree clones or shared cross-OS `node_modules` environment.

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

**ACCEPTED / QUALIFIED BY POSTGRESQL CONSTITUTION**

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

Detailed current doctrine is governed by ADR-010 and the closed CP6-02 Constitution.

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

Protected-main required contexts are repository-enforced current contexts, not guessed names. Documentation snapshots must not override the live ruleset.

Current named required checks in accepted project documentation:

```text
Backend CI Gate
Dependency Review
Frontend CI Gate
```

Protected workflows use least privilege and immutable Action SHA pinning. Supply-chain controls activate with real artifacts/manifests/capabilities.

## TD-25 — Cloud/IaC and current implementation boundary

**PARTLY DEFERRED / CURRENT**

Backend compute provider, IaC engine, registry and remote sizing remain deliberately deferred until first remote infrastructure.

Closed/integrated foundations:

```text
Frontend Engineering Foundation   CLOSED / INTEGRATED VIA PR #22
Frontend Materialization          CLOSED / PASS / INTEGRATED VIA PR #28
Backend CP1–CP5 scaffold          CLOSED / DIRECT QA / INTEGRATED VIA PR #24
Backend CP6 database              CLOSED / DIRECT QA / INTEGRATED VIA PR #42
PostgreSQL LOCAL Recovery         CLOSED / LOCAL PASS / INTEGRATED VIA PR #47
```

Current protected-main database/recovery baseline:

```text
PostgreSQL          18.6
Alembic             20260830_09
69 tables
5 views
15 routines
76 triggers
97 indexes
69 FKs
123 CHECKs
remote backup provider   TBD / NOT ACTIVATED
production/cloud recovery NOT CLAIMED
```

Current bounded unmerged workstreams observed at the 2026-09-01 reconciliation:

```text
feature/access-auth             active full-stack product vertical
feature/home-react              active frontend workstream
feature/platform-observability  active platform workstream
feature/ai-architecture         active AI architecture design/reengineering workstream
```

The old wording that the first post-CP6 backend product vertical had not started is deprecated/stale. `feature/access-auth` is a real active full-stack vertical.

The old CP6-03 → Gate 03 → CP6-04 → CP6-05 sequence and Recovery CP01–CP07 sequence are completed historical execution, not current next-step plans.

## TD-26 — PostgreSQL Persistence Constitution

**ACCEPTED / CROSS-CUTTING**

DANTE accepts the reusable PostgreSQL persistence doctrine closed by CP6-02 and implemented through CP6/Recovery evolution.

ADR authority:

`docs/decisions/ADR-010-postgresql-persistence-constitution.md`

Detailed normative authority:

`docs/development/backend-cp6-02-postgresql-persistence-constitution.md`

Durable consequences include stable UUID/reference addressing, bounded heterogeneous anchors, material-state/current-history separation, typed relation/constraint doctrine, transaction/concurrency/idempotency rules, migration/evolution posture and owner/migrator/runtime privilege separation.

## TD-27 — AI provider replaceability boundary

**ACCEPTED STRUCTURAL BOUNDARY / CONCRETE PROVIDER-MODEL SELECTION OPEN**

DANTE feature, Domain and accepted intelligence semantics must not depend directly on one concrete model/provider SDK identity.

Binding separation:

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
DANTE FEATURE/BUSINESS CODE != CONCRETE PROVIDER SDK
PROVIDER REPLACEABLE != PROVIDERS IDENTICAL
PROVIDER REPLACEABLE != LOWEST-COMMON-DENOMINATOR PROVIDER USAGE
```

Productionization direction:

```text
DANTE work/capability need
→ ModelTarget
→ HarnessProfile
→ ProviderBinding
→ Provider Adapter
→ concrete provider / model / deployment
```

`HarnessProfile` preserves provider/model-specific controllable behavior rather than pretending all providers expose identical capabilities. `ProviderBinding` resolves a target to the concrete endpoint/model/deployment/auth/configuration posture. `ProviderAdapter` owns protocol/SDK-specific request, stream, tool, structured-output, usage/error and receipt translation.

This architecture permits, for example, a later direct-provider → Azure-hosted deployment change or an Anthropic/Gemini/other adapter without rewriting DANTE feature/Domain/Context/Retrieval/Memory/Effect semantics.

It does **not** require multi-provider implementation on day one. AI-04 must first define representative workloads/evals and may select one primary V1 provider if that is the best measured simplicity/quality/cost posture.

Concrete provider/model/deployment/SDK selection remains AI-04 evidence-driven work and is not accepted by TD-27 itself.

## Current branch-local AI architecture context — NON-ACCEPTED IMPLEMENTATION SELECTION

`feature/ai-architecture` is currently at:

```text
AI-00  Semantic & Product Foundation
       COMPLETE

AI-01  Product Form + Production Engineering Research
       COMPLETE

AI-02  Intelligence Runtime Architecture
       COMPLETE / STRUCTURALLY ACCEPTED
       AI-02.1 v0.5 CLOSED
       all pressure/mega-test rounds complete
       targeted v0.5 structural verification complete

AI-03  Context / Retrieval / Memory
       CLOSED / STRUCTURALLY ACCEPTED
       AI-03A CLOSED / C01..C33
       AI-03B CLOSED / B01..B35
       AI-03C CLOSED / MAT-01..MAT-15

AI-04  Productionization Architecture
       ACTIVE / CURRENT
       workload/eval first
       provider/model/economics after eval requirements
       concrete runtime/capabilities/external intelligence
       security/privacy/control-plane/operations

AI-05  Whole-System Acceptance + Implementation Blueprint
       FUTURE / FINAL ARCHITECTURE-TO-BUILD BOUNDARY
```

This is **not** a new accepted provider/runtime technology selection. It records branch-local responsibility boundaries and current design sequencing while concrete provider/runtime activation decisions remain open.

AI-03 accepted contracts/invariants include:

```text
ContextPlan
InformationNeed
ContextStrategy
ContextFragment
ContextReadiness
ConsumerContext
ContextManifest
+ inherited BasisManifest

AI-03A C01..C33
AI-03B B01..B35
AI-03C MAT-01..MAT-15
```

Important accepted boundaries include:

```text
Context != canonical reality
Context != Retrieval != Memory
Reality Scope is explicit
Scenario A != Scenario B != canonical current
Source Standing != Domain Authority
DATA != INSTRUCTION
model-discovered need may refine != may widen WorkContract/policy scope
Interaction Session continuity != provider-context continuity
WorkContract propagation != parent-context inheritance
ConsumerContext != ContextManifest
ContextManifest != BasisManifest
ContextReadiness is consumer-specific and non-monotonic
RetrievalCandidate != ContextFragment
APPROXIMATE != COMPLETE
Memory survival defaults to NO
Memory exists != memory may be recalled
processing/retrieval eligibility != retention/future-reuse eligibility
canonical application memory belongs to Domain/PostgreSQL
restored derived bytes != restored eligibility
ANN is optimization, not prerequisite
derived representation generations must not mix silently
semantic obligation != execution/audit evidence
```

AI-03 closure required no Domain/Logical/Physical/PostgreSQL/Alembic change and claims no implementation PASS.

Current structural constraints relevant to AI-04 technical selection include:

```text
API-first frontier intelligence posture
no foundation-model training baseline
no DANTE-owned frontier model
no large always-on self-hosted frontier fleet/GPU cluster baseline
provider/model replaceability
ModelTarget / HarnessProfile / ProviderBinding / ProviderAdapter separation
semantic/deterministic fast path
Execution Environment isolation only when workload/threat model requires it
no raw privileged credentials in arbitrary generated/untrusted code
policy mesh rather than model-selected authorization
safe publication rather than raw sensitive provider stream
PostgreSQL remains sole canonical persistence/material-history authority
search/vector/cache/provider memory remain noncanonical
AI-03 Context/Retrieval/Memory contracts are fixed upstream for AI-04
materialization/activation follows demonstrated consumer need + direct proof
```

Current AI authority:

```text
docs/architecture/dante-ai-03-context-retrieval-memory.md
docs/architecture/dante-ai-03a-full-context-architecture.md
docs/architecture/dante-ai-03b-retrieval-memory-architecture.md
docs/architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md
docs/workstreams/ai-architecture.md
```

Temporary branch continuity may additionally use:

```text
docs/workstreams/ai-architecture-live-handoff.md
TEMPORARY / MUST NOT MERGE TO protected main
```

Concrete choices remain OPEN/DEFERRED, including:

```text
OpenAI / Azure OpenAI / Anthropic / Gemini / other provider selection
specific model/deployment mapping
model routing/gateway product or implementation
agent SDK/framework
exact Execution Environment technology
local model family/size/server
conversation persistence physical form
Run/working persistence physical form
memory persistence beyond already accepted Domain ownership
embedding model / dimensions
pgvector/FTS activation for AI retrieval
HNSW / IVFFlat design
chunk/document retrieval schema
reranker / hybrid retrieval implementation
summary/compaction/adaptive-memory persistence
provider thread/cache strategy
```

No such choice is promoted to accepted technology merely because AI-04 is active.

## Selected technologies not to reintroduce casually

Closed Physical/Engineering/Frontend selections exclude or do not select as current defaults, among others:

- separate graph/vector/search/event-store canonical databases;
- Redis/Valkey/Kafka/RabbitMQ/NATS/Debezium by default;
- universal event sourcing;
- Temporal/DBOS/Celery as default workflow stack where Restate remains the accepted Class-B target;
- Zero/Electric/CRDT canonical authority;
- Next.js for the authenticated DANTE Web app;
- Flutter/React Native Web universal renderer;
- Nx baseline;
- Redux as default state authority;
- browser PowerSync/TanStack alpha integration as baseline;
- generic PWA/service-worker offline baseline;
- mandatory Kubernetes/microservices for AI responsibility boxes;
- mandatory sandbox/microVM for every AI request;
- large always-on self-hosted frontier inference fleet as baseline.

Reopen only with materially changed requirements/evidence and explicit scope.
