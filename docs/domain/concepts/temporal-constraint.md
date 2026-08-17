# Temporal Constraint v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-11  
**Meaning of accepted:** best current decision; reopenable with better evidence  
**Workstream:** Core Domain Model v0 — Time cluster

## Canonical definition

> **A Temporal Constraint is a rule that restricts or prefers the temporal placement, duration, or temporal relationship of a domain subject. It defines where in time execution or occurrence is permitted, required, bounded, or preferred; it does not itself choose the accepted Schedule and does not describe what actually happened.**

A Temporal Constraint answers questions such as:

> **When may this happen?**  
> **When must this happen?**  
> **By when must a relevant temporal condition be satisfied?**  
> **How long may or should an execution slice be?**  
> **How far apart must two related executions be?**  
> **What temporal relationship must hold between this subject and another fact or subject?**

It does **not** by itself answer:

- what the domain subject fundamentally is;
- when the subject is currently scheduled;
- whether the subject actually occurred or was executed;
- whether the user is available or busy;
- whether a target date was achieved;
- whether a Goal or Milestone is complete;
- whether a temporal violation implies a business outcome such as `missed`;
- who is allowed to change the Schedule or the constraint itself;
- whether a recurring pattern should generate Occurrences.

The core temporal separation is:

```text
Temporal Constraint
= what time is allowed / required / preferred

Schedule
= what time is currently accepted

Session / Event Actual
= what time actually happened
```

---

## Why this concept exists

The accepted Time-cluster concepts already require a temporal rule layer that is distinct from accepted placement and actual execution.

`Schedule v0` intentionally rejects a calendar-object model in which every date-like fact becomes part of Schedule. It requires deadlines, target dates, valid/preferred windows, movement policy, recurrence, and capacity to remain separate from accepted temporal assignment.

`Session v0` requires actual execution to remain recordable even when it violates a previous temporal expectation or planning rule.

`Occurrence v0` requires one generated instance to retain identity independently from where or whether it is scheduled.

The earlier LifeOS scheduling documentation already identified multiple temporal semantics, including:

- fixed placement;
- bounded execution windows;
- deadlines;
- preferred windows;
- open scheduling;
- minimum duration;
- spacing and recovery requirements;
- movement policies that may differ from temporal validity.

Those concerns cannot be represented safely with one `due_at`, one `window`, or one `flexible` boolean.

A general Temporal Constraint capability is therefore justified because the same fundamental rule type appears across study, work, health, medication, maintenance, travel, projects/plans, routines, deadlines, recovery rules, and event-relative actions.

---

## Validation basis

Temporal Constraint v0 was reviewed against:

### Existing LifeOS documentation

- `docs/product/v1-scheduling-flexibility.md`;
- `docs/product/v1-execution-status.md`;
- `docs/product/v1-core-domain-glossary.md`;
- `docs/product/feature-discovery-simulation-2026-08.md`;
- the accepted Domain Atlas concepts Goal, Plan, Activity, Event, Routine, Milestone, Occurrence, Schedule, and Session;
- the validated Intention & Execution cluster checkpoint.

### Representative LifeOS scenarios

The review included:

- submit a report by Friday;
- begin treatment no later than Monday;
- perform a blood test only between 07:00 and 09:00;
- study preferably between 17:00 and 21:00;
- do not schedule meetings during lunch;
- maintain at least 48 hours of recovery between hard workouts;
- take medication no earlier than a defined interval after a prior dose;
- complete a follow-up within seven days after a medical visit;
- keep a focus session at least 45 minutes and at most 90 minutes;
- execute a maintenance action during a valid date range;
- distinguish a Goal target date from an application deadline;
- revise an external deadline and subsequently replan work;
- record Actual execution that violated a hard planning rule;
- detect an impossible set of simultaneous hard constraints;
- preserve date-only, floating-local, named-zone, and instant boundaries;
- apply Plan/Routine-level rules without duplicating them onto every governed child;
- apply an Occurrence-specific temporal exception without rewriting the source policy.

### External benchmark patterns

External systems were used as evidence rather than copied as LifeOS ontology.

Relevant patterns include:

- **RFC 5545 / iCalendar** distinguishes scheduled start (`DTSTART`) from due boundary (`DUE`), and supports both `DATE` and `DATE-TIME` semantics;
- **Microsoft Graph / To Do** distinguishes start, due, and completion timestamps rather than collapsing them into one temporal field;
- calendar and scheduling systems generally distinguish accepted placement from constraints, recurrence, and availability even when their physical schemas differ.

These benchmarks reinforce the semantic separation required by the LifeOS model.

---

## Core model

Conceptually:

```text
Domain subject
Activity / Event / Occurrence / Plan / Routine / Milestone / other reviewed type
             │
             ↓
     Temporal Constraint(s)
             │
      ┌──────┼───────────────┐
      │      │               │
  boundary  window        duration
      │      │               │
      ├──── spacing / relative relationship
      │
      └──── hard or soft semantics
             │
             ↓
          Schedule
             │
             ↓
     Session / Event Actual
```

The same domain subject can have multiple independent constraints.

Example:

```text
Activity
Study chapter 5

Constraints
- earliest start: 17:00
- latest completion: 22:00
- minimum contiguous duration: 60 min
- preferred window: 18:00 -> 20:00

Schedule
18:30 -> 19:30
```

The Schedule is one accepted choice satisfying the applicable rule set; it is not the rule set itself.

