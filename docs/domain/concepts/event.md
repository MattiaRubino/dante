# Event v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-10  
**Meaning of accepted:** best current decision; reopenable with better evidence  
**Workstream:** Core Domain Model v0

## Canonical definition

> **An Event is a persistent representation of an expected occurrence for which temporal placement is intrinsic to its meaning. An Event describes something expected to happen and may include participation, organizer, location, and availability semantics; it is not primarily an action whose completion is the main meaning. Planned occurrence, actual attendance/outcome, and provenance remain distinct.**

Examples include appointments, meetings, lessons, exams, hearings, flights, concerts, ceremonies, races, interviews, shifts, webinars, and other time-centred commitments or occurrences.

An Event can be all-day or span multiple days. External participants are optional.

## Validation basis

Event v0 was reviewed against:

- the LifeOS feature-discovery simulation, including lessons, exams, hearings, shifts, medical visits, interviews, flights, meetings, dinners, ceremonies, concerts, races, and external commitments;
- the existing LifeOS core glossary and execution-status documents;
- the already accepted Goal v0, Plan v0, and Activity v0 boundaries;
- external patterns from iCalendar/RFC 5545, Google Calendar event and recurring-instance semantics, and Apple EventKit event/availability semantics.

External systems are benchmark inputs, not models to copy directly.

## Core distinction: occurrence-centred versus action-centred

The primary distinction from Activity is semantic rather than visual or calendar-based.

```text
Activity
Write the report

Event
Client meeting
```

An Activity is action-centred: the user intends to perform work or behavior.

An Event is occurrence-centred: the fact that something is expected to happen in a temporal context is central to its identity.

Therefore:

> **Having an exact time does not turn an Activity into an Event.**

Examples:

```text
Activity
Workout
18:00-19:00
```

remains an Activity even though it occupies a scheduled interval.

```text
Event
Concert
21:00-23:00
```

is an Event because the occurrence itself is time-centred.

## Event versus Activity

Representative distinctions:

| Activity | Event |
|---|---|
| Call the dentist | Dentist appointment |
| Prepare slides | Client presentation |
| Study chapter 4 | University lesson |
| Prepare for exam | Exam |
| Pack luggage | Flight |
| Run 5 km at 18:00 | Race at 09:00 |

Event and Activity may be linked without duplication.

```text
Activity: Prepare documents
    prepares_for ->
Event: Exam
```

```text
Event: Interview
    followed_by ->
Activity: Send follow-up
```

The exact relationship vocabulary belongs to the future Relationship Model.

## Temporal placement is intrinsic, but not immutable

For an Event, expected temporal placement is part of the Event meaning.

```text
Event
Flight AZ123
10 September 14:20
```

If the flight is officially moved to 18:00, the Event remains the same Event while its accepted schedule changes.

This is different from an Activity whose schedule may simply be a planner decision about when to perform the work.

Temporal identity must therefore support change without rewriting history.

## Original expectation, current schedule, and actual occurrence

LifeOS must distinguish at least three temporal layers conceptually:

```text
Original expectation
        ↓
Schedule revisions
        ↓
Current accepted schedule
        ↓
Actual occurrence
```

Example — official reschedule before the meeting:

```text
Original expectation
15:00-16:00

Current accepted schedule
15:30-16:30
```

Example — no reschedule, but reality differs:

```text
Current accepted schedule
15:00-16:00

Actual
15:18-16:25
```

The second case is not a reschedule. It is an actual occurrence that differed from the accepted expectation.

## Actual time may differ in either direction

Actual start/end are independent from planned start/end and may occur before, after, or exactly at the expected times.

Valid examples include:

```text
Planned 15:00-16:00
Actual  14:52-15:55
```

```text
Planned 15:00-16:00
Actual  14:55-16:20
```

```text
Planned 15:00-16:00
Actual  15:20-15:50
```

```text
Planned 15:00-16:00
Actual  15:00-16:00
```

Therefore concepts such as `late_start`, `early_start`, `overrun`, or `finished_early` should normally be derived from planned-versus-actual comparison rather than stored as foundational Event truth.

Conceptually:

```text
start deviation = actual_start - accepted_start
end deviation   = actual_end   - accepted_end
actual duration = actual_end   - actual_start
```

The future temporal model must not assume deviations only occur later than planned.

## Event state, participation intention, and actual attendance are different

These dimensions must remain separate.

Example:

```text
Event state
CONFIRMED

My participation intention
ACCEPTED

Actual attendance
DID_NOT_ATTEND
```

An Event may be confirmed while a user declines it. A user may accept an Event but not actually attend.

This prevents overloaded status fields.

Potential semantics include, without fixing a physical enum yet:

- Event state: confirmed, tentative, cancelled, rescheduled, etc.;
- participant response: accepted, tentative, declined, needs action, etc.;
- actual attendance: attended, partially attended, did not attend, unknown, etc.

Exact state machines remain deferred.

## Event passage of time is not completion

When an Event's expected end passes, LifeOS must not automatically infer a generic `completed = true`.

Different questions remain separate:

```text
Did the Event occur?
Did the user attend?
Was there an outcome?
Was an external result produced?
How does LifeOS know?
```

Some ordinary Events need no execution outcome at all.

Other Events may produce meaningful outcomes:

```text
Event: Exam
Outcome: passed
```

```text
Event: Race
Actual result: 1h48m
```

```text
Event: Medical visit
Outcome: diagnosis / prescription / follow-up
```

Those outcomes are not equivalent to Event attendance.

## Event and Actual/Evidence

An Event may produce Actual records, Observations, measurements, outcomes, or other Evidence relevant to Goal criteria.

Example:

```text
Event
Organized photographic hike
        ↓
Actual attendance / observations
10 km walked
        ↓
Evidence
        ↓
Goal criterion
Physical activity
```

This follows the same evidence principle established by Activity v0: Goal evaluation is driven by valid evidence, not only by execution originally planned for that Goal.

An Event therefore does not need an artificial duplicate Activity merely to contribute to a Goal.

## Event and Goal/Plan

An Event may exist without an explicit Goal or Plan.

It may also be linked directly to one or more Goals or Plans where useful.

Examples:

```text
Goal: Pass the exam
Event: Exam on 15 October
```

```text
Goal: Run a half marathon
Event: Half marathon race
```

```text
Plan: Move house
Event: Key handover appointment
```

The exact relationship semantics are deferred to the Relationship Model.

## Event and related Activities

An Event may have preparation, travel, follow-up, or other Activities linked to it.

Examples:

```text
Activity: Prepare slides
prepares_for -> Event: Presentation
```

```text
Activity: Travel to airport
supports -> Event: Flight
```

```text
Event: Interview
followed_by -> Activity: Send thank-you message
```

LifeOS must not automatically generate a duplicate `Attend event` Activity for every Event. Participation/attendance semantics belong to the Event itself unless a genuinely distinct action exists.

## Event versus Deadline

A deadline is a temporal boundary within which another intention or requirement must be satisfied.

```text
Activity
Submit declaration

Deadline
30 April
```

The deadline may be displayed in calendar/timeline surfaces without becoming an Event.

Therefore:

> **Event != Deadline.**

The exact deadline/window model belongs to the temporal/constraint review.

## Event versus Milestone

A Milestone marks a meaningful checkpoint, achievement, delivery, or decision state.

```text
Milestone
Design approved
```

An Event may be related to that milestone:

```text
Event
Design review — 30 September 15:00
```

but they are not the same concept.

Therefore:

> **Event != Milestone.**

## Event versus Calendar Block / Availability

The existence of an Event does not automatically imply that the entire Event interval must consume scheduling capacity.

Examples:

```text
Event
Birthday — all day
```

should not automatically make the entire day unavailable.

```text
Event
Optional webinar — 15:00-16:00
```

may intentionally leave availability open depending on user policy.

External calendar systems similarly separate event occurrence from free/busy or availability semantics.

Therefore:

> **Event != Calendar Block / Availability.**

The exact capacity/protection model is deliberately deferred to the temporal cluster.

## All-day and multi-day Events

All-day and multi-day semantics are temporal forms of Event, not separate kernel entity types.

Examples:

```text
Event
Wedding
all day
```

```text
Event
Conference
3 days
```

Whether those intervals block planning capacity is a separate availability concern.

## Event recurrence versus Routine

Recurring Event and Routine are not assumed to be synonyms.

Preliminary distinction:

```text
Recurring Event
Team meeting every Monday 10:00
```

represents a repeating sequence of expected occurrences.

```text
Routine
Train Monday / Wednesday / Friday
```

represents a reusable behavioral rule/pattern that guides or generates execution.

Some real-life cases may blur this boundary, such as a weekly family dinner. The exact recurrence-series versus Routine relationship must be stress-tested during Routine review rather than resolved prematurely here.

## Recurring occurrence identity and rescheduling

A specific occurrence in a recurring Event series must retain identity when moved.

Conceptually:

```text
Recurring Event Series
Weekly lesson
        │
        ├── occurrence 1
        ├── occurrence 2
        └── occurrence 3
                original: 10:00
                current: 16:00
```

Occurrence 3 remains the same occurrence. History must not pretend it was always at 16:00.

Google Calendar's `originalStartTime` semantics for recurring instances are a useful external benchmark for this principle, though LifeOS is not required to copy its data model.

The full Series/Occurrence model is deferred to the temporal cluster.

## Shift as a stress-test case

