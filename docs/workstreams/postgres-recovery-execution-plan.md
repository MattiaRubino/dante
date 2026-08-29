# DANTE — PostgreSQL Recovery Execution Plan

- **Status:** CURRENT EXECUTION PLAN / CP01 ACTIVE
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/postgres-recovery`
- **Baseline:** `baa9aba52932a0fa09b957ee7668aeb459fb4a20`
- **Primary workstream record:** `postgres-recovery.md`
- **Purpose:** define the bounded, evidence-driven path from selected recovery architecture to directly proven PostgreSQL backup, WAL archive, restore, PITR and operator-grade recovery closure.

> This plan activates an already selected capability. It does not reopen CP6/database architecture, and it does not authorize unrelated production infrastructure.

---

## 1. Execution principles

The workstream follows these rules throughout:

```text
correctness before convenience
proof before PASS
fresh-target recovery before clever in-place recovery
deterministic tests before timing-sensitive tests
minimal operational complexity before elaborate backup chains
configuration separate from secrets
real PostgreSQL evidence before database correctness claims
real AWS S3 evidence before selected-cloud PASS
restore semantics before traffic reopen
```

Permanent anti-shortcut rules:

```text
backup created != backup usable
WAL uploaded != PITR usable
container starts != recovery PASS
local S3 emulator != AWS S3 proof
restored bytes != accepted semantic state
old backup restore != permission to resurrect later-deleted state
```

---

## 2. Dependency graph

```text
CP01 Recovery Contract / Bootstrap
   │
   ├── version/security/topology freeze
   ├── evidence vocabulary
   ├── RPO/RTO measurement contract
   └── anti-resurrection problem statement
   ↓
CP02 pgBackRest Foundation
   │
   ├── exact reproducible package/version
   ├── config/secrets boundary
   ├── repository topology
   ├── stanza-create
   └── pgBackRest check
   ↓
CP03 Continuous WAL + Backup
   │
   ├── PostgreSQL archive settings
   ├── archive-push
   ├── archive health
   ├── full backup
   └── retention behavior
   ↓
CP04 Destructive / Isolated Restore
   │
   ├── fresh/disposable target
   ├── restore from physical backup
   ├── PostgreSQL start
   └── semantic/catalog verification
   ↓
CP05 Deterministic PITR
   │
   ├── recovery marker
   ├── pre/post-marker writes
   ├── archived WAL completeness
   ├── target recovery
   └── exact state assertions
   ↓
CP06 Failure Injection + Semantic Recovery
   │
   ├── missing/unreachable repository
   ├── missing WAL
   ├── invalid credentials/config
   ├── unusable/partial recovery set
   ├── impossible target
   ├── SC-011 anti-resurrection
   └── derived/object reconciliation boundaries
   ↓
CP07 Whole Recovery QA + Runbook + Closure
   ├── clean end-to-end rehearsal
   ├── measured RPO/RTO
   ├── real AWS selected-stack acceptance
   ├── operator runbook
   ├── documentation lifecycle cleanup
   └── integration-ready closure
```

No later checkpoint may be declared closed merely because its source files exist.

---

# 3. CP01 — Recovery Contract / Bootstrap

## Goal

Freeze the exact problem, boundaries, evidence model and safe implementation path before touching PostgreSQL recovery settings.

## Required reads

```text
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/database/
accepted Physical Model
post-selection validation register
whole-database QA / CP6 closure material
docs/development/agent-operating-manual.md
documentation lifecycle policy
infra/local/postgres/
infra/compose/
```

## Decisions to freeze

### Version

```text
PostgreSQL        18.6
pgBackRest        accepted baseline 2.59.0
maintenance       2.59.1 candidate pending direct activation evidence
```

Expected decision rule:

```text
2.59.1 direct compatibility/reproducibility PASS
→ ratify maintenance refresh

material incompatibility or packaging/repository issue
→ retain 2.59.0 and document why
```

No technology-selection reopening unless direct evidence invalidates the accepted choice.

### Initial backup schedule

Provisional baseline:

```text
continuous WAL archive
+
daily FULL backup
```

Do not add differential/incremental scheduling until measurements justify it.

### Test topology

```text
LOCAL
→ PostgreSQL 18.6 + pgBackRest + disposable POSIX repository

