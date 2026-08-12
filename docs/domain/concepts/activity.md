# Activity v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-10  
**Multi-actor wording hardening:** 2026-08-11  
**Meaning of accepted:** best current decision; reopenable with better evidence  
**Workstream:** Core Domain Model v0

## Canonical definition

> **An Activity is a persistent representation of an actionable intention: a unit of work or behavior intended to be performed, whose responsibility, planned execution, actual execution, and outcome LifeOS may track separately. An Activity defines what is to be done; it does not itself define who must perform it, when execution occurs, or what actually happened.**

Examples include buying something, calling someone, writing part of a document, studying for a bounded amount of time, running a distance, preparing a presentation, performing maintenance, completing a backup, or working on a creative idea for a time-boxed period.

The same primitive must support simple personal tasks, measurable actions, collaborative/shared work, specialist-domain execution, and larger but still actionable units without creating one entity type per life domain.

## Why the multi-actor wording changed

The original Activity v0 wording said:

```text
a unit of work or behavior the user intends to perform
```

That is a correct personal-first case but incorrectly suggests that intention-holder, requester, responsible actor and performer must be the same person.

Multi-actor discovery and external research show common cases such as:

```text
Activity
Prepare presentation

requested by
Manager

responsible
Luca

performed by
Luca + Sara
```

or:

```text
Activity
Pick up child

responsibility transfer requested
Mattia -> Luca
```

or:

```text
Activity
Cover open shift task

responsible actor
not yet assigned / claimable
```

The actionable intention remains one Activity while actor relationships may change.

Therefore the canonical definition is actor-neutral without introducing a premature Responsibility/Actor schema.

## Validation basis

Activity v0 has been reviewed against:

- the broad LifeOS feature-discovery simulation;
- personal work, study, health, home, maintenance, travel, creative and caregiving scenarios;
- fixed/flexible scheduling, splitting, partial completion, fallback and replanning;
- planned-versus-actual execution, confirmation, measurements, postponement and replacement;
- iCalendar VTODO/VEVENT separation, task-system scheduling patterns and issue/sub-issue decomposition;
- the completed multi-actor discovery simulation;
- the multi-actor external research and evidence-synthesis checkpoint, especially assignment, hand-off, open responsibility and actual-performer distinctions.

External systems and research are evidence, not schemas to copy.

## Task semantics

`Task` is not currently a separate domain primitive.

> **Task is a user-facing/contextual form of Activity whose primary semantics are the completion of a defined unit of work.**

Examples:

```text
Activity: Buy milk
UI: Task / checkbox
```

```text
Activity: Study English for 60 minutes
UI: Study / activity
```

```text
Activity: Run 5 km
UI: Workout
```

A specialist module may extend execution/evidence data associated with an Activity without creating a second scheduling/execution universe.

## Core semantic separation

```text
Goal      -> what is wanted
Plan      -> how it is intended to be pursued/organized
Activity  -> what concrete action is intended
Schedule  -> when concrete execution is planned
Session   -> when a bounded execution episode actually occurred
Actual    -> broader truth about what happened
Evidence  -> what may support evaluation
```

Multi-actor relationships add dimensions around Activity without changing Activity identity:

```text
requester
responsible actor / assignee
performer
approver
subject / beneficiary
provenance
```

These are not synonyms for Activity.

## Activity versus Goal

A Goal expresses a desired outcome, condition, change or behavioral pattern. An Activity expresses actionable intended work/behavior.

```text
Goal: Improve physical fitness
Activity: Go for a 5 km run
```

Therefore:

> **Activity != Goal.**

An Activity may contribute to zero, one or multiple Goals and may exist without a Goal.

## Activity versus Plan

A Plan coordinates a strategy/body of execution. Activity is an actionable unit within or outside such structure.

```text
Plan: Prepare for exam
Activities:
- study chapter 1
- solve exercise set
- complete mock exam
```

An Activity may itself contain meaningful sub-activities without becoming a Plan automatically.

Current distinction:

> **Activity is a meaningful executable unit; Plan coordinates multiple execution elements or a broader strategy.**

No arbitrary number of subtasks/hours defines the boundary.

Therefore:

> **Activity != Plan.**

## Activity versus Schedule

Scheduling an Activity does not change what the Activity is.

```text
Activity: Write thesis introduction
Estimated effort: 3h
Schedules:
- Tuesday 18:00-20:00
- Wednesday 19:00-20:00
```

Moving/splitting/removing planned placement does not automatically create a new Activity.

Therefore:

> **Activity != Schedule.**

## Activity versus Session

One Activity may require zero, one or multiple actual execution Sessions.

```text
Activity: Write report
Session A: Monday 18:00-19:30
Session B: Tuesday 17:30-18:15
Session C: Thursday 20:00-21:00
```

