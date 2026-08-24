> **CURRENT CP6-03 RESUME — 2026-08-24 / SECOND TOMBSTONE REPAIR COMPLETE**  
> Canonical authority is now `docs/database/dante-postgresql-database.md` + Parts 2–17, plus the hardened Dictionary v1 foundation. **DB-U25 is CLOSED** after repairing all five real B findings from the first post-hardening second-audit pass: Recurrence selector/phase/range determinism, non-quota generated-coordinate duplication, five NULL-unsafe CHECK expressions, exact governing-Recurrence membership, and one-way current-history lifecycle/column-scoped INSERT. Frozen counts remain `68 tables / 5 views / 14 routines / 75 triggers / 95 indexes / 68 FKs / 120 CHECKs`; **GLOBAL DB-U OPEN = 0**.  
> The mandatory next operation is a **fresh SECOND FULL TOMBSTONE AUDIT FROM ZERO over the repaired Parts 1–17**. The pre-repair audit is not a PASS. Gate 03 is NOT yet earned; CP6-04 remains NOT STARTED / NOT AUTHORIZED; protected-`main` realignment remains deferred. This overlay supersedes only older CURRENT/resume prose below that stops at Part 16 or treats the prior audit pass as final; historical derivation/evidence remains preserved.  

> **CURRENT CP6-03 RESUME — 2026-08-24 / PRE-GATE03 HARDENING COMPLETE**  
> Canonical authority is now `docs/database/dante-postgresql-database.md` + Parts 2–16, plus the hardened Dictionary v1 foundation. **DB-U24 is CLOSED**, the **Direct PostgreSQL Proof / Test Plan is FROZEN**, and **GLOBAL DB-U OPEN = 0**. Frozen baseline remains `68 tables / 5 views / 14 routines / 75 triggers / 95 indexes / 68 FKs`, now with an exact **120-CHECK** manifest and fail-closed P0/M1 contract.  
> The exact next CP6-03 operation is the mandatory **SECOND FULL TOMBSTONE AUDIT FROM ZERO**. Gate 03 is NOT yet earned; CP6-04 remains NOT STARTED / NOT AUTHORIZED. Protected-`main` realignment remains deferred to its later separate gate. This overlay supersedes only older CURRENT/resume prose below that stops at Part 15 or says the proof plan is still pending; historical derivation/evidence remains preserved.  

> **CURRENT CP6-03 RESUME — 2026-08-24 / DATABASE DICTIONARY READY**  
> The authoritative current state is now: Final Object Inventory FROZEN + DB-U08 CLOSED + DB-U15 CLOSED + DB-U21 CLOSED + Migration DAG FROZEN + SQLAlchemy Mapping Plan FROZEN + **Database Dictionary Readiness READY/PASS**. Canonical authority is `docs/database/dante-postgresql-database.md` + Parts 2–15, plus the readiness foundation under `docs/database/dictionary/`. **GLOBAL DB-U OPEN = 0**. The exact next CP6-03 block is **DIRECT POSTGRESQL PROOF / TEST PLAN**.  
> Dictionary target is 87 standalone DANTE-owned entries (`68 table + 5 view + 14 routine`), with 75 triggers and 95 physical indexes embedded in owning table entries. Object-specific entries remain intentionally absent until CP6-04 creates the corresponding real objects. The second full tombstone audit has NOT yet run; Gate 03 is NOT earned; CP6-04 remains NOT STARTED / NOT AUTHORIZED.  
> Protected-`main` realignment remains intentionally deferred to a later separate gate. This overlay supersedes only older CURRENT/resume prose below that says Parts 1–14 or that Database Dictionary readiness is pending/next; historical derivation/evidence remains preserved.  

> **CURRENT CP6-03 RESUME — 2026-08-24 / SQLALCHEMY MAPPING PLAN FROZEN**  
> The authoritative current operational state is now: **Final Actual PostgreSQL Object Inventory FROZEN + DB-U08 CLOSED + DB-U15 CLOSED + DB-U21 CLOSED + Migration / Materialization DAG FROZEN + SQLAlchemy Mapping Plan FROZEN**. Canonical authority is `docs/database/dante-postgresql-database.md` + Parts 2–14. **GLOBAL DB-U OPEN = 0**. The exact next CP6-03 block is **DATABASE DICTIONARY READINESS**. The second full tombstone audit has NOT yet run, Gate 03 is NOT earned, and CP6-04 remains NOT STARTED / NOT AUTHORIZED.  
> Part 14 freezes 68 explicit `...Row` mappings across seven DB-family modules, zero baseline ORM relationships/cascades, five Core-only current-view handles, exact NativeRef/ScopedRecordRef/MaterialStateRef typing, 68 PK + 2 UQ + 25 explicit Index metadata reconciliation, migration-owned functions/triggers/views, explicit mapping loading, and deterministic transaction-scoped advisory-lock key derivation/namespace ordering.  
> Per explicit user direction, protected-`main` realignment remains intentionally deferred to a later separate gate. This overlay supersedes only older CURRENT/resume prose below that says Parts 1–13 or that SQLAlchemy mapping planning is still next/unfrozen; historical derivation/evidence remains preserved.  

> **CURRENT CP6-03 RESUME — 2026-08-24 / MIGRATION DAG FROZEN**  
> The authoritative current operational state is now: **Final Actual PostgreSQL Object Inventory FROZEN + DB-U08 CLOSED + DB-U15 CLOSED + DB-U21 CLOSED + Migration / Materialization DAG FROZEN**. Canonical authority is `docs/database/dante-postgresql-database.md` + Parts 2–13. **GLOBAL DB-U OPEN = 0**. The exact next CP6-03 block is **SQLALCHEMY MAPPING PLAN**. The second full tombstone audit has NOT yet run, Gate 03 is NOT earned, and CP6-04 remains NOT STARTED / NOT AUTHORIZED.  
> The frozen DAG is: P0 provisioning ACL hardening prerequisite, then seven linear Alembic business nodes `cp6_native_identity_address → cp6_scoped_material_control → cp6_schedule_actual_session → cp6_recurrence → cp6_core_integrity_current_views → cp6_occurrence_generation → cp6_runtime_acl_activation`. Allocation reconciles exactly to **68 tables / 95 indexes / 14 routines / 75 triggers / 5 views**, with runtime business DML activated only in the final ACL node.  
> Per explicit user direction, protected-`main` realignment remains intentionally deferred to a later separate gate. This overlay supersedes only older CURRENT/resume prose below that says Parts 1–12 or that the migration/materialization DAG is still next/unfrozen; historical derivation/evidence remains preserved.  

