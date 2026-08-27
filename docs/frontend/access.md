# DANTE — Access frontend contract

- **Status:** CURRENT / AUTHORITATIVE FOR THE MATERIALIZED WEB ACCESS FRONTEND
- **Scope:** accepted Web Access baseline in `apps/web` plus current full-stack integration obligations for `feature/access-auth`
- **Frozen design source:** `prototype/access-system` at `469b68370e80185fa8a16d5335845e402ee1de3b`
- **Current workstream authority for newer unmerged full-stack decisions:** `../workstreams/access-auth.md`

## Purpose

Access gets an unauthenticated person to an authenticated DANTE session and, for a new account, through the smallest useful first-run handoff.

This document owns the current production-frontend contract carried forward from the frozen Access design work and completed Web materialization. Implementation truth remains the checked-out code/tests. The frozen prototype branch is historical design evidence and must not override newer production code, this contract or the active full-stack workstream record.

## Product invariants

```text
Person != Account != Principal != Actor
sign-in != external-integration authorization
provider state != canonical DANTE state
provider authentication != permission to read provider data
verification != profile setup
reauthentication != initial sign-in
client/device signal != person identity
frontend request/success != backend-authoritative success
```

Google/Apple sign-in authenticates a DANTE account only. Gmail, Calendar, iCloud and other provider-data permissions are separate explicit integration flows.

## Access Visual / UX Freeze — accepted 2026-08-27

The current Web Access design direction is accepted as the production integration baseline. It must not be redesigned merely for novelty while backend work begins.

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

### Geometry rule

Access must remain a system, not a collection of one-off visual placements.

When the surface is touched, preserve or deliberately evolve a coherent contract for:

- content bounds;
- auth-panel width;
- spacing scale;
- control heights;
- radius hierarchy;
- typography hierarchy;
- desktop/compact/tablet/phone breakpoints;
- elevation/surface roles.

Use semantic design-system/token roles where available rather than adding unrelated repeated raw values. Visual polish may change exact values after review, but the geometry must remain governed and internally consistent.

Mobile is not a scaled desktop. Native Mobile Access is a later implementation macro-phase against the same canonical backend semantics.

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

## Materialized Web baseline

The completed pre-backend Web materialization includes:

- production SignIn shell and approved Access surface inventory;
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

The Web frontend is intentionally backend-incomplete rather than backed by a disposable fake Auth service.

## Password UX / policy contract

The earlier 12-character minimum is superseded by the current full-stack Access/Auth decision for password-only authentication:

```text
minimum                    15 characters
support                    >=64 characters
mandatory composition      none
paste/password manager     allowed / first-class
show/hide                   allowed
silent truncation           forbidden
common/breached blocklist  required server-side
periodic forced change      not used without a security reason
```

Do not add arbitrary composition rules merely because another product uses them.

The server remains authoritative for breached/common-password rejection and any final password acceptance semantics. Frontend validation may provide early feedback but must not become a second independent policy authority.

## Session / multi-device frontend contract

DANTE supports concurrent Web and Native sessions for the same Account.

The frontend must therefore never assume:

```text
one Account == one current session globally
```

Instead:

```text
one Account
→ multiple independent AuthSessions across allowed clients
```

Consequences for Web Access/session UI:

- current-session logout revokes only the current AuthSession unless the user explicitly chooses a broader action;
- future logout-all/session-management UI must be possible without changing account semantics;
- session expiry/revocation must be reflected from backend-authoritative state;
- a valid session on another device must not be treated as an error;
- IP/User-Agent/device descriptions are presentation metadata, not identity proof;
- global session bootstrap is separate from one form reducer lifecycle.

## Provider contract

Provider authentication must use the current official provider mechanism/assets where required at real integration time.

The existing pre-backend custom Google/Apple button presentation is a visual baseline only; it is **not** final compliance authority for the production provider integration.

DANTE owns:

- transaction binding;
- pending/failure feedback;
- backend validation handoff;
- collision/linking UX;
- authenticated return;
- canonical DANTE Account/AuthSession state.

DANTE must not:

- fake provider chooser/consent UI;
- collect provider credentials;
- treat provider email alone as proof of an existing DANTE account;
- silently convert authentication provider permissions into Gmail/Calendar/iCloud integration permissions.

Account collision follows:

```text
collision
→ prove control of existing DANTE account
→ explicit link decision
→ backend-authoritative link
```

