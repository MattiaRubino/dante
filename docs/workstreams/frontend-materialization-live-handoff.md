# DANTE Frontend Materialization — LIVE HANDOFF

> TEMPORARY / DISPOSABLE SAVE-GAME.
>
> Purpose: make the frontend workstream resumable if the current chat dies.
> Keep this file updated after every substantive slice/gate.
> Delete it only when frontend materialization is fully closed and durable docs contain everything needed.

## 0. Resume protocol

Read this file completely, then read:

1. `docs/workstreams/frontend-materialization.md`
2. `docs/development/frontend-local-development.md`
3. `docs/decisions/ADR-008-frontend-engineering-stack.md`
4. `docs/decisions/ADR-009-frontend-architecture-boundaries.md`
5. referenced Frontend Engineering Foundation docs.

Before any repository write:

```bash
git fetch origin feature/frontend-materialization
git rev-parse HEAD
git rev-parse origin/feature/frontend-materialization
git status --short
```

Require remote HEAD to equal the approved PRE-SCOPE. No silent scope expansion.

The documentation-closure commit containing this file is self-referential and therefore cannot embed its own SHA without another commit. Resolve the current documentation closure SHA from `origin/feature/frontend-materialization`. The last directly validated implementation/CI SHA is recorded below.

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
Git / Node / pnpm / Turbo / Vite / Metro / Expo CLI / Playwright

Windows
Firefox/browser / Android Studio / Android emulator / ADB / JetBrains UI
```

Hard invariant:

```text
ONE authoritative Git history
WSL-backed source/worktrees
NO divergent Windows clone
NO cross-OS shared node_modules
```

Do not merge/rebase `main` into this branch unless separately scoped.

## 2. Current checkpoint

Last directly validated implementation/CI commit:

```text
31deffddd35f69d48bee82465e0385e508c42876
ci: materialize frontend validation workflow
```

Current state:

```text
FM-06A dependency architecture enforcement     PASS
FM-06B generated-source drift enforcement      PASS
FM-06C real unit-test baseline                  PASS
FM-06D Web E2E + Mobile bundle smoke            PASS
FM-06E GitHub-hosted CI orchestration           PASS
FM-06                                             COMPLETE
NEXT = FM-07 CLEAN MATERIALIZATION BASELINE
```

FM-06E was promoted to PASS only after a real GitHub-hosted run, not merely from workflow syntax or local parity.

## 3. Completed materialization checkpoints

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
FM-06D d6138f5f5049e8fc11f877b774ff0191af44069f
FM-06E 31deffddd35f69d48bee82465e0385e508c42876
```

Known durable closure SHAs before FM-06D:

```text
FM-05A closure  d4d99b157bab9e00c4f0285bf82745e73a9c944d
FM-05B closure  098be4c815eb724c32f49c277b058e85df81e03a
FM-05C closure  61d19795867e13818a2d43252906b565d23e96e5
FM-06A closure  b57709b4ce073ec179b4e55dc6dda72f509641a4
FM-06B closure  ae0ff9e9849ff3aedcd095a645750993297c4384
FM-06D closure  a481e24936c745c3573077a464a2af8a24794d1b
```

Resolve the FM-06E/FM-06 documentation closure from current branch HEAD after this docs commit lands.

## 4. Accepted toolchain

```text
Node                        24.19.0
pnpm                        11.22.0
TypeScript                  6.0.3
Turborepo                   2.10.11
ESLint                      10.8.1
Prettier                    3.9.0
dependency-cruiser          18.2.0
Vitest                      4.1.11
@playwright/test            1.62.1

Web
React / React DOM           19.2.8
Vite                        8.2.1
TanStack Router             1.170.31

Mobile
Expo                        57.0.9
React Native                0.86.2
React                       19.2.3
Expo Router                 57.0.9

Shared
i18next                     26.3.6
react-i18next               17.0.11
temporal-polyfill           1.0.4
Terrazzo                    2.7.1
```

## 5. Shared authority model

```text
visible copy / labels / messages / a11y
-> @dante/i18n

visual semantic values
-> @dante/design-tokens

platform control presentation
-> future Web/Mobile design-system implementation

assets
-> versioned asset authority

click/workflow behavior
-> owning feature logic
```

Do not create a universal dictionary mixing unrelated concerns. Do not create `@dante/api-client` until real FastAPI OpenAPI exists.

## 6. FM-06A — dependency architecture — PASS

Implementation:

```text
38dbbd3efb764a8419f4498d27a2e29a3602fc5d
```

