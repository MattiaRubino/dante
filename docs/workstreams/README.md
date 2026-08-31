# DANTE Workstream Records

- **Status:** CURRENT INDEX
- **Rule:** current subsystem/workstream files describe present truth; Git/PR history preserves chronology.

## Current authority

Protected-main project truth is owned by:

- `../PROJECT-STATUS.md`
- `../ROADMAP.md`

Branch-local workstream files may describe additional unmerged implementation only on their own branch. They never silently become protected-main truth.

## Current durable subsystem entry points

### Database

- `../database/README.md` — current DANTE PostgreSQL System of Record.
- `../database/dante-postgresql-database.md` + Parts 2–19 — human-readable database reference.
- `../database/dictionary/` — machine-readable current database contract.

### Backend

- `backend-scaffold.md` — accepted backend foundation/closure record.

### Frontend

- `frontend-foundation.md`
- `frontend-materialization.md`
- `frontend-materialization-integration.md`
- `../frontend/access.md`

### Engineering / architecture

- `engineering-foundation.md`
- `physical-model.md`
- `pre-physical-coherence.md`

### Domain / Logical

Current semantic authority lives in:

- `../domain/README.md`
- `../logical-model/README.md`

## PostgreSQL recovery workstream

Closure/integration-candidate record:

```text
repo       MattiaRubino/dante
branch     feature/postgres-recovery
worktree   /home/mattia/projects/dante-postgres-recovery
```

The permanent bootstrap/CP07 runner does **not** depend on that branch/worktree name; it accepts any clean attached branch exactly aligned with its configured upstream.

Read in this order:

1. `postgres-recovery.md`
2. `postgres-recovery-execution-plan.md`
3. `../database/README.md`
4. `../database/dante-postgresql-database-part-19.md`
5. `../operations/postgres-recovery-runbook.md`

Current recovery state:

```text
CP01 Recovery Contract / Bootstrap      CLOSED / CONTRACT FROZEN
CP02 pgBackRest Foundation              LOCAL PASS
CP03 Continuous WAL + Backup            LOCAL PASS
CP04 Destructive / Isolated Restore     LOCAL PASS
SC-031 destructive local restore        PASS
CP05 Deterministic PITR                 LOCAL PASS
PSV-40 local archive/restore/PITR       PASS
CP06 Failure + Semantic Recovery        LOCAL PASS / CLOSED
Failure Matrix                          VERSIONED LOCAL PASS
SC-011 mechanism prototype              DIRECT LOCAL PASS
SC-011 versioned final harness          LOCAL PASS
current DB evolution                    Alembic 20260830_09
current DB topology                     69|5|15|76|97|69|123|0|0|0
CP07 Whole Recovery QA + Runbook        LOCAL PASS / CLOSED
remote backup provider                  TBD / NOT ACTIVATED
```

CP06 is **LOCAL PASS / CLOSED** on the directly exercised local contract. The implementation/runtime proof head is `a1a6323210b3d7af66284006a754759fa9d08028`; the closure commit itself is documentation-only and therefore has a later SHA.

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

Current recovery truth:

```text
CP06 = LOCAL PASS / CLOSED
SC-011 = PASS
CP07 = LOCAL PASS / CLOSED
database-local reopen = PASS
remote backup provider = TBD / NOT ACTIVATED
production/cloud recovery = NOT CLAIMED
```

The recovery workstream is closed for the current LOCAL project phase. Remote-provider production recovery remains a future deployment checkpoint, not an unfinished CP07 item.

## Recovery permanent rules

```text
PostgreSQL = sole canonical persistence authority
backup repository != canonical truth
restored bytes != accepted semantic truth
pg_isready != traffic-open proof
pg_is_in_recovery=false + semantic acceptance required
old backup restore != permission to resurrect retired payload
recovery suppression ledger != second canonical database
stale derived/search/vector/sync state != authority
successful LOCAL proof != remote/cloud production proof
```

The recovery suppression ledger uses:

```text
PREPARED
→ canonical PostgreSQL retirement/redaction commit
→ canonical read-back verification
→ COMMITTED bound to PREPARED SHA-256
```

Ambiguous/tampered suppression evidence blocks recovery.

## Production boundary

```text
remote backup provider      TBD
remote provider activated   NO
production/cloud recovery   NOT CLAIMED
```

The local recovery workstream must close independently of a cloud vendor. A future remote provider is selected only when deployment requires it and only after provider-specific backup/WAL/restore/PITR acceptance.

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

The permanent runner is being hardened for branch-agnostic fresh-clone reuse; exact-head proof is recorded below after the hardened implementation itself is rerun.

### Reproducible LOCAL recovery exact-head proof

Implementation/runtime proof HEAD:

```text
789e946a8f096b52f2a440b967120cc3e0a340a3
```

Reusable-bootstrap / runner proof:

```text
validation clone started without recovery secrets         PASS
first bootstrap created all three LOCAL secrets           PASS
second bootstrap preserved exact secret contents          PASS
secret files mode 0600 / ignored / untracked              PASS
repository Compose validation                              PASS
repository-built pinned recovery image                     PASS
runner independent from feature/postgres-recovery name     PASS
clean attached branch + configured upstream gate           PASS
whole backend QA on exact hardened tree                    PASS
pre-push whole CP07 rehearsal                              PASS
exact pushed implementation HEAD whole CP07 rehearsal      PASS
database-local reopen                                      PASS
deterministic PITR A-present / B-absent                    PASS
old protected X physical resurrection                      PROVEN
ledger anti-resurrection reconciliation                    PASS
payload reinsertion after retirement                       REJECTED
normal LOCAL / retained recovery / CP05 non-interference   PASS
disposable cleanup                                         PASS
remote backup provider                                     TBD / NOT ACTIVATED
production/cloud recovery                                  NOT CLAIMED
```

Exact-head runtime relation:

```text
branch          feature/postgres-recovery
upstream        origin/feature/postgres-recovery
recovery image  dante-postgres-recovery:18.6-pgbackrest-2.59.1
```

Measured LOCAL observations from the exact pushed hardened runner:

```text
backup label                              20260831-120208F
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

These are LOCAL rehearsal observations, not production RPO/RTO targets.



## Operational continuation rule

Before continuing an active workstream:

1. verify exact branch/worktree/remote relation;
2. read current subsystem authority;
3. read the active branch-local workstream record;
4. use repository/code/tests over conversation memory;
5. do not write to protected `main`;
6. do not treat selected/unimplemented capability as PASS;
7. keep current docs aligned with the materialized repository contract.

## Carry-forward engineering rules

```text
SELECTED != IMPLEMENTED
IMPLEMENTED != PROVEN
PROVEN != CLOSED UNTIL THE CHECKPOINT CONTRACT IS SATISFIED
UNMERGED BRANCH TRUTH != protected-main TRUTH
VERSION-SENSITIVE CLAIMS REQUIRE CURRENT EVIDENCE
CURRENT DOCUMENTATION != DEPRECATED SNAPSHOT
```
