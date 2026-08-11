# Routine v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-10  
**Meaning of accepted:** best current decision; reopenable with better evidence  
**Workstream:** Core Domain Model v0

## Canonical definition

> **A Routine is a persistent reusable policy that expresses a pattern of behavior or execution the user intends to repeat over time. A Routine governs when, how often, and under which rules that behavior is expected; individual occurrences, their scheduling, and what actually happens remain distinct concepts.**

A Routine may represent a simple recurring behavior, a flexible recurring expectation, or a structured recurring bundle of actions. It is not merely a stored recurrence expression and it is not the list of occurrences it produces.

Examples include:

- train Monday / Wednesday / Friday;
- brush teeth every evening;
- perform a weekly review every Sunday;
- take a medicine every 12 hours;
- replace a filter a fixed interval after the previous replacement;
- perform a backup after each photography session;
- execute a multi-step morning routine.

## Validation basis

Routine v0 was reviewed against:

- the LifeOS feature-discovery simulation, including flexible routines, cyclic shifts, medication, maintenance, sport, study, home management, temporary disruptions, and Goal progress from recurring execution;
- the existing LifeOS core glossary and scheduling-flexibility rules;
- the already accepted Goal v0, Plan v0, Activity v0, and Event v0 boundaries;
- external recurrence patterns from iCalendar/RFC 5545, Google Calendar recurring-series/exception behavior, Todoist recurrence semantics, and Microsoft Planner recurrence-series behavior.

External systems are benchmark inputs rather than models to copy directly.

## Routine versus recurrence

A recurrence rule describes a temporal or relational repetition pattern. A Routine represents a recurring behavioral or execution policy.

Therefore:

> **Routine != recurrence rule.**

The same future recurrence capability may be usable by recurring Events, Routine occurrences, reminders, or other temporal concepts without turning them all into Routines.

```text
Recurring Event
Team meeting every Monday at 10:00

Routine
Train Monday / Wednesday / Friday
```

The first is a recurring Event series because repeated occurrence is intrinsic to the Event series. The second is a recurring behavioral policy.

## Routine versus Activity

An Activity represents a concrete actionable intention. A Routine represents the persistent policy that expects or guides repeated execution.

```text
Routine
Take out trash every Thursday

Occurrence
Thursday 13 August

Execution Activity / Actual
Take out trash
```

The interface may describe this as a recurring task, but the domain must preserve the distinction between the recurring policy and each expected execution.

Therefore:

> **A recurring task in the UI does not require one Activity identity to be moved forward forever.**

LifeOS should preserve the series/policy separately from its individual occurrences and execution history.

## Routine versus Event

Recurring temporal occurrence alone does not make something a Routine.

```text
Recurring Event
University lesson every Tuesday at 09:00
```

remains an Event series.

```text
Routine
Study Tuesday and Thursday evenings
```

is a recurring behavioral policy.

Therefore:

> **Routine != recurring Event.**

The exact shared recurrence and occurrence machinery is deferred to the Temporal Model.

## Routine versus Goal

A Goal describes a condition or result the user wants to reach or sustain. A Routine describes the repeated execution policy used to produce behavior.

```text
Goal
Train at least 3 times per week

Routine
Gym Monday / Wednesday / Friday
```

The Goal may survive changes to the Routine. The Routine may also exist without an explicit Goal.

Therefore:

> **Routine != Goal.**

## Routine versus Plan

A Plan coordinates how a purpose is intended to be pursued or organized. A Routine coordinates a pattern that is expected to repeat.

A Plan may use one or more Routines:

```text
Plan
Half-marathon preparation

Routines
- easy run
- long run
- strength
```

A Routine may also exist independently of any Plan.

A complex Routine does not automatically become a Plan merely because it contains multiple steps. The dominant semantic distinction is whether the structure represents a repeating pattern/policy or a broader strategy coordinated toward a purpose.

### Progression guardrail

