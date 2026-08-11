# Recurrence v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-11  
**Meaning of accepted:** best current decision; reopenable with better evidence  
**Workstream:** Core Domain Model v0 — Time cluster

## Canonical definition

> **A Recurrence is a structured rule that describes how a temporal or generative pattern repeats from an explicit basis over an effective range. When used by a recurring source, it determines the candidate sequence, quota, or anchor relationship from which expected Occurrences are produced; when used by another temporal rule, it may define repeated applicability without changing the parent concept's semantics. Recurrence does not itself represent the recurring behavior/Event, an Occurrence identity, an accepted Schedule, or Actual execution.**

Recurrence answers the question:

> **How does this pattern repeat?**

It does not by itself answer:

- what the recurring thing fundamentally is;
- why it matters;
- which specific instance is being discussed;
- when a specific instance is currently scheduled;
- whether an instance was executed, attended, skipped, cancelled, or completed;
- what Actual occurred;
- what fallback should happen after a miss;
- whether the generated time consumes user capacity;
- what arbitrary external condition should trigger an automation.

Representative examples include:

```text
Recurring Event
Team meeting

Recurrence
Every Monday at 10:00 Europe/Rome
```

```text
Routine
Strength training

Recurrence
Monday / Wednesday / Friday
```

```text
Routine
English practice

Recurrence
3 expected practices per week
```

```text
Routine
Take medication

Recurrence
Every 12 elapsed hours from qualifying anchor
```

```text
Routine
Replace water filter

Recurrence
30 days after actual previous replacement
```

```text
Routine / related execution policy
Back up photographs

Recurrence
One expected backup after each qualifying photography Session
```

The same recurrence capability may be reused by different parent concepts without collapsing their domain semantics.

---

## Why this concept exists

The accepted Time-cluster concepts require a reusable model of repeated temporal/generative structure that remains distinct from both source semantics and individual instance identity.

`Routine v0` requires:

- Routine to remain a recurring behavioral/execution policy rather than a recurrence string;
- recurring behavior to support calendar, interval, completion-relative, and relation-anchored semantics;
- one-off Occurrence changes not to rewrite future Routine policy;
- future structural changes to remain historically explainable.

`Event v0` requires:

- recurring Events to remain Event semantics rather than being forced into Routine;
- individual recurring Event instances to retain identity when moved;
- original expectation, current Schedule, and Actual occurrence to remain distinct.

`Occurrence v0` requires:

- one stable logical instance identity distinct from the source rule;
- future instances to be potentially virtual before materialization;
- moved/skipped/cancelled instances to preserve historical identity;
- occurrence identity not to depend on current start/end;
- historical instances to retain enough source/version context to explain why they existed.

`Schedule v0` requires:

- the accepted temporal assignment of one subject/Occurrence to remain separate from recurrence;
- one-off rescheduling not to mutate the generation rule automatically.

`Temporal Constraint v0` requires:

- repeated temporal admissibility/preferences to be supportable without pretending those repeated windows necessarily generate Occurrences;
- recurrence machinery to be reusable without collapsing Constraint and Recurrence semantics.

Without a Recurrence concept, LifeOS would be forced into weak alternatives such as:

1. embedding recurrence fields directly into Routine/Event/Constraint in incompatible forms;
2. treating every repeated pattern as an iCalendar RRULE even when the semantics are not calendar-set based;
3. deriving Occurrence identity directly from current timestamps;
4. treating completion-relative generation as ordinary calendar recurrence;
5. mutating the recurring source whenever one individual Occurrence changes;
6. implementing separate recurrence engines for Routine, Event, and Constraint;
7. collapsing threshold/state Trigger behavior into temporal recurrence;
8. eagerly materializing indefinite future Occurrences.

Recurrence provides a reusable structured pattern layer while preserving the semantics of the parent concept and the identity/history of individual Occurrences.

---

## Design authority rule — LifeOS semantics first

External standards, products, APIs, and schemas are **benchmark evidence, not design authorities**.

LifeOS must not distort its internal domain model merely to match another platform.

Canonical rule:

> **LifeOS adopts an external pattern when it improves the internal model or provides useful interoperability at negligible conceptual cost. External compatibility is not a kernel invariant.**

The design direction is:

```text
LifeOS semantics
        ↓
strong internal model
        ↓
optional adapters / mappings
        ↓
external providers and standards
```

not:

```text
external provider schema
        ↓
LifeOS kernel must imitate it
```

Consequences:

- RFC 5545/iCalendar is useful evidence for recurrence-set, instance-identity, timezone, and exception problems;
- Google Calendar and Microsoft Graph are useful evidence for mature recurring-series behavior;
- Todoist is useful evidence that completion-relative recurrence is materially different from fixed-date recurrence;
- none of those schemas is automatically the LifeOS persistence model;
- RRULE compatibility is optional interoperability behavior, not a requirement that limits LifeOS semantics;
- if a LifeOS recurrence cannot be represented losslessly by an external provider, an integration adapter may use controlled degradation, extra provider metadata, multiple external objects, partial support, or explicit incompatibility;
- the kernel should not be weakened merely to make external export easier.

Therefore:

> **Lossless mapping to any external recurrence format is not a Recurrence v0 invariant.**

---

## Validation basis

Recurrence v0 was reviewed against:

### Existing LifeOS documentation

- `docs/product/feature-discovery-simulation-2026-08.md`;
- `docs/product/v1-scheduling-flexibility.md`;
- `docs/product/v1-execution-status.md`;
- `docs/product/v1-core-domain-glossary.md`;
- the accepted Routine, Event, Occurrence, Schedule, Session, and Temporal Constraint concepts;
- the validated Intention & Execution cluster.

### Representative LifeOS scenarios

The review included:

- recurring meetings and lessons;
- weekly study routines;
- `3 times per week` flexible behavioral expectations;
- medication every N elapsed hours;
- local-wall-clock routines;
- travel and timezone changes;
- DST gaps/duplicates;
- monthly and yearly edge cases;
- cyclic work/shift patterns;
- completion-relative maintenance;
- post-event follow-up generation;
- recurring hard/preferred scheduling constraints;
- skipped and cancelled expected instances;
- one-off extra execution;
- `this occurrence` changes;
- `this and future` structural changes;
- correction of Actual used as a recurrence anchor;
- virtual future Occurrences and materialization horizons.

### External benchmark evidence

Benchmark evidence included patterns from:

- RFC 5545 / iCalendar recurrence sets and recurrence-instance identity;
- Google Calendar recurring event instances and original-instance identity;
- Microsoft Graph recurrence pattern/range concepts;
- Todoist original-date versus completion-date recurrence behavior.

These sources expose real temporal problems and possible solutions. They do not constrain the LifeOS kernel.

---

## Recurrence versus Routine

A Routine represents recurring behavioral/execution policy.

Recurrence represents only the repeating/generative structure used by that Routine.

```text
Routine
Strength training

Recurrence
Mon / Wed / Fri
```

The Routine may additionally define or relate to:

- behavior semantics;
- bundle/step structure;
- fallback/adaptation policy;
- Goal/Plan relationships;
- recovery or replacement behavior;
- temporary pause/end semantics;
- outcome expectations.

Those concerns do not become part of Recurrence merely because the Routine repeats.

Therefore:

> **Routine != Recurrence.**

The UI may call something a recurring task or recurring routine, but the domain should preserve the behavioral source separately from the recurrence pattern.

---

## Recurrence versus recurring Event

Recurring temporal occurrence does not change Event semantics into Routine semantics.

```text
Event
Team meeting

Recurrence
Every Monday at 10:00
```

remains an Event source/series.

```text
Routine
Weekly review

Recurrence
Every Sunday evening
```

remains a Routine.

The recurrence capability is shared; the parent meaning is not.

Therefore:

> **Recurrence does not determine whether the parent is Routine, Event, or another approved recurring source.**

### EventSeries is not introduced as a kernel primitive yet

External calendar systems often expose a series-master resource, but LifeOS does not currently have evidence that `EventSeries` requires materially distinct kernel identity/lifecycle beyond Event semantics plus recurrence and Occurrence identity.

Current direction:

```text
Event semantics
+
Recurrence
+
Occurrence identity
```

is sufficient conceptually.

If persistence/integration behavior later proves that a series master has materially different invariants, `EventSeries` may be reopened as a specialization. It is not assumed now.

---

## Recurrence versus Occurrence

Recurrence answers:

> how does the pattern repeat?

Occurrence answers:

> which individual expected instance?

Example:

```text
Recurrence
Every Monday at 10:00

Occurrence
Monday 17 August instance
```

A moved Occurrence remains the same Occurrence:

```text
Original expected instance
Mon 10:00

Current Schedule
Tue 15:00
```

The one-off Schedule change does not automatically modify Recurrence.

Therefore:

> **Recurrence != Occurrence.**

Recurrence may be used to derive candidate/future Occurrences, but a materialized Occurrence has its own identity/history.

---

## Recurrence versus Schedule

Recurrence expresses repeated generation/applicability.

Schedule expresses the current accepted temporal assignment of a specific schedulable subject.

```text
Recurrence
Every Monday

Occurrence
Monday instance

Schedule
Monday 18:30-19:30
```

or after a one-off move:

```text
Same Occurrence

Schedule
Tuesday 20:00-21:00
```

The Recurrence remains `every Monday` unless the future rule itself changes.

Therefore:

> **Recurrence != Schedule.**

---

## Recurrence versus Session / Actual

Recurrence produces or governs expected structure.

Session and Actual describe reality.

```text
Recurrence
Every Monday
        ↓
Occurrence
Monday instance
        ↓
Schedule
18:00
        ↓
Session
18:12-19:04
        ↓
Actual / Outcome
```

Actual execution can:

- happen early or late;
- happen partially;
- happen in multiple Sessions;
- not happen;
- happen spontaneously without a preceding recurrence-generated Occurrence.

Those facts do not rewrite Recurrence automatically.

Therefore:

> **Recurrence != Session / Actual.**

---

## Recurrence versus Temporal Constraint

The same temporal pattern shape can have different meanings.

```text
Every Monday
```

may mean:

```text
Recurrence
Generate one expected Occurrence every Monday
```

or:

```text
Temporal Constraint
This Activity may only be scheduled on Mondays
```

Likewise:

```text
Every weekday 17:00-21:00
```

may be a recurring preferred/allowed Constraint without generating any expected Occurrence.

Therefore:

> **Recurrence != Temporal Constraint.**

However, a recurrence-pattern capability may be reused to express repeated applicability of a Temporal Constraint.

Conceptually:

```text
Temporal Constraint
Preferred study window
        ↓
Recurrence pattern
Weekdays 17:00-21:00
```

versus:

```text
Routine
Study practice
        ↓
Recurrence pattern
3 expected practices per week
        ↓
Occurrences
```

The pattern machinery may be shared; the parent semantics determine whether instances are generated.

---

## Recurrence versus Trigger / automation

Recurrence is not a universal event-condition-action engine.

Valid temporal/generative recurrence examples include:

```text
Every Monday
```

```text
Every 12 elapsed hours
```

```text
30 days after previous qualifying completion
```

```text
One expected backup after each qualifying photography Session
```

But these are different from arbitrary conditions such as:

```text
When account balance < €500
```

```text
When temperature > 30°C
```

```text
When device battery < 20%
```

```text
Every 10,000 km of vehicle usage
```

Those are primarily threshold/state/usage Trigger semantics, even if they eventually generate work.

Therefore:

> **Recurrence != generic IF/THEN automation.**

Recurrence may consume a well-defined temporal or qualifying-anchor stream, but it must not become an arbitrary workflow engine.

