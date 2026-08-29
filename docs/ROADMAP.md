# DANTE Roadmap

- **Status:** CURRENT FOR `feature/access-auth`
- **Last reconciled:** 2026-08-29
- **Protected `main`:** integrated source authority; Access/Auth branch remains unmerged until explicit gate
- **Active vertical:** Access/Auth
- **Current macro-phase:** M4 — Signup + Verification + Recovery + Reset + Reauth
- **M4 architecture authority:** `architecture/access-auth-m4-contract.md`
- **Forward execution authority:** `workstreams/access-auth-m4-m7-execution-plan.md`
- **Observability:** PRE-M4 feasibility review completed; full observability DEFERRED TO M7

## 1. Completed foundations and forward sequence

```text
Product / North Star
        CURRENT
          ↓
Domain Model
        CLOSED
          ↓
Logical Model
        CLOSED / 57 OF 57 / WL-H01..WL-H12
          ↓
Pre-Physical Coherence
        CLOSED / FINAL QA PASS
          ↓
Physical Model / PostgreSQL 18
        CLOSED
          ↓
Engineering + Frontend + Backend CP1–CP6
        CLOSED / ACCEPTED
          ↓
Access Pre-Backend Web Materialization
        CLOSED / ACCEPTED
          ↓
Access/Auth M1 — Visual / UX Freeze
        CLOSED
          ↓
Access/Auth M2 — Auth Architecture Freeze
        CLOSED
          ↓
Access/Auth M3 — Email/Password Signin + AuthSession Spine
        CLOSED / ENGINEERING PASS / USER ACCEPTED
          ↓
Observability PRE-M4 feasibility
        COMPLETE
        FULL STACK DEFERRED TO M7
          ↓
Access/Auth M4 — Signup + Verification + Recovery + Reset + Reauth
        ACTIVE
          ↓
Access/Auth M5 — Google + Apple + Passkeys + Explicit Linking
        PLANNED
          ↓
Access/Auth M6 — Native Mobile Access
        PLANNED
          ↓
Access/Auth M7 — Security Hardening + Observability + Authenticated Handoff
        PLANNED / FINAL WHOLE-VERTICAL GATE
```

M3 is closed. The whole Access/Auth vertical is not.

---

## 2. Current branch database baseline

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

Permanent structural change rule:

```text
Alembic
≈ SQLAlchemy
≈ Database Dictionary
≈ current human DB reference
≈ real PostgreSQL
≈ direct tests
```

Applied historical revisions are immutable evidence.

---

## 3. M1–M3 closed foundations

### M1 — Visual / UX Freeze

**CLOSED.** Existing Access composition is the production baseline. No redesign-for-novelty.

### M2 — Auth Architecture Freeze

**CLOSED / M2.1–M2.11 ACCEPTED.** Binding foundations include:

```text
same-origin browser topology
opaque DB-backed AuthSession
Secure HttpOnly host-only cookie
CSRF + Origin + Fetch Metadata
Account / EmailIdentity / optional PasswordCredential
runtime-only Principal
multiple independent sessions
Argon2id + HIBP + normalized email comparison
/api/v1 + RFC9457
READ COMMITTED + targeted locking
Account security serialization point
OpenAPI → Orval Fetch → governed @dante/api-client
real PostgreSQL + real browser proof contract
```

### M3 — Email/Password Signin + AuthSession Spine

**CLOSED / ENGINEERING PASS / USER ACCEPTED.** Evidence:

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

Permanent M3 regression rules:

```text
unknown/loading != signed-out/signed-in
critical session state resolves at Router boundary
no login-first + useEffect repair
no hidden sign-in geometry placeholder
route consumes Access public API only
no persisted browser Auth cache
no fake frontend Auth success
```

---

## 4. Observability decision

The bounded feasibility review found that DANTE already has server-authoritative `request_id` correlation but currently has no OTel/Prometheus dependency and no local Grafana-class stack; local Compose is essentially PostgreSQL.

Therefore:

```text
FULL OBSERVABILITY BEFORE M4 = NO
FULL OBSERVABILITY = DEFERRED TO M7
```

