# DANTE — Project Status

- **Status:** CURRENT TRUTH FOR `feature/access-auth`
- **Last reconciled:** 2026-09-01
- **Protected `main`:** integrated source authority; Access/Auth remains branch-local until explicit merge gate
- **Active product vertical:** Access/Auth
- **Current macro-phase:** M5 — Multi-authenticator Account Layer — **ACTIVE**
- **Last accepted execution block:** **GROUP 3 — M5-H + M5-I — COMPLETE / ENGINEERING PASS**
- **Current execution block:** **GROUP 4 — M5-J + M5-K+ — Access Web + browser/provider/security/UAT — NEXT**
- **Group 3 PRE-SCOPE:** `ee099dc7c6bef4742c6e66e5d15f9a0428dd8ffa`
- **Group 3 engineering checkpoint:** `05b348e9e0293cd9cd0cc3f190824527761b24d9`
- **Accepted Alembic head:** `20260831_13`
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
    ├── GROUP 2  M5-F         passkeys/WebAuthn                                  COMPLETE / ENGINEERING PASS
    ├── GROUP 3  M5-H + M5-I  public FastAPI + OpenAPI/governed client           COMPLETE / ENGINEERING PASS
    └── GROUP 4  M5-J + M5-K+ Access Web + security/provider/browser/UAT         NEXT

M6 — Native Mobile Access
FUTURE / OPTIONAL / ONLY IF DELIBERATELY RE-GATED

M7 — Security Hardening + Observability + Authenticated Handoff
PLANNED / FINAL WHOLE-VERTICAL GATE

Whole Access/Auth vertical
ACTIVE / NOT CLOSED
```

The labels `M5-E` through `M5-K+` remain the frozen semantic decomposition of M5. They are not seven independent execution gates. The grouped execution above is authoritative.

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

GROUP 1 / M5-E + M5-G
1c4b7c988eaae130d6a90d43940a42e2a550870d

GROUP 2 / M5-F final engineering checkpoint
f6a8da43fbe674ca18c366cd3731afc8f97ec045

GROUP 3 / M5-H + M5-I PRE-SCOPE
ee099dc7c6bef4742c6e66e5d15f9a0428dd8ffa

GROUP 3 / M5-H + M5-I engineering checkpoint
05b348e9e0293cd9cd0cc3f190824527761b24d9
```

## 3. Group 2 accepted proof

M5-F / Passkeys is closed at the engineering layer. Real browser/hardware WebAuthn acceptance intentionally remains Group 4.

```text
uv lock --check                  PASS / 57 packages
Ruff                             PASS
mypy src                         PASS / 51 source files
non-PostgreSQL                   191 PASS / 132 deselected
PostgreSQL                       132 PASS / 191 deselected
total                            323 PASS
backend build                    PASS
git diff --check                 PASS
scope audit                      PASS
```

Accepted behavior includes real `python-fido2` verification, resident credentials + UV required, discoverable signin, passkey registration/reauthentication/removal, Account-wide anti-lockout, monotonic credential-state handling, deterministic race proof and canonical DANTE AuthSession authority.

## 4. Group 3 accepted proof

Group 3 materialized the full frozen public M5 Auth contract and governed client boundary.

```text
Backend static quality
uv lock --check                  PASS / 57 packages
Ruff lint                        PASS
Ruff format --check              PASS / 100 files
mypy src                         PASS / 56 source files

HTTP / OpenAPI
focused M5 HTTP/OpenAPI           35 PASS
full non-PostgreSQL regression    225 PASS / 134 deselected
backend build                     PASS / sdist + wheel

Real PostgreSQL
provider-continuation authority   2 PASS
full PostgreSQL regression        134 PASS / 225 deselected

Governed client
ESLint                            PASS
TypeScript                        PASS
Vitest                            11 PASS
OpenAPI/Orval/Zod drift proof     PASS / deterministic and current / 78 files

Workspace
architecture check                PASS / 151 modules / 287 dependencies
typecheck                         PASS / 6 of 6 packages
build                             PASS / 2 of 2 build tasks
git diff --check                  PASS
final worktree                    CLEAN / SYNCED

Scope audit
PRE-SCOPE ee099dc7... → 05b348e9...
ahead-only                        PASS
DB/Alembic/ACL/frontend spill     NONE
```

Group 3 public surface now includes:

```text
methods + password lifecycle
provider enrollment
provider link + unlink
Google begin/complete
Apple begin/callback/notifications
passkey registration/authentication/reauthentication/update/remove
stable /api/v1 operationIds
RFC 9457 typed problems
request IDs + Cache-Control: no-store
same-origin browser security
Apple form_post isolated ingress
opaque HttpOnly provider continuation cookies
deterministic OpenAPI
Orval Fetch + generated Zod
governed @dante/api-client
strict success-payload widening rejection
```

Apple callback/notifications are backend ingress and are intentionally not exported as ordinary browser-client calls.

## 5. Current database truth

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

`20260831_13` is ACL-only and grants the governed runtime DELETE needed for safe password removal. Group 2 and Group 3 required no new schema, Alembic, Dictionary or ACL widening.

Permanent structural invariant:

```text
Database Dictionary
≈ SQLAlchemy mappings
≈ Alembic head
≈ current PostgreSQL catalog
≈ current human DB reference
≈ direct tests
```

## 6. Binding Auth constitution

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

## 7. Exact continuation pointer

The next implementation block is **GROUP 4**, not more Group 3 backend work.

```text
GROUP 4 — M5-J + M5-K+
Access Web + Final M5 Browser / Provider / Security / UAT
```

Group 4 must materialize the Web flows against the governed client and then prove real browser/provider/passkey behavior. It owns real Google smoke/UAT, real Apple registered-domain smoke/UAT, Apple Private Email Relay sender configuration, real WebAuthn/passkey UAT, browser matrix, final integrated M5 security/browser proof and explicit user acceptance.

M5 does not close merely because Group 3 is engineering-pass. Whole M5 closure requires Group 4 acceptance.

## 8. Branch/worktree safety

Continue exactly unless explicitly changed by the user:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not touch `main`, `feature/home-react`, `feature/access-frontend` or `/home/mattia/projects/dante-frontend` without a new explicit topology/write gate.
