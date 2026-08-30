# DANTE — Access/Auth Full-Stack Vertical Workstream

- **Status:** ACTIVE VERTICAL / M1–M4 CLOSED / M5 ACTIVE / M5.1 COMPLETE / M5.2 COMPLETE / M5-A NEXT
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Created from protected `main`:** `f011e252b6a294a12c38927ef2d528244ea1fee6`
- **M3:** CLOSED / ENGINEERING PASS / USER ACCEPTED
- **M4:** CLOSED / ENGINEERING PASS / USER ACCEPTED
- **M4 final implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **M4 documentation closure:** `a95955da72cbb9119982aa1544c2aaa356fc5e6a`
- **M5.1 checkpoint:** `8f993ace74d21c98d4034b0e521a1f9b458b007a`
- **M5.1:** COMPLETE / architecture + external-authority freeze
- **M5.2:** COMPLETE / exact persistence + API design
- **M5 architecture authority:** `../architecture/access-auth-m5-contract.md`
- **M5.2 exact design authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **M5 live handoff:** `access-auth-m5-live-handoff-2026-08-29.md`
- **M4–M7 forward plan:** `access-auth-m4-m7-execution-plan.md`
- **Observability:** full Grafana/OpenTelemetry-class baseline DEFERRED TO M7

> A new chat is not a new project, branch or worktree. Continue this vertical on `feature/access-auth` and `/home/mattia/projects/dante` until whole Access/Auth closure or an explicit user topology gate.

---

## 1. Mandatory continuation bootstrap

Continue exactly:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

The separate `/home/mattia/projects/dante-frontend` worktree is independent Home/frontend territory.

Read first:

1. `docs/PROJECT-STATUS.md`
2. `docs/ROADMAP.md`
3. this file
4. `docs/workstreams/access-auth-m5-live-handoff-2026-08-29.md`
5. `docs/architecture/access-auth-m5-contract.md`
6. `docs/architecture/access-auth-m5-persistence-api-contract.md`
7. `docs/workstreams/access-auth-m4-m7-execution-plan.md`
8. Access/Auth architecture/security/API/testing contracts + ADR-011
9. DB System of Record + `docs/database/access-auth.md` + Dictionary
10. CP6 persistence constitution
11. `docs/frontend/access.md`
12. `docs/development/agent-operating-manual.md`
13. current implementation/tests for the exact M5-A concern

Repository truth beats conversation memory. Do not reinterpret M1–M4 or rerun broad M5 discovery from scratch.

No new branch/worktree, merge, rebase, force-push/history rewrite or protected-main write without explicit user authorization.

---

