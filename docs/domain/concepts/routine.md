# Routine v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-10  
**Validation hardening:** 2026-08-11  
**Multi-actor wording hardening:** 2026-08-11  
**Meaning of accepted:** best current decision; reopenable with better evidence  
**Workstream:** Core Domain Model v0

## Canonical definition

> **A Routine is a persistent reusable policy that expresses a pattern of behavior or execution intentionally expected to repeat over time. A Routine governs when, how often, and under which rules that behavior is expected; performer/responsibility, individual Occurrences, their scheduling, and what actually happens remain distinct concepts.**

A Routine may represent a simple recurring behavior, a flexible recurring expectation, or a structured recurring bundle of actions. It is not merely a recurrence expression and it is not the list of Occurrences it produces.

The personal-first case usually has the user performing the repeated behavior. Multi-actor evidence shows that performer/responsibility may instead rotate or change by Occurrence without changing Routine identity.

Examples include:

- train Monday / Wednesday / Friday;
- brush teeth every evening;
- perform a weekly review every Sunday;
- take medicine every 12 elapsed hours;
- replace a filter a fixed interval after previous replacement;
- perform a backup after each photography session;
- execute a multi-step morning routine;
- take household recycling out every Thursday with rotating responsibility.

## Why the multi-actor wording changed

The original wording described a pattern `the user intends to repeat`.

That remains correct for personal V1 but accidentally implied:

```text
Routine identity = performer identity
```

Multi-actor scenarios demonstrate:

```text
Routine
Take recycling out every Thursday

Occurrence 1 -> Mattia
Occurrence 2 -> Luca
Occurrence 3 -> Sara
```

One repeating policy is sufficient. Three duplicate Routines are not required merely because the responsible/performing actor changes.

Therefore Routine semantics remain about the recurring policy, while performer/responsibility belong to separate relations/context.

## Validation basis

Routine v0 has been reviewed against:

- flexible routines, cyclic shifts, medication, maintenance, sport, study, home management and temporary disruptions;
- Goal progress from recurring execution;
- accepted Goal, Plan, Activity and Event boundaries;
- Time-cluster Occurrence, Schedule, Recurrence, Session and Actual distinctions;
- iCalendar/provider recurrence patterns, Todoist fixed/completion-relative recurrence and other mature recurrence behavior;
- long-horizon progression stress tests;
- multi-actor discovery/research involving household rotation, team/shared repetition, recurring care, responsibility transfer and external participants.

External systems are evidence, not design authorities.

## Routine versus Recurrence

Recurrence describes how a temporal/generative pattern repeats. Routine represents the recurring behavioral/execution policy using that pattern.

```text
Routine
Strength training

Recurrence
Mon / Wed / Fri
```

Therefore:

> **Routine != Recurrence.**

The same Recurrence capability may be used by recurring Event sources, Temporal Constraints, Availability rules or other approved semantics without turning them into Routines.

## Routine versus Activity

Activity represents actionable intended work. Routine represents persistent repeated execution policy.

```text
Routine
Take out trash every Thursday

Occurrence
Thursday 13 August

Activity / execution semantics
Take out trash
```

The UI may call this a recurring task, but the domain must preserve policy vs individual expectation/execution history.

Therefore:

> **A recurring task UI does not require one Activity identity to be moved forward forever.**

## Routine versus Event

Recurring temporal occurrence alone does not create Routine semantics.

```text
Recurring Event
University lesson every Tuesday 09:00
```

remains Event semantics.

```text
Routine
Study Tuesday and Thursday evenings
```

is repeated behavioral/execution policy.

Therefore:

> **Routine != recurring Event.**

## Routine versus Goal

Goal defines a desired condition/result/pattern. Routine defines repeated execution policy.

```text
Goal
Train >= 3 times/week

Routine
Gym Mon/Wed/Fri
```

Goal may survive Routine changes and Routine may exist without an explicit Goal.

Therefore:

> **Routine != Goal.**

## Routine versus Plan

Plan coordinates broader pursuit/strategy. Routine coordinates a repeated policy.

```text
Plan
Half-marathon preparation

Routines
- easy run
- long run
- strength
```

Routine may also exist independently.

### Progression guardrail

