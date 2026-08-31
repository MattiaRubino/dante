# DANTE — Access/Auth M4–M7 Execution Plan

- **Status:** CURRENT EXECUTION PLAN / M4 CLOSED / M5 ACTIVE / GROUP 1 COMPLETE / GROUP 2 ACTIVE CANDIDATE
- **Vertical:** Access/Auth
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **Current execution block:** **GROUP 2 — M5-F — WebAuthn / Passkeys — IMPLEMENTATION CANDIDATE / QA PENDING**
- **M5-F PRE-SCOPE:** `64849f2cd60f1d7275344519efdf735eb9c1af95`
- **M5-F implementation snapshot before docs-only handoff commits:** `0da2d516be8d46b24318404bec494f61a9d9ddc1`
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

Implementation/debug responsibility belongs to the assistant. The user runs requested QA commands and returns raw output; do not push manual source patches or Ruff debugging onto the user.

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
real HTTPS Chromium + Firefox + WebKit proof at the appropriate later boundary
```

Permanent Auth rules:

```text
provider identity = issuer + subject
provider email != Account/link authority
provider authentication != provider-data authorization
provider assertion/token != DANTE AuthSession
passwordless Account valid
PasskeyCredential = authenticator, not Account
WebAuthn user_handle = opaque discoverable Account binding
normal provider/passkey removal = logical revoke
no Account before accepted mailbox proof
reauth rotates exact bearer on same AuthSession
network/expensive external verification outside DB mutation transaction
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

GROUP 2 — CURRENT
M5-F
WebAuthn / Passkeys
ACTIVE / IMPLEMENTATION CANDIDATE / QA PENDING

GROUP 3
M5-H + M5-I
Public FastAPI + Deterministic OpenAPI / Governed Client
BLOCKED ON GROUP 2 ACCEPTANCE

GROUP 4
M5-J + M5-K+
Access Web + Security / Provider / Browser / UAT / Acceptance
PLANNED
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

# 6. GROUP 2 — M5-F — Passkeys / WebAuthn — ACTIVE CANDIDATE

## 6.1 Purpose

Add WebAuthn credentials as another first-class direct authenticator under the lifecycle/anti-lockout framework proved by Group 1.

## 6.2 Approved physical scope and current scope audit

M5-F PRE-SCOPE:

```text
64849f2cd60f1d7275344519efdf735eb9c1af95
```

Implementation snapshot before docs-only handoff commits:

```text
0da2d516be8d46b24318404bec494f61a9d9ddc1
```

PRE-SCOPE → snapshot:

```text
ahead 19 / behind 0
10 changed paths
all inside M5-F gate
```

Exact current M5-F paths:

```text
M  apps/backend/.env.example
M  apps/backend/src/dante/auth/contracts.py
A  apps/backend/src/dante/auth/passkey_flow.py
M  apps/backend/src/dante/auth/proofs.py
M  apps/backend/src/dante/auth/provider_flow_runtime.py
M  apps/backend/src/dante/auth/webauthn.py
M  apps/backend/src/dante/platform/config/auth_provider.py
A  apps/backend/tests/integration/auth/test_m5_passkeys.py
A  apps/backend/tests/test_auth_passkey_flow.py
M  apps/backend/tests/test_auth_webauthn.py
```

Still explicitly out of Group 2:

```text
Alembic / new DB structural delta
SQLAlchemy mapping changes
Database Dictionary / Blueprint
public M5 FastAPI routes
OpenAPI / Orval generation
Access Web UI
Google/Apple protocol-core redesign
real provider/browser/WebAuthn UAT
provider-data integration scopes
```

If real proof discovers a physical/ACL insufficiency, STOP and separately re-gate it. Do not silently widen DB privileges/schema.

## 6.3 Materialized candidate behavior

```text
stable opaque random 32-byte WebAuthn user_handle
registration begin/complete
authenticated Account + recent auth for registration
resident credential required
user verification required
attestation none
exact RP ID and explicit allowed HTTPS origin
short single-use challenge
discoverable username-less authentication
passkey reauthentication on same AuthSession
multiple passkeys
credential-id lifetime uniqueness
COSE public-key + algorithm persistence
signCount monotonic update policy
backup eligibility immutable / backup state current verified signal
bounded transport hints and label
safe active-passkey management projection
logical revoke
Group-1 anti-lockout integration
canonical DANTE AuthSession only
bounded challenge/rate cleanup
real python-fido2 2.2.1 verification
```

Challenge ordering is intentionally:

```text
parse bounded response fields
→ atomic conditional challenge claim
→ COMMIT claim
→ real fido2 verification outside DB mutation transaction
→ authoritative Account/session/credential transaction
→ consume claimed challenge
→ commit/reconcile
```

