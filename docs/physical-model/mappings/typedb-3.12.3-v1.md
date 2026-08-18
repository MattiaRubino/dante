# TypeDB CE 3.12.3 Physical Mapping v1

- Mapping ID: `PM02-TDB-001`
- Candidate: TypeDB CE
- Exact PM-01 subject: TypeDB CE **3.12.3**, self-hosted single-node qualification topology; official driver **3.12.3**
- Status: **PM-02 DESIGN COMPLETE / PM-03 NOT RUN**
- Selection: **NOT SELECTED**
- Purpose: idiomatic TypeDB mapping of the closed LifeOS Logical Model; no executable TypeQL/schema deployment is authorized by this document.

## 1. Design thesis

Use TypeDB's typed entity/relation/role system to encode LifeOS semantic specificity directly while refusing a generic object graph.

```text
concrete owner entity types
+ concrete relation types with named roles
+ relation-profiled role eligibility
+ explicit owner-specific material-state types
+ separate external/provider types
+ bounded technical consistency guards where snapshot isolation needs additional coordination
```

Reject:

```text
universal `entity`/`thing` semantic root used as LifeOS ontology
universal Relationship/Edge relation
one generic `ref` relation that accepts everything
TypeDB IID as LifeOS identity
one universal Version/Fact entity
relation type strings/payloads as semantic escape hatch
```

TypeDB's own type hierarchy is implementation/schema structure. Any shared supertype/interface introduced later must be strictly capability-oriented and must not imply a new Domain semantic superclass.

## 2. LR-01 native owner mapping

Create a concrete entity type for each of the 15 LR-01 owners:

```text
person
living-referent
asset
place
content-artifact
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

Each concrete owner owns an explicit stable LifeOS `native-id` key attribute.

Rules:

```text
native-id == NativeRef payload for that concrete owner family
TypeDB internal IID != NativeRef
shared key attribute definition != shared semantic owner
```

A technical schema interface may express “has native-id” or “eligible for a bounded role” if useful, but there is no canonical generic Entity record carrying arbitrary semantic properties.

## 3. LR-02 contextual/material records

Represent material/addressable contextual records as concrete entity or relation types according to their semantics.

Examples of entity-like contextual records may include:

```text
schedule
actual
material-evaluation
material-resource-requirement
proposal/request/decision when independently materialized
agreement context when modeled as contextual object
```

Every independently addressable LR-02 representation owns a `scoped-record-id` key.

When the semantic structure is naturally relation-first, TypeDB relation types may carry the scoped key and attributes directly rather than manufacturing a wrapper entity.

The choice is per semantic family, not one rule that all LR-02 become entities or all become relations.

## 4. LR-03 relation mapping

Use concrete TypeDB relation types with named roles and cardinality constraints.

Examples of relation families:

```text
membership(member, collective)
ownership(owner, owned)
possession(holder, possessed)
participation(participant, context)
responsibility(responsible-party, responsibility-context)
dependency(dependent, prerequisite/condition-target)
representation(actor, represented-party, context)
resource-allocation(requirement/consumer, resource-provider, context)
```

Exact role sets follow the Logical Reference Contract for each family.

Do not create:

```text
relationship(from, type, to)
```

as a generic semantic fallback.

## 5. Reference Contracts through role eligibility

TypeDB's strongest fit for LifeOS is that endpoint eligibility can be expressed at the schema/role level rather than primarily through application-side kind switches.

For each heterogeneous Reference Contract:

1. define the semantic relation/record role;
2. allow only the concrete owner/context/state types that are valid to play it;
3. preserve endpoint role meaning separately from the target's type;
4. use explicit typed keys for application-visible addresses.

A role such as `subject` or `resource-provider` remains contextual capability; it does not create a Subject/Resource native identity.

No generic `ReferenceAddress` object is required merely to point to multiple TypeDB types. The logical address family is reconstructed from:

```text
target concrete type
+ target key family (`native-id`, `scoped-record-id`, `material-state-id`, external key)
+ containing semantic role/Reference Contract
```

## 6. NativeRef mapping

`NativeRef` is represented by:

```text
concrete LR-01 type
+ native-id key
```

A heterogeneous query may match the specific role and return multiple eligible concrete types, but the returned reference is still discriminated by owner family.

TypeDB internal IDs are opaque implementation handles and are never exposed as semantic NativeRef identity.

## 7. ScopedRecordRef mapping

Addressable LR-02 entity/relation types own explicit `scoped-record-id` keys.

Scope is part of the semantic record's relation/context, not merely a globally unique opaque identifier. If an LR-02 record is only meaningful under an owning context, the mapping includes the owning relation/context as a required role/attribute constraint.

No universal RelationRef is introduced.

## 8. MaterialStateRef mapping

Use explicit owner/facet-specific material-state types rather than TypeDB transaction identity or mutable attributes on the owner alone.

Conceptual family:

```text
<owner>-material-state
  material-state-id @key
  recorded chronology attributes
  effective/world chronology where applicable
  state payload/typed relations

