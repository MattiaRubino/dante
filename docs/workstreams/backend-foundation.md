# Workstream — Backend Foundation

- Status: **NOT STARTED / DEFERRED**
- Intended future branch: `feature/backend-foundation` only after prerequisites are satisfied and a fresh branch/write gate is approved
- Current base: **none** — no backend implementation branch is authorized
- Work type: future production technical foundation

## Purpose

Provide the future production backend skeleton for LifeOS **after** the semantic, Pre-Physical, Physical and runtime/security/integration prerequisites required by the chosen first slice exist.

This handoff is deliberately non-executable today. It must not be used to bypass the current final Pre-Physical verification, invent Domain/Logical semantics, select persistence by implementation convenience or start production code before the required gates are closed.

## Current stage boundary

```text
Core Domain Model / Domain Atlas
CLOSED

Logical Model
CLOSED

Phase 5 requirements
CURRENT

Phase 6 AI/context/runtime/integration boundaries
CURRENT

Phase 7 durable-execution benchmark
CURRENT

Phase 8 governed-operation/effect contract
CURRENT

Phase 9 search/observability/calendar/solver pressure
CURRENT

Phase 10 Physical benchmark method
CURRENT / QA PASS

Phase 11 repository engineering safety
QA PASS / effective main rules remotely verified

Phase 12 clean-room repository/architecture QA
CLOSING ON chore/pre-physical-coherence

Pre-Physical Coherence
FINAL CLOSURE CANDIDATE
independent total repository audit required before definitive whole-workstream closure

Physical Model
NOT STARTED / NOT AUTHORIZED

Backend Foundation / production implementation
NOT STARTED / DEFERRED
```

Backend Foundation does **not** own Domain or Logical modeling. The old instruction to develop Domain Model v0 inside Backend Foundation is superseded. Any genuine future semantic contradiction requires its own explicit reopen scope and applicable methodology.

## Prerequisites before this workstream may become READY TO START

All of the following must be true before a backend implementation branch is created:

1. Phase 12 is QA PASS and the separately requested independent total repository audit has passed;
2. Pre-Physical Repository & Architecture Coherence is definitively closed and integrated as current repository truth;
3. the user has separately authorized and accepted the Physical Model workstream/result;
4. accepted Physical persistence/runtime boundaries exist for the implementation slice being started;
5. current Phase 5 requirements are consumed and implementation-dependent open parameters are resolved at the proper later gate;
6. Phase 6 AI/context/runtime and Integration Hub contracts are consumed wherever the slice touches those concerns;
7. Phase 7 durable-execution posture is consumed and any operation class needing a runtime has an accepted mechanism at the appropriate implementation gate;
8. Phase 8 governed-operation/effect contract is preserved before consequential routes/DTOs/tool schemas are stabilized;
9. Phase 9 search/observability/calendar/solver boundaries are consumed where applicable;
10. the Phase 10 Physical benchmark method has been executed by the separately authorized Physical workstream and the accepted result records relevant evidence/conditions;
11. Phase 11 effective repository safety remains active, and any future required checks correspond to real stable workflow/check contexts;
12. current `main`, global status, active workstream handoffs and current architecture/model sources are re-read immediately before the future branch/write gate.

Until those conditions are satisfied:

```text
DO NOT create feature/backend-foundation
DO NOT create SQL/schema/migrations
DO NOT stabilize concrete API routes/DTOs
DO NOT select persistence by convenience
DO NOT implement AuthN/AuthZ/provider/runtime mechanisms implicitly
DO NOT adopt Restate / Temporal / DBOS by benchmark preference alone
DO NOT add dedicated search/vector infrastructure by default
DO NOT make a solver write canonical state directly
DO NOT treat Phase 10 PREFERRED/REGISTERED candidates as selected technology
DO NOT weaken verified repository-safety controls
DO NOT invent required CI checks before real stable check contexts exist
DO NOT reopen Domain/Logical semantics inside backend work
```

