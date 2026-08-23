# DANTE Frontend Materialization — LIVE HANDOFF

> TEMPORARY / DISPOSABLE SAVE-GAME.
>
> Keep this file only until the frontend-materialization workstream receives the final hosted-CI proof and the durable docs contain the finished state. Delete it in the separately authorized final cleanup.

## 0. Resume protocol

Read completely, then read:

1. `docs/workstreams/frontend-materialization.md`
2. `docs/development/frontend-local-development.md`
3. `docs/decisions/ADR-008-frontend-engineering-stack.md`
4. `docs/decisions/ADR-009-frontend-architecture-boundaries.md`

Before any repository write:

```bash
git fetch origin feature/frontend-materialization
git rev-parse HEAD
git rev-parse origin/feature/frontend-materialization
git status --short
```

Require remote HEAD to equal the approved PRE-SCOPE. No silent scope expansion.

The commit containing this file cannot embed its own SHA. Resolve the current documentation closure SHA from `origin/feature/frontend-materialization` after the commit lands.

## 1. Repository / branch

```text
repository  MattiaRubino/dante
worktree    /home/mattia/projects/dante-frontend
branch      feature/frontend-materialization
opening     ff46eb16b971b1fde96eef9047b09faa02e1a5db
```

Hard invariants:

```text
ONE authoritative Git history
WSL-backed source/worktrees
NO divergent Windows clone
NO cross-OS shared node_modules
NO direct main work
NO unscoped merge/rebase main into this branch
```

## 2. Current checkpoint

Last implementation/CI commit before FM-07 repair:

```text
31deffddd35f69d48bee82465e0385e508c42876
ci: materialize frontend validation workflow
```

FM-07 clean-materialization source/repair commit:

```text
e79beadbddcf401d1d20c483c2d15d0b3cce96ad
chore: ignore Turborepo local cache
```

Current state:

```text
FM-06A dependency architecture enforcement     PASS
FM-06B generated-source drift enforcement      PASS
FM-06C real unit-test baseline                  PASS
FM-06D Web E2E + Mobile bundle smoke            PASS
FM-06E GitHub-hosted CI orchestration           PASS
FM-06                                             COMPLETE
FM-07 clean materialization baseline            PASS
FRONTEND MATERIALIZATION                         TECHNICALLY COMPLETE
FINAL HOSTED-CI PROOF                            PENDING FOR THIS DOC CLOSURE
FINAL TEMPORARY CLEANUP                          NOT YET RUN
```

## 3. Completed implementation checkpoints

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
FM-07 repair/source e79beadbddcf401d1d20c483c2d15d0b3cce96ad
```

Known durable closures:

```text
FM-05A closure       d4d99b157bab9e00c4f0285bf82745e73a9c944d
FM-05B closure       098be4c815eb724c32f49c277b058e85df81e03a
FM-05C closure       61d19795867e13818a2d43252906b565d23e96e5
FM-06A closure       b57709b4ce073ec179b4e55dc6dda72f509641a4
FM-06B closure       ae0ff9e9849ff3aedcd095a645750993297c4384
FM-06D closure       a481e24936c745c3573077a464a2af8a24794d1b
FM-06E/FM-06 closure 8ec088f0fce1db1e6116fa15acc2302981616ac5
```

Resolve FM-07 documentation closure from the current branch HEAD after this commit lands.

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
Expo                        57.0.9 specifier / 57.0.15 clean resolution
React Native                0.86.2
React                       19.2.3
Expo Router                 57.0.9 specifier / 57.0.15 clean resolution

Shared
i18next                     26.3.6
react-i18next               17.0.11
temporal-polyfill           1.0.4
Terrazzo                    2.7.1
```

## 5. Shared authority model

```text
visible copy / labels / messages / a11y -> @dante/i18n
visual semantic values                  -> @dante/design-tokens
platform control presentation           -> future Web/Mobile design systems
assets                                  -> versioned asset authority
click/workflow behavior                 -> owning feature logic
```

Do not create `@dante/api-client` until real FastAPI OpenAPI exists.

## 6. FM-06 enforcement baseline

```text
FM-06A architecture
pnpm architecture:check
36 modules / 45 dependencies / 0 violations

FM-06B generated drift
pnpm generated:check
packages/design-tokens/generated/web.css
packages/design-tokens/generated/native.ts
apps/web/src/routeTree.gen.ts

FM-06C units
Vitest 4.1.11
@dante/time 5 PASS
@dante/i18n 5 PASS
Turbo 2/2 PASS

FM-06D runtime smoke
Playwright Chromium production-preview E2E 1 PASS
Expo Android Hermes bundle smoke PASS
FM-06D .hbc 4,077,727 bytes

FM-06E hosted CI
Frontend CI #3 SUCCESS
Quality PASS
Web E2E PASS
Mobile Bundle PASS
```

