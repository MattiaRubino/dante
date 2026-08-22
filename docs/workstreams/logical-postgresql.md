# Workstream — CP6 Concrete Persistence Readiness

- **Status:** ACTIVE / DESIGN-FIRST / NO BUSINESS IMPLEMENTATION AUTHORIZED
- **Product:** DANTE
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/logical-postgresql`
- **Protected-main anchor at branch origin:** `fd3bc8dd918cf6aadeff4572221af68612c3cb42`
- **Upstream Domain Model:** CLOSED / SEMANTICALLY COMPLETE FOR CURRENT SCOPE
- **Upstream Logical Model:** CLOSED / 57 OF 57 CLASSIFIED / WL-H01..WL-H12 ACTIVE
- **Upstream Physical Model:** CLOSED / SELECTED / ACCEPTED / PostgreSQL 18.4 CANONICAL PRIMARY
- **Production backend scaffold:** CP1–CP5 CLOSED / DIRECT QA PASS / INTEGRATED IN PROTECTED main
- **CP6-00:** CLOSED / COMPLETE
- **CP6-01:** CLOSED / GATE 01 PASS
- **CP6-02:** NEXT / NOT STARTED
- **Business schema/migrations:** NOT STARTED / OUT OF CP6 IMPLEMENTATION SCOPE
- **Vertical #1 implementation:** OUT OF CP6 / SEPARATELY AUTHORIZED ONLY AFTER CP6 CLOSURE

## 1. Purpose and terminal boundary

CP6 is the bounded transition from the closed DANTE semantic/physical architecture and the closed CP1–CP5 technical backend foundation into a concrete, reusable PostgreSQL persistence foundation.

CP6 is **not** another Domain, Logical or Physical modeling cycle and is **not** the first business implementation phase.

It must end with:

```text
CLOSED DOMAIN
+
CLOSED LOGICAL
+
ACCEPTED POSTGRESQL PHYSICAL TARGET
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

Vertical #1 business migration, SQLAlchemy mapping, persistence adapter, application operation and business API belong to the separately authorized post-CP6 implementation phase.

## 2. Authority and precedence

Repository truth outranks conversation memory.

Use this precedence:

1. current protected-main code, migrations, tests and accepted model/ADR truth;
2. current durable Product / Domain / Logical / Physical / architecture / engineering documents;
3. this active bounded CP6 workstream for newer unmerged work;
4. other current workstream sources;
5. historical evidence, closed branches, PR/Git history;
6. conversation memory.

Implementation convenience never outranks accepted semantics.

A closed upstream decision may reopen only when concrete contradictory implementation evidence proves it cannot hold. Easier SQL, fewer joins, ORM convenience or generic schema preferences are not reopen evidence.

## 3. Mandatory continuation bootstrap

A fresh session must verify/read at minimum:

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
```

Then consume the complete closed Domain, Logical, Pre-Physical, Physical, Engineering and backend-scaffold workstreams including every canonical continuation.

Current CP6-01 authorities are deliberately split into non-competing responsibilities:

```text
docs/development/backend-cp6-01-concrete-persistence-coverage.md
= exact 57/57 owner/role persistence ledger

docs/development/backend-cp6-01-concrete-persistence-coverage-part-2.md
= single cross-cutting LR/WL-H/PG-R/DEFER-WL/HG/SC/PSV ledger

docs/development/backend-cp6-01-concrete-persistence-coverage-closure.md
= formal Gate 01 closure evidence
```

Do not stop at Part 1 of split canonical material.

## 4. CP6 classification discipline

Every material question is classified before design proceeds:

```text
INHERITED / CLOSED
accepted upstream decision; consume exactly

CONCRETE DECISION
true global PostgreSQL decision intentionally left open; CP6 must close it

VERTICAL-SPECIFIC
not needed for global foundation coherence; defer to the relevant vertical

DIRECT-PROOF
meaning/mechanism accepted; remaining work is executable evidence
```

This prevents both re-designing closed semantics and pretending genuinely open PostgreSQL choices were already decided.

## 5. Inherited semantic baseline — CLOSED

Whole Logical remains:

```text
DOMAIN CONCEPTS CLASSIFIED       57 / 57
UNCLASSIFIED                      0
LR-01 NATIVE OWNERS             15
GENERIC FALLBACK DEPENDENCIES     0
OWNERLESS MATERIAL STATE          0
REQUIRED UNIVERSAL ROOTS           0
```

Exact LR-01 native owners:

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

`Actor`, `Subject` and `Resource` remain contextual roles/capabilities. No ActorRef / SubjectRef / ResourceRef wrapper identity.

Accepted representation vocabulary remains LR-01..LR-13. Reference addressability remains discriminated:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

Do not collapse these into a universal semantic `kind + id` root.

## 6. Non-collapse invariants

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
provider state != canonical DANTE state
derived projection != canonical truth
current state != historical state
correction != silent overwrite
shared reality != per-recipient duplicate reality
AI/solver inference != accepted canonical effect
```

