# DANTE Backend

Production backend application for DANTE.

CP1 established the Python/process/configuration foundation. CP2 established the reproducible LOCAL PostgreSQL 18.4 image/envelope and direct phase-time evidence. CP3 activated application persistence, Alembic authority, PostgreSQL role separation and the real PostgreSQL acceptance harness. CP4 established calibrated CI and protected-main enforcement. CP5 re-proved the integrated scaffold end to end on the canonical WSL2/Linux workstation. PR #24 subsequently merged the closed scaffold into protected `main`.

CP6 now consumes that foundation to derive and materialize the concrete DANTE PostgreSQL database from the closed Domain + Logical + Physical model. The PostgreSQL architecture remains major line 18; CP6 refreshed the current technical patch from 18.4 to 18.6 and directly re-proved the technical foundation remotely before business-schema materialization begins.

## Current status

```text
CP1   CLOSED / DIRECT QA PASS
CP2   CLOSED / DIRECT QA PASS — ORIGINAL POSTGRESQL 18.4 EVIDENCE
CP3   CLOSED / DIRECT QA PASS — ORIGINAL POSTGRESQL 18.4 EVIDENCE
CP4   CLOSED / DIRECT REMOTE QA PASS
CP5   CLOSED / DIRECT INTEGRATED QA PASS
PR #24 MERGED / POST-MERGE BACKEND CI PASS

CP6-00 COMPLETE
CP6-01 CLOSED / GATE 01 PASS
CP6-02 CLOSED / GATE 02 PASS
CP6-03 NEXT / NOT STARTED — WHOLE DANTE DATABASE BLUEPRINT
POSTGRESQL 18.6 FOUNDATION REGRESSION DIRECT REMOTE QA PASS
```

Current CP6 execution boundary:

```text
CP6-03
whole DANTE database blueprint
        ↓
CP6-04
real database materialization
Alembic schema + tables + constraints + indexes + SQLAlchemy mappings
        ↓
CP6-05
whole-database direct PostgreSQL QA + CP6 closure
        ↓
POST-CP6
first product vertical application implementation
```

CP6 may therefore create business-schema migrations and SQLAlchemy database mappings once the whole-database blueprint authorizes them. CP6 does **not** implement the first product vertical's application use cases, product persistence adapters, API or frontend.

## Runtime contract

```text
Python supported line      3.14.x
initial exact pin          3.14.7
package manager            uv
import namespace           dante
project distribution       dante-backend
server semantics           Linux / WSL2
canonical DB architecture  PostgreSQL 18
current technical patch    PostgreSQL 18.6
Physical/CP2/CP3 evidence  PostgreSQL 18.4 historical exact evidence
```

The repository-controlled environment lives at `apps/backend/.venv` after `uv sync`. Do not share a single virtual environment between Windows and WSL.

## Dependency bootstrap

From `apps/backend`:

```bash
uv sync --locked
uv lock --check
uv tree --locked --depth 1
```

`pyproject.toml` records bounded compatibility policy; `uv.lock` records the exact resolved graph. Never hand-edit `uv.lock`.

Current persistence resolution is:

```text
SQLAlchemy       2.0.52
psycopg          3.3.4
Alembic          1.19.1
pytest-asyncio   1.4.0
```

## Runtime configuration

`.env.example` is a safe runtime-only template. Copy it to `.env.local` and replace the LOCAL runtime password with the credential provisioned for `dante_runtime`.

The application does not discover `.env.local` automatically; inject it explicitly through `uv`.

Runtime database variables:

| Variable | Required | Default | Secret | Meaning |
|---|---:|---|---:|---|
| `DANTE_DATABASE__HOST` | yes | none | no | PostgreSQL host |
| `DANTE_DATABASE__PORT` | no | `5432` | no | PostgreSQL port |
| `DANTE_DATABASE__NAME` | yes | none | no | database name |
| `DANTE_DATABASE__USER` | yes | none | no | runtime login; LOCAL uses `dante_runtime` |
| `DANTE_DATABASE__PASSWORD` | yes | none | yes | runtime credential |
| `DANTE_DATABASE__CONNECT_TIMEOUT_SECONDS` | no | `5` | no | connect timeout |
| `DANTE_DATABASE__POOL_SIZE` | no | `5` | no | persistent pool size |
| `DANTE_DATABASE__MAX_OVERFLOW` | no | `10` | no | bounded pool overflow |
| `DANTE_DATABASE__POOL_TIMEOUT_SECONDS` | no | `30` | no | pool checkout timeout |
| `DANTE_DATABASE__READINESS_TIMEOUT_SECONDS` | no | `2` | no | readiness deadline |

