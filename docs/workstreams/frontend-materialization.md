# Workstream — Frontend Materialization

- Status: **ACTIVE — FM-06C REAL UNIT-TEST BASELINE PASS / FM-06 IN PROGRESS**
- Branch: `feature/frontend-materialization`
- Opening base: `ff46eb16b971b1fde96eef9047b09faa02e1a5db`
- Current validated workspace commit: `610e33a7a31987d97564b1d6004a7b9896acaedc`
- Frontend Engineering Foundation: **CLOSED / ACCEPTED / FINAL REVIEW PASS / integrated via PR #22**
- Production frontend scaffold: **ROOT WORKSPACE + ENGINEERING TOOLING + MINIMAL WEB + MINIMAL MOBILE + SHARED DESIGN TOKENS + SHARED I18N + SHARED TIME + DEPENDENCY ARCHITECTURE ENFORCEMENT + GENERATED-SOURCE DRIFT ENFORCEMENT + REAL UNIT-TEST BASELINE MATERIALIZED**
- Machine runtime baseline: **PASS**
- Root engineering dependencies: **INSTALLED / PINNED / LOCKED**
- Minimal Web dependency graph: **INSTALLED / PINNED / LOCKED**
- Minimal Mobile dependency graph: **INSTALLED / PINNED / LOCKED / DIRECTLY RUNTIME-VALIDATED**
- Shared design-token package: **MATERIALIZED / GENERATED / WEB+MOBILE DIRECTLY RUNTIME-VALIDATED**
- Shared i18n package: **MATERIALIZED / IT+EN / STRICTLY TYPED / WEB+MOBILE DIRECTLY RUNTIME-VALIDATED**
- Shared time package: **MATERIALIZED / TEMPORAL SEMANTICS / WEB+MOBILE DIRECTLY RUNTIME-VALIDATED**
- Unit-test baseline: **VITEST 4.1.11 / 10 REAL TESTS / ROOT TURBO 2/2 PASS**
- Direct frontend validation: **PARTIAL — FM-V01/FM-V02/FM-V03/FM-V05/FM-V06/FM-V08/FM-V09/FM-V10/FM-V11/FM-V13/FM-V14/FM-V15 PASS; FM-V07 CURRENT REAL ARCHITECTURE/CYCLE ENFORCEMENT PASS WITH FUTURE FEATURE-SPECIFIC RULES NOT RUN; FM-V12 PUBLIC SURFACES + REPRESENTATIVE FORBIDDEN DEEP-IMPORT REJECTION PASS; GENERATED-SOURCE DRIFT PASS; REAL UNIT-TEST BASELINE PASS; remaining register scoped below**
- Product-surface implementation: **NOT AUTHORIZED BY THIS CHECKPOINT**

## 1. Purpose

Materialize the accepted DANTE Frontend Engineering Foundation into a real, reproducible production workspace and directly validate the selected Web/Mobile/tooling boundaries before product feature implementation depends on them.

This workstream consumes rather than redesigns:

- `../architecture/frontend-engineering-foundation.md`;
- `../architecture/frontend-engineering-foundation-part-2.md`;
- `../architecture/frontend-engineering-foundation-final-review.md`;
- `../architecture/frontend-engineering-foundation-post-closure-qa.md`;
- `../decisions/ADR-008-frontend-engineering-stack.md`;
- `../decisions/ADR-009-frontend-architecture-boundaries.md`;
- closed Engineering Foundation/repository-layout authorities;
- accepted Physical target and applicable validation obligations.

## 2. Evidence discipline

```text
selected != installed
installed != configured
configured != directly validated
direct scenario PASS != whole-frontend PASS
```

No component receives a direct `PASS` merely because a package was added or a command returned successfully once.

Version-sensitive dependencies are reverified against current primary documentation immediately before installation. The accepted major/line remains the design baseline; exact patches are fixed during materialization after compatibility verification.

## 3. Developer topology

Primary LOCAL posture:

```text
WINDOWS 11
├── JetBrains / PyCharm UI
├── browser
├── Android Studio / Android emulator
└── Docker Desktop

WSL2 / Linux
├── linked DANTE Git worktree(s)
├── Git
├── Node / pnpm / Turbo
├── Vite
├── Metro / Expo CLI
├── Python / uv / backend tooling when applicable
└── Docker CLI

Docker LOCAL
└── stateful/local infrastructure only when real consumers exist
```

Normal frontend development processes are not containerized merely for appearance.

```text
Vite dev server     WSL process
Metro / Expo CLI    WSL process
Web browser         Windows
Android emulator    Windows
PostgreSQL          Docker when backend LOCAL infra is materialized
PowerSync service   Docker only when its real LOCAL integration scope activates
```

Hard invariant:

```text
ONE authoritative Git repository/history
purpose-specific linked Git worktrees inside WSL are allowed
NO divergent independent Windows + WSL clones/source trees
NO cross-OS shared node_modules tree
```

Observed parallel worktree topology:

```text
/home/mattia/projects/dante
feature/backend-scaffold

/home/mattia/projects/dante-frontend
feature/frontend-materialization
```

Detailed developer/onboarding authority: `../development/frontend-local-development.md`.

## 4. Materialization phases

### FM-00 — workstation preflight — PASS

Observed:

```text
WSL2 kernel                 PASS
Ubuntu                      24.04.4 LTS
Git                         2.43.0 /usr/bin/git
Docker CLI                  29.7.2 /usr/bin/docker
Docker Compose              5.4.0
frontend checkout           /home/mattia/projects/dante-frontend
Windows Node leakage        none observed
```

### FM-01 — runtime and package-manager baseline — PASS

```text
fnm         1.39.0
Node        24.19.0
npm         11.17.0
pnpm        11.22.0
```

Direct checks proved Linux-side runtime ownership, isolated login-shell selection and `.node-version` selection.

### FM-02 — root JavaScript workspace — PASS

#### FM-02A — minimal workspace authority

Repository authorities:

```text
.node-version
package.json
pnpm-workspace.yaml
pnpm-lock.yaml
```

Remote checkpoint:

```text
c3f7945da7137b2bdd9e9f8922af452f1a79770f
build: establish frontend workspace runtime baseline
```

#### FM-02B — root engineering tooling

```text
TypeScript          6.0.3
Turborepo           2.10.11
ESLint              10.8.1
@eslint/js           10.0.1
typescript-eslint   8.67.0
Prettier            3.9.0
```

Final tooling/lock checkpoint:

```text
7ad88e2fbba1e8140149be05f9a3fe3005ad0488
build: lock frontend engineering toolchain
```

Direct WSL validation included install, frozen install, lint, formatter authority, TypeScript base-config probe and Turbo configuration dry-run.

### FM-03 — minimal Web application — PASS

Materialized exact baseline:

```text
React                     19.2.8
React DOM                 19.2.8
Vite                      8.2.1
@vitejs/plugin-react      6.1.0
@tanstack/react-router    1.170.31
@tanstack/router-plugin   1.168.34
@types/node               24.13.3
@types/react              19.2.18
@types/react-dom          19.2.4
```

The minimal diagnostic route `/` is real production scaffold code but is not Access/Home product UI and does not invent backend contracts.

Generated Web closure:

```text
1568d90091064162da9a438f3555675f1921c226
build: lock minimal web runtime
```

Direct Web validation:

```text
pnpm install                                  PASS
pnpm build                                    PASS
pnpm typecheck                                PASS
pnpm lint                                     PASS
pnpm format:check                             PASS
pnpm install --frozen-lockfile                PASS
TanStack routeTree.gen.ts generation          PASS
Windows Firefox <- WSL Vite runtime           PASS
```

### FM-04 — minimal Mobile application — PASS

Materialized compatibility baseline:

```text
Expo                         57.0.9
React Native                 0.86.2
React                        19.2.3
Expo Router                  57.0.9
React Native Gesture Handler 2.32.0
React Native Reanimated      4.5.1
React Native Safe Area       5.7.0
React Native Screens         4.26.2
React Native Worklets        0.10.1
```

Validated implementation:

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

Expo Go warnings and optional WSL React Native DevTools `libnspr4.so` warning were non-blocking and do not authorize project `updates.url` or unrelated workstation changes.

