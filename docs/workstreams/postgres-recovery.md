# DANTE — PostgreSQL Recovery Workstream

- **Status:** ACTIVE / CP02 LOCAL PASS / CP03 NOT STARTED
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/postgres-recovery`
- **Created from protected `main`:** `baa9aba52932a0fa09b957ee7668aeb459fb4a20`
- **Local worktree:** `/home/mattia/projects/dante-postgres-recovery`
- **Current PostgreSQL:** 18.6
- **Accepted recovery technology baseline:** pgBackRest 2.59.0 + AWS S3 Standard `eu-south-1` + Versioning + Object Lock GOVERNANCE
- **Activation implementation pin:** pgBackRest 2.59.1 / PGDG `2.59.1-1.pgdg13+1`; CP02 direct local foundation proof PASS
- **Current macro-checkpoint:** CP02 — pgBackRest Foundation / LOCAL PASS; CP03 requires a new write gate
- **Live handoff:** `postgres-recovery-live-handoff-2026-08-29.md`
- **Execution plan:** `postgres-recovery-execution-plan.md`

> Repository truth beats conversation memory. This workstream activates the recovery capability already selected by the accepted Physical Model. It does not reopen CP6, does not create a second canonical database, and does not treat a backup copy as accepted application truth.

---

## 1. Mandatory continuation boundary

Continue exactly:

```text
repo:     MattiaRubino/dante
branch:   feature/postgres-recovery
base:     baa9aba52932a0fa09b957ee7668aeb459fb4a20
worktree: /home/mattia/projects/dante-postgres-recovery
```

The recovery branch has its own dedicated worktree. Do not steal, detach, reset, rebase, or repurpose the other occupied DANTE worktrees.

Before any local write/proof:

```bash
pwd
git status --short --branch
git rev-parse HEAD
git rev-parse origin/feature/postgres-recovery
git rev-parse origin/main
git worktree list --porcelain
```

Never write to protected `main`. No force-push/history rewrite. No merge/rebase from another feature branch without an explicit integration reason and user gate.

---

## 2. Authority and read order

Read before implementation:

1. `docs/PROJECT-STATUS.md`
2. `docs/ROADMAP.md`
3. this file
4. `docs/workstreams/postgres-recovery-execution-plan.md`
5. current database System of Record under `docs/database/`
6. accepted Physical Model and post-selection validation material
7. whole-database QA / CP6 closure evidence
8. `docs/development/agent-operating-manual.md`
9. documentation lifecycle policy
10. current `infra/local/postgres/` and `infra/compose/` runtime materialization

Authority order:

```text
current protected-main code / migrations / executable tests
> accepted current Domain / Logical / Physical / ADR contracts
> Database System of Record and current development QA contracts
> this branch-local workstream record
> temporary live handoff
> conversation memory
```

This branch may add direct recovery evidence and later update durable recovery authority, but it must not silently reinterpret accepted database semantics.

---

## 3. Recovery constitution

Permanent constraints:

```text
PostgreSQL = sole canonical persistence + material-history authority
backup repository != canonical truth
restored bytes != automatically accepted current semantic truth
restore != resurrection of logically retired truth
selected != implemented != activated != directly proven
successful backup != successful restore
successful restore != successful PITR
successful PITR != semantic recovery PASS
configuration present != operational evidence
```

Recovery must preserve the accepted DANTE semantic rules, including:

```text
specific truthful semantics > generic catch-all abstraction
planned/intended != Actual
Observation != Actual
Evidence != Provenance
absence != false
canonical != provider state
retention/redaction/tombstone integrity
NativeRef non-reuse
non-interference / inference-leakage obligations
```

No recovery shortcut may rewrite historical semantics merely to make a restored database look current.

---

## 4. Accepted target vs current implementation

### 4.1 Current implementation after CP02 local proof

Current branch source materializes a PostgreSQL 18.6 image with PostGIS, pgvector and an exact pgBackRest package pin. The local compose topology mounts a dedicated recovery repository volume physically distinct from `PGDATA`, and the recovery-specific compose overlay isolates the test runtime from the ordinary LOCAL/observability stack.

Current source/runtime topology:

```text
PostgreSQL base image            postgres:18.6-trixie pinned by digest
PostgreSQL runtime               PostgreSQL 18.6 direct local PASS
PostgreSQL PGDATA                /var/lib/postgresql/18/docker direct local PASS
PostgreSQL persistence volume    postgres-data:/var/lib/postgresql
pgBackRest package pin           2.59.1-1.pgdg13+1 clean build PASS
pgBackRest CLI                   pgBackRest 2.59.1 direct local PASS
pgBackRest config                /etc/pgbackrest/pgbackrest.conf
stanza                           dante direct local PASS
local repository type            POSIX
local repository path            /var/lib/pgbackrest
local repository volume          pgbackrest-repository:/var/lib/pgbackrest
config ownership                 root:postgres / 0640 direct local PASS
repository ownership             postgres:postgres / 0750 direct local PASS
recovery Compose project         dante-postgres-recovery
recovery image                   dante-postgres-recovery:18.6-pgbackrest-2.59.1
recovery host port               127.0.0.1:55432
ordinary LOCAL PostgreSQL        remained healthy on 127.0.0.1:5432
```

Direct CP02 evidence observed on the dedicated worktree/runtime:

```text
clean image build                              PASS
container health                               PASS
ordinary dante-local PostgreSQL non-interference PASS
ordinary Alloy non-interference                PASS
pgbackrest version == pgBackRest 2.59.1        PASS
PostgreSQL version == 18.6                     PASS
data_directory == /var/lib/postgresql/18/docker PASS
config readable by postgres                    PASS
repository writable by postgres                PASS
PGDATA writable by postgres                    PASS
stanza-create                                  PASS
pgbackrest --stanza=dante info                 PASS
archive.info / backup.info metadata present    PASS
```

Expected end-of-CP02 `info` state is intentionally:

```text
stanza: dante
status: error (no valid backups)
wal archive min/max (18): none present
```

That state is not a CP02 failure. It proves the stanza/repository foundation exists while backup and WAL work remain deliberately unstarted.

Therefore the truthful status is:

```text
PostgreSQL 18.6                    LOCAL PASS
pgBackRest source/config           LOCAL PASS
pgBackRest 2.59.1 foundation       LOCAL PASS
stanza-create                      LOCAL PASS
pgBackRest info                    LOCAL PASS
continuous WAL archive             SELECTED / NOT IMPLEMENTED
pgBackRest check                   NOT RUN / CP03 OWNED
full backup                        NOT RUN
AWS S3 recovery repository         SELECTED / NOT ACTIVATED
S3 Versioning                      SELECTED / NOT ACTIVATED
Object Lock GOVERNANCE             SELECTED / NOT ACTIVATED
restore rehearsal                  NOT RUN
PITR rehearsal                     NOT RUN
SC-031 destructive recovery proof  NOT RUN
SC-011 anti-resurrection proof      NOT RUN
```

### 4.2 Accepted production recovery target

Accepted Physical target:

```text
POSTGRESQL BACKUP
pgBackRest 2.59.0 baseline
→ AWS S3 Standard eu-south-1
→ Versioning
→ Object Lock GOVERNANCE
→ finite policy-bound retention
```

Recovery copies remain non-canonical.

`Object Lock COMPLIANCE` is not the default because irreversible retention must not defeat privacy/deletion obligations.

### 4.3 Activation-time version rule

pgBackRest `2.59.1` is the maintenance release selected for the implementation. External evidence identified the exact Debian 13/Trixie PGDG package `2.59.1-1.pgdg13+1`; CP02 then directly proved a clean local image build, exact CLI version, PostgreSQL 18.6 interoperability and stanza/repository initialization.

Therefore `2.59.1` is ratified as the implementation maintenance pin for this workstream. This does **not** silently rewrite historical Physical Model evidence that selected `2.59.0`; durable architecture/current-state documentation is reconciled at the appropriate integration boundary.

Decision result:

```text
2.59.1 clean build                         PASS
exact version assertion                    PASS
PostgreSQL 18.6 foundation interoperability PASS
stanza/repository foundation               PASS
→ implementation maintenance refresh RATIFIED
```

### 4.4 CP01 recovery-contract freeze

CP01 is frozen:

```text
PostgreSQL major/patch        18.6
PGDATA                        /var/lib/postgresql/18/docker
implementation pgBackRest     2.59.1 exact PGDG pin
stanza                        dante
local repository              POSIX / dedicated Docker named volume
repository path               /var/lib/pgbackrest
config path                   /etc/pgbackrest/pgbackrest.conf
secrets                       none in pgBackRest local config
AWS                           deferred / not activated
initial backup hypothesis     continuous WAL + daily FULL
RPO/RTO                       measured later; no invented targets
SC-011                        OPEN HARD GATE
```

The pgBackRest `check` command is explicitly owned by CP03 rather than CP02 because a meaningful `check` validates the archive path and forces WAL/archive interaction. CP02 proves the foundation only: build/version, configuration readability, repository/stanza creation and PostgreSQL readiness without claiming WAL health.

---

## 5. Recovery objectives

The workstream closes only when DANTE can demonstrate, not merely describe:

```text
1. reproducible pgBackRest installation/configuration
2. valid stanza/repository health
3. continuous WAL archiving
4. usable physical backup
5. destructive or fresh-target restore
6. deterministic PITR
7. negative-path behavior under recovery failures
8. semantic verification after restore
9. anti-resurrection handling for later deletion/redaction state
10. measured recovery timing/data-loss behavior
11. operator-grade runbook from dead database to reopened traffic
12. direct remote acceptance on the selected AWS S3 topology before production-recovery PASS
```

No evidence may be promoted from `DESIGNED` to `PASS` without the relevant executable artifact/output.

---

## 6. RPO / RTO contract

No numeric production RPO/RTO is frozen at branch start.

Rules:

```text
RPO desired value != observed recoverability
RTO desired value != measured restoration duration
```

CP01 defines measurement semantics and business questions. Later recovery rehearsals record actual values. A production target may only be ratified after workload/backup/WAL characteristics are measurable enough to make the number meaningful.

Required measurements include at minimum:

```text
last archived WAL position / archive freshness
backup age
backup duration
restore duration
WAL replay duration
semantic verification duration
operator critical-path duration
actual recoverable target
actual data-loss window in the exercised scenario
```

---

## 7. Initial backup-policy hypothesis

DANTE favors maximum correctness with minimum unjustified operational complexity.

Initial operational hypothesis:

```text
continuous WAL archiving
+
daily FULL physical backup
```

This is a hypothesis to validate, not an irreversible production policy. At current project scale it minimizes backup-chain and restore-chain complexity.

Differential/incremental capability may be exercised in QA without being enabled in the default schedule. The policy should evolve only when measured database size, full-backup duration, WAL volume, storage cost or restore time justify the additional chain complexity.

Retention must be co-designed with S3 Versioning/Object Lock behavior and directly tested; apparent lifecycle expiration must not be mistaken for deletion of a still-retained protected version.

---

## 8. Local vs remote proof boundary

### LOCAL deterministic harness

Versioned local recovery topology:

```text
base compose     infra/compose/local.yaml
recovery overlay infra/compose/postgres-recovery.override.yaml
project          dante-postgres-recovery
host port        127.0.0.1:55432
PostgreSQL 18.6
+ pgBackRest 2.59.1
+ separate POSIX repository volume
→ backup
→ WAL archive
→ destructive/fresh restore
→ PITR
→ failure injection
```

The POSIX repository is test infrastructure only. It is not a second selected production recovery architecture.

Local proof exists to make recovery deterministic, cheap and repeatable. Recovery commands must include the dedicated project name and overlay so the ordinary `dante-local`/observability runtime is not targeted.

### REMOTE selected-stack acceptance

Before production-recovery PASS:

```text
real AWS S3 eu-south-1
+ Versioning
+ Object Lock GOVERNANCE
+ actual scoped credentials
+ backup
+ WAL archive
+ restore / PITR
+ retention / access behavior checks
```

MinIO/LocalStack/local POSIX evidence must never be mislabeled as direct AWS S3 acceptance.

No paid cloud resource or production IaC system is activated by this bootstrap.

---

## 9. Security and credential model

Configuration and secrets are separate.

Never commit:

```text
AWS access keys
secret keys
session credentials
repository encryption passphrases
PostgreSQL passwords
raw recovery secrets
private bucket policy credentials
```

Remote acceptance should prefer narrowly scoped, temporary/role-derived AWS credentials when the deployment environment supports them.

Object Lock GOVERNANCE posture:

```text
normal backup identity
→ minimum required repository read/write/list permissions
→ NO s3:BypassGovernanceRetention

