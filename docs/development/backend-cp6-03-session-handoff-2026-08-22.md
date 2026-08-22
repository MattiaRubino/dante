# DANTE Backend CP6-03 — Temporary Session Resume Handoff — 2026-08-22

- **Status:** TEMPORARY SESSION HANDOFF / RESUME AID
- **Purpose:** allow a fresh ChatGPT/AI/human session to continue CP6-03 from the current repository state with the same rigor, boundaries and decision context as the session that produced this handoff.
- **Branch:** `feature/logical-postgresql`
- **PRE-SCOPE when this handoff was written:** `bdbd5e8447f27447480c0a9667e7ff63b5c0a9f6`
- **Protected-main anchor / merge-base:** `fd3bc8dd918cf6aadeff4572221af68612c3cb42`
- **Branch relation at PRE-SCOPE:** ahead `55`, behind `0`
- **Current CP6 stage:** `CP6-03 ACTIVE / WHOLE DANTE DATABASE BLUEPRINT / GATE 03 NOT YET EARNED`
- **Canonical CP6 blueprint/reference:** `docs/database/dante-postgresql-database.md`
- **Canonical CP6 workstream:** `docs/workstreams/logical-postgresql.md`
- **Deletion policy:** once the next session has fully re-read the canonical sources, verified live Git state and absorbed the resume point, this file may be deleted through an exact write gate. It is intentionally not a permanent architectural authority.

> **Critical authority rule:** repository truth outranks this handoff and conversation memory. If the branch has advanced after the PRE-SCOPE above, inspect the newer commits/current canonical documents first and update the resume point rather than forcing this file onto newer truth.

---

## 1. What the project is doing right now

DANTE has already closed its Domain, Logical and Physical modelling phases for the current scope and has an integrated production backend scaffold through CP5. The active backend persistence workstream is **CP6 Concrete PostgreSQL Database**.

The current execution sequence is not a generic “foundation now, real DB later” plan. The current repository authority explicitly requires CP6 to design and materialize the concrete PostgreSQL database that can already be derived non-speculatively from the closed model.

```text
CLOSED DOMAIN
+ CLOSED LOGICAL
+ ACCEPTED PHYSICAL POSTGRESQL MAPPING
+ CLOSED CP6-01 PERSISTENCE COVERAGE
+ CLOSED CP6-02 POSTGRESQL CONSTITUTION
        ↓
CP6-03 — WHOLE DANTE DATABASE BLUEPRINT
        ↓
whole-blueprint audit / repair loops until clean
        ↓
CP6-04 — WHOLE DANTE DATABASE MATERIALIZATION
        ↓
Alembic business migrations
SQLAlchemy mappings
real PostgreSQL schema
exact grants/constraints/indexes
same-change database documentation
        ↓
CP6-05 — WHOLE DATABASE DIRECT QA + CLEAN-ROOM CLOSURE
        ↓
CP6 CLOSED
        ↓
FIRST PRODUCT VERTICAL — SEPARATE POST-CP6 APPLICATION PHASE
```

Hard boundary:

```text
DATABASE DESIGN + DATABASE IMPLEMENTATION
= CP6

FIRST APPLICATION VERTICAL
= AFTER CP6
```

CP6 may and eventually must create the concrete business/database schema, migrations, mappings and direct database tests. CP6 must **not** implement application use cases, business services, product persistence adapters, HTTP/API routes, frontend behavior or the first product vertical workflow.

---

## 2. How the current work must be performed

The user explicitly wants a repeated **design → total audit → repair → continue** discipline all the way to the real database.

Do not build a long sequence of locally plausible decisions and wait until the end to discover that they conflict. After every meaningful database-design block:

```text
1. derive the next bounded database block from closed authority;
2. write only after an exact gate is approved;
3. re-read the WHOLE accumulated blueprint, not only the new section;
4. cross-check it against Domain + Logical + Physical + CP6-01 + CP6-02 + real CP3 code;
5. pressure PostgreSQL feasibility where mechanism details matter;
6. classify findings:
   A. still valid / closed;
   B. valid direction but closed too early;
   C. concrete defect/blocker;
7. repair all material findings before moving on;
8. revalidate the repaired whole;
9. only then open the next semantic/database block.
```

The standard is intentionally enterprise-grade: the target is a database and documentation system understandable and maintainable like a serious large-system repository, not a hobby schema optimized for minimum file count or fastest coding.

At the same time:

```text
professional != ceremonial
enterprise-grade != speculative complexity
selected capability != activate it now
complete DB != invent future product semantics
```

Every structure must be justified by accepted model authority or an already-real database requirement.

---

## 3. Mandatory bootstrap for the next session

Before any material write, re-read/verify at minimum:

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

docs/workstreams/logical-postgresql.md

docs/database/README.md
docs/database/dante-postgresql-database.md

docs/development/backend-cp6-01-concrete-persistence-coverage.md
docs/development/backend-cp6-01-concrete-persistence-coverage-part-2.md
docs/development/backend-cp6-01-concrete-persistence-coverage-closure.md

