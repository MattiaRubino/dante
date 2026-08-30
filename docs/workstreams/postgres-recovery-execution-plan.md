# DANTE — PostgreSQL Recovery Execution Plan

- **Status:** CURRENT EXECUTION PLAN / CP01 FROZEN / CP02 LOCAL PASS / CP03 LOCAL PASS / CP04 LOCAL PASS / CP05 LOCAL PASS / CP06 NOT STARTED
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
successful local proof != selected remote-stack proof
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
   ├── materialized semantic backup source
   ├── destructive PGDATA replacement
   ├── exact-set restore
   ├── PostgreSQL start
   └── catalog / ACL / semantic verification
   ↓
CP05 Deterministic PITR
   │
   ├── promoted timeline + timeline history
   ├── A / named restore point / B
   ├── archived WAL completeness
   ├── destructive exact-target recovery
   ├── A present / B absent
   └── measured replay/readiness timings
   ↓
CP06 Failure Injection + Semantic Recovery
   │
   ├── broader recovery failure matrix
   ├── missing/unreachable repository/WAL cases
   ├── wrong target/config mismatch cases
   ├── SC-011 anti-resurrection
   └── derived/object reconciliation boundaries
   ↓
CP07 Whole Recovery QA + Runbook + Closure
   ├── clean end-to-end rehearsal
   ├── measured RPO/RTO evidence
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

## Frozen decisions

```text
PostgreSQL                     18.6
base image                     postgres:18.6-trixie pinned by digest
PGDATA                         /var/lib/postgresql/18/docker
persistent root                /var/lib/postgresql
accepted pgBackRest baseline   2.59.0 historical selection
activation implementation      2.59.1
PGDG package pin               2.59.1-1.pgdg13+1
stanza                         dante
LOCAL repo                     POSIX / dedicated named volume
repo path                      /var/lib/pgbackrest
recovery Compose project       dante-postgres-recovery
recovery host port             127.0.0.1:55432
AWS selected topology          S3 Standard eu-south-1 + Versioning + Object Lock GOVERNANCE
AWS activation                 DEFERRED
backup policy hypothesis       continuous WAL + daily FULL
numeric production RPO/RTO     NOT INVENTED
SC-011                         OPEN HARD GATE
```

Security boundary:

```text
no secrets in repository
minimum AWS repository permissions
no normal-role governance-retention bypass
separate break-glass administration
finite retention
```

## CP01 state

```text
CP01 CONTRACT FROZEN
```

SC-011 itself is not closed by CP01.

---

# 4. CP02 — pgBackRest Foundation

## Goal

Materialize pgBackRest reproducibly without claiming archive, backup or recovery correctness before those mechanisms are exercised.

## Implemented source surface

```text
infra/local/postgres/Dockerfile
infra/local/postgres/pgbackrest/pgbackrest.conf
infra/compose/local.yaml
infra/compose/postgres-recovery.override.yaml
```

Current exact foundation:

```text
pgBackRest package             2.59.1-1.pgdg13+1
expected CLI                   pgBackRest 2.59.1
config                         /etc/pgbackrest/pgbackrest.conf
config ownership               root:postgres / 0640
stanza                         dante
pg1-path                       /var/lib/postgresql/18/docker
repo1-type                     posix
repo1-path                     /var/lib/pgbackrest
repository volume              pgbackrest-repository:/var/lib/pgbackrest
repository ownership           postgres:postgres / 0750
```

## Direct CP02 evidence

```text
clean Docker image build                            PASS
exact package/CLI assertion during build            PASS
container health                                    PASS
PostgreSQL version == 18.6                          PASS
data_directory == /var/lib/postgresql/18/docker     PASS
config/read/write permissions                       PASS
stanza-create                                       PASS
pgbackrest info                                     PASS
archive.info / backup.info metadata                 PASS
ordinary dante-local PostgreSQL non-interference    PASS
ordinary Alloy non-interference                     PASS
```

Expected CP02 `info` state was deliberately `status: error (no valid backups)` because CP02 had no backup/WAL archive yet.

