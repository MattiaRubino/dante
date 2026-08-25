# DANTE Access frontend — live handoff

**Status:** AF-02B PASS / ACCESS VERTICAL STILL OPEN  
**Date:** 2026-08-25  
**Branch:** `feature/access-frontend`  
**Permanent frontend worktree:** `/home/mattia/projects/dante-frontend`  
**AF-01D synchronized shell checkpoint:** `236d97931b56f1ebd13fb04fedf623138e895743`  
**AF-02A accepted checkpoint:** `0ba0c5f7012c6b7bd312f5a1ff727a9b764b0d4f`  
**AF-02B code/formatting checkpoint:** `c39d1a8312fb2d00bc322604bcd453d13fa2b510`  
**Backend/logical-PostgreSQL worktree:** `/home/mattia/projects/dante`  
**WSL distro:** `Ubuntu-24.04`

This is the mandatory first continuity read for any new chat/agent/session continuing DANTE Access.

Repository truth and a fresh read of the current branch HEAD override chat memory.

---

## 0. Non-negotiable continuity rule

A new chat/session does **not** mean a new feature branch, a new worktree or a reset of the workstream.

Until the user explicitly says otherwise:

```text
continue Access
→ branch: feature/access-frontend
→ worktree: /home/mattia/projects/dante-frontend
→ same Access workstream
→ no merge to main
→ no branch split
→ no new frontend directory
```

The goal is to keep working on Access until the **whole Access vertical is actually production-ready and closed**, not merely until the current UI batch is done.

Do not create `feature/access-*` successors just because AF-02B is PASS. Do not create another worktree for later Access phases.

A branch/worktree/merge change requires an explicit user gate.

---

## 1. Mandatory startup sequence for the next chat

Before proposing or writing changes:

1. read this file completely;
2. read `docs/workstreams/access-frontend.md` completely;
3. read the approved Access authorities as needed:
   - `prototypes/frontend/access/README.md`
   - `docs/frontend/access/current-checkpoint.md`
   - `docs/frontend/access/contract.md`
   - `docs/frontend/access/state-model.md`
   - `docs/frontend/access/benchmark-2026-08-20.md`;
4. fresh-read the current `feature/access-frontend` HEAD;
5. inspect current local/remote divergence before asking the user to run anything;
6. state the exact next batch and a bounded WRITE GATE;
7. immediately before the first write, fresh-check HEAD again;
8. write only allowed paths;
9. read back/compare the exact delta;
10. give the user one `.sh` for pull/format/QA/screenshot when local execution is needed;
11. review QA output and screenshots before calling a batch PASS;
12. never merge to `main` without a separate explicit merge gate.

Never rebase, force-push, move refs backwards or rewrite history unless the user explicitly authorizes it.

### Historical note

After AF-02B formatting checkpoint `c39d1a8312fb2d00bc322604bcd453d13fa2b510`, an accidental `__noop__` file was created and then immediately removed in two ordinary commits. Net repository tree impact is zero. Do **not** try to clean those commits by rebase/force/history rewrite.

---

## 2. Stable worktree rule — critical

```text
/home/mattia/projects/dante
→ backend / logical→PostgreSQL work

/home/mattia/projects/dante-frontend
→ permanent frontend worktree
→ feature/access-frontend until Access closes
```

**NEW CHAT != NEW BRANCH.**  
**NEW ACCESS PHASE != NEW WORKTREE.**

---

## 3. User/assistant operating workflow

Preferred workflow:

1. assistant fresh-checks branch HEAD and declares scope;
2. assistant modifies GitHub remotely when safe/available;
3. assistant readbacks/compares the remote delta;
4. assistant gives one downloadable `.sh` for pull/format/QA/screenshot;
5. user runs it from WSL, normally:
   `bash /mnt/c/Users/mtaru/Downloads/<script>.sh`;
6. user reviews code/diffs in WebStorm and UI in browser;
7. assistant reviews output/screenshots;
8. only then create a formatting/checkpoint commit if needed;
9. merge remains a separate user decision.

Do not make the user manually patch source files when the assistant can safely write them remotely.

Do not use the user’s local WSL as the first parser/linter if the change can be statically sanity-checked first.

When a QA harness fails, diagnose whether the defect is in production code or in the harness/runtime assumptions **before** modifying production code.

---

## 4. Stable frontend environment

