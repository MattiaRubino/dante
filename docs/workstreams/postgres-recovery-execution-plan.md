# DANTE — PostgreSQL Recovery Execution Plan

- **Status:** CURRENT EXECUTION PLAN / CP01 FROZEN / CP02 LOCAL PASS / CP03 LOCAL PASS / CP04 NOT STARTED
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
   └── anti-resurrection hard-gate statement
   ↓
CP02 pgBackRest Foundation
   │
   ├── exact reproducible package/version
   ├── config/secrets boundary
   ├── repository topology
   ├── stanza-create
   └── info / foundation readability
   ↓
CP03 Continuous WAL + Backup
   │
   ├── PostgreSQL archive settings
   ├── archive-push
   ├── pgBackRest check
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

## Frozen decisions

### Version

```text
PostgreSQL                  18.6
accepted pgBackRest baseline 2.59.0
activation implementation    2.59.1
PGDG package pin             2.59.1-1.pgdg13+1
```

The `2.59.1` package exists for Debian 13/Trixie, is pinned in source and has now passed the CP02 local foundation proof plus CP03 local WAL/backup proof. It is ratified as the implementation maintenance pin while the historical accepted Physical Model selection record remains reconciled at integration rather than silently rewritten in place.

No technology-selection reopening unless direct evidence invalidates the accepted choice.

### PostgreSQL image/data-path contract

```text
base image      postgres:18.6-trixie pinned by digest
PGDATA          /var/lib/postgresql/18/docker
persistent root /var/lib/postgresql
```

The PostgreSQL 18 image uses a version-specific `PGDATA`, so pgBackRest targets the exact nested path while Docker persists the parent `/var/lib/postgresql` volume.

### Local repository topology

```text
stanza                       dante
repo1-type                   posix
repo1-path                   /var/lib/pgbackrest
repository Docker volume     pgbackrest-repository
PostgreSQL Docker volume     postgres-data
recovery Compose project     dante-postgres-recovery
recovery host port           127.0.0.1:55432
recovery image               dante-postgres-recovery:18.6-pgbackrest-2.59.1
recovery overlay             infra/compose/postgres-recovery.override.yaml
```

The recovery repository is physically distinct from `PGDATA` so a destructive database-loss rehearsal can destroy/recreate PostgreSQL state without also destroying the recovery source. The dedicated Compose project/port/image prevent interference with the ordinary `dante-local`/observability runtime.

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

Frozen:

```text
no secrets in repository
minimum AWS repository permissions
no normal-role governance-retention bypass
separate break-glass administration
finite retention
```

Local pgBackRest configuration contains no credentials or secret material.

### Anti-resurrection

The problem remains an explicit hard gate. CP01 freezes the failure model and forbids fake closure; no new persistent subsystem is accepted merely to satisfy the checklist.

## CP01 evidence

```text
workstream record exists
execution plan exists
live handoff exists
current runtime inspected
accepted recovery authority reconciled
current pgBackRest maintenance release/package checked
implementation scope bounded
PGDATA/repository/config topology frozen
NOT-PROVEN list explicit
```

## CP01 close criteria

```text
[x] activation implementation version recorded
[x] package acquisition/pinning strategy identified
[x] local repository topology frozen
[x] production S3 contract frozen enough for later acceptance
[x] secret/config separation frozen
[x] RPO/RTO measurement semantics frozen
[x] anti-resurrection retained as explicit open hard gate without fake mechanism
[x] CP02 exact source/write/test scope defined
```

CP01 is contract-frozen. SC-011 itself is **not** closed by CP01 and remains owned by the later semantic recovery gate.

---

# 4. CP02 — pgBackRest Foundation

## Goal

Materialize pgBackRest reproducibly without yet claiming backup, WAL archive or recovery correctness.

## Implemented source surface

```text
infra/local/postgres/Dockerfile
infra/local/postgres/pgbackrest/pgbackrest.conf
infra/compose/local.yaml
infra/compose/postgres-recovery.override.yaml
```

No Alembic migration or application/domain schema change is involved.

## Required materialization

```text
exact pgBackRest version/package source
version assertion in image/build
pgBackRest configuration
repository path ownership/permissions
stanza name
secrets injected externally when later required
PostgreSQL path settings compatible with current image
recovery runtime isolated from ordinary LOCAL stack
```

Current source materializes:

