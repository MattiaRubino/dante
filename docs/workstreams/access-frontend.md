# Access frontend workstream

**Branch:** `feature/access-frontend`
**Permanent frontend worktree:** `/home/mattia/projects/dante-frontend`
**Product authority:** `prototypes/frontend/access/README.md`, `docs/frontend/access/current-checkpoint.md`, `docs/frontend/access/contract.md`, `docs/frontend/access/state-model.md`
**Desktop visual authority:** Access A3.4
**Mobile visual authority:** M1.2 + PRG-0

## Purpose

Materialize the complete DANTE Access vertical inside the production frontend and carry it through real backend integration and release-quality validation without inventing authentication semantics, fake success, disposable mock architecture or low-quality UI shortcuts.

This workstream stays on `feature/access-frontend` and in `/home/mattia/projects/dante-frontend` until Access is actually closed. A new chat/session is **not** a reason to create a new branch or worktree. Branch/worktree changes require an explicit user decision.

## Quality target

Access is treated as production software from the first implementation pass. The target is the quality bar of a mature consumer/productivity application, not a prototype that merely compiles.

Every surface must feel intentionally designed as part of one system. Do not assemble screens as a collage/coupage of unrelated cards, copied patterns, arbitrary decorations or one-off CSS. Reuse the established DANTE visual grammar, hierarchy, spacing, typography, controls, semantic tokens and interaction language.

A batch is not accepted because it "looks okay" or because CI is green. Acceptance requires technical QA **and** product/visual review at the relevant viewport/state combinations.

## Current production state

### AF-01A — first React materialization

Materialized the unauthenticated SignIn shell on Web:

- DANTE brand stage and locked brand masters;
- email/password visual controls;
- Google/Apple provider affordances;
- Italian/English resource ownership through `@dante/i18n`;
- desktop and narrow responsive composition;
- no real submission, provider transaction, session or backend contract.

### AF-01C — foundation hardening

Completed foundation work includes:

- Access UI behind `features/access/index.ts` and the feature-local `ui/` boundary;
- routes consuming only the feature public API;
- design-token, architecture and generated-output gates;
- production provider marks;
- Testing Library component coverage;
- Playwright production-preview coverage;
- axe WCAG A/AA automation;
- React Hooks lint qualification;
- desktop open brand-stage geometry, narrow composition and phone-width overflow coverage;
- professional IT/EN selector with browser-locale fallback and persisted preference.

### AF-01D — shell completion / professional polish — PASS

AF-01D was accepted after fresh local QA and visual review on 2026-08-25.

Accepted behavior includes:

- production Italian hero copy `Comprendi la vita. / Dai forma al prossimo passo.`;
- English hero copy `Understand life. / Shape what comes next.`;
- locale-aware desktop headline sizing;
- `document.documentElement.lang` following the active locale;
- localized field/visibility strings;
- real local password show/hide behavior;
- hardened locale popover keyboard/focus behavior;
- browser locale fallback plus persisted IT/EN preference;
- unit/E2E coverage and desktop/narrow/phone overflow/accessibility gates.

The accepted production composition preserves the A3.4 direction: full warm canvas, open left brand stage, muted Living Orbits, locked DANTE topbar, compact locale control and separate Access card.

### AF-02A — complete pre-backend frontend state graph — PASS

AF-02A was accepted after iterative local QA, E2E and visual review on 2026-08-25.

The user explicitly chose to continue frontend work while backend Auth is still being built, but without a fake/mock authentication service.

Accepted implementation includes:

- feature-local `model/access-flow.ts` with the approved canonical Access states;
- explicit orthogonal transport conditions: idle, backend-required, offline, server-unavailable and rate-limited;
- local transitions for sign-in navigation, signup email/password, recovery entry and setup choices;
- browser `online` / `offline` event integration;
- production IT/EN copy for the complete approved Access screen inventory;
- signup email and signup password screens;
- DANTE V1 12-character password minimum, paste/password-manager-safe behavior and no composition rule;
- forgot-password screen with neutral account-existence copy;
- verify-email, recovery-sent, reset-password and reset-complete surfaces;
- provider pending/error and account-link surfaces;
- reauthentication surface;
- setup name, locale/timezone and first-run choice surfaces;
- first-action/import/demo/Home-handoff surfaces;
- local validation and password visibility behavior;
- E2E coverage for signup/recovery frontend navigation and backend-boundary stopping;
- reducer tests that prove local actions do **not** fabricate backend success;
- backend-required conditions remaining internal/non-user-facing;
- desktop and phone visual review.

Critical rule:

```text
frontend-only transition
→ may advance locally

backend-authoritative transition
→ stays on the current safe state
→ condition = BACKEND_REQUIRED
→ never fabricates VERIFY_EMAIL / AUTHENTICATED_RETURN / RECOVERY_SENT / LINK success
```

### AF-02B — downstream surface hardening — PASS

