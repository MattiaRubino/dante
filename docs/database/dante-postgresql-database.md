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

### 7.1 NativeRef — bounded heterogeneous address topology CLOSED

```text
homogeneous target contract
→ direct FK to concrete native-owner table

genuinely heterogeneous native target contract
→ bounded dante.native_address control row
```

`native_address` exists only as technical address/control infrastructure. It is **not** a mandatory semantic parent row for every native owner and it is not an Entity/Thing table. A row is created when an existing native owner needs to participate in a heterogeneous NativeRef contract or another accepted technical mechanism, such as MaterialState owner addressing, requires the bounded address.

#### Concrete control table — `dante.native_address`

```text
native_ref     uuid  PRIMARY KEY
owner_family   text  NOT NULL
```

`native_ref` is the same stable UUIDv7 identity already owned by the concrete LR-01 owner. The address row does not mint a second semantic identity.

`owner_family` is a bounded technical discriminator. The accepted family vocabulary is exactly the 15 LR-01 native-owner families:

```text
person
living_referent
asset
place
content_artifact
collective
possibility
goal
plan
activity
event
routine
occurrence
session
observation
```

The implementation MUST reject any other `owner_family`. The concrete migration may express the closed set as deterministic `text + CHECK`; a PostgreSQL ENUM is not required and the value is not runtime-extensible metadata.

#### Owner binding

The concrete owner row exists **before** its optional `native_address` projection is inserted.

On `native_address` INSERT, database-local integrity verifies:

```text
native_ref exists in the concrete owner table selected by owner_family
```

The dispatcher is bounded to the 15 accepted owner tables. Unknown family values reject. `native_ref` and `owner_family` are immutable after insertion under ordinary runtime authority.

A custom cross-table check is required because PostgreSQL `CHECK` constraints are row-local and cannot truthfully enforce existence in one of multiple unrelated owner tables. The mechanism therefore uses a narrow schema-qualified trigger/constraint function only for the cross-table part that FK/CHECK cannot express.

Owner deletion/retirement must not leave a live address falsely claiming an extant owner. Until DB-U14 closes owner-specific lifecycle, physical deletion of an addressed owner is not an ordinary runtime operation. The final lifecycle design must either retain the truthful owner/tombstone continuity or remove the address in the same governed lifecycle operation when no surviving references/history require it.

#### Heterogeneous consumer shape

A heterogeneous NativeRef slot stores the reference UUID and uses:

```text
consumer.target_native_ref
    → FK dante.native_address(native_ref)
    → ON DELETE NO ACTION
```

The concrete Reference Contract additionally installs a bounded eligibility check that compares the referenced `native_address.owner_family` with the exact allowed family set for that semantic slot. This eligibility check is database-enforced through a narrow trigger because a normal FK cannot express “FK target exists and its discriminator belongs to this consumer-specific subset”.

The allowed family set is owned by the consuming semantic Reference Contract, not by `native_address` globally.

This deliberately avoids:

```text
application-only type + uuid
one-of-N nullable FKs for one heterogeneous slot
global generic target_kind + target_id semantics
```

Homogeneous slots continue to bypass `native_address` and use direct concrete-owner FKs.

#### Index posture

```text
PRIMARY KEY(native_ref)
→ sufficient canonical address lookup index

owner_family
→ no standalone index by default
```

No redundant UUID index is added. Any later owner-family scan index requires a real query/maintenance need under DB-U15.

#### SQLAlchemy shape

CP6-04 may map `native_address` as a small technical row class. It MUST NOT become a polymorphic ORM base for native semantic owners. Concrete owner mappings remain independent.

#### Direct proof obligation

At CP6-04/05, real PostgreSQL must prove at least:

```text
valid existing owner + correct owner_family anchor       PASS
unknown owner_family                                    REJECT
nonexistent concrete owner                              REJECT
owner UUID in wrong concrete family                     REJECT
heterogeneous consumer valid family                     PASS
heterogeneous consumer wrong family                     REJECT
heterogeneous consumer missing address                  REJECT by FK
attempt to mutate native_ref / owner_family             REJECT
address payload beyond bounded control contract         absent by schema
```

This closes **DB-U01** at the control-topology level. Exact heterogeneous consumer eligibility sets are closed with their concept-specific Reference Contracts rather than being guessed globally.

### 7.2 ScopedRecordRef — shared bounded address topology REQUIRED / CLOSED

Concrete LR-02 or qualified-relation records receive stable ScopedRecordRef only when independent addressability, material history, reconciliation or cross-record referencing justifies it.

```text
homogeneous scoped target
→ direct FK to concrete scoped family where possible

genuinely heterogeneous scoped target
→ dante.scoped_address

MaterialStateRef owned by addressable contextual families
→ dante.scoped_address as the scoped owner-address space
```

The shared scoped address mechanism is required because the closed model already contains multiple independently addressable/material contextual families — for example Agreement terms/state, Schedule and consequential governance/contextual records — whose MaterialStateRef control must preserve a discriminated scoped owner address without collapsing those families into one semantic root.

#### Concrete control table — `dante.scoped_address`

```text
scoped_ref      uuid  PRIMARY KEY
scoped_family   text  NOT NULL
```

`scoped_ref` is the stable UUIDv7 ScopedRecordRef of the concrete contextual record. The concrete scoped record remains the semantic owner; `scoped_address` is only a bounded address projection.

`scoped_family` is a schema-controlled technical discriminator. The accepted value set is the set of concrete ScopedRecordRef-owning families that survive the complete CP6-03 object-level derivation. The set is not runtime extensible. Each newly accepted scoped family updates the schema-controlled bounded family validation in the same change as that family.

The concrete contextual record exists before its `scoped_address` row is created. A schema-qualified bounded integrity trigger validates that `scoped_ref` exists in the concrete table selected by `scoped_family`; unknown families reject. `scoped_ref` and `scoped_family` are immutable under ordinary runtime authority.

A scoped owner that never needs stable ScopedRecordRef does **not** receive a ceremonial `scoped_address` row.

#### Heterogeneous scoped consumer shape

A genuine heterogeneous ScopedRecordRef consumer uses:

```text
consumer.target_scoped_ref
    → FK dante.scoped_address(scoped_ref)
    → ON DELETE NO ACTION
```

plus a database-enforced consumer-specific family-eligibility check against `scoped_address.scoped_family`.

Homogeneous scoped references use direct concrete-table FKs and do not route through the shared address table.

#### Index / ORM / proof posture

```text
PRIMARY KEY(scoped_ref)
→ canonical scoped-address lookup

scoped_family
→ no standalone index without DB-U15 proof
```

SQLAlchemy may map a technical `ScopedAddress` row but MUST NOT use it as a semantic mapped superclass.

Direct PostgreSQL proof mirrors NativeRef:

```text
correct scoped family                               PASS
unknown scoped family                               REJECT
missing concrete scoped row                         REJECT
wrong concrete scoped family                        REJECT
heterogeneous consumer wrong family                 REJECT
heterogeneous consumer dangling address             REJECT by FK
address mutation                                    REJECT
```

This closes **DB-U02**. The exact final `scoped_family` vocabulary is populated by the remaining object-level family derivation; that inventory work does not reopen the shared topology decision.

### 7.3 MaterialStateRef — owner-address and facet topology CLOSED

Material semantic states use stable explicit addresses independent from PostgreSQL MVCC tokens, hashes, provider revisions, UUID order or timestamps.

The shared material-state control layer is required and remains technical only.

#### Concrete control table — `dante.material_state_address`

```text
material_state_ref   uuid  PRIMARY KEY
native_owner_ref     uuid  NULL
scoped_owner_ref     uuid  NULL
facet_code           text  NOT NULL
```

Foreign keys:

```text
native_owner_ref
→ dante.native_address(native_ref)
→ ON DELETE NO ACTION

scoped_owner_ref
→ dante.scoped_address(scoped_ref)
→ ON DELETE NO ACTION
```

Row-local owner-space invariant:

```text
exactly one of native_owner_ref / scoped_owner_ref is non-NULL
```

This is an intentional two-address-space discriminator, **not** the forbidden one-of-N owner-FK encoding of a heterogeneous NativeRef slot. It distinguishes two already-closed reference families (`NativeRef` versus `ScopedRecordRef`) and keeps both referential paths database-enforced.

