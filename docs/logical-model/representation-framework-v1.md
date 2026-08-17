# LifeOS Logical Representation Framework v1

**Status:** Stage-0H hardened normative foundation + Slice-A + Slice-B + integrated A+B contract  
**Date:** 2026-08-17  
**Purpose:** provide a controlled vocabulary for classifying logical representation choices without equating representation shape with domain ontology

---

## 1. Core rule

The Logical Model answers:

> How is accepted LifeOS meaning represented, referenced, queried, historized and reconciled?

It does not re-answer:

> What semantic realities exist?

The Domain Atlas already owns that question.

Therefore:

```text
one Domain concept != necessarily one logical record/table
one logical mechanism != necessarily one Domain superclass
one UI object != necessarily one Domain owner
one provider object != necessarily one LifeOS object
```

---

## 2. Logical disposition vocabulary

Every accepted Domain Atlas owner in a slice must receive one or more explicit logical dispositions from the following vocabulary.

These are **representation roles**, not new ontology classes.

### LR-01 — Native identity-bearing logical record

Use when a semantic owner requires stable independent identity/history/reference across contexts.

Candidate examples to test, not pre-approved mappings:

```text
Person
Living Referent
Asset
Goal
Possibility
Content Artifact
```

The decision must be proven slice-by-slice.

### LR-02 — Dependent semantic record

Use when materially distinct semantic state must persist but its identity/lifecycle is naturally scoped to another owner/context.

It may still require stable reference or history.

### LR-03 — Typed association / relation record

Use for accepted semantics whose primary role relates actors/referents/context while retaining their own scope, validity, provenance or history.

Potential pressure includes:

```text
Responsibility
Participation
Authority
Visibility
Membership
Ownership
Possession
Dependency
Resource Allocation
```

A shared technical association mechanism is allowed only if the specific semantic type remains explicit and enforceable.

### LR-04 — Value semantics

Use when meaning is primarily carried by a value plus required qualifiers rather than independent referent identity.

Examples of pressure:

```text
Quantity
MonetaryAmount
```

Value semantics may still require source/history when embedded in a historical assertion.

### LR-05 — Rule / policy definition

Use when the accepted semantic primarily defines generation, constraint, conditional behavior or evaluation policy rather than one realized occurrence.

Potential pressure includes:

```text
Recurrence
Conditional Policy
Criterion
Temporal Constraint
```

Policy definition must remain distinct from generated/realized state.

### LR-06 — Material state / realization record

Use for materially relevant realized/current/historical state that must not be inferred only from intention or schedule.

Potential pressure includes:

```text
Actual
Outcome
Occurrence
Observation
```

This category does not imply a common lifecycle between those concepts.

### LR-07 — Version / correction / lineage record

Use for explicit history, version, reconciliation or provenance semantics where reconstruction requires addressable change/lineage.

Potential pressure includes:

```text
Version
Reconciliation
Provenance
Evidence linkage
```

Shared infrastructure may exist, but these meanings remain distinct.

### LR-08 — Derived projection / read model

Use when information can be deterministically/evaluatively derived from canonical inputs and does not itself require independent canonical truth under the Domain Atlas.

Examples may include:

```text
summaries
rollups
search projections
calculated availability views
progress views where derivable
```

Derived state must record sufficient derivation basis/version where stale or historical interpretation would matter.

### LR-09 — Provider identity / integration mapping

Use to map external objects/IDs/versions to LifeOS semantics without promoting provider identity to LifeOS identity.

Must support:

```text
provider
external ID
provider version/revision when applicable
mapping confidence/status
mapping history
source payload/provenance reference
reconciliation state where required
```

Exact fields remain slice/physical-stage decisions.

### LR-10 — Flexible descriptive / extension metadata

Use for genuinely flexible, low-consequence, provider-specific or extension detail that is not a missing required kernel semantic owner.

JSON-like representation may be appropriate later.

Forbidden use:

```text
required canonical semantic truth hidden because modeling it is inconvenient
```

