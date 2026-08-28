# DANTE — Access frontend contract

- **Status:** CURRENT / AUTHORITATIVE FOR MATERIALIZED WEB ACCESS + CLOSED M3 AUTH INTEGRATION
- **Scope:** accepted Web Access baseline in `apps/web`, closed M3 signin/session/logout integration and carry-forward obligations for M4–M7
- **Frozen design source:** `prototype/access-system` at `469b68370e80185fa8a16d5335845e402ee1de3b`
- **Current workstream:** `../workstreams/access-auth.md`

## 1. Purpose

Access gets an unauthenticated person to a server-authoritative authenticated DANTE session and, in later phases, through the smallest useful first-run/account-lifecycle handoff.

This document owns the production Web Access contract. Implementation truth remains current code/tests. The frozen prototype is historical visual evidence and must never override current production code, the active full-stack workstream or newer accepted architecture/security decisions.

---

## 2. Product invariants

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
signin != external-integration authorization
provider state != canonical DANTE state
provider authentication != permission to read provider data
verification != profile setup
reauthentication != initial signin
client/device signal != person identity
frontend request/success != backend-authoritative success
unknown/loading != signed-out/empty
```

Google/Apple authentication is an Auth mechanism only. Gmail, Calendar, iCloud and other provider-data access require separate explicit integration authorization.

---

## 3. Visual / UX baseline

The accepted Web Access design direction remains the production baseline. Do not redesign it merely for novelty when a backend phase changes.

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

Use governed semantic tokens/roles where available. Mobile-Web is not scaled desktop. Native Mobile Access remains M6 and may use platform-appropriate composition against the same canonical backend semantics.

---

## 4. Canonical Access states

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

Orthogonal conditions are not Account/Auth states:

```text
idle
backend-required
offline
server-unavailable
rate-limited
```

Permanent transition rule:

```text
frontend-owned transition
→ may advance locally

backend-authoritative transition
→ advance only from real backend result
→ never fabricate auth/verification/recovery/link/session success
```

Preserve:

```text
REQUEST_* = user/application intent
SERVER_*  = backend-authoritative result
```

A `REQUEST_SIGN_IN` transition may never itself establish authenticated state.

---

## 5. Materialized Web baseline through M3

The production Web Access system now includes:

- accepted SignIn shell and full pre-backend Access surface inventory;
- staged signup/recovery/reset/provider/linking/reauth/setup surfaces for later real integration;
- feature-local Access reducer/model and tests;
- IT/EN resources and persisted locale preference with `<html lang>` synchronization;
- local frontend validation without fake backend success;
- password show/hide, paste and password-manager-safe behavior;
- browser offline integration;
- design-token and feature-boundary enforcement;
- responsive/reduced-motion/accessibility foundations;
- real M3 email/password signin;
- real authoritative session bootstrap;
- real current-session logout;
- real server failure/rate-limit mapping used by the M3 spine;
- deterministic governed Auth API client integration;
- TanStack Query remote lifecycle;
- Router-first critical Auth bootstrap;
- full-stack cross-browser proof through real FastAPI/PostgreSQL.

M3 closes only the real email/password + AuthSession spine. Later Access surfaces remain non-authoritative until their M4/M5/M7 backend slices exist.

---

## 6. Production M3 integration path

Current Web architecture:

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

Important ownership:

```text
route
→ navigation/bootstrap coordination only

Access feature
→ product/application Auth behavior + Access state graph

TanStack Query
→ remote request/cache lifecycle only

Web Auth remote
→ browser transport policy

@dante/api-client
→ governed wire contract/runtime validation