AF-02B was accepted on 2026-08-25 after full repository QA, exhaustive downstream axe checks, desktop screenshot review and 390px mobile overflow/accessibility checks.

**Accepted code/formatting checkpoint:** `c39d1a8312fb2d00bc322604bcd453d13fa2b510`.

Accepted downstream coverage includes:

- verify-email six-digit local validation, resend/change-email actions and accessible errors;
- recovery-sent neutral account-existence messaging;
- reset-password two-field validation, password-manager-safe behavior and working visibility controls;
- reset-complete return-to-sign-in surface;
- provider pending, provider error and account-link surfaces;
- authenticated-return and reauthentication surfaces;
- setup name validation;
- locale/timezone confirmation surface;
- first-run start choices;
- first-action, import, demo and Home-handoff surfaces;
- IT/EN resource parity;
- downstream component tests via canonical state fixtures rather than a fake auth service;
- provider/auth copy that does not imply external-data authorization;
- password-guide contrast corrected to meet automated WCAG AA checks;
- real browser offline E2E using Playwright BrowserContext state instead of a synthetic race-prone event.

Final AF-02B QA evidence:

```text
Playwright reachable E2E             10 / 10 PASS
Web unit/component tests             17 / 17 PASS
workspace typecheck                   5 / 5 PASS
architecture                         PASS
Generated sources deterministic       PASS
Web production build                  PASS
axe desktop downstream inventory      PASS
axe phone verify/reset/setup-start    PASS
390px horizontal overflow checks      390 / 390 PASS
```

The downstream QA harness is test-only and temporary. It must never become a production debug route or fake server control.

## Access is NOT closed yet

AF-02B closes the production-quality **frontend-owned/pre-backend surfaces**, not the Access vertical itself.

Access remains open until the real backend-auth boundary and release gates are complete. Do not change branch/worktree merely because AF-02B is PASS.

Remaining backend-authoritative work includes, as applicable to the final backend contract:

- real account creation;
- credential authentication;
- email verification proof validation;
- recovery proof validation and reset mutation;
- Google/Apple transaction start/callback/validation;
- secure account linking;
- session establishment/bootstrap/expiry/revocation;
- reauthentication for sensitive operations;
- real server rate-limit/error mapping;
- stable Auth OpenAPI;
- generated typed client;
- remote-state/query integration where justified;
- final authenticated Home handoff;
- full-stack E2E against an isolated test environment;
- final legal Terms/Privacy destinations/content;
- native Mobile Access when its implementation gate opens.

## Production design / UX standard

All future Access work must follow these rules.

### One coherent product, not a collage

- Every screen must look like DANTE, not like a collection of unrelated examples copied from other sites.
- Do not bolt on random cards, chips, illustrations, gradients, icons or decorative effects just to fill space.
- New patterns must reuse the design system or justify a reusable semantic component/token.
- Desktop and mobile are designed compositions, not merely the same desktop DOM squeezed narrower.
- Empty space may be intentional; do not fill it with decorative noise.
- Do not ship developer/debug language to users.
- Do not keep placeholder copy, fake routes, dead buttons or temporary visual affordances in a surface declared production-ready.

### Hierarchy and interaction

- One clear primary action per state unless the product contract genuinely requires otherwise.
- Secondary/destructive/cancel actions must have visually and semantically appropriate priority.
- Loading, disabled, success, error, offline, rate-limited and unavailable states must preserve layout stability and explain the next useful action.
- Avoid surprise navigation and ambiguous CTAs.
- Forms must support Enter/submit semantics, browser autofill, password managers and paste where appropriate.
- Prevent accidental double-submit once real network mutations exist.
- Focus must move intentionally after validation/navigation and remain keyboard-visible.

### Responsive quality

Before a surface is considered release-ready, validate representative widths rather than one desktop plus one phone only. At minimum cover the relevant breakpoints around:

```text
390–430px phone
~768–820px tablet/narrow
~1024–1280px compact desktop
1440–1536px accepted desktop authority
large desktop where composition could become too sparse/wide
```

No horizontal overflow, clipped controls, unreadable line lengths, accidental orphan headings or unreachable actions.

### Internationalization

- No production user-facing string hardcoded outside the owned localization resources unless the product contract explicitly marks it invariant.
- IT and EN must remain semantically equivalent, not mechanically word-for-word when that harms natural language or layout.
- `<html lang>` must track the active locale.
- Text expansion must not break controls/layout.
- Provider/legal text must respect official provider wording and real legal destinations.

### Accessibility

Release target is WCAG 2.2 AA-quality behavior for the Access flow.

Required checks include:

- semantic labels/names/roles;
- full keyboard operation and visible focus;
- logical focus order;
- associated inline errors/help;
- `aria-live`/status behavior where asynchronous feedback needs announcement;
- sufficient color contrast in every state, including muted surfaces;
- no information conveyed by color alone;
- usable zoom/text scaling;
- reduced-motion handling for nonessential animation;
- adequate mobile/touch target usability;
- axe automation plus manual keyboard/product review.

