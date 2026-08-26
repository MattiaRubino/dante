# DANTE — Access frontend contract

- **Status:** CURRENT / AUTHORITATIVE FOR THE MATERIALIZED PRE-BACKEND FRONTEND
- **Scope:** Web Access frontend baseline already implemented in `apps/web`; product/backend Auth remains a later full-stack vertical
- **Frozen design source:** `prototype/access-system` at `469b68370e80185fa8a16d5335845e402ee1de3b`

## Purpose

Access gets an unauthenticated person to an authenticated DANTE session and, for a new account, through the smallest useful first-run handoff.

This document owns the current production-frontend contract carried forward from the frozen Access design work and the completed `feature/access-frontend` materialization. Implementation truth remains the checked-out code/tests. The frozen prototype branch is historical design evidence and must not override newer production code or this current contract.

## Product invariants

```text
Person != Account != Principal != Actor
sign-in != external-integration authorization
provider state != canonical DANTE state
provider authentication != permission to read provider data
verification != profile setup
reauthentication != initial sign-in
client integrity != person identity
```

Google/Apple sign-in authenticates a DANTE account only. Gmail, Calendar, iCloud and other provider-data permissions are separate explicit integration flows.

## Accepted visual direction

Desktop/web review authority remains A3.4. Mobile design authority remains M1.2 + PRG-0.

The materialized Web composition preserves:

```text
warm full canvas
+ open left brand stage
+ muted Living Orbits
+ locked DANTE topbar
+ compact locale control
+ separate rounded/shadowed Access card
```

Approved hero copy:

```text
IT  Comprendi la vita. / Dai forma al prossimo passo.
EN  Understand life. / Shape what comes next.
```

Mobile is not a scaled desktop. Native Mobile Access is not implemented by this frontend workstream and remains a later product implementation gate.

## Canonical Access states

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

Orthogonal frontend conditions are not account states:

```text
idle
backend-required
offline
server-unavailable
rate-limited
```

Permanent authority rule:

```text
frontend-owned transition
→ may advance locally

backend-authoritative transition
→ remain on the safe current state
→ never fabricate verification/authentication/recovery/link/session success
```

## Materialized frontend baseline

The completed pre-backend Web materialization includes:

- production SignIn shell and complete approved Access surface inventory;
- staged signup, recovery/reset, provider pending/error, account-link, reauth and lightweight setup/first-run surfaces;
- feature-local Access state model and reducer tests;
- IT/EN resources and persisted locale preference with `<html lang>` synchronization;
- local frontend validation without fake backend success;
- password show/hide, paste and password-manager-safe behavior;
- browser offline integration;
- design-token and feature-boundary enforcement;
- Testing Library coverage;
- Playwright production-preview coverage;
- axe accessibility automation;
- responsive release-matrix coverage including phone, tablet/narrow, compact desktop and large desktop pressure;
- reduced-motion and overflow checks;
- final large-desktop auth-card width refined to a 480px maximum while preserving compact-desktop behavior.

The accepted Web frontend is intentionally backend-incomplete rather than backed by a disposable fake Auth service.

## Password policy

```text
minimum                    12 characters
support                    >=64 characters
mandatory composition      none
paste/password manager     allowed
show/hide                   allowed
common/breached blocklist  required server-side
```

Do not add arbitrary composition rules merely because another product uses them.

## Provider, verification, recovery and session contract

Provider authentication must use the current official provider mechanism/assets where required. DANTE owns transaction binding, pending/failure feedback, backend validation handoff, collision/linking UX and authenticated return; it does not fake provider chooser/consent UI or collect provider credentials.

Account collision must follow:

```text
collision
→ prove control of existing DANTE account
→ explicit link decision
→ backend-authoritative link
```

Recovery start remains neutral to account existence. Verification/recovery proofs are backend-owned, short-lived and replay/single-use aware. Backend session state remains authoritative for bootstrap, expiry, revocation and reauthentication.

Never log or persist raw password, OTP, recovery proof, OAuth authorization code, PKCE verifier, provider token/assertion, access token, refresh token or session secret outside the approved security design.

## Accessibility and responsive quality

Release target is WCAG 2.2 AA-quality behavior. Automated axe is necessary but not sufficient; keyboard/focus behavior, text expansion, zoom, reduced motion, mobile/touch usability and product review remain part of acceptance for changed surfaces.

Representative Web pressure includes at least phone widths around 390–430px, tablet/narrow around 768–820px, compact desktop around 1024–1280px, accepted desktop around 1440–1536px and large desktop where composition can become too sparse or wide.

## Architecture boundary

The real integration path is:

```text
FastAPI stable Auth OpenAPI
→ generated typed client (`@dante/api-client` / current repository authority)
→ remote-state/query boundary where justified
→ existing Access state graph
→ real provider/session/recovery flows
→ full-stack E2E
```

Do not introduce a fake-success Auth adapter merely to make the frontend reachable.

## Not implemented by this closed frontend workstream

The following are not claimed complete:

```text
real account creation / credential authentication
email verification proof validation
recovery proof validation / reset mutation
Google / Apple backend transaction validation
secure account linking
session establishment/bootstrap/expiry/revocation
reauthentication backend behavior
server rate-limit/error mapping
stable Auth OpenAPI
generated real Auth client binding
frontend/backend Auth integration
full-stack isolated E2E
real authenticated Home handoff
final Terms/Privacy destinations/content
native Mobile Access
```

These belong to the next bounded full-stack Access/Auth product vertical. That vertical starts from current protected `main`; it does not reopen this completed pre-backend frontend materialization unless real integration proves a frontend defect or required contract adjustment.

## Quality / change rule

Future Access UI changes remain allowed after backend integration. Pure visual polish can change layout, spacing, typography, geometry or motion under normal review without redesigning backend semantics. Changes to state meaning, provider/linking behavior, session/recovery semantics or backend-authoritative transitions require full-stack contract review.

Production code never imports prototype implementation. Frozen Access prototype material remains recoverable on `prototype/access-system`; current production truth is this document plus current code/tests and later full-stack contracts.
