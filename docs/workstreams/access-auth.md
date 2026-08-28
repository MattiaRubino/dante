# DANTE — Access/Auth Full-Stack Vertical Workstream

- **Status:** ACTIVE VERTICAL / M1–M3 CLOSED / M4 NEXT
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Created from protected `main`:** `f011e252b6a294a12c38927ef2d528244ea1fee6`
- **M3 accepted implementation candidate before closure-doc reconciliation:** `d8a47f1cce271b1db30a53eff729f34501fe838a`
- **Current macro-phase:** `M4 — Signup + Verification + Recovery + Reset + Reauth` — NEXT / NOT STARTED
- **Last closed macro-phase:** `M3 — Email/Password Signin + AuthSession Spine` — CLOSED / ENGINEERING PASS / USER ACCEPTED
- **Purpose:** durable operational authority for the production Access/Auth vertical, including branch safety, accepted architecture, executable evidence, reopen rules and the next safe implementation boundary.

> A new chat is not a new project, branch or worktree. Continue this vertical on `feature/access-auth` and `/home/mattia/projects/dante` until the whole Access/Auth vertical is closed or the user explicitly re-gates the repository topology.

---

## 1. Mandatory continuation bootstrap

Continue exactly:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

The separate `/home/mattia/projects/dante-frontend` worktree is a real frontend worktree for independent frontend work such as Home. It is **not** the Access/Auth worktree and must not receive Access/Auth implementation merely because the changed files are frontend files.

Before any write:

```bash
pwd
git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
git rev-parse origin/feature/access-auth
git worktree list --porcelain
```

Read at minimum:

1. root `README.md`;
2. `docs/PROJECT-STATUS.md`;
3. `docs/ROADMAP.md`;
4. `docs/development/agent-operating-manual.md`;
5. `docs/development/documentation-lifecycle-policy.md`;
6. this file;
7. `docs/frontend/access.md`;
8. `docs/architecture/access-auth-architecture.md`;
9. `docs/architecture/access-auth-security-contract.md`;
10. `docs/architecture/access-auth-api-contract.md`;
11. `docs/architecture/access-auth-testing-contract.md`;
12. `docs/decisions/ADR-011-access-auth-architecture.md`;
13. `docs/database/README.md`, `docs/database/dante-postgresql-database.md` and `docs/database/access-auth.md` when persistence is relevant.

Repository truth beats conversation memory.

---

## 2. Authority and documentation lifecycle

Use the strictest applicable current source:

```text
accepted Domain / Logical / Physical / ADR decisions
+ current implementation / migrations / tests
↓
current durable architecture / security / API / testing / DB / frontend docs
↓
this branch-local workstream for current phase state and handoff
↓
historical branch records / frozen evidence
↓
conversation memory
```

Permanent database reconciliation invariant:

```text
Database current reference
≈ Database Dictionary
≈ SQLAlchemy mappings
≈ Alembic head
≈ real PostgreSQL catalog
≈ direct tests
```

Historical CP6 evidence remains historical. Current/evolving references must move when an accepted later product slice changes current truth.

---

## 3. Non-negotiable semantic constitution

Preserve unless a stronger explicit architecture gate reopens the exact choice:

```text
Person != Account
Account != Principal
Principal != Actor
AuthSession != DANTE Session
signin != provider-data integration authorization
provider state != canonical DANTE state
verification != setup completion
reauthentication != initial signin
client/device signal != identity
frontend request/success != backend-authoritative success
method != factor != assurance
```

Account/Auth model:

```text
Account = durable access/security root
EmailIdentity != Account
PasswordCredential optional
Account may be passwordless
ExternalIdentity key = issuer + subject
provider email never silently links Accounts
Account may have 0..N PasskeyCredential
Principal remains runtime-only absent stronger evidence
AuthSession belongs to Account, not to one authenticator
multiple independent AuthSessions are normal
```

Do not reopen JWT/localStorage browser Auth, Redis/JWT session authority, a Principal table, silent provider-email merge, Account advisory locking, Axios, generated React Query hooks, wide credentialed CORS or fake frontend Auth success without a separately justified architecture reopen.

---

## 4. Closed macro-phases

### M1 — Access Visual / UX Freeze

**Status:** `CLOSED / ACCEPTED`

The existing Web Access composition is the production baseline. It is not disposable mock UI and must not be redesigned for novelty during backend work.

Important carry-forward rules:

```text
systematic geometry/tokens
responsive/mobile-Web behavior remains platform appropriate
frontend may own local navigation/form transitions
backend-authoritative success may never be fabricated
```

