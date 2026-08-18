# Workstream — Backend Foundation

- Status: **NOT STARTED / DEFERRED**
- Intended future branch: `feature/backend-foundation` only after all prerequisites are satisfied and a fresh branch/write gate is approved
- Current implementation base: **none**
- Work type: future production technical foundation

## Purpose

Provide the future production backend skeleton for LifeOS **after** the semantic, integrated Pre-Physical, accepted Physical and applicable runtime/security/integration prerequisites required by the chosen first slice exist.

This handoff is deliberately non-executable today. The active Physical Model workstream does not authorize Backend Foundation by itself.

```text
PHYSICAL WORKSTREAM AUTHORIZED
!=
PHYSICAL RESULT ACCEPTED
!=
BACKEND AUTHORIZED
```

## Current stage boundary

```text
Core Domain Model / Domain Atlas
CLOSED / INTEGRATED

Logical Model
CLOSED / INTEGRATED
WL-H01..WL-H12 ACTIVE DOWNSTREAM

Phase 5 requirements
CURRENT

Phase 6 AI/context/runtime/integration boundaries
CURRENT
including consequential AI evaluation/regression requirement

Phase 7 durable-execution contract
CURRENT / conditional ranking only

Phase 8 governed-operation/effect contract
CURRENT

Phase 9 search/observability/calendar/solver pressure
CURRENT

Phase 10 Physical benchmark method
CURRENT / QA PASS

Phase 11 repository engineering safety
QA PASS / effective main rules remotely verified

Phase 12 + independent Pre-Physical audit
CLOSED / PASS

Pre-Physical Coherence
DEFINITIVE CLOSED / FINAL QA PASS
INTEGRATED / POST-MERGE VERIFIED

Physical readiness
ESTABLISHED

Physical Model
AUTHORIZED / IN PROGRESS — PM-00 BOOTSTRAP
branch feature/physical-model
base main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79
mapping NOT STARTED
benchmark NOT STARTED
selection NONE

Backend Foundation / production implementation
NOT STARTED / DEFERRED
```

Backend Foundation does **not** own Domain or Logical modeling. Any genuine future semantic contradiction requires a separate explicit reopen scope/methodology.

## Prerequisites before Backend Foundation may become READY TO START

All must be true before `feature/backend-foundation` is created:

1. Phase 12 + independent Pre-Physical closure passed — **SATISFIED**;
2. Pre-Physical result integrated into current repository truth — **SATISFIED**;
3. Physical Model workstream is completed, independently QA-verified and its result explicitly accepted — **NOT SATISFIED**;
4. accepted Physical persistence boundaries exist for the implementation slice — **NOT SATISFIED**;
5. Phase 5 requirements needed by the slice are consumed and required open parameters are resolved at the proper gate;
6. Phase 6 AI/context/runtime + Integration Hub contracts are consumed where applicable;
7. Phase 7 durable-execution posture is consumed and any operation class needing a runtime has an accepted mechanism at the proper implementation gate;
8. Phase 8 governed-operation/effect contract is preserved before routes/DTOs/tool schemas are stabilized;
9. Phase 9 search/observability/calendar/solver boundaries are consumed where applicable;
10. Phase-10 method has been executed by the Physical workstream and the accepted Physical result carries all evidence/conditions/sensitivity — **NOT SATISFIED**;
11. Phase-11 effective repository safety remains active and any required checks correspond to real stable workflow contexts;
12. then-current `main`, global status, active handoffs and current model/architecture sources are re-read immediately before Backend authorization.

Until then:

```text
DO NOT create feature/backend-foundation
DO NOT create production SQL/schema/migrations
DO NOT stabilize concrete API routes/DTOs
DO NOT select persistence by convenience
DO NOT implement AuthN/AuthZ/provider/runtime mechanisms implicitly
DO NOT adopt Restate / Temporal / DBOS by benchmark preference alone
DO NOT add dedicated search/vector infrastructure by default
DO NOT make solver/AI output write canonical state directly
DO NOT treat PREFERRED/REGISTERED candidates as selected
DO NOT weaken repository-safety controls
DO NOT invent required CI checks before stable contexts exist
DO NOT reopen Domain/Logical semantics inside backend work
```

