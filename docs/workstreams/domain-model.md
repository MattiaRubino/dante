# Workstream — Core Domain Model v0

- Status: **IN PROGRESS**
- Active branch: `feature/domain-model`
- Base: `main` at `73f0d172de239853e568532535a4739ce77a0877`
- PR: none yet
- Work type: domain modeling / invariants / persistence preparation
- Current execution mode: documentation/modeling slice independent from backend implementation

## Purpose

Turn the LifeOS product vocabulary and requirements into an implementation-ready domain model without prematurely designing every specialist module or every final SQL table.

This pass explicitly revalidates earlier concepts instead of treating prior documentation as automatically correct. Earlier product definitions remain valuable inputs, but a concept can be revised when broader scenario coverage, stronger reasoning, external benchmarks, or implementation constraints reveal a better model.

## Current decision rule

**Accepted means current best decision, not immutable decision.**

Decisions may be reopened when new evidence, edge cases, contradictions, or better abstractions emerge. Changes must be explicit, reasoned, and preserved in history rather than silently rewriting prior assumptions.

The active modeling method, documentation standard, benchmark/interoperability rule, and mandatory concept-review protocol live in [`../domain/README.md`](../domain/README.md).

## Required reading

1. [`../PROJECT-STATUS.md`](../PROJECT-STATUS.md)
2. [`../development/operating-rules.md`](../development/operating-rules.md)
3. [`../domain/README.md`](../domain/README.md)
4. [`../domain/checkpoints/intention-execution-v0.md`](../domain/checkpoints/intention-execution-v0.md)
5. [`../domain/concepts/goal.md`](../domain/concepts/goal.md)
6. [`../domain/concepts/plan.md`](../domain/concepts/plan.md)
7. [`../domain/concepts/activity.md`](../domain/concepts/activity.md)
8. [`../domain/concepts/event.md`](../domain/concepts/event.md)
9. [`../domain/concepts/routine.md`](../domain/concepts/routine.md)
10. [`../domain/concepts/milestone.md`](../domain/concepts/milestone.md)
11. [`../domain/concepts/occurrence.md`](../domain/concepts/occurrence.md)
12. [`../domain/concepts/schedule.md`](../domain/concepts/schedule.md)
13. [`../domain/concepts/session.md`](../domain/concepts/session.md)
14. [`../domain/concepts/temporal-constraint.md`](../domain/concepts/temporal-constraint.md)
15. [`../domain/concepts/recurrence.md`](../domain/concepts/recurrence.md)
16. [`../domain/concepts/availability-capacity.md`](../domain/concepts/availability-capacity.md)
17. [`../product/v1-core-domain-glossary.md`](../product/v1-core-domain-glossary.md)
18. [`../product/v1-goal-and-program-lifecycle.md`](../product/v1-goal-and-program-lifecycle.md)
19. [`../product/v1-execution-status.md`](../product/v1-execution-status.md)
20. [`../product/v1-confirmation-and-reminders.md`](../product/v1-confirmation-and-reminders.md)
21. [`../product/v1-scheduling-flexibility.md`](../product/v1-scheduling-flexibility.md)
22. [`../product/v1-data-history-and-privacy.md`](../product/v1-data-history-and-privacy.md)
23. [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md)
24. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
25. [`../decisions/ADR-003-primary-database.md`](../decisions/ADR-003-primary-database.md)
26. [`../decisions/ADR-006-hybrid-personal-data-model.md`](../decisions/ADR-006-hybrid-personal-data-model.md)

## Where to work

The current work is a clearly separated documentation/modeling slice, so it is running on `feature/domain-model` without backend implementation changes.

When persistence mapping and backend package boundaries begin to overlap materially with Backend Foundation, the branches/workstreams must be synchronized deliberately before implementation. Do not run two branches against the same implementation/domain files merely to make the workstreams look separate on paper.

The Domain Model handoff remains separate so decisions and unresolved questions can be resumed independently by another agent.

