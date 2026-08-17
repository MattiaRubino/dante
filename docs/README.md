# Documentation Index

This directory is the durable project memory for LifeOS. A new human/AI contributor should be able to resume from repository truth without reconstructing decisions from chat history.

## Start here

Read in this order:

1. [`../README.md`](../README.md)
2. [`PROJECT-STATUS.md`](PROJECT-STATUS.md)
3. [`development/agent-operating-manual.md`](development/agent-operating-manual.md)
4. [`development/operating-rules.md`](development/operating-rules.md)
5. [`development/documentation-and-handoff.md`](development/documentation-and-handoff.md)
6. [`development/branching-and-environments.md`](development/branching-and-environments.md)
7. [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md)
8. active/final-verification [`workstreams/`](workstreams/) handoff
9. current model/architecture index and linked current sources
10. relevant ADRs/evidence/methodologies
11. relevant implementation/tests

## Current backend/architecture stage

```text
PRODUCT / NORTH STAR
CURRENT

CORE DOMAIN MODEL / DOMAIN ATLAS
CLOSED — PR #10

LOGICAL MODEL
CLOSED — PR #11
Whole-Logical PASS WITH HARDENING / REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active downstream

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
FINAL CLOSURE CANDIDATE on chore/pre-physical-coherence
Phase 0–11 QA PASS
Phase 12 clean-room closure record written
Phase 12 activation requires exact final remote gate QA

AFTER PHASE 12
independent total repository audit required before definitive closure
NO main integration yet

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED
```

Active/final-verification backend/architecture handoff: [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md).

## Current semantic/model sources

### Product

- [`product/product-identity-and-north-star.md`](product/product-identity-and-north-star.md) — current product identity/North Star.

### Domain

The Domain authority is cumulative. The early entry payload retains truthful historical in-progress state; current closure is established by later continuations/evidence.

Read at minimum:

- [`domain/README.md`](domain/README.md) — Domain Atlas entry payload;
- [`domain/README-part-20.md`](domain/README-part-20.md) — final corrected Domain status / closure activation;
- [`domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md`](domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md) — final closure evidence;
- [`domain/language-map.md`](domain/language-map.md) plus [`domain/language-map-part-22.md`](domain/language-map-part-22.md) — terminology authority and final disposition.

Current Domain state: **CLOSED**.

### Logical

- [`logical-model/whole-logical-model-v1.md`](logical-model/whole-logical-model-v1.md) — canonical Whole-Logical content payload;
- complete `logical-model/decision-and-assumption-register-v1*` logical chain;
- [`logical-model/checkpoints/whole-logical-v1-remote-qa.md`](logical-model/checkpoints/whole-logical-v1-remote-qa.md) — separate closure activation / CLOSED evidence.

Current Logical state: **CLOSED**.

Product/UI terminology does not override accepted Domain/Logical semantics.

## Current architecture sources

Start with:

- [`architecture/README.md`](architecture/README.md)
- [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md)
- [`architecture/requirements/README.md`](architecture/requirements/README.md) + all four Phase 5 packages
- [`architecture/ai-context-runtime-boundaries.md`](architecture/ai-context-runtime-boundaries.md)
- [`architecture/integration-hub-boundaries.md`](architecture/integration-hub-boundaries.md)
- [`architecture/durable-execution-benchmark.md`](architecture/durable-execution-benchmark.md)
- [`architecture/governed-operation-effect-contract.md`](architecture/governed-operation-effect-contract.md)
- [`architecture/search-observability-calendar-solver-boundaries.md`](architecture/search-observability-calendar-solver-boundaries.md)
- [`architecture/physical-benchmark-specification.md`](architecture/physical-benchmark-specification.md)
- [`architecture/physical-benchmark-scenario-corpus.md`](architecture/physical-benchmark-scenario-corpus.md)
- [`architecture/physical-benchmark-register.md`](architecture/physical-benchmark-register.md)
- [`architecture/pre-physical-clean-room-qa.md`](architecture/pre-physical-clean-room-qa.md) — Phase 12 evidence/activation contract
- [`architecture/system-overview.md`](architecture/system-overview.md)
- [`architecture/technical-decisions.md`](architecture/technical-decisions.md)
- [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md)

