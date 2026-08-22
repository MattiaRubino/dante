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

`DB-U01` is therefore closed for address topology, but its destructive lifecycle path is explicitly dependent on `DB-U14`; topology closure is not permission to bypass owner/address continuity during deletion, retirement or redaction.

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

As with NativeRef, `DB-U02` is closed for the shared address topology while destructive lifecycle behavior remains dependent on `DB-U14`. A scoped semantic row may not disappear while a live address/history contract would thereby become false.

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

### 7.3 MaterialStateRef — owner-address and facet topology CLOSED / BIDIRECTIONAL COMPLETENESS HARDENED

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

The payload relation is a **total 1:1 contract for a live material state**, not merely an insertion-time convention.

The database must enforce both directions:

```text
live material_state_address
→ exactly one matching owner/facet payload exists by COMMIT

live owner/facet payload
→ exactly one matching material_state_address exists

ordinary payload DELETE
→ MUST NOT leave a live MaterialStateRef resolving to no semantic payload

ordinary address DELETE
→ MUST NOT bypass surviving payload/current/history references
```

A narrow deferred constraint trigger on the address/control side permits the address row and payload row to be inserted in the same transaction and requires the complete live state to exist by commit. A paired payload-side deferred integrity check/guard must also reject deletion or mutation that would leave a live address incomplete. Payload-side validation rejects wrong owner/facet immediately or at the selected constraint boundary.

Privacy/redaction/retention **does not create an exception to MaterialStateRef totality**. `DB-U14` may later define which protected fields are removed, replaced or rendered unavailable and what minimal owner-specific redacted/tombstone representation survives, but a live `material_state_ref` MUST still resolve to exactly one valid owner/facet persistence representation. `DB-U14` therefore chooses the truthful surviving representation; it never authorizes `material_state_address` to remain live while its semantic payload disappears completely. Until that lifecycle path is closed, direct ordinary runtime deletion of a material-state payload is not an accepted operation.

This hardening preserves the closed DB-U03/DB-U04 topology; it closes a missing **bidirectional completeness invariant** rather than introducing a new semantic state root.

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
direct payload delete leaving live address                REJECT by commit
address delete with surviving payload/current/history     REJECT
attempt to mutate state address owner/facet/ref            REJECT
governed redaction/tombstone                              preserves one resolvable owner-specific representation under DB-U14
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

The live address↔payload relationship is bidirectionally complete under section 7.3. A material payload cannot be removed as ordinary cleanup while its MaterialStateRef remains live, and a control address cannot be used to represent an owner/facet state whose semantic payload does not exist. Governed redaction may remove protected fields only while preserving an owner-specific redacted/tombstone representation that keeps the MaterialStateRef resolvable and truthful.

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

Exact numeric/temporal value contracts are closed in section 21. The six Recurrence semantic families are retained, but their final owner/scoped persistence boundary and remaining exact recurrence constraints are reopened under `DB-U12` by the whole-blueprint audit. Place spatial shape remains intentionally absent from the mandatory Place identity row; PostGIS activation is trigger-bound as specified there.

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

## 13. Transaction, concurrency and database privilege contract

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
→ bidirectional deferred completeness checks fire no later than COMMIT
→ current binding may be inserted/updated after the complete state exists
```

A `DEFERRABLE INITIALLY DEFERRED` **constraint trigger** is permitted for the address→payload completeness invariant because the two rows are intentionally created in one transaction and PostgreSQL permits constraint-trigger execution at transaction end. The payload side must carry the complementary deletion/completeness protection so a live MaterialStateRef cannot be orphaned by deleting only its semantic payload. Ordinary direct FKs remain immediate unless a concrete transaction genuinely requires deferral.

### 13.2 Object privilege topology — DB-U21 OPEN / BLOCKER BEFORE CP6-04

The real CP3 provisioning currently grants `dante_runtime` broad `SELECT, INSERT, UPDATE, DELETE` on all existing/future tables, `USAGE` on all existing/future sequences, and default `USAGE` on types in schema `dante`; it also revokes default routine execution from `PUBLIC`. That was an acceptable technical-foundation posture while no DANTE business objects existed. It is **not** sufficient for the concrete database now being designed because several accepted structures are immutable-by-policy, control-only or should not be executable/usable by runtime merely because they exist.

Gate 03 must therefore produce an exact per-object privilege matrix across the PostgreSQL object classes that can affect runtime authority:

```text
tables / partitioned tables where ever introduced
views / materialized views when introduced
sequences / identity helpers when genuinely required
types / domains owned by DANTE
routines / functions / procedures
schema usage and migration-history boundaries
```

Minimum class posture to close:

```text
native/scoped/material address-control rows
→ runtime SELECT + INSERT as required by accepted writes
→ ordinary UPDATE/DELETE denied by default

accepted immutable-by-policy material-state payload rows
→ runtime SELECT + INSERT as required
→ ordinary UPDATE denied
→ ordinary DELETE denied; DB-U14 may expose only a narrower governed redaction mechanism while preserving MaterialStateRef totality

current accepted-state bindings
→ runtime SELECT + INSERT + UPDATE as required by accepted-state replacement
→ DELETE only where the exact owner lifecycle proves it

native/contextual/relation owner rows
→ exact DML by concrete lifecycle; never inherited mechanically from one blanket all-table grant

views / materialized views
→ runtime SELECT only when they are an accepted runtime read surface
→ no privilege by symmetry

sequences
→ runtime USAGE/SELECT only when a concrete runtime write path actually consumes that sequence
→ UUIDv7 semantic IDs do not justify blanket sequence access

types / domains
→ runtime USAGE only for concrete types/domains required by runtime-accessible objects
→ no blanket grant merely because a type exists in schema dante

routines
→ no runtime EXECUTE by default
→ trigger-backed integrity does not justify exposing a callable runtime API
→ any explicit runtime-callable routine requires a concrete contract, least-privilege review and direct tests

migration history / DDL / ownership
→ remains unavailable to dante_runtime
```

This is a **design class baseline**, not permission to grant privileges mechanically. Every concrete object still receives its exact least-privilege entry.

The post-repair audit fixes the privilege-ownership direction for CP6-04:

```text
PROVISIONING
→ owns cluster/database role creation, credentials, schema ownership/usage foundation and safe PUBLIC revokes
→ MUST NOT act as a blanket business-object ACL reconciler
→ MUST NOT install broad future-business default DML/sequence/type/routine grants

ALEMBIC BUSINESS MIGRATION
→ creates/changes a concrete DANTE business/control object
→ grants/revokes the exact approved runtime privileges for that object in the same reviewed schema change
→ updates the Database Dictionary privilege record in the same change
```

Existing CP3 broad defaults/all-object reconciliation must therefore be removed or narrowed during CP6-04 before the business schema is considered safe. Re-running provisioning after CP6-04 must be idempotent **without changing the approved ACLs of existing business objects** and without causing future business objects to inherit broad privileges automatically.

Gate-03 privilege closure therefore requires:

```text
complete object-level runtime privilege matrix
+
provisioning role/schema-foundation design with no blanket business ACL authority
+
migration-owned exact ACL application design for tables/views/sequences/types/domains/routines
+
proof that repeated provisioning cannot broaden those ACLs
```

No `SECURITY DEFINER` or alternate privileged mutation path is introduced merely to evade this matrix. Any later exceptional controlled routine requires the existing Constitution gate and explicit security tests.

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
| Recurrence | six typed structured recurrence families; **owner-bound by default when independent addressability/lifecycle is absent; independently scoped only when justified** | REQUIRED where accepted canonical recurrence is persisted | no RRULE/provider-string canonical kernel; six semantic families retained; DB-U12 physical ownership/constraint boundary REOPENED |
| Resource Requirement | structured requirement specification | REQUIRED where accepted | contextual address only where justified |
| Temporal Constraint | structured temporal constraint family | REQUIRED | distinct from Schedule |

Recurrence therefore follows the same anti-inflation rule as other LR-05 structures: persistence of a rule does not automatically manufacture an independently addressable contextual identity.

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
| 43 | Recurrence | LR-05 | typed structured recurrence persisted owner-bound unless independent scoped addressability/lifecycle is justified; six semantic families retained; DB-U12 physical contract under hardening |
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
| MaterialStateRef | MATERIALIZE IN CP6 | `material_state_address` owner-space/facet topology CLOSED + owner-specific state rows; live address↔payload totality is bidirectional and survives redaction through an owner-specific resolvable representation |
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
| Tombstone/retirement/redaction continuity | MATERIALIZE IN CP6 where owner lifecycle requires it | owner-specific/minimal continuity; NO generic semantic Tombstone owner; must close owner↔address and material-address↔owner-specific redacted/tombstone representation without breaking MaterialStateRef totality |
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
   + paired deferred live address↔payload completeness constraints
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
9. OBJECT PRIVILEGE CLOSURE + APPLICATION
   exact per-object dante_runtime matrix across tables/views/sequences/types/domains/routines
   provisioning narrowed to role/schema foundation without blanket business ACL reconciliation
   migration-owned exact GRANT/REVOKE for each concrete object
        ↓
10. PROVIDER / DERIVED / SPECIALIST STRUCTURES
   only where closed authority and real trigger justify materialization
        ↓
11. DOCUMENTATION + INTROSPECTION QA
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
→ satisfy bidirectional deferred live-state completeness by COMMIT
→ create/update explicit current binding where required
```