---

## Recurrence is not necessarily a timestamp generator

A central LifeOS decision is:

> **A Recurrence may generate logical expected instances without assigning exact datetimes.**

Example:

```text
Routine
English practice

Recurrence
3 times per week
```

The Recurrence can establish:

```text
Week 34
Occurrence 1
Occurrence 2
Occurrence 3
```

without deciding:

```text
Mon 18:00
Wed 18:00
Sat 10:00
```

Those placements belong to Schedule.

This is necessary for flexible scheduling and prevents false precision.

It also means Recurrence is broader than an RRULE-like function returning timestamps.

---

## Recurrence semantic families

Recurrence v0 does not fix a physical enum or DSL, but it requires several materially distinct semantic families.

At minimum:

1. calendar / wall-clock recurrence;
2. elapsed-interval recurrence;
3. quota-per-period recurrence;
4. completion-relative recurrence;
5. anchor-stream-relative recurrence;
6. cyclic positional recurrence.

These families share a concept of repeated generation/applicability but do not necessarily share one expansion algorithm.

### Why not force one algorithm

The following cannot safely be treated as syntax variations of the same timestamp recurrence:

```text
Every Monday at 18:00
```

```text
Every 12 real hours
```

```text
3 times per week
```

```text
30 days after actual completion
```

```text
After each qualifying photography Session
```

They differ in:

- anchor source;
- whether exact candidate times exist in advance;
- whether future instances depend on Actual;
- whether missed instances alter future generation;
- how DST/travel applies;
- whether multiple slots exist within one period without dates;
- whether the chain can be expanded independently into the far future.

A single algorithm can be an implementation abstraction later only if it preserves those semantics explicitly.

---

## Calendar / wall-clock recurrence

Examples:

```text
Every Monday at 18:00 Europe/Rome
```

```text
Every 15th day of the month
```

```text
Last Friday of each month
```

```text
Every 29 February
```

Calendar recurrence is based on calendar positions and wall-clock semantics, not merely elapsed seconds.

### Wall-clock semantics are not elapsed-duration semantics

```text
Every day at 08:00 Europe/Rome
```

means the recurring expectation stays aligned to 08:00 in the named zone.

When DST changes, the corresponding UTC instant may change.

This differs from:

```text
Every 24 elapsed hours
```

which preserves elapsed duration from the anchor.

Therefore:

> **`every day at 08:00` != `every 24 elapsed hours`.**

Likewise:

> **calendar-day recurrence must not be implemented universally as fixed-second arithmetic.**

---

## Floating/user-local versus named-zone versus absolute semantics

Wall-clock recurrence may require different location/time-zone semantics.

### Named-zone wall clock

```text
Team meeting
10:00 Europe/Rome every Monday
```

The semantic anchor remains the Rome wall clock.

Travel does not move the meeting to 10:00 in the user's current location.

### Floating/user-local wall clock

```text
Breakfast
08:00 local wherever I am
```

The expectation follows the user's applicable local zone/policy.

### Absolute/UTC-based pattern

Some repeated technical processes may be anchored to absolute instants rather than local wall clock.

These three semantics must remain distinguishable.

LifeOS must not normalize them into one stored UTC timestamp sequence and then lose the original intention.

---

## Elapsed-interval recurrence

Example:

```text
Medication
Every 12 elapsed hours from qualifying anchor
```

The next expectation is determined by elapsed duration from the anchor, not by a repeated local clock position.

Conceptually:

```text
anchor instant
      ↓ +12h elapsed
Occurrence 1
      ↓ +12h elapsed
Occurrence 2
```

Depending on the rule, the next anchor may be:

- the original fixed anchor plus N intervals;
- the previous generated expected instant;
- a qualifying Actual fact;
- another reviewed anchor source.

Those variants must not be silently conflated.

---

## Quota-per-period recurrence

Example:

```text
Train 3 times per week
```

The rule expresses a number of expected instances within a period rather than exact named positions.

Conceptually:

```text
Period: week 34
Expected quota: 3

Occurrence A
Occurrence B
Occurrence C
```

Exact placement can be deferred to Schedule and optimized using:

- Temporal Constraints;
- spacing/recovery rules;
- Availability/Capacity;
- priorities;
- user preferences.

Quota recurrence must not be rewritten into arbitrary weekdays merely to fit a calendar recurrence representation.

### Quota count is not Goal progress

```text
Recurrence
3 expected Occurrences per week
```

is distinct from:

```text
Goal criterion
Complete 3 workouts per week
```

Recurrence describes expectations generated.
Goal evaluation describes what success means.

A generated Occurrence may be skipped, missed, replaced, or completed; Goal evaluation handles the evidence/outcome semantics later.

---

## Completion-relative recurrence

Example:

```text
Replace water filter
30 days after actual previous replacement
```

This is not equivalent to:

```text
Every 30 calendar days from 1 January
```

A completion-relative recurrence identifies a qualifying Actual/fact as the anchor for the next expected instance.

Conceptually:

```text
Occurrence #12
      ↓
Actual replacement completed 11 Aug
      ↓ +30 days
Occurrence #13 expected 10 Sep
```

### Sequential generation

Completion-relative recurrence often forms a sequential chain.

If Occurrence #12 has not yet been completed, LifeOS should not necessarily generate independent Occurrences #13, #14, #15 every 30 days.

Instead:

```text
Occurrence #12
unresolved / overdue

no qualifying completion anchor yet
```

The next expected instance may remain undefined until the rule receives the qualifying Actual anchor.

Therefore:

> **A completion-relative chain must not silently behave like a fixed calendar series.**

### Qualifying anchor must be explicit

The rule must eventually identify what fact qualifies as the anchor, such as:

- actual completion time;
- actual replacement observation;
- confirmed service event;
- another reviewed Actual/Outcome fact.

`scheduled end` is not automatically a substitute for Actual completion.

