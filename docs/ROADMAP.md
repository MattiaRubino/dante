# DANTE Roadmap

- **Status:** CURRENT FOR `feature/access-auth`
- **Last reconciled:** 2026-08-29
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active vertical:** Access/Auth
- **Last closed macro-phase:** M4 — Signup + Verification + Recovery + Reset + Reauth
- **Current macro-phase:** M5 — Google + Apple + Passkeys + Explicit Linking
- **M5.1:** COMPLETE
- **Next exact step:** M5.2 — exact persistence + API design
- **M4 final accepted implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **M5 architecture authority:** `architecture/access-auth-m5-contract.md`
- **M5 continuation handoff:** `workstreams/access-auth-m5-live-handoff-2026-08-29.md`
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
M4 — Signup + Verification + Recovery + Reset + Reauth
        CLOSED / ENGINEERING PASS / USER ACCEPTED
          ↓
M5 — Google + Apple + Passkeys + Explicit Linking
        ACTIVE
          ↓
M5.1 — External Authority + Benchmark + Architecture Freeze
        COMPLETE
          ↓
M5.2 — Exact Persistence + API Design
        NEXT / NOT STARTED
          ↓
M5 implementation/materialization
        NOT STARTED
          ↓
M6 — Native Mobile Access
        PLANNED
          ↓
M7 — Security Hardening + Observability + Authenticated Handoff
        PLANNED / FINAL WHOLE-VERTICAL GATE
