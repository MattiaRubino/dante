# Workstream — Frontend Materialization

- Status: **TECHNICALLY COMPLETE — FM-07 PASS / FINAL HOSTED-CI PROOF + TEMPORARY CLEANUP PENDING**
- Branch: `feature/frontend-materialization`
- Opening base: `ff46eb16b971b1fde96eef9047b09faa02e1a5db`
- Current clean-materialization source commit: `e79beadbddcf401d1d20c483c2d15d0b3cce96ad`
- Last implementation/CI commit before FM-07 repair: `31deffddd35f69d48bee82465e0385e508c42876`
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

Hard invariants:

```text
ONE authoritative Git history
WSL-backed source/worktrees
NO divergent Windows + WSL clones
NO cross-OS shared node_modules
```

Observed worktree:

```text
/home/mattia/projects/dante-frontend
feature/frontend-materialization
```

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
checkpoint                1568d90091064162da9a438f3555675f1921c226
```

Direct Windows Firefox <- WSL Vite runtime PASS.

### FM-04 — minimal Mobile — PASS

```text
Expo specifier              57.0.9
Expo resolved in FM-07      57.0.15
React Native                0.86.2
React                       19.2.3
Expo Router specifier       57.0.9
Expo Router resolved        57.0.15
Gesture Handler             2.32.0
Reanimated                  4.5.1
Safe Area Context           5.7.0
Screens                     4.26.2
Worklets                    0.10.1
implementation              3c150c4806191f0347b64c645d53168123ce0ede
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

## 4. FM-05 — genuine shared packages — COMPLETE

### FM-05A — `@dante/design-tokens` — PASS

```text
implementation  acd846a06614270fda9d66542a3fdc87fca7202e
closure         d4d99b157bab9e00c4f0285bf82745e73a9c944d
Terrazzo        2.7.1
DTCG            2025.10
```

Initial shared semantics remain deliberately narrow: real duplicated radii only. Generated Web CSS and Native TypeScript are committed deterministic output.

### FM-05B — `@dante/i18n` — PASS

```text
implementation  5e5fae5d696a5da6b457e3198b70f642245ec323
closure         098be4c815eb724c32f49c277b058e85df81e03a
i18next         26.3.6
react-i18next   17.0.11
Italian         PRIMARY / DEFAULT / FALLBACK
English         SUPPORTED SECONDARY
```

Shared core owns locale/resources/fallback/types; app bootstraps own React integration. Strict selectors are enabled.

### FM-05C — `@dante/time` — PASS

