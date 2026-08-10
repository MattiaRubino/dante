# Workstream — Core Domain Model v0

- Status: **IN PROGRESS**
- Active branch: `feature/domain-model`
- Base: `main` at `73f0d172de239853e568532535a4739ce77a0877`
- PR: none yet
- Work type: domain modeling / invariants / persistence preparation
- Current execution mode: documentation/modeling slice independent from backend implementation

## Purpose

Turn the LifeOS product vocabulary and requirements into an implementation-ready domain model without prematurely designing every specialist module or every final SQL table.

This pass explicitly revalidates earlier concepts instead of treating prior documentation as automatically correct. Earlier product definitions remain valuable inputs, but a concept can be revised when broader scenario coverage, stronger reasoning, or implementation constraints reveal a better model.

## Current decision rule

**Accepted means current best decision, not immutable decision.**

Decisions may be reopened when new evidence, edge cases, contradictions, or better abstractions emerge. Changes must be explicit, reasoned, and preserved in history rather than silently rewriting prior assumptions.

The active modeling method and concept records live in [`../domain/README.md`](../domain/README.md).

## Required reading

1. [`../PROJECT-STATUS.md`](../PROJECT-STATUS.md)
2. [`../development/operating-rules.md`](../development/operating-rules.md)
3. [`../domain/README.md`](../domain/README.md)
4. [`../domain/concepts/goal.md`](../domain/concepts/goal.md)
5. [`../domain/concepts/plan.md`](../domain/concepts/plan.md)
6. [`../product/v1-core-domain-glossary.md`](../product/v1-core-domain-glossary.md)
7. [`../product/v1-goal-and-program-lifecycle.md`](../product/v1-goal-and-program-lifecycle.md)
8. [`../product/v1-execution-status.md`](../product/v1-execution-status.md)
9. [`../product/v1-confirmation-and-reminders.md`](../product/v1-confirmation-and-reminders.md)
10. [`../product/v1-scheduling-flexibility.md`](../product/v1-scheduling-flexibility.md)
11. [`../product/v1-data-history-and-privacy.md`](../product/v1-data-history-and-privacy.md)
12. [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md)
13. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
14. [`../decisions/ADR-003-primary-database.md`](../decisions/ADR-003-primary-database.md)
15. [`../decisions/ADR-006-hybrid-personal-data-model.md`](../decisions/ADR-006-hybrid-personal-data-model.md)

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
- Actual session/result;
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

This list is a modeling input, not an accepted ontology and not a command to create one SQL table per bullet.

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
- Do not model one table per life topic (`english`, `photography`, `farming`, etc.).
- Do not collapse everything into one `entities` table or arbitrary JSON blob.
- Do not treat AI inference as confirmed truth.
- Keep operational policy separate from domain/topic type where behavior differs by user/plan.
- Preserve planned/actual/history distinctions.
- Prefer progressive formalization: generic first when genuinely unpredictable; promote repeated/query-heavy concepts through reviewed migrations.
- Do not reopen an accepted architectural ADR merely because a first implementation mapping is inconvenient; propose an explicit ADR change when new evidence genuinely challenges the architecture.
- Preserve earlier documents while conflicts are being revalidated; propagate replacements deliberately after related concepts are understood.

## Current modeling progress

### Completed current baselines

#### Goal v0

- Goal reviewed against the existing LifeOS feature-discovery simulation and broader goal patterns.
- Goal definition broadened to cover outcomes, conditions, changes, and behavioral patterns.
- Goal evaluation criteria separated conceptually from Goal identity.
- Goal progress rejected as a universally canonical percentage.
- Goal temporal target/window separated from operational calendar occupancy.
- Goal ownership distinguished from optional subject.

Current record:

- [`../domain/concepts/goal.md`](../domain/concepts/goal.md)

#### Plan v0

- `Plan` introduced as the current execution-strategy primitive: it describes how a purpose is intended to be pursued or organized.
- Plan separated from Goal, Activity, Routine, Schedule, and Actual.
- Plan given persistent identity independent of linked Goals.
- Plan allowed to exist without an explicit Goal to avoid artificial duplicate Goals.
- Goal↔Plan treated conceptually as many-to-many.
- Plan may coordinate typed capabilities such as phases, activities, milestones, dependencies, routines, constraints, progression, scheduling policies, and adaptation rules without requiring all of them.
- `Project` is not currently justified as a separate kernel primitive.
- `Program` is not currently accepted as a separate kernel primitive; program-like progression remains a specialization candidate to be tested later.
- Project-like, program-like, and hybrid plans are all representable without a premature `PROJECT | PROGRAM` kernel enum.
- Plan explicitly rejected as an arbitrary metadata/JSON mega-object.

Current record:

- [`../domain/concepts/plan.md`](../domain/concepts/plan.md)

### Current conceptual direction

```text
Goal      -> what is wanted
Plan      -> how it is intended to be pursued or organized
Activity  -> what concrete action is intended
Schedule  -> when concrete execution is planned
Actual    -> what actually happened
Evidence  -> what supports evaluation
```

This is a conceptual model under active review, not yet a persistence schema.

### Important unresolved questions

- whether `Program` eventually requires a formal specialization with distinct invariants;
- whether `Project` remains a product label/view or later proves distinct domain behavior;
- exact Plan and Goal lifecycle state machines;
- exact version-versus-replacement boundaries;
- criterion entity/value-object/persistence model;
- relationship semantics such as support, contribution, decomposition, and multi-goal execution;
- exact Activity/Task boundary;
- Routine semantics relative to generated occurrences and Plans;
- Milestone semantics;
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

`Workspace → Goal/Plan → Activity → Schedule → Actual/Confirmation`

This is still a working implementation target, not a final persistence schema. The concepts in the sequence must each be validated before implementation.

## Current task

Continue the Domain Atlas one concept at a time. Do not begin broad SQL or backend implementation while the core conceptual boundaries are still under review.

## Next exact step

Select the next domain concept with the user and review it with the same definition/invariants/alternatives/stress-test method used for Goal and Plan.

Given the accepted Goal/Plan split, `Activity / Task` is a strong next candidate because it defines the executable unit that sits between Plan and Schedule. `Routine`, `Milestone`, and formal Program specialization remain nearby candidates, but none is pre-decided.

## Handoff

- Active branch: `feature/domain-model`
- PR: none
- Base main commit: `73f0d172de239853e568532535a4739ce77a0877`
- Last completed concepts: `Goal v0`, `Plan v0`
- Goal concept commit: `084394ef5523517139335b5e5496aa0e4862c737`
- Plan concept commit: `7a5b9962abb503aa9532daf2acf41af23d699060`
- Backend implementation: not started in this branch
- Main modified: no
- Phase 4 prototype branch modified: no
- Known documentation conflict: previous canonical glossary assumes Goal/Program/Project are distinct; active Domain Atlas now uses Goal + Plan as the current baseline and leaves Project/Program as specialization candidates pending further evidence