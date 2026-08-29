# DANTE — Access/Auth M4 Live Handoff — 2026-08-29

- **Status:** CURRENT LIVE HANDOFF / M4 ACTIVE / NOT CLOSED
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Implementation checkpoint before this handoff:** `538f29ad9367ab03135644e3cbc9bc5c5c5d5653`
- **Checkpoint commit message:** `test(auth): prove M4 lifecycle on real PostgreSQL`
- **Last closed macro-phase:** M3 — Email/Password Signin + AuthSession Spine — CLOSED / ENGINEERING PASS / USER ACCEPTED
- **Current macro-phase:** M4 — Signup + Verification + Recovery + Reset + Reauth
- **Current M4 state:** backend/security/database/API materialization advanced; OpenAPI/client/Web integration and accepted proof remain
- **Observability:** full Grafana/OpenTelemetry-class baseline DEFERRED TO M7; do not block M4

> This file is the live continuation checkpoint for a new chat. Repository truth beats conversation memory. M4 is **not** closed merely because substantial backend code and test code exist.

---

## 1. Mandatory continuation boundary

Continue exactly here unless the user explicitly changes topology:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do **not**:

```text
create a new feature/access-* branch
create another Access/Auth worktree
merge/rebase against main
force-push / rewrite history
write to protected main
move work into /home/mattia/projects/dante-frontend
```

The separate `/home/mattia/projects/dante-frontend` worktree is independent Home/frontend territory.

If Docker is needed for proof, tell the user **Docker deve essere acceso** before asking them to run the proof.

---

## 2. Read order for the next chat

Read in this order before modifying code:

1. `docs/PROJECT-STATUS.md`
2. `docs/ROADMAP.md`
3. `docs/workstreams/access-auth.md`
4. **this file**
5. `docs/workstreams/access-auth-m4-m7-execution-plan.md`
6. `docs/architecture/access-auth-m4-contract.md`
7. `docs/architecture/access-auth-architecture.md`
8. `docs/architecture/access-auth-security-contract.md`
9. `docs/architecture/access-auth-api-contract.md`
10. `docs/architecture/access-auth-testing-contract.md`
11. `docs/decisions/ADR-011-access-auth-architecture.md`
12. `docs/database/README.md`
13. `docs/database/access-auth.md`
14. M4 Dictionary entries and migration `20260829_11`
15. `docs/frontend/access.md`
16. `docs/development/agent-operating-manual.md`

Do not reinterpret M1–M3 from scratch.

---

## 3. Frozen foundations that M4 must preserve

M1–M3 are closed. M4 builds on them; it does not replace them.

Permanent invariants:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential is optional
Account may become passwordless in later phases
Principal remains runtime-derived
multiple independent AuthSessions are normal
frontend request/success != backend-authoritative success
unknown/loading != signed-out/signed-in
provider email never silently links Accounts
method != factor != assurance
```

Do not reopen without direct defect evidence and a bounded explicit gate:

```text
JWT/localStorage browser Auth
Redis/JWT as browser session authority
Principal persistence table
silent provider-email Account merge
Account advisory-lock replacement
wide credentialed CORS
Axios as alternate Auth boundary
generated React Query hooks as application boundary
fake frontend Auth success
persisted browser Auth cache
login-first then useEffect repair
hidden sign-in geometry placeholder
route deep-import of Access internals
```

M3 Router-first bootstrap remains canonical:

```text
hard load
→ Router loader resolves/prefetches /auth/session
→ Query cache ready
→ AccessPage mounts
→ first business render is authoritative
```

---

## 4. M4 architecture already frozen

Authority:

```text
docs/architecture/access-auth-m4-contract.md
```

M4 is intentionally one coherent lifecycle macro-batch, not six separately closed mini-projects.

Standard signup:

```text
email
→ password
→ six-digit email OTP
→ only after valid mailbox proof:
   Account
   + verified EmailIdentity
   + PasswordCredential
   + AuthSession