---

## Anchor-stream-relative recurrence

Example:

```text
After each photography Session
create/expect one backup instance
```

Conceptually:

```text
qualifying photography Session A
        ↓ relation/offset
Backup Occurrence A

qualifying photography Session B
        ↓ relation/offset
Backup Occurrence B
```

This is a repeated mapping from a defined stream of qualifying anchors.

It is broader than simple completion-relative chaining because each qualifying anchor may independently generate a related Occurrence.

### Boundary with Trigger

Anchor-stream recurrence remains appropriate when:

- the anchor type/source is defined;
- the mapping is structurally repetitive;
- generation semantics are temporal/relational and bounded;
- it is not evaluating arbitrary world conditions.

Trigger/automation remains appropriate when:

- arbitrary state thresholds are detected;
- external conditions drive behavior;
- complex IF/THEN logic is required;
- non-temporal usage/environment conditions dominate.

This boundary may be revisited during Trigger review.

---

## Cyclic positional recurrence

Some schedules repeat as cycles rather than ordinary weekday rules.

Examples:

```text
2 days on / 2 days off
```

```text
4-night shift cycle followed by 3 rest days
```

```text
A / B / C rotation every 3 weeks
```

The cycle has:

- an anchor phase;
- ordered positions;
- a repeat length;
- optional per-position semantics.

LifeOS should preserve cycle position semantics instead of expanding them into an arbitrary long list of calendar dates as the only canonical representation.

---

## Pattern anchor versus effective range

A recurrence pattern requires an explicit basis/anchor where the semantics need one.

Example:

```text
Every 2 weeks
```

is incomplete without knowing the phase of the pattern.

Possible model meaning:

```text
anchor
5 August

pattern
Every 2 weeks
```

Separately, the rule may only be effective from a later point:

```text
effective from
1 September
```

The pattern anchor and the effective range are therefore distinct concepts.

Canonical rule:

> **Do not silently use `created_at` as the recurrence anchor unless creation time is explicitly the intended anchor.**

---

## Recurrence effective range

Recurrence must support conceptually at least:

```text
open-ended
```

```text
until a temporal boundary
```

```text
for N expected Occurrences
```

A physical schema may later use a typed range representation, but the semantics are distinct from the pattern itself.

Conceptually:

```text
Recurrence
pattern: every Monday
range: 10 expected occurrences
```

versus:

```text
Recurrence
pattern: every Monday
range: until 31 December
```

### Occurrence count does not mean successful completion count

If the recurrence range is:

```text
10 expected Occurrences
```

and Occurrence #4 is skipped, it is still one of the ten expectations generated.

If the desired outcome is:

```text
continue until 10 successful workouts are completed
```

that belongs primarily to Goal/Plan completion/evaluation semantics, potentially with a Routine that remains active until the criterion is reached.

Recurrence-count must not be overloaded with Goal success semantics.

---

## One-off Occurrence exception versus structural Recurrence change

This distinction is foundational.

### This Occurrence only

```text
Recurrence
Every Wednesday 18:00

Occurrence #27
Move this one to Thursday 20:00
```

This normally changes the Occurrence Schedule/exception only.

Recurrence remains unchanged.

### Selected Occurrences

Changing several explicitly selected Occurrences does not automatically create a new Recurrence rule.

They may each be occurrence-specific exceptions.

### This and future

```text
Current recurrence
Wednesday 18:00

From occurrence #27 onward
Wednesday 20:00
```

This is a structural future-rule change.

Conceptually:

```text
Recurrence revision v1
Wednesday 18:00

boundary
Occurrence #27 / effective point

Recurrence revision v2
Wednesday 20:00
```

Historical Occurrences remain explainable under v1.
Future Occurrences are governed by v2.

Therefore:

> **Structural recurrence change is an effective revision, not retroactive mutation.**

Exact version persistence remains deferred to the Version/History model.

---

## Skip versus structural exclusion

These are not the same.

### Generated then skipped

```text
Recurrence
Every Monday

Occurrence
Monday 17 Aug

Resolution
Skipped
```

The Occurrence existed as an expectation.

It remains relevant to history/adherence.

### Excluded by governing rule before generation

```text
Pattern
Every weekday

Structural exclusion
Public holidays
```

If a holiday is excluded by the governing rule before the candidate instance becomes an expected Occurrence, LifeOS may legitimately produce no Occurrence for that day.

Canonical distinction:

> **Not generated by rule != generated and later skipped/cancelled.**

This distinction matters for history, analytics, adherence, and explanation.

---

## Cancelled Occurrence versus Recurrence end

Cancelling one Occurrence does not end the Recurrence.

Ending the source/Recurrence for the future does not retroactively cancel historical Occurrences.

Example:

```text
Recurring Event
Weekly meeting

Occurrence 17 Aug
cancelled

future recurrence
continues
```

versus:

```text
Recurring Event
Weekly meeting

series/source ended from 1 Sep
```

The lifecycle semantics are distinct.

---

## Extra execution / extra Occurrence

Example:

```text
Routine
Gym Mon/Wed/Fri
```

The user also trains on Sunday once.

LifeOS should not automatically mutate the Recurrence into:

```text
Mon/Wed/Fri/Sun
```

Possible semantics include:

- explicit extra Occurrence related to the Routine;
- independent Activity/Session;
- one-off replacement/support behavior.

Only an explicit structural future change such as:

```text
From now on also Sunday
```

changes Recurrence.

Observed extra behavior does not rewrite historical/future intention automatically.

---

## Pause and end belong to the source lifecycle

A source may be paused or ended while retaining its recurrence definition/history.

Example:

```text
Routine
Gym Mon/Wed/Fri

Temporary pause
1-15 September
```

This is not necessarily a mutation of the core recurrence expression.

Likewise, ending a Routine is a source lifecycle action.

Exact lifecycle/pause modeling remains deferred.

