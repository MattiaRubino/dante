# LifeOS Logical Representation Framework v1

**Status:** Stage-0 foundation  
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

## 9. Slice deliverable template

Every logical slice should produce at least:

1. owner inventory;
2. mandatory semantic invariants;
3. candidate logical representations;
4. selected representation and rejected alternatives;
5. identity/reference rules;
6. lifecycle/state rules;
7. history/correction rules;
8. typed relationship rules;
9. provider/reconciliation rules;
10. derived/projection rules;
11. simple-case representation;
12. specialist extension boundaries;
13. high-value queries;
14. adversarial test results;
15. external benchmark findings;
16. reverse mapping;
17. open logical questions;
18. LM gate matrix;
19. exact deferred physical decisions.

No exact SQL schema is required or authorized by this template.

---

## 10. Initial slice roadmap

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
