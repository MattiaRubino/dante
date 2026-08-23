# Workstream — Frontend Materialization

- Status: **ACTIVE — FM-06 COMPLETE / FM-07 CLEAN MATERIALIZATION BASELINE NEXT**
- Branch: `feature/frontend-materialization`
- Opening base: `ff46eb16b971b1fde96eef9047b09faa02e1a5db`
- Current validated frontend implementation/CI commit: `31deffddd35f69d48bee82465e0385e508c42876`
- Frontend Engineering Foundation: **CLOSED / ACCEPTED / FINAL REVIEW PASS / integrated via PR #22**
- Product-surface implementation: **NOT AUTHORIZED BY THIS CHECKPOINT**

## 1. Purpose

Materialize the accepted DANTE frontend engineering foundation into a real, reproducible Web/Mobile workspace and directly validate each platform/tooling boundary before product features depend on it.

Evidence discipline:

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
├── Vite / Playwright
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

Checkpoints:

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

Initial shared semantics are deliberately narrow: duplicated card/panel radii only. Generated Web CSS and Native TypeScript are committed deterministic output. The durable Metro repair was a valid root package export; no hoisting, custom Metro resolver or Windows Node path was introduced.

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

Shared core owns locale/resources/fallback/types; app bootstraps own React integration. Strict selectors are enabled. Direct Web + Android Italian runtime PASS; English runtime switch PASS. Source-first package internals use extensionless imports.

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

## 5. FM-06 — enforcement, tests, runtime smoke and CI — COMPLETE

### FM-06A — dependency architecture + cycle enforcement — PASS

```text
implementation  38dbbd3efb764a8419f4498d27a2e29a3602fc5d
closure         b57709b4ce073ec179b4e55dc6dda72f509641a4
dependency-cruiser 18.2.0
pnpm architecture:check
```

Rules reject unresolved production imports, source cycles, Web->Mobile, Mobile->Web, shared->apps, production->prototypes and framework/platform imports from shared cores.

Historical diagnostics retained:

```text
unsafe combined regex -> atomic safe path regexes
package-local node_modules gathered as roots -> doNotFollow.path = node_modules
```

### FM-06B — generated-source drift enforcement — PASS

```text
implementation  362b95a415ac7845260daf19cc99547501151eaa
closure         ae0ff9e9849ff3aedcd095a645750993297c4384
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

```text
implementation  610e33a7a31987d97564b1d6004a7b9896acaedc
Vitest          4.1.11 exact root devDependency
pnpm test       turbo run test
```

Real baseline:

```text
@dante/time    5 tests PASS
@dante/i18n    5 tests PASS
Turbo root     2 successful / 2 total
```

Coverage includes Temporal parsing/DST/round-trip/duration semantics and i18n locale/default/fallback/runtime/resource-shape/strict-selector semantics.

Final regression:

```text
5-package strict TypeScript graph             PASS
architecture:check                            PASS
36 modules / 45 dependencies / 0 violations  PASS
generated:check                               PASS
lint / format                                 PASS
Web build                                     PASS
frozen install                                PASS
```

Known diagnostics retained: root-output ANSI parser false negative, strict i18next selector repair to explicit `common` namespace, and a React/react-dom workspace peer warning proven to pre-exist FM-06C. The peer warning is intentionally re-evaluated in FM-07 rather than silenced through arbitrary React/pnpm configuration changes.

### FM-06D — Web E2E + Mobile bundle smoke — PASS

Implementation:

```text
d6138f5f5049e8fc11f877b774ff0191af44069f
test: establish frontend runtime smoke baseline
```

Web E2E:

```text
@playwright/test 1.62.1 exact app-local devDependency
Chromium headless
1 worker / 0 retries
pnpm test:e2e:web
Vite production build + preview
127.0.0.1:4173
reuseExistingServer = false
1 real browser E2E PASS
```

Asserted runtime semantics:

```text
route /
Frontend pronto
DANTE Web
Percorso /
Scopo / Scaffold diagnostico FM-03
2026-08-22T20:00:00+02:00[Europe/Rome]
```

Mobile bundle smoke:

```text
pnpm mobile:bundle:check
Expo SDK 57
expo export --platform android
Hermes bytecode enabled
1 non-empty Android .hbc
observed size 4,077,727 bytes
temporary output cleanup PASS
```

Classification remains explicit: bundle smoke is not APK/AAB build and is not device execution; FM-04 Android emulator/Hermes execution remains stronger runtime evidence.

FM-06D diagnostics retained:

```text
Chromium initial launch -> missing libnspr4.so
owning layer = WSL/Linux browser system dependencies
repair = official playwright install-deps chromium

