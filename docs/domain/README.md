# LifeOS Domain Atlas

**Status:** In progress  
**Started:** 2026-08-10  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

The Domain Atlas is the working source for re-evaluating and defining LifeOS domain concepts before broad persistence or backend implementation.

Its job is not to preserve earlier terminology by inertia. Its job is to produce the strongest current domain model we can justify from product intent, real-world scenarios, external patterns, implementation constraints, and explicit reasoning.

## Decision rule

In this workstream, **accepted means current best decision, not immutable decision**.

A concept may be reopened when new scenarios, evidence, implementation constraints, contradictions, or better abstractions emerge. Changes must be deliberate and documented; prior reasoning must not be silently overwritten.

Earlier product documents, simulations, glossaries, ADRs, prototypes, and conversation history are inputs to re-evaluate. They are not automatically treated as correct merely because they were written earlier.

Where an accepted ADR defines a broader architectural constraint, this workstream should respect it unless new evidence is strong enough to justify an explicit ADR change.

## Mandatory concept-review protocol

Every Domain Atlas concept must be reviewed against more than the immediately preceding discussion before it is accepted.

The default review cycle is:

1. inspect relevant existing LifeOS documentation and prior decisions;
2. inspect the feature-discovery simulation and other applicable real-user scenarios;
3. perform a targeted external benchmark/research pass where comparable mature systems, standards, APIs, or research can expose missing semantics;
4. propose the smallest strong domain model that explains the evidence;
5. review and challenge the proposal with the user;
6. add edge cases and intentionally difficult scenarios;
7. check consistency against already accepted Domain Atlas concepts;
8. save the concept only when it is coherent enough to be the current baseline.

Existing documentation and external products are evidence, not authority. Contradictions must be surfaced rather than inherited silently.

A full external research pass does not need to repeat identical stable evidence for every adjacent concept, but each concept must receive enough targeted validation to expose likely missing cases.

## External benchmark and interoperability rule

External standards, products, APIs, and schemas are **benchmark evidence, not design authorities**.

LifeOS should adopt an external pattern when it improves the internal model or provides useful interoperability at negligible conceptual cost. The domain model must not be weakened, distorted, or made more complex merely to match another platform's schema or limitations.

The preferred direction is:

```text
LifeOS semantics
        ↓
strong internal model
        ↓
optional adapters / mappings
        ↓
external standards and providers
```

not:

```text
external schema
        ↓
LifeOS kernel must imitate it
```

Consequences:

- external systems may expose real edge cases and useful patterns;
- provider-specific identifiers, recurrence formats, status taxonomies, or persistence shapes do not become LifeOS identity by default;
- lossless mapping to an external format is not a kernel invariant;
- integration adapters should absorb provider-specific mapping, controlled degradation, or incompatibility when that is preferable to weakening LifeOS semantics;
- interoperability is desirable when useful, but LifeOS semantics remain primary.

## Documentation standard

Canonical Domain Atlas documentation is written in **English**.

Conversation and review may occur in another language, but the repository keeps one canonical version rather than maintaining duplicated translations that could diverge.

Each accepted concept should document, where relevant:

- canonical definition;
- why the concept exists;
- validation basis;
- boundaries against adjacent concepts;
- identity and ownership/context;
- lifecycle and temporal semantics;
- planned/current/actual/history distinctions;
- evidence/provenance implications;
- representative and adversarial examples;
- invariants;
- alternatives considered/rejected;
- questions intentionally deferred;
- implications for future persistence/API design without prematurely fixing physical tables.

Checkpoint documents should record scope, methodology, scenario matrix, boundary results, ambiguities/failures, changes made, remaining dependencies, and PASS/FAIL status.

## Working method

Concepts are reviewed one at a time.

For each concept we aim to establish:

1. canonical definition;
2. what the concept is and is not;
3. identity and ownership;
4. lifecycle and temporal semantics;
5. invariants;
6. relationships to other concepts;
7. evidence, provenance, and derived state where relevant;
8. real-world and edge-case coverage;
9. alternatives considered and why they are not preferred;
10. open questions intentionally deferred;
11. implications for future persistence and APIs without prematurely designing tables.

A concept is saved when it is coherent enough to be the current baseline. Saving it does not make it permanently closed.

## Validation approach

Definitions should be stress-tested against multiple classes of use rather than one productivity workflow. Relevant evidence includes:

- existing LifeOS product simulations and requirements;
- everyday personal planning;
- study and learning;
- work and professional deadlines;
- health and fitness;
- finance and resource tracking;
- home, travel, assets, and maintenance;
- creative work;
- caregiving and subject-based tracking;
- temporary disruptions and unusual schedules;
- patterns from mature external systems where they solve a comparable problem.

