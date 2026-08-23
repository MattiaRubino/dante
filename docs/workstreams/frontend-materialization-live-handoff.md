# DANTE Frontend Materialization — LIVE HANDOFF

> TEMPORARY / DISPOSABLE SAVE-GAME.
>
> Purpose: make the frontend workstream resumable if the current chat dies.
> Keep this file updated after every substantive slice/gate.
> Delete it only when the frontend-materialization workstream is fully closed and the durable docs contain everything needed.

## 0. Resume protocol for a new chat

Read this file completely, then read:

1. `docs/workstreams/frontend-materialization.md`
2. `docs/development/frontend-local-development.md`
3. `docs/decisions/ADR-008-frontend-engineering-stack.md`
4. `docs/decisions/ADR-009-frontend-architecture-boundaries.md`
5. the Frontend Engineering Foundation authorities referenced by the workstream.

Do not restart discovery from memory and do not redesign accepted decisions unless new evidence contradicts them.

Before any write:

```bash
git fetch origin feature/frontend-materialization
git rev-parse HEAD
git rev-parse origin/feature/frontend-materialization
git status --short
```

The documentation-closure commit containing this file is self-referential and cannot embed its own Git SHA without another commit. Resolve the current documentation HEAD from `origin/feature/frontend-materialization`. The last directly validated implementation SHA is recorded below.

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
Git / Node / pnpm / Turbo / Vite / Metro / Expo CLI

Windows
Firefox/browser / Android Studio / Android emulator / ADB / JetBrains UI
```

Hard invariant:

```text
ONE authoritative Git history
WSL-backed source/worktrees
NO independent divergent Windows clone
NO cross-OS shared node_modules
NO merge/rebase of main into this branch unless separately scoped
```

## 2. Current checkpoint

Last directly validated implementation commit:

```text
610e33a7a31987d97564b1d6004a7b9896acaedc
test: establish shared frontend unit baseline
```

Current state:

```text
FM-06A DEPENDENCY ARCHITECTURE ENFORCEMENT — PASS
FM-06B GENERATED-SOURCE DRIFT ENFORCEMENT — PASS
FM-06C REAL UNIT-TEST BASELINE — PASS
FM-06 IN PROGRESS
NEXT = FM-06D WEB E2E + MOBILE BUNDLE SMOKE
```

## 3. Completed materialization checkpoints

```text
FM-00 workstation preflight                         PASS
FM-01 fnm/Node/pnpm WSL runtime                     PASS
FM-02A root workspace                               PASS
FM-02B root engineering tooling                     PASS
FM-03 minimal Web + Windows Firefox runtime         PASS
FM-04 minimal Mobile + Android/Metro/Hermes runtime PASS
FM-05A shared design tokens                         PASS
FM-05B shared i18n                                  PASS
FM-05C shared time                                  PASS
FM-06A dependency architecture                      PASS
FM-06B generated-source drift                       PASS
FM-06C real unit-test baseline                      PASS
```

Key implementation commits:

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

## 4. Accepted frontend baseline

```text
Node                        24.19.0
pnpm                        11.22.0
TypeScript                  6.0.3
Turborepo                   2.10.11
ESLint                      10.8.1
Prettier                    3.9.0
dependency-cruiser          18.2.0
Vitest                      4.1.11

Web React                   19.2.8
React DOM                   19.2.8
Vite                        8.2.1
TanStack React Router       1.170.31
TanStack Router plugin      1.168.34

Mobile Expo                 57.0.9
React Native                0.86.2
Mobile React                19.2.3
Expo Router                 57.0.9
Gesture Handler             2.32.0
Reanimated                  4.5.1
Safe Area Context           5.7.0
Screens                     4.26.2
Worklets                    0.10.1

Terrazzo                    2.7.1
i18next                     26.3.6
react-i18next               17.0.11
temporal-polyfill           1.0.4
```

## 5. Shared authorities

```text
visible copy / labels / messages / a11y
-> @dante/i18n

colors / radii / spacing / typography / shadows / theme semantics
-> @dante/design-tokens

platform component presentation / interaction states
-> Web/Mobile design-system implementation

assets / logos / illustrations / backgrounds
-> versioned asset authority