### FM-05 — first genuine shared packages — COMPLETE

#### FM-05A — `@dante/design-tokens` — PASS

```text
implementation  acd846a06614270fda9d66542a3fdc87fca7202e
closure         d4d99b157bab9e00c4f0285bf82745e73a9c944d
Terrazzo        2.7.1
DTCG            2025.10
```

Initial real semantics are deliberately narrow: shared card/panel radii only. Generated Web CSS and Native TypeScript are committed deterministic output, not semantic authority.

Real consumers:

```text
Web    @dante/design-tokens/web.css
Mobile @dante/design-tokens/native
```

Direct Web + Android runtime PASS.

Metro diagnosis retained: the initial bare package subpath failed despite valid workspace visibility; a relative-import probe proved Metro could execute external TS; durable repair was the root `"."` package export with `react-native`/`default`. No Metro override, hoisting or Windows Node was introduced.

#### FM-05B — `@dante/i18n` — PASS

```text
implementation  5e5fae5d696a5da6b457e3198b70f642245ec323
closure         098be4c815eb724c32f49c277b058e85df81e03a
i18next         26.3.6
react-i18next   17.0.11
```

Locale authority:

```text
Italian  (it) PRIMARY / DEFAULT / FALLBACK
English  (en) SUPPORTED SECONDARY
```

The shared core owns locale/resource/fallback/type semantics; app bootstraps own React integration. Core resources are bundled locally and strict selector typing is enabled.

Direct Web Italian render, Android Italian render and English runtime switch PASS.

Source-first diagnosis retained: explicit `.ts` package-internal imports caused TS5097; durable repair is extensionless internal imports. Plain Node ESM strip-types is not the Vite/Metro bundler contract; Vite SSR was the valid Web runtime probe.

#### FM-05C — `@dante/time` — PASS

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

Do not use JavaScript `Date` as a universal DANTE time semantic. Locale and timezone remain separate concerns.

Direct evidence includes parsing, duration arithmetic, Instant/ZonedDateTime round trip, Europe/Rome DST transition, Firefox/Vite runtime and Android/Metro/Hermes runtime.

### FM-06 — architecture, generation and test enforcement — IN PROGRESS

FM-06 is deliberately split into bounded executable slices.

#### FM-06A — dependency architecture + cycle enforcement — PASS

Implementation:

```text
38dbbd3efb764a8419f4498d27a2e29a3602fc5d
build: enforce frontend dependency architecture
```

Tooling:

```text
dependency-cruiser 18.2.0
pnpm architecture:check
```

Initial real graph at closure:

```text
33 modules
40 dependencies cruised
0 enforced violations
```

The rules reject unresolved production imports, cycles, Web->Mobile, Mobile->Web, shared->apps, production->prototypes and framework/platform imports from shared cores.

Negative probes directly proved each intended boundary. Public package surfaces resolve and representative forbidden deep imports are rejected.

Diagnostic repairs retained:

```text
unsafe combined regex -> atomic safe path regexes
package-local node_modules gathered as roots -> doNotFollow.path = node_modules
```

Neither failure represented DANTE architecture violations and no rule was weakened.

#### FM-06B — generated-source drift enforcement — PASS

Implementation:

```text
362b95a415ac7845260daf19cc99547501151eaa
build: enforce generated-source drift
```

Root command:

```text
pnpm generated:check
```

Checked generated authorities:

```text
packages/design-tokens/generated/web.css
packages/design-tokens/generated/native.ts
apps/web/src/routeTree.gen.ts
```

The checker snapshots current bytes, invokes the real Terrazzo and TanStack Router Vite generation paths, compares byte-for-byte, reports exact drift and restores pre-check bytes in all cases.

Direct evidence:

```text
clean generated state PASS
token generated drift REJECTED / PASS
routeTree generated drift REJECTED / PASS
pre-check byte restoration PASS
second clean generated check PASS
architecture/typecheck/lint/format/build/frozen install PASS
3 authorized paths / 0 unexpected
remote readback PASS
```

