# Access frontend workstream

**Branch:** `feature/access-frontend`  
**Permanent frontend worktree:** `/home/mattia/projects/dante-frontend`  
**Product authority:** `prototypes/frontend/access/README.md`, `docs/frontend/access/current-checkpoint.md`, `docs/frontend/access/contract.md`, `docs/frontend/access/state-model.md`  
**Desktop visual authority:** Access A3.4  
**Mobile visual authority:** M1.2 + PRG-0

## Purpose

Materialize the approved DANTE Access experience inside the production React/Vite frontend without inventing backend authentication semantics before the real backend contract exists.

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

AF-02A therefore advances every safe frontend-owned part of Access while preserving backend authority.

Accepted implementation includes:

- feature-local `model/access-flow.ts` with the approved canonical Access states;
- explicit orthogonal transport conditions: idle, backend-required, offline, server-unavailable and rate-limited;
- local transitions for sign-in navigation, signup email/password, recovery entry and setup choices;
- browser `online` / `offline` event integration;
- production IT/EN copy for the complete approved Access screen inventory;
- signup email screen;
- signup password screen with the DANTE V1 12-character minimum, paste/password-manager-safe behavior and no composition rule;
- forgot-password screen with neutral account-existence copy;
- verify-email, recovery-sent, reset-password and reset-complete surfaces;
- provider pending/error and account-link surfaces;
- reauthentication surface;
- setup name, locale/timezone and first-run choice surfaces;
- first-action/import/demo/Home-handoff surfaces;
- local validation and password visibility behavior;
- E2E coverage for signup/recovery frontend navigation and backend-boundary stopping;
- reducer tests that specifically prove local actions do **not** fabricate backend success;
- backend-required conditions remaining internal/non-user-facing;
- desktop visual review of SignIn, signup email/password and recovery;
- phone visual review of signup at 390px;
- product-copy polish for provider continuation and neutral recovery wording.

Critical rule:

```text
frontend-only transition
→ may advance locally

backend-authoritative transition
→ stays on the current safe state
→ condition = BACKEND_REQUIRED
→ never fabricates VERIFY_EMAIL / AUTHENTICATED_RETURN / RECOVERY_SENT / LINK success
```

Examples:

```text
CREATE_ACCOUNT
SIGN_IN → SIGN_UP_EMAIL                         local / real

valid signup email
SIGN_UP_EMAIL → SIGN_UP_PASSWORD                local / real

submit signup password
SIGN_UP_PASSWORD → BACKEND_REQUIRED(sign-up)    real boundary
NOT → fake VERIFY_EMAIL

forgot password + valid email
FORGOT_PASSWORD → BACKEND_REQUIRED(recovery)    real boundary
NOT → fake RECOVERY_SENT

Google/Apple click
SIGN_IN → BACKEND_REQUIRED(provider-*)          real boundary
NOT → fake PROVIDER_PENDING
```

Server/provider events are already represented in the reducer so the later real integration can activate the downstream states without redesigning the UI state model.

AF-02A QA passed the normal frontend gate: formatting, lint, typecheck, architecture, generated-output check, unit tests, Web build, Playwright E2E and diff check. Visual review accepted the polished desktop and phone surfaces.

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

## Backend-readiness gate — 2026-08-25

The post-AF-01D backend inspection was performed against `feature/logical-postgresql`.

Observed backend state:

- FastAPI/bootstrap exists;
- PostgreSQL runtime/config/provisioning and migration foundation exists;
- persistence/database testing is active;
- current app factory exposes `/health/live` and `/health/ready`;
- no implemented Access Auth/session/OAuth/recovery/account-link route/domain surface yet;
- no stable Access OpenAPI contract yet.

Verdict:

```text
frontend shell / visual authority            PASS
AF-02A pre-backend frontend flow             PASS
backend PostgreSQL foundation                ADVANCED / ACTIVE
real Access Auth API/OpenAPI                  NOT READY
AF-03 real integration                       BLOCKED BY BACKEND AUTH BOUNDARY
```

## Deliberately not materialized yet

- backend AuthN/AuthZ implementation;
- password/session/token physical design;
- Google client ID / Apple Services ID;
- OAuth/OIDC callback execution;
- real provider transaction start;
- backend account-linking mutation;
- verification/recovery proof validation;
- OpenAPI/Orval generated Access client;
- TanStack Query remote-auth integration;
- backend-authoritative session bootstrap;
- canonical authenticated Home routing;
- native Mobile Access implementation;
- final Terms/Privacy destinations/content.

Terms/Privacy are deliberately rendered as non-interactive legal placeholders until real destinations/content exist; do not create fake/broken routes.

## Form-library boundary

AF-02A uses small controlled React forms and pure local validation only for frontend-owned preflight behavior. Password/OTP/recovery/provider secrets are not moved into global flow state or persisted.

Do not prematurely lock server DTO/error semantics into a client schema before the real Auth OpenAPI exists. At the real integration boundary, evaluate/adopt TanStack Form + Zod against the actual DTO/error contract rather than building a second fake API model now.

## Password/security contract

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

## QA gate

Normal frontend release-quality gate:

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

AF-02A manual/browser acceptance covered:

- SignIn desktop authority unchanged;
- create-account → email → password;
- backend-required state remaining non-user-facing after signup submit;
- forgot-password frontend path with neutral copy;
- provider continuation wording;
- 390px phone signup composition;
- no obvious visual regressions on accepted desktop composition.

## AF-02B — downstream surface hardening

Next safe frontend-only batch:

- verify-email surface behavior/validation/accessibility;
- recovery-sent and reset-password/reset-complete;
- provider pending/error and account-link;
- reauthentication;
- setup name;
- setup locale/timezone;
- setup start choices;
- first-action/import/demo/Home-handoff;
- IT/EN parity;
- desktop/phone visual QA;
- reducer/unit/E2E coverage where transitions are frontend-owned or can be tested with reducer/server-event fixtures without a fake service.

AF-02B must **not** create a fake authentication adapter or pretend that backend-owned success happened in the production UI.

## Next integration boundary

Continue AF-02B frontend-owned hardening only where it does not invent backend semantics.

When backend Auth becomes ready:

```text
FastAPI Auth + stable OpenAPI
→ generated typed API boundary
→ real provider/session/recovery transactions
→ remote-state/query integration where justified
→ real form/schema binding
→ full-stack E2E
```

Do not create a fake success adapter merely to make downstream states reachable. Server-owned events already exist in the reducer for the real integration.

## Merge discipline

A merge to protected `main` remains a separate explicit gate after local and hosted QA. Never merge merely because GitHub reports the branch mergeable.

## Continuity

Read `docs/workstreams/access-frontend-live-handoff.md` before continuing this workstream in a new chat/tool/session. Repository truth overrides chat memory.
