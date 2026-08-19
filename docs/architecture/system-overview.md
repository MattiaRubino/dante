# System Overview

- Status: **Current architecture overview — Physical target accepted; Engineering Foundation v0 active**
- Last updated: 2026-08-19
- Current product/app name: **DANTE** (`LifeOS` is the previous working/project name retained only where historical/technical continuity requires it)

## Stage boundary

```text
Product / North Star
CURRENT

Core Domain Model / Domain Atlas
CLOSED

Logical Model
CLOSED

Phase 5 requirements
CURRENT

Phase 6 AI/context/runtime/integration boundaries
CURRENT

Phase 7 durable-execution contract
CURRENT / PHYSICAL MECHANISM RESOLVED

Phase 8 governed-operation/effect contract
CURRENT

Phase 9 search/observability/calendar/solver contract
CURRENT / PHYSICAL MECHANISMS RESOLVED WHERE SELECTED

Phase 10 benchmark method
CURRENT METHOD / HISTORICAL DECISION-EVIDENCE AUTHORITY

Repository engineering safety
QA PASS at verified scope

Pre-Physical Coherence
DEFINITIVE CLOSED / FINAL QA PASS
INTEGRATED / POST-MERGE VERIFIED

Physical Model target
CLOSED / SELECTED / ACCEPTED
INTEGRATED INTO MAIN VIA PR #15
selected canonical primary PostgreSQL 18.4

Direct selected-stack implementation validation
NOT STARTED / DIRECT HG PASS 0

Engineering Foundation v0
ACTIVE / UNMERGED on chore/engineering-foundation-v0

Backend / production application implementation
NOT STARTED
```

Domain semantics are defined by the CLOSED Domain Atlas; Logical representation/downstream hardenings by the CLOSED Whole Logical Model. Engineering Foundation introduces no new semantic owner.

## Product/runtime system architecture

```text
Web client (Next.js) -----------------------\
                                             \
Mobile client (Expo / React Native) ----------> Versioned DANTE backend boundary
                                                  |-- authentication context / AuthZ enforcement
                                                  |-- governed operation/effect boundary
                                                  |-- planning / scheduling / reasoning
                                                  |-- deterministic solver boundary
                                                  |-- provenance / history / reconciliation
                                                  |-- projection / disclosure
                                                  |-- search / retrieval
                                                  |-- Integration Hub / provider adapters
                                                  |-- AI Gateway + Context Builder
                                                  |-- AI evaluation / promotion boundary
                                                  |-- bounded async + durable execution
                                                  |-- observability / operational controls
                                                            |
                                                            v
                                                   PostgreSQL 18.4
                                                   canonical persistence
                                                      /    |    \
                                                     /     |     \
                                                 PostGIS  pgvector  FTS
                                                    |
                 -----------------------------------+-----------------------------------
                 |                                  |                                  |
          PowerSync / SQLite                 Restate runtime                    Cloudflare R2
          local/sync projection              Class-B execution                 raw object bytes
                 |                                  |                                  |
                 +-------------------------- backend authority -------------------------+
                                                    |
                                                pgBackRest
                                                    |
                                      AWS S3 recovery repositories

Operational telemetry:
OpenTelemetry -> Grafana Alloy -> Grafana Cloud EU

Constraint solving:
OR-Tools CP-SAT -> candidate output -> governed acceptance path
```

This diagram is the accepted target topology, not a claim that every component is already deployed.

External providers, assistants, caches, indexes, projections, solver candidates, workflow/runtime state and device-local stores are not alternate canonical DANTE truth merely because they contain data.

## Engineering/repository topology

Engineering Foundation defines the implementation container around that system:

```text
DANTE polyglot monorepo
│
├── apps/api
│   Python / FastAPI / Pydantic
│   capability-first modular monolith
│   SQLAlchemy 2.0 / psycopg 3 / Alembic
│
├── apps/web
│   Next.js / React / TypeScript
│
├── apps/mobile
│   Expo / React Native / TypeScript
│
├── packages
│   generated API client + precise shared TS artifacts only
│
├── infra
│   local stateful topology + future reproducible remote infrastructure definitions
│
├── tooling
│   repository engineering/codegen only
│
├── tests/system
│   cross-application black-box tests only
│
├── docs
│   durable project/architecture/engineering authority
│
└── prototypes
    non-production / never an import dependency of production apps
```

