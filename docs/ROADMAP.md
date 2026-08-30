# DANTE Roadmap

- **Status:** CURRENT FOR `feature/access-auth`
- **Last reconciled:** 2026-08-30
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active vertical:** Access/Auth
- **Last closed macro-phase:** M4 — Signup + Verification + Recovery + Reset + Reauth
- **Current macro-phase:** M5 — Google + Apple + Passkeys + Explicit Linking
- **M5.1:** COMPLETE
- **M5.2:** COMPLETE
- **M5-A:** COMPLETE / REAL POSTGRESQL PROVEN
- **Next exact step:** M5-B — Provider/JWK/JOSE/AEAD Infrastructure
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
        NEXT
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

The whole Access/Auth vertical is **not closed**. M5-A proves only its persistence boundary and does not imply provider runtime, API, client, Web or provider/browser acceptance.

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
WebAuthnChallenge exact Account/AuthSession/userHandle ownership
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

# 7. M5-B — NEXT

M5-B owns **Provider/JWK/JOSE/AEAD Infrastructure**.

Required gate direction:

```text
qualify dependencies actually consumed
Python 3.14 compatibility + current advisory review
deterministic uv lock
explicit JOSE algorithm allowlists
typed Google/Apple/WebAuthn settings
bounded provider/JWK HTTP clients
JWK cache + rotation behavior
Apple grant AEAD key ring / AES-256-GCM baseline
purpose-separated provider transaction verifiers
secret/token/assertion logging controls
process-scoped lifecycle / clean shutdown
focused vectors + static/type/test/build
```

Candidate dependency direction identified in M5.2:

```text
fido2         2.2.1
joserfc       1.7.4
cryptography  50.0.x baseline
existing httpx
```

Versions are candidates until M5-B performs current qualification and lock admission.

---

# 8. M5-C onward

```text
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
→ whole-stage PostgreSQL acceptance where needed
→ browser acceptance
→ real provider UAT
→ manual UAT
→ docs reconciliation
→ explicit user acceptance
```

---

# 9. Browser/provider acceptance topology

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

# 10. M6 / M7

```text
M6 — Native Mobile Access
PLANNED / AFTER M5 UNLESS RE-GATED

M7 — Security Hardening + Observability + Authenticated Handoff
PLANNED / FINAL WHOLE-VERTICAL GATE
```

M7 owns complete session/device/security management, new-login alerts/“this wasn’t me”, whole-vertical observability and final release/privacy/accessibility/security acceptance. It does not absorb unfinished M5 lifecycle correctness.

---

# 11. Whole-vertical closure rule

```text
M1 CLOSED
M2 CLOSED
M3 CLOSED
M4 CLOSED
M5 ACTIVE
  M5.1 COMPLETE
  M5.2 COMPLETE
  M5-A COMPLETE / POSTGRESQL PROVEN
  M5-B NEXT
M6 PLANNED
M7 PLANNED / FINAL GATE

Whole Access/Auth vertical
ACTIVE / NOT CLOSED
```

Only completion of M5–M7 plus final explicit user acceptance may close the whole Access/Auth vertical.
