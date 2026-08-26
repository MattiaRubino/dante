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
6. summarize what is PASS, what is still open and what the next bounded batch should be;
7. **do not write yet**;
8. state the exact WRITE GATE: purpose + exact allowed paths + explicit exclusions;
9. obtain explicit user authorization for that batch unless the user already authorized that exact bounded batch in the same message;
10. immediately before the first write, fresh-check HEAD again;
11. if HEAD changed, STOP and re-gate;
12. write only allowed paths;
13. if scope needs to expand, STOP and declare a new gate before touching any new path;
14. read back/compare the exact delta;
15. give the user one `.sh` for pull/format/QA/screenshot when local execution is needed;
16. review QA output and screenshots before calling a batch PASS;
17. never merge to `main` without a separate explicit merge gate.

### Write permission is mandatory

A chat/agent must **not** infer write permission merely because it knows what should be changed.

Forbidden behavior:

```text
"I know the next step, so I changed it"
"while I was there I cleaned up..."
"I also updated these adjacent files..."
"this is harmless so I did not re-gate"
```

Required behavior:

```text
fresh HEAD
→ bounded WRITE GATE
→ explicit user approval for that batch
→ fresh HEAD immediately before first write
→ exact-path write only
→ readback/compare
→ QA
```

If a compiler/test reveals a new file must change, that is a **new scope decision**, not automatic permission to edit it.

Documentation-only changes are still branch-visible writes and require the same discipline unless the user explicitly authorized that documentation batch.

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
2. user authorizes the bounded batch;
3. assistant modifies GitHub remotely when safe/available;
4. assistant readbacks/compares the remote delta;
5. assistant gives one downloadable `.sh` for pull/format/QA/screenshot;
6. user runs it from WSL, normally:
   `bash /mnt/c/Users/mtaru/Downloads/<script>.sh`;
7. user reviews code/diffs in WebStorm and UI in browser;
8. assistant reviews output/screenshots;
9. only then create a formatting/checkpoint commit if needed;
10. merge remains a separate user decision.

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

The user explicitly requires a mature, high-end application standard. Treat every screen as if it may ship to production immediately.

The target is not “good enough for a prototype”. It is the quality bar expected from a mature large application: coherent, intentional, accessible, secure, maintainable and polished across states and viewports.

### 8.1 No collage/coupage UI

Never build screens by stitching together unrelated visual patterns from random apps or examples.

Rules:

- one coherent DANTE visual language;
- no random cards/gradients/chips/icons/illustrations just to make a page look designed;
- no arbitrary per-screen CSS hacks when a reusable semantic rule/component is appropriate;
- new UI patterns must visually belong to the existing Access system;
- whitespace can be intentional — do not fill empty panels with decorative noise;
- do not mimic another big app literally; study mature patterns, then adapt them to DANTE’s product/brand contract;
- visual hierarchy must be intentional at all viewports;
- a screen must not look half-finished merely because its backend action is not yet available.

### 8.2 Design tokens, palette and color — mandatory

`@dante/design-tokens` and the accepted Access visual authority are the default source of truth for production visual values.

Rules:

- prefer semantic design tokens over raw primitive values;
- do not introduce random hex/rgb/hsl values because they look close;
- do not invent a new palette for one screen;
- do not change the established warm canvas / ink / muted-surface / DANTE accent relationship without an explicit design gate;
- do not use the accent orange as a generic warning/error/success color merely because it is available;
- color must carry product meaning consistently across the flow;
- contrast must be checked on the **actual background surface**, including muted panels, disabled states and hover/focus states;
- never rely on color alone to communicate state;
- if a new semantic color role is genuinely needed, define/justify it at the token/design-system level instead of scattering raw values through feature CSS;
- before adding a token, check whether an existing semantic token already expresses the intent.

No “magic color values” in feature CSS unless there is a documented exceptional reason and the write gate explicitly includes that design decision.

### 8.3 Typography — mandatory

Typography is part of the product system, not per-screen decoration.

Rules:

- preserve the established DANTE/Access font family and hierarchy;
- do not invent arbitrary heading sizes/weights/line-heights per screen;
- use existing type scale/semantic styles where available;
- line length and wrapping must be reviewed in both IT and EN;
- headings must not become oversized merely to resemble another app;
- compact helper/legal/error text must remain readable and accessible;
- typography changes that materially alter hierarchy require visual review at desktop and mobile widths.

