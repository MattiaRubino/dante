# DANTE LOCAL infrastructure

This directory owns the current developer-facing Docker Compose entry point for DANTE LOCAL PostgreSQL and the isolated PostgreSQL recovery harness.

Current protected-main database/recovery baseline:

```text
PostgreSQL       18.6
Alembic          20260830_09
topology         69|5|15|76|97|69|123|0|0|0
LOCAL Recovery   CP01–CP07 PASS / CLOSED / integrated via PR #47
remote provider  TBD / NOT ACTIVATED
cloud recovery   NOT CLAIMED
```

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

The current canonical application schema is `dante`; the current protected-main Alembic head is `20260830_09`.

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

### Fresh-clone recovery bootstrap

Repository-level recovery prerequisites are materialized by:

```bash
bash infra/local/postgres/recovery/bootstrap-local-recovery.sh
```

It is idempotent, branch-agnostic and fail-closed. It requires a clean attached Git branch with a configured upstream and exact HEAD/upstream equality, creates missing LOCAL recovery secrets without overwriting existing non-empty values, validates mode/ignore policy and Compose, then builds the pinned recovery image from `infra/local/postgres/Dockerfile`.

The whole CP07 rehearsal invokes this bootstrap automatically.

### Reproducible LOCAL recovery exact-head proof

Implementation/runtime proof HEAD:

```text
789e946a8f096b52f2a440b967120cc3e0a340a3
```

Reusable-bootstrap / runner proof:

```text
validation clone started without recovery secrets         PASS
first bootstrap created all three LOCAL secrets           PASS
second bootstrap preserved exact secret contents          PASS
secret files mode 0600 / ignored / untracked              PASS
repository Compose validation                              PASS
repository-built pinned recovery image                     PASS
runner independent from feature/postgres-recovery name     PASS
clean attached branch + configured upstream gate           PASS
whole backend QA on exact hardened tree                    PASS
pre-push whole CP07 rehearsal                              PASS
exact pushed implementation HEAD whole CP07 rehearsal      PASS
database-local reopen                                      PASS
deterministic PITR A-present / B-absent                    PASS
old protected X physical resurrection                      PROVEN
ledger anti-resurrection reconciliation                    PASS
payload reinsertion after retirement                       REJECTED
normal LOCAL / retained recovery / CP05 non-interference   PASS
disposable cleanup                                         PASS
remote backup provider                                     TBD / NOT ACTIVATED
production/cloud recovery                                  NOT CLAIMED
```

Phase-time exact-head proof relation:

```text
branch          feature/postgres-recovery
upstream        origin/feature/postgres-recovery
recovery image  dante-postgres-recovery:18.6-pgbackrest-2.59.1
```

That branch/upstream pair records the exact proof context only. The permanent runner is branch-agnostic; the Recovery workstream itself is now integrated into protected `main` via PR #47.

Measured LOCAL observations from the exact pushed hardened runner:

```text
backup label                              20260831-120208F
backup duration                           53.964433 s
backup repository size                    5743173 bytes
WAL archive freshness at disaster         0.834662 s
restore-point age at disaster             3.629809 s
physical restore                          7.650652 s
PITR replay to target                     0.144582 s
recovery to ready                         0.382306 s
semantic reconciliation                   1.021309 s
structural/security acceptance            0.910673 s
PGDATA loss → database-local reopen       16.261533 s
```

These are LOCAL rehearsal observations, not production RPO/RTO targets.

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

That value is **LOCAL harness policy only**. It is not a future remote-provider retention contract.

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

### CP07 whole local operator rehearsal

```bash
bash infra/local/postgres/recovery/cp07-whole-recovery-rehearsal.sh
```

This is a single disposable end-to-end rehearsal: healthy current PostgreSQL → FULL/WAL → deterministic PITR point → later retirement → total disposable PGDATA loss → restore/PITR → anti-resurrection reconciliation → structural/security/runtime acceptance → database-local reopen decision.

It writes ignored local evidence to:

```text
infra/compose/secrets/postgres_recovery_cp07_report.json.local
```

### CP07 exact local evidence

Implementation/runtime proof HEAD:

```text
8893efe629ff1dc9fc2b512779aa56457b802be6
```

Direct whole-rehearsal result:

```text
whole local operator rehearsal                  PASS
database-local reopen                           PASS
deterministic PITR A-present / B-absent         PASS
old protected X physical resurrection           PROVEN
ledger anti-resurrection reconciliation         PASS
payload reinsertion after retirement            REJECTED
structural/security/runtime acceptance          PASS
ordinary local volume non-interference          PASS
real recovery repository non-interference       PASS
retained CP05 target non-interference            PASS
disposable cleanup                              PASS
remote backup provider                          TBD / NOT ACTIVATED
production/cloud recovery                       NOT CLAIMED
```

Measured LOCAL observations:

```text
backup label                              20260831-091947F
backup duration                           52.598280 s
backup repository size                    5743174 bytes
WAL archive freshness at disaster         0.904446 s
restore-point age at disaster             3.980700 s
physical restore                          7.947759 s
PITR replay to target                     0.145295 s
recovery to ready                         0.389248 s
semantic reconciliation                   0.603417 s
structural/security acceptance            0.928466 s
PGDATA loss → database-local reopen       15.614213 s
```

These are LOCAL rehearsal observations only. They are not production RPO/RTO targets.

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

## 9. Future remote-provider boundary

The current LOCAL recovery system is deliberately provider-neutral.

```text
remote backup provider      TBD
remote provider activated   NO
production/cloud recovery   NOT CLAIMED
```

A future provider must satisfy the required capabilities when production deployment actually needs them:

```text
pgBackRest-compatible recovery path
durable remote storage
versioning / immutability appropriate to policy
finite retention
independent least-privilege credentials
required region/data-residency properties
backup + WAL readback
restore + PITR proof
suppression evidence retained across the full resurrection horizon
```

Provider selection, credentials, costs and production acceptance are deferred.

## 10. Authority

Current Recovery authority is deliberately durable and does not depend on the removed active-workstream overlays:

```text
current database contract
→ docs/database/README.md
→ docs/database/dante-postgresql-database-part-19.md

operator recovery procedure
→ docs/operations/postgres-recovery-runbook.md

executable recovery truth
→ infra/local/postgres/recovery/

historical closed-branch narrative
→ docs/archive/branches/2026-08-feature-postgres-recovery.md  (NON-AUTHORITATIVE)
```

The former `docs/workstreams/postgres-recovery.md` and `docs/workstreams/postgres-recovery-execution-plan.md` were deliberately removed during branch closure and must not be used as current links or authorities.

Git/Alembic preserve chronology; this README describes the current operational contract.
