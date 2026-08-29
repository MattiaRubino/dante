# DANTE — Access frontend contract

- **Status:** CURRENT / AUTHORITATIVE FOR MATERIALIZED WEB ACCESS THROUGH CLOSED M4 + FROZEN M5.1 WEB SEMANTICS
- **Scope:** accepted Web Access baseline, closed M3 signin/session/logout, closed M4 lifecycle, and frozen M5 provider/passkey/linking/smart-onboarding requirements before runtime materialization
- **M4 final accepted implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **M5 architecture authority:** `../architecture/access-auth-m5-contract.md`
- **M5 live handoff:** `../workstreams/access-auth-m5-live-handoff-2026-08-29.md`
- **Frozen design source:** `prototype/access-system` at `469b68370e80185fa8a16d5335845e402ee1de3b`
- **Current workstream:** `../workstreams/access-auth.md`

## 1. Purpose

Access gets an unauthenticated person to a server-authoritative DANTE AuthSession and through the materialized account lifecycle. M5 extends the same product boundary to Google, Apple, passkeys and explicit linking without creating a second Auth UI/application architecture.

Current runtime capability ends at M4. M5.1 statements in this file are frozen **requirements**, not claims that provider/passkey runtime code already exists.

---

## 2. Product invariants

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
signin != external-integration authorization
provider state != canonical DANTE state
provider identity != provider email
provider authentication != permission to read provider data
provider profile bootstrap != continuous provider-owned profile sync
verification != profile setup
reauthentication != initial signin
client/device signal != person identity
frontend request/provider callback != backend-authoritative success
unknown/loading != signed-out/empty
method != factor != assurance
```

Google/Apple authentication remains an Auth mechanism only. Gmail, Calendar, iCloud and other provider-data access require separate explicit integration authorization and lifecycle.

---

## 3. Visual / UX baseline

The accepted Web Access design direction remains production baseline. M5 does not justify gratuitous redesign.

Composition:

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

Geometry remains a system:

```text
content bounds
auth-panel width
spacing scale
control heights
radius hierarchy
typography hierarchy
responsive breakpoints
elevation/surface roles
```

Use governed semantic tokens/roles. Mobile-Web is not scaled desktop. Native Mobile Access remains M6.

Provider controls use official branding/HIG requirements rather than DANTE-drawn fake Google/Apple consent surfaces.

---

## 4. Canonical Access states

Current/frozen state vocabulary includes:

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

M5 implementation may refine provider/passkey substate representation without turning every transport phase into a permanent product state.

Orthogonal conditions remain:

```text
idle
backend-required
offline
server-unavailable
rate-limited
provider-unavailable
```

Permanent transition rule:

```text
frontend-owned transition
→ may advance locally

backend-authoritative transition
→ advance only from real backend result
→ never fabricate auth/verification/recovery/link/passkey/session success
```

Preserve `REQUEST_* = intent` and `SERVER_* = backend-authoritative result`.

---

## 5. Materialized Web baseline through M4

Production Web Access currently includes:

```text
accepted SignIn shell + Access visual/state system
IT/EN resources + locale preference + html lang sync
local UX validation without fake backend success
password show/hide, paste and password-manager-safe behavior
offline/server/rate-limit states
design-token and feature-boundary enforcement
responsive/reduced-motion/accessibility foundations

M3:
real email/password signin
real authoritative session bootstrap
real current-session logout
TanStack Router critical-session bootstrap
TanStack Query remote lifecycle
real failure/rate-limit mapping

M4:
real signup initiation
real six-digit email OTP verification/resend
real existing-account result after mailbox proof
real neutral recovery initiation
recovery-link capture + proof validation
immediate recovery URL fragment scrub
memory-only recovery bearer
real password reset
fresh-signin requirement after reset
real reauthentication
same-session bearer rotation
M4 governed generated-client integration
```

Setup persistence/HOME behavior beyond accepted Auth handoff remains owned by later product work unless M5 needs bounded bootstrap staging to prevent provider data loss.

---

## 6. Production integration path

Current Web architecture remains:

```text
TanStack Router
→ route loader / route context
→ Access feature public API
→ TanStack Query
→ feature Auth application boundary
→ platform Web Auth remote
→ governed @dante/api-client
→ same-origin /api/v1
→ FastAPI
→ PostgreSQL
```

Ownership:

```text
route
→ navigation/bootstrap coordination only