### M2 — Auth Architecture Freeze

**Status:** `CLOSED / M2.1–M2.11 ACCEPTED / DOCUMENTED / READBACK QA PASS`

Durable authority:

```text
docs/architecture/access-auth-architecture.md
docs/architecture/access-auth-security-contract.md
docs/architecture/access-auth-api-contract.md
docs/architecture/access-auth-testing-contract.md
docs/decisions/ADR-011-access-auth-architecture.md
```

M2 fixed the browser/session/security/API/generated-client/transaction/test architecture under which M3 was implemented.

### M3 — Email/Password Signin + AuthSession Spine

**Status:** `CLOSED / ENGINEERING GATE PASS / USER ACCEPTANCE ACCEPTED`

M3 is the first real authenticated DANTE path. It is **not** the closure of the whole Access/Auth vertical; M4–M7 remain.

---

## 5. M3 implementation — authoritative summary

### 5.1 Database

Current branch database:

```text
PostgreSQL          18.6
Alembic head        20260827_10
72 tables
5 views
15 routines
75 triggers
104 physical indexes
71 foreign keys
137 CHECK constraints
92 standalone Dictionary entries
```

M3 materialized:

```text
dante.account
dante.email_identity
dante.password_credential
dante.auth_session
dante.acquire_account_security_lock(uuid)
```

Representation chain is aligned across:

```text
Alembic 20260827_09 + 20260827_10
SQLAlchemy mappings + mapping registry
Database Dictionary
whole-DB current reference
docs/database/access-auth.md
real PostgreSQL catalog/tests
```

`DB-U09 Account persistence` is resolved/materialized. `DB-U10 Principal persistence` is resolved **without** a Principal table.

`dante_runtime` still cannot directly UPDATE Account or issue direct Account `SELECT ... FOR UPDATE`. Account-wide security serialization uses only the narrow migration-owned `SECURITY DEFINER` function `dante.acquire_account_security_lock(uuid)`.

### 5.2 Backend runtime/API

Production backend spine:

```text
POST   /api/v1/auth/signin
GET    /api/v1/auth/session
DELETE /api/v1/auth/session
```

Implemented semantics include:

```text
email normalization/comparison
Argon2id v19 64 MiB / t=3 / p=4
HMAC-SHA256 separate pepper
HIBP k-anonymity integration
bounded KDF concurrency/admission
unknown-account dummy verification
opaque DB-backed AuthSession
runtime Principal derivation
__Host-dante-session Secure/HttpOnly/Path=/SameSite=Lax
session-bound CSRF
Origin + Fetch Metadata + X-Dante-Client fail-closed Web ingress
current-session logout/revocation
ambiguous AuthSession commit reconciliation without blind retry
Cache-Control: no-store on sensitive Auth responses
RFC9457 application/problem+json with stable machine code/category/request_id/retryable
```

### 5.3 OpenAPI and generated client

M3 materialized the governed client chain:

```text
FastAPI/Pydantic
→ deterministic committed OpenAPI 3.1 snapshot
→ Orval Fetch
→ generated TypeScript + Zod
→ framework-neutral @dante/api-client
→ Web transport/application boundary
```

Important invariants:

```text
Axios                         NOT SELECTED
Orval React Query hooks       NOT SELECTED
raw generated operations      not public app API
hand-edited generated output  FORBIDDEN
remote DEV OpenAPI in CI      FORBIDDEN
browser Auth cache persistence NOT SELECTED
```

The governed client returns typed remote outcomes and validates status/media type/payload/request-id/cache-policy expectations at runtime.

### 5.4 Web integration

The production Web path is real:

```text
TanStack Router
→ Access feature public API
→ TanStack Query remote lifecycle
→ Web Auth remote adapter
→ @dante/api-client
→ same-origin /api/v1
```

Web transport owns browser concerns:

```text
credentials: same-origin
Accept JSON/problem
X-Dante-Client: web
CSRF only on authenticated unsafe mutation
AbortSignal propagation
no manual Origin/Sec-Fetch-Site forging
```

Mutation retry is disabled. Session GET may use only the bounded accepted transient retry policy.

The Access reducer still distinguishes user intent from server authority:

```text
REQUEST_SIGN_IN
!= authenticated state

SERVER_AUTHENTICATED
→ authenticated transition
```

No Auth state is stored in localStorage/sessionStorage.

---

## 6. M3 browser bootstrap rule — permanent regression guard

A manual UAT defect exposed an important application-level rule.

### 6.1 Defect observed

