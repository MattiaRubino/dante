# DANTE — Access/Auth M5 Contract

- **Status:** CURRENT / BRANCH-LOCAL AUTHORITATIVE FOR M5 / M5.1 + M5.2 DESIGN FREEZE COMPLETE / M5-A–D ACCEPTED / GROUP 1 ACTIVE
- **Vertical:** Access/Auth
- **Branch:** `feature/access-auth`
- **Prerequisite:** M1–M4 CLOSED; M4 ENGINEERING PASS; M4 MANUAL UAT PASS; USER ACCEPTED
- **M5.1:** architecture + external-authority freeze COMPLETE
- **M5.2:** exact persistence + API design COMPLETE
- **M5-A:** persistence foundations COMPLETE / REAL POSTGRESQL ACCEPTED
- **M5-B:** provider/JWK/JOSE/AEAD/WebAuthn policy infrastructure COMPLETE / ENGINEERING PASS
- **M5-C:** Google backend COMPLETE / ENGINEERING PASS
- **M5-D:** Apple backend + grant/notification lifecycle COMPLETE / ENGINEERING PASS
- **Group 1 / M5-E + M5-G:** authenticator lifecycle + password/passwordless adaptation ACTIVE / ENGINEERING CANDIDATE UNDER PROOF
- **Accepted PostgreSQL/Alembic head before Group 1:** `20260830_12`
- **Group 1 candidate revision:** `20260831_13` — ACL-only, pending Group 1 acceptance
- **Exact M5.2 authority:** `access-auth-m5-persistence-api-contract.md`
- **Next after Group 1 acceptance:** M5-F — WebAuthn/passkeys
- **Companion authorities:** Access/Auth architecture/security/API/testing contracts, ADR-011, Database System of Record and CP6 persistence constitution

M5 turns DANTE Account authentication into a production-grade multi-authenticator system without creating parallel Account/session authorities. M5-A through M5-D are accepted branch truth. Group 1 now materializes Account-wide authenticator lifecycle and password/passwordless behavior; public M5 HTTP/OpenAPI/Web materialization and final provider/browser acceptance remain later work.

---

## 1. Target shape

```text
Account
├── verified EmailIdentity 1..N over lifecycle
├── PasswordCredential 0..1
├── ExternalIdentity 0..N
│   ├── Google issuer + subject
│   └── Apple issuer + subject
├── WebAuthnAccount 0..1
│   └── PasskeyCredential 0..N
└── AuthSession 0..N
```

Google, Apple, password and passkey are authentication methods for the same Account. Successful proof always converges on canonical DANTE AuthSession semantics.

---

## 2. Permanent invariants

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
provider identity key = issuer + subject
provider email != provider identity
provider email coincidence != Account ownership proof
provider authentication != provider-data integration authorization
provider token/assertion != DANTE AuthSession
passwordless Account valid
PasskeyCredential != Account
method != factor != assurance
frontend/provider SDK success != backend-authoritative Auth success
provider bootstrap != permanent provider profile sync
```

Rejected:

```text
JWT/localStorage browser Auth
provider token as session
email auto-link
one Account per login method
provider profile fields dumped into Account
one permanent passkey only
generic auth-token/proof god-table
Google Auth grant reused as Calendar/Gmail grant
Apple Auth grant reused as future data-integration grant
```

---

## 3. Provider-enriched onboarding

DANTE uses provider data that is genuinely useful to remove redundant first-run questions while preserving data minimization and provenance.

Useful Google inputs when returned/validated:

```text
email / email_verified
name / given_name / family_name
picture
locale
hosted-domain metadata
protocol authentication claims
```

Useful Apple inputs when returned:

```text
email / Private Email Relay
first name on first authorization
last name on first authorization
private-email/reachability semantics
protocol authentication claims
```

Rules:

```text
first Account creation
→ provider values may initialize/stage DANTE setup/profile defaults

