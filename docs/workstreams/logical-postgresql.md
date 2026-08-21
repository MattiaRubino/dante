# Workstream — CP6 Concrete Persistence Readiness

- Status: **ACTIVE / DESIGN-FIRST / NO BUSINESS IMPLEMENTATION AUTHORIZED**
- Product: **DANTE**
- Repository: `MattiaRubino/dante`
- Branch: `feature/logical-postgresql`
- Protected-main anchor at branch origin: `fd3bc8dd918cf6aadeff4572221af68612c3cb42`
- CP6 durable-handoff PRE-SCOPE: `6c01e6aa6432824ae27478e2b91d8b809bc54bfb`
- Upstream Domain Model: **CLOSED / SEMANTICALLY COMPLETE FOR CURRENT SCOPE**
- Upstream Logical Model: **CLOSED / 57 OF 57 CLASSIFIED / WL-H01..WL-H12 ACTIVE**
- Upstream Physical Model: **CLOSED / SELECTED / ACCEPTED / PostgreSQL 18.4 CANONICAL PRIMARY**
- Production backend scaffold: **CP1–CP5 CLOSED / DIRECT QA PASS / INTEGRATED IN PROTECTED main**
- CP6-00: **READ-ONLY AUTHORITY RECONSTRUCTION COMPLETE**
- Business schema/migrations: **NOT STARTED / OUT OF CP6 IMPLEMENTATION SCOPE**
- Vertical #1 implementation: **OUT OF CP6 / NEXT SEPARATELY AUTHORIZED PHASE AFTER CP6 CLOSURE**

## 1. Purpose

CP6 is the bounded transition from the already-closed DANTE semantic/physical architecture into a concrete, reusable PostgreSQL persistence foundation.

It is **not** another Domain, Logical or Physical modeling cycle. The extensive upstream work exists precisely so this stage can translate accepted meaning into concrete relational rules without re-discovering or weakening that meaning.

CP6 must end with:

```text
CLOSED DOMAIN
+
CLOSED LOGICAL
+
ACCEPTED PHYSICAL POSTGRESQL MAPPING
+
CLOSED CP1–CP5 BACKEND FOUNDATION
        ↓
CONCRETE POSTGRESQL PERSISTENCE FOUNDATION
CLOSED / READY
        +
VERTICAL #1
SELECTED
EXACTLY DESIGNED
READY FOR IMPLEMENTATION
```

CP6 must **not** implement Vertical #1. The first business Alembic migration, first business SQLAlchemy mapping, first business persistence adapter and first application operation for Vertical #1 belong to the separately authorized phase that starts only after CP6 is closed.

The quality target is deliberately high:

- consume the full closed Domain → Logical → Physical evidence chain;
- preserve semantic ownership and reverse mapping;
- close genuinely global PostgreSQL decisions once, not repeatedly per vertical;
- establish concrete relational topology and implementation dependency order;
- design Vertical #1 to implementation-ready precision;
- directly prove only those PostgreSQL-foundation claims that can be proved without inventing speculative business schema;
- carry any vertical-dependent direct proof forward honestly rather than manufacturing a paper or synthetic PASS.

## 2. Authority and precedence

Repository truth outranks conversation memory.

Use the current project precedence from the development operating rules:

1. current protected-main code, migrations, tests and accepted model/ADR truth;
2. current durable Product / Domain / Logical / Physical / architecture / engineering documents;
3. this active bounded CP6 workstream handoff for newer unmerged work;
4. other current workstream sources;
5. historical evidence, closed branches, PR/Git history;
6. conversation memory.

Implementation convenience never outranks accepted semantics.

A closed upstream decision is reopened only when **concrete contradictory implementation evidence** proves the affected decision cannot hold. Any reopen must be targeted and separately gated. A preference for easier SQL, ORM mappings, fewer joins or a generic schema is not reopen evidence.

## 3. Mandatory continuation bootstrap

A fresh session working on CP6 must reconstruct repository authority, not rely on this handoff alone.

At minimum read/verify:

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

this workstream handoff
```

Then consume the complete closed upstream workstreams and all canonical continuation parts they require:

```text
docs/workstreams/domain-model.md
+ canonical Domain continuations through final closure

docs/workstreams/logical-model.md
+ logical-model-part-2.md ... logical-model-part-9.md
+ complete split Logical payloads

docs/workstreams/pre-physical-coherence.md

docs/workstreams/physical-model.md

docs/workstreams/engineering-foundation.md

