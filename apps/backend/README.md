# DANTE Backend

Production backend application for DANTE.

CP1 established the Python/process/configuration foundation. CP2 established the reproducible LOCAL
PostgreSQL 18.4 image/envelope. CP3 activates application persistence, Alembic authority, PostgreSQL
role separation and the real PostgreSQL acceptance harness.

## Runtime contract

```text
Python supported line   3.14.x
initial exact pin       3.14.7
package manager         uv
import namespace        dante
project distribution    dante-backend
server semantics        Linux / WSL2
canonical DB            PostgreSQL 18.4
```

The repository-controlled environment lives at `apps/backend/.venv` after `uv sync`. Do not share a
single virtual environment between Windows and WSL.

## Dependency bootstrap

From `apps/backend`:

```bash
uv sync --locked
uv lock --check
uv tree --locked --depth 1
```

`pyproject.toml` records bounded compatibility policy; `uv.lock` records the exact resolved graph.
Never hand-edit `uv.lock`.

Current CP3 persistence resolution is:

```text
SQLAlchemy       2.0.52
psycopg          3.3.4
Alembic          1.19.1
pytest-asyncio   1.4.0
```

## Runtime configuration

`.env.example` is a safe runtime-only template. Copy it to `.env.local` and replace the LOCAL runtime
password with the credential provisioned for `dante_runtime`.

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

## LOCAL database security provisioning

The CP2 PostgreSQL container starts with the platform/bootstrap administrator `postgres`. CP3 adds the
application security boundary through the explicit provisioning command:

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
```

Provisioning is intentionally separate from FastAPI startup and Alembic. Supply admin, migrator and
runtime credentials only to the provisioning command/process.

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

Migration commands must receive the dedicated migrator password separately from runtime config. Normal
application startup never runs migrations.

The first revision is the technical CP3 baseline `20260820_01`; it intentionally creates no business
schema.

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

Probe responses deliberately expose no credentials, DSN, database host/name, SQL or stack details.
Neither endpoint appears in the product OpenAPI surface.

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

The outer application-operation boundary owns commit/rollback. Persistence adapters never commit
implicitly. There is no generic `Repository[T]` or generic Unit of Work in CP3.

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

# Real PostgreSQL 18.4 CP3 acceptance tests
uv run pytest -m postgres

# Full backend suite; includes the real PostgreSQL harness
uv run pytest

# Build wheel + source distribution
uv build
```

PostgreSQL-marked tests require the CP2 image `dante-postgres-local:18.4`. They start one disposable,
loopback-only acceptance container for the pytest session and create fresh databases inside that
isolated cluster. If the required image is absent, the tests fail explicitly rather than skip.

This design protects the ordinary LOCAL `dante` database and its cluster-global application-role
credentials from destructive acceptance testing while exercising the exact same DANTE PostgreSQL
image/envelope.

## Boundaries

CP3 still does not authorize:

- concrete Logical → PostgreSQL business tables/mappings;
- business repositories/adapters;
- product API routes;
- AuthN/AuthZ;
- direct AI database access;
- PowerSync, Restate, PgBouncer or pgBackRest activation;
- transactional outbox implementation;
- automatic deadlock/serialization retries;
- production deployment or blanket Physical HG/PSV PASS.
