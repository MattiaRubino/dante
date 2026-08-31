# DANTE — Access/Auth Full-Stack Vertical Workstream

- **Status:** ACTIVE VERTICAL / M1–M4 CLOSED / M5 ACTIVE / M5.1–M5-D COMPLETE
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Next execution block:** **M5-E + M5-G — Authenticator Lifecycle + Password/Passwordless Adaptation**
- **M5-D accepted implementation checkpoint:** `7d13b712f032e8d41d7cf03d406555fd9f3c0160`
- **M5-D documentation closure:** `1cc331851d52d39f42e922147f300e0370649670`
- **M5 architecture authority:** `../architecture/access-auth-m5-contract.md`
- **M5 exact design authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **M5 live handoff:** `access-auth-m5-live-handoff-2026-08-29.md`
- **Forward execution authority:** `access-auth-m4-m7-execution-plan.md`

> New chat != new project, branch or worktree. Continue this vertical on `feature/access-auth` and `/home/mattia/projects/dante` until whole Access/Auth closure or an explicit user topology gate.

## 1. Mandatory continuation bootstrap

Read/verify in this order:

```text
docs/PROJECT-STATUS.md
→ docs/development/agent-operating-manual.md
→ docs/ROADMAP.md
→ this file
→ docs/workstreams/access-auth-m5-live-handoff-2026-08-29.md
→ docs/architecture/access-auth-m5-contract.md
→ docs/architecture/access-auth-m5-persistence-api-contract.md
→ docs/workstreams/access-auth-m4-m7-execution-plan.md
→ Access/Auth architecture/security/API/testing contracts + ADR-011
→ DB System of Record + docs/database/access-auth.md + Dictionary
→ current implementation/tests for the exact execution block
```

Repository truth beats conversation memory. Do not reinterpret M1–M4 or redo broad M5 discovery from scratch.

No new branch/worktree, merge, rebase, force-push/history rewrite or protected-main write without explicit user authorization.

## 2. Frozen Auth constitution

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived
multiple independent AuthSessions normal
provider identity key = issuer + subject
provider email never silently links Accounts
provider authentication != provider-data integration authorization
provider token/assertion != DANTE AuthSession
passwordless Account valid
verification != setup completion
reauthentication != initial signin
frontend/provider callback != backend-authoritative success
unknown/loading != signed-out/signed-in/error
method != factor != assurance
```

Do not reintroduce:

```text
JWT/localStorage browser Auth
Redis/JWT session authority
Principal table
silent provider-email merge
provider-specific parallel Account/session authority
Account advisory-lock replacement
wide credentialed CORS
fake frontend Auth success
persisted browser Auth cache
login-first + useEffect session repair
```

## 3. Closed foundation

```text
M1  Visual / UX Freeze                                  CLOSED / ACCEPTED
M2  Auth Architecture Freeze                           CLOSED / ACCEPTED / QA PASS
M3  Email/Password Signin + AuthSession Spine          CLOSED / ENGINEERING PASS / USER ACCEPTED
M4  Signup + Verification + Recovery + Reset + Reauth  CLOSED / ENGINEERING PASS / USER ACCEPTED

M5.1 architecture/external-authority freeze            COMPLETE
M5.2 exact persistence/API design                      COMPLETE
M5-A persistence foundations                           COMPLETE / REAL POSTGRESQL PROVEN
M5-B provider/JWK/JOSE/AEAD infrastructure             COMPLETE / ENGINEERING PASS
M5-C Google authentication                             COMPLETE / ENGINEERING PASS
M5-D Apple authentication + grant/notifications        COMPLETE / ENGINEERING PASS
```

Accepted current DB truth:

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

M5-D closeout:

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

Do not reopen closed slices absent direct defect evidence.

## 4. Remaining M5 execution — authoritative grouping

The labels M5-E/F/G/H/I/J/K+ remain useful semantic ownership labels from the frozen design. They are **not separate execution gates** anymore.

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

This order intentionally executes M5-G with M5-E before M5-F because anti-lockout must account for provider identities and PasswordCredential under one Account-wide model before passkeys join it.

## 5. Exact next block — Group 1 / M5-E + M5-G

Goal: establish one provider-neutral direct-authenticator lifecycle and then adapt the existing password/recovery system to it.

Required behavior:

```text
authentication-method inventory derived from current durable Account truth
provider-first link challenge inspection/confirmation
explicit Account proof + recent auth + consent before provider-first link
provider unlink = logical ExternalIdentity revoke, not DELETE
Apple unlink = local revoke first + durable grant reconciliation
no provider email coincidence as link authority
backend-authoritative active direct-authenticator counts
Account security lock around all authenticator mutations
anti-lockout recheck under lock
passwordless Account requires viable verified recovery EmailIdentity
establish first PasswordCredential with existing HIBP/Argon2id/pepper policy
remove PasswordCredential only when anti-lockout still holds
M4 reset becomes create-or-replace PasswordCredential
normal password mutation invalidates stale password recovery proof
security-sensitive retained AuthSession rotates exact bearer
commit ambiguity gets operation-specific reconciliation only
concurrent provider/password mutations converge against DB constraints/locks
```

Implementation rule: prefer extracting provider-neutral lifecycle helpers/services where they reduce duplication. Do **not** add more unrelated lifecycle logic to `apple_flow.py` merely because Apple has grant state.

Still out of scope:

```text
passkey registration/authentication/management
public M5 FastAPI routes
OpenAPI/Orval client generation
Access Web implementation
real provider/browser/UAT acceptance
provider-data integration authorization/scopes
schema/Alembic/Dictionary changes unless direct evidence forces a separately gated forward fix
```

## 6. Group 2 — M5-F

Passkeys/WebAuthn join the lifecycle established by Group 1:

```text
opaque 32-byte user_handle
registration begin/complete
discoverable username-less signin
reauthentication on same AuthSession
multiple passkeys
UV required / resident credential direction / attestation none
credential-id lifetime uniqueness
COSE algorithm persistence
signCount + backup-state policy
label/update/remove
logical revoke
Group-1 anti-lockout integration
```

## 7. Group 3 — M5-H + M5-I

One delivery pipeline:

```text
application services
→ exact FastAPI/Pydantic contract
→ RFC9457 + no-store + request IDs
→ Apple form_post ingress boundary
→ deterministic OpenAPI
→ frozen operationIds/success unions/problems
→ Orval Fetch + generated Zod
→ governed @dante/api-client
→ drift/determinism tests
```

## 8. Group 4 — M5-J + M5-K+

First materialize the Web product, then run final M5 acceptance without opening another architecture phase.

```text
Access Web Google/Apple/passkey/email-password
provider enrollment/link/security-management states
smart provider-enriched onboarding
Chromium / Firefox / WebKit
real Google UAT
real Apple registered-domain UAT
Apple Private Email Relay sender configuration
real WebAuthn/passkey UAT
final security/race/HTTP/OpenAPI/client/PostgreSQL proof as applicable
manual integrated UAT
docs reconciliation
explicit user acceptance
```

## 9. Quality / testing posture

```text
prove each invariant at the truthful layer
focused proof during development
real PostgreSQL for DB/race authority
no flaky Auth hidden behind retries
no blind retry of non-idempotent provider mutations
one heavy closeout regression when candidate is ready
browser/provider proof only when the public/Web surfaces exist
```

## 10. Branch/worktree safety

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not touch `main`, `feature/home-react`, `feature/access-frontend` or `/home/mattia/projects/dante-frontend` without explicit topology authorization.