```

Anonymous email/password submission creates only `PasswordSignupChallenge`; it does not create canonical Account state.

Purpose-specific persistence only:

```text
password_signup_challenge
password_recovery_challenge
```

No generic `auth_token(type,payload)` / proof god-table.

Recovery/reset:

```text
neutral recovery initiation
→ high-entropy out-of-band recovery proof
→ single-use / superseding challenge
→ password replacement under Account security serialization
→ revoke ALL AuthSessions
→ no auto-login
→ fresh normal signin required
```

Reauthentication:

```text
same AuthSession
+ fresh password evidence
→ refresh recent_auth_at / session window
→ rotate exact presented bearer secret
→ preserve auth_session_ref identity
```

Canonical endpoint is **`POST /api/v1/auth/reauthenticate`**, not `/auth/reauth/password`.

---

## 5. Current source/database materialization

Current M4 migration:

```text
apps/backend/migrations/versions/20260829_11_m4_auth_lifecycle_challenges.py
revision:     20260829_11
down_revision: 20260827_10
```

Current branch source target after migration 11:

```text
PostgreSQL major family   18.6
Alembic head candidate    20260829_11
74 tables
5 views
15 routines
75 triggers
113 physical indexes
72 foreign keys
149 CHECK constraints
94 standalone Dictionary entries
```

These counts are the expected current representation after the M4 delta. They must still be confirmed by the real PostgreSQL/current-catalog acceptance run before M4 closure.

M4 DB delta:

```text
+ dante.password_signup_challenge
+ dante.password_recovery_challenge
+ uq_email_identity_email_identity_ref_account_ref
+ narrow M4 runtime ACL evolution on Account / EmailIdentity /
  PasswordCredential / AuthSession
```

Security reason for composite EmailIdentity binding:

```text
password_recovery_challenge(email_identity_ref, account_ref)
→ must reference the exact EmailIdentity owned by the exact Account
```

This protects future multi-email Accounts and prevents recovery-channel/account cross-binding even if application code is wrong.

Least privilege remains deliberate:

```text
Account / EmailIdentity / PasswordCredential
→ column-bounded INSERT only where account establishment requires it

AuthSession
→ only the narrow reauth/session-secret columns required

