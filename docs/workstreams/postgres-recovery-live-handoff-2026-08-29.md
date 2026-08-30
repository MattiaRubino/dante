# DANTE — PostgreSQL Recovery Live Handoff — 2026-08-29

- **Status:** CURRENT LIVE HANDOFF / CP03 LOCAL PASS / CP04 NOT STARTED
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/postgres-recovery`
- **Created from protected `main`:** `baa9aba52932a0fa09b957ee7668aeb459fb4a20`
- **Latest validated checkpoint before this handoff update:** `c38a36c5916f6a6cb629fcdfabb51def3e3bde2b`
- **Checkpoint message:** `docs(recovery): close CP03 execution gate`
- **Local worktree:** `/home/mattia/projects/dante-postgres-recovery`
- **Current macro-checkpoint:** CP03 — Continuous WAL + Backup / LOCAL PASS; CP04 NOT STARTED
- **Runtime source/config:** CP02 FOUNDATION PASS + CP03 ARCHIVE/BACKUP IMPLEMENTED
- **Runtime execution evidence:** CP02 DIRECT LOCAL PASS + CP03 DIRECT LOCAL PASS

> This file is the temporary continuation checkpoint for the active recovery branch. Repository truth beats conversation memory. It must be removed/consolidated before protected-main integration under the documentation lifecycle policy.

---

## 1. Continue exactly here

```text
repo:     MattiaRubino/dante
branch:   feature/postgres-recovery
base:     baa9aba52932a0fa09b957ee7668aeb459fb4a20
worktree: /home/mattia/projects/dante-postgres-recovery
```

The recovery worktree is dedicated to this branch. Other occupied worktrees include independent Access/Home/Platform work and must not be detached/reset/reassigned.

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

## 2. Read order for the next chat/engineer

Read in this order:

1. `docs/PROJECT-STATUS.md`
2. `docs/ROADMAP.md`
3. `docs/workstreams/postgres-recovery.md`
4. **this file**
5. `docs/workstreams/postgres-recovery-execution-plan.md`
6. current `docs/database/` System of Record
7. accepted Physical Model recovery section
8. post-selection validation register / SC-011 / SC-031 material
9. whole-database QA / CP6 closure evidence
10. `docs/development/agent-operating-manual.md`
11. documentation lifecycle policy
12. `infra/local/postgres/Dockerfile`
13. `infra/local/postgres/pgbackrest/pgbackrest.conf`
14. `infra/local/postgres/recovery/archive-failure-recovery-check.sh`
15. `infra/compose/local.yaml`
16. `infra/compose/postgres-recovery.override.yaml`
17. `infra/compose/README.md`

Do not reinterpret the database architecture from scratch.

---

## 3. What has actually been done

### Branch topology

```text
feature/postgres-recovery
→ created directly from protected main
→ baseline baa9aba52932a0fa09b957ee7668aeb459fb4a20
```

No feature branch was merged into it.

### Dedicated local worktree

```text
/home/mattia/projects/dante-postgres-recovery
```

At creation it tracked `origin/feature/postgres-recovery` exactly and was clean. The other DANTE worktrees remain dedicated to their own branches.

### Documentation/bootstrap

```text
docs/workstreams/postgres-recovery.md
docs/workstreams/postgres-recovery-execution-plan.md
docs/workstreams/postgres-recovery-live-handoff-2026-08-29.md
docs/workstreams/README.md
```

The workstream record freezes authority, boundaries, evidence vocabulary, selected-vs-implemented truth, local/remote acceptance boundary, provisional backup-policy hypothesis, recovery semantics, SC-011 hard gate and documentation lifecycle.

The execution plan defines CP01–CP07 with explicit implementation/evidence/closure conditions.

### CP01 contract freeze

Frozen:

```text
PostgreSQL                   18.6
base image                   postgres:18.6-trixie pinned by digest
PGDATA                       /var/lib/postgresql/18/docker
accepted pgBackRest baseline 2.59.0 historical selection
implementation maintenance   2.59.1 RATIFIED
PGDG package                 2.59.1-1.pgdg13+1
stanza                       dante
local repository             POSIX
repo path                    /var/lib/pgbackrest
repository volume            pgbackrest-repository
AWS                          NOT ACTIVATED
initial backup hypothesis    continuous WAL + daily FULL
numeric RPO/RTO              NOT INVENTED
SC-011                       OPEN HARD GATE
```

### CP02 source materialization

Recovery runtime paths:

```text
infra/local/postgres/Dockerfile
infra/local/postgres/pgbackrest/pgbackrest.conf
infra/compose/local.yaml
infra/compose/postgres-recovery.override.yaml
```

Implemented source behavior:

```text
pgBackRest package pin       2.59.1-1.pgdg13+1
build package assertion      exact dpkg version
build CLI assertion          pgBackRest 2.59.1
config path                  /etc/pgbackrest/pgbackrest.conf
config ownership             root:postgres / 0640
repository image ownership   postgres:postgres / 0750
stanza                       dante
pg1-path                     /var/lib/postgresql/18/docker
repo1-type                   posix
repo1-path                   /var/lib/pgbackrest
Docker repository volume     pgbackrest-repository:/var/lib/pgbackrest
```

The recovery repository is separate from the PostgreSQL data volume so a destructive `PGDATA` scenario does not delete the recovery source at the same time.

### Recovery Docker isolation

The ordinary LOCAL/observability stack was already using:

```text
dante-local-postgres-1  → 127.0.0.1:5432
dante-local-alloy-1     → healthy
```

Recovery uses its own contract:

```text
Compose project   dante-postgres-recovery
image             dante-postgres-recovery:18.6-pgbackrest-2.59.1
host port         127.0.0.1:55432
PostgreSQL volume dante-postgres-recovery_postgres-data
recovery volume   dante-postgres-recovery_pgbackrest-repository
```

The versioned override is:

```text
infra/compose/postgres-recovery.override.yaml
```

Recovery commands must use both Compose files and `-p dante-postgres-recovery`; do not target the ordinary `dante-local` project.

### CP03 source/config activation

The approved CP03 source materializes archive configuration only in the isolated recovery harness:

```text
archive_mode = on
archive_command = /usr/bin/pgbackrest --stanza=dante archive-push %p
archive_library = unset
wal_level = replica (existing/inherited value; not overridden)
repo1-retention-full = 2 (LOCAL test policy only)
```

The recovery overlay repeats the already-established `shared_preload_libraries=pg_stat_statements` and `compute_query_id=on` settings before the archive settings so replacing the Compose `command` does not remove existing PostgreSQL behavior.

### CP03 direct runtime proof

The isolated recovery image/config was rebuilt and the recovery PostgreSQL container recreated without destroying its PostgreSQL or pgBackRest repository volumes.

Direct evidence:

```text
container healthy                                             PASS
archive_mode                                                  on PASS
archive_command                                               exact pgBackRest archive-push PASS
archive_library                                               unset PASS
wal_level                                                     replica PASS
initial forced WAL                                            000000010000000000000002
pg_stat_archiver successful archive                           PASS
compressed WAL artifact physically present                   PASS
pgbackrest --stanza=dante check                               PASS
first FULL backup                                             20260830-114043F PASS
repeated FULL backups                                         PASS
repo1-retention-full=2 behavior                               PASS
explicit pgbackrest expire                                    PASS
retained FULL backup                                          20260830-114411F
retained FULL backup                                          20260830-114419F
```

Retention proof showed older FULL sets expiring as additional FULL backups crossed the configured LOCAL retention count. The explicit `expire` command also completed successfully.

### CP03 archive-failure/recovery proof

The directly executed negative-path scenario used target WAL:

```text
00000001000000000000000E
```

Observed sequence:

```text
archive directory baseline          postgres:postgres 0750
→ temporary injected mode           0550
→ pg_stat_archiver failure visible  PASS
→ last_failed_wal                   target ...000E
→ restore mode                      0750
→ automatic archive retry           PASS
→ last_archived_wal                 same ...000E
→ compressed physical WAL           PRESENT
→ pgbackrest check post-failure     PASS
→ pgbackrest info                   status: ok
```

Final observed archive range after recovery:

```text
00000001000000000000000A / 00000001000000000000000F
```

The reusable bounded harness is versioned at:

```text
infra/local/postgres/recovery/archive-failure-recovery-check.sh
```

Run it with:

```bash
bash infra/local/postgres/recovery/archive-failure-recovery-check.sh
```

The harness targets only the `dante-postgres-recovery` project and restores archive-directory permissions via `trap` if the injected failure path exits early.

`pg_stat_archiver` counters are runtime statistics and may reset across PostgreSQL restart/statistics reset. Persistent proof therefore also uses physical pgBackRest repository artifacts plus `check` and `info` rather than treating those counters as durable history.

---

## 4. CP02 direct runtime evidence

Observed on the dedicated recovery runtime:

```text
clean image build                                      PASS
image tag dante-postgres-recovery:18.6-pgbackrest-2.59.1 PASS
container recovery health                              PASS
host port isolation 55432                              PASS
ordinary dante-local PostgreSQL remained healthy       PASS
ordinary Alloy remained healthy                        PASS
pgbackrest version                                     pgBackRest 2.59.1 PASS
PostgreSQL version                                     18.6 PASS
data_directory                                         /var/lib/postgresql/18/docker PASS
/etc/pgbackrest/pgbackrest.conf                        root:postgres 0640 PASS
/var/lib/pgbackrest                                    postgres:postgres 0750 PASS
/var/lib/postgresql/18/docker                          postgres-owned/writable PASS
config readable by postgres                            PASS
repository writable by postgres                        PASS
stanza-create                                          PASS
pgbackrest --stanza=dante info                         PASS
archive.info + archive.info.copy                       PRESENT
backup.info + backup.info.copy                         PRESENT
```

Observed end-state from `pgbackrest --stanza=dante info` at CP02:

```text
stanza: dante
status: error (no valid backups)
cipher: none

