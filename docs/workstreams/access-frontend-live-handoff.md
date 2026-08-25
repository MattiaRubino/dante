# DANTE Access frontend — live handoff

**Status:** AF-02A PASS / AF-02B NEXT  
**Date:** 2026-08-25  
**Branch:** `feature/access-frontend`  
**AF-01D final synchronized checkpoint SHA:** `236d97931b56f1ebd13fb04fedf623138e895743`  
**AF-02A accepted code checkpoint before docs closure:** `0ba0c5f7012c6b7bd312f5a1ff727a9b764b0d4f`  
**Frontend worktree:** `/home/mattia/projects/dante-frontend`  
**Backend/logical-PostgreSQL worktree:** `/home/mattia/projects/dante`  
**WSL distro:** `Ubuntu-24.04`

This file is the first continuity read for any new chat/agent/session continuing Access frontend work. Repository truth and current branch HEAD override remembered chat state.

## 1. Mandatory startup sequence

Before proposing or writing changes:

1. read this handoff;
2. read `docs/workstreams/access-frontend.md`;
3. use the approved product authorities on `prototype/access-system` for semantic/security questions:
   - `prototypes/frontend/access/README.md`
   - `docs/frontend/access/current-checkpoint.md`
   - `docs/frontend/access/contract.md`
   - `docs/frontend/access/state-model.md`
   - `docs/frontend/access/benchmark-2026-08-20.md`;
4. fresh-read `feature/access-frontend` HEAD;
5. compare the expected base SHA immediately before the first write;
6. state a bounded write gate;
7. read back/compare exact changed paths;
8. never merge to `main` without a separate explicit merge gate.

Never rebase/force-push/rewrite history unless explicitly authorized.

## 2. Worktree rule — critical

```text
/home/mattia/projects/dante
→ backend / logical→PostgreSQL work

/home/mattia/projects/dante-frontend
→ permanent frontend worktree
→ feature/access-frontend (or future frontend feature branch)
```

A new frontend feature branch does **not** create a new frontend directory.

## 3. User/assistant workflow

Preferred workflow:

1. assistant fresh-checks branch HEAD and declares scope;
2. assistant modifies GitHub remotely when safe/available;
3. assistant readbacks/compares the remote delta;
4. assistant gives one downloadable `.sh` for pull/format/QA/screenshot;
5. user runs it from WSL, normally:
   `bash /mnt/c/Users/mtaru/Downloads/<script>.sh`;
6. user reviews in WebStorm/browser;
7. assistant reviews QA output/screenshots before any final formatting push or merge gate.

Do not make the user manually patch source files when the assistant can safely write the branch itself.

## 4. Stable frontend environment

```text
Node 24.19.0
pnpm 11.22.0
TypeScript 6.0.3
Web: React 19.2.8 + Vite 8.2.1 + TanStack Router
```

Web dev:

```bash
cd /home/mattia/projects/dante-frontend
pnpm --filter @dante/web dev
```

Expected URL:

```text
http://localhost:5173/
```

WebStorm is the preferred frontend IDE for this worktree. The user now has live Vite/browser feedback plus Git Log/diff visibility.

## 5. Product authority / invariants

Access purpose:

> Get an unauthenticated person to an authenticated DANTE session and, for a new account, through the smallest useful first-run handoff.

```text
Person != Account != Principal != Actor
sign-in != external-integration authorization
provider state != canonical DANTE state
provider authentication != permission to read provider data
verification != profile setup
reauthentication != initial sign-in
client integrity != person identity
```

Google/Apple Access authenticates DANTE only; it never implicitly authorizes Gmail, Calendar, iCloud or unrelated provider data.

Desktop visual authority is A3.4. Mobile authority is M1.2 + PRG-0.

## 6. AF-01D accepted checkpoint

AF-01D is PASS and synchronized at:

```text
236d97931b56f1ebd13fb04fedf623138e895743
```

Accepted Web shell includes:

- full warm desktop canvas;
- open left brand stage + muted Living Orbits;
- locked DANTE symbol/wordmark topbar;
- separate rounded/shadowed Access card;
- IT/EN selector with browser fallback + persistence;
- synchronized `<html lang>`;
- responsive narrow/phone composition;
- working local show/hide password;
- Testing Library / Playwright / axe / architecture gates.

Final hero copy:

```text
IT
Comprendi la vita.
Dai forma al prossimo passo.

EN
Understand life.
Shape what comes next.
```

Do not regress this shell while advancing the flow.

## 7. AF-02A — accepted pre-backend flow checkpoint

AF-02A is **PASS** after local QA, E2E and visual review on 2026-08-25.

Accepted code checkpoint before documentation-only closure commits:

```text
0ba0c5f7012c6b7bd312f5a1ff727a9b764b0d4f
```

The user explicitly asked to continue to the most advanced useful frontend point while backend Auth is still being built, **without using a fake/mock authentication service**.

### State/model

`apps/web/src/features/access/model/access-flow.ts`

Materializes the approved semantic graph:

```text
SIGN_IN
SIGN_UP_EMAIL
SIGN_UP_PASSWORD
VERIFY_EMAIL
FORGOT_PASSWORD
RECOVERY_SENT
RESET_PASSWORD
RESET_COMPLETE
PROVIDER_PENDING
PROVIDER_ERROR
ACCOUNT_LINK
AUTHENTICATED_RETURN
REAUTH
SETUP_NAME
SETUP_LOCALE
SETUP_START
FIRST_ACTION
IMPORT
DEMO
HOME_HANDOFF
```

Orthogonal conditions:

```text
idle
backend-required
offline
server-unavailable
rate-limited
```

The reducer exposes server-owned events for future real integration, but production UI cannot dispatch fake successful backend outcomes.

### Safety rule

```text
frontend-owned transition
→ can happen locally

backend-authoritative transition
→ stay on current safe canonical state
→ condition = BACKEND_REQUIRED
→ never fabricate success
```

Examples:

```text
SIGN_IN → SIGN_UP_EMAIL                     local
SIGN_UP_EMAIL → SIGN_UP_PASSWORD            local
SIGN_UP_PASSWORD submit → BACKEND_REQUIRED  not fake VERIFY_EMAIL
FORGOT_PASSWORD submit → BACKEND_REQUIRED   not fake RECOVERY_SENT
provider click → BACKEND_REQUIRED           not fake PROVIDER_PENDING
```

### Accepted UI and behavior

- SignIn with local form validation and callbacks;
- signup email/password;
- forgot-password entry;
- password manager/paste-safe password behavior;
- browser online/offline transport condition;
- IT/EN resources for the complete approved screen inventory;
- desktop and phone signup visual acceptance;
- recovery visual acceptance;
- provider signup wording uses `Continue/Continua with` semantics rather than claiming account creation before backend authority;
- neutral recovery copy does not leak account existence;
- `backend-required` remains an internal state and is **not** rendered as technical text to the user;
- Terms/Privacy remain non-interactive placeholders until real legal destinations exist.

### AF-02A QA

Passed before acceptance:

```text
Prettier / format check
ESLint
TypeScript
architecture check
generated-output check
unit tests
Web build
Playwright E2E
git diff --check
visual desktop review
visual 390px phone review
```

Do not regress AF-02A while hardening downstream states.

## 8. Current backend readiness

Backend readiness was inspected on `feature/logical-postgresql` after AF-01D.

Observed:

- FastAPI/bootstrap exists;
- PostgreSQL runtime/config/provisioning/migrations exist;
- DB/persistence tests are active;
- app factory exposes `/health/live` and `/health/ready`;
- no Access Auth/session/OAuth/recovery/account-link route/domain surface yet;
- no stable Access OpenAPI yet.

Verdict:

```text
PostgreSQL/persistence foundation       ACTIVE / ADVANCED
real Access Auth API                    NOT READY
stable Access OpenAPI                   NOT READY
AF-03 real frontend integration         WAIT
```

The user is continuing backend work in parallel.

## 9. AF-02B — next safe frontend batch

Goal: harden every downstream Access surface that can be made production-ready without inventing backend outcomes.

Target inventory:

```text
VERIFY_EMAIL
RECOVERY_SENT
RESET_PASSWORD
RESET_COMPLETE
PROVIDER_PENDING
PROVIDER_ERROR
ACCOUNT_LINK
AUTHENTICATED_RETURN
REAUTH
SETUP_NAME
SETUP_LOCALE
SETUP_START
FIRST_ACTION
IMPORT
DEMO
HOME_HANDOFF
```

Required AF-02B work:

- verify-email local validation/accessibility;
- reset-password confirmation/visibility/local validation;
- provider pending/error/link visual semantics;
- reauth form behavior without fake session success;
- setup name validation;
- locale/timezone confirmation UI;
- first-run choice accessibility and responsive polish;
- first-action/import/demo/Home-handoff production copy/semantics;
- IT/EN parity;
- desktop/phone screenshots;
- reducer/unit/E2E coverage where frontend-owned;
- reducer/server-event fixtures may test downstream rendering, but no fake service or production fake-success control may be introduced.

AF-02B must stop at backend-authoritative transitions exactly as AF-02A does.

## 10. Deliberately absent / never fake

Still absent until the real backend exists:

- credential authentication result;
- account creation mutation;
- backend session establishment/bootstrap;
- Google/Apple real transaction/callback;
- verification proof validation;
- recovery proof validation;
- account-link mutation;
- backend rate-limit timing;
- generated OpenAPI/Orval Access client;
- TanStack Query remote-auth integration;
- canonical authenticated Home routing;
- final Terms/Privacy destinations/content.

Do not create fake routes, fake tokens, fake provider success or fake session state.

## 11. Form/security boundary

Current pre-backend forms use local controlled state and small pure validation only. Passwords/codes are component-local and are not stored in the global reducer or persisted.

Password V1:

```text
minimum                    12 characters
support                    >=64 characters
mandatory composition      none
paste/password manager     allowed
show/hide                   allowed
common/breached blocklist  required server-side
```

Never log/persist raw password, OTP, recovery proof, auth code, PKCE verifier, access/refresh/session secret or provider token/assertion.

TanStack Form + Zod should be bound to the real DTO/error contract when stable Auth OpenAPI exists; do not invent a parallel fake server schema now.

## 12. QA gates

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

Visual QA for AF-02B must include representative desktop and 390px phone downstream surfaces. Do not call a batch PASS merely because it compiles.

## 13. Real integration boundary

When backend Auth becomes sufficiently ready:

```text
FastAPI Auth + stable OpenAPI
→ generated typed API client
→ real remote state/query boundary
→ real form/schema binding
→ provider/session/recovery integration
→ authenticated Home handoff
→ full-stack E2E
```

Server-owned events already exist in the reducer, so AF-03 should wire real responses into the existing graph rather than redesign Access.

## 14. Merge discipline

No merge to protected `main` is authorized by this handoff. Merge is a separate explicit gate after QA/review.

Never rebase/force-push/rewrite history. Never merge solely because GitHub says mergeable.
