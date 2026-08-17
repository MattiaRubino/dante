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
8. the active [`workstreams/`](workstreams/) handoff
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
IN PROGRESS
Phase 0–10 QA PASS
Phase 11 repository engineering safety QA PASS
Phase 12 clean-room coherence QA NEXT

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED
```

Active backend/architecture handoff: [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md).

## Current semantic/model sources

- [`product/product-identity-and-north-star.md`](product/product-identity-and-north-star.md) — current product identity/North Star.
- [`domain/README.md`](domain/README.md) — Domain Atlas entry point; read complete canonical split chains where applicable.
- [`domain/language-map.md`](domain/language-map.md) — current Domain language map.
- [`logical-model/whole-logical-model-v1.md`](logical-model/whole-logical-model-v1.md) — closed Whole Logical Model.
- complete `logical-model/decision-and-assumption-register-v1*` logical document — current Logical decisions/hardenings/deferrals unless explicitly superseded.
- [`logical-model/checkpoints/whole-logical-v1-remote-qa.md`](logical-model/checkpoints/whole-logical-v1-remote-qa.md) — canonical Logical closure evidence.

Product/UI terminology does not override accepted Domain/Logical semantics.

## Current architecture sources

Start with:

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
- [`architecture/README.md`](architecture/README.md)
- [`architecture/system-overview.md`](architecture/system-overview.md)
- [`architecture/technical-decisions.md`](architecture/technical-decisions.md)

Historical `architecture/domain-model-logical-readiness*` files remain truthful transition/validation evidence, not current architecture specifications.

## Phase 5 requirements

Current requirement owners:

- AuthN/AuthZ;
- security/privacy/retention/security-aware recovery;
- consistency/side effects;
- non-functional/multi-device/operational recovery.

Accepted requirements, explicit open parameters and deferred implementation mechanisms remain separate. Open parameters are downstream obligations, not permission for arbitrary defaults.

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
OpenTelemetry-first / equivalent = current direction
no vendor selected

CALENDAR
iCalendar / JSCalendar / provider APIs = adapter pressure, not ontology

SOLVER
simple deterministic rules/heuristics = baseline
OR-Tools CP-SAT = preferred specialized benchmark candidate — NOT implemented
```

## Phase 10 Physical benchmark method

Current package:

- [`architecture/physical-benchmark-specification.md`](architecture/physical-benchmark-specification.md)
- [`architecture/physical-benchmark-scenario-corpus.md`](architecture/physical-benchmark-scenario-corpus.md)
- [`architecture/physical-benchmark-register.md`](architecture/physical-benchmark-register.md)

Phase 10 decides **how** the later Physical Model benchmark must be run. It does not select a winner or create a Physical schema.

```text
PRIMARY
PostgreSQL hybrid — preferred mandatory baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH
no-specialized-store baseline vs Neo4j

SEARCH / VECTOR
structured + lexical/full-text baseline vs bounded pgvector

EVENT / DOCUMENT
bounded mechanisms first; specialized product only on demonstrated gap/benefit
```

Hard correctness gates precede performance scoring. LOW/BASE/HIGH values are synthetic qualification envelopes, not business forecasts. `PREFERRED != SELECTED`.

## Phase 11 repository engineering safety

Current policy: [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md).

Verified current main ruleset:

```text
lifeos-main-safety
active
~DEFAULT_BRANCH
no bypass
main deletion blocked
force-push/non-fast-forward blocked
pull request required
required approvals = 0 while owner-driven
review-thread resolution required
merge commits only
required checks = 0 until real stable workflows exist
auto-delete merged head branches enabled
```

Confirmed accidental refs were removed. Dependabot/secret/code-scanning state cannot be independently read by the connected GitHub integration because those endpoints return 403; the limitation is recorded explicitly in the safety policy.

Future implementation must add real tests/lint/types/security/Physical checks before any such context becomes required on `main`.

## Current Physical benchmark posture

No Physical technology is finally selected.

- PostgreSQL hybrid — preferred primary benchmark baseline;
- TypeDB — mandatory primary challenger;
- Neo4j/property graph — serious secondary/read-projection candidate;
- event/document mechanisms — bounded candidates;
- pgvector — bounded semantic-retrieval candidate where applicable;
- generic EAV/generic-edge/universal meta-model — hard reject for canonical kernel.

## Workstreams

- [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md) — active backend/architecture preparation; Phase 0–11 QA PASS, Phase 12 next.
- [`workstreams/today-home.md`](workstreams/today-home.md) — active separate Phase 4 UX/product workstream.
- [`workstreams/backend-foundation.md`](workstreams/backend-foundation.md) — **NOT STARTED / DEFERRED** future implementation handoff.

Domain/Logical historical branches and workstream documents are evidence, not starting points for new semantic work.

## Documentation lifecycle rule

```text
CURRENT SPECIFICATION
= current truth only

ADR
= rationale + explicit current status/supersession

HISTORICAL / VALIDATION EVIDENCE
= truthful chronology

GIT
= recoverable history
```

A physical `*-part-N` chain is one logical document. If splitting exists only because of size/tool limits, the complete payload must be preserved losslessly; a split is not a summary, condensation or hidden semantic rewrite.

Before replacing/deleting stale current documentation:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```

## Source-of-truth rule

For integrated state, current `main` wins over conversation memory and historical branches/files. For active unmerged work, bounded handoff/current files may contain newer truth only inside that scope.

## Immediate next step

```text
PHASE 12
CLEAN-ROOM REPOSITORY / ARCHITECTURE COHERENCE QA
READ-ONLY FIRST

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED
```
