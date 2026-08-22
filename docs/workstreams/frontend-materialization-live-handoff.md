# DANTE Frontend Materialization — LIVE HANDOFF

> TEMPORARY / DISPOSABLE SAVE-GAME.
>
> Purpose: make the frontend workstream resumable if the current chat dies.
> Keep this file updated after every substantive slice/gate.
> Delete it only when the frontend-materialization workstream is fully closed and the durable docs contain everything needed.

## 0. Resume protocol for a new chat

A new chat must first read this file completely, then read these durable authorities from GitHub:

1. `docs/workstreams/frontend-materialization.md`
2. `docs/development/frontend-local-development.md`
3. `docs/decisions/ADR-008-frontend-engineering-stack.md`
4. `docs/decisions/ADR-009-frontend-architecture-boundaries.md`
5. Frontend Engineering Foundation docs referenced by the workstream.

Do not restart discovery from memory and do not redesign already accepted decisions unless new evidence contradicts them.

## 1. Repository / branch / workstation

Repository:

```text
MattiaRubino/dante
```

Active frontend worktree:

```text
/home/mattia/projects/dante-frontend
```

Active branch:

```text
feature/frontend-materialization
```

Authoritative execution split:

```text
WSL2/Linux
Git
Node
pnpm
Turbo
Vite
Metro / Expo CLI

Windows
Firefox/browser
Android Studio
Android emulator
ADB platform tools
JetBrains/PyCharm UI
```

Hard invariant:

```text
ONE authoritative Git history
WSL-backed source/worktrees
NO independent divergent Windows clone
NO cross-OS shared node_modules
```

## 2. Current remote checkpoint

Current durable remote HEAD before FM-06A:

```text
61d19795867e13818a2d43252906b565d23e96e5
docs: close FM-05C shared time
```

FM-06A must start only if local HEAD and `origin/feature/frontend-materialization` still equal this SHA.

## 3. Completed frontend materialization

### FM-00 workstation preflight — PASS

Observed:

```text
Ubuntu 24.04.4 LTS / WSL2
Git 2.43.0
Docker CLI 29.7.2
Docker Compose 5.4.0
```

### FM-01 runtime/package-manager — PASS

```text
fnm   1.39.0
Node  24.19.0
npm   11.17.0
pnpm  11.22.0
```

### FM-02A root workspace — PASS

Commit:

```text
c3f7945da7137b2bdd9e9f8922af452f1a79770f
build: establish frontend workspace runtime baseline
```

### FM-02B root engineering tooling — PASS

Accepted exact lines:

```text
TypeScript          6.0.3
Turborepo           2.10.11
ESLint              10.8.1
@eslint/js           10.0.1
typescript-eslint   8.67.0
Prettier            3.9.0
```

Final lock/tooling checkpoint:

```text
7ad88e2fbba1e8140149be05f9a3fe3005ad0488
build: lock frontend engineering toolchain
```

### FM-03 minimal Web — PASS

Stack:

```text
React                     19.2.8
React DOM                 19.2.8
Vite                      8.2.1
@vitejs/plugin-react      6.1.0
@tanstack/react-router    1.170.31
@tanstack/router-plugin   1.168.34
```

Generated Web closure:

```text
1568d90091064162da9a438f3555675f1921c226
build: lock minimal web runtime
```

Windows Firefox ↔ WSL Vite runtime is directly validated.

### FM-04 minimal Mobile — PASS

Stack:

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

Directly validated:

```text
Windows Android emulator
ADB reverse tcp:8081 tcp:8081
Metro in WSL
Expo Go 57.0.9
Hermes bundle/runtime
Gesture Handler
Reanimated
```

Do NOT add project `updates.url` because of Expo Go client warnings.

Optional RN DevTools missing `libnspr4.so` was non-blocking. Do not install it unless DevTools itself becomes required.

### FM-05A shared design tokens — PASS

Implementation:

```text
acd846a06614270fda9d66542a3fdc87fca7202e
feat: materialize shared design tokens
```

Documentation closure:

```text
d4d99b157bab9e00c4f0285bf82745e73a9c944d
docs: close FM-05A design-token materialization
```

Package:

```text
@dante/design-tokens
Terrazzo 2.7.1
DTCG 2025.10
```

Initial real shared semantics only:

```text
semantic.radius.card  = 20
semantic.radius.panel = 12
```

Generated outputs:

```text
packages/design-tokens/generated/web.css
packages/design-tokens/generated/native.ts
```

Direct Web + Android runtime PASS.

Important Metro diagnosis:
- bare `@dante/design-tokens/native` initially failed;
- workspace symlink, TS support and Metro visibility were already correct;
- `--clear` did NOT fix it;
- temporary relative import proved Metro could execute external workspace TS;
- durable repair was a root `"."` package export with `react-native`/`default`;
- no Metro override, hoisting, alternate clone or Windows Node was introduced.

### FM-05B shared i18n — PASS

Implementation:

```text
5e5fae5d696a5da6b457e3198b70f642245ec323
feat: materialize shared i18n
```

Documentation closure:

```text
098be4c815eb724c32f49c277b058e85df81e03a
docs: close FM-05B shared i18n
```

Package:

```text
@dante/i18n
i18next        26.3.6
react-i18next  17.0.11
```

Locale policy:

```text
Italian  (it) PRIMARY / DEFAULT / FALLBACK
English  (en) SUPPORTED SECONDARY
other locales NOT YET SUPPORTED
```

Core is framework-free; React integration is app-owned.

Strict selector typing/runtime is enabled.

Direct Web Italian render PASS.
Direct Android Italian render PASS.
English `changeLanguage('en')` runtime PASS.

Important source-first diagnosis:
- explicit `.ts` internal imports caused TS5097 in consuming workspaces;
- accepted repair is extensionless package-internal imports;
- plain Node ESM `--experimental-strip-types` was rejected as non-representative for Vite/Metro Bundler resolution;
- Vite SSR was the valid Web resolution/runtime probe.

### FM-05C shared time — PASS

Implementation:

```text
aeb43e9e5ed7add42464e61f5c02acd6a53fed85
feat: materialize shared time semantics
```

Documentation closure / current remote HEAD:

```text
61d19795867e13818a2d43252906b565d23e96e5
docs: close FM-05C shared time
```

Package:

```text
@dante/time
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

Do NOT use JavaScript `Date` as a universal DANTE time semantic.

Locale and timezone are different concerns:

```text
it / en                     -> i18n
Europe/Rome / America/...   -> time/platform/user preference
```

Directly validated:
- Instant parse;
- PlainDate preservation;
- PlainTime parse;
- PlainDateTime + Duration arithmetic;
- ZonedDateTime parse;
- Instant ↔ ZonedDateTime round trip;
- Europe/Rome DST transition;
- Firefox/Vite runtime;
- Android/Metro/Hermes runtime.

Observed Temporal Web route footprint:

```text
61.27 kB raw
21.49 kB gzip
```

This is observed evidence, not yet a permanent performance budget.

FM-05 is COMPLETE.

## 4. UI / content authority model

Default ownership:

```text
user-visible copy / labels / messages / a11y
-> @dante/i18n

colors / radii / spacing / typography / shadows / theme semantics
-> @dante/design-tokens

Button / Card / control presentation and visual states
-> platform design-system implementation

logos / images / illustrations / backgrounds
-> versioned asset authority