initial exact text locator -> purpose + Temporal value share one <dd>
application unchanged
repair = semantic Scopo definition-row locator
```

### FM-06E — GitHub-hosted CI orchestration — PASS

Implementation:

```text
31deffddd35f69d48bee82465e0385e508c42876
ci: materialize frontend validation workflow
```

Repository authority:

```text
.github/workflows/frontend-ci.yml
name: Frontend CI
runner: ubuntu-24.04
permissions: contents: read
concurrency: cancel stale runs for same workflow/ref
```

External Actions are pinned to immutable full commit SHAs:

```text
actions/checkout v7.0.1
3d3c42e5aac5ba805825da76410c181273ba90b1

pnpm/setup v2.0.0
c9883cc79df532ad1a7b81bf9ab944ceb090d65c

actions/upload-artifact v7.0.1
043fb46d1a93c77aae656e7c1c64a875d1fc6a0a
```

CI runtime/bootstrap:

```text
Node 24.19.0 exact
pnpm 11.22.0 exact
pnpm store cache only
explicit pnpm install --frozen-lockfile
NO node_modules cache
NO Playwright browser cache
NO Turbo remote cache
```

Jobs replay existing local authorities rather than creating a second validation architecture:

```text
Quality
  format:check
  lint
  typecheck
  architecture:check
  generated:check
  pnpm test
  pnpm build
  git diff --check
  git diff --exit-code

Web E2E
  frozen install
  Playwright Chromium headless shell + Linux deps
  pnpm test:e2e:web
  upload test-results only on failure

Mobile Bundle
  frozen install
  pnpm mobile:bundle:check
```

Real GitHub-hosted evidence from the authoritative push run:

```text
Frontend CI #3
commit       31deffddd35f69d48bee82465e0385e508c42876
event        push
overall      SUCCESS
duration     1m 14s

Quality        PASS / 47s
Web E2E        PASS / 47s
Mobile Bundle  PASS / 53s

Quality summary
@dante/time    5 tests PASS
@dante/i18n    5 tests PASS
```

The intermediate run #2 was superseded/cancelled under the configured concurrency policy; the latest authoritative run #3 is green.

Observed real check/job names are therefore:

```text
Quality
Web E2E
Mobile Bundle
```

Required branch checks are **NOT CONFIGURED** in FM-06E. They require a separate governance scope after the real emitted context names have been observed, which is now satisfied as evidence but not authorization to mutate branch protection.

Trigger posture during this workstream:

```text
pull_request -> main
push -> main
push -> feature/frontend-materialization  TEMPORARY FM-06E BOOTSTRAP
```

The feature-branch push trigger exists only to obtain real GitHub-hosted evidence before integration and must be removed when the final integration/closure scope authorizes it.

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
FM-V26 GitHub-hosted frontend CI orchestration — PASS
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
FM-07 clean materialization baseline — READ-ONLY DISCOVERY FIRST
```

FM-06A/B/C/D/E are now directly validated at their stated scopes and FM-06 is complete.

FM-07 must prove the accepted frontend can be materialized from a clean checkout/worktree without hidden state from the accumulated workstation. It must also re-evaluate the known pre-existing workspace React/react-dom peer warning under the clean install and current Expo compatibility evidence.

Still NOT RUN / outside the completed FM-06 scope:

```text
required branch checks / branch protection mutation
Firefox/WebKit automated E2E
product Access/Home E2E
TanStack Form + Zod real form
TanStack Query first remote path
OpenAPI -> Orval
PowerSync / OP-SQLite / SQLCipher
offline reconciliation
identity-scoped local DB lifecycle
versioned Web runtime config
Cloudflare deployment
Sentry
APK/AAB release build
iOS runtime/release
EAS release path
coverage thresholds
backend integration
main synchronization
FM-07 clean baseline
```