```

The whole Access/Auth vertical is **not closed**. M5.1 completion does not authorize skipping M5 implementation/QA, M6 or M7 and does not authorize a merge to `main`.

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

M5.1 adds **no persistence**. Current accepted branch DB head remains `20260829_11`.

M5.2 must design the exact persistence delta before any migration:

```text
ExternalIdentity
provider transaction/link state
pending provider enrollment when mailbox proof remains required
Apple grant/token secret lifecycle
Apple notification idempotency only if durability requires it
opaque WebAuthn Account user handle
PasskeyCredential
WebAuthn ceremony challenges
one-shot provider profile-bootstrap staging only if no current canonical owner exists
```

The bullets are semantic needs, not pre-approved table names/counts.

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

Critical rules:

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

M4 additionally freezes:

```text
no canonical Account before accepted mailbox proof
existing-account outcome only after mailbox proof
recovery initiation anti-enumeration neutral
single-use reset + revoke ALL AuthSessions + no auto-login
reauth rotates exact presented bearer on same auth_session_ref
recovery secret memory-only in Web and URL-scrubbed immediately
```

---

# 4. M4 — CLOSED

**Status:** `CLOSED / ENGINEERING PASS / USER ACCEPTED`

Final accepted implementation checkpoint:

```text
c95e3b2ca664725bcacc374cb5ba6ed49409fe2b
fix(auth): reconcile M4 PostgreSQL acceptance
```

Accepted evidence:

```text
backend static / typing / lint / build        PASS
backend fast                                 87 / 87 PASS
real PostgreSQL marked suite                 87 / 87 PASS
Web Access UI                                22 / 22 PASS
real Auth full-stack browser                 33 / 33 PASS
Chromium / Firefox / WebKit                  11 / 11 PASS each
manual integrated M4 UAT                     PASS / USER ACCEPTED
```

Do not reopen/retest M4 absent direct regression evidence.

---

# 5. M5 — Multi-authenticator Account layer

**Status:** `ACTIVE`

Durable authority:

```text
docs/architecture/access-auth-m5-contract.md
```

Current continuation save-game:

```text
docs/workstreams/access-auth-m5-live-handoff-2026-08-29.md
```

## 5.1 M5.1 — Architecture / external authority freeze

**Status:** `COMPLETE`

Completed readback/benchmark:

```text
Google Identity Services / OIDC
Sign in with Apple Web/REST/grant lifecycle
WebAuthn Level 3 / FIDO passkeys
browser/platform constraints
mature-product patterns from Linear/Notion/GitHub/Todoist/Figma/Slack where relevant
reconciliation with DANTE M2–M4 and CP6
```

Frozen capability envelope:

```text
ExternalIdentity = issuer + subject
Google authentication
Sign in with Apple
provider email != Account merge key
explicit linking only
provider-enriched first-account bootstrap
provider provenance + no later profile overwrite
Apple one-shot name preservation
Apple Hide My Email support
Apple grant/revocation/server-notification lifecycle
PasskeyCredential 0..N
opaque WebAuthn user handle
username-less/discoverable passkey signin
synced/device-bound/hardware/cross-device passkeys where supported
passwordless Accounts
add-password capability
safe authenticator add/remove
anti-lockout
lost-all-passkeys/provider recovery through strong email recovery proof
Auth grants isolated from Gmail/Calendar/iCloud data integrations
future Security & Access settings readiness
```

No DANTE username is invented from provider data.

## 5.2 M5.2 — Exact persistence + API design

**Status:** `NEXT / NOT STARTED`

Must close before production code:

```text
exact persistent owners and object names
columns/types/nullability
PK/FK/UNIQUE/CHECK/indexes
secret/verifier/encryption model
retention/cleanup
runtime ACL
transaction/lock/race state machines
provider callback topology
WebAuthn RP/origin/challenge topology
exact public API paths
operationIds
RFC9457 machine problems
OpenAPI impact
dependency qualification
proof-layer matrix
```

Special questions:

```text
Where does one-shot provider profile bootstrap live without polluting Auth?
How is Apple grant material encrypted/rotated/revoked?
How are Apple notifications made idempotent?
How does M4 recovery become create-or-replace PasswordCredential for passwordless recovery?
What exact DB shape owns opaque WebAuthn userHandle and PasskeyCredential?
How is provider-link state bound to authenticated Account/recent-auth without weakening callback security?
```

## 5.3 Implementation sequence after M5.2

```text
Dictionary/persistence design
→ SQLAlchemy/Alembic
→ provider protocol adapters
→ Google
→ Apple
→ passkeys/WebAuthn
→ explicit linking/authenticator management
→ FastAPI/Pydantic
→ deterministic OpenAPI + Orval
→ governed @dante/api-client
→ Web Access integration
→ focused proof by layer
→ real PostgreSQL acceptance
→ real browser/provider/passkey proof
→ manual M5 UAT
→ docs reconciliation + explicit user acceptance
```

---

# 6. M5 closure proof direction

Mandatory CI remains deterministic and does not depend on public Google/Apple availability.

```text
DANTE real adapter/security path
→ protocol-faithful local Google/Apple substitutes
```

M5 closure additionally needs real-provider smoke/UAT against final provider configuration.

Known deployment/testing constraints:

```text
WebAuthn browser harness needs valid RP/domain posture; target https://localhost:<port>, RP ID localhost
Apple Web production acceptance requires an Apple-registered HTTPS domain
browser matrix remains Chromium + Firefox + WebKit for truthful product semantics
engine-specific WebAuthn/provider automation limitations are recorded, not faked
```

Real PostgreSQL remains required for persistence/race claims.

---

# 7. M6 — Native Mobile Access

**Status:** `PLANNED / AFTER M5 UNLESS EXPLICITLY RE-GATED`

Reuse canonical Account/AuthSession with native-appropriate transport/storage:

```text
Keychain / Keystore / SecureStore
app lifecycle
logout/revoke
multi-device
deep links/provider callbacks
native passkeys
uninstall/reinstall semantics
real emulator/device proof
```

Native is not scaled Web.

---

# 8. M7 — Security Hardening + Observability + Authenticated Handoff

**Status:** `PLANNED / FINAL ACCESS-AUTH GATE`

M7 owns final whole-vertical work including:

```text
complete session/device management UX
remote revoke / revoke all others / logout everywhere
new-login alerts and “this wasn’t me” response
whole-vertical threat/abuse/replay review
production-credible observability
privacy/legal/accessibility/dependency/release review
real authenticated handoff into next DANTE vertical
whole-vertical manual UAT
```

M7 may not be used to defer correctness-critical M5 requirements such as provider-link integrity, anti-lockout, Apple grant lifecycle or passwordless recovery coherence.

Only M7 + final explicit user acceptance may close the whole Access/Auth vertical.

---

## 9. Branch/worktree rule

Continue exactly:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

No new branch/worktree, merge, rebase, force-push/history rewrite or protected-main write without explicit user gate.