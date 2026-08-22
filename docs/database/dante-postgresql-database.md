# DANTE PostgreSQL Database — Architecture, Reference & Whole-Database Blueprint

- **Status:** CP6-03 ACTIVE / CANDIDATE BLUEPRINT / GATE 03 NOT YET EARNED
- **Created:** 2026-08-22
- **Product:** DANTE
- **Database:** PostgreSQL 18 major family
- **Current repository patch:** PostgreSQL 18.6
- **Schema:** `dante`
- **Workstream:** `../workstreams/logical-postgresql.md`
- **Database documentation authority:** `README.md`
- **Persistence Constitution:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Persistence ADR:** `../decisions/ADR-010-postgresql-persistence-constitution.md`
- **CP6-01 Domain coverage:** `../development/backend-cp6-01-concrete-persistence-coverage.md`
- **CP6-01 cross-cutting coverage:** `../development/backend-cp6-01-concrete-persistence-coverage-part-2.md`
- **Implementation status:** business schema / business SQLAlchemy mappings / product vertical **NOT YET MATERIALIZED**

---

## 1. Purpose

This is the canonical human-readable specification of the concrete DANTE PostgreSQL database produced by CP6.

It has two simultaneous jobs:

1. **CP6-03 blueprint:** derive the maximum non-speculative database that follows from the closed Domain + Logical + Physical + PostgreSQL Constitution authorities;
2. **long-lived database reference:** remain the engineer-facing explanation of the database after CP6-04 materializes it and CP6-05 validates it.

A future engineer should be able to begin here and understand what the database is, why each object exists, how objects relate, which invariants PostgreSQL enforces, how current and historical state differ, what is canonical/provider/derived/technical, what migrations and mappings implement each object, and what tests prove the contract.

This document is deliberately not a migration script, ORM model dump or historical diary.

```text
Domain / Logical
→ semantic meaning

Physical Model
→ accepted PostgreSQL mapping thesis

CP6-02 Constitution / ADR-010
→ reusable PostgreSQL doctrine

THIS DOCUMENT
→ concrete DANTE database specification

Alembic + SQLAlchemy + PostgreSQL + tests
→ implementation and proof of this specification
```

At Gate 03 this document must be implementation-deterministic for every database fact that is actually derivable from closed authority.

---

## 2. Definition of “whole DANTE database”

`WHOLE DANTE DATABASE` means:

```text
maximum non-speculative persistence
that can be derived today
from closed DANTE authorities
```

It does **not** mean:

```text
every table DANTE might ever need
57 concepts mechanically becoming 57 tables
one table per future API or screen
placeholder columns for undecided product behavior
activation of dormant provider/runtime capabilities
```

A structure belongs in CP6 when the accepted model already determines that the database needs it and its meaning can be specified without inventing later application behavior.

If a fact is genuinely undecidable from closed authority, it is recorded explicitly with:

```text
exact unresolved parameter
why current authority cannot decide it
why a placeholder would be speculative
exact future stage / owner / trigger
```

“Vertical-specific” is not a valid excuse for deferring a database fact that is already determinable.

---

## 3. Authority chain and derivation discipline

Concrete database facts are derived through this chain:

```text
Domain concept / invariant
        ↓
Whole-Logical representation role
        ↓
CP6-01 persistence pressure
        ↓
accepted Physical PostgreSQL mapping
        ↓
CP6-02 Constitution
        ↓
concrete database object / column / constraint / test
```

No layer may silently redefine an earlier semantic layer for SQL or ORM convenience.

### 3.1 Required source families

At minimum this blueprint consumes:

```text
closed Domain Atlas + concept specifications
closed Whole-Logical 57/57 model
LR-01..LR-13 representation framework
WL-H01..WL-H12
CP6-01 Part 1 57/57 ledger
CP6-01 Part 2 cross-cutting/non-owner ledger
accepted PostgreSQL Physical mapping
PG-R01..PG-R10
Physical HG / SC / PSV evidence contracts
CP6-02 Constitution
ADR-010
CP3 real PostgreSQL/Alembic/SQLAlchemy foundation
```

### 3.2 Column rule

A column is not accepted because it is common in CRUD applications.

For example, none of the following is globally assumed merely by convention:

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

Each persisted field must have an exact semantic or bounded technical purpose.

### 3.3 Object naming status

Object names in the candidate catalog below are **design handles** until their object-level derivation is completed.

Gate 03 will freeze deterministic lower-case PostgreSQL names and the Database Dictionary will use those exact names.

A name becoming concrete does not make the corresponding semantic family more generic than its upstream model permits.

---

## 4. Existing PostgreSQL foundation — already materialized

CP6 inherits the CP3 technical persistence foundation rather than recreating it.

```text
PostgreSQL application schema        dante
SQLAlchemy                           2.0 stable
psycopg                              3
Alembic                              one environment / one DAG / one head
AsyncEngine                          one per process
async_sessionmaker                   one per process
AsyncSession                         one per application operation
autobegin                            False
autoflush                            True
expire_on_commit                     False
outer transaction owner              application operation
adapter commit                       forbidden implicitly
READ COMMITTED                       default isolation posture

dante_owner                          NOLOGIN
dante_migrator                       LOGIN NOINHERIT + bounded SET ROLE
dante_runtime                        LOGIN NOINHERIT / runtime DML posture
```

Current technical patch evidence is PostgreSQL 18.6. Physical/CP2/CP3 direct 18.4 evidence remains historical exact evidence and is never rewritten as 18.6 execution.

### 4.1 One physical PostgreSQL schema

The accepted CP3 application schema remains:

```text
dante
```

Earlier Physical documentation used conceptual labels such as `core`, `history`, `integration`, `projection` and `technical` to explain responsibility. CP6-03 does **not** turn those labels into separate PostgreSQL schemas unless a later explicit authority changes the CP3 decision.

Within schema `dante`, object names and documentation distinguish those persistence roles.

---

## 5. Global database topology

