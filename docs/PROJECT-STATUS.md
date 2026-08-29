# DANTE — Project Status

- **Status:** CURRENT TRUTH FOR `feature/access-auth`
- **Last reconciled:** 2026-08-29
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active product vertical:** Access/Auth
- **Last closed macro-phase:** M4 — Signup + Verification + Recovery + Reset + Reauth — **CLOSED / ENGINEERING PASS / USER ACCEPTED**
- **Current macro-phase:** M5 — Google + Apple + Passkeys + Explicit Linking — **ACTIVE**
- **M5.1:** external-authority + benchmark + architecture/security freeze — **COMPLETE**
- **Next exact step:** M5.2 — exact persistence + API design — **NEXT / NOT STARTED**
- **Final accepted M4 implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **M4 documentation closure:** `a95955da72cbb9119982aa1544c2aaa356fc5e6a`
- **M4 closure handoff:** `workstreams/access-auth-m4-live-handoff-2026-08-29.md`
- **M5 architecture authority:** `architecture/access-auth-m5-contract.md`
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
├── M5.1 architecture/external-authority freeze   COMPLETE
└── M5.2 exact persistence + API design           NEXT / NOT STARTED

Access/Auth M6 — Native Mobile Access
PLANNED

Access/Auth M7 — Security Hardening + Observability + Authenticated Handoff
PLANNED / FINAL WHOLE-VERTICAL GATE / OBSERVABILITY MANDATORY

