# Workstream — Frontend Materialization

- Status: **ACTIVE — FM-02B ROOT ENGINEERING TOOLING PASS**
- Branch: `feature/frontend-materialization`
- Opening base: `ff46eb16b971b1fde96eef9047b09faa02e1a5db`
- Current validated workspace commit: `7ad88e2fbba1e8140149be05f9a3fe3005ad0488`
- Frontend Engineering Foundation: **CLOSED / ACCEPTED / FINAL REVIEW PASS / integrated via PR #22**
- Production frontend scaffold: **ROOT WORKSPACE + ENGINEERING TOOLING MATERIALIZED**
- Machine runtime baseline: **PASS**
- Root engineering dependencies: **INSTALLED / PINNED / LOCKED**
- Direct frontend validation: **PARTIAL — FM-V01/FM-V02 PASS; root tooling baseline directly validated; remaining register scoped below**
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

```text
selected != installed
installed != configured
configured != directly validated
direct scenario PASS != whole-frontend PASS
```

No component receives a direct `PASS` merely because a package was added or a command returned successfully once.

Version-sensitive dependencies are reverified against current primary documentation immediately before installation. The accepted major/line remains the design baseline; exact patches are fixed during materialization after compatibility verification.

## 3. Developer topology

Primary LOCAL posture:

```text
WINDOWS 11
├── JetBrains / PyCharm UI
├── browser
├── Android Studio / Android emulator
└── Docker Desktop

WSL2 / Linux
├── linked DANTE Git worktree(s)
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
ONE authoritative Git repository/history
purpose-specific linked Git worktrees inside WSL are allowed
NO divergent independent Windows + WSL clones/source trees
NO cross-OS shared node_modules tree
```

Observed parallel worktree topology:

```text
/home/mattia/projects/dante
feature/backend-scaffold

/home/mattia/projects/dante-frontend
feature/frontend-materialization
```

Detailed developer/onboarding authority: `../development/frontend-local-development.md`.

## 4. Materialization phases

### FM-00 — workstation preflight — PASS

Observed:

```text
WSL2 kernel                 PASS
Ubuntu                      24.04.4 LTS
Git                         2.43.0 /usr/bin/git
Docker CLI                  29.7.2 /usr/bin/docker
Docker Compose              5.4.0
frontend checkout           /home/mattia/projects/dante-frontend
Windows Node leakage        none observed
```

The preflight initially found no Linux Node/npm/pnpm/Corepack installation, which allowed a clean runtime setup.

### FM-01 — runtime and package-manager baseline — PASS

Materialized machine-level WSL frontend tooling:

```text
fnm         1.39.0
Node        24.19.0
npm         11.17.0
pnpm        11.22.0
```

Observed installation prerequisites for this path:

```text
unzip
libatomic1
```

`libatomic1` was required by the pnpm standalone Linux executable on this Ubuntu 24.04 WSL installation.

Direct checks:

```text
node Linux-side resolution      PASS
npm Linux-side resolution       PASS
pnpm Linux-side resolution      PASS
isolated login-shell selection  PASS
fnm .node-version selection     PASS
```

### FM-02 — root JavaScript workspace

#### FM-02A — minimal workspace authority — PASS

Repository authorities now exist:

```text
.node-version
package.json
pnpm-workspace.yaml
pnpm-lock.yaml
```

Exact runtime/package-manager authority:

```text
Node        24.19.0
pnpm        11.22.0
```

Workspace roots are reserved for real consumers only:

```text
apps/*
packages/*
```

Direct evidence:

```text
pnpm install                       PASS
pnpm install --frozen-lockfile     PASS
lockfile generated by pnpm         PASS
unexpected apps/                   0
unexpected packages/               0
unexpected node_modules/           0 in empty-workspace baseline
```

Remote commit:

```text
c3f7945da7137b2bdd9e9f8922af452f1a79770f
build: establish frontend workspace runtime baseline
```

Exact changed paths in that commit:

```text
.node-version
package.json
pnpm-lock.yaml
pnpm-workspace.yaml
```

No Web, Mobile, shared package or product code was created.

#### FM-02B — root engineering tooling — PASS

Materialized exact root engineering pins:

```text
TypeScript          6.0.3
Turborepo           2.10.11
ESLint              10.8.1
@eslint/js          10.0.1
typescript-eslint   8.67.0
Prettier            3.9.0
```

Repository authorities added:

```text
turbo.json
tsconfig.base.json
eslint.config.mjs
prettier.config.mjs
.prettierignore
```

`package.json` now provides predictable root scripts for build/dev/lint/format/test/typecheck. `pnpm-lock.yaml` is generated by pnpm from the real WSL installation and records the exact dependency graph; it is not hand-authored.

Compatibility evidence captured before installation:

```text
typescript-eslint 8.67.0 peer range
TypeScript >=4.8.4 <6.1.0
ESLint ^8.57.0 || ^9.0.0 || ^10.0.0
Node includes >=21.1.0
```

