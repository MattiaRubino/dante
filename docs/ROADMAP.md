# DANTE Roadmap

- **Status:** CURRENT FOR `feature/access-auth`
- **Last reconciled:** 2026-09-01
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active vertical:** Access/Auth
- **Current macro-phase:** M5 — Multi-authenticator Account Layer — **ACTIVE**
- **Last accepted execution block:** **GROUP 3 — M5-H + M5-I — COMPLETE / ENGINEERING PASS**
- **Current execution block:** **GROUP 4 — M5-J + M5-K+ — ACTIVE / ENGINEERING CANDIDATE / QA + UAT PENDING**
- **Group 4 PRE-SCOPE:** `a04009e645aa476af8a2b6ab1628142890b326d9`
- **Current Group 4 code checkpoint:** `4fd8068e1e51379f75c2bfaf59b46336f4e14637`

## 1. Current sequence

```text
Product / North Star
        CURRENT
          ↓
Domain / Logical / Physical
        CLOSED
          ↓
Engineering + Frontend + Backend CP1–CP6
        CLOSED / ACCEPTED
          ↓
Access pre-backend Web materialization
        CLOSED / ACCEPTED
          ↓
M1–M4 Access/Auth
        CLOSED / ACCEPTED
          ↓
M5.1 / M5.2 / M5-A–D
        COMPLETE
          ↓
GROUP 1 — M5-E + M5-G
        COMPLETE / ENGINEERING PASS
          ↓
GROUP 2 — M5-F Passkeys
        COMPLETE / ENGINEERING PASS
          ↓
GROUP 3 — M5-H + M5-I FastAPI/OpenAPI/Client
        COMPLETE / ENGINEERING PASS
          ↓
GROUP 4 — M5-J + M5-K+
Access Web + Security / Provider / Browser / UAT
        ACTIVE / ENGINEERING CANDIDATE / QA PENDING
          ↓
M5 closure
        BLOCKED ON GROUP 4 ACCEPTANCE
          ↓
M6 Native Mobile
        FUTURE / OPTIONAL / ONLY IF RE-GATED
          ↓
M7 Hardening / Observability / Authenticated Handoff
        PLANNED / FINAL WHOLE-VERTICAL GATE
```

The historical M5-E…M5-K+ labels remain semantic ownership labels. The grouped sequence above is authoritative.

## 2. Accepted foundation

```text
M5-A                                    7e40e02d301b0812b3f55e0d9d4ce6439e420b2a
M5-B                                    e2d40a7666e3c0130afecd8113b8063390b86b9d
M5-C                                    e6f738a1ea3f5152caa7d99f1d6ccd108747c806
M5-D                                    7d13b712f032e8d41d7cf03d406555fd9f3c0160
GROUP 1                                 1c4b7c988eaae130d6a90d43940a42e2a550870d
GROUP 2                                 f6a8da43fbe674ca18c366cd3731afc8f97ec045
GROUP 3 PRE-SCOPE                       ee099dc7c6bef4742c6e66e5d15f9a0428dd8ffa
GROUP 3 engineering checkpoint          05b348e9e0293cd9cd0cc3f190824527761b24d9
GROUP 4 PRE-SCOPE                       a04009e645aa476af8a2b6ab1628142890b326d9
GROUP 4 current code checkpoint         4fd8068e1e51379f75c2bfaf59b46336f4e14637
```

Accepted DB truth remains PostgreSQL 18.6 / Alembic `20260831_13`. Group 4 has introduced no backend/DB/ACL delta.

## 3. Closed Group 2 / Group 3

Group 2 / WebAuthn-passkeys is engineering-pass with 323 total backend tests across non-PG/PG and real `python-fido2` proof. Browser/hardware proof remains Group 4.

Group 3 delivered the complete public M5 API and governed client with:

```text
35 focused HTTP/OpenAPI PASS
225 full non-PG PASS
2 provider-continuation PG PASS
134 full PG PASS
11 api-client tests PASS
OpenAPI/Orval/Zod determinism PASS / 78 files
architecture/typecheck/build/scope PASS
```

Do not reopen Groups 2–3 absent direct defect evidence.

## 4. Group 4 — ACTIVE

### 4.1 Materialized candidate

PRE-SCOPE `a04009e6...` → checkpoint `4fd8068e...` is ahead-only by 30 commits and changes 21 approved Web/i18n paths only.

Materialized:

```text
existing M3/M4 email-password lifecycle retained
governed @dante/api-client Web boundary
Google public build configuration
Google official GIS renderButton lifecycle
DANTE begin transaction/nonce → GIS credential → DANTE complete
Apple begin + redirect return to Access/Security
provider enrollment via HttpOnly continuation cookie
provider collision/link-required + explicit confirmation
browser WebAuthn adapter without frontend crypto
passkey signin/register/reauth/rename/remove
/security route and authenticator inventory
password establish/remove
provider link/unlink
password + passkey reauthentication
IT/EN M5 copy
```

The Google implementation deliberately does **not** use a custom button to programmatically trigger Google One Tap. The official GIS rendered button is the browser interaction surface; DANTE remains the authentication authority.

### 4.2 Not yet accepted

No final frontend QA has been recorded after the latest Google propagation. Before any final UAT/closure:

```text
canonical Prettier + ESLint
TypeScript typecheck
unit/component tests
TanStack route generation for /security
materialize routeTree.gen.ts only through generator
complete missing approved Group-4 tests
extend Web remote tests
Group-4 Playwright M5 scenarios
Chromium / Firefox / WebKit HTTPS stack proof
accessibility / keyboard / focus / responsive proof
```

Then external/manual acceptance:

```text
real Google UAT
real Apple registered-domain UAT
Apple Private Email Relay sender configuration/proof
real passkey browser/authenticator UAT
provider enrollment/link collision UAT
security-management UAT
manual integrated user UAT
explicit user acceptance
```

M5 cannot close before these are complete.

## 5. Next execution

The next chat must **continue Group 4 from the existing candidate**, not start a new Web/Auth implementation.

Priority:

```text
sync branch
→ run canonical frontend generator/static/unit QA
→ fix candidate defects
→ complete focused tests/E2E
→ browser matrix
→ real provider/passkey UAT
→ user UAT
→ Group 4/M5 closure docs
```

A stray remote ref `tmp-not-used` points only to Group-4 PRE-SCOPE and contains no work. It is not part of the roadmap and should be deleted when convenient.

## 6. M6 / M7

```text
M6 — Native Mobile Access
FUTURE / OPTIONAL / ONLY IF DELIBERATELY RE-GATED

M7 — Security Hardening + Observability + Authenticated Handoff
PLANNED / FINAL WHOLE-VERTICAL GATE
```

## 7. Current authorities

```text
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/access-auth.md
docs/workstreams/access-auth-m5-live-handoff-2026-08-29.md
docs/workstreams/access-auth-m4-m7-execution-plan.md
docs/architecture/access-auth-m5-contract.md
docs/architecture/access-auth-m5-persistence-api-contract.md
```

The architecture contracts remain frozen design authority; operational status lives in the five status/workstream documents above.
