# DANTE — Access/Auth M5 Live Handoff — 2026-08-29

- **Status:** CURRENT CONTINUATION SAVE-GAME / M5.1–M5-D COMPLETE / GROUP 1 COMPLETE / GROUP 2 M5-F ACTIVE CANDIDATE / QA PENDING
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **Last accepted code checkpoint:** `1c4b7c988eaae130d6a90d43940a42e2a550870d` — Group 1 / M5-E + M5-G
- **Last accepted docs / M5-F PRE-SCOPE:** `64849f2cd60f1d7275344519efdf735eb9c1af95`
- **M5-F implementation candidate snapshot before handoff-doc commits:** `0da2d516be8d46b24318404bec494f61a9d9ddc1`
- **Accepted Alembic head:** `20260831_13`
- **Current execution block:** **M5-F — WebAuthn / Passkeys — implementation candidate; NOT accepted**
- **Architecture authority:** `../architecture/access-auth-m5-contract.md`
- **Exact M5 design authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **Forward plan:** `access-auth-m4-m7-execution-plan.md`

> This file is the live save-game. A new chat must reconstruct state from repository truth, verify the current branch HEAD, then continue the in-flight M5-F candidate from this handoff. Do not replay prior conversations, do not restart M5-F from scratch, do not reopen Group 1 absent direct defect evidence, and do not advance to M5-H/I until M5-F has real QA/closure evidence.

## 1. Mandatory continuation topology

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

New chat != new project, branch or worktree.

Do not touch without a new explicit topology/write gate:

```text
main
feature/home-react
feature/access-frontend
/home/mattia/projects/dante-frontend
```

No merge, rebase, history rewrite, force push or main integration without explicit user authorization.

Before remote writes obey `docs/development/agent-operating-manual.md`: exact branch, PRE-SCOPE SHA, exact CREATE/UPDATE/DELETE paths, purpose/out-of-scope, explicit approval, HEAD race-check and post-write compare.

## 2. Mandatory read order in a new chat

```text
docs/PROJECT-STATUS.md
→ docs/development/agent-operating-manual.md
→ docs/ROADMAP.md
→ docs/workstreams/access-auth.md
→ this file
→ docs/architecture/access-auth-m5-contract.md
→ docs/architecture/access-auth-m5-persistence-api-contract.md
→ docs/workstreams/access-auth-m4-m7-execution-plan.md
→ docs/architecture/access-auth-security-contract.md
→ docs/architecture/access-auth-api-contract.md
→ docs/architecture/access-auth-testing-contract.md
→ ADR-011 and relevant DB authority
→ docs/database/access-auth.md + Database System of Record + Dictionary as needed
→ current M5-F implementation/tests listed below
```

Repository truth beats conversation memory. The two long M5 architecture contracts remain frozen design authority while M5-F is in flight; current operational state lives in this handoff/status/roadmap/execution plan.

## 3. Permanent Auth constitution — do not reinterpret

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal is runtime-derived, never persisted
multiple independent AuthSessions are normal
provider identity key = issuer + subject
provider email != Account/link authority
provider authentication != provider-data authorization
provider assertion/token != DANTE AuthSession
passwordless Account is valid
PasskeyCredential = authenticator, not Account
WebAuthn user_handle = opaque discoverable Account binding
user_handle != email != account_ref
method != factor != assurance
reauthentication != initial signin
frontend/provider/browser completion != backend-authoritative success
```

Rejected unless separately re-gated:

```text
JWT/localStorage browser auth
Redis/JWT session authority
Principal persistence
generic auth/credential god table
silent provider-email merge
provider email as ExternalIdentity identity key
provider-specific Account/AuthSession authority
wide credentialed CORS
fake frontend auth success
hand-rolled WebAuthn/CBOR/COSE/signature crypto
biometric/PIN/device-fingerprint persistence
Account advisory-lock replacement
blind retry of non-idempotent/ambiguous auth mutations
```

Canonical security persistence remains PostgreSQL-backed. Account-wide auth mutations serialize through the accepted Account security lock under READ COMMITTED plus targeted row locks/conditional mutation.

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

Group 1 accepted evidence:

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

Group 1 accepted behavior includes provider-neutral method inventory, explicit provider-first link confirmation, provider unlink, Apple local-first grant-revocation handoff, Account-wide anti-lockout, first password establishment, safe password removal, passwordless recovery create-or-replace, exact retained-session bearer rotation and concurrent authenticator-removal serialization.

## 5. Remaining M5 grouped execution

```text
GROUP 1
M5-E + M5-G
Authenticator Lifecycle + Password/Passwordless Adaptation
COMPLETE / ENGINEERING PASS