The concrete database is organized by semantic role, not by a universal supertype.

```text
DANTE PostgreSQL
│
├── native canonical owner families                 LR-01
│
├── contextual / dependent material families        LR-02 / LR-06
│
├── specific semantic relation families             LR-03
│
├── structured values                               LR-04
│
├── rule / policy / specification families          LR-05
│
├── material-state / history / lineage structures   LR-07
│
├── derived / query / projection structures         LR-08
│
├── provider / external integration structures      LR-09
│
├── bounded flexible metadata                       LR-10
│
├── candidate / unresolved structures               LR-11
│
├── product / organizational profile structures     LR-12
│
├── specialist extension structures                 LR-13
│
└── bounded technical control structures
    ├── heterogeneous reference addressing where proven
    ├── MaterialStateRef control
    ├── current-state control
    ├── idempotency where a real operation requires it
    └── other narrowly justified integrity/evolution machinery
```

Forbidden as global shortcuts:

```text
universal entity / thing table
universal relationship / edge table
canonical EAV / property bag
universal Rule(type,payload)
universal Fact / Version semantic root
universal event log as ontology
generic kind+uuid reference without database integrity
JSONB as required-semantic escape hatch
PostgreSQL inheritance as ontology
```

---

## 6. Identity topology

### 6.1 LR-01 native identity owners

Exactly 15 Domain concepts own native DANTE identity:

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

Each receives an owner-specific canonical relational family.

The native identity contract is:

```text
DANTE-owned stable identity
→ PostgreSQL native uuid
→ UUIDv7 policy
→ normally generated at backend application boundary
```

UUIDv7 ordering is a storage/locality property, never semantic chronology.

A native owner does not require a common semantic parent row.

### 6.2 Contextual roles that must NOT become native owners

```text
Actor
Subject
Resource
```

These are contextual roles/capabilities over eligible referents or representations.

Therefore:

```text
ActorRef    forbidden as universal wrapper
SubjectRef  forbidden as universal wrapper
ResourceRef forbidden as universal wrapper
```

The owning record/reference contract stores the actual eligible target.

### 6.3 Native owner table baseline

Every LR-01 owner table must eventually specify at minimum:

```text
native UUID primary key
exact identity semantics
whether/how heterogeneous NativeRef participation is represented
lifecycle continuity required for its identity
owner-specific canonical fields
owner-specific current/material-state behavior
owner-specific history behavior
```

No generic audit/lifecycle column set is assumed globally.

---

## 7. Reference topology

DANTE preserves four distinct reference contracts:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

They may all use SQL `uuid` somewhere in their physical representation; that does not make them interchangeable.

### 7.1 NativeRef

```text
homogeneous target contract
→ direct FK to concrete native-owner table

genuinely heterogeneous native target contract
→ bounded native-address control mechanism
```

A heterogeneous reference must preserve database-enforced:

```text
address existence
concrete owner existence
concrete owner family
consumer-slot family eligibility
lifecycle continuity where required
```

Application-only `type + uuid` is rejected.

#### Candidate shared family — `native_address`

**Status:** REQUIRED ONLY TO THE EXTENT ACTUAL HETEROGENEOUS NativeRef CONTRACTS REQUIRE IT; exact topology OPEN in CP6-03.

The accepted Physical/Constitution requires a bounded native-address mechanism where heterogeneous NativeRef exists, but CP6-03 must still enumerate every actual consumer contract before freezing:

```text
participating owner families
owner-family representation
1:1 owner binding
consumer eligibility enforcement
retirement/tombstone behavior
constraint-vs-trigger mechanism
```

The object must remain address infrastructure only. It must never accumulate generic domain properties.

### 7.2 ScopedRecordRef

Concrete LR-02 / qualified relation records receive a stable scoped address only when independent addressability/history/reconciliation justifies it.

```text
homogeneous scoped target
→ direct FK to concrete scoped family where possible

genuinely heterogeneous scoped target
→ separate bounded scoped-address mechanism MAY be required
```

Native, scoped and material address spaces must not collapse into one generic reference table.

#### Candidate shared family — `scoped_address`

**Status:** CONDITIONAL / NOT YET PROVEN NECESSARY AS A SHARED TABLE.

CP6-03 must first identify a real heterogeneous ScopedRecordRef consumer. If none exists, no shared scoped-address table will be created merely for symmetry.

### 7.3 MaterialStateRef

Material semantic states use stable explicit addresses independent from PostgreSQL MVCC tokens, hashes, provider revisions or timestamps.

A bounded material-state address/control family is **required**.

Conceptual contract:

```text
MaterialStateRef UUID
+
exact semantic owner address
+
exact material facet/purpose
+
owner-specific state payload row
+
explicit current accepted-state binding where required
```

#### Required shared family — `material_state_address`

**Status:** REQUIRED FAMILY / EXACT COLUMNS AND OWNER-ADDRESS TOPOLOGY TO BE CLOSED IN CP6-03.

It is a technical control structure, not a semantic Fact/Version table.

It must be possible for PostgreSQL to reject:

```text
missing state address
state address with no matching owner-specific state row
wrong owner
wrong facet
invalid current-state binding
```

### 7.4 ExternalRef

External identity is issuer/provider scoped.

Physical representation must be able to preserve as applicable:

```text
provider/source
realm / tenant / external account / integration instance
external object type where material
opaque external identifier
provider revision/version where material
```

No generic provider table is materialized until a real integration contract determines those semantics.

---

## 8. Material state, current truth and history topology

### 8.1 Baseline pattern

For every concept/facet that crosses the materiality threshold:

```text
stable semantic owner/contextual record
        ↓
owner-specific immutable-by-policy material-state rows
        ↓
MaterialStateRef control/address
        ↓
explicit current accepted-state binding
        ↓
typed correction/replacement/reconciliation lineage
```

Current truth is not inferred from:

```text
MAX(revision)
MAX(created_at)
latest UUIDv7
latest provider version
latest insertion order
```

