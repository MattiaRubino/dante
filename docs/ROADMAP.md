# DANTE Roadmap

- **Status:** CURRENT FOR `feature/access-auth`
- **Last reconciled:** 2026-09-01
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active vertical:** Access/Auth
- **Current macro-phase:** M5 — Multi-authenticator Account Layer — **ACTIVE**
- **Last accepted execution block:** **GROUP 3 — M5-H + M5-I — COMPLETE / ENGINEERING PASS**
- **Current execution block:** **GROUP 4 — M5-J + M5-K+ — NEXT**
- **Group 3 PRE-SCOPE:** `ee099dc7c6bef4742c6e66e5d15f9a0428dd8ffa`
- **Group 3 engineering checkpoint:** `05b348e9e0293cd9cd0cc3f190824527761b24d9`

## 1. Current sequence

```text
Product / North Star
        CURRENT
          ↓
Domain / Logical / Pre-Physical / Physical
        CLOSED
          ↓
Engineering + Frontend + Backend CP1–CP6
        CLOSED / ACCEPTED
          ↓
Access pre-backend Web materialization
        CLOSED / ACCEPTED
          ↓
M1 — Visual / UX Freeze
        CLOSED / ACCEPTED
          ↓
M2 — Auth Architecture Freeze
        CLOSED / ACCEPTED / QA PASS
          ↓
M3 — Email/Password Signin + AuthSession Spine
        CLOSED / ENGINEERING PASS / USER ACCEPTED
          ↓
M4 — Signup + Verification + Recovery + Reset + Reauth
        CLOSED / ENGINEERING PASS / USER ACCEPTED
          ↓
M5.1 — External Authority + Architecture Freeze
        COMPLETE
          ↓
M5.2 — Exact Persistence + API Design
        COMPLETE
          ↓
M5-A — Persistence Foundations
        COMPLETE / REAL POSTGRESQL PROVEN
          ↓
M5-B — Provider/JWK/JOSE/AEAD Infrastructure
        COMPLETE / ENGINEERING PASS
          ↓
M5-C — Google Authentication
        COMPLETE / ENGINEERING PASS
          ↓
M5-D — Apple Authentication + Grant Lifecycle
        COMPLETE / ENGINEERING PASS
          ↓
GROUP 1 — M5-E + M5-G
Authenticator Lifecycle + Password/Passwordless
        COMPLETE / ENGINEERING PASS
          ↓
GROUP 2 — M5-F
WebAuthn / Passkeys
        COMPLETE / ENGINEERING PASS
          ↓
GROUP 3 — M5-H + M5-I
Public FastAPI + Deterministic OpenAPI / Governed Client
        COMPLETE / ENGINEERING PASS
          ↓
GROUP 4 — M5-J + M5-K+
Access Web + Security / Provider / Browser / UAT / Acceptance
        NEXT
          ↓
M6 — Native Mobile Access
        FUTURE / OPTIONAL / ONLY IF RE-GATED
          ↓
M7 — Security Hardening + Observability + Authenticated Handoff
        PLANNED / FINAL WHOLE-VERTICAL GATE
```

The historical labels `M5-E` through `M5-K+` remain the frozen semantic decomposition used by the architecture/API contract. They are not separate execution gates. The grouped order above is authoritative.

## 2. Accepted M5 foundation

```text
M5-A persistence checkpoint
7e40e02d301b0812b3f55e0d9d4ce6439e420b2a

M5-B provider/runtime checkpoint
e2d40a7666e3c0130afecd8113b8063390b86b9d

M5-C Google checkpoint
e6f738a1ea3f5152caa7d99f1d6ccd108747c806

M5-D Apple checkpoint
7d13b712f032e8d41d7cf03d406555fd9f3c0160

GROUP 1 / M5-E + M5-G
1c4b7c988eaae130d6a90d43940a42e2a550870d

GROUP 2 / M5-F
f6a8da43fbe674ca18c366cd3731afc8f97ec045

GROUP 3 / M5-H + M5-I PRE-SCOPE
ee099dc7c6bef4742c6e66e5d15f9a0428dd8ffa

GROUP 3 engineering checkpoint
05b348e9e0293cd9cd0cc3f190824527761b24d9
```

