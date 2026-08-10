# Activity v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-10  
**Meaning of accepted:** best current decision; reopenable with better evidence  
**Workstream:** Core Domain Model v0

## Canonical definition

> **An Activity is a persistent representation of an actionable intention: a unit of work or behavior the user intends to perform and whose planned execution, actual execution, and outcome LifeOS may track separately. An Activity defines what is to be done; it does not itself define when execution occurs or what actually happened.**

Examples include buying something, calling someone, writing part of a document, studying for a bounded amount of time, running a distance, preparing a presentation, performing maintenance, completing a backup, or working on a creative idea for a time-boxed period.

The same primitive must support simple personal tasks, measurable actions, specialist-domain execution, and larger but still actionable units without creating one entity type per life domain.

## Validation basis

Activity v0 was reviewed against:

- the LifeOS feature-discovery simulation across study, professional work, health and fitness, home, maintenance, travel, creative work, caregiving, and disrupted schedules;
- the existing LifeOS scheduling-flexibility model, including fixed/flexible execution, splitting, partial completion, fallback, and replanning;
- the existing LifeOS planned-versus-actual model, including outcome, confirmation, measurements, postponement, and replacement;
- external patterns including iCalendar `VTODO` versus `VEVENT`, Google Tasks scheduling semantics, and Linear parent/sub-issue decomposition.

External systems are benchmark inputs, not models to copy directly.

## Task semantics

`Task` is not currently a separate domain primitive.

> **Task is a user-facing or contextual form of Activity whose primary semantics are the completion of a defined unit of work.**

Examples:

```text
Activity: Buy milk
UI: Task / checkbox
```

```text
Activity: Study English for 60 minutes
UI: Study session / activity
```

```text
Activity: Run 5 km
UI: Workout
```

A specialist module may extend the execution data associated with an Activity, such as distance, sets, repetitions, pages, quantities, or domain-specific measurements, without creating a second scheduling/execution universe.

## Core semantic separation

```text
Goal      -> what is wanted
Plan      -> how it is intended to be pursued or organized
Activity  -> what concrete action is intended
Schedule  -> when concrete execution is planned
Actual    -> what actually happened
Evidence  -> what may support evaluation
```

These concepts must remain distinguishable even when a simple productivity application might store them together.

## Activity versus Goal

A Goal expresses a desired outcome, condition, change, or behavioral pattern. An Activity expresses an action the user intends to perform.

```text
Goal: Improve physical fitness
Activity: Go for a 5 km run
```

Therefore:

> **Activity != Goal.**

An Activity may contribute to zero, one, or multiple Goals, but it does not need a Goal in order to exist.

## Activity versus Plan

A Plan coordinates a strategy or body of execution. An Activity is an actionable unit within or outside such a structure.

```text
Plan: Prepare for exam
Activities:
- study chapter 1
- solve exercise set
- complete mock exam
```

An Activity may itself be decomposable into meaningful sub-activities, but this does not make Activity and Plan interchangeable.

Current distinction:

> **Activity is a meaningful executable unit; Plan coordinates multiple execution elements or a broader strategy.**

No arbitrary threshold such as number of subtasks or hours determines when an Activity becomes a Plan. The exact composite-Activity-versus-Plan boundary remains a checkpoint question.

Therefore:

> **Activity != Plan.**

## Activity versus Schedule

Scheduling an Activity does not change what the Activity is.

```text
Activity: Write thesis introduction
Estimated effort: 3 hours
Scheduled execution:
- Tuesday 18:00-20:00
- Wednesday 19:00-20:00
```

Moving, splitting, or removing scheduled execution does not automatically create a new Activity.

Therefore:

> **Activity != Schedule.**

## Activity versus Session

One Activity may require multiple execution sessions.

```text
Activity: Write report
Session A: Monday 18:00-19:30
Session B: Tuesday 17:30-18:15
Session C: Thursday 20:00-21:00
```

These are not three separate Tasks merely because execution is divided over time.

Therefore:

> **Activity != Session.**

## Sub-activity versus Session

A sub-activity is semantic decomposition of work:

```text
Activity: Write article
Sub-activities:
- introduction
- analysis
- conclusion
```

A Session is temporal decomposition of execution:

```text
Activity: Write introduction
Sessions:
- Monday 20:00-21:00
- Tuesday 18:00-19:30
```

Therefore:

> **Sub-activity decomposition and session splitting are independent dimensions.**

## Activity versus Actual

Activity records intention. Actual records what happened.

