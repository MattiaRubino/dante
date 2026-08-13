# Occurrence v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-11  
**Meaning of accepted:** best current decision; reopenable with better evidence  
**Workstream:** Core Domain Model v0 — Time cluster

## Canonical definition

> **An Occurrence is the stable logical identity of one expected instance produced by a recurring or generative source. It identifies which instance is being referred to even when its schedule, disposition, execution, or surrounding policy later changes. An Occurrence is not the source rule, the concrete Activity/Event semantics, the current Schedule, a Session, or what actually happened.**

Occurrence exists to answer a precise temporal-identity question:

> **Which individual expected instance are we talking about?**

It is therefore an identity concept before it is a persistence-shape decision.

Representative examples:

- the Wednesday workout expected by a Monday/Wednesday/Friday Routine;
- the 12 August instance of a weekly team-meeting Event series;
- the third expected study execution inside a flexible `3 times per week` Routine;
- the next filter-replacement instance generated relative to the previous completion;
- the backup instance expected after one specific photography session;
- one specific morning-routine instance whose contained actions may execute differently from the surrounding Routine policy.

## Why this concept exists

The validated Intention & Execution cluster already requires a distinction between recurring/generative source semantics and one specific expected instance.

Routine v0 establishes that:

- Routine is a persistent recurring behavior/execution policy;
- individual expected instances must retain identity/history distinct from the Routine policy;
- a one-off change must not silently alter the future Routine;
- skip occurrence, pause Routine, and end Routine are different semantics;
- recurrence may be calendar-, wall-clock-, interval-, completion-, or relation-anchored.

Event v0 establishes that:

- a recurring Event occurrence must retain identity when individually moved;
- original expectation, current accepted schedule, and actual occurrence are separate layers;
- rescheduling is not the same as what actually happened.

Without an Occurrence concept, LifeOS would have to choose among several weak alternatives:

1. overwrite the source Routine/Event every time one instance changes;
2. use the current datetime as the identity of an instance;
3. create a new unrelated Activity/Event whenever an instance is moved;
4. erase skipped/cancelled expectations from history;
5. materialize every future recurrence forever;
6. overload Schedule with both temporal placement and logical series-instance identity.

All of those approaches conflict with the accepted LifeOS history and planned-versus-actual principles.

## Validation basis

Occurrence v0 was reviewed against:

- the validated `Goal + Plan + Activity + Event + Routine + Milestone` cluster;
- the existing scheduling-flexibility rules, especially `this occurrence` versus `all future occurrences` changes;
- the feature-discovery simulation, including cyclic work, medication, study, training, maintenance, travel, recurring household work, disrupted weeks, and flexible routines;
- Event v0 temporal-history requirements;
- Routine v0 recurrence, exception, pause, and revision requirements;
- external recurring-instance patterns from RFC 5545 / iCalendar, Google Calendar, Microsoft Graph, and other mature calendar/task systems.

External systems are benchmark evidence rather than schemas to copy.

The strongest external pattern is that a moved recurring instance remains the same logical instance. RFC 5545 identifies a specific recurrence instance through series identity plus recurrence identity, and the recurrence reference remains anchored to the original instance even when the instance is moved. Google Calendar similarly preserves an `originalStartTime` for a recurring instance. LifeOS keeps the semantic principle while avoiding dependence on an original datetime as its universal internal identity.

## Core identity rule

> **Occurrence identity must not depend on the occurrence's current start or end time.**

Example:

```text
Routine
Gym Monday / Wednesday / Friday

Occurrence
Wednesday instance

Original expectation
Wednesday 18:00

Current accepted schedule
Thursday 19:00

Actual
Thursday 19:12-20:24
```

This remains one Occurrence.

The following transformation is normally wrong:

```text
Delete Wednesday occurrence
Create unrelated Thursday occurrence
```

unless the user or governing semantics genuinely replace one expected instance with another independent one.

Rescheduling changes placement, not automatically identity.

## LifeOS identity is not the original datetime

Although calendar standards often identify recurring instances using an original temporal anchor, LifeOS cannot use `source_id + original_start_datetime` as its universal occurrence identity.

LifeOS must support recurring/generative patterns that may not begin with one exact datetime, for example:

```text
Train 3 times per week
```

```text
Replace the filter 30 days after the previous replacement
```

```text
Back up photographs after each shooting session
```

```text
Perform this maintenance every 10,000 km
```

