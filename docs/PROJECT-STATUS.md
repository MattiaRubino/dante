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
CP1 PYTHON/BACKEND PROCESS + TYPED CONFIG CLOSED / DIRECT QA PASS
CP2 REPRODUCIBLE LOCAL POSTGRESQL CLOSED / DIRECT QA PASS
CP3 PERSISTENCE/MIGRATIONS/REAL-POSTGRESQL HARNESS CLOSED / DIRECT QA PASS
CP4 QUALITY/CI ENFORCEMENT NEXT / NOT STARTED
CP5 FULL SCAFFOLD QA/CLOSURE NOT STARTED

CONCRETE LOGICAL → POSTGRESQL IMPLEMENTATION
NOT STARTED

DIRECT SELECTED-STACK IMPLEMENTATION VALIDATION
CP1 DIRECT PASS RECORDED
CP2 LOCAL POSTGRESQL DIRECT PASS RECORDED
CP3 DIRECT PASS RECORDED
CP3 POSTGRESQL ACCEPTANCE 18/18 PASS
CP3 FULL BACKEND PYTEST 50/50 PASS
DIRECT HG-01..HG-12 NOT RUN
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
Hypothesis when meaningful
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

DANTE owns a reproducible LOCAL PostgreSQL build/configuration. CP2 directly proved the selected image, capabilities, persistence/reset semantics and Windows host connectivity on the canonical workstation.

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

## 7. Backend CP1 — direct implementation truth

CP1 is closed on `feature/backend-scaffold` with implementation/lock closure HEAD:

```text
02d113d772cdb247faebb3cef4d857d125266da3
```

Materialized runtime/tooling:

```text
Python              3.14.7
fastapi             0.141.1
pydantic            2.13.4
pydantic-settings   2.15.0
uvicorn             0.52.4
httpx2               2.12.0
mypy                 2.3.1
pytest               9.1.1
pytest-cov           7.1.0
ruff                 0.16.3
```

Direct WSL/Linux evidence earned on 2026-08-20:

```text
uv lock --check                         PASS
uv tree --locked --depth 1              PASS
uv sync --locked                         PASS
Python project interpreter 3.14.7       PASS
installed dante src-layout import        PASS
ruff format --check                      PASS
ruff check                               PASS
mypy strict                              PASS
pytest                                   PASS — 25/25
CP1 statement coverage                   100.00%
CP1 branch coverage                      100.00%
uv build                                 PASS
real Uvicorn factory startup             PASS
GET /health/live over real HTTP          PASS — 200 / {"status":"ok"}
GET /health/ready over real HTTP         PASS — 200 / {"status":"ready"}
remote uv.lock readback                  PASS
```

Coverage 100% is evidence for the very small CP1 surface, **not** a permanent arbitrary threshold.

Important implementation findings resolved without weakening quality policy:

- Pydantic mypy plugin enabled after real strict-mypy evidence;
- narrow runtime immutability-test suppression only;
- Starlette TestClient dependency corrected from `httpx` to `httpx2`;
- warnings-as-errors preserved;
- `.coverage` ignored as generated local state.

## 8. Backend CP2 — direct LOCAL PostgreSQL truth

CP2 is closed on `feature/backend-scaffold`. Durable authority and full acceptance evidence:

`docs/development/backend-cp2-postgres-contract.md`

Direct evidence earned on 2026-08-20:

```text
Compose model                               PASS
immutable PostgreSQL base digest            PASS
clean/no-cache DANTE image build            PASS
PostgreSQL                                  18.4 PASS
PostGIS package/extension                   3.6.4 PASS
pgvector package/extension                  0.8.6 PASS
pg_trgm                                     PASS
unaccent                                    PASS
pg_stat_statements preload                  PASS
compute_query_id=on                         PASS
pg_stat_statements real query collection    PASS
fresh initdb + 010-extensions.sql           PASS
named-volume persistence                    PASS
down --volumes destructive reset            PASS
fresh post-reset reinitialization            PASS
Windows DBeaver host connection             PASS
```

The Windows GUI query directly returned:

```text
current_database = dante
current_user     = postgres
PostgreSQL       = 18.4 line
```

The first no-cache build exposed a missing `ca-certificates` trust-store prerequisite in the pinned PostgreSQL base image. The accepted repair preserved HTTPS and PGDG signed-repository verification; the repaired clean build passed directly.

CP2 does not establish application SQLAlchemy/psycopg connectivity, Alembic migration behavior, privilege separation, concrete schema mapping, restore/PITR or HG/PSV PASS.

## 9. Backend CP3 — direct implementation truth — CLOSED

CP3 design CP3-01..CP3-06, implementation and direct QA are closed under:

`docs/development/backend-cp3-persistence-contract.md`

Implementation/direct-QA HEAD:

```text
35cf6440bc121a38342f6bbee72e210435a788a4
```

Materialized technical surface includes:

```text
SQLAlchemy async runtime
psycopg 3
Alembic environment + technical baseline
nested typed database settings
FastAPI database lifespan
DB-aware readiness
schema dante metadata authority
owner/migrator/runtime provisioning
real PostgreSQL acceptance harness
transaction/migration/privilege/runtime tests
```

Exact locked persistence/tooling resolution:

```text
SQLAlchemy       2.0.52
psycopg          3.3.4
Alembic          1.19.1
pytest-asyncio   1.4.0
```

The PostgreSQL acceptance harness uses one disposable cluster created from the already certified `dante-postgres-local:18.4` image per pytest PostgreSQL session. This keeps the ordinary LOCAL `dante` database and cluster-global application-role credentials untouched while exercising the exact CP2 image/envelope.

