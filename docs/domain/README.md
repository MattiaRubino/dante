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

Default cycle:

1. inspect relevant LifeOS documentation and prior decisions;
2. inspect feature-discovery simulations and applicable real-life scenarios;
3. perform targeted external benchmark/research where mature systems, standards, APIs or research can expose missing semantics;
4. propose the smallest strong model explaining the evidence;
5. challenge the proposal with the user;
6. add adversarial/edge cases;
7. check consistency against accepted concepts;
8. run applicable multi-actor compatibility tests;
9. save only when coherent enough to become the current baseline.

Existing documentation and external systems are evidence, not authority. Contradictions must be surfaced rather than inherited silently.

---

# Validation Methodology v2

Reference:

- [`Validation Methodology v2`](validation-methodology-v2.md)
- [`Validation Methodology v2 — Multi-Actor Addendum`](validation-methodology-v2-multi-actor-addendum.md)

The methodology includes, where applicable:

- Real-World Workflow Inversion;
- deep chronological simulation;
- adversarial REMOVE / MERGE / SPLIT / UNIVERSALIZE / INVERT / EXTREME tests;
- semantic redundancy / merge-split analysis;
- downward composition;
- upward reconstruction from reality;
- lateral cross-domain propagation;
- orphan / independence testing;
- external cross-domain benchmarking;
- external anti-pattern review;
- scale/history stress;
- simple-user versus power-user validation;
- multi-actor identity/authority/privacy/burden testing;
- final cross-cluster consistency testing.

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

Checkpoint documents record scope, methodology, scenario matrix, failures/ambiguities, hardenings, remaining dependencies and PASS/FAIL result.

---

# Domain & Product Language Map

Canonical quick-reference terminology now lives in:

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

Examples:

- `Occurrence` is canonical but normally hidden behind `this time` / `this occurrence`;
- `Task` is product/UI language over Activity;
- `Project` and `Program` remain product-profile candidates over Plan semantics;
- `Calendar Block` remains product/UI language over Schedule/Availability/Capacity semantics where applicable.

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
9. multi-actor compatibility where applicable;
10. rejected alternatives;
11. deliberately deferred questions;
12. implications for future persistence/APIs.

Saving a concept does not permanently close it.

---

# Validation approach

Definitions are stress-tested across multiple life/work classes rather than one productivity workflow:

- everyday personal planning;
- study/learning;
- work/professional deadlines;
- health/fitness;
- finance/resource tracking;
- home/travel/assets/maintenance;
- creative work;
- caregiving/subject-based tracking;
- temporary disruption/unusual schedules;
- multi-actor social/household/team/professional coordination;
- mature external systems/research solving comparable hard problems.

Prefer a small set of strong primitives over overlapping nouns. A new entity requires materially different identity, lifecycle, authority, invariants, query behavior or other demonstrated semantics — not merely a familiar label.

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

The cluster later passed Validation Methodology v2 and the evidence-backed multi-actor synthesis.

Multi-actor wording was hardened on 2026-08-11 for:

- Goal;
- Activity;
- Routine.

This changes actor/governance assumptions, not the core primitive boundaries.

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

The cluster passed deep chronological, redundancy, reductio, traceability, benchmark, scale/history and simple/power-user tests.

Earlier hardenings:

1. quota Recurrence preserves an explicit-enough period frame where membership/boundary semantics matter; equivalent quota Occurrences do not gain arbitrary ordinal meaning;
2. materially changing long-horizon progression tends toward Plan rather than one mega-Routine;
3. Event identity/historical expectation may survive temporary absence of current Schedule when postponed/unresolved.

## Cross-cluster validation — VALIDATED CURRENT BASELINE

- [`Cross-Cluster Validation v2`](checkpoints/cross-cluster-validation-v2.md)

Result: all twelve concepts retained; no justified merge/removal; no universal hierarchy required; top-down planning, bottom-up reality capture and lateral relevance remain representable without rewriting historical intention.

## Multi-Actor Evidence Synthesis — VALIDATED CURRENT BASELINE

The completed collaboration simulation and independent external Deep Research were reconciled against the first two clusters.