Validation Methodology v2 strengthened this boundary with long-horizon progression cases.

A Routine may be composite and may contain adaptive execution rules, but it should not become the default container for materially changing stages, strategy transitions, milestones, and several distinct recurring policies simply because those stages happen sequentially over time.

Example:

```text
Plan
12-week training progression

Stage 1
Routine A

Stage 2
Routine B

Stage 3
Routine C
```

is generally stronger than one mega-Routine that owns the entire 12-week progression, every phase transition, all milestones, and every changing policy.

Current guardrail:

> **Routine may contain repeated internal structure and adaptive execution rules, but coordination of materially changing stages, strategy, milestones, and multiple recurring policies tends toward Plan semantics.**

This is intentionally a semantic guardrail rather than an arbitrary threshold based on duration, number of steps, or number of child objects.

## Routine versus Template

A Template is a reusable structure that can be instantiated when needed. A Routine creates or governs repeated expectation over time.

```text
Template
Travel checklist

Routine
Weekly review every Sunday
```

A Routine may eventually reuse a Template, but they do not share the same lifecycle or semantics.

Therefore:

> **Routine != Template.**

## Routine versus Trigger

A Routine expresses repeated behavioral expectation. A Trigger detects a condition or event that may cause an action, notification, or rule to run.

```text
Routine
Replace filter every three months

Trigger
Alert when filter reaches X hours of use
```

Conditional automation such as arbitrary `if condition then action` must not be hidden inside Routine merely because it may eventually initiate recurring work.

Therefore:

> **Routine != Trigger.**

## Routine occurrence

A Routine is not a list of materialized executions. LifeOS requires the semantic concept of an expected occurrence belonging to the Routine.

```text
Routine
Gym Monday / Wednesday / Friday

Occurrence A
Monday

Occurrence B
Wednesday

Occurrence C
Friday
```

The exact physical representation and materialization strategy for Occurrence is deferred to the Temporal Model.

An occurrence may eventually carry or link to:

- its original expected time or valid window;
- current accepted scheduling;
- occurrence-specific exception data;
- execution Activity or Session where appropriate;
- Actual execution;
- Outcome and Confirmation;
- provenance and history.

## Occurrence exceptions do not rewrite the Routine

A one-off change belongs to the occurrence or its scheduling unless the user explicitly changes the future rule.

```text
Routine
Gym Wednesday 18:00

This Wednesday only
20:00
```

The Routine remains unchanged.

By contrast:

```text
From now on
Gym Wednesday 20:00
```

changes the future Routine policy.

LifeOS must be able to distinguish at least conceptually:

- this occurrence only;
- selected occurrences;
- future occurrences from an effective point;
- the complete Routine definition where historically meaningful.

## Effective-dated revisions

Structural changes to a Routine must not silently rewrite the rule that governed earlier occurrences.

```text
Routine revision v1
run 30 minutes Mon/Wed/Fri

effective later:
Routine revision v2
run 45 minutes Mon/Wed/Fri
```

Past occurrences remain explainable under the rule that was effective at the time.

The physical versioning mechanism is deferred to the Version/History model.

## Skip, pause, and end are distinct

LifeOS must not collapse these semantics.

### Skip occurrence

A specific expected occurrence is not executed.

The Routine remains active.

### Pause Routine

The Routine remains conceptually valid but future expectation is temporarily suspended or overridden.

### End Routine

The repeated policy is no longer expected to continue.

The exact lifecycle state machine remains deferred, but these semantic differences must be preserved.

Temporary modes such as illness, holiday, travel, exams, or intense work may suspend or modify selected Routine behavior without rewriting long-term policy.

## Recurrence anchor semantics

LifeOS must support more than one way to determine the next expected occurrence.

Required semantic families include at least:

### Calendar-anchored

```text
Every Monday at 18:00
```

### Wall-clock anchored

```text
Every day at 08:00 local time
```

This is not necessarily equivalent to an exact elapsed 24-hour interval across DST or timezone changes.