Physical benchmark-only mapping/schema/harness code, when later authorized inside `feature/physical-model`, remains **benchmark infrastructure**, not Backend Foundation production code.

## Required reading before future backend implementation

At minimum:

1. root `README.md`;
2. `docs/README.md`;
3. `docs/PROJECT-STATUS.md`;
4. all development operating/safety manuals;
5. this handoff;
6. current architecture index/baseline/system overview/technical decisions;
7. all Phase-5 requirement packages;
8. Phase-6 AI/context/runtime + Integration Hub contracts;
9. Phase-7 durable-execution contract;
10. Phase-8 governed-operation/effect contract;
11. Phase-9 search/observability/calendar/solver contract;
12. all Phase-10 benchmark-method documents;
13. accepted Domain closure authority and Language Map;
14. accepted Logical Model + complete decision register + remote closure evidence;
15. the complete accepted Physical Model authority, benchmark evidence/result, conditions and closure evidence once it exists;
16. current ADRs with supersession/qualification state;
17. then-current repository rules/check contexts;
18. the exact backend workstream gate/first-slice requirements.

Older documents/branches remain evidence only and cannot override accepted current authority.

## Current technical direction to preserve

Unless separately reviewed through the normal decision process:

- backend: Python + FastAPI + Pydantic;
- architecture: modular monolith first;
- domain/application logic independent from FastAPI request handling;
- clients use governed backend contracts, not direct canonical persistence;
- AI remains behind replaceable/provider-neutral boundaries;
- AI/context/runtime representation remains distinct from canonical truth;
- material consequential AI changes are promotion-gated by reproducible evaluation;
- Integration Hub preserves five accepted integration modes and canonical/provider separation;
- storage remains behind an abstraction compatible with the **accepted** Physical result;
- bounded async and material durable long-running work remain separate classes;
- governed operation/effect semantics remain independent from route/tool/workflow implementation;
- search/index/vector state remains projection, not canonical truth;
- OpenTelemetry-first/equivalent remains observability direction, not Domain Provenance/audit by identity;
- calendar standards/provider schemas remain adapter pressure rather than ontology;
- deterministic solver output remains candidate/scenario state until governed application;
- DEV/UAT/PROD are environments, not permanent Git branches;
- accepted Domain + Logical semantics, including `WL-H01..WL-H12`, remain implementation constraints.

SQLAlchemy, Alembic and PostgreSQL-specific implementation choices remain conditional until the accepted Physical result justifies them.

## Phase-5 requirements future backend must consume

### AuthN/AuthZ

Preserve at minimum:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
actual Actor != represented party where applicable
technical authorization provenance != Domain identity
```

Support delayed-effect revalidation, non-human Principal governance and selective-disclosure/non-interference constraints.

### Security / privacy / retention / recovery

Support purpose-aware minimization, secret isolation, sensitive-data handling, category-sensitive retention, truthful deletion/redaction/tombstone semantics, downstream deletion propagation and recovery without forbidden-data resurrection.

### Consistency / side effects

Preserve expected-state semantics, idempotency distinct from identity, no universal silent last-write-wins, atomic multi-owner change where required, truthful staged/partial state across external boundaries, provider/canonical separation and ambiguous-failure reconciliation.

### Non-functional / multi-device / operational recovery

Preserve device divergence, operation-specific offline semantics, truthful degraded/provider state, long-history/current-state access, temporal/DST semantics, safe observability and accepted later RPO/RTO/latency/availability/scale targets.

Open values are obligations to resolve, not permission to invent defaults.

## Phase-6 AI / Context / Runtime contract

Preserve distinct:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

```text
runtime Agent / Principal != Domain Actor automatically
tool invocation != authorization
tool/protocol action != canonical governed effect
eval result != canonical LifeOS truth
eval PASS != Authority / governed-effect authorization
```

The Context Builder remains purpose/disclosure/provenance/freshness aware. Whole-history/full-database exposure is not default.

Material changes to model/version/provider, prompt/instruction layer, Context Builder policy, tool schema/selection or fallback/routing require versioned/reproducible evaluation appropriate to the affected behavior.

## Integration Hub contract

Keep five modes distinct:

1. canonical import;
2. sync/mirror;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

```text
ExternalRef != NativeRef
provider revision != MaterialStateRef
provider state/effect != canonical LifeOS state/effect automatically
```

MCP/A2A/future protocols remain adapters.

## Durable-execution contract

```text
BOUNDED ASYNC
DB/worker/outbox style = valid baseline mechanism class

