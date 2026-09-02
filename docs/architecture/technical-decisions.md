# DANTE Technical Decisions

- **Status:** CURRENT DECISION REGISTER
- **Last reconciled:** 2026-09-02

This file summarizes current accepted technical decisions. Detailed rationale and constraints remain in Domain/Logical/Physical/Engineering/Frontend sources, architecture authorities and ADRs. Git preserves phase-time chronology.

AI architecture design/reengineering is now structurally closed. The accepted implementation boundary is current, while concrete provider/model/SDK, retrieval accelerators, durable AI state and production activation remain evidence/trigger-driven unless explicitly selected below.

## TD-01 — Canonical persistence

**ACCEPTED**

```text
PostgreSQL 18 major family
= sole canonical persistence + material-history authority

current patch                     18.6
historical pre-Recovery Alembic   20260826_08
current Alembic head              20260830_09
current topology                  69 tables / 5 views / 15 routines /
                                  76 triggers / 97 indexes / 69 FKs /
                                  123 CHECK constraints
```

No separate graph/vector/search/event-store database is canonical by default.

## TD-02 — PostgreSQL capability envelope

**ACCEPTED TARGET / TRIGGER-BASED USE**

Selected capability envelope includes PostGIS 3.6.4, pgvector 0.8.6, native FTS, pg_trgm, unaccent, pg_stat_statements and PgBouncer target posture.

Availability in the image does not mean Search/vector/AI serving is activated. FTS/trgm/vector remain direct-evidence and same-change gated.

## TD-03 — Offline/sync

**ACCEPTED TARGET / OPERATION-SPECIFIC ACTIVATION**

PowerSync + encrypted SQLite bounded local state.

```text
SQLite != canonical truth
PowerSync arrival order != conflict resolution
local pending mutation != canonical accepted effect
consequential offline mutation → backend governance/revalidation → PostgreSQL
```

## TD-04 — Async/durable work

**ACCEPTED / TRIGGER-BASED ACTIVATION**

```text
Class A → PostgreSQL transactional outbox + bounded worker
Class B → Restate, dormant until first real durable workflow
```

Durability is workload/semantics-driven, not simply elapsed time.

## TD-05 — Object bytes

**ACCEPTED TARGET / TRIGGER-BASED ACTIVATION**

Cloudflare R2 Standard private/EU posture for raw bytes when real `ContentArtifact` byte flow exists. PostgreSQL retains semantic authority/metadata/provenance/visibility/retention/hash/locator meaning.

## TD-06 — Recovery

**ACCEPTED PHYSICAL TARGET / CURRENT LOCAL IMPLEMENTATION QUALIFIED**

```text
pgBackRest LOCAL recovery   IMPLEMENTED / REHEARSED / PR #47
CP01–CP07                   LOCAL PASS / CLOSED
remote backup provider      TBD / NOT ACTIVATED
production/cloud recovery   NOT CLAIMED
```

Recovery copies remain noncanonical and anti-resurrection obligations remain binding.

## TD-07 — Solver

**ACCEPTED TARGET / TRIGGER-BASED ACTIVATION**

OR-Tools CP-SAT.

```text
UNKNOWN != INFEASIBLE
solver output != accepted canonical effect
```

Activate only for real solver-backed capabilities.

## TD-08 — Observability

**ACCEPTED TARGET**

Backend target: OpenTelemetry + Grafana Alloy + Grafana Cloud EU + pg_stat_statements. Frontend: Sentry behind bounded adapters when activated.

```text
TELEMETRY != AUDIT != CANONICAL TRUTH
```

AI prompts/ConsumerContext/model responses are not automatically safe telemetry.

## TD-09 — Repository strategy and root ownership

**ACCEPTED**

One DANTE product monorepo. Root ownership includes `apps/`, `packages/`, `infra/`, `tooling/`, `tests/system/`, `docs/`, `prototypes/`, `.github/`. Paths are created only when real content exists.

## TD-10 — Backend architecture

**ACCEPTED**

Capability-first modular monolith.