## Required reading before future implementation

Read current sources, including complete cumulative/split chains where material:

1. root `README.md`;
2. `docs/README.md`;
3. `docs/PROJECT-STATUS.md`;
4. `docs/development/agent-operating-manual.md`;
5. `docs/development/operating-rules.md`;
6. `docs/development/documentation-and-handoff.md`;
7. `docs/development/branching-and-environments.md`;
8. `docs/development/repository-engineering-safety.md` plus then-current effective GitHub rules/settings/checks;
9. `docs/architecture/README.md`, `pre-physical-architecture-baseline.md`, `system-overview.md` and `technical-decisions.md`;
10. all four Phase 5 requirement packages;
11. both Phase 6 boundary contracts;
12. the Phase 7 durable-execution benchmark;
13. the Phase 8 governed-operation/effect contract;
14. the Phase 9 search/observability/calendar/solver contract;
15. all three Phase 10 benchmark-method documents;
16. the complete accepted Domain Atlas authority including final closure/status continuation and final language disposition;
17. the closed Whole Logical Model, complete decision/assumption-register chain and `whole-logical-v1-remote-qa.md` closure record;
18. the accepted Physical Model sources, benchmark evidence/result and closure evidence once they exist;
19. current ADRs using their current supersession/qualification state;
20. the then-current backend workstream gate and exact first-slice requirements.

Older product/architecture documents may remain useful evidence but do not override accepted Domain/Logical/Physical/current architecture sources.

## Current technical direction to preserve

Unless separately reviewed through the normal decision process:

- backend: Python + FastAPI + Pydantic;
- architecture: modular monolith first;
- domain/application logic independent from FastAPI request handling;
- clients use governed backend contracts, not direct canonical persistence;
- AI remains behind replaceable/provider-neutral boundaries;
- AI/context/runtime representation remains distinct from canonical truth;
- Integration Hub preserves five accepted integration modes and canonical/provider separation;
- Storage remains behind a provider abstraction;
- bounded async and material durable long-running work remain separate operation classes;
- governed operation/effect semantics remain independent from route/tool/workflow implementation;
- search/index/vector state remains projection rather than canonical truth;
- OpenTelemetry-first or equivalent is observability direction, not Domain history/audit by identity;
- calendar standards/provider schemas remain adapter pressure rather than ontology;
- deterministic solver output remains candidate/scenario state until a governed effect establishes canonical state;
- Physical preference/registration remains benchmark posture until accepted Physical selection;
- DEV/UAT/PROD are deployment environments, not permanent Git branches;
- `main` integration follows effective repository rules and real required checks;
- accepted Domain + Logical semantics, including `WL-H01..WL-H12`, are implementation constraints;
- Phase 5–11 contracts and the eventual accepted Physical result are mandatory downstream inputs, not implementation authorization by themselves.

## Phase 5 requirements future backend must consume

At minimum:

- AuthN/AuthZ preserves `Person != Account != Principal != Actor`, `Authority != AuthZ decision`, actual Actor vs represented party, consequential AuthZ provenance, non-human Principal governance, delayed-effect revalidation and non-interference/disclosure constraints;
- security/privacy supports purpose-aware minimization, secret isolation, sensitive-data handling, category-sensitive retention, truthful deletion/redaction/tombstone semantics, derived/external deletion propagation and secure recovery without forbidden-data resurrection;
- consistency/side-effects preserves expected-state semantics, idempotency distinct from identity, no silent material last-write-wins, semantic multi-owner atomicity where required, truthful staged/partial state, canonical/provider separation, ambiguous-failure safety and effect/reconciliation provenance;
- non-functional/multi-device/recovery preserves device divergence, operation-specific offline semantics, truthful degraded/provider state, long-history/current-state access, temporal/DST semantics, safe observability, recovery testing and later accepted RPO/RTO/latency/availability/scale targets.

