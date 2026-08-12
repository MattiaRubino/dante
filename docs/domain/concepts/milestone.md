# Milestone v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-11  
**Meaning of accepted:** best current decision; reopenable with better evidence  
**Workstream:** Core Domain Model v0

## Canonical definition

> **A Milestone is a persistent contextual checkpoint representing a meaningful state, achievement, decision, delivery, or transition whose attainment matters within a broader Goal or Plan. A Milestone marks that something significant has become true; it does not represent the work performed, the occurrence in which it happened, or the temporal constraint by which it was expected.**

A Milestone is intentionally contextual. Its meaning normally exists because a larger Goal, Plan, or both make that checkpoint significant.

Examples include:

- design approved;
- B1 reached during a broader B2 journey;
- master version locked;
- release live on distribution platforms;
- first job offer received;
- visa issued;
- architecture selected;
- emergency fund threshold intentionally designated as a checkpoint.

## Why this concept exists

The first intention/execution cluster checkpoint exposed cases that are not naturally represented by Goal, Plan, Activity, Event, or Routine alone.

Example:

```text
Goal
Rebuild personal website

Plan
Design -> development -> launch

Activity
Prepare design mockup

Event
Design review

Milestone
Design approved
```

The review may occur without the design being approved. The Activity may be completed without the checkpoint being reached. The checkpoint therefore carries distinct semantics.

The existing Goal model already requires milestone/checkpoint evaluation semantics, and Plan already needs to coordinate milestones, but neither concept by itself represents the identity and history of a meaningful checkpoint that can be reached through multiple possible sources of evidence.

## Milestone is contextual rather than a general standalone objective

A Milestone normally needs meaningful context from at least one Goal or Plan.

```text
Goal
Reach spoken English B2

Milestone
B1 reached

Plan
Six-month English plan
```

The same Milestone may matter to both the Goal and the Plan.

LifeOS should not require a rigid parent tree. Conceptually a Milestone may relate to one or more Goals and/or Plans.

However, a completely isolated checkpoint with its own strategy, lifecycle, evaluation criteria, and independent importance should be reconsidered as a Goal rather than preserved as a context-free Milestone.

Current rule:

> **If an outcome has independent strategic meaning and can naturally be pursued on its own, it tends toward Goal. If its meaning is primarily as a significant checkpoint inside a broader path, it tends toward Milestone.**

## Milestone versus Goal

A Goal defines what the user wants to reach, change, maintain, reduce, produce, or sustain.

A Milestone marks a meaningful intermediate or structural checkpoint within a broader Goal or Plan.

```text
Goal
Reach spoken English B2

Milestones
- A2 consolidated
- B1 reached
- B2 mock exam passed
```

If `Reach B1` itself becomes independently important and receives its own strategy and evaluation, it can instead be modeled as a Goal.

Therefore:

> **Milestone != Goal.**

## Milestone versus GoalCriterion

A GoalCriterion defines how a Goal is evaluated.

A Milestone is a checkpoint that can actually be reached and whose attainment can have its own history, evidence, provenance, and target expectation.

Example:

```text
Goal
Publish album

Criterion
Release-live Milestone must be reached

Milestone
Release live on distribution platforms
```

The Criterion says how the Goal is evaluated. The Milestone represents the checkpoint itself.

Therefore:

> **Milestone != GoalCriterion.**

A Criterion may reference or depend on one or more Milestones without the two concepts becoming identical.

## Milestone versus Activity

An Activity represents executable intended work.

A Milestone represents a significant state or checkpoint becoming true.

```text
Activity
Finalize the master

Actual / Outcome
Master completed and approved

Milestone
Master locked
```

Completing an Activity does not automatically create or reach a Milestone. Only meaningful checkpoints should be represented as Milestones.

Therefore:

> **Milestone != Activity.**

## Milestone versus Event

An Event represents an occurrence whose temporal placement is intrinsic to its meaning.

A Milestone represents a significant state or checkpoint that may or may not be reached during that Event.

```text
Event
Design review
15 September 15:00

Outcome
Changes requested

Milestone
Design approved
not reached
```

The Event can happen while the Milestone remains unreached.

Therefore:

> **Milestone != Event.**

## Milestone versus Outcome

An Outcome records what resulted from a particular execution or occurrence.

A Milestone is a contextual checkpoint that an Outcome may help satisfy.

```text
Event
Exam

Outcome
Passed

Evidence
Pass result

Milestone
Certification checkpoint reached
```

A Milestone may also be reached by evidence that does not come from a single Activity or Event.

Examples include an external approval, an imported status, a document arriving, a threshold being reached, or an explicit user declaration.

Therefore:

> **Milestone != Outcome.**

## Milestone versus Deadline

A Milestone can have a target date or target window, but that expectation is not automatically a hard deadline.

```text
Milestone
Master approved

Target date
15 September

Actual achievement
18 September
```