`material_state_ref`, owner address and `facet_code` are immutable under ordinary runtime authority. The table stores no semantic payload, generic status, generic history fields or provider state.

#### Facet representation — `facet_code`

`facet_code` is PostgreSQL `text` with stable schema-owned values.

It is not:

```text
a PostgreSQL-wide semantic enum hierarchy
a runtime-extensible lookup taxonomy
a universal Fact/Version type
a substitute for the owner-specific state table
```

Each materialized state family receives one stable globally unambiguous code, using a documented owner/family-qualified convention such as:

```text
agreement.terms
goal.state
schedule.placement
```

Exact codes are frozen when each material state family is derived. The accepted set is schema-controlled; unknown facet codes reject. A facet addition is a reviewed schema/database-reference change, not runtime metadata insertion.

A bounded cross-table integrity dispatcher maps each accepted `facet_code` to its exact owner address space/family and exact owner-specific material-state payload table. That dispatcher enforces what ordinary row-local CHECK/FK constraints cannot:

```text
facet is recognized
owner address space is correct for that facet
owner family is eligible for that facet
exact owner-specific material-state payload row exists
payload row binds the same MaterialStateRef
payload row binds the same concrete owner
```

Owner-specific state payload tables remain the semantic authority. Their baseline shape is:

```text
material_state_ref
→ PRIMARY KEY
→ FK dante.material_state_address(material_state_ref)

concrete owner FK
→ native or scoped concrete owner table

owner/facet-specific payload columns
→ defined by that concept/facet
```

The payload table is 1:1 with its `material_state_ref`. A narrow deferred constraint trigger on the address/control side permits the address row and payload row to be inserted in the same transaction and requires the complete state to exist by commit. Payload-side validation rejects wrong owner/facet immediately or at the selected constraint boundary.

This closes **DB-U03** and **DB-U04**.

#### Structural indexes

```text
PRIMARY KEY(material_state_ref)

INDEX(native_owner_ref, facet_code)
WHERE native_owner_ref IS NOT NULL

INDEX(scoped_owner_ref, facet_code)
WHERE scoped_owner_ref IS NOT NULL
```

The two partial owner/facet indexes are justified by material-history reconstruction and owner/facet state lookup; they also support owner-side integrity/lifecycle checks. They are not generic “index every FK” decoration. Final names follow the CP3 deterministic naming convention.

#### Direct proof obligation

Real PostgreSQL must prove:

```text
exactly-one owner address invariant                        PASS
missing native/scoped address                             REJECT by FK
unknown facet_code                                        REJECT
facet with wrong owner address space                      REJECT
facet with wrong concrete owner family                    REJECT
missing owner-specific payload by commit                  REJECT
payload MaterialStateRef mismatch                         REJECT
payload owner mismatch                                    REJECT
attempt to mutate state address owner/facet/ref            REJECT
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
optional bounded native/scoped owner-address projection
        ↓
dante.material_state_address
        ↓
owner-specific immutable-by-policy material-state row
        ↓
explicit current accepted-state binding where required
        ↓
typed owner-specific correction/replacement/reconciliation lineage
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

Every material-state payload family owns its semantic columns and chronology. `material_state_address` owns only address/control facts.

### 8.3 Current accepted-state binding topology CLOSED

Where the accepted model needs singular current material truth for an owner/facet, DANTE uses two bounded technical current-binding tables that preserve the NativeRef/ScopedRecordRef separation.

#### `dante.native_current_material_state`

```text
native_owner_ref     uuid  NOT NULL
facet_code           text  NOT NULL
material_state_ref   uuid  NOT NULL

PRIMARY KEY(native_owner_ref, facet_code)
UNIQUE(material_state_ref)

FK native_owner_ref
→ dante.native_address(native_ref)
→ ON DELETE NO ACTION

FK material_state_ref
→ dante.material_state_address(material_state_ref)
→ ON DELETE NO ACTION
```

#### `dante.scoped_current_material_state`

```text
scoped_owner_ref     uuid  NOT NULL
facet_code           text  NOT NULL
material_state_ref   uuid  NOT NULL

PRIMARY KEY(scoped_owner_ref, facet_code)
UNIQUE(material_state_ref)

FK scoped_owner_ref
→ dante.scoped_address(scoped_ref)
→ ON DELETE NO ACTION

FK material_state_ref
→ dante.material_state_address(material_state_ref)
→ ON DELETE NO ACTION
```

The composite primary key guarantees at most one current accepted MaterialStateRef per owner/facet in each address space. `UNIQUE(material_state_ref)` states the reciprocal invariant: one exact MaterialStateRef cannot simultaneously be the current binding for another owner/facet.

A narrow database trigger validates, on INSERT/UPDATE, that the selected `material_state_address` has:

```text
same address space
same owner ref
same facet_code
```

Because material-state address ownership/facet is immutable, this validation cannot silently become stale later.

Normal mutation of current truth is therefore:

```text
insert new MaterialStateRef/control row
→ insert exact owner-specific immutable state payload
→ validate complete state
→ update current binding from old state_ref to new state_ref
→ commit under the operation's applicable expected-state/concurrency rule
```

The current-binding tables contain no semantic payload and no lifecycle history. Past truth remains in owner-specific material-state/history structures.

No owner-specific sparse `current_*_state_ref` column proliferation is required, and no generic `owner_kind + owner_id` current-state table is introduced.

This closes **DB-U05**.

#### Current-binding direct proof

```text
first current state for owner/facet                        PASS
replacement with another valid same-owner/same-facet state PASS
second simultaneous row for same owner/facet               REJECT by PK
same MaterialStateRef bound twice                           REJECT by UNIQUE
wrong owner                                                 REJECT
wrong facet                                                 REJECT
wrong address space                                         REJECT
dangling MaterialStateRef                                   REJECT by FK
current selected by MAX/UUID order                          absent by design
```

### 8.4 Lineage topology CLOSED

DANTE does **not** create a shared `material_state_edge`, `state_lineage(type, from, to)` or universal history graph.

Lineage is classified as follows:

```text
simple owner/facet-specific one-predecessor correction/replacement
→ explicit typed FK column(s) on the concrete material-state family when that exactly represents the semantics

owner/facet-specific multi-predecessor or metadata-bearing lineage
→ dedicated owner/facet-specific lineage relation table

Reconciliation as a material semantic resolution
→ concrete Reconciliation contextual family referencing the competing MaterialStateRefs / sources and the resulting accepted state as required