Historical `architecture/domain-model-logical-readiness*` files remain truthful transition/validation evidence, not current architecture specifications.

## Phase 5 requirements

Current owners:

- AuthN/AuthZ;
- security/privacy/retention/security-aware recovery;
- consistency/side effects;
- non-functional/multi-device/operational recovery.

Accepted requirements, explicit open parameters and deferred implementation mechanisms remain distinct. Open parameters are downstream obligations, not permission for arbitrary defaults.

## Phase 6 boundaries

AI/context/runtime keeps distinct:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

Integration Hub preserves five modes: canonical import, sync/mirror, live federated read, retrieval/index projection and action/tool integration.

Runtime Agent/Principal is not Domain Actor automatically; tool/protocol actions are not canonical governed effects; `ExternalRef != NativeRef`; provider revision != `MaterialStateRef`.

## Phase 7–9 architecture posture

### Durable execution

```text
BOUNDED ASYNC
DB + worker/outbox style = valid baseline mechanism class

DEDICATED DURABLE EXECUTION
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional PostgreSQL-dependent challenger — NOT selected
```

### Governed operation/effect

Consequential operation semantics remain independent from HTTP/UI/tool/AuthZ/workflow implementation. Request, canonical, provider, runtime and reconciliation outcomes remain distinct.

### Search / observability / calendar / solver

```text
SEARCH
structured + lexical/full-text = baseline
semantic/vector = bounded candidate

OBSERVABILITY
OpenTelemetry-first / equivalent = direction
no vendor selected

CALENDAR
iCalendar / JSCalendar / provider APIs = adapter pressure, not ontology

SOLVER
simple deterministic rules/heuristics = baseline
OR-Tools CP-SAT = preferred specialized benchmark candidate — NOT implemented
```

## Phase 10 Physical benchmark method

The Phase 10 package defines **how** a later authorized Physical benchmark must run. It does not select a technology.

```text
PRIMARY
PostgreSQL hybrid — preferred mandatory baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH
no-specialized-store baseline vs Neo4j

SEARCH / VECTOR
structured + lexical/full-text baseline vs bounded pgvector
```

Hard correctness gates precede weighted scoring. LOW/BASE/HIGH are synthetic qualification envelopes, not forecasts. Evidence pins exact product/version/edition/deployment. `PREFERRED != SELECTED`.

## Phase 11 repository safety

Phase 11 is QA PASS. Effective remote `main` protection was verified through `lifeos-main-safety` rather than inferred from documentation.

Current owner-driven posture:

```text
PR required
main deletion blocked
force-push/non-fast-forward blocked
review-thread resolution required
required approvals = 0 while no independent reviewer exists
required status checks = none until real stable check contexts exist
```

Security-setting endpoints unavailable to the connector remain explicitly connector-unverifiable.

## Phase 12 clean-room QA

Current evidence: [`architecture/pre-physical-clean-room-qa.md`](architecture/pre-physical-clean-room-qa.md).

The initial clean-room review found bounded current-truth propagation/discoverability defects, not Domain/Logical or architectural contradictions. Repairs were limited to current consumer/navigation documents.

Phase 12 becomes `QA PASS / CLOSED` only after its final remote activation gate proves:

```text
unique paths 11
added 1
modified 10
deleted 0
unexpected 0
behind_by 0
main unchanged
```

After Phase 12 activation, current user instruction still requires a **separate independent total repository audit** before definitive whole Pre-Physical closure. Do not merge to `main` yet.

## Documentation architecture rule

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

A physical split is not separate authority. A size/tool-limit split must preserve the complete logical payload losslessly; it is not summary/condensation/hidden semantic rewrite.

## Active parallel workstream

Phase 4 Home/Today remains separate on `prototype/phase-4-today-home`. Prototype choices do not redefine accepted Domain/Logical/backend architecture implicitly.

## Explicit current boundary

```text
MAIN INTEGRATION
NOT AUTHORIZED YET

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND FOUNDATION
NOT STARTED / DEFERRED

NEXT AFTER PHASE 12 ACTIVATION
independent total repository audit
```