A work shift is both work performed and a time-centred external commitment.

```text
Hospital shift
08:00-16:00
```

Its intrinsic temporal placement, presence/attendance semantics, possible shift swaps, and external commitment make it Event-like in the current model.

Activities may occur during the shift, and actual worked time may differ from the accepted shift schedule.

LifeOS does not currently require a separate `Shift` kernel primitive.

## External identity and integrations

LifeOS Event identity must remain separate from provider identity.

Do not make a provider ID the canonical Event identity.

Conceptually:

```text
LifeOS Event
    │
    └── ExternalRecord
        provider = Google Calendar
        external_id = ...
        iCalUID = ...
```

This allows imports, provider migration, deduplication, and multiple external representations without surrendering canonical identity to a single integration.

## Provenance and corrections

Event facts, schedule revisions, attendance, and Actual data must preserve source/provenance where relevant.

If imported or inferred actual times are later corrected by the user, current truth may change while audit/history preserves the previous value and correction source.

Example:

```text
Imported actual start
15:05

Corrected by user
15:20
```

Statistics use the corrected current value while audit/history preserves the relevant previous record.

## Current invariants

1. `Event != Activity`.
2. `Event != generic Schedule`.
3. `Event != Deadline`.
4. `Event != Milestone`.
5. `Event != Calendar Block / Availability`.
6. Temporal placement is intrinsic to Event meaning, even when that placement can change.
7. Giving an Activity an exact scheduled time does not transform it into an Event.
8. An Event may exist without a Goal or Plan.
9. An Event may contribute directly to Goal criteria through outcome, attendance, observations, measurements, or other valid Evidence.
10. An Event does not require external participants.
11. Event state, participant response, and actual attendance are separate dimensions.
12. Passage of scheduled time does not automatically create completion or an execution outcome.
13. Original expectation, current accepted schedule, and actual occurrence must be distinguishable.
14. Actual start/end may be earlier, later, or equal to planned start/end; no one-direction delay assumption is allowed.
15. Early/late/overrun/finished-early semantics are normally derived from planned-versus-actual comparison rather than foundational Event state.
16. Cancellation and rescheduling must preserve identity and relevant history.
17. A recurring occurrence retains identity even when individually moved.
18. Event recurrence and Routine are not assumed to be synonyms.
19. An Event may have related preparation/follow-up Activities without requiring an artificial duplicate Activity representing attendance.
20. An Event may be all-day or multi-day without becoming a different kernel type.
21. Event existence does not automatically imply full scheduling-capacity occupancy.
22. LifeOS Event identity and external provider identity remain separate.
23. Imported/inferred facts and later user corrections preserve provenance/history.

## Stress-test coverage

Representative cases that fit the current model include:

| Case | Current representation |
|---|---|
| Dentist appointment | Event + participation/attendance as needed |
| Client meeting | Event + related preparation/follow-up Activities |
| University lesson | Event |
| Exam | Event + external result/evidence |
| Hearing | Event |
| Work shift | Event-like commitment + Actual worked time |
| Flight | Event + provider/external identity |
| Concert | Event |
| Wedding | all-day Event |
| Conference | multi-day Event |
| Race | Event + actual result/evidence |
| Optional webinar | Event + separate availability semantics |
| Recurring team meeting | recurring Event series; occurrence model deferred |
| Meeting starts early | accepted schedule preserved + earlier Actual start |
| Meeting starts late | accepted schedule preserved + later Actual start |
| Meeting officially moved | schedule revision + preserved prior expectation |
| Event produces unexpected Goal evidence | Event Actual/Observation -> Evidence -> Goal criterion |

No reviewed case currently requires splitting Event into separate kernel primitives such as Appointment, Meeting, Flight, Exam, Shift, Lesson, or Ceremony.

## Deliberately deferred questions

The following are not decided by Event v0:

- exact Event lifecycle/state machine;
- exact participant and attendance state machines;
- exact representation of schedule revisions;
- exact Series/Occurrence persistence model;
- exact recurrence rule representation;
- Event recurrence versus Routine boundary in ambiguous repeated-life cases;
- Calendar Block / Availability / capacity-reservation model;
- Deadline and temporal-constraint model;
- exact Actual/Observation/Evidence persistence;
- relationship vocabulary for preparation, follow-up, support, causation, and Goal/Plan linkage;
- provider deduplication/import matching rules;
- SQL/API representation.

## Decision note

Event v0 intentionally strengthens the previous LifeOS glossary definition by making temporal placement intrinsic rather than merely present, separating Event state from participation and actual attendance, separating accepted schedule from actual occurrence, and explicitly allowing actual times to deviate in either direction.

The older glossary remains preserved as source material until changes are propagated deliberately after adjacent concepts and the intention/execution cluster are reviewed.