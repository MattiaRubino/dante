# DANTE Database System of Record

- **Status:** CURRENT / MATERIALIZED
- **PostgreSQL:** 18.6
- **Alembic head in this tree:** `20260830_09`
- **Schema:** `dante`
- **Scope:** current DANTE PostgreSQL architecture, Dictionary, mappings, migrations, lifecycle/recovery integrity, direct proof and documentation consistency
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Architecture decision:** `../decisions/ADR-010-postgresql-persistence-constitution.md`

## 1. Purpose

This directory is the durable current entry point for the DANTE database.

A developer must be able to determine from this repository, without chat history:

```text
what database objects exist now
why they exist
what persisted fields mean
how identity/references/current/history are represented
what PostgreSQL integrity and ACL are enforced
how retirement/redaction and recovery reconciliation work
what migration/mapping/tests implement and prove the contract
```

Git/Alembic preserve chronology. Current database docs describe the accepted current contract, not obsolete implementation checkpoints.

## 2. Current materialized database

```text
PostgreSQL           18.6
Alembic              20260830_09
schema               dante

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

Required extensions:

```text
postgis             3.6.4
vector              0.8.6
pg_trgm             1.6
unaccent            1.1
pg_stat_statements  1.12
```

The pre-recovery protected-main CP6 baseline remains historical evidence:

```text
20260826_08 / 68|5|14|75|95|68|120|0|0|0
```

The Recovery workstream adds the bounded forward evolution:

```text
20260830_09 / 69|5|15|76|97|69|123|0|0|0
```

Integration status is determined by live Git refs.

## 3. Recovery/lifecycle addition

`20260830_09` materializes the WL-H10 / SC-011 retirement and anti-resurrection contract.

Canonical PostgreSQL adds:

```text
dante.material_state_retirement
```

Supported materialized facets:

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
retirement reason/time/suppression identity remain explicit
protected payload must be absent
payload reinsertion is rejected by database-local integrity
```

This is not a universal soft-delete model and does not introduce a generic Entity/Thing root.

## 4. Recovery suppression ledger boundary

The external suppression ledger is **technical disaster-recovery evidence only**. PostgreSQL remains the sole canonical DANTE persistence surface.

Protocol v1:

```text
PREPARED durable suppression intent
→ canonical PostgreSQL retirement/redaction transaction
→ canonical DB read-back verification
→ COMMITTED marker bound to PREPARED SHA-256
```

Recovery blocks on ambiguity/tamper, including:

```text
missing/unavailable records directory
unexpected entry
duplicate MaterialStateRef target
PREPARED without COMMITTED
COMMITTED without PREPARED
identity/target mismatch
hash mismatch
invalid/non-canonical record
```

The ledger must survive the relevant database-loss boundary independently from PGDATA and from the pgBackRest database-backup repository. Its retention must cover the complete resurrection horizon of retained database/WAL/object versions.

## 5. Authority model

```text
closed Domain / Logical / Physical
→ semantic + architectural authority

PostgreSQL Persistence Constitution + ADR-010
→ reusable PostgreSQL doctrine

Alembic
→ deployed schema evolution authority

SQLAlchemy MetaData / mappings
→ application representation of deployed schema

real PostgreSQL introspection
→ observed materialized schema

Database Architecture & Reference
→ human-readable current database meaning

Database Dictionary
→ machine-readable current object contract

direct tests / recovery harnesses
→ executable proof
```

Permanent reconciliation invariant:

```text
DATABASE ARCHITECTURE & REFERENCE
≈ DATABASE DICTIONARY
≈ SQLALCHEMY METADATA / MAPPINGS
≈ ALEMBIC HEAD
≈ REAL POSTGRESQL SCHEMA
```

A mismatch is a defect.

## 6. Security baseline

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

## 7. Non-collapse obligations

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

## 8. Same-change rule

A structural database change is incomplete unless the same reviewed change updates, as applicable:

```text
Alembic migration
SQLAlchemy metadata/mappings
Database Dictionary
human-readable current database reference
generated artifacts/diagrams where governed
direct tests
recovery/operational harnesses affected by head/topology
current workstream/project documentation
```

