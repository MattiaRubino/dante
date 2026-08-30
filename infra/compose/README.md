# DANTE LOCAL infrastructure

This directory owns the current developer-facing Docker Compose entry point for DANTE LOCAL PostgreSQL and the isolated PostgreSQL recovery harness.

## 1. Normal LOCAL PostgreSQL

Prerequisites:

```text
Docker Desktop + WSL2 backend
Ubuntu WSL integration
Docker CLI / Compose available without sudo
repository on Linux filesystem
```

Create the ignored LOCAL bootstrap secret once:

```bash
mkdir -p infra/compose/secrets
umask 077
python3 - <<'PY' > infra/compose/secrets/postgres_password.local
import secrets
print(secrets.token_urlsafe(32))
PY
```

Normal LOCAL commands:

```bash
docker compose -f infra/compose/local.yaml config --quiet
docker compose -f infra/compose/local.yaml build postgres
docker compose -f infra/compose/local.yaml up -d --wait
docker compose -f infra/compose/local.yaml ps
```

Normal endpoint:

```text
127.0.0.1:5432
```

Current image:

```text
dante-postgres-local:18.6
```

Current selected database capabilities:

```text
PostgreSQL           18.6
PostGIS              3.6.4
pgvector             0.8.6
pg_trgm              enabled
unaccent             enabled
pg_stat_statements   enabled + preloaded
native FTS           available
```

Application database roles are provisioned explicitly by the backend:

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
```

The current canonical application schema is `dante`; the current Alembic head is `20260830_09`.

## 2. Normal persistence/reset behavior

Preserve LOCAL data:

```bash
docker compose -f infra/compose/local.yaml down
```

Destroy LOCAL data intentionally:

```bash
docker compose -f infra/compose/local.yaml down --volumes
```

`down --volumes` destroys the PostgreSQL cluster. Application roles/schema must then be provisioned again before normal runtime use.

Initdb scripts bootstrap extensions only; they are not a migration system.

## 3. Real PostgreSQL acceptance isolation

Backend PostgreSQL acceptance does not use SQLite and must not mutate the ordinary LOCAL cluster.

From `apps/backend`:

```bash
uv run --frozen pytest -m postgres
```

The test harness uses disposable PostgreSQL state, generated test credentials and the current DANTE image.

## 4. Isolated recovery topology

Recovery uses:

```text
base     infra/compose/local.yaml
overlay  infra/compose/postgres-recovery.override.yaml
project  dante-postgres-recovery
```

Resolve it with:

```bash
docker compose \
  -p dante-postgres-recovery \
  -f infra/compose/local.yaml \
  -f infra/compose/postgres-recovery.override.yaml \
  config
```

Current isolated topology:

```text
image             dante-postgres-recovery:18.6-pgbackrest-2.59.1
host endpoint     127.0.0.1:55432
PostgreSQL volume dante-postgres-recovery_postgres-data
pgBackRest volume dante-postgres-recovery_pgbackrest-repository
PGDATA            /var/lib/postgresql/18/docker
repository path   /var/lib/pgbackrest
stanza            dante
```

The recovery PostgreSQL source enables:

```text
archive_mode              = on
archive_command           = /usr/bin/pgbackrest --stanza=dante archive-push %p
wal_level                 = replica
shared_preload_libraries  = pg_stat_statements
compute_query_id          = on
```

Local pgBackRest configuration uses:

```text
repo1-retention-full=2
```

That value is **LOCAL harness policy only**. It is not the production AWS retention contract.

## 5. Recovery safety boundary

The recovery workstream intentionally separates:

```text
PGDATA volume
!=
pgBackRest repository volume
```

Destructive database rehearsals may delete only the explicitly named recovery PGDATA volume after the script's manual confirmation. They must not delete the pgBackRest repository or ordinary `dante-local` volumes.

A restored verification target normally runs with:

```text
archive_mode=off
```

so verification does not create a new archive branch accidentally.

`pg_isready` is not a recovery-acceptance gate. Traffic/readiness acceptance requires at least:

```text
pg_is_in_recovery() = false
PostgreSQL 18.6
current Alembic head
current topology/security checks
semantic recovery checks
suppression-ledger reconciliation
```

## 6. Current database acceptance contract

Reusable recovery harnesses now expect:

```text
Alembic          20260830_09
tables           69
views             5
routines         15
triggers         76
indexes          97
foreign keys      69
CHECKs           123
other forbidden   0
```

They also verify the presence/security posture of:

```text
dante.material_state_retirement
runtime SELECT only
```

## 7. Recovery commands

### Archive failure/retry

```bash
bash infra/local/postgres/recovery/archive-failure-recovery-check.sh
```

### Materialize current database + FULL

```bash
bash infra/local/postgres/recovery/cp04-materialize-backup.sh
```

This runs the backend provisioning/Alembic boundaries, verifies the current database contract, seeds the deterministic Person fixture and creates the FULL used by later destructive tests.

### Destructive isolated restore

```bash
bash infra/local/postgres/recovery/cp04-destructive-restore-check.sh
```

Requires explicit:

```text
DELETE_RECOVERY_PGDATA
```

### Prepare deterministic PITR source

```bash
bash infra/local/postgres/recovery/cp05-prepare-pitr-source.sh
```

### Destructive named-target PITR

```bash
bash infra/local/postgres/recovery/cp05-destructive-pitr-check.sh
```

Requires explicit:

```text
DELETE_RECOVERY_PGDATA_FOR_PITR
```

### CP06 failure matrix

```bash
bash infra/local/postgres/recovery/cp06-failure-matrix-check.sh
```

Negative corruption/missing-WAL tests mutate only disposable repository clones.

### CP06 SC-011 anti-resurrection

```bash
bash infra/local/postgres/recovery/cp06-sc011-anti-resurrection-check.sh
```

This creates an entirely disposable source/B0/ledger topology, upgrades that source to the current repository head, proves physical resurrection from B0 and reconciles it using the versioned PREPARED/COMMITTED suppression ledger.

## 8. Suppression ledger contract

The external recovery suppression ledger is independent from both canonical PGDATA and the database backup repository.

Protocol:

```text
PREPARED
→ canonical PostgreSQL retirement/redaction commit
→ canonical read-back verification
→ COMMITTED bound to PREPARED SHA-256
```

Ambiguous/tampered state blocks recovery.

The ledger is technical disaster-recovery evidence only; PostgreSQL remains canonical.

## 9. Production boundary

Current local POSIX proof is not production AWS proof.

Production recovery acceptance still requires the selected topology to be activated and directly tested:

```text
AWS S3 Standard eu-south-1
Versioning
Object Lock GOVERNANCE
finite policy-bound retention
scoped backup identity
real backup/WAL objects
real restore/PITR readback
```

Production suppression-ledger storage/retention and object-store reconciliation remain separate activation/acceptance work.

## 10. Authority

Current detailed recovery status and evidence are maintained in:

```text
docs/workstreams/postgres-recovery.md
docs/workstreams/postgres-recovery-execution-plan.md
docs/database/README.md
docs/database/dante-postgresql-database-part-19.md
```

Git/Alembic preserve chronology; this README describes the current operational contract.