Therefore:

> **Activity != Session.**

## Sub-activity versus Session

Sub-activity is semantic decomposition:

```text
Activity: Write article
Sub-activities:
- introduction
- analysis
- conclusion
```

Session is temporal execution decomposition:

```text
Activity: Write introduction
Sessions:
- Monday 20:00-21:00
- Tuesday 18:00-19:30
```

Therefore:

> **Sub-activity decomposition and Session splitting are independent dimensions.**

## Activity versus Actual

Activity records intention; Actual records reality.

```text
Activity intention: Run 5 km
Actual result: 3.8 km
```

The Activity must not be rewritten to `Run 3.8 km` afterward because that destroys the original expectation.

Therefore:

> **Activity != Actual.**

Planned and actual quantities, durations, timing, quality and results remain distinguishable.

## Activity versus Event

Activity is action-centred. Event is occurrence-centred.

```text
Activity: Call dentist
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

An Activity can occupy a precise calendar interval and remain an Activity.

Therefore:

> **Activity != Event.**

## Activity versus Routine

Routine is persistent recurring behavioral/execution policy. Activity is one actionable intention.

```text
Routine: Gym Mon/Wed/Fri
Occurrence-specific action: Wednesday training
```

LifeOS should not represent recurrence by moving one completed Activity identity forward forever.

Therefore:

> **Activity != Routine.**

## Independent existence

An Activity may exist without Goal, Plan, Routine or exact Schedule.

Examples include buying milk, calling a mechanic or backing up photos.

LifeOS must not create artificial parent objects solely to satisfy a rigid hierarchy.

## Responsibility, assignment and performer

Activity identity is independent from ordinary changes in who requests, owns responsibility for, is assigned to, approves or actually performs the work.

Canonical non-collapse rules:

> **Activity identity != requester.**

> **Activity identity != responsible actor / assignee.**

> **Activity identity != eventual performer.**

> **Activity creator != automatic authority over every actor involved.**

Example:

```text
Activity
Prepare release artwork

requester
Band lead

responsible
Designer A

reassigned later
Designer B

Actual performer
Designer B + Assistant
```

Ordinary reassignment preserves Activity identity/history.

A materially changed intended action may still require replacement.

## Open / claimable responsibility

The future responsibility model must allow a valid state where work is intentionally available to be claimed rather than prematurely assigned.

Examples:

```text
Household Activity
Take recycling out
responsibility: open / someone eligible may claim
```

```text
Care help request
Pick up prescription
responsibility: unclaimed
```

This requirement does not yet decide the physical Responsibility model.

## Hand-off is not automatically effective on send

Where responsibility transfer matters, LifeOS must be able to distinguish at least conceptually:

```text
hand-off requested
recipient response/acceptance
canonical responsibility changed
Actual performer later
```

Low-consequence UI may collapse these stages. The domain must not force `request sent = responsibility transferred` where that would create false certainty.

## Coordination stewardship is not proved by assignment

Multi-actor research shows that assigning visible execution may leave another actor carrying anticipation, reminding, monitoring and repair burden.

Therefore:

> **Assignment is not proof that coordination stewardship or mental load transferred.**

No standalone Stewardship primitive is accepted yet. The distinction remains a mandatory future Relationship/Responsibility/product-validation question.

## Relationship to Goals and Plans

Conceptually:

```text
Activity -> 0..N Goals
Activity -> 0..N Plans
```

This is semantic relationship direction, not a final physical cardinality decision.

One Activity may intentionally support multiple Goals.

```text
Activity: Go hiking with friends
may support:
- be more physically active
- improve social life
```

## Planned relevance versus discovered relevance

LifeOS must distinguish why an Activity was created from what its execution later affects.

### Intentional support

```text
Goal: Improve fitness
Activity: Gym session
Relation: intentionally supports Goal
```

### Discovered relevance

```text
Activity: Photography excursion
Actual/observations:
- walked 10.4 km
- several hours outdoors