Access feature
→ product/application Auth behavior + Access state graph

TanStack Query
→ remote request/cache lifecycle only

Web Auth remote
→ browser transport/provider/passkey orchestration policy

@dante/api-client
→ governed wire contract/runtime validation

backend + PostgreSQL
→ canonical Auth authority
```

Route code imports Access capabilities only through `features/access/index.ts`; route-level deep imports are forbidden. Presentation/reducer code does not import raw Orval internals or call raw `fetch`.

Provider SDK/browser APIs must be wrapped behind bounded platform/application adapters rather than leaking throughout presentation components.

---

## 7. Web transport/security contract

The normal Web Auth remote owns:

```text
same-origin relative API use
credentials: same-origin
Accept: application/json / application/problem+json
X-Dante-Client: web
CSRF injection for applicable authenticated unsafe mutations
AbortSignal propagation
safe header handling
```

Browser-owned `Origin` and `Sec-Fetch-Site` are not forged by application code.

Mutation retry remains disabled. `retryable=true` is never blanket permission to replay a mutation. Auth state/query cache is not persisted to localStorage/sessionStorage.

M4 recovery secret rule remains:

```text
URL fragment
→ capture once into transient memory
→ scrub immediately
→ never browser persistent storage
→ never ordinary query persistence/logging
```

M5 provider callback routes may follow provider-defined protocol methods/content types. They do not weaken the normal same-origin CSRF contract globally.

---

## 8. Session bootstrap contract — permanent M3 regression rule

Rejected:

```text
Access reducer initially SIGN_IN
→ paints login
→ GET /auth/session
→ effect repairs state
```

Accepted:

```text
hard document load
→ TanStack Router loader resolves/prefetches /auth/session
→ Query cache populated
→ AccessPage mounts
→ first business render already SIGNED_IN or SIGNED_OUT
```

```text
UNKNOWN / LOADING
!= SIGNED_OUT
!= SIGNED_IN
!= ERROR
```

M5 provider/passkey returns must converge through the same authoritative session model rather than adding client-only “Google logged in” truth.

---

## 9. Password UX / policy

Existing policy remains:

```text
minimum                    15 Unicode code points
support                    >=64 characters
mandatory composition      none
paste/password manager     first-class
show/hide                   allowed
silent truncation           forbidden
breach screening            server-side HIBP
periodic forced change      not used without security reason
```

M5 adds a future authenticated **Add password** path for Accounts created with provider/passkey only. The frontend does not assume a password always exists.

---

## 10. M4 lifecycle UX — closed regression baseline

Signup:

```text
SIGN_UP_EMAIL
→ SIGN_UP_PASSWORD
→ REQUEST_SIGN_UP
→ pending challenge only
→ VERIFY_EMAIL
→ REQUEST_VERIFY_EMAIL
```

New email valid OTP establishes Account + verified EmailIdentity + PasswordCredential + AuthSession.

Existing email:

```text
before mailbox proof → no existence disclosure
after valid proof    → existing_account guidance
no authentication
no password overwrite
```

Recovery:

```text
FORGOT_PASSWORD
→ neutral request
→ RECOVERY_SENT
→ recovery link capture/scrub/validate
→ RESET_PASSWORD
→ reset
→ RESET_COMPLETE
→ fresh SIGN_IN
```

Reauth:

```text
SERVER_REAUTH_REQUIRED
→ REAUTH
→ fresh evidence
→ backend rotates exact bearer on same AuthSession
→ SERVER_REAUTH_SUCCEEDED
```

These remain M5 regression requirements.

---

# 11. M5.1 Web semantics — FROZEN, NOT YET MATERIALIZED

M5 Access target adds:

```text
Continue with Google
Continue with Apple
Use a passkey
email/password path remains available
```

Provider/pipeline success never directly mutates canonical signed-in UI state until the DANTE server establishes/returns authoritative session outcome.

---

## 12. Google UX

Initial direction:

```text
official Google Identity Services button/branding
explicit user initiation
FedCM-compatible current GIS behavior where supported
auto-select off by default
One Tap not required for M5 closure
```

DANTE does not collect Google credentials or fake Google account chooser/consent UI.

Provider cancel returns to a stable Access state; it is not shown as an alarming application error unless provider semantics warrant it.

Provider dependency failure uses normal safe server/dependency UX, never fake authentication success.

---

## 13. Apple UX

Use official Sign in with Apple branding/current Human Interface requirements.

Expected browser lifecycle:

```text
user starts Apple
→ provider navigation/popup according to final adapter
→ Apple callback/return
→ PROVIDER_PENDING while DANTE validates server-side
→ backend result
→ authenticated / link-required / safe error
```

Private Email Relay is respected. DANTE does not show “now give us your real email” merely because the user selected Hide My Email.

Apple first-authorization name fields may be used for bootstrap but are not shown as provider-certified identity facts.

---

## 14. Provider-enriched smart onboarding

This is a direct M5 product requirement.

First Account creation may receive useful data:

Google examples:

```text
name
given_name
family_name
picture
locale
email
```

Apple examples:

```text
first_name / last_name on first authorization
email / Private Relay
```

UX rule:

```text
validated provider bootstrap available
→ pre-fill or skip redundant setup steps
→ ask only for missing information
```

Examples:

```text
Google gives name + locale
→ do not force the user to type them again without product reason

