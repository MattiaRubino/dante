# DANTE Technical Decisions

- **Status:** CURRENT DECISION REGISTER
- **Last reconciled:** 2026-09-03
- **Branch note:** protected `main` is integrated authority; `feature/access-auth` contains newer accepted Auth + Email truth until its integration gate completes

Historical milestone progress does not override later accepted executable/materialized evidence.

## TD-01 — Canonical persistence

**ACCEPTED**

```text
PostgreSQL 18 major family
sole canonical persistence + material-history authority

Physical/CP2/CP3 historical exact patch  18.4
current repository patch                 18.6
historical common CP6 head               20260826_08
protected-main current Alembic           20260830_09 / Recovery
feature/access-auth current Alembic      20260903_15 / Auth + Email
```

Current Access-branch catalog before convergence:

```text
87 tables / 5 views / 15 routines / 75 triggers
170 physical indexes / 88 FKs / 267 CHECKs
```

The two Alembic histories diverge after `20260826_08`; integration preserves both and uses a forward merge revision. No separate graph/vector/search/event-store database is canonical by default.

## TD-02 — PostgreSQL capability envelope

**ACCEPTED**

- PostGIS 3.6.4
- pgvector 0.8.6
- native FTS
- pg_trgm
- unaccent
- pg_stat_statements
- PgBouncer 1.25.2 when concretely activated/validated

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

Class A = PostgreSQL transactional outbox + bounded worker.

The shared Email Platform is the first concrete Class-A consumer:

```text
dante.email_delivery_intent
dante.email_delivery_attempt
dante.email_provider_event
dante.email_recipient_suppression
```

Feature mutation + EmailIntent are atomically coordinated; provider I/O occurs after commit. Email delivery state is technical control/evidence, not DANTE MaterialState.

Class B Restate remains selected/dormant until first real Class-B durable workflow.

## TD-05 — Object bytes

**ACCEPTED TARGET / TRIGGER-BASED ACTIVATION**

Cloudflare R2 Standard, private, EU-jurisdiction posture, raw bytes only. PostgreSQL owns ContentArtifact authority/metadata/provenance/visibility/retention/hash/locator semantics.

## TD-06 — Recovery

**ACCEPTED / PROTECTED-MAIN RECOVERY EVOLUTION INTEGRATED**

Recovery architecture remains:

```text
pgBackRest 2.59.0
+ AWS S3 Standard eu-south-1
+ Versioning/Object Lock GOVERNANCE posture
+ WAL/PITR
```

Protected main includes the bounded material-state retirement/recovery evolution at Alembic `20260830_09`.

Email Platform adds:

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

**ACCEPTED / IMPLEMENTED ON SEPARATE CLOSED BRANCH / NOT YET MAIN-INTEGRATED**

Accepted platform implementation lives on `feature/platform-observability` and includes:

```text
backend OpenTelemetry
Grafana Alloy
Grafana Cloud EU
Prometheus/Loki/Tempo paths
pg_stat_statements + bounded PostgreSQL observer
Web Grafana Faro instrumentation
black-box readiness
dashboards + governed alerts
privacy/redaction/cardinality/failure-isolation contracts
```

The older Sentry-as-frontend-target wording is superseded by the accepted Faro implementation on that closed workstream. This Access branch does not claim Observability is already integrated into protected main.

Email Platform exposes privacy-minimized operational signals without recipient/secret dimensions. OTP/recovery proof never belongs in logs, metrics or traces.

## TD-09 — Repository strategy and root ownership

**ACCEPTED**

One DANTE product monorepo.

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

Paths exist only when real content exists.

## TD-10 — Backend architecture

**ACCEPTED**

Capability-first modular monolith.

- no mechanical 57 owners → 57 modules translation
- no generic CRUD `Repository[T]` semantic model
- no BaseService/service locator/global DB session
- Domain/application meaning independent of FastAPI/SQLAlchemy/provider SDK identity
- explicit composition root
- private module implementation is not a public interface
- cross-module ACID transaction allowed when semantics require it

Access/Auth and Email Platform follow this model.

## TD-11 — Frontend application architecture

**ACCEPTED / INTEGRATED FOUNDATION**

```text
apps/web     React DOM + Vite + TanStack Router
apps/mobile  React Native + Expo + Expo Router boundary
```

Feature-first boundaries, thin route adapters, no Web/Mobile private cross-imports, executable architecture rules, shared packages only for real multi-consumer value.

## TD-12 — Frontend language/toolchain

**ACCEPTED / INTEGRATED**