> **CURRENT CP6-03 RESUME — 2026-08-24 / DB-U21 CLOSED**  
> The authoritative current operational state is now: **Final Actual PostgreSQL Object Inventory FROZEN + DB-U08 CLOSED + DB-U15 CLOSED + DB-U21 Exact Object-Level PostgreSQL Privilege Matrix CLOSED**. Canonical authority is `docs/database/dante-postgresql-database.md` + Parts 2–12. **GLOBAL DB-U OPEN = 0**. The exact next CP6-03 block is **MIGRATION / MATERIALIZATION DAG**. The second full tombstone audit has NOT yet run, Gate 03 is NOT earned, and CP6-04 remains NOT STARTED / NOT AUTHORIZED.  
> DB-U21 freezes the exact least-privilege baseline: 68/68 runtime SELECT, 54/68 INSERT, exact 14-table no-INSERT set, zero table-level runtime UPDATE, five `current_until_at` column updates, zero direct base-table DELETE, five bounded current-view ACLs with DELETE only for Schedule/Actual, 14 integrity routines with no direct runtime/PUBLIC EXECUTE, migration-owned business ACLs, and removal of CP3 blanket default/ALL-object grants during CP6-04. Earlier owner-row locking wording is hardened where PostgreSQL would require a fake UPDATE privilege: transaction-scoped advisory serialization is used when no truthful mutable row can provide the lock.  
> Per explicit user direction, protected-`main` realignment remains intentionally deferred to a later separate gate. This overlay supersedes only older CURRENT/resume prose below that says Parts 1–11, DB-U21 is still open/next, global DB-U remains nonzero, or blanket owner-row locking/grants remain current; historical derivation/evidence remains preserved.  

> **CURRENT CP6-03 RESUME — 2026-08-24 / DB-U15 CLOSED**  
> The authoritative current operational state is now: **Final Actual PostgreSQL Object Inventory FROZEN + DB-U08 CLOSED + DB-U15 Final Structural / Query Index Matrix CLOSED**. Canonical authority is `docs/database/dante-postgresql-database.md` + Parts 2–11. The surviving global DB-U open set is exactly **DB-U21 only**; the exact next design block is **DB-U21 — exact object-level PostgreSQL privilege matrix**. The second full tombstone audit has NOT yet run, Gate 03 is NOT earned, and CP6-04 remains NOT STARTED / NOT AUTHORIZED.  
> DB-U15 freezes **95 DANTE-owned baseline indexes**: retained 78-index structural floor + 16 justified referencing-side FK/structural indexes + 1 quota-period query/concurrency index. All 68 FKs were reviewed; 52 are already covered by PK/UQ/partial-leading access and 16 require added indexing. No speculative GiST/GIN/BRIN/trigram/vector/INCLUDE index was added.  
> Per explicit user direction, protected-`main` realignment remains intentionally deferred to a later separate gate. This overlay supersedes only older CURRENT/resume prose below that says Parts 1–10, DB-U15 is still open/next, or 78 is the final index count; historical derivation/evidence remains preserved.  

> **CURRENT CP6-03 RESUME — 2026-08-24 / DB-U08 CLOSED**  
> The authoritative current operational state is now: **Final Actual PostgreSQL Object Inventory FROZEN + DB-U08 Final PostgreSQL Object Naming CLOSED**. Canonical authority is `docs/database/dante-postgresql-database.md` + Parts 2–10. The surviving global open set is exactly `DB-U15 / DB-U21`; the exact next design block is **DB-U15 — final structural/query index matrix**. The second full tombstone audit has NOT yet run, Gate 03 is NOT earned, and CP6-04 remains NOT STARTED / NOT AUTHORIZED.  
> DB-U08 freezes: existing Part-9 table/column/view identifiers unchanged; CP3 `pk/fk/uq/ix/ck` convention retained; explicit `ux/trg/ctrg` additions; 68 exact PK names; 68 FK outcomes with 17 direct convention names + 51 explicit semantic aliases for overlength names; current 78-index floor names; 14 integrity-routine names; 75 trigger names; 63-byte/unquoted/collision policy; migration revision/file naming policy.  
> Per explicit user direction, protected-`main` realignment is intentionally deferred to a later separate gate. This overlay supersedes only older CURRENT/resume prose below that says Parts 1–9, DB-U08 is still open/next, or `FINAL ACTUAL POSTGRESQL OBJECT INVENTORY NEXT`; historical derivation/evidence remains preserved.  

> **CURRENT CP6-03 RESUME — 2026-08-24 / INVENTORY FREEZE**  
> The authoritative current operational state is now: **Final Actual PostgreSQL Object Inventory FROZEN** in `docs/database/dante-postgresql-database-part-9.md`, section 38. Parts 1–9 are one canonical Database Architecture & Reference. Checkpoint J / DB-U23 remains CLOSED; the surviving global open set remains exactly `DB-U08 / DB-U15 / DB-U21`; the exact next design block is **DB-U08 — final PostgreSQL object naming**. The second full tombstone audit has NOT yet run, Gate 03 is NOT earned, and CP6-04 remains NOT STARTED / NOT AUTHORIZED. This overlay supersedes only older CURRENT/resume prose below that says Parts 1–8 or `FINAL ACTUAL POSTGRESQL OBJECT INVENTORY NEXT`; all historical derivation, evidence and process rationale below remain preserved.  
> Inventory freeze: **68 DANTE-owned tables + 5 bounded current views; scoped families = schedule/actual; MaterialState facets = schedule.placement / actual.realization / session.timing / routine.recurrence / event.recurrence; minimum structural-index floor = 78; bounded integrity roles = 14 with 75 table-trigger attachments (18 immediate + 57 deferred)**. Exact SQL identifiers remain DB-U08; the complete final index matrix remains DB-U15; exact ACLs remain DB-U21.  
> Per explicit user direction, protected-`main` realignment is intentionally deferred to a later separate gate and is NOT part of this inventory freeze. Do not reinterpret temporary branch divergence as permission to merge `main` during the current CP6 design sequence.  

