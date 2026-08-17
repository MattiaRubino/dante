# LifeOS Logical Model — Slice C External Benchmark Record v1

**Status:** current Slice-C benchmark record  
**Verified:** 2026-08-17  
**Scope:** Time / Reality logical representation  
**Policy:** external systems are structural evidence and anti-pattern evidence, never LifeOS ontology authority

---

## 1. Purpose

This record captures the current external evidence used to challenge and harden Slice C. It follows `../external-benchmark-policy-v1.md` and intentionally samples direct product, adjacent platform, specialist and infrastructure/standard systems rather than copying one calendar/task schema.

For each mechanism:

```text
SOURCE
PROBLEM
MECHANISM
INVARIANT / INSIGHT
LIMITATION / ANTI-PATTERN
LIFEOS DISPOSITION
REOPEN IMPACT
```

All product behavior below was checked against current official documentation on 2026-08-17. Stable standards are used for structural evidence; vendor-specific behavior is treated as evolving.

---

## 2. EVID-C01 — RFC 5545 / iCalendar recurrence and temporal forms

```text
SOURCE
IETF RFC 5545 — Internet Calendaring and Scheduling Core Object Specification (iCalendar)
https://www.rfc-editor.org/rfc/rfc5545

PROBLEM
Calendar systems need recurring-set semantics, individual recurrence-instance identity, local/floating/UTC time forms and exception handling.

MECHANISM
DATE and DATE-TIME values;
floating local time;
UTC and TZID-bound local time;
RRULE/RDATE/EXDATE recurrence sets;
RECURRENCE-ID for one recurrence instance;
instance rescheduling without changing which recurrence instance is being referenced.

INVARIANT / INSIGHT
current temporal placement and recurrence-instance identity are different concerns;
wall-clock and absolute-instant semantics must remain distinguishable;
calendar recurrence is not merely repeated fixed-second arithmetic.

LIMITATION / ANTI-PATTERN
RFC 5545 is fundamentally calendar-set oriented. It is not a complete LifeOS model for quota-per-period, completion-relative or arbitrary anchor-stream recurrence.
Using RECURRENCE-ID/original datetime as the universal LifeOS Occurrence identity would fail non-calendar recurrence families.

LIFEOS DISPOSITION
ADAPT structural principles;
DO NOT copy iCalendar as kernel ontology or persistence schema.

REOPEN IMPACT
supports current Domain/Logical separation; no Domain reopen.
```

---

## 3. EVID-C02 — Google Calendar recurring instances

```text
SOURCE
Google Calendar API — Recurring events
https://developers.google.com/workspace/calendar/api/guides/recurringevents

PROBLEM
One recurring event series needs individually addressable instances that can be changed without rewriting the whole series.

MECHANISM
recurringEventId links an instance to the recurring event;
originalStartTime identifies the original recurrence position and remains distinct from the instance's current start after a move;
instance-specific updates become exceptions to the series.

INVARIANT / INSIGHT
moved instance identity != current scheduled start;
one-off exception != structural series revision.

LIMITATION / ANTI-PATTERN
originalStartTime works naturally for calendar-generated instances but cannot be the universal LifeOS identity for quota/completion-relative/anchor-stream recurrence.
Provider instance/series IDs remain provider identity.

LIFEOS DISPOSITION
ADAPT instance-versus-current-placement separation;
REJECT provider IDs/datetime as LifeOS canonical Occurrence identity.

REOPEN IMPACT
reinforces selected Slice-C candidate; no reopen.
```

---

## 4. EVID-C03 — Microsoft Graph patterned recurrence

```text
SOURCE
Microsoft Graph — recurrencePattern / recurrenceRange / patternedRecurrence
https://learn.microsoft.com/graph/api/resources/recurrencepattern
https://learn.microsoft.com/graph/api/resources/recurrencerange
https://learn.microsoft.com/graph/api/resources/patternedrecurrence

PROBLEM
Recurring calendar items need a repeating pattern separated from the range over which it applies.

MECHANISM
recurrencePattern defines frequency/interval/positions;
recurrenceRange separately defines start/end/no-end/number-of-occurrences and recurrence time-zone context.

INVARIANT / INSIGHT
pattern shape != effective range;
zone/range framing is material recurrence context rather than incidental UI state.

LIMITATION / ANTI-PATTERN
calendar-centric semantics do not cover every LifeOS generative family and do not determine LifeOS source/Occurrence identity.

LIFEOS DISPOSITION
ADAPT pattern/range separation and explicit temporal framing;
DO NOT copy provider enums as universal recurrence taxonomy.

REOPEN IMPACT
supports current Recurrence LR-05 design.
```

---

## 5. EVID-C04 — Todoist scheduled-date vs completion-date recurrence