## 7. WL-H01..WL-H12 remain active

```text
WL-H01 Agreement terms bind justified owned MaterialStateRef; no ownerless TermsRef.
WL-H02 Consequential effects preserve operation/target/state/context/purpose/governance semantics.
WL-H03 Projection/disclosure surfaces preserve source/material basis/exposure boundary; no ProjectionRef root.
WL-H04 absence/no record != false/negative/non-realization.
WL-H05 stale-write-sensitive consequential mutation requires expected-state semantics.
WL-H06 idempotency != semantic identity.
WL-H07 multi-owner invariants require truthful atomicity or explicit staged/partial/reconciliation state.
WL-H08 canonical state != provider apply/sync state.
WL-H09 consequential LR-08 use revalidates or binds material derivation basis.
WL-H10 retention/redaction/tombstone preserves truthful permitted continuity; NativeRef never reused.
WL-H11 consequential AuthZ provenance preserves Actor/represented party/Principal/governance distinctions.
WL-H12 selective disclosure includes counts/existence/ranking/errors/timing/explanations/candidates/aggregates/relations.
```

## 8. Inherited PostgreSQL Physical baseline — CLOSED

```text
PostgreSQL 18.4
= sole canonical DANTE persistence + material-history authority
```

Selected bounded capabilities:

```text
PostGIS 3.6.4
pgvector 0.8.6
native FTS
pg_trgm
unaccent
pg_stat_statements
PgBouncer 1.25.2 selected / activation bounded
```

Accepted mapping thesis:

```text
owner-specific canonical families
+ owner-specific material-state/history families
+ specific relation families
+ bounded technical address/state anchors only where genuinely required
+ separate integration/projection/technical concerns
```

Hard rejects:

```text
universal Entity / Thing
universal Relationship / Edge
canonical EAV/property bag
universal event-log ontology
JSONB required-semantic escape hatch
PostgreSQL inheritance as ontology
```

Direct homogeneous FK remains preferred. MaterialStateRef remains independent from xmin/xid/updated_at/hash/ETag/provider revision. Current accepted state is not merely highest revision/latest row.

## 9. PostgreSQL risk and validation carry-forward

All PG-R01..PG-R10 remain active:

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

Physical post-selection validation remains staged truthfully. In particular:

```text
PSV-01 old-backup anti-resurrection
PSV-02 actual V1→V2 mapping/schema evolution
PSV-03 destructive restore + semantic verification
PSV-04 capacity/backpressure truthful degradation
PSV-05 WL-H12 system-level non-interference
PSV-35 selected PostgreSQL mapping end-to-end smoke corpus
```

Canonical search scenario bindings are singular:

```text
SC-017 = Search hidden-result non-interference
PSV-06 -> SC-017

SC-018 = FTS mixed filter/query
PSV-07 -> SC-018
```

Canonical `SC-*` names come from `docs/architecture/physical-benchmark-scenario-corpus.md`; downstream ledgers may not rename them.

## 10. Inherited CP1–CP5 backend foundation — CLOSED

Already materialized and directly tested:

```text
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
shared Base / MetaData
one Alembic environment / one migration DAG
version table dante.alembic_version
online migrations
SET ROLE dante_owner for migration DDL
dante_owner / dante_migrator / dante_runtime role separation
real PostgreSQL acceptance lane
```

Default isolation remains `READ COMMITTED`; stronger locking/isolation is invariant-specific. Do not introduce generic Repository[T], generic UnitOfWork, generic BaseService or a second persistence metadata system.

`CP3 TECHNICAL QA != BUSINESS-SEMANTIC HG PASS`.

## 11. CP6 checkpoint sequence

```text
CP6-00 Authority Reconstruction & Scope Freeze
CLOSED / COMPLETE
        ↓
CP6-01 Concrete Persistence Coverage Map
CLOSED / GATE 01 PASS
        ↓
CP6-02 PostgreSQL Persistence Constitution
NEXT / NOT STARTED
        ↓
CP6-03 Concrete Relational Topology
       + Implementation Dependency DAG
       + Vertical Decomposition
        ↓
CP6-04 Vertical #1 Selection
        ↓
CP6-05 Vertical #1 Exact Persistence Design
        ↓
CP6-06 PostgreSQL Foundation Direct Readiness Proof
        ↓
CP6-07 Whole Persistence Readiness / Clean-Room QA
        ↓
CP6 CLOSED
```

## 12. CP6-00 — CLOSED