Original M3 Web wiring initialized the Access reducer in `SIGN_IN`, then resolved `GET /auth/session` asynchronously. On an authenticated F5, the login screen could paint briefly before the server-authoritative session arrived.

A first attempted mitigation kept a real sign-in panel in layout but hid its form during bootstrap. That removed the visible login flash but produced perceptible geometry/recomposition during refresh and was rejected in manual UAT.

### 6.2 Accepted professional pattern

Critical bootstrap data must be resolved before the route component is mounted:

```text
hard refresh
→ TanStack Router loader
→ ensure/prefetch authoritative /auth/session
→ Query cache populated
→ AccessPage mounts
→ first Access render already SIGNED_IN or SIGNED_OUT
```

The route imports the Auth bootstrap query only through the **Access feature public API**, never through a deep feature import.

The initial session value is temporarily fresh (`staleTime` bounded to the bootstrap handoff) so loader → component mount does not immediately trigger a duplicate session read. Later refetches remain background lifecycle and must not reset the UI to a false loading/signed-out state.

### 6.3 Forbidden bootstrap anti-patterns

Do not reintroduce:

```text
unknown session == signed out
paint login first, repair after effect
hidden sign-in form as geometry placeholder
blank authenticated state replaced after useEffect
route deep-import of Access application internals
persisted client Auth cache as canonical state
```

General DANTE remote-state rule:

```text
unknown/loading
!= empty/signed-out
!= populated/signed-in
!= error
```

When a remote fact is critical to the correctness of the first screen, model it explicitly and resolve it at the appropriate route/bootstrap boundary instead of briefly rendering a false business state.

### 6.4 Manual refresh acceptance

Manual Firefox video review after the Router-first implementation established:

```text
login flash                    eliminated
card/brand/topbar geometry     stable across app render
brief browser document blank   normal hard-reload repaint, not Auth state churn
user acceptance                ACCEPTED
```

Do not reopen M3 merely to eliminate a browser-owned single-frame document repaint. A future global Web shell/bootstrap optimization may address document-paint polish if it becomes a product-wide requirement, but it is not an Auth defect.

---

## 7. M3 executable proof

### 7.1 Backend / PostgreSQL

Accepted evidence:

```text
fast non-PostgreSQL pytest                 73 / 73 PASS
package build                              PASS
real PostgreSQL 18.6 marked suite          83 / 83 PASS
real signin/session integration            4 / 4 PASS
migration/current catalog                  PASS
Dictionary ↔ SQLAlchemy ↔ Alembic ↔ PG    PASS
runtime ACL + Account security lock        PASS
transaction / ambiguous outcome            PASS
runtime outage/readiness recovery          PASS
CP6 historical regression                  PASS
```

### 7.2 Web static/unit/build

Accepted evidence:

```text
TypeScript typecheck             PASS
ESLint                          PASS
Vitest                          6 files / 25 tests PASS
architecture dependency cruise  PASS
Prettier                        PASS
production Vite build           PASS
generated:check                 PASS
```

### 7.3 Real cross-stack browser proof

Harness topology:

```text
Playwright
→ HTTPS Vite production preview
→ same-origin /api/v1 proxy
→ real FastAPI process
→ real SQLAlchemy async runtime
→ disposable PostgreSQL 18.6
```

External HIBP behavior uses a protocol-faithful local substitute. TLS material, passwords, peppers and database credentials are synthetic/ephemeral.

Critical matrix:

```text
7 scenarios × 3 browser engines = 21 / 21 PASS

Chromium  7 / 7
Firefox   7 / 7
WebKit    7 / 7
```

Scenarios:

1. real signin + cookie contract + delayed bootstrap regression + logout;
2. invalid credentials remain unauthenticated with safe public feedback;
3. two independent BrowserContexts/AuthSessions; logout A does not revoke B;
4. server-side AuthSession revocation → reload converges unauthenticated and clears cookie;
5. server-side AuthSession expiry → reload converges unauthenticated and clears cookie;
6. disposable PostgreSQL actually stopped → signin gets service-unavailable behavior and never fake-authenticates; database then restarts;
7. real `SigninAttemptLimiter` → 429/Retry-After and never fake-authenticates.

The E2E control utility is test support only. It does **not** add public `/test/*` FastAPI endpoints. It locates only the disposable `dante-fullstack-*` test container and manipulates synthetic test state/processes required for deterministic proof.

Critical Auth Playwright retries remain disabled.

---

## 8. M3 closure verdict

Closure formula used:

```text
implementation complete for M3 scope
+ technical/security/code review
+ static/unit/generated/build proof
+ real PostgreSQL proof
+ real HTTPS browser proof across Chromium/Firefox/WebKit
+ manual UAT
+ issues fixed and re-proved
+ user explicit acceptance
= M3 CLOSED
```

Verdicts:

```text
ENGINEERING GATE:      PASS
USER ACCEPTANCE GATE: ACCEPTED
M3 STATUS:             CLOSED
```

M3 closure does **not** mean:

```text
whole Access/Auth vertical closed
signup complete
email verification complete
recovery/reset complete
reauth complete
Google/Apple complete
passkeys complete
Native Mobile Access complete
whole-product production deployment complete
```

---

## 9. Known harness / repository lessons

### 9.1 Disposable PostgreSQL extension ownership

The certified local PostgreSQL image already creates the required extensions. A first harness version duplicated extension creation and hit `DuplicateObject` for PostGIS.

Permanent rule:

```text
reuse certified image initialization
+ use idempotent extension guard where harness must verify versions
+ verify PostGIS 3.6.4 / vector 0.8.6 / pg_trgm / unaccent / pg_stat_statements
```

Do not create a competing PostgreSQL initialization path.

### 9.2 Feature boundary

Routes consume Access only through `apps/web/src/features/access/index.ts`. Do not make route code deep-import `features/access/application/*` to reach bootstrap logic.

### 9.3 Formatter/tooling discipline

Generated code and lockfiles are not hand-edited. For pure Prettier/Ruff formatter drift, run the repository formatter rather than guessing its exact output.

### 9.4 Connector incident history

Some remote connector operations in this branch created no-op/transient commits/files while preparing changes. The final tree was cleaned each time and history was not force-rewritten because no rewrite gate was authorized.

Do not treat those transient commits as product architecture. Before merge, history may be squashed/reorganized only under an explicit user gate; never force-push merely for aesthetics.

---

## 10. Current vertical boundary after M3

### M4 — Signup + Verification + Recovery + Reset + Reauth

**Status:** `NEXT / NOT STARTED`

Goal: complete the first-party account lifecycle around the M3 session spine.

Expected scope, gated slice-by-slice:

```text
signup/account establishment
email verification proof lifecycle
neutral recovery initiation
recovery proof validation
password reset
post-reset session revocation policy
fresh signin after recovery
recent-auth / reauthentication
email delivery port + protocol-faithful deterministic test substitute
new persistence only where the closed M4 contract actually requires it
OpenAPI/generated-client/Web integration in the same slice
real PostgreSQL + browser race/replay proof
```

M4 must preserve anti-enumeration, one-time/replay safety and account-security serialization. Do not invent generic token/proof tables before the exact M4 proof semantics are closed.

### M5 — Google + Apple + Passkeys + Explicit Linking

**Status:** `NOT STARTED`

Official current provider mechanisms + WebAuthn/passkeys, preserving issuer+subject identity and explicit collision linking. Provider login never grants Gmail/Calendar/iCloud data access.

### M6 — Native Mobile Access

**Status:** `NOT STARTED`

Use existing Expo/React Native/Expo Router foundation with the same canonical Account/AuthSession semantics and native-appropriate secure credential transport/storage.

### M7 — Security Hardening + Authenticated Handoff + Vertical Closure

**Status:** `NOT STARTED`

Whole-vertical threat/rate/replay/concurrency/session-management/privacy/legal/accessibility/native/CI/database/client-drift proof and authenticated handoff to the next product vertical.

Only M7 completion + whole-vertical user acceptance may close Access/Auth as a complete product vertical.

---

## 11. Git/write safety

No new branch/worktree, merge, rebase, force-push or history rewrite without explicit user authorization.

Repository write discipline:

```text
fresh branch HEAD
→ exact scope
→ write only required files
→ readback diff/path audit
→ run applicable quality gates
→ user review/acceptance where required
```

`main` remains protected and is not modified by this workstream without a separate merge gate.

If Docker is required for a requested proof, state **Docker deve essere acceso** before asking the user to run it.

---

## 12. Immediate next safe action

Do **not** reopen M3 or start an unrelated branch.

Next action:

```text
M4 contract/slice selection
→ identify the smallest production-complete first-party lifecycle slice
→ close exact verification/recovery/reauth semantics
→ decide only the DB objects required by that slice
→ implement backend + OpenAPI + generated client + Web together
→ layered real PostgreSQL/browser proof
→ durable documentation
```

The M3 Account/AuthSession spine, generated-client boundary, Router-first session bootstrap and full-stack harness are now reusable foundations for M4–M7.