click behavior / workflow / feature decisions
-> owning feature logic
```

Do not create one universal dictionary containing unrelated concerns.

## 5. Architecture rules already accepted

From ADR-009:

```text
apps/backend
apps/web
apps/mobile
```

are sibling deployables.

Web/Mobile are platform-specific clients with selective semantic sharing.

When real product structure exists:

```text
features/<capability>
platform/
ui/
bootstrap/
routes/navigation adapters
```

Cross-boundary dependencies use public APIs only.

Feature/package dependencies must remain acyclic.

Shared packages exist only for genuine multi-consumer semantics.

Shared client cores are framework/platform-free by default.

Backend remains canonical authority for Domain/AuthZ/conflict/accepted effect/material history.

Do not create `@dante/api-client` until real FastAPI OpenAPI exists.

Do not create broad shared feature packages before real Web+Mobile reuse exists.

## 6. Write / QA governance

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

Immediately before first write:
- fetch remote;
- local HEAD must equal PRE-SCOPE;
- remote branch HEAD must equal PRE-SCOPE;
- working tree must satisfy the gate.

No silent scope expansion.

After writes:
- validate exact changed paths;
- zero unexpected paths;
- run applicable real QA;
- remote readback after push.

Evidence rule:

```text
selected != installed
installed != configured
configured != directly validated
scenario PASS != whole-system PASS
```

Never convert NOT RUN to PASS without direct evidence.

No direct work on `main`.
No casual force push.
No merge/rebase of `main` into this branch unless separately scoped.

## 7. Local runtime sequences

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

Second WSL terminal:

```bash
powershell.exe -NoProfile -Command '& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" reverse tcp:8081 tcp:8081'
```

Launch:

```text
exp://127.0.0.1:8081
```

Do not introduce tunnel/hoisting/Metro config/Windows Node without concrete contradictory evidence.

## 8. FM-06 plan

FM-06 is intentionally split:

```text
FM-06A dependency architecture + cycle enforcement
FM-06B generated-source drift enforcement
FM-06C unit-test baseline
FM-06D Web E2E + Mobile bundle smoke
FM-06E CI orchestration after local checks are real
```

Do not create a giant enforcement commit.

Do not enforce feature/ui/platform rules before those real structures exist.

## 9. CURRENT SLICE — FM-06A

Status at creation of this handoff:

```text
APPROVED / MATERIALIZATION ABOUT TO RUN
NOT YET PASS
NOT YET COMMITTED
```

Current FM-06A implementation state:

```text
STATIC / NEGATIVE-PROBE QA PASS
COMMIT + PUSH ABOUT TO RUN
```

Observed diagnostics retained:
- attempt 1: unsafe combined regex -> repaired with atomic safe patterns;
- attempt 2: package-root scan included node_modules -> repaired with
  `doNotFollow.path = 'node_modules'`, preserving external boundary visibility.

Accepted dependency after materialization-time revalidation:

```text
dependency-cruiser 18.2.0
```

Compatibility verified against current package metadata:

```text
Node:       ^22 || ^24 || >=26
TypeScript: >=2 <7
```

This covers DANTE Node 24.19.0 + TypeScript 6.0.3.

FM-06A must enforce only currently real boundaries:

```text
source dependency cycles       FORBIDDEN
Web -> Mobile                  FORBIDDEN
Mobile -> Web                  FORBIDDEN
shared packages -> apps        FORBIDDEN
production frontend -> prototypes FORBIDDEN
framework/platform imports from shared cores FORBIDDEN
unresolvable source imports    FORBIDDEN
```

Public package surfaces must remain usable:

```text
@dante/design-tokens/native
@dante/design-tokens/web.css
@dante/i18n
@dante/time
```

Forbidden deep imports must be directly rejected, including representative probes under:

```text
@dante/time/src/...
@dante/i18n/src/...
@dante/design-tokens/generated/...
```

Do NOT claim yet:

```text
feature -> feature public API enforcement
routes -> feature public API enforcement
ui/platform -> feature prohibition
feature cycle semantics
```

because those real directories/consumers do not yet exist.

## 10. FM-06A exact repository gate

The user's latest instruction explicitly approved proceeding with FM-06A and requested this live handoff file.

The script shown with this file uses this exact gate:

```text
BRANCH
feature/frontend-materialization

PRE-SCOPE
61d19795867e13818a2d43252906b565d23e96e5

CREATE
dependency-cruiser.config.mjs
docs/workstreams/frontend-materialization-live-handoff.md

UPDATE
package.json
pnpm-lock.yaml

DELETE
none

PURPOSE
Materialize FM-06A executable dependency-architecture enforcement
and establish the disposable live handoff/save-game used for every
subsequent frontend-materialization slice.

