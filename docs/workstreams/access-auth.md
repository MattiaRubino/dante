# DANTE — Access/Auth Full-Stack Vertical Workstream

- **Status:** ACTIVE VERTICAL / M1–M4 CLOSED / M5 ACTIVE / M5.1–M5-C COMPLETE / M5-D NEXT
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Created from protected `main`:** `f011e252b6a294a12c38927ef2d528244ea1fee6`
- **M3:** CLOSED / ENGINEERING PASS / USER ACCEPTED
- **M4:** CLOSED / ENGINEERING PASS / USER ACCEPTED
- **M5.1:** COMPLETE / architecture + external-authority freeze
- **M5.2:** COMPLETE / exact persistence + API design
- **M5-A:** COMPLETE / REAL POSTGRESQL PROVEN
- **M5-B:** COMPLETE / ENGINEERING PASS / provider-JWK-JOSE-AEAD-WebAuthn policy infrastructure
- **M5-C:** COMPLETE / ENGINEERING PASS / Google authentication + Account creation/collision
- **M5-D:** NEXT / Apple authentication + grant/notification lifecycle
- **M5-C accepted implementation checkpoint:** `e6f738a1ea3f5152caa7d99f1d6ccd108747c806`
- **M5-B accepted implementation checkpoint:** `e2d40a7666e3c0130afecd8113b8063390b86b9d`
- **M5-A accepted implementation checkpoint:** `7e40e02d301b0812b3f55e0d9d4ce6439e420b2a`
- **M4 final implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **M4 documentation closure:** `a95955da72cbb9119982aa1544c2aaa356fc5e6a`
- **M5.1 checkpoint:** `8f993ace74d21c98d4034b0e521a1f9b458b007a`
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
13. current implementation/tests for the exact M5-D concern

Repository truth beats conversation memory. Do not reinterpret M1–M4 or redo broad M5 discovery from scratch.

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
Axios as alternate Auth boundary
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
CLOSED / ACCEPTED / QA PASS

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

Accepted M4 proof remains:

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

All successful authentication methods converge on canonical DANTE `AuthSession`.

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

M5.2 froze the exact implementation design before code.

Physical envelope:

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

M5.2 also froze:

```text
provider identity issuer+subject authority
provider transaction claim/replay semantics
Apple pending grant + remote revoke lifecycle
provider collision/enrollment challenge state
provider bootstrap staging
WebAuthn Account/passkey/challenge model
passwordless add/remove/recovery race rules
exact public API paths + operationIds + problems
provider outcome union
Apple callback/notification topology
WebAuthn RP/origin topology
dependency direction
proof-layer matrix
```

---

## 7. M5-A — COMPLETE / REAL POSTGRESQL PROVEN

M5-A materialized only the persistence foundation frozen by M5.2.

Current accepted database truth:

```text
PostgreSQL          18.6
Alembic             20260830_12
83 tables
5 views
15 routines
75 triggers
156 physical indexes
85 foreign keys
233 CHECK constraints
103 standalone Dictionary entries
```

Accepted implementation checkpoint:

```text
7e40e02d301b0812b3f55e0d9d4ce6439e420b2a
fix(auth): reconcile M5 persistence acceptance
```

Accepted proof:

```text
uv lock                                      PASS
Ruff format / lint                           PASS
mypy strict                                  PASS
backend fast                                 87 / 87 PASS
real PostgreSQL 18.6                         95 / 95 PASS
M5 persistence tests                          8 / 8 PASS
migration head/base/head                      PASS
Alembic autogenerate drift                    PASS
Dictionary ≈ SQLAlchemy ≈ Alembic ≈ PG       PASS
runtime ACL / negative constraints            PASS
backend build                                 PASS
```

Physical hardening accepted during implementation:

```text
ExternalIdentity composite exact Apple identity target
AppleAuthGrant exact issuer+subject binding
Apple link/signup challenge exact grant identity binding
AuthSession composite Account ownership target
WebAuthnAccount composite Account+userHandle target
WebAuthnChallenge exact Account/session/userHandle FKs
PasskeyCredential ownership through WebAuthnAccount
explicit cose_algorithm
logical passkey revocation
backup_state => backup_eligible
cleanup indexes for profile-bootstrap/pending Apple grant
column-scoped EmailIdentity INSERT/UPDATE reconciliation
```

