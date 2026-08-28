# DANTE — Project Status

- **Status:** CURRENT TRUTH FOR `feature/access-auth`
- **Last reconciled:** 2026-08-28
- **Protected `main`:** integrated source authority; current Access/Auth branch work remains unmerged until an explicit merge gate
- **Active product vertical:** Access/Auth on `feature/access-auth`
- **Current macro-phase:** M4 next
- **Last closed macro-phase:** M3 — Email/Password Signin + AuthSession Spine

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

ACCESS/AUTH M4
NEXT / NOT STARTED

WHOLE ACCESS/AUTH VERTICAL
ACTIVE / NOT CLOSED
M4–M7 REMAIN
```

M3 closure means the first real authenticated production path is accepted. It does **not** mean signup/recovery/providers/passkeys/native/whole-vertical closure are complete.

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

## 4. Binding semantic invariants

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
```

Universal Entity/Thing, generic semantic edge tables, canonical EAV/property bags and JSONB required-semantic escape hatches remain forbidden shortcuts.

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

Real Web integration now exists through:

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

## 6. Session bootstrap / refresh rule

M3 UAT found and fixed a real authenticated-refresh defect.

Rejected behavior:

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

Accepted behavior:

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

### Manual acceptance

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

Signup/recovery/provider/passkey/setup surfaces that require later backend behavior remain non-authoritative until their corresponding M4/M5/M7 slices materialize.

---

## 9. Current branch/worktree safety

Continue Access/Auth on:

```text
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not create another `feature/access-*` branch or worktree merely because M4 begins. Do not merge/rebase/force-push/history-rewrite or write to protected `main` without explicit user authorization.

The separate `/home/mattia/projects/dante-frontend` worktree remains independent frontend territory and must not be accidentally used for Access/Auth commands.

---

## 10. Next product boundary — M4

M4 goal:

```text
Signup
+ Email Verification
+ Recovery
+ Password Reset
+ Reauthentication / Recent Auth
```

M4 must build on, not replace, the M3 spine.

Required direction:

```text
close exact proof/token lifecycle semantics first
→ materialize only justified persistence
→ backend/FastAPI
→ deterministic OpenAPI
→ generated client
→ Web integration
→ real PostgreSQL/race/replay proof
→ full-stack browser proof
→ durable docs
```

Important M4 constraints:

```text
neutral recovery initiation / anti-enumeration
single-use/replay-safe verification and recovery proofs
security-sensitive mutations serialized correctly
reset revocation policy explicit
fresh authentication behavior explicit
no speculative generic token god-table
no fake email delivery success
```

M5 providers/passkeys, M6 Native and M7 whole-vertical hardening/handoff remain later phases.

---

## 11. Current direct-validation non-claims

Do not claim:

```text
whole Access/Auth vertical closed                  NO
M4 signup/verification/recovery/reset/reauth       NOT STARTED
Google / Apple production authentication           NOT STARTED
passkeys/WebAuthn                                   NOT STARTED
Native Mobile Access                               NOT IMPLEMENTED
whole-vertical legal/release closure               NOT COMPLETE
production deployment                              NOT STARTED
PowerSync product activation                       NOT RUN
Restate product activation                         NOT RUN
restore/PITR rehearsal                             NOT RUN
```

M3 closure is deliberately bounded to the first email/password + AuthSession spine.

---

## 12. Current navigation

Start with:

```text
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/access-auth.md
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