docs/workstreams/backend-scaffold.md
```

Current Logical authority includes, at minimum:

```text
docs/logical-model/whole-logical-model-v1.md
docs/logical-model/checkpoints/whole-logical-v1-validation.md
docs/logical-model/checkpoints/whole-logical-v1-remote-qa.md
docs/logical-model/decision-and-assumption-register-v1-part-9.md
docs/logical-model/traceability-and-regression-ledger-v1-part-9.md
docs/logical-model/test-corpus-v1-part-9.md
```

Current Physical-consuming authority includes, at minimum:

```text
docs/physical-model/README.md
docs/physical-model/pm-02-primary-mapping-overview-v1.md
docs/physical-model/mappings/postgresql-18.4-v1.md
docs/physical-model/pm-03-semantic-hard-gate-preflight-v1.md
docs/physical-model/pm-11-explicit-selection-v1.md
docs/physical-model/pm-12-accepted-physical-model-v1.md
docs/physical-model/pm-13-clean-room-qa-v1.md
docs/physical-model/final-stack-capability-matrix-v1.md
docs/physical-model/final-stack-audit-v1.md
docs/physical-model/recommendation/post-selection-validation-register-v1.md
```

Current backend persistence authority includes the real CP3 implementation and tests, especially:

```text
docs/development/backend-cp3-persistence-contract.md
apps/backend/src/dante/platform/config/database.py
apps/backend/src/dante/platform/database/runtime.py
apps/backend/src/dante/platform/database/metadata.py
apps/backend/src/dante/platform/database/provisioning.py
apps/backend/src/dante/bootstrap/
apps/backend/migrations/
apps/backend/tests/
infra/local/postgres/
infra/compose/
.github/workflows/backend-ci.yml
.github/workflows/dependency-review.yml
```

Do not stop at Part 1 of a split canonical document. Size/tool-limit splits are lossless continuations, not summaries.

## 4. CP6 classification discipline

Every material question encountered in CP6 must be classified before work proceeds.

```text
INHERITED / CLOSED
accepted upstream decision;
consume and apply;
do not re-decide for convenience.

CONCRETE DECISION
upstream semantics/architecture deliberately left exact PostgreSQL implementation open;
CP6 must resolve it at the appropriate checkpoint.

VERTICAL-SPECIFIC
not required to make the global persistence foundation coherent;
defer until the relevant vertical design, beginning with CP6-05 for Vertical #1.

DIRECT-PROOF
meaning/mechanism already accepted;
remaining work is executable evidence, not a new architecture decision.
```

This classification is mandatory in CP6-01 and CP6-02 decision registers.

It prevents two opposite failures:

```text
FAILURE A
repeating Domain / Logical / Physical design already closed

FAILURE B
calling an unresolved concrete PostgreSQL choice “already decided”
```

## 5. Inherited semantic baseline — CLOSED / DO NOT REOPEN BY CONVENIENCE

### 5.1 Whole Logical coverage

The closed Logical Model already establishes:

```text
DOMAIN CONCEPTS CLASSIFIED       57 / 57
DOMAIN OWNER GAP                  0
UNCLASSIFIED                      0
NEW DOMAIN OWNER REQUIRED         0
GENERIC FALLBACK DEPENDENCIES     0
OWNERLESS MATERIAL STATE          0
REQUIRED UNIVERSAL ROOTS           0
```

CP6 consumes that classification. It does not perform another missing-concept census.

### 5.2 Native identity owners

The accepted LR-01 native identity set is exactly:

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

`Actor`, `Subject` and `Resource` remain contextual roles/capabilities and do not gain native wrapper identity merely because heterogeneous persistence/querying would be easier.

### 5.3 Logical representation vocabulary

The accepted representation kernel remains:

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

Reference addressability remains discriminated:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

Do not collapse those families into one semantic `kind + id` reference root.

No universal `ActorRef`, `SubjectRef`, `ResourceRef`, `TermsRef`, `ProjectionRef` or semantic `RelationRef` is required.

### 5.5 State-layer separation

The accepted model distinguishes:

```text
canonical DANTE state
material historical state
derived / projection state
external / provider state
unresolved / candidate state
security / AuthZ runtime state
transient computation state
```

Storage co-location never makes those layers semantically equivalent.

### 5.6 High-risk non-collapse invariants

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
Quantity != Monetary Amount
Asset != Resource role
Responsibility != Participation != Coordination Stewardship
Authority != Visibility
Agreement != Consent
Ownership != Possession
Collective != current Membership set
Schedule != Capacity Claim != Resource Allocation != Actual use
provider state != canonical DANTE state automatically
derived projection != canonical truth
current state != historical state
correction != silent overwrite
shared reality != per-recipient duplicate reality
AI/solver inference != accepted canonical effect
```

## 6. WL-H01..WL-H12 — active implementation obligations

All twelve Whole-Logical hardenings remain active throughout CP6 and subsequent vertical implementation.