### Elapsed-interval anchored

```text
Every 12 elapsed hours
```

### Completion-anchored

```text
Replace filter 30 days after the previous replacement
```

If execution occurs late, the next expectation may be relative to the Actual completion rather than the previously planned date.

### Relation-anchored

```text
Backup photos after every photo shoot
Stretch after every workout
```

The exact relation to Trigger and dependency semantics remains deferred.

These are semantic requirements, not a decision to create one database enum per family.

## Flexible routines

A Routine need not prescribe one exact timestamp for every occurrence.

```text
Routine
Train 3 times per week

preferred days
Mon / Wed / Fri

preferred window
17:00-21:00

spacing
at least one recovery day where applicable
```

The Routine defines expected pattern/policy. A future scheduler may choose concrete placement according to availability, constraints, priorities, and user policy.

Therefore:

> **Routine policy != concrete Schedule.**

A missed preferred placement may be rescheduled without changing the underlying Routine when the Routine permits that flexibility.

## Composite routines

A Routine may govern a recurring bundle of actions.

```text
Morning Routine
- drink water
- medication
- breakfast
- prepare bag
- leave home
```

The bundle does not require five independent Routine identities merely because its execution contains multiple actions.

Individual steps may remain distinct Activities or structured execution components where their history/outcome matters.

A composite Routine does not automatically become a Plan: repetition remains its dominant semantic purpose.

The exact boundary between a structured Routine and a Plan should be rechecked during the intention/execution cluster checkpoint.

## Routine and Goal/Plan relationships

A Routine may exist without any Goal or Plan.

A Routine may also:

- support one or multiple Goals;
- belong to or be coordinated by one or multiple Plans where the future relationship model allows it;
- generate execution whose Actuals become Evidence for Goals not originally associated with the Routine.

As with Activity and Event, discovered relevance must not rewrite the original intention of the Routine.

## Planned execution, Actual, and evidence

Routine expectation is not Actual behavior.

```text
Routine
Walk every evening

Expected occurrence
Monday

Actual
no walk
```

or:

```text
Actual
8.4 km walk
```

Occurrence outcome and measurements can feed statistics, Goal criteria, future planning, and adaptation.

The passage of expected time does not prove execution.

## Adherence and streaks are derived

A Routine must not require canonical fields such as:

```text
streak = 42
adherence = 87%
```

These values are derived from occurrence history, Actuals, Outcomes, confirmation policy, and the evaluation period.

LifeOS must be able to compute useful adherence/trend views while avoiding punitive or misleading universal streak semantics.

## Replanning and fallback

When an expected occurrence cannot happen as planned, policy may permit outcomes such as:

- skip without replacement;
- postpone within a valid period;
- move to another acceptable time;
- replace with an equivalent execution;
- shorten or split where the generated Activity permits it;
- replan surrounding occurrences;
- temporarily pause the Routine;
- propose a structural Routine revision when repeated deviations indicate that the current policy is unrealistic.

A single deviation must not automatically rewrite the whole Routine.

## AI boundary

AI may propose:

- a Routine from user intent;
- recurrence/cadence options;
- occurrence rescheduling;
- exception handling;
- a future Routine revision;
- links to Goal or Plan;
- insights about adherence or recurring conflicts.

AI does not silently convert one-off behavior into a canonical Routine or alter a Routine's future policy when the change is material without the applicable user-control rule.

Repeated observed behavior may justify a proposal such as "Do you want to make this a Routine?" but observation alone is not canonical Routine intent.

## Current invariants