`pgbackrest check` is not a CP02 gate. A meaningful `check` validates archive interaction and therefore belongs to CP03.

## CP02 state

```text
CP02 LOCAL PASS
```

---

# 5. CP03 — Continuous WAL + Backup

## Goal

Prove PostgreSQL 18.6 continuously archives WAL through pgBackRest and that a physical FULL backup completes with a usable archive path.

## Recovery-only runtime settings

```text
archive_mode = on
archive_command = /usr/bin/pgbackrest --stanza=dante archive-push %p
archive_library = unset
wal_level = replica (existing/inherited; not overridden)
repo1-retention-full = 2 (LOCAL test policy only)
```

## Direct CP03 evidence

```text
recovery runtime recreated from versioned source       PASS
archive_mode=on                                        PASS
archive_command exact                                   PASS
archive_library unset                                   PASS
wal_level=replica                                      PASS
forced WAL switch                                      PASS
pg_stat_archiver success                               PASS
physical WAL artifact in repository                    PASS
pgbackrest check                                       PASS
FULL backup                                            PASS
repeated FULL backups                                  PASS
repo1-retention-full=2 behavior                        PASS
explicit expire                                        PASS
archive failure visibility                             PASS
same-WAL retry after repository permission recovery    PASS
post-failure physical WAL                              PASS
post-failure check/info                                PASS
```

Versioned failure harness:

```text
infra/local/postgres/recovery/archive-failure-recovery-check.sh
```

The LOCAL retention setting is not a production S3 retention contract.

## CP03 state

```text
CP03 LOCAL PASS
```

CP03 alone does not prove restore, PITR, AWS, Object Lock or anti-resurrection.

---

# 6. CP04 — Destructive / Isolated Restore

## Goal

Prove recovery from a real physical backup after the disposable source PGDATA is genuinely unavailable.

## Materialization prerequisite discovered during CP04

The earlier CP03 backups were physically valid but represented the bootstrap database rather than the fully materialized DANTE semantic database. CP04 therefore first materialized the accepted database through existing production boundaries rather than inventing recovery-only schema setup.

Versioned materialization harness:

```text
infra/local/postgres/recovery/cp04-materialize-backup.sh
```

Direct semantic source evidence:

```text
P0 provisioning                         PASS
Alembic upgrade/current/check           20260826_08 PASS
accepted topology                       68|5|14|75|95|68|120|0|0|0 PASS
owners                                  dante_owner PASS
roles                                   dante_owner/migrator/runtime PASS
runtime alembic_version SELECT           denied PASS
required extension versions             PASS
canonical Person fixture UUIDv7         PASS
semantic FULL                           20260830-132540F PASS
```

## Destructive restore scenario

Versioned harness:

```text
infra/local/postgres/recovery/cp04-destructive-restore-check.sh
```

Direct proof:

```text
source-volume marker                    written
postgres-data volume                    deleted
pgBackRest repository volume            preserved
repository metadata hash                unchanged
new PostgreSQL volume                   recreated
old source marker                       absent
exact FULL                              20260830-132540F
pgBackRest restore                      PASS
restore size                            40.6MB / 1501 files
PostgreSQL startup                      PASS
archive_mode verification target        off
PostgreSQL                              18.6
Alembic                                 20260826_08
topology                                exact PASS
canonical fixture                       PASS
owners/roles/ACL/extensions             PASS
real dante_runtime login/read           PASS
```

### PostgreSQL 18 version-parent finding

A root pgBackRest restore into a newly-created PostgreSQL 18 Docker volume created `/var/lib/postgresql/18` as `root:root 0700`. The restored PGDATA itself was valid, but the official PostgreSQL entrypoint could not traverse that parent after dropping privileges.

Proven narrow normalization:

```text
chown postgres:postgres /var/lib/postgresql/18
chmod 0700 /var/lib/postgresql/18
```

The versioned destructive harness performs this before first boot.

## CP04 close criteria