REMOTE ACCEPTANCE
→ real AWS S3 eu-south-1 + Versioning + Object Lock GOVERNANCE
```

Local POSIX exists only for deterministic engineering proof.

### RPO/RTO

CP01 does not invent numeric production targets. It defines what is measured and where timestamps/LSNs/durations are captured.

### Security

Freeze:

```text
no secrets in repository
minimum AWS repository permissions
no normal-role governance-retention bypass
separate break-glass administration
finite retention
```

### Anti-resurrection

Keep the problem as an explicit hard gate. CP01 may derive candidate mechanisms, but no new persistent subsystem is accepted without semantic and operational justification.

## CP01 evidence

```text
workstream record exists
execution plan exists
live handoff exists
current runtime inspected
accepted recovery authority reconciled
external/current pgBackRest maintenance version checked
implementation scope bounded
NOT-PROVEN list explicit
```

## CP01 close criteria

```text
[ ] version activation decision recorded
[ ] package acquisition/pinning strategy identified
[ ] local repository topology frozen
[ ] production S3 contract frozen enough for later acceptance
[ ] secret/config separation frozen
[ ] RPO/RTO measurement semantics frozen
[ ] anti-resurrection candidate analysis recorded without fake closure
[ ] CP02 exact file/write/test scope defined
```

---

# 4. CP02 — pgBackRest Foundation

## Goal

Materialize pgBackRest reproducibly without yet claiming backup/recovery correctness.

## Likely implementation surface

Exact paths must be verified before write, but expected bounded areas are:

```text
infra/local/postgres/
infra/compose/
recovery-specific scripts/config under infra or development tooling
recovery tests/docs only
```

No Alembic migration or application/domain schema change is expected.

## Required materialization

```text
exact pgBackRest version/package source
version assertion in image/build
pgBackRest configuration file/template
repository path ownership/permissions
stanza name
log/spool paths if required
secrets injected externally
PostgreSQL path/socket settings compatible with current image
```

### Foundation commands/evidence

At minimum prove:

```text
pgbackrest version
pgbackrest --stanza=<dante> stanza-create
pgbackrest --stanza=<dante> check
```

`check` must succeed in the actual local topology intended for CP03. A binary being present is not sufficient.

## Quality gates

```text
rebuild from clean image succeeds
pin/version assertion succeeds
no credential material committed
container ownership/permissions explicit
configuration parse succeeds
stanza-create succeeds
check succeeds or expected pre-WAL limitation is explicitly understood and bounded
existing PostgreSQL readiness is not regressed
```

## CP02 NOT-PROVEN even after success

```text
continuous WAL durability
usable full backup
restore
PITR
AWS S3 behavior
Object Lock
anti-resurrection
```

---

# 5. CP03 — Continuous WAL + Backup

## Goal

Prove that PostgreSQL 18.6 continuously archives WAL through pgBackRest and that a physical full backup completes only with the required archive state.

## PostgreSQL settings

Expected concepts, exact values to be derived from current topology:

```text
archive_mode = on
archive_command = pgBackRest archive-push ...
wal_level compatible with current workload/recovery
```

If asynchronous archiving is justified for the final remote topology, configure it only with explicit spool ownership/durability behavior. Do not add `archive-async` merely because it exists.

## WAL proof

Deterministic evidence should include:

```text
force WAL switch or generate bounded WAL
confirm pgBackRest archive-push succeeds
confirm archived segment exists in repository
confirm pgBackRest check sees healthy archive path
record WAL/LSN marker useful for later recovery assertions
```

## Backup proof

Start with:

```text
pgbackrest --stanza=<dante> --type=full backup
```

Verify:

```text
backup completes
backup metadata/info lists expected set
required WAL archive completeness is satisfied
backup age/time recorded
repository integrity/check path passes
```

## Retention

Initial local retention exists to exercise expiry behavior without pretending it equals production object retention.

Production retention must later reconcile:

```text
pgBackRest retention
S3 Versioning
Object Lock GOVERNANCE
S3 lifecycle
privacy/deletion policy
storage growth
PITR continuity
```

Do not expire WAL so aggressively that remaining backups advertise recovery points requiring missing WAL.

## CP03 close criteria

```text
[ ] continuous archive observed directly
[ ] forced/generated WAL found in repository
[ ] full backup direct PASS
[ ] pgBackRest info/check usable
[ ] archive failure produces visible failure/degraded evidence
[ ] existing database tests/readiness not regressed
```

---

# 6. CP04 — Destructive / Isolated Restore

## Goal

Prove SC-031-class recovery from a real physical backup after the active/disposable source state is unavailable.

## Preferred topology

Use a brand-new PostgreSQL 18.6 target or a clearly disposable target whose `PGDATA` is destroyed before restore.

The test must not accidentally succeed because original data files remain mounted.

## Scenario

```text
seed deterministic canonical fixture
→ full backup
→ record backup metadata
→ destroy/isolate target PGDATA
→ initialize recovery target prerequisites only
→ pgBackRest restore
→ start PostgreSQL
→ run direct catalog + semantic verification
```

## Required post-restore verification

At minimum:

```text
PostgreSQL server version == expected 18.6 family
required extensions available
Alembic head == source backup expectation
schema objects/topology match expected source
critical roles/ACLs are valid for recovered deployment model
representative rows/checksums/fixtures match
critical constraints/routines/triggers available
application/backend can reach readiness boundary where appropriate
whole-database semantic smoke suite passes
```

The verification must be specific enough that an empty or partially restored cluster cannot accidentally pass.

## SC-031 state

Only after this checkpoint may SC-031 be considered for PASS, and only if the accepted exact deployment/version criteria are directly satisfied.

---

# 7. CP05 — Deterministic PITR

## Goal

Prove recovery to a selected point between two observable business/database states.

## Primary scenario

```text
1. create valid physical backup
2. write A and commit
3. create named PostgreSQL restore point R
4. force/confirm WAL containing R is archived
5. write B and commit
6. force/confirm later WAL archival
7. destroy/isolate recovery target
8. restore backup
9. configure recovery target = R
10. start recovery
11. promote/finish according to explicit target action
12. verify A exists
13. verify B does not exist
14. run semantic/catalog verification
```

Use a unique scenario identifier so stale data from an earlier run cannot satisfy assertions.

## Additional wall-clock test

A recovery-target-time scenario may be added as supplementary acceptance. It must avoid ambiguous timestamp boundaries and record UTC/offset semantics explicitly.

## PITR negative checks

```text
impossible target
missing required WAL
wrong recovery target configuration
repository unreachable during restore/replay
```

The system/test harness must fail loudly rather than silently booting an unintended current state.

## CP05 close criteria

```text
[ ] deterministic marker recovery PASS
[ ] A present
[ ] B absent
[ ] semantic verification PASS
[ ] required WAL chain proven
[ ] failure to satisfy target is visible and non-silent
[ ] measured replay/recovery timings recorded
```

---

# 8. CP06 — Failure Injection + Semantic Recovery

## Goal

Prove that the recovery process remains truthful under representative failures and that post-restore semantic obligations are enforceable before traffic reopens.

## Failure matrix

At minimum exercise:

```text
repository unavailable
bad/missing repository credentials where applicable
missing WAL segment
corrupted/unusable backup artifact if safely reproducible
wrong stanza/repository configuration
empty/destroyed PGDATA
impossible PITR target
operator starts from wrong recovery set / mismatch detection
```

A negative scenario passes when the system fails safely, observably and diagnosably—not when the command happens to return zero.

## SC-011 anti-resurrection

Required semantic scenario:

```text
T0 create state X
T1 backup B0
T2 accept later deletion/redaction D1 for X
T3 destroy canonical database
T4 restore B0
T5 apply accepted anti-resurrection/reconciliation procedure
T6 verify X does not silently return to a currently permitted state
T7 verify required tombstone/reference continuity remains truthful
T8 verify NativeRef identity is not reused
```

### Design constraint

The mechanism used at T5 must not casually create a second canonical application database. It must be recovery-bounded, explicitly authoritative for the narrow suppression/reconciliation fact it carries, auditable and compatible with accepted privacy/material-history semantics.

If no mechanism can satisfy those constraints, CP06 remains BLOCKED rather than inventing a fake PASS.

## Derived-state reconciliation

Where the selected system contains disposable projections/sync/search/vector state, recovery closure must define:

```text
which state is discarded
which state is rebuilt from PostgreSQL
what freshness/version marker proves rebuild completion
what remains unavailable until rebuild completes
```

Do not let a stale derived store override the restored canonical PostgreSQL state.

## Object backup reconciliation

The PostgreSQL workstream must define the contract boundary for reconciling database references to backed-up R2/object state. Full implementation may belong to a later object-recovery slice, but the DB recovery runbook cannot pretend the boundary does not exist.

---

# 9. CP07 — Whole Recovery QA + Runbook + Closure

## Goal

Turn the individually proven mechanisms into one repeatable operator recovery procedure and collect direct selected-stack evidence.

## Whole rehearsal

Target scenario:

```text
healthy PostgreSQL
→ continuous WAL + usable backup available
→ simulated complete database loss
→ operator starts with repository + documented credentials/identity path
→ clean PostgreSQL target prepared
→ restore or PITR executed
→ database starts
→ semantic verification runs
→ anti-resurrection/reconciliation runs where applicable
→ derived-state reconciliation gate runs
→ application readiness verified
→ traffic-reopen decision made
```

## Remote AWS acceptance

Before production recovery is marked PASS, repeat the relevant path against the selected remote topology:

```text
AWS S3 Standard eu-south-1
Versioning enabled
Object Lock GOVERNANCE configured
finite retention contract
scoped backup identity
no normal-role governance bypass
real backup objects
real WAL objects
real restore/PITR readback
```

Prove versioning/object-lock/lifecycle behavior directly enough to rule out a configuration that looks correct but permits unintended deletion or indefinite accumulation.

## Measured evidence

Capture:

```text
backup size
backup duration
WAL archive freshness/latency in exercised environment
restore duration
PITR WAL replay duration
semantic verification duration
end-to-end operator recovery duration
actual recovery point/data-loss window
```

These observations inform later production RPO/RTO target ratification.

## Runbook requirements

The runbook must be executable by an engineer who did not build the feature.

It must answer:

```text
How do I identify the correct stanza/repository?
How do I verify backup health before destroying anything else?
How do I prepare a fresh PostgreSQL 18.6 target?
How do I choose full restore vs PITR?
How do I choose/verify the PITR target?
How do I know required WAL exists?
How do I know recovery has completed rather than paused?
What exact semantic verification runs?
How is anti-resurrection/reconciliation applied?
What derived/object state must be rebuilt/reconciled?
What conditions keep traffic closed?
What is the break-glass path?
What evidence/logs are retained from the incident/rehearsal?
```

No step may require chat memory.

## Closure criteria

```text
[ ] CP01–CP06 evidence reconciled
[ ] local clean whole rehearsal PASS
[ ] direct AWS selected-stack acceptance PASS
[ ] SC-031 PASS
[ ] SC-011 PASS or explicitly blocks production recovery closure
[ ] measured timing/data-loss evidence captured
[ ] security/retention checks PASS
[ ] operator runbook direct rehearsal PASS
[ ] durable current docs updated
[ ] temporary live handoff removed after knowledge audit
[ ] PROJECT-STATUS / ROADMAP integration updates prepared
[ ] no recovery secret committed
[ ] no unrelated architecture activated
```

If SC-011 cannot be truthfully closed, the workstream may still retain valuable backup/restore/PITR engineering evidence but must not claim whole production recovery closure.

---

## 10. Test strategy

Use layered evidence rather than one giant brittle script.

### Static/config checks

```text
version pin assertions
configuration ownership/path checks
secret scanning
compose/build validation
shell/script lint where applicable
```

### Fast deterministic recovery tests

```text
stanza/config validation
repository path/permission validation
fixture helpers
metadata parsers/assertions
negative configuration cases
```

### Real PostgreSQL integration

```text
WAL archive
full backup
fresh restore
PITR
catalog verification
semantic fixtures
failure injection
```

### Remote acceptance

```text
real S3 bucket characteristics
real IAM/role behavior
real Versioning/Object Lock behavior
real repository read/write/archive
real restore/PITR
```

Do not use SQLite or mocked PostgreSQL behavior as correctness evidence for physical recovery.

---

## 11. CI boundary

Recovery tests are destructive and infrastructure-heavy. Do not blindly add the full suite to every normal backend test run.

Expected future split:

```text
fast/static recovery checks
→ normal CI candidate

