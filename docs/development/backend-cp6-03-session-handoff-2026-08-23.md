# Backend CP6-03 — Session Continuation Handoff — 2026-08-23

- **Status:** TEMPORARY CONTINUATION HANDOFF / READ FIRST IN NEXT SESSION
- **Product:** DANTE (historical documents may still say LifeOS)
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/logical-postgresql`
- **Purpose:** allow a fresh ChatGPT session to resume this exact CP6-03 database-design conversation without losing architectural decisions, process discipline, current findings, or the immediate next action.
- **Deletion rule:** this file is intentionally temporary. A later session may delete it only after it has fully re-established repository truth from the durable authorities listed below and no longer needs this handoff as continuity scaffolding.
- **Important:** repository truth outranks this handoff if the branch advances after this file is written.

---

## 1. Read this first — exact current project position

DANTE has already completed the semantic and technology-selection stages that precede concrete database design.

Current architecture progression is:

```text
CLOSED DOMAIN MODEL
        ↓
CLOSED LOGICAL MODEL
57 / 57 concepts classified
WL-H01..WL-H12 active
        ↓
CLOSED / SELECTED / ACCEPTED PHYSICAL MODEL
PostgreSQL 18 canonical primary
        ↓
BACKEND CP1–CP5
technical foundation implemented / direct QA pass
        ↓
CP6-00 COMPLETE
CP6-01 CLOSED / GATE 01 PASS
CP6-02 CLOSED / GATE 02 PASS
        ↓
CP6-03 ACTIVE
WHOLE DANTE DATABASE BLUEPRINT
        ↓
CP6-04
WHOLE DANTE DATABASE MATERIALIZATION
        ↓
CP6-05
WHOLE DATABASE DIRECT QA + CP6 CLOSURE
        ↓
POST-CP6
FIRST PRODUCT VERTICAL APPLICATION PHASE
```

Critical boundary:

```text
DATABASE DESIGN + DATABASE IMPLEMENTATION
= CP6

FIRST APPLICATION VERTICAL
= AFTER CP6
```

CP6 is **not** only a generic persistence foundation. It must derive and materially implement the maximum non-speculative DANTE database that is already determinable from CLOSED Domain + Logical + Physical + CP6 authority.

The first product vertical does **not** invent its database from scratch. It consumes the database produced by CP6 and may trigger later reviewed schema evolution only if a requirement genuinely could not have been determined earlier.

---

## 2. Mandatory working style — preserve this standard

The user explicitly wants a professional, large-system/enterprise-quality engineering process and does not want speed traded for correctness.

Operating discipline:

```text
NO arbitrary implementation
NO inventing semantics to make SQL easier
NO yes-man behavior
NO broad refactors outside the approved scope
NO generic abstractions merely for uniformity
NO undocumented schema decisions
NO speculative infrastructure activation
NO fake PASS claims
NO rewriting historical evidence
```

Repository-first truth is mandatory.

For every material write:

```text
1. read/verify relevant authority
2. define exact bounded write gate
3. identify live PRE-SCOPE
4. user approval authorizes only that exact gate
5. verify HEAD == PRE-SCOPE immediately before write
6. write only approved paths
7. remote readback
8. exact PRE-SCOPE → HEAD delta
9. added / modified / deleted / unexpected path check
10. branch relation to protected main
11. applicable validation/tests
12. truthful checkpoint status
```

A design discussion is not write approval.

A user `vai` approves only the specifically presented gate.

Docs-only work does not manufacture runtime test evidence.

Do not call a gate PASS/CLOSED until its evidence contract is actually satisfied.

---

## 3. New review cadence agreed in the saturated session

The user explicitly requested an iterative accumulated-audit method instead of building the whole blueprint and reviewing only at the end.

Use this cadence from now until the real database exists:

```text
DESIGN ONE CONCRETE BLOCK
        ↓
AUDIT THE ENTIRE ACCUMULATED DATABASE BLUEPRINT
against Domain + Logical + Physical + CP6-01 + CP6-02 + CP3 real code
        ↓
CLASSIFY FINDINGS
A. still sound
B. sound direction but closed too early
C. concrete defect / blocker
        ↓
REPAIR EVERYTHING MATERIAL
        ↓
READBACK / RE-AUDIT
        ↓
ONLY THEN START NEXT BLOCK
```

Repeat this after each major semantic/database block.

Before CP6-04, perform another whole-blueprint clean review.

After CP6-04 materialization, perform whole real-database QA before CP6 closure.

The intent is to prevent individually plausible decisions from composing into an inconsistent database.

---

## 4. Durable authority chain to reconstruct before continuing

Do not rely on this handoff alone.

### Repository/process bootstrap

Read/verify at minimum:

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
```

### Current CP6 authority

```text
docs/workstreams/logical-postgresql.md
```

This is the current execution-boundary authority and supersedes stale earlier CP6 staging prose.

### Current database documentation authority