later user edit in DANTE
→ DANTE owns the value
→ later provider login MUST NOT overwrite it
```

No canonical DANTE username is invented from Google/Apple data.

Apple name may be one-shot. The accepted M5 persistence therefore includes bounded `account_profile_bootstrap` staging when the canonical authenticated profile/settings owner has not yet consumed it.

Provider picture URL is suggestion/bootstrap only; future import goes through the governed Asset/media boundary rather than an unrestricted server fetch.

---

## 4. Google contract

Use current Google Identity Services for Web.

Initial UX:

```text
official Google button
explicit user action
auto-select off by default
FedCM-compatible current behavior where supported
One Tap optional later, not M5 closure prerequisite
```

No Gmail/Calendar/Drive scopes belong in Auth.

Canonical identity:

```text
issuer = https://accounts.google.com
subject = sub
```

Server verifies Google ID-token evidence, including signature/JWK, allowed algorithm, issuer, audience, `azp` where required, expiry, nonce, subject and required claim shape.

JWK handling is cached/bounded. Unknown `kid` can cause one coordinated refresh, never an unbounded refresh storm.

Google email authority is classified:

```text
verified Gmail
→ Google can establish that exact mailbox

verified Workspace + hosted-domain context
→ Google can establish that exact hosted Google mailbox

Google Account using third-party mailbox
→ Google account verification alone is not treated as perpetual current mailbox control
→ DANTE mailbox proof is required where the DANTE recovery invariant needs it
```

Email never becomes the external identity key.

M5-C has already materialized and proved this backend trust/application slice. Public Google routes and browser integration remain later M5 work.

---

## 5. Apple contract

Web direction:

```text
DANTE begin transaction
→ high-entropy state + nonce
→ Apple authorization
→ form_post callback
→ claim transaction
→ server-side code exchange
→ signed ID-token verification
→ issuer + subject resolution
→ DANTE Account/link/session decision
```

Canonical issuer:

```text
https://appleid.apple.com
```

Validate signature/JWK, allowed algorithm, issuer, audience, expiry, nonce, subject and required claim shape.

Apple email including supported Private Email Relay addresses can become the exact verified DANTE EmailIdentity. Hide My Email users are not forced to reveal a hidden real mailbox.

Apple first/last name supplied on first authorization is user/profile bootstrap data, not a signed identity claim. It is validated/sanitized and durably staged when needed so it cannot be lost.

### 5.1 Apple grant lifecycle

Apple Auth has a real server-side grant lifecycle. M5 stores only the minimum durable secret required for production revoke/reconciliation.

Accepted `apple_auth_grant` states:

```text
pending
active
revocation_pending
revoked
```

A provider authorization that succeeds before DANTE linking/enrollment finishes remains durably revocable rather than becoming an orphan secret.

Refresh token material is application-layer AEAD encrypted, key-versioned, never logged and never stored in plaintext. Encryption key material stays outside PostgreSQL/Git.

Local unlink/revoke disables ExternalIdentity before remote provider network work. Provider outage cannot leave Apple login locally usable merely because remote revoke is pending.

### 5.2 Apple server notifications

M5-D handles verified signed provider notifications for relevant lifecycle classes including:

```text
email-disabled
email-enabled
consent-revoked
account-deleted
```

Email reachability uses event-time ordering so old/replayed events cannot overwrite newer truth.

Apple Account deletion/revocation does not automatically delete the DANTE Account. It updates provider binding/grant/recovery reachability according to DANTE lifecycle policy.

M5-D has already materialized and proved this backend protocol/application/grant lifecycle. Public Apple callback/notification routes, production registration and browser acceptance remain later M5 work.

---

## 6. ExternalIdentity

`ExternalIdentity` is durable security binding, not provider-profile storage.

Hard invariant:

```text
UNIQUE(issuer, subject)
```

Do not impose `UNIQUE(account_ref, provider)`; one Account may support multiple identities from the same provider if product needs it.

Normal unlink is logical revocation, not SQL DELETE. The lifetime identity row remains bound to its Account so the same provider identity cannot silently be recycled onto another Account.

Fresh proof may reactivate it only for the same Account under normal M5 lifecycle.

---

## 7. Explicit linking

Never:

```text
same provider email == same Account
```

Link requires:

```text
fresh verified provider proof
+ control of target DANTE Account
+ current session where applicable
+ recent authentication for link mutation
+ explicit user consent
+ Account security lock
+ final issuer+subject uniqueness recheck
+ atomic binding
```

Existing Account proof can be password, passkey or another accepted provider method; do not assume PasswordCredential exists.

Provider-first collision:

```text
provider proof
→ email collision
→ no duplicate Account
→ bounded ExternalLinkChallenge
→ user signs in to exact existing Account
→ explicit link confirmation
```

Authenticated Settings linking uses the already-proven Account and does not create an unnecessary second link challenge.

Group 1 materializes the backend Account-wide confirmation/unlink authority. Public link routes remain M5-H/I work.

---

## 8. Provider transaction semantics

M5 uses one short-lived `external_auth_transaction` for Google/Apple because the transaction lifecycle is genuinely shared.

Purposes:

```text
sign_in
link
reauthenticate
```

Policy:

```text
sign_in
→ anonymous