Later evidence may be relevant to:
Goal: Increase physical activity
```

LifeOS must not retroactively pretend the fitness Goal was the reason the Activity existed.

Therefore:

> **Discovered relevance preserves original Activity intention and connects through Evidence/evaluation semantics.**

## Goal evaluation is not limited to planned Activities

A Goal may receive valid Evidence from:

- Actuals produced by intentionally linked Activities;
- unrelated Activities;
- independent Observations;
- imported workouts/measurements/transactions/records;
- Register entries;
- integrations;
- authorized declarations;
- deterministic derived values;
- other sources accepted by the criterion/policy.

```text
Goal: Walk >= 30 km/week
Imported observation: unplanned walk 8.2 km
```

The walk may count without a prior Activity.

Therefore:

> **Goal evaluation is Evidence-driven, not limited to compliance with planned Activities.**

## Evidence contribution is contextual

An Activity is not intrinsically positive/negative for every Goal.

Correct evaluation pattern:

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

Therefore contribution direction belongs to context/evaluation.

## Inferred relevance and AI boundary

AI may identify possible Activity/Evidence relevance to additional Goals.

Ambiguous semantic reinterpretation remains inferred/proposed with provenance/confidence until resolved by authorized policy/actor.

Deterministic calculations may apply automatically when accepted evidence and criterion policy already authorize them.

Canonical rule:

> **AI may discover possible relevance but does not rewrite Activity purpose, actor responsibility, authority or Actual history merely by inference.**

## Goal-to-Goal influence discovered as requirement

Activities expose cases where Goals support, compete, overlap or depend on one another.

Do not reduce this prematurely to one generic `influences` field.

Typed relationship semantics belong to the future Relationship Model.

## Completion semantics

Not every Activity becomes `done` in the same way.

LifeOS must support at least:

- output-bounded;
- quantity-bounded;
- effort/time-bounded;
- checklist/composite;
- partial execution;
- specialist completion where justified.

A universal canonical `completion_percentage` is not required.

## Estimated effort, scheduled duration and actual effort

These are distinct:

```text
Estimated effort: 3h
Scheduled: Tue 2h + Wed 1h
Actual effort: 2h24m
```

Do not overload one `duration` field across lifecycle meanings.

## Temporal semantics

Activity may participate in:

- accepted Schedule placements;
- valid/preferred windows;
- hard/soft Temporal Constraints;
- deadlines;
- movement policies;
- open scheduling;
- duration/spacing constraints.

These semantics remain distinct.

Do not use one ambiguous `due` field for scheduling date, target date and deadline.

## Divisibility and execution policy

Activities may be:

- indivisible;
- split across Sessions;
- partially completable;
- resumable;
- allowed to end early when result achieved;
- constrained by minimum useful Session duration;
- subject to preparation/recovery/spacing/specialist rules.

These capabilities do not imply every rule belongs directly on the Activity table.

## Recurrence and Occurrences

Repeating execution must preserve individual expected-instance history.

```text
Routine / recurring source
        ↓