```text
docs/database/README.md
docs/database/dante-postgresql-database.md
```

### CP6-01

```text
docs/development/backend-cp6-01-concrete-persistence-coverage.md

docs/development/backend-cp6-01-concrete-persistence-coverage-part-2.md

docs/development/backend-cp6-01-concrete-persistence-coverage-closure.md
```

Part 1 owns exact 57/57 Domain concept coverage.

Part 2 owns cross-cutting/non-owner persistence coverage and is mandatory because:

```text
57 / 57 Domain coverage
is necessary
but NOT sufficient
```

### CP6-02

```text
docs/development/backend-cp6-02-postgresql-persistence-constitution.md

docs/development/backend-cp6-02-postgresql-persistence-constitution-closure.md

docs/decisions/ADR-010-postgresql-persistence-constitution.md
```

### Logical authorities

At minimum:

```text
docs/logical-model/whole-logical-model-v1.md
docs/logical-model/representation-framework-v1.md
docs/logical-model/slices/identity-reference-v1.md
docs/logical-model/slices/time-reality-v1.md
docs/logical-model/slices/evidence-knowledge-history-v1.md
docs/logical-model/slices/resources-values-capacity-v1.md
```

Also consume the remaining accepted Logical slices/checkpoints as required by each concept block rather than reasoning from memory.

### Physical PostgreSQL authorities

At minimum:

```text
docs/physical-model/pm-02-primary-mapping-overview-v1.md
docs/physical-model/mappings/postgresql-18.4-v1.md
docs/physical-model/preflight/postgresql-18.4-v1.md
docs/physical-model/pm-11-explicit-selection-v1.md
docs/physical-model/pm-12-accepted-physical-model-v1.md
docs/physical-model/pm-13-clean-room-qa-v1.md
docs/physical-model/result-register-v1.md
docs/physical-model/recommendation/post-selection-validation-register-v1.md
```

The 18.4 files are historical exact Physical evidence. Do not rewrite them as 18.6.

### Domain concept specs

For every object-level derivation, consume the complete relevant Domain concept documents. Do not infer exact persistence from the 57-row summary alone.

This was especially important for `Recurrence`: its complete Domain document contained deferred ownership/entity-value boundaries that the shorter ledgers did not fully communicate.

---

## 5. Closed semantic baseline — do NOT casually reopen

### 57 / 57 Logical concepts

The Logical Model is closed for current scope.

Exact native LR-01 owners are 15:

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

Do not add another LR-01 owner merely for persistence convenience.

Contextual roles remain:

```text
Actor
Subject
Resource
```

They are roles/capabilities, not wrapper identities.

Therefore no universal:

```text
ActorRef
SubjectRef
ResourceRef
```

### Reference family separation

Preserve:

```text
NativeRef
!= ScopedRecordRef
!= MaterialStateRef
!= ExternalRef
```

Logical `ReferenceAddress` is representation vocabulary only, not a Domain Entity/Thing superclass.

### State layers

Preserve:

```text
canonical DANTE state
material historical state
derived / projection state
external / provider state
unresolved / candidate state
security / AuthZ runtime state
```

Storage coincidence does not make those semantics identical.

### High-risk non-collapses

At minimum preserve:

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
AI/solver result != accepted canonical effect
```

---

## 6. Closed PostgreSQL physical thesis

The accepted PostgreSQL database direction remains:

```text
owner-specific canonical tables/families
+
owner-specific material-state/history tables/families
+
specific relation tables/families
+
bounded technical address/control structures only where heterogeneous addressing/control genuinely requires them
+
separate provider / projection / technical concerns
```

Globally rejected:

```text
universal Entity / Thing table
universal Relationship / generic edge table
canonical EAV / property bag
universal event log as ontology
universal Fact / Version semantic payload table
required-semantic JSONB escape hatch
PostgreSQL inheritance as ontology
```

Do not revive these shortcuts during object-level design.

---

## 7. Current PostgreSQL / backend technology truth

Architecture:

```text
PostgreSQL major 18
```

Historical exact Physical/CP2/CP3 patch:

```text
PostgreSQL 18.4
```

Current CP6 technical patch:

```text
PostgreSQL 18.6
```

Current directly regressed technical stack includes:

```text
Python       3.14.7
SQLAlchemy   2.0.52
Alembic      1.19.1
psycopg      3.3.4
PostGIS      3.6.4
pgvector     0.8.6
PgBouncer    1.25.2 selected, not automatically activated
```

18.6 foundation evidence:

```text
Backend CI run        32568664940
executed HEAD         ec3dc795b5e044daa3a77723c94a1b4b5b92865c
Backend Quality       32 / 32 fast tests PASS
Backend PostgreSQL    18 / 18 real PostgreSQL tests PASS
Backend CI Gate       SUCCESS
```

Do not misreport this as one 50/50 pytest run. It is a 50-test corpus covered across two mandatory CI lanes.

---

## 8. Current real CP3 implementation foundation

No DANTE business schema has been materially implemented yet beyond CP3 technical baseline.

### Alembic

Current migration tree has one baseline business-independent technical revision:

```text
apps/backend/migrations/versions/20260820_01_cp3_persistence_baseline.py
```

Alembic is the sole deployed application-schema evolution authority.

One environment / one DAG / one head.

No `metadata.create_all()` deployment authority.

### SQLAlchemy metadata

Current canonical metadata:

```text
schema = dante
one Base / one MetaData
CP3 deterministic naming convention
```

Do not create a second independent business MetaData.

### Runtime/session posture

Real current code already uses:

```text
one AsyncEngine per process
one async_sessionmaker per process
one AsyncSession per application operation
autobegin=False
autoflush=True
expire_on_commit=False
pool_pre_ping=True
outer application operation owns commit/rollback
adapter may flush, never implicit commit
READ COMMITTED default
stronger isolation/locking selected by invariant
```

No generic Repository/UoW/BaseService is wanted merely to make the persistence layer look uniform.

### Database roles

Current role model:

```text
dante_owner      NOLOGIN object/schema owner
dante_migrator   LOGIN NOINHERIT + bounded SET ROLE dante_owner
dante_runtime    LOGIN NOINHERIT runtime identity
```

This role architecture remains valid, but the **current broad runtime table grants must be hardened before CP6-04**, as explained later in this handoff.

---

## 9. CP6-01 current closed coverage

### Part 1

Exact 57/57 concept coverage and persistence pressure.

Examples:

```text
Agreement
→ LR-02 n-ary contextual + typed assent
→ terms MaterialStateRef required

