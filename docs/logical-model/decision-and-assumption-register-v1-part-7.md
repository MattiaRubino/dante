<!-- LIFEOS-CANONICAL-CONTINUATION document="decision-and-assumption-register-v1.md" follows="decision-and-assumption-register-v1-part-6.md" -->
> **Canonical continuation of the Logical Model Decision and Assumption Register v1.** Earlier decisions/assumptions remain active unless explicitly superseded. This continuation records Integrated A+B+C+D+E cumulative decisions and hardening.

# Integrated A+B+C+D+E — Decision Register

## DEC-ABCDE001 — Retain layered typed architecture after cumulative technology reconsideration

**Decision:** retain the layered typed Logical Model using domain-owned semantic records, `ReferenceAddress`, `MaterialStateRef`, typed specification/relation roles, LR-08 projections and specialist boundaries.

**Why selected:** it remains the only candidate that simultaneously preserves semantic ownership, historical reconstructibility, simple-case compactness, solver replaceability, provider/source separation and future physical freedom without introducing a universal semantic root.

**Rejected alternatives:**

```text
universal Resource / Requirement / Constraint graph
universal Capacity / Claim / Reservation ledger as whole kernel
fully owner-specific Logical Model baseline
universal bitemporal/event-sourced planning ontology
snapshot-everything solver/audit model
solver-first canonical model
```

**Retained ingredients from rejected candidates:**

```text
owner-specific physical structures
bounded capacity/claim accounting
bitemporal/event-history techniques
consequence-sensitive snapshots
solver/optimization engines
shared predicate/expression machinery
```

**Regression impact:** R3 WHOLE-LOGICAL.

**Reopen trigger:** stronger cross-domain evidence shows an alternative survives identity/history/governance/simple-case/product-reality pressure better without recreating a generic semantic root.

**Status:** RETAIN + HARDEN.

## DEC-ABCDE002 — Resource-target addressability remains heterogeneous

**Decision:** Resource-capable Reference Contracts may target justified `NativeRef` owners or bounded non-native dependent/value/service/pool/supply/specialist representations.

**Why selected:** `Resource` is contextual role semantics and does not independently justify identity for every candidate/provider representation.

**Rejected alternatives:** NativeRef-only resource targeting; synthetic Resource wrapper/native identity.

**Trace/tests:** INV-ABCDE001; ABCDE-REF-01..03.

**Reopen trigger:** a concrete target family proves independent persistent identity/history requiring a reviewed native/specialist owner.

**Status:** RETAIN + HARDEN.

## DEC-ABCDE003 — Consequential Allocation/Claim must bind to material input state

**Decision:** where consequence/reproducibility requires it, Allocation/Claim must bind to or reconstruct the applicable Requirement, temporal, Availability/Capacity, policy and governance basis.

**Why selected:** current mutable source state cannot truthfully explain a historical consequential effect after later revisions/corrections.

**Rejected alternatives:** current-state reconstruction only; copying all input fields universally onto each effect; universal `InputSnapshot` ontology root.

**Trace/tests:** INV-ABCDE002; ABCDE-HIST-01..04.

**Physical deferral:** exact storage may be version FK, MaterialStateRef anchor, bounded snapshot, bitemporal reconstruction or hybrid.

**Reopen trigger:** physical pressure demonstrates that the logical binding cannot be implemented without violating compactness or owner specificity.

**Status:** RETAIN + HARDEN.

## DEC-ABCDE004 — Candidate history is consequence-sensitive

**Decision:** Candidate Set remains LR-08 by default; exact historical candidate universe is retained/reconstructed only where materially consequential.

**Why selected:** current candidate recomputation can drift; snapshotting every transient universe is wasteful and solver-coupling.

**Rejected alternatives:** canonical candidate rows for every run; current query used as historical truth; no historical basis at all.

**Trace/tests:** INV-ABCDE003; ABCDE-CAND-01..03.

**Reopen trigger:** product/regulatory scope requires exact historical candidate-set identity broadly enough that a stronger reusable snapshot mechanism is justified.

**Status:** RETAIN + HARDEN.

## DEC-ABCDE005 — Narrow `Actual use` terminology to appropriate reality ownership

**Decision:** Slice E uses `realized resource use / consumption` as the general concept; Domain `Actual` is used only when reconciling a prior expectation.

**Why selected:** Domain Actual explicitly is not the universal database of everything that happened.

