# Technical Decisions

- Status: **Current technical direction — Physical target accepted; Engineering Foundation v0 active**
- Last updated: 2026-08-19
- Current product/app name: **DANTE** (`LifeOS` is the previous working/project name retained only where historical/technical continuity requires it)
- Physical integration commit: `e6f191bad947388a44defe2c15f4939345084f58` via PR #15
- Engineering Foundation branch: `chore/engineering-foundation-v0`
- Engineering Foundation PRE-SCOPE: `ebc3616956faeabd99d90f5f32458b284be218e4`

This document is a current technical summary. Detailed requirements/contracts remain authoritative in their dedicated sources; historical rationale remains in ADRs, evidence and Git.

## Stage boundary

```text
Product / North Star                         CURRENT
Domain Model / Domain Atlas                 CLOSED
Logical Model                               CLOSED
Phase 5 requirements                        CURRENT
Phase 6 AI/context/runtime/integration      CURRENT
Phase 7 durable-execution contract          CURRENT / PHYSICAL MECHANISM RESOLVED
Phase 8 governed operation/effect           CURRENT
Phase 9 search/observability/calendar/solver CURRENT / PHYSICAL MECHANISMS RESOLVED WHERE SELECTED
Phase 10 benchmark method                   CURRENT METHOD / HISTORICAL DECISION-EVIDENCE AUTHORITY
Repository engineering safety              QA PASS at verified scope
Pre-Physical Coherence                      CLOSED / INTEGRATED / VERIFIED

Physical Model target
CLOSED / SELECTED / ACCEPTED / INTEGRATED
selected canonical primary PostgreSQL 18.4

Direct selected-stack implementation validation
NOT STARTED / DIRECT HG PASS 0

Engineering Foundation v0
ACTIVE / UNMERGED

Backend / production implementation
NOT STARTED
```

## Clients and backend direction

Accepted direction:

- Web: Next.js + React + TypeScript.
- Mobile: Expo + React Native + TypeScript.
- Backend: Python + FastAPI + Pydantic.
- Architecture: capability-first modular monolith.
- Clients use versioned governed backend contracts, not direct primary-persistence access.
- Domain/application logic remains independent from HTTP/framework/persistence/provider representations by identity.

Engineering Foundation branch baseline now additionally selects:

```text
BACKEND PERSISTENCE TOOLKIT
SQLAlchemy 2.0 stable line
psycopg 3
Alembic

PYTHON ENGINEERING
Python 3.14 line
uv + committed lockfile
Ruff
mypy strict
pytest

JS ENGINEERING
Node 24 LTS
pnpm 11 + committed lockfile
TypeScript strict
ESLint + Prettier
Turborepo for JS/TS task graph

DELIVERY
GitHub Actions primary CI/CD orchestration
GitHub Environments for privileged deployment once real workflows exist
```

These are active unmerged Foundation decisions. Production backend implementation has not started.

## Repository/application architecture

DANTE uses a **polyglot monorepo** target:

```text
apps/api
apps/web
apps/mobile
packages/<precise-shared-TS-artifacts>
infra
tooling
tests/system
docs
prototypes
```

Rules:

- one integrated source tree allows atomic contract/client/infrastructure/documentation changes;
- production apps never depend on `prototypes/`;
- `packages/` does not become a `shared/common/utils` dumping ground;
- no root Python workspace is introduced while there is only one real Python project;
- backend modules are selected by capability/change cohesion, not one module per table, Logical owner, route or screen;
- no universal generic `Repository[T]`, CRUD `BaseService` or service locator becomes the application model;
- cross-module atomic PostgreSQL transactions remain allowed where accepted semantics require true atomicity;
- microservices/Kubernetes/brokers/build-system complexity require a measured later need rather than enterprise imitation.

Detailed authority: `docs/development/repository-layout-v0.md` and `application-structure-v0.md`.

## Semantic/model authority

Technical design follows the accepted Domain Atlas and closed Logical Model; storage/runtime convenience does not create ontology.

Rejected for the canonical kernel:

```text
universal semantic Entity / Thing
universal generic Relationship / edge
generic EAV / property-bag ontology
provider schema as DANTE ontology
AI-output schema as DANTE ontology
unresolved AI meaning persisted as fabricated generic canonical truth
```

Bounded technical registries, discriminators, references, JSON/provider metadata, indexes and projections remain allowed where semantic ownership stays explicit.

## Accepted Physical persistence/runtime target

### Canonical primary

```text
PostgreSQL 18.4
SELECTED / ACCEPTED
```

PostgreSQL is the sole canonical persistence authority for DANTE current truth/material history through the accepted owner-specific mapping.

### PostgreSQL capability envelope

```text
PostGIS 3.6.4
pgvector 0.8.6
native FTS
pg_trgm
unaccent
pg_stat_statements
PgBouncer 1.25.2
```

These are implementation capabilities, not new Domain owners.

### Offline / multi-device

```text
PowerSync Service 1.25.0 Open Edition
encrypted SQLite local state
PostgreSQL-backed PowerSync sync storage
```

```text
LOCAL != CANONICAL
sync arrival order != semantic conflict resolution
consequential offline mutation -> DANTE backend revalidation -> PostgreSQL
```

No universal consequential LWW.

### Async / durable execution

```text
BOUNDED CLASS A
PostgreSQL transactional outbox + bounded worker

MATERIAL CLASS B
Restate runtime
Restate Python SDK 1.0.3
Restate Server 1.7.2 self-hosted/reproducible subject
```

Restate deployment capability remains:

```text
SELF-HOSTED
FIRST-CLASS

CLOUD EU
ALLOWED MANAGED OPTION

GLOBAL DEFAULT
NONE
```

Current activation truth is more specific than the original generic later-profile wording:

```text
INITIAL DEV
DORMANT / NOT ACTIVE

ACTIVATE
first real Class-B durable-workflow need

SELF-HOSTED vs CLOUD EU
choose only when activation trigger exists
```

Current Python use must not assume TypeScript-only Restate client-side journal encryption. Journal payload minimization remains mandatory when Restate activates.

No workflow runtime creates exactly-once external reality by itself and runtime state does not become Domain ontology/history by identity.

### Object storage

```text
Cloudflare R2 Standard
EU jurisdiction
private
```

R2 stores raw bytes. `ContentArtifact` identity/metadata/provenance/Visibility/retention/hashes/object locator remain PostgreSQL-owned.

### Recovery

```text
pgBackRest 2.59.0
-> AWS S3 Standard eu-south-1
-> Versioning
-> Object Lock GOVERNANCE
-> finite policy-bound retention

R2 raw-object backup
-> separate AWS S3 eu-south-1 repository
```

Recovery copies remain noncanonical. `Object Lock Compliance` is not the default.

Initial DEV activation is already fixed:

```text
pgBackRest + AWS S3
DORMANT / NOT ACTIVE
ACTIVATE = recovery/production boundary OR real recovery rehearsal
```

### Solver

```text
OR-Tools 9.15 CP-SAT
```

Solver output remains candidate/derived state. `UNKNOWN != INFEASIBLE`; solver output != accepted canonical effect.

### Observability

```text
OpenTelemetry
Grafana Alloy 1.18.0
Grafana Cloud EU
pg_stat_statements
```

Telemetry remains privacy-minimized operational state, not Domain Provenance/security audit/canonical history automatically.

## Database engineering decisions

Engineering Foundation fixes the implementation discipline before concrete schema work:

```text
ORM / SQL toolkit       SQLAlchemy 2.0 stable
PostgreSQL driver       psycopg 3
migration system        Alembic
backend DB tests        real PostgreSQL 18.4 semantics
```

Rules:

- SQLite is never used as a convenience substitute to prove backend PostgreSQL semantics;
- application startup does not use `metadata.create_all()` as deployed schema management;
- every durable deployed schema change is an Alembic migration;
- autogenerate output is a candidate requiring review;
- merged/applied migrations are not rewritten for cosmetic convenience;
- one controlled migration/release job executes schema change where required; application replicas do not race on startup;
- risky evolution uses expand/migrate/contract when old/new services or mobile clients overlap;
- `alembic downgrade` is not assumed to be a universal production rollback mechanism;
- session/transaction scope belongs to the application operation/request/job, is injected and not global;
- `AsyncSession` is not shared across concurrent tasks;
- transaction boundaries follow accepted semantic atomicity rather than ORM convenience.