# Workstream — CP6 Concrete PostgreSQL Database

- Status: **ACTIVE / DATABASE BLUEPRINT + MATERIALIZATION**
- Product: **DANTE**
- Repository: `MattiaRubino/dante`
- Branch: `feature/logical-postgresql`
- Protected-main anchor at branch origin: `fd3bc8dd918cf6aadeff4572221af68612c3cb42`
- Current scope-realignment PRE-SCOPE: `7ac8b5be7b61c85f1b0952206d5bbd6a3a58a6b2`
- Upstream Domain Model: **CLOSED / SEMANTICALLY COMPLETE FOR CURRENT SCOPE**
- Upstream Logical Model: **CLOSED / 57 OF 57 CLASSIFIED / WL-H01..WL-H12 ACTIVE**
- Upstream Physical Model: **CLOSED / SELECTED / ACCEPTED / PostgreSQL 18 MAJOR FAMILY; exact phase-time patch 18.4**
- Production backend scaffold: **CP1–CP5 CLOSED / DIRECT QA PASS / INTEGRATED IN PROTECTED main**
- CP6-00: **COMPLETE**
- CP6-01: **CLOSED / GATE 01 PASS**
- CP6-02: **CLOSED / GATE 02 PASS**
- CP6-03: **ACTIVE / CHECKPOINT J + DB-U23 CLOSED / FINAL ACTUAL POSTGRESQL OBJECT INVENTORY NEXT / GATE 03 NOT YET EARNED**
- CP6-03 blueprint/reference: **`docs/database/dante-postgresql-database.md` + Parts 2–8 as one canonical authority**
- Current global DB-U open set: **DB-U08 / DB-U15 / DB-U21**
- Final independent second tombstone audit: **NOT YET RUN / MANDATORY BEFORE GATE 03**
- Current PostgreSQL technical patch: **18.6 / DIRECT REMOTE FOUNDATION REGRESSION PASS**
- PostgreSQL 18.6 evidence: **Backend CI run `32568664940` at HEAD `ec3dc795b5e044daa3a77723c94a1b4b5b92865c`**
- Current DANTE business database: **NOT YET MATERIALIZED**
- First product vertical: **POST-CP6 / NOT PART OF THIS WORKSTREAM**

## 0. Current durable resume and routing reconciliation — 2026-08-23

This section is the durable current resume state for CP6 and supersedes older **process/routing/resume prose only** wherever that older prose still points to Vertical #1 inside CP6, to `CP6-06`/`CP6-07`, or to a pre-Checkpoint-J CP6-03 position. It does **not** rewrite the historical truth or technical decisions of closed CP6-01/02 artifacts.

Current exact state:

```text
CP6-03
ACTIVE

DATABASE REFERENCE
Parts 1–8 active together

CHECKPOINT J / DB-U23
CLOSED

57 / 57 FINAL MATERIALIZATION DISPOSITION
PASS AFTER HARDENING

LOCAL EXACT OPEN
0

GLOBAL DB-U OPEN
DB-U08  final PostgreSQL object naming
DB-U15  final structural/query index matrix
DB-U21  exact object-level privilege matrix

NEXT DESIGN BLOCK
FINAL ACTUAL POSTGRESQL OBJECT INVENTORY

SECOND FULL TOMBSTONE AUDIT FROM ZERO
NOT YET RUN
MANDATORY BEFORE GATE 03

GATE 03
NOT YET EARNED

CP6-04 REAL DATABASE MATERIALIZATION
NOT STARTED / NOT AUTHORIZED
```

Current routing map for any older CP6-01/02 proof/staging prose:

```text
old “CP6-05 designs Vertical #1”
→ SUPERSEDED
→ CP6-05 = WHOLE DATABASE DIRECT QA + CP6 CLOSURE

old CP6-06 / CP6-07 proof or clean-room route
→ SUPERSEDED AS CHECKPOINT NAMES
→ applicable database proof/clean-room work is absorbed into CP6-03..05
→ application-only proof remains POST-CP6 with the first qualifying vertical

old “CP6 foundation + Vertical #1 exact design”
→ SUPERSEDED AS PROCESS ROUTING
→ CP6 = database blueprint + materialization + direct DB QA
→ first product vertical = separate POST-CP6 phase
```

The current exact remaining CP6-03 order is:

```text
1. Final Actual PostgreSQL Object Inventory
2. DB-U08 exact object naming
3. DB-U15 exact structural/query index matrix
4. DB-U21 exact object-level privilege matrix
5. migration/materialization DAG
6. SQLAlchemy mapping plan
7. Database Dictionary readiness
8. direct PostgreSQL proof/test plan
9. SECOND FULL TOMBSTONE AUDIT FROM ZERO
10. Gate 03 only if the whole blueprint remains clean
```

At Gate 03, STOP. Entering CP6-04 creates the real DANTE business database and therefore requires a separate explicit user-approved materialization gate.

## 1. Purpose — corrected execution boundary

CP6 is the phase that turns the already-closed DANTE Domain + Logical + Physical model into the **concrete PostgreSQL database of DANTE**.

The workstream is not a generic foundation exercise and it is not a first-product-vertical implementation.

The intended sequence is:

```text
CLOSED DOMAIN
+ CLOSED LOGICAL
+ ACCEPTED PHYSICAL POSTGRESQL MAPPING
+ CLOSED POSTGRESQL CONSTITUTION
        ↓
WHOLE DANTE DATABASE BLUEPRINT
        ↓
REAL POSTGRESQL MATERIALIZATION
        ↓
DIRECT DATABASE QA / CLEAN-ROOM REVIEW
        ↓
CP6 CLOSED
        ↓
SEPARATE FIRST PRODUCT VERTICAL PHASE
```

### What CP6 MUST do

CP6 MUST derive, design and then materially implement everything that is already determinable from the closed model without inventing application behavior that belongs to a later product vertical.

That includes, where the closed model requires it:

```text
relational families and concrete tables
owner identities and address/control structures
specific relations and relation tables
MaterialStateRef address/control structures
owner-specific material-state/history structures
explicit current-state bindings
history / correction / replacement / reconciliation structures
canonical/provider/derived separation
provenance and governance persistence structures
typed PostgreSQL columns
PK / FK / UNIQUE / CHECK / EXCLUDE / range constraints
required reference-family integrity
structural indexes and index justification
migration dependency order
Alembic business-schema migrations
SQLAlchemy mappings for the materialized database
owner / migrator / runtime privilege posture for those objects
real PostgreSQL positive/negative acceptance tests
real migration fresh→head / drift / upgrade-path proof where applicable
real concurrency / reference / history proof where the materialized database makes it executable
```

### What CP6 MUST NOT do

CP6 MUST NOT implement the first product vertical as an application slice.

Out of scope until CP6 is closed:

```text
first-vertical application use cases
first-vertical application services
first-vertical persistence adapters that encode application behavior
business HTTP/API routes
frontend consumption
product workflow orchestration
product-specific UI behavior
activation of dormant specialist infrastructure without a real database-level trigger
```

The important boundary is therefore:

```text
DATABASE DESIGN + DATABASE IMPLEMENTATION
= CP6

FIRST APPLICATION VERTICAL
= AFTER CP6
```

## 2. Scope-realignment authority

This section corrects the process boundary that had become too restrictive during CP6-02 planning.

The technical decisions closed by CP6-01 and CP6-02 remain valid and are **not reopened**.

In particular, the following remain closed:

```text
57 / 57 Logical classification
15 LR-01 native owners
LR-01..LR-13 meanings
WL-H01..WL-H12
NativeRef / ScopedRecordRef / MaterialStateRef / ExternalRef separation
PostgreSQL 18 as sole canonical persistence/material-history authority
owner-specific canonical/history/relation thesis
UUIDv7 / native PostgreSQL uuid posture
bounded heterogeneous NativeRef anchor rule
bounded MaterialStateRef address/control rule
current-state explicit binding rule
missingness / history / temporal rules
constraint / index / transaction / idempotency rules
Alembic migration doctrine
owner / migrator / runtime privilege model
specialist-capability activation boundaries
```

What is superseded is only earlier **process/staging prose** that said or implied any of the following:

```text
no business schema anywhere in CP6
no business Alembic migrations anywhere in CP6
no SQLAlchemy business mappings anywhere in CP6
exact DANTE tables/columns must wait for a product vertical
CP6 ends with Vertical #1 selected/designed but with the DANTE database still unmaterialized
```

Those statements are no longer current CP6 execution authority.

They must be read narrowly as describing the bounded CP6-01/CP6-02 checkpoints themselves, which correctly created no business schema while coverage and global PostgreSQL rules were still being closed.

This scope correction does **not** retroactively change the truth of Gate 01 or Gate 02: those gates passed without business DDL, exactly as recorded.

## 3. Authority and precedence

Repository truth outranks conversation memory.

For CP6, use this order:

1. protected-main code/migrations/tests and accepted model/ADR truth;
2. closed Domain / Logical / Physical authorities;
3. closed CP6-01 coverage artifacts;
4. closed CP6-02 PostgreSQL Constitution for technical doctrine;
5. **this workstream for current CP6 execution scope and resume point**;
6. current project-status / roadmap entry points;
7. historical evidence / closed branches / conversation memory.

Where older CP6-02 process prose conflicts with section 0–2 of this workstream, section 0–2 is the current execution-boundary/routing authority. CP6-02 technical doctrine remains closed and fully authoritative.

## 4. Mandatory continuation bootstrap

Before a material CP6 write, read or verify at minimum:

```text
README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md

docs/development/agent-operating-manual.md
docs/development/operating-rules.md
docs/development/documentation-and-handoff.md
docs/development/branching-and-environments.md
docs/development/repository-engineering-safety.md

docs/database/README.md
docs/database/dante-postgresql-database.md
docs/database/dante-postgresql-database-part-2.md
docs/database/dante-postgresql-database-part-3.md
docs/database/dante-postgresql-database-part-4.md
docs/database/dante-postgresql-database-part-5.md
docs/database/dante-postgresql-database-part-6.md
docs/database/dante-postgresql-database-part-7.md
docs/database/dante-postgresql-database-part-8.md

this workstream handoff
```

Then consume the relevant closed model authorities rather than re-deriving them from memory.

### CP6-01 authority

```text
docs/development/backend-cp6-01-concrete-persistence-coverage.md
= exact 57/57 owner/role persistence ledger

docs/development/backend-cp6-01-concrete-persistence-coverage-part-2.md
= cross-cutting LR/WL-H/PG-R/DEFER-WL/HG/SC/PSV ledger

docs/development/backend-cp6-01-concrete-persistence-coverage-closure.md
= Gate 01 closure
```

### CP6-02 authority

```text
docs/development/backend-cp6-02-postgresql-persistence-constitution.md
= closed reusable PostgreSQL doctrine

docs/development/backend-cp6-02-postgresql-persistence-constitution-closure.md
= Gate 02 closure

docs/decisions/ADR-010-postgresql-persistence-constitution.md
= durable architectural acceptance record
```

### Physical-consuming authority

At minimum:

```text
docs/physical-model/README.md
docs/physical-model/pm-02-primary-mapping-overview-v1.md
docs/physical-model/mappings/postgresql-18.4-v1.md
docs/physical-model/pm-03-semantic-hard-gate-preflight-v1.md
docs/physical-model/pm-11-explicit-selection-v1.md
docs/physical-model/pm-12-accepted-physical-model-v1.md
docs/physical-model/pm-13-clean-room-qa-v1.md
docs/physical-model/recommendation/post-selection-validation-register-v1.md
```

The `18.4` Physical files preserve phase-time evidence. Current compatible PostgreSQL patch is 18.6.

## 5. Inherited semantic baseline

### 5.1 Whole Logical coverage

```text
DOMAIN CONCEPTS CLASSIFIED       57 / 57
DOMAIN OWNER GAP                  0
UNCLASSIFIED                      0
NEW DOMAIN OWNER REQUIRED         0
GENERIC FALLBACK DEPENDENCIES     0
OWNERLESS MATERIAL STATE          0
REQUIRED UNIVERSAL ROOTS           0
```

CP6 consumes this model. It does not run another owner census.

### 5.2 LR-01 native identity set

Exactly:

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

`Actor`, `Subject` and `Resource` remain roles/capabilities, not generic native owners.

### 5.3 Representation families

