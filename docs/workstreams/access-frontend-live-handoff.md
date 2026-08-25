# DANTE Access frontend — live handoff

**Status:** PARKED AT AF-01D PASS / BACKEND-AUTH GATE  
**Date:** 2026-08-25  
**Branch:** `feature/access-frontend`  
**AF-01D accepted implementation SHA:** `d2a9017cd2c1c546a163fdaf87dd3a708cb64f59`  
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

The user should be able to inspect Project tree, Git Log/diff, Problems, editor and terminal in WebStorm while Vite updates the browser live. `.sh` scripts are QA/automation tools, not the user's only visibility into the frontend.

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

## 7. Current Access implementation checkpoint — AF-01D PASS

AF-01A/AF-01C/AF-01D Web shell/foundation work is complete and accepted.

Accepted production UI includes:

- full warm desktop canvas with open/full-area left brand stage;
- locked DANTE symbol + wordmark topbar;
- separate rounded/shadowed Access card;
- large muted Living Orbits treatment;
- responsive narrow/mobile Web composition;
- compact professional IT/EN selector;
- browser locale fallback and persisted preference;
- `html lang` synchronized with active locale;
- localized email placeholder and password-visibility labels;
- working local show/hide-password control;
- Google/Apple visual affordances only (real provider execution intentionally absent);
- Testing Library, Playwright and axe coverage;
- architecture/design-token/generated-output gates.

Final hero copy:

```text
IT
Comprendi la vita.
Dai forma al prossimo passo.

EN
Understand life.
Shape what comes next.
```

Italian desktop typography has an explicit locale-aware scale adjustment so the longer language preserves the intended visual hierarchy without changing the English composition.

The user visually accepted the final IT composition on 2026-08-25. The final screenshot was produced only after the QA script reached its post-QA preview/screenshot stage.

## 8. QA gates

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

The AF-01D scripts ran these gates before generating the accepted final screenshots. Future continuation must rerun the relevant gates after any new change.

Visual review includes desktop 1536×864 plus narrow and phone behavior. Do not declare visual PASS merely because the page renders.

## 9. Deliberately inactive / not fake

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

## 10. Password/security contract

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

## 11. Approved semantic state graph

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

## 12. Backend-readiness inspection — 2026-08-25

The mandatory stop/check was performed against current repository truth on `feature/logical-postgresql`.

Observed backend state:

- FastAPI application/bootstrap exists;
- PostgreSQL runtime/config/provisioning and migration foundation exists;
- persistence/database testing is active;
- current FastAPI application factory exposes `/health/live` and `/health/ready`;
- no production Access Auth route/domain surface is present in the current backend tree;
- no stable login/signup/verify/recovery/session/provider/account-link OpenAPI contract exists yet.

Verdict:

```text
AF-01D frontend shell                     PASS
backend persistence/PostgreSQL foundation ACTIVE / ADVANCED
backend Access Auth API                    NOT READY
stable Access OpenAPI                      NOT READY
real frontend Auth integration             WAIT
```

This is not a backend failure; Auth is simply outside the currently materialized backend boundary.

## 13. Mandatory stop before mock / real integration

**STOP HERE. Do not automatically begin AF-02 mock work.**

The user is continuing backend work in parallel. On the next explicit frontend continuation:

1. fresh-read this handoff and `feature/access-frontend` HEAD;
2. fresh-inspect backend branch/workstream truth;
3. determine whether Auth/session/provider/recovery API + stable OpenAPI now exist;
4. if yes, skip the temporary adapter and design the real typed integration boundary;
5. if no, discuss whether a thin deterministic temporary adapter is still worth building before writing it.

Expected alternatives:

```text
BACKEND AUTH READY
FastAPI/OpenAPI
→ Orval/generated @dante/api-client
→ TanStack Query where remote state belongs
→ TanStack Form + Zod for real forms
→ Access state graph
→ full-stack E2E

BACKEND AUTH STILL NOT READY AND MOCK IS USEFUL
React Access
→ thin temporary Access interface
→ deterministic adapter scenarios
→ no fake security semantics
```

Never build the mock merely because it was once planned.

## 14. Merge discipline

No Access merge to protected `main` has been authorized by this checkpoint. Merge remains a separate explicit gate after local/hosted QA and review.

Do not rebase/force-push/rewrite history. Do not merge merely because GitHub reports the branch mergeable.

## 15. Next immediate action

Frontend Access is intentionally parked.

Before any new frontend feature work:

```text
1. sync/close any expected local Prettier residue from the AF-01D QA
2. keep feature/access-frontend as the accepted checkpoint
3. continue backend work independently
4. when returning to Access, re-run backend readiness check
5. choose real integration vs temporary adapter from current repository truth
```

A new chat/session should not reconstruct this state from memory; read this file first.