```text
WL-H01
Agreement terms bind to a justified owned MaterialStateRef;
no generic ownerless TermsRef.

WL-H02
Governed consequential effects preserve operation family, semantic target/facet,
material target state where required, effect semantics, context/purpose,
preconditions and governance requirements;
HTTP route/AuthZ action/UI button != canonical effect.

WL-H03
Projection/disclosure surfaces retain bounded source, derivation/profile,
material basis, purpose/context and disclosure boundary;
no universal ProjectionRef.

WL-H04
absence / no record != false / no / inactive / declined / cancelled /
known non-realization.

WL-H05
stale-write-sensitive consequential mutation requires expected MaterialStateRef
or semantic equivalent; mismatch never silently overwrites accepted state.

WL-H06
idempotency controls retry/effect duplication and remains distinct from semantic identity.

WL-H07
multi-owner invariants use truthful atomic consistency where co-located;
otherwise explicit staged/partial state + reconciliation/compensation.

WL-H08
canonical DANTE state != provider apply/sync state.

WL-H09
consequential LR-08 use revalidates or binds material derivation basis;
stale derived state cannot silently become canonical effect.

WL-H10
retention/redaction/tombstone behavior preserves truthful permitted historical continuity;
retired NativeRef is never reused.

WL-H11
consequential AuthZ provenance remains reconstructible without redefining
Authority, Consent, Actor or Domain history as technical AuthZ state.

WL-H12
selective disclosure includes inference/non-interference across counts,
existence, ranking, errors, timing, explanations, candidates, aggregates and relations.
```

CP6-01 maps applicability; CP6-02 defines reusable physical rules where global; CP6-05 applies them exactly to Vertical #1; vertical-dependent executable proof belongs to the later implementation phase unless CP6-06 can prove a foundation rule without speculative business structures.

## 7. Inherited PostgreSQL Physical baseline — CLOSED

### 7.1 Canonical authority

```text
PostgreSQL 18.4
= sole canonical DANTE persistence and material-history authority
```

Selected adjacent PostgreSQL capabilities remain bounded mechanisms:

```text
PostGIS 3.6.4
pgvector 0.8.6
native FTS
pg_trgm
unaccent
pg_stat_statements
PgBouncer 1.25.2 selected, not automatically active day one
```

Noncanonical companion mechanisms remain noncanonical, including encrypted SQLite/PowerSync, Restate, R2, recovery S3, OR-Tools and observability systems.

### 7.2 Accepted PostgreSQL mapping thesis

The accepted PostgreSQL design is:

```text
owner-specific canonical tables/families
+
owner-specific material-state/history tables/families
+
specific relation tables/families
+
bounded technical address/state anchors only where genuine heterogeneous addressing requires them
+
separate integration/projection/technical concerns without semantic collapse
```

Explicitly rejected:

```text
universal Entity / Thing table
universal Relationship table
generic canonical EAV/property bag
universal event-log ontology
JSONB as required semantic escape hatch
PostgreSQL inheritance as ontology
```

### 7.3 NativeRef physical rule

```text
homogeneous target family
→ direct FK preferred

genuinely heterogeneous native target family
→ bounded technical native-address anchor may be used
```

An address anchor is not a semantic superclass, cannot own generic Domain properties/lifecycle and must not become a universal Entity table.

### 7.4 ScopedRecordRef physical rule

Concrete LR-02 records own stable scoped identity where addressability is justified. A separate bounded scoped-address mechanism may exist only for genuine heterogeneous scoped addressing. Native/scoped/material/external addressing must not collapse into one generic reference space.

### 7.5 MaterialStateRef physical rule

Material semantic state has explicit stable identity independent from storage/MVCC tokens.

```text
MaterialStateRef
!= xmin/xid
!= updated_at
!= row hash
!= ETag
!= provider revision
```

Accepted baseline:

```text
stable semantic owner
+
explicit current accepted material-state binding where required
+
retained owner-specific material states/history
+
typed correction/replacement/reconciliation lineage
+
effective/world chronology where material
+
recorded/learned chronology where material
```

Current accepted state is not semantically “the row with the highest revision number”.

### 7.6 Relation physical rule

```text
simple binary LR-03
→ specific association table/family with concrete eligible endpoints

qualified/material/consequential LR-03
→ contextual relation record with scoped identity/history/governance/provenance where required

n-ary semantics
→ real contextual/n-ary representation
```

No universal `from_ref, relation_type, to_ref, payload` fallback is accepted.

### 7.7 Concurrency physical rule

Use the narrowest PostgreSQL mechanism that truthfully protects the concrete invariant:

```text
NOT NULL / CHECK / FK / UNIQUE
DEFERRABLE where transaction-end validity is required
partial UNIQUE where predicate-bounded uniqueness is required
EXCLUDE/range constraints where applicable
conditional updates / row-key coordination
SERIALIZABLE for predicate/write-skew-sensitive consequential operations
```

Default backend isolation remains `READ COMMITTED`; CP6 must not switch the entire application to SERIALIZABLE for convenience.

### 7.8 Schema evolution physical rule

Accepted direction:

1. additive/backward-readable evolution where practical;
2. new semantic shape without silently reinterpreting old rows;
3. explicit data migration/backfill with provenance/checkpoint where required;
4. preserve NativeRef/ScopedRecordRef/MaterialStateRef continuity;
5. preserve historical temporal/governance meaning;
6. preserve tombstone/redaction semantics;
7. remove obsolete structures only after read/write cutover evidence.

ORM autogeneration/implicit synchronization never substitutes for reviewed migration semantics.

