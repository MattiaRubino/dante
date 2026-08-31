# DANTE — PostgreSQL Recovery Execution Plan

- **Status:** CURRENT EXECUTION PLAN / CP07 LOCAL PASS / CLOSED / LOCAL RECOVERY CLOSED
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/postgres-recovery`
- **Primary workstream:** `postgres-recovery.md`
- **PostgreSQL:** 18.6
- **Current DANTE Alembic head:** `20260830_09`
- **Current topology:** `69|5|15|76|97|69|123|0|0|0`

> Proof precedes PASS. Current source files, tests, Dictionary and recovery harnesses must agree before a checkpoint is closed.

---

## 1. Execution principles

```text
correctness before convenience
proof before PASS
fresh/disposable recovery before risky in-place manipulation
configuration separate from secrets
real PostgreSQL evidence before database claims
restored bytes != accepted semantic state
pg_isready != traffic reopen
local POSIX proof != remote/cloud production proof
old backup restore != permission to resurrect later-retired data
```

## 2. Current checkpoint graph

```text
CP01 Recovery Contract / Bootstrap        CLOSED
   ↓
CP02 pgBackRest Foundation                LOCAL PASS
   ↓
CP03 Continuous WAL + Backup              LOCAL PASS
   ↓
CP04 Destructive / Isolated Restore       LOCAL PASS
   ↓
CP05 Deterministic PITR                   LOCAL PASS
   ↓
CP06 Failure + Semantic Recovery          LOCAL PASS / CLOSED
   ├── failure matrix                     VERSIONED LOCAL PASS
   ├── MaterialState retirement           materialized
   ├── suppression ledger                 materialized
   ├── SC-011 definitive harness          VERSIONED LOCAL PASS
   ├── derived-state reopen boundary      defined
   └── object-store reopen boundary       defined
   ↓
CP07 Whole Recovery QA + Runbook          LOCAL PASS / CLOSED
   ├── whole operator rehearsal
   ├── measured end-to-end evidence
   ├── provider-neutral local operator proof
   └── final integration closure
```

## 3. CP01 — Recovery Contract

Current frozen decisions:

```text
PostgreSQL                     18.6
PGDATA                         /var/lib/postgresql/18/docker
pgBackRest                     2.59.1
PGDG package                   2.59.1-1.pgdg13+1
stanza                         dante
LOCAL repo                     POSIX / dedicated volume
repo path                      /var/lib/pgbackrest
recovery Compose project       dante-postgres-recovery
recovery host port             127.0.0.1:55432
remote backup provider          TBD / capability-driven
remote-provider activation      deferred
numeric production RPO/RTO     not invented
```

State:

```text
CP01 CLOSED / CONTRACT FROZEN
```

## 4. CP02 — pgBackRest Foundation

Required foundation is directly proven:

```text
exact package/CLI                     PASS
PostgreSQL 18.6                       PASS
PGDATA path                           PASS
config/repository ownership           PASS
stanza-create                         PASS
pgBackRest info/repository metadata   PASS
LOCAL non-interference                PASS
```

State:

```text
CP02 LOCAL PASS
```

## 5. CP03 — Continuous WAL + Backup

Current recovery-source settings:

```text
archive_mode = on
archive_command = /usr/bin/pgbackrest --stanza=dante archive-push %p
archive_library = unset
wal_level = replica
repo1-retention-full = 2   # LOCAL harness only
```

Direct proof:

```text
forced WAL archive                        PASS
physical WAL artifact                     PASS
pgBackRest check                          PASS
FULL backup                               PASS
LOCAL retention/expire                    PASS
archive permission failure visible        PASS
same-WAL retry after repair               PASS
```

State:

```text
CP03 LOCAL PASS
```

## 6. CP04 — Destructive / Isolated Restore

Current reusable source path:

```text
infra/local/postgres/recovery/cp04-materialize-backup.sh
```

It now materializes/accepts the current database contract:

```text
Alembic          20260830_09
topology         69|5|15|76|97|69|123|0|0|0
retirement       dante.material_state_retirement present
runtime ACL      SELECT only on retirement table
```

Destructive harness:

```text
infra/local/postgres/recovery/cp04-destructive-restore-check.sh
```

Safety contract:

```text
delete only recovery PGDATA volume
preserve pgBackRest repository
manual DELETE_RECOVERY_PGDATA confirmation
isolated restored target archive_mode=off
require pg_is_in_recovery()=false
verify current head/topology/ACL/fixture/extensions
```

Retained direct destructive-restore evidence is PASS. Reusable current-head scripts must be rerun as part of later whole-recovery rehearsal when a new source set is required.

State:

```text
CP04 LOCAL PASS
SC-031 PASS
```

## 7. CP05 — Deterministic PITR

Current source/preparation path:

```text
infra/local/postgres/recovery/cp05-prepare-pitr-source.sh
infra/local/postgres/recovery/cp05-destructive-pitr-check.sh
```

The destructive PITR harness now requires the current database head/topology for newly prepared scenarios.

Required deterministic scenario:

```text
BASELINE exists before target
A committed before named restore point
named PostgreSQL restore point
B committed after target
complete WAL + timeline history archived
exact FULL restored
recovery_target_name exact
recovery_target_timeline exact
recovery_target_action=promote
A present after promotion
B absent after promotion
```

Retained direct PITR evidence is PASS, including promotion to a new timeline and measured replay/readiness observations.

State:

```text
CP05 LOCAL PASS
PSV-40 LOCAL PASS
```

## 8. CP06 — Failure Injection + Semantic Recovery

### Goal

Prove recovery fails safely/observably under representative faults and that an old backup cannot silently reintroduce payload that DANTE validly retired after the backup.

### 8.1 Failure matrix

Versioned harness:

```text
infra/local/postgres/recovery/cp06-failure-matrix-check.sh
```

Required cases:

```text
N1 wrong stanza/config
N2 empty/unavailable repository
N3 nonexistent recovery set
N4 impossible PITR target
N5 required WAL missing from disposable repository clone
N6 corrupted backup artifact in disposable repository clone
N7 physically bootable but stale semantic target
```

Acceptance for a negative case requires:

```text
safe failure
observable failure
diagnosable cause
no dangerous target accepted as recovered
real repository unchanged
```

Prototype/direct execution proved the mechanism, and the versioned final harness subsequently passed on implementation/runtime head `a1a6323210b3d7af66284006a754759fa9d08028` with all seven cases fail-closed.

### 8.2 MaterialState retirement

Migration:

```text
20260830_09_recovery_material_state_retirement.py
```

Adds:

```text
dante.material_state_retirement
dante.enforce_material_state_retirement()
```

Supported facets:

```text
schedule.placement
actual.realization
session.timing
routine.recurrence
event.recurrence
```

A committed retirement preserves the permitted envelope/reference/history while requiring protected payload/selectors to be absent.

Retirement is append-only; runtime receives SELECT only.

Existing Schedule/Actual/Session/Recurrence validators are retirement-aware and reject post-retirement payload resurrection.

### 8.3 Suppression ledger

Versioned implementation:

```text
apps/backend/src/dante/platform/recovery/suppression_ledger.py
infra/local/postgres/recovery/recovery-suppression-record-v1.schema.json
```

Protocol:

```text
PREPARED
→ canonical PostgreSQL retirement/redaction transaction
→ canonical DB read-back verification
→ COMMITTED(prepared_sha256)
```

Block recovery for any ambiguity/tamper:

```text
missing/unavailable `records/` directory
unexpected entry inside `records/`
duplicate MaterialStateRef suppression target
PREPARED without COMMITTED
COMMITTED without PREPARED
identity/target mismatch
prepared SHA mismatch
invalid/non-canonical JSON
```

The ledger is recovery-only evidence, never a second canonical database.

### 8.4 SC-011 definitive rehearsal

Versioned harness:

```text
infra/local/postgres/recovery/cp06-sc011-anti-resurrection-check.sh
```

Required sequence:

```text
current disposable source at 20260830_09
→ create real Session MaterialState + protected X
→ create B0 FULL containing X
→ write PREPARED
→ prove orphan PREPARED blocks
→ canonical retirement/redaction removes X
→ verify canonical retirement row
→ write COMMITTED
→ destroy only disposable PGDATA
→ preserve independent B0 repository + suppression ledger
→ restore exact B0
→ prove X physically resurrected while target isolated
→ load/verify committed suppression evidence
→ reconcile tombstone + remove X
→ prove envelope/history continuity
→ prove X cannot be reinserted
→ prove runtime ACL/current head/not-in-recovery
→ prove real pgBackRest repo + CP05 target + Git untouched
```

The earlier mechanism prototype proved the architecture end-to-end. The versioned implementation/rehearsal then passed on implementation/runtime head `a1a6323210b3d7af66284006a754759fa9d08028`, earning final local SC-011 PASS.

### 8.5 Derived-state boundary

Derived/search/vector/sync state is non-canonical.

Recovery acceptance rule:

```text
stale derived state never overrides restored PostgreSQL
```

A derived store that can expose affected state stays unavailable until discarded/rebuilt from accepted PostgreSQL or independently reconciled.

PowerSync/search/vector activation/implementation is not introduced here.

### 8.6 Object-store boundary

PostgreSQL restore does not prove R2/object consistency.

Object-backed capabilities stay closed until their referenced object state is verified/reconciled. Full object backup/recovery implementation remains a later recovery slice.

### 8.7 CP06 closure checklist

```text
[x] local branch == remote branch / clean worktree
[x] Python/Bash syntax checks PASS
[x] fresh DB -> 20260830_09 PASS
[x] downgrade 20260830_09 -> 20260826_08 -> head PASS
[x] Alembic check PASS
[x] current topology PASS
[x] current catalog / Dictionary / mappings reconciliation PASS
[x] all five retirement-facet integration tests PASS
[x] retirement append-only / ACL / reinsertion negative tests PASS
[x] suppression-ledger unit tests PASS
[x] required backend quality/static checks PASS
[x] versioned CP06 failure matrix PASS
[x] definitive versioned SC-011 rehearsal PASS
[x] real repository non-interference PASS
[x] current documentation audit PASS
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
CP07 = NEXT / NOT STARTED
remote backup provider = TBD / NOT ACTIVATED
```

This LOCAL closure does not prove remote/cloud production recovery, production RPO/RTO, remote object-store recovery, PowerSync/search/vector recovery implementation or the whole CP07 operator rehearsal.

## 9. CP07 — Whole Local Recovery QA + Runbook + Local Closure

CP07 is implemented as a **single integrated disposable rehearsal**, not as a wrapper that merely replays CP04/CP05/CP06 independently.

Versioned harness:

```text
infra/local/postgres/recovery/cp07-whole-recovery-rehearsal.sh
```

Runbook:

```text
docs/operations/postgres-recovery-runbook.md
```

Required exact flow:

```text
fresh healthy PostgreSQL 18.6
→ provisioning + Alembic 20260830_09
→ structural/security acceptance
→ real Session MaterialState + protected X
→ FULL B0 containing X
→ A commit
→ deterministic restore point R1
→ B commit after R1
→ PREPARED suppression
→ canonical retirement removes X
→ COMMITTED suppression after DB verification
→ final WAL archive verification
→ total disposable PGDATA loss
→ independent B0 repository + suppression ledger survive
→ exact B0 restore + named PITR to R1
→ promote
→ A present / B absent
→ X physically resurrected / tombstone absent
→ target remains isolated
→ committed-ledger reconciliation
→ tombstone present / X absent
→ payload reinsertion rejected
→ topology/owners/roles/ACL/extensions/runtime acceptance
→ database-local reopen PASS
→ disposable cleanup
```

Measured LOCAL observations required:

```text
backup duration + repository size
WAL archive freshness at disaster
restore-point age at disaster
physical restore duration
PITR replay-to-target
recovery-to-ready
semantic reconciliation
structural/security acceptance
PGDATA-loss → database-local-reopen
```

These are observations only, not production RPO/RTO targets.

### CP07 closure checklist

```text
[x] implementation tree passes Ruff / mypy / whole backend pytest
[x] pre-push disposable whole rehearsal PASS
[x] implementation commit pushed after proof
[x] exact pushed implementation HEAD whole rehearsal PASS
[x] ignored JSON evidence report valid
[x] database-local reopen PASS
[x] anti-resurrection reconciliation PASS
[x] deterministic A-present / B-absent PITR PASS
[x] non-interference PASS
[x] disposable cleanup PASS
[x] operator runbook reconciled
[x] current durable docs reconciled
[x] remote backup provider = TBD / NOT ACTIVATED
[x] production/cloud recovery = NOT CLAIMED
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


Remote-provider implementation is deliberately outside current CP07. A future provider must be selected and proven only when DANTE actually approaches production deployment.
