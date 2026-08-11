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
13. [`../domain/concepts/session.md`](../domain/concepts/session.md)
14. [`../product/v1-core-domain-glossary.md`](../product/v1-core-domain-glossary.md)
15. [`../product/v1-goal-and-program-lifecycle.md`](../product/v1-goal-and-program-lifecycle.md)
16. [`../product/v1-execution-status.md`](../product/v1-execution-status.md)
17. [`../product/v1-confirmation-and-reminders.md`](../product/v1-confirmation-and-reminders.md)
18. [`../product/v1-scheduling-flexibility.md`](../product/v1-scheduling-flexibility.md)
19. [`../product/v1-data-history-and-privacy.md`](../product/v1-data-history-and-privacy.md)
20. [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md)
21. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
22. [`../decisions/ADR-003-primary-database.md`](../decisions/ADR-003-primary-database.md)
23. [`../decisions/ADR-006-hybrid-personal-data-model.md`](../decisions/ADR-006-hybrid-personal-data-model.md)

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
→ Session v0 — accepted
→ Deadline / Window / Temporal Constraint — current review target
→ Recurrence
→ Calendar Block / Availability / Capacity
```

The order may change when a concept reveals a stronger dependency.

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

## Current task — Deadline / Window / Temporal Constraint

Review the temporal constraint family before proceeding to Recurrence.

The review must determine at minimum:

- whether `Deadline` should be a distinct entity/value-object or a specialized temporal constraint;
- whether `Window` is one concept or several semantics such as valid window, preferred window, target window, and availability window;
- how hard versus soft temporal constraints are represented;
- the boundary between **accepted Schedule placement** and **allowed/preferred temporal space**;
- earliest-start, latest-start, latest-finish, date-range, exact-boundary, and relative-boundary semantics;
- whether a deadline means latest start, latest completion, delivery time, or another typed boundary;
- target date versus hard deadline versus review date versus Milestone target;
- whether passing a deadline changes canonical state or only creates a derived violation/miss until Actual/Outcome rules decide the result;
- how hard windows constrain replanning and whether execution outside them is invalid, late, overridden, or requires explicit user authority;
- how preferred windows influence scheduling without becoming hard constraints;
- how constraints can attach to Activity, Event, Occurrence, Routine, Plan, Goal, or Milestone without forcing all concepts to own generic date fields;
- how temporal constraints compose when several apply simultaneously;
- how conflicting constraints are surfaced and how AI proposals respect authority;
- whether constraint revisions require effective dating/history;
- date-only, floating, named-zone, and absolute-instant boundary semantics;
- interaction with recurrence without prematurely embedding recurrence inside constraints;
- how temporal constraints differ from Calendar Block / Availability / Capacity.

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
Session    -> which actual execution episode happened
Constraint -> where/when execution is allowed, required, or preferred (under review)
Actual     -> broader truth about what happened
Evidence   -> what supports evaluation
```

Important temporal separation now required:

```text
Temporal intent / rule
        ↓
Constraint(s): what time is allowed/required/preferred
        ↓
Schedule: what time is currently accepted
        ↓
Session / Event Actual: what time actually happened
        ↓
Outcome / Evidence later
```

## Important unresolved questions

- exact Deadline / Window / Temporal Constraint taxonomy;
- exact hard/soft constraint semantics and override authority;
- target date versus deadline versus review date;
- temporal constraint composition/conflict rules;
- relation of temporal constraints to lifecycle/missed/expired outcomes;
- exact Session state/lifecycle and pause persistence;
- exact Schedule planned-placement/revision persistence;
- exact Occurrence identity/materialization SQL representation;
- Recurrence materialization, timezone/DST, travel, and completion-relative mechanics;
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
- Completed current baselines: `Goal v0`, `Plan v0`, `Activity v0`, `Event v0`, `Routine v0`, `Milestone v0`, `Occurrence v0`, `Schedule v0`, `Session v0`
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
- Backend implementation: not started in this branch
- Main modified: no
- Phase 4 prototype branch modified: no
- Current task: `Deadline / Window / Temporal Constraint` review
- Known documentation conflicts: earlier glossary assumes Goal/Program/Project are distinct and uses narrower Activity/Event/Routine semantics; active Domain Atlas baselines supersede those definitions for this workstream pending deliberate reconciliation after related clusters are stable.
