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
Phase 5 requirements accepted
Phase 6 AI/context/runtime/integration boundaries accepted on active branch after QA

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
4. the current Phase 5 requirement packages for AuthN/AuthZ, security/privacy/retention/recovery, consistency/side effects and non-functional/multi-device/operational recovery are accepted and any implementation-dependent open parameters are resolved at the appropriate later gate;
5. the current Phase 6 AI/context/runtime and Integration Hub boundary contracts are accepted where the first implementation slice touches them;
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
9. the complete current Phase 5 requirement set beginning at [`../architecture/requirements/README.md`](../architecture/requirements/README.md), including all four linked requirement packages;
10. current Phase 6 [`../architecture/ai-context-runtime-boundaries.md`](../architecture/ai-context-runtime-boundaries.md) and [`../architecture/integration-hub-boundaries.md`](../architecture/integration-hub-boundaries.md);
11. the complete accepted Domain Atlas beginning at [`../domain/README.md`](../domain/README.md), including its canonical continuation parts where required;
12. the closed Whole Logical Model at [`../logical-model/whole-logical-model-v1.md`](../logical-model/whole-logical-model-v1.md), its complete decision/assumption-register chain, and closure evidence [`../logical-model/checkpoints/whole-logical-v1-remote-qa.md`](../logical-model/checkpoints/whole-logical-v1-remote-qa.md);
13. the then-current accepted Physical Model sources and closure evidence, once they exist;
14. the then-current accepted durable-workflow/API/search/observability/runtime contracts relevant to the first slice;
15. current ADRs under [`../decisions/`](../decisions/), using their current qualification/supersession status rather than historical labels.

Older product documents such as `v1-core-domain-glossary.md`, `v1-execution-status.md` and `v1-data-history-and-privacy.md` may remain useful **product evidence/requirements input**. They do not override the accepted Domain Atlas, closed Logical Model, later Physical Model or current architecture contracts.

## Current technical direction to preserve

Unless separately reviewed through the normal decision process:

- backend language/framework direction: Python + FastAPI + Pydantic;
- architecture direction: modular monolith first;
- domain/application logic remains independent from FastAPI request handling;
- clients use governed backend contracts and do not connect directly to primary persistence;
- AI remains behind replaceable/provider-neutral boundaries and may not bypass accepted validation/governance;
- AI/context/runtime representation remains distinct from canonical truth, and model output/tool invocation is not an accepted effect by itself;
- Integration Hub flows preserve the five accepted modes and canonical/provider separation;
- Storage remains behind a provider abstraction;
- provider/external state remains distinct from canonical LifeOS state;
- DEV/UAT/PROD are deployment environments, not permanent Git branches;
- accepted Domain + Logical semantics, including `WL-H01..WL-H12`, are implementation constraints rather than suggestions;
- the current Pre-Physical Architecture Baseline, Phase 5 requirements and Phase 6 boundary contracts are mandatory downstream inputs and do not themselves authorize implementation.

## Phase 5 requirements that future implementation must consume

Backend Foundation must implement, test and preserve the accepted requirement contracts rather than choose mechanisms that redefine them.

At minimum:

- AuthN/AuthZ preserves `Person != Account != Principal != Actor`, `Authority != AuthZ decision`, actual Actor vs represented party, consequential AuthZ provenance, non-human Principal governance, delayed-effect governance revalidation and non-interference/disclosure constraints;
- security/privacy supports purpose-aware minimization, secret isolation, sensitive-data handling, category-sensitive retention, truthful deletion/redaction/tombstone semantics, derived/external deletion propagation and secure recovery without forbidden-data resurrection;
- consistency/side effects preserves expected-state semantics, idempotency distinct from identity, no silent material last-write-wins, semantic multi-owner atomicity where required, truthful staged/partial state, canonical/provider separation, ambiguous-failure safety and effect/reconciliation provenance;
- non-functional/multi-device/recovery preserves multi-device divergence, operation-specific offline semantics, truthful degraded/provider state, long-history/current-state access, temporal/DST semantics, safe observability, recovery testing and later accepted RPO/RTO/latency/availability/scale targets.

Open parameters in the Phase 5 packages are future decisions to resolve before the dependent implementation/benchmark; they are not permission to ignore the requirement.

## Phase 6 boundaries that future implementation must consume

### AI / Context / Runtime

Future implementation must preserve:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

The Context Builder is purpose-, disclosure-, provenance- and freshness-aware. Whole-history/full-database exposure is not the default.

LifeOS does not maintain generic `AI memory` as a second canonical truth store. AI output is classified according to its actual role and does not become effective merely because it is structured/high-confidence.

```text
runtime Agent / Principal != Domain Actor automatically
tool invocation != authorization
tool/protocol action != canonical governed operation
```

Non-human Principals, delayed tool effects and external/retrieved instructions remain subject to Phase 5 governance, expected-state, privacy, idempotency and provenance requirements.

### Integration Hub

Future implementation preserves five modes:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

`ExternalRef != NativeRef`; provider revision != `MaterialStateRef`; provider state/effect status != canonical LifeOS state/effect automatically.

Sync direction/conflict handling, live-read freshness, deletion-aware retrieval/index state, callbacks/replay and ambiguous external effects remain explicit bounded contracts rather than provider-driven defaults.

MCP/A2A/future protocols remain adapters and do not redefine LifeOS ontology/governance.

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
- AI provider/model/router and tool/action adapters;
- MCP/A2A/protocol adapters;
- projection/cache/search infrastructure;
- observability implementation details that could expose sensitive data.

A UI button, HTTP route, tool name or technical AuthZ action string is not the canonical semantic operation. Consequential backend effects must preserve the governed operation/effect contract and the applicable expected-state, provenance, disclosure, freshness and consistency requirements.

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

When backend implementation is eventually authorized, the first slice must be chosen from the accepted Domain + Logical + Phase 5 requirements + Phase 6 boundaries + Physical + runtime/API contracts and current product need. It should be narrow enough to validate the architecture end to end without using product labels as an ontology shortcut.

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
- applicable Phase 5 open parameters have been resolved rather than silently defaulted;
- AI/context tests preserve context-category/provenance/freshness/disclosure boundaries where applicable;
- tool/agent callers cannot bypass governance and retrieved content cannot self-authorize effects;
- integration tests distinguish canonical/provider state, duplicate callbacks, unknown external outcomes and reconciliation;
- recovery/degraded/multi-device tests appropriate to the slice exercise the accepted requirement contracts;
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
HTTP route / UI button / tool string / AuthZ action string != canonical governed effect
runtime Agent / Principal != Domain Actor automatically
```

And all `WL-H01..WL-H12`, accepted Phase 5 requirement packages and accepted Phase 6 boundary contracts remain active downstream constraints.

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

AFTER PHASE 6 REMOTE QA
coordinated Phase 7–9 architecture tranche
(beginning with read-only durable-workflow benchmark preparation)
```
