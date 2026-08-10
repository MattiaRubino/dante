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
8. [`../product/v1-core-domain-glossary.md`](../product/v1-core-domain-glossary.md)
9. [`../product/v1-goal-and-program-lifecycle.md`](../product/v1-goal-and-program-lifecycle.md)
10. [`../product/v1-execution-status.md`](../product/v1-execution-status.md)
11. [`../product/v1-confirmation-and-reminders.md`](../product/v1-confirmation-and-reminders.md)
12. [`../product/v1-scheduling-flexibility.md`](../product/v1-scheduling-flexibility.md)
13. [`../product/v1-data-history-and-privacy.md`](../product/v1-data-history-and-privacy.md)
14. [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md)
15. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
16. [`../decisions/ADR-003-primary-database.md`](../decisions/ADR-003-primary-database.md)
17. [`../decisions/ADR-006-hybrid-personal-data-model.md`](../decisions/ADR-006-hybrid-personal-data-model.md)

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

- Goal reviewed against the existing LifeOS feature-discovery simulation and broader goal patterns.
- Goal definition covers outcomes, conditions, changes, and behavioral patterns.
- Goal evaluation criteria separated conceptually from Goal identity.
- Goal progress rejected as a universally canonical percentage.
- Goal temporal target/window separated from operational calendar occupancy.
- Goal ownership distinguished from optional subject.

Record:

- [`../domain/concepts/goal.md`](../domain/concepts/goal.md)

### Plan v0

- `Plan` is the current execution-strategy primitive: it describes how a purpose is intended to be pursued or organized.
- Plan separated from Goal, Activity, Routine, Schedule, and Actual.
- Plan has persistent identity independent of linked Goals.
- Plan may exist without an explicit Goal to avoid artificial duplicate Goals.
- Goal-to-Plan is conceptually many-to-many.
- Plan may coordinate typed capabilities such as phases, activities, milestones, dependencies, routines, constraints, progression, scheduling policies, and adaptation rules without requiring all of them.
- `Project` is not currently justified as a separate kernel primitive.
- `Program` is not currently accepted as a separate kernel primitive; program-like progression remains a specialization candidate.
- Plan explicitly rejected as an arbitrary metadata/JSON mega-object.

Record:

- [`../domain/concepts/plan.md`](../domain/concepts/plan.md)

### Activity v0

- `Activity` accepted as the actionable-intention primitive between Plan and execution time.
- `Task` is not currently a separate primitive; it is a contextual/user-facing form of Activity for defined work completion.
- Activity separated from Goal, Plan, Event, Routine, Schedule, Session, and Actual.
- Semantic work decomposition (`sub-activity`) separated from temporal execution decomposition (`Session`).
- Estimated effort, scheduled duration, and actual effort separated conceptually.
- Calendar placement does not transform an Activity into an Event.
- Activity may exist without Goal, Plan, Routine, or exact Schedule.
- Activity may intentionally contribute to multiple Goals.
- Goal evaluation is explicitly not limited to Activities originally planned for that Goal.
- Actuals/Observations arising from unrelated or unplanned Activities may become valid evidence for Goal criteria.
- Discovered relevance must not retroactively rewrite the original purpose of an Activity.
- Positive/negative impact is contextual to evidence + criterion + evaluation policy, not an intrinsic Activity property.
- Ambiguous AI-discovered relevance remains proposed/inferred with provenance until user authority or approved policy resolves it; deterministic authorized calculations need not ask redundant confirmations.
- Goal-to-Goal influence was discovered as a real cross-domain requirement and deferred to the formal Relationship Model rather than represented as a generic `influences` field.
- Composite Activity versus Plan remains an explicit checkpoint boundary rather than being resolved through an arbitrary size threshold.

Record:

- [`../domain/concepts/activity.md`](../domain/concepts/activity.md)

### Event v0

- `Event` accepted as the occurrence-centred primitive whose temporal placement is intrinsic to its meaning.
- Event remains distinct from Activity even when both appear at exact times in calendar surfaces.
- Event separated from generic Schedule, Deadline, Milestone, Calendar Block, and Availability.
- Event state, participant response, actual attendance, and Event outcome are separate dimensions.
- Original expectation, current accepted schedule, and actual occurrence are explicitly distinct temporal layers.
- Actual start/end may occur before, after, or exactly at planned start/end; early/late/overrun semantics are derived rather than foundational Event state.
- Passage of scheduled time does not automatically imply completion or attendance.
- Event may contribute directly to Goal criteria through outcome, attendance, observations, measurements, or other valid Evidence.
- Event may have preparation/follow-up Activities without requiring a duplicate `Attend event` Activity.
- All-day and multi-day are temporal Event forms rather than different kernel entities.
- A recurring Event occurrence must preserve identity when individually rescheduled.
- Event recurrence versus Routine remains deliberately open for Routine review.
- Event existence does not automatically imply that its entire interval consumes scheduling capacity; availability/blocking semantics remain for the temporal cluster.
- LifeOS Event identity remains separate from external provider identity.

