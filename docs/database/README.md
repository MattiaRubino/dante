# DANTE Database System of Record

- **Status:** CURRENT / DATABASE DOCUMENTATION AUTHORITY
- **Created:** 2026-08-22
- **Scope:** DANTE PostgreSQL database architecture, dictionary, generated reference, evolution and schema-documentation consistency
- **Current workstream:** `../workstreams/logical-postgresql.md`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Architecture decision:** `../decisions/ADR-010-postgresql-persistence-constitution.md`

## 1. Purpose

This directory is the durable entry point for understanding the DANTE database itself.

A developer must be able to start here and answer, without reconstructing old chat history or reading every Domain/Logical/Physical checkpoint:

```text
what database objects exist?
why does each object exist?
what does every persisted field mean?
how are objects related?
what integrity does PostgreSQL enforce?
how are identity, references, current state and history represented?
what is canonical vs provider/derived/technical state?
what migration created or changed an object?
what SQLAlchemy mapping represents it?
what tests prove its invariants?
what remains intentionally unmaterialized and why?
```

This database documentation does not replace Domain, Logical, Physical or the PostgreSQL Persistence Constitution. Those documents remain the design/rationale authorities. This system of record is the **current operational and structural reference for the database produced from them**.

## 2. Design principle

DANTE adopts a repository-native database documentation model informed by mature large-system practice:

```text
human-readable architecture/reference
+
machine-readable database dictionary
+
generated structural reference
+
derived diagrams
+
Alembic migration history
+
SQLAlchemy metadata/mappings
+
real PostgreSQL introspection
+
direct database tests
```

No external enterprise catalog product is required merely to imitate organizational scale. The repository remains the source-controlled knowledge surface; future tooling may consume the structured dictionary without changing its meaning.

## 3. One logical authority, multiple representations

The database system of record is one logical documentation authority even when physically split across files.

Expected shape as real content materializes:

```text
docs/database/
├── README.md
├── dante-postgresql-database.md
├── dictionary/
│   ├── tables/
│   ├── views/
│   └── other-object-types only when real objects exist
├── generated/
├── diagrams/
└── evolution/ only when a complex evolution needs durable explanatory material
```

Empty ceremonial directories are forbidden. A path is created only when real content exists.

### `dante-postgresql-database.md`

Human-readable architecture and reference. It explains the database from global topology down to concrete families/objects and is intended for engineers who need to understand the system rather than reverse-engineer DDL.

### `dictionary/`

Machine-readable object metadata. Every materialized DANTE table and every separately governed persisted view/object that requires durable understanding receives a structured dictionary entry.

### `generated/`

Artifacts derived from SQLAlchemy metadata and/or real PostgreSQL introspection where automation is reliable. Generated output is never edited as an alternate manual authority.

### `diagrams/`

ER/topology diagrams should be generated or mechanically derived where practical. A manually maintained diagram must not become an independent source of schema truth.

### `evolution/`

Used only for migrations/evolutions complex enough to need durable rollout/backfill/cutover/recovery explanation beyond the executable Alembic revision and tests.

## 4. Authority model

The representations have different jobs and must not silently diverge:

```text
closed Domain / Logical / Physical
→ semantic and architectural source

CP6-02 Constitution + ADR-010
→ reusable PostgreSQL doctrine

Alembic
→ deployed application-schema evolution authority

SQLAlchemy MetaData / mappings
→ application mapping of the deployed database contract

real PostgreSQL introspection
→ observed materialized schema

Database Architecture & Reference
→ human-readable current database meaning

Database Dictionary
→ structured current object metadata

generated reference / diagrams
→ derived structural views

direct tests
→ executable proof of required invariants
```

A mismatch is a defect to investigate, not permission to choose whichever representation is convenient.

## 5. Consistency invariant

At CP6 closure and after every later structural database change, the following must describe the same accepted database contract:

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

