# DANTE — Access/Auth M4 Lifecycle Architecture Contract

- **Status:** CURRENT M4 ARCHITECTURE CANDIDATE / CONTRACT FREEZE ACTIVE
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **Prerequisite:** M1–M3 CLOSED / M3 ENGINEERING PASS / USER ACCEPTED
- **M4 scope:** Signup + Email Verification + Recovery + Password Reset + Reauthentication
- **Observability:** full Grafana/OpenTelemetry stack DEFERRED TO M7 after PRE-M4 feasibility readback; M4 must still preserve privacy-safe logging
- **Implementation strategy:** one coherent M4 macro-batch with one final heavy PostgreSQL/browser/UAT gate; internal sub-slices are development structure, not six independent release gates

> M4 builds on the accepted M3 Account/AuthSession spine. It does not reopen M1–M3, create another branch/worktree, replace the generated-client path, or introduce a second Auth/session architecture.

---

## 1. Why M4 is designed as one lifecycle

Signup, verification, recovery, reset and reauthentication are security-coupled. Designing them separately creates contradictory proof semantics, duplicated token tables, inconsistent rate limits and avoidable session bugs.

M4 therefore freezes the **whole first-party lifecycle contract first**, then materializes it as one vertical implementation:

```text
lifecycle contract
→ exact persistence
→ backend application/security runtime
→ email boundary
→ FastAPI/Pydantic
→ deterministic OpenAPI
→ Orval Fetch + governed @dante/api-client
→ Web integration
→ focused unit/static proof during development
→ one comprehensive real PostgreSQL/API/browser closure gate
→ manual UAT
→ docs reconciliation
```

Do not run a full cross-browser acceptance matrix after every internal helper/table/screen. Critical concurrency/replay invariants are tested at the lowest truthful layer as soon as they are built; the expensive whole-stack matrix runs once against the integrated M4 candidate.

---

## 2. External benchmark readback — adopt principles, not product cosplay

M4 was checked against current public guidance/behavior from mature systems and standards.

### OWASP

Adopt:

```text
generic registration/recovery responses where account existence would otherwise leak
consistent-enough timing posture
cryptographically generated proof secrets
single-use + expiry
rate/resource controls
no account mutation before valid recovery proof
normal signin after password recovery rather than automatic login
session invalidation after reset
verified email before treating email as trusted identity/recovery channel
```

### NIST SP 800-63B Rev. 4

Use as an engineering benchmark, not a compliance claim:

```text
reauthentication is a first-class security event
session/recent-auth freshness is server-authoritative
phishing-resistant methods should remain possible in M5
method != factor != assurance
```

### GitHub

Relevant observed product posture:

```text
email verification gates meaningful capabilities
email uniqueness is strict
password reset uses verified email channels
password reset links are time-limited
HIBP-style compromised-password screening is used
```

DANTE does **not** copy GitHub's choice to maintain normal unverified Accounts because DANTE can satisfy the already-frozen signup UX without doing so.

### Auth0

Relevant architecture/product posture:

```text
supports email verification after account creation
also supports OTP verification before account creation
email OTP avoids accidental verification from automated link scanners
one-time reset links
newer reset issuance supersedes older reset links
neutral password-recovery response is recommended
```

The pre-account OTP model fits DANTE best because Access already uses a six-digit verification-code screen and the canonical consumer invariant expects a verified recovery/contact EmailIdentity.

### Google

Relevant posture:

```text
sensitive actions may require fresh identity verification even inside an authenticated session
recent/trusted authentication is distinct from ordinary logged-in state
```

DANTE adopts the principle through server-side `recent_auth_at` + explicit reauthentication, without copying Google's device/risk system.

### Apple / Microsoft

Relevant recovery posture:

```text
recovery becomes deliberately conservative when strong existing proof is unavailable
support operators do not simply bypass the security model
recovery is not equivalent to ordinary signin
```

DANTE M4 keeps recovery narrow: verified email proof + password reset + revoke all sessions + fresh normal signin.

---

## 3. Frozen M3 foundations M4 must reuse

