# DANTE — Access/Auth M5 Live Handoff — 2026-08-29

- **Status:** CURRENT CONTINUATION SAVE-GAME / M5.1–M5-D COMPLETE / GROUP 1 NEXT
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **Last accepted code checkpoint:** `7d13b712f032e8d41d7cf03d406555fd9f3c0160` — M5-D
- **M5-D docs closure:** `1cc331851d52d39f42e922147f300e0370649670`
- **Exact next execution block:** **M5-E + M5-G — Authenticator Lifecycle + Password/Passwordless Adaptation**
- **Architecture authority:** `../architecture/access-auth-m5-contract.md`
- **Exact M5 design authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **Forward plan:** `access-auth-m4-m7-execution-plan.md`

> This file is the live save-game. A new chat should not replay prior conversations or restart M5 discovery. Verify the current branch HEAD, read the current authorities, then continue from Group 1.

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
→ current backend implementation/tests for Group 1
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
```

Current accepted DB:

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

No DB schema change in M5-B/C/D.

## 5. M5-D accepted evidence

```text
uv lock --check                              PASS
Ruff format/check/lint                       PASS
mypy src                                     PASS
backend fast                                 171 / 171 PASS
focused real PostgreSQL M5-D                  9 / 9 PASS
full real PostgreSQL regression              111 / 111 PASS
backend build                                PASS / sdist + wheel
git diff --check                             PASS
scope audit                                  PASS
```

M5-D proves the Apple backend protocol/application/persistence/grant/notification slice. It does not claim real Apple browser/provider production acceptance.

## 6. Remaining M5 — grouped execution

The frozen labels remain for traceability, but there are now four execution gates:

```text
GROUP 1 — NEXT
M5-E + M5-G
Authenticator Lifecycle + Password/Passwordless Adaptation

GROUP 2
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

## 7. Exact next work — Group 1 / M5-E + M5-G

Purpose:

```text
one provider-neutral direct-authenticator lifecycle
+ explicit provider linking/unlinking
+ backend-authoritative methods truth
+ Account-wide anti-lockout
+ password/passwordless lifecycle adaptation
```

Required behavior:

```text
inspect current authentication methods from durable Account state
inspect/confirm provider-first ExternalLinkChallenge
prove exact Account + recent auth + explicit consent before provider-first link
safe provider unlink = logical ExternalIdentity revoke
Apple unlink = local identity revoke first, then durable grant revoke reconciliation
count active direct authenticators under Account security lock
recheck anti-lockout inside mutation transaction
passwordless safety requires a viable verified recovery EmailIdentity
establish first password with existing HIBP/Argon2id/pepper stack
remove password only when Account remains recoverable/authenticatable
M4 reset create-or-replace PasswordCredential
invalidate older pending password recovery proof on normal password mutation
rotate exact retained AuthSession bearer after sensitive mutations
concurrent link/unlink/password mutations converge on DB truth
commit ambiguity uses exact operation-specific reconciliation only
```

Architecture direction:

```text
provider-neutral lifecycle logic should be extracted where it is genuinely shared
Google/Apple protocol evidence stays provider-specific
Apple grant mechanics stay Apple-specific
apple_flow.py must not become the home for new generic authenticator-management logic
```

Still out of scope:

```text
M5-F WebAuthn/passkey ceremonies
M5-H public FastAPI endpoints
M5-I OpenAPI/Orval generation
M5-J Access Web
M5-K+ real provider/browser/UAT closure
provider-data scopes/integrations
schema/Alembic/Dictionary change unless direct evidence forces a separately approved forward fix
```

## 8. Later groups

```text
GROUP 2 / M5-F
passkey registration + discoverable signin + reauth + management
→ reuse Group-1 anti-lockout framework

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

Use focused proof while developing Group 1. Do not rerun the full PostgreSQL suite after every edit. Before Group-1 closure, run the meaningful whole-backend regression because Account/authenticator lifecycle touches shared password/provider state.

Never push debugging to the user: local output is evidence; implementation defects are fixed in the branch.