Recurrence
→ LR-05 typed rule/specification
→ Scoped/Material conditional
→ exact material rule state required when historical Occurrences depend on it

Schedule
→ LR-02 dependent semantic record
→ Scoped + Material when consequential/addressable

Quantity / MonetaryAmount
→ LR-04 values
→ no independent identity by default
```

### Part 2

Cross-cutting/non-owner constructs include at minimum:

```text
ReferenceAddress / Reference Contract
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
current accepted-state binding
correction/replacement/reconciliation lineage
world/effective chronology
recorded/learned/accepted chronology
Governed Operation / Effect Contract
idempotency
correlation/causation
Projection / Disclosure Surface
provider/sync/apply state
flexible metadata
candidate/unresolved
product/profile
specialist extension
Account
Principal/security context
Actor / Subject / Resource role addressing
Capacity Claim pressure
tombstone/retirement/redaction continuity
anti-resurrection reconciliation
transactional outbox capability-triggered state
PowerSync/local noncanonical state boundary
search/vector/derived pressure
```

At Gate 03 every persistence-relevant Part-2 entry must be classified exactly as:

```text
MATERIALIZE IN CP6
NO INDEPENDENT PERSISTENCE
GENUINELY DEFERRED
```

No unclassified entry is allowed.

---

## 10. CP6-02 closed PostgreSQL Constitution — important rules

### Identity

```text
DANTE stable independent IDs
→ PostgreSQL native uuid
→ UUIDv7
→ backend application boundary generation by default
```

UUIDv7 ordering/timestamp is not semantic chronology.

Not every row/value receives UUID.

### References

```text
homogeneous NativeRef
→ direct FK

