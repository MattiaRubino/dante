# DANTE LOCAL infrastructure

- **Status:** CURRENT / OPERATIONAL REFERENCE
- **Last reconciled:** 2026-09-05

This directory owns the developer-facing Docker Compose entry point for DANTE LOCAL PostgreSQL, the optional Platform Observability profile and the isolated PostgreSQL recovery harness.

Current repository baseline:

```text
PostgreSQL       18.6
Alembic          20260904_17
topology         88|5|16|76|172|89|270|0|0|0
LOCAL Recovery   CP07 DATABASE-LOCAL PASS / CP08 APPLICATION+EMAIL REOPEN PASS
Observability    OPTIONAL COMPOSE PROFILE / ACCEPTED IN CURRENT TREE
remote provider  TBD / NOT ACTIVATED
cloud recovery   NOT CLAIMED
```

Detailed historical Recovery exact-head/timing evidence is intentionally not duplicated here; it remains in `../../docs/archive/branches/2026-08-feature-postgres-recovery.md`, retained evidence and Git history. This README describes the current operational surface directly.

## 1. Normal LOCAL PostgreSQL

Prerequisites:

```text
Docker Desktop + WSL2 backend
Ubuntu WSL integration
Docker CLI / Compose available without sudo
Docker Compose >= 2.24.4 for the recovery overlay `!override` tag
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

Normal endpoint and image:

```text
127.0.0.1:5432
dante-postgres-local:18.6
```

Selected database capabilities:

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

The canonical application schema is `dante`; the current Alembic head is `20260904_17`.

## 2. Persistence/reset behavior

Preserve LOCAL data:

```bash
docker compose -f infra/compose/local.yaml down
```

Destroy LOCAL named-volume state intentionally:

```bash
docker compose -f infra/compose/local.yaml down --volumes
```

`down --volumes` destroys the ordinary LOCAL PostgreSQL cluster and named volumes attached by `infra/compose/local.yaml`, including the ordinary-local pgBackRest repository volume. Application roles/schema must then be provisioned again before normal runtime use.

Initdb scripts bootstrap extensions only; they are not a migration system.

## 3. Platform Observability profile

The normal Compose path remains usable without telemetry. Platform Observability is an explicit optional profile layered into the same current `local.yaml`.

Prepare the LOCAL observer/Grafana secrets according to `../observability/README.md`, then expose only the caller's private WSL group to the non-root Alloy process:

```bash
export DANTE_OBSERVABILITY_LOG_GID="$(id -g)"
docker compose -f infra/compose/local.yaml --profile observability up -d --wait
```

The profile starts the current PostgreSQL service plus hardened Grafana Alloy. Alloy uses the dedicated `dante_observer` DSN, not backend runtime or administrator credentials. `dante_observer` is limited to `pg_read_all_stats` and has no DANTE/public business-object access.

LOCAL Alloy endpoints are loopback-only:

```text
UI / health   http://127.0.0.1:12345
OTLP gRPC     127.0.0.1:4317
OTLP HTTP     http://127.0.0.1:4318
Faro          http://127.0.0.1:12347/collect
```

Canonical observability references:

- `../observability/README.md` — collector, secrets, Grafana Cloud and operational assets
- `../../docs/architecture/observability-runtime-contract.md` — privacy/cardinality/failure contract
- `../../docs/development/observability-runbook.md` — operator verification and incident procedure

The application must remain available if Alloy or Grafana Cloud is unavailable. Telemetry queues/retries are bounded; telemetry failure never changes product/database truth.

## 4. Real PostgreSQL acceptance isolation

Backend PostgreSQL acceptance does not use SQLite and must not mutate the ordinary LOCAL cluster.

From `apps/backend`:

```bash
uv run --frozen pytest -m postgres
```

The test harness uses disposable PostgreSQL state, generated test credentials and the current DANTE image.

## 5. Isolated recovery topology

Materialize repository-level recovery prerequisites with:

```bash
bash infra/local/postgres/recovery/bootstrap-local-recovery.sh
```

The bootstrap is idempotent, branch-agnostic and fail-closed. It requires a clean attached Git branch with configured upstream and exact HEAD/upstream equality, creates missing LOCAL recovery secrets without overwriting existing non-empty values, validates mode/ignore policy and Compose, then builds the pinned recovery image.

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

The recovery PostgreSQL source enables archive mode, pgBackRest WAL archiving, replica-level WAL and `pg_stat_statements`. LOCAL pgBackRest retention uses `repo1-retention-full=2`; this is a LOCAL harness policy, not a production-provider contract.

## 6. Recovery safety boundary

```text
PGDATA volume
!=
pgBackRest repository volume
```

Destructive database rehearsals may delete only the explicitly named recovery PGDATA volume after the script's manual confirmation. They must not delete the pgBackRest repository or ordinary `dante-local` volumes.

`pg_isready` alone is not a recovery-acceptance gate. Traffic/readiness acceptance requires at least:

```text
pg_is_in_recovery() = false
PostgreSQL 18.6
current Alembic head
current topology/security checks
semantic recovery checks
suppression-ledger reconciliation
```

For application/Email reopen, CP08 additionally requires fail-closed Email reconciliation before workers/provider I/O resume.

## 7. Current database acceptance contract

Reusable recovery harnesses expect:

```text
Alembic          20260904_17
tables           88
views             5
routines         16
triggers         76
indexes          172
foreign keys      89
CHECKs           270
other forbidden   0
```

They also verify the presence/security posture of `dante.material_state_retirement` and runtime SELECT-only behavior.

## 8. Recovery commands

Archive failure/retry:

```bash
bash infra/local/postgres/recovery/archive-failure-recovery-check.sh
```

Materialize current database + FULL:

```bash
bash infra/local/postgres/recovery/cp04-materialize-backup.sh
```

Destructive isolated restore:

```bash
bash infra/local/postgres/recovery/cp04-destructive-restore-check.sh
```

Requires `DELETE_RECOVERY_PGDATA`.

Prepare deterministic PITR source:

```bash
bash infra/local/postgres/recovery/cp05-prepare-pitr-source.sh
```

Destructive named-target PITR:

```bash
bash infra/local/postgres/recovery/cp05-destructive-pitr-check.sh
```

Requires `DELETE_RECOVERY_PGDATA_FOR_PITR`.

CP06 failure matrix:

```bash
bash infra/local/postgres/recovery/cp06-failure-matrix-check.sh
```

CP06 SC-011 anti-resurrection:

```bash
bash infra/local/postgres/recovery/cp06-sc011-anti-resurrection-check.sh
```

CP07 whole LOCAL operator rehearsal:

```bash
bash infra/local/postgres/recovery/cp07-whole-recovery-rehearsal.sh
```

Ignored evidence output:

```text
infra/compose/secrets/postgres_recovery_cp07_report.json.local
```

CP08 Email/application reopen rehearsal:

```bash
bash infra/local/postgres/recovery/cp08-email-application-reopen-rehearsal.sh
```

Ignored evidence output:

```text
infra/compose/secrets/postgres_recovery_cp08_email_report.json.local
```

Accepted evidence scope remains:

```text
CP07 database-local reopen                           PASS
CP08 restored sendable Email work reconciliation    PASS
Email workers during reconciliation                 STOPPED
sensitive delivery material wipe                    PASS
second reconciliation                               IDEMPOTENT
claimable Email work before reopen                  0
application / Email reopen                          PASS
remote backup provider                              TBD / NOT ACTIVATED
production/cloud recovery                           NOT CLAIMED
```

## 9. Suppression-ledger contract

The external recovery suppression ledger is independent from both canonical PGDATA and the database backup repository.

```text
PREPARED
→ canonical PostgreSQL retirement/redaction commit
→ canonical read-back verification
→ COMMITTED bound to PREPARED SHA-256
```

Ambiguous/tampered state blocks recovery. The ledger is technical disaster-recovery evidence only; PostgreSQL remains canonical.

## 10. Future remote-provider boundary

```text
remote backup provider      TBD
remote provider activated   NO
production/cloud recovery   NOT CLAIMED
```

A future provider must preserve the pgBackRest-compatible recovery path, durable/appropriately immutable remote storage, finite retention, independent least-privilege credentials, required residency properties, backup/WAL readback, restore/PITR proof and suppression evidence across the full resurrection horizon.

Provider selection, credentials, costs and production acceptance remain deferred.

## 11. Authority

```text
current database contract
→ ../../docs/database/README.md

current observability contract
→ ../observability/README.md
→ ../../docs/architecture/observability-runtime-contract.md

operator recovery procedure
→ ../../docs/operations/postgres-recovery-runbook.md

executable recovery truth
→ ../local/postgres/recovery/

historical Recovery branch narrative
→ ../../docs/archive/branches/2026-08-feature-postgres-recovery.md
```

Git and archived evidence preserve chronology; this README stays focused on the current operational contract.
