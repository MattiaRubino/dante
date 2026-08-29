# DANTE — Project Status

- **Status:** CURRENT TRUTH FOR `feature/access-auth`
- **Last reconciled:** 2026-08-29
- **Protected `main`:** integrated source authority; current Access/Auth branch work remains unmerged until an explicit merge gate
- **Active product vertical:** Access/Auth on `feature/access-auth`
- **Current macro-phase:** M4 — Signup + Verification + Recovery + Reset + Reauth
- **Current engineering state:** M4 CONTRACT FREEZE ACTIVE / IMPLEMENTATION NEXT
- **Last closed macro-phase:** M3 — Email/Password Signin + AuthSession Spine
- **Observability decision:** full Grafana/OpenTelemetry stack DEFERRED TO M7 after bounded feasibility readback
- **M4 architecture authority:** `architecture/access-auth-m4-contract.md`
- **Forward execution authority:** `workstreams/access-auth-m4-m7-execution-plan.md`

## 1. Executive state

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL
CLOSED / SEMANTICALLY COMPLETE FOR CURRENT SCOPE

LOGICAL MODEL
CLOSED / 57 OF 57 CLASSIFIED
WL-H01..WL-H12 BINDING

PRE-PHYSICAL COHERENCE
CLOSED / FINAL QA PASS

PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED
PostgreSQL 18 major family canonical

ENGINEERING FOUNDATION v0
CLOSED / ACCEPTED

FRONTEND ENGINEERING FOUNDATION
CLOSED / ACCEPTED / INTEGRATED

FRONTEND MATERIALIZATION
CLOSED / ACCEPTED / INTEGRATED

BACKEND CP1–CP6
CLOSED / ACCEPTED / INTEGRATED

ACCESS PRE-BACKEND WEB MATERIALIZATION
CLOSED / ACCEPTED

ACCESS/AUTH M1
CLOSED — Visual / UX Freeze

ACCESS/AUTH M2
CLOSED — Auth Architecture Freeze

ACCESS/AUTH M3
CLOSED — Email/Password Signin + AuthSession Spine
ENGINEERING GATE PASS
USER ACCEPTANCE ACCEPTED

OBSERVABILITY PRE-M4
FEASIBILITY REVIEW COMPLETE
FULL STACK DEFERRED TO M7
NOT BLOCKING M4

ACCESS/AUTH M4
ACTIVE — CONTRACT FREEZE / IMPLEMENTATION NEXT

ACCESS/AUTH M5
PLANNED

ACCESS/AUTH M6
PLANNED

ACCESS/AUTH M7
PLANNED / FINAL WHOLE-VERTICAL GATE
FULL OBSERVABILITY MANDATORY HERE

WHOLE ACCESS/AUTH VERTICAL
ACTIVE / NOT CLOSED
M4–M7 REMAIN
```

M3 closure remains final unless direct defect evidence justifies a bounded reopen.

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

Current `feature/access-auth` after M3:

```text
PostgreSQL          18.6
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

M3 materialized:

```text
dante.account
dante.email_identity
dante.password_credential
dante.auth_session
dante.acquire_account_security_lock(uuid)
```

Permanent structural reconciliation invariant:

```text
Database Dictionary
≈ SQLAlchemy mappings
≈ Alembic head
≈ current PostgreSQL catalog
≈ current human DB reference
≈ direct tests
```

Applied historical migrations/evidence are not rewritten to impersonate later state.

---

## 3. Binding semantic/Auth invariants

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
provider authentication != provider-data integration authorization
provider state != canonical DANTE state
verification != setup completion
reauthentication != initial signin
method != factor != assurance
frontend request/success != backend-authoritative success
unknown/loading != signed-out/signed-in
```

Do not reopen without an explicit bounded architecture gate:

```text
JWT/localStorage browser Auth
Redis/JWT session authority
Principal persistence table
silent provider-email Account merge
Account advisory-lock replacement
Axios
generated React Query hooks as app boundary
wide credentialed CORS
fake frontend Auth success
persisted browser Auth cache
```

---

## 4. M3 frozen production spine

Backend:

```text
POST   /api/v1/auth/signin
GET    /api/v1/auth/session
DELETE /api/v1/auth/session
```

Security/runtime:

```text
email normalization/comparison
Argon2id 64 MiB / t=3 / p=4
separate HMAC password pepper
HIBP range screening
bounded KDF admission
unknown-account dummy verification
opaque DB-backed AuthSession
runtime Principal
Secure HttpOnly __Host-dante-session
session-bound CSRF
Origin + Fetch Metadata + X-Dante-Client
RFC9457 problem contract
Account-row security serialization
ambiguous AuthSession commit reconciliation
```

Client/Web chain:

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
→ route loader resolves authoritative /auth/session
→ Query cache ready
→ AccessPage mounts once
→ first business render is already signed-in or signed-out
```

