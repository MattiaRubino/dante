# DANTE Technical Decisions

- **Status:** CURRENT DECISION REGISTER
- **Last reconciled:** 2026-09-03
- **Branch note:** protected `main` remains the integrated baseline; `feature/access-auth` contains newer accepted/materialized Access/Auth + Email Platform truth until explicit integration

This file summarizes current accepted technical decisions. Detailed rationale and constraints live in linked Domain/Logical/Physical/Engineering/Frontend/Access authorities and ADRs. Historical phase-time status does not override later executable/materialized evidence.

## TD-01 — Canonical persistence

**ACCEPTED**

```text
PostgreSQL 18 major family
sole canonical persistence + material-history authority

Physical/CP2/CP3 historical exact patch  18.4
current repository patch                 18.6
protected-main CP6 Alembic               20260826_08
feature/access-auth Alembic              20260903_15
```

Current `feature/access-auth` catalog:

```text
87 tables / 5 views / 15 routines / 75 triggers
170 physical indexes / 88 FKs / 267 CHECKs
```

Patch maintenance inside PostgreSQL 18 does not reopen the selected architecture. No separate graph/vector/search/event-store database is canonical by default.

## TD-02 — PostgreSQL capability envelope

**ACCEPTED**

Selected target:

- PostGIS 3.6.4;
- pgvector 0.8.6;
- native FTS;
- pg_trgm;
- unaccent;
- pg_stat_statements;
- PgBouncer 1.25.2 when concretely activated/validated.

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

## TD-04 — Async/durable work

**ACCEPTED / FIRST CLASS-A CONSUMER MATERIALIZED**

Class A: PostgreSQL transactional outbox + bounded worker.

The shared Email Platform is the first concrete Class-A consumer and is materialized through:

```text
dante.email_delivery_intent
dante.email_delivery_attempt
dante.email_provider_event
dante.email_recipient_suppression
```

Auth/business mutation + EmailIntent are atomically coordinated; external provider I/O occurs after commit. Email is technical durable-work state, not DANTE MaterialState.

Class B: Restate remains selected/dormant until first real Class-B durable workflow.

## TD-05 — Object bytes

**ACCEPTED TARGET / TRIGGER-BASED ACTIVATION**

Cloudflare R2 Standard, private, EU-jurisdiction posture, raw bytes only. PostgreSQL owns ContentArtifact authority/metadata/provenance/visibility/retention/hash/locator semantics.

## TD-06 — Recovery

**ACCEPTED TARGET / ACTIVATION AT RECOVERY OR PRODUCTION BOUNDARY**

```text
pgBackRest 2.59.0
+ AWS S3 Standard eu-south-1
+ Versioning/Object Lock GOVERNANCE posture
+ WAL/PITR
```

Email Platform adds a specific post-restore rule:

```text
email workers CLOSED
→ restore
→ reconciliation
→ uncertain restored nonterminal email work = recovery_quarantined
→ sensitive payload wiped
→ workers reopen
```

## TD-07 — Solver

**ACCEPTED TARGET / TRIGGER-BASED ACTIVATION**

OR-Tools CP-SAT. `UNKNOWN != INFEASIBLE`. Solver output remains candidate/derived until governed acceptance.

## TD-08 — Observability

**ACCEPTED TARGET**

Backend: OpenTelemetry + Grafana Alloy + Grafana Cloud EU + pg_stat_statements.

Frontend: Sentry behind bounded Web/Mobile observability adapters when activated.

Email Platform currently exposes privacy-minimized DB-backed operational signals without recipient/secret dimensions. No OTP/recovery proof belongs in logs, metrics or traces.

## TD-09 — Repository strategy and root ownership

**ACCEPTED**

One DANTE product monorepo; keep current repository.

Reserved root ownership:

```text
apps/
packages/
infra/
tooling/
tests/system/
docs/
prototypes/
.github/
```

Paths are created only when real content exists.

## TD-10 — Backend architecture

**ACCEPTED**

Capability-first modular monolith.

- no mechanical 57 owners → 57 modules translation;
- no generic CRUD `Repository[T]` semantic model;
- no BaseService/service locator/global DB session;
- Domain/application meaning independent of FastAPI/SQLAlchemy/provider SDK identity;
- explicit composition root;
- private module implementation is not a public interface;
- cross-module ACID transaction allowed when semantics require it.

