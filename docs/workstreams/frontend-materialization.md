# Workstream — Frontend Materialization

- Status: **ACTIVE — FM-06D WEB E2E + MOBILE BUNDLE SMOKE PASS / FM-06 IN PROGRESS**
- Branch: `feature/frontend-materialization`
- Opening base: `ff46eb16b971b1fde96eef9047b09faa02e1a5db`
- Current validated implementation commit: `d6138f5f5049e8fc11f877b774ff0191af44069f`
- Frontend Engineering Foundation: **CLOSED / ACCEPTED / FINAL REVIEW PASS / integrated via PR #22**
- Product-surface implementation: **NOT AUTHORIZED BY THIS CHECKPOINT**

## 1. Purpose

Materialize the accepted DANTE frontend engineering foundation into a real, reproducible Web/Mobile workspace and directly validate each platform/tooling boundary before product features depend on it.

Evidence discipline remains:

```text
selected != installed
installed != configured
configured != directly validated
scenario PASS != whole-system PASS
```

Version-sensitive tooling is reverified immediately before materialization. `NOT RUN` is never silently promoted to `PASS`.

## 2. Developer topology

```text
Windows 11
├── JetBrains / PyCharm UI
├── browser
├── Android Studio / emulator
└── Docker Desktop

WSL2 / Linux
├── authoritative frontend Git worktree
├── Git / Node / pnpm / Turbo
├── Vite
├── Metro / Expo CLI
└── Docker CLI
```

Hard invariant:

```text
ONE authoritative Git history
WSL-backed source/worktrees
NO divergent Windows + WSL clones
NO cross-OS shared node_modules
```

Observed frontend worktree:

```text
/home/mattia/projects/dante-frontend
feature/frontend-materialization
```

Detailed developer authority: `../development/frontend-local-development.md`.

## 3. Materialized baseline

### FM-00 — workstation preflight — PASS

```text
Ubuntu 24.04.4 LTS / WSL2
Git 2.43.0
Docker CLI 29.7.2
Docker Compose 5.4.0
```

### FM-01 — runtime/package manager — PASS

```text
fnm   1.39.0
Node  24.19.0
npm   11.17.0
pnpm  11.22.0
```

### FM-02 — root workspace/tooling — PASS

```text
TypeScript          6.0.3
Turborepo           2.10.11
ESLint              10.8.1
@eslint/js           10.0.1
typescript-eslint   8.67.0
Prettier            3.9.0
```

Selected checkpoints:

```text
FM-02A c3f7945da7137b2bdd9e9f8922af452f1a79770f
FM-02B 7ad88e2fbba1e8140149be05f9a3fe3005ad0488
```

### FM-03 — minimal Web — PASS

```text
React                     19.2.8
React DOM                 19.2.8
Vite                      8.2.1
@vitejs/plugin-react      6.1.0
@tanstack/react-router    1.170.31
@tanstack/router-plugin   1.168.34
```

Checkpoint:

```text
1568d90091064162da9a438f3555675f1921c226
build: lock minimal web runtime
```

Direct Windows Firefox <- WSL Vite runtime PASS.

### FM-04 — minimal Mobile — PASS

```text
Expo                         57.0.9
React Native                 0.86.2
React                        19.2.3
Expo Router                  57.0.9
Gesture Handler              2.32.0
Reanimated                   4.5.1
Safe Area Context            5.7.0
Screens                      4.26.2
Worklets                     0.10.1
```

Implementation:

```text
3c150c4806191f0347b64c645d53168123ce0ede
build: lock minimal mobile runtime
```

Direct Android evidence:

```text
Windows Android emulator                    PASS
ADB reverse tcp:8081 tcp:8081               PASS
Metro / Expo CLI in WSL                     PASS
Android Expo manifest                       HTTP 200
Android Hermes bundle                       HTTP 200 / 9,162,793 bytes
Expo Go 57.0.9                              PASS
DANTE route / render                        PASS
Gesture Handler/Reanimated probe            PASS
expo-doctor                                 21/21 PASS
```

Expo Go warnings and the historical optional React Native DevTools `libnspr4.so` warning were non-blocking for FM-04 and did not justify project configuration changes.

## 4. FM-05 — genuine shared packages — COMPLETE

### FM-05A — `@dante/design-tokens` — PASS

```text
implementation  acd846a06614270fda9d66542a3fdc87fca7202e
closure         d4d99b157bab9e00c4f0285bf82745e73a9c944d
Terrazzo        2.7.1
DTCG            2025.10
```

Initial real shared semantics are deliberately narrow: duplicated card/panel radii only. Generated Web CSS and Native TypeScript are committed deterministic output.