technical correlation/causation
→ technical provenance/runtime fields or relations
→ never substituted for semantic correction/replacement/reconciliation
```

The exact relation name and cardinality are owned by the concrete concept/facet. Examples such as `corrects_material_state_ref`, `replaces_material_state_ref` or a specific `<family>_state_lineage` table are accepted only when the corresponding Domain semantics require them.

Rules:

```text
correction != replacement != reconciliation
old MaterialStateRef remains stable
new accepted meaning receives a new MaterialStateRef
no semantic state payload is overwritten to fake history
no generic lineage type vocabulary is introduced merely for reuse
same-family/same-owner/facet eligibility is database-enforced for each concrete lineage relation
```

Reusable SQLAlchemy/migration helpers may reduce technical repetition, but they must not create a shared semantic mapped/table root.

This closes **DB-U06**.

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

The reusable physical encoding contract and owner-family chronology placement are closed in section 21.3.

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

Exact numeric/temporal/recurrence value contracts are closed in section 21. Place spatial shape remains intentionally absent from the mandatory Place identity row; PostGIS activation is trigger-bound as specified there.

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

For the bounded address/material-state controls closed in sections 7–8, trigger use is restricted to cross-table owner/family/facet/payload equality/existence that PostgreSQL row-local CHECK and ordinary FK constraints cannot fully express. It is not product workflow logic.

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

### 13.1 Control-row transaction ordering

The bounded control topology uses explicit transaction ordering rather than deferring ordinary FKs by convenience:

```text
native/scoped semantic owner exists
→ optional address row is inserted and owner existence is checked
→ material_state_address is inserted
→ owner-specific material-state payload is inserted
→ deferred completeness check fires no later than COMMIT
→ current binding may be inserted/updated after the complete state exists
```

A `DEFERRABLE INITIALLY DEFERRED` **constraint trigger** is permitted for the address→payload completeness invariant because the two rows are intentionally created in one transaction and PostgreSQL permits constraint-trigger execution at transaction end. Ordinary direct FKs remain immediate unless a concrete transaction genuinely requires deferral.

---

## 14. Candidate relational family inventory

This inventory is the first CP6-03 concrete map. `REQUIRED` means the closed model requires a concrete family. `CONDITIONAL` means the semantic family exists but an independent persistent table/state is created only when the material/addressability threshold is met. `NO ROOT` means the concept is represented through another concrete family rather than receiving an independent generic table.

### 14.1 Native canonical owner families — LR-01

| Domain concept | Candidate canonical owner object | Status | Material/history pressure |
|---|---|---|---|
| Person | `person` | REQUIRED | conditional owner-specific material state/history |
| Living Referent | `living_referent` | REQUIRED | conditional owner-specific material state/history |
| Asset | `asset` | REQUIRED | conditional owner-specific material state/history |
| Place | `place` | REQUIRED | no mandatory geometry/address payload; spatial state is trigger-bound |
| Content Artifact | `content_artifact` | REQUIRED | material content-state/history when exact revision matters |
| Collective | `collective` | REQUIRED | identity independent from membership; governance/state history conditional |
| Possibility | `possibility` | REQUIRED once retained as canonical | candidate state before acceptance remains noncanonical |
| Goal | `goal` | REQUIRED | material lifecycle/history when consequential |
| Plan | `plan` | REQUIRED | exact material plan history when later meaning depends on revision |
| Activity | `activity` | REQUIRED | material state/history when consequential |
| Event | `event` | REQUIRED | temporal placement remains Schedule; material state/history conditional |
| Routine | `routine` | REQUIRED | Recurrence remains separate LR-05; governing state/history when Occurrences depend on exact state |
| Occurrence | `occurrence` | REQUIRED once individually distinguished | lazy pre-materialization locator remains separate from native identity; generation context retained |
| Session | `session` | REQUIRED | execution chronology is state, not identity; correction/split/merge history conditional |
| Observation | `observation` | REQUIRED | effective assertion chronology/payload remain owner-specific; material correction/history required when material |

No table above inherits from a common semantic Entity table.

A `native_address` row is a lazy bounded technical projection created only when a concrete owner must participate in heterogeneous/address-control semantics; the canonical owner row above remains the semantic identity owner.

The exact identity-shell columns for all 15 owners are closed in section 21.1.

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

Addressable/material contextual families use `scoped_address` only when the exact family owns a justified ScopedRecordRef.

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
| Recurrence | `recurrence` scoped definition + material `recurrence.definition` state + six family-specific typed payloads | REQUIRED where canonical recurrence is persisted | no RRULE/provider-string canonical kernel; exact family contract CLOSED |
| Resource Requirement | structured requirement specification | REQUIRED where accepted | contextual address only where justified |
| Temporal Constraint | structured temporal constraint family | REQUIRED | distinct from Schedule |

### 14.5 Value semantics — LR-04

| Concept | Persistence disposition |
|---|---|
| Monetary Amount | NO independent identity/root; owner-bound `numeric` amount + explicit three-letter currency code contract |
| Quantity | NO independent identity/root; owner-bound exact `numeric` magnitude + bounded unit semantics |
| Capacity | NO universal Capacity owner; typed value/rule/contextual representation as accepted consumer requires |

Repeated Quantity/MonetaryAmount shapes may use SQLAlchemy composites/helpers, but no shared semantic row identity is introduced.

### 14.6 Cross-cutting history / projection / integration families

| Logical role | Candidate persistence family | Status |
|---|---|---|
| LR-07 material history | owner-specific material-state rows + `material_state_address` + bounded current-state controls + typed owner-specific lineage | REQUIRED where material |
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
| 02 | Activity | LR-01 | required native canonical owner family; identity shell CLOSED, semantic state derivation continues |
| 03 | Actor | contextual role | NO ROOT; actual eligible referent carried by owning operation/provenance/relation |
| 04 | Actual | LR-06/LR-02 | specific realization family for material canonical Actual |
| 05 | Agreement | LR-02 + n-ary relation | required contextual Agreement + terms MaterialState + party assent topology |
| 06 | Asset | LR-01 | required native canonical owner family; identity shell CLOSED |
| 07 | Authority | LR-03/LR-02/LR-05/LR-08 | governance relation/state + basis + derived effective view; no generic ACL truth |
| 08 | Availability | LR-05/LR-02/LR-08 | structured rule/override; effective state derived |
| 09 | Capacity | LR-04/LR-05/LR-02/LR-08 | NO native root; typed capacity/rule/material context as consumer requires |
| 10 | Collective | LR-01 | required native canonical owner family independent of member set; identity shell CLOSED |
| 11 | Conditional Policy | LR-05 | structured policy/specification family |
| 12 | Confirmation | LR-03 | specific attestation relation; material qualification conditional |
| 13 | Consent | LR-03/LR-02 | specific governance relation/state with material history when consequential |
| 14 | Content Artifact | LR-01 | required native canonical owner; byte storage remains separate bounded capability; identity shell CLOSED |
| 15 | Contribution | LR-03 | specific contribution/attribution relation |
| 16 | Coordination Stewardship | LR-03 | specific stewardship relation |
| 17 | Criterion | LR-05 | structured criterion/specification family |
| 18 | Evaluation | LR-08 / LR-02 | derived by default; material snapshot only when consequential |
| 19 | Decision | LR-02 | conditional independent decision record when lifecycle/history matters |
| 20 | Dependency | LR-03 | specific directional contingency relation |
| 21 | Event | LR-01 | required native canonical owner family; temporal placement remains Schedule; identity shell CLOSED |
| 22 | Evidence | LR-03 | typed source→evaluation/context use relation; exact source state when required |
| 23 | Goal | LR-01 | required native canonical owner family; identity shell CLOSED |
| 24 | Interpersonal Relationship | LR-03 | bounded Person-to-Person specific relation family |
| 25 | Living Referent | LR-01 | required native canonical owner family distinct from Person/Asset; identity shell CLOSED |
| 26 | Membership | LR-03 | specific membership relation; Collective identity remains independent |
| 27 | Milestone | LR-02 | dependent milestone family; material address/history where justified |
| 28 | Monetary Amount | LR-04 | NO ROOT; exact owner-bound numeric/currency contract CLOSED |
| 29 | Observation | LR-01 | required native canonical owner; identity shell + temporal placement contract CLOSED; payload/state derivation continues |
| 30 | Occurrence | LR-01 when distinguished | native owner once individually distinguished; lazy locator before row materialization; generation context preserved |
| 31 | Outcome | LR-06/LR-02 | specific result/disposition family when materially persistent |
| 32 | Ownership | LR-03 | specific ownership relation |
| 33 | Participation | LR-03 | specific intended/response/actual participation relation semantics |
| 34 | Person | LR-01 | required native canonical owner; separate from Account/Principal; identity shell CLOSED |
| 35 | Place | LR-01 | required native owner; no universal geometry/address field; PostGIS activation trigger CLOSED |
| 36 | Plan | LR-01 | required native owner; material plan-state history when revision matters; identity shell CLOSED |
| 37 | Possession | LR-03 | specific possession/custody relation |
| 38 | Possibility | LR-01 once canonical | required native owner after acceptance; pre-acceptance candidates noncanonical; identity shell CLOSED |
| 39 | Proposal | LR-02 | conditional proposal record; target exact state when consequential |
| 40 | Provenance | LR-07 | bounded typed lineage/provenance attached to concrete effects/states; NO universal graph root |
| 41 | Quantity | LR-04 | NO ROOT; exact owner-bound magnitude/unit contract CLOSED |
| 42 | Reconciliation | LR-02/LR-07 | material reconciliation record where resolution/history matters |
| 43 | Recurrence | LR-05 | scoped typed definition when persisted + six family-specific material-state payloads; physical family contract CLOSED |
| 44 | Representation | LR-03/LR-02 | specific on-behalf-of governance relation/state |
| 45 | Request | LR-02 | conditional directed request record; distinct from effect/idempotency identity |
| 46 | Resource Allocation | LR-03/LR-02 | specific allocation relation/contextual record when material |
| 47 | Resource Requirement | LR-05/LR-02 | structured requirement; scoped record where materially addressable |
| 48 | Resource | contextual role | NO ROOT; eligible concrete provider/value/service/pool/specialist target |
| 49 | Responsibility | LR-03 | specific responsibility relation family |
| 50 | Routine | LR-01 | required native owner; Recurrence separate; identity shell CLOSED |
| 51 | Schedule | LR-02 | dependent accepted-placement family; material/scoped when consequential |
| 52 | Session | LR-01 | required native execution-episode owner; identity shell CLOSED; actual chronology belongs to state |
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

## 16. CP6-01 Part-2 cross-cutting/non-owner disposition — current matrix

Gate 03 requires 100% accounting beyond the 57 Domain concepts. This matrix uses the final allowed disposition vocabulary and now contains no `OPEN DERIVATION` entry.

| Construct | Current disposition | Current CP6-03 reasoning / exact trigger |
|---|---|---|
| ReferenceAddress | NO INDEPENDENT PERSISTENCE as universal root | represented by the four discriminated address contracts and concrete bounded mechanisms |
| Reference Contract | NO INDEPENDENT PERSISTENCE | homogeneous direct FK; heterogeneous native/scoped address + database-enforced consumer-family eligibility |
| NativeRef | MATERIALIZE IN CP6 | native owner UUIDs + direct FKs; `native_address` CLOSED as bounded heterogeneous/material-owner control topology |
| ScopedRecordRef | MATERIALIZE IN CP6 where concrete scoped families require stable address | shared `scoped_address` topology CLOSED; rows exist only for justified addressable contextual families |
| MaterialStateRef | MATERIALIZE IN CP6 | `material_state_address` owner-space/facet topology CLOSED + owner-specific state rows |
| ExternalRef | GENUINELY DEFERRED for generic/shared provider structures | trigger = first concrete integration/provider contract; no provider ontology invented now |
| Current accepted-state binding | MATERIALIZE IN CP6 where material state exists | `native_current_material_state` / `scoped_current_material_state` topology CLOSED |
| Correction/replacement/reconciliation lineage | MATERIALIZE IN CP6 where material history exists | owner/facet-specific typed lineage; no universal state graph; topology CLOSED |
| World/effective chronology | MATERIALIZE IN CP6 per family where material | reusable typed temporal contract CLOSED; concrete semantic columns stay owner-specific |
| Recorded/learned/accepted chronology | MATERIALIZE IN CP6 per family where material | separate from world chronology only when required; absolute instants use `timestamptz` |
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
| Capacity Claim pressure | CONDITIONAL OWNER-SPECIFIC MATERIALIZATION / NO UNIVERSAL ROOT | owner/context-specific qualified commitment relation; ScopedRecordRef only when material/addressable; historical Schedule/material basis reconstructible |
| Tombstone/retirement/redaction continuity | MATERIALIZE IN CP6 where owner lifecycle requires it | owner-specific/minimal continuity; NO generic semantic Tombstone owner |
| Anti-resurrection reconciliation | GENUINELY DEFERRED as executable recovery mechanism | trigger = destructive recovery/restore stage; schema must not make later enforcement impossible |
| Transactional outbox | GENUINELY DEFERRED | trigger = first real Class-A async external effect; not Domain history/event store |
| PowerSync/encrypted SQLite | GENUINELY DEFERRED | trigger = offline/mobile activation; PostgreSQL remains canonical |
| Search/vector indexes/caches | GENUINELY DEFERRED except concrete indexes justified by the database model | trigger = real search/vector/query consumer; no speculative pgvector/GIN materialization |

```text
UNCLASSIFIED CROSS-CUTTING CONSTRUCTS
0
```

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
1. SEMANTIC OWNER / SCOPED ROW FOUNDATIONS
   15 LR-01 canonical owner tables
   + concrete scoped/contextual tables as their derivations are frozen
        ↓
2. BOUNDED ADDRESS CONTROL
   native_address
   scoped_address
   + schema-qualified family-validation trigger functions
        ↓
3. MATERIAL-STATE CONTROL FOUNDATION
   material_state_address
   native_current_material_state
   scoped_current_material_state
   + owner-space/facet/current-binding validation functions
        ↓
4. OWNER-SPECIFIC MATERIAL STATE / HISTORY
   exact material-state payload rows
   chronology
   owner/facet-specific correction/replacement/reconciliation lineage
   + deferred address→payload completeness constraints
        ↓
5. DEPENDENT / CONTEXTUAL FAMILIES
   Agreement / Schedule / Milestone / Actual / Proposal / Decision / Request / etc.
   (where not already required as addressable owner prerequisites)
        ↓
6. SPECIFIC RELATION FAMILIES
   Membership / Responsibility / Participation / Ownership / Consent / Authority / Visibility / etc.
        ↓
7. RULE / POLICY / SPECIFICATION FAMILIES
   Recurrence / Temporal Constraint / Criterion / Availability / Conditional Policy / Resource Requirement
        ↓
8. RESULT / GOVERNANCE / PROVENANCE COMPLETION
   Outcome / material Evaluation / reconciliation / exact provenance bindings
        ↓
9. PROVIDER / DERIVED / SPECIALIST STRUCTURES
   only where closed authority and real trigger justify materialization
        ↓
10. DOCUMENTATION + INTROSPECTION QA
   dictionary / generated reference / diagrams / schema drift / direct tests
```