```text
Node                  24.19.0
pnpm                  11.22.0
TypeScript            6.0.3
Web                   React 19.2.8 + Vite 8.2.1
Routing               TanStack Router
Unit/component        Vitest + Testing Library
E2E                   Playwright
Accessibility         axe via Playwright
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

WebStorm is the preferred frontend IDE for this worktree.

Known nonblocking peer warning remains: Mobile React 19.2.3 vs Web `react-dom@19.2.8` wanting React `^19.2.8`. Platforms are intentionally isolated. Do not force/hoist/suppress versions casually just to remove the warning.

---

## 5. Product authority and invariants

Access purpose:

> Get an unauthenticated person to an authenticated DANTE session and, for a new account, through the smallest useful first-run handoff.

Canonical invariants:

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

Desktop visual authority: A3.4.  
Mobile authority: M1.2 + PRG-0.

Accepted shell direction:

```text
full warm canvas
+ open left brand stage
+ muted Living Orbits
+ locked DANTE topbar
+ compact locale control
+ separate rounded/shadowed Access card
```

Do not regress this into a hard 50/50 panel split or a generic SaaS login composition.

---

## 6. Current accepted state

### AF-01D — PASS

Accepted shell behavior:

- professional full-canvas composition;
- final hero copy:
  - IT: `Comprendi la vita. / Dai forma al prossimo passo.`
  - EN: `Understand life. / Shape what comes next.`;
- locale-aware hero sizing;
- IT/EN selector with browser fallback + persistence;
- `<html lang>` synchronization;
- localized placeholders/visibility strings;
- working show/hide password;
- desktop/narrow/phone responsive composition;
- Testing Library / Playwright / axe / architecture gates.

### AF-02A — PASS

Accepted pre-backend flow:

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

Safety rule:

```text
frontend-owned transition
→ may happen locally

