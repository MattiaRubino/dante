# DANTE PostgreSQL Database — Current Architecture & Reference

- **Status:** CURRENT / MATERIALIZED
- **Product:** DANTE
- **PostgreSQL:** 18.6
- **Schema:** `dante`
- **Alembic head:** `20260830_09`
- **Database SoR:** `README.md`
- **Persistence Constitution:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **ADR:** `../decisions/ADR-010-postgresql-persistence-constitution.md`

## 1. Purpose

This is the current human-readable architecture entry point for the DANTE PostgreSQL database.

It describes the database that exists **now**. Git and Alembic preserve implementation chronology.

The complete current contract is jointly represented by:

```text
this architecture/reference
+ Parts 2–19 for detailed family/object semantics
+ docs/database/dictionary/
+ Alembic migrations
+ SQLAlchemy mappings
+ direct PostgreSQL tests
```

A disagreement between those representations is a defect to reconcile, not a historical supersession puzzle for the reader.

## 2. Definition of the whole DANTE database

The database contains the maximum **non-speculative** persistence determined by accepted DANTE semantics and currently materialized capabilities.

It does not mean:

```text
one table per Domain concept
one table per API/screen
placeholder columns for undecided product behavior
dormant provider/runtime capabilities activated by anticipation
```

A field/table exists because its semantic or bounded technical role is explicit.

No global convention automatically creates:

```text
name
status
created_at
updated_at
deleted_at
is_deleted
metadata JSONB
version integer
```

## 3. Current materialized topology

```text
PostgreSQL          18.6
schema              dante
Alembic head        20260830_09

tables              69
views                 5
routines             15
triggers             76
indexes              97
foreign keys          69
CHECK constraints    123

enum/domain            0
sequences              0
materialized views      0
partitioned tables      0
RLS policies            0
```

Required extensions:

```text
postgis             3.6.4
vector              0.8.6
pg_trgm             1.6
unaccent            1.1
pg_stat_statements  1.12
```



### 3.1 Recovery operational entry points

The database semantics remain independent from the operator tooling, but the current repository owns a reproducible LOCAL recovery procedure:

```text
bootstrap  infra/local/postgres/recovery/bootstrap-local-recovery.sh
runner     infra/local/postgres/recovery/cp07-whole-recovery-rehearsal.sh
runbook    docs/operations/postgres-recovery-runbook.md
```

The runner is branch-agnostic and fail-closed on Git/upstream alignment. The bootstrap may create missing ignored LOCAL credentials and build the pinned recovery image, but it does not make the suppression ledger or backup repository canonical application state.

<!-- RECOVERY-REPRODUCIBILITY-PROOF: PENDING -->


## 4. Semantic/non-collapse architecture

DANTE persists specific semantic families rather than collapsing them into generic roots.

Forbidden global shortcuts:

```text
universal Entity / Thing table
universal Relationship / Edge table
canonical EAV / property bag
universal Rule(type,payload)
universal Fact / Version semantic root
universal event log as ontology
generic kind+uuid reference without DB integrity
JSONB as required-semantic escape hatch
PostgreSQL inheritance as ontology
```

Permanent distinctions include:

```text
planned/intended != Actual
Observation != Actual
Evidence != Provenance
Authority != Visibility
Responsibility != Participation
Ownership != Possession
Schedule != Actual
Schedule != Session
Schedule != Recurrence
Actual != Outcome
Actual != Observation
Recurrence != Occurrence
provider state != canonical state
retirement tombstone != protected payload
```

## 5. Native identity topology

Exactly 15 concepts own native DANTE identity:

```text
Person
Living Referent
Asset
Place
Content Artifact
Collective
Possibility
Goal
Plan
Activity
Event
Routine
Occurrence
Session
Observation
```

Each owns an independent canonical UUIDv7 identity shell. There is no semantic parent `entity` row.

The native identity baseline is intentionally narrow:

```text
SQL type                         uuid
ID policy                        UUIDv7
normal issuer                    backend application boundary
PK mutation                      forbidden in ordinary runtime
semantic parent FK               none
created_at / updated_at          none by convention
status                           none by convention
deleted_at / is_deleted          none by convention
metadata JSONB                   none by convention
```

Identity is not chronology. UUIDv7 ordering is technical locality only.

