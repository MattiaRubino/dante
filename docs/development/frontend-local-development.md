# Frontend Local Development and Workstation Runbook

- Status: **CURRENT / FRONTEND MATERIALIZATION CLOSED / PASS / INTEGRATED VIA PR #28**
- Purpose: reproducible frontend workstation setup, installation, validation and LOCAL runtime topology
- Foundation authority: Frontend Engineering Foundation integrated via PR #22
- Final clean-materialization source commit: `e79beadbddcf401d1d20c483c2d15d0b3cce96ad`
- FM-07 documentation closure + final hosted-CI proof commit: `c1a77f249c716e0cb35159ecf2ad2c63b0bf4007`
- Protected-main frontend integration: PR #28 / merge `f1aacb0724088e0b4b086008a5219c2fba5ce0cf`

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

Observed materialization worktree:

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

## 4. Repository authorities and generated/local state

Root/tooling authorities:

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

## 5. Fresh-machine materialization sequence

The current baseline was directly proven from a new HTTPS clone with no `node_modules`, a new isolated pnpm store and a new isolated Playwright browser path.

Recommended sequence:

```bash
pnpm install --frozen-lockfile

cd apps/mobile
CI=1 EXPO_NO_TELEMETRY=1 pnpm exec expo install --check
cd ../..

pnpm --filter @dante/web exec playwright install chromium
pnpm --filter @dante/web exec playwright install-deps chromium

pnpm format:check
pnpm lint
pnpm typecheck
pnpm architecture:check
pnpm generated:check
pnpm test
pnpm test:e2e:web
pnpm mobile:bundle:check
pnpm build

git diff --check
git diff --exit-code
git status --porcelain --untracked-files=all
```

Acceptance for the final Git status command is empty output.

The clean FM-07 proof additionally used an isolated temporary pnpm store and isolated Playwright browser directory to prove the baseline did not rely on previously downloaded repository/package/browser state.

## 6. Normal root commands

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

## 7. Web LOCAL manual runtime

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

## 8. Mobile LOCAL interactive runtime

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

## 9. Playwright Web E2E

Repository dependency:

```text
@playwright/test 1.62.1
apps/web devDependency
```

The browser binary and Linux shared-library dependencies are machine-owned and are not committed to Git.

Fresh Ubuntu/WSL setup after `pnpm install --frozen-lockfile`:

```bash
pnpm --filter @dante/web exec playwright install chromium
pnpm --filter @dante/web exec playwright install-deps chromium
```

`install-deps chromium` may invoke `sudo`/APT. The directly validated host required `libnspr4` and related Chromium runtime libraries. A missing `libnspr4.so` is a workstation/browser dependency failure, not evidence to modify the Web application or package graph.

Run:

```bash
pnpm test:e2e:web
```

Configuration:

```text
browser                  Chromium
headless                 true
workers                  1
retries                  0
base URL                 http://127.0.0.1:4173
server                   Vite production preview
reuseExistingServer      false
```

The real smoke validates:

```text
route /
Frontend pronto
DANTE Web
Percorso /
Scopo / Scaffold diagnostico FM-03
2026-08-22T20:00:00+02:00[Europe/Rome]
```

Purpose and Temporal value share one semantic `<dd>`; the accepted locator anchors to the visible `Scopo` definition row instead of assuming the purpose is the element's entire exact text.

## 10. Mobile headless production-bundle smoke

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

## 11. Unit-test baseline

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

## 12. Architecture and generated-source enforcement

Run:

```bash
pnpm architecture:check
pnpm generated:check
```

Current observed dependency graph:

```text
36 DANTE-owned modules
45 dependencies cruised
0 violations
```

Architecture rules reject unresolved imports, source cycles, Web->Mobile, Mobile->Web, shared->apps, production->prototypes and framework/platform dependencies from shared cores.

Generated outputs checked byte-for-byte:

```text
packages/design-tokens/generated/web.css
packages/design-tokens/generated/native.ts
apps/web/src/routeTree.gen.ts
```

The checker uses real Terrazzo and TanStack Router generation paths and restores pre-check bytes in all cases.

## 13. Shared authority model

```text
visible copy / labels / messages / a11y -> @dante/i18n
visual semantic values                  -> @dante/design-tokens
platform control presentation           -> Web/Mobile design-system layers when real UI requires them
assets                                  -> versioned asset authority
click/workflow behavior                 -> owning feature logic
```

Italian is the primary/default/fallback locale; English is the supported secondary locale. React integration remains app-owned. Time semantics use explicit Temporal types rather than JavaScript `Date` as a universal semantic.

