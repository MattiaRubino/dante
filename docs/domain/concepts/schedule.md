# Schedule v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-11  
**Meaning of accepted:** best current decision; reopenable with better evidence  
**Workstream:** Core Domain Model v0 — Time cluster

## Canonical definition

> **A Schedule is the current accepted temporal assignment of a schedulable subject, expressing when its execution or occurrence is intended or expected to take place at the precision currently committed. A Schedule may be revised without changing the identity of its subject, and remains distinct from temporal constraints, recurrence rules, capacity blocking, and what actually happened.**

A Schedule answers the operational question:

> **When is this currently intended or expected to happen?**

It does not answer:

- what the thing is;
- why it matters;
- whether it is recurring;
- whether a time is merely allowed/preferred rather than accepted;
- whether the user is busy during that time;
- whether execution actually happened at that time;
- whether a target or deadline was met.

The same scheduling capability may be used by different domain subjects without collapsing their semantics.

Examples:

```text
Activity
Study chapter 5

Schedule
Tuesday 18:00 -> 20:00
```

```text
Event
Client meeting

Schedule
Tuesday 15:00 -> 16:00
```

```text
Routine Occurrence
Workout — Wednesday instance

Schedule
Thursday 19:00 -> 20:30
```

The Activity remains an Activity, the Event remains an Event, and the Occurrence remains the same logical instance. Schedule supplies accepted temporal placement.

---

## Why this concept exists

The accepted Intention & Execution concepts already require a reusable temporal layer that can change independently of domain identity.

`Activity v0` requires:

- Activity identity to remain stable when work is rescheduled;
- estimated effort, scheduled duration, and actual effort to remain distinct;
- a single Activity to potentially be split across several planned execution periods;
- calendar placement not to transform Activity into Event.

`Event v0` requires:

- temporal placement to be intrinsic to Event meaning but still mutable;
- original expectation, current accepted schedule, and actual occurrence to remain distinguishable;
- official reschedule to differ from real-world early/late execution;
- Event identity to survive a temporal change.

`Routine v0` requires:

- recurring policy to remain separate from concrete scheduled instances;
- one-off occurrence changes not to mutate the whole Routine;
- flexible routines to be able to produce expected instances before exact placement.

`Occurrence v0` requires:

- stable identity for one generated instance independent from current start/end;
- an Occurrence to be able to exist before exact temporal placement;
- rescheduling not to create a new Occurrence automatically.

The previous LifeOS scheduling documents also distinguish:

- fixed placement;
- bounded windows;
- deadlines;
- preferred windows;
- open scheduling;
- movement policy;
- rescheduling history;
- planned versus actual execution.

Those requirements cannot be represented safely by putting `start_at` / `end_at` fields directly on every domain object and overwriting them whenever plans change.

Schedule therefore exists as the temporal-assignment capability between domain intention/occurrence identity and Actual execution.

---

## Validation basis

Schedule v0 was reviewed against:

### Existing LifeOS documentation

- `docs/product/v1-scheduling-flexibility.md`;
- `docs/product/v1-execution-status.md`;
- `docs/product/v1-core-domain-glossary.md`;
- `docs/product/feature-discovery-simulation-2026-08.md`;
- the accepted Domain Atlas concepts Goal, Plan, Activity, Event, Routine, Milestone, and Occurrence;
- the validated Intention & Execution cluster checkpoint.

### Representative LifeOS scenarios

The review included:

- study assigned to an exact block;
- study intentionally assigned only to an afternoon/day;
- work eligible inside a window but not yet assigned;
- tasks with deadlines but no accepted execution time;
- meetings moved earlier or later;
- meetings that start early/late without being rescheduled;
- meetings explicitly extended while already in progress;
- all-day/date-based events;
- activities split into several planned blocks;
- recurring Routine occurrences that exist before exact placement;
- recurring Event instances with one-off exceptions;
- schedules that should not consume availability/busy time;
- floating local time versus named-time-zone placement;
- AI-proposed schedules awaiting user authority.

### External benchmark patterns

Schedule v0 used external systems as evidence rather than authority.

Relevant benchmark patterns include:

- iCalendar/RFC 5545 distinguishes event/task temporal placement from due constraints and represents DATE separately from DATE-TIME;
- iCalendar distinguishes floating local time, UTC, and local time bound to a time zone;
- iCalendar `TRANSP` demonstrates that temporal placement and busy-time consumption are different semantics;
- Google Calendar represents all-day events as dates, timed events as date-time values, recurrence separately from individual instance placement, and transparency separately from timing;
- Google recurring instances preserve original instance identity even when one instance is moved;
- Apple EventKit exposes event dates separately from availability semantics.

