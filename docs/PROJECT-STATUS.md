# Project Status

- Last updated: 2026-08-17
- Canonical integrated branch: `main`
- Current accepted main baseline for this workstream: `148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`
- Active backend/architecture preparation branch: `chore/pre-physical-coherence`
- Production application code: **NOT STARTED**

## Current stage

```text
PRODUCT / NORTH STAR
CURRENT

CORE DOMAIN MODEL / DOMAIN ATLAS
CLOSED — integrated through PR #10

LOGICAL MODEL
CLOSED — integrated through PR #11
Whole-Logical PASS WITH HARDENING / REMOTE QA PASS
WD-03 PASS
WD-05 PASS

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
IN PROGRESS
Phase 0 + Phase 1 QA PASS
Phase 2 architecture supersession/current-truth cleanup — QA PASS
Phase 3 Backend Foundation handoff cleanup — QA PASS
Phase 4 Current Pre-Physical Architecture Baseline — QA PASS
Phase 5 requirements that can constrain Physical design — QA PASS
Phase 6 AI/context/runtime/integration boundaries — QA PASS
Coordinated Phase 7–9 architecture tranche — NEXT

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND FOUNDATION / PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED
```

Phase 4 UX remains a separate active product/design workstream.

## Read this first

1. [`README.md`](../README.md)
2. [`docs/README.md`](README.md)
3. this file
4. [`development/agent-operating-manual.md`](development/agent-operating-manual.md)
5. [`development/operating-rules.md`](development/operating-rules.md)
6. [`development/documentation-and-handoff.md`](development/documentation-and-handoff.md)
7. [`development/branching-and-environments.md`](development/branching-and-environments.md)
8. active workstream handoff
9. [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md), [`architecture/requirements/README.md`](architecture/requirements/README.md), [`architecture/ai-context-runtime-boundaries.md`](architecture/ai-context-runtime-boundaries.md), [`architecture/integration-hub-boundaries.md`](architecture/integration-hub-boundaries.md) and [`architecture/README.md`](architecture/README.md) with linked current sources
10. relevant ADR/evidence/methodology
11. relevant implementation/tests

Conversation history is secondary to repository truth.

When a canonical document is physically split, read the complete split/continuation chain rather than treating the first path or newest part as the whole logical document.

A split caused only by size/tool limits is a lossless physical partition of the complete logical payload. It is not a summary/condensation or a hidden semantic rewrite.

## Accepted/current foundations

- [`product/product-identity-and-north-star.md`](product/product-identity-and-north-star.md) — current product identity/North Star.
- Core Domain Model / Domain Atlas — **CLOSED**.
- Logical Model — **CLOSED**, with `WL-H01..WL-H12` active downstream constraints.
- [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md) — **CURRENT** Pre-Physical bridge; `DECIDED != AUTHORIZED TO IMPLEMENT`.
- [`architecture/requirements/README.md`](architecture/requirements/README.md) + four linked Phase 5 packages — **CURRENT** requirements constraining later Physical/runtime/API/backend design.
- [`architecture/ai-context-runtime-boundaries.md`](architecture/ai-context-runtime-boundaries.md) — **CURRENT** Phase 6 AI/context/runtime contract.
- [`architecture/integration-hub-boundaries.md`](architecture/integration-hub-boundaries.md) — **CURRENT** Phase 6 five-mode Integration Hub/provider contract.
- Web direction — Next.js + React + TypeScript.
- Mobile direction — Expo + React Native + TypeScript.
- Backend direction — Python + FastAPI + Pydantic; modular monolith.
- SQLAlchemy/Alembic — conditional candidates depending on accepted Physical persistence.
- AI — replaceable/provider-neutral gateway + bounded Context Builder + governed proposals/effects.
- Integration/provider state remains distinct from canonical LifeOS state.
- DEV/UAT/PROD are deployment environments, not permanent Git branches.
- Repository visibility: **public**.

