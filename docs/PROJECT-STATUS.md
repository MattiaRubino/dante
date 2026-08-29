# DANTE — Project Status

- **Status:** CURRENT TRUTH FOR `feature/access-auth`
- **Last reconciled:** 2026-08-29
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active product vertical:** Access/Auth
- **Last closed macro-phase:** M4 — Signup + Verification + Recovery + Reset + Reauth — **CLOSED / ENGINEERING PASS / USER ACCEPTED**
- **Next macro-phase:** M5 — Google + Apple + Passkeys + Explicit Linking — **PLANNED / NOT STARTED**
- **Final accepted M4 implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **M4 closure handoff:** `workstreams/access-auth-m4-live-handoff-2026-08-29.md`
- **M4 architecture authority:** `architecture/access-auth-m4-contract.md`
- **Forward execution authority:** `workstreams/access-auth-m4-m7-execution-plan.md`
- **Observability:** full production-credible baseline DEFERRED TO M7; this did not block M4

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
CLOSED / ENGINEERING PASS / USER ACCEPTED

Access/Auth M5 — Google + Apple + Passkeys + Explicit Linking
PLANNED / NEXT / NOT STARTED

Access/Auth M6 — Native Mobile Access
PLANNED

Access/Auth M7 — Security Hardening + Observability + Authenticated Handoff
PLANNED / FINAL WHOLE-VERTICAL GATE / OBSERVABILITY MANDATORY

Whole Access/Auth vertical
ACTIVE / NOT CLOSED
```

M1–M4 remain closed unless direct defect evidence justifies a bounded reopen. Closing M4 does **not** close the whole Access/Auth vertical.

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

Accepted M4 branch state after migration `20260829_11`:

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

This M4 state is no longer a source-only candidate. It is reconciled across Dictionary, SQLAlchemy, Alembic and the real PostgreSQL/current-catalog acceptance suite.

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

## 4. Closed M3 production spine

M3 production API remains:

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

Never reintroduce login-first + effect repair, hidden sign-in geometry placeholders or persisted browser Auth truth.

---

## 5. Closed M4 lifecycle

Authority:

```text
docs/architecture/access-auth-m4-contract.md
```

M4 is implemented and accepted as one coherent lifecycle.

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

Existing canonical email remains anti-enumeration safe: account existence is revealed only after mailbox proof; the submitted signup password is discarded, the existing credential is not overwritten and no fake session is issued.

Recovery/reset:

```text
known/unknown public semantics neutral
256-bit high-entropy raw bearer
single current challenge per Account
proof bound to exact EmailIdentity + Account
new issue supersedes old
raw proof never persisted/logged
single-use reset
replace password
revoke ALL AuthSessions
no auto-login
fresh normal signin required
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

---

## 6. M4 accepted engineering evidence

Final implementation checkpoint before documentation closure:

```text
c95e3b2ca664725bcacc374cb5ba6ed49409fe2b
fix(auth): reconcile M4 PostgreSQL acceptance
```

Accepted evidence accumulated on the integrated candidate:

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

The browser matrix exercised production-built Vite/React, real same-origin HTTPS, FastAPI, disposable PostgreSQL 18.6 and protocol-faithful loopback SMTP capture.

Manual UAT accepted:

```text
login / authoritative session / logout regression
new signup → email OTP → Account/AuthSession → setup handoff
password recovery → captured recovery link → reset → fresh signin
existing-account signup → mailbox proof → explicit existing_account outcome
```

The existing-account UAT also confirmed the intended anti-enumeration UX: DANTE does not reveal account existence before mailbox proof.

---

## 7. M4 hardening that remains binding

```text
OTP verifier = HMAC-SHA256 under a dedicated purpose key, bound to signup_ref
password pepper / OTP key / CSRF key material are distinct
recovery bearer is 256-bit and purpose-separated
recovery challenge is bound to exact EmailIdentity + Account at PostgreSQL level
reset consumes proof with conditional DELETE ... RETURNING
reauth is conditioned on the exact bearer verifier presented
stale bearer cannot rotate again after concurrent reauth
Argon2/HIBP/network work remains outside DB security transactions
READ COMMITTED + targeted serialization; no blanket SERIALIZABLE
no blind mutation retries
runtime ACL remains narrow/column-bounded
bounded SMTP queue/workers/timeouts/shutdown
no SMTP/network I/O inside DB transaction
non-local SMTP requires STARTTLS/TLS
no password/session/CSRF/OTP/recovery-secret logging
```

---

## 8. Next work — M5

M4 is closed. Do not continue M4 implementation by default.

Next macro-phase:

```text
M5 — Google + Apple + Passkeys + Explicit Linking
PLANNED / NEXT / NOT STARTED
```

Before M5 implementation, re-read current official Google, Apple and WebAuthn/FIDO specifications and perform the bounded M5 architecture/security contract gate. Preserve:

```text
ExternalIdentity = issuer + subject
provider email != Account merge key
provider login != Gmail/Calendar/iCloud data authorization
provider token != DANTE AuthSession
linking requires explicit proof/consent
DANTE AuthSession remains canonical
```

M6 and M7 remain planned. Full observability remains a mandatory M7 closure gate if still deferred.

---

## 9. Branch/worktree safety

Continue exactly unless the user explicitly changes topology:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

No new Access branch/worktree, merge, rebase, history rewrite or protected-main write without explicit user gate.

Current continuation/closure record:

```text
docs/workstreams/access-auth-m4-live-handoff-2026-08-29.md
```