```text
SOURCE
Todoist Help — Introduction to recurring dates
https://www.todoist.com/help/articles/introduction-to-recurring-dates-YUYVJJAV

PROBLEM
Repeated work may recur from the planned schedule or from when the prior execution was actually completed.

MECHANISM
ordinary `every` recurrence advances from the scheduled/original recurring date;
completion-based `every!` advances from completion date/time.

INVARIANT / INSIGHT
calendar-relative recurrence != completion-relative recurrence;
the choice of anchor materially changes future expectations.

LIMITATION / ANTI-PATTERN
product syntax is task-centric and not a general recurrence ontology;
completion-date behavior cannot define LifeOS Actual semantics merely because a task product exposes it.

LIFEOS DISPOSITION
ADAPT anchor-family distinction;
DO NOT copy Todoist syntax or task lifecycle.

REOPEN IMPACT
strongly supports Recurrence family separation; no reopen.
```

---

## 6. EVID-C05 — Reclaim Habit source versus conflict behavior

```text
SOURCE
Reclaim Help — Habits / Habit scheduling documentation
https://help.reclaim.ai/en/articles/4125436-how-to-create-and-manage-habits
https://help.reclaim.ai/en/articles/5439006-habits-faq

PROBLEM
A recurring behavioral expectation needs a default temporal pattern while the scheduler may move, shorten, skip or defend individual generated calendar placements under conflict rules.

MECHANISM
Habit has recurring/default event semantics plus separate scheduling behavior around rescheduling, skipping, duration and protection;
future scheduling is handled inside a bounded scheduling horizon rather than requiring infinite concrete future events.

INVARIANT / INSIGHT
recurring behavioral source != recurrence expression != individual placement != movement/conflict policy;
operational future expansion can be bounded/lazy.

LIMITATION / ANTI-PATTERN
Reclaim's product semantics are optimization-oriented and should not become LifeOS Routine/Occurrence ontology.

LIFEOS DISPOSITION
ADAPT separation and bounded-horizon insight;
DO NOT copy Habit resource/schema.

REOPEN IMPACT
supports lazy Occurrence/materialization direction.
```

---

## 7. EVID-C06 — Motion dynamic scheduling

```text
SOURCE
Motion Help — Auto-scheduling / task scheduling behavior
https://help.usemotion.com/en/articles/8999890-auto-scheduling
https://help.usemotion.com/en/articles/8714436-tasks-in-motion

PROBLEM
Actionable work has duration, priorities, start/deadline constraints and chunking/availability rules, while the resulting calendar placement may change dynamically.

MECHANISM
Task/constraint inputs are evaluated to create and later adjust scheduled work blocks.

INVARIANT / INSIGHT
intended work and scheduling inputs are distinct from the produced accepted/operational placement;
one Activity may need several planned blocks.

LIMITATION / ANTI-PATTERN
a scheduler product can intentionally optimize and reshuffle more aggressively than LifeOS governance may permit;
product task status is not universal LifeOS reality.

LIFEOS DISPOSITION
ADAPT intention/constraint/placement separation;
REJECT task/calendar block identity collapse.

REOPEN IMPACT
supports Slice B+C composition.
```

---

## 8. EVID-C07 — Android Health Connect planned vs completed exercise

```text
SOURCE
Android Developers — Health Connect training plans / planned exercise sessions
https://developer.android.com/health-and-fitness/health-connect/features/training-plans

PROBLEM
Health/workout systems need to represent a planned exercise separately from an exercise session that actually occurred.

MECHANISM
PlannedExerciseSessionRecord represents planned training content/time;
executed exercise-session records represent completed activity and can be linked to the plan context.

INVARIANT / INSIGHT
planned execution != actual execution record;
actual measurements/session data should not overwrite the plan.

LIMITATION / ANTI-PATTERN
health data is specialist-domain evidence; its record taxonomy is not a general LifeOS kernel.

LIFEOS DISPOSITION
ADAPT planned-versus-actual separation;
KEEP specialist measurement semantics bounded.

REOPEN IMPACT
supports Schedule/Session/Actual separation.
```

---

## 9. EVID-C08 — Apple HealthKit workout-session lifecycle

```text
SOURCE
Apple Developer Documentation — HKWorkoutSession / workout-session lifecycle
https://developer.apple.com/documentation/healthkit/hkworkoutsession

PROBLEM
One actual workout episode may start, pause, resume and end while remaining one logically continuous session.

MECHANISM
workout-session lifecycle supports preparation/start/pause/resume/stop/end behavior;
active duration can differ from elapsed wall-clock duration.

INVARIANT / INSIGHT
pause does not necessarily create a new execution identity;
elapsed time != active time;
Session lifecycle != broader work/result lifecycle.

LIMITATION / ANTI-PATTERN
HealthKit session states and workout semantics remain specialist/API behavior, not universal Activity/Outcome state.

LIFEOS DISPOSITION
ADAPT Session identity and pause/active-time principles;
DO NOT import HealthKit ontology.

REOPEN IMPACT
supports Session LR-01 direction.
```

---

