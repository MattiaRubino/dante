# DANTE Roadmap

- **Status:** CURRENT FOR `feature/access-auth`
- **Last reconciled:** 2026-08-29
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active vertical:** Access/Auth
- **Current macro-phase:** M4 — Signup + Verification + Recovery + Reset + Reauth
- **M4 live handoff:** `workstreams/access-auth-m4-live-handoff-2026-08-29.md`
- **M4 architecture authority:** `architecture/access-auth-m4-contract.md`
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
        CLOSED
          ↓
M2 — Auth Architecture Freeze
        CLOSED
          ↓
M3 — Email/Password Signin + AuthSession Spine
        CLOSED / ENGINEERING PASS / USER ACCEPTED
          ↓
Observability feasibility
        COMPLETE / FULL STACK DEFERRED TO M7
          ↓
M4 — Signup + Verification + Recovery + Reset + Reauth
        ACTIVE / BACKEND-SECURITY MATERIALIZATION ADVANCED
        OPENAPI/CLIENT/WEB + ACCEPTED PROOF REMAIN
          ↓
M5 — Google + Apple + Passkeys + Explicit Linking
        PLANNED
          ↓
M6 — Native Mobile Access
        PLANNED
          ↓
M7 — Security Hardening + Observability + Authenticated Handoff
        PLANNED / FINAL WHOLE-VERTICAL GATE
```

The whole Access/Auth vertical is not closed.

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

M4 source/current-catalog target:

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

M4 adds:

```text
password_signup_challenge
password_recovery_challenge
exact recovery EmailIdentity↔Account integrity binding
narrow runtime ACL evolution for account establishment and reauth
```

These M4 counts are not accepted observed PostgreSQL evidence until the canonical real-DB run passes.

Permanent rule:

```text
Alembic
≈ SQLAlchemy
≈ Database Dictionary
≈ real PostgreSQL catalog
≈ current human DB reference
≈ direct tests
```

---

## 3. M1–M3 frozen foundation

M1–M3 are closed and reused.

Critical permanent rules:

```text
same-origin Web Auth
opaque PostgreSQL-backed AuthSession
Secure HttpOnly __Host-dante-session
CSRF + Origin + Fetch Metadata + X-Dante-Client
runtime-only Principal
multiple independent AuthSessions
Argon2id + HIBP + purpose-separated pepper
/api/v1 + RFC9457
READ COMMITTED + targeted Account serialization
no blind mutation retry
FastAPI → deterministic OpenAPI → Orval Fetch → governed @dante/api-client
TanStack Query remote lifecycle
Router-first critical session bootstrap
real PostgreSQL + real Chromium/Firefox/WebKit proof
```

M3 regression guard:

```text
unknown/loading != signed-out
route resolves authoritative session before Access business render
no login-first + useEffect repair
no hidden sign-in geometry placeholder
no persisted browser Auth cache
no fake frontend Auth success
```

---

# 4. M4 — Signup + Verification + Recovery + Reset + Reauth

**Status:** `ACTIVE / BACKEND-SECURITY-DATABASE-API ADVANCED / NOT CLOSED`

Implementation checkpoint before current live docs:

```text
538f29ad9367ab03135644e3cbc9bc5c5c5d5653
```

Detailed current state:

```text
docs/workstreams/access-auth-m4-live-handoff-2026-08-29.md
```

## 4.1 Frozen signup semantics

```text
email + password
→ pending PasswordSignupChallenge only
→ NO Account yet

