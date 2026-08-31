# DANTE Roadmap

- **Status:** CURRENT FOR `feature/access-auth`
- **Last reconciled:** 2026-08-31
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active vertical:** Access/Auth
- **Last closed macro-phase:** M4 — Signup + Verification + Recovery + Reset + Reauth
- **Current macro-phase:** M5 — Google + Apple + Passkeys + Explicit Linking
- **M5.1:** COMPLETE
- **M5.2:** COMPLETE
- **M5-A:** COMPLETE / REAL POSTGRESQL PROVEN
- **M5-B:** COMPLETE / ENGINEERING PASS
- **M5-C:** COMPLETE / ENGINEERING PASS
- **M5-D:** COMPLETE / ENGINEERING PASS
- **Next exact step:** M5-E — Explicit Linking + Authenticator Lifecycle
- **M5-D accepted implementation checkpoint:** `7d13b712f032e8d41d7cf03d406555fd9f3c0160`
- **M5-C accepted implementation checkpoint:** `e6f738a1ea3f5152caa7d99f1d6ccd108747c806`
- **M5-B accepted implementation checkpoint:** `e2d40a7666e3c0130afecd8113b8063390b86b9d`
- **M5-A accepted implementation checkpoint:** `7e40e02d301b0812b3f55e0d9d4ce6439e420b2a`
- **M5 architecture authority:** `architecture/access-auth-m5-contract.md`
- **M5.2 authority:** `architecture/access-auth-m5-persistence-api-contract.md`
- **M5 continuation handoff:** `workstreams/access-auth-m5-live-handoff-2026-08-29.md`
- **Forward execution authority:** `workstreams/access-auth-m4-m7-execution-plan.md`
- **Observability:** full baseline DEFERRED TO M7

## 1. Current sequence

```text
Product / North Star
        CURRENT
          ↓
Domain / Logical / Pre-Physical / Physical
        CLOSED
          ↓
Engineering + Frontend + Backend CP1–CP6
        CLOSED / ACCEPTED
          ↓
Access pre-backend Web materialization
        CLOSED / ACCEPTED
          ↓
M1 — Visual / UX Freeze
        CLOSED / ACCEPTED
          ↓
M2 — Auth Architecture Freeze
        CLOSED / ACCEPTED / QA PASS
          ↓
M3 — Email/Password Signin + AuthSession Spine
        CLOSED / ENGINEERING PASS / USER ACCEPTED
          ↓
M4 — Signup + Verification + Recovery + Reset + Reauth
        CLOSED / ENGINEERING PASS / USER ACCEPTED
          ↓
M5 — Google + Apple + Passkeys + Explicit Linking
        ACTIVE
          ↓
M5.1 — External Authority + Benchmark + Architecture Freeze
        COMPLETE
          ↓
M5.2 — Exact Persistence + API Design
        COMPLETE
          ↓
M5-A — Persistence Foundations
        COMPLETE / REAL POSTGRESQL PROVEN
          ↓
M5-B — Provider/JWK/JOSE/AEAD Infrastructure
        COMPLETE / ENGINEERING PASS
          ↓
M5-C — Google Authentication + Account Creation / Collision
        COMPLETE / ENGINEERING PASS
          ↓
M5-D — Apple Authentication + Grant/Notification Lifecycle
        COMPLETE / ENGINEERING PASS
          ↓
M5-E — Explicit Linking + Authenticator Lifecycle
        NEXT
          ↓
M5-F — WebAuthn / Passkeys
        PLANNED
          ↓
M5-G — Passwordless Password/Recovery Adaptation
        PLANNED
          ↓
M5-H/I — FastAPI/OpenAPI + Governed Client
        PLANNED
          ↓
M5-J — Access Web / Smart Onboarding
        PLANNED
          ↓
M5-K+ — Focused Proof / PostgreSQL / Browser / Provider UAT / Acceptance
        PLANNED
          ↓
M6 — Native Mobile Access
        PLANNED
          ↓
M7 — Security Hardening + Observability + Authenticated Handoff
        PLANNED / FINAL WHOLE-VERTICAL GATE
```