Admin and migrator secrets do **not** belong in the normal backend runtime environment.

The complete CP3 database contract lives in:

`docs/development/backend-cp3-persistence-contract.md`

The closed CP6-02 database constitution lives in:

`docs/development/backend-cp6-02-postgresql-persistence-constitution.md`

Formal Gate 02 closure evidence lives in:

`docs/development/backend-cp6-02-postgresql-persistence-constitution-closure.md`

Current CP6 execution scope and resume point live in:

`docs/workstreams/logical-postgresql.md`

## LOCAL database security provisioning

The PostgreSQL container starts with the platform/bootstrap administrator `postgres`. CP3 adds the application security boundary through the explicit provisioning command:

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
```

Provisioning is intentionally separate from FastAPI startup and Alembic. Supply admin, migrator and runtime credentials only to the provisioning command/process.

Conceptual invocation from `apps/backend`:

```bash
DANTE_DATABASE__HOST=127.0.0.1 \
DANTE_DATABASE__PORT=5432 \
DANTE_DATABASE__NAME=dante \
DANTE_ADMIN__USER=postgres \
DANTE_ADMIN__PASSWORD='<local admin secret>' \
DANTE_MIGRATOR__PASSWORD='<local migrator secret>' \
DANTE_RUNTIME__PASSWORD='<local runtime secret>' \
uv run python -m dante.platform.database.provisioning
```

Do not commit these secrets or reuse LOCAL credentials in DEV/UAT/PROD.

## Alembic

Alembic owns deployment history for the DANTE application schema.

```text
schema               dante
version table        dante.alembic_version
migration login      dante_migrator
DDL owner role       dante_owner via explicit SET ROLE
```

Migration commands must receive the dedicated migrator password separately from runtime config. Normal application startup never runs migrations.

The first revision is the technical CP3 baseline `20260820_01`; it intentionally creates no business schema. CP6-04 will add reviewed business-schema revisions only after CP6-03 closes the whole-database blueprint and materialization order.

PostgreSQL server patch maintenance such as 18.4 → 18.6 is platform/image maintenance and does not rewrite Alembic business/schema history.

## Run locally

After PostgreSQL roles/schema are provisioned and `.env.local` contains the matching runtime credential:

```bash
uv run --env-file .env.local \
  uvicorn dante.bootstrap.app:create_app \
  --factory \
  --reload
```

Technical probes:

```text
GET /health/live   process liveness only
GET /health/ready  bounded real PostgreSQL readiness
```

Expected dependency behavior:

```text
PostgreSQL available     live 200   ready 200
PostgreSQL unavailable   live 200   ready 503
PostgreSQL recovers      same process can return ready 200
```

Probe responses deliberately expose no credentials, DSN, database host/name, SQL or stack details. Neither endpoint appears in the product OpenAPI surface.

## Session and transaction rules

```text
one AsyncEngine per process
one async_sessionmaker per process
one AsyncSession per application operation/task
session never global/shared across concurrent tasks
autobegin=False
expire_on_commit=False
autoflush=True
```

The outer application-operation boundary owns commit/rollback. Persistence adapters never commit implicitly. There is no generic `Repository[T]` or generic Unit of Work in the closed scaffold.

## API documentation behavior

```text
LOCAL / DEV / UAT   /docs ON    /openapi.json ON    /redoc OFF
PROD                /docs OFF   /openapi.json OFF   /redoc OFF
```

## Quality and acceptance commands

From `apps/backend`:

```bash
# Local formatting (modifies files)
uv run ruff format .

# Non-mutating quality gates
uv run ruff format --check .
uv run ruff check .
uv run mypy

# Fast tests only — no PostgreSQL acceptance container
uv run pytest -m "not postgres"

# Real PostgreSQL 18.6 acceptance tests
uv run pytest -m postgres

# Full backend suite; includes the real PostgreSQL harness
uv run pytest