Recurrence answers how repetition works while effective.
It does not own every source lifecycle decision.

---

## Future Occurrences may remain virtual

Recurrence must not require eager indefinite materialization.

Wrong default:

```text
Daily Routine created
→ create 20 years of future Occurrence rows
```

Preferred conceptual direction:

```text
Recurrence
      ↓
virtual future candidate Occurrences
      ↓
operational horizon / interaction
      ↓
materialize when needed
```

Materialization may become necessary when an instance acquires specific history such as:

- accepted Schedule;
- one-off exception;
- user edit/note;
- notification state whose history matters;
- provider instance identity;
- external sync state;
- skip/cancel disposition;
- Session/Actual;
- Confirmation/Evidence;
- another persisted relation.

The exact horizon and persistence algorithm are implementation decisions deferred beyond Recurrence v0.

---

## Recurrence revision and virtual future instances

A structural future Recurrence revision may invalidate previously derived virtual candidates.

Purely virtual future instances may be regenerated according to the new effective rule.

However, a future Occurrence that already has instance-specific history must not silently disappear as though it never existed.

Example:

```text
Recurrence v1
Mon/Wed/Fri

Future Occurrence
Fri 21 Aug
already has accepted Schedule and provider ID

Recurrence changes to Tue/Thu
```

LifeOS must reconcile the existing materialized instance explicitly rather than merely deleting history because the new recurrence expansion no longer contains Friday.

Exact reconciliation policy is deferred, but silent disappearance is not acceptable.

---

## Historical Occurrences retain generation context

Historical Occurrences must remain explainable under the rule/version that generated them.

Example:

```text
Recurrence v1
Mon/Wed/Fri

Occurrence #20
Occurrence #21
Occurrence #22
```

Later:

```text
Recurrence v2
Tue/Thu
```

The past must not be re-expanded using v2 and made to look as though Monday/Wednesday/Friday were never expected.

Therefore:

> **Historical generation context is part of the audit/history requirement.**

The exact version storage mechanism remains deferred.

---

## DST and local-time resolution

LifeOS must preserve the user's recurrence semantics through daylight-saving transitions rather than relying on one hidden universal policy.

### Nonexistent local time

Example:

```text
Medication Routine
02:30 local
```

On a DST spring-forward day, 02:30 may not exist in the relevant zone.

Possible intended policies include:

- skip that instance;
- shift to first valid time after the gap;
- shift by the DST delta;
- preserve elapsed duration instead;
- use a specialist medication policy;
- ask/require explicit rule choice.

LifeOS must not assume one policy fits every domain.

### Ambiguous/repeated local time

On a DST fall-back day, a local wall-clock time may map to two possible instants.

LifeOS must preserve enough zone/resolution semantics to choose/reconstruct the intended instant without creating duplicate Occurrences merely because the clock label appears twice.

### No universal UTC-only recurrence truth

A normalized UTC instant may be useful operationally, but it must not replace the canonical semantic distinction among:

- floating/user-local wall clock;
- named-zone wall clock;
- absolute instant;
- elapsed-duration recurrence.

---

## Travel behavior

Travel exposes whether the recurrence is attached to a fixed timezone or to the user's local context.

Examples:

```text
Breakfast
08:00 local wherever I am
```

may follow the user's current locality.

```text
Team meeting
10:00 Europe/Rome
```

remains tied to Rome time.

```text
Medication
Every 12 elapsed hours
```

may remain tied to elapsed time independent of local wall clock.

These are distinct policies.

LifeOS must not infer travel behavior merely from the current resolved timestamp.

---

## Invalid calendar dates

Calendar recurrence must distinguish different user intentions instead of silently normalizing invalid dates.

### Exact ordinal day

```text
Every 31st day of the month
```

may mean only months that actually have a 31st.

### Last valid day

```text
Last day of every month
```

means 28/29/30/31 depending on the month.

These are not equivalent.

Likewise:

```text
Every 29 February
```

must not automatically become 28 February in non-leap years unless that fallback is explicitly part of the rule.

Possible rule/policy options may include:

- skip invalid calendar positions;
- clamp to last valid day;
- move to next valid day;
- another domain-specific choice.

LifeOS must preserve enough semantics to distinguish the requested pattern from fallback behavior.

---

## nth-weekday and positional calendar patterns

Patterns such as:

```text
second Tuesday of every month
```

```text
last Friday of every month
```

```text
first working day after the 15th
```

may require positional/calendar expressions more expressive than simple fixed intervals.

The first two are ordinary calendar recurrence patterns.
The last may require holiday/calendar context and could cross into constraint/business-calendar semantics depending on implementation.

Recurrence v0 requires expressive room for positional patterns but does not fix a DSL now.

---

## Natural-language recurrence is input, not canonical truth

The user may say:

```text
Every week
```

but that phrase can mean materially different behaviors:

- every Monday;
- every 7 elapsed days;
- one expected occurrence during each calendar week;
- 7 days after completion;
- every week relative to another anchor.

Therefore:

> **Natural-language recurrence text is not the canonical normalized recurrence model.**

The original text may be preserved as user input/provenance, but LifeOS should normalize the material semantics.

When ambiguity changes behavior materially, the product/AI should resolve it from context or request confirmation rather than silently choosing a potentially wrong recurrence family.

---

## Completion-relative anchor correction

This is a critical history edge case.

Example:

```text
Actual filter replacement recorded
20 Jan

Recurrence
+30 days

Generated expectation
19 Feb
```

Later the user corrects the Actual:

```text
Actual replacement was 18 Jan
```

The recomputed expectation becomes:

```text
17 Feb
```

### If the future Occurrence was still purely virtual

The future candidate may simply be regenerated from the corrected anchor.

### If the future Occurrence was materialized

The same Occurrence identity should normally remain and preserve history such as:

```text
original generated expectation
19 Feb

current recomputed expectation
17 Feb

reason
correction of anchor Actual
```