The last case may ultimately belong partly to Trigger/maintenance semantics rather than ordinary temporal recurrence, but it demonstrates why an identity abstraction must not assume an exact timestamp.

Current direction:

> **Occurrence has LifeOS-stable identity independent from provider identifiers and independent from its current temporal placement.**

The exact physical identifier and persistence representation remain intentionally deferred.

## Occurrence versus source policy / series

An Occurrence is one expected instance produced by a source.

A source may be, depending on future reviewed concepts:

- a Routine;
- a recurring Event series;
- another approved generative temporal structure;
- a completion-relative generator;
- a relation-anchored generator.

Conceptually:

```text
Source policy / recurring series
        ↓
Occurrence A
Occurrence B
Occurrence C
```

The source answers:

> what pattern or series governs repetition?

The Occurrence answers:

> which individual expected instance?

Therefore:

> **Occurrence != source policy / series.**

Changing one Occurrence does not automatically change the source.

## Occurrence versus recurrence rule

A recurrence rule describes how instances are generated or selected.

Occurrence is one instance identity resulting from that governing recurrence/generation context.

```text
Recurrence
Every Monday / Wednesday / Friday

Occurrence
Wednesday 12 August instance
```

Therefore:

> **Occurrence != RecurrenceRule.**

The exact recurrence language, expansion algorithm, DST semantics, completion-relative generation, and relation-anchored generation remain for the Recurrence review.

## Occurrence versus Routine

Routine represents repeated behavioral/execution policy.

Occurrence represents one expected instance of that policy.

```text
Routine
Weekly review every Sunday

Occurrence
Weekly review expected Sunday 16 August
```

If that one review is moved to Monday, the Routine need not change.

Therefore:

> **Occurrence != Routine.**

Routine lifecycle actions and occurrence-level actions must remain distinct.

Examples:

```text
Skip this occurrence
```

is different from:

```text
Pause the Routine
```

and different again from:

```text
End the Routine
```

## Occurrence versus Activity

Activity represents a concrete actionable intention.

Occurrence represents one expected instance in a recurring/generated context.

They may be related, but they are not identical.

Example:

```text
Routine
Practice English 3 times per week

Occurrence
Second expected practice this week

Activity semantics
English conversation practice
```

The distinction becomes more important for composite Routines.

```text
Routine
Morning routine

Occurrence
Morning routine — 11 August

Contained / generated action semantics
- drink water
- take medication
- prepare bag
```

One Routine Occurrence may coordinate several Activities or steps.

Therefore:

> **Occurrence != Activity.**

### Not every Activity gets an Occurrence

A one-off Activity normally uses its own identity.

```text
Activity
Buy milk
```

LifeOS should not create an artificial:

```text
Occurrence #1 — Buy milk
```

merely because every intention happens sometime.

Likewise:

```text
Activity
Write thesis introduction
```

may execute over multiple Sessions without those Sessions becoming multiple Occurrences.

Occurrence is not a universal wrapper around every Activity.

## Occurrence versus Event

Event is occurrence-centred domain meaning whose temporal placement is intrinsic.

A one-off Event already has persistent Event identity and normally does not need a second Occurrence wrapper solely because it happens once.

```text
Event
Dentist appointment — 18 August 15:00
```

For recurring Events, however, LifeOS needs to distinguish the recurring source/series from individual instances.

Conceptually:

```text
Recurring Event source / series
        ↓
Occurrence 1
Occurrence 2
Occurrence 3
```

The exact physical representation of a recurring Event source remains deferred to the Recurrence/Event-series review. LifeOS does not yet introduce `EventSeries` as a new kernel primitive merely because external calendar APIs expose such a resource.

Therefore:

> **Occurrence != Event.**

and:

> **A one-off Event does not automatically need a separate Occurrence object.**

## Occurrence versus Schedule

Occurrence identifies the expected instance.

Schedule represents temporal placement/commitment of something that can be scheduled.

A flexible recurring expectation may exist before exact placement is chosen.

Example:

```text
Routine
Train 3 times this week

Occurrences
A
B
C

Exact schedule
not assigned yet
```

Later the scheduler may place them:

```text
A — Monday 18:00
B — Thursday 19:00
C — Saturday 10:00
```

Therefore:

> **Occurrence can exist without an exact Schedule.**

and:

> **Occurrence != Schedule.**

Moving the Schedule does not automatically change Occurrence identity.