The whole Access/Auth vertical is **not closed**. M5-A proves its persistence boundary, M5-B proves the shared provider/JWK/JOSE/AEAD/WebAuthn-policy runtime foundation, M5-C proves the Google backend application/persistence slice, and M5-D proves the Apple backend protocol/application/persistence/grant-lifecycle slice. Public M5 API, generated client, Access Web integration, complete authenticator management and real provider/browser acceptance remain later work.

---

## 2. Database progression

Accepted M3 baseline:

```text
Alembic             20260827_10
72 tables
5 views
15 routines
75 triggers
104 physical indexes
71 foreign keys
137 CHECK constraints
92 standalone Dictionary entries
```

Accepted M4 historical baseline:

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

Accepted/current M5-A materialized state:

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

M5-A materialized:

```text
ALTER dante.email_identity
  + recovery_restriction_code
  + recovery_restriction_observed_at

CREATE
  dante.external_identity
  dante.external_auth_transaction
  dante.external_link_challenge
  dante.external_signup_challenge
  dante.account_profile_bootstrap
  dante.apple_auth_grant
  dante.webauthn_account
  dante.passkey_credential
  dante.webauthn_challenge
```

Physical implementation hardening accepted during M5-A:

```text
ExternalIdentity exact Apple issuer+subject composite target
AppleAuthGrant exact ExternalIdentity issuer+subject binding
Apple link/signup challenge exact grant identity binding
AuthSession exact auth_session_ref+account_ref composite target
WebAuthnAccount exact account_ref+user_handle composite target
WebAuthnChallenge exact Account+AuthSession ownership
PasskeyCredential ownership through WebAuthnAccount
explicit cose_algorithm
logical passkey revocation
backup_state => backup_eligible
profile-bootstrap / pending-grant cleanup indexes
least-privilege EmailIdentity INSERT/UPDATE delta
```

Permanent rule:

```text
Dictionary
≈ SQLAlchemy
≈ Alembic
≈ real PostgreSQL catalog
≈ current human DB reference
≈ direct tests
```

---

## 3. Frozen foundation reused through M5

```text
same-origin Web Auth
opaque PostgreSQL-backed AuthSession
Secure HttpOnly __Host-dante-session
session-bound CSRF + Origin + Fetch Metadata + X-Dante-Client
runtime-only Principal
multiple independent AuthSessions
Argon2id + HIBP + purpose-separated secrets
/api/v1 + RFC9457
READ COMMITTED + targeted Account serialization
no blind mutation retry
FastAPI → deterministic OpenAPI → Orval Fetch → governed @dante/api-client
TanStack Query remote lifecycle
Router-first critical session bootstrap
real PostgreSQL + Chromium/Firefox/WebKit proof
```

M4 additionally freezes:

```text
no Account before accepted mailbox proof
existing-account disclosure only after mailbox proof
neutral recovery initiation
single-use reset + revoke ALL sessions + no auto-login
reauth rotates exact presented bearer on same auth_session_ref
recovery secret memory-only + URL scrub
```

M5 adds:

```text
provider identity = issuer + subject
provider email != silent Account link
Google/Apple/password/passkeys converge on DANTE AuthSession
provider-enriched onboarding, then DANTE-owned profile state
Apple one-shot name preservation
Apple grant/revocation/server-notification lifecycle
explicit Account linking
passkeys 0..N + opaque user handle
passwordless Account
safe add/remove authenticators
anti-lockout
passwordless recovery create-or-replace password
Auth vs provider-data grant isolation
```

---

# 4. M5.1 — COMPLETE

Completed:

```text
current Google GIS/OIDC readback
current Sign in with Apple Web/REST/grant/relay/account-change readback
current WebAuthn Level 3 / FIDO readback
mature-product benchmark sweep
reconciliation with M2–M4 and CP6
architecture/security semantics freeze
```

Authority:

```text
docs/architecture/access-auth-m5-contract.md
```

---

