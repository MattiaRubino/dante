# Workstream — Backend Foundation

- Status: **NOT STARTED / DEFERRED**
- Intended future branch: `feature/backend-foundation` only after remaining prerequisites are satisfied and a fresh branch/write gate is approved
- Current implementation base: **none**
- Work type: future production technical foundation
- Accepted Physical input: **CLOSED / SELECTED / ACCEPTED / integrated into `main` via PR #15**
- Development Profile v0: **NOT STARTED / NEXT SEPARATE OPERATIONAL SCOPE**

## Purpose

Provide the future production backend skeleton for LifeOS **after** the semantic, integrated Pre-Physical, accepted/integrated Physical and applicable runtime/security/integration prerequisites required by the chosen first slice exist.

This handoff is deliberately non-executable today. Physical closure and integration do not authorize Backend Foundation by themselves.

```text
PHYSICAL TARGET CLOSED / SELECTED / ACCEPTED
!=
DIRECT SELECTED-STACK VALIDATION PASS
!=
DEVELOPMENT PROFILE DEFINED
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
CURRENT / physically resolved by PM-11/12 where selected

Phase 8 governed-operation/effect contract
CURRENT

Phase 9 search/observability/calendar/solver pressure
CURRENT / physically resolved where selected

Phase 10 Physical benchmark method
CURRENT METHOD / QA PASS / HISTORICAL INPUT TO CLOSED PHYSICAL DECISION

Phase 11 repository engineering safety
QA PASS / effective main rules remotely verified

Phase 12 + independent Pre-Physical audit
CLOSED / PASS

Pre-Physical Coherence
DEFINITIVE CLOSED / FINAL QA PASS
INTEGRATED / POST-MERGE VERIFIED

Physical Model
CLOSED / SELECTED / ACCEPTED
INTEGRATED INTO MAIN VIA PR #15
main e6f191bad947388a44defe2c15f4939345084f58
former feature/physical-model MERGED / AUTO-DELETED
selected canonical primary PostgreSQL 18.4
selected companion architecture ESTABLISHED

Direct selected-stack implementation validation
NOT STARTED / DIRECT HG PASS 0

Development Profile v0
NOT STARTED / NEXT SEPARATE OPERATIONAL SCOPE

Backend Foundation / production implementation
NOT STARTED / DEFERRED
```

Backend Foundation does **not** own Domain or Logical modeling and does not silently reopen the accepted Physical target. Any genuine semantic contradiction requires a separate explicit Domain/Logical reopen scope; any selected-stack failure that invalidates a Physical choice requires an explicit Physical reopen.

## Prerequisites before Backend Foundation may become READY TO START

All must be true before `feature/backend-foundation` is created:

1. Phase 12 + independent Pre-Physical closure passed — **SATISFIED**;
2. Pre-Physical result integrated into current repository truth — **SATISFIED**;
3. Physical Model workstream completed, independently QA-verified and explicitly accepted — **SATISFIED**;
4. accepted Physical persistence boundaries exist for the implementation slice — **SATISFIED**;
5. Phase 5 requirements needed by the slice are consumed and required open parameters are resolved at the proper gate;
6. Phase 6 AI/context/runtime + Integration Hub contracts are consumed where applicable;
7. Phase 7 durable-execution posture is consumed and any operation class needing Class-B durable execution uses the accepted Restate boundary without bypassing its PSV obligations;
8. Phase 8 governed-operation/effect contract is preserved before routes/DTOs/tool schemas are stabilized;
9. Phase 9 search/observability/calendar/solver boundaries are consumed where applicable;
10. Phase-10/Physical decision method has completed and the accepted Physical result carries its evidence/conditions/sensitivity — **SATISFIED AT TARGET-ARCHITECTURE LEVEL**; direct selected-stack PSV obligations remain separately **NOT RUN** until the applicable implementation/release boundary;
11. Phase-11 effective repository safety remains active and any required checks correspond to real stable workflow contexts;
12. Development Profile v0 and any other operational choice required by the first backend slice are resolved at the proper separate gate;
13. then-current `main`, global status, handoffs and current model/architecture sources are re-read immediately before Backend authorization.

Until then:

```text
DO NOT create feature/backend-foundation
DO NOT create production SQL/schema/migrations
DO NOT stabilize concrete API routes/DTOs
DO NOT change accepted persistence/runtime/search/solver choices by convenience
DO NOT implement AuthN/AuthZ/provider/runtime mechanisms implicitly
DO NOT add excluded dedicated search/vector/graph/broker infrastructure by default
DO NOT make solver/AI output write canonical state directly
DO NOT treat SELECTED as DEPLOYED or DIRECT PASS
DO NOT weaken repository-safety controls
DO NOT invent required CI checks before stable contexts exist
DO NOT reopen Domain/Logical/Physical semantics inside backend work implicitly
```

Any future selected-stack validation mapping/schema/harness code remains **validation infrastructure** unless and until a separately authorized backend scope deliberately adopts the relevant implementation artifact.

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
12. all Phase-10 benchmark-method documents where evidence/method history is material;
13. accepted Domain closure authority and Language Map;
14. accepted Logical Model + complete decision register + remote closure evidence;
15. complete accepted Physical Model authority: PM-11 selection, PM-12 Accepted Physical Model, PM-13 QA, PM-14 historical closure evidence, current result register and post-selection validation register;
16. current ADRs with supersession/qualification state;
17. then-current repository rules/check contexts;
18. Development Profile v0 once accepted;
19. the exact backend workstream gate/first-slice requirements.

Older documents/branches remain evidence only and cannot override accepted current authority.

## Current technical direction to preserve

Unless separately reviewed through the normal decision process:

- backend: Python + FastAPI + Pydantic;
- architecture: modular monolith first;
- domain/application logic independent from FastAPI request handling;
- clients use governed backend contracts, not direct canonical persistence;
- canonical persistence: PostgreSQL 18.4 through the accepted owner-specific Physical mapping;
- AI remains behind replaceable/provider-neutral boundaries;
- AI/context/runtime representation remains distinct from canonical truth;
- material consequential AI changes are promotion-gated by reproducible evaluation;
- Integration Hub preserves five accepted integration modes and canonical/provider separation;
- bounded async uses PostgreSQL transactional outbox + bounded worker where applicable;
- material Class-B durable execution uses the selected Restate runtime where applicable;
- governed operation/effect semantics remain independent from route/tool/workflow implementation;
- search/index/vector state remains projection, not canonical truth;
- accepted search baseline is PostgreSQL FTS + `pg_trgm` + `unaccent`, with pgvector for bounded vector retrieval;
- observability target is OpenTelemetry + Grafana Alloy + Grafana Cloud EU, with privacy minimization;
- calendar standards/provider schemas remain adapter pressure rather than ontology;
- OR-Tools 9.15 CP-SAT is the selected solver; its output remains candidate/scenario state until governed application;
- DEV/UAT/PROD are environments, not permanent Git branches;
- accepted Domain + Logical semantics, including `WL-H01..WL-H12`, remain implementation constraints.

SQLAlchemy and Alembic may now be evaluated/used against the accepted PostgreSQL target **only inside a separately authorized backend/development scope**. Physical acceptance does not itself authorize their implementation.

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
PostgreSQL transactional outbox + bounded worker
SELECTED CLASS-A MECHANISM

MATERIAL DURABLE LONG-RUNNING
Restate runtime
SELECTED CLASS-B TECHNOLOGY
self-hosted FIRST-CLASS OR Cloud EU ALLOWED MANAGED OPTION
global deployment default NONE
```

Temporal and DBOS remain non-selected historical challengers, not backend implementation alternatives by default.

Replay/idempotency, delayed target/governance revalidation, ambiguous external effects, runtime-vs-Domain cancellation, execution-vs-semantic identity, in-flight compatibility and truthful pending/partial/reconciliation remain mandatory. Current Python use must not assume TypeScript-only Restate Cloud journal encryption; journal minimization and applicable PSV checks remain required.

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
PostgreSQL native FTS + pg_trgm + unaccent SELECTED
pgvector bounded semantic/vector retrieval SELECTED
search/index state remains derived
search miss != canonical nonexistence

OBSERVABILITY
OpenTelemetry + Grafana Alloy + Grafana Cloud EU SELECTED TARGET
telemetry != Domain Provenance/security audit by identity

CALENDAR
iCalendar/JSCalendar/provider APIs = adapter pressure, not ontology

SOLVER
OR-Tools 9.15 CP-SAT SELECTED
UNKNOWN != INFEASIBLE
solver output != accepted canonical effect
```

