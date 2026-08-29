# DANTE — Access frontend contract

- **Status:** CURRENT / AUTHORITATIVE FOR MATERIALIZED WEB ACCESS THROUGH CLOSED M4
- **Scope:** accepted Web Access baseline, closed M3 signin/session/logout spine, closed M4 signup/verification/recovery/reset/reauth integration and carry-forward obligations for M5–M7
- **M4 final accepted implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **Frozen design source:** `prototype/access-system` at `469b68370e80185fa8a16d5335845e402ee1de3b`
- **Current workstream:** `../workstreams/access-auth.md`

## 1. Purpose

Access gets an unauthenticated person to a server-authoritative DANTE AuthSession and through the currently materialized first-party account lifecycle. This document owns the production Web Access contract. Current code/tests and accepted architecture/security decisions override historical prototype implementation details.

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

Google/Apple authentication remains an Auth mechanism only. Gmail, Calendar, iCloud and other provider-data access require separate explicit integration authorization.

---

## 3. Visual / UX baseline

The accepted Web Access design direction remains the production baseline. Backend phases do not justify gratuitous redesign.

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

Preserve `REQUEST_* = intent` and `SERVER_* = backend-authoritative result`.

---

## 5. Materialized Web baseline through M4

Production Web Access now includes:

```text
accepted SignIn shell + full Access visual/state system
IT/EN resources + persisted locale preference + html lang synchronization
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
real server failure/rate-limit mapping

M4:
real signup initiation
real six-digit email OTP verification
real OTP resend
real existing-account result after mailbox proof
real neutral recovery initiation
recovery-link capture + proof validation
immediate recovery URL fragment scrub
memory-only recovery bearer handling
real password reset
fresh-signin requirement after reset
real reauthentication
same-session bearer rotation
M4 generated/governed API-client integration
```

Setup persistence/HOME product behavior beyond the accepted Auth handoff remains owned by later product vertical work; M4 proves the correct authenticated transition into that flow.

---

## 6. Production integration path

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

Ownership:

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

Route code imports Access capabilities only through `features/access/index.ts`; route-level deep imports into Access internals are forbidden. Presentation/reducer code does not import raw Orval internals or call raw `fetch`.

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

Browser-owned `Origin` and `Sec-Fetch-Site` are not forged by application code.

Mutation retry is disabled. `retryable=true` is never blanket permission to replay a mutation. Auth state/query cache is not persisted to localStorage/sessionStorage.

M4 recovery-specific rule:

```text
raw recovery secret
→ received in URL fragment
→ captured exactly once into transient in-memory flow state
→ fragment scrubbed from browser URL immediately
→ never localStorage/sessionStorage
→ never ordinary query persistence
→ never logs/telemetry
```

---

## 8. Session bootstrap contract — permanent M3 regression rule

Rejected:

```text
Access reducer initially SIGN_IN
→ AccessPage paints login
→ GET /auth/session resolves authenticated
→ effect repairs state after paint
```

Accepted:

```text
hard document load
→ TanStack Router loader resolves/prefetches authoritative /auth/session
→ Query cache populated
→ AccessPage mounts
→ first business render is already SIGNED_IN or SIGNED_OUT
```

Permanent rule:

```text
UNKNOWN / LOADING
!= SIGNED_OUT
!= SIGNED_IN
!= ERROR
```

Do not reintroduce false Auth states to hide browser-owned document repaint.

---

## 9. Password UX / policy

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

Frontend validation is UX; backend policy remains authoritative.

---

## 10. M4 signup / verification UX contract

```text
SIGN_UP_EMAIL
→ SIGN_UP_PASSWORD
→ REQUEST_SIGN_UP
→ server creates pending challenge only
→ VERIFY_EMAIL
→ REQUEST_VERIFY_EMAIL
```

For a new canonical email, valid OTP establishes Account + verified EmailIdentity + PasswordCredential + AuthSession and transitions into authenticated setup/handoff.