## Occurrence versus Session

Session represents a concrete temporal execution slice.

One Occurrence may be realized through multiple Sessions.

```text
Occurrence
English study expected today

Session 1
18:00-18:40

Session 2
21:00-21:50
```

This remains one Occurrence if both Sessions collectively realize that expected instance.

Therefore:

> **Occurrence != Session.**

and:

> **One Occurrence may map to zero, one, or multiple Sessions depending on execution semantics.**

The exact Session model is deferred to its own review.

## Occurrence versus Actual

Occurrence is expected-instance identity.

Actual represents what happened.

An Occurrence may have no Actual:

```text
Occurrence
Expected workout

Resolution
Skipped

Actual execution
none
```

An Actual may also exist without a prior Occurrence:

```text
Spontaneous photographic hike
Actual distance: 10.4 km
```

Therefore:

> **Occurrence != Actual.**

and neither is existence-dependent on the other.

The future Actual/Outcome/Evidence cluster will define how an Actual satisfies, partially satisfies, replaces, or otherwise relates to an Occurrence.

## Original expectation, Schedule, and Actual

Occurrence gives the temporal-history stack a stable subject.

Conceptually:

```text
Source policy / series
        ↓
Occurrence identity
        ↓
Original generation expectation
        ↓
Schedule revisions / exception
        ↓
Current accepted schedule
        ↓
Actual execution / attendance / occurrence
```

This prevents history from being overwritten when placement changes.

Example:

```text
Occurrence
Team meeting — weekly instance

Original expectation
Monday 10:00

Official reschedule
Monday 11:30

Actual
Monday 11:38-12:42
```

The three temporal facts remain distinct.

## One-off exception versus future-series revision

Occurrence provides the natural boundary between a local exception and a source-policy revision.

### This occurrence only

```text
Routine
Gym Monday / Wednesday / Friday at 18:00

Occurrence
Wednesday instance

Exception
move to Thursday 20:00
```

The Routine remains unchanged.

### This and future policy

```text
Routine v1
Monday / Wednesday / Friday at 18:00

Boundary occurrence
Wednesday instance

Routine v2
future Wednesdays at 20:00
```

The precise versioning and `effective from` mechanics remain deferred to Recurrence + Versioning, but the semantic requirement is established:

> **Occurrence-level exception and source-policy revision are different operations.**

## Skip, cancellation, postponement, replacement, and identity

A non-executed expected instance must not disappear merely because it did not happen.

Examples:

```text
Occurrence
Workout expected Wednesday
resolution: skipped
```

```text
Occurrence
Weekly meeting instance
resolution: cancelled
```

```text
Occurrence
Study instance
current schedule moved from Wednesday to Thursday
```

The historical identity may remain meaningful for:

- adherence analysis;
- planning quality;
- user review;
- recurrence exception history;
- external synchronization;
- AI explanation;
- audit/history reconstruction.

The exact lifecycle/status vocabulary is intentionally deferred. Occurrence v0 requires only that non-execution and movement do not automatically erase logical identity.

### Replacement

Replacement is more nuanced.

An expected instance may be fulfilled by an alternative execution without becoming that alternative's identity.

Example:

```text
Occurrence
Outdoor run

Weather disruption

Replacement Activity / Actual
Indoor cycling
```

LifeOS may later represent a relation such as `replaced_by` or `satisfied_by_alternative` while preserving the original expected Occurrence.

Exact semantics belong to Relationship + Actual/Outcome reviews.

## Occurrence can exist before exact placement

A generated instance can be identifiable through non-exact anchors.

Possible semantic anchors include:

- local date;
- local datetime;
- instant;
- expected window;
- ordinal within a period;
- completion-relative anchor;
- relation-derived anchor;
- source-version plus sequence/generation context;
- another reviewed temporal anchor.

Occurrence v0 does **not** choose one universal anchor field.

This is essential for patterns such as:

```text
3 times per week
```

where expected instances may exist before specific days/times are selected.

## Completion-relative generation

A completion-relative Routine makes clear that Occurrence is not merely a stored datetime.

```text
Routine
Replace filter 30 days after previous replacement
```

Suppose:

```text
Occurrence #12
Actual completion: 11 August
```

Then the governing policy may generate:

```text
Occurrence #13
expected relative to completion of #12
```

The next exact expected time is causally derived from the previous Actual rather than from a fixed pre-expanded calendar sequence.

