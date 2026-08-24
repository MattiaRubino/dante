> **CURRENT INTEGRATION RECONCILIATION — 2026-08-24**  
> Frontend materialization is **CLOSED / PASS / INTEGRATED into protected `main` via PR #28**. Any later statement in this preserved body that still calls it active is pre-merge status. Backend CP6 remains on `feature/logical-postgresql`, current with `main`, with CP6-03 ACTIVE, Checkpoint J / DB-U23 CLOSED, Parts 1–8 active, `DB-U08 / DB-U15 / DB-U21` OPEN, exact next block = **FINAL ACTUAL POSTGRESQL OBJECT INVENTORY**, Gate 03 not earned, CP6-04 not authorized. This banner supersedes only contradictory status/routing wording below.  

# DANTE Architecture Index

- Status: **CURRENT**

## 1. Architecture state

```text
Domain Model                  CLOSED
Logical Model                 CLOSED
Pre-Physical coherence        CLOSED
Physical target               CLOSED / ACCEPTED
Engineering Foundation v0     CLOSED / ACCEPTED
Frontend Foundation Passo 1   PASS
Frontend Foundation Passo 2   PASS
Frontend Foundation Passo 3   FINAL REVIEW PASS
Frontend Foundation           DESIGN/ARCHITECTURE CLOSED / ACCEPTED / INTEGRATED VIA PR #22
Frontend materialization      ACTIVE ON feature/frontend-materialization
Production backend scaffold   CLOSED / INTEGRATED IN PROTECTED main / DIRECT QA PASS
Backend CP6                   ACTIVE ON feature/logical-postgresql
Backend CP6-01                CLOSED / GATE 01 PASS
Backend CP6-02                CLOSED / GATE 02 PASS
Backend CP6-03                ACTIVE / CHECKPOINT J + DB-U23 CLOSED / FINAL ACTUAL POSTGRESQL OBJECT INVENTORY NEXT
Gate 03                       NOT YET EARNED
DB-U08 / DB-U15 / DB-U21      OPEN
PostgreSQL architecture       18 major family / sole canonical persistence + material-history authority
Physical exact patch          18.4 / HISTORICAL PHASE-TIME SELECTION
Current PostgreSQL patch      18.6 / DIRECT REMOTE FOUNDATION REGRESSION PASS
Current DANTE business DB     NOT YET MATERIALIZED
Direct business HG / PSV      ONLY AS EXACTLY EARNED
```

`main` is integrated authority for closed shared foundations. Current unmerged backend CP6 truth lives on `feature/logical-postgresql`; current frontend materialization truth lives on `feature/frontend-materialization`.

## 2. Current architecture entry points

- `system-overview.md` — current system/component/authority overview
- `technical-decisions.md` — current decision register
- `frontend-engineering-foundation.md` — frontend technology specification
- `frontend-engineering-foundation-part-2.md` — frontend application/package/dependency/data-authority specification
- `frontend-engineering-foundation-final-review.md` — final review/closure evidence
- `frontend-engineering-foundation-post-closure-qa.md` — post-closure knowledge/evidence QA
- `../decisions/ADR-003-primary-database.md` — historical PostgreSQL-primary rationale with current replacement authority identified
- `../decisions/ADR-007-domain-model-informed-persistence-boundaries.md` — active semantic persistence guardrail with historical Physical posture qualified
- `../decisions/ADR-008-frontend-engineering-stack.md` — frontend technology ADR
- `../decisions/ADR-009-frontend-architecture-boundaries.md` — frontend architecture ADR
- `../decisions/ADR-010-postgresql-persistence-constitution.md` — accepted reusable PostgreSQL persistence doctrine ADR
- `../workstreams/logical-postgresql.md` — active CP6 database blueprint/materialization handoff and durable exact resume point
- `../database/README.md` — database System-of-Record/documentation contract
- `../database/dante-postgresql-database.md` + Parts 2–8 — one canonical multi-part Database Architecture & Reference
- `../workstreams/frontend-foundation.md` — frontend closure/integration handoff
- `../workstreams/engineering-foundation.md` — closed Engineering Foundation handoff
- `../development/engineering-foundation-v0.md` — backend engineering contract
- `../development/repository-layout-v0.md` — accepted root topology/path ownership

