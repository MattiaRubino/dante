# DANTE — Access/Auth M4–M7 Execution Plan

- **Status:** CURRENT EXECUTION PLAN / M4 CLOSED / M5 NEXT / M6–M7 PLANNED
- **Vertical:** Access/Auth
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **Closed prerequisite:** M1–M4 CLOSED; M4 engineering gate PASS; user acceptance ACCEPTED
- **M4 final accepted implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **Observability rule:** full production-credible baseline remains mandatory at M7 if still deferred
- **Purpose:** preserve accepted foundations, record M4 closure evidence and define the safe production-quality sequence through M5–M7.

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
4. this file
5. `docs/workstreams/access-auth-m4-live-handoff-2026-08-29.md`
6. Access/Auth architecture/security/API/testing contracts + ADR-011
7. `docs/frontend/access.md`
8. `docs/database/README.md` + `docs/database/access-auth.md`
9. current official external authorities required by the phase

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

Do not reopen without direct evidence and an explicit bounded architecture decision:

```text
JWT/localStorage browser Auth
Redis/JWT as session authority
Principal persistence table
silent provider-email account merge
Account advisory-lock replacement
Axios
Orval-generated React Query hooks as app boundary
wide credentialed CORS
frontend fake Auth success
persisted browser Auth cache
hidden sign-in form as bootstrap placeholder
route deep-import of Access application internals
```

Permanent M3 lesson:

```text
unknown/loading
!= signed-out
!= signed-in
!= empty
!= error
```

Router-first Auth bootstrap remains canonical.

Permanent M4 lessons:

```text
no Account before verified mailbox proof
anti-enumeration before mailbox proof
purpose-specific proof persistence rather than generic auth-token tables
recovery proof exact-identity binding
single-use reset + revoke all sessions + fresh signin
reauth rotates exact bearer on same AuthSession
external email I/O outside DB transaction
Web recovery bearer remains memory-only and URL-scrubbed
```

---

# 3. M4 closure record — COMPLETE

M4 lifecycle:

```text
Signup + Verification + Recovery + Password Reset + Reauthentication
```

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

Accepted M4 evidence:

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

Manual UAT covered:

```text
login/session/logout regression
new signup → OTP → Account/AuthSession → setup handoff
recovery → reset → replacement-password signin
existing-account signup → mailbox proof → safe existing_account result
```

Closure verdict:

```text
M4 ENGINEERING GATE     PASS
M4 MANUAL UAT           PASS
M4 USER ACCEPTANCE      ACCEPTED
M4                       CLOSED
```

No additional M4 QA cycle is required absent direct defect evidence.

---

# 4. M5 — Google + Apple + Passkeys + Explicit Linking

**Status:** `NEXT / PLANNED / NOT STARTED`

## 4.1 Required first step: current external-authority readback

Before freezing M5 implementation, read current official sources for:

```text
Google authentication / OpenID Connect
Sign in with Apple
WebAuthn / FIDO2 / passkeys
browser/platform passkey constraints
provider key discovery / rotation / nonce/state handling
```

Do not rely on remembered provider SDK behavior or historical examples when current protocol/security rules can change.

## 4.2 M5 architectural invariants

```text
ExternalIdentity = issuer + subject
provider email is an attribute, not an Account merge key
provider authentication != provider-data integration authorization
provider token/assertion != DANTE AuthSession
DANTE AuthSession remains canonical after successful provider/passkey proof
linking requires explicit proof + explicit user consent
no silent link from matching email
provider callback state/challenge is purpose-specific and bounded
passkey credential identity is server-authoritative
passwordless Account must remain possible
method != factor != assurance
```

M5 must fit the existing Account/AuthSession architecture rather than create parallel session authority.

## 4.3 M5 implementation sequence

```text
1. current official protocol readback
2. bounded M5 architecture/security/API contract
3. exact persistence delta only after semantics are frozen
4. provider transaction/challenge handling
5. ExternalIdentity and explicit-linking behavior
6. WebAuthn/passkey registration + authentication ceremonies
7. FastAPI/Pydantic public API
8. deterministic OpenAPI + Orval regeneration
9. governed @dante/api-client extension
10. Web Access provider/passkey/linking integration
11. focused static/unit/protocol/race/replay proof
12. real PostgreSQL acceptance where persistence is involved
13. real browser/provider/passkey integration proof where feasible
14. manual M5 UAT
15. docs reconciliation + explicit user acceptance
```

## 4.4 M5 proof obligations

At minimum prove:

```text
provider state/nonce replay rejection
provider cancel/error/outage behavior
issuer+subject identity authority
provider key rotation/JWK refresh behavior
email collision does not silently link Accounts
explicit linking requires authenticated Account control
link replay/race protection
passkey RP ID/origin/challenge/user-handle correctness
passkey registration replay rejection
passkey authentication replay rejection
lost-device/passwordless recovery posture remains coherent
multiple AuthSessions remain normal
provider/passkey success issues canonical DANTE AuthSession only
```

Do not multiply low-level transaction races across every browser; prove each invariant at the lowest truthful layer and use browser matrices for browser/product semantics.

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
multi-device behavior
deep links/provider callbacks
passkeys on native platforms
uninstall/reinstall semantics
real emulator/device proof
```

Native is not scaled Web and must not weaken server-side session authority.

---

# 6. M7 — Security Hardening + Observability + Authenticated Handoff

**Status:** `PLANNED / FINAL WHOLE-VERTICAL GATE`

M7 owns:

```text
whole-vertical threat/abuse/replay review
session/account management required by product
provider/linking/WebAuthn/native hardening
production-credible observability
privacy/legal/accessibility/dependency/release review
real authenticated handoff into next DANTE vertical
whole-vertical manual UAT
```

If observability is still deferred, M7 may not close without a credible baseline:

```text
privacy-safe structured logs
request/trace correlation
metrics/traces
collector/backend topology
useful dashboards/queries
secret-redaction proof
telemetry outage must not break Auth correctness
```

Never emit passwords, session/cookie bearer values, CSRF secrets, OTP/recovery secrets, OAuth codes/tokens or passkey private material.

---

## 7. Whole-vertical closure rule

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

Only completion of M5–M7 plus final explicit user acceptance may close the whole Access/Auth vertical.
