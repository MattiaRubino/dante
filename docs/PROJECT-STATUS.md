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
Phase 3 Backend Foundation handoff cleanup — READ-ONLY AUDIT NEXT

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND FOUNDATION / PRODUCTION IMPLEMENTATION
NOT STARTED
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
9. [`architecture/README.md`](architecture/README.md) and linked current architecture/model sources
10. relevant ADR/evidence/methodology
11. relevant implementation/tests

Conversation history is secondary to repository truth.

## Accepted/current foundations

- [`product/product-identity-and-north-star.md`](product/product-identity-and-north-star.md) — current product identity/North Star.
- Core Domain Model / Domain Atlas — **CLOSED**.
- Logical Model — **CLOSED**, with `WL-H01..WL-H12` active downstream constraints.
- Web direction — Next.js + React + TypeScript.
- Mobile direction — Expo + React Native + TypeScript.
- Backend direction — Python + FastAPI + Pydantic; modular monolith.
- SQLAlchemy/Alembic — conditional candidates depending on accepted Physical persistence.
- AI — replaceable/provider-neutral gateway + bounded Context Builder + governed proposals/effects.
- Integration/provider state remains distinct from canonical LifeOS state.
- DEV/UAT/PROD are deployment environments, not permanent Git branches.
- Repository visibility: **public**.

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
- Existing handoff: [`workstreams/backend-foundation.md`](workstreams/backend-foundation.md).
- Phase 3 will first audit that handoff read-only, then propose a separate exact write gate.
- Backend Foundation must eventually consume closed Domain + Logical, accepted Physical Model and current runtime/security/integration contracts.

## Current architecture documentation policy

Current specifications contain current truth only. ADRs preserve rationale + explicit supersession/qualification. Historical validation/checkpoint files preserve truthful chronology. Git preserves recoverable history.

Stale current docs are replaced/deleted only after knowledge coverage proves meaningful content is safely mapped.

Current architecture navigation: [`architecture/README.md`](architecture/README.md).

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

## Immediate next work

1. **Phase 3 — read-only Backend Foundation handoff audit.**
2. Compare `docs/workstreams/backend-foundation.md` against current Domain + Logical + architecture truth.
3. Classify every stale/current requirement before proposing changes.
4. Then present a **separate exact Phase 3 write gate**.
5. Do not start Phase 3 writes from the consumed Phase 2 gate.
6. Do not start Physical Model, SQL/schema/migrations/API/backend/Auth/provider implementation implicitly.
7. Continue Phase 4 UX independently.

## Non-negotiable downstream Logical obligations

`WL-H01..WL-H12` must survive later architecture/Physical/runtime work: governed effects, disclosure surfaces, unknown/absence semantics, expected-state mutation, idempotency separation, truthful multi-owner consistency, provider/canonical separation, derived-state freshness, retention/tombstone integrity, AuthZ provenance and inference-leakage protection.
