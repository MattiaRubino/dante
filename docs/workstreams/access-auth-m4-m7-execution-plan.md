# DANTE — Access/Auth M4–M7 Execution Plan

- **Status:** CURRENT EXECUTION PLAN / M4 CLOSED / M5 ACTIVE / M5.1 COMPLETE / M5.2 COMPLETE / M5-A NEXT / M6–M7 PLANNED
- **Vertical:** Access/Auth
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **Closed prerequisite:** M1–M4 CLOSED; M4 engineering gate PASS; user acceptance ACCEPTED
- **M4 final accepted implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **M5.1 architecture checkpoint:** `8f993ace74d21c98d4034b0e521a1f9b458b007a`
- **M5 architecture authority:** `../architecture/access-auth-m5-contract.md`
- **M5.2 authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **M5 live handoff:** `access-auth-m5-live-handoff-2026-08-29.md`
- **Observability rule:** full production-credible baseline remains mandatory at M7 if still deferred

> This plan does not reopen M1–M4 and does not authorize a new branch/worktree. Repository truth and accepted Access/Auth architecture/security/API/testing contracts remain binding.

---

## 1. Continuation rules

Continue exactly:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Before writes, follow `docs/development/agent-operating-manual.md`: exact PRE-SCOPE, exact paths, exact purpose/out-of-scope, explicit user approval, race-check, post-write compare.

No merge/rebase/history rewrite/protected-main write without explicit gate.

Read current state first:

1. `docs/PROJECT-STATUS.md`
2. `docs/ROADMAP.md`
3. `docs/workstreams/access-auth.md`
4. `docs/workstreams/access-auth-m5-live-handoff-2026-08-29.md`
5. `docs/architecture/access-auth-m5-contract.md`
6. `docs/architecture/access-auth-m5-persistence-api-contract.md`
7. this file
8. Access/Auth architecture/security/API/testing contracts + ADR-011
9. DB System of Record + `docs/database/access-auth.md` + Dictionary
10. CP6 persistence constitution
11. `docs/frontend/access.md`
12. current implementation/tests for the exact slice

---

## 2. M1–M4 frozen foundations

Reuse, do not replace:

```text
Account = durable access/security root
EmailIdentity separate from Account
PasswordCredential optional
Principal runtime-derived
opaque PostgreSQL-backed AuthSession
multiple independent AuthSessions normal
same-origin Web Auth
Secure HttpOnly host-only __Host-dante-session
session-bound CSRF
Origin + Fetch Metadata + X-Dante-Client
/api/v1 + RFC9457
Account security serialization point
READ COMMITTED + targeted locking
no blind mutation retry
FastAPI/Pydantic → deterministic OpenAPI → Orval Fetch → governed @dante/api-client
TanStack Query remote lifecycle
TanStack Router critical-session bootstrap
real PostgreSQL proof
real HTTPS Chromium + Firefox + WebKit proof
```

Permanent M3 lesson:

```text
unknown/loading != signed-out != signed-in != empty != error
```

Permanent M4 lessons:

```text
no Account before accepted mailbox proof
anti-enumeration before mailbox/account disclosure
purpose-specific proof persistence
recovery proof exact-identity binding
single-use reset + revoke all sessions + fresh signin
reauth rotates exact bearer on same AuthSession
external email/network outside DB transaction
Web recovery bearer memory-only + URL scrub
```

M4 accepted catalog remains current materialized truth:

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

No further M4 QA absent direct defect evidence.

---

# 3. M5 — Google + Apple + Passkeys + Explicit Linking

**Status:** `ACTIVE`

Authorities:

```text
docs/architecture/access-auth-m5-contract.md
docs/architecture/access-auth-m5-persistence-api-contract.md
```

Save-game:

```text
docs/workstreams/access-auth-m5-live-handoff-2026-08-29.md
```

---

## 3.1 M5.1 — COMPLETE

Completed:

```text
Google GIS/OIDC external-authority review
Sign in with Apple Web/REST/grant/revocation/relay/account-change review
WebAuthn L3/FIDO review
browser/provider deployment constraints
mature-product benchmark sweep
reconciliation with M2–M4 + CP6
architecture/security semantic freeze
```

Frozen capability envelope:

```text
ExternalIdentity = issuer + subject
provider email != Account merge key
DANTE AuthSession remains canonical
provider-enriched onboarding with provenance
provider bootstrap never silently overwrites DANTE-owned values
Apple one-shot name preserved
Apple Hide My Email supported
Apple server-side grant/revoke/notification lifecycle
explicit linking only after Account proof + consent
PasskeyCredential 0..N
opaque WebAuthn user handle
resident/discoverable passkeys + UV required
passwordless Account
add/remove password capability
safe authenticator removal / anti-lockout
passwordless email recovery
Auth/provider-data grant isolation
```

---

## 3.2 M5.2 — COMPLETE

M5.2 froze exact persistence/API/state/race design before code.

### Physical target

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

Exactly 9 new tables.

No persistence is accepted yet. Alembic remains `20260829_11` until M5-A proof.

### Important M5.2 hardening

```text
ExternalIdentity unlink = logical revoke, not delete
Passkey removal = logical revoke, not delete
provider identity UNIQUE(issuer,subject)
passkey identity UNIQUE(credential_id)
AppleAuthGrant supports pending unbound grant for abandoned-flow revocation
Apple remote revoke occurs outside DB tx after local disable
Apple relay reachability uses event-time ordering
provider transaction is claimed before Apple code exchange
reauth requires session+CSRF but not already-fresh recent-auth
provider/link/register/remove mutations require recent-auth
provider profile bootstrap expires after <=30 days and never resyncs
```

### Exact API inventory

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
PATCH  /api/v1/auth/passkeys/{passkey_credential_ref}
DELETE /api/v1/auth/passkeys/{passkey_credential_ref}
```

OperationIds and problem codes are frozen in the M5.2 authority.

Provider result union:

```text
authenticated
link_required
enrollment_required
```

---

# 4. M5-A — Persistence Foundations

**Status:** `NEXT / NOT STARTED`

M5-A should be executed in a bounded gate before any Google/Apple/WebAuthn runtime adapter work.

## M5-A1 — Dictionary

Materialize exact current-spec objects:

```text
UPDATE
email_identity Dictionary entry

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

Every Dictionary object records:

```text
purpose/canonicality
semantic/domain traceability
exact columns/types/nullability
PK/FK/UQ/CHECK
index reasons
lifecycle/retention
security/ACL target
proof obligations
```

Do not claim catalog truth yet.

## M5-A2 — SQLAlchemy

Materialize exact mappings in existing Auth persistence boundary.

Rules:

```text
no Repository/UoW framework invention
mappings mirror exact Dictionary types/constraints
adapters flush, outer application owns transaction
no provider network in persistence adapters
```

## M5-A3 — Alembic

One canonical revision from `20260829_11` unless implementation evidence requires a separately gated split.

Must include:

```text
EmailIdentity ALTER
9 tables
exact PK/FK/UQ/CHECK
justified indexes
REVOKE default/public/runtime/migrator posture for new objects
least-privilege runtime grants
narrow EmailIdentity UPDATE grant
downgrade exact inverse
```

Applied migration becomes immutable evidence under MIG-02 after acceptance.

## M5-A4 — Persistence acceptance

Focused fast/static proof first; then real PostgreSQL 18.6 proof.

Prove:

```text
single Alembic head/DAG
Dictionary validation/parity
SQLAlchemy/import/static/type/lint
fresh upgrade from accepted baseline
catalog exact table/column/constraint/index counts
constraint negative cases
runtime ACL exactness
owner/migrator/runtime role separation
flow claim uniqueness where DB is arbiter
ExternalIdentity issuer+subject race
Passkey credential-id duplicate race
Email reachability event ordering
AppleGrant lifecycle constraints
clean downgrade where project acceptance requires it
```

