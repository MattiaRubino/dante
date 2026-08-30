<!-- DANTE-CANONICAL-CONTINUATION document="dante-postgresql-database.md" follows="dante-postgresql-database-part-18.md" -->

# DANTE PostgreSQL Database Architecture & Reference — Part 19

**Status:** CURRENT / MATERIALIZED  
**Scope:** MaterialState retirement, redaction continuity, recovery suppression and anti-resurrection  
**PostgreSQL:** 18.6  
**Alembic head:** `20260830_09`  
**Current topology:** 69 tables / 5 views / 15 routines / 76 triggers / 97 indexes / 69 FKs / 123 CHECKs  

---

## 56. MaterialState retirement and anti-resurrection

### 56.1 Problem boundary

A valid DANTE retirement/redaction can happen after an older database backup was created.

If canonical PostgreSQL is later lost and the older backup is restored, raw restored bytes may contain protected payload that is no longer permitted current truth.

Therefore:

```text
successful backup != successful semantic recovery
successful restore != permission to expose restored payload
restored historical bytes != automatically accepted current truth
```

The database and recovery procedure must preserve WL-H10:

```text
referent/state existed
payload may later become unavailable/redacted
minimal truthful address/tombstone/history continuity remains
stable identity/reference is not silently reused
old backups may not silently resurrect retired payload
```

### 56.2 Canonical retirement table

Current PostgreSQL materializes:

```text
dante.material_state_retirement
```

Columns:

```text
material_state_ref          uuid        PRIMARY KEY
retirement_code             text        NOT NULL
retired_at                  timestamptz NOT NULL
recovery_suppression_ref    uuid        NOT NULL UNIQUE
```

Current constraints:

```text
material_state_ref
→ FK dante.material_state_address(material_state_ref)
→ ON DELETE NO ACTION

retirement_code
→ redacted | unavailable

retired_at
→ finite timestamp

recovery_suppression_ref
→ UUIDv7
```

`recovery_suppression_ref` is a narrow technical recovery correlation identifier. It is **not** a new Domain identity family and does not redefine NativeRef / ScopedRecordRef / MaterialStateRef / ExternalRef.

### 56.3 Canonical lifecycle semantics

Retirement is append-only.

Ordinary runtime authority may read retirement state but may not insert/update/delete it directly.

A committed retirement means:

```text
MaterialStateRef address/envelope remains truthful
permitted current/history rows remain truthful
retirement reason/time remains truthful
protected facet payload is absent
```

A retirement row is not permission to erase identity/address/history continuity that the accepted model still requires.

### 56.4 Materialized facets covered

Current retirement integrity covers exactly these materialized facets:

```text
schedule.placement
actual.realization
session.timing
routine.recurrence
event.recurrence
```

The envelope/state tables remain addressable; protected typed payload/selectors may be removed as part of a governed retirement transaction.

#### Schedule

Retained envelope/history:

```text
schedule_placement_state
schedule_placement_current_history
material_state_address
current-state bindings where still semantically valid
```

Retirable protected payload:

```text
schedule_placement_date_state
schedule_placement_floating_local_state
schedule_placement_named_zone_state
schedule_placement_absolute_state
```

#### Actual

Retained envelope/history:

```text
actual_realization_state
actual_realization_current_history
material_state_address
```

Retirable protected payload:

```text
actual_realization_timing
actual_realization_session_basis
```

#### Session

Retained envelope/history:

```text
session_timing_state
session_timing_current_history
material_state_address
```

Retirable protected payload:

```text
session_timing_absolute
session_timing_elapsed
session_timing_pause
```

#### Routine/Event Recurrence

Retained envelope/history:

```text
routine_recurrence_state
event_recurrence_state
routine_recurrence_current_history
event_recurrence_current_history
material_state_address
```

Retirable selector/payload families include boundary, calendar, wall-time/weekday/month-day/ordinal/year selector rows, elapsed, quota, cyclic and cycle-position rows.

### 56.5 Deferred retirement validator

Current routine:

```text
dante.enforce_material_state_retirement()
```

is installed as a DEFERRABLE INITIALLY DEFERRED constraint trigger on `material_state_retirement`.

This allows one owner-controlled transaction to:

```text
remove all protected payload
insert the retirement tombstone
commit
```

At commit the validator requires:

```text
retirement target has a valid MaterialState address
facet is one of the supported materialized facets
no protected payload remains
retirement row is append-only
```

Attempted UPDATE/DELETE of the retirement row is rejected.

### 56.6 Existing facet validators are retirement-aware

These current routines now distinguish live vs retired state:

```text
dante.enforce_schedule_placement_totality()
dante.enforce_actual_realization_basis()
dante.enforce_session_timing_totality()
dante.enforce_recurrence_aggregate_integrity()
```

For a live state they preserve their normal exact payload contract.

For a retired state they require zero protected payload/selectors and reject payload resurrection.

This means anti-resurrection is enforced both during initial retirement and against later attempts to reinsert payload for the same MaterialStateRef.

### 56.7 External recovery suppression ledger

A PostgreSQL tombstone inside canonical PGDATA is not sufficient by itself: an older backup may predate that tombstone.

Recovery therefore uses minimal independently surviving suppression evidence outside:

```text
canonical PGDATA
pgBackRest database-backup repository
```

