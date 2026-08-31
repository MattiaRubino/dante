# DANTE — Project Status

- **Status:** CURRENT TRUTH FOR `feature/access-auth`
- **Last reconciled:** 2026-08-31
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active product vertical:** Access/Auth
- **Current macro-phase:** M5 — Multi-authenticator Account Layer — **ACTIVE**
- **Last accepted execution block:** **GROUP 1 — M5-E + M5-G — COMPLETE / ENGINEERING PASS**
- **Current execution block:** **GROUP 2 — M5-F — WebAuthn / Passkeys — IMPLEMENTATION CANDIDATE ACTIVE / QA PENDING**
- **M5-F PRE-SCOPE:** `64849f2cd60f1d7275344519efdf735eb9c1af95`
- **Current M5-F candidate HEAD:** `0da2d516be8d46b24318404bec494f61a9d9ddc1`
- **Forward execution authority:** `workstreams/access-auth-m4-m7-execution-plan.md`
- **M5 exact design authority:** `architecture/access-auth-m5-persistence-api-contract.md`
- **M5 live handoff:** `workstreams/access-auth-m5-live-handoff-2026-08-29.md`

## 1. Current state

```text
Product / North Star                       CURRENT
Domain Model                               CLOSED
Logical Model                              CLOSED / 57 OF 57
Pre-Physical Coherence                     CLOSED / FINAL QA PASS
Physical PostgreSQL target                 CLOSED
Engineering + Frontend + Backend CP1–CP6  CLOSED / ACCEPTED
Access pre-backend Web materialization     CLOSED / ACCEPTED

Access/Auth M1 — Visual / UX Freeze
CLOSED / ACCEPTED

Access/Auth M2 — Auth Architecture Freeze
CLOSED / ACCEPTED / QA PASS

Access/Auth M3 — Email/Password Signin + AuthSession Spine
CLOSED / ENGINEERING PASS / USER ACCEPTED

Access/Auth M4 — Signup + Verification + Recovery + Reset + Reauth
CLOSED / ENGINEERING PASS / USER ACCEPTED

Access/Auth M5 — Multi-authenticator Account Layer
ACTIVE
├── M5.1 architecture/external-authority freeze              COMPLETE
├── M5.2 exact persistence + API design                      COMPLETE
├── M5-A persistence foundations                             COMPLETE / POSTGRESQL PROVEN
├── M5-B provider/JWK/JOSE/AEAD/WebAuthn infrastructure      COMPLETE / ENGINEERING PASS
├── M5-C Google authentication                               COMPLETE / ENGINEERING PASS
├── M5-D Apple authentication + grant lifecycle              COMPLETE / ENGINEERING PASS
└── grouped execution
    ├── GROUP 1  M5-E + M5-G  authenticator lifecycle + password/passwordless   COMPLETE / ENGINEERING PASS
    ├── GROUP 2  M5-F         passkeys/WebAuthn                                  ACTIVE / CANDIDATE / QA PENDING
    ├── GROUP 3  M5-H + M5-I  public FastAPI + OpenAPI/governed client           PLANNED
    └── GROUP 4  M5-J + M5-K+ Access Web + security/provider/browser/UAT         PLANNED

M6 — Native Mobile Access
PLANNED

M7 — Security Hardening + Observability + Authenticated Handoff
PLANNED / FINAL WHOLE-VERTICAL GATE

Whole Access/Auth vertical
ACTIVE / NOT CLOSED
```

The labels `M5-E` through `M5-K+` remain the frozen semantic decomposition of M5. They are **not seven independent execution gates**. The grouped execution above is authoritative.

## 2. Accepted checkpoints