```text
Activity intention: Run 5 km
Actual result: 3.8 km
```

The Activity must not be rewritten to `Run 3.8 km` after execution, because doing so would destroy the original expectation.

Therefore:

> **Activity != Actual.**

Planned and actual quantities, durations, timing, quality, and results remain distinguishable.

## Activity versus Event

An Activity is action-centred: something the user intends to do.

An Event is occurrence-centred: something expected to occur at a time or in a temporal context, often without task-style completion semantics.

```text
Activity: Call the dentist
Event: Dentist appointment
```

```text
Activity: Prepare slides
Event: Client presentation
```

```text
Activity: Study chapter 8
Event: University lecture
```

An Activity may occupy a precise calendar interval and remain an Activity. Putting it on the calendar does not transform it into an Event.

The iCalendar distinction between `VTODO` action items and `VEVENT` scheduled events provides useful external support for keeping action semantics separate from occurrence semantics.

Therefore:

> **Activity != Event.**

The exact Event model remains a separate review.

## Activity versus Routine

A Routine is a reusable recurring rule or behavioral pattern. An Activity is an actionable intention.

```text
Routine: Gym Monday / Wednesday / Friday
Expected execution: Wednesday training Activity/occurrence
```

An Activity may also exist independently of any Routine.

LifeOS should not model recurrence by merely moving one completed Activity into the future and thereby obscuring historical occurrences.

Therefore:

> **Activity != Routine.**

## Independent existence

An Activity may exist without a Goal, Plan, Routine, or exact Schedule.

Examples include buying milk, calling a mechanic, or backing up photos.

LifeOS must not create artificial Goals or Plans merely to satisfy a rigid hierarchy.

## Relationship to Goals and Plans

Conceptually:

```text
Activity -> 0..N Goals
Activity -> 0..N Plans
```

This is relationship semantics, not yet a physical database-cardinality decision.

One Activity may intentionally support multiple Goals.

```text
Activity: Go hiking with friends
may contribute to:
- Goal: be more physically active
- Goal: improve social life
```

## Planned relevance versus discovered relevance

LifeOS must distinguish why an Activity was created from what its execution later turns out to affect.

### Intentional support

Known before execution:

```text
Goal: Improve fitness
Activity: Gym session
Relation: intentionally supports Goal
```

### Discovered relevance

An Activity may produce Actual data or Observations that become relevant to a Goal that was not part of the original intention.

```text
Activity: Photography excursion
Actual / observations:
- walked 10.4 km
- many steps
- several hours outdoors

Evidence may become relevant to:
Goal: Increase physical activity
```

LifeOS must not retroactively rewrite the Activity as though the fitness Goal had been the reason the excursion was created.

Therefore:

> **Discovered relevance preserves the original Activity intention and connects through evidence/evaluation semantics instead of historical rewriting.**

## Goal progress is not limited to planned Activities

A Goal may receive valid evidence from:

- Actuals produced by intentionally linked Activities;
- Actuals produced by unrelated Activities;
- independent Observations;
- imported workouts, measurements, transactions, or records;
- Register entries;
- external integrations;
- user declarations;
- deterministic derived values;
- other sources accepted by the relevant criterion.

Example:

```text
Goal: Walk at least 30 km/week
Imported observation: Unplanned walk, 8.2 km
```

The walk may count even though no Activity was planned beforehand.

Therefore:

> **Goal evaluation is evidence-driven, not limited to compliance with originally planned Activities.**

This is a cross-concept requirement to be propagated through GoalCriterion, Evidence, Observation, Actual, and Relationship reviews.

## Evidence is contextual, not intrinsically positive or negative

An Activity itself is not globally good, bad, positive, or negative for a Goal.

A picnic may generate food observations relevant to a nutrition Goal, but the effect depends on the criterion, evaluation period, and policy.

A long hike may support a Goal to increase physical activity while being incompatible with another recovery-related objective or constraint.

The correct conceptual chain is:

```text
Fact / Actual / Observation
          +
Criterion
          +
Evaluation policy
          ↓
Goal evaluation
```

not:

```text
Activity -> globally positive/negative
```

Therefore:

> **Contribution direction is contextual to a criterion/evaluation, not an intrinsic property of Activity.**

## Inferred relevance and AI boundary

LifeOS or AI may notice that an Activity or its resulting evidence could be relevant to an additional Goal.

When the interpretation is ambiguous, it remains inferred/proposed with provenance and, where useful, confidence until accepted by user authority or an approved policy.

Example:

```text
Goal: Complete three serious workouts/week
Actual: 10 km photography hike
```

The distance may be factual while whether it qualifies as a `serious workout` remains semantically ambiguous.

Where a criterion is deterministic and its source policy already authorizes the evidence, no redundant user confirmation is required.

Therefore:

> **AI may discover possible relevance; deterministic domain rules establish authorized calculations; ambiguous semantic reinterpretations remain proposed/inferred until resolved by policy or user authority.**

## Goal-to-Goal influence discovered as a requirement

Activity review exposed a broader requirement: Goals themselves may support, depend on, compete with, overlap with, or otherwise affect one another.

This must not be reduced prematurely to a generic `Goal A influences Goal B` field.

Possible relation semantics such as supports, conflicts with, prerequisite for, contributes to, overlaps with, or depends on belong to the future Relationship Model review.

Activity v0 records this as a discovered cross-domain requirement but does not define the final relationship ontology.

## Completion semantics

Not every Activity becomes `done` in the same way.

LifeOS must support at least:

- output-bounded execution, such as submitting a document;
- quantity-bounded execution, such as reading pages or covering distance;
- effort/time-bounded execution, such as studying for sixty minutes;
- checklist/composite execution;
- partial execution;
- context-specific specialist completion where justified.

A universal canonical `completion_percentage` is therefore not required. A percentage may be useful as a derived presentation where meaningful.

## Estimated effort, scheduled duration, and actual effort

These are distinct concepts.

```text
Estimated effort: 3 hours
Scheduled execution: 2 hours Tuesday + 1 hour Wednesday
Actual effort: 2 hours 24 minutes
```

They must not be collapsed into one `duration` field whose meaning changes over the lifecycle.

## Temporal semantics and deadline ambiguity

Activity may participate in temporal rules such as fixed execution, valid window, preferred window, hard deadline, scheduling preference, or open scheduling.

These concepts remain semantically distinct.

External task systems illustrate why a generic `due` field is dangerous. Google Tasks currently documents its `due` field as the day a task should be done or shown on the calendar grid and explicitly states that it is not the task's deadline.

LifeOS should therefore avoid ambiguous temporal fields whose meaning changes between scheduling date, target date, and hard deadline.

Exact temporal value objects belong to the later Time cluster.

## Divisibility and execution policy

The existing LifeOS simulation and scheduling requirements require support for Activities that may be:

- indivisible;
- split into multiple sessions;
- partially completable;
- resumable after interruption;
- allowed to finish early when the intended result is reached;
- constrained by minimum useful session duration;
- subject to preparation, recovery, spacing, or specialist execution rules.

These are required capabilities, not a decision to place every policy directly on the Activity table.

## Recurrence and occurrences

LifeOS should not treat recurrence as merely mutating one Activity's date forward after each completion.

Individual expectations and results must remain historically available.

```text
Routine / recurring source
        ↓
Occurrence A -> planned -> actual -> outcome
Occurrence B -> planned -> actual -> outcome
```

The exact Routine/Occurrence/Schedule model remains a later review.

## Identity and continuity

An Activity normally retains identity across ordinary scheduling changes such as moving it, splitting execution across sessions, changing a preferred window, or resuming partial work.

A materially changed intended action may instead require replacement.

```text
Activity A: Prepare written report
replaced by
Activity B: Prepare live demo
```

The original intention and replacement relationship remain historically visible.

The exact version-versus-replacement boundary is deferred to the history/versioning review.

## Templates are not execution instances

A reusable Activity blueprint does not share the completion lifecycle of an executable Activity generated from it.

Completing a generated Activity must not complete the reusable template itself.

## External benchmark observations

The following patterns informed Activity v0 without being adopted wholesale:

- iCalendar separates `VTODO`, representing an action item or assignment, from `VEVENT`, supporting the Activity-versus-Event distinction;
- iCalendar supports separate to-do completion/status and temporal properties, showing that action identity and time placement need not be the same concept;
- Google Tasks distinguishes its scheduling-oriented `due` meaning from a true deadline, reinforcing explicit temporal semantics;
- Linear supports parent and sub-issues and explicitly describes a middle ground between a single issue and a project, supporting a semantic rather than numeric boundary between composite Activity and Plan.

LifeOS deliberately keeps planned execution, Actual, Evidence, specialist measurements, and cross-goal relevance more explicit where needed.

## Current invariants