Current accepted DB truth remains:

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

No Group 2 or Group 3 schema/Alembic/Dictionary/ACL widening was required.

## 3. Group 2 — COMPLETE

**M5-F — WebAuthn / Passkeys**

Accepted engineering result:

```text
real python-fido2 verifier
resident credential + UV required
discoverable username-less signin
stable opaque WebAuthn user_handle
registration / authentication / reauthentication
multiple passkeys
safe management projection
label update + logical revoke
Account-wide anti-lockout
canonical DANTE AuthSession only
bounded challenge/rate/resource policy
real PostgreSQL race/concurrency proof
```

Closure evidence:

```text
Ruff / mypy                     PASS
non-PostgreSQL                  191 PASS
PostgreSQL                      132 PASS
total                           323 PASS
backend build                   PASS
scope audit                     PASS
```

Real HTTPS browser/hardware WebAuthn acceptance remains Group 4.

## 4. Group 3 — COMPLETE

**M5-H + M5-I — Public FastAPI + Deterministic OpenAPI / Governed Client**

Accepted result:

```text
full frozen public M5 Auth route inventory
stable /api/v1 operationIds
Pydantic/FastAPI materialization
RFC 9457 typed problems
request IDs + no-store
Origin + Fetch Metadata + X-Dante-Client
session-bound CSRF
opaque HttpOnly provider continuation cookies
Google begin/complete
Apple begin + bounded form_post callback + notifications
provider enrollment/link/unlink
password lifecycle
passkey HTTP lifecycle
safe passkey management projection
deterministic OpenAPI
Orval Fetch + generated Zod
governed @dante/api-client
strict payload-widening rejection
generated drift + two-run determinism proof
```

Closure evidence:

```text
uv lock --check                        PASS / 57 packages
Ruff                                  PASS
mypy                                  PASS / 56 source files
focused HTTP/OpenAPI                  35 PASS
full non-PostgreSQL                   225 PASS
provider continuation PostgreSQL      2 PASS
full PostgreSQL                       134 PASS
backend build                         PASS
api-client lint/typecheck             PASS
api-client tests                      11 PASS
generated drift/determinism           PASS / 78 files
architecture check                    PASS / 151 modules / 287 dependencies
workspace typecheck                   PASS / 6 of 6 packages
workspace build                       PASS / 2 of 2 build tasks
clean/synced worktree                 PASS
scope audit                           PASS
```

Do not reopen Group 3 absent direct defect evidence.

## 5. Group 4 — NEXT

**M5-J + M5-K+ — Access Web + Final M5 Proof / Acceptance**

One macro-block with two internal responsibilities:

```text
A. Web materialization
   email/password + provider + passkey flows
   provider enrollment
   link-required + confirm
   methods/security management
   loading/cancel/error/recovery states
   backend-authoritative success only
   no browser auth cache/localStorage authority

B. Final acceptance
   Chromium / Firefox / WebKit
   real Google smoke/UAT
   real Apple registered-domain smoke/UAT
   Apple Private Email Relay sender configuration
   real WebAuthn/passkey UAT
   final security/provider/browser proof
   manual integrated M5 UAT
   docs reconciliation
   explicit user acceptance
```

M5 cannot close before Group 4 acceptance.

## 6. M6 / M7

```text
M6 — Native Mobile Access
FUTURE / OPTIONAL / ONLY IF DELIBERATELY RE-GATED

M7 — Security Hardening + Observability + Authenticated Handoff
PLANNED / FINAL WHOLE-VERTICAL GATE
```

M7 owns complete production hardening, observability and authenticated handoff. It does not absorb unfinished M5 browser/provider acceptance.

## 7. Current authorities

```text
docs/PROJECT-STATUS.md
docs/architecture/access-auth-m5-contract.md
docs/architecture/access-auth-m5-persistence-api-contract.md
docs/workstreams/access-auth.md
docs/workstreams/access-auth-m5-live-handoff-2026-08-29.md
docs/workstreams/access-auth-m4-m7-execution-plan.md
```

The M5 architecture contracts remain frozen design authority. Repository truth beats conversation memory. New chat != new branch/worktree.
