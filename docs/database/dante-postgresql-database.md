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

This document is the current human-readable architecture entry point for the DANTE PostgreSQL database.

It explains the database that exists **now**. Git and Alembic preserve historical implementation chronology.

The complete object-level contract is jointly represented by:

```text
this current architecture/reference
+ Parts 2–19 for detailed object/family semantics
+ docs/database/dictionary/
+ Alembic migrations
+ SQLAlchemy mappings
+ direct PostgreSQL tests
```

A conflict between those representations is a defect to reconcile, not a supersession puzzle for the reader.

## 2. Current materialized topology

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

The database remains one explicit PostgreSQL schema with owner/migrator/runtime separation.

## 3. Semantic architecture

DANTE persists specific semantic families rather than collapsing them into universal rows.

Forbidden shortcuts remain:

```text
universal Entity / Thing table
universal Relationship / Edge table
canonical EAV / property bag
universal Rule(type,payload)
universal Fact / Version semantic root
provider state treated as canonical state
JSONB as an escape hatch for required semantics
```

The physical database preserves upstream semantic distinctions even when multiple concepts share SQL types.

## 4. Identity and reference topology

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

Native identities use stable UUIDv7 values. UUID ordering is technical locality, never semantic chronology.

DANTE keeps four reference families distinct:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

Shared address tables are bounded technical integrity structures, not semantic parents:

```text
dante.native_address
dante.scoped_address
dante.material_state_address
```

Homogeneous relations use direct FKs where possible. Heterogeneous references use bounded address/control rows plus database-enforced eligibility.

## 5. Current/material/history topology

Current state is explicit and must never be inferred from UUID ordering or newest insertion.

MaterialStateRef represents stable addressability of a material interpretation/state. It is not a universal version/event root.

Current materialized facets include:

```text
schedule.placement
actual.realization
session.timing
routine.recurrence
event.recurrence
```

Each facet has an explicit envelope/address contract plus its specific typed payload/history structures.

## 6. Retirement, redaction and anti-resurrection

The current database materializes WL-H10 / SC-011 through:

```text
dante.material_state_retirement
```

A retirement row is append-only and identifies:

```text
material_state_ref
retirement_code       redacted | unavailable
retired_at
recovery_suppression_ref
```

The retirement table is not a generic soft-delete mechanism. It is a narrow canonical lifecycle record for materialized MaterialState facets whose protected payload may later be unavailable while identity/address/history continuity must remain truthful.

For a retired MaterialState:

```text
MaterialStateRef address/envelope remains
permitted current/history continuity remains
retirement reason/time remains
protected facet payload must be absent
payload reinsertion after retirement is rejected
```

The following database-local validators are retirement-aware:

```text
dante.enforce_schedule_placement_totality()
dante.enforce_actual_realization_basis()
dante.enforce_session_timing_totality()
dante.enforce_recurrence_aggregate_integrity()
dante.enforce_material_state_retirement()
```

The retirement integrity trigger is deferred so one transaction can remove all protected payload and insert the tombstone atomically; at commit, a tombstone with surviving protected payload is rejected.

## 7. Recovery suppression boundary

Database backup/restore alone cannot know about a redaction accepted **after** an older backup was created. DANTE therefore keeps minimal independently surviving recovery suppression evidence outside PGDATA and outside the pgBackRest database repository.

That evidence is technical recovery control, not canonical application truth.

Protocol v1:

```text
PREPARED
→ canonical PostgreSQL retirement/redaction transaction
→ canonical read-back verification
→ COMMITTED bound to PREPARED SHA-256
```

Recovery handling:

```text
valid committed pair
→ suppression may be reconciled deterministically before reopen

prepared without commit
committed without prepare
hash mismatch / tamper / invalid shape
→ recovery BLOCKED
```

The suppression ledger must survive the same disaster class that can destroy canonical PGDATA and must be retained at least as long as any retained backup/object version could resurrect the protected payload.

## 8. Restore acceptance

Successful physical startup does not equal accepted DANTE recovery.

A target may transiently accept read-only connections while PostgreSQL is still replaying recovery. Therefore `pg_isready` alone is insufficient for traffic reopen.

At minimum, accepted recovery requires:

```text
pg_is_in_recovery() = false
current PostgreSQL version
current Alembic head
current topology
owners / roles / ACL
required extensions
semantic state checks
suppression-ledger reconciliation
anti-resurrection checks
derived/object reconciliation gate
```

A physically bootable but structurally or semantically stale database is rejected.

## 9. Security posture

Current role model:

```text
dante_owner      NOLOGIN object owner
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application identity
```

Core posture:

```text
PUBLIC default deny on DANTE objects
bounded runtime grants only
runtime denied dante.alembic_version
integrity routines not directly executable by runtime
material_state_retirement runtime access = SELECT only
ordinary runtime DELETE is not the lifecycle mechanism
```

## 10. Provider and derived boundaries

Provider/integration state is not canonical DANTE truth.

Derived/search/vector/sync state must never override restored PostgreSQL. After recovery, disposable derived state may remain unavailable until rebuilt/reconciled from accepted canonical PostgreSQL.

Object-store consistency is a separate recovery boundary; a PostgreSQL restore by itself does not prove referenced object availability or consistency.

## 11. Current proof obligations

The database contract is complete only when these representations agree:

```text
Database Architecture & Reference
Database Dictionary
SQLAlchemy mappings
Alembic head
real PostgreSQL introspection
integration tests
recovery harnesses
```

Current topology expected by direct tests:

```text
69|5|15|76|97|69|123|0|0|0
```

Current Alembic head expected by direct tests:

```text
20260830_09
```

## 12. Detailed reference

Parts 2–18 contain detailed family/object semantics that remain valid. Part 19 is the current lifecycle/recovery continuation for MaterialState retirement and anti-resurrection.

No Part is permission to retain a fact that conflicts with the materialized current database. If detailed prose becomes false after an accepted forward evolution, it must be reconciled in the same database change.

## 13. Permanent non-collapse rules

```text
specific truthful semantics > generic abstraction
planned/intended != Actual
Observation != Actual
Evidence != Provenance
Authority != Visibility
Responsibility != Participation
Ownership != Possession
absence != false
canonical != provider state
recovery suppression evidence != canonical database
retirement tombstone != payload
identity != chronology
```

## 14. Acceptance bar

The database is acceptable only when an engineer can derive the same present contract from code, migrations, Dictionary, current documentation and live PostgreSQL without relying on conversation memory or historical supersession chains.