```text
[x] materialized DANTE backup source
[x] source PGDATA genuinely destroyed
[x] recovery repository survives independently
[x] exact backup restored
[x] restored PostgreSQL starts
[x] PostgreSQL/Alembic/catalog topology exact
[x] canonical fixture restored
[x] owners/roles/ACL/extensions verified
[x] real runtime login/read verified
[x] SC-031 local destructive proof satisfied
```

## CP04 state

```text
CP04 LOCAL PASS
SC-031 LOCAL PASS
```

---

# 7. CP05 — Deterministic PITR

## Goal

Prove recovery to one exact point between two observable canonical database states without depending on ambiguous wall-clock timing.

## Accepted deterministic scenario

```text
FULL base
→ promoted recovery source timeline
→ ensure timeline-history continuity in repository
→ write A and commit
→ create named restore point R1
→ force/confirm R1 WAL archive
→ write B and commit
→ force/confirm later B WAL archive
→ prove source contains baseline + A + B
→ destroy PGDATA
→ restore exact FULL
→ replay exact target timeline to R1
→ promote
→ baseline present
→ A present
→ B absent
→ catalog/ACL/runtime verification
→ timing readback
```

Versioned harnesses:

```text
infra/local/postgres/recovery/cp05-prepare-pitr-source.sh
infra/local/postgres/recovery/cp05-destructive-pitr-check.sh
```

## Timeline-history finding

The CP04 verification target was intentionally promoted with `archive_mode=off`. Its new timeline-history file therefore existed locally but had not been queued for archive. Re-enabling `archive_mode` on a later restart did not retroactively queue the already-created file.

The CP05 preparation harness therefore follows this rule:

```text
current timeline WAL must archive normally
+
timeline-history must physically exist in repository
+
if the existing history file was created while archive_mode=off,
explicitly pgbackrest archive-push that PostgreSQL history file
+
never fabricate/manipulate pg_wal/archive_status manually
```

This condition must pass before A/R1/B are created.

## Direct CP05 scenario evidence

```text
base FULL                          20260830-132540F
target timeline                    2
timeline history                   00000002.history
scenario                           dante_cp05_20260830T140906Z_19757
restore point                      dante_cp05_20260830T140906Z_19757_R1
restore point LSN                  0/16000230
restore point WAL                  000000020000000000000016
A                                  01a05300-a55e-7845-a710-69387408d147
B                                  01a05300-a5c0-7d08-a608-74ac9d821817
B WAL                              000000020000000000000017
source current WAL after scenario  000000020000000000000019
repository WAL range after source  ...timeline1... / 000000020000000000000018
```

Source state immediately before destructive PITR:

```text
BASELINE  PRESENT
A         PRESENT
B         PRESENT
```

Archive completeness:

```text
timeline-2 WAL                     PASS
00000002.history                   PASS
restore-point WAL ...0016          PASS
post-target B WAL ...0017          PASS
pgBackRest check                   PASS
```

## Destructive PITR command contract

The direct successful restore used:

```text
--set=20260830-132540F
--type=name
--target=dante_cp05_20260830T140906Z_19757_R1
--target-timeline=2
--target-action=promote
--archive-mode=off
```

Generated recovery settings were verified before first boot.

Direct restore/replay evidence:

```text
PGDATA volume deleted                           PASS
repository survived unchanged                   PASS
old source marker absent                        PASS
exact FULL restore                              PASS
named restore target                            PASS
target timeline 2                               PASS
target-action promote                           PASS
PITR target ready / pg_is_in_recovery=false     PASS
new timeline                                    3
current promoted WAL                            000000030000000000000016
BASELINE                                        PRESENT
A                                               PRESENT
B                                               ABSENT
PostgreSQL 18.6                                 PASS
Alembic 20260826_08                             PASS
accepted topology                               PASS
owners/roles/ACL/extensions                     PASS
dante_runtime sees A and not B                  PASS
repository metadata unchanged                   PASS
```

PostgreSQL logs directly showed:

```text
starting point-in-time recovery to named R1
redo starts at 0/11000028
recovery stopping at named R1
redo done at 0/160001C8
selected new timeline ID: 3
archive recovery complete
database system is ready to accept connections
```

## Direct LOCAL timing evidence

