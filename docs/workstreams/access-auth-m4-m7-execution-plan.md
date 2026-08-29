# DANTE — Access/Auth M4–M7 Execution Plan

- **Status:** CURRENT EXECUTION PLAN / M4 CLOSED / M5 ACTIVE / M5.1 COMPLETE / M5.2 NEXT / M6–M7 PLANNED
- **Vertical:** Access/Auth
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **Closed prerequisite:** M1–M4 CLOSED; M4 engineering gate PASS; user acceptance ACCEPTED
- **M4 final accepted implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **M5 architecture authority:** `../architecture/access-auth-m5-contract.md`
- **M5 live handoff:** `access-auth-m5-live-handoff-2026-08-29.md`
- **Observability rule:** full production-credible baseline remains mandatory at M7 if still deferred
- **Purpose:** preserve accepted foundations and define the safe production-quality sequence through M5–M7.

> This plan does not reopen M1–M4 and does not authorize a new branch/worktree. Repository truth and accepted Access/Auth architecture/security/API/testing contracts remain binding.

---

## 1. Mandatory continuation rules

Continue exactly:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Before writes, follow `docs/development/agent-operating-manual.md`: establish PRE-SCOPE SHA, exact paths, exact intended modifications and explicit user approval.

Never infer that a new chat means a new branch/worktree. No merge/rebase/history rewrite/protected-main write without explicit user gate.

Read current state first:

1. `docs/PROJECT-STATUS.md`
2. `docs/ROADMAP.md`
3. `docs/workstreams/access-auth.md`
4. `docs/workstreams/access-auth-m5-live-handoff-2026-08-29.md`
5. `docs/architecture/access-auth-m5-contract.md`
6. this file
7. Access/Auth architecture/security/API/testing contracts + ADR-011
8. `docs/frontend/access.md`
9. `docs/database/README.md` + `docs/database/access-auth.md` + Dictionary
10. CP6 persistence constitution
11. current official external authorities only where adapter/config details can change

---

## 2. M1–M4 frozen foundations — reuse, do not replace

```text
Account = durable access/security root
EmailIdentity separate from Account
PasswordCredential optional
Principal runtime-derived
opaque PostgreSQL-backed AuthSession
multiple independent AuthSessions normal
same-origin Web Auth topology
Secure HttpOnly host-only __Host-dante-session
session-bound CSRF
Origin + Fetch Metadata + X-Dante-Client Web ingress
/api/v1 + RFC9457 problem contract
Account security serialization point
READ COMMITTED + targeted locking
no blind mutation retry
ambiguous-commit reconciliation only where explicitly designed
FastAPI/Pydantic → deterministic OpenAPI → Orval Fetch → governed @dante/api-client
TanStack Query remote lifecycle
TanStack Router critical-session bootstrap
real PostgreSQL proof
real HTTPS Chromium + Firefox + WebKit proof
```

Do not reopen without direct evidence and explicit bounded decision:

```text
JWT/localStorage browser Auth
Redis/JWT as session authority
Principal persistence table
silent provider-email account merge
provider token as DANTE AuthSession
Account advisory-lock replacement
Axios
Orval-generated React Query hooks as app boundary
wide credentialed CORS
frontend fake Auth success
persisted browser Auth cache
hidden sign-in form as bootstrap placeholder
route deep-import of Access internals
```

Permanent M3 lesson:

```text
unknown/loading != signed-out != signed-in != empty != error
```

Permanent M4 lessons:

```text
no Account before accepted mailbox proof
anti-enumeration before mailbox/account disclosure
purpose-specific proof persistence rather than generic auth-token tables
recovery proof exact-identity binding
single-use reset + revoke all sessions + fresh signin
reauth rotates exact bearer on same AuthSession
external email I/O outside DB transaction
Web recovery bearer memory-only + URL-scrubbed
```

---

# 3. M4 closure record — COMPLETE

Final implementation checkpoint:

```text
c95e3b2ca664725bcacc374cb5ba6ed49409fe2b
fix(auth): reconcile M4 PostgreSQL acceptance
```

Accepted M4 persistence:

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

No additional M4 QA absent direct defect evidence.

---

# 4. M5 — Google + Apple + Passkeys + Explicit Linking

**Status:** `ACTIVE`

Durable authority:

```text
docs/architecture/access-auth-m5-contract.md
```

Continuation save-game:

```text
docs/workstreams/access-auth-m5-live-handoff-2026-08-29.md
```

## 4.1 M5.1 — external-authority/benchmark/architecture freeze

**Status:** `COMPLETE`

Completed scope:

```text
current Google GIS/OIDC review
current Sign in with Apple Web/REST/grant-lifecycle review
current WebAuthn L3/FIDO review
browser/provider deployment constraints
mature-product benchmark sweep
reconciliation with M2–M4, frontend contract and CP6
```

Frozen invariants/capabilities:

```text
ExternalIdentity = issuer + subject
provider email is evidence/metadata, not Account merge key
provider authentication != provider-data integration authorization
DANTE AuthSession remains canonical
provider-enriched onboarding with provenance
provider bootstrap never silently overwrites later DANTE-owned profile state
Apple one-shot name data must not be lost
Apple Hide My Email supported as actual EmailIdentity
Apple grant/token revocation + server-notification lifecycle
explicit provider linking only after existing Account proof + consent
PasskeyCredential 0..N
opaque random WebAuthn Account user handle
resident/discoverable passkeys + userVerification required
synced/device-bound/hardware/cross-device passkeys where supported
passwordless Account
add-password capability
safe authenticator removal / anti-lockout
lost-authenticator passwordless recovery through strong email proof
Auth/data-integration grant isolation
```

M5.1 freezes semantics, not exact SQL/API spellings.

---

## 4.2 M5.2 — exact persistence + API design

**Status:** `NEXT / NOT STARTED`

This is the exact next work. Do not begin with provider controller implementation.

### Step A — repository/current-owner readback

Inspect:

```text
current Auth mappings/services/API/tests
Account/EmailIdentity/PasswordCredential/AuthSession Dictionary
M4 challenge objects
CP6 UUID/FK/index/ACL/migration doctrine
current Domain/Logical/Physical owner for profile/name/locale/setup/bootstrap
current frontend Access state/data-source boundaries
```

### Step B — freeze M5 state machines

At minimum:

```text
Google known-identity signin
Google new-account enrollment
Google email collision/linking
third-party Google mailbox requiring DANTE proof
Apple known-identity signin
Apple first account creation
Apple form_post/callback/code exchange
Apple Private Relay lifecycle
Apple account-change notification handling
provider link/unlink
provider signin vs Account disable/unlink race
passkey registration
discoverable passkey signin
passkey add/remove
add first password
passwordless/lost-authenticator recovery
```

### Step C — exact physical delta

For every required persistent object, freeze:

```text
purpose/canonicality
exact name
columns/types/nullability
PK/FK/UNIQUE/CHECK
index + query justification
UUIDv7 vs bounded technical identity
secret/verifier/encryption representation
retention/cleanup
runtime ACL
Dictionary mapping
SQLAlchemy mapping
Alembic behavior
```

Semantic needs currently include:

```text
ExternalIdentity
provider signin/link transaction state
pending provider enrollment when mailbox proof remains required
Apple protected grant/token lifecycle
Apple notification idempotency only if durability requires it
opaque WebAuthn user handle
PasskeyCredential
WebAuthn registration/authentication challenge state
one-shot provider profile bootstrap only if no existing canonical owner can safely consume it
```

Do not infer one table per bullet. Do not create a generic auth-token god-table.

### Step D — exact API design

Freeze application intents/paths/operationIds/problems for:

```text
Google begin/complete
Apple begin/callback/complete
provider enrollment completion
explicit link begin/confirm
provider unlink
authentication-method view/manage where required
passkey registration begin/complete
passkey authentication begin/complete
passkey remove
add first password
passwordless recovery adaptation
Apple notification ingress
provider grant revoke/reconcile
```

Preserve `/api/v1`, RFC9457, no-store, request_id, deterministic OpenAPI and governed generated client.

### Step E — callback / browser topology

Freeze:

```text
provider state/nonce/purpose binding
safe return-target handling / no open redirects
Apple form_post protocol ingress exception without weakening normal CSRF
Google GIS browser/server handoff
WebAuthn origin/RP ID
M5 local test origin
real provider UAT origins
```

### Step F — dependency qualification

No hand-rolled JOSE/WebAuthn/AEAD.

Qualify maintained libraries for:

```text
Python 3.14
security/maintenance status
algorithm allowlisting
WebAuthn/COSE behavior
JWK/key rotation handling
uv lock determinism
mypy/Ruff/tests/build
```

### Step G — proof mapping

Map every invariant to the weakest truthful sufficient layer:

```text
unit/pure
real PostgreSQL
FastAPI HTTP
OpenAPI/generated client
Web application
browser full-stack
real external-provider acceptance
```

Then present one exact implementation write gate.

---

## 4.3 M5 implementation sequence after M5.2

Recommended implementation order:

```text
M5-A  persistence foundations / Dictionary / Alembic / mappings
M5-B  provider transaction + JOSE/JWK infrastructure
M5-C  Google authentication + account creation/collision
M5-D  Apple authentication + protected grant lifecycle + notifications
M5-E  explicit linking + authenticator lifecycle / anti-lockout
M5-F  WebAuthn/passkey registration + authentication
M5-G  add-password + passwordless recovery adaptation
M5-H  FastAPI/Pydantic + exact public API/problem contract
M5-I  deterministic OpenAPI + Orval + governed client
M5-J  Web Access provider/passkey/linking/smart-onboarding integration
M5-K  focused protocol/security/race proof
M5-L  real PostgreSQL acceptance
M5-M  browser/provider/passkey acceptance
M5-N  manual UAT
M5-O  docs reconciliation + explicit user acceptance
```

The exact split may be refined after M5.2, but do not mix unrelated concerns into one uncontrolled patch.

---

## 4.4 M5 proof obligations

### Provider common

```text
state/nonce replay rejection where applicable
provider cancel/error/outage
issuer+subject authority
JWK/key rotation
email collision does not silently link Accounts
explicit linking requires existing Account proof + consent
link replay/race protection
provider profile bootstrap does not overwrite later user-owned values
provider signin issues canonical DANTE AuthSession only
```

### Google

```text
valid known identity
new account
mailbox-authority distinction
third-party Google mailbox proof path
invalid signature/issuer/audience/expiry/nonce
unknown kid + bounded refresh
email/profile changes preserve issuer+subject binding
```

### Apple

```text
form_post/state/nonce/code exchange
ID-token verification
one-shot first-name/last-name handling
Private Relay
protected token/grant storage
revocation
signed server-to-server notifications
relay/account lifecycle changes
real registered-domain provider UAT
```

### WebAuthn

```text
RP ID/origin/challenge/userHandle correctness
registration replay/expiry
assertion replay/expiry
UV required
discoverable username-less signin
multiple passkeys
duplicate credential prevention
synced/device-bound metadata behavior
signCount risk policy
safe removal/anti-lockout
passwordless Account
lost-authenticator recovery
```

Do not multiply every low-level transaction race across every browser. Prove each invariant at the truthful layer.

---

## 4.5 Browser/provider acceptance topology

Mandatory CI:

```text
no public provider dependency
protocol-faithful local provider substitute
real DANTE adapter/application/security path
```

Known M5 constraints:

```text
M4 full-stack origin https://127.0.0.1 is not the target WebAuthn RP posture
M5 WebAuthn target: https://localhost:<ephemeral-port>, RP ID localhost, or equivalent reviewed test domain
Apple real Web proof requires registered HTTPS domain
Google/Apple real-provider smoke/UAT required before M5 production-ready closure
```

Chromium/Firefox/WebKit remain critical product matrix. If provider/passkey automation is engine-specific, record the bounded exception rather than faking capability.

---

# 5. M6 — Native Mobile Access

**Status:** `PLANNED / AFTER M5 UNLESS EXPLICITLY RE-GATED`

M6 reuses canonical Account/AuthSession authority with native-appropriate transport/storage.

Required concerns:

```text
secure session credential representation
Keychain / Keystore / SecureStore
app restart/background lifecycle
logout/revoke
multi-device
deep links/provider callbacks
native passkeys
uninstall/reinstall semantics
real emulator/device proof
```

Native is not scaled Web.

---

# 6. M7 — Security Hardening + Observability + Authenticated Handoff

**Status:** `PLANNED / FINAL WHOLE-VERTICAL GATE`

M7 owns:

```text
whole-vertical threat/abuse/replay review
complete session/account/device management required by product
new-login alerts / “this wasn’t me” response
provider/linking/WebAuthn/native final hardening
production-credible observability
privacy/legal/accessibility/dependency/release review
real authenticated handoff into next DANTE vertical
whole-vertical manual UAT
```

If observability is still deferred, M7 may not close without:

```text
privacy-safe structured logs
request/trace correlation
metrics/traces
collector/backend topology
useful dashboards/queries
secret-redaction proof
telemetry outage must not break Auth correctness
```

Never emit password/session/CSRF/OTP/recovery/provider-token/passkey secret material.

---

## 7. Whole-vertical closure rule

```text
M1 CLOSED
M2 CLOSED
M3 CLOSED
M4 CLOSED
M5 ACTIVE
  M5.1 COMPLETE
  M5.2 NEXT
M6 PLANNED
M7 PLANNED / FINAL GATE

Whole Access/Auth vertical
ACTIVE / NOT CLOSED
```

Only completion of M5–M7 plus final explicit user acceptance may close the whole Access/Auth vertical.