## 8. PostgreSQL risk register carried into CP6

The accepted Physical mapping already identified ten PostgreSQL-specific proof/risk lanes. CP6 must consume them rather than invent a replacement risk list.

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

Each risk must receive one of:

```text
FOUNDATION RULE CLOSED IN CP6
DIRECTLY PROVABLE IN CP6 WITHOUT SPECULATIVE BUSINESS STRUCTURE
VERTICAL #1 DESIGN OBLIGATION
LATER VERTICAL IMPLEMENTATION PROOF
RELEASE/RECOVERY STAGE PROOF
```

No risk may disappear merely because it is inconvenient to test now.

## 9. Post-selection validation carry-forward

The Physical post-selection validation register remains authoritative. In particular, preserve stage ownership for:

```text
PSV-01 old-backup anti-resurrection
PSV-02 actual V1 → V2 mapping/schema evolution
PSV-03 destructive restore + semantic verification
PSV-04 capacity/backpressure truthful degradation
PSV-05 WL-H12 system-level non-interference
PSV-35 PostgreSQL selected mapping end-to-end smoke corpus
```

and all later specialist obligations when their capability is activated.

`SELECTED`, `ACCEPTED`, `STATIC PASS-CONDITIONAL` and `ARCHITECTURE QA PASS` do not equal direct runtime PASS.

CP6 may close only directly applicable foundation evidence. Anything requiring the real business vertical, real historical data evolution, real restore/recovery or an inactive specialist remains explicitly carried forward to the correct later stage.

## 10. Inherited CP1–CP5 backend foundation — CLOSED

CP6 extends the existing persistence foundation; it must not create a parallel architecture.

Already frozen and directly tested:

```text
Python 3.14.7 initial scaffold runtime
uv lock/build authority
Ruff
mypy strict
pytest / real PostgreSQL test lane

PostgreSQL 18.4 LOCAL envelope
application schema dante
SQLAlchemy 2 async
psycopg 3
Alembic

one AsyncEngine per process
one async_sessionmaker per process
one AsyncSession per application operation/task
expire_on_commit=False
autobegin=False
autoflush=True
outer application operation owns commit/rollback
adapter may flush but does not implicitly commit

one shared SQLAlchemy Base/MetaData
schema = dante
existing naming convention

one Alembic environment
one migration DAG
one canonical head on integrated main
version table = dante.alembic_version
online migrations only
migration DDL under SET ROLE dante_owner
runtime access to alembic_version denied

roles
dante_owner     NOLOGIN object/schema owner
dante_migrator  LOGIN/NOINHERIT with bounded SET ROLE
dante_runtime   LOGIN/NOINHERIT / DML-only posture
```

Do not introduce generic `Repository[T]`, generic UnitOfWork, generic BaseService or a second persistence metadata system merely for uniformity.

## 11. CP6 scope and terminal boundary

CP6 is a readiness/foundation phase, not the first business vertical implementation phase.

It must close:

```text
whole-model concrete persistence coverage
PostgreSQL persistence constitution
concrete relational topology
implementation dependency DAG
vertical decomposition
Vertical #1 selection
Vertical #1 exact persistence design
applicable non-speculative PostgreSQL foundation proof
whole readiness / clean-room QA
```

It must terminate at:

```text
CONCRETE POSTGRESQL FOUNDATION
CLOSED / READY

VERTICAL #1
SELECTED
EXACTLY DESIGNED
READY FOR IMPLEMENTATION
```

The next separately authorized phase implements Vertical #1.

## 12. CP6-00 — Authority Reconstruction & Scope Freeze

**Status: COMPLETE / READ-ONLY.**

Purpose:

- verify live branch/main relation;
- reconstruct complete Domain → Logical → Physical authority;
- inspect current CP3/CP5 implementation rather than relying on design memory;
- identify closed vs truly open concrete persistence decisions;
- establish this CP6 checkpoint plan before business schema work.

Completion criteria:

```text
Domain authority reconstructed              PASS
Logical 57/57 + WL-H01..12 reconstructed    PASS
Physical PostgreSQL mapping reconstructed   PASS
PG-R01..10 reconstructed                    PASS
PSV carry-forward reconstructed             PASS
CP3/CP5 implementation reconstructed        PASS
business schema started                     NO
```

CP6-00 completion does not authorize later checkpoint writes automatically.

## 13. CP6-01 — Concrete Persistence Coverage Map

### Purpose

Translate the existing 57/57 Logical disposition into a **concrete implementation-obligation map** without repeating semantic owner discovery.

This checkpoint answers:

> Given the already accepted meaning, what persistence family, reference/material/history pressure, dependency and later proof obligation does each concept impose on the concrete PostgreSQL architecture?

### Required row-level coverage

For every accepted Domain concept record at least:

```text
Domain concept
existing Logical disposition / LR class
canonical / contextual / relation / value / rule / result /
history / projection / provider / flexible / unresolved / profile / specialist role

identity/addressability pressure
NativeRef / ScopedRecordRef / MaterialStateRef / ExternalRef / none

concrete persistence family
material-state pressure: none / conditional / required
history pressure: none / lightweight / material
effective/world chronology pressure
recorded/learned chronology pressure
reference-contract pressure
constraint/invariant class
transaction/concurrency pressure
provenance/governance pressure
retention/redaction/tombstone pressure
query/access pressure
PostGIS / FTS / pg_trgm / pgvector / JSONB pressure where justified
WL-H01..WL-H12 applicability
PG-R01..PG-R10 applicability
PSV applicability
upstream/dependency pressure
classification: INHERITED/CLOSED | CONCRETE DECISION | VERTICAL-SPECIFIC | DIRECT-PROOF
```

This is **not** table/column design for all 57 concepts.

### Required aggregate outputs

CP6-01 must derive:

1. complete 57/57 concrete-persistence coverage matrix;
2. physical-family map;
3. dependency-pressure graph inputs;
4. closed-vs-open concrete decision register;
5. WL-H01..12 applicability map;
6. PG-R01..10 applicability map;
7. PSV stage/applicability map.

### Gate 01

Do not advance until:

```text
57 / 57 concepts accounted                         PASS
15 / 15 LR-01 families accounted                   PASS
reference pressure classified                      PASS
materiality/history pressure classified            PASS
canonical/provider/derived boundaries classified   PASS
dependency pressure classified                     PASS
WL-H01..12 applicability complete                  PASS
PG-R01..10 applicability complete                  PASS
PSV applicability/stage complete                   PASS
semantic owner reclassification                    0
generic semantic fallback                          0
unexplained JSONB fallback                          0
unclassified persistence family                     0
accidental upstream architecture reopen             0
```

No business DDL is authorized by Gate 01.

## 14. CP6-02 — PostgreSQL Persistence Constitution

### Purpose

Close the global reusable PostgreSQL rules that future verticals must consume instead of re-deciding repeatedly.

This is the DANTE database constitution. It is **not** the complete future database DDL.

### Required constitution families

#### ID — Physical identity

Close rules for:

```text
primary-key/identifier strategy
identifier type selection
generation locus
opacity/exposure
sortability where justified
offline-safe issuance implications
immutability/non-reuse
index/storage implications
```

Do not assume one type before evidence/review.

#### REF — Reference addressing

Close concrete reusable mechanics for:

```text
direct homogeneous FKs
bounded native heterogeneous addressing
scoped-record addressing
material-state addressing
external issuer-scoped addressing
target-family eligibility enforcement
dangling-reference prevention
```

No universal semantic root.

#### MAT — Material state / current truth

Close reusable rules for:

```text
MaterialStateRef physical shape
state-owner/facet binding
current accepted-state binding
owner-specific material state
immutability/update policy
correction
replacement
reconciliation
lineage
mapping/schema revision metadata
```

#### HIST / TIM — Historical and temporal truth

Close reusable rules for:

```text
material history retention
world/effective chronology
recorded/learned/accepted chronology
current vs historical access
historical reconstruction
when dual chronology is required vs unnecessary
```

No universal bitemporal Fact table.

#### MISS — Missing / unknown / negative

Close the representation doctrine for:

```text
NULL
row absence
explicit unknown
explicit negative
not-applicable
redacted
unavailable
retired
```

No global `missing == false` convention.

#### TYP — PostgreSQL type/finite-state doctrine

Define decision rules for applicable:

```text
PostgreSQL ENUM
text + CHECK
reference/lookup table
DOMAIN/composite where justified
arrays
range/multirange
typed JSONB only within accepted boundaries
```

Do not select one mechanism globally without semantic/evolution reasons.

#### REL — Relation doctrine

Define reusable physical patterns for:

```text
specific simple binary relation
qualified/material relation
n-ary relation
addressable relation state
governance-bearing relation
relation history
```

No generic semantic edge fallback.

#### PROV — Provenance/authorship

Define a bounded persistence pattern capable, where consequence requires, of reconstructing applicable:

```text
operation family
semantic target/facet
expected MaterialStateRef
actual Actor
represented party
Principal/security context reference
Authority / Consent / Visibility / Agreement material basis
purpose/context
idempotency reference
correlation/causation
resulting canonical effect
provider/runtime outcome separately
```

This remains technical provenance, not a new universal Domain Operation/Command owner.

#### LIFE — Lifecycle / retention / tombstone

Close rules for:

```text
retirement
logical removal where justified
payload redaction
minimal tombstone/reference continuity
identity non-reuse
lineage minimization
anti-resurrection requirements
```

#### CON — Constraint doctrine

Define which invariant classes belong in:

```text
NOT NULL
CHECK
FK
UNIQUE
partial UNIQUE
DEFERRABLE constraints
EXCLUDE/range constraints
trigger only when clearly justified
transactional application check only when DB-local declarative enforcement is insufficient
```

Prefer database-enforced local structural truth where PostgreSQL can express it correctly.

#### TX — Transaction/concurrency doctrine

