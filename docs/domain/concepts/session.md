# Session v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-11  
**Meaning of accepted:** best current decision; reopenable with better evidence  
**Workstream:** Core Domain Model v0 — Time cluster

## Canonical definition

> **A Session is a persistent record of a bounded episode of actual execution or performed behavior, representing one logically continuous execution attempt whose elapsed and active time may be tracked separately. A Session describes when execution actually took place; it is not the planned temporal placement, the intended work identity, or the broader execution outcome.**

A Session answers the temporal execution question:

> **When did this execution episode actually take place?**

It does not by itself answer:

- what the intended work or behavior fundamentally is;
- when that work was planned;
- whether the broader Activity, Occurrence, Goal, or Plan was completed;
- what quantitative or qualitative outcome resulted;
- whether an Event occurred or a participant attended;
- why the execution matters;
- how LifeOS knows all non-temporal facts about the execution.

The core distinction is therefore:

```text
Schedule
= planned / accepted temporal placement

Session
= actual execution episode

Actual
= broader truth about what happened
```

A Session is actual execution history, not a planned calendar block.

---

## Why this concept exists

The accepted LifeOS domain model already requires a strong separation between intention, scheduling, execution, and evidence.

`Activity v0` requires:

- intended work identity to survive rescheduling;
- estimated effort to remain distinct from scheduled duration and actual effort;
- one Activity to be executable across multiple temporal slices;
- actual execution not to rewrite the original intention.

`Occurrence v0` requires:

- one expected generated instance to have stable identity;
- an Occurrence to exist even when no execution happens;
- one Occurrence to potentially be realized through multiple execution slices;
- Actual to remain separate from expected-instance identity.

`Schedule v0` requires:

- accepted temporal placement to remain distinct from actual execution;
- actual early/late/shorter/longer execution not to silently rewrite the Schedule;
- one schedulable subject to support multiple planned placements when needed.

The existing LifeOS execution-status documentation also requires planned and actual start/end/duration to remain distinguishable and explicitly rejects time passage as automatic completion.

Without a Session concept, LifeOS would be forced into one of two weak models:

1. overwrite planned Schedule timestamps with actual timestamps; or
2. place all timing details directly inside a broad `Actual` record and lose the reusable identity/lifecycle of individual execution episodes.

Session provides the missing temporal execution layer.

---

## Validation basis

Session v0 was reviewed against:

### Existing LifeOS documentation

- `docs/product/v1-execution-status.md`;
- `docs/product/v1-scheduling-flexibility.md`;
- `docs/product/feature-discovery-simulation-2026-08.md`;
- accepted `Activity v0`;
- accepted `Event v0`;
- accepted `Routine v0`;
- accepted `Occurrence v0`;
- accepted `Schedule v0`;
- the validated Intention & Execution cluster checkpoint.

### Representative LifeOS scenarios

The review included:

- study planned for one block but actually executed earlier/later;
- one Activity completed across several work episodes;
- one Routine Occurrence split across morning and evening execution;
- paused and resumed timer-based work;
- stopped work resumed hours later;
- spontaneous unplanned debugging;
- manually entered historical work time;
- imported workout/session data;
- workout sessions with measurements and internal phases;
- Event attendance whose actual interval does not need an artificial Session;
- overlapping passive and active behaviors;
- accidental timer fragmentation requiring merge;
- one incorrectly broad Session requiring split;
- correction of imported start/end times;
- open/running Sessions with unknown end;
- Sessions producing Evidence for Goals not originally associated with the execution.

### External benchmark patterns

External systems were used as evidence, not copied as LifeOS architecture.

Relevant patterns include:

- Android Health Connect distinguishing planned exercise sessions from executed exercise-session records;
- Health Connect using stable record identity and source metadata for workout/session-like execution history;
- Apple HealthKit workout-session lifecycle supporting start, pause, resume, stop/end behavior inside one session identity;
- health/workout systems associating measurements, route, distance, heart rate, laps, or segments with a session without equating the session itself with every measurement;
- mature time-tracking products preserving tracked intervals independently from the task/project objects they relate to.

The common useful principle is that actual execution intervals have identity and lifecycle distinct from plans, tasks, and broader outcomes.

---

## Core model

The current conceptual chain is:

```text
Domain intention / expected instance
Activity / Occurrence
        │
        ↓
Accepted Schedule placement(s)
        │
        │ planned
════════╪════════════════════════════
        │ reality
        ↓
Session(s)
        │
        ↓
Actual / Outcome / Measurements
        │
        ↓
Evidence
```