Occurrence A -> Schedule -> Session/Actual/Outcome
Occurrence B -> Schedule -> Session/Actual/Outcome
```

One Activity identity must not be advanced forever after completion to simulate recurrence.

## Identity and continuity

Activity normally retains identity across:

- rescheduling;
- splitting execution across Sessions;
- preferred-window changes;
- ordinary reassignment;
- partial execution/resumption;
- adding supporting context/relations.

A materially changed intended action may require replacement:

```text
Activity A: Prepare written report
replaced by
Activity B: Prepare live demo
```

Original intention/replacement history remains visible.

Exact version/replacement boundary remains deferred.

## Templates are not execution instances

A reusable Activity blueprint does not share the completion lifecycle of generated executable Activities.

Completing one generated Activity does not complete the template.

## External benchmark observations

Useful benchmark patterns include:

- iCalendar `VTODO` vs `VEVENT` supports action vs occurrence semantics;
- action identity/time placement need not be the same concept;
- task products demonstrate ambiguity of `due` terminology;
- issue trackers demonstrate semantic parent/sub-work decomposition;
- multi-actor work/shift/care systems demonstrate assignment, hand-off and actual performer distinctions.

LifeOS keeps its stronger planned/actual/evidence/actor-separation semantics rather than copying provider models.

## Multi-actor evidence hardening

The completed discovery/research establishes these mandatory guardrails:

```text
Activity identity != requester
Activity identity != assignee/responsible actor
Activity identity != performer
assignment != responsibility transfer proof
assignment != coordination-stewardship transfer proof
planned performer != Actual performer
creator != universal authority
```

The future model must also tolerate open/claimable work and truthful hand-off states where needed.

None of these findings requires splitting Activity itself.

## Current invariants

1. `Activity != Goal`.
2. `Activity != Plan`.
3. `Activity != Schedule`.
4. `Activity != Session`.
5. `Activity != Actual`.
6. `Activity != Event`.
7. `Activity != Routine`.
8. `Task` is product/context language, not a separate kernel primitive.
9. Activity may exist without Goal, Plan, Routine or exact Schedule.
10. Activity may intentionally contribute to multiple Goals/structures.
11. Activity may be indivisible or executed through multiple Sessions.
12. Sessions are not sub-activities.
13. Sub-activities are semantic decomposition; Sessions are temporal execution episodes.
14. Estimated effort, scheduled time and actual effort are distinct.
15. Deadline, valid window, preference and Schedule are distinct temporal meanings.
16. Putting Activity on calendar does not transform it into Event.
17. Passage of time does not complete Activity.
18. Planned result and Actual result remain distinct.
19. Rescheduling/splitting/ordinary execution adjustment does not automatically change Activity identity.
20. Ordinary reassignment does not automatically change Activity identity.
21. Activity identity is independent from requester, responsible actor/assignee and eventual performer.
22. Open/claimable responsibility must remain representable by the future relationship model.
23. Hand-off request does not universally prove effective responsibility transfer.
24. Assignment does not prove coordination-stewardship/mental-load transfer.
25. Replacement preserves the original Activity and successor relationship/history.
26. Repeating execution preserves individual Occurrence history.
27. Completion semantics may be output-, quantity-, effort-, checklist-, composite- or context-based; no universal completion percentage.
28. Prior Goal linkage is not required for later Evidence relevance.
29. Actuals/Observations may become Evidence for Goals not originally linked.
30. Goal evaluation can use unplanned/imported/independent evidence.
31. Discovered relevance must not rewrite original purpose.
32. Positive/negative contribution is contextual to Evidence/criterion/evaluation policy.
33. Ambiguous inferred relevance preserves provenance and remains proposed until authorized/resolved.
34. Deterministic calculations may use accepted evidence under authorized policy.
35. Reusable templates do not share generated Activity completion lifecycle.
36. AI does not gain actor authority merely by seeing or reasoning over Activity context.

## Stress-test coverage

Representative cases include:

| Case | Representation |
|---|---|
| Buy milk | independent output Activity |
| Study 30 pages | quantity-bounded Activity |
| Study 60 minutes | effort-bounded Activity |
| Fix software bug | output Activity |
| Deep work | time-boxed Activity |
| Vehicle maintenance | Asset-linked Activity |
| Workout | specialist Activity + measurements |
| Prepare suitcase | checklist/composite Activity |
| Interrupted work | one Activity + multiple Sessions |
| Replace report with demo | replacement between Activities |
| Photography hike walks 10 km | Actual becomes Evidence for another Goal |
| Shared presentation | one Activity + several actor relationships |
| Reassign deliverable | same Activity, responsibility relationship changes |
| Open household chore | Activity with future claimable responsibility |
| Care hand-off requested but not accepted | Activity preserved; transfer remains pending |
| Planned worker absent, substitute performs | same Activity; planned vs Actual performer differ |

No reviewed scenario requires a second independent Task primitive or per-actor Activity clones for genuinely shared work.

## Deliberately deferred questions

Activity v0 does not decide:

- final Responsibility/Assignment/Hand-off model;
- Actor/Person/Account/Principal model;
- authority/visibility model;
- whether coordination stewardship becomes domain state or product metric;
- exact Event semantics beyond accepted Event v0;
- exact Actual/Outcome/Observation/Evidence persistence;
- actor-specific Actual contribution model;
- GoalCriterion persistence;
- formal Relationship Model;
- exact composite Activity/Plan boundary;
- exact completion-policy persistence;
- lifecycle/status state machine;
- exact version/replacement implementation;
- Template persistence;
- specialist extension mechanism;
- SQL/API representation.

## Decision note

Activity v0 remains the accepted actionable-intention primitive.

The 2026-08-11 hardening removes the accidental assumption that the person whose LifeOS contains the Activity must also be its requester, responsible actor and performer. It does not change the core Activity/Event/Plan/Schedule/Session boundaries.

---

# 2026-08-12 — Responsibility v0 closure amendment

Responsibility v0 and its validation checkpoint close the previously deferred **semantic** Responsibility/Assignment/Claim/Hand-off boundary without changing Activity identity.

Current authoritative interpretation:

```text
Activity
= actionable intention identity

Responsibility
= specific semantic relation: who is accountable for ensuring the bounded commitment is appropriately handled

Assignment
= role-specific establishment/change operation
NOT standalone universal primitive

Claim
= self-initiated role-acquisition operation
NOT standalone universal primitive

Hand-off
= role-specific transfer workflow/pattern
NOT standalone universal primitive

Expected performer
!= Responsibility

Actual performer
!= Responsibility

Coordination Stewardship
!= Responsibility
standalone primitive SAFE DEFERRED
```

The older wording above referring to a **future Responsibility model** is superseded at the semantic level by `concepts/responsibility.md`. Physical identity/cardinality/state/version/API/SQL representation remains deferred to the logical model and later Authority/Acceptance/Visibility reviews.

Additional canonical hardening:

```text
unknown responsible Actor
!=
explicitly open / unassigned / claimable
```

A hand-off request does not universally establish a transfer, Assignment does not universally imply Acceptance, and ordinary Responsibility change continues to preserve the same Activity identity.

See:

- `concepts/responsibility.md`;
- `checkpoints/responsibility-v0-validation.md`;
- `checkpoints/relationship-v0-validation.md`.