Create an explicit matrix:

```text
invariant/race class
expected-state requirement
constraint strategy
locking/conditional-write strategy
isolation escalation
retry/reconciliation semantics
observable conflict/error behavior
required direct concurrency proof stage
```

Default remains CP3 `READ COMMITTED`; escalation is invariant-specific.

#### IDEM — Idempotency doctrine

Close reusable rules for:

```text
operation scope
idempotency key
material operation fingerprint
same-operation replay
materially-different reuse conflict
result retention
lifetime/expiry only where justified
```

Idempotency never becomes Domain identity.

#### IDX — Index doctrine

Define evidence/rules for:

```text
FK-supporting indexes
unique indexes
partial indexes
composite key order
INCLUDE/covering indexes
range/GiST/GIN use
search indexes
redundant-index avoidance
query-driven index justification
```

Do not pre-design every future vertical index.

#### CAP — PostgreSQL capability boundaries

Define operational use rules for:

```text
PostGIS
native FTS
pg_trgm
unaccent
pgvector
JSONB
```

Preserve:

```text
geometry/geography != Place identity
search/vector result != canonical truth
JSONB != required semantic escape hatch
provider/raw/flexible metadata may use bounded JSONB where accepted
```

#### MIG — Migration/evolution doctrine

Close rules for:

```text
Alembic single-head discipline
revision naming/ordering/dependency
reviewed DDL
schema/data migration separation where useful
backfill/checkpoint/provenance
expand → migrate → contract
forward compatibility
safe downgrade where genuinely reversible
forward-fix where downgrade would lie or destroy semantic evidence
destructive change requirements
read/write cutover
schema drift checks
identity/reference/material-history continuity
```

#### SEC — Ownership/privilege doctrine

Consume CP3's owner/migrator/runtime split and define how future DANTE business objects inherit that posture. Do not redesign the role architecture without concrete contradictory evidence.

#### QA — Direct persistence acceptance doctrine

Define required future proof classes, including:

```text
positive constraint acceptance
negative constraint rejection
wrong ref-family rejection
dangling-reference rejection
history reconstruction
unknown vs explicit negative
expected-state concurrency
multi-owner race where applicable
rollback/atomicity
runtime privilege rejection
fresh DB → head
single Alembic head
schema drift
real data evolution
recovery/anti-resurrection at the correct later stage
```

### Gate 02

Do not advance until:

```text
all genuinely global concrete decisions closed       PASS
all inherited decisions traceable                    PASS
all remaining decisions explicitly vertical-specific PASS
all direct-proof obligations have stage/owner        PASS

universal Entity root                      0
universal Relationship root                0
generic canonical EAV                      0
generic history/event ontology             0
provider token == MaterialStateRef          0
NULL-as-universal-negative                  0
silent consequential LWW                    0
implicit ORM schema authority               0

CP3 contradiction                           0
Logical contradiction                       0
Physical contradiction                      0

PG-R01..PG-R10 concrete proof path         complete
applicable PSV ownership/stage              complete
```

No business DDL is authorized by Gate 02.

## 15. CP6-03 — Concrete Relational Topology + Implementation Dependency DAG + Vertical Decomposition

### Naming boundary

The Physical Model is already CLOSED / SELECTED / ACCEPTED. CP6-03 does **not** redesign the Physical Model and therefore must not be called a new “Physical Topology” phase.

CP6-03 maps the accepted Logical/Physical contracts into concrete relational families and implementation order.

### Required outputs

#### A. Concrete relational topology

Establish how the DANTE `dante` relational namespace is organized conceptually and concretely across families such as:

```text
native canonical owner families
dependent/material contextual families
material-state/history families
specific relation families
rule/specification families
provenance/governance support
provider/integration state
derived/projection/read structures
bounded technical support structures
specialist-extension boundaries
```

This does not require separate PostgreSQL schemas. CP3 already established application schema `dante`; any proposal to change that requires explicit contradictory evidence and a separate decision.

#### B. Implementation dependency DAG

Model foundation and vertical prerequisites explicitly:

```text
which persistence primitive/rule must exist before which family
which owner identity is required before dependent records
which history/reference/governance foundation a vertical needs
which dependencies are structural vs merely query/product ordering
```

The DAG exists to prevent partial implementation from discovering hidden foundational dependencies mid-vertical.

#### C. Vertical decomposition

Define coherent implementation verticals from the dependency graph and product/domain structure.

A vertical is not automatically:

```text
one Domain owner
one Logical owner
one table
one API route
one screen
one repository
```

A vertical may legitimately combine multiple owners/relations/foundation concerns when that is the smallest coherent implementable capability boundary.

### Gate 03

Require:

```text
relational families coherent                 PASS
foundation dependencies explicit             PASS
vertical boundaries explicit                 PASS
vertical dependency order explicit           PASS
57/57 coverage preserved                     PASS
no capability reserved by placeholder code   PASS
no speculative business DDL                  PASS
Physical Model redesign                      0
```

## 16. CP6-04 — Vertical #1 Selection

