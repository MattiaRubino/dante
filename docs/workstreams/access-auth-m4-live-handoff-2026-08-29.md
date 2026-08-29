# DANTE — Access/Auth M4 Closure Handoff — 2026-08-29

- **Status:** M4 CLOSED / ENGINEERING PASS / USER ACCEPTED
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Final accepted M4 implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **Checkpoint message:** `fix(auth): reconcile M4 PostgreSQL acceptance`
- **Closed macro-phases:** M1–M4
- **Next macro-phase:** M5 — Google + Apple + Passkeys + Explicit Linking — PLANNED / NOT STARTED
- **Observability:** full Grafana/OpenTelemetry-class baseline DEFERRED TO M7

> This file is now the historical closure/continuation checkpoint for M4. Repository truth beats conversation memory. M4 is closed; future chats must not restart it merely because this file originated as a live handoff.

---

## 1. Mandatory continuation boundary

Continue exactly unless the user explicitly changes topology:

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

The separate `/home/mattia/projects/dante-frontend` worktree remains independent Home/frontend territory.

---

## 2. Read order for continuation into M5

Read in this order before modifying Access/Auth again:

1. `docs/PROJECT-STATUS.md`
2. `docs/ROADMAP.md`
3. `docs/workstreams/access-auth.md`
4. this M4 closure handoff
5. `docs/workstreams/access-auth-m4-m7-execution-plan.md`
6. `docs/architecture/access-auth-architecture.md`
7. `docs/architecture/access-auth-security-contract.md`
8. `docs/architecture/access-auth-api-contract.md`
9. `docs/architecture/access-auth-testing-contract.md`
10. `docs/decisions/ADR-011-access-auth-architecture.md`
11. `docs/architecture/access-auth-m4-contract.md` when M4 behavior is relevant
12. `docs/database/README.md`
13. `docs/database/access-auth.md`
14. `docs/frontend/access.md`
15. `docs/development/agent-operating-manual.md`
16. current official Google, Apple and WebAuthn/FIDO sources before freezing M5

Do not reinterpret M1–M4 from scratch.

---

## 3. Frozen foundations carried out of M4

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived
multiple independent AuthSessions normal
frontend request/success != backend-authoritative success
unknown/loading != signed-out/signed-in
provider email never silently links Accounts
method != factor != assurance
```

M3 Router-first bootstrap remains canonical:

```text
hard load
→ Router loader resolves/prefetches /auth/session
→ Query cache ready
→ AccessPage mounts
→ first business render is authoritative
```

Do not reopen without direct defect evidence and a bounded explicit gate:

```text
JWT/localStorage browser Auth
Redis/JWT session authority
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

---

## 4. M4 architecture closed as implemented

Authority:

```text
docs/architecture/access-auth-m4-contract.md
```

Standard signup:

```text
email
→ password
→ PasswordSignupChallenge only
→ six-digit email OTP
→ only after valid mailbox proof:
   Account
   + verified EmailIdentity
   + PasswordCredential
   + AuthSession
```

Anonymous signup remains anti-enumeration safe. Multiple pending challenges for one email are isolated by `signup_ref`. Existing canonical Account state is revealed only after mailbox proof; the submitted signup password is discarded and never overwrites an existing PasswordCredential.

Recovery/reset:

```text
neutral recovery initiation
→ high-entropy recovery proof
→ exact EmailIdentity + Account binding
→ one current challenge per Account
→ newer proof supersedes older proof
→ single-use password reset
→ replace PasswordCredential
→ revoke ALL AuthSessions
→ no auto-login
→ fresh normal signin
```

Reauthentication:

```text
current AuthSession + CSRF + fresh password
→ same auth_session_ref
→ exact presented bearer required
→ refresh recent_auth_at/session window
→ rotate bearer
→ stale bearer rejected
```

Canonical endpoint is `POST /api/v1/auth/reauthenticate`.

---

## 5. Accepted persistence state

M4 migration:

```text
apps/backend/migrations/versions/20260829_11_m4_auth_lifecycle_challenges.py
revision:       20260829_11
down_revision: 20260827_10
```

Accepted branch catalog:

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
+ exact EmailIdentity↔Account composite recovery binding
+ narrow runtime ACL evolution for Account / EmailIdentity /
  PasswordCredential / AuthSession / challenge tables