This prevents replay without holding a DB transaction during cryptographic verification.

## 6.4 Already-corrected candidate defects

### WebAuthnAccount lock/ACL mismatch

An earlier candidate requested `SELECT ... FOR UPDATE` on `webauthn_account`. Runtime intentionally owns only the least privilege needed for stable-handle creation (`SELECT + INSERT`).

Correct fix already applied:

```text
remove FOR UPDATE
retain Account security lock
NO ACL widening
```

The Account security lock serializes first `WebAuthnAccount` creation for one Account.

### WebAuthn RP/origin configuration hardening

Candidate validates:

```text
RP ID = localhost or valid DNS domain
IP RP ID rejected
RP ID IDNA/lowercase normalization
origin HTTPS required
origin set unique/non-empty
localhost RP → localhost origin only
other origins → exact RP hostname or subdomain
challenge TTL <= 300 s
```

Before closure perform one final canonicalization check for browser-equivalent origin spellings such as hostname case/default HTTPS port.

## 6.5 Known code hardening still required BEFORE candidate QA

### A. Ambiguous passkey signin reconciliation

Current reconciliation must not require mutable credential state to remain exactly equal to an older assertion after another valid assertion succeeds.

Required successful reconciliation predicate:

```text
credential immutable identity exact:
  ref / account / credential_id / public key / COSE algorithm / backup_eligible

credential monotonic state:
  sign_count >= earlier verified assertion
  last_used_at >= earlier mutation timestamp
  updated_at >= earlier mutation timestamp

backup_state:
  current value may differ after later valid use

challenge:
  consumed

new AuthSession:
  exact generated auth_session_ref
  exact secret_verifier
  exact authenticated_at / recent_auth_at / expires_at
  unrevoked
```

If the generated AuthSession is absent and challenge remains in the expected pre-terminal condition, return only the bounded retryable outcome permitted by the ambiguous-commit policy. Never blindly create a second AuthSession.

### B. Ambiguous reauthentication reconciliation

Same principle for passkey reauth:

```text
credential may have later valid mutable observations
same existing AuthSession must prove exact new bearer verifier
recent_auth_at must prove the reauth commit or a later valid recent-auth state
challenge must be consumed
immutable credential identity remains exact
```

Do not treat a later valid assertion as integrity corruption.

### C. Passkey signin mutation chronology

`complete_authentication()` currently forms mutation timestamp/expiry before the Account security lock. Move authoritative mutation timestamp and expiry derivation to the final serialized mutation transaction after Account lock acquisition.

Why:

```text
cryptographic verification time != authoritative session mutation order
Account security lock defines final security serialization
session chronology should reflect that serialized mutation point
```

### D. Non-increasing positive signCount signal

Frozen policy:

```text
non-increasing counter is a risk signal
!= unconditional failure
!= automatic Account lock
```

A safe non-secret warning/event may be added during hardening. Do not change authentication semantics without a separate security decision.

## 6.6 Current proof already authored

### Pure/protocol

```text
real ES256 software authenticator
real Fido2Server registration verification
real Fido2Server assertion verification
wrong challenge rejection
wrong origin rejection
missing UV rejection
wrong signature rejection
challenge verifier purpose separation + exact width
challenge TTL cap
RP/origin configuration bounds
label/transport bounds
signCount does not decrease
backup eligibility cannot mutate
```

### Real PostgreSQL current tests

```text
registration → management projection → label update
same-Account duplicate credential rejection
discoverable signin
challenge replay rejection
same-session passkey reauthentication
logical revoke
revoked passkey cannot authenticate
concurrent removal of two passkeys preserves one
passkey removal vs provider unlink preserves one direct authenticator under Account lock
```

These tests are committed source, not accepted run evidence yet.

## 6.7 Mandatory focused proof still to add

### Race 1 — same credential across two Accounts

Deterministic shape:

```text
Account A + recent session
Account B + recent session
begin registration for both
use same software credential ID/public key in both valid registration responses
complete concurrently
DB UNIQUE(credential_id) is final arbiter
expected:
  one durable credential wins
  other operation converges to PasskeyAlreadyRegisteredError
  no Account cross-binding
```

### Race 2 — passkey authentication vs passkey removal

```text
Account has password + active passkey
begin anonymous authentication
run REAL fido2 verification
pause after verification with deterministic event/barrier
remove passkey through real remove_passkey transaction
release signin finalization
expected:
  final credential re-read sees revoked/state change
  signin does not create AuthSession
```

The synchronization wrapper may pause around the real verifier result; it must not replace fido2 with `return True`.

### Race 3 — Account disable vs passkey signin