### Purpose

Select the first business vertical **after** the topology and dependency DAG reveal which candidate is the strongest initial implementation/crash-test of the foundation.

Do not pre-select Access, Identity, Goal, Planning or any other candidate merely because it feels natural.

### Selection criteria

Compare serious candidates against at least:

```text
foundation/dependency leverage
semantic coverage
reference-contract coverage
history/material-state pressure
concurrency pressure
provenance/governance pressure
query usefulness
product usefulness
implementation complexity
risk
ability to expose foundation defects early
amount of speculative prerequisite work required
```

Choose the best evidence-backed first vertical, not necessarily the easiest.

### Gate 04

Record:

```text
candidate set
comparison criteria
trade-offs
selected Vertical #1
rejected/deferred alternatives and reasons
exact prerequisite foundation
```

Selection does not authorize implementation.

## 17. CP6-05 — Vertical #1 Exact Persistence Design

### Purpose

Design Vertical #1 to a level where the next phase can implement it without inventing persistence architecture on the fly.

### Required design precision

Where applicable define completely:

```text
relational tables/families
columns
PostgreSQL types
PK
FK
UNIQUE
CHECK
partial UNIQUE
DEFERRABLE constraints
EXCLUDE/range constraints
indexes
reference topology
material-state topology
current-state binding
history/lineage
chronology
provenance/governance binding
missing/unknown/negative semantics
retention/redaction/tombstone behavior
transaction boundaries
expected-state algorithm
locking/isolation/retry strategy
idempotency where applicable
primary query shapes
index justification
SQLAlchemy mapping shape
Alembic migration plan/order
runtime privilege implications
acceptance-test plan
```

This is **design only**.

CP6-05 may specify the exact migration that the next phase should create, but it must not create that migration.

CP6-05 may specify SQLAlchemy mapped structures, but it must not add the mapped classes.

CP6-05 may specify a capability persistence adapter boundary, but it must not implement the adapter.

### Gate 05

A fresh implementer should be able to answer from repository documentation, without conversation memory:

```text
what tables need to exist?
what does every column mean?
what are the PK/FK/reference rules?
what is current vs historical state?
what must PostgreSQL reject?
what race conditions must fail safely?
what migration should be written?
what SQLAlchemy mappings should be written?
what queries drive indexes?
what direct tests prove correctness?
```

If major persistence architecture decisions remain to be invented during the next implementation phase, Gate 05 is not PASS.

## 18. CP6-06 — PostgreSQL Foundation Direct Readiness Proof

### Boundary

CP6-06 proves the **PostgreSQL foundation**, not Vertical #1.

It may close direct evidence only when the subject already exists or can be exercised without manufacturing speculative business persistence.

### CP6-06 MAY

- re-prove existing CP2/CP3 PostgreSQL envelope/foundation where CP6 relies on it;
- directly validate already-materialized migration, role, transaction, extension and metadata behavior;
- directly validate a chosen global PostgreSQL rule when that proof does not create a speculative canonical/business primitive;
- use the isolated real-PostgreSQL test harness for non-business foundation verification;
- record explicit evidence gaps that intrinsically require the future business implementation;
- classify each PG-R/HG/PSV item by actual proof stage.

### CP6-06 MUST NOT

```text
create business tables merely to get evidence
create speculative shared canonical primitives merely to get evidence
create Vertical #1 Alembic migrations
create Vertical #1 SQLAlchemy mappings
create Vertical #1 persistence adapters
create Vertical #1 application operations
create business API routes
claim vertical-dependent HG/PSV items PASS before implementation exists
activate dormant specialist infrastructure solely to satisfy a paper checklist
```

### Non-speculative proof rule

A direct test is permitted only if its subject is one of:

```text
already materialized CP2/CP3 foundation
an accepted PostgreSQL capability exercised without becoming DANTE business schema
an actual CP6 foundation artifact independently justified for production use
```

A table/primitive whose only reason to exist is “so CP6 can test it” is forbidden.

### Gate 06

Produce a truth-preserving ledger:

```text
FOUNDATION DIRECT PASS
DIRECTLY TESTABLE BUT FAIL
NOT YET APPLICABLE — VERTICAL IMPLEMENTATION REQUIRED
NOT YET APPLICABLE — REAL V1→V2 EVOLUTION REQUIRED
NOT YET APPLICABLE — RECOVERY/RELEASE STAGE REQUIRED
NOT YET APPLICABLE — SPECIALIST DORMANT
```

A NOT-YET-APPLICABLE result is valid when the required real subject does not exist yet. It must carry an explicit future owner/stage.

CP6-06 is complete when no direct-proof obligation is ambiguously staged, not when every future Physical PSV item is falsely green.

## 19. CP6-07 — Whole Persistence Readiness / Clean-Room QA

### Purpose

Independently verify the new concrete persistence foundation and Vertical #1 design without re-running Domain/Logical discovery.

Core question:

> Can a fresh engineer reconstruct and implement Vertical #1 from repository truth without conversation memory and without inventing new global database rules?