References:

- [`Multi-Actor Readiness v1`](multi-actor-readiness-v1.md) — current normative guardrail;
- [`Multi-Actor Evidence Synthesis v0`](checkpoints/multi-actor-evidence-synthesis-v0.md) — validation record;
- [`Multi-Actor Readiness v0`](multi-actor-readiness-v0.md) — preserved earlier pre-research baseline/history;
- [`Discovery Simulation`](../product/multi-actor-collaboration-discovery-simulation-2026-08.md);
- [`External Deep Research`](../product/multi-actor-collaboration-research-2026-08.md).

Result:

```text
Intention & Execution v0 — PASS
Time v0                 — PASS
Multi-Actor Readiness   — PASS WITH EVIDENCE-BACKED HARDENING

Structural reopenings   — 0
Concept removals         — 0
Concept merges           — 0
Mandatory new primitives — 0
```

Promoted guardrails include:

- shared canonical fact + actor-scoped personal overlay;
- Account/Person/Actor/Subject must not be collapsed;
- Activity identity != requester/assignee/performer;
- participation response != Actual participation;
- accepted Schedule != participant acceptance;
- responsibility is richer than one assignee;
- assignment does not prove coordination-stewardship/mental-load transfer;
- delivery/acknowledgement/agreement/authority/Actual may differ;
- useful coordination may use private-derived projections without source disclosure;
- privacy includes inference/explanation/tool boundaries;
- creator != automatic social authority;
- access lifecycle/revocation != historical attribution;
- partial/external/assisted participation is normal;
- coordination burden must be evaluated per actor;
- AI knowledge != disclosure permission and AI authority remains bounded.

No Actor/Team/Organization/ACL/Stewardship primitive is pre-approved by this evidence.

---

# Provisional future clusters

## Observed Reality & Evidence

Likely includes:

- Actual;
- Outcome;
- Confirmation;
- Observation;
- Evidence;
- Provenance.

## Data / Subjects

Likely includes:

- Register;
- Quantity;
- Asset;
- Subject;
- Person/Actor review;
- Resource.

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

The project still does **not** automatically begin the next cluster merely because the first two are validated. User-led architecture/product brainstorming and explicit sequencing remain part of the agreed workflow.

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
- Session is actual execution episode, not planned placement;
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
Actual       -> broader reality of what happened (future review)
Evidence     -> what supports evaluation (future review)
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

Important consequences:

- Project/Program remain product profiles unless later proven distinct;
- Task remains Activity-facing UI language;
- observed habit/pattern does not automatically become Routine;
- placing Activity at exact time does not make it Event;
- Event state, participation response, attendance and Outcome remain separable;
- Routine, Recurrence, Occurrence, Schedule, Session and Actual remain distinct;
- Occurrence identity survives placement/assignment changes;
- accepted Schedule does not imply all participants accepted;
- Schedule presence does not imply Capacity consumption;
- private source facts can support authorized derived projections without source disclosure;
- creator/participant/visibility do not imply authority;
- coordination burden/mental load is not proved transferred by assignment;
- historical participation does not imply future access;
- AI access does not create disclosure permission or social authority;
- progressive disclosure is mandatory: kernel precision must not become casual-user bureaucracy.

---

# Current modeling sequence

Current validated state:

```text
Intention & Execution v0       — PASS
Time v0                        — PASS
Cross-Cluster Validation v2   — PASS
Multi-Actor Evidence Synthesis — PASS WITH HARDENING
Domain & Product Language Map — ESTABLISHED

↓
USER-LED BRAINSTORMING / QUESTIONS / ADDITIONAL TESTS

↓ only after explicit decision
select next Domain Atlas cluster
```

The workstream must not automatically proceed to `Actual / Outcome / Evidence` merely because this hardening is complete.

---

# Reopen watchlist

Deliberately revisit later:

- Milestone vs Outcome vs GoalCriterion;
- Plan vs Routine under complex progression/adaptation;
- Event participation vs personal commitment/delegation;
- Session vs broader Actual and actor-specific execution attribution;
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