GROUP 2 — CURRENT
M5-F
Passkeys / WebAuthn
ACTIVE / IMPLEMENTATION CANDIDATE / QA PENDING

GROUP 3
M5-H + M5-I
Public FastAPI + OpenAPI / Governed Client
BLOCKED ON M5-F ACCEPTANCE

GROUP 4
M5-J + M5-K+
Access Web + Final Security / Provider / Browser / UAT Acceptance
PLANNED
```

Do not revert to the old seven-step E→F→G→H→I→J→K execution sequence. The labels remain semantic ownership labels; the four grouped blocks are the current execution plan.

## 6. M5-F approved gate and scope

M5-F PRE-SCOPE:

```text
64849f2cd60f1d7275344519efdf735eb9c1af95
```

Approved purpose:

```text
materialize passkeys/WebAuthn as a first-class direct authenticator
under the Account-wide lifecycle + anti-lockout authority proved by Group 1
without public API/Web materialization and without changing DB structure unless direct evidence forces a re-gate
```

Current candidate code snapshot before docs-only handoff reconciliation:

```text
0da2d516be8d46b24318404bec494f61a9d9ddc1
```

Remote compare PRE-SCOPE → candidate:

```text
ahead 19
behind 0
10 changed files
all inside approved M5-F gate
```

Exact candidate files:

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

Explicitly absent from the candidate:

```text
Alembic / migration
SQLAlchemy mapping
Database Dictionary / DB Blueprint
public FastAPI M5 route
OpenAPI / Orval / generated client
React / Access Web
Google protocol core
Apple protocol core
main / other branch/worktree
```

M5-F has therefore not changed accepted DB shape or Alembic head. Existing M5-A persistence/ACL is intentionally reused.

## 7. M5-F implementation already materialized

### 7.1 `webauthn.py` — protocol/policy boundary

Uses the real pinned `python-fido2==2.2.1` runtime, not a Boolean test stub.

Materialized policy:

```text
residentKey       REQUIRED
userVerification  REQUIRED
user presence     required by Fido2Server verification
attestation        NONE
RP ID              exact configured authority
origin             exact configured canonical set
challenge          32-byte CSPRNG
credential ID      bounded to persistence contract
COSE public key    bounded to persistence contract
```

Responsibilities:

```text
registration option generation
assertion option generation
response parsing for bounded routing evidence
Fido2Server.register_complete verification
Fido2Server.authenticate_complete verification
RP hash/origin/challenge/UP/UV/signature enforcement
COSE public-key canonical serialization
COSE reconstruction through CoseKey.parse
algorithm-vs-persisted-metadata consistency check
AttestedCredentialData reconstruction with Aaguid.NONE for signature verification
```

DANTE does not persist AAGUID, biometric template, device PIN or device fingerprint. AAGUID is not required to verify the stored public credential key.

### 7.2 `proofs.py` — challenge capability boundary

WebAuthn uses the existing purpose-separated proof machinery:

```text
raw 32-byte challenge
→ purpose-specific verifier
→ only verifier persisted
```

The raw WebAuthn challenge is never stored as durable authority and is never logged.

### 7.3 `passkey_flow.py` — M5-F application/persistence state machine

This is currently a large single M5-F state machine. Do not split it cosmetically before proof. Refactor only if a real responsibility/transaction boundary justifies it.

#### Registration begin

```text
exact configured origin
→ bounded begin limiter
→ expired-challenge cleanup
→ decode/verify current bearer
→ Account security lock
→ current AuthSession re-read
→ recent-auth required
→ read/create stable WebAuthnAccount
→ random 32-byte user_handle on first creation
→ verified EmailIdentity chosen deterministically only as authenticator display metadata
→ collect lifetime Account credential IDs for exclusion
→ create verifier-only WebAuthn challenge
→ bind exact Account + AuthSession + bearer verifier + user_handle + RP ID + origin
→ commit
→ generate WebAuthn registration options
```

Important already-fixed defect:

```text
EARLIER CANDIDATE
SELECT WebAuthnAccount ... FOR UPDATE