### If the downstream Occurrence already has Actual/history

LifeOS must not delete/recreate that history merely because the anchor changed retroactively.

The correction should update current derived interpretation while preserving audit/provenance.

Exact mechanics require the later Actual/Provenance and Version models.

---

## Completion-relative miss behavior

A missed fixed calendar recurrence and a missing completion-relative anchor behave differently.

### Fixed independent cadence

```text
Every Monday
```

Monday may be missed, while the next Monday still exists independently.

### Completion-relative chain

```text
30 days after actual completion
```

If the current expected action has not completed, the next anchor may not exist yet.

Therefore future generation may remain blocked/undefined rather than creating independent 30-day slots.

The recurrence family must make this dependency explicit.

---

## Recurrence does not define fallback after missed execution

When an expected Occurrence is missed, the system may need to:

- skip;
- postpone;
- replace;
- compress future work;
- replan the day/week;
- change Routine strategy.

Those are Routine/Plan/fallback/replanning semantics.

Recurrence describes repeated expectation generation.
It does not decide what operational recovery behavior should occur after divergence.

Therefore:

> **Miss-handling/fallback policy != Recurrence.**

---

## Recurrence does not imply busy/capacity reservation

A recurring pattern that produces an expected Event/Occurrence does not automatically reserve calendar capacity.

```text
Recurring webinar
Every Friday 17:00
```

may be visible but non-blocking.

```text
Recurring focus block
Every Friday 17:00
```

may reserve capacity.

Availability/Capacity semantics remain separate.

---

## Recurring Temporal Constraints

Temporal Constraints may need repeated applicability.

Example:

```text
Constraint
Prefer study between 17:00 and 21:00

Applies
Weekdays
```

This can conceptually reuse recurrence-pattern machinery without generating expected execution Occurrences.

Another example:

```text
Constraint
No meetings 12:30-14:00

Applies
Monday-Friday
```

Again, the recurring pattern repeats the rule's applicability.

Therefore the recurrence engine/capability should not assume every expanded match becomes a domain Occurrence.

The parent semantic determines the effect.

---

## Recurrence and source scoping

A Recurrence may belong to or govern a source such as:

- Routine;
- recurring Event semantics;
- a repeated Temporal Constraint;
- another future reviewed temporal/generative source.

LifeOS should avoid copying the same recurrence definition onto every generated child.

Occurrence-specific exceptions belong to the Occurrence/scheduling/history layer unless they change the future source rule.

The exact parent ownership/cardinality and persistence model remain deferred.

---

## Recurrence identity and revision identity

Recurrence v0 does not yet fix whether Recurrence itself is always an entity, value object, versioned component, or a combination.

However, several semantic requirements are clear:

- the recurring source has persistent identity;
- material structural recurrence changes must be historically reconstructible;
- historical Occurrences need the effective rule context that generated them;
- external provider rule IDs/series IDs must not become LifeOS identity;
- a recurrence expression may be replaced/revised without recreating the parent source automatically.

The physical versioning boundary will be reviewed later.

---

## External provider mapping

External integrations may use provider-specific concepts such as:

- recurrence strings;
- series masters;
- original-start identifiers;
- instance IDs;
- recurrence exceptions;
- provider timezone resolution rules.

LifeOS should preserve mapping metadata necessary for sync while keeping provider identity separate from LifeOS identity.

Mapping may be:

```text
lossless
```

```text
lossy but acceptable
```

```text
provider-expanded
```

```text
LifeOS-expanded
```

```text
unsupported without user-visible degradation
```

depending on the recurrence family.

No external provider's limitations define the LifeOS kernel.

---

## Representative scenario matrix

| Scenario | LifeOS interpretation |
|---|---|
| Team meeting every Monday 10 | recurring Event semantics + calendar Recurrence |
| Gym Mon/Wed/Fri | Routine + calendar Recurrence |
| Workout 3x/week | Routine + quota-per-period Recurrence |
| Medication every 12 real hours | elapsed-interval Recurrence |
| Breakfast 08:00 local while travelling | floating/user-local wall-clock Recurrence |
| Meeting 10:00 Europe/Rome | named-zone wall-clock Recurrence |
| Filter 30 days after replacement | completion-relative Recurrence |
| Backup after every photography Session | anchor-stream-relative Recurrence / Trigger boundary |
| Maintenance every 10,000 km | primarily Trigger/usage rule, not temporal Recurrence |
| Only Mondays | Temporal Constraint unless it generates expected Occurrences |
| Preferred study window every weekday | recurring applicability of Temporal Constraint |
| Monday Occurrence moved Tuesday | same Occurrence + Schedule exception |
| Skip one Monday | Occurrence skipped; Recurrence unchanged |
| Cancel one recurring Event instance | Occurrence cancelled; Recurrence continues |
| From now Mon/Wed/Fri -> Tue/Thu | effective Recurrence/source revision |
| Extra workout Sunday once | extra Occurrence or independent Activity; no automatic Recurrence mutation |
| 10 expected Occurrences | Recurrence range/count |
| Complete 10 successful workouts | Goal/Plan criterion, not Recurrence count |
| Fixed weekly Occurrence missed | later weekly Occurrences can continue |
| Completion-relative Occurrence unresolved | next chain anchor may not exist yet |
| Every 31st | exact ordinal-day semantics with explicit invalid-date policy |
| Last day monthly | separate positional semantics |
| Every Feb 29 | explicit leap-year behavior |
| Nonexistent DST local time | explicit/derived resolution policy required |
| Ambiguous repeated local time | zone/resolution semantics decide one expected instance |
| Correct anchor Actual retroactively | recompute future expectation without rewriting history |
| Recurrence revision with pure virtual future | regenerate candidates |
| Recurrence revision with materialized future | reconcile existing instance-specific history |
| No meetings every weekday at lunch | recurring Temporal Constraint, not execution Recurrence |
| Two days on / two days off | cyclic positional Recurrence |