Open Phase 5 parameters are obligations to resolve before dependent implementation/benchmarking, not permission to ignore the requirement.

## Phase 6 AI / Context / Runtime contract

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

The Context Builder is purpose-, disclosure-, provenance- and freshness-aware. Whole-history/full-database exposure is not default.

LifeOS does not maintain generic AI memory as a second canonical truth store.

```text
runtime Agent / Principal != Domain Actor automatically
tool invocation != authorization
tool/protocol action != canonical governed operation
```

Non-human Principals, delayed tool effects and external/retrieved instructions remain subject to governance, expected-state, privacy, idempotency and provenance requirements.

## Phase 6 Integration Hub contract

Five modes remain distinct:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

`ExternalRef != NativeRef`; provider revision != `MaterialStateRef`; provider state/effect status != canonical LifeOS state/effect automatically.

Sync direction/conflict handling, live-read freshness, deletion-aware projections, callbacks/replays and ambiguous external effects remain explicit bounded contracts. MCP/A2A/future protocols remain adapters.

## Phase 7 durable-execution contract

```text
BOUNDED ASYNC
short / bounded / cheaply reconstructible
→ DB/worker/outbox style remains valid baseline mechanism class

MATERIAL DURABLE LONG-RUNNING
long waits / human review / callbacks / crash-resume /
material cancellation / compensation / reconciliation
→ dedicated durable execution is structurally justified
```

Current candidates remain unselected:

```text
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional PostgreSQL-dependent challenger — NOT selected
```

Future implementation preserves replay/idempotency safety, delayed target/governance revalidation, external-effect ambiguity, runtime-vs-Domain cancellation separation, execution-vs-semantic identity separation, in-flight compatibility/versioning and truthful pending/partial/reconciliation state.

## Phase 8 governed-operation/effect contract

Consequential operations preserve by materiality:

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
idempotency + operation equivalence
correlation/causation
execution class
deadline/expiry/technical cancellation
canonical result
provider result
runtime result
conflict/partial/reconciliation/provenance
```

```text
HTTP route / UI button / tool / AuthZ action / workflow step
!= canonical governed operation/effect
request accepted != effect completed
provider acknowledgement != canonical completion automatically
workflow completed != Actual automatically
technical cancellation != Domain cancellation automatically
```

Concrete routes/DTOs/error codes/command buses remain later implementation design.

## Phase 9 contracts

### Search / retrieval

```text
structured filters + lexical/full-text  BASELINE
semantic/vector retrieval              BOUNDED CANDIDATE
pgvector                               BOUNDED IF POSTGRESQL SURVIVES PHYSICAL
dedicated search/vector service        NOT JUSTIFIED BY DEFAULT
```

Search miss != canonical nonexistence; ranking/similarity remains derived; inclusion/count/ranking/snippets/autocomplete/timing are disclosure surfaces; deletion/redaction propagates to projections.

### Observability

OpenTelemetry-first/equivalent is current direction. Technical trace/request/workflow IDs do not replace Domain Provenance, security audit or material effect history.

### Calendar

iCalendar/JSCalendar/provider APIs are interoperability pressure, not ontology. Adapters preserve recurrence exceptions, all-day/floating/zoned time, DST/history and provider token/deletion state without equating provider state with LifeOS state.

### Solver

```text
simple deterministic rules / heuristics  BASELINE
OR-Tools CP-SAT                       PREFERRED SPECIALIZED BENCHMARK CANDIDATE — NOT IMPLEMENTED
```

Hard constraints are not silently relaxed; `UNKNOWN != INFEASIBLE`; solver output remains candidate/scenario until a governed effect establishes canonical state.

## Phase 10 benchmark method

The later Physical Model must consume:

- `physical-benchmark-specification.md`;
- `physical-benchmark-scenario-corpus.md`;
- `physical-benchmark-register.md`.

Current role posture:

```text
PRIMARY CANONICAL
PostgreSQL hybrid — mandatory preferred baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH
no-specialized-store baseline vs Neo4j

