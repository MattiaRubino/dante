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

## Active PostgreSQL recovery workstream

```text
repo       MattiaRubino/dante
branch     feature/postgres-recovery
worktree   /home/mattia/projects/dante-postgres-recovery
```

Read in this order:

1. `postgres-recovery.md`
2. `postgres-recovery-execution-plan.md`
3. `postgres-recovery-live-handoff-2026-08-29.md`
4. `../database/README.md`
5. `../database/dante-postgresql-database-part-19.md`

Current recovery state:

```text
CP01 Recovery Contract / Bootstrap      CLOSED / CONTRACT FROZEN
CP02 pgBackRest Foundation              LOCAL PASS
CP03 Continuous WAL + Backup            LOCAL PASS
CP04 Destructive / Isolated Restore     LOCAL PASS
SC-031 destructive local restore        PASS
CP05 Deterministic PITR                 LOCAL PASS
PSV-40 local archive/restore/PITR       PASS
CP06 Failure + Semantic Recovery        IMPLEMENTED / FINAL LOCAL QA PENDING
Failure Matrix A                        DIRECT PROTOTYPE EVIDENCE PASS CANDIDATE
SC-011 mechanism prototype              DIRECT LOCAL PASS CANDIDATE
SC-011 versioned final harness          IMPLEMENTED / NOT YET RUN
current DB evolution                    Alembic 20260830_09
current DB topology                     69|5|15|76|97|69|123|0|0|0
CP07 Whole Recovery QA + Runbook        NOT STARTED
AWS S3 selected topology                NOT ACTIVATED
```

CP06 is **not closed merely because implementation exists**. Closure requires direct execution against the exact current branch HEAD of:

```text
current database migration/catalog/ACL tests
suppression-ledger unit tests
versioned CP06 failure matrix
versioned definitive SC-011 anti-resurrection rehearsal
quality/static checks required by the backend
current-documentation reconciliation
```

Only after those are green may the workstream record state:

```text
CP06 LOCAL PASS / CLOSED
SC-011 PASS
```

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
successful LOCAL proof != selected AWS production proof
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

The selected production recovery topology remains:

```text
pgBackRest
→ AWS S3 Standard eu-south-1
→ Versioning
→ Object Lock GOVERNANCE
→ finite policy-bound retention
```

It is **not activated or directly proven** by the current LOCAL workstream evidence.

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