LifeOS intentionally does not copy any one provider model physically.

---

## Core semantic position

The current temporal chain is:

```text
Domain intention / recurring source
        ↓
Occurrence identity where applicable
        ↓
Original temporal expectation
        ↓
Schedule revisions
        ↓
Current accepted Schedule
        ↓
Actual execution / attendance / occurrence
```

Schedule occupies one specific layer:

> **the currently accepted temporal assignment.**

It is neither the identity of the domain subject nor the historical/actual result.

---

## Accepted versus proposed schedule

A candidate placement proposed by LifeOS or AI is not automatically canonical Schedule truth.

Example:

```text
AI proposal
Study 18:00 -> 20:00
```

Before approval, this is a scheduling proposal.

After user acceptance, or after an explicitly authorized automation policy applies it, it becomes the current accepted Schedule.

Conceptually:

```text
Scheduling proposal
        ↓ user / approved policy authority
Accepted Schedule
```

This preserves the broader LifeOS rule that AI may propose canonical changes but must not silently establish user intent unless an explicit reusable authorization permits it.

Schedule history should eventually retain enough provenance to explain:

- who proposed a placement;
- who or what accepted/applied it;
- when it became effective;
- what previous accepted placement it replaced;
- why it changed when known.

The exact provenance persistence model is deferred.

---

## Schedule versus Activity

An Activity is an actionable intention.

A Schedule assigns temporal placement to that intention.

```text
Activity
Write report

Schedule
Tuesday 14:00 -> 16:00
```

Changing the Schedule does not change the Activity identity.

```text
Same Activity

Old accepted Schedule
Tuesday 14:00 -> 16:00

New accepted Schedule
Wednesday 09:00 -> 11:00
```

Therefore:

> **Schedule != Activity.**

An Activity may exist with no Schedule at all.

Example:

```text
Activity
Buy a new SSD

Schedule
none
```

It may still have a deadline, preferred window, priority, or other planning constraints.

---

## Schedule versus Event

An Event is occurrence-centred and temporal placement is intrinsic to its meaning.

Schedule supplies the Event's accepted temporal assignment without becoming the Event identity itself.

```text
Event
Flight AZ123

Schedule
10 September 14:20 -> 16:05
```

If the airline changes the flight:

```text
Same Event

Original accepted placement
14:20 -> 16:05

Current accepted Schedule
18:00 -> 19:45
```

The Event remains the same Event.

This means the physical model should avoid competing canonical truths such as independent `event.start_at` and `schedule.start_at` values representing the same semantic fact.

The exact persistence boundary remains deferred, but conceptually:

> **Event owns occurrence-centred meaning; Schedule represents its accepted temporal placement.**

Therefore:

> **Schedule != Event.**

---

## Schedule versus Occurrence

Occurrence answers:

> **Which generated/recurring instance is this?**

Schedule answers:

> **When is this instance currently expected to happen?**

Example:

```text
Routine
Workout Monday / Wednesday / Friday

Occurrence
Wednesday instance #27

Original expectation
Wednesday 18:00

Current Schedule
Thursday 19:00 -> 20:30
```

It remains occurrence #27 after rescheduling.

Therefore:

> **Occurrence identity must not be derived from current Schedule placement.**

An Occurrence may exist before exact Schedule assignment.

Example:

```text
Routine
Train 3 times this week

Occurrences
A
B
C

Exact Schedules
not assigned yet
```

Later:

```text
A -> Monday 18:00
B -> Thursday 19:00
C -> Saturday 10:00
```

Therefore:

> **Schedule != Occurrence.**

---

## Schedule versus Routine and Recurrence

A Routine represents a persistent recurring execution policy.

A recurrence capability determines how repeated instances are generated or anchored.

Schedule represents the accepted temporal placement of a particular schedulable subject or instance.

Conceptually:

```text
Routine / recurring Event
        ↓
Recurrence semantics
        ↓
Occurrences
        ↓
Schedules
```

A one-off Schedule change for an Occurrence does not automatically change recurrence policy.

Therefore:

> **Schedule != Routine.**

and:

> **Schedule != RecurrenceRule.**

Schedule must not become a mega-object containing recurrence syntax merely because recurring instances eventually receive schedules.