Access/Auth and Email Platform follow this model: provider SDK/SMTP/WebAuthn details remain outside Domain/application authority.

## TD-11 — Frontend application architecture

**ACCEPTED / INTEGRATED**

```text
apps/web     React DOM + Vite + TanStack Router
apps/mobile  React Native + Expo + Expo Router
```

Feature-first boundaries, thin route adapters, no Web/Mobile private cross-imports, executable architecture rules, shared packages only for real multi-consumer value.

## TD-12 — Frontend language/toolchain

**ACCEPTED / INTEGRATED**

```text
Node 24 LTS
TypeScript 6.0.x strict
pnpm 11
Turborepo 2.x
```

## TD-13 — Frontend data/state authority

**ACCEPTED / INTEGRATED**

```text
canonical accepted state/effect   backend + PostgreSQL
synced local projection           PowerSync/SQLite noncanonical
offline pending mutation          local staging only
remote request state              TanStack Query + typed API
online governed command           FastAPI/backend
form draft                        TanStack Form
component transient               React
cross-tree transient              Zustand only when justified
```

Browser/provider/WebAuthn completion is evidence only; backend response remains Auth success authority.

## TD-14 — Frontend offline posture

**ACCEPTED / INTEGRATED**

Mobile activates PowerSync + encrypted SQLite only for capabilities that need it. Web baseline remains online-first. Browser PWA/service-worker offline behavior is not baseline.

## TD-15 — Frontend API/codegen

**ACCEPTED / MATERIALIZED FOR ACCESS/AUTH**

```text
FastAPI/Pydantic
→ deterministic OpenAPI 3.1 snapshot
→ Orval 8 Fetch generation
→ @dante/api-client
→ Web/Native application boundary
→ UI
```

Generated source is deterministic and drift checked.

## TD-16 — Frontend UI/tokens/i18n/time

**ACCEPTED / INTEGRATED**

Web UI uses the DANTE layer over Radix + Tailwind/CSS variables + Motion where required. Mobile uses DANTE RN components over native RN styling/animation primitives. Shared semantic tokens/i18n/time cores remain framework-bounded as accepted.

## TD-17 — Frontend Web runtime config/delivery

**ACCEPTED / INTEGRATED**

Immutable SPA promotion with validated public runtime config where supported. Cloudflare Workers Static Assets remains selected Web delivery target. Client config never contains secrets.

## TD-18 — Mobile build/release

**ACCEPTED / INTEGRATED AS ARCHITECTURE**

EAS Build/Submit/Update selected. GitHub Actions remains primary orchestration. M6 remains future/optional and requires re-gating.

## TD-19 — Backend language/runtime

**ACCEPTED**

```text
Python 3.14.x
uv
apps/backend/src/dante
Ruff
mypy strict
pytest
Hypothesis
```

## TD-20 — Developer OS/workflow

**ACCEPTED**

Backend canonical semantics: Linux. Primary Windows posture uses one authoritative WSL-backed repository checkout. No divergent Windows/WSL source clones or shared cross-OS dependency trees.

## TD-21 — LOCAL container/persistence toolkit

**ACCEPTED**

Backend process direct in WSL/Linux for normal reload/debug; Docker Compose owns LOCAL stateful dependencies; future backend deployable uses OCI packaging.

```text
SQLAlchemy 2.x
psycopg 3
Alembic
```

Disposable PostgreSQL harnesses may isolate automated/manual UAT.

## TD-22 — Migration/copy/recovery governance

**ACCEPTED / QUALIFIED BY POSTGRESQL CONSTITUTION**

- Alembic revision history = deployment schema-change authority;
- autogenerate candidate only;
- applied revisions immutable;
- schema drift tested;
- expand → migrate → contract;
- bounded resumable backfills;
- separated DB privilege classes;
- logical copy distinct from physical PITR recovery;
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

Backend uses typed fail-fast settings and remote workload-identity/secret-manager posture. Client config is public and never contains secrets.

Real-provider UAT is explicit opt-in. Email local UAT uses a named `dante-uat` AWS profile with temporary `aws login` credentials; no Access Key is required for the dedicated IAM user.

## TD-24 — Testing/CI/supply chain

**ACCEPTED**

GitHub Actions primary CI/CD.

