# DANTE — Project Status

- **Status:** CURRENT TRUTH FOR `feature/access-auth`
- **Last reconciled:** 2026-08-29
- **Protected `main`:** integrated source authority; current Access/Auth branch work remains unmerged until an explicit merge gate
- **Active product vertical:** Access/Auth on `feature/access-auth`
- **Immediate decision:** PRE-M4 observability quick-feasibility check only; do not let it become a blocking infrastructure workstream
- **Next product macro-phase:** M4 — Signup + Verification + Recovery + Reset + Reauth
- **Last closed macro-phase:** M3 — Email/Password Signin + AuthSession Spine
- **Detailed forward plan:** `workstreams/access-auth-m4-m7-execution-plan.md`

## 1. Executive state

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL
CLOSED / SEMANTICALLY COMPLETE FOR CURRENT SCOPE

LOGICAL MODEL
CLOSED / 57 OF 57 CLASSIFIED
WL-H01..WL-H12 BINDING

PRE-PHYSICAL COHERENCE
CLOSED / FINAL QA PASS

PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED
PostgreSQL 18 major family canonical

ENGINEERING FOUNDATION v0
CLOSED / ACCEPTED

FRONTEND ENGINEERING FOUNDATION
CLOSED / ACCEPTED / INTEGRATED

FRONTEND MATERIALIZATION
CLOSED / ACCEPTED / INTEGRATED

BACKEND CP1–CP6
CLOSED / ACCEPTED / INTEGRATED

ACCESS PRE-BACKEND WEB MATERIALIZATION
CLOSED / ACCEPTED

ACCESS/AUTH M1
CLOSED — Visual / UX Freeze

ACCESS/AUTH M2
CLOSED — Auth Architecture Freeze

ACCESS/AUTH M3
CLOSED — Email/Password Signin + AuthSession Spine
ENGINEERING GATE PASS
USER ACCEPTANCE ACCEPTED

PRE-M4 OBSERVABILITY
CONDITIONAL QUICK GATE
DO NOW ONLY IF BOUNDED / NON-INVASIVE
OTHERWISE DEFER TO M7

ACCESS/AUTH M4
NEXT / NOT STARTED

ACCESS/AUTH M5
PLANNED

ACCESS/AUTH M6
PLANNED

ACCESS/AUTH M7
PLANNED / FINAL WHOLE-VERTICAL GATE
OBSERVABILITY MANDATORY HERE IF NOT CLOSED EARLIER

WHOLE ACCESS/AUTH VERTICAL
ACTIVE / NOT CLOSED
M4–M7 REMAIN
```

M3 closure means the first real authenticated production path is accepted. It does **not** mean signup/recovery/providers/passkeys/native/whole-vertical closure are complete.

PRE-M4 observability is **not** allowed to delay the product vertical merely to build infrastructure early. The next chat must first perform a bounded feasibility/readback. If the baseline is genuinely small and isolated, it may be completed before M4. If it expands into a real observability/infrastructure workstream, record the deferral and start M4; M7 then owns mandatory observability/release closure.

---

## 2. Protected-main baseline vs active branch truth

Protected `main` still carries the integrated CP6 database baseline until the Access/Auth branch is explicitly merged:

```text
protected main / CP6 baseline
PostgreSQL          18.6
Alembic             20260826_08
68 tables
5 views
14 routines
75 triggers
95 physical indexes
68 foreign keys
120 CHECK constraints
```

Current `feature/access-auth` database truth after M3:

```text
PostgreSQL          18.6
Alembic             20260827_10
72 tables
5 views
15 routines
75 triggers
104 physical indexes
71 foreign keys
137 CHECK constraints
92 standalone Dictionary entries
```

The branch adds:

```text
dante.account
dante.email_identity
dante.password_credential
dante.auth_session
dante.acquire_account_security_lock(uuid)
```

The branch-local current reference must describe these objects even though protected `main` has not yet integrated them.

---

## 3. Persistence authority

Permanent database authority chain:

```text
Domain / Logical / Physical
→ semantic and architectural source

PostgreSQL Persistence Constitution + ADR-010
→ durable persistence doctrine

Database current/evolving reference + Dictionary
→ current human + machine database meaning

Alembic
→ deployed schema evolution authority

SQLAlchemy mappings
→ application representation

real PostgreSQL catalog
→ observed materialization

direct tests
→ executable proof
```

Required same-change invariant:

```text
Dictionary
≈ SQLAlchemy
≈ Alembic
≈ current PostgreSQL
≈ human current reference
≈ tests
```

Historical CP6 acceptance evidence is not rewritten to pretend later Auth objects existed during CP6.

---

## 4. Binding semantic and Auth invariants

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
Subject != Resource != native identity
Possibility != Goal != Proposal != Decision != Plan != Activity
Routine != Recurrence != Occurrence
Occurrence != Schedule != Session != Actual
Actual != Observation != Outcome
Evidence != Provenance
Version != Reconciliation
Authority != Visibility
Agreement != Consent
Ownership != Possession
provider state != canonical DANTE state
provider authentication != provider-data integration authorization
derived projection != canonical truth
absence/unknown != false
MaterialStateRef != ETag/MVCC/provider revision
idempotency != semantic identity
client local state != canonical accepted effect
frontend request/success != backend-authoritative success
unknown/loading != signed-out/signed-in
```

