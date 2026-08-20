# DANTE Architecture Index

- Status: **CURRENT**

## 1. Architecture state

```text
Domain Model                  CLOSED
Logical Model                 CLOSED
Pre-Physical coherence        CLOSED
Physical target               CLOSED / ACCEPTED
Engineering Foundation v0     CLOSED / ACCEPTED
Frontend Foundation Passo 1   DESIGN COMPLETE / branch-local
Frontend Foundation Passo 2   DESIGN COMPLETE / branch-local
Frontend Foundation Passo 3   CLEAN REVIEW IN PROGRESS
Production implementation     NOT STARTED
Direct PSV                    NOT RUN
```

`main` remains integrated authority. Frontend Foundation documents on `feature/frontend-foundation` are newer unmerged workstream truth until protected-main integration.

## 2. Current architecture entry points

- `system-overview.md` — system/component/authority overview
- `technical-decisions.md` — accepted technical decision register
- `frontend-engineering-foundation.md` — frontend technology specification
- `frontend-engineering-foundation-part-2.md` — frontend application/package/dependency/data-authority specification
- `../decisions/ADR-008-frontend-engineering-stack.md` — frontend technology ADR
- `../decisions/ADR-009-frontend-architecture-boundaries.md` — frontend architecture ADR
- `../workstreams/frontend-foundation.md` — active frontend handoff
- `../workstreams/engineering-foundation.md` — closed Engineering Foundation handoff
- `../development/engineering-foundation-v0.md` — backend engineering contract
- `../development/repository-layout-v0.md` — accepted root topology/path ownership inherited by frontend

## 3. Current system direction

One DANTE product monorepo:

```text
apps/backend
apps/web
apps/mobile
```

Accepted root ownership also reserves `packages/`, `infra/`, `tooling/`, `tests/system/`, `docs/`, `prototypes/` and `.github/`; paths are materialized only when real content exists.

Backend starts as a capability-first modular monolith. PostgreSQL 18.4 remains sole canonical persistence authority.

Frontend is platform-specific at renderer/UI/platform-adapter level with selective semantic sharing. Data paths preserve backend canonical authority and operation-specific offline governance.

## 4. Frontend Foundation branch-local decisions

Passo 1 selects the TypeScript/React/Vite/Expo/pnpm/Turbo/PowerSync/Query/Form/Zod/Orval/UI/test/release baseline.

Passo 2 fixes:

- inherited repository root ownership;
- feature-first Web/Mobile architecture;
- public-API-only and acyclic dependency direction;
- small real-consumer shared packages;
- framework-free shared cores by default;
- Data Authority Matrix;
- feature data firewall;
- mobile local-first/offline capability with backend-governed effects;
- Web online-first with PowerSync Web + browser PWA/service worker dormant;
- identity-scoped local data;
- session adapters without invented backend protocol;
- design-token/UI/i18n/time/config boundaries;
- LOCAL/DEV/UAT/PROD vocabulary;
- versioned Web runtime public config;
- GitHub Actions CI/CD authority;
- WSL-backed single-checkout developer posture with native bridge direct-validation obligation.

## 5. Remaining bounded deferrals

- exact backend AuthN/AuthZ protocol;
- concrete API routes/versioning;
- concrete product feature inventory/folder contents;
- PowerSync Web activation;
- browser PWA/service-worker activation;
- cloud/backend compute provider and IaC engine;
- infrastructure materialization timing;
- platform release activation schedule;
- dormant specialist activation based on measured need.

## 6. Architecture reopen discipline

Closed Domain/Logical/Physical/Engineering decisions are not casually reselected.

Frontend design reopens only with concrete contradictory evidence/material requirements. Native/tooling validation failure first reopens its affected adapter/tooling choice.

## 7. Next architecture work

```text
finish Frontend Foundation Passo 3
↓
closure decision / PR preparation
↓
protected-main integration after authorization
↓
new bounded materialization scope
↓
direct validation progressively
```

Direct implementation evidence remains NOT RUN until real artifacts execute the required scenarios.
