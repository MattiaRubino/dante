# LifeOS Roadmap

- Last updated: 2026-08-17
- Purpose: current delivery/architecture-stage sequence, not a calendar commitment

## Completed foundations

### Product / North Star

Accepted current LifeOS identity/North Star and supporting V1 product studies are integrated.

### Core Domain Model / Domain Atlas

**CLOSED — integrated into `main` via PR #10.**

### Logical Model

**CLOSED — integrated into `main` via PR #11.**

```text
Whole-Logical PASS WITH HARDENING
REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active downstream constraints
```

Logical closure does not select Physical persistence/API/Auth/runtime/backend implementation.

## Active parallel product/design track

### Phase 4 — UX prototype/product-structure validation

Separate workstream on `prototype/phase-4-today-home`.

It may continue independently but does not redefine accepted Domain/Logical/backend architecture.

## Active backend/architecture preparation track

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

Phase 10 — Physical benchmark specification/register
QA PASS

Phase 11 — repository engineering safety
QA PASS

Phase 12 — clean-room repository/architecture coherence QA
NEXT — READ-ONLY FIRST
```

This workstream does **not** itself start the Physical Model.

## Documentation architecture rule

Current specifications contain current truth only. Obsolete design chronology does not accumulate inside them.

```text
CURRENT SPECIFICATION
= current truth only

ADR
= rationale + explicit supersession/qualification

HISTORICAL / VALIDATION EVIDENCE
= truthful chronology

GIT
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

A physical split is not separate authority. If a split exists only because of size/tool limits, all parts together must preserve the complete logical payload losslessly; a split is not summary/condensation/hidden semantic rewrite.

## Pre-Physical sequence

1. **Phase 0 — freeze/current-state inventory** — PASS.
2. **Phase 1 — global entry-point/current-truth alignment** — QA PASS.
3. **Phase 2 — architecture supersession/current-truth cleanup** — QA PASS.
4. **Phase 3 — Backend Foundation handoff cleanup** — QA PASS.
5. **Phase 4 — current Pre-Physical Architecture Baseline** — QA PASS.
6. **Phase 5 — requirements that can constrain Physical design** — QA PASS.
7. **Phase 6 — AI/context/runtime/integration boundaries** — QA PASS.
8. **Phase 7 — durable workflow / async benchmark** — QA PASS WITH CONDITIONAL RANKING.
9. **Phase 8 — governed API / command / effect contract** — QA PASS.
10. **Phase 9 — search / observability / calendar / solver pressure** — QA PASS.
11. **Phase 10 — Physical benchmark specification/register** — QA PASS.
12. **Phase 11 — repository engineering safety alignment** — QA PASS.
13. **Phase 12 — clean-room repository/architecture coherence QA and closure** — NEXT, read-only first.
14. **Separate user gate** — decide whether to authorize a Physical Model workstream.

Phases 7–9 were executed as one coordinated outer tranche while preserving strict internal checkpoint order `7 → 8 → 9`.

## Current architecture sources

Current navigation:

- [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md)
- [`architecture/requirements/README.md`](architecture/requirements/README.md) + all four Phase 5 requirement packages
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

Repository engineering safety: [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md).

The Pre-Physical Architecture Baseline coordinates decided/prohibited/open/mandatory downstream constraints but does not replace Domain/Logical/ADR authority.

## Current Physical technology posture — benchmark, not selection

```text
PRIMARY CANONICAL PERSISTENCE
PostgreSQL hybrid — preferred mandatory baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH / TRAVERSAL
no-specialized-store baseline vs Neo4j/property graph

SEARCH / SEMANTIC RETRIEVAL
structured + lexical/full-text baseline vs bounded pgvector where applicable

EVENT / DOCUMENT
bounded native mechanisms first; specialized candidate only on demonstrated gap/benefit

generic EAV / generic edge / universal meta-model
HARD REJECT FOR CANONICAL KERNEL
```

Technology selection must use LifeOS-specific correctness/history/governance/concurrency/operability/runtime/search/solver pressure under the Phase 10 benchmark method.

## Phase 5 — requirements before Physical — QA PASS

Current package begins at [`architecture/requirements/README.md`](architecture/requirements/README.md) and covers:

- AuthN/AuthZ;
- security/privacy/retention/security-aware recovery;
- consistency/side effects;
- non-functional/multi-device/operational recovery.

No Auth/security/transaction/workflow/Physical mechanism or arbitrary numeric NFR target was selected.

## Phase 6 — AI/context/runtime/integration boundaries — QA PASS

Current sources:

- [`architecture/ai-context-runtime-boundaries.md`](architecture/ai-context-runtime-boundaries.md)
- [`architecture/integration-hub-boundaries.md`](architecture/integration-hub-boundaries.md)