```text
LR-01 Native identity-bearing record
LR-02 Dependent/material contextual record
LR-03 Specific typed association/relation
LR-04 Value semantics
LR-05 Rule/policy/specification
LR-06 Realization/result
LR-07 Version/correction/lineage/history
LR-08 Derived/effective projection/read model
LR-09 Provider/external state and mapping
LR-10 Flexible low-consequence descriptive metadata
LR-11 Unresolved/candidate interpretation
LR-12 Product/organizational profile
LR-13 Specialist extension record
```

### 5.4 Reference families

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

No universal semantic `kind + id` root.

### 5.5 High-risk non-collapse invariants

Preserve at minimum:

```text
Person != Account != Principal != Actor
Person != Living Referent != Asset
Subject != Resource != native identity
Possibility != Goal != Proposal != Decision != Plan != Activity
Routine != Recurrence != Occurrence
Occurrence != Schedule != Session != Actual
Actual != Observation != Outcome
Evidence != Provenance
Version != Reconciliation
Authority != Visibility
Agreement != Consent
Ownership != Possession
Collective != current Membership set
Schedule != Capacity Claim != Resource Allocation != Actual use
provider state != canonical DANTE state
derived projection != canonical truth
current state != historical state
correction != silent overwrite
AI/solver inference != accepted canonical effect
```

## 6. WL-H01..WL-H12 remain active

All twelve Whole-Logical hardenings constrain blueprint, materialization and direct QA.

Especially:

```text
WL-H01 Agreement terms bind justified owned MaterialStateRef
WL-H02 governed consequential effects preserve semantic target/effect/governance basis
WL-H03 projections preserve source/material/disclosure basis
WL-H04 absence != explicit negative
WL-H05 stale-write-sensitive mutation uses expected MaterialStateRef/semantic equivalent
WL-H06 idempotency != semantic identity
WL-H07 multi-owner invariant gets truthful atomicity or staged/reconciliation semantics
WL-H08 canonical state != provider apply/sync state
WL-H09 consequential derived use binds/revalidates derivation basis
WL-H10 retention/redaction/tombstone preserves truthful continuity and no ID reuse
WL-H11 AuthZ provenance does not redefine Domain governance
WL-H12 selective disclosure includes non-interference across indirect surfaces
```

## 7. Closed PostgreSQL mapping thesis

The concrete database must follow the accepted thesis:

```text
owner-specific canonical tables/families
+
owner-specific material-state/history tables/families
+
specific relation tables/families
+
bounded technical address/control structures only where genuine heterogeneous addressing requires them
+
separate provider / projection / technical concerns
```

Rejected globally:

```text
universal Entity / Thing table
universal Relationship / generic edge table
canonical EAV / property bag
universal event ontology
universal Fact/Version semantic payload root
JSONB required-semantic escape hatch
PostgreSQL inheritance as ontology
```

### NativeRef

```text
homogeneous target
→ direct FK

genuinely heterogeneous NativeRef
→ bounded native-address anchor
```

### MaterialStateRef

```text
stable UUIDv7 MaterialStateRef
+
bounded material-state address/control record
+
exact owner + facet
+
owner-specific material-state payload row
+
explicit current accepted-state binding where required
```

Material-state control infrastructure is not a universal semantic Fact/Version table.

### Relations

```text
simple binary LR-03
→ specific relation table/family

qualified/material/consequential LR-03
→ contextual relation record with scoped identity/history/governance as required

true n-ary relation
→ preserve n-ary semantics
```

## 8. Existing technical PostgreSQL foundation

Already materialized and frozen through CP3:

```text
schema                               dante
SQLAlchemy async                     2.0 stable line
psycopg                              3
Alembic                              one environment / one DAG / one head
one AsyncEngine per process
one async_sessionmaker per process
one AsyncSession per app operation
autobegin=False
autoflush=True
expire_on_commit=False
outer app operation owns commit/rollback
adapter may flush, never implicit commit
READ COMMITTED default

dante_owner                          NOLOGIN
dante_migrator                       LOGIN NOINHERIT + bounded SET ROLE
dante_runtime                        LOGIN NOINHERIT / runtime DML posture
```

No generic `Repository[T]`, generic UnitOfWork or generic BaseService is introduced merely for uniformity.

### Current PostgreSQL patch evidence

```text
PostgreSQL architecture             major 18
Physical / CP2 / CP3 exact patch   18.4 / historical exact evidence
current technical patch            18.6
PostGIS                            3.6.4
pgvector                           0.8.6
Backend CI run                    32568664940
executed HEAD                     ec3dc795b5e044daa3a77723c94a1b4b5b92865c
Backend Quality                   SUCCESS / 32 fast tests PASS
Backend PostgreSQL                SUCCESS / 18 PostgreSQL tests PASS
Backend CI Gate                   SUCCESS
current corpus                    50 / 50 covered across mandatory CI lanes
18.6 release-note impact          PASS / NO CURRENT POST-UPGRADE ACTION
```

Historical 18.4 evidence is never rewritten as 18.6 evidence.

## 9. CP6-01 — CLOSED / GATE 01 PASS

Gate 01 established complete persistence coverage before concrete schema design.

Closure summary:

```text
57 / 57 Domain concepts                         PASS
15 / 15 LR-01 native owners                     PASS
LR-01..LR-13                                    PASS
cross-cutting / non-owner coverage              PASS
reference pressure                              PASS
materiality/history pressure                    PASS
canonical/provider/derived boundaries           PASS
dependency pressure                             PASS
WL-H01..WL-H12                                  PASS
PG-R01..PG-R10                                  PASS
DEFER-WL01..20                                  COMPLETE
HG-01..HG-12 carry-forward                      COMPLETE / TRUTHFUL
SC-001..SC-035 canonical names/stages           PASS
full PSV stage ownership                        PASS
semantic owner reclassification                 0
generic semantic fallback                       0
unexplained canonical JSONB fallback            0
business DDL at Gate 01                         0
```

The fact that Gate 01 itself had zero business DDL is phase-local truth, not a prohibition on later CP6 materialization.

CP6-01 Part 2 is a mandatory Gate-03 input because **57/57 Domain coverage is necessary but not sufficient**. Persistence-relevant non-57/cross-cutting constructs such as `Account`, `Principal`, reference-address/control families, idempotency/provenance/correlation controls, provider/derived state, tombstone/retirement continuity, outbox/capability-triggered state and other Part-2 entries must not disappear merely because they are not Domain owners.