`≈` means semantically and structurally consistent for the facts each representation owns; it does not mean identical serialization.

Examples of defects:

```text
real table exists but dictionary entry is missing
mapped column is absent from Alembic-produced schema
FK documented but PostgreSQL does not enforce it
constraint exists in PostgreSQL but its semantic reason is undocumented
manual diagram disagrees with current schema
migration changes a table but current reference still describes the old shape
current reference calls provider/derived state canonical
```

## 6. Database Dictionary contract

CP6-03 will finalize the machine-readable format together with the real blueprint rather than inventing metadata fields detached from actual schema needs.

Every table entry must nevertheless be able to account for the following classes of information when applicable:

```text
identity
- schema name
- object name
- object type
- persistence role
- short purpose

semantic traceability
- Domain / Logical source where applicable
- representation family / cross-cutting construct
- canonical vs contextual vs relation vs state/history vs provider/derived/technical role

implementation traceability
- introducing migration
- later structural migrations where material
- SQLAlchemy mapping
- owning backend boundary/module once one exists

columns
- column name
- PostgreSQL type
- nullability
- default/generation rule
- exact persisted meaning
- accepted value/range semantics where applicable

keys and relationships
- primary key
- stable-address contract where applicable
- foreign keys
- target family
- cardinality
- delete/update behavior
- semantic reason for the relationship

integrity
- UNIQUE
- CHECK
- EXCLUDE/range constraints
- trigger/function-backed integrity only where declarative enforcement is insufficient
- cross-row/reference-family invariants

indexes
- columns/expressions
- method
- uniqueness where applicable
- structural/query reason
- no speculative index merely for completeness

state/history
- MaterialStateRef behavior
- current-state binding
- chronology semantics
- correction/replacement/reconciliation lineage
- immutability policy where applicable

lifecycle
- retention
- redaction
- tombstone/retirement continuity
- deletion behavior

security
- owner/migrator/runtime privilege posture
- sensitive handling only where an accepted classification exists

proof
- direct tests
- relevant HG / SC / PSV / PG-R obligations
- known staged evidence that cannot yet be truthfully executed
```

An inapplicable category may be explicitly marked as not applicable by the eventual dictionary schema. Required facts must not disappear through omission.

## 7. Human-readable Database Architecture & Reference

The long-lived reference must support both top-down and object-level reading.

Minimum global structure:

```text
1. database purpose and authority
2. schema/object organization
3. identity topology
4. reference topology
5. canonical/current/material-history topology
6. relation topology
7. temporal representation
8. governance/provenance topology
9. provider/integration separation
10. derived/query/search separation
11. account/security persistence boundary
12. retention/redaction/tombstone model
13. privileges/ownership
14. dependency/materialization topology
15. table/family catalog
16. constraint/reference integrity catalog
17. index strategy/catalog
18. migration/evolution traceability
19. SQLAlchemy traceability
20. direct-test/evidence traceability
21. explicitly deferred/non-materialized constructs
```

For a concrete object, a future engineer should be able to find its purpose, semantic origin, columns, types, keys, relationships, constraints, history/lifecycle behavior, indexes, migration, mapping and tests from this documentation system without database archaeology.

## 8. DANTE-specific non-collapse obligations

The database documentation must make important technical-vs-semantic boundaries obvious, especially:

```text
technical address anchor != semantic Entity/Thing
technical material-state control != universal Fact/Version owner
NativeRef != ScopedRecordRef != MaterialStateRef != ExternalRef
current accepted state != newest inserted row
material history != universal event sourcing
provider state != canonical DANTE state
derived/search state != canonical DANTE truth
Person != Account != Principal != Actor
Authority != AuthZ decision
absence / unknown != explicit negative
idempotency != semantic identity
```

A schema reader should not have to infer these distinctions from naming alone.

## 9. Same-change documentation rule

A structural database change is incomplete unless the same reviewed change updates all affected current representations.

As applicable, a database change includes together:

```text
Alembic migration
SQLAlchemy metadata/mapping
database dictionary entry/update
human-readable database reference when meaning/topology changes
generated reference/diagram regeneration
direct tests
workstream/status documentation when milestone state changes
```

A new table introduced without its dictionary entry is incomplete.

A structural table change without corresponding dictionary/reference reconciliation is incomplete.

Documentation may be generated for facts that can be derived reliably, but semantic purpose, invariants and rationale must not be replaced by generated DDL output.

## 10. Generated-artifact rule

Prefer generation for facts PostgreSQL/SQLAlchemy can state exactly:

```text
object inventory
columns/types/nullability
PK/FK/UNIQUE/CHECK metadata where introspectable
indexes
basic dependency graph
ER relationships
migration head/current revision
```

Prefer human-authored current reference/dictionary fields for facts the schema cannot explain by itself:

```text
why an object exists
what semantic concept/facet it represents
why a reference contract is bounded a certain way
why a constraint exists
what current/history distinction means
what is canonical vs provider/derived
what lifecycle behavior means
what must never be inferred from absence/order/UUID/etc.
```

Generation must reduce drift, not create another competing authority.

## 11. Automated QA target

CP6-03 designs the checks; CP6-04 materializes them where practical; CP6-05 requires the applicable checks to pass.

The target is automatic detection of conditions such as:

```text
undocumented real table/view
stale dictionary object
column/type/nullability drift
PK/FK/constraint/index drift
SQLAlchemy-vs-Alembic schema drift
missing dictionary entry for newly introduced table
invalid generated reference
diagram generation failure
migration head mismatch
```

Semantic descriptions cannot be fully generated and remain subject to review/clean-room QA.

## 12. CP6 responsibilities

### CP6-03 — Whole DANTE Database Blueprint

CP6-03 must create the first complete approved database specification and initialize this documentation system with the real structures selected by the blueprint.

It must not produce a second theory document disconnected from implementation. The blueprint and database reference must be detailed enough that CP6-04 can implement the schema without inventing global persistence decisions while coding.

### CP6-04 — Whole DANTE Database Materialization

As each approved batch becomes real, update the Database System of Record in the same change so the documented database tracks Alembic, SQLAlchemy and PostgreSQL throughout materialization rather than being repaired only at the end.

### CP6-05 — Whole Database Direct QA + Closure

CP6 cannot close until applicable consistency checks show that the current database documentation, dictionary, SQLAlchemy metadata, Alembic head and real PostgreSQL schema are aligned, with remaining non-executable evidence explicitly staged rather than falsely passed.

## 13. Future database evolution rule

After CP6, the same discipline remains permanent.

Every later product vertical or schema evolution must treat database documentation as part of the database change itself.

For ordinary changes, Git/Alembic history is the chronology; current reference documentation remains current rather than accumulating obsolete implementation stories.

For complex migrations, preserve the necessary rollout/backfill/verification/recovery rationale under the appropriate durable evolution/ADR/evidence source.

## 14. Tooling posture

Repository-native is the default.

Do not introduce DataHub, Collibra, Atlan or another catalog/governance platform merely to make the project look enterprise-grade.

A future catalog may be justified when team size, object count, lineage/discovery pressure, governance requirements or multiple data platforms create a real operational need. The machine-readable dictionary is intentionally designed so future tooling can consume it without redefining database meaning.

## 15. Acceptance bar

The DANTE Database System of Record is successful when a new engineer can begin here and, without relying on conversation memory:

```text
understand the database architecture
locate every real persisted object
understand why it exists
understand its columns and relationships
understand the integrity PostgreSQL enforces
trace it to migration + SQLAlchemy mapping
locate the tests that prove it
understand current/history/provider/derived boundaries
identify what is intentionally deferred and why
```

The goal is not documentation volume. The goal is a database that is understandable, inspectable, reviewable and maintainable at large-system engineering standards.