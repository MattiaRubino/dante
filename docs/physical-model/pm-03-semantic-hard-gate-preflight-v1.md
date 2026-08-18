# PM-03 Semantic Hard-Gate Preflight v1

- Status: **CURRENT — STATIC PREFLIGHT COMPLETE / EXECUTED HARD GATES NOT RUN**
- Workstream: `feature/physical-model`
- PM-03 PRE-SCOPE: `db127af8c759aacf69b43d0f5a5444b04fd43759`
- Date: 2026-08-18
- Mapping subjects: `PM02-PG-001`, `PM02-TDB-001`, `PM02-XT-001`, `PM02-SDB-001`
- Database deployment: **NOT STARTED**
- Harness/fixtures: **NOT STARTED**
- Benchmark execution: **NOT STARTED**
- Technology selection: **NONE**

## 1. Purpose

PM-03 is a destructive semantic preflight over the four PM-02 primary mappings before executable benchmark infrastructure exists.

It asks:

> Does the proposed candidate-native mapping contain a structural semantic contradiction, generic-root escape hatch, reference collapse, concurrency lie, history lie, governance collapse or temporal/history shortcut that should block the candidate before implementation?

PM-03 does **not** prove runtime behavior that requires an actual database, concurrent execution, backup/restore or migration run.

Therefore two result layers remain distinct:

```text
PM-03 STATIC PREFLIGHT RESULT
PASS-CONDITIONAL | HOLD | REJECT | NOT-APPLICABLE

EXECUTED HG RESULT
NOT RUN until direct PM-05/PM-07 evidence exists
```

A static `PASS-CONDITIONAL` means the mapping is structurally credible and may advance to executable proof. It is not a benchmark hard-gate PASS.

## 2. Authority consumed

The preflight consumes without reopening:

- CLOSED Domain Atlas and Whole-Domain closure;
- CLOSED Whole-Logical Model and full decision/assumption register;
- `WL-H01..WL-H12`;
- Phase-10 Physical Benchmark Specification and Scenario Corpus;
- Physical acceptance matrix;
- PM-01 technology/candidate freeze;
- PM-02 mapping overview and all four candidate mappings;
- current official product documentation for version-sensitive transaction/schema/relation capabilities.

No candidate is allowed to weaken accepted semantics to improve its preflight result.

## 3. Evaluation rule

For each candidate and each `HG-01..HG-12`, PM-03 classifies the mapping using:

```text
PASS-CONDITIONAL
static design is coherent and a plausible native mechanism exists;
direct executable confirmation remains mandatory where the benchmark requires it

HOLD
one or more material claims depend on direct behavior not safely inferable from the mapping/docs,
or a candidate-specific integrity mechanism remains materially unproven

REJECT
an idiomatic good-faith mapping still requires violating a closed semantic invariant

NOT-APPLICABLE
only where the gate genuinely does not apply; none of HG-01..HG-12 is globally N/A for current primary candidates
```

Generic future execution requirements such as destructive restore remain `HOLD` for every candidate rather than being converted into paper PASS.

## 4. Cross-candidate preflight matrix

| Gate | PostgreSQL 18.4 | TypeDB CE 3.12.3 | XTDB 2.1.0 | SurrealDB CE 3.2.3 |
|---|---|---|---|---|
| HG-01 Semantic ownership | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-02 Reference-family integrity | PASS-CONDITIONAL | PASS-CONDITIONAL | **HOLD** | PASS-CONDITIONAL |
| HG-03 Typed/n-ary relation fidelity | PASS-CONDITIONAL | PASS-CONDITIONAL | **HOLD** | PASS-CONDITIONAL |
| HG-04 Expected-state concurrency | PASS-CONDITIONAL | **HOLD** | PASS-CONDITIONAL | **HOLD** |
| HG-05 Multi-owner consistency | PASS-CONDITIONAL | **HOLD** | PASS-CONDITIONAL | **HOLD** |
| HG-06 History/correction/reconciliation | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-07 State-layer separation | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-08 Governance/selective disclosure | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-09 Retention/redaction/tombstone/restore | **HOLD** | **HOLD** | **HOLD** | **HOLD** |
| HG-10 Temporal/recurrence/timezone | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-11 Schema/data evolution | **HOLD** | **HOLD** | **HOLD** | **HOLD** |
| HG-12 Recoverability/evidence quality | **HOLD** | **HOLD** | **HOLD** | **HOLD** |

