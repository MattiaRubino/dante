<!-- LIFEOS-CANONICAL-CONTINUATION document="test-corpus-v1.md" follows="test-corpus-v1.md" -->
> **Canonical continuation of `test-corpus-v1.md`.** This physical file is Part 2 of the same logical test corpus. Earlier scenarios remain unchanged and permanent; this continuation adds Slice-C Time / Reality regression pressure.

# P. Slice C accepted regression expansion — Time / Reality

These scenarios are permanent R3 regression pressure after Slice C activation. They replay Slice-A identity/reference, Slice-B intention/execution and integrated A+B invariants where applicable.

## TC-P01 — Moved recurring instance keeps identity

```text
Routine
Gym Mon/Wed/Fri

Occurrence
Wednesday expected instance

Original expectation
Wednesday 18:00

Current accepted Schedule
Thursday 19:00

Actual
Thursday 19:12-20:24
```

Required:

```text
same Occurrence identity
original expectation retained
Schedule revision retained
Actual retained separately
```

Current start/end must not define Occurrence identity.

---

## TC-P02 — Flexible quota recurrence before exact scheduling

```text
Routine
Train 3 times per week
```

At the beginning of the week no exact days/times have been chosen.

Required:

```text
three expected semantic instances may be derivable/distinguishable
exact Schedule may be absent
no arbitrary weekdays invented
no eager infinite future materialization required
```

---

## TC-P03 — Equivalent quota slots have no artificial ordinal meaning

Three quota Occurrences are semantically equivalent until another rule, dependency, schedule or source semantics orders them.

Required:

```text
stable distinguishability where addressable
!= semantic first/second/third invented for implementation convenience
```

---

## TC-P04 — Recurrence source revision preserves past expectations

```text
Routine state V1
Mon/Wed/Fri

past Occurrences
#20 #21 #22

Routine state V2
Tue/Thu
```

Required:

```text
past Occurrences remain governed/explainable under V1
future derivation uses V2 where applicable
no retroactive regeneration of #20-#22 under V2
```

---

## TC-P05 — Completion-relative recurrence uses qualifying Actual

```text
Replace filter 30 days after actual previous replacement
```

Occurrence #12 was scheduled for 10 August but actually completed on 12 August.

Required:

```text
next qualifying expectation anchors from accepted Actual completion
not stale scheduled end
unless source rule explicitly says otherwise
```

If no qualifying completion exists, later chain elements may remain undefined rather than behaving like a fixed calendar series.

---

## TC-P06 — Anchor-stream recurrence

```text
After every qualifying photography Session
expect one backup instance
```

Two photography Sessions occur.

Required:

```text
Session A -> Backup Occurrence A
Session B -> Backup Occurrence B
```

No generic IF/THEN workflow root is required merely because the source is an anchor stream.

---

## TC-P07 — Cyclic positional doctor shifts

```text
4 night shifts
3 rest days
repeat
```

Required:

```text
cycle anchor + ordered positions + repeat length preserved
no canonical requirement to flatten years into literal dates
one moved/swap occurrence does not automatically rewrite whole cycle
```

---

## TC-P08 — DST spring gap

Named-zone wall-clock Schedule/Recurrence requests `2026-03-29 02:30 Europe/Rome`, a local time affected by the spring transition.

Required:

```text
original wall-clock meaning retained
resolution/exception policy explicit where consequential
no silent parser default promoted to canonical user intent
```

---

## TC-P09 — DST fall overlap

Named-zone wall-clock meaning requests `2026-10-25 02:30 Europe/Rome`, which is ambiguous across the fall transition.

Required:

```text
ambiguity is representable/resolvable
chosen instant does not erase original named-zone wall-clock intent
```

---

## TC-P10 — Travel: floating versus named-zone behavior

Case A:

```text
Breakfast 08:00 local wherever I am
```

Case B:

```text
Team meeting 08:00 Europe/Rome
```

User travels to Tokyo.

Required:

```text
A follows applicable local-time policy
B remains Rome-wall-clock anchored
```

The same textual hour must not imply the same temporal semantics.

---

## TC-P11 — Date-only event is not a 24-hour capacity block

```text
Event
Birthday
Schedule
17 August — all day/date-based
```

Required:

```text
date visibility retained
capacity reservation decided separately
no automatic 00:00-24:00 busy semantics
```

---

## TC-P12 — Two planned placements, three actual Sessions

```text
Activity
Study chapter

accepted Schedule placements
Tue 18:00-20:00
Wed 18:00-19:00

actual Sessions
Tue 18:15-19:35
Tue 21:00-21:40
Wed 18:10-18:45
```

