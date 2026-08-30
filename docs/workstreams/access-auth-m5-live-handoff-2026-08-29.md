# DANTE — Access/Auth M5 Live Handoff — 2026-08-29

- **Status:** CURRENT CONTINUATION SAVE-GAME / M5.1–M5-B COMPLETE / M5-C NEXT
- **Vertical:** Access/Auth
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **M5-B accepted implementation checkpoint:** `e2d40a7666e3c0130afecd8113b8063390b86b9d`
- **M5-A accepted implementation checkpoint:** `7e40e02d301b0812b3f55e0d9d4ce6439e420b2a`
- **M4 implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **M4 documentation closure:** `a95955da72cbb9119982aa1544c2aaa356fc5e6a`
- **M5.1 architecture freeze checkpoint:** `8f993ace74d21c98d4034b0e521a1f9b458b007a`
- **M5 architecture authority:** `../architecture/access-auth-m5-contract.md`
- **M5.2 exact persistence/API authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **Forward plan:** `access-auth-m4-m7-execution-plan.md`

> This file is the live save-game for continuation. Repository truth wins if the branch has moved after this handoff. A new chat should not replay the conversation or redo broad M5 research; it should verify current branch state, read the authorities above, and continue from M5-C.

---

# 1. Mandatory continuation

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not create another Access branch/worktree merely because the chat changed.

Do not touch without explicit topology/write gate:

```text
main
feature/home-react
feature/access-frontend
/home/mattia/projects/dante-frontend
```

Before remote Git writes, obey `docs/development/agent-operating-manual.md`:

```text
1. fetch current branch HEAD
2. establish exact PRE-SCOPE SHA
3. list exact CREATE/UPDATE/DELETE paths
4. list exact purpose and exclusions
5. obtain explicit user approval
6. re-fetch HEAD before first write
7. post-write compare actual path/status set against gate
```

No merge/rebase/force-push/protected-main write without explicit authorization.

Recommended read order:

1. `docs/PROJECT-STATUS.md`
2. `docs/ROADMAP.md`
3. `docs/workstreams/access-auth.md`
4. this file
5. `docs/architecture/access-auth-m5-contract.md`
6. `docs/architecture/access-auth-m5-persistence-api-contract.md`
7. `docs/workstreams/access-auth-m4-m7-execution-plan.md`
8. Access/Auth architecture/security/API/testing contracts + ADR-011
9. `docs/database/README.md`
10. `docs/database/access-auth.md`
11. current Access/Auth Dictionary entries
12. CP6 persistence constitution
13. `docs/frontend/access.md`
14. current backend implementation/tests for the exact M5-C slice

---

# 2. User quality bar / working style

DANTE must be built at the level expected from mature large applications such as Google, Notion, Linear, Facebook and comparable serious products.

Interpretation:

```text
production-quality architecture
security-first consumer-grade UX
high performance
strong PostgreSQL integrity
clean maintainable code
no hidden technical debt for convenience
configurable/tokenized UI rather than hardcoded one-offs
strong accessibility/responsive behavior
real boundary proof rather than mock-only confidence
no gratuitous enterprise theatre/overengineering without consumer value
```

Testing preference retained from M4/M5-A/M5-B:

```text
prove each invariant at the truthful layer
use focused proof during development
avoid rerunning heavy suites after every tiny edit
one heavy closeout QA when candidate is actually ready
never hide flaky Auth behind retries
```

For manual UAT, advance one action at a time.

Avoid top-level `exit` in shell snippets.

---

# 3. Closed foundation — do not reopen casually

```text
M1 — Access Visual/UX Freeze
CLOSED / ACCEPTED

M2 — Auth Architecture Freeze
CLOSED / ACCEPTED / QA PASS

M3 — Email/Password Signin + AuthSession Spine
CLOSED / ENGINEERING PASS / USER ACCEPTED

M4 — Signup + Verification + Recovery + Reset + Reauth
CLOSED / ENGINEERING PASS / USER ACCEPTED
```

Whole Access/Auth remains:

```text
ACTIVE / NOT CLOSED
```