M4–M6 still require privacy-safe logging and must never emit Auth/proof/provider/passkey secrets.

M7 may not close Access/Auth without a production-credible observability/release gate.

---

# 5. M4 — Signup + Verification + Recovery + Reset + Reauth

**Status:** `ACTIVE / CONTRACT FREEZE → IMPLEMENTATION`

Detailed authority:

```text
docs/architecture/access-auth-m4-contract.md
```

M4 is executed as **one coherent macro-batch**, not six independent mini releases.

## 5.1 Standard password signup

Frozen Web shape stays:

```text
email
→ password
→ 6-digit email OTP
```

Canonical backend decision:

```text
email + password
→ pending PasswordSignupChallenge only
→ NO canonical Account yet

valid OTP
→ create Account
→ create VERIFIED EmailIdentity
→ create PasswordCredential
→ create AuthSession
→ delete pending signup
→ commit
→ issue cookie
```

This avoids canonical junk Accounts, unverified AuthSessions and email squatting by abandoned signup.

Initial signup remains non-enumerating. Existing verified-email signup does not modify the real Account/credential. Only after mailbox proof may the product reveal an `existing_account` outcome and route to signin/recovery.

## 5.2 Signup proof

```text
6 numeric digits
CSPRNG
HMAC-SHA256 verifier under dedicated purpose key
15-minute OTP lifetime
max 5 failed attempts per issued OTP
resend rotates OTP and invalidates old code
pending signup lifetime 24 h
```

A plain digest of the six-digit OTP is forbidden.

## 5.3 Email delivery

```text
Auth application
→ EmailDeliveryPort
→ bounded async dispatch queue
→ SMTP adapter
→ production transactional provider / local SMTP capture
```

No email network I/O inside PostgreSQL transactions. No unbounded `create_task` fan-out. No blind resend after ambiguous SMTP acceptance.

Transactional outbox remains capability-triggered; activate only if real deployment requires durable guaranteed dispatch.

## 5.4 Recovery

Public recovery initiation is neutral for known/unknown/disabled/provider-only accounts.

Eligible M4 password recovery requires:

```text
verified EmailIdentity
active Account
current PasswordCredential
```

Recovery challenge:

```text
32 random bytes / 256 bits
single use
30-minute baseline lifetime
new issuance supersedes previous challenge
raw secret never persisted/logged
```

Preferred email link keeps the raw bearer secret out of normal query strings and local/session storage.

## 5.5 Password reset

```text
valid recovery proof + new password
→ HIBP + Argon2 outside transaction
→ Account security lock
→ replace credential
→ consume/remove recovery proof
→ revoke ALL AuthSessions
→ commit/reconcile ambiguity
→ NO auto-login
→ fresh normal signin required
```

## 5.6 Reauthentication

```text
same AuthSession
+ fresh password evidence
→ update server-side recent_auth_at
→ rotate session secret
→ replacement cookie/CSRF
```

Default recent-auth freshness candidate: **10 minutes**, configurable and always enforced by backend-sensitive operations.

Reauth does not create a second AuthSession and is not a client boolean.

## 5.7 M4 planned persistence

Exactly two purpose-specific ephemeral security objects are expected:

```text
password_signup_challenge
password_recovery_challenge
```

No generic `auth_token`, `proof(type,payload)` or JSONB god-table.

## 5.8 M4 target API

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

All unsafe Web calls preserve the M3 ingress/security contract.

## 5.9 M4 performance posture

```text
Argon2/HIBP outside DB transactions
existing bounded KDF admission reused
bounded signup/recovery/reauth ingress limiters
bounded email dispatch queue/workers
short READ COMMITTED transactions
indexed equality lookups on hot paths
PostgreSQL uniqueness = final email race arbiter
Account lock only for Account-wide mutations
no blanket SERIALIZABLE
no network/human wait while row locks are held
no blind mutation retries
```

## 5.10 M4 testing strategy

Do **not** run six expensive closure cycles.

During implementation:

```text
focused unit/service tests
schema/Dictionary/migration checks
critical concurrency/replay tests
static/type/lint/generated checks
```

At candidate closure:

```text
ONE integrated real PostgreSQL M4 matrix
+ ONE integrated Chromium/Firefox/WebKit M4 matrix
+ ONE manual integrated M4 UAT
```

Low-level DB race tests are not redundantly repeated in all browser engines.

Critical browser proof:

```text
signup → captured real OTP → verify → authenticated/setup
existing-account signup after mailbox proof remains non-destructive
resend invalidates old code
recovery link → reset → fresh signin
old sessions rejected after reset
reauth rotates cookie but preserves AuthSession identity
degraded DB/email/server paths never fake success
M3 Router-first refresh regression remains fixed
```

M4 closes only after technical/security review, aligned DB/client/docs, real DB/browser proof and explicit user acceptance.

---

# 6. M5 — Google + Apple + Passkeys + Explicit Linking

**Status:** `PLANNED / AFTER M4`

Before coding, re-read current official Google/Apple/WebAuthn/FIDO specifications.

Permanent rules:

```text
ExternalIdentity = issuer + subject
provider email != automatic Account-link key
provider login != Gmail/Calendar/iCloud authorization
provider token != DANTE AuthSession
DANTE AuthSession remains canonical
```

Design explicit collision/linking state machine before implementation. Prove replay/cancel/outage/key rotation and linking races.

Passkey gate covers RP ID/origin, user handle, UV, attestation posture, discoverable credentials, multiple passkeys, revoke/lost-device and passwordless Accounts. Private passkey material never reaches DANTE servers.

---

# 7. M6 — Native Mobile Access

**Status:** `PLANNED / AFTER M5 UNLESS EXPLICITLY RE-GATED`

Use existing Expo / React Native / Expo Router and the same canonical Account/AuthSession backend.

Close native-specific transport/security first:

```text
session credential representation
SecureStore / Keychain / Keystore
CSRF applicability
app lifecycle / restart / background
logout/revoke
multi-device
verification/recovery/provider deep links
passkey platform APIs
uninstall/reinstall semantics
```

Native is not scaled Web. Critical native security requires real emulator/device proof.

---

# 8. M7 — Security Hardening + Observability + Authenticated Handoff + Vertical Closure

**Status:** `PLANNED / FINAL GATE`

M7 owns:

```text
whole-vertical threat review
credential stuffing / spraying / enumeration / rate abuse
session theft/fixation/replay
verification/recovery/reset replay
provider/linking/WebAuthn collision review
native credential/device-loss review
session/account management required by product
FULL observability baseline
privacy/legal/accessibility/dependency/release review
real authenticated handoff into next DANTE vertical
complete manual whole-vertical UAT
```

Observability must include privacy-safe structured logs, request/trace correlation, metrics/traces, collector/backend topology, useful dashboards/queries, redaction proof and non-fatal telemetry outage behavior. Grafana/Alloy/Loki/Tempo/Prometheus/Mimir remain candidates, not mandatory brand choices.

Only M7 + explicit final user acceptance may close the whole Access/Auth vertical.

---

## 9. Branch/worktree rule

Continue exactly:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

No new branch/worktree merely because M4 begins. Do not merge/rebase/force-push/history-rewrite or write to protected `main` without explicit user gate.

The separate `/home/mattia/projects/dante-frontend` worktree remains independent Home/frontend territory.

---

## 10. Immediate sequence

```text
1. M3 remains CLOSED
2. M4 architecture contract readback against M2 authorities
3. materialize exact two-table M4 persistence + ACL delta
4. implement signup/verification/recovery/reset/reauth + email boundary as one batch
5. regenerate OpenAPI/client
6. wire existing Access states
7. focused tests while coding
8. one integrated static + real PostgreSQL M4 gate
9. one integrated cross-browser M4 gate
10. manual M4 UAT
11. docs reconciliation + explicit M4 acceptance
12. then M5
```

Do not reopen M3 or implement the deferred observability stack now unless a new direct requirement explicitly re-gates it.
