# DANTE — PostgreSQL Recovery Execution Plan

- **Status:** CURRENT EXECUTION PLAN / CP01 FROZEN / CP02 LOCAL PASS / CP03 LOCAL PASS / CP04 LOCAL PASS / CP05 NOT STARTED
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
PostgreSQL                    18.6
accepted pgBackRest baseline  2.59.0
activation implementation     2.59.1
PGDG package pin              2.59.1-1.pgdg13+1
```

The `2.59.1` package exists for Debian 13/Trixie, is pinned in source and has passed CP02 foundation, CP03 archive/backup and CP04 destructive-restore proof. It is ratified as the implementation maintenance pin while the historical accepted Physical Model selection record remains reconciled at integration rather than silently rewritten in place.

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

The first three items were subsequently proven by CP03 and restore was proven by CP04; PITR/AWS/anti-resurrection remain later gates.

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

## Backup proof

Direct FULL backup evidence:

```text
first FULL backup       20260830-114043F
start/stop              2026-08-30 11:40:43+00 / 11:40:50+00
database size           38.2MB
repo1 backup set size   4.7MB
status                  PASS
```

Additional FULL backups were deliberately/redundantly generated while exercising retention. At the CP03 closure boundary the two retained FULL sets were:

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

CP03 does **not** prove restore, PITR, AWS S3 behavior, Object Lock, production retention, SC-031 or SC-011. Restore/SC-031 were subsequently proven by CP04; the remaining items stay open.

---

# 6. CP04 — Destructive / Isolated Restore

## Goal

Prove SC-031-class recovery from a real physical backup after the active/disposable source state is unavailable.

## Proven topology

CP04 uses the dedicated recovery project only:

```text
PostgreSQL data volume     dante-postgres-recovery_postgres-data
pgBackRest repo volume     dante-postgres-recovery_pgbackrest-repository
semantic backup            20260830-132540F
canonical fixture          Person 01993f19-9c00-7000-8000-000000000001
verification target        dante-postgres-recovery-cp04-restore
archive_mode               off during isolated restore verification
```

The pgBackRest repository and PostgreSQL data volumes are distinct. Only the PostgreSQL data volume is disposable in this checkpoint.

## Semantic backup preparation

A preflight discovered that the CP03 backup sets contained only bootstrap PostgreSQL plus extensions: no `dante` schema, no Alembic relation and no DANTE application roles. That discovery does not invalidate CP03, whose scope was WAL/archive/physical-backup mechanics, but it prevents those backups from being used as semantic SC-031 proof.

The versioned materialization harness is:

```text
infra/local/postgres/recovery/cp04-materialize-backup.sh
```

It directly uses the accepted backend boundaries:

```text
P0 provisioning command
→ dante_owner / dante_migrator / dante_runtime
→ dante schema + security envelope
→ Alembic upgrade head as dante_migrator / SET ROLE dante_owner
→ P0 reconciliation
→ Alembic current/check
→ deterministic Person NativeRef fixture
→ catalog/owner/ACL/extension verification
→ pgBackRest check
→ dedicated FULL
```

Direct materialization evidence:

```text
uv                                            0.12.5
P0 provisioning                               PASS
Alembic upgrade                               PASS
P0 post-migration reconciliation              PASS
Alembic current                               20260826_08 (head)
Alembic check                                 no new upgrade operations
fixture UUID version                          7
fixture                                       01993f19-9c00-7000-8000-000000000001
topology                                      68|5|14|75|95|68|120|0|0|0
DANTE object owner                            dante_owner
DANTE role set                                owner/migrator/runtime
required extension set                        PASS
pgBackRest check                              PASS
```

Dedicated semantic FULL:

```text
label             20260830-132540F
start/stop        2026-08-30 13:25:40+00 / 13:26:24+00
wal start/stop    000000010000000000000011 / 000000010000000000000012
database size     40.6MB
repo set size     4.9MB
```

## Destructive restore scenario

The versioned destructive harness is:

```text
infra/local/postgres/recovery/cp04-destructive-restore-check.sh
```

The directly executed sequence was:

```text
verify exact semantic backup + fixture
→ hash pgBackRest backup.info
→ write unique marker outside PGDATA but inside PostgreSQL volume
→ manual DELETE_RECOVERY_PGDATA confirmation
→ stop/remove only recovery PostgreSQL service
→ delete dante-postgres-recovery_postgres-data
→ prove pgBackRest repository survives unchanged
→ recreate empty PostgreSQL volume without initdb
→ prove old source marker absent
→ restore exact set 20260830-132540F with --archive-mode=off
→ verify restored PG_VERSION
→ start isolated target
→ verify PostgreSQL/catalog/fixture/security/runtime path
```

pgBackRest restore direct output:

```text
restore backup set 20260830-132540F
recovery start reference 2026-08-30 13:25:40
updated postgresql.auto.conf
restored global/pg_control last
restore size 40.6MB
file total 1501
restore command completed successfully
```

## First-boot filesystem finding

The first restored startup failed after the restore itself had succeeded:

```text
mkdir: cannot create directory '/var/lib/postgresql/18': Permission denied
```

Direct inspection found:

```text
/var/lib/postgresql              postgres:postgres 1777
/var/lib/postgresql/18           root:root 0700
/var/lib/postgresql/18/docker    postgres:root 0700
```

The root restore process had created the PostgreSQL 18 version parent, and the official entrypoint could not traverse that parent after dropping privileges. This was a harness/filesystem-boundary defect, not a backup-data defect.

The exact proven correction is:

```text
chown postgres:postgres /var/lib/postgresql/18
chmod 0700 /var/lib/postgresql/18
```

The versioned destructive harness performs this normalization immediately after restore and before boot.

## Required post-restore verification — direct result

```text
[x] original PGDATA volume genuinely deleted/recreated
[x] source-volume marker absent after recreation/restore
[x] pgBackRest repository survives unchanged
[x] exact-set pgBackRest restore completes
[x] PostgreSQL starts from restored PGDATA
[x] server_version_num == 180006
[x] pg_is_in_recovery() == false
[x] isolated restore target archive_mode == off
[x] required extensions/version set restored
[x] Alembic head == 20260826_08
[x] exact schema/catalog topology == 68/5/14/75/95/68/120
[x] forbidden enum/domain + sequence/materialized/partitioned/RLS counts == 0
[x] DANTE object owner == dante_owner
[x] DANTE role set restored
[x] dante_runtime remains denied SELECT on dante.alembic_version
[x] deterministic canonical Person fixture restored exactly once
[x] real dante_runtime credential authenticates and reads restored fixture
```

## CP04 close criteria

```text
[x] semantic backup source is materially meaningful
[x] source PGDATA cannot survive the destructive rehearsal
[x] recovery repository survives independently
[x] restore target starts from restored bytes
[x] catalog/schema topology matches accepted source
[x] deterministic semantic fixture matches accepted source
[x] roles/ACL/runtime access path match accepted source
[x] filesystem restore/startup boundary is understood and repeatably handled
[x] SC-031 local destructive proof directly satisfied
```

Current state:

```text
CP04 LOCAL PASS
SC-031 LOCAL PASS
```

CP04 does **not** prove PITR, AWS S3 behavior, S3 Versioning, Object Lock, production retention or SC-011.

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

## CP05 opening constraints carried from CP04

The CP04 restored target is intentionally left isolated with `archive_mode=off` after verification. CP05 must explicitly choose whether to discard/recreate that target or reactivate a fresh archive-producing source; it may not silently use the isolated CP04 verification target as if it were the continuous-archive primary.

The CP05 harness must preserve:

```text
same accepted PostgreSQL 18.6 image
dedicated recovery project/volumes only
repository independence from disposable PGDATA
P0/Alembic/catalog semantic baseline
unique deterministic A/B fixture identifiers
named restore point rather than timing-only target
explicit WAL archive evidence before destruction
traffic/application closed until target assertions pass
```

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

CP03 already proves one narrow archive-push failure/retry path. CP04 proves one restore-startup filesystem defect and its bounded recovery. Those evidence items are retained, but they do not replace the broader CP06 failure matrix.

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
[x] SC-031 local destructive PostgreSQL proof PASS
[ ] SC-031 selected-stack evidence reconciled where required
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

CP01 is contract-frozen, CP02 is **LOCAL PASS**, CP03 is **LOCAL PASS**, CP04 is **LOCAL PASS**, and CP05 is **NOT STARTED**.

Next safe technical sequence:

```text
1. fast-forward /home/mattia/projects/dante-postgres-recovery to the CP04 closure HEAD
2. keep dante-postgres-recovery-cp04-restore isolated with archive_mode=off until CP05 topology is frozen
3. decide whether CP05 discards that target and recreates the archive-producing recovery source or uses another explicitly isolated source/target pair
4. materialize/verify the accepted DANTE database baseline before PITR writes
5. create a fresh valid FULL baseline appropriate for the PITR scenario
6. write deterministic state A and commit
7. create a unique named pg_create_restore_point marker R
8. force/confirm WAL containing R is archived through pgBackRest
9. write deterministic state B and commit
10. force/confirm later WAL archival
11. destroy/isolate the CP05 target PGDATA while preserving the repository
12. restore the selected FULL with recovery_target_name=R and an explicit target action
13. prove recovery actually reaches R
14. prove A PRESENT and B ABSENT
15. repeat catalog/owner/ACL/extension/runtime semantic verification
16. capture recovery/replay timings
```

Do **not** enter AWS, production retention or SC-011 implementation under CP05. A successful CP04 full restore is not deterministic PITR proof.