### 8.2 Owner-specific semantic payload

Material-state payload remains owner/facet specific.

Examples of eventual families may include concept-specific state tables such as an Activity state, Agreement terms state, Schedule placement state or governance state, but exact table names and fields are accepted only after the corresponding Domain concept derivation.

There is no universal semantic state payload table.

### 8.3 Current-state control

A concrete current-state mechanism is required wherever the accepted model needs a current material state.

**Open topology question:** whether the final implementation uses narrowly shared technical current-binding control plus owner-specific constraints, owner-specific current-binding tables/columns, or a bounded hybrid.

Whatever mechanism is selected must enforce:

```text
current state exists
current state belongs to same owner
current state belongs to same facet
current state is a valid accepted state
```

### 8.4 Lineage

Correction, replacement and reconciliation must preserve typed meaning.

The database must not invent one universal `state_edge(type, from, to)` graph merely because it is convenient.

CP6-03 must decide which lineage relationships can be represented by bounded technical control and which must remain owner-specific semantic relationships.

### 8.5 Chronology

DANTE distinguishes where material:

```text
world/effective chronology
recorded/learned/accepted chronology
```

No blanket bitemporal schema is required.

Each concrete family must specify whether it needs:

```text
date
local wall-clock
IANA zone
absolute timestamptz instant
range / multirange
duration
precision/granularity
world/effective interval
recorded/accepted instant/interval
```

---

## 9. Relation topology

No universal Relationship table exists.

### 9.1 Simple specific relation

When a binary relationship is fully represented by its endpoints and specific semantics:

```text
specific relation table
+ concrete endpoint FKs where homogeneous
+ exact uniqueness/cardinality constraints
```

### 9.2 Qualified/material relation

When a relationship has material lifecycle/history/governance/provenance/context:

```text
specific contextual relation record
+ stable ScopedRecordRef where justified
+ exact semantic endpoint roles
+ MaterialStateRef/history where material
+ governance/provenance bindings where required
```

### 9.3 True n-ary relation

Naturally n-ary semantics remain n-ary.

Agreement is the canonical high-pressure example:

```text
Agreement contextual record
+ one exact material terms state per accepted terms state
+ N party-role assent records
+ assent bound to that exact terms MaterialStateRef
```

Amendment creates a new material terms state; old assent cannot silently transfer to the new terms state.

---

## 10. Missingness and lifecycle rules

Across the database:

```text
absence != explicit negative
unknown != false
not observed != proved absent
no response != declined
provider missing != canonical deletion
redacted/unavailable != never existed
```

No sentinel values are used to simulate these distinctions.

No global `deleted_at` / `is_deleted` convention is assumed.

Foreign-key lifecycle default:

```text
ON DELETE NO ACTION
```

`CASCADE` or `SET NULL` require concept-specific proof.

Stable identity is not reused after retirement/tombstone.

---

## 11. PostgreSQL type doctrine carried into the blueprint

Concrete field derivation follows these defaults:

```text
DANTE stable identity              uuid
absolute instant                   timestamptz
local civil date                   date
local wall-clock                   time / structured local representation as required
named zone                         IANA zone identifier + applicable civil/instant basis
interval semantics                 PostgreSQL ranges/multiranges where exact
currency                           explicit ISO currency semantics
PostgreSQL money                   forbidden
required semantic structure        typed columns/relations over generic JSONB
bounded low-consequence metadata   JSONB allowed only when explicitly justified
provider/raw payload               bounded JSONB allowed where integration contract needs it
```

Exact numeric precision, geometry shape/SRID, recurrence parameters and other domain-specific types are not guessed; they are closed during object-level derivation.

---

## 12. Constraint and index doctrine

### 12.1 Constraint-first

Prefer declarative PostgreSQL integrity in this progression:

```text
NOT NULL / FK / UNIQUE / CHECK
→ range / EXCLUDE / DEFERRABLE constraints where truthful
→ bounded trigger/function integrity only when declarative SQL cannot express the invariant
→ application validation as additional semantic layer, not substitute for enforceable DB truth
```

### 12.2 Foreign keys

Every FK must document:

```text
semantic reason
target family
cardinality
on-delete behavior
on-update behavior
whether deferrable
whether the referencing side needs an index
```

### 12.3 Indexes

Indexes are created because a structural or demonstrated query requirement exists.

Required review includes:

```text
PK/UNIQUE already-backed indexes
referencing FK lookup/index pressure
range/exclusion support
temporal query pressure
actual FTS/trgm/vector use
```

Forbidden:

```text
index every foreign key blindly
index every timestamp
duplicate PK/UNIQUE indexes
speculative GIN/GiST/vector indexes
speculative partitioning/sharding
```

---

## 13. Transaction and concurrency contract

CP6 database design preserves the CP3/CP6-02 transaction model:

```text
outer application operation owns transaction
adapter may flush
adapter does not implicitly commit
READ COMMITTED default
```

Invariant enforcement escalates only when needed:

```text
declarative invariant
→ expected-state / conditional update
→ deterministic row/key locking
→ SERIALIZABLE for real predicate/write-skew semantics
```

A material stale-write-sensitive mutation uses expected `MaterialStateRef` or an explicitly equivalent semantic precondition.

No external provider effect is described as atomically rolled back with PostgreSQL.

---

## 14. Candidate relational family inventory

This inventory is the first CP6-03 concrete map. `REQUIRED` means the closed model requires a concrete family. `CONDITIONAL` means the semantic family exists but an independent persistent table/state is created only when the material/addressability threshold is met. `NO ROOT` means the concept is represented through another concrete family rather than receiving an independent generic table.

### 14.1 Native canonical owner families — LR-01