**Rejected alternative:** create Actual for every observed/spontaneous use.

**Trace/tests:** INV-ABCDE004; ABCDE-ACTUAL-01/02.

**Reopen trigger:** none from naming/implementation convenience; requires Domain semantic change.

**Status:** RETAIN + HARDEN.

## DEC-ABCDE006 — LR-05 remains owner-specific representation role, not universal Rule root

**Decision:** allow shared predicate/expression/comparison infrastructure while preserving Criterion, Resource Requirement, Temporal Constraint, Availability rule, Conditional Policy and other specifications as distinct semantic owners.

**Why selected:** identical technical shape does not imply identical purpose, lifecycle, governance, history or effect semantics.

**Rejected alternative:** canonical `Rule(id,type,payload)` semantic superclass/escape hatch.

**Trace/tests:** INV-ABCDE005; ABCDE-RULE-01..03.

**Reopen trigger:** a reviewed higher-order semantic owner is independently proven across existing families, not merely shared technical syntax.

**Status:** RETAIN + HARDEN.

## DEC-ABCDE007 — Implicit Requirement escalates only at consequence threshold

**Decision:** retain compact embedded/implicit Requirement representation in simple cases; require material reconstructibility when a consequential effect depends on its exact state.

**Why selected:** preserves simple-case compactness without sacrificing historical truth.

**Rejected alternatives:** mandatory Requirement entity everywhere; permanently mutable embedded Requirement after consequential use.

**Trace/tests:** INV-ABCDE006; ABCDE-IMPLICIT-01/02.

**Physical deferral:** explicit LR-02, containing-owner MaterialStateRef or another typed form may implement the escalation.

**Reopen trigger:** repeated implementation complexity shows a stable simpler materialization rule is safer across owners.

**Status:** RETAIN + HARDEN.

## DEC-ABCDE008 — Capacity Claim historical time basis is explicit/reconstructible

**Decision:** when a claim is subordinate to Schedule and Schedule changes, historical claim placement must remain reconstructible through Schedule MaterialStateRef or claim-owned temporal basis.

**Why selected:** current Schedule cannot rewrite prior capacity commitments.

**Rejected alternative:** claim always dereferences only current Schedule state.

**Trace/tests:** INV-ABCDE007; ABCDE-HIST-04.

**Reopen trigger:** final physical model proves one representation dominates without losing historical truth.

**Status:** RETAIN + HARDEN.

## DEC-ABCDE009 — Solver/AI auditability is consequence-sensitive and engine-independent

**Decision:** solver/model remains replaceable computation; consequential accepted effects preserve/reconstruct only the material inputs/configuration/rationale needed for explanation/replay.

**Why selected:** avoids both opaque AI/solver decisions and excessive snapshotting/solver lock-in.

**Rejected alternatives:** solver variables/solution as canonical state; persist every search node; no retained material basis.

**Trace/tests:** INV-ABCDE008; ABCDE-SOLVER-01..04.

**Physical deferral:** exact audit payload/schema/versioning strategy is Physical Model work.

**Reopen trigger:** legal/regulatory/product requirements require broader deterministic replay than currently assumed.

**Status:** RETAIN + HARDEN.

## DEC-ABCDE010 — Preserve typed feasibility ladder

**Decision:** maintain semantic distinction among eligibility, candidacy, availability, feasibility, capacity sufficiency, allocation, claim and realized use.

**Why selected:** one boolean/status cannot truthfully answer all resource questions across people/assets/places/pools/services.

**Rejected alternative:** universal `available` or `resource_status` source field.

**Trace/tests:** INV-ABCDE009; ABCDE-FEAS-01..05.

**Reopen trigger:** none from UI/API convenience; projections may compress but source semantics remain distinct.

**Status:** RETAIN.

# Integrated A+B+C+D+E — Assumption Register

## ASM-ABCDE001 — Consequential effects are the correct threshold for stronger historical binding

**Statement:** most ordinary transient evaluations/searches do not require durable exact snapshots; consequential effects do.

**Evidence:** current LifeOS product scenarios; Slice D historical reconstruction; Slice E scale/simple-case tests; mature planner/saved-plan patterns.

**Stability:** EVOLVING.

**If false:** introduce a broader audited-computation retention policy, still without changing semantic owner identities.

**Refresh trigger:** compliance, legal, financial, medical or enterprise product scope materially raises replay obligations.