---

# Temporal Constraint versus Schedule

This is the primary boundary.

```text
Temporal Constraint
Tuesday afternoon is an allowed execution window
```

means:

> execution may be placed there.

```text
Schedule
Tuesday afternoon
```

means:

> this is the currently accepted placement.

The temporal geometry may be identical while the semantics differ.

Therefore:

> **Temporal Constraint != Schedule.**

A constraint may exist with no Schedule.

Example:

```text
Activity
Renew insurance

Constraint
complete by 31 August

Schedule
none yet
```

This is a valid state.

---

# Temporal Constraint versus Session / Actual

A constraint expresses planning validity or preference.

A Session or other Actual record expresses reality.

Example:

```text
Constraint
Workout must finish by 20:00

Schedule
18:30 -> 19:30

Session
18:45 -> 20:15
```

The Session is not rejected merely because reality violated the rule.

LifeOS may derive:

```text
constraint violation
15 minutes
```

but must preserve the real execution.

Therefore:

> **Hard for planning does not mean impossible to record in reality.**

This rule is essential for trustworthy history.

---

# Temporal Constraint versus Recurrence

A temporal constraint may repeat, but repetition is not the constraint itself.

Example:

```text
Constraint intent
Study only on weekdays between 17:00 and 21:00
```

contains a recurring pattern.

The exact recurrence representation belongs to `Recurrence v0` review.

Temporal Constraint therefore defines the rule semantics while Recurrence will define how a repeating temporal pattern is expressed/generated.

> **Temporal Constraint != Recurrence.**

No `RRULE`-style machinery is accepted as part of the Temporal Constraint kernel at this stage.

---

# Temporal Constraint versus Availability / Capacity

Example:

```text
Availability
User is free 18:00 -> 20:00
```

is a statement about capacity or availability.

```text
Temporal Constraint
Never schedule workouts after 20:00
```

is a rule applied to a schedulable subject even if the user is technically free later.

The concepts may interact, but they are not identical.

> **Temporal Constraint != Availability / Capacity.**

The exact boundary is deferred to the later Calendar Block / Availability / Capacity review.

---

# Temporal Constraint versus Movement Policy

A constraint says what placements are valid or preferred.

A movement policy says who/what may alter an accepted placement and under which authority.

Example:

```text
Hard deadline
Friday 17:00

Schedule
Thursday 15:00 -> 16:00

Movement policy
AI may replan freely before the deadline
```

and:

```text
same hard deadline
same Schedule

Movement policy
locked unless user explicitly approves change
```

share the same Temporal Constraint but different movement authority.

Therefore:

> **Temporal Constraint != Movement Policy.**

---

# Temporal Constraint versus Goal / Milestone target

A target date expresses desired timing of an outcome.

A Temporal Constraint limits admissible planning/execution.

Example:

```text
Goal
Reach B2

Target date
31 December
```

normally means:

> the user wants the outcome by that horizon.

It does not necessarily mean:

> after 31 December the Goal becomes temporally invalid.

Similarly:

```text
Milestone
Master approved

Target
15 September
```

may still be achieved on 18 September.

The target was missed, but the Milestone remains meaningful.

By contrast:

```text
External submission deadline
15 September 23:59
```

is a latest-bound constraint: after that point the original submission condition is no longer satisfied unless the rule itself changes or an explicit exception exists.

Therefore:

> **Target date/window != Temporal Constraint by default.**

A product workflow may intentionally convert a target into a hard planning rule, but this must be explicit rather than assumed.

---

# Temporal Constraint versus Review Date

A review date means the user/system intends to reassess something at a point in time.

Example:

```text
Goal
Improve sleep

Review date
1 October
```

This does not mean the Goal must be achieved by 1 October.

The review date may later drive a Reminder/Event/Review Queue mechanism, but it is not automatically a constraint on Goal achievement.

> **Review date != Temporal Constraint by default.**

---

# Deadline semantics

`Deadline` is accepted as a **specialized latest-bound Temporal Constraint**, not an independent kernel primitive parallel to Temporal Constraint.

Canonical semantic definition:

> **A Deadline is a latest-bound Temporal Constraint requiring a specified temporal condition to be satisfied no later than a defined boundary.**

This means `Deadline` is useful domain/product vocabulary while sharing the general Temporal Constraint model.

---

## Deadline must constrain a meaningful temporal condition

The phrase:

```text
Deadline: Friday
```

is not universally precise enough.

It may mean:

```text
start <= Friday
```

or:

```text
completion <= Friday
```

or:

```text
delivery <= Friday
```

or another domain-specific temporal fact.

Examples:

```text
Submit report by Friday
```

normally constrains completion/delivery.

```text
Begin treatment no later than Monday
```

constrains start.

```text
Arrive at airport by 08:30
```

constrains arrival.

LifeOS must therefore preserve which temporal aspect the deadline constrains when that distinction matters.

It must not implement a universal rule equivalent to:

```text
Deadline == subject.end_at
```

---

## Deadline versus due date

User-facing language may use `due date` and `deadline` differently depending on context.

The domain concern is not the label; it is the latest-bound rule semantics.

A due date that behaves only as a soft reminder may actually be a target/preference.

A due date after which execution becomes invalid behaves as a hard latest-bound constraint.

The product may expose different wording while the domain preserves the actual semantics.

---

## Passing a deadline is not automatically an outcome