# Build wheel + source distribution
uv build
```

PostgreSQL-marked tests require the current image `dante-postgres-local:18.6`. They start one disposable, loopback-only acceptance container for the pytest session and create fresh databases inside that isolated cluster. If the required image is absent, the tests fail explicitly rather than skip.

This design protects the ordinary LOCAL `dante` database and its cluster-global application-role credentials from destructive acceptance testing while exercising the exact same DANTE PostgreSQL image/envelope.

## Historical CP5 integrated acceptance evidence

CP5 re-ran the production scaffold on the actual WSL2/Linux workstation against the then-current PostgreSQL 18.4 envelope:

```text
uv 0.12.5                                  PASS
Python 3.14.7                               PASS
uv lock --check / sync --locked            PASS
Ruff format + lint                         PASS
mypy strict                                PASS
fast pytest                                32/32 PASS
canonical PostgreSQL image rebuild         PASS
PostgreSQL pytest                          18/18 PASS
full pytest                                50/50 PASS
full-run coverage                          97.42% evidence only
uv build wheel + sdist                     PASS
LOCAL Compose PostgreSQL healthy           PASS
explicit provisioning                      PASS
real Uvicorn factory startup               PASS
GET /health/live                           200 {"status":"ok"}
GET /health/ready                          200 {"status":"ready"}
```

One immediately repeated full-suite launch hit a Docker Desktop/WSL `/forwards/expose` HTTP 500 while creating a disposable PostgreSQL container on a loopback port that had no Linux listener. After the diagnostic container was removed, a clean full run passed 50/50. The event is treated as transient local Docker port-forwarding behavior, not as an application or PostgreSQL acceptance failure.

## Current PostgreSQL 18.6 direct remote regression

CP6 refreshed only the PostgreSQL 18 maintenance patch and then executed the existing mandatory CI lanes against the exact branch HEAD:

```text
Backend CI run                32568664940
workflow event                workflow_dispatch
HEAD                          ec3dc795b5e044daa3a77723c94a1b4b5b92865c

PostgreSQL base               18.6-trixie
PostGIS                       3.6.4
pgvector                      0.8.6

Backend Quality               SUCCESS
fast pytest                   32 / 32 PASS
Ruff format/lint              PASS
mypy strict                   PASS
wheel + sdist                 PASS

Backend PostgreSQL            SUCCESS
PostgreSQL pytest             18 / 18 PASS
Alembic fresh → head          PASS
Alembic base/head round-trip  PASS
Alembic drift check           PASS
privilege matrix              PASS
runtime identity              PASS
outage/readiness recovery     PASS
transaction semantics         PASS

Backend CI Gate               SUCCESS
current test corpus           50 / 50 covered across the two mandatory CI lanes
```

This is **DIRECT REMOTE QA PASS for the technical PostgreSQL 18.6 foundation regression**. It does not convert any business-semantic HG/PSV item into PASS and predates the concrete DANTE business-database materialization stage.

PostgreSQL 18.6 release-note review found no current DANTE post-upgrade cleanup action: DANTE currently has no business GIN indexes, `btree_gist`, `ltree`, custom logical-decoding output plugin or `pgcrypto` use. Future PowerSync/logical-replication activation must review `output_plugin_libraries` and any then-applicable maintenance requirements.

## Boundaries

CP6 now explicitly authorizes, after the relevant blueprint/write gates:

- concrete Logical → PostgreSQL DANTE business tables;
- Alembic business-schema migrations;
- SQLAlchemy mappings that materialize the approved database model;
- concrete DB constraints, indexes, privileges and database-level support structures;
- real PostgreSQL tests of those database structures.

CP6 still does **not** automatically authorize:

- first-product-vertical application persistence adapters/use cases;
- product API routes merely because database objects exist;
- frontend behavior;
- AuthN/AuthZ product implementation;
- direct AI database access;
- PowerSync, Restate, PgBouncer or pgBackRest activation merely because selected;
- transactional outbox implementation without a real Class-A requirement;
- automatic deadlock/serialization retries without operation-specific safety/idempotency design;
- production deployment or blanket Physical HG/PSV PASS.

Current next backend action is **CP6-03 — Whole DANTE Database Blueprint**. It derives the full concrete relational schema and implementation/migration DAG from the closed 57/57 model and Constitution. Only after Gate 03 does CP6-04 begin real database materialization. First product vertical application work begins only after CP6 closes.