Metro package-resolution diagnosis retained: bare subpath initially failed despite valid workspace visibility; a temporary relative-import probe proved external TS execution; durable repair was the root `"."` package export. No Metro override, hoisting or Windows Node runtime was introduced.

### FM-05B — `@dante/i18n` — PASS

```text
implementation  5e5fae5d696a5da6b457e3198b70f642245ec323
closure         098be4c815eb724c32f49c277b058e85df81e03a
i18next         26.3.6
react-i18next   17.0.11
```

```text
Italian  (it) PRIMARY / DEFAULT / FALLBACK
English  (en) SUPPORTED SECONDARY
```

Shared core owns locale/resources/fallback/types; app bootstraps own React integration. Strict selectors are enabled. Direct Web + Android Italian runtime PASS; English runtime switch PASS.

Source-first diagnosis retained: explicit `.ts` internal imports caused TS5097; extensionless internal imports are the accepted repair. Native Node strip-types is not the Vite/Metro consumer contract.

### FM-05C — `@dante/time` — PASS

```text
implementation  aeb43e9e5ed7add42464e61f5c02acd6a53fed85
closure         61d19795867e13818a2d43252906b565d23e96e5
temporal-polyfill 1.0.4
```

Semantic vocabulary:

```text
Instant
PlainDate
PlainTime
PlainDateTime
ZonedDateTime
Duration
```

Do not use JavaScript `Date` as a universal DANTE time semantic. Locale and timezone remain separate concerns. Web + Android/Hermes runtime and Europe/Rome DST behavior were directly validated.

## 5. FM-06 — enforcement/test/runtime-smoke materialization — IN PROGRESS

### FM-06A — dependency architecture + cycle enforcement — PASS

```text
38dbbd3efb764a8419f4498d27a2e29a3602fc5d
build: enforce frontend dependency architecture

dependency-cruiser 18.2.0
pnpm architecture:check
```

Rules currently reject unresolved production imports, source cycles, Web->Mobile, Mobile->Web, shared->apps, production->prototypes and framework/platform imports from shared cores.

Negative probes directly proved intended rejection. Diagnostic history retained:

```text
unsafe combined regex -> atomic safe path regexes
package-local node_modules gathered as roots -> doNotFollow.path = node_modules
```

### FM-06B — generated-source drift enforcement — PASS

```text
362b95a415ac7845260daf19cc99547501151eaa
build: enforce generated-source drift

pnpm generated:check
```

Checked authorities:

```text
packages/design-tokens/generated/web.css
packages/design-tokens/generated/native.ts
apps/web/src/routeTree.gen.ts
```

The checker snapshots current bytes, runs the real generators, compares byte-for-byte and restores pre-check bytes in all cases. Deliberate token and route-tree drift probes were rejected.

### FM-06C — real unit-test baseline — PASS

Implementation:

```text
610e33a7a31987d97564b1d6004a7b9896acaedc
test: establish shared frontend unit baseline
```

Runner:

```text
Vitest 4.1.11
pnpm test -> turbo run test
```

Real baseline:

```text
@dante/time    5 tests PASS
@dante/i18n    5 tests PASS
Turbo root     2 successful / 2 total
```

Coverage includes Temporal parsing/DST/round-trip/duration semantics and i18n locale/default/fallback/runtime/resource-shape/strict-selector semantics.

Final FM-06C regression:

```text
5-package strict TypeScript graph             PASS
architecture:check                            PASS
36 modules / 45 dependencies / 0 violations  PASS
generated:check                               PASS
lint / format                                 PASS
Web build                                     PASS
frozen install                                PASS
```

Known diagnostics retained: output-parser ANSI issue, pre-existing React/react-dom workspace peer warning, and strict i18next selector repair to explicit `common` namespace. The peer warning was proven pre-existing and is deferred to FM-07 clean closure for re-evaluation.

### FM-06D — Web E2E + Mobile bundle smoke — PASS

Implementation:

```text
d6138f5f5049e8fc11f877b774ff0191af44069f
test: establish frontend runtime smoke baseline
```

Materialized Web E2E:

```text
@playwright/test 1.62.1 exact app-local devDependency
Chromium only
pnpm test:e2e:web
Vite production build + preview
127.0.0.1:4173
reuseExistingServer = false
```

Direct browser evidence:

```text
Playwright Chromium browser installation PASS
Playwright Chromium Linux system dependencies PASS
Chromium headless process launch PASS
Vite production build PASS
Vite preview PASS
1 real browser E2E PASS
```

The real E2E asserts current diagnostic runtime semantics:

```text
route /
heading Frontend pronto
eyebrow DANTE Web
Percorso /
Scopo / Scaffold diagnostico FM-03
2026-08-22T20:00:00+02:00[Europe/Rome]
```

