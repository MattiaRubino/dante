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
4. [`../product/v1-core-domain-glossary.md`](../product/v1-core-domain-glossary.md)
5. [`../product/v1-goal-and-program-lifecycle.md`](../product/v1-goal-and-program-lifecycle.md)
6. [`../product/v1-execution-status.md`](../product/v1-execution-status.md)
7. [`../product/v1-confirmation-and-reminders.md`](../product/v1-confirmation-and-reminders.md)
8. [`../product/v1-scheduling-flexibility.md`](../product/v1-scheduling-flexibility.md)
9. [`../product/v1-data-history-and-privacy.md`](../product/v1-data-history-and-privacy.md)
10. [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md)
11. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
12. [`../decisions/ADR-003-primary-database.md`](../decisions/ADR-003-primary-database.md)
13. [`../decisions/ADR-006-hybrid-personal-data-model.md`](../decisions/ADR-006-hybrid-personal-data-model.md)

## Where to work

The current work is a clearly separated documentation/modeling slice, so it is running on `feature/domain-model` without backend implementation changes.

When persistence mapping and backend package boundaries begin to overlap materially with Backend Foundation, the branches/workstreams must be synchronized deliberately before implementation. Do not run two branches against the same implementation/domain files merely to make the workstreams look separate on paper.

The Domain Model handoff remains separate so decisions and unresolved questions can be resumed independently by another agent.

## Concepts expected to be evaluated

The existing vocabulary includes or strongly suggests:

- User / Workspace;
- Goal;
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
- Keep operational policy separate from domain/topic type where behavior differs by user/program.
- Preserve planned/actual/history distinctions.
- Prefer progressive formalization: generic first when genuinely unpredictable; promote repeated/query-heavy concepts through reviewed migrations.
- Do not reopen an accepted architectural ADR merely because a first implementation mapping is inconvenient; propose an explicit ADR change when new evidence genuinely challenges the architecture.
- Preserve earlier documents while conflicts are being revalidated; propagate replacements deliberately after related concepts are understood.

## Current modeling progress

### Completed current baseline

- Domain Atlas working method established.
- `Goal v0` reviewed against the existing LifeOS feature-discovery simulation and broader goal patterns.
- Goal definition broadened to cover outcomes, conditions, changes, and behavioral patterns.
- Goal evaluation criteria separated conceptually from Goal identity.
- Goal progress rejected as a universally canonical percentage.
- Goal temporal target/window separated from operational calendar occupancy.
- Goal ownership distinguished from optional subject.
- `Project` as an independent primitive explicitly reopened for revalidation instead of inherited automatically from the previous glossary.

Current concept record:

- [`../domain/concepts/goal.md`](../domain/concepts/goal.md)

### Important unresolved questions

- whether `Project` is an independent domain entity or an execution structure/presentation over other primitives;
- exact `Program` semantics;
- exact Goal lifecycle and versioning boundaries;
- criterion entity/value-object/persistence model;
- relationship semantics such as support, contribution, decomposition, and multi-goal execution;
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

`Workspace → Goal/Program → Activity → Schedule → Actual/Confirmation`

This sequence is still a working implementation target, not proof that every named concept is already modeled correctly. In particular, Program and adjacent execution structures must be revalidated before implementation.

## Current task

Continue the Domain Atlas one concept at a time. Do not begin broad SQL or backend implementation while the core conceptual boundaries are still under review.

## Next exact step

Select the next domain concept with the user, review it with the same definition/invariants/alternatives/stress-test method used for Goal, and save it only after agreement. The `Program` / `Project` boundary is a likely next area because it directly depends on the newly accepted Goal semantics, but it is not pre-decided.

## Handoff

- Active branch: `feature/domain-model`
- PR: none
- Base main commit: `73f0d172de239853e568532535a4739ce77a0877`
- Last completed concept: `Goal v0`
- Last concept document commit before this handoff update: `084394ef5523517139335b5e5496aa0e4862c737`
- Backend implementation: not started in this branch
- Main modified: no
- Phase 4 prototype branch modified: no
- Known documentation conflict: previous canonical glossary assumes Goal/Program/Project are distinct; Project is now explicitly pending revalidation