Diagnostics retained: implicit Node globals were rejected by ESLint and repaired with explicit `node:process` stdout/stderr APIs; a failed textual repair was discarded and the still-uncommitted checker rewritten deterministically. No global ESLint exception or alternate router CLI was introduced.

#### FM-06C — real unit-test baseline — PASS

Implementation:

```text
610e33a7a31987d97564b1d6004a7b9896acaedc
test: establish shared frontend unit baseline
```

Materialized runner:

```text
Vitest 4.1.11
exact root devDependency pin
pnpm test -> turbo run test
```

Real test packages:

```text
@dante/time    5 tests PASS
@dante/i18n    5 tests PASS
Turbo root     2 successful / 2 total
```

`@dante/time` assertions cover:

```text
Temporal primitive parsing
Europe/Rome spring DST transition
Instant <-> ZonedDateTime round trip
PlainDateTime + Duration arithmetic
ZonedDateTime instant preservation
```

`@dante/i18n` assertions cover:

```text
supported locale/default/fallback contract
Italian runtime
English runtime
unsupported locale -> Italian fallback
IT/EN runtime resource leaf-shape parity
strict selectors with explicit common namespace
```

Regression after final test repair:

```text
5-package strict TypeScript graph             PASS
architecture:check                            PASS
36 modules / 45 dependencies / 0 violations  PASS
generated:check                               PASS
root lint                                     PASS
root format check                             PASS
Web production build                          PASS
pnpm install --frozen-lockfile                PASS
git diff --check                              PASS
7 authorized implementation paths             PASS
0 unexpected paths                            PASS
remote commit/readback                        PASS
```

FM-06C diagnostic record:

```text
1. package tests and root Turbo already PASS; script output parser failed on colored/prefixed output
   -> repaired by disabling/stripping ANSI and checking both task labels + Turbo 2/2 + non-zero tests

2. pnpm peers check surfaced react-dom@19.2.8 / Mobile react@19.2.3 mismatch
   -> read-only PRE-SCOPE comparison proved it already existed before FM-06C
   -> Web/Mobile lockfile importer blocks unchanged by FM-06C
   -> classified KNOWN PRE-EXISTING WORKSPACE PEER WARNING
   -> do not alter already runtime-validated Expo/RN React baseline merely to silence it
   -> re-evaluate in FM-07 clean closure if still observable

3. i18n runtime tests passed but strict TypeScript rejected flat selectors
   -> $.runtime / $.gesture changed to $.common.runtime / $.common.gesture
   -> tests now exercise the accepted strict namespace-selector contract
```

No DOM/component library, React Testing Library, React Native test renderer, coverage threshold, Playwright or CI workflow was introduced by FM-06C.

#### FM-06D — Web E2E + Mobile bundle smoke — NEXT

Read-only discovery must first reverify the current supported Playwright line and inspect the actual Expo SDK 57 deterministic headless bundle/export path. Do not choose these commands from memory.

#### FM-06E — CI orchestration after local checks are real — NOT RUN

A required GitHub check is not configured until its real emitted context has been observed and proven meaningful.

### FM-07 — materialization baseline closure

Closure requires evidence that a clean developer path can reproduce the accepted base:

```text
clean authoritative checkout/worktree
-> governed runtime versions
-> pnpm install --frozen-lockfile
-> pnpm lint
-> pnpm format:check
-> pnpm typecheck
-> pnpm architecture:check
-> pnpm generated:check
-> pnpm test
-> Web build/run
-> Mobile baseline/run on applicable local target
-> shared-package imports
-> architecture violations rejected
```

The pre-existing workspace-wide React/react-dom peer warning discovered during FM-06C must be re-observed/classified during FM-07 rather than silently fixed by changing the already-proven platform baselines.

Only after this baseline is directly validated should a product feature such as Access rely on it as production infrastructure.

## 5. Carried direct-validation register