Contextual roles such as Actor/Subject/Resource do not become universal native owners.

## 6. Reference topology

DANTE preserves four reference families:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

Their SQL representation may all involve UUID values, but they are not interchangeable semantic contracts.

### 6.1 NativeRef

Homogeneous NativeRef targets use direct FKs to the concrete owner table when possible.

Genuinely heterogeneous NativeRef consumers use:

```text
dante.native_address
  native_ref     uuid PRIMARY KEY
  owner_family   text NOT NULL
```

`native_address` is a bounded technical address/control projection of an already-existing native owner. It does not mint a second identity and is not an Entity table.

The discriminator is schema-bounded to the 15 accepted native owner families. Database-local integrity verifies the referenced UUID exists in the concrete owner table selected by the discriminator. Consumer-specific eligibility remains bounded by the consuming semantic contract.

### 6.2 ScopedRecordRef

Addressable contextual records use:

```text
dante.scoped_address
  scoped_ref      uuid PRIMARY KEY
  scoped_family   text NOT NULL
```

only where independent contextual addressability/history/reconciliation warrants ScopedRecordRef.

This address table is also technical control infrastructure, never a semantic superclass.

### 6.3 MaterialStateRef

Material state is addressed through:

```text
dante.material_state_address
```

which binds one MaterialStateRef to exactly one accepted native/scoped owner and one bounded material facet.

MaterialState existence does **not** imply currentness.

### 6.4 ExternalRef

Provider/external identities remain separate from canonical DANTE identity. Provider mappings do not redefine NativeRef or canonical state.

## 7. Material state, current state and history

DANTE uses material history only where later meaning depends on the exact accepted state.

Rules:

```text
MaterialStateRef is stable addressability of one exact material state
materially changed state -> new MaterialStateRef
same old state may be reselected without minting a false new state
current state is selected explicitly
UUID ordering/insertion order never defines currentness
```

Bounded current-state controls include native/scoped owner + facet bindings.

Owner/facet-specific current-history rows preserve episodes of accepted currentness when that chronology is material.

History is not a universal event-sourcing root.

## 8. Transaction and concurrency discipline

The database preserves the application transaction model:

```text
outer application operation owns transaction
adapter may flush
adapter does not implicitly commit
READ COMMITTED default
```

Invariant enforcement escalates only as required:

```text
declarative constraint
→ expected-state / conditional mutation
→ deterministic row/key locking
→ SERIALIZABLE only for real predicate/write-skew pressure
```

Stale-write-sensitive material-state replacement uses expected MaterialStateRef or an equivalent explicit semantic precondition.

No external provider effect is represented as atomically rolled back with PostgreSQL.

## 9. Index discipline

Indexes exist for structural/integrity or demonstrated query need.

Review considers:

```text
PK/UNIQUE-backed indexes already present
FK lookup pressure
range/exclusion needs
actual temporal query pressure
actual FTS/trigram/vector use
```

Forbidden by default:

```text
index every FK blindly
index every timestamp
redundant PK/UNIQUE indexes
speculative GIN/GiST/vector indexes
speculative partitioning/sharding
```

## 10. Typed temporal contract

DANTE has no universal `temporal_value` table.

Current temporal representation preserves source meaning:

| Meaning | PostgreSQL representation | Rule |
|---|---|---|
| civil/date-only | `date` | never invent midnight UTC |
| floating local datetime | `timestamp without time zone` | no implicit device zone |
| named-zone local datetime | local timestamp + `zone_id` | IANA zone remains explicit |
| consequential resolved named-zone datetime | local + zone + `resolved_at timestamptz` | retain accepted historical instant |
| absolute instant | `timestamptz` | display zone is not identity |
| date range | `daterange` | owning family defines bounds |
| absolute instant range | `tstzrange` | owning family defines bounds |
| local/zoned range | typed local boundaries + explicit frame/zone | do not fake UTC semantics |
| elapsed duration | exact elapsed representation owned by family | do not mix calendar-relative semantics |
| coarse/partial precision | typed value + bounded precision when defined | no invented precision |

`timetz` is not used as a substitute for IANA named-zone semantics.

A later timezone-database change must not rewrite a consequential historical `resolved_at` value DANTE already accepted.

## 11. Place / PostGIS boundary

Canonical Place identity remains:

```text
dante.place(place_ref uuid PRIMARY KEY)
```

and does not imply:

```text
Place = postal address
Place = coordinates
Place = geometry
Place = provider Place ID
```

PostGIS is available, but no universal Place geometry/geography/lat-lon column or spatial index is activated merely because the extension exists.

The first future canonical spatial facet must define its exact shape, CRS/SRID, geometry-vs-geography semantics, provenance/correction/history and demonstrated index/query need before migration.

## 12. Security / privilege topology

Current roles:

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
```

Provisioning owns role/schema/security foundation. Business migrations own exact object ACL changes for the objects they create/change.

Permanent posture:

```text
PUBLIC default deny
no blanket business-object DML from provisioning
runtime privilege bounded by object/column contract
migration history unavailable to runtime
integrity routines not directly executable by runtime
UUIDv7 semantic identities do not justify blanket sequence privilege
```

Immutable material-state/history/control surfaces do not receive UPDATE/DELETE merely because they are tables.

## 13. Schedule

Schedule is accepted placement, not Actual execution and not a capacity claim.

Current accepted placement uses typed material state under facet:

```text
schedule.placement
```

Typed payload families include exact representations for:

```text
date span
floating local
named-zone local
absolute instant/range
```

The database does not manufacture qualitative day-part clock boundaries such as `afternoon = 12:00..18:00` without an accepted vocabulary.

Schedule history records which exact placement state was accepted as current over time; currentness is not inferred from newest row.

A Schedule cannot survive as a ceremonial shell with no accepted placement/currentness contract.

## 14. Actual

Actual records canonical realization truth and remains separate from Schedule/Outcome/Observation.

Absence of Actual is unknown/absent, not an explicit negative.

`actual.realization` uses explicit material state. When realization timing is based on a Session, the exact Session timing MaterialStateRef is retained rather than only Session identity, so later Session correction cannot rewrite historical Actual basis.

## 15. Session

Session owns execution chronology; timing is state, not identity.

Current `session.timing` supports typed absolute/elapsed forms and pause state where admitted. Precision can be exact/approximate/rounded where the concrete state supports it; imported/coarse timing is not coerced into false exactness.

A canonical Session is not permitted to remain an empty UUID shell with no required timing state at its consistency boundary.

There is no universal Session `running/paused/done` lifecycle enum and no global non-overlap invariant across unrelated Sessions.

## 16. Recurrence and Occurrence

Recurrence is a structured rule/specification, not a universal `Rule(type,payload)` row and not provider RRULE canonical truth.

Current materialized source-owned facets are:

```text
routine.recurrence
event.recurrence
```

Baseline deterministic recurrence families retain typed relational structures for:

```text
calendar wall-clock
elapsed interval
quota per period
cyclic positional
```

No generic recurrence JSON/DSL, hidden invalid-date policy, hidden DST fallback or semantic quota ordinal is introduced.

An Occurrence is distinct from its Recurrence source and from Schedule/Actual.

Materialized occurrence-generation context retains the exact governing recurrence MaterialStateRef needed to explain why an expectation existed. A later recurrence revision does not make an already-materialized Occurrence appear to have been generated by the newer rule.

Virtual future expectations need not be eagerly persisted. Native Occurrence UUID identity is minted when an expectation becomes persistently distinguishable through scheduling, exception, actual/participation/evidence/provider history or another material relation.

Quota recurrence does not fabricate first/second/third semantic slot identity before an expectation is actually differentiated.

## 17. Current materialized retirement/redaction contract

Alembic `20260830_09` materializes WL-H10 / SC-011 through:

```text
dante.material_state_retirement
```

Columns:

```text
material_state_ref
retirement_code       redacted | unavailable
retired_at
recovery_suppression_ref
```

Retirement is append-only.

Supported materialized facets:

```text
schedule.placement
actual.realization
session.timing
routine.recurrence
event.recurrence
```

For a retired MaterialState:

```text
MaterialStateRef address/envelope remains
permitted current/history continuity remains
retirement reason/time remains
protected facet payload/selectors must be absent
later payload reinsertion is rejected
```

This is a narrow lifecycle mechanism, not global soft delete.

Database-local retirement-aware routines:

```text
dante.enforce_material_state_retirement()
dante.enforce_schedule_placement_totality()
dante.enforce_actual_realization_basis()
dante.enforce_session_timing_totality()
dante.enforce_recurrence_aggregate_integrity()
```

The retirement integrity trigger is deferred so one transaction can remove all protected payload and insert the tombstone atomically; commit rejects a tombstone whose protected payload still survives.

## 18. Recovery suppression boundary

An old physical backup can predate the PostgreSQL tombstone. Therefore DANTE keeps minimal recovery suppression evidence independently from both canonical PGDATA and the pgBackRest database repository.

This evidence is technical disaster-recovery control only, not canonical application persistence.

Protocol:

```text
PREPARED
→ canonical PostgreSQL retirement/redaction transaction
→ canonical DB read-back verification
→ COMMITTED bound to PREPARED SHA-256
```

Recovery blocks on:

```text
missing/unavailable `records/` directory
unexpected entry inside `records/`
duplicate MaterialStateRef suppression target
PREPARED without COMMITTED
COMMITTED without PREPARED
identity/target mismatch
prepared hash mismatch
non-canonical/invalid record
```

A PREPARED record alone never authorizes automatic deletion because the database transaction might never have committed.

Suppression evidence must be retained for the complete resurrection horizon: it cannot expire while a retained database/WAL/object version could still reintroduce the protected payload.

## 19. Restore acceptance

Successful physical startup does not equal accepted DANTE recovery.

Direct negative testing established that PostgreSQL can accept read-only connections during recovery and later fail because the requested target/WAL is unreachable.

Therefore `pg_isready` alone is insufficient.

At minimum traffic reopen requires:

```text
pg_is_in_recovery() = false
PostgreSQL 18.6
Alembic 20260830_09
current topology 69|5|15|76|97|69|123|0|0|0
owners / roles / ACL
required extension versions
semantic state checks
complete suppression-ledger reconciliation
zero protected payload for retired states
derived/object reconciliation gate
```

A physically bootable but structurally/semantically stale target is rejected.

## 20. Provider and derived boundaries

Provider/integration state is not canonical DANTE state.

Derived/search/vector/sync state must never override restored PostgreSQL. A stale derived store remains unavailable until discarded/rebuilt from accepted PostgreSQL or independently reconciled.

Object-store consistency is separate: a PostgreSQL restore does not prove referenced R2/object availability or correctness.

## 21. Current exact proof obligations

Current direct database tests must reconcile:

```text
Database Architecture & Reference
Database Dictionary
SQLAlchemy mappings
Alembic head
real PostgreSQL introspection
owners / ACL
integration tests
recovery harnesses
```

Expected topology:

```text
69|5|15|76|97|69|123|0|0|0
```

Expected head:

```text
20260830_09
```

Recovery-specific proof additionally requires:

```text
retirement with surviving payload rejects
valid retirement preserves envelope/history and removes payload
retirement UPDATE/DELETE rejects
payload reinsertion after retirement rejects
suppression ledger ambiguity/tamper blocks
old B0 can physically resurrect X
recovery reconciliation suppresses X before reopen
```

## 22. Detailed current reference map

This document deliberately does not retain the former chronological candidate/checkpoint narrative.

Current detail is distributed by responsibility:

```text
Parts 2–18
→ detailed accepted object/family/reference/integrity semantics

Part 19
→ current retirement/redaction/recovery anti-resurrection contract

Database Dictionary
→ exact current per-object columns/keys/checks/indexes/triggers/ACL/mappings/proof refs

Persistence Constitution + ADR-010
→ reusable transaction/index/security/migration doctrine

Alembic + SQLAlchemy
→ executable materialization
```

If a Part or Dictionary object conflicts with this current architecture or the materialized schema, it must be reconciled; historical ordering is not an override rule.

## 23. Same-change rule

A database evolution is incomplete unless the same reviewed change updates all affected current representations:

```text
Alembic
SQLAlchemy
Database Dictionary
human-readable database reference
recovery/operational tooling affected by topology/head
executable tests
current workstream documentation
```

## 24. Acceptance bar

A new engineer must be able to derive the same present database contract from repository documentation, migrations, mappings, Dictionary and live PostgreSQL without conversation memory.

The goal is not maximum prose. The goal is full current knowledge coverage with no stale/deprecated contract left in the working tree.