## Phase-10 / closed Physical relationship

Phase 10 defines the benchmark/evidence method. The completed Physical workstream consumed it and selected/accepted the current target through PM-11/12, with PM-13 QA PASS and protected-main integration via PR #15.

Current target posture is therefore no longer an unselected candidate register:

```text
PRIMARY
PostgreSQL 18.4 SELECTED / ACCEPTED

GRAPH
no dedicated graph database in accepted initial target

SEARCH/VECTOR
PostgreSQL FTS + pg_trgm + unaccent
pgvector bounded vector retrieval

DURABLE CLASS-B
Restate runtime

SOLVER
OR-Tools 9.15 CP-SAT
```

Physical evidence rules remain active: `LOW/BASE/HIGH` are unexecuted direct tiers, `DIRECT HG PASS = 0`, `SELECTED != DIRECT PASS`, and applicable PSV obligations remain mandatory.

Backend consumes the **accepted Physical result**, not interim Phase-10 candidate preference.

## Physical-dependent implementation candidates

The accepted Physical result now permits later authorized evaluation/implementation of PostgreSQL-aligned mechanisms such as:

- SQLAlchemy;
- Alembic;
- PostgreSQL-specific configuration;
- concrete transaction/isolation/version-token mechanics;
- table/index/key/partition strategy;
- database migration mechanics;
- database-specific test/operational tooling;
- PostgreSQL-native FTS / pgvector production implementation;
- PostGIS / PgBouncer integration where applicable.

None is authorized merely by appearing here. Exact implementation still requires the Backend/Development gate and must preserve accepted semantics plus applicable PSV obligations.

TypeDB- or Neo4j-specific production infrastructure is **not part of the accepted initial Physical target** and requires an explicit later architecture reopen if reintroduced.

## Runtime/API-dependent implementation details

Do not freeze prematurely:

- REST/RPC/GraphQL surface;
- concrete route/DTO versioning;
- Auth middleware/policy engine/persistence;
- idempotency storage/replay mechanics;
- outbox/inbox/publication implementation details;
- bounded worker implementation details;
- concrete Restate binding/deployment activation;
- provider adapters;
- AI provider/model/router/tool adapters;
- AI evaluation frameworks/datasets/runners/thresholds;
- MCP/A2A adapters;
- projection/cache implementation details;
- OpenTelemetry SDK/Collector/backend configuration;
- calendar provider SDK/adapters;
- OR-Tools service/module topology.

## Future backend bootstrap deliverables

Only after authorization, likely foundation work includes:

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
- provider-neutral interfaces where accepted contracts require them;
- explicit API/application/semantic/persistence/provider/runtime separation.

Physical/runtime/provider-specific deliverables are added according to the accepted target and the exact authorized slice.

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
- all applicable post-selection Physical validation obligations;
- migrations/rollback only when the implemented Physical design uses them;
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
SELECTED != DEPLOYED
SELECTED != DIRECT PASS
NOT RUN != PASS
```

All `WL-H01..WL-H12`, Phase-5 requirements, Phase-6 boundaries, Phase-7..9 contracts, Phase-10 evidence rules, Phase-11 controls, Pre-Physical closure constraints, accepted Physical ownership boundaries and PSV conditions remain downstream constraints.

## Where to work when eventually authorized

Do **not** create the Backend branch now.

When every remaining prerequisite is satisfied and the user explicitly authorizes Backend Foundation:

1. re-read current `main` and this handoff;
2. verify complete accepted Domain/Logical/Physical authorities and Development Profile;
3. verify effective repository rules/checks;
4. define exact backend scope/path ownership and first slice;
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
CLOSED / SELECTED / ACCEPTED
INTEGRATED INTO MAIN VIA PR #15
MAIN e6f191bad947388a44defe2c15f4939345084f58
FORMER feature/physical-model MERGED / AUTO-DELETED

DIRECT SELECTED-STACK IMPLEMENTATION VALIDATION
NOT STARTED / DIRECT HG PASS 0

CURRENT PROJECT ACTION
Development Profile v0 — separate bounded operational-design scope

BACKEND ELIGIBILITY
Physical acceptance blocker CLEARED
Backend remains DEFERRED until explicit authorization + remaining slice/profile prerequisites
```
