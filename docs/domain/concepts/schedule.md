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
        ↓ applicable acceptance / Authority / approved policy
Accepted Schedule
```

Authority v0 now makes the governance boundary explicit: acting/proposing does not create Authority, and Authority to make one bounded scheduling effect effective does not imply broader Authority or Visibility.

Schedule history should eventually retain enough provenance to explain:

- who proposed a placement;
- who or what accepted/applied it;
- what Authority/policy basis made the change effective where material;
- when it became effective;
- what previous accepted placement it replaced;
- why it changed when known.

The exact Provenance/Decision persistence model is deferred.

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

### Event postponed without a replacement Schedule

An Event can retain identity and historical temporal meaning even when its previously accepted placement is withdrawn and no replacement time is known yet.

Example:

```text
Event
Concert

Historical accepted Schedule
20 September 21:00

Provider update
POSTPONED — new date TBD

Current accepted Schedule
none
```

This does not make the Event timeless in meaning and does not require a fake placeholder Schedule.

It means the current temporal assignment is unresolved.

Canonical hardening:

> **An Event whose previous placement is withdrawn/postponed may temporarily have no current accepted Schedule while preserving Event identity and reconstructible historical expectation. Schedule absence must not be used to erase the Event or invent replacement precision.**

Event lifecycle/disposition semantics such as postponed/cancelled remain separate from Schedule.

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

Concepts such as early start, late start, early finish, late finish, overrun, and underrun are normally derived from accepted Schedule versus Actual comparison rather than stored as foundational Schedule state.

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

LifeOS may additionally preserve semantic reasons such as postponed after missing original placement, proactively rescheduled, external provider update, user preference change, conflict resolution, or recovery/replanning.

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

The current Schedule is operationally authoritative for present planning when one exists.

Previous accepted placements remain historical facts.

They are not silently overwritten.

For a postponed/unresolved Event, the current accepted Schedule may be absent while historical placements remain reconstructible.

This history is required for auditability, user explanation, provider reconciliation, AI reasoning, replanning analytics, and planned-versus-actual comparison against the correct effective expectation.

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

---

## Schedule versus movement policy

Schedule answers:

> **Where is this currently assigned?**

Movement policy answers:

> **How may LifeOS change that assignment?**

The same Schedule may be locked, movable inside a valid window, movable only after user approval, or freely replannable according to an authorized policy.

Therefore:

> **Schedule != movement policy.**

The accepted placement must not be overloaded with change-Authority semantics.

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

Therefore:

> **Having a Schedule does not imply busy/capacity reservation.**

and:

> **Schedule != Availability / Capacity.**

---

## Schedule versus Session

Schedule represents planned temporal assignment.

Session represents an actual execution slice.

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

---

## Schedule precision must not be invented

LifeOS should represent temporal commitment at the precision actually known/accepted.

Valid scheduling intentions may include:

```text
Tuesday
Tuesday afternoon
Tuesday at 18:00
Tuesday 18:00 -> 20:00
Start Tuesday 18:00 / End not yet specified
```

These are not semantically identical.

The system must not convert a coarse commitment into false precision merely because the database or UI prefers exact timestamps.

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

LifeOS should not interpret this as inherently meaning `00:00 -> 24:00 capacity consumption`.

Date-based placement has calendar-date semantics.

---

## Floating time, zoned local time, and absolute instant

Schedule must preserve different time interpretations when they matter.

### Floating local time

```text
09:00 local wherever I am
```

### Zoned local time

```text
09:00 Europe/Rome
```

### Absolute instant

```text
One globally fixed instant
```

These semantics must not be collapsed prematurely into one UTC timestamp if doing so loses the user's temporal intention.

---

## Travel and time-zone changes

A Schedule should not silently reinterpret user intent merely because device or current location time zone changes.

The detailed timezone/DST/travel policy belongs to Recurrence and temporal-value design, but Schedule v0 requires preserving enough semantics for those policies to be applied correctly.

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

For Event, Schedule absence may also be valid temporarily when a prior accepted placement is withdrawn/postponed and the new Event time is unresolved, provided the Event still retains its occurrence-centred temporal history/meaning.

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

This distinction is important for AI replanning because changing an accepted commitment carries different Authority and user expectation than selecting a time from an unscheduled valid window.

---

## Reschedule versus postponement

Schedule v0 separates temporal revision history from semantic reasons for revision.

A proactive move may be a reschedule. A missed placement followed by deliberate later carry-forward may be called postponement. An Event may also be externally postponed with no replacement time yet.

Both scheduled moves and schedule withdrawal may be historically meaningful, but lifecycle reason is not equivalent to the geometry of the Schedule change.

---

## Cancellation and Schedule

Cancelling an Event or Occurrence is not equivalent to merely deleting its Schedule.

The historical occurrence may need to remain identifiable together with its previous accepted placement.

Similarly, unscheduling an Activity does not necessarily cancel the Activity.

---

## Schedule removal / unscheduling

A subject may transition from scheduled back to unscheduled while retaining identity.

```text
Activity
Write report