| Domain concept | Candidate canonical owner object | Status | Material/history pressure |
|---|---|---|---|
| Person | `person` | REQUIRED | conditional owner-specific material state/history |
| Living Referent | `living_referent` | REQUIRED | conditional owner-specific material state/history |
| Asset | `asset` | REQUIRED | conditional owner-specific material state/history |
| Place | `place` | REQUIRED | conditional material address/geometry history; PostGIS shape unresolved |
| Content Artifact | `content_artifact` | REQUIRED | material content-state/history when exact revision matters |
| Collective | `collective` | REQUIRED | identity independent from membership; governance/state history conditional |
| Possibility | `possibility` | REQUIRED once retained as canonical | candidate state before acceptance remains noncanonical |
| Goal | `goal` | REQUIRED | material lifecycle/history when consequential |
| Plan | `plan` | REQUIRED | exact material plan history when later meaning depends on revision |
| Activity | `activity` | REQUIRED | material state/history when consequential |
| Event | `event` | REQUIRED | material state/history conditional |
| Routine | `routine` | REQUIRED | governing material state/history when Occurrences depend on exact state |
| Occurrence | `occurrence` | REQUIRED once individually distinguished | lazy pre-materialization locator remains separate from native identity |
| Session | `session` | REQUIRED | correction/split/merge history conditional |
| Observation | `observation` | REQUIRED | material correction/history required for material observations |

No table above inherits from a common semantic Entity table.

### 14.2 Contextual / realization / result families — LR-02 / LR-06

| Concept | Candidate family | Status | Key rule |
|---|---|---|---|
| Actual | `actual` contextual realization family | CONDITIONAL/REQUIRED for canonical material Actual | never overwrites Schedule; absence != negative |
| Agreement | `agreement` + terms/state + party-assent structures | REQUIRED | n-ary common terms MaterialStateRef |
| Decision | `decision` contextual family | CONDITIONAL | only when independent lifecycle/history matters |
| Evaluation | derived evaluation by default; material `evaluation` snapshot when consequential | CONDITIONAL | source/material basis preserved |
| Milestone | dependent `milestone` family | REQUIRED as accepted dependent concept | attainment basis historical when material |
| Outcome | `outcome` result/disposition family | CONDITIONAL | absence distinct from negative result |
| Proposal | `proposal` contextual family | CONDITIONAL | exact target state when consequential |
| Reconciliation | `reconciliation` material resolution family | CONDITIONAL→REQUIRED for material resolution | competing states/sources + resolution retained |
| Request | `request` contextual family | CONDITIONAL | Request != effect/Authority/idempotency key |
| Resource Requirement | structured requirement + contextual address where justified | CONDITIONAL | specification semantics remain distinct from Allocation |
| Schedule | `schedule` dependent placement family | REQUIRED when accepted placement is persisted | distinct from Occurrence/Session/Actual/Capacity Claim |

### 14.3 Specific relation families — LR-03

| Concept | Candidate relation family | Status | Non-collapse rule |
|---|---|---|---|
| Acknowledgement | `acknowledgement` attestation relation | CONDITIONAL persistent qualification | target exact MaterialStateRef when consequential |
| Authority | authority grant/state relation family | REQUIRED when canonical governance state exists | Authority != AuthZ runtime decision |
| Confirmation | `confirmation` attestation relation | CONDITIONAL persistent qualification | target state binding when consequential |
| Consent | consent governance relation/state family | REQUIRED for consequential consent state | grant/withdrawal history material |
| Contribution | `contribution` relation | REQUIRED where contribution is canonical | attribution history when material |
| Coordination Stewardship | `coordination_stewardship` relation | REQUIRED when canonical | distinct from Responsibility/Authority |
| Dependency | `dependency` directional contingency relation | REQUIRED where canonical | no universal DAG edge |
| Evidence | `evidence_use` / specific evaluative-use relation | REQUIRED where Evidence use is canonical | Evidence != source truth / Provenance |
| Interpersonal Relationship | bounded person-to-person relation family | REQUIRED | no generic relationship root |
| Membership | `membership` relation | REQUIRED | member set does not define Collective identity |
| Ownership | `ownership` relation | REQUIRED | distinct from Possession/Authority |
| Participation | `participation` relation family | REQUIRED | intended/response != Actual participation |
| Possession | `possession` relation | REQUIRED | distinct from Ownership/Allocation |
| Representation | representation/on-behalf-of governance relation | REQUIRED where canonical | represented party != Actor/Principal |
| Resource Allocation | allocation relation/contextual family | REQUIRED where canonical | Schedule != claim != allocation != actual use |
| Responsibility | `responsibility` relation | REQUIRED | requester/performer/steward/Authority remain distinct |
| Visibility | visibility/disclosure governance relation/state family | REQUIRED when canonical | effective projection remains separate LR-08 |

Exact endpoint tables/cardinalities/qualification fields are closed concept-by-concept before Gate 03.

### 14.4 Rule / policy / specification families — LR-05

| Concept | Candidate structured family | Status | Rule |
|---|---|---|---|
| Availability | baseline/rule + material override family | REQUIRED where accepted rules/overrides exist | effective availability remains derived |
| Conditional Policy | typed policy/specification family | REQUIRED where accepted | no universal Rule(type,payload) |
| Criterion | structured criterion family | REQUIRED where accepted | exact state retained for consequential Evaluation basis |
| Recurrence | structured recurrence family | REQUIRED | canonical model not reduced to provider/RRULE format |
| Resource Requirement | structured requirement specification | REQUIRED where accepted | contextual address only where justified |
| Temporal Constraint | structured temporal constraint family | REQUIRED | distinct from Schedule |

### 14.5 Value semantics — LR-04

| Concept | Persistence disposition |
|---|---|
| Monetary Amount | NO independent identity/root; owner-bound typed amount + explicit currency semantics |
| Quantity | NO independent identity/root by default; owner-bound typed magnitude/unit representation |
| Capacity | NO universal Capacity owner; typed value/rule/contextual representation as accepted consumer requires |

The object-level pass will determine whether repeated value shapes merit SQLAlchemy composites or bounded dependent tables without inventing semantic identity.

### 14.6 Cross-cutting history / projection / integration families