This behavior is required conceptually but its generation algorithm belongs to Recurrence.

## Relation-anchored generation

Similarly:

```text
Routine
Back up photographs after every shooting session
```

may generate one expected instance relative to another Event/Activity/Actual.

This intersects the future Trigger and Relationship models.

Occurrence v0 records the requirement without turning Routine into a universal automation engine.

## Time zone, DST, and travel

Occurrence identity must survive changes in the calculated UTC instant that arise from legitimate temporal semantics.

Example:

```text
Routine
08:00 Europe/Rome every day
```

Across daylight-saving changes, `08:00 Europe/Rome` maps to different UTC offsets.

The occurrence remains the expected local-time instance for that date. It does not become a different Occurrence merely because the corresponding UTC instant changes.

Therefore:

> **Occurrence identity must not be defined solely by the resolved UTC timestamp.**

Travel semantics are deliberately deferred. A Routine may be home-time-zone anchored, current-local-time anchored, floating, elapsed-interval based, or governed by domain-specific policy. Recurrence/Schedule must define that later without changing Occurrence identity principles.

## Provider identity and synchronization

External providers may expose:

- series IDs;
- instance IDs;
- recurrence IDs;
- original-start markers;
- external occurrence keys;
- detached-instance identifiers.

LifeOS must preserve provider mappings for synchronization without making them the canonical LifeOS Occurrence identity.

Conceptually:

```text
LifeOS occurrence identity
        ↕ mapping
Provider series / occurrence identity
```

This protects LifeOS history when providers use different recurrence models or IDs change during import/sync behavior.

The exact `ExternalRecord` / integration mapping belongs to the Integration architecture review.

## Virtual versus materialized Occurrences

Occurrence is first a logical identity concept. That does not imply pre-inserting every future instance as a database row.

A daily Routine can conceptually produce tens of thousands of future instances over decades. Eagerly materializing all future Occurrences would be wasteful and creates difficult invalidation when policies change.

Current semantic direction:

```text
Source policy / series
        ↓
Virtual / derivable future occurrence identities
        ↓
Operational horizon or meaningful interaction
        ↓
Materialized / persistently reconstructible occurrence state
```

The exact implementation is intentionally deferred.

### When persistent reconstruction becomes required

Once an Occurrence acquires meaningful independent history, LifeOS must be able to reconstruct it stably.

Examples include:

- user-specific reschedule or edit;
- skip/cancellation;
- exception from source policy;
- accepted Schedule placement that must survive replanning/history;
- notification/confirmation state that matters historically;
- Actual execution or attendance;
- replacement relation;
- external synchronization identity;
- Evidence or analysis tied to that instance;
- any other state whose loss would rewrite history.

This does not yet require a particular SQL table design.

The invariant is:

> **A meaningful historical occurrence must not vanish or silently change identity because the source is expanded again later.**

## Source-version context

Historical Occurrences must retain enough source context to preserve what was expected at the time.

Example:

```text
Routine v1
Monday / Wednesday / Friday

Past occurrences
#20 #21 #22

Routine v2
Tuesday / Thursday
```

LifeOS must not regenerate #20-#22 under v2 and pretend Tuesday/Thursday had always been expected.

Therefore an Occurrence needs persistent association with the governing source context/version or equivalent reconstructible history.

The exact versioning model is deferred.

## Generated Occurrence does not imply generated Activity identity forever

For a simple recurring task, UI may present:

```text
Take out trash every Thursday
```

while the domain preserves:

```text
Routine
        ↓
Occurrence
        ↓
Action semantics / execution
```

LifeOS should avoid one Activity identity that is repeatedly moved forward forever, because that destroys per-instance history.

However, Occurrence v0 does not yet force one separate persistent Activity row for every future Routine instance. That mapping is a persistence/API decision to revisit after Schedule, Session, Actual, and Recurrence are defined.

## User-facing visibility

Occurrence is primarily a domain/temporal identity primitive.

The user does not need to see the noun `Occurrence` in ordinary UI.

User-facing language may instead say:

- this workout;
- this week's review;
- this meeting;
- today's medication;
- this occurrence;
- this instance;
- only this one;
- all future ones.

The domain should remain precise without exposing implementation terminology unnecessarily.

## Representative stress tests

### Moved recurring workout

```text
Routine
Gym M/W/F

Occurrence
Wednesday instance

Original expected
Wednesday 18:00

Current Schedule
Thursday 19:00

Actual
Thursday 19:12-20:24
```

