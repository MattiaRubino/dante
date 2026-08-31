# DANTE — Access/Auth Full-Stack Vertical Workstream

- **Status:** ACTIVE VERTICAL / M1–M4 CLOSED / M5 ACTIVE / M5.1–M5-D COMPLETE / GROUP 1 COMPLETE
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Last completed execution block:** **M5-E + M5-G — Authenticator Lifecycle + Password/Passwordless Adaptation — COMPLETE / ENGINEERING PASS**
- **Accepted Group-1 code checkpoint:** `1c4b7c988eaae130d6a90d43940a42e2a550870d`
- **Next execution block:** **M5-F — WebAuthn / Passkeys**
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

Do not reintroduce JWT/localStorage browser Auth, Redis/JWT session authority, Principal persistence, silent provider-email merge, provider-specific Account/session authority, Account advisory-lock replacement, wide credentialed CORS, fake frontend Auth success, persisted browser Auth cache or login-first/useEffect session repair.

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
GROUP 1 / M5-E + M5-G                                  COMPLETE / ENGINEERING PASS
```

Accepted current DB truth:

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

Group-1 closeout:

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

`20260831_13` is ACL-only: it grants `DELETE` on `dante.password_credential` to `dante_runtime`; no table shape, mapping, index or constraint changed.

Do not reopen closed slices absent direct defect evidence.

## 4. Remaining M5 execution — authoritative grouping

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

The labels M5-E/F/G/H/I/J/K+ remain semantic ownership labels from the frozen design; they are not separate execution gates.

## 5. Group 1 accepted result

```text
authentication-method inventory from durable Account truth
provider-first link challenge inspection/confirmation
exact Account proof + recent auth before provider-first link
provider unlink = logical ExternalIdentity revoke
Apple unlink = local revoke first + durable grant reconciliation
backend-authoritative direct-authenticator counts
Account security lock around authenticator mutations
anti-lockout recheck under lock
passwordless safety requires verified recovery-eligible EmailIdentity
first PasswordCredential establishment with existing HIBP/Argon2id/pepper policy
safe PasswordCredential removal
M4 reset create-or-replace PasswordCredential
normal password mutation invalidates stale recovery proof
security-sensitive retained AuthSession rotates exact bearer
concurrent password/provider removal preserves one viable authenticator
operation-specific ambiguous commit reconciliation
```

Provider-neutral lifecycle logic lives outside `apple_flow.py`; Apple grant mechanics remain Apple-specific.

## 6. Exact next block — Group 2 / M5-F

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
canonical DANTE AuthSession only
```

Public FastAPI/OpenAPI/client, Access Web and real browser/provider UAT remain later groups.

## 7. Group 3 — M5-H + M5-I

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
browser/provider proof only when public/Web surfaces exist
```

## 10. Branch/worktree safety

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not touch `main`, `feature/home-react`, `feature/access-frontend` or `/home/mattia/projects/dante-frontend` without explicit topology authorization.
