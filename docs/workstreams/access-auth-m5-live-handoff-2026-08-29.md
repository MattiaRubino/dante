# DANTE — Access/Auth M5 Live Handoff — 2026-08-29

- **Status:** CURRENT CONTINUATION SAVE-GAME / M5.1–M5-D COMPLETE / GROUP 1 COMPLETE / GROUP 2 NEXT
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **Last accepted code checkpoint:** `1c4b7c988eaae130d6a90d43940a42e2a550870d` — Group 1 / M5-E + M5-G
- **Accepted Alembic head:** `20260831_13`
- **Exact next execution block:** **M5-F — WebAuthn / Passkeys**
- **Architecture authority:** `../architecture/access-auth-m5-contract.md`
- **Exact M5 design authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **Forward plan:** `access-auth-m4-m7-execution-plan.md`

> This file is the live save-game. A new chat should verify branch HEAD, read the current authorities, and continue from Group 2. Do not replay prior conversations or reopen closed Group 1 work absent direct defect evidence.

## 1. Mandatory continuation

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not create another Access branch/worktree because the chat changed.

Do not touch without explicit topology/write gate:

```text
main
feature/home-react
feature/access-frontend
/home/mattia/projects/dante-frontend
```

Before remote writes obey `docs/development/agent-operating-manual.md`: exact PRE-SCOPE SHA, exact CREATE/UPDATE/DELETE paths, purpose/out-of-scope, explicit approval, HEAD race-check, post-write compare.

## 2. Read order for a new chat

```text
docs/PROJECT-STATUS.md
→ docs/development/agent-operating-manual.md
→ docs/ROADMAP.md
→ docs/workstreams/access-auth.md
→ this file
→ docs/architecture/access-auth-m5-contract.md
→ docs/architecture/access-auth-m5-persistence-api-contract.md
→ docs/workstreams/access-auth-m4-m7-execution-plan.md
→ Access/Auth architecture/security/API/testing contracts + ADR-011
→ DB System of Record + docs/database/access-auth.md + Dictionary
→ current backend implementation/tests for Group 2 / M5-F
```

Repository truth beats conversation memory.

## 3. Permanent Auth constitution

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
provider identity = issuer + subject
provider email != identity/link authority
provider auth != provider-data authorization
provider token/assertion != DANTE AuthSession
passwordless Account valid
multiple independent AuthSessions normal
method != factor != assurance
frontend/provider callback != backend-authoritative success
```

No JWT/localStorage auth, no Redis/JWT session authority, no silent provider-email merge, no provider-specific Account/session authority, no fake frontend success.

## 4. Closed state — do not reopen casually

```text
M1  CLOSED / ACCEPTED
M2  CLOSED / ACCEPTED / QA PASS
M3  CLOSED / ENGINEERING PASS / USER ACCEPTED
M4  CLOSED / ENGINEERING PASS / USER ACCEPTED

M5.1 COMPLETE
M5.2 COMPLETE
M5-A COMPLETE / REAL POSTGRESQL PROVEN
M5-B COMPLETE / ENGINEERING PASS
M5-C COMPLETE / ENGINEERING PASS
M5-D COMPLETE / ENGINEERING PASS
GROUP 1 / M5-E + M5-G COMPLETE / ENGINEERING PASS
```

Current accepted DB:

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

`20260831_13` is ACL-only: governed runtime `DELETE` on `password_credential`; no table shape, mapping, index or constraint change.

## 5. Group 1 accepted evidence

```text
uv lock --check                              PASS / 57 packages
Ruff format/check/lint                       PASS
mypy src                                     PASS / 50 source files
backend fast                                 179 / 179 PASS
focused real PostgreSQL Group 1              16 / 16 PASS
full real PostgreSQL regression              120 / 120 PASS
backend build                                PASS / sdist + wheel
git diff --check                             PASS
scope audit                                  PASS
```

Accepted behavior includes provider-neutral method inventory, explicit provider-first link confirmation, provider unlink, Apple local-first grant revocation handoff, Account-wide anti-lockout, password establish/remove, passwordless recovery create-or-replace, exact bearer rotation and concurrent-removal serialization.

## 6. Remaining M5 — grouped execution

```text
GROUP 1
M5-E + M5-G
Authenticator Lifecycle + Password/Passwordless Adaptation
COMPLETE / ENGINEERING PASS

GROUP 2 — NEXT
M5-F
Passkeys / WebAuthn

GROUP 3
M5-H + M5-I
Public FastAPI + OpenAPI / Governed Client

GROUP 4
M5-J + M5-K+
Access Web + Final Security / Provider / Browser / UAT Acceptance
```

Do not revert to the old seven-step sequential execution merely because the semantic labels still exist in the frozen M5 design.

## 7. Exact next work — Group 2 / M5-F

Purpose:

```text
add passkeys as a first-class direct authenticator
under the Account-wide lifecycle/anti-lockout authority proved by Group 1
```

Required behavior:

```text
stable random 32-byte WebAuthnAccount user_handle
registration begin/complete
authenticated Account + recent auth for registration
resident credential required direction
user verification required
attestation none
exact RP ID and allowed origin
short single-use challenge
discoverable username-less authentication
passkey reauthentication on same AuthSession
multiple passkeys per Account
credential_id lifetime uniqueness
COSE algorithm persistence
signCount / backup eligibility / backup state policy
bounded transport hints
label/update/remove
logical revoke rather than DELETE
Group-1 anti-lockout recheck on removal
canonical DANTE AuthSession only
commit/race reconciliation at truthful DB boundaries
```

Still out of scope:

```text
M5-H public FastAPI endpoints
M5-I OpenAPI/Orval generation
M5-J Access Web
M5-K+ real browser/provider/WebAuthn acceptance
provider-data scopes/integrations
```

## 8. Later groups

```text
GROUP 3 / M5-H+I
FastAPI/Pydantic
→ RFC9457/no-store/request IDs
→ deterministic OpenAPI
→ Orval Fetch/Zod
→ governed @dante/api-client

GROUP 4 / M5-J+K+
Access Web
→ Google/Apple/passkey/password surfaces
→ provider enrollment/link/security management
→ browser matrix
→ real Google/Apple/WebAuthn UAT
→ Private Email Relay sender proof
→ final races/HTTP/client/PostgreSQL proof
→ manual M5 UAT
→ docs + explicit user acceptance
```

## 9. Testing posture

Use focused proof while developing M5-F. Real PostgreSQL is authoritative for credential/challenge lifecycle, uniqueness and races. Do not run the full heavy regression after every edit; run it at the candidate gate. Real browser/WebAuthn proof remains Group 4 because the public API/Web surface is not materialized yet.

Never push debugging to the user: local output is evidence; implementation defects are fixed in the branch.
