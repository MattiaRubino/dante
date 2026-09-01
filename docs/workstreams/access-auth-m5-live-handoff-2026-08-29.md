# DANTE — Access/Auth M5 Live Handoff — 2026-08-29

- **Status:** CURRENT CONTINUATION SAVE-GAME / GROUPS 1–3 COMPLETE / GROUP 4 NEXT
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **Last accepted execution block:** **GROUP 3 — M5-H + M5-I — COMPLETE / ENGINEERING PASS**
- **Group 3 PRE-SCOPE:** `ee099dc7c6bef4742c6e66e5d15f9a0428dd8ffa`
- **Group 3 engineering checkpoint:** `05b348e9e0293cd9cd0cc3f190824527761b24d9`
- **Accepted Alembic head:** `20260831_13`
- **Current execution block:** **GROUP 4 — M5-J + M5-K+ — Access Web + browser/provider/security/UAT — NEXT**
- **Architecture authority:** `../architecture/access-auth-m5-contract.md`
- **Exact M5 design authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **Forward plan:** `access-auth-m4-m7-execution-plan.md`

> This file is the current save-game. A new chat must reconstruct state from repository truth, verify the current branch HEAD, then continue with Group 4. Do not restart Group 2/3, do not reopen accepted backend work absent direct defect evidence, and do not claim whole-M5 acceptance before Group 4 browser/provider/passkey UAT is complete.

## 1. Mandatory continuation topology

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

New chat != new project, branch or worktree.

Do not touch without a new explicit topology/write gate:

```text
main
feature/home-react
feature/access-frontend
/home/mattia/projects/dante-frontend
```

No merge, rebase, history rewrite, force push or main integration without explicit user authorization.

Before remote writes obey `docs/development/agent-operating-manual.md`: exact branch, PRE-SCOPE SHA, exact CREATE/UPDATE/DELETE paths, purpose/out-of-scope, explicit approval, HEAD race-check and post-write compare.

## 2. Mandatory read order in a new chat

```text
docs/PROJECT-STATUS.md
→ docs/development/agent-operating-manual.md
→ docs/ROADMAP.md
→ docs/workstreams/access-auth.md
→ this file
→ docs/architecture/access-auth-m5-contract.md
→ docs/architecture/access-auth-m5-persistence-api-contract.md
→ docs/workstreams/access-auth-m4-m7-execution-plan.md
→ docs/architecture/access-auth-security-contract.md
→ docs/architecture/access-auth-api-contract.md
→ docs/architecture/access-auth-testing-contract.md
→ ADR-011 and relevant DB authority
→ docs/database/access-auth.md + Database System of Record + Dictionary as needed
→ current Group-4 frontend/browser implementation once materialized
```

Repository truth beats conversation memory. The M5 architecture contracts remain frozen design authority; current operational state lives in this handoff/status/roadmap/execution plan.

## 3. Permanent Auth constitution — do not reinterpret

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal is runtime-derived, never persisted
multiple independent AuthSessions are normal
provider identity key = issuer + subject
provider email != Account/link authority
provider authentication != provider-data authorization
provider assertion/token != DANTE AuthSession
passwordless Account is valid
PasskeyCredential = authenticator, not Account
WebAuthn user_handle = opaque discoverable Account binding
user_handle != email != account_ref
method != factor != assurance
reauthentication != initial signin
frontend/provider/browser completion != backend-authoritative success
```

Rejected unless separately re-gated:

```text
JWT/localStorage browser auth
Redis/JWT session authority
Principal persistence
generic auth/credential god table
silent provider-email merge
provider email as ExternalIdentity identity key
provider-specific Account/AuthSession authority
wide credentialed CORS
fake frontend auth success
hand-rolled WebAuthn/CBOR/COSE/signature crypto
biometric/PIN/device-fingerprint persistence
Account advisory-lock replacement
blind retry of non-idempotent/ambiguous auth mutations
```

## 4. Closed state — do not reopen casually

```text
M1  CLOSED / ACCEPTED
M2  CLOSED / ACCEPTED / QA PASS
M3  CLOSED / ENGINEERING PASS / USER ACCEPTED
M4  CLOSED / ENGINEERING PASS / USER ACCEPTED

M5.1 COMPLETE
M5.2 COMPLETE
M5-A COMPLETE / REAL POSTGRESQL PROVEN
M5-B COMPLETE / ENGINEERING PASS
M5-C COMPLETE / ENGINEERING PASS
M5-D COMPLETE / ENGINEERING PASS
GROUP 1 / M5-E + M5-G COMPLETE / ENGINEERING PASS
GROUP 2 / M5-F COMPLETE / ENGINEERING PASS
GROUP 3 / M5-H + M5-I COMPLETE / ENGINEERING PASS
```

Current accepted DB:

```text
PostgreSQL          18.6
Alembic             20260831_13
83 tables
5 views
15 routines
75 triggers
156 physical indexes
85 foreign keys
233 CHECK constraints
103 standalone Dictionary entries
```

`20260831_13` is ACL-only. No Group 2/3 schema shape, mapping, index, constraint, Dictionary or ACL widening was required.

## 5. Group 2 closure record

Group 2 / M5-F established passkeys under the existing Account/AuthSession authority and is closed at the engineering layer.

```text
real python-fido2 verification
resident credentials required
UV required
opaque discoverable WebAuthn user_handle
registration / signin / reauthentication
multiple passkeys
safe management projection
logical revoke
Account-wide anti-lockout
monotonic assertion-state handling
real PostgreSQL race/concurrency proof
canonical DANTE AuthSession only
```

Accepted evidence:

```text
Ruff / mypy                     PASS
non-PostgreSQL                  191 PASS
PostgreSQL                      132 PASS
total                           323 PASS
backend build                   PASS
scope audit                     PASS
```

Real browser/hardware WebAuthn acceptance remains Group 4.

## 6. Group 3 closure record

Group 3 / M5-H + M5-I materialized the frozen public Auth API and governed client.

### HTTP/security surface

```text
/api/v1 stable paths and operationIds
RFC 9457 typed problems
Cache-Control: no-store
request IDs
Origin + Fetch Metadata + X-Dante-Client
session-bound CSRF
Secure HttpOnly __Host-dante-session
opaque Secure HttpOnly provider enrollment/link cookies
Apple form_post callback isolated from ordinary browser mutations
Apple notification JSON ingress
bounded body/media-type handling
```

### Public M5 API

```text
GET    /api/v1/auth/methods
POST   /api/v1/auth/password/establish
DELETE /api/v1/auth/password

