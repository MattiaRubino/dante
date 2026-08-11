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

Current intended checkpoint structure:

### Intention and execution

Current baseline set:

- Goal;
- Plan;
- Activity;
- Event;
- Routine;
- Milestone.

Milestone was added after the first cluster checkpoint exposed a real semantic gap between work/occurrence and a meaningful contextual checkpoint. The cluster must now receive one final combined validation pass before it is marked validated.

### Time

Likely includes Schedule, Occurrence, Session, recurrence, deadline/window semantics, and temporal constraints.

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
- `Milestone v0` treats significant checkpoints as contextual entities distinct from Goal, GoalCriterion, Activity, Event, Outcome, Deadline, Phase, and Decision Record.

## Current concepts

- [`Goal v0`](concepts/goal.md) — current baseline accepted on 2026-08-10.
- [`Plan v0`](concepts/plan.md) — current baseline accepted on 2026-08-10.
- [`Activity v0`](concepts/activity.md) — current baseline accepted on 2026-08-10.
- [`Event v0`](concepts/event.md) — current baseline accepted on 2026-08-10.
- [`Routine v0`](concepts/routine.md) — current baseline accepted on 2026-08-10.
- [`Milestone v0`](concepts/milestone.md) — current baseline accepted on 2026-08-11.

## Current structural direction

```text
Goal      -> what is wanted
Plan      -> how it is intended to be pursued or organized
Activity  -> what concrete action is intended
Event     -> what occurrence is expected at an intrinsic temporal placement
Routine   -> what recurring behavioral/execution policy is intended
Milestone -> what meaningful contextual checkpoint is expected/reached
Schedule  -> when concrete execution is planned or an occurrence is currently expected
Actual    -> what actually happened
Evidence  -> what supports evaluation
```

This is a working domain direction, not yet a persistence schema.

Important current consequences:

- `Project` and `Program` remain specialization/product-language candidates rather than assumed independent aggregate roots;
- `Task` is not currently a second primitive beside Activity;
- placing an Activity at an exact time does not transform it into an Event;
- Event state, participant response, actual attendance, and Event outcome are distinct dimensions;
- original temporal expectation, current accepted schedule, and actual occurrence must remain distinguishable;
- actual start/end can deviate from schedule in either direction; early/late/overrun semantics are derived rather than fundamental Event state;
- Routine is not `repeat=true`; the recurring policy, expected occurrence, scheduling, and Actual execution must remain distinguishable;
- recurring Event series and Routine are distinct even when both use recurrence machinery;
- a one-off Routine occurrence change must not silently change the future Routine policy;
- Milestone is not executable work or a time-centred occurrence; it records a meaningful contextual checkpoint becoming true;
- target expectation and actual Milestone achievement remain distinct, and target dates do not automatically become deadlines;
- completing an Activity or crossing a metric threshold does not automatically create a Milestone;
- Goal progress/evaluation must be able to use valid evidence even when the evidence came from an Activity, Event, Routine occurrence, Milestone, or observation that was not originally planned for that Goal;
- discovered relevance must not rewrite historical intention;
- Goal-to-Goal influence is a real requirement but its formal semantics are deferred to the Relationship Model rather than reduced to a generic `influences` field;
- availability/capacity, exact occurrence materialization, recurrence/DST, and generated execution remain deliberately open for the temporal cluster.

## Current modeling sequence

The first **intention/execution cluster checkpoint** has identified and filled one real semantic gap by accepting Milestone v0.

The immediate next step is a final combined checkpoint over:

```text
Goal
Plan
Activity
Event
Routine
Milestone
```

The checkpoint must test the six baselines together against the same representative scenarios and adversarial mixed cases.

It should specifically look for:

- duplicated representations of the same real-world thing;
- cases where two primitives cannot be distinguished naturally;
- forced parent/child hierarchies that do not fit real life;
- planned versus actual/history leakage;
- recurrence versus occurrence confusion;
- evidence that cannot reach relevant Goal criteria cleanly;
- Activity/Plan and Routine/Plan boundary failures;
- recurring Activity versus recurring Event ambiguity;
- Milestone versus Goal/GoalCriterion/Outcome ambiguity;
- scenarios that would require arbitrary JSON or domain-specific tables merely to work.

If the combined checkpoint passes without reopening a baseline, the intention/execution cluster can be marked validated and the next modeling cluster is Time, beginning with `Occurrence`.