Result: same Occurrence. PASS.

### Skipped workout

```text
Occurrence
Friday workout

Actual
none

Resolution
skipped
```

Result: occurrence remains historically meaningful. PASS.

### Flexible `3 times/week`

```text
Routine
Train 3 times per week
```

Three expected instance identities may exist before exact scheduling.

Result: Occurrence does not require exact datetime. PASS.

### Multi-session execution

```text
Occurrence
Study today

Session A
18:00-18:40

Session B
21:00-21:50
```

Result: one Occurrence, multiple Sessions. PASS.

### Spontaneous execution

```text
Actual
Unplanned 10 km photographic hike
```

Result: Actual exists without Occurrence. PASS.

### One-off Activity

```text
Activity
Buy milk
```

Result: no Occurrence required. PASS.

### One-off Event

```text
Event
Dentist appointment
```

Result: Event identity sufficient; no duplicate Occurrence wrapper required. PASS.

### Recurring meeting exception

```text
Weekly meeting series
Occurrence Monday
moved to Tuesday this week
```

Result: occurrence identity survives move; series remains unchanged. PASS.

### Source revision

```text
Routine v1 M/W/F
past occurrence history
Routine v2 Tue/Thu
```

Result: past occurrence expectations remain governed by historical source context. PASS.

### DST transition

```text
Routine
08:00 Europe/Rome daily
```

UTC mapping changes across DST.

Result: identity does not change merely because UTC offset changes. PASS.

### Completion-relative maintenance

```text
Replace filter every 30 days after actual replacement
```

Result: next occurrence may not have exact temporal identity until prior completion is known. Occurrence remains valid as generated-instance concept. PASS.

## Alternatives considered

### Alternative A — no Occurrence concept; use Schedule only

Rejected.

Schedule describes placement but cannot safely represent stable identity across moves, skip/cancellation, or unscheduled flexible instances.

### Alternative B — current datetime is the occurrence identity

Rejected.

Rescheduling would change identity; flexible occurrences may have no datetime; DST and provider behavior would become brittle.

### Alternative C — original datetime is the universal occurrence ID

Rejected as a LifeOS-wide rule.

It works for many calendar series but fails for flexible frequency, completion-relative, and relation-anchored patterns.

The original temporal anchor remains important metadata/history where applicable, not universal canonical identity.

### Alternative D — every Activity/Event gets exactly one Occurrence

Rejected.

This adds meaningless wrappers to one-off items and blurs Occurrence with ordinary entity identity.

### Alternative E — persist every future Occurrence indefinitely

Rejected as a semantic requirement.

Future expansion can be virtual/lazy. Persistent reconstruction becomes mandatory when instance-specific history exists.

### Alternative F — reuse one recurring Activity and move it forward after completion

Rejected.

This destroys historical per-instance expectation and makes skip, exception, analytics, and actual comparison ambiguous.

## Current invariants

1. **Occurrence != Routine.**
2. **Occurrence != recurring source/series.**
3. **Occurrence != RecurrenceRule.**
4. **Occurrence != Activity.**
5. **Occurrence != Event.**
6. **Occurrence != Schedule.**
7. **Occurrence != Session.**
8. **Occurrence != Actual.**
9. An Occurrence identifies one specific expected instance produced by a recurring/generative source.
10. Occurrence identity does not depend on current start/end.
11. Rescheduling does not automatically create a new Occurrence.
12. Skip/cancellation/non-execution may remain historically identifiable rather than deleting the expected instance.
13. One-off occurrence exceptions do not automatically change the source policy/series.
14. `This and future` changes belong to source-policy/series revision semantics; an Occurrence may provide the effective boundary.
15. Not every Activity requires an Occurrence.
16. Not every Event requires an Occurrence.
17. A one-off Activity normally uses Activity identity directly.
18. A one-off Event normally uses Event identity directly.
19. An Occurrence may exist before exact Schedule placement.
20. One Occurrence may be realized through multiple Sessions.
21. An Actual may exist without a prior Occurrence.
22. An Occurrence may exist without an Actual.
23. LifeOS Occurrence identity is independent from external-provider identity.
24. Occurrence identity must not be defined solely by resolved UTC timestamp.
25. The original semantic anchor may be datetime, date, window, ordinal, completion-relative, relation-derived, or another reviewed anchor; no universal datetime assumption is accepted.
26. Infinite future Occurrences need not all be eagerly materialized.
27. Once meaningful instance-specific history exists, the Occurrence must remain persistently reconstructible.
28. Historical Occurrences must preserve enough governing source/version context to avoid retrospective rewriting.
29. Regenerating a source under a newer rule must not mutate the meaning of historical Occurrences.
30. Occurrence is primarily a domain identity concept; its physical persistence shape remains deferred.