| Logical role | Candidate persistence family | Status |
|---|---|---|
| LR-07 material history | owner-specific material-state rows + bounded MaterialStateRef control + typed lineage | REQUIRED where material |
| LR-08 derived/effective | view/materialized/cache/query structures | CONDITIONAL / only for real derived/query need |
| LR-09 provider/external | provider mapping/revision/apply/sync/reconciliation structures | GENUINELY DEFERRED until concrete integration contract unless a closed concept requires a provider-neutral field now |
| LR-10 flexible metadata | owner-bound bounded JSONB/typed metadata | CONDITIONAL / never a global property bag |
| LR-11 candidate/unresolved | candidate structures | GENUINELY DEFERRED until a concrete accepted producer/consumer needs persistence |
| LR-12 profile | product/organizational profile structures | GENUINELY DEFERRED until product profile semantics are closed |
| LR-13 specialist extension | specialist-specific structures | GENUINELY DEFERRED until specialist trigger exists |

---

## 15. 57/57 Domain persistence traceability — initial CP6-03 matrix

This table ensures every Domain concept reaches a concrete database disposition. It is an initial blueprint matrix, not yet the Gate-03 final column-level contract.

| # | Concept | Logical role | Initial CP6-03 database disposition |
|---:|---|---|---|
| 01 | Acknowledgement | LR-03 | specific attestation relation; persistent qualification only where material/addressable |
| 02 | Activity | LR-01 | required native canonical owner family; state/history derived next |
| 03 | Actor | contextual role | NO ROOT; actual eligible referent carried by owning operation/provenance/relation |
| 04 | Actual | LR-06/LR-02 | specific realization family for material canonical Actual |
| 05 | Agreement | LR-02 + n-ary relation | required contextual Agreement + terms MaterialState + party assent topology |
| 06 | Asset | LR-01 | required native canonical owner family |
| 07 | Authority | LR-03/LR-02/LR-05/LR-08 | governance relation/state + basis + derived effective view; no generic ACL truth |
| 08 | Availability | LR-05/LR-02/LR-08 | structured rule/override; effective state derived |
| 09 | Capacity | LR-04/LR-05/LR-02/LR-08 | NO native root; typed capacity/rule/material context as consumer requires |
| 10 | Collective | LR-01 | required native canonical owner family independent of member set |
| 11 | Conditional Policy | LR-05 | structured policy/specification family |
| 12 | Confirmation | LR-03 | specific attestation relation; material qualification conditional |
| 13 | Consent | LR-03/LR-02 | specific governance relation/state with material history when consequential |
| 14 | Content Artifact | LR-01 | required native canonical owner; byte storage remains separate bounded capability |
| 15 | Contribution | LR-03 | specific contribution/attribution relation |
| 16 | Coordination Stewardship | LR-03 | specific stewardship relation |
| 17 | Criterion | LR-05 | structured criterion/specification family |
| 18 | Evaluation | LR-08 / LR-02 | derived by default; material snapshot only when consequential |
| 19 | Decision | LR-02 | conditional independent decision record when lifecycle/history matters |
| 20 | Dependency | LR-03 | specific directional contingency relation |
| 21 | Event | LR-01 | required native canonical owner family |
| 22 | Evidence | LR-03 | typed source→evaluation/context use relation; exact source state when required |
| 23 | Goal | LR-01 | required native canonical owner family |
| 24 | Interpersonal Relationship | LR-03 | bounded Person-to-Person specific relation family |
| 25 | Living Referent | LR-01 | required native canonical owner family distinct from Person/Asset |
| 26 | Membership | LR-03 | specific membership relation; Collective identity remains independent |
| 27 | Milestone | LR-02 | dependent milestone family; material address/history where justified |
| 28 | Monetary Amount | LR-04 | NO ROOT; typed owner-bound amount/currency value |
| 29 | Observation | LR-01 | required native canonical owner + material correction/history when material |
| 30 | Occurrence | LR-01 when distinguished | native owner once persisted; lazy locator before differentiation |
| 31 | Outcome | LR-06/LR-02 | specific result/disposition family when materially persistent |
| 32 | Ownership | LR-03 | specific ownership relation |
| 33 | Participation | LR-03 | specific intended/response/actual participation relation semantics |
| 34 | Person | LR-01 | required native canonical owner; separate from Account/Principal |
| 35 | Place | LR-01 | required native owner; geo representation closed in object-level pass |
| 36 | Plan | LR-01 | required native owner; material plan-state history when revision matters |
| 37 | Possession | LR-03 | specific possession/custody relation |
| 38 | Possibility | LR-01 once canonical | required native owner after acceptance; pre-acceptance candidates noncanonical |
| 39 | Proposal | LR-02 | conditional proposal record; target exact state when consequential |
| 40 | Provenance | LR-07 | bounded typed lineage/provenance attached to concrete effects/states; NO universal graph root |
| 41 | Quantity | LR-04 | NO ROOT; typed owner-bound magnitude/unit value |
| 42 | Reconciliation | LR-02/LR-07 | material reconciliation record where resolution/history matters |
| 43 | Recurrence | LR-05 | structured recurrence specification; exact families/parameters derived next |
| 44 | Representation | LR-03/LR-02 | specific on-behalf-of governance relation/state |
| 45 | Request | LR-02 | conditional directed request record; distinct from effect/idempotency identity |
| 46 | Resource Allocation | LR-03/LR-02 | specific allocation relation/contextual record when material |
| 47 | Resource Requirement | LR-05/LR-02 | structured requirement; scoped record where materially addressable |
| 48 | Resource | contextual role | NO ROOT; eligible concrete provider/value/service/pool/specialist target |
| 49 | Responsibility | LR-03 | specific responsibility relation family |
| 50 | Routine | LR-01 | required native owner + governing material state/history for dependent Occurrences |
| 51 | Schedule | LR-02 | dependent accepted-placement family; material/scoped when consequential |
| 52 | Session | LR-01 | required native execution-episode owner family |
| 53 | Subject | contextual role | NO ROOT; eligible ReferenceAddress target through owning contract |
| 54 | Temporal Constraint | LR-05 | structured temporal constraint family distinct from Schedule |
| 55 | Verification | Evaluation purpose/profile | NO ROOT; represented through applicable Evaluation form |
| 56 | Version | LR-07 | NO universal Version root; represented by material-state/history machinery |
| 57 | Visibility | LR-03/LR-02/LR-05/LR-08 | disclosure governance state/policy + separate derived effective surface |

