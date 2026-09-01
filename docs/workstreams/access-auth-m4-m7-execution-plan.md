# DANTE — Access/Auth M4–M7 Execution Plan

- **Status:** CURRENT EXECUTION PLAN / M4 CLOSED / M5 ACTIVE / GROUPS 1–3 COMPLETE / GROUP 4 ACTIVE CANDIDATE
- **Vertical:** Access/Auth
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **Current execution block:** **GROUP 4 — M5-J + M5-K+ — Access Web + Final Browser / Provider / Security / UAT**
- **Last accepted execution block:** **GROUP 3 — M5-H + M5-I — COMPLETE / ENGINEERING PASS**
- **Group 4 PRE-SCOPE:** `a04009e645aa476af8a2b6ab1628142890b326d9`
- **Current Group 4 code checkpoint:** `4fd8068e1e51379f75c2bfaf59b46336f4e14637`
- **Accepted Alembic head:** `20260831_13`
- **Architecture authority:** `../architecture/access-auth-m5-contract.md`
- **Exact M5 design authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **Live handoff:** `access-auth-m5-live-handoff-2026-08-29.md`

> This plan is the current execution authority. Implementation/debug responsibility belongs to the assistant. The user runs requested QA/UAT and returns raw output; do not push manual source debugging or patches onto the user.

## 1. Continuation rules

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Before remote writes follow `docs/development/agent-operating-manual.md`: exact PRE-SCOPE, exact paths, purpose/out-of-scope, explicit approval, branch race-check, post-write compare.

No merge/rebase/history rewrite/protected-main write without explicit authorization.

## 2. Frozen foundations

Reuse, do not replace:

```text
Account = durable security root
EmailIdentity separate from Account
PasswordCredential optional
Principal runtime-derived
opaque PostgreSQL-backed AuthSession
Secure HttpOnly host-only __Host-dante-session
session-bound CSRF
Origin + Fetch Metadata + X-Dante-Client
/api/v1 + RFC9457
FastAPI/Pydantic → deterministic OpenAPI → Orval/Zod → governed @dante/api-client
TanStack Query remote lifecycle
TanStack Router session bootstrap
real browser proof at Group-4 boundary
```

Permanent Auth rules:

```text
provider identity = issuer + subject
provider email != Account/link authority
provider assertion/token != DANTE AuthSession
passwordless Account valid
PasskeyCredential != Account
WebAuthn user_handle = opaque Account binding
provider/browser completion != backend authentication success
no blind mutation retry
```

## 3. Closed M5 implementation

```text
M5.1 / M5.2                                           COMPLETE
M5-A                                                  COMPLETE / PG PROVEN
M5-B                                                  COMPLETE / ENGINEERING PASS
M5-C Google backend                                   COMPLETE / ENGINEERING PASS
M5-D Apple backend                                    COMPLETE / ENGINEERING PASS
GROUP 1 / M5-E+G                                      COMPLETE / ENGINEERING PASS
GROUP 2 / M5-F                                        COMPLETE / ENGINEERING PASS
GROUP 3 / M5-H+I                                      COMPLETE / ENGINEERING PASS
```

Group 2 closed with 191 non-PG + 132 PG = 323 tests. Group 3 closed with 35 focused HTTP/OpenAPI, 225 non-PG, 2 continuation PG, 134 full PG, 11 client tests, deterministic 78-file OpenAPI/Orval/Zod generation and workspace architecture/typecheck/build proof.

Accepted DB remains PostgreSQL 18.6 / Alembic `20260831_13`.

## 4. GROUP 4 — ACTIVE

### 4.1 Purpose

Finish the actual Access Web vertical over the already-governed backend/client contract and prove it in real browsers/providers/authenticators before closing M5.

### 4.2 Current physical state

```text
PRE-SCOPE
  a04009e645aa476af8a2b6ab1628142890b326d9

current code checkpoint
  4fd8068e1e51379f75c2bfaf59b46336f4e14637

remote relation
  ahead 30 / behind 0

scope
  21 approved Web/i18n paths
  no backend / DB / Alembic / ACL spill
```

Current materialization:

```text
web-auth-remote over governed client
Google public build config
Google official GIS renderButton
DANTE begin transaction + nonce before Google credential
DANTE complete as sole Google outcome authority
Apple begin + redirect return target
HttpOnly provider continuation resume
provider enrollment
provider link-required + explicit confirm
WebAuthn browser conversion adapter
passkey signin/register/reauth/update/remove
/security route
methods/security management
password establish/remove
provider link/unlink
password/passkey reauth
IT/EN copy
```

### 4.3 Google browser rule — frozen for current candidate