GET    /api/v1/auth/provider-enrollment
POST   /api/v1/auth/provider-enrollment/email
POST   /api/v1/auth/provider-enrollment/verify
POST   /api/v1/auth/provider-enrollment/resend

GET    /api/v1/auth/provider-link
POST   /api/v1/auth/provider-link/confirm
DELETE /api/v1/auth/providers/{external_identity_ref}

POST   /api/v1/auth/google/begin
POST   /api/v1/auth/google/complete

POST   /api/v1/auth/apple/begin
POST   /api/v1/auth/apple/callback
POST   /api/v1/auth/apple/notifications

POST   /api/v1/auth/passkeys/registration/begin
POST   /api/v1/auth/passkeys/registration/complete
POST   /api/v1/auth/passkeys/authentication/begin
POST   /api/v1/auth/passkeys/authentication/complete
POST   /api/v1/auth/passkeys/reauthentication/begin
POST   /api/v1/auth/passkeys/reauthentication/complete
PATCH  /api/v1/auth/passkeys/{passkey_credential_ref}
DELETE /api/v1/auth/passkeys/{passkey_credential_ref}
```

### Continuation authority

Provider flow cookies contain only raw high-entropy continuation capability. Provider code, challenge ref, Account/email/subject and routing metadata are not exposed as browser-readable authority. Capability resolution is server-side and purpose separated.

### Governed client

```text
FastAPI/Pydantic
→ deterministic OpenAPI snapshot
→ Orval Fetch
→ generated Zod
→ governed @dante/api-client
```

Raw generated Auth operations remain absent from the package root. Runtime success validation rejects unknown/widened metadata, including provider subject/continuation material and raw passkey credential metadata.

Apple callback and Apple notifications are backend ingress and are intentionally not normal browser-client methods.

### Accepted Group-3 evidence

```text
uv lock --check                        PASS / 57 packages
Ruff                                  PASS
mypy                                  PASS / 56 source files
focused M5 HTTP/OpenAPI               35 PASS
full non-PostgreSQL                   225 PASS
provider-continuation PostgreSQL      2 PASS
full PostgreSQL                       134 PASS
backend build                         PASS
api-client lint                       PASS
api-client typecheck                  PASS
api-client Vitest                     11 PASS
generated drift + determinism         PASS / 78 files
architecture check                    PASS / 151 modules / 287 dependencies
workspace typecheck                   PASS / 6 of 6 packages
workspace build                       PASS / 2 of 2 build tasks
git diff + clean/synced tree          PASS
scope audit                           PASS
```

Group 3 PRE-SCOPE:

```text
ee099dc7c6bef4742c6e66e5d15f9a0428dd8ffa
```

Group 3 engineering checkpoint:

```text
05b348e9e0293cd9cd0cc3f190824527761b24d9
```

Do not reopen this block absent direct defect evidence.

## 7. Current execution pointer — Group 4

```text
GROUP 4 — M5-J + M5-K+
Access Web + Final Security / Provider / Browser / UAT Acceptance
NEXT
```

The next assistant should work from the existing Access UI/UX authority and the governed `@dante/api-client`, not create another auth architecture.

Materialize:

```text
email/password flows
Google
Apple
passkeys
provider enrollment
provider collision/link-required + confirm
methods/security management
password/passkey/provider management
loading/cancel/error/recovery states
backend-authoritative success only
```

Do not create browser auth authority in localStorage/sessionStorage, do not infer DANTE authentication from provider SDK success and do not bypass the governed client with parallel raw fetch helpers.

## 8. Group 4 final acceptance

M5 cannot close before:

```text
Chromium / Firefox / WebKit proof
real Google smoke/UAT
real Apple registered-domain smoke/UAT
Apple Private Email Relay sender setup
real WebAuthn/passkey browser/hardware UAT
provider enrollment/link collision proof
reauth + authenticator-management proof
same-origin/session/CSRF behavior in real browser
manual integrated M5 UAT
final docs reconciliation
explicit user acceptance
```

## 9. M6 / M7

```text
M6 — Native Mobile Access
FUTURE / OPTIONAL / ONLY IF DELIBERATELY RE-GATED

M7 — Security Hardening + Observability + Authenticated Handoff
PLANNED / FINAL WHOLE-VERTICAL GATE
```

## 10. Branch/worktree safety

Continue exactly unless explicitly changed by the user:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not touch `main`, `feature/home-react`, `feature/access-frontend` or `/home/mattia/projects/dante-frontend` without a new explicit topology/write gate.