For an ordinary Event, the default path is different:

```text
Event
  ↓
Schedule
  ↓
Actual event occurrence / attendance / outcome
```

A Session is introduced only when a distinct executable episode genuinely needs tracking.

This prevents Session from becoming a redundant wrapper around every temporal fact.

---

## Session versus Schedule

A Schedule records accepted future/current temporal assignment.

A Session records actual execution.

Example:

```text
Activity
Study chapter 5

Schedule
18:00 -> 21:00

Session
17:40 -> 20:15
```

The Schedule remains 18:00–21:00 because that was the accepted plan.

The Session records that actual execution started earlier and ended earlier.

LifeOS may derive:

```text
start deviation = -20m
scheduled duration = 3h
session elapsed duration = 2h35m
```

but must not rewrite the Schedule to match reality merely because execution differed.

Therefore:

> **Session != Schedule.**

---

## Planned placement does not require one-to-one Session mapping

A planned placement and an actual Session are not required to correspond one-to-one.

Example:

```text
Activity
Study chapter 5

Planned placements
Tuesday 18:00 -> 20:00
Wednesday 18:00 -> 19:00
```

Actual execution:

```text
Session 1
Tuesday 18:15 -> 19:35

Session 2
Tuesday 21:00 -> 21:40

Session 3
Wednesday 18:10 -> 18:45
```

The reality is three Sessions against two planned placements.

A future relationship model may describe which Session realizes which planned placement where useful, but the kernel must not require perfect cardinality.

This is necessary for interrupted work, spontaneous continuation, partial execution, replanning, and retrospective time entry.

---

## Session versus Activity

An Activity is an actionable intention.

A Session is one actual execution episode related to work or behavior.

Example:

```text
Activity
Prepare presentation
```

may exist for several days and have:

```text
Session 1
Monday 09:00 -> 10:20

Session 2
Tuesday 14:15 -> 15:00

Session 3
Thursday 18:00 -> 20:00
```

The Activity answers:

> What am I intending to do?

The Sessions answer:

> During which actual episodes did I work on it?

Therefore:

> **Session != Activity.**

Ending a Session does not complete the Activity automatically.

---

## Session versus Occurrence

An Occurrence identifies one expected instance produced by a recurring/generative source.

A Session represents actual execution.

Example:

```text
Routine
English practice 3x/week
        ↓
Occurrence
Tuesday expected practice instance
```

Possible reality:

```text
Session 1
18:00 -> 18:40

Session 2
21:00 -> 21:50
```

Therefore:

```text
1 Occurrence
2 Sessions
```

The same Occurrence could instead have:

```text
0 Sessions
Outcome: skipped
```

Therefore:

> **Session != Occurrence.**

An Occurrence may exist without Session, and a Session may exist without prior Occurrence.

---

## Session versus Event actual occurrence

LifeOS must not create a Session automatically for every Event that actually occurs.

Example:

```text
Event
Client meeting

Schedule
15:00 -> 16:00

Actual event occurrence
15:12 -> 16:25

Attendance
attended
```

The actual Event interval already has natural Event semantics.

Creating this by default would duplicate the same real-world fact:

```text
Session
15:12 -> 16:25
```

Therefore:

> **Event attendance/actual occurrence does not require a Session by default.**

A Session may still exist in relation to an Event when a distinct executable episode is useful.

Example:

```text
Event
Technical workshop

Session
Hands-on coding exercise performed during workshop
```

The Session exists because there is separate execution semantics, not merely because the Event occupied time.

---

## Session versus Actual

Session is part of actual history, but it is not the complete `Actual` concept.

A Session primarily represents execution timing and its episode identity.

Broader Actual semantics may include:

- execution outcome;
- completion/partial completion;
- quantities;
- pages;
- repetitions;
- distance;
- quality;
- difficulty;
- cost;
- subjective assessment;
- attendance;
- result;
- replacement behavior;
- measurements;
- provenance and confirmation.

Example:

```text
Activity
Study chapter 5

Sessions
18:00 -> 18:40
21:00 -> 21:50

Actual
Outcome: partially completed
Pages: 32
Difficulty: high
Total active time: 1h30m
```

The Actual may aggregate data from multiple Sessions.

Likewise, an Actual outcome may exist without detailed Sessions at all.

Example:

```text
Activity
Call insurance company

Actual
completed
```

with no need to track start/end.

Therefore:

> **Session != broader Actual / Outcome.**

The later Observed Reality & Evidence cluster will define the exact relationship.

---

## Session is actual, not planned

The kernel uses Session for actual execution only.

LifeOS user-facing language may still say:

> "Tomorrow's study session"

for a scheduled block because that language is natural.

That UI wording must not force the domain to represent future planned blocks as Session records.

Canonical domain rule:

```text
planned execution slice
= Schedule placement

actual execution slice
= Session
```

This prevents planned and actual timing from collapsing into one structure.

---

## Session may exist without prior Schedule

Unplanned execution is valid.

Example:

```text
Activity
Write article

Schedule
none
```

The user begins spontaneously:

```text
Session
10:17 -> 11:35
```

The Session is valid because it records reality.

No retrospective Schedule needs to be invented.

This preserves the distinction between:

```text
planned
versus
actually happened
```

---

## Session may exist without a pre-existing Activity

LifeOS must also support spontaneous execution that did not have a prior formal Activity.

Example:

```text
Unexpected production issue
```

The user spends:

```text
Session
10:00 -> 11:20
Label/context: unplanned debugging
```

The Session may later be related to a Plan, Activity, Goal, incident, subject, or other context if useful.

LifeOS must not fabricate historical intention by pretending that an Activity existed before the execution when it did not.

This follows the broader Domain Atlas principle:

> **Observed reality does not require prior planned intention.**

However, a Session should still carry enough semantic context to be intelligible; a completely anonymous interval is weak evidence and weak execution history.

The exact ownership/relationship cardinality is deferred.

---

## Session identity

Session identity is independent from its timestamps.

Example:

```text
Session S123
18:05 -> 19:05
```

The user later corrects the start:

```text
Session S123
17:55 -> 19:05
```

This remains the same Session.

Therefore:

> **session identity != start timestamp + end timestamp.**

Session requires stable LifeOS identity so corrections, imports, sync reconciliation, split/merge history, and offline capture do not create accidental duplicates.

Provider IDs may be mapped to a Session, but provider identity is not LifeOS identity.

---

## Running Sessions

A Session can exist before its end is known.

Example:

```text
Session
start: 18:12
end: unknown
```

This represents an execution episode currently in progress.

The Session may subsequently be:

- paused;
- resumed;
- ended;
- corrected;
- abandoned/recovered after tracker failure;
- reconciled with imported data.

The exact lifecycle enum is intentionally deferred, but the domain must support an open Session.

---

## Pause and resume remain inside one Session

A pause does not automatically terminate Session identity.

Example:

```text
Session
start 18:00

pause
18:40 -> 18:50

resume
18:50

end
19:30
```

This is one logically continuous execution attempt.

Derived timing may be:

```text
elapsed duration = 1h30m
paused duration  = 10m
active duration  = 1h20m
```

Therefore:

> **pause != Session boundary by default.**

This supports Pomodoro-like interruption, brief breaks, phone calls, rest intervals, workout pauses, and temporary interruption without fragmenting history.

---

## Ending and later restarting normally creates another Session

If the user explicitly ends/closes execution and later begins again, the normal interpretation is a new Session.

Example:

```text
Session 1
18:00 -> 18:40
END

Session 2
21:00 -> 21:50
```

Both may relate to the same Activity or Occurrence.

The distinction is semantic:

```text
PAUSE
same execution episode remains open

END / CLOSE
execution episode ended
```

LifeOS must not use a universal arbitrary threshold such as:

```text
pause > 30 minutes => new Session
```

because the meaningful boundary varies by context.

LifeOS may propose recovery when a tracker appears stale, but must not silently rewrite history based on a generic duration threshold.

---

## Elapsed, active, and paused time are distinct

For a Session with pauses:

```text
start -> end
```

represents wall-clock elapsed span.

Actual active work may exclude pause intervals.

Conceptually LifeOS must distinguish:

- elapsed duration;
- active duration;
- paused duration.

For simple manually entered Sessions, only elapsed duration may be known.

LifeOS must not invent active-time precision when it was not captured.

The exact pause-segment persistence model is deferred.

---

## End Session does not mean work completed

Ending execution only says that this episode ended.

Example:

```text
Activity
Write report

Session
18:00 -> 19:00

Activity outcome
partial
```

or even:

```text
Activity outcome
unknown / not yet confirmed
```

Therefore:

> **Session lifecycle != Activity/Occurrence outcome lifecycle.**

Time passing and Session ending do not silently mark an Activity complete.