## 2. Frozen semantic/Auth constitution

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived
multiple independent AuthSessions normal
provider identity key = issuer + subject
provider email never silently links Accounts
provider authentication != provider-data integration authorization
provider token/assertion != DANTE AuthSession
passwordless Account valid
verification != setup completion
reauthentication != initial signin
frontend/provider callback != backend-authoritative success
unknown/loading != signed-out/signed-in
method != factor != assurance
```

Do not reopen without a bounded explicit gate:

```text
JWT/localStorage browser Auth
Redis/JWT session authority
Principal table
silent provider-email merge
provider-specific parallel Account/session authority
Account advisory-lock replacement
Axios
generated React Query hooks as application boundary
wide credentialed CORS
fake frontend Auth success
persisted browser Auth cache
login-first then useEffect repair
hidden sign-in geometry placeholder
route deep-import of Access internals
```

---

## 3. Closed foundation

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

Permanent M3 guard:

```text
hard refresh
→ route loader resolves /auth/session
→ Query cache ready
→ AccessPage mounts once
→ first business render already authoritative
```

Permanent M4 guards:

```text
no canonical Account before accepted mailbox proof
anonymous signup does not reveal account existence
existing-account outcome only after mailbox proof
recovery initiation neutral
recovery proof single-use/superseding/exact-identity bound
password reset revokes ALL AuthSessions and never auto-logs-in
reauth rotates exact bearer on same auth_session_ref
Web recovery secret memory-only + fragment scrubbed
```

Final accepted M4 catalog remains the current materialized DB truth:

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

Accepted M4 proof:

```text
backend static / typing / lint / build        PASS
backend fast                                 87 / 87 PASS
real PostgreSQL marked suite                 87 / 87 PASS
Web Access UI                                22 / 22 PASS
real Auth full-stack browser                 33 / 33 PASS
Chromium / Firefox / WebKit                  11 / 11 PASS each
manual integrated M4 UAT                     PASS / USER ACCEPTED
```

No extra M4 QA absent direct regression evidence.

---

## 4. Current phase — M5

```text
M5 — Google + Apple + Passkeys + Explicit Linking
ACTIVE
```

M5 is the multi-authenticator Account layer, not a social-login patch.

Capability envelope:

```text
Google authentication
Sign in with Apple
ExternalIdentity = issuer + subject
provider-enriched first-account bootstrap
explicit Account linking
passkeys/WebAuthn
passwordless Accounts
add/remove password safely
safe authenticator add/remove
anti-lockout
passwordless/lost-authenticator recovery coherence
provider grant/revocation lifecycle
Apple relay/account-change lifecycle
Auth vs provider-data integration isolation
future Security & Access settings readiness
```

---

## 5. M5.1 — COMPLETE

Authority:

```text
docs/architecture/access-auth-m5-contract.md
```

Completed:

```text
Google GIS/OIDC official readback
Apple Web/REST/grant/revocation/account-change/relay readback
WebAuthn Level 3 / FIDO passkey readback
mature-product benchmark sweep
reconciliation with M2–M4 and CP6
architecture/security freeze
```

Key rules:

```text
provider identity = issuer + subject
email coincidence != link authority
provider data → first-run bootstrap only
later DANTE user edit → DANTE owns value
Apple one-shot name must not be lost
Hide My Email relay is valid EmailIdentity
Apple grant/token lifecycle is server-side and revocable
PasskeyCredential 0..N
opaque WebAuthn user handle
signCount anomaly = risk signal, not automatic lockout
passwordless Account valid
```

---

## 6. M5.2 — COMPLETE

Exact authority:

```text
docs/architecture/access-auth-m5-persistence-api-contract.md
```

M5.2 closed repository/domain/CP6 readback and froze the exact implementation design.

### 6.1 Physical target

Future M5-A persistence delta:

```text
ALTER
email_identity
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

Exactly 9 new tables. No generic auth-token/challenge table.

**This is design, not current catalog truth.** Current PostgreSQL/Alembic head remains `20260829_11` until M5-A materializes and proves it.

### 6.2 Email recovery reachability

`verified_at` remains historical mailbox-control evidence.

M5 adds provider-neutral recovery restriction state:

```text
recovery_restriction_code
recovery_restriction_observed_at
```

Apple `email-disabled` / `email-enabled` are applied only when provider event time is newer than current observed evidence, preventing out-of-order/replayed events from reversing newer reachability truth.

### 6.3 ExternalIdentity lifecycle

Hard invariant:

```text
UNIQUE(issuer, subject)
```

Normal unlink is logical `active → revoked`, not SQL DELETE. Lifetime provider identity remains bound to its Account and cannot silently be recycled onto another Account.

No artificial `UNIQUE(account_ref, provider)`.

### 6.4 Provider transaction

One bounded `external_auth_transaction` serves Google/Apple because lifecycle semantics are genuinely shared.

```text
purpose = sign_in | link | reauthenticate
TTL <= 15 minutes
state/nonce stored only as 32-byte verifiers
link/reauth bind exact auth_session_ref + begin-time bearer-verifier snapshot
single conditional claim
```

Apple transaction is claimed **before** one-use code exchange. Ambiguous code exchange is not blindly retried.

### 6.5 AppleAuthGrant

`apple_auth_grant` states:

```text
pending
active
revocation_pending
revoked
```

