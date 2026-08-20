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
Production implementation     NOT STARTED
Direct PSV                    NOT RUN
```

`main` remains the integrated authority. Frontend Foundation documents on `feature/frontend-foundation` are newer unmerged workstream truth until protected-main integration.

## 2. Current architecture entry points

- `system-overview.md` — current system/component/authority overview
- `technical-decisions.md` — current accepted technical decision register
- `frontend-engineering-foundation.md` — Frontend Foundation Passo-1 technology/current-stack specification on the active branch
- `frontend-engineering-foundation-part-2.md` — Frontend Foundation Passo-2 application/package/dependency/data-authority specification on the active branch
- `../decisions/ADR-008-frontend-engineering-stack.md` — frontend technology ADR
- `../decisions/ADR-009-frontend-architecture-boundaries.md` — frontend application/dependency/data-authority ADR
- `../workstreams/frontend-foundation.md` — active frontend workstream handoff
- `../workstreams/engineering-foundation.md` — closed Engineering Foundation handoff
- `../development/engineering-foundation-v0.md` — complete backend engineering contract

For implementation, also consume the Domain/Logical/Physical indexes and accepted detailed sources.

## 3. Current system direction

DANTE is one product monorepo with three top-level application boundaries:

```text
apps/backend
apps/web
apps/mobile
```

Backend begins as a capability-first modular monolith.

Frontend is platform-specific at the renderer/UI/platform-adapter level while sharing only real cross-platform semantics/contracts.

PostgreSQL 18.4 is the sole canonical persistence authority. PowerSync/SQLite is bounded noncanonical local/sync state; frontend data paths preserve operation-specific governance and the Data Authority Matrix.

Selected specialist components remain bounded and activate only at their real implementation/release triggers.

## 4. Engineering Foundation decisions

Backend baseline includes:

- Python 3.14.x / initial 3.14.7;
- uv;
- WSL2/Linux canonical backend workflow on Windows;
- PyCharm WSL interpreter supported, repository IDE-neutral;
- Docker Compose for LOCAL stateful dependencies;
- real PostgreSQL 18.4 with full selected extension envelope enabled from first LOCAL DB;
- SQLAlchemy 2.0 stable line + psycopg 3 + Alembic;
- capability-specific persistence/application boundaries;
- migration risk governance and logical-copy/recovery separation;
- pydantic-settings typed configuration;
- workload identity/secret manager/OIDC target;
- real-PostgreSQL risk-layered testing;
- GitHub Actions + protected-main/supply-chain baseline;
- LOCAL/DEV/UAT/PROD environment model with provider deferred.

## 5. Frontend Foundation decisions — branch local pending integration

Passo 1 selects the TypeScript/React/Vite/Expo/pnpm/Turbo/PowerSync/Query/Form/Zod/Orval/UI/test/release baseline.

Passo 2 fixes:

- feature-first Web/Mobile application architecture;
- public-API-only dependency direction;
- small real-consumer shared-package policy;
- framework-free shared cores by default;
- formal Data Authority Matrix;
- feature data firewall;
- mobile local-first/offline capability with backend-governed canonical effects;
- Web online-first with PowerSync Web and browser PWA/service worker dormant;
- identity-scoped local-data lifecycle;
- auth/session adapter boundaries without invented backend contracts;
- design-token/UI/i18n/time/config boundaries;
- DANTE LOCAL/DEV/UAT/PROD vocabulary;
- versioned Web runtime public config;
- GitHub Actions primary CI/CD and app-specific test/release responsibilities;
- one authoritative WSL-backed developer checkout posture, with native bridging directly validated later.

## 6. Remaining explicit deferrals

Still not fixed by frontend architecture because real implementation facts are required:

- exact backend AuthN/AuthZ protocol;
- concrete API route/version surface;
- concrete product feature inventory/folder contents;
- activation date for PowerSync Web;
- activation of browser PWA/service worker;
- cloud/backend compute provider and IaC;
- future root infrastructure topology;
- platform release activation schedule;
- measured need for dormant specialist libraries/services.

These are bounded deferrals, not permission for silent improvisation.

## 7. Repository identity

Continue in the existing repository. Do not create a new implementation repo.

## 8. Architecture reopen discipline

Closed Domain/Logical/Physical/Engineering decisions are not casually reselected during implementation.

Frontend technology/architecture design choices can be reopened only by concrete contradictory evidence or a material new requirement. Native/tooling validation failure should first reopen the affected adapter/tooling choice, not the entire architecture.

## 9. Next architecture work

```text
Frontend Foundation Passo 3
whole-design clean review
        ↓
closure decision / PR preparation
        ↓
protected-main integration
        ↓
new bounded materialization/scaffold scope
        ↓
direct validation obligations executed progressively
```

Direct implementation evidence remains NOT RUN until real scaffold/artifacts execute the required scenarios.