This pattern preserves:

```text
concrete semantic owner remains authoritative
address exists only for a real owner
live MaterialStateRef resolves to one exact semantic payload
no universal Entity/Thing row
no application-only referential integrity
```

### 17.2 Restore / bulk-load validation implication

Custom cross-table trigger enforcement is not a replacement for restore/evolution QA. CP6-05 must include explicit integrity scans that can prove after migration/restore-style loading that:

```text
no native/scoped address is orphaned or family-mismatched
no live material_state_address lacks/mismatches its owner-specific payload or redacted/tombstone representation
no payload exists without its matching material_state_address
no current binding mismatches owner/facet/state
```

Destructive backup/restore evidence itself remains staged under HG-09/HG-12/PSV as already defined.

### 17.3 Recurrence sub-DAG — ownership boundary REOPENED UNDER DB-U12

The six accepted Recurrence semantic families remain intact, but the whole-blueprint audit rejected the assumption that every persisted Recurrence must first become an independently scoped record.

Two physical ownership paths must be supported truthfully:

```text
A. OWNER-BOUND RECURRENCE
concrete Routine / recurring Event / Temporal Constraint / another accepted source
→ recurrence semantics persist as a typed source-owned material facet/state
→ no independent recurrence ScopedRecordRef unless another contract requires it
→ six family-specific typed payload shapes apply
→ Occurrence generation binds the exact governing recurrence material state

B. INDEPENDENTLY SCOPED RECURRENCE
independent addressability / reuse / cross-reference / reconciliation / lifecycle-history is actually justified
→ recurrence scoped owner
→ scoped_address
→ recurrence.definition MaterialStateRef
→ six family-specific typed payload shapes apply
→ explicit current recurrence.definition binding where singular currentness is required
→ Occurrence generation binds that exact governing recurrence material state
```

The source-specific ownership/cardinality remains owned by the consuming concept. No generic `owner_kind + owner_id` recurrence root is introduced.

DB-U12 must reclose the exact common header/FK/facet topology so both modes use one coherent, enforceable design without promoting ordinary source-owned recurrence into a ceremonial entity.

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

Recurrence mapping follows the **revalidated owner-bound versus independently scoped boundary while DB-U12 remains open**. Owner-bound recurrence state maps as part of the concrete source/state persistence family; an independently addressable Recurrence may map to its own scoped row only when the LR-05 addressability/lifecycle threshold justifies it. The exact common header and family mapping are not frozen until DB-U12 recloses. In both modes family dispatch remains explicit typed persistence logic, not SQLAlchemy polymorphic semantic inheritance and not a generic Rule model.

Each final Database Dictionary entry will point to its SQLAlchemy mapping when one exists.

Views/generated/projection objects do not require ORM classes merely for symmetry.

---

## 19. Direct PostgreSQL proof plan — current

CP6-03 must end with an exact test matrix. Current required categories include:

### 19.1 Foundation / schema alignment / privileges

```text
fresh database → Alembic head
single canonical Alembic head
SQLAlchemy metadata vs Alembic/PostgreSQL drift
role ownership/grants
runtime DDL denial
Database Dictionary object coverage
per-object dante_runtime privilege matrix matches the approved blueprint across tables/views/sequences/types/domains/routines
runtime UPDATE/DELETE denied on immutable/control objects where not explicitly authorized
runtime sequence/type/routine privileges absent unless the exact object contract requires them
new business objects do not inherit blanket runtime DML/USAGE/EXECUTE through default privileges
re-running provisioning/reconciliation does not broaden any approved business-object ACL
migration-created business objects receive their exact approved ACL in the same schema change
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
payload delete leaving a live MaterialStateRef rejected by commit
payload without matching material-state address rejected
wrong owner rejected
wrong facet rejected
current binding points to valid same-owner/same-facet accepted state
one current state per owner/facet enforced
one MaterialStateRef cannot be current for another owner/facet
correction creates new state rather than silent overwrite
owner-specific typed lineage rejects wrong-owner/facet links
historical state remains reconstructible
governed redaction/tombstone preserves a resolvable owner-specific state representation and permitted continuity under DB-U14
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
calendar recurrence keeps wall-clock/zone semantics only through an explicitly accepted DST policy where that pressure exists
calendar recurrence has no placeholder/free-text policy field standing in for an unclosed invalid-date/DST vocabulary
calendar weekday selector rejects duplicate non-ordinal weekday rows through NULLS NOT DISTINCT uniqueness
quota recurrence preserves explicit period frame and does not invent ordinal quota identity
completion-relative recurrence cannot generate the next chain without a qualifying anchor when the rule requires one
anchor-stream recurrence keeps qualifying anchor contract distinct from generic Trigger
cyclic recurrence preserves position/cycle semantics and an explicit phase basis where required
exactly one recurrence family payload per material recurrence state
family discriminator/payload mismatch rejected
owner-bound recurrence does not manufacture a scoped recurrence identity
independently scoped recurrence exists only when its addressability/lifecycle contract is justified
historical Occurrence binds the exact governing recurrence material state in either ownership mode
governing recurrence material state is valid for the concrete source
governing source MaterialStateRef, when separately material, cannot be confused with governing Recurrence state
unordered quota slots do not gain fake ordinal identity
pattern/effective boundaries preserve exact accepted temporal meaning
calendar-relative completion/anchor offsets do not silently inherit an unspecified frame/zone
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
native/scoped owner ↔ address continuity remains truthful under DB-U14
MaterialStateRef totality remains true through redaction/tombstone; no live address resolves to missing semantic representation
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

The 15 native owner identity-table names are stable design names. The six Recurrence semantic families are stable, but the exact Recurrence persistence object names/header ownership are **not frozen** until DB-U12 recloses the owner-bound versus independently scoped topology. Dictionary materialization still waits for the remaining object-level table/column graph so one coherent dictionary is generated rather than a sequence of partial files.

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
privileges, including related view/sequence/type/domain/routine ACL where applicable
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

### 21.2 Occurrence generation-context requirement — RECURRENCE OWNER MODE HARDENED

A materialized `Occurrence` must retain enough generation context to explain why that expected instance exists under the exact governing source/rule state.

The companion family remains conceptually:

```text
dante.occurrence_generation
  occurrence_ref                       uuid PRIMARY KEY
  source_native_ref                    uuid NOT NULL
  governing_recurrence_state_ref       uuid NOT NULL
  governing_source_state_ref           uuid NULL
```

Constraints that remain closed:

```text
occurrence_ref
→ FK dante.occurrence(occurrence_ref)
→ ON DELETE NO ACTION

source_native_ref
→ FK dante.native_address(native_ref)
→ ON DELETE NO ACTION
→ current accepted generation-source eligibility: routine OR event

governing_recurrence_state_ref
→ FK dante.material_state_address(material_state_ref)
→ ON DELETE NO ACTION
→ MUST resolve to the exact material state that contains the governing Recurrence semantics
→ MUST be valid for source_native_ref under the concrete source/recurrence ownership contract