VALIDATE
dependency-cruiser current real graph PASS
deliberate Web -> Mobile violation FAIL
deliberate Mobile -> Web violation FAIL
deliberate shared package -> app violation FAIL
deliberate source cycle FAIL
deliberate shared-core framework import FAIL
public @dante exports PASS
forbidden @dante deep imports FAIL
existing typecheck/lint/format/build PASS
frozen install PASS
exact authorized delta
commit/push/remote readback only after all gates PASS

EXPLICITLY OUT OF SCOPE
feature-layer enforcement not backed by real directories
Vitest
Playwright
Mobile bundle smoke
generated-source drift checks
GitHub Actions
product UI
Access/Home
PowerSync
backend contracts
main synchronization
```

## 10A. FM-06A attempt-1 diagnostic record

The first FM-06A execution stopped before any architecture graph verdict.

Observed failure:

```text
dependency-cruiser rejected the `shared-core-no-framework` rule itself
because one combined path regular expression was classified as unsafe.
```

Interpretation:

```text
configuration-safety failure
NOT a DANTE architecture violation
NOT a dependency graph failure
NOT a reason to weaken the architecture rule
```

Accepted repair:

```text
replace the single complex framework/node_modules regex
with an array of small independently safe path regexes
covering package specifiers and resolved node_modules paths
```

No hoisting, resolver override, package-layout change or architecture exception is introduced.

## 10B. FM-06A attempt-2 diagnostic record

The second FM-06A execution passed configuration safety, then the current-graph
check reported 151 violations.

The reported paths showed the cause directly:

```text
packages/design-tokens/node_modules/@terrazzo/...
packages/time/node_modules/temporal-polyfill/...
packages/i18n/node_modules/i18next/...
```

The two apparent framework-boundary errors were also inside Terrazzo's own
`node_modules` subtree, not in DANTE shared-package source.

Interpretation:

```text
dependency-cruiser was recursively gathering package-local node_modules because
the package directories themselves were command-line roots
NOT 151 DANTE architecture violations
```

Accepted repair follows dependency-cruiser's documented filter semantics:

```text
doNotFollow.path = 'node_modules'
```

This excludes `node_modules` from the initial root-file gather while still
allowing an external dependency reached from DANTE source to appear as a
dependency boundary node; dependency-cruiser then stops traversal there.

The architecture rules remain unchanged. No dependency is installed, hoisted,
ignored by package name, or granted an exception.

## 11. If the FM-06A script fails

Do NOT blindly rerun from the beginning after it has created files.

Instead:
1. preserve terminal output;
2. inspect the first failing gate only;
3. keep local HEAD at PRE-SCOPE;
4. verify changed paths are only the four authorized paths;
5. fix one variable;
6. rerun the smallest relevant check;
7. update this handoff with the failure and accepted repair before commit.

If dependency-cruiser itself exposes resolution behavior that differs from the expected pnpm/Vite/Metro graph, do not immediately add hoisting or broad resolver overrides.

## 12. What comes after FM-06A PASS

First:
- verify implementation commit on remote;
- update this live handoff to the actual FM-06A commit SHA/status.

Then perform a separate documentation closure gate for the durable docs:
- `docs/workstreams/frontend-materialization.md`
- `docs/development/frontend-local-development.md`
- live handoff update if still needed.

After FM-06A closure:

```text
NEXT = FM-06B generated-source drift enforcement
```

FM-06B should focus on authorities that already generate committed source, especially:
- design-token deterministic generation;
- TanStack route-tree generated source.

Do not mix unit tests, E2E and CI into FM-06B.

## 13. Future queued work after FM-06

```text
FM-07 clean materialization baseline closure
```

Only after FM-06/FM-07 provide the accepted infrastructure baseline should production Access rely on it.

Home design/prototype may continue separately but must not silently become production code.

## 14. Things explicitly still NOT RUN / deferred

Among the carried validation register:

```text
hoisted pnpm fallback                         NOT RUN / not needed
full architecture feature/boundary rules      NOT RUN
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

