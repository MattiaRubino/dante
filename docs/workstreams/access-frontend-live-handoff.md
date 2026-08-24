# DANTE Access frontend — live handoff

**Status:** ACTIVE operational handoff  
**Date:** 2026-08-24  
**Branch:** `feature/access-frontend`  
**Frontend worktree:** `/home/mattia/projects/dante-frontend`  
**Backend/logical-PostgreSQL worktree:** `/home/mattia/projects/dante`  
**WSL distro:** `Ubuntu-24.04`

This file is the first continuity read for any new chat/agent/session continuing Access frontend work. Repository truth and current branch HEAD override remembered chat state.

## 1. Mandatory startup sequence

Before proposing or writing changes:

1. open/read this handoff;
2. read `docs/workstreams/access-frontend.md`;
3. read the product authorities on `prototype/access-system` when semantic/security questions arise:
   - `prototypes/frontend/access/README.md`
   - `docs/frontend/access/current-checkpoint.md`
   - `docs/frontend/access/contract.md`
   - `docs/frontend/access/state-model.md`
   - `docs/frontend/access/benchmark-2026-08-20.md`;
4. fresh-read `feature/access-frontend` HEAD;
5. compare the expected base SHA with the branch immediately before the first write;
6. state an explicit bounded write gate (paths + intent + exclusions);
7. after writes, compare/read back exact changed paths;
8. do not merge to `main` without a separate explicit merge gate.

Never rebase/force-push/rewrite history unless explicitly authorized.

## 2. Worktree rule — critical

```text
/home/mattia/projects/dante
→ backend / logical→PostgreSQL work

/home/mattia/projects/dante-frontend
→ permanent frontend worktree
→ feature/access-frontend (or future frontend feature branch)
```

**A new frontend branch does not mean a new frontend directory.** Switch frontend branches inside `/home/mattia/projects/dante-frontend`.

## 3. User/assistant operating workflow

Preferred workflow:

1. assistant fresh-checks branch HEAD and declares bounded scope;
2. assistant modifies GitHub branch remotely when safe/available;
3. assistant readbacks/compares the remote delta;
4. assistant gives one downloadable `.sh` only for pull/format/QA/screenshot tasks;
5. user runs it from WSL, usually from Windows Downloads:
   `bash /mnt/c/Users/mtaru/Downloads/<script>.sh`;
6. user reviews code/diff in WebStorm and the running UI in the browser;
7. assistant reviews QA output/screenshot before any final formatting commit/push or merge gate.

Do not make the user manually patch source files when the assistant can safely write the repo itself. Scripts must not silently commit/push unless that is the explicitly approved purpose.

## 4. Local frontend developer environment

WebStorm is the primary frontend IDE. The repository is opened directly from WSL, not cloned again onto Windows:

```text
\\wsl.localhost\Ubuntu-24.04\home\mattia\projects\dante-frontend
```

Stable runtime paths:

```text
Node 24.19.0
/home/mattia/.local/share/fnm/node-versions/v24.19.0/installation/bin/node

pnpm 11.22.0
/home/mattia/.local/share/pnpm/bin/pnpm

TypeScript 6.0.3
project node_modules/typescript
```

Web dev command:

```bash
pnpm --filter @dante/web dev
```

Expected Vite URL:

```text
http://localhost:5173/
```

User should be able to inspect Project tree, Git Log/diff, Problems, editor and terminal in WebStorm while Vite updates the browser live.

## 5. Access product authority

Access purpose:

> Get an unauthenticated person to an authenticated DANTE session and, for a new account, through the smallest useful first-run handoff.

Key invariants:

```text
Person != Account != Principal != Actor
sign-in != external-integration authorization
provider state != canonical DANTE state
provider authentication != permission to read provider data
verification != profile setup
reauthentication != initial sign-in
client integrity != person identity
```

Google/Apple sign-in authenticates DANTE only; it never implicitly authorizes Gmail, Calendar, iCloud or other provider data.

Desktop visual authority is A3.4. Mobile authority is M1.2 + PRG-0. Production migrates semantic states/behavior/security/locales; it must not mechanically copy the prototype DOM.

## 6. Current frontend architecture

Web: React DOM + Vite + TanStack Router.  
Mobile: React Native + Expo + Expo Router.

Feature-first boundary:

```text
features/<feature>/
├── index.ts
├── model/   only when justified
├── data/    only when justified
└── ui/
```

Routes import feature public APIs only. No Web↔Mobile private imports. No shared→apps. No production→prototypes. No empty `model`/`data` directories.

Current shared packages include:

- `@dante/design-tokens`
- `@dante/i18n`
- `@dante/time`

Do not create `@dante/api-client` before a real stable FastAPI OpenAPI contract exists. Do not create a generic `Repository<T>` abstraction. PowerSync only enters when the first real offline vertical is activated.

## 7. Current Access implementation checkpoint

The branch has completed the AF-01A/AF-01C production shell/foundation work and is currently closing **AF-01D — shell completion / professional polish**.

