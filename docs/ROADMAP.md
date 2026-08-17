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

Before replacing/deleting stale current docs:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```

When a canonical document is physically split, the complete continuation chain is one logical document and must be read before drawing current-state conclusions. Physical splitting is a tooling/layout mechanism, not a reason to create parallel authority.

A split performed only because of file size/tool/connector limits is a **lossless physical partition of the complete logical payload**. It must not summarize, condense, omit or hide a semantic rewrite. Chronological/evidence continuation is a distinct case and may append genuine later evidence after the previous payload.

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
12. **Phase 11 — repository engineering safety alignment** — NEXT, read-only first.
13. **Phase 12 — clean-room repository/architecture coherence QA and closure**.
14. **Separate user gate** — decide whether to authorize a Physical Model workstream.

Phases 7–9 were executed as one coordinated outer tranche to reduce repeated global-document churn while preserving separate internal dependency/QA checkpoints in the mandatory order `7 → 8 → 9`.

## Current architecture sources

Current navigation:

- [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md)
- [`architecture/requirements/README.md`](architecture/requirements/README.md) plus all four Phase 5 requirement packages
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

The Pre-Physical Architecture Baseline is the current bridge for decided/prohibited/open/mandatory downstream constraints and authorization boundaries. It coordinates but does not replace Domain/Logical/ADR authority.

The Phase 5 requirement package defines what later Physical/runtime/API/backend design must satisfy while separating accepted requirements, explicit open parameters and implementation-deferred mechanisms.

Phase 6 adds current AI/context/runtime and Integration Hub boundaries without selecting providers, agent frameworks or protocols.

Phase 7–9 adds current durable-execution benchmark posture, governed-operation/effect contract and search/observability/calendar/solver pressure without starting production implementation or Physical design.

Phase 10 adds the executable future Physical benchmark method: role-specific candidate lanes, hard correctness gates, common scenario corpus, low/base/high synthetic qualification tiers, sensitivity handling, evidence pinning and result bookkeeping. It does not select the Physical Model.

The old mixed `architecture/personal-data-ai-integration.md` current specification remains retired after knowledge-coverage QA. Its historical payload remains recoverable in Git.

The `architecture/domain-model-logical-readiness*` chain remains historical transition/validation evidence, not a current architecture specification.

## Current Physical technology posture — benchmark, not selection

```text
PRIMARY CANONICAL PERSISTENCE
PostgreSQL hybrid — current preferred baseline, NOT selected
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

## Completed Pre-Physical architecture stages

### Phase 3 — Backend Foundation handoff cleanup — QA PASS

The future Backend Foundation handoff is current but deferred. It consumes Domain + Logical rather than recreating them, treats SQLAlchemy/Alembic as Physical-dependent candidates, keeps PostgreSQL as benchmark posture rather than mandate and defers implementation-specific mechanisms until their prerequisite contracts exist.

### Phase 4 — current Pre-Physical Architecture Baseline — QA PASS