Previous Schedule
Tuesday 18:00 -> 20:00

Current Schedule
none
```

The history should preserve that the Activity had previously been scheduled.

---

## Replanning scope

Schedule revision may occur at several scopes, including one placement, one Occurrence, all remaining placements, dependent items, a day/week, or future recurring occurrences.

Schedule itself represents the resulting accepted temporal assignment.

Replanning policy/Authority decides the scope and effectiveness of changes.

---

## Relationship with external providers

LifeOS Schedule identity/semantics must remain canonical independently of Google Calendar, Apple EventKit, Microsoft Graph, or another provider.

Imported external timing may become accepted Schedule through integration policy and Provenance.

Provider synchronization must preserve distinctions such as external event/instance identifier, LifeOS Event/Occurrence identity, provider current start/end, original recurring-instance anchor, LifeOS accepted Schedule, and conflict/reconciliation state.

---

## Relationship with AI scheduling

AI may propose a first Schedule, move, split, conflict resolution, or broader replanning.

AI must not silently convert a proposal into accepted Schedule unless the applicable bounded automation policy grants effective Authority.

Material changes should remain explainable.

Visibility v0 additionally requires that AI scheduling can use authorized private Availability/Schedule sources without disclosing private reasons or source objects to recipients who only receive a safe projection.

---

## Derived schedule analytics

Moved earlier/later, deltas, durations, revision counts, Schedule-to-Actual deviations, preferred-window adherence and conflict counts can normally be derived rather than stored as canonical Schedule truth.

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
| Event postponed, new date TBD | Event retains identity/history; current Schedule may be absent |
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

Validated adversarial cases include same interval/different semantics, actual early/late deviation, explicit mid-session extension, multi-block Activity scheduling, coarse commitment, all-day non-blocking placement, provider update versus Actual, unscheduling without cancellation, and Event postponement without a replacement date.

---

## Core invariants

1. **Schedule is not the schedulable subject.**
2. **Schedule != Actual.**
3. **Schedule != Deadline.**
4. **Schedule != Goal/Milestone target.**
5. **Schedule != Temporal Constraint / preferred window.**
6. **Schedule != RecurrenceRule.**
7. **Schedule != Routine.**
8. **Schedule != Movement Policy.**
9. **Schedule != Availability/Capacity.**
10. **Schedule != Session.**
11. A Schedule represents **accepted** temporal assignment, not merely an AI/system proposal.
12. Applicable Acceptance/Authority/policy is required to make a material proposal effective; proposing/acting alone is insufficient.
13. Activity may exist with no Schedule.
14. Occurrence may exist before exact Schedule placement.
15. Event temporal meaning may use Schedule without duplicating Event identity.
16. Schedule revision does not automatically change subject identity.
17. Original accepted placement and current accepted Schedule must remain historically reconstructible.
18. Actual deviation must not silently rewrite Schedule.
19. Schedule revisions may move start/end earlier/later and change duration independently.
20. Explicit expectation may be revised during execution; this remains distinct from unplanned overrun.
21. Temporal precision must not be fabricated.
22. Date-based/all-day placement remains distinct from ordinary 24-hour instant interval.
23. Floating local, named-zone local and absolute-instant semantics remain distinguishable where relevant.
24. One schedulable subject may require multiple accepted planned placements when execution is divisible.
25. Estimated effort, scheduled duration and actual duration remain distinct.
26. Temporal range shape alone does not classify Schedule.
27. Having a Schedule does not imply the same interval reserves capacity.
28. Recurrence generates/organizes instances; one-off Schedule exceptions do not automatically mutate recurrence policy.
29. Lack of Schedule is valid and does not require synthetic `UNSCHEDULED` temporal object.
30. Unscheduling does not automatically cancel the subject.
31. Cancelling an Occurrence/Event is not represented merely by deleting Schedule history.
32. Schedule revision history must preserve enough Provenance/Authority for later explanation/reconciliation.
33. Provider identities remain external mappings, not LifeOS Schedule identity.
34. Derived timing deltas are not foundational Schedule state.
35. Exact SQL/API representation remains deferred.
36. Session remains planned-placement versus actual-execution-slice boundary.
37. Event may temporarily have no current accepted Schedule after postponement while identity/history remain reconstructible.
38. Authority to change Schedule != Visibility of all related private source/context.
39. Visibility of a free/busy or coarse Schedule projection != Visibility of the underlying private Schedule subject/reason/participants.

---

## Alternatives considered and rejected

Rejected as domain models:

- direct overwritable `start_at/end_at` on every planning object;
- Schedule mega-object containing start/end/due/window/rrule/busy/movable/Actual;
- every temporal item becoming Event;
- every schedulable object receiving one exact UTC interval;
- Schedule as purely transient UI calculation.

Physical denormalization/caching may still exist later without changing semantic truth.

---

## Questions intentionally deferred

Schedule v0 does **not** yet fix:

- exact entity/value/revision persistence shape;
- planned placement child structure;
- exact Deadline/Window/Temporal Constraint persistence;
- hard/soft constraint persistence;
- exact movement-policy/policy persistence;
- Recurrence materialization/DST/travel policy;
- full lifecycle/disposition vocabulary;
- exact cancellation/postponement ownership;
- Provenance/audit physical schema;
- external-provider conflict-resolution rules;
- SQL range/time-zone representation;
- API serialization/coarse/floating/date values;
- offline/sync conflict semantics;
- Decision/reconciliation representation.

Authority and Visibility semantic boundaries are now resolved. Acceptance/Acknowledgement, detailed Decision/effective-change and technical Principal/enforcement remain separate future reviews.

---

## Implications for future persistence

The eventual persistence model must answer current/past Schedule, effective history, who/what changed it, original accepted expectation, Authority/policy basis where material, which Schedule was effective at Actual execution, temporal precision/meaning, multiple placements, unscheduling, and Event postponement without fabrication.

The model should support these queries without arbitrary JSON as the primary representation.

---

## Implications for APIs

Future APIs should make semantic roles explicit rather than expose ambiguous `date/due/time` fields.

Material Schedule mutations should support concurrency/versioning or equivalent protection from silent lost updates during sync/AI/user edits.

---

## Current conclusion

Schedule v0 establishes:

> **Schedule is accepted temporal assignment, not everything temporal about an object.**

Current model:

```text
Domain subject / recurring source
        ↓