Example:

```text
Activity
Submit report

Deadline
Friday 17:00
```

At 17:01 LifeOS knows:

```text
current time > deadline boundary
```

but may not yet know whether:

```text
submitted at 16:58
```

or:

```text
not submitted
```

or:

```text
submitted late at 17:05
```

Therefore the passage of a deadline may produce a derived temporal condition such as:

```text
past deadline
```

but does not by itself establish a canonical execution outcome such as `missed`.

Outcome semantics remain in the later Actual / Outcome / Confirmation cluster.

This preserves the LifeOS rule:

> **Time passing does not silently establish what happened.**

---

# Window semantics

`Window` is not accepted as one independent kernel primitive because the same range shape can carry several materially different meanings.

A window is therefore treated as a **range-shaped temporal expression inside a typed semantic context**.

---

## Hard validity window

Example:

```text
Blood test
Valid execution window
07:00 -> 09:00
```

Meaning:

> execution must satisfy the specified relationship with this interval.

An automated planner should not silently schedule the blood test at 10:30.

---

## Preferred window

Example:

```text
Study
Preferred window
17:00 -> 21:00
```

Meaning:

> prefer placement inside this interval, but a valid placement outside it may be acceptable according to policy.

This is a soft Temporal Constraint.

---

## Target window

Example:

```text
Goal
Reach target weight

Target window
November -> December
```

This is primarily desired-outcome timing, not automatically a scheduling-validity constraint.

It remains part of Goal/Milestone target semantics unless explicitly promoted into a planning constraint.

---

## Availability window

Example:

```text
User availability
17:00 -> 21:00
```

belongs to Availability/Capacity semantics, not Temporal Constraint merely because it is a range.

---

## Accepted Schedule window

Example:

```text
Schedule
Tuesday afternoon
```

means the range/coarse period is the accepted placement itself.

Again:

> **Identical temporal shape does not imply identical domain meaning.**

---

# Hard versus soft constraints

Temporal constraints require at least two conceptual strength classes.

## Hard constraint

A hard constraint defines planning admissibility.

An automated Schedule is not valid if it violates a hard constraint unless an explicit override/change with sufficient authority is applied.

Example:

```text
Workout
not before 07:00
```

Schedule proposal:

```text
06:30 -> 07:30
```

is invalid under the current hard rule.

## Soft constraint / preference

A soft constraint influences optimization but does not by itself define invalidity.

Example:

```text
Workout
prefer 17:00 -> 20:00
```

If the only feasible placement is:

```text
12:00 -> 13:00
```

LifeOS may propose it while explaining the trade-off, depending on user policy.

Conceptually:

```text
Hard constraints
-> define admissibility

Soft constraints
-> influence optimization/ranking
```

The precise scoring/priority model is deferred.

---

# Constraint strength is not authority or mutability

This is a critical distinction.

A rule may be hard for the scheduler while still being user-editable.

Example:

```text
Self-imposed deadline
Friday
hard for automatic scheduling
```

The user may explicitly change it to Monday.

That is a **constraint revision**, not the scheduler silently violating the current rule.

By contrast:

```text
External application deadline
Friday 23:59
```

may be externally authoritative.

LifeOS should not rewrite it to Monday because the plan became difficult.

It may instead report infeasibility and suggest actions.

Therefore at least these conceptual dimensions remain separate:

```text
constraint strength
hard / soft

constraint authority / mutability
who may change or override the rule
```

Exact authority structures belong to later policy/provenance design.

---

# Boundary constraints

Temporal Constraint must support lower and upper bounds rather than only deadlines.

## Earliest-start / not-before

Example:

```text
Medication
not before 20:00
```

Conceptually:

```text
actual/planned relevant start >= boundary
```

## Latest-start

Example:

```text
Begin treatment no later than Monday 09:00
```

Conceptually:

```text
start <= boundary
```

## Latest-completion / deadline

Example:

```text
Submit application by Friday 23:59
```

Conceptually:

```text
completion/delivery <= boundary
```

## Earliest-completion

Less common but valid.

Example:

```text
Do not finalize the legal filing before the review period ends
```

Conceptually:

```text
completion >= boundary
```

The physical field representation is deferred; the semantic family is accepted.

---

# Containment and range relationship semantics

A bounded window does not always mean the same relation.

Given:

```text
Window
17:00 -> 18:00
```

possible rules include:

```text
start must fall inside the window
```

or:

```text
completion must fall inside the window
```

or:

```text
the entire execution must fit inside the window
```

or:

```text
execution must overlap the window
```

Example:

```text
Activity duration
90 min

Window
17:00 -> 18:00

Schedule
17:30 -> 19:00
```

The schedule satisfies `start inside window` but violates `full execution contained in window`.

Therefore LifeOS must not model a window merely as `min_at/max_at` without preserving the rule relationship that gives the range meaning.

---

# Duration constraints

Temporal Constraint also includes rules about execution/session duration where the duration itself is part of admissibility or preference.

Example:

```text
Study session
minimum contiguous duration
45 min
```

This is not equivalent to:

```text
estimated effort = 45 min
```

The first means:

> a planned/executed slice shorter than 45 minutes does not satisfy this policy.

The second is an estimate of how much effort is expected overall.

Other valid examples:

```text
maximum focus Session
90 min
```

```text
minimum appointment block
30 min
```

```text
preferred workout duration
45-60 min
```

