# DANTE — Project Status

- **Status:** CURRENT TRUTH FOR `feature/access-auth`
- **Last reconciled:** 2026-08-30
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active product vertical:** Access/Auth
- **Last closed macro-phase:** M4 — Signup + Verification + Recovery + Reset + Reauth — **CLOSED / ENGINEERING PASS / USER ACCEPTED**
- **Current macro-phase:** M5 — Google + Apple + Passkeys + Explicit Linking — **ACTIVE**
- **M5.1:** architecture/external-authority freeze — **COMPLETE**
- **M5.2:** exact persistence + API design — **COMPLETE**
- **M5-A:** persistence foundations — **COMPLETE / REAL POSTGRESQL PROVEN**
- **Next exact step:** M5-B — provider transaction + JOSE/JWK/AEAD infrastructure — **NEXT**
- **M5-A accepted implementation checkpoint:** `7e40e02d301b0812b3f55e0d9d4ce6439e420b2a`
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
├── M5-A persistence foundations                 COMPLETE / POSTGRESQL PROVEN
└── M5-B provider/JWK/JOSE/AEAD infrastructure   NEXT

Access/Auth M6 — Native Mobile Access
PLANNED

Access/Auth M7 — Security Hardening + Observability + Authenticated Handoff
PLANNED / FINAL WHOLE-VERTICAL GATE / OBSERVABILITY MANDATORY

Whole Access/Auth vertical
ACTIVE / NOT CLOSED
```

M1–M4 remain closed unless direct defect evidence justifies a bounded reopen. M5-A proves the persistence foundation only; it does **not** claim that Google/Apple/passkey runtime, public API, generated client or Web integration already exists.

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

Accepted current M5-A materialized state:

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

Implementation hardening discovered and accepted during physical materialization:

```text
Apple grant ↔ exact ExternalIdentity issuer+subject binding
Apple link/signup challenge ↔ exact pending Apple grant identity
WebAuthn challenge ↔ exact Account/AuthSession/userHandle ownership
PasskeyCredential ↔ WebAuthnAccount ownership
backup_state=true → backup_eligible=true
logical PasskeyCredential revocation / lifetime credential-id retention
explicit cose_algorithm persistence
pending Apple grant lifecycle for abandoned-flow revocation
cleanup indexes for profile bootstrap and pending Apple grants
EmailIdentity INSERT ACL extended only to the two new nullable ORM columns
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

Observed PostgreSQL truth, not source estimation, is authoritative for accepted counts.

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

## 6. M5-A — COMPLETE / ACCEPTED

M5-A persistence foundations are **COMPLETE / REAL POSTGRESQL PROVEN**.

Accepted implementation checkpoint:

```text
7e40e02d301b0812b3f55e0d9d4ce6439e420b2a
fix(auth): reconcile M5 persistence acceptance
```

Accepted proof:

```text
uv lock                                      PASS
Ruff format                                  PASS
Ruff lint                                    PASS
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

The PostgreSQL acceptance includes retained CP6/M3/M4 regression proof and exact M5 persistence constraints/ACLs. No browser/provider full-stack claim is attached to M5-A.

---

## 7. Exact next work — M5-B

```text
M5-B — provider transaction + JOSE/JWK/AEAD infrastructure
NEXT
```

M5-B owns the bounded runtime infrastructure required before Google/Apple/WebAuthn product flows:

```text
qualify/admit exact dependencies actually consumed
current advisory/Python 3.14 compatibility proof
typed Google/Apple/WebAuthn/provider settings
bounded provider/JWK HTTP clients
JWK cache and rotation behavior
explicit JOSE algorithm allowlists
Apple grant encryption key ring / AEAD primitive
purpose-separated provider-flow verifier primitives
no provider network I/O under DB transaction
no token/assertion/bearer logging
clean lifecycle/shutdown
focused vectors + static/type/test/build proof
```

No Google/Apple end-user flow, public API/OpenAPI/client or Web Access materialization is implied unless included in the exact M5-B write gate.

---

## 8. M5 proof/deployment posture

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

## 9. M5/M7 boundary

M5 correctness includes provider/passkey lifecycle, linking, anti-lockout, provider revoke/account-change handling and correct security-management metadata.

M7 still owns the complete whole-vertical security/session/device management surface, new-login alerts/“this wasn’t me”, durable security-event/observability posture where not already required, final privacy/legal/accessibility/dependency/release review and whole-vertical acceptance.

M7 is not permission to leave M5 correctness incomplete.

---

## 10. Branch/worktree safety

Continue exactly unless explicitly changed by the user:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not touch `main`, `feature/home-react`, `feature/access-frontend` or `/home/mattia/projects/dante-frontend` without a new explicit topology/write gate.