Counts:

```text
PostgreSQL  PASS-CONDITIONAL 9   HOLD 3   REJECT 0
TypeDB      PASS-CONDITIONAL 7   HOLD 5   REJECT 0
XTDB        PASS-CONDITIONAL 7   HOLD 5   REJECT 0
SurrealDB   PASS-CONDITIONAL 7   HOLD 5   REJECT 0
```

These counts are not scores and must never be used as a ranking. A HOLD may be a generic future execution obligation or a candidate-specific risk of very different severity.

## 5. Candidate-specific material HOLDs

### P0 PostgreSQL

No candidate-specific static HOLD was found in HG-01..HG-08/HG-10.

The remaining HOLDs are direct-execution obligations:

```text
HG-09 destructive retention/redaction + old-backup anti-resurrection
HG-11 V1 -> V2 migration/evolution
HG-12 destructive backup/restore/recovery evidence
```

This does not mean PostgreSQL has passed those gates.

### P1 TypeDB

Material candidate-specific HOLDs:

```text
HG-04 expected-state consequential concurrency
HG-05 multi-owner predicate/write-skew consistency
```

Reason: the exact TypeDB 3.x transaction model documents ACID guarantees up to snapshot isolation. PM-02's narrow `consistency-guard` mutation is a plausible hardening pattern, but PM-03 cannot truthfully prove from documentation alone that all representative LifeOS stale/predicate races are closed.

Executable pressure must include same-base race and disjoint-owner write-skew where both operations touch the same guard.

Generic future execution HOLDs also remain HG-09/HG-11/HG-12.

### P2 XTDB

Material candidate-specific HOLDs:

```text
HG-02 ReferenceAddress/ref integrity without conventional FK constraints
HG-03 role/cardinality/uniqueness fidelity without conventional schema constraints
```

XTDB documents serialized DML transactions and `ASSERT`, which gives a strong path for HG-04/HG-05, but the mapping deliberately accepts extra writer-side integrity machinery. PM-03 cannot prove that every consequential reference/relation creation path is complete and bypass-safe without implementing the canonical mutation pack.

The direct proof must show:

- wrong-family references reject;
- dangling references reject;
- cardinality/uniqueness races reject;
- split/incomplete assertions cannot be accepted as canonical writer behavior.

Generic future execution HOLDs remain HG-09/HG-11/HG-12.

### P3 SurrealDB

Material candidate-specific HOLDs:

```text
HG-04 expected-state consequential concurrency
HG-05 multi-owner predicate/write-skew consistency
```

SurrealDB documents snapshot isolation with write-write conflict detection. The PM-02 narrow `consistency_guard` pattern intentionally turns disjoint semantic writes that share an invariant into one write-write contention point. That design is plausible but must be executed under the exact Community 3.2.3/RocksDB subject before it receives credit.

Generic future execution HOLDs remain HG-09/HG-11/HG-12.

## 6. HG-01 — semantic ownership preservation

### PostgreSQL — PASS-CONDITIONAL

The mapping uses owner-specific tables, specific relation families and bounded technical anchors. The anchor design is explicitly barred from owning generic Domain properties.

Static destructive mutations rejected by design:

```text
M-PG-01 move all owners into one Entity table                    REJECTED
M-PG-02 use JSONB generic property bag for required semantics    REJECTED
M-PG-03 route every semantic relation through generic edge       REJECTED
```

Executable C0 reverse mapping still remains mandatory.

### TypeDB — PASS-CONDITIONAL

Concrete owner entity/relation types and named roles preserve semantic specificity. TypeDB's PERA model is used as implementation structure, not as permission to create one LifeOS semantic root.

Rejected mutation:

```text
M-TDB-01 introduce universal LifeOS object/thing supertype with generic properties
REJECTED
```

### XTDB — PASS-CONDITIONAL

Owner-specific tables and four separated address spaces preserve owner meaning despite a flexible row model.

Rejected mutation:

```text
M-XT-01 use dynamic schema as a generic canonical fact/property store
REJECTED
```

### SurrealDB — PASS-CONDITIONAL

`SCHEMAFULL` owner tables and specific relation tables prevent the multimodel engine from becoming a universal document/graph ontology.

Rejected mutations:

```text
M-SDB-01 canonical SCHEMALESS/FLEXIBLE object root    REJECTED
M-SDB-02 universal edge(type,payload)                 REJECTED
```

## 7. HG-02 — Reference-family integrity