```text
implementation      aeb43e9e5ed7add42464e61f5c02acd6a53fed85
closure             61d19795867e13818a2d43252906b565d23e96e5
temporal-polyfill   1.0.4
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

Do not use JavaScript `Date` as a universal DANTE time semantic. Locale and timezone remain separate concerns.

## 5. FM-06 — enforcement, tests, runtime smoke and CI — COMPLETE

### FM-06A — dependency architecture + cycle enforcement — PASS

```text
implementation  38dbbd3efb764a8419f4498d27a2e29a3602fc5d
closure         b57709b4ce073ec179b4e55dc6dda72f509641a4
dependency-cruiser 18.2.0
pnpm architecture:check
```

Current directly observed graph:

```text
36 DANTE-owned modules
45 dependencies cruised
0 violations
```

Rules reject unresolved production imports, source cycles, Web->Mobile, Mobile->Web, shared->apps, production->prototypes and framework/platform imports from shared cores.

### FM-06B — generated-source drift enforcement — PASS

```text
implementation  362b95a415ac7845260daf19cc99547501151eaa
closure         ae0ff9e9849ff3aedcd095a645750993297c4384
pnpm generated:check
```

Checked committed authorities:

```text
packages/design-tokens/generated/web.css
packages/design-tokens/generated/native.ts
apps/web/src/routeTree.gen.ts
```

### FM-06C — real unit-test baseline — PASS

```text
implementation  610e33a7a31987d97564b1d6004a7b9896acaedc
Vitest          4.1.11
@dante/time     5 PASS
@dante/i18n     5 PASS
Turbo root      2 successful / 2 total
```

Coverage includes Temporal parsing/DST/round-trip/duration semantics and i18n locale/default/fallback/runtime/resource-shape/strict-selector semantics.

### FM-06D — Web E2E + Mobile bundle smoke — PASS

```text
implementation  d6138f5f5049e8fc11f877b774ff0191af44069f
Playwright      1.62.1
browser         Chromium headless
Web E2E         1 real production-preview test PASS
Mobile smoke    Expo Android production export / Hermes .hbc PASS
FM-06D .hbc     4,077,727 bytes
```

Bundle smoke is not APK/AAB build and is not device execution; FM-04 Android emulator/Hermes execution remains stronger device-runtime evidence.

### FM-06E — GitHub-hosted CI orchestration — PASS

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

Required branch checks remain NOT CONFIGURED; branch protection is a separate governance scope.

The temporary `push -> feature/frontend-materialization` trigger is retained only until the FM-07 closure commit receives one final hosted-CI proof.

## 6. FM-07 — clean materialization baseline — PASS

### 6.1 Attempt 1

Source:

```text
8ec088f0fce1db1e6116fa15acc2302981616ac5
fresh HTTPS clone
no node_modules
isolated temporary pnpm store
isolated temporary Playwright browser path
```

All functional/build/test gates passed, but final repository immutability failed because normal Turbo execution created repository-visible untracked `.turbo/cache/**` files.

Root cause:

```text
Turborepo local cache is expected machine-generated state
.gitignore lacked .turbo/
```

Repository repair:

```text
e79beadbddcf401d1d20c483c2d15d0b3cce96ad
chore: ignore Turborepo local cache
```

The repair added `.turbo/` to `.gitignore` and changed no architecture/runtime dependency.

### 6.2 Clean retest after repair — PASS

Source:

```text
e79beadbddcf401d1d20c483c2d15d0b3cce96ad
new fresh HTTPS clone
no node_modules
clean Git state
.turbo correctly ignored
new isolated temporary pnpm store
new isolated temporary Chromium headless-shell path
```

Direct evidence:

```text
Node 24.19.0                                      PASS
pnpm 11.22.0                                      PASS
pnpm install --frozen-lockfile                    PASS
isolated pnpm store                               PASS
lockfile unchanged                                PASS
Expo `expo install --check`                       PASS / Dependencies are up to date
Playwright Chromium Linux dependency bootstrap    PASS
format:check                                      PASS
lint                                              PASS
5-package typecheck                               PASS
architecture:check                                PASS / 36 modules / 45 deps / 0 violations
generated:check                                   PASS
@dante/time                                       5 PASS
@dante/i18n                                       5 PASS
Turbo unit tasks                                  2/2 PASS
Web production Playwright E2E                     1 PASS
Mobile Expo Android Hermes bundle                 PASS
FM-07 observed .hbc                               4,077,727 bytes
production build                                  PASS
git diff --check                                  PASS
git diff --exit-code                              PASS
tracked repository residue                        0
untracked repository residue                      0
```

This proves the frontend engineering baseline can be materialized from a genuinely fresh checkout without relying on accumulated repository state, existing `node_modules`, the normal pnpm content store, or an existing Playwright browser cache.

### 6.3 React/react-dom peer diagnostic — classified / non-blocking

The clean install reproduced exactly one workspace peer diagnostic:

```text
pnpm peers check exit 1
unmet peer react
Installed: 19.2.3
Wanted: ^19.2.8
owner shown: react-dom@19.2.8
```

At the same fresh checkout:

```text
Expo `expo install --check` -> Dependencies are up to date
Mobile React               -> 19.2.3
React Native               -> 0.86.2
Expo resolved              -> 57.0.15
Web React/ReactDOM          -> 19.2.8 / 19.2.8
```

Final classification:

```text
KNOWN WORKSPACE PEER DIAGNOSTIC
reproducible on a fresh install
non-blocking for the directly validated Expo/RN baseline
NOT justification for React version changes
```

Do not add pnpm peer suppression, `packageExtensions`, `nodeLinker`/hoisting changes or arbitrary React version changes merely to make `pnpm peers check` green.

## 7. Current validation register

```text
FM-V01 Node 24 WSL runtime resolution — PASS
FM-V02 pnpm 11 workspace/install — PASS
FM-V03 isolated dependency layout with Expo/native graph — PASS
FM-V04 hoisted fallback — NOT RUN / not needed
FM-V05 Turbo multi-workspace task graph — PASS
FM-V06 strict TypeScript cross-workspace graph — PASS
FM-V07 dependency/cycle enforcement — PASS
FM-V08 Vite/React production build — PASS
FM-V09 Windows browser <-> WSL Vite — PASS
FM-V10 Expo SDK 57 / RN baseline — PASS
FM-V11 WSL Metro <-> Windows Android emulator — PASS
FM-V12 package exports / forbidden deep-import probes — PASS
FM-V13 design-token generation + drift rejection — PASS
FM-V14 shared i18n consumption + unit baseline — PASS
FM-V15 shared time consumption + unit baseline — PASS
FM-V26 GitHub-hosted frontend CI orchestration — PASS
FM-V27 fresh clean materialization baseline — PASS
```

Still NOT RUN because they belong to later product/integration/release scopes:

```text
TanStack Form + Zod real product form
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
required branch checks / branch protection mutation
backend integration
main synchronization
```

## 8. Product-feature boundary

Materialization does not authorize invented AuthN/AuthZ transport, invented backend endpoints, product UI copied blindly from prototypes, frontend canonical domain state or speculative shared packages.

Access remains the intended first production frontend vertical slice after final materialization cleanup/integration governance. Home prototype/design work can continue separately.

## 9. Exact next action

The frontend materialization baseline is technically complete. This documentation closure intentionally retains two temporary workstream mechanisms for one final proof:

```text
.github/workflows/frontend-ci.yml
  push -> feature/frontend-materialization  TEMPORARY

docs/workstreams/frontend-materialization-live-handoff.md
  TEMPORARY / DISPOSABLE SAVE-GAME
```

Next:

```text
1. observe the real GitHub-hosted Frontend CI triggered by this FM-07 closure commit
2. require Quality / Web E2E / Mobile Bundle PASS
3. then separately authorize final cleanup:
   - remove temporary feature-branch push trigger
   - delete temporary LIVE HANDOFF
4. prepare integration/PR to main as a separate governed scope
```

No direct `main` write, required-check mutation, deployment, product UI, PowerSync or backend integration is authorized by this closure.