### LR-11 — Unresolved / candidate interpretation

Use when imported/AI/user material cannot yet be safely established as canonical typed meaning.

The representation should retain enough source/provenance/uncertainty to revisit the interpretation without manufacturing a generic canonical Relation/property.

### LR-12 — Product / organizational profile

Use for application-level grouping/configuration whose operational identity is useful but does not become a new Domain Atlas native semantic merely because it has an ID/UI.

Examples historically classified this way include pressure such as:

```text
Life Area
Project / Program profiles
Inbox / review queue / template-like containers
```

### LR-13 — Specialist extension record

Use when a bounded domain genuinely owns richer semantics than the general LifeOS kernel.

Examples of pressure:

```text
financial Transaction
inventory Movement
clinical specialist records
regulated validity records
```

The extension may be strongly typed and persistent without becoming a universal kernel owner.

---

## 3. Identity classification questions

Before assigning native logical identity, answer:

1. Must this reality be referenced independently across multiple contexts?
2. Can its material history change independently from its nearest owner?
3. Does deduplication/matching matter independently?
4. Can provider/storage representation change while identity remains?
5. Would embedding destroy important history, authority, provenance or queryability?
6. Is the identity required by the Domain Atlas or only by product/implementation convenience?

A `YES` to convenience alone is insufficient.

---

## 4. Materialization rule

```text
semantic capability
!= mandatory standalone materialization
```

A logical owner may be represented compactly when:

- the simple case has no material independent history;
- no independent reference is required;
- no actor/provenance distinction is lost;
- later formalization can occur without rewriting meaning.

But compactness fails when it causes:

```text
identity collision
history loss
semantic ambiguity
visibility leakage
provider coupling
impossible reverse mapping
```

---

## 5. Canonical vs derived vs external state

Every slice must explicitly identify three layers where applicable:

```text
CANONICAL LIFEOS STATE
what LifeOS currently accepts/owns under the Domain Atlas

DERIVED / PROJECTION STATE
what is calculated, summarized, ranked, indexed or displayed from canonical inputs

EXTERNAL / SOURCE STATE
what providers/documents/devices/AI/user assertions supplied
```

These layers may reference one another but must not be silently interchangeable.

---

## 6. Current, effective and recorded time

Logical history design must evaluate at least:

```text
when something was effective/true/intended in the represented world
when LifeOS learned/recorded/accepted it
when it was corrected or superseded
```

This framework does **not** mandate one global bitemporal/event-sourced implementation.

It mandates that slices prove the temporal distinctions they materially require.

A universal temporal mechanism may be adopted only if it remains simpler and semantically correct across the owners that use it.

---

## 7. Relationship representation rule

A generic technical association infrastructure is acceptable only if all of the following remain recoverable:

```text
semantic family/type
source/target roles
scope/context
valid/effective history where material
actor attribution
Authority/Visibility implications if any
Provenance/Evidence where material
constraints/cardinality/directionality required by that family
```

A bare:

```text
from_id -> related_to -> to_id
```

is not canonical LifeOS meaning.

---

## 8. Reverse-mapping template

For every proposed logical structure document:

```text
LOGICAL REPRESENTATION
<record/mechanism/state shape>

DOMAIN OWNER(S)
<exact accepted semantics represented>

NOT REPRESENTED AS
<nearest concepts that must not collapse>

IDENTITY RULE
<what remains the same / what creates new identity>

HISTORY RULE
<what changes overwrite vs create historical state>

SOURCE RULE
<canonical vs provider/source relation>

MULTI-ACTOR RULE
<actor/visibility/authority implications>

DERIVED RULE
<what is calculated rather than canonical>

SPECIALIST RULE
<what remains outside general kernel>
```

If this template cannot be filled unambiguously, the candidate is not ready for PASS.

---

## 9. Candidate comparison template

Every material candidate comparison must use a common frame rather than free-form advocacy.