Hard/soft semantics may apply to duration constraints as well.

---

# Spacing and recovery constraints

Many real LifeOS scenarios require a relationship between separate executions rather than an absolute time boundary.

Example:

```text
Hard workout
minimum recovery spacing
48h
```

Conceptually:

```text
next relevant start
>=
previous relevant completion + 48h
```

Other examples:

```text
Medication dose
at least 8h after previous dose
```

```text
Language practice
prefer no more than 3 days between sessions
```

```text
Maintenance action
not more often than once every 30 days
```

The exact source-selection relationship (`previous relevant Session`, `previous completed Occurrence`, etc.) will require coordination with Recurrence, Actual, and Relationship models.

The semantic requirement is accepted now.

---

# Relative temporal constraints

A Temporal Constraint may be relative to another Event, Milestone, Activity, Session, Occurrence, Observation, or later reviewed temporal fact.

Examples:

```text
Follow-up Activity
must start >= 30 min after Event ends
```

```text
Medical follow-up
must occur within 7 days after visit
```

```text
Activity B
must complete <= 48h after Milestone A is reached
```

```text
Recovery Session
prefer >= 24h after hard workout Session
```

The relationship model will later determine how references are persisted and validated.

Temporal Constraint v0 only establishes that **relative temporal relationships are first-class semantics**, not special-case metadata.

---

# Forbidden windows

A rule may exclude a temporal interval.

Example:

```text
No meetings
12:30 -> 14:00
```

This may exist even if the user is otherwise technically available.

It is therefore not necessarily Availability.

Conceptually it is equivalent to an exclusion constraint:

```text
Schedule placement must not satisfy forbidden overlap relation
```

Exact normalized representation is deferred.

---

# Multiple simultaneous constraints

A subject may be governed by several constraints at once.

Example:

```text
Activity
Study

Constraints
- earliest start: 17:00
- latest completion: 22:00
- minimum duration: 60 min
- preferred window: 18:00 -> 20:00
```

Schedule:

```text
18:30 -> 19:30
```

satisfies the full set.

The model must support composition rather than forcing one universal temporal rule field.

---

# Hard constraint conflict and infeasibility

Example:

```text
earliest start
20:00

latest completion
20:30

minimum duration
60 min
```

There is no valid Schedule satisfying all three.

LifeOS must not silently choose one hard rule to ignore.

The current planning problem is:

```text
INFEASIBLE
```

LifeOS may then explain the conflict and propose authorized changes such as:

- revise the deadline;
- reduce the minimum duration if allowed;
- change the earliest-start rule;
- split/replace execution if the domain permits;
- alter another surrounding commitment;
- request user decision.

The exact planner/optimizer API is deferred, but this invariant is fundamental:

> **A complete-looking schedule is not valid if it silently violates hard constraints.**

---

# Soft constraint conflicts

Preferences may conflict without making planning impossible.

Example:

```text
prefer morning
prefer after gym
prefer uninterrupted 90 min
```

The scheduler may be unable to satisfy all simultaneously.

This is an optimization problem rather than an admissibility failure.

The future scheduler may use priorities, weights, user preferences, context, or learned policies.

Temporal Constraint v0 does not define the optimizer; it preserves the distinction between hard validity and soft preference.

---

# Constraints at different scopes

A constraint does not need to be duplicated physically onto every individual child object.

Examples:

```text
Plan
Exam preparation

Constraint
valid execution horizon: 1 Sep -> 30 Nov
```

may govern relevant Plan execution.

```text
Routine
Workout

Constraint
weekdays only
```

may govern generated Occurrences.

```text
Occurrence #27
Exception constraint
Saturday also allowed
```

may alter only one instance without rewriting the entire source policy.

Therefore the conceptual model must support:

```text
constraint declared at a scope
        ↓
effective on governed subjects
        ↓
possible more-specific override/exception
```

The exact inheritance/scoping graph belongs to later Relationship/Persistence work.

The current rule is:

> **Do not duplicate identical governing constraints onto every child merely to make querying easy.**

---

# Constraint revision versus Schedule revision

These are different facts.

Example:

```text
Original external deadline
Friday
```

changes officially to:

```text
New deadline
Monday
```

The constraint changed.

An existing Schedule may remain unchanged or may subsequently be replanned.

Conceptually:

```text
Constraint revision
        ↓
may cause
Schedule revision
```

LifeOS should be able to explain:

> The Activity moved because the governing deadline changed.

If constraint and Schedule were collapsed into one field, this causal explanation would be lost.

---

# Constraint history and provenance

Material rule changes must not silently rewrite history when the earlier rule mattered to planning, analytics, integrations, or decisions.

Example:

```text
Original deadline
Friday 17:00
source: external provider

Revised deadline
Monday 17:00
source: external provider update
```

LifeOS should preserve enough history to answer:

- what rule was believed/accepted at a given time;
- when it changed;
- who or what changed it;
- which Schedule decisions were made under the old rule;
- whether the change was correction, external revision, user override, or policy revision.

Exact event/version persistence is deferred to later history/provenance modeling.

---

# Hard rule override versus rule revision

These must remain conceptually distinguishable.

## Rule revision

```text
Deadline Friday -> Monday
```

means the governing rule changed.

## One-off override / exception

```text
Rule remains Friday generally
but this specific Occurrence receives an authorized exception
```

means the base rule remains and a narrower exception applies.