## Current Phase 5 requirement inputs

The Phase 5 package defines requirements, open parameters and deferred mechanisms separately.

Current packages:

- [`architecture/requirements/authn-authz.md`](architecture/requirements/authn-authz.md);
- [`architecture/requirements/security-privacy-retention-recovery.md`](architecture/requirements/security-privacy-retention-recovery.md);
- [`architecture/requirements/consistency-side-effects.md`](architecture/requirements/consistency-side-effects.md);
- [`architecture/requirements/nonfunctional-multidevice-recovery.md`](architecture/requirements/nonfunctional-multidevice-recovery.md).

Current constraints include, among others:

- `Person != Account != Principal != Actor` and technical allow/deny != canonical Authority/Consent/Visibility;
- actual Actor and represented party remain distinct;
- consequential AuthZ/effect provenance and delayed-governance revalidation;
- purpose-aware minimization, sensitive-data handling, truthful deletion/redaction/tombstone semantics and secure restore without forbidden-data resurrection;
- expected-state writes, idempotency != identity, no silent material last-write-wins, truthful multi-owner atomic/staged consistency and canonical/provider-effect separation;
- multi-device divergence, operation-specific offline semantics, truthful degraded/provider state, long-history/current-state access and recovery testing;
- RPO/RTO/latency/availability/scale/offline-duration values remain explicit open parameters, not invented Phase 5 constants.

Mechanisms such as Auth provider/policy engine, token/session store, encryption/KMS, outbox/inbox/queue/workflow, CRDT/OT, database schema, replication/failover and concrete offline-sync technology remain later decisions.

## Current Phase 6 boundary inputs

### AI / context / runtime

Current contract preserves:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

The Context Builder is purpose-, minimization-, disclosure-, provenance- and freshness-aware. Whole-history/full-database exposure is not the default.

LifeOS does not use generic `AI memory` as a second canonical truth store. AI output does not become effective solely because it is structured/high-confidence.

```text
runtime Agent / Principal != Domain Actor automatically
tool invocation != authorization
tool/protocol action != canonical governed operation
```

Non-human Principals, delayed tool effects, provider fallback and external/retrieved instructions remain subject to Phase 5 governance/privacy/consistency requirements.

### Integration Hub

Five current modes:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

Current invariants include:

```text
ExternalRef != NativeRef
provider revision != MaterialStateRef by identity
provider state/effect != canonical LifeOS state/effect automatically
```

Sync conflict does not use universal last-write-wins; live-read failure can remain unknown/degraded; indexes/projections remain derived/deletion-aware; external effects preserve idempotency, ambiguous-outcome and reconciliation truth. MCP/A2A/future protocols remain adapters, not ontology/governance.

AI provider/model, agent framework, provider adapters, MCP/A2A adoption and durable workflow mechanisms remain deferred.

## Current Physical benchmark posture

No Physical technology is finally selected.

- PostgreSQL hybrid — current preferred baseline;
- TypeDB — mandatory challenger;
- Neo4j/property graph — serious secondary/read-projection candidate;
- event/document mechanisms — bounded candidates;
- generic EAV/generic-edge/universal meta-model — hard reject for canonical kernel.

Physical selection requires a later separate user authorization and benchmark/design scope.

## Active workstreams

### Pre-Physical Repository & Architecture Coherence