### PostgreSQL — PASS-CONDITIONAL

The mapping keeps `NativeRef`, `ScopedRecordRef`, `MaterialStateRef` and `ExternalRef` separate and uses direct FKs where contracts are homogeneous plus bounded address anchors for real heterogeneous addressing.

Direct proof must verify owner-family eligibility and anchor-to-owner existence.

### TypeDB — PASS-CONDITIONAL

Reference family reconstructibility comes from concrete type + explicit key family + containing semantic role/Reference Contract. Internal IID and transaction snapshot are explicitly excluded from semantic reference identity.

### XTDB — HOLD

The four address spaces are correctly separated, but no conventional FK constraint automatically protects every reference path. `ASSERT` can enforce the contract inside controlled writes, yet the actual mutation pack must prove complete enforcement.

The HOLD is candidate-specific and must not be normalized away as ordinary application validation.

### SurrealDB — PASS-CONDITIONAL

Typed record links/unions plus separate material/external address structures can preserve the discriminated family. Direct proof must show generic record references cannot bypass the accepted target set.

## 8. HG-03 — typed/n-ary relation fidelity

### PostgreSQL — PASS-CONDITIONAL

Dedicated binary association tables plus contextual/material relation records can represent specific relations. Agreement is represented as one common contextual record + party assent bound to the same terms `MaterialStateRef`.

### TypeDB — PASS-CONDITIONAL

This is TypeDB's strongest static fit: first-class relation types, named roles and cardinality constraints directly represent binary and n-ary structures. This is not a performance result.

### XTDB — HOLD

Specific relation-family tables and n-ary Agreement mapping are semantically sound, but role/cardinality/uniqueness integrity is largely enforced through `_id` design + `ASSERT` + writer discipline rather than native FK/cardinality constraints. Executable destructive proof is required before the gate can advance.

### SurrealDB — PASS-CONDITIONAL

Binary relations may use typed `TYPE RELATION` tables; n-ary/material structures deliberately use normal contextual records rather than being forced into pairwise graph edges.

## 9. HG-04 — expected-state consequential concurrency

### PostgreSQL — PASS-CONDITIONAL

The mapping carries expected `MaterialStateRef`, supports conditional current-state update/locking and can escalate predicate-sensitive operations to Serializable transactions. PostgreSQL documents Serializable behavior that prevents serialization anomalies, with retry on serialization failure.

SC-001/SC-009 direct races remain mandatory.

### TypeDB — HOLD

Exact-current-state matching solves direct stale updates but snapshot isolation can permit predicate/write-skew over disjoint objects. The narrow technical guard may close this if shared guard mutation creates the required conflict, but direct proof is mandatory.

### XTDB — PASS-CONDITIONAL

The mapping places expected-state checks in the DML transaction using `ASSERT`. XTDB documents serialized DML transactions through a totally ordered log and serializable behavior. The precondition design is therefore structurally credible.

Direct SC-001 proof remains required.

### SurrealDB — HOLD

Snapshot isolation + write-write detection does not by itself establish predicate serializability. The narrow guard pattern is plausible but unproven for the actual subject.

## 10. HG-05 — multi-owner consistency truthfulness

### PostgreSQL — PASS-CONDITIONAL

One local PostgreSQL transaction can update multiple co-located owner/relation/state rows atomically; candidate mapping also explicitly separates external/provider partial effects into staged/reconciliation state.

Predicate-sensitive invariants must use a mechanism strong enough for the actual race, not merely default Read Committed.

### TypeDB — HOLD

A write transaction can carry multiple co-located changes atomically, but snapshot-isolation write-skew remains material for invariants spanning disjoint objects. Guard execution is mandatory.

### XTDB — PASS-CONDITIONAL

All co-located effects plus invariant `ASSERT`s can be placed in one serialized DML transaction. The non-interactive transaction model is accepted only if representative governed operations can express all necessary preconditions/effects declaratively.

### SurrealDB — HOLD

Multi-statement transactions are atomic, but predicate invariants under snapshot isolation still depend materially on the guard pattern.

## 11. HG-06 — history/correction/reconciliation reconstructibility

All four candidates receive **PASS-CONDITIONAL** at static preflight.

Common reason:

- stable owner identity remains separate from material-state identity;
- explicit `MaterialStateRef` remains independent from engine storage tokens;
- current-state access uses explicit current binding/state rather than lifetime replay;
- correction/provenance/reconciliation are retained as specific lineage/state;
- provider revision remains external state.