This distinction is especially important for Routine/recurring Event Occurrences.

The exact effective-dating mechanics will be coordinated with Recurrence and Versioning.

---

# Constraint violation as derived state

LifeOS should prefer deriving many violation labels from constraint versus Schedule/Actual comparison rather than storing them as foundational truth.

Examples:

```text
late completion
```

```text
started too early
```

```text
outside preferred window
```

```text
minimum spacing violated
```

```text
maximum duration exceeded
```

The facts are:

```text
Constraint
Schedule / Actual
```

The violation classification is derived according to the rule semantics.

A material user-confirmed override/reason may still deserve audit/provenance.

---

# Hard constraint violation by Schedule versus by Actual

These cases differ.

## Invalid planned placement

```text
Hard window
07:00 -> 09:00

Schedule proposal
10:00 -> 10:30
```

The automated proposal is inadmissible unless an authorized rule change/override occurs.

## Real execution outside hard window

```text
Accepted Schedule
08:00 -> 08:30

Session
09:15 -> 09:40
```

Reality is recorded.

LifeOS may derive a violation and evaluate downstream consequences, but it must not erase or reject Actual.

This distinction preserves both safe planning and truthful history.

---

# Exact, date-only, floating, zoned, and instant boundaries

Constraint boundaries must preserve the user's/source's actual temporal precision and anchoring semantics.

Example:

```text
Deadline
30 April
```

must not be silently normalized to:

```text
30 April 00:00 UTC
```

without a defined semantic rule.

Relevant boundary forms may include:

- date-only inclusive day;
- exact local date/time with named timezone;
- floating local date/time;
- absolute instant;
- coarse period such as morning/afternoon where product semantics support it;
- relative boundary derived from another temporal fact.

The same false-precision rule accepted by Schedule applies here:

> **Do not invent temporal precision that the original constraint did not contain.**

DST/timezone/travel behavior remains a shared concern to be stress-tested further during Recurrence.

---

# Inclusive/exclusive boundary semantics

A precise implementation must eventually define whether bounds are inclusive or exclusive.

Examples:

```text
complete by 17:00
```

usually implies completion at exactly 17:00 is acceptable.

```text
not before 17:00
```

usually implies start at exactly 17:00 is acceptable.

A date range may use domain-specific inclusive/exclusive behavior.

Temporal Constraint v0 establishes that boundary inclusion is semantically relevant and must not be guessed implicitly by database operators.

The physical representation is deferred.

---

# Multi-placement and divisible execution

Constraints may apply to:

- every planned placement;
- the union of placements;
- first start;
- final completion;
- each Session;
- total duration;
- spacing between placements/Sessions.

Example:

```text
Activity
Study 3 hours

Constraint
complete by Friday
minimum individual Session duration 45 min
```

Possible Schedule:

```text
Wednesday 18:00 -> 19:30
Thursday 18:00 -> 19:30
```

The final completion deadline applies to the overall Activity while minimum duration applies to each execution slice.

Therefore future persistence/API design must preserve **constraint scope and constrained temporal feature**, not merely attach a generic start/end range to the Activity.

---

# Occurrence-specific constraints

A generated Occurrence may inherit source constraints and receive narrower exception rules.

Example:

```text
Routine
Workout weekdays

Occurrence #27
originally Wednesday

Exception
Saturday execution also permitted for this occurrence
```

This does not automatically modify future Routine Occurrences.

The Occurrence keeps stable identity; its effective constraint set changes for that instance.

This is consistent with Occurrence v0 and the rule that one-off changes do not silently mutate recurring policy.

---

# Event constraints

Events can also have constraints distinct from Schedule.

Example:

```text
Event
Medical appointment

Schedule
Tuesday 15:00 -> 15:30

Constraint
must occur before treatment begins
```

Or:

```text
Event
Flight

Constraint
check-in must complete no later than 40 min before departure
```

The second example may apply to a related Activity rather than Event itself depending on product modeling.

The point is that Event intrinsic time does not eliminate the need for external temporal relationships.

---

# Plan constraints

A Plan may define a temporal horizon without occupying the calendar itself.

Example:

```text
Plan
Exam preparation

Effective / valid horizon
1 September -> 30 November
```

Activities/Occurrences governed by the Plan may need to remain within that horizon.

This is distinct from:

```text
Schedule
1 Sep -> 30 Nov
```

because the Plan itself is not a 90-day calendar block.

Plan temporal horizons may therefore function as scoped Temporal Constraints or adjacent Plan temporal semantics depending on later persistence design.

The current rule is semantic:

> **Plan horizon != Schedule occupancy.**

---

# Routine constraints

Routine policy may include temporal constraints in addition to recurrence semantics.

Example:

```text
Routine
Workout 3x/week

Constraints
- minimum 24h spacing
- preferably after 17:00
- never after 22:00
```

The frequency/generation rule and the admissibility/preference rules are related but distinct.

This separation is one of the reasons Recurrence remains a separate concept review.

---

# Medication and safety-sensitive cases

Temporal Constraint must remain expressive enough for safety-sensitive workflows without pretending LifeOS is a medical authority.

Examples of representable semantics include:

```text
not before X hours after previous confirmed dose
```

```text
must occur within an authorized window
```

```text
minimum interval
```

```text
maximum interval
```

The source, authority, and confirmation of such constraints become especially important.

LifeOS must not silently relax externally/safety-authoritative hard constraints merely to optimize convenience.

