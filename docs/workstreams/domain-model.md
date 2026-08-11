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

The active modeling method, documentation standard, and mandatory concept-review protocol live in [`../domain/README.md`](../domain/README.md).

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
13. [`../product/v1-core-domain-glossary.md`](../product/v1-core-domain-glossary.md)
14. [`../product/v1-goal-and-program-lifecycle.md`](../product/v1-goal-and-program-lifecycle.md)
15. [`../product/v1-execution-status.md`](../product/v1-execution-status.md)
16. [`../product/v1-confirmation-and-reminders.md`](../product/v1-confirmation-and-reminders.md)
17. [`../product/v1-scheduling-flexibility.md`](../product/v1-scheduling-flexibility.md)
18. [`../product/v1-data-history-and-privacy.md`](../product/v1-data-history-and-privacy.md)
19. [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md)
20. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
21. [`../decisions/ADR-003-primary-database.md`](../decisions/ADR-003-primary-database.md)
22. [`../decisions/ADR-006-hybrid-personal-data-model.md`](../decisions/ADR-006-hybrid-personal-data-model.md)

## Where to work

The current work is a clearly separated documentation/modeling slice, so it is running on `feature/domain-model` without backend implementation changes.

When persistence mapping and backend package boundaries begin to overlap materially with Backend Foundation, the branches/workstreams must be synchronized deliberately before implementation. Do not run two branches against the same implementation/domain files merely to make the workstreams look separate on paper.

The Domain Model handoff remains separate so decisions and unresolved questions can be resumed independently by another agent.

## Rules

- Revalidate concepts one at a time; do not inherit terminology merely because it already exists.
- For every concept, inspect applicable internal documentation/scenarios and perform enough targeted external benchmarking to expose likely missing semantics before acceptance.
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

The cluster was tested against one consistent scenario matrix spanning study, work, health, fitness, medication, job search, travel, moving house, creative release, finance, caregiving/subjects, disrupted weeks, multi-Goal evidence, recurring behavior, and mixed Event/Activity cases.

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

The workstream is now in the **Time** cluster.

Current sequence:

```text
Occurrence v0 — accepted
→ Schedule v0 — accepted
→ Session — current review target
→ Deadline / Window / Temporal Constraint
→ Recurrence
→ Calendar Block / Availability / Capacity
```

The order may change when a concept reveals a stronger dependency.

## Occurrence v0 — accepted current baseline

`Occurrence` is accepted as the stable logical identity of one expected instance produced by a recurring/generative source.

Key decisions:

- Occurrence identifies **which expected instance**, not when it is currently scheduled;
- Occurrence is distinct from Routine, recurring source/series, RecurrenceRule, Activity, Event, Schedule, Session, and Actual;
- identity does not depend on current start/end or the resolved UTC instant;
- rescheduling an instance does not automatically create a new Occurrence;
- skip/cancellation/non-execution may remain historically identifiable;
- one-off Activity and one-off Event normally use their own identity without an artificial Occurrence wrapper;
- Occurrence may exist before exact Schedule placement;
- one Occurrence may later be realized through multiple Sessions;
- Actual may exist without Occurrence and Occurrence may exist without Actual;
- LifeOS identity remains independent from provider recurrence/instance IDs;
- temporal anchors may be exact datetime, local date/time, window, ordinal, completion-relative, relation-derived, or another reviewed anchor rather than one universal datetime key;
- future Occurrences may remain virtual/derived rather than being eagerly materialized forever;
- once instance-specific history exists, the Occurrence must remain persistently reconstructible;
- historical Occurrences must retain enough source/version context so later source revisions cannot rewrite prior expectations;
- exact SQL persistence/materialization mechanics remain deliberately deferred.

Record:

- [`../domain/concepts/occurrence.md`](../domain/concepts/occurrence.md)

## Schedule v0 — accepted current baseline

`Schedule` is accepted as the current accepted temporal assignment of a schedulable subject.

Key decisions:

- Schedule answers **when execution/occurrence is currently intended or expected**, not what the subject is;
- Schedule is distinct from Activity, Event, Occurrence, Actual, Session, Deadline/Target, Temporal Constraint, RecurrenceRule, Routine, Movement Policy, and Availability/Capacity;
- an AI/system suggestion is a Schedule proposal until user authority or an explicitly authorized automatic policy accepts it;
- Activity may exist without Schedule;
- Occurrence may exist before exact Schedule placement;
- Event uses Schedule for accepted temporal placement without duplicating Event identity;
- Schedule revision preserves subject identity;
- original accepted placement and current accepted Schedule must remain historically reconstructible;
- Actual deviation does not silently rewrite Schedule;
- Schedule revisions can move earlier/later, shorten/extend, or change only one boundary;
- explicit expected end/start may be revised during execution without confusing that revision with an unplanned Actual overrun;
- Schedule precision may be date-only, coarse, exact, start-only, interval-based, floating local, named-zone local, or absolute-instant as applicable; false precision must not be invented;
- all-day/date-based placement is not semantically the same as a normal 24-hour instant interval;
- one schedulable subject may have multiple accepted planned placements when execution is divisible;
- estimated effort, scheduled duration, and actual duration remain distinct;
- the same temporal shape may represent accepted Schedule, allowed/preferred Constraint, capacity block, or another concept depending on semantics;
- having a Schedule does not imply consuming user capacity/busy time;
- recurrence remains separate from the single accepted Schedule of an instance;
- lack of Schedule is valid; unscheduling does not cancel the subject;
- cancellation of an Event/Occurrence is not represented merely by deleting Schedule history;
- Schedule revisions require enough provenance/authority for explanation and external reconciliation;
- exact Schedule/placement/revision SQL representation remains deliberately deferred.