Do not run browser/provider full-stack during M5-A unless a direct regression requires it.

---

# 5. M5-B — Provider / JOSE / AEAD Infrastructure

**Status:** PLANNED after M5-A acceptance.

Candidate baseline identified in M5.2:

```text
fido2        2.2.1
joserfc      1.7.4
cryptography 50.0.0
httpx2       existing
```

Before lock admission:

```text
Python 3.14
current advisory state
uv deterministic lock
explicit algorithm allowlists
JWK/key-rotation vectors
WebAuthn ceremony vectors
DANTE-owned counter policy
no unsafe token/credential logging
Ruff/mypy/tests/build
```

Materialize typed nested Auth settings for Google/Apple/WebAuthn/key ring. No scattered `os.getenv()`.

Build bounded provider/JWK HTTP clients with current M4 lifecycle discipline: process-scoped clients, bounded timeouts/connection pools, coordinated JWK refresh, clean shutdown.

---

# 6. M5-C — Google Authentication

Implement:

```text
GIS begin/complete
OIDC nonce/transaction binding
JWK validation
known identity signin
new Account with provider-authoritative mailbox
third-party Google mailbox → provider enrollment
email collision → explicit link-required flow
provider reauthentication
provider Settings link
profile bootstrap
```

No Gmail/Calendar/Drive scopes.

Proof includes invalid iss/aud/signature/nonce/expiry, unknown kid bounded refresh, provider cancel/outage, identity/profile changes, races and canonical DANTE AuthSession issuance.

---

# 7. M5-D — Apple Authentication / Grant / Notifications

Implement:

```text
Apple begin authorization URL
form_post callback
transaction claim before code exchange
server-side code exchange
ID-token/JWK validation
new Account / collision / enrollment / reauth / link
one-shot name staging
Hide My Email
pending → active grant binding
revocation_pending → remote revoke → revoked
signed server notification verification
email-disabled/email-enabled event ordering
consent-revoked/account-deleted reconciliation
```

Real Web production readiness requires registered HTTPS Services ID/domain and Private Email Relay sender configuration.

No blind retry of ambiguous authorization-code exchange or remote revocation mutation.

---

# 8. M5-E — Explicit Linking / Authenticator Management

Implement current-account method view and safe link/unlink.

Key invariant:

```text
provider email coincidence != link
```

Provider-first linking:

```text
provider proof
→ targeted ExternalLinkChallenge
→ prove exact Account
→ recent auth
→ explicit consent
→ Account lock
→ uniqueness recheck
→ atomic binding
```

Normal provider unlink = local logical revoke first, then provider grant reconciliation where needed.

Implement anti-lockout using backend-authoritative active authenticator counts and recovery reachability.

---

# 9. M5-F — WebAuthn / Passkeys

Implement:

```text
opaque 32-byte WebAuthn user handle
registration begin/complete
residentKey required
UV required
attestation none
username-less discoverable signin
reauth begin/complete
multiple passkeys
synced/device-bound/hardware/password-manager credentials
backup state/counter update policy
safe label/remove
logical revoke
```

WebAuthn local test origin:

```text
https://localhost:<ephemeral-port>
RP ID localhost
```

No biometric/PIN material; no AAGUID/device fingerprint unless a future consumer justifies it.

---

# 10. M5-G — Passwordless Password/Recovery Adaptation

Implement:

```text
add first PasswordCredential
safe password removal
pending recovery invalidation on normal password mutation
M4 reset create-or-replace PasswordCredential
all-session revoke
no auto-login
```

Use existing HIBP/Argon2/pepper policy and Account security lock.

No second password system.

---

# 11. M5-H / M5-I — Public API / Generated Client

Materialize the exact API contract from M5.2.

Requirements:

```text
/api/v1
stable operationIds
Pydantic request/response types
RFC9457
no-store
request_id
provider outcome union
Apple form_post exception documented
Apple notification ingress documented
OpenAPI deterministic without live providers/secrets
Orval Fetch + generated Zod
governed @dante/api-client only
raw generated ops not product API
```

No frontend raw fetch bypass.

---

# 12. M5-J — Access Web / Smart Onboarding

Maintain accepted M1 design quality and M3/M4 session architecture.

Primary actions:

```text
Continue with Google
Continue with Apple
Use a passkey
email/password path remains
```

Use official provider branding. Never imitate provider credential UI.

Required states:

```text
provider pending/cancel/error
provider account created
known provider signin
link required
link confirm
provider enrollment/email OTP
passkey selector/cancel/error
backend-authoritative success only
```

Smart onboarding:

```text
validated provider name/email/avatar/locale available
→ do not ask redundant fields
→ stage/consume only useful values
→ later DANTE-owned values win
```

Full long-lived Home Security Settings can be built in authenticated Home phase/M7, but M5 backend/API must already support it without rearchitecture.

---

# 13. M5-K+ — Focused Proof / Acceptance

Proof sequence:

```text
focused unit/protocol vectors
real PostgreSQL race/constraint/ACL acceptance
FastAPI exact HTTP contract
OpenAPI/generated client drift proof
Web component/application tests
browser full-stack Chromium/Firefox/WebKit
real Google smoke/UAT
real Apple registered-domain smoke/UAT
real WebAuthn/passkey UAT
manual integrated M5 UAT
docs reconciliation
explicit user acceptance
```

Do not run every low-level race across every browser.

No public provider dependency in mandatory CI; use protocol-faithful substitutes through real DANTE adapters.

---

# 14. M5 proof obligations

### Provider common

```text
state/nonce replay rejection
provider cancel/error/outage
issuer+subject authority
JWK/key rotation
email collision never silent-links
explicit link requires Account proof + consent
link replay/race
provider profile never overwrites user-owned values
canonical DANTE AuthSession only
```

### Google

```text
known identity
new Account
authoritative mailbox distinction
third-party Google mailbox enrollment
invalid signature/issuer/audience/expiry/nonce
unknown kid bounded refresh
email/profile changes preserve binding
```

### Apple

```text
form_post/state/nonce/code exchange
claim before exchange
ID-token validation
one-shot name
Private Relay
pending/active encrypted grant
revocation_pending reconciliation
signed notifications
event ordering
registered-domain UAT
```

### WebAuthn

```text
RP ID/origin/challenge/userHandle
registration/assertion replay/expiry
UV required
discoverable signin
multiple passkeys
duplicate prevention
backup/counter policy
safe removal/anti-lockout
passwordless recovery
```

---

# 15. M6 — Native Mobile Access

**Status:** `PLANNED / AFTER M5 UNLESS EXPLICITLY RE-GATED`

Reuse canonical Account/AuthSession authority with native transport/storage:

```text
Keychain / Keystore / SecureStore
app restart/background lifecycle
logout/revoke
multi-device
deep links/provider callbacks
native passkeys
uninstall/reinstall semantics
real emulator/device proof
```

Native is not scaled Web.

---

# 16. M7 — Security Hardening + Observability + Authenticated Handoff

**Status:** `PLANNED / FINAL WHOLE-VERTICAL GATE`

M7 owns:

```text
whole-vertical threat/abuse/replay review
complete session/account/device management
new-login alerts / “this wasn’t me”
provider/linking/WebAuthn/native final hardening
production-credible observability
privacy/legal/accessibility/dependency/release review
real authenticated handoff into next DANTE vertical
whole-vertical manual UAT
```

If observability remains deferred, M7 may not close without privacy-safe structured logs, request/trace correlation, metrics/traces, collector/backend topology, useful dashboards/queries and secret-redaction proof.

Telemetry outage must not break Auth correctness.

---

# 17. Whole-vertical closure

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
