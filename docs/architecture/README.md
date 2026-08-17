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
5. [`system-overview.md`](system-overview.md) — current logical/system boundary overview;
6. [`technical-decisions.md`](technical-decisions.md) — current decided technical directions and explicitly open benchmark choices;
7. [`../domain/README.md`](../domain/README.md) and [`../domain/language-map.md`](../domain/language-map.md) — accepted Domain Atlas semantics; read their complete physical continuation chains where split;
8. [`../logical-model/whole-logical-model-v1.md`](../logical-model/whole-logical-model-v1.md) plus the complete decision/assumption-register chain — accepted Logical Model and current downstream decisions/hardenings;
9. [`../logical-model/checkpoints/whole-logical-v1-remote-qa.md`](../logical-model/checkpoints/whole-logical-v1-remote-qa.md) — Logical Model closure evidence;
10. [`../workstreams/pre-physical-coherence.md`](../workstreams/pre-physical-coherence.md) — active Pre-Physical workstream and still-open phase ownership.

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

## Current stage boundary

```text
Domain Model
CLOSED

Logical Model
CLOSED

Pre-Physical Repository & Architecture Coherence
IN PROGRESS
Phase 5 requirement packages accepted
Phase 6 AI/context/runtime/integration boundary contracts established on active branch

Physical Model
NOT STARTED / NOT AUTHORIZED

Backend production implementation
NOT STARTED / DEFERRED
```

The current persistence posture is a benchmark posture, not a final Physical selection:

- PostgreSQL hybrid — current preferred baseline;
- TypeDB — mandatory challenger;
- Neo4j/property graph — serious secondary/read-projection candidate;
- event/document mechanisms — bounded candidates;
- generic EAV/generic-edge/universal meta-model — rejected for the canonical kernel.

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