The ledger is technical recovery control only. It does not become an application datastore or a second source of canonical DANTE truth.

Record protocol v1:

```text
PREPARED
→ canonical retirement/redaction transaction
→ canonical DB read-back verification
→ COMMITTED
```

PREPARED records include:

```text
record_version
state = PREPARED
recovery_suppression_ref
target_reference_family = MaterialStateRef
material_state_ref
facet_code
effect = suppress_payload
retirement_code
accepted_at
```

COMMITTED records include:

```text
record_version
state = COMMITTED
recovery_suppression_ref
material_state_ref
prepared_sha256
committed_at
```

The COMMITTED marker cryptographically binds to the canonical bytes of PREPARED.

### 56.8 Crash/ambiguity rule

The external ledger must never guess whether a canonical retirement actually committed.

Therefore:

```text
PREPARED + matching COMMITTED
→ valid committed suppression evidence

PREPARED without COMMITTED
→ recovery BLOCKED

COMMITTED without PREPARED
→ recovery BLOCKED

prepared hash mismatch
→ recovery BLOCKED

non-canonical/invalid JSON
→ recovery BLOCKED
```

This prevents both unsafe resurrection and unsafe automatic deletion caused by an uncommitted PREPARED intent.

### 56.9 Recovery reconciliation sequence

A restored PostgreSQL target remains closed to application traffic while anti-resurrection reconciliation executes.

Required order:

```text
1. restore/PITR PostgreSQL target
2. require PostgreSQL recovery to finish / promote
3. verify current migration/schema contract or apply approved current schema evolution while isolated
4. load and validate all committed suppression evidence
5. BLOCK on ambiguous/tampered ledger state
6. for each valid committed suppression:
     preserve MaterialStateRef envelope/history
     ensure material_state_retirement exists with matching suppression identity
     remove protected resurrected payload/selectors
7. verify zero retired payload remains
8. verify owners/roles/ACL/extensions/current topology
9. verify semantic recovery checks
10. verify derived/object reconciliation gates
11. only then permit traffic reopen
```

### 56.10 Traffic-reopen gate

`pg_isready` is insufficient.

Direct failure testing proved PostgreSQL can report readiness for read-only connections while still replaying recovery and later fail because a required target/WAL is unreachable.

Traffic reopen requires at least:

```text
pg_is_in_recovery() = false
PostgreSQL 18.6
Alembic 20260830_09
current topology 69|5|15|76|97|69|123|0|0|0
DANTE ownership/role/ACL checks
required extension versions
suppression ledger fully reconciled
zero protected payload for retired MaterialStates
semantic acceptance checks
derived/object reconciliation gate satisfied
```

### 56.11 Recovery suppression retention

Suppression evidence must remain available for the full resurrection horizon.

It may not expire while any retained object can still reintroduce the protected payload, including as applicable:

```text
pgBackRest FULL/diff/incremental backup
archived WAL required by a retained recovery point
S3 versioned backup objects
object-store versions/backups that can reintroduce referenced protected state
```

Production retention must therefore reconcile:

```text
pgBackRest retention
S3 Versioning
Object Lock GOVERNANCE
S3 lifecycle
privacy/deletion policy
PITR continuity
suppression-ledger retention
```

### 56.12 Security posture

```text
material_state_retirement owner    dante_owner
runtime table privilege            SELECT only
PUBLIC                              denied
migrator direct runtime role        bounded by normal migration boundary
integrity routine EXECUTE runtime   denied
```

The recovery ledger production identity must be scoped only to its recovery repository and must not gain authority over canonical application data.

### 56.13 Current direct proof obligations

The definitive local acceptance must prove against the versioned `20260830_09` implementation:

```text
fresh database -> head
head -> 20260826_08 -> head
Alembic check clean
current topology exact
Dictionary ↔ SQLAlchemy ↔ PostgreSQL exact
runtime ACL exact
retirement with surviving payload rejects
valid retirement removes payload and retains envelope/history
retirement UPDATE/DELETE rejects
payload reinsertion after retirement rejects
PREPARED without COMMITTED blocks
COMMITTED without PREPARED blocks
tampered hash blocks
old B0 physically resurrects protected X
recovery target remains isolated
valid committed ledger reconciles X away
NativeRef / MaterialStateRef continuity remains truthful
real pgBackRest repository remains untouched by disposable SC-011 proof
```

### 56.14 Derived and object boundaries

SC-011 database anti-resurrection does not by itself prove external derived/object consistency.

Permanent rule:

```text
restored PostgreSQL = canonical candidate after semantic reconciliation
stale derived/search/vector/sync state != authority
```

Disposable derived stores must be discarded/rebuilt or independently reconciled before they are allowed to serve state that could contradict restored PostgreSQL.

Object-store recovery/reconciliation is a separate boundary. PostgreSQL recovery closure must state which object checks remain required before traffic reopen rather than pretending database recovery proves object availability.

### 56.15 Current status

The anti-resurrection architecture has direct local prototype proof. The repository now materializes the canonical retirement table, recovery ledger protocol and retirement-aware validators at `20260830_09`.

Final SC-011 PASS is earned only after the definitive **versioned** harness runs successfully on the exact current branch HEAD. Until then the implementation is materialized but the checkpoint is not closed.