local destructive PostgreSQL recovery suite
→ explicit marked/manual or dedicated CI job

real AWS recovery acceptance
→ controlled manual/scheduled/release-boundary job with scoped credentials
```

Exact CI activation belongs to the checkpoint where the runtime is stable enough to avoid creating a flaky permanent pipeline.

---

## 12. Change-control discipline

Before each checkpoint write:

```text
verify branch/worktree
verify HEAD vs origin
state exact files/directories allowed
state explicit exclusions
apply bounded change
run checkpoint-appropriate evidence
commit checkpoint
update workstream + live handoff truthfully
```

Do not mix unrelated frontend/backend/domain work into this branch.

Likely forbidden without a separate explicit gate:

```text
business schema redesign
new canonical data store
application feature work
Auth changes
Home/frontend changes
observability programme
production deployment redesign
Terraform/OpenTofu selection solely for this branch
R2 object-recovery implementation beyond the defined reconciliation contract
```

---

## 13. Current next action

CP01 remains active.

Next safe technical step:

```text
1. bind feature/postgres-recovery to a safe free local worktree when available
2. inspect exact PostgreSQL image/package acquisition constraints
3. revalidate pgBackRest 2.59.1 vs accepted 2.59.0 baseline
4. freeze local repository/config/secrets topology
5. define CP02 exact write gate
6. materialize pgBackRest foundation only
```

No runtime recovery setting should be changed before that bounded CP02 gate.