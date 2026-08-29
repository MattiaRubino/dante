# DANTE — Access/Auth Full-Stack Vertical Workstream

- **Status:** ACTIVE VERTICAL / M1–M3 CLOSED / M4 ACTIVE
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Created from protected `main`:** `f011e252b6a294a12c38927ef2d528244ea1fee6`
- **M3 status:** CLOSED / ENGINEERING PASS / USER ACCEPTED
- **M4 implementation checkpoint before current handoff:** `538f29ad9367ab03135644e3cbc9bc5c5c5d5653`
- **M4 live handoff:** `access-auth-m4-live-handoff-2026-08-29.md`
- **M4 architecture authority:** `../architecture/access-auth-m4-contract.md`
- **M4–M7 forward plan:** `access-auth-m4-m7-execution-plan.md`
- **Observability:** full Grafana/OpenTelemetry-class baseline DEFERRED TO M7; not blocking M4

> A new chat is not a new project, branch or worktree. Continue this vertical on `feature/access-auth` and `/home/mattia/projects/dante` until whole Access/Auth closure or an explicit user topology gate.

---

## 1. Mandatory continuation bootstrap

Continue exactly:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

The separate `/home/mattia/projects/dante-frontend` worktree is independent Home/frontend territory.

Read first:

1. `docs/PROJECT-STATUS.md`
2. `docs/ROADMAP.md`
3. this file
4. `docs/workstreams/access-auth-m4-live-handoff-2026-08-29.md`
5. `docs/workstreams/access-auth-m4-m7-execution-plan.md`
6. `docs/architecture/access-auth-m4-contract.md`
7. M2 architecture/security/API/testing contracts + ADR-011
8. DB System of Record + `docs/database/access-auth.md` + Dictionary
9. `docs/frontend/access.md`
10. `docs/development/agent-operating-manual.md`

Repository truth beats conversation memory.

No new branch/worktree, merge, rebase, force-push/history rewrite or write to protected `main` without explicit user authorization.

If Docker is required, tell the user **Docker deve essere acceso** before asking for the proof.

---

## 2. Frozen semantic/Auth constitution

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived
multiple independent AuthSessions normal
provider email never silently links Accounts
verification != setup completion
reauthentication != initial signin
frontend request/success != backend-authoritative success
unknown/loading != signed-out/signed-in
method != factor != assurance
```

Do not reopen without a bounded explicit gate:

```text
JWT/localStorage browser Auth
Redis/JWT session authority
Principal table
silent provider-email merge
Account advisory-lock replacement
Axios
generated React Query hooks as application boundary
wide credentialed CORS
fake frontend Auth success
persisted browser Auth cache
login-first then useEffect repair
hidden sign-in geometry placeholder
route deep-import of Access internals
```

---

## 3. Closed phases

```text
M1 — Access Visual/UX Freeze
CLOSED / ACCEPTED

M2 — Auth Architecture Freeze
CLOSED / M2.1–M2.11 ACCEPTED / QA PASS

M3 — Email/Password Signin + AuthSession Spine
CLOSED / ENGINEERING PASS / USER ACCEPTED
```

M3 accepted evidence remains:

```text
backend fast tests                     73 / 73 PASS
real PostgreSQL marked suite           83 / 83 PASS
real Auth integration                   4 / 4 PASS
Web unit                               25 / 25 PASS
TypeScript / ESLint / architecture     PASS
generated drift / build / formatting   PASS
browser full-stack                     21 / 21 PASS
Chromium / Firefox / WebKit             7 / 7 each
manual refresh/UAT                     ACCEPTED
```

M3 Router-first bootstrap is a permanent regression guard:

```text
hard refresh
→ route loader resolves /auth/session
→ Query cache ready
→ AccessPage mounts once
→ first business render already authoritative
```

---

## 4. M4 current state

**M4 is ACTIVE and materially implemented, but NOT CLOSED.**

Current implementation checkpoint before the live-handoff docs:

```text
538f29ad9367ab03135644e3cbc9bc5c5c5d5653
test(auth): prove M4 lifecycle on real PostgreSQL
```

Current M4 backend/security materialization includes:

```text
migration 20260829_11
SQLAlchemy mappings
Dictionary evolution
narrow runtime ACL delta
PasswordSignupChallenge
PasswordRecoveryChallenge
signup OTP crypto
recovery proof crypto
signup/account establishment
verification
resend
recovery initiation/validation
password reset
all-session revocation after reset
reauthentication with exact bearer rotation
bounded lifecycle rate limiting
bounded SMTP dispatcher
SMTP capture test support
M4 public FastAPI API
M4 browser ingress security
M4 OpenAPI exporter governance changes
M4 unit/bootstrap/catalog/lifecycle test code
```

The new test code is **prepared evidence**, not accepted PASS until the canonical local run output exists.

---

## 5. Current M4 database source target

Migration:

```text
20260829_11_m4_auth_lifecycle_challenges.py
```

Expected source/current-catalog target after migration 11:

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

M4 delta:

```text
+ dante.password_signup_challenge
+ dante.password_recovery_challenge
+ exact composite EmailIdentity/Account recovery binding
+ narrow Account/EmailIdentity/PasswordCredential INSERT grants
+ narrow AuthSession reauth update grants
```

Permanent invariant:

```text
Dictionary
≈ SQLAlchemy
≈ Alembic
≈ real PostgreSQL catalog
≈ human DB reference
≈ direct tests
```

Do not claim the numbers as observed PostgreSQL PASS until the real marked/current-catalog run confirms them.

---

## 6. M4 frozen lifecycle design

Signup:

```text
email + password
→ pending PasswordSignupChallenge only
→ six-digit CSPRNG OTP
→ HMAC-SHA256 verifier under dedicated purpose key
→ no canonical Account before mailbox proof

