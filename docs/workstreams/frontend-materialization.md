# Workstream — Frontend Materialization

- Status: **ACTIVE — FM-00 WORKSTATION PREFLIGHT NOT RUN**
- Branch: `feature/frontend-materialization`
- Opening base: `ff46eb16b971b1fde96eef9047b09faa02e1a5db`
- Frontend Engineering Foundation: **CLOSED / ACCEPTED / FINAL REVIEW PASS / integrated via PR #22**
- Production frontend scaffold: **NOT STARTED**
- Dependencies installed/configured: **NO**
- Direct frontend validation: **NOT RUN**
- Product-surface implementation: **NOT AUTHORIZED BY THIS CHECKPOINT**

## 1. Purpose

Materialize the accepted DANTE Frontend Engineering Foundation into a real, reproducible production workspace and directly validate the selected Web/Mobile/tooling boundaries before product feature implementation depends on them.

This workstream consumes rather than redesigns:

- `../architecture/frontend-engineering-foundation.md`;
- `../architecture/frontend-engineering-foundation-part-2.md`;
- `../architecture/frontend-engineering-foundation-final-review.md`;
- `../architecture/frontend-engineering-foundation-post-closure-qa.md`;
- `../decisions/ADR-008-frontend-engineering-stack.md`;
- `../decisions/ADR-009-frontend-architecture-boundaries.md`;
- closed Engineering Foundation/repository-layout authorities;
- accepted Physical target and applicable validation obligations.

## 2. Evidence discipline

Materialization uses the repository truth model:

```text
selected != installed
installed != configured
configured != directly validated
direct scenario PASS != whole-frontend PASS
```

No component receives a direct `PASS` merely because a package was added or a command returned successfully once.

Version-sensitive dependencies must be reverified against current primary documentation immediately before installation. The accepted major/line remains the design baseline; exact patches are fixed during materialization after compatibility verification.

## 3. Developer topology to materialize

Primary local posture:

```text
WINDOWS 11
├── JetBrains / PyCharm UI
├── browser
├── Android Studio / Android emulator
└── Docker Desktop

WSL2 / Linux
├── authoritative DANTE Git checkout
├── Git
├── Node / pnpm / Turbo
├── Vite
├── Metro / Expo CLI
├── Python / uv / backend tooling when applicable
└── Docker CLI

Docker LOCAL
└── stateful/local infrastructure only when real consumers exist
```

Normal frontend development processes are not containerized merely for appearance.

```text
Vite dev server     WSL process
Metro / Expo CLI    WSL process
Web browser         Windows
Android emulator    Windows
PostgreSQL          Docker when backend LOCAL infra is materialized
PowerSync service   Docker only when its real LOCAL integration scope activates
```

Hard invariant:

```text
ONE authoritative checkout
NO divergent Windows + WSL source trees
NO cross-OS shared node_modules tree
```

Detailed developer/onboarding authority: `../development/frontend-local-development.md`.

## 4. Materialization phases

### FM-00 — workstation preflight

Goal: establish actual machine state before installation.

Read-only evidence includes:

- WSL distro/kernel/version;
- repository physical path and branch/HEAD;
- Git;
- existing Node/npm/pnpm/Corepack state;
- Docker CLI / Compose reachability;
- Windows WSL/Docker/Android tooling where required.

No installation or repository manifest is authorized until the preflight result is reviewed.

Gate result statuses:

```text
FM-00 NOT RUN
FM-00 PASS
FM-00 PASS WITH REPAIR REQUIRED
FM-00 BLOCKED
```

### FM-01 — runtime and package-manager baseline

Materialize machine-level frontend runtime tooling in WSL only after FM-00.

Design baseline:

```text
Node       24 LTS
pnpm       11
```

Exact supported patch/version-manager mechanism is verified before installation.

Requirements:

- Node resolves from Linux/WSL, not a Windows executable leaked into PATH;
- pnpm resolves from the governed WSL toolchain;
- no project library is installed globally;
- repository declares Node/pnpm expectations;
- version verification commands are recorded.

### FM-02 — root JavaScript workspace

Materialize only real root artifacts required by the accepted Foundation, expected to include as applicable:

```text
package.json
pnpm-workspace.yaml
pnpm-lock.yaml
turbo.json
tsconfig.base.json
eslint.config.mjs
prettier.config.mjs
Node version authority
```

Requirements:

- private monorepo/workspace;
- one shared lockfile;
- `workspace:*` for internal packages;
- frozen-lockfile CI posture when CI activates;
- dependency lifecycle/build scripts explicitly governed;
- strict TypeScript baseline;
- repository scripts are predictable and documented.

No empty app/package directories are created only to match a diagram.

### FM-03 — minimal Web application

Materialize `apps/web` with only the accepted baseline required to prove the platform:

```text
React / React DOM
Vite
TypeScript
TanStack Router
```

Before product UI:

- development server starts from the WSL checkout;
- Windows browser can reach the app;
- production build succeeds;
- typecheck succeeds;
- lint succeeds;
- routing baseline works;
- architecture/import rules can be enforced.

The initial screen is diagnostic/scaffold content only, not Access/Home production implementation.

### FM-04 — minimal Mobile application

Materialize `apps/mobile` with the exact Expo SDK 57-compatible dependency graph resolved at that time.

