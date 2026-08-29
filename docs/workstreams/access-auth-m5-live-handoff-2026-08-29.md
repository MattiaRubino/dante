# DANTE — Access/Auth M5 Live Handoff — 2026-08-29

- **Status:** CURRENT CONTINUATION SAVE-GAME / M5.1 COMPLETE / M5.2 NEXT
- **Vertical:** Access/Auth
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **PRE-SCOPE before this M5.1 documentation freeze:** `a95955da72cbb9119982aa1544c2aaa356fc5e6a`
- **M4 implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **M4 documentation-closure commit before M5.1:** `a95955da72cbb9119982aa1544c2aaa356fc5e6a`
- **M5 architecture authority:** `../architecture/access-auth-m5-contract.md`
- **M4 authority:** `../architecture/access-auth-m4-contract.md`
- **Forward plan:** `access-auth-m4-m7-execution-plan.md`

> This file exists so a new chat/agent can resume M5 without depending on conversation memory. Repository truth wins if branch state has moved after this handoff.

---

# 1. Read this first in a new chat

Mandatory continuation:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do **not** create a new Access branch/worktree merely because the chat changed.

Do not touch:

```text
main
feature/home-react
feature/access-frontend
/home/mattia/projects/dante-frontend
```

unless the user explicitly changes scope/topology.

Before any write, obey `docs/development/agent-operating-manual.md`:

```text
1. fetch current branch HEAD
2. establish exact PRE-SCOPE
3. exact CREATE/UPDATE/DELETE paths
4. exact purpose/out-of-scope
5. obtain explicit user approval
6. re-fetch HEAD before first write
7. post-write verify actual paths against gate
```

No merge/rebase/force-push/protected-main write without explicit gate.

Recommended bootstrap read order:

1. `docs/PROJECT-STATUS.md`
2. `docs/ROADMAP.md`
3. `docs/workstreams/access-auth.md`
4. **this file**
5. `docs/architecture/access-auth-m5-contract.md`
6. `docs/workstreams/access-auth-m4-m7-execution-plan.md`
7. `docs/architecture/access-auth-architecture.md`
8. `docs/architecture/access-auth-security-contract.md`
9. `docs/architecture/access-auth-api-contract.md`
10. `docs/architecture/access-auth-testing-contract.md`
11. `docs/decisions/ADR-011-access-auth-architecture.md`
12. `docs/database/README.md`
13. `docs/database/access-auth.md`
14. current Access/Auth Dictionary entries
15. `docs/development/backend-cp6-02-postgresql-persistence-constitution.md`
16. `docs/frontend/access.md`
17. current backend/Web implementation and tests

Do not restart M1–M4 from scratch.

---

# 2. User quality bar / working style

The user explicitly requires DANTE to be built at the level expected from large mature applications such as Google, Notion, Linear, Facebook and comparable serious products.

Interpretation:

```text
production-quality architecture
security-first but consumer-usable UX
high performance
strong DB integrity
clean maintainable code
no hidden technical debt left behind for convenience
configurable/tokenized UI rather than hardcoded one-offs
strong accessibility/responsive behavior
real boundary proof rather than mock-only confidence
no gratuitous enterprise theatre / overengineering without need
```

The user does **not** want a yes-man. If a design is weaker than mature-product practice, say so and correct it.

Testing preference learned during M4:

```text
prove each invariant at the truthful layer
avoid rerunning the entire expensive browser/PostgreSQL matrix after every tiny edit
use one heavy closeout QA when the candidate is actually ready
never mask flaky Auth with automatic retries
```

For manual UAT, advance **one action at a time**.

Avoid shell snippets with top-level `exit`.

---

# 3. Closed foundation — do not reopen casually

```text
M1 — Access Visual/UX Freeze
CLOSED / ACCEPTED

M2 — Auth Architecture Freeze
CLOSED / M2.1–M2.11 ACCEPTED / QA PASS

M3 — Email/Password Signin + AuthSession Spine
CLOSED / ENGINEERING PASS / USER ACCEPTED

M4 — Signup + Verification + Recovery + Reset + Reauth
CLOSED / ENGINEERING PASS / USER ACCEPTED
```