The exact cluster version check uses `SHOW server_version_num = 180004`. Real outage/recovery acceptance uses stop/start of that same disposable cluster so live connections close, database state survives the outage and readiness recovery is proved without restarting the backend.

Direct WSL/Docker evidence earned on 2026-08-20:

```text
uv lock --check                         PASS
uv tree --locked --depth 1              PASS
uv sync --locked                         PASS
ruff format --check .                    PASS — 23 files already formatted
ruff check .                             PASS
mypy                                    PASS — 20 source files
pytest -m "not postgres"                PASS — 32/32
pytest -m postgres                       PASS — 18/18 in 15.61s
full pytest                              PASS — 50/50 in 24.72s
full-run coverage                        97.42% evidence only; not threshold
uv build                                 PASS
source distribution                      PASS
wheel                                    PASS
Alembic fresh DB/head/round-trip/drift    PASS
runtime/migrator/owner privilege matrix   PASS
runtime identity/search_path              PASS
stale pooled-connection recovery          PASS
DB outage live 200 / ready 503            PASS
DB recovery ready 200 without app restart PASS
commit/rollback/flush/SAVEPOINT            PASS
```

Remote exact-scope QA from original CP3 PRE-SCOPE to executable QA HEAD:

```text
PRE-SCOPE       a09936d168de48909d948425387b168d016911e8
QA HEAD         35cf6440bc121a38342f6bbee72e210435a788a4
ahead_by        45
behind_by       0
changed paths   27
expected paths  27
unexpected      0
deleted         0
```

The 97.42% coverage figure is evidence for the full CP3 closure run, not a permanent arbitrary project threshold.

Evidence-driven hardening finding retained after closure: `docker pause` demonstrated a stronger frozen/blackholed-peer condition where TCP can stay open while PostgreSQL cannot answer and driver cancellation/cleanup can exceed the Python-level readiness timeout. CP3 does not claim a bounded wall-clock result for that stronger scenario.

CP3 final state:

```text
CLOSED / DIRECT QA PASS
```

## 10. Direct-validation truth beyond CP3

CP3 directly established the application persistence boundary below. Do not extrapolate these PASS results into blanket Physical validation:

```text
APPLICATION DB CONNECTION/HARNESS    DIRECT QA PASS
ALEMBIC MIGRATION HARNESS            DIRECT QA PASS
RUNTIME/MIGRATOR PRIVILEGE SPLIT     DIRECT QA PASS
CP3 TRANSACTION ACCEPTANCE           DIRECT QA PASS
CP3 READINESS FAILURE/RECOVERY        DIRECT QA PASS for real stop/start outage
FROZEN/BLACKHOLED-PEER READINESS     HARDENING / NOT CLAIMED PASS
DIRECT HG-01..HG-12                  NOT RUN
DIRECT HG PASS                       0
LOW/BASE/HIGH                        NOT RUN
RESTORE REHEARSAL                    NOT RUN
MIGRATION REHEARSAL                  NOT RUN beyond CP3 technical migration acceptance
FAILURE INJECTION                    NOT RUN beyond bounded CP3 acceptance
POWERSYNC DIRECT TEST                NOT RUN
RESTATE DIRECT TEST                  NOT RUN
OBJECT RECOVERY TEST                 NOT RUN
SOLVER DIRECT TEST                   NOT RUN
VERIFIED-RUN SCORE                   NOT AVAILABLE
```

Workstation/CP1/CP2/CP3 evidence does not count as a blanket Physical HG/PSV pass.

## 11. Current repository branches/workstreams

The separate Phase-4 frontend/prototype work remains outside backend Engineering Foundation implementation authority.

Engineering Foundation v0 is closed. Repository rename is complete.

Production Backend Scaffold is the active bounded workstream:

```text
branch              feature/backend-scaffold
handoff             docs/workstreams/backend-scaffold.md
CP1 contract         docs/development/backend-cp1-contract.md
CP2 contract         docs/development/backend-cp2-postgres-contract.md
CP3 contract         docs/development/backend-cp3-persistence-contract.md
state               CP1 CLOSED / CP2 CLOSED / CP3 CLOSED / DIRECT QA PASS / CP4 NEXT
```

The verified workstation/bootstrap state is recorded in:

`docs/development/local-backend-workstation-bootstrap.md`

## 12. Exact next action

Do not redesign CP1, CP2 or CP3 and do not jump to concrete Logical schema implementation.

Resume from the active scaffold handoff:

```text
STEP 1
Verify feature/backend-scaffold, remote/local HEAD and clean tree.

STEP 2
Treat CP1, CP2 and CP3 as CLOSED / DIRECT QA PASS.

STEP 3
Begin CP4 read-only inspection of current repository quality checks, GitHub Actions state and protected-main settings.

STEP 4
Select only CI/checks backed by commands already directly proven stable.

STEP 5
Define CP4 quality/architecture/CI enforcement and its direct acceptance matrix.

STEP 6
Open a new exact Git write gate before any CP4 mutation.

STEP 7
Run the emitted CI contexts remotely before considering any required-check protection.

STEP 8
Deliberately verify a stable required context blocks a failing merge before requiring it on protected main.

STEP 9
Resolve only evidence-backed CP4 defects under narrow correction gates.

STEP 10
After CP4 direct QA, execute CP5 full scaffold QA/closure.

STEP 11
Only after scaffold QA begin concrete Logical → PostgreSQL mapping/schema implementation.
```

The scaffold workstream quality bar is production-grade and future-team-ready, but it explicitly rejects placeholder structure and unnecessary complexity. Closed models/Foundation/CP1/CP2/CP3 are not reopened unless concrete implementation evidence reveals an actual contradiction.