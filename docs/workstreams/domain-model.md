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
4. [`../domain/concepts/goal.md`](../domain/concepts/goal.md)
5. [`../domain/concepts/plan.md`](../domain/concepts/plan.md)
6. [`../domain/concepts/activity.md`](../domain/concepts/activity.md)
7. [`../domain/concepts/event.md`](../domain/concepts/event.md)
8. [`../domain/concepts/routine.md`](../domain/concepts/routine.md)
9. [`../domain/concepts/milestone.md`](../domain/concepts/milestone.md)
10. [`../product/v1-core-domain-glossary.md`](../product/v1-core-domain-glossary.md)
11. [`../product/v1-goal-and-program-lifecycle.md`](../product/v1-goal-and-program-lifecycle.md)
12. [`../product/v1-execution-status.md`](../product/v1-execution-status.md)
13. [`../product/v1-confirmation-and-reminders.md`](../product/v1-confirmation-and-reminders.md)
14. [`../product/v1-scheduling-flexibility.md`](../product/v1-scheduling-flexibility.md)
15. [`../product/v1-data-history-and-privacy.md`](../product/v1-data-history-and-privacy.md)
16. [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md)
17. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
18. [`../decisions/ADR-003-primary-database.md`](../decisions/ADR-003-primary-database.md)
19. [`../decisions/ADR-006-hybrid-personal-data-model.md`](../decisions/ADR-006-hybrid-personal-data-model.md)

## Where to work

The current work is a clearly separated documentation/modeling slice, so it is running on `feature/domain-model` without backend implementation changes.

When persistence mapping and backend package boundaries begin to overlap materially with Backend Foundation, the branches/workstreams must be synchronized deliberately before implementation. Do not run two branches against the same implementation/domain files merely to make the workstreams look separate on paper.

The Domain Model handoff remains separate so decisions and unresolved questions can be resumed independently by another agent.

## Concepts expected to be evaluated

The existing vocabulary includes or strongly suggests:

- User / Workspace;
- Goal;
- Plan;
- Program;
- Project;
- Activity / Task;
- Event;
- Routine;
- Reminder;
- Milestone;
- Schedule occurrence / Calendar block;
- Session / Actual result;
- Observation / Evidence;
- Confirmation / provenance / source;
- Register / RegisterEntry / Quantity;
- Asset / Subject;
- Skill / skill state;
- Requirement / Capability;
- Dependency;
- semantic Relation;
- Version / Decision / AuditEvent;
- Integration / external record;
- Template / Review Queue / Trigger where justified by V1 sequencing.

This list is modeling input, not an accepted ontology and not a command to create one SQL table per bullet.

## Questions Domain Model v0 must answer

- What is an entity versus a value object or enum/state?
- What is owned directly by a workspace?
- Which relationships are structural invariants and should become explicit relational references?
- Which relationships are personal/emergent and belong to the semantic relation layer?
- Which values require provenance or confirmation state?
- What is planned state versus actual state?
- What changes create a new version versus a normal mutable update?
- What is canonical fact versus derived summary?
- Which flexible properties are appropriate for metadata/JSONB?
- What information must be present for safe deduplication/import?
- What invariants must be enforceable without AI?

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

## Current modeling progress

### Goal v0

- Goal covers outcomes, conditions, changes, and behavioral patterns.
- Evaluation criteria remain conceptually separate from Goal identity.
- Progress is not universally a canonical percentage.
- Temporal target/window does not directly reserve operational calendar time.
- Goal ownership is distinct from optional subject.

Record: [`../domain/concepts/goal.md`](../domain/concepts/goal.md)

### Plan v0

- `Plan` is the current execution-strategy primitive.
- Plan is separate from Goal, Activity, Routine, Schedule, and Actual.
- Plan may exist without an explicit Goal.
- Goal-to-Plan is conceptually many-to-many.
- `Project` and `Program` remain specialization/product-language candidates rather than assumed kernel primitives.

Record: [`../domain/concepts/plan.md`](../domain/concepts/plan.md)

### Activity v0

- `Activity` is the actionable-intention primitive.
- `Task` is a contextual/user-facing form of Activity, not currently a separate primitive.
- Semantic work decomposition is distinct from temporal Session decomposition.
- Estimated effort, scheduled duration, and actual effort are distinct.
- Calendar placement does not transform Activity into Event.
- Activity may exist independently and may contribute to multiple Goals.
- Actuals/Observations from unplanned or differently motivated Activities may become valid Evidence for Goal criteria without rewriting original intent.