The matrix does not currently require reopening Occurrence, Schedule, Session, Temporal Constraint, Routine, or Event.

---

## Adversarial cases

### Case 1 — flexible quota with recovery

```text
Routine
Strength training

Recurrence
3 times per week

Temporal Constraint
minimum 48h between qualifying Sessions
```

The Recurrence creates three logical weekly expectations.
The Constraint and Scheduler decide valid placements.
The Recurrence does not invent Mon/Wed/Fri.

### Case 2 — recurring Event moved once

```text
Event
Weekly meeting

Recurrence
Mon 10:00

Occurrence
Mon 17 Aug

Schedule exception
Tue 15:00
```

Same Occurrence, Recurrence unchanged.

### Case 3 — recurring Event moves permanently

```text
From 1 Sep
meeting moves from Mon 10:00 to Tue 11:00
```

Future source/Recurrence revision, past remains under old rule.

### Case 4 — completion-relative maintenance

```text
Actual replacement
11 Aug

next expected
10 Sep
```

If 10 Sep is missed, a second independent 10 Oct instance is not automatically generated unless the rule explicitly says fixed cadence rather than completion-relative chain.

### Case 5 — imported correction

Provider imports replacement as 11 Aug.
User corrects it to 9 Aug.
A materialized future expectation moves earlier, preserving the reason/history.

### Case 6 — travel

```text
Routine A
Breakfast 08:00 local

Routine B
Remote team sync 10:00 Europe/Rome

Routine C
Medication every 12 elapsed hours
```

Travelling from Rome to New York affects each differently.

### Case 7 — DST gap

A local 02:30 recurrence reaches a day with no 02:30.
LifeOS uses explicit/domain policy rather than silently applying one universal calendar-library behavior.

### Case 8 — repeated clock hour

A wall-clock time appears twice during DST fallback.
The recurrence should not automatically generate two Occurrences merely because the label repeats.

### Case 9 — historical structural change

A Routine used Mon/Wed/Fri for six months, then switches to Tue/Thu.
Historical adherence must still be evaluated against the old expected pattern.

### Case 10 — extra unplanned behavior

User trains Sunday once.
Actual/Evidence can count toward Goals without changing the Routine's recurrence intent.

---

## Invariants

1. **Recurrence != Routine.**
2. **Recurrence != recurring Event semantics.**
3. **Recurrence != Occurrence.**
4. **Recurrence != Schedule.**
5. **Recurrence != Session / Actual.**
6. **Recurrence != Temporal Constraint**, even though recurrence-pattern machinery may repeat Constraint applicability.
7. **Recurrence != Trigger / generic IF-THEN automation.**
8. Recurrence describes a structured repeated pattern from an explicit basis/anchor over an effective range where applicable.
9. A recurring source's semantic identity remains separate from its Recurrence expression.
10. A Recurrence may generate logical expected instances without exact timestamps.
11. Quota-per-period recurrence must not be forced into arbitrary fixed weekdays.
12. Calendar/wall-clock recurrence and elapsed-duration recurrence are materially distinct.
13. `Every day at 08:00` is not automatically equivalent to `every 24 elapsed hours`.
14. Floating/user-local, named-zone wall-clock, and absolute/elapsed semantics must remain distinguishable.
15. The recurrence pattern anchor must not be silently inferred from `created_at` when creation time is not the intended anchor.
16. Pattern anchor and effective range/start are distinct semantics.
17. Recurrence range may be open-ended, time-bounded, or count-limited by expected Occurrences.
18. Recurrence count measures expected instances, not successful completions.
19. `Complete N times` normally belongs to Goal/Plan evaluation rather than Recurrence count.
20. Completion-relative recurrence must explicitly depend on a qualifying anchor fact/Actual.
21. Completion-relative chaining must not silently behave as fixed independent calendar recurrence.
22. Anchor-stream-relative recurrence is a defined repeated mapping from qualifying anchors, not arbitrary condition detection.
23. Usage/threshold/state conditions are not forced into temporal Recurrence.
24. Rescheduling one Occurrence does not automatically change Recurrence.
25. A one-off Occurrence edit belongs to Occurrence/Schedule unless the future generation rule actually changes.
26. Selected occurrence-specific edits do not automatically create a new Recurrence revision.
27. Structural `this and future` changes require effective future Recurrence/source revision rather than retroactive mutation.
28. Historical Occurrences retain enough rule/version context to explain how they were generated.
29. Skipping/cancelling an already expected Occurrence does not erase its historical expectation.
30. Structural exclusion before generation is distinct from a generated Occurrence later skipped/cancelled.
31. One-off extra execution does not automatically mutate Recurrence.
32. Source pause/end lifecycle remains distinct from the recurrence expression itself.
33. Future Occurrences may remain virtual and need not be eagerly materialized indefinitely.
34. Purely virtual future candidates may be regenerated after a future structural revision.
35. Future Occurrences with instance-specific history must not silently disappear when the source rule changes.
36. Corrections to an anchor Actual may recompute future expectations but must preserve materialized history/provenance.
37. A downstream Occurrence that already has Actual/history must not be deleted/recreated merely because an upstream anchor was corrected.
38. Recurrence does not define fallback/replanning behavior after missed execution.
39. Recurrence does not imply capacity/busy reservation.
40. Recurring Temporal Constraints may reuse recurrence-pattern machinery without becoming occurrence-generating sources.
41. DST/nonexistent/ambiguous local-time behavior must preserve explicit/domain recurrence semantics rather than rely on one universal hidden policy.
42. Invalid-date behavior must distinguish exact ordinal patterns from fallback semantics such as last-day-of-month.
43. Leap-day behavior must not be silently rewritten into another date unless the rule/policy explicitly says so.
44. Natural-language recurrence text is input/provenance, not the canonical normalized model.
45. Materially ambiguous recurrence language should be resolved explicitly rather than silently choosing a different recurrence family.
46. External provider recurrence IDs/rules do not become LifeOS identity.
47. External standards/products are benchmark evidence, not design authorities.
48. Lossless mapping to RFC 5545/RRULE, Google Calendar, Microsoft Graph, Todoist, or any other provider is not a kernel invariant.
49. Integration adapters absorb provider-specific mapping/degradation when doing so is preferable to weakening LifeOS semantics.
50. Exact Recurrence entity/value-object split, DSL, SQL schema, resolver algorithms, materialization horizon, and version-storage mechanics remain deliberately deferred.