Whole Access/Auth vertical is still:

```text
ACTIVE / NOT CLOSED
```

M5, M6 and M7 remain.

Permanent identity/security constitution:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived
multiple independent AuthSessions normal
same-origin browser Auth
Secure HttpOnly host-only __Host-dante-session
session-bound CSRF + Origin + Fetch Metadata + X-Dante-Client
provider identity != provider email
provider authentication != provider-data integration authorization
method != factor != assurance
frontend request/success != backend-authoritative success
unknown/loading != signed-out/signed-in/error
```

Do not reintroduce:

```text
JWT/localStorage browser Auth
Redis/JWT session authority
Principal table
silent provider-email merge
Account advisory-lock replacement
wide credentialed CORS
Axios just for Auth
raw fetch from Access UI
fake frontend Auth success
persisted browser Auth cache
login-first + useEffect session repair
```

---

# 4. M4 closure evidence — accepted historical baseline

Final M4 implementation checkpoint:

```text
c95e3b2ca664725bcacc374cb5ba6ed49409fe2b
fix(auth): reconcile M4 PostgreSQL acceptance
```

M4 documentation closure before this M5 handoff:

```text
a95955da72cbb9119982aa1544c2aaa356fc5e6a
docs(auth): close M4 lifecycle
```

Accepted M4 DB state:

```text
PostgreSQL          18.6
Alembic             20260829_11
74 tables
5 views
15 routines
75 triggers
113 physical indexes
72 foreign keys
149 CHECK constraints
94 standalone Dictionary entries
```

Accepted automated evidence:

```text
backend static / typing / lint / build        PASS
backend fast                                 87 / 87 PASS
real PostgreSQL marked suite                 87 / 87 PASS
Web Access UI                                22 / 22 PASS
real Auth full-stack browser                 33 / 33 PASS
Chromium                                     11 / 11 PASS
Firefox                                      11 / 11 PASS
WebKit                                       11 / 11 PASS
```

Accepted manual M4 UAT:

```text
login/session/logout                         PASS
new signup → OTP → Account/AuthSession       PASS
setup/name authenticated handoff             PASS
recovery → reset → fresh replacement signin  PASS
existing Account signup → OTP → safe
existing_account outcome                     PASS
```

Do not rerun M4 QA absent direct regression evidence.

---

# 5. M5 current status

```text
M5 overall                                  ACTIVE
M5.1 external-authority readback            COMPLETE
M5.1 mature-product benchmark sweep         COMPLETE
M5.1 architecture/security semantic freeze  COMPLETE
M5.2 exact persistence + API design         NEXT
M5 production code                          NOT STARTED
M5 Dictionary delta                         NOT STARTED
M5 SQLAlchemy delta                         NOT STARTED
M5 Alembic migration                        NOT STARTED
M5 OpenAPI/client delta                     NOT STARTED
M5 Web runtime integration                  NOT STARTED
```

The new durable authority is:

```text
docs/architecture/access-auth-m5-contract.md
```

Do not perform another broad “what should Google/Apple/passkeys do?” discovery pass unless provider standards have materially changed. Start M5.2.

---

# 6. What M5 actually is

M5 is no longer described merely as three login buttons.

It is the **multi-authenticator Account layer**:

```text
Google authentication
+ Sign in with Apple
+ passkeys/WebAuthn
+ explicit Account linking
+ provider-enriched onboarding/bootstrap
+ passwordless Accounts
+ add-password capability
+ safe authenticator add/remove
+ anti-lockout
+ provider grant/revocation lifecycle
+ Apple relay/account-change lifecycle
+ Auth vs provider-data integration isolation
+ future Home/Security-settings readiness
```

All successful methods still create/use canonical DANTE `AuthSession`.

---

# 7. Provider-enriched onboarding — important user requirement

The user explicitly asked to take **all provider data genuinely useful to DANTE**, at the same quality level as large applications, and then make the resulting DANTE profile/settings editable later in authenticated Home/Settings.

Frozen rule:

```text
provider data
→ validate/classify provenance
→ use to remove redundant first-run questions
→ initialize or stage useful DANTE profile/setup values
→ user may later edit them in DANTE
→ provider does NOT overwrite later user-owned DANTE values
```

Useful Google bootstrap when actually returned:

```text
email
email_verified
name
given_name
family_name
picture
locale
hosted-domain metadata where present
security/authentication claims where actually available
```

Useful Apple bootstrap:

```text
email or Private Email Relay address
first name on initial authorization when supplied
last name on initial authorization when supplied
private-email/reachability semantics
security/authentication claims actually supplied by protocol
```

Do **not** invent a DANTE username from provider data. DANTE currently has no frozen canonical username concept.

Important provenance rule:

```text
provider bootstrap != permanent provider sync
```

Example:

```text
first Google login: name “Mattia Rubino”
→ DANTE may initialize name