## Open questions intentionally deferred

Occurrence v0 deliberately does not decide:

- exact SQL/table/value-object representation;
- exact occurrence-ID generation algorithm;
- exact virtual-occurrence addressing before materialization;
- exact Event-series parent representation;
- exact Routine-to-Activity materialization model;
- exact Schedule ownership/cardinality;
- exact Session mapping;
- exact lifecycle/status enum for expected/skipped/cancelled/replaced/etc.;
- exact Actual-to-Occurrence fulfillment relation;
- exact recurrence rule language;
- `this and future` revision mechanics;
- completion-relative generation algorithm;
- relation-anchored Routine versus Trigger boundary;
- time-zone/DST/travel policy;
- external-provider deduplication/mapping mechanics;
- notification state ownership;
- retention horizon/materialization strategy;
- offline/conflict-resolution behavior for concurrently edited occurrences.

These questions belong to later Time, Actual/Evidence, Versioning, Relationship, Integration, and persistence reviews.

## Implications for the next concepts

### Schedule

Schedule can now be reviewed without carrying series-instance identity.

It must answer:

> **When is this Activity/Event/Occurrence currently intended or expected to occupy time?**

rather than:

> which recurring instance is this?

Schedule review must determine:

- whether Schedule is entity/value object/history stream;
- original versus current accepted placement;
- schedule revision identity/history;
- exact versus flexible placement;
- whether one Occurrence/Activity can have multiple planned Sessions;
- relationship to Event intrinsic time;
- capacity/availability implications without conflating them with temporal placement.

### Session

Session can focus on execution slices rather than recurring-instance identity.

### Recurrence

Recurrence can focus on generation/pattern semantics rather than historical instance identity.

### Actual / Outcome

Actual can later define how observed execution realizes, partially realizes, replaces, or fails to realize an Occurrence.

## Current conclusion

Occurrence v0 establishes a narrow but essential temporal identity primitive:

```text
Recurring / generative source
        ↓
Occurrence
which expected instance?
        ↓
Schedule / exception
when is it currently expected?
        ↓
Session / Actual
what happened?
```

The key architectural decision is intentionally not `create another calendar object`.

It is:

> **Preserve stable identity for one expected generated instance without forcing every one-off Activity/Event into an Occurrence wrapper and without requiring infinite eager persistence of future instances.**

This is the current accepted baseline entering the Schedule review.

---

# 2026-08-13 — Version / material-equivalence downstream closure amendment

Version v0 closes Occurrence's former source-version / `this and future` / offline-edit semantic dependencies without changing Occurrence identity.

```text
Occurrence identity
= which expected generated instance

Occurrence material state
= materially relevant occurrence-specific state/exception

Source Version
= materially relevant state of the Routine/Event-series/generative policy that governed the instance
```

Historical Occurrences remain attributable to the source Version that generated/governed them. Re-expanding a newer source Version must not mutate their original expectation. A material source-policy revision can apply from a defined boundary without turning earlier Occurrences into descendants of the new policy state.

Occurrence-specific edits such as reschedule, skip, cancellation or assignment exception may have their own material state history while preserving the same Occurrence identity. `This occurrence` and `this and future` remain different operations: the latter changes source-policy state; the former changes the instance state unless policy explicitly says otherwise.

Offline/concurrent edits may branch from one material Occurrence or source state. Version preserves the competing bases; reconciliation/Authority/Decision selects or constructs current accepted state. Technical/provider occurrence revisions and original-start identifiers remain integration/concurrency metadata, not LifeOS semantic Version identity.

AI/system proposals affecting an Occurrence or future policy must retain the material base state where stale-base application would be unsafe.

The historical source-version and concurrent-edit dependencies are now downstream-closed semantically. Exact virtual occurrence addressing/materialization, recurrence generation, lifecycle vocabulary, external mapping and physical persistence remain separately owned.

No Occurrence invariant failed. **Occurrence remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `version.md`;
- `../checkpoints/version-material-equivalence-v0-validation.md`.