link
→ AuthSession + CSRF + recent auth at begin and completion

reauthenticate
→ AuthSession + CSRF
→ recent auth NOT required at begin
→ successful new proof refreshes recent_auth_at
→ same auth_session_ref + bearer rotation
```

Transaction stores only verifiers for high-entropy state/nonce capabilities and, for authenticated flows, the initiating `auth_session_ref` plus exact begin-time bearer-verifier snapshot.

Apple transaction is claimed before code exchange. Ambiguous single-use code exchange is not blindly retried.

---

## 9. Passkey/WebAuthn contract

M5 implements WebAuthn/passkeys, never a custom signature protocol.

```text
Account → WebAuthnAccount 0..1 → PasskeyCredential 0..N
```

Support:

```text
multiple passkeys
synced passkeys
device-bound passkeys
password managers
hardware security keys
cross-device/hybrid when platform supports it
passwordless Accounts
discoverable username-less signin
```

Registration baseline:

```text
authenticated Account
recent authentication
residentKey required
userVerification required
attestation none
exact RP ID
exact allowed origin
short single-use challenge
```

DANTE stores no biometric template, fingerprint, face data or device PIN.

WebAuthn `user.id` is a stable random 32-byte opaque user handle, never `account_ref`.

Passkey credential stores credential ID, public key, COSE algorithm, sign counter, backup eligibility/state, bounded transport hints, label and lifecycle timestamps/status.

No AAGUID/device fingerprint is persisted in M5 without a real consumer.

Non-increasing/zero sign counter after a valid assertion is a risk signal, not an automatic Account lock. Synced passkeys make blanket counter lockout incorrect.

Conditional mediation and other WebAuthn L3 capability APIs are progressive enhancement; explicit “Use a passkey” remains functional without them.

Passkey removal is logical revoke rather than physical delete, preserving lifetime credential uniqueness.

The persistence and policy foundation exists from M5-A/B; full WebAuthn ceremony implementation is **M5-F**, immediately after Group 1 acceptance.

---

## 10. Passwordless Accounts / authenticator lifecycle

Supported management capabilities:

```text
link/unlink Google
link/unlink Apple
add/remove passkey
add password to provider/passkey-only Account
remove password when safe
```

Every security-sensitive mutation is backend-authoritative, Account-lock serialized and recent-auth protected, except **reauthentication itself**, which by definition must work when freshness has expired.

### 10.1 Anti-lockout

Active direct authenticators are:

```text
PasswordCredential present
active ExternalIdentity count
active PasskeyCredential count
```

Normal authenticator removal cannot leave zero viable direct authenticators.

Passwordless Accounts must additionally retain at least one verified recovery-eligible EmailIdentity.

UI prevention is not authority; backend rechecks current durable truth under Account lock.

Group 1 materializes this Account-wide decision and includes deterministic PostgreSQL race proof as an acceptance obligation.

### 10.2 Add password

```text
session + CSRF + recent auth
+ password policy
+ HIBP fail-closed screening
+ Argon2id/pepper outside DB write transaction
→ Account lock
→ PasswordCredential still absent
→ invalidate old password-recovery proof
→ insert PasswordCredential
→ rotate current session bearer
```

### 10.3 Remove password

```text
session + CSRF + recent auth
→ Account lock
→ PasswordCredential still current
→ Account-wide anti-lockout recheck
→ invalidate old password-recovery proof
→ delete PasswordCredential
→ rotate current session bearer
```

Group 1 candidate revision `20260831_13` adds only the runtime `DELETE` privilege required for this governed mutation. It does not alter table shape, constraints, indexes or SQLAlchemy mapping.

### 10.4 Passwordless recovery

M4 recovery becomes create-or-replace:

```text
strong exact EmailIdentity + Account recovery proof
→ Account lock
→ PasswordCredential exists? replace
→ absent? create first PasswordCredential
→ conditionally consume proof
→ revoke ALL AuthSessions
→ no auto-login
→ fresh signin
```

M4 anti-enumeration, supersession, exact binding and single-use proof remain unchanged. Recovery eligibility also respects current EmailIdentity recovery restriction state.

---

## 11. Auth vs provider-data integrations

Permanent separation:

```text
Continue with Google != Connect Google Calendar/Gmail
Continue with Apple  != Connect Apple/iCloud data
```

Separate provider client/configuration, scopes, consent, token storage and revocation lifecycle where required by provider behavior.

M5 Auth requests only identity/bootstrap scopes.

Final provider configuration must prove Auth revoke/disconnect cannot accidentally destroy unrelated future provider-data authorization and vice versa.

---

## 12. Exact M5 persistence authority

The exact schema is frozen and reconciled in:

```text
docs/architecture/access-auth-m5-persistence-api-contract.md
```

M5-A materialized:

```text
ALTER email_identity
+ recovery_restriction_code
+ recovery_restriction_observed_at