challenge tables
→ exact operational SELECT/INSERT/UPDATE/DELETE capability
```

Never widen Auth tables to broad UPDATE/DELETE for convenience.

Database reconciliation invariant remains:

```text
Dictionary
≈ SQLAlchemy
≈ Alembic
≈ PostgreSQL catalog
≈ human DB reference
≈ direct tests
```

---

## 6. M4 implementation already materialized

### 6.1 Security/config/proofs

Materialized:

```text
apps/backend/src/dante/platform/config/auth.py
apps/backend/src/dante/platform/config/settings.py
apps/backend/src/dante/auth/proofs.py
```

Key decisions:

```text
dedicated rotatable signup OTP HMAC key ring
password pepper / OTP key / CSRF key purpose separation
bootstrap rejects secret aliasing across purposes
6-digit OTP generated by CSPRNG
OTP verifier = HMAC-SHA256 domain-separated and bound to signup_ref
raw OTP never persisted
recovery bearer = 32 random bytes / 256 bits
canonical Base64URL
recovery verifier domain-separated
raw recovery secret never persisted
recent-auth default candidate = 10 minutes, server-authoritative
non-local SMTP plain transport rejected
```

### 6.2 Lifecycle service

Materialized:

```text
apps/backend/src/dante/auth/lifecycle.py
apps/backend/src/dante/auth/lifecycle_runtime.py
apps/backend/src/dante/auth/contracts.py
```

Implemented lifecycle semantics include:

```text
pending signup creation
OTP resend/cooldown/attempt limits
mailbox verification
atomic Account + verified EmailIdentity + PasswordCredential + AuthSession establishment
existing-account collision outcome without credential overwrite
neutral password recovery initiation
recovery supersession
non-consuming recovery validation
single-use password reset
all-session revocation after reset
password reauthentication
exact bearer rotation on same AuthSession
bounded process-local lifecycle rate limiters
ambiguous-commit reconciliation paths where explicitly designed
bounded expired-challenge cleanup
```

Important hardening already added:

```text
recovery proof bound to exact EmailIdentity + Account
reset consumes proof with conditional DELETE ... RETURNING
reauth mutation is conditioned on the exact bearer verifier presented
stale bearer cannot rotate again after concurrent reauth
credential/email/session state is revalidated under Account lock where required
Argon2/HIBP/network work stays outside security DB transactions
no blanket SERIALIZABLE
no blind mutation retry
```

M4 reuses M3 process resources rather than duplicating them:

```text
same PostgreSQL pool
same PasswordKdf worker resource
same HIBP transport
new lifecycle service
new email dispatcher
```

---

## 7. Email boundary and full-stack capture already materialized

Production/application boundary:

```text
AuthLifecycleService
→ EmailDeliveryPort
→ SmtpEmailDispatcher
→ SMTP
```

Materialized:

```text
apps/backend/src/dante/auth/email_delivery.py
```

Operational rules:

```text
bounded queue
fixed workers
bounded SMTP timeout
no unbounded create_task fan-out
no network I/O inside DB transaction
no blind resend after ambiguous SMTP outcome
clean lifecycle startup/shutdown
shutdown drain bounded by configured timeout
no recipient/proof secrets in failure logs
remote/non-local SMTP requires STARTTLS or TLS
```

Full-stack test support:

```text
tooling/access_auth_smtp_capture.py
tooling/access-auth-e2e-control.py
tooling/serve-access-auth-stack.py
tooling/run-access-auth-stack.py
```

The SMTP capture/control path is test support only. It must not add a public production `/test/*` endpoint to FastAPI.

---

## 8. Public M4 API already materialized

Backend file:

```text
apps/backend/src/dante/auth/api.py
```

Current M4 public surface:

```text
POST /api/v1/auth/signup
  operationId: auth_begin_signup

POST /api/v1/auth/signup/verify
  operationId: auth_verify_signup

POST /api/v1/auth/signup/resend
  operationId: auth_resend_signup_verification

POST /api/v1/auth/recovery
  operationId: auth_request_password_recovery

POST /api/v1/auth/recovery/validate
  operationId: auth_validate_password_recovery

POST /api/v1/auth/reset-password
  operationId: auth_reset_password

POST /api/v1/auth/reauthenticate
  operationId: auth_reauthenticate
```

M3 endpoints remain:

```text
POST   /api/v1/auth/signin
GET    /api/v1/auth/session
DELETE /api/v1/auth/session
```

Public semantics already wired include:

```text
RFC9457 Problem Details
stable machine codes
neutral recovery acknowledgement
explicit existing_account outcome only after mailbox proof
Set-Cookie only after durable/reconciled session success
reset clears browser session cookie defensively
reauth requires current session + session-bound CSRF
reauth rotates the exact presented cookie bearer
Auth responses remain Cache-Control: no-store
server-authoritative X-Request-ID remains binding
```

Browser ingress middleware now covers all M4 JSON POST operations before body parsing:

```text
Origin == canonical Web origin
Sec-Fetch-Site == same-origin
X-Dante-Client == web
Content-Type == application/json
```

Reauth additionally requires the admitted AuthSession + CSRF proof.

---

## 9. OpenAPI governance partially updated, generation still pending

Materialized source governance:

```text
apps/backend/src/dante/bootstrap/openapi_export.py
```

The exporter has been extended conceptually for M4 browser security, response metadata, discriminators, Set-Cookie semantics and Retry-After annotations.

**But the committed deterministic OpenAPI snapshot and generated client are still M3 until canonical generation is executed.**

Do not hand-edit:

```text
packages/api-client/openapi/dante-v1.openapi.json
packages/api-client/src/generated/**
pnpm lockfile
```

Canonical generation path already exists:

```text
pnpm api:generate
```

That performs:

```text
FastAPI deterministic OpenAPI export
→ Orval generation
→ generated formatting
```

The next chat should not manually fabricate generated DTOs/operations.

---

## 10. M4 tests already written vs evidence actually accepted

Materialized tests include:

```text
apps/backend/tests/test_auth_proofs.py
apps/backend/tests/test_settings.py
apps/backend/tests/test_bootstrap.py
apps/backend/tests/integration/database/test_current_catalog.py
apps/backend/tests/integration/auth/test_m4_lifecycle.py
apps/backend/tests/integration/auth/test_signin_session.py
```

`test_m4_lifecycle.py` currently covers real-PostgreSQL scenarios such as:

```text
no canonical Account before valid mailbox proof
successful verified account establishment
existing verified email cannot overwrite credential or create unwanted session
recovery supersession
single-use reset
all-session revocation after reset
new password verifier becomes valid
reauth rotates exact presented bearer
same auth_session_ref survives reauth
stale pre-rotation bearer is rejected
```

Important evidence rule:

```text
TEST CODE EXISTS
!=
TEST EXECUTION PASS
```

At this handoff there is no user-provided canonical local output proving the new M4 PostgreSQL matrix green. Therefore document it as **prepared / pending execution**, not PASS.

M3 evidence remains accepted and must remain regression-safe:

```text
M3 real PostgreSQL     83 / 83 PASS
M3 browser matrix      21 / 21 PASS
M3 manual UAT          ACCEPTED
```

---

## 11. What is NOT finished yet

M4 is **not closed**.

The remaining integrated work is:

```text
1. canonical deterministic OpenAPI regeneration
2. Orval-generated M4 operations/models/Zod
3. governed @dante/api-client runtime extension for all M4 response shapes
4. governed runtime strict parsing / response metadata checks
5. WebAuthRemote extension for M4 operations
6. TanStack Query mutation/query lifecycle wiring where appropriate
7. Access feature real wiring:
   - signup
   - OTP verify
   - resend
   - recovery initiation
   - recovery-link capture/cleanup
   - recovery proof validation
   - password reset
   - reauth
8. preserve Router-first M3 bootstrap with zero flash/bounce regression
9. focused static/unit/integration QA
10. real PostgreSQL M4 acceptance run
11. integrated HTTPS full-stack SMTP-backed browser matrix
12. Chromium + Firefox + WebKit
13. manual integrated M4 UAT
14. current DB/frontend/API/workstream documentation reconciliation
15. explicit user M4 acceptance
```

Only then:

```text
ENGINEERING GATE PASS
+ USER ACCEPTANCE
= M4 CLOSED
```

---

## 12. Immediate continuation sequence

Do not start another architecture brainstorm. The heavy architecture is already frozen and the backend/security core is materialized.

Continue in this order:

```text
A. READBACK / STATIC CONSISTENCY
   → current HEAD
   → M4 migration/mappings/Dictionary/API/OpenAPI exporter
   → ensure no stale /reauth/password naming remains in current docs/code

B. CANONICAL GENERATION
   → run pnpm api:generate in the canonical local environment when needed
   → inspect generated diff, never hand-edit generated output
   → generated:check

C. GOVERNED API CLIENT
   → extend framework-neutral DanteApiClient
   → strict parsing for SignupCreated / SignupVerification discriminator /
     RecoveryAccepted / RecoveryValidation / 204 reset / reauth session
   → retain no-store/request-id/problem/status contract enforcement
   → no generated React Query hooks as app boundary

D. WEB PLATFORM + ACCESS FEATURE
   → Web remote owns credentials/include, X-Dante-Client, CSRF, AbortSignal
   → feature consumes platform boundary, not generated internals
   → mutation retry false
   → no Auth cache persistence
   → authoritative transitions only after backend result
   → recovery secret memory-only; capture URL fragment once and scrub it
   → no localStorage/sessionStorage for recovery bearer

E. FOCUSED QA
   → Python Ruff / typing / unit
   → TS type/lint/architecture/unit
   → OpenAPI/generated drift
   → build/format

F. ONE HEAVY M4 GATE
   → real PostgreSQL current-catalog + lifecycle matrix
   → real HTTPS Web + FastAPI + PostgreSQL + SMTP capture
   → Chromium / Firefox / WebKit integrated M4 scenarios

G. MANUAL UAT + DOCS
   → integrated human flow
   → no refresh regression
   → closure documentation
   → explicit user acceptance
```

Do not make the user run repeated heavy gates after every small subfeature. Keep focused proof during implementation and one integrated heavy closure gate, except where a critical security race requires earlier direct proof.

---

## 13. Required browser/full-stack M4 closure scenarios

At minimum the final integrated browser matrix should prove:

```text
signup → captured real SMTP OTP → verify → authenticated
no canonical Account before verification
resend → old OTP invalid / new OTP valid
existing-account signup after mailbox proof → explicit non-destructive outcome
recovery known Account → real captured link
recovery unknown/ineligible Account → externally neutral behavior
recovery link fragment captured and scrubbed from URL/history-visible state
reset → no auto-login
reset → all old sessions invalid
fresh signin with replacement password
old password rejected
reauth → same auth_session_ref
reauth → cookie/session bearer rotated
pre-rotation bearer cannot be reused
wrong reauth password safe failure
PostgreSQL outage never fake-successes
SMTP/capture/dependency degradation never creates false success where delivery admission is required
M3 signin/logout/session bootstrap regression remains green
```

Low-level concurrency/replay is primarily proven in PostgreSQL/service tests and does not need redundant implementation in every browser engine.

---

## 14. Security/performance rules the next chat must not lose

```text
Argon2/HIBP outside DB transaction
bounded KDF admission
bounded lifecycle rate limiters
bounded SMTP queue/workers/timeouts/shutdown
short READ COMMITTED transactions
Account lock only for Account-wide security mutation
PostgreSQL uniqueness as canonical race arbiter
no blanket SERIALIZABLE
no email/network wait under DB lock
no blind mutation retry
no raw request bodies in logs
no password/session/CSRF/OTP/recovery secret in logs
no email/proof secret metric labels
no public production test endpoints
```

Recovery secret URL policy:

```text
non-secret password_recovery_ref may be query/route context
raw high-entropy secret stays in URL fragment on entry
client captures once
client removes fragment immediately
secret remains memory-only
no third-party analytics/resources on sensitive reset surface
```

---

## 15. Observability remains deferred

Do not stop M4 to build Grafana/Alloy/Loki/Tempo.

Current decision:

```text
full operational observability
→ M7 mandatory gate
```

M4–M6 still require privacy-safe logs and no secret leakage.

---

## 16. M5–M7 remain after M4

```text
M5 — Google + Apple + Passkeys + Explicit Linking
M6 — Native Mobile Access
M7 — Security Hardening + Observability + Authenticated Handoff + Whole-Vertical Closure
```

Do not close the whole Access/Auth vertical at M4.

---

## 17. Current verdict

```text
M1  CLOSED
M2  CLOSED
M3  CLOSED / ENGINEERING PASS / USER ACCEPTED
M4  ACTIVE / ADVANCED BACKEND-SECURITY MATERIALIZATION / NOT CLOSED
M5  PLANNED
M6  PLANNED
M7  PLANNED / FINAL WHOLE-VERTICAL GATE
```

Immediate engineering focus:

```text
OpenAPI generation
→ governed @dante/api-client M4
→ Web Access real wiring
→ focused QA
→ one integrated PostgreSQL + cross-browser M4 gate
→ manual UAT
→ M4 closure docs + explicit user acceptance
```
