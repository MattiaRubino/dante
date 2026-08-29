# DANTE — Access/Auth Full-Stack Vertical Workstream

- **Status:** ACTIVE VERTICAL / M1–M4 CLOSED / M5 NEXT
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Created from protected `main`:** `f011e252b6a294a12c38927ef2d528244ea1fee6`
- **M3 status:** CLOSED / ENGINEERING PASS / USER ACCEPTED
- **M4 status:** CLOSED / ENGINEERING PASS / USER ACCEPTED
- **M4 final accepted implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **M4 closure handoff:** `access-auth-m4-live-handoff-2026-08-29.md`
- **M4 architecture authority:** `../architecture/access-auth-m4-contract.md`
- **M4–M7 forward plan:** `access-auth-m4-m7-execution-plan.md`
- **Observability:** full Grafana/OpenTelemetry-class baseline DEFERRED TO M7

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
6. relevant current M5 contracts once materialized
7. `docs/architecture/access-auth-architecture.md`
8. `docs/architecture/access-auth-security-contract.md`
9. `docs/architecture/access-auth-api-contract.md`
10. `docs/architecture/access-auth-testing-contract.md`
11. `docs/decisions/ADR-011-access-auth-architecture.md`
12. DB System of Record + `docs/database/access-auth.md` + Dictionary
13. `docs/frontend/access.md`
14. `docs/development/agent-operating-manual.md`

Repository truth beats conversation memory. Do not reinterpret M1–M4 from scratch.

No new branch/worktree, merge, rebase, force-push/history rewrite or protected-main write without explicit user authorization.

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

M4 — Signup + Verification + Recovery + Reset + Reauth
CLOSED / ENGINEERING PASS / USER ACCEPTED
```

M3 Router-first bootstrap remains a permanent regression guard:

```text
hard refresh
→ route loader resolves /auth/session
→ Query cache ready
→ AccessPage mounts once
→ first business render already authoritative
```

M4 adds permanent lifecycle guards:

```text
no canonical Account before mailbox proof
anonymous signup does not reveal account existence
existing-account outcome only after mailbox proof
recovery initiation is neutral
recovery proof is single-use/superseding and exact-identity bound
password reset revokes ALL AuthSessions and never auto-logs-in
reauth rotates the exact bearer on the same auth_session_ref
Web recovery secret is memory-only and URL-fragment scrubbed
```

---

## 4. M4 closed implementation state

Final accepted implementation checkpoint:

```text
c95e3b2ca664725bcacc374cb5ba6ed49409fe2b
fix(auth): reconcile M4 PostgreSQL acceptance
```

M4 materialized one full first-party lifecycle across:

```text
PostgreSQL/Alembic/SQLAlchemy/Dictionary
Auth lifecycle service + security proofs
bounded lifecycle rate limiting
bounded SMTP dispatcher
FastAPI/Pydantic public API
browser ingress security
OpenAPI + generated Orval client
governed @dante/api-client
Web Auth remote
TanStack Query mutation lifecycle
Access state graph and UI wiring
real HTTPS full-stack harness
protocol-faithful SMTP capture
```

Canonical M4 public API:

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

Do not reintroduce obsolete `/auth/reauth/password` naming.

---

## 5. Accepted M4 database state

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

M4 DB delta:

```text
+ dante.password_signup_challenge
+ dante.password_recovery_challenge
+ exact composite EmailIdentity/Account recovery binding
+ narrow Account/EmailIdentity/PasswordCredential establishment grants
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

Least privilege remains deliberate; never widen Auth tables to broad UPDATE/DELETE for convenience.

---

## 6. Closed M4 lifecycle design

Signup:

```text
email + password
→ pending PasswordSignupChallenge only
→ six-digit CSPRNG OTP
→ dedicated purpose-separated HMAC verifier
→ no Account before mailbox proof

valid OTP
→ Account(active)
→ verified EmailIdentity
→ PasswordCredential
→ AuthSession
→ delete sibling pending challenges
→ durable commit/reconciliation
→ cookie only after authoritative success
```

Existing canonical email after mailbox proof returns explicit `existing_account`; it never overwrites the existing credential or creates a signup session.

Recovery/reset:

```text
public known/unknown semantics neutral
256-bit raw bearer
single current challenge per Account
proof bound to exact EmailIdentity + Account
new issue supersedes old
raw proof never persisted/logged
conditional single-use consume
replace credential
revoke ALL AuthSessions
no auto-login
fresh signin required
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

M4 reuses the M3 PostgreSQL pool, PasswordKdf and HIBP transport; it does not create a second Auth stack.

---

## 7. Accepted M4 proof

Canonical accumulated closure evidence:

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
login/session/logout regression
new signup → captured OTP → Account/AuthSession → setup handoff
recovery → captured link → reset → fresh signin with replacement password
existing-account signup → OTP → explicit safe existing_account guidance
```

The full-stack browser proof used production-built Web, real same-origin HTTPS, FastAPI, disposable PostgreSQL 18.6 and loopback SMTP capture.

`TEST CODE EXISTS != TEST EXECUTION PASS` remains a permanent evidence rule for future phases; for M4 the required executions are complete and accepted.

---

## 8. Email/runtime posture carried forward

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

Test SMTP capture/control remains private harness support only; no production `/test/*` endpoint.

---

## 9. Next work: M5

Do **not** restart M4 architecture or implementation by default.

```text
M5 — Google + Apple + Passkeys + Explicit Linking
PLANNED / NEXT / NOT STARTED
```

Before implementation:

```text
read current official Google authentication guidance
read current official Apple Sign in with Apple guidance
read current WebAuthn/FIDO specifications
reconcile with DANTE M1–M4 contracts
freeze exact provider/passkey/linking semantics
then materialize minimal persistence/API/Web changes
```

Permanent M5 rules already known:

```text
ExternalIdentity = issuer + subject
provider email != Account merge key
provider authentication != provider-data integration authorization
provider token != DANTE AuthSession
linking requires explicit proof + explicit consent
DANTE AuthSession remains canonical
```

M6 remains Native Mobile Access. M7 remains the final whole-vertical security/observability/handoff gate.

---

## 10. Whole-vertical status

```text
M1 CLOSED
M2 CLOSED
M3 CLOSED
M4 CLOSED
M5 NEXT / PLANNED
M6 PLANNED
M7 PLANNED / FINAL GATE

Whole Access/Auth vertical
ACTIVE / NOT CLOSED
```

Only M7 plus explicit final user acceptance may close the whole Access/Auth vertical.