This directly covers the selected TypeScript `6.0.3`, ESLint `10.8.1`, and Node `24.19.0` combination.

Direct WSL evidence:

```text
pnpm install                                  PASS
pnpm exec tsc --version                       6.0.3
pnpm exec turbo --version                     2.10.11
pnpm exec eslint --version                    10.8.1
pnpm exec prettier --version                  3.9.0
pnpm lint                                     PASS
pnpm format:check                             PASS
TypeScript base-config temporary probe        PASS
Turbo configuration dry-run                   PASS
pnpm install --frozen-lockfile                PASS
```

The initial `prettier --check .` found only quote-style drift in `pnpm-workspace.yaml`; the repository file was aligned to the configured Prettier style and the check was rerun successfully. This was a real repair, not a suppressed failure.

A direct `tsc --showConfig -p tsconfig.base.json` invocation was not treated as a valid standalone acceptance gate because the base config intentionally has no source inputs. Instead, a temporary TypeScript project extending `tsconfig.base.json` compiled successfully; no probe file was added to the repository.

Remote FM-02B sequence:

```text
0e3872ce8028d0bbf67f209f7ad3c605329dc251
build: materialize root frontend engineering tooling

ab5405d13d667ee24287ad1cfa21773aae638794
style: align prettier root config

459373d9dbbe2938079ba1e94a2e0251dcab49f6
style: align workspace manifest with prettier

7ad88e2fbba1e8140149be05f9a3fe3005ad0488
build: lock frontend engineering toolchain
```

The final lockfile commit changed exactly `pnpm-lock.yaml`: one modified path, zero unexpected paths.

FM-02B does **not** claim that cross-workspace TypeScript, real Turbo app task execution, architecture boundaries, package cycles, Web, or Mobile are validated; those require real consumers.

### FM-03 — minimal Web application — NEXT

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

Android and iOS remain supported architectural targets. Initial local Windows validation focuses on Android; release/device gates activate only for real release targets.

### FM-05 — first genuine shared packages

Materialize only packages with immediate real Web+Mobile consumers. Initial accepted candidates:

```text
@dante/design-tokens
@dante/i18n
@dante/time
```

Do not create `@dante/api-client` before real FastAPI OpenAPI exists. Do not create a shared feature package before genuine cross-platform reuse exists.

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
clean authoritative checkout/worktree
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

```text
FM-V01 Node 24 WSL runtime resolution — PASS
FM-V02 pnpm 11 install/workspace resolution — PASS
FM-V03 preferred isolated dependency layout with Expo/native graph — NOT RUN
FM-V04 evidence-driven hoisted fallback if required — NOT RUN
FM-V05 Turbo task graph — CONFIG DRY-RUN PASS; REAL WORKSPACE TASK GRAPH NOT RUN
FM-V06 TypeScript strict cross-workspace graph — BASE CONFIG PROBE PASS; CROSS-WORKSPACE NOT RUN
FM-V07 ESLint/import/boundary/cycle enforcement — ROOT ESLINT PASS; ARCHITECTURE/BOUNDARY/CYCLE NOT RUN
FM-V08 Vite/React production build — NOT RUN
FM-V09 Windows browser ↔ WSL Vite — NOT RUN
FM-V10 Expo SDK 57 / RN compatible baseline — NOT RUN
FM-V11 WSL Metro ↔ Windows Android emulator/device — NOT RUN
FM-V12 package exports / forbidden deep imports — NOT RUN
FM-V13 DTCG → Web CSS + Native TS token generation — NOT RUN
FM-V14 Web/Mobile i18n shared-core consumption — NOT RUN
FM-V15 Temporal/time shared-core consumption — NOT RUN
FM-V16 TanStack Form Web + RN + Zod when first real form activates — NOT RUN
FM-V17 TanStack Query remote path when first real remote path exists — NOT RUN
FM-V18 OpenAPI → Orval when real backend OpenAPI exists — NOT RUN
FM-V19 PowerSync + OP-SQLite + SQLCipher encrypted lifecycle when sync scope activates — NOT RUN
FM-V20 offline upload/accept/reject/conflict reconciliation when backend path exists — NOT RUN
FM-V21 identity-scoped local DB lifecycle when Auth/session scope exists — NOT RUN
FM-V22 versioned Web runtime config when delivery bootstrap activates — NOT RUN
FM-V23 Cloudflare deployment when remote Web delivery activates — NOT RUN
FM-V24 Sentry integration when observability activates — NOT RUN
FM-V25 EAS build/update/release path when mobile release infrastructure activates — NOT RUN
```

Deferred items remain explicit `NOT RUN`, never silently converted to PASS.

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
FM-03 MINIMAL WEB APPLICATION
```

FM-00, FM-01, FM-02A and FM-02B are directly validated at their stated scope. Before materializing Web, reverify the exact current compatible patches for the accepted React 19.2 / React DOM / Vite 8 / TanStack Router lines and create only the minimum production Web scaffold required to validate FM-V08 and FM-V09.

Mobile, shared packages and product surfaces remain outside FM-03 unless separately gated.