---

## Schedule versus Actual

Schedule represents accepted expectation.

Actual represents observed reality.

Example — no reschedule:

```text
Schedule
15:00 -> 16:00

Actual
15:18 -> 16:25
```

This is not a Schedule revision.

It is execution/occurrence that differed from the accepted Schedule.

Example — explicit reschedule:

```text
Original Schedule
15:00 -> 16:00

Current Schedule
15:30 -> 16:30

Actual
15:38 -> 16:24
```

All three temporal facts are meaningful.

The system must not automatically rewrite Schedule to match Actual simply because a timer starts early/late or an Event runs long.

Otherwise LifeOS would lose the ability to reason about:

- estimation quality;
- punctuality/deviation;
- realistic future planning;
- overrun/underrun patterns;
- missed versus proactively rescheduled execution;
- adherence and replanning.

Therefore:

> **Schedule != Actual.**

---

## Actual may begin earlier or later than Schedule

The model must make no assumption that deviation is only lateness.

All of these are valid:

```text
Schedule 15:00 -> 16:00
Actual   14:52 -> 15:55
```

```text
Schedule 15:00 -> 16:00
Actual   14:55 -> 16:20
```

```text
Schedule 15:00 -> 16:00
Actual   15:20 -> 15:50
```

```text
Schedule 15:00 -> 16:00
Actual   15:00 -> 16:00
```

Concepts such as:

- early start;
- late start;
- early finish;
- late finish;
- overrun;
- underrun;

are normally derived from accepted Schedule versus Actual comparison rather than stored as foundational Schedule state.

---

## Schedule revisions may move in either direction

A Schedule revision may move execution earlier, later, longer, shorter, or change only one boundary.

Examples:

```text
Original
18:00 -> 21:00

Revised
17:30 -> 20:30
```

```text
Original
18:00 -> 21:00

Revised
19:00 -> 22:00
```

```text
Original
15:00 -> 16:00

Revised
15:00 -> 16:30
```

The temporal geometry of the change can be derived from revisions.

LifeOS may additionally preserve semantic reasons such as:

- postponed after missing original placement;
- proactively rescheduled;
- external provider update;
- user preference change;
- conflict resolution;
- recovery/replanning.

Those reasons are not equivalent to the mathematical direction of the shift.

---

## A Schedule may be revised during execution

A Schedule revision is not restricted to changes made before Actual starts.

Example:

```text
Schedule
Meeting 15:00 -> 16:00

Actual start
15:02
```

At 15:50, participants explicitly decide:

```text
Expected end changed to 16:30
```

LifeOS can preserve:

```text
Schedule revision at 15:50
new expected end: 16:30

Actual end
16:24
```

This differs from a meeting that simply runs until 16:24 without any explicit change to the expected end.

In the latter case the accepted Schedule remains 15:00-16:00 and Actual records the overrun.

---

## Original expectation versus current accepted Schedule

LifeOS must preserve enough history to distinguish:

```text
Original accepted expectation
        ↓
Revision 1
        ↓
Revision 2
        ↓
Current accepted Schedule
```

The current Schedule is operationally authoritative for present planning.

Previous accepted placements remain historical facts.

They are not silently overwritten.

This history is required for:

- auditability;
- user explanation;
- provider reconciliation;
- AI reasoning;
- replanning analytics;
- planned-versus-actual comparison against the correct effective expectation.

The physical implementation may use revision records, effective-dated values, an audit stream, or another reviewed mechanism. Schedule v0 fixes the semantic requirement, not the final database representation.

---

## Schedule versus Deadline

A Deadline defines a latest permissible or meaningful boundary for another intention/requirement.

A Schedule assigns when execution is currently intended.

Example:

```text
Activity
Submit declaration

Deadline
30 April 23:59

Schedule
27 April 18:00 -> 19:00
```

The Deadline may exist without a Schedule.

A Schedule may exist without a Deadline.

Therefore:

> **Schedule != Deadline.**

A deadline displayed in a calendar does not become an Event or Schedule placement merely because it has a date/time.

Exact Deadline semantics are deferred to the dedicated temporal-constraint review.

---

## Schedule versus Target date/window

A target expresses when an outcome/checkpoint is desired.

Schedule expresses when execution/occurrence is currently assigned.

Example:

```text
Milestone
Master approved

Target date
15 September
```

That target does not mean:

```text
Schedule
15 September
```

Likewise:

```text
Goal
Reach B2 by December
```

