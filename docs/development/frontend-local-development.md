# Frontend Local Development and Workstation Runbook

- Status: **CURRENT FOR `feature/frontend-materialization`**
- Purpose: reproducible frontend workstation setup, installation guidance, validation commands and LOCAL topology
- Foundation authority: Frontend Engineering Foundation integrated via PR #22
- Current execution state: **FM-06C REAL UNIT-TEST BASELINE PASS / FM-06 IN PROGRESS**

## 1. Core posture

DANTE uses one authoritative Git repository/history with working directories under WSL/Linux semantics. Purpose-specific linked Git worktrees inside WSL are allowed when backend/frontend or other bounded workstreams run concurrently.

```text
Windows 11
├── JetBrains / PyCharm UI
├── browser
├── Android Studio / emulator
└── Docker Desktop

WSL2 / Linux
├── linked DANTE Git worktree(s)
├── Node / pnpm / Turbo
├── Vite
├── Metro / Expo CLI
├── Python / uv where applicable
└── Docker CLI
```

Docker is for real stateful/local infrastructure, not a blanket wrapper around frontend development processes.

Normal LOCAL ownership:

```text
Git worktrees            WSL filesystem
Node/pnpm/Turbo          WSL
Vite                     WSL
Metro/Expo CLI           WSL
PyCharm/JetBrains UI     Windows using WSL project/tooling
browser                  Windows
Android Studio/emulator  Windows
Docker daemon            Docker Desktop / WSL integration
PostgreSQL               Docker when backend LOCAL infra is active
```

## 2. Filesystem and worktree invariant

Preferred paths:

```text
/home/<user>/projects/dante
/home/<user>/projects/dante-frontend
```

Observed topology:

```text
/home/mattia/projects/dante
feature/backend-scaffold

/home/mattia/projects/dante-frontend
feature/frontend-materialization
```

Hard rules:

```text
one authoritative Git repository/history
linked purpose-specific WSL worktrees allowed
no divergent Windows + WSL clones for active development
no shared cross-OS node_modules
no manual source copying between Windows and WSL trees
```

Avoid `/mnt/c/...` as the authoritative source/worktree unless concrete evidence requires it.

## 3. Python analogy for frontend dependency management

| Backend/Python | Frontend/TypeScript |
| --- | --- |
| Python runtime | Node runtime |
| `uv` | `pnpm` |
| `pyproject.toml` | `package.json` |
| `uv.lock` | `pnpm-lock.yaml` |
| `.venv` | project dependency graph exposed through `node_modules` |
| `uv sync` | `pnpm install` |

The analogy is useful but not exact. Node is a machine/WSL runtime selected by repository policy; project dependencies live in the pnpm-managed workspace graph.

## 4. Machine-level versus repository-managed tooling

Machine/WSL level:

- Git;
- fnm or equivalent accepted Node version manager;
- pnpm activation mechanism;
- Docker CLI integration;
- Android platform tooling on Windows.

Current repository-managed exact pins:

```text
Root engineering
TypeScript                    6.0.3
Turborepo                     2.10.11
ESLint                        10.8.1
@eslint/js                    10.0.1
typescript-eslint             8.67.0
Prettier                      3.9.0

Architecture enforcement
dependency-cruiser            18.2.0

Unit testing
Vitest                        4.1.11

Minimal Web
React                         19.2.8
React DOM                     19.2.8
Vite                          8.2.1
@vitejs/plugin-react          6.1.0
@tanstack/react-router        1.170.31
@tanstack/router-plugin       1.168.34
@types/node                   24.13.3
@types/react                  19.2.18
@types/react-dom              19.2.4

Minimal Mobile
Expo                          57.0.9
React Native                  0.86.2
React                         19.2.3
Expo Router                   57.0.9
Gesture Handler               2.32.0
Reanimated                    4.5.1
Safe Area Context             5.7.0
Screens                       4.26.2
Worklets                      0.10.1

Shared design tokens
@terrazzo/cli                 2.7.1
@terrazzo/parser              2.7.1
@terrazzo/plugin-css          2.7.1

Shared i18n
i18next                       26.3.6
react-i18next                 17.0.11

Shared time
temporal-polyfill             1.0.4
```

FM-06B adds no package dependency: generated-source drift uses the existing Terrazzo and TanStack Router Vite generation paths through `tooling/check-generated.mjs`.

FM-06C adds only the real unit-test runner at root. No DOM environment, React Testing Library, React Native test renderer or coverage package is installed yet.

Future dependencies activate only when real consumers require them, including additional TanStack libraries, Zod, Playwright/E2E tooling, PowerSync/native SQLite integrations and release tooling.