Command:

```text
pnpm architecture:check
```

Rules reject:

```text
unresolvable production imports
source cycles
Web -> Mobile
Mobile -> Web
shared -> apps
production -> prototypes
shared core -> React / React DOM / React Native / react-i18next / Expo / Vite
```

Current observed graph:

```text
36 modules
45 dependencies
0 violations
```

Historical repairs:

```text
unsafe combined regex -> atomic safe regexes
third-party node_modules gathered as roots -> doNotFollow.path = node_modules
```

## 7. FM-06B — generated-source drift — PASS

Implementation:

```text
362b95a415ac7845260daf19cc99547501151eaa
```

Command:

```text
pnpm generated:check
```

Checked outputs:

```text
packages/design-tokens/generated/web.css
packages/design-tokens/generated/native.ts
apps/web/src/routeTree.gen.ts
```

Checker snapshots bytes, runs real generators, compares exact bytes and restores pre-check state. Deliberate token and route-tree drift probes were rejected.

## 8. FM-06C — real unit-test baseline — PASS

Implementation:

```text
610e33a7a31987d97564b1d6004a7b9896acaedc
```

```text
Vitest 4.1.11
@dante/time  5 tests PASS
@dante/i18n  5 tests PASS
root Turbo   2 successful / 2 total
```

Time coverage:

```text
Temporal primitive parsing
Europe/Rome DST transition
Instant <-> ZonedDateTime round trip
PlainDateTime + Duration arithmetic
ZonedDateTime instant preservation
```

i18n coverage:

```text
locale/default/fallback contract
Italian runtime
English runtime
unsupported locale -> Italian fallback
IT/EN resource-shape parity
strict explicit common namespace selectors
```

Diagnostics retained:

```text
root-output parser failure on colored/prefixed output
-> test execution itself already PASS
-> normalized ANSI evidence parser repair

workspace React/react-dom peer warning
-> proven PRE-EXISTING at FM-06C PRE-SCOPE
-> Web/Mobile importers unchanged
-> re-evaluate in FM-07 if still observable

strict selector typecheck
-> $.runtime / $.gesture rejected
-> repaired to $.common.runtime / $.common.gesture
```

## 9. FM-06D — Web E2E + Mobile bundle smoke — PASS

Implementation:

```text
d6138f5f5049e8fc11f877b774ff0191af44069f
test: establish frontend runtime smoke baseline
```

Web E2E:

```text
@playwright/test 1.62.1 exact app-local devDependency
Chromium only / headless
1 worker / 0 retries
Vite production build + preview
127.0.0.1:4173
1 real browser E2E PASS
```

Asserted real semantics:

```text
/
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
1 Android .hbc
4,077,727 bytes
non-empty
cleanup PASS
```

Classification:

```text
bundle smoke != APK/AAB release build
bundle smoke != device runtime
FM-04 Android emulator/Hermes runtime remains stronger direct runtime evidence
```

Diagnostics retained:

```text
attempt 1
Chromium failed before page creation on missing libnspr4.so
-> WSL/Linux browser host dependency
-> official playwright install-deps chromium repair

attempt 2
exact purpose locator failed because purpose + Temporal share one <dd>
-> application correct
-> semantic Scopo definition-row locator repair
```

## 10. FM-06E — GitHub-hosted CI — PASS

Implementation:

```text
31deffddd35f69d48bee82465e0385e508c42876
ci: materialize frontend validation workflow
```

Exact implementation scope:

```text
CREATE
.github/workflows/frontend-ci.yml

UPDATE
docs/workstreams/frontend-materialization-live-handoff.md

2 authorized paths
0 unexpected
```

Workflow authority:

```text
name: Frontend CI
runner: ubuntu-24.04
permissions: contents: read
concurrency: cancel stale runs for same workflow/ref
```

Triggers:

```text
pull_request -> main
push -> main
push -> feature/frontend-materialization  TEMPORARY FM-06E BOOTSTRAP
```

The feature-branch push trigger exists only to obtain real hosted evidence before integration. Remove it in a separately scoped final integration/closure step.

Action full-SHA pins:

```text
actions/checkout v7.0.1
3d3c42e5aac5ba805825da76410c181273ba90b1

pnpm/setup v2.0.0
c9883cc79df532ad1a7b81bf9ab944ceb090d65c

actions/upload-artifact v7.0.1
043fb46d1a93c77aae656e7c1c64a875d1fc6a0a
```

Bootstrap/cache policy:

```text
Node 24.19.0 exact
pnpm 11.22.0 exact
pnpm store cache only
automatic install false
explicit pnpm install --frozen-lockfile
NO node_modules cache
NO Playwright browser cache
NO Turbo remote cache
```

Jobs / real emitted context names:

```text
Quality
Web E2E
Mobile Bundle
```

Quality replays:

```text
format:check
lint
typecheck
architecture:check
generated:check
pnpm test
pnpm build
git diff --check
git diff --exit-code
```

Web E2E replays:

```text
frozen install
playwright install --with-deps --only-shell chromium
pnpm test:e2e:web
failure-only apps/web/test-results artifact
```

Mobile Bundle replays:

```text
frozen install
pnpm mobile:bundle:check
```

Authoritative hosted evidence:

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

The intermediate run #2 was superseded/cancelled under the configured concurrency policy. The latest authoritative run #3 is green.

Required checks remain:

```text
OBSERVED CONTEXT NAMES
Quality
Web E2E
Mobile Bundle

CONFIGURATION
NOT RUN / NOT AUTHORIZED IN FM-06E
```

Do not mutate branch protection merely because the names are now known.

## 11. Normal local commands

```bash
pnpm install --frozen-lockfile
pnpm lint
pnpm format:check
pnpm typecheck
pnpm architecture:check
pnpm generated:check
pnpm test
pnpm test:e2e:web
pnpm mobile:bundle:check
pnpm build
```

Playwright setup on a fresh WSL host:

```bash
pnpm --filter @dante/web exec playwright install chromium
pnpm --filter @dante/web exec playwright install-deps chromium
```

Web manual runtime:

```bash
cd ~/projects/dante-frontend
pnpm --filter @dante/web dev
```

Mobile manual runtime:

```bash
cd ~/projects/dante-frontend/apps/mobile
pnpm exec expo start --localhost
```

Then Windows ADB reverse:

```bash
powershell.exe -NoProfile -Command '& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" reverse tcp:8081 tcp:8081'
```

## 12. Write / QA governance

Before repository writes:

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

Immediately before first branch-visible write, re-read remote HEAD and require it to equal PRE-SCOPE. No silent expansion.

After writes:

```text
validate exact changed paths
zero unexpected paths
run applicable real QA
remote readback
```

No direct `main` work. No casual force push. No unscoped main merge/rebase.

## 13. CURRENT SLICE — FM-07

Status:

```text
NEXT / READ-ONLY DISCOVERY REQUIRED BEFORE WRITE GATE
```

Objective:

```text
prove clean frontend materialization from a fresh checkout/worktree
without relying on accumulated workstation repository state
```

Discovery must determine the exact clean-checkout procedure and evidence boundary before any write. Expected validation surface:

```text
fresh checkout/worktree at exact remote HEAD
Node 24.19.0 selection
pnpm 11.22.0 activation
pnpm install --frozen-lockfile
Playwright Chromium + Linux dependency bootstrap
format/lint/typecheck
architecture:check
generated:check
unit tests
Web E2E
Mobile Android Hermes bundle smoke
production build
repository mutation/diff checks
```

FM-07 must separately re-evaluate the known pre-existing React/react-dom workspace peer warning using clean-install evidence and current Expo/RN compatibility. Do not “repair” it with React version changes, pnpm peer suppression, packageExtensions, nodeLinker changes or hoisting without causal evidence.

No FM-07 write gate exists yet. Start READ-ONLY.

## 14. Still NOT RUN / deferred

```text
hoisted pnpm fallback                         NOT RUN / not needed
feature-specific architecture rules           NOT RUN
required branch checks                        NOT RUN
Firefox/WebKit automated E2E                  NOT RUN
product Access/Home E2E                       NOT RUN
TanStack Form + Zod real form                 NOT RUN
TanStack Query first remote path              NOT RUN
OpenAPI -> Orval                              NOT RUN
PowerSync / OP-SQLite / SQLCipher             NOT RUN
offline reconciliation                        NOT RUN
identity-scoped local DB lifecycle             NOT RUN
versioned Web runtime config                   NOT RUN
Cloudflare deployment                         NOT RUN
Sentry                                         NOT RUN
APK/AAB release build                         NOT RUN
iOS runtime/release                            NOT RUN
EAS release path                              NOT RUN
coverage thresholds                           NOT RUN
main synchronization                          NOT RUN
FM-07 clean baseline                          NOT RUN — NEXT
```

Preserve these as NOT RUN until their real scope activates.
