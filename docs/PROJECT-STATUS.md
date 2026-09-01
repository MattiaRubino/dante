# DANTE — Project Status

- **Status:** CURRENT TRUTH FOR `feature/access-auth`
- **Last reconciled:** 2026-09-01
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active product vertical:** Access/Auth
- **Current macro-phase:** M5 — Multi-authenticator Account Layer — **ACTIVE**
- **Last accepted execution block:** **GROUP 3 — M5-H + M5-I — COMPLETE / ENGINEERING PASS**
- **Current execution block:** **GROUP 4 — M5-J + M5-K+ — Access Web + browser/provider/security/UAT — ACTIVE / ENGINEERING CANDIDATE / QA PENDING**
- **Group 4 PRE-SCOPE:** `a04009e645aa476af8a2b6ab1628142890b326d9`
- **Current Group 4 code checkpoint:** `4fd8068e1e51379f75c2bfaf59b46336f4e14637`
- **Accepted Alembic head:** `20260831_13`
- **Forward execution authority:** `workstreams/access-auth-m4-m7-execution-plan.md`
- **M5 exact design authority:** `architecture/access-auth-m5-persistence-api-contract.md`
- **M5 live handoff:** `workstreams/access-auth-m5-live-handoff-2026-08-29.md`

## 1. Current state

```text
Product / North Star                       CURRENT
Domain / Logical / Physical                CLOSED
Engineering + Frontend + Backend CP1–CP6  CLOSED / ACCEPTED
Access pre-backend Web materialization     CLOSED / ACCEPTED

M1 Visual / UX Freeze                      CLOSED / ACCEPTED
M2 Auth Architecture Freeze                CLOSED / QA PASS
M3 Email/Password + AuthSession            CLOSED / ENGINEERING PASS / USER ACCEPTED
M4 Lifecycle / Recovery / Reauth           CLOSED / ENGINEERING PASS / USER ACCEPTED

M5.1 architecture/external authority       COMPLETE
M5.2 persistence/API design                COMPLETE
M5-A persistence                           COMPLETE / POSTGRESQL PROVEN
M5-B provider/crypto/WebAuthn infra         COMPLETE / ENGINEERING PASS
M5-C Google backend                        COMPLETE / ENGINEERING PASS
M5-D Apple backend/grants/notifications    COMPLETE / ENGINEERING PASS
GROUP 1 M5-E+G lifecycle/passwordless      COMPLETE / ENGINEERING PASS
GROUP 2 M5-F passkeys                      COMPLETE / ENGINEERING PASS
GROUP 3 M5-H+I FastAPI/OpenAPI/client      COMPLETE / ENGINEERING PASS
GROUP 4 M5-J+K+ Access Web/UAT             ACTIVE / ENGINEERING CANDIDATE / QA PENDING

M6 Native Mobile                           FUTURE / OPTIONAL / ONLY IF RE-GATED
M7 Hardening/Observability/Handoff         PLANNED / FINAL WHOLE-VERTICAL GATE

Whole Access/Auth vertical                 ACTIVE / NOT CLOSED
```

The M5-E…M5-K+ labels are semantic ownership labels, not separate execution gates. The grouped execution above is authoritative.

## 2. Accepted engineering checkpoints

```text
M5-A persistence                           7e40e02d301b0812b3f55e0d9d4ce6439e420b2a
M5-B provider/runtime                      e2d40a7666e3c0130afecd8113b8063390b86b9d
M5-C Google backend                        e6f738a1ea3f5152caa7d99f1d6ccd108747c806
M5-D Apple backend                         7d13b712f032e8d41d7cf03d406555fd9f3c0160
GROUP 1                                    1c4b7c988eaae130d6a90d43940a42e2a550870d
GROUP 2 / M5-F                             f6a8da43fbe674ca18c366cd3731afc8f97ec045
GROUP 3 PRE-SCOPE                          ee099dc7c6bef4742c6e66e5d15f9a0428dd8ffa
GROUP 3 engineering checkpoint             05b348e9e0293cd9cd0cc3f190824527761b24d9
GROUP 4 PRE-SCOPE                          a04009e645aa476af8a2b6ab1628142890b326d9
GROUP 4 current code checkpoint            4fd8068e1e51379f75c2bfaf59b46336f4e14637
```

Group 4 is **not accepted yet**. `4fd8068e...` is a handoff/checkpoint, not a PASS claim.

## 3. Closed Group 2 / Group 3 proof

Group 2 / passkeys:

```text
Ruff / mypy                     PASS
non-PostgreSQL                  191 PASS
PostgreSQL                      132 PASS
total                           323 PASS
backend build                   PASS
scope audit                     PASS
```