Read-only authority reconstruction completed with Domain, Logical 57/57 + WL-H, accepted PostgreSQL Physical mapping, PG-R, PSV and CP3/CP5 implementation reconstructed. Business schema remained absent.

## 13. CP6-01 — CLOSED / GATE 01 PASS

Formal closure:

`docs/development/backend-cp6-01-concrete-persistence-coverage-closure.md`

Gate result:

```text
57/57 Domain concepts                         PASS
15/15 LR-01                                   PASS
LR-01..LR-13                                  PASS
cross-cutting/non-owner coverage              PASS
WL-H01..WL-H12                                PASS
PG-R01..PG-R10                                PASS
DEFER-WL01..20                                ASSIGNED / COMPLETE
HG-01..HG-12                                  STAGED TRUTHFULLY
SC-001..SC-035                                CANONICAL / STAGED
full PSV ledger                               STAGED / COMPLETE
CP3 technical-vs-semantic distinction         PASS
current active documentation contradictions   0
semantic owner reclassification               0
generic semantic fallback                     0
canonical JSONB escape hatch                   0
business DDL                                  0
business migration                            0
business SQLAlchemy mapping                   0
persistence adapter                           0
Physical Model reopen                         0
false direct HG/SC/PSV PASS                   0
```

CP6-01 must not be redone unless concrete contradictory evidence appears.

## 14. CP6-02 — PostgreSQL Persistence Constitution

**Status: NEXT / NOT STARTED.**

Purpose: close global reusable PostgreSQL rules future verticals consume instead of re-deciding repeatedly. It is the DANTE database constitution, not complete future DDL.

Required constitution families:

```text
ID
physical identifier strategy, generation locus, opacity/exposure,
sortability/offline-safe implications, immutability/non-reuse

REF
direct homogeneous FK doctrine, bounded heterogeneous Native/Scoped/Material/External addressing,
eligibility and dangling-reference prevention

MAT
MaterialStateRef physical shape, owner/facet binding, current accepted-state binding,
immutability/correction/replacement/reconciliation/lineage

HIST / TIM
material history, world/effective chronology, recorded/learned/accepted chronology,
historical reconstruction, dual-chronology trigger

MISS
NULL, row absence, explicit unknown, explicit negative, N/A, redacted, unavailable, retired

TYP
ENUM vs text+CHECK vs reference table, DOMAIN/composite/array/range/multirange decision rules

REL
simple binary, qualified/material, n-ary, addressable/governance/history relation patterns

PROV
bounded consequential provenance: operation family, target/facet, expected state,
Actor, represented party, Principal context, governance basis, purpose/context,
idempotency/correlation/causation, canonical result, provider/runtime result separately

LIFE
retirement, logical removal, redaction, tombstone/reference continuity,
identity non-reuse, lineage minimization, anti-resurrection

CON
NOT NULL/CHECK/FK/UNIQUE/partial UNIQUE/DEFERRABLE/EXCLUDE/trigger/application-check doctrine

TX
race/invariant taxonomy, expected state, locking/conditional write,
isolation escalation, retry/reconciliation/conflict behavior

IDEM
scope + key + material fingerprint + replay/different-operation conflict + retention

IDX
FK/composite/partial/INCLUDE/GiST/GIN/search index evidence doctrine

CAP
PostGIS/FTS/pg_trgm/unaccent/pgvector/JSONB activation boundaries

MIG
Alembic single-head, reviewed DDL, data migration/backfill,
expand→migrate→contract, downgrade-vs-forward-fix, cutover, drift,
identity/reference/history continuity

SEC
future business objects inherit CP3 owner/migrator/runtime posture

QA
positive/negative constraints, wrong-family/dangling refs, history reconstruction,
unknown-vs-negative, concurrency, multi-owner races, rollback/atomicity,
privilege rejection, fresh DB→head, single head, drift, evolution, later recovery
```

Gate 02 requires all genuinely global decisions closed, all inherited decisions traceable, all remaining choices explicitly vertical-specific, and every direct-proof obligation assigned to a truthful stage.

No business DDL is authorized by Gate 02.

## 15. CP6-03 — Concrete Relational Topology + Dependency DAG + Vertical Decomposition

Must establish conceptual/concrete relational families, foundation prerequisites, implementation dependency order and coherent vertical boundaries.

A vertical is not automatically one Domain owner, Logical owner, table, route, screen or repository.

Gate 03 requires coherent relational families, explicit dependencies/vertical order, preserved 57/57 coverage, no speculative DDL and no Physical Model redesign.

## 16. CP6-04 — Vertical #1 Selection

Select only after CP6-03 using evidence across foundation leverage, semantic/reference/history/concurrency/provenance coverage, product usefulness, implementation complexity, risk and ability to expose foundation defects early.

Do not pre-select Access, Identity, Goal, Planning or another candidate by intuition alone.

