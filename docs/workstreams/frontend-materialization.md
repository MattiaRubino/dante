# Workstream — Frontend Materialization

- Status: **CLOSED / PASS — FM-00 THROUGH FM-07 COMPLETE AT THEIR STATED SCOPES**
- Branch: `feature/frontend-materialization`
- Opening base: `ff46eb16b971b1fde96eef9047b09faa02e1a5db`
- Clean-materialization source/repair commit: `e79beadbddcf401d1d20c483c2d15d0b3cce96ad`
- FM-07 documentation closure + final hosted-CI proof commit: `c1a77f249c716e0cb35159ecf2ad2c63b0bf4007`
- Last implementation/CI commit before FM-07 repair: `31deffddd35f69d48bee82465e0385e508c42876`
- Frontend Engineering Foundation: **CLOSED / ACCEPTED / FINAL REVIEW PASS / integrated via PR #22**
- Product-surface implementation: **NOT AUTHORIZED BY THIS WORKSTREAM**

## 1. Purpose and evidence discipline

This workstream materialized the accepted DANTE frontend engineering foundation into a real, reproducible Web/Mobile workspace and directly validated each platform/tooling boundary before product features depend on it.

Evidence discipline remains:

```text
selected != installed
installed != configured
configured != directly validated
scenario PASS != whole-system PASS
```

`NOT RUN` is not promoted to `PASS` without direct evidence.

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

Observed frontend worktree during materialization:

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

Repository authorities include `.node-version`, `package.json`, `pnpm-workspace.yaml` and `pnpm-lock.yaml`.

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
checkpoint                1568d90091064162da9a438f3555675f1921c226
```

Direct Windows Firefox <- WSL Vite runtime PASS.

### FM-04 — minimal Mobile — PASS

```text
Expo specifier              57.0.9
Expo clean-install resolve  57.0.15
React Native                0.86.2
React                       19.2.3
Expo Router specifier       57.0.9
Expo Router resolution      57.0.15
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

Bundle-smoke evidence elsewhere in this workstream does not replace this direct device-runtime evidence.

## 4. FM-05 — genuine shared packages — COMPLETE

### FM-05A — `@dante/design-tokens` — PASS

```text
implementation  acd846a06614270fda9d66542a3fdc87fca7202e
closure         d4d99b157bab9e00c4f0285bf82745e73a9c944d
Terrazzo        2.7.1
DTCG            2025.10
```

The package canonizes only real duplicated visual semantics. Initial shared semantics are deliberately narrow: duplicated radii. Generated Web CSS and Native TypeScript are committed deterministic output.

### FM-05B — `@dante/i18n` — PASS

```text
implementation  5e5fae5d696a5da6b457e3198b70f642245ec323
closure         098be4c815eb724c32f49c277b058e85df81e03a
i18next         26.3.6
react-i18next   17.0.11
Italian         PRIMARY / DEFAULT / FALLBACK
English         SUPPORTED SECONDARY
```

Shared core owns locales/resources/fallback/types; app bootstraps own React integration. Strict selectors are enabled. Source-first package internals use extensionless imports.

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
implementation       38dbbd3efb764a8419f4498d27a2e29a3602fc5d
closure              b57709b4ce073ec179b4e55dc6dda72f509641a4
dependency-cruiser   18.2.0
command              pnpm architecture:check
observed graph        36 modules / 45 dependencies / 0 violations
```

Rules reject unresolved production imports, source cycles, Web->Mobile, Mobile->Web, shared->apps, production->prototypes and framework/platform imports from shared cores. `node_modules` is deliberately excluded from graph traversal while external dependency edges remain visible.

### FM-06B — generated-source drift enforcement — PASS

```text
implementation  362b95a415ac7845260daf19cc99547501151eaa
closure         ae0ff9e9849ff3aedcd095a645750993297c4384
command         pnpm generated:check
```

Checked committed authorities:

```text
packages/design-tokens/generated/web.css
packages/design-tokens/generated/native.ts
apps/web/src/routeTree.gen.ts
```

The checker runs the real generation paths, compares byte-for-byte and restores pre-check bytes.

### FM-06C — real unit-test baseline — PASS

```text
implementation  610e33a7a31987d97564b1d6004a7b9896acaedc
Vitest          4.1.11
@dante/time     5 PASS
@dante/i18n     5 PASS
Turbo root      2 successful / 2 total
```

Coverage includes Temporal parsing/DST/round-trip/duration semantics and i18n locale/default/fallback/runtime/resource-shape/strict-selector semantics.

Retained diagnostics:

```text
Turbo/Vitest evidence parser false negative
-> normalize ANSI/prefixed output; test execution itself was PASS

