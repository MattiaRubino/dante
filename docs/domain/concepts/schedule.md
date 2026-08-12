# Schedule v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-11  
**Meaning of accepted:** best current decision; reopenable with better evidence  
**Workstream:** Core Domain Model v0 — Time cluster

## Canonical definition

> **A Schedule is the current accepted temporal assignment of a schedulable subject, expressing when its execution or occurrence is intended or expected to take place at the precision currently committed. A Schedule may be revised without changing the identity of its subject, and remains distinct from temporal constraints, recurrence rules, capacity blocking, participant response, Acknowledgement, and what actually happened.**

Schedule answers:

> **When is this currently intended or expected to happen?**

It does not answer what the thing is, why it matters, whether it is recurring, whether a time is merely allowed/preferred, whether capacity is consumed, whether every participant accepted, whether another actor acknowledged a change, or what actually happened.

---

# 1. Why Schedule exists

LifeOS needs reusable temporal assignment that can change independently from domain identity.

```text
Activity
Study chapter 5

Schedule
Tuesday 18:00–20:00
```

```text
Event
Client meeting

Schedule
Tuesday 15:00–16:00
```

```text
Routine Occurrence
Workout — Wednesday instance

Schedule
Thursday 19:00–20:30
```

Activity remains Activity, Event remains Event, Occurrence remains the same logical instance. Schedule supplies accepted temporal placement.

Putting mutable `start_at/end_at` directly on every domain object and destructively overwriting them would lose temporal history and blur planned/current/Actual distinctions.

---

# 2. Core temporal position

```text
Domain intention / recurring source
        ↓
Occurrence identity where applicable
        ↓
original temporal expectation
        ↓
Schedule revisions
        ↓
current accepted Schedule
        ↓
Actual execution / attendance / occurrence
```

Schedule occupies one layer: **current accepted temporal assignment**.

It is neither subject identity nor Actual result.

---

# 3. Proposed versus current Schedule

A candidate placement proposed by user, LifeOS, provider or AI is not automatically current Schedule truth.

```text
Scheduling proposal
        ↓ applicable proposal/effect + Authority/policy semantics
Current accepted Schedule
```

The word `accepted` here means **the temporal assignment that is currently canonical/effective in the applicable governing context**. It does **not** imply a universal cross-domain Acceptance primitive.

Generic Acceptance was tested later in Acknowledgement v0 and rejected as a standalone kernel concept.

Therefore:

```text
Schedule proposal accepted/applied
→ scheduling proposal/effect semantics
NOT generic Acceptance entity
```

Authority v0 answers who/what may legitimately make the bounded scheduling effect effective. Acknowledgement v0 answers who explicitly took notice of a specific resulting proposal/change/version. Participation response answers whether a participant intends to take part.

These are independent:

```text
current accepted Schedule
!= participant accepted Participation
!= participant Acknowledgement of Schedule change
```

The exact Decision/Approval/effective-change persistence model remains deferred.

---

# 4. Schedule versus Activity

```text
Schedule != Activity
```

An Activity may exist without a Schedule. Rescheduling does not change Activity identity.

Estimated effort, scheduled duration and Actual effort remain separate.

---

# 5. Schedule versus Event

Event owns occurrence-centred meaning; Schedule represents its current accepted temporal placement.

```text
Schedule != Event
```

Event identity may survive reschedule.

## Postponed Event with no replacement Schedule

```text
Event
Concert

historical Schedule
20 September 21:00

provider update
POSTPONED — new date TBD

current Schedule
none
```

This preserves Event identity and historical expectation without inventing fake precision.

> **An Event may temporarily have no current accepted Schedule while historical placements remain reconstructible.**

Postponed/cancelled lifecycle/disposition remains separate from Schedule.

---

# 6. Schedule versus Occurrence

```text
Occurrence = which generated instance?
Schedule   = when is this instance currently assigned?
```

Occurrence identity must not be derived from current Schedule placement.

A generated Occurrence may exist before exact placement and retain identity after one-off rescheduling.

```text
Occurrence #27
original expectation Wednesday 18:00
current Schedule Thursday 19:00–20:30
```

It remains occurrence #27.

---

# 7. Schedule versus Routine / Recurrence

```text
Routine / recurring Event
        ↓
Recurrence semantics
        ↓
Occurrences
        ↓
Schedules
```

One-off Schedule revision does not automatically mutate Recurrence or Routine policy.

```text
Schedule != Routine
Schedule != Recurrence
```

---

# 8. Schedule versus Actual

```text
Schedule 15:00–16:00
Actual   15:18–16:25
```

This is deviation, not automatically a Schedule revision.

