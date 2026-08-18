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

Domain/Logical closure does not select Physical persistence/API/Auth/runtime/backend implementation.

## Active parallel product/design track

### Phase 4 — UX prototype/product-structure validation

Separate workstream on `prototype/phase-4-today-home`.

It may continue independently but does not redefine accepted Domain/Logical/backend architecture.

## Backend/architecture preparation track

### Pre-Physical Repository & Architecture Coherence

Branch: `chore/pre-physical-coherence`  
Handoff: [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md)

Current progress:

```text
Phase 0 — baseline/freeze
PASS

Phase 1 — global current-truth entry-point alignment
QA PASS

Phase 2 — architecture supersession/current-truth cleanup
QA PASS

Phase 3 — Backend Foundation handoff cleanup
QA PASS

Phase 4 — Current Pre-Physical Architecture Baseline
QA PASS

Phase 5 — requirements that can constrain Physical design
QA PASS

Phase 6 — AI/context/runtime/integration boundaries
QA PASS

Phase 7 — durable workflow / async benchmark
QA PASS WITH CONDITIONAL RANKING

Phase 8 — governed API / command / effect contract
QA PASS

Phase 9 — search / observability / calendar / solver pressure
QA PASS

Phase 10 — Physical benchmark specification/register/method
QA PASS

Phase 11 — repository engineering safety
QA PASS

Phase 12 — clean-room repository/architecture coherence QA
QA PASS / CLOSED

Independent total Pre-Physical audit
CORE PASS
bounded final repairs incorporated
final exact remote activation QA pending
```

Current whole-workstream state:

```text
PRE-PHYSICAL COHERENCE
FINAL CLOSURE CANDIDATE
```

The final audit record is [`architecture/pre-physical-final-coherence-audit.md`](architecture/pre-physical-final-coherence-audit.md).

No `main` integration is performed by this closure gate.

## Documentation architecture rule

Current specifications contain current truth only. Obsolete design chronology does not accumulate inside them.

```text
CURRENT SPECIFICATION = current truth only
ADR = rationale + explicit supersession/qualification
HISTORICAL / VALIDATION EVIDENCE = truthful chronology
GIT / PR HISTORY = recoverable history
```

Before replacing/deleting stale current documentation:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```

A physical split is not separate authority. A size/tool-limit split must preserve the complete logical payload losslessly and must not become summary/condensation/hidden semantic rewrite.

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
- final independent audit evidence/activation contract.

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

The current Phase 6 contract now makes explicit that materially consequential changes to model/model version/provider, prompt/instruction layer, Context Builder policy, tool/action schema, tool-selection policy or fallback/routing policy require versioned/reproducible evaluation before promotion.

Pressure includes structured output, false canonical claims, tool errors, governance bypass, privacy/inference leakage, stale context, substitution regression, fallback/refusal, human-approval flows and material cost/latency.

```text
eval result != canonical LifeOS truth
eval PASS != Authority / governed-effect authorization
```

Concrete evaluation tooling/thresholds remain later engineering choices.

## Phase 11 repository engineering safety

`lifeos-main-safety` is active and effective for protected-main integration. Current owner-driven rules require PR integration, block deletion/force-push, require review-thread resolution, use zero required approvals while no independent reviewer exists and have no required CI checks until real stable check contexts exist. Auto-delete merged head branches is enabled.

Repository-safety settings do not start backend implementation.

## Phase 12 + independent final audit

Phase 12 is **QA PASS / CLOSED**.

The broader independent total audit then checked the full branch delta for:

- accidental semantic/architecture regressions;
- stale current instructions;
- missing/superseded knowledge;
- current-vs-history misclassification;
- unintended scope changes;
- false PASS/CLOSED claims;
- repository-rules inconsistencies;
- accidental Physical/backend work;
- Product/Domain/Logical/current-architecture contradiction;
- factual technology errors.

Core result:

```text
DOMAIN REOPEN REQUIRED              0
LOGICAL REOPEN REQUIRED             0
NEW DOMAIN OWNER REQUIRED           0
MAJOR SEMANTIC CONTRADICTION        0
MAJOR ARCHITECTURAL CONTRADICTION   0
PHYSICAL ACCIDENTALLY STARTED       0
BACKEND ACCIDENTALLY STARTED        0
MAJOR KNOWLEDGE LOSS                0
```

Bounded repairs are incorporated. The final audit activation contract still requires exact remote compare/readback before definitive closure is claimed.

## Immediate next — final branch-local closure QA

```text
FINAL REMOTE ACTIVATION QA
```

Required proof:

```text
PRE-SCOPE     1bd142afe51221211bc777f6271a642911c650fc
unique paths  23
added          1
modified      22
deleted        0
unexpected     0
behind_by      0
main           148a4cb5d5741b4a5b9667cf8d30231ebc0545f0 unchanged
critical readback PASS
```

If and only if that passes:

```text
PRE-PHYSICAL COHERENCE
DEFINITIVE CLOSED / FINAL QA PASS

PHYSICAL READINESS
ESTABLISHED
PHYSICAL MODEL NOT STARTED / NOT AUTHORIZED

MAIN INTEGRATION
PENDING / NOT PERFORMED
```

## Later sequence — not authorized by this gate

After definitive branch-local Pre-Physical closure, and only after separate approval:

```text
Pre-Physical protected PR to main
→ merge commit
→ post-merge main verification
→ separately authorize Physical Model
→ execute real Physical mappings + benchmark
→ select/accept Physical result
→ only then authorize Backend Foundation
```

## Explicitly unauthorized now

```text
merge of chore/pre-physical-coherence into main
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