user later changes DANTE display name to “Mattia”
→ future Google login MUST NOT restore “Mattia Rubino”
```

---

# 8. One-shot Apple profile data

Apple may provide name only on the first authorization. This became an explicit M5 requirement during the final sweep.

Therefore M5 must not rely on “we will save profile later” if that can lose the first payload.

Required semantic solution:

```text
use canonical downstream profile/settings owner if one exists and is ready
OR
use bounded durable onboarding/bootstrap staging
```

The staging must:

```text
preserve provider provenance
be consumable by the future profile/settings owner
not live as profile columns on Account
not turn ExternalIdentity into a Google/Apple profile dump
not overwrite user-owned state later
```

**M5.2 must inspect current Domain/Logical/Physical owners before choosing the table/object.**

This is a key M5.2 design question, not permission to invent `account_profile` blindly.

---

# 9. Google decisions frozen in M5.1

Use current Google Identity Services for Web.

Initial UX:

```text
official Continue with Google button
explicit user action
FedCM-compatible current GIS path where supported
auto-select off by default
One Tap not required for M5 closure
```

Identity:

```text
issuer + sub
```

Never email.

Server verifies current Google ID-token protocol evidence, including signature, issuer, audience, expiry, nonce and subject, plus other protocol-required claim checks.

JWK handling:

```text
bounded cache
bounded refresh on unknown kid
no refresh storm
unverifiable token fails closed
network outside DB transaction
```

Google email authority distinction:

```text
verified Gmail
→ Google can prove that Gmail mailbox

verified Workspace + hosted-domain context
→ Google can prove the hosted Google account mailbox

