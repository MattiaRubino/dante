# DANTE — Access/Auth Full-Stack Vertical Workstream

- **Status:** ACTIVE VERTICAL / M1–M3 CLOSED / M4 NEXT
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Created from protected `main`:** `f011e252b6a294a12c38927ef2d528244ea1fee6`
- **M3 accepted implementation candidate before closure-doc reconciliation:** `d8a47f1cce271b1db30a53eff729f34501fe838a`
- **M3 closure docs checkpoint:** `68f38906e4282a267afa5fcc0d45a16bd7972d8b`
- **Immediate decision:** observability quick-feasibility check; do it pre-M4 only if bounded/non-invasive, otherwise defer to M7
- **Current product macro-phase:** `M4 — Signup + Verification + Recovery + Reset + Reauth` — NEXT / NOT STARTED
- **Last closed macro-phase:** `M3 — Email/Password Signin + AuthSession Spine` — CLOSED / ENGINEERING PASS / USER ACCEPTED
- **Detailed forward execution plan:** `access-auth-m4-m7-execution-plan.md`

> A new chat is not a new project, branch or worktree. Continue this vertical on `feature/access-auth` and `/home/mattia/projects/dante` until whole Access/Auth closure or an explicit user topology gate.

---

## 1. Mandatory continuation bootstrap

Continue exactly:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

The separate `/home/mattia/projects/dante-frontend` worktree is independent frontend/Home territory and is not the Access/Auth worktree.

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

1. `docs/PROJECT-STATUS.md`;
2. `docs/ROADMAP.md`;
3. this file;
4. `docs/workstreams/access-auth-m4-m7-execution-plan.md`;
5. `docs/architecture/access-auth-architecture.md`;
6. `docs/architecture/access-auth-security-contract.md`;
7. `docs/architecture/access-auth-api-contract.md`;
8. `docs/architecture/access-auth-testing-contract.md`;
9. `docs/decisions/ADR-011-access-auth-architecture.md`;
10. `docs/frontend/access.md`;
11. `docs/database/README.md`, `docs/database/access-auth.md` and the Dictionary when persistence is touched;
12. `docs/development/agent-operating-manual.md` and documentation lifecycle policy.

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
this workstream + detailed execution plan
↓
historical branch records
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

---

## 3. Non-negotiable semantic/Auth constitution

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

Existing Web Access composition remains the production baseline. No redesign for novelty. Backend-authoritative success may never be fabricated.

### M2 — Auth Architecture Freeze

**Status:** `CLOSED / M2.1–M2.11 ACCEPTED / DOCUMENTED / QA PASS`

Binding authority:

```text
docs/architecture/access-auth-architecture.md
docs/architecture/access-auth-security-contract.md
docs/architecture/access-auth-api-contract.md
docs/architecture/access-auth-testing-contract.md
docs/decisions/ADR-011-access-auth-architecture.md
```

### M3 — Email/Password Signin + AuthSession Spine

**Status:** `CLOSED / ENGINEERING GATE PASS / USER ACCEPTANCE ACCEPTED`

M3 is the first real authenticated DANTE path. It is not whole Access/Auth closure.

---

## 5. M3 materialized implementation

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

Production Auth API:

```text
POST   /api/v1/auth/signin
GET    /api/v1/auth/session
DELETE /api/v1/auth/session
```

