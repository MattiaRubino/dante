# DANTE — Project Status

- **Status:** CURRENT TRUTH FOR `feature/access-auth`
- **Last reconciled:** 2026-08-30
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active product vertical:** Access/Auth
- **Last closed macro-phase:** M4 — Signup + Verification + Recovery + Reset + Reauth — **CLOSED / ENGINEERING PASS / USER ACCEPTED**
- **Current macro-phase:** M5 — Google + Apple + Passkeys + Explicit Linking — **ACTIVE**
- **M5.1:** architecture/external-authority freeze — **COMPLETE**
- **M5.2:** exact persistence + API design — **COMPLETE**
- **Next exact step:** M5-A — persistence foundations — **NEXT / NOT STARTED**
- **Final accepted M4 implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **M4 documentation closure:** `a95955da72cbb9119982aa1544c2aaa356fc5e6a`
- **M5.1 documentation checkpoint:** `8f993ace74d21c98d4034b0e521a1f9b458b007a`
- **M5 architecture authority:** `architecture/access-auth-m5-contract.md`
- **M5.2 exact design authority:** `architecture/access-auth-m5-persistence-api-contract.md`
- **M5 continuation handoff:** `workstreams/access-auth-m5-live-handoff-2026-08-29.md`
- **Forward execution authority:** `workstreams/access-auth-m4-m7-execution-plan.md`
- **Observability:** full production-credible baseline DEFERRED TO M7; this does not weaken M5 correctness requirements

## 1. Executive state

```text
Product / North Star                       CURRENT
Domain Model                               CLOSED
Logical Model                              CLOSED / 57 OF 57
Pre-Physical Coherence                     CLOSED / FINAL QA PASS
Physical PostgreSQL target                 CLOSED
Engineering + Frontend + Backend CP1–CP6  CLOSED / ACCEPTED
Access pre-backend Web materialization     CLOSED / ACCEPTED

Access/Auth M1 — Visual / UX Freeze
CLOSED / ACCEPTED

Access/Auth M2 — Auth Architecture Freeze
CLOSED / ACCEPTED / QA PASS

Access/Auth M3 — Email/Password Signin + AuthSession Spine
CLOSED / ENGINEERING PASS / USER ACCEPTED

Access/Auth M4 — Signup + Verification + Recovery + Reset + Reauth
CLOSED / ENGINEERING PASS / USER ACCEPTED

Access/Auth M5 — Google + Apple + Passkeys + Explicit Linking
ACTIVE
├── M5.1 architecture/external-authority freeze  COMPLETE
├── M5.2 exact persistence + API design          COMPLETE
└── M5-A persistence foundations                 NEXT / NOT STARTED

Access/Auth M6 — Native Mobile Access
PLANNED

Access/Auth M7 — Security Hardening + Observability + Authenticated Handoff
PLANNED / FINAL WHOLE-VERTICAL GATE / OBSERVABILITY MANDATORY

Whole Access/Auth vertical
ACTIVE / NOT CLOSED
```

M1–M4 remain closed unless direct defect evidence justifies a bounded reopen. M5.1/M5.2 completion is a design freeze, **not evidence that M5 runtime capability exists**.

---

## 2. Current database truth

Protected-main CP6 historical baseline:

```text
PostgreSQL          18.6
Alembic             20260826_08
68 tables
5 views
14 routines
75 triggers
95 physical indexes
68 foreign keys
120 CHECK constraints
```

Accepted M3 branch baseline:

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

Accepted M4 branch state — still the **current materialized DB truth**:

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

M5.2 freezes a future persistence delta but does not materialize it.

Frozen M5-A target design:

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

Until M5-A migrations/tests are accepted:

```text
accepted Alembic head = 20260829_11
M5 tables in PostgreSQL = 0
M5 Dictionary objects = 0
```

Permanent structural invariant:

```text
Database Dictionary
≈ SQLAlchemy mappings
≈ Alembic head
≈ current PostgreSQL catalog
≈ current human DB reference
≈ direct tests
```

---