## Passkeys and future MFA

The full-stack architecture is passkey-ready and the production roadmap includes passkeys/WebAuthn.

The Web frontend must therefore avoid assumptions such as:

```text
all Accounts always have a password
```

Future passkey surfaces must consume the same Access application/session contract rather than create a parallel login product.

MFA/TOTP/recovery codes/step-up MFA are intentionally deferred. Current UI and state semantics must not prevent their later addition, but no MFA surface should be invented before that future product/security gate.

## Verification, recovery and session contract

Recovery start remains neutral to account existence where security requires anti-enumeration.

Verification/recovery proofs are backend-owned, short-lived and replay/single-use aware.

Backend session state remains authoritative for:

- bootstrap;
- expiry;
- revocation;
- reauthentication/recent-auth;
- account-disable/security-policy effects;
- logout/logout-all results.

Never log or persist raw password, OTP, recovery proof, OAuth authorization code, PKCE verifier, provider token/assertion, access token, refresh token or session secret outside the approved security design.

## Accessibility and responsive quality

Release target is WCAG 2.2 AA-quality behavior.

Automated axe is necessary but not sufficient. Changed/real-integrated surfaces must also review:

- keyboard and focus behavior;
- text expansion and zoom;
- reduced motion;
- touch/mobile-Web usability;
- screen-reader semantics where changed;
- autofill/password-manager behavior;
- loading/pending/error announcements;
- offline/server-unavailable/rate-limited states;
- provider-return states.

Representative Web pressure includes at least:

```text
phone              ~390–430px
tablet/narrow      ~768–820px
compact desktop    ~1024–1280px
accepted desktop   ~1440–1536px
large desktop      composition pressure / excessive sparsity check
```

## Architecture boundary

The real Web integration path is:

```text
FastAPI stable Auth OpenAPI
→ generated typed client (`@dante/api-client` / current repository authority)
→ Access application / remote-state boundary
→ existing Access state graph
→ real provider/session/recovery/passkey flows
→ full-stack E2E
```

Do not introduce a fake-success Auth adapter merely to make the frontend reachable.

Preserve the semantic split:

```text
REQUEST_* = user intent
SERVER_*  = backend-authoritative result
```

Transport details belong behind the application/data-source boundary; presentation/reducer code must not couple directly to raw `fetch` response shapes or parse English error strings.

## Native Mobile relationship

The repository already has an Expo + React Native + Expo Router foundation. Native Mobile Access is not implemented by the closed Web materialization, but it is now an explicit later macro-phase of the same full-stack Access/Auth vertical.

Native Mobile must consume the same canonical:

```text
Account
AuthSession
Principal
provider/linking/recovery semantics
```

while using client-appropriate secure transport/storage rather than forcing browser-cookie semantics into the domain/application layer.

## Deferred integration / closure obligations

The following are not claimed complete merely because the Web visual baseline is accepted:

```text
real account creation / credential authentication
email verification proof validation
recovery proof validation / reset mutation
Google / Apple backend protocol validation
passkey/WebAuthn registration and authentication
secure account linking
session establishment/bootstrap/expiry/revocation
multi-session management backend behavior
reauthentication backend behavior
server rate-limit/error mapping
stable Auth OpenAPI
generated real Auth client binding
frontend/backend Auth integration
full-stack isolated E2E
real authenticated Home handoff
final Terms/Privacy destinations/content
native Mobile Access
final real-backend loading/error/autofill/provider visual QA
```

These belong to the current `feature/access-auth` full-stack workstream and its definitive seven-macro-phase roadmap.

## Terms / Privacy

Terms and Privacy remain placeholder destinations in the current pre-backend surface. Before Access/Auth closure they must become real product destinations/content according to the appropriate legal/product gate. Do not leave non-functional legal affordances in a production release.

## Quality / change rule

Future Access UI changes remain allowed when real backend/provider/mobile integration proves a frontend defect, missing state or required contract adjustment.

Pure visual polish may change layout, spacing, typography, geometry or motion under normal review without redesigning backend semantics, provided the visual system remains coherent.

Changes to state meaning, provider/linking behavior, session/recovery semantics, passkey semantics or backend-authoritative transitions require full-stack contract review.

Production code never imports prototype implementation. Frozen Access prototype material remains recoverable on `prototype/access-system`; current production truth is this document plus current code/tests and the active full-stack workstream record until integration.
