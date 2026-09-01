# DANTE — Access/Auth M5 Live Handoff — 2026-09-01 Group 4

- **Status:** CURRENT CONTINUATION SAVE-GAME / GROUPS 1–3 COMPLETE / GROUP 4 ACTIVE ENGINEERING CANDIDATE / QA + UAT PENDING
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **Last accepted execution block:** **GROUP 3 — M5-H + M5-I — COMPLETE / ENGINEERING PASS**
- **Group 3 engineering checkpoint:** `05b348e9e0293cd9cd0cc3f190824527761b24d9`
- **Group 4 PRE-SCOPE:** `a04009e645aa476af8a2b6ab1628142890b326d9`
- **Group 4 current code checkpoint before these handoff-doc commits:** `4fd8068e1e51379f75c2bfaf59b46336f4e14637`
- **Accepted Alembic head:** `20260831_13`
- **Current execution block:** **GROUP 4 — M5-J + M5-K+ — Access Web + browser/provider/security/UAT**
- **Architecture authority:** `../architecture/access-auth-m5-contract.md`
- **Exact M5 design authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **Forward plan:** `access-auth-m4-m7-execution-plan.md`

> This file is the current save-game. A new chat must verify repository HEAD, read the current operational docs and continue this **existing Group-4 candidate**. Do not restart Access, do not create a new branch/worktree, do not reopen Groups 1–3 absent direct defect evidence, and do not claim M5 closed before browser/provider/passkey/manual UAT.

## 1. Mandatory topology

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not touch without a new explicit topology gate:

```text
main
feature/home-react
feature/access-frontend
/home/mattia/projects/dante-frontend
```

No merge, rebase, history rewrite, force push or main integration without explicit user authorization.

Before remote writes obey `docs/development/agent-operating-manual.md`: exact branch, PRE-SCOPE, exact CREATE/UPDATE/DELETE paths, purpose/out-of-scope, explicit approval, HEAD race-check and post-write compare.

Implementation/debug belongs to the assistant. The user runs QA/UAT commands and returns raw output; do not ask the user to hand-edit project source.

## 2. Mandatory new-chat read order

```text
docs/PROJECT-STATUS.md
→ docs/development/agent-operating-manual.md
→ docs/ROADMAP.md
→ docs/workstreams/access-auth.md
→ THIS FILE
→ docs/workstreams/access-auth-m4-m7-execution-plan.md
→ docs/architecture/access-auth-m5-contract.md
→ docs/architecture/access-auth-m5-persistence-api-contract.md
→ docs/architecture/access-auth-security-contract.md
→ docs/architecture/access-auth-api-contract.md
→ docs/architecture/access-auth-testing-contract.md
→ ADR-011
→ current Group-4 code/tests
```

The two M5 architecture contracts remain frozen design authority. Their historical progress metadata must not override the operational status recorded here/status/roadmap/execution-plan.