M5-A does **not** claim provider end-user flows, FastAPI public API, generated client, Web Access, provider smoke/UAT or browser M5 acceptance.

---

## 8. M5-B — COMPLETE / ENGINEERING PASS

```text
M5-B — Provider/JWK/JOSE/AEAD/WebAuthn Policy Infrastructure
COMPLETE / ENGINEERING PASS
```

Accepted implementation checkpoint:

```text
e2d40a7666e3c0130afecd8113b8063390b86b9d
chore(auth): finalize M5-B lock and formatting
```

Admitted baseline:

```text
fido2         2.2.1
joserfc       1.7.4
cryptography  50.0.1
existing httpx2
Python        3.14
uv            0.12.5
```

Implemented:

```text
typed provider configuration with safe disabled defaults
bounded provider/JWK HTTP runtime
trusted configured JWKS authority only
strict RS256 JOSE allowlist and canonical compact admission
coordinated JWK cache, conditional revalidation, rotation and unknown-kid cooldown
JWKS byte/key-count/duplicate/private-material bounds
Apple AES-256-GCM grant key ring / 12-byte nonce / stable AAD
purpose-separated provider-flow verifiers
FIDO2 WebAuthn RP/origin policy baseline
process-scoped ProviderRuntime inside existing AuthRuntime lifecycle
no provider network I/O at startup
```

Accepted proof:

```text
uv lock --check                              PASS
Ruff autofix / format / lint                 PASS
mypy strict                                  PASS / 73 source files
backend fast                                 127 / 127 PASS
backend build                                PASS / sdist + wheel
git diff --check                             PASS
```

M5-B changes no schema/Alembic/Dictionary, so the already accepted M5-A PostgreSQL gate was not rerun absent direct regression evidence.

---

## 9. M5-C — COMPLETE / ENGINEERING PASS

```text
M5-C — Google Authentication + Account Creation / Collision
COMPLETE / ENGINEERING PASS
```

Accepted implementation checkpoint:

```text
e6f738a1ea3f5152caa7d99f1d6ccd108747c806
chore(auth): finalize M5-C formatting
```

Implemented:

```text
Google GIS/OIDC begin + complete application flow
transaction/state/nonce verifier-only persistence
single conditional claim / replay rejection
trusted JWK signature verification through M5-B runtime
issuer/audience/azp/nonce/exp/iat/nbf/subject validation
canonical issuer and issuer+subject identity authority
known ExternalIdentity signin
provider-authoritative mailbox → passwordless Account + verified EmailIdentity
third-party Google mailbox → DANTE provider-enrollment OTP
email collision → explicit link_required, never silent merge
Google reauthentication and Settings-link session binding
provider profile bootstrap staging
canonical DANTE AuthSession issuance/rotation only
bounded provider ingress limits
commit ambiguity / uniqueness race reconciliation
```

Accepted proof:

```text
uv lock --check                              PASS
Ruff format / format-check / lint            PASS
mypy strict                                  PASS / 79 source files
backend fast                                 148 / 148 PASS
focused real PostgreSQL M5-C                  7 / 7 PASS
backend build                                PASS / sdist + wheel
git diff --check                             PASS
```

M5-C does not expose the later public API/Web UI and does not claim real Google browser/provider UAT.

---

## 10. Exact next slice — M5-D

```text
M5-D — Apple Authentication + Grant / Notification Lifecycle
NEXT
```

M5-D goal: reuse the accepted provider/runtime and provider-flow foundation while implementing Apple-specific authorization-code, grant, relay and notification semantics without creating parallel auth authority.

Required direction:

```text
Apple begin authorization URL
form_post callback
claim transaction before code exchange
server-side code exchange outside DB transaction
trusted JWK signature + issuer/audience/nonce/expiry/subject validation
known ExternalIdentity signin
new Account / collision / provider enrollment
provider link + reauthentication semantics as frozen
one-shot Apple name bootstrap preservation
Hide My Email / provider_email_private semantics
pending AppleAuthGrant after successful exchange
pending → active exact ExternalIdentity binding
revocation_pending → remote revoke → revoked
signed server notification verification
email-disabled/email-enabled event-time ordering
consent-revoked/account-deleted reconciliation
canonical DANTE AuthSession only
```