Universal Entity/Thing, generic semantic edge tables, canonical EAV/property bags and JSONB required-semantic escape hatches remain forbidden shortcuts.

Do not reopen without an explicit bounded architecture gate:

```text
JWT/localStorage browser Auth
Redis/JWT session authority
Principal persistence
silent provider-email merge
Account advisory-lock replacement
Axios
generated React Query hooks as app boundary
wide credentialed CORS
fake frontend Auth success
persisted browser Auth cache
```

---

## 5. M3 closed implementation

### Backend

Real Auth operations:

```text
POST   /api/v1/auth/signin
GET    /api/v1/auth/session
DELETE /api/v1/auth/session
```

Implemented security/runtime spine:

```text
email normalization/comparison
Argon2id + separate HMAC pepper
HIBP range integration
bounded KDF admission/concurrency
unknown-account dummy verification
opaque PostgreSQL-backed AuthSession
runtime Principal
Secure HttpOnly host-only __Host-dante-session
session-bound CSRF
Origin + Fetch Metadata + X-Dante-Client Web protection
RFC9457 problem responses
ambiguous AuthSession commit reconciliation
current-session logout/revocation
Account-row security serialization through narrow DB function
```

### OpenAPI/client

```text
FastAPI/Pydantic
→ deterministic OpenAPI 3.1
→ Orval Fetch
→ generated TypeScript/Zod
→ governed framework-neutral @dante/api-client
```

No Axios, no generated React Query hooks, no hand-edited generated output and no persisted browser Auth cache.

### Web

Real Web integration:

```text
TanStack Router
→ Access feature public API
→ TanStack Query remote lifecycle
→ Web Auth remote adapter
→ @dante/api-client
→ same-origin /api/v1
```

The Access reducer never authenticates from request intent alone.

---

## 6. Permanent M3 bootstrap / refresh regression rule

M3 UAT found and fixed a real authenticated-refresh defect.

Rejected:

```text
initial reducer = SIGN_IN
→ paint login
→ async /auth/session
→ repair UI after paint
```

Also rejected:

```text
keep sign-in panel geometry
+ hide form during bootstrap
→ removes login flash
→ introduces perceptible refresh recomposition
```

Accepted:

```text
hard refresh
→ TanStack Router loader resolves authoritative session
→ Query cache ready
→ AccessPage mounts once
→ first business render is already signed-in or signed-out
```

Permanent rule:

```text
unknown/loading != signed-out
unknown/loading != signed-in
```

Critical first-screen remote state must not temporarily render a false business state merely because data has not arrived.

The brief browser-owned blank/repaint frame of a hard document reload was manually compared and accepted; it is not an Auth-state or layout regression.

Routes consume Access through its public API, never through deep feature imports.

---

## 7. M3 direct proof

### Backend/PostgreSQL

```text
fast non-PG tests                    73 / 73 PASS
real PostgreSQL 18.6 marked suite    83 / 83 PASS
real Auth integration                4 / 4 PASS
package build                        PASS
migration/catalog/ACL                PASS
Dictionary/SQLAlchemy/Alembic/PG     PASS
Account security lock                PASS
runtime recovery                     PASS
transaction behavior                 PASS
```

### Web

```text
TypeScript typecheck                 PASS
ESLint                               PASS
Vitest                               6 files / 25 tests PASS
architecture dependency cruise       PASS
Prettier                             PASS
production Vite build                PASS
generated:check                      PASS
```

### Full stack

```text
real HTTPS browser
→ production Vite build
→ same-origin proxy
→ real FastAPI
→ real PostgreSQL 18.6

21 / 21 PASS
7 scenarios × Chromium / Firefox / WebKit
```

Browser scenarios prove:

```text
real signin + cookie + logout
bootstrap/reload with no false login paint
wrong credentials
independent sessions
server-side revoke
server-side expiry
real PostgreSQL outage
real signin rate limiter / 429
```

Manual acceptance:

```text
login flash                  eliminated
refresh geometry             accepted
manual user UAT              ACCEPTED
```

M3 verdict:

```text
ENGINEERING GATE:      PASS
USER ACCEPTANCE GATE: ACCEPTED
M3:                    CLOSED
```

---

## 8. Current Access frontend truth

The pre-backend Access visual/state system remains the accepted surface, now with real M3 signin/session/logout integration.

Current production rules:

```text
frontend-owned transition may be local
backend-authoritative success must come from backend
transport stays behind application/remote boundary
route code consumes feature public API, not deep internals
Auth state is not stored in localStorage/sessionStorage
session bootstrap is route-coordinated
background refetch must not reset the screen to false signed-out/loading state
```