```text
pgBackRest physical restore reported        7.530 s
WAL replay start -> target                  0.263121 s
recovery start -> database ready            0.539736 s
target -> database ready                    0.276615 s
```

These are measurements from the exercised LOCAL small-dataset scenario. They prove measurement/readback capability and local behavior; they are not production RPO/RTO targets.

## CP05 close criteria

```text
[x] deterministic marker recovery PASS
[x] A present
[x] B absent
[x] baseline semantic fixture present
[x] Alembic/catalog/ACL/runtime verification PASS
[x] required timeline-history and WAL chain proven
[x] explicit exact backup and target timeline used
[x] recovery target reached visibly in PostgreSQL logs
[x] target promotion visible
[x] replay/recovery timings recorded
[x] repository survives destructive target replacement
```

## CP05 state

```text
CP05 Deterministic PITR                  LOCAL PASS
PSV-40 local archive/restore/PITR       PASS
```

The remote selected AWS topology is still not activated/proven, so LOCAL PSV-40 evidence must not be mislabeled as remote production acceptance.

---

# 8. CP06 — Failure Injection + Semantic Recovery / Anti-Resurrection

## Goal

Prove recovery fails safely and observably under representative failure conditions, then address the semantic state that byte-correct backup/restore/PITR cannot solve by itself.

## CP06 opening boundary

CP05 proved the happy-path physical recovery mechanics strongly enough that CP06 can now focus on failure truth and recovery semantics rather than re-proving basic restore.

### Recovery failure matrix

At minimum consider/exercise:

```text
repository unavailable
bad/missing repository credentials where applicable
missing required WAL
corrupted/unusable recovery artifact where safely reproducible
wrong stanza/repository configuration
empty/destroyed PGDATA
impossible PITR target
operator selects wrong recovery set / mismatch detection
```

A negative scenario passes only when the recovery procedure fails safely, observably and diagnosably. A non-zero command by itself is not sufficient evidence if the failure is ambiguous or leaves a dangerous partially usable target.

CP03 already proves one narrow archive-push permission failure/retry path. It remains valid evidence but does not replace the broader CP06 matrix.

## SC-011 anti-resurrection

Required semantic failure model:

```text
T0 state X exists and old backup B0 captures it
T1 accepted later deletion/redaction D1 retires or restricts X
T2 canonical PostgreSQL is lost
T3 B0 is restored successfully
T4 raw restored bytes contain X again
T5 recovery procedure applies/validates independently surviving suppression/reconciliation facts
T6 X is not silently accepted/exposed as current permitted truth
T7 identity/tombstone/material-history obligations remain truthful
T8 derived/object state is reconciled before traffic reopen
```

### Design constraint

The T5 mechanism must not casually create a second canonical application database. It must be narrowly recovery-authoritative for the exact suppression/reconciliation facts it carries, auditable, durable enough to survive the relevant disaster boundary, and compatible with accepted DANTE deletion/redaction/material-history semantics.

If no mechanism satisfies those constraints, CP06 remains `BLOCKED` rather than inventing a fake PASS.

## Derived-state reconciliation

Where disposable projections/sync/search/vector state exists, define:

```text
which state is discarded
which state is rebuilt from PostgreSQL
what freshness/version marker proves rebuild completion
what remains unavailable until rebuild completes
```

A stale derived store must never override restored canonical PostgreSQL.

## Object-backup reconciliation

The PostgreSQL recovery procedure must define the boundary for reconciling database references to backed-up R2/object state. Full object-recovery implementation may be a later slice, but the runbook cannot pretend that database restore alone proves object consistency.

## CP06 state

```text
CP06 NOT STARTED
SC-011 OPEN HARD GATE / NOT PASS
```

---

# 9. CP07 — Whole Recovery QA + Runbook + Closure

## Goal

Turn the individually proven mechanisms into one repeatable operator procedure and collect direct selected-stack evidence.

## Whole rehearsal target

