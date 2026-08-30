# DANTE — PostgreSQL Recovery Live Handoff — 2026-08-29

- **Status:** CURRENT LIVE HANDOFF / CP04 LOCAL PASS / CP05 NOT STARTED
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/postgres-recovery`
- **Created from protected `main`:** `baa9aba52932a0fa09b957ee7668aeb459fb4a20`
- **Local worktree:** `/home/mattia/projects/dante-postgres-recovery`
- **Current macro-checkpoint:** CP04 — Destructive / Isolated Restore / LOCAL PASS; CP05 deterministic PITR NOT STARTED
- **Runtime evidence:** CP02 FOUNDATION PASS + CP03 WAL/BACKUP PASS + CP04 DESTRUCTIVE RESTORE PASS
- **SC-031 local disposition:** PASS
- **SC-011:** OPEN HARD GATE / NOT PASS

> This file is the temporary continuation checkpoint for the active recovery branch. Repository truth beats conversation memory. It must be removed/consolidated before protected-main integration under the documentation lifecycle policy.

---

## 1. Continue exactly here

```text
repo:     MattiaRubino/dante
branch:   feature/postgres-recovery
base:     baa9aba52932a0fa09b957ee7668aeb459fb4a20
worktree: /home/mattia/projects/dante-postgres-recovery
```

The recovery worktree is dedicated to this branch. Other occupied DANTE worktrees must not be detached, reset or reassigned.

Before local work:

```bash
pwd
git status --short --branch
git rev-parse HEAD
git rev-parse origin/feature/postgres-recovery
git rev-parse origin/main
git worktree list --porcelain
```

Use `git pull --ff-only` only after confirming the recovery worktree is clean and behind the same branch. Do not rewrite history.

---

## 2. Mandatory read order

1. `docs/PROJECT-STATUS.md`
2. `docs/ROADMAP.md`
3. `docs/workstreams/postgres-recovery.md`
4. **this file**
5. `docs/workstreams/postgres-recovery-execution-plan.md`
6. `docs/database/README.md` + Database Dictionary
7. accepted Physical Model recovery section
8. post-selection validation material / SC-011 / SC-031
9. `docs/development/backend-cp6-05-whole-database-qa.md`
10. `docs/development/agent-operating-manual.md`
11. documentation lifecycle policy
12. `infra/local/postgres/Dockerfile`
13. `infra/local/postgres/pgbackrest/pgbackrest.conf`
14. `infra/local/postgres/recovery/archive-failure-recovery-check.sh`
15. `infra/local/postgres/recovery/cp04-materialize-backup.sh`
16. `infra/local/postgres/recovery/cp04-destructive-restore-check.sh`
17. `infra/compose/local.yaml`
18. `infra/compose/postgres-recovery.override.yaml`
19. `infra/compose/README.md`

Do not reinterpret the database architecture from scratch.

---

## 3. Frozen recovery topology

```text
PostgreSQL                   18.6
base image                   postgres:18.6-trixie pinned by digest
PGDATA                       /var/lib/postgresql/18/docker
accepted pgBackRest baseline 2.59.0 historical selection
implementation maintenance   2.59.1 RATIFIED
PGDG package                 2.59.1-1.pgdg13+1
stanza                       dante
local repo type              POSIX
repo path                    /var/lib/pgbackrest
Compose project              dante-postgres-recovery
host port                    127.0.0.1:55432
PostgreSQL volume            dante-postgres-recovery_postgres-data
pgBackRest repo volume       dante-postgres-recovery_pgbackrest-repository
AWS                          NOT ACTIVATED
numeric RPO/RTO              NOT RATIFIED
SC-011                       OPEN HARD GATE
```

The PostgreSQL data and recovery repository volumes are deliberately separate. Destructive tests may delete only the explicitly disposable recovery PostgreSQL volume, never the ordinary `dante-local` data and never the pgBackRest repository unless a future separately approved test explicitly owns that action.

---

## 4. Checkpoint state

```text
CP01  Recovery Contract / Bootstrap                  CONTRACT FROZEN
CP02  pgBackRest Foundation                          LOCAL PASS
CP03  Continuous WAL + Backup                        LOCAL PASS
CP04  Destructive / Isolated Restore                 LOCAL PASS
CP05  Deterministic PITR                             NOT STARTED
CP06  Failure Injection + Semantic Recovery          NOT STARTED
CP07  Whole Recovery QA + Runbook + Closure          NOT STARTED
```

Do not shorten this to `recovery done`.

---

## 5. CP02 / CP03 evidence carried forward

CP02 directly proved the exact pgBackRest 2.59.1 foundation on PostgreSQL 18.6, isolated from ordinary LOCAL/observability runtime.

CP03 directly proved:

```text
archive_mode=on                                             PASS
archive_command pgBackRest archive-push                     PASS
archive_library unset                                       PASS
wal_level=replica                                           PASS
forced WAL archive                                          PASS
physical WAL repository object                              PASS
pgBackRest check                                            PASS
FULL backup                                                 PASS
repeated FULL backup                                        PASS
repo1-retention-full=2                                      PASS
explicit expire                                             PASS
archive failure visibility                                  PASS
automatic retry after repository recovery                   PASS
post-failure check/info                                     PASS
```

The versioned CP03 negative-path harness is:

```text
infra/local/postgres/recovery/archive-failure-recovery-check.sh
```

At CP03 closure the retained bootstrap FULLs were `20260830-114411F` and `20260830-114419F`; later CP04 work correctly discovered that they contained PostgreSQL bootstrap/extensions only, not a materialized DANTE application schema. They remain valid CP03 physical-backup evidence but are not semantic restore evidence.

---

## 6. CP04 semantic backup preparation

The CP04 preflight found:

```text
current database              dante
PostgreSQL                    18.6
schema dante                  absent
alembic_version               absent
DANTE owner/migrator/runtime  absent
required extensions           present
```

Therefore CP04 first materialized the accepted DANTE database through the existing backend boundaries rather than ad-hoc SQL.

Versioned harness:

```text
infra/local/postgres/recovery/cp04-materialize-backup.sh
```

Direct sequence:

```text
P0 provisioning
→ Alembic upgrade head
→ P0 reconciliation
→ Alembic current/check
→ canonical deterministic Person fixture
→ catalog/owner/role/ACL/extension verification
→ pgBackRest check
→ dedicated FULL
```

Observed materialized acceptance:

```text
uv                                 0.12.5
Alembic                            20260826_08
catalog topology                   68|5|14|75|95|68|120|0|0|0
DANTE object owner                 dante_owner
DANTE roles                        dante_owner / dante_migrator / dante_runtime
required extension set             PASS
canonical Person NativeRef         01993f19-9c00-7000-8000-000000000001
UUID version                       7
pgBackRest check                   PASS
```

Dedicated semantic FULL:

```text
label              20260830-132540F
start/stop         2026-08-30 13:25:40+00 / 13:26:24+00
wal start/stop     000000010000000000000011 / 000000010000000000000012
database size      40.6MB
repo set size      4.9MB
```

Workstation-local ignored files used by the harness:

```text
infra/compose/secrets/postgres_recovery_migrator_password.local
infra/compose/secrets/postgres_recovery_runtime_password.local
infra/compose/secrets/postgres_recovery_cp04_backup_label.local
```

Never commit or paste their secret values.

---

## 7. CP04 destructive restore proof

Versioned harness:

```text
infra/local/postgres/recovery/cp04-destructive-restore-check.sh
```

Directly exercised safety boundary:

```text
DELETE ONLY       dante-postgres-recovery_postgres-data
PRESERVE          dante-postgres-recovery_pgbackrest-repository
PRESERVE          ordinary dante-local volumes
REQUIRE           literal DELETE_RECOVERY_PGDATA confirmation
```

Proof sequence:

```text
verify semantic backup + fixture
→ hash repository backup.info
→ write unique marker into original PostgreSQL volume after backup
→ stop/remove only recovery PostgreSQL service
→ delete recovery PostgreSQL data volume
→ prove repository survived unchanged
→ recreate empty PostgreSQL volume without initdb
→ prove old marker absent
→ restore exact set 20260830-132540F with --archive-mode=off
→ verify restored PG_VERSION
→ boot isolated restored target
→ verify catalog + semantic + ACL + runtime state
```

pgBackRest direct restore evidence:

```text
backup set           20260830-132540F
restore size         40.6MB
file total           1501
pg_control           restored last
command              completed successfully
```

### First restored startup finding

The first boot failed with:

```text
mkdir: cannot create directory '/var/lib/postgresql/18': Permission denied
```

Direct filesystem inspection showed:

```text
/var/lib/postgresql              postgres:postgres 1777
/var/lib/postgresql/18           root:root 0700
/var/lib/postgresql/18/docker    postgres:root 0700
```

This was not a failed restore. pgBackRest had already restored PGDATA successfully. The root restore process had created the version parent with ownership that the official entrypoint could not traverse after dropping privileges.

Exact proven repair:

```text
chown postgres:postgres /var/lib/postgresql/18
chmod 0700 /var/lib/postgresql/18
```

After that repair the already-restored target booted successfully. The versioned destructive harness incorporates the repair immediately after restore and before boot.

### Final CP04 evidence

```text
PGDATA destructive replacement                    PASS
old source-volume marker absent                  PASS
repository survived unchanged                    PASS
exact-set pgBackRest restore                     PASS
restore parent permission normalization          PASS
PostgreSQL server_version_num                    180006 PASS
pg_is_in_recovery()                              false PASS
archive_mode                                     off PASS
Alembic                                          20260826_08 PASS
catalog topology                                 68/5/14/75/95/68/120 PASS
canonical Person fixture                        PASS
DANTE object owner                              dante_owner PASS
DANTE role/ACL state                            PASS
required extension/version set                  PASS
real dante_runtime restored authentication/read PASS
```

Disposition:

```text
CP04 Destructive / Isolated Restore   LOCAL PASS
SC-031 destructive local proof        PASS
```

---

## 8. Current runtime state after CP04

The restored verification target was intentionally left running as:

```text
dante-postgres-recovery-cp04-restore
```

Its accepted final evidence included:

```text
server_version_num  180006
pg_is_in_recovery() false
archive_mode        off
Alembic             20260826_08
fixture             01993f19-9c00-7000-8000-000000000001
```

**Do not start the normal recovery Compose PostgreSQL service on the same volume until CP05 topology is deliberately frozen.** The CP04 target is a verification target with `archive_mode=off`; it is not automatically the archive-producing source for CP05.

If the machine was rebooted, re-read actual container/volume state before acting. Runtime state is never inferred solely from this handoff.

---

## 9. CP05 opening boundary

Primary required scenario:

```text
valid FULL baseline
→ write deterministic A
→ create unique named restore point R
→ force/confirm WAL containing R archived
→ write deterministic B
→ force/confirm later WAL archived
→ destroy/isolate CP05 target
→ restore backup with recovery target R
→ prove recovery reached R
→ A PRESENT
→ B ABSENT
→ repeat catalog/semantic/ACL verification
```

Before executing CP05, freeze explicitly:

```text
which container/PGDATA is source vs restore target
whether the current CP04 target is discarded or replaced
how archive_mode is re-enabled on the source without contaminating the isolated verification target
which FULL is the PITR baseline
unique A/B NativeRefs or other deterministic canonical fixtures
unique restore-point name
exact WAL proof before destructive action
exact recovery_target_name / recovery_target_action behavior
filesystem-parent normalization after restore
post-PITR catalog/ACL/runtime checks
replay/recovery timing measurements
```

Do not use only wall-clock time as the primary target. Do not claim PITR from a normal full restore.

---

## 10. SC-011 anti-resurrection — still open

Scenario:

```text
T0 old backup contains X
T1 accepted later deletion/redaction removes/restricts X
T2 canonical DB is destroyed
T3 old backup is restored
```

Raw physical recovery may bring X back. DANTE cannot silently expose or treat X as current permitted truth again.

Required conceptual recovery order:

```text
restore PostgreSQL
→ apply/verify deletion-redaction suppression / anti-resurrection state
→ verify canonical semantics
→ rebuild/discard stale derived state
→ reconcile object backup state
→ reopen traffic
```

There is currently **no accepted concrete implementation** for the independently surviving deletion/redaction suppression mechanism.

```text
SC-011 = NOT PASS
ANTI-RESURRECTION = OPEN HARD GATE
```

Do not invent a generic external ledger or second canonical database merely to make the test green.

---

## 11. Production recovery boundary still NOT PROVEN

Accepted remote target remains:

```text
pgBackRest
→ AWS S3 Standard eu-south-1
→ Versioning
→ Object Lock GOVERNANCE
→ finite policy-bound retention
```

Not yet proven:

```text
real AWS S3 repository
Versioning behavior
Object Lock GOVERNANCE behavior
production retention/lifecycle
remote IAM/credential boundary
remote restore/PITR
R2/object reconciliation
production RPO/RTO
operator-grade whole recovery runbook
```

LOCAL POSIX evidence must never be mislabeled as direct AWS selected-stack evidence.

---

## 12. What remains intentionally out of current CP04 closure

```text
PITR execution
named recovery marker proof
A-present/B-absent proof
AWS/S3 activation
Versioning/Object Lock
production retention
SC-011 implementation
R2/object reconciliation
application feature work
frontend work
new Alembic/schema changes
new database semantics
PROJECT-STATUS.md / ROADMAP.md branch-diary updates
protected main
other feature branches/worktrees
```

---

## 13. Handoff discipline

At every meaningful checkpoint update this file with:

```text
latest validated implementation/documentation checkpoint
what changed
what direct commands/tests ran
what PASS means
what remains NOT PROVEN
new blockers/risks
next safe action
```

The branch HEAD itself is always re-read from Git before the next write/proof.

When the workstream is ready for protected-main integration, consolidate durable truth/evidence and delete this temporary handoff after documentation knowledge coverage is verified.