```text
57 / 57 concepts accounted in initial blueprint     PASS
Gate-03 exact table/column contract                  NOT YET PASS
```

---

## 16. CP6-01 Part-2 cross-cutting/non-owner disposition — initial matrix

Gate 03 requires 100% accounting beyond the 57 Domain concepts. This initial matrix uses the final allowed disposition vocabulary but remains subject to object-level proof before Gate 03.

| Construct | Initial disposition | Current CP6-03 reasoning / exact trigger |
|---|---|---|
| ReferenceAddress | NO INDEPENDENT PERSISTENCE as universal root | represented by the four discriminated address contracts and concrete bounded mechanisms |
| Reference Contract | NO INDEPENDENT PERSISTENCE | enforced through concrete FK/anchor eligibility constraints per consuming slot |
| NativeRef | MATERIALIZE IN CP6 | native owner UUIDs + direct FKs; bounded native-address control where real heterogeneous contracts prove need |
| ScopedRecordRef | MATERIALIZE IN CP6 where concrete scoped families require stable address | no shared scoped anchor unless heterogeneous scoped consumer is proven |
| MaterialStateRef | MATERIALIZE IN CP6 | required bounded material-state address/control family + owner-specific state rows |
| ExternalRef | GENUINELY DEFERRED for generic/shared provider structures | trigger = first concrete integration/provider contract; no provider ontology invented now |
| Current accepted-state binding | MATERIALIZE IN CP6 where material state exists | exact shared-vs-owner-specific topology must enforce same owner/facet |
| Correction/replacement/reconciliation lineage | MATERIALIZE IN CP6 where material history exists | typed lineage; no universal event/state graph |
| World/effective chronology | MATERIALIZE IN CP6 per family where material | exact type/range determined by concept chronology |
| Recorded/learned/accepted chronology | MATERIALIZE IN CP6 per family where material | separate from world chronology only when needed |
| Governed Operation / Effect Contract | NO INDEPENDENT PERSISTENCE as universal operation owner | operation-specific persistence/provenance fields when a concrete consequential effect exists |
| Governed Operation Request | GENUINELY DEFERRED | trigger = first post-CP6 application operation whose audit/recovery semantics require persistent request state |
| Execution receipt/result | GENUINELY DEFERRED | trigger = first runtime/provider operation requiring durable execution receipt; never automatically Actual/Outcome |
| Idempotency record | GENUINELY DEFERRED as a generic table | trigger = first persistent material operation needing retry/replay protection; Constitution then mandates exact reservation semantics |
| Correlation/causation references | NO INDEPENDENT PERSISTENCE by default | bounded fields/relations on concrete provenance/runtime/provider records when those exist |
| Projection / Disclosure Surface Contract | NO INDEPENDENT PERSISTENCE as universal root | concrete derived structures/views only when a real projection is materialized |
| Provider/sync/apply state | GENUINELY DEFERRED | trigger = concrete integration/sync consumer |
| Flexible low-consequence metadata | NO INDEPENDENT PERSISTENCE | bounded owner-local JSONB/typed fields only where concept authority permits |
| Candidate/unresolved interpretation | GENUINELY DEFERRED | trigger = first accepted candidate-producing capability requiring persistence |
| Product/organizational profile | GENUINELY DEFERRED | trigger = closed product profile semantics / real product consumer |
| Specialist extension | GENUINELY DEFERRED | trigger = selected specialist capability with concrete schema requirement |
| Account | GENUINELY DEFERRED | Domain explicitly keeps Account separate and detailed access model deferred; no speculative login/account table in CP6 |
| Principal/security context | GENUINELY DEFERRED as independent registry | trigger = closed AuthN/AuthZ security context; provenance must remain able to bind a later Principal without redefining Actor/Person |
| Actor role | NO INDEPENDENT PERSISTENCE | owning record stores concrete eligible referent/address; no ActorRef |
| Subject role | NO INDEPENDENT PERSISTENCE | owning Reference Contract stores eligible target; no SubjectRef |
| Resource role | NO INDEPENDENT PERSISTENCE | concrete eligible provider/value/service/pool/specialist representation; no ResourceRef |
| Capacity Claim pressure | OPEN DERIVATION — expected contextual/material representation | exact accepted capacity-claim semantics must be traced from closed time/resource authorities before final disposition |
| Tombstone/retirement/redaction continuity | MATERIALIZE IN CP6 where owner lifecycle requires it | owner-specific/minimal continuity; NO generic semantic Tombstone owner |
| Anti-resurrection reconciliation | GENUINELY DEFERRED as executable recovery mechanism | trigger = destructive recovery/restore stage; schema must not make later enforcement impossible |
| Transactional outbox | GENUINELY DEFERRED | trigger = first real Class-A async external effect; not Domain history/event store |
| PowerSync/encrypted SQLite | GENUINELY DEFERRED | trigger = offline/mobile activation; PostgreSQL remains canonical |
| Search/vector indexes/caches | GENUINELY DEFERRED except concrete indexes justified by the database model | trigger = real search/vector/query consumer; no speculative pgvector/GIN materialization |

The single remaining `OPEN DERIVATION` entry above is deliberately visible. Gate 03 cannot pass while any cross-cutting construct remains unclassified.

---

## 17. Candidate implementation / materialization dependency DAG

The exact Alembic revision batches are frozen only after table/column derivation, but the structural dependency order is already constrained.