Pending grant may exist before Account/link finalization so an abandoned Apple authorization can still be revoked correctly.

Refresh token material:

```text
AEAD encrypted
key id/versioned
key outside PostgreSQL/Git
token never logged/browser-stored
secret cleared after confirmed revoke
```

Local ExternalIdentity revoke happens before remote network revoke. Provider outage cannot keep local Apple Auth enabled.

### 6.6 Provider collision / enrollment

Provider-first email collision:

```text
verified provider proof
→ no duplicate Account
→ external_link_challenge
→ user proves target Account
→ explicit consent
→ recent-auth recheck
→ Account lock
→ issuer+subject uniqueness recheck
→ atomic link
```

Provider proof requiring DANTE mailbox control:

```text
external_signup_challenge
→ optional mailbox input
→ purpose-separated OTP
→ verified terminal transition
→ create Account OR convert race/collision into link challenge
```

No Account before accepted mailbox proof.

### 6.7 Provider profile bootstrap

`account_profile_bootstrap` is non-canonical staging only:

```text
source provider/issuer
name/given/family/picture/locale where useful
TTL <= 30 days
insert once
future canonical profile/setup consumes/deletes
future provider login does not overwrite/refresh
```

This preserves Apple one-shot name without turning Account/ExternalIdentity into profile storage.

### 6.8 Passkeys

```text
webauthn_account
→ account_ref
→ random immutable 32-byte user_handle

passkey_credential
→ credential_id UNIQUE
→ public key / COSE algorithm
→ sign_count
→ backup eligibility/state
→ transports text[]
→ label
→ active/revoked lifecycle

webauthn_challenge
→ registration | authentication | reauthentication
→ TTL <= 5 minutes
→ exact rp_id + expected_origin
→ single conditional claim
```

Passkey removal is logical revoke, preserving lifetime credential uniqueness.

No AAGUID/device fingerprint in M5 without a concrete consumer.

### 6.9 Reauth security rule

This distinction is frozen:

```text
provider/passkey SIGN-IN
→ no existing session

provider LINK / passkey REGISTER / authenticator mutation
→ session + CSRF + recent auth

provider/passkey REAUTHENTICATE
→ session + CSRF
→ recent auth NOT required at start
→ new strong proof
→ same auth_session_ref
→ recent_auth_at refresh
→ bearer rotation
```

Requiring recent auth to begin reauthentication would be a logical deadlock and is rejected.

### 6.10 Password/anti-lockout

Active direct authenticators:

```text
PasswordCredential present
active ExternalIdentity
active PasskeyCredential
```

Normal removal may not leave zero direct authenticators. Passwordless Accounts additionally require a verified recovery-eligible EmailIdentity.

Add/remove password invalidates old pending password-recovery proof under the same Account security lock.

M4 reset becomes create-or-replace PasswordCredential while retaining all-session revoke and no-auto-login semantics.

---

## 7. Exact M5 API freeze

Frozen application API:

```text
POST   /api/v1/auth/google/begin
       auth_begin_google_authentication
POST   /api/v1/auth/google/complete
       auth_complete_google_authentication

POST   /api/v1/auth/apple/begin
       auth_begin_apple_authentication
POST   /api/v1/auth/apple/callback
       auth_handle_apple_callback
POST   /api/v1/auth/apple/notifications
       auth_process_apple_notification

GET    /api/v1/auth/provider-enrollment
       auth_get_provider_enrollment
POST   /api/v1/auth/provider-enrollment/email
       auth_set_provider_enrollment_email
POST   /api/v1/auth/provider-enrollment/verify
       auth_verify_provider_enrollment
POST   /api/v1/auth/provider-enrollment/resend
       auth_resend_provider_enrollment_verification

GET    /api/v1/auth/provider-link
       auth_get_provider_link
POST   /api/v1/auth/provider-link/confirm
       auth_confirm_provider_link

GET    /api/v1/auth/methods
       auth_get_authentication_methods
DELETE /api/v1/auth/providers/{external_identity_ref}
       auth_unlink_provider

POST   /api/v1/auth/password/establish
       auth_establish_password
DELETE /api/v1/auth/password
       auth_remove_password

POST   /api/v1/auth/passkeys/registration/begin
       auth_begin_passkey_registration
POST   /api/v1/auth/passkeys/registration/complete
       auth_complete_passkey_registration
POST   /api/v1/auth/passkeys/authentication/begin
       auth_begin_passkey_authentication
POST   /api/v1/auth/passkeys/authentication/complete
       auth_complete_passkey_authentication
POST   /api/v1/auth/passkeys/reauthentication/begin
       auth_begin_passkey_reauthentication
POST   /api/v1/auth/passkeys/reauthentication/complete
       auth_complete_passkey_reauthentication
PATCH  /api/v1/auth/passkeys/{passkey_credential_ref}
       auth_update_passkey
DELETE /api/v1/auth/passkeys/{passkey_credential_ref}
       auth_remove_passkey
```

