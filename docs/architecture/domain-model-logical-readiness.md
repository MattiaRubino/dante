# Domain Model → Logical Model Readiness Contract

**Status:** CURRENT / SATISFIED  
**Originally established:** 2026-08-16  
**Current closure state:** Domain CLOSED; Logical Model CLOSED; WD-03 and WD-05 discharged  
**Authority:** Domain Validation Methodology v3 + accepted Domain Atlas + ADR-007 + Whole-Logical remote-QA closure

## Purpose

This document is the durable implementation bridge between the accepted Domain Model and logical/persistence representation.

It does not define SQL tables, API resources, migrations or ORM classes. Its job is to prevent technical representation from silently changing accepted semantic meaning.

The readiness transition described here is no longer pending: the Logical Model was completed and remotely closed. The original guardrails remain current because downstream physical/database work must continue to preserve them.

Current activation evidence:

- [`../domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md`](../domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md) — Domain closure;
- [`../logical-model/checkpoints/whole-logical-v1-remote-qa.md`](../logical-model/checkpoints/whole-logical-v1-remote-qa.md) — Logical Model closure and final WD-03 / WD-05 discharge.

The chronological continuation files `domain-model-logical-readiness-part-2.md` through `domain-model-logical-readiness-part-5.md` are now transition/closure evidence. They do not need to be read to establish the current state represented here.

---

# 1. Authority order

For semantic meaning:

```text
accepted Domain Atlas / current validation checkpoints
        >
this readiness contract
        >
legacy architecture examples and candidate persistence language
        >
provider schema / convenience
```

Architecture documents created before the completed Domain Atlas remain valuable historical/technical context but do not reopen or override later accepted semantic decisions.

ADR-007 owns the compatibility rule.

---

# 2. What logical and physical design may optimize

Technical representation may optimize:

- referential integrity;
- queryability;
- transaction boundaries;
- indexability;
- history/audit reconstruction;
- provider reconciliation;
- simple V1 implementation;
- progressive formalization;
- storage efficiency;
- privacy/security enforcement;
- API/tool usability.

It may not optimize by erasing semantic distinctions the Domain Atlas requires.

---

# 3. Representation is not ontology

Implementation may use common technical structures.

Examples:

```text
reference registry
shared typed relation table
common history table
polymorphic reference envelope
JSONB metadata
provider identity mapping
search projection
```

None of these, by itself, establishes:

```text
universal Thing
universal Entity
universal Relationship
semantic-free related_to
one lifecycle shared by all referents
one visibility/authority model inherited by all links
```

A shared physical structure must preserve typed semantic ownership.

---

# 4. Required identity distinctions

Technical representation must preserve independent identity where the Domain Atlas requires it.

At minimum:

```text
Person != Account
Person != Actor
Account != Actor

Goal != Plan
Plan != Activity
Activity != Event
Routine != Occurrence
Occurrence != current schedule placement

Asset != Resource
Place != Asset
Content Artifact != file/blob/provider object
Collective != membership set
```

Role/capability participation in another semantic family must not replace native identity.

---

# 5. Required temporal/reality distinctions

At minimum:

```text
intended / expected
!= current accepted placement/state
!= actual realization

Occurrence != Schedule
Schedule != Session
Session != Actual
Actual != Observation
Actual != Outcome
```

Logical or physical shortcuts must not make one-off recurrence exceptions indistinguishable from source-policy changes.

Past effective state must remain reconstructible where material.

---

# 6. Required evidence/epistemic distinctions

At minimum:

```text
source/provider record != canonical truth automatically
Observation != Evidence
Evidence != Provenance
Confirmation != universal truth
AI proposal/inference != established domain state
correction != silent overwrite
unknown != explicitly absent/open
```

Unresolved conflict is a valid state. No universal last-write/provider/highest-confidence winner is allowed unless a bounded domain policy explicitly establishes one.

---

# 7. Required relationship/governance distinctions

Specific accepted semantics must remain distinguishable even if one physical relation mechanism is used.

At minimum:

```text
Participation
Responsibility
Coordination Stewardship
Authority
Visibility
Acknowledgement
Agreement
Consent
Representation
Membership
Contribution
Ownership
Possession
Interpersonal Relationship
Dependency
Resource Allocation
```

Canonical guardrails include:

```text
Authority != Visibility
Agreement != Consent
Responsibility != Participation
Responsibility != Stewardship
Membership != Authority
Ownership != Possession
Interpersonal relationship label != rights/duties
```

---

# 8. Required value distinctions

```text
Quantity
= reusable physical/quantitative value semantics where unit equivalence is stable/applicable

MonetaryAmount
= numerical amount + unambiguous currency semantics

Quantity != MonetaryAmount
```

Cross-currency derivation must preserve applicable conversion basis where material. It must not be treated as ordinary stable unit conversion.

---

# 9. Content and Place boundaries

```text
Content Artifact
!= blob/file/path/URL/provider object

Place
!= address
!= coordinates
!= provider place ID
```

Storage/provider identity changes must be representable without automatically changing domain identity.

---

# 10. Privacy and multi-actor requirement

Technical design must support bounded projection semantics.

```text
Visibility(object/container)
!= Visibility(all facets)
!= Visibility(relationships)
!= Visibility(source causes)
```

A private source may produce an authorized shared projection without exposing the source.

The model must not force object duplication per recipient merely to achieve selective visibility.

External/accountless Persons must remain representable independently from Account/Principal implementation.

---

# 11. Simple-user requirement

Semantic precision is internal capability, not mandatory UI complexity.

Technical design should permit simple cases to remain compact when no material distinction would be lost.

```text
semantic capability
!= mandatory standalone persisted object in every case
!= mandatory UI form
!= mandatory user-visible lifecycle
```

Materialization should be consequence/query/history-sensitive where the owning concept allows it.

---

# 12. Generic/flexible data boundary

JSONB, metadata and generic technical references remain useful for:

- provider-specific detail;
- flexible descriptive properties;
- optional specialist metadata;
- temporary raw integration material;
- implementation projection.

They may not conceal an unresolved required kernel semantic owner.

AI uncertainty must remain proposal/unresolved/source-backed state rather than become an untyped canonical property/relation.

---

# 13. Specialist-boundary rule

The logical/physical core must allow specialist modules/adapters to relate to accepted kernel semantics without forcing specialist ontology into the general kernel.

Examples include:

- full accounting/ledger/shared-expense netting;
- inventory movement/stock ledger;
- provider ticket entitlement;
- regulated clinical/legal validity;
- enterprise governance;
- AuthN/AuthZ Principal/runtime identity.

Future specialist evidence may reopen a bounded semantic question, but specialist storage needs alone do not rewrite the general kernel.

---

# 14. Validation requirement retained downstream

The Logical Model was required to prove:

1. semantic owner coverage;
2. identity preservation;
3. history/material-state reconstruction;
4. relation specificity;
5. multi-actor/selective-visibility pressure;
6. provider reconciliation pressure;
7. simple-case compactness;
8. specialist-boundary pressure;
9. no semantic-free generic fallback;
10. reverse mapping from logical representation back to domain meaning.

The completed Whole-Logical closure established these properties and discharged the two Domain carry-forward obligations:

```text
WD-03 historical reconstruction  PASS
WD-05 persistence/API pressure   PASS
```

These remain regression obligations for later implementation. A physical/database representation that cannot satisfy an accepted invariant must report the conflict and trigger targeted review; it must not silently simplify the model.

---

# 15. Current readiness verdict

```text
DOMAIN MODEL
SEMANTICALLY CLOSED FOR CURRENT ACCEPTED KERNEL

WD-01..WD-10
PASS

LOGICAL MODEL
POST-WRITE QA PASS
CLOSED

LEGACY GENERIC-MODEL AUTHORITY
SUPERSEDED WHERE INCOMPATIBLE

POSTGRESQL / HYBRID DIRECTION
RETAINED AND SUBSEQUENTLY MATERIALIZED UNDER LATER PHYSICAL/BACKEND GATES
```

This document no longer grants a future transition by itself; it records the durable semantic compatibility contract that downstream work must continue to satisfy.

## Historical transition evidence

The following files remain evidence of how the readiness state evolved and was activated:

- `domain-model-logical-readiness-part-2.md`;
- `domain-model-logical-readiness-part-3.md`;
- `domain-model-logical-readiness-part-4.md`;
- `domain-model-logical-readiness-part-5.md`.

They are not independent current architecture authorities. Any future compaction/removal of them must pass the documentation knowledge-coverage gate first.