Permanent Auth constitution:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived
multiple independent AuthSessions normal
same-origin Web Auth
Secure HttpOnly host-only __Host-dante-session
session-bound CSRF + Origin + Fetch Metadata + X-Dante-Client
provider identity = issuer + subject
provider email != identity/link authority
provider authentication != provider-data integration authorization
provider token/assertion != DANTE AuthSession
passwordless Account valid
method != factor != assurance
frontend/provider callback != backend-authoritative success
unknown/loading != signed-out/signed-in/error
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
Axios just for Auth
raw fetch from Access UI
fake frontend Auth success
persisted browser Auth cache
login-first + useEffect session repair
```

---

# 4. M4 accepted baseline

Final M4 implementation checkpoint:

```text
c95e3b2ca664725bcacc374cb5ba6ed49409fe2b
fix(auth): reconcile M4 PostgreSQL acceptance
```

Accepted M4 database baseline:

```text
PostgreSQL          18.6
Alembic             20260829_11
74 tables
5 views
15 routines
75 triggers
113 physical indexes
72 foreign keys
149 CHECK constraints
94 standalone Dictionary entries
```

Accepted M4 automated proof:

```text
backend static / typing / lint / build        PASS
backend fast                                 87 / 87 PASS
real PostgreSQL marked suite                 87 / 87 PASS
Web Access UI                                22 / 22 PASS
real Auth full-stack browser                 33 / 33 PASS
Chromium / Firefox / WebKit                  11 / 11 PASS each
```

Accepted manual UAT:

```text
login/session/logout
new signup → OTP → Account/AuthSession → setup handoff
recovery → reset → fresh replacement signin
existing-account signup → OTP → safe existing_account result
```

Do not rerun M4 QA absent direct regression evidence.

---

# 5. M5 current status

```text
M5 overall                                  ACTIVE
M5.1 external-authority/benchmark freeze    COMPLETE
M5.1 architecture/security freeze           COMPLETE
M5.2 persistence/API design                 COMPLETE
M5-A persistence implementation             COMPLETE / POSTGRESQL PROVEN
M5-B dependency/runtime infrastructure      COMPLETE / ENGINEERING PASS
M5-C Google authentication                  NEXT
M5 OpenAPI/client materialization           NOT STARTED
M5 Web runtime integration                  NOT STARTED
```

The design authorities are:

```text
docs/architecture/access-auth-m5-contract.md
docs/architecture/access-auth-m5-persistence-api-contract.md
```

Do not perform another broad “what should Google/Apple/passkeys do?” discovery sweep unless provider standards materially changed. M5-C starts from the frozen contracts, accepted M5-A persistence reality and accepted M5-B trust/runtime foundation.

---

# 6. M5-A accepted persistence truth

Accepted implementation checkpoint:

```text
7e40e02d301b0812b3f55e0d9d4ce6439e420b2a
fix(auth): reconcile M5 persistence acceptance
```

Current database:

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

Materialized delta:

```text
ALTER
  dante.email_identity
    + recovery_restriction_code
    + recovery_restriction_observed_at

CREATE
  dante.external_identity
  dante.external_auth_transaction
  dante.external_link_challenge
  dante.external_signup_challenge
  dante.account_profile_bootstrap
  dante.apple_auth_grant
  dante.webauthn_account
  dante.passkey_credential
  dante.webauthn_challenge
