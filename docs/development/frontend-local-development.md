# Frontend Local Development and Workstation Runbook

- Status: **CURRENT FOR `feature/frontend-materialization`**
- Purpose: reproducible frontend workstation setup, installation, validation and LOCAL runtime topology
- Foundation authority: Frontend Engineering Foundation integrated via PR #22
- Current execution state: **FM-06D WEB E2E + MOBILE BUNDLE SMOKE PASS / FM-06 IN PROGRESS**

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
├── Vite
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

Machine prerequisites already observed on Ubuntu 24.04 WSL include `unzip` and `libatomic1` for the selected Node/pnpm setup path.

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
Expo                          57.0.9
React Native                  0.86.2
React                         19.2.3
Expo Router                  57.0.9
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

Do not run broad blind upgrades such as `pnpm update --latest` without an explicit upgrade scope and compatibility QA. Native-sensitive upgrades require compatibility-aware validation.

## 4. Current repository authorities

Root:

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
dependency-cruiser.config.mjs
tooling/check-generated.mjs
tooling/check-mobile-bundle.mjs
```

Web:

```text
apps/web/package.json
apps/web/index.html
apps/web/tsconfig.json
apps/web/vite.config.ts
apps/web/playwright.config.ts
apps/web/e2e/runtime.spec.ts
apps/web/src/main.tsx
apps/web/src/routes/__root.tsx
apps/web/src/routes/index.tsx
apps/web/src/styles.css
apps/web/src/routeTree.gen.ts
apps/web/src/bootstrap/i18n.ts
```

Mobile:

```text
apps/mobile/package.json
apps/mobile/app.config.ts
apps/mobile/tsconfig.json
apps/mobile/app/_layout.tsx
apps/mobile/app/index.tsx
apps/mobile/src/bootstrap/i18n.ts
```

Shared packages:

```text
packages/design-tokens/**
packages/i18n/src/index.ts
packages/i18n/src/index.test.ts
packages/i18n/src/resources/{it,en}/common.ts
packages/time/src/index.ts
packages/time/src/index.test.ts
```

Generated outputs are committed deterministic runtime source and must not be hand-edited.

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

Current root task meaning:

```text
pnpm test
-> turbo run test
-> @dante/i18n + @dante/time real Vitest suites

pnpm test:e2e:web
-> @dante/web Playwright suite
-> Vite production build + preview
-> Chromium headless

pnpm mobile:bundle:check
-> Expo SDK 57 Android production export
-> require non-empty Hermes .hbc
-> remove temporary export
```

## 6. Web LOCAL manual runtime

Start from WSL:

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

No `--host`, custom proxy, alternate clone or Windows Node process was required on the observed workstation.

## 7. Mobile LOCAL interactive runtime

Start Windows Android emulator first, then from WSL:

```bash
cd ~/projects/dante-frontend/apps/mobile
pnpm exec expo start --localhost
```

Verify device:

```bash
powershell.exe -NoProfile -Command '& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" devices'
```

Establish reverse mapping:

```bash
powershell.exe -NoProfile -Command '& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" reverse tcp:8081 tcp:8081'
```

Verify:

```bash
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

## 8. Playwright Web E2E setup — FM-06D PASS

Repository dependency:

```text
@playwright/test 1.62.1
apps/web devDependency
```

The browser binary and its Linux shared-library dependencies are machine-owned and are **not** committed to Git or represented as pnpm dependencies.

On a new Ubuntu/WSL developer machine, after `pnpm install --frozen-lockfile`:

```bash
cd ~/projects/dante-frontend
pnpm --filter @dante/web exec playwright install chromium
pnpm --filter @dante/web exec playwright install-deps chromium
```

`install-deps chromium` may invoke `sudo`/APT. On the directly validated Ubuntu 24.04 WSL host it installed the Linux packages needed by Chromium, including `libnspr4`, `libnss3`, fonts and related X/graphics/audio runtime libraries.

The initial Chromium launch failed with:

```text
chrome-headless-shell: error while loading shared libraries:
libnspr4.so: cannot open shared object file
```

This was a workstation/browser ELF dependency failure, not a DANTE Web or Playwright assertion failure. The accepted repair is the official Playwright dependency installer above, not adding Linux libraries to `package.json` and not changing the Web application.

Run E2E:

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

Locator lesson retained: `Scaffold diagnostico FM-03` and the Temporal value share one semantic `<dd>`. Do not use an `exact: true` locator expecting the purpose substring to be the element's entire text. The accepted test anchors to the visible `Scopo` definition-list row and asserts contained purpose + exact Temporal value.

Playwright local output directories are ignored:

```text
playwright-report/
test-results/
```

## 9. Mobile headless production-bundle smoke — FM-06D PASS

Run:

```bash
pnpm mobile:bundle:check
```

The checker executes the real Expo SDK 57 path:

```text
apps/mobile
-> expo export --platform android
-> Metro production bundling
-> Hermes bytecode enabled
-> temporary OS directory outside repository
```

Acceptance requires at least one non-empty Android `.hbc` bundle and successful cleanup of the temporary export.

Direct FM-06D evidence:

```text
Android export                                 PASS
Hermes .hbc                                    PASS
observed bundle size                           4,077,727 bytes
temporary output cleanup                       PASS
```

This is a deterministic bundle smoke, not an APK/AAB release build and not device execution. The earlier FM-04 Android emulator/Hermes runtime remains stronger direct runtime evidence.

## 10. Unit-test baseline — FM-06C PASS

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

Accepted strict selector form:

```text
$.common.runtime...
$.common.gesture...
```

## 11. Architecture enforcement

Run:

```bash
pnpm architecture:check
```

Current graph after FM-06C/FM-06D source additions:

```text
36 DANTE-owned modules in the enforced graph
45 dependencies cruised
0 violations
```

Current rules reject unresolved imports, source cycles, Web->Mobile, Mobile->Web, shared->apps, production->prototypes and framework/platform dependencies from shared cores.

`doNotFollow.path = node_modules` deliberately prevents third-party internals from becoming architecture roots while preserving external dependency edges.

## 12. Generated-source drift

Run:

```bash
pnpm generated:check
```

Checked committed outputs:

```text
packages/design-tokens/generated/web.css
packages/design-tokens/generated/native.ts
apps/web/src/routeTree.gen.ts
```

The checker uses the actual Terrazzo and TanStack Router Vite generation paths, compares byte-for-byte and restores the pre-check bytes in all cases.

Do not hand-edit generated output to make this gate green.

## 13. Shared package rules

### Design tokens

```text
user-visible copy -> @dante/i18n
visual semantic values -> @dante/design-tokens
```

The token package currently canonizes only real duplicated radii. Diagnostic colors/typography are not automatically brand authority.

### i18n

```text
Italian = primary/default/fallback
English = supported secondary
```

Core is framework-free. React integration stays app-owned. Source-first package internals use extensionless imports.

### Time

Use the explicit Temporal semantic vocabulary:

```text
Instant / PlainDate / PlainTime / PlainDateTime / ZonedDateTime / Duration
```

Do not use JavaScript `Date` as a universal semantic and do not infer timezone from locale.

## 14. Known dependency diagnostic

A workspace-wide peer diagnostic reports:

```text
react-dom@19.2.8 wants react ^19.2.8
Mobile direct React = 19.2.3
```

FM-06C proved this association existed before the unit-test materialization and did not change the Web/Mobile lockfile importer blocks.

Classification:

```text
KNOWN PRE-EXISTING WORKSPACE PEER WARNING
NOT introduced by Vitest or Playwright
```

Do not move Mobile React away from its directly validated Expo/RN baseline merely to silence it. Re-evaluate during FM-07 clean materialization closure if still observable.

## 15. Clean-machine target

A future developer should be able to execute:

```text
clone/create WSL worktree
-> select Node 24.19.0
-> activate pnpm 11.22.0
-> pnpm install --frozen-lockfile
-> install Playwright Chromium + chromium Linux deps
-> pnpm lint
-> pnpm format:check
-> pnpm typecheck
-> pnpm architecture:check
-> pnpm generated:check
-> pnpm test
-> pnpm test:e2e:web
-> pnpm mobile:bundle:check
-> pnpm build
-> start manual Web/Mobile runtimes when required
```

FM-07 will directly validate this clean materialization path. It is not yet whole-baseline PASS.

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
PowerSync/SQLite               future sync platform boundary
```

Do not respond to failures with random global installs, blanket cache deletion, force flags or broad version changes.

## 17. Current next action

Proceed to **FM-06E CI orchestration** with read-only discovery first.

Do not add required branch checks until the real emitted workflow/job context names are observed. CI must orchestrate already-real local gates rather than introduce a second independent validation architecture.

Still outside the closed FM-06D scope:

```text
GitHub Actions frontend CI
required branch checks
Firefox/WebKit automated E2E
product Access/Home E2E
APK/AAB/iOS release validation
EAS
coverage thresholds
PowerSync
backend integration
main synchronization
```
