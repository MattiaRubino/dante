# DANTE — PostgreSQL Recovery Workstream

- **Status:** ACTIVE / CP06 IMPLEMENTED / FINAL LOCAL QA PENDING
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/postgres-recovery`
- **Worktree:** `/home/mattia/projects/dante-postgres-recovery`
- **PostgreSQL:** 18.6
- **Current DANTE Alembic head on this branch:** `20260830_09`
- **Current DANTE topology:** `69|5|15|76|97|69|123|0|0|0`
- **pgBackRest:** 2.59.1 / PGDG `2.59.1-1.pgdg13+1`
- **Current checkpoint:** CP06 Failure Injection + Semantic Recovery / Anti-Resurrection — implementation materialized, final versioned proof pending
- **Execution plan:** `postgres-recovery-execution-plan.md`
- **Live continuation:** `postgres-recovery-live-handoff-2026-08-29.md`

> Repository truth beats conversation memory. PostgreSQL remains the sole canonical DANTE persistence authority. Backup/restore tooling, suppression evidence and derived stores do not become alternate canonical truth.

---

## 1. Continuation boundary

Continue only on:

```text
branch     feature/postgres-recovery
worktree   /home/mattia/projects/dante-postgres-recovery
```

Do not detach/reset/rebase another occupied DANTE worktree. Never write directly to protected `main`.

Before local proof:

```bash
pwd
git status --short --branch
git rev-parse HEAD
git rev-parse origin/feature/postgres-recovery
git rev-parse origin/main
git worktree list --porcelain
```

Local proof requires local HEAD == remote branch HEAD and a clean worktree.

## 2. Authority / read order

1. `docs/PROJECT-STATUS.md`
2. `docs/ROADMAP.md`
3. this file
4. `postgres-recovery-execution-plan.md`
5. `docs/database/README.md`
6. `docs/database/dante-postgresql-database.md`
7. `docs/database/dante-postgresql-database-part-19.md`
8. accepted Domain / Logical / Physical recovery semantics
9. `docs/development/agent-operating-manual.md`
10. current recovery source under `infra/local/postgres/` and `infra/compose/`

The recovery workstream activates accepted capability; it does not reinterpret closed Domain/Logical semantics.

## 3. Recovery constitution

Permanent constraints:

```text
PostgreSQL = sole canonical persistence + material-history authority
backup repository != canonical truth
restored bytes != automatically accepted current semantic truth
successful backup != successful restore
successful restore != successful PITR
successful PITR != semantic recovery PASS
pg_isready != traffic-open proof
restore != permission to resurrect later-retired payload
selected != implemented != directly proven
local POSIX proof != AWS selected-stack proof
```

DANTE semantic invariants remain active during recovery, including:

```text
planned/intended != Actual
Observation != Actual
Evidence != Provenance
absence != false
canonical != provider state
NativeRef / MaterialStateRef non-reuse
retention/redaction/tombstone integrity
non-interference / inference-leakage obligations
```

## 4. Current local recovery topology

```text
PostgreSQL base image            postgres:18.6-trixie pinned by digest
PGDATA                           /var/lib/postgresql/18/docker
persistent PostgreSQL root       /var/lib/postgresql
pgBackRest package               2.59.1-1.pgdg13+1
pgBackRest CLI                   2.59.1
stanza                           dante
LOCAL repository type            POSIX
LOCAL repository path            /var/lib/pgbackrest
LOCAL full retention             repo1-retention-full=2
Compose project                  dante-postgres-recovery
recovery image                   dante-postgres-recovery:18.6-pgbackrest-2.59.1
host port                        127.0.0.1:55432
PostgreSQL volume                dante-postgres-recovery_postgres-data
pgBackRest volume                dante-postgres-recovery_pgbackrest-repository
archive_mode source              on
archive_command                  /usr/bin/pgbackrest --stanza=dante archive-push %p
wal_level                        replica
archive_library                  unset
```

`repo1-retention-full=2` is only a deterministic LOCAL harness policy.

## 5. Selected production target

```text
pgBackRest
→ AWS S3 Standard eu-south-1
→ S3 Versioning
→ Object Lock GOVERNANCE
→ finite policy-bound retention
```

Production activation is **not yet implemented or directly proven**.

Normal backup identity must remain scoped and must not have ordinary `s3:BypassGovernanceRetention`. Governance bypass, if ever required, belongs to separate break-glass administration.

## 6. Current checkpoint matrix

```text
CP01 Recovery Contract / Bootstrap      CLOSED / CONTRACT FROZEN
CP02 pgBackRest Foundation              LOCAL PASS
CP03 Continuous WAL + Backup            LOCAL PASS
CP04 Destructive / Isolated Restore     LOCAL PASS
SC-031 destructive restore              PASS
CP05 Deterministic PITR                 LOCAL PASS
PSV-40 local archive/restore/PITR       PASS
CP06 Failure Injection + Semantic       IMPLEMENTED / FINAL LOCAL QA PENDING
Failure Matrix prototype/direct proof   LOCAL PASS CANDIDATE
SC-011 mechanism prototype              LOCAL PASS CANDIDATE
SC-011 versioned implementation         MATERIALIZED
SC-011 definitive versioned harness     IMPLEMENTED / NOT YET RUN
CP07 Whole Recovery QA + Runbook        NOT STARTED
AWS selected-stack acceptance           NOT RUN
```

CP06 is not closed until direct proof runs on the exact current branch HEAD.

## 7. Retained direct CP02–CP05 evidence

### CP02

```text
exact pgBackRest package/CLI             PASS
PostgreSQL 18.6                          PASS
PGDATA path                              PASS
config/repository permissions            PASS
stanza-create/info metadata              PASS
ordinary LOCAL non-interference          PASS
```

### CP03

```text
archive_mode/archive_command             PASS
forced WAL archival                      PASS
physical WAL repository artifact         PASS
pgBackRest check                         PASS
FULL backup                              PASS
LOCAL retention behavior                 PASS
archive failure visibility/retry         PASS
```

Versioned negative archive harness:

`infra/local/postgres/recovery/archive-failure-recovery-check.sh`

### CP04

Direct destructive restore proved:

```text
semantic DANTE source materialized       PASS
canonical UUIDv7 fixture                 PASS
source PGDATA volume deleted             PASS
pgBackRest repository preserved          PASS
exact-set restore                        PASS
PostgreSQL 18.6 boot                     PASS
pg_is_in_recovery=false                  PASS
owners/roles/ACL/extensions              PASS
runtime login/read path                  PASS
```

A PostgreSQL 18 restore-parent permission defect was found and corrected narrowly:

```text
chown postgres:postgres /var/lib/postgresql/18
chmod 0700 /var/lib/postgresql/18
```

Do not replace this with recursive ownership mutation.

Current reusable CP04 harnesses now materialize and accept the **current branch database head**, not the pre-recovery database shape:

```text
infra/local/postgres/recovery/cp04-materialize-backup.sh
infra/local/postgres/recovery/cp04-destructive-restore-check.sh
```

### CP05

Direct PITR proof used:

```text
base FULL            20260830-132540F
source timeline      2
restore point        dante_cp05_20260830T140906Z_19757_R1
restore WAL          000000020000000000000016
A_REF                01a05300-a55e-7845-a710-69387408d147
B_REF                01a05300-a5c0-7d08-a608-74ac9d821817
```

After destructive PGDATA replacement and named-target recovery:

```text
BASELINE present                       PASS
A present                              PASS
B absent                               PASS
promotion to a new timeline            PASS
repository metadata unchanged          PASS
```

Direct LOCAL timing observations from that exercised dataset:

```text
pgBackRest physical restore        7.530 s
replay start -> target             0.263121 s
recovery start -> ready            0.539736 s
target -> ready                    0.276615 s
```

These are observations, not production RPO/RTO targets.

Current reusable CP05 destructive harness now accepts the current `20260830_09` database contract when a fresh current CP04 source/scenario is prepared.

## 8. CP06 failure-injection evidence

Direct disposable failure work has already demonstrated:

```text
N1 wrong stanza                         PASS
N2 empty/unavailable repository         PASS
N3 invalid backup set                   PASS
N4 impossible PITR target fail-closed   PASS
N5 missing required WAL fail-closed     PASS
N6 corrupted cloned backup artifact     PASS
N7 bootable stale DB rejected           PASS
real pgBackRest repository unchanged    PASS
CP05 target unchanged                   PASS
```

Important finding:

PostgreSQL may report readiness for **read-only connections** during recovery and later terminate because a configured target/WAL cannot be reached.

Therefore:

```text
pg_isready == success
```

is not sufficient to reopen application traffic.

Versioned definitive failure matrix:

`infra/local/postgres/recovery/cp06-failure-matrix-check.sh`

It is implemented but must still be rerun from the exact final CP06 HEAD before closure.

## 9. SC-011 canonical retirement model

The current branch materializes:

```text
Alembic 20260830_09
dante.material_state_retirement
dante.enforce_material_state_retirement()
```

Current database topology becomes:

```text
69 tables
5 views
15 routines
76 triggers
97 indexes
69 FKs
123 CHECKs
0 enum/domain
0 sequences/materialized/partitioned/RLS
```

Retirement is append-only and runtime has SELECT only.

Supported materialized facets:

```text
schedule.placement
actual.realization
session.timing
routine.recurrence
event.recurrence
```

For retired state:

```text
MaterialStateRef address/envelope remains
permitted current/history remains
explicit retirement reason/time remains
protected payload/selectors must be absent
later payload reinsertion rejects
```

The existing Schedule/Actual/Session/Recurrence validators are retirement-aware.

## 10. External recovery suppression ledger

The suppression ledger exists because an old backup may predate the canonical PostgreSQL tombstone.

It is independent from:

```text
canonical PGDATA
pgBackRest database backup repository
```

It is not a second canonical datastore.

Versioned protocol:

```text
PREPARED durable intent
→ canonical DB retirement/redaction commit
→ canonical DB read-back verification
→ COMMITTED marker bound to PREPARED SHA-256
```

Recovery blocks on:

```text
PREPARED without COMMITTED
COMMITTED without PREPARED
identity/target mismatch
prepared hash mismatch
non-canonical/invalid record
```

Suppression evidence retention must cover the complete resurrection horizon: it may not expire while any retained database/WAL/object version could still reintroduce the protected payload.

## 11. SC-011 direct prototype evidence

The disposable mechanism prototype directly proved:

```text
real Session + MaterialState + protected X      PASS
old B0 contains X                               PASS
accepted retirement removes X                   PASS
NativeRef continuity                            PASS
MaterialStateRef continuity                     PASS
current/history continuity                      PASS
PGDATA destruction                              PASS
B0 + independent ledger survive                 PASS
old B0 physically resurrects X                  PROVEN
restored target isolated                        PASS
ledger reconciliation removes resurrected X     PASS
runtime sees tombstone, not X                   PASS
NativeRef reuse rejected                        PASS
real pgBackRest repository untouched            PASS
CP05 target untouched                           PASS
```

This proved the architecture. It did not by itself prove the versioned final implementation.

Definitive versioned harness:

`infra/local/postgres/recovery/cp06-sc011-anti-resurrection-check.sh`

The definitive harness upgrades its disposable source to `20260830_09`, creates B0 on that real schema, uses the versioned Python PREPARED/COMMITTED ledger implementation, destroys only disposable PGDATA, proves physical resurrection and performs reconciliation using the real migration/integrity contract.

It is implemented but not yet executed against the exact final CP06 HEAD.

## 12. Derived-state reconciliation boundary

Derived/search/vector/sync state is non-canonical.

After database recovery:

```text
stale derived state must never override PostgreSQL
```

Any disposable derived state that can reflect retired/recovered payload must be discarded/rebuilt from accepted PostgreSQL or independently reconciled before that capability is reopened.

Current CP06 boundary:

```text
PostgreSQL semantic recovery can close locally
while provider-specific derived-store implementation remains deferred
provided traffic/feature reopen explicitly blocks on rebuild/reconciliation
```

PowerSync/search/vector activation is not introduced by this branch.

## 13. Object-store reconciliation boundary

A PostgreSQL restore does not prove R2/object availability or consistency.

Current recovery rule:

```text
DB row/reference restored
!=
referenced object proven recoverable/current
```

Full R2 backup/recovery implementation is deferred, but operator recovery must keep object-backed features closed until referenced object state is verified/reconciled.

The database recovery path must never manufacture object consistency by deleting/rewriting canonical references merely because object recovery is incomplete.

## 14. CP06 closure contract

Before CP06 may become `LOCAL PASS / CLOSED`:

```text
[ ] exact branch/worktree alignment
[ ] migration fresh -> head PASS
[ ] 20260830_09 -> 20260826_08 -> 20260830_09 PASS
[ ] Alembic check PASS
[ ] current topology exact PASS
[ ] Dictionary ↔ SQLAlchemy ↔ PostgreSQL PASS
[ ] retirement ACL/integrity tests PASS
[ ] all five material facets retirement tests PASS
[ ] suppression-ledger unit tests PASS
[ ] Ruff/static checks required by backend PASS
[ ] versioned CP06 failure matrix PASS
[ ] versioned definitive SC-011 destructive rehearsal PASS
[ ] real pgBackRest repository non-interference PASS
[ ] CP05 target non-interference PASS where retained
[ ] current documentation reconciled
```

Until then:

```text
CP06 IMPLEMENTED / FINAL LOCAL QA PENDING
SC-011 NOT YET FINAL PASS
```

## 15. CP07 next boundary

CP07 will own:

```text
whole clean operator-grade recovery rehearsal
measured end-to-end recovery evidence
operator runbook
real AWS selected-stack activation/acceptance
Versioning/Object Lock/security/retention proof
selected-cloud backup/WAL/restore/PITR readback
object/derived reopen procedures
final recovery workstream closure/integration
```

Do not start AWS activation without its own explicit implementation/write gate.