# DANTE Database System of Record

- **Status:** CURRENT / MATERIALIZED
- **PostgreSQL:** 18.6
- **Alembic head:** `20260830_09`
- **Schema:** `dante`
- **Scope:** current DANTE PostgreSQL architecture, Dictionary, mappings, migrations, lifecycle/recovery integrity, direct proof and documentation consistency
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Architecture decision:** `../decisions/ADR-010-postgresql-persistence-constitution.md`

## 1. Purpose

This directory is the durable current entry point for the DANTE database.

A developer must be able to start here and determine, without chat history:

```text
what database objects exist now
why each object exists
what every persisted field means
how identity, references, current state and history are represented
what PostgreSQL integrity is enforced
how retirement/redaction and recovery reconciliation work
what migration and SQLAlchemy mapping implement each object
what tests prove the current contract
```

Git/Alembic preserve chronology. Files in this directory describe the **current accepted database**, not obsolete implementation stages.

## 2. Current materialized database

The current accepted application schema is:

```text
tables               69
views                  5
routines              15
triggers              76
physical indexes      97
foreign keys           69
CHECK constraints     123

custom enum/domain      0
sequences               0
materialized views      0
partitioned tables      0
RLS policies            0
```

Current Alembic head:

```text
20260830_09
```

Current extensions required by DANTE:

```text
postgis             3.6.4
vector              0.8.6
pg_trgm             1.6
unaccent            1.1
pg_stat_statements  1.12
```

## 3. Current recovery/lifecycle addition

`20260830_09` materializes the WL-H10 / SC-011 retirement and anti-resurrection contract.

Canonical PostgreSQL now includes:

```text
dante.material_state_retirement
```

for explicit retirement/redaction continuity of material state while protected payload may be physically removed.

The current materialized facets covered by this contract are:

```text
schedule.placement
actual.realization
session.timing
routine.recurrence
event.recurrence
```

For an explicitly retired MaterialState:

```text
MaterialStateRef address/envelope remains truthful
permitted current/history continuity remains truthful
material_state_retirement records reason/time/suppression identity
protected payload must be absent
payload reinsertion is rejected by database-local integrity
```

This is not a universal soft-delete model and does not introduce a generic Entity/Thing root.

## 4. Recovery suppression ledger boundary

The external recovery suppression ledger is **technical disaster-recovery evidence only**. PostgreSQL remains the sole canonical DANTE persistence surface.

Protocol v1:

```text
PREPARED durable suppression intent
→ canonical PostgreSQL retirement/redaction transaction
→ canonical DB read-back verification
→ COMMITTED marker bound to PREPARED SHA-256
```

Recovery rules:

```text
valid PREPARED + COMMITTED pair
→ eligible for deterministic suppression reconciliation

PREPARED without COMMITTED
COMMITTED without PREPARED
hash mismatch
invalid/non-canonical record
→ recovery BLOCKED
```

The ledger must survive the relevant database-loss boundary independently from PGDATA and from the pgBackRest database-backup repository. Its retention must cover every retained database/object version that could still resurrect the protected payload.

## 5. Authority model

Current representations have distinct jobs and must agree:

```text
closed Domain / Logical / Physical
→ semantic and architectural authority

PostgreSQL Persistence Constitution + ADR-010
→ reusable PostgreSQL doctrine

Alembic
→ deployed schema evolution authority

SQLAlchemy MetaData / mappings
→ application mapping of deployed schema

real PostgreSQL introspection
→ observed materialized schema

Database Architecture & Reference
→ human-readable current database meaning

Database Dictionary
→ machine-readable current object contract

direct tests / recovery harnesses
→ executable proof
```

A mismatch is a defect.

Permanent invariant:

```text
DATABASE ARCHITECTURE & REFERENCE
        ≈
DATABASE DICTIONARY
        ≈
SQLALCHEMY METADATA / MAPPINGS
        ≈
ALEMBIC HEAD
        ≈
REAL POSTGRESQL SCHEMA
```

## 6. Current directory roles

```text
docs/database/
├── README.md
├── dante-postgresql-database.md
├── dante-postgresql-database-part-2.md ... part-19.md
├── dictionary/
│   ├── README.md
│   ├── scope.json
│   ├── schema/
│   ├── tables/
│   ├── views/
│   └── routines/
├── generated/    only when current generated artifacts exist
├── diagrams/     only when current useful diagrams exist
└── evolution/    only when a current complex rollout requires durable rationale
```

The multi-part reference is one logical reference. Where older prose conflicts with a later materialized contract, that conflict is a documentation defect to remove; readers are not expected to reconstruct historical supersession chains.

## 7. Security baseline

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
```

Current posture includes:

```text
DANTE objects owned by dante_owner
PUBLIC denied unless explicitly justified
runtime denied access to dante.alembic_version
runtime privileges bounded per object/column
material_state_retirement runtime access = SELECT only
integrity routines not directly executable by runtime
```

## 8. DANTE non-collapse obligations

Database work must preserve:

```text
technical address anchor != semantic Entity/Thing
NativeRef != ScopedRecordRef != MaterialStateRef != ExternalRef
current accepted state != newest inserted row
material history != universal event sourcing
retirement tombstone != generic soft-delete row
recovery suppression evidence != second canonical database
provider state != canonical DANTE state
derived/search state != canonical DANTE truth
Person != Account != Principal != Actor
Authority != AuthZ decision
absence / unknown != explicit negative
idempotency != semantic identity
```

## 9. Same-change rule

A structural database change is incomplete unless the same reviewed change updates, as applicable:

```text
Alembic migration
SQLAlchemy metadata/mappings
Database Dictionary
human-readable current database reference
generated artifacts/diagrams
direct tests
recovery/operational harnesses affected by head/topology
workstream documentation
```

No current document may intentionally retain a superseded head, topology, status or semantic contract as a historical snapshot. Git/Alembic provide history.

## 10. Current QA contract

QA must detect at least:

```text
undocumented real table/view/routine
stale Dictionary object
column/type/nullability/default drift
PK/FK/UQ/CHECK/index drift
trigger/routine/view drift
SQLAlchemy-vs-Alembic drift
migration head mismatch
owner/ACL drift
retired MaterialState with protected payload
payload reinsertion after retirement
ambiguous/tampered recovery suppression records
recovery target still in recovery when presented as accepted
structurally bootable but semantically unacceptable restore
```

`pg_isready` alone is never a traffic-reopen proof. Recovery acceptance requires `pg_is_in_recovery() = false` plus current structural/security/semantic verification and completed suppression reconciliation.

## 11. Current proof state

Direct local recovery evidence currently proves:

```text
pgBackRest foundation                         PASS
continuous WAL + FULL backup                  PASS
destructive isolated restore                  PASS
deterministic named-target PITR               PASS
negative failure matrix                       LOCAL PASS candidate
SC-011 mechanism prototype                    LOCAL PASS candidate
```

The versioned `20260830_09` implementation is not considered fully closed until fresh migration/DB QA and the definitive versioned SC-011 destructive harness pass on the exact branch HEAD.

Remote AWS selected-stack evidence and whole operator recovery closure belong to the PostgreSQL recovery workstream and are not implied by local proofs.

## 12. Acceptance bar

The Database System of Record succeeds when a new engineer can use the repository alone to:

```text
understand current architecture
locate every real persisted object
trace objects to migration + mapping + tests
understand integrity and ACL
understand current/history/lifecycle semantics
understand retirement/redaction and anti-resurrection behavior
identify what is canonical vs recovery/derived/provider state
run the current database/recovery acceptance procedures
```

The goal is not documentation volume. The goal is one coherent, inspectable, current database contract.