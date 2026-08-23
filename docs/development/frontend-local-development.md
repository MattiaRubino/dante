# Frontend Local Development and Workstation Runbook

- Status: **CURRENT FOR `feature/frontend-materialization`**
- Purpose: reproducible frontend workstation setup, installation, validation and LOCAL runtime topology
- Foundation authority: Frontend Engineering Foundation integrated via PR #22
- Current execution state: **FM-07 CLEAN MATERIALIZATION BASELINE PASS / FINAL HOSTED-CI PROOF + TEMPORARY CLEANUP PENDING**

## 1. Core posture

DANTE uses one authoritative Git history with active source/worktrees under WSL/Linux semantics.

```text
Windows 11
├── JetBrains / PyCharm UI
├── browser
├── Android Studio / emulator
└── Docker Desktop

WSL2 / Linux
├── linked DANTE worktree(s)
├── Git / Node / pnpm / Turbo
├── Vite / Playwright
├── Metro / Expo CLI
└── Docker CLI
```

Normal ownership:

```text
Git worktrees            WSL filesystem
Node/pnpm/Turbo          WSL
Vite                     WSL
Metro/Expo CLI           WSL
Playwright Chromium      WSL/Linux
PyCharm/JetBrains UI     Windows using WSL project/tooling
browser                  Windows for normal manual Web work
Android Studio/emulator  Windows
Docker daemon            Docker Desktop / WSL integration
```

Hard rules:

```text
one authoritative Git history
linked WSL worktrees allowed
no divergent Windows + WSL source clones
no cross-OS shared node_modules
no manual source copying between Windows and WSL trees
```

Observed frontend worktree:

```text
/home/mattia/projects/dante-frontend
feature/frontend-materialization
```

Avoid `/mnt/c/...` as the authoritative source/worktree unless concrete evidence requires it.

## 2. Governed runtime and package manager

```text
fnm   1.39.0
Node  24.19.0
npm   11.17.0
pnpm  11.22.0
```

Repository authorities:

```text
.node-version
package.json
pnpm-workspace.yaml
pnpm-lock.yaml
```

Do not run broad blind upgrades such as `pnpm update --latest` without an explicit upgrade scope and compatibility QA.

## 3. Repository-managed exact pins

```text
Root engineering
TypeScript                    6.0.3
Turborepo                     2.10.11
ESLint                        10.8.1
@eslint/js                    10.0.1
typescript-eslint             8.67.0
Prettier                      3.9.0

Architecture
dependency-cruiser            18.2.0

Unit testing
Vitest                        4.1.11

Web E2E
@playwright/test              1.62.1

Web
React                         19.2.8
React DOM                     19.2.8
Vite                          8.2.1
@vitejs/plugin-react          6.1.0
@tanstack/react-router        1.170.31
@tanstack/router-plugin       1.168.34

Mobile
Expo specifier                57.0.9
Expo clean-install resolution 57.0.15
React Native                  0.86.2
React                         19.2.3
Expo Router specifier         57.0.9
Expo Router resolution        57.0.15
Gesture Handler               2.32.0
Reanimated                    4.5.1
Safe Area Context             5.7.0
Screens                       4.26.2
Worklets                      0.10.1

Design tokens
@terrazzo/cli                 2.7.1
@terrazzo/parser              2.7.1
@terrazzo/plugin-css          2.7.1

i18n
i18next                       26.3.6
react-i18next                 17.0.11

Time
temporal-polyfill             1.0.4
```

## 4. Repository authorities

Root/tooling:

```text
.node-version
package.json
pnpm-workspace.yaml
pnpm-lock.yaml
turbo.json
tsconfig.base.json
eslint.config.mjs
prettier.config.mjs
.prettierignore
.gitignore
dependency-cruiser.config.mjs
tooling/check-generated.mjs
tooling/check-mobile-bundle.mjs
.github/workflows/frontend-ci.yml
```

Web:

```text
apps/web/package.json
apps/web/index.html
apps/web/tsconfig.json
apps/web/vite.config.ts
apps/web/playwright.config.ts
apps/web/e2e/runtime.spec.ts
apps/web/src/**
```

Mobile:

```text
apps/mobile/package.json
apps/mobile/app.config.ts
apps/mobile/tsconfig.json
apps/mobile/app/**
apps/mobile/src/**
```

Shared packages:

```text
packages/design-tokens/**
packages/i18n/**
packages/time/**
```

Generated outputs are committed deterministic runtime source and must not be hand-edited.

Local/machine-generated paths that must not become repository-visible include:

```text
node_modules/
dist/
.expo/
playwright-report/
test-results/
.turbo/
```

`.turbo/` is deliberately ignored because normal Turborepo validation creates machine-local cache files there.

