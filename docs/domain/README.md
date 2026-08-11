# LifeOS Domain Atlas

**Status:** In progress  
**Started:** 2026-08-10  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

The Domain Atlas is the working source for re-evaluating and defining LifeOS domain concepts before broad persistence or backend implementation.

Its job is not to preserve earlier terminology by inertia. Its job is to produce the strongest current domain model we can justify from product intent, real-world scenarios, external evidence, implementation constraints and explicit reasoning.

## Decision rule

**Accepted means current best decision, not immutable decision.**

A concept may be reopened when new scenarios, evidence, implementation constraints, contradictions or better abstractions emerge. Changes must be deliberate and documented; prior reasoning must not be silently overwritten.

Earlier product documents, simulations, glossaries, ADRs, prototypes and conversation history are inputs to re-evaluate. They are not automatically correct merely because they were written earlier.

Where an accepted ADR defines a broader architectural constraint, this workstream respects it unless new evidence is strong enough to justify an explicit ADR change.

---

# Mandatory concept-review protocol

Every Domain Atlas concept must be reviewed against more than the immediately preceding discussion before it is accepted.

All new concepts use **Domain Validation Methodology v3** and its mandatory execution template.

Ordered validation pipeline:

```text
A. Evidence + candidate formation
        ↓
B. Core Semantic Validation Gate
        ↓
C. Multi-Actor Compatibility Gate
        ↓
D. Cross-Concept Consistency Gate
        ↓
Concept verdict
```

Every completed cluster then passes:

```text
Cluster Integration Gate
        ↓
Cluster Multi-Actor Stress Gate
        ↓
Cluster verdict
```

Before broad persistence/API stabilization the whole accepted domain must pass final whole-domain regression, multi-actor and implementation-pressure gates.

Canonical references:

- [`Validation Methodology v3`](validation-methodology-v3.md)
- [`Validation Execution Template v3`](validation-execution-template-v3.md)
- [`Multi-Actor Readiness v1`](multi-actor-readiness-v1.md)

Validation Methodology v2 and its multi-actor addendum remain preserved under `history/` as audit/evolution evidence. Compatibility redirect files remain at their previous paths so older links do not silently point to a competing active standard.

The goal is not the largest ontology. It is the smallest model that survives real life without losing semantic meaning, history, queryability, extensibility, privacy or usability.

---

# External benchmark and interoperability rule

External standards, products, APIs and schemas are **benchmark evidence, not design authorities**.

LifeOS should adopt an external pattern when it improves the internal model or provides useful interoperability at negligible conceptual cost. The domain model must not be weakened/distorted merely to match another platform.

Preferred direction:

```text
LifeOS semantics
        ↓
strong internal model
        ↓
optional adapters / mappings
        ↓
external standards/providers
```

not:

```text
external schema
        ↓
LifeOS kernel must imitate it
```

Consequences:

- provider identifiers/recurrence/status taxonomies do not become canonical identity by default;
- lossless external mapping is not a kernel invariant;
- adapters absorb provider-specific compromise where practical;
- specialist systems can remain authoritative while LifeOS coordinates around permitted facts.

---

# Documentation standard

Canonical Domain Atlas documentation is written in **English**.

Discussion may occur in another language, but the repository maintains one canonical documentation tree rather than parallel translations that can diverge.

Each accepted concept should document where relevant:

- canonical definition;
- why the concept exists;
- validation basis;
- boundaries against adjacent concepts;
- identity and context/ownership/governance implications;
- lifecycle and temporal semantics;
- planned/current/actual/history distinctions;
- evidence/provenance implications;
- multi-actor implications;
- representative/adversarial examples;
- invariants;
- alternatives considered/rejected;
- deliberately deferred questions;
- persistence/API implications without prematurely fixing physical tables.

Every new concept/cluster checkpoint must use the v3 test registry, record applicable test IDs, justify `N/A`, record hardenings/dependencies and select exactly one verdict:

```text
PASS
PASS WITH HARDENING
REOPEN
DEFERRED DEPENDENCY
```

---

# Domain & Product Language Map

Canonical quick-reference terminology lives in:

- [`Domain & Product Language Map`](language-map.md)

It separates:

```text
DOMAIN LANGUAGE
PRODUCT LANGUAGE
UI LANGUAGE
IMPLEMENTATION LANGUAGE
```

and classifies terms as:

```text
CANONICAL
DERIVED
PRODUCT PROFILE
PRODUCT / UI TERM
PROVISIONAL
DEFERRED
HISTORICAL / SUPERSEDED
```

Core rule:

> **Domain concept != mandatory UI object, and UI label != mandatory domain primitive.**

The Language Map records decisions; it does not create primitives. New canonical terms must first pass normal Domain Atlas review.

The older `docs/product/v1-core-domain-glossary.md` remains product-history evidence but is not authoritative where the Domain Atlas/Language Map supersedes its kernel terminology.

---

# Working method

Concepts are reviewed one at a time.

For each concept establish:

1. canonical definition;
2. what it is/is not;
3. identity and actor/context independence;
4. lifecycle/temporal semantics;
5. invariants;
6. relationships to other concepts;
7. evidence/provenance/derived state where relevant;
8. real-world and edge-case coverage;
9. explicit Multi-Actor Compatibility Gate;
10. cross-concept consistency;
11. rejected alternatives;
12. deliberately deferred questions;
13. implications for future persistence/APIs.

Saving a concept does not permanently close it.

---

# Cluster checkpoints

Concept-level validation is necessary but insufficient. Related concepts must also survive cluster and cross-cluster tests.

## Intention & Execution — VALIDATED CURRENT BASELINE

Validated set:

- Goal;
- Plan;
- Activity;
- Event;
- Routine;
- Milestone.

Checkpoint:

- [`Intention & Execution Cluster v0`](checkpoints/intention-execution-v0.md)

The cluster later passed the cross-cluster validation and evidence-backed multi-actor synthesis.

## Time — VALIDATED CURRENT BASELINE

Validated set:

- Occurrence;
- Schedule;
- Session;
- Temporal Constraint;
- Recurrence;
- Availability & Capacity.

Checkpoint:

- [`Time Cluster v0`](checkpoints/time-v0.md)

Earlier hardenings retained:

1. quota Recurrence preserves an explicit-enough period frame where membership/boundary semantics matter; equivalent quota Occurrences do not gain arbitrary ordinal meaning;
2. materially changing long-horizon progression tends toward Plan rather than one mega-Routine;
3. Event identity/historical expectation may survive temporary absence of current Schedule when postponed/unresolved.

## Cross-cluster validation — VALIDATED CURRENT BASELINE

- [`Cross-Cluster Validation v2`](checkpoints/cross-cluster-validation-v2.md)

Result: all twelve initial concepts retained; no justified merge/removal; no universal hierarchy required; top-down planning, bottom-up reality capture and lateral relevance remain representable without rewriting historical intention.

## Multi-Actor Evidence Synthesis — VALIDATED CURRENT BASELINE

References:

- [`Multi-Actor Readiness v1`](multi-actor-readiness-v1.md);
- [`Multi-Actor Evidence Synthesis v0`](checkpoints/multi-actor-evidence-synthesis-v0.md);
- [`Discovery Simulation`](../product/multi-actor-collaboration-discovery-simulation-2026-08.md);
- [`External Deep Research`](../product/multi-actor-collaboration-research-2026-08.md).

Result:

```text
Intention & Execution v0 — PASS
Time v0                 — PASS
Multi-Actor Readiness   — PASS WITH EVIDENCE-BACKED HARDENING

Structural reopenings    — 0
Concept removals          — 0
Concept merges            — 0
Mandatory new primitives — 0
```

## Observed Reality & Evidence — IN PROGRESS

Current accepted concepts:

- [`Actual v0`](concepts/actual.md) — accepted 2026-08-11 under Methodology v3;
- [`Outcome v0`](concepts/outcome.md) — accepted 2026-08-11 under Methodology v3;
- [`Observation v0`](concepts/observation.md) — accepted 2026-08-11 under Methodology v3.

Validation records:

- [`Actual v0 Validation`](checkpoints/actual-v0-validation.md) — **PASS WITH HARDENING**;
- [`Outcome v0 Validation`](checkpoints/outcome-v0-validation.md) — **PASS WITH HARDENING**;
- [`Observation v0 Validation`](checkpoints/observation-v0-validation.md) — **PASS WITH HARDENING**.

Current boundaries:

```text
Actual
= contextual realization of a specific intention/expectation

Outcome
= contextual result/disposition of that realization where result meaning matters

Observation
= contextual measurement/property/state/rating/simple assertion about a subject

Actual != Session
Actual != Outcome
Actual != Observation
Outcome != Observation
Observation != Quantity
Observation != Register
Observation != Evidence
Observation != Confirmation
Observation != Provenance
```

