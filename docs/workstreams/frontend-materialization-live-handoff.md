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

Before any write:

```bash
git fetch origin feature/frontend-materialization
git rev-parse HEAD
git rev-parse origin/feature/frontend-materialization
git status --short
```

The documentation-closure commit containing this file is self-referential and cannot embed its own SHA without another commit. Resolve the current documentation HEAD from `origin/feature/frontend-materialization`. The last directly validated implementation SHA is recorded below.

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

Last directly validated implementation:

```text
d6138f5f5049e8fc11f877b774ff0191af44069f
test: establish frontend runtime smoke baseline
```

Current state:

```text
FM-06A dependency architecture enforcement     PASS
FM-06B generated-source drift enforcement      PASS
FM-06C real unit-test baseline                  PASS
FM-06D Web E2E + Mobile bundle smoke            PASS
FM-06                                             IN PROGRESS
NEXT = FM-06E CI ORCHESTRATION
```

The documentation closure containing this handoff should be resolved from the current remote branch HEAD after the closure commit lands.

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
```

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

Do not create a universal dictionary mixing unrelated concerns.

Do not create `@dante/api-client` until real FastAPI OpenAPI exists.

## 6. FM-06A — dependency architecture — PASS

Implementation:

```text
38dbbd3efb764a8419f4498d27a2e29a3602fc5d
```

Command:

```text
pnpm architecture:check
```

Rules currently reject:

```text
unresolvable production imports
source cycles
Web -> Mobile
Mobile -> Web
shared -> apps
production -> prototypes
shared core -> React / React DOM / React Native / react-i18next / Expo / Vite
```

Current observed graph after FM-06C/FM-06D:

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

Checker snapshots bytes, runs real generators, compares exact bytes and restores pre-check state. Token and route-tree deliberate drift probes were rejected.

Do not add an alternate TanStack Router CLI while the real Vite plugin owns route generation.

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

FM-06C diagnostics retained:

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

Exact implementation scope:

```text
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

9 authorized paths
0 unexpected
```

### Web E2E

```text
@playwright/test 1.62.1 exact app-local devDependency
Chromium only
headless
1 worker
0 retries
Vite production build + preview
127.0.0.1:4173
reuseExistingServer = false
```

Direct PASS:

```text
Playwright Chromium browser install
Playwright Chromium Linux system dependencies
Chromium process launch
Vite production build
Vite preview
1 real browser E2E
```

Asserted real runtime semantics:

```text
/
Frontend pronto
DANTE Web
Percorso /
Scopo / Scaffold diagnostico FM-03
2026-08-22T20:00:00+02:00[Europe/Rome]
```

### Mobile bundle smoke

```text
pnpm mobile:bundle:check
Expo SDK 57
expo export --platform android
Hermes bytecode enabled
output in OS temporary directory
```

Direct PASS:

```text
Android export
1 Android Hermes .hbc
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

### FM-06D final regression

```text
pnpm test                                  PASS
5-package typecheck                        PASS
architecture 36 modules / 45 deps / 0     PASS
generated:check                            PASS
lint                                       PASS
format                                     PASS
Web build                                  PASS
frozen install                             PASS
git diff --check                           PASS
commit/push/remote readback                PASS
```

### FM-06D diagnostic A — Chromium host dependency

Attempt 1 reached Playwright install + Vite build/preview, then Chromium failed before page creation:

```text
libnspr4.so: cannot open shared object file
```

Owning layer:

```text
WSL/Linux browser system dependencies
NOT DANTE Web
NOT test assertion
```

Accepted repair:

```bash
pnpm --filter @dante/web exec playwright install-deps chromium
```

This installed the required Ubuntu browser host packages, including `libnspr4`. The older FM-04 RN DevTools warning remains distinct: that helper was optional, while FM-06D Chromium is now a real required test process.

### FM-06D diagnostic B — semantic locator

After Chromium launched, the E2E failed only on an exact text search for:

```text
Scaffold diagnostico FM-03
```

The real DOM places purpose + Temporal value in the same `<dd>`, so exact full-element text did not equal the substring.

Accepted repair:

```text
anchor to visible `Scopo` definition row
assert contained purpose
assert exact Temporal value inside the row
```

Application code remained unchanged.

## 10. Normal local commands

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

Playwright machine setup on a fresh WSL host:

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

## 11. Write / QA governance

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

Immediately before first branch-visible write, re-read remote HEAD and require it to equal PRE-SCOPE. No silent scope expansion.

After writes:

```text
validate exact changed paths
zero unexpected paths
run applicable real QA
remote readback
```

No direct `main` work. No casual force push. No unscoped main merge/rebase.

## 12. CURRENT SLICE — FM-06E

Status:

```text
NEXT / READ-ONLY DISCOVERY REQUIRED BEFORE WRITE GATE
```

Objective:

```text
materialize CI orchestration for already-real local frontend gates
without creating a second validation architecture
```

Discovery must inspect:

```text
current GitHub workflow directory/state
current branch/PR event policy
Node + pnpm setup actions and supported versions
Playwright Chromium install/dependency path in GitHub-hosted Ubuntu
which local gates belong in CI and whether any should be split by job
actual emitted job/check names before configuring required branch checks
cache policy for pnpm/Turbo/Playwright browser binaries
failure-artifact policy for Playwright traces/reports
Mobile bundle-smoke requirements in headless CI
```

Do not create required branch checks until real emitted contexts have been observed.

FM-06E does not authorize product UI, backend contracts, PowerSync, EAS, coverage thresholds or main synchronization.

## 13. Future queued work

```text
FM-06E CI orchestration                     NEXT
FM-07 clean materialization baseline        NOT RUN
```

After FM-06E local/remote CI evidence is real, FM-07 performs clean-checkout/materialization closure.

## 14. Still NOT RUN / deferred

```text
hoisted pnpm fallback                         NOT RUN / not needed
feature-specific architecture rules           NOT RUN
GitHub Actions frontend CI                    NOT RUN — NEXT FM-06E
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
FM-07 clean baseline                          NOT RUN
```

Preserve these as NOT RUN until their real scope activates.