Passing axe alone does not prove accessibility.

### Security / privacy UX

Never expose or persist raw password, OTP, recovery proof, auth code, PKCE verifier, provider assertion/token, access/refresh/session secret.

Never leak account existence through recovery or signup/linking copy unless the backend contract explicitly allows it.

Provider sign-in authenticates DANTE only. Gmail/Calendar/iCloud or other integration authorization is a distinct flow.

Real integration must preserve transaction binding, exact redirect/callback validation, provider assertion validation, replay protection, account-link takeover defenses and backend-authoritative session state.

### Provider quality

Google/Apple production integration must use current official provider mechanisms/assets/requirements rather than handcrafted lookalikes where the provider SDK/official rendering is required.

Do not assume provider success from client-side UI. The backend remains authoritative for account/session/link state.

### Error-state quality

Do not collapse distinct failures into "password wrong". Real integration must distinguish at least the product-relevant classes represented by the backend contract, such as:

- invalid credentials;
- verification required;
- provider cancelled/failed;
- account-link required/conflict;
- offline/network timeout;
- rate limited;
- server unavailable;
- session expired/revoked;
- reauthentication required.

Copy must be useful without disclosing sensitive security detail.

## Invariants

```text
Person != Account != Principal != Actor
sign-in != external-integration authorization
provider state != canonical DANTE state
provider authentication != permission to read provider data
verification != profile setup
reauthentication != initial sign-in
client integrity != person identity
```

Google/Apple Access authenticates a DANTE account only. It does not grant Gmail, Calendar, iCloud or other provider-data permissions.

## Backend-readiness gate

The latest recorded backend inspection was performed against `feature/logical-postgresql` after AF-01D and found PostgreSQL/persistence advanced but no stable real Access Auth API/OpenAPI yet.

Do **not** rely indefinitely on that old inspection. Before starting real integration, fresh-read the backend branch and re-evaluate readiness from repository truth.

Decision rule:

```text
Auth backend + stable contract ready
→ integrate real backend directly

Auth backend still not ready
→ continue only durable frontend work that will survive real integration
→ do not create a fake-success auth service merely for reachability
```

## Form-library / API boundary

Current pre-backend forms use local controlled React state and pure local validation for frontend-owned preflight behavior. Passwords/codes remain component-local and are not persisted/globalized.

When the real Auth OpenAPI is stable, bind forms/errors to the real contract and evaluate/adopt TanStack Form + Zod at that boundary. Do not invent a parallel fake server DTO/error model now.

Real API flow should follow the architecture decision then current, expected direction:

```text
FastAPI stable Auth OpenAPI
→ generated typed client (`@dante/api-client` / Orval if still authoritative)
→ remote-state/query boundary where justified
→ existing Access state graph
→ real provider/session/recovery flows
→ full-stack E2E
```

## Password/security contract

```text
minimum                    12 characters
support                    >=64 characters
mandatory composition      none
paste/password manager     allowed
show/hide                   allowed
common/breached blocklist  required server-side
```

Never add arbitrary composition rules merely because another app uses them.

## Mandatory QA gate

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

Future batches must add targeted QA for the risk introduced, not merely rerun the generic gate. Examples:

- visual screenshots for new/changed surfaces;
- axe for new states;
- keyboard/focus checks for menus/forms/dialog-like flows;
- mobile overflow/viewport checks;
- real network/error mapping tests when APIs exist;
- provider callback/session/recovery full-stack tests when backend exists;
- hosted CI before merge;
- manual product review before claiming visual PASS.

A test harness must faithfully import the same relevant global styles/runtime assumptions as production. A harness failure must be diagnosed before changing production code.

## Final Access closure criteria

Do **not** mark Access closed until all applicable items are true:

```text
VISUAL / UX
[ ] all canonical Access states visually reviewed
[ ] desktop/tablet/phone responsive quality accepted
[ ] no placeholder/debug/developer-facing UI
[ ] provider/legal copy final

I18N / A11Y
[ ] IT/EN parity final
[ ] keyboard/focus behavior complete
[ ] WCAG AA automation + manual checks pass
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

QA
[ ] unit/component tests pass
[ ] browser E2E pass
[ ] full-stack E2E against isolated backend/DB pass
[ ] production build pass
[ ] visual regression/product review accepted
[ ] hosted CI gates green

RELEASE
[ ] Terms/Privacy destinations/content real
[ ] authenticated Home handoff real
[ ] migration/deployment/config requirements documented
```

Only after these are satisfied should a separate merge/closure gate be proposed.

## Merge discipline

No merge to protected `main` is implied by any AF checkpoint. Merge remains a separate explicit user gate after final QA/review.

Never rebase/force-push/rewrite history without explicit authorization. Never merge merely because GitHub reports mergeable.

## Continuity

Read `docs/workstreams/access-frontend-live-handoff.md` first when a new chat/agent/session takes over. Repository truth and fresh branch HEAD override chat memory.