A Routine may be composite/adaptive but should not become the default container for materially changing long-horizon stages, strategy transitions, milestones and multiple distinct recurring policies.

```text
Plan
12-week training progression

Stage 1 -> Routine A
Stage 2 -> Routine B
Stage 3 -> Routine C
```

is generally stronger than a mega-Routine owning the full staged strategy.

Canonical guardrail:

> **Routine may contain repeated internal structure and adaptive execution rules, but coordination of materially changing stages, strategy, milestones and multiple recurring policies tends toward Plan semantics.**

No arbitrary duration/step count defines the boundary.

## Routine versus Template

Template is reusable structure instantiated when needed. Routine generates/governs repeated expectation.

```text
Template
Travel checklist

Routine
Weekly review Sunday
```

Therefore:

> **Routine != Template.**

A Routine may reuse a Template without sharing lifecycle.

## Routine versus Trigger

Routine expresses repeated expected behavior/execution. Trigger detects a condition/event and may cause action/notification/rule execution.

```text
Routine
Replace filter every 3 months

Trigger
Alert when usage reaches X hours
```

Therefore:

> **Routine != Trigger.**

Arbitrary `if condition then action` logic must not be hidden inside Routine.

## Routine versus observed habit/pattern

Repeated observed behavior does not automatically become an intended Routine.

```text
Observation
Usually reads around 22:30
```

may justify:

```text
AI proposal
Do you want to protect reading time in the evening?
```

but must not silently create:

```text
Routine
Read every evening
```

Canonical rule:

> **Observed repeated behavior != canonical Routine intent.**

This distinction is essential for future personal-learning/preference intelligence.

## Routine Occurrence

Routine is not a materialized list of executions.

```text
Routine
Gym Mon/Wed/Fri
        ↓
Occurrence A
Occurrence B
Occurrence C
```

An Occurrence may carry/link to:

- generation/source context;
- original expectation;
- current Schedule;
- occurrence-specific exception;
- responsible/assigned actor where later supported;
- Activity/Session/Actual;
- Outcome/Confirmation;
- provenance/history.

## Performer/responsibility does not define Routine or Occurrence identity

Multi-actor hardening:

> **Routine identity != performer.**

> **Occurrence identity != assigned/responsible actor.**

A one-off change in who performs an Occurrence normally changes an actor relationship/state, not the Routine and not the Occurrence identity.

Example:

```text
Routine
Household bin night every Thursday

Occurrence
13 August
originally responsible: Mattia
substitution: Luca
```

The expected Thursday instance remains the same Occurrence.

## Responsibility rotation is not Recurrence identity

A repeated responsibility pattern may later reuse recurrence/rule machinery, but Recurrence itself answers `how does the expected pattern repeat?`, not `who gets assigned next?`.

Therefore:

> **Recurrence must not become a generic assignment-rotation engine.**

Exact rotation/responsibility policy belongs to later Relationship/Responsibility review.

## Occurrence exceptions do not rewrite Routine

One-off placement/assignment changes remain occurrence-specific unless future policy is explicitly revised.

```text
Routine
Gym Wednesday 18:00

This Wednesday only
20:00
```

Routine remains unchanged.

```text
From now on
Wednesday 20:00
```

changes future policy.

Likewise:

```text
This occurrence only
Luca substitutes for Mattia
```

must not automatically rewrite long-term responsibility policy.

## Effective-dated revisions

Structural Routine changes must not silently rewrite the policy governing earlier Occurrences.

```text
v1
Run 30m Mon/Wed/Fri

later effective v2
Run 45m Mon/Wed/Fri
```

Past Occurrences remain explainable under the effective rule/version.

Exact version persistence is deferred.

## Skip, pause and end are distinct

### Skip Occurrence

One expected instance is not executed; Routine remains active.

### Pause Routine

Routine remains conceptually valid but future expectation is temporarily suspended/overridden.

### End Routine

Repeated policy is no longer expected to continue.

Temporary modes such as illness, holiday, travel, exams or intense work may alter execution without rewriting stable long-term policy.

## Recurrence semantic families

Routine may use several recurrence families; Routine itself does not define their implementation.

Examples:

### Calendar/wall-clock

```text
Every Monday at 18:00
Every day at 08:00 local
```

### Elapsed interval

```text
Every 12 elapsed hours
```

### Quota