For an existing canonical email:

```text
before mailbox proof
→ do not reveal account existence

valid OTP
→ explicit existing_account server result
→ show safe signin/recovery guidance
→ do not authenticate
→ do not replace existing password
```

Manual M4 UAT explicitly accepted this anti-enumeration behavior.

OTP resend operates on the current transient `signup_ref`; stale codes must not be treated as success.

---

## 11. M4 recovery / reset UX contract

Recovery initiation remains neutral where account existence would otherwise leak.

```text
FORGOT_PASSWORD
→ REQUEST_RECOVERY
→ neutral server acknowledgement
→ RECOVERY_SENT

recovery email link
→ capture/scrub secret
→ validate server proof
→ RESET_PASSWORD
→ REQUEST_RESET_PASSWORD
→ RESET_COMPLETE
→ fresh normal SIGN_IN
```

Reset never fabricates authenticated state and never auto-logs-in. Successful reset invalidates all historical AuthSessions server-side; the Web must converge on backend authority.

---

## 12. M4 reauthentication UX contract

Canonical API:

```text
POST /api/v1/auth/reauthenticate
```

```text
SERVER_REAUTH_REQUIRED
→ REAUTH
→ REQUEST_REAUTH with fresh password evidence
→ backend rotates exact presented bearer on same AuthSession
→ SERVER_REAUTH_SUCCEEDED
```

No client-only recent-auth Boolean is authoritative. Reauthentication is not initial signin and must not create a second AuthSession.

---

## 13. Session / multi-client contract

One Account supports `0..N` independent AuthSessions.

Consequences:

```text
current logout revokes only current AuthSession
another browser/context may remain authenticated
password reset intentionally revokes ALL AuthSessions
expiry/revocation converge from backend authority
IP/User-Agent/device metadata is signal, not identity proof
```

M4 preserves the M3 independent-session model rather than replacing it.

---

## 14. Provider and passkey boundary — M5 next

Provider authentication must use current official provider protocols/assets at M5 implementation time.

DANTE must not:

```text
fake provider chooser/consent UI
collect provider credentials
use provider email alone as existing-account identity proof
silently link Accounts from matching email
reuse provider Auth permission as Gmail/Calendar/iCloud data permission
```

M5 collision/linking remains:

```text
collision
→ prove existing DANTE Account control
→ explicit link decision
→ backend-authoritative link
```

The architecture is passkey-ready. Frontend code must not assume every Account always has a password.

---

## 15. Accessibility / responsive quality

Release target remains WCAG 2.2 AA-quality behavior.

Changed integrated surfaces must review:

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

## 16. Accepted Web proof through M4

M3 evidence remains accepted and is a regression baseline.

M4 integrated evidence:

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

Manual UAT accepted:

```text
login/session/logout
new signup → OTP → authenticated setup handoff
recovery → reset → fresh replacement-password signin
existing-account signup → OTP → safe existing_account message
```

---

## 17. Deferred obligations after M4

```text
M5
Google / Apple protocol validation
passkeys/WebAuthn
secure explicit account linking
provider collision UX

M6
Native Mobile Access

M7
whole-vertical session/account management as required
security hardening
production-credible observability
final Terms/Privacy destinations/content
final provider/legal/accessibility/dependency/release QA
real authenticated handoff into next DANTE vertical
whole-vertical user acceptance
```

Do not describe M3/M4 capabilities as incomplete merely because M5–M7 are open.

---

## 18. Quality / change rule

Future Access UI changes are allowed when real M5+ integration proves a defect or missing state. Pure visual polish may evolve layout under normal review, but state semantics and backend-authoritative boundaries require full-stack review.

Production code never imports prototype implementation.

Current truth is:

```text
this document
+ current apps/web code/tests
+ current Access/Auth architecture/security/API/testing contracts
+ active workstream
```

The frozen prototype remains recoverable design evidence only.