```text
healthy PostgreSQL
→ continuous WAL + usable backup available
→ simulated complete database loss
→ repository/credentials identified
→ clean PostgreSQL target prepared
→ restore or PITR executed
→ database starts
→ semantic verification
→ anti-resurrection/reconciliation
→ derived/object reconciliation gate
→ application readiness verification
→ traffic-reopen decision
```

## Remote AWS acceptance

Before production recovery is marked PASS, repeat the relevant recovery path against:

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

Local POSIX evidence is deliberately insufficient for this remote selected-stack claim.

## Measured evidence

Capture at minimum:

```text
backup size / duration
WAL archive freshness/latency
restore duration
PITR replay duration
semantic verification duration
end-to-end operator recovery duration
actual recovery point/data-loss window
```

## Runbook requirements

The runbook must answer without chat memory:

```text
How do I identify the correct stanza/repository?
How do I verify backup health before destroying anything else?
How do I prepare a clean PostgreSQL 18.6 target?
How do I choose full restore vs PITR?
How do I choose and verify the PITR target/timeline?
How do I verify required WAL/timeline-history exists?
How do I know recovery reached the target and promoted?
What semantic/catalog checks run?
How is anti-resurrection/reconciliation applied?
What derived/object state must be rebuilt/reconciled?
What conditions keep traffic closed?
What is the break-glass path?
What evidence/logs are retained?
```

## Closure criteria

```text
[ ] CP01–CP06 evidence reconciled
[ ] local clean whole rehearsal PASS
[ ] direct AWS selected-stack acceptance PASS
[ ] SC-031 retained PASS
[ ] PSV-40 remote selected-stack evidence PASS where required
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

---

## 10. Test strategy

Use layered evidence rather than one giant brittle script.

### Static/config checks

```text
version pins
configuration ownership/path checks
secret scanning
compose/build validation
shell/script lint where applicable
```

### Deterministic local recovery tests

```text
stanza/config validation
repository permissions
archive-path failure/retry
semantic fixture materialization
FULL backup
fresh/destructive restore
named-target PITR
timeline-history continuity
catalog/ACL/runtime verification
failure injection
```

### Real PostgreSQL integration

Do not use SQLite or mocked PostgreSQL behavior as correctness evidence for physical recovery.

### Remote acceptance

```text
real S3 bucket characteristics
real IAM/role behavior
real Versioning/Object Lock behavior
real repository read/write/archive
real restore/PITR
```

---

## 11. CI boundary

Recovery tests are destructive and infrastructure-heavy. Do not blindly add the full suite to every normal backend test run.

Expected split:

```text
fast/static recovery checks
→ normal CI candidate

local destructive PostgreSQL recovery suite
→ explicit marked/manual or dedicated CI job

real AWS recovery acceptance
→ controlled manual/scheduled/release-boundary job with scoped credentials
```

Exact CI activation belongs to the checkpoint where the runtime is stable enough to avoid a flaky permanent pipeline.

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

Forbidden without a separate explicit gate include:

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

Current state:

```text
CP01 CONTRACT FROZEN
CP02 LOCAL PASS
CP03 LOCAL PASS
CP04 LOCAL PASS
SC-031 LOCAL PASS
CP05 LOCAL PASS
PSV-40 local archive/restore/PITR PASS
CP06 NOT STARTED
SC-011 OPEN HARD GATE
AWS selected topology NOT ACTIVATED
```

The CP05 verification target may remain isolated with `archive_mode=off` until the closure commit is synchronized locally.

Next safe sequence:

```text
1. fast-forward the dedicated recovery worktree to the CP05 closure HEAD
2. verify the versioned CP05 harnesses and current docs read back correctly
3. retain CP05 evidence; do not mutate it into CP06 claims
4. inspect current accepted deletion/redaction/tombstone semantics and their disaster boundaries
5. design the CP06 failure matrix and SC-011 proof model before destructive execution
6. identify which negative tests can be exercised safely on the LOCAL topology
7. derive the narrowest truthful anti-resurrection mechanism or explicitly record BLOCKED
8. freeze a new exact CP06 write/runtime gate
```

Do **not** enter AWS activation, production retention, whole runbook closure or unrelated application work under the CP05 closure gate.