This is a dependency DAG, not a product roadmap. Specific families can move earlier/later when their FK/material-state dependencies prove it.

### 17.1 Address-control insertion dependency

The closed control topology avoids circular semantic ownership by treating address rows as **bounded projections of already-existing semantic owners**, not parents that every owner must inherit from.

Normal order:

```text
create concrete native/scoped semantic row
→ when heterogeneous/material addressing is actually required, create matching native_address/scoped_address
→ validate address family against concrete owner
→ create material_state_address when a material state is accepted
→ create exact owner-specific state payload
→ satisfy deferred completeness check by COMMIT
→ create/update explicit current binding where required
```

This pattern preserves:

```text
concrete semantic owner remains authoritative
address exists only for a real owner
no universal Entity/Thing row
no application-only referential integrity
```

### 17.2 Restore / bulk-load validation implication

Custom cross-table trigger enforcement is not a replacement for restore/evolution QA. CP6-05 must include explicit integrity scans that can prove after migration/restore-style loading that:

```text
no native/scoped address is orphaned or family-mismatched
no material_state_address lacks/mismatches its payload
no current binding mismatches owner/facet/state
```

Destructive backup/restore evidence itself remains staged under HG-09/HG-12/PSV as already defined.

### 17.3 Recurrence sub-DAG

A persisted, material Recurrence follows the already-closed address/state order:

```text
concrete recurring source (Routine/Event or another later accepted source)
→ recurrence scoped owner
→ scoped_address when stable Recurrence addressability is required
→ recurrence.definition MaterialStateRef
→ recurrence_state header
→ exactly one family-specific recurrence-state payload
→ effective-range/boundary rows where applicable
→ current recurrence.definition binding
→ Occurrence generation context may bind the exact governing MaterialStateRef
```

No generated Occurrence is required merely to prove the Recurrence schema.

---

## 18. SQLAlchemy mapping plan — current

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

The bounded control objects may be represented by technical mappings such as:

```text
NativeAddress
ScopedAddress
MaterialStateAddress
NativeCurrentMaterialState
ScopedCurrentMaterialState
```

Those classes are persistence-control rows only. Native/scoped semantic owners do not inherit from them in SQLAlchemy.

Reference-family Python types continue to distinguish `NativeRef`, `ScopedRecordRef` and `MaterialStateRef` even though their SQL scalar is `uuid`.

The 15 native owner tables map to 15 independent semantic row classes with no polymorphic base table. Reusable Quantity/MonetaryAmount and temporal column bundles may use SQLAlchemy value/composite helpers; value-object convenience must not create an extra persistence identity.

Recurrence maps as a scoped Recurrence row + material `RecurrenceState` header + one typed family-state row. Family dispatch is explicit application persistence logic over the discriminator; it is not SQLAlchemy polymorphic semantic inheritance and it does not authorize a generic Rule model.

Each final Database Dictionary entry will point to its SQLAlchemy mapping when one exists.

Views/generated/projection objects do not require ORM classes merely for symmetry.

---