backend-authoritative transition
→ remain on safe canonical state
→ backend-required internally
→ never fabricate success
```

### AF-02B — PASS

AF-02B hardened downstream surfaces and passed final exhaustive QA on 2026-08-25.

Accepted downstream surfaces:

- verify email;
- recovery sent;
- reset password;
- reset complete;
- provider pending;
- provider error;
- account link;
- authenticated return;
- reauth;
- setup name;
- setup locale/timezone;
- setup start;
- first action;
- import;
- demo;
- Home handoff.

Accepted behavior includes:

- six-digit verification validation;
- accessible inline errors;
- resend/change-email frontend actions;
- two-field password reset validation;
- password-manager/paste-safe behavior;
- working password visibility controls;
- setup-name empty/whitespace validation;
- first-action empty-input validation;
- production-safe provider/link/reauth copy;
- server-owned downstream rendering tested via state fixtures, not fake services;
- backend-required condition never exposed as developer text;
- IT/EN resource parity;
- password-guide contrast corrected to automated WCAG AA expectations;
- real browser offline E2E (`BrowserContext.setOffline`) instead of synthetic race-prone event dispatch.

Final AF-02B QA:

```text
Playwright E2E                  10/10 PASS
Web unit/component              17/17 PASS
workspace typecheck             5/5 PASS
architecture                    PASS
Generated sources               PASS / deterministic
production Web build            PASS
axe all desktop downstream      PASS
axe phone verify/reset/start    PASS
mobile horizontal overflow      390/390 PASS
```

The temporary downstream harness is a QA tool only. Never convert it into a production debug route or production fake-state switch.

---

## 7. ACCESS IS STILL OPEN

Do not interpret `AF-02B PASS` as `Access finished`.

Frontend-owned/pre-backend surfaces are now strong, but production Access still requires real backend integration and final release hardening.

The next chat must continue **on this same branch/worktree** until the remaining applicable closure criteria are satisfied.

---

## 8. Production Quality Bar — mandatory for every future Access change

The user explicitly requires a mature, high-end application standard. Treat every screen as if it may ship to production.

### 8.1 No collage/coupage UI

Never build screens by stitching together unrelated visual patterns from random apps or examples.

Rules:

- one coherent DANTE visual language;
- no random cards/gradients/chips/icons/illustrations just to make a page "look designed";
- no arbitrary per-screen CSS hacks when a reusable semantic rule/component is appropriate;
- new UI patterns must visually belong to the existing Access system;
- whitespace can be intentional — do not fill empty panels with decorative noise;
- do not mimic another big app literally; study mature patterns, then adapt them to DANTE’s product/brand contract;
- visual hierarchy must be intentional at all viewports;
- a screen must not look half-finished merely because its backend action is not yet available.

### 8.2 Production copy only

Never expose:

- `backend required`;
- `frontend ready`;
- debug state names;
- raw server errors;
- developer instructions;
- placeholder legal destinations;
- fake provider/security claims.

User copy must be natural, concise, secure and action-oriented.

IT/EN are transcreated for natural language and equivalent meaning, not mechanically translated word-for-word.

### 8.3 Interaction standard

Every interactive state must consider:

```text
default
hover
focus-visible
pressed/active
disabled
loading
success
validation error
server error
offline
rate limited
server unavailable
cancel/retry where applicable
```

Do not add states that have no valid product meaning merely to appear complete.

Forms must use semantic form behavior where appropriate:

- Enter submits the expected action;
- password manager/autofill works;
- paste works where security policy permits it;
- browser autocomplete attributes are correct;
- double-submit is prevented for real mutations;
- focus moves or is restored intentionally after errors/navigation;
- field errors are associated with the field;
- asynchronous status/error announcements are accessible when needed.

### 8.4 Responsive standard

Do not validate only 1536px + 390px and assume everything between them works.

For changed production surfaces, cover relevant sizes around:

```text
390–430px phone
~768–820px tablet/narrow
~1024–1280px compact desktop
1440–1536px desktop authority
large desktop where spacing/max-width can become visually weak
```

Check:

- no horizontal overflow;
- no clipped focus rings/controls;
- no awkward orphaned headings;
- readable line lengths;
- CTA reachable without broken viewport behavior;
- no desktop card merely shrunk into an unusable phone layout;
- touch targets usable on mobile.

### 8.5 Accessibility standard

Target WCAG 2.2 AA-quality behavior.

Automation is necessary but insufficient.

Required when relevant:

- axe A/AA checks;
- manual keyboard traversal;
- visible focus;
- logical focus order;
- semantic labels/roles;
- errors/help associated to fields;
- contrast on all surfaces, not only white;
- no color-only meaning;
- zoom/text scaling checks;
- reduced-motion behavior for nonessential motion;
- screen-reader-friendly status semantics;
- usable touch targets.

Never say "accessible" solely because axe is green.

### 8.6 Internationalization standard

- no hardcoded production user-facing strings outside the owning i18n resources unless explicitly invariant;
- IT and EN resource shapes remain aligned;
- `<html lang>` follows active locale;
- text expansion cannot break layout;
- provider/legal text follows official semantics;
- changing locale must not reset or corrupt safe local flow state.

### 8.7 Security/privacy standard

Never log, persist, expose in URL/state storage or analytics:

- password;
- OTP;
- recovery proof;
- auth code;
- PKCE verifier;
- provider assertion/token;
- access/refresh/session secret.

Never leak account existence through recovery copy unless the approved backend/product contract explicitly allows it.

Real integration must defend against:

- credential stuffing/brute force;
- account enumeration;
- OTP/recovery abuse;
- provider transaction tampering/replay;
- account-link takeover;
- session hijack/fixation;
- unsafe redirect/callback handling.

Backend remains authoritative for session/account/link state.

### 8.8 Provider standard

For production Google/Apple integration:

- use current official provider mechanism/SDK/rendering requirements where required;
- use official provider marks/assets;
- validate backend-side provider assertions;
- bind provider transaction state correctly;
- use exact approved redirects/callbacks;
- use PKCE where applicable to the final client/platform flow;
- provider authentication does not silently grant Gmail/Calendar/iCloud permissions.

Do not handcraft a "looks like Google" production button if official provider rendering/mechanism requires otherwise.

### 8.9 Error-state standard

Do not convert every failure into "wrong password".

Map real backend errors into user-relevant classes such as, where the contract supports them:

```text
invalid credentials
verification required
provider cancelled
provider failed
account link required/conflict
offline / timeout
rate limited
server unavailable
session expired/revoked
security reauthentication required
```

Do not expose sensitive internal reason codes.

### 8.10 Architecture standard

- feature-first ownership remains;
- routes consume the feature public API only;
- no Web ↔ Mobile private imports;
- no shared package dumping grounds;
- no generic `Repository<T>` abstractions;
- no fake DTO/API layer created just for tests/screenshots;
- stable server OpenAPI should drive the generated client boundary;
- TanStack Query/Form/Zod are adopted at the real justified boundary, not inserted ceremonially;
- generated outputs remain deterministic;
- no debug/test harness code in production routes/bundles.

---

## 9. Backend readiness / integration decision

The last recorded backend readiness inspection found PostgreSQL/persistence advanced but no stable real Access Auth API/OpenAPI yet.

That finding is stale as soon as backend work advances.

Before the next real integration batch:

1. inspect the current backend branch from repository truth;
2. determine whether Auth/session/recovery/provider surfaces exist;
3. inspect OpenAPI/DTO/error semantics;
4. only then choose the next integration slice.

Decision:

```text
backend Auth ready enough
→ integrate the real boundary directly