Candidate distinctions:

```text
PostgreSQL  owner-specific material-state/history structures
TypeDB      explicit material-state types + typed lineage relations
XTDB        explicit material states + native bitemporal substrate where semantically aligned
SurrealDB   explicit material states; changefeed explicitly rejected as canonical history
```

SC-010/013/014 remain mandatory direct proof.

## 12. HG-07 — state-layer separation

All four candidates receive **PASS-CONDITIONAL**.

Every mapping keeps distinguishable:

```text
canonical
material history
provider/external
derived/projection
candidate/unresolved
runtime/security
```

Co-location in one engine is never used as evidence of semantic equivalence.

SC-004/005/006/008/026/027/034 must still execute later.

## 13. HG-08 — governance/selective disclosure

All four candidates receive **PASS-CONDITIONAL**, with different enforcement risks.

The mappings preserve canonical Authority/Consent/Visibility/Representation separately from technical authorization and avoid per-recipient canonical duplication.

Candidate pressure:

```text
PostgreSQL
RLS is a possible enforcement ingredient, not selected authority;
FK/constraint behavior can create covert-channel pressure and must be tested.

TypeDB
rich role/type structure may improve semantic query precision but does not itself supply WL-H12 non-interference.

XTDB
query/application enforcement must prevent historical/bitemporal/count leakage; native bitemporal access is not automatically recipient-safe.

SurrealDB
table/field permissions are an enforcement ingredient, but Domain Visibility is richer than database record permissions and system-user paths remain a separate trust boundary.
```

SC-007/008/016/033 remain mandatory proof.

## 14. HG-09 — retention/redaction/tombstone/restore integrity

**HOLD for all four candidates.**

Static mappings all contain plausible tombstone/redaction separation, but the hard gate explicitly requires old-backup restore anti-resurrection behavior. No database has been deployed and no destructive restore has occurred.

Candidate-specific later pressure:

```text
PostgreSQL  tombstone + retained deletion ledger / restore reconciliation
TypeDB      payload/attribute/relation removal while preserving permitted minimal keys/history
XTDB        normal temporal deletion vs irreversible ERASE + retained non-sensitive anchor
SurrealDB   relation cleanup vs qualified historical relation/tombstone continuity
```

SC-011/012 and PM-07 direct evidence are mandatory.

## 15. HG-10 — temporal/recurrence/timezone fidelity

All four candidates receive **PASS-CONDITIONAL**.

None of the mappings reduces canonical time to UTC-only or equates storage temporal features with Recurrence/Schedule/Actual semantics.

Candidate observations:

```text
PostgreSQL
explicit temporal shapes + named-zone semantics + ranges/constraints where useful

TypeDB
semantic temporal forms represented through explicit typed attributes/structures

XTDB
native valid/system axes used only where their meaning matches accepted world/record chronology;
explicit semantic timestamps retained where needed

SurrealDB
explicit semantic temporal structures; datetime used only for actual instant semantics
```

SC-022..025 and lazy-Occurrence pressure remain direct proof obligations.

## 16. HG-11 — schema/data evolution integrity

**HOLD for all four candidates.**

Each PM-02 mapping has a credible migration strategy, but HG-11 requires a real V1 -> V2 evolution preserving identity, references, history, governance basis and tombstones.

Static documentation cannot prove that.

SC-030 is mandatory later.

## 17. HG-12 — recoverability/evidence quality

**HOLD for all four candidates.**

Reasons:

```text
benchmark host still HOLD
no exact executable deployment frozen for PM-04+
no backup created
no destructive restore performed
no post-restore semantic oracle run
```

PM-01 product documentation about backup/restore remains capability evidence only.

SC-031 and relevant failure-injection evidence are mandatory.

XTDB additionally retains its production-topology HOLD.

## 18. Destructive mutation summary

The static review explicitly attempted the following classes of mapping corruption:

```text
universal Entity/Thing root
universal generic edge
canonical EAV/property bag
generic TypedRef(kind,id) collapsing address spaces
storage token/transaction timestamp as MaterialStateRef
pairwise reconstruction of n-ary Agreement
missing row interpreted as false
provider revision promoted to canonical state
latest row/event promoted to current semantic truth
UTC-only canonical temporal representation
recurrence reduced to storage valid-time/calendar provider shape
stale consequential update without expected state
snapshot-isolation write-skew without coordination
external partial effect reported as atomic success
changefeed/event log promoted to canonical history
per-recipient canonical duplication for disclosure
old-backup restore treated as automatically safe
schema flexibility treated as migration strategy
```

