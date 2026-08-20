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
Production implementation     NOT STARTED
Direct PSV                    NOT RUN
```

`main` is integrated authority. Frontend Foundation design/architecture is now integrated through PR #22.

## 2. Current architecture entry points

- `system-overview.md` — current system/component/authority overview
- `technical-decisions.md` — current decision register
- `frontend-engineering-foundation.md` — frontend technology specification
- `frontend-engineering-foundation-part-2.md` — frontend application/package/dependency/data-authority specification
- `frontend-engineering-foundation-final-review.md` — final review/closure evidence
- `frontend-engineering-foundation-post-closure-qa.md` — post-closure knowledge/evidence QA
- `../decisions/ADR-008-frontend-engineering-stack.md` — frontend technology ADR
- `../decisions/ADR-009-frontend-architecture-boundaries.md` — frontend architecture ADR
- `../workstreams/frontend-foundation.md` — frontend closure/integration handoff
- `../workstreams/engineering-foundation.md` — closed Engineering Foundation handoff
- `../development/engineering-foundation-v0.md` — backend engineering contract
- `../development/repository-layout-v0.md` — accepted root topology/path ownership

## 3. Current system direction

One DANTE product monorepo with `apps/backend`, `apps/web`, `apps/mobile` and accepted root ownership for `packages/`, `infra/`, `tooling/`, `tests/system/`, `docs/`, `prototypes/`, `.github/`. Paths are materialized only when real content exists.

Backend is a capability-first modular monolith. PostgreSQL 18.4 remains sole canonical persistence/material-history authority.

Frontend is platform-specific at renderer/UI/platform-adapter level with selective semantic sharing. Data paths preserve backend canonical authority and operation-specific offline governance.

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

- exact backend AuthN/AuthZ protocol;
- concrete API routes/versioning;
- concrete product feature inventory/folder contents;
- PowerSync Web activation;
- browser PWA/service-worker activation;
- backend cloud compute/IaC;
- infrastructure materialization timing;
- platform release activation schedule;
- dormant specialist activation based on measured need.

## 6. Architecture reopen discipline

Closed Domain/Logical/Physical/Engineering/Frontend Foundation decisions are not casually reselected.

Frontend implementation evidence first reopens the affected technology/adapter/boundary rather than the entire architecture unless a wider contradiction is proven.

## 7. Next architecture work

```text
open fresh bounded frontend materialization/direct-validation workstream
↓
materialize accepted workspace/app/package boundaries
↓
execute carried direct validations progressively
```

Direct implementation evidence remains NOT RUN until real artifacts execute the required scenarios.