```text
Account = durable access/security root
EmailIdentity separate from Account
PasswordCredential optional
Principal runtime-derived
opaque PostgreSQL-backed AuthSession
multiple independent AuthSessions normal
same-origin Web topology
Secure HttpOnly host-only __Host-dante-session
session-bound CSRF
Origin + Fetch Metadata + X-Dante-Client browser protection
RFC9457 machine errors
READ COMMITTED + targeted locking
Account security serialization point
no blind mutation retry
FastAPI/Pydantic → deterministic OpenAPI → Orval Fetch → @dante/api-client
TanStack Query remote lifecycle
TanStack Router critical-session bootstrap
real PostgreSQL proof
real HTTPS Chromium/Firefox/WebKit proof
```

Permanent M3 regression guards remain binding:

```text
unknown/loading != signed-out
no login-first/useEffect repair
no hidden sign-in geometry placeholder
no persisted browser Auth cache
no route deep-import into Access internals
no frontend-auth success without backend authority
```

---

# 4. M4 signup model — verify before Account creation

## 4.1 Canonical user flow

The frozen Access UX already uses:

```text
SIGN_UP_EMAIL
→ SIGN_UP_PASSWORD
→ VERIFY_EMAIL (6-digit OTP)
```

M4 preserves that exact product shape.

Backend semantics:

```text
email + password submitted
→ validate / normalize / rate-limit
→ HIBP + Argon2id outside DB transaction
→ create/replace one pending password-signup challenge
→ enqueue six-digit email OTP
→ public response remains non-enumerating

valid OTP
→ one short authoritative transaction
→ re-check current email collision
→ create Account
→ create verified EmailIdentity
→ create PasswordCredential
→ create AuthSession
→ remove pending signup challenge
→ COMMIT
→ issue session cookie only after durable success/reconciliation
```

A standard password signup therefore does **not** create an unverified durable Account.

Benefits:

```text
no junk canonical Accounts from abandoned/bot signup
no email-squatting lockout by an unverified Account
no need for Account pending status
no unverified AuthSession
no cleanup job required for canonical Account state
verified recovery identity exists at Account birth
```

`Person` is still not created implicitly. `Person != Account` remains binding.

## 4.2 Existing-email anti-enumeration

Initial signup must not reveal whether an Account already exists.

The same syntactically valid request path creates/replaces a pending signup challenge and queues an OTP email regardless of current Account existence. Canonical Account state is not changed.

Only **after the user proves control of that mailbox with the OTP** may verification return a safe business outcome such as:

```text
new_account_authenticated
existing_account
```

For `existing_account`:

```text
submitted signup password is discarded
existing PasswordCredential is never changed
no AuthSession is issued
UI routes to normal signin/recovery
```

This prevents registration enumeration without turning signup into email-OTP login or password reset.

## 4.3 Pending signup lifetime

Use one purpose-specific ephemeral persistence object, not a generic token table.

Proposed semantic object:

```text
PasswordSignupChallenge
```

It owns only pending first-party password signup:

```text
password_signup_ref
normalized email address
email comparison key (unique active row)
Argon2id password verifier
password pepper key id
HMAC verifier for current email OTP
verification key id
created_at
updated_at
signup_expires_at
verification_issued_at
verification_expires_at
failed_verification_attempts
```

Baseline lifetimes:

```text
pending signup lifetime        24 h
individual email OTP lifetime  15 min
failed OTP attempts            max 5 per issued OTP
resend                         rotates OTP and resets attempt counter
old OTP after resend           invalid immediately
```

Exact rate capacities remain validated settings so deployment pressure can be tuned without changing semantics.

On successful account establishment, delete the pending challenge in the same transaction. Expired pending rows may be replaced lazily by a new signup; they are not canonical history.

## 4.4 Six-digit OTP security

The existing Web UI deliberately expects six numeric digits. Six digits are acceptable only as an online-limited proof.

Requirements:

```text
CSPRNG uniform code generation
exactly 000000..999999
never store raw OTP
store HMAC-SHA256 verifier under a dedicated purpose key
constant-time verifier comparison
short TTL
max failed attempts
resend cooldown / issuance rate limit
no OTP in logs/telemetry
```

A plain SHA-256 of a six-digit code is forbidden because the code space is trivially enumerable after DB compromise.

Use a dedicated signup-OTP HMAC key distinct from password pepper(s), CSRF key and future provider secrets.

---

# 5. Email delivery boundary

## 5.1 Architecture

Email is an external side effect, never part of a PostgreSQL transaction.

```text
Auth application
→ EmailDeliveryPort
→ bounded process-owned dispatch queue
→ SMTP adapter
→ transactional email provider / local protocol-faithful sink
```