PROBLEM
runtime ACL intentionally has SELECT + INSERT, not UPDATE

FIX
remove FOR UPDATE
Account security lock already serializes WebAuthnAccount/user_handle creation
NO ACL widening
```

#### Registration complete

```text
parse bounded response evidence
→ complete limiter
→ atomic conditional challenge claim (`claimed_at`) and COMMIT
→ replay is now durably blocked
→ real fido2 crypto verification OUTSIDE DB mutation transaction
→ Account security lock
→ current AuthSession/bearer/recent-auth recheck
→ exact WebAuthnAccount/user_handle recheck
→ lifetime credential_id duplicate check
→ persist public credential only
→ consume claimed challenge
→ rotate exact retained AuthSession bearer
→ commit / operation-specific ambiguous reconciliation
```

Persisted passkey state:

```text
passkey_credential_ref
account_ref
credential_id
COSE public key bytes
COSE algorithm
sign_count
backup_eligible
backup_state
bounded transports
label
status/timestamps
last_used_at
revocation state
```

No private key or authenticator secret is persisted.

#### Discoverable authentication

Begin:

```text
anonymous allowed
no allowCredentials restriction
exact RP/origin + random verifier-only challenge
```

Complete:

```text
claim single-use challenge before crypto
→ require 32-byte userHandle
→ resolve active credential by credential_id
→ exact durable WebAuthnAccount user_handle match
→ real fido2 signature/UP/UV/RP/origin verification
→ Account security lock
→ active Account + immutable credential recheck
→ monotonic credential usage-state update
→ consume challenge
→ create fresh canonical DANTE AuthSession
→ commit / ambiguous reconciliation
```

`user_handle`, not email and not `account_ref`, is the discoverable credential binding.

#### Reauthentication

```text
current AuthSession required
already-recent auth NOT required
begin binds challenge to exact Account/session/bearer/user_handle
allowCredentials = active passkeys for that Account
real fido2 assertion verification
Account security lock + exact frozen bearer/session recheck
credential state update
challenge consume
recent_auth_at refresh
same auth_session_ref
bearer rotation
```

#### Management

```text
list_passkeys
→ active safe projection only
→ ref / label / transports / backup flags / created_at / last_used_at
→ no credential ID/public key/user_handle exposure

update_label
→ label only
→ no authentication/security-evidence mutation

remove_passkey
→ recent auth
→ Account security lock
→ active credential recheck
→ Group-1 authenticator inventory re-read
→ subtract this passkey
→ anti-lockout decision
→ logical revoke, never DELETE
→ same-session bearer rotation
```

### 7.4 Counter and backup policy

Current implementation:

```text
sign_count = max(stored, verified observed)
backup_eligible is immutable lifetime credential metadata
backup_state is current verified signal
last_used_at/updated_at advance on successful assertion
```

Frozen security rule:

```text
non-increasing signCount != unconditional auth failure
non-increasing positive counter = risk signal
risk signal != automatic Account lock
```

A safe non-secret logging/telemetry hook may be added while hardening M5-F; do not turn this into a blocking counter policy without a new security decision.

### 7.5 Runtime composition

`ProviderFlowRuntime` now owns an optional `passkey_service` alongside provider/authenticator services while reusing existing process resources.

```text
WebAuthn disabled
→ no PasskeyFlowService
→ no requirement to read/build WebAuthn policy in provider-flow composition