Google Account based on third-party email
→ do not assume Google remains current mailbox authority
→ require DANTE mailbox proof if current EmailIdentity/recovery proof is needed
```

If provider email is absent/insufficient, a pending provider enrollment can wait for DANTE email verification before canonical Account creation.

No Gmail/Calendar/Drive authorization scope belongs in M5 Auth.

---

# 10. Apple decisions frozen in M5.1

Web direction:

```text
server-created state + nonce
Apple authorization
provider-defined form_post callback
server-side authorization-code exchange
Apple ID-token verification
issuer + subject identity
DANTE Account/link/session decision
```

Normal DANTE CSRF/session cookie posture is not weakened globally for the external callback.

Apple verified email, including `@privaterelay.appleid.com`, can become the exact DANTE EmailIdentity supplied by Apple.

If user chooses Hide My Email:

```text
DANTE accepts relay address
DANTE does not force collection of hidden real email
```

Production relay delivery needs Apple sender configuration and authenticated mail sender posture including SPF/DKIM as required.

Apple name on first authorization is useful bootstrap but not a signed identity claim; validate/sanitize it and preserve it through the one-shot bootstrap mechanism.

Apple grant lifecycle is a real production obligation:

```text
server-side code validation
minimum required token/grant retention
protected encrypted provider secret material
revocation capability
server-to-server account-change notifications
JWK/key rotation
provider lifecycle reconciliation
```

Retained refresh/access-token material:

```text
never plaintext convenience data
never browser/localStorage
never logs
application-layer authenticated encryption
key id/version
key outside PostgreSQL/Git
rotation/revocation plan
```

Apple notification boundary must verify signatures and idempotently reconcile events such as email-forwarding changes, credential/consent revocation and Apple/app-account deletion notifications according to current Apple docs.

These events do not mean `Apple Account == DANTE Account`. They update/revoke the Apple binding/grant and provider-derived reachability; full DANTE deletion/retention policy remains separately governed.

---

# 11. ExternalIdentity decisions

Conceptual durable binding:

```text
ExternalIdentity
├── external_identity_ref
├── account_ref
├── provider/issuer
├── subject
└── lifecycle evidence
```

Hard DB invariant expected:

```text
UNIQUE(issuer, subject)
```

No provider identity may belong to two Accounts.

Do not automatically impose one Google/Apple identity per Account. Architecture can support multiple external identities from the same provider unless M5.2 finds a concrete reason to prohibit it.

Do not persist provider profile dump fields inside `ExternalIdentity` merely because they are available.

---

# 12. Explicit linking

No silent merge:

```text
matching provider email
!= DANTE Account ownership
```

Provider-first collision:

```text
provider proof
→ EmailIdentity collision
→ no duplicate Account
→ ACCOUNT_LINK state
→ prove existing DANTE Account with an allowed authenticator
→ appropriate recent auth
→ explicit user consent
→ Account security lock
→ final provider-identity uniqueness recheck
→ atomic ExternalIdentity link
```

User may prove existing Account with password, passkey or another accepted method. **Do not assume PasswordCredential exists.**

Linking is security-sensitive and should rotate the initiating AuthSession secret when retaining the same session/security context is appropriate.

Concurrent link attempts must be resolved by DB uniqueness + targeted serialization, not process memory.

---

# 13. Passkey/WebAuthn decisions

M5 implements real WebAuthn/passkeys.

Account supports:

```text
0..N PasskeyCredential
multiple passkeys
synced passkeys
device-bound passkeys
password-manager passkeys
hardware keys
passwordless Accounts
username-less/discoverable signin
cross-device/hybrid flows where supported
```

Baseline registration:

```text
current authenticated Account
recent authentication
>=32-byte CSPRNG challenge direction
short expiry
single use
residentKey required
userVerification required
privacy-minimizing attestation none
exact RP ID
exact origin
```

No biometric/face/fingerprint/PIN data is ever stored by DANTE.

### Opaque user handle

Do not expose `account_ref` directly as WebAuthn `user.id`.

Use a stable opaque random per-Account WebAuthn user handle, target 256 random bits, within WebAuthn limits.

Reason:

```text
AccountRef is DANTE identity, UUIDv7 and contains unnecessary timestamp metadata
WebAuthn user.id should be protocol-specific opaque identity
```

Exact owner/table shape is M5.2.

### Username-less login

```text
Use a passkey
→ issue challenge/options
→ discoverable credential selector
→ returned credential + userHandle
→ server verifies challenge/origin/RP/signature/UV/binding
→ resolve Account
→ fresh DANTE AuthSession
```

### Counter

`signCount` anomaly is a risk/security signal, not an automatic Account lock rule, especially with synced passkeys.

### L3 progressive features

Conditional mediation/autofill and WebAuthn L3 signal APIs may be used where supported, but explicit passkey login remains functional without them.

---

# 14. Add/remove authenticators and anti-lockout

M5 backend/application must be ready for authenticated Home → Security/Access settings even if the complete Settings UI is built in the next authenticated product phase.

Capabilities:

```text
link/unlink Google
link/unlink Apple
add/remove passkey
add password to passwordless/provider-created Account
safe password removal when another access path exists and policy allows
```

Every add/remove is backend-authoritative, recent-auth protected and security-event capable.

Hard invariant:

```text
normal authenticator removal
MUST NOT leave the Account with no viable authentication/recovery path
```

Backend transaction rechecks remaining authenticators and recovery reachability. UI-only prevention is insufficient.

---

# 15. Add-password capability

This was explicitly added after mature-product benchmark review (Notion/Todoist-class behavior).

Provider/passkey-created Account may have:

```text
PasswordCredential = NULL
```

Later authenticated user may add one:

```text
current AuthSession
+ recent valid authentication
+ password policy
+ HIBP fail-closed establishment screening
+ Argon2id + pepper
+ Account lock/recheck
+ insert PasswordCredential iff still absent
+ security event
+ session-secret rotation where appropriate
```

No alternate password stack.

---

# 16. Passwordless lost-device recovery

M5 cannot create unrecoverable passkey-only Accounts.

Minimum accepted fallback:

```text
strong existing email recovery proof
→ if PasswordCredential absent, establish first password
→ if present, replace it
→ same HIBP/Argon2 policy
→ revoke ALL existing AuthSessions
→ no auto-login
→ fresh signin
```

M5.2 must adapt the M4 recovery lifecycle to **create-or-replace** password while preserving:

```text
anti-enumeration
exact EmailIdentity + Account binding
single-use proof
supersession
conditional consume
no auto-login
all-session revocation
```

Do not invent a weaker temporary recovery session just to simplify passkey recovery.

---

# 17. Auth vs Google/Apple data integration

Permanent separation:

```text
Google Auth != Gmail/Calendar integration
Apple Auth  != iCloud/Calendar integration
```

Separate lifecycle may require separate:

```text
provider client/application configuration
consent
scopes
tokens
refresh/revocation
security events
user-facing connection management
```

The final provider setup must prove that Auth disconnect/revocation cannot accidentally revoke future unrelated DANTE Google/Apple data integration grants and vice versa.

Important correction from the benchmark discussion: do **not** freeze a guessed Google revocation side effect from memory. Verify the concrete GIS/OAuth configuration and current Google docs when the adapter/provider project configuration is materialized.

---

# 18. Provider challenge/transaction semantics

Purpose-specific bounded state, never a generic auth-token god table.

Required semantics:

```text
high entropy state/nonce where protocol uses them
provider binding
signin/create/link purpose binding
short TTL
single terminal consume
safe return target only; no open redirect
replay rejection
cleanup
secret redaction
```

Authenticated provider linking binds server-side to the initiating Account/AuthSession/recent-auth context.

Apple cross-site `form_post` is a narrowly reviewed provider-protocol endpoint exception. It does not weaken ordinary DANTE same-origin unsafe API CSRF rules.

---

# 19. Candidate persistence families — NOT YET APPROVED SQL

M5.2 must design the minimal exact physical model for:

```text
ExternalIdentity
provider signin/link transaction state
pending provider enrollment when email proof is still required
Apple grant/token secret lifecycle
Apple lifecycle notification idempotency state only if durable state is required
WebAuthn opaque Account user handle
PasskeyCredential
WebAuthn registration challenge
WebAuthn authentication challenge
provider profile-bootstrap staging if no canonical profile owner can consume one-shot data yet
```

Do not infer that each bullet means one table.

Do not merge unrelated semantics into one generic challenge/token table merely to reduce table count.

For every object M5.2 must freeze:

```text
purpose/canonicality
exact names
columns/types/nullability
PK/FK/UNIQUE/CHECK
indexes and actual queries
retention/cleanup
secret/verifier/encryption model
runtime ACL
Dictionary
SQLAlchemy
Alembic
real PostgreSQL proof
```

Current accepted DB head remains `20260829_11` until an authorized M5 migration is created and proved.

---

# 20. Candidate API intent families — exact paths NEXT

Do not start coding endpoint names before M5.2 freezes them.

Required intents include:

```text
Google begin/complete
Apple begin/callback/complete
provider account enrollment completion
provider link begin/confirm
provider unlink
passkey registration begin/complete
passkey authentication begin/complete
authentication-method listing/management as needed
passkey remove
add first password
passwordless recovery adaptation
Apple server notification ingress
provider grant revoke/reconcile
```

All normal DANTE operations still use:

```text
/api/v1
stable operationId
RFC 9457
request_id
Cache-Control: no-store where auth/security state is involved
OpenAPI/Pydantic authority
Orval Fetch + generated Zod
governed @dante/api-client
```

---

# 21. Web UX requirements

Keep accepted M1/M3/M4 Access quality and geometry.

Primary actions:

```text
Continue with Google
Continue with Apple
Use a passkey
email/password remains available
```

Use official provider branding. Do not fake Google/Apple credential/consent screens.

Required states:

```text
PROVIDER_PENDING
PROVIDER_ERROR
provider cancel
ACCOUNT_LINK
link confirmation
passkey pending/cancel/error
backend-authoritative Auth success
```

Smart first-account flow:

```text
provider gives useful validated data
→ skip/pre-fill redundant setup
→ ask only what is missing
→ hand off authenticated user toward Home
```

The user specifically wants later Home/Settings to allow internal editing of name/avatar/locale/security methods. M5 must prepare the backend/contracts now; do not build an incompatible temporary profile model.

Passkey needs a real enrollment entry point in M5 for production/UAT. Until Home Settings exists, a bounded post-auth/onboarding security prompt is acceptable. No public test-only production endpoint.

---

# 22. Browser/provider test constraints discovered

### WebAuthn RP test origin

M4 harness currently uses:

```text
https://127.0.0.1:4173
```

M5 WebAuthn must move the browser-facing test origin to a valid RP/domain posture, target:

```text
https://localhost:<ephemeral-port>
RP ID = localhost
```

or an equivalent explicitly configured test domain.

### Apple real Web UAT

Apple Web redirect configuration cannot be proven production-ready with localhost/IP only.

M5 closure requires:

```text
protocol-faithful local Apple substitute in deterministic CI
+
real Apple smoke/UAT on an Apple-registered HTTPS DANTE domain
```

Google receives equivalent real-provider smoke/UAT against final configuration.

### Browser matrix

Keep Chromium/Firefox/WebKit for product-critical browser semantics. Do not fake WebAuthn automation capabilities that a browser/test engine does not expose. Use the lowest truthful proof layer plus explicit bounded testing-contract exceptions where required.

---

# 23. Dependency direction

Current backend before M5 has no dedicated production WebAuthn/JOSE/AEAD stack admitted for this feature.

Candidates identified during M5.1 research included maintained WebAuthn, JOSE/JWK/JWT and `cryptography`-backed capabilities, but **no package/version is approved yet**.

M5.2/implementation qualification must check:

```text
Python 3.14 support
maintained/security status
algorithm allowlisting
no dangerous implicit defaults
transitive dependencies
uv lock
mypy/Ruff compatibility
protocol-vector behavior
```

Do not hand-roll JWT/JWS/JWK, COSE/CBOR/WebAuthn or authenticated encryption.

---

# 24. Testing obligations to carry forward

Mandatory CI does not depend on public Internet providers.

Use:

```text
real DANTE provider adapter/protocol implementation
→ protocol-faithful deterministic local Google/Apple substitute
```

Do not bypass internal validation/application/DB path.

Google test classes:

```text
known identity signin
new account
mailbox-authority distinction
email collision/no auto-link
explicit linking
invalid signature/issuer/audience/nonce/expiry
JWK rotation/unknown kid
replay
cancel/error/outage
profile change no identity change
profile no-overwrite
concurrent identity/link races
Account disabled race
```

Apple:

```text
state/nonce/code
code exchange
ID-token validation
one-shot name
subsequent login without name
Private Relay
relay/account-change notifications
consent/revocation
notification signature/replay/idempotency
JWK rotation
exchange failures/replay
protected grant secret
revoke behavior
real registered-domain UAT
```

Passkey:

```text
registration
discoverable/username-less auth
UV required
opaque userHandle
challenge expiry/replay
origin/RP mismatch
credential/userHandle mismatch
bad signature
duplicate credential
multiple passkeys
synced/device-bound metadata
counter anomaly policy
remove anti-lockout
passwordless login
lost-passkey recovery
hybrid/conditional behavior where supported
```

Real PostgreSQL is required for persistence/concurrency claims.

`unit != PostgreSQL != API != generated-contract != Web != browser != real-provider acceptance`.

---

# 25. Mature-product benchmark summary

Benchmark applications were used to find missing capability classes, not copied blindly.

Key findings carried into M5:

```text
Linear
→ provider/SSO first-account provisioning can bootstrap profile
→ later provider login does not own/overwrite profile
→ passkeys + Security & Access + sessions/authorized apps patterns

