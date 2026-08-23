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

Then verify the live branch before any write:

```bash
git fetch origin feature/frontend-materialization
git rev-parse HEAD
git rev-parse origin/feature/frontend-materialization
git status --short
```

The documentation-closure commit containing this file is self-referential and therefore cannot embed its own Git SHA without requiring another commit. Resolve the exact current documentation HEAD from `origin/feature/frontend-materialization`. The last directly validated implementation SHA is recorded below.

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

Opening base:

```text
ff46eb16b971b1fde96eef9047b09faa02e1a5db
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

Do not merge/rebase `main` into this branch unless separately scoped.

## 2. Current checkpoint

Last directly validated implementation commit:

```text
362b95a415ac7845260daf19cc99547501151eaa
build: enforce generated-source drift
```

State represented by this handoff:

```text
FM-06A DEPENDENCY ARCHITECTURE ENFORCEMENT — PASS
FM-06B GENERATED-SOURCE DRIFT ENFORCEMENT — PASS
FM-06 IN PROGRESS
NEXT = FM-06C UNIT-TEST BASELINE
```

The exact documentation-closure SHA is the current branch HEAD containing this file. Resolve it from the branch instead of trusting a pasted SHA.

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

Windows Firefox ↔ WSL Vite runtime directly validated.

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

Package/tooling:

```text
@dante/design-tokens
Terrazzo 2.7.1
DTCG 2025.10
```

Initial real shared semantics:

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

Strict selector typing/runtime enabled.

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

Documentation closure:

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

Locale and timezone are separate concerns:

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

This is observed evidence, not a permanent performance budget.

FM-05 is COMPLETE.

### FM-06A dependency architecture enforcement — PASS

Implementation:

```text
38dbbd3efb764a8419f4498d27a2e29a3602fc5d
build: enforce frontend dependency architecture
```

Tooling:

```text
dependency-cruiser 18.2.0
dependency-cruiser.config.mjs
pnpm architecture:check
```

Current real graph:

```text
33 modules
40 dependencies cruised
0 enforced violations
```

Current executable boundaries:

```text
unresolvable production frontend source imports forbidden
source dependency cycles forbidden
Web -> Mobile forbidden
Mobile -> Web forbidden
shared packages -> apps forbidden
production frontend -> prototypes forbidden
shared core -> React / React DOM / React Native / react-i18next / Expo / Vite forbidden
```

Negative probes rejected by the intended rules:

```text
Web -> Mobile
Mobile -> Web
shared package -> app
source cycle
shared core -> React
```

Package-surface probes:

```text
@dante/design-tokens/native public PASS
@dante/design-tokens/web.css public PASS
@dante/i18n public PASS
@dante/time public PASS
representative forbidden deep imports rejected PASS
```

Regression after probes:

```text
5-package typecheck PASS
lint PASS
format PASS
Web build PASS
frozen install PASS
git diff --check PASS
4 implementation paths / 0 unexpected
remote readback PASS
```

FM-06A explicitly does NOT yet claim feature-to-feature, route-to-feature, `ui/` or `platform/` enforcement because those real structures do not yet exist.

### FM-06B generated-source drift enforcement — PASS

Implementation:

```text
362b95a415ac7845260daf19cc99547501151eaa
build: enforce generated-source drift
```

Root command and implementation:

```text
pnpm generated:check
tooling/check-generated.mjs
```

Checked committed generated authorities:

```text
packages/design-tokens/generated/web.css
packages/design-tokens/generated/native.ts
apps/web/src/routeTree.gen.ts
```

Generation ownership:

```text
DTCG token source -> Terrazzo 2.7.1 -> Web CSS + Native TypeScript
Web route source -> TanStack Router Vite plugin -> routeTree.gen.ts
```

No new package dependency and no alternate TanStack CLI were added.

Checker behavior:

```text
snapshot current generated bytes
run real generators
compare regenerated bytes
report exact drifted paths
restore pre-check bytes in all cases
clean/current -> exit 0
drift -> non-zero
```

Direct evidence:

```text
clean generated:check PASS
deliberate token generated drift REJECTED / PASS
deliberate routeTree generated drift REJECTED / PASS
pre-check byte restoration PASS
second clean generated:check PASS
architecture:check PASS
33 modules / 40 dependencies / 0 violations
5-package typecheck PASS
lint PASS
format PASS
Web production build PASS
frozen install PASS
git diff --check PASS
3 implementation paths / 0 unexpected
remote readback PASS
```

FM-06B diagnostics retained:

```text
attempt 1
functional generated checks PASS
root lint then rejected implicit process/console globals in the new .mjs checker
-> bounded repair: explicit import from node:process + stdout/stderr writes
-> no repository-wide Node globals added to ESLint