Business/domain code must not know SMTP/Grafana/provider payloads.

M4 selects SMTP as the first transport adapter because it is vendor-neutral and supported by production transactional providers. A later HTTP provider adapter may replace it without changing application semantics.

## 5.2 Performance / anti-enumeration

Do not hold Auth DB transactions open while waiting for email network I/O.

Do not make recovery response latency directly depend on whether a real recipient exists.

Use a bounded asynchronous dispatcher:

```text
request commits proof state
→ enqueue delivery command quickly
→ HTTP response completes
→ worker performs SMTP outside request/DB transaction
```

For neutral recovery paths, enqueue an equivalent bounded no-op command when no eligible Account exists so public request behavior does not branch on an external send.

Dispatcher rules:

```text
bounded queue
bounded worker count
bounded SMTP timeout
no unbounded create_task fan-out
clean lifespan startup/shutdown
telemetry/logging never contains proof secret
no blind resend after ambiguous SMTP acceptance
user-driven resend is the recovery mechanism
```

A process crash can lose an unpersisted queued email. This is accepted in M4 because verification/recovery issuance is safely repeatable and resendable. If real deployment evidence requires guaranteed asynchronous delivery, activate the already-planned PostgreSQL transactional outbox under its own trigger rather than inventing it pre-emptively.

## 5.3 Local/full-stack proof

Use a protocol-faithful local SMTP capture service in the real full-stack harness. Browser E2E must read the actual captured email/code/link through test control outside production FastAPI APIs.

No public `/test/*` endpoint is added to DANTE.

---

# 6. Verification transaction and race behavior

Verification consumes the pending signup challenge under row-level serialization.

Expected transaction:

```text
BEGIN
→ lock current PasswordSignupChallenge
→ reject expired/exhausted/incorrect code
→ re-check EmailIdentity uniqueness/current collision
→ if collision exists:
     remove pending challenge
     COMMIT
     return existing_account
→ else:
     insert Account(active)
     insert EmailIdentity(verified_at=now)
     insert PasswordCredential(pending verifier)
     insert AuthSession
     remove pending challenge
→ COMMIT
→ reconcile ambiguous outcome by exact generated refs/verifiers if needed
→ only then emit raw AuthSession secret
```

PostgreSQL unique `EmailIdentity.comparison_key` remains the final concurrency arbiter. Two concurrent verification attempts cannot create two Accounts for one canonical email.

Do not use global SERIALIZABLE or advisory locks for this flow.

---

# 7. Recovery initiation

## 7.1 Public contract

Recovery request accepts an email and always responds neutrally for syntactically valid requests:

```text
If an eligible account exists, recovery instructions will be sent.
```

Do not disclose:

```text
Account exists / does not exist
Account disabled
email unverified
Account has no PasswordCredential
provider-only Account
```

Public HTTP status/body must not encode those distinctions.

Use the same canonical email normalization/comparison as signin/signup.

## 7.2 Eligible Account

M4 password recovery email is issued only when current state proves:

```text
EmailIdentity exists
EmailIdentity is verified
Account is active
current PasswordCredential exists
```

Provider-only/passwordless recovery is handled by M5 authentication methods, not by manufacturing a password silently.

## 7.3 Recovery proof persistence

Use a separate purpose-specific object:

```text
PasswordRecoveryChallenge
```

Proposed fields:

```text
password_recovery_ref   UUIDv7 public non-secret challenge reference
account_ref             FK / one current challenge per Account
secret_verifier         SHA-256 of 32 random bytes (or stronger domain-separated verifier)
issued_at
expires_at
```

Raw recovery secret:

```text
32 CSPRNG bytes
Base64URL canonical encoding
never persisted
never logged
single use
30-minute baseline lifetime
new issuance supersedes/replaces prior challenge
```

Because the raw secret has 256 bits of entropy, a cryptographic digest is already resistant to offline brute force. Do not reduce recovery to a short numeric code.

---

# 8. Recovery link handling

Do not put the raw recovery bearer secret in a normal query string where it can reach server/access logs, browser history synchronization or referrers.

Preferred Web link shape:

```text
https://<canonical-origin>/?recovery=<non-secret password_recovery_ref>#<raw-secret>
```

Client entry behavior:

```text
capture fragment once
→ validate canonical encoding/length
→ immediately remove secret fragment from visible URL/history
→ keep secret only in component/application memory
→ optionally validate proof server-side without consuming it
→ show RESET_PASSWORD only for a structurally/authoritatively valid recovery flow
```

No localStorage/sessionStorage persistence of the recovery secret.

The reset page must not load third-party analytics/resources that could observe sensitive navigation context.

---

# 9. Password reset

Password reset request contains:

```text
password_recovery_ref
raw recovery secret
new password
```

Client-side confirmation field remains UX-only; backend receives one new password value.

Expensive work occurs before the authoritative transaction:

```text
validate token shape
normalize password
HIBP breach check
Argon2id hash under existing bounded KDF admission
```

Authoritative mutation:

```text
BEGIN
→ resolve + validate recovery challenge
→ acquire Account security lock
→ re-read current Account/PasswordCredential/challenge
→ require active Account + still-current recovery proof
→ replace PasswordCredential verifier
→ remove/consume recovery challenge
→ revoke ALL AuthSessions with reason password_reset
→ COMMIT
→ reconcile ambiguous outcome if necessary
```

After recovery reset:

```text
NO automatic login
NO surviving browser session
fresh normal signin required
security notification email queued after durable success
```

This preserves the already-accepted M2 lifecycle and OWASP guidance.

---

# 10. Reauthentication / recent-auth

## 10.1 Principle

Being signed in is not sufficient proof for every future sensitive operation.

M4 materializes password reauthentication as the first method while keeping the architecture compatible with M5 passkeys/providers.

```text
valid AuthSession
+ fresh password evidence
→ refresh recent-auth security context on SAME AuthSession
→ rotate session bearer secret
```

Do not create a second AuthSession for reauth.

## 10.2 Baseline freshness

Use a configurable server-side recent-auth window with a conservative default:

```text
10 minutes
```

Endpoints that require recent auth enforce it on the backend and return a stable problem such as:

```text
auth.reauthentication_required
```

The frontend may react by showing `REAUTH`, but it never decides that the security requirement is satisfied.

## 10.3 Password reauth transaction

```text
read current credential snapshot
→ Argon2 verification outside DB transaction
→ optional HIBP policy outside transaction
→ BEGIN
→ acquire Account security lock
→ re-read current credential/session
→ prove credential evidence still current
→ update AuthSession.recent_auth_at
→ rotate AuthSession.secret_verifier
→ COMMIT
→ reconcile ambiguity if needed
→ issue replacement __Host-dante-session cookie + derived CSRF
```

`authenticated_at` remains the original session authentication time; `recent_auth_at` tracks fresh assurance.

No reauth mutation retry.

---

# 11. Proposed M4 database delta

M4 should require only two new ephemeral security tables plus ACL evolution for already-existing Auth tables:

```text
password_signup_challenge
password_recovery_challenge
```

No generic `auth_token`, `proof`, `challenge(type,payload)` or JSONB token god-table.

Expected existing-table permission/evolution needs:

```text
Account              narrow INSERT capability for verified account establishment
EmailIdentity        narrow INSERT capability
PasswordCredential   narrow INSERT capability + existing verifier UPDATE
AuthSession          existing INSERT/revoke + narrow recent_auth_at/secret_verifier UPDATE for reauth
```

Exact grants must remain column-bounded where possible and be proven against `dante_runtime` in real PostgreSQL.

Every structural change updates atomically as one change-set:

```text
Alembic
SQLAlchemy
Database Dictionary
current whole-DB reference
Access/Auth DB reference
real PostgreSQL catalog tests
```

Likely next migration starts from `20260827_10`; never edit applied revisions.

---

# 12. Proposed M4 HTTP surface

Exact names remain subject to OpenAPI readback, but the target semantic surface is:

```text
POST /api/v1/auth/signup
POST /api/v1/auth/signup/verify
POST /api/v1/auth/signup/resend

POST /api/v1/auth/recovery
POST /api/v1/auth/recovery/validate
POST /api/v1/auth/reset-password

POST /api/v1/auth/reauth/password
```

All browser unsafe operations preserve M3 browser ingress protections.

### Signup

`POST /auth/signup`

```text
request: email + password (+ locale if selected for email copy)
response: neutral verification-required result
no cookie
```

`POST /auth/signup/verify`

```text
request: email + 6-digit code
response discriminator:
  authenticated
  existing_account

Set-Cookie only for authenticated outcome after durable commit/reconciliation.
```