uses Goal horizon/target semantics, not Schedule occupancy.

Therefore target semantics remain outside Schedule unless a concrete schedulable subject is explicitly assigned to that time.

---

## Schedule versus Temporal Constraint / Window

The same temporal shape can express different domain meaning.

Example phrase:

```text
Tuesday afternoon
```

Case A — accepted assignment:

> I decided to study Tuesday afternoon.

Then it is Schedule semantics.

Case B — valid/available window:

> I may study at any time Tuesday afternoon.

Then it is a Temporal Constraint / valid window and exact Schedule may still be absent.

Conceptually:

```text
Temporal Constraint
where/when scheduling is allowed or preferred

Schedule
where/when execution is currently assigned
```

Therefore:

> **Schedule != Temporal Constraint.**

Classification must depend on meaning, not only on a pair of timestamps.

The dedicated Deadline / Window / Temporal Constraint review will formalize hard versus soft bounds and preference semantics.

---

## Schedule versus movement policy

Schedule answers:

> **Where is this currently assigned?**

Movement policy answers:

> **How may LifeOS change that assignment?**

The same Schedule may be:

- locked;
- movable inside a valid window;
- movable only after user approval;
- freely replannable according to an authorized policy.

Therefore:

> **Schedule != movement policy.**

The accepted placement must not be overloaded with change-authority semantics.

---

## Schedule versus capacity / availability

Temporal placement does not automatically mean the user's capacity is consumed for the entire interval.

Examples:

```text
Event
Birthday — all day
```

may be visible all day without making the user unavailable for the day.

```text
Event
Optional webinar — 17:00 -> 18:00
```

may be scheduled but intentionally marked as non-blocking.

Conversely, a capacity block may reserve time even without a concrete Activity/Event outcome.

External systems also separate time from availability/busy semantics.

Therefore:

> **Having a Schedule does not imply busy/capacity reservation.**

and:

> **Schedule != Availability / Capacity.**

Calendar Block / Availability / Capacity will receive a dedicated review later in the Time cluster.

---

## Schedule versus Session

Schedule represents planned temporal assignment.

Session will represent an actual execution slice.

Example:

```text
Activity
Study chapter 5

Scheduled placement
18:00 -> 20:00

Actual Session
18:12 -> 19:47
```

Those are not the same object or lifecycle.

Actual execution may contain pauses, resumptions, multiple slices, or additional unplanned work.

Likewise one accepted Activity may have multiple planned placements before any Session occurs.

Therefore:

> **Schedule != Session.**

The exact boundary will be stress-tested in Session v0.

---

## Multiple planned placements

A schedulable subject may require more than one planned temporal placement.

Example:

```text
Activity
Study chapter 5

Estimated effort
3 hours
```

Accepted planning:

```text
Tuesday
18:00 -> 20:00

Wednesday
18:00 -> 19:00
```

This cannot be represented safely by one universal `start_at/end_at` pair on Activity.

Schedule semantics must therefore support, directly or through a related structure, more than one accepted placement for one execution intention when the subject is divisible.

The physical model is intentionally not fixed yet.

Possible future implementations include:

- one Schedule owning multiple planned placements;
- multiple schedule-assignment records linked to one subject;
- planned execution slices as a dedicated temporal structure.

Session review must determine how planned slices map to Actual execution slices without duplicating identity.

---

## Estimated effort versus scheduled duration versus actual duration

These values are distinct.

Example:

```text
Estimated effort
3h

Scheduled placements
2h + 1h

Actual Sessions
1h20 + 40m + 35m
```

LifeOS must not silently treat any one of these as the other.

This distinction enables future reasoning such as:

- systematic underestimation;
- realistic schedule generation;
- partial completion;
- overrun/underrun analysis;
- adaptation of future effort estimates.

---

## Schedule precision must not be invented

LifeOS should represent temporal commitment at the precision actually known/accepted.

Valid scheduling intentions may include:

```text
Tuesday
```

```text
Tuesday afternoon
```

```text
Tuesday at 18:00
```

```text
Tuesday 18:00 -> 20:00
```

```text
Start Tuesday 18:00
End not yet specified
```

These are not semantically identical.

The system must not convert a coarse commitment into false precision merely because the database or UI prefers exact timestamps.

The physical temporal-value model remains deferred, but Schedule v0 requires explicit support for meaningful precision distinctions.

---

## Date-based / all-day placement