Record: [`../domain/concepts/activity.md`](../domain/concepts/activity.md)

### Event v0

- `Event` is occurrence-centred and temporal placement is intrinsic to its meaning.
- Event remains distinct from Activity even when both have exact times.
- Event state, participant response, actual attendance, and Event outcome are separate dimensions.
- Original expectation, current accepted schedule, and actual occurrence are distinct temporal layers.
- Actual start/end may be before, after, or equal to planned start/end; timing deviation is derived.
- Recurring Event occurrence identity must survive one-off rescheduling.

Record: [`../domain/concepts/event.md`](../domain/concepts/event.md)

### Routine v0

- `Routine` is the persistent recurring behavior/execution-policy primitive.
- Routine is distinct from Activity, Event, recurrence rule, concrete Schedule, Goal, Template, and Trigger.
- Recurring Event series remain Event semantics rather than being forced into Routine.
- A recurring task may be presented that way in UI while the domain preserves Routine policy + occurrence + execution history.
- Individual Routine occurrences have identity/history distinct from the Routine policy.
- One-off occurrence changes do not automatically modify the Routine.
- Skip occurrence, pause Routine, and end Routine are distinct semantics.
- Future structural changes must be effective-dated/versionable without rewriting past occurrence meaning.
- Routine may exist without Goal/Plan and may support multiple Goals/Plans.
- Routine may govern a single action or a structured recurring bundle.
- Required recurrence semantics include calendar/wall-clock, elapsed interval, completion-relative, and relation-anchored patterns.
- Routine policy is distinct from concrete scheduling and from Actual execution.
- Adherence/streak are derived rather than universal canonical state.
- Repeated observed behavior does not automatically establish canonical Routine intent.

Record: [`../domain/concepts/routine.md`](../domain/concepts/routine.md)

### Milestone v0

- `Milestone` is accepted as a distinct contextual checkpoint entity after the first cluster checkpoint exposed a real semantic gap.
- Milestone is separate from Goal, GoalCriterion, Activity, Event, Outcome, Deadline, Phase, and Decision Record.
- It represents a meaningful state, achievement, decision, delivery, or transition becoming true within a broader Goal and/or Plan context.
- A Milestone normally requires meaningful Goal/Plan context rather than existing as a context-free standalone objective.
- If a checkpoint acquires independent strategic meaning and its own pursuit, it should be reconsidered as a Goal.
- Activity completion and ordinary Goal thresholds do not automatically create Milestones.
- Target date/window and actual achievement are distinct; reaching before/after target is derived rather than a fundamental state.
- Passing a target does not automatically reach or fail the Milestone.
- Milestones may be reached from Activity/Event outcomes, observations, imports, measurements, decisions, explicit user declaration, or other valid Evidence.
- Readiness/progress toward a Milestone is optional and derived rather than a universal stored percentage.
- Target changes preserve identity/history unless the checkpoint itself is materially redefined or abandoned.

Record: [`../domain/concepts/milestone.md`](../domain/concepts/milestone.md)

## Current conceptual direction

```text
Goal      -> what is wanted
Plan      -> how it is intended to be pursued or organized
Activity  -> what concrete action is intended
Event     -> what occurrence is expected at an intrinsic temporal placement
Routine   -> what recurring behavioral/execution policy is intended
Milestone -> what meaningful contextual checkpoint is expected/reached
Schedule  -> when concrete execution is planned or an occurrence is currently expected
Actual    -> what actually happened
Evidence  -> what supports evaluation
```

Important evidence path required by the model:

```text
Activity / Event / Routine occurrence / Milestone / independent observation
        ↓
Actual / Observation / Outcome / Achievement
        ↓
Evidence
        ├──> Goal criterion A
        └──> Goal criterion B
```

Important temporal distinction required by the model:

```text
Original expectation
        ↓
Schedule/target revisions or occurrence exception
        ↓
Current accepted expectation
        ↓
Actual occurrence / achievement
```

This remains a conceptual model under active review, not a persistence schema.

## Important unresolved questions