1. `Routine != Activity`.
2. `Routine != Event`.
3. `Routine != RecurrenceRule`.
4. `Routine != Schedule`.
5. `Routine != Template`.
6. `Routine != Trigger`.
7. `Routine != Goal`.
8. A Routine represents persistent recurring policy/pattern, not the list of occurrences it produces.
9. Individual occurrences require identity/history distinct from the Routine.
10. Changing one occurrence does not automatically change the Routine.
11. Skip occurrence, pause Routine, and end Routine are distinct semantics.
12. Future structural changes must be effective-dated/versionable without rewriting past occurrences.
13. A Routine may exist without Goal or Plan.
14. A Routine may support multiple Goals and may participate in multiple Plans subject to the future relationship model.
15. A Routine may govern a single recurring action or a structured recurring bundle.
16. Recurrence must support multiple anchor semantics rather than one universal fixed interval.
17. Wall-clock recurrence and elapsed-time recurrence must remain distinguishable.
18. Completion-relative recurrence must be possible where the next expectation depends on Actual completion.
19. Relation-anchored recurring behavior must be representable without turning Routine into a generic automation engine.
20. Routine policy and concrete Schedule are distinct.
21. Expected occurrence and Actual execution are distinct.
22. Adherence, streaks, and similar statistics are derived rather than universal canonical Routine state.
23. One-off deviations must not automatically rewrite the recurring policy.
24. A recurring Event series does not require a Routine.
25. A recurring Activity may be presented that way in the UI while using Routine + occurrence semantics in the domain.
26. Arbitrary condition-based automation belongs to Trigger/automation semantics rather than Routine itself.
27. Passage of time does not establish occurrence completion.
28. Repeated observed behavior does not automatically become canonical Routine intent.
29. History must preserve which Routine policy/revision governed each occurrence.
30. Exact recurrence materialization, timezone/DST behavior, and occurrence persistence remain Temporal Model concerns.
31. Routine may contain repeated internal structure and adaptive execution rules, but coordination of materially changing stages, strategy, milestones, and multiple recurring policies tends toward Plan semantics rather than being absorbed into one mega-Routine.

## Stress-test coverage

Routine v0 was checked against representative LifeOS cases including:

| Case | Current representation |
|---|---|
| Gym Mon/Wed/Fri | Routine + expected occurrences |
| Brush teeth nightly | simple Routine |
| Weekly review | Routine |
| Medication every 12 elapsed hours | elapsed-interval Routine |
| Medication at 08:00/20:00 local | wall-clock Routine |
| Replace filter after previous replacement | completion-anchored Routine |
| Team meeting every Monday | recurring Event, not Routine |
| University course every Tuesday | recurring Event series |
| Stretch after workout | relation-anchored Routine / future Trigger relation |
| Morning routine with multiple steps | composite Routine |
| Maintenance after 10,000 km | Trigger/maintenance condition, not simple temporal Routine |
| Train 3 times/week | Routine when execution policy; Goal when desired condition |
| 12-week staged training progression | Plan coordinating stage-specific Routines rather than one default mega-Routine |
| Move one gym session | occurrence exception |
| Holiday for two weeks | Routine pause/temporary override |
| Change Wednesday time from now on | effective future Routine revision |
| Miss one occurrence | occurrence outcome; Routine remains active |

No reviewed case currently requires representing Routine as Activity-with-repeat or as a generic automation primitive.

## Deliberately deferred questions

The following are not decided by Routine v0:

- exact Occurrence entity/value-object/persistence design;
- recurrence materialization strategy;
- timezone and DST algorithms;
- exact Routine lifecycle enum/state machine;
- exact versioning persistence;
- exact Routine-to-Plan/Goal relationship representation;
- precise relation-anchored recurrence versus Trigger boundary;
- precise composite Routine versus Plan boundary;
- exact generated Activity versus occurrence relationship;
- how far future occurrences are materialized or derived on demand;
- API and SQL representation.

## Decision note

Routine v0 supersedes the narrower repeated-pattern definition for the active Domain Model workstream by making the policy/occurrence/execution distinction explicit and by supporting flexible, interval-, completion-, wall-clock-, and relation-anchored behavior.

It does not replace existing product documents yet. Broader documentation will be reconciled deliberately after the intention/execution cluster checkpoint.