genuinely heterogeneous NativeRef
→ bounded native-address mechanism
```

Application-only `type + uuid` is forbidden.

One-of-N nullable FKs are forbidden as an alternate encoding of one heterogeneous NativeRef slot.

Default FK delete behavior:

```text
ON DELETE NO ACTION
```

CASCADE requires semantic lifecycle proof.

### Material state

MaterialStateRef is stable semantic state identity and is never:

```text
xmin/xid
updated_at
ETag
row hash
provider revision
latest row
```

Required topology:

```text
bounded material-state address/control
+
exact owner/facet
+
owner-specific material-state payload
+
explicit current accepted-state binding where required
+
typed correction/replacement/reconciliation lineage
```

Accepted material states are immutable-by-policy; correction normally creates a new state.

### Missingness

```text
NULL / row absence
!= global false/declined/unknown/redacted/etc.
```

No magic sentinel values.

### Types

```text
native PostgreSQL types preferred
PostgreSQL money forbidden
MonetaryAmount = exact numeric + explicit currency semantics
JSONB only bounded
```

### Relations

Specific relation families only.

Qualified/material relation becomes contextual record.

True n-ary semantics remain n-ary.

### Constraints/indexes

Declarative-first.

PostgreSQL CHECK is row-local and must not pretend to enforce cross-table truth.

FK referencing columns are reviewed individually because PostgreSQL does not automatically create indexes on the referencing side.

No speculative partitioning/sharding.

### Transactions/concurrency

```text
declarative invariant
→ expected-state / conditional update
→ deterministic lock
→ SERIALIZABLE only where required
```

No network/human wait inside DB transaction.

Serializable retry = whole application transaction, bounded and explicit.

### Idempotency

```text
UNIQUE(operation_scope, idempotency_key)
material fingerprint separate
```

Same key + same fingerprint → replay/observe result.

Same key + different fingerprint → conflict.

### Migration

Alembic sole application-schema authority.

Applied history immutable.

Autogenerate is candidate only.

No fake downgrade.

Non-transactional DDL is isolated explicitly.

### Security

Runtime is least-privilege, not blanket full DML by principle.

Runtime gets only the DML actually required by an object/family.

---

## 11. Enterprise-grade database documentation decision

The user explicitly requested database documentation at the standard expected from large mature systems.

Adopted repository-native pattern:

```text
docs/database/
├── README.md
├── dante-postgresql-database.md       # human architecture/reference
├── dictionary/                        # machine-readable object dictionary when real objects are ready
├── generated/                         # generated structural reference when useful
├── diagrams/                          # derived/generated where practical
└── evolution/                         # only for genuinely complex evolutions
```

Do not create empty ceremonial directories.

Permanent target invariant:

```text
DATABASE ARCHITECTURE & REFERENCE
≈ DATABASE DICTIONARY
≈ SQLALCHEMY METADATA / MAPPINGS
≈ ALEMBIC HEAD
≈ REAL POSTGRESQL SCHEMA
```

A mismatch is a defect.

Structural DB changes are incomplete unless affected database documentation/dictionary is updated in the same reviewed change.

The dictionary must eventually capture, where applicable:

```text
purpose / semantic role
source authority
columns + exact persisted meaning
PostgreSQL types
nullability/defaults
PK/FK/cardinality/delete behavior
UNIQUE/CHECK/EXCLUDE/trigger integrity
indexes + justification
MaterialState/current/history behavior
lifecycle/redaction/tombstone
security privileges
migration traceability
SQLAlchemy mapping
real direct tests
HG/SC/PSV/PG-R traceability
staged evidence
```

Generate machine facts where reliable; human-author semantic purpose/why.

---

## 12. CP6-03 current durable blueprint

Canonical file:

```text
docs/database/dante-postgresql-database.md
```

This is already a substantial active blueprint, not a blank shell.

Current major content includes:

```text
identity topology
reference topology
native_address
scoped_address
material_state_address
current material-state bindings
typed lineage direction
temporal physical contract
15 LR-01 identity-shell baseline
Place/PostGIS baseline decision
Recurrence current candidate physical contract
Quantity / MonetaryAmount value contract
Capacity Claim disposition
unresolved DB-U register
Gate 03 acceptance contract
```

No business migration or SQLAlchemy business mapping has been authorized merely because these candidate designs exist.

---

## 13. CP6-03 decisions that remain strong after the latest whole-audit

The latest accumulated audit re-read the blueprint against Logical, Representation Framework, multiple Logical slices, Physical PostgreSQL mapping/preflight, CP6-01, CP6-02 and the real CP3 code.

The following remain architecturally sound and should **not** be casually reopened:

```text
15 LR-01 owner set
UUIDv7 + native PostgreSQL uuid
one PostgreSQL schema dante
one SQLAlchemy Base/MetaData
NativeRef / ScopedRecordRef / MaterialStateRef / ExternalRef separation
homogeneous direct FK / heterogeneous bounded address anchor
technical native_address concept
technical scoped_address concept
technical material_state_address concept
explicit current accepted-state binding
owner-specific semantic state payloads
typed lineage; no generic lineage graph ontology
temporal type separation
six Recurrence semantic families
Place with no mandatory geometry in baseline
Quantity / MonetaryAmount as value semantics
Capacity Claim non-universal disposition
NO ACTION default
no generic Entity
no generic Relationship
no EAV
no universal event sourcing
no required semantic JSONB payload
PostgreSQL 18 architecture
CP3 session/transaction architecture
```

The PostgreSQL primitives selected were also rechecked conceptually against PostgreSQL 18 behavior. No blocker was found in the database capabilities themselves:

```text
UNIQUE NULLS NOT DISTINCT       available/correct when semantics require it
constraint triggers            can be deferred when appropriate
CHECK                          row-local; cross-table truth needs another mechanism
referencing FK indexes         not automatic
numeric NaN/Infinity           real PostgreSQL behavior; reject where canonical exact values forbid them
```

The remaining issues are DANTE contract hardening, not “PostgreSQL cannot implement this”.

---

## 14. Current concrete control topology already designed

### `dante.native_address`

Candidate closed topology:

```text
native_ref     uuid PRIMARY KEY
owner_family   text NOT NULL
```

`native_ref` is the exact LR-01 native UUID, not a second semantic identity.

Bounded owner vocabulary = exactly the 15 native owner families.

Cross-table database-local integrity must prove the selected owner-family table contains that exact native UUID.

Unknown family rejects.

Heterogeneous NativeRef consumer:

```text
consumer.target_native_ref
→ FK dante.native_address(native_ref)
→ ON DELETE NO ACTION
+
consumer-specific DB-enforced owner-family eligibility
```

Homogeneous reference still uses direct owner FK.

`native_address` must never become an ORM polymorphic base or semantic Entity root.

### `dante.scoped_address`

Candidate topology:

```text
scoped_ref      uuid PRIMARY KEY
scoped_family   text NOT NULL
```

Only genuinely independently addressable/material contextual records receive ScopedRecordRef.

Exact family vocabulary is schema-controlled and grows only when a concrete accepted scoped family is added.

Again, no semantic superclass.

### `dante.material_state_address`

Candidate topology:

```text
material_state_ref   uuid PRIMARY KEY
native_owner_ref     uuid NULL
scoped_owner_ref     uuid NULL
facet_code           text NOT NULL
```

Exactly one owner address space is populated.

Native and scoped owner FKs remain separate.

Facet is schema-controlled and owner/family-qualified, examples:

```text
agreement.terms
goal.state
schedule.placement
```

No semantic payload lives in the control table.

Owner-specific state payload table owns meaning.

### Current binding

Candidate technical binding split preserves reference-family separation:

```text
dante.native_current_material_state

