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
8. [`workstreams/physical-model.md`](workstreams/physical-model.md)
9. [`physical-model/README.md`](physical-model/README.md) + all current Physical bootstrap documents
10. [`architecture/README.md`](architecture/README.md) and linked Phase-5..10 current sources
11. complete Domain/Logical closure authority where Physical mapping semantics are involved
12. relevant ADRs/evidence/methodologies
13. current Git refs/branch relation to `main`

## Current backend/architecture stage

```text
PRODUCT / NORTH STAR
CURRENT

CORE DOMAIN MODEL / DOMAIN ATLAS
CLOSED — PR #10
Whole-Domain PASS WITH HARDENING / POST-WRITE QA PASS

LOGICAL MODEL
CLOSED — PR #11
Whole-Logical PASS WITH HARDENING / REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active downstream

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
DEFINITIVE CLOSED / FINAL QA PASS
INTEGRATED / POST-MERGE VERIFIED
PR #13 + current-truth alignment PR #14

PHYSICAL MODEL
AUTHORIZED / IN PROGRESS — PM-00 BOOTSTRAP
branch feature/physical-model
base main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79
mapping NOT STARTED
benchmark execution NOT STARTED
technology selection NONE

BACKEND PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED
```

Exact active handoff: [`workstreams/physical-model.md`](workstreams/physical-model.md).

## Current semantic/model sources

### Product

- [`product/product-identity-and-north-star.md`](product/product-identity-and-north-star.md) — current Product/North Star.

### Domain

The Domain authority is cumulative. Current closure is established by the complete chain, including:

- [`domain/README.md`](domain/README.md);
- [`domain/README-part-20.md`](domain/README-part-20.md);
- [`domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md`](domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md);
- [`domain/language-map.md`](domain/language-map.md) + [`domain/language-map-part-22.md`](domain/language-map-part-22.md).

Current Domain state: **CLOSED**.

### Logical

- [`logical-model/whole-logical-model-v1.md`](logical-model/whole-logical-model-v1.md);
- complete `logical-model/decision-and-assumption-register-v1*` chain;
- [`logical-model/checkpoints/whole-logical-v1-remote-qa.md`](logical-model/checkpoints/whole-logical-v1-remote-qa.md).

Current Logical state: **CLOSED**.

Product/UI terminology does not override accepted Domain/Logical semantics.

## Active Physical Model sources

Current execution authority:

- [`physical-model/README.md`](physical-model/README.md) — active Physical authority/index;
- [`physical-model/execution-methodology-v1.md`](physical-model/execution-methodology-v1.md) — PM-00..PM-14 methodology;
- [`physical-model/execution-template-v1.md`](physical-model/execution-template-v1.md) — reproducible mapping/run/evidence template;
- [`physical-model/acceptance-test-matrix-v1.md`](physical-model/acceptance-test-matrix-v1.md) — HG/CG/corpus/scenario ledger;
- [`physical-model/result-register-v1.md`](physical-model/result-register-v1.md) — current candidate/result state;
- [`workstreams/physical-model.md`](workstreams/physical-model.md) — live save-game.

Phase-10 method authority consumed by the Physical workstream:

- [`architecture/physical-benchmark-specification.md`](architecture/physical-benchmark-specification.md);
- [`architecture/physical-benchmark-scenario-corpus.md`](architecture/physical-benchmark-scenario-corpus.md);
- [`architecture/physical-benchmark-register.md`](architecture/physical-benchmark-register.md).

The method is not duplicated or redefined by the new Physical files.

## Current architecture sources

Also read:

- [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md)
- [`architecture/requirements/README.md`](architecture/requirements/README.md) + all four Phase 5 packages
- [`architecture/ai-context-runtime-boundaries.md`](architecture/ai-context-runtime-boundaries.md)
- [`architecture/integration-hub-boundaries.md`](architecture/integration-hub-boundaries.md)
- [`architecture/durable-execution-benchmark.md`](architecture/durable-execution-benchmark.md)
- [`architecture/governed-operation-effect-contract.md`](architecture/governed-operation-effect-contract.md)
- [`architecture/search-observability-calendar-solver-boundaries.md`](architecture/search-observability-calendar-solver-boundaries.md)
- [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md)
- [`architecture/pre-physical-clean-room-qa.md`](architecture/pre-physical-clean-room-qa.md)
- [`architecture/pre-physical-final-coherence-audit.md`](architecture/pre-physical-final-coherence-audit.md)
- [`architecture/system-overview.md`](architecture/system-overview.md)
- [`architecture/technical-decisions.md`](architecture/technical-decisions.md)