---

## Alternatives considered and rejected

### Alternative A — store an RRULE string as the universal recurrence model

Rejected because:

- LifeOS must support quota-per-period patterns;
- completion-relative recurrence depends on Actual;
- anchor-stream recurrence may depend on qualifying anchor streams;
- LifeOS-specific travel/DST policies may exceed provider semantics;
- a provider format should not dictate the kernel;
- opaque strings are weak for validation/querying/reasoning.

RRULE may remain an integration representation or one compatible expression form.

### Alternative B — recurrence lives only inside Routine

Rejected because recurring Event series and repeated Temporal Constraints also need recurrence-pattern semantics.

### Alternative C — recurring Event becomes Routine

Rejected because repeated Event occurrence and recurring behavioral policy have different domain meaning.

### Alternative D — every recurring instance is just a timestamp

Rejected because:

- flexible quota patterns may have no exact timestamp yet;
- Occurrence identity must survive rescheduling;
- completion-relative future may not exist before Actual anchor;
- historical instance identity cannot depend on current placement.

### Alternative E — every missed occurrence shifts the series

Rejected because fixed independent cadence and completion-relative chains have different semantics.

### Alternative F — store all future occurrences eagerly

Rejected because open-ended recurrence is unbounded and most future instances need no persistent row until operational/history relevance exists.

### Alternative G — one generic condition engine handles recurrence and triggers

Rejected because temporal repetition and arbitrary state/threshold automation have different semantics, safety boundaries, and query needs.

### Alternative H — external calendar compatibility defines the domain model

Rejected. Compatibility is useful only when it does not weaken LifeOS semantics.

---

## Questions intentionally deferred

Recurrence v0 deliberately does not yet fix:

- exact physical `Recurrence` entity/value-object boundary;
- recurrence DSL / typed model / AST;
- SQL tables and indexes;
- range/anchor persistence representation;
- materialization horizon algorithm;
- provider-sync expansion ownership;
- exact Event-series persistence parent;
- exact effective-version storage;
- full calendar-system abstraction beyond current Gregorian-oriented product assumptions;
- exact DST gap/ambiguity resolution policy types;
- travel/location source precedence;
- exact public-holiday/business-calendar integration;
- exact occurrence-exception persistence representation;
- exact reconciliation behavior for already materialized future Occurrences after structural revisions;
- exact Trigger versus anchor-stream boundary for non-temporal external sources;
- exact source pause/end lifecycle representation;
- exact Actual/Outcome/Confirmation rules that qualify completion-relative anchors;
- exact notification/reminder behavior for recurring instances;
- performance strategy for recurrence expansion at scale.

These are deferred because the current semantic boundaries are sufficient to continue the Time-cluster review without prematurely fixing persistence.

---

## Persistence and API implications — non-binding direction

Recurrence v0 does imply several future requirements even though no SQL design is accepted yet.

A future persistence/API model must be able to represent or derive:

- parent/source identity separately from recurrence expression;
- recurrence family/type semantics;
- anchor/basis;
- effective range;
- timezone/wall-clock/elapsed semantics;
- quota/cycle parameters where applicable;
- qualifying Actual/anchor relationships for relative recurrence;
- effective revisions;
- occurrence exceptions separately from source rules;
- lazy future expansion;
- provider mappings separately from LifeOS identity;
- enough historical context to explain generated Occurrences.

The physical model should avoid:

- opaque unvalidated recurrence text as the only canonical field;
- one provider-specific RRULE column as universal truth;
- deriving Occurrence identity solely from generated datetime;
- storing all possible future occurrences indefinitely;
- arbitrary JSON as the primary structure for every recurrence family.

Exact mapping belongs to the later logical/physical data-model phase.

---

## Conceptual model after Recurrence v0

```text
Recurring source semantics
Routine / recurring Event / compatible future source
                │
                ↓
          Recurrence
   how the pattern repeats
                │
                ↓
          Occurrence
   which expected instance
                │
       ┌────────┴────────┐
       ↓                 ↓
Temporal Constraint   Schedule
 allowed/preferred    accepted placement
       │                 │
       └────────┬────────┘
                ↓
        Session / Event Actual
                ↓
        Outcome / Evidence
```

For repeated constraints:

```text
Temporal Constraint
        │
        ↓
Recurrence pattern
repeated applicability

(no execution Occurrence is required merely because the constraint repeats)
```

This model keeps the Time cluster composable without collapsing identity, planning, expectation, or reality.

---

## Current accepted conclusion

Recurrence v0 is accepted as the current LifeOS baseline with these central decisions:

> **Recurrence is a structured repeating-pattern capability, not a Routine, RRULE string, Schedule, Occurrence, or generic automation engine.**

and:

> **Recurrence may generate logical expected instances rather than exact timestamps.**

and:

> **LifeOS semantics come first. External recurrence standards and products provide evidence and optional interoperability targets, but they do not constrain the kernel when doing so would weaken the model.**

This allows one coherent temporal architecture to support:

```text
Mon/Wed/Fri
3x/week
every 12 elapsed hours
30 days after completion
after each qualifying Session
cyclic rotations
recurring temporal constraints
```

while preserving the already accepted distinctions among Routine, Event, Occurrence, Temporal Constraint, Schedule, Session, Actual, and future Trigger semantics.