break-glass/admin identity
→ separately controlled
→ bypass capability only if operationally required
```

This boundary must be proven against the final remote topology rather than assumed from configuration text.

---

## 10. Restore strategy

Default acceptance strategy is restoration into a clean, isolated PostgreSQL 18.6 target or destructive replacement of an explicitly disposable test target.

Recovery test must not depend on preserving the original live `PGDATA`.

Minimum post-restore verification:

```text
server version
expected extensions
Alembic head
schema/catalog topology
critical roles/ACL expectations
representative canonical data
constraints/routines/triggers required by current DB authority
application readiness boundary
semantic verification suite
```

Traffic must remain closed until recovery verification and required reconciliation steps finish.

---

## 11. PITR acceptance model

Use a deterministic scenario, not an imprecise sleep-and-clock test.

Preferred automated scenario:

```text
physical backup
→ write A
→ create named restore point / deterministic recovery marker
→ force/confirm WAL archival
→ write B
→ destroy/isolate source target
→ restore to marker
→ assert A is present
→ assert B is absent
→ run semantic verification
```

A wall-clock recovery-target test may also be retained as additional evidence, but the primary automated proof should minimize timing flakiness.

---

## 12. Mandatory validation gates

This workstream inherits the accepted post-selection validations, including:

```text
SC-031  destructive backup/restore operational verification
SC-011  old-backup anti-resurrection
PSV-31  primary object-loss recovery from object backup where applicable
PSV-32  database restore + object-backup reconciliation
PSV-34  backup access/audit + finite retention
PSV-40  pgBackRest archive/restore/PITR rehearsal
```

The PostgreSQL recovery branch directly owns the PostgreSQL side of these gates and must preserve explicit boundaries with any later R2/object recovery work.

---

## 13. Anti-resurrection hard gate

This is intentionally unresolved at bootstrap and may not be hand-waved.

Failure model:

```text
T0 backup contains sensitive/currently-visible state X
T1 accepted later deletion/redaction D1 removes or restricts X
T2 disaster destroys canonical database
T3 operator restores T0
```

A byte-correct restore can physically reintroduce X. DANTE must not silently treat X as permitted current truth again.

Accepted required recovery sequence remains conceptually:

```text
restore canonical PostgreSQL under accepted recovery procedure
→ apply/verify deletion-redaction suppression / anti-resurrection state
→ verify canonical semantic state
→ rebuild/discard stale derived sync/search/vector state
→ reconcile object-backup state
→ only then reopen affected traffic
```

At workstream start there is no accepted concrete implementation for a post-backup deletion/redaction suppression source that survives independently enough to reconcile an older restore.

Therefore:

```text
ANTI-RESURRECTION DESIGN      OPEN HARD GATE
SC-011                        NOT PASS
```

Do not invent a generic ledger, external canonical store or second database merely to close the checklist. CP01/CP06 must derive the narrowest truthful mechanism consistent with PostgreSQL remaining canonical and with DANTE deletion/redaction semantics.

---

## 14. Checkpoint model

```text
CP01  Recovery Contract / Bootstrap                         CONTRACT FROZEN
CP02  pgBackRest Foundation                                 LOCAL PASS
CP03  Continuous WAL + Backup                               NOT STARTED
CP04  Destructive / Isolated Restore                        NOT STARTED
CP05  Deterministic PITR                                    NOT STARTED
CP06  Failure Injection + Semantic Recovery / Anti-Resurrection  NOT STARTED
CP07  Whole Recovery QA + Runbook + Closure                 NOT STARTED
```

Detailed sequencing and evidence gates live in `postgres-recovery-execution-plan.md`.

Each checkpoint must end with:

```text
implementation delta
+ direct evidence
+ explicit NOT-PROVEN list
+ docs reconciliation
+ safe next action
```

---

## 15. Evidence-state vocabulary

Use only truthful states:

```text
SELECTED      accepted architectural target
DESIGNED      contract/approach written, not materialized
IMPLEMENTED   source/config exists
LOCAL PASS    direct local selected-substitute evidence exists
REMOTE PASS   direct remote selected-stack evidence exists
CLOSED        required implementation + evidence + documentation closure complete
DEFERRED      intentionally outside current boundary
BLOCKED       cannot truthfully advance without a missing prerequisite
```

Never collapse these states into a generic `done`.

---

## 16. Documentation lifecycle

During the active branch:

```text
postgres-recovery.md
→ durable workstream record