```text
Original Schedule 15:00–16:00
Current Schedule  15:30–16:30
Actual            15:38–16:24
```

All are meaningful.

> **Schedule != Actual.**

LifeOS must not rewrite Schedule to match Actual merely because execution starts early/late or runs long.

Derived comparisons may include early/late start, overrun/underrun, punctuality and estimation quality.

---

# 9. Revisions may move any temporal boundary

Schedule revisions may move earlier/later, lengthen/shorten, or change only one boundary.

Temporal geometry of the change can be derived; semantic reason may be separately preserved through Provenance/Decision context.

A Schedule can also be revised during execution if participants explicitly change the expected end. This remains distinct from an unplanned overrun in Actual.

---

# 10. Original expectation / current Schedule / history

LifeOS must preserve enough history to distinguish:

```text
original accepted expectation
→ revision 1
→ revision 2
→ current accepted Schedule
```

Previous placements remain historical facts rather than being silently overwritten.

This supports auditability, provider reconciliation, AI explanation, replanning analytics and planned-versus-Actual comparison against the correct effective expectation.

Physical revision/version mechanism is deferred.

---

# 11. Schedule versus Deadline / target / Temporal Constraint

```text
Schedule != Deadline
Schedule != target date/window
Schedule != Temporal Constraint
```

Example:

```text
Deadline
30 April 23:59

Schedule
27 April 18:00–19:00
```

A deadline/constraint may exist without Schedule.

Same temporal shape can have different meaning:

```text
"Tuesday afternoon"

accepted assignment → Schedule
allowed/preferred window → Temporal Constraint
```

Classification follows semantics, not timestamp shape alone.

---

# 12. Schedule versus Availability / Capacity / busy state

Temporal placement does not automatically consume capacity or mean `busy`.

```text
scheduled != capacity consumed
scheduled != universally busy
```

Availability/Capacity and Reservation/Claim semantics remain separate.

A visible free/busy projection may also exist without exposing private Schedule source details.

---

# 13. Precision and all-day/date semantics

Schedule precision should reflect what is actually committed.

Examples may include exact date-time, date/all-day, or another bounded accepted placement supported by the Time model.

Do not fabricate exact time merely because the system prefers a calendar grid.

Floating local time, UTC and named-time-zone semantics must remain representable where relevant; external standards are benchmark evidence, not kernel authority.

---

# 14. Schedule change versus Acknowledgement

A material Schedule change and actor acknowledgement of that change are distinct.

```text
Schedule v1 = 15:00
Schedule v2 = 16:00

Luca Acknowledgement(v2)
```

```text
Schedule v2 current
!= Luca acknowledged v2
```

One actor may acknowledge while another has not. Acknowledgement of v1 does not silently acknowledge materially different v2.

Schedule itself therefore does not own delivery/read/common-ground state.

---

# 15. Schedule versus Participation response

One shared Event can have one current Schedule while actors hold different response states.

```text
Meeting
Schedule 15:00–16:00

A accepted Participation
B tentative
C declined
```

> **Current accepted Schedule does not mean every participant accepted Participation.**

Participation response remains actor-scoped and independent from temporal assignment.

---

# 16. Authority / Visibility / AI boundaries

Authority determines who/what may legitimately make the bounded scheduling effect effective.

Visibility determines what Schedule/projection/source information may be exposed.

Acknowledgement records explicit taking-notice.

AI may propose placement but does not gain Authority or human Acknowledgement merely because it can optimize.

```text
AI proposal != current Schedule
AI source access != disclosure permission
AI inference != human Acknowledgement
```

---

# 17. Product / UI implications

Product UI may expose:

```text
Scheduled for…
Move to…
All day
This afternoon
Proposed time
Apply
Keep current time
```

`Apply` or `Accept` can be scheduling-proposal UI language; it must not create a generic Acceptance concept.

Acknowledgement, when valuable, should appear separately as natural common-ground action such as `Got it` rather than being inferred from schedule visibility.

---

# 18. External benchmark interpretation

Mature calendars/standards provide useful evidence for date vs date-time, time zones, recurrence/instance separation, transparency/busy semantics and rescheduling history.

LifeOS borrows/adapts useful behavior but does not make iCalendar/Google/Apple vocabulary or lossless mapping a kernel invariant.

LifeOS semantics first; adapters later.

---

# 19. Core invariants

