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
Phase 5 requirements CURRENT
Phase 6 AI/context/runtime/integration boundaries CURRENT
Phase 7 durable-execution benchmark CURRENT
Phase 8 governed-operation/effect contract CURRENT
Phase 9 search/observability/calendar/solver pressure CURRENT

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
6. the current Phase 7 durable-execution posture is consumed and any chosen operation class has an accepted runtime mechanism at the appropriate implementation gate;
7. the current Phase 8 governed operation/effect contract is accepted before concrete consequential routes/DTOs/tool schemas are stabilized;
8. the current Phase 9 search/observability/calendar/solver boundaries are consumed where the implementation slice touches those capabilities;
9. repository engineering safety/CI requirements needed before production backend work are in place;
10. current `main` and all active current-specification sources are re-read immediately before the new branch/write gate.

Until these conditions are satisfied:

```text
DO NOT create feature/backend-foundation
DO NOT create SQL/schema/migrations
DO NOT stabilize concrete API routes/DTOs
DO NOT select persistence by convenience
DO NOT implement AuthN/AuthZ/provider/runtime mechanisms implicitly
DO NOT adopt Restate / Temporal / DBOS by benchmark preference alone
DO NOT add dedicated search/vector infrastructure by default
DO NOT make a solver write canonical state directly
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
11. current Phase 7 [`../architecture/durable-execution-benchmark.md`](../architecture/durable-execution-benchmark.md);
12. current Phase 8 [`../architecture/governed-operation-effect-contract.md`](../architecture/governed-operation-effect-contract.md);
13. current Phase 9 [`../architecture/search-observability-calendar-solver-boundaries.md`](../architecture/search-observability-calendar-solver-boundaries.md);
14. the complete accepted Domain Atlas beginning at [`../domain/README.md`](../domain/README.md), including its canonical continuation parts where required;
15. the closed Whole Logical Model at [`../logical-model/whole-logical-model-v1.md`](../logical-model/whole-logical-model-v1.md), its complete decision/assumption-register chain, and closure evidence [`../logical-model/checkpoints/whole-logical-v1-remote-qa.md`](../logical-model/checkpoints/whole-logical-v1-remote-qa.md);
16. the then-current accepted Physical Model sources and closure evidence, once they exist;
17. current ADRs under [`../decisions/`](../decisions/), using their current qualification/supersession status rather than historical labels.

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
- bounded async work and material durable long-running work are separate operation classes;
- governed operation/effect semantics remain independent from route/tool/workflow implementation;
- search/index/vector state remains downstream projection rather than canonical truth;
- OpenTelemetry-first or equivalent instrumentation is a technical observability direction, not Domain history/audit by identity;
- calendar standards/provider schemas remain adapter/interoperability pressure;
- deterministic solver output remains candidate/scenario state until a governed effect establishes canonical state;
- DEV/UAT/PROD are deployment environments, not permanent Git branches;
- accepted Domain + Logical semantics, including `WL-H01..WL-H12`, are implementation constraints rather than suggestions;
- the current Pre-Physical Architecture Baseline, Phase 5 requirements and Phase 6–9 contracts are mandatory downstream inputs and do not themselves authorize implementation.

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

## Phase 7 durable-execution contract that future implementation must consume

LifeOS uses an operation-class boundary instead of one universal workflow mechanism.

```text
BOUNDED ASYNC
short / bounded / cheaply reconstructible
→ simple DB/worker/outbox style remains valid baseline mechanism class

MATERIAL DURABLE LONG-RUNNING
long waits / human review / callbacks / crash-resume /
material cancellation / compensation / reconciliation
→ dedicated durable execution is structurally justified
```

Current dedicated candidates are benchmark posture only:

```text
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional PostgreSQL-dependent challenger — NOT selected
```

Future implementation must preserve:

- replay/recovery without duplicate governed consequence;
- delayed target/governance revalidation;
- explicit external-effect ambiguity;
- runtime cancellation separate from Domain cancellation;
- runtime execution identity separate from semantic identity;
- in-flight compatibility/versioning;
- truthful pending/partial/reconciliation state.

## Phase 8 governed-operation/effect contract that future implementation must consume

Consequential operations preserve, where applicable:

```text
contract/version
semantic target/facet
requested effect
input/candidate
purpose/context
material/expected state
derived/live basis + freshness
Principal / actual Actor / represented party
governance basis
autonomy / preview / confirmation
idempotency
correlation/causation
execution class
deadline/expiry/cancellation semantics
canonical result
provider result
runtime result
conflict/partial/reconciliation/provenance
```

Current non-collapse rules:

```text
HTTP route / UI button / tool / AuthZ action / workflow step
!= canonical governed operation/effect

