# DANTE LOCAL infrastructure

This directory owns the developer-facing Docker Compose entry point for DANTE LOCAL stateful infrastructure.

Current CP2 scope contains only PostgreSQL. The backend process continues to run directly in WSL during the normal developer inner loop.

## Prerequisites

- Docker Desktop running with the WSL2 backend;
- Ubuntu-24.04 WSL integration enabled;
- Docker CLI and Compose available from WSL without `sudo`;
- repository checked out on the Linux filesystem.

Run commands below from the repository root.

## Create the LOCAL PostgreSQL secret

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

## Validate Compose configuration

```bash
docker compose -f infra/compose/local.yaml config --quiet
```

## Build PostgreSQL

Normal rebuild:

```bash
docker compose -f infra/compose/local.yaml build postgres
```

CP2 first-build acceptance uses a clean build as well:

```bash
docker compose -f infra/compose/local.yaml build --no-cache postgres
```

The DANTE image is based on the immutable OCI index digest recorded in `infra/local/postgres/Dockerfile` and installs exact PostGIS/pgvector PGDG package versions.

## Start and inspect

```bash
docker compose -f infra/compose/local.yaml up -d --wait
docker compose -f infra/compose/local.yaml ps
docker compose -f infra/compose/local.yaml logs postgres
```

The service is published only on:

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

The `postgres` identity is a LOCAL bootstrap administrator for CP2. Application runtime/migrator/owner roles are deliberately deferred to the persistence boundary.

## Stop while preserving data

```bash
docker compose -f infra/compose/local.yaml down
```

The named volume remains. A later `up -d --wait` recreates the container against the same PostgreSQL cluster.

## Destructive LOCAL reset

```bash
docker compose -f infra/compose/local.yaml down --volumes
```

**This destroys the LOCAL PostgreSQL cluster and all data stored in its named volume.**

The next `up -d --wait` performs a fresh `initdb` and reruns `/docker-entrypoint-initdb.d/010-extensions.sql`.

Use a destructive reset after a failed first-cluster initialization once the root cause has been corrected. Init scripts are bootstrap scripts, not a migration system, and they do not rerun against an already initialized volume.

## Selected database capabilities

A fresh `dante` database must contain:

```text
PostgreSQL           18.4
PostGIS              3.6.4
pgvector             0.8.6
pg_trgm              enabled
unaccent             enabled
pg_stat_statements   enabled + preloaded
native FTS           available
```

Detailed SQL and lifecycle acceptance obligations are recorded in:

`docs/development/backend-cp2-postgres-contract.md`

## Windows database GUI

DBeaver or PyCharm Database Tools on Windows connects through the published loopback port:

```text
Host      127.0.0.1
Port      5432
Database  dante
User      postgres
Password  contents of infra/compose/secrets/postgres_password.local
```

A successful GUI connection is part of CP2 direct acceptance; it is not inferred merely because the container is healthy.

## Boundaries

This Compose configuration does not provide:

- a backend application container;
- PgBouncer;
- SQLAlchemy/psycopg/Alembic;
- application database roles;
- business/domain tables;
- cloud or production infrastructure.
