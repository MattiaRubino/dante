# DANTE — Access/Auth Full-Stack Vertical Workstream

- **Status:** ACTIVE VERTICAL / M1–M4 CLOSED / M5 ACTIVE / GROUPS 1–3 COMPLETE / GROUP 4 NEXT
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Last accepted execution block:** **GROUP 3 — M5-H + M5-I — COMPLETE / ENGINEERING PASS**
- **Group 3 PRE-SCOPE:** `ee099dc7c6bef4742c6e66e5d15f9a0428dd8ffa`
- **Group 3 engineering checkpoint:** `05b348e9e0293cd9cd0cc3f190824527761b24d9`
- **Current execution block:** **GROUP 4 — M5-J + M5-K+ — Access Web + browser/provider/security/UAT — NEXT**
- **Accepted Alembic head:** `20260831_13`
- **M5 architecture authority:** `../architecture/access-auth-m5-contract.md`
- **M5 exact design authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **M5 live handoff:** `access-auth-m5-live-handoff-2026-08-29.md`
- **Forward execution authority:** `access-auth-m4-m7-execution-plan.md`

> New chat != new project, branch or worktree. Continue this vertical on `feature/access-auth` and `/home/mattia/projects/dante` until whole Access/Auth closure or an explicit user topology gate.

## 1. Mandatory continuation bootstrap

Read/verify in this order:

```text
docs/PROJECT-STATUS.md
→ docs/development/agent-operating-manual.md
→ docs/ROADMAP.md
→ this file
→ docs/workstreams/access-auth-m5-live-handoff-2026-08-29.md
→ docs/architecture/access-auth-m5-contract.md
→ docs/architecture/access-auth-m5-persistence-api-contract.md
→ docs/workstreams/access-auth-m4-m7-execution-plan.md
→ Access/Auth architecture/security/API/testing contracts + ADR-011
→ DB System of Record + docs/database/access-auth.md + Dictionary where relevant
→ current Group-4 implementation/tests once materialized
```

Repository truth beats conversation memory. Do not reinterpret M1–M4 or reopen accepted M5 groups absent direct defect evidence.

No new branch/worktree, merge, rebase, force-push/history rewrite or protected-main write without explicit user authorization.

## 2. Frozen Auth constitution

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
PasskeyCredential = authenticator, not Account
WebAuthn user_handle = opaque discoverable binding
verification != setup completion
reauthentication != initial signin
frontend/provider/browser completion != backend-authoritative success
unknown/loading != signed-out/signed-in/error
method != factor != assurance
```

Do not reintroduce JWT/localStorage browser Auth, Redis/JWT session authority, Principal persistence, silent provider-email merge, provider-specific Account/session authority, Account advisory-lock replacement, wide credentialed CORS, fake frontend Auth success, persisted browser Auth cache, provider-profile dumping into Account, hand-rolled WebAuthn/COSE crypto or biometric/device-secret storage.

## 3. Closed foundation

```text
M1  Visual / UX Freeze                                  CLOSED / ACCEPTED
M2  Auth Architecture Freeze                           CLOSED / ACCEPTED / QA PASS
M3  Email/Password Signin + AuthSession Spine          CLOSED / ENGINEERING PASS / USER ACCEPTED
M4  Signup + Verification + Recovery + Reset + Reauth  CLOSED / ENGINEERING PASS / USER ACCEPTED