---

## Manual, timer-based, and imported Sessions share the same semantics

A Session can originate through different capture mechanisms.

Examples:

```text
source
stopwatch
```

```text
source
manual retrospective entry
```

```text
source
external integration
```

```text
source
automatically inferred under approved policy
```

These sources do not create different Session domain types.

They affect provenance, confidence, confirmation, correction authority, and reconciliation.

Therefore:

> **capture source != Session semantic type.**

---

## Timer and Stopwatch are capture/control mechanisms

Timer and Stopwatch are useful product tools, but they do not need to become parallel execution-history concepts.

Conceptually:

```text
Stopwatch / tracker
start
pause
resume
stop
        ↓
create/update
        ↓
Session
```

A countdown timer such as a 25-minute focus timer may exist operationally without producing a persisted Session if the user does not want execution tracking.

When it does record actual work, its persistent result is a Session.

Therefore:

> **Timer/Stopwatch != Session; they are mechanisms that may create or update Session.**

---

## Corrections preserve Session identity and history

Session timing may be corrected after capture.

Example:

```text
Imported Session
18:05 -> 19:05
```

User correction:

```text
17:55 -> 19:10
```

The corrected values become the current accepted actual timing while audit/provenance retains sufficient information to understand:

- original source;
- original timestamps;
- correction source;
- correction time;
- reason where available;
- current authoritative values.

A correction is not automatically a new Session.

---

## Split and merge

Execution capture may have structural errors.

### Split

A tracker records:

```text
Session
10:00 -> 12:00
```

The user later clarifies:

```text
10:00 -> 10:50 coding
10:50 -> 12:00 meeting
```

LifeOS must be able to split the original record into meaningful execution episodes without pretending that the original captured fact never existed.

### Merge

A tracker accidentally creates:

```text
Session A
10:00 -> 10:30

Session B
10:31 -> 11:00
```

The user confirms this was one continuous work episode.

LifeOS may merge them into one current Session representation while preserving traceability to the original records.

Therefore:

> **split/merge are corrections/reconciliation operations, not silent destructive rewrites.**

The physical implementation is deferred to history/versioning and persistence design.

---

## Session and measurements

A Session may provide temporal context for measurements or Observations.

Examples:

```text
Workout Session
07:05 -> 08:01

associated observations
- heart rate
- distance
- pace
- route
- energy expenditure
```

```text
Study Session
18:00 -> 19:15

associated observations
- pages read
- exercises completed
- focus rating
```

```text
Photography Session
05:30 -> 07:10

associated observations
- location
- photos captured
- walking distance
```

These facts should not force Session into an arbitrary universal metadata blob.

Conceptually:

```text
Session
   ↓
Measurements / Observations / Evidence
```

The later Data and Evidence clusters will determine the reusable data structures.

---

## Session and internal segments

Some execution episodes have meaningful internal structure.

Example workout:

```text
Session
Run workout

segments
- warmup
- interval 1
- recovery
- interval 2
- cooldown
```

These do not necessarily require five separate Sessions because they remain part of one coherent execution episode.

LifeOS should support specialist structures when justified but must not introduce a universal `SessionSegment` kernel primitive prematurely.

The distinction mirrors the existing Activity rule:

- semantic sub-work may use Activity decomposition;
- internal specialist phases may belong to the specialist module;
- temporal pause intervals may belong to Session timing;
- none automatically require new Session identity.

---

## Overlapping Sessions are not universally invalid

LifeOS must not impose a global invariant that Sessions cannot overlap.

Valid example:

```text
Session A
Walking
17:00 -> 18:00

Session B
English listening
17:00 -> 18:00
```

The user can genuinely perform both simultaneously.

Another valid example may involve passive monitoring or travel combined with another behavior.

However, some overlaps may be suspicious or impossible:

```text
Deep focused coding
10:00 -> 11:00

Driving
10:30 -> 11:30
```

LifeOS may surface conflicts, but the rule depends on semantic compatibility and context rather than raw timestamp overlap.

Therefore:

> **Session overlap policy is context-specific, not a universal database prohibition.**

---

## Overlap affects aggregation semantics

If two Sessions overlap completely:

```text
Walking
1h

English listening
1h
```

LifeOS may truthfully report:

```text
walking exposure = 1h
English exposure = 1h
unique wall-clock coverage = 1h
```

It must not automatically report:

```text
total elapsed day time = 2h
```

without clarifying the aggregation meaning.

Future analytics must distinguish at least conceptually between:

- category/domain time;
- active effort;
- elapsed Session duration;
- unique wall-clock coverage;
- intentionally double-counted multi-domain contribution.

Therefore:

> **`SUM(session.duration)` is not a universally valid measure of total time spent.**

---

## Session can contribute to multiple Goals without rewriting intent

A Session may produce Evidence relevant to Goals that were not its original purpose.

Example:

```text
Session
Photographic hike
06:00 -> 09:00
```

Actual observations may include:

```text
10.4 km walked
social interaction
photography practice
```

These may contribute to:

- fitness Goal;
- social Goal;
- photography Goal.

The Session itself does not need to be rewritten as though all those Goals motivated it from the start.

This preserves the accepted Domain Atlas rule:

> **Discovered relevance must not rewrite historical intention.**

---

## Session context and ownership

A Session should normally have enough context to explain what execution episode it represents.

Potential context may include:

- Activity;
- Occurrence;
- Plan;
- subject/resource;
- specialist record;
- descriptive label for spontaneous work;
- imported external semantic context.

LifeOS should not require a rigid universal parent tree such as:

```text
Session must belong to exactly one Activity
```

because spontaneous Sessions and multi-context execution exist.

At the same time, a Session should not become an unstructured generic time record with arbitrary JSON relationships.

The exact distinction between primary context, ownership, and secondary semantic relations belongs to the Relationship Model and persistence review.

---

## One Session and multiple semantic intentions

A real execution episode may serve more than one intention.

Example:

```text
Session
Walk while practicing spoken English with a friend
```

It may simultaneously support:

- a fitness Activity/Goal;
- an English-practice Activity/Goal;
- a social Goal.

LifeOS should not force arbitrary duplication into three identical Sessions merely to preserve domain links.

However, this does not imply that every Session should directly own arbitrary lists of Goals/Activities.

The formal relation semantics are deferred.

---

## Sessions and recurring behavior

Routine does not directly become Session.

The conceptual flow remains:

```text
Routine
  ↓
Occurrence
  ↓
Schedule optional
  ↓
Session(s)
  ↓
Actual / Outcome
```

A repeated observed Session pattern also does not silently create a Routine.

Example:

```text
user worked out every Tuesday for six weeks
```

may suggest a Routine, but repeated history is not equivalent to declared recurring intent.

AI may propose creation of a Routine, preserving provenance and user authority.

---

## Sessions and Events

Sessions may relate to Events, but no universal relation is assumed.

Useful examples:

```text
Event
Workshop

Session
Hands-on exercise
```

```text
Event
Flight

Session
Work on laptop during flight
```

```text
Event
Doctor appointment

Actual attendance
attended
```

The doctor appointment does not require Session merely because time elapsed.

This preserves the Event/Activity distinction established in the validated Intention & Execution cluster.

---

## Session timestamps and temporal semantics

Actual execution timestamps usually represent real instants, but LifeOS must not assume perfect timestamp precision in every capture path.

Possible data quality levels include:

- tracker-recorded exact instants;
- manually entered approximate times;
- imported rounded times;
- start known/end unknown while running;
- retrospective duration known but exact boundaries uncertain.

The future Actual/Provenance model must be able to express source and confidence/precision without inventing false certainty.

Unlike planned Schedule, actual execution is usually tied to real elapsed time, but date/time precision semantics still matter for manual and imported history.

---

## Session duration is derived where possible

When exact start/end and pause intervals are known:

```text
elapsed_duration = end - start
active_duration  = elapsed_duration - paused_duration
```

These are derived quantities.

LifeOS should avoid independently storing conflicting canonical duration values unless there is a legitimate reason, such as imported source data that reports duration but lacks exact boundaries.

When source data provides inconsistent boundaries and duration, provenance/reconciliation rules must decide the accepted current representation rather than silently normalizing history.

---

## Estimated effort, scheduled duration, and Session time remain separate

Example:

```text
Activity estimated effort
3h

Schedule
18:00 -> 21:00
scheduled duration = 3h

Session
17:40 -> 20:15
elapsed = 2h35m
active = 2h20m
```

All values answer different questions.

LifeOS must not assume:

```text
estimated effort
=
scheduled duration
=
active execution time
=
elapsed Session duration
```

This distinction is important for future estimation learning and replanning.

---

## Session lifecycle is intentionally narrow

The exact state machine is deferred, but Session lifecycle concerns execution-record state rather than work outcome.

Conceptually relevant states/actions may include:

- open/running;
- paused;
- ended/closed;
- corrected;
- split/merged through reconciliation;
- invalidated/deleted under data-correction policy.

These must not be overloaded with Activity outcomes such as:

- completed;
- partially completed;
- skipped;
- missed;
- replaced.

A Session can end while the Activity remains incomplete.

An Occurrence can be skipped and therefore have no Session at all.

---

## Session deletion versus correction

If a Session was created accidentally or represents false data, deletion/recovery rules may remove it according to the future data-history policy.

If the Session represents a real episode but has incorrect timing/context, correction is preferable to delete-and-recreate because the history remains meaningful.

The exact tombstone/recovery/audit behavior remains for persistence/history design.

---

## External identity and synchronization

Imported Session-like records may have provider-specific IDs.

LifeOS must preserve:

```text
LifeOS Session identity
!=
provider record identity
```

The integration layer may map:

- provider;
- external record ID;
- source application/device;
- import/update timestamps;
- source revision/version;
- deletion/tombstone where exposed.

Corrections made in LifeOS must not silently masquerade as provider-original values.

Conflict policy is deferred to Integration and Provenance reviews.

---

## AI authority

AI may assist with:

- suggesting that a stale running Session should be closed;
- detecting likely duplicate Sessions;
- proposing split/merge;
- linking an unplanned Session to likely Activities/Plans;
- deriving useful summaries;
- identifying schedule-vs-actual deviations;
- suggesting a Routine from repeated behavior.

AI must not silently:

- fabricate execution time;
- rewrite imported/user-confirmed Session boundaries without policy;
- convert a pause into a new Session arbitrarily;
- mark an Activity complete merely because a Session ended;
- invent prior intentional links to Goals/Activities.

Ambiguous AI corrections remain proposals unless user policy authorizes deterministic handling.

---

## Representative scenario matrix

| Scenario | Session interpretation |
|---|---|
| Study planned 18:00–21:00, actual 17:40–20:15 | one Session 17:40–20:15; Schedule unchanged |
| Activity worked on Monday, Tuesday, Thursday | three Sessions linked to same Activity |
| Routine Occurrence executed morning and evening | two Sessions for one Occurrence |
| Expected Routine Occurrence skipped | zero Sessions |
| Timer pause 10 minutes and resume | one Session with pause interval |
| Timer stopped, work restarted hours later | normally two Sessions |
| Session currently running | start known, end unknown |
| Manual retrospective entry | valid Session with manual provenance |
| Imported workout | valid Session with integration provenance |
| Unexpected debugging | Session may exist without prior Activity/Schedule |
| Client meeting attended | Event Actual; no Session required by default |
| Coding exercise during workshop | Session may relate to Event |
| One tracker interval actually contains two activities | split Session with history |
| Two accidental adjacent tracker records were one episode | merge Session with history |
| User corrects start time | same Session identity, corrected timing |
| Walk + English listening simultaneously | overlapping Sessions allowed contextually |
| Deep coding + driving overlap | suspicious conflict, not universal DB prohibition |
| Session ends but report unfinished | Activity remains incomplete |
| Workout Session includes route/heart-rate | associated Measurements/Observations |
| Repeated Tuesday Sessions suggest a pattern | AI may propose Routine; no automatic Routine creation |
| Photo hike produces 10 km evidence | Session/Actual can support fitness Goal without rewriting original intent |

---

## Adversarial cases

### Planned two hours, accidentally leave timer running six hours

The tracker may produce:

```text
Session
18:00 -> 00:00
```

LifeOS should not silently rewrite it.

It may flag:

- anomalous duration;
- long inactivity;
- likely stale timer;
- possible correction suggestion.

User or authorized policy can correct/end/split it with provenance.

### Session starts before planned placement

```text
Schedule
18:00 -> 20:00

Session
17:30 -> 19:10
```

Valid. This is actual deviation, not automatic reschedule.

### Session starts inside one planned placement and ends inside another

This is possible when planned blocks were artificial scheduling partitions.

LifeOS must not force a new Session at the exact Schedule boundary unless execution semantics actually changed.

### Activity completed without tracked Session

Valid.

Actual may be:

```text
completed
```

with no detailed temporal history.

### Session exists but user cannot identify exact work

The Session can remain with coarse context/provenance rather than fabricating an Activity.

Future review may determine how incomplete context is represented and surfaced for review.

### Imported provider record changes after user correction

LifeOS must retain enough source/provenance information to reconcile rather than silently replacing the user-confirmed current truth.

