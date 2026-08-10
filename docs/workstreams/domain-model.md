# Workstream — Core Domain Model v0

- Status: **READY TO START**
- Intended branch: `feature/domain-model` or a bounded sub-scope of `feature/backend-foundation`
- Work type: domain modeling / invariants / persistence preparation

## Purpose

Turn the accepted LifeOS product vocabulary into an implementation-ready domain model without prematurely designing every specialist module or every final SQL table.

## Required reading

1. [`../product/v1-core-domain-glossary.md`](../product/v1-core-domain-glossary.md)
2. [`../product/v1-goal-and-program-lifecycle.md`](../product/v1-goal-and-program-lifecycle.md)
3. [`../product/v1-execution-status.md`](../product/v1-execution-status.md)
4. [`../product/v1-confirmation-and-reminders.md`](../product/v1-confirmation-and-reminders.md)
5. [`../product/v1-scheduling-flexibility.md`](../product/v1-scheduling-flexibility.md)
6. [`../product/v1-data-history-and-privacy.md`](../product/v1-data-history-and-privacy.md)
7. [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md)
8. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
9. [`../decisions/ADR-003-primary-database.md`](../decisions/ADR-003-primary-database.md)
10. [`../decisions/ADR-006-hybrid-personal-data-model.md`](../decisions/ADR-006-hybrid-personal-data-model.md)

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

## Handoff maintenance

Once modeling begins, record the last validated commit/document revision, resolved decisions, unresolved questions and the next exact modeling task here.
