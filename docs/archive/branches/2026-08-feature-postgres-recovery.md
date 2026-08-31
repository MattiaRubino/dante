# Branch history — feature/postgres-recovery

> Historical branch record. **NON-AUTHORITATIVE for current project state.**
> Current truth lives in protected-main/live Git, the Database System of Record, current code/migrations/tests and the PostgreSQL Recovery operator runbook.

## Identity

- Repository: `MattiaRubino/dante`
- Branch: `feature/postgres-recovery`
- Worktree used at closure: `/home/mattia/projects/dante-postgres-recovery`
- LOCAL recovery checkpoints: CP01–CP07
- Closure documentation anchor before archival: `10a4dab17f2c968fc918211dfe6476245d7f23d7`
- Reusable-runner implementation/runtime proof HEAD: `789e946a8f096b52f2a440b967120cc3e0a340a3`
- Initial CP07 whole-rehearsal implementation proof HEAD: `8893efe629ff1dc9fc2b512779aa56457b802be6`
- CP06 implementation/runtime proof HEAD: `a1a6323210b3d7af66284006a754759fa9d08028`
- PostgreSQL: 18.6
- Recovery-tree Alembic head: `20260830_09`
- Recovery-tree topology: `69|5|15|76|97|69|123|0|0|0`
- Remote backup provider at closure: `TBD / NOT ACTIVATED`
- Production/cloud recovery at closure: `NOT CLAIMED`

The branch/worktree names above are phase-time evidence only. The permanent bootstrap and CP07 runner are branch-agnostic and require a clean attached branch with a configured upstream and exact `HEAD == upstream` after fetch.

## Purpose

The workstream turned the accepted Physical recovery capability into a directly rehearsed LOCAL PostgreSQL recovery system without creating a second canonical persistence authority.

Permanent doctrine:

```text
PostgreSQL = sole canonical persistence + material-history authority
backup repository != canonical truth
restored bytes != automatically accepted semantic truth
pg_isready != traffic-open proof
old backup restore != permission to resurrect later-retired payload
successful LOCAL recovery != production/cloud recovery proof
```

The workstream also materialized the bounded recovery lifecycle evolution required to preserve WL-H10 / SC-011 retirement semantics across old-backup restoration.

## Milestone sequence

```text
CP01  Recovery Contract / Bootstrap          CLOSED / CONTRACT FROZEN
CP02  pgBackRest Foundation                  LOCAL PASS
CP03  Continuous WAL + Backup                LOCAL PASS
CP04  Destructive / Isolated Restore         LOCAL PASS
CP05  Deterministic PITR                     LOCAL PASS
CP06  Failure + Semantic Recovery            LOCAL PASS / CLOSED
CP07  Whole Recovery QA + Operator Runbook   LOCAL PASS / CLOSED
POST  Fresh-clone reproducibility hardening  PASS / EXACT-HEAD PROVEN
```

## Recovery topology and activation boundary

LOCAL recovery used:

```text
PostgreSQL base image        postgres:18.6-trixie pinned by digest
PGDATA                       /var/lib/postgresql/18/docker
pgBackRest                   2.59.1
stanza                       dante
LOCAL repository             POSIX / dedicated volume
Compose project              dante-postgres-recovery
recovery image               dante-postgres-recovery:18.6-pgbackrest-2.59.1
remote provider              TBD / NOT ACTIVATED
production/cloud recovery    NOT CLAIMED
```

The Physical phase preserved a historical target involving S3, but this branch deliberately did not pretend that a production remote provider had been activated. Provider-specific credentials, retention, immutability, restore/PITR and production RPO/RTO proof remain a later deployment boundary.

## Database evolution for anti-resurrection

The branch added one normal forward revision:

```text
20260826_08
    ↓
20260830_09  recovery material-state retirement
```

`20260830_09` materialized:

```text
dante.material_state_retirement
dante.enforce_material_state_retirement()
```

and moved the branch-local topology from the protected-main CP6 baseline:

```text
20260826_08 / 68|5|14|75|95|68|120|0|0|0
```

to:

```text
20260830_09 / 69|5|15|76|97|69|123|0|0|0
```

Supported retirement-aware material facets at closure:

```text
schedule.placement
actual.realization
session.timing
routine.recurrence
event.recurrence
```

For retired material state, the semantic address/envelope and permitted history remain truthful while protected payload is absent and reinsertion is rejected.

## Suppression-ledger protocol

An old physical backup can predate a later canonical tombstone. The workstream therefore added an independent **recovery-only** suppression ledger; it is not a second canonical database.

Protocol:

```text
PREPARED durable suppression intent
→ canonical PostgreSQL retirement/redaction transaction
→ canonical DB read-back verification
→ COMMITTED marker bound to PREPARED SHA-256
```

Recovery blocks on ambiguous or tampered evidence, including missing/unavailable record storage, unexpected entries, duplicate targets, orphan PREPARED/COMMITTED records, identity mismatch, hash mismatch or invalid/non-canonical records.

Suppression evidence retention must cover the full resurrection horizon of retained database/WAL/object versions.

## CP02–CP05 retained direct proof

The LOCAL workstream directly proved:

```text
pgBackRest package/CLI/config/repository        PASS
continuous WAL archive                          PASS
FULL backup + deterministic LOCAL retention     PASS
archive failure visibility/retry                PASS
destructive isolated restore                    PASS
source PGDATA destruction                       PASS
repository preservation                         PASS
PostgreSQL 18.6 boot + not-in-recovery          PASS
roles/owners/ACL/extensions/runtime path         PASS
deterministic named-target PITR                  PASS
A-before-target present                          PASS
B-after-target absent                            PASS
timeline promotion                              PASS
```

These results are LOCAL evidence only.

## CP06 — failure injection and semantic recovery

Versioned failure matrix covered:

```text
N1 wrong stanza/config
N2 empty/unavailable repository
N3 nonexistent recovery set
N4 impossible PITR target
N5 required WAL missing
N6 corrupted backup artifact
N7 bootable but semantically stale target
```

All seven cases failed closed without accepting a dangerous recovery target.

The definitive SC-011 rehearsal proved:

```text
old B0 physically contains protected X          PASS
canonical later retirement removes X            PASS
old B0 restore physically resurrects X           PROVEN
restored target remains isolated                 PASS
committed suppression evidence validates         PASS
ledger reconciliation removes resurrected X      PASS
NativeRef continuity                             PASS
MaterialStateRef continuity                      PASS
current/history continuity                       PASS
payload reinsertion after retirement             REJECTED
runtime retirement ACL SELECT-only               PASS
real recovery repository non-interference        PASS
retained CP05 target non-interference             PASS
```

CP06 implementation/runtime proof HEAD:

```text
a1a6323210b3d7af66284006a754759fa9d08028
```

## CP07 — whole operator rehearsal

The integrated CP07 flow exercised one disposable end-to-end disaster scenario rather than merely replaying earlier scripts:

```text
healthy current PostgreSQL
→ FULL backup + continuous WAL
→ deterministic restore point
→ A before target
→ B after target
→ canonical retirement + committed suppression
→ complete disposable PGDATA loss
→ exact restore + named PITR
→ promotion
→ A present / B absent
→ old protected X physically resurrected while isolated
→ suppression-ledger reconciliation
→ tombstone present / X absent
→ payload reinsertion rejected
→ structural/security/runtime acceptance
→ database-local reopen
→ cleanup
```

Initial whole-rehearsal proof HEAD:

```text
8893efe629ff1dc9fc2b512779aa56457b802be6
```

Initial measured LOCAL observations:

```text
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

These are observations, not production RPO/RTO targets.

## Fresh-clone reproducibility hardening

After CP07 closure, the permanent recovery entry points were hardened so a fresh clone no longer depends on the historical feature branch name or manually replaying CP01–CP06.

Permanent entry points:

```text
infra/local/postgres/recovery/bootstrap-local-recovery.sh
infra/local/postgres/recovery/cp07-whole-recovery-rehearsal.sh
docs/operations/postgres-recovery-runbook.md
```

The bootstrap/runner proof established:

```text
validation clone started without recovery secrets         PASS
first bootstrap created all three LOCAL secrets           PASS
second bootstrap preserved exact secret contents          PASS
secret files mode 0600 / ignored / untracked              PASS
repository Compose validation                              PASS
repository-built pinned recovery image                     PASS
branch-name independence                                  PASS
clean attached branch + configured upstream gate           PASS
whole backend QA on exact hardened tree                    PASS
pre-push whole CP07 rehearsal                              PASS
exact pushed implementation HEAD whole CP07 rehearsal      PASS
database-local reopen                                      PASS
deterministic PITR A-present / B-absent                    PASS
old protected X physical resurrection                      PROVEN
ledger anti-resurrection reconciliation                    PASS
payload reinsertion after retirement                       REJECTED
non-interference / cleanup                                 PASS
```

Exact reusable-runner implementation/runtime proof HEAD:

```text
789e946a8f096b52f2a440b967120cc3e0a340a3
```

Measured LOCAL observations from that exact pushed hardened runner:

```text
backup duration                           53.964433 s
backup repository size                    5743173 bytes
WAL archive freshness at disaster         0.834662 s
restore-point age at disaster             3.629809 s
physical restore                          7.650652 s
PITR replay to target                     0.144582 s
recovery to ready                         0.382306 s
semantic reconciliation                   1.021309 s
structural/security acceptance            0.910673 s
PGDATA loss → database-local reopen       16.261533 s
```

Again: LOCAL observations only.

## Final runtime/reproducibility hardening result

The final hardening run completed with:

```text
CP01–CP07                      LOCAL PASS / CLOSED
FRESH-CLONE BOOTSTRAP          PASS
BOOTSTRAP IDEMPOTENCE          PASS
BRANCH-AGNOSTIC RUNNER         PASS
WHOLE BACKEND QA               128 / 128 PASS
EXACT-HEAD WHOLE CP07          PASS
TEMPORARY LIVE HANDOFF         REMOVED
REMOTE BACKUP PROVIDER         TBD / NOT ACTIVATED
PRODUCTION/CLOUD RECOVERY      NOT CLAIMED
```

Implementation/runtime proof HEAD:

```text
789e946a8f096b52f2a440b967120cc3e0a340a3
```

Documentation anchor produced by that run:

```text
10a4dab17f2c968fc918211dfe6476245d7f23d7
```

## Current durable ownership after branch closure

```text
current database meaning/topology
→ docs/database/README.md
→ docs/database/dante-postgresql-database.md + current continuation parts
→ docs/database/dictionary/

operator recovery procedure
→ docs/operations/postgres-recovery-runbook.md

reusable recovery execution
→ infra/local/postgres/recovery/

migration / mapping / integrity implementation
→ apps/backend/alembic + src/dante/platform/database + recovery support

historical branch narrative
→ this file

complete chronology / removed overlays
→ Git history
```

## Removed active-workstream / handoff material

The active-branch files below were useful while the branch was being built but are intentionally not retained as current main-navigation authorities:

```text
docs/workstreams/postgres-recovery.md
docs/workstreams/postgres-recovery-execution-plan.md
docs/workstreams/postgres-recovery-live-handoff-2026-08-29.md
```

The live handoff had already been removed by reproducibility hardening. The workstream and execution-plan overlays are absorbed into this single historical record plus the current Database System of Record and operator runbook.

Their exact former payload remains recoverable through Git.

## Knowledge-coverage disposition

```text
current DB contract                    -> Database System of Record + Dictionary
operator procedure                     -> PostgreSQL Recovery runbook
executable recovery                    -> versioned bootstrap/rehearsal harnesses
anti-resurrection implementation       -> migration + DB integrity + suppression ledger
direct regression proof                -> tests/harnesses + retained exact proof heads
branch chronology / milestone context  -> this archive record
cross-chat / active-plan mechanics      -> Git history only
remote-provider production work        -> deferred / TBD / not activated
```

No removed active-workstream file remains current authority after closure.