## 3. Permanent Auth constitution

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived, never persisted
multiple AuthSessions normal
provider identity = issuer + subject
provider email != Account/link authority
provider auth != provider-data grant
provider token/assertion != DANTE AuthSession
passwordless Account valid
PasskeyCredential != Account
WebAuthn user_handle = opaque Account binding
method != factor != assurance
reauthentication != signin
frontend/provider/browser completion != backend-authoritative success
```

Never reintroduce JWT/localStorage browser auth, sessionStorage auth authority, Redis/JWT session authority, silent provider-email merge, provider-specific Account/AuthSession authority, frontend auth cache as source of truth, provider SDK success as DANTE success, raw generated-operation bypass, ad-hoc auth fetch proliferation, hand-written WebAuthn crypto, or biometric/PIN/device-fingerprint persistence.

## 4. Closed state — do not reopen casually

```text
M1–M4                                      CLOSED / ACCEPTED
M5.1 / M5.2                                COMPLETE
M5-A                                       COMPLETE / REAL PG PROVEN
M5-B                                       COMPLETE / ENGINEERING PASS
M5-C Google backend                        COMPLETE / ENGINEERING PASS
M5-D Apple backend                         COMPLETE / ENGINEERING PASS
GROUP 1 / M5-E + M5-G                      COMPLETE / ENGINEERING PASS
GROUP 2 / M5-F                             COMPLETE / ENGINEERING PASS
GROUP 3 / M5-H + M5-I                      COMPLETE / ENGINEERING PASS
GROUP 4 / M5-J + M5-K+                     ACTIVE / CANDIDATE / QA PENDING
```

Accepted database remains PostgreSQL 18.6 / Alembic `20260831_13`. Group 4 has no backend/DB structural delta at this checkpoint.

Group 3 closure authority remains:

```text
35 focused HTTP/OpenAPI PASS
225 non-PG PASS
2 continuation PG PASS
134 full PG PASS
11 governed-client tests PASS
OpenAPI/Orval/Zod deterministic/current / 78 files
architecture/typecheck/build/scope PASS
```

## 5. Group 4 approved macro-scope

Group-4 PRE-SCOPE:

```text
a04009e645aa476af8a2b6ab1628142890b326d9
```

Current code checkpoint before handoff docs:

```text
4fd8068e1e51379f75c2bfaf59b46336f4e14637
```

PRE-SCOPE → code checkpoint:

```text
ahead 30
behind 0
21 changed files
all within approved Group-4 Web/i18n surface
no backend / DB / migration / ACL / unrelated frontend spill
```

Authorized implementation ownership includes existing Access Web/platform auth/application/model/UI/CSS, Access E2E tests, i18n Access resources, and generator-owned `apps/web/src/routeTree.gen.ts`. Generator-owned output must never be hand-edited.

## 6. What is already materialized

### 6.1 Governed browser remote

`apps/web/src/platform/auth/web-auth-remote.ts` extends the existing M3/M4 Web boundary over `@dante/api-client` for:

```text
session/signin/logout
signup/verification/recovery/reset/reauth
methods
password establish/remove
Google begin/complete
Apple begin
provider enrollment get/set/resend/verify
provider link inspect/confirm
provider unlink
passkey registration begin/complete
passkey authentication begin/complete
passkey reauthentication begin/complete
passkey update/remove
```

It retains `credentials: same-origin`, `X-Dante-Client: web`, governed Accept header and exact CSRF header insertion for authenticated mutations. No parallel raw Auth API has been introduced.

### 6.2 Google browser boundary — IMPORTANT

`apps/web/src/platform/auth/web-auth-provider.ts` loads Google Identity Services and renders the **official Google button**.

Current frozen browser flow:

```text
DANTE /google/begin
→ ExternalAuthTransaction + state + DANTE nonce
→ Google GIS initialize(client_id, nonce, callback)
→ google.accounts.id.renderButton(...)
→ Google credential callback
→ DANTE /google/complete
→ backend returns authenticated | link_required | enrollment_required
```

Do **not** replace this with a custom Google button that calls `google.accounts.id.prompt()`. That earlier direction was intentionally corrected before UAT.

Google public build configuration:

```text
VITE_DANTE_GOOGLE_CLIENT_ID
```

It is a public browser identifier, not a secret or DANTE authority.

Signin/signup currently prepare the DANTE Google transaction while the Google-capable Access surface is visible, then render the official button with the DANTE nonce. GIS initialization failure exposes a provider error without disabling password/passkey signin.

Security Google linking intentionally uses two stages:

```text
user selects Link Google
→ DANTE authenticated /google/begin purpose=link + CSRF
→ official GIS button rendered with DANTE nonce
→ credential callback
→ DANTE /google/complete
→ only authenticated backend result is accepted as linked
```

### 6.3 Apple browser boundary

```text
DANTE /apple/begin
→ validate returned authorization URL authority
→ redirect only to https://appleid.apple.com
→ Apple form_post handled by backend
→ backend fixed return target / or /security
```

No Apple state/link/enrollment secret becomes localStorage/sessionStorage or JavaScript authority.

### 6.4 Provider continuation

Provider enrollment/link continuation is resumed by asking the backend. Raw continuation capability remains in Secure HttpOnly flow cookies and is never made browser-readable.

Materialized:

```text
provider enrollment email entry
OTP verification/resend
provider collision → link_required
password or passkey authentication of existing Account
explicit provider-link confirmation
```

### 6.5 Passkey browser boundary

`web-auth-webauthn.ts` owns only browser representation conversion:

```text
Base64URL ↔ ArrayBuffer
PublicKeyCredential creation/request option adaptation
navigator.credentials.create/get
browser credential evidence → governed request JSON
```

It does not perform cryptographic verification or persist credential/private material. Backend `python-fido2` remains the security authority.

Materialized flows:

```text
passkey signin
registration
reauthentication
rename
logical remove
```

### 6.6 Security surface

`/security` exists in source and materializes:

```text
method inventory
password establish/remove
password reauth
passkey reauth
passkey register/rename/remove
Google link through official GIS button
Apple link through backend redirect
provider unlink
anti-lockout/backend error surfacing
```

Authenticated Access return links to `/security`.

### 6.7 i18n

M5/Group-4 Access copy is materially present in both:

```text
packages/i18n/src/resources/en/access.ts
packages/i18n/src/resources/it/access.ts
```

Final QA should still check that no new user-facing English literals remain where translations are expected; `AccessSecurityPage` currently contains some inherited hard-coded English error fallback text worth polishing if lint/tests/UX review expose it.

## 7. Last refactor completed before this handoff

The prior saturated chat stopped at commit:

```text
0f5f55941185cdba849e81c9700ed519e989e5a6
fix(auth-web): use official Google button on sign-in
```

At that point `auth-provider.ts` had already moved to the new official-Google preparation/completion lifecycle, but `AccessPage`, `AccessFlowPanel` and `AccessSecurityPage` still referenced the removed old `useProviderAuthenticationMutation` API.

That incompatibility has now been propagated and removed in the current checkpoint. Relevant continuation commits include:

```text
da9fee58  expose Google button lifecycle state
b9ba628e  distinguish unavailable Google state
a3e05cff  propagate official provider controls
1027fe82  complete provider lifecycle propagation
a50c9778  complete official Google security link
d37ec2f0  align sign-in provider test contract
98225d96  align flow-panel provider props
4fd8068e  remove DOM matcher dependency
```

The code is now a coherent handoff candidate by inspection, but this **is not equivalent to a successful compiler/test run**.

## 8. Mandatory next step — engineering QA before UAT

No authoritative local QA has yet been recorded for `4fd8068e...` after the Google propagation. The next chat must start here.

Recommended first local run:

```bash
cd /home/mattia/projects/dante

