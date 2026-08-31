# DANTE — Access/Auth M4–M7 Execution Plan

- **Status:** CURRENT EXECUTION PLAN / M4 CLOSED / M5 ACTIVE / GROUP 1 COMPLETE
- **Vertical:** Access/Auth
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **Exact next execution block:** **GROUP 2 — M5-F — WebAuthn / Passkeys**
- **Accepted Group-1 code checkpoint:** `1c4b7c988eaae130d6a90d43940a42e2a550870d`
- **Accepted Alembic head:** `20260831_13`
- **Architecture authority:** `../architecture/access-auth-m5-contract.md`
- **Exact M5 design authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **Live handoff:** `access-auth-m5-live-handoff-2026-08-29.md`

> This plan is the current execution authority. The M5-E/F/G/H/I/J/K+ labels remain semantic ownership labels from the frozen M5 design; they do not imply seven sequential implementation gates.

## 1. Continuation rules

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Before writes follow `docs/development/agent-operating-manual.md`: exact PRE-SCOPE, exact paths, purpose/out-of-scope, explicit approval, branch race-check, post-write compare.

No merge/rebase/history rewrite/protected-main write without explicit authorization.

## 2. Frozen foundations

Reuse, do not replace:

```text
Account = durable access/security root
EmailIdentity separate from Account
PasswordCredential optional
Principal runtime-derived
opaque PostgreSQL-backed AuthSession
multiple independent AuthSessions normal
same-origin Web Auth
Secure HttpOnly host-only __Host-dante-session
session-bound CSRF
Origin + Fetch Metadata + X-Dante-Client
/api/v1 + RFC9457
Account security serialization point
READ COMMITTED + targeted locking
no blind mutation retry
FastAPI/Pydantic → deterministic OpenAPI → Orval Fetch → governed @dante/api-client
TanStack Query remote lifecycle
TanStack Router critical-session bootstrap
real PostgreSQL proof
real HTTPS Chromium + Firefox + WebKit proof
```

Permanent Auth rules:

```text
provider identity = issuer + subject
provider email != Account/link authority
provider authentication != provider-data authorization
provider assertion/token != DANTE AuthSession
passwordless Account valid
normal provider/passkey removal = logical revoke
no Account before accepted mailbox proof
reauth rotates exact bearer on same AuthSession
network outside DB transaction
commit ambiguity → operation-specific reconciliation only
```

## 3. Closed M5 implementation

```text
M5.1 architecture/external-authority freeze            COMPLETE
M5.2 exact persistence/API design                      COMPLETE
M5-A persistence foundations                           COMPLETE / REAL POSTGRESQL PROVEN
M5-B provider/JWK/JOSE/AEAD/WebAuthn infrastructure    COMPLETE / ENGINEERING PASS
M5-C Google authentication                             COMPLETE / ENGINEERING PASS
M5-D Apple authentication + grant/notifications        COMPLETE / ENGINEERING PASS
GROUP 1 / M5-E + M5-G                                  COMPLETE / ENGINEERING PASS
```

Group-1 proof:

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

Current accepted DB is Alembic `20260831_13`, PostgreSQL 18.6, 83 tables, 5 views, 15 routines, 75 triggers, 156 physical indexes, 85 FKs, 233 CHECKs and 103 standalone Dictionary entries. `20260831_13` is ACL-only and grants the governed runtime DELETE required for password removal.

## 4. Remaining M5 — four execution groups

```text
GROUP 1
M5-E + M5-G
Authenticator Lifecycle + Password/Passwordless Adaptation
COMPLETE / ENGINEERING PASS

GROUP 2 — NEXT
M5-F
WebAuthn / Passkeys

GROUP 3
M5-H + M5-I
Public FastAPI + Deterministic OpenAPI / Governed Client

GROUP 4
M5-J + M5-K+
Access Web + Security / Provider / Browser / UAT / Acceptance
```

Execution order is Group 1 → Group 2 → Group 3 → Group 4. Do not restore the old E→F→G→H→I→J→K sequence.

# 5. GROUP 1 — M5-E + M5-G — COMPLETE

Accepted result:

```text
authentication-method inventory from durable Account truth
provider-first link challenge inspection + confirmation
provider link finalization after exact Account proof + recent auth
safe provider unlink / logical ExternalIdentity revoke
Apple local-first identity/grant revoke with remote reconciliation handoff
backend-authoritative direct-authenticator counting
recovery-eligible EmailIdentity determination
anti-lockout under Account security lock
establish first PasswordCredential
remove PasswordCredential safely
M4 password reset create-or-replace PasswordCredential
normal password mutation invalidates pending recovery proof
security-sensitive retained session rotates exact bearer
concurrent provider/password removals preserve a viable authenticator
operation-specific ambiguous commit reconciliation
```