## Rules

- Revalidate concepts one at a time; do not inherit terminology merely because it already exists.
- For every concept, inspect applicable internal documentation/scenarios and perform enough targeted external benchmarking to expose likely missing semantics before acceptance.
- External standards/products are evidence, not compatibility requirements or design authorities; preserve LifeOS semantics first and push provider-specific compromises into adapters when practical.
- Canonical Domain Atlas documentation is maintained in English; discussion language does not create a second canonical translation tree.
- Do not model one table per life topic (`english`, `photography`, `farming`, etc.).
- Do not collapse everything into one `entities` table or arbitrary JSON blob.
- Do not treat AI inference as confirmed truth.
- Keep operational policy separate from domain/topic type where behavior differs by user/plan.
- Preserve planned/actual/history distinctions.
- Preserve original intention when later evidence reveals additional relevance; do not rewrite history to make past execution look intentionally linked to a Goal when it was not.
- Prefer progressive formalization: generic first when genuinely unpredictable; promote repeated/query-heavy concepts through reviewed migrations.
- Do not reopen an accepted architectural ADR merely because a first implementation mapping is inconvenient; propose an explicit ADR change when new evidence genuinely challenges the architecture.
- Preserve earlier documents while conflicts are being revalidated; propagate replacements deliberately after related concepts are understood.
- Run cluster checkpoints in addition to concept-level reviews; do not defer all cross-model validation until the end.

## Validated cluster — Intention & Execution v0

Status: **PASS — current validated cluster baseline**.

Validated concepts:

- Goal v0;
- Plan v0;
- Activity v0;
- Event v0;
- Routine v0;
- Milestone v0.

Checkpoint record:

- [`../domain/checkpoints/intention-execution-v0.md`](../domain/checkpoints/intention-execution-v0.md)

Checkpoint conclusions:

- no accepted baseline currently needs reopening;
- Milestone was the one material missing concept exposed by the first pass and is now included;
- no universal parent/child hierarchy is required;
- Activity versus Plan and Routine versus Plan remain intentionally soft semantic boundaries but passed the current scenario matrix;
- Activity versus Event remains action-centred versus occurrence-centred rather than schedule-based;
- recurring Event versus Routine remains series-of-occurrences versus behavioral-policy semantics;
- Goal versus Milestone remains independent desired outcome versus contextual checkpoint;
- planned/current/actual/history distinctions remain intact;
- evidence may reach Goal criteria even when the source execution was not originally linked to that Goal;
- later temporal, evidence, relationship, persistence, or implementation work may still reopen the cluster if new contradictions appear.

## Current cluster — Time

All currently planned individual Time-concept reviews are complete.

Accepted current baselines:

```text
Occurrence v0
Schedule v0
Session v0
Temporal Constraint v0
Recurrence v0
Availability & Capacity v0
```

Status of the cluster itself:

> **CHECKPOINT PENDING — not yet a validated cluster baseline.**

Next required step:

> **Time Cluster Checkpoint v0**

The checkpoint must stress-test all six concepts together before the workstream proceeds to Observed Reality & Evidence.

## Occurrence v0 — accepted current baseline

`Occurrence` is the stable logical identity of one expected instance produced by a recurring/generative source.

Key decisions:

- identifies **which expected instance**, not when it is currently scheduled;
- distinct from Routine, recurring source/series, RecurrenceRule, Activity, Event, Schedule, Session, and Actual;
- identity does not depend on current start/end or resolved UTC instant;
- rescheduling does not automatically create a new Occurrence;
- skip/cancellation/non-execution may remain historically identifiable;
- one-off Activity and Event normally use their own identity without artificial Occurrence wrappers;
- may exist before exact Schedule placement;
- may later be realized through multiple Sessions;
- future Occurrences may remain virtual/derived until instance-specific history requires persistent reconstruction;
- historical Occurrences retain enough source/version context to prevent later source revisions from rewriting history;
- exact SQL persistence/materialization remains deferred.