```text
Node 24 LTS
TypeScript 6 strict
pnpm 11
Turborepo 2
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

**ACCEPTED / INTEGRATED FOUNDATION**

Mobile activates PowerSync + encrypted SQLite only for capabilities that need it. Web remains online-first. Generic browser PWA/service-worker offline behavior is not baseline.

## TD-15 — Frontend API/codegen

**ACCEPTED / MATERIALIZED FOR ACCESS/AUTH**

```text
FastAPI/Pydantic
→ deterministic OpenAPI 3.1 snapshot
→ Orval Fetch generation
→ @dante/api-client
→ Web/Native application boundary
→ UI
```

Generated source is deterministic and drift checked.

## TD-16 — Frontend UI/tokens/i18n/time

**ACCEPTED / INTEGRATED FOUNDATION**

Web UI uses the DANTE layer over accepted primitives/tokens. Mobile uses DANTE RN components over native RN styling/animation primitives. Shared semantic tokens/i18n/time cores remain framework-bounded.

## TD-17 — Frontend Web runtime config/delivery

**ACCEPTED / INTEGRATED FOUNDATION**

Immutable SPA promotion with validated public runtime config where supported. Cloudflare Workers Static Assets remains selected Web delivery target. Client config never contains secrets.

## TD-18 — Mobile build/release

**ACCEPTED AS ARCHITECTURE / IMPLEMENTATION FUTURE**

EAS Build/Submit/Update selected. GitHub Actions remains primary orchestration. Native Mobile product work remains future/optional and requires explicit re-gating.

## TD-19 — Backend language/runtime

**ACCEPTED**

```text
Python 3.14.x
uv
apps/backend/src/dante
Ruff
mypy strict
pytest
Hypothesis where meaningful
```

## TD-20 — Developer OS/workflow

**ACCEPTED**

Backend canonical semantics are Linux. Primary Windows posture uses one authoritative WSL-backed repository checkout. No divergent Windows/WSL source clones or shared cross-OS dependency trees.

## TD-21 — LOCAL container/persistence toolkit

**ACCEPTED**

Backend process runs directly in WSL/Linux for normal reload/debug; Docker Compose owns LOCAL stateful dependencies; future backend deployable uses OCI packaging.

```text
SQLAlchemy 2.x
psycopg 3
Alembic
```

Disposable PostgreSQL harnesses isolate automated/manual UAT.

## TD-22 — Migration/copy/recovery governance

**ACCEPTED / QUALIFIED BY POSTGRESQL CONSTITUTION**

- Alembic revision history = deployment schema-change authority
- autogenerate candidate only
- applied revisions immutable
- schema drift tested
- expand → migrate → contract
- bounded resumable backfills
- separated DB privilege classes
- logical copy distinct from physical PITR recovery
- raw PROD → DEV forbidden by default
- PostgreSQL major upgrade is separate platform work
- divergent accepted feature histories converge through explicit Alembic merge revisions, never history rewriting

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

Real-provider UAT is explicit opt-in. Email local UAT uses a named `dante-uat` AWS profile with temporary browser-login credentials; no static Access Key is required for the dedicated UAT IAM user.

## TD-24 — Testing/CI/supply chain

**ACCEPTED**

GitHub Actions is primary CI/CD.

Backend uses risk-layered unit/application/property/architecture/real-PostgreSQL/migration/concurrency/provider/API/privacy/release validation. Frontend uses strict type/boundary/cycle checks plus unit/component/E2E layers.

A simulated provider test never becomes a real-provider acceptance claim.

## TD-25 — Cloud/IaC and current implementation boundary

**PARTLY DEFERRED / CURRENT**

General backend compute provider, IaC engine, registry and remote sizing remain deliberately deferred until real remote infrastructure requires them. Email-provider selection does not select the whole hosting platform.

Current branch truth:

```text
PostgreSQL                         18.6
feature/access-auth Alembic        20260903_15
Access branch topology             87/5/15/75/170/88/267
Access M1–M5                       CLOSED / ACCEPTED
Windows Hello UAT                  PASS
Google real UAT                    PASS
Email Platform + real SES UAT      CLOSED / PASS
Apple real registered-domain UAT   BOUNDED DEFERRED / NON-BLOCKING
current work                       PRE-INTEGRATION AUDIT
```

Protected main separately owns Recovery at `20260830_09`. Combined truth is not claimed before merge + proof.

## TD-26 — PostgreSQL Persistence Constitution

**ACCEPTED / CROSS-CUTTING**

Authority:

- `../decisions/ADR-010-postgresql-persistence-constitution.md`
- `../development/backend-cp6-02-postgresql-persistence-constitution.md`

Durable consequences include stable reference addressing, material-state/current-history separation, transaction/concurrency/idempotency rules, migration/evolution posture and owner/migrator/runtime privilege separation.

## TD-27 — Shared transactional Email Platform

**ACCEPTED / MATERIALIZED / REAL-PROVIDER UAT PASS**

Authorities:

- `email-platform.md`
- `../decisions/ADR-012-email-delivery-platform.md`
- `../development/email-platform-local-uat.md`
- `../development/email-platform-acceptance-2026-09-03.md`
- `access-auth-email-delivery.md` for the first consumer only

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
hard bounce/complaint may create delivery restriction
Auth/security tracking + click rewriting OFF
production SPF + DKIM + DMARC required before sender acceptance
production workload identity preferred over developer credentials
```

Accepted SES UAT used `eu-west-3`/Paris and proved signup verification, password recovery, reset notification, no auto-login, prior-session revocation, provider MessageId correlation and secret wipe.

SES region remains deployment configuration. Production sender-domain/DNS/reputation, workload identity and live cloud event-ingress are separate deployment gates.

## TD-28 — Shared-foundation integration order

**ACCEPTED / CURRENT EXECUTION POSTURE**

```text
close/audit feature/access-auth
→ merge protected main into Access branch
→ forward Alembic merge + combined QA
→ PR Access/Auth + Email to main
→ merge enriched main into already-closed platform-observability branch
→ observability integration/release rechecks
→ PR Observability to main
→ future product branches start from enriched main
```

This prevents long-lived foundation branches from blocking unrelated product work and avoids layering new M6/M7 scope onto a branch that first needs to return shared capability to main.

## Technologies not to reintroduce casually

Closed Physical/Engineering/Frontend selections exclude or do not select as defaults, among others: separate graph/vector/search/event-store canonical databases; Redis/Valkey/Kafka/RabbitMQ/NATS/Debezium by default; universal event sourcing; Temporal/DBOS/Celery as default workflow stack; CRDT canonical authority; Next.js for the authenticated DANTE Web app; universal Web/Native renderer; Redux as default state authority; generic PWA/service-worker offline baseline; self-hosted production MTA as default email architecture.

Reopen only with materially changed requirements/evidence and explicit scope.