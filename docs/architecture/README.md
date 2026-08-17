# Architecture Documentation

- Status: **Current navigation**
- Last updated: 2026-08-17

## Purpose

This directory separates **current architectural truth** from historical transition/validation evidence.

Current specifications must describe the architecture as it is understood now. They are not chronological logs. When a current specification changes, obsolete prose is replaced after a knowledge-coverage check; useful rationale/history remains recoverable through Git, ADRs, checkpoints, or explicitly historical evidence.

## Current architecture sources

Read these for the current architecture state:

1. [`pre-physical-architecture-baseline.md`](pre-physical-architecture-baseline.md) — current Pre-Physical bridge: decided/prohibited/open/mandatory downstream constraints and authorization boundary;
2. [`requirements/README.md`](requirements/README.md) — current Phase 5 Pre-Physical requirement-package index; read all four requirement packages before later Physical/runtime/API/backend design;
3. [`ai-context-runtime-boundaries.md`](ai-context-runtime-boundaries.md) — current Phase 6 AI/context/runtime boundary contract;
4. [`integration-hub-boundaries.md`](integration-hub-boundaries.md) — current Phase 6 five-mode Integration Hub/provider boundary contract;
5. [`durable-execution-benchmark.md`](durable-execution-benchmark.md) — Phase 7 durable execution/async benchmark, operation-class boundary and conditional candidate ranking;
6. [`governed-operation-effect-contract.md`](governed-operation-effect-contract.md) — Phase 8 engine-/transport-neutral governed operation/effect contract before concrete routes/DTOs;
7. [`search-observability-calendar-solver-boundaries.md`](search-observability-calendar-solver-boundaries.md) — Phase 9 search/retrieval, observability, calendar-interoperability and deterministic-solver pressure contract;
8. [`physical-benchmark-specification.md`](physical-benchmark-specification.md) — Phase 10 executable benchmark methodology: candidate lanes, hard gates, fairness, scoring, evidence and result rules;
9. [`physical-benchmark-scenario-corpus.md`](physical-benchmark-scenario-corpus.md) — Phase 10 common semantic/destructive fixtures, synthetic low/base/high qualification tiers and sensitivity cases;
10. [`physical-benchmark-register.md`](physical-benchmark-register.md) — Phase 10 role/candidate register and future result slots; registered/preferred does not mean selected;
11. [`system-overview.md`](system-overview.md) — current logical/system boundary overview;
12. [`technical-decisions.md`](technical-decisions.md) — current decided technical directions and explicitly open benchmark choices;
13. [`../domain/README.md`](../domain/README.md) and [`../domain/language-map.md`](../domain/language-map.md) — accepted Domain Atlas semantics; read their complete physical continuation chains where split;
14. [`../logical-model/whole-logical-model-v1.md`](../logical-model/whole-logical-model-v1.md) plus the complete decision/assumption-register chain — accepted Logical Model and current downstream decisions/hardenings;
15. [`../logical-model/checkpoints/whole-logical-v1-remote-qa.md`](../logical-model/checkpoints/whole-logical-v1-remote-qa.md) — Logical Model closure evidence;
16. [`../workstreams/pre-physical-coherence.md`](../workstreams/pre-physical-coherence.md) — active Pre-Physical workstream and still-open phase ownership.

A physically split canonical document is **one logical document**. Never treat the first path, the newest continuation or an isolated `*-part-N` file as complete authority.

A tool/size split must preserve the complete logical payload losslessly. Splitting a document is not permission to summarize, condense, paraphrase away, omit or silently clean up content; semantic/current-truth editing is a separate operation.

## Phase 5 requirement packages

Current Pre-Physical requirement packages are:

- [`requirements/authn-authz.md`](requirements/authn-authz.md) — authentication/security-context and authorization-enforcement requirements without `Principal = Actor = Authority` collapse;
- [`requirements/security-privacy-retention-recovery.md`](requirements/security-privacy-retention-recovery.md) — security, minimization, sensitive-data, retention/redaction/deletion and security-aware recovery requirements;
- [`requirements/consistency-side-effects.md`](requirements/consistency-side-effects.md) — expected-state, idempotency, concurrency, multi-owner consistency, provider/external side-effect and reconciliation/compensation requirements;
- [`requirements/nonfunctional-multidevice-recovery.md`](requirements/nonfunctional-multidevice-recovery.md) — multi-device/offline, latency/availability classes, scale assumptions, resilience and operational-recovery requirements.

These documents define requirements and explicit open parameters. They do not select Auth providers, policy engines, databases, schemas, transaction mechanisms, workflow/queue/outbox technologies, offline sync engines or numeric RPO/RTO/SLA targets by convenience.

## Phase 6 AI/context/runtime/integration contracts

Current boundary contracts are:

- [`ai-context-runtime-boundaries.md`](ai-context-runtime-boundaries.md) — seven context categories, Context Builder, durable/transient AI memory, provider-neutral AI Gateway, AI proposal/effect boundary, runtime Agent/Principal/Actor/tool boundaries and delayed AI/tool execution constraints;
- [`integration-hub-boundaries.md`](integration-hub-boundaries.md) — canonical import, sync/mirror, live federated read, retrieval/index projection and action/tool integration, including ExternalRef, provider revision, reconciliation, privacy/deletion and ambiguous-effect behavior.

These contracts deliberately do **not** select an AI provider/model, agent framework, MCP/A2A implementation, provider adapter, queue/workflow engine or concrete API/tool schema.

```text
AI/context/runtime representation != canonical truth by default
provider state != canonical LifeOS state
tool/protocol action != canonical governed effect
runtime Agent / Principal != Domain Actor automatically
```

## Phase 7–9 coordinated architecture contracts

### Phase 7 — durable execution / async

[`durable-execution-benchmark.md`](durable-execution-benchmark.md) establishes two execution classes rather than one universal workflow mechanism:

```text
bounded asynchronous work
→ simple DB/worker/outbox style remains a valid baseline

material long-running/recoverable coordination
→ dedicated durable execution is structurally justified
```

Current dedicated candidate posture:

```text
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional PostgreSQL-dependent challenger — NOT selected
```

The runtime does not define Domain truth; external-effect ambiguity/idempotency/reconciliation remain explicit.

### Phase 8 — governed operation / effect

[`governed-operation-effect-contract.md`](governed-operation-effect-contract.md) defines the engine-/transport-neutral consequential-operation contract around semantic target/effect, material/expected state, purpose/context, Principal/Actor/represented party, governance, confirmation/autonomy, idempotency/correlation, execution class and multi-axis result/provenance.

```text
route / UI button / tool / AuthZ action / workflow step
!= canonical governed operation/effect meaning
```

No concrete REST/RPC/GraphQL route, DTO, command bus or execution engine is selected.

### Phase 9 — search / observability / calendar / solver

[`search-observability-calendar-solver-boundaries.md`](search-observability-calendar-solver-boundaries.md) establishes:

- structured + lexical/full-text search as the baseline posture;
- vector/pgvector as bounded candidates, not semantic truth;
- no dedicated search/vector service by default without demonstrated benefit;
- OpenTelemetry-first or equivalent standards-based observability direction, with telemetry separate from Domain history/audit;
- iCalendar/JSCalendar/provider calendar models as adapter/interoperability pressure, not ontology;
- deterministic rules/heuristics as solver baseline and OR-Tools CP-SAT as preferred specialized solver benchmark candidate;
- solver output as candidate/projection that still crosses the governed-effect boundary.

No search vendor, vector database, telemetry vendor, calendar-provider model or solver implementation is selected.

## Phase 10 Physical benchmark method

The current Phase 10 package consists of three distinct logical documents:

- [`physical-benchmark-specification.md`](physical-benchmark-specification.md);
- [`physical-benchmark-scenario-corpus.md`](physical-benchmark-scenario-corpus.md);
- [`physical-benchmark-register.md`](physical-benchmark-register.md).