```text
0. CP3 TECHNICAL FOUNDATION — ALREADY REAL
   schema dante
   roles / grants
   Alembic base
   SQLAlchemy MetaData/Base
        ↓
1. CORE IDENTITY OBJECTS
   15 LR-01 canonical owner tables
   + bounded native-address control if concrete hetero NativeRef contracts require it
        ↓
2. MATERIAL-STATE CONTROL FOUNDATION
   MaterialStateRef address/control
   + exact owner/facet binding mechanism
   + current-state control mechanism
        ↓
3. OWNER-SPECIFIC MATERIAL STATE / HISTORY
   state rows
   chronology
   correction/replacement/reconciliation lineage
        ↓
4. DEPENDENT / CONTEXTUAL FAMILIES
   Agreement / Schedule / Milestone / Actual / Proposal / Decision / Request / etc.
        ↓
5. SPECIFIC RELATION FAMILIES
   Membership / Responsibility / Participation / Ownership / Consent / Authority / Visibility / etc.
        ↓
6. RULE / POLICY / SPECIFICATION FAMILIES
   Recurrence / Temporal Constraint / Criterion / Availability / Conditional Policy / Resource Requirement
        ↓
7. RESULT / GOVERNANCE / PROVENANCE COMPLETION
   Outcome / material Evaluation / reconciliation / exact provenance bindings
        ↓
8. PROVIDER / DERIVED / SPECIALIST STRUCTURES
   only where closed authority and real trigger justify materialization
        ↓
9. DOCUMENTATION + INTROSPECTION QA
   dictionary / generated reference / diagrams / schema drift / direct tests
```

This is a dependency DAG, not a product roadmap. Specific families can move earlier/later when their FK/material-state dependencies prove it.

### 17.1 Cyclic-integrity caution

Heterogeneous native-address integrity may require a staged migration shape because the address controller and concrete owner tables can depend on one another conceptually.

CP6-03 must select a PostgreSQL-enforceable design that preserves:

```text
anchor exists
concrete owner exists
owner family matches
one owner binding only
consumer contract eligibility
```

without making the anchor a semantic superclass.

The migration plan may therefore need:

```text
create control table
→ create concrete owner tables / bindings
→ install bounded constraint/trigger enforcement
→ verify wrong-family/dangling rejection
```

This is not permission for application-only integrity.

---

## 18. SQLAlchemy mapping plan — initial

The existing canonical SQLAlchemy `Base.metadata` remains the single application metadata authority for DANTE-owned PostgreSQL objects.

CP6-04 mappings will follow these rules:

```text
one shared Base / MetaData
schema = dante
one mapped class per actual row-shaped persistence object where ORM mapping is useful
no generic Repository[T]
no generic semantic Entity mapped superclass
no polymorphic semantic root merely to share columns
no implicit create_all deployment
Alembic remains deployed-schema authority
```

Reusable Python mixins/types are allowed only for technical repetition that does not imply semantic inheritance.

Each final Database Dictionary entry will point to its SQLAlchemy mapping when one exists.

Views/generated/projection objects do not require ORM classes merely for symmetry.

---

## 19. Direct PostgreSQL proof plan — initial

CP6-03 must end with an exact test matrix. Current required categories include:

### 19.1 Foundation / schema alignment

```text
fresh database → Alembic head
single canonical Alembic head
SQLAlchemy metadata vs Alembic/PostgreSQL drift
role ownership/grants
runtime DDL denial
Database Dictionary object coverage
```

### 19.2 Identity/reference

```text
native UUID round-trip
UUIDv7 generation/storage
homogeneous FK integrity
heterogeneous native reference: valid target PASS
heterogeneous native reference: wrong family REJECT
heterogeneous native reference: dangling target REJECT
anchor leakage / forbidden generic payload REJECT by design/schema
```

Maps especially to PG-R01 / PG-R02.

### 19.3 Material state/history

```text
MaterialStateRef exists exactly once
state row belongs to correct owner/facet
missing state row rejected
wrong owner rejected
wrong facet rejected
current binding points to valid same-owner/same-facet accepted state
correction creates new state rather than silent overwrite
historical state remains reconstructible
```

Maps especially to PG-R03 / PG-R07 and WL-H05.

### 19.4 Relations/governance

```text
endpoint/cardinality constraints
Agreement common terms-state binding
amendment does not silently inherit assent
Consent/Authority/Visibility history where material
Representation preserves Actor vs represented party
Membership does not redefine Collective identity
Ownership != Possession constraints/structures remain separate
```

Maps especially to PG-R06 and WL-H01/WL-H11.

### 19.5 Temporal/Occurrence

```text
world vs recorded chronology where material
range/exclusion constraints where applicable
lazy occurrence locator → persisted Occurrence continuity
unordered quota slots do not gain fake ordinal identity
```

Maps especially to PG-R07 / PG-R08.

### 19.6 Missingness/lifecycle

```text
absence does not encode universal false
explicit negative states remain distinguishable
NO ACTION lifecycle defaults hold
retired/tombstoned stable identity not reused
redacted/unavailable does not become never-existed
```

### 19.7 Concurrency

When a concrete subject exists:

```text
stale expected MaterialStateRef conflicts
valid expected state succeeds
multi-owner invariant survives concurrent writes
whole transaction rolls back atomically on local invariant failure
```

Maps to PG-R04 / PG-R05.

### 19.8 Derived/provider boundaries

Only after a concrete subject exists:

```text
provider state cannot silently become canonical
material derived state retains/revalidates basis
hidden state does not leak through query/search surfaces
```

SC-017 / SC-018 remain canonical scenario identifiers where applicable.

---

## 20. Database Dictionary plan

The machine-readable dictionary defined by `docs/database/README.md` will be instantiated only once concrete objects reach stable names/fields during CP6-03.

Every materialized table will eventually have a structured entry accounting for, as applicable:

```text
object identity / role
semantic source
columns/types/nullability/defaults
PK/FK/cardinality/delete behavior
UNIQUE/CHECK/EXCLUDE/trigger invariants
indexes + reason
MaterialState/current/history behavior
lifecycle/retention/tombstone
privileges
migration traceability
SQLAlchemy mapping
proof/test IDs
known staged evidence
```