```text
CANDIDATE ID
representation summary

STRENGTHS
what it solves naturally

FAILURE PRESSURE
where it is most likely to collapse semantics/history/privacy/queryability

TRACE COVERAGE
which invariant/owner entries it satisfies

MUTATION RESULT
what breaks if key structure is removed/merged/genericized

COUNTERFACTUAL RESULT
which near-identical cases remain distinguishable

SIMPLE CASE
minimum ceremony required

WORST CASE
history/scale/provider/multi-actor behavior

EVOLUTION
likely migration/extension pressure

EXTERNAL EVIDENCE
principles/anti-patterns only

ASSUMPTIONS
registered dependencies

PHYSICAL FREEDOM
which SQL/API implementation choices remain open

VERDICT
SELECTED / REJECTED / BLOCKED / RETEST
```

At least one rejected candidate should normally be materially plausible; straw-man comparison does not satisfy the methodology.

---

## 10. Traceability and decision records

Every selected logical disposition must be connected to:

- `traceability-and-regression-ledger-v1.md` for Domain invariant -> logical representation -> query -> test -> verdict;
- `decision-and-assumption-register-v1.md` for accepted decisions, rejected alternatives, material assumptions, evidence freshness and physical deferrals.

A representation that cannot be traced or whose meaning depends on undocumented assumptions is not accepted merely because it can be implemented.

---

## 11. Slice deliverable template

Every logical slice should produce at least:

1. owner inventory;
2. mandatory semantic invariants;
3. traceability matrix + cumulative invariant delta;
4. high-value query/operation corpus;
5. candidate logical representations;
6. selected representation and rejected plausible alternatives;
7. decision + assumption register entries;
8. identity/reference rules;
9. lifecycle/state rules;
10. history/correction rules;
11. typed relationship rules;
12. provider/reconciliation rules;
13. derived/projection rules;
14. simple-case representation;
15. worst-case/scale representation;
16. specialist extension boundaries;
17. historical replay results;
18. fresh adversarial test results;
19. mutation/destructive test results;
20. counterfactual test results;
21. external benchmark findings;
22. Product Reality pressure where relevant;
23. reverse mapping;
24. cross-slice regression impact + replay;
25. open logical questions;
26. LM gate matrix;
27. exact deferred physical decisions;
28. remote Git QA when written.

No exact SQL schema is required or authorized by this template.

---

## 12. Reference architecture guardrails for Slice A

Slice A must prove a way for native identities and contextual roles to share technical references without introducing false semantic inheritance.

At minimum test:

```text
Person
Living Referent
Asset
Place
Content Artifact
Collective

Actor role
Subject role
Resource role

Account / Principal boundary
provider identity mapping
```

Hard guardrails:

```text
native referent identity may be shared technically
!= universal semantic Entity / Thing

Actor / Subject / Resource role reference
!= wrapper identity by default

Account / Principal / provider identity
!= Person or other native referent identity

specific typed role/relation
!= generic semantic edge
```

The framework does not preselect a registry, union/reference envelope, explicit-FK-only design or hybrid. Slice A must compare and falsify plausible alternatives.

---

## 13. Initial slice roadmap

### Slice A — Identity / Reference

Pressure owners/families:

```text
Person
Actor / Account boundary
Living Referent
Asset
Place
Content Artifact
Collective identity pressure
Subject / Resource role pressure
provider identity mapping
```

Primary objective:

> establish how LifeOS can share technical references without creating a universal semantic Thing/Entity.

### Slice B — Intention / Execution

```text
Possibility
Goal
Proposal
Decision
Plan
Activity
Event
Routine
Milestone
Request
Dependency pressure
```

### Slice C — Time / Reality

```text
Recurrence
Occurrence
Schedule
Session
Actual
Outcome
Temporal Constraint
Conditional Policy pressure
```

### Slice D — Evidence / Knowledge / History

```text
Observation
Evidence
Provenance
Version
Reconciliation
Confirmation
Verification
Criterion / Evaluation
Acknowledgement pressure
```

### Slice E — Resources / Values / Capacity