Rejected permanently:

```text
login-first then useEffect repair
hidden sign-in form as bootstrap geometry placeholder
route deep-import into Access application internals
persisted browser Auth cache
```

---

## 5. M3 accepted evidence

```text
backend fast tests                     73 / 73 PASS
real PostgreSQL 18.6 marked suite      83 / 83 PASS
real Auth API integration               4 / 4 PASS
Web unit                               25 / 25 PASS
TypeScript / ESLint / architecture     PASS
generated drift / build / formatting   PASS
browser full-stack                     21 / 21 PASS
Chromium                                7 / 7 PASS
Firefox                                 7 / 7 PASS
WebKit                                  7 / 7 PASS
manual refresh/UAT                     ACCEPTED
```

Browser proof includes signin/logout, delayed session bootstrap, invalid credentials, independent sessions, server-side revoke/expiry, real PostgreSQL outage and real rate limiting.

M3 verdict:

```text
ENGINEERING GATE:      PASS
USER ACCEPTANCE GATE: ACCEPTED
M3:                    CLOSED
```

---

## 6. Observability decision — DEFERRED TO M7

The bounded PRE-M4 feasibility readback is complete.

Observed repository truth:

```text
server-authoritative request_id already exists
unexpected-error logging already correlates request_id
no OpenTelemetry/Prometheus dependency currently exists
local Compose currently contains PostgreSQL, not an observability stack
Grafana + Alloy + Loki + Tempo + metrics would therefore be a real new subsystem
```

Decision:

```text
DO NOT build the full observability stack before M4.
DEFER full operational observability to M7.
```

M4–M6 must still preserve safe logging and must never emit passwords, session/cookie values, CSRF secrets, verification/recovery proofs, OAuth codes/tokens or passkey private material.

M7 may not close the whole Access/Auth vertical until the required production-credible logging/metrics/tracing/dashboard/redaction/degraded-telemetry gate is complete.

---

## 7. M4 current architecture decision

M4 is designed as **one coherent lifecycle macro-batch**, not six mini releases.

Authoritative contract:

```text
docs/architecture/access-auth-m4-contract.md
```

Core decision:

```text
SIGN_UP_EMAIL
→ SIGN_UP_PASSWORD
→ six-digit email OTP
→ ONLY AFTER valid OTP:
   Account + verified EmailIdentity + PasswordCredential + AuthSession
```

Standard signup does **not** create an unverified canonical Account.

Initial email/password submission creates only a purpose-specific ephemeral `PasswordSignupChallenge`. This prevents abandoned/bot signup from polluting canonical Account state and prevents an unverified signup from squatting an email indefinitely.

M4 planned persistence:

```text
password_signup_challenge
password_recovery_challenge
```

No generic `auth_token(type,payload)` / proof god-table.

Recovery/reset:

```text
neutral recovery initiation
→ verified active password Account only receives out-of-band recovery proof
→ 256-bit single-use recovery secret
→ reset replaces password under Account serialization
→ revoke ALL AuthSessions
→ NO auto-login
→ fresh normal signin required
```

Reauthentication:

```text
same AuthSession
+ fresh password evidence
→ update server-side recent_auth_at
→ rotate session bearer secret
→ no second AuthSession
```

Baseline recent-auth window candidate: 10 minutes, configurable and enforced server-side by sensitive operations.

---

## 8. M4 performance/security posture

```text
Argon2/HIBP outside DB transaction
bounded existing KDF admission reused
short READ COMMITTED transactions
PostgreSQL uniqueness = final email race arbiter
Account row lock only for Account-wide security mutation
no blanket SERIALIZABLE
email SMTP/network I/O outside DB transactions
bounded email dispatch queue/workers
no unbounded background tasks
no blind mutation retries
```

Signup OTP:

```text
6 numeric digits because frozen UI already expects it
CSPRNG generation
HMAC-SHA256 verifier under dedicated purpose key
15-minute OTP lifetime
max 5 failed attempts per issued OTP
resend rotates/invalidates prior OTP
```

Pending signup may survive up to 24 hours so a user can request a fresh OTP without repeating password entry; it is ephemeral and deleted on successful account establishment.

Recovery:

```text
32 random bytes / 256-bit bearer secret
single use
30-minute baseline lifetime
new issuance supersedes prior challenge
raw secret never persisted/logged
secret kept out of ordinary query strings
```

---

## 9. M4 email boundary

Email is a platform side effect behind an application port.

Target:

```text
Auth application
→ EmailDeliveryPort
→ bounded process dispatch queue
→ SMTP adapter
→ real provider or protocol-faithful local capture
```

No email network call occurs inside PostgreSQL transactions.

The first adapter is SMTP to avoid binding business logic to one provider API. A later provider-specific HTTP adapter may replace it behind the same port.

A full durable transactional outbox is **not** activated by ceremony. If real deployment evidence shows guaranteed asynchronous delivery is required, activate the already-planned outbox capability under its own trigger.

---

## 10. M4 target HTTP surface

Semantic target, subject to final OpenAPI readback:

```text
POST /api/v1/auth/signup
POST /api/v1/auth/signup/verify
POST /api/v1/auth/signup/resend

POST /api/v1/auth/recovery
POST /api/v1/auth/recovery/validate
POST /api/v1/auth/reset-password

POST /api/v1/auth/reauth/password
```

All browser unsafe calls preserve M3 Origin/Fetch-Metadata/X-Dante-Client/CSRF policy as applicable.

Recovery initiation remains neutral for known vs unknown Account state.

---

## 11. M4 test strategy — one heavy closure gate

Do **not** run six complete acceptance cycles for M4.1–M4.6.

Development-time proof stays focused:

```text
unit/service tests
migration/Dictionary/schema checks
critical DB race/replay tests
formatter/type/lint/generated drift
```

Then one integrated real PostgreSQL M4 matrix proves all lifecycle and concurrency invariants.

Then one integrated Chromium/Firefox/WebKit matrix proves only browser/user semantics, not every low-level DB race in every browser.

Critical browser scenarios:

```text
signup → real captured OTP → verify → authenticated/setup transition
existing-account signup after mailbox proof → non-destructive signin/recovery guidance
resend invalidates old OTP
recovery email link → reset → fresh signin required
old sessions rejected after reset
reauth rotates cookie but preserves AuthSession identity
DB/email/server degradation never fake-successes
M3 refresh/bootstrap regression remains fixed
```

One manual integrated M4 UAT follows automation.

---

## 12. Current branch/worktree safety

Continue exactly:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not create another `feature/access-*` branch/worktree merely because M4 starts. Do not merge/rebase/force-push/history-rewrite or write to protected `main` without explicit user authorization.

The separate `/home/mattia/projects/dante-frontend` worktree remains independent frontend/Home territory.

If Docker is required for proof, state **Docker deve essere acceso** before asking the user to run it.

---

## 13. Forward roadmap

```text
M4 — Signup + Verification + Recovery + Reset + Reauth
ACTIVE

M5 — Google + Apple + Passkeys + Explicit Linking
PLANNED

M6 — Native Mobile Access
PLANNED

M7 — Security Hardening + Observability + Authenticated Handoff + Vertical Closure
PLANNED / FINAL GATE
```

M5 must re-read current official Google/Apple/WebAuthn specifications before implementation. Provider email never silently links Accounts.

M6 uses the same canonical Account/AuthSession backend but native-appropriate secure credential transport/storage; Native is not scaled Web.

M7 owns full observability if still deferred, whole-vertical threat/release/dependency/privacy/accessibility review, real authenticated handoff and final user acceptance.

---

## 14. Immediate next action

Do not reopen M3 and do not implement observability now.

```text
M4 contract readback against M2 security/API/testing authorities
→ materialize exact M4 DB delta
→ implement whole M4 backend/email/API/client/Web batch
→ focused tests during coding
→ one integrated static + PostgreSQL gate
→ one integrated cross-browser gate
→ manual UAT
→ docs closure
```

Read first:

```text
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/access-auth.md
docs/architecture/access-auth-m4-contract.md
docs/architecture/access-auth-architecture.md
docs/architecture/access-auth-security-contract.md
docs/architecture/access-auth-api-contract.md
docs/architecture/access-auth-testing-contract.md
docs/database/access-auth.md
docs/frontend/access.md
```

### Known documentation cleanup note

`docs/database/dante-postgresql-database.md` still contains a small older M3-A/Alembic `20260827_09` wording in its opening reconciliation block. Current DB authority is Alembic `20260827_10`, Dictionary, `docs/database/README.md`, `docs/database/access-auth.md` and real tests. This wording drift does **not** reopen M3; reconcile it safely before the M4 structural DB change is finalized.
