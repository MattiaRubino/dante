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
- Schedule v0.

Next concept under review:

- Session.

Likely later concepts include Deadline / Window / Temporal Constraint, Recurrence, and Calendar Block / Availability / Capacity.

Occurrence v0 establishes stable logical identity for one expected generated/recurring instance without forcing every one-off Activity/Event into an Occurrence wrapper and without requiring infinite eager materialization of future instances.

Schedule v0 establishes accepted temporal assignment as a separate capability rather than collapsing deadlines, constraints, recurrence, capacity, movement authority, and Actual execution into one calendar object.

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
- `Schedule v0` treats accepted temporal assignment as distinct from the schedulable subject, Actual execution, deadlines/targets, windows/constraints, recurrence, movement policy, and availability/capacity.

## Current concepts

- [`Goal v0`](concepts/goal.md) — current baseline accepted on 2026-08-10.
- [`Plan v0`](concepts/plan.md) — current baseline accepted on 2026-08-10.
- [`Activity v0`](concepts/activity.md) — current baseline accepted on 2026-08-10.
- [`Event v0`](concepts/event.md) — current baseline accepted on 2026-08-10.
- [`Routine v0`](concepts/routine.md) — current baseline accepted on 2026-08-10.
- [`Milestone v0`](concepts/milestone.md) — current baseline accepted on 2026-08-11.
- [`Occurrence v0`](concepts/occurrence.md) — current baseline accepted on 2026-08-11.
- [`Schedule v0`](concepts/schedule.md) — current baseline accepted on 2026-08-11.

## Current structural direction

```text
Goal       -> what is wanted
Plan       -> how it is intended to be pursued or organized
Activity   -> what concrete action is intended
Event      -> what occurrence-centred thing is expected to happen
Routine    -> what recurring behavioral/execution policy is intended
Milestone  -> what meaningful contextual checkpoint is expected/reached
Occurrence -> which individual expected instance exists in a recurring/generated context
Schedule   -> when execution/occurrence is currently accepted to happen
Session    -> actual execution slice (next review)
Actual     -> what actually happened
Evidence   -> what supports evaluation
```

This is a working domain direction, not yet a persistence schema.

Important current consequences:

- `Project` and `Program` remain specialization/product-language candidates rather than assumed independent aggregate roots;
- `Task` is not currently a second primitive beside Activity;
- placing an Activity at an exact time does not transform it into an Event;
- Event state, participant response, actual attendance, and Event outcome are distinct dimensions;
- original temporal expectation, current accepted Schedule, and Actual occurrence must remain distinguishable;
- actual start/end can deviate from Schedule in either direction; early/late/overrun semantics are derived rather than fundamental state;
- Routine is not `repeat=true`; recurring policy, expected occurrence, scheduling, and Actual execution remain distinguishable;
- recurring Event series and Routine are distinct even when both use recurrence machinery;
- a one-off Routine occurrence change must not silently change future Routine policy;
- Milestone is not executable work or a time-centred occurrence; it records a meaningful contextual checkpoint becoming true;
- Occurrence identity does not depend on current start/end or resolved UTC instant;
- not every one-off Activity or Event receives a redundant Occurrence wrapper;
- Occurrence may exist before exact Schedule placement;
- Schedule is accepted temporal assignment, not a container for every temporal fact;
- Activity may exist without Schedule, and an Occurrence may exist before exact Schedule assignment;
- Schedule revision does not change subject identity and Actual deviation does not silently rewrite Schedule;
- Schedule may preserve coarse/date-based/floating/zoned/instant semantics rather than inventing exact UTC precision;
- multiple planned placements may support one divisible Activity/Occurrence while remaining distinct from Actual Sessions;
- having a Schedule does not imply that the interval consumes availability/capacity;
- deadlines, target dates, temporal windows/constraints, recurrence, movement policy, and availability/capacity remain separate adjacent concerns;
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
→ Session — next review
→ Deadline / Window / Temporal Constraint
→ Recurrence
→ Calendar Block / Availability / Capacity
```

The sequence is not immutable. A reviewed concept may expose a stronger dependency and reorder adjacent concepts.

## Open temporal questions entering Session review

Occurrence v0 and Schedule v0 intentionally leave the following issues for adjacent concepts:

- what exactly constitutes a Session;
- whether Session is always Actual execution or can also represent planned execution slices;
- whether one Activity/Occurrence/Event can have zero, one, or multiple Sessions;
- how pauses/resumes affect Session identity;
- whether a timer pause creates a new Session or remains inside one Session with pause intervals;
- how Session relates to Actual, Outcome, attendance, and measurements;
- whether one actual Session can realize more than one planned placement or more than one Activity;
- how interrupted/resumed work is represented without fabricating new Activities/Occurrences;
- how actual time captured manually differs from stopwatch/timer-derived time;
- how corrections to Session start/end preserve provenance/history;
- exact Deadline / Window / Temporal Constraint semantics;
- hard versus soft temporal constraints;
- Recurrence and timezone/DST/travel behavior;
- Calendar Block / Availability / Capacity semantics;
- exact Schedule placement/revision persistence;
- exact Occurrence materialization persistence.

## Final validation rule

A final whole-domain stress test remains mandatory before broad persistence implementation. A cluster PASS does not prevent later reopening when another cluster exposes a contradiction.
