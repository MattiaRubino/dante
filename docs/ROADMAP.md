# DANTE Roadmap

- **Status:** CURRENT FOR `feature/access-auth`
- **Last reconciled:** 2026-08-29
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active vertical:** Access/Auth
- **Last closed macro-phase:** M4 — Signup + Verification + Recovery + Reset + Reauth
- **Next macro-phase:** M5 — Google + Apple + Passkeys + Explicit Linking
- **M4 final accepted implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **M4 closure handoff:** `workstreams/access-auth-m4-live-handoff-2026-08-29.md`
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
        CLOSED / ACCEPTED
          ↓
M2 — Auth Architecture Freeze
        CLOSED / ACCEPTED / QA PASS
          ↓
M3 — Email/Password Signin + AuthSession Spine
        CLOSED / ENGINEERING PASS / USER ACCEPTED
          ↓
Observability feasibility
        COMPLETE / FULL STACK DEFERRED TO M7
          ↓
M4 — Signup + Verification + Recovery + Reset + Reauth
        CLOSED / ENGINEERING PASS / USER ACCEPTED
          ↓
M5 — Google + Apple + Passkeys + Explicit Linking
        PLANNED / NEXT / NOT STARTED
          ↓
M6 — Native Mobile Access
        PLANNED
          ↓
M7 — Security Hardening + Observability + Authenticated Handoff
        PLANNED / FINAL WHOLE-VERTICAL GATE
```

The whole Access/Auth vertical is **not closed**. M4 closure advances the vertical to M5; it does not authorize a merge to `main` or skip M5–M7.

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

Accepted M4 state:

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

M4 added:

```text
password_signup_challenge
password_recovery_challenge
exact recovery EmailIdentity↔Account integrity binding
narrow runtime ACL evolution for account establishment and reauth
```

The M4 counts are now accepted observed PostgreSQL/current-catalog evidence, not merely a source target.

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

## 3. M1–M4 frozen foundation

M1–M4 are closed and reused.

Critical permanent rules:

```text
same-origin Web Auth
opaque PostgreSQL-backed AuthSession
Secure HttpOnly __Host-dante-session
CSRF + Origin + Fetch Metadata + X-Dante-Client
runtime-only Principal
multiple independent AuthSessions
Argon2id + HIBP + purpose-separated secrets
/api/v1 + RFC9457
READ COMMITTED + targeted Account serialization
no blind mutation retry
FastAPI → deterministic OpenAPI → Orval Fetch → governed @dante/api-client
TanStack Query remote lifecycle
Router-first critical session bootstrap
real PostgreSQL + real Chromium/Firefox/WebKit proof
```

Permanent frontend regression guard:

```text
unknown/loading != signed-out
route resolves authoritative session before Access business render
no login-first + useEffect repair
no hidden sign-in geometry placeholder
no persisted browser Auth cache
no fake frontend Auth success
```

M4 additionally freezes:

```text
no canonical Account before mailbox proof
existing-account outcome only after mailbox proof
recovery initiation remains anti-enumeration neutral
reset is single-use and revokes ALL AuthSessions
reset never auto-logs-in
reauth rotates the exact presented bearer on the same auth_session_ref
recovery secret remains memory-only in Web and is scrubbed from the URL fragment immediately
```

---

# 4. M4 — Signup + Verification + Recovery + Reset + Reauth

**Status:** `CLOSED / ENGINEERING PASS / USER ACCEPTED`

Final accepted implementation checkpoint:

```text
c95e3b2ca664725bcacc374cb5ba6ed49409fe2b
fix(auth): reconcile M4 PostgreSQL acceptance
```

Detailed closure record:

```text
docs/workstreams/access-auth-m4-live-handoff-2026-08-29.md
```

## 4.1 Accepted lifecycle semantics

Signup:

```text
email + password
→ pending PasswordSignupChallenge only
→ NO Account yet
→ six-digit CSPRNG OTP / purpose-separated HMAC verifier

valid mailbox proof
→ Account(active)
→ verified EmailIdentity
→ PasswordCredential
→ AuthSession
→ durable commit/reconciliation
→ cookie only after authoritative success
```

Existing canonical email after mailbox proof returns explicit `existing_account`; the submitted signup password is discarded, the existing credential is never overwritten and no AuthSession is issued by that signup attempt.

Recovery/reset:

```text
known/unknown public recovery semantics neutral
256-bit high-entropy raw bearer
single current recovery challenge per Account
proof bound to exact EmailIdentity + Account
new issuance supersedes prior proof
raw secret never persisted/logged
single-use reset
replace PasswordCredential
revoke ALL AuthSessions
NO auto-login
fresh signin required
```

Reauthentication:

```text
POST /api/v1/auth/reauthenticate
current AuthSession + session-bound CSRF + fresh password
→ same auth_session_ref
→ exact presented bearer verifier required
→ refresh recent-auth/session window
→ rotate session bearer
→ stale bearer rejected
```

## 4.2 Accepted public M4 API

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

Do not reintroduce `/auth/reauth/password`.

## 4.3 Accepted M4 engineering evidence

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

The browser closure used real same-origin HTTPS, production-built React/Vite, FastAPI, disposable PostgreSQL 18.6 and loopback SMTP capture.

Manual UAT accepted:

```text
login/session/logout M3 regression
new signup → OTP → authenticated setup handoff
recovery → reset → fresh signin with replacement password
existing-account signup → OTP → safe existing_account guidance
```

---

# 5. M5 — Google + Apple + Passkeys + Explicit Linking

**Status:** `PLANNED / NEXT / NOT STARTED`

Before implementation, re-read current official Google, Apple and WebAuthn/FIDO specifications and establish the bounded M5 contract against current provider behavior.

Permanent rules:

```text
ExternalIdentity = issuer + subject
provider email != Account merge key
provider login != Gmail/Calendar/iCloud data authorization
provider token != DANTE AuthSession
linking requires explicit proof/consent
DANTE AuthSession remains canonical
```

M5 must prove provider replay/cancel/outage/key rotation/linking collisions and passkey RP/origin/challenge/lost-device/passwordless semantics. M5 may not weaken M1–M4 AuthSession or anti-enumeration guarantees.

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

No new branch/worktree, merge, rebase, force-push/history rewrite or protected-main write without explicit user gate.