db (current)
    wal archive min/max (18): none present
```

This was **expected at CP02**. No backup or WAL archive existed at that boundary.

Important distinction:

```text
CP02 foundation LOCAL PASS
!= CP03 archive/backup LOCAL PASS
!= restore PASS
!= PITR PASS
!= semantic recovery PASS
```

CP03 has now independently proven the archive/backup layer; the later distinctions remain active.

---

## 5. Recovery architecture carried forward

Accepted production target remains conceptually:

```text
PostgreSQL backup
pgBackRest accepted historical selection baseline 2.59.0
implementation maintenance pin 2.59.1
→ AWS S3 Standard eu-south-1
→ Versioning
→ Object Lock GOVERNANCE
→ finite policy-bound retention
```

The `2.59.1` implementation refresh is supported by direct CP02 foundation evidence plus CP03 WAL/backup evidence. Durable architecture documents are reconciled at integration rather than rewriting historical selection evidence as if it had always used the newer maintenance release.

The LOCAL `repo1-retention-full=2` value is only a deterministic test policy and is not the production retention contract.

---

## 6. Current recovery status matrix

```text
PostgreSQL 18.6                  LOCAL PASS
CP01 contract                    FROZEN
CP02 pgBackRest foundation       LOCAL PASS
pgBackRest source/config         LOCAL PASS
pgBackRest 2.59.1 runtime        LOCAL PASS
stanza-create                    LOCAL PASS
versioned recovery overlay       IMPLEMENTED
archive_mode runtime             LOCAL PASS
archive_command runtime          LOCAL PASS
continuous WAL                   LOCAL PASS
physical WAL repository proof    LOCAL PASS
pgBackRest check                 LOCAL PASS
local POSIX repository topology  LOCAL PASS
repo1-retention-full=2           LOCAL PASS
full backup proof                LOCAL PASS
archive failure/retry            LOCAL PASS
CP03                             LOCAL PASS
fresh/destructive restore        NOT RUN / CP04 NOT STARTED
PITR                             NOT RUN
AWS S3 repository                SELECTED / NOT ACTIVATED
S3 Versioning                    SELECTED / NOT ACTIVATED
Object Lock GOVERNANCE           SELECTED / NOT ACTIVATED
production retention behavior    NOT PROVEN
RPO/RTO measurements             PARTIAL LOCAL OBSERVATIONS ONLY / NO TARGETS RATIFIED
SC-031                           NOT RUN
SC-011                           OPEN HARD GATE / NOT RUN
operator runbook                 NOT IMPLEMENTED
```

Never shorten this to `recovery done`.

---

## 7. Frozen execution order

```text
CP01  Recovery Contract / Bootstrap                  CONTRACT FROZEN
CP02  pgBackRest Foundation                          LOCAL PASS
CP03  Continuous WAL + Backup                        LOCAL PASS
CP04  Destructive / Isolated Restore                 NOT STARTED
CP05  Deterministic PITR                             NOT STARTED
CP06  Failure Injection + Semantic Recovery          NOT STARTED
CP07  Whole Recovery QA + Runbook + Closure          NOT STARTED
```

Do not skip directly to AWS or a production bucket. Deterministic local proof comes first; real AWS selected-stack acceptance comes before final production-recovery PASS.

`pgbackrest check` was a **CP03** gate and is now directly proven. Successful backup still does not prove restore or PITR.

---

## 8. Important frozen decisions / hypotheses

### Canonicality

```text
PostgreSQL remains sole canonical persistence/material-history authority.
Recovery copies never become canonical merely because they were restored.
```

### Backup schedule hypothesis

```text
continuous WAL
+
daily FULL
```

This is the initial simplicity-first hypothesis, not an irreversible production schedule. Add differential/incremental scheduling only if measurements justify it.

### Restore topology

Prefer a fresh isolated PostgreSQL 18.6 target or an explicitly disposable target whose original `PGDATA` is destroyed.

A restore test must not pass because source data files survived.

### PITR

Primary automated test should use a deterministic restore point/marker:

```text
backup
→ write A
→ restore point R
→ archive WAL
→ write B
→ restore to R
→ A present
→ B absent
```

### RPO/RTO

No numeric production values are accepted yet. Measure actual backup/archive/restore/replay/operator timings first.

---

## 9. SC-011 anti-resurrection — do not lose this

This is the most important unresolved semantic issue.

Scenario:

```text
T0 old backup contains X
T1 accepted later deletion/redaction removes/restricts X
T2 canonical DB is destroyed
T3 old backup is restored
```

Raw physical recovery may bring X back. DANTE cannot silently expose/treat X as current permitted truth again.

Required conceptual recovery order:

```text
restore PostgreSQL
→ apply/verify deletion-redaction suppression / anti-resurrection state
→ verify canonical semantics
→ rebuild/discard stale derived state
→ reconcile object backup state
→ reopen traffic
```

There is currently **no accepted concrete implementation** for the independently surviving deletion/redaction suppression source/mechanism.

Therefore:

```text
SC-011 = NOT PASS
ANTI-RESURRECTION = OPEN HARD GATE
```

Do not invent a generic external ledger or second canonical database to make the test green. Derive the narrowest truthful mechanism consistent with accepted DANTE semantics.

---

## 10. Security boundary

Do not commit:

```text
AWS credentials
repository encryption passphrase
PostgreSQL secrets
bucket admin credentials
raw secret material
```

Selected remote posture to preserve:

```text
normal backup identity
→ minimum repository permissions
→ no s3:BypassGovernanceRetention