SEARCH / VECTOR
structured + lexical/full-text baseline vs bounded pgvector where applicable

EVENT / DOCUMENT
bounded native mechanisms first; specialized candidate only on admitted gap/benefit
```

Physical candidates must satisfy semantic/correctness hard gates before performance/operability scores matter. LOW/BASE/HIGH values are synthetic benchmark envelopes, not production promises. Evidence is pinned to exact version/edition/deployment. `PREFERRED != SELECTED`.

Future backend implementation consumes the **accepted Physical result and all its conditions**, not the candidate labels above.

## Phase 11 repository-engineering safety

Current source: `docs/development/repository-engineering-safety.md`.

Phase 11 is QA PASS and effective main rules were remotely verified. Current owner-driven posture:

```text
pull request required
main deletion blocked
force-push/non-fast-forward blocked
review-thread resolution required
0 required approvals while no independent reviewer exists
0 required status checks until real stable checks exist
merge-commit history preserved by current policy
```

Required checks are promoted only after real stable contexts exist. Backend Foundation must not weaken these controls for convenience.

## Physical-dependent implementation candidates

The following are **not current architecture commitments** and may be adopted only if the accepted Physical Model justifies them:

- SQLAlchemy;
- Alembic;
- PostgreSQL-specific development configuration;
- relational migration mechanics;
- concrete transaction/isolation/version-token mechanisms;
- table/index/key/partition strategy;
- database-specific test fixtures/operational tooling;
- PostgreSQL-native FTS / pgvector as implementation components.

## Runtime/API-dependent implementation candidates

Do not freeze before prerequisite contracts/mechanism decisions exist:

- concrete versioned API route/DTO surface;
- REST/RPC/GraphQL surface;
- AuthN/AuthZ middleware/policy engine/persistence;
- idempotency storage/replay mechanics;
- transactional outbox/inbox/publication mechanics;
- bounded worker implementation;
- Restate / Temporal / DBOS runtime binding;
- workflow/automation execution mechanics;
- notification delivery runtime;
- provider adapters;
- AI provider/model/router/tool adapters;
- MCP/A2A/protocol adapters;
- projection/cache/search/vector infrastructure;
- OpenTelemetry SDK/Collector/backend;
- calendar provider SDK/adapters;
- OR-Tools/solver service;
- observability details that could expose sensitive data.

## Future bootstrap deliverables — implementation-independent core

When this workstream is actually authorized, likely initial foundation deliverables include:

- Python project/package structure;
- FastAPI application bootstrap;
- Pydantic settings/configuration;
- modular-monolith package boundaries;
- pytest baseline;
- externalized dependency/config/secrets handling;
- domain/application logic testability without FastAPI request handling;
- error-handling baseline;
- structured logging compatible with privacy/minimization requirements;
- development health/readiness endpoint where appropriate;
- provider-neutral interfaces only where an accepted contract exists;
- clear separation among API, application, Domain/Logical translation, persistence and provider/runtime concerns.

Physical-specific deliverables are added only after Physical acceptance. Runtime/provider-specific deliverables are added only after their mechanism selection is accepted.

## First implementation slice rule

There is **no fixed canonical first vertical slice today**.

The old target:

```text
Workspace → Goal/Program → Activity → Schedule → Actual/Confirmation
```

is superseded as a backend/domain contract. `Workspace` is not an accepted universal Domain owner; Project/Program product vocabulary maps to accepted semantics according to actual meaning rather than manufacturing new kernel roots.

When backend implementation is eventually authorized, the first slice is chosen from the accepted Domain + Logical + Phase 5 requirements + Phase 6–9 contracts + accepted Physical result + current product need. It must be narrow enough to validate architecture end-to-end without using product labels as ontology shortcuts.

## Future validation baseline

As applicable to the accepted design, validate at minimum:

- application starts in intended development environment;
- configuration/secrets are externalized appropriately;
- unit tests run independently of production providers;
- critical Domain/application logic is testable without HTTP handling;
- API/persistence/provider layers do not become the Domain Model;
- expected-state/conflict semantics are testable for consequential mutations;
- provider partial failure/divergence is truthful;
- history/provenance/correction survive persistence translation;
- selective disclosure and inference-leakage constraints are tested;
- Phase 5 open parameters needed by the slice are resolved rather than silently defaulted;
- AI/context tests preserve provenance/freshness/disclosure categories where relevant;
- tool/agent callers cannot bypass governance and retrieved content cannot self-authorize effects;
- integration tests distinguish canonical/provider state, duplicate callbacks, unknown outcomes and reconciliation;
- durable-runtime tests prove replay/idempotency/cancellation/version/recovery behavior appropriate to operation class;
- governed-operation tests prove target/material/governance/confirmation/result-axis semantics independently from transport;
- search tests cover authorization/disclosure, stale index, deletion propagation and vector recall where applicable;
- observability tests diagnose without sensitive payload leakage and without relying on telemetry as sole audit/provenance;
- calendar tests cover recurrence overrides, DST/floating/all-day and provider resync/token invalidation;
- solver tests preserve hard constraints, feasible/infeasible/unknown distinctions, stale input rejection and governed-effect application;
- recovery/degraded/multi-device tests exercise accepted requirements;
- accepted Physical hard-gate conditions/sensitivity caveats become implementation/deployment tests;
- migrations/rollback are tested only if the accepted Physical design uses migration-based persistence;
- database connectivity/config tests are added only for the accepted persistence;
- real required repository/CI checks pass before integration.

## Non-negotiable guardrails

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
provider state != canonical LifeOS state
derived projection != canonical truth
absence/unknown != false
idempotency != identity
HTTP/UI/tool/AuthZ string != canonical governed effect
runtime Agent / Principal != Domain Actor automatically
workflow completed != Actual automatically
technical cancellation != Domain cancellation automatically
search miss != canonical nonexistence
solver result != accepted canonical effect
preferred benchmark candidate != selected implementation
```