Do not install project libraries globally for convenience:

```text
npm install -g vite
npm install -g typescript
npm install -g expo
sudo npm ...
```

unless a future tool explicitly requires a documented global exception.

## 5. Current repository authorities

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
```

Web:

```text
apps/web/package.json
apps/web/index.html
apps/web/tsconfig.json
apps/web/vite.config.ts
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
apps/mobile/.gitignore
apps/mobile/src/bootstrap/i18n.ts
```

Design tokens:

```text
packages/design-tokens/package.json
packages/design-tokens/tsconfig.json
packages/design-tokens/terrazzo.config.ts
packages/design-tokens/tokens/primitives.json
packages/design-tokens/tokens/semantic.json
packages/design-tokens/tooling/native-plugin.ts
packages/design-tokens/generated/web.css
packages/design-tokens/generated/native.ts
```

`tokens/*.json` is semantic authority. `generated/*` is committed deterministic output and must not be hand-edited.

Shared i18n:

```text
packages/i18n/package.json
packages/i18n/tsconfig.json
packages/i18n/src/index.ts
packages/i18n/src/index.test.ts
packages/i18n/src/resources/it/common.ts
packages/i18n/src/resources/en/common.ts
```

Shared time:

```text
packages/time/package.json
packages/time/tsconfig.json
packages/time/src/index.ts
packages/time/src/index.test.ts
```

The shared time core is platform-neutral and does not own device/user timezone detection, timezone persistence, presentation formatting, reminders or product scheduling policy.

## 6. Docker boundary

Use Docker where it gives reproducible stateful service semantics.

Expected examples when activated:

```text
PostgreSQL
PowerSync service
other real stateful LOCAL dependencies
```

Normal frontend servers stay direct in WSL:

```text
Vite
Metro / Expo CLI
```

Container lifecycle and persistent data lifecycle are separate. Stateful services use explicit persistent storage/volumes when required.

## 7. Browser and Mobile networking

### Web — directly validated

Observed path:

```text
Vite 8.2.1 in WSL
http://localhost:5173/
↓
Windows localhost forwarding
↓
Firefox on Windows
↓
DANTE Web diagnostic route /
```

Start:

```bash
cd ~/projects/dante-frontend
pnpm --filter @dante/web dev
```

No `--host`, manual proxy, Windows Node process, alternate clone or custom bridge was required on the observed workstation. Do not add one pre-emptively.

### Mobile — directly validated

Observed path:

```text
Metro / Expo CLI in WSL
exp://127.0.0.1:8081
↓
Windows ADB platform-tools via WSL interoperability
adb reverse tcp:8081 tcp:8081
↓
Windows Android emulator
Expo Go 57.0.9
↓
DANTE Mobile diagnostic route /
```

Start Metro:

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

Verify reverse mapping:

```bash
powershell.exe -NoProfile -Command '& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" reverse --list'
```

Launch local Expo URL when needed:

```bash
powershell.exe -NoProfile -Command '& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" shell am start -a android.intent.action.VIEW -d "exp://127.0.0.1:8081"'
```

Diagnose failures in order:

```text
ADB device
-> reverse mapping
-> Metro
-> manifest
-> bundle
-> Expo Go/client runtime
```

Do not introduce tunnels, Metro overrides, hoisting, Windows Node, a second clone or project `updates.url` merely because the emulator cannot initially render.

Direct FM-04 evidence included manifest HTTP 200, Hermes bundle HTTP 200 / 9,162,793 bytes, Expo Go reaching Metro, JS execution and visible DANTE render.

### FM-05A Metro workspace-package resolution

The first `@dante/design-tokens/native` bare import failed even though:

```text
workspace symlink exists
Node resolves the package subpath
Metro watchFolders already include the workspace package
app/root node_modules paths are present
package exports support is enabled
TypeScript source extension is enabled
```

A `--clear` restart did not repair the issue. A temporary relative import into the generated TS file rendered successfully, proving external workspace TS visibility/execution.

Durable public surface:

```json
{
  ".": {
    "react-native": "./generated/native.ts",
    "default": "./generated/native.ts"
  },
  "./native": "./generated/native.ts",
  "./web.css": "./generated/web.css"
}
```

After restoring the real bare import, Android rendered successfully. No custom `metro.config.js`, pnpm hoist/linker change or Windows Node path is accepted as part of the baseline.

## 8. Normal command policy

Root repository commands:

```text
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
pnpm build
```

Current real root graph:

```text
typecheck
@dante/design-tokens
@dante/i18n
@dante/time
@dante/web
@dante/mobile

build
@dante/design-tokens -> @dante/web

test
@dante/i18n
@dante/time
```

Use project-local execution through pnpm rather than unrelated global binaries.

## 9. Architecture enforcement

`pnpm architecture:check` is backed by `dependency-cruiser.config.mjs` and validates DANTE-owned source rather than recursively validating third-party package internals.

Currently enforced real rules:

```text
unresolvable production source imports forbidden
source cycles forbidden
Web -> Mobile forbidden
Mobile -> Web forbidden
shared packages -> apps forbidden
production frontend -> prototypes forbidden
shared cores -> React / React DOM / React Native / react-i18next / Expo / Vite forbidden
```

After FM-06C test files were added, the current graph directly passed:

```text
36 modules
45 dependencies cruised
0 enforced violations
```

Dependency-cruiser troubleshooting:

- if a rule itself is rejected as unsafe, fix the rule; do not interpret it as an application architecture violation;
- `doNotFollow.path = 'node_modules'` prevents package-local third-party trees from becoming initial roots while retaining external dependency boundary edges;
- do not add package-name exceptions, hoisting or resolver weakening merely to get green output.

Feature-to-feature, route-to-feature and future `ui/`/`platform/` rules remain NOT RUN until those structures exist.

## 10. Generated-source drift enforcement

`pnpm generated:check` is backed by `tooling/check-generated.mjs`.

Checked authorities:

```text
packages/design-tokens/generated/web.css
packages/design-tokens/generated/native.ts
apps/web/src/routeTree.gen.ts
```

Behavior:

```text
snapshot current generated bytes
run real generators
compare byte-for-byte
report exact drifted paths
restore pre-check bytes in all cases
clean/current -> exit 0
drift -> non-zero
```

Generation owners:

```text
DTCG token source -> Terrazzo 2.7.1 -> Web CSS / Native TS
Web route source -> TanStack Router Vite plugin -> routeTree.gen.ts
```

Do not hand-edit generated output to make the gate green. Change owning source, regenerate through the real generator, review output and rerun the gate.

Do not add `@tanstack/router-cli`: the supported Vite plugin already owns route generation in this repository.

## 11. Real unit-test baseline — FM-06C PASS

Implementation:

```text
610e33a7a31987d97564b1d6004a7b9896acaedc
test: establish shared frontend unit baseline
```

Runner:

```text
Vitest 4.1.11
root exact devDependency
```

Package scripts:

```text
@dante/i18n  vitest run
@dante/time  vitest run
```

Root authority:

```bash
pnpm test
```

which executes `turbo run test` and currently runs the two real package suites.

Direct evidence:

```text
@dante/time                      5 tests PASS
@dante/i18n                      5 tests PASS
root Turbo                       2 successful / 2 total
non-zero real test count         PASS
5-package strict typecheck       PASS
architecture                     36 modules / 45 deps / 0 violations
pnpm generated:check             PASS
lint / format                    PASS
Web production build             PASS
frozen install                   PASS
git diff --check                 PASS
7 implementation paths           PASS
0 unexpected paths               PASS
remote readback                  PASS
```

### Time test semantics

The initial suite asserts real shared-core behavior:

```text
Temporal primitive parsing
Europe/Rome DST spring transition
Instant <-> ZonedDateTime round trip
PlainDateTime + Duration arithmetic
ZonedDateTime instant preservation
```

### i18n test semantics

The initial suite asserts:

```text
supported locales = it/en
default locale = it
fallback locale = it
default namespace = common
Italian runtime
English runtime
unsupported locale -> Italian fallback
IT/EN resource leaf-shape parity
strict selector namespace contract
```

With `enableSelector: 'strict'`, the accepted test selector shape includes the explicit namespace:

```text
$.common.runtime...
$.common.gesture...
```

Do not weaken the production i18n contract or TypeScript config to accommodate a test that omits the required namespace.

### FM-06C diagnostics

Root-test output parser:

```text
package tests PASS
Turbo 2/2 PASS
post-run parser initially failed on colored/prefixed output
```

Repair: disable/strip ANSI and assert both package task labels, Turbo 2/2 and non-zero test counts.

Pre-existing peer warning:

```text
pnpm peers check
react-dom@19.2.8 wants react ^19.2.8
Mobile direct React = 19.2.3
```

Read-only comparison proved this association already existed at FM-06C PRE-SCOPE, and FM-06C did not change the Web/Mobile lockfile importer blocks.

Classification:

```text
KNOWN PRE-EXISTING WORKSPACE PEER WARNING
NOT introduced by Vitest
NOT a failing unit assertion
```

Do not move Mobile React away from the directly runtime-validated Expo/RN baseline or downgrade the correctly paired Web React/ReactDOM baseline merely to silence the workspace-wide peer diagnostic. Re-evaluate it during FM-07 clean materialization closure if still observable.

Strict-selector repair:

```text
runtime tests initially PASS
TypeScript rejected $.runtime / $.gesture
repair -> $.common.runtime / $.common.gesture
```

This strengthened the test; no production resource/fallback policy was changed.

## 12. Selected historical checkpoints

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
```

## 13. Shared design-token workflow

Normal commands:

```bash
pnpm --filter @dante/design-tokens tokens:lint
pnpm --filter @dante/design-tokens generate
pnpm generated:check
```

Current generated outputs are committed and consumed by Web/Mobile. The initial shared semantics intentionally cover only already-real duplicated radii; diagnostic colors/typography are not promoted into canonical brand semantics without a real design authority decision.

## 14. Shared i18n workflow

Current locale policy:

```text
Italian  (it)  PRIMARY / DEFAULT / FALLBACK
English  (en)  SUPPORTED SECONDARY
other locales  NOT YET SUPPORTED
```

Core is framework-free. React integration stays in app bootstraps. Core catalogs are bundled locally. New namespaces appear only with real feature consumers; do not add empty placeholder catalogs.

Source-first package internals use extensionless imports. Do not broaden consumer `tsconfig` or add a duplicate package build merely to satisfy an unrelated native-Node-only resolution probe.

## 15. Shared time workflow

Accepted semantic vocabulary:

```text
Instant
PlainDate
PlainTime
PlainDateTime
ZonedDateTime
Duration
```

Do not use JavaScript `Date` as a universal DANTE semantic. Locale is not timezone.

Current public primitives include Temporal, parse helpers and Instant/ZonedDateTime conversion helpers. Product scheduling, reminders, timezone selection/persistence and presentation formatting remain outside this shared core.

## 16. Clean-machine/onboarding acceptance target

A future developer should be able to reach the accepted base without chat context:

```text
clone or create linked WSL worktree
-> install documented machine prerequisites
-> install/activate fnm
-> select governed Node runtime
-> activate governed pnpm
-> pnpm install --frozen-lockfile
-> pnpm lint
-> pnpm format:check
-> pnpm typecheck
-> pnpm architecture:check
-> pnpm generated:check
-> pnpm test
-> pnpm build
-> start Web
-> open Web from Windows browser
-> start Mobile in WSL
-> establish ADB reverse
-> launch on Windows Android emulator
-> diagnose failures from documented ownership boundaries
```

The runtime/root-tooling/Web/minimal-Mobile/shared packages, current dependency architecture, generated-source drift and real unit-test baseline are directly proven. The full materialization target is not PASS until FM-06D/FM-06E and FM-07 obligations are directly exercised.

## 17. Troubleshooting discipline

For any failure:

```text
capture exact command
capture full output
identify owning layer
change one variable
rerun the smallest relevant validation
record durable fix if project-specific
```

Do not respond to failures with random global installs, blanket cache deletion, force flags or broad version changes.

Ownership examples:

```text
Node executable/version        workstation runtime
pnpm resolution/lockfile       workspace/package layer
TypeScript                     package/root type contract
ESLint / Prettier              root engineering tooling
dependency-cruiser             dependency architecture
tooling/check-generated.mjs    generated-source drift
Vitest                         unit-test runner
Turbo test                     workspace test orchestration
i18next strict selector        @dante/i18n type contract
Vite build                     Web toolchain
Vite localhost                 WSL <-> Windows Web adapter
Metro resolution               Mobile toolchain
ADB/emulator                   WSL <-> Windows Mobile adapter
PowerSync/SQLite               Mobile sync platform boundary
PostgreSQL                     Docker/backend LOCAL infra
```

## 18. Current next action

Proceed to **FM-06D Web E2E + Mobile bundle smoke** with read-only discovery first.

FM-06A, FM-06B and FM-06C are directly validated and closed at their stated scopes. FM-06D should:

```text
Web
reverify current supported Playwright line
select a smallest meaningful browser E2E assertion against the existing diagnostic route
establish local browser installation/cache ownership suitable for future CI

Mobile
inspect the actual Expo SDK 57 supported deterministic headless bundle/export path
materialize a bundle smoke without requiring interactive emulator UI for every run
retain the already-proven Android emulator runtime as stronger direct runtime evidence
```

Do not mix GitHub Actions, product Access/Home UI, PowerSync, coverage thresholds or backend contracts into FM-06D.