git pull --ff-only
git status --short --branch
git rev-parse HEAD

corepack pnpm --filter @dante/web exec prettier --write \
  src/platform/auth \
  src/features/access \
  src/routes/security.tsx

corepack pnpm --filter @dante/web lint
corepack pnpm --filter @dante/web typecheck
corepack pnpm --filter @dante/web test
corepack pnpm --filter @dante/web build

cd /home/mattia/projects/dante
git diff --check
git status --short --branch
git diff --name-status
git diff --stat
```

Interpretation rules:

```text
- user does not hand-fix source
- assistant diagnoses and fixes code on feature/access-auth
- formatter/generator output is materialized canonically, never manually reconstructed
- if build regenerates routeTree.gen.ts, inspect and commit exact generated output only
- do not claim browser/UAT acceptance from unit tests
```

Potential first-run areas to inspect if they fail:

```text
AccessPage useEffect dependency around prepareGoogleMutation
GoogleAuthenticationBegun.nonce exact generated typing
existing tests that still assume old provider-button selectors
Prettier normalization in access-flow-panel.tsx
routeTree.gen.ts lacking /security until canonical generation
```

Do not preemptively rewrite working code merely because these are risk areas; let static/test evidence decide.

## 9. Missing/unfinished approved focused tests

The original Group-4 macro-gate also approved these tests; several are not yet materialized and must be added only with meaningful invariant coverage:

```text
apps/web/src/platform/auth/web-auth-provider.test.ts
apps/web/src/platform/auth/web-auth-webauthn.test.ts
apps/web/src/features/access/application/auth-provider.test.ts
apps/web/src/features/access/application/auth-passkey.test.ts
apps/web/src/features/access/application/auth-methods.test.ts
apps/web/src/features/access/ui/access-provider-flow-panel.test.tsx
apps/web/src/features/access/ui/access-security-page.test.tsx
apps/web/e2e/auth/access-m5.spec.ts
```

Also extend/update as justified:

```text
apps/web/src/platform/auth/web-auth-remote.test.ts
apps/web/e2e/auth/access-auth.spec.ts
packages/i18n/src/index.test.ts
```

Do not create test files merely to satisfy an inventory. Prove the actual provider/passkey/security/browser invariants.

## 10. Route generation

`apps/web/src/routes/security.tsx` exists, but `apps/web/src/routeTree.gen.ts` is generator-owned. It may still be stale at handoff.

Rule:

```text
run canonical TanStack Router/Vite generation/build
→ inspect routeTree.gen.ts
→ materialize exact generator output
```

Never hand-edit the generated route tree.

## 11. Browser QA after static/unit green

Use the existing HTTPS auth Playwright harness:

```text
apps/web/playwright.auth.config.ts
Chromium / Firefox / WebKit
```

Prove truthful browser behavior for:

```text
session bootstrap
email/password regression
signup/recovery/reauth regression
same-origin credentials
CSRF/browser-security behavior
provider loading/error states
provider continuation resume
provider collision/link confirmation
/security authenticated gating
methods/password/provider/passkey management
passkey browser-boundary behavior where automation can prove it
accessibility / keyboard / focus / responsive behavior
```

Do not fake Google/Apple success and report it as real provider acceptance.

## 12. Real UAT — user-facing acceptance gate

Only after engineering/browser QA is green, begin real user UAT:

```text
Google real account smoke/UAT
Apple registered-domain smoke/UAT
Apple Private Email Relay sender setup/proof
real browser/authenticator passkey UAT
provider enrollment with real mailbox
existing-email collision → link-required → explicit confirm
Security password/provider/passkey lifecycle
reauth password/passkey
integrated manual Access M5 flow
```

Whole Group 4 / M5 closes only after explicit user acceptance.

## 13. Accidental remote ref cleanup

A remote branch/ref exists:

```text
tmp-not-used
```

It points only to Group-4 PRE-SCOPE `a04009e6...`; it contains no feature changes and never touched `feature/access-auth` history.

The connector does not expose a delete-ref action. Clean it from the local worktree when convenient:

```bash
git push origin --delete tmp-not-used
```

Do not use or merge it.

## 14. Branch/worktree safety

Continue exactly:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

No new branch/worktree merely because there is a new chat. Do not touch other workstreams.

## 15. Exact continuation pointer

The next assistant should **not ask what to do next**. It should:

```text
1. verify current feature/access-auth HEAD and clean/sync status
2. read the current operational docs + frozen M5 authorities
3. run/interpret the canonical frontend QA above
4. fix all concrete static/unit/build defects in approved Group-4 paths
5. materialize canonical route generation/formatter output
6. complete meaningful missing focused tests
7. run Chromium/Firefox/WebKit auth E2E
8. only then guide real Google/Apple/passkey/user UAT
9. close Group 4/M5 only on actual evidence
```

Do not reopen backend/DB unless a concrete Group-4 failure proves an authority defect.