Whole Access/Auth vertical
ACTIVE / NOT CLOSED
```

M1–M4 remain closed unless direct defect evidence justifies a bounded reopen. M5.1 is a semantic/architecture freeze, **not evidence that M5 runtime capability exists**.

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

Accepted M4 branch state:

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

M5 has **no accepted persistence delta yet**. Current accepted head remains `20260829_11` until M5.2 freezes exact objects and a separately gated implementation materializes/proves them.

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
frontend request/provider callback != backend-authoritative success
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

## 4. Closed M3 production spine

M3 API remains:

```text
POST   /api/v1/auth/signin
GET    /api/v1/auth/session
DELETE /api/v1/auth/session
```

Accepted chain:

```text
FastAPI/Pydantic
→ deterministic OpenAPI 3.1
→ Orval Fetch + generated Zod
→ governed @dante/api-client
→ Web Auth remote
→ TanStack Query
→ Access feature
→ TanStack Router critical-session bootstrap
```

Permanent refresh rule:

```text
hard refresh
→ Router loader resolves authoritative /auth/session
→ Query cache ready
→ AccessPage mounts once
→ first business render already signed-in or signed-out
```

---

## 5. Closed M4 lifecycle

M4 authority:

```text
docs/architecture/access-auth-m4-contract.md
```

M4 remains fully accepted:

```text
signup → pending challenge only before mailbox proof
valid OTP → Account + verified EmailIdentity + PasswordCredential + AuthSession
existing email revealed only after mailbox proof; no overwrite/fake session
neutral recovery initiation
single-use exact EmailIdentity+Account recovery proof
reset replaces password + revokes ALL AuthSessions + no auto-login
reauth rotates exact bearer on same auth_session_ref
```

Current M4 public API:

```text
POST /api/v1/auth/signup
POST /api/v1/auth/signup/verify
POST /api/v1/auth/signup/resend
POST /api/v1/auth/recovery
POST /api/v1/auth/recovery/validate
POST /api/v1/auth/reset-password
POST /api/v1/auth/reauthenticate
```

---

## 6. M4 accepted engineering evidence

```text
backend static / typing / lint / build        PASS
backend fast                                 87 / 87 PASS
real PostgreSQL marked suite                 87 / 87 PASS
Web Access UI                                22 / 22 PASS
real Auth full-stack browser                 33 / 33 PASS
Chromium                                     11 / 11 PASS
Firefox                                      11 / 11 PASS
WebKit                                       11 / 11 PASS
manual integrated M4 UAT                     PASS / USER ACCEPTED
```

Manual UAT accepted:

```text
login/session/logout
new signup → OTP → Account/AuthSession → setup handoff
recovery → reset → fresh replacement-password signin
existing-account signup → OTP → safe existing_account result
```

No additional M4 QA cycle is required absent direct regression evidence.

---

## 7. M5.1 freeze — COMPLETE

Authority:

```text
docs/architecture/access-auth-m5-contract.md
```

Continuation record:

```text
docs/workstreams/access-auth-m5-live-handoff-2026-08-29.md
```

M5.1 completed:

```text
current Google Identity Services / OIDC readback
current Sign in with Apple Web/REST/lifecycle readback
current WebAuthn Level 3 / passkey readback
mature-product benchmark sweep
reconciliation with DANTE M2–M4 + CP6
multi-authenticator architecture/security freeze
```

Frozen M5 capability envelope:

```text
Google authentication
Sign in with Apple
ExternalIdentity = issuer + subject
explicit Account linking only
provider-enriched first-account bootstrap
provider provenance + no later overwrite
Apple one-shot name preservation
Apple Hide My Email / relay lifecycle
Apple grant/revocation/server-notification lifecycle
passkeys/WebAuthn 0..N
opaque WebAuthn user handle
passwordless Account
add-password capability
safe authenticator removal / anti-lockout
lost-passkey/passwordless email recovery posture
Auth vs Gmail/Calendar/iCloud authorization isolation
future Home → Security/Access management readiness
```

Provider profile data is bootstrap, not permanent sync. Google/Apple profile data does not become Account identity and no DANTE username is invented from provider data.

---

## 8. Exact next work — M5.2

```text
M5.2 — exact persistence + API design
NEXT / NOT STARTED
```

Before production code, M5.2 must close:

```text
exact ExternalIdentity persistence
provider signin/link transaction state
pending provider enrollment when DANTE mailbox proof is required
Apple encrypted grant/token lifecycle state
Apple notification idempotency requirements
opaque WebAuthn Account user handle
PasskeyCredential exact columns/constraints
WebAuthn challenge persistence
one-shot provider profile-bootstrap staging or existing canonical owner
M4 recovery create-or-replace PasswordCredential adaptation
exact API paths / operationIds / machine problems
provider callback/redirect topology
WebAuthn RP/origin topology
dependency qualification
proof-layer matrix
```

M5.2 must apply CP6:

```text
purpose
→ Dictionary design
→ exact PostgreSQL constraints/indexes/ACL
→ SQLAlchemy
→ Alembic
→ real PostgreSQL proof
```

No M5 schema, code, OpenAPI or Web capability may be described as implemented yet.

---

## 9. M5 testing/deployment findings already frozen

```text
mandatory provider CI = deterministic protocol-faithful local substitutes
real DANTE adapter/security path must still execute
real provider smoke/UAT required before M5 closure
Apple Web production proof needs an Apple-registered HTTPS domain
WebAuthn test harness must use valid RP/domain posture such as https://localhost:<port>, RP ID localhost
Chromium/Firefox/WebKit remain product-critical matrix; do not fake unavailable engine-specific WebAuthn automation
```

Provider/JWK/token/network work stays outside DB transactions. No blind retries of non-idempotent/single-use provider operations.

---

## 10. M5/M7 boundary

M5 correctness includes:

```text
provider/passkey lifecycle
linking
anti-lockout
provider revoke/account-change evidence
security-event capability
correct metadata for later management
```

M7 still owns final whole-vertical capabilities such as:

```text
complete session/device management UI
remote revoke UX
new-login alerts / “this wasn’t me”
final security-event retention where not needed earlier
full production observability
final privacy/legal/accessibility/dependency/release review
whole-vertical acceptance
```

M7 is not permission to leave M5 provider/passkey correctness incomplete.

---

## 11. Branch/worktree safety

Continue exactly unless the user explicitly changes topology:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

No new Access branch/worktree, merge, rebase, history rewrite or protected-main write without explicit user gate.