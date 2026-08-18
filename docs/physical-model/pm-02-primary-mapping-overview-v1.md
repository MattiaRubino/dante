# PM-02 Primary Mapping Design Overview v1

- Status: **CURRENT — PM-02 DESIGN PACKAGE / UNVALIDATED UNTIL PM-03**
- Workstream: `feature/physical-model`
- PM-02 PRE-SCOPE: `fac3b5baf1813f886c4773594e6234810e5ba8c6`
- Upstream: Domain CLOSED; Logical CLOSED; `WL-H01..WL-H12` mandatory
- PM-01: PASS-CONDITIONAL; benchmark-host freeze HOLD
- Mapping execution: **DESIGN ONLY**
- Benchmark execution: **NOT STARTED**
- Technology selection: **NONE**

## 1. Purpose

Define one idiomatic Physical mapping for every PM-01 admitted primary candidate without forcing one database to imitate another and without weakening accepted LifeOS semantics.

The package contains:

```text
P0 PostgreSQL 18.4
P1 TypeDB CE 3.12.3
P2 XTDB 2.1.0
P3 SurrealDB Community 3.2.3
```

This is a design checkpoint, not correctness evidence.

```text
MAPPING WRITTEN != HARD-GATE PASS
OFFICIAL FEATURE != EXECUTED PROOF
PREFERRED != SELECTED
```

PM-03 must independently challenge every mapping against `HG-01..HG-12`.

## 2. Common semantic oracle

Every candidate must preserve the same accepted distinctions.

### Identity / addressability

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

No candidate may collapse these into one semantic identity family.

### State layers

```text
canonical LifeOS state
material historical state
derived / projection state
external / provider state
unresolved / candidate state
runtime / security state
transient computation state
```

### Whole hardenings

```text
WL-H01 Agreement terms bind justified material state
WL-H02 Governed Operation / Effect Contract
WL-H03 Projection / Disclosure Surface Contract
WL-H04 absence != false
WL-H05 expected-state consequential concurrency
WL-H06 idempotency != identity
WL-H07 multi-owner consistency
WL-H08 canonical != provider sync state
WL-H09 consequential derived-state freshness/material basis
WL-H10 retention/redaction/tombstone integrity
WL-H11 consequential AuthZ provenance
WL-H12 non-interference/inference leakage
```

### Non-collapses retained

```text
Person != Account != Actor
Subject / Resource / Actor != native root
Possibility != Goal != Proposal != Decision != Plan != Activity
Routine != Recurrence != Occurrence
Occurrence != Schedule != Session != Actual
Actual != Observation != Outcome
Evidence != Provenance
Version != Reconciliation
Authority != Visibility
Agreement != Consent
provider state != canonical state
derived projection != canonical truth
current state != historical state
correction != silent overwrite
```

## 3. PM-02 mapping policy

The mappings intentionally differ.

```text
SAME
semantic owners
Reference Contracts
hardening obligations
mutation meaning
history meaning
truth oracle

DIFFERENT
physical identity anchor
relation representation
state/history technique
constraint mechanism
concurrency hardening
query strategy
```

Shared implementation vocabulary is permitted only when it remains clearly technical.

A technical registry/guard/anchor:

```text
MAY support addressability, consistency or indexing
MUST NOT become universal Entity / Relationship / Fact / Version ontology
MUST NOT own domain lifecycle by convenience
```

## 4. Mapping IDs

```text
PM02-PG-001   docs/physical-model/mappings/postgresql-18.4-v1.md
PM02-TDB-001  docs/physical-model/mappings/typedb-3.12.3-v1.md
PM02-XT-001   docs/physical-model/mappings/xtdb-2.1.0-v1.md
PM02-SDB-001  docs/physical-model/mappings/surrealdb-3.2.3-v1.md
```

All four are `DESIGN COMPLETE / PM-03 NOT RUN`.

## 5. Cross-candidate architecture summary