break-glass/admin
→ separately controlled
```

The local POSIX pgBackRest config contains no credentials. `infra/compose/secrets/postgres_password.local` remains workstation-local and ignored by Git.

Do not choose Terraform/OpenTofu merely because a bucket may later be needed. Production IaC remains a separate production-boundary decision unless explicitly activated.

---

## 11. What was intentionally NOT changed

The CP03 closure write does **not** modify or activate:

```text
infra/compose/local.yaml ordinary LOCAL runtime contract
apps/backend/
apps/web/
Alembic migrations
DANTE database schema
PostgreSQL roles/ACLs
wal_level
archive_library
backup scheduler/cron
restore/PITR configuration
recovery.signal
archive-get
AWS resources
S3 buckets
Versioning/Object Lock activation
production retention policy
secrets
PROJECT-STATUS.md
ROADMAP.md
protected main
other feature branches/worktrees
```

CP03 proves only the isolated LOCAL continuous-WAL/full-backup layer and its bounded local retention/failure behavior.

`PROJECT-STATUS.md` and `ROADMAP.md` remain protected-main truth and should be reconciled at the appropriate integration/closure boundary rather than used as a live branch diary.

---

## 12. Immediate next safe action

First fast-forward the dedicated recovery worktree to the CP03 closure HEAD and confirm repository health/readback. Then derive CP04 without destroying anything yet.

CP04 preparation must answer:

```text
which PostgreSQL target/container/volume is explicitly disposable?
which pgBackRest repository volume is the protected recovery source and must survive?
which retained FULL backup is selected as the restore source?
what deterministic fixture proves that restored data is the intended backup rather than stale surviving PGDATA?
what exact catalog/schema/role/ACL/semantic checks must pass?
what exact pgBackRest restore command/options are valid for PostgreSQL 18.6 and this topology?
what keeps restored traffic/application use closed until semantic verification passes?
```

Do **not** destroy PGDATA or invoke `pgbackrest restore` before the new CP04 topology/write/proof gate is explicitly frozen and approved.

---

## 13. CP04 opening boundary

CP04 owns:

```text
fresh/disposable PostgreSQL 18.6 restore target
explicit source-PGDATA isolation/destruction proof
protected preservation of pgBackRest recovery repository
selected retained FULL backup readback
pgBackRest restore execution
PostgreSQL startup from restored bytes
extension/catalog/schema topology verification
critical role/ACL verification where applicable
representative deterministic data verification
critical constraint/routine/trigger verification
application/readiness boundary verification where appropriate
SC-031 consideration only after direct proof
```

CP04 still does **not** prove:

```text
PITR
AWS S3
S3 Versioning
Object Lock
production retention
SC-011 anti-resurrection
whole recovery runbook closure
```

A successful CP03 backup is not restore proof. CP04 must be genuinely destructive/isolated enough that surviving source `PGDATA` cannot make the test pass accidentally.

---

## 14. Handoff discipline

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

The handoff may identify the latest validated checkpoint immediately preceding its own update; the branch HEAD itself is always re-read from Git before the next write/proof.

When the workstream is ready for protected-main integration, consolidate durable truth/evidence and delete this temporary handoff after documentation knowledge coverage is verified.
