# ADR-008: Frontend Engineering Stack

- Status: **ACCEPTED / INTEGRATED VIA PR #22**
- Date: 2026-08-20
- Supersedes: [`ADR-001-client-platforms.md`](ADR-001-client-platforms.md)
- Current specification: [`../architecture/frontend-engineering-foundation.md`](../architecture/frontend-engineering-foundation.md)

## Context

ADR-001 selected Next.js + React for Web and Expo + React Native for Mobile before the dedicated frontend-engineering workstream had evaluated the complete DANTE stack against the closed Physical Model, local/offline semantics, backend boundary, monorepo governance and current 2026 ecosystem.

The dedicated workstream established enough evidence to replace that provisional Web framework choice and to fix the broader frontend engineering baseline. The accepted decision was integrated into protected `main` through PR #22.

DANTE already has durable constraints that the frontend must consume:

- one product monorepo with `apps/backend`, `apps/web`, `apps/mobile`;
- FastAPI/application services as backend boundary;
- PostgreSQL as sole canonical state/material-history authority;
- PowerSync + encrypted SQLite as bounded local/sync capability;
- operation-specific offline eligibility and backend governance for consequential effects;
- GitHub Actions as repository CI/CD authority;
- Web and Mobile may share semantics/contracts without requiring one universal renderer.

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
synced local projection  PowerSync + encrypted SQLite
remote request state     TanStack Query
form state               TanStack Form
runtime validation       Zod 4
transient local UI       React
cross-tree transient UI  Zustand only when justified
```

Use FastAPI OpenAPI → Orval 8 for typed frontend transport generation.

Use platform-appropriate UI foundations rather than a universal renderer:

```text
Web     Radix Primitives + Tailwind CSS + CSS variables
Mobile  React Native StyleSheet + typed DANTE tokens
Shared  DTCG-compatible semantic token source compiled through Terrazzo
```

Use GitHub Actions as the primary orchestrator. EAS Build/Submit/Update are selected mobile services; EAS Workflows is optional/dormant.

The complete selected/specialist/deferred technology matrix is authoritative in `docs/architecture/frontend-engineering-foundation.md`.

## PowerSync write-path qualification

A synchronized table/entity does **not** imply that every mutation is safe to perform as an offline local write.

Two governed write classes are required:

1. **online governed command** — UI → FastAPI → AuthZ/governance/expected-state → canonical commit → downstream sync;
2. **offline-eligible operation** — local pending mutation → PowerSync upload → backend governance/conflict validation → canonical commit or reject/conflict → reconciliation.

Offline eligibility is operation-specific. Local arrival order is not semantic truth and universal consequential LWW remains forbidden.

## Rationale

### React DOM + Vite over Next.js for the application Web client

DANTE already has a dedicated backend/application boundary and is a client-heavy browser application. React DOM preserves first-class browser/DOM capabilities without introducing a second application-server model that DANTE does not require.

### Expo/React Native for Mobile

It preserves a common TypeScript/React engineering ecosystem while keeping Mobile native and allowing native modules/Kotlin/Swift where measured need exists.

### Turborepo over Nx

Turbo remains a thin task orchestrator over pnpm/Vite/Expo rather than becoming another framework layer coupled to the release cadence of each application framework.

### Explicit state ownership

PowerSync, TanStack Query and Zustand solve different state classes. Keeping those authorities separate prevents multiple competing copies of DANTE reality inside the frontend.

### Platform-specific UI, shared semantics

DANTE optimizes sharing of contracts, validation, tokens, i18n, time semantics and pure logic rather than forcing identical Web/Mobile rendering.

## Consequences

- ADR-001 is superseded; Next.js is no longer the selected `apps/web` application framework.
- `apps/web` and `apps/mobile` remain separate first-class clients.
- the frontend does not become a second canonical state authority;
- PowerSync write behavior must follow operation-specific backend governance;
- Web baseline is online-first; PowerSync Web/PWA activation remains dormant unless explicitly required;
- exact shared package boundaries are governed by ADR-009 / the Part-2 specification;
- selected technologies are not claimed as installed/configured/directly validated yet;
- high-coupling integrations carry explicit materialization validation obligations.

## Validation status

```text
TECHNOLOGY SELECTION
DESIGN COMPLETE / INTEGRATED VIA PR #22

INSTALLATION
NOT STARTED

CONFIGURATION
NOT STARTED

DIRECT FRONTEND VALIDATION
NOT STARTED
```

A failed material validation may reopen the affected technology decision without automatically reopening the complete frontend stack.