Phase 10 decides **how a later authorized Physical Model must be benchmarked**, not which technology wins.

The benchmark uses competition by role:

```text
PRIMARY CANONICAL LANE
PostgreSQL hybrid — mandatory preferred baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH LANE
no-specialized-store baseline
vs Neo4j

SEARCH / SEMANTIC RETRIEVAL LANE
structured + lexical/full-text baseline
vs bounded pgvector where applicable

EVENT / DOCUMENT LANE
bounded native mechanisms first
specialized candidate only on demonstrated gap/benefit
```

Primary candidates must pass non-compensable semantic/correctness hard gates before weighted performance/operability scoring. The common scenario corpus includes expected-state races, multi-owner consistency, deep history, selective disclosure, provider divergence, deletion + restore, recurrence/DST, search/vector filtering, solver freshness, recovery and schema evolution.

Low/base/high numbers are **synthetic qualification tiers**, not user-growth forecasts. Open RPO/RTO/latency/scale values remain sensitivity inputs until accepted product/operational targets exist.

Benchmark evidence is pinned to exact product version + edition + deployment mode. `PREFERRED != SELECTED` remains mandatory.

No Physical mapping/schema or benchmark implementation is authorized by the Phase 10 documentation package itself.

## Current stage boundary

```text
Domain Model
CLOSED

Logical Model
CLOSED

Pre-Physical Repository & Architecture Coherence
IN PROGRESS
Phase 5 requirement packages CURRENT
Phase 6 AI/context/runtime/integration contracts CURRENT
Phase 7 durable-execution benchmark CURRENT
Phase 8 governed-operation/effect contract CURRENT
Phase 9 search/observability/calendar/solver pressure contract CURRENT
Phase 10 Physical benchmark method package CURRENT

Physical Model
NOT STARTED / NOT AUTHORIZED

Backend production implementation
NOT STARTED / DEFERRED
```

The current persistence posture remains a benchmark posture, not a final Physical selection:

- PostgreSQL hybrid — current preferred primary baseline;
- TypeDB — mandatory primary challenger;
- Neo4j/property graph — serious secondary/read-projection candidate;
- event/document mechanisms — bounded candidates;
- pgvector — bounded semantic-retrieval candidate when applicable;
- generic EAV/generic-edge/universal meta-model — rejected for the canonical kernel.

Phase 10 provides a reproducible future decision method. It does not authorize execution of the Physical Model benchmark or production implementation.

## Historical transition / validation evidence

The following canonical chain records the truthful Domain → Logical readiness transition. It is **evidence**, not a current architecture specification:

- [`domain-model-logical-readiness.md`](domain-model-logical-readiness.md)
- [`domain-model-logical-readiness-part-2.md`](domain-model-logical-readiness-part-2.md)
- [`domain-model-logical-readiness-part-3.md`](domain-model-logical-readiness-part-3.md)
- [`domain-model-logical-readiness-part-4.md`](domain-model-logical-readiness-part-4.md)
- [`domain-model-logical-readiness-part-5.md`](domain-model-logical-readiness-part-5.md)

Those files intentionally retain READY/HOLD/reopen/restoration/clearance chronology. Do not rewrite them to look current.

## ADR handling

ADRs preserve decision rationale and explicit supersession state. An older ADR may remain useful historical evidence while no longer being current execution authority.

Current architecture specifications should not repeat obsolete ADR prose merely to preserve history. They should state the current result and link to the relevant ADR only where rationale is useful.

No new ADR is created merely to record a preferred benchmark candidate or benchmark method. A benchmark preference/method is not an implementation selection.

## Documentation rule

```text
CURRENT SPECIFICATION
= current truth only

HISTORICAL / VALIDATION EVIDENCE
= truthful chronology preserved

ADR
= decision rationale + explicit supersession/qualification

GIT
= complete recoverable file history
```

Before replacing or deleting a stale current document, classify every meaningful statement and prove:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```
