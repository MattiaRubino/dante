# DANTE — Access/Auth Full-Stack Vertical Workstream

- **Status:** ACTIVE VERTICAL / M1–M4 CLOSED / M5 ACTIVE / GROUPS 1–3 COMPLETE / GROUP 4 ACTIVE CANDIDATE
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Last accepted execution block:** **GROUP 3 — M5-H + M5-I — COMPLETE / ENGINEERING PASS**
- **Group 4 PRE-SCOPE:** `a04009e645aa476af8a2b6ab1628142890b326d9`
- **Current Group 4 code checkpoint:** `4fd8068e1e51379f75c2bfaf59b46336f4e14637`
- **Current execution block:** **GROUP 4 — M5-J + M5-K+ — ACTIVE / ENGINEERING CANDIDATE / QA + UAT PENDING**
- **Accepted Alembic head:** `20260831_13`
- **M5 architecture authority:** `../architecture/access-auth-m5-contract.md`
- **M5 exact design authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **M5 live handoff:** `access-auth-m5-live-handoff-2026-08-29.md`
- **Forward execution authority:** `access-auth-m4-m7-execution-plan.md`

> New chat != new project, branch or worktree. Continue this vertical on `feature/access-auth` and `/home/mattia/projects/dante`. Do not restart Group 4 from scratch.

## 1. Mandatory continuation bootstrap

Read/verify in this order:

```text
docs/PROJECT-STATUS.md
→ docs/development/agent-operating-manual.md
→ docs/ROADMAP.md
→ this file
→ docs/workstreams/access-auth-m5-live-handoff-2026-08-29.md
→ docs/workstreams/access-auth-m4-m7-execution-plan.md
→ docs/architecture/access-auth-m5-contract.md
→ docs/architecture/access-auth-m5-persistence-api-contract.md
→ Access/Auth security/API/testing contracts + ADR-011
→ current Group-4 frontend/browser implementation/tests
```

Repository truth beats conversation memory. Do not reopen Groups 1–3 absent direct defect evidence.

## 2. Frozen Auth constitution

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived
provider identity = issuer + subject
provider email never silently links Accounts
provider auth != provider-data authorization
provider token/assertion != DANTE AuthSession
passwordless Account valid
PasskeyCredential != Account
WebAuthn user_handle = opaque Account binding
reauthentication != signin
frontend/provider/browser completion != backend-authoritative success
```

Forbidden without a separate gate: JWT/localStorage browser Auth, sessionStorage auth authority, Redis/JWT session authority, persisted Principal, silent provider-email merge, provider-specific Account/session authority, fake frontend success, raw generated-operation bypass, ad-hoc fetch proliferation, hand-rolled WebAuthn crypto, biometric/PIN/device-fingerprint persistence.

## 3. Closed foundation

```text
M1–M4                                                 CLOSED / ACCEPTED
M5.1 / M5.2                                           COMPLETE
M5-A persistence                                      COMPLETE / PG PROVEN
M5-B provider/crypto/WebAuthn infra                    COMPLETE / ENGINEERING PASS
M5-C Google backend                                   COMPLETE / ENGINEERING PASS
M5-D Apple backend/grant/notifications                COMPLETE / ENGINEERING PASS
GROUP 1 / M5-E + M5-G                                 COMPLETE / ENGINEERING PASS
GROUP 2 / M5-F                                        COMPLETE / ENGINEERING PASS
GROUP 3 / M5-H + M5-I                                 COMPLETE / ENGINEERING PASS
GROUP 4 / M5-J + M5-K+                                ACTIVE / CANDIDATE / QA PENDING
```

Accepted DB remains PostgreSQL 18.6 / Alembic `20260831_13`. Group 4 currently has no backend/DB/ACL delta.

## 4. Group 3 handoff authority

Group 3 closed the public HTTP/API-client contract. Relevant proof remains:

```text
35 focused HTTP/OpenAPI PASS
225 full non-PG PASS
2 continuation PG PASS
134 full PG PASS
11 governed-client tests PASS
generated determinism PASS / 78 files
workspace architecture/typecheck/build PASS
```

The frontend must consume the governed `@dante/api-client`; it must not rebuild protocol contracts or raw fetch wrappers beside it.

## 5. Group 4 current candidate

### Scope

```text
PRE-SCOPE
  a04009e645aa476af8a2b6ab1628142890b326d9