```text
Resource
Requirement
Allocation
Availability / Capacity
Quantity
MonetaryAmount
Asset/Resource boundary replay
```

### Slice F — Relationships / Multi-Actor / Governance

```text
Responsibility
Participation
Coordination Stewardship
Authority
Visibility
Agreement
Consent
Representation
Membership
Contribution
Ownership
Possession
Interpersonal Relationship
Collective
```

The roadmap may be subdivided for manageability, but accepted Domain Atlas ownership is not changed by slice grouping.

---

## 14. Accepted Slice-A identity/reference contract

This section is activated with `slices/identity-reference-v1.md` and its validation checkpoint after exact remote QA.

### 14.1 Layered separation

```text
native identity
!= NativeRef addressability
!= Reference Contract meaning
!= ExternalRef/provider identity
!= Account / Principal identity
!= Reconciliation state
!= Version/material state
!= disclosure/public handle
```

### 14.2 NativeRef

`NativeRef` is the logical address of an independently justified native Domain identity.

Requirements:

```text
owner/type deterministically recoverable
opaque identity key
key not reused for another native referent
no semantic Entity/Thing superclass implied
```

NativeRef is a representation mechanism, not a Domain owner.

### 14.3 Reference Contract

A heterogeneous reference is canonical only under a containing contract that preserves:

```text
semantic role/family
eligible target families
cardinality/directionality where required
unresolved-target behavior
history/materiality rules
specialist/extension boundary
```

A technically valid NativeRef can still be semantically invalid for a particular slot.

### 14.4 Role references

```text
Actor / Subject / Resource
!= wrapper identity
```

When the referenced target has native identity, the role/typed relation points to that native referent directly through the applicable contract.

Not every valid role target is required to possess NativeRef/native identity; bounded service/pool/supply/value/specialist representations remain allowed where truthful.

### 14.5 ExternalRef

Provider/source identity lives in a separate scoped reference space.

Logical scope may require:

```text
provider/source
realm/tenant/account/integration instance
provider object type
opaque external ID
provider revision/version where material
```

Exact scope is adapter/provider-contract specific.

```text
ExternalRef != NativeRef
```

### 14.6 Identity mapping/reconciliation

```text
ExternalRef -> Reconciliation/Mapping -> NativeRef
```

or native-native duplicate resolution is explicit logical state where material.

Required properties:

```text
unresolved mapping allowed
candidate != accepted equivalence
accepted equivalence != irreversible rewrite
merge/supersession preserves historical addressability
wrong merge/link can be corrected/revoked
current resolution does not rewrite what was historically known
```

### 14.7 Identity vs Version

```text
NativeRef
= which continuing referent

Version/material-state reference
= which consequential state of that referent
```

Exact Version mechanism remains Slice-D work.

### 14.8 Privacy/correlation

```text
internal identity equality
!= public correlation permission
!= Visibility
!= Authority
```

One native referent may be exposed through context-scoped handles later without duplicating canonical identity.

### 14.9 Physical freedom

The accepted logical contract deliberately leaves open:

```text
technical anchor/registry
owner-specific FKs
composite typed references
hybrid model
key generation/data type
public ID serialization
```

Physical design may choose any sound implementation that preserves the contract.

PostgreSQL inheritance or one global table is not assumed or required.

### 14.10 Canonical Slice-A references

- `slices/identity-reference-v1.md`
- `checkpoints/identity-reference-v1-validation.md`
- `benchmarks/identity-reference-v1.md`
- `traceability-and-regression-ledger-v1.md` TA-01..TA-17 / INV-041..060
- `decision-and-assumption-register-v1.md` DEC-A / ALT-A / ASM-A entries

Later slices must not silently weaken this contract. Changes affecting it are at least R2 and normally R3 regression impact.

---

## 15. Accepted Slice-B intention/execution contract

This section activates with `slices/intention-execution-v1.md` after exact Slice-B remote QA.

### 15.1 No universal work/intention root

