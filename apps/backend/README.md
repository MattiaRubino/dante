# DANTE Backend

Production backend application for DANTE.

CP1 establishes the Python/process/configuration foundation only. PostgreSQL infrastructure starts in
CP2; application persistence, SQLAlchemy/psycopg and Alembic start in CP3.

## Runtime contract

```text
Python supported line   3.14.x
initial exact pin       3.14.7
package manager         uv
import namespace        dante
project distribution    dante-backend
server semantics        Linux / WSL2
```

The repository-controlled environment lives at `apps/backend/.venv` after `uv sync`. Do not share a
single virtual environment between Windows and WSL.

## Bootstrap

From `apps/backend`:

```bash
cp .env.example .env.local
uv sync --locked
uv lock --check
```

`.env.local` is a LOCAL convenience file and is ignored by Git. The application does not discover or
load it automatically; the local process command injects it explicitly through `uv`.

## Run locally

```bash
uv run --env-file .env.local \
  uvicorn dante.bootstrap.app:create_app \
  --factory \
  --reload
```

Default technical probes:

```text
GET /health/live   process liveness
GET /health/ready  CP1 bootstrap/configuration readiness
```

Neither probe belongs to the product OpenAPI surface. Their responses deliberately expose no
environment, release/build identity, host information, dependency versions or configuration values.

## Bootstrap configuration

| Variable | Required | Default | Secret | Meaning |
|---|---:|---|---:|---|
| `DANTE_ENV` | yes | none | no | `local`, `dev`, `uat`, or `prod` runtime identity |
| `DANTE_RELEASE_SHA` | yes | none | no | source/release identity; `local` marker only in LOCAL |
| `DANTE_BUILD_ID` | yes | none | no | build/execution identity; `local` marker only in LOCAL |
| `DANTE_DEBUG` | no | `false` | no | FastAPI application debug behavior only |

Safety rules include:

```text
unknown DANTE_ENV                    -> bootstrap failure
missing/blank release or build ID    -> bootstrap failure
prod + DANTE_DEBUG=true              -> bootstrap failure
dev/uat/prod + local identity marker -> bootstrap failure
```

`DANTE_DEBUG` does not control Uvicorn reload, host, port, workers or log level. Those belong to the
ASGI server/runtime boundary.

The durable rationale and complete variable contract live in
`docs/development/backend-cp1-contract.md`.

## API documentation behavior

```text
LOCAL / DEV / UAT   /docs ON    /openapi.json ON    /redoc OFF
PROD                /docs OFF   /openapi.json OFF   /redoc OFF
```

This behavior is derived from validated `DANTE_ENV`; there is no extra docs-toggle variable in CP1.

## Quality commands

From `apps/backend`:

```bash
# Local formatting (modifies files)
uv run ruff format .

# Non-mutating format gate
uv run ruff format --check .

# Lint
uv run ruff check .

# Static typing
uv run mypy

# Tests + statement/branch coverage report
uv run pytest

# Build wheel + source distribution
uv build
```

Coverage is measured from the first real tests, including branch coverage, but CP1 deliberately has no
arbitrary percentage threshold. Material behavior still requires direct tests regardless of coverage
percentage.

## Dependency discipline

`pyproject.toml` records bounded compatibility policy; `uv.lock` records the exact resolved graph.
Never hand-edit `uv.lock`. Dependency upgrades are explicit reviewed changes and must regenerate the
lock through `uv` and run the affected validation suite.

## CP1 boundaries

Not present by design in CP1:

- PostgreSQL or database settings;
- SQLAlchemy, psycopg or Alembic;
- business/domain capability modules;
- product API routes;
- AuthN/AuthZ;
- fake observability/security layers;
- `lifespan.py` or `wiring.py` without a real resource/component graph;
- backend OCI packaging;
- PowerSync, Restate, R2, OR-Tools, PgBouncer or cloud/IaC implementation.

A new backend `DANTE_*` variable is not complete until its ownership, type, source, requiredness,
default, secret class, consumer, effect, invalid combinations, exposure policy, lifecycle and test
evidence are documented according to the permanent rule in the CP1 technical contract.