The production tree is a target contract. Engineering Foundation itself creates documentation only; production code/scaffold has not started.

## Backend internal shape

The backend starts as one **capability-first modular monolith**.

Conceptual structure:

```text
dante/
├── bootstrap/      composition root / process lifecycle
├── kernel/         small stable cross-capability primitives only
├── platform/       bounded technical services/config/database/observability
└── modules/
    └── <capability>/
        ├── domain/
        ├── application/
        ├── ports/
        ├── adapters/
        └── public.py
```

Rules:

- capability cohesion, not one module per table/Logical owner/route;
- domain/application logic does not depend by identity on FastAPI/SQLAlchemy/provider SDKs;
- cross-module access uses explicit public/application interfaces rather than private persistence imports;
- the modular monolith may still use one PostgreSQL transaction across modules where accepted multi-owner semantics require true atomicity;
- no generic `Repository[T]`/`BaseService`/service-locator kernel is introduced as a universal semantic abstraction;
- future service extraction requires measured operational/ownership/security/scaling evidence.

## Canonical ownership

```text
CANONICAL DANTE TRUTH
PostgreSQL 18.4

MATERIAL HISTORY
PostgreSQL 18.4

RAW OBJECT BYTES
Cloudflare R2

LOCAL/OFFLINE COPY
encrypted SQLite / noncanonical

SYNC PROJECTION
PowerSync / noncanonical

DURABLE RUNTIME STATE
Restate / noncanonical

BACKUPS
S3 / recovery only

SOLVER OUTPUT
OR-Tools / candidate only

TELEMETRY
OTel/Grafana / operational only
```

## Client responsibilities

Clients own presentation, navigation, local interaction state, secure session handling, platform capabilities and collection of user intent/confirmation where required.

Multi-device/offline behavior obeys operation-specific freshness, expected-state, conflict, governance and sensitive-data requirements. Clients do not own canonical persistence or critical authorization/Domain invariants.

UI actions may request governed operations; UI labels/buttons do not define semantic operation identity.

Web/mobile consume a generated/versioned backend transport client where the OpenAPI contract can represent it. Generated transport types are not the Domain Model.

Web/server components and mobile clients never receive direct PostgreSQL credentials or bypass the governed backend to mutate canonical persistence.

## Backend boundary responsibilities

The future backend enforces accepted semantics through technical services, including:

- semantic target/operation validation;
- governed operation/effect admission + multi-axis result semantics;
- authorization enforcement without collapsing Principal, Actor, Authority, Consent or Visibility;
- expected-state/conflict handling;
- autonomy/preview/confirmation according to consequence/governance;
- provenance/material history/correction/reconciliation;
- truthful multi-owner consistency or explicit staged/partial outcomes with reconciliation/compensation;
- provider-state vs canonical-state separation;
- selective projection/disclosure;
- scheduling/replanning and deterministic calculation/constraint services;
- solver candidate generation rather than direct canonical writes;
- AI context construction/provider-neutral routing;
- versioned/reproducible evaluation before promotion of materially consequential AI behavior changes;
- provider/integration orchestration;
- bounded background work vs durable long-running coordination by execution class;
- search/retrieval separated from canonical meaning;
- privacy-safe observability and operational controls.

Concrete database mappings/routes/AuthN/AuthZ implementation remain future implementation work, not Engineering Foundation payload.

## Governed operation/effect responsibility

Where material, consequential operations preserve:

```text
contract/version
semantic target/facet
requested effect
input/candidate
purpose/context
material/expected state
derived/live basis + freshness
Principal / actual Actor / represented party
governance basis
autonomy / preview / confirmation
idempotency/equivalence
correlation/causation
execution class
deadline/expiry/technical cancellation
canonical result
provider/external result
runtime result
conflict/partial/reconciliation/provenance
```