Occurrence identity where applicable
        ↓
Accepted Schedule placement(s), when one is currently known/accepted
        ↓
Actual execution/attendance later
```

with adjacent but distinct concepts:

```text
Temporal Constraints / Deadline / Target
Recurrence
Movement Policy
Availability / Capacity
Provenance
Authority
Visibility
```

A current Schedule may legitimately be absent even when the subject has meaningful temporal history.

---

# 2026-08-12 — Authority + Visibility closure amendment

Authority v0 and Visibility v0 close the previously deferred governance/exposure boundaries around accepted temporal assignment.

```text
Scheduling proposal
!= accepted Schedule

Authority
= who/what may legitimately make a bounded Schedule change effective

Visibility
= what Schedule/availability projection or source detail may be exposed
```

Therefore Authority to reschedule does not imply Visibility into every private Event/Activity/reason, and a recipient may see a free/busy or coarse temporal projection without seeing the private Schedule source. Current accepted Schedule retains its own temporal semantics; Authority/Visibility remain orthogonal capabilities rather than fields that redefine Schedule identity.

AI scheduling preserves the same boundary: optimization/proposal capability does not create Authority, and authorized source processing does not create disclosure permission.

---

# 2026-08-12 — Acknowledgement / generic Acceptance closure amendment

Acknowledgement v0 closes the previously deferred common-ground boundary without changing Schedule identity or temporal semantics.

The word `accepted` in **accepted Schedule** means that the temporal assignment is the current canonical/effective assignment under the applicable proposal/effect + Authority/policy semantics. It does **not** establish a universal domain `Acceptance` primitive and does not mean that every participant accepted Participation.

```text
Scheduling proposal
!= current accepted Schedule