## 10. CP6-02 — CLOSED / GATE 02 PASS

Gate 02 closed reusable PostgreSQL doctrine.

Closed rule families:

```text
TECH  technology lifecycle
ID    physical identity
REF   reference addressing
MAT   material state/current truth
HIST  historical truth
TIM   temporal truth
MISS  missing/unknown/negative
LIFE  lifecycle/retention/tombstone
TYP   PostgreSQL types
REL   relation doctrine
CON   constraints
IDX   indexes
TX    transaction/concurrency
IDEM  idempotency
PROV  provenance
CAP   PostgreSQL capability boundaries
MIG   migration/evolution
SEC   ownership/privileges
QA    direct persistence acceptance
```

Final targeted post-repair review was CLEAN.

The fact that Gate 02 itself created no business schema is also phase-local truth. CP6-02 had to close global rules before whole-database blueprint/materialization began.

## 11. Remaining CP6 plan — simplified and concrete

The remaining work is intentionally reduced to three real stages. Do not fragment it into additional documentation-only pseudo-phases.

```text
CP6-03  WHOLE DANTE DATABASE BLUEPRINT
        ↓
CP6-04  WHOLE DANTE DATABASE MATERIALIZATION
        ↓
CP6-05  WHOLE DATABASE DIRECT QA + CP6 CLOSURE
        ↓
POST-CP6 FIRST PRODUCT VERTICAL
```

Earlier CP6 planning that described CP6-04 as “Vertical #1 Selection”, CP6-05 as “Vertical #1 Exact Persistence Design”, CP6-06 and CP6-07 as separate pre-vertical layers is superseded by this current workstream plan.

No information is lost: their useful topology, dependency, direct-proof and clean-room requirements are absorbed into CP6-03..05 below.

## 12. CP6-03 — Whole DANTE Database Blueprint

### Status

```text
ACTIVE / CHECKPOINT J + DB-U23 CLOSED / FINAL ACTUAL POSTGRESQL OBJECT INVENTORY NEXT / GATE 03 NOT YET EARNED
```

Current blueprint/reference:

```text
docs/database/dante-postgresql-database.md
+ docs/database/dante-postgresql-database-part-2.md
+ docs/database/dante-postgresql-database-part-3.md
+ docs/database/dante-postgresql-database-part-4.md
+ docs/database/dante-postgresql-database-part-5.md
+ docs/database/dante-postgresql-database-part-6.md
+ docs/database/dante-postgresql-database-part-7.md
+ docs/database/dante-postgresql-database-part-8.md
= ONE CANONICAL DATABASE ARCHITECTURE & REFERENCE
```

Checkpoint J closed the residual `DB-U23` materialization-disposition gap found by the first total pre-freeze audit. It did not freeze the final actual object inventory. The current global open set is exactly `DB-U08`, `DB-U15`, `DB-U21`.

### Purpose

Translate the complete closed model into the concrete relational database blueprint before implementation.

This stage must answer **what the DANTE database actually is**.

`WHOLE DANTE DATABASE` has a strict meaning:

```text
maximum non-speculative persistence
that is derivable today from closed Domain + Logical + Physical + CP6 authority
```

It does **not** mean inventing every table DANTE might conceivably need in the future.

### Required outputs — Domain coverage

For the entire 57/57 model, derive where applicable:

```text
concrete table/family name
semantic owner/role
canonical vs contextual vs relation vs state/history vs provider/derived role
columns and exact meaning
PostgreSQL type
PK
stable IDs
FK / target family
UNIQUE
CHECK
NULL/missingness semantics
range / EXCLUDE / temporal constraints
material-state address/control binding
current-state binding
history/lineage/correction behavior
relation topology
provenance/governance binding
retention/tombstone/redaction behavior
structural/query index requirement
privilege posture
dependency/prerequisite
migration batch/order
SQLAlchemy mapping shape
required direct tests
```

### Required outputs — CP6-01 Part-2 cross-cutting/non-owner coverage

Gate 03 MUST also account for **100% of the CP6-01 Part-2 persistence-relevant constructs**, including constructs intentionally outside the 57 Domain census.

Every Part-2 entry must receive exactly one implementation disposition:

```text
MATERIALIZE IN CP6
→ independent/shared/concrete persistence is required and determinable now

NO INDEPENDENT PERSISTENCE
→ represented through another accepted owner/value/reference/mechanism;
  exact owning representation must be named

GENUINELY DEFERRED
→ cannot be materialized without inventing semantics or activating a dormant capability;
  exact reason + exact future owner/stage/trigger must be recorded
```

At minimum explicitly account for:

```text
Account
Principal / security context
ReferenceAddress / reference-family control
NativeRef heterogeneous anchor pressure
ScopedRecordRef heterogeneous addressing pressure where justified
MaterialStateRef address/control
current accepted-state binding
correction/replacement/reconciliation lineage
Governed Operation / Effect persistence pressure
idempotency
correlation / causation technical linkage
projection / disclosure basis
provider / sync / apply state
flexible metadata boundary
candidate / unresolved persistence pressure
product/profile pressure
specialist-extension pressure
Actor / Subject / Resource role addressing
Capacity Claim persistence pressure
tombstone / retirement / redaction continuity
anti-resurrection reconciliation pressure
transactional outbox capability-triggered state
PowerSync/local noncanonical state boundary
search/vector/derived index/cache pressure
```

This accounting does **not** turn those constructs into new Domain owners.

### Dependency/materialization DAG

The blueprint MUST produce an explicit implementation order.

At minimum distinguish:

```text
technical CP3 base already present
shared bounded address/control structures
native owner families
dependent/contextual records
material-state/history structures
specific relation families
rules/specifications/results
provider/integration structures
derived/query structures
specialist structures only when selected capability is actually required by the closed model
```

The DAG is about database dependencies, not a product-vertical roadmap.

### Non-speculative rule

A concrete table/column/constraint is included when it follows from accepted Domain/Logical/Physical/Constitution truth.

Do not omit a determinable database structure merely by labeling it “vertical-specific”.

Conversely, do not invent a field, state, index, precision, SRID, recurrence parameter or product workflow whose semantics were not actually closed upstream.

Where something is truly not determinable, record the exact unresolved parameter and why; do not create a placeholder schema pretending it is known.