We should prefer a small set of strong primitives over many overlapping nouns. A new domain entity should exist because it has materially different identity, lifecycle, invariants, or behavior—not merely because another productivity product uses that label.

## Cluster checkpoints

Concept-by-concept validation is necessary but not sufficient. After a small group of strongly related primitives is defined, the group must be stress-tested together before the Domain Atlas moves too far downstream.

### Intention and execution — VALIDATED CURRENT BASELINE

Validated on 2026-08-11.

Current validated set:

- Goal;
- Plan;
- Activity;
- Event;
- Routine;
- Milestone.

The combined checkpoint passed after Milestone filled the one material gap exposed by the first pass. No current baseline needs to be reopened before the Time cluster.

Checkpoint record:

- [`Intention & Execution Cluster v0`](checkpoints/intention-execution-v0.md)

Validation is provisional in the Domain Atlas sense: downstream temporal, evidence, relationship, persistence, or implementation work may still reopen a concept if new evidence exposes a contradiction.

### Time — CURRENT CLUSTER

Current accepted baselines:

- Occurrence v0;
- Schedule v0;
- Session v0;
- Temporal Constraint v0;
- Recurrence v0.

Next review block:

- Calendar Block / Availability / Capacity.

Occurrence v0 establishes stable logical identity for one expected generated/recurring instance without forcing every one-off Activity/Event into an Occurrence wrapper and without requiring infinite eager materialization of future instances.

Schedule v0 establishes accepted temporal assignment as a separate capability rather than collapsing deadlines, constraints, recurrence, capacity, movement authority, and Actual execution into one calendar object.

Session v0 establishes actual execution episode identity as distinct from planned Schedule placement, expected Occurrence identity, Event attendance, and broader Actual/Outcome semantics.

Temporal Constraint v0 establishes temporal admissibility/preference as a general rule capability: deadlines are latest-bound constraints and windows are range-shaped expressions whose semantics depend on whether they are hard validity rules, soft preferences, targets, availability, or accepted Schedule placement.

Recurrence v0 establishes structured repeating-pattern semantics separately from Routine/Event identity, Occurrence identity, Schedule, Actual, Temporal Constraint, and generic Trigger behavior. It supports exact calendar patterns, quota-based expectations, elapsed intervals, completion-relative chains, anchor-stream mappings, and cycles without requiring all patterns to resolve to exact timestamps in advance.

### Observed reality and evidence

Likely includes Actual, Outcome, Confirmation, Observation, Evidence, and Provenance.

### Data and subjects

Likely includes Register, Quantity, Asset, Subject, Resource, and related measurement semantics.

### Relationships and reasoning

Likely includes semantic relationships, dependencies, contribution, Goal-to-Goal interactions, evidence-to-criterion relations, Decision, Version, and AI proposal boundaries.

Cluster membership is provisional and may change as concepts are reviewed.

At each checkpoint, representative feature-discovery scenarios must be reconstructed using only the model accepted so far. Repeated duplication, ambiguous ownership, hidden history rewrites, arbitrary JSON escape hatches, or excessive special cases are signals to reopen earlier concepts.

A final whole-domain stress test is required before broad SQL/persistence implementation.

## Relationship to existing documentation

Existing product documents remain preserved as historical and product-definition inputs while this pass is underway.

When a Domain Atlas concept conflicts with an older definition, the conflict must be made explicit. The older document should not be silently rewritten until the impact is understood and the newer domain decision is ready to propagate.

Current known examples:

- existing documentation treats `Goal`, `Program`, and `Project` as distinct canonical concepts;
- `Goal v0` broadened Goal semantics and reopened `Project` for revalidation;
- `Plan v0` provides the current execution-strategy primitive and does not accept `Project` or `Program` as separate kernel primitives unless later review demonstrates materially distinct identity, lifecycle, or invariants;
- `Activity v0` keeps `Task` as a contextual/user-facing form of Activity rather than a separate primitive and makes planned execution, Actual execution, and evidence separate semantics;
- `Event v0` strengthens the Activity/Event boundary by treating temporal placement as intrinsic to Event meaning while preserving original expectation, current accepted schedule, actual occurrence, participation, attendance, and provenance as distinct semantics;
- `Routine v0` treats recurring behavior as persistent policy distinct from recurrence syntax, concrete schedule, generated occurrence, and Actual execution; recurring Event series remain Event semantics rather than being forced into Routine;
- `Milestone v0` treats significant checkpoints as contextual entities distinct from Goal, GoalCriterion, Activity, Event, Outcome, Deadline, Phase, and Decision Record;
- `Occurrence v0` introduces stable logical identity for one expected recurring/generated instance while keeping source policy, Schedule, Session, Activity/Event semantics, and Actual distinct;
- `Schedule v0` treats accepted temporal assignment as distinct from the schedulable subject, Actual execution, deadlines/targets, windows/constraints, recurrence, movement policy, and availability/capacity;
- `Session v0` treats actual execution episodes as distinct from planned placements, Occurrence identity, Activity identity, Event actual occurrence, and broader Actual/Outcome semantics;
- `Temporal Constraint v0` replaces the assumption that Deadline and Window require parallel kernel primitives: Deadline is a latest-bound Temporal Constraint, while range/window semantics are typed by purpose and remain distinct from Schedule, target, availability, and Actual;
- `Recurrence v0` treats recurrence as a structured reusable repeating-pattern capability rather than RRULE/provider syntax, Routine identity, Event identity, Occurrence identity, Schedule, or generic Trigger logic; external recurrence formats remain optional adapter targets rather than kernel authorities.

## Current concepts

- [`Goal v0`](concepts/goal.md) — current baseline accepted on 2026-08-10.
- [`Plan v0`](concepts/plan.md) — current baseline accepted on 2026-08-10.
- [`Activity v0`](concepts/activity.md) — current baseline accepted on 2026-08-10.
- [`Event v0`](concepts/event.md) — current baseline accepted on 2026-08-10.
- [`Routine v0`](concepts/routine.md) — current baseline accepted on 2026-08-10.
- [`Milestone v0`](concepts/milestone.md) — current baseline accepted on 2026-08-11.
- [`Occurrence v0`](concepts/occurrence.md) — current baseline accepted on 2026-08-11.
- [`Schedule v0`](concepts/schedule.md) — current baseline accepted on 2026-08-11.
- [`Session v0`](concepts/session.md) — current baseline accepted on 2026-08-11.
- [`Temporal Constraint v0`](concepts/temporal-constraint.md) — current baseline accepted on 2026-08-11.
- [`Recurrence v0`](concepts/recurrence.md) — current baseline accepted on 2026-08-11.

## Current structural direction

```text
Goal       -> what is wanted
Plan       -> how it is intended to be pursued or organized
Activity   -> what concrete action is intended
Event      -> what occurrence-centred thing is expected to happen
Routine    -> what recurring behavioral/execution policy is intended
Milestone  -> what meaningful contextual checkpoint is expected/reached
Recurrence -> how a recurring/generative pattern repeats
Occurrence -> which individual expected instance exists in a recurring/generated context
Constraint -> where/when execution is allowed, required, bounded, or preferred
Schedule   -> when execution/occurrence is currently accepted to happen
Session    -> which bounded actual execution episode happened
Actual     -> broader truth about what happened
Evidence   -> what supports evaluation
```

This is a working domain direction, not yet a persistence schema.

Important current consequences:

- `Project` and `Program` remain specialization/product-language candidates rather than assumed independent aggregate roots;
- `Task` is not currently a second primitive beside Activity;
- placing an Activity at an exact time does not transform it into an Event;
- Event state, participant response, actual attendance, and Event outcome are distinct dimensions;
- original temporal expectation, current accepted Schedule, Session timing, and broader Actual remain distinguishable;
- actual start/end can deviate from Schedule in either direction; early/late/overrun semantics are derived rather than fundamental state;
- Routine is not `repeat=true`; recurring policy, Recurrence, expected Occurrence, scheduling, Sessions, and broader Actual execution remain distinguishable;
- recurring Event series and Routine are distinct even when both use recurrence machinery;
- a one-off Routine occurrence change must not silently change future Routine policy;
- Milestone is not executable work or a time-centred occurrence; it records a meaningful contextual checkpoint becoming true;
- Recurrence is structured repeating-pattern semantics, not a provider recurrence string or generic automation engine;
- Recurrence may produce logical/quota Occurrences without assigning exact timestamps;
- calendar/wall-clock recurrence remains distinct from elapsed-duration recurrence;
- fixed independent cadence remains distinct from completion-relative chaining;
- source pattern anchor remains distinct from the effective recurrence range;
- recurrence-count semantics describe expected Occurrences, not successful completions;
- recurring Temporal Constraints may reuse recurrence-pattern machinery without becoming occurrence-generating sources;
- structural recurrence changes are effective future revisions rather than retroactive rewrites;
- Occurrence identity does not depend on current start/end or resolved UTC instant;
- not every one-off Activity or Event receives a redundant Occurrence wrapper;
- Occurrence may exist before exact Schedule placement;
- future Occurrences may remain virtual until instance-specific history requires persistent reconstruction;
- Schedule is accepted temporal assignment, not a container for every temporal fact;
- Activity may exist without Schedule, and an Occurrence may exist before exact Schedule assignment;
- Schedule revision does not change subject identity and actual Session deviation does not silently rewrite Schedule;
- Schedule may preserve coarse/date-based/floating/zoned/instant semantics rather than inventing exact UTC precision;
- multiple planned placements may support one divisible Activity/Occurrence while remaining distinct from actual Sessions;
- Session is actual execution, not planned execution;
- one Activity/Occurrence may have zero, one, or many Sessions;
- a pause may remain inside one Session, while explicit end and later restart normally creates another Session;
- elapsed, active, and paused Session time remain conceptually distinct;
- ending a Session does not imply Activity/Occurrence completion;
- Session may exist without prior Schedule and may record spontaneous work without fabricating historical intent;
- Event actual occurrence/attendance does not receive a redundant Session by default;
- Session measurements/Observations remain related data rather than arbitrary metadata blobs;
- Session overlaps are not globally forbidden and analytics must not naïvely sum overlapping elapsed time;
- Temporal Constraint is distinct from Schedule, Session/Actual, Recurrence, Availability/Capacity, and Movement Policy;
- Deadline is a latest-bound Temporal Constraint semantic specialization, not a separate kernel primitive;
- a range/window can represent hard validity, soft preference, target, availability, or accepted placement depending on semantic context;
- target dates/windows and review dates do not automatically become scheduling constraints;
- hard constraints define planning admissibility but do not prevent recording Actual reality that violates them;
- hard/soft strength is separate from authority/mutability;
- a passed deadline does not automatically establish `missed` or failure outcome;
- multiple hard constraints must be jointly satisfiable or planning is infeasible rather than silently inconsistent;
- constraints may be boundary-, range-, duration-, spacing-, exclusion-, or relation-based;
- constraints may operate at broader scopes and receive occurrence-specific exceptions without physical duplication or silent source-policy rewrite;
- external standards and products remain benchmark evidence and optional mapping targets, not design authorities;
- Goal progress/evaluation must be able to use valid evidence regardless of whether the source execution was originally linked to that Goal;
- discovered relevance must not rewrite historical intention;
- Goal-to-Goal influence remains deferred to the Relationship Model.

## Current modeling sequence

The **Intention & Execution Cluster v0 is validated** as the current baseline.

The workstream is now in the **Time cluster**.

Current sequence:

```text
Occurrence v0 — accepted
→ Schedule v0 — accepted
→ Session v0 — accepted
→ Temporal Constraint v0 — accepted
→ Recurrence v0 — accepted
→ Calendar Block / Availability / Capacity — next review
```

The sequence is not immutable. A reviewed concept may expose a stronger dependency and reorder adjacent concepts.

## Open temporal questions entering Calendar Block / Availability / Capacity review

The accepted Time concepts intentionally leave the following issues for the final adjacent review block:

- whether Calendar Block is an independent kernel primitive, a Schedule/Capacity specialization, or primarily a product/UI construct;
- how user Availability differs from scheduled occupancy, hard Temporal Constraints, preferences, and external free/busy data;
- what `busy`, `free`, `tentative`, `focus`, and protected time mean semantically;
- whether every scheduled Event/Activity consumes capacity automatically or capacity consumption must remain explicit;
- how partial capacity and multi-resource capacity are represented;
- whether simultaneous compatible activities can share capacity;
- personal attention capacity versus physical/resource capacity;
- external calendar busy time versus LifeOS semantic availability;
- recurring Availability/Capacity patterns and how they reuse Recurrence without becoming occurrence-generating sources unnecessarily;
- capacity exceptions and temporary modes such as travel, illness, holidays, or disrupted weeks;
- conflict detection among Schedule placements, Temporal Constraints, and available Capacity;
- whether capacity reservation itself has identity/history;
- relation of Calendar Block to Activity/Event identity and whether a block without work semantics is still useful;
- exact provider free/busy mapping without making provider semantics authoritative;
- exact persistence/API representation for Time-cluster baselines;
- whether this final review exposes any need to reopen Occurrence, Schedule, Session, Temporal Constraint, or Recurrence before the Time-cluster checkpoint.

## Final validation rule

A final whole-domain stress test remains mandatory before broad persistence implementation. A cluster PASS does not prevent later reopening when another cluster exposes a contradiction.