six-digit email OTP valid
→ Account(active)
→ verified EmailIdentity
→ PasswordCredential
→ AuthSession
→ durable commit/reconciliation
→ cookie
```

Existing canonical email after mailbox proof returns an explicit non-destructive `existing_account` outcome. It never overwrites the existing credential.

OTP posture:

```text
6 digits
CSPRNG
HMAC-SHA256 verifier
purpose-separated rotatable key
verifier bound to signup_ref
15-minute baseline OTP lifetime
max 5 failed attempts
resend rotates/invalidate prior OTP
```

## 4.2 Recovery/reset semantics

```text
known/unknown public recovery semantics neutral
256-bit high-entropy raw bearer
single current recovery challenge per Account
proof bound to exact EmailIdentity + Account
new issuance supersedes prior proof
raw secret never persisted/logged
```

Reset:

```text
HIBP + Argon2 outside transaction
→ Account security lock
→ exact proof/identity/credential revalidation
→ conditional single-use proof consume
→ replace PasswordCredential
→ revoke ALL AuthSessions
→ commit/reconcile ambiguity
→ NO auto-login
→ fresh signin required
```

## 4.3 Reauthentication

Canonical API:

```text
POST /api/v1/auth/reauthenticate
operationId: auth_reauthenticate
```

Semantics:

```text
current AuthSession + session-bound CSRF + fresh password
→ same auth_session_ref
→ exact presented bearer verifier required
→ refresh recent-auth/session window
→ rotate session bearer
→ stale bearer rejected
```

Do not reintroduce `/auth/reauth/password`.

## 4.4 M4 public API now materialized

```text
POST /api/v1/auth/signup
POST /api/v1/auth/signup/verify
POST /api/v1/auth/signup/resend
POST /api/v1/auth/recovery
POST /api/v1/auth/recovery/validate
POST /api/v1/auth/reset-password
POST /api/v1/auth/reauthenticate
```

Browser security middleware protects all M4 JSON POSTs pre-body with exact same-origin policy. Reauth additionally requires admitted session + CSRF.

## 4.5 Email boundary now materialized

```text
AuthLifecycleService
→ EmailDeliveryPort
→ bounded SmtpEmailDispatcher
→ SMTP
```

Rules:

```text
bounded queue/workers/timeouts/shutdown
no network I/O inside DB transaction
no unbounded background tasks
no blind SMTP retry after ambiguous acceptance
non-local SMTP requires STARTTLS/TLS
no proof/recipient secrets in logs
```

Protocol-faithful local SMTP capture and private E2E control support are also materialized; no public `/test/*` FastAPI endpoint.

## 4.6 Tests written, acceptance run still required

Prepared test coverage includes:

```text
crypto/proof unit tests
settings/bootstrap tests
current-catalog/ACL tests
real-PostgreSQL M4 lifecycle test module
M3 signin/session regression adjustments
```

Prepared real-PostgreSQL lifecycle scenarios include:

```text
no Account before OTP proof
verified account establishment
existing-account non-overwrite
recovery supersession
single-use reset
all-session revoke after reset
replacement password validity
same-session reauth
exact bearer rotation
stale bearer rejection
```

Binding rule:

```text
TEST CODE EXISTS != TEST EXECUTION PASS
```

Do not mark the M4 PostgreSQL matrix green until the canonical local output exists.

## 4.7 Immediate M4 remaining work

```text
1. deterministic OpenAPI regeneration
2. Orval M4 generation
3. governed @dante/api-client M4 runtime extension
4. strict success/problem/no-store/request-id/status parsing
5. Web Auth remote M4 operations
6. TanStack Query lifecycle wiring
7. Access real signup/verify/resend/recovery/reset/reauth wiring
8. memory-only recovery secret capture + immediate URL-fragment scrub
9. focused Python/TypeScript/static/unit QA
10. real PostgreSQL M4 acceptance execution
11. integrated HTTPS Web/FastAPI/PostgreSQL/SMTP capture harness
12. Chromium + Firefox + WebKit matrix
13. manual integrated M4 UAT
14. final DB/API/frontend/workstream docs reconciliation
15. explicit user M4 acceptance
```

Generated artifacts/lockfiles are not hand-edited.

## 4.8 M4 test strategy

M4 remains one macro-batch.

```text
focused tests during coding
→ ONE integrated real PostgreSQL M4 gate
→ ONE integrated cross-browser M4 gate
→ ONE manual integrated M4 UAT
```

Do not repeat the heavy gate for each small lifecycle subfeature unless direct critical security evidence requires it.

M4 closes only when:

```text
technical/security review PASS
DB representations aligned
OpenAPI/generated client aligned
Web real integration complete
real PostgreSQL proof PASS
Chromium/Firefox/WebKit proof PASS
manual UAT PASS
current docs reconciled
user explicitly accepts M4
```

---

# 5. M5 — Google + Apple + Passkeys + Explicit Linking

**Status:** `PLANNED / AFTER M4`

Before implementation, re-read current official Google, Apple and WebAuthn/FIDO specifications.

Permanent rules:

```text
ExternalIdentity = issuer + subject
provider email != Account merge key
provider login != Gmail/Calendar/iCloud data authorization
provider token != DANTE AuthSession
linking requires explicit proof/consent
DANTE AuthSession remains canonical
```

M5 must prove provider replay/cancel/outage/key rotation/linking collisions and passkey RP/origin/challenge/lost-device/passwordless semantics.

---

# 6. M6 — Native Mobile Access

**Status:** `PLANNED / AFTER M5 UNLESS EXPLICITLY RE-GATED`

Use the same canonical Account/AuthSession backend with native-appropriate transport/storage.

Close native-specific:

```text
secure session credential representation
SecureStore / Keychain / Keystore
app restart/background lifecycle
logout/revoke
multi-device behavior
deep links
provider callbacks
passkeys
uninstall/reinstall semantics
real emulator/device proof
```

Native is not scaled Web.

---

# 7. M7 — Security Hardening + Observability + Authenticated Handoff

**Status:** `PLANNED / FINAL ACCESS-AUTH GATE`

M7 owns:

```text
whole-vertical threat/abuse/replay review
session/account management required by product
provider/linking/WebAuthn/native hardening
FULL production-credible observability
privacy/legal/accessibility/dependency/release review
real authenticated handoff into next DANTE vertical
whole-vertical manual UAT
```

Observability is mandatory here if still deferred:

```text
privacy-safe structured logs
request/trace correlation
metrics/traces
collector/backend topology
useful dashboards/queries
redaction proof
telemetry outage must not break Auth correctness
```

Only M7 + explicit final user acceptance may close the whole Access/Auth vertical.

---

## 8. Branch/worktree rule

Continue exactly:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

No new branch/worktree, merge/rebase/force-push/history rewrite or protected-main write without explicit user gate.