governing_source_state_ref
→ FK dante.material_state_address(material_state_ref)
→ ON DELETE NO ACTION when present
→ MUST belong to source_native_ref and an explicitly generation-relevant source facet
```

The former stricter assumption that every `governing_recurrence_state_ref` must be facet `recurrence.definition` owned by a separate scoped Recurrence is superseded. Under DB-U12 reclosure the governing state may be either:

```text
owner-bound source Recurrence material facet/state
OR
independently scoped Recurrence definition state
```

A bounded database eligibility check must validate whichever mode the source contract uses. The two MaterialStateRefs remain deliberately separate: the exact state carrying the Recurrence definition is not silently conflated with another optional material Routine/Event source state that also affected generation.

If a later accepted generative source family is added, its eligibility is a reviewed schema change.

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
→ pattern anchor/effective range belong to the exact source-owned or independently scoped Recurrence material state
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

`unit_code` is a normalized semantic token owned/validated by the consuming quantity-kind contract, not an arbitrary display label. Where a standard unit vocabulary is adopted later, that is a bounded vocabulary decision; custom units requiring conversion/versioning do not gain a fake global conversion rule.

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

### 21.6 Recurrence physical family contract — DB-U12 REOPENED / SIX SEMANTIC FAMILIES RETAINED

The whole-blueprint audit found that the earlier physical closure made one assumption stronger than the closed Domain/Logical authority permits:

```text
persisted canonical Recurrence
→ always independent recurrence row
→ always ScopedRecordRef
→ always scoped_address
→ always recurrence.definition MaterialStateRef
```

That implication is **not** accepted.

Closed upstream authority instead requires:

```text
Recurrence
→ LR-05 structured rule/specification
→ ScopedRecordRef only when independent addressability/history/reconciliation/cross-reference is justified
→ material state when historical/consequential meaning requires exact rule state
```

Therefore the six semantic families below remain valid, but the physical ownership envelope is now explicitly split.

#### Mode A — owner-bound Recurrence — DEFAULT WHEN NO INDEPENDENT ADDRESSABILITY EXISTS

A Recurrence that is only a structured part of an accepted source policy/state is persisted as a typed material facet/state of that concrete owner/context.

Examples of current pressure:

```text
Routine recurrence policy
recurring Event recurrence policy
Temporal Constraint repeated applicability
```

In this mode:

```text
no dante.recurrence row merely for storage uniformity
no recurrence ScopedRecordRef merely for storage uniformity
no scoped_address merely because the rule is material
MaterialStateRef owner = the concrete native/scoped source that owns the material recurrence facet
family payload remains typed and exact
historical Occurrence can bind that exact governing recurrence material state
```

The exact facet code is owner-qualified and frozen with the concrete source family, for example a future `routine.recurrence`-style code if that is the accepted Routine state decomposition. The example is not itself a prematurely frozen table/facet name.

#### Mode B — independently scoped Recurrence — ONLY WHEN JUSTIFIED

A Recurrence receives its own scoped identity only when a concrete contract proves one or more of:

```text
independent addressability
reuse by multiple owning contexts where one shared rule identity is semantically real
cross-record reference to the rule itself
independent reconciliation
independent lifecycle/history distinct from the containing source
```

Only then is the earlier scoped shape admissible:

```text
dante.recurrence
  recurrence_ref uuid PRIMARY KEY

recurrence_ref
→ UUIDv7 ScopedRecordRef
→ matching scoped_address family recurrence

material Recurrence definition
→ MaterialStateRef owned by that scoped Recurrence
→ facet recurrence.definition
```

This is an escalation path, not the baseline representation of every canonical recurrence rule.

#### Shared typed family payload contract — RETAINED / EXACT HEADER TO BE RECLOSED

The six accepted semantic families remain:

```text
calendar_wall_clock
elapsed_interval
quota_per_period
completion_relative
anchor_stream_relative
cyclic_positional
```

No RRULE/provider string/JSON payload is canonical Recurrence truth.

A material recurrence state still requires one explicit family discriminator and exactly one family-specific typed payload by COMMIT. What is reopened is the exact common header/FK topology that must support both owner-bound and independently scoped modes without introducing a generic semantic Rule root.

The earlier mandatory header:

```text
dante.recurrence_state(material_state_ref, recurrence_ref, family_code)
```

is therefore **not implementation-frozen** because mandatory `recurrence_ref` would reintroduce the rejected identity inflation. DB-U12 reclosure must choose the exact header decomposition and facet/owner validation for both modes.

The family-specific structures below remain **candidate typed payload pressure**, not blanket implementation authorization. A candidate field whose value requires a semantic policy/vocabulary that closed authority has not yet fixed does not become a nullable text escape hatch, free-form code, placeholder enum or “decide later” JSON field merely to make the table executable. Gate 03 must either derive the exact semantics/vocabulary or leave that field/variant unauthorized until its explicit closure trigger exists.

This applies especially to:

```text
invalid-date behavior
DST-gap behavior
DST-overlap behavior
calendar-relative frame/zone behavior
pattern/cycle phase requirements
qualifying-anchor vocabularies
```

The anti-placeholder rule is:

```text
closed semantic vocabulary / invariant
→ exact typed column + CHECK/FK/trigger contract may be frozen

semantic vocabulary / invariant still open
→ candidate pressure remains documented
→ no free-text policy column
→ no generic policy_code placeholder
→ no JSON semantic escape hatch
→ no invented enum values
```

#### Effective range / boundaries — RETAINED SHAPE, CONSTRAINT HARDENING REQUIRED

Recurrence range semantics remain separate from family parameters.

Candidate shape:

```text
dante.recurrence_effective_range_state
  material_state_ref          uuid PRIMARY KEY
  range_kind                  text NOT NULL
  expected_occurrence_count   integer NULL
```

`range_kind` remains bounded to:

```text
open
until_boundary
expected_count
```

Required semantics remain:

```text
expected_count
→ expected_occurrence_count > 0 and no effective_until boundary

until_boundary
→ expected_occurrence_count IS NULL
→ exactly one typed effective_until boundary exists by COMMIT

open
→ expected_occurrence_count IS NULL
→ no effective_until boundary exists
```

Candidate recurrence-specific temporal boundary row:

```text
dante.recurrence_temporal_boundary_state
  material_state_ref   uuid NOT NULL
  boundary_role        text NOT NULL
  boundary_kind        text NOT NULL
  date_value           date NULL
  local_value          timestamp without time zone NULL
  zone_id              text NULL
  instant_value        timestamptz NULL
  resolved_at          timestamptz NULL   -- only when an accepted named-zone resolution is materially required

  PRIMARY KEY(material_state_ref, boundary_role)
```

`boundary_role` pressure remains:

```text
pattern_anchor
effective_from
effective_until
```

`boundary_kind` remains:

```text
date
floating_local
named_zone_local
absolute_instant
```

Row-local combination semantics remain:

```text
date             → date_value only
floating_local   → local_value only
named_zone_local → local_value + zone_id; resolved_at only when the accepted resolution itself is material
absolute_instant → instant_value only
```

DB-U12 reclosure must make exact which recurrence families/parameter combinations **require** `pattern_anchor` rather than treating it as optional. At minimum, any multi-period/cyclic pattern whose phase cannot be determined from its selectors/frame must not fall back to source `created_at` or another hidden default.

#### Family 1 — calendar / wall-clock — SEMANTIC SHAPE RETAINED

Candidate payload pressure:

```text
dante.recurrence_calendar_state
  material_state_ref   uuid PRIMARY KEY
  frequency_code       text NOT NULL
  interval_count       integer NOT NULL
  clock_basis_code     text NOT NULL
  wall_time            time without time zone NULL
  zone_id              text NULL
  invalid_date_policy  <NOT IMPLEMENTATION-AUTHORIZED UNTIL VOCABULARY CLOSES>
  dst_gap_policy       <NOT IMPLEMENTATION-AUTHORIZED UNTIL VOCABULARY CLOSES>
  dst_overlap_policy   <NOT IMPLEMENTATION-AUTHORIZED UNTIL VOCABULARY CLOSES>
```

Closed constraints retained:

```text
frequency_code     IN ('day','week','month','year')
interval_count     > 0
clock_basis_code   IN ('floating_local','named_zone','absolute_utc')
named_zone         → zone_id required
floating_local     → zone_id absent
absolute_utc       → zone_id absent; UTC basis is intrinsic to the code
```

Normalized selector pressure remains:

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
  UNIQUE NULLS NOT DISTINCT (material_state_ref, weekday_number, ordinal)
```

`NULLS NOT DISTINCT` remains deliberate PostgreSQL 18 behavior for duplicate non-ordinal weekday prevention.

Not yet closed under DB-U12:

```text
exact accepted invalid_date_policy vocabulary
exact accepted dst_gap_policy vocabulary
exact accepted dst_overlap_policy vocabulary
exact selector-combination validity beyond scalar ranges
exact pattern_anchor requirement for interval_count / selector combinations
exact historical named-zone boundary resolution placement where materially consequential
```

No calendar-library default may silently supply any of those semantics, and no policy field is materialized merely to hold an unknown future answer.

#### Family 2 — elapsed interval — SEMANTIC SHAPE RETAINED

Candidate payload:

```text
dante.recurrence_elapsed_interval_state
  material_state_ref   uuid PRIMARY KEY
  elapsed_seconds      numeric NOT NULL
  anchor_mode_code     text NOT NULL
  anchor_instant       timestamptz NULL
```

Retained constraints:

```text
elapsed_seconds finite AND > 0
anchor_mode_code IN ('fixed_anchor','previous_expected')
fixed_anchor      → anchor_instant required
previous_expected → anchor_instant is the initial seed only when explicitly established
```

Fixed elapsed seconds deliberately prevent `every 24 elapsed hours` from silently becoming calendar-day recurrence.