1. **Schedule = current accepted temporal assignment.**
2. **Schedule != schedulable subject identity.**
3. **Schedule != Activity/Event/Occurrence/Routine/Recurrence.**
4. **Schedule != Temporal Constraint/Deadline/target.**
5. **Schedule != Availability/Capacity/Reservation by default.**
6. **Schedule != Actual.**
7. **Occurrence identity does not depend on current Schedule.**
8. **Event may retain identity while current Schedule is absent after postponement.**
9. **Original/current/historical Schedule placements remain reconstructible where material.**
10. **Actual deviation does not silently revise Schedule.**
11. **A proposal does not become current Schedule without applicable effect/Authority/policy semantics.**
12. **Generic cross-domain Acceptance is not required for Schedule.**
13. **Current accepted Schedule != participant accepted Participation.**
14. **Current Schedule/change != actor Acknowledgement of that change.**
15. **Acknowledgement(v1) does not imply Acknowledgement(v2) after material change.**
16. **Authority to change Schedule != Visibility of private scheduling sources.**
17. **AI proposal/optimization != Authority/current Schedule/human Acknowledgement.**
18. **No competing canonical temporal truth should be duplicated across subject + Schedule persistence.**

---

# 20. Adjacent Dependency Sweep — current

## RESOLVED

- Schedule ↔ Activity/Event/Occurrence/Routine/Recurrence boundaries remain distinct.
- Schedule ↔ Actual: planned/current temporal assignment != realization.
- Schedule ↔ Temporal Constraint/Deadline/target: assignment != boundary/goal horizon.
- Schedule ↔ Availability/Capacity: temporal placement != capacity truth.
- Schedule ↔ Participation response: current shared time != actor willingness to participate.
- Schedule ↔ Authority: governance/effect owned by Authority, not Schedule.
- Schedule ↔ Visibility: exposure/source privacy separate from temporal assignment.
- Schedule ↔ Acknowledgement: current/material change != explicit taking-notice.
- Schedule ↔ generic Acceptance: universal primitive rejected; scheduling proposal response remains proposal/effect-specific.

## SAFE DEFERRED

### Decision / Approval / effective-change representation

**Owner:** Relationships / Reasoning — Decision review.  
**Why safe:** Schedule owns resulting current temporal state; Authority owns governance; proposal/effect can remain separate.  
**Reopening trigger:** current Schedule cannot explain/reconstruct why a proposed revision became effective without making Schedule itself a Decision record.  
**Tests to rerun:** CORE-02, CORE-04, CORE-09, MA-06, XCON-03, XCON-04.

### Version / Schedule revision persistence

**Owner:** Version/logical model.  
**Why safe:** historical reconstruction requirement is fixed without physical mechanism.  
**Reopening trigger:** material schedule history cannot be preserved without duplicating/overwriting truth.  
**Tests to rerun:** CORE-02, CORE-09, CORE-10, CORE-13, XCON-03.

### Reservation / Capacity Claim

**Owner:** Resource/Allocation/Reservation + scheduling logical model.  
**Why safe:** scheduling and capacity consumption are explicitly separate.  
**Reopening trigger:** resource coordination cannot prevent conflict without collapsing Schedule into Reservation.  
**Tests to rerun:** CORE-04, MA-14, XCON-04.

### Provider conflict/reconciliation

**Owner:** Provenance/Decision/Integration.  
**Why safe:** provider assertions do not automatically overwrite current truth.  
**Reopening trigger:** multi-provider Schedule cannot preserve authoritative/current/historical state without changing Schedule semantics.  
**Tests to rerun:** CORE-02, CORE-09, MA-12, XCON-03.

```text
REOPEN                         0
unclassified material items    0
```

---

# 21. Rejected alternatives

Rejected:

- start/end duplicated as competing source truth on every domain object;
- Schedule = Event/Occurrence/Recurrence/Actual;
- Schedule = Deadline/Temporal Constraint;
- Schedule = busy/Capacity/Reservation;
- current Schedule inferred from Actual timestamps;
- provider date/time vocabulary as ontology authority;
- AI proposal automatically becoming Schedule;
- participant acceptance equated with current Schedule;
- Acknowledgement equated with current Schedule;
- universal Acceptance primitive merely to apply scheduling proposals;
- placeholder/fake precision for postponed unresolved Event.

---

# 22. Reopening triggers

Reopen Schedule v0 if later evidence shows that:

1. current accepted assignment cannot remain distinct from constraints/Actual/capacity;
2. Event postponement cannot preserve identity/history without a different temporal model;
3. Decision/Version persistence requires materially different Schedule identity;
4. multi-provider reconciliation creates competing canonical temporal truths;
5. multi-actor response/Acknowledgement cannot remain independent from Schedule state;
6. logical persistence cannot avoid duplicated canonical timing while retaining history.

Until then, Schedule remains the current accepted temporal-assignment capability.