`POST /auth/signup/resend`

```text
request: email
response: neutral accepted/resend result
rotates current OTP
```

### Recovery

`POST /auth/recovery`

```text
request: email
response: neutral accepted result
```

`POST /auth/recovery/validate`

```text
request: non-secret recovery ref + raw bearer secret
response: valid / invalid-or-expired
never consumes proof
```

`POST /auth/reset-password`

```text
request: recovery ref + secret + new password
response: reset complete
no session issuance
clears any current browser Auth cookie defensively
```

### Reauth

`POST /auth/reauth/password`

```text
requires current AuthSession + CSRF
request: current password
response: refreshed session metadata
rotates cookie/session secret
```

No endpoint returns raw proof secrets except the out-of-band email channel.

---

# 13. Error/outcome policy

Stable machine semantics should distinguish public-safe business outcomes without leaking Account existence prematurely.

Candidate codes/categories:

```text
auth.signup_rate_limited
auth.verification_invalid_or_expired
auth.verification_attempts_exhausted
auth.recovery_invalid_or_expired
auth.reauthentication_required
auth.email_delivery_unavailable
auth.invalid_credentials
auth.password_compromised
auth.account_unavailable
```

`existing_account` after successful mailbox verification is an expected business outcome, not an anonymous-enumeration error.

Recovery initiation does not return different statuses for known vs unknown email.

All sensitive Auth responses remain `Cache-Control: no-store` and carry the server-authoritative request ID.

---

# 14. Performance / resource-control contract

M4 must remain fast under legitimate load and bounded under abuse.

```text
Argon2/HIBP/network work outside DB transactions
reuse existing bounded KDF admission
bounded per-process ingress token buckets
bounded email dispatch queue/workers
short READ COMMITTED transactions
indexed equality lookups only on hot Auth paths
PostgreSQL uniqueness as final email race arbiter
Account lock only for Account-wide security mutations
no SERIALIZABLE blanket mode
no network/email wait under row lock
no unbounded background task creation
no raw request bodies in logs
```

Expected hot-path lookup indexes:

```text
password_signup_challenge.email_comparison_key UNIQUE
password_recovery_challenge.password_recovery_ref UNIQUE/PK
password_recovery_challenge.account_ref UNIQUE
password_recovery_challenge.secret_verifier UNIQUE or bounded lookup companion
existing email_identity.comparison_key UNIQUE
existing auth_session.secret_verifier UNIQUE
```

Do not introduce Redis merely to claim scale. A later measured multi-instance/edge requirement may move rate limiting behind an explicit operational gate.

---

# 15. M4 frontend integration

Preserve frozen Access state graph; materialize existing backend-required events rather than redesigning the surface.

Required real wiring:

```text
REQUEST_SIGN_UP
→ POST signup
→ SERVER_SIGN_UP_CREATED
→ VERIFY_EMAIL

REQUEST_VERIFY_EMAIL
→ POST signup/verify
→ authenticated new Account: SERVER_EMAIL_VERIFIED + real AuthSession
→ existing Account after mailbox proof: explicit existing-account server outcome

REQUEST_RESEND_VERIFICATION
→ real resend

REQUEST_RECOVERY
→ neutral POST recovery
→ RECOVERY_SENT

recovery email entry
→ capture/sanitize recovery secret
→ server proof validation
→ SERVER_RECOVERY_PROOF_VALID
→ RESET_PASSWORD

REQUEST_RESET_PASSWORD
→ real reset
→ RESET_COMPLETE

SERVER_REAUTH_REQUIRED
→ REAUTH
REQUEST_REAUTH
→ password reauth
→ SERVER_REAUTH_SUCCEEDED
```

`SERVER_EMAIL_VERIFIED` may continue into existing setup UI after a real AuthSession is established. Setup persistence/handoff remains outside M4 unless separately promoted.

Fix existing M4 password-UX drift: `isValidNewPassword` must match the authoritative M3 policy minimum of **15 Unicode code points**, not the current pre-backend 12-character placeholder.

---

# 16. Testing strategy — maximum coverage without six redundant release cycles

M4 does **not** close M4.1, M4.2, M4.3, etc. as six independent releases.

Use a pyramid:

### Development-time focused proof

Run while implementing changed pieces:

```text
unit tests for normalization/proof codecs/state mapping
fast service tests
migration/Dictionary/schema checks
purpose-specific concurrency tests
formatter/type/lint/generated drift
```

### One real PostgreSQL M4 acceptance suite

Prove all security invariants once on the integrated M4 candidate:

```text
new signup → OTP → atomic Account/verified Email/Password/AuthSession
existing verified email signup remains non-destructive
concurrent signup same email
OTP expiry
OTP replay
OTP resend invalidates old code
OTP max attempts
verification concurrent double-consume
Account/email uniqueness race
recovery known vs unknown public equivalence
recovery expiry
recovery replay
new recovery invalidates old proof
reset concurrent double-consume
password/HIBP failure leaves credential/proof/session state correct
reset revokes every AuthSession
ambiguous commit reconciliation
reauth invalid password
reauth credential changed during KDF
reauth updates recent_auth_at and rotates session secret
runtime ACL exactness
email dispatcher outage does not corrupt DB state
```

### One real browser closure matrix

Do not multiply every DB race by three browsers. Cross-browser tests prove user/browser semantics; DB/service tests prove transaction races.

Run the critical user flows on Chromium + Firefox + WebKit:

```text
signup → captured real email OTP → verify → authenticated/setup transition
existing-account signup after verified OTP → safe signin/recovery guidance
resend → old code fails/new code succeeds
recovery → captured link → reset → fresh signin required
post-reset old sessions rejected
reauth → cookie rotates / session identity preserved
server/DB/email degraded states never fake success
refresh/bootstrap remains regression-free after M4
```

This gives high assurance without wasting time by repeating low-level concurrency tests in every browser engine.

### Manual UAT

One integrated M4 UAT after automation is green.

---

# 17. M4 closure gate

M4 closes only when all are true:

```text
whole lifecycle contract accepted
exact M4 persistence materialized
DB Dictionary/SQLAlchemy/Alembic/current docs aligned
backend runtime complete
email delivery boundary operational in real local harness
OpenAPI snapshot deterministic
generated client governed and drift-clean
Web Access real wiring complete
static/type/lint/architecture/build PASS
real PostgreSQL full M4 matrix PASS
critical Chromium/Firefox/WebKit M4 matrix PASS
M3 21/21 regression semantics preserved
manual M4 UAT PASS
user explicit acceptance
```

Heavy full-stack acceptance is performed once against the integrated M4 candidate, not after each internal sub-slice.

---

# 18. Explicit non-goals / deferments

Not M4:

```text
Google/Apple authentication
ExternalIdentity persistence
passkeys/WebAuthn
MFA/TOTP/recovery codes
Native credential transport
full session/device management UI
email-address change flow
Person/profile creation by implication
Grafana/Alloy/Loki/Tempo/Prometheus/Mimir stack
production on-call/alerting
Home integration
```

Full observability is now an explicit mandatory M7 release gate unless independently promoted later.

---

# 19. Forbidden M4 shortcuts

```text
generic auth_token/proof table with type + JSON payload
creating canonical Account on initial anonymous signup before mailbox proof
letting unverified standard signup issue AuthSession
using plain SHA-256 for six-digit OTP
storing raw OTP/reset token/password
reset auto-login
reset that leaves historical sessions alive
email send/network call inside DB transaction
recovery response that reveals Account existence
frontend fake verification/reset success
client-only recent-auth boolean
reauth creating a second AuthSession
persisting recovery bearer secret in local/session storage
raw recovery secret in normal query string
blind mutation retry
broad Account UPDATE grant just for convenience
copying provider-specific/email-mailbox tricks into canonical email comparison
```

---

# 20. Immediate implementation sequence

M4 should now proceed as one coordinated batch:

```text
1. readback this contract against M2 security/API/testing authorities
2. materialize exact two-table M4 DB delta + ACL changes
3. implement proof codecs + signup/recovery/reauth application operations
4. implement bounded email dispatcher + SMTP adapter + local capture boundary
5. expose FastAPI M4 endpoints/RFC9457 outcomes
6. regenerate governed OpenAPI/Orval client
7. wire existing Access signup/verify/recovery/reset/reauth surfaces
8. add focused tests while coding
9. run one integrated static + real PostgreSQL acceptance gate
10. run one integrated cross-browser M4 gate
11. manual UAT
12. reconcile docs and close M4
```

Do not split this into new branches or six macro-phase closure cycles.
