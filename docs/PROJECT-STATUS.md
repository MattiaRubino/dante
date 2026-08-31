# DANTE — Project Status

- **Status:** CURRENT TRUTH FOR `feature/access-auth`
- **Last reconciled:** 2026-08-31
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active product vertical:** Access/Auth
- **Current macro-phase:** M5 — Google + Apple + Passkeys + Explicit Linking — **ACTIVE**
- **Last completed execution block:** **GROUP 1 — M5-E + M5-G — Authenticator Lifecycle + Password/Passwordless Adaptation — COMPLETE / ENGINEERING PASS**
- **Next execution block:** **GROUP 2 — M5-F — WebAuthn / Passkeys — NEXT**
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
└── Remaining grouped execution                              3 GROUPS
    ├── GROUP 1  M5-E + M5-G  authenticator lifecycle + password/passwordless   COMPLETE / ENGINEERING PASS
    ├── GROUP 2  M5-F         passkeys/WebAuthn                                  NEXT
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
passwordless Account is valid
verification != setup completion
reauthentication != initial signin
method != factor != assurance
frontend/provider callback != backend-authoritative success
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
```

## 5. Exact next block — Group 2 / M5-F

**Purpose:** add WebAuthn/passkeys as another direct authenticator under the Account-wide lifecycle and anti-lockout model already proved by Group 1.

```text
stable opaque WebAuthnAccount user_handle
registration begin/complete
discoverable username-less authentication
passkey reauthentication
multiple credentials
UV required / resident credential direction / attestation none
credential_id lifetime uniqueness
COSE algorithm persistence
signCount + backup state update policy
label/update/remove
logical revoke
Group-1 anti-lockout integration
canonical DANTE AuthSession only
```

Still out of scope for Group 2:

```text
M5-H public FastAPI materialization
M5-I deterministic OpenAPI / Orval client
M5-J Access Web implementation
M5-K+ real provider/browser/UAT acceptance
provider-data integration scopes
```

## 6. Branch/worktree safety

Continue exactly unless explicitly changed by the user:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not touch `main`, `feature/home-react`, `feature/access-frontend` or `/home/mattia/projects/dante-frontend` without a new explicit topology/write gate.