docs/development/backend-cp6-02-postgresql-persistence-constitution.md
docs/development/backend-cp6-02-postgresql-persistence-constitution-closure.md
docs/decisions/ADR-010-postgresql-persistence-constitution.md
```

For semantic derivation, consume the actual relevant canonical Domain/Logical sources rather than relying on this handoff summaries. At minimum know how to reach:

```text
docs/logical-model/whole-logical-model-v1.md
docs/logical-model/representation-framework-v1.md
docs/logical-model/slices/*
docs/domain/concepts/*
```

For Physical/PostgreSQL constraints, re-read as needed:

```text
docs/physical-model/README.md
docs/physical-model/pm-02-primary-mapping-overview-v1.md
docs/physical-model/mappings/postgresql-18.4-v1.md
docs/physical-model/preflight/postgresql-18.4-v1.md
docs/physical-model/pm-11-explicit-selection-v1.md
docs/physical-model/pm-12-accepted-physical-model-v1.md
docs/physical-model/pm-13-clean-room-qa-v1.md
docs/physical-model/recommendation/post-selection-validation-register-v1.md
```

Also inspect the **real CP3 implementation**, especially:

```text
apps/backend/src/dante/platform/database/metadata.py
apps/backend/src/dante/platform/database/runtime.py
apps/backend/src/dante/platform/database/provisioning.py
apps/backend/migrations/env.py
apps/backend/migrations/versions/20260820_01_cp3_persistence_baseline.py
apps/backend/tests/integration/database/*
```

Do not assume this handoff's PRE-SCOPE is still HEAD. Resolve live `feature/logical-postgresql` HEAD first and compare it to protected main.

---

## 4. Git / write discipline — hard requirement

No repository mutation is casual.

Before a material write, present/obtain an exact bounded gate:

```text
BRANCH
feature/logical-postgresql

PRE-SCOPE
<exact live branch HEAD>

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

Immediately before first write, verify live branch HEAD == approved PRE-SCOPE.

After the write:

```text
remote readback
exact PRE-SCOPE → HEAD compare
added / modified / deleted counts
unexpected paths = 0
branch relation to protected main
applicable tests/checks
truthful checkpoint status
```

A user `vai` approves only the specific gate that was presented. Do not smuggle unrelated documentation/code paths into an approved write.

Do not mutate protected `main` directly. Do not merge outside the protected integration path.

---

## 5. Current technical platform truth

Architecture:

```text
PostgreSQL major family    18
Physical phase exact patch 18.4
CP2/CP3 exact execution    18.4 historical evidence
Current CP6 technical patch 18.6
```

Current technical stack recorded by CP6:

```text
Python       3.14.7
SQLAlchemy   2.0.52
Alembic      1.19.1
psycopg      3.3.4
PostGIS      3.6.4
pgvector     0.8.6
PgBouncer    1.25.2 selected capability / not activated merely by selection
```

PostgreSQL 18.6 technical foundation regression is already direct evidence:

```text
Backend CI run      32568664940
executed HEAD       ec3dc795b5e044daa3a77723c94a1b4b5b92865c
Backend Quality     32 / 32 fast lane PASS
Backend PostgreSQL  18 / 18 real-PostgreSQL lane PASS
aggregate CI gate   SUCCESS
```

Never rewrite old 18.4 evidence as though it executed on 18.6. Never describe the split 32+18 CI corpus as one single `pytest 50/50` invocation.

Current Docker PostgreSQL image recorded by CP6:

```text
postgres:18.6-trixie
sha256:ae6c78831cbc35fa3a4aaf4d763ddacf6183d6004774cc2dc28b3920410d1d1a
```

Do not move to SQLAlchemy 2.1 pre-release or PostGIS 3.7 beta merely because they exist.

---

## 6. CP3 real implementation baseline that CP6 must preserve

Real code already establishes:

```text
schema = dante
one SQLAlchemy Base / MetaData
one AsyncEngine per process
one async_sessionmaker per process
one AsyncSession per application operation/task
autobegin=False
autoflush=True
expire_on_commit=False
pool_pre_ping=True
outer application operation owns commit/rollback
adapter may flush; adapter must not own implicit commit
READ COMMITTED default
stronger concurrency chosen per invariant
one Alembic environment / one DAG / one canonical head
metadata.create_all() forbidden as deployment authority
```

SQLAlchemy metadata naming convention is deterministic:

```text
pk_%(table_name)s
fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s
uq_%(table_name)s_%(column_0_N_name)s
ix_%(table_name)s_%(column_0_N_name)s
ck_%(table_name)s_%(constraint_name)s
```

Existing database roles:

```text
dante_owner      NOLOGIN object/schema owner
dante_migrator   LOGIN NOINHERIT + bounded SET ROLE dante_owner
dante_runtime    LOGIN NOINHERIT runtime identity
```

Current Alembic environment uses migrator identity, `SET ROLE dante_owner`, schema `dante`, metadata drift comparison and revokes runtime access to `dante.alembic_version`.

Do not add generic `Repository[T]`, generic UnitOfWork, generic BaseService, one generic contextual ORM root, or a polymorphic semantic base merely for implementation uniformity.

---

## 7. Closed semantic/model foundation — do not casually reopen

Whole Logical currently preserves:

```text
DOMAIN CONCEPTS               57 / 57 classified
LR-01 NATIVE OWNERS           exactly 15
NEW DOMAIN OWNER REQUIRED     0
GENERIC FALLBACK DEPENDENCY   0
```

The exact 15 LR-01 native identity owners are:

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

Contextual roles remain roles, not wrapper identities:

```text
Actor
Subject
Resource
```

Forbidden default wrappers:

```text
ActorRef
SubjectRef
ResourceRef
```

ReferenceAddress remains a discriminated representation family:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

They may share PostgreSQL `uuid` at the physical level, but they are not interchangeable semantic/reference spaces.

High-risk separations that must survive every schema choice include:

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

Global forbidden persistence shortcuts remain:

```text
universal Entity / Thing table
universal generic Relationship / edge table
canonical EAV/property bag
universal event-log ontology
universal Fact/Version semantic payload table
generic kind+uuid reference without DB integrity
one-of-N nullable FK encoding for one heterogeneous NativeRef slot
provider ID promoted to NativeRef
MVCC / ETag / provider revision promoted to MaterialStateRef
absence/NULL interpreted globally as false
silent consequential last-write-wins
DB-wide SERIALIZABLE by convenience
PostgreSQL money for MonetaryAmount
JSONB as required-semantic escape hatch
RLS treated as Authority/Consent/Visibility truth
CASCADE as database/ORM default
speculative partitioning/sharding
specialist service activation without a real trigger
```

---

## 8. Physical PostgreSQL thesis already selected

The accepted PostgreSQL Physical model uses:

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

Important: historical Physical documents sometimes describe conceptual namespaces such as `core/history/integration/projection/technical`. CP3 later fixed the actual PostgreSQL deployment schema to **one PostgreSQL schema `dante`**. Do not create multiple PostgreSQL schemas merely because the Physical design used conceptual grouping language.

The accepted Physical risk lanes remain live:

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

Existing Physical direct business-semantic HG/PSV evidence must remain truthful: many items are staged/not-run until their executable database/application subject actually exists. Architecture acceptance is not the same as direct execution PASS.

---

## 9. CP6-01 and CP6-02 state

### CP6-01

```text
CLOSED / GATE 01 PASS
```

Part 1 owns exact 57/57 concept persistence coverage.

Part 2 is mandatory because:

```text
57/57 Domain coverage
is necessary
but not sufficient
```

Part 2 also accounts for non-57/cross-cutting pressure such as:

```text
Account
Principal/security context
ReferenceAddress / Reference Contract
NativeRef / ScopedRecordRef / MaterialStateRef / ExternalRef
current accepted-state binding
correction/replacement/reconciliation lineage
world/effective vs recorded/learned chronology
Governed Operation / Effect Contract
idempotency
correlation / causation
Projection / Disclosure Surface
provider/sync/apply state
flexible metadata
candidate/unresolved state
product/profile state
specialist extension
Actor/Subject/Resource roles
Capacity Claim
retention/tombstone/redaction continuity
anti-resurrection
transactional outbox capability trigger
PowerSync/local noncanonical state
search/vector/derived pressure
```

Every CP6-03 cross-cutting construct must end with exactly one truthful disposition:

```text
MATERIALIZE IN CP6
NO INDEPENDENT PERSISTENCE
GENUINELY DEFERRED with exact reason + future trigger/owner
```

### CP6-02

```text
CLOSED / GATE 02 PASS
```

The PostgreSQL Persistence Constitution is the reusable technical doctrine. Major closed rule families:

```text
TECH
ID
REF
MAT
HIST
TIM
MISS
LIFE
TYP
REL
CON
IDX
TX
IDEM
PROV
CAP
MIG
SEC
QA
```

Important closed points include:

- DANTE-owned stable independent identities use PostgreSQL `uuid` + UUIDv7;
- UUIDv7 is not semantic chronology and not universal row decoration;
- homogeneous reference contract → direct FK;
- genuinely heterogeneous NativeRef → bounded native-address infrastructure;
- application-only `type + uuid` is insufficient;
- MaterialStateRef is explicit and separate from MVCC/storage/provider revision;
- owner-specific material payload/history; no universal Version/Fact payload;
- explicit current accepted-state binding; never infer current by MAX/revision/UUID order;
- history is materiality-driven, not universal event sourcing;
- future named-zone civil time preserves IANA-zone semantics;
- absence/unknown/negative are not collapsed;
- `ON DELETE NO ACTION` is default; CASCADE requires semantic proof;
- `numeric` for exact amounts; PostgreSQL `money` forbidden;
- native typed semantics over generic JSONB;
- simple LR-03 relations remain specific; n-ary remains n-ary;
- declarative DB constraints first, narrow trigger only when necessary;
- FK index review mandatory, but index-every-FK is not automatic;
- READ COMMITTED default, stronger concurrency only where required;
- idempotency uniqueness is `(operation_scope, idempotency_key)`, fingerprint separate;
- Alembic is deployed schema authority; one DAG/head;
- migrations use expand/backfill/verify/cutover/contract where required;
- runtime privilege is least privilege, not blanket DML by principle;
- PostgreSQL semantics must be tested on real PostgreSQL.

---

## 10. Database documentation methodology already established

DANTE now has a permanent repository-native Database System of Record:

```text
docs/database/README.md
docs/database/dante-postgresql-database.md
future dictionary/* only when real approved objects exist
future generated/* only when real generated content exists
future diagrams/* only when useful/derived
future evolution/* only for complex real schema evolution
```

The professional consistency target is:

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

At CP6 closure they must be semantically/structurally consistent for the facts each representation owns.

Permanent same-change rule:

> A structural database change is incomplete unless the affected database documentation/dictionary/mapping/tests are updated in the same reviewed change.

Repository-native documentation was chosen deliberately. Do not add a heavy external catalog platform merely to look enterprise-grade.

The eventual dictionary must be able to record, where applicable:

```text
schema/object/type/persistence role/purpose
semantic source and representation family
canonical/contextual/relation/history/provider/derived/technical role
migration + SQLAlchemy mapping
column name/type/nullability/default/exact meaning
PK/stable address/FK/cardinality/delete/update/semantic reason
UNIQUE/CHECK/EXCLUDE/trigger-backed integrity
indexes + method + reason
MaterialState/current/history/chronology/lineage
retention/redaction/tombstone/delete behavior
owner/migrator/runtime privilege posture
direct tests + HG/SC/PSV/PG-R traceability
staged evidence that cannot yet be truthfully executed
```

No empty ceremonial directory should be created.

---

## 11. CP6-03 blueprint — global topology already closed

The current canonical blueprint is a long progressive specification in:

```text
docs/database/dante-postgresql-database.md
```

It already contains the following closed global topology.

### 11.1 NativeRef bounded address control — DB-U01

Current technical design:

```text
dante.native_address
  native_ref    uuid PRIMARY KEY
  owner_family  text NOT NULL
```

The `native_ref` is the same stable UUIDv7 already owned by the concrete LR-01 owner; the table does not mint another semantic identity.

The bounded `owner_family` vocabulary is the exact 15 native owner families.

A narrow DB-local dispatcher/constraint trigger is required for the cross-table invariant that PostgreSQL cannot express via an ordinary row-local CHECK:

```text
native_address(native_ref, owner_family)
→ native_ref must exist in the exact concrete owner table selected by owner_family
```

Heterogeneous consumers use FK to `native_address`, plus a consumer-specific bounded owner-family eligibility check.

Homogeneous references bypass `native_address` and use direct owner FKs.

`native_address` remains technical control infrastructure; it must never acquire name/title/status/generic properties/business lifecycle payload.

DB-U01 topology is closed, but destructive owner/address lifecycle behavior still depends on DB-U14.

### 11.2 ScopedRecordRef bounded address control — DB-U02

```text
dante.scoped_address
  scoped_ref     uuid PRIMARY KEY
  scoped_family  text NOT NULL
```

Only concrete contextual/relation families that actually require stable ScopedRecordRef participate.

The final `scoped_family` vocabulary grows only with approved concrete scoped families. It is schema-controlled, not runtime-extensible generic metadata.

Homogeneous scoped references use direct concrete-table FKs. Genuine heterogeneous scoped references use the bounded scoped address mechanism.

DB-U02 topology is closed, but destructive scoped-owner/address lifecycle behavior also depends on DB-U14.

### 11.3 MaterialStateRef control — DB-U03/DB-U04

Current control shape:

```text
dante.material_state_address
  material_state_ref   uuid PRIMARY KEY
  native_owner_ref     uuid NULL
  scoped_owner_ref     uuid NULL
  facet_code           text NOT NULL
```

Exactly one of `native_owner_ref` / `scoped_owner_ref` is non-null.

The two nullable columns distinguish two already-separated address spaces; they are not the forbidden one-of-N owner-FK implementation of a single heterogeneous NativeRef slot.

`facet_code` is schema-owned and globally unambiguous, e.g. conceptually:

```text
agreement.shared_assent
schedule.placement
actual.realization
milestone.context
```

Each facet maps to its exact owner address space/family and exact owner-specific payload family.

The whole-blueprint audit hardened **bidirectional MaterialState totality**. A live MaterialStateRef must never become an address row whose owner-specific material representation disappeared.

Required integrity direction:

```text
material_state_address without required owner-specific representation by COMMIT
→ REJECT

owner-specific payload with wrong state ref/owner/facet
→ REJECT

ordinary deletion of owner-specific payload leaving live MaterialStateRef orphaned
→ REJECT

redaction/tombstone
→ may reduce protected payload only through an owner-specific still-resolvable representation
→ must not convert the MaterialStateRef into a dangling historical fiction
```

Redaction is **not** an exception to MaterialStateRef resolvability.

### 11.4 Current accepted-state binding — DB-U05

Current technical topology uses separate native/scoped control tables, not a generic kind/id root:

```text
dante.native_current_material_state
  native_owner_ref
  facet_code
  material_state_ref
  PRIMARY KEY(native_owner_ref, facet_code)
  UNIQUE(material_state_ref)


dante.scoped_current_material_state
  scoped_owner_ref
  facet_code
  material_state_ref
  PRIMARY KEY(scoped_owner_ref, facet_code)
  UNIQUE(material_state_ref)
```

Narrow integrity validates that current selected MaterialStateRef has the same address space, same owner and same facet.

Current truth is never inferred from latest insertion, UUIDv7 order, provider revision or MAX revision.

### 11.5 Typed lineage — DB-U06

Correction/replacement/supersession/reconciliation lineage remains typed; there is no universal semantic `related_to`/Version edge.

Exact owner-specific relation families are derived where actual semantics require them.

### 11.6 Temporal physical contract — DB-U07

The database preserves the semantic distinctions among:

```text
date-only
floating local wall-clock/date-time
named-zone local date-time + IANA zone
absolute instant / timestamptz
interval/range where semantically exact
duration/elapsed amount
precision/granularity/frame where meaning depends on it
world/effective chronology vs recorded/learned/accepted chronology where material
```

Do not collapse future named-zone intention to UTC-only truth.

DB-U07 remains closed, but some concept-specific coarse representations such as Schedule `Tuesday afternoon` remain open because the upstream model has not yet supplied a deterministic bounded encoding.

### 11.7 Place/PostGIS — DB-U11

Place does **not** receive a mandatory geometry merely because PostGIS is selected.

Baseline Place identity/state may exist without geospatial shape. PostGIS geometry/indexing is materialized only when an accepted Place facet/consumer actually requires the exact shape/SRID/query semantics.

No speculative spatial column/index is created to “use PostGIS”.

### 11.8 Quantity and MonetaryAmount — DB-U13

Both remain LR-04 value semantics owned by containing state, with no independent UUID/reference by default.

Quantity and MonetaryAmount may share low-level numeric infrastructure but remain semantically distinct.

Exact decimals use PostgreSQL `numeric` with finite-value checks where Infinity/NaN would be invalid; `money` is forbidden. Currency remains explicit ISO 4217 semantics.

No generic quantity/value root is introduced.

### 11.9 Capacity Claim — DB-U16

Capacity Claim remains owner/context-specific commitment pressure:

```text
LR-03 qualified commitment relation
LR-02 + ScopedRecordRef only when material history/addressability justifies it
NO native identity
NO universal Reservation root
```

Mandatory separations:

```text
Capacity Claim != Schedule
Capacity Claim != Resource Allocation
Capacity Claim != Actual utilization
Capacity Claim != Ownership/Possession
Capacity Claim != universal inventory/financial reservation
```

No ceremonial capacity-claim row is created where no accepted capacity commitment exists.

---

## 12. Whole-blueprint audit performed before the latest semantic pass

The user explicitly requested a **total control of everything already designed** before continuing.

The audit re-read/cross-checked the accumulated blueprint against:

```text
Whole Logical / Representation Framework
Logical Slice A identity/reference
Slice C time/reality
Slice D evidence/history
Slice E resource/value/capacity
accepted PostgreSQL Physical mapping
PostgreSQL semantic preflight / PM-13 boundaries
CP6-01 Part 1 + Part 2
CP6-02 Constitution
real CP3 metadata/runtime/Alembic/provisioning code
PostgreSQL 18 mechanism behavior where relevant
```

The audit conclusion was **architecture good, several hardenings required before continuing** rather than rollback/rebuild.

### 12.1 Recurrence finding — DB-U12 reopened only at physical boundary

The six accepted semantic Recurrence families remain valid:

```text
1. calendar / wall-clock
2. elapsed interval
3. quota per period
4. completion-relative
5. anchor-stream-relative
6. cyclic positional
```

The defect was the earlier tendency to make every persisted Recurrence an independently scoped/versioned mini-entity.

Upstream authority instead says Recurrence is LR-05 and receives independent ScopedRecordRef/material lifecycle only when independent addressability/reuse/history actually requires it.

Current corrected rule:

```text
OWNER-BOUND RECURRENCE
= default when recurrence is simply a structured material facet/state of a Routine/Event/Temporal Constraint/accepted source

INDEPENDENTLY SCOPED RECURRENCE
= only when a real independent addressability/reuse/reconciliation/lifecycle trigger exists
```

Material history is still preserved in both modes.

Example:

```text
Routine material recurrence state R1
→ historical Occurrence records retain R1 as governing state
→ structural source revision creates source-owned R2
```

or, where justified:

```text
independently scoped Recurrence state R1
→ scoped Recurrence identity + recurrence.definition MaterialStateRef
→ later material rule R2
```

The audit revalidation confirmed this owner-bound/scoped boundary is aligned with Domain, Logical, Physical and CP6-01.

**What remains open:** exact PostgreSQL recurrence physical constraint contract. DB-U12 is not allowed to return to CLOSED until all required semantics are deterministic.

Current open DB-U12 pressure includes:

```text
exact common family header/discriminator topology
material facet codes + owner/family eligibility by source mode
source↔recurrence cardinality for current accepted sources
pattern-anchor requirement per family/parameter combination
calendar selector combination validity
invalid-date policy vocabulary
DST gap policy vocabulary
DST overlap policy vocabulary
historical named-zone accepted-resolution placement where consequential
completion-relative calendar-offset frame/zone semantics
anchor-stream calendar-offset frame/zone semantics
cyclic explicit phase/anchor representation
bounded qualifying-anchor vocabularies
family payload totality/exclusivity
Occurrence governing-state eligibility across both ownership modes
SQLAlchemy shape/migration order/privileges/direct tests
zero placeholder/free-text/JSON policy fields for unclosed semantics
```

No library default may silently become DANTE semantics.

### 12.2 MaterialStateRef totality finding — repaired in blueprint

The earlier design correctly rejected an address row without a payload at commit, but did not sufficiently protect the reverse direction: deleting the child payload could leave a live MaterialStateRef resolving to nothing.

The blueprint was hardened so address ↔ owner-specific material representation totality is bidirectional and destructive lifecycle/redaction must preserve a truthful still-resolvable owner-specific representation.

This hardening is integrated and revalidated PASS.

### 12.3 Runtime privilege/provisioning finding — DB-U21 opened

The real CP3 provisioning code currently has broad bootstrap behavior conceptually equivalent to:

```text
ALTER DEFAULT PRIVILEGES ...
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO dante_runtime

GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA dante
TO dante_runtime
```

That was acceptable for the CP3 technical foundation before immutable/control business objects existed, but it conflicts with the CP6 database model where many objects must be append-only or immutable under ordinary runtime authority.

Current corrected direction:

```text
PROVISIONING
→ owns database roles, role membership, schema/database foundation and global hardening only
→ MUST NOT blanket-grant business-object DML

BUSINESS/CONTROL ALEMBIC MIGRATION
→ owns exact table/view/sequence/type/domain/routine ACLs for the objects introduced/changed by that migration
```

DB-U21 is a **Gate-03 blocker before CP6-04** until the complete object-by-object privilege matrix is closed.

The later CP6-04 code change must also remove/narrow CP3 blanket reconciliation behavior so rerunning provisioning cannot accidentally regrant UPDATE/DELETE on immutable/control tables.

Examples of intended direction, not yet final ACL matrix:

```text
identity owner shell      SELECT + INSERT; stable identity binding not ordinary UPDATE; DELETE gated by lifecycle
address/control row       SELECT + INSERT; no ordinary UPDATE/DELETE
immutable material state  SELECT + INSERT; no ordinary UPDATE/DELETE
current binding           SELECT + INSERT/UPDATE as required; DELETE only through a narrowly proven cessation path
immutable material child relation rows SELECT + INSERT; no ordinary UPDATE/DELETE
integrity trigger routines no direct runtime EXECUTE by default
```

Do not code the provisioning repair until Gate 03 exact matrix closes and the corresponding CP6-04 write gate is approved.

### 12.4 Anchor lifecycle finding

DB-U01/DB-U02 topology remains good. The unresolved part is destructive lifecycle continuity:

```text
concrete owner disappears
while native_address/scoped_address or material history survives
```

must never leave a live address falsely claiming an extant semantic owner.

This is assigned to DB-U14. Do not reopen the anchor architecture itself unless contradictory evidence appears.

### 12.5 PostgreSQL primitive feasibility check

The audit also verified that the selected mechanisms are real PostgreSQL 18 behavior rather than paper architecture. Important confirmations included:

```text
UNIQUE NULLS NOT DISTINCT supported and intentional
constraint triggers can be deferred to transaction end
CHECK is row-local and must not pretend to enforce cross-table existence
PostgreSQL does not automatically index referencing FK columns
numeric admits NaN/+Infinity/-Infinity, therefore DANTE finite-value checks matter where those values are invalid
```

The remaining blockers are DANTE contract specificity, not lack of PostgreSQL capability.

---

## 13. Current global DB-U unresolved register after audit

The current blueprint classifies these global/database items as still open:

```text
DB-U08 final PostgreSQL object naming beyond already-frozen design names
DB-U09 Account persistence — genuinely deferred; detailed access model not closed
DB-U10 Principal/security persistence — genuinely deferred; independent AuthN/AuthZ registry not closed
DB-U12 Recurrence physical ownership/constraint contract — reopened only at physical exactness layer
DB-U14 owner/family lifecycle/tombstone/destructive continuity
DB-U15 remaining structural FK/query indexes after final graph
DB-U17 provider/integration object shapes — deferred until real provider contract
DB-U18 idempotency table timing — deferred until first persistent material operation needs it
DB-U19 transactional outbox timing — deferred until first real Class-A async effect
DB-U20 derived/search/vector persisted structures — deferred until real consumer proves need
DB-U21 object-level runtime privilege matrix + CP3 provisioning reconciliation — Gate-03 blocker
```

Count recorded by current blueprint before pass-II local items:

```text
GLOBAL UNRESOLVED DB-U ITEMS 11
UNCLASSIFIED                0
```

A `GENUINELY DEFERRED` item is a legitimate final CP6-03 disposition only when exact current authority cannot truthfully determine the schema and the later trigger is explicit. It is **not** permission to create a placeholder table now.

---

## 14. Latest completed database design block — Object-level closure pass II

Current branch HEAD at handoff PRE-SCOPE:

```text
bdbd5e8447f27447480c0a9667e7ff63b5c0a9f6
commit: docs(database): close schedule actual milestone agreement topology
```

This commit added the second major object-level closure pass to the canonical blueprint. It derived Schedule / Actual / Outcome / Milestone / Agreement without inventing generic payloads.

### 14.1 Schedule

Closed stable envelope:

```text
dante.schedule
  schedule_ref        uuid PRIMARY KEY
  subject_native_ref  uuid NOT NULL
```

`schedule_ref` is UUIDv7 ScopedRecordRef with matching `scoped_address` family `schedule`.

`subject_native_ref` is a heterogeneous NativeRef contract limited to:

```text
Activity
Event
Occurrence
```

One subject may legitimately own multiple independent Schedule placements. Therefore there is **no global UNIQUE(subject_native_ref)**.

Material Schedule placement uses:

```text
facet_code = schedule.placement

dante.schedule_placement_state
  material_state_ref uuid PRIMARY KEY
  schedule_ref       uuid NOT NULL
```

Current accepted placement uses the scoped current-binding topology. Material reschedule creates a new MaterialStateRef and preserves prior placement history.

Schedule absence is valid. Do not create synthetic `UNSCHEDULED`, `POSTPONED` or `AVAILABLE` rows by convenience.

Open Schedule items:

```text
SCH-U01 exact coarse placement encoding
SCH-U02 current-binding cessation / unscheduling lifecycle + safe privilege path
```

SCH-U01 exists because `Tuesday afternoon` cannot be silently encoded as an invented `12:00–18:00` window or free-text precision code.

SCH-U02 exists because becoming unscheduled must preserve historical Schedule/material state and must not justify blanket DELETE privilege on shared current-binding tables.

### 14.2 Actual

Closed envelope:

```text
dante.actual
  actual_ref          uuid PRIMARY KEY
  subject_native_ref  uuid NOT NULL
```

Scoped family `actual`; subject NativeRef limited to Activity/Event/Occurrence.

Current material realization:

```text
facet_code = actual.realization

dante.actual_realization_state
  material_state_ref    uuid PRIMARY KEY
  actual_ref            uuid NOT NULL
  realization_occurred  boolean NOT NULL
```

Very important missingness semantics:

```text
no established Actual/current realization state
→ UNKNOWN / not established

realization_occurred = false
→ KNOWN NON-REALIZATION

realization_occurred = true
→ SOME realization established
→ does NOT mean completed/successful/passed
```

Where Sessions materially compose a realization state, candidate typed relation:

```text
dante.actual_realization_session
  material_state_ref uuid NOT NULL
  session_ref        uuid NOT NULL
  PRIMARY KEY(material_state_ref, session_ref)
```

Event Actual may exist without Session. Spontaneous Session may exist without Actual.

Open Actual item:

```text
ACT-U01 exact subject cardinality + optional timing/replacement facets
```

A read-only derivation initially considered `UNIQUE(subject_native_ref)` but the audit rejected freezing it because the canonical Actual authority had explicitly deferred final physical cardinality. This is a deliberate hardening, not a semantic reopening.

### 14.3 Outcome

Closed semantic dependency:

```text
Outcome
→ contextual result/disposition of an exact Actual realization context
```

But current authority rejects a universal result vocabulary. Therefore **no universal concrete Outcome table is implementation-authorized**.

Forbidden placeholder/fallback shapes include:

```text
dante.outcome(result_code text)
universal Outcome ENUM
global completed/partial/skipped/passed/failed taxonomy
JSONB result payload as semantic escape hatch
one Outcome per participant by default
```

If a real concrete Outcome family later becomes material/addressable, its envelope must use a ScopedRecordRef and direct FK to the exact Actual.

Open item:

```text
OUT-U01 first concrete typed Outcome result family
```

Until that closes, the correct CP6 disposition is **no universal result payload**, not a fake generic schema.

### 14.4 Milestone

Closed contextual owner:

```text
dante.milestone
  milestone_ref uuid PRIMARY KEY
```

Scoped family `milestone`.

Milestone meaning requires at least one Goal and/or Plan and may truthfully involve multiple of each. No rigid Goal→Plan→Milestone parent tree.

Current material context topology:

```text
facet_code = milestone.context

dante.milestone_context_state
  material_state_ref uuid PRIMARY KEY
  milestone_ref      uuid NOT NULL

dante.milestone_context_goal
  material_state_ref uuid NOT NULL
  goal_ref           uuid NOT NULL
  PRIMARY KEY(material_state_ref, goal_ref)

dante.milestone_context_plan
  material_state_ref uuid NOT NULL
  plan_ref           uuid NOT NULL
  PRIMARY KEY(material_state_ref, plan_ref)
```

Deferred by-commit invariant:

```text
COUNT(goal links) + COUNT(plan links) >= 1
```

Multiple Goal/Plan links are valid.

Do **not** create generic Milestone columns such as:

```text
reached boolean
status enum
progress_percent
completed_at
```

Attainment remains Evidence/Evaluation-backed. Target date/window is temporal target semantics, not Schedule placement.

Open item:

```text
MIL-U01 exact definition/target/attainment physical facet split
```

### 14.5 Agreement

Closed scoped contextual owner:

```text
dante.agreement
  agreement_ref uuid PRIMARY KEY
```

Agreement is true n-ary mutual assent to the **same exact material terms state**, not pairwise `agreed_with` edges.

Current material state:

```text
facet_code = agreement.shared_assent

dante.agreement_shared_assent_state
  material_state_ref       uuid PRIMARY KEY
  agreement_ref            uuid NOT NULL
  terms_material_state_ref uuid NOT NULL
```

Party set:

```text
dante.agreement_party_assent
  agreement_material_state_ref uuid NOT NULL
  party_native_ref             uuid NOT NULL
  PRIMARY KEY(agreement_material_state_ref, party_native_ref)
```

Party NativeRef family is bounded to:

```text
Person
Collective
```

All parties in the n-ary state are bound structurally to the same parent terms MaterialStateRef. An amendment produces a new material terms/assent state; prior assent is not silently inherited.

Do not collapse Representation/on-behalf-of semantics into party identity.

Open item:

```text
AGR-U01 Agreement terms-state eligibility + consequential assent provenance
```

Not every arbitrary MaterialStateRef may serve as Agreement terms. Exact eligible owner/facet set and Representation/Authority/Provenance binding still need closure.

---

## 15. Pass-II local unresolved register

Current local object-level open items from the latest pass:

```text
SCH-U01  coarse accepted Schedule placement encoding
SCH-U02  Schedule current-binding cessation / unscheduling operation
ACT-U01  Actual exact cardinality + optional timing/replacement facets
OUT-U01  first concrete typed Outcome result family
MIL-U01  Milestone definition/target/attainment facet split
AGR-U01  Agreement terms-state eligibility + assent provenance
```

All six are classified. None authorizes a placeholder schema.

The latest pass ended with:

```text
Schedule envelope/subject/material ownership       CLOSED
Schedule coarse encoding + cessation path          OPEN

Actual envelope/subject/realization axis            CLOSED
Actual exact cardinality/optional facets            OPEN

Outcome universal fallback                          REJECTED
Outcome first concrete typed family                 OPEN

Milestone scoped identity + Goal/Plan context       CLOSED
Milestone target/attainment split                   OPEN

Agreement scoped n-ary same-terms topology          CLOSED
Agreement terms eligibility/provenance              OPEN

PASS-II UNCLASSIFIED                                0
CP6 BUSINESS DDL AUTHORIZED                         NO
GATE 03                                             NOT YET EARNED
```

---

## 16. Current object-level privilege direction after pass II

The exact DB-U21 matrix is still open, but the pass-II objects constrain it further.

Current design direction:

```text
schedule / actual / milestone / agreement semantic owner rows
→ runtime SELECT + INSERT for accepted creation paths
→ PK/subject binding ordinary UPDATE denied
→ DELETE denied until DB-U14 proves exact lifecycle

schedule_placement_state
actual_realization_state
milestone_context_state
agreement_shared_assent_state
→ runtime SELECT + INSERT
→ UPDATE denied after acceptance
→ DELETE denied except a future explicit lifecycle/redaction mechanism preserving MaterialState totality

actual_realization_session
milestone_context_goal
milestone_context_plan
agreement_party_assent
→ immutable components of accepted material state
→ ordinary UPDATE/DELETE denied

current binding
→ INSERT/UPDATE as required
→ Schedule cessation DELETE remains specifically gated by SCH-U02

integrity routines
→ no direct runtime EXECUTE by default

UUIDv7 semantic identities
→ no sequence required by default
```

Exact GRANT/REVOKE must be owned by the migration that creates each object.

---

## 17. Index posture after pass II

Do not index every FK reflexively.

Currently accepted structural indexes/keys from pass II are mostly PK/composite PK structures:

```text
schedule PK(schedule_ref)
actual PK(actual_ref)
milestone PK(milestone_ref)
agreement PK(agreement_ref)

actual_realization_session PK(material_state_ref, session_ref)
milestone_context_goal PK(material_state_ref, goal_ref)
milestone_context_plan PK(material_state_ref, plan_ref)
agreement_party_assent PK(agreement_material_state_ref, party_native_ref)
```

Possible additional indexes on:

```text
schedule.subject_native_ref
actual.subject_native_ref
goal_ref
plan_ref
party_native_ref
session_ref
terms_material_state_ref
```

remain under DB-U15 until the complete FK/query/delete-check graph justifies them.

Do not add Schedule GiST/EXCLUDE merely because Schedule uses temporal ranges. Time overlap is not universally a Schedule conflict; actual feasibility/conflict belongs to Capacity/Availability/owner-specific policy.

---

## 18. Current Gate-03 acceptance bar

The current workstream/blueprint requires CP6-03 to earn all of these kinds of closure before real business materialization begins:

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

**Do not call Gate 03 PASS while unresolved Gate-03 blockers still exist.**

The blueprint currently says Gate 03 is **NOT YET EARNED**.

---

## 19. Exact next work from current repository truth

The latest blueprint explicitly states that the **next semantic pass should consume the specific LR-03 relation/governance families and the Criterion/Evaluation/Temporal Constraint pressures needed to close the remaining dependencies**, instead of inventing placeholder payloads for Schedule/Actual/Outcome/Milestone/Agreement.

Therefore do **not** immediately start writing Alembic or SQLAlchemy.

Recommended next analysis block:

```text
A. Specific LR-03 relations / governance
   Responsibility
   Participation
   Coordination Stewardship
   Authority
   Visibility
   Consent
   Representation
   Membership
   Contribution
   Ownership
   Possession
   Interpersonal Relationship
   Resource Allocation / Dependency / attestation/evidence relations as required by dependency graph

B. Rule/evaluation pressure required by currently-open pass-II items
   Criterion
   Evaluation / Verification
   Temporal Constraint
   relevant Availability / Resource Requirement interactions where needed

C. Use the above to close or narrow
   AGR-U01
   MIL-U01
   SCH-U01 / SCH-U02 where upstream temporal/governance/lifecycle pressure becomes deterministic
   ACT-U01 where relation/reconciliation semantics determine cardinality/replacement
   OUT-U01 only if a genuinely typed result family is actually derivable now
```

The next pass must use the standard per-object derivation chain:

```text
1. consume complete canonical Domain + Logical authority
2. define exact table(s) / or classify no independent persistence
3. define columns and exact persisted meanings
4. define PK/FK/Reference Contract
5. define NULL/missingness
6. define UNIQUE/CHECK/EXCLUDE/trigger integrity
7. define material-state/current/history behavior
8. define lifecycle/delete behavior
9. justify indexes
10. define SQLAlchemy mapping shape
11. define migration dependencies
12. define direct PostgreSQL tests
13. define exact object-level privileges
14. add/update Database Dictionary entry when the object is approved for the system-of-record phase
15. close/update affected global/local unresolved item
```

No object is complete before this chain is satisfied or explicitly marked not-applicable/deferred for a justified reason.

---

## 20. Required audit immediately after the next design block

Once the next relation/governance/rule block is added, stop and run another **whole accumulated audit** before opening another block.

Minimum audit questions:

```text
Does any new table accidentally create a semantic root?
Did any LR-03 relation become generic edge infrastructure?
Did a role become wrapper identity?
Did a scoped record get promoted to NativeRef without justification?
Did any MaterialStateRef become ownerless/dangling or lose bidirectional totality?
Does current binding still preserve owner/facet/address-space exactness?
Did we add silent latest-write/currentness semantics?
Did any relation lose n-ary/role/context meaning?
Did provider/derived/security/runtime state become canonical?
Did absence become a negative by row omission?
Did lifecycle/delete behavior contradict history/tombstone/MaterialState totality?
Did object privileges accidentally give UPDATE/DELETE on immutable/control structures?
Did any new FK/reference become application-only rather than DB-enforced?
Did a CHECK try to enforce cross-table truth it cannot enforce?
Did indexes become speculative?
Did any recurrence/schedule/time rule invent precision/policy not closed upstream?
Did SQLAlchemy mapping direction introduce a generic semantic superclass?
Does the migration DAG still have a safe implementable order?
Can each promised PostgreSQL invariant actually be proven directly?
Did any staged HG/SC/PSV obligation get falsely relabeled PASS?
Does the current Database System of Record remain internally coherent?
```

If any material finding appears, repair and revalidate before continuing.

---

## 21. What must NOT happen in the next session

Do not:

- start CP6-04 because several tables now have names;
- call CP6-03 complete while DB-U/open local items remain;
- invent Account/Principal tables because authentication will eventually exist;
- create a generic `outcome(result_code)` table;
- create a generic `rule(type,json)` or `relationship(from,type,to)` table;
- make every Recurrence independently scoped;
- invent DST/invalid-date/day-part policies to make SQL easy;
- use JSONB/free text as a placeholder for semantics not yet closed;
- add `deleted_at`/`is_deleted` to everything;
- give runtime blanket UPDATE/DELETE on all business tables;
- make trigger routines executable by runtime just because triggers use them;
- use PostgreSQL RLS as Domain Authority/Consent/Visibility truth;
- infer current material state from latest timestamp/revision/UUID;
- make every relation or material child row a UUID entity;
- add indexes merely because a column is an FK;
- add PostGIS/FTS/pgvector objects merely because those technologies were selected;
- activate PgBouncer/PowerSync/Restate/R2/pgBackRest/OR-Tools merely to complete a checklist;
- create use cases/services/API/frontend inside CP6;
- modify code/migrations/provisioning before the corresponding Gate-03 contract is closed and an exact CP6-04 write gate is approved;
- rewrite historical Physical/CP3 evidence to match current patch/version language;
- treat this temporary handoff as higher authority than newer Git truth.

---

## 22. CP6-04 — later, only after Gate 03 is actually clean

When Gate 03 is earned, CP6-04 will materially implement the approved blueprint in bounded dependency-DAG batches.

Authorized classes after exact per-batch gates include:

```text
Alembic business-schema revisions
DANTE business/control tables
owner-specific canonical tables
bounded native/scoped/material address control
owner-specific material-state/history rows
specific typed relation tables
provider/integration DB structures only where already determined
bounded derived/query persistence only where already determined
PostgreSQL constraints/indexes
SQLAlchemy mappings/metadata
mapping-specific value types/codecs
exact object privileges/grants
real PostgreSQL acceptance fixtures/tests
schema drift checks
same-change database dictionary/reference updates
```

Each batch must have:

```text
exact PRE-SCOPE/path gate
migration dependency relation
fresh DB → Alembic head proof
negative constraint/reference proof where executable
schema/metadata drift proof
actual runtime/migrator role privilege proof
remote readback and exact delta
```

Do not build one giant migration if the dependency DAG supports safer bounded batches.

Likely early dependency order remains conceptually:

```text
CP3 technical base
→ approved control/address structures
→ LR-01 identity shells
→ approved scoped contextual owners
→ material-state payload families/current bindings
→ specific relation/rule/history families
→ later provider/derived objects only if actually determined
```

But the final DAG must come from completed Gate 03, not this simplified handoff.

---

## 23. CP6-05 — eventual whole database QA

CP6-05 must directly prove the materialized database against the blueprint/model using real PostgreSQL where PostgreSQL semantics matter.

Expected lanes include, where executable:

```text
fresh DB → Alembic head
one canonical Alembic head
SQLAlchemy/Alembic/PostgreSQL drift alignment
owner/migrator/runtime privilege matrix
valid + invalid reference integrity
wrong-family rejection
dangling-reference rejection
CHECK/UNIQUE/EXCLUDE positive+negative cases
missingness/unknown/negative distinctions
MaterialState owner/facet/payload/current binding integrity
bidirectional MaterialState totality
history reconstruction/correction without false overwrite
expected-state/concurrency real multi-connection race where subject exists
idempotency real duplicate/conflicting fingerprint behavior if materialized
transaction rollback/atomicity
truthful downgrade/evolution semantics
PostGIS/FTS/pgvector only where actual schema uses them
database documentation/dictionary vs Alembic/SQLAlchemy/real-schema consistency
```

Some obligations remain honestly staged until a real V1→V2, destructive restore, real product workflow or specialist activation exists. Do not fake those PASSes.

Important staged examples include:

```text
HG-09 destructive retention/restore
HG-11 real semantic V1→V2 evolution
HG-12 destructive recovery
PSV-01 old-backup anti-resurrection
application-level governed-effect scenarios requiring a real use case
specialist-capability proof with no activated consumer
```

---

## 24. Intended CP6 closure state

The workstream may close only when repository truth supports something equivalent to:

```text
CP6
CLOSED / CONCRETE POSTGRESQL DATABASE PASS

DANTE DATABASE
BLUEPRINT COMPLETE
MATERIALIZED TO MAXIMUM NON-SPECULATIVE EXTENT
MIGRATED
MAPPED
DIRECTLY TESTED
DATABASE DOCUMENTATION IN SYNC
QA CLEAN

FIRST PRODUCT VERTICAL
NOT YET IMPLEMENTED
NEXT SEPARATE PHASE
```

The first product vertical must consume this already-designed/materialized database. It does not start by inventing a separate DB from scratch. Later schema evolution is normal only for requirements that genuinely could not have been determined earlier.

---

## 25. User expectations / quality bar for continuation

The working style matters as much as the technical content.

The user expects:

```text
repo-first truth
no arbitrary implementation
no yes-man behavior
professional/enterprise standard
exact gates before writes
complete readback after writes
strong audit before progression
no speed/quality trade unless explicitly discussed
open-source / zero-cost preferred when quality is equivalent
paid option discussable only if materially better
no ceremonial documentation proliferation
useful durable documentation where it genuinely helps future maintenance
```

If a design is wrong, say it is wrong and fix it. Do not preserve a prior answer just because it was previously written.

If a direction is sound but was declared CLOSED too early, reclassify it precisely rather than pretending it is fully deterministic.

If something is genuinely unknowable without a future product/provider/specialist contract, classify it explicitly and **do not invent placeholder schema**.

Keep user-facing progress updates concise during long reviews, but show material findings as soon as they are discovered.

---

## 26. Resume checklist for the next chat

A fresh session is aligned only after it can answer all of these correctly from current repository truth:

```text
[ ] What is the live feature/logical-postgresql HEAD?
[ ] What is its relation to protected main?
[ ] CP6-00 COMPLETE?
[ ] CP6-01 CLOSED / Gate 01 PASS?
[ ] CP6-02 CLOSED / Gate 02 PASS?
[ ] CP6-03 ACTIVE / Gate 03 NOT YET EARNED?
[ ] Why does CP6 include the real database, while the first application vertical is post-CP6?
[ ] What are the exact 15 LR-01 owners?
[ ] Why are Actor/Subject/Resource not wrapper identities?
[ ] What are NativeRef/ScopedRecordRef/MaterialStateRef/ExternalRef?
[ ] Why is material_state_address technical control, not a universal Version/Fact table?
[ ] How is current accepted state represented?
[ ] Why is MaterialState totality bidirectional?
[ ] Why is redaction not permission to leave a dangling MaterialStateRef?
[ ] Why was DB-U12 partially reopened?
[ ] What remains valid about the six Recurrence families?
[ ] What is owner-bound vs independently scoped Recurrence?
[ ] Why is DB-U21 a blocker before CP6-04?
[ ] Why must provisioning stop blanket business DML grants?
[ ] What did pass II close for Schedule?
[ ] What is SCH-U01 / SCH-U02?
[ ] What did pass II close for Actual?
[ ] Why is Actual absence != known non-realization?
[ ] What is ACT-U01?
[ ] Why is there no universal Outcome table yet?
[ ] What is OUT-U01?
[ ] What exact Milestone Goal/Plan context topology is accepted?
[ ] What is MIL-U01?
[ ] How does Agreement preserve n-ary same-terms assent?
[ ] What is AGR-U01?
[ ] What are DB-U08/09/10/12/14/15/17/18/19/20/21?
[ ] Why is CP6 business DDL still unauthorized today?
[ ] What semantic/governance/rule block comes next?
[ ] What whole-blueprint audit must follow that block?
```

Only after those are resolved from live Git should the temporary handoff be considered consumed and eligible for deletion.

---

## 27. Immediate continuation sentence

If nothing newer exists on the branch, resume with:

> **CP6-03 remains ACTIVE at the post-pass-II blueprint. Do a read-only derivation of the next specific LR-03 relation/governance + Criterion/Evaluation/Temporal Constraint block, using complete Domain/Logical authority. Do not write until the exact next gate is presented. Use that block to close/narrow AGR-U01, MIL-U01, SCH-U01/02, ACT-U01 and only close OUT-U01 if a genuinely typed result family is derivable. After the write, run another whole accumulated blueprint audit against Domain + Logical + Physical + CP6-01 + CP6-02 + real CP3 code before opening any further block. CP6-04 remains forbidden until Gate 03 is actually earned.**