Record:

- [`../domain/concepts/schedule.md`](../domain/concepts/schedule.md)

## Current task — Session

Review `Session` as the next Time-cluster concept.

The review must determine at minimum:

- whether Session is fundamentally an **actual execution interval/slice** rather than a planned scheduling structure;
- whether a Session requires an Activity/Occurrence/Event parent or may exist independently;
- whether one Activity or Occurrence may have zero, one, or many Sessions;
- whether one Session may realize more than one planned Schedule placement;
- whether one Session may contribute to multiple Activities/Goals without creating ambiguous ownership;
- how pause/resume works: pause intervals inside one Session versus multiple Sessions;
- whether stopping and later resuming the same work creates a new Session and under what boundary;
- how manual actual-time entry differs from stopwatch/timer-captured Session data;
- how Session relates to Actual, Outcome, Completion, Attendance, quantities, notes, and Evidence;
- whether Events need Sessions or use attendance/actual occurrence semantics directly;
- how background/passive activities or long-running work are represented;
- how simultaneous/overlapping Sessions should be treated;
- whether Session itself can be corrected/reopened while retaining previous timing history;
- how a Session relates to planned placements when execution begins earlier/later or outside the planned block;
- how estimated effort, scheduled duration, active working time, paused time, and elapsed Session duration remain distinct;
- whether Timer/Stopwatch are tools that create/update Session rather than separate domain execution concepts;
- how imported actual intervals from integrations map into Session/Actual with provenance.

## Current conceptual direction

```text
Goal       -> what is wanted
Plan       -> how it is intended to be pursued or organized
Activity   -> what concrete action is intended
Event      -> what occurrence-centred thing is expected to happen
Routine    -> what recurring behavioral/execution policy is intended
Milestone  -> what meaningful contextual checkpoint is expected/reached
Occurrence -> which individual expected generated instance exists
Schedule   -> when execution/occurrence is currently accepted to happen
Session    -> actual execution slice (under review)
Actual     -> what actually happened
Evidence   -> what supports evaluation
```

Important temporal chain now required conceptually:

```text
Source policy / domain intention
        ↓
Occurrence identity where applicable
        ↓
Accepted Schedule placement(s)
        ↓
Actual execution Session(s)
        ↓
Outcome / Observation / Evidence later
```

Actual time may be earlier, later, shorter, longer, split, interrupted, or absent relative to accepted Schedule.

## Important unresolved questions

- exact Session identity and lifecycle;
- Session versus broader Actual record boundary;
- Session pause/resume and active-vs-elapsed time semantics;
- Session ownership/linking to Activity/Occurrence/Event;
- whether one Session can realize multiple semantic intentions;
- Timer/Stopwatch domain/tool boundary;
- exact Schedule planned-placement persistence;
- exact Schedule revision/audit persistence;
- exact Occurrence identity/materialization SQL representation;
- exact Deadline / Window / Temporal Constraint semantics;
- hard versus soft temporal constraints;
- recurrence materialization, timezone/DST, travel, and completion-relative recurrence mechanics;
- Calendar Block / Availability / Capacity semantics;
- exact Event-series parent representation;
- exact Event lifecycle/participant/attendance state machines;
- exact Goal/Plan/Routine/Milestone lifecycle state machines;
- exact version-versus-replacement boundaries;
- criterion entity/value-object/persistence model;
- Actual, Observation, Evidence, Outcome, Confirmation, and Provenance boundaries;
- formal relationship semantics, including support, contribution, conflict, dependency, decomposition, Goal-to-Goal effects, and multi-goal execution;
- relation-anchored Routine versus Trigger boundary;
- exact Life Area / World / Value model;
- Asset / Subject model;
- persistence/API mapping.

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

`Workspace → Goal/Plan → Activity/Event/Routine/Milestone → Occurrence/Schedule/Session → Actual/Confirmation`

This remains a working implementation target, not a final persistence schema.

## Handoff

- Active branch: `feature/domain-model`
- PR: none
- Base main commit: `73f0d172de239853e568532535a4739ce77a0877`
- Intention & Execution Cluster v0: **PASS / validated current baseline**
- Completed current baselines: `Goal v0`, `Plan v0`, `Activity v0`, `Event v0`, `Routine v0`, `Milestone v0`, `Occurrence v0`, `Schedule v0`
- Goal concept commit: `084394ef5523517139335b5e5496aa0e4862c737`
- Plan concept commit: `7a5b9962abb503aa9532daf2acf41af23d699060`
- Activity final concept commit: `f2b2db24bd26684bd58aa925478a1623bf2316fc`
- Event concept commit: `84e460ba31d5b88b1f415d27d8254803358109f4`
- Routine concept commit: `f0de8c241d7650bbdbaffdf1b8cb102facf713fc`
- Milestone concept commit: `46ddf9d4bdc514fc56a718a93ad0258a2aa34a4b`
- Intention/execution checkpoint commit: `646f41452c357010550f3fa0ab96147518ddaa4c`
- Occurrence concept commit: `a55fa28b2fb27b1967d18f26b318b173972e35ee`
- Schedule concept commit: `e716e6ad16391f20bd9264c84733dc4f88da4ef8`
- Backend implementation: not started in this branch
- Main modified: no
- Phase 4 prototype branch modified: no
- Current task: `Session` review
- Known documentation conflicts: earlier glossary assumes Goal/Program/Project are distinct and uses narrower Activity/Event/Routine semantics; active Domain Atlas baselines supersede those definitions for this workstream pending deliberate reconciliation after related clusters are stable.