## 3. Current system direction

One DANTE product monorepo with `apps/backend`, `apps/web`, `apps/mobile` and accepted root ownership for `packages/`, `infra/`, `tooling/`, `tests/system/`, `docs/`, `prototypes/`, `.github/`. Paths are materialized only when real content exists.

Backend is a capability-first modular monolith. PostgreSQL **18 major family** is the sole canonical persistence/material-history authority. PostgreSQL **18.4** remains exact historical Physical/CP2/CP3 evidence; PostgreSQL **18.6** is the current repository-controlled maintenance patch and has a direct remote technical-foundation regression PASS.

CP6 now converts the closed Domain + Logical + Physical model into the concrete DANTE PostgreSQL database: CP6-03 blueprint, CP6-04 materialization, CP6-05 direct database QA/closure. CP6-03 has completed Checkpoint J / `DB-U23`; the next design block is the **Final Actual PostgreSQL Object Inventory**, while `DB-U08`, `DB-U15` and `DB-U21` remain open. Gate 03 is not yet earned. The first product vertical is post-CP6.

Frontend is platform-specific at renderer/UI/platform-adapter level with selective semantic sharing. Data paths preserve backend canonical authority and operation-specific offline governance. Frontend materialization is already active on its dedicated bounded branch.

## 4. Frontend Foundation accepted design

Passo 1 fixes the TypeScript/React/Vite/Expo/pnpm/Turbo/PowerSync/Query/Form/Zod/Orval/UI/test/release baseline.

Passo 2 fixes:

- inherited repository root ownership;
- feature-first Web/Mobile architecture;
- public-API-only and acyclic dependency direction;
- real-consumer shared-package policy;
- framework-free shared cores by default;
- Data Authority Matrix;
- feature data firewall;
- mobile local/offline capability with backend-governed canonical effects;
- Web online-first with PowerSync Web + browser PWA/SW dormant;
- identity-scoped local data;
- session adapters without invented backend protocol;
- design-token/UI/i18n/time/config boundaries;
- LOCAL/DEV/UAT/PROD vocabulary;
- versioned Web runtime public config;
- GitHub Actions CI/CD authority;
- WSL-backed single-checkout developer posture with native bridge direct validation.

Passo 3 clean review found and repaired root-topology inheritance, feature-cycle enforcement and stale CURRENT documentation/governance. Blocking defects after repair: **0**.

## 5. Remaining bounded deferrals

- exact backend AuthN/AuthZ application protocol where not already fixed by security/persistence authority;
- concrete product API routes/versioning;
- concrete product feature inventory/folder contents beyond materialized workstreams;
- PowerSync Web activation;
- browser PWA/service-worker activation;
- backend cloud compute/IaC;
- remote infrastructure materialization timing;
- platform release activation schedule;
- dormant specialist activation based on real need.

These deferrals do not authorize CP6 to omit database structures already determinable from closed Domain/Logical/Physical/CP6 authority.

## 6. Architecture reopen discipline

Closed Domain/Logical/Physical/Engineering/Frontend Foundation and CP6-02 PostgreSQL-doctrine decisions are not casually reselected.

Implementation evidence first reopens the affected technology/adapter/boundary rather than the entire architecture unless a wider contradiction is proven.

## 7. Next architecture work

```text
BACKEND
CP6-03 ACTIVE / WHOLE DANTE DATABASE BLUEPRINT
→ Checkpoint J / DB-U23 CLOSED
→ consume Database Reference Parts 1–8 together
→ FINAL ACTUAL POSTGRESQL OBJECT INVENTORY NEXT
→ keep DB-U08 / DB-U15 / DB-U21 open until inventory freeze
→ close naming/index/ACL + DAG/mapping/Dictionary/direct-proof plan
→ mandatory SECOND FULL TOMBSTONE AUDIT FROM ZERO
→ Gate 03 only after clean audit
→ CP6-04 real database materialization only after separate explicit authorization
→ CP6-05 direct database QA / CP6 closure

FRONTEND
continue feature/frontend-materialization independently under its own workstream
```

Direct implementation evidence is claimed only after the relevant real artifact/scenario executes.