Notion
→ Google/Apple/password/passkeys coexist
→ social/provider-created Account can establish password
→ multiple passkeys / security management

Todoist
→ social-created Account can add password

GitHub
→ mature passkey/cross-device flows

Figma / Slack / comparable products
→ connected applications/data integrations are separate from sign-in/security
```

DANTE remains stricter on provider-email linking:

```text
matching email alone
NEVER silently links Accounts
```

---

# 26. M5 vs M7 boundary

M5 must materialize the **correct underlying capability/evidence**.

M7 still owns final whole-vertical hardening/management/observability such as:

```text
complete session/device management UI
remote revoke UX
new-login alerts
“this wasn’t me” response
final durable security-event retention where not needed earlier
full production observability
final privacy/legal/accessibility/dependency/release review
whole-vertical manual UAT
```

Do not defer an invariant needed for M5 correctness merely because M7 exists. Example: anti-lockout and Apple grant revocation are M5 correctness concerns.

---

# 27. Exact next action for a new chat — M5.2

Do **not** start by coding Google callback handlers.

Start here:

```text
M5.2 — exact persistence + API design
```

Sequence:

```text
1. fetch current feature/access-auth HEAD
2. read M5 contract + this handoff
3. inspect current Auth mappings/services/API/tests
4. inspect Dictionary objects for Account/EmailIdentity/PasswordCredential/AuthSession/M4 challenges
5. inspect CP6 naming/UUID/FK/ACL/migration rules
6. inspect current Domain/Logical owner for profile/name/locale/bootstrap before adding any profile persistence
7. design exact M5 state machines
8. design minimal physical delta
9. design exact public API/problem codes/operationIds
10. design provider callback topology and WebAuthn RP/origin topology
11. map every invariant to unit/PostgreSQL/API/browser/real-provider proof
12. present exact implementation write gate to user
```

M5.2 must answer explicitly:

```text
What exact persistent owner stores ExternalIdentity?
What exact server state carries provider nonce/state/link intent?
How is an unbound provider identity staged while DANTE mailbox proof is pending?
How is Apple retained grant material encrypted/rotated/revoked?
How are Apple notifications made idempotent?
Where does opaque WebAuthn userHandle live?
What exact PasskeyCredential columns are actually required?
One vs separate WebAuthn challenge tables — which semantics justify it?
How is one-shot provider profile bootstrap preserved without polluting Auth?
How does M4 recovery become create-or-replace PasswordCredential safely?
What exact API operations and machine problems expose these intents?
What exact browser callback/redirect state machine prevents CSRF/open redirect/replay?
```

No code should be committed before those answers are coherent enough to define a bounded write scope.

---

# 28. Official source reminders

Current M5.1 external-authority review included at minimum:

```text
Google Identity Services / ID-token verification / OIDC
https://developers.google.com/identity/gsi/web/guides/verify-google-id-token
https://developers.google.com/identity/gsi/web/reference/js-reference
https://developers.google.com/identity/openid-connect/openid-connect

Sign in with Apple Web / REST / revocation / account changes / relay
https://developer.apple.com/documentation/signinwithapple/configuring-your-webpage-for-sign-in-with-apple
https://developer.apple.com/documentation/signinwithapplerestapi/revoke-tokens
https://developer.apple.com/documentation/signinwithapple/processing-changes-for-sign-in-with-apple-accounts
https://developer.apple.com/help/account/capabilities/configure-private-email-relay-service

WebAuthn / FIDO
https://www.w3.org/TR/webauthn-3/
https://fidoalliance.org/passkeys/
```

Current standards/provider guidance must be rechecked only where adapter/config implementation depends on changeable details.

---

# 29. Final continuation verdict

```text
M1–M4        CLOSED / DO NOT REOPEN WITHOUT EVIDENCE
M5.1         COMPLETE / FROZEN
M5.2         NEXT
M6           PLANNED
M7           PLANNED / FINAL WHOLE-VERTICAL GATE

Whole Access/Auth
ACTIVE / NOT CLOSED
```

The continuation agent should now be able to proceed from repository truth without access to the saturated conversation that produced this handoff.