workflow / click behavior / feature decisions
-> owning feature logic
```

Do not create one universal dictionary containing unrelated concerns.

Current genuine shared packages:

```text
@dante/design-tokens
@dante/i18n
@dante/time
```

Do not create `@dante/api-client` until real FastAPI OpenAPI exists. Do not create broad shared feature packages before real cross-platform reuse exists.

## 6. Runtime sequences already proven

Web:

```bash
cd ~/projects/dante-frontend
pnpm --filter @dante/web dev
```

Windows browser:

```text
http://localhost:5173/
```

Mobile:

```bash
cd ~/projects/dante-frontend/apps/mobile
pnpm exec expo start --localhost
```

ADB reverse from WSL:

```bash
powershell.exe -NoProfile -Command '& "$env:LOCALAPPDATA\\Android\\Sdk\\platform-tools\\adb.exe" reverse tcp:8081 tcp:8081'
```

Launch through Expo Go:

```text
exp://127.0.0.1:8081
```

Do not introduce tunnel/hoisting/Metro config/Windows Node without concrete contradictory evidence.

## 7. Executable engineering gates now real

```text
pnpm typecheck
pnpm lint
pnpm format:check
pnpm architecture:check
pnpm generated:check
pnpm test
pnpm build
pnpm install --frozen-lockfile
```

FM-06A current architecture graph after FM-06C tests:

```text
36 modules
45 dependencies cruised
0 enforced violations
```

Currently enforced dependency rules include:

```text
unresolvable production source forbidden
source cycles forbidden
Web -> Mobile forbidden
Mobile -> Web forbidden
shared packages -> apps forbidden
production frontend -> prototypes forbidden
shared core -> React/React DOM/RN/react-i18next/Expo/Vite forbidden
```

Feature/ui/platform-specific rules remain NOT RUN until those structures really exist.

FM-06B generated drift authorities:

```text
packages/design-tokens/generated/web.css
packages/design-tokens/generated/native.ts
apps/web/src/routeTree.gen.ts
```

The checker snapshots bytes, runs the real Terrazzo and TanStack Router Vite generation paths, compares byte-for-byte, reports exact drift and restores pre-check bytes in all cases.

## 8. LAST CLOSED SLICE — FM-06C

Final state:

```text
PASS
COMMITTED
PUSHED
REMOTE READBACK PASS
```

Implementation:

```text
610e33a7a31987d97564b1d6004a7b9896acaedc
test: establish shared frontend unit baseline
```

Exact implementation gate:

```text
BRANCH
feature/frontend-materialization

PRE-SCOPE
ae0ff9e9849ff3aedcd095a645750993297c4384

CREATE
packages/time/src/index.test.ts
packages/i18n/src/index.test.ts

UPDATE
package.json
pnpm-lock.yaml
packages/time/package.json
packages/i18n/package.json
docs/workstreams/frontend-materialization-live-handoff.md