### 8.4 Spacing, radius, borders and shadow — mandatory

- reuse established spacing rhythm before inventing new gaps;
- controls that are semantically equivalent should share height, radius, border behavior and focus treatment;
- do not create a new radius/shadow language per screen;
- Access card geometry should remain coherent with the accepted shell;
- shadows must support depth/hierarchy, not decoration;
- borders/dividers should be subtle and semantic, not random visual separators;
- one-off values are allowed only when geometry genuinely requires them and the reason is clear.

### 8.5 Assets and brand masters — mandatory

Production assets must come from the authoritative repository asset set or from an explicitly approved new asset.

Rules:

- use the locked DANTE symbol/wordmark masters already in the repository;
- do not redraw, approximate, trace or manually recreate the DANTE logo/wordmark when the master asset exists;
- preserve aspect ratio and intended clear space;
- prefer vector/master assets when available instead of unnecessary raster copies;
- do not recolor/warp/distort brand assets outside the approved brand treatment;
- the Living Orbits visual language is part of the accepted Access composition — do not replace it with unrelated decoration without an explicit design gate;
- do not import stock/decorative imagery merely to fill whitespace;
- new imagery/illustration must have a product purpose and a consistent DANTE art direction;
- any new asset must have clear ownership/location/naming and must not be dumped into an arbitrary folder.

### 8.6 Provider assets and marks — mandatory

For Google/Apple production integration:

- use current official provider mechanism/SDK/rendering requirements where required;
- use official provider marks/assets;
- do not redraw or approximate provider logos;
- do not modify provider marks in a way forbidden by provider guidelines;
- provider visual treatment must remain coherent with DANTE while respecting official requirements;
- validate backend-side provider assertions;
- bind provider transaction state correctly;
- use exact approved redirects/callbacks;
- use PKCE where applicable to the final client/platform flow;
- provider authentication does not silently grant Gmail/Calendar/iCloud permissions.

Do not handcraft a “looks like Google/Apple” production button when official rendering/mechanism requirements say otherwise.

### 8.7 Iconography — mandatory

- use the existing icon source/pattern when available;
- keep stroke weight, optical size and alignment coherent;
- do not mix unrelated icon families casually;
- do not use emoji/random Unicode glyphs as production icons merely because they are convenient;
- if a symbol is decorative, keep it out of the accessibility tree;
- if an icon is interactive, it needs a proper accessible name and touch target;
- icon-only actions must remain understandable and discoverable.

### 8.8 Production copy only

Never expose:

- `backend required`;
- `frontend ready`;
- debug state names;
- raw server errors;
- developer instructions;
- placeholder legal destinations presented as real links;
- fake provider/security claims.

User copy must be natural, concise, secure and action-oriented.

### 8.9 IT/EN internationalization quality — mandatory

Italian and English are both production languages, not “primary + rough translation”.

Rules:

- no production user-facing string hardcoded outside the owning i18n resources unless explicitly invariant;
- IT and EN resource shapes remain aligned;
- copy is transcreated for natural language and equivalent meaning, not mechanically translated word-for-word;
- `<html lang>` follows the active locale;
- text expansion/wrapping must be checked in **both** languages;
- provider/legal names and official wording remain semantically correct;
- changing locale must not reset/corrupt safe local flow state;
- error/loading/success/offline/rate-limit copy requires IT/EN parity too;
- no newly added state is considered done until both languages are complete and visually checked where text length can alter composition.

### 8.10 Interaction standard

Every interactive state must consider, where semantically applicable:

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
cancel/retry
```

Forms must use semantic form behavior where appropriate:

- Enter submits the expected action;
- password manager/autofill works;
- paste works where security policy permits it;
- browser autocomplete attributes are correct;
- double-submit is prevented for real mutations;
- focus moves or is restored intentionally after errors/navigation;
- field errors are associated with the field;
- asynchronous status/error announcements are accessible when needed.

Do not add meaningless states merely to appear complete.

### 8.11 Responsive standard

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
- touch targets usable on mobile;
- IT and EN text expansion at relevant widths.

### 8.12 Accessibility standard

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

Never say “accessible” solely because axe is green.

### 8.13 Security/privacy standard

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

### 8.14 Error-state standard

Do not convert every failure into “wrong password”.

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

### 8.15 Architecture standard

- feature-first ownership remains;
- routes consume the feature public API only;
- no Web ↔ Mobile private imports;
- no shared-package dumping grounds;
- no generic `Repository<T>` abstractions;
- no fake DTO/API layer created just for tests/screenshots;
- stable server OpenAPI should drive the generated client boundary;
- TanStack Query/Form/Zod are adopted at the real justified boundary, not inserted ceremonially;
- generated outputs remain deterministic;
- no debug/test harness code in production routes/bundles;
- no dependency/version churn merely to silence nonblocking warnings.

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
→ real form/error contract
→ remote-state/query integration where justified
→ existing Access state graph
→ real provider/session/recovery/link flows
→ authenticated Home handoff
→ full-stack E2E
```