Required:

```text
one Activity
two planned placements
three Sessions
no one-to-one cardinality requirement
```

---

## TC-P13 — Schedule revised four times

One meeting is accepted at four successive placements before it occurs.

Required:

```text
current Schedule query returns latest accepted state
history can reconstruct all material accepted placements and their chronology
Actual remains separate
```

---

## TC-P14 — Explicit mid-execution extension versus ordinary overrun

Case A:

```text
meeting Schedule 15:00-16:00
at 15:50 participants explicitly extend expected end to 16:30
Actual ends 16:24
```

Case B:

```text
meeting Schedule 15:00-16:00
no accepted revision
Actual ends 16:24
```

Required:

```text
A -> Schedule revision + Actual
B -> unchanged Schedule + Actual overrun
```

---

## TC-P15 — Event postponed with date TBD

```text
Event
Concert

historical accepted Schedule
20 Sep 21:00

provider status
postponed; new date unknown
```

Required:

```text
Event identity retained
historical Schedule retained
current Schedule may be absent
no fake replacement date
```

---

## TC-P16 — Deadline passes but Actual is unknown

An application deadline passes. No trusted submission source and no user confirmation exists.

Required:

```text
past-deadline temporal condition may be derived
no automatic missed/failed Outcome
no automatic known non-realization
```

---

## TC-P17 — Later user confirmation establishes non-realization

After TC-P16 the user states that the application was not submitted.

Required:

```text
Actual may now establish known non-realization
contextual Outcome may be established where appropriate
source/provenance preserved
prior period of uncertainty not rewritten as always-known fact
```

---

## TC-P18 — Spontaneous Session without prior intention

Unexpected production issue causes work from 10:00-11:20.

Required:

```text
Session can be recorded truthfully
no retrospective Activity/Schedule fabricated as though it existed beforehand
later contextual links may be added without rewriting historical intention
```

---

## TC-P19 — Pause/resume versus end/restart

Case A:

```text
Session start 18:00
pause 18:40-18:50
resume
end 19:30
```

Case B:

```text
Session 1 18:00-18:40 END
Session 2 21:00-21:50
```

Required:

```text
A normally one Session
B normally two Sessions
no universal pause-duration threshold decides identity
```

---

## TC-P20 — Session split/merge correction

A tracker captured one broad Session that is later proven to contain two different execution episodes; another day it captured two fragmented Sessions later proven continuous.

Required:

```text
split/merge correction supported
current accepted structure can change
original capture/provenance remains reconstructible
```

---

## TC-P21 — Overlapping Sessions and aggregation

```text
Walking 17:00-18:00
English listening 17:00-18:00
```

Required:

```text
walking exposure = 1h
English exposure = 1h
unique wall-clock coverage = 1h
```

A naive universal `SUM(duration)=2h of day consumed` is invalid.

---

## TC-P22 — Shared Event Actual versus actor participation

```text
Shared Event Actual
meeting occurred 10:08-11:23

Actor A attended 10:08-11:23
Actor B attended 10:08-10:45
Actor C did not attend
```

Required:

```text
one shared Event Actual
actor-specific Participation reality remains separate
no duplicate shared Actual per actor
```

---

## TC-P23 — Provider moved recurring instance

Provider series instance originally Monday 10:00 is moved to Tuesday 15:00.

Required:

```text
provider original-instance anchor preserved as source metadata
LifeOS same Occurrence retained after move
provider current start != LifeOS identity
```

---

## TC-P24 — Out-of-order provider sync and identifier churn

Provider sends:

1. revised instance state;
2. later a stale older payload;
3. migration changes provider identifier.

Required:

```text
latest arrival != automatic canonical winner
ExternalRef history/mapping retained
LifeOS Occurrence identity stable where reconciliation supports continuity
```

---

## TC-P25 — Provider cannot export LifeOS recurrence losslessly

A LifeOS completion-relative or quota recurrence cannot be represented losslessly by a calendar provider.

Required:

```text
LifeOS recurrence semantics remain canonical
adapter may degrade, expand, store provider metadata or reject export explicitly
kernel is not weakened to match provider
```

---

## TC-P26 — Ten-year recurrence without eager row explosion

A daily Routine has a ten-year horizon.

Required:

```text
future derivation can remain lazy/bounded
material/history-bearing Occurrences remain stably reconstructible
no semantic requirement to persist every future day immediately
```

---

## TC-P27 — Hard Temporal Constraint violated by reality

```text
Constraint
workout must finish by 20:00

Schedule
18:30-19:30

Actual Session
18:45-20:15
```