Record:

- [`../domain/concepts/event.md`](../domain/concepts/event.md)

## Current conceptual direction

```text
Goal      -> what is wanted
Plan      -> how it is intended to be pursued or organized
Activity  -> what concrete action is intended
Event     -> what occurrence is expected at an intrinsic temporal placement
Schedule  -> when concrete execution is planned or an Event is currently expected
Actual    -> what actually happened
Evidence  -> what supports evaluation
```

Important evidence paths now required by the model:

```text
Activity or Event (possibly unrelated to Goal)
        ↓
Actual / Observation / Outcome
        ↓
Evidence
        ├──> Goal criterion A
        └──> Goal criterion B
```

The evidence path may also begin from an unplanned import/observation with no originating Activity or Event.

Important temporal distinction now required by the model:

```text
Original expectation
        ↓
Schedule revisions
        ↓
Current accepted schedule
        ↓
Actual occurrence
```

Actual time may differ in either direction from accepted schedule.

This is a conceptual model under active review, not yet a persistence schema.

## Important unresolved questions

- whether `Program` eventually requires formal specialization with distinct invariants;
- whether `Project` remains a product label/view or later proves distinct domain behavior;
- exact Plan and Goal lifecycle state machines;
- exact version-versus-replacement boundaries;
- criterion entity/value-object/persistence model;
- Routine semantics and generated-occurrence identity;
- Event recurrence versus Routine in ambiguous repeated-life cases;
- exact composite Activity versus Plan boundary;
- Schedule versus Session versus Occurrence boundaries;
- Calendar Block / Availability / capacity-reservation semantics;
- Deadline and temporal-constraint semantics;
- exact Event lifecycle/participant/attendance state machines;
- Actual, Observation, Evidence, Outcome, Confirmation, and Provenance boundaries;
- formal relationship semantics, including support, contribution, conflict, dependency, decomposition, Goal-to-Goal effects, and multi-goal execution;
- Milestone semantics;
- exact Life Area / World / Value model;
- Asset / Subject model;
- persistence/API mapping.

## Checkpoint plan

Do not wait until the complete Domain Atlas is finished to test coherence.

The first intended cluster checkpoint is the **intention/execution cluster**, after enough adjacent concepts are reviewed to test Goal + Plan + Activity + Event together with Routine and any required Milestone semantics.

At that checkpoint, rebuild representative scenarios from the feature-discovery simulation and add difficult cross-domain cases, including Activities/Events that unexpectedly affect multiple Goals and Goal interactions that create support or conflict.

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

`Workspace → Goal/Plan → Activity/Event → Schedule → Actual/Confirmation`

This remains a working implementation target, not a final persistence schema. Concepts in the sequence must each be validated before implementation.

## Current task

Continue the Domain Atlas one concept at a time. Do not begin broad SQL or backend implementation while core conceptual boundaries remain under review.

## Next exact step

Review `Routine` using the mandatory internal-documentation + simulation + external-benchmark + stress-test method.

Routine should specifically test recurring behavioral rules, generation versus identity of occurrences, pause/revision/exceptions, relation to Plan/Goal/Activity, and the boundary with recurring Events. Do not assume that recurrence alone makes something a Routine.

## Handoff

- Active branch: `feature/domain-model`
- PR: none
- Base main commit: `73f0d172de239853e568532535a4739ce77a0877`
- Completed current baselines: `Goal v0`, `Plan v0`, `Activity v0`, `Event v0`
- Goal concept commit: `084394ef5523517139335b5e5496aa0e4862c737`
- Plan concept commit: `7a5b9962abb503aa9532daf2acf41af23d699060`
- Activity final concept commit: `f2b2db24bd26684bd58aa925478a1623bf2316fc`
- Event concept commit: `84e460ba31d5b88b1f415d27d8254803358109f4`
- Backend implementation: not started in this branch
- Main modified: no
- Phase 4 prototype branch modified: no
- Known documentation conflicts: previous glossary assumes Goal/Program/Project are distinct and uses narrower Activity/Event semantics; active Domain Atlas now uses Goal + Plan + Activity + Event as the current baselines while Project/Program remain specialization candidates pending evidence