```text
Possibility
Goal
Plan
Activity
Event
Routine
Milestone
Proposal
Request
Decision
Dependency
```

retain their accepted Domain ownership. Shared representation mechanisms do not create `WorkItem`, `Intent`, `WorkflowNode` or universal parent hierarchy semantics.

### 15.2 Owner dispositions

The integrated A+B checkpoint hardens the original Slice-B wording. Once a canonical owner exists as a persisted LifeOS semantic object, its Domain identity classification is not optional merely because a storage strategy could embed it.

```text
Possibility  -> LR-01 when it has become a retained canonical Possibility
Goal         -> LR-01
Plan         -> LR-01
Activity     -> LR-01 for canonical persisted Activity
Event        -> LR-01 for canonical persisted Event
Routine      -> LR-01
Milestone    -> normally LR-02 dependent semantic record
Proposal     -> LR-02 conditionally materialized
Request      -> LR-02 conditionally materialized
Decision     -> LR-02 conditionally materialized
Dependency   -> LR-03 typed association/relation
```

Transient suggestions/candidates do not become Possibility/Activity/Event merely because they resemble their content.

Persistent addressability of LR-02/LR-03 does not itself imply native Domain identity.

### 15.3 Layered separation

```text
semantic owner
!= material state/version
!= typed link / semantic act
!= occurrence/schedule/execution
!= Actual
!= Outcome
!= derived operational status
```

### 15.4 Selective semantic materialization

Proposal/Request/Decision require standalone persistent representation when independent lifecycle/reference/history matters, including:

```text
async review or response
multi-actor interaction
counter-proposal
withdrawal / expiry / supersession
material target-version binding
Authority / rationale / provenance
auditability
material consequence
```

A trivial synchronous interaction does not require synthetic semantic records merely to satisfy architectural ceremony.

However:

```text
no standalone semantic-act record
!= no lineage/provenance/history for consequential target change
```

Selective materialization must not become selective auditability.

### 15.5 Lifecycle rule

There is no universal canonical status enum.

Each owner preserves its own material lifecycle/disposition dimensions. Product/UI may derive compact status projections, but those projections are not universal canonical truth.

### 15.6 Possibility maturation

```text
Possibility P1
-> typed adoption/origin lineage
-> Goal G1

P1 != G1
```

Later adoption never retypes pre-adoption history and the lineage must not degrade to a generic `related_to` edge.

### 15.7 Plan revision/replacement

```text
ordinary operational revision
!= automatic new Plan identity

materially different execution strategy
may create linked replacement/continuation Plan
```

Where a distinct replacement Plan is justified, the predecessor/successor relation is typed lineage and does not imply `old Plan v2` automatically.

Exact material Version mechanics remain Slice D.

### 15.8 Proposal/Decision version binding

Where material content changes:

```text
approval / Decision over target V1
!= automatic approval of materially different target V2
```

Material-equivalence/applicability must remain reconstructible.

### 15.9 Decision/effect separation

```text
Decision
!= target mutation
```

A Decision may have zero/one/many effects; effective state remains owned by the affected concept. Previously authorized Conditional Policy may produce permitted effects without manufacturing a new Decision for each mutation.

### 15.10 Request / instruction / Authority boundary

The earlier shorthand that an explicit request can `authorize` the requested action is superseded.

Correct rule:

```text
explicit user instruction/request
may establish that Actor's bounded intent/instruction
and may remove redundant confirmation ceremony
```

but:

```text
Request != Authority
Request != Consent
requester != Authority holder automatically
```

A shared/governed effect still requires independently applicable Authority/Consent/policy semantics.

### 15.11 Dependency

```text
Dependency
= typed directional contingency
!= hierarchy
!= containment
!= pure temporal order
!= universal DAG edge
```

Where consequence depends on one facet/state/result/transition rather than the whole target, the logical endpoint must preserve:

```text
ReferenceAddress(target)
+
materially relevant facet/state/result/transition/condition
```

Current `blocked/satisfied/eligible` state is normally derived from the Dependency plus relevant prerequisite/target state.