## ASM-ABCDE002 — Shared predicate/expression machinery can preserve owner typing

**Statement:** future Physical Model/runtime can reuse rule/predicate infrastructure without collapsing Criterion/Requirement/TemporalConstraint/etc. into one semantic root.

**Evidence:** representation roles already separate semantics from mechanism; cross-slice reverse mapping remains deterministic.

**Stability:** STABLE at Logical Model level; EVOLVING physically.

**If false:** use more owner-specific physical structures/DSLs.

**Refresh trigger:** one shared implementation repeatedly leaks generic semantics, weak typing or invalid cross-owner operations.

## ASM-ABCDE003 — Candidate history can remain selective rather than universal

**Statement:** exact historical candidate universe is material only for a subset of consequential workflows.

**Evidence:** ordinary recommendation/search scenarios vs audit/Decision scenarios.

**Stability:** EVOLVING.

**If false:** define a stronger reusable candidate-evaluation snapshot profile.

**Refresh trigger:** product analytics/audit repeatedly needs exact historical candidate universes across ordinary flows.

## ASM-ABCDE004 — MaterialStateRef remains sufficient as the logical state-binding abstraction

**Statement:** no new `RequirementStateRef`, `AvailabilityRef`, `CapacityRef` or `FeasibilityRef` is currently needed.

**Evidence:** A+B+C+D+E replay successfully binds material owner state without introducing new universal identities.

**Stability:** STABLE.

**If false:** add the narrowest reviewed owner-specific addressing contract; do not default to universal Fact/State identity.

**Refresh trigger:** reverse mapping or historical reconstruction fails for a concrete consequential state.

## ASM-ABCDE005 — Solver/model replacement should not require semantic migration

**Statement:** optimization engines will evolve and can change without changing canonical LifeOS domain identity/state.

**Evidence:** multiple viable solver families and current architecture separation.

**Stability:** STABLE.

**If false:** solver-specific execution state may be retained as specialist/computation metadata, while canonical semantic ownership stays independent.

**Refresh trigger:** a solver-owned state becomes user-visible/domain-significant beyond computation mechanics.

## ASM-ABCDE006 — Private feasibility causes can remain separable from shareable results

**Statement:** future governance/visibility model can authorize use of private inputs while exposing only bounded capacity/availability consequences.

**Evidence:** accepted Visibility/Authority boundaries and D/E Product Reality tests.

**Stability:** EVOLVING pending Slice F.

**If false:** Slice F must block or redesign affected shared workflows; do not solve by universal disclosure.

**Refresh trigger:** Slice F reveals an enforcement/authority contradiction.

## ASM-ABCDE007 — Capacity Claim may operationally follow Schedule without losing semantic independence

**Statement:** subordinate claims can track the current Schedule operationally while history binds material prior placements.

**Evidence:** Slice E scheduling/claim semantics + cumulative historical replay.

**Stability:** EVOLVING.

**If false:** claims may require stronger standalone temporal ownership in the Physical Model.

**Refresh trigger:** conflict resolution, concurrency or external reservation integration proves independent claim timing lifecycle is common.

# Rejected-alternative register additions

```text
ALT-ABCDE01 NativeRef-only Resource targets
REJECT — promotes non-native role targets into synthetic identity

ALT-ABCDE02 universal InputSnapshot semantic owner
REJECT — snapshot is mechanism, not domain owner

ALT-ABCDE03 canonical Candidate Set for every solver/search run
REJECT — scale/lock-in/simple-case failure

ALT-ABCDE04 universal Actual for every realized resource use
REJECT — violates Actual expectation-reconciliation boundary

ALT-ABCDE05 universal Rule semantic root
REJECT — shared LR-05 machinery != shared owner

ALT-ABCDE06 always-implicit mutable Requirement
REJECT — historical consequence becomes unreconstructible

ALT-ABCDE07 Claim points only to current Schedule state
REJECT — historical temporal basis drifts

ALT-ABCDE08 snapshot every solver variable/search node
REJECT — excessive volume and engine coupling

ALT-ABCDE09 opaque solver/AI accepted effect
REJECT — consequential result lacks reconstructible material basis
```

# Cumulative decision integrity counters

```text
unclassified material decisions        0
unregistered material assumptions      0
rejected candidates without rationale  0
unsafe physical deferrals              0
Domain reopen required                  0
```

No decision in this continuation authorizes SQL/schema/API/runtime implementation or Slice F semantics.