## 19. Direct PostgreSQL proof plan — current

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
15 owner PKs reject duplicate identity
native owner PK mutation forbidden by persistence contract
homogeneous FK integrity
native_address valid existing owner/family PASS
native_address unknown family REJECT
native_address nonexistent owner REJECT
heterogeneous native reference valid target PASS
heterogeneous native reference wrong family REJECT
heterogeneous native reference dangling target REJECT
scoped_address valid existing owner/family PASS
scoped_address unknown/wrong/missing owner REJECT
heterogeneous scoped wrong family/dangling target REJECT
address ref/family mutation REJECT
anchor leakage / forbidden generic payload REJECT by design/schema
```

Maps especially to PG-R01 / PG-R02.

### 19.3 Material state/history

```text
MaterialStateRef exists exactly once
exactly one native/scoped owner address present
unknown material facet rejected
facet owner-space/family mismatch rejected
state row belongs to correct owner/facet
missing state payload rejected by commit
wrong owner rejected
wrong facet rejected
current binding points to valid same-owner/same-facet accepted state
one current state per owner/facet enforced
one MaterialStateRef cannot be current for another owner/facet
correction creates new state rather than silent overwrite
owner-specific typed lineage rejects wrong-owner/facet links
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
Capacity Claim does not collapse into Schedule/Allocation/Actual use
material Capacity Claim retains/reconstructs exact temporal/material basis
```

Maps especially to PG-R06 and WL-H01/WL-H11.

### 19.5 Temporal / Recurrence / Occurrence

```text
date-only remains date-only
floating local != named-zone local != absolute instant
named-zone consequential resolution preserves original local value + zone + accepted resolved instant
no false UTC conversion of floating local values
daterange/tstzrange bound semantics preserved where used
elapsed recurrence rejects zero/negative interval and calendar-month substitution
calendar recurrence keeps wall-clock/zone semantics through DST policy
quota recurrence preserves explicit period frame and does not invent ordinal quota identity
completion-relative recurrence cannot generate the next chain without a qualifying anchor when the rule requires one
anchor-stream recurrence keeps qualifying anchor contract distinct from generic Trigger
cyclic recurrence preserves position/cycle semantics
exactly one recurrence family payload per recurrence definition MaterialStateRef
family discriminator/payload mismatch rejected
current recurrence state explicit; MAX/time/UUID inference absent
world vs recorded chronology where material
lazy occurrence locator → persisted Occurrence continuity
materialized historical Occurrence retains governing recurrence/source MaterialStateRef
unordered quota slots do not gain fake ordinal identity
```

Maps especially to PG-R07 / PG-R08.

### 19.6 Quantity / MonetaryAmount

```text
exact decimal round-trip without binary-float substitution
NaN/+Infinity/-Infinity rejected for canonical amounts
Quantity requires non-empty bounded unit semantics
MonetaryAmount requires explicit three-letter uppercase currency code
PostgreSQL money absent
no Quantity/MonetaryAmount identity table
source/display/conversion rounding does not rewrite material source representation
```

### 19.7 Place / PostGIS boundary

```text
Place persists with only native identity and no mandatory geometry/address
no speculative GiST/SP-GiST spatial index exists
PostGIS capability presence does not manufacture canonical spatial truth
future spatial facet cannot be introduced without explicit shape/SRID/index/query contract
```

### 19.8 Missingness/lifecycle

```text
absence does not encode universal false
explicit negative states remain distinguishable
NO ACTION lifecycle defaults hold
retired/tombstoned stable identity not reused
redacted/unavailable does not become never-existed
address/owner continuity remains truthful under the final DB-U14 lifecycle design
```

### 19.9 Concurrency

When a concrete subject exists:

```text
stale expected MaterialStateRef conflicts
valid expected state succeeds
multi-owner invariant survives concurrent writes
whole transaction rolls back atomically on local invariant failure
```

Maps to PG-R04 / PG-R05.

### 19.10 Derived/provider boundaries

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

The five bounded control objects now have stable design names and must receive dictionary entries when dictionary files are instantiated:

```text
native_address
scoped_address
material_state_address
native_current_material_state
scoped_current_material_state
```

The 15 native owner identity-table names and the Recurrence family names in section 21 are now stable design names as well; dictionary materialization still waits for the remaining object-level table/column graph so one coherent dictionary is generated rather than a sequence of partial files.

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

## 21. Object-level closure pass I — LR-01 identity shells + temporal/value/recurrence/spatial/capacity contracts

This section consumes the complete canonical continuations for the 15 LR-01 owners together with the accepted Time/Reality and Resources/Values/Capacity logical slices. It closes the deterministic part of their relational baseline without inventing owner payload columns that the Domain does not establish.

The central rule is:

```text
stable native identity
!= current mutable semantic payload
!= MaterialStateRef
!= relation membership
!= Schedule / Recurrence / Actual
!= provider identity
```

### 21.1 Exact LR-01 native identity-shell tables — CLOSED

The minimum canonical row for each LR-01 owner is intentionally narrow:

```text
dante.person
  person_ref              uuid PRIMARY KEY

dante.living_referent
  living_referent_ref     uuid PRIMARY KEY

dante.asset
  asset_ref               uuid PRIMARY KEY

dante.place
  place_ref               uuid PRIMARY KEY

dante.content_artifact
  content_artifact_ref    uuid PRIMARY KEY

dante.collective
  collective_ref          uuid PRIMARY KEY

dante.possibility
  possibility_ref         uuid PRIMARY KEY

dante.goal
  goal_ref                uuid PRIMARY KEY

dante.plan
  plan_ref                uuid PRIMARY KEY

dante.activity
  activity_ref            uuid PRIMARY KEY

dante.event
  event_ref               uuid PRIMARY KEY

dante.routine
  routine_ref             uuid PRIMARY KEY

dante.occurrence
  occurrence_ref          uuid PRIMARY KEY

dante.session
  session_ref             uuid PRIMARY KEY

dante.observation
  observation_ref         uuid PRIMARY KEY
```

Rules applying to all 15:

```text
SQL type                         PostgreSQL uuid
ID policy                        UUIDv7
normal issuer                    backend application boundary
DB-generated semantic ID         not the default
PK update                        forbidden under ordinary runtime behavior
semantic parent FK               none
created_at / updated_at          none by convention
name / title                     none by convention
status                           none by convention
deleted_at / is_deleted          none by convention
metadata JSONB                   none by convention
native_address FK                none on owner row
```

`native_address` remains an optional technical projection of an already-existing owner. The owner row does not depend on the address row.

This identity shell is not permission to establish semantically empty business objects. The application operation that creates a canonical owner must establish every companion semantic row/state required by that concept at the same consistency boundary. The distinction is that those facts are **not identity columns** and therefore do not belong in the native-owner PK shell merely for CRUD convenience.

Owner-specific separation is now fixed as follows:

| Native owner | Not part of native identity row | Where the fact belongs |
|---|---|---|
| Person | name/contact/account/provider identity/relationships | owner-specific semantic state, typed relation, Account/ExternalRef boundary as applicable |
| Living Referent | species/classification/current descriptive state | owner-specific state; no Asset collapse |
| Asset | model/classification/ownership/possession/location/provider ID | owner-specific state or the exact relation/provider family |
| Place | name/address/coordinates/geometry/home-work role/provider ID | owner-specific spatial/descriptive state or specific spatial relation/provider mapping |
| Content Artifact | bytes/content revision/provider object | content material state + bounded byte-storage/provider boundary |
| Collective | current member set/governance | Membership/governance relations and material state where required |
| Possibility | pre-acceptance candidate interpretation | LR-11 before canonical retention; owner-specific state after it becomes canonical |
| Goal | progress/status/Plan/criteria/target timing/governor | Goal state, Criterion/Evaluation, relations and temporal value semantics |
| Plan | Activities/current strategy/status/Schedule | Plan material state + typed relations; Schedule remains separate |
| Activity | Schedule/performer/Actual/status | Activity state + typed relations + Schedule/Actual families |
| Event | current start/end/current venue/Actual/participants | Schedule, specific spatial/participation relations and Actual |
| Routine | recurrence expression/generated instances/current schedule | Recurrence + Occurrence + Schedule; Routine remains source policy identity |
| Occurrence | current datetime/Schedule/Actual | generation context + Schedule/Actual; moved instance keeps same identity |
| Session | start/end/current duration/Activity identity | Session execution state + typed realization relations |
| Observation | subject/property/value/effective time/provider evidence | Observation assertion/material state + typed subject/value/provenance contracts |

The table shell therefore remains stable even when ordinary semantic state changes. Material state is added only at the CP6-02 materiality threshold; low-consequence current fields do not automatically receive history merely because the owner has native identity.

### 21.2 Occurrence generation-context requirement

A materialized `Occurrence` must retain enough generation context to explain why that expected instance exists under the exact governing source/rule state.

The companion family is:

```text
dante.occurrence_generation
  occurrence_ref                   uuid PRIMARY KEY
  source_native_ref                uuid NOT NULL
  governing_material_state_ref     uuid NOT NULL