## 10. EVID-C09 — HL7 FHIR Appointment versus Encounter

```text
SOURCE
HL7 FHIR R5 Appointment / Encounter
https://hl7.org/fhir/R5/appointment.html
https://hl7.org/fhir/R5/encounter.html

PROBLEM
Clinical systems distinguish planned booking/scheduling from the actual care encounter that occurred.

MECHANISM
Appointment represents planned booking context;
Encounter represents actual encounter context and can reference Appointment;
Encounter exposes actualPeriod separately from plannedStartDate/plannedEndDate.

INVARIANT / INSIGHT
planned appointment != actual real-world occurrence;
actual timing can differ while original planning remains meaningful.

LIMITATION / ANTI-PATTERN
clinical resource identity/lifecycles are specialist semantics and cannot be generalized into LifeOS TemporalEvent/Actual roots.

LIFEOS DISPOSITION
ADAPT planning-versus-actual separation;
REJECT healthcare ontology copy.

REOPEN IMPACT
supports Event/Schedule/Actual boundary.
```

---

## 11. EVID-C10 — PostgreSQL date/time and interval semantics

```text
SOURCE
PostgreSQL 18 Documentation — Date/Time Types and Date/Time Functions and Operators
https://www.postgresql.org/docs/18/datatype-datetime.html
https://www.postgresql.org/docs/18/functions-datetime.html

PROBLEM
Physical time storage/calculation must cope with named time zones, daylight-saving transitions, civil calendar arithmetic and elapsed-duration arithmetic.

MECHANISM
PostgreSQL distinguishes timestamp with/without time zone, time-zone conversion and interval components;
calendar interval operations can differ from fixed elapsed-hour arithmetic across DST.

INVARIANT / INSIGHT
civil/calendar time and elapsed time are not safely reducible to one fixed-second model;
named-zone interpretation carries rules beyond a numeric offset.

LIMITATION / ANTI-PATTERN
PostgreSQL data types are physical mechanisms, not semantic owners;
`timestamp with time zone` alone does not preserve every original LifeOS wall-clock/floating/coarse intention automatically.

LIFEOS DISPOSITION
USE as physical-feasibility and negative-normalization evidence;
DEFER exact PostgreSQL representation to Physical Model.

REOPEN IMPACT
no Domain reopen; reinforces explicit LR-04 temporal semantics.
```

---

## 12. EVID-C11 — Reclaim legacy elapsed-event completion as negative evidence

```text
SOURCE
Reclaim historical/legacy Task scheduling behavior documented in official help material during product evolution.

PROBLEM
Some scheduler workflows infer task progress/completion from calendar event passage to simplify rescheduling.

MECHANISM
legacy behavior could treat an elapsed task event as completed for scheduling purposes unless the user/state model corrected it.

INVARIANT / INSIGHT
calendar passage is not reliable evidence of actual execution.

LIMITATION / ANTI-PATTERN
this shortcut destroys the distinction between expected time and real execution when used as canonical truth.

LIFEOS DISPOSITION
NEGATIVE BENCHMARK:
Schedule elapsed != Actual;
Schedule elapsed != completed Outcome.

REOPEN IMPACT
none; directly reinforces accepted LifeOS invariant.
```

---

## 13. Cross-source synthesis

The strongest recurring structural pattern is not one common schema but repeated separation among:

```text
source/policy
recurrence pattern
instance identity
current placement
actual execution
result
provider/source identity
```

The benchmark also exposes where external systems intentionally collapse or specialize these layers for their product domain. LifeOS should reuse the good separation while rejecting the collapse as kernel ontology.

---

## 14. Candidate implications

### Universal TemporalEvent

External evidence does not justify it. Mature systems frequently retain different resources/states for plan, instance and actual behavior.

### Owner-specific only

External systems prove that local typing is feasible, but shared temporal patterns/reconciliation/history recur enough that LifeOS benefits from reusable representation mechanisms.

### Layered Typed Time & Reality

Best fit with both accepted LifeOS semantics and observed structural evidence.

### Universal event sourcing

No benchmark requires it for the logical model. It remains an implementation technique, not a semantic conclusion.

### Provider/RRULE kernel

Rejected because external calendar formats are narrower than accepted LifeOS recurrence semantics.

---

## 15. Freshness and reopen record

```text
LAST VERIFIED
2026-08-17

PRIMARY/OFFICIAL SOURCES
YES

MATERIAL PASS DEPENDENCY ON ONE VENDOR
NO

VOLATILE PRODUCT BEHAVIOR
Todoist / Reclaim / Motion / Google / Microsoft / Android / Apple details
-> refresh if later decision materially depends on changed behavior

STABLE STRUCTURAL SOURCES
RFC 5545 / FHIR / PostgreSQL documented semantics
-> refresh at Whole-Logical final regression or if implementation choice relies on version-specific behavior

DOMAIN REOPEN EVIDENCE
0

LOGICAL BLOCKER
0
```