request accepted != effect completed
provider acknowledgement != canonical completion automatically
workflow completed != Actual automatically
technical cancellation != Domain cancellation automatically
```

Concrete routes/DTOs/error codes/command buses may be designed only after preserving this contract.

## Phase 9 search / observability / calendar / solver contracts that future implementation must consume

### Search / retrieval

```text
structured filters + lexical/full-text
BASELINE

semantic/vector retrieval
BOUNDED CANDIDATE

pgvector
BOUNDED CANDIDATE IF POSTGRESQL SURVIVES PHYSICAL SELECTION

dedicated search/vector service
NOT JUSTIFIED BY DEFAULT
```

Search miss != canonical nonexistence; ranking/vector similarity remains derived; result inclusion/count/ranking/snippets/autocomplete/timing remain disclosure surfaces; deletion/redaction must propagate to projections.

### Observability

OpenTelemetry-first or equivalent standards-based instrumentation is the current direction; no telemetry vendor is selected. Trace/request/workflow IDs are technical and do not replace Domain Provenance, security audit or material effect history.

### Calendar

iCalendar/JSCalendar/provider APIs are interoperability pressure, not ontology. Adapters must preserve recurrence exceptions, all-day/floating/zoned time, DST/history and provider sync-token/deletion state without equating provider identity/revision with LifeOS identity/material state.

### Solver

```text
simple deterministic rules / heuristics
BASELINE

OR-Tools CP-SAT
PREFERRED SPECIALIZED SOLVER BENCHMARK CANDIDATE — NOT IMPLEMENTED
```

Hard constraints are not silently relaxed; `UNKNOWN != INFEASIBLE`; solver output remains candidate/scenario until Phase 8 validates an accepted effect.

## Physical-dependent implementation candidates

The following are **not current architecture commitments** and may be adopted only if the accepted Physical Model justifies them:

- SQLAlchemy;
- Alembic;
- PostgreSQL-specific local development configuration;
- relational migration mechanics;
- concrete transaction/isolation/version-token mechanisms;
- table/index/key/partition strategy;
- database-specific test fixtures or operational tooling;
- PostgreSQL-native FTS / pgvector as implementation components.

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

Do not freeze these before their accepted prerequisite contracts and later implementation gates exist:

- versioned concrete API route/DTO surface;
- REST/RPC/GraphQL concrete surface;
- AuthN/AuthZ middleware, policy engine or persistence;
- idempotency storage and replay mechanics;
- transactional outbox/inbox/publication mechanics;
- bounded worker queue implementation;
- Restate / Temporal / DBOS runtime binding;
- workflow/automation execution mechanics;
- notification delivery runtime;
- Integration Hub provider adapters;
- AI provider/model/router and tool/action adapters;
- MCP/A2A/protocol adapters;
- projection/cache/search/vector infrastructure;
- OpenTelemetry SDK/Collector/backend implementation;
- calendar provider SDK/adapters;
- OR-Tools/solver service implementation;
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

Physical-specific bootstrap deliverables are added only after Physical acceptance. Runtime/provider-specific deliverables are added only after their prerequisite contracts and mechanism selections are accepted.

## First implementation slice rule

There is **no fixed canonical first vertical slice in this handoff today**.

The old target:

```text
Workspace → Goal/Program → Activity → Schedule → Actual/Confirmation
```

is superseded as a backend/domain contract. `Workspace` is not an accepted universal Domain owner, while `Project`/`Program` product vocabulary maps to accepted semantics such as a `Plan` profile according to the actual case rather than manufacturing new kernel roots.

When backend implementation is eventually authorized, the first slice must be chosen from the accepted Domain + Logical + Phase 5 requirements + Phase 6 boundaries + Phase 7–9 contracts + accepted Physical design + current product need. It should be narrow enough to validate the architecture end to end without using product labels as an ontology shortcut.

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
- bounded async/durable runtime tests prove replay/idempotency/cancellation/version/recovery behavior appropriate to the operation class;
- governed-operation tests prove target/material/governance/confirmation/result-axis semantics independently from transport;
- search tests cover authorization/disclosure, stale index, deletion propagation and semantic/vector recall where applicable;
- observability tests prove required diagnosis without sensitive payload leakage and without relying on telemetry as the only audit/provenance store;
- calendar tests cover recurrence overrides, DST/floating/all-day and provider resync/token invalidation where applicable;
- solver tests preserve hard constraints, feasible/infeasible/unknown distinctions, stale input rejection and governed-effect application;
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
workflow completed != Actual automatically
technical cancellation != Domain cancellation automatically
search miss != canonical nonexistence
solver result != accepted canonical effect
```

And all `WL-H01..WL-H12`, accepted Phase 5 requirement packages, accepted Phase 6 boundary contracts and accepted Phase 7–9 architecture contracts remain active downstream constraints.

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

AFTER COORDINATED PHASE 7–9 REMOTE QA
Phase 10 — Physical benchmark specification/register
READ-ONLY FIRST

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED
```