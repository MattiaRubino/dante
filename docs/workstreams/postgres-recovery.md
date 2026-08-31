# DANTE — PostgreSQL Recovery Workstream

- **Status:** LOCAL RECOVERY WORKSTREAM CLOSED / CP07 LOCAL PASS / REPRODUCIBILITY HARDENING IMPLEMENTED / EXACT-HEAD REPROOF PENDING
- **Repository:** `MattiaRubino/dante`
- **Closure branch:** `feature/postgres-recovery` — phase-time integration candidate, not a runtime requirement
- **Closure worktree:** `/home/mattia/projects/dante-postgres-recovery` — phase-time only
- **PostgreSQL:** 18.6
- **Current DANTE Alembic head on this branch:** `20260830_09`
- **Current DANTE topology:** `69|5|15|76|97|69|123|0|0|0`
- **pgBackRest:** 2.59.1 / PGDG `2.59.1-1.pgdg13+1`
- **Current checkpoint:** CP07 Whole Local Recovery QA + Operator Runbook — LOCAL PASS / CLOSED
- **Execution plan:** `postgres-recovery-execution-plan.md`

> Repository truth beats conversation memory. PostgreSQL remains the sole canonical DANTE persistence authority. Backup/restore tooling, suppression evidence and derived stores do not become alternate canonical truth.

---

## 1. Integration and reusable execution boundary

The workstream is locally closed. `feature/postgres-recovery` and `/home/mattia/projects/dante-postgres-recovery` identify the phase-time integration candidate only; they are not permanent execution requirements.

Permanent recovery entry points:

```text
bootstrap  infra/local/postgres/recovery/bootstrap-local-recovery.sh
runner     infra/local/postgres/recovery/cp07-whole-recovery-rehearsal.sh
runbook    docs/operations/postgres-recovery-runbook.md
```

Both executable entry points are branch-agnostic and fail closed unless the current branch is attached, clean, has a configured upstream and `HEAD == upstream` after fetch. This allows the same repository procedure to remain valid after merge and feature-branch deletion.

Before writes or integration, repository engineering safety and the explicit Git write gate remain binding.

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
local POSIX proof != remote/cloud production proof
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

## 5. Future remote-provider boundary

No remote backup provider is selected or activated in the current project phase.

```text
remote backup provider      TBD
remote provider activated   NO
production/cloud recovery   NOT CLAIMED
```

Future provider selection is capability-driven: pgBackRest-compatible recovery, durable remote storage, appropriate versioning/immutability, finite retention, least-privilege credentials, required residency properties, backup/WAL readback and real restore/PITR proof.

## 6. Current checkpoint matrix

```text
CP01 Recovery Contract / Bootstrap      CLOSED / CONTRACT FROZEN
CP02 pgBackRest Foundation              LOCAL PASS
CP03 Continuous WAL + Backup            LOCAL PASS
CP04 Destructive / Isolated Restore     LOCAL PASS
SC-031 destructive restore              PASS
CP05 Deterministic PITR                 LOCAL PASS
PSV-40 local archive/restore/PITR       PASS
CP06 Failure Injection + Semantic       LOCAL PASS / CLOSED
Failure Matrix versioned final harness  LOCAL PASS
SC-011 mechanism prototype              LOCAL PASS
SC-011 versioned implementation         MATERIALIZED
SC-011 definitive versioned harness     LOCAL PASS
CP07 Whole Recovery QA + Runbook        LOCAL PASS / CLOSED
remote-provider production acceptance           NOT RUN
```

CP06 direct local proof completed on implementation/runtime head `a1a6323210b3d7af66284006a754759fa9d08028`. The documentation-only closure commit intentionally has a later SHA.

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

The versioned final failure matrix passed against implementation/runtime head `a1a6323210b3d7af66284006a754759fa9d08028` with N1–N7 all fail-closed and the real pgBackRest repository, retained CP05 target and Git worktree unchanged.

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
missing/unavailable `records/` directory
unexpected entry inside `records/`
duplicate MaterialStateRef suppression target
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

The definitive versioned harness passed against implementation/runtime head `a1a6323210b3d7af66284006a754759fa9d08028`. It proved physical resurrection of protected X from old B0 while isolated, committed-ledger reconciliation before reopen, payload reinsertion rejection, NativeRef/MaterialStateRef/current-history continuity, SELECT-only retirement ACL and non-interference with the real pgBackRest repository, retained CP05 target and Git worktree.

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

CP06 local acceptance is complete.