A future structural migration that changes an object without updating its dictionary entry is incomplete.

Generated schema/ER material must be derived from SQLAlchemy/PostgreSQL where practical and must not become a competing manual authority.

---

## 21. CP6-03 unresolved-parameter register

These are design questions that remain after the first whole-database inventory. They are not generic “TBD” placeholders: each exists because the authority chain must still be traced to a concrete decision.

| ID | Unresolved parameter | Why not guessed now | Closure requirement |
|---|---|---|---|
| DB-U01 | exact `native_address` relational topology and participating owner families | bounded heterogeneous integrity is required, but every concrete consuming Reference Contract must be enumerated first | prove owner existence/family/eligibility with PostgreSQL and no semantic-root leakage |
| DB-U02 | whether a shared `scoped_address` table is needed | Physical says MAY only for genuine heterogeneous scoped addressing | identify at least one real heterogeneous ScopedRecordRef consumer or reject shared table |
| DB-U03 | MaterialStateRef owner-address encoding across native/scoped owners | must preserve exact owner/facet without universal semantic root | select bounded referentially enforced topology |
| DB-U04 | material facet representation | generic text/enum/lookup choice cannot be made before actual facet sets are enumerated | enumerate facets and select typed bounded representation |
| DB-U05 | current accepted-state binding topology | shared control vs owner-specific binding must preserve same-owner/same-facet integrity | produce enforceable relational design + negative tests |
| DB-U06 | correction/replacement/reconciliation lineage topology | must not become a universal semantic history graph | classify lineage relationships into bounded technical vs owner-specific semantic forms |
| DB-U07 | exact chronology columns/ranges per family | no blanket bitemporality or universal created_at semantics | derive temporal needs from each Domain concept |
| DB-U08 | final PostgreSQL object naming convention | names must follow actual family shapes and remain readable/stable | freeze deterministic naming before dictionary generation |
| DB-U09 | Account persistence | Domain keeps Account separate but detailed access model is deferred | remain genuinely deferred unless another closed authority determines enough schema |
| DB-U10 | Principal/security persistence | AuthN/AuthZ context not yet closed as independent registry | preserve separation and defer independent registry until security contract |
| DB-U11 | Place geometry type/SRID/indexes | PostGIS selected, but exact geometry semantics must come from Place authority | derive exact geometry/address facets; no speculative spatial schema |
| DB-U12 | Recurrence family parameter tables/columns | recurrence families are known; exact lossless structured parameters require concept-level derivation | close each accepted family representation |
| DB-U13 | Monetary Amount / Quantity exact numeric precision/unit representation | semantic value families exist but storage precision cannot be guessed globally | derive accepted precision/range/unit requirements |
| DB-U14 | owner-specific lifecycle/tombstone fields | no global deleted_at/tombstone table | derive permitted lifecycle continuity per owner/family |
| DB-U15 | structural FK indexes and query indexes | index doctrine is closed but actual FK/query graph is not yet final | justify every index against structure/query proof |
| DB-U16 | Capacity Claim disposition | persistence pressure exists outside 57 but exact concrete family must be traced | resolve to MATERIALIZE / NO INDEPENDENT / GENUINELY DEFERRED with exact owner |
| DB-U17 | provider/integration object shapes | no concrete provider contract is active | remain deferred unless closed Domain data requires provider-neutral persistence now |
| DB-U18 | idempotency table timing | persistent semantics are closed but no qualifying product operation exists yet | materialize only at first real operation requiring persistent reservation |
| DB-U19 | transactional outbox timing | selected Class-A mechanism but no real Class-A operation exists | defer until real async external effect trigger |
| DB-U20 | derived/search/vector persisted structures | selected capabilities do not imply activation | create only from real query/search requirement and test basis |

```text
UNRESOLVED PARAMETERS AT CP6-03 OPEN
20

UNCLASSIFIED PARAMETERS ALLOWED AT GATE 03
0
```

---

## 22. Next derivation pass — object-level contract

The next CP6-03 work does not create another methodology document.

It expands this specification through a repeatable object-level derivation pass.

For each required/conditional family:

```text
1. read complete Domain concept specification / canonical continuations
2. read Whole-Logical disposition + WL-H pressure
3. read CP6-01 ledger entry
4. apply Physical mapping + Constitution
5. define exact table(s)
6. define exact columns and PostgreSQL types
7. define PK/FK/reference contracts
8. define NULL/missingness semantics
9. define UNIQUE/CHECK/EXCLUDE/trigger integrity
10. define material-state/current/history behavior
11. define lifecycle/delete behavior
12. justify structural indexes
13. define SQLAlchemy mapping shape
14. define migration dependencies
15. define direct PostgreSQL tests
16. create/update Database Dictionary entry
17. close or update every affected DB-U item
```

No object is called complete before this chain is satisfied.

---

## 23. Gate 03 acceptance contract

CP6-03 cannot close until all of the following are true:

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
Database System-of-Record structure for approved objects       PASS
unclassified cross-cutting persistence construct              0
unclassified database family                                  0
unresolved DB-U item                                           0
accidental new Domain owner                                    0
generic Entity/Relationship/EAV shortcut                       0
speculative placeholder schema                                 0
application Vertical #1 implementation                         0
```

Current result:

```text
CP6-03
ACTIVE

WHOLE DATABASE INVENTORY
OPENED

57/57 INITIAL TRACEABILITY
COMPLETE

PART-2 INITIAL DISPOSITION
OPEN / ONE EXPLICIT OPEN DERIVATION (Capacity Claim)

EXACT TABLE/COLUMN/CONSTRAINT BLUEPRINT
IN PROGRESS

GATE 03
NOT YET EARNED
```

No business migration, SQLAlchemy business mapping, persistence adapter, API or product vertical is authorized merely by this candidate blueprint.
