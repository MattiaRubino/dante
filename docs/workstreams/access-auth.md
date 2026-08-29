# DANTE — Access/Auth Full-Stack Vertical Workstream

- **Status:** ACTIVE VERTICAL / M1–M3 CLOSED / PRE-M4 NEXT
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Created from protected `main`:** `f011e252b6a294a12c38927ef2d528244ea1fee6`
- **M3 accepted implementation candidate before closure-doc reconciliation:** `d8a47f1cce271b1db30a53eff729f34501fe838a`
- **M3 closure docs checkpoint:** `68f38906e4282a267afa5fcc0d45a16bd7972d8b`
- **Current engineering gate:** `PRE-M4 — Operational Observability Baseline` — NEXT / NOT STARTED
- **Next product macro-phase:** `M4 — Signup + Verification + Recovery + Reset + Reauth`
- **Last closed macro-phase:** `M3 — Email/Password Signin + AuthSession Spine` — CLOSED / ENGINEERING PASS / USER ACCEPTED
- **Detailed forward execution plan:** `access-auth-m4-m7-execution-plan.md`
- **Purpose:** durable operational authority for branch safety, accepted architecture, M3 evidence/regression guards, current next action and whole-vertical handoff.

> A new chat is not a new project, branch or worktree. Continue this vertical on `feature/access-auth` and `/home/mattia/projects/dante` until the whole Access/Auth vertical is closed or the user explicitly re-gates repository topology.

---

## 1. Mandatory continuation bootstrap

Continue exactly:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

The separate `/home/mattia/projects/dante-frontend` worktree is independent frontend/Home territory. It is **not** the Access/Auth worktree.

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
4. this file;
5. `docs/workstreams/access-auth-m4-m7-execution-plan.md`;
6. `docs/development/agent-operating-manual.md`;
7. `docs/development/documentation-lifecycle-policy.md`;
8. `docs/frontend/access.md`;
9. `docs/architecture/access-auth-architecture.md`;
10. `docs/architecture/access-auth-security-contract.md`;
11. `docs/architecture/access-auth-api-contract.md`;
12. `docs/architecture/access-auth-testing-contract.md`;
13. `docs/decisions/ADR-011-access-auth-architecture.md`;
14. `docs/database/README.md`, `docs/database/access-auth.md` and the Dictionary when persistence is relevant.

Repository truth beats conversation memory.

---

## 2. Authority / lifecycle

Use the strictest applicable source:

```text
accepted Domain / Logical / Physical / ADR decisions
+ current implementation / migrations / tests
↓
current architecture / security / API / testing / DB / frontend docs
↓
this workstream + detailed forward execution plan
↓
historical branch records / frozen evidence
↓
conversation memory
```

Permanent database reconciliation invariant:

```text
current human DB reference
≈ Database Dictionary
≈ SQLAlchemy mappings
≈ Alembic head
≈ real PostgreSQL catalog
≈ direct tests
```

Historical evidence remains exact to its checkpoint. Current references follow accepted current truth.

---

## 3. Non-negotiable semantic/Auth constitution

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
unknown/loading != signed-out/signed-in
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
AuthSession belongs to Account, not one authenticator
multiple independent AuthSessions are normal
```

Do not reopen without bounded evidence/gate:

```text
JWT/localStorage browser Auth
Redis/JWT session authority
Principal table
silent provider-email merge
Account advisory locking
Axios
generated React Query hooks as app boundary
wide credentialed CORS
fake frontend Auth success
persisted browser Auth cache
```

---

## 4. Closed macro-phases

### M1 — Access Visual / UX Freeze

**Status:** `CLOSED / ACCEPTED`

The existing Web Access composition remains the production baseline. No redesign for novelty. Backend-authoritative success may never be fabricated.

### M2 — Auth Architecture Freeze

**Status:** `CLOSED / M2.1–M2.11 ACCEPTED / DOCUMENTED / QA PASS`

Durable authority:

```text
docs/architecture/access-auth-architecture.md
docs/architecture/access-auth-security-contract.md
docs/architecture/access-auth-api-contract.md
docs/architecture/access-auth-testing-contract.md
docs/decisions/ADR-011-access-auth-architecture.md
```

### M3 — Email/Password Signin + AuthSession Spine

**Status:** `CLOSED / ENGINEERING GATE PASS / USER ACCEPTANCE ACCEPTED`

M3 is the first real authenticated DANTE path. It is **not** whole Access/Auth closure.

---

## 5. M3 materialized implementation

### Database

Current branch database after M3:

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

`DB-U09 Account persistence` is resolved/materialized. `DB-U10 Principal persistence` is resolved without a Principal table.

`dante_runtime` cannot directly UPDATE Account or directly lock Account with `FOR UPDATE`; Account-wide security serialization uses the narrow migration-owned `SECURITY DEFINER` lock function.

### Backend runtime/API

```text
POST   /api/v1/auth/signin
GET    /api/v1/auth/session
DELETE /api/v1/auth/session
```

Implemented semantics:

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
RFC9457 application/problem+json with stable machine metadata
```

