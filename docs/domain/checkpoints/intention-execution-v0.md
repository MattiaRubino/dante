# Intention & Execution Cluster v0 Checkpoint

**Status:** PASS — current validated cluster baseline  
**Validated:** 2026-08-11  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Scope

This checkpoint validates the first LifeOS Domain Atlas cluster as a combined system rather than as isolated concepts.

Validated current baselines:

- Goal v0;
- Plan v0;
- Activity v0;
- Event v0;
- Routine v0;
- Milestone v0.

The purpose of the checkpoint is to determine whether these primitives remain distinguishable, composable, history-safe, and useful across representative LifeOS scenarios without requiring duplicate entities, forced hierarchies, hidden planned/actual rewrites, arbitrary JSON escape hatches, or additional missing primitives.

## Common evaluation matrix

Each scenario was tested against the same questions:

1. Can the scenario be represented naturally?
2. Does each persistent concept have one coherent identity?
3. Is duplicate representation required?
4. Do planned expectation, current schedule, actual reality, and history remain distinguishable?
5. Are relationships natural rather than forced into one parent-child tree?
6. Do recurrence and individual occurrence semantics remain separable?
7. Can valid evidence reach the relevant Goal criteria even when not planned for those Goals?
8. Can real execution deviate from the plan without rewriting original intent?
9. Does the model avoid arbitrary JSON or one-off life-domain entities merely to represent the case?
10. Is another primitive required to explain a materially different identity, lifecycle, invariant, or behavior?

## Result

**PASS.**

No accepted baseline needs to be reopened before entering the Time cluster.

Milestone was the one material gap exposed during the first pass. After Milestone v0 was introduced and the full matrix rerun, no additional primitive is currently required for intention/execution semantics.

This validation is a current baseline, not a permanent closure. A later temporal, evidence, relationship, persistence, or implementation review may reopen one of these concepts if new evidence exposes a contradiction.

## Representative scenario matrix

| Scenario | Natural representation | Result |
|---|---|---|
| Spoken English B2 | Goal + Plan + Routine + Activities + lesson/test Events + Milestones | PASS |
| Exam preparation | Goal + Plan + study Routine + Activities + exam Event + preparation/result Milestones | PASS |
| Rebuild personal website | Goal + Plan + Activities + review Events + design/release Milestones | PASS |
| Diet / body-composition journey | Goal + optional Plan + Routines + Activities/Events + Observations/Evidence | PASS |
| Picnic with friends | Event + Actual/Observations feeding multiple Goal criteria | PASS |
| Photography excursion | Activity or Event according to action-centred vs occurrence-centred meaning; Actual may feed photography, fitness, and social Goals | PASS |
| Hospital/work shift | recurring Event series + attendance/Actual + Activities performed inside the shift | PASS |
| Medicine every 12 hours | Routine + future Occurrence + Actual; exact interval/time-zone mechanics intentionally deferred | PASS with Time dependency |
| Weekly team meeting | recurring Event series, not Routine merely because recurrence exists | PASS |
| Multi-step morning routine | Routine governing a recurring action bundle without becoming a Plan merely because it is composite | PASS |
| Rehabilitation/training program | Plan coordinating Routines, Activities, Events, constraints, and Milestones | PASS |
| Job search | Goal + Plan + recurring search Routine + application Activities + interview Events + offer Milestone | PASS |
| Music release | Goal + Plan + production Activities + optional production Routine + review/release Events + master/release-live Milestones | PASS |
| Saving EUR 20,000 | Goal; intermediate values are derived progress unless intentionally designated Milestones | PASS |
| Moving house | Plan may stand alone or support a Goal; Activities, Events, and Milestones compose naturally | PASS |
| Asset/plant/caregiving behavior | Goal optional + Routine + Activities/Events; subject semantics deferred to later cluster | PASS with Subject dependency |
| Disrupted week | Routine occurrence exceptions, Plan replanning, and Event preservation work conceptually; Temporary Mode remains a later capability | PASS |
| Fitness Goal plus injury-recovery Goal | same Actual/Evidence may affect multiple Goal criteria differently; relationship/evaluation semantics deferred | PASS with Relationship dependency |

## Boundary validation

### Goal versus Milestone

PASS.

- Goal has independent desired-outcome meaning and may have its own evaluation and pursuit.
- Milestone has contextual checkpoint meaning within a broader Goal and/or Plan.
- A checkpoint that acquires independent strategic meaning should be reconsidered as a Goal.

