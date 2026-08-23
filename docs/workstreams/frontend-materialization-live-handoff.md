# DANTE Frontend Materialization — LIVE HANDOFF

> TEMPORARY / DISPOSABLE SAVE-GAME.
>
> Purpose: make the frontend workstream resumable if the current chat dies.
> Keep this file updated after every substantive slice/gate.
> Delete it only when frontend materialization is fully closed and durable docs contain everything needed.

## 0. Resume protocol

Read this file completely, then read:

1. `docs/workstreams/frontend-materialization.md`
2. `docs/development/frontend-local-development.md`
3. `docs/decisions/ADR-008-frontend-engineering-stack.md`
4. `docs/decisions/ADR-009-frontend-architecture-boundaries.md`
5. referenced Frontend Engineering Foundation docs.

Before any repository write:

```bash
git fetch origin feature/frontend-materialization
git rev-parse HEAD
git rev-parse origin/feature/frontend-materialization
git status --short
```

Require remote HEAD to equal the approved PRE-SCOPE. No silent scope expansion.

The documentation-closure commit containing this file is self-referential and therefore cannot embed its own SHA without another commit. Resolve the current documentation closure SHA from `origin/feature/frontend-materialization`. The last directly validated implementation/CI SHA is recorded below.

## 1. Repository / branch / workstation

```text
repository  MattiaRubino/dante
worktree    /home/mattia/projects/dante-frontend
branch      feature/frontend-materialization
opening     ff46eb16b971b1fde96eef9047b09faa02e1a5db
```

Execution ownership:

```text
WSL2/Linux
Git / Node / pnpm / Turbo / Vite / Metro / Expo CLI / Playwright

Windows
Firefox/browser / Android Studio / Android emulator / ADB / JetBrains UI
```

Hard invariant:

```text
ONE authoritative Git history
WSL-backed source/worktrees
NO divergent Windows clone
NO cross-OS shared node_modules
```

Do not merge/rebase `main` into this branch unless separately scoped.

## 2. Current checkpoint

Last directly validated implementation/CI commit:

```text
31deffddd35f69d48bee82465e0385e508c42876
ci: materialize frontend validation workflow
```

Current durable documentation closure before the active FM-07 repair:

```text
8ec088f0fce1db1e6116fa15acc2302981616ac5
docs: close FM-06E frontend CI
```

Current state:

```text
FM-06A dependency architecture enforcement     PASS
FM-06B generated-source drift enforcement      PASS
FM-06C real unit-test baseline                  PASS
FM-06D Web E2E + Mobile bundle smoke            PASS
FM-06E GitHub-hosted CI orchestration           PASS
FM-06                                             COMPLETE
FM-07 clean materialization baseline            REPAIR MATERIALIZED / CLEAN RETEST REQUIRED
```

## 3. Completed materialization checkpoints

```text
FM-02A c3f7945da7137b2bdd9e9f8922af452f1a79770f
FM-02B 7ad88e2fbba1e8140149be05f9a3fe3005ad0488
FM-03  1568d90091064162da9a438f3555675f1921c226
FM-04  3c150c4806191f0347b64c645d53168123ce0ede
FM-05A acd846a06614270fda9d66542a3fdc87fca7202e
FM-05B 5e5fae5d696a5da6b457e3198b70f642245ec323
FM-05C aeb43e9e5ed7add42464e61f5c02acd6a53fed85
FM-06A 38dbbd3efb764a8419f4498d27a2e29a3602fc5d
FM-06B 362b95a415ac7845260daf19cc99547501151eaa
FM-06C 610e33a7a31987d97564b1d6004a7b9896acaedc
FM-06D d6138f5f5049e8fc11f877b774ff0191af44069f
FM-06E 31deffddd35f69d48bee82465e0385e508c42876
```

Known durable closures:

```text
FM-05A closure  d4d99b157bab9e00c4f0285bf82745e73a9c944d
FM-05B closure  098be4c815eb724c32f49c277b058e85df81e03a
FM-05C closure  61d19795867e13818a2d43252906b565d23e96e5
FM-06A closure  b57709b4ce073ec179b4e55dc6dda72f509641a4
FM-06B closure  ae0ff9e9849ff3aedcd095a645750993297c4384
FM-06D closure  a481e24936c745c3573077a464a2af8a24794d1b
FM-06E/FM-06 closure 8ec088f0fce1db1e6116fa15acc2302981616ac5
```

## 4. Accepted toolchain

```text
Node                        24.19.0
pnpm                        11.22.0
TypeScript                  6.0.3
Turborepo                   2.10.11
ESLint                      10.8.1
Prettier                    3.9.0
dependency-cruiser          18.2.0
Vitest                      4.1.11
@playwright/test            1.62.1

Web
React / React DOM           19.2.8
Vite                        8.2.1
TanStack Router             1.170.31

Mobile
Expo                        57.0.9 specifier / 57.0.15 lock resolution observed
React Native                0.86.2
React                       19.2.3
Expo Router                 57.0.9 specifier / 57.0.15 lock resolution observed

Shared
i18next                     26.3.6
react-i18next               17.0.11
temporal-polyfill           1.0.4
Terrazzo                    2.7.1
```