state-of-<owner>(state, owner)
current-state-of-<owner>(owner, state)
```

A shared technical capability interface for `material-state-id` is permitted, but no universal native Version/Fact owner is created.

For bounded heterogeneous state-reference slots, role eligibility may target the allowed state types.

Forbidden identities:

```text
TypeDB IID            != MaterialStateRef
transaction snapshot  != MaterialStateRef
latest matching state != MaterialStateRef by definition
```

The explicit `material-state-id` is the semantic state address.

## 9. Owner current state

Keep stable owner identity separate from materially mutable state where consequence/history requires.

A `current-state-of-*` binding marks the accepted current material state for a specific facet. It is updated in the same transaction as establishment of the replacement state.

Do not infer currentness from maximum timestamp or latest insertion alone.

Low-consequence metadata that does not justify material state may remain direct typed attributes under LR-10 policy.

## 10. History / correction / knowledge chronology

TypeDB does not become a universal event ledger. Historical material states remain explicit objects/relations.

Where material, each state preserves:

```text
world/effective interval or applicability semantics
recorded/learned/accepted chronology
correction/supersession relation
Provenance / Reconciliation linkage
```

Typed relations such as:

```text
supersedes(previous-state, new-state)
corrects(previous-state, corrected-state)
derived-from(source-state, result-state)
```

are only created where that specific lineage meaning applies. No universal related-to edge.

## 11. LR-04 value semantics

Use typed attributes for simple scalar/value semantics and bounded dependent value structures for composite values.

Quantity and Monetary Amount remain semantically distinct even if both use decimal attributes.

A composite value such as amount + currency or quantity + unit may be modeled through:

```text
owner-specific attributes when compact and semantically sufficient
or
anonymous/dependent value object/relation when multiple fields/constraints require structure
```

Do not assign a LifeOS public stable identity merely because TypeDB internally represents an object.

## 12. LR-05 rule/specification mapping

Criterion, Recurrence, Temporal Constraint, Conditional Policy, Availability rules and Resource Requirement remain distinct schema types.

Shared predicate/expression attributes/relations may be reused technically only if the owning type remains explicit.

Forbidden canonical shortcut:

```text
rule(type, json-payload)
```

for required semantics.

## 13. Agreement — native n-ary strength

TypeDB can model Agreement as a first-class n-ary relation/context without pairwise collapse.

Conceptual shape:

```text
agreement
  roles:
    party
    terms-state
    agreement-context/owner as required
  owns:
    scoped-record-id where addressable
    agreement-specific attributes