dante.scoped_current_material_state
```

Primary key by `(owner_ref, facet_code)` enforces at most one current state per owner/facet.

The database must enforce that current MaterialStateRef has same owner/address-space/facet.

Current truth is never inferred from MAX timestamp, UUID order or insertion order.

### Lineage

Correction/replacement/supersession/reconciliation must remain typed.

No universal generic graph edge should erase those meanings.

---

## 15. Latest whole-audit findings — MUST repair before next semantic block

The latest session deliberately audited the accumulated blueprint rather than moving directly to Schedule/Actual/Agreement.

Result:

```text
BASE ARCHITECTURE
strong / coherent

NEXT SEMANTIC BLOCK
DO NOT START YET

AUDIT REPAIR
required first
```

### Finding A — Recurrence materialization was made too unconditional

This is the most important semantic hardening.

Closed upstream truth:

```text
Recurrence
→ LR-05 typed rule/specification
→ ScopedRecordRef conditional
→ MaterialStateRef conditional
→ material exact rule state required where history/consequence depends on it
```

The full Domain Recurrence authority explicitly left the exact entity/value-object split, parent ownership/cardinality and persistence model deferred.

The current blueprint candidate effectively drifted toward:

```text
every persisted Recurrence
→ dante.recurrence scoped owner
→ ScopedRecordRef
→ scoped_address
→ recurrence.definition MaterialStateRef
```

That is too strong.

Required repair direction:

```text
OWNER-BOUND RECURRENCE
DEFAULT when recurrence is simply structured policy/state owned by:
- Routine
- recurring Event
- Temporal Constraint
- another accepted concrete source

INDEPENDENT SCOPED RECURRENCE
ONLY when one of these is genuinely required:
- independent addressability
- reuse across contexts
- cross-record reference
- independent reconciliation
- independent lifecycle/history
```

This does **not** remove Recurrence material history.

Example truthful owner-bound shape:

```text
Routine R1
→ material facet routine.recurrence
→ MaterialStateRef MS1
→ recurrence-family payload

Occurrence O7
→ governing source / governing MaterialStateRef MS1
```

Historical Occurrences remain fully explainable without manufacturing a standalone Recurrence identity for every source.

If a Recurrence later genuinely needs its own addressability/lifecycle, it may become a scoped record under the accepted trigger.

### Finding B — six Recurrence semantic families remain valid

Do not throw away the family design.

Required minimum semantic families remain:

```text
calendar / wall-clock
elapsed interval
quota per period
completion-relative
anchor-stream-relative
cyclic positional
```

These were directly required upstream.

The repair concerns ownership/materialization policy and exact constraints, not the six-family semantic model.

### Finding C — DB-U12 was declared CLOSED too early

The full physical Recurrence contract still needs deterministic closure for at least:

```text
when pattern_anchor is required
exact pattern anchor vs effective-range distinction
valid month/month-day/weekday/ordinal selector combinations
exact effective_until boundary semantics
invalid-date policy vocabulary
dst-gap policy vocabulary
dst-overlap policy vocabulary
period frame / zone rules
calendar-offset frame for completion-relative recurrence
calendar-offset frame for anchor-stream recurrence
source ↔ recurrence exact ownership/cardinality
named-zone accepted resolution / resolved_at history where consequential
```

Therefore preferred status after repair:

```text
SIX RECURRENCE SEMANTIC FAMILIES
CLOSED / RETAIN

FULL DB-U12 PHYSICAL CONTRACT
REOPENED FOR TARGETED HARDENING
```

Do not re-run general recurrence discovery; close only the remaining physical contract.

### Finding D — MaterialStateRef address ↔ payload integrity is currently only clearly protected in one direction

Current blueprint correctly intends to reject:

```text
material_state_address exists
payload missing at commit
```

But child-side deletion must also be prevented from creating:

```text
MaterialStateRef address still exists
owner-specific semantic payload deleted
```

A child FK from payload → address does not prevent deleting the child payload row itself.

Required invariant is bidirectional completeness while the state is live:

```text
address without required payload
→ REJECT