Provider-neutral lifecycle logic is outside `apple_flow.py`; Apple grant mechanics remain Apple-specific.

# 6. GROUP 2 — M5-F — Passkeys / WebAuthn — NEXT

## Purpose

Add WebAuthn credentials as another direct authenticator under the lifecycle/anti-lockout framework proved by Group 1.

## Scope

```text
stable opaque random 32-byte WebAuthn user_handle
registration begin/complete
authenticated Account + recent auth for registration
resident credential required direction
user verification required
attestation none
exact RP ID and allowed origin
short single-use challenge
discoverable username-less authentication
passkey reauthentication on same AuthSession
multiple passkeys
credential-id lifetime uniqueness
COSE algorithm persistence
signCount / backup eligibility / backup-state verified update policy
bounded transport hints
label/update/remove
logical revoke
Group-1 anti-lockout integration
canonical DANTE AuthSession only
```

## Concurrency/security scope

```text
registration duplicate credential race
registration completion replay
signin assertion vs credential removal
reauth assertion vs bearer rotation
concurrent passkey removals
passkey removal vs password/provider removal
challenge consume races
signCount / backup-state update races
Account disable vs registration/authentication
ambiguous commit reconciliation where mutation outcome can be safely proven
```

Account-wide mutation continues to serialize on the existing Account security lock. Database uniqueness remains final arbiter.

## Proof

```text
Ruff format/check/lint
mypy
fast protocol/policy/service tests
focused real PostgreSQL credential/challenge/race proof
full backend/PostgreSQL regressions at candidate gate when shared state justifies it
backend build
git diff --check
scope audit
```

Real browser/WebAuthn UAT is deferred to Group 4 because public FastAPI/Web surfaces are not yet materialized.

## Explicitly out of Group 2

```text
public M5 FastAPI routes
OpenAPI / Orval generation
Access Web UI
real provider/browser/WebAuthn UAT
provider-data integration scopes
```

# 7. GROUP 3 — M5-H + M5-I — Public API + Governed Client

M5-H and M5-I are executed together because they form one deterministic contract-delivery pipeline.

```text
application services from Groups 1–2
→ exact FastAPI/Pydantic materialization
→ stable /api/v1 paths and operationIds
→ RFC9457 typed problems
→ no-store / request-id behavior
→ Apple form_post callback ingress exception
→ Apple notifications boundary
→ deterministic OpenAPI without live providers/secrets
→ Orval Fetch + generated Zod
→ governed @dante/api-client
→ schema/client drift + deterministic-generation proof
```

# 8. GROUP 4 — M5-J + M5-K+ — Web + Final M5 Acceptance

## Gate A — Web product materialization

```text
Google control
Apple control
passkey control
email/password path
provider enrollment + OTP
provider collision/link-required + confirm
authentication-method/security management
password establish/remove states
passkey management states
smart provider-enriched onboarding
loading/pending/cancel/error/recovery states
hard-refresh backend-authoritative session truth
```

## Gate B — final M5 proof / acceptance

```text
focused security/race proof
whole PostgreSQL regression where justified
FastAPI HTTP contract
OpenAPI/client drift proof
Web component/application tests
Chromium / Firefox / WebKit
real Google configured-client smoke/UAT
real Apple registered HTTPS Services ID/domain smoke/UAT
Apple Private Email Relay sender configuration proof
real WebAuthn/passkey UAT
manual integrated M5 UAT
docs reconciliation
explicit user acceptance
```

Mandatory CI remains deterministic and provider-independent; real providers are acceptance/UAT, not CI dependencies.

# 9. M6 / M7

```text
M6 — Native Mobile Access
PLANNED / AFTER M5 UNLESS RE-GATED

M7 — Security Hardening + Observability + Authenticated Handoff
PLANNED / FINAL WHOLE-VERTICAL GATE
```

M7 owns complete session/device/security management, new-login alerts/“this wasn’t me”, production observability, final privacy/accessibility/dependency/release review and whole-vertical closure. It does not absorb unfinished M5 authenticator correctness.

# 10. Current execution pointer

```text
M1 CLOSED
M2 CLOSED
M3 CLOSED
M4 CLOSED
M5 ACTIVE
  M5.1 COMPLETE
  M5.2 COMPLETE
  M5-A COMPLETE / POSTGRESQL PROVEN
  M5-B COMPLETE / ENGINEERING PASS
  M5-C COMPLETE / ENGINEERING PASS
  M5-D COMPLETE / ENGINEERING PASS

  GROUP 1  M5-E + M5-G  COMPLETE / ENGINEERING PASS
  GROUP 2  M5-F         NEXT
  GROUP 3  M5-H + M5-I  PLANNED
  GROUP 4  M5-J + M5-K+ PLANNED

M6 PLANNED
M7 PLANNED / FINAL GATE
```

Whole Access/Auth remains ACTIVE / NOT CLOSED.