Critical Actual invariants:

- Actual is not a universal reality mega-object;
- spontaneous reality may exist without Actual when no expectation is being reconciled;
- no established Actual does not mean failed/skipped/missed;
- known non-realization is distinct from unknown;
- passage of time does not establish Actual;
- shared Actual does not imply identical actor-specific participation;
- correction changes current accepted realized truth without silently deleting relevant assertion/provenance history.

Critical Outcome invariants:

- Outcome is optional and contextual;
- lifecycle/operational state is distinct from Outcome;
- no universal Outcome enum is accepted;
- absence of Outcome is not a negative Outcome;
- `unconfirmed` belongs to Confirmation/epistemic semantics rather than Outcome;
- measurements/Observations and produced artifacts remain separate;
- shared Outcome does not imply identical actor-specific consequences;
- one actor/provider assertion does not automatically establish universal canonical Outcome.

Critical Observation invariants:

- Observation is a measurement/simple-assertion concept, not a universal data/fact/blob primitive;
- may exist without prior intention, Actual, Outcome, Goal, Session, or Register;
- Observation identity is not derived from subject/type/time/value;
- correction of the same observational act normally preserves identity; re-observation normally creates a new Observation;
- effective time/context is distinct from recorded/ingested time;
- missing Observation != explicit negative Observation != failed/unavailable measurement;
- subjective observations are valid when perspective/source/context are preserved;
- conflicting observations may coexist and must not be silently averaged/overwritten;
- derived observations preserve traceability to source facts;
- query/chart aggregates do not automatically become persisted Observations;
- high-frequency sampled data does not require one physical Observation row per tick;
- subject != observer != recorder != source/provider/device != authority != viewer;
- related shared context does not automatically make an Observation shared.

Next concept under review: **Confirmation**.

---

# Provisional future clusters

## Observed Reality & Evidence

Remaining likely concepts:

- Confirmation;
- Evidence;
- Provenance.

Cluster membership may still change as pairwise redundancy tests run.

## Data / Subjects

Likely includes:

- Register;
- Quantity;
- Asset;
- Subject;
- Person/Actor review;
- Resource.

Observation v0 creates mandatory re-tests for:

- Observation vs Quantity;
- Observation vs Register/RegisterEntry;
- subject/observer/recorder typing;
- high-volume sampled-series physical representation.

## Relationships / Reasoning

Likely includes:

- semantic Relationship;
- Dependency;
- Responsibility / Assignment / Hand-off;
- Contribution;
- Goal-to-Goal relationships;
- Evidence-to-Criterion relationships;
- Authority / Visibility review;
- Decision;
- Version;
- AI Proposal.

Cluster membership/naming remain provisional until individual review.

---

# Relationship to existing documentation

Older V1 product documents remain preserved while Domain Atlas terminology is promoted deliberately.

Current known differences include:

- older docs treat Goal/Program/Project as distinct canonical concepts; current kernel uses Goal + Plan while Project/Program remain product profiles unless later evidence justifies separation;
- Task remains contextual/user-facing Activity language;
- Event remains occurrence-centred and distinct from Schedule/attendance/Outcome;
- Routine remains repeated execution policy, distinct from Recurrence, observed habit, Schedule, Occurrence and Actual;
- Milestone remains contextual checkpoint, distinct from Goal/Outcome/Deadline/Event;
- Occurrence is stable expected-instance identity;
- Schedule is accepted temporal assignment, distinct from Constraint/Recurrence/Capacity/Actual;
- Session is actual execution episode, not planned placement or broader realization;
- Actual is the contextual realization record linking a specific expectation to realized reality;
- Outcome is a contextual result/disposition, not a universal completion/status field;
- Observation is the bounded contextual record for measurement/simple assertion, not a universal data row;
- Deadline is latest-bound Temporal Constraint semantics;
- Availability/Capacity/reservation semantics replace the assumption that every calendar-shaped item is a duplicate Calendar Block;
- Calendar Block remains useful product/UI vocabulary.

Do not silently rewrite historical product documents solely to make wording uniform. Current navigation/terminology references must instead make precedence explicit.

---

# Current concepts