### OpenAPI/generated client

```text
FastAPI/Pydantic
→ deterministic committed OpenAPI 3.1
→ Orval Fetch
→ generated TypeScript + Zod
→ framework-neutral @dante/api-client
→ platform/application boundary
```

Forbidden:

```text
Axios
raw generated operations as app API
hand-edited generated output
remote DEV OpenAPI generation in CI
generated React Query hooks as the application boundary
browser Auth-cache persistence
```

### Web integration

```text
TanStack Router
→ Access feature public API
→ TanStack Query remote lifecycle
→ Web Auth remote
→ @dante/api-client
→ same-origin /api/v1
```

Mutation retry is disabled. Session GET uses only bounded accepted transient retry behavior. Auth state is not stored in localStorage/sessionStorage.

---

## 6. Permanent M3 bootstrap regression guard

### Defect found

Original Web integration initialized Access as `SIGN_IN`, then asynchronously resolved `/auth/session`. Authenticated hard refresh could paint login before the authoritative session arrived.

### Rejected mitigation

Keeping the real sign-in panel in layout and hiding its form removed the login flash but introduced visible refresh recomposition/bounce. This is rejected.

### Accepted professional pattern

```text
hard refresh
→ TanStack Router loader
→ resolve/prefetch authoritative /auth/session
→ Query cache ready
→ AccessPage mounts
→ first business render already SIGNED_IN or SIGNED_OUT
```

Route code consumes bootstrap options only through the Access feature public API.

Permanent rule:

```text
unknown/loading
!= signed-out
!= signed-in
!= error
```

Forbidden regressions:

```text
paint login then useEffect repair
unknown session == signed-out
hidden sign-in geometry placeholder
persisted client Auth cache
route deep-import of Access application internals
background refetch resetting resolved UI into false bootstrap state
```

Manual Firefox video review after Router-first fix:

```text
login flash                    eliminated
card/brand/topbar geometry     stable
brief browser document blank   accepted browser hard-reload repaint
user acceptance                ACCEPTED
```

Do not reopen M3 just to hide browser-owned document repaint.

---

## 7. M3 executable proof

### Backend / PostgreSQL

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

### Web

```text
TypeScript typecheck             PASS
ESLint                           PASS
Vitest                           6 files / 25 tests PASS
architecture dependency cruise   PASS
Prettier                         PASS
production Vite build            PASS
generated:check                  PASS
```

### Real browser/full stack

```text
Playwright
→ HTTPS Vite production preview
→ same-origin /api/v1 proxy
→ real FastAPI
→ real SQLAlchemy async runtime
→ disposable PostgreSQL 18.6
```

```text
7 scenarios × 3 engines = 21 / 21 PASS
Chromium  7 / 7
Firefox   7 / 7
WebKit    7 / 7
```

Scenarios:

1. real signin + cookie + delayed bootstrap regression + logout;
2. invalid credentials and safe feedback;
3. independent BrowserContexts/AuthSessions;
4. server-side revocation → unauthenticated convergence;
5. server-side expiry → unauthenticated convergence;
6. real disposable PostgreSQL outage → service unavailable / never fake-auth;
7. real signin limiter → 429 / never fake-auth.

Test control remains outside public FastAPI product APIs; no production `/test/*` surface.

M3 closure verdict:

```text
ENGINEERING GATE:      PASS
USER ACCEPTANCE GATE: ACCEPTED
M3 STATUS:             CLOSED
```

---

## 8. Repository lessons that must survive

### Certified PostgreSQL image

Reuse certified local image initialization. Do not create competing extension/bootstrap paths. Harness version guards may be idempotent but must not own a second schema truth.

### Feature boundary

Routes consume Access through `apps/web/src/features/access/index.ts`. Do not deep-import feature internals.

### Formatter discipline

Generated code/lockfiles are not hand-edited. Pure Prettier/Ruff drift is fixed using repository formatters.

### Git connector/history

This branch contains connector-created transient/no-op history from earlier remote operations. Final tree correctness is what matters. Do not force-rewrite/squash/rebase without an explicit user gate. Before eventual merge, ask whether the user wants history cleanup.

### Documentation drift

The huge `docs/database/dante-postgresql-database.md` opening reconciliation block still contains older M3-A/Alembic `20260827_09` wording. Current DB authority is `docs/database/README.md`, `docs/database/access-auth.md`, Dictionary, Alembic `20260827_10` and real tests. This wording drift does not reopen M3. Reconcile it safely before the next structural DB change rather than using a risky destructive whole-file replacement.

---

# 9. CURRENT NEXT GATE — PRE-M4 Operational Observability Baseline

**Status:** `NEXT / NOT STARTED`