DELETE
none
```

Runner:

```text
Vitest 4.1.11
exact root devDependency pin
```

Real unit baseline:

```text
@dante/time    5 tests PASS
@dante/i18n    5 tests PASS
root Turbo     2 successful / 2 total
```

`@dante/time` coverage:

```text
Temporal primitive parsing
Europe/Rome DST spring transition
Instant <-> ZonedDateTime round trip
PlainDateTime + Duration arithmetic
ZonedDateTime instant preservation
```

`@dante/i18n` coverage:

```text
supported locale/default/fallback contract
Italian runtime
English runtime
unsupported locale -> Italian fallback
IT/EN resource leaf-shape parity
strict selectors with explicit common namespace
```

Regression evidence:

```text
5-package strict typecheck PASS
architecture:check PASS — 36 modules / 45 dependencies / 0 violations
generated:check PASS
lint PASS
format PASS
Web production build PASS
frozen install PASS
git diff --check PASS
7 authorized implementation paths / 0 unexpected
remote readback PASS
```

## 9. Historical diagnostics that must not be rediscovered blindly

### FM-05A Metro package resolution

Bare `@dante/design-tokens/native` initially failed even though workspace visibility and Node resolution were correct. `--clear` did not fix it. A temporary relative import proved Metro could execute the external TS file. Durable fix: root `"."` export with `react-native`/`default`; no Metro override or hoisting.

### FM-05B source-first TypeScript

Explicit `.ts` internal imports caused TS5097 in consumers. Durable fix: extensionless package-internal imports. Plain Node ESM strip-types was rejected as a non-representative probe; Vite SSR is the valid Web bundler-resolution probe.

### FM-06A dependency-cruiser

```text
attempt 1: unsafe combined regex -> split into atomic safe patterns
attempt 2: package-local node_modules gathered as roots -> doNotFollow.path = node_modules
```

Neither was a DANTE architecture violation.

### FM-06B generated checker

```text
implicit process/console globals -> root ESLint rejected
repair -> explicit node:process + stdout/stderr
textual repair failed to remove every console.* -> rewrite checker deterministically
```

No repository-wide ESLint global exception was added.

### FM-06C diagnostics

Attempt 1:

```text
package tests PASS
root Turbo 2/2 PASS
post-run evidence parser failed to recognize colored/prefixed output
```

Repair: disable color, strip residual ANSI, assert both package task labels, Turbo 2/2 and non-zero test counts.

Peer diagnostic:

```text
pnpm peers check reports react-dom@19.2.8 wanting react ^19.2.8 while Mobile direct React is 19.2.3
```

Read-only comparison proved the association already existed at the FM-06C PRE-SCOPE and FM-06C did not change Web/Mobile lockfile importer blocks. Classification: **KNOWN PRE-EXISTING WORKSPACE PEER WARNING**, not introduced by Vitest. Do not change the already runtime-validated Expo/RN React baseline merely to silence it. Re-evaluate during FM-07 clean materialization closure if still observable.

Strict-selector diagnostic:

```text
runtime tests initially passed
strict TypeScript rejected $.runtime / $.gesture selectors
repair -> $.common.runtime / $.common.gesture
```

This strengthened the tests to exercise the accepted `enableSelector: 'strict'` namespace contract; no production i18n policy was weakened.

## 10. Write / QA governance

Before repository writes use an exact gate:

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

Immediately before first branch-visible write, re-read remote HEAD and require it to equal PRE-SCOPE. No silent scope expansion.

After writes:

```text
validate exact changed paths
zero unexpected paths
run applicable real QA
remote readback after push
```

Evidence rule:

```text
selected != installed
installed != configured
configured != directly validated
scenario PASS != whole-system PASS
```

Never convert NOT RUN to PASS without direct evidence. No direct work on `main`. No casual force push.

## 11. CURRENT SLICE — FM-06D

Status:

```text
WEB E2E + MOBILE BUNDLE-SMOKE QA PASS
COMMIT + PUSH ABOUT TO RUN
```

Objective:

```text
establish a real Web E2E baseline and a deterministic Mobile bundle smoke
without mixing CI orchestration or product UI into the slice
```

Approved FM-06D gate:

```text
BRANCH
feature/frontend-materialization

PRE-SCOPE
15a0fabfe7c0583a2350e4f213559723beddc967

CREATE
apps/web/playwright.config.ts
apps/web/e2e/runtime.spec.ts
tooling/check-mobile-bundle.mjs

UPDATE
.gitignore
package.json
pnpm-lock.yaml
apps/web/package.json
apps/web/tsconfig.json
docs/workstreams/frontend-materialization-live-handoff.md

DELETE
none
```

Materialization-time technology revalidation:

```text
@playwright/test 1.62.1 exact app-local devDependency
Chromium only for the first automated browser baseline
Expo SDK 57 `expo export --platform android`
Hermes bytecode left enabled
```

Root commands:

```text
pnpm test:e2e:web
pnpm mobile:bundle:check
```

No interactive Firefox or Android emulator rerun is required by this slice.


Expected discovery questions:

```text
Web
- reverify current stable Playwright line and Node/Vite compatibility
- define smallest real browser assertion against existing diagnostic route
- decide browser install/cache ownership for local + future CI

Mobile
- inspect the supported Expo SDK 57 headless export/bundle path
- prefer a deterministic bundle/export smoke over requiring emulator UI for every test run
- preserve the already-proven Android emulator runtime evidence as stronger direct runtime proof
```

Do not select commands from memory; inspect the current Expo/Metro and Playwright primary documentation and actual repository scripts first.

Direct FM-06D evidence:

```text
@playwright/test 1.62.1 registry revalidation PASS
Playwright Chromium browser installation PASS
Playwright Chromium Linux system dependencies PASS
Chromium headless process launch PASS
Web production Vite build launched by Playwright webServer PASS
Vite preview 127.0.0.1:4173 PASS
Chromium route / E2E PASS
1 real Web E2E test PASS
Italian runtime heading + eyebrow PASS
route/purpose definition-list semantics PASS
Temporal Europe/Rome runtime value PASS

