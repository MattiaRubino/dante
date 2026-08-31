# DANTE Roadmap

- **Status:** CURRENT FOR `feature/access-auth`
- **Last reconciled:** 2026-08-31
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active vertical:** Access/Auth
- **Current macro-phase:** M5 — Multi-authenticator Account Layer — **ACTIVE**
- **Last accepted execution block:** **GROUP 1 — M5-E + M5-G — COMPLETE / ENGINEERING PASS**
- **Current execution block:** **GROUP 2 — M5-F — WebAuthn / Passkeys — ACTIVE / IMPLEMENTATION CANDIDATE / QA PENDING**
- **M5-F PRE-SCOPE:** `64849f2cd60f1d7275344519efdf735eb9c1af95`
- **Current M5-F candidate HEAD before handoff-doc commits:** `0da2d516be8d46b24318404bec494f61a9d9ddc1`

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
        ACTIVE / IMPLEMENTATION CANDIDATE / QA PENDING
          ↓
GROUP 3 — M5-H + M5-I
Public FastAPI + Deterministic OpenAPI / Governed Client
        BLOCKED ON M5-F ACCEPTANCE
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

The historical labels `M5-E` through `M5-K+` remain the frozen semantic decomposition used by the architecture/API contract. They are not separate execution gates. The grouped order above is the only current execution order.

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

GROUP 1 / M5-E + M5-G code checkpoint
1c4b7c988eaae130d6a90d43940a42e2a550870d

GROUP 1 docs closure / M5-F PRE-SCOPE
64849f2cd60f1d7275344519efdf735eb9c1af95
```

Current accepted DB truth:

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

`20260831_13` is ACL-only and grants the governed runtime DELETE required for safe password removal; no schema shape/mapping/index/constraint change.

Group-1 closeout evidence:

```text
uv lock --check                              PASS / 57 packages
Ruff format/check/lint                       PASS
mypy src                                     PASS / 50 source files
backend fast                                 179 / 179 PASS
focused PostgreSQL Group 1                   16 / 16 PASS
full PostgreSQL regression                   120 / 120 PASS
backend build                                PASS
git diff --check                             PASS
scope audit                                  PASS
```

## 3. Group 1 — M5-E + M5-G — COMPLETE

**Authenticator Lifecycle + Password / Passwordless Adaptation**

Accepted result:

```text
provider-neutral authentication-method inventory
provider-first ExternalLinkChallenge confirmation
safe provider unlink / logical revoke
Apple grant revocation reconciliation when unlinking Apple
backend-authoritative direct-authenticator counting
Account security lock around authenticator mutations
anti-lockout recheck inside authoritative transaction
verified/recovery-eligible EmailIdentity requirement for passwordless safety
establish first password using existing Argon2id/HIBP/pepper policy
safe remove password
M4 reset adapted to create-or-replace password
normal password mutation invalidates stale recovery proof
security-sensitive retained session rotates exact bearer
concurrent provider/password removal converges safely
operation-specific ambiguous-commit reconciliation only
```

Do not reopen this block absent direct defect evidence.

## 4. Group 2 — M5-F — ACTIVE CANDIDATE

**WebAuthn / Passkeys**

Implementation is already materially present on the branch. It is **not accepted yet**.

Candidate PRE-SCOPE and snapshot:

```text
PRE-SCOPE
64849f2cd60f1d7275344519efdf735eb9c1af95

candidate implementation HEAD before docs handoff
0da2d516be8d46b24318404bec494f61a9d9ddc1

remote relation
19 commits ahead / 0 behind
10 M5-F files changed
0 migration / 0 Dictionary / 0 mapping / 0 public API / 0 frontend
```

Materialized direction:

```text
stable opaque 32-byte WebAuthnAccount user_handle
registration begin/complete
discoverable username-less authentication
passkey reauthentication
multiple credentials
UV required
resident credential required
attestation none
exact RP ID / explicit HTTPS origin
credential_id lifetime uniqueness
COSE public-key + algorithm persistence
signCount monotonic update policy
backup eligibility/state handling
label/update/remove
logical revoke
same Account anti-lockout framework from Group 1
canonical DANTE AuthSession only
real python-fido2 verifier
bounded challenge/rate/resource policy
```

Current focused proof in source includes real software-ES256 fido2 registration/assertion verification, negative crypto policy tests, full register→signin→reauth→revoke PostgreSQL path, replay rejection, duplicate credential handling, concurrent passkey-removal anti-lockout and passkey-removal vs provider-unlink Account-lock proof.

Before candidate QA/closure the following must still be completed:

```text
ambiguous signin/reauth reconciliation tolerant of later valid credential-state advancement
passkey signin authoritative mutation timestamp after Account security lock
same credential across Accounts race proof
passkey signin vs passkey removal proof
Account disable vs passkey signin proof
reauth vs concurrent bearer rotation proof
passkey removal vs password removal proof
concurrent assertion / signCount / backup-state advancement proof
ambiguous terminal-commit reconciliation proof
explicit enabled/disabled runtime composition proof
```

Only after those writes: local Ruff/mypy/fast/focused-PG/build, then full PostgreSQL regression, formatter materialization, final scope/architecture audit and documentation closure.

Real HTTPS browser/WebAuthn acceptance remains Group 4 and must not be claimed by M5-F.

## 5. Group 3 — M5-H + M5-I

**Public FastAPI + OpenAPI / Governed Client**

Blocked until M5-F is accepted. These are one delivery pipeline, not two independent gates:

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

The two M5 architecture contracts remain frozen design authority while M5-F is still a candidate; do not rewrite them merely to narrate in-flight implementation. They are reconciled again only after accepted M5-F proof.

Repository truth beats conversation memory. New chat != new branch/worktree.