current accepted Schedule
!= Participation response `accepted`

current Schedule/change
!= Acknowledgement of that Schedule/change
```

Acknowledgement answers a separate question:

```text
Who explicitly took notice of this specific Schedule target/material version/change?
```

and therefore:

```text
delivery/read/display evidence != Acknowledgement
Acknowledgement(v1) != Acknowledgement(v2) after a material Schedule change
Acknowledgement != Authority / Decision / effective change
```

Generic cross-domain `Acceptance` was tested and rejected as a standalone kernel primitive. Scheduling UI such as `Accept`, `Apply`, or `Use this` maps to the relevant proposal/effect operation rather than a universal Acceptance object.

Decision/Approval/effective-change persistence and Version/material-equivalence mechanics remain separately owned deferred dependencies. No Schedule reopening is required.

---

# 2026-08-13 — Decision / effective Schedule closure amendment

Decision v0 resolves the semantic Decision/effective-change boundary for Schedule without changing temporal identity or accepted-placement semantics.

Current chain where consequence requires explicit resolution:

```text
Scheduling proposal
!= Acknowledgement
!= family/proposal-specific positive response
!= Approval / Decision
!= current effective Schedule
!= later Actual
```

Canonical separation:

```text
Decision
= bounded resolution of the scheduling question/proposal

Schedule
= current accepted/effective temporal assignment
```

A Decision may approve, reject, defer or retain the current placement. Therefore a Decision does not imply that Schedule changed. Conversely, an already-authorized bounded automation policy may legitimately apply a Schedule change without fabricating a new human Decision.

When a Decision does produce a Schedule change, the Schedule concept owns the resulting current temporal state and its effective history. Decision/Authority/Provenance explain the resolution, legitimacy and lineage where material.

Material proposal/version changes do not inherit earlier Decision/Approval automatically. Decision time, effective Schedule time and Actual occurrence/execution time remain distinct.

Provider reconciliation remains capable of retaining conflicting imported proposals/source states until a policy/reconciliation process establishes the current Schedule; last-write-wins is not a canonical rule.

Downstream closure:

```text
Schedule ↔ Decision                 RESOLVED
Schedule ↔ Approval                 RESOLVED
Schedule ↔ effective change         RESOLVED — Schedule owns state
Schedule ↔ Reconciliation boundary  RESOLVED semantically
```

Version/material-equivalence mechanics, proposal reusable identity, detailed provider/source-precedence reconciliation, technical Principal/enforcement, offline/sync conflicts and physical revision persistence remain independently deferred.

**Schedule v0 verdict is unchanged. REOPEN = 0.**

---

# 2026-08-13 — Version / material-equivalence downstream closure amendment

Version v0 closes Schedule's former `Version / material-equivalence`, revision-history and stale-base conflict dependencies without changing Schedule identity or temporal semantics.

```text
Schedule identity/context
= the accepted temporal-assignment context for a schedulable subject