CREATE
external_identity
external_auth_transaction
external_link_challenge
external_signup_challenge
account_profile_bootstrap
apple_auth_grant
webauthn_account
passkey_credential
webauthn_challenge
```

Accepted M5-A PostgreSQL/Alembic truth before Group 1:

```text
revision 20260830_12
PostgreSQL 18.6
83 tables
5 views
15 routines
75 triggers
156 physical indexes
85 foreign keys
233 CHECK constraints
103 standalone Dictionary entries
```

Group 1 candidate adds forward revision:

```text
20260831_13
GRANT DELETE ON dante.password_credential TO dante_runtime
```

This is ACL-only. It does not change topology, schema shape or mapping metadata. Until Group 1 QA closes, `20260830_12` remains the last accepted head and `20260831_13` remains candidate head.

Permanent chain:

```text
Dictionary
≈ SQLAlchemy
≈ Alembic
≈ PostgreSQL catalog
≈ human DB reference
≈ direct tests
```

---

## 13. Exact M5 API authority

Exact paths/operationIds/problems remain frozen in `access-auth-m5-persistence-api-contract.md`.

API families:

```text
Google begin/complete
Apple begin/callback/notifications
provider enrollment + OTP
provider collision link state/confirm
list/unlink providers
add/remove password
passkey registration
passkey anonymous authentication
passkey reauthentication
passkey label/remove
```

Google/Apple terminal application outcome is a typed union:

```text
authenticated
link_required
enrollment_required
```

Collision is not treated as an exception.

All successful authentication methods use canonical DANTE AuthSession.

M5-C/D and Group 1 implement backend application/persistence behavior only. **Public M5 FastAPI routes are not yet materialized**; that remains M5-H + M5-I together with deterministic OpenAPI/client generation.

---

## 14. Browser/deployment constraints

Ordinary DANTE unsafe API rules remain same-origin with existing session/CSRF/Origin/Fetch-Metadata/X-Dante-Client protections.

Apple `form_post` callback is a single reviewed provider-protocol exception whose authority is state/nonce/provider proof, not ordinary app CSRF.

No global cookie downgrade.

Provider-link/provider-enrollment continuation uses Secure HttpOnly host-only bounded flow cookies; no localStorage/sessionStorage secrets.

WebAuthn local test authority:

```text
https://localhost:<ephemeral-port>
RP ID = localhost
```

Real Apple Web closure requires a registered HTTPS domain. Real Google/Apple smoke/UAT is required before M5 production-ready closure; CI remains protocol-faithful and local/deterministic.

---

## 15. Dependencies / crypto

Do not hand-roll JOSE, WebAuthn/COSE/CBOR or AEAD.

Accepted M5-B dependency/runtime baseline:

```text
fido2         2.2.1
joserfc       1.7.4
cryptography  50.0.1
existing httpx2
Python        3.14
uv            0.12.5
```

These dependencies are already in the accepted backend lock/runtime truth. Later slices do not silently widen algorithms, trust sources or provider-data scopes.

---

## 16. Transaction/concurrency doctrine

Provider/JWK/code-exchange network work and expensive crypto stay outside authoritative DB write transactions.

Use:

```text
READ COMMITTED
Account security lock for Account-wide mutation
DB uniqueness as final identity race arbiter
conditional challenge claim/consume
operation-specific commit reconciliation only
no blanket SERIALIZABLE
no blind retries
```

Required race proof includes concurrent first provider signup, link to two Accounts, signin vs unlink/disable, Apple notification vs signin/link, passkey registration duplicate, passkey auth vs removal, add/remove password vs recovery and concurrent authenticator removals.

Group 1 specifically must prove that concurrent authenticator removals serialize on the Account lock and cannot jointly violate anti-lockout.

---

## 17. Privacy/logging

Never log provider tokens/codes/state/nonce, Apple refresh token/client key, passkey challenge/raw assertion secrets, password/session/CSRF/OTP/recovery secrets.

Provider email/name/avatar/locale are personal data. Provider subject is security identity data and is not normal UI/log material.

---

## 18. Proof posture

M5 evidence remains layered:

```text
unit/pure
!= real PostgreSQL
!= FastAPI HTTP
!= OpenAPI/generated client
!= Web UI
!= browser full-stack
!= real external provider acceptance
```

Real PostgreSQL is mandatory for physical/race claims.

Accepted prior evidence:

```text
M5-A persistence                         COMPLETE / real PostgreSQL accepted
M5-B provider/crypto policy runtime      COMPLETE / engineering pass
M5-C Google backend                      COMPLETE / engineering pass
M5-D Apple backend                       COMPLETE / engineering pass
```

Group 1 acceptance requires its own static/fast/focused PostgreSQL proof plus the relevant broader regression gate. No Group 1 PASS is claimed by this document before those runs complete.

CI uses protocol-faithful local provider substitutes through the real DANTE adapters.

Chromium/Firefox/WebKit remain the product browser matrix, with truthful recorded exceptions if an engine cannot automate a specific native WebAuthn/provider capability.

---

## 19. Current status / next step

```text
M5 overall                               ACTIVE
M5.1 architecture/external authority     COMPLETE
M5.2 persistence/API design              COMPLETE
M5-A persistence foundations             COMPLETE / ACCEPTED
M5-B provider/JWK/JOSE/AEAD infra        COMPLETE / ENGINEERING PASS
M5-C Google backend                      COMPLETE / ENGINEERING PASS
M5-D Apple backend                       COMPLETE / ENGINEERING PASS

GROUP 1 / M5-E + M5-G                    ACTIVE / ENGINEERING CANDIDATE UNDER PROOF
candidate Alembic head                   20260831_13
accepted pre-Group1 head                 20260830_12

M5-F WebAuthn/passkeys                   PLANNED / NEXT AFTER GROUP 1
M5-H + M5-I public API/OpenAPI/client    PLANNED
M5-J + M5-K+ Web + wider proof/UAT       PLANNED
```

Group 1 currently owns:

```text
provider-first explicit link confirmation
provider inventory / unlink
Account-wide anti-lockout
Apple local-first unlink + durable remote-reconcile handoff
first-password establishment
safe password removal
passwordless recovery create-or-replace
current-session bearer rotation for retained-session mutations
focused Account-lock/race proof
exact PasswordCredential DELETE ACL parity
```

Still not claimed:

```text
full WebAuthn/passkey ceremonies
public M5 FastAPI routes
OpenAPI/generated client
Access Web integration
real provider/browser acceptance
whole-M5 production-ready closure
```

Next execution step is to complete Group 1 local/static/PostgreSQL acceptance. After Group 1 is accepted, proceed directly to **M5-F — WebAuthn/passkeys** under its own exact write gate.