The checkpoint was reached three days after the target. The target date passing did not itself determine success or failure.

A Deadline is a temporal constraint; Milestone is the checkpoint.

Therefore:

> **Milestone != Deadline.**

## Milestone versus Phase

A Phase represents a segment of a Plan.

A Milestone may mark a meaningful transition between phases without being the phase itself.

```text
Phase
Design

Milestone
Design approved

Phase
Development
```

Not every phase must end with a Milestone and not every Milestone must correspond to a phase transition.

Therefore:

> **Milestone != Phase.**

## Milestone versus Decision Record

A Decision Record preserves what was decided, why, by whom or what, when it became effective, and what it affected.

A decision may cause or support a Milestone.

```text
Decision Record
Use PostgreSQL as primary database

Milestone
Primary architecture selected
```

The Decision Record preserves reasoning. The Milestone marks the checkpoint.

Therefore:

> **Milestone != Decision Record.**

## Meaningful checkpoint, not automatic duplication

LifeOS must not automatically convert every completed Activity, reached metric, or threshold into a Milestone.

Examples:

```text
Activity
Buy domain
completed
```

does not automatically require:

```text
Milestone
Domain bought
```

unless domain acquisition is intentionally significant to the broader path.

Similarly:

```text
Goal
Save EUR 20,000

Current amount
EUR 5,000
```

should not automatically create a Milestone at EUR 5,000 merely because it represents 25% progress.

If the user deliberately defines:

```text
Milestone
Emergency reserve reaches EUR 5,000
```

then it is a real checkpoint.

The distinction is semantic and intentional, not purely mathematical.

## Target expectation versus actual achievement

Milestone temporal semantics follow the same general LifeOS historical principle used elsewhere:

```text
Target expectation
        !=
Actual achievement
```

A target may move without changing Milestone identity.

```text
Milestone
Beta release

Original target
1 October

Current target
15 October
```

The Milestone remains the same checkpoint while target history can be preserved.

Actual achievement may occur before, after, or exactly at the current target.

```text
Target
20 September

Reached
17 September
```

or:

```text
Reached
25 September
```

`early`, `late`, and delay values are derived from comparing the target expectation with the actual achievement. They are not fundamental Milestone states.

Passing a target date does not automatically mark the Milestone reached, failed, or completed.

## Evidence and provenance

A Milestone can be reached through evidence from multiple possible sources, including:

- Activity Actual or Outcome;
- Event Outcome;
- Observation;
- Register or measurement history;
- external integration/import;
- Decision Record;
- explicit user declaration;
- approved deterministic rule;
- composite evidence.

Example:

```text
Goal
Find a new job

Milestone
Receive first job offer

External email / imported observation
Offer received
        ↓
Evidence
        ↓
Milestone reached
```

LifeOS must not invent an artificial Activity such as `Receive job offer` merely to make the checkpoint reachable.

User declaration remains authoritative according to the broader LifeOS confirmation/provenance policy. Imported or inferred evidence retains source and provenance.

Canonical attainment hardening:

> **Milestone attainment is evidence/evaluation-backed checkpoint state. It must not become a second independent source of Actual, Outcome, Observation, or other underlying reality.**

The system may derive or materialize a reached/effective time for history/querying, but the basis for attainment must remain explainable and must not silently duplicate or overwrite its source facts.

## Progress toward a Milestone

Milestone attainment and readiness/progress are different concepts.

A Milestone may support an optional derived readiness or progress view based on linked work, requirements, evidence, or sub-checkpoints.

However:

> **A universal stored Milestone percentage is not canonical truth.**

For a checkpoint such as `Design approved`, `72% approved` is usually false precision. The system may instead derive that 72% of linked preparatory work is complete while the Milestone itself remains unreached.

This follows the same LifeOS principle already applied to Goal progress.

## Identity and history

A Milestone has persistent identity while ordinary target changes or evidence updates occur.

Examples that normally do not change identity:

- moving the target date;
- adding evidence;
- correcting a label;
- linking another supporting Activity;
- revising a readiness estimate.

Examples that may imply replacement, removal, waiver, or a different Milestone:

- abandoning the checkpoint entirely;
- replacing `Beta release` with `Launch directly`;
- redefining the checkpoint so substantially that it represents a different state.

Exact lifecycle, waiver, cancellation, versioning, and replacement semantics are deferred to the lifecycle/history review.

Historical target changes and actual achievement must not be silently rewritten.

## Relationships

Conceptually, a Milestone may:

- belong to or matter within one or more Plans;
- support or be referenced by one or more Goals;
- be evaluated from one or more Evidence sources;
- be preceded or followed by Activities, Events, phases, or other Milestones;
- participate in dependencies;
- trigger later planning or execution once reached.

The exact structural versus semantic relationship model is deferred to the Relationship Model review.