Concrete tables/columns/constraints/indexes/migration revisions remain future implementation.

## Environment and release decisions

Engineering Foundation defines:

```text
LOCAL
individual disposable developer context
Linux backend semantics canonical; Windows via WSL2/Linux
stateful dependencies via Docker Compose as activated

DEV
shared integration environment for accepted main artifacts / synthetic data

UAT
production-like exact release-candidate acceptance + migration rehearsal

PROD
real released service/data
```

No permanent Git branch represents an environment.

Server/web baseline is **build once, promote exact immutable artifact** where the platform permits. Release evidence records source SHA, build ID and artifact/image digest where available.

Mobile is an explicit exception where different signed/environment-specific binaries may be required; each build remains tied to the same reviewed source, locked dependencies and explicit build profile.

Exact compute hosting provider, artifact registry and IaC engine are intentionally deferred until real remote infrastructure implementation because accepted architecture has not selected them.

## Configuration / secret decisions

- backend configuration uses typed `pydantic-settings` at bootstrap;
- invalid/missing critical deployed configuration fails before serving work;
- secrets remain external to Git;
- client-visible/browser/mobile values are public by definition;
- environment credentials/state are isolated;
- runtime database privilege is separated from migration/admin/replication/backup roles where material;
- GitHub Actions -> cloud/provider identity prefers OIDC/short-lived federation where supported;
- sensitive payloads/credentials are excluded from logs/traces by default.

Exact runtime secret-manager vendor depends on future compute/provider choice and is therefore deferred.

## Testing / CI decisions

DANTE uses risk-layered tests:

```text
unit / property-invariant
architecture dependency enforcement
real PostgreSQL integration
migration evolution/drift
provider contracts
OpenAPI/generated-client drift
web/mobile component/integration
system/E2E
security/supply chain
performance/recovery/PSV at applicable boundaries
```

Web baseline: Vitest + Testing Library + Playwright E2E.

Mobile baseline: Jest + React Native Testing Library + Maestro native E2E when activated. Expo development builds are the canonical production-grade mobile development path; Expo Go is not the production runtime baseline.

GitHub Actions is the primary repository CI/CD orchestrator. Normal PR jobs use least-privilege permissions, locked installs and no production deployment secrets.

Third-party actions are pinned to immutable SHAs where practical. Dependency review, CodeQL, Dependabot/update automation, container/IaC scans and build provenance are activated when corresponding real manifests/source/artifacts exist and their actual support/context is verified.

No required-main status check is invented before a real workflow emits a stable verified context whose failure genuinely should block merge.

Aggregate coverage is a signal, not semantic proof. Exact numeric coverage floors are deferred until real code gives a meaningful denominator; critical invariants require direct tests regardless of aggregate percentage.

## State/history/consistency direction

Implementation must preserve, where applicable:

- intended/planned vs accepted/current vs actual realization;
- Actual vs Observation/Outcome;
- canonical vs provider/external state;
- material state/history vs derived projection;
- candidate/unresolved vs established canonical meaning;
- correction/version/reconciliation vs silent overwrite;
- owner identity vs storage/provider/runtime identity;
- expected-state semantics for consequential writes;
- atomic multi-owner changes where required or truthful staged/partial state with reconciliation/compensation.

```text
NativeRef != ScopedRecordRef != MaterialStateRef != ExternalRef
ETag / MVCC token / provider revision != MaterialStateRef by identity
idempotency != semantic identity
absence / unknown != false
```

## Flexible/provider data and object storage

JSON/metadata may represent genuinely flexible, low-consequence, provider-specific or specialist detail; it must not hide unresolved kernel semantics.

Large file bytes remain behind the selected object-storage boundary; ContentArtifact identity is not identical to blob/path/URL/provider-object identity.