Do not redesign the state graph merely because the backend arrives. Wire real authoritative events into the existing canonical graph unless repository truth proves a contract change is required.

---

## 11. Password/security contract

```text
minimum                    12 characters
support                    >=64 characters
mandatory composition      none
paste/password manager     allowed
show/hide                   allowed
common/breached blocklist  required server-side
```

Do not add arbitrary composition rules just because another application uses them.

---

## 12. Mandatory QA gate

Normal repository gate:

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

Generic QA is not enough. Every batch must add targeted checks for the risk introduced.

Examples:

- visual screenshots for new/changed states;
- IT + EN visual checks where copy changed;
- axe for new/changed states;
- keyboard/focus checks for menus/forms/dialog-like flows;
- responsive checks beyond one desktop/one phone where layout changed;
- mobile overflow and touch-target checks;
- token/color contrast checks on the real surface;
- asset/brand/provider mark review when visual assets change;
- real network/error mapping tests when APIs exist;
- provider callback/session/recovery full-stack tests when backend exists;
- hosted CI before merge;
- manual product review before claiming visual PASS.

A test harness must faithfully import the same relevant global styles/runtime assumptions as production. A harness failure must be diagnosed before changing production code.

---

## 13. Final Access closure criteria

Do **not** mark Access closed until all applicable items are true:

```text
VISUAL / DESIGN SYSTEM
[ ] all canonical Access states visually reviewed
[ ] desktop/tablet/phone responsive quality accepted
[ ] IT/EN visual expansion reviewed
[ ] no placeholder/debug/developer-facing UI
[ ] no random raw colors/spacing/icon styles outside approved design rules
[ ] DANTE brand masters/assets used correctly
[ ] provider marks/mechanisms conform to official requirements
[ ] typography/spacing/radius/shadow hierarchy coherent across the whole flow

I18N / A11Y
[ ] IT/EN parity final
[ ] keyboard/focus behavior complete
[ ] WCAG 2.2 AA automation + manual checks pass
[ ] text expansion/zoom/reduced-motion risks handled

AUTH / SECURITY
[ ] real signup/signin/verification/recovery wired
[ ] real Google/Apple transactions wired
[ ] account linking secure
[ ] session bootstrap/expiry/revocation handled
[ ] reauth works for protected transitions
[ ] no sensitive material logged/persisted client-side
[ ] server errors/rate limits mapped correctly

ARCHITECTURE
[ ] stable OpenAPI/typed client boundary
[ ] no temporary fake auth adapter remains
[ ] routes import feature public API only
[ ] no architecture violations
[ ] no production debug/test harness remains

QA
[ ] unit/component tests pass
[ ] browser E2E pass
[ ] full-stack E2E against isolated backend/DB pass
[ ] production build pass
[ ] targeted responsive/a11y/i18n/security tests pass
[ ] visual/product review accepted
[ ] hosted CI gates green

RELEASE
[ ] Terms/Privacy destinations/content real
[ ] authenticated Home handoff real
[ ] migration/deployment/config requirements documented
```

Only after these are satisfied should a separate merge/closure gate be proposed.

---

## 14. Merge discipline

No merge to protected `main` is authorized by this handoff.

Merge is a separate explicit user gate after final QA/review.

Never rebase/force-push/rewrite history. Never merge solely because GitHub says mergeable.

---

## 15. What the next chat must report before asking to write

After reading this handoff and repository authorities, the next chat should report:

1. the live `feature/access-frontend` HEAD it verified;
2. whether local/remote divergence exists;
3. AF-01D / AF-02A / AF-02B status;
4. what remains to truly close Access;
5. current backend Auth/OpenAPI readiness from a fresh repository read;
6. the proposed next bounded batch;
7. exact files it would need to touch;
8. explicit exclusions;
9. expected QA and visual evidence.

Only after the user approves that bounded gate should it write.