```text
M4 final implementation
c95e3b2ca664725bcacc374cb5ba6ed49409fe2b

M5-A persistence
7e40e02d301b0812b3f55e0d9d4ce6439e420b2a

M5-B provider/runtime infrastructure
e2d40a7666e3c0130afecd8113b8063390b86b9d

M5-C Google backend
e6f738a1ea3f5152caa7d99f1d6ccd108747c806

M5-D Apple backend
7d13b712f032e8d41d7cf03d406555fd9f3c0160

M5-D documentation closure
1cc331851d52d39f42e922147f300e0370649670

M5-E + M5-G accepted code / formatter checkpoint
1c4b7c988eaae130d6a90d43940a42e2a550870d

M5-E + M5-G documentation / M5-F PRE-SCOPE
64849f2cd60f1d7275344519efdf735eb9c1af95
```

Group 1 / M5-E + M5-G accepted proof:

```text
uv lock --check                              PASS / 57 packages
Ruff format + lint                           PASS
mypy src                                     PASS / 50 source files
backend fast                                 179 / 179 PASS
focused Group-1 PostgreSQL                   16 / 16 PASS
full real PostgreSQL regression              120 / 120 PASS
backend build                                PASS / sdist + wheel
git diff --check                             PASS
scope audit                                  PASS
```

Accepted Group-1 behavior includes provider-neutral method inventory, explicit provider-first link confirmation, logical provider unlink, Apple local-first grant revocation handoff, Account-wide anti-lockout, first-password establishment, safe password removal, passwordless recovery create-or-replace, bearer rotation, Account-lock serialization and concurrent removal proof.

## 3. Current database truth

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

`20260831_13` is an ACL-only forward revision:

```text
GRANT DELETE ON dante.password_credential TO dante_runtime
```

It changes no table shape, mapping, constraint or index. Dictionary/catalog/migration/privilege parity was proved in the Group-1 PostgreSQL regression.

M5-F currently requires **no schema/Alembic/Dictionary change**. The accepted M5-A persistence already supplies `webauthn_account`, `passkey_credential` and `webauthn_challenge` with the required least-privilege runtime ACL. Any future discovered physical insufficiency must be separately re-gated rather than silently widened.

Permanent structural invariant:

```text
Database Dictionary
≈ SQLAlchemy mappings
≈ Alembic head
≈ current PostgreSQL catalog
≈ current human DB reference
≈ direct tests
```

## 4. Binding Auth constitution

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
provider identity key = issuer + subject
provider email != Account/link authority
provider authentication != provider-data integration authorization
provider token/assertion != DANTE AuthSession
passkey credential != Account
WebAuthn user_handle = opaque discoverable Account binding, not email/account UUID
passwordless Account is valid
verification != setup completion
reauthentication != initial signin
method != factor != assurance
frontend/provider/browser callback != backend-authoritative success
unknown/loading != signed-out/signed-in/error
```

Rejected without a bounded architecture gate:

```text
JWT/localStorage browser Auth
Redis/JWT session authority
Principal persistence table
silent provider-email Account merge
provider email as ExternalIdentity key
provider-specific parallel Account/session authority
Account advisory-lock replacement
wide credentialed CORS
fake frontend Auth success
persisted browser Auth cache
provider profile fields dumped into Account
hand-rolled WebAuthn/COSE/signature verification
biometric/PIN/device fingerprint persistence
```

## 5. M5-F implementation candidate — current remote truth

M5-F PRE-SCOPE:

```text
64849f2cd60f1d7275344519efdf735eb9c1af95
```

Current remote candidate HEAD:

```text
0da2d516be8d46b24318404bec494f61a9d9ddc1
```

Remote compare is `ahead 19 / behind 0` and contains exactly these 10 M5-F files:

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

No migration, Dictionary, SQLAlchemy mapping, public FastAPI, OpenAPI/client, frontend or Google/Apple protocol-core file is in the M5-F delta.

Candidate behavior already materialized includes:

```text
real python-fido2 2.2.1 registration/assertion verification
resident credential REQUIRED
user verification REQUIRED
attestation NONE
exact configured RP ID/origin
stable random 32-byte WebAuthn user_handle
verifier-only 32-byte challenge persistence
single-use challenge claim committed before cryptographic verification
cryptographic verification outside DB mutation transaction
COSE public-key persistence + algorithm consistency checks
discoverable username-less passkey signin
fresh canonical DANTE AuthSession on passkey signin
passkey reauthentication on same AuthSession + bearer rotation
safe active-passkey management projection
label-only update
logical passkey revoke
Group-1 Account-wide anti-lockout reuse
monotonic sign-count storage
backup eligibility immutable / backup state current signal
bounded transport/label/resource policy
WebAuthn disabled-default lazy runtime composition
RP ID DNS/localhost validation, IP rejection, HTTPS origins and same-RP origin family
software ES256 authenticator proof through the real fido2 verifier
```

An earlier candidate bug was already fixed before this snapshot: `begin_registration()` no longer requests `FOR UPDATE` on `webauthn_account`; the Account security lock already serializes user-handle creation and the accepted runtime ACL intentionally has only `SELECT + INSERT` there.

## 6. M5-F is NOT accepted yet

Do not mark M5-F COMPLETE/ENGINEERING PASS from implementation presence alone. No authoritative local Ruff/mypy/pytest/build run has yet been recorded for the current M5-F candidate.

The final audit also identified remaining closure work:

```text
1. harden ambiguous authentication/reauthentication reconciliation
   - tolerate a later valid assertion advancing mutable credential observations
   - immutable credential identity/key/algorithm/backup-eligibility must remain exact
   - sign_count must be >= the reconciled assertion
   - last_used_at/updated_at may be later than the ambiguous operation
   - current backup_state must not be required to equal an older assertion after later valid use
   - exact generated AuthSession ref/secret/timestamps remain the authority for signin outcome

