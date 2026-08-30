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

CP2 first-build acceptance also proved a clean build on the then-current PostgreSQL 18.4 image:

```bash
docker compose -f infra/compose/local.yaml build --no-cache postgres
```

The DANTE image is based on the immutable OCI index digest recorded in `infra/local/postgres/Dockerfile` and installs exact PostGIS/pgvector PGDG package versions.

The current LOCAL image name is:

```text
dante-postgres-local:18.6
```

CP2/CP3 original direct evidence remains historically tied to PostgreSQL 18.4. CP6 refreshed the current PostgreSQL 18 maintenance patch to 18.6 and directly re-proved the technical foundation remotely in Backend CI run `32568664940` at HEAD `ec3dc795b5e044daa3a77723c94a1b4b5b92865c`.

The real-PostgreSQL tests deliberately reuse the current exact image in one disposable acceptance container per pytest PostgreSQL session. They do not mutate the ordinary Compose cluster.

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

A fresh current Compose `dante` database contains:

```text
PostgreSQL           18.6
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

That CP2 document intentionally preserves the exact PostgreSQL 18.4 phase-time image and direct evidence; it is historical evidence, not the current image tag.

## PostgreSQL acceptance isolation

The real database test suite does not use SQLite and does not point destructive provisioning tests at the ordinary LOCAL Compose cluster.

From `apps/backend`:

```bash
uv run pytest -m postgres
```

The current test harness:

```text
requires dante-postgres-local:18.6
creates one loopback-only disposable PostgreSQL container
uses generated test-only admin/migrator/runtime secrets
creates fresh databases inside that isolated cluster
installs the exact selected extension envelope
runs provisioning + Alembic + runtime/transaction/privilege tests
destroys the acceptance container after the pytest session
```

The isolation is necessary because PostgreSQL roles are cluster-global; using the normal LOCAL cluster would allow acceptance provisioning to change the real LOCAL `dante_runtime` / `dante_migrator` credentials.

If the required image is absent, PostgreSQL-marked tests fail explicitly instead of skipping.

Current PostgreSQL 18.6 remote regression evidence:

```text
Backend CI run        32568664940
HEAD                  ec3dc795b5e044daa3a77723c94a1b4b5b92865c
Backend PostgreSQL    SUCCESS
PostgreSQL suite      18 / 18 PASS
Backend Quality       SUCCESS
Backend CI Gate       SUCCESS
```

## Windows database GUI

DBeaver or PyCharm Database Tools on Windows can connect to the normal LOCAL Compose database through:

```text
Host      127.0.0.1
Port      5432
Database  dante
```

For platform/bootstrap inspection use `postgres` with the contents of `infra/compose/secrets/postgres_password.local`.

After CP3 provisioning, application-level inspection can also use `dante_runtime` with the separately generated LOCAL runtime credential, subject to its intentionally restricted privileges.

## PostgreSQL recovery harness

The recovery workstream uses the normal `local.yaml` as its base and overlays only recovery-specific local isolation through:

```text
infra/compose/postgres-recovery.override.yaml
```

Run it with a dedicated Compose project name:

```bash
docker compose \
  -p dante-postgres-recovery \
  -f infra/compose/local.yaml \
  -f infra/compose/postgres-recovery.override.yaml \
  config