A date-based Schedule is not semantically equivalent to a normal 24-hour instant interval.

Example:

```text
Event
Birthday

Schedule
11 August — date-based / all-day
```

LifeOS should not interpret this as inherently meaning:

```text
00:00 -> 24:00 capacity consumption
```

Date-based placement has calendar-date semantics.

This matters for:

- all-day events;
- birthdays/anniversaries;
- travel across time zones;
- daylight-saving transitions;
- calendar interoperability;
- availability.

Exact date-range representation, including inclusive/exclusive boundaries, will be resolved in temporal persistence/API design.

---

## Floating time, zoned local time, and absolute instant

Schedule must preserve different time interpretations when they matter.

### Floating local time

```text
09:00 local wherever I am
```

The local clock meaning is primary.

### Zoned local time

```text
09:00 Europe/Rome
```

The named time zone is part of the accepted temporal meaning.

### Absolute instant

```text
One globally fixed instant
```

The instant is primary and local display changes according to zone.

These semantics must not be collapsed prematurely into one UTC timestamp if doing so loses the user's temporal intention.

The detailed timezone/DST/travel policy belongs to Recurrence and temporal-value design, but Schedule v0 requires preserving enough semantics to distinguish them.

---

## Travel and time-zone changes

A Schedule should not silently reinterpret user intent merely because device or current location time zone changes.

Example questions that later policies must answer explicitly:

- Is a doctor's appointment fixed to Europe/Rome even while traveling?
- Is a morning routine intended at 08:00 local wherever the user currently is?
- Is a remote webinar fixed to one absolute instant?
- Does an imported flight carry origin/destination zone semantics?

Schedule v0 does not solve all travel behavior, but requires that the temporal representation retain enough information for those policies to be applied correctly.

---

## Unscheduled means absence of Schedule

LifeOS should not require a fake schedule record/state merely to say something has not been assigned to time.

Example:

```text
Activity
Buy SSD

Schedule
none

Deadline
31 August

Preferred window
weekend
```

The Activity exists and remains actionable.

Therefore:

> **No Schedule is a valid condition.**

A future planning-state model may still expose user-facing states such as available or unscheduled, but those should not require a synthetic temporal assignment.

---

## Flexible assignment versus unscheduled eligibility

LifeOS must distinguish:

```text
Accepted Schedule
Tuesday afternoon
```

from:

```text
Temporal eligibility
any time Tuesday afternoon

Schedule
none
```

The first means the user has committed the item to that coarse period.

The second means the period is merely an allowed/available scheduling space.

This distinction is important for AI replanning because changing an accepted commitment carries different authority and user expectation than selecting a time from an unscheduled valid window.

---

## Reschedule versus postponement

Schedule v0 separates temporal revision history from semantic reasons for revision.

A proactive move:

```text
Monday 18:00
→
Tuesday 18:00
```

may be a reschedule.

A missed placement followed by a deliberate later carry-forward may be called postponement.

Both involve a changed accepted Schedule, but the second additionally describes execution/history context.

Therefore `rescheduled` or `postponed` should not be treated as the only current Schedule state.

The revision history and eventual execution outcome contain richer information.

Exact planning-state terminology will be revisited with Actual/Outcome and temporal constraints.

---

## Cancellation and Schedule

Cancelling an Event or Occurrence is not equivalent to merely deleting its Schedule.

Example:

```text
Recurring meeting occurrence
Monday 10:00

Disposition
cancelled
```

The historical occurrence may need to remain identifiable together with its previous accepted placement.

Therefore cancellation/disposition belongs to the subject/Occurrence lifecycle rather than being represented solely through Schedule absence.

Similarly, unscheduling an Activity does not necessarily cancel the Activity.

```text
Activity remains actionable
Schedule removed
```

is different from:

```text
Activity cancelled / no longer intended
```

---

## Schedule removal / unscheduling

A subject may transition from scheduled back to unscheduled while retaining identity.

Example:

```text
Activity
Write report

Previous Schedule
Tuesday 18:00 -> 20:00

Current Schedule
none
```

The history should preserve that the Activity had previously been scheduled.

Whether unscheduling itself is stored as a revision event or derived from active assignment history is a physical-design decision.

---

## Replanning scope

Schedule revision may occur at several scopes:

- one planned placement;
- one Occurrence;
- all remaining placements of one Activity;
- surrounding dependent items;
- current day/week;
- future occurrences governed by a Routine/recurring Event revision.

