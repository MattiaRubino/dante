# LifeOS Roadmap

- Last updated: 2026-08-17
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
CLOSURE RECORD WRITTEN
activation requires final exact remote gate QA
```

Current whole-workstream state:

```text
PRE-PHYSICAL COHERENCE
FINAL CLOSURE CANDIDATE
NOT YET DEFINITIVELY CLOSED
```

Per current user instruction, even after Phase 12 activates as `QA PASS / CLOSED`, one additional **independent total repository audit** must run before definitive Pre-Physical closure.

No `main` integration is authorized before that audit/closure decision.

## Documentation architecture rule

Current specifications contain current truth only. Obsolete design chronology does not accumulate inside them.

```text
CURRENT SPECIFICATION
= current truth only

ADR
= rationale + explicit supersession/qualification

HISTORICAL / VALIDATION EVIDENCE
= truthful chronology

GIT / PR HISTORY
= recoverable history
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
- Phase 7 durable-execution posture;
- Phase 8 governed operation/effect contract;
- Phase 9 search/observability/calendar/solver boundary contract;
- Phase 10 Physical benchmark method, scenario corpus and candidate register;
- Phase 11 effective repository engineering safety;
- Phase 12 clean-room evidence after activation.

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

## Current runtime/search/solver posture

```text
DURABLE EXECUTION
bounded async → DB/worker/outbox style baseline class
material durable orchestration → dedicated engine structurally justified
Restate preferred candidate / Temporal mandatory challenger / DBOS conditional
NONE SELECTED

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

## Phase 11 repository engineering safety

`lifeos-main-safety` is active and effective for protected-main integration. Current owner-driven rules require PR integration, block deletion/force-push, require review-thread resolution, use zero required approvals while no independent reviewer exists and have no required CI checks until real stable check contexts exist.

Repository-safety settings do not start backend implementation.

## Phase 12 clean-room closure

Current evidence: [`architecture/pre-physical-clean-room-qa.md`](architecture/pre-physical-clean-room-qa.md).

Initial review found five bounded current-truth/discoverability repairs and zero Domain/Logical/architectural reopen:

```text
DOMAIN REOPEN REQUIRED              0
LOGICAL REOPEN REQUIRED             0
SEMANTIC CONTRADICTION              0
ARCHITECTURAL CONTRADICTION         0
PHYSICAL MODEL STARTED              0
BACKEND STARTED                     0
REPAIR ITEMS                        5
REPAIR ITEMS REMAINING              0
```

Phase 12 activates as `QA PASS / CLOSED` only if final remote QA proves exactly:

```text
unique paths 11
added 1
modified 10
deleted 0
unexpected 0
behind_by 0
main unchanged
```

## Next — after Phase 12 activation

```text
INDEPENDENT TOTAL REPOSITORY AUDIT
```

This is deliberately broader than Phase 12's clean-room closure gate. It must inspect the relevant repository/workstream end-to-end for:

- accidental semantic or architecture regressions;
- stale current instructions still hiding outside the primary entry points;
- missing/superseded knowledge;
- erroneous current-vs-history classifications;
- unintended path/scope changes from the Pre-Physical workstream;
- false PASS/CLOSED claims;
- branch/PR/ruleset inconsistencies;
- Physical/backend work accidentally started or implied;
- contradictions between Product, Domain, Logical and current architecture;
- anything that should block definitive closure.

Only if that audit passes may the user separately authorize:

```text
PRE-PHYSICAL COHERENCE
DEFINITIVE CLOSED
```

## Later sequence — not authorized now

After definitive Pre-Physical closure, and only after separate approval:

```text
Pre-Physical PR / protected-main integration
→ post-merge main verification
→ separately authorize Physical Model
→ execute real Physical mappings + benchmark
→ select/accept Physical result
→ only then authorize Backend Foundation
```

The exact ordering of Physical authorization versus repository integration must follow the final closure decision and current `main` state at that time; nothing in this roadmap authorizes either step automatically.

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