### Gate 03

```text
57 / 57 persistence coverage preserved                         PASS
CP6-01 Part-2 cross-cutting/non-owner constructs accounted    100%
Account explicitly accounted                                  PASS
Principal/security context explicitly accounted               PASS
reference-address/control families explicitly accounted       PASS
MaterialState control/current binding explicitly accounted    PASS
idempotency/provenance/correlation explicitly accounted       PASS
provider/derived/tombstone/outbox pressures accounted         PASS
all determinable relational families concrete                 PASS
all determinable tables/columns/types concrete                PASS
all determinable PK/FK/reference topology concrete            PASS
all determinable material-state/history topology concrete     PASS
all determinable relation topology concrete                   PASS
all determinable constraints concrete                         PASS
all determinable structural indexes justified                 PASS
migration/materialization DAG complete                         PASS
SQLAlchemy mapping plan complete                               PASS
direct-test plan complete                                     PASS
second full tombstone audit from zero                          PASS
unclassified cross-cutting persistence construct              0
unclassified database family                                  0
unresolved DB-U                                                0
accidental new Domain owner                                    0
generic Entity/Relationship/EAV shortcut                       0
speculative placeholder schema                                 0
application Vertical #1 implementation                         0
```

Only after Gate 03 is clean does real DANTE database materialization become eligible for a separate explicit authorization gate.

## 13. CP6-04 — Whole DANTE Database Materialization

### Purpose

Implement the approved CP6-03 blueprint in the repository and real PostgreSQL environment.

This is where CP6 stops being mainly documentation and starts producing the real DANTE database.

### Authorized implementation classes

After Gate 03 **and a separate explicit user-approved materialization gate**, CP6-04 may create/update:

```text
Alembic business-schema revisions
DANTE business tables
bounded native/scoped/material-state address/control tables
owner-specific canonical tables
owner-specific material-state/history tables
specific relation tables
provider/integration tables where already determined
bounded derived/query persistence where already determined
PostgreSQL constraints and indexes
SQLAlchemy business mappings / metadata
mapping-specific value codecs/types where required
object ownership/default privileges/grants
real PostgreSQL acceptance fixtures/tests
migration/drift checks
```

### Required implementation discipline

```text
one Alembic DAG/head
no metadata.create_all deployment authority
applied migration history immutable
reviewed deterministic naming
native PostgreSQL types over generic payloads
FK/reference integrity in DB
NO ACTION delete default unless semantic proof says otherwise
MaterialStateRef != storage token
explicit current-state binding
history not silent overwrite
provider/derived state not canonical automatically
outer transaction ownership preserved
runtime DDL denied
```

### Implementation batching

Do not attempt one giant migration if the dependency DAG supports safer bounded batches.

Each batch must have:

```text
exact PRE-SCOPE
exact CREATE/UPDATE/DELETE paths
migration dependency relation
fresh-DB migration proof
negative constraint/reference proof where executable
schema-drift proof
remote/local readback
```

### What remains out of scope in CP6-04

```text
application use cases
business service orchestration
product API
frontend
first product vertical behavior
provider workflow activation without real need
PowerSync/Restate/R2/pgBackRest activation merely to complete a checklist
```

A SQLAlchemy mapping is allowed because it is part of materializing the DANTE database contract. A product persistence adapter/use case is not automatically allowed because that belongs to application behavior.

## 14. CP6-05 — Whole Database Direct QA + CP6 Closure

### Purpose

Prove that the materialized DANTE database matches the closed model and blueprint, then close CP6.

### Required direct QA

Use real PostgreSQL for PostgreSQL semantics.

Where the materialized schema makes the proof applicable, cover:

```text
fresh database → Alembic head
single canonical Alembic head
schema drift / metadata alignment
owner/migrator/runtime privilege matrix
all material FK/reference integrity
wrong-family and dangling-reference rejection
positive/negative CHECK/UNIQUE/EXCLUDE cases
missingness distinctions where represented
MaterialStateRef owner/facet/current-binding integrity
history reconstruction / correction without false overwrite
idempotency structures if materialized by the database model
expected-state/concurrency behavior where schema-level subject exists
transaction rollback/atomicity
migration downgrade only where truthful
upgrade path from prior supported schema state once such prior state exists
PostGIS/FTS/pgvector only where the concrete database actually materializes those selected capabilities
```

### Truthful staged evidence

Some evidence cannot exist before a real application vertical, real V1→V2 evolution, destructive restore or dormant specialist activation.

Those items remain explicitly staged rather than being faked.

Examples:

```text
HG-09 destructive retention/restore
HG-11 real V1→V2 semantic evolution
HG-12 destructive recovery
PSV-01 old-backup anti-resurrection
specialist activation proofs without an activated consumer
application-level governed-effect scenarios that require a real use case
```

### Clean-room closure question

A fresh engineer should be able to inspect repository truth and answer:

```text
what is the DANTE database?
what tables/families exist and why?
what does every column mean?
how are references enforced?
how are current and historical states represented?
what must PostgreSQL reject?
what migration history creates the schema?
what SQLAlchemy mappings correspond to it?
what privileges apply?
what direct tests prove the database contract?
what is still intentionally deferred because it requires application behavior or later lifecycle evidence?
```

### CP6 closure condition

Only after CP6-05 PASS may the workstream become:

```text
CP6
CLOSED / CONCRETE POSTGRESQL DATABASE PASS

DANTE DATABASE
BLUEPRINT COMPLETE
MATERIALIZED TO MAXIMUM NON-SPECULATIVE EXTENT
MIGRATED
MAPPED
DIRECTLY TESTED
QA CLEAN

FIRST PRODUCT VERTICAL
NOT YET IMPLEMENTED
NEXT SEPARATE PHASE
```

## 15. Post-CP6 — First product vertical

The first product vertical starts **after CP6 closure** under a new separately approved workstream/branch boundary.

It consumes the database already derived and materially implemented from Domain/Logical/Physical.

Its purpose is not “invent the database for that vertical from scratch”.

It adds the first coherent application behavior over the already-materialized persistence model, for example as applicable:

```text
application use cases
capability-specific persistence adapters
commands/queries
business governance orchestration
API boundary
frontend/mobile consumption
end-to-end semantic scenarios
vertical-specific HG/PSV evidence
```