## Integration Hub

Five modes remain distinct:

```text
canonical import
sync / mirror
live federated read
retrieval / index projection
action / tool integration
```

```text
ExternalRef != NativeRef
provider revision != MaterialStateRef
provider state/effect != canonical DANTE state/effect automatically
provider/tool operation string != canonical governed effect
```

Callbacks/webhooks/polling/push are adapter mechanisms. MCP/A2A/future protocols remain adapters, not ontology/governance authority.

Provider SDKs live behind outbound adapters rather than becoming domain/application types by identity.

## AI / context / runtime

AI remains behind a replaceable/provider-neutral gateway and bounded Context Builder.

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

```text
AI memory != second canonical truth store
model output != accepted canonical effect
tool invocation != authorization
runtime Agent / Principal != Domain Actor automatically
```

Before promotion of materially consequential AI changes, DANTE requires versioned/reproducible evaluation appropriate to affected behavior.

```text
eval result != canonical DANTE truth
eval PASS != Authority
eval PASS != governed-effect authorization
```

## Governed operations/effects

Consequential operation meaning remains independent from route/UI/tool/AuthZ/workflow implementation.

```text
request accepted != effect completed
provider acknowledgement != canonical completion automatically
workflow completion != Actual automatically
technical cancellation != Domain cancellation automatically
```

Where material, preserve semantic target/effect, purpose/context, expected/material state, Principal/Actor/represented party, governance, autonomy/confirmation, idempotency/equivalence, correlation/causation, execution class, deadlines/cancellation semantics and independent canonical/provider/runtime/reconciliation outcomes.

## Security / AuthZ

Later implementation preserves:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
```

Consequential authorization/effect provenance must be reconstructible where required. Non-human Principals do not bypass semantic governance.

## Specialized-infrastructure decision

The accepted target deliberately does **not** add a dedicated graph/search/vector/event-broker zoo.

Not selected in the target include:

```text
TypeDB / XTDB / SurrealDB primary
Neo4j
Qdrant
OpenSearch
Redis / Valkey
Kafka / RabbitMQ / NATS
Debezium
Temporal
DBOS
Celery + broker
```

Engineering Foundation likewise does not add Kubernetes/microservices/build-system complexity without a concrete measured need. Any reintroduction/extraction requires an explicit decision based on changed requirements/evidence.

## Direct implementation-validation truth

```text
DATABASE DEPLOYMENT      NOT STARTED
FIXTURE/HARNESS           NOT STARTED
DIRECT HG PASS            0
LOW/BASE/HIGH            NOT RUN
RESTORE/MIGRATION         NOT RUN
FAILURE INJECTION         NOT RUN
POWERSYNC                 NOT RUN
RESTATE                   NOT RUN
OBJECT RECOVERY           NOT RUN
SOLVER                    NOT RUN
VERIFIED-RUN SCORE        NOT AVAILABLE
```

Applicable direct obligations remain in `docs/physical-model/recommendation/post-selection-validation-register-v1.md`.

## Repository safety

Effective `main` protections remain the integration policy: PR required, main deletion/non-fast-forward blocked, review-thread resolution required, no invented required checks before stable real contexts exist.

Engineering Foundation selecting GitHub Actions does not assert that workflows/check contexts already exist.

## Engineering Foundation boundary

The previously proposed standalone Development Profile is no longer the next separate operational phase.

Operational concerns are now handled by:

1. the durable Engineering Foundation contract for repository/environments/config/toolchain/testing/delivery; and
2. the actual capability/release implementation boundary that has the information needed to activate a selected Physical component.

This does not reopen or weaken the accepted Physical target.

## Explicit next boundary

```text
PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED / INTEGRATED

DIRECT IMPLEMENTATION VALIDATION
NOT STARTED / CARRIED FORWARD

ENGINEERING FOUNDATION v0
ACTIVE / UNMERGED / PENDING FINAL REVIEW + QA

THEN
production repository scaffold
→ backend bootstrap
→ PostgreSQL local profile + migration harness
→ concrete Logical-to-PostgreSQL schema
→ vertical implementation
```