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
8. relevant [`workstreams/`](workstreams/) handoff
9. [`architecture/README.md`](architecture/README.md) and linked current architecture/model sources
10. Phase 12 + final independent audit evidence
11. relevant ADRs/evidence/methodologies
12. relevant implementation/tests
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
DEFINITIVE CLOSED / FINAL QA PASS — integrated into main via PR #13
Phase 0–11 QA PASS
Phase 12 QA PASS / CLOSED
Independent total audit PASS
activation checkpoint 9c53e812d13ffd1b3d3d3dc20b8b162799e13c1d
post-merge main checkpoint 74593ae283ce5a1d22335502480ee3fa54be0436

PHYSICAL MODEL
READY FOR SEPARATE AUTHORIZATION
NOT STARTED / NOT AUTHORIZED

BACKEND PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED

MAIN INTEGRATION
COMPLETE / POST-MERGE VERIFIED
PR #13
```

Exact handoff: [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md).

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
- [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md)
- [`architecture/pre-physical-clean-room-qa.md`](architecture/pre-physical-clean-room-qa.md)
- [`architecture/pre-physical-final-coherence-audit.md`](architecture/pre-physical-final-coherence-audit.md)
- [`architecture/system-overview.md`](architecture/system-overview.md)
- [`architecture/technical-decisions.md`](architecture/technical-decisions.md)

Historical `architecture/domain-model-logical-readiness*` files remain truthful transition/validation evidence, not current architecture specifications.

## Current architecture posture

### Phase 5

AuthN/AuthZ, security/privacy/retention/recovery, consistency/side-effects and non-functional/multi-device/operational recovery remain the four current requirement owners. Phase 10 already consumed them into benchmark method/hard gates/scenarios; the later separately authorized Physical Model executes candidate evidence and resolves ranking-dependent open parameters.

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

Material consequential AI behavior changes require versioned/reproducible evaluation before promotion. `eval result != canonical truth`; `eval PASS != Authority/effect authorization`.

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

### Phase 10

```text
PRIMARY
PostgreSQL hybrid — preferred mandatory baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH
no-specialized-store baseline vs Neo4j

SEARCH / VECTOR
structured + lexical/full-text baseline vs bounded pgvector
```

Hard correctness gates precede weighted scoring. LOW/BASE/HIGH are synthetic qualification envelopes, not forecasts. Unexecuted tiers remain unverified. `PREFERRED != SELECTED`.

### Phase 11

Effective `lifeos-main-safety` was remotely verified. Current owner-driven `main` posture requires PR integration, blocks deletion/force-push, requires review-thread resolution, uses zero approvals while no independent reviewer exists, has no required CI checks until real stable check contexts exist, and auto-deletes merged head branches.

## Phase 12 + final independent audit

Phase 12 clean-room QA is **QA PASS / CLOSED**. Evidence: [`architecture/pre-physical-clean-room-qa.md`](architecture/pre-physical-clean-room-qa.md).

The subsequent independent total audit reviewed the full Pre-Physical delta and found no major semantic/architectural contradiction, Domain/Logical reopen need, material knowledge loss or accidental Physical/backend implementation. Its bounded current-truth/factual/engineering repairs were applied and remotely activated at checkpoint `9c53e812d13ffd1b3d3d3dc20b8b162799e13c1d` with exactly:

```text
unique paths 23
added 1
modified 22
deleted 0
unexpected 0
behind_by 0
main unchanged
critical readback PASS
```

Final evidence: [`architecture/pre-physical-final-coherence-audit.md`](architecture/pre-physical-final-coherence-audit.md).

PR #13 subsequently integrated the closed Pre-Physical workstream into protected `main` at merge commit `74593ae283ce5a1d22335502480ee3fa54be0436`. Post-merge verification proved the final branch tree and merged `main` tree differ by one merge commit and zero files; the merged head branch was auto-deleted.

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
DEFINITIVE CLOSED / FINAL QA PASS
INTEGRATED INTO MAIN VIA PR #13
POST-MERGE VERIFIED

MAIN INTEGRATION
COMPLETE

PHYSICAL MODEL
READY FOR SEPARATE AUTHORIZATION
NOT STARTED / NOT AUTHORIZED

BACKEND FOUNDATION
NOT STARTED / DEFERRED
```

The next architecture/model action requires separate explicit user authorization to start the Physical Model. Backend Foundation remains deferred until the Physical result is separately accepted.