No rigid universal hierarchy such as `Goal -> Plan -> Milestone -> Activity` is accepted.

## Representative stress tests

### Website redesign

```text
Goal
Rebuild personal website

Plan
Design -> development -> deployment

Activity
Prepare mockups

Event
Design review

Milestone
Design approved
```

Pass: each concept has distinct semantics.

### Language learning

```text
Goal
Reach B2

Milestone
B1 reached

Routine
Speaking practice 3x/week

Event
Certification exam
```

Pass: Milestone is meaningful as a checkpoint while B2 remains the Goal.

If B1 becomes independently pursued, it may become a Goal instead.

### Music release

```text
Goal
Publish album

Plan
Production and release plan

Activity
Finalize master

Milestone
Master locked

Event
Release-day event

Milestone
Release live on platforms
```

Pass: Event occurrence and distribution state remain distinct.

### Job search

```text
Goal
Find a new job

Plan
Job-search strategy

Activity
Submit application

Event
Interview

Milestone
First offer received
```

Pass: external result can reach the Milestone without synthetic executable work.

### Savings

```text
Goal
Save EUR 20,000
```

EUR 5,000 is ordinary derived progress unless intentionally designated as a meaningful checkpoint.

Pass: Milestone does not duplicate arbitrary metric thresholds.

### Architecture decision

```text
Decision Record
Choose PostgreSQL

Milestone
Primary database selected
```

Pass: reasoning/history and checkpoint attainment remain distinct.

## Current invariants

1. `Milestone != Goal`.
2. `Milestone != GoalCriterion`.
3. `Milestone != Activity`.
4. `Milestone != Event`.
5. `Milestone != Outcome`.
6. `Milestone != Deadline`.
7. `Milestone != Phase`.
8. `Milestone != Decision Record`.
9. A Milestone represents a meaningful checkpoint, not work to execute.
10. A Milestone should normally have meaningful context from at least one Goal and/or Plan.
11. A Milestone may relate to multiple Goals or Plans without imposing a rigid hierarchy.
12. A target date/window does not directly occupy operational calendar time.
13. Target expectation and actual achievement remain distinct.
14. Actual achievement may occur before, after, or exactly at the target.
15. Passing the target date does not automatically reach or fail the Milestone.
16. A Milestone may be reached through Activity, Event, Observation, import, measurement, Decision, user declaration, or other valid Evidence.
17. Achievement evidence/provenance must remain traceable where available.
18. Progress/readiness toward a Milestone is optional and derived rather than universal canonical percentage state.
19. Completing an Activity does not automatically create or reach a Milestone.
20. A Goal threshold or progress point does not automatically become a Milestone.
21. A checkpoint with independent strategic meaning should be reconsidered as a Goal.
22. Ordinary target-date changes do not automatically change Milestone identity.
23. Historical target revisions and actual achievement must not be silently rewritten.
24. Exact lifecycle, waiver, cancellation, versioning, replacement, and persistence semantics remain deferred.
25. Milestone attainment is evidence/evaluation-backed and must not become an independent duplicate source of underlying reality.

## External benchmark lessons

External systems use the term `milestone` differently:

- some model it as a special work item or task-like marker;
- some model it as a project stage/checkpoint with linked work and derived progress;
- some model it as a grouping/target container for issues or deliverables.

LifeOS does not copy any one of these shapes. The useful common semantic core is a meaningful checkpoint within a broader context.

This reinforces the decision to keep Milestone distinct from executable Activity, time-centred Event, Goal, and generic progress percentages.

## Open questions intentionally deferred

The following remain open for later reviews:

- exact persistence shape and aggregate ownership;
- exact lifecycle and states such as planned, reached, waived, cancelled, superseded, or not-applicable;
- whether some milestone relationships are structural foreign keys versus semantic relations;
- dependency semantics between Milestones;
- phase-transition mechanics;
- how milestone readiness/progress is derived in specialist plans;
- GoalCriterion persistence and how criteria reference Milestones;
- exact Evidence/evaluation relationship that establishes attainment;
- version/replacement behavior for materially redefined checkpoints;
- notification and Trigger behavior when a Milestone is reached or at risk;
- AI proposal/confirmation rules for inferred Milestones.

## Current conclusion

Milestone is accepted as a distinct contextual domain concept because the intention/execution checkpoint exposed real cases that Goal, Plan, Activity, Event, and Routine do not represent cleanly by themselves.

It is not accepted as a universal standalone objective or as a synonym for progress, deadline, task, Event, Goal, Outcome, Evidence, or Actual reality storage.

The first-three-cluster Validation Methodology v3 regression confirms that Milestone remains distinct after Actual, Outcome, Observation, Confirmation, Evidence and Provenance were introduced.

Any future model that stores Milestone attainment independently of its evaluation/evidence basis must explicitly reopen this boundary.