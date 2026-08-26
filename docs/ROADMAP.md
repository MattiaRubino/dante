> **CURRENT MAIN + CP6 RECONCILIATION — 2026-08-26**
> Protected `main` anchor imported by this alignment is `87fe668c2ade78b17e0326d635e4d7a67920ae8a`. Its post-merge truth is preserved: frontend materialization/integration is **CLOSED / INTEGRATED via PR #28**, deterministic Frontend CI compatibility repair is integrated via PR #37, and the clean Home B2 v27 React handoff is integrated via PR #36. The main-only frontend contracts, fixtures, tokens and pre-production guard remain byte-identical to that protected-main anchor.
> Backend CP6 is independently **CLOSED / CONCRETE POSTGRESQL DATABASE PASS**. Accepted implementation HEAD is `22bbc078391d52c43665474bf465593d6225106e`; closure-documentation branch anchor before this alignment is `8c33c897ff57cfff9130fe00db1854470aa06bb5`; persistent LOCAL PostgreSQL 18.6 is at Alembic `20260826_08`; verified topology remains `68 tables / 5 views / 14 routines / 75 triggers / 95 indexes / 68 FKs / 120 CHECKs`.
> This overlay supersedes only contradictory **current status, routing, branch and next-step prose** later in this file. Historical evidence, accepted architecture, frontend product contracts, failed-run/repair evidence and phase-time records remain historical truth and are not rewritten. The aligned feature branch is only a candidate for protected-main integration: **no final merge into `main` is authorized by this overlay**. Protected-main integration still requires the normal PR, current-head required checks and a separate final merge gate.

> **CURRENT INTEGRATION RECONCILIATION — 2026-08-24**  
> PR #28 is merged into protected `main` at `f1aacb0724088e0b4b086008a5219c2fba5ce0cf`; frontend materialization is **CLOSED / PASS / INTEGRATED**. Any later roadmap text that still labels frontend materialization active or PR #28 pending is preserved pre-merge status and is superseded by this banner. Backend `feature/logical-postgresql` is current with `main`; CP6-03 remains ACTIVE with Checkpoint J / DB-U23 CLOSED, `DB-U08 / DB-U15 / DB-U21` OPEN, exact next action = **FINAL ACTUAL POSTGRESQL OBJECT INVENTORY**, second full tombstone mandatory before Gate 03, CP6-04 not authorized.  

# DANTE Roadmap

- Status: **CURRENT**
- Current backend workstream: `feature/logical-postgresql` — **CP6 Concrete PostgreSQL Database ACTIVE**

## Completed architecture / design sequence

```text
Product / North Star
        CURRENT
          ↓
Domain Model
        CLOSED
          ↓
Logical Model
        CLOSED / 57 OF 57 / WL-H01..WL-H12
          ↓
Pre-Physical Repository & Architecture Coherence
        CLOSED
          ↓
Physical Model / Target Selection
        CLOSED / SELECTED / ACCEPTED
        PostgreSQL 18 major family canonical
        exact Physical phase-time patch 18.4
          ↓
Engineering Foundation v0
        CLOSED / ACCEPTED
          ↓
Frontend Engineering Foundation
        CLOSED / ACCEPTED / FINAL REVIEW PASS
        INTEGRATED VIA PR #22
          ↓
Backend CP1–CP5 Scaffold
        CLOSED / DIRECT QA PASS
        INTEGRATED VIA PR #24
```

Architecture closure remains distinct from implementation/direct validation. PostgreSQL patch maintenance within accepted major line 18 does not reopen the Physical selection.

## Backend CP6 — Concrete PostgreSQL Database — ACTIVE

Branch:

`feature/logical-postgresql`

CP6 consumes the closed Domain + Logical + Physical model and turns it into the **concrete DANTE PostgreSQL database**.

It is not a new semantic modeling cycle and it is not the first product vertical.

### Closed CP6 checkpoints

```text
CP6-00
Authority Reconstruction & Scope Freeze
COMPLETE
        ↓
CP6-01
Concrete Persistence Coverage Map
CLOSED / GATE 01 PASS
        ↓
CP6-02
PostgreSQL Persistence Constitution
CLOSED / GATE 02 PASS
PostgreSQL 18.6 technical refresh DIRECT REMOTE QA PASS
```

CP6-01 closure authority:

`docs/development/backend-cp6-01-concrete-persistence-coverage-closure.md`

CP6-02 Constitution:

`docs/development/backend-cp6-02-postgresql-persistence-constitution.md`

CP6-02 closure authority:

`docs/development/backend-cp6-02-postgresql-persistence-constitution-closure.md`

Current execution-boundary authority:

`docs/workstreams/logical-postgresql.md`

## Remaining CP6 sequence — authoritative

The remaining work is deliberately simplified into three concrete stages:

```text
CP6-03
WHOLE DANTE DATABASE BLUEPRINT
        ↓
CP6-04
WHOLE DANTE DATABASE MATERIALIZATION
        ↓
CP6-05
WHOLE DATABASE DIRECT QA + CP6 CLOSURE
        ↓
CP6 CLOSED
        ↓
FIRST PRODUCT VERTICAL — SEPARATE PHASE
```

Earlier planning that treated CP6-04 as Vertical #1 Selection, CP6-05 as Vertical #1 Exact Persistence Design, and CP6-06/07 as extra pre-vertical documentation/QA stages is superseded by this roadmap.

Their useful requirements are absorbed into CP6-03..05; no closed technical decision is discarded.

## CP6-03 — Whole DANTE Database Blueprint — ACTIVE

Current exact state:

```text
CHECKPOINT J / DB-U23
CLOSED

57 / 57 FINAL MATERIALIZATION DISPOSITION
PASS AFTER HARDENING

GLOBAL DB-U OPEN
DB-U08  final PostgreSQL object naming
DB-U15  final structural/query index matrix
DB-U21  exact object-level PostgreSQL privilege matrix

NEXT DESIGN BLOCK
FINAL ACTUAL POSTGRESQL OBJECT INVENTORY

SECOND FULL TOMBSTONE AUDIT FROM ZERO
MANDATORY BEFORE GATE 03

GATE 03
NOT YET EARNED
```

Purpose: derive the complete relational database that follows from the already-closed model.

Required coverage, where applicable across 57/57:

```text
concrete relational families
concrete tables
columns + exact semantics
PostgreSQL types
PK
stable identity
FK / target-family rules
UNIQUE
CHECK
NULL / missingness semantics
range / temporal / EXCLUDE constraints
NativeRef / ScopedRecordRef / MaterialStateRef topology
current-state bindings
owner-specific material-state/history topology
correction / replacement / reconciliation lineage
specific relation topology
provenance/governance structures
provider/integration structures
derived/query structures already required by the model
retention/tombstone/redaction rules
structural indexes + justification
ownership/privilege posture
SQLAlchemy mapping plan
real PostgreSQL direct-test plan
implementation/migration dependency DAG
```

The active Database Architecture & Reference is one canonical multi-part authority across `docs/database/dante-postgresql-database.md` and Parts 2–8. Checkpoint J repaired the first total pre-freeze audit's residual 57-concept materialization-disposition gap; it did **not** freeze the final actual PostgreSQL object inventory.

The exact remaining CP6-03 order is:

```text
Final Actual PostgreSQL Object Inventory
→ DB-U08 exact names
→ DB-U15 exact structural/query index matrix
→ DB-U21 exact object-level privilege matrix
→ migration/materialization DAG
→ SQLAlchemy mapping plan
→ Database Dictionary readiness
→ direct PostgreSQL proof/test plan
→ SECOND FULL TOMBSTONE AUDIT FROM ZERO
→ Gate 03
```

CP6-03 must not defer an already-determinable database structure by merely calling it “vertical-specific”.

It also must not invent product semantics that were never closed upstream.

Gate 03 requires a blueprint complete enough that CP6-04 can implement the DANTE database without inventing global persistence architecture on the fly.

## CP6-04 — Whole DANTE Database Materialization

After Gate 03 **and a separate explicit user-approved materialization gate**, CP6 materially implements the approved blueprint.

Authorized under exact write gates:

```text
Alembic business-schema revisions
DANTE business tables
bounded address/control structures
owner-specific canonical tables
owner-specific material-state/history tables
specific relation tables
provider/integration DB structures already determined
bounded derived/query DB structures already determined
PostgreSQL constraints
PostgreSQL indexes
SQLAlchemy business/database mappings
mapping-specific persistence types/codecs where justified
owner/migrator/runtime object privileges
real PostgreSQL acceptance tests
```

Implementation proceeds in bounded migration/materialization batches following the dependency DAG rather than one giant speculative migration.

CP6-04 does not implement:

```text
first-product-vertical application use cases
application services
product persistence adapters that encode application behavior
business API routes
frontend behavior
product workflow orchestration
```

## CP6-05 — Whole Database Direct QA + CP6 Closure

CP6-05 proves the materialized database against the closed model and blueprint.