#### Family 3 — quota per period — SEMANTIC SHAPE RETAINED

Candidate payload:

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

Retained constraints:

```text
quota_count      > 0
period_span      > 0
period_unit_code IN ('day','week','month','year')
frame_code       IN ('floating_local','named_zone','absolute_utc')
named_zone       → zone_id required
other frames     → zone_id absent
period_unit='week' → week_start required AND CHECK 1..7
other period units → week_start NULL
period_span > 1    → explicit phase/anchor required; candidate anchor_date remains one possible encoding
```

The period frame, not device/library locale, decides membership. The quota creates expected cardinality; no `slot_number`/ordinal is canonical for equivalent future slots unless another accepted relation gives them real order.

DB-U12 must verify that `anchor_date` is sufficient for every admitted multi-period frame rather than retaining it merely because it is convenient SQL.

#### Family 4 — completion relative — SEMANTIC FAMILY RETAINED / CALENDAR FRAME NOT YET CLOSED

Candidate payload pressure:

```text
dante.recurrence_completion_relative_state
  material_state_ref       uuid PRIMARY KEY
  anchor_feature_code      text NOT NULL
  offset_kind              text NOT NULL
  elapsed_offset_seconds   numeric NULL
  calendar_offset_months   integer NULL
  calendar_offset_days     integer NULL
  <calendar-frame/zone basis if calendar offset is admitted>
```

`anchor_feature_code` remains a schema-owned Recurrence vocabulary identifying the qualifying established reality feature; it is not arbitrary expression text. The exact accepted vocabulary must be derived from the admitted anchor contract before implementation; it is not a free-text placeholder.

Closed portion:

```text
offset_kind='elapsed'
→ finite elapsed_offset_seconds > 0
→ calendar offsets absent
```

Calendar-relative offsets remain semantically valid upstream, but CP6-03 has **not yet closed** the exact frame/zone basis required to make “+N calendar months/days” deterministic across local/named-zone/absolute anchor contexts. Therefore the calendar-offset columns are not implementation-authorized until DB-U12 closes that basis.

The rule cannot silently substitute Schedule end for Actual/other qualifying reality. When no qualifying anchor exists, the next sequential expectation may remain undefined.

#### Family 5 — anchor-stream relative — SEMANTIC FAMILY RETAINED / CALENDAR FRAME NOT YET CLOSED

Candidate payload pressure:

```text
dante.recurrence_anchor_stream_state
  material_state_ref      uuid PRIMARY KEY
  anchor_family_code      text NOT NULL
  anchor_feature_code     text NOT NULL
  offset_kind             text NOT NULL
  elapsed_offset_seconds  numeric NULL
  calendar_offset_months  integer NULL
  calendar_offset_days    integer NULL
  <calendar-frame/zone basis if calendar offset is admitted>
```

`anchor_family_code` and `anchor_feature_code` remain a bounded Recurrence-specific Reference Contract over accepted qualifying anchor streams such as Session/Actual/Observation facets. Their exact accepted vocabulary must close with that Reference Contract before implementation. They cannot encode arbitrary state predicates or downstream actions and cannot survive as unconstrained free-text placeholders.

Elapsed-offset constraints mirror the completion-relative family. Calendar offsets have the same unresolved deterministic frame/zone requirement and are not implementation-authorized until DB-U12 recloses it.

Qualifying-filter semantics that exceed the bounded anchor contract must be represented through another accepted typed Criterion/Policy/relation, never hidden in JSON or free-form SQL.

This preserves:

```text
anchor-stream recurrence
!= generic Trigger
!= Conditional Policy
```

#### Family 6 — cyclic positional — SEMANTIC SHAPE RETAINED / PHASE REQUIREMENT HARDENED

Candidate payload:

```text
dante.recurrence_cyclic_state
  material_state_ref   uuid PRIMARY KEY
  cycle_length         integer NOT NULL
  position_span        integer NOT NULL
  position_unit_code   text NOT NULL
```

Retained constraints:

```text
cycle_length       > 0
position_span      > 0
position_unit_code IN ('day','week')
```

A cyclic pattern **must have an explicit phase/anchor basis** sufficient to determine which cycle position applies. The earlier candidate did not encode that requirement and therefore was not implementation-deterministic. DB-U12 must close its exact typed representation; `created_at` is forbidden as an implicit phase anchor.

The currently accepted cyclic examples are calendar-position cycles (`2 days on / 2 days off`, week rotations). A future truly elapsed sub-day cycle must be reviewed explicitly rather than overloading `position_span` with an unspecified elapsed unit; the existing elapsed-interval family remains available for pure fixed-duration repetition.

Ordered position pressure remains:

```text
dante.recurrence_cycle_position_state
  material_state_ref   uuid NOT NULL
  position_index       integer NOT NULL
  generates_expected  boolean NOT NULL
  position_code        text NULL

  PRIMARY KEY(material_state_ref, position_index)
  CHECK position_index >= 0
```

A bounded deferred check still needs to require positions to cover exactly `0 .. cycle_length-1` for an accepted state. `position_code` may carry owner-specific position semantics only when the source contract defines them; it is not a generic metadata payload.

#### Recurrence source binding — CURRENT RULE

DANTE still does not use:

```text
recurrence.owner_kind
recurrence.owner_id
```

Source ownership/cardinality is explicit in the consuming family.

```text
owner-bound mode
→ source directly owns the material recurrence facet/state

independent scoped mode
→ source has an explicit typed relation/FK to the independently addressable Recurrence
```

Current accepted Occurrence-generating native sources remain Routine and recurring Event semantics. Repeated Temporal Constraint applicability may reuse Recurrence without generating Occurrences. A later source addition is a reviewed schema/reference-contract change.

#### Recurrence state/history — CURRENT RULE

A structural rule change always creates a new exact material recurrence state when history/consequence requires it. What changes with this audit is **who owns that state**, not whether material history is preserved.

```text
owner-bound recurrence state v1
→ historical Occurrences retain v1 basis
→ structural revision creates source-owned recurrence state v2

independently scoped recurrence state v1
→ historical Occurrences retain v1 basis
→ structural revision creates scoped recurrence.definition state v2
```

Purely virtual future candidates may be regenerated. An already materialized Occurrence with history is reconciled; it is never silently deleted/recreated because new expansion differs.

#### DB-U12 exact reclosure requirements

DB-U12 may return to `CLOSED` only when all of the following are deterministic:

```text
owner-bound vs independently scoped persistence topology
exact common family discriminator/header decomposition
exact material facet codes and owner/family eligibility for each admitted source mode
exact source↔recurrence ownership/cardinality per currently accepted source family
pattern_anchor requirement by recurrence family/parameter combination
exact calendar selector-combination validity
exact invalid-date policy vocabulary
exact DST gap policy vocabulary
exact DST overlap policy vocabulary
named-zone boundary accepted-resolution placement where consequential
completion-relative calendar-offset frame/zone semantics
anchor-stream calendar-offset frame/zone semantics
cyclic phase/anchor representation
exact qualifying-anchor vocabularies where persisted
family payload totality/exclusivity constraints
zero free-text/placeholder/JSON policy fields for semantics not yet closed
Occurrence governing-state eligibility across both ownership modes
SQLAlchemy mapping shape for both modes
migration ordering and privilege matrix entries
direct positive/negative PostgreSQL tests
```

Until those close, the six semantic families are authoritative but the prior `DB-U12 CLOSED` physical claim is superseded.

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

### 21.8 Migration / mapping / direct-proof consequences of this pass — AUDIT HARDENED

This design pass does not authorize CP6 business DDL. It fixes future materialization order and proof obligations.

Future CP6-04 migration grouping must respect at least:

```text
15 native owner identity shells
→ bounded native-address dispatcher update

material recurrence state
→ owner-bound path by default when no independent Recurrence addressability exists
→ independently scoped Recurrence path only when exact LR-05 addressability/lifecycle trigger is proven
→ six typed family payloads only after DB-U12 recloses exact header/facet/constraint/policy topology
→ no placeholder policy columns are materialized to stand in for unclosed semantics

Occurrence
→ occurrence_generation after native/material address prerequisites
→ governing recurrence state valid in either accepted ownership mode

Quantity/MonetaryAmount
→ columns/composites only inside real consuming state tables

Place
→ no spatial column/index in baseline migration

Capacity Claim
→ only inside first concrete owner/context family that actually owns the commitment

object privileges
→ provisioning narrowed to role/schema foundation
→ CP3 blanket runtime DML/sequence/type grants removed or narrowed before business-object safety is claimed
→ each business/control migration owns exact approved table/view/sequence/type/domain/routine ACLs in the same change
```

No table exists solely to make the future QA matrix green.

---