Apple gives first/last name once
→ preserve them through the bootstrap handoff so closing/reloading does not lose one-shot data
```

Provider data becomes **initial input**, not continuous synchronization.

```text
user later edits name/avatar/locale in DANTE Settings
→ DANTE-owned value wins permanently until user changes it again
```

No automatic `@username` is generated because DANTE has no frozen username concept.

### Avatar

Provider picture URL is a suggestion/bootstrap source, not automatically a canonical DANTE Asset. A later accepted avatar import must go through the proper media/Asset owner.

### Locale

Explicit DANTE choice outranks provider/browser suggestion.

---

## 15. ACCOUNT_LINK UX

Email coincidence never silently links.

Provider-first collision direction:

```text
provider proof
→ backend detects collision
→ ACCOUNT_LINK
→ explain that an existing DANTE Account must be confirmed
→ user authenticates existing Account with any accepted method
→ explicit “Link/Continue” decision
→ backend finalizes atomically
```

Do not reveal unnecessary account metadata before sufficient proof.

Do not assume password; passkey/other accepted methods may prove the existing Account.

After successful link, product UI reflects backend truth and the initiating AuthSession lifecycle according to M5 API contract.

---

## 16. Passkey UX

M5 must provide real passkey signin and a real registration entry point.

Signin:

```text
Use a passkey
→ browser/platform passkey selector
→ username-less/discoverable credential
→ DANTE verifies
→ canonical AuthSession
```

Support platform-native passkey experiences including password managers/security keys/cross-device flows where supported. Do not build a fake DANTE passkey chooser for authenticators the browser/platform owns.

Passkey cancel is a normal recoverable state. User may return to other sign-in methods.

`userVerification` is required by backend policy; UI does not claim biometric semantics because the authenticator may use device PIN/other verification.

Conditional mediation/autofill may enhance future UX but explicit `Use a passkey` remains functional.

### Registration

Until authenticated Home Settings exists, M5 may expose a bounded optional post-auth/onboarding security prompt for adding a passkey.

Do not create hidden production test routes/endpoints merely for UAT.

---

## 17. Authentication-method management readiness

M5 backend/application must support future Home → Security & Access settings:

```text
Google identities
Apple identities
password present/absent
passkeys 0..N
add/remove operations
safe recovery path
```

Full long-lived management UI can be materialized with Home/Settings, but M5 must not bake in assumptions that make it impossible without Auth redesign.

Anti-lockout is backend-authoritative:

```text
normal remove provider/passkey/password
→ reject if resulting Account has no viable auth/recovery path
```

Frontend should explain why removal is unavailable rather than merely disabling without reason.

---

## 18. Passwordless recovery UX

Provider/passkey-only Account may have no password.

If all such authenticators are lost and user proves the strong existing email recovery channel:

```text
recovery link/proof
→ create first password (not just replace)
→ RESET_COMPLETE
→ all old AuthSessions revoked
→ fresh SIGN_IN
```

The public recovery initiation remains anti-enumeration neutral.

M5.2 freezes exact API/state differences; UI must not fork into a weaker “email = instant login” shortcut.

---

## 19. Auth vs provider-data integrations in UI

DANTE must present these as different user concepts:

```text
Sign-in methods / Security
├── Google login
├── Apple login
├── Password
└── Passkeys