Do not regress to custom-button `google.accounts.id.prompt()` flow.

```text
DANTE POST /google/begin
→ server-bound transaction/state/nonce
→ Google Identity Services official renderButton
→ credential callback
→ DANTE POST /google/complete
→ backend returns authenticated | link_required | enrollment_required
```

A Google SDK credential is evidence only. It is never DANTE authentication authority and is not persisted in browser storage.

Authenticated Security link uses the same model but intentionally begins with a DANTE “Link Google” preparation action before rendering the official Google button with the DANTE nonce.

### 4.4 Apple browser rule

```text
DANTE /apple/begin
→ browser redirect to appleid.apple.com only
→ Apple form_post to backend callback
→ backend continuation/redirect
→ fixed DANTE return target / or /security
```

No Apple transaction/link/enrollment capability becomes JavaScript storage authority.

### 4.5 Passkey browser rule

Frontend ownership is limited to:

```text
Base64URL ↔ ArrayBuffer
public WebAuthn JSON adaptation
navigator.credentials.create/get
bounded browser error handling
```

Cryptographic verification, credential authority and Account/AuthSession state remain backend-owned.

## 5. Engineering candidate QA — NEXT

`4fd8068e...` is **not yet QA-pass**. No authoritative local run has been recorded after official-Google propagation.

The next chat must first run and interpret:

```text
sync exact branch
canonical Prettier
ESLint
TypeScript typecheck
Web unit/component tests
canonical TanStack route generation/build
workspace architecture/typecheck/build as justified
```

The `/security` route exists in source, but `apps/web/src/routeTree.gen.ts` remains generator-owned and must be refreshed only through the canonical TanStack/Vite workflow. Never hand-edit it.

Missing/unfinished focused proof from the approved macro-gate must then be completed, especially:

```text
web-auth-provider.test.ts
web-auth-webauthn.test.ts
auth-provider.test.ts
auth-passkey.test.ts
auth-methods.test.ts
access-provider-flow-panel.test.tsx
access-security-page.test.tsx
web-auth-remote M5 coverage
access-m5.spec.ts
existing access-auth.spec.ts updates where contract changed
```

Do not mechanically create empty tests; each must prove a meaningful browser/application invariant.

## 6. Browser QA after static/unit green

Use the existing HTTPS Access/Auth Playwright harness and run:

```text
Chromium
Firefox
WebKit
```

Prove at minimum:

```text
critical session bootstrap
email/password lifecycle regression
Secure HttpOnly session behavior
CSRF/Origin/Fetch-Metadata behavior through real browser
provider loading/cancel/error states
provider continuation resume
link-required flow
/security authenticated gating
methods/password/provider/passkey management states
passkey browser-boundary behavior where automation can truthfully prove it
accessibility / keyboard / focus / responsive regressions
```

Do not fake Google/Apple/provider success in a way that is later reported as real provider acceptance.

## 7. Real UAT / final M5 acceptance

Only after engineering/browser QA is green:

```text
real Google smoke + user UAT
real Apple registered-domain smoke + user UAT
Apple Private Email Relay sender configuration/proof
real WebAuthn/passkey browser/authenticator UAT
provider enrollment collision/link-required UAT
reauth + security-management UAT
manual integrated Access M5 UAT
final docs reconciliation
explicit user acceptance
```

M5 closes only after Group 4 acceptance.

Backend/DB regressions should be rerun only if Group-4 work discovers a backend authority defect or changes backend code. Do not rerun heavy PostgreSQL suites mechanically for frontend-only fixes.

## 8. Scope / topology

Approved Group-4 work remains limited to the existing Access Web/platform auth/i18n/E2E/test surfaces and generator-owned `routeTree.gen.ts`, plus closure docs. No backend redesign or DB change is authorized by default.

A stray remote branch/ref `tmp-not-used` points to PRE-SCOPE `a04009e6...` and contains no changes. It is not an implementation branch. Delete with `git push origin --delete tmp-not-used` when convenient.

## 9. M6 / M7

```text
M6 — FUTURE / OPTIONAL / ONLY IF DELIBERATELY RE-GATED
M7 — PLANNED / FINAL WHOLE-VERTICAL HARDENING + OBSERVABILITY + HANDOFF
```

## 10. Current authorities

```text
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/access-auth.md
docs/workstreams/access-auth-m5-live-handoff-2026-08-29.md
docs/workstreams/access-auth-m4-m7-execution-plan.md
docs/architecture/access-auth-m5-contract.md
docs/architecture/access-auth-m5-persistence-api-contract.md
```

The M5 architecture contracts are frozen design authority; operational state is defined by the status/roadmap/workstream/handoff documents.