No universal predicate/expression language is introduced by this requirement.

### 15.12 Routine/instance barrier

```text
Routine != Recurrence != Occurrence != Actual
```

A recurring owner must not be modeled as one mutable Activity whose date advances forever when occurrence/history distinctions matter.

### 15.13 Governed-by material state

Where consequence requires, later Occurrence/execution must be able to identify the material Plan/Routine/Policy state that governed it.

Slice C owns exact instance/execution representation; Slice D owns exact Version/history representation.

### 15.14 Canonical Slice-B references

- `slices/intention-execution-v1.md`
- `checkpoints/intention-execution-v1-validation.md`
- `benchmarks/intention-execution-v1.md`
- `checkpoints/integrated-a-b-v1-validation.md`
- `traceability-and-regression-ledger-v1.md` Slice-B + integrated entries
- `decision-and-assumption-register-v1.md` Slice-B + integrated entries

Later slices must replay applicable Slice-A, Slice-B and cumulative integrated invariants rather than silently superseding them.

---

## 16. Integrated reference-address hardening

The A+B checkpoint exposed a referenceability gap between native identities and persistently addressable non-native semantic records.

### 16.1 ReferenceAddress

LifeOS therefore uses a **discriminated logical address family**:

```text
ReferenceAddress
=
  NativeRef
  OR ScopedRecordRef
  OR MaterialStateRef
  OR ExternalRef
  OR another later explicitly accepted bounded address variant
```

`ReferenceAddress` is representation vocabulary only.

```text
ReferenceAddress != Entity
ReferenceAddress != Thing
ReferenceAddress != Object superclass
ReferenceAddress != Relationship
ReferenceAddress != lifecycle
```

### 16.2 NativeRef

```text
NativeRef
= address of independently justified native Domain identity
```

Examples include current accepted native owners when their semantics require stable independent identity.

### 16.3 ScopedRecordRef

```text
ScopedRecordRef
= stable logical address of a materialized semantic record whose identity/history is scoped/dependent rather than native-referent identity
```

Current pressure includes:

```text
Milestone
materialized Proposal
materialized Request
materialized Decision
qualified Dependency when relation history/addressability matters
```

`ScopedRecordRef` does not promote those semantics to native referent identity.

### 16.4 MaterialStateRef

```text
MaterialStateRef
= address of the materially relevant state/version of a target
```

It remains distinct from the target's own continuing address. Exact Version/material-state construction is Slice D.

### 16.5 ExternalRef

```text
ExternalRef
= provider/source-scoped identity
```

It remains outside canonical native/scoped-record identity unless reconciliation establishes an applicable mapping.

### 16.6 Address-space non-collapse

```text
NativeRef != ScopedRecordRef
NativeRef != MaterialStateRef
NativeRef != ExternalRef
ScopedRecordRef != MaterialStateRef
ScopedRecordRef != ExternalRef
MaterialStateRef != ExternalRef
```

A future technical envelope/registry may carry these variants, but it may not erase the distinction.

### 16.7 Reference Contract extension

A Reference Contract now constrains, where applicable:

```text
semantic role/family
eligible address variants
eligible target owner/family
scope/context
cardinality/directionality
unresolved-target behavior
material-state/facet binding
history/materiality rules
Visibility/Authority implications
specialist/extension boundary
```

Resolvable/addressable does not imply semantically eligible.

### 16.8 Technology/mechanism reconsideration result

The integrated checkpoint reopened:

```text
owner-specific reference families
global Node/Entity registry
one undifferentiated TypedRef(kind,id)
discriminated ReferenceAddress family + Reference Contract
```

Current verdict:

```text
SELECTED FAMILY
ReferenceAddress discriminated family + Reference Contract

TECHNOLOGY / MECHANISM VERDICT
RETAIN + HARDEN
```

Owner-specific references remain a strong Physical Model ingredient. A technical registry may still be used later if it stays representation-only. A global semantic Node/Entity root remains rejected.
