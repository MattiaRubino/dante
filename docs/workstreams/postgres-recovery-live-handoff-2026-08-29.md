# DANTE — PostgreSQL Recovery Live Handoff — 2026-08-29

- **Status:** CURRENT LIVE HANDOFF / CP05 LOCAL PASS / CP06 NOT STARTED
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/postgres-recovery`
- **Created from protected `main`:** `baa9aba52932a0fa09b957ee7668aeb459fb4a20`
- **Local worktree:** `/home/mattia/projects/dante-postgres-recovery`
- **Current macro-checkpoint:** CP05 — Deterministic PITR / LOCAL PASS; CP06 Failure Injection + Semantic Recovery / Anti-Resurrection NOT STARTED
- **Runtime evidence:** CP02 FOUNDATION PASS + CP03 WAL/BACKUP PASS + CP04 DESTRUCTIVE RESTORE PASS + CP05 DETERMINISTIC PITR PASS
- **SC-031 local disposition:** PASS
- **PSV-40 local archive/restore/PITR disposition:** PASS
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

## 2. Read order for the next chat / engineer

Read in this order:

1. `docs/PROJECT-STATUS.md`
2. `docs/ROADMAP.md`
3. `docs/workstreams/postgres-recovery.md`
4. **this file**
5. `docs/workstreams/postgres-recovery-execution-plan.md`
6. current `docs/database/` System of Record
7. accepted Physical Model recovery section
8. post-selection validation register / SC-011 / SC-031 / PSV-40 material
9. whole-database QA / CP6 closure evidence
10. `docs/development/agent-operating-manual.md`
11. documentation lifecycle policy
12. `infra/local/postgres/Dockerfile`
13. `infra/local/postgres/pgbackrest/pgbackrest.conf`
14. `infra/local/postgres/recovery/archive-failure-recovery-check.sh`
15. `infra/local/postgres/recovery/cp04-materialize-backup.sh`
16. `infra/local/postgres/recovery/cp04-destructive-restore-check.sh`
17. `infra/local/postgres/recovery/cp05-prepare-pitr-source.sh`
18. `infra/local/postgres/recovery/cp05-destructive-pitr-check.sh`
19. `infra/compose/local.yaml`
20. `infra/compose/postgres-recovery.override.yaml`
21. `infra/compose/README.md`

Do not reinterpret the database architecture from scratch.

---

## 3. Frozen branch / runtime topology

```text
branch                       feature/postgres-recovery
worktree                     /home/mattia/projects/dante-postgres-recovery
PostgreSQL                   18.6
base image                   postgres:18.6-trixie pinned by digest
PGDATA                       /var/lib/postgresql/18/docker
persistent root              /var/lib/postgresql
pgBackRest                   2.59.1
PGDG package                 2.59.1-1.pgdg13+1
stanza                       dante
LOCAL repository             POSIX / /var/lib/pgbackrest
Compose project              dante-postgres-recovery
host port                    127.0.0.1:55432
PostgreSQL volume            dante-postgres-recovery_postgres-data
repository volume            dante-postgres-recovery_pgbackrest-repository
```

Selected production topology remains:

```text
pgBackRest
→ AWS S3 Standard eu-south-1
→ Versioning
→ Object Lock GOVERNANCE
→ finite policy-bound retention
```

AWS is still **NOT ACTIVATED** and local POSIX evidence must never be relabeled as direct AWS acceptance.

---

## 4. Current checkpoint matrix

```text
CP01 Recovery Contract / Bootstrap                  CONTRACT FROZEN
CP02 pgBackRest Foundation                          LOCAL PASS
CP03 Continuous WAL + Backup                        LOCAL PASS
CP04 Destructive / Isolated Restore                 LOCAL PASS
SC-031 destructive local restore                    PASS
CP05 Deterministic PITR                             LOCAL PASS
PSV-40 local pgBackRest archive/restore/PITR        PASS
CP06 Failure Injection + Semantic Recovery          NOT STARTED
SC-011 anti-resurrection                            OPEN HARD GATE / NOT PASS
CP07 Whole Recovery QA + Runbook + Closure          NOT STARTED
AWS selected recovery topology                      NOT ACTIVATED
```

Never shorten this to `recovery done`.

---

## 5. CP02 / CP03 retained foundation evidence

### CP02

```text
pgBackRest 2.59.1 exact package/CLI                 PASS
PostgreSQL 18.6                                     PASS
PGDATA /var/lib/postgresql/18/docker                PASS
config root:postgres 0640                           PASS
repository postgres:postgres 0750                   PASS
stanza-create                                       PASS
info / repository metadata                          PASS
ordinary LOCAL/Alloy non-interference               PASS
```

### CP03

```text
archive_mode=on                                     PASS
archive_command exact pgBackRest archive-push       PASS
archive_library unset                               PASS
wal_level=replica                                   PASS
forced WAL archive                                  PASS
physical WAL artifact                               PASS
pgBackRest check                                    PASS
FULL backup                                         PASS
repo1-retention-full=2 local behavior               PASS
explicit expire                                     PASS
archive permission failure visible                  PASS
same-WAL retry after repair                         PASS
post-failure check/info                             PASS
```

Versioned negative-path harness:

```text
infra/local/postgres/recovery/archive-failure-recovery-check.sh
```

---

## 6. CP04 destructive restore — retained exact truth

The CP03 backups were physically valid but the original recovery cluster was bootstrap-only. CP04 therefore materialized the accepted DANTE database through the existing backend provisioning/Alembic boundary before creating the semantic restore source.

Semantic source:

```text
P0 provisioning                         PASS
Alembic                                 20260826_08
accepted topology                       68|5|14|75|95|68|120|0|0|0
owner                                   dante_owner
roles                                   dante_owner,dante_migrator,dante_runtime
required extensions                     PASS
canonical Person fixture                01993f19-9c00-7000-8000-000000000001
semantic FULL                           20260830-132540F
DB size                                 40.6MB
repo set                                4.9MB
```

Versioned harnesses:

```text
infra/local/postgres/recovery/cp04-materialize-backup.sh
infra/local/postgres/recovery/cp04-destructive-restore-check.sh
```

Destructive CP04 proof:

```text
source-volume marker                    written
postgres-data volume                    deleted
repository volume                       preserved
repository hash                         unchanged
new empty PostgreSQL volume             recreated
old source marker                       absent
exact FULL restore                      PASS
restore size                            40.6MB / 1501 files
PostgreSQL boot                         PASS
archive_mode verification target        off
PostgreSQL                              18.6
Alembic                                 20260826_08
topology / owners / roles / ACL         PASS
extensions                              PASS
real dante_runtime login/read           PASS
```

### PostgreSQL 18 restore-parent finding

First CP04 startup failed after a successful pgBackRest restore because the root restore process had created:

```text
/var/lib/postgresql/18   root:root 0700
```

The restored PGDATA was valid. The official PostgreSQL entrypoint later dropped privileges and could not traverse the parent.

Proven narrow fix:

```text
chown postgres:postgres /var/lib/postgresql/18
chmod 0700 /var/lib/postgresql/18
```

This is built into the versioned destructive recovery harnesses. Do not replace it with an unbounded recursive `chown`.

---

## 7. CP05 deterministic PITR — exact direct evidence

### Source preparation

The CP04 restored target was on timeline 2 with `archive_mode=off`:

```text
current WAL          000000020000000000000014
local history        /var/lib/postgresql/18/docker/pg_wal/00000002.history
```

It was restarted as the CP05 archiving source with:

```text
archive_mode=on
archive_command=/usr/bin/pgbackrest --stanza=dante archive-push %p
pg_is_in_recovery()=false
timeline=2
```

Timeline-2 WAL archived successfully.

### Timeline-history finding

`00000002.history` had been created during the prior CP04 promotion while `archive_mode=off`. Enabling archiving later did **not** queue that existing history file retroactively.

The direct proof therefore did:

```text
pgbackrest --stanza=dante archive-push \
  /var/lib/postgresql/18/docker/pg_wal/00000002.history