## 5. Normal root commands

```bash
pnpm install
pnpm install --frozen-lockfile
pnpm dev
pnpm lint
pnpm lint:fix
pnpm format
pnpm format:check
pnpm typecheck
pnpm architecture:check
pnpm generated:check
pnpm test
pnpm test:e2e:web
pnpm mobile:bundle:check
pnpm build
```

Task meaning:

```text
pnpm test
-> turbo run test
-> @dante/i18n + @dante/time Vitest suites

pnpm test:e2e:web
-> @dante/web Playwright suite
-> Vite production build + preview
-> Chromium headless

pnpm mobile:bundle:check
-> Expo Android production export
-> require non-empty Hermes .hbc
-> remove temporary export
```

## 6. Web LOCAL manual runtime

From WSL:

```bash
cd ~/projects/dante-frontend
pnpm --filter @dante/web dev
```

Open from Windows:

```text
http://localhost:5173/
```

Directly validated topology:

```text
WSL Vite
-> Windows localhost forwarding
-> Firefox
-> DANTE route /
```

## 7. Mobile LOCAL interactive runtime

Start Windows Android emulator first, then from WSL:

```bash
cd ~/projects/dante-frontend/apps/mobile
pnpm exec expo start --localhost
```

Verify device and reverse mapping:

```bash
powershell.exe -NoProfile -Command '& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" devices'
powershell.exe -NoProfile -Command '& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" reverse tcp:8081 tcp:8081'
powershell.exe -NoProfile -Command '& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" reverse --list'
```

Launch when needed:

```bash
powershell.exe -NoProfile -Command '& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" shell am start -a android.intent.action.VIEW -d "exp://127.0.0.1:8081"'
```

Diagnose in order:

```text
ADB device
-> reverse mapping
-> Metro
-> manifest
-> bundle
-> Expo Go/client runtime
```

Do not introduce tunnels, Metro overrides, hoisting, Windows Node, a second clone or project `updates.url` without contradictory evidence.

## 8. Playwright Web E2E

Repository dependency:

```text
@playwright/test 1.62.1
apps/web devDependency
```

The browser binary and Linux shared-library dependencies are machine-owned and are not committed to Git.

Fresh Ubuntu/WSL setup after `pnpm install --frozen-lockfile`:

```bash
cd ~/projects/dante-frontend
pnpm --filter @dante/web exec playwright install chromium
pnpm --filter @dante/web exec playwright install-deps chromium
```

`install-deps chromium` may invoke `sudo`/APT. The directly validated host required `libnspr4` and related Chromium runtime libraries.

Run:

```bash
pnpm test:e2e:web
```

Current configuration:

```text
browser                  Chromium
headless                 true
workers                  1
retries                  0
base URL                 http://127.0.0.1:4173
server                   Vite production preview
reuseExistingServer      false
```

Current real test validates:

```text
route /
Frontend pronto
DANTE Web
Percorso /
Scopo / Scaffold diagnostico FM-03
2026-08-22T20:00:00+02:00[Europe/Rome]
```

## 9. Mobile headless production-bundle smoke

Run:

```bash
pnpm mobile:bundle:check
```

Path:

```text
apps/mobile
-> expo export --platform android
-> Metro production bundling
-> Hermes bytecode enabled
-> temporary OS directory outside repository
```

Acceptance requires at least one non-empty Android `.hbc` and successful cleanup.

Direct evidence:

```text
FM-06D observed .hbc    4,077,727 bytes
FM-07 clean retest      4,077,727 bytes
cleanup                 PASS
```

This is not an APK/AAB release build and not device execution. FM-04 Android emulator/Hermes runtime remains stronger direct runtime evidence.

## 10. Unit-test baseline

```text
Vitest 4.1.11
@dante/time  5 tests PASS
@dante/i18n  5 tests PASS
root Turbo   2 successful / 2 total
```

Time coverage:

```text
Temporal parsing
Europe/Rome spring DST
Instant <-> ZonedDateTime round trip
PlainDateTime + Duration arithmetic
ZonedDateTime instant preservation
```

i18n coverage:

```text
supported locales
default/fallback locale
Italian runtime
English runtime
unsupported locale -> Italian fallback
IT/EN resource leaf-shape parity
strict namespace selectors
```

Accepted selector form:

```text
$.common.runtime...
$.common.gesture...
```

## 11. Architecture enforcement

Run:

```bash
pnpm architecture:check
```

Current observed graph:

```text
36 DANTE-owned modules
45 dependencies cruised
0 violations
```

Rules reject unresolved imports, source cycles, Web->Mobile, Mobile->Web, shared->apps, production->prototypes and framework/platform dependencies from shared cores.

## 12. Generated-source drift

Run:

```bash
pnpm generated:check
```

Checked outputs:

```text
packages/design-tokens/generated/web.css
packages/design-tokens/generated/native.ts
apps/web/src/routeTree.gen.ts
```

The checker uses real Terrazzo and TanStack Router generation paths, compares byte-for-byte and restores pre-check bytes in all cases.

## 13. GitHub-hosted frontend CI

Repository authority:

```text
.github/workflows/frontend-ci.yml
name: Frontend CI
runner: ubuntu-24.04
permissions: contents: read
```

Current triggers:

```text
pull_request -> main
push -> main
push -> feature/frontend-materialization  TEMPORARY BOOTSTRAP
```

The feature-branch push trigger remains only until the FM-07 documentation closure receives a final hosted-CI proof. It must then be removed in a separately authorized final cleanup scope.

CI bootstrap:

```text
Node 24.19.0 exact
pnpm 11.22.0 exact
pnpm store cache only
explicit pnpm install --frozen-lockfile
no node_modules cache
no Playwright browser cache
no Turbo remote cache
```

Jobs / observed real context names:

```text
Quality
Web E2E
Mobile Bundle
```

Authoritative prior hosted proof:

```text
Frontend CI #3
commit       31deffddd35f69d48bee82465e0385e508c42876
overall      SUCCESS
Quality      PASS
Web E2E      PASS
Mobile Bundle PASS
```

Required branch checks are not configured.

## 14. Known workspace peer diagnostic

A fresh FM-07 clean install reproduced exactly:

```text
pnpm peers check exit 1
unmet peer react
Installed: 19.2.3
Wanted: ^19.2.8
owner: react-dom@19.2.8
```

At the same clean checkout:

```text
expo install --check       Dependencies are up to date
Mobile React               19.2.3
React Native               0.86.2
Expo resolved              57.0.15
Web React / ReactDOM       19.2.8 / 19.2.8
```

Classification:

```text
KNOWN WORKSPACE PEER DIAGNOSTIC
reproducible on fresh install
non-blocking for validated Expo/RN baseline
```

Do not move Mobile React merely to silence it. Do not add peer suppression, `packageExtensions`, hoisting or `nodeLinker` changes without new causal evidence.

## 15. Clean-machine materialization — FM-07 PASS

The final clean baseline was proved from a new HTTPS clone at:

```text
e79beadbddcf401d1d20c483c2d15d0b3cce96ad
```

Procedure/evidence:

```text
fresh clone at exact remote HEAD
no node_modules
clean Git state
.turbo ignored
Node 24.19.0
pnpm 11.22.0
new isolated pnpm store
pnpm install --frozen-lockfile
lockfile unchanged
expo install --check PASS
known peer diagnostic reproduced exactly
new isolated Playwright Chromium headless-shell
Playwright Linux dependency bootstrap
format:check PASS
lint PASS
typecheck 5/5 PASS
architecture 36/45/0 PASS
generated:check PASS
@dante/time 5 PASS
@dante/i18n 5 PASS
Turbo tests 2/2 PASS
Web E2E 1 PASS
Mobile Hermes bundle PASS
production build PASS
git diff --check PASS
git diff --exit-code PASS
tracked residue 0
untracked residue 0
```

This is the accepted clean-machine target for the current frontend engineering baseline.

## 16. Troubleshooting discipline

For any failure:

```text
capture exact command
capture full output
identify owning layer
change one variable
rerun smallest relevant validation
record durable fix if project-specific
```

Ownership examples:

```text
Node/pnpm                      workstation/workspace
TypeScript                     package/root type contract
ESLint/Prettier                root engineering
Dependency Cruiser             dependency architecture
Vitest                         unit-test runner
Playwright assertion           Web E2E test contract
Chromium missing .so           WSL/Linux browser host dependency
Vite build/preview             Web toolchain
Metro/Expo export              Mobile bundling toolchain
ADB/emulator                   WSL<->Windows mobile adapter
GitHub Actions runner          hosted CI execution boundary
PowerSync/SQLite               future sync platform boundary
```

Do not respond to failures with random global installs, blanket cache deletion, force flags or broad version changes.

## 17. Current next action

FM-07 is PASS and the frontend materialization baseline is technically complete.

Next:

```text
1. observe the GitHub-hosted Frontend CI triggered by the FM-07 documentation closure commit
2. require Quality / Web E2E / Mobile Bundle PASS
3. separately authorize final cleanup:
   - remove temporary feature-branch push trigger
   - delete docs/workstreams/frontend-materialization-live-handoff.md
4. prepare integration/PR to main as separate scope
```

Still outside this closure:

```text
required branch checks / branch protection mutation
product Access/Home implementation
PowerSync
backend integration
deployment
main synchronization
```