Do not create `@dante/api-client` until real FastAPI OpenAPI exists.

## 14. GitHub-hosted frontend CI

Repository authority:

```text
.github/workflows/frontend-ci.yml
name: Frontend CI
runner: ubuntu-24.04
permissions: contents: read
```

Durable triggers after final materialization cleanup:

```text
pull_request -> main
push -> main
```

The temporary `push -> feature/frontend-materialization` bootstrap trigger was removed after a final successful hosted run on the FM-07 documentation closure.

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

External actions remain pinned to immutable full SHAs:

```text
actions/checkout v7.0.1
3d3c42e5aac5ba805825da76410c181273ba90b1

pnpm/setup v2.0.0
c9883cc79df532ad1a7b81bf9ab944ceb090d65c

actions/upload-artifact v7.0.1
043fb46d1a93c77aae656e7c1c64a875d1fc6a0a
```

Jobs / real context names:

```text
Quality
Web E2E
Mobile Bundle
Frontend CI Gate
```

Initial workflow proof:

```text
Frontend CI #3
commit        31deffddd35f69d48bee82465e0385e508c42876
overall       SUCCESS
Quality       PASS / 47s
Web E2E       PASS / 47s
Mobile Bundle PASS / 53s
```

Final FM-07 closure proof before temporary-trigger removal:

```text
commit        c1a77f249c716e0cb35159ecf2ad2c63b0bf4007
overall       SUCCESS
total         53s
Quality       PASS / 49s
Web E2E       PASS / 46s
Mobile Bundle PASS / 40s
Vitest        @dante/time 5 PASS + @dante/i18n 5 PASS
```

`Frontend CI Gate` later completed controlled green/red/recovery calibration on PR #28. The canonical protected-main ruleset definition contains `Backend CI Gate`, `Dependency Review` and `Frontend CI Gate`. The repository owner confirmed applying the frontend promotion; direct ruleset API readback is unavailable through the current connector, so that administrative setting is **OWNER-CONFIRMED APPLIED / DIRECT API READBACK UNAVAILABLE**.

PR #28 final head `a6607ceabd35f874dc9e5f63fe8f57f71a92bf80` directly passed Frontend Quality, Web E2E, Mobile Bundle and Frontend CI Gate, alongside Backend CI and Dependency Review, before merge to protected `main` as `f1aacb0724088e0b4b086008a5219c2fba5ce0cf`. The current connector cannot read push-triggered workflow runs for that merge SHA, so push-main CI remains **DIRECT READBACK UNAVAILABLE**.

## 15. Known workspace peer diagnostic

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

## 16. Clean-machine materialization evidence — FM-07 PASS

Final clean source:

```text
e79beadbddcf401d1d20c483c2d15d0b3cce96ad
```

Proved from a new HTTPS clone:

```text
no node_modules
clean initial Git state
.turbo ignored
Node 24.19.0
pnpm 11.22.0
new isolated pnpm store
pnpm install --frozen-lockfile PASS
lockfile unchanged
expo install --check PASS
known peer diagnostic reproduced exactly
new isolated Playwright Chromium headless-shell
Playwright Linux dependency bootstrap PASS
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

## 17. Troubleshooting discipline

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

## 18. Materialization closure and integrated continuation

Frontend materialization is **CLOSED / PASS**. The temporary live handoff has been deleted and the temporary feature-branch CI trigger has been removed; durable materialization knowledge now lives in this runbook and `docs/workstreams/frontend-materialization.md`.

At materialization closure, integration, required-check governance and protected-main merge were deliberately outside FM-00..FM-07. Those later integration steps are recorded in `docs/workstreams/frontend-materialization-integration.md` and repository-safety documentation rather than retroactively rewriting FM evidence.

Integration outcome:

```text
PR #28               MERGED
final PR head         a6607ceabd35f874dc9e5f63fe8f57f71a92bf80
protected-main merge  f1aacb0724088e0b4b086008a5219c2fba5ce0cf
merge parentage       PASS
merged tree identity  PASS
```

Current continuation is outside this workstation/materialization runbook:

```text
repository-security maturation -> CodeQL default setup evaluation under a fresh gate
backend next                   -> Concrete Logical -> PostgreSQL under a fresh workstream
product next                   -> first real vertical slice with capability-triggered activation
```

Still outside this runbook's materialization scope:

```text
product Access/Home implementation
PowerSync product integration
concrete backend business schema
remote deployment
CodeQL activation
```