payload with wrong owner/facet/ref
→ REJECT

ordinary payload DELETE leaving address alive
→ REJECT

address DELETE while payload/current/history references survive
→ REJECT
```

Privacy/redaction/lawful lifecycle operations remain possible only through an explicit DB-U14 lifecycle/redaction contract that preserves truthful permitted continuity.

This is a real integrity hardening, not a stylistic preference.

### Finding E — CP3 runtime grants are too broad for the future immutable/control tables

Current real provisioning code was written before business schema existed and currently grants broadly:

```text
SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA dante
TO dante_runtime
```

and default table privileges also broadly grant runtime DML.

That was acceptable for the technical CP3 foundation, but it conflicts with CP6's intended object-specific immutability/least-privilege rules as soon as tables such as these exist:

```text
native_address
scoped_address
material_state_address
accepted immutable material-state payload tables
```

Required CP6 design correction:

```text
OBJECT-SPECIFIC RUNTIME PRIVILEGE MATRIX
```

Conceptual direction:

```text
native/scoped/material address control
→ SELECT + INSERT as needed
→ no ordinary UPDATE/DELETE

immutable accepted material-state payload
→ SELECT + INSERT as needed
→ no ordinary UPDATE/DELETE

current-binding rows
→ SELECT + INSERT + UPDATE as needed
→ DELETE only if exact lifecycle requires it

ordinary mutable owner/context tables
→ only exact DML justified by that family

redaction/retention/destructive repair
→ separate controlled path
→ not blanket runtime DELETE authority
```

Before CP6-04 materialization, provisioning/default-privilege behavior must be changed so a later provisioning/reconciliation run cannot silently re-grant UPDATE/DELETE on protected tables.

Do not write that code during CP6-03 unless an exact separate gate explicitly authorizes it. CP6-03 must first finish the privilege design.

### Finding F — native/scoped address topology remains sound but lifecycle depends on DB-U14

Do not reopen DB-U01/DB-U02 architecture by default.

However final owner deletion/retirement integrity cannot be considered completely proven until DB-U14 closes owner/family-specific lifecycle/tombstone/redaction behavior.

An owner must not physically disappear while an address row continues to falsely imply extant owner semantics.

Treat this as:

```text
DB-U01 / DB-U02 CONTROL TOPOLOGY
PASS / RETAIN

FINAL LIFECYCLE INTEGRITY
depends on DB-U14
```

### Finding G — temporal DB-U07 remains sound

Do not redesign temporal architecture.

Retain:

```text
date
floating local date/time
named-zone local + IANA zone
absolute timestamptz
range/multirange where meaning matches
elapsed duration separate from calendar semantics
world/effective chronology separate from knowledge chronology where material
```

Only harden zone-validation and named-zone accepted-resolution interaction with Recurrence where consequential.

---

## 16. Latest accumulated-audit matrix

Current assessment at the end of the saturated session:

```text
PostgreSQL canonical authority / schema dante           PASS
57 / 57 Logical coverage                                PASS
15 LR-01 native owners                                  PASS
15 identity-shell baseline                              PASS
no Entity/Thing/EAV/generic edge                        PASS
Reference family separation                             PASS
native_address / scoped_address direction               PASS + lifecycle dependency
current-state binding direction                         PASS
owner-specific material payload thesis                  PASS
lineage / no universal history graph                    PASS
temporal DB-U07                                         PASS + hardening
Place/PostGIS DB-U11                                    PASS
Quantity/MonetaryAmount DB-U13                          PASS
Capacity Claim DB-U16                                   PASS
PostgreSQL primitive feasibility                        PASS
CP3 runtime/session/migration compatibility              PASS
MaterialState address↔payload completeness              HARDENING REQUIRED
Recurrence ownership/materialization                    HARDENING REQUIRED
Recurrence full physical contract DB-U12                 REOPEN TARGETED
runtime database privileges                             BLOCKER BEFORE CP6-04
Gate 03                                                 NOT EARNED
```

This is the current review posture. Do not report CP6-03 as clean/closed.

---

## 17. Current unresolved DB-U register — conceptual state

Before the latest audit, the blueprint listed:

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

and remaining classified items such as:

```text
DB-U08 final remaining object naming
DB-U09 Account persistence
DB-U10 Principal/security persistence
DB-U14 owner/family lifecycle/tombstone fields
DB-U15 remaining structural/query indexes
DB-U17 provider/integration shapes
DB-U18 idempotency table timing
DB-U19 outbox timing
DB-U20 derived/search/vector structures
```

After the latest audit, the next repair should **not** leave DB-U12 marked fully closed.

Also add/represent the privilege-design obligation explicitly in the current unresolved/gate model rather than allowing it to remain hidden only in CP3 provisioning code.

Whether that receives a new DB-U ID or is incorporated into an existing security/privilege register should be decided consistently with the document's numbering style; do not create arbitrary numbering churn without reviewing the current file.

MaterialState completeness also needs a visible resolved/unresolved state rather than merely prose.

---

## 18. Immediate next action — do this BEFORE another semantic block

The next session must **not** jump directly to Schedule/Actual/Outcome/Agreement.

First perform a bounded audit-repair of:

```text
docs/database/dante-postgresql-database.md
```

The saturated session had proposed this exact repair intent:

```text
1. Recurrence
   - preserve six-family design
   - remove unconditional independent scoped ownership
   - define owner-bound vs independently scoped Recurrence
   - reopen/finalize DB-U12 exact physical constraints