All four PM-02 designs reject these shortcuts. The remaining HOLDs identify where runtime proof rather than prose is required.

## 19. Candidate advancement decision

PM-03 finds **no static REJECT**.

```text
P0 PostgreSQL 18.4
ADVANCE TO EXECUTABLE PROOF
candidate-specific static blocker: NONE

P1 TypeDB CE 3.12.3
ADVANCE WITH CONCURRENCY HOLD
must prove consistency-guard write-skew closure

P2 XTDB 2.1.0
ADVANCE WITH REFERENCE/CONSTRAINT HOLD
must prove ASSERT-based integrity across canonical write paths
production topology remains HOLD

P3 SurrealDB CE 3.2.3
ADVANCE WITH CONCURRENCY HOLD
must prove consistency-guard write-skew closure
```

`ADVANCE` means the candidate deserves implementation/executable testing. It does not mean the hard gates have passed.

## 20. Primary executable proof pack derived from PM-03

The first executable correctness pack must prioritize the uncertain mechanisms rather than start with performance.

### Shared mandatory core

```text
SC-001 same-base consequential race
SC-003 atomic multi-owner mutation
SC-009 offline/stale-base divergence
SC-010 correction without false rewrite
SC-012 NativeRef non-reuse
SC-015 typed n-ary relation fidelity
SC-016 selective disclosure without source leakage
SC-022/023 DST gap/fold
SC-024 individual recurrence override
SC-030 V1->V2 evolution
SC-011 + SC-031 destructive restore/anti-resurrection
```

### TypeDB priority additions

```text
concurrent disjoint semantic writes sharing one consistency guard
same invariant without guard as negative control
commit-conflict/retry semantics
```

### XTDB priority additions

```text
wrong-family ReferenceAddress creation
missing-target reference
cardinality/uniqueness race
incomplete ASSERT pack negative control
non-interactive complex governed mutation
```

### SurrealDB priority additions

```text
write-skew without guard negative control
same race with narrow guard
record-union/reference-family rejection
binary relation vs contextual n-ary Agreement
```

### PostgreSQL priority additions

```text
heterogeneous anchor wrong-family/dangling target
Read-Committed negative-control race vs selected stronger mechanism
Serializable/locking retry behavior
RLS/query leakage pressure where later enforcement design uses RLS
```

## 21. PM-03 final disposition

```text
PM-03 STATIC DESTRUCTIVE REVIEW
COMPLETE

STATIC REJECTS
0 / 4 candidates

EXECUTED HARD GATES
NOT RUN

P0 PostgreSQL
ADVANCE

P1 TypeDB
ADVANCE WITH CONCURRENCY HOLD

P2 XTDB
ADVANCE WITH REFERENCE/CONSTRAINT HOLD
PRODUCTION TOPOLOGY HOLD

P3 SurrealDB
ADVANCE WITH CONCURRENCY HOLD

BENCHMARK HOST
HOLD

PM-04 EXECUTABLE HARNESS/FIXTURES
NOT STARTED

PERFORMANCE
NOT STARTED

SELECTION
NONE
```

## 22. Official primary-source refresh used by PM-03

Current version-sensitive capability claims were rechecked on 2026-08-18 against official documentation.

PostgreSQL:

- https://www.postgresql.org/docs/18/transaction-iso.html
- https://www.postgresql.org/docs/18/features-sql-standard.html
- https://www.postgresql.org/docs/18/ddl-rowsecurity.html

TypeDB:

- https://typedb.com/docs/core-concepts/typedb/transactions/
- https://typedb.com/docs/core-concepts/typeql/constraining-data/
- https://typedb.com/docs/typeql-reference/annotations/key/
- https://typedb.com/docs/typeql-reference/annotations/card/

XTDB:

- https://docs.xtdb.com/about/txs-in-xtdb.html
- https://docs.xtdb.com/reference/main/sql/txs.html

SurrealDB:

- https://surrealdb.com/docs/architecture
- https://surrealdb.com/docs/reference/query-language/statements/define/table
- https://surrealdb.com/docs/reference/query-language/statements/relate
- https://surrealdb.com/docs/learn/querying/concepts-and-guides/transactions

These sources are capability evidence, not executed LifeOS hard-gate proof.
