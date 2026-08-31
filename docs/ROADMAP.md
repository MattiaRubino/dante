# DANTE Roadmap

- **Status:** CURRENT FOR `feature/access-auth`
- **Last reconciled:** 2026-08-31
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active vertical:** Access/Auth
- **Current macro-phase:** M5 — Multi-authenticator Account Layer — **ACTIVE**
- **Last completed slice:** M5-D — Apple Authentication + Grant / Notification Lifecycle — **COMPLETE / ENGINEERING PASS**
- **Next execution block:** **M5-E + M5-G — Authenticator Lifecycle + Password/Passwordless Adaptation**

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
        NEXT
          ↓
GROUP 2 — M5-F
WebAuthn / Passkeys
        PLANNED
          ↓
GROUP 3 — M5-H + M5-I
Public FastAPI + Deterministic OpenAPI / Governed Client
        PLANNED
          ↓
GROUP 4 — M5-J + M5-K+
Access Web + Security / Provider / Browser / UAT / Acceptance
        PLANNED
          ↓
M6 — Native Mobile Access
        PLANNED
          ↓
M7 — Security Hardening + Observability + Authenticated Handoff
        PLANNED / FINAL WHOLE-VERTICAL GATE
```

The historical labels `M5-E` through `M5-K+` remain the frozen semantic decomposition used by the architecture/API contract. They are no longer separate execution gates. The grouped order above is the only current execution order.

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

M5-D docs closure
1cc331851d52d39f42e922147f300e0370649670
```

Current DB truth remains:

```text
PostgreSQL          18.6
Alembic             20260830_12
83 tables
5 views
15 routines
75 triggers
156 physical indexes
85 foreign keys
233 CHECK constraints
103 standalone Dictionary entries
```

M5-D closeout evidence:

```text
uv lock --check                              PASS
Ruff format/check/lint                       PASS
mypy                                         PASS
backend fast                                 171 / 171 PASS
focused PostgreSQL M5-D                       9 / 9 PASS
full PostgreSQL regression                   111 / 111 PASS
backend build                                PASS
git diff --check                             PASS
scope audit                                  PASS
```

## 3. Group 1 — M5-E + M5-G — NEXT

**Authenticator Lifecycle + Password / Passwordless Adaptation**

These slices are executed together because anti-lockout, provider removal, password establishment/removal and recovery reachability are one Account-wide security problem.

Required result:

```text
provider-neutral authentication-method inventory
provider-first ExternalLinkChallenge confirmation
safe provider unlink / logical revoke
Apple grant revocation reconciliation when unlinking Apple
backend-authoritative direct-authenticator counting
Account security lock around authenticator mutations
anti-lockout recheck inside the authoritative transaction
verified/recovery-eligible EmailIdentity requirement for passwordless safety
establish first password using existing Argon2id/HIBP/pepper policy
safe remove password
M4 reset adapts to create-or-replace password
normal password mutation invalidates stale recovery proof
security-sensitive retained session rotates exact bearer
concurrent link/unlink/password mutations converge safely
operation-specific ambiguous-commit reconciliation only
```

No passkey implementation in Group 1. Passkeys join the same lifecycle through Group 2 after the provider/password model is stable.

## 4. Group 2 — M5-F

**WebAuthn / Passkeys**

```text
stable opaque WebAuthnAccount user_handle
registration begin/complete
discoverable username-less authentication
passkey reauthentication
multiple credentials
UV required / resident credential direction / attestation none
credential_id lifetime uniqueness
COSE algorithm persistence
signCount + backup state update policy
label/update/remove
logical revoke
same Account anti-lockout framework from Group 1
canonical DANTE AuthSession only
real HTTPS WebAuthn acceptance later in Group 4
```

## 5. Group 3 — M5-H + M5-I

**Public FastAPI + OpenAPI / Governed Client**

These are one delivery pipeline, not two independent gates:

```text
application services from Groups 1–2
→ exact Pydantic/FastAPI endpoints
→ RFC 9457 + request IDs + no-store
→ Apple form_post ingress exception materialized exactly
→ deterministic OpenAPI
→ frozen operationIds / success unions / problems
→ Orval Fetch + generated Zod
→ governed @dante/api-client
→ drift / determinism / generated-client tests
```

No frontend raw-fetch bypass and no alternate auth API semantics.

## 6. Group 4 — M5-J + M5-K+

**Access Web + Final M5 Proof / Acceptance**

One macro-block with two internal gates:

```text
A. Web materialization
   Google / Apple / passkey / email-password
   provider enrollment
   link-required + confirm
   methods/security management
   smart provider-enriched onboarding
   loading/cancel/error/recovery states
   backend-authoritative success only

B. Final acceptance
   focused security/race proof
   whole PostgreSQL regression where justified
   FastAPI contract proof
   OpenAPI/client drift proof
   Chromium / Firefox / WebKit
   real Google smoke/UAT
   real Apple registered-domain smoke/UAT
   Apple Private Email Relay sender configuration
   real WebAuthn/passkey UAT
   manual integrated M5 UAT
   docs reconciliation
   explicit user acceptance
```

M5 cannot close before Group 4 acceptance.

## 7. M6 / M7

```text
M6 — Native Mobile Access
PLANNED / AFTER M5 UNLESS RE-GATED

M7 — Security Hardening + Observability + Authenticated Handoff
PLANNED / FINAL WHOLE-VERTICAL GATE
```

M7 owns complete session/device/security management, production observability, final release/privacy/accessibility/security review and whole-vertical closure. It does not absorb unfinished M5 authenticator correctness.

## 8. Current authorities

```text
docs/PROJECT-STATUS.md
docs/architecture/access-auth-m5-contract.md
docs/architecture/access-auth-m5-persistence-api-contract.md
docs/workstreams/access-auth.md
docs/workstreams/access-auth-m5-live-handoff-2026-08-29.md
docs/workstreams/access-auth-m4-m7-execution-plan.md
```

Repository truth beats conversation memory. New chat != new branch/worktree.
