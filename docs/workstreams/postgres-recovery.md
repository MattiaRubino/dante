# DANTE — PostgreSQL Recovery Workstream

- **Status:** ACTIVE / CP01 RECOVERY CONTRACT
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/postgres-recovery`
- **Created from protected `main`:** `baa9aba52932a0fa09b957ee7668aeb459fb4a20`
- **Local worktree:** NOT ASSIGNED; do not reuse an occupied worktree
- **Current PostgreSQL:** 18.6
- **Accepted recovery technology baseline:** pgBackRest 2.59.0 + AWS S3 Standard `eu-south-1` + Versioning + Object Lock GOVERNANCE
- **Activation-time maintenance candidate:** pgBackRest 2.59.1; requires direct compatibility/reproducibility evidence before the branch changes the accepted version pin
- **Current macro-checkpoint:** CP01 — Recovery Contract / Bootstrap
- **Live handoff:** `postgres-recovery-live-handoff-2026-08-29.md`
- **Execution plan:** `postgres-recovery-execution-plan.md`

> Repository truth beats conversation memory. This workstream activates the recovery capability already selected by the accepted Physical Model. It does not reopen CP6, does not create a second canonical database, and does not treat a backup copy as accepted application truth.

---

## 1. Mandatory continuation boundary

Continue exactly:

```text
repo:   MattiaRubino/dante
branch: feature/postgres-recovery
base:   baa9aba52932a0fa09b957ee7668aeb459fb4a20
```

A local worktree is intentionally not assigned yet because the user has another new worktree occupied by a different branch. Do not steal, detach, reset, rebase, or repurpose an occupied worktree. Before local runtime work, first verify the available worktree topology and explicitly bind this branch to a safe path.

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

### 4.1 Current implementation at branch creation

Current local PostgreSQL materialization is PostgreSQL 18.6 with PostGIS/pgvector and persistent Docker storage. It has no pgBackRest package/configuration, no pgBackRest stanza, no continuous archive command, no recovery harness and no directly proven PITR path.

Therefore the truthful current status is:

```text
PostgreSQL 18.6                    IMPLEMENTED
pgBackRest                         SELECTED / NOT IMPLEMENTED
continuous WAL archive             SELECTED / NOT IMPLEMENTED
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

pgBackRest `2.59.1` is the current maintenance candidate identified at workstream start. This branch must not silently replace the accepted `2.59.0` baseline. CP01/CP02 must produce direct evidence that the maintenance refresh is compatible with PostgreSQL 18.6, repository format expectations and the intended recovery workflow before the durable version pin is changed.

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

Permitted test topology:

```text
PostgreSQL 18.6
+ pgBackRest
+ temporary/local POSIX repository
→ backup
→ WAL archive
→ destructive/fresh restore
→ PITR
→ failure injection
```

The POSIX repository is test infrastructure only. It is not a second selected production recovery architecture.

Local proof exists to make recovery deterministic, cheap and repeatable.

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
CP01  Recovery Contract / Bootstrap
CP02  pgBackRest Foundation
CP03  Continuous WAL + Backup
CP04  Destructive / Isolated Restore
CP05  Deterministic PITR
CP06  Failure Injection + Semantic Recovery / Anti-Resurrection
CP07  Whole Recovery QA + Runbook + Closure
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

## 17. Current state at bootstrap

```text
branch created from protected main            YES
runtime recovery code/config changed          NO
pgBackRest installed                          NO
WAL archive enabled                           NO
local recovery proof                          NO
AWS resources created                         NO
AWS credentials committed                     NO
restore rehearsal                             NO
PITR rehearsal                                NO
anti-resurrection mechanism frozen            NO
SC-011 PASS                                   NO
SC-031 PASS                                   NO
runbook accepted                              NO
```

**Next safe action:** complete CP01 architecture/recovery contract readback and version/security/test-topology freeze, then enter CP02 with a bounded infrastructure write gate.