```

Constraints:

```text
occurrence_ref
→ FK dante.occurrence(occurrence_ref)
→ ON DELETE NO ACTION

source_native_ref
→ FK dante.native_address(native_ref)
→ ON DELETE NO ACTION
→ current accepted generation-source eligibility: routine OR event

governing_material_state_ref
→ FK dante.material_state_address(material_state_ref)
→ ON DELETE NO ACTION
```

A bounded database eligibility check verifies the source family and that the governing MaterialStateRef is an applicable material state for the source/Recurrence generation context. If a later accepted generative source family is added, its eligibility is a reviewed schema change.

Family-specific virtual coordinates are **not** forced into this common row. Calendar coordinates, quota-period slots, qualifying completion anchors, anchor-stream facts and cycle positions remain recurrence/occurrence-family-specific typed structures. In particular, unordered quota slots do not receive a fabricated semantic ordinal.

A purely virtual, still-indistinguishable future quota slot does not require an `occurrence` row. Once an individual expected instance is semantically distinguished, its UUID identity is stable and subsequent materialization does not create a different Occurrence.

### 21.3 Typed temporal physical contract — DB-U07 CLOSED

DANTE does not create a universal `temporal_value` table. Temporal meaning is embedded through typed column bundles in the exact semantic owner/state that owns the fact.

Closed physical encodings:

| Semantic temporal form | PostgreSQL representation | Required rule |
|---|---|---|
| civil/date-only | `date` | never converted to midnight UTC merely for storage |
| floating local datetime | `timestamp without time zone` | no zone/instant may be inferred from device locale |
| named-zone local datetime | `timestamp without time zone` + `zone_id text` | `zone_id` stores the IANA zone identifier; original civil meaning remains canonical |
| consequential resolved named-zone datetime | named-zone columns + `resolved_at timestamptz` | retains the exact accepted instant used historically; later tzdb changes do not rewrite it |
| absolute instant | `timestamptz` | one fixed instant; display zone is not canonical identity |
| date range | `daterange` | bounds/inclusivity declared by the owning semantic family |
| absolute-instant range | `tstzrange` | bounds/inclusivity declared by the owning semantic family |
| local/zoned range | paired typed local boundaries + one explicit frame/zone contract | do not fake a UTC range when the source meaning is local/floating |
| elapsed duration | `interval` restricted to an elapsed-duration contract or exact numeric elapsed quantity where the family requires fixed arithmetic | calendar-relative month/day semantics must not be smuggled into elapsed recurrence |
| coarse/partial precision | semantic value + bounded `precision_code` where needed | no invented minute/second precision |

DANTE does not use `time with time zone`/`timetz` as a substitute for named-zone semantics because a UTC offset is not an IANA time-zone rule set.

`zone_id` is schema/application validated against the accepted IANA vocabulary used by the runtime. It is not a foreign key to a mutable provider-owned timezone table.

Where a named-zone value becomes consequentially resolved, storing `resolved_at` alongside the originating local value and `zone_id` is sufficient to preserve which instant DANTE actually accepted; future timezone-rule updates may affect future recurrence expansion but do not reinterpret the historical accepted instant.

Chronology placement for the current database families is closed as follows:

```text
15 LR-01 identity rows
→ no mandatory chronology column

MaterialState control address
→ no generic semantic created_at/current_at ordering

owner/facet-specific material state
→ world/effective chronology only where the concept requires it
→ recorded/learned/accepted chronology only where materially distinct

Schedule
→ accepted placement chronology owned by Schedule state

Session
→ actual execution chronology owned by Session state

Observation
→ effective/observed chronology owned by Observation assertion/state
→ recorded/learned chronology separate only where material

Recurrence
→ pattern anchor/effective range belong to Recurrence state
→ source creation time is never the implicit recurrence anchor

Occurrence
→ original/generation coordinate belongs to occurrence-generation context
→ current placement remains Schedule

Goal/Plan/Activity/Event/Routine
→ target/horizon/constraint/recurrence/schedule time does not become an identity-row timestamp
```

Specific semantic column names are owned by the concrete state/relation family (`observed_at`, `accepted_at`, `effective_range`, etc.); a global `created_at`/`updated_at` doctrine remains rejected.

### 21.4 Place/PostGIS disposition — DB-U11 CLOSED

The only universally required Place table remains:

```text
dante.place
  place_ref uuid PRIMARY KEY
```

The current Domain authority explicitly defines:

```text
Place != address
Place != coordinates / geometry
Place != provider Place ID
```

Therefore CP6 does **not** invent any of:

```text
place.geometry geometry(Point, 4326)
place.geography geography(Point, 4326)
place.latitude / place.longitude
one universal postal-address column set
one universal Place spatial index
```

PostGIS remains an accepted PostgreSQL capability but **no canonical Place spatial column or GiST/SP-GiST index is activated merely because the extension is available**.

The first future canonical spatial facet must explicitly establish before migration:

```text
what the stored shape means
Point / Polygon / Multi* / another reviewed shape
geometry vs geography semantics
SRID / coordinate-reference contract
2D / Z / M requirements
source vs accepted geometry
correction/history/materiality
required spatial operations
exact GiST/SP-GiST index reason
```

Trigger for that activation:

```text
first closed DANTE capability whose canonical behavior requires persisted geometry
(e.g. exact distance/geofence/spatial-containment/query semantics)
```

Address/geocoder/provider coordinates may exist as source/evidence/integration state without silently becoming canonical Place geometry.

DB-U11 is therefore closed as **NO UNIVERSAL MANDATORY SPATIAL COLUMN; FUTURE OWNER-SPECIFIC SPATIAL FACET TRIGGER-BOUND**. This is a concrete negative design decision, not an unresolved placeholder.

### 21.5 Quantity and MonetaryAmount value contract — DB-U13 CLOSED

Neither value family receives an identity table.

#### Quantity

Canonical persisted shape at the containing owner/state:

```text
<magnitude_column>   numeric NOT NULL
<unit_code_column>   text    NOT NULL
```

Rules:

```text
numeric is exact decimal storage
no global precision/scale is imposed
NaN / +Infinity / -Infinity are rejected for canonical Quantity values
unit_code must be non-empty and normalized under the consuming quantity-kind contract
unit semantics do not encode the measured property/Subject
custom unit labels do not imply a global conversion definition
```

A specific owner may add a stricter `numeric(p,s)`, range CHECK or controlled unit vocabulary only when its Domain contract proves that bound. There is no universal `unit` entity/catalog in the kernel.

#### MonetaryAmount

Canonical persisted shape at the containing owner/state:

```text
<amount_column>         numeric NOT NULL
<currency_code_column>  text    NOT NULL
```

Rules:

```text
PostgreSQL money type                         FORBIDDEN
NaN / +Infinity / -Infinity                   REJECTED
currency_code syntactic contract              ^[A-Z]{3}$
currency semantic vocabulary                  ISO-4217-compatible where applicable
Currency native entity                        NONE
FX rate/provider basis                        separate contextual/provenance state
converted display/value                       derived; never mutates source amount
```

A current external currency-code catalog is not used as a hard FK that could make historically valid codes unreadable after vocabulary change. Specialist non-fiat/token/instrument semantics remain outside the kernel MonetaryAmount contract.

PostgreSQL `numeric` does not by itself preserve source lexical precision as a semantic claim. If source precision/rounding is consequential, the containing state/provenance retains the material source representation or explicit source-scale/rounding basis. Display scale is never inferred to be source precision merely from the stored numeric value.

SQLAlchemy may package these column pairs as immutable value/composite Python types for application ergonomics. Such Python values do not create ORM identity or a shared database row.

### 21.6 Recurrence physical family contract — DB-U12 CLOSED

A persisted Recurrence is a scoped LR-05 definition, not a native owner and not a universal Rule root.

When Recurrence has independent history/reference because it governs canonical repeated generation/applicability, the concrete identity row is:

```text
dante.recurrence
  recurrence_ref uuid PRIMARY KEY