Selection does not authorize implementation.

## 17. CP6-05 — Vertical #1 Exact Persistence Design

Design Vertical #1 to implementation-ready precision, including where applicable:

```text
tables/families
columns/types
PK/FK/UNIQUE/CHECK/partial UNIQUE/DEFERRABLE/EXCLUDE
indexes and query justification
reference topology
material/current/history/lineage topology
chronology
provenance/governance
missing/unknown/negative semantics
retention/redaction/tombstone
transaction boundaries
expected-state/locking/isolation/retry
idempotency
SQLAlchemy mapping shape
Alembic migration plan
privilege implications
acceptance-test plan
```

Design only: do not create the migration, mapped classes, adapter or application operation.

## 18. CP6-06 — PostgreSQL Foundation Direct Readiness Proof

May re-prove or directly test only already materialized/non-speculative foundation subjects. Must not invent business tables or speculative shared canonical primitives just to obtain a green test.

Truth-preserving result classes:

```text
FOUNDATION DIRECT PASS
DIRECTLY TESTABLE BUT FAIL
NOT YET APPLICABLE — VERTICAL IMPLEMENTATION REQUIRED
NOT YET APPLICABLE — REAL V1→V2 EVOLUTION REQUIRED
NOT YET APPLICABLE — RECOVERY/RELEASE STAGE REQUIRED
NOT YET APPLICABLE — SPECIALIST DORMANT
```

## 19. CP6-07 — Whole Persistence Readiness / Clean-Room QA

A fresh engineer must be able to reconstruct and implement Vertical #1 from repository truth without conversation memory and without inventing global database rules.

Closure requires zero open architecture blockers, unregistered concrete assumptions, generic semantic escape hatches, accidental specialist activations or conversation-only material decisions.

Only then:

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

## 20. Phase after CP6

Separately authorized Vertical #1 implementation may then create the approved business migration(s), SQLAlchemy mappings, capability-specific persistence adapter, application operations and direct semantic/concurrency acceptance.

Do not assume the next phase's formal checkpoint name/number before CP6 closure.

## 21. Explicit CP6 non-goals

CP6 does not, absent separately gated contradictory evidence:

- redesign Domain/Logical/Physical;
- change PostgreSQL canonical authority;
- create universal Entity/Relationship/EAV/event ontology;
- use JSONB to hide required semantics;
- mechanically create one module/table/service per Logical concept;
- introduce generic Repository/UoW/BaseService abstractions;
- implement Vertical #1;
- create Vertical #1 migrations/mappings/adapters/use cases/APIs;
- implement AuthN/AuthZ product behavior;
- activate PowerSync, Restate, R2, OR-Tools, PgBouncer or pgBackRest/S3 merely because selected;
- add unapproved Redis/Kafka/Neo4j/Qdrant/OpenSearch/Kubernetes/microservices;
- change frontend/brand assets;
- mutate CI/rulesets/CodeQL without separate authorization;
- mutate protected main directly;
- merge the branch outside the normal protected PR path.

## 22. Write/gate discipline

Every material repository mutation requires an exact gate with:

```text
BRANCH
PRE-SCOPE
CREATE
UPDATE
DELETE
PURPOSE
EXPLICITLY OUT OF SCOPE
```

Immediately before the first write verify live HEAD equals approved PRE-SCOPE. After write: remote readback, exact PRE-SCOPE→HEAD delta, added/modified/deleted/unexpected counts, branch relation to main, and applicable checks.

Do not call a checkpoint PASS/CLOSED before its evidence contract is satisfied.

## 23. Bootstrap retirement — COMPLETE

`docs/workstreams/logical-postgresql-bootstrap.md` is retired and must not be used as current authority. Git history preserves it only as provenance.

## 24. Current resume point

A fresh session must establish:

```text
1. live feature/logical-postgresql HEAD and relation to protected main;
2. this durable handoff is current;
3. CP6-00 is CLOSED / COMPLETE;
4. CP6-01 is CLOSED / GATE 01 PASS;
5. Part 1 is the exact 57/57 owner ledger;
6. Part 2 is the single cross-cutting LR/WL-H/PG-R/DEFER-WL/HG/SC/PSV ledger;
7. the CP6-01 closure record is present and authoritative;
8. CP6-02 is NEXT / NOT STARTED;
9. no business schema/migration/mapping/adapter is authorized anywhere in CP6;
10. Vertical #1 implementation begins only after CP6 closes under a separate authorization.
```

Immediate next action:

```text
CP6-02 POSTGRESQL PERSISTENCE CONSTITUTION
READ/RESEARCH/DESIGN FIRST
        ↓
GATE 02 only after its full constitution contract is satisfied
```

No Domain, Logical or Physical redesign is implied by this resume point.