Record: [`../domain/concepts/occurrence.md`](../domain/concepts/occurrence.md)

## Schedule v0 — accepted current baseline

`Schedule` is the current accepted temporal assignment of a schedulable subject.

Key decisions:

- answers **when execution/occurrence is currently intended or expected**, not what the subject is;
- distinct from Activity, Event, Occurrence, Actual, Session, Deadline/Target, Temporal Constraint, RecurrenceRule, Routine, Movement Policy, and Availability/Capacity;
- system/AI suggestion remains a proposal until accepted by user authority or authorized policy;
- Activity may exist without Schedule;
- Occurrence may exist before exact Schedule placement;
- Event uses Schedule for accepted temporal placement without duplicating Event identity;
- Schedule revision preserves subject identity and history;
- Actual deviation does not silently rewrite Schedule;
- Schedule precision may be date-only, coarse, exact, start-only, interval-based, floating local, named-zone local, or absolute-instant as applicable;
- one schedulable subject may have multiple accepted planned placements;
- estimated effort, scheduled duration, and actual duration remain distinct;
- having a Schedule does not imply consuming user capacity/busy time;
- recurrence remains separate from the single accepted Schedule of an instance;
- exact placement/revision SQL representation remains deferred.

Record: [`../domain/concepts/schedule.md`](../domain/concepts/schedule.md)

## Session v0 — accepted current baseline

`Session` is accepted as a persistent record of one bounded episode of actual execution or performed behavior.

Key decisions:

- Session is **actual execution**, never the canonical planned placement;
- Session is distinct from Schedule, Activity, Occurrence, Routine, Event attendance/actual occurrence, and broader Actual/Outcome;
- one Activity/Occurrence may have zero, one, or many Sessions;
- planned placements and Sessions do not require one-to-one mapping;
- Session may exist without prior Schedule;
- spontaneous execution may be captured as Session without fabricating a pre-existing Activity, while retaining sufficient semantic context/provenance;
- pause does not automatically create a new Session;
- one Session may contain multiple active intervals separated by pauses;
- elapsed, active, and paused duration are conceptually distinct;
- explicit end/close followed by later restart normally creates another Session;
- no arbitrary universal pause threshold determines Session identity;
- a running Session may have unknown end;
- Session identity is stable independently from timestamps;
- corrections preserve identity/history; split/merge preserve lineage/provenance;
- ending Session does not imply Activity/Occurrence completion;
- manual, timer/stopwatch, imported, and authorized automatic sources are provenance differences rather than Session types;
- Timer/Stopwatch are capture/control mechanisms; Session is the persistent execution record;
- measurements/Observations may relate to Session without becoming arbitrary Session JSON;
- overlapping Sessions are not globally invalid; compatibility is context-specific and analytics must avoid naïve elapsed-time summation;
- Event actual occurrence/attendance does not receive a redundant Session by default;
- broader Actual may aggregate several Sessions and may also exist without any Session detail;
- LifeOS Session identity remains separate from provider record identity;
- exact lifecycle enum, pause persistence, parent cardinality, split/merge schema, and SQL remain deferred.

Record: [`../domain/concepts/session.md`](../domain/concepts/session.md)

## Temporal Constraint v0 — accepted current baseline

`Temporal Constraint` is accepted as the general rule capability that restricts or prefers temporal placement, duration, or temporal relationships without becoming Schedule or Actual.

Key decisions:

- Temporal Constraint answers **when execution/occurrence is allowed, required, bounded, or preferred**;
- Temporal Constraint is distinct from Schedule, Session/Actual, Recurrence, Availability/Capacity, and Movement Policy;
- `Deadline` is a latest-bound Temporal Constraint semantic specialization rather than a separate kernel primitive;
- `Window` is a range-shaped temporal expression whose semantics depend on context rather than a universal primitive;
- target date/window and review date do not automatically become hard Temporal Constraints;
- the constrained temporal feature must remain explicit when relevant: start, completion/delivery, containment, duration, spacing, exclusion, or another temporal relationship;
- hard constraints define planning admissibility; soft constraints/preferences guide optimization;
- hard/soft strength is distinct from authority/mutability;
- Actual that violates a hard constraint remains valid history and may produce a derived violation;
- passing a deadline does not automatically create `missed` or failure outcome;
- multiple hard constraints must be jointly satisfiable or the current planning problem is infeasible;
- LifeOS must surface infeasibility instead of silently violating hard constraints;
- constraints may be boundary-, range-, duration-, spacing-, exclusion-, or relation-based;
- constraints may operate at broader Plan/Routine scopes and receive Occurrence-specific exceptions without requiring physical duplication;
- material constraint revisions remain distinct from Schedule revisions and preserve enough history/provenance to explain replanning;
- recurring constraint patterns may reuse Recurrence without becoming occurrence-generating sources;
- exact entity/value-object split, SQL, scoping persistence, optimizer representation, and rule encoding remain deferred.

Record: [`../domain/concepts/temporal-constraint.md`](../domain/concepts/temporal-constraint.md)

## Recurrence v0 — accepted current baseline

`Recurrence` is accepted as a structured repeating-pattern capability that describes how repeated temporal/generative structure behaves without becoming the recurring source, Occurrence, Schedule, Actual, or generic automation engine.

Key decisions:

- Recurrence is distinct from Routine and recurring Event semantics;
- Recurrence is distinct from Occurrence identity, Schedule, Session/Actual, Temporal Constraint, and Trigger;
- Recurrence may produce logical/quota Occurrences without exact timestamps;
- calendar/wall-clock, elapsed-interval, quota-per-period, completion-relative, anchor-stream-relative, and cyclic semantics are materially distinct families;
- `every day at 08:00` is not automatically equivalent to `every 24 elapsed hours`;
- floating/user-local, named-zone wall-clock, and absolute/elapsed semantics remain distinguishable;
- pattern anchor and effective recurrence range remain separate;
- occurrence-count semantics describe expectations generated, not successful completions;
- completion-relative recurrence explicitly depends on qualifying Actual/fact anchors and must not silently become an independent fixed calendar series;
- anchor-stream recurrence remains a bounded repeated mapping from qualifying anchors rather than arbitrary condition detection;
- one-off Schedule/Occurrence exceptions do not automatically mutate the recurrence rule;
- structural `this and future` changes become effective future source/Recurrence revisions rather than rewriting history;
- generated-then-skipped/cancelled remains distinct from structurally excluded-before-generation;
- future Occurrences may remain virtual and purely virtual future candidates may be regenerated after a structural revision;
- future Occurrences with instance-specific history must be reconciled rather than silently disappearing;
- correction of an Actual recurrence anchor may recompute future expectations while preserving materialized history/provenance;
- DST, travel, invalid calendar dates, leap days, and ambiguous/nonexistent local times require explicit/domain semantics rather than one hidden universal policy;
- natural-language recurrence text is input/provenance, not the normalized canonical model;
- external recurrence standards/provider formats are benchmark evidence and optional adapter targets, not kernel authorities;
- lossless mapping to RRULE or any provider recurrence format is not a LifeOS invariant;
- exact DSL, SQL, typed representation, resolver algorithms, materialization horizon, and effective-version storage remain deferred.

Record: [`../domain/concepts/recurrence.md`](../domain/concepts/recurrence.md)

## Availability & Capacity v0 — accepted current baseline

`Availability & Capacity` is accepted as the scheduling-resource model that separates usable capacity from accepted Schedule placement.

Key decisions:

- Availability answers **when a schedulable resource has capacity that may be used**;
- Capacity answers **what compatible commitments the resource can sustain**;
- Capacity Reservation/Claim represents capacity committed, occupied, protected, or held;
- Effective Free Capacity is derived rather than treated as a canonical list of stored empty intervals;
- Schedule placement and capacity reservation remain distinct semantics;
- a scheduled item does not automatically imply busy/occupied capacity;
- Availability is distinct from Temporal Constraint and from scheduling preference;
- Capacity is not universally binary and not universally a single scalar/percentage;
- timestamp overlap alone does not establish capacity conflict; compatibility semantics matter;
- incompatible overbooking must remain representable and surfaced rather than rejected/destructively normalized;
- recurring Availability may reuse Recurrence without creating execution Occurrences;
- positive/negative Availability overrides can alter baseline capacity temporarily;
- Temporary Mode may alter Availability/Capacity without rewriting stable baseline history;
- Event participation/attendance and all-day placement do not automatically determine capacity impact;
- external free/busy data remains imported evidence/provenance, not universal LifeOS truth;
- `Calendar Block` remains valid product/UI language but is not a separate kernel primitive by default;
- standalone protected/unavailable/tentative temporal constructs can be represented through reservation/availability semantics without inventing fake Activities;
- exact Resource, reservation identity, capacity dimensions, SQL, and persistence shape remain deferred.

Record: [`../domain/concepts/availability-capacity.md`](../domain/concepts/availability-capacity.md)

## Current task — Time Cluster Checkpoint v0

The individual Time concepts are accepted but must now be validated as one combined model.

Checkpoint scope:

```text
Occurrence
Schedule
Session
Temporal Constraint
Recurrence
Availability & Capacity
```

The checkpoint must determine whether the combined model survives realistic and adversarial scenarios without:

- duplicated temporal truth;
- accidental identity changes;
- hidden history rewrites;
- one-to-one assumptions between planned and actual execution;
- false free/busy assumptions;
- recurrence ambiguity;
- excessive special-case behavior;
- one universal JSON temporal escape hatch;
- provider-specific schemas leaking into the kernel.

## Required checkpoint tests

At minimum the checkpoint should test:

### Recurring workout with reschedule and Actual deviation

```text
Routine
M/W/F workout

Wednesday Occurrence
original expectation Wed 18:00
current Schedule Thu 19:00
Session Thu 18:50-20:05
```

Verify:

- same Occurrence identity;
- Recurrence unchanged;
- Schedule revision preserved;
- Session does not rewrite Schedule;
- capacity impact remains coherent.

### Flexible quota recurrence

```text
Routine
3 workouts per week
```

Verify:

- logical expected Occurrences may exist without exact dates;
- Schedule can assign them later;
- no fake M/W/F assumption;
- quota count is expectation count, not completion criterion.

### Completion-relative maintenance

```text
Replace filter
30 days after previous Actual replacement
```

Verify:

- fixed calendar recurrence is not invented;
- next Occurrence depends on qualifying Actual anchor;
- correction of anchor Actual can recompute future expectation without rewriting materialized history.

### Medication / DST

Test both:

```text
08:00 local wall-clock
```

and:

```text
every 12 elapsed hours
```

Verify they remain distinct through DST/travel behavior and no hidden universal UTC assumption appears.

### Recurring Event instance moved

```text
Monday meeting series
one Monday moved to Tuesday
```

Verify:

- Event semantics remain Event semantics;
- same Occurrence identity;
- one-off Schedule exception does not mutate Recurrence;
- `this and future` requires source/Recurrence revision instead.

### Deadline + preferred window + availability

```text
Activity
submit report

hard completion deadline Friday 17:00
preferred work window morning
user availability 09:00-18:00
```

Verify:

- Deadline/Window do not become Schedule;
- preference does not become Availability;
- planner can find a feasible accepted placement;
- passing deadline does not automatically assert `missed` without Actual/Outcome.

### Protected focus and non-blocking Event

```text
Protected focus 15:00-17:00
Optional webinar 15:30-16:30
```

Verify:

- Calendar Block does not need separate kernel duplication;
- focus can reserve capacity without Activity;
- scheduled webinar may remain non-blocking/compatible;
- timestamp overlap alone is not conflict.

### Imported double booking

```text
Meeting A 15:00-16:00
Meeting B 15:30-16:30
```

Verify:

- both facts remain representable;
- capacity conflict is derived;
- system does not silently delete/rewrite either.

### Temporary disruption

```text
Normal availability Mon-Fri 09:00-18:00
Temporary illness week
```

Verify:

- temporary capacity/availability override does not rewrite stable baseline;
- future Schedule can be replanned while past history remains intact.

### Divisible Activity

```text
Activity
3h study

planned placements
2h + 1h

actual Sessions
80m + 40m + 35m
```

Verify:

- multiple planned placements and multiple actual Sessions coexist;
- no one-to-one mapping requirement;
- estimated effort, scheduled duration, active Session time, and Outcome remain separate.

### Compatible concurrent behavior

```text
Walk + English listening
```

Verify:

- overlapping Schedule/Session intervals can be compatible;
- analytics do not naïvely treat two one-hour Sessions as two elapsed wall-clock hours.

### External provider mapping

Test provider recurrence/free-busy input that is weaker/different than LifeOS semantics.

Verify:

- provider IDs/statuses do not become LifeOS identity;
- adapters can map/degrade without kernel distortion;
- provenance remains available.

## Checkpoint decision questions

The checkpoint must answer:

1. Are the six Time concepts individually necessary?
2. Is any pair still semantically duplicated?
3. Is a missing Time primitive exposed by combined scenarios?
4. Can history be reconstructed after rescheduling, recurrence revision, Actual correction, or availability override?
5. Can simple one-off Activities/Events avoid unnecessary wrappers?
6. Can recurring/generative sources avoid eager infinite materialization?
7. Can flexible and exact temporal semantics coexist without false precision?
8. Can the planner distinguish allowed, preferred, accepted, available, reserved, and actual time?
9. Can inconsistent/imported real-world states remain representable?
10. Can future persistence remain relational/queryable without turning the model into arbitrary JSON?
11. Does any conclusion require reopening the Intention & Execution cluster?
12. Which unresolved questions genuinely belong to Actual/Outcome/Provenance, Resource, Relationship, Version, or persistence work rather than Time?

The checkpoint result must be explicitly documented as PASS or FAIL before the workstream proceeds.

## Current conceptual direction

```text
Goal         -> what is wanted
Plan         -> how it is intended to be pursued or organized
Activity     -> what concrete action is intended
Event        -> what occurrence-centred thing is expected to happen
Routine      -> what recurring behavioral/execution policy is intended
Milestone    -> what meaningful contextual checkpoint is expected/reached
Recurrence   -> how a recurring/generative pattern repeats
Occurrence   -> which individual expected generated instance exists
Constraint   -> where/when execution is allowed, required, or preferred
Availability -> when schedulable capacity may be used
Capacity     -> ability to accept compatible commitments
Schedule     -> when execution/occurrence is currently accepted to happen
Session      -> which actual execution episode happened
Actual       -> broader truth about what happened
Evidence     -> what supports evaluation
```

Important temporal separation:

```text
Recurring source / intention
        ↓
Recurrence where applicable
        ↓
Occurrence identity where applicable
        ↓
Temporal Constraint(s)
        ↓
Availability / Capacity feasibility
        ↓
Schedule
        ↓
Session / Event Actual
        ↓
Outcome / Evidence later
```

This is conceptual rather than a required execution pipeline. Schedule may create capacity claims, and current availability/capacity determines whether a candidate Schedule is feasible.

## Important unresolved questions after individual Time reviews

The following remain deliberately open and should not be mistaken for failures of the current concept definitions:

- exact Recurrence DSL/types/resolver/materialization persistence;
- exact Session state/lifecycle and pause persistence;
- exact Schedule planned-placement/revision persistence;
- exact Temporal Constraint persistence/scoping/authority representation;
- exact Occurrence identity/materialization SQL representation;
- exact Availability/Capacity/Reservation persistence shape;
- exact Resource model and capacity dimensions;
- exact Event-series persistence parent;
- exact Event lifecycle/participant/attendance state machines;
- exact Goal/Plan/Routine/Milestone lifecycle state machines;
- exact version-versus-replacement boundaries;
- criterion entity/value-object/persistence model;
- Actual, Observation, Evidence, Outcome, Confirmation, and Provenance boundaries;
- formal relationship semantics, including support, contribution, conflict, dependency, decomposition, Goal-to-Goal effects, and multi-goal execution;
- exact Life Area / World / Value model;
- Asset / Subject / Resource model;
- persistence/API mapping.

The Time checkpoint should identify whether any of these actually blocks temporal coherence. If not, they remain downstream dependencies rather than reasons to prematurely design tables now.

## Output expected before broad persistence implementation

- concise conceptual model;
- entity/value-object boundaries;
- key invariants;
- ownership model;
- lifecycle/state distinctions;
- structural relationship map;
- dynamic relationship/provenance rules;
- first persistence mapping for the initial vertical slice;
- explicit list of questions intentionally deferred.

## First implementation target

The model should eventually become concrete enough to implement an initial vertical slice around:

`Workspace → Goal/Plan → Activity/Event/Routine/Milestone → Recurrence/Occurrence/Constraint/Availability/Capacity/Schedule/Session → Actual/Confirmation`

This remains a working implementation target, not a final persistence schema.

## Handoff

- Active branch: `feature/domain-model`
- PR: none
- Base main commit: `73f0d172de239853e568532535a4739ce77a0877`
- Intention & Execution Cluster v0: **PASS / validated current baseline**
- Time cluster: **individual concept reviews complete / checkpoint pending**
- Completed current baselines: `Goal v0`, `Plan v0`, `Activity v0`, `Event v0`, `Routine v0`, `Milestone v0`, `Occurrence v0`, `Schedule v0`, `Session v0`, `Temporal Constraint v0`, `Recurrence v0`, `Availability & Capacity v0`
- Goal concept commit: `084394ef5523517139335b5e5496aa0e4862c737`
- Plan concept commit: `7a5b9962abb503aa9532daf2acf41af23d699060`
- Activity final concept commit: `f2b2db24bd26684bd58aa925478a1623bf2316fc`
- Event concept commit: `84e460ba31d5b88b1f415d27d8254803358109f4`
- Routine concept commit: `f0de8c241d7650bbdbaffdf1b8cb102facf713fc`
- Milestone concept commit: `46ddf9d4bdc514fc56a718a93ad0258a2aa34a4b`
- Intention/execution checkpoint commit: `646f41452c357010550f3fa0ab96147518ddaa4c`
- Occurrence concept commit: `a55fa28b2fb27b1967d18f26b318b173972e35ee`
- Schedule concept commit: `e716e6ad16391f20bd9264c84733dc4f88da4ef8`
- Session concept commit: `fef80394849e38e9215303b3ee6b1813ef3621a0`
- Temporal Constraint concept commit: `de3a6bb8ca78a7c2f429cf2986c65f084592ac64`
- Recurrence concept commit: `58e2c50bcfac45a7a5ad8b5140b90040038fddae`
- Availability & Capacity concept commit: `87881b5ddd2ae7952e1982a3624d0a1f1b261833`
- Backend implementation: not started in this branch
- Main modified: no
- Phase 4 prototype branch modified: no
- Current task: `Time Cluster Checkpoint v0` review/stress test
- Known documentation conflicts: earlier glossary assumes Goal/Program/Project are distinct and uses narrower Activity/Event/Routine/Calendar Block semantics; active Domain Atlas baselines supersede those definitions for this workstream pending deliberate reconciliation after related clusters are stable.