```text
3 times per week
```

### Completion-relative

```text
Replace filter 30 days after Actual previous replacement
```

### Relation/anchor-stream relative

```text
Backup after every qualifying photo Session
```

Exact semantics live in Recurrence v0.

## Flexible Routine

Routine need not prescribe exact timestamp per Occurrence.

```text
Routine
Train 3 times/week

preferences
Mon/Wed/Fri
17:00-21:00

spacing
recovery where applicable
```

Routine defines expected policy; scheduler may select placements based on constraints, availability, capacity and policy.

Therefore:

> **Routine policy != concrete Schedule.**

## Composite Routine

Routine may govern a recurring bundle:

```text
Morning Routine
- water
- medication
- breakfast
- prepare bag
- leave home
```

The bundle does not require one Routine per step.

Individual steps may remain Activities/components where their own history/Outcome matters.

Repetition remains the dominant semantic; long-horizon strategic stage changes tend toward Plan.

## Routine and Goal/Plan relationships

Routine may exist without Goal/Plan.

It may:

- support multiple Goals;
- be coordinated by multiple Plans where future relationships allow;
- generate Actuals/Evidence later relevant to Goals not originally associated with it.

Discovered relevance must not rewrite original Routine intent.

## Planned execution, Actual and Evidence

Routine expectation is not Actual behavior.

```text
Routine
Walk every evening

Occurrence
Monday

Actual
no walk
```

or:

```text
Actual
8.4 km walk
```

Passage of expected time does not prove execution.

## Adherence and streaks are derived

Routine does not require canonical fields:

```text
streak = 42
adherence = 87%
```

These are derived from Occurrence history, Actuals, Outcomes, confirmation policy and evaluation period.

Useful trend views remain possible without universal punitive streak semantics.

## Replanning and fallback

Policy may permit:

- skip without replacement;
- postpone within valid period;
- move to another acceptable time;
- equivalent replacement;
- shorten/split generated execution;
- replan surrounding Occurrences;
- temporarily pause;
- propose structural revision after repeated unrealistic deviations.

One deviation must not automatically rewrite Routine.

## AI boundary

AI may propose:

- Routine from explicit intent;
- cadence/Recurrence;
- rescheduling;
- occurrence exception handling;
- future Routine revision;
- Goal/Plan links;
- insights about adherence/conflicts;
- responsibility/rotation suggestions where authorized.

AI must not:

- silently convert observation into Routine;
- materially alter future policy without applicable authority/policy;
- assign another actor without authority;
- treat recurring observed behavior as consent;
- reveal private reasons behind another actor's availability.

## Multi-actor evidence hardening

Research/discovery confirms:

```text
Routine identity != one mandatory performer
Occurrence identity != assigned actor
assignment exception != Routine revision
responsibility rotation != Recurrence identity
observed group behavior != shared Routine intent
```

A genuinely shared repeated policy may later have multiple stakeholders/governors while preserving one Routine identity.

Independent personal routines should not be merged solely because their schedules/behavior look similar.

## Current invariants

1. `Routine != Activity`.
2. `Routine != Event`.
3. `Routine != Recurrence`.
4. `Routine != Schedule`.
5. `Routine != Template`.
6. `Routine != Trigger`.
7. `Routine != Goal`.
8. `Routine != observed habit/pattern`.
9. Routine represents persistent repeated policy, not produced Occurrences.
10. Individual Occurrences require distinct identity/history.
11. Changing one Occurrence does not automatically change Routine.
12. Skip Occurrence, pause Routine and end Routine are distinct.
13. Structural future changes are effective-dated/versionable without rewriting history.
14. Routine may exist without Goal/Plan.
15. Routine may support multiple Goals/Plans subject to future relationship semantics.
16. Routine may govern one recurring action or a structured recurring bundle.
17. Recurrence supports materially distinct temporal/generative families.
18. Wall-clock and elapsed recurrence remain distinguishable.
19. Completion-relative generation can depend on qualifying Actual.
20. Relation-anchored behavior must not make Routine a generic automation engine.
21. Routine policy and concrete Schedule are distinct.
22. Expected Occurrence and Actual execution are distinct.
23. Adherence/streaks are derived rather than universal state.
24. One-off deviations do not automatically rewrite recurring policy.
25. Recurring Event series does not require Routine.
26. Recurring task UI may map to Routine + Occurrence semantics.
27. Generic condition automation belongs to Trigger/automation semantics.
28. Passage of time does not establish completion.
29. Repeated observed behavior does not create Routine intent automatically.
30. History preserves which Routine policy/version governed each Occurrence.
31. Materially changing long-horizon stages/strategy tend toward Plan rather than mega-Routine.
32. Routine identity is independent from one mandatory performer.
33. Occurrence responsibility/performer changes do not automatically change Occurrence/Routine identity.
34. Responsibility rotation is not Recurrence's core meaning.
35. AI does not gain authority to create shared/assigned Routine behavior merely from inferred patterns.