Signup/recovery/provider/passkey/setup surfaces requiring later backend behavior remain non-authoritative until their corresponding M4/M5/M7 slices materialize.

---

## 9. Current branch/worktree safety

Continue Access/Auth on:

```text
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not create another `feature/access-*` branch or worktree merely because the observability feasibility check or M4 begins. Do not merge/rebase/force-push/history-rewrite or write to protected `main` without explicit user authorization.

The separate `/home/mattia/projects/dante-frontend` worktree remains independent frontend territory and must not be accidentally used for Access/Auth commands.

---

## 10. Immediate decision — observability quick gate vs defer

Before M4 implementation, perform **only a bounded observability feasibility/readback**.

Do it before M4 only if the useful baseline can stay within all of these boundaries:

```text
no new product/domain persistence
no invasive refactor of M3 Auth
no new cross-service business architecture
no production deployment/on-call project
no CI/release redesign merely for observability
no large permanent infrastructure subsystem
telemetry failure remains non-fatal to Auth
application instrumentation remains vendor-neutral
```

A quick pre-M4 baseline may include, if genuinely contained:

```text
safe structured logs
request_id / trace correlation
minimal OpenTelemetry traces/metrics
small disposable local collector/backend stack
one representative Auth query/dashboard path
secret-redaction proof
```

If achieving that requires a real infrastructure workstream, **stop before implementation, document `DEFERRED TO M7`, and begin M4**. Do not build Grafana/Loki/Tempo/Prometheus/Mimir early just because they are good tools.

If deferred, M4–M6 still must preserve safe logging and must never emit Auth/proof/provider/passkey secrets. Full observability then becomes a mandatory M7 release/operational gate before whole-vertical closure.

---

## 11. Forward macro-roadmap

### M4 — Signup + Verification + Recovery + Reset + Reauth

**Status:** `NEXT / NOT STARTED`

Contract-first implementation of the first-party lifecycle. Must prove anti-enumeration, proof expiry/replay/concurrency, email delivery degradation, password-reset/session-revocation semantics and recent-auth behavior on real PostgreSQL and real browser boundaries.

### M5 — Google + Apple + Passkeys + Explicit Linking

Current official provider/WebAuthn flows, issuer+subject identity, explicit collision/linking, no provider-email silent merge, provider login distinct from provider-data integration authorization.

### M6 — Native Mobile Access

Existing Expo/React Native/Expo Router foundation, same canonical server-side Account/AuthSession authority, native-specific secure credential transport/storage, deep-link/provider/passkey handling and real native proof.

### M7 — Security Hardening + Authenticated Handoff + Vertical Closure

Whole-vertical threat review, session/account management as product-required, **mandatory observability/release baseline if not completed before M4**, security/privacy/accessibility regression, authenticated handoff into the next product vertical and complete manual user acceptance.

Exact subphases, anti-patterns and exit gates are authoritative in:

```text
docs/workstreams/access-auth-m4-m7-execution-plan.md
```

---

## 12. Current direct-validation non-claims

Do not claim:

```text
whole Access/Auth vertical closed                  NO
full observability baseline                        NOT YET CLOSED / CONDITIONAL PRE-M4 OR M7
M4 signup/verification/recovery/reset/reauth       NOT STARTED
Google / Apple production authentication           NOT STARTED
passkeys/WebAuthn                                  NOT STARTED
Native Mobile Access                               NOT IMPLEMENTED
whole-vertical legal/release closure               NOT COMPLETE
production deployment                              NOT STARTED
PowerSync product activation                       NOT RUN
Restate product activation                         NOT RUN
restore/PITR rehearsal                             NOT RUN
```

M3 closure is deliberately bounded to the first email/password + AuthSession spine.

---

## 13. Current navigation

Start with:

```text
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/access-auth.md
docs/workstreams/access-auth-m4-m7-execution-plan.md
```

Access/Auth architecture:

```text
docs/architecture/access-auth-architecture.md
docs/architecture/access-auth-security-contract.md
docs/architecture/access-auth-api-contract.md
docs/architecture/access-auth-testing-contract.md
docs/decisions/ADR-011-access-auth-architecture.md
```

Database:

```text
docs/database/README.md
docs/database/dante-postgresql-database.md
docs/database/access-auth.md
docs/database/dictionary/
```

Web:

```text
docs/frontend/access.md
apps/web/src/features/access/
apps/web/src/platform/auth/
apps/web/e2e/auth/access-auth.spec.ts
```

Historical branch narratives remain evidence only and do not override current implementation/reference truth.

### Known documentation cleanup note

`docs/database/dante-postgresql-database.md` is a very large evolving blueprint whose opening current-reconciliation block still contains an older M3-A/Alembic `20260827_09` wording. Current DB authority is `docs/database/README.md`, `docs/database/access-auth.md`, Dictionary, Alembic `20260827_10` and real tests. This wording drift does **not** reopen M3; reconcile it safely in a bounded documentation sweep before the next structural DB change rather than risking destructive whole-file replacement.
