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
FINAL CLOSURE CANDIDATE on chore/pre-physical-coherence
Phase 0–11 QA PASS
Phase 12 QA PASS / CLOSED
independent total audit CORE PASS
bounded final repairs incorporated
exact final remote activation QA pending

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED

MAIN INTEGRATION
NOT PERFORMED
```

Exact handoff: [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md).

## Current semantic/model sources

### Product

- [`product/product-identity-and-north-star.md`](product/product-identity-and-north-star.md) — current product identity/North Star.

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
- [`architecture/pre-physical-clean-room-qa.md`](architecture/pre-physical-clean-room-qa.md) — Phase 12 evidence
- [`architecture/pre-physical-final-coherence-audit.md`](architecture/pre-physical-final-coherence-audit.md) — independent total-audit/final closure evidence
- [`architecture/system-overview.md`](architecture/system-overview.md)
- [`architecture/technical-decisions.md`](architecture/technical-decisions.md)

Historical `architecture/domain-model-logical-readiness*` files remain truthful transition/validation evidence, not current architecture specifications.

## Phase 5 requirements

Current owners:

- AuthN/AuthZ;
- security/privacy/retention/security-aware recovery;
- consistency/side effects;
- non-functional/multi-device/operational recovery.

Phase 10 already consumed them into benchmark method/hard gates/scenarios. The later separately authorized Physical Model executes candidate evidence and resolves ranking-dependent open parameters. Open parameters are downstream obligations, not arbitrary defaults.

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

Material consequential AI behavior changes require versioned/reproducible evaluation before promotion. `eval result != canonical truth`; `eval PASS != Authority/effect authorization`.

## Phase 7–9 architecture posture

### Durable execution

```text
BOUNDED ASYNC
DB + worker/outbox style = valid baseline mechanism class

DEDICATED DURABLE EXECUTION
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional challenger — NOT selected
          SQLite-capable local/bounded Python use
          PostgreSQL-recommended production
          distributed multi-server PostgreSQL-coupled
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

Hard correctness gates precede weighted scoring. LOW/BASE/HIGH are synthetic qualification envelopes, not forecasts. Unexecuted tiers remain unverified. Evidence pins exact product/version/edition/deployment. `PREFERRED != SELECTED`.

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
auto-delete merged head branches = enabled
```

Security-setting endpoints unavailable to the connector remain explicitly connector-unverifiable.

## Phase 12 + final independent audit

Phase 12 clean-room QA is **QA PASS / CLOSED**. Evidence: [`architecture/pre-physical-clean-room-qa.md`](architecture/pre-physical-clean-room-qa.md).

The subsequent independent total audit reviewed the full Pre-Physical delta and found no major semantic/architectural contradiction, Domain/Logical reopen need, material knowledge loss or accidental Physical/backend implementation. It found only bounded current-truth/factual/engineering repairs, now incorporated.

Final audit evidence: [`architecture/pre-physical-final-coherence-audit.md`](architecture/pre-physical-final-coherence-audit.md).

Definitive branch-local closure activates only after exact remote QA proves:

```text
PRE-SCOPE 1bd142afe51221211bc777f6271a642911c650fc
unique paths 23
added 1
modified 22
deleted 0
unexpected 0
behind_by 0
main unchanged at 148a4cb5d5741b4a5b9667cf8d30231ebc0545f0
critical readback PASS
```

Until then status is `FINAL CLOSURE CANDIDATE`.

## Documentation architecture rule

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

A physical split is not separate authority. A size/tool-limit split must preserve the complete logical payload losslessly; it is not summary/condensation/hidden semantic rewrite.

## Active parallel workstream

Phase 4 Home/Today remains separate on `prototype/phase-4-today-home`. Prototype choices do not redefine accepted Domain/Logical/backend architecture implicitly.

## Explicit current boundary

```text
PRE-PHYSICAL
FINAL CLOSURE CANDIDATE / final remote QA pending

MAIN INTEGRATION
NOT PERFORMED

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND FOUNDATION
NOT STARTED / DEFERRED
```

After successful branch-local closure, the next step remains a separately authorized protected PR/main integration and post-merge verification — not Physical/backend implementation.