## 3. Binding Access/Auth invariants

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
provider identity key = issuer + subject
provider authentication != provider-data integration authorization
provider email never silently links Accounts
provider token/assertion != DANTE AuthSession
passwordless Account is valid
verification != setup completion
reauthentication != initial signin
method != factor != assurance
frontend/provider callback != backend-authoritative success
unknown/loading != signed-out/signed-in
```

Rejected without new bounded evidence/architecture gate:

```text
JWT/localStorage browser Auth
Redis/JWT session authority
Principal persistence table
silent provider-email Account merge
provider email as ExternalIdentity key
provider-specific parallel session authority
Account advisory-lock replacement
Axios as alternate Auth boundary
generated React Query hooks as app boundary
wide credentialed CORS
fake frontend Auth success
persisted browser Auth cache
provider profile fields dumped into Account
```

---

## 4. Closed M3/M4 foundation

M3 API:

```text
POST   /api/v1/auth/signin
GET    /api/v1/auth/session
DELETE /api/v1/auth/session
```

M4 API:

```text
POST /api/v1/auth/signup
POST /api/v1/auth/signup/verify
POST /api/v1/auth/signup/resend
POST /api/v1/auth/recovery
POST /api/v1/auth/recovery/validate
POST /api/v1/auth/reset-password
POST /api/v1/auth/reauthenticate
```

Permanent behavior:

```text
hard refresh resolves authoritative /auth/session before Access business render
no Account before accepted mailbox proof
existing-account signup reveals existence only after mailbox proof
neutral recovery initiation
single-use exact EmailIdentity+Account recovery proof
reset revokes ALL AuthSessions + no auto-login
reauth rotates exact bearer on same auth_session_ref
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

Do not rerun M4 QA absent direct regression evidence.

---

## 5. M5.1 + M5.2 freeze — COMPLETE

M5.1 authority:

```text
docs/architecture/access-auth-m5-contract.md
```

M5.2 exact implementation-design authority:

```text
docs/architecture/access-auth-m5-persistence-api-contract.md
```

Frozen capability envelope:

```text
Google Identity Services authentication
Sign in with Apple
ExternalIdentity = issuer + subject
provider-enriched first-account bootstrap
Apple one-shot name preservation
Apple Hide My Email + grant/revocation/notification lifecycle
explicit Account linking only
passkeys/WebAuthn 0..N
opaque WebAuthn user handle
passwordless Accounts
add/remove password safely
safe authenticator add/remove + anti-lockout
passwordless email recovery create-or-replace password
Auth vs provider-data integration isolation
future Home → Security/Access readiness
```

M5.2 additionally freezes:

```text
9-table persistence delta + EmailIdentity recovery-reachability evolution
exact PK/FK/UQ/CHECK/index/ACL design
Apple pending/active/revocation grant state
provider transaction claim/replay semantics
provider collision/enrollment challenge state
exact public API paths + operationIds + problem codes
provider outcome union: authenticated | link_required | enrollment_required
WebAuthn RP/origin/challenge model
Google/Apple link vs reauth security policy
dependency direction: fido2 + joserfc + cryptography
real PostgreSQL/provider/browser proof layers
```

Provider/profile data remains bootstrap only; later user-owned DANTE values are never silently overwritten by provider login.

---

## 6. Exact next work — M5-A

```text
M5-A — persistence foundations
NEXT / NOT STARTED
```

Order:

```text
M5-A1  Dictionary objects + EmailIdentity delta
M5-A2  SQLAlchemy mappings
M5-A3  Alembic migration + runtime ACL
M5-A4  real PostgreSQL catalog/constraint/ACL/race acceptance
```

M5-A must be separately write-gated before modifying implementation/schema files.

No dependency/OpenAPI/Web/provider adapter change is implied by M5-A unless explicitly included in that future gate.

---

## 7. M5 proof/deployment posture

```text
provider CI = deterministic protocol-faithful local substitutes
real DANTE adapter/security path still executes
real Google/Apple smoke/UAT required before M5 closure
Apple Web production proof needs registered HTTPS domain
Apple Private Email Relay sender configuration must be proven
WebAuthn local target = https://localhost:<port>, RP ID localhost
Chromium/Firefox/WebKit remain product-critical browser matrix
real PostgreSQL required for schema/race claims
```

Provider/JWK/token/network work stays outside DB transactions. No blind retry of non-idempotent/single-use provider operations.

---

## 8. M5/M7 boundary

M5 correctness includes provider/passkey lifecycle, linking, anti-lockout, provider revoke/account-change handling and correct security-management metadata.

M7 still owns the complete whole-vertical security/session/device management surface, new-login alerts/“this wasn’t me”, durable security-event/observability posture where not already required, final privacy/legal/accessibility/dependency/release review and whole-vertical acceptance.

M7 is not permission to leave M5 correctness incomplete.

---

## 9. Branch/worktree safety

Continue exactly unless explicitly changed by the user:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not touch `main`, `feature/home-react`, `feature/access-frontend` or `/home/mattia/projects/dante-frontend` without a new explicit topology/write gate.