```

Result:

```text
/var/lib/pgbackrest/archive/dante/18-1/00000002.history
```

This was followed by `pgbackrest check` PASS before any A/R1/B scenario was created.

Do not manually fake `.ready` state in `pg_wal/archive_status`. The versioned CP05 preparation harness handles the already-created history file explicitly through pgBackRest when needed.

### Exact CP05 scenario

```text
base FULL          20260830-132540F
scenario           dante_cp05_20260830T140906Z_19757
target timeline    2
restore point      dante_cp05_20260830T140906Z_19757_R1
restore LSN        0/16000230
restore WAL        000000020000000000000016
A                  01a05300-a55e-7845-a710-69387408d147
B                  01a05300-a5c0-7d08-a608-74ac9d821817
B WAL              000000020000000000000017
```

Archive proof:

```text
timeline history                   PASS
restore-point WAL ...0016          PASS
post-target B WAL ...0017          PASS
post-scenario pgBackRest check     PASS
repository WAL range reached       ... / 000000020000000000000018
```

Source immediately before destruction:

```text
BASELINE  PRESENT
A         PRESENT
B         PRESENT
```

### Destructive PITR

Direct pgBackRest target contract:

```text
--set=20260830-132540F
--type=name
--target=dante_cp05_20260830T140906Z_19757_R1
--target-timeline=2
--target-action=promote
--archive-mode=off
```

Direct results:

```text
postgres-data volume deleted                   PASS
repository survived                            PASS
old source marker absent                       PASS
exact-set FULL restore                         PASS
restore size                                   40.6MB / 1501 files
generated recovery_target_name                 PASS
generated recovery_target_timeline=2           PASS
generated recovery_target_action=promote       PASS
PITR target ready                              PASS
pg_is_in_recovery=false                        PASS
promoted timeline                              3
current WAL                                    000000030000000000000016
BASELINE                                       PRESENT
A                                              PRESENT
B                                              ABSENT
PostgreSQL 18.6                                PASS
Alembic 20260826_08                            PASS
accepted topology                              PASS
owners / roles / ACL                           PASS
required extension versions                    PASS
dante_runtime sees A and not B                 PASS
repository metadata unchanged                  PASS
```

This is the decisive deterministic state assertion:

```text
source before loss: baseline=1 / A=1 / B=1
restored to R1:     baseline=1 / A=1 / B=0
```

### Direct PostgreSQL recovery logs

```text
2026-08-30 14:13:00.197 UTC starting point-in-time recovery to R1
2026-08-30 14:13:00.210 UTC redo starts at 0/11000028
2026-08-30 14:13:00.460 UTC recovery stopping at R1
2026-08-30 14:13:00.460 UTC redo done at 0/160001C8
2026-08-30 14:13:00.502 UTC selected new timeline ID: 3
2026-08-30 14:13:00.568 UTC archive recovery complete
2026-08-30 14:13:00.736 UTC database system is ready to accept connections
```

### Direct LOCAL timing evidence

```text
pgBackRest physical restore reported       7.530 s
REPLAY_TO_TARGET_SECONDS                   0.263121
RECOVERY_TO_READY_SECONDS                  0.539736
TARGET_TO_READY_SECONDS                    0.276615
```

These values are LOCAL observations for this exercised dataset. They are not production RTO/RPO targets.

Versioned CP05 harnesses:

```text
infra/local/postgres/recovery/cp05-prepare-pitr-source.sh
infra/local/postgres/recovery/cp05-destructive-pitr-check.sh
```

The destructive harness incorporates timing derivation from PostgreSQL logs so a future clean rehearsal does not need a separate ad-hoc timing script.

---

## 8. Current runtime after CP05

The direct CP05 proof intentionally leaves the isolated verification target running:

```text
container      dante-postgres-recovery-cp05-pitr
archive_mode   off
in_recovery    false
current WAL    timeline 3
state          BASELINE + A present / B absent
```

Do not start the normal recovery service on the same PGDATA while this isolated target is being retained as evidence.

Once CP05 closure is synchronized and CP06 topology is explicitly designed, this target may be stopped/replaced under the new CP06 gate.

---

## 9. Security / secret boundary

Never commit:

```text
AWS credentials
repository encryption passphrases
PostgreSQL passwords
bucket admin credentials
raw secret material
```

The CP04/CP05 scenario/credential files under `infra/compose/secrets/*.local` are workstation-local and ignored by Git.

Selected future remote posture remains:

```text
normal backup identity
→ minimum repository permissions
→ no s3:BypassGovernanceRetention

break-glass/admin
→ separately controlled
```

Do not choose Terraform/OpenTofu merely because a bucket may later be required; production IaC remains a separate decision unless explicitly activated.

---

## 10. SC-011 anti-resurrection — next hard semantic problem

This remains the most important unresolved recovery issue.

Failure model:

```text
T0 backup contains state X
T1 accepted later deletion/redaction D1 removes or restricts X
T2 canonical DB is destroyed
T3 old backup is restored
T4 byte-correct restored PostgreSQL physically contains X again
```

Raw pgBackRest recovery cannot know that D1 happened later than the restored backup.

Required conceptual recovery order remains:

```text
restore PostgreSQL
→ apply/verify independently surviving deletion/redaction suppression facts
→ verify canonical semantics
→ rebuild/discard stale derived state
→ reconcile object backup state
→ reopen traffic only after all gates pass
```

Current truth:

```text
SC-011 = NOT PASS
ANTI-RESURRECTION = OPEN HARD GATE
accepted concrete suppression mechanism = NONE YET
```

Do not invent a generic external ledger or second canonical database just to make SC-011 green. CP06 must derive the narrowest truthful mechanism or remain blocked.

---

## 11. CP06 opening boundary

CP06 owns two different but related responsibilities.

### A. broader failure injection

At minimum evaluate/exercise:

```text
repository unavailable
missing required WAL
wrong stanza/repository config
bad/missing credentials where applicable
impossible PITR target
unusable/corrupted recovery set where safely reproducible
wrong backup/target mismatch
partially prepared target / dangerous startup boundary
```

A negative-path PASS means safe, visible, diagnosable failure. A command returning non-zero without a clear safe state is not enough.

CP03's archive-push permission failure/retry remains valid but is only one narrow failure case.

### B. semantic recovery / anti-resurrection

CP06 must inspect accepted current deletion/redaction/tombstone/material-history semantics and decide where the independently surviving recovery authority for later suppression facts can truthfully live.

Constraints:

```text
PostgreSQL remains sole canonical application persistence/material-history authority
no generic second canonical database
suppression authority must be narrowly recovery-scoped
must survive the disaster boundary it is supposed to repair
must be auditable
must not violate NativeRef identity/non-reuse semantics
must preserve deletion/redaction/privacy obligations
traffic remains closed until reconciliation PASS
```

Derived search/vector/sync state and R2/object reconciliation boundaries must also be defined before whole recovery closure.

---

## 12. Immediate next safe action

After the CP05 closure commit is pulled into the dedicated worktree:

```text
1. verify HEAD == origin and worktree clean
2. verify both versioned CP05 harnesses read back correctly
3. keep CP05 result as evidence; do not mutate it into CP06 claims
4. read accepted deletion/redaction/tombstone/material-history authority in current Domain/Logical/Physical/DB docs
5. enumerate actual disaster-survival boundaries available to DANTE
6. design the CP06 negative matrix
7. derive the narrowest possible SC-011 mechanism or explicitly identify the blocker
8. issue a new exact Git/runtime gate before writes/destructive tests
```

Do not activate AWS, Object Lock, production retention, object recovery, frontend/backend feature work or unrelated architecture under the CP05 closure scope.

---

## 13. Handoff discipline

At every meaningful checkpoint update this file with:

```text
latest validated checkpoint
what changed
what direct commands/tests ran
what PASS means
what remains NOT PROVEN
new blockers/risks
next safe action
```

The branch HEAD itself must always be re-read from Git before the next remote write/proof.

Before protected-main integration:

```text
current recovery truth → durable docs
accepted evidence       → durable QA/recovery record
useful branch narrative → optional one consolidated history record
live handoff             → REMOVE after knowledge coverage audit
```

No step of the eventual operator runbook may depend on this chat.