```

For every material assent state:

```text
all participating assent bindings
-> same justified terms MaterialStateRef/state object
```

If amendments occur, preserve prior agreement/assent state and establish a new material binding. Do not mutate the terms pointer and pretend old assent applied to the new terms.

Where individual party assent lifecycle itself requires history, materialize typed assent relation/state rather than flattening into a boolean relation attribute.

## 14. Consent / Authority / Visibility / Representation

Use separate concrete relation/context families.

### Consent

Consequential Consent must retain:

```text
giver
recipient/use/action/exposure role
target
purpose/context
time/applicability
target/terms material state
withdrawal/revocation history
```

### Authority

Explicit Authority may be a typed relation/material state. Effective Authority may be derived via TypeQL queries/functions over policy and relation state.

### Visibility

Visibility may target endpoint, relation/context, projection or source/evidence independently. Do not reduce to a whole-object ACL relation.

### Representation

Preserve actual Actor, represented party and legitimacy/Authority basis separately.

No technical allow/deny relation is canonical Domain Authority.

## 15. ExternalRef / provider state

Create explicit provider/external entity types or scoped records with a key derived from the provider's actual uniqueness scope, for example:

```text
provider/source
integration instance / tenant / account scope where required
provider object kind
opaque external ID
```

Provider revision/payload/apply status and reconciliation remain separate attributes/relations.

External object types do not play LR-01 owner roles merely because they map to a native LifeOS owner.

## 16. Temporal values

Preserve typed semantic temporal forms instead of one UTC instant attribute.

Candidate mapping uses distinct value structures/types for applicable:

```text
date-only
floating local wall-clock
named-zone wall-clock + zone ID
accepted historical resolution basis
absolute instant
interval/range
duration
precision/granularity/frame
```

TypeDB attribute primitives may store components, but the containing semantic type/roles preserve interpretation.

## 17. Recurrence

Create distinct typed Recurrence specification families or a typed recurrence hierarchy whose subtypes remain semantically explicit:

```text
calendar-recurrence
elapsed-interval-recurrence
quota-period-recurrence
completion-relative-recurrence
anchor-stream-recurrence
cyclic-positional-recurrence
```

Shared technical attributes do not erase subtype/family semantics.

## 18. Lazy Occurrence

Before persistent differentiation, the bounded occurrence locator remains an application/logical derivation tuple:

```text
governing source ReferenceAddress
governing material-state-id
recurrence family
semantic coordinate where one exists
```

Do not create placeholder `occurrence` entities for every future expansion merely to obtain an IID/key.

When an individual Occurrence becomes semantically distinguished/addressable, create the concrete `occurrence` entity with `native-id` and retain relation to the governing source/material state/locator basis.

Unordered equivalent quota slots remain unnumbered until differentiated.

## 19. Schedule / Session / Actual / Outcome

Keep separate types:

```text
occurrence entity
schedule contextual record/relation
session entity
actual contextual entity/relation
outcome contextual result structure
```

Actual is LR-02 + LR-06 and owns a scoped record key when material. It is not promoted to native entity identity.

No Actual record remains unknown, not false/non-realization.

## 20. Expected-state consequential concurrency

For a consequential mutation:

```text
1. match owner + exact current material-state-id
2. require that it equals expected MaterialStateRef
3. create replacement material state / relation state
4. replace current-state binding
5. update all required affected owners/relations
6. update technical consistency guard when the invariant boundary requires it
7. commit one write transaction
```

If the expected state does not match, the mutation matches nothing/returns conflict and must not silently apply against a newer state.

Snapshot isolation is not assumed to prevent all predicate/write-skew anomalies across disjoint objects.

## 21. Technical consistency guard

For invariant sets where two concurrent transactions could each read compatible snapshots and update disjoint semantic objects while jointly violating an invariant, introduce a **narrow technical** guard.

Conceptual type:

```text
consistency-guard
  guard-id @key
  guard-revision / nonce
