# PostgreSQL 18.4 Physical Mapping v1

- Mapping ID: `PM02-PG-001`
- Candidate: PostgreSQL
- Exact PM-01 subject: PostgreSQL **18.4**, self-hosted single-node qualification topology; psycopg **3.3.4**
- Status: **PM-02 DESIGN COMPLETE / PM-03 NOT RUN**
- Selection: **NOT SELECTED**
- Purpose: idiomatic PostgreSQL mapping of the closed LifeOS Logical Model; no executable DDL is authorized by this document.

## 1. Design thesis

Use PostgreSQL as an explicit typed relational/hybrid store:

```text
owner-specific canonical tables
+ owner-specific material-state/history tables
+ specific relation tables
+ bounded technical address/state anchors only where heterogeneous addressing requires them
+ separate integration/projection/technical namespaces
```

The design deliberately rejects:

```text
one universal Entity table
one universal Relationship table
canonical EAV/property bag
universal event log as ontology
JSONB as required semantic escape hatch
PostgreSQL inheritance as ontology
```

Technical shared structures exist only to solve physical addressability, concurrency or indexing. They do not own Domain meaning.

## 2. Conceptual namespace layout

A candidate deployment may organize physical objects approximately as:

```text
core         canonical semantic owners/current material bindings
history      material historical state and bounded provenance
integration  provider/external mappings and sync/apply state
projection   rebuildable LR-08 read/search/materialized projections
technical    address anchors, idempotency and invariant-control machinery
```

These namespaces are operational organization only. They are not semantic state layers by identity and do not authorize moving meaning between layers.

## 3. LR representation strategy

### LR-01 native identity owners

Each of the 15 accepted native owners receives its own canonical table/family:

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

There is no required common semantic parent row. Stable native identity is owned by the concrete owner table.

Shared technical columns such as creation metadata or mapping revision may be reused by convention/library, not by semantic inheritance.

### LR-02 dependent/material contextual records

Use owner-specific contextual tables when independent scoped addressability/history is justified, for example material Schedule, Actual, Agreement, consequential Consent, material Evaluation, material Resource Requirement or qualified relation state.

A trivial low-consequence interaction remains embedded/derived when the Logical Model allows selective materialization.

### LR-03 specific relations

Use specific association tables per relation family. Simple binary relations can be compact join tables. Consequential or independently addressable relations use qualified contextual records with their own scoped identity/material state.

There is no canonical table of:

```text
from_ref, relation_type, to_ref, json_payload
```

as a universal semantic fallback.

### LR-04 values

Quantity, Monetary Amount and other typed value semantics use owner-bound typed columns/composites/dependent tables as needed. Shared scalar infrastructure is allowed, but semantic families remain distinct.

### LR-05 rules/specifications

Recurrence, Criterion, Temporal Constraint, Conditional Policy, Availability rules and Resource Requirements use owner-specific structured relational representations. Reusable predicate/expression machinery may exist technically, but no universal canonical `Rule(type,payload)` root is introduced.

### LR-06 realization/results

Actual and Outcome remain their accepted contextual semantic families, not generic status rows.

### LR-07 history/provenance

History is implemented through explicit material-state records plus typed lineage/provenance where material, not through one mandatory global event table.

### LR-08 projections

Views, materialized views or cache/read-model tables are rebuildable and explicitly carry source/material basis where consequence needs it.

### LR-09 provider/external

Provider identifiers, revisions, payloads and synchronization/apply state live in integration-specific structures and never define native identity automatically.

### LR-10..LR-13

Flexible low-consequence metadata may use bounded JSONB only where the accepted Logical Model permits flexibility. Unresolved/candidate, product profile and specialist-extension data stay explicitly classified and cannot leak into the canonical kernel as generic payload storage.

## 4. NativeRef mapping

PostgreSQL cannot enforce one heterogeneous FK over unrelated owner tables without introducing a technical common target. Use a hybrid.

### Homogeneous Reference Contract

When a slot accepts one concrete native owner family, use a direct FK to that owner table.

Examples:

```text
Occurrence -> Routine source where the specific contract requires it
Observation -> Person subject where a bounded contract says exactly Person
```

Exact owner contracts remain authoritative; these are illustrative only.

### Heterogeneous Reference Contract

Use a bounded technical `native_address_anchor` concept containing only address-control metadata such as:

```text
native_ref_id
owner_family discriminator
owner-row existence binding
lifecycle/tombstone control metadata where required
```

Every LR-01 row that must participate in heterogeneous addressability is bound one-to-one to its anchor.

Rules:

```text
anchor != Entity
anchor != semantic superclass
anchor has no generic domain properties/lifecycle
Reference Contract still limits eligible owner families
```

A heterogeneous reference stores the anchor identity plus enough contracted type information to validate eligibility. Application/database constraints/triggers used later must reject an anchor whose owner family is outside the specific Reference Contract.

Direct FKs remain preferred where the contract is homogeneous; do not route every relationship through the anchor merely for uniformity.

## 5. ScopedRecordRef mapping

Addressable LR-02 records use stable scoped IDs owned by their concrete contextual tables.

For heterogeneous slots that genuinely address multiple LR-02 families, a separate bounded `scoped_address_anchor` may be used. Do not merge scoped/native/material/external addressing into one universal `kind,id` table.

Scope ownership and target eligibility remain explicit in the containing Reference Contract.

## 6. MaterialStateRef mapping

Material semantic state receives a stable explicit address independent of PostgreSQL MVCC/storage tokens.

Conceptual pattern:

```text
material_state_anchor
  material_state_ref
  semantic owner address
  facet/purpose discriminator
  mapping revision
  material chronology metadata

owner-specific material-state row
  material_state_ref
  owner identity
  semantic state fields
  effective/world chronology where applicable
  recorded/knowledge chronology where applicable
  provenance/reconciliation links where applicable
```

The current accepted state of an owner/facet is represented by an explicit binding/pointer or current-state relation, not by “highest revision number” as semantic truth.

Forbidden identities:

```text
xmin/xid       != MaterialStateRef
updated_at     != MaterialStateRef
row hash       != MaterialStateRef
ETag           != MaterialStateRef
```

Those values may assist concurrency or diagnostics later.

## 7. ExternalRef / provider state

Represent provider addresses with explicit issuer scope:

```text
provider/source
realm / tenant / account / integration instance where required
provider object type where required
opaque external identifier
provider revision/version where material
```

A separate mapping connects ExternalRef to current reconciliation candidates/accepted native or scoped targets.

Keep separately:

```text
provider payload/state
provider apply/sync state
provider revision
canonical LifeOS state
reconciliation record/status
```

Provider success/failure never silently rewrites canonical state.

## 8. Current state and material history

Use direct current-state access plus retained material states.

Baseline pattern:

```text
stable owner row
+ current accepted material-state binding where required
+ append-retained/immutable-by-policy material-state rows
+ typed correction/replacement/reconciliation lineage
```

Not every mutable low-consequence field requires a full material-state record. Escalation follows the accepted consequence/history threshold.

Historical queries must not infer past state from today’s mutable row.

### Effective/world vs knowledge chronology

Where material, preserve separate ranges/instants for:

```text
when the represented state applied in the world
when LifeOS recorded/learned/accepted/corrected it
```

PostgreSQL range/date/time types may encode those axes where appropriate, but no universal bitemporal Fact schema is required.

## 9. Typed relation mapping

### Simple direct relation

A specific binary LR-03 family may use a dedicated association table with concrete FK endpoints and relation-specific fields.

### Qualified material relation

When history, governance, scope, visibility, provenance or state binding matters, use a contextual relation record with:

```text
ScopedRecordRef where addressability is required
specific endpoint roles
Reference Contract-valid targets
material-state history where required
scope/purpose/context
provenance
governance/disclosure basis
```

### Agreement

Material Agreement uses one contextual Agreement record plus explicit party-assent bindings.

```text
Agreement
-> exactly one justified terms MaterialStateRef per applicable accepted terms state
-> N party-role assent records bound to that same terms state
```

An amendment produces a new material terms binding/Agreement state; prior assent is not silently inherited.

### Consent / Authority / Visibility / Representation

Use separate owner-specific qualified relation/state structures. No generic permission/ACL row becomes canonical governance truth.

## 10. Temporal representation

Do not normalize every semantic time to UTC only.

Preserve dedicated structures/columns for applicable:

```text
date-only
floating local date + wall-clock time
named-zone wall-clock + IANA zone identifier
accepted historical resolution basis (offset/instant where consequence requires)
absolute instant
interval/range
duration
precision/granularity/frame
```

