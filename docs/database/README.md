# DANTE Database System of Record

- **Status:** CURRENT / MATERIALIZED / CP6 CLOSED / INTEGRATED IN `main`
- **Scope:** DANTE PostgreSQL architecture, Dictionary, mappings, migrations, generated reference, direct proof and documentation consistency
- **PostgreSQL:** 18.6
- **Alembic head:** `20260826_08`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Architecture decision:** `../decisions/ADR-010-postgresql-persistence-constitution.md`
- **Final CP6 acceptance:** `../development/backend-cp6-05-whole-database-qa.md`

## 1. Purpose

This directory is the durable entry point for understanding the DANTE database itself.

A developer should be able to start here and answer, without reconstructing chat history:

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

This database documentation does not replace Domain, Logical, Physical or the PostgreSQL Persistence Constitution. Those remain semantic/design/rationale authorities. This system of record is the **current operational and structural reference for the database produced from them**.

## 2. Current materialized baseline

The accepted CP6 database is materialized and directly verified.

```text
tables               68
views                 5
routines             14
triggers              75
physical indexes     95
foreign keys          68
CHECK constraints    120

custom enum/domain     0
sequences              0
materialized views     0
RLS policies           0
```

The current machine-readable Dictionary contains:

```text
68 table entries
5 view entries
14 routine entries
87 standalone entries total
```

`docs/database/dictionary/scope.json` records `status = materialized` and CP6-M01..M07 as complete.

## 3. Database documentation model

DANTE uses a repository-native database documentation system:

```text
human-readable architecture/reference
+
machine-readable Database Dictionary
+
generated structural reference where reliable
+
derived diagrams where useful
+
Alembic migration history
+
SQLAlchemy metadata/mappings
+
real PostgreSQL introspection
+
direct database tests
```

No external enterprise catalog product is required merely to imitate organizational scale. Future tooling may consume the structured Dictionary without redefining database meaning.

## 4. Current directory roles

```text
docs/database/
├── README.md
├── dante-postgresql-database.md
├── dante-postgresql-database-part-2.md
├── ...
├── dante-postgresql-database-part-19.md
├── dictionary/
│   ├── README.md
│   ├── scope.json
│   ├── schema/
│   ├── tables/
│   ├── views/
│   └── routines/
├── generated/    when generated current artifacts exist
├── diagrams/     when useful/current diagrams exist
└── evolution/    only for complex evolutions requiring durable rollout rationale
```

Empty ceremonial directories are forbidden.

### Human-readable Database Architecture & Reference

The current human-readable reference is still physically represented by `dante-postgresql-database.md` plus Parts 2–19. Those files were accumulated during CP6 and together contain the accepted detailed derivation, object model and repair history.

They are **one logical reference**, not 19 independent authorities. Until a dedicated lossless compaction/reorganization is completed, readers and tooling that depend on detailed blueprint provenance must treat the complete set as the source payload.

The documentation-cleanup workstream may later recompose this frozen reference into fewer/topic-based read-only files, but only under the repository's lossless knowledge-coverage policy. No accepted requirement, invariant, rationale or important evidence may disappear merely to reduce file count.

### `dictionary/`

Machine-readable current object metadata. Every materialized DANTE table, view and routine has a structured entry; table-owned subobjects such as FK/CHECK/index/trigger metadata are embedded under their owning entries.

### `generated/`

Artifacts derived from SQLAlchemy metadata and/or real PostgreSQL introspection where automation is reliable. Generated output is never edited as an alternate manual authority.

### `diagrams/`

ER/topology diagrams should be generated or mechanically derived where practical. A manually maintained diagram must not become an independent source of schema truth.

### `evolution/`

Used only for migrations/evolutions complex enough to need durable rollout/backfill/cutover/recovery explanation beyond executable Alembic revisions and tests.

## 5. Authority model

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
→ human-readable database meaning and design traceability

Database Dictionary
→ structured current object metadata

generated reference / diagrams
→ derived structural views

direct tests
→ executable proof of required invariants
```

A mismatch is a defect to investigate, not permission to choose whichever representation is convenient.

## 6. Permanent consistency invariant

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
real table exists but Dictionary entry is missing
mapped column is absent from Alembic-produced schema
FK documented but PostgreSQL does not enforce it
constraint exists in PostgreSQL but its semantic reason is undocumented
manual diagram disagrees with current schema
migration changes a table but current reference still describes the old shape
current reference calls provider/derived state canonical
```

## 7. Database Dictionary contract