```

Every consequential operation sharing that invariant boundary must mutate the same guard in the transaction.

Examples may include a bounded shared allocation/capacity boundary or another explicitly identified multi-owner invariant.

Rules:

```text
consistency-guard != Domain Transaction
consistency-guard != semantic owner
one guard is not global to all LifeOS writes
scope is the narrowest invariant boundary
```

PM-03 must directly prove that this pattern closes the relevant snapshot-isolation write-skew cases under the actual TypeDB subject.

## 22. Multi-owner consistency

One TypeDB write transaction carries all co-located semantic changes.

Use:

```text
schema cardinality/uniqueness constraints for local structural invariants
exact current-state matching for stale-write prevention
shared technical guard mutation for predicate/write-skew-sensitive multi-owner invariants
```

External/provider effects remain staged/reconciled when they cannot share atomicity.

## 23. Idempotency

Use bounded technical idempotency entity/records keyed by operation scope + supplied idempotency key + material operation fingerprint.

Do not create a universal semantic Command entity.

## 24. Derived/projection state

Prefer TypeQL queries/functions for derived state when query cost is acceptable.

Materialize projection entities only where required for performance/reproducibility and retain:

```text
projection kind
source state references/material basis
freshness/refreshed time
purpose/context where consequential
```

Effective Authority/Visibility, Candidate Set, knowledge view and Effective Availability/Capacity remain derived by default.

## 25. Selective disclosure

The canonical schema remains shared. Recipient-context projections are query/enforcement outputs, not duplicate owner entities per user.

TypeDB query role/type richness does not by itself guarantee non-interference. PM-03/later security work must pressure:

```text
hidden relation existence
counts
role traversal
inference via type/cardinality knowledge
candidate ranking/explanations
error behavior
```

No AuthZ vendor is selected by this mapping.

## 26. Retention / redaction / tombstones

When payload deletion is required but reference continuity is legally/permissibly retained:

```text
keep owner key + minimal tombstone classification
remove/redact sensitive attributes/relations/history according to policy
preserve only allowed lineage/material-state continuity
never reuse native-id
```

If a material-state payload must disappear while the fact that a state existed remains important/permitted, retain a minimal state key/tombstone object rather than rewriting history as if the state never existed.

PM-03/07 must verify TypeDB deletion behavior and practical reconstruction.

## 27. Governed-effect provenance

Consequential effects use bounded technical/domain-owned provenance relationships sufficient to reconstruct applicable:

```text
actual Actor
represented party
Principal/security context reference
governance basis state IDs
semantic target/facet
expected material-state-id
purpose/context
idempotency/correlation metadata
resulting material state/effect
provider/runtime result separately
```

No universal Operation/Command semantic root.

## 28. Query strategy

Candidate-native query strengths deliberately used:

```text
typed relation traversal through named roles
n-ary relation queries
schema-constrained eligible player types
functions/queries for derived relation-heavy views
owner/material-state joins expressed through semantic relations
```

Do not introduce generic relationship tables merely for SQL-style familiarity.

Current-state queries follow `current-state-of-*` bindings; historical queries traverse material-state/lineage relations. No lifetime event replay is required.

## 29. Schema evolution

TypeDB schema evolution must keep owner typing explicit.

Process:

1. version the LifeOS mapping;
2. add/modify concrete owner/relation/state types under a reviewed migration;
3. migrate data in controlled transactions;
4. preserve `native-id`, `scoped-record-id`, `material-state-id` continuity;
5. verify role/cardinality changes against existing data/history;
6. preserve old state semantics rather than reinterpreting old objects through a new type meaning;
7. remove obsolete structures only after migration/rollback evidence.

A new common supertype is permitted only when it represents a proven technical capability, not to save schema lines.

## 30. Candidate-native strengths deliberately used

```text
first-class relation types and named roles
n-ary relation representation
schema role/cardinality/key constraints
typed polymorphism through role eligibility
relation instances that can themselves carry attributes/play roles
rich relation-centric query language
```

These are tested as potential semantic-mapping simplifiers, not assumed performance/operability wins.

## 31. PM-03 proof obligations / known risks

### TDB-R01 — no generic root leakage

Prove shared supertypes/interfaces remain technical capabilities and no semantic operation falls back to generic entity/relation/payload conventions.

### TDB-R02 — ReferenceAddress reverse mapping

Prove an independent reader can deterministically recover NativeRef vs ScopedRecordRef vs MaterialStateRef vs ExternalRef from type + key + role contract.

### TDB-R03 — material-state ergonomics

Prove explicit state object/relation design remains practical across representative owner/relation families and does not force accidental “everything is a state entity” modeling.

### TDB-R04 — snapshot-isolation stale/write-skew protection

Prove exact-state matching and consistency-guard mutation reject concurrent consequential anomalies required by WL-H05/WL-H07.

### TDB-R05 — n-ary Agreement/common terms

Prove party assent, common material terms state and amendment history remain explicit and queryable.

### TDB-R06 — temporal/history separation

Prove world/effective and knowledge chronology remain queryable without conflating database transaction history with semantic history.

### TDB-R07 — lazy Occurrence

Prove pre-materialization locator and later `occurrence` entity preserve one semantic identity.

### TDB-R08 — unknown/negative state

Prove missing relation/state is never globally interpreted as false and explicit negative states remain owner-specific.

### TDB-R09 — retention/tombstone

Prove payload deletion and retained minimal historical continuity are achievable for representative sensitive state without key reuse.

### TDB-R10 — selective disclosure/inference

Prove role traversal, counts, existence and derived query behavior can respect WL-H12 under later enforcement architecture.

### TDB-R11 — mapping/schema evolution

Prove a representative V1->V2 type/relation migration retains addresses and historical meaning.

## 32. PM-02 result

```text
MAPPING ID
PM02-TDB-001

SUBJECT
TypeDB CE 3.12.3 / self-hosted single-node qualification topology / driver 3.12.3

DESIGN
COMPLETE

HG-01..HG-12
NOT RUN

BENCHMARK
NOT STARTED

CURRENT DISPOSITION
ADMITTED / NOT SELECTED
```

No hard-gate PASS, performance superiority or selection is claimed.