Future named-zone recurrence remains based on applicable named-zone rules rather than freezing future occurrences to a historical offset.

## 11. Recurrence

Use explicit owner-specific Recurrence representation with a required recurrence-family discriminator and family-specific structured parameters.

At minimum preserve families:

```text
calendar / wall-clock
elapsed interval
quota per period
completion-relative
anchor-stream-relative
cyclic positional
```

Do not make an RFC/calendar library’s recurrence format the canonical kernel if it cannot represent the accepted families losslessly.

## 12. Lazy Occurrence identity

Before individual persistent differentiation, identify a derivable candidate through a bounded locator:

```text
governing source ReferenceAddress
governing MaterialStateRef
recurrence family
semantic coordinate when that family provides one
```

Once the Occurrence becomes independently differentiated/addressable, create the concrete `Occurrence` LR-01 row and NativeRef while retaining locator/source lineage.

Do not invent ordinal identities for unordered equivalent quota slots merely because a primary key would be convenient.

## 13. Schedule / Session / Actual / Outcome

Keep separate physical owners:

```text
Occurrence   stable expected-instance identity
Schedule     dependent accepted placement
Session      stable execution-episode identity
Actual       contextual realization record
Outcome      contextual result/disposition where material
```

Actual does not overwrite Schedule. Absence of Actual remains unknown unless an owner-specific negative semantic state exists.

## 14. Expected-state consequential concurrency

Every consequential mutation that can corrupt meaning under stale state carries an expected `MaterialStateRef` or equivalent semantic precondition.

Conceptual transaction:

```text
1. locate current semantic owner/facet
2. verify current material_state_ref == expected_material_state_ref
3. lock/serialize required invariant rows
4. establish new material state / relation state
5. update current binding atomically
6. write bounded provenance/idempotency metadata where applicable
7. commit
```

A mismatch returns conflict/re-read/reconcile rather than silent last-write-wins.

PostgreSQL row locks, conditional updates and `SERIALIZABLE` isolation may implement the physical check later; they do not become semantic state identity.

## 15. Multi-owner consistency

Co-located invariants use one PostgreSQL transaction.

Use the narrowest mechanism that truthfully enforces the invariant:

```text
ordinary FK/UNIQUE/CHECK for local structural constraints
DEFERRABLE constraints for transaction-end cross-row validity where applicable
exclusion/range constraints for applicable interval conflicts
row/key locking for explicit write coordination
SERIALIZABLE for predicate/write-skew-sensitive consequential operations
```

Do not claim provider/global atomicity. When an external side effect cannot share the database transaction, canonical state must expose staged/pending/partial/reconciliation state per WL-H07/WL-H08. Outbox/runtime implementation is later scope.

## 16. Idempotency

Use bounded technical idempotency records keyed by operation scope + idempotency key + material operation fingerprint.

```text
same key + materially same operation -> prior effect/result may replay
same key + materially different operation -> reject/conflict
```

Idempotency record/key is not a NativeRef, Request ID or Decision ID.

## 17. Derived/projection state

Use normal views for cheap derivations and materialized/cache tables only when justified.

Any materialized consequential projection carries/reconstructs:

```text
projection kind
bounded source set
source MaterialStateRefs/material basis
created/refreshed timestamp
freshness/expiry
purpose/context where material
```

Candidate Set, Effective Availability, Effective Authority/Visibility and current knowledge remain LR-08 by default.

## 18. Search / JSONB boundary

PostgreSQL full-text/JSONB capabilities may support bounded flexible and search needs, but:

```text
required semantic relationship != JSONB property
required material state != JSONB blob by convenience
provider/raw payload may use JSONB
LR-10 low-consequence metadata may use JSONB
specialist extension may use bounded JSONB when justified
```

No canonical generic property bag.

## 19. Selective disclosure

Canonical storage remains shared reality. Recipient-specific exposure is enforced through bounded query/policy/projection mechanisms; do not duplicate canonical records per recipient.

Potential later mechanisms include application predicates, RLS and dedicated authorization projections. PM-02 selects none.

PM-03 must pressure:

```text
hidden row existence through FK/errors
counts/aggregates
ranking
relation existence
source/projection leakage
RLS/application-policy mismatches
```

## 20. Retention / redaction / tombstones

When policy permits continuity but requires payload deletion:

```text
retain minimal stable native/scoped/material address/tombstone
remove/redact protected payload/history fields as required
retain only permitted lineage/minimal chronology
mark redacted/unavailable explicitly enough to avoid “never existed” fiction
```

NativeRef is never reused.

An old backup restore must later be tested for anti-resurrection of data whose current retention policy forbids restoration.

## 21. Governed-effect provenance

Consequential effects must be able to retain/reconstruct bounded technical provenance including applicable:

```text
operation family
target semantic owner/facet
expected MaterialStateRef
actual Actor
represented party
Principal/security context reference
Authority/Consent/Visibility/Agreement basis MaterialStateRefs
purpose/context
idempotency key
correlation/causation
new material state/effect
provider/runtime outcome separately
```

This is a technical provenance record/profile, not a universal Domain Operation/Command owner.

## 22. Query strategy

Current-state queries should normally hit owner/current-state structures directly without lifetime replay.

Use:

```text
direct FK joins for homogeneous relations
address-anchor joins only for genuinely heterogeneous references
owner-specific material-state tables for history
range/time indexes for temporal pressure
recursive CTEs for bounded traversal where appropriate
projection tables for expensive derived reads when justified
```

Mapping complexity, join count and anchor fan-out become PM-03/06 evidence; they are not hidden.

## 23. Schema evolution

Every canonical object/state family carries a mapping/schema revision contract at the migration/evidence level.

Evolution policy:

1. additive/backward-readable change where practical;
2. create new semantic state shape without reinterpreting old rows;
3. migrate/backfill with explicit provenance/checkpoint;
4. verify NativeRef/ScopedRecordRef/MaterialStateRef continuity;
5. verify historical temporal/governance meaning;
6. verify tombstone/redaction semantics;
7. remove obsolete structures only after read/write cutover evidence.

ORM autogeneration or implicit schema synchronization never substitutes for reviewed migration semantics.

## 24. Candidate-native strengths deliberately used

This mapping intentionally uses PostgreSQL strengths where they materially help:

```text
mature relational constraints/FKs
transactions and serializable isolation
range/exclusion semantics
rich SQL/reporting/CTEs
JSONB only for bounded flexible/provider payloads
well-developed backup/restore ecosystem (tested later, not assumed PASS)
```

Candidate-native use is not a requirement that the other mappings mimic these mechanisms.

## 25. PM-03 proof obligations / known risks

### PG-R01 — technical anchor leakage

Prove `native_address_anchor`/other anchors remain address infrastructure and cannot become generic Entity/Thing/property containers.

### PG-R02 — heterogeneous reference integrity

Prove each Reference Contract rejects ineligible anchor owner families and dangling owner bindings.

### PG-R03 — history maintainability

Prove owner-specific material-state structures remain coherent across representative LR-01/LR-02/LR-03 families without an unmanageable universal-state escape hatch.

### PG-R04 — expected-state concurrency

Prove stale consequential mutations conflict and no silent overwrite survives under concurrency.

### PG-R05 — multi-owner write skew

Prove representative invariant-spanning changes survive concurrent execution with the selected lock/serializable strategy.

### PG-R06 — Agreement/governance materiality

Prove n-ary common terms state and consequential Consent/Authority/Visibility bindings remain reconstructible after amendment/revocation.

### PG-R07 — temporal/history semantics

Prove world/effective and knowledge chronology can be queried without making all tables universal bitemporal records or requiring lifetime replay.

### PG-R08 — lazy Occurrence

Prove derivable locator -> persisted NativeRef transition preserves semantic identity and unordered quota slots are not given fake early identity.

### PG-R09 — selective disclosure/non-interference

Prove row-level/query-level enforcement does not leak hidden relations/source state through counts, errors, ranking or timing-sensitive paths.

### PG-R10 — retention/restore

Prove redaction/tombstone integrity and anti-resurrection after restore.

## 26. PM-02 result

```text
MAPPING ID
PM02-PG-001

SUBJECT
PostgreSQL 18.4 / self-hosted single-node qualification topology / psycopg 3.3.4

DESIGN
COMPLETE

HG-01..HG-12
NOT RUN

BENCHMARK
NOT STARTED

CURRENT DISPOSITION
ADMITTED / PRE-EXISTING PREFERRED BASELINE / NOT SELECTED
```

No performance, hard-gate PASS or selection claim is made by this mapping.