---

## Rejected alternatives

### Alternative A — Planned and actual sessions use one Session entity

Rejected because it collapses Schedule and execution reality.

Consequences would include:

- ambiguous planned-versus-actual fields;
- harder rescheduling history;
- inability to represent spontaneous Sessions cleanly;
- tendency to overwrite planned timestamps with actual timestamps.

### Alternative B — Session is merely start/end fields on Activity

Rejected because:

- one Activity may have many Sessions;
- Session has independent lifecycle/corrections/provenance;
- Sessions may exist without prior Activity;
- Occurrences may have Sessions independently from Activity identity.

### Alternative C — Session equals Occurrence

Rejected because:

- an Occurrence may be skipped with zero Sessions;
- one Occurrence may have multiple Sessions;
- spontaneous Sessions may have no Occurrence;
- Occurrence is expected-instance identity while Session is actual execution.

### Alternative D — Every Event Actual creates a Session

Rejected because it duplicates ordinary Event actual occurrence/attendance semantics.

### Alternative E — Every pause creates a new Session

Rejected because a pause can remain part of one logically continuous execution episode and would create unnecessary fragmentation.

### Alternative F — Any pause over a fixed duration creates a new Session

Rejected because no universal time threshold defines semantic continuity across all domains.

### Alternative G — Forbid overlapping Sessions

Rejected because valid multi-domain/passive overlap exists and overlap validity is context-dependent.

### Alternative H — Put all measurements inside Session metadata JSON

Rejected because recurring/query-heavy observations need typed data/evidence structures rather than arbitrary Session blobs.

---

## Current invariants

1. **Session represents an actual execution episode, not planned placement.**
2. **Session != Schedule.**
3. **Session != Activity.**
4. **Session != Occurrence.**
5. **Session != Routine.**
6. **Session != Event actual occurrence/attendance by default.**
7. **Session != broader Actual / Outcome.**
8. One Activity or Occurrence may relate to zero, one, or many Sessions.
9. Planned Schedule placement and Session do not require one-to-one cardinality.
10. A Session may exist without prior Schedule.
11. A Session may represent spontaneous execution without a pre-existing Activity, provided sufficient context/provenance exists.
12. Pause does not automatically create a new Session.
13. One Session may contain multiple active intervals separated by pauses.
14. Elapsed, active, and paused duration are conceptually distinct.
15. Ending/closing a Session ends that execution episode; later restart normally creates another Session.
16. No universal arbitrary pause-duration threshold defines Session identity.
17. An open/running Session may have unknown end time.
18. Session identity does not depend on start/end timestamps.
19. Corrections to Session timing preserve identity unless the real-world episode itself is being reclassified/split.
20. Split and merge must preserve enough provenance/history to explain the original capture.
21. Ending a Session does not imply Activity/Occurrence completion.
22. Manual, timer/stopwatch, imported, and authorized automatic capture are provenance differences, not different Session semantic types.
23. Timer/Stopwatch are capture/control mechanisms; Session is the persistent execution record.
24. Measurements and Observations may relate to Session without being arbitrary Session metadata.
25. Overlapping Sessions are not globally forbidden; compatibility is context-specific.
26. Analytics must not assume raw sum of Session durations equals unique wall-clock time.
27. A Session may become Evidence for Goals not originally linked to its execution without rewriting historical intent.
28. A broader Actual may aggregate information from multiple Sessions.
29. Actual/Outcome may exist without Session detail.
30. LifeOS Session identity remains independent from provider record identity.
31. Session corrections/import reconciliation require provenance and authority semantics.
32. Repeated Session history does not silently create canonical Routine intent.
33. AI may propose Session correction/linking/reconciliation but cannot silently fabricate execution history.
34. Exact lifecycle enum, pause-interval persistence, parent cardinality, split/merge implementation, and SQL design remain intentionally deferred.

---

## Consequences for adjacent concepts

### Deadline / Window / Temporal Constraint

Session confirms that actual execution may occur:

- inside a valid window;
- outside a preferred window;
- before/after a target placement;
- after a deadline if the work is still permitted but late;
- not at all if the hard validity window expired.

The next temporal review must therefore distinguish temporal allowance/requirement from both Schedule and Session.

### Recurrence

Recurrence produces expected instances/Occurrences, not Sessions.

Observed repeated Sessions may inform analytics or suggestions but do not define recurrence intent.

### Actual

The later Actual review must determine how:

- Session timing;
- execution outcome;
- quantity;
- attendance;
- measurement;
- confirmation;
- correction;
- provenance

combine without creating a universal mega-record.

### Evidence

Session can provide temporal evidence and context for Observations/Measurements, but Goal evaluation should consume valid Evidence rather than treating raw Session existence as universally sufficient.

### Relationship Model

The relationship model must eventually clarify:

- primary execution context;
- Session -> Activity;
- Session -> Occurrence;
- Session -> Event where distinct execution exists;
- Session contribution to multiple Goals;
- spontaneous Session later linked to work structures;
- split/merge lineage.

---

## Questions intentionally deferred

The following are not required to accept Session v0:

- exact Session state enum;
- whether pause intervals are rows, ranges, event stream entries, or another structure;
- exact persisted representation of active versus elapsed duration;
- whether Session has one mandatory primary parent/reference;
- exact Session-to-Activity/Occurrence cardinality constraints;
- exact handling of Session that intentionally realizes multiple Activities;
- exact split/merge lineage schema;
- stale-running-Session recovery policy;
- external-provider conflict policy;
- offline timer synchronization;
- device clock drift handling;
- specialist workout segment/lap representation;
- exact Observation/Measurement schema;
- exact Actual/Outcome relationship;
- exact provenance/confirmation model;
- exact SQL indexes/range constraints;
- aggregation algorithms for overlapping Sessions;
- privacy/access rules for sensitive execution data.

These belong to later temporal, evidence, integration, relationship, and persistence reviews.

---

## Persistence implications without fixing SQL

Future persistence must be able to support:

- stable Session identity;
- open Sessions with unknown end;
- corrected start/end;
- pause/resume history or equivalent active-interval reconstruction;
- source/provenance;
- optional relation to Activity/Occurrence/other context;
- split/merge lineage or audit history;
- provider identity mappings;
- overlap without a universal exclusion constraint;
- efficient time-range querying;
- optional related measurements/observations;
- distinction between deleted false data and corrected real data.

This does **not** yet decide whether Session becomes:

- one table plus child interval table;
- one table plus audit events;
- temporal ranges with derived active intervals;
- an aggregate with related Observation records;
- another normalized relational shape.

Physical design remains downstream of the conceptual Time and Actual/Evidence reviews.

---

## API implications without fixing endpoints

Future APIs should be capable of supporting operations such as:

- start Session;
- pause Session;
- resume Session;
- end Session;
- create retrospective/manual Session;
- correct Session timing;
- split Session;
- merge Sessions;
- attach/detach execution context under valid rules;
- list Sessions by time range/context;
- surface overlapping/conflicting Sessions;
- import/reconcile provider Sessions;
- retrieve Session measurements/observations;
- expose current versus original/corrected values with provenance where appropriate.

These are capability requirements, not accepted endpoint names.

---

## Current conclusion

Session v0 establishes a clean temporal execution primitive:

```text
Schedule
= planned temporal assignment

Session
= actual execution episode

Actual
= broader observed truth / outcome
```

This separation preserves:

- planning history;
- spontaneous execution;
- multi-session Activities and Occurrences;
- pause/resume semantics;
- manual and imported actual time;
- corrections and reconciliation;
- future analytics and estimation learning;
- evidence provenance;
- Event attendance without redundant Session records.

Session is therefore accepted as the current Time-cluster baseline for actual execution slices, while exact lifecycle, persistence, and Actual/Evidence integration remain intentionally deferred.

---

# 2026-08-12 — Participation v0 closure amendment

Participation v0 resolves the previously deferred Event-attendance relationship while preserving Session v0 unchanged in purpose.

Canonical separation:

```text
Session
= bounded actual execution/performed-behavior episode

Actual Participation / Attendance
= actor-scoped involvement in a shared Event/interaction
```

Therefore:

```text
Participation != Session
Event attendance != Session by default
one attendee != one Session
partial attendance intervals != automatic Session splitting
```

A Session still exists when a distinct executable episode is genuinely present, for example hands-on work during a workshop. Attendance alone does not manufacture execution history.

Provider join/leave intervals may support Actual Participation through Provenance/Evidence/reconciliation semantics; they are not automatically Session records or canonical human attendance truth.

The older deferred question about `Session -> Event where distinct execution exists` remains valid; what is now resolved is that ordinary Event Participation/Attendance is a separate relation family rather than a Session subtype.

See:

- `concepts/participation.md`;
- `checkpoints/participation-v0-validation.md`.
