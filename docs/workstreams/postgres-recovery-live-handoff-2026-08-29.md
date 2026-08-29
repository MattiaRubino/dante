# DANTE — PostgreSQL Recovery Live Handoff — 2026-08-29

- **Status:** CURRENT LIVE HANDOFF / CP02 SOURCE IMPLEMENTED / LOCAL PROOF PENDING
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/postgres-recovery`
- **Created from protected `main`:** `baa9aba52932a0fa09b957ee7668aeb459fb4a20`
- **Latest validated checkpoint before this handoff update:** `1edc0d66d049797120a684e967fd78454b546c59`
- **Checkpoint message:** `docs(recovery): align CP02 and CP03 proof boundaries`
- **Local worktree:** NOT ASSIGNED; an additional user worktree is currently occupied by another branch
- **Current macro-checkpoint:** CP02 — pgBackRest Foundation
- **Runtime source/config:** IMPLEMENTED
- **Runtime execution evidence:** NOT YET RUN

> This file is the temporary continuation checkpoint for the active recovery branch. Repository truth beats conversation memory. It must be removed/consolidated before protected-main integration under the documentation lifecycle policy.

---

## 1. Continue exactly here

```text
repo:   MattiaRubino/dante
branch: feature/postgres-recovery
base:   baa9aba52932a0fa09b957ee7668aeb459fb4a20
```

Do not assume a local worktree path from old conversations. The user created another worktree, but it is presently being used by a different branch. Do not detach/reset/reassign it.

Before local work:

```bash
pwd
git status --short --branch
git rev-parse HEAD
git rev-parse origin/feature/postgres-recovery
git rev-parse origin/main
git worktree list --porcelain
```

Then bind this branch only to a safe free worktree.

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
14. `infra/compose/local.yaml`

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

Frozen enough to enter runtime proof:

```text
PostgreSQL                   18.6
base image                   postgres:18.6-trixie pinned by digest
PGDATA                       /var/lib/postgresql/18/docker
accepted pgBackRest baseline 2.59.0
activation implementation    2.59.1
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

The accepted Physical Model baseline is not silently rewritten from 2.59.0 merely because source now attempts 2.59.1. Runtime proof is still required before maintenance refresh ratification.

### CP02 source materialization

Changed recovery runtime paths:

```text
infra/local/postgres/Dockerfile
infra/local/postgres/pgbackrest/pgbackrest.conf
infra/compose/local.yaml
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

The recovery repository is intentionally separate from the PostgreSQL data volume so a later destructive `PGDATA` scenario does not delete the recovery source at the same time.

---

## 4. Current runtime truth

Current source/config state:

```text
PostgreSQL image             18.6-trixie / pinned digest
PostGIS                      installed/pinned
pgvector                     installed/pinned
PostgreSQL persistent volume yes
pg_stat_statements           enabled in local compose
pgBackRest source            IMPLEMENTED / exact 2.59.1 package pin
pgBackRest runtime install   NOT YET DIRECTLY PROVEN
pgBackRest config            IMPLEMENTED
stanza-create                NOT RUN
pgBackRest info              NOT RUN
archive_mode                 NOT activated for this workstream
archive_command              no pgBackRest archive-push yet
WAL archive proof            NONE
recovery repository source   IMPLEMENTED as separate named volume
recovery repository runtime  NOT YET DIRECTLY PROVEN
restore harness              NONE
PITR harness                 NONE
AWS S3                       NOT ACTIVATED
```

Important distinction:

```text
source/config IMPLEMENTED
!= image build PASS
!= stanza PASS
!= WAL archive PASS
!= backup PASS
!= recovery PASS
```

---

## 5. Recovery architecture carried forward

Accepted production target remains conceptually:

```text
PostgreSQL backup
pgBackRest 2.59.0 accepted baseline
→ AWS S3 Standard eu-south-1
→ Versioning
→ Object Lock GOVERNANCE
→ finite policy-bound retention
```

Activation implementation candidate:

```text
pgBackRest 2.59.1
PGDG Debian 13/Trixie package 2.59.1-1.pgdg13+1
```

Source is pinned to the candidate. Direct build/runtime evidence decides whether the maintenance refresh is ratified for implementation.

---

## 6. Current recovery status matrix

```text
PostgreSQL 18.6                  IMPLEMENTED
CP01 contract                    FROZEN
pgBackRest source/config         IMPLEMENTED / LOCAL PROOF PENDING
pgBackRest 2.59.1 runtime        NOT PROVEN
stanza-create                    NOT RUN
pgBackRest info                  NOT RUN
continuous WAL                   SELECTED / NOT IMPLEMENTED
local POSIX repository topology  IMPLEMENTED IN SOURCE / RUNTIME NOT PROVEN
full backup proof                NOT RUN
fresh/destructive restore        NOT RUN
PITR                             NOT RUN
AWS S3 repository                SELECTED / NOT ACTIVATED
S3 Versioning                    SELECTED / NOT ACTIVATED
Object Lock GOVERNANCE           SELECTED / NOT ACTIVATED
retention behavior               NOT PROVEN
RPO/RTO measurements             NONE
SC-031                           NOT RUN
SC-011                           OPEN HARD GATE / NOT RUN
operator runbook                 NOT IMPLEMENTED
```

Never shorten this to `recovery started = done`.

---

## 7. Frozen execution order

```text
CP01  Recovery Contract / Bootstrap                  CONTRACT FROZEN
CP02  pgBackRest Foundation                          IMPLEMENTED / LOCAL PROOF PENDING
CP03  Continuous WAL + Backup                        NOT STARTED
CP04  Destructive / Isolated Restore                 NOT STARTED
CP05  Deterministic PITR                             NOT STARTED
CP06  Failure Injection + Semantic Recovery          NOT STARTED
CP07  Whole Recovery QA + Runbook + Closure          NOT STARTED
```

Do not skip directly to AWS or a production bucket. Deterministic local proof comes first; real AWS selected-stack acceptance comes before final production-recovery PASS.

`pgbackrest check` is explicitly a **CP03** gate, not CP02, because a meaningful check validates WAL/archive integration and forces archive interaction. CP02 must not activate WAL merely to make `check` green.

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

The local POSIX pgBackRest config contains no credentials.

Do not choose Terraform/OpenTofu merely because a bucket may later be needed. Production IaC remains a separate production-boundary decision unless explicitly activated.

---

## 11. What was intentionally NOT changed

The current approved source scope did **not** modify:

```text
apps/backend/
apps/web/
Alembic migrations
DANTE database schema
PostgreSQL roles/ACLs
archive_mode
archive_command
WAL archive runtime configuration
backup scheduling
restore/PITR configuration
AWS resources
S3 buckets
secrets
PROJECT-STATUS.md
ROADMAP.md
protected main
other feature branches/worktrees
```

`PROJECT-STATUS.md` and `ROADMAP.md` remain protected-main truth and should be reconciled at the appropriate integration/closure boundary rather than used as a live branch diary.

---

## 12. Immediate next safe action

Run **CP02 local proof** before any CP03 write.

Required sequence once a safe local worktree is available:

```text
1. bind/fetch feature/postgres-recovery without rewriting history
2. verify local HEAD == origin/feature/postgres-recovery
3. build the local PostgreSQL image cleanly
4. start the current local PostgreSQL service
5. verify PostgreSQL readiness
6. verify `pgbackrest version` == `pgBackRest 2.59.1`
7. verify config ownership/readability as postgres
8. verify /var/lib/pgbackrest is writable by postgres and distinct from PGDATA
9. run `pgbackrest --stanza=dante stanza-create`
10. run `pgbackrest --stanza=dante info`
11. capture exact outputs
12. update workstream/handoff with observed evidence
```

Do **not** enable WAL archiving under the current gate.

Do **not** require a successful `pgbackrest check` in CP02. `check` becomes mandatory after `archive_mode` + `archive_command` are deliberately activated in CP03.

---

## 13. CP02 proof boundary

CP02 may become LOCAL PASS only if direct runtime evidence proves:

```text
clean image build                  PASS
exact pgBackRest version           PASS
PostgreSQL readiness               PASS
config permissions                 PASS
repository permissions             PASS
stanza-create                      PASS
info / stanza readability          PASS
existing local PostgreSQL behavior no regression observed
```

Even then the following remain NOT PROVEN:

```text
WAL archive
pgBackRest check
full backup
restore
PITR
AWS
Object Lock
SC-031
SC-011
```

CP03 requires a **new exact Git write gate** before archive settings or backup behavior are changed.

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