- whether `Program` eventually requires formal specialization with distinct invariants;
- whether `Project` remains a product label/view or later proves distinct domain behavior;
- exact Goal/Plan/Routine/Milestone lifecycle state machines;
- exact version-versus-replacement boundaries;
- criterion entity/value-object/persistence model;
- exact composite Activity versus Plan boundary;
- exact composite Routine versus Plan boundary;
- Schedule versus Session versus Occurrence boundaries;
- recurrence materialization, timezone/DST, and completion-relative recurrence mechanics;
- recurring Event versus Routine behavior in deliberately ambiguous life cases;
- Calendar Block / Availability / capacity-reservation semantics;
- Deadline and temporal-constraint semantics;
- exact Event lifecycle/participant/attendance state machines;
- Actual, Observation, Evidence, Outcome, Confirmation, and Provenance boundaries;
- formal relationship semantics, including support, contribution, conflict, dependency, decomposition, Goal-to-Goal effects, and multi-goal execution;
- relation-anchored Routine versus Trigger boundary;
- exact Milestone persistence, lifecycle, dependency, waiver, and GoalCriterion-reference semantics;
- exact Life Area / World / Value model;
- Asset / Subject model;
- persistence/API mapping.

## Checkpoint plan

The first intention/execution checkpoint identified Milestone as one real missing concept. Milestone v0 has now been accepted, so the current task is the **final combined validation pass** for the cluster:

`Goal + Plan + Activity + Event + Routine + Milestone`

The final pass must test all six current baselines against the same representative scenarios and adversarial mixed cases.

It must specifically search for:

- duplicate representations of the same real-world thing;
- inability to distinguish two primitives naturally;
- hidden hierarchy assumptions;
- planned/actual/history leakage;
- recurrence/occurrence identity problems;
- evidence that cannot flow to the correct Goal criteria;
- Activity-versus-Plan and Routine-versus-Plan boundary failures;
- recurring Activity versus recurring Event ambiguity;
- Milestone-versus-Goal, GoalCriterion, Event Outcome, or ordinary progress ambiguity;
- difficult multi-Goal interactions;
- missing primitive candidates that are actually necessary rather than merely traditional labels;
- escape hatches that would require arbitrary JSON or one-off domain tables.

Representative scenarios must be drawn from the existing feature-discovery simulation and supplemented with adversarial mixed cases.

If the final checkpoint exposes a real conflict, reopen the affected current baseline rather than carrying the inconsistency into downstream modeling.

If the final checkpoint passes without reopening a baseline, mark the intention/execution cluster validated and move to the Time cluster beginning with `Occurrence`.

A final whole-domain stress test remains mandatory before broad persistence implementation.

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

## Current task

Run the final intention/execution cluster checkpoint before moving to the temporal cluster.

## Next exact step

Stress-test `Goal + Plan + Activity + Event + Routine + Milestone` together using one consistent scenario matrix drawn from the feature-discovery simulation plus adversarial mixed cases. Record pass/fail/ambiguity for each primitive boundary, reopen any concept that fails, and if the cluster passes, mark it validated and begin `Occurrence` review.

## Handoff

- Active branch: `feature/domain-model`
- PR: none
- Base main commit: `73f0d172de239853e568532535a4739ce77a0877`
- Completed current baselines: `Goal v0`, `Plan v0`, `Activity v0`, `Event v0`, `Routine v0`, `Milestone v0`
- Goal concept commit: `084394ef5523517139335b5e5496aa0e4862c737`
- Plan concept commit: `7a5b9962abb503aa9532daf2acf41af23d699060`
- Activity final concept commit: `f2b2db24bd26684bd58aa925478a1623bf2316fc`
- Event concept commit: `84e460ba31d5b88b1f415d27d8254803358109f4`
- Routine concept commit: `f0de8c241d7650bbdbaffdf1b8cb102facf713fc`
- Milestone concept commit: `46ddf9d4bdc514fc56a718a93ad0258a2aa34a4b`
- Backend implementation: not started in this branch
- Main modified: no
- Phase 4 prototype branch modified: no
- Next task: final intention/execution cluster checkpoint
- Known documentation conflicts: previous glossary assumes Goal/Program/Project are distinct and uses narrower Activity/Event/Routine semantics; active Domain Atlas baselines supersede those definitions for this workstream pending deliberate reconciliation after checkpoint