If real implementation uncovers a database requirement that genuinely could not have been determined during CP6, it may trigger a normal reviewed schema evolution. That is feedback, not the default plan.

## 16. PostgreSQL risk / proof carry-forward

The accepted Physical risk lanes remain active:

```text
PG-R01 technical anchor leakage
PG-R02 heterogeneous reference integrity
PG-R03 owner-specific history maintainability
PG-R04 expected-state concurrency
PG-R05 multi-owner write skew
PG-R06 Agreement/governance materiality
PG-R07 temporal/history semantics
PG-R08 lazy Occurrence
PG-R09 selective disclosure/non-interference
PG-R10 retention/restore anti-resurrection
```

CP6-03 assigns each risk to concrete database structures/tests where determinable.
CP6-04 materializes the corresponding DB mechanism where applicable.
CP6-05 directly proves what now has a real executable subject and truthfully carries the rest forward.

## 17. Post-selection validation carry-forward

The Physical PSV register remains authoritative.

Especially preserve:

```text
PSV-01 old-backup anti-resurrection
PSV-02 actual V1→V2 mapping/schema evolution
PSV-03 destructive restore + semantic verification
PSV-04 capacity/backpressure truthful degradation
PSV-05 WL-H12 system-level non-interference
PSV-06 → SC-017 Search hidden-result non-interference
PSV-07 → SC-018 FTS mixed filter/query correctness
PSV-35 selected PostgreSQL mapping end-to-end smoke corpus
```

A design or schema object existing is not a direct semantic PASS unless the qualifying scenario actually executes.

## 18. Specialist activation remains trigger-bound

Selection does not mean activation.

Still dormant until a real requirement exists:

```text
PgBouncer
PowerSync / logical replication
Restate
Cloudflare R2
pgBackRest + S3
OR-Tools
additional observability components
```

If the closed database model itself requires a PostgreSQL-native structure such as PostGIS geometry or FTS indexing, CP6 may materialize/test that database structure. This does not automatically activate the surrounding product/runtime capability.

## 19. Explicit non-goals

Unless concrete contradictory evidence forces a separately gated reopen, CP6 does not:

- redesign Domain semantics;
- rerun the Logical owner census;
- redefine LR-01..LR-13;
- change the four reference families;
- reselect PostgreSQL vs another canonical database;
- change canonical authority away from PostgreSQL;
- create a universal Entity/Thing root;
- create a universal Relationship/edge root;
- create canonical EAV/property-bag storage;
- adopt universal event sourcing as ontology;
- use JSONB to hide required semantics;
- create one service/module/API route per Logical concept mechanically;
- create generic Repository/UoW/BaseService abstractions;
- implement the first product vertical;
- create application use cases or product APIs;
- implement AuthN/AuthZ product behavior;
- activate dormant specialist infrastructure merely because selected;
- mutate frontend or brand assets;
- mutate CI/rulesets/CodeQL without separate authorization;
- mutate protected `main` directly;
- merge this branch outside the protected PR path.

## 20. Write / gate discipline

Every material repository mutation requires an exact bounded gate:

```text
BRANCH
feature/logical-postgresql

PRE-SCOPE
<exact live HEAD>

CREATE
<exact paths>

UPDATE
<exact paths>

DELETE
<exact paths>

PURPOSE
<bounded purpose>

EXPLICITLY OUT OF SCOPE
<bounded non-scope>
```

Immediately before the first write verify current branch HEAD equals approved PRE-SCOPE.

After writes:

```text
remote readback
PRE-SCOPE → HEAD compare
added/modified/deleted counts
unexpected paths = 0
branch relation to protected main
applicable tests/checks
truthful checkpoint status
```

Do not call a checkpoint PASS/CLOSED before its evidence contract is satisfied.

## 21. Current resume point

A fresh session must establish:

```text
1. feature/logical-postgresql live HEAD / protected-main relation;
2. CP6-00 COMPLETE;
3. CP6-01 CLOSED / GATE 01 PASS;
4. CP6-02 CLOSED / GATE 02 PASS;
5. PostgreSQL architecture = major 18;
6. Physical/CP2/CP3 historical exact patch = 18.4;
7. current technical patch = 18.6 / DIRECT REMOTE QA PASS;
8. this workstream supersedes earlier CP6 process prose that prohibited all business DB materialization;
9. ADR-010 records the accepted PostgreSQL Persistence Constitution without duplicating it;
10. CP6-03 is ACTIVE; Database Reference Parts 1–8 are one canonical authority;
11. Checkpoint J / DB-U23 is CLOSED;
12. final 57/57 materialization disposition is PASS AFTER HARDENING;
13. current local exact open = 0;
14. current global DB-U open = DB-U08 / DB-U15 / DB-U21 only;
15. exact next design block = FINAL ACTUAL POSTGRESQL OBJECT INVENTORY;
16. the second full tombstone audit from zero has NOT run and is mandatory before Gate 03;
17. Gate 03 is NOT YET EARNED;
18. CP6-04 business database materialization is NOT STARTED / NOT AUTHORIZED;
19. CP6-05 is whole-database direct QA + CP6 closure;
20. first product vertical begins only after CP6 is closed.
```

Immediate next action:

```text
CP6-03 — FINAL ACTUAL POSTGRESQL OBJECT INVENTORY

consume Parts 1–8 together
→ enumerate every surviving baseline PostgreSQL object exactly
→ include tables, views, types/domains, routines, triggers, constraints and dispatch/control structures actually required
→ exclude every object removed by later explicit no-DDL disposition
→ reconcile every scoped_family and MaterialState facet against the final survivor audit
→ verify every table/column/key/constraint can be implemented without semantic invention
→ keep DB-U08 / DB-U15 / DB-U21 OPEN during derivation
→ run cumulative whole-database audit over the inventory
→ show an exact write gate before saving the inventory freeze
```

After inventory freeze:

```text
DB-U08 exact naming
→ DB-U15 exact index matrix
→ DB-U21 exact privilege matrix
→ migration/materialization DAG
→ SQLAlchemy mapping plan
→ Database Dictionary readiness
→ direct PostgreSQL proof plan
→ SECOND FULL TOMBSTONE AUDIT FROM ZERO
→ Gate 03
```

No new Domain/Logical/Physical discovery cycle is implied.