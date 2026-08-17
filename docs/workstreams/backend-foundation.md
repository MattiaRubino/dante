# Workstream — Backend Foundation

- Status: **NOT STARTED / DEFERRED — current handoff cleaned for future execution**
- Intended future branch: `feature/backend-foundation` only after prerequisites are satisfied and a fresh branch/write gate is approved
- Current base: **none** — no backend implementation branch is authorized yet
- Work type: future production technical foundation

## Purpose

Provide the future production backend skeleton for LifeOS **after** the accepted semantic, Physical and runtime/security/integration prerequisites exist.

This handoff is intentionally executable only in the future. It must not be used to bypass the active Pre-Physical workstream, invent Domain semantics, select Physical persistence by implementation convenience, or start backend code before the required gates are closed.

## Current stage boundary

```text
Core Domain Model / Domain Atlas
CLOSED

Logical Model
CLOSED

Pre-Physical Repository & Architecture Coherence
IN PROGRESS

Physical Model
NOT STARTED / NOT AUTHORIZED

Backend Foundation / production implementation
NOT STARTED / DEFERRED
```

Backend Foundation does **not** own Domain or Logical modeling. The old instruction to develop `Domain Model v0` inside Backend Foundation is superseded.

## Prerequisites before this workstream may become READY TO START

All of the following must be true before a backend implementation branch is created:

1. Pre-Physical Repository & Architecture Coherence is closed with clean-room QA PASS;
2. the user has separately authorized and accepted the Physical Model workstream/result;
3. accepted Physical persistence/runtime boundaries exist for the implementation being started;
4. current AuthN/AuthZ, security/privacy/retention/recovery and consistency/side-effect requirements that constrain implementation are accepted;
5. current AI/context/runtime/integration boundaries are accepted where the first implementation slice touches them;
6. the governed API/command/effect contract is accepted before concrete consequential routes are stabilized;
7. repository engineering safety/CI requirements needed before production backend work are in place;
8. current `main` and all active current-specification sources are re-read immediately before the new branch/write gate.

Until these conditions are satisfied:

```text
DO NOT create feature/backend-foundation
DO NOT create SQL/schema/migrations
DO NOT stabilize concrete API routes/DTOs
DO NOT select persistence by convenience
DO NOT implement AuthN/AuthZ/provider/runtime mechanisms implicitly
```

## Required reading before future implementation

Read current sources, including complete canonical split/continuation chains where applicable:

1. root [`../../README.md`](../../README.md);
2. [`../README.md`](../README.md);
3. [`../PROJECT-STATUS.md`](../PROJECT-STATUS.md);
4. [`../development/agent-operating-manual.md`](../development/agent-operating-manual.md);
5. [`../development/operating-rules.md`](../development/operating-rules.md);
6. [`../development/documentation-and-handoff.md`](../development/documentation-and-handoff.md);
7. [`../development/branching-and-environments.md`](../development/branching-and-environments.md);
8. current [`../architecture/pre-physical-architecture-baseline.md`](../architecture/pre-physical-architecture-baseline.md), [`../architecture/README.md`](../architecture/README.md), [`../architecture/system-overview.md`](../architecture/system-overview.md) and [`../architecture/technical-decisions.md`](../architecture/technical-decisions.md);
9. the complete accepted Domain Atlas beginning at [`../domain/README.md`](../domain/README.md), including its canonical continuation parts where required;
10. the closed Whole Logical Model at [`../logical-model/whole-logical-model-v1.md`](../logical-model/whole-logical-model-v1.md), its complete decision/assumption-register chain, and closure evidence [`../logical-model/checkpoints/whole-logical-v1-remote-qa.md`](../logical-model/checkpoints/whole-logical-v1-remote-qa.md);
11. the then-current accepted Physical Model sources and closure evidence, once they exist;
12. the then-current accepted security/runtime/integration/API contracts relevant to the first slice;
13. current ADRs under [`../decisions/`](../decisions/), using their current qualification/supersession status rather than historical labels.

Older product documents such as `v1-core-domain-glossary.md`, `v1-execution-status.md` and `v1-data-history-and-privacy.md` may remain useful **product evidence/requirements input**. They do not override the accepted Domain Atlas, closed Logical Model, later Physical Model or current architecture contracts.

## Current technical direction to preserve

Unless separately reviewed through the normal decision process:

- backend language/framework direction: Python + FastAPI + Pydantic;
- architecture direction: modular monolith first;
- domain/application logic remains independent from FastAPI request handling;
- clients use governed backend contracts and do not connect directly to primary persistence;
- AI remains behind replaceable/provider-neutral boundaries and may not bypass accepted validation/governance;
- Storage remains behind a provider abstraction;
- provider/external state remains distinct from canonical LifeOS state;
- DEV/UAT/PROD are deployment environments, not permanent Git branches;
- accepted Domain + Logical semantics, including `WL-H01..WL-H12`, are implementation constraints rather than suggestions;
- the current Pre-Physical Architecture Baseline is a mandatory downstream bridge and does not itself authorize implementation.

## Physical-dependent implementation candidates

The following are **not current architecture commitments** and may be adopted only if the accepted Physical Model justifies them:

- SQLAlchemy;
- Alembic;
- PostgreSQL-specific local development configuration;
- relational migration mechanics;
- concrete transaction/isolation/version-token mechanisms;
- table/index/key/partition strategy;
- database-specific test fixtures or operational tooling.

Current posture before Physical authorization remains:

```text
PostgreSQL hybrid
preferred Physical benchmark baseline — not selected

TypeDB
mandatory challenger

Neo4j / property graph
serious secondary/read-projection candidate

event/document mechanisms
bounded candidates

generic EAV / generic edge / universal meta-model
hard reject for canonical kernel
```

## Runtime/API-dependent implementation candidates

Do not freeze these before their accepted prerequisite contracts exist:

- versioned concrete API route/DTO surface;
- AuthN/AuthZ middleware, policy engine or persistence;
- idempotency storage and replay mechanics;
- transactional outbox/inbox/publication mechanics;
- workflow/automation execution engine;
- notification delivery runtime;
- Integration Hub provider adapters;
- AI tool/action adapters;
- projection/cache/search infrastructure;
- observability implementation details that could expose sensitive data.

A UI button, HTTP route or technical AuthZ action string is not the canonical semantic operation. Consequential backend effects must preserve the governed operation/effect contract and the applicable expected-state, provenance, disclosure, freshness and consistency requirements.

## Future bootstrap deliverables — implementation-independent core

When this workstream is actually authorized, likely foundation deliverables include:

- Python project/package structure;
- FastAPI application bootstrap;
- Pydantic settings/configuration;
- modular-monolith package boundaries;
- pytest baseline;
- dependency/configuration separation with no hard-coded secrets;
- domain/application logic testability without FastAPI request handling;
- error-handling baseline;
- structured logging baseline compatible with privacy/minimization requirements;
- development health/readiness endpoint where appropriate;
- provider-neutral interfaces only where the corresponding accepted contract already exists;
- clear separation among API, application, domain/logical translation, persistence and provider/runtime concerns.

Physical-specific bootstrap deliverables are added only after Physical acceptance. Runtime/provider-specific deliverables are added only after their prerequisite contracts are accepted.

## First implementation slice rule

There is **no fixed canonical first vertical slice in this handoff today**.

The old target:

```text
Workspace → Goal/Program → Activity → Schedule → Actual/Confirmation
```

is superseded as a backend/domain contract. `Workspace` is not an accepted universal Domain owner, while `Project`/`Program` product vocabulary maps to accepted semantics such as a `Plan` profile according to the actual case rather than manufacturing new kernel roots.

When backend implementation is eventually authorized, the first slice must be chosen from the accepted Domain + Logical + Physical + runtime/API contracts and current product need. It should be narrow enough to validate the architecture end to end without using product labels as an ontology shortcut.

## Future tests / validation baseline

When applicable to the accepted implementation design, validate at minimum:

- application starts in the intended development environment;
- configuration/secrets are externalized appropriately;
- unit tests run independently of production providers;
- critical domain/application logic is testable without HTTP handling;
- API/persistence/provider layers do not become the Domain Model;
- accepted expected-state/conflict semantics are testable for consequential mutations;
- provider partial failure/divergence is represented truthfully where relevant;
- history/provenance/correction requirements survive persistence translation;
- selective disclosure and inference-leakage constraints are tested where the slice exposes governed data;
- migrations/rollback are tested **only if** the accepted Physical implementation uses migration-based persistence;
- database connectivity/config tests are added **only for** the accepted Physical persistence;
- required CI/repository checks pass before integration.

## Non-negotiable semantic/runtime guardrails

Future implementation must preserve at least:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority

provider state != canonical LifeOS state
derived projection != canonical truth
absence/unknown != false
idempotency != identity
HTTP route / UI button / AuthZ action string != canonical governed effect
```

And all `WL-H01..WL-H12` remain active downstream constraints.

## Where to work when eventually authorized

Do **not** create the implementation branch now.

When all prerequisites are satisfied:

1. re-read current `main` and this handoff;
2. verify all required current split/continuation documents in full;
3. define the exact backend implementation scope and path ownership;
4. present a fresh branch/PRE-SCOPE/CREATE-UPDATE-DELETE gate;
5. only after explicit approval, create the bounded implementation branch from current `main`;
6. update this handoff to **IN PROGRESS** with actual branch, PRE-SCOPE, scope, package paths and validation commands.

## Handoff maintenance after implementation starts

Record at least:

- actual branch and PR;
- implementation PRE-SCOPE;
- exact approved path scope;
- last validated commit;
- actual package/file paths;
- commands to run/test/migrate where applicable;
- accepted Physical/runtime dependencies used by the implementation;
- completed tasks;
- current task;
- known issues/risks;
- validation evidence;
- next exact steps.

Do not update `PROJECT-STATUS.md` for every backend commit. Update global status only when the workstream actually starts, blocks, reaches an integrated milestone, changes branch/PR or finishes.

## Current exact next step

```text
BACKEND FOUNDATION
NO IMPLEMENTATION ACTION

CURRENT PROJECT ACTION
continue Pre-Physical Coherence

NEXT PRE-PHYSICAL PHASE
Phase 5 — Requirements That Can Constrain Physical Design
```