## 22. CP6-03 unresolved-parameter register — WHOLE-BLUEPRINT AUDIT HARDENED

The following global/database parameters remain closed after the audit:

```text
DB-U01 native_address topology                         CLOSED / lifecycle path depends on DB-U14
DB-U02 scoped_address topology                         CLOSED / lifecycle path depends on DB-U14
DB-U03 MaterialStateRef owner-address encoding         CLOSED / bidirectional totality hardened; redaction cannot break totality
DB-U04 material facet representation                   CLOSED / bidirectional totality hardened; redaction cannot break totality
DB-U05 current accepted-state binding topology         CLOSED
DB-U06 lineage topology                                CLOSED
DB-U07 typed chronology/temporal physical contract     CLOSED
DB-U11 Place/PostGIS mandatory-spatial disposition     CLOSED
DB-U13 MonetaryAmount / Quantity physical values       CLOSED
DB-U16 Capacity Claim persistence disposition          CLOSED
```

The whole-blueprint audit **reopened DB-U12 only at the physical ownership/constraint level**. The targeted post-repair revalidation confirmed that owner-bound-by-default / independently-scoped-when-justified is aligned with Domain, Logical, Physical and CP6-01. The six accepted Recurrence semantic families remain closed upstream and are not being semantically redesigned.

The remaining questions are not generic “TBD” placeholders. Each has an explicit current disposition and closure condition.

| ID | Remaining parameter | Current reason / closure requirement |
|---|---|---|
| DB-U08 | final PostgreSQL object naming beyond currently frozen control/native design names | freeze remaining concrete relation/context/state names with their object derivations before dictionary generation; Recurrence object names wait for DB-U12 reclosure |
| DB-U09 | Account persistence | genuinely deferred: Domain keeps Account separate and detailed access model is not closed; do not invent login/account tables |
| DB-U10 | Principal/security persistence | genuinely deferred: AuthN/AuthZ independent registry not closed; preserve Actor/Person separation and later provenance binding |
| DB-U12 | Recurrence physical ownership + exact constraint contract | REOPENED by whole-blueprint audit; owner-bound/scoped boundary revalidated PASS. Still close exact anchor/policy/frame/zone/selector/qualifying-anchor constraints, family totality, source ownership and Occurrence governing-state eligibility; no placeholder policy fields are allowed |
| DB-U14 | owner/family-specific lifecycle/tombstone fields and destructive continuity | derive actual retirement/redaction/delete continuity per owner/relation; close native/scoped owner↔address behavior and the owner-specific redacted/tombstone representation that preserves MaterialStateRef totality; no global deleted_at or tombstone semantic root |
| DB-U15 | remaining structural FK indexes and query indexes | final FK/query graph must justify each; preserve already-closed PK/UNIQUE/material owner-facet indexes and add none speculatively |
| DB-U17 | provider/integration object shapes | genuinely deferred until first concrete integration/provider contract |
| DB-U18 | idempotency table timing | genuinely deferred until first persistent material operation requiring reservation/replay semantics |
| DB-U19 | transactional outbox timing | genuinely deferred until first real Class-A async external effect |
| DB-U20 | derived/search/vector persisted structures | genuinely deferred until a real query/search/vector consumer proves materialization/index need |
| DB-U21 | object-level runtime privilege matrix + CP3 provisioning reconciliation | Gate-03 blocker before CP6-04. Privilege ownership direction is now fixed: provisioning owns role/schema foundation with no blanket business ACL grants; migrations own exact ACLs across tables/views/sequences/types/domains/routines. Exact object-by-object matrix still must close |

```text
UNRESOLVED PARAMETERS CURRENT
11

UNCLASSIFIED PARAMETERS ALLOWED AT GATE 03
0
```

`GENUINELY DEFERRED` is a classified final CP6-03 disposition when current closed authority cannot truthfully determine a schema and the future trigger is explicit. It is not permission to create a placeholder table.

---

## 23. Next derivation pass — remaining concrete owner/context/relation contract

The next CP6-03 work continues in this same database specification; it does not create another methodology document and it does not reopen DB-U01..DB-U07/11/13/16 unless contradictory evidence is found.

### 23.1 Targeted post-repair revalidation — PASS / HARDENINGS INTEGRATED

The whole-blueprint repair was rechecked against the current Whole-Logical model, accepted PostgreSQL Physical mapping, CP6-01 ledgers, CP6-02 Constitution and the real CP3 provisioning code before opening another semantic block.

Result:

```text
DB-U12 owner-bound vs independently scoped Recurrence boundary
REVALIDATED / PASS
six semantic families unchanged
exact physical policy/anchor/frame constraints remain legitimately open

DB-U03 / DB-U04 MaterialState totality
REVALIDATED / PASS
redaction/tombstone is NOT an exception to resolvability
DB-U14 must preserve one owner-specific resolvable state representation

DB-U21 privilege/provisioning pressure
REVALIDATED / REAL CODE PRESSURE CONFIRMED
CP3 broad table DML + sequence/type privileges are too broad for future immutable/control business objects
provisioning→role/schema foundation direction FIXED
migration-owned exact business ACL direction FIXED
object-by-object matrix remains open

DB-U14 lifecycle dependency
REVALIDATED / CORRECTLY OPEN
no universal deletion/tombstone policy invented
```

No contradiction requiring Domain, Logical, Physical, CP6-01 or CP6-02 reopening was found.

Highest-value remaining semantic work now resumes with:

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
12. define exact object-level privileges
13. create/update Database Dictionary entry
14. close/update affected DB-U item
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
MaterialState live address↔owner-specific representation       PASS
MaterialState totality preserved through redaction/tombstone   PASS
idempotency/provenance/correlation explicitly accounted       PASS
provider/derived/tombstone/outbox pressures accounted         PASS
all determinable relational families concrete                 PASS
all determinable tables/columns/types concrete                PASS
all determinable PK/FK/reference topology concrete            PASS
all determinable material-state/history topology concrete     PASS
all determinable relation topology concrete                   PASS
all determinable constraints concrete                         PASS
all determinable structural indexes justified                 PASS
object-level runtime privilege matrix complete                PASS
CP3 provisioning narrowed to role/schema foundation           PASS
migration-owned exact business ACL design complete             PASS
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
DB-U03/04 BIDIRECTIONAL TOTALITY HARDENED
REDACTION/TOMBSTONE CANNOT BREAK MATERIALSTATEREF RESOLVABILITY
DB-U01/02 DESTRUCTIVE LIFECYCLE DEPENDENCY → DB-U14

LR-01 NATIVE IDENTITY-SHELL BASELINE
15 / 15 CLOSED

TEMPORAL / PLACE / VALUE / CAPACITY PASS
DB-U07 / DB-U11 / DB-U13 / DB-U16 CLOSED

RECURRENCE
SIX SEMANTIC FAMILIES RETAINED
OWNER-BOUND / INDEPENDENTLY-SCOPED BOUNDARY REVALIDATED PASS
DB-U12 EXACT PHYSICAL CONSTRAINT CONTRACT OPEN
ZERO PLACEHOLDER POLICY FIELDS ALLOWED

DATABASE PRIVILEGES
DB-U21 OPEN / BLOCKER BEFORE CP6-04
PROVISIONING ROLE/SCHEMA FOUNDATION DIRECTION FIXED
MIGRATION-OWNED BUSINESS ACL DIRECTION FIXED
EXACT OBJECT MATRIX STILL OPEN

TARGETED POST-REPAIR REVALIDATION
PASS / HARDENINGS INTEGRATED

EXACT REMAINING SEMANTIC TABLE/COLUMN/CONSTRAINT BLUEPRINT
IN PROGRESS

UNRESOLVED DB-U ITEMS
11

GATE 03
NOT YET EARNED
```

No business migration, SQLAlchemy business mapping, provisioning implementation, persistence adapter, API or product vertical is authorized merely by this candidate blueprint.

---

## 25. Object-level closure pass II — Schedule / Actual / Outcome / Milestone / Agreement

This pass consumes the complete accepted Domain continuations and Logical Time/Reality + Relationships/Governance contracts for five high-pressure contextual/result families. It is later than sections 14–24 and therefore **supersedes only the provisional statements for these five families where this section is more specific**. It does not reopen the already-closed reference/material-state topology, DB-U07 temporal value doctrine, or Recurrence semantics.

The pass deliberately distinguishes:

```text
relational envelope that closed authority determines now
!=
semantic payload that would require an invented universal vocabulary
```

No `status`, `result_code`, generic terms JSON, generic temporal payload, universal parent tree or cross-domain enum is introduced merely to make a candidate table look complete.

### 25.1 Schedule — scoped accepted-placement identity/topology CLOSED; exact coarse encoding locally open

Schedule is a dependent accepted temporal placement, not a timestamp pair embedded into Activity/Event/Occurrence.

The stable contextual envelope is:

```text
dante.schedule
  schedule_ref         uuid PRIMARY KEY
  subject_native_ref   uuid NOT NULL
