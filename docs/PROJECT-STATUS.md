# DANTE — Project Status

- Status: **CURRENT TRUTH**
- Product: **DANTE**

## 1. Executive state

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL
CLOSED
integrated via protected-main workflow
Whole-Domain PASS WITH HARDENING
POST-WRITE QA PASS

LOGICAL MODEL
CLOSED
Whole-Logical PASS WITH HARDENING
REMOTE QA PASS
WL-H01..WL-H12 ACTIVE

PRE-PHYSICAL COHERENCE
DEFINITIVE CLOSED / FINAL QA PASS

PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED
PM-11 COMPLETE
PM-12 COMPLETE
PM-13 QA PASS
PM-14 CLOSURE COMPLETE

ENGINEERING FOUNDATION v0
CLOSED / ACCEPTED / FINAL REVIEW PASS

FRONTEND ENGINEERING FOUNDATION
ACTIVE on feature/frontend-foundation
PASSO 1 TECHNOLOGY SELECTION DESIGN COMPLETE
PASSO 2 STRUCTURE / OWNERSHIP NOT STARTED
PRODUCTION FRONTEND CODE NOT STARTED
DIRECT FRONTEND VALIDATION NOT STARTED

PRODUCTION BACKEND SCAFFOLD
NOT STARTED

CONCRETE LOGICAL → POSTGRESQL IMPLEMENTATION
NOT STARTED

DIRECT SELECTED-STACK IMPLEMENTATION VALIDATION
NOT STARTED
DIRECT HG PASS 0
VERIFIED-RUN SCORE NOT AVAILABLE
```

## 2. Product/North Star

DANTE is a personal operating system designed to help people understand, organize and improve their real life by turning intentions, needs and possibilities into outcomes they can realistically pursue.

Compass: **Understand life. Shape what comes next.**

Important product invariants include:

- life central, not task/calendar centric;
- planned vs actual preserved;
- user authority and authorship;
- historical/material truth;
- privacy and provenance;
- honest uncertainty;
- progressive complexity;
- personal-first, not personal-only;
- AI is not the product authority;
- possibility != action/decision/preference;
- Effort != Execution != Outcome != Goal Progress.

## 3. Core identity/governance invariants

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
HTTP/UI/tool/AuthZ string != canonical governed effect
```

WL-H01..WL-H12 remain active and constrain implementation.

## 4. Logical model

57/57 owners are classified.

Native identity owners include Person, Living Referent, Asset, Place, Content Artifact, Collective, Possibility, Goal, Plan, Activity, Event, Routine, Occurrence, Session and Observation.

Reference families:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

No implementation scope may mechanically translate 57 Logical owners into 57 services/modules/tables by assumption.

## 5. Accepted Physical target

### Canonical persistence

```text
PostgreSQL 18.4
sole canonical persistence + material history authority
```

Selected PostgreSQL capabilities:

- PostGIS 3.6.4;
- pgvector 0.8.6;
- native full-text search;
- pg_trgm;
- unaccent;
- pg_stat_statements;
- PgBouncer 1.25.2.

### Offline/sync

- PowerSync Service 1.25.0 Open Edition target from the accepted Physical Model;
- encrypted SQLite local state;
- PostgreSQL-backed PowerSync bucket storage;
- explicit client-safe sync projections.

Frontend-engineering implementation must preserve:

```text
SQLite local copy != canonical truth
PowerSync arrival order != conflict resolution
offline capability = operation-specific
consequential offline mutation → DANTE backend revalidation → PostgreSQL
```

PowerSync JavaScript client packaging/version is selected separately in the active frontend workstream and does not rewrite the accepted Physical ownership semantics.

### Async/durable

Class A:

- PostgreSQL transactional outbox + bounded worker.

Class B:

- Restate selected;
- Restate Python SDK 1.0.3 / Server 1.7.2 target posture;
- **dormant / not active** until first real Class-B durable workflow;
- self-hosted vs Cloud EU deferred until activation.

### Objects

- Cloudflare R2 Standard;
- EU jurisdiction;
- private;
- raw bytes only;
- PostgreSQL owns ContentArtifact identity/metadata/provenance/visibility/retention/hash/locator semantics.

### Recovery

- pgBackRest 2.59.0;
- AWS S3 Standard `eu-south-1`;
- Versioning + accepted Object Lock GOVERNANCE posture;
- recovery copies noncanonical;
- anti-resurrection required;
- **dormant** until recovery/production boundary or real rehearsal.

### Solver

- OR-Tools 9.15 CP-SAT candidate mechanism;
- UNKNOWN != INFEASIBLE.

### Observability

- OpenTelemetry;
- Grafana Alloy 1.18.0;
- Grafana Cloud EU;
- privacy-minimized operational telemetry.

## 6. Engineering Foundation v0 — closed

### Repository

```text
one product monorepo
apps/backend
apps/web
apps/mobile
```

Production implementation remains in the current repository; no new repo is planned.

### Backend architecture

- capability-first modular monolith;
- Domain/application/adapters separated;
- FastAPI is an inbound adapter/process host;
- no universal generic `Repository[T]`/BaseService/service locator/global DB session;
- cross-module transactions allowed where accepted semantics require atomicity.

### Backend toolchain