```

Exactly 9 new tables. No generic provider/auth token/challenge table.

Accepted proof:

```text
uv lock                                      PASS
Ruff format / lint                           PASS
mypy strict                                  PASS
backend fast                                 87 / 87 PASS
real PostgreSQL 18.6                         95 / 95 PASS
M5 persistence tests                          8 / 8 PASS
migration head/base/head                      PASS
Alembic autogenerate drift                    PASS
Dictionary ≈ SQLAlchemy ≈ Alembic ≈ PG       PASS
runtime ACL / negative constraints            PASS
backend build                                 PASS
```

Physical hardening accepted during materialization:

```text
ExternalIdentity exact Apple composite target
AppleAuthGrant exact issuer+subject binding
Apple link/signup challenge exact grant binding
AuthSession exact Account composite target
WebAuthnAccount exact Account+userHandle target
WebAuthnChallenge exact Account/session/userHandle binding
PasskeyCredential ownership through WebAuthnAccount
explicit cose_algorithm
logical passkey revocation
backup_state => backup_eligible
cleanup indexes for profile bootstrap / pending Apple grant
column-scoped EmailIdentity INSERT/UPDATE reconciliation
```

---

# 7. Provider-enriched onboarding

Provider data policy remains:

```text
provider data
→ validate/classify provenance
→ eliminate redundant onboarding
→ initialize/stage useful setup/profile values
→ user later edits in DANTE
→ future provider login never silently overwrites DANTE-owned values
```

Google useful bootstrap when actually returned:

```text
email
email_verified
name
given_name
family_name
picture
locale
hosted-domain metadata
security/authentication claims actually supplied
```

Apple useful bootstrap:

```text
email or Private Email Relay
first/last name on initial authorization when supplied
private-email/reachability semantics
security/authentication claims actually supplied
```

Apple name may be one-shot. M5-A has bounded `account_profile_bootstrap` staging so later lifecycle code does not lose it or dump profile fields into Account/ExternalIdentity.

---

# 8. Frozen M5 persistence/lifecycle invariants carried forward

### EmailIdentity reachability

```text
verified_at = historical mailbox proof
recovery_restriction_code = current recovery-blocking policy
recovery_restriction_observed_at = newest provider reachability evidence
```

Older/equal Apple relay events cannot reverse newer state.

### ExternalIdentity

```text
identity key = issuer + subject
UNIQUE(issuer,subject)
normal unlink = logical revoke
provider email is metadata only
```

### ExternalAuthTransaction

```text
purpose = sign_in | link | reauthenticate
TTL <= 15 min
state/nonce verifier only
link/reauth bind exact session + begin-time bearer verifier snapshot
single conditional claim
Apple claim before code exchange
```

### AppleAuthGrant

```text
pending
active
revocation_pending
revoked
```

Refresh token is application-layer AEAD encrypted; key material stays outside PostgreSQL/Git/logs. Local auth revoke precedes remote provider revoke.

### Provider collision

```text
provider proof + matching existing email
→ no duplicate Account
→ targeted link challenge
→ prove exact Account
→ explicit consent + recent auth
→ Account lock
→ final issuer+subject uniqueness check
→ atomic binding
```

### Passkeys

```text
random immutable 32-byte user_handle
credential_id lifetime UNIQUE
explicit COSE algorithm
backup/signCount metadata
logical revoke
no biometric/PIN material
```

---

# 9. M5-B accepted trust/runtime foundation

```text
M5-B — provider/JWK/JOSE/AEAD/WebAuthn policy infrastructure
COMPLETE / ENGINEERING PASS
```

Accepted implementation checkpoint:

```text
e2d40a7666e3c0130afecd8113b8063390b86b9d
chore(auth): finalize M5-B lock and formatting
```

Accepted dependency/runtime baseline:

```text
fido2         2.2.1
joserfc       1.7.4
cryptography  50.0.1
httpx2        existing runtime
Python        3.14
uv            0.12.5
```

Accepted infrastructure:

```text
typed provider settings + safe disabled defaults
bounded provider/JWK network runtime
trusted configured JWKS source only
coordinated JWK cache/conditional refresh/unknown-kid cooldown
strict RS256 JOSE boundary + canonical unpadded Base64URL segments
Apple AES-256-GCM grant key ring + 12-byte nonce + stable AAD
purpose-separated 256-bit provider/link/enrollment/WebAuthn proofs
FIDO2 RP/origin policy baseline
single process-scoped AuthRuntime ownership / clean shutdown
no provider network I/O at startup
```

Accepted closeout proof:

```text
uv lock --check                              PASS
Ruff autofix / format / lint                 PASS
mypy strict                                  PASS / 73 source files
backend fast                                 127 / 127 PASS
backend build                                PASS
git diff --check                             PASS
```

No PostgreSQL rerun was required because M5-B changes no schema/Alembic/Dictionary/DB contract.

---

# 10. Exact next work — M5-C

```text
M5-C — Google Authentication + Account Creation / Collision
NEXT
```

M5-C must consume the accepted M5-B runtime without creating a second provider/session authority.

Exact product boundary:

```text
Google GIS/OIDC authentication
begin/complete transaction lifecycle
provider ID-token cryptographic verification via trusted JWK runtime
provider claim semantics: issuer/audience/azp/nonce/expiry/subject
known ExternalIdentity signin
new Account path only under frozen mailbox-authority rules
email collision → explicit link_required state, never silent merge
provider enrollment state when mailbox authority is insufficient
provider reauthentication and Settings-link semantics only as frozen by M5 contract
canonical DANTE AuthSession issuance only
provider bootstrap staging without overwriting DANTE-owned values
```

Still out of scope until later slices:

```text
Apple callback/code exchange/grant notifications
provider unlink/authenticator management
full WebAuthn ceremonies
password lifecycle adaptation
public M5 FastAPI/OpenAPI/generated client
Access Web UI
real provider/browser final M5 acceptance
Gmail/Calendar/Drive integration scopes
```

---

# 11. Forward execution

```text
M5-C  Google authentication                        NEXT
M5-D  Apple auth + grant/notifications             PLANNED
M5-E  explicit linking/authenticator lifecycle     PLANNED
M5-F  WebAuthn/passkeys                            PLANNED
M5-G  passwordless password/recovery adaptation    PLANNED
M5-H  FastAPI/Pydantic public contract             PLANNED
M5-I  deterministic OpenAPI + governed client      PLANNED
M5-J  Access Web / smart onboarding                PLANNED
M5-K+ focused security/provider/browser/UAT         PLANNED
M6    Native Mobile Access                         PLANNED
M7    Security + Observability + final handoff      PLANNED
```

---

# 12. Testing / acceptance posture

Mandatory layers through later M5:

```text
unit/pure protocol vectors
real PostgreSQL where persistence/races are truthful
FastAPI HTTP contract
OpenAPI/generated client
Web application
browser full-stack
real external-provider acceptance
```

Do not multiply every low-level race across every browser.

Chromium/Firefox/WebKit remain product-critical. Engine-specific WebAuthn/provider limitations are recorded truthfully, not faked.

Real M5 closure requires:

```text
real Google smoke/UAT
real Apple registered-domain smoke/UAT
Apple Private Email Relay sender configuration
real HTTPS WebAuthn/passkey acceptance
manual integrated M5 UAT
explicit user acceptance
```

---

# 13. Whole-vertical state

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
  M5-C NEXT
M6 PLANNED
M7 PLANNED / FINAL GATE

Whole Access/Auth vertical
ACTIVE / NOT CLOSED
```