```text
[x] exact branch/worktree alignment
[x] migration fresh -> head PASS
[x] 20260830_09 -> 20260826_08 -> 20260830_09 PASS
[x] Alembic check PASS
[x] current topology exact PASS
[x] Dictionary ↔ SQLAlchemy ↔ PostgreSQL PASS
[x] retirement ACL/integrity tests PASS
[x] all five material facets retirement tests PASS
[x] suppression-ledger unit tests PASS
[x] Ruff/static checks required by backend PASS
[x] versioned CP06 failure matrix PASS
[x] versioned definitive SC-011 destructive rehearsal PASS
[x] real pgBackRest repository non-interference PASS
[x] CP05 target non-interference PASS
[x] current documentation reconciled
```

## CP06 local acceptance evidence

Implementation/runtime proof head:

```text
a1a6323210b3d7af66284006a754759fa9d08028
```

The later closure commit is documentation-only, so its Git SHA is expected to differ from the implementation/runtime proof head above.

Directly exercised local evidence:

```text
suppression-ledger unit tests             11/11 PASS
targeted database acceptance              17/17 PASS
whole database regression                 80/80 PASS
whole backend test suite                 128/128 PASS
Ruff format/check                         PASS
mypy strict                               PASS
versioned CP06 failure matrix N1-N7       PASS
definitive versioned SC-011               PASS
old B0 physical resurrection of X         PROVEN
ledger reconciliation before reopen       PASS
payload reinsertion after retirement      REJECTED
NativeRef continuity                      PASS
MaterialStateRef continuity               PASS
current/history continuity                PASS
runtime retirement ACL SELECT-only        PASS
real pgBackRest repository non-interference PASS
retained CP05 target non-interference     PASS
Git worktree non-interference             PASS
SC-011 readback/teardown clean             PASS
```

Current checkpoint truth:

```text
CP06 = LOCAL PASS / CLOSED
SC-011 = PASS
CP07 = LOCAL PASS / CLOSED
remote backup provider = TBD / NOT ACTIVATED
```

CP06 local closure does not prove production/cloud recovery, production RPO/RTO, remote object-store recovery, PowerSync/search/vector recovery implementation or the CP07 integrated operator rehearsal.

## 15. CP07 — whole local recovery QA + operator runbook

CP07 owns one integrated, disposable, operator-grade local rehearsal:

```text
healthy current PostgreSQL
→ verified FULL + continuous WAL
→ deterministic restore point
→ later writes + canonical retirement
→ independently durable suppression evidence
→ complete disposable PGDATA loss
→ clean B0 restore + PITR
→ promotion/readiness
→ deterministic A-present / B-absent proof
→ physical resurrection of old protected X
→ ledger-driven anti-resurrection reconciliation
→ structural/security/runtime acceptance
→ database-local reopen decision
→ measured evidence
→ complete disposable cleanup
```

Versioned harness:

```text
infra/local/postgres/recovery/cp07-whole-recovery-rehearsal.sh
```

Operator runbook:

```text
docs/operations/postgres-recovery-runbook.md
```

Closure requires:

```text
[x] exact implementation HEAD proven
[x] whole backend QA PASS on the implementation tree
[x] whole CP07 rehearsal PASS
[x] database-local reopen PASS
[x] anti-resurrection retained PASS
[x] deterministic PITR A-present / B-absent PASS
[x] measured local evidence captured
[x] ordinary local volumes untouched
[x] retained recovery repository untouched
[x] retained CP05 target untouched
[x] disposable CP07 resources fully cleaned
[x] operator runbook reconciled with executable flow
[x] remote backup provider remains TBD / not activated
[x] no production/cloud recovery claim
```

### CP07 initial exact local evidence

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


When this checklist is directly proven, the PostgreSQL recovery workstream may close **for the current LOCAL project phase**. Remote-provider production recovery remains a future deployment checkpoint, not an unfinished CP07 item.


## 16. Post-closure reproducibility hardening

The closed recovery behavior is not being semantically redesigned. This hardening makes the already-proven LOCAL procedure self-contained for a fresh clone after machine prerequisites exist:

```text
branch-agnostic Git/upstream gate
idempotent ignored LOCAL-secret bootstrap
no overwrite of existing non-empty secrets
0600 secret mode
Compose validation
repository-built pinned recovery image
CP07 automatic bootstrap
same disposable backup/WAL/PITR/anti-resurrection/reopen proof
```

No migration, mapping, Dictionary, suppression-ledger or Domain/Logical/Physical semantic change belongs to this hardening.

Exact-head proof remains unearned until the hardened implementation commit is pushed and CP07 is rerun on that exact remote HEAD.

<!-- RECOVERY-REPRODUCIBILITY-PROOF: PENDING -->