Backend uses risk-layered unit/application/property/architecture/real-PostgreSQL/migration/concurrency/provider/API/privacy/release validation. Frontend uses strict type/boundary/cycle checks plus unit/component/E2E layers.

Access/Auth and Email Platform retain separate manual real-boundary proof: a simulated provider test never becomes a real-provider acceptance claim.

## TD-25 — Cloud/IaC and current implementation boundary

**PARTLY DEFERRED / CURRENT**

Backend general compute provider, IaC engine, registry and remote sizing remain deliberately deferred until first remote infrastructure. A bounded provider selection for email does not automatically select the entire DANTE hosting platform.

Current branch truth:

```text
PostgreSQL                         18.6
Access/Auth Alembic                20260903_15
Access/Auth + Email tables         87
views                              5
routines                           15
triggers                           75
physical indexes                  170
foreign keys                       88
CHECK constraints                 267
```

Current product boundary:

```text
feature/access-auth
→ M1–M4 closed
→ M5 Groups 1–3 engineering pass
→ Group 4 automated QA pass
→ real Windows Hello/passkey UAT pass
→ real Google UAT pass
→ shared Email Platform engineering + real SES UAT closed
→ real Apple registered-domain UAT deferred/open
→ whole M5 final closure reconciliation current
```

## TD-26 — PostgreSQL Persistence Constitution

**ACCEPTED / CROSS-CUTTING**

Authority:

- `docs/decisions/ADR-010-postgresql-persistence-constitution.md`
- `docs/development/backend-cp6-02-postgresql-persistence-constitution.md`

Durable consequences include stable reference addressing, material-state/current-history separation, transaction/concurrency/idempotency rules, migration/evolution posture and owner/migrator/runtime privilege separation.

## TD-27 — Shared transactional Email Platform

**ACCEPTED / MATERIALIZED / REAL-PROVIDER UAT PASS**

Authorities:

- `docs/architecture/email-platform.md`
- `docs/decisions/ADR-012-email-delivery-platform.md`
- `docs/development/email-platform-local-uat.md`
- `docs/development/email-platform-acceptance-2026-09-03.md`
- `docs/architecture/access-auth-email-delivery.md` for the first consumer only

Decision:

```text
DANTE owns email intent/lifecycle/state
specialist provider owns last-mile Internet delivery
PostgreSQL transactional outbox is materialized
feature mutation + EmailIntent commit atomically
provider I/O occurs after commit
Amazon SES API v2 is accepted primary external adapter
SMTP remains LOCAL/CI/generic compatibility adapter
provider feedback returns into DANTE event/suppression state
```

Current persistence:

```text
dante.email_delivery_intent
dante.email_delivery_attempt
dante.email_provider_event
dante.email_recipient_suppression
```

Security/operational consequences:

```text
provider accepted != delivered
network timeout != definitely not sent
no blind retry after ambiguous send
OTP/recovery secret excluded from logs/metrics/traces
short-lived dedicated AEAD-protected sensitive payload
terminal/unsafe-state secret wipe
hard bounce/complaint may create DANTE delivery restriction
Auth/security tracking + click rewriting OFF
production SPF + DKIM + DMARC required before sender acceptance
Auth/security / product notifications / future marketing separable
production workload identity preferred over developer IAM user/static credentials
```

Accepted real SES UAT used `eu-west-3`/Paris and proved signup verification, password recovery, reset notification, no auto-login, prior-session revocation, provider MessageId correlation and secret wipe in direct PostgreSQL inspection.

SES region is deployment configuration; no current architecture hardcodes Milan as the preferred production region.

Production sender-domain/DNS/reputation, workload identity and live cloud event-ingress remain separate deployment gates. `ACCEPTED PLATFORM != PRODUCTION DEPLOYED` remains binding.

## Selected technologies not to reintroduce casually

Closed Physical/Engineering/Frontend selections exclude or do not select as defaults, among others: separate graph/vector/search/event-store canonical databases; Redis/Valkey/Kafka/RabbitMQ/NATS/Debezium by default; universal event sourcing; Temporal/DBOS/Celery default workflow stack; Zero/Electric/CRDT canonical authority; Next.js for the authenticated DANTE Web app; Flutter/React Native Web universal renderer; Nx baseline; Redux as default state authority; generic PWA/service-worker offline baseline; self-hosted production MTA as the default DANTE email architecture.

Reopen only with materially changed requirements/evidence and explicit scope.