2. move passkey signin mutation timestamp/expiry formation to the serialized finalization point
   after the Account security lock, so authoritative chronology follows the committed mutation boundary

3. complete focused real-PostgreSQL/race proof, especially:
   - same credential attempted across two Accounts
   - passkey authentication vs passkey removal
   - Account disable vs passkey signin
   - passkey reauth vs concurrent bearer rotation
   - passkey removal vs password removal
   - concurrent valid assertions / signCount advancement / backup-state advancement
   - operation-specific ambiguous terminal commit reconciliation

4. prove runtime composition explicitly:
   - WebAuthn disabled does not require/read a WebAuthn policy and exposes no passkey service
   - WebAuthn enabled with validated policy creates exactly one passkey service through existing runtime ownership

5. run local candidate QA only after the above writes are complete
```

The frozen security policy remains: a non-increasing signature counter is a **risk signal**, not unconditional authentication failure or Account lock. A safe non-secret warning/telemetry hook may be added during final M5-F hardening; do not turn this into a new blocking counter policy.

## 7. Exact continuation pointer

A new chat must continue **M5-F**, not start M5-H/I and not reopen Group 1.

Required sequence:

```text
verify branch HEAD/current compare
→ review this status + live handoff + M5 frozen contracts
→ fix the known M5-F reconciliation/chronology hardening
→ add the missing deterministic runtime/PostgreSQL race proof
→ PRE-SCOPE 64849f2... → candidate scope audit (still only approved M5-F paths)
→ STOP WRITES
→ user pulls and runs local Ruff/mypy/fast/focused-PG/build QA
→ assistant fixes any defects; user does not patch code manually
→ full PostgreSQL regression once candidate is green
→ materialize local formatter/autofix output exactly
→ final PRE-SCOPE scope/architecture audit
→ only then update closure docs and mark M5-F COMPLETE / ENGINEERING PASS
→ Group 3 / M5-H + M5-I becomes NEXT
```

Real Chromium/Firefox/WebKit WebAuthn behavior remains Group 4 because public FastAPI/Web surfaces do not yet exist. Do not claim browser/production WebAuthn acceptance in M5-F.

## 8. Branch/worktree safety

Continue exactly unless explicitly changed by the user:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not touch `main`, `feature/home-react`, `feature/access-frontend` or `/home/mattia/projects/dante-frontend` without a new explicit topology/write gate.