## 5. Shared authority model

```text
visible copy / labels / messages / a11y -> @dante/i18n
visual semantic values                  -> @dante/design-tokens
platform control presentation           -> future Web/Mobile design systems
assets                                  -> versioned asset authority
click/workflow behavior                 -> owning feature logic
```

Do not create a universal dictionary mixing unrelated concerns. Do not create `@dante/api-client` until real FastAPI OpenAPI exists.

## 6. FM-06 enforcement baseline — COMPLETE

### FM-06A dependency architecture — PASS

```text
implementation 38dbbd3efb764a8419f4498d27a2e29a3602fc5d
command        pnpm architecture:check
observed       36 modules / 45 dependencies / 0 violations
```

Rules reject unresolved production imports, source cycles, Web->Mobile, Mobile->Web, shared->apps, production->prototypes and framework/platform dependencies from shared cores.

### FM-06B generated-source drift — PASS

```text
implementation 362b95a415ac7845260daf19cc99547501151eaa
command        pnpm generated:check
```

Checked committed outputs:

```text
packages/design-tokens/generated/web.css
packages/design-tokens/generated/native.ts
apps/web/src/routeTree.gen.ts
```

### FM-06C unit baseline — PASS

```text
implementation 610e33a7a31987d97564b1d6004a7b9896acaedc
Vitest         4.1.11
@dante/time    5 PASS
@dante/i18n    5 PASS
Turbo          2 successful / 2 total
```

Time coverage includes Temporal parsing, Europe/Rome DST, Instant/ZonedDateTime round trip and duration arithmetic. i18n coverage includes locale/default/fallback, Italian/English runtime, resource-shape parity and strict explicit `common` namespace selectors.

### FM-06D Web E2E + Mobile bundle smoke — PASS

```text
implementation d6138f5f5049e8fc11f877b774ff0191af44069f
Playwright     Chromium / headless / 1 worker / Vite production preview
Web E2E        1 real test PASS
Mobile         Expo Android production export / Hermes .hbc PASS
observed .hbc  4,077,727 bytes in FM-06D
```

Direct Android emulator/Hermes runtime from FM-04 remains stronger device-runtime evidence than bundle smoke.

### FM-06E GitHub-hosted CI — PASS

```text
implementation 31deffddd35f69d48bee82465e0385e508c42876
workflow       Frontend CI
runner         ubuntu-24.04
```

Real hosted evidence:

```text
Frontend CI #3
commit        31deffddd35f69d48bee82465e0385e508c42876
event         push
overall       SUCCESS
duration      1m 14s
Quality       PASS / 47s
Web E2E       PASS / 47s
Mobile Bundle PASS / 53s
```

Observed real check context names:

```text
Quality
Web E2E
Mobile Bundle
```

Required checks are NOT configured. Branch protection remains separate governance scope.

## 7. Normal local commands

```bash
pnpm install --frozen-lockfile
pnpm lint
pnpm format:check
pnpm typecheck
pnpm architecture:check
pnpm generated:check
pnpm test
pnpm test:e2e:web
pnpm mobile:bundle:check
pnpm build
```

Fresh WSL Playwright setup:

```bash
pnpm --filter @dante/web exec playwright install chromium
pnpm --filter @dante/web exec playwright install-deps chromium
```

## 8. Known diagnostics retained

```text
FM-06C root-output parser
-> colored/prefixed Turbo output caused a false-negative evidence parser
-> normalize ANSI/prefixes; test execution itself was PASS

FM-06C workspace React/react-dom peer warning
-> pre-existing before Vitest
-> Web direct React/ReactDOM = 19.2.8/19.2.8
-> Mobile direct React = 19.2.3, no direct react-dom

FM-06C strict i18next selector typecheck
-> $.runtime / $.gesture rejected
-> repaired to $.common.runtime / $.common.gesture

FM-06D Chromium host dependency
-> libnspr4.so missing before browser page creation
-> official Playwright Linux dependency installer repair

FM-06D semantic E2E locator
-> purpose + Temporal shared one <dd>
-> anchor to visible Scopo row; application unchanged
```

## 9. FM-07 clean materialization — ATTEMPT 1

Purpose:

```text
prove clean frontend materialization from a fresh remote clone without relying
on accumulated repository state, local pnpm store, or cached browser binaries
```

Attempt-1 source:

```text
remote HEAD
8ec088f0fce1db1e6116fa15acc2302981616ac5

fresh HTTPS clone
no node_modules
clean Git state
isolated temporary pnpm store
isolated temporary Playwright browser path
```

Direct PASS before the final immutability check:

```text
Node 24.19.0
pnpm 11.22.0
pnpm install --frozen-lockfile from isolated store
lockfile unchanged
Expo `expo install --check`: Dependencies are up to date
Playwright Chromium headless-shell fresh download
Playwright Linux dependency bootstrap
format:check
lint
5-package typecheck
architecture:check = 36 modules / 45 dependencies / 0 violations
generated:check
@dante/time 5 tests PASS
@dante/i18n 5 tests PASS
Turbo unit tasks 2/2 PASS
Web production Playwright E2E 1 PASS
Mobile Expo Android Hermes bundle smoke PASS
production build PASS
```

