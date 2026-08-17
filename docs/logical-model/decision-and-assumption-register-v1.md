# LifeOS Logical Model Decision & Assumption Register v1

**Status:** Stage-0H normative foundation  
**Date:** 2026-08-17  
**Purpose:** prevent forgotten rejected designs, hidden assumptions, stale external dependencies and accidental reversals during Logical Model design

---

## 1. Why this register exists

Logical-model work will compare many plausible structures. Without a durable register, teams tend to repeat rejected approaches, forget why a hardening exists, or let temporary assumptions silently become permanent architecture.

This register separates:

```text
ACCEPTED LOGICAL DECISION
REJECTED ALTERNATIVE
WORKING ASSUMPTION
EXTERNAL DEPENDENCY / EVIDENCE
STAGE-DEFERRED PHYSICAL DECISION
```

None of these categories may be silently substituted for another.

---

## 2. Accepted decision record

Every material accepted logical decision should record:

```text
DECISION ID
SLICE / SCOPE
QUESTION
SELECTED CANDIDATE
DOMAIN INVARIANTS PRESERVED
WHY SELECTED
FALSIFICATION SURVIVED
REJECTED ALTERNATIVES
TRACE / TEST REFERENCES
EXTERNAL EVIDENCE USED
ASSUMPTIONS
HARDENINGS
REGRESSION IMPACT CLASS
PHYSICAL DECISIONS DEFERRED
REOPEN TRIGGERS
STATUS
```

A decision is not accepted merely because one candidate was documented first.

---

## 3. Rejected Alternatives Register

Every materially plausible candidate that is rejected must remain discoverable.

Record at least:

```text
ALT ID
QUESTION / SCOPE
CANDIDATE
WHY IT LOOKED PLAUSIBLE
FAILURE EVIDENCE
INVARIANTS / TESTS FAILED
WHETHER REJECTION IS LOGICAL OR ONLY CURRENT-PHYSICAL
CONDITIONS THAT COULD JUSTIFY RETEST
```

Purpose:

- avoid rediscovering and re-proposing already falsified architectures;
- make future reviews understand trade-offs rather than seeing only the winner;
- distinguish a permanently semantically invalid candidate from one rejected only under current evidence;
- expose confirmation bias where all rejected alternatives are caricatures.

At least one rejected candidate should normally be a strong plausible alternative, not an obvious straw man.

---

## 4. Assumption Register

Any material decision that depends on something not guaranteed by the Domain Atlas must identify the assumption.

Record:

```text
ASSUMPTION ID
STATEMENT
SCOPE / DECISIONS DEPENDING ON IT
EVIDENCE
CONFIDENCE
STABILITY
FAILURE CONSEQUENCE
REFRESH TRIGGER
LAST VERIFIED
STATUS
```

Suggested stability vocabulary:

```text
STABLE
slow-changing standard/domain fact

EVOLVING
product/provider pattern likely to change over time

VOLATILE
API/provider/product behavior that may materially change quickly

UNPROVEN
working hypothesis requiring validation before acceptance
```

An `UNPROVEN` assumption cannot support a final PASS where its failure would materially invalidate the representation.

---

## 5. Refresh triggers

Assumptions/evidence must be rechecked when any of these occur:

```text
start of a slice materially depending on them
selection of a preferred candidate
provider/API version change
external standard revision
new product capability introduces conflicting pressure
later slice changes shared infrastructure
whole-logical final regression
material implementation feasibility evidence contradicts the assumption
```

Do not refresh external evidence merely for ceremony when it cannot affect the decision, but do not rely on stale remembered behavior where it can.

---

## 6. External evidence classification

External evidence should be recorded as one of:

```text
STRUCTURAL PRINCIPLE
mechanism/invariant useful beyond one vendor implementation

CURRENT PRODUCT BEHAVIOR
useful but potentially volatile implementation evidence

INTEROPERABILITY CONSTRAINT
must be respected when integration/standard compatibility matters

SPECIALIST BOUNDARY EVIDENCE
shows richer lifecycle/identity belongs to a bounded domain

NEGATIVE BENCHMARK
behavior LifeOS intentionally rejects
```

A current product behavior must not silently become a permanent LifeOS invariant.

---

## 7. Physical-stage deferral register

Logical Model should deliberately defer exact physical choices that are not needed to settle meaning.

Record:

```text
DEFER ID
LOGICAL QUESTION ALREADY RESOLVED
PHYSICAL QUESTION DEFERRED
WHY DEFERRAL IS SAFE
WHAT MUST BE PRESERVED LATER
ACTIVATION STAGE
```

Typical examples may include:

```text
exact PostgreSQL table split
index strategy
partitioning
ORM mapping
API serialization envelope
cache/read-model technology
runtime authorization enforcement mechanism
```

Deferral is invalid if it hides an unresolved logical behavior.

---

## 8. Decision quality checks

Before a material decision is accepted, verify:

1. the selected candidate is not simply the first candidate considered;
2. rejected alternatives include at least one materially plausible option where one exists;
3. assumptions are explicit;
4. external evidence is classified by stability and authority;
5. mutation and counterfactual tests challenged the preferred candidate;
6. simple and worst-case scenarios both survive;
7. the traceability ledger shows which Domain invariants are preserved;
8. later physical implementation still has more than one option where the Logical Model does not require one exact shape;
9. no provider-specific convenience has been promoted into semantic truth;
10. reopen triggers are concrete enough to detect future invalidation.

---

## 9. Seed anti-assumptions

The following must never be treated as implicit assumptions:

```text
one Account = one Person forever
one provider ID = one LifeOS referent
latest provider write = canonical truth
every scheduled block happened
every AI inference is a stable preference
every native referent needs one universal superclass
every cross-domain reference requires a generic semantic Relation
every semantic capability requires standalone persistence
every current product API behavior is permanent
every high-volume history requires event sourcing
every historical requirement requires full bitemporality everywhere
PostgreSQL convenience can redefine Domain meaning
```

If a candidate depends on one of these, it must be rejected or explicitly reformulated.

---

## 10. Register state vocabulary

```text
PROPOSED
UNDER TEST
ACCEPTED WITH HARDENING
ACCEPTED
REJECTED
SUPERSEDED LOGICALLY
STALE EVIDENCE — REFRESH REQUIRED
STAGE-DEFERRED PHYSICAL
BLOCKED
```

Historical accepted/rejected records remain preserved even after a later decision supersedes them.

---

## 11. Final closure requirement

Whole-Logical closure requires:

```text
unclassified material decisions        0
unregistered material assumptions      0
stale material external dependencies   0
rejected candidates without rationale  0
unsafe physical deferrals              0
```

The final clean-room reconstruction must be able to understand why the major representation choices were made using this register plus the traceability ledger, without relying on undocumented conversation history.