Connected apps / Integrations
├── Google Calendar
├── Gmail
├── iCloud/Calendar
└── future services
```

A user unlinking a sign-in method must not unexpectedly lose unrelated integration consent, and disconnecting an integration must not sign the user out of DANTE.

Exact Home Settings surfaces are later, but this conceptual separation is frozen now.

---

## 20. Accessibility / responsive quality

Release target remains WCAG 2.2 AA-quality behavior.

M5 changed surfaces must review:

```text
keyboard/focus return across provider navigation
screen-reader names for provider/passkey controls
loading/pending/error announcements
text expansion/zoom
reduced motion
touch/mobile-Web behavior
provider popup/redirect recovery
passkey browser-dialog cancel/retry
account-link explanation/focus order
offline/server/provider unavailable states
```

Representative pressure:

```text
phone              ~390–430px
tablet/narrow      ~768–820px
compact desktop    ~1024–1280px
accepted desktop   ~1440–1536px
large desktop      excessive-sparsity/composition pressure
```

Provider buttons must fit the established card/geometry without violating provider branding requirements.

---

## 21. Browser / platform constraints

Current M4 test ingress uses `https://127.0.0.1:4173`.

M5 WebAuthn target test posture:

```text
https://localhost:<ephemeral-port>
RP ID = localhost
```

or equivalent reviewed domain setup.

Apple real Web acceptance requires a registered HTTPS domain; local fake-provider browser proof is necessary but not sufficient for production-ready Apple closure.

Critical product browser semantics remain Chromium + Firefox + WebKit. Engine-specific provider/passkey automation gaps are documented truthfully rather than bypassed/faked.

---

## 22. Web application/data-source testing

Application-level tests must prove mappings such as:

```text
provider cancel → stable non-authenticated Access state
provider dependency unavailable → provider/server error state, never authenticated
link_required → ACCOUNT_LINK
link success only after SERVER_* result
passkey cancel → recoverable signin state
passkey failure → no fake session
provider bootstrap → prefill/skip only initial values
later user-owned value → provider bootstrap cannot overwrite
unknown future provider machine code → category/status safe fallback
```

Presentation/reducer tests do not import raw generated Orval internals.

---

## 23. Accepted Web proof through M4

```text
Web Access UI                                22 / 22 PASS
real Auth full-stack browser                 33 / 33 PASS
Chromium                                     11 / 11 PASS
Firefox                                      11 / 11 PASS
WebKit                                       11 / 11 PASS
real production Vite build                   PASS
real same-origin HTTPS                       PASS
real FastAPI/PostgreSQL/SMTP boundary        PASS
manual integrated M4 UAT                     PASS / USER ACCEPTED
```

This remains regression evidence, not M5 provider/passkey proof.

---

## 24. M5 proof direction

Mandatory deterministic CI:

```text
real DANTE generated client/Web application
real FastAPI/security/application path
real PostgreSQL where persistence involved
protocol-faithful local provider substitute
```

M5 additionally needs real-provider smoke/UAT before closure.

Passkey proof must include real WebAuthn verification/credential lifecycle; fake reducer success is insufficient.

Do not multiply low-level races across every browser. Use browser matrix for product/browser semantics and real PostgreSQL/protocol tests for backend invariants.

---

## 25. Deferred obligations after M5.1

```text
M5.2
exact persistence/API/provider callback design

M5 implementation
Google / Apple / passkeys / linking / smart onboarding / add-password / passwordless recovery

M6
Native Mobile Access

M7
complete session/device/account-security management UX
new-login alerts / “this wasn’t me”
whole-vertical hardening
production observability
final Terms/Privacy/accessibility/dependency/release QA
real authenticated handoff
whole-vertical acceptance
```

Do not describe M3/M4 capabilities as incomplete because M5–M7 are open. Do not describe M5 as implemented because M5.1 is closed.

---

## 26. Quality / change rule

Future Access UI changes are allowed when real M5 integration proves a missing state or defect. State semantics/backend authority require full-stack review.

Production code never imports prototype implementation.

Current truth is:

```text
this document
+ current apps/web code/tests
+ access-auth-m5-contract.md for frozen M5 semantics
+ current Access/Auth architecture/security/API/testing contracts
+ active workstream/handoff
```

The frozen prototype remains recoverable design evidence only.