Applied migrations are immutable. Current docs must not intentionally retain a superseded head/topology/status as if it were present truth.

## 9. Current QA contract

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
ambiguous/tampered suppression records
recovery target still in recovery when presented as accepted
structurally bootable but semantically unacceptable restore
```

`pg_isready` alone is never a traffic-reopen proof. Recovery acceptance requires `pg_is_in_recovery() = false`, current structural/security/semantic verification and completed suppression reconciliation.

## 10. Current recovery proof

Direct LOCAL proof includes:

```text
pgBackRest foundation                         PASS
continuous WAL + FULL backup                  PASS
destructive isolated restore                  PASS
deterministic named-target PITR               PASS
negative failure matrix N1–N7                 PASS
SC-011 definitive anti-resurrection           PASS
whole CP07 operator recovery rehearsal        PASS
database-local reopen                         PASS
whole backend suite at CP07 implementation    PASS
fresh-clone bootstrap                         PASS
bootstrap idempotence                         PASS
branch-agnostic runner                        PASS
exact pushed implementation HEAD CP07         PASS
remote backup provider                        TBD / NOT ACTIVATED
production/cloud recovery                     NOT CLAIMED
```

Permanent operator entry points:

```text
infra/local/postgres/recovery/bootstrap-local-recovery.sh
infra/local/postgres/recovery/cp07-whole-recovery-rehearsal.sh
docs/operations/postgres-recovery-runbook.md
```

### Reproducible LOCAL exact-head proof

Implementation/runtime proof HEAD:

```text
789e946a8f096b52f2a440b967120cc3e0a340a3
```

Proof summary:

```text
validation clone without recovery secrets                PASS
first bootstrap created exactly three LOCAL secrets      PASS
second bootstrap preserved secret contents               PASS
secret mode 0600 / ignored / untracked                   PASS
repository Compose validation                            PASS
repository-built pinned recovery image                   PASS
branch-name independence                                 PASS
clean attached branch + configured upstream gate         PASS
whole backend QA                                          PASS
pre-push whole CP07 rehearsal                            PASS
exact pushed implementation HEAD whole CP07              PASS
database-local reopen                                    PASS
deterministic PITR A-present / B-absent                  PASS
old protected X physical resurrection                    PROVEN
ledger reconciliation                                    PASS
payload reinsertion after retirement                     REJECTED
normal LOCAL / retained recovery / CP05 non-interference PASS
disposable cleanup                                       PASS
```

Exact pushed-run LOCAL observations:

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

## 11. Directory / maintenance map

```text
current database meaning
→ docs/database/README.md
→ docs/database/dante-postgresql-database.md + current continuation parts

machine-readable database contract
→ docs/database/dictionary/

forward schema evolution
→ apps/backend/alembic/versions/

SQLAlchemy deployed-schema representation
→ apps/backend/src/dante/platform/database/mappings/
→ apps/backend/src/dante/platform/database/metadata.py

database / recovery acceptance tests
→ apps/backend/tests/

suppression-ledger implementation
→ apps/backend/src/dante/platform/recovery/suppression_ledger.py
→ infra/local/postgres/recovery/recovery-suppression-record-v1.schema.json

PostgreSQL / pgBackRest image/config
→ infra/local/postgres/

Compose topology / LOCAL secrets boundary
→ infra/compose/

recovery bootstrap + executable rehearsals
→ infra/local/postgres/recovery/

operator procedure
→ docs/operations/postgres-recovery-runbook.md

closed Recovery branch history
→ docs/archive/branches/2026-08-feature-postgres-recovery.md (NON-AUTHORITATIVE)
```

## 12. Acceptance bar

The database System of Record succeeds when a new engineer can use the repository alone to understand current architecture, locate every real persisted object, trace objects to migration/mapping/tests, understand integrity/ACL/current/history/lifecycle semantics, understand anti-resurrection behavior, distinguish canonical from provider/derived/recovery state and execute the current database/recovery acceptance procedures.
