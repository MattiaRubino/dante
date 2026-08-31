# DANTE — PostgreSQL Recovery Live Handoff

- **Status:** CURRENT LIVE HANDOFF / CP06 LOCAL PASS / CLOSED / CP07 NEXT
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/postgres-recovery`
- **Worktree:** `/home/mattia/projects/dante-postgres-recovery`
- **PostgreSQL:** 18.6
- **Current branch DB head:** `20260830_09`
- **Current branch DB topology:** `69|5|15|76|97|69|123|0|0|0`
- **CP01–CP05:** directly proven LOCAL PASS
- **CP06:** LOCAL PASS / CLOSED
- **SC-011:** PASS — definitive versioned harness directly proven
- **CP07:** not started

> This file is only the active branch continuation checkpoint. Repository/code/tests beat this handoff if they disagree. Remove/consolidate it before protected-main integration once durable current documents cover all necessary information.

---

## 1. Continue exactly here

```text
repo       MattiaRubino/dante
branch     feature/postgres-recovery
worktree   /home/mattia/projects/dante-postgres-recovery
```

Other occupied DANTE worktrees must not be reset/detached/repurposed.

Before any local proof:

```bash
pwd
git status --short --branch
git rev-parse HEAD
git rev-parse origin/feature/postgres-recovery
git rev-parse origin/main
git worktree list --porcelain
```

Require a clean worktree and local HEAD == remote branch HEAD.

## 2. Current read order

1. `docs/workstreams/postgres-recovery.md`
2. this file
3. `docs/workstreams/postgres-recovery-execution-plan.md`
4. `docs/database/README.md`
5. `docs/database/dante-postgresql-database.md`
6. `docs/database/dante-postgresql-database-part-19.md`
7. `apps/backend/migrations/versions/20260830_09_recovery_material_state_retirement.py`
8. `apps/backend/src/dante/platform/recovery/suppression_ledger.py`
9. `apps/backend/tests/integration/database/test_database_current_catalog.py`
10. `apps/backend/tests/integration/database/test_recovery_material_state_retirement.py`
11. `apps/backend/tests/unit/platform/recovery/test_suppression_ledger.py`
12. `infra/local/postgres/recovery/cp06-failure-matrix-check.sh`
13. `infra/local/postgres/recovery/cp06-sc011-anti-resurrection-check.sh`
14. `docs/development/agent-operating-manual.md`

Do not redesign the database/recovery semantics from scratch.

## 3. Current runtime topology

```text
PostgreSQL                   18.6
PGDATA                       /var/lib/postgresql/18/docker
pgBackRest                   2.59.1
PGDG package                 2.59.1-1.pgdg13+1
stanza                       dante
LOCAL repository             POSIX / /var/lib/pgbackrest
Compose project              dante-postgres-recovery
host port                    127.0.0.1:55432
PostgreSQL volume            dante-postgres-recovery_postgres-data
repository volume            dante-postgres-recovery_pgbackrest-repository
```

Selected production topology remains:

```text
pgBackRest
→ AWS S3 Standard eu-south-1
→ Versioning
→ Object Lock GOVERNANCE
→ finite policy-bound retention
```

AWS remains **NOT ACTIVATED**.

## 4. Current checkpoint matrix

```text
CP01 Recovery Contract / Bootstrap       CLOSED / CONTRACT FROZEN
CP02 pgBackRest Foundation               LOCAL PASS
CP03 Continuous WAL + Backup             LOCAL PASS
CP04 Destructive / Isolated Restore      LOCAL PASS
SC-031 destructive local restore         PASS
CP05 Deterministic PITR                  LOCAL PASS
PSV-40 local archive/restore/PITR        PASS
CP06 Failure Injection + Semantic        LOCAL PASS / CLOSED
Failure Matrix versioned final harness   LOCAL PASS
SC-011 mechanism prototype               LOCAL PASS
SC-011 versioned final harness           LOCAL PASS
CP07 Whole Recovery QA + Runbook         NEXT / NOT STARTED
AWS selected recovery topology           NOT ACTIVATED
```

## 5. Direct retained CP05 state

The currently retained isolated CP05 target is:

```text
dante-postgres-recovery-cp05-pitr
```

Direct state retained from the proven scenario:

```text
server_version_num   180006
pg_is_in_recovery    false
archive_mode         off
A                     present
B                     absent
```

Scenario identifiers:

```text
BASE_BACKUP       20260830-132540F
TARGET_TIMELINE   2
RESTORE_POINT     dante_cp05_20260830T140906Z_19757_R1
RESTORE_WAL       000000020000000000000016
A_REF             01a05300-a55e-7845-a710-69387408d147
B_REF             01a05300-a5c0-7d08-a608-74ac9d821817
```

Do not destroy/repurpose this target casually; CP06 harnesses use it as a non-interference sentinel.

## 6. Current database evolution

New migration:

```text
20260830_09_recovery_material_state_retirement.py
```

Adds:

```text
dante.material_state_retirement
dante.enforce_material_state_retirement()
```

Current expected topology:

```text
69 tables
5 views
15 routines
76 triggers
97 indexes
69 foreign keys
123 CHECK constraints
0 enum/domain
0 sequences/materialized/partitioned/RLS
```

Supported retirement-aware facets:

```text
schedule.placement
actual.realization
session.timing
routine.recurrence
event.recurrence
```

Retirement preserves permitted envelope/address/history continuity while protected payload/selectors must be absent.

Runtime access to `material_state_retirement` is SELECT only.

## 7. Suppression ledger

Versioned implementation:

```text
apps/backend/src/dante/platform/recovery/suppression_ledger.py
infra/local/postgres/recovery/recovery-suppression-record-v1.schema.json
```

Protocol:

```text
PREPARED
→ canonical PostgreSQL retirement/redaction commit
→ canonical read-back verification
→ COMMITTED bound to PREPARED SHA-256
```

Recovery blocks on missing/unavailable `records/`, unexpected entries, duplicate MaterialStateRef targets, orphan PREPARED/COMMITTED state, identity/target mismatch, prepared-hash mismatch and invalid/non-canonical evidence.

The ledger is recovery-only evidence and must survive independently from both PGDATA and the database backup repository.

## 8. Failure-matrix status

Direct disposable proof already demonstrated:

```text
wrong stanza                         PASS
empty repository                    PASS
invalid backup set                  PASS
impossible PITR target              PASS
missing required WAL                PASS
corrupted cloned backup artifact    PASS
bootable stale database rejection   PASS
non-interference                    PASS
```

Important finding:

```text
pg_isready/read-only readiness != recovery acceptance
```

Versioned final harness:

```text
infra/local/postgres/recovery/cp06-failure-matrix-check.sh
```

Versioned final harness passed on implementation/runtime head `a1a6323210b3d7af66284006a754759fa9d08028` with N1–N7 PASS and non-interference preserved.

## 9. SC-011 status

Direct disposable prototype proved:

```text
B0 contained protected X                     PASS
accepted redaction removed X                  PASS
PGDATA destroyed                              PASS
independent ledger + B0 survived              PASS
old B0 physically resurrected X               PROVEN
target remained isolated                      PASS
ledger reconciliation removed X               PASS
NativeRef / MaterialStateRef continuity        PASS
current/history continuity                     PASS
runtime saw tombstone, not X                   PASS
real pgBackRest repo untouched                PASS
CP05 target untouched                          PASS
```

The final repository implementation corrects the prototype crash gap with PREPARED/COMMITTED evidence.

Definitive harness:

```text
infra/local/postgres/recovery/cp06-sc011-anti-resurrection-check.sh
```

It uses the real migration + real suppression library and creates B0 from a disposable source upgraded to `20260830_09`.

Definitive versioned SC-011 passed on implementation/runtime head `a1a6323210b3d7af66284006a754759fa9d08028` and is now local PASS.

## 10. Derived/object reopen boundary

Derived/search/vector/sync state is not canonical. After recovery it must be rebuilt/reconciled from accepted PostgreSQL before affected features reopen.

R2/object consistency is a separate recovery boundary. PostgreSQL restore does not prove referenced object recovery. Object-backed features remain closed until object verification/reconciliation is complete.

## 11. Current continuation

CP06 local acceptance is complete; do not repeat destructive CP06 proof merely to manufacture another identical PASS.

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
AWS selected production recovery = NOT YET PROVEN
```

This LOCAL closure does not prove AWS S3 activation, Versioning/Object Lock production acceptance, production RPO/RTO, R2 recovery, PowerSync/search/vector recovery implementation or the whole CP07 operator rehearsal.

The next recovery implementation boundary is CP07. Any CP07 code/infra/AWS activation still requires its own explicit gate.

## 12. CP06 closure rule

```text
CP06 LOCAL PASS / CLOSED
SC-011 PASS
CP07 NEXT / NOT STARTED
```

The closure is LOCAL only. AWS selected-stack acceptance and the whole CP07 operator rehearsal remain unproven.

## 13. CP07 boundary## 13. CP07 boundary

CP07 owns:

```text
whole clean operator rehearsal
measured end-to-end recovery evidence
operator runbook
real AWS selected-stack activation/acceptance
Versioning / Object Lock / retention/security proof
real cloud backup/WAL/restore/PITR readback
derived/object reopen procedure
final recovery integration closure
```

Do not activate AWS or production recovery infrastructure from this handoff without a separate explicit gate.