backend Auth not ready
→ continue only durable frontend production hardening
→ no fake-success service just to move screens
```

The user is working on backend in parallel, so re-check rather than assuming the old status.

---

## 10. Expected real integration direction

When the backend contract is stable enough, expected direction is:

```text
FastAPI Auth
→ stable OpenAPI
→ generated typed client (Orval / @dante/api-client if still authoritative)
→ real remote-state boundary
→ existing Access reducer/state graph
→ real signup/signin/verification/recovery/provider/session flows
→ authenticated Home handoff
→ full-stack E2E
```

Do not redesign the whole state graph just because the real API arrives. Map real server outcomes into the already approved canonical states unless the backend contract proves the state model itself must change.

---

## 11. Password contract

```text
minimum                    12 characters
support                    >=64 characters
mandatory composition      none
paste/password manager     allowed
show/hide                   allowed
common/breached blocklist  required server-side
```

Do not add arbitrary uppercase/symbol/number composition rules.

---

## 12. Mandatory QA discipline

Baseline gate:

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

But every batch needs **risk-specific QA**, not only the baseline.

Examples:

- changed UI → representative screenshots + visual review;
- new/changed state → unit/component state tests;
- keyboard/menu/form behavior → keyboard/focus checks;
- new responsive behavior → multiple viewport checks and overflow assertions;
- accessibility-affecting change → axe + manual review;
- new API → success/error/timeout/offline/rate-limit tests;
- provider integration → callback/cancel/error/link collision tests;
- session integration → bootstrap/expiry/revocation/reauth tests;
- recovery → neutral enumeration behavior + proof expiry/single-use full-stack tests;
- final integration → isolated backend/DB full-stack E2E.

Never call a visual PASS before actually looking at the screenshots. A compile/test PASS is not a product PASS.

---

## 13. Final Access closure checklist

Access is not "done" until all applicable items below are satisfied.

### Visual / UX

```text
[ ] every canonical state has production-quality UI
[ ] desktop/tablet/phone composition reviewed
[ ] no collage/coupage or inconsistent component grammar
[ ] no placeholder/debug/developer copy
[ ] loading/error/offline/rate-limit states polished
[ ] provider/legal surfaces final
```

### I18N / accessibility

```text
[ ] IT/EN parity final
[ ] keyboard/focus behavior complete
[ ] WCAG AA automated checks pass
[ ] manual accessibility checks pass
[ ] text expansion/zoom/reduced-motion risks handled
```

### Real auth/security

```text
[ ] real signup
[ ] real sign-in
[ ] real email verification
[ ] real recovery/reset
[ ] real Google/Apple provider flows
[ ] secure account linking
[ ] real session bootstrap
[ ] session expiry/revocation handling
[ ] real reauth for protected operations
[ ] server errors/rate-limit mappings final
[ ] no secrets/sensitive proofs logged or persisted client-side
```

### Architecture / integration

```text
[ ] stable Auth OpenAPI
[ ] generated typed client boundary
[ ] no temporary fake auth adapter remains
[ ] state graph mapped to real backend outcomes
[ ] routes/public API boundaries remain clean
[ ] architecture/generated gates pass
```

### QA / release

```text
[ ] unit/component tests pass
[ ] browser E2E pass
[ ] full-stack E2E against isolated backend/DB pass
[ ] production build passes
[ ] visual/product review accepted
[ ] hosted CI green
[ ] real Terms/Privacy destinations/content
[ ] authenticated Home handoff real
[ ] deployment/config requirements documented
```

Only after this should the assistant propose a separate Access closure + merge gate.

---

## 14. Merge discipline

No merge to protected `main` is authorized by this handoff.

Never:

- merge because GitHub says `mergeable`;
- rebase/force-push to make history look cleaner;
- change branch/worktree because the chat changed;
- silently rewrite historical evidence;
- include unrelated cleanup in an Access batch.

Merge requires a new explicit user gate after final hosted/local QA and review.

---

## 15. What the next chat should do first

The next chat should **not immediately code**.

First response/action sequence:

```text
1. read this handoff + workstream completely
2. fresh-read feature/access-frontend HEAD
3. verify local worktree/branch expectations
4. inspect current backend Auth readiness
5. identify the highest-value remaining Access slice
6. state exact write gate
7. only then modify files
```

If backend Auth is now mature enough, prioritize real integration rather than inventing more temporary frontend layers.

If it is not ready, continue only durable frontend work that advances final production readiness.

The current chat can remain available as a reviewer during handoff: if the next chat proposes branch churn, fake auth, low-quality UI shortcuts, unbounded writes, unjustified architecture changes or declares PASS without visual/security/QA evidence, stop and correct it before proceeding.
