# DANTE Roadmap

- **Status:** CURRENT FOR `feature/access-auth`
- **Last reconciled:** 2026-08-30
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active vertical:** Access/Auth
- **Last closed macro-phase:** M4 — Signup + Verification + Recovery + Reset + Reauth
- **Current macro-phase:** M5 — Google + Apple + Passkeys + Explicit Linking
- **M5.1:** COMPLETE
- **M5.2:** COMPLETE
- **Next exact step:** M5-A — persistence foundations
- **M4 final accepted implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
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
        NEXT / NOT STARTED
          ↓
M5-B — Provider/JWK/JOSE/AEAD Infrastructure
        PLANNED
          ↓
M5-C — Google Authentication
        PLANNED
          ↓
M5-D — Apple Authentication + Grant/Notification Lifecycle
        PLANNED
          ↓
M5-E — Explicit Linking + Authenticator Lifecycle
        PLANNED
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

The whole Access/Auth vertical is **not closed**. M5.1/M5.2 are design gates only; they do not imply runtime/schema/API capability and do not authorize merge to `main`.

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

Accepted/current M4 materialized state:

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

M5.2 adds **design only**, no accepted persistence yet.

Frozen M5-A target:

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

Exact columns/PK/FK/UQ/CHECK/index/ACL are authoritative in:

```text
docs/architecture/access-auth-m5-persistence-api-contract.md
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

No schema/code/dependency/OpenAPI/client/Web materialization occurred in M5.2.

---

# 6. M5-A — NEXT

**Purpose:** materialize only the persistence foundation frozen in M5.2.

Recommended split:

```text
M5-A1
Database Dictionary
→ 9 new table entries
→ email_identity Dictionary evolution

M5-A2
SQLAlchemy auth mappings

M5-A3
one canonical Alembic revision from 20260829_11
→ tables/constraints/indexes
→ runtime ACL
→ downgrade exact inverse

M5-A4
focused tests
→ Dictionary parity
→ migration head/DAG
→ real PostgreSQL catalog
→ exact ACL
→ negative constraints
→ synchronization races where persistence itself is arbiter
```

Do not add Google/Apple provider HTTP clients, JOSE dependencies, WebAuthn dependencies or frontend code merely because they are downstream consumers unless a separate approved gate includes them.

---

# 7. M5-B onward

```text
M5-B
provider/JWK/JOSE/AEAD infrastructure
→ qualify/pin fido2, joserfc, cryptography where actually consumed
→ typed provider settings
→ bounded JWK cache/network timeouts
→ encrypted Apple grant key ring

M5-C
Google signin/new Account/collision/reauth/link

M5-D
Apple begin/form_post/code exchange/new Account/link/reauth
+ pending/active grant lifecycle
+ revoke reconciliation
+ signed notifications
+ Private Relay state

M5-E
explicit provider link/unlink
+ auth methods API
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
→ real PostgreSQL acceptance
→ browser acceptance
→ real provider UAT
→ manual UAT
→ docs reconciliation
→ explicit user acceptance
```

---

# 8. Browser/provider acceptance topology

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

# 9. M6 / M7

```text
M6 — Native Mobile Access
PLANNED / AFTER M5 UNLESS RE-GATED

M7 — Security Hardening + Observability + Authenticated Handoff
PLANNED / FINAL WHOLE-VERTICAL GATE
```

M7 owns complete session/device/security management, new-login alerts/“this wasn’t me”, whole-vertical observability and final release/privacy/accessibility/security acceptance. It does not absorb unfinished M5 lifecycle correctness.

---

# 10. Whole-vertical closure rule

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