valid OTP
→ Account(active)
→ verified EmailIdentity
→ PasswordCredential
→ AuthSession
→ delete sibling pending challenges for canonical email
→ commit / bounded ambiguity reconciliation
→ only then issue cookie
```

Existing canonical email after mailbox proof returns explicit `existing_account` and never overwrites the existing credential.

Recovery:

```text
public known/unknown semantics neutral
256-bit raw bearer
single current challenge per Account
proof bound to exact EmailIdentity + Account
new issue supersedes old
30-minute baseline lifetime
raw secret never persisted/logged
```

Reset:

```text
HIBP + Argon2 outside transaction
→ Account security lock
→ exact credential/email/proof revalidation
→ conditional single-use consume
→ replace password
→ revoke ALL AuthSessions
→ commit/reconcile
→ no auto-login
→ fresh signin required
```

Reauth:

```text
POST /api/v1/auth/reauthenticate
valid AuthSession + CSRF + fresh password
→ same auth_session_ref
→ exact presented bearer verifier required
→ refresh recent_auth_at/session window
→ rotate session secret
→ stale bearer cannot rotate again
```

---

## 7. Current public API

M3:

```text
POST   /api/v1/auth/signin
GET    /api/v1/auth/session
DELETE /api/v1/auth/session
```

M4 materialized:

```text
POST /api/v1/auth/signup
POST /api/v1/auth/signup/verify
POST /api/v1/auth/signup/resend
POST /api/v1/auth/recovery
POST /api/v1/auth/recovery/validate
POST /api/v1/auth/reset-password
POST /api/v1/auth/reauthenticate
```

Canonical operation IDs:

```text
auth_begin_signup
auth_verify_signup
auth_resend_signup_verification
auth_request_password_recovery
auth_validate_password_recovery
auth_reset_password
auth_reauthenticate
```

Do not reintroduce the obsolete `/auth/reauth/password` wording.

All M4 JSON POSTs preserve fail-closed same-origin browser ingress before body parsing. Reauth additionally requires current session + session-bound CSRF.

---

## 8. Email/runtime posture

```text
AuthLifecycleService
→ EmailDeliveryPort
→ bounded SmtpEmailDispatcher
→ SMTP
```

Rules:

```text
bounded queue
fixed workers
bounded SMTP timeout
bounded shutdown drain
no network I/O in DB transaction
no unbounded background tasks
no blind transport retry after ambiguous SMTP acceptance
non-local SMTP must use STARTTLS/TLS
proof/recipient secrets never logged
```

M4 reuses the M3 PostgreSQL pool, PasswordKdf and HIBP transport. It does not create a second Auth stack.

Test SMTP capture/control is private harness support only; no production `/test/*` endpoint.

---

## 9. Immediate remaining M4 work

Do **not** restart architecture design. Continue the integration batch:

```text
1. canonical deterministic OpenAPI regeneration
2. Orval-generated M4 operations/models/Zod
3. governed @dante/api-client M4 runtime parsing
4. strict no-store / request-id / content-type / status / ProblemDetails enforcement
5. Web Auth remote M4 operations
6. TanStack Query mutations/remote lifecycle
7. Access real wiring:
   signup
   verify OTP
   resend
   recovery
   recovery link fragment capture + scrub
   reset
   reauth
8. focused backend/frontend static + unit QA
9. real PostgreSQL M4 matrix execution
10. integrated HTTPS FastAPI/PostgreSQL/SMTP browser harness
11. Chromium + Firefox + WebKit M4 matrix
12. manual integrated M4 UAT
13. DB/API/frontend/workstream docs reconciliation
14. explicit user M4 acceptance
```

Generated files/lockfiles are not hand-edited. Use the repo generator/formatters.

---

## 10. Test strategy

Keep M4 as one macro-batch.

During implementation:

```text
focused unit/service/schema/race tests
static/type/lint/architecture checks
OpenAPI/generated drift checks
```

At closure:

```text
ONE integrated real PostgreSQL M4 gate
+ ONE integrated Chromium/Firefox/WebKit full-stack gate
+ ONE manual integrated M4 UAT
```

Do not make the user rerun expensive end-to-end gates after every small subfeature unless a critical security issue requires an earlier direct proof.

`TEST CODE EXISTS != TEST EXECUTION PASS` remains binding.

---

## 11. Observability decision

Full Grafana/Alloy/Loki/Tempo/Prometheus-class observability is **DEFERRED TO M7**.

Do not stop M4 for it.

M4–M6 still forbid secret leakage in logs and must preserve privacy-safe diagnostics.

---

## 12. Forward roadmap

```text
M4 — Signup + Verification + Recovery + Reset + Reauth
ACTIVE / ADVANCED BACKEND-SECURITY MATERIALIZATION / NOT CLOSED

M5 — Google + Apple + Passkeys + Explicit Linking
PLANNED

M6 — Native Mobile Access
PLANNED

M7 — Security Hardening + Observability + Authenticated Handoff
PLANNED / FINAL WHOLE-VERTICAL GATE
```

Only M7 + final explicit user acceptance may close the whole Access/Auth vertical.

For exact continuation details, use:

```text
docs/workstreams/access-auth-m4-live-handoff-2026-08-29.md
```