```text
request accepted != effect completed
provider acknowledgement != canonical completion automatically
workflow completion != Actual automatically
runtime cancellation != Domain cancellation automatically
```

## Persistence/transaction responsibility

Engineering Foundation fixes these implementation rules before concrete schema work:

- SQLAlchemy 2.0 stable + psycopg 3 as backend PostgreSQL toolkit;
- Alembic owns durable schema migration history;
- real PostgreSQL integration tests; SQLite is not a backend substitute;
- application startup does not manage deployed schema through `create_all()`;
- application replicas do not race to auto-run migrations on boot;
- migrations are controlled/reviewed release operations;
- Alembic autogenerate output is a candidate requiring human/technical review;
- session/transaction scope belongs to an application operation/job/request and is not global;
- `AsyncSession` is not shared across concurrent tasks;
- transaction scope follows semantic atomicity, not ORM convenience;
- risky evolution uses expand/migrate/contract where old/new application or mobile versions overlap.

Concrete tables, columns, constraints and migration revisions remain future implementation.

## Durable execution responsibility

```text
BOUNDED ASYNC
PostgreSQL transactional outbox + bounded worker

DEDICATED DURABLE CLASS-B
Restate runtime — SELECTED
```

Restate disposition:

```text
INITIAL DEV
DORMANT / NOT ACTIVE

ACTIVATE
first real Class-B durable-workflow need

THEN CHOOSE DEPLOYMENT
self-hosted FIRST-CLASS
Cloud EU ALLOWED MANAGED OPTION
global default NONE
```

The previous generic “deployment profile chooses now” formulation is superseded by the fixed dormant trigger. Current Python use must not assume TypeScript-only client-side journal encryption; journal minimization remains mandatory when activated.

No runtime creates exactly-once external reality. Runtime/workflow IDs remain technical and do not become Domain/material-state identity.

## Offline / multi-device responsibility

```text
PostgreSQL canonical
→ approved PowerSync projection
→ encrypted SQLite local copy
→ offline mutation
→ DANTE backend expected-state/governance/AuthZ revalidation
→ PostgreSQL canonical commit if valid
```

Local arrival order is not semantic conflict resolution. Universal consequential LWW is rejected. Visibility/delete/redaction changes must propagate to affected sync/local copies.

PowerSync/SQLite implementation activates when the real mobile/offline vertical slice exists; selection is not reopened.

## Object responsibility

```text
ContentArtifact identity/metadata/authority
PostgreSQL

raw object bytes
Cloudflare R2 Standard / EU / private
```

R2 is not a semantic database. Public permanent object URLs/buckets are not the default. R2 implementation activates when real ContentArtifact byte handling exists.

## Recovery responsibility

```text
PostgreSQL backup
pgBackRest 2.59.0 -> AWS S3 Standard eu-south-1

R2 object backup
-> separate S3 repository
```

Target uses Versioning + Object Lock GOVERNANCE with finite policy-bound retention. Recovery copies are noncanonical and restore must preserve anti-resurrection/deletion semantics.

Initial DEV posture is already fixed:

```text
pgBackRest + AWS S3
DORMANT / NOT ACTIVE
ACTIVATE = recovery/production boundary OR real recovery rehearsal
```

## Canonical-state responsibility

Physical persistence preserves owner-specific identity/lifecycle boundaries, discriminated reference families, planned/current/actual/observed/derived distinctions, relationship/governance semantics, provider/canonical separation, material history/correction/reconciliation/retention integrity, bounded flexible/provider metadata and unresolved/candidate meaning where not established.

```text
Person != Account != Principal != Actor
provider state != canonical state
derived projection != canonical truth
absence / unknown != false
AI / solver inference != accepted canonical effect
```

All `WL-H01..WL-H12` remain mandatory downstream.

## Integration responsibility

Five Integration Hub modes remain distinct:

1. canonical import;
2. sync/mirror;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

`ExternalRef != NativeRef`; provider revision != `MaterialStateRef`; provider acknowledgement/result != canonical completion automatically. MCP/A2A/future protocols remain adapters.