```

The recovery overlay intentionally keeps the ordinary LOCAL stack untouched and resolves to:

```text
Compose project   dante-postgres-recovery
image             dante-postgres-recovery:18.6-pgbackrest-2.59.1
host endpoint     127.0.0.1:55432
container port    5432
PostgreSQL volume dante-postgres-recovery_postgres-data
recovery volume   dante-postgres-recovery_pgbackrest-repository
```

The recovery worktree currently used for direct local proof is:

```text
/home/mattia/projects/dante-postgres-recovery
```

The same workstation-local `infra/compose/secrets/postgres_password.local` contract applies; the secret is ignored by Git and must never be committed. Recovery commands must include both Compose files and the `-p dante-postgres-recovery` project name so they cannot accidentally target the ordinary `dante-local` cluster.

CP02 directly proved the isolated harness with PostgreSQL 18.6 and pgBackRest 2.59.1.

### Recovery CP03 source activation

CP03 source/config is materialized only in the isolated recovery overlay. The ordinary `dante-local` service remains unchanged.

Resolved recovery-only PostgreSQL settings are:

```text
shared_preload_libraries = pg_stat_statements
compute_query_id          = on
archive_mode              = on
archive_command           = /usr/bin/pgbackrest --stanza=dante archive-push %p
wal_level                 = replica (inherited/current PostgreSQL value; not overridden)
archive_library           = unset
```

The local pgBackRest repository also sets:

```text
repo1-retention-full=2
```

This retention value is a deterministic LOCAL test policy only. It is not the production AWS retention contract and must not be extrapolated to S3 Versioning/Object Lock/lifecycle behavior.

### Recovery CP03 direct local proof

CP03 is **LOCAL PASS** for continuous WAL archiving and physical full backup on the isolated POSIX recovery harness.

Directly observed evidence includes:

```text
recovery container health                         PASS
archive_mode=on runtime                           PASS
archive_command exact runtime value               PASS
archive_library unset                             PASS
wal_level=replica                                 PASS
forced WAL switch                                 PASS
pg_stat_archiver successful archive               PASS
archived WAL physically present in repository     PASS
pgbackrest --stanza=dante check                   PASS
first FULL backup                                 PASS
repeated FULL backups                             PASS
pgbackrest info status=ok                         PASS
repo1-retention-full=2 behavior                   PASS
explicit pgbackrest expire                        PASS
archive failure visibility                        PASS
archive retry after repository recovery           PASS
post-failure physical WAL presence                PASS
post-failure pgBackRest check                     PASS
post-failure pgBackRest info status=ok            PASS
```

The retained full backups at CP03 closure were:

```text
20260830-114411F
20260830-114419F
```

The final observed archived WAL range at CP03 closure was:

```text
00000001000000000000000A / 00000001000000000000000F
```

The negative archive-path proof temporarily changed the current pgBackRest archive-directory mode from `0750` to `0550`, observed PostgreSQL archiver failure for WAL `00000001000000000000000E`, restored `0750`, observed successful retry of the same WAL, verified the compressed WAL artifact physically in the repository, and finished with `pgbackrest check` and `info` healthy.

The reusable bounded failure/recovery harness is:

```text
infra/local/postgres/recovery/archive-failure-recovery-check.sh
```

Run it from any repository location with:

```bash
bash infra/local/postgres/recovery/archive-failure-recovery-check.sh
```

The script targets only the dedicated `dante-postgres-recovery` Compose project and restores repository permissions with a shell trap if the injected failure path exits early.

`pg_stat_archiver` counters are runtime statistics and may reset across PostgreSQL restart/statistics reset. Persistent recovery evidence therefore also relies on pgBackRest repository artifacts plus `check`/`info`, not on treating the counters as durable history.

### Recovery CP04 materialization + destructive restore

CP04 is **LOCAL PASS** for destructive/isolated restore of the materialized DANTE PostgreSQL database. The earlier CP03 FULL sets were correctly discovered to contain only the bootstrap PostgreSQL/extension state: no `dante` schema, no DANTE application roles and no Alembic materialization. They remain valid CP03 archive/backup evidence but are not used as semantic restore proof.

The CP04 materialization harness is:

```text
infra/local/postgres/recovery/cp04-materialize-backup.sh
```

It uses the production backend's existing provisioning and Alembic boundaries rather than ad-hoc schema creation:

```text
P0 provisioning
→ dante_owner / dante_migrator / dante_runtime
→ Alembic upgrade head
→ P0 reconciliation
→ Alembic current/check
→ deterministic canonical Person fixture
→ accepted catalog/ACL/extension verification
→ pgBackRest check
→ dedicated FULL backup
```

The accepted deterministic CP04 fixture is:

```text
Person NativeRef 01993f19-9c00-7000-8000-000000000001
UUID version      7
```

The directly exercised semantic FULL was:

```text
backup label       20260830-132540F
start/stop         2026-08-30 13:25:40+00 / 13:26:24+00
database size      40.6MB
repo backup size   4.9MB
wal start/stop     ...00011 / ...00012
```

Before that FULL was accepted, direct verification proved:

```text
Alembic head                         20260826_08
tables/views/routines                68 / 5 / 14
triggers/indexes/FKs/CHECKs          75 / 95 / 68 / 120
forbidden enum/domain families       0
sequences/materialized/partitioned   0
RLS policies                         0
DANTE object owner                   dante_owner
DANTE roles                          dante_owner / dante_migrator / dante_runtime
dante_runtime SELECT alembic_version denied
PostGIS                              3.6.4
pgvector                             0.8.6
required extension set               PASS
```

The destructive restore harness is:

```text
infra/local/postgres/recovery/cp04-destructive-restore-check.sh
```

Its safety model is explicit:

```text
delete only      dante-postgres-recovery_postgres-data
preserve         dante-postgres-recovery_pgbackrest-repository
preserve         ordinary dante-local volumes
require manual   DELETE_RECOVERY_PGDATA confirmation
```

The rehearsal wrote a marker into the original PostgreSQL volume after the backup, removed the recovery PostgreSQL service, deleted the PostgreSQL named volume, verified the pgBackRest repository metadata survived unchanged, recreated an empty PostgreSQL volume, verified the marker was absent, and restored exactly `20260830-132540F` with `archive_mode=off` for the isolated verification target.

The first restored startup exposed a real filesystem boundary defect rather than a restore-data defect:

```text
/var/lib/postgresql              postgres:postgres 1777
/var/lib/postgresql/18           root:root 0700       ← blocked postgres traversal
/var/lib/postgresql/18/docker    postgres:root 0700    ← restored PGDATA
```

pgBackRest had already restored `40.6MB`, `1501` files and `global/pg_control` successfully. The only required repair was to normalize the version parent before the official PostgreSQL entrypoint dropped privileges:

```text
chown postgres:postgres /var/lib/postgresql/18
chmod 0700 /var/lib/postgresql/18
```

The versioned destructive harness incorporates that repair directly after restore so the known first-boot defect is not repeated.

Final CP04 direct evidence:

```text
PGDATA destructive replacement                    PASS
old source-volume marker absent                  PASS
pgBackRest repository survived unchanged         PASS
exact-set pgBackRest restore                     PASS
restored PGDATA boot                             PASS
PostgreSQL server_version_num                    180006 PASS
pg_is_in_recovery()                              false PASS
archive_mode on isolated target                  off PASS
Alembic                                           20260826_08 PASS
catalog topology                                  68/5/14/75/95/68/120 PASS
canonical Person fixture                         PASS
DANTE owners / roles / ACL                       PASS
required extension/version set                   PASS
real dante_runtime restored login + SELECT       PASS
```

Therefore:

```text
CP04 Destructive / Isolated Restore   LOCAL PASS
SC-031 destructive local restore      PASS
```

The current restored verification target is intentionally isolated with `archive_mode=off` until the next checkpoint topology is established. CP04 does **not** prove PITR, AWS S3, S3 Versioning, Object Lock, production retention or SC-011 anti-resurrection.