- [`Goal v0`](concepts/goal.md) — accepted; multi-actor wording hardened 2026-08-11.
- [`Plan v0`](concepts/plan.md) — accepted.
- [`Activity v0`](concepts/activity.md) — accepted; multi-actor responsibility wording hardened 2026-08-11.
- [`Event v0`](concepts/event.md) — accepted; Time hardening retained.
- [`Routine v0`](concepts/routine.md) — accepted; progression + multi-actor performer wording hardened 2026-08-11.
- [`Milestone v0`](concepts/milestone.md) — accepted.
- [`Occurrence v0`](concepts/occurrence.md) — accepted.
- [`Schedule v0`](concepts/schedule.md) — accepted; postponed/TBD hardening retained.
- [`Session v0`](concepts/session.md) — accepted.
- [`Temporal Constraint v0`](concepts/temporal-constraint.md) — accepted.
- [`Recurrence v0`](concepts/recurrence.md) — accepted; quota/period hardening retained.
- [`Availability & Capacity v0`](concepts/availability-capacity.md) — accepted.
- [`Actual v0`](concepts/actual.md) — accepted under Methodology v3; contextual realization semantics.
- [`Outcome v0`](concepts/outcome.md) — accepted under Methodology v3; contextual result/disposition semantics.
- [`Observation v0`](concepts/observation.md) — accepted under Methodology v3; bounded measurement/simple-assertion semantics.

---

# Current structural direction

```text
Goal         -> what is wanted
Plan         -> how it is pursued/organized
Activity     -> what actionable work/behavior is intended
Event        -> what occurrence-centred thing is expected
Routine      -> what repeated behavioral/execution policy is intended
Milestone    -> what meaningful contextual checkpoint matters
Recurrence   -> how a repeated/generative pattern repeats
Occurrence   -> which expected generated instance exists
Constraint   -> where/when placement is allowed/required/preferred
Availability -> when schedulable capacity may be used
Capacity     -> ability to accept compatible commitments
Schedule     -> when execution/occurrence is currently accepted
Session      -> which bounded actual execution episode happened
Actual       -> how a specific expectation was realized in reality
Outcome      -> what result/disposition followed from that realization
Observation  -> what measurement/simple assertion applies to a subject/context
Evidence     -> information used in evaluation (future review)
```

Cross-cutting multi-actor direction:

```text
shared canonical fact
+
actor-scoped personal state

object identity
!= account
!= participation
!= responsibility
!= performer
!= subject
!= authority
!= visibility
```

This is a domain direction, not a persistence schema.

---

# Current modeling sequence

Current validated state:

```text
Intention & Execution v0        — PASS
Time v0                         — PASS
Cross-Cluster Validation v2     — PASS
Multi-Actor Evidence Synthesis  — PASS WITH HARDENING
Domain & Product Language Map   — ESTABLISHED
Validation Methodology v3       — ACTIVE MANDATORY STANDARD
Actual v0                       — PASS WITH HARDENING / ACCEPTED
Outcome v0                      — PASS WITH HARDENING / ACCEPTED
Observation v0                  — PASS WITH HARDENING / ACCEPTED

↓
Confirmation review
↓
Evidence / Provenance reviews
↓
Observed Reality & Evidence cluster integration
↓
cluster multi-actor stress
```

---

# Reopen watchlist

Deliberately revisit later:

- Actual vs Confirmation/Provenance;
- Outcome vs Confirmation/Provenance;
- Observation vs Evidence;
- Observation vs Confirmation/Provenance;
- Observation vs Quantity;
- Observation vs Register/RegisterEntry;
- subject vs observer/recorder/source semantics;
- Milestone vs Outcome vs GoalCriterion;
- competing contextual Outcome/Observation assertions under future authority rules;
- Plan vs Routine under complex progression/adaptation;
- Event participation vs personal commitment/delegation;
- collaborative Session vs actor-scoped Actual participation;
- completion-relative Recurrence vs Trigger/relative Constraint semantics;
- Availability/Capacity vs Resource model;
- Person/Actor/Subject/Account/Principal boundaries;
- Responsibility/Assignment/Hand-off/Stewardship boundaries;
- Authority vs Visibility vs governance relationships;
- typed/directional Relationship semantics;
- confirmation/acknowledgement/common-ground depth by consequence;
- AI context selection/inference privacy.

These are watch items, not current failures.

---

# Final validation rule

A final whole-domain stress test remains mandatory before broad persistence implementation.

Cluster PASS does not prevent later reopening when another cluster, physical data model, integration, implementation evidence, safety requirement or stronger real-world evidence exposes a genuine contradiction.