```text
pgBackRest package             2.59.1-1.pgdg13+1
expected CLI                   pgBackRest 2.59.1
config                         /etc/pgbackrest/pgbackrest.conf
config ownership               root:postgres / 0640
stanza                         dante
pg1-path                       /var/lib/postgresql/18/docker
repo1-type                     posix
repo1-path                     /var/lib/pgbackrest
repository image ownership     postgres:postgres / 0750
repository volume              pgbackrest-repository:/var/lib/pgbackrest
recovery project               dante-postgres-recovery
recovery image                 dante-postgres-recovery:18.6-pgbackrest-2.59.1
recovery host port             127.0.0.1:55432
```

### Direct CP02 evidence

Observed in `/home/mattia/projects/dante-postgres-recovery`:

```text
clean Docker image build                            PASS
exact package/CLI assertion during build            PASS
container health                                    PASS
pgbackrest version == pgBackRest 2.59.1             PASS
PostgreSQL version == 18.6                          PASS
data_directory == /var/lib/postgresql/18/docker     PASS
config root:postgres 0640                           PASS
repository postgres:postgres 0750                   PASS
config readable by postgres                         PASS
repository writable by postgres                     PASS
PGDATA writable by postgres                         PASS
stanza-create                                       PASS
pgbackrest --stanza=dante info                      PASS
archive.info/archive.info.copy present              PASS
backup.info/backup.info.copy present                PASS
ordinary dante-local PostgreSQL remained healthy    PASS
ordinary Alloy remained healthy                     PASS
```

Expected `info` state at the CP02 boundary:

```text
stanza: dante
status: error (no valid backups)
cipher: none
wal archive min/max (18): none present
```

This was expected because CP02 intentionally contained no WAL archive and no backup.

### Why `pgbackrest check` is not a CP02 gate

A meaningful `pgbackrest check` validates repository/archive integration and forces PostgreSQL WAL/archive interaction. Continuous WAL archiving was deliberately not activated in CP02. Therefore:

```text
CP02 check requirement  = NONE
CP03 check requirement  = MANDATORY
```

A pre-WAL `check` failure must not be mislabeled as CP02 failure, and a syntactically configured but non-archiving system must not be mislabeled as recovery health.

## Quality gates

```text
[x] rebuild from clean image succeeds
[x] exact package/version assertion succeeds
[x] no credential material committed
[x] config ownership/permissions verified
[x] repository ownership/permissions verified
[x] stanza-create succeeds
[x] info reads the stanza/repository
[x] existing PostgreSQL readiness is not regressed
[x] recovery runtime isolated from ordinary LOCAL/observability runtime
```

Current state:

```text
CP02 LOCAL PASS
```

## CP02 NOT-PROVEN after success

```text
continuous WAL durability
pgBackRest archive check
usable full backup
restore
PITR
AWS S3 behavior
Object Lock
anti-resurrection
```

Those first three items were subsequently proven by CP03; restore/PITR/AWS/anti-resurrection remain open later gates.

---

# 5. CP03 — Continuous WAL + Backup

## Goal

Prove that PostgreSQL 18.6 continuously archives WAL through pgBackRest and that a physical full backup completes only with the required archive state.

## Source/config activation

The approved CP03 source scope is materialized in the isolated recovery harness only:

```text
infra/compose/postgres-recovery.override.yaml
infra/local/postgres/pgbackrest/pgbackrest.conf
```

Exact recovery-only PostgreSQL configuration:

```text
archive_mode = on
archive_command = /usr/bin/pgbackrest --stanza=dante archive-push %p
archive_library = unset
wal_level = replica (existing/inherited value; deliberately not overridden)
```

The override repeats the existing `shared_preload_libraries=pg_stat_statements` and `compute_query_id=on` command-line settings before adding the two archive settings so Compose command replacement cannot silently drop the established LOCAL PostgreSQL behavior.

The LOCAL POSIX pgBackRest repository configures:

```text
repo1-retention-full=2
```

This is a deterministic LOCAL test retention policy only. It is not the production AWS retention value and does not prove S3 Versioning, Object Lock or lifecycle behavior.

Current CP03 state:

```text
source/config activation       LOCAL PASS
runtime container recreation   LOCAL PASS
archive_mode runtime           LOCAL PASS
archive_command runtime        LOCAL PASS
continuous archive             LOCAL PASS
pgBackRest check               LOCAL PASS
full backup                    LOCAL PASS
retention behavior             LOCAL PASS
archive failure/retry          LOCAL PASS
```

## WAL proof

Directly observed:

```text
recovery PostgreSQL service recreated from current source
archive_mode=on
archive_command=/usr/bin/pgbackrest --stanza=dante archive-push %p
archive_library unset
wal_level=replica
initial pg_stat_archiver baseline clean
current WAL segment recorded
pg_switch_wal() executed
closed WAL archived successfully
pg_stat_archiver successful archive observed
compressed WAL artifact physically present in repository
pgbackrest --stanza=dante check exits successfully
```

The first forced segment observed in the repository was `000000010000000000000002`. Later backup/recovery activity advanced the retained archive range.

`pgbackrest check` belongs here because this is the first checkpoint where archive behavior is intentionally active and can be truthfully verified.

## Backup proof

Direct FULL backup evidence:

```text
first FULL backup       20260830-114043F
start/stop              2026-08-30 11:40:43+00 / 11:40:50+00
database size           38.2MB
repo1 backup set size   4.7MB
status                  PASS
```

Additional FULL backups were deliberately/redundantly generated while exercising retention. At the CP03 closure boundary the two retained FULL sets are:

```text
20260830-114411F
20260830-114419F
```

Final direct `pgbackrest info` after the archive-failure/recovery proof reported:

```text
stanza: dante
status: ok
wal archive min/max (18): 00000001000000000000000A/00000001000000000000000F
```

## Retention

The LOCAL policy `repo1-retention-full=2` was exercised directly rather than inferred from configuration text.

Observed behavior:

```text
multiple FULL backups completed
older full sets expired as new full sets crossed retention=2
explicit pgbackrest --stanza=dante expire completed successfully
exactly two current full backups remained
remaining WAL range advanced consistently with retained recovery sets
```

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

## Archive failure/recovery proof

A reusable copy of the directly executed failure/recovery test is versioned at:

```text
infra/local/postgres/recovery/archive-failure-recovery-check.sh
```

The direct run proved:

```text
archive directory owner/mode baseline     postgres:postgres 0750
target WAL                                00000001000000000000000E
injected archive-directory mode           0550
pg_stat_archiver failure became visible   PASS
last_failed_wal matched target WAL        PASS
repository mode restored                  0750
same WAL automatically retried            PASS
last_archived_wal matched target WAL      PASS
compressed target WAL physically present PASS
post-failure pgbackrest check             PASS
post-failure pgbackrest info status=ok    PASS
```

The harness restores the original archive-directory mode through a shell trap. `pg_stat_archiver` counters are not treated as persistent history because they can reset across PostgreSQL restart/statistics reset; repository artifacts plus pgBackRest `check`/`info` provide the durable evidence layer.

## CP03 close criteria

```text
[x] resolved archive settings direct PASS
[x] continuous archive observed directly
[x] forced/generated WAL found in repository
[x] pg_stat_archiver success evidence captured
[x] pgBackRest check direct PASS
[x] full backup direct PASS
[x] pgBackRest info usable
[x] local retention behavior exercised and recorded
[x] archive failure produces visible failure/degraded evidence
[x] recovery service PostgreSQL readiness/health preserved
[x] recovery isolation contract preserved; ordinary LOCAL source/runtime contract not modified
```

Current state:

```text
CP03 LOCAL PASS
```

CP03 does **not** prove restore, PITR, AWS S3 behavior, Object Lock, production retention, SC-031 or SC-011.

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

CP03 already proves one narrow archive-push failure/retry path. That evidence is retained, but it does not replace the broader CP06 failure matrix.

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

CP01 is contract-frozen, CP02 is **LOCAL PASS**, CP03 is **LOCAL PASS**, and CP04 is **NOT STARTED**.

Next safe technical sequence:

```text
1. fast-forward /home/mattia/projects/dante-postgres-recovery to the CP03 closure HEAD
2. confirm the two retained FULL backups and repository health still read correctly
3. preserve the recovery repository volume as the recovery source
4. derive an explicitly disposable/fresh PostgreSQL 18.6 restore target that cannot accidentally reuse source PGDATA
5. define the deterministic fixture/catalog/semantic evidence that must survive the restore
6. freeze exactly what PGDATA/container/volume may be destroyed and what recovery repository must not be destroyed
7. freeze the exact pgBackRest restore command and target topology
8. define and approve a new CP04 Git/runtime write gate
9. only after approval execute destructive/isolated restore
10. verify PostgreSQL startup plus catalog/schema/representative semantic state before considering SC-031
```

Do **not** enter PITR, AWS, production retention or anti-resurrection implementation under CP04. CP03 backup success is not restore proof.
