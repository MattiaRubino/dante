# DANTE — Project Status

- **Status:** CURRENT TRUTH FOR `feature/access-auth`
- **Last reconciled:** 2026-08-29
- **Protected `main`:** integrated source authority; current Access/Auth work remains unmerged until explicit user gate
- **Active product vertical:** Access/Auth
- **Current macro-phase:** M4 — Signup + Verification + Recovery + Reset + Reauth
- **Current engineering state:** M4 backend/security/database/API materialization advanced; OpenAPI/client/Web + accepted proof remain
- **Implementation checkpoint before current live docs:** `538f29ad9367ab03135644e3cbc9bc5c5c5d5653`
- **M4 live handoff:** `workstreams/access-auth-m4-live-handoff-2026-08-29.md`
- **M4 architecture authority:** `architecture/access-auth-m4-contract.md`
- **Forward execution authority:** `workstreams/access-auth-m4-m7-execution-plan.md`
- **Observability:** full production-credible baseline DEFERRED TO M7; not blocking M4

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

Observability PRE-M4 feasibility
COMPLETE / FULL STACK DEFERRED TO M7

Access/Auth M4 — Signup + Verification + Recovery + Reset + Reauth
ACTIVE / ADVANCED BACKEND-SECURITY MATERIALIZATION / NOT CLOSED

Access/Auth M5
PLANNED

Access/Auth M6
PLANNED

Access/Auth M7
PLANNED / FINAL WHOLE-VERTICAL GATE / OBSERVABILITY MANDATORY

Whole Access/Auth vertical
ACTIVE / NOT CLOSED
```

M3 remains closed unless direct defect evidence justifies a bounded reopen.

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

Current M4 source/catalog target after migration `20260829_11`:

```text
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

Important evidence distinction:

```text
current source/Dictionary/migration target
!= accepted observed PostgreSQL PASS
```

The real M4 PostgreSQL/current-catalog execution is still pending in the accepted closure evidence.

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
provider authentication != provider-data integration authorization
provider email never silently links Accounts
verification != setup completion
reauthentication != initial signin
method != factor != assurance
frontend request/success != backend-authoritative success
unknown/loading != signed-out/signed-in
```

Rejected without a new bounded architecture gate:

```text
JWT/localStorage browser Auth
Redis/JWT session authority
Principal persistence table
silent provider-email Account merge
Account advisory-lock replacement
Axios as alternate Auth boundary
generated React Query hooks as app boundary
wide credentialed CORS
fake frontend Auth success
persisted browser Auth cache
```

---

## 4. M3 frozen production spine

M3 production API:

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

Refresh rule:

```text
hard refresh
→ Router loader resolves authoritative /auth/session
→ Query cache ready
→ AccessPage mounts once
→ first business render already signed-in or signed-out
```

Never reintroduce login-first + effect repair or hidden sign-in geometry placeholders.

M3 evidence remains:

```text
backend fast tests                     73 / 73 PASS
real PostgreSQL marked suite           83 / 83 PASS
real Auth API integration               4 / 4 PASS
Web unit                               25 / 25 PASS
TypeScript / ESLint / architecture     PASS
generated drift / build / formatting   PASS
browser full-stack                     21 / 21 PASS
Chromium / Firefox / WebKit             7 / 7 each
manual refresh/UAT                     ACCEPTED
```

---

## 5. M4 frozen lifecycle architecture

Authority:

```text
docs/architecture/access-auth-m4-contract.md
```

M4 is one coherent lifecycle macro-batch.

Signup:

```text
email + password
→ PasswordSignupChallenge only
→ six-digit CSPRNG email OTP
→ no canonical Account before mailbox proof