Current boundary keeps canonical/history/retrieved/derived/live-external/candidate/transient-LLM context separate and preserves the five Integration Hub modes.

No AI provider/model, agent framework, protocol implementation, provider adapter or workflow engine was selected.

## Phase 7–9 coordinated architecture tranche — QA PASS

### Phase 7

```text
BOUNDED ASYNC
DB + worker/outbox style = valid baseline mechanism class

DEDICATED DURABLE EXECUTION
Restate   = preferred structural-fit candidate — NOT selected
Temporal  = strongest mandatory challenger — NOT selected
DBOS      = conditional PostgreSQL-dependent challenger — NOT selected
```

### Phase 8

The governed-operation/effect contract remains engine-/transport-neutral.

```text
HTTP route / UI button / tool / AuthZ action / workflow step
!= canonical governed operation

request accepted != effect complete
provider acknowledgement != canonical completion automatically
workflow completed != Actual automatically
technical cancellation != Domain cancellation automatically
```

### Phase 9

```text
SEARCH
structured/lexical/full-text = baseline
semantic/vector = bounded candidate

OBSERVABILITY
OpenTelemetry-first / equivalent
no vendor selected

CALENDAR
iCalendar / JSCalendar / provider APIs = adapter pressure, not ontology

SOLVER
simple deterministic rules/heuristics = baseline
OR-Tools CP-SAT = preferred benchmark candidate — NOT implemented
```

## Phase 10 — Physical benchmark specification/register — QA PASS

Current package:

- [`architecture/physical-benchmark-specification.md`](architecture/physical-benchmark-specification.md)
- [`architecture/physical-benchmark-scenario-corpus.md`](architecture/physical-benchmark-scenario-corpus.md)
- [`architecture/physical-benchmark-register.md`](architecture/physical-benchmark-register.md)

Phase 10 establishes role-specific competition, non-compensable correctness hard gates, idiomatic candidate mappings under common semantic assertions, deterministic destructive scenarios, LOW/BASE/HIGH synthetic qualification tiers, NFR sensitivity handling, exact evidence pinning and result vocabulary.

It does not create a Physical schema, benchmark harness implementation or technology winner. `PREFERRED != SELECTED`.

## Phase 11 — repository engineering safety — QA PASS

Current policy: [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md).

Verified main protection:

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
required checks = 0 today
auto-delete merged head branches enabled
confirmed accidental refs removed
```

No fake CI workflow or fake required status check was introduced. Future code must create and stabilize actual tests/lint/types/security/Physical checks before promoting them into main protection.

Dependabot/secret/code-scanning status is connector-unverifiable due 403 on the security endpoints; the limitation is recorded rather than inferred.

## Phase 12 — clean-room QA and closure — NEXT

Phase 12 must be executed as if by a new agent with no chat context. It must independently reconstruct:

```text
what LifeOS is
→ source authority/current navigation
→ Domain CLOSED
→ Logical CLOSED
→ current architecture truth
→ Phase 5 requirements
→ Phase 6 boundaries
→ Phase 7–9 contracts
→ Phase 10 benchmark method
→ Phase 11 repository safety
→ what remains unauthorized
```

Target closure:

```text
REPOSITORY / ARCHITECTURE COHERENCE
PASS

DOMAIN
UNCHANGED / CLOSED

LOGICAL
UNCHANGED / CLOSED

PHYSICAL MODEL
READY FOR SEPARATE AUTHORIZATION
NOT STARTED
```

Only after Phase 12 closure may the user separately decide whether to authorize a Physical Model workstream.

## Backend Foundation / implementation — later

Backend Foundation and production implementation are **NOT STARTED / DEFERRED**.

Implementation may proceed only after Pre-Physical closure, separate Physical authorization/acceptance and the applicable accepted runtime/security/API/Physical prerequisites.

## Explicitly rejected/deferred by default

Do not introduce by default:

- permanent dev/uat/prod Git branches;
- microservices/Kubernetes by fashion;
- document/graph/meta-model storage as universal canonical kernel;
- generic EAV/generic-edge ontology;
- dedicated search/vector infrastructure without demonstrated benefit;
- one universal workflow engine for every background job;
- Restate/Temporal/DBOS adoption merely because one is preferred in a benchmark;
- Phase 10 registered/preferred database candidates as selected infrastructure;
- solver output as direct canonical state;
- fake required CI checks before real stable workflows exist;
- implicit collaboration/social implementation inside personal-first V1.

Specialized infrastructure requires measured workload benefit or sufficiently strong structural improvement in correctness, durability, security, evolvability, operational reliability or migration-risk reduction.