## Stress-test coverage

| Case | Representation |
|---|---|
| Gym Mon/Wed/Fri | Routine + Occurrences |
| Brush teeth nightly | simple Routine |
| Weekly review | Routine |
| Medication every 12 elapsed hours | elapsed-interval Routine |
| Medication 08:00/20:00 local | wall-clock Routine |
| Replace filter after previous replacement | completion-relative Routine |
| Team meeting Monday | recurring Event, not Routine |
| University course Tuesday | recurring Event source |
| Stretch after workout | relation-anchored Routine / future Trigger boundary |
| Morning multi-step sequence | composite Routine |
| Maintenance after 10,000 km | Trigger/usage condition, not ordinary temporal Routine |
| Train 3x/week | Routine when policy; Goal when desired condition |
| 12-week staged training | Plan with stage-specific Routines |
| Move one gym occurrence | Occurrence/Schedule exception |
| Holiday two weeks | pause/temporary override |
| Change Wednesday time from now | effective future revision |
| Miss one occurrence | Occurrence outcome; Routine remains |
| Household chore rotates people | one Routine + occurrence-specific responsibility |
| One-off substitute | same Occurrence, actor relation changes |
| Repeated observed evening reading | Observation/pattern; possible Routine proposal, not automatic Routine |

No reviewed case requires representing Routine as Activity-with-repeat, per-actor duplicate Routines, or a generic automation/assignment engine.

## Deliberately deferred questions

- exact Routine lifecycle state machine;
- exact version persistence;
- final Routine-to-Goal/Plan relationships;
- Responsibility/Assignment/rotation policy model;
- shared Routine governance;
- Actor/Person/Account/Principal model;
- exact generated Activity/Occurrence relationship;
- precise relation-anchored Recurrence vs Trigger boundary;
- composite Routine vs Plan edge cases;
- future materialization horizon;
- API/SQL representation.

## Decision note

Routine v0 remains the accepted recurring behavioral/execution-policy primitive.

The 2026-08-11 hardening generalizes the policy beyond one mandatory performer while preserving all prior Time/Occurrence/Recurrence/history boundaries.

---

# 2026-08-13 — Version / material-equivalence downstream closure amendment

Version v0 resolves Routine's former `exact version persistence` semantic dependency without changing Routine identity.

```text
Routine identity
= persistent recurring behavioral/execution policy

Routine material state
= materially relevant policy state governing future/occurrence generation

Version
= reference to that material state for the relevant purpose
```

A material policy revision (for example 30m → 45m, cadence change, eligibility or structural rule change) produces a later material Routine state while preserving the same Routine identity unless the change actually redefines the policy into a different Routine. Past Occurrences remain bound to the Routine state that generated/governed them.

Occurrence-specific exceptions do not become Routine Versions by default. A one-off reschedule or performer substitution stays occurrence-specific unless the persistent policy itself changes.

Non-material edits may preserve applicability where the relevant policy facet is unchanged. Technical row versions/provider revisions do not define Routine materiality automatically. Routine Version history may branch under offline/concurrent edits; reconciliation/Authority/Decision choose current policy, not Version itself.

AI proposals to revise a Routine should preserve the material base state; stale proposals must be re-evaluated after material divergence rather than silently applied.

The historical version-persistence dependency is now downstream-closed semantically. Lifecycle state, Responsibility/rotation, shared governance, Trigger boundary, materialization horizon and physical persistence remain separately owned.

No Routine hardening failed. **Routine remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `version.md`;
- `../checkpoints/version-material-equivalence-v0-validation.md`.