Historical `architecture/domain-model-logical-readiness*` files remain truthful transition/validation evidence, not current architecture specifications.

## Current architecture posture

### Phase 5

AuthN/AuthZ, security/privacy/retention/recovery, consistency/side-effects and non-functional/multi-device/operational recovery remain the four current requirement owners. Phase 10 converted them into benchmark hard gates/scenarios; the active Physical workstream executes candidate evidence without inventing missing business targets.

### Phase 6

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

Runtime Agent/Principal is not Domain Actor automatically; tool/protocol actions are not canonical governed effects; `ExternalRef != NativeRef`; provider revision != `MaterialStateRef`.

Material consequential AI changes require versioned/reproducible evaluation before promotion. `eval result != canonical truth`; `eval PASS != Authority/effect authorization`.

### Phase 7–9

```text
DURABLE EXECUTION
Restate preferred — NOT selected
Temporal strongest mandatory challenger — NOT selected
DBOS conditional — NOT selected
local/bounded Python SQLite-capable
production PostgreSQL-recommended
distributed multi-server PostgreSQL-coupled

SEARCH
structured + lexical/full-text baseline
semantic/vector bounded

OBSERVABILITY
OpenTelemetry-first / equivalent direction

CALENDAR
standards/providers = adapter pressure, not ontology

SOLVER
simple deterministic rules/heuristics baseline
OR-Tools CP-SAT preferred specialized benchmark candidate — NOT implemented
```

### Phase 10 + Physical execution

```text
PRIMARY
PostgreSQL hybrid — preferred mandatory baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH
G0 no-specialized-store baseline vs G1 Neo4j

SEARCH / VECTOR
S0 structured + lexical/full-text baseline vs S1 bounded pgvector where applicable
```

Hard correctness gates precede weighted scoring. LOW/BASE/HIGH are synthetic qualification envelopes, not forecasts. Unexecuted tiers remain unverified. `PREFERRED != SELECTED`.

The active Physical progression is:

```text
PM-00 bootstrap
PM-01 read-only candidate/environment freeze
PM-02 mapping design
PM-03 hard-gate preflight
PM-04 harness/fixture design
PM-05 correctness/destructive execution
PM-06 performance/tiers
PM-07 recovery/evolution/failure
PM-08 secondary lanes
PM-09 scoring/sensitivity
PM-10 recommendation
PM-11 explicit selection gate
PM-12 accepted Physical Model
PM-13 independent clean-room QA
PM-14 closure/main integration
```

## Repository safety

Effective `lifeos-main-safety` remains the protected-main integration policy. `feature/physical-model` is an active bounded branch. Do not invent required CI checks before stable real contexts exist, and do not treat benchmark-only code/evidence as production backend infrastructure automatically.

## Documentation architecture rule

```text
CURRENT SPECIFICATION = current truth only
ADR = rationale + explicit supersession/qualification
HISTORICAL / VALIDATION EVIDENCE = truthful chronology
GIT / PR HISTORY = recoverable history
```

A size/tool-limit split preserves the complete logical payload losslessly and is not summary/condensation/hidden semantic rewrite.

## Active parallel workstream

Phase 4 Home/Today remains separate on `prototype/phase-4-today-home`.

## Explicit current boundary

```text
PRE-PHYSICAL
DEFINITIVE CLOSED / INTEGRATED / VERIFIED

PHYSICAL MODEL
AUTHORIZED / IN PROGRESS — PM-00 BOOTSTRAP
MAPPING NOT STARTED
BENCHMARK NOT STARTED
SELECTION NONE

BACKEND FOUNDATION
NOT STARTED / DEFERRED
```

After PM-00 remote QA, the exact next step is PM-01 **READ-ONLY FIRST**. It freezes exact current candidate versions/editions/deployment modes and the available benchmark environment from official primary sources, then stops before any mapping/schema/harness write.