```

Rules:

```text
schedule_ref
→ UUIDv7 ScopedRecordRef
→ matching dante.scoped_address(scoped_ref)
→ scoped_family = schedule

subject_native_ref
→ FK dante.native_address(native_ref)
→ ON DELETE NO ACTION
→ bounded Reference Contract owner_family IN ('activity','event','occurrence')

schedule subject binding
→ immutable under ordinary runtime authority

one subject
→ MAY own multiple independent Schedule placements when semantics permit
→ therefore NO global UNIQUE(subject_native_ref)
```

The chosen identity is **one independently revisionable accepted placement**, not one generic Schedule container holding anonymous blocks. This preserves divisible Activity cases such as two accepted placements for one Activity while allowing each placement to carry its own material revision history.

Schedule current material truth uses the existing scoped current-binding topology:

```text
facet_code = 'schedule.placement'

Schedule row
→ scoped_address
→ MaterialStateRef
→ owner-specific Schedule placement payload
→ dante.scoped_current_material_state when one current accepted placement state exists
```

The stable state-envelope design name is:

```text
dante.schedule_placement_state
  material_state_ref   uuid PRIMARY KEY
  schedule_ref         uuid NOT NULL
```

with:

```text
material_state_ref
→ FK dante.material_state_address(material_state_ref)
→ ON DELETE NO ACTION
→ exact scoped owner = schedule_ref
→ exact facet = schedule.placement

schedule_ref
→ FK dante.schedule(schedule_ref)
→ ON DELETE NO ACTION
```

The exact typed temporal payload must use DB-U07 representations and must never duplicate current time fields on Activity/Event/Occurrence. Historical placement states remain immutable-by-policy; a material reschedule creates a new MaterialStateRef and the explicit current binding moves to the new state.

Schedule absence remains valid:

```text
no Schedule row ever created
→ subject has no accepted placement history

historical Schedule row exists + no currently applicable placement binding
→ previously scheduled / now unscheduled or unresolved under the owning lifecycle semantics
```

No synthetic row/value is created for:

```text
UNSCHEDULED
POSTPONED
AVAILABLE
```

because those words do not all belong to Schedule placement state and some belong to lifecycle/constraint/product interpretation.

#### SCH-U01 — exact coarse accepted-placement encoding

DB-U07 correctly preserves coarse/partial precision as a semantic requirement, but current closed authority does **not** yet define a deterministic database vocabulary for a Schedule such as:

```text
Tuesday afternoon
```

DANTE therefore MUST NOT silently invent boundaries such as `12:00–18:00`, nor materialize a free-form `precision_code='afternoon'` whose semantics are not closed.

SCH-U01 closes only when the accepted Time/Schedule authority determines the exact typed representation and bounded vocabulary for coarse accepted placements, including any day-part semantics. Exact date, floating-local, named-zone, absolute-instant and exact range variants may continue to consume DB-U07; a generic wide nullable temporal blob is not authorized.

#### SCH-U02 — current-binding cessation / unscheduling lifecycle

Removing current accepted Schedule placement is not the same as deleting Schedule history or cancelling its subject. SCH-U02 must close the exact database operation and privilege posture for:

```text
current schedule.placement binding exists
→ accepted placement becomes absent without new replacement placement
→ historical Schedule + historical MaterialStateRefs remain reconstructible
```

The closure must remain compatible with the shared current-binding topology and DB-U14. In particular, CP6 must not grant blanket DELETE on `scoped_current_material_state` merely to support one Schedule use case unless bounded database enforcement proves that other facets cannot be erased incorrectly.

### 25.2 Actual — scoped realization envelope + known realization/non-realization axis CLOSED; physical cardinality/facets locally open

Actual remains the contextual realization of one specific intended/expected native subject. It does not become a universal reality root.

Stable envelope:

```text
dante.actual
  actual_ref           uuid PRIMARY KEY
  subject_native_ref   uuid NOT NULL
```

Rules:

```text
actual_ref
→ UUIDv7 ScopedRecordRef
→ matching scoped_address family actual

subject_native_ref
→ FK dante.native_address(native_ref)
→ ON DELETE NO ACTION
→ bounded Reference Contract owner_family IN ('activity','event','occurrence')

subject binding
→ immutable under ordinary runtime authority
```

The accepted semantic default remains one canonical realization context for one expectation rather than multiplying Actual rows for Session/Observation/Participation facets. However the Domain explicitly deferred final physical cardinality; therefore this pass **does not yet freeze `UNIQUE(subject_native_ref)`**. ACT-U01 must reclose that exact SQL cardinality before implementation.

Current material realization uses:

```text
facet_code = 'actual.realization'
```

with stable state-envelope design name:

```text
dante.actual_realization_state
  material_state_ref      uuid PRIMARY KEY
  actual_ref              uuid NOT NULL
  realization_occurred    boolean NOT NULL
```

Meaning is deliberately narrow:

```text
NO established Actual/current realization state
→ realization UNKNOWN / not established

realization_occurred = false
→ KNOWN NON-REALIZATION of the expectation

realization_occurred = true
→ SOME realization of the expectation is established
```

`true` does **not** mean completed/successful/passed, and `false` does not encode every possible Outcome. Partial, different, replaced, failed, accepted, passed and similar semantics remain outside this boolean.

The state row must satisfy:

```text
material_state_ref
→ FK material_state_address
→ exact scoped owner actual_ref
→ exact facet actual.realization

actual_ref
→ FK dante.actual(actual_ref)
→ ON DELETE NO ACTION
```

A new correction/reconciliation creates a new MaterialStateRef; current accepted realization moves through the existing scoped current binding rather than overwriting the old payload.

Where actual execution Sessions materially compose a particular realization state, the typed relation candidate is:

```text
dante.actual_realization_session
  material_state_ref   uuid NOT NULL
  session_ref          uuid NOT NULL

  PRIMARY KEY(material_state_ref, session_ref)
```

with direct homogeneous FK to `dante.session(session_ref)` and an exact eligibility check that `material_state_ref` is `actual.realization`. No Session is required for ordinary Event Actual, and spontaneous Session may exist without an Actual.

#### ACT-U01 — remaining Actual physical closure

ACT-U01 must close, without a generic status/result payload:

```text
whether one canonical Actual per subject is enforced by UNIQUE(subject_native_ref) or by a narrower semantic key
exact optional Actual timing facet shape where Actual itself owns realized chronology rather than Session/Observation
replacement/substitution relation topology
how progressive establishment/reconciliation affects physical cardinality
exact indexes once those FKs/query paths are frozen
```

The open item does not weaken the closed unknown-vs-known-non-realization distinction.

### 25.3 Outcome — semantic envelope defined; universal concrete result table NOT authorized

Outcome remains contextual result/disposition of a specific Actual when such result semantics materially matter.

Closed dependency:

```text
Outcome
→ belongs to one exact Actual realization context
→ does not replace Actual / Session / Observation / Milestone / Confirmation / Provenance / Contribution
```

If a concrete Outcome family becomes materially persistent and independently addressable, its relational envelope must use:

```text
outcome_ref   UUIDv7 ScopedRecordRef
actual_ref    direct FK to dante.actual(actual_ref)
```

However current closed authority explicitly rejects a universal Outcome vocabulary. Therefore CP6-03 does **not** implementation-authorize any of:

```text
dante.outcome(result_code text)
universal Outcome ENUM
completed/partial/skipped/passed/failed global result taxonomy
JSONB result payload as semantic escape hatch
one Outcome per participant by default
```

The design handle `outcome` remains reserved for a concrete typed result family only after its result semantics are closed. The Database Dictionary must not advertise a materialized universal Outcome table before that happens.

Shared result and actor-scoped Contribution remain separate: one shared Outcome may coexist with several Contributions without duplicating the Outcome per Actor.

#### OUT-U01 — first concrete typed Outcome result family

OUT-U01 closes when an accepted owner/context provides a deterministic typed result family with:

```text
exact result semantics/vocabulary
exact cardinality against Actual
material-state/history requirement
conflicting contextual assertion behavior
correction/reconciliation behavior
SQL columns/constraints
privilege posture
direct positive/negative tests
```

Until then the correct CP6 disposition is **NO universal concrete result payload**, not a placeholder schema.

### 25.4 Milestone — scoped contextual checkpoint + material Goal/Plan context set CLOSED

Milestone is a persistent dependent checkpoint whose meaning requires context from at least one Goal and/or Plan and may truthfully matter to more than one of either. No rigid `Goal → Plan → Milestone` parent tree is accepted.

Stable contextual owner:

```text
dante.milestone
  milestone_ref   uuid PRIMARY KEY