Schedule itself represents the resulting accepted temporal assignment.

Replanning policy decides the scope and authority of changes.

The two must remain separate.

---

## Relationship with external providers

LifeOS Schedule identity/semantics must remain canonical independently of Google Calendar, Apple EventKit, Microsoft Graph, or another provider.

Imported external timing may become accepted Schedule through integration policy and provenance.

Provider synchronization must preserve distinctions such as:

- external event/instance identifier;
- LifeOS Event/Occurrence identity;
- provider current start/end;
- original recurring-instance anchor where applicable;
- LifeOS accepted Schedule;
- conflict/reconciliation state.

LifeOS must not use a provider event identifier as the universal Schedule identity.

Exact Integration Hub mappings are deferred.

---

## Relationship with AI scheduling

AI may:

- propose a first Schedule;
- propose moving a Schedule;
- propose splitting planned work;
- detect conflicts;
- compare capacity/constraints;
- propose broader replanning.

AI must not silently convert a proposal into the accepted Schedule unless the user has enabled a relevant low-risk automatic policy.

Material changes should remain explainable:

```text
What moved?
Why?
Which constraints were protected?
Which other items are affected?
Does this change one occurrence or future policy?
```

This preserves user authority while still allowing automation where explicitly desired.

---

## Derived schedule analytics

The following can normally be derived rather than stored as canonical Schedule truth:

- moved earlier/later;
- start delta;
- end delta;
- scheduled duration;
- total scheduled duration across placements;
- number of revisions;
- time since last revision;
- schedule-to-actual start deviation;
- schedule-to-actual end deviation;
- schedule-to-actual duration delta;
- adherence to preferred windows;
- conflict count.

Derived values may be cached for performance later, but they do not define Schedule identity.

---

## Representative scenario matrix

| Scenario | Schedule interpretation |
|---|---|
| Study 18:00-21:00 | exact accepted block |
| Study assigned to Tuesday afternoon | coarse accepted placement |
| Study allowed anywhere 17:00-21:00 | Temporal Constraint/window; Schedule may be absent |
| Task due Friday | Deadline; Schedule optional |
| Meeting 15:00-16:00 | Event + accepted Schedule |
| Meeting officially moved to 14:30 | Schedule revision, same Event |
| Meeting begins 14:52 without official change | Actual deviation, Schedule unchanged |
| Activity starts 20 minutes early | Actual deviation unless Schedule was explicitly revised |
| Meeting explicitly extended while in progress | Schedule revision of expected end + separate Actual |
| Meeting simply runs late | Actual overrun, Schedule unchanged |
| Birthday all day | date-based Schedule, capacity separate |
| Optional webinar visible but non-blocking | Schedule + separate availability/capacity semantics |
| 3h Activity planned as 2h + 1h | multiple planned placements |
| Routine 3x/week before placement | Occurrences may exist without exact Schedule |
| Goal B2 by December | Goal target/horizon, not Schedule |
| Milestone target 15 Sep | target/deadline semantics, not Schedule |
| Plan 1 Sep-30 Nov | Plan horizon, not Schedule occupancy |
| Routine Mon/Wed/Fri | recurring policy, not one Schedule |
| Event start known/end unknown | partial-precision Schedule semantics required |
| 09:00 floating | floating local Schedule semantics |
| 09:00 Europe/Rome | zoned local Schedule semantics |
| Fixed webinar global instant | absolute-instant semantics |
| Activity schedule removed but Activity kept | unscheduled Activity, historical Schedule retained |
| Recurring occurrence cancelled | occurrence disposition/history, not merely deleted Schedule |

---

## Adversarial cases

### Case 1 — same interval, different semantics

```text
Tuesday 17:00 -> 21:00
```

May mean:

- accepted Schedule;
- allowed window;
- preferred window;
- capacity block;
- Event occurrence time.

The timestamp shape alone is insufficient. Domain meaning must determine classification.

### Case 2 — actual starts early

```text
Schedule
18:00 -> 21:00

Actual
17:40 -> 20:15
```

No automatic Schedule rewrite.

### Case 3 — explicit mid-session extension

```text
Original Schedule
15:00 -> 16:00

At 15:50 explicit new expectation
end 16:30

Actual
15:02 -> 16:24
```

The Schedule history contains the explicit revision.

### Case 4 — long Activity split across planned blocks

```text
Activity
Prepare presentation

Estimated effort
4h

Schedule placements
Mon 18:00-20:00
Tue 18:00-20:00
```