WebAuthn enabled
→ AuthRuntime owns one validated WebAuthnPolicy
→ ProviderFlowRuntime constructs one PasskeyFlowService
→ dedicated bounded begin/complete limiters
```

No second HTTP/session/crypto runtime authority is introduced.

### 7.6 Configuration hardening already present

WebAuthn settings now include bounded challenge lifetime and process-local ingress limits.

Accepted candidate validation direction:

```text
RP ID = localhost or valid DNS domain
IP address RP ID rejected
RP ID normalized lower-case/IDNA
origin must be HTTPS
origin set non-empty + unique
localhost RP requires localhost origin
non-localhost origin host must equal RP ID or be its subdomain
challenge lifetime <= 300 seconds
```

One final quality check remains worthwhile before closure: ensure origin canonicalization/rejection is strict enough that accepted configuration cannot differ from browser canonical origin merely by host case/default HTTPS port representation.

## 8. Test proof already present in source

### Fast / protocol proof

`tests/test_auth_webauthn.py` uses a real software ES256 authenticator path against `python-fido2`:

```text
positive registration
positive assertion
exact RP/origin policy
resident-required direction
UV required
attestation none
wrong challenge rejected
missing UV rejected
wrong origin rejected
wrong signature rejected
```

`tests/test_auth_passkey_flow.py` currently proves:

```text
challenge TTL capped at five minutes
RP ID/origin configuration bounds
purpose-separated exact-width challenge verifier
label/transport bounds
non-decreasing sign-count storage
backup eligibility cannot change
```

### Real PostgreSQL proof already written

`tests/integration/auth/test_m5_passkeys.py` currently contains real PostgreSQL + real fido2 scenarios for:

```text
register → list → label update
same-Account duplicate credential rejection
discoverable passkey signin
challenge replay rejection
reauthentication on same AuthSession
logical removal
revoked passkey cannot authenticate
concurrent two-passkey removal preserves one authenticator
passkey removal vs provider unlink shares Account-wide lock and preserves one authenticator
```

This source-level proof exists but has **not yet been accepted by a local QA run for the current M5-F candidate**.

## 9. Known candidate hardening still required before QA

### 9.1 Ambiguous signin / reauth reconciliation must tolerate later valid assertions

Current candidate reconciliation is too strict about mutable credential observations. A later valid assertion may legitimately advance `last_used_at`, `updated_at`, `sign_count` or current `backup_state` before an earlier ambiguous operation reconciles.

Do not require an older assertion's mutable state to remain the latest current state.

Required reconciliation direction:

```text
immutable credential identity must remain exact:
  passkey_credential_ref
  account_ref
  credential_id
  public key
  COSE algorithm
  backup_eligible

monotonic state:
  persisted sign_count >= reconciled assertion sign_count
  persisted last_used_at >= reconciled operation mutation time
  persisted updated_at >= reconciled operation mutation time

current backup_state:
  may have changed due to a later valid assertion
  do NOT require equality with the older ambiguous assertion

passkey signin outcome authority:
  generated AuthSession ref exact
  generated secret verifier exact
  authenticated/recent timestamps exact
  expiry exact
  session unrevoked
  challenge consumed