```

Rules:

```text
milestone_ref
→ UUIDv7 ScopedRecordRef
→ matching scoped_address family milestone
```

The contextual meaning is material and version-sensitive, so the exact context set is represented as one Milestone-owned material state rather than mutable sparse parent FKs:

```text
facet_code = 'milestone.context'

dante.milestone_context_state
  material_state_ref   uuid PRIMARY KEY
  milestone_ref        uuid NOT NULL

dante.milestone_context_goal
  material_state_ref   uuid NOT NULL
  goal_ref             uuid NOT NULL
  PRIMARY KEY(material_state_ref, goal_ref)

dante.milestone_context_plan
  material_state_ref   uuid NOT NULL
  plan_ref             uuid NOT NULL
  PRIMARY KEY(material_state_ref, plan_ref)
```

FKs:

```text
milestone_context_state.material_state_ref
→ material_state_address
→ exact scoped owner milestone_ref
→ exact facet milestone.context

milestone_context_state.milestone_ref
→ dante.milestone(milestone_ref)
→ ON DELETE NO ACTION

milestone_context_goal.goal_ref
→ dante.goal(goal_ref)
→ ON DELETE NO ACTION

milestone_context_plan.plan_ref
→ dante.plan(plan_ref)
→ ON DELETE NO ACTION

child material_state_ref
→ dante.milestone_context_state(material_state_ref)
→ ON DELETE NO ACTION
```

A deferred database invariant must require, by COMMIT:

```text
COUNT(goal links) + COUNT(plan links) >= 1
```

for each live `milestone.context` state. Multiple Goal and/or Plan links are valid. Duplicate links reject through the composite PKs.

Context revision creates a new MaterialStateRef when materially consequential; old context remains reconstructible. This does not imply every newly added supporting fact changes Milestone identity.

Milestone does **not** receive universal columns for:

```text
reached boolean
status enum
progress_percent
completed_at
```

Attainment remains Evidence/Evaluation-backed. Target date/window remains temporal target semantics, not Schedule placement.

#### MIL-U01 — definition/target/attainment physical facets

MIL-U01 must close the exact typed persistence boundaries among:

```text
Milestone checkpoint definition/material state
Milestone target date/window/expectation
Criterion/Evaluation/Evidence-backed attainment
historical reached/effective time where material
waiver/cancellation/supersession only if an accepted lifecycle requires them
```

No stored percentage or independent attainment truth may duplicate its underlying Evidence/Evaluation basis.

### 25.5 Agreement — scoped n-ary shared-assent topology CLOSED; terms eligibility/provenance locally open

Agreement is contextual multi-party mutual assent to the **same materially specific terms state**. It is neither a native owner nor pairwise `agreed_with` edges.

Stable contextual owner:

```text
dante.agreement
  agreement_ref   uuid PRIMARY KEY
```

Rules:

```text
agreement_ref
→ UUIDv7 ScopedRecordRef
→ matching scoped_address family agreement
```

The accepted shared-assent state is material:

```text
facet_code = 'agreement.shared_assent'

dante.agreement_shared_assent_state
  material_state_ref          uuid PRIMARY KEY
  agreement_ref               uuid NOT NULL
  terms_material_state_ref    uuid NOT NULL
```

with:

```text
material_state_ref
→ FK dante.material_state_address(material_state_ref)
→ exact scoped owner agreement_ref
→ exact facet agreement.shared_assent

agreement_ref
→ FK dante.agreement(agreement_ref)
→ ON DELETE NO ACTION

terms_material_state_ref
→ FK dante.material_state_address(material_state_ref)
→ ON DELETE NO ACTION
→ bounded eligible terms-bearing owner/facet contract to be closed by AGR-U01
```

The parties that share that assent are preserved as an n-ary set bound to the exact Agreement material state:

```text
dante.agreement_party_assent
  agreement_material_state_ref   uuid NOT NULL
  party_native_ref               uuid NOT NULL

  PRIMARY KEY(agreement_material_state_ref, party_native_ref)
```

Reference Contract:

```text
agreement_material_state_ref
→ FK dante.agreement_shared_assent_state(material_state_ref)
→ ON DELETE NO ACTION

party_native_ref
→ FK dante.native_address(native_ref)
→ ON DELETE NO ACTION
→ bounded owner_family IN ('person','collective')
```

A deferred database invariant requires at least two distinct party rows for each live accepted shared-assent state. The composite PK already rejects duplicate party entries.

All parties in one `agreement_shared_assent_state` necessarily bind the same `terms_material_state_ref` because terms are owned once by the parent material state rather than repeated independently on each party row.

Material amendment:

```text
terms T1 + parties P1/P2 → Agreement state A1
material terms T2       → new Agreement MaterialStateRef A2
A1 party rows remain historical
A2 requires its own applicable party-assent rows
```

Old assent therefore cannot silently float from T1 to T2.

A true Collective may be one Agreement party. DANTE does not expand it into all current members and does not infer Collective assent from member assent or vice versa.

Actual acting Actor / represented party / Principal / governance basis are not collapsed into `party_native_ref`. On-behalf-of semantics remain Representation/provenance/governance concerns.

#### AGR-U01 — exact terms-state and on-behalf-of/provenance contract

AGR-U01 must close:

```text
exact eligible terms_material_state_ref owner/facet families
whether a dedicated Agreement terms owner/state is required in any accepted ordinary case
exact material equivalence/applicability enforcement at DB boundary
on-behalf-of assent binding to actual Actor + represented party + Authority/Representation basis where material
Provenance/recorded chronology required for consequential assent
exact indexes once query/cardinality pressure is frozen
```

`terms_material_state_ref` may never mean “any MaterialStateRef in the database”. Consumer-specific database eligibility is mandatory.

### 25.6 Migration-DAG consequences of pass II

No CP6-04 business migration is authorized yet, but the dependency order for these families is now constrained.

```text
LR-01 native owner identity shells
→ native_address support for Activity/Event/Occurrence/Person/Collective targets

scoped contextual owner tables
→ schedule
→ actual
→ milestone
→ agreement

scoped_address dispatcher vocabulary
→ add only the concrete scoped families above

material_state_address + current-binding control foundation
→ unchanged

owner-specific material state payloads
→ schedule_placement_state after SCH-U01/02 closure
→ actual_realization_state after ACT-U01 exact cardinality/facet closure
→ milestone_context_state + Goal/Plan child relations
→ agreement_shared_assent_state + party rows after AGR-U01 exact terms eligibility closure

Outcome
→ no universal migration until OUT-U01 closes a concrete typed result family
```

Insert ordering for a material contextual state follows the already-closed control contract:

```text
create scoped semantic row
→ create scoped_address projection
→ create material_state_address
→ create exact owner-specific state payload + immutable child rows
→ satisfy deferred payload totality/cardinality constraints
→ create/update current binding where applicable
→ COMMIT
```

### 25.7 SQLAlchemy mapping consequences

CP6-04 mapping direction is now:

```text
Schedule
Actual
Milestone
Agreement
→ independent semantic row classes
→ no shared ContextualEntity mapped superclass

SchedulePlacementState
ActualRealizationState
MilestoneContextState
AgreementSharedAssentState
→ owner/facet-specific immutable-by-policy state classes

ActualRealizationSession
MilestoneContextGoal
MilestoneContextPlan
AgreementPartyAssent
→ explicit typed relation/association mappings

Outcome
→ no generic mapped class until OUT-U01 closes a real result family
```

Reference Python types preserve `NativeRef`, `ScopedRecordRef` and `MaterialStateRef` distinctions. Temporal helper/composite types may encode the exact DB-U07 variants after SCH-U01 closes remaining coarse Schedule precision; they do not create ORM identity.

No generic repository/UoW/base-service layer is introduced by these mappings.

### 25.8 Structural index posture for pass II

Only structurally justified indexes are accepted now:

```text
schedule PK(schedule_ref)
actual PK(actual_ref)
milestone PK(milestone_ref)
agreement PK(agreement_ref)

milestone_context_goal PK(material_state_ref, goal_ref)
milestone_context_plan PK(material_state_ref, plan_ref)
agreement_party_assent PK(agreement_material_state_ref, party_native_ref)
actual_realization_session PK(material_state_ref, session_ref)
```

Additional indexes on:

```text
schedule.subject_native_ref
actual.subject_native_ref
goal_ref
plan_ref
party_native_ref
session_ref
terms_material_state_ref
```

remain under DB-U15 until the final FK lookup/query graph proves they are needed; DANTE does not index every FK by reflex.

No temporal GiST/EXCLUDE index is introduced for Schedule merely because ranges exist. Overlap/conflict semantics belong to Capacity/Availability/owner policy and are not a universal Schedule invariant.

### 25.9 Object-level privilege implications

Pending final DB-U21 matrix, these objects constrain the least-privilege direction:

```text
schedule / actual / milestone / agreement owner rows
→ runtime SELECT + INSERT for accepted creation paths
→ PK/subject binding UPDATE denied under ordinary runtime behavior
→ DELETE denied until DB-U14 exact lifecycle proves it

