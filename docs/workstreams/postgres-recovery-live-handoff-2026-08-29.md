# DANTE — PostgreSQL Recovery Live Handoff — 2026-08-29

- **Status:** CURRENT LIVE HANDOFF / CP01 ACTIVE / RUNTIME NOT YET MODIFIED
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/postgres-recovery`
- **Created from protected `main`:** `baa9aba52932a0fa09b957ee7668aeb459fb4a20`
- **Latest checkpoint before this handoff:** `f02337c20878973698d7f30e7ce249ccf198dd4f`
- **Checkpoint message:** `docs(recovery): define recovery execution plan`
- **Local worktree:** NOT ASSIGNED; an additional user worktree is currently occupied by another branch
- **Current macro-checkpoint:** CP01 — Recovery Contract / Bootstrap
- **Runtime recovery implementation:** NOT STARTED

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
13. `infra/compose/local.yaml`

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

### Documentation/bootstrap created

```text
docs/workstreams/postgres-recovery.md

docs/workstreams/postgres-recovery-execution-plan.md

docs/workstreams/postgres-recovery-live-handoff-2026-08-29.md
```

The workstream record freezes authority, boundaries, evidence vocabulary, selected-vs-implemented truth, local/remote acceptance boundary, provisional backup-policy hypothesis, recovery semantics, SC-011 hard gate and documentation lifecycle.

The execution plan defines CP01–CP07 with explicit implementation/evidence/closure conditions.

---

## 4. Current runtime truth

At branch start the real local PostgreSQL surface is:

```text
PostgreSQL image     18.6-trixie
PostGIS              installed/pinned
pgvector             installed/pinned
persistent volume    yes
pg_stat_statements   enabled in local compose
pgBackRest           NOT installed/configured
stanza               NONE
archive_mode         not activated for this workstream
archive_command      no pgBackRest archive-push
recovery repository  NONE
restore harness      NONE
PITR harness         NONE
AWS S3               NOT ACTIVATED
```

No runtime file under `infra/`, `apps/`, migrations or database schema has been modified by the recovery workstream yet.

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

Current maintenance candidate:

```text
pgBackRest 2.59.1
```

Do not silently change the accepted pin. CP01/CP02 must directly prove the maintenance refresh is appropriate before ratifying it in durable current authority.

---

## 6. Current recovery status matrix

```text
PostgreSQL 18.6                  IMPLEMENTED
pgBackRest                       SELECTED / NOT IMPLEMENTED
continuous WAL                   SELECTED / NOT IMPLEMENTED
local POSIX recovery harness     DESIGNED / NOT IMPLEMENTED
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
CP01  Recovery Contract / Bootstrap                  ACTIVE
CP02  pgBackRest Foundation                          NOT STARTED
CP03  Continuous WAL + Backup                        NOT STARTED
CP04  Destructive / Isolated Restore                 NOT STARTED
CP05  Deterministic PITR                             NOT STARTED
CP06  Failure Injection + Semantic Recovery          NOT STARTED
CP07  Whole Recovery QA + Runbook + Closure          NOT STARTED
```

Do not skip directly to AWS or a production bucket. Deterministic local proof comes first; real AWS selected-stack acceptance comes before final production-recovery PASS.

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

Do not choose Terraform/OpenTofu merely because a bucket may later be needed. Production IaC remains a separate production-boundary decision unless explicitly activated.

---

## 11. What was intentionally NOT changed

```text
infra/local/postgres/
infra/compose/
apps/backend/
apps/web/
Alembic migrations
DANTE database schema
PostgreSQL roles/ACLs
PostgreSQL runtime settings
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

Finish CP01 before runtime writes.

The next technical read/write sequence is:

```text
1. obtain/bind a safe free local worktree for feature/postgres-recovery
2. inspect package/build constraints of postgres:18.6-trixie
3. directly revalidate pgBackRest 2.59.1 vs accepted 2.59.0 baseline
4. freeze exact local POSIX repository layout
5. freeze config/secrets/ownership paths
6. freeze pgBackRest stanza name and command topology
7. define exact CP02 write gate
8. install/configure pgBackRest foundation only
9. prove version + stanza-create + check
10. update this handoff with observed evidence
```

Do not enable WAL archiving in the same uncontrolled edit if CP02 foundation has not first been proven.

---

## 13. Expected CP02 write boundary

Exact paths must be verified against the free local worktree before authorization. Likely scope is narrowly within:

```text
infra/local/postgres/
infra/compose/
possibly one recovery-specific config/script/test directory after confirming repo conventions
recovery workstream docs
```

Explicitly not expected in CP02:

```text
business/domain migrations
application API changes
frontend changes
Auth changes
new canonical stores
AWS activation
PITR implementation
anti-resurrection persistence implementation
```

---

## 14. Handoff discipline

At every meaningful checkpoint update this file with:

```text
exact HEAD
what changed
what direct commands/tests ran
what PASS means
what remains NOT PROVEN
new blockers/risks
next safe action
```

When the workstream is ready for protected-main integration, consolidate durable truth/evidence and delete this temporary handoff after documentation knowledge coverage is verified.