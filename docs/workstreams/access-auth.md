# DANTE — Access/Auth Full-Stack Vertical Workstream

- **Status:** ACTIVE VERTICAL / M1–M4 CLOSED / M5 ACTIVE / M5.1 COMPLETE / M5.2 NEXT
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Created from protected `main`:** `f011e252b6a294a12c38927ef2d528244ea1fee6`
- **M3:** CLOSED / ENGINEERING PASS / USER ACCEPTED
- **M4:** CLOSED / ENGINEERING PASS / USER ACCEPTED
- **M4 final implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **M4 documentation closure:** `a95955da72cbb9119982aa1544c2aaa356fc5e6a`
- **M5.1:** COMPLETE / architecture + external-authority freeze
- **M5 architecture authority:** `../architecture/access-auth-m5-contract.md`
- **M5 live handoff:** `access-auth-m5-live-handoff-2026-08-29.md`
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
4. `docs/workstreams/access-auth-m5-live-handoff-2026-08-29.md`
5. `docs/architecture/access-auth-m5-contract.md`
6. `docs/workstreams/access-auth-m4-m7-execution-plan.md`
7. `docs/workstreams/access-auth-m4-live-handoff-2026-08-29.md` when M4 evidence/history is needed
8. `docs/architecture/access-auth-architecture.md`
9. `docs/architecture/access-auth-security-contract.md`
10. `docs/architecture/access-auth-api-contract.md`
11. `docs/architecture/access-auth-testing-contract.md`
12. `docs/decisions/ADR-011-access-auth-architecture.md`
13. DB System of Record + `docs/database/access-auth.md` + Dictionary
14. CP6 persistence constitution
15. `docs/frontend/access.md`
16. `docs/development/agent-operating-manual.md`
17. current implementation/tests for the exact M5.2 concern

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
provider identity key = issuer + subject
provider email never silently links Accounts
provider authentication != provider-data integration authorization
provider token/assertion != DANTE AuthSession
passwordless Account valid
verification != setup completion
reauthentication != initial signin
frontend request/provider callback != backend-authoritative success
unknown/loading != signed-out/signed-in
method != factor != assurance
```

Do not reopen without a bounded explicit gate:

```text
JWT/localStorage browser Auth
Redis/JWT session authority
Principal table
silent provider-email merge
provider-specific parallel Account/session authority
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

M3 permanent regression guard:

```text
hard refresh
→ route loader resolves /auth/session
→ Query cache ready
→ AccessPage mounts once
→ first business render already authoritative
```

M4 permanent lifecycle guards:

```text
no canonical Account before accepted mailbox proof
anonymous signup does not reveal account existence
existing-account outcome only after mailbox proof
recovery initiation neutral
recovery proof single-use/superseding/exact-identity bound
password reset revokes ALL AuthSessions and never auto-logs-in
reauth rotates exact bearer on same auth_session_ref
Web recovery secret memory-only + fragment scrubbed
```

---

## 4. Closed M4 implementation state

Final accepted M4 implementation checkpoint:

```text
c95e3b2ca664725bcacc374cb5ba6ed49409fe2b
fix(auth): reconcile M4 PostgreSQL acceptance
```

Accepted M4 catalog:

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

Accepted M4 proof:

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

Manual UAT:

```text
login/session/logout
new signup → captured OTP → Account/AuthSession → setup handoff
recovery → captured link → reset → fresh signin
existing-account signup → OTP → safe existing_account guidance
```

No extra M4 QA absent direct regression evidence.

---

## 5. Current phase — M5

```text
M5 — Google + Apple + Passkeys + Explicit Linking
ACTIVE
```

M5 is the multi-authenticator Account layer, not a superficial social-login patch.

Capability envelope:

```text
Google authentication
Sign in with Apple
ExternalIdentity = issuer + subject
provider-enriched first-account bootstrap
explicit Account linking
passkeys/WebAuthn
passwordless Accounts
add-password capability
safe authenticator add/remove
anti-lockout
passwordless/lost-authenticator recovery coherence
provider grant/revocation lifecycle
Apple relay/account-change lifecycle
Auth vs provider-data integration isolation
future Security & Access settings readiness
```

---

## 6. M5.1 — COMPLETE

Authority:

```text
docs/architecture/access-auth-m5-contract.md
```

Continuation handoff:

```text
docs/workstreams/access-auth-m5-live-handoff-2026-08-29.md
```

M5.1 completed:

```text
Google GIS/OIDC official readback
Apple Web/REST/grant/revocation/account-change/relay readback
WebAuthn Level 3 / FIDO passkey readback
mature-product benchmark sweep
reconciliation with M2–M4 and CP6
architecture/security freeze
```

### 6.1 Provider identity/linking

```text
ExternalIdentity = issuer + subject
email coincidence != link authority
known issuer+subject → existing Account signin
unbound identity + collision → explicit link flow
link = provider proof + existing Account proof + recent auth + consent + Account lock + final uniqueness recheck
```

Do not assume every Account has a password during linking.

### 6.2 Provider-enriched bootstrap

Use all useful provider data that DANTE legitimately receives for first-run convenience, with provenance and data minimization.

Google examples when available:

```text
email/email_verified
name/given_name/family_name
picture
locale
hosted-domain metadata
```

Apple:

```text
email / Private Relay
first/last name on first authorization when supplied
provider reachability/lifecycle semantics
```

Rule:

```text
provider → bootstrap
user later edits in DANTE → DANTE owns value
future provider login → no silent overwrite
```

No canonical DANTE username is inferred.

Apple one-shot name must not be lost. Use existing canonical profile/setup owner if valid, otherwise bounded durable bootstrap staging; M5.2 decides exact owner after Domain/Logical/Physical inspection.

### 6.3 Google

Initial Web direction:

```text
Google Identity Services
official button/branding
explicit user action
auto-select off by default
FedCM-compatible current path where supported
One Tap optional later
```

Server verifies signature/JWK/issuer/audience/expiry/nonce/subject and other current protocol-required claims.

Mailbox authority is classified: verified Gmail/Workspace can satisfy exact-address proof; third-party-mailbox Google accounts do not automatically satisfy current DANTE mailbox control requirements.

No Gmail/Calendar scopes in Auth.

### 6.4 Apple

```text
server state + nonce
provider form_post callback
server-side code exchange
ID-token verification
issuer + subject
```

Hide My Email relay is a valid EmailIdentity; DANTE does not force hidden real email.

Apple first-name/last-name data may be one-shot and is bootstrap/user data, not signed identity.

Production Apple lifecycle includes protected minimum token/grant retention, revocation and signed server-to-server account-change notifications. Retained secret material requires authenticated encryption with key material outside PostgreSQL/Git.

### 6.5 Passkeys

```text
Account → 0..N PasskeyCredential
resident/discoverable credentials
userVerification required
privacy-minimizing attestation none
synced/device-bound/hardware/password-manager passkeys
username-less signin
cross-device/hybrid where supported
```

Use stable opaque random WebAuthn `user.id`, not `account_ref`.

`signCount` anomaly is a risk signal, not automatic Account lockout.

Conditional UI/WebAuthn L3 signals are progressive enhancement only.

### 6.6 Authenticator lifecycle

```text
link/unlink Google
link/unlink Apple
add/remove passkey
add password to passwordless Account
safe password removal when another access path remains and policy permits
```

Normal removal may not leave Account with no viable auth/recovery path.

### 6.7 Passwordless recovery

M4 recovery must be adaptable from replace-only to create-or-replace PasswordCredential:

```text
strong email recovery proof
→ create first password if absent OR replace current password
→ HIBP + Argon2 policy
→ revoke ALL AuthSessions
→ no auto-login
→ fresh signin
```

Preserve M4 anti-enumeration, exact binding, single-use and conditional consume.

---

## 7. M5.2 — NEXT

```text
M5.2 — exact persistence + API design
NEXT / NOT STARTED
```

Do not begin by coding Google/Apple callbacks.

M5.2 sequence:

```text
1. inspect current Auth implementation/tests
2. inspect Dictionary + CP6 rules
3. inspect existing Domain/Logical owner for profile/name/locale/bootstrap
4. freeze provider/link/passkey/recovery state machines
5. freeze minimal physical objects
6. freeze PK/FK/UNIQUE/CHECK/indexes
7. freeze retention/encryption/verifier/cleanup
8. freeze runtime ACL
9. freeze exact API paths/operationIds/problem codes
10. freeze callback/redirect + WebAuthn RP/origin topology
11. qualify dependencies
12. map every invariant to proof layer
13. present exact implementation write gate
```

M5 persistence is **not** yet authorized/materialized.

---

## 8. Current DB posture

Accepted head remains:

```text
20260829_11
```

M5.1 semantic needs to design in M5.2 include:

```text
ExternalIdentity
provider transaction/link state
pending provider enrollment when mailbox proof remains required
Apple protected grant lifecycle
Apple notification idempotency only if needed
opaque WebAuthn user handle
PasskeyCredential
WebAuthn challenge state
one-shot profile-bootstrap staging only if no canonical owner exists
```

These are not pre-approved one-table-per-line SQL names.

Permanent rule:

```text
Dictionary
≈ SQLAlchemy
≈ Alembic
≈ real PostgreSQL catalog
≈ human DB reference
≈ direct tests
```

---

## 9. M5 testing posture

Mandatory CI:

```text
real DANTE adapter/protocol path
→ deterministic protocol-faithful local provider substitutes
→ no public Internet dependency
```

M5 closure also requires real Google/Apple smoke/UAT against final provider configuration.

Known constraints:

```text
Apple Web real acceptance requires registered HTTPS domain
WebAuthn test origin needs valid RP/domain posture; target https://localhost:<port>, RP ID localhost
Chromium/Firefox/WebKit remain critical product matrix
engine-specific WebAuthn/provider automation limitations are recorded truthfully, not faked
```

Real PostgreSQL is mandatory for persistence/race claims.

---

## 10. Email/runtime posture carried forward

M4 SMTP rules remain:

```text
bounded queue/workers/timeouts/shutdown
no network I/O in DB transaction
no blind transport retry after ambiguous SMTP acceptance
non-local SMTP STARTTLS/TLS
proof/recipient secrets never logged
```

Apple Private Relay adds provider sender-domain/authentication configuration requirements when that path is materialized.

---

## 11. M6 / M7

```text
M6 — Native Mobile Access
PLANNED

M7 — final whole-vertical security/observability/account-management/handoff gate
PLANNED
```

M7 owns the complete user-facing session/device/security-management layer, new-login alerts/“this wasn’t me”, full observability and final whole-vertical acceptance, but M5 correctness-critical lifecycle cannot be deferred there.

---

## 12. Whole-vertical status

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