Google/Apple complete application outcome union:

```text
authenticated
link_required
enrollment_required
```

Email collision is a typed link state, not an exception.

Provider link/enrollment continuation is held in Secure HttpOnly host-only bounded flow cookies, never localStorage/sessionStorage.

Apple callback is the single reviewed external `form_post` ingress exception and does not weaken the normal session/CSRF cookie posture.

---

## 8. M5 dependencies / deployment posture

M5.2 candidate dependency direction as of 2026-08-30:

```text
fido2 2.2.1
joserfc 1.7.4
cryptography 50.0.0
existing httpx2
```

They are not yet in `pyproject.toml`/`uv.lock`. M5-B must prove current advisories, Python 3.14, algorithm allowlists, vector behavior, logging and deterministic lock before admission.

WebAuthn local browser authority:

```text
https://localhost:<ephemeral-port>
RP ID = localhost
```

Real Apple Web closure requires registered HTTPS domain. Real Google/Apple smoke/UAT remains mandatory before M5 production-ready closure. CI stays deterministic with protocol-faithful local substitutes through real DANTE adapter paths.

---

## 9. Exact next work — M5-A

```text
M5-A — persistence foundations
NEXT / NOT STARTED
```

Sequence:

```text
M5-A1  Dictionary exact objects + EmailIdentity delta
M5-A2  SQLAlchemy mappings
M5-A3  Alembic revision + narrow runtime ACL
M5-A4  real PostgreSQL catalog/constraint/ACL/race proof
```

Do not begin Google/Apple callback implementation before the persistence foundation is materialized/proven.

M5-A requires a fresh exact Git write gate. The M5.2 documentation gate does not authorize schema/code writes.

---

## 10. M5 testing posture

Mandatory layers:

```text
unit/pure
real PostgreSQL
FastAPI HTTP
OpenAPI/generated client
Web application
browser full-stack
real external-provider acceptance
```

Do not multiply every low-level race across every browser. Prove each invariant at the truthful layer.

Chromium/Firefox/WebKit remain product-critical. Engine-specific WebAuthn/provider limitations are recorded, not faked.

---

## 11. M6 / M7

```text
M6 — Native Mobile Access
PLANNED

M7 — final whole-vertical security/observability/account-management/handoff gate
PLANNED
```

M7 owns complete user-facing session/device/security management, new-login alerts/“this wasn’t me”, full observability and final whole-vertical acceptance. M5 correctness-critical lifecycle cannot be deferred there.

---

## 12. Whole-vertical status

```text
M1 CLOSED
M2 CLOSED
M3 CLOSED
M4 CLOSED
M5 ACTIVE
  M5.1 COMPLETE
  M5.2 COMPLETE
  M5-A NEXT
M6 PLANNED
M7 PLANNED / FINAL GATE

Whole Access/Auth vertical
ACTIVE / NOT CLOSED
```

Only completion of M5–M7 plus final explicit user acceptance may close the whole Access/Auth vertical.
