# Workstream — Core Domain Model v0

- Status: **READY TO START**
- Preferred initial execution: bounded sub-scope of `feature/backend-foundation`
- Separate branch later if needed: `feature/domain-model`
- Work type: domain modeling / invariants / persistence preparation

## Purpose

Turn the accepted LifeOS product vocabulary into an implementation-ready domain model without prematurely designing every specialist module or every final SQL table.

## Required reading

1. [`../PROJECT-STATUS.md`](../PROJECT-STATUS.md)
2. [`../development/operating-rules.md`](../development/operating-rules.md)
3. [`../product/v1-core-domain-glossary.md`](../product/v1-core-domain-glossary.md)
4. [`../product/v1-goal-and-program-lifecycle.md`](../product/v1-goal-and-program-lifecycle.md)
5. [`../product/v1-execution-status.md`](../product/v1-execution-status.md)
6. [`../product/v1-confirmation-and-reminders.md`](../product/v1-confirmation-and-reminders.md)
7. [`../product/v1-scheduling-flexibility.md`](../product/v1-scheduling-flexibility.md)
8. [`../product/v1-data-history-and-privacy.md`](../product/v1-data-history-and-privacy.md)
9. [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md)
10. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
11. [`../decisions/ADR-003-primary-database.md`](../decisions/ADR-003-primary-database.md)
12. [`../decisions/ADR-006-hybrid-personal-data-model.md`](../decisions/ADR-006-hybrid-personal-data-model.md)

## Where to work

Because Domain Model v0 and Backend Foundation will initially touch the same package boundaries, persistence mapping and tests, the default is to develop Domain Model v0 **inside `feature/backend-foundation` first**.

Open a separate `feature/domain-model` branch only when:

- Backend Foundation has merged and Domain Model work continues independently; or
- there is a clearly separated documentation/modeling slice that will not edit the same implementation files in parallel.

Do not run two branches against the same domain files merely to make the workstreams look separate on paper.

The Domain Model handoff remains separate even when the code lives on the Backend Foundation branch, so its decisions/questions can be resumed independently.

## Concepts expected to be evaluated

The accepted vocabulary includes or strongly suggests:

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

This list is a modeling input, not a command to create one SQL table per bullet.

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

- Do not model one table per life topic (`english`, `photography`, `farming`, etc.).
- Do not collapse everything into one `entities` table or arbitrary JSON blob.
- Do not treat AI inference as confirmed truth.
- Keep operational policy separate from domain/topic type where behavior differs by user/program.
- Preserve planned/actual/history distinctions.
- Prefer progressive formalization: generic first when genuinely unpredictable; promote repeated/query-heavy concepts through reviewed migrations.
- Do not reopen the accepted hybrid data architecture merely because a first implementation mapping is inconvenient; propose a deliberate ADR change only with strong new evidence.

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

The model should become concrete enough to implement:

`Workspace → Goal/Program → Activity → Schedule → Actual/Confirmation`

without requiring completion of every domain extension.

## Next exact step

When Backend Foundation starts, mark this workstream **IN PROGRESS** on the same branch and begin with a conceptual/invariant pass before broad SQL mapping.

## Handoff maintenance

Once modeling begins, record:

- actual branch/PR being used;
- last validated commit/document revision;
- resolved decisions;
- unresolved questions;
- current modeling task;
- next exact modeling task.
