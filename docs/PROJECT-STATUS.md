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

REPOSITORY IDENTITY GOVERNANCE
COMPLETE
MattiaRubino/lifeos → MattiaRubino/dante

PRODUCTION BACKEND SCAFFOLD
ACTIVE
CP1-01 DEPENDENCY/VERSION POLICY APPROVED
CP1-02 PYPROJECT/QUALITY TOOLING APPROVED
CP1-03 FASTAPI/SETTINGS/HEALTH CONTRACT APPROVED
CP1 IMPLEMENTATION NOT STARTED

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

- PowerSync Service 1.25.0 Open Edition;
- encrypted SQLite local state;
- PostgreSQL-backed PowerSync bucket storage;
- explicit client-safe sync projections.

Rules:

```text
SQLite local copy != canonical truth
PowerSync arrival order != conflict resolution
consequential offline mutation → DANTE backend revalidation → PostgreSQL
```

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

Production implementation remains in the current repository; no new repo is planned. Repository identity governance is complete and the current GitHub repository is `MattiaRubino/dante`; `MattiaRubino/lifeos` is historical identity only.

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

### Explicit frontend defer

Engineering Foundation v0 does **not** freeze Node/package-manager/Turborepo/web/mobile test/build/release details. Those return to the frontend workstream.

### Explicit cloud defer

Compute provider, IaC engine, registry and remote sizing are not selected until first remote environment.

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
VERIFIED-RUN SCORE       NOT AVAILABLE
```

Workstation Docker/WSL smoke tests are direct evidence of the developer environment only. They do not count as PostgreSQL/database/HG/PSV validation.

CP1 design approval is documentation/design evidence only. No CP1 implementation command has yet earned PASS.

## 8. Current repository branches/workstreams

The separate Phase-4 frontend/prototype work remains outside backend Engineering Foundation implementation authority.

Engineering Foundation v0 is closed. Repository rename is complete.

Production Backend Scaffold is the active bounded workstream:

```text
branch             feature/backend-scaffold
handoff            docs/workstreams/backend-scaffold.md
CP1 contract        docs/development/backend-cp1-contract.md
state              CP1-01/02/03 APPROVED / IMPLEMENTATION NOT STARTED
```

The CP1 contract is deliberately self-contained and records the complete variable registry, version ranges/rationale, `pyproject`/Ruff/mypy/pytest/coverage policy, FastAPI application-factory behavior, LOCAL `.env.local` loading, health/readiness semantics, standard commands and acceptance tests.

The verified workstation bootstrap is recorded in:

`docs/development/local-backend-workstation-bootstrap.md`

## 9. Exact next action

Do not repeat the already-closed CP1 decisions by default and do not jump to PostgreSQL or concrete schema implementation.

Resume from the active scaffold handoff + CP1 contract:

```text
STEP 1
Verify feature/backend-scaffold, remote/local HEAD and clean tree.

STEP 2
Re-check upstream package evidence only if version-sensitive facts materially changed since 2026-08-19.

STEP 3
Present a fresh exact CP1 implementation Git write gate covering the approved apps/backend file set only.

STEP 4
After explicit approval, materialize CP1:
Python package + pyproject/uv.lock + FastAPI factory + typed settings + health routes + real tests + backend README/.env example.

STEP 5
Generate the lockfile with uv; never hand-write it.

STEP 6
Run every direct CP1 acceptance command listed in `docs/development/backend-cp1-contract.md` on the real WSL/Linux workstation.

STEP 7
Run remote exact-delta/readback QA and record actual resolved versions/evidence.

STEP 8
Only after CP1 PASS, design/gate CP2 DANTE-owned LOCAL PostgreSQL 18.4 infrastructure.

STEP 9
Then CP3 persistence/migrations/real-PostgreSQL harness, CP4 CI enforcement, and CP5 scaffold closure.

STEP 10
Only after scaffold QA begin concrete Logical → PostgreSQL mapping/schema implementation.
```

The scaffold workstream quality bar is production-grade and future-team-ready, but it explicitly rejects placeholder structure and unnecessary complexity. Closed models/Foundation are not reopened unless concrete implementation evidence reveals an actual contradiction.