- Status: **IN PROGRESS**
- Branch: `chore/pre-physical-coherence`
- Original workstream base: `main @ 148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`
- Handoff: [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md)
- Phase 0 + 1: **QA PASS**.
- Phase 2: **QA PASS** — current architecture/supersession cleanup completed with exact remote path QA and knowledge-coverage QA.
- Phase 2 content HEAD before closure markers: `dfc1f4e124f362d342c336485e166c8ac57afba4`.
- Phase 3: **QA PASS** — Backend Foundation handoff cleaned against closed Domain/Logical/current architecture.
- Phase 4: **QA PASS** — current Pre-Physical Architecture Baseline established and made mandatory downstream input without authorizing Physical/backend implementation.
- Phase 4 content HEAD before global closure markers: `d67cd83f462611b2cc6d341937432e705f7a8682`.
- Phase 5: **QA PASS** — four requirement packages plus index established; baseline/backend handoff/navigation propagated; lossless size/tool-limit split rule hardened.
- Phase 5 PRE-SCOPE: `e26f95af6d46292bf0f42aa43fa67b1f9f4fc05f`.
- Phase 5 content HEAD before global closure markers: `c29cfe4bde47d5df4f46507a5f1717acd1903112`.
- Phase 6: **QA PASS** — AI/context/runtime + Integration Hub boundary contracts established and propagated without provider/runtime/protocol selection.
- Phase 6 PRE-SCOPE: `40728080ae7a69703d40d14dd256a556516ccc58`.
- Phase 6 content HEAD before global closure markers: `67d6a0d63ecaf39379912606dcf5113550718594`.
- Next: **coordinated Phase 7–9 architecture tranche**, preserving internal dependency order `7 → 8 → 9`.
- Domain/Logical remain closed/unchanged.

### Phase 4 — Home / Today UX

- Status: **IN PROGRESS — separate product/design workstream**
- Branch: `prototype/phase-4-today-home`
- Handoff: [`workstreams/today-home.md`](workstreams/today-home.md)
- Does not override backend/domain/logical architecture.

## Deferred production/model workstreams

### Physical Model

- **NOT STARTED / NOT AUTHORIZED**.
- May start only after Pre-Physical Coherence closes and the user approves a separate branch/PRE-SCOPE/write gate/benchmark/validation boundary.

### Backend Foundation

- **NOT STARTED / DEFERRED**.
- Current future handoff: [`workstreams/backend-foundation.md`](workstreams/backend-foundation.md).
- The current handoff consumes the Pre-Physical Architecture Baseline, Phase 5 requirements and Phase 6 boundary contracts and remains intentionally non-executable.
- Backend Foundation may start only after Pre-Physical Coherence closes, a separate Physical Model is accepted, and applicable accepted Physical/runtime/security/integration/API prerequisites exist.
- Do not create `feature/backend-foundation`, SQL/schema/migrations, concrete API/backend/Auth/provider implementation or a persistence-specific bootstrap from this status.

## Current architecture documentation policy

Current specifications contain current truth only. ADRs preserve rationale + explicit supersession/qualification. Historical validation/checkpoint files preserve truthful chronology. Git preserves recoverable history.

Stale current docs are replaced/deleted only after knowledge coverage proves meaningful content is safely mapped.

Current architecture navigation starts at [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md), [`architecture/requirements/README.md`](architecture/requirements/README.md), [`architecture/ai-context-runtime-boundaries.md`](architecture/ai-context-runtime-boundaries.md), [`architecture/integration-hub-boundaries.md`](architecture/integration-hub-boundaries.md) and [`architecture/README.md`](architecture/README.md).

## Phase 2 verified result

Approved Phase 2 PRE-SCOPE:

`d9610a7da4fe8fc759e9809843d989f1befcda5c`

Verified content HEAD before closure markers:

`dfc1f4e124f362d342c336485e166c8ac57afba4`

Remote fallback QA result:

```text
linear content commits 17
added                  1
modified              15
deleted                 1
unexpected              0
main changed            0
```

The native GitHub compare endpoint returned `404` and was not counted as PASS. Equivalent scope was proven through remote refs, the bounded linear commit chain, per-commit single-path/status evidence and remote payload readback.