Group 3 / public API + governed client:

```text
uv lock / Ruff / mypy           PASS
focused M5 HTTP/OpenAPI          35 PASS
full non-PostgreSQL             225 PASS
provider-continuation PG          2 PASS
full PostgreSQL                 134 PASS
backend build                   PASS
api-client lint/typecheck       PASS
api-client tests                 11 PASS
generated determinism           PASS / 78 files
architecture                    PASS / 151 modules / 287 dependencies
workspace typecheck             PASS / 6 of 6
workspace build                 PASS / 2 of 2
scope / clean-tree audit        PASS
```

Do not reopen Groups 2–3 absent direct defect evidence.

## 4. Group 4 materialized candidate

PRE-SCOPE `a04009e6...` → code checkpoint `4fd8068e...` is ahead-only by 30 commits and contains 21 Web/i18n paths, all within the approved Group-4 macro-scope. No backend, DB, migration, ACL or unrelated frontend path entered the delta.

Materialized direction now includes:

```text
governed Web remote over @dante/api-client
Google build-time public client-id configuration
Google official GIS renderButton flow
DANTE /google/begin transaction + nonce before Google credential
DANTE /google/complete as the only Google success authority
Apple backend begin + fixed redirect return target
HttpOnly provider enrollment/link continuation resume
provider enrollment email/verify/resend
provider collision → existing Account auth → explicit confirm
browser WebAuthn JSON/Base64URL ↔ ArrayBuffer adapter only
navigator.credentials.create/get; no frontend crypto verification
passkey signin / register / reauth / rename / remove
/security route
methods/password lifecycle
provider link/unlink
password establish/remove
password/passkey reauthentication
Security link from authenticated Access return
IT/EN Group-4 copy
```

Google was corrected during implementation: DANTE no longer tries to launch Google One Tap/programmatic prompt from a custom Google button. The current design uses the official Google Identity Services rendered button (`renderButton`) with the DANTE-issued nonce.

## 5. Group 4 still pending before UAT

No authoritative QA has yet been recorded for `4fd8068e...` after the official-Google lifecycle propagation. Therefore the following remain mandatory:

```text
pull exact candidate
canonical Prettier/ESLint/typecheck
web unit/component tests
fix any TS/lint/test regressions
canonical TanStack route generation so /security enters routeTree.gen.ts
materialize generator-owned routeTree only through the canonical generator
complete the approved focused Group-4 tests still missing
extend Web remote tests
create/complete Group-4 Playwright M5 coverage
Chromium / Firefox / WebKit HTTPS stack proof
accessibility/keyboard/focus/responsive checks
then real Google UAT
real Apple registered-domain UAT
Apple Private Email Relay sender setup/proof
real passkey/browser/authenticator UAT
manual integrated user UAT
```

Only after those proofs may Group 4 and whole M5 be declared closed.

## 6. Database truth

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

Group 4 is Web-only unless direct defect evidence justifies a separately gated backend/DB change.

## 7. Binding Auth constitution

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived
provider identity = issuer + subject
provider email != link/ownership authority
provider token/assertion != DANTE AuthSession
PasskeyCredential != Account
WebAuthn user_handle = opaque Account binding
passwordless Account valid
reauthentication != signin
frontend/provider/browser completion != backend-authoritative success
```

Forbidden without a new architecture gate: JWT/localStorage browser Auth, sessionStorage auth authority, persisted Principal, silent provider-email merge, provider-specific Account/session authority, fake frontend Auth success, raw generated-operation bypass, ad-hoc fetch proliferation, hand-rolled WebAuthn crypto, biometric/PIN/device-fingerprint persistence.

## 8. Exact continuation pointer

Continue **Group 4**, from the existing implementation. Do not restart discovery or rebuild Access from scratch.

First objective in the next chat:

```text
verify feature/access-auth HEAD
→ pull 4fd8068e... (or later docs-only handoff HEAD)
→ run canonical frontend generation/static/unit QA
→ fix defects in authorized Group-4 paths
→ complete missing focused tests/E2E
→ Chromium/Firefox/WebKit
→ real provider/passkey UAT
→ user UAT
→ only then Group 4 / M5 closure
```

A stray remote ref `tmp-not-used` exists and points to the Group-4 PRE-SCOPE only. It contains no feature changes and must not be used. Clean it with `git push origin --delete tmp-not-used` when convenient.

## 9. Branch/worktree safety

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not touch `main`, `feature/home-react`, `feature/access-frontend` or `/home/mattia/projects/dante-frontend` without explicit topology authorization.