```text
Python             3.14.x
initial pin         3.14.7
uv
Ruff
mypy strict
pytest
Hypothesis
SQLAlchemy 2.0 stable line
psycopg 3
Alembic
```

### Developer environment

- Linux canonical server semantics;
- Windows 11 supported through WSL2/Linux;
- repository/workflow kept in WSL filesystem for backend development;
- PyCharm with WSL interpreter supported;
- backend inner-loop process runs directly in WSL;
- Docker Compose runs stateful LOCAL infrastructure;
- future backend deployable packaged as immutable OCI image.

### LOCAL PostgreSQL

First LOCAL DB uses real PostgreSQL 18.4 and has the full selected extension envelope installed/enabled immediately, including pg_stat_statements preload configuration.

DANTE owns a reproducible LOCAL PostgreSQL build/configuration.

### Persistence/migration

- async DB I/O at technical boundaries; Domain/application sync/pure by default;
- one AsyncSession per concurrent use-case/task scope;
- application boundary owns transaction;
- Alembic migration authority;
- autogenerate candidate only;
- applied migrations immutable;
- schema drift checked;
- risk classification + online/staged PostgreSQL techniques where appropriate;
- expand → migrate → contract;
- large backfills resumable/idempotent/bounded;
- separate owner/migrator/runtime/replication/backup privilege classes;
- `pg_dump`/`pg_restore` logical-copy path;
- pgBackRest/WAL/PITR recovery path at accepted activation boundary;
- raw PROD → DEV forbidden by default; production-derived lower-environment clones require sanitization/minimization.

### Config/secrets

- pydantic-settings typed/fail-fast immutable bootstrap configuration;
- LOCAL safe `.env.example` + ignored `.env.local`;
- remote hierarchy: minimize secrets → workload identity → provider secret manager → least privilege → rotation/revocation/audit;
- GitHub OIDC preferred for future cloud deployment;
- independent DEV/UAT/PROD and runtime/migrator credentials.

### Testing/CI

- real PostgreSQL integration, never SQLite as PostgreSQL proof;
- unit/application/property/state-machine/architecture/migration/concurrency/provider/API/privacy test layers;
- PR/DEV/nightly/UAT cost tiers;
- coverage tracked without arbitrary pre-code percentage;
- GitHub Actions primary CI/CD;
- protected-main real-check-before-required-check rule;
- least-privilege workflow permissions;
- immutable SHA-pinned Actions in protected workflows;
- dependency review/CodeQL/secret protection when artifacts/source/capability exist;
- GitHub-hosted runner initially;
- future OCI build-once/promote, attestation and SBOM at release boundary.

### Frontend workstream activation

The dedicated frontend workstream is now active on `feature/frontend-foundation`.

Passo 1 has selected the frontend technology baseline in design. The durable branch-local authorities are:

- `docs/architecture/frontend-engineering-foundation.md`;
- `docs/decisions/ADR-008-frontend-engineering-stack.md`;
- `docs/workstreams/frontend-foundation.md`.

Until protected-main integration, these are newer unmerged workstream truth rather than integrated `main` authority.

### Explicit cloud defer

Backend compute provider, IaC engine, registry and remote sizing remain unselected until first remote backend infrastructure. The frontend workstream may select bounded Web-delivery/mobile-build services without silently selecting the backend compute/IaC platform.

## 7. Direct-validation truth

Never claim these have passed:

```text
DATABASE DEPLOYMENT      NOT STARTED
FIXTURE/HARNESS          NOT STARTED
DIRECT HG-01..HG-12      NOT RUN
DIRECT HG PASS           0
LOW/BASE/HIGH            NOT RUN
RESTORE REHEARSAL        NOT RUN
MIGRATION REHEARSAL      NOT RUN
FAILURE INJECTION        NOT RUN
POWERSYNC DIRECT TEST    NOT RUN
RESTATE DIRECT TEST      NOT RUN
OBJECT RECOVERY TEST     NOT RUN
SOLVER DIRECT TEST       NOT RUN
FRONTEND DIRECT TEST     NOT RUN
VERIFIED-RUN SCORE       NOT AVAILABLE
```

Frontend Passo-1 selections carry explicit direct-validation obligations into later materialization; they are not blanket direct-PASS claims.

## 8. Current repository branches/workstreams

- `feature/frontend-foundation` — **ACTIVE**, documentation/architecture work only at this checkpoint; Passo 1 design complete, Passo 2 next.
- separate prototype/UX workstreams remain outside production frontend engineering authority.
- Engineering Foundation v0 is closed.
- no production frontend or backend scaffold has yet been created by this workstream.

## 9. Exact next action

### Active frontend workstream

```text
PASSO 2
Define the definitive frontend application/package structure,
ownership and dependency direction as one coherent architecture pass.

THEN
whole-foundation review / closure / PR / protected-main integration.

ONLY AFTER FOUNDATION INTEGRATION
materialize the production frontend scaffold and run direct validations.
```

### Backend implementation remains separate

The production backend scaffold remains **NOT STARTED** and requires its own bounded implementation gate. Frontend Foundation work does not authorize backend schema/business implementation.

Do not reopen closed Product/Domain/Logical/Physical/Engineering decisions unless a concrete implementation contradiction supplies evidence for an explicit reopen.