Before product UI:

- Expo/Metro starts from WSL;
- typecheck/lint/bundle baseline passes;
- Expo diagnostics pass at the supported level;
- Windows Android emulator/device can consume the WSL-hosted development runtime;
- the WSL↔Windows Metro/ADB bridge is directly proven rather than assumed.

Android and iOS remain supported architectural targets. Only activated release targets receive release/device gates; initial local Windows validation focuses on Android.

### FM-05 — first genuine shared packages

Materialize only packages with immediate real Web+Mobile consumers. Initial accepted candidates:

```text
@dante/design-tokens
@dante/i18n
@dante/time
```

Do not create `@dante/api-client` before real FastAPI OpenAPI exists. Do not create a shared feature package before genuine cross-platform reuse exists.

Directly validate:

- workspace resolution;
- package exports;
- no deep/private cross-boundary import;
- Web consumption;
- Mobile consumption;
- framework-free core rules.

### FM-06 — architecture, test and generation enforcement

Activate only real checks with real consumers, including as applicable:

- ESLint architecture/boundary rules;
- feature/package cycle detection;
- strict typecheck;
- unit/component baseline;
- Web build and E2E smoke;
- Mobile test/bundle smoke;
- deterministic generated-source drift checks;
- design-token generation.

A future GitHub required check is not configured until its real emitted context has been observed and proven meaningful.

### FM-07 — materialization baseline closure

Closure requires evidence that a clean developer path can reproduce the accepted base:

```text
clean authoritative checkout
→ governed runtime versions
→ install
→ lint
→ typecheck
→ Web build/run
→ Mobile baseline/run on applicable local target
→ shared-package imports
→ architecture violations rejected
```

Only after this baseline is directly validated should a product feature such as Access rely on it as production infrastructure.

## 5. Carried direct-validation register

All start as **NOT RUN**:

```text
FM-V01 Node 24 WSL runtime resolution
FM-V02 pnpm 11 install/workspace resolution
FM-V03 preferred isolated dependency layout with Expo/native graph
FM-V04 evidence-driven hoisted fallback if required
FM-V05 Turbo task graph
FM-V06 TypeScript strict cross-workspace graph
FM-V07 ESLint/import/boundary/cycle enforcement
FM-V08 Vite/React production build
FM-V09 Windows browser ↔ WSL Vite
FM-V10 Expo SDK 57 / RN compatible baseline
FM-V11 WSL Metro ↔ Windows Android emulator/device
FM-V12 package exports / forbidden deep imports
FM-V13 DTCG → Web CSS + Native TS token generation
FM-V14 Web/Mobile i18n shared-core consumption
FM-V15 Temporal/time shared-core consumption
FM-V16 TanStack Form Web + RN + Zod when first real form activates
FM-V17 TanStack Query remote path when first real remote path exists
FM-V18 OpenAPI → Orval when real backend OpenAPI exists
FM-V19 PowerSync + OP-SQLite + SQLCipher encrypted lifecycle when sync scope activates
FM-V20 offline upload/accept/reject/conflict reconciliation when backend path exists
FM-V21 identity-scoped local DB lifecycle when Auth/session scope exists
FM-V22 versioned Web runtime config when delivery bootstrap activates
FM-V23 Cloudflare deployment when remote Web delivery activates
FM-V24 Sentry integration when observability activates
FM-V25 EAS build/update/release path when mobile release infrastructure activates
```

Not every validation belongs to the initial scaffold commit. Deferred items remain explicit `NOT RUN`, never silently converted to PASS.

## 6. Product-feature boundary

Access is the intended first production frontend vertical slice after the materialization baseline is stable enough to support it.

Home may continue separately as prototype/design evidence while its design is still evolving.

Materialization itself does **not** authorize:

- invented AuthN/AuthZ transport contracts;
- invented FastAPI endpoints;
- canonical state logic in the frontend;
- product UI copied from prototypes before the relevant base is ready;
- broad shared package extraction.

## 7. Documentation/onboarding requirement

A competent developer who did not participate in the chat must be able to determine from the repository:

- required machine tooling;
- exact/guided setup sequence;
- runtime/package versions;
- where Web/Mobile/backend/infra run;
- normal commands;
- architecture boundaries;
- validation commands;
- troubleshooting/repair entry points;
- what is selected versus directly proven.

Chat memory is never required to reproduce the frontend environment.

## 8. Write discipline inside this workstream

Each materialization slice gets its own exact remote write gate and QA.

Do not combine unrelated environment repairs, dependency additions, Web scaffold, Mobile scaffold and product feature work merely to reduce commit count.

Before each dependency/materialization write:

1. verify branch HEAD;
2. verify current primary compatibility documentation when version-sensitive;
3. state exact CREATE/UPDATE/DELETE paths;
4. state validation expected from that slice;
5. write only authorized paths;
6. run/record applicable direct evidence;
7. compare expected versus actual paths;
8. preserve `NOT RUN` for evidence not actually executed.

## 9. Exact next action

```text
FM-00 WORKSTATION PREFLIGHT
```

No installation yet.

Run the read-only WSL preflight from `../development/frontend-local-development.md`, return the complete output, classify the existing machine state, and only then authorize FM-01 installation/repair.
