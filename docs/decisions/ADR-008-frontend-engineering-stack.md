# ADR-008: Frontend Engineering Stack

- Status: **ACCEPTED / INTEGRATED VIA PR #22 / MATERIALIZED AT FM-00..FM-07 STATED SCOPES**
- Date: 2026-08-20
- Materialization qualification: 2026-08-23
- Supersedes: [`ADR-001-client-platforms.md`](ADR-001-client-platforms.md)
- Design-time specification: [`../architecture/frontend-engineering-foundation.md`](../architecture/frontend-engineering-foundation.md)
- Direct implementation evidence: [`../workstreams/frontend-materialization.md`](../workstreams/frontend-materialization.md)

## Context

ADR-001 selected Next.js + React for Web and Expo + React Native for Mobile before the dedicated frontend-engineering workstream evaluated the complete DANTE stack against the closed Physical Model, local/offline semantics, backend boundary, monorepo governance and current ecosystem.

The Frontend Foundation replaced that provisional Web choice and fixed the broader frontend engineering baseline. PR #22 integrated the architecture/design decision. The subsequent `feature/frontend-materialization` workstream then installed, configured and directly validated the real baseline through FM-00..FM-07.

DANTE constraints that remain unchanged:

- one product monorepo with sibling `apps/backend`, `apps/web`, `apps/mobile`;
- FastAPI/application services as backend authority;
- PostgreSQL as sole canonical state/material-history authority;
- PowerSync + encrypted SQLite as bounded noncanonical local/sync capability when activated;
- operation-specific offline eligibility and backend governance for consequential effects;
- GitHub Actions as repository CI/CD authority;
- shared semantics do not require one universal Web/Mobile renderer.

## Decision

Use a TypeScript/React family with platform-specific renderers:

```text
TOOLING
Node.js 24 LTS
TypeScript 6.0.x strict
pnpm 11
Turborepo 2.x
GitHub Actions primary CI/CD

WEB
React 19.2 + React DOM
Vite 8
TanStack Router

MOBILE
React Native 0.86
Expo SDK 57
Expo Router
```

Use explicit state/data ownership:

```text
canonical state          backend + PostgreSQL
synced local projection  PowerSync + encrypted SQLite when activated
remote request state     TanStack Query when activated
form state               TanStack Form when activated
runtime validation       Zod
transient local UI       React
cross-tree transient UI  Zustand only when justified
```

Use FastAPI OpenAPI -> Orval for typed frontend transport generation only when a real product API contract exists.

Use platform-appropriate UI implementations over shared semantics/tokens rather than a universal renderer.

GitHub Actions remains primary repository orchestration. EAS Build/Submit/Update remain selected Mobile release services but are not activated merely by this ADR.

## PowerSync write-path qualification

A synchronized table/entity does not imply every mutation is safe as an offline local write.

Two governed write classes remain required:

1. **online governed command** — UI -> FastAPI -> governance/expected-state -> canonical commit -> downstream sync;
2. **offline-eligible operation** — local pending mutation -> upload -> backend governance/conflict validation -> canonical commit or reject/conflict -> reconciliation.

Local arrival order is not semantic truth and universal consequential LWW remains forbidden.

## Rationale

### React DOM + Vite over Next.js

DANTE already has a dedicated backend/application boundary and a client-heavy browser application. Vite/React DOM avoids introducing an unnecessary second application-server model.

### Expo/React Native for Mobile

It preserves a common TypeScript/React ecosystem while keeping Mobile native and allowing native modules/platform code where measured need exists.

### Turborepo over Nx

Turbo remains a thin task orchestrator over pnpm/Vite/Expo rather than becoming another broad framework layer.

### Explicit state ownership

PowerSync, TanStack Query, forms and UI state solve different state classes. Keeping them separate prevents competing copies of DANTE reality.

### Platform-specific UI, shared semantics

DANTE shares contracts, validation, tokens, i18n, time semantics and pure logic where valuable without forcing identical Web/Mobile rendering.

## Consequences

- ADR-001 remains superseded; Next.js is not the selected authenticated-app Web framework;
- Web and Mobile remain separate first-class clients;
- frontend never becomes canonical DANTE state authority;
- PowerSync writes remain operation-specific/backend-governed;
- Web starts online-first;
- shared package boundaries remain governed by ADR-009;
- capabilities not consumed by a real feature remain dormant rather than placeholder-installed.

## Materialization qualification

The Foundation used selection-time version wording. Later direct materialization establishes the implementation authority at the tested scopes:

```text
Node                         24.19.0
pnpm                         11.22.0
TypeScript                   6.0.3 strict
Turborepo                    2.10.11

Web React / React DOM        19.2.8 / 19.2.8
Vite                         8.2.1
TanStack Router              1.170.31

Expo SDK                     57.x / clean resolve 57.0.15
React Native                 0.86.2
Mobile React                 19.2.3
Expo Router                  57.x / clean resolve 57.0.15
Gesture Handler              2.32.0
Reanimated                   4.5.1

Temporal implementation      temporal-polyfill 1.0.4
Web E2E                      apps/web/e2e/
```

This directly qualifies two design-time details that must not be read as current implementation requirements:

```text
Foundation text: @js-temporal/polyfill
Qualified implementation: temporal-polyfill 1.0.4

Foundation text: Gesture Handler 3 line
Expo-qualified implementation: Gesture Handler 2.32.0
```

These are bounded implementation qualifications, not a reopening of the architecture decision.

## Direct validation status

Closed materialization evidence includes:

```text
fresh frozen workspace install                  PASS
strict TypeScript                               PASS
Web production build                            PASS
Web Chromium production-preview E2E             PASS
Android Expo/Metro/Hermes emulator runtime      PASS
Android Hermes production bundle smoke          PASS
Expo dependency compatibility                   PASS
architecture graph                              36 modules / 45 deps / 0 violations
generated-source drift                          PASS
unit tests                                      10 PASS
GitHub-hosted Frontend CI                       PASS
fresh-clone/store/browser materialization       PASS
tracked + untracked repository residue          0
```

The known workspace peer diagnostic (`react-dom@19.2.8` versus the workspace Mobile React `19.2.3`) is reproducible but non-blocking because Expo `install --check` directly passes for the Mobile baseline. It does not authorize React version forcing, peer suppression, packageExtensions, hoisting or nodeLinker changes.

## Current integration state

The closed materialization is being integrated through draft PR #28 on `chore/frontend-materialization-integration`. `Frontend CI Gate` has emitted and passed but is not a required `main` check until deliberate-red/recovery-green calibration and a separate ruleset decision.

A failed future material validation reopens the affected technology decision first; the complete frontend stack reopens only if evidence proves a wider contradiction.