Current production UI includes:

- full warm desktop canvas with open left brand stage;
- locked DANTE symbol + wordmark topbar;
- separate rounded/shadowed Access card;
- responsive narrow/mobile Web composition;
- Google/Apple visual affordances only (real provider execution intentionally absent);
- email/current-password controls;
- professional IT/EN selector with browser fallback and persisted preference;
- Testing Library, Playwright and axe coverage;
- architecture/design-token/generated-output gates.

AF-01D delta includes:

- production Italian hero headline localized (`Comprendi la vita. / Dai forma a ciò che viene dopo.`); immutable prototype evidence is not rewritten;
- dynamic `<html lang>` following IT/EN;
- localized email placeholder and show/hide password labels;
- real local password visibility toggle;
- hardened locale popover focus/Escape/keyboard semantics;
- expanded unit/E2E coverage;
- workstream/handoff documentation update.

**AF-01D is not accepted until fresh local QA and visual review pass.**

## 8. Deliberately inactive / not fake

Do not pretend these exist before their actual boundary:

- credential submission/auth result;
- backend session establishment;
- Google/Apple transaction/callback;
- recovery proof;
- verification backend challenge;
- account linking mutation;
- authenticated Home return;
- final Terms/Privacy legal content/destinations.

The current Terms/Privacy controls must not be called production-complete until real legal destinations/content exist. Do not invent broken/fake routes simply to satisfy appearance.

## 9. Password/security contract

DANTE V1 password policy:

```text
minimum                    12 characters
support                    >=64 characters
mandatory composition      none
paste/password manager     allowed
show/hide                   allowed
common/breached blocklist  required server-side
```

Never log/persist raw password, OTP, recovery proof, auth code, PKCE verifier, access/refresh/session secret or provider token/assertion.

Production Access must ultimately cover credential stuffing/brute force, enumeration, recovery abuse, provider transaction attacks, replay, account-link takeover and session hijack. Backend remains authoritative for session state.

## 10. Approved semantic state graph

```text
SIGN_IN
├─ provider → PROVIDER_PENDING → AUTHENTICATED_RETURN | PROVIDER_ERROR | ACCOUNT_LINK
├─ email/password → AUTHENTICATED_RETURN
├─ create account → SIGN_UP_EMAIL
└─ forgot password → FORGOT_PASSWORD

SIGN_UP_EMAIL
→ SIGN_UP_PASSWORD
→ VERIFY_EMAIL
→ SETUP_NAME
→ SETUP_LOCALE
→ SETUP_START
   ├─ FIRST_ACTION → HOME_HANDOFF
   ├─ IMPORT → HOME_HANDOFF
   ├─ DEMO → HOME_HANDOFF
   └─ skip → HOME_HANDOFF

FORGOT_PASSWORD
→ RECOVERY_SENT
→ recovery proof/link
→ RESET_PASSWORD
→ RESET_COMPLETE
→ SIGN_IN

SESSION_EXPIRED / SECURITY_REAUTH_REQUIRED
→ REAUTH
→ success: restore only safe valid context
→ cancel/cannot continue: SIGN_IN
```

Orthogonal conditions include OFFLINE/REACHABILITY_FAILURE, REQUEST_IN_FLIGHT, RATE_LIMITED and SERVER_UNAVAILABLE; they do not become fake credential states.

## 11. QA gates

Normal frontend gate set:

```bash
pnpm format:check
pnpm lint
pnpm typecheck
pnpm architecture:check
pnpm generated:check
pnpm test
pnpm --filter @dante/web build
pnpm --filter @dante/web test:e2e
git diff --check
```

Visual review must include at least desktop 1536×864 plus narrow and phone behavior. Do not declare visual PASS merely because the page renders; compare composition against the accepted authority and current approved production adjustments.

## 12. Mandatory stop before mock/AF-02 integration

**Do not automatically begin a mock Access adapter after AF-01D.**

When AF-01D passes:

1. STOP;
2. inspect current backend branches/workstreams/repository truth;
3. determine whether real Auth + stable API/OpenAPI is now ready enough for frontend integration;
4. if yes, skip the mock and design the real typed integration boundary;
5. if no, only then consider the thin deterministic temporary adapter described by AF-02.

The user may be working on backend in parallel and expects this readiness check before any mock work.

## 13. Next immediate action

At handoff creation, implementation writes have been made remotely for AF-01D but local QA has not yet been run against them.

Next session should:

1. fresh-read `feature/access-frontend` HEAD;
2. compare the AF-01D delta from base `c63e2828cc69bd2eef8df2c4765e7b2ed328dae7`;
3. give the user one safe pull/Prettier/full-QA/screenshot script that tolerates only expected local Prettier residue;
4. inspect output and screenshot;
5. if failures exist, assistant fixes remote first, then supplies a new pull/QA script;
6. only after QA + visual acceptance, commit/push any local Prettier-only delta with a strict whitelist;
7. STOP before mock and inspect backend readiness.