```text
no one-table/owner-per-module mechanical translation
no generic Repository[T]
no generic UnitOfWork/BaseService/service locator
explicit composition root
private implementation != public interface
cross-module ACID allowed when semantics require it
```

AI responsibility boxes do not imply microservices/tables.

## TD-11 — Frontend application architecture

**ACCEPTED / INTEGRATED VIA PR #22**

Web/Mobile feature-first boundaries, thin route/navigation adapters, public-API-only acyclic feature dependencies, selective shared packages and production isolation from prototypes.

## TD-12 — Frontend language/toolchain

**ACCEPTED / INTEGRATED VIA PR #22**

```text
Node 24 LTS
TypeScript 6.0.x strict
pnpm 11
Turborepo 2.x
```

## TD-13 — Frontend data/state authority

**ACCEPTED / INTEGRATED VIA PR #22**

```text
canonical accepted state/effect → backend + PostgreSQL
synced local projection          → PowerSync/SQLite noncanonical
remote request state             → TanStack Query + typed API
form draft                        → TanStack Form
component transient              → React
Zustand                           → only when justified
```

## TD-14 — Frontend offline posture

**ACCEPTED / INTEGRATED VIA PR #22**

Mobile may activate PowerSync + encrypted SQLite for capabilities that need it. Web is online-first. Local data is identity-scoped.

## TD-15 — Frontend API/codegen

**ACCEPTED / INTEGRATED VIA PR #22**

FastAPI OpenAPI → Orval 8 → framework-light API client when real OpenAPI exists. Generated artifacts are deterministic/drift-checked.

## TD-16 — Frontend UI/tokens/i18n/time

**ACCEPTED / INTEGRATED VIA PR #22**

Web DANTE UI layer over Radix/Tailwind/CSS variables/Motion as required; Mobile DANTE RN layer; one semantic token source; framework-free i18n/time shared cores; Temporal-based semantic time handling.

## TD-17 — Web runtime config/delivery

**ACCEPTED / INTEGRATED VIA PR #22**

One immutable SPA artifact promoted across environments where possible, with versioned validated public runtime configuration. Cloudflare Workers Static Assets selected target; bounded bootstrap config is not a BFF/business backend.

## TD-18 — Mobile build/release

**ACCEPTED / INTEGRATED VIA PR #22**

EAS Build/Submit/Update selected. Android/iOS remain supported architecture targets subject to signing/device/store gates.

## TD-19 — Backend language/runtime

**ACCEPTED**

```text
Python 3.14.x
initial exact pin 3.14.7
uv
apps/backend/src/dante
Ruff
mypy strict
pytest / Hypothesis where meaningful
```

## TD-20 — Developer OS/workflow

**ACCEPTED**

Backend canonical semantics are Linux; primary Windows posture uses one authoritative WSL-backed checkout. No divergent Windows/WSL source clones or cross-OS dependency directories.

## TD-21 — LOCAL container/persistence toolkit

**ACCEPTED**

Backend runs directly in WSL/Linux for normal debug/reload; Docker Compose owns LOCAL stateful dependencies. SQLAlchemy 2.0 + psycopg 3 + Alembic are the persistence toolkit.

## TD-22 — Migration/copy/recovery governance

**ACCEPTED**

Alembic is schema-change authority; applied revisions immutable; autogenerate candidate only; structural change uses reviewed forward evolution and same-change documentation/tests. Raw PROD → DEV is forbidden by default.

## TD-23 — Environment/config/secrets

**ACCEPTED**

Exactly:

```text
LOCAL
DEV
UAT
PROD
```

Environment != Git branch. Backend uses typed fail-fast settings; remote workload identity/secret-manager/OIDC posture where applicable. Client config is public and contains no secrets.

## TD-24 — Testing/CI/supply chain

**ACCEPTED**

GitHub Actions is primary CI/CD. Backend uses layered unit/application/property/architecture/real-PostgreSQL/migration/concurrency/provider/API/privacy/release validation. Existing normal CI is never replaced by AI eval/provider evidence.

## TD-25 — Cloud/IaC and current implementation boundary