Required:

```text
truthful Session/Actual retained
constraint violation may be derived/evaluated
Actual is not rejected or rewritten to make plan appear valid
```

---

## TC-P28 — Timed Conditional Policy activates but effect fails

```text
Policy
At 18:00, if still unresolved, send reminder
```

At 18:00 the basis is satisfied; notification service fails.

Required:

```text
activation history may remain meaningful
response failure != no activation
Schedule/Recurrence/Actual are not fabricated
```

---

## TC-P29 — Outcome correction after authoritative source update

Initial source says exam passed; later authoritative correction says failed.

Required:

```text
current accepted Outcome may change
prior assertion/source history retained
Outcome correction != Session/Actual rewrite unless those facts also changed
```

---

## TC-P30 — Simple one-off appointment stays compact

```text
Event
Dentist appointment
Schedule
18 Aug 15:00-15:30
```

No recurrence, execution timer, special Outcome or complex history is needed.

Required:

```text
Event + Schedule is sufficient
no artificial Occurrence wrapper for one-off Event
no artificial Session/Outcome
```

If later Actual timing/attendance becomes material, add only the required reality semantics.

---

# Slice-C additional high-value queries

52. What is the currently accepted Schedule for a subject, and what Schedule was accepted at time T?
53. Which Occurrence is referenced after a one-off reschedule, and what was its original expectation?
54. Which material source/Recurrence state generated a historical Occurrence?
55. Which future Occurrences are currently derivable without requiring all future instances to be persisted?
56. Which expected instances were never generated by rule versus generated then skipped/cancelled?
57. Which recurrence semantic family governs this source: wall-clock, elapsed, quota, completion-relative, anchor-stream or cycle?
58. What period frame determines membership for this quota recurrence?
59. Is a temporal value date-only, floating local, named-zone wall-clock, absolute instant, duration or another accepted typed form?
60. Which accepted placements belong to one divisible Activity?
61. Which Sessions actually occurred for an Activity/Occurrence, including overlapping or unplanned execution?
62. What elapsed, paused and active duration is known, and what precision/source supports it?
63. Did an Actual become established, or did only the Schedule/deadline time pass?
64. Is the current state unknown or known non-realization?
65. What Outcome was established, and which lifecycle/operational state remains separately owned?
66. Which Temporal Constraints applied, and which were violated by truthful Actual?
67. Which provider series/instance/original-start identifiers currently or historically map to this LifeOS Occurrence?
68. Can the system explain a moved provider instance without changing LifeOS Occurrence identity?
69. Can current Schedule/Session/Actual state be answered without replaying the subject's entire lifetime history in application memory?
70. Can a simple one-off Event remain compact without artificial Occurrence/Session/Outcome wrappers?
71. Can a spontaneous Session remain truthful without fabricating retrospective intention?
72. Can a DST gap/overlap be resolved without losing the original named-zone wall-clock semantics?
73. Can a lossless provider export failure be explained without changing canonical LifeOS recurrence meaning?
74. Can an activation be distinguished from downstream policy response success/failure?
75. Can one interval appear in Schedule, Constraint and Availability contexts while remaining semantically distinguishable?

---

# Slice-C mutation regression anchors

Every later affected slice/physical candidate must continue to reject at least:

```text
Occurrence = current/original datetime universally
Occurrence = Schedule
persist all future Occurrences indefinitely
one recurring Activity advanced forever
one universal recurrence algorithm/ontology
UTC-only semantic normalization
Schedule elapsed => Actual/Outcome
Schedule overwritten by Actual
one start/end per divisible Activity
all-day => capacity reservation
pause => new Session always
global Session non-overlap
provider identity => LifeOS identity
one universal Outcome/status
hard constraint => impossible Actual
Conditional Policy = Recurrence
global event sourcing required for current state
generic VirtualRef required by lazy recurrence
```

---

# Slice-C regression result at acceptance candidate stage

```text
TC-P01..P30
PASS / PASS WITH explicitly stage-bound Slice-D/F history/governance mechanics

NEW HIGH-VALUE QUERIES
52..75

SLICE-A REGRESSION FAILURE
0

SLICE-B REGRESSION FAILURE
0

INTEGRATED A+B REGRESSION FAILURE
0

REFERENCE MECHANISM
RETAIN + HARDEN

DOMAIN REOPEN REQUIRED
0
```

After exact Slice-C remote QA these tests become permanent cumulative pressure. Before Slice D, the mandatory Integrated A+B+C checkpoint must replay the affected prior and new corpus rather than treating this local PASS as sufficient.