| Concern | PostgreSQL | TypeDB | XTDB | SurrealDB |
|---|---|---|---|---|
| Native owners | owner-specific relational tables | owner-specific entity types | owner-specific dynamic tables | owner-specific `SCHEMAFULL` tables |
| Heterogeneous addressability | bounded technical anchors + direct FKs where homogeneous | relation-role interfaces / key attributes | four address-space anchor tables + ASSERT | typed record links / bounded anchors only where needed |
| Specific relations | owner-specific association tables | first-class relation types with named roles | owner-specific relation tables | typed record links or specific relation tables |
| N-ary relations | contextual record + party/role tables | native n-ary relation types | contextual record + role rows/tables | contextual normal records + participant records; not binary graph edge |
| MaterialStateRef | explicit stable state anchor + owner-specific state rows | owner-specific state object types with `material-state-id` keys | explicit state records; bitemporal system columns are not state identity | explicit state records with stable record IDs |
| History | current + owner-specific material history; selective effective periods | explicit owner/relation state objects and lineage | native bitemporality + explicit semantic material-state records | explicit material-state records; changefeeds are integration evidence only |
| Expected state | expected state predicate + transactional update/lock | current-state match + write conflict hardening | `ASSERT` against current state inside serialized DML tx | conditional update + technical consistency guard where needed |
| Multi-owner atomicity | one DB transaction; serializable/locks where needed | one write tx + invariant-boundary guard for write-skew pressure | one serialized DML transaction | one tx + invariant-boundary guard for write-skew pressure |
| Provider state | separate integration tables/schema | separate external/provider entity/relation types | separate external tables/address space | separate external/provider records |
| Derived state | views/materialized/cache records with source basis | functions/read queries or explicit projection objects | queries or explicit projection tables | computed fields/views or explicit projection records |
| Lazy Occurrence | bounded locator then NativeRef on differentiation/materialization | bounded locator outside persistent identity, then Occurrence entity | bounded locator + explicit Occurrence row when distinguished | bounded locator + Occurrence record when distinguished |
| Primary risk entering PM-03 | polymorphic-ref/history complexity | snapshot-isolation/write-skew and history verbosity | no FK/schema constraints + non-interactive DML | snapshot-isolation/write-skew + graph/document escape-hatch risk |

## 6. ReferenceAddress strategy by candidate

### PostgreSQL

Use a hybrid:

- direct owner FKs whenever a Reference Contract has one concrete target family;
- bounded technical address anchors only for heterogeneous slots;
- separate anchor spaces for native, scoped/material and external addressing rather than one `kind/id` root;
- owner table remains semantic authority.

### TypeDB

Use schema interfaces rather than a global object root:

- concrete entity/relation types implement the specific roles they are eligible to play;
- heterogeneous Reference Contracts are represented by role eligibility;
- application-visible addressing uses typed key attributes;
- TypeDB internal IID is not `NativeRef` or `MaterialStateRef`.

### XTDB

Because XTDB 2.1 has no native foreign keys and no uniqueness beyond `_id`, use explicit technical anchor tables plus transaction assertions:

```text
native_address
scoped_address
material_state_address
external_address
```

These are address indexes only. Canonical meaning remains in owner-specific tables.

### SurrealDB

Use typed record IDs/record links where the target table set is bounded; use specific relation tables for binary LR-03 semantics. A generic graph edge is forbidden as fallback. Contextual/n-ary semantics use normal `SCHEMAFULL` records plus typed participants.

## 7. Material-state strategy

No candidate is allowed to identify material semantic state with its storage revision token.

```text
PostgreSQL xmin/xid      != MaterialStateRef
TypeDB IID/tx snapshot   != MaterialStateRef
XTDB system-time/token   != MaterialStateRef
SurrealDB versionstamp   != MaterialStateRef
```

Every mapping therefore provides an explicit stable material-state identifier bound to an owner/facet.

The candidate may still use its native revision/isolation machinery to implement conflict detection or historical queries.

## 8. Current vs historical state

The baseline pattern is:

```text
stable semantic owner
+
current accepted material-state pointer/binding where applicable
+
retained material states/history
+
separate effective/world chronology where material
+
separate recorded/learned chronology where material
```

This is intentionally not universal event sourcing.

XTDB may answer more historical queries directly from its system/valid-time axes, but an explicit `MaterialStateRef` is still required when LifeOS semantics bind to a materially specific state.

## 9. Relation strategy

### Binary/simple relation

Use the candidate-native lightweight relation mechanism if it preserves the exact relation family and endpoint contract.

### Qualified/consequential relation

Escalate to an independently addressable contextual representation carrying:

```text
scoped record identity where required
roles/endpoints
material state/history where required
scope/purpose/context
provenance
governance/visibility basis
```

### N-ary Agreement

Must preserve common-ground semantics:

```text
one Agreement context
one justified terms MaterialStateRef
N party assent bindings to that same material terms state
```

Pairwise `agreed_with` edges are forbidden.

## 10. Expected-state strategy

Every consequential mutation design includes:

```text
expected MaterialStateRef
match/verify against current accepted state
apply mutation only on match
produce new material state where needed
return conflict on mismatch
```

The physical check may use candidate-native mechanisms but the storage token does not become semantic state identity.

## 11. Multi-owner consistency strategy

### PostgreSQL

Co-located invariants use one transaction, FK/unique/exclusion/deferrable constraints, row locking or `SERIALIZABLE` where required.

### TypeDB

A normal write transaction atomically changes multiple objects, but snapshot isolation alone is not assumed sufficient against write-skew. PM-02 introduces a narrow technical `consistency-guard` object per invariant boundary whose revision is updated by every consequential operation sharing that boundary. PM-03 must prove this actually forces the required conflict behavior.

### XTDB

All writes for one database are processed serially. A multi-owner mutation is one non-interactive DML transaction containing all `ASSERT` preconditions and writes. PM-03 must prove invariant checks and failure visibility under real concurrent submissions.

### SurrealDB

One transaction carries all co-located writes. Because the subject provides snapshot isolation with write-write conflict detection rather than serializable isolation, PM-02 uses a narrow technical `consistency_guard` record for invariant sets susceptible to write-skew. PM-03 must prove the guard and conditional-write semantics.

## 12. Temporal / recurrence strategy

No candidate maps all time to one timestamp.

Mappings preserve as separate where applicable:

```text
date-only
floating local wall-clock
named-zone wall-clock
absolute instant
range / interval
duration
precision / granularity
accepted resolution basis
```

Recurrence remains owner-specific `Recurrence` LR-05 semantics with explicit family.

The database's own temporal machinery does not replace recurrence semantics.

XTDB valid-time is used only where it truthfully represents world/effective applicability; it must not absorb all Schedule/Recurrence/Occurrence semantics.

## 13. Lazy Occurrence strategy

Before persistent individual addressability:

```text
governing source address
+ governing MaterialStateRef
+ recurrence family
+ semantic coordinate when one exists
= bounded occurrence locator
```

When an individual Occurrence becomes differentiated/persistently addressable, create the candidate's native Occurrence representation and retain locator/source lineage.

For unordered equivalent quota slots, do not invent an ordinal merely to generate IDs.

## 14. Provider / canonical separation

Every candidate keeps:

```text
provider/source scope
external opaque identifier
provider revision/version where material
provider payload/state
sync/apply status
reconciliation status
canonical mapping target
```

outside native identity/material-state semantics.

Provider success/failure never silently rewrites canonical LifeOS state.

## 15. Derived/projection strategy

LR-08 remains rebuildable/derived by default.

Any materialized projection used for consequence must expose:

```text
projection kind
source/bounded source set
source MaterialStateRefs or equivalent material basis
created/refreshed time
freshness/expiry semantics
purpose/context where material
```

A projection ID is not automatically a canonical semantic reference.

## 16. Retention / redaction / tombstone strategy

Every candidate must support this distinction where policy permits:

```text
never existed
!= existed but payload later redacted/unavailable
```

Native identity is never reused.

Candidate-specific methods differ, but the common design retains a minimal non-sensitive address/tombstone continuity while allowing payload/history erasure where policy requires.

## 17. Governed-effect provenance

The mapping package does not introduce a Domain `Operation` root.

For consequential mutations, candidate-specific physical history must be able to retain/reconstruct:

```text
operation family
semantic target/facet
expected material state
actual Actor
represented party where applicable
Principal/security context reference where applicable
governance basis MaterialStateRefs
purpose/context
idempotency key if used
correlation/causation metadata
resulting canonical effect state
provider/runtime outcome separately
```

This may be stored in bounded technical provenance/audit structures, not as universal LifeOS ontology.

## 18. Schema/evolution strategy

Every mapping includes an explicit mapping revision.

Evolution must prove later that it preserves:

```text
NativeRef continuity
ScopedRecordRef continuity
MaterialStateRef continuity
historical meaning
unknown vs negative states
provider/canonical separation
tombstone/redaction state
```

Migration convenience cannot rewrite semantic history.

## 19. PM-03 proof obligations

The following are deliberately unresolved until hard-gate preflight:

### PostgreSQL

- prove bounded address anchors do not become ontology or create invalid target references;
- prove owner-specific history/current pointers remain maintainable across 57 owners;
- prove `SERIALIZABLE`/locking strategy for consequential multi-owner changes;
- prove selective disclosure does not leak through FK/RLS/error behavior.

### TypeDB

- prove `ReferenceAddress` role eligibility can cover heterogeneous native/scoped/material/external targets without generic-root pressure;
- prove material state/history mapping is practical and reverse-mappable;
- prove technical consistency guards close snapshot-isolation write-skew for applicable invariants;
- prove deletion/redaction can preserve required tombstone/history continuity.

### XTDB

- prove anchor + `ASSERT` discipline supplies referential and cardinality integrity absent native FKs/schema constraints;
- prove MaterialStateRef remains distinct from system-time/snapshot tokens;
- prove non-interactive DML can express required governed mutations cleanly;
- prove dynamic schema evolution does not create silent semantic drift.

### SurrealDB

- prove `SCHEMAFULL` + typed record links prevent generic document/graph escape hatches;
- prove n-ary/material relations are not collapsed into binary edges;
- prove technical consistency guards close snapshot-isolation write-skew;
- prove retention/history semantics do not depend on bounded changefeed retention.

## 20. PM-02 disposition

```text
P0 PostgreSQL 18.4
MAPPING DESIGN COMPLETE
PM-03 NOT RUN

P1 TypeDB CE 3.12.3
MAPPING DESIGN COMPLETE
PM-03 NOT RUN

P2 XTDB 2.1.0
MAPPING DESIGN COMPLETE
PM-03 NOT RUN

P3 SurrealDB Community 3.2.3
MAPPING DESIGN COMPLETE
PM-03 NOT RUN

PM-02
DESIGN PACKAGE COMPLETE

HARD-GATE VERDICT
NONE YET

BENCHMARK
NOT STARTED

SELECTION
NONE
```

## 21. Current official capability sources used

Version-sensitive capability claims were rechecked against current official documentation before this package was written.

### PostgreSQL 18

- PostgreSQL 18 constraints, `CREATE TABLE`, range types, MVCC/concurrency and row-security documentation.

### TypeDB 3.x / subject 3.12.3

- TypeDB entities/relations/attributes, schema constraints (`@key`, `@unique`, `@card`) and transaction/isolation documentation.

### XTDB 2.1

- XTDB key concepts, bitemporal time model, SQL transaction/`ASSERT` reference and transaction-consistency documentation.

### SurrealDB 3.2

- SurrealDB `SCHEMAFULL`, record ID/link/reference, `RELATE`, architecture/isolation and changefeed documentation.

Official documentation is capability evidence only. PM-03/04+ must generate direct LifeOS evidence.