**PARTLY DEFERRED / CURRENT**

Backend compute provider, IaC engine, registry and remote sizing remain deferred until real remote infrastructure. Closed/integrated foundations include frontend foundation/materialization, backend CP1–CP6 and LOCAL PostgreSQL Recovery.

Current bounded work includes active Access/Auth, Home React, platform observability and the unmerged AI branch whose **architecture design is now closed and ready for implementation entry**.

## TD-26 — PostgreSQL Persistence Constitution

**ACCEPTED / CROSS-CUTTING**

ADR-010 and CP6-02 govern stable UUID/reference addressing, material-state/current-history separation, typed relation/constraint doctrine, transaction/concurrency/idempotency, migration/evolution and owner/migrator/runtime privilege separation.

AI implementation receives no exception.

## TD-27 — AI provider replaceability / production-route boundary

**ACCEPTED STRUCTURAL BOUNDARY / CONCRETE PROVIDER-MODEL-SDK SELECTION OPEN**

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY
HARNESSPROFILE != PROVIDERBINDING
DANTE FEATURE/BUSINESS CODE != CONCRETE PROVIDER SDK
```

One primary V1 provider is allowed if direct DANTE evidence supports it. Provider replaceability does not force lowest-common-denominator usage or multi-provider implementation on day one.

Correct provider lifecycle:

```text
candidate discovery/shortlist
→ candidate admission for qualification
→ inactive private adapter/binding
→ adapter conformance
→ live compatibility using eligible/minimized test data
→ direct DANTE eval on production-owned material composition
→ applicable security/privacy/capacity/economics evidence
→ qualification
→ promotion
```

```text
CANDIDATE ADMISSION != PRODUCTION QUALIFICATION
```

Qualification/live/shadow traffic is real disclosure. Every auxiliary model inference uses the same governed ModelAccess/data-egress/resource/eval boundary.

## TD-28 — Final DANTE Intelligence implementation boundary

**ACCEPTED / BUILD ENTRY AUTHORIZED / IMPLEMENTATION NOT YET STARTED**

Current authority:

```text
docs/architecture/dante-ai-implementation-baseline-final.md
```

Acceptance evidence:

```text
docs/architecture/dante-ai-post05-final-mega-acceptance.md
POST05-H01..H25
MKT-001..MKT-100 PASS
C01..C20 PASS
reverse authority PASS
Product/simulation replay PASS
```

Accepted implementation split:

```text
modules/search
→ independent deterministic Global Search/discovery
→ permission-safe bounded read projection
→ no canonical mutation authority

modules/intelligence
→ Work/Context/Reference/SemanticQuery/Retrieval orchestration
→ optional governed ModelAccess
→ Verification / Result Maturity / explicit NO_EFFECT / Safe Publication
→ no raw database/canonical ownership

provider SDK/protocol
→ admitted private outbound adapter only
```

Additional binding rules:

```text
SEARCH RESULT / CURSOR / TARGET REF != AUTHORIZATION
SEMANTIC QUERY GATEWAY != INTELLIGENCE-OWNED CROSS-CAPABILITY SQL
RetrievalCandidate != ContextFragment
DATA != INSTRUCTION
MASKING / REDACTION != SEMANTIC EQUIVALENCE
PROVIDER COMPLETED != VERIFIED != PUBLISHABLE
PROVIDER FAILURE != DISCLOSURE DID NOT HAPPEN
AUXILIARY MODEL CALL != FREE PROVIDER CALL
DEFAULT NONCANONICAL AI PERSISTENCE = NO
BUILD-READY != INTEGRATION-READY != ACTIVATION-READY
```

First technical vertical remains private authenticated single-turn/request-owned read-only Global Search subset + read-only Ask DANTE. Public streaming, background/durable resume and consequential mutation are OFF initially.

The post-AI05 mega test found **no evidence requiring a Domain, Logical, Physical, PostgreSQL or Alembic change**.

Current implementation sequence starts at:

```text
I0 repository/application ownership + architecture-test skeleton
```

I0 is build-authorized. Production Search/Ask/provider activation is not.