immutable material state payloads
→ runtime SELECT + INSERT
→ UPDATE denied
→ DELETE denied except a later explicitly governed DB-U14 mechanism that preserves MaterialStateRef totality

actual_realization_session
milestone_context_goal
milestone_context_plan
agreement_party_assent
→ treated as immutable components of one material state after acceptance
→ ordinary UPDATE/DELETE denied

current binding
→ INSERT/UPDATE only as already required
→ Schedule cessation DELETE remains SCH-U02-specific and must not broaden other-facet authority

trigger/integrity routines
→ no direct runtime EXECUTE by default

sequences
→ none required by UUIDv7 semantic identities
```

Exact GRANT/REVOKE remains migration-owned in the same change that creates each object.

### 25.10 Direct PostgreSQL proof matrix added by pass II

#### Schedule

```text
Activity subject accepted                                PASS
Event subject accepted                                   PASS
Occurrence subject accepted                              PASS
wrong native owner family                                REJECT
missing native_address                                   REJECT
multiple independent Schedule rows for one Activity      PASS
material state wrong scoped owner/facet                  REJECT
material reschedule preserves old state                  PASS
current state selected only by explicit binding          PASS
synthetic UNSCHEDULED payload                            absent by schema
coarse day-part encoding                                 STAGED until SCH-U01
current binding cessation/unscheduling                   STAGED until SCH-U02
```

#### Actual

```text
Activity/Event/Occurrence subject accepted               PASS
wrong subject family                                     REJECT
no Actual/current state                                  remains UNKNOWN
realization_occurred=false                               known non-realization
realization_occurred=true                                established realization; not universal success
wrong owner/facet state                                  REJECT
Session link to real Session                             PASS
Session link duplicate in same state                    REJECT by PK
Event Actual without Session                             PASS
spontaneous Session without Actual                       PASS
correction creates new MaterialStateRef                  PASS
exact subject cardinality/replacement/time facets        STAGED until ACT-U01
```

#### Outcome

```text
universal Outcome enum/table                             absent by design
unconfirmed encoded as Outcome                           absent by design
shared Outcome duplicated per Contribution              forbidden by design
first concrete typed result family                       STAGED until OUT-U01
```

#### Milestone

```text
Milestone scoped identity/address                        PASS
context state with Goal only                             PASS
context state with Plan only                             PASS
context state with Goal + Plan                           PASS
context state with multiple Goals/Plans                  PASS
context state with zero Goal/Plan links by COMMIT        REJECT
same Goal/Plan duplicate link                            REJECT by PK
reached/progress universal columns                       absent by schema
attainment duplicates underlying Evidence/Evaluation     forbidden by design
exact target/attainment facets                           STAGED until MIL-U01
```

#### Agreement

```text
Agreement scoped identity/address                        PASS
Person party                                             PASS
Collective party                                         PASS
wrong party owner family                                 REJECT
one-party shared-assent state by COMMIT                  REJECT
two or more distinct parties                            PASS
duplicate party                                          REJECT by PK
all parties bind same parent terms MaterialStateRef      PASS by structure
material terms amendment reuses old assent automatically REJECT by structure
old shared-assent state/history preserved                PASS
arbitrary MaterialStateRef accepted as terms             REJECT once AGR-U01 contract closes
on-behalf-of collapsed into party identity                forbidden by design
```

### 25.11 Local object-level unresolved register from pass II

These are not vague TODOs and do not authorize placeholder schema.

| ID | Exact remaining parameter | Why it remains open | Closure trigger |
|---|---|---|---|
| SCH-U01 | coarse accepted Schedule placement encoding | current authority requires coarse precision but does not define exact day-part/bounded vocabulary | close exact Time/Schedule representation without invented clock boundaries or free-text precision codes |
| SCH-U02 | Schedule current-binding cessation / unscheduling operation | historical Schedule must survive while current placement may become absent; shared current-binding DELETE privilege cannot be widened casually | close DB operation + DB-U14/DB-U21-safe privilege/integrity path |
| ACT-U01 | Actual exact subject cardinality + optional timing/replacement facets | semantic default is one contextual realization, but Domain explicitly deferred physical cardinality and specialist realization facets | close exact UNIQUE/key rule, realized chronology ownership and replacement relation topology |
| OUT-U01 | first concrete typed Outcome result family | Domain rejects a universal result enum/payload | first accepted result context with exact typed vocabulary and cardinality |
| MIL-U01 | Milestone definition/target/attainment facet split | context is now concrete; target and evaluation-backed attainment still require exact physical ownership | close Criterion/Evaluation/Evidence + target physical contract without duplicate reality |
| AGR-U01 | Agreement terms-state eligibility + consequential assent provenance | Agreement must bind one exact material terms state, but not every MaterialStateRef is eligible and on-behalf-of attribution is separate | close bounded terms owner/facet set + Representation/Authority/Provenance binding |

```text
PASS-II LOCAL UNRESOLVED ITEMS
6

UNCLASSIFIED PASS-II ITEMS
0
```

The six items are Gate-03 blockers only to the extent their current concepts require concrete CP6 materialization; they are not permission to manufacture a generic fallback.

### 25.12 Accumulated audit result after pass II

The new topology was regressed against the already-closed identity/reference/material-state/value/time/spatial/capacity decisions.

```text
15 LR-01 identity owners                                  PASS
NativeRef topology                                        PASS
ScopedRecordRef topology                                  PASS
MaterialStateRef totality                                 PASS
current binding topology                                  PASS
typed lineage                                             PASS

Schedule heterogeneous NativeRef {Activity,Event,Occurrence} PASS
Actual heterogeneous NativeRef {Activity,Event,Occurrence}   PASS
Milestone Goal/Plan context with homogeneous FKs             PASS
Agreement party NativeRef {Person,Collective}                 PASS
Agreement n-ary same-terms binding                            PASS
Outcome exact Actual dependency                               PASS

NO generic Entity                                          PASS
NO generic Relationship                                    PASS
NO generic TemporalEvent                                   PASS
NO global status enum                                      PASS
NO global Outcome enum                                     PASS
NO generic Agreement terms JSON/EAV                        PASS
NO artificial Milestone parent tree                        PASS

Schedule != Actual                                         PASS
Actual != Outcome                                          PASS
Outcome != Milestone                                       PASS
Agreement != Consent / Authority                           PASS
Schedule != Capacity                                       PASS
Schedule != Recurrence                                     PASS

DB-U11 Place/PostGIS                                       UNAFFECTED / PASS
DB-U13 Quantity/Money                                      UNAFFECTED / PASS
DB-U16 Capacity Claim                                      UNAFFECTED / PASS
DB-U12 Recurrence                                          UNAFFECTED / REMAINS OPEN ONLY AS PREVIOUSLY CLASSIFIED
DB-U21 ACL direction                                       COMPATIBLE / STILL OPEN
```

One audit correction is deliberate: the read-only derivation initially considered freezing `UNIQUE(actual.subject_native_ref)`, but the canonical Actual Domain authority still states that final physical cardinality must not be frozen prematurely. The blueprint therefore records the semantic one-context default while keeping the exact SQL cardinality in ACT-U01. This is a hardening, not a semantic reopening of Actual.

### 25.13 Current CP6-03 status after pass II

This pass moves the object graph forward but does not earn Gate 03.

```text
Schedule envelope / subject contract / material ownership     CLOSED
Schedule exact coarse placement + cessation path               SCH-U01 / SCH-U02 OPEN

Actual envelope / subject contract / realization axis          CLOSED
Actual exact SQL cardinality / optional facets                 ACT-U01 OPEN

Outcome universal fallback                                    REJECTED
Outcome concrete typed family                                 OUT-U01 OPEN

Milestone scoped identity + material Goal/Plan context         CLOSED
Milestone target/attainment physical split                     MIL-U01 OPEN

Agreement scoped n-ary same-terms assent topology              CLOSED
Agreement terms eligibility/provenance                         AGR-U01 OPEN

PASS-II UNCLASSIFIED                                           0
CP6 BUSINESS DDL AUTHORIZED                                    NO
GATE 03                                                        NOT YET EARNED
```

The next semantic pass should therefore consume the specific LR-03 relation/governance families and the Criterion/Evaluation/Temporal Constraint pressures needed to close the remaining dependencies, rather than inventing placeholder payloads for the six local open items.