Still out of scope for M5-D unless separately re-gated:

```text
full provider unlink/authenticator management
full passkey ceremonies
password lifecycle adaptation
public M5 API/OpenAPI/client
Access Web UI
provider-data integration authorization
real whole-M5 provider/browser acceptance
```

No blind retry of ambiguous authorization-code exchange or non-idempotent provider mutation.

---

## 11. Provider-enriched onboarding

User requirement remains: take **all provider data genuinely useful to DANTE** at mature-app quality, then let DANTE own/edit resulting values later.

Frozen rule:

```text
provider data
→ validate/classify provenance
→ eliminate redundant onboarding
→ initialize/stage useful setup/profile values
→ user later edits in DANTE
→ future provider login never silently overwrites DANTE-owned values
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
hosted-domain metadata
security/authentication claims actually supplied
```

Useful Apple bootstrap:

```text
email or Private Email Relay
first/last name on initial authorization when supplied
private-email/reachability semantics
security/authentication claims actually supplied
```

No DANTE username is inferred.

Apple name may be one-shot; `account_profile_bootstrap` exists so later lifecycle code can preserve it without dumping profile state into Account/ExternalIdentity.

---

## 12. Exact provider/link/passkey invariants carried forward

### ExternalIdentity

```text
identity key = issuer + subject
UNIQUE(issuer,subject)
normal unlink = logical revoke, not DELETE
provider email/name/avatar changes never move identity to another Account
```

### Provider transaction

```text
purpose = sign_in | link | reauthenticate
TTL <= 15 min
state/nonce verifier only
link/reauth bind exact auth_session_ref + begin-time bearer verifier snapshot
single conditional claim
Apple claim before code exchange
```

### Provider-first collision

```text
verified provider proof
+ email matches existing EmailIdentity
→ no duplicate Account
→ explicit targeted link challenge
→ prove exact Account
→ consent + recent auth
→ Account lock
→ issuer+subject uniqueness recheck
→ atomic binding
```

### Apple grant

```text
pending → active → revocation_pending → revoked
refresh token AEAD encrypted
key outside PostgreSQL/Git
local ExternalIdentity revoke first
remote Apple revoke outside DB tx
```

### Passkeys

```text
opaque random 32-byte user_handle
credential_id lifetime UNIQUE
resident/discoverable direction
UV required
attestation none
multiple passkeys
logical revoke
backup/signCount metadata handled as risk state, not fake device identity
```

---

## 13. Frozen public API inventory for later M5-H/I

```text
POST   /api/v1/auth/google/begin
POST   /api/v1/auth/google/complete

POST   /api/v1/auth/apple/begin
POST   /api/v1/auth/apple/callback
POST   /api/v1/auth/apple/notifications

GET    /api/v1/auth/provider-enrollment
POST   /api/v1/auth/provider-enrollment/email
POST   /api/v1/auth/provider-enrollment/verify
POST   /api/v1/auth/provider-enrollment/resend

GET    /api/v1/auth/provider-link
POST   /api/v1/auth/provider-link/confirm

GET    /api/v1/auth/methods
DELETE /api/v1/auth/providers/{external_identity_ref}

POST   /api/v1/auth/password/establish
DELETE /api/v1/auth/password

POST   /api/v1/auth/passkeys/registration/begin
POST   /api/v1/auth/passkeys/registration/complete
POST   /api/v1/auth/passkeys/authentication/begin
POST   /api/v1/auth/passkeys/authentication/complete
POST   /api/v1/auth/passkeys/reauthentication/begin
POST   /api/v1/auth/passkeys/reauthentication/complete
DELETE /api/v1/auth/passkeys/{passkey_credential_ref}
```

No frontend route or generated client may redefine these semantics independently.

---

## 14. Whole-vertical state

```text
M1 CLOSED
M2 CLOSED
M3 CLOSED
M4 CLOSED
M5 ACTIVE
  M5.1 COMPLETE
  M5.2 COMPLETE
  M5-A COMPLETE / POSTGRESQL PROVEN
  M5-B COMPLETE / ENGINEERING PASS
  M5-C COMPLETE / ENGINEERING PASS
  M5-D NEXT
M6 PLANNED
M7 PLANNED / FINAL GATE

Whole Access/Auth vertical
ACTIVE / NOT CLOSED
```
