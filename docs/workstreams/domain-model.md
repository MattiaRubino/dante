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

The active modeling method and mandatory concept-review protocol live in [`../domain/README.md`](../domain/README.md).

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
11. [`../product/v1-core-domain-glossary.md`](../product/v1-core-domain-glossary.md)
12. [`../product/v1-goal-and-program-lifecycle.md`](../product/v1-goal-and-program-lifecycle.md)
13. [`../product/v1-execution-status.md`](../product/v1-execution-status.md)
14. [`../product/v1-confirmation-and-reminders.md`](../product/v1-confirmation-and-reminders.md)
15. [`../product/v1-scheduling-flexibility.md`](../product/v1-scheduling-flexibility.md)
16. [`../product/v1-data-history-and-privacy.md`](../product/v1-data-history-and-privacy.md)
17. [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md)
18. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
19. [`../decisions/ADR-003-primary-database.md`](../decisions/ADR-003-primary-database.md)
20. [`../decisions/ADR-006-hybrid-personal-data-model.md`](../decisions/ADR-006-hybrid-personal-data-model.md)

## Where to work

The current work is a clearly separated documentation/modeling slice, so it is running on `feature/domain-model` without backend implementation changes.

When persistence mapping and backend package boundaries begin to overlap materially with Backend Foundation, the branches/workstreams must be synchronized deliberately before implementation. Do not run two branches against the same implementation/domain files merely to make the workstreams look separate on paper.

The Domain Model handoff remains separate so decisions and unresolved questions can be resumed independently by another agent.

## Rules

- Revalidate concepts one at a time; do not inherit terminology merely because it already exists.
- For every concept, inspect applicable internal documentation/scenarios and perform enough targeted external benchmarking to expose likely missing semantics before acceptance.
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

### Checkpoint conclusions

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

The workstream now enters the **Time** cluster.

Provisional concepts:

```text
Occurrence
→ Schedule
→ Session
→ Deadline / Window / Temporal Constraint
→ Recurrence
→ Calendar Block / Availability / Capacity
```

The order may change when a concept reveals a stronger dependency.

## Current task — Occurrence

Review `Occurrence` as the first Time-cluster concept.

The review must determine at minimum:

- what an Occurrence is relative to Routine, recurring Event, and possibly generated Activity;
- whether every occurrence is persisted or only occurrences whose identity/history must survive;
- how one occurrence retains identity after rescheduling;
- how original expected placement differs from current accepted Schedule;
- how skip, cancel, postpone, replace, detach, and execute affect occurrence identity;
- whether a one-off Activity scheduled once needs an Occurrence or only a Schedule/Session;
- whether recurring Event instances and Routine-generated expected executions can share one occurrence abstraction without losing their different parent semantics;
- whether occurrence identity exists before materialization;
- how far ahead recurring/generated occurrences should be materialized;
- what belongs to Occurrence versus RecurrenceRule, Schedule, Session, or Actual;
- how occurrence exceptions interact with future-series revisions;
- what time-zone/DST/travel requirements Occurrence imposes without prematurely solving recurrence implementation.

## Current conceptual direction

```text
Goal       -> what is wanted
Plan       -> how it is intended to be pursued or organized
Activity   -> what concrete action is intended
Event      -> what occurrence is expected at an intrinsic temporal placement
Routine    -> what recurring behavioral/execution policy is intended
Milestone  -> what meaningful contextual checkpoint is expected/reached
Occurrence -> individual expected instance identity in a recurring/generated context (under review)
Schedule   -> current planned temporal placement
Actual     -> what actually happened
Evidence   -> what supports evaluation
```

Important temporal distinction already required by accepted concepts:

```text
Original expectation
        ↓
Schedule / target revisions or occurrence exception
        ↓
Current accepted expectation
        ↓
Actual occurrence / achievement
```

Actual time may be earlier, later, shorter, longer, or absent relative to the accepted schedule.

## Important unresolved questions

- exact Occurrence identity/materialization rules;
- exact Schedule versus Occurrence versus Session boundaries;
- recurrence materialization, timezone/DST, travel, and completion-relative recurrence mechanics;
- Calendar Block / Availability / capacity-reservation semantics;
- Deadline and temporal-constraint semantics;
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

`Workspace → Goal/Plan → Activity/Event/Routine/Milestone → Schedule/Occurrence → Actual/Confirmation`

This remains a working implementation target, not a final persistence schema.

## Handoff

- Active branch: `feature/domain-model`
- PR: none
- Base main commit: `73f0d172de239853e568532535a4739ce77a0877`
- Intention & Execution Cluster v0: **PASS / validated current baseline**
- Completed current baselines: `Goal v0`, `Plan v0`, `Activity v0`, `Event v0`, `Routine v0`, `Milestone v0`
- Goal concept commit: `084394ef5523517139335b5e5496aa0e4862c737`
- Plan concept commit: `7a5b9962abb503aa9532daf2acf41af23d699060`
- Activity final concept commit: `f2b2db24bd26684bd58aa925478a1623bf2316fc`
- Event concept commit: `84e460ba31d5b88b1f415d27d8254803358109f4`
- Routine concept commit: `f0de8c241d7650bbdbaffdf1b8cb102facf713fc`
- Milestone concept commit: `46ddf9d4bdc514fc56a718a93ad0258a2aa34a4b`
- Checkpoint commit: `646f41452c357010550f3fa0ab96147518ddaa4c`
- Backend implementation: not started in this branch
- Main modified: no
- Phase 4 prototype branch modified: no
- Current task: `Occurrence` review
- Known documentation conflicts: earlier glossary assumes Goal/Program/Project are distinct and uses narrower Activity/Event/Routine semantics; active Domain Atlas baselines supersede those definitions for this workstream pending deliberate reconciliation after related clusters are stable.