Materialized Mobile smoke:

```text
pnpm mobile:bundle:check
Expo SDK 57
expo export --platform android
Hermes bytecode enabled
temporary output outside repository
```

Direct Mobile evidence:

```text
Android export PASS
1 Hermes .hbc PASS
bundle size 4,077,727 bytes
non-empty bundle PASS
temporary export cleanup PASS
```

Classification:

```text
Mobile bundle smoke != APK/AAB release build
Mobile bundle smoke != device runtime
FM-04 Android emulator/Hermes execution remains stronger direct runtime evidence
```

Final FM-06D regression:

```text
pnpm test                                   PASS
5-package typecheck                         PASS
architecture 36 modules / 45 deps / 0      PASS
generated:check                             PASS
lint                                        PASS
format                                      PASS
Web build                                   PASS
pnpm install --frozen-lockfile              PASS
git diff --check                            PASS
9 authorized implementation paths           PASS
0 unexpected paths                          PASS
remote readback                              PASS
```

FM-06D diagnostics retained:

```text
attempt 1
Chromium failed before page creation on missing libnspr4.so
-> owning layer = WSL/Linux browser system dependencies
-> repaired through official `playwright install-deps chromium`
-> no repository dependency/config workaround

attempt 2
exact text locator for `Scaffold diagnostico FM-03` failed
because purpose + Temporal value share one semantic <dd>
-> application was correct
-> E2E anchored to `Scopo` definition row and asserted contained purpose + exact Temporal value
```

The older FM-04 `libnspr4.so` observation remains correctly classified: optional RN DevTools did not justify installing it then; FM-06D introduced a real Chromium process that did require the Linux library, making machine-level installation justified now.

## 6. Current validation register

```text
FM-V01 Node 24 WSL runtime resolution — PASS
FM-V02 pnpm 11 workspace/install — PASS
FM-V03 isolated dependency layout with Expo/native graph — PASS
FM-V04 hoisted fallback — NOT RUN / not needed
FM-V05 Turbo multi-workspace task graph — PASS
FM-V06 strict TypeScript cross-workspace graph — PASS
FM-V07 current dependency/cycle enforcement — PASS
FM-V08 Vite/React production build — PASS
FM-V09 Windows browser <-> WSL Vite — PASS
FM-V10 Expo SDK 57 / RN baseline — PASS
FM-V11 WSL Metro <-> Windows Android emulator — PASS
FM-V12 package exports / representative forbidden deep imports — PASS
FM-V13 design-token generation + drift rejection — PASS
FM-V14 shared i18n consumption + unit baseline — PASS
FM-V15 shared time consumption + unit baseline — PASS
FM-V16 TanStack Form + Zod real form — NOT RUN
FM-V17 TanStack Query first remote path — NOT RUN
FM-V18 OpenAPI -> Orval — NOT RUN
FM-V19 PowerSync + OP-SQLite + SQLCipher — NOT RUN
FM-V20 offline reconciliation — NOT RUN
FM-V21 identity-scoped local DB lifecycle — NOT RUN
FM-V22 versioned Web runtime config — NOT RUN
FM-V23 Cloudflare deployment — NOT RUN
FM-V24 Sentry — NOT RUN
FM-V25 EAS build/update/release — NOT RUN
```

## 7. Product-feature boundary

Materialization does not authorize invented AuthN/AuthZ transport, invented backend endpoints, product UI copied from prototypes, frontend canonical domain state or broad speculative shared packages.

Access remains the intended first production frontend vertical slice after the materialization baseline is closed. Home prototype/design work can continue separately.

## 8. Write discipline

Every materialization slice requires an exact remote gate with branch, PRE-SCOPE, CREATE/UPDATE/DELETE, purpose and explicit exclusions. Immediately before first branch-visible write, remote HEAD must equal PRE-SCOPE.

After writes:

```text
validate exact changed paths
zero unexpected paths
run applicable real QA
commit/push
remote readback
```

No direct `main` writes, casual force push or unscoped merge/rebase of `main` into this branch.

## 9. Exact next action

```text
FM-06E CI orchestration — READ-ONLY DISCOVERY FIRST
```

FM-06A/B/C/D are directly validated and closed at their stated scopes. FM-06E must now design and materialize CI orchestration only after inspecting the current repository tasks and GitHub Actions behavior. Required branch checks are not declared until the emitted check/job context names are directly observed.

Explicitly outside the FM-06D closure and not yet PASS:

```text
GitHub Actions frontend CI
required branch checks
Firefox/WebKit automated E2E
product Access/Home E2E
APK/AAB release build
iOS bundle/runtime
EAS
coverage thresholds
PowerSync
backend integration
main synchronization
FM-07 clean materialization baseline closure
```