2. MaterialStateRef
   - make address ↔ payload integrity bidirectional
   - prevent ordinary payload deletion from orphaning a MaterialStateRef
   - preserve lifecycle/redaction escape only through explicit DB-U14 contract

3. privileges
   - introduce exact Gate-03 object privilege-design obligation
   - record CP3 broad-runtime-DML reconciliation incompatibility
   - stage provisioning change for CP6-04
   - add privilege completeness to Gate-03 acceptance

4. temporal/Recurrence hardening
   - exact anchor requirements
   - named-zone accepted resolution where consequential
   - selector/policy/frame constraints

5. audit bookkeeping
   - stop claiming DB-U12 fully CLOSED until repaired
   - correct unresolved register/count
   - record DB-U01/02 lifecycle dependency on DB-U14
```

Do not broaden this repair into new concept design.

After the repair:

```text
REMOTE READBACK
+
TARGETED RE-AUDIT
+
CHECK NO UPSTREAM AUTHORITY WAS REOPENED
```

Only if clean should the next semantic database block begin.

---

## 19. Then continue CP6-03 object-level derivation

After the audit repair passes, continue the same canonical database specification rather than creating another theory document.

Highest-value remaining concrete blocks were identified as:

```text
owner-specific material-state families actually required by LR-01 owners
Schedule / Actual / Outcome / Milestone contextual topology
Agreement + exact terms state + n-party assent
specific LR-03 relation endpoints/cardinalities
Temporal Constraint / Criterion / Availability / Resource Requirement structured families
governance state families
owner-specific lifecycle/tombstone/redaction semantics
remaining FK + structural index review
final stable names
Database Dictionary materialization/generation
```

For each family:

```text
1. read complete Domain concept authority
2. read matching Logical disposition / slice hardenings
3. consume Physical + Constitution rules
4. decide exact persistence disposition
5. define exact table(s)
6. define columns + meanings + PostgreSQL types
7. define PK/FK/reference contracts
8. define NULL/missingness semantics
9. define UNIQUE/CHECK/EXCLUDE/trigger integrity
10. define MaterialState/current/history behavior
11. define lifecycle/delete/redaction behavior
12. justify indexes
13. define SQLAlchemy mapping shape
14. define migration dependencies
15. define privilege posture
16. define real PostgreSQL positive/negative tests
17. create/update Database Dictionary plan/entry
18. update unresolved/closure status
19. audit accumulated blueprint again before moving on
```

No object is complete before this chain is satisfied.

---

## 20. CP6-03 Gate 03 bar

CP6-03 cannot close until at least:

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
object/family privilege posture complete                       PASS
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

The enterprise documentation requirement is part of the gate, not after-the-fact cleanup.

---

## 21. CP6-04 materialization — future, NOT YET

Only after Gate 03 is clean does CP6 start real business database materialization.

Authorized classes then include, under exact batch gates:

```text
Alembic business-schema revisions
DANTE business tables
bounded address/control tables
owner-specific canonical tables
owner-specific material-state/history tables
specific relation tables
provider/integration tables only where already determined
bounded derived/query persistence only where already determined
constraints and indexes
SQLAlchemy mappings
object-specific privileges/default grants
real PostgreSQL fixtures/tests
database dictionary/reference updates in same change
```

Implementation should follow the dependency DAG in bounded migration batches, not one giant migration if avoidable.

Each batch must prove at minimum where applicable:

```text
fresh DB → Alembic head
single head
schema drift clean
real FK/reference negative cases
constraint positive/negative cases
runtime/migrator privilege behavior
remote readback
```

Do not implement product use cases/services/API/frontend during CP6-04.

---

## 22. CP6-05 direct QA / closure — future

Whole real database QA includes as applicable:

```text
fresh database → head
single Alembic head
SQLAlchemy ↔ Alembic ↔ PostgreSQL schema alignment
documentation/dictionary ↔ real schema alignment
owner/migrator/runtime privilege matrix
wrong-family/dangling-reference rejection
CHECK/UNIQUE/EXCLUDE positive + negative cases
missingness behavior
MaterialState owner/facet/current binding integrity
MaterialState address ↔ payload completeness
history reconstruction/correction
idempotency if materialized
expected-state/concurrency races where executable
transaction rollback/atomicity
truthful downgrade behavior
PostGIS/FTS/pgvector only if concrete schema actually uses them
```

Some evidence remains honestly staged until a real later subject exists:

```text
destructive old-backup anti-resurrection
real V1→V2 semantic evolution
destructive recovery corpus
inactive specialist capabilities
application-level governed effects requiring real use cases
```

Never convert those to PASS on paper.

Desired closure truth:

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

---

## 23. Specialist/selected capability activation boundary

Selection does not equal activation.

Do not materialize merely to complete a checklist:

```text
PgBouncer
PowerSync / encrypted SQLite
Restate
Cloudflare R2
pgBackRest + S3
OR-Tools
extra observability infrastructure
```

A selected capability activates only when a real consumer/need exists.

PostgreSQL-native schema capability such as a true PostGIS column/index may be materialized during CP6 only when the closed database model genuinely requires it.

Current Place decision specifically does **not** force baseline PostGIS geometry merely because PostGIS is selected.

---

## 24. Important Physical risk lanes to keep alive

Do not lose these when moving from documentation to SQL:

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

CP6-03 assigns concrete structures/tests where determinable.

CP6-04 implements the mechanisms.

CP6-05 directly proves what now has a real executable subject and leaves the rest staged honestly.

---

## 25. Things the next session must NOT do

Unless concrete contradictory evidence forces a separately gated reopen:

```text
DO NOT redesign Domain
DO NOT rerun Logical owner census
DO NOT change the exact 15 LR-01 owners
DO NOT collapse reference families
DO NOT introduce Entity/Thing root
DO NOT introduce generic Relationship/edge root
DO NOT introduce canonical EAV
DO NOT introduce universal event sourcing
DO NOT make provider state canonical
DO NOT use JSONB to hide required semantics
DO NOT add one table per concept mechanically without materiality review
DO NOT give every LR-02 record UUID just for consistency
DO NOT give every Recurrence independent ScopedRecordRef by default
DO NOT infer current from MAX/UUID/latest insert
DO NOT use provider revision/MVCC as MaterialStateRef
DO NOT enable broad CASCADE by convention
DO NOT activate dormant technology just because selected
DO NOT create generic Repository/UoW/BaseService
DO NOT implement first product vertical inside CP6
DO NOT mutate protected main directly
DO NOT silently broaden a user-approved write gate
```

---

## 26. Current Git/write truth at handoff creation

Immediately before this handoff request, the latest explicitly surfaced live PRE-SCOPE in the saturated session was:

```text
bd87bc91802cfea66ae64327314ae7e9642972a6
```

That value was the PRE-SCOPE proposed for the next audit-repair write and must be treated as historical once this handoff commit is created.

After this file is committed, **the handoff commit SHA returned by GitHub becomes the branch HEAD at that moment**.

The next session must still verify live branch HEAD before any new write because another actor/session may advance the branch.

Protected-main branch must remain untouched directly.

---

## 27. Exact resume script for the next ChatGPT session

A fresh session should effectively do this:

```text
1. Read this temporary handoff completely.
2. Verify feature/logical-postgresql exists and read live branch truth.
3. Read current docs/workstreams/logical-postgresql.md.
4. Read docs/database/README.md.
5. Read docs/database/dante-postgresql-database.md completely enough to reconstruct the current blueprint and DB-U register.
6. Re-read CP6-01 Part 1 + Part 2 relevant sections.
7. Re-read CP6-02 relevant REF/MAT/HIST/TIM/REL/CON/IDX/MIG/SEC/QA rules.
8. Re-read complete Domain + Logical Recurrence authority because the next repair depends on it.
9. Re-check real CP3 provisioning.py because privilege hardening depends on current grants.
10. Confirm no new remote change superseded this handoff.
11. Do NOT start a new semantic block.
12. Present/execute only the exact bounded audit-repair gate after user approval.
13. Remote-readback and re-audit the repaired blueprint.
14. Only then continue Schedule/Actual/Outcome/Milestone/Agreement/etc.
15. After every new block, repeat the accumulated audit method.
```

When fully aligned from durable repository truth, the session may remove this temporary file in a later exact write gate if desired.

---

## 28. Final continuity statement

The project is **not stuck and not being redesigned**.

The current blueprint is structurally strong. The latest audit intentionally found issues before SQL existed, which is exactly the purpose of CP6-03.

Current objective is narrow:

```text
repair Recurrence ownership/materialization precision
+
finish full Recurrence physical constraints
+
make MaterialStateRef payload integrity bidirectional
+
close object-specific runtime privilege posture
+
record lifecycle dependencies accurately
        ↓
re-audit accumulated blueprint
        ↓
continue remaining semantic database families
        ↓
Gate 03
        ↓
real PostgreSQL materialization
```

Do not lower the engineering standard for speed. The next session should continue from here as if it were the same conversation.