```text
FM-V01 Node 24 WSL runtime resolution — PASS
FM-V02 pnpm 11 install/workspace resolution — PASS
FM-V03 preferred isolated dependency layout with Expo/native graph — PASS
FM-V04 evidence-driven hoisted fallback if required — NOT RUN
FM-V05 Turbo task graph — MULTI-WORKSPACE PASS: 5-PACKAGE TYPECHECK; DESIGN-TOKENS + WEB BUILD; I18N + TIME TEST
FM-V06 TypeScript strict cross-workspace graph — PASS: DESIGN-TOKENS + I18N + TIME + WEB + MOBILE
FM-V07 ESLint/import/boundary/cycle enforcement — PASS FOR CURRENT REAL PACKAGE/APPLICATION ARCHITECTURE + CYCLE RULES; FUTURE FEATURE/UI/PLATFORM-SPECIFIC RULES NOT RUN
FM-V08 Vite/React production build — PASS
FM-V09 Windows browser <-> WSL Vite — PASS
FM-V10 Expo SDK 57 / RN compatible baseline — PASS
FM-V11 WSL Metro <-> Windows Android emulator/device — PASS
FM-V12 package exports / forbidden deep imports — PASS
FM-V13 DTCG -> Web CSS + Native TS generation — PASS; GENERATED DRIFT REJECTION PASS THROUGH FM-06B
FM-V14 Web/Mobile i18n shared-core consumption — PASS; REAL I18N UNIT BASELINE PASS THROUGH FM-06C
FM-V15 Temporal/time shared-core consumption — PASS; REAL TIME UNIT BASELINE PASS THROUGH FM-06C
FM-V16 TanStack Form Web + RN + Zod when first real form activates — NOT RUN
FM-V17 TanStack Query remote path when first real remote path exists — NOT RUN
FM-V18 OpenAPI -> Orval when real backend OpenAPI exists — NOT RUN
FM-V19 PowerSync + OP-SQLite + SQLCipher encrypted lifecycle when sync scope activates — NOT RUN
FM-V20 offline upload/accept/reject/conflict reconciliation when backend path exists — NOT RUN
FM-V21 identity-scoped local DB lifecycle when Auth/session scope exists — NOT RUN
FM-V22 versioned Web runtime config when delivery bootstrap activates — NOT RUN
FM-V23 Cloudflare deployment when remote Web delivery activates — NOT RUN
FM-V24 Sentry integration when observability activates — NOT RUN
FM-V25 EAS build/update/release path when mobile release infrastructure activates — NOT RUN
```

Deferred items remain explicit `NOT RUN`, never silently converted to PASS.

## 6. Product-feature boundary

Access is the intended first production frontend vertical slice after the materialization baseline is stable enough to support it.

Home may continue separately as prototype/design evidence while its design is still evolving.

Materialization itself does **not** authorize:

- invented AuthN/AuthZ transport contracts;
- invented FastAPI endpoints;
- canonical state logic in the frontend;
- product UI copied from prototypes before the relevant base is ready;
- broad shared package extraction.

## 7. Documentation/onboarding requirement

A competent developer who did not participate in chat must be able to determine from the repository:

- required machine tooling;
- exact/guided setup sequence;
- runtime/package versions;
- where Web/Mobile/backend/infra run;
- normal commands;
- architecture boundaries;
- test/generation validation commands;
- troubleshooting/repair entry points;
- what is selected versus directly proven.

Chat memory is never required to reproduce the frontend environment.

## 8. Write discipline inside this workstream

Each materialization slice gets its own exact remote write gate and QA.

Before each dependency/materialization write:

1. verify branch HEAD;
2. verify current primary compatibility documentation when version-sensitive;
3. state exact CREATE/UPDATE/DELETE paths;
4. state validation expected from that slice;
5. write only authorized paths;
6. run/record applicable direct evidence;
7. compare expected versus actual paths;
8. preserve `NOT RUN` for evidence not actually executed.

## 9. Exact next action

```text
FM-06D Web E2E + Mobile bundle smoke — READ-ONLY DISCOVERY FIRST
```

FM-00 through FM-05C and FM-06A/FM-06B/FM-06C are directly validated at their stated scopes. FM-06D must next establish a real Web browser E2E baseline and deterministic Mobile bundle smoke without mixing CI orchestration or product UI into the slice.

Product UI, PowerSync, EAS release infrastructure and invented backend contracts remain outside this closure unless separately gated.