# 5. M5.2 — COMPLETE

Completed:

```text
physical ownership and 9-table minimal delta
EmailIdentity recovery reachability evolution
exact PK/FK/UQ/CHECK/index design
least-privilege runtime ACL design
provider transaction claim/replay semantics
Apple pending grant + remote revoke reconciliation
provider collision/link challenge
provider enrollment + OTP challenge
one-shot profile bootstrap staging
WebAuthn Account/passkey/challenge design
passwordless add/remove/recovery race rules
exact API paths + operationIds
provider outcome union + machine problems
Apple callback/notification topology
WebAuthn RP/origin topology
dependency direction
proof-layer/race matrix
```

Authority:

```text
docs/architecture/access-auth-m5-persistence-api-contract.md
```

M5.2 was a design freeze; M5-A subsequently materialized only the persistence subset.

---

# 6. M5-A — COMPLETE / ACCEPTED

**Purpose:** materialize only the persistence foundation frozen in M5.2 and prove it on real PostgreSQL 18.6.

Implemented:

```text
M5-A1  Dictionary objects + EmailIdentity delta                 COMPLETE
M5-A2  SQLAlchemy mappings                                      COMPLETE
M5-A3  Alembic 20260830_12 + runtime ACL                        COMPLETE
M5-A4  real PostgreSQL catalog/constraint/ACL/migration proof   COMPLETE
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

No Google/Apple provider HTTP client, JOSE/JWK runtime, WebAuthn library, public M5 API, generated client or Web UI was smuggled into M5-A.

---

# 7. M5-B — COMPLETE / ENGINEERING PASS

M5-B owns the accepted **Provider/JWK/JOSE/AEAD/WebAuthn Policy Infrastructure** baseline.

Accepted implementation checkpoint:

```text
e2d40a7666e3c0130afecd8113b8063390b86b9d
```

Admitted dependencies:

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
explicit RS256 JOSE allowlist and strict compact/header admission
typed Google/Apple/WebAuthn provider settings
bounded provider/JWK HTTP runtime
coordinated JWK cache/rotation/unknown-kid refresh cooldown
conditional ETag/Last-Modified revalidation
JWKS size/key-count/duplicate/private-material rejection
Apple AES-256-GCM grant key ring with stable AAD contract
purpose-separated provider-flow verifier primitives
FIDO2 WebAuthn RP/origin/policy construction
process-scoped provider runtime + clean shutdown
no provider network I/O at startup
```

Accepted proof:

```text
uv lock --check                              PASS
Ruff autofix / format / lint                 PASS
mypy strict                                  PASS / 73 source files
backend fast                                 127 / 127 PASS
backend build                                PASS
git diff --check                             PASS
```

M5-B changes no schema/Alembic/Dictionary; the accepted M5-A PostgreSQL gate was therefore not rerun absent regression evidence.

---

# 8. M5-C — COMPLETE / ENGINEERING PASS

M5-C consumes the M5-B trust/runtime foundation and implements the Google backend product path without creating parallel Account/session authority.

Accepted implementation checkpoint:

```text
e6f738a1ea3f5152caa7d99f1d6ccd108747c806
```

Implemented:

```text
Google OIDC begin/complete application flow
state/nonce verifier-only transaction persistence and single claim
trusted JWK/RS256 verification through M5-B runtime
issuer/audience/azp/nonce/exp/iat/nbf/subject validation
canonical issuer + issuer/subject identity authority
Gmail/Workspace/third-party mailbox authority classification
known ExternalIdentity signin
provider-authoritative mailbox → passwordless Account
third-party mailbox → DANTE provider-enrollment OTP
email collision → explicit link_required, never silent merge
Google link and reauth exact AuthSession binding
canonical DANTE AuthSession issuance/rotation only
provider profile bootstrap staging only
bounded provider ingress limits
commit ambiguity/race reconciliation
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

The PostgreSQL proof covers verifier-only transaction state/replay rejection, Account/EmailIdentity/ExternalIdentity/AuthSession creation, identity reuse, collision→link, third-party enrollment, enrollment collision, concurrent same-sub convergence and link/reauth behavior.

M5-C does not yet expose public M5 routes or Access Web Google UI and does not claim real Google browser/provider acceptance; those remain later M5 slices.

---

# 9. M5-D — COMPLETE / ENGINEERING PASS

M5-D consumes the shared provider runtime and the M5-A Apple persistence foundation without introducing parallel Account/session authority.

Accepted implementation checkpoint:

```text
7d13b712f032e8d41d7cf03d406555fd9f3c0160
```

Implemented:

```text
Apple Web begin/form_post authorization topology
state/nonce server-authoritative transaction and pre-exchange single claim
front-channel ID token + server-side authorization-code exchange convergence
issuer/audience/nonce/exp/iat/subject/c_hash verification
ES256 Apple client-secret issuance
single-use code exchange with no blind retry on ambiguous transport result
one-shot Apple name/profile bootstrap
Hide My Email recognition for privaterelay.appleid.com + private.icloud.com
known identity signin / new passwordless Account / collision / provider enrollment
Apple link + reauth bound to canonical DANTE AuthSession
AES-256-GCM refresh grant with exact grant+issuer+subject+client AAD
pending→active→revocation_pending→revoked grant lifecycle
local-first revoke + bounded idempotent remote reconciliation
signed server-notification handling
email-disabled/email-enabled ordered recovery restriction updates
consent-revoked/account-deleted identity/grant reconciliation
ambiguous PostgreSQL commit reconciliation
same issuer+subject race convergence without active-grant regression
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

M5-D does not expose public M5 routes or Access Web Apple UI and does not claim Apple registered-domain/browser/provider UAT or Private Email Relay sender setup; those remain later M5 gates.

---

# 10. M5-E onward

```text
M5-E — NEXT
explicit provider link/unlink
+ authenticator lifecycle / auth methods API semantics
+ anti-lockout

M5-F
WebAuthn registration / username-less signin / reauth / management

M5-G
establish/remove password
+ passwordless recovery adaptation

M5-H/I
FastAPI/Pydantic exact public contract
→ deterministic OpenAPI
→ Orval Fetch/Zod
→ governed @dante/api-client

M5-J
Access UI
→ official Google/Apple controls
→ passkey
→ provider-enrollment/link states
→ smart provider-enriched onboarding

M5-K+
focused security/race proof
→ whole-stage PostgreSQL acceptance where needed
→ browser acceptance
→ real provider UAT
→ manual UAT
→ docs reconciliation
→ explicit user acceptance
```

---

# 11. Browser/provider acceptance topology

Mandatory CI:

```text
no public provider dependency
protocol-faithful local provider substitute
real DANTE adapter/application/security path
```

M5 closure additionally requires:

```text
real Google provider smoke/UAT
real Apple registered-domain smoke/UAT
Apple Private Email Relay delivery configuration
real HTTPS WebAuthn/passkey acceptance
```

WebAuthn local target:

```text
https://localhost:<ephemeral-port>
RP ID localhost
```

Chromium/Firefox/WebKit remain critical. Engine-specific native capability gaps are recorded truthfully rather than bypassed/faked.

---

# 12. M6 / M7

```text
M6 — Native Mobile Access
PLANNED / AFTER M5 UNLESS RE-GATED

M7 — Security Hardening + Observability + Authenticated Handoff
PLANNED / FINAL WHOLE-VERTICAL GATE
```

M7 owns complete session/device/security management, new-login alerts/“this wasn’t me”, whole-vertical observability and final release/privacy/accessibility/security acceptance. It does not absorb unfinished M5 lifecycle correctness.

---

# 13. Whole-vertical closure rule

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
  M5-D COMPLETE / ENGINEERING PASS
  M5-E NEXT
M6 PLANNED
M7 PLANNED / FINAL GATE

Whole Access/Auth vertical
ACTIVE / NOT CLOSED
```

Only completion of M5–M7 plus final explicit user acceptance may close the whole Access/Auth vertical.