```text
begin signin
real fido2 verification succeeds
pause before final Account transaction
disable Account under canonical Account security lock and commit
release signin
expected:
  AccountUnavailable / no new AuthSession
```

### Race 4 — passkey reauth vs bearer rotation

```text
begin passkey reauth against exact current bearer
real assertion verification succeeds
pause before finalization
perform another real security-sensitive operation on same Account/session that rotates bearer
release reauth
expected:
  frozen old bearer/session snapshot cannot finalize
  AuthStateChanged / no stale reauth commit
```

Do not mutate the DB out-of-band if an existing real lifecycle operation can create the same security event.

### Race 5 — passkey removal vs password removal

```text
Account has password + passkey + recovery-eligible email
two independent AuthSessions
concurrently invoke real remove_passkey and real remove_password
Account security lock serializes both
expected:
  one succeeds
  one AuthenticatorRemovalBlockedError
  exactly one direct authenticator remains
```

### Race 6 — concurrent valid assertions / counter + backup state

```text
one active passkey
issue two independent authentication challenges
valid assertions with increasing counters, e.g. 10 and 11
optionally different valid backup_state observations
complete concurrently
expected:
  both may create independent canonical AuthSessions
  durable sign_count never regresses and reaches >= 11
  no false ambiguous-reconciliation integrity error from a later valid observation
```

### Proof 7 — ambiguous terminal commit reconciliation

Reuse the existing DANTE deterministic fault-injection pattern from accepted AuthSession/provider lifecycle tests if one exists. Do not invent blind retry.

At minimum prove each M5-F reconciler classifies:

```text
exact committed terminal state → success
known pre-commit state → bounded retryable where safe
mismatched/impossible durable state → AuthIntegrityError
```

Critical sign-in rule:

```text
ambiguous AuthSession create
→ lookup generated auth_session_ref
→ never blind second INSERT
```

### Proof 8 — runtime enabled/disabled composition

Prove:

```text
WebAuthn disabled
→ ProviderFlowRuntime.passkey_service is None
→ provider-flow composition does not require/read a WebAuthn policy

WebAuthn enabled with validated policy
→ exactly one PasskeyFlowService is created
→ it reuses existing DatabaseRuntime/AuthRuntime ownership
→ no second HTTP/crypto/session runtime
```

## 6.8 Candidate QA gate — only after sections 6.5–6.7 are finished

Stop remote writes first. Then user pulls exact candidate and runs local authority.

Initial QA shape:

```text
cd /home/mattia/projects/dante

git pull --ff-only
git status --short --branch
git rev-parse HEAD

cd apps/backend

uv lock --check
uv run ruff format <M5-F touched Python/test files>
uv run ruff check --fix .
uv run ruff check .
uv run mypy src
uv run pytest -m "not postgres"
uv run pytest -m postgres tests/integration/auth/test_m5_passkeys.py -q
uv build

cd /home/mattia/projects/dante
git diff --check
git diff --stat
git status --short --branch
```

Rules:

```text
formatter/autofix dirty files are expected
user does NOT manually patch defects
assistant diagnoses static/test failures and edits the branch
no full PostgreSQL regression while candidate still has obvious focused failures
```

When static + fast + focused PG + build are green, run exactly one full backend PostgreSQL regression:

```text
cd /home/mattia/projects/dante/apps/backend
uv run pytest -m postgres
```

Then materialize/commit exact local formatter tree and run final scope/architecture audit.

## 6.9 M5-F closure definition

M5-F can become `COMPLETE / ENGINEERING PASS` only after real evidence proves:

```text
uv lock --check PASS
Ruff format/check/lint PASS
mypy PASS
backend fast PASS
focused real PostgreSQL M5-F PASS
full real PostgreSQL regression PASS
backend build PASS
git diff --check PASS
M5-F PRE-SCOPE scope audit PASS
no unauthorized DB/API/frontend delta
formatter/autofix tree committed
final architecture audit PASS
closure docs reconciled
```

Real browser/WebAuthn acceptance is NOT part of this engineering gate and remains Group 4.

# 7. GROUP 3 — M5-H + M5-I — Public API + Governed Client

Blocked until M5-F closure.

M5-H and M5-I execute together because they form one deterministic contract-delivery pipeline:

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
real WebAuthn/passkey browser/UAT
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
  GROUP 2  M5-F         ACTIVE / CANDIDATE / QA PENDING
  GROUP 3  M5-H + M5-I  BLOCKED ON M5-F ACCEPTANCE
  GROUP 4  M5-J + M5-K+ PLANNED

M6 PLANNED
M7 PLANNED / FINAL GATE
```

Whole Access/Auth remains ACTIVE / NOT CLOSED.