current code checkpoint
  4fd8068e1e51379f75c2bfaf59b46336f4e14637

PRE-SCOPE → checkpoint
  ahead 30 / behind 0
  21 changed paths
  all inside approved Web/i18n Group-4 scope
  no backend / DB / migration / ACL spill
```

### Materialized Web vertical

The existing Access React surface was extended rather than replaced. Current candidate includes:

```text
M3/M4 email-password/sign-up/recovery lifecycle retained
same-origin Web remote over governed @dante/api-client
VITE_DANTE_GOOGLE_CLIENT_ID public build configuration
Google official GIS renderButton lifecycle
DANTE Google begin before provider interaction
DANTE-issued transaction ref + state + nonce
Google credential callback passed directly to DANTE complete
backend outcome is sole authenticated/link/enrollment authority
Apple backend begin + safe redirect authority
Apple return to / or /security
provider continuation resolved only through HttpOnly flow cookies
provider enrollment set-email / resend / verify
provider link-required → existing Account auth → explicit confirm
browser WebAuthn conversion boundary only
navigator.credentials.create/get
no WebAuthn crypto verification in JS
passkey signin/register/reauth/update/remove
/security route
methods/password/provider/passkey management
password establish/remove
provider link/unlink
password/passkey reauthentication
IT/EN Group-4 copy
```

### Google correction

The earlier custom-button/programmatic-prompt direction was rejected during implementation. The candidate now uses Google Identity Services `renderButton`; DANTE performs `/google/begin` first to mint the bound transaction/nonce, the official Google button obtains credential evidence, and `/google/complete` decides the DANTE result.

Security linking intentionally uses a two-stage interaction: DANTE prepares an authenticated link transaction, then renders the official Google button with the DANTE nonce, then completes the link through the backend.

## 6. Candidate is not QA-pass yet

Do **not** claim Group 4 or M5 complete at `4fd8068e...`. No authoritative frontend QA has been recorded after the latest official-Google propagation.

Immediate next work:

```text
1. pull/sync current branch
2. run canonical Prettier + ESLint + TypeScript
3. run Web unit/component tests
4. run canonical TanStack route generation/build for /security
5. materialize routeTree.gen.ts only from generator output
6. fix all defects in assistant-owned code
7. complete missing approved Group-4 focused tests
8. extend web-auth-remote tests for M5 methods
9. create/complete access-m5 Playwright coverage
10. run HTTPS Chromium / Firefox / WebKit
11. accessibility / keyboard / focus / responsive checks
```

Focused approved tests still expected include provider browser, WebAuthn adapter, provider orchestration, passkey orchestration, methods, provider-flow panel, security page and M5 E2E coverage.

Only after engineering/browser QA is green should the user run real UAT:

```text
Google real
Apple registered-domain real
Apple Private Email Relay sender setup/proof
passkey real browser/authenticator
provider enrollment/link collision
security management
integrated manual Access M5
```

## 7. Branch/worktree safety

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not touch `main`, `feature/home-react`, `feature/access-frontend` or `/home/mattia/projects/dante-frontend` without explicit topology authorization.

A stray ref `tmp-not-used` exists at the Group-4 PRE-SCOPE only. It contains no feature work. Delete it when convenient with `git push origin --delete tmp-not-used`; never use it as an implementation branch.

## 8. M6 / M7

```text
M6 — FUTURE / OPTIONAL / ONLY IF DELIBERATELY RE-GATED
M7 — PLANNED / FINAL WHOLE-VERTICAL HARDENING + HANDOFF
```

Whole M5 remains ACTIVE until Group 4 browser/provider/passkey/manual acceptance is complete.