Schedule material state
= the materially relevant accepted placement state at a point in its history

Version
= a reference to that material state for the purpose/facet being evaluated
```

A material reschedule, unscheduling, precision change, or materially different placement creates a later material Schedule state while preserving the same Schedule/subject identity unless the operation establishes a genuinely different independent placement. Historical proposals, Acknowledgements, Participation responses, Decisions, Confirmations and evaluations remain bound to the Schedule state they actually concerned.

Prior semantic state does not silently carry across a material Schedule change. Non-material equivalence may preserve applicability only when the relevant temporal facet/purpose is unchanged. Provider `SEQUENCE`, ETag, sync revision, hash or storage row version may support integration/concurrency but does not define LifeOS semantic Schedule Version automatically.

Concurrent/offline Schedule edits may branch from one material base state. Version preserves those divergent states and bases; Authority/Decision/reconciliation determines which state becomes current or whether a merged/reconciled state is created. Version itself does not choose the winner and last-write-wins is not a canonical rule.

AI/system scheduling proposals and material mutations must retain the material base state where stale application could overwrite newer intent. After material divergence, a stale proposal/action must be re-evaluated rather than silently applied.

Schedule history may remain reconstructible without requiring universal event sourcing, one versions table, or indefinite retention of all private source payloads. Visibility of a Schedule projection remains separate from Visibility of hidden source state/history.

The historical Version/revision/offline-conflict dependency is now downstream-closed semantically. Proposal reusable identity, detailed provider/source-precedence reconciliation, Principal/enforcement, retention and physical persistence remain independently owned.

No Schedule hardening failed. **Schedule remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `version.md`;
- `../checkpoints/version-material-equivalence-v0-validation.md`.

---

# 2026-08-13 — Reconciliation / Source Precedence downstream closure amendment

Reconciliation v0 closes Schedule's detailed provider/source-precedence and conflict-resolution semantic dependency without changing Schedule identity or temporal semantics.

Canonical separation:

```text
competing Schedule proposals / material states
!= Reconciliation
!= current accepted Schedule
!= later Actual

Reconciliation
= contextual process/capability handling material competition

Schedule
= owner of the current accepted/effective temporal assignment
```

A provider placement, user edit, organizer proposal, AI proposal or offline branch does not become current merely because it is newer, arrived last, comes from a particular provider, or was created by the organizer. Source Precedence is valid only when a bounded policy/Authority establishes it for the relevant target/facet/context/time.

Reconciliation may select one state, combine compatible temporal changes, correct/supersede a state, defer, escalate or leave the conflict unresolved. An already-authorized deterministic scheduling rule may reconcile a bounded conflict without fabricating a human Decision; a material judgment may instead culminate in a separate Decision.

Availability, Capacity and Temporal Constraints may inform feasibility/evaluation, but none is a universal winner-selection rule. The resulting current Schedule remains owned by Schedule; Actual later records what really occurred rather than being used as reconciliation history.

Version preserves competing/predecessor material Schedule states and Provenance preserves materially relevant lineage/basis. Conflict/source/rationale Visibility remains independently governed, including safe free/busy projections.

Universal last-write-wins, newest-provider-wins, organizer-always-wins and user-always-wins remain rejected.

Downstream classification:

```text
Schedule ↔ Reconciliation       RESOLVED
Schedule ↔ Source Precedence    RESOLVED — bounded policy only
Schedule ↔ Actual               RESOLVED — expectation vs reality unchanged
```

Proposal reusable identity, exact effective dating, provider mapping, Principal/enforcement, retention and physical sync/persistence remain independently SAFE DEFERRED.

No Schedule hardening failed. **Schedule remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `reconciliation.md`;
- `../checkpoints/reconciliation-source-precedence-v0-validation.md`.