```

Reauthentication similarly must tolerate later credential usage while preserving exact same-session bearer/recent-auth evidence for the reauth commit.

### 9.2 Authoritative passkey-signin mutation time

Current `complete_authentication()` forms `mutation_at`/expiry before acquiring the Account security lock. Move authoritative mutation timestamp/expiry formation to the serialized finalization boundary after the Account lock so chronology corresponds to the actual canonical mutation order.

### 9.3 Focused deterministic proof still missing

Before M5-F candidate QA/closure add direct proof for:

```text
same credential attempted across two Accounts
passkey authentication vs passkey removal
Account disable vs passkey signin
passkey reauth vs concurrent bearer rotation
passkey removal vs password removal
concurrent valid assertions on the same credential
signCount monotonic advancement under concurrency
backup-state advancement/change under concurrent valid assertions
operation-specific ambiguous terminal commit reconciliation
runtime enabled/disabled composition
```

Use real PostgreSQL and real fido2 verification where the cryptographic boundary is material. It is acceptable to pause after real verification with deterministic synchronization to create a race; do not mock the verifier into returning True and do not use `sleep()` as primary race synchronization.

Suggested deterministic race shapes are documented in `access-auth-m4-m7-execution-plan.md`.

## 10. M5-F QA has NOT happened yet

Do not infer PASS from committed implementation/tests.

No accepted current-candidate evidence yet exists for:

```text
uv lock --check
Ruff format/check/lint
mypy src
full non-postgres backend suite
focused M5-F PostgreSQL suite
backend build
full PostgreSQL regression
git diff --check
formatted candidate scope audit
```

The user must not patch/debug code. Assistant modifies branch files; user only runs the requested QA commands and returns raw output.

Local toolchain is authority:

```text
ruff format          → materialize formatter
ruff check --fix     → safe autofix
ruff check           → remaining findings
mypy src             → strict type proof
pytest               → application/real-PG proof
uv build             → package proof
```

Do not hand-edit `uv.lock`; `uv==0.12.5` local repository toolchain is authority.

## 11. Exact next execution sequence

A new chat should do exactly this:

```text
1. verify current `feature/access-auth` HEAD and compare from M5-F PRE-SCOPE `64849f2...`
2. read this handoff + current status/roadmap/execution plan + frozen M5 contracts
3. inspect current 10-file M5-F delta; do not restart implementation
4. fix reconciliation tolerance + mutation-time hardening in existing approved M5-F files
5. add the missing deterministic runtime/PG race proof in existing approved test files
6. re-run PRE-SCOPE → candidate scope audit; expected scope remains M5-F-only
7. STOP REMOTE WRITES
8. user pulls current branch
9. user runs local candidate QA supplied by assistant
10. assistant diagnoses/fixes any failures; user does not patch source manually
11. once static + fast + focused PG + build are green, run one full PostgreSQL regression
12. user materializes local Ruff formatter/autofix output only when assistant requests it
13. commit/push the exact locally-tested formatter tree
14. assistant performs final architecture + PRE-SCOPE scope audit
15. update all M5 authority/closure docs
16. mark M5-F COMPLETE / ENGINEERING PASS only from real evidence
17. set GROUP 3 / M5-H + M5-I as NEXT
```

Do not start public FastAPI/OpenAPI/client or Web while M5-F is still a candidate.

## 12. M5-F closure criteria

M5-F closes only when all of these are true:

```text
frozen registration/signin/reauth/management semantics materialized
no schema/ACL drift or separately re-gated if direct evidence proves one is required
real fido2 verifier used by mandatory automated proof
challenge single-use/replay proof
credential lifetime uniqueness proof
Account/session/user_handle exact binding proof
Group-1 anti-lockout integration proof
cross-authenticator removal race proof
Account-disable/session-rotation race proof
counter/backup state concurrency proof
ambiguous outcome reconciliation proof
runtime enabled/disabled composition proof
Ruff PASS
mypy PASS
fast backend PASS
focused real PostgreSQL M5-F PASS
full real PostgreSQL regression PASS
backend build PASS
git diff --check PASS
PRE-SCOPE scope audit PASS
formatter tree materialized and committed
closure docs reconciled
```

Real Chromium/Firefox/WebKit authenticator behavior, production RP/domain setup and full browser WebAuthn UAT remain Group 4. M5-F ENGINEERING PASS must not be described as final browser/production acceptance.

## 13. Later groups

```text
GROUP 3 / M5-H+I
FastAPI/Pydantic
→ exact frozen /api/v1 routes
→ RFC9457/no-store/request IDs
→ deterministic OpenAPI
→ Orval Fetch/Zod
→ governed @dante/api-client
→ drift/determinism tests

GROUP 4 / M5-J+K+
Access Web
→ Google/Apple/passkey/password surfaces
→ provider enrollment/link/security management
→ browser matrix
→ real Google UAT
→ real Apple registered-domain UAT
→ Apple Private Email Relay sender proof
→ real WebAuthn/passkey UAT
→ final races/HTTP/client/PostgreSQL proof as applicable
→ manual M5 UAT
→ docs + explicit user acceptance
```

## 14. Working style for the next assistant

- Respond in Italian unless user asks otherwise.
- Be direct and technical; green means evidence, not a label.
- Do not ask the user to repeat project context already in repository/handoff.
- Do not ask the user to manually patch code or debug Ruff/mypy/pytest findings.
- Assistant edits implementation; user runs QA commands and pastes output.
- Local formatter/toolchain output is authoritative; do not guess formatting.
- Do not run full expensive PostgreSQL regression after every small edit; use focused proof during development and one full regression at candidate closeout.
- Do not refactor large auth flow files merely to reduce line count; extract only on real responsibility/transaction boundaries.
- Do not broaden DB/API/frontend scope opportunistically.
- Do not claim provider/browser/production readiness from backend engineering proof.