Provider SDKs live at outbound adapters rather than inside domain/application semantics by identity.

## AI / Context Builder responsibility

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

AI output/tool invocation never becomes canonical truth/effect merely because a model/runtime produced it. DANTE does not create a second generic AI-memory source of truth.

Material consequential AI changes require versioned/reproducible evaluation before promotion.

```text
eval result != canonical DANTE truth
eval PASS != Authority / governed-effect authorization
```

## Search / calendar / solver / observability responsibility

- Search: PostgreSQL native FTS + `pg_trgm` + `unaccent`; pgvector for bounded vector retrieval; search/index state remains derived and disclosure-aware.
- Graph traversal: explicit PostgreSQL mappings + recursive SQL; no dedicated graph database in the accepted target.
- Calendar: standards/providers are adapter pressure; recurrence/overrides/DST/floating/all-day/provider-resync semantics remain DANTE-owned.
- Solver: OR-Tools 9.15 CP-SAT selected; `UNKNOWN != INFEASIBLE`; output crosses governed acceptance before canonical change.
- Observability: OpenTelemetry + Grafana Alloy + Grafana Cloud EU target; telemetry identifiers do not replace NativeRef/MaterialStateRef/Provenance/audit.

## Development/delivery environment model

Engineering Foundation defines:

```text
LOCAL
individual disposable development context
Linux semantics canonical for backend; Windows via WSL2/Linux
Docker Compose for activated stateful dependencies

DEV
shared integration environment for accepted main artifacts and synthetic data

UAT
production-like exact release-candidate verification/migration rehearsal

PROD
real released service/data
```

Optional PR previews are ephemeral and noncanonical. No environment is represented by a permanent Git branch.

GitHub Actions is the primary CI/CD orchestration baseline; GitHub Environments become privileged `dev`/`uat`/`prod` deployment boundaries once real workflows exist. Exact compute hosting/IaC engine remain deferred until remote infrastructure implementation.

Server/web artifacts use exact source/build/digest identity and build-once promotion where platform permits. Mobile is an explicit signed/environment-build exception but remains reproducible/traceable to reviewed source, lockfiles and build profile.

## Configuration/security engineering

- backend config is typed/validated via `pydantic-settings` at process bootstrap;
- secrets never live in Git or browser/mobile bundles;
- client-visible configuration is public by definition;
- DEV/UAT/PROD use isolated credentials/state where provider capabilities permit;
- normal runtime DB privilege is separated from migration/admin/replication/backup privileges where implementation requires;
- GitHub-to-provider OIDC/short-lived identity is preferred where supported;
- logs/traces exclude sensitive payloads/credentials by default.

## Testing/CI architecture

Engineering Foundation establishes risk-layered validation:

```text
unit / property-invariant
architecture dependency tests
real PostgreSQL integration
migration evolution/drift
provider/adapter contracts
OpenAPI/generated-client drift
web/mobile component tests
system/E2E
security/supply chain
performance/recovery/PSV at applicable boundaries
```

Aggregate coverage is a signal, not a substitute for invariant/conflict/migration/recovery/non-interference tests. Exact numeric coverage floors are deferred until real code creates a meaningful denominator.

No required-main CI status is invented in documentation; a check becomes required only after its real stable emitted context is verified and its failure genuinely should block merge.

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

Applicable obligations remain in `docs/physical-model/recommendation/post-selection-validation-register-v1.md`.

## Repository engineering safety

Effective `main` protections remain the integration mechanism. Future work continues on bounded branches with exact gates and no direct-main bypass.

Engineering Foundation defining workflow classes does not prove that those GitHub Actions exist or make them required-main checks.

## Current next boundary

```text
ENGINEERING FOUNDATION v0
ACTIVE / UNMERGED
complete current-doc alignment
→ exact remote QA
→ user acceptance
→ protected PR integration

THEN
production repository scaffold
→ backend bootstrap
→ PostgreSQL local profile + migration harness
→ concrete Logical-to-PostgreSQL schema
→ vertical implementation

DIRECT PSV
NOT RUN / carried forward
```
