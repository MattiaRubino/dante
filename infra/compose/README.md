# DANTE LOCAL infrastructure

This directory owns the developer-facing Docker Compose entry point for DANTE LOCAL stateful infrastructure.

The Compose topology still contains only PostgreSQL. The backend process continues to run directly in WSL during the normal developer inner loop. CP3 consumes this PostgreSQL boundary without adding a backend container, PgBouncer or additional LOCAL services.

## Prerequisites

- Docker Desktop running with the WSL2 backend;
- Ubuntu-24.04 WSL integration enabled;
- Docker CLI and Compose available from WSL without `sudo`;
- repository checked out on the Linux filesystem.

Run commands below from the repository root.

## Create the LOCAL PostgreSQL admin secret

The real password file is workstation-local and ignored by Git.

```bash
mkdir -p infra/compose/secrets
umask 077
python3 - <<'PY' > infra/compose/secrets/postgres_password.local
import secrets

print(secrets.token_urlsafe(32))
PY
```

Do not commit, paste into documentation, or reuse this LOCAL credential in DEV/UAT/PROD.

This credential belongs to the LOCAL platform/bootstrap administrator `postgres`. It is not the normal backend runtime credential.

## Validate Compose configuration

```bash
docker compose -f infra/compose/local.yaml config --quiet
```

## Build PostgreSQL

Normal rebuild:

```bash
docker compose -f infra/compose/local.yaml build postgres
```

CP2 first-build acceptance also proved a clean build:

```bash
docker compose -f infra/compose/local.yaml build --no-cache postgres
```

The DANTE image is based on the immutable OCI index digest recorded in `infra/local/postgres/Dockerfile` and installs exact PostGIS/pgvector PGDG package versions.

The resulting LOCAL image name is:

```text
dante-postgres-local:18.4
```

CP3 real-PostgreSQL tests deliberately reuse this exact image in one disposable acceptance container per pytest PostgreSQL session. They do not mutate the ordinary Compose cluster.

## Start and inspect

```bash
docker compose -f infra/compose/local.yaml up -d --wait
docker compose -f infra/compose/local.yaml ps
docker compose -f infra/compose/local.yaml logs postgres
```

The normal LOCAL service is published only on:

```text
127.0.0.1:5432
```

Container-to-container DNS, when a future Compose service needs it, uses:

```text
postgres:5432
```

## Connect with psql inside the container

```bash
docker compose -f infra/compose/local.yaml exec postgres \
  psql -U postgres -d dante
```

The `postgres` identity remains the LOCAL platform/bootstrap administrator. CP3 does **not** run FastAPI or Alembic as this superuser.

## CP3 application database roles

CP3 provisions the application security boundary separately from Compose/initdb:

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN normal backend runtime identity
```

The explicit provisioning command owns creation/reconciliation of these roles, their memberships, the `dante` schema, database/schema hardening and default privileges.

Conceptual LOCAL invocation from `apps/backend`:

```bash
DANTE_DATABASE__HOST=127.0.0.1 \
DANTE_DATABASE__PORT=5432 \
DANTE_DATABASE__NAME=dante \
DANTE_ADMIN__USER=postgres \
DANTE_ADMIN__PASSWORD="$(cat ../../infra/compose/secrets/postgres_password.local)" \
DANTE_MIGRATOR__PASSWORD='<generated LOCAL migrator secret>' \
DANTE_RUNTIME__PASSWORD='<generated LOCAL runtime secret>' \
uv run python -m dante.platform.database.provisioning
```

The migrator/runtime values must be generated independently, kept outside Git and supplied only to the process that needs them. The backend runtime receives only the runtime credential. Alembic receives only the migrator credential.

`dante_owner` has `NOLOGIN` and therefore no password.

Detailed persistence/security authority is recorded in:

`docs/development/backend-cp3-persistence-contract.md`

## Stop while preserving data

```bash
docker compose -f infra/compose/local.yaml down
```

The named volume remains. A later `up -d --wait` recreates the container against the same PostgreSQL cluster, including previously provisioned application roles/schema and data.

## Destructive LOCAL reset

```bash
docker compose -f infra/compose/local.yaml down --volumes
```

**This destroys the LOCAL PostgreSQL cluster and all data/application roles stored in it.**

The next `up -d --wait` performs a fresh `initdb` and reruns `/docker-entrypoint-initdb.d/010-extensions.sql`. CP3 application roles/schema must then be provisioned again before the normal backend can connect as `dante_runtime`.

Init scripts are bootstrap scripts, not a migration system, and they do not rerun against an already initialized volume.

## Selected database capabilities

A fresh Compose `dante` database contains:

```text
PostgreSQL           18.4
PostGIS              3.6.4
pgvector             0.8.6
pg_trgm              enabled
unaccent             enabled
pg_stat_statements   enabled + preloaded
native FTS           available
```

CP3 adds the dedicated application schema `dante`; extension/provider objects remain outside DANTE schema authority.

Detailed CP2 SQL/image/lifecycle evidence remains in:

`docs/development/backend-cp2-postgres-contract.md`

## CP3 PostgreSQL acceptance isolation

The real database test suite does not use SQLite and does not point destructive provisioning tests at the ordinary LOCAL Compose cluster.

From `apps/backend`:

```bash
uv run pytest -m postgres
```

The test harness:

```text
requires dante-postgres-local:18.4
creates one loopback-only disposable PostgreSQL container
uses generated test-only admin/migrator/runtime secrets
creates fresh databases inside that isolated cluster
installs the exact selected extension envelope
runs provisioning + Alembic + runtime/transaction/privilege tests
destroys the acceptance container after the pytest session
```

The isolation is necessary because PostgreSQL roles are cluster-global; using the normal LOCAL cluster would allow acceptance provisioning to change the real LOCAL `dante_runtime` / `dante_migrator` credentials.

If the required CP2 image is absent, PostgreSQL-marked tests fail explicitly instead of skipping.

## Windows database GUI

DBeaver or PyCharm Database Tools on Windows can connect to the normal LOCAL Compose database through:

```text
Host      127.0.0.1
Port      5432
Database  dante
```

For platform/bootstrap inspection use `postgres` with the contents of `infra/compose/secrets/postgres_password.local`.

After CP3 provisioning, application-level inspection can also use `dante_runtime` with the separately generated LOCAL runtime credential, subject to its intentionally restricted privileges.

The CP2 Windows GUI acceptance remains historical direct evidence and is not re-opened by CP3.

## Boundaries

This Compose configuration still does not provide:

- a backend application container;
- PgBouncer;
- business/domain tables;
- PowerSync or Restate;
- backup/recovery services;
- cloud or production infrastructure.

SQLAlchemy/psycopg/Alembic and application database roles belong to CP3 backend/tooling, not to the Compose service definition itself.
