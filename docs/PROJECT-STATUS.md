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
Phase 2 architecture supersession/current-truth cleanup — CONTENT WRITTEN / FINAL QA PENDING

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
- Phase 2: architecture current-truth/supersession cleanup content written; final remote scope/coverage QA pending.
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
- Existing handoff still requires its separately gated Phase 3 cleanup before execution.
- Backend Foundation must eventually consume closed Domain + Logical, accepted Physical Model and current runtime/security/integration contracts.

## Current architecture documentation policy

Current specifications contain current truth only. ADRs preserve rationale + explicit supersession/qualification. Historical validation/checkpoint files preserve truthful chronology. Git preserves recoverable history.

Stale current docs are replaced/deleted only after knowledge coverage proves meaningful content is safely mapped.

Current architecture navigation: [`architecture/README.md`](architecture/README.md).

## Immediate next work

1. Complete Phase 2 final remote physical-path + knowledge-coverage QA.
2. Only after Phase 2 QA PASS, move to **Phase 3 — Backend Foundation handoff cleanup**, beginning with read-only review and a separate exact write gate.
3. Do not start Physical Model, SQL/schema/migrations/API/backend/Auth/provider implementation implicitly.
4. Continue Phase 4 UX independently.

## Non-negotiable downstream Logical obligations

`WL-H01..WL-H12` must survive later architecture/Physical/runtime work: governed effects, disclosure surfaces, unknown/absence semantics, expected-state mutation, idempotency separation, truthful multi-owner consistency, provider/canonical separation, derived-state freshness, retention/tombstone integrity, AuthZ provenance and inference-leakage protection.