Real emitted check names:

```text
Quality
Web E2E
Mobile Bundle
```

Required checks remain NOT CONFIGURED.

## 7. FM-07 clean materialization — PASS

### Attempt 1

Source:

```text
8ec088f0fce1db1e6116fa15acc2302981616ac5
fresh HTTPS clone
isolated pnpm store
isolated Playwright browser path
```

All functional/build/test gates passed, but final immutability failed because normal Turbo execution created untracked `.turbo/cache/**` files.

Root cause:

```text
expected machine-local Turborepo cache
.gitignore lacked .turbo/
```

Repair:

```text
e79beadbddcf401d1d20c483c2d15d0b3cce96ad
chore: ignore Turborepo local cache
.gitignore -> .turbo/
```

### Clean retest after repair — PASS

Source:

```text
e79beadbddcf401d1d20c483c2d15d0b3cce96ad
NEW fresh HTTPS clone
no node_modules
clean Git state
.turbo ignored
NEW isolated pnpm store
NEW isolated Chromium headless-shell path
```

Evidence:

```text
Node 24.19.0                                      PASS
pnpm 11.22.0                                      PASS
pnpm install --frozen-lockfile                    PASS
lockfile unchanged                                PASS
Expo `expo install --check`                       PASS / Dependencies are up to date
Playwright Linux dependency bootstrap             PASS
format:check                                      PASS
lint                                              PASS
5-package typecheck                               PASS
architecture:check                                PASS / 36 modules / 45 deps / 0 violations
generated:check                                   PASS
@dante/time                                       5 PASS
@dante/i18n                                       5 PASS
Turbo test tasks                                  2/2 PASS
Web Playwright E2E                                1 PASS
Mobile Android Hermes bundle                      PASS
FM-07 .hbc                                        4,077,727 bytes
production build                                  PASS
git diff --check                                  PASS
git diff --exit-code                              PASS
tracked residue                                   0
untracked residue                                 0
```

This is the decisive proof that the current frontend foundation materializes from a clean remote checkout without accumulated repository state.

## 8. Peer diagnostic — final FM-07 classification

Fresh clean install reproduced exactly one warning:

```text
pnpm peers check exit 1
unmet peer react
Installed: 19.2.3
Wanted: ^19.2.8
owner: react-dom@19.2.8
```

Same clean checkout:

```text
Expo `expo install --check` -> Dependencies are up to date
Mobile React               -> 19.2.3
React Native               -> 0.86.2
Expo resolved              -> 57.0.15
Web React/ReactDOM          -> 19.2.8 / 19.2.8
```

Classification:

```text
KNOWN WORKSPACE PEER DIAGNOSTIC
exactly reproducible
NON-BLOCKING for validated Expo/RN baseline
NO React version change justified
```

Do not add peer suppression, `packageExtensions`, `nodeLinker`, hoisting or arbitrary React changes merely to make `pnpm peers check` green.

## 9. Current temporary CI posture

`.github/workflows/frontend-ci.yml` still contains:

```text
pull_request -> main
push -> main
push -> feature/frontend-materialization  TEMPORARY
```

The temporary feature push trigger is retained deliberately so this FM-07 documentation closure itself receives a final real hosted-CI run.

The LIVE HANDOFF is also retained deliberately until that run is verified.

## 10. NEXT — exact resume point

After this documentation closure commit lands:

```text
1. observe the new Frontend CI run on feature/frontend-materialization
2. require overall SUCCESS
3. require jobs:
   Quality PASS
   Web E2E PASS
   Mobile Bundle PASS
4. if failure: inspect first red job/step only; do not perform random repairs
5. if green: open a separately scoped final cleanup gate
```

Expected final cleanup scope after green CI:

```text
UPDATE
.github/workflows/frontend-ci.yml
  remove temporary push -> feature/frontend-materialization

DELETE
docs/workstreams/frontend-materialization-live-handoff.md

UPDATE
final durable workstream/runbook wording if needed
```

Then prepare integration/PR to `main` as a separate governed scope.

## 11. Still deferred / NOT RUN

```text
required branch checks / branch protection mutation
Firefox/WebKit automated E2E
product Access/Home implementation
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
main synchronization
```