### Goal versus Routine

PASS.

- Goal expresses the desired condition or behavioral result.
- Routine expresses the intended recurring execution policy.
- A Goal can be satisfied by execution outside the linked Routine.

### Plan versus Activity

PASS with a deliberate soft boundary.

- Activity is directly executable as a coherent unit of action.
- Plan coordinates execution strategy and multiple elements.
- No arbitrary threshold such as number of child items is required.
- Composite Activity remains valid when its children are semantic decomposition of one coherent executable result; strategy/coordination across independently executable elements tends toward Plan.

This boundary must be rechecked during persistence/API design but does not currently require reopening either primitive.

### Plan versus Routine

PASS with a deliberate soft boundary.

- Plan coordinates a strategy or path.
- Routine coordinates a pattern intended to repeat.
- A complex recurring bundle may remain Routine when repetition is its dominant semantic.
- A progression structure that coordinates changing phases, multiple Routines, Activities, Milestones, and adaptation remains Plan.

### Activity versus Event

PASS.

- Activity is action-centred.
- Event is occurrence-centred and temporal placement is intrinsic to its meaning.
- Exact scheduling does not turn Activity into Event.
- A real-world case is not duplicated merely because both action and time matter; classification follows the dominant intended meaning, with linked preparation/follow-up Activities where needed.

### Routine versus recurring Event

PASS.

- Routine is a recurring behavioral/execution policy.
- A recurring Event is an Event series whose occurrence repeats.
- Recurrence machinery is a shared temporal capability, not sufficient reason to classify something as Routine.

### Milestone versus Event/Outcome/GoalCriterion

PASS.

- Event is the occurrence.
- Outcome records what happened in an execution/occurrence.
- Milestone is the meaningful contextual checkpoint that may be reached through one or more outcomes/evidence sources.
- GoalCriterion defines how Goal evaluation uses such evidence/checkpoints.

## History and temporal safety

The cluster remains consistent with the current LifeOS history rules:

- passing time does not imply completion;
- original intention is not rewritten because later evidence reveals new relevance;
- original expectation, current accepted schedule/target, and actual occurrence/achievement remain distinguishable;
- actual execution can start/end before or after scheduled time;
- moving one recurring occurrence does not silently rewrite the series/Routine;
- future structural changes may require effective-dated versions while past execution remains tied to the rules that governed it.

Exact persistence/versioning mechanics remain deferred.

## Evidence and multi-Goal safety

The cluster supports evidence paths that are not limited to originally intended Goal links.

```text
Activity / Event / Routine occurrence / independent observation
        ↓
Actual / Observation / Outcome
        ↓
Evidence
        ├──> Goal criterion A
        └──> Goal criterion B
```

A later-discovered relationship does not rewrite why the Activity/Event originally existed. Positive/negative impact is not an intrinsic property of the source item; it depends on Evidence + Criterion + evaluation policy.

## No forced universal hierarchy

The checkpoint explicitly rejects a universal tree such as:

```text
Goal
└── Plan
    └── Routine
        └── Activity
            └── Event
                └── Milestone
```

The accepted concepts have independent identity and optional relationships. Goal, Plan, Activity, Event, Routine, and Milestone may exist in different combinations according to actual semantics.

## Deferred dependencies, not cluster failures

The following unresolved concepts are required downstream but do not invalidate this cluster:

- Occurrence identity/materialization;
- Schedule;
- Session;
- recurrence mechanics and timezone/DST behavior;
- Deadline/window/temporal constraints;
- Calendar Block / Availability / capacity;
- Actual / Outcome / Observation / Evidence / Confirmation / Provenance;
- semantic Relationship and Goal-to-Goal interaction;
- Trigger / Reminder;
- lifecycle/version/replacement mechanics;
- Asset / Subject and specialist-domain measurements;
- persistence/API mapping.

## Next cluster

The next Domain Atlas cluster is **Time**.

The first concept to review is `Occurrence`, because both Routine and recurring Event semantics now depend on a stable identity for an expected individual instance that can be rescheduled, skipped, cancelled, executed, or corrected without rewriting its originating series/policy.

Provisional sequence:

```text
Occurrence
→ Schedule
→ Session
→ Deadline / Window / Temporal Constraint
→ Recurrence
→ Calendar Block / Availability / Capacity
```

The sequence may change if Occurrence review reveals a stronger dependency.