backend + PostgreSQL
→ canonical Auth authority
```

Route code imports Access capabilities only through `features/access/index.ts`; route-level deep imports into `features/access/application/*` are forbidden.

Presentation/reducer code does not import generated Orval internals or call raw `fetch`.

---

## 7. Web transport contract

The Web Auth remote owns:

```text
same-origin relative API use
credentials: same-origin
Accept: application/json / application/problem+json
X-Dante-Client: web
CSRF injection only for authenticated unsafe mutation
AbortSignal propagation
safe header handling
```

Browser-owned `Origin` and `Sec-Fetch-Site` are not manually forged by application code.

Mutation retry is disabled. Session GET may use only the bounded accepted transient retry behavior. `retryable=true` in a problem response is never blanket permission to replay a mutation.

Auth state/query cache is not persisted to localStorage/sessionStorage.

---

## 8. Session bootstrap contract — M3 UAT regression rule

This rule is now permanent because manual UAT found a real defect.

### Rejected first implementation

```text
Access reducer initially SIGN_IN
→ AccessPage paints login
→ GET /auth/session resolves authenticated
→ effect repairs state after paint
```

Result: a visible login flash on authenticated F5.

### Rejected mitigation

```text
render a real sign-in panel
→ hide its form while /auth/session is pending
→ preserve nominal geometry
```

Result: login flash disappeared but refresh recomposition/rimbalzo became visibly worse. This pattern is rejected.

### Accepted implementation

Critical Auth bootstrap is route-coordinated:

```text
hard document load
→ TanStack Router loader resolves/prefetches authoritative /auth/session
→ Query cache populated
→ AccessPage mounts
→ first business render is already SIGNED_IN or SIGNED_OUT
```

The freshly loader-resolved session is briefly fresh so loader → component mount does not immediately issue a duplicate session read. Subsequent refetches are background lifecycle and must not throw the resolved UI back into bootstrap or signed-out state.

Permanent frontend rule:

```text
UNKNOWN / LOADING
!= SIGNED_OUT
!= SIGNED_IN
!= ERROR
```

When a remote fact is critical to the correctness of the first screen, the application must not display a false empty/signed-out state while waiting merely because that is the reducer's convenient default.

### Hard-refresh visual acceptance

Manual Firefox video comparison after the Router-first fix established:

```text
false login paint                NO
Access card/brand layout jump    NO app-level regression
brief whole-document blank       browser hard-reload repaint
manual acceptance                PASS
```

Do not reintroduce false Auth states to hide a browser-owned document repaint. A future global HTML/shell paint optimization is a separate Web-platform polish decision, not an M3 Auth fix.

---

## 9. Password UX / policy

Current password-only Auth policy:

```text
minimum                    15 Unicode code points
support                    >=64 characters
request resource bound     current API contract
mandatory composition      none
paste/password manager     allowed / first-class
show/hide                   allowed
silent truncation           forbidden
breach screening            server-side HIBP policy
periodic forced change      not used without a security reason
```

Frontend validation is UX. Backend policy remains authoritative.

---

## 10. Session / multi-client contract

DANTE supports concurrent independent AuthSessions.

Never assume:

```text
one Account == one global current session
```

Instead:

```text
one Account
→ 0..N independent AuthSessions
```

Consequences:

- current logout revokes only the current AuthSession;
- another browser/context session may remain authenticated;
- future revoke-all/session-management is a separate explicit intent;
- expiry/revocation are reflected from backend-authoritative bootstrap/admission;
- IP/User-Agent/device metadata is presentation/risk signal, not identity proof;
- global session bootstrap is not one form reducer lifecycle.

M3 full-stack proof directly verifies two independent BrowserContexts and server-side revoke/expiry convergence.

---

## 11. Provider contract

Provider authentication must use current official provider protocols/assets at M5 implementation time.

The existing pre-M5 Google/Apple button presentation remains only a visual baseline, not final provider compliance authority.

DANTE owns:

```text
transaction binding
pending/failure feedback
backend validation
collision/linking UX
authenticated return
canonical DANTE Account/AuthSession state
```

DANTE must not:

```text
fake provider chooser/consent UI
collect provider credentials
use provider email alone as existing-account identity proof
silently link Accounts from matching email
reuse provider Auth permission as Gmail/Calendar/iCloud data permission
```

Collision remains:

```text
collision
→ prove existing DANTE Account control
→ explicit link decision
→ backend-authoritative link
```

---

## 12. Passkeys and future MFA

The architecture is passkey-ready. Frontend code must not assume every Account always has a password.

M5 passkey surfaces must reuse the canonical Access/Auth application/session boundary rather than create a parallel login system.

MFA/TOTP/recovery codes/step-up MFA remain deferred. Do not invent an `mfa_enabled` Boolean as a substitute for an assurance/evidence model.

---

## 13. Verification, recovery and reauth relationship

M4 will materialize the backend authority for:

```text
signup/account establishment
email verification
neutral recovery initiation
single-use/replay-safe recovery proof
password reset
post-reset session policy
reauthentication/recent-auth
```

Until then, corresponding prebuilt UI surfaces remain presentation/state scaffolding and may not claim canonical success.

Recovery initiation remains anti-enumeration neutral where required. Verification/recovery secrets remain backend-owned, short-lived and replay-aware.

Never log or persist raw password, OTP, recovery proof, OAuth authorization code, PKCE verifier, provider token/assertion, session bearer secret or CSRF secret outside the approved security design.

---

## 14. Accessibility / responsive quality

Release target remains WCAG 2.2 AA-quality behavior.

Automation is necessary but not sufficient. Changed integrated surfaces must review:

```text
keyboard/focus
text expansion/zoom
reduced motion
touch/mobile-Web behavior
screen-reader semantics
autofill/password-manager behavior
loading/pending/error announcements
offline/server-unavailable/rate-limited states
provider-return states when M5 lands
```

Representative pressure:

```text
phone              ~390–430px
tablet/narrow      ~768–820px
compact desktop    ~1024–1280px
accepted desktop   ~1440–1536px
large desktop      excessive-sparsity/composition pressure
```

---

## 15. M3 Web proof

Accepted local/canonical evidence:

```text
TypeScript typecheck                 PASS
ESLint                               PASS
Vitest                               6 files / 25 tests PASS
architecture dependency cruise       PASS
Prettier                             PASS
production Vite build                PASS
generated source drift               PASS
```

Real full-stack browser proof:

```text
Chromium  7 / 7 PASS
Firefox   7 / 7 PASS
WebKit    7 / 7 PASS
TOTAL     21 / 21 PASS
```

Critical scenarios:

```text
real signin / secure cookie / logout
bootstrap with delayed real session and no false signin render
wrong credentials
independent sessions
server-side revoke
server-side expiry
real PostgreSQL unavailable
real signin rate-limit 429
```

Manual UAT accepted the final Router-first refresh behavior.

---

## 16. Deferred obligations after M3

M3 is closed. Remaining Access/Auth frontend/full-stack work belongs to later macro-phases:

```text
M4
real account creation
email verification
recovery/reset
reauth/recent-auth

M5
Google / Apple protocol validation
passkeys/WebAuthn
secure explicit account linking
provider collision UX

M6
Native Mobile Access

M7
whole-vertical session-management/security hardening
final Terms/Privacy destinations/content
final provider/legal/accessibility/release QA
real authenticated handoff into next product vertical
whole-vertical user acceptance
```

Do not describe M3 signin/session/logout as incomplete merely because M4–M7 are still open.

---

## 17. Quality / change rule

Future Access UI changes are allowed when real M4+ integration proves a defect or missing state. Pure visual polish may evolve layout under normal review, but state semantics and backend-authoritative boundaries require full-stack review.

Production code never imports prototype implementation.

Current truth is:

```text
this document
+ current apps/web code/tests
+ current Access/Auth architecture/security/API/testing contracts
+ active workstream
```

The frozen prototype remains recoverable design evidence only.