```

`recurrence_ref` is a UUIDv7 ScopedRecordRef. An applicable `dante.scoped_address` row uses scoped family `recurrence` when shared scoped/material addressing is required.

The accepted definition state uses facet:

```text
recurrence.definition
```

Common material-state header:

```text
dante.recurrence_state
  material_state_ref   uuid PRIMARY KEY
  recurrence_ref       uuid NOT NULL
  family_code          text NOT NULL
```

Constraints:

```text
material_state_ref
→ FK dante.material_state_address(material_state_ref)

recurrence_ref
→ FK dante.recurrence(recurrence_ref)
→ ON DELETE NO ACTION

family_code
→ CHECK IN (
    'calendar_wall_clock',
    'elapsed_interval',
    'quota_per_period',
    'completion_relative',
    'anchor_stream_relative',
    'cyclic_positional'
  )
```

A bounded deferred completeness constraint requires **exactly one** family payload row matching `family_code` by commit. No RRULE/provider string/JSON payload is canonical Recurrence truth.

#### Effective range / boundaries

Recurrence range semantics are represented separately from family parameters:

```text
dante.recurrence_effective_range_state
  material_state_ref          uuid PRIMARY KEY
  range_kind                  text NOT NULL
  expected_occurrence_count   integer NULL
```

`range_kind` is bounded to:

```text
open
until_boundary
expected_count
```

Checks enforce:

```text
expected_count
→ expected_occurrence_count > 0 and no until boundary

until_boundary
→ exactly one typed effective-until boundary exists

open
→ neither expected count nor effective-until boundary exists
```

Temporal boundaries use recurrence-specific typed rows rather than one generic temporal object:

```text
dante.recurrence_temporal_boundary_state
  material_state_ref   uuid NOT NULL
  boundary_role        text NOT NULL
  boundary_kind        text NOT NULL
  date_value           date NULL
  local_value          timestamp without time zone NULL
  zone_id              text NULL
  instant_value        timestamptz NULL

  PRIMARY KEY(material_state_ref, boundary_role)
```

`boundary_role` is bounded to the roles actually used by Recurrence such as:

```text
pattern_anchor
effective_from
effective_until
```

`boundary_kind` is a discriminated union:

```text
date
floating_local
named_zone_local
absolute_instant
```

Row-local CHECK constraints enforce the exact valid column combination. Named-zone values may carry a separate accepted resolved instant where consequence/history requires it under section 21.3.

A structural `this-and-future` revision may additionally bind the new recurrence state to the exact boundary Occurrence through an owner-specific typed revision/effect relation; it is not encoded by rewriting old states.

#### Family 1 — calendar / wall-clock

```text
dante.recurrence_calendar_state
  material_state_ref   uuid PRIMARY KEY
  frequency_code       text NOT NULL
  interval_count       integer NOT NULL
  clock_basis_code     text NOT NULL
  wall_time            time without time zone NULL
  zone_id              text NULL
  invalid_date_policy  text NULL
  dst_gap_policy       text NULL
  dst_overlap_policy   text NULL
```

Closed constraints:

```text
frequency_code     IN ('day','week','month','year')
interval_count     > 0
clock_basis_code   IN ('floating_local','named_zone','absolute')
named_zone         → zone_id required
floating/absolute  → zone_id absent unless the specific absolute pattern uses UTC as explicit frame
```

Normalized selectors:

```text
dante.recurrence_calendar_month_state
  material_state_ref uuid NOT NULL
  month_number       smallint NOT NULL CHECK 1..12
  PRIMARY KEY(material_state_ref, month_number)

dante.recurrence_calendar_month_day_state
  material_state_ref uuid NOT NULL
  month_day          smallint NOT NULL
  PRIMARY KEY(material_state_ref, month_day)
  CHECK month_day IN [-31..-1] OR [1..31]

dante.recurrence_calendar_weekday_state
  material_state_ref uuid NOT NULL
  weekday_number     smallint NOT NULL CHECK 1..7
  ordinal            smallint NULL
  CHECK ordinal IS NULL OR (ordinal BETWEEN -5 AND 5 AND ordinal <> 0)
  UNIQUE(material_state_ref, weekday_number, ordinal)
```

Positive/negative month-day and weekday ordinals preserve exact ordinal/last-position semantics; invalid-date and DST policy are explicit only when the pattern can encounter those conditions. No calendar-library default silently becomes canonical policy.

#### Family 2 — elapsed interval

```text
dante.recurrence_elapsed_interval_state
  material_state_ref   uuid PRIMARY KEY
  elapsed_seconds      numeric NOT NULL
  anchor_mode_code     text NOT NULL
  anchor_instant       timestamptz NULL
```

Constraints:

```text
elapsed_seconds finite AND > 0
anchor_mode_code IN ('fixed_anchor','previous_expected')
fixed_anchor      → anchor_instant required
previous_expected → anchor_instant is the initial seed only when explicitly established
```

Fixed elapsed seconds deliberately prevent `every 24 elapsed hours` from silently becoming calendar-day recurrence.

#### Family 3 — quota per period

```text
dante.recurrence_quota_state
  material_state_ref   uuid PRIMARY KEY
  quota_count          integer NOT NULL
  period_unit_code     text NOT NULL
  period_span          integer NOT NULL
  frame_code           text NOT NULL
  zone_id              text NULL
  week_start           smallint NULL
  anchor_date          date NULL
```

Constraints:

```text
quota_count      > 0
period_span      > 0
period_unit_code IN ('day','week','month','year')
frame_code       IN ('floating_local','named_zone','absolute')
named_zone       → zone_id required
week_start       → NULL unless period_unit_code='week'; otherwise CHECK 1..7
```

The period frame, not device/library locale, decides membership. The quota creates expected cardinality; no `slot_number`/ordinal is canonical for equivalent future slots unless another accepted relation gives them real order.

#### Family 4 — completion relative

```text
dante.recurrence_completion_relative_state
  material_state_ref       uuid PRIMARY KEY
  anchor_feature_code      text NOT NULL
  offset_kind              text NOT NULL
  elapsed_offset_seconds   numeric NULL
  calendar_offset_months   integer NULL
  calendar_offset_days     integer NULL
```

`anchor_feature_code` is a schema-owned Recurrence vocabulary identifying the qualifying established reality feature, for example an applicable actual completion/end feature; it is not arbitrary expression text.

Checks enforce exactly one offset representation:

```text
offset_kind='elapsed'
→ finite elapsed_offset_seconds > 0
→ calendar offsets NULL

offset_kind='calendar'
→ at least one non-zero calendar month/day component
→ elapsed offset NULL
```

The rule cannot silently substitute Schedule end for Actual/other qualifying reality. When no qualifying anchor exists, the next sequential expectation may remain undefined.

#### Family 5 — anchor-stream relative

```text
dante.recurrence_anchor_stream_state
  material_state_ref      uuid PRIMARY KEY
  anchor_family_code      text NOT NULL
  anchor_feature_code     text NOT NULL
  offset_kind             text NOT NULL
  elapsed_offset_seconds  numeric NULL
  calendar_offset_months  integer NULL
  calendar_offset_days    integer NULL
```

`anchor_family_code` and `anchor_feature_code` form a bounded Recurrence-specific Reference Contract over accepted qualifying anchor streams such as Session/Actual/Observation facets. They cannot encode arbitrary state predicates or downstream actions.

The same offset one-of invariant used by completion-relative recurrence applies. Qualifying-filter semantics that exceed this bounded anchor contract must be represented through another accepted typed Criterion/Policy/relation, never hidden in JSON or free-form SQL.

This preserves:

```text
anchor-stream recurrence
!= generic Trigger
!= Conditional Policy
```

#### Family 6 — cyclic positional

```text
dante.recurrence_cyclic_state
  material_state_ref   uuid PRIMARY KEY
  cycle_length         integer NOT NULL
  position_span        integer NOT NULL
  position_unit_code   text NOT NULL