postgres-recovery-execution-plan.md
→ durable execution/evidence plan while active

postgres-recovery-live-handoff-2026-08-29.md
→ temporary branch/session continuation artifact
```

Before protected-main integration:

```text
current recovery truth
→ durable current architecture / operations / database docs

accepted evidence
→ durable QA/recovery validation record

useful branch narrative
→ optional single consolidated history record

live handoff
→ REMOVE after knowledge-coverage audit
```

`PROJECT-STATUS.md` and `ROADMAP.md` remain protected-main current truth and are updated at the appropriate integration/closure boundary, not used as a branch diary.

---

## 17. Current state

```text
branch created from protected main            YES
recovery worktree assigned                     YES
CP01 recovery contract frozen                 YES
runtime recovery source/config changed        YES
versioned recovery compose overlay            YES
pgBackRest exact source pin                    LOCAL PASS
pgBackRest locally installed/executed          LOCAL PASS
stanza-create                                  LOCAL PASS
pgBackRest info                                LOCAL PASS
pgBackRest check                               NOT RUN / CP03 OWNED
WAL archive enabled                            NO
full backup                                    NOT RUN
AWS resources created                         NO
AWS credentials committed                     NO
restore rehearsal                             NO
PITR rehearsal                                NO
anti-resurrection mechanism frozen            NO
SC-011 PASS                                   NO
SC-031 PASS                                   NO
runbook accepted                              NO
```

**Next safe action:** fast-forward the dedicated recovery worktree to the current branch HEAD, validate the versioned `infra/compose/postgres-recovery.override.yaml` resolves to the same isolated runtime contract, then define and approve a new exact CP03 write gate for `archive_mode`, pgBackRest `archive-push`, full `pgbackrest check`, WAL evidence and the first FULL backup. Do not enable WAL archiving without that new gate.