repair attempt
text replacement failed to eliminate every console.* occurrence
-> script stopped before commit
-> still-uncommitted checker rewritten deterministically as a complete file
```

No browser, Android emulator, Metro or Expo Go runtime validation was required for FM-06B because application runtime code did not change. The Web generation path was exercised headlessly through the real Vite build.

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
FM-06A dependency architecture + cycle enforcement    PASS
FM-06B generated-source drift enforcement             PASS
FM-06C unit-test baseline                              NEXT
FM-06D Web E2E + Mobile bundle smoke                   NOT RUN
FM-06E CI orchestration after local checks are real    NOT RUN
```

Do not create a giant enforcement commit.

Do not enforce feature/ui/platform rules before those real structures exist.

## 9. LAST CLOSED SLICE — FM-06B

Final state:

```text
PASS
COMMITTED
PUSHED
REMOTE READBACK PASS
```

Implementation commit:

```text
362b95a415ac7845260daf19cc99547501151eaa
build: enforce generated-source drift
```

Exact implementation gate:

```text
BRANCH
feature/frontend-materialization

PRE-SCOPE
b57709b4ce073ec179b4e55dc6dda72f509641a4

CREATE
tooling/check-generated.mjs

UPDATE
package.json
docs/workstreams/frontend-materialization-live-handoff.md

DELETE
none
```

Result:

```text
3 authorized paths
0 unexpected paths
commit 362b95a415ac7845260daf19cc99547501151eaa
```

FM-06B verifies only the generated authorities that exist today. It does not invent future generators.

## 10. Historical FM-06A diagnostics

Attempt 1:

```text
dependency-cruiser rejected the combined shared-core framework regex as unsafe
-> replaced by atomic safe path regexes
```

This was configuration safety failure before graph analysis, not a DANTE architecture violation.

Attempt 2:

```text
package directories were command-line roots
-> package-local node_modules were gathered
-> 151 third-party/internal violations appeared
-> doNotFollow.path = node_modules
```

The repair preserves the external dependency boundary while stopping traversal into dependency internals. No hoisting, resolver weakening or package exception was introduced.

## 11. Historical FM-06B diagnostics

Attempt 1:

```text
clean generated check PASS
token drift probe PASS
routeTree drift probe PASS
architecture/typecheck PASS
lint FAIL on process/console no-undef in tooling/check-generated.mjs
```

Cause:

```text
new Node checker used implicit Node/global bindings
while repository JS lint intentionally had no broad Node-global declaration
```

Accepted repair:

```text
import process from node:process
use process.stdout/process.stderr
no ESLint config expansion
```

Repair-attempt stop:

```text
textual patch did not remove every console.* occurrence
-> no commit occurred
-> checker rewritten completely and deterministically
```

Final run passed all gates and remote readback.

## 12. Live handoff maintenance rule

After every substantive slice or meaningful failure:

1. update the exact validated implementation SHA;
2. record PASS / FAIL / NOT RUN accurately;
3. record diagnostic failures and accepted repair when they are reusable knowledge;
4. record the exact next slice and its boundaries;
5. keep prior durable decisions intact;
6. never rely on chat history alone.

For a documentation commit that updates this file, do not attempt to embed that commit's own SHA in the same commit. Record the implementation SHA and resolve the documentation HEAD from the branch.

## 13. CURRENT SLICE — FM-06C UNIT-TEST BASELINE

Status:

```text
NEXT / READ-ONLY TECHNOLOGY + TEST-SCOPE DESIGN REQUIRED BEFORE WRITE GATE
```

Objective:

```text
make root `pnpm test` meaningful with real assertions against actual DANTE semantics
```

Strong first real candidates:

```text
@dante/time
- Instant / ZonedDateTime conversion
- Europe/Rome DST behavior
- round-trip semantics
- duration arithmetic

@dante/i18n
- supported locale contract
- Italian default/fallback semantics
- IT/EN resource shape/runtime behavior
```

Do NOT create dummy tests merely so Turbo reports green.

FM-06C should prefer framework-free unit coverage first. Do not pull DOM/component libraries into the repository until real component tests justify them.

Version-sensitive test tooling must be reverified at materialization time. Vitest is a strong candidate from earlier discovery, but its exact current stable version is NOT fixed by this handoff and must be checked again immediately before the FM-06C write gate.

Do not mix into FM-06C:

```text
Playwright / Web E2E
Mobile bundle smoke
GitHub Actions
product UI
Access/Home
PowerSync
backend contracts
main synchronization
```

## 14. Future queued work

After FM-06C:

```text
FM-06D Web E2E + Mobile bundle smoke
FM-06E CI orchestration after local checks are real
FM-07 clean materialization baseline closure
```

Only after FM-06/FM-07 provide the accepted infrastructure baseline should production Access rely on it.

Home design/prototype may continue separately but must not silently become production code.

## 15. Things explicitly still NOT RUN / deferred

```text
hoisted pnpm fallback                         NOT RUN / not needed
feature-specific architecture rules           NOT RUN
unit-test baseline                            NOT RUN — NEXT FM-06C
Web E2E                                       NOT RUN
Mobile bundle smoke                           NOT RUN
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