strict i18next selector typecheck
-> $.runtime / $.gesture rejected
-> accepted form uses $.common.runtime / $.common.gesture
```

### FM-06D — Web E2E + Mobile bundle smoke — PASS

```text
implementation  d6138f5f5049e8fc11f877b774ff0191af44069f
Playwright      1.62.1
browser         Chromium headless
workers         1
retries         0
Web E2E         1 real production-preview test PASS
Mobile smoke    Expo Android production export / Hermes .hbc PASS
FM-06D .hbc     4,077,727 bytes
```

The Web E2E validates the real `/` route, `Frontend pronto`, `DANTE Web`, `Percorso /`, `Scopo / Scaffold diagnostico FM-03` and `2026-08-22T20:00:00+02:00[Europe/Rome]` using Vite production preview on `127.0.0.1:4173`.

Retained diagnostics:

```text
Chromium initial launch -> missing libnspr4.so
owning layer = WSL/Linux browser system dependencies
repair = official Playwright install-deps chromium

initial exact text locator -> purpose + Temporal value share one <dd>
application unchanged
repair = semantic Scopo definition-row locator
```

Bundle smoke is not APK/AAB build and is not device execution; FM-04 remains stronger direct Android runtime evidence.

### FM-06E — GitHub-hosted CI orchestration — PASS

```text
implementation 31deffddd35f69d48bee82465e0385e508c42876
workflow       .github/workflows/frontend-ci.yml
name           Frontend CI
runner         ubuntu-24.04
permissions    contents: read
```

External Actions are pinned to full immutable commit SHAs:

```text
actions/checkout v7.0.1
3d3c42e5aac5ba805825da76410c181273ba90b1

pnpm/setup v2.0.0
c9883cc79df532ad1a7b81bf9ab944ceb090d65c

actions/upload-artifact v7.0.1
043fb46d1a93c77aae656e7c1c64a875d1fc6a0a
```

CI bootstrap:

```text
Node 24.19.0 exact
pnpm 11.22.0 exact
pnpm store cache only
explicit pnpm install --frozen-lockfile
NO node_modules cache
NO Playwright browser cache
NO Turbo remote cache
```

Real emitted job/check names:

```text
Quality
Web E2E
Mobile Bundle
```

Initial authoritative hosted evidence:

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

Required branch checks remain NOT CONFIGURED; branch protection is a separate governance scope.

The temporary feature-branch push trigger used only to bootstrap and prove the workflow has been removed in the final materialization cleanup. The durable workflow trigger posture after closure is:

```text
pull_request -> main
push -> main
```

## 6. FM-07 — clean materialization baseline — PASS

### 6.1 Attempt 1 — repository hygiene failure only

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

Do not add peer suppression, `packageExtensions`, `nodeLinker`/hoisting changes or arbitrary React version changes merely to make `pnpm peers check` green.

### 6.4 FM-07 documentation closure hosted proof — PASS

The documentation closure itself was also executed by the real GitHub-hosted workflow before temporary cleanup:

```text
commit        c1a77f249c716e0cb35159ecf2ad2c63b0bf4007
event         push
overall       SUCCESS
total         53s
Quality       PASS / 49s
Web E2E       PASS / 46s
Mobile Bundle PASS / 40s
Vitest        @dante/time 5 PASS + @dante/i18n 5 PASS
```

This is the final hosted-CI proof for the materialized baseline before removal of the temporary feature-branch trigger.

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
FM-V28 final hosted-CI proof on FM-07 closure — PASS
```

## 8. Durable authority model

```text
visible copy / labels / messages / a11y -> @dante/i18n
visual semantic values                  -> @dante/design-tokens
platform control presentation           -> Web/Mobile design-system layers when real UI requires them
assets                                  -> versioned asset authority
click/workflow behavior                 -> owning feature logic
```

Do not create a universal dictionary mixing unrelated concerns. Do not create `@dante/api-client` until real FastAPI OpenAPI exists.

## 9. Still NOT RUN / later scopes

These remain outside the materialization workstream and must not be interpreted as failures:

```text
required branch checks / branch protection mutation
Firefox/WebKit automated E2E
product Access/Home E2E
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
backend integration
main synchronization / merge
```

## 10. Product-feature boundary

Materialization does not authorize invented AuthN/AuthZ transport, invented backend endpoints, product UI copied blindly from prototypes, frontend canonical domain state or speculative shared packages.

Access remains the intended first production frontend vertical slice after integration governance. Home prototype/design work can continue separately.

## 11. Closure state and next scope

Frontend materialization is **CLOSED / PASS**.

Temporary mechanisms used only to make this workstream resumable and directly verifiable have been removed:

```text
feature/frontend-materialization push trigger -> REMOVED
frontend-materialization-live-handoff.md      -> DELETED
```

The durable documentation now carries the required materialization history and runbook knowledge.

Next work is a separate governed scope:

```text
prepare/review integration PR to main
observe PR-triggered Frontend CI
merge only under separate authorization
do not mutate required checks / branch protection unless separately scoped
```

No direct `main` write, deployment, product UI, PowerSync or backend integration is authorized by this closure.