Direct PostgreSQL proof includes, where applicable:

```text
fresh DB → Alembic head
single canonical head
schema drift / metadata alignment
runtime/migrator/owner privilege matrix
positive + negative constraint proof
wrong-family / dangling-reference rejection
MaterialStateRef owner/facet/current-binding integrity
history/correction reconstruction
transaction rollback / atomicity
expected-state / concurrency behavior where a real DB subject exists
migration upgrade path where a prior supported business schema exists
selected PostgreSQL capability proof where the concrete DB activates it
```

Evidence that intrinsically requires a later product vertical, real destructive restore, real V1→V2 lifecycle or dormant specialist activation remains truthfully staged rather than artificially passed.

CP6 closes only when:

```text
DANTE DATABASE
BLUEPRINT COMPLETE
MATERIALIZED TO MAXIMUM NON-SPECULATIVE EXTENT
MIGRATED
MAPPED
DIRECTLY TESTED
QA CLEAN
```

## Post-CP6 — First product vertical

The first product vertical begins **after CP6 closes**.

It consumes the database already derived/materialized from Domain + Logical + Physical.

Its purpose is application behavior, not to invent its persistence model from scratch:

```text
application use cases
capability-specific persistence adapters
commands/queries
governance orchestration
API boundary
frontend/mobile consumption
end-to-end semantic scenarios
vertical-specific HG/PSV evidence
```

A later vertical may still expose a real missing/evolving DB requirement; that becomes normal reviewed schema evolution, not the default reason to postpone determinable schema from CP6.

## Current PostgreSQL technical evidence

```text
PostgreSQL architecture              major 18
Physical/CP2/CP3 exact evidence      18.4 / historical
current technical patch              18.6
configuration refresh                APPLIED
Backend CI run                       32568664940
executed HEAD                        ec3dc795b5e044daa3a77723c94a1b4b5b92865c
Backend Quality                      SUCCESS / 32 fast tests PASS
Backend PostgreSQL                   SUCCESS / 18 PostgreSQL tests PASS
Backend CI Gate                      SUCCESS
18.6 release-note impact             PASS / NO CURRENT POST-UPGRADE ACTION
```

The 18.6 run is technical-foundation evidence; it does not pre-prove the not-yet-materialized DANTE business database.

## Capability-triggered implementation

Selected specialist components activate only at real triggers:

```text
PowerSync + encrypted SQLite
→ real offline/multi-device implementation

PostgreSQL transactional outbox
→ real Class-A async requirement

R2
→ real ContentArtifact byte flow

OR-Tools
→ solver-backed capability

Restate
→ first real Class-B durable workflow

pgBackRest + AWS S3
→ recovery/production boundary or real recovery rehearsal
```

A PostgreSQL-native structure required by the concrete DANTE database may be materialized in CP6 without automatically activating the surrounding product/runtime capability.

## Frontend production materialization — ACTIVE

Branch:

`feature/frontend-materialization`

Frontend production materialization remains independent. Direct frontend PASS is earned only by that workstream's executed validations.

## Persistent rules

```text
SELECTED ARCHITECTURE != IMPLEMENTED COMPONENT
DOCUMENTATION PASS != DIRECT IMPLEMENTATION PASS
CP3 TECHNICAL QA != BUSINESS-SEMANTIC HG PASS
POSTGRESQL PATCH REFRESH != PHYSICAL ARCHITECTURE REOPEN
HISTORICAL 18.4 EVIDENCE != CURRENT 18.6 RUNTIME CLAIM
CLIENT LOCAL STATE != CANONICAL EFFECT AUTHORITY
ENVIRONMENT != GIT BRANCH
CLOSED FEATURE BRANCH != INTEGRATED MAIN UNTIL VERIFIED MERGE
DETERMINABLE DATABASE STRUCTURE != VERTICAL-SPECIFIC DEFERRAL
DATABASE MATERIALIZATION != FIRST PRODUCT VERTICAL APPLICATION IMPLEMENTATION
```

## Immediate next action

```text
CP6-03 — FINAL ACTUAL POSTGRESQL OBJECT INVENTORY

consume Database Reference Parts 1–8 together
→ enumerate every surviving actual PostgreSQL object
→ exclude all explicitly superseded/no-DDL candidates
→ reconcile scoped-family + MaterialState-facet survivors
→ prove each table/column/key/constraint is non-speculative
→ keep DB-U08 / DB-U15 / DB-U21 open during derivation
→ cumulative whole-database audit
→ exact write gate before inventory freeze
```
