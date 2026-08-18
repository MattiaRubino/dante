# LifeOS Roadmap

- Last updated: 2026-08-18
- Purpose: current delivery/architecture-stage sequence, not a calendar commitment

## Completed foundations

### Product / North Star

Accepted current LifeOS identity/North Star and supporting product studies are integrated.

### Core Domain Model / Domain Atlas

**CLOSED — integrated into `main` via PR #10.**

```text
Whole-Domain PASS WITH HARDENING
POST-WRITE QA PASS
```

### Logical Model

**CLOSED — integrated into `main` via PR #11.**

```text
Whole-Logical PASS WITH HARDENING
REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active downstream
```

### Pre-Physical Repository & Architecture Coherence

**DEFINITIVE CLOSED / FINAL QA PASS — integrated into `main` via PR #13 and post-merge verified.**

```text
Phase 0–11        QA PASS
Phase 12          QA PASS / CLOSED
Independent audit PASS
Activation checkpoint
9c53e812d13ffd1b3d3d3dc20b8b162799e13c1d

Protected main integration
PR #13
74593ae283ce5a1d22335502480ee3fa54be0436
POST-MERGE VERIFIED
```

The merged head branch `chore/pre-physical-coherence` was auto-deleted after integration. The closed/integrated result does not select Physical persistence or start backend implementation.

## Active parallel product/design track

### Phase 4 — UX prototype/product-structure validation

Separate workstream on `prototype/phase-4-today-home`.

It may continue independently but does not redefine accepted Domain/Logical/backend architecture.

## Closed and integrated Pre-Physical result

The final independent audit confirmed:

```text
CORE ARCHITECTURE HOLDS                 PASS
DOMAIN REOPEN REQUIRED                     0
LOGICAL REOPEN REQUIRED                    0
NEW DOMAIN OWNER REQUIRED                  0
MAJOR SEMANTIC CONTRADICTION                0
MAJOR ARCHITECTURAL CONTRADICTION           0
PHYSICAL ACCIDENTALLY STARTED               0
BACKEND ACCIDENTALLY STARTED                0
MAJOR KNOWLEDGE LOSS                        0
TECHNOLOGY ACCIDENTALLY SELECTED            0
```

The bounded final repairs included:

- removal of stale stage-handoff prose from current specs;
- Phase 10 method vs future Physical execution clarification;
- repository bootstrap/hygiene alignment;
- DBOS coupling correction: SQLite-capable local/bounded Python use, PostgreSQL-recommended production, distributed multi-server PostgreSQL-coupled;
- explicit versioned/reproducible consequential AI change evaluation requirement;
- explicit `unexecuted upper benchmark envelope != VERIFIED-RUN` handling.

Protected integration then preserved the final branch tree exactly: `34e9ea3b547922600cb472adf1549a321e6ddfe4 → 74593ae283ce5a1d22335502480ee3fa54be0436` is one merge commit ahead with zero file differences.

## Current Pre-Physical architecture inputs

The following remain current downstream constraints:

- CLOSED Domain Atlas and final closure/status continuations;
- CLOSED Whole Logical Model + complete decision/assumption-register chain + remote QA closure;
- Phase 5 AuthN/AuthZ, security/privacy/retention/recovery, consistency/side-effects and NFR/multi-device/recovery requirements;
- Phase 6 AI/context/runtime and Integration Hub boundaries;
- consequential AI behavior changes promotion-gated by versioned/reproducible evaluation;
- Phase 7 durable-execution posture;
- Phase 8 governed operation/effect contract;
- Phase 9 search/observability/calendar/solver boundary contract;
- Phase 10 Physical benchmark method, scenario corpus and candidate register;
- Phase 11 effective repository engineering safety;
- Phase 12 clean-room evidence;
- final independent audit evidence;
- PR #13 / post-merge `main` verification.

## Current Physical benchmark posture

No Physical technology is selected.

```text
PRIMARY CANONICAL
PostgreSQL hybrid — preferred mandatory baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH
no-specialized-store baseline vs Neo4j

SEARCH / VECTOR
structured + lexical/full-text baseline vs bounded pgvector where applicable

EVENT / DOCUMENT
bounded mechanisms first; specialized candidate only on demonstrated gap/benefit

generic EAV / generic edge / universal meta-model
HARD REJECT FOR CANONICAL KERNEL
```

Phase 10 defines how a later authorized benchmark must run. `PREFERRED != SELECTED`.

LOW/BASE/HIGH values are synthetic qualification envelopes, not business forecasts. Unexecuted tiers are not `VERIFIED-RUN`; progressive saturation/scaling evidence may support sensitivity only when its limits are explicit.

## Current runtime/search/solver posture

```text
DURABLE EXECUTION
bounded async → DB/worker/outbox style baseline class
material durable orchestration → dedicated engine structurally justified
Restate preferred candidate — NOT selected
Temporal mandatory strongest challenger — NOT selected
DBOS conditional challenger — NOT selected
     local/bounded Python SQLite-capable
     production PostgreSQL-recommended
     distributed multi-server PostgreSQL-coupled

SEARCH
structured + lexical/full-text baseline
semantic/vector bounded
no dedicated service by default

OBSERVABILITY
OpenTelemetry-first / equivalent direction
no vendor selected

CALENDAR
iCalendar / JSCalendar / providers = adapter pressure, not ontology

SOLVER
simple deterministic rules/heuristics baseline
OR-Tools CP-SAT preferred benchmark candidate — NOT implemented
```

## AI evaluation posture

Materially consequential changes to model/model version/provider, prompt/instruction layer, Context Builder policy, tool/action schema, tool-selection policy or fallback/routing policy require versioned/reproducible evaluation before promotion.

```text
eval result != canonical LifeOS truth
eval PASS != Authority / governed-effect authorization
```

Concrete evaluation tooling/thresholds remain later engineering choices.

## Repository engineering safety

`lifeos-main-safety` was remotely verified during Phase 11. Current owner-driven rules require PR integration, block deletion/force-push, require review-thread resolution, use zero required approvals while no independent reviewer exists and have no required CI checks until real stable check contexts exist. Auto-delete merged head branches is enabled and removed the merged Pre-Physical source branch after PR #13.

## Immediate next — separate authorization required

```text
PHYSICAL MODEL
READY FOR SEPARATE AUTHORIZATION
NOT STARTED / NOT AUTHORIZED
```

Pre-Physical protected integration and post-merge verification are complete. Do not start Physical merely because readiness is established; beginning the Physical Model requires a new explicit user authorization and a fresh workstream/write gate.

## Later sequence — separate authorizations

After Physical Model authorization:

```text
create bounded Physical workstream from current main
→ execute real Physical mappings + benchmark
→ select/accept Physical result
→ only then authorize Backend Foundation
```

## Explicitly unauthorized now

```text
direct main write
Physical schema/tables/indexes/migrations
PostgreSQL / TypeDB / Neo4j selection
SQL / TypeQL / Cypher benchmark implementation
concrete API routes / DTOs
AuthN/AuthZ implementation
Restate / Temporal / DBOS adoption
queue/outbox implementation
provider adapters
AI provider/model/agent framework
MCP/A2A adoption
dedicated search/vector deployment
observability vendor
solver implementation
production backend code
feature/backend-foundation
Domain/Logical changes without explicit reopen
```