Accepted runtime/security spine:

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
RFC9457 application/problem+json
```

OpenAPI/client path:

```text
FastAPI/Pydantic
→ deterministic committed OpenAPI 3.1
→ Orval Fetch
→ generated TypeScript + Zod
→ framework-neutral @dante/api-client
→ platform/application boundary
```

Web path:

```text
TanStack Router
→ Access feature public API
→ TanStack Query remote lifecycle
→ Web Auth remote
→ @dante/api-client
→ same-origin /api/v1
```

---

## 6. Permanent M3 bootstrap regression guard

Original defect:

```text
initial Access state = SIGN_IN
→ login paints
→ /auth/session resolves later
→ authenticated UI repairs after paint
```

Rejected mitigation:

```text
real sign-in panel kept in layout
+ form visibility:hidden
→ flash removed
→ refresh recomposition/bounce worsened
```

Accepted pattern:

```text
hard refresh
→ TanStack Router loader
→ resolve/prefetch authoritative /auth/session
→ Query cache ready
→ AccessPage mounts
→ first business render already SIGNED_IN or SIGNED_OUT
```

Forbidden regressions:

```text
paint login then useEffect repair
unknown session == signed-out
hidden sign-in geometry placeholder
persisted client Auth cache
route deep-import of Access internals
background refetch resetting resolved UI to false bootstrap state
```

Manual UAT after Router-first fix:

```text
login flash                    eliminated
card/brand/topbar geometry     stable
brief browser document blank   accepted hard-reload repaint
user acceptance                ACCEPTED
```

---

## 7. M3 executable proof

```text
fast non-PostgreSQL pytest                 73 / 73 PASS
real PostgreSQL 18.6 marked suite          83 / 83 PASS
real signin/session integration            4 / 4 PASS
TypeScript / ESLint / architecture         PASS
Vitest                                     25 / 25 PASS
Prettier / build / generated:check         PASS
real browser/full-stack                    21 / 21 PASS
Chromium / Firefox / WebKit                7 / 7 each
manual UAT                                 ACCEPTED
```

Browser matrix includes real signin/logout, invalid credentials, independent sessions, server-side revoke, server-side expiry, real PostgreSQL outage and real rate limiting. Test control does not add public production `/test/*` APIs.

M3 verdict:

```text
ENGINEERING GATE:      PASS
USER ACCEPTANCE GATE: ACCEPTED
M3 STATUS:             CLOSED
```

---

## 8. Repository lessons that must survive

```text
reuse certified PostgreSQL image initialization
routes consume Access only through feature public API
formatter handles pure Prettier/Ruff drift
generated code and lockfiles are not hand-edited
no unauthorized branch/history rewrite
real degraded/race/replay proof for security-sensitive paths
current docs move with accepted truth; historical evidence stays historical
```

The huge `docs/database/dante-postgresql-database.md` opening reconciliation block still carries older M3-A/Alembic `20260827_09` wording. Current DB authority is `docs/database/README.md`, `docs/database/access-auth.md`, Dictionary, Alembic `20260827_10` and real tests. This wording drift does not reopen M3. Reconcile safely before the next structural DB change.

---

## 9. Immediate observability decision — quick or defer

Observability is **not** a mandatory blocking PRE-M4 workstream.

Before M4, do only a bounded feasibility/readback and ask one question:

```text
Can we get a genuinely useful baseline without opening a real infrastructure project?
```

Suitable pre-M4 scope if contained:

```text
safe structured logs
request_id / trace correlation
minimal OpenTelemetry traces/metrics
small disposable local collector/backend path
one representative Auth dashboard/query path
secret-redaction proof
```

Pre-M4 is acceptable only if it does not require:

```text
new product/domain persistence
invasive Auth refactor
large permanent infrastructure subsystem
production deployment/on-call design
CI/release redesign
new cross-service business architecture
```

Candidate tools remain OpenTelemetry + Grafana/Alloy/Loki/Tempo/Prometheus-or-Mimir, but brands are not architecture requirements.

Decision:

```text
small / isolated / directly useful
→ implement now and close

scope expands materially
→ document DEFERRED TO M7
→ start M4
```

If deferred, M4–M6 still forbid secret leakage in logs and must preserve enough safe diagnostics for development. Full production-credible observability is then mandatory in M7 before whole-vertical closure.

---

## 10. Forward product macro-phases

### M4 — Signup + Verification + Recovery + Reset + Reauth

**Status:** `NEXT / NOT STARTED`

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
→ real PostgreSQL race/replay proof
→ real browser proof
→ docs/UAT
```

### M5 — Google + Apple + Passkeys + Explicit Linking

Before coding, re-read current official provider/WebAuthn documentation. Preserve issuer+subject identity, explicit linking, no provider-email silent merge, provider authentication distinct from provider-data integration authorization, and DANTE AuthSession as canonical session.

### M6 — Native Mobile Access

Use existing Expo/React Native/Expo Router foundation and the same backend Auth authority. Close native secure credential storage/transport, lifecycle, revoke/logout, deep links, provider/passkey platform paths, reinstall behavior and real emulator/device proof.

### M7 — Security Hardening + Authenticated Handoff + Whole-Vertical Closure

Re-run whole-vertical threat/abuse/replay/session/linking/passkey/native/privacy/dependency review; implement only product-required session/account management; perform real authenticated handoff; close release/UAT regression; **close observability here if it was deferred before M4**.

Only M7 + explicit whole-vertical user acceptance may close Access/Auth.

Detailed subphases and proof matrices:

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

If Docker is required for a requested proof, state **Docker deve essere acceso** first.

---

## 12. Immediate next safe action

Do **not** reopen M3.

Next action:

```text
1. quick observability feasibility/readback
2. if bounded → implement minimal useful baseline
3. if not bounded → mark observability DEFERRED TO M7
4. begin M4 contract-first lifecycle design immediately after that decision
```

The M3 Account/AuthSession spine, generated-client boundary, Router-first bootstrap and real full-stack harness remain frozen reusable foundations for M4–M7.