Rationale: M4 introduces verification/recovery/reset/email side effects and M5 introduces providers/passkeys. DANTE should enter those phases with correlation, safe logs, metrics and traces rather than ad-hoc production debugging.

Required architecture posture:

```text
structured privacy-safe logs
+ request_id correlation
+ OpenTelemetry traces/metrics
+ trace/log correlation
+ low-cardinality metrics
+ collector/forwarder boundary
+ local Grafana-class exploration/dashboard path
```

Candidate stack to evaluate, not blindly preselect:

```text
OpenTelemetry
Grafana
Grafana Alloy
Loki
Tempo
Prometheus or Mimir
```

Do not couple application business logic to Grafana/Loki/Tempo APIs.

Never emit Auth secrets in telemetry:

```text
passwords
session/cookie values
CSRF secrets
verification/recovery/reset raw proof secrets
OAuth codes/tokens
passkey private material
hashes/pepper
secret-link full URLs
sensitive bodies by default
```

Telemetry outage must not change Auth correctness.

PRE-M4 direct closure must prove a real Auth request can be correlated across safe logs/request_id/trace, useful metrics exist, PostgreSQL outage is observable, telemetry backend outage is non-fatal, and redaction/leakage tests pass.

Exact PRE-M4 architecture/QA checklist is in `access-auth-m4-m7-execution-plan.md`.

---

# 10. Forward product macro-phases

## M4 — Signup + Verification + Recovery + Reset + Reauth

**Status:** `PLANNED / START AFTER PRE-M4`

Contract-first subphases:

```text
M4.1 Account establishment/signup semantics
M4.2 verification proof lifecycle
M4.3 email delivery port/adapter + deterministic local substitute
M4.4 anti-enumerating recovery initiation
M4.5 replay-safe password reset + explicit session revocation
M4.6 server-side recent-auth/reauth assurance
```

Do not start table-first. Close proof purpose/binding/entropy/storage/expiry/consumption/concurrency/ambiguous-outcome semantics first. No generic verification/recovery token god-table.

Each slice follows:

```text
closed contract
→ justified DB evolution
→ backend
→ OpenAPI
→ generated client
→ Web
→ observability
→ real PostgreSQL race/replay proof
→ real browser proof
→ docs/UAT
```

## M5 — Google + Apple + Passkeys + Explicit Linking

**Status:** `PLANNED / AFTER M4`

Before implementation re-read current official provider/WebAuthn documentation. Preserve:

```text
ExternalIdentity = issuer + subject
provider email never silently merges Accounts
provider login != provider-data integration authorization
provider token != DANTE AuthSession
DANTE AuthSession remains canonical
```

Design the collision/linking state machine before coding. Prove state/nonce/PKCE where applicable, issuer/audience/subject, replay/cancel/outage/key rotation, linking races and WebAuthn RP/origin/challenge/credential lifecycle.

## M6 — Native Mobile Access

**Status:** `PLANNED / AFTER M5 UNLESS EXPLICITLY RE-GATED`

Use existing Expo/React Native/Expo Router foundation and the same canonical backend Auth authority. Do not copy browser storage/cookie mechanics blindly.

Close native secure credential storage/transport, app lifecycle, revoke/logout, deep links, provider/passkey platform paths, reinstall behavior and device/emulator proof.

## M7 — Security Hardening + Authenticated Handoff + Whole-Vertical Closure

**Status:** `PLANNED / FINAL GATE`

Re-run whole-vertical threat analysis, abuse/rate/replay/session/linking/passkey/native/telemetry/privacy/dependency review; implement only product-required session/account management; integrate the real authenticated handoff into the next DANTE vertical under an explicit Home/frontend integration gate; run complete release/UAT regression.

Only M7 + explicit whole-vertical user acceptance may close Access/Auth.

Detailed subphases/proof matrices/exit criteria:

```text
docs/workstreams/access-auth-m4-m7-execution-plan.md
```

---

## 11. Git/write safety

No new branch/worktree, merge, rebase, force-push or history rewrite without explicit user authorization.

Repository write discipline:

```text
fresh branch HEAD
→ exact scope
→ write only required files
→ readback diff/path audit
→ applicable quality gates
→ user review/acceptance where required
```

`main` remains protected.

If Docker is required for a requested proof, state **Docker deve essere acceso** before asking the user to run it.

---

## 12. Immediate next safe action

Do **not** reopen M3 and do **not** start M4 implementation yet.

Next action:

```text
PRE-M4 observability architecture readback
→ choose minimum production-credible local stack
→ define safe structured log + OTel metric/trace semantics
→ implement collector/backends/dashboard path
→ instrument existing M3 Auth as first proof subject
→ prove redaction/correlation/DB-outage/telemetry-outage behavior
→ close PRE-M4 + docs
→ only then start M4 contract-first lifecycle design
```

The M3 Account/AuthSession spine, generated-client boundary, Router-first bootstrap and real full-stack harness are frozen reusable foundations for PRE-M4 and M4–M7.