### Required review

Check at minimum:

```text
Domain meaning preserved
Logical 57/57 dispositions preserved
WL-H01..12 preserved
accepted PostgreSQL Physical mapping preserved
CP3 persistence architecture preserved

CP6-01 coverage complete
CP6-02 constitution complete
CP6-03 relational topology complete
CP6-03 dependency DAG complete
CP6-03 vertical decomposition complete
CP6-04 Vertical #1 selection justified
CP6-05 Vertical #1 exact design complete
CP6-06 direct-proof ledger truthful

open architecture blockers = 0
unregistered concrete assumptions = 0
generic semantic escape hatches = 0
accidental specialist activation = 0
conversation-only material decision = 0
```

### Closure condition

Only after CP6-07 PASS may the workstream state become:

```text
CP6
CLOSED / CONCRETE PERSISTENCE READINESS PASS

CONCRETE POSTGRESQL FOUNDATION
CLOSED / READY

VERTICAL #1
SELECTED
EXACTLY DESIGNED
READY FOR IMPLEMENTATION
```

No Vertical #1 implementation is part of CP6 closure.

## 20. Phase after CP6

The next phase is separately authorized **after CP6 closure** and owns Vertical #1 implementation.

Its scope may include, after its own exact gate:

```text
approved Vertical #1 Alembic business migration(s)
approved SQLAlchemy business mappings
approved capability-specific persistence adapter
approved application operation(s)
real PostgreSQL semantic/constraint/concurrency acceptance
vertical-specific HG/PSV discharge
later API boundary only when separately authorized by that phase plan
```

Do not assume the next phase's formal checkpoint name/number until it is explicitly established after CP6 closure.

## 21. Explicit CP6 non-goals

Unless separately reopened by contradictory evidence, CP6 does not:

- revalidate or redesign the Domain kernel;
- redo the Logical owner census;
- redefine LR-01..LR-13;
- reconsider the four accepted ReferenceAddress families at semantic level;
- re-run PostgreSQL-vs-TypeDB technology selection;
- redesign the accepted Physical target stack;
- change the canonical authority away from PostgreSQL;
- create a universal Entity/Thing root;
- create a universal Relationship/edge root;
- create canonical EAV/property-bag storage;
- adopt universal event sourcing as ontology;
- use JSONB to hide required semantics;
- create one repository/service/module per Logical concept mechanically;
- create generic Repository/UoW/BaseService abstractions;
- implement Vertical #1;
- create Vertical #1 business migrations;
- create Vertical #1 business SQLAlchemy mappings;
- create Vertical #1 persistence adapters;
- create application use cases or business APIs;
- implement AuthN/AuthZ product behavior;
- activate PowerSync, Restate, R2, OR-Tools, PgBouncer or pgBackRest/S3 merely because selected;
- add Redis/Kafka/Neo4j/Qdrant/OpenSearch/Kubernetes/microservices by convenience;
- change frontend or brand assets;
- mutate CI/rulesets/CodeQL without separate authorization;
- mutate protected `main` directly;
- merge this branch without the normal protected PR path.

## 22. Write/gate discipline

Every material repository mutation requires its own exact gate:

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

Immediately before the first write, verify:

```text
current branch HEAD == approved PRE-SCOPE
```

If not identical, stop, inspect drift and re-gate.

After the write:

- fetch/read the written remote payload;
- compare exact PRE-SCOPE → new HEAD;
- verify added/modified/deleted path counts;
- verify unexpected paths = 0;
- verify branch relation to protected main;
- run applicable checks/tests where the scope has executable content;
- do not call a checkpoint PASS/CLOSED until its exact evidence contract is satisfied.

`main` remains protected and normal integration remains feature branch → PR → required checks → merge-commit path under current repository rules.

## 23. Temporary bootstrap retirement

The branch currently also contains:

```text
docs/workstreams/logical-postgresql-bootstrap.md
```

That file is intentionally temporary.

This durable handoff must first be remotely written and verified. Only **after** that verification may the temporary bootstrap be deleted under a separate explicit gate with a fresh PRE-SCOPE.

Do not combine bootstrap deletion with creation of this durable authority.

## 24. Resume point

A fresh session resuming CP6 must establish:

```text
1. live feature branch HEAD and relation to protected main;
2. this durable workstream handoff is current and readable;
3. temporary bootstrap has been retired only if a later gated deletion proves it;
4. CP6-00 remains complete unless repository drift materially invalidates it;
5. next unfinished checkpoint is CP6-01;
6. CP6-01 consumes the existing 57/57 Logical census rather than recreating it;
7. no business schema/migration/mapping/adapter may be created before CP6 closure;
8. Vertical #1 implementation begins only in the separately authorized post-CP6 phase.
```

Immediate next work after this handoff and bootstrap retirement is **CP6-01 — Concrete Persistence Coverage Map**, starting READ-ONLY/design-first from the complete closed Logical corpus and accepted PostgreSQL mapping.