M5.1 architecture/external-authority freeze            COMPLETE
M5.2 exact persistence/API design                      COMPLETE
M5-A persistence foundations                           COMPLETE / REAL POSTGRESQL PROVEN
M5-B provider/JWK/JOSE/AEAD infrastructure             COMPLETE / ENGINEERING PASS
M5-C Google authentication                             COMPLETE / ENGINEERING PASS
M5-D Apple authentication + grant/notifications        COMPLETE / ENGINEERING PASS
GROUP 1 / M5-E + M5-G                                  COMPLETE / ENGINEERING PASS
GROUP 2 / M5-F                                         COMPLETE / ENGINEERING PASS
GROUP 3 / M5-H + M5-I                                  COMPLETE / ENGINEERING PASS
```

Accepted current DB truth:

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

`20260831_13` is ACL-only. Groups 2 and 3 required no schema/Alembic/Dictionary/ACL widening.

## 4. Group 2 accepted result

M5-F established WebAuthn/passkeys as a first-class direct authenticator under the Account-wide lifecycle and anti-lockout authority.

```text
real python-fido2 verification
opaque stable WebAuthn user_handle
registration / discoverable authentication / reauthentication
resident credentials required
UV required
multiple passkeys
credential lifetime uniqueness
COSE public-key persistence
monotonic credential-state handling
safe management projection
logical revoke
Account-wide anti-lockout
canonical DANTE AuthSession only
real PostgreSQL race proof
```

Closure:

```text
191 non-PostgreSQL PASS
132 PostgreSQL PASS
323 total PASS
Ruff / mypy / build / diff / scope PASS
```

Real browser/hardware WebAuthn acceptance remains Group 4.

## 5. Group 3 accepted result

M5-H + M5-I materialized the public HTTP contract and the governed client as one deterministic delivery pipeline:

```text
application services
→ exact FastAPI/Pydantic materialization
→ stable /api/v1 operationIds
→ RFC 9457 + no-store + request IDs
→ same-origin browser security + session CSRF
→ opaque HttpOnly provider continuation cookies
→ Apple bounded form_post external ingress
→ deterministic OpenAPI
→ Orval Fetch + generated Zod
→ governed @dante/api-client
→ strict runtime success validation
→ drift + two-run determinism proof
```

Public M5 surface includes methods/password, provider enrollment/link/unlink, Google, Apple and complete passkey lifecycle. Apple callback/notifications remain backend ingress and are not ordinary browser-client methods.

Closure evidence:

```text
Ruff / mypy                                      PASS
focused M5 HTTP/OpenAPI                          35 PASS
full non-PostgreSQL                              225 PASS
provider-continuation real PostgreSQL             2 PASS
full real PostgreSQL                             134 PASS
backend build                                    PASS
api-client lint / typecheck                       PASS
api-client Vitest                                 11 PASS
generated OpenAPI/Orval/Zod                       deterministic + current / 78 files
architecture check                                PASS / 151 modules / 287 dependencies
workspace typecheck                               PASS / 6 of 6
workspace build                                   PASS / 2 of 2
git diff + clean synced tree                      PASS
PRE-SCOPE scope audit                             PASS
```

Do not reopen Group 3 absent direct defect evidence.

## 6. Remaining M5 execution — authoritative grouping

```text
GROUP 1
M5-E + M5-G
Authenticator Lifecycle + Password/Passwordless Adaptation
COMPLETE / ENGINEERING PASS

GROUP 2
M5-F
WebAuthn / Passkeys
COMPLETE / ENGINEERING PASS

GROUP 3
M5-H + M5-I
Public FastAPI + Deterministic OpenAPI / Governed Client
COMPLETE / ENGINEERING PASS

GROUP 4 — CURRENT / NEXT
M5-J + M5-K+
Access Web + Security / Provider / Browser / UAT / Acceptance
NEXT
```

The labels M5-E/F/G/H/I/J/K+ remain semantic ownership labels from the frozen design; they are not independent execution gates.

## 7. Group 4 purpose

Group 4 is the next implementation block. It must consume the governed `@dante/api-client`; raw generated operations and ad-hoc fetch proliferation remain forbidden.

Materialize:

```text
email/password Access flows
Google begin/complete
Apple begin + returned callback outcome handling
passkey registration/authentication/reauthentication
provider enrollment
provider link-required + confirmation
methods/security management
loading/cancel/error/recovery states
backend-authoritative success only
no localStorage/sessionStorage auth authority
no frontend inference of provider success
```

Then prove:

```text
Chromium / Firefox / WebKit
real Google smoke/UAT
real Apple registered-domain smoke/UAT
Apple Private Email Relay sender configuration
real WebAuthn/passkey browser/hardware UAT
final browser/security/provider proof
manual integrated M5 UAT
docs reconciliation
explicit user acceptance
```

Whole M5 remains ACTIVE until Group 4 acceptance.

## 8. M6 / M7

```text
M6 — Native Mobile Access
FUTURE / OPTIONAL / ONLY IF DELIBERATELY RE-GATED

M7 — Security Hardening + Observability + Authenticated Handoff
PLANNED / FINAL WHOLE-VERTICAL GATE
```

## 9. Quality / testing posture

```text
prove each invariant at the truthful layer
focused proof during development
real PostgreSQL for persistence/race authority
real python-fido2 for WebAuthn crypto verification
no flaky Auth hidden behind retries
no blind retry of non-idempotent/ambiguous mutations
browser/provider proof only at the public/Web boundary
```

Local `uv==0.12.5` / Ruff behavior is authority. Never hand-edit `uv.lock`. The user runs requested QA; implementation/debug responsibility remains with the assistant.

## 10. Branch/worktree safety

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not touch `main`, `feature/home-react`, `feature/access-frontend` or `/home/mattia/projects/dante-frontend` without explicit topology authorization.
