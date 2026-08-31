# DANTE — Access/Auth M4–M7 Execution Plan

- **Status:** CURRENT EXECUTION PLAN / M4 CLOSED / M5 ACTIVE / M5.1–M5-D COMPLETE / M5-E NEXT / M6–M7 PLANNED
- **Vertical:** Access/Auth
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **Closed prerequisite:** M1–M4 CLOSED; M4 engineering gate PASS; user acceptance ACCEPTED
- **M5-D accepted implementation checkpoint:** `7d13b712f032e8d41d7cf03d406555fd9f3c0160`
- **M5-C accepted implementation checkpoint:** `e6f738a1ea3f5152caa7d99f1d6ccd108747c806`
- **M5-B accepted implementation checkpoint:** `e2d40a7666e3c0130afecd8113b8063390b86b9d`
- **M5-A accepted implementation checkpoint:** `7e40e02d301b0812b3f55e0d9d4ce6439e420b2a`
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

Accepted M4 catalog remains historical baseline:

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

Physical target subsequently materialized by M5-A:

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

Important frozen hardening:

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

Frozen public API inventory remains in the M5.2 authority and is materialized later in M5-H/I, not by M5-A/M5-B/M5-C/M5-D.

---

# 4. M5-A — Persistence Foundations

**Status:** `COMPLETE / REAL POSTGRESQL PROVEN`

Accepted implementation checkpoint:

```text
7e40e02d301b0812b3f55e0d9d4ce6439e420b2a
fix(auth): reconcile M5 persistence acceptance
```

Current accepted DB truth:

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

## M5-A1 — Dictionary

Completed:

```text
EmailIdentity evolution
9 new table entries
current constraints/index/lifecycle/ACL metadata
scope/count reconciliation
```

## M5-A2 — SQLAlchemy

Completed exact Auth persistence mappings without Repository/UoW framework invention.

## M5-A3 — Alembic

Completed one canonical revision from `20260829_11`:

```text
20260830_12
→ EmailIdentity ALTER
→ 9 tables
→ exact PK/FK/UQ/CHECK
→ justified indexes
→ default-deny/new-object REVOKE posture
→ least-privilege runtime grants
→ exact downgrade inverse
```

## M5-A4 — Persistence acceptance

Accepted proof:

```text
uv lock                                      PASS
Ruff format / lint                           PASS
mypy strict                                  PASS
backend fast                                 87 / 87 PASS
real PostgreSQL 18.6                         95 / 95 PASS
M5 persistence tests                          8 / 8 PASS
single Alembic head/DAG                       PASS
fresh upgrade                                 PASS
previous-head upgrade                         PASS
head/base/head round-trip                     PASS
Alembic autogenerate drift                    PASS
Dictionary ≈ SQLAlchemy ≈ Alembic ≈ PG       PASS
runtime ACL / negative constraints            PASS
CP6/M3/M4 DB regressions                      PASS
backend build                                 PASS
```

Physical implementation refinements accepted during M5-A:

```text
ExternalIdentity composite exact Apple target
AppleAuthGrant exact issuer+subject binding
Apple link/signup challenge exact grant binding
AuthSession composite Account ownership target
WebAuthnAccount composite Account+userHandle target
WebAuthnChallenge exact Account/session/userHandle FKs
PasskeyCredential ownership through WebAuthnAccount
explicit cose_algorithm
logical PasskeyCredential revocation
backup_state => backup_eligible
profile-bootstrap/pending-grant cleanup indexes
column-scoped EmailIdentity INSERT/UPDATE reconciliation
PostgreSQL-safe shortened Apple challenge FK names
```

M5-A browser/provider full-stack was intentionally not run because no provider/Web product capability was introduced.

---

# 5. M5-B — Provider / JOSE / JWK / AEAD Infrastructure

**Status:** `COMPLETE / ENGINEERING PASS`

Accepted implementation checkpoint:

```text
e2d40a7666e3c0130afecd8113b8063390b86b9d
chore(auth): finalize M5-B lock and formatting
```

Accepted dependency/runtime baseline:

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
deterministic uv lock
explicit RS256 JOSE allowlist
strict compact/header/Base64URL admission
nested typed Google/Apple/WebAuthn settings
bounded provider/JWK HTTP clients and connection/time bounds
trusted configured JWKS authority only
coordinated JWK cache + conditional revalidation + bounded refresh
unknown-kid cooldown preventing refresh storms
JWKS response/key-count/duplicate/private-material rejection
Apple grant AES-256-GCM key ring + 12-byte nonce + stable AAD
purpose-separated 256-bit flow verifier primitives
FIDO2 WebAuthn RP/origin policy baseline
process-scoped runtime + clean shutdown
no provider network I/O at process startup
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

No scattered `os.getenv()` was introduced; settings remain typed/governed.

Provider/JWK/token network calls remain outside DB transactions.

M5-B changed no DB schema/Alembic/Dictionary, so the accepted M5-A PostgreSQL gate was not rerun absent direct regression evidence.

---

# 6. M5-C — Google Authentication

**Status:** `COMPLETE / ENGINEERING PASS`.

Accepted implementation checkpoint:

```text
e6f738a1ea3f5152caa7d99f1d6ccd108747c806
chore(auth): finalize M5-C formatting
```

Implemented:

```text
GIS/OIDC begin + complete application flow
OIDC nonce/state verifier-only transaction persistence
single claim / replay rejection
JWK validation through accepted M5-B runtime
issuer/audience/azp/nonce/exp/iat/nbf/subject validation
canonical Google issuer + issuer/subject identity authority
known ExternalIdentity signin
new passwordless Account under provider-authoritative mailbox rules
third-party Google mailbox → provider enrollment OTP
email collision → explicit link_required, never silent merge
provider reauthentication
provider Settings link semantics under frozen M5 contract
profile bootstrap staging only
canonical DANTE AuthSession issuance/rotation only
bounded provider ingress limits
commit ambiguity / uniqueness-race reconciliation
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

The focused PostgreSQL proof covers verifier-only transaction persistence/replay rejection, passwordless Account creation and identity reuse, collision→link, third-party enrollment, enrollment collision, concurrent same Google identity convergence and link/reauth behavior.

No Gmail/Calendar/Drive scopes. Public M5 routes, Access Web Google UI and real Google browser/provider UAT remain later slices.

---

# 7. M5-D — Apple Authentication / Grant / Notifications

**Status:** `COMPLETE / ENGINEERING PASS`.

Accepted implementation checkpoint:

```text
7d13b712f032e8d41d7cf03d406555fd9f3c0160
chore(auth): finalize M5-D formatting
```

Implemented:

```text
Apple Web authorization begin + form_post-compatible topology
transaction claim before single-use code exchange
front-channel ID token + server-side exchange identity convergence
issuer/audience/nonce/exp/iat/subject/c_hash verification
ES256 Apple client-secret issuance
ambiguous code exchange → reconciliation-pending, never blind retry
new Account / collision / enrollment / reauth / link
one-shot Apple name/profile staging
Hide My Email classification for privaterelay.appleid.com + private.icloud.com
AES-256-GCM pending/active Apple grant with grant+issuer+subject+client AAD
local-first revoke → revocation_pending → remote revoke → revoked
bounded revocation-pending reconciliation + secret wipe
signed server notification verification
email-disabled/email-enabled event-time ordering
consent-revoked/account-deleted identity/grant reconciliation
ambiguous DB commit reconciliation
concurrent same issuer+subject convergence without active-grant regression
```

Accepted proof:

```text
uv lock --check                              PASS
Ruff autofix / format / format-check / lint PASS
mypy src                                     PASS / 49 source files
backend fast                                 171 / 171 PASS
focused real PostgreSQL M5-D                  9 / 9 PASS
full real PostgreSQL regression              111 / 111 PASS
backend build                                PASS / sdist + wheel
git diff --check                             PASS
```

The full PostgreSQL acceptance retains M4, Google, M5 persistence, CP6 catalog/constraint/ACL/migration/runtime/transaction proof while proving Apple grant and lifecycle races on real PostgreSQL.

Real Web production readiness still requires registered HTTPS Services ID/domain, Private Email Relay sender configuration and real Apple provider/browser UAT in later M5 gates.

---

# 8. M5-E — Explicit Linking / Authenticator Management

**Status:** `NEXT`.

Materialize current-account method view and safe provider link/unlink lifecycle using the provider-specific proof primitives already accepted in M5-C/M5-D.

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

M5-E must implement backend-authoritative active authenticator counts and recovery reachability before any removal, and preserve lifetime `(issuer, subject)` ownership.

Do not keep adding provider-neutral lifecycle responsibility to `apple_flow.py`; extract shared authenticator-management collaboration where the M5-E boundary requires it.

---

# 9. M5-F — WebAuthn / Passkeys

**Status:** PLANNED.

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

No biometric/PIN material; no AAGUID/device fingerprint without a real consumer.

---

# 10. M5-G — Passwordless Password/Recovery Adaptation

**Status:** PLANNED.

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

**Status:** PLANNED.

Materialize exact API contract from M5.2.

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

**Status:** PLANNED.

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

---

# 13. M5-K+ — Focused Proof / Acceptance

**Status:** PLANNED.

Proof sequence:

```text
focused unit/protocol vectors
real PostgreSQL race/constraint/ACL proof where later lifecycle adds behavior
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
invalid signature/issuer/audience/azp/expiry/nonce
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
RP ID/origin/challenge verification
user verification required
discoverable username-less signin
credential-id duplicate rejection
counter/backup-state handling
multiple passkeys
safe logical removal
reauth on same AuthSession with bearer rotation
```

---

# 15. M6 / M7

```text
M6 — Native Mobile Access
PLANNED / AFTER M5 UNLESS RE-GATED

M7 — Security Hardening + Observability + Authenticated Handoff
PLANNED / FINAL WHOLE-VERTICAL GATE
```

M7 owns complete session/device/security management, new-login alerts/“this wasn’t me”, whole-vertical observability and final release/privacy/accessibility/security acceptance. It does not absorb unfinished M5 lifecycle correctness.

---

# 16. Current execution pointer

```text
M1 CLOSED
M2 CLOSED
M3 CLOSED
M4 CLOSED
M5 ACTIVE
  M5.1 COMPLETE
  M5.2 COMPLETE
  M5-A COMPLETE / REAL POSTGRESQL PROVEN
  M5-B COMPLETE / ENGINEERING PASS
  M5-C COMPLETE / ENGINEERING PASS
  M5-D COMPLETE / ENGINEERING PASS
  M5-E NEXT
M6 PLANNED
M7 PLANNED / FINAL GATE
```

M5-E is now the exact next slice. It must consume the accepted Google/Apple provider-specific proof and lifecycle primitives rather than rebuilding or bypassing them.