The Activity remains one Activity; the planned temporal slices do not become semantic sub-Activities automatically.

### Case 5 — coarse commitment

```text
Activity
Call accountant

Accepted Schedule
Friday morning
```

LifeOS must not fabricate 09:00-09:30 until an exact placement is actually chosen.

### Case 6 — all-day does not mean unavailable

```text
Event
Anniversary

Schedule
11 August, all day

Capacity
not blocked by default merely because Schedule is all-day
```

### Case 7 — provider update versus Actual

External calendar changes meeting from 15:00 to 15:30 before it starts.

With accepted sync policy this may become a Schedule revision.

If the provider still says 15:00 but participants begin 15:18, that is Actual deviation instead.

### Case 8 — unschedule without cancellation

```text
Activity
Study chapter 5

Old Schedule
Tuesday 18:00-20:00

Current Schedule
none
```

The Activity remains intended; only temporal assignment was withdrawn.

---

## Core invariants

1. **Schedule is not the schedulable subject.** Activity, Event, Occurrence, or another reviewed subject retains its own identity.
2. **Schedule != Actual.** Accepted temporal expectation and observed reality remain separate.
3. **Schedule != Deadline.** A latest boundary does not equal accepted execution placement.
4. **Schedule != Goal/Milestone target.** Desired achievement timing does not equal operational placement.
5. **Schedule != Temporal Constraint / preferred window.** Allowed/preferred space is distinct from accepted assignment.
6. **Schedule != RecurrenceRule.** Recurrence generation is separate from instance placement.
7. **Schedule != Routine.** Routine governs recurring behavior; Schedule places concrete execution/occurrence.
8. **Schedule != Movement Policy.** Placement and authority to move placement are distinct.
9. **Schedule != Availability/Capacity.** Being scheduled does not automatically mean busy/blocking.
10. **Schedule != Session.** Planned placement and actual execution slice are distinct.
11. A Schedule represents **accepted** temporal assignment, not merely an AI/system proposal.
12. User approval or an explicitly authorized automation policy is required to establish material accepted Schedule changes.
13. Activity may exist with no Schedule.
14. Occurrence may exist before exact Schedule placement.
15. Event temporal meaning may use Schedule without duplicating Event identity.
16. Schedule revision does not automatically change the subject identity.
17. Original accepted placement and current accepted Schedule must remain historically reconstructible.
18. Actual deviation must not silently rewrite Schedule.
19. Schedule revisions may move start/end earlier or later and may change duration independently.
20. Explicit expectation may be revised even during execution; this remains distinct from unplanned overrun.
21. Temporal precision must not be fabricated.
22. Date-based/all-day placement must remain semantically distinct from an ordinary 24-hour instant interval.
23. Floating local, named-zone local, and absolute-instant semantics must remain distinguishable where relevant.
24. One schedulable subject may require multiple accepted planned placements when its execution is divisible.
25. Estimated effort, scheduled duration, and actual duration remain distinct quantities.
26. A temporal range is not classified as Schedule solely by shape; semantic intent decides whether it is assignment, constraint, availability, or another concept.
27. Having a Schedule does not imply that the same interval reserves user capacity.
28. Recurrence generates/organizes instances; one-off Schedule exceptions do not automatically mutate recurrence policy.
29. Lack of Schedule is valid and does not require a synthetic `UNSCHEDULED` temporal object.
30. Unscheduling does not automatically cancel the Activity/Event/Occurrence subject.
31. Cancelling an Occurrence/Event is not represented merely by deleting its Schedule history.
32. Schedule revision history must preserve enough provenance/authority for later explanation and reconciliation.
33. Provider identities remain external mappings rather than LifeOS Schedule identity.
34. Derived timing deltas are not foundational Schedule state.
35. Exact SQL/API representation of Schedule, placements, revisions, and temporal value types remains deferred.
36. Session review must verify the planned-placement versus actual-execution-slice boundary before physical persistence is fixed.

---

## Alternatives considered and rejected

### Alternative A — put `start_at` / `end_at` directly on every planning object

Rejected as the domain model.

Why:

- overwriting destroys Schedule revision history;
- different concepts need different temporal precision;
- multi-placement Activities do not fit one pair;
- date-only/all-day semantics become awkward;
- constraints/deadlines are easily conflated with Schedule;
- Occurrence identity risks becoming tied to current time;
- provider and Actual differences become difficult to reconcile.