Attempt-1 Mobile bundle evidence:

```text
Expo Router resolved 57.0.15
Android Hermes .hbc
4,077,728 bytes
non-empty
cleanup PASS
```

### FM-07 peer-warning re-evaluation

Fresh clean install reproduced exactly:

```text
pnpm peers check exit 1
unmet peer react
Installed: 19.2.3
Wanted: ^19.2.8
owner shown: react-dom@19.2.8
```

At the same fresh checkout, Expo SDK compatibility authority reported:

```text
Dependencies are up to date
Mobile React 19.2.3
React Native 0.86.2
Expo resolved 57.0.15
```

Classification remains:

```text
KNOWN WORKSPACE PEER DIAGNOSTIC
reproducible on a fresh install
NOT evidence that Mobile's directly validated Expo/RN baseline is incompatible
NOT justification for React version changes
```

Do not add pnpm peer suppression, packageExtensions, nodeLinker/hoisting changes or arbitrary React version changes merely to make `pnpm peers check` green.

### FM-07 attempt-1 first real failure

Every functional/build/test gate above passed. The final repository immutability check failed only because normal Turbo execution produced untracked local cache files:

```text
.turbo/cache/*-manifest.json
.turbo/cache/*-meta.json
.turbo/cache/*.tar.zst
```

Root cause:

```text
Turborepo local cache is expected machine-generated state
.gitignore did not contain .turbo/
therefore normal validation left repository-visible untracked residue
```

This is repository hygiene, not a build/test/runtime failure.

Approved repair gate:

```text
BRANCH
feature/frontend-materialization

PRE-SCOPE
8ec088f0fce1db1e6116fa15acc2302981616ac5

CREATE
none

UPDATE
.gitignore
docs/workstreams/frontend-materialization-live-handoff.md

DELETE
none

PURPOSE
Ignore Turborepo's machine-generated local cache and record the exact FM-07
clean-materialization evidence/failure without widening architecture.

CHANGE
add `.turbo/` to repository ignore authority

EXPLICITLY OUT OF SCOPE
React version changes
pnpm peer suppression
packageExtensions
nodeLinker/hoisting changes
Turbo remote cache
CI changes
product UI
backend integration
main synchronization
```

## 10. Current FM-07 gate after repair

Status:

```text
REPAIR MATERIALIZED
CLEAN RETEST REQUIRED BEFORE FM-07 PASS
```

Next evidence must come from a NEW fresh checkout at the repaired remote HEAD, not from deleting `.turbo` inside the failed attempt clone.

Required retest:

```text
fresh exact remote clone
Node 24.19.0
pnpm 11.22.0
isolated fresh pnpm store
pnpm install --frozen-lockfile
Expo dependency compatibility check
pnpm peers check diagnostic/classification
isolated fresh Playwright Chromium headless shell
format:check
lint
typecheck
architecture:check
generated:check
unit tests
Web E2E
Mobile Android Hermes bundle smoke
production build
git diff --check
git diff --exit-code
git status --porcelain --untracked-files=all MUST be empty
```

FM-07 is not PASS until the complete retest succeeds from the repaired HEAD.

## 11. Write / QA governance

Before repository writes:

```text
BRANCH
<exact branch>
PRE-SCOPE
<exact SHA>
CREATE
<exact paths>
UPDATE
<exact paths>
DELETE
<exact paths>
PURPOSE
...
EXPLICITLY OUT OF SCOPE
...
```

Immediately before first branch-visible write, re-read remote HEAD and require it to equal PRE-SCOPE. No silent expansion.

After writes:

```text
validate exact changed paths
zero unexpected paths
run applicable real QA
remote readback
```

No direct `main` work. No casual force push. No unscoped main merge/rebase.

## 12. Still NOT RUN / deferred

```text
hoisted pnpm fallback                         NOT RUN / not needed
feature-specific architecture rules           NOT RUN
required branch checks                        NOT RUN
Firefox/WebKit automated E2E                  NOT RUN
product Access/Home E2E                       NOT RUN
TanStack Form + Zod real form                 NOT RUN
TanStack Query first remote path              NOT RUN
OpenAPI -> Orval                              NOT RUN
PowerSync / OP-SQLite / SQLCipher             NOT RUN
offline reconciliation                        NOT RUN
identity-scoped local DB lifecycle             NOT RUN
versioned Web runtime config                   NOT RUN
Cloudflare deployment                         NOT RUN
Sentry                                         NOT RUN
APK/AAB release build                         NOT RUN
iOS runtime/release                            NOT RUN
EAS release path                              NOT RUN
coverage thresholds                           NOT RUN
main synchronization                          NOT RUN
FM-07 clean baseline                          IN PROGRESS
```

Preserve these as NOT RUN until their real scope activates.