The materialized Dictionary v1 must account for these classes of information where applicable.

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
- EXCLUDE/range constraints where used
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
- relevant obligations
- staged evidence only when it cannot yet be executed truthfully
```

An inapplicable category may be explicitly marked as not applicable by the Dictionary schema. Required facts must not disappear through omission.

See `dictionary/README.md` for the current materialized Dictionary contract.

## 8. Human-readable reference obligations

The long-lived reference must support both top-down and object-level reading, including:

```text
database purpose and authority
schema/object organization
identity topology
reference topology
canonical/current/material-history topology
relation topology
temporal representation
governance/provenance topology
provider/integration separation
derived/query/search separation
account/security persistence boundary
retention/redaction/tombstone model
privileges/ownership
dependency/materialization topology
table/family catalog
constraint/reference integrity catalog
index strategy/catalog
migration/evolution traceability
SQLAlchemy traceability
direct-test/evidence traceability
explicitly deferred/non-materialized constructs
```

For a concrete object, an engineer must be able to find its purpose, semantic origin, columns, types, keys, relationships, constraints, history/lifecycle behavior, indexes, migration, mapping and tests without database archaeology.

## 9. DANTE-specific non-collapse obligations

Database documentation must keep these technical-vs-semantic boundaries explicit:

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

## 10. Same-change documentation rule

A structural database change is incomplete unless the same reviewed change updates all affected current representations.

As applicable, a database change includes together:

```text
Alembic migration
SQLAlchemy metadata/mapping
Database Dictionary entry/update
human-readable database reference when meaning/topology changes
generated reference/diagram regeneration
direct tests
workstream/status documentation when milestone state changes
```

A new table introduced without its Dictionary entry is incomplete.

A structural table change without corresponding Dictionary/reference reconciliation is incomplete.

Documentation may be generated for facts that can be derived reliably, but semantic purpose, invariants and rationale must not be replaced by generated DDL output.

## 11. Generated-artifact rule

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

Prefer human-authored current reference/Dictionary fields for facts the schema cannot explain by itself:

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

## 12. Automated QA contract

Current and future QA must detect conditions such as:

```text
undocumented real table/view/routine
stale Dictionary object
column/type/nullability/default drift
PK/FK/UQ/CHECK/index drift
trigger/routine/view drift
SQLAlchemy-vs-Alembic schema drift
missing Dictionary entry for a real object
invalid generated reference
diagram generation failure where diagrams are governed
migration head mismatch
owner/ACL drift
extension-owned false positives
```

Semantic descriptions cannot be fully generated and remain subject to review.

CP6-05 proved the baseline by reconciling Dictionary ↔ SQLAlchemy ↔ Alembic ↔ live PostgreSQL plus final topology/security and direct concurrency/integrity evidence.

## 13. Current security baseline

The materialized baseline preserves explicit owner/migrator/runtime separation:

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
```

Current proof includes exact DANTE role-membership topology, owner no-password posture, bounded runtime grants, denied runtime access to `dante.alembic_version`, hardened routine search paths and direct negative security evidence.

Security documentation must describe actual grants and invariants rather than broad `read/write` labels.

## 14. CP6 historical lifecycle

CP6 is closed. Its phases are historical evidence, not current next steps:

```text
CP6-01  concrete persistence coverage          CLOSED / GATE 01 PASS
CP6-02  PostgreSQL Persistence Constitution    CLOSED / GATE 02 PASS
CP6-03  whole database blueprint               CLOSED / GATE 03 PASS
CP6-04  materialization                        CLOSED / MATERIALIZATION PASS
CP6-05  whole-database direct QA               CLOSED / DIRECT QA PASS
```

The branch-level history is retained under:

`../archive/branches/2026-08-feature-logical-postgresql.md`

Detailed final acceptance remains in:

`../development/backend-cp6-05-whole-database-qa.md`

CP6 design-stage statements such as `Gate 03 not earned`, `CP6-04 not started`, `Dictionary entries not yet materialized` or `protected-main alignment next` are historical and must not be used as current routing.

## 15. Future database evolution rule

After CP6, the same discipline remains permanent.

Every later product vertical or schema evolution treats database documentation as part of the database change itself.

For ordinary changes, Git/Alembic history is the chronology; current reference documentation remains current rather than accumulating obsolete implementation stories.

For complex migrations, preserve necessary rollout/backfill/verification/recovery rationale under an appropriate durable evolution/ADR/evidence source.

Applied Alembic revisions remain immutable; later corrections use new forward revisions.

## 16. Documentation lifecycle

Frozen/read-only multi-part references may be compacted when this genuinely improves maintainability, but only through the lossless knowledge-coverage rules in:

`../development/documentation-lifecycle-policy.md`

Compaction must preserve still-valid substantive information, accepted decisions, invariants, requirements, continuing rationale and important evidence. Obsolete status wrappers, duplicate routing and superseded operational chronology may be removed once coverage is proven.

## 17. Acceptance bar

The DANTE Database System of Record is successful when a new engineer can begin here and, without conversation memory:

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
