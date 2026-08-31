# DANTE — Access/Auth M4–M7 Execution Plan

- **Status:** CURRENT EXECUTION PLAN / M4 CLOSED / M5 ACTIVE / M5.1–M5-D COMPLETE
- **Vertical:** Access/Auth
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **Exact next execution block:** **GROUP 1 — M5-E + M5-G**
- **M5-D accepted implementation checkpoint:** `7d13b712f032e8d41d7cf03d406555fd9f3c0160`
- **M5-D docs closure:** `1cc331851d52d39f42e922147f300e0370649670`
- **Architecture authority:** `../architecture/access-auth-m5-contract.md`
- **Exact M5 design authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **Live handoff:** `access-auth-m5-live-handoff-2026-08-29.md`

> This plan is the current execution authority. The M5-E/F/G/H/I/J/K+ labels remain semantic ownership labels from the frozen M5 design; they no longer imply seven sequential implementation gates.

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
```

M5-D proof:

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

Current accepted DB remains Alembic `20260830_12`, PostgreSQL 18.6, 83 tables, 5 views, 15 routines, 75 triggers, 156 physical indexes, 85 FKs, 233 CHECKs and 103 standalone Dictionary entries.

## 4. Remaining M5 — four execution groups

```text
GROUP 1 — NEXT
M5-E + M5-G
Authenticator Lifecycle + Password/Passwordless Adaptation

GROUP 2
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

# 5. GROUP 1 — M5-E + M5-G — NEXT

## Purpose

Create one Account-wide direct-authenticator lifecycle for provider identities and PasswordCredential before passkeys join that model.

## Functional scope

```text
authentication-method inventory from durable Account truth
provider-first link challenge inspection + confirmation
provider link finalization after exact Account proof + recent auth + consent
safe provider unlink / logical ExternalIdentity revoke
Apple grant revocation lifecycle on unlink
backend-authoritative direct-authenticator counting
recovery-eligible EmailIdentity determination
anti-lockout under Account security lock
establish first PasswordCredential
remove PasswordCredential safely
M4 password reset adapts to create-or-replace PasswordCredential
normal password mutation invalidates pending recovery proof
security-sensitive retained session rotates exact bearer
```

## Concurrency/security scope

```text
link confirm vs competing issuer+subject link
unlink vs concurrent signin/reauth
unlink vs Account disable
provider unlink vs password removal
password establish vs recovery reset
password remove vs recovery reset
concurrent authenticator removals
recovery reachability changes vs passwordless safety decision
same AuthSession bearer rotation races
ambiguous commit reconciliation
```

Account-wide mutations serialize on the existing Account security lock. Database constraints remain the final arbiter.

## Architecture rule

Provider-neutral lifecycle logic belongs in provider-neutral application code. Do not extend `apple_flow.py` with generic methods/anti-lockout/password responsibilities. Apple-specific grant revoke/reconciliation remains Apple-specific and should be called through a narrow boundary.

## Group-1 closure proof

Candidate must prove, at minimum:

```text
Ruff format/check/lint
mypy
fast backend suite
focused unit/service lifecycle tests
focused real PostgreSQL Group-1 races/state transitions
full PostgreSQL regression before final Group-1 acceptance
backend build
git diff --check
scope audit
```

No browser/provider real-UAT gate in Group 1 because public API/Web surfaces are not materialized yet.

## Explicitly out of Group 1

```text
passkey ceremonies or passkey credential management
public FastAPI M5 routes
OpenAPI / Orval generation
Access Web UI
real provider/browser UAT
provider-data integration scopes
schema/Alembic/Dictionary change unless direct evidence forces a separately approved forward fix
```

# 6. GROUP 2 — M5-F — Passkeys / WebAuthn

## Purpose

Add WebAuthn credentials as another direct authenticator under the lifecycle/anti-lockout framework proved by Group 1.

## Scope

```text
stable opaque 32-byte WebAuthn user_handle
registration begin/complete
resident credential required direction
user verification required
attestation none
discoverable username-less authentication
passkey reauthentication on same AuthSession
multiple passkeys
credential-id lifetime uniqueness
COSE algorithm persistence
signCount / backup-state verified update policy
label/update/remove
logical revoke
anti-lockout integration
canonical DANTE AuthSession only
```

## Proof

```text
protocol/policy unit vectors
real PostgreSQL credential/challenge/race proof
full backend regressions at candidate gate
real browser/WebAuthn UAT deferred to Group 4
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

No frontend route may redefine provider/authenticator semantics independently.

# 8. GROUP 4 — M5-J + M5-K+ — Web + Final M5 Acceptance

This is one macro-block with two internal gates.

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

Official provider branding only. No provider credential imitation and no frontend-authoritative auth success.

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

  GROUP 1  M5-E + M5-G  NEXT
  GROUP 2  M5-F         PLANNED
  GROUP 3  M5-H + M5-I  PLANNED
  GROUP 4  M5-J + M5-K+ PLANNED

M6 PLANNED
M7 PLANNED / FINAL GATE
```

Whole Access/Auth remains ACTIVE / NOT CLOSED.