```

Database reconciliation invariant remains:

```text
Dictionary
≈ SQLAlchemy
≈ Alembic
≈ PostgreSQL catalog
≈ human DB reference
≈ direct tests
```

Least privilege remains deliberate; do not widen Auth tables to broad UPDATE/DELETE for convenience.

---

## 6. Materialized M4 runtime and API

The closed implementation includes:

```text
purpose-separated OTP/recovery cryptography
validated M4 settings
bounded lifecycle rate limiters
pending signup creation + OTP verify + resend
atomic Account/EmailIdentity/PasswordCredential/AuthSession establishment
existing-account collision protection
neutral recovery initiation
non-consuming recovery validation
single-use password reset
all-session revoke after reset
same-session reauth + exact bearer rotation
bounded SMTP dispatcher
SMTP capture/private E2E control support
M4 FastAPI public API
same-origin browser ingress security
OpenAPI exporter + deterministic snapshot
Orval-generated operations/models/Zod
governed @dante/api-client M4 boundary
Web Auth remote M4 operations
TanStack Query mutation lifecycle
Access real signup/verify/resend/recovery/reset/reauth wiring
memory-only recovery bearer capture + immediate URL fragment scrub
```

Public M4 API:

```text
POST /api/v1/auth/signup
POST /api/v1/auth/signup/verify
POST /api/v1/auth/signup/resend
POST /api/v1/auth/recovery
POST /api/v1/auth/recovery/validate
POST /api/v1/auth/reset-password
POST /api/v1/auth/reauthenticate
```

Auth responses preserve `Cache-Control: no-store`, request-id governance, RFC9457 Problem Details and exact same-origin browser transport policy.

---

## 7. Accepted security hardening

```text
OTP verifier is HMAC-SHA256 under a dedicated key and bound to signup_ref
password pepper / OTP key / CSRF key material must be distinct
recovery bearer is 256-bit and purpose-separated
raw OTP/recovery/session secrets are never persisted or logged
recovery challenge binds exact EmailIdentity + Account in PostgreSQL
reset consumes proof via conditional DELETE ... RETURNING
reset revokes every AuthSession
reauth mutation requires exact bearer verifier presented by the request
stale bearer cannot rotate again after concurrent reauth
Argon2/HIBP/network work remains outside DB security transactions
READ COMMITTED + targeted Account serialization
no blanket SERIALIZABLE
no blind mutation retry
bounded queue/workers/SMTP timeout/shutdown
no email network wait inside DB transaction
non-local SMTP requires STARTTLS/TLS
```

---

## 8. Accepted M4 automated evidence

Final closure evidence:

```text
backend static / typing / lint / build        PASS
backend fast                                 87 / 87 PASS
real PostgreSQL marked suite                 87 / 87 PASS
Web Access UI                                22 / 22 PASS
real Auth full-stack browser                 33 / 33 PASS
Chromium                                     11 / 11 PASS
Firefox                                      11 / 11 PASS
WebKit                                       11 / 11 PASS
```

The full-stack matrix exercised:

```text
production-built Vite/React Web
real same-origin HTTPS
real FastAPI
real disposable PostgreSQL 18.6
protocol-faithful loopback SMTP capture
```

Critical browser behavior included M3 session regression plus M4 signup/verification, existing-account protection, recovery/reset, all-session invalidation and reauthentication semantics.

---

## 9. Manual integrated M4 UAT — PASS

User acceptance on 2026-08-29 covered:

```text
1. login / authoritative session / logout regression
   PASS

2. new signup
   email → password → captured six-digit OTP
   → Account/AuthSession created only after mailbox proof
   → setup/name handoff
   PASS

3. recovery/reset
   recovery request → captured recovery link
   → reset password → fresh signin with replacement password
   → authenticated return/Home
   PASS

4. existing-account signup
   same canonical email → password → OTP
   → no pre-proof account enumeration
   → after mailbox proof explicit existing_account guidance
   → no automatic authentication / no credential overwrite
   PASS
```

Manual M4 UAT therefore satisfies the human closure gate. User explicitly authorized M4 closure and documentation reconciliation.

---

## 10. M4 closure verdict

```text
lifecycle contract                         ACCEPTED
persistence / Dictionary / Alembic         ALIGNED
backend runtime                            COMPLETE
email boundary                             COMPLETE
OpenAPI / generated client                 ALIGNED
Web Access real integration                COMPLETE
static / type / lint / build               PASS
real PostgreSQL                            87 / 87 PASS
real Chromium/Firefox/WebKit               33 / 33 PASS
manual integrated UAT                      PASS
user acceptance                            ACCEPTED

M4                                         CLOSED
```

This does not close the whole Access/Auth vertical.

---

## 11. Immediate continuation: M5

Next macro-phase:

```text
M5 — Google + Apple + Passkeys + Explicit Linking
PLANNED / NEXT / NOT STARTED
```

Do not begin implementation by copying provider SDK examples directly. First re-read current official provider/WebAuthn authorities and freeze the bounded DANTE M5 contract.

Permanent M5 constraints already carried forward:

```text
ExternalIdentity = issuer + subject
provider email != Account merge key
provider login != provider-data authorization
provider token/assertion != DANTE AuthSession
linking requires explicit proof and explicit consent
DANTE AuthSession remains canonical
```

M6 remains Native Mobile Access. M7 remains the mandatory final security/observability/authenticated-handoff gate. Only M7 plus explicit final user acceptance may close the whole Access/Auth vertical.