The product may require additional specialist safety rules later; those do not invalidate the general Temporal Constraint abstraction.

---

# Maintenance and use-based cases

Example:

```text
Replace filter
30 days after actual previous replacement
```

The next temporal boundary depends on Actual history.

This illustrates the interaction among:

```text
Actual
→ relative temporal anchor
→ constraint / recurrence generation
→ Occurrence
→ Schedule
```

The exact classification between completion-relative Recurrence and relative Temporal Constraint will be tested in the upcoming Recurrence review.

Temporal Constraint v0 intentionally does not force the answer prematurely.

---

# Constraint composition and explanation

The scheduler/AI must eventually be able to explain why a Schedule is valid, invalid, or preferred.

Example:

```text
Chosen Schedule
Tuesday 18:00 -> 19:00

Reasons
- after earliest-start constraint
- before deadline
- satisfies minimum duration
- inside preferred evening window
- does not violate recovery spacing
```

Or:

```text
No valid Schedule exists

Conflict
- earliest start 20:00
- latest completion 20:30
- minimum duration 60 min
```

This explainability requirement is a strong reason to model constraints explicitly rather than hiding them inside arbitrary planner JSON.

---

# AI authority and proposals

AI may:

- infer possible constraints;
- detect conflicts;
- propose a constraint from natural language;
- propose relaxing a self-imposed rule;
- propose a Schedule satisfying current constraints;
- explain which constraints are driving a plan.

AI must not silently:

- convert a target into a hard deadline;
- weaken an external hard constraint;
- invent a constraint as confirmed user policy;
- overwrite historical rules;
- treat an inference as authoritative source data.

Proposed/inferred constraints require provenance and the appropriate confirmation/authority path.

---

# Constraint source and provenance

A Temporal Constraint may originate from:

- explicit user input;
- Plan/Routine policy;
- imported external data;
- an external authoritative system;
- a reviewed template;
- an approved automated rule;
- AI inference awaiting confirmation;
- a derived relation from another confirmed fact.

The source affects trust, edit authority, conflict handling, and synchronization.

The exact Provenance model remains deferred, but Temporal Constraint must be compatible with it.

---

# External identity

An imported deadline or temporal rule may have provider identifiers.

LifeOS identity must not be defined solely by provider IDs.

A provider record may be replaced, corrected, or resynchronized while LifeOS preserves the semantic rule/history.

Exact integration mapping belongs to the Integration model.

---

# Derived concepts and presentation labels

The UI may present convenient labels such as:

- due today;
- overdue;
- too early;
- inside preferred window;
- outside preferred window;
- deadline risk;
- impossible schedule;
- recovery requirement;
- available after 17:00.

These should normally be derived from current constraints, Schedule, Actual, and current time rather than stored as universal canonical flags.

This prevents stale derived state and keeps the model explainable.

---

# Representative model examples

## Work deadline

```text
Activity
Submit proposal

Constraint
hard latest completion: Friday 17:00
source: client

Schedule
Thursday 14:00 -> 16:00

Session
Thursday 14:12 -> 15:48

Actual
submitted Thursday 15:52
```

No ambiguity exists among deadline, plan, execution, and result.

---

## Preferred study window

```text
Activity
Study chapter 8

Constraint
soft preferred window: 18:00 -> 21:00

Schedule
12:30 -> 13:30
```

The Schedule is valid but violates a preference.

LifeOS may explain why the compromise was selected.

---

## Hard blood-test window

```text
Activity
Blood test

Constraint
hard full-execution window: 07:00 -> 09:00

Schedule proposal
09:30 -> 10:00
```

The proposal is inadmissible unless the constraint is changed/overridden with valid authority.

---

## Actual outside hard window

```text
Constraint
hard full-execution window: 07:00 -> 09:00

Accepted Schedule
08:15 -> 08:45

Actual Event/Session
09:10 -> 09:35
```

LifeOS records reality and derives the violation rather than rejecting history.

---

## Goal target versus external deadline

```text
Goal
Reach B2
Target date: 31 Dec
```

is a desired horizon.

```text
Exam registration Activity
Hard submission deadline: 1 Nov 23:59
```

is an admissibility constraint.

They are not automatically the same temporal rule.

---

## Recovery spacing

```text
Routine
Strength training

Constraint
hard minimum spacing: 48h after previous hard-training Session end
```

A Schedule proposal 24h later is invalid under the current rule.

---

## Medical follow-up

```text
Event
Medical visit
Actual end: 10 Aug 11:00

Activity
Book follow-up

Constraint
complete within 7 days after visit
```

The temporal rule is relative to another fact rather than a fixed datetime entered manually.

---

## Constraint revision causes replan

```text
External deadline v1
15 Sep 17:00

Schedule
14 Sep 14:00 -> 16:00
```

Provider changes deadline:

```text
External deadline v2
12 Sep 17:00
```

LifeOS now detects the current Schedule is invalid and proposes a replan.

The earlier deadline and Schedule remain historically reconstructible.

---

## Impossible combination

```text
hard earliest start: 20:00
hard latest completion: 20:30
hard minimum duration: 60m
```

Result:

```text
no admissible Schedule
```

LifeOS must surface the conflict instead of fabricating a solution.

---

# Adversarial boundary cases

## Same range, different semantics

```text
Tuesday 17:00 -> 21:00
```

could be:

- accepted Schedule;
- hard valid window;
- soft preferred window;
- user Availability;
- Calendar Block;
- Goal target window.

Therefore raw range shape cannot determine the domain concept.

---

## Deadline after execution but before confirmation

```text
Deadline
17:00

Actual submission
16:58

LifeOS confirmation received
17:20
```

The Activity was on time despite confirmation arriving after the deadline.

Deadline evaluation depends on the relevant Actual fact, not when LifeOS learned it.

This will be formalized further in Provenance/Confirmation review.

---

## User deliberately violates self-imposed rule

```text
Constraint
no work after 20:00
source: user
hard for scheduler

User manually starts Session
20:30
```

LifeOS records the Session.

It may ask whether:

- this was a one-off override;
- the constraint should change;
- no change is needed.

It must not silently rewrite the historical rule.

---

## External hard rule cannot be changed by convenience

```text
Application closes
Friday 23:59
```

No feasible Schedule exists.

LifeOS must not move the deadline to Monday.

It may propose reducing scope, prioritizing work, or abandoning/replacing the Activity according to user authority.

---

## Constraint inherited from Plan plus Occurrence exception

```text
Plan rule
work only Mon-Fri

Occurrence exception
Saturday permitted this time
```

The exception affects the specific instance without silently changing Plan-wide policy.

---

## Constraint uses Actual-relative anchor

```text
Next maintenance action
not before 30 days after actual previous replacement
```

If previous Actual date is corrected, future effective timing may need recomputation while preserving the earlier reasoning/history.

This will be stress-tested jointly with Recurrence and Actual later.

---

# Alternatives considered

## Alternative A — separate `Deadline`, `Window`, and `TemporalConstraint` primitives

Rejected for the current kernel.

Why:

- Deadline is naturally a latest-bound rule;
- Window is only a range shape whose semantics vary;
- duration, spacing, exclusion, and relative constraints would still require a fourth abstraction;
- parallel entities would duplicate authority, provenance, scoping, history, and hard/soft behavior;
- users can still see dedicated `Deadline` and `Preferred window` product concepts without separate kernel roots.

Preferred direction:

```text
TemporalConstraint
  ├─ deadline/latest-bound semantics
  ├─ earliest/latest boundary semantics
  ├─ window/range semantics
  ├─ duration semantics
  ├─ spacing semantics
  └─ relative temporal relation semantics
```

---

## Alternative B — put all temporal rules inside Schedule

Rejected.

Why:

- an unscheduled Activity can still have a deadline;
- allowed time and chosen time are different facts;
- constraint revision and Schedule revision have different histories;
- a hard rule can be violated by Actual without making Actual invalid;
- recurrence and availability would make Schedule a temporal mega-object.

---

## Alternative C — one `due_at` field on Activity/Goal/etc.

Rejected.

Why:

- latest start and latest completion differ;
- earliest boundaries exist;
- range and duration rules exist;
- relative rules exist;
- Goal target is not necessarily deadline;
- multiple simultaneous constraints are common;
- hard/soft/source/authority/history cannot be represented safely.

---

## Alternative D — generic arbitrary JSON constraint engine immediately

Rejected.

LifeOS requires extensibility, but core scheduling rules are highly queryable and behaviorally important.

An opaque JSON rule language would make:

- conflict detection harder;
- database queries weaker;
- planner invariants harder to enforce;
- migration and analytics less reliable;
- AI-generated rules harder to validate;
- external integrations harder to map safely.

The future persistence model may use controlled JSONB for extension metadata, but common temporal semantics should be formally modeled.

---

## Alternative E — treat every hard constraint violation as failure/missed outcome

Rejected.

Constraint violation and execution outcome are different dimensions.

A user may complete something late, start too early, execute outside a preferred window, or violate a self-imposed rule while still producing a valid Actual result.

The Outcome model will decide downstream semantics.

---

# Invariants

Temporal Constraint v0 establishes the following current invariants.

1. **Temporal Constraint is distinct from Schedule.**
2. **Temporal Constraint is distinct from Session and broader Actual.**
3. **Temporal Constraint is distinct from Recurrence.**
4. **Temporal Constraint is distinct from Availability / Capacity.**
5. **Temporal Constraint is distinct from Movement Policy and scheduling authority.**
6. `Deadline` is a latest-bound Temporal Constraint semantic specialization, not a separate kernel primitive at this stage.
7. `Window` is a range-shaped temporal expression whose domain meaning depends on context; it is not a standalone universal primitive.
8. Goal/Milestone target date or target window does not automatically become a hard Temporal Constraint.
9. Review date does not automatically constrain achievement/execution.
10. A temporal constraint must preserve what temporal feature/relation it constrains when that distinction matters: start, completion, containment, duration, spacing, or another explicit relation.
11. Hard constraints define admissibility for automatic planning under the current rules.
12. Soft constraints/preferences shape optimization/ranking and may be violated according to policy.
13. Constraint strength and authority/mutability are separate dimensions.
14. A hard constraint does not prevent LifeOS from recording Actual reality that violated it.
15. Passing a deadline does not automatically create a canonical `missed` or failure outcome.
16. Constraint revision and Schedule revision are distinct historical facts.
17. Material constraint changes require enough history/provenance to explain decisions when the earlier rule mattered.
18. Multiple hard constraints must be jointly satisfiable for an automatic Schedule to be admissible.
19. LifeOS must surface infeasibility rather than silently violate hard constraints to produce a complete-looking schedule.
20. Temporal constraints may be absolute, boundary-based, range-based, duration-based, spacing-based, exclusion-based, or relative to another temporal fact.
21. Constraint boundaries preserve date-only/floating/zoned/instant semantics without inventing temporal precision.
22. Boundary inclusion/exclusion semantics are relevant and must eventually be explicit rather than accidentally inherited from storage operators.
23. Constraints may be declared at broader scope and govern related subjects without requiring physical duplication onto every child.
24. A more-specific Occurrence constraint/exception may differ from source policy without silently rewriting the source or other Occurrences.
25. Recurring patterns of constraints must be supportable, but their representation is deferred to Recurrence review.
26. Deadline evaluation uses the relevant temporal fact, not necessarily the time when LifeOS learned/confirmed that fact.
27. Derived violation labels should normally come from Constraint-versus-Schedule/Actual evaluation rather than being foundational duplicated state.
28. AI-inferred constraints are proposals/inferences until accepted through appropriate authority or trusted source semantics.
29. External authoritative constraints must not be silently weakened because the scheduler cannot find a convenient solution.
30. Exact entity/value-object boundaries, SQL tables, inheritance/scoping persistence, optimizer representation, and rule encoding remain deliberately deferred.