Physical tables may still denormalize current placement for query performance later, but that must not become the semantic model.

### Alternative B — Schedule contains every temporal concern

Example mega-object:

```text
start
end
due
window
rrule
busy
movable
actual_start
actual_end
```

Rejected.

This would collapse:

- accepted placement;
- deadline;
- temporal constraints;
- recurrence;
- capacity;
- movement policy;
- Actual.

The result would be difficult to reason about, version, integrate, and query safely.

### Alternative C — every temporal item becomes Event

Rejected.

A scheduled Activity remains action-centred. A deadline remains a constraint. A capacity block may not represent occurrence. Schedule is a reusable temporal capability rather than a new domain type conversion.

### Alternative D — every schedulable object receives one exact UTC interval

Rejected.

It invents precision and loses:

- date-only semantics;
- coarse commitments;
- floating local time;
- named-zone local meaning;
- incomplete/unknown end;
- flexible placement.

### Alternative E — Schedule is only a transient UI calculation

Rejected.

Accepted Schedule changes are meaningful historical facts needed for:

- planned-versus-actual analysis;
- explanation;
- audit;
- external sync;
- AI reasoning;
- replanning.

The exact persistence technique is open, but Schedule semantics cannot be purely ephemeral.

---

## Questions intentionally deferred

Schedule v0 does **not** yet fix:

- whether Schedule itself is an entity, aggregate-owned value object, current-state projection, revision stream, or combination;
- the exact shape/name of planned placement records;
- whether multiple planned placements are child values of one Schedule or independent assignment rows;
- exact Session model and planned-placement-to-Actual mapping;
- exact Deadline / Window / Temporal Constraint entities/value objects;
- hard versus soft constraint persistence;
- exact movement-policy persistence;
- exact Recurrence rule/pattern model;
- recurrence materialization horizon;
- DST/travel policy for recurring/floating schedules;
- exact Calendar Block / Availability / Capacity model;
- full Schedule lifecycle/state vocabulary;
- exact cancellation/postponement/replacement state ownership;
- provenance/audit physical schema;
- external provider conflict-resolution rules;
- current-value denormalization/caching strategy;
- SQL range/timestamptz/date/time-zone representation;
- API serialization of coarse/floating/date-only temporal values;
- offline/sync conflict semantics.

These remain deliberately open because adjacent Time-cluster concepts must be reviewed first.

---

## Implications for future persistence

The eventual persistence model must be able to answer at least:

```text
What is currently scheduled?
What was scheduled at a past point in time?
When did the accepted Schedule change?
Who/what changed it?
What was the original accepted expectation?
Which Schedule was effective when Actual execution occurred?
Was the item scheduled exactly or only at coarse precision?
Was the temporal meaning floating, zoned, date-based, or instant-based?
Did the subject have multiple planned placements?
Was it later unscheduled without being cancelled?
```

The model should support these queries without forcing arbitrary JSON as the primary representation.

A likely future design may contain typed temporal value structures plus explicit current/revision semantics, but Schedule v0 intentionally stops before choosing tables.

---

## Implications for APIs

Future APIs should avoid ambiguous payloads such as:

```json
{
  "date": "2026-08-11",
  "due": "2026-08-11",
  "time": "18:00"
}
```

without semantic roles.

The API should eventually make clear whether a value is:

- accepted Schedule placement;
- constraint/window;
- deadline;
- target;
- capacity block;
- Actual time.

Material Schedule mutations should eventually support optimistic concurrency/versioning or another mechanism that prevents silent lost updates during sync/AI/user edits.

Exact API design is deferred.

---

## Current conclusion

Schedule v0 establishes one strong rule for the Time cluster:

> **Schedule is accepted temporal assignment, not everything temporal about an object.**

The resulting current temporal model is:

```text
Domain subject / recurring source
        ↓
Occurrence identity where applicable
        ↓
Accepted Schedule placement(s)
        ↓
Actual execution/attendance later
```

with adjacent but distinct concepts:

```text
Temporal Constraints / Deadline / Target
Recurrence
Movement Policy
Availability / Capacity
Provenance / Authority
```

This separation preserves history, user authority, realistic flexible planning, recurring-instance identity, and planned-versus-actual analysis without prematurely committing LifeOS to one physical calendar schema.

The next Time-cluster concept is **Session**, specifically to test whether one Activity/Occurrence can have multiple planned placements and multiple actual execution slices while preserving the distinction between Schedule and Actual execution.