MATERIAL DURABLE LONG-RUNNING
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional challenger — NOT selected
          local/bounded Python SQLite-capable
          production PostgreSQL-recommended
          distributed multi-server PostgreSQL-coupled
```

Replay/idempotency, delayed target/governance revalidation, ambiguous external effects, runtime-vs-Domain cancellation, execution-vs-semantic identity, in-flight compatibility and truthful pending/partial/reconciliation remain mandatory.

## Governed-operation/effect contract

Consequential operations preserve as material:

```text
contract/version
target/facet
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

Concrete route/DTO/command-bus design remains later implementation work.

## Search / observability / calendar / solver

```text
SEARCH
structured + lexical/full-text baseline
semantic/vector bounded candidate
search miss != canonical nonexistence

OBSERVABILITY
OpenTelemetry-first/equivalent direction
telemetry != Domain Provenance/security audit by identity

CALENDAR
iCalendar/JSCalendar/provider APIs = adapter pressure, not ontology

SOLVER
simple deterministic rules/heuristics baseline
OR-Tools CP-SAT preferred specialized benchmark candidate — NOT implemented
UNKNOWN != INFEASIBLE
solver output != accepted canonical effect
```

## Phase-10 / active Physical relationship

Phase 10 defines the benchmark method; `feature/physical-model` now executes it under `docs/physical-model/**`.

Current registered posture remains unselected:

```text
PRIMARY
PostgreSQL hybrid — mandatory preferred baseline — NOT SELECTED
TypeDB            — mandatory challenger        — NOT SELECTED

GRAPH
G0 no-specialized-store vs Neo4j

SEARCH/VECTOR
S0 structured/FTS vs bounded pgvector where applicable
```

Physical hard-gate evidence precedes scoring. `LOW/BASE/HIGH` are synthetic qualification envelopes; unexecuted tiers remain unverified. `PREFERRED != SELECTED`.

Backend consumes the **accepted Physical result**, not interim benchmark preference.

## Physical-dependent implementation candidates

Do not adopt until accepted Physical result justifies them:

- SQLAlchemy;
- Alembic;
- PostgreSQL-specific configuration;
- concrete transaction/isolation/version-token mechanics;
- table/index/key/partition strategy;
- database migration mechanics;
- database-specific test/operational tooling;
- PostgreSQL-native FTS / pgvector as production components;
- TypeDB-specific client/schema infrastructure;
- Neo4j-specific production projection infrastructure.

## Runtime/API-dependent candidates

Do not freeze prematurely:

- REST/RPC/GraphQL surface;
- concrete route/DTO versioning;
- Auth middleware/policy engine/persistence;
- idempotency storage/replay mechanics;
- outbox/inbox/publication implementation;
- bounded worker implementation;
- Restate/Temporal/DBOS binding;
- provider adapters;
- AI provider/model/router/tool adapters;
- AI evaluation frameworks/datasets/runners/thresholds;
- MCP/A2A adapters;
- projection/cache/search/vector services;
- OpenTelemetry SDK/Collector/backend;
- calendar provider SDK/adapters;
- OR-Tools/solver service.

## Future backend bootstrap deliverables

Only after authorization, likely implementation-independent foundation work includes:

- Python project/package structure;
- FastAPI bootstrap;
- Pydantic settings/configuration;
- modular-monolith package boundaries;
- pytest baseline;
- externalized secrets/config;
- domain/application testability without HTTP;
- error-handling baseline;
- privacy-aware structured logging;
- development health/readiness endpoint where appropriate;
- provider-neutral interfaces only where accepted contracts exist;
- explicit API/application/semantic/persistence/provider/runtime separation.

Physical/runtime/provider-specific deliverables are added only after their relevant accepted decisions.

## First implementation slice rule

There is **no fixed canonical first vertical slice today**.

The old product-shaped shortcut:

```text
Workspace → Goal/Program → Activity → Schedule → Actual/Confirmation
```

is superseded as a backend/domain contract. `Workspace` is not an accepted universal owner. Product vocabulary maps to accepted semantics according to meaning rather than manufacturing ontology roots.

When Backend is eventually authorized, choose a narrow slice from accepted Domain + Logical + Phase-5..9 contracts + accepted Physical result + current product need.

## Future validation baseline

As applicable, future Backend must validate:

- application/config/secrets bootstrap;
- unit tests independent of production providers;
- critical logic testable without HTTP;
- API/persistence/provider layers do not become Domain Model;
- expected-state conflicts;
- provider partial/unknown outcomes;
- history/provenance/correction persistence;
- disclosure/inference leakage;
- AI/context provenance/freshness/disclosure;
- consequential AI promotion evaluation;
- tool/agent governance non-bypass;
- integration duplicate/reorder/unknown/reconciliation behavior;
- durable-runtime replay/idempotency/cancellation/version/recovery;
- governed-operation target/material/governance/confirmation/result axes;
- search authorization/staleness/deletion/vector recall where applicable;
- observability without sensitive leakage;
- recurrence/DST/floating/all-day/provider resync;
- solver hard-constraint/result-category/stale-input rules;
- recovery/degraded/multi-device requirements;
- all accepted Physical hard-gate conditions/sensitivity caveats;
- migrations/rollback only when the accepted Physical design uses them;
- real required repository/CI checks before integration.

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
eval result != canonical LifeOS truth
preferred benchmark candidate != selected implementation
```

All `WL-H01..WL-H12`, Phase-5 requirements, Phase-6 boundaries, Phase-7..9 contracts, Phase-10 benchmark method, Phase-11 controls, Pre-Physical closure constraints and eventual accepted Physical conditions remain downstream constraints.

## Where to work when eventually authorized

Do **not** create the Backend branch now.

When every prerequisite is satisfied:

1. re-read current `main` and this handoff;
2. verify complete accepted model/Physical authorities;
3. verify effective repository rules/checks;
4. define exact backend scope/path ownership;
5. present fresh branch/PRE-SCOPE/CREATE-UPDATE-DELETE gate;
6. after approval create bounded implementation branch from then-current `main`;
7. update this handoff to **IN PROGRESS** with actual branch/PRE-SCOPE/package paths/validation commands.

## Handoff maintenance after Backend starts

Record actual branch/PR, PRE-SCOPE, approved paths, validated commit, implementation paths, test/migrate commands, accepted Physical/runtime dependencies, current task, risks, evidence and exact next steps.

Do not update global status for every backend commit.

## Current exact next step

```text
BACKEND FOUNDATION
NO IMPLEMENTATION ACTION
NOT STARTED / DEFERRED

PHYSICAL MODEL
AUTHORIZED / IN PROGRESS — PM-00 BOOTSTRAP
feature/physical-model
base 3de84bb49f9cef30e88e9bde4961ed84335daa79

PHYSICAL RESULT
NOT YET ACCEPTED
mapping NOT STARTED
benchmark NOT STARTED
selection NONE

CURRENT PROJECT ACTION
complete PM-00 bootstrap QA
then PM-01 READ-ONLY candidate/version/edition/deployment/environment freeze

BACKEND ELIGIBILITY
BLOCKED until accepted Physical result + remaining prerequisites
```