valid OTP
→ Account(active)
→ verified EmailIdentity
→ PasswordCredential
→ AuthSession
→ durable commit/reconciliation
→ only then browser session cookie
```

Recovery:

```text
known/unknown public semantics neutral
256-bit high-entropy raw bearer
single current challenge per Account
proof bound to exact EmailIdentity + Account
new issue supersedes old
raw proof never persisted/logged
```

Reset:

```text
HIBP + Argon2 outside transaction
→ Account security lock
→ exact state/proof revalidation
→ single-use challenge consume
→ password replacement
→ revoke ALL AuthSessions
→ no auto-login
```

Reauthentication:

```text
POST /api/v1/auth/reauthenticate
current AuthSession + CSRF + fresh password evidence
→ same auth_session_ref
→ exact presented bearer required
→ recent-auth/session-window refresh
→ bearer rotation
→ stale bearer rejected
```

The obsolete `/auth/reauth/password` target is not current.

---

## 6. M4 materialized backend/security state

Already materialized on `feature/access-auth`:

```text
migration 20260829_11
M4 SQLAlchemy mappings
M4 Dictionary evolution
narrow runtime ACL delta
signup/recovery challenge persistence
purpose-separated OTP/recovery cryptography
validated M4 settings
bounded lifecycle rate limiters
signup + OTP verify + resend
existing-account collision protection
neutral recovery initiation
recovery proof validation
single-use password reset
all-session revoke after reset
same-session reauth + exact bearer rotation
bounded SMTP dispatcher
SMTP capture/private E2E control support
M4 FastAPI public API
M4 browser ingress middleware
M4 OpenAPI exporter governance changes
M4 unit/bootstrap/catalog/real-PostgreSQL test code
```

Current public M4 API:

```text
POST /api/v1/auth/signup
POST /api/v1/auth/signup/verify
POST /api/v1/auth/signup/resend
POST /api/v1/auth/recovery
POST /api/v1/auth/recovery/validate
POST /api/v1/auth/reset-password
POST /api/v1/auth/reauthenticate
```

Current operation IDs:

```text
auth_begin_signup
auth_verify_signup
auth_resend_signup_verification
auth_request_password_recovery
auth_validate_password_recovery
auth_reset_password
auth_reauthenticate
```

---

## 7. Important M4 hardening already resolved

Do not undo these during Web/client integration:

```text
OTP verifier is HMAC-SHA256 under a dedicated key and bound to signup_ref
password pepper / OTP key / CSRF key material must be distinct
recovery bearer is 256-bit and purpose-separated
recovery challenge is bound to exact EmailIdentity + Account at PostgreSQL level
reset consumes proof with conditional DELETE ... RETURNING
reauth is conditioned on the exact bearer verifier presented
stale bearer cannot rotate again after concurrent reauth
Argon2/HIBP/network work remains outside DB security transactions
no blanket SERIALIZABLE
no blind mutation retries
runtime ACL remains narrow/column-bounded
```

SMTP boundary:

```text
bounded queue
fixed workers
bounded timeout/shutdown
no network I/O inside DB transaction
no blind retry after ambiguous SMTP acceptance
non-local SMTP requires STARTTLS/TLS
no proof/recipient secret logging
```

---

## 8. M4 proof state

Test code is materialized, including:

```text
apps/backend/tests/test_auth_proofs.py
apps/backend/tests/test_settings.py
apps/backend/tests/test_bootstrap.py
apps/backend/tests/integration/database/test_current_catalog.py
apps/backend/tests/integration/auth/test_m4_lifecycle.py
apps/backend/tests/integration/auth/test_signin_session.py
```

The real-PostgreSQL M4 lifecycle module covers prepared scenarios including:

```text
no Account before mailbox proof
verified account establishment
existing-account credential non-overwrite
recovery supersession
single-use reset
all-session revoke after reset
new password validity
same-session reauth
exact bearer rotation
stale bearer rejection
```

At this checkpoint, **do not claim these new M4 tests PASS unless canonical local execution output is available**.

```text
TEST CODE EXISTS != TEST EXECUTION PASS
```

---

## 9. Immediate remaining work

The next engineering block is no longer architecture design.

```text
1. deterministic OpenAPI regeneration
2. Orval M4 generation
3. governed @dante/api-client M4 runtime parsing
4. strict success/problem/no-store/request-id/status validation
5. Web Auth remote M4 operations
6. TanStack Query mutation lifecycle
7. Access real wiring:
   signup
   verify OTP
   resend
   recovery
   recovery link capture + immediate fragment scrub
   password reset
   reauth
8. focused backend/frontend static + unit QA
9. real PostgreSQL M4 acceptance execution
10. real HTTPS Web/FastAPI/PostgreSQL/SMTP capture matrix
11. Chromium + Firefox + WebKit
12. integrated manual M4 UAT
13. current DB/API/frontend/workstream docs reconciliation
14. explicit user acceptance
```

Generated files and lockfiles are never hand-edited. Use repository generation/formatting commands.

Test strategy remains one macro-batch:

```text
focused proof during coding
→ ONE integrated real PostgreSQL M4 gate
→ ONE integrated cross-browser M4 gate
→ ONE manual integrated M4 UAT
```

---

## 10. Observability

The PRE-M4 feasibility review is complete.

Full Grafana/OpenTelemetry-class observability is **DEFERRED TO M7** because it is a real subsystem, not a small M4 prerequisite.

M4–M6 still require privacy-safe logging and must never emit passwords, cookies/session bearers, CSRF values, OTPs, recovery secrets, OAuth tokens/codes or passkey private material.

M7 may not close Access/Auth without the production-credible observability gate.

---

## 11. Forward roadmap

```text
M4 — Signup + Verification + Recovery + Reset + Reauth
ACTIVE / NOT CLOSED

M5 — Google + Apple + Passkeys + Explicit Linking
PLANNED

M6 — Native Mobile Access
PLANNED

M7 — Security Hardening + Observability + Authenticated Handoff
PLANNED / FINAL WHOLE-VERTICAL GATE
```

Only M7 + explicit final user acceptance may close the whole Access/Auth vertical.

---

## 12. Branch/worktree safety

Continue exactly:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

No new Access branch/worktree. No merge/rebase/history rewrite/main write without explicit user gate.

Detailed continuation checkpoint:

```text
docs/workstreams/access-auth-m4-live-handoff-2026-08-29.md
```