1. `Activity != Goal`.
2. `Activity != Plan`.
3. `Activity != Schedule`.
4. `Activity != Session`.
5. `Activity != Actual`.
6. `Activity != Event`.
7. `Activity != Routine`.
8. `Task` is not currently a separate kernel primitive; it is a user-facing/contextual semantic of Activity.
9. An Activity may exist without a Goal, Plan, Routine, or exact Schedule.
10. An Activity may intentionally contribute to multiple Goals and participate in multiple relevant structures where relationship rules allow it.
11. An Activity may be indivisible or executed through multiple sessions.
12. Sessions are not sub-activities.
13. Sub-activities represent semantic work decomposition; sessions represent temporal execution decomposition.
14. Estimated effort, scheduled time, and actual effort are distinct.
15. Hard deadline, valid window, scheduling preference, and calendar placement are distinct temporal semantics.
16. Putting an Activity on a calendar does not transform it into an Event.
17. Passage of time does not automatically complete an Activity.
18. Planned result and Actual result remain distinct.
19. Rescheduling, splitting, or ordinary execution adjustments do not automatically change Activity identity.
20. Replacement preserves the original Activity and links the successor rather than silently rewriting history.
21. Repeating execution must preserve individual occurrence history.
22. Activity completion may be output-, quantity-, effort-, checklist-, composite-, or context-based; no universal canonical completion percentage is required.
23. Intentional prior Goal linkage is not required for an Activity's execution to become relevant to a Goal.
24. Actuals and Observations produced during or after an Activity may become evidence for Goal criteria that were not originally linked to that Activity.
25. Goal evaluation must be able to use evidence from unplanned Activities, independent observations, imports, and other accepted sources.
26. Discovered relevance must not retroactively rewrite the original purpose or meaning of the Activity.
27. Positive/negative/neutral impact is not an intrinsic Activity property; it is contextual to evidence, criterion, and evaluation policy.
28. Inferred ambiguous relevance preserves provenance and remains proposed/inferred until accepted by user authority or approved policy.
29. Deterministic calculations may incorporate accepted evidence automatically when the criterion and source policy already authorize it.
30. Reusable templates do not share the completion lifecycle of generated executable Activities.

## Stress-test coverage

Representative cases covered without a second Task primitive include:

| Case | Current representation |
|---|---|
| Buy milk | independent output-bounded Activity |
| Study 30 pages | quantity-bounded Activity |
| Study 60 minutes | effort/time-bounded Activity |
| Correct a batch of assignments | composite/batch Activity |
| Fix software bug | output-bounded Activity |
| Deep work | time-boxed Activity |
| Prepare hard-deadline professional work | deadline-constrained Activity within wider Plan |
| Vehicle maintenance | Asset-linked Activity |
| Water plant | Subject/Asset-linked Activity |
| Workout | specialist Activity with domain measurements |
| Submit job application | output-bounded Activity |
| Prepare suitcase | checklist/composite Activity |
| Photography backup | output-bounded Activity |
| Interrupted work resumed later | one Activity with multiple execution sessions |
| Replace report with demo | replacement between distinct Activities |
| Photography hike walks 10 km | Actual becomes evidence for unrelated fitness Goal |
| Picnic produces nutrition data | observations evaluated against relevant criteria without making picnic intrinsically good/bad |
| Unplanned imported walk | evidence may advance walking Goal without a planned Activity |
| One hike affects several goals | one execution may provide evidence relevant to multiple criteria |

No reviewed scenario currently requires `Task` as a second independent domain primitive.

## Deliberately deferred questions

Activity v0 does not decide:

- exact Event semantics;
- exact Routine and recurring-occurrence model;
- exact Schedule versus Session boundaries;
- exact Actual entity/value-object structure;
- exact Observation and Evidence models;
- GoalCriterion persistence and evaluation policy;
- the formal Relationship Model, including Goal-to-Goal influence and Activity-to-Goal relation types;
- exact composite Activity versus Plan boundary;
- exact completion-policy persistence;
- exact deadline/window/scheduling value objects;
- exact lifecycle/status state machine;
- exact version-versus-replacement implementation;
- Template persistence;
- specialist module extension mechanism;
- SQL and API representation.

## Checkpoint requirement

The composite-Activity-versus-Plan boundary and interactions among Goal, Plan, Activity, Event, and Routine must be re-tested at the first intention/execution cluster checkpoint rather than assumed permanently closed.

## Decision note

Activity v0 supersedes the narrower previous Activity/Task glossary semantics **for the active Domain Model workstream only** while the broader documentation set is being revalidated.

The previous product documents remain preserved as source material until changes are propagated deliberately after adjacent concepts have been reviewed.