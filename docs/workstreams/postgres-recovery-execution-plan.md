# DANTE — PostgreSQL Recovery Execution Plan

- **Status:** CURRENT EXECUTION PLAN / CP06 FINAL LOCAL QA
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
local POSIX proof != AWS proof
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
CP06 Failure + Semantic Recovery          IMPLEMENTED / FINAL LOCAL QA
   ├── failure matrix                     versioned / rerun pending
   ├── MaterialState retirement           materialized
   ├── suppression ledger                 materialized
   ├── SC-011 definitive harness          versioned / rerun pending
   ├── derived-state reopen boundary      defined
   └── object-store reopen boundary       defined
   ↓
CP07 Whole Recovery QA + Runbook          NOT STARTED
   ├── whole operator rehearsal
   ├── measured end-to-end evidence
   ├── real AWS selected-stack acceptance
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
AWS selected topology          S3 Standard eu-south-1 + Versioning + Object Lock GOVERNANCE
AWS activation                 deferred
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

Prototype/direct execution already proved all seven cases. The versioned final harness must still be run on the exact final CP06 HEAD.

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

The earlier mechanism prototype already proved the architecture end-to-end. Final SC-011 PASS requires this versioned implementation/rehearsal to pass.

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
[ ] local branch == remote branch / clean worktree
[ ] Python/Bash syntax checks PASS
[ ] fresh DB -> 20260830_09 PASS
[ ] downgrade 20260830_09 -> 20260826_08 -> head PASS
[ ] Alembic check PASS
[ ] current topology PASS
[ ] current catalog / Dictionary / mappings reconciliation PASS
[ ] all five retirement-facet integration tests PASS
[ ] retirement append-only / ACL / reinsertion negative tests PASS
[ ] suppression-ledger unit tests PASS
[ ] required backend quality/static checks PASS
[ ] versioned CP06 failure matrix PASS
[ ] definitive versioned SC-011 rehearsal PASS
[ ] real repository non-interference PASS
[ ] current documentation audit PASS
```

Current state:

```text
CP06 IMPLEMENTED / FINAL LOCAL QA PENDING
SC-011 NOT FINAL PASS
```

## 9. CP07 — Whole Recovery QA + Runbook + Closure

CP07 starts only after CP06 is actually closed.

Required whole flow:

```text
healthy PostgreSQL
→ continuous WAL + usable backup
→ simulated complete DB loss
→ repository/credentials identified
→ clean PostgreSQL target
→ restore/PITR
→ PostgreSQL promotion/readiness
→ current structural/security verification
→ anti-resurrection reconciliation
→ derived/object reopen gates
→ application readiness decision
```

Production selected-stack acceptance additionally requires real:

```text
AWS S3 Standard eu-south-1
Versioning
Object Lock GOVERNANCE
finite retention
scoped backup identity
real backup objects
real WAL objects
real restore/PITR readback
```

CP07 also captures measured:

```text
backup duration/size
WAL archive freshness
physical restore duration
PITR replay duration
semantic reconciliation duration
operator end-to-end recovery duration
actual recovery-point/data-loss window
```

No production numeric RPO/RTO value is invented before measured evidence.

## 10. CP07 closure bar

```text
[ ] CP01–CP06 evidence reconciled
[ ] whole LOCAL rehearsal PASS
[ ] SC-011 retained PASS
[ ] real selected AWS topology PASS
[ ] security/retention/Object Lock checks PASS
[ ] object/derived recovery gates operator-usable
[ ] measured recovery evidence captured
[ ] operator runbook rehearsal PASS
[ ] current durable docs aligned
[ ] no recovery secret committed
[ ] no unrelated capability activated
```

Only then may the PostgreSQL recovery workstream be integration-ready/closed.