Knowledge coverage for the retired `architecture/personal-data-ai-integration.md` passed:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```

The retired file is absent from the active branch. Historical `domain-model-logical-readiness*` evidence was not modified.

## Phase 3 result

The Backend Foundation cleanup preserves useful future implementation requirements while removing or deferring stale assumptions.

Current future handoff establishes Domain + Logical as consumed closed authorities, Physical/runtime/API prerequisites as later gates, SQLAlchemy/Alembic as conditional implementation candidates, and no canonical first slice based on old product-label ontology.

Exact Phase 3 PRE-SCOPE and remote closure evidence are recorded in [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md).

## Phase 4 result

[`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md) is the current bridge source for:

- decided current direction versus implementation authorization;
- semantic non-collapse/prohibited shortcuts;
- `LR-01..LR-13` / discriminated-reference and state-layer boundaries;
- mandatory `WL-H01..WL-H12` downstream hardenings;
- runtime/product/technical concepts that are not Domain owners by default;
- AI/integration current boundaries;
- Physical and durable-workflow benchmark posture;
- Phase 5–12 ownership of still-open obligations;
- explicit non-authorization of Physical/schema/API/Auth/runtime/provider/backend implementation.

It coordinates current authority; it does not duplicate or reopen Domain/Logical semantics.

## Phase 5 result

Phase 5 converted already-supported Domain/Logical/product/security pressure into four current Pre-Physical requirement packages without selecting implementation mechanisms.

Remote content QA from Phase 5 PRE-SCOPE to content HEAD returned:

```text
ahead_by       10
behind_by       0
total_commits   10
added            5
modified         5
deleted          0
unexpected       0
```

The five created paths are the requirement index plus four packages. The five content-local updates are architecture navigation/baseline, Backend Foundation handoff and the two workflow documents that state explicitly:

```text
SIZE / TOOL-LIMIT SPLIT
= LOSSLESS PHYSICAL PARTITION
!= SUMMARY / CONDENSATION / HIDDEN CONTENT REWRITE
```

No Domain/Logical/ADR/Physical/backend implementation path was changed by the Phase 5 content package.

## Phase 6 result

Phase 6 creates two current boundary contracts:

- [`architecture/ai-context-runtime-boundaries.md`](architecture/ai-context-runtime-boundaries.md);
- [`architecture/integration-hub-boundaries.md`](architecture/integration-hub-boundaries.md).

The Phase 6 content package passed remote compare from PRE-SCOPE to content HEAD:

```text
ahead_by        8
behind_by       0
total_commits    8
added             2
modified          6
deleted           0
unexpected        0
```

The six content-local updates are architecture navigation/baseline/system/technical, ADR-005 and Backend Foundation. No Domain/Logical/Physical/backend implementation path was changed.

Phase 6 selects no AI provider/model, agent framework, workflow engine, MCP/A2A implementation or provider adapter.

## Immediate next work — coordinated Phase 7–9 tranche

Treat Phases 7, 8 and 9 as one coordinated Pre-Physical architecture tranche to reduce repeated global-document churn, while preserving three ordered internal checkpoints:

```text
Phase 7
Durable workflow / async benchmark
        ↓ accepted benchmark result / constraints
Phase 8
Governed API / command / effect contract
        ↓ accepted operation/effect surface
Phase 9
Search / observability / calendar / solver pressure
```

The tranche may share one outer read-only inventory and, after a separately approved exact gate, one bounded propagation scope. However:

- Phase 8 must consume Phase 7 results rather than assuming a workflow mechanism;
- Phase 9 must consume the accepted Phase 8 effect/disclosure boundary;
- each internal checkpoint gets its own QA/verdict before the next is treated as accepted;
- no failure in one checkpoint is hidden by the outer combined scope;
- no Physical technology is selected by the tranche.

Phase 7 begins read-only with the current requirements and Phase 6 contracts.

## Non-negotiable downstream obligations

`WL-H01..WL-H12`, all accepted Phase 5 requirements and both Phase 6 boundary contracts must survive later architecture/Physical/runtime work. Open parameters/decisions must be resolved at the appropriate later gate rather than silently defaulted.