All `WL-H01..WL-H12`, Phase 5 requirements, Phase 6 boundaries, Phase 7–9 contracts, Phase 10 benchmark method, effective Phase 11 repository controls and later accepted Physical conditions remain active downstream constraints.

## Where to work when eventually authorized

Do **not** create the implementation branch now.

When every prerequisite is satisfied:

1. re-read current `main` and this handoff;
2. verify complete current split/continuation authorities;
3. verify effective repository rules and real required check contexts;
4. define exact backend implementation scope/path ownership;
5. present fresh branch/PRE-SCOPE/CREATE-UPDATE-DELETE gate;
6. only after approval create bounded implementation branch from current `main`;
7. update this handoff to **IN PROGRESS** with actual branch, PRE-SCOPE, package paths and validation commands.

## Handoff maintenance after implementation starts

Record at least:

- actual branch and PR;
- implementation PRE-SCOPE;
- exact approved path scope;
- last validated commit;
- actual package/file paths;
- commands to run/test/migrate where applicable;
- accepted Physical/runtime dependencies;
- completed tasks/current task;
- known issues/risks;
- validation evidence;
- next exact steps.

Do not update `PROJECT-STATUS.md` for every backend commit. Update global status only when the workstream genuinely starts, blocks, reaches an integrated milestone, changes branch/PR or finishes.

## Current exact next step

```text
BACKEND FOUNDATION
NO IMPLEMENTATION ACTION

CURRENT PROJECT ACTION
finish Phase 12 clean-room closure on chore/pre-physical-coherence
then perform the separately requested independent total repository audit

PRE-PHYSICAL COHERENCE
FINAL CLOSURE CANDIDATE
NOT YET DEFINITIVELY CLOSED

MAIN INTEGRATION
NOT AUTHORIZED YET

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED
```