[`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md) provides the current bridge source for decided direction vs authorization, semantic prohibitions, representation/state boundaries, `WL-H01..WL-H12`, runtime-vs-Domain distinctions, benchmark posture and remaining phase ownership.

### Phase 5 — requirements before Physical — QA PASS

Current requirement index: [`architecture/requirements/README.md`](architecture/requirements/README.md).

Phase 5 establishes four current requirement documents:

- AuthN/AuthZ;
- security/privacy/retention/security-aware recovery;
- consistency/side effects;
- non-functional/multi-device/operational recovery.

No Auth/security/transaction/workflow/Physical mechanism or arbitrary numeric NFR target was selected.

Remote content QA:

```text
PRE-SCOPE
 e26f95af6d46292bf0f42aa43fa67b1f9f4fc05f

CONTENT HEAD
 c29cfe4bde47d5df4f46507a5f1717acd1903112

ahead_by       10
behind_by       0
total_commits   10
added            5
modified         5
deleted          0
unexpected       0
```

### Phase 6 — AI/context/runtime/integration boundaries — QA PASS

Current sources:

- [`architecture/ai-context-runtime-boundaries.md`](architecture/ai-context-runtime-boundaries.md);
- [`architecture/integration-hub-boundaries.md`](architecture/integration-hub-boundaries.md).

AI/context/runtime preserves:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

The Context Builder is purpose/disclosure/provenance/freshness bounded; generic AI memory is not a second canonical truth store; model output/tool calls are not accepted effects by themselves; runtime Agent/Principal is not Domain Actor automatically.

Integration Hub preserves five modes: canonical import, sync/mirror, live federated read, retrieval/index projection, action/tool integration. `ExternalRef != NativeRef`; provider revision != `MaterialStateRef`; provider success/failure does not automatically determine canonical effect truth; MCP/A2A/future protocols remain adapters.

No AI provider/model, agent framework, protocol implementation, provider adapter or workflow engine was selected.

Phase 6 content QA:

```text
PRE-SCOPE
40728080ae7a69703d40d14dd256a556516ccc58

CONTENT HEAD
67d6a0d63ecaf39379912606dcf5113550718594

ahead_by        8
behind_by       0
total_commits    8
added             2
modified          6
deleted           0
unexpected        0
```

## Coordinated Phase 7–9 architecture tranche — QA PASS

PRE-SCOPE:

`2cf77ea7e3d548147bbe2b0d87304b4d5393ff5f`

Internal checkpoint sequence:

```text
PHASE 7
Durable execution benchmark
022131c2568c0375e74563e46a22c9347b277fc5
PASS WITH CONDITIONAL RANKING
        ↓
PHASE 8
Governed operation/effect contract
1d92f9e77ecc808095086fc5497eaac88e2039fa
PASS
        ↓
PHASE 9
Search/observability/calendar/solver pressure
95df2a17b1187a590b5cba646ba0e107c038e5d3
PASS
```

Content integration HEAD:

`4cbf50ec23ede3b02a49c75bc52fa57c3b192a6d`

Remote content QA from PRE-SCOPE:

```text
ahead_by       8
behind_by      0
total_commits  8
added           3
modified        5
deleted         0
unexpected      0
```

### Phase 7 current result

LifeOS does not force every async operation into one universal workflow runtime.

```text
BOUNDED ASYNC
PostgreSQL + worker/outbox style = baseline mechanism class

DEDICATED DURABLE EXECUTION
Restate   = preferred structural-fit candidate — NOT selected
Temporal  = strongest mandatory challenger — NOT selected
DBOS      = conditional PostgreSQL-dependent challenger — NOT selected
```

Dedicated durable execution is structurally justified for operation classes involving material long waits/timers, human review, provider callbacks, crash-resume, material cancellation/timeouts, compensation or multi-step reconciliation.

No durable runtime creates exactly-once external provider reality automatically.

### Phase 8 current result

The current governed-operation/effect contract is engine-/transport-neutral and preserves semantic target/effect, expected/material state, purpose/context, governance, confirmation/autonomy, idempotency/correlation, execution class and independent canonical/provider/runtime/conflict/reconciliation results.

```text
HTTP route / UI button / tool / AuthZ action / workflow step
!= canonical Governed Operation

request accepted != effect complete
provider acknowledgement != canonical completion automatically
workflow completed != Actual automatically
technical cancellation != Domain cancellation automatically
```

Concrete routes/DTOs/API style remain deferred.

### Phase 9 current result

Search:

- structured/lexical/full-text baseline;
- semantic/vector bounded candidate;
- pgvector bounded if PostgreSQL selected;
- dedicated search/vector infrastructure not justified by default.

Observability:

- OpenTelemetry-first or equivalent standards-based direction;
- no vendor selected;
- telemetry != Domain Provenance/security audit/material history by identity.

Calendar:

- iCalendar/JSCalendar/provider APIs are interoperability/adapter pressure, not ontology;
- recurrence exceptions, timezone/DST/all-day/floating semantics and provider sync-token state are benchmark pressure.

Solver:

```text
simple deterministic rules / heuristics
BASELINE

OR-Tools CP-SAT
PREFERRED SPECIALIZED SOLVER BENCHMARK CANDIDATE — NOT IMPLEMENTED
```

Hard constraints are not silently relaxed; `UNKNOWN != INFEASIBLE`; solver output remains candidate/scenario until accepted through the governed-operation contract.

## Phase 10 — Physical benchmark specification/register — QA PASS

PRE-SCOPE:

`01df10a4267880a213ede8582b0193ff616f9a70`

Current package:

- [`architecture/physical-benchmark-specification.md`](architecture/physical-benchmark-specification.md);
- [`architecture/physical-benchmark-scenario-corpus.md`](architecture/physical-benchmark-scenario-corpus.md);
- [`architecture/physical-benchmark-register.md`](architecture/physical-benchmark-register.md).

Content HEAD:

`057df9bdc19d89ea74fcee0e5d999ebc34cf93dc`

Remote content QA:

```text
ahead_by       8
behind_by      0
total_commits  8
added           3
modified        5
deleted         0
unexpected      0
```

Phase 10 establishes:

- role-specific competition rather than one false universal database leaderboard;
- PostgreSQL hybrid vs TypeDB as mandatory primary lane;
- no-specialized-store vs Neo4j as secondary graph lane;
- structured/lexical baseline vs bounded pgvector where applicable;
- bounded event/document mechanisms with explicit admission trigger for specialized products;
- non-compensable semantic/correctness hard gates before weighted scoring;
- common semantic assertions with idiomatic candidate-specific Physical mappings;
- deterministic destructive corpus including concurrency, governance, provider divergence, deletion/restore, temporal/DST, search/vector, solver, recovery and evolution;
- LOW/BASE/HIGH synthetic qualification tiers that are explicitly **not forecasts**;
- sensitivity treatment for open RPO/RTO/latency/availability/scale inputs;
- exact product/version/edition/deployment evidence pinning;
- result vocabulary `PASS / PASS-CONDITIONAL / HOLD / REJECT / SENSITIVITY-DEPENDENT / PREFERRED`;
- `PREFERRED != SELECTED`.

Phase 10 did not create PostgreSQL tables, TypeDB schema, Neo4j projection, pgvector index, benchmark harness implementation or any Physical winner.

## Phase 11 — repository engineering safety — NEXT

Phase 11 is **read-only first**.

It should determine the repository-safety baseline needed before future production work, including as applicable:

- main-branch protection/ruleset posture;
- required review/merge constraints;
- CI/check classes that are meaningful before backend implementation;
- secret/security scanning posture;
- dependency/update policy;
- artifact/test/evidence expectations;
- how future branches/PRs prove required checks without inventing non-existent CI jobs today.

Phase 11 does not start backend implementation or the Physical Model.

## Phase 12 — clean-room QA and closure

A new agent with no chat context must reconstruct:

```text
what LifeOS is
→ current/canonical sources
→ Domain CLOSED
→ Logical CLOSED
→ current architecture truth
→ requirements/boundaries constraining downstream design
→ benchmark method/candidates
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

Only after accepted prerequisites should implementation proceed through bounded vertical slices derived from Domain + Logical + Phase 5 requirements + Phase 6–9 contracts + the accepted Physical result produced under the Phase 10 method + current runtime contracts rather than old product-label schemas.

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
- implicit collaboration/social implementation inside personal-first V1.

Specialized infrastructure may be justified by measured workload **or** strong structural benefit in correctness/durability/security/evolvability/operations/migration risk.