```

Constraints:

```text
cycle_length       > 0
position_span      > 0
position_unit_code IN ('day','week','elapsed_interval')
```

Ordered positions are explicit:

```text
dante.recurrence_cycle_position_state
  material_state_ref   uuid NOT NULL
  position_index       integer NOT NULL
  generates_expected  boolean NOT NULL
  position_code        text NULL

  PRIMARY KEY(material_state_ref, position_index)
  CHECK position_index >= 0
```

A bounded deferred check requires positions to cover exactly `0 .. cycle_length-1` for the accepted state. `position_code` may carry owner-specific position semantics only when the source contract defines them; it is not a generic metadata payload.

#### Recurrence source binding

DANTE does not use:

```text
recurrence.owner_kind
recurrence.owner_id
```

A concrete source binds Recurrence through owner-specific typed relations/direct FKs. Current accepted Occurrence-generating native sources are Routine and recurring Event semantics. Repeated Temporal Constraint applicability may reuse Recurrence without generating Occurrences. Source cardinality is owned by the consuming concept and is not generalized into one polymorphic parent field.

#### Recurrence state/history

A structural rule change creates a new `recurrence.definition` MaterialStateRef and updates the explicit scoped current-state binding under the applicable expected-state rule. Historical states and already-distinguished Occurrences remain reconstructible under the state that governed them.

```text
Recurrence state v1
→ historical Occurrences retain v1 basis

Recurrence state v2
→ current/future generation follows v2 according to effective boundary
```

Purely virtual future candidates may be regenerated. An already materialized Occurrence with history is reconciled; it is never silently deleted/recreated because new expansion differs.

### 21.7 Capacity Claim disposition — DB-U16 CLOSED

Capacity Claim does **not** become one universal `capacity_claim`/`reservation` root merely because several resource contexts may commit capacity.

Closed disposition:

```text
Capacity Claim
→ LR-03 owner/context-specific qualified commitment relation
→ LR-02 + ScopedRecordRef only when material lifecycle/history/addressability requires it
→ NO native identity
→ NO universal Reservation root
```

A concrete material claim family must own exact:

```text
capacity-bearing target/reference contract
claiming purpose/context
quantity/capacity dimension where applicable
accepted temporal footprint
material Requirement/Allocation basis where applicable
Decision/Authority/Provenance basis where consequential
```

Historical temporal truth is preserved through either:

```text
claim → exact Schedule MaterialStateRef
```

or:

```text
claim-owned accepted temporal footprint/material state
```

according to the concrete claim family. A later Schedule move cannot make an old claim appear to have always occupied the new time.

Mandatory separations:

```text
Capacity Claim != Schedule
Capacity Claim != Resource Allocation
Capacity Claim != Actual utilization
Capacity Claim != Ownership / Possession
Capacity Claim != universal inventory/financial reservation
```

If no accepted capacity commitment exists, no ceremonial claim row is created.

### 21.8 Migration / mapping / direct-proof consequences of this pass

This design pass does not authorize CP6 business DDL. It fixes future materialization order and proof obligations.

Future CP6-04 migration grouping must respect at least:

```text
15 native owner identity shells
→ bounded native-address dispatcher update

recurrence scoped owner
→ scoped-address family update
→ material-state facet recurrence.definition
→ recurrence state header
→ six family payload tables + selector/boundary tables
→ current binding

Occurrence
→ occurrence_generation after native/material address prerequisites

Quantity/MonetaryAmount
→ columns/composites only inside real consuming state tables

Place
→ no spatial column/index in baseline migration

Capacity Claim
→ only inside first concrete owner/context family that actually owns the commitment
```

No table exists solely to make the future QA matrix green.

---

## 22. CP6-03 unresolved-parameter register

The following global/database parameters are closed:

```text
DB-U01 native_address topology                         CLOSED
DB-U02 scoped_address topology                         CLOSED
DB-U03 MaterialStateRef owner-address encoding         CLOSED
DB-U04 material facet representation                   CLOSED
DB-U05 current accepted-state binding topology         CLOSED
DB-U06 lineage topology                                CLOSED
DB-U07 typed chronology/temporal physical contract     CLOSED
DB-U11 Place/PostGIS mandatory-spatial disposition     CLOSED
DB-U12 Recurrence six-family physical contract         CLOSED
DB-U13 MonetaryAmount / Quantity physical values       CLOSED
DB-U16 Capacity Claim persistence disposition          CLOSED
```

The remaining questions are not generic “TBD” placeholders. Each has an explicit current disposition and closure condition.

| ID | Remaining parameter | Current reason / closure requirement |
|---|---|---|
| DB-U08 | final PostgreSQL object naming beyond currently frozen control/native/recurrence design names | freeze remaining concrete relation/context/state names with their object derivations before dictionary generation |
| DB-U09 | Account persistence | genuinely deferred: Domain keeps Account separate and detailed access model is not closed; do not invent login/account tables |
| DB-U10 | Principal/security persistence | genuinely deferred: AuthN/AuthZ independent registry not closed; preserve Actor/Person separation and later provenance binding |
| DB-U14 | owner/family-specific lifecycle/tombstone fields | derive actual retirement/redaction/delete continuity per owner/relation; no global deleted_at or tombstone semantic root |
| DB-U15 | remaining structural FK indexes and query indexes | final FK/query graph must justify each; preserve already-closed PK/UNIQUE/material owner-facet indexes and add none speculatively |
| DB-U17 | provider/integration object shapes | genuinely deferred until first concrete integration/provider contract |
| DB-U18 | idempotency table timing | genuinely deferred until first persistent material operation requiring reservation/replay semantics |
| DB-U19 | transactional outbox timing | genuinely deferred until first real Class-A async external effect |
| DB-U20 | derived/search/vector persisted structures | genuinely deferred until a real query/search/vector consumer proves materialization/index need |

```text
UNRESOLVED PARAMETERS CURRENT
9

UNCLASSIFIED PARAMETERS ALLOWED AT GATE 03
0
```

`GENUINELY DEFERRED` is a classified final CP6-03 disposition when current closed authority cannot truthfully determine a schema and the future trigger is explicit. It is not permission to create a placeholder table.

---

## 23. Next derivation pass — remaining concrete owner/context/relation contract

The next CP6-03 work continues in this same database specification; it does not create another methodology document and it does not reopen DB-U01..DB-U07/11/12/13/16.

Highest-value remaining work is now the concrete semantic payload/relation graph:

```text
owner-specific material state families actually required by the 15 LR-01 owners
Schedule / Actual / Outcome / Milestone contextual topology
Agreement + terms + assent
specific LR-03 relation endpoints/cardinalities
Temporal Constraint / Criterion / Availability / Resource Requirement structured families
governance state families
owner-specific lifecycle/tombstone semantics
remaining FK + structural index review
final stable names
Database Dictionary generation
```

For each remaining required/conditional family:

```text
1. consume complete canonical Domain + Logical authority
2. define exact table(s) and columns
3. define PK/FK/Reference Contract
4. define NULL/missingness semantics
5. define UNIQUE/CHECK/EXCLUDE/trigger integrity
6. define material-state/current/history behavior
7. define lifecycle/delete behavior
8. justify structural indexes
9. define SQLAlchemy mapping shape
10. define migration dependencies
11. define direct PostgreSQL tests
12. create/update Database Dictionary entry
13. close/update affected DB-U item
```

No object is called complete before that chain is satisfied.

---

## 24. Gate 03 acceptance contract

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
ACTIVE / PROGRESSIVE

57/57 TRACEABILITY
COMPLETE

PART-2 CROSS-CUTTING DISPOSITION
COMPLETE / UNCLASSIFIED 0

REFERENCE / MATERIAL-STATE CONTROL TOPOLOGY
DB-U01..DB-U06 CLOSED

LR-01 NATIVE IDENTITY-SHELL BASELINE
15 / 15 CLOSED

TEMPORAL / PLACE / RECURRENCE / VALUE / CAPACITY PASS
DB-U07 / DB-U11 / DB-U12 / DB-U13 / DB-U16 CLOSED

EXACT REMAINING SEMANTIC TABLE/COLUMN/CONSTRAINT BLUEPRINT
IN PROGRESS

UNRESOLVED DB-U ITEMS
9

GATE 03
NOT YET EARNED
```

No business migration, SQLAlchemy business mapping, persistence adapter, API or product vertical is authorized merely by this candidate blueprint.