---

# Open questions intentionally deferred

Temporal Constraint v0 deliberately does **not** finalize:

- the physical entity/value-object split for constraint declarations versus effective constraints;
- exact database schema for boundaries, windows, duration, spacing, relative references, and exclusions;
- the controlled type system/enums used in APIs;
- constraint inheritance/scoping resolution order;
- exact priority/weight model for soft constraints;
- exact authority/override model;
- exact effective-dating/version-event persistence;
- exact provenance structure;
- exact interaction between relative constraints and Relationship entities;
- exact distinction between completion-relative Recurrence and relative Temporal Constraint in borderline maintenance/medication cases;
- recurring-constraint expression syntax;
- timezone/DST/travel resolution rules for repeating windows;
- exact Outcome semantics for deadline misses, expiry, lateness, overrides, and exceptions;
- exact lifecycle meaning of `expired` from older product documentation;
- how Calendar Block / Availability / Capacity contributes additional effective scheduling restrictions;
- optimizer implementation and feasibility solver;
- SQL exclusion/range constraints that may eventually be appropriate in PostgreSQL.

These questions should be answered by the adjacent Recurrence, Availability/Capacity, Actual/Outcome, Relationship, Provenance, and persistence reviews rather than guessed here.

---

# Implications for future persistence

Without fixing tables yet, persistence must eventually support:

- multiple constraints per governed subject/scope;
- typed constrained temporal feature/relation;
- hard/soft semantics;
- source/authority/provenance;
- stable identity/history where a rule is independently revised or referenced;
- absolute/date-only/local/floating/instant boundary semantics;
- ranges with explicit relationship/inclusion semantics;
- duration and spacing rules;
- relative references to other temporal facts;
- scoped constraints and instance-specific exceptions;
- efficient active/effective-constraint queries;
- planner feasibility evaluation;
- audit of material revisions;
- external source mapping without using provider IDs as LifeOS identity.

This strongly suggests a formally typed relational core rather than arbitrary per-subject JSON fields, while still leaving room for controlled extensibility later.

---

# Implications for future APIs

Future APIs should be able to distinguish operations such as:

```text
create a hard completion deadline
```

```text
add a soft preferred window
```

```text
change the governing deadline
```

```text
apply a one-off Occurrence exception
```

```text
remove a preference without changing Schedule
```

```text
ask why a proposed Schedule is invalid
```

```text
ask which constraints caused a replan
```

```text
record Actual execution outside a hard window
```

without conflating these into generic calendar timestamp updates.

The exact REST/resource design is deferred.

---

# Relationship to accepted Time concepts

The Time-cluster direction after Temporal Constraint v0 is:

```text
Routine / recurring Event / generator
        ↓
Occurrence
which expected instance
        ↓
Temporal Constraint(s)
what is allowed / required / preferred
        ↓
Schedule
what time is currently accepted
        ↓
Session / Event Actual
what time actually happened
        ↓
Actual / Outcome / Evidence
what happened and what it means
```

Not every subject requires every layer:

- one-off Activity may have Constraint + Schedule + Session without Occurrence;
- Activity may have Deadline but no Schedule yet;
- spontaneous Session may exist without prior Schedule/Constraint;
- Event may use Schedule and Actual occurrence without Session;
- Goal may have a target date without Temporal Constraint;
- Plan may govern a horizon that constrains child scheduling without itself occupying the calendar.

This optional composition is intentional.

---

# Next review dependency

The next Time-cluster concept is `Recurrence`.

Recurrence review must stress-test Temporal Constraint v0 especially for:

- recurring hard/preferred windows;
- calendar-anchored versus elapsed-interval patterns;
- completion-relative generation;
- recurring Event series;
- Routine occurrence generation;
- effective future revisions;
- exceptions and `this occurrence` versus `this and future` semantics;
- timezone/DST/travel behavior;
- constraints that repeat versus recurrence rules that create expected instances;
- when a completion-relative rule is recurrence versus merely a relative constraint.

If Recurrence exposes a contradiction, Temporal Constraint v0 remains reopenable under the Domain Atlas decision rule.
