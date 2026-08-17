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

Coordinated Phase 7–9 architecture tranche
NEXT
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
8. **Coordinated Phase 7–9 architecture tranche** — NEXT, with mandatory internal order:
   - Phase 7 — durable workflow / async benchmark;
   - Phase 8 — governed API / command / effect contract;
   - Phase 9 — search / observability / calendar / solver pressure.
9. **Phase 10 — Physical benchmark specification/register**.
10. **Phase 11 — repository engineering safety alignment**.
11. **Phase 12 — clean-room repository/architecture coherence QA and closure**.
12. **Separate user gate** — decide whether to authorize a Physical Model workstream.

The combined 7–9 tranche reduces repeated global-document churn but does not collapse the internal dependencies: Phase 8 consumes Phase 7 results, Phase 9 consumes the accepted Phase 8 effect/disclosure boundary, and every internal phase keeps a separate verdict/QA checkpoint.

## Current architecture sources

Current navigation:

- [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md)
- [`architecture/requirements/README.md`](architecture/requirements/README.md) plus all four Phase 5 requirement packages
- [`architecture/ai-context-runtime-boundaries.md`](architecture/ai-context-runtime-boundaries.md)
- [`architecture/integration-hub-boundaries.md`](architecture/integration-hub-boundaries.md)
- [`architecture/README.md`](architecture/README.md)
- [`architecture/system-overview.md`](architecture/system-overview.md)
- [`architecture/technical-decisions.md`](architecture/technical-decisions.md)

The Pre-Physical Architecture Baseline is the current bridge for decided/prohibited/open/mandatory downstream constraints and authorization boundaries. It coordinates but does not replace Domain/Logical/ADR authority.

The Phase 5 requirement package defines what later Physical/runtime/API/backend design must satisfy while separating accepted requirements, explicit open parameters and implementation-deferred mechanisms.

Phase 6 adds current AI/context/runtime and Integration Hub boundaries without selecting providers, agent frameworks, protocols or workflow mechanisms.

The old mixed `architecture/personal-data-ai-integration.md` current specification has been retired after knowledge-coverage QA. Its surviving valid knowledge is carried by current architecture, ADR, Logical and Pre-Physical sources; the old payload remains recoverable in Git history.

The `architecture/domain-model-logical-readiness*` chain remains historical transition/validation evidence, not a current architecture specification.

## Current Physical technology posture — benchmark, not selection

- **PostgreSQL hybrid:** current preferred baseline, not final selection.
- **TypeDB:** mandatory challenger.
- **Neo4j/property graph:** serious secondary/read-projection challenger.
- **event store/event stream:** bounded history/integration mechanism candidate.
- **document store:** bounded provider/specialist/flexible candidate.
- **pgvector:** bounded semantic-retrieval candidate.
- **generic EAV/generic edge/universal meta-model:** hard reject for canonical kernel.
- **durable workflow technologies:** separate runtime benchmark, not persistence ontology.

Technology selection must use LifeOS-specific correctness/history/governance/concurrency/operability pressure.

## Phase 3 — Backend Foundation handoff cleanup — QA PASS

The future Backend Foundation handoff is current but deferred. It consumes Domain + Logical rather than recreating them, treats SQLAlchemy/Alembic as Physical-dependent candidates, keeps PostgreSQL as benchmark posture rather than mandate, defers concrete API/Auth/workflow/provider mechanisms, removes the old fixed product-label slice as a canonical contract, and preserves valid future Python/FastAPI/Pydantic/modular-monolith/testing/provider-boundary requirements.

Backend Foundation may become executable only after Pre-Physical closure, separate Physical acceptance and the applicable accepted runtime/security/integration/API prerequisites.

## Phase 4 — current Pre-Physical Architecture Baseline — QA PASS

[`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md) provides one current bridge source for decided direction vs authorization, semantic prohibitions, representation/state boundaries, `WL-H01..WL-H12`, runtime-vs-Domain distinctions, benchmark posture and remaining phase ownership.

## Phase 5 — requirements before Physical — QA PASS

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

CONTENT HEAD BEFORE GLOBAL CLOSURE MARKERS
 c29cfe4bde47d5df4f46507a5f1717acd1903112

ahead_by       10
behind_by       0
total_commits   10
added            5
modified         5
deleted          0
unexpected       0
```

## Phase 6 — AI/context/runtime/integration boundaries — QA PASS

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

CONTENT HEAD BEFORE GLOBAL CLOSURE MARKERS
67d6a0d63ecaf39379912606dcf5113550718594

ahead_by        8
behind_by       0
total_commits    8
added             2
modified          6
deleted           0
unexpected        0
```

## Coordinated Phase 7–9 architecture tranche — NEXT

### Internal Phase 7 — durable workflow / async benchmark

Compare at least:

- PostgreSQL + worker + transactional outbox;
- Temporal;
- Restate;
- DBOS.

Pressure must include provider retry/sync, human approval, long AI work, reconciliation, cancellation/timeouts, partial external effect, duplicate/replay, delayed governance/target change and crash/recovery.

Phase 7 may choose/qualify a durable-execution posture only after evidence; it must not become a new ontology or bypass Phase 5/6 contracts.

### Internal Phase 8 — governed API / command / effect contract

Phase 8 consumes Phase 7 results but remains mechanism-neutral at the semantic contract level.

Before concrete routes, define consequential-operation requirements around Principal/Actor/represented party, semantic target, operation/effect, expected/material state, inputs/context/purpose, governance basis, autonomy/confirmation, idempotency/correlation, delayed execution and result/provenance/conflict/partial semantics.

```text
HTTP route / UI button / tool string / AuthZ action string
!= canonical Governed Operation
```

### Internal Phase 9 — search / observability / calendar / solver pressure

Phase 9 consumes the accepted Phase 8 effect/disclosure boundary.

Pressure includes:

- search/retrieval projection separate from canonical truth;
- structured/full-text baseline and bounded pgvector candidate where applicable;
- specialized search/vector only on demonstrated benefit;
- standards-based observability with privacy minimization;
- iCalendar/JSCalendar/Google/Microsoft semantics as interoperability pressure, not ontology;
- deterministic solver/services for deterministic constraints;
- AI for ambiguity/interpretation/explanation/cross-domain reasoning where useful;
- truthful feasible/infeasible/uncertain/at-risk/conflicting/partial planner outcomes;
- search/explanation/ranking non-interference under `WL-H12`.

## Phase 10 — Physical benchmark specification/register

Benchmark destructive LifeOS scenarios including:

- concurrent consequential edits;
- expected-state conflicts;
- multi-owner changes;
- selective disclosure/inference leakage;
- provider divergence/reconciliation;
- redaction/history reconstruction;
- recurrence across DST;
- stale availability/derived state;
- AuthZ provenance;
- AI proposal → approval → effect;
- revoked consent/authority during execution;
- long-running crash/restart;
- backup/restore;
- schema evolution over historical state;
- multi-device/offline divergence;
- ambiguous external-effect failure/replay;
- restore after deletion/redaction;
- explicit low/base/high scale and performance scenarios where exact forecasts remain open.

Phase 10 must resolve or scenario-model Phase 5 open parameters when their values materially affect candidate scoring.

## Phase 11 — repository engineering safety

Before production backend implementation, establish appropriate main protection/ruleset/CI/required checks when concrete checks exist.

## Phase 12 — clean-room QA and closure

A new agent with no chat context must reconstruct:

```text
what LifeOS is
→ current/canonical sources
→ Domain CLOSED
→ Logical CLOSED
→ current architecture truth
→ requirements/boundaries constraining downstream design
→ benchmark candidates
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

## Backend Foundation / implementation — later

Backend Foundation and production implementation are **NOT STARTED / DEFERRED**.

Only after accepted prerequisites should implementation proceed through bounded vertical slices derived from Domain + Logical + Phase 5 requirements + Phase 6 boundaries + Physical/current runtime/API contracts rather than old product-label schemas.

## Explicitly rejected/deferred by default

Do not introduce by default:

- permanent dev/uat/prod Git branches;
- microservices/Kubernetes by fashion;
- document/graph/meta-model storage as universal canonical kernel;
- generic EAV/generic-edge ontology;
- specialized search/cache/vector/analytics/workflow infrastructure without demonstrated benefit;
- implicit collaboration/social implementation inside personal-first V1.

Specialized infrastructure may be justified by measured workload **or** strong structural benefit in correctness/durability/security/evolvability/operations/migration risk.