Expo SDK 57 Android production export PASS
Hermes .hbc bundle present PASS
Hermes .hbc non-empty PASS
temporary export outside repository PASS
temporary export cleanup PASS

root pnpm test PASS
5-package typecheck PASS
architecture:check PASS
generated:check PASS
lint PASS
format PASS
Web build PASS
frozen install PASS
git diff --check PASS
```

Evidence classification:

```text
Web E2E = real automated Chromium execution against Vite production preview
Mobile bundle smoke = deterministic headless Metro/Expo production bundling proof
Mobile bundle smoke != APK/AAB build
Mobile bundle smoke != device runtime
previous Android emulator/Hermes runtime PASS remains stronger direct runtime evidence
```

FM-06D explicitly does NOT include:

```text
GitHub Actions / required checks
product Access/Home UI
PowerSync
backend contracts
coverage thresholds
main synchronization
```

## 11A. FM-06D attempt-1 Playwright host dependency diagnostic

The first FM-06D Web E2E run reached:

```text
Playwright 1.62.1 installed
Chromium browser binaries installed
Vite production build PASS
Vite preview reachable at 127.0.0.1:4173
```

Chromium itself then failed before a browser page could start:

```text
chrome-headless-shell: error while loading shared libraries:
libnspr4.so: cannot open shared object file
```

Classification:

```text
DANTE Web build PASS
Playwright browser download PASS
browser process launch FAIL
owning layer = WSL/Linux browser system dependencies
NOT a Web application failure
NOT a Playwright test assertion failure
```

This differs from the historical optional React Native DevTools `libnspr4.so`
warning: FM-04 application runtime did not require that helper, so installing
host packages was not justified there. FM-06D now has a real Chromium process
whose execution directly requires the missing Linux browser dependency.

Accepted repair uses Playwright's supported dependency installer for the
single selected browser:

```text
playwright install-deps chromium
```

Do not add browser shared libraries to the repository dependency graph and do
not change the Web application to work around a workstation-level ELF
dependency.

## 11B. FM-06D attempt-2 Web E2E assertion diagnostic

After Playwright's Chromium Linux dependencies were installed:

```text
libnspr4.so visible PASS
Chromium process launch PASS
Vite production build PASS
Vite preview PASS
browser reached the real DANTE route
heading `Frontend pronto` PASS
eyebrow `DANTE Web` PASS
```

The E2E then failed only on:

```text
getByText('Scaffold diagnostico FM-03', { exact: true })
```

The real DOM renders the purpose and Temporal probe in the same semantic
`<dd>`:

```text
Scaffold diagnostico FM-03
2026-08-22T20:00:00+02:00[Europe/Rome]
```

With Playwright `exact: true`, the containing element's normalized full text
is not exactly the purpose substring. This is a test-locator mismatch, not
missing application copy.

Accepted repair:

```text
anchor the assertion to the visible `Scopo` definition-list row
assert that row contains the expected FM-03 purpose
assert that row contains the exact Temporal code value
```

This preserves the real user-visible contract and is stronger than weakening
the application or replacing the assertion with an unrelated implementation
selector.

The `NO_COLOR`/`FORCE_COLOR` warning seen in the failed run is non-blocking
runner output noise. The resume does not set `NO_COLOR`; output validation
already strips ANSI sequences when needed.

## 12. Future queued work

```text
FM-06D Web E2E + Mobile bundle smoke        NEXT
FM-06E CI orchestration                     NOT RUN
FM-07 clean materialization baseline        NOT RUN
```

Only after FM-06/FM-07 provide the accepted infrastructure baseline should production Access rely on it.

## 13. Still NOT RUN / deferred

```text
hoisted pnpm fallback                         NOT RUN / not needed
feature-specific architecture rules           NOT RUN
Web E2E                                       NOT RUN — NEXT FM-06D
Mobile bundle smoke                           NOT RUN — NEXT FM-06D
GitHub Actions frontend CI                    NOT RUN
TanStack Form + Zod real form                 NOT RUN
TanStack Query first remote path              NOT RUN
OpenAPI -> Orval                              NOT RUN
PowerSync / OP-SQLite / SQLCipher             NOT RUN
offline reconciliation                        NOT RUN
identity-scoped local DB lifecycle             NOT RUN
versioned Web runtime config                   NOT RUN
Cloudflare deployment                         NOT RUN
Sentry                                         NOT RUN
EAS release path                              NOT RUN
iOS runtime/release                            NOT RUN
```

Preserve these as NOT RUN until their real scope activates.
