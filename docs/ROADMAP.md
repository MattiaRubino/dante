# DANTE Roadmap

- **Status:** CURRENT FOR `feature/access-auth`
- **Last reconciled:** 2026-08-28
- **Protected `main`:** integrated source authority; current Access/Auth branch work is not yet merged
- **Active vertical:** Access/Auth
- **Current phase:** M4 next

## 1. Completed foundations

```text
Product / North Star
        CURRENT
          ↓
Domain Model
        CLOSED
          ↓
Logical Model
        CLOSED / 57 OF 57 / WL-H01..WL-H12
          ↓
Pre-Physical Coherence
        CLOSED / FINAL QA PASS
          ↓
Physical Model / Target Selection
        CLOSED / PostgreSQL 18 major family
          ↓
Engineering Foundation v0
        CLOSED / ACCEPTED
          ↓
Frontend Engineering Foundation
        CLOSED / ACCEPTED
          ↓
Frontend Production Materialization
        CLOSED / ACCEPTED
          ↓
Backend CP1–CP6
        CLOSED / ACCEPTED / INTEGRATED
          ↓
Access Pre-Backend Web Materialization
        CLOSED / ACCEPTED
          ↓
Access/Auth M1 — Visual / UX Freeze
        CLOSED
          ↓
Access/Auth M2 — Auth Architecture Freeze
        CLOSED
          ↓
Access/Auth M3 — Email/Password Signin + AuthSession Spine
        CLOSED / ENGINEERING PASS / USER ACCEPTED
          ↓
Access/Auth M4 — Signup + Verification + Recovery + Reset + Reauth
        NEXT
```

Architecture closure, a closed macro-phase and whole-product closure are different claims. M3 is closed; the complete Access/Auth vertical is not.

---

## 2. PostgreSQL baseline and branch evolution

Protected-main CP6 historical baseline:

```text
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

Current Access/Auth branch after M3:

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

M3 added Account/Auth persistence and the narrow account-security lock capability without reopening CP6 doctrine.

Permanent same-change rule:

```text
structural DB change
→ Alembic forward migration
→ SQLAlchemy mapping/metadata
→ Database Dictionary
→ current/evolving human DB reference
→ tests
→ real PostgreSQL proof
```

Applied historical revisions remain immutable. Current references evolve with accepted later truth.

---

## 3. Access/Auth definitive macro-roadmap

### M1 — Access Visual / UX Freeze

**Status:** `CLOSED`

Accepted the existing Web Access design/state baseline. No redesign-from-zero. Backend-authoritative success remains impossible to fake.

### M2 — Auth Architecture Freeze

**Status:** `CLOSED / M2.1–M2.11 ACCEPTED`

Closed:

```text
same-origin browser topology
opaque server-side AuthSession
cookie / CSRF / Origin / Fetch Metadata posture
Account / EmailIdentity / PasswordCredential / Principal semantics
multi-session behavior
password/KDF/breach policy
passkey-ready architecture
email normalization/comparison
/api/v1 + RFC9457 machine errors
transaction/concurrency/ambiguous outcome policy
OpenAPI → Orval Fetch → governed client path
real PostgreSQL + browser proof contract
```

### M3 — Email/Password Signin + AuthSession Spine

**Status:** `CLOSED / ENGINEERING GATE PASS / USER ACCEPTANCE ACCEPTED`

Implemented:

```text
Account / EmailIdentity / PasswordCredential / AuthSession persistence
Account security serialization capability
email/password signin
server-authoritative session bootstrap
current-session logout
runtime Principal
FastAPI Auth API
RFC9457 problems
cookie / CSRF / Origin / Fetch Metadata enforcement
OpenAPI 3.1 snapshot
Orval Fetch + generated Zod
framework-neutral @dante/api-client
Web Auth remote boundary
TanStack Query remote lifecycle
TanStack Router critical session bootstrap
real Access signin/session/logout wiring
real HTTPS full-stack harness
```

Accepted proof:

```text
backend fast tests                     73 / 73 PASS
real PostgreSQL marked suite           83 / 83 PASS
real Auth API integration              4 / 4 PASS
Web unit                               25 / 25 PASS
TypeScript / ESLint / architecture     PASS
generated drift / build / formatting   PASS
browser full-stack                     21 / 21 PASS
Chromium                               7 / 7 PASS
Firefox                                7 / 7 PASS
WebKit                                 7 / 7 PASS
manual UAT                             ACCEPTED
```

The 21 browser cases cover real signin/logout, bootstrap, invalid credentials, independent sessions, server-side revoke, server-side expiry, real PostgreSQL outage and real rate limiting.

M3 UAT also established the permanent session-bootstrap rule:

```text
critical auth state unresolved
→ do not render signed-out as a placeholder
→ route loader resolves /auth/session
→ Query cache is ready
→ AccessPage mounts directly into the authoritative state
```

A hidden sign-in panel used as a layout placeholder is explicitly rejected because it produced visible recomposition.

### M4 — Signup + Verification + Recovery + Reset + Reauth

**Status:** `NEXT / NOT STARTED`

Build the first-party lifecycle around M3:

```text
account establishment
email verification
neutral recovery initiation
single-use/replay-safe recovery proof
password reset
session revocation after reset
fresh authentication behavior
recent-auth / reauthentication
email delivery abstraction + deterministic test substitute
```

M4 must close exact proof lifecycle semantics before introducing new persistence. No generic verification/recovery token god-table by convenience.

### M5 — Google + Apple + Passkeys + Explicit Linking

**Status:** `NOT STARTED`

Implement official current provider flows and WebAuthn/passkeys while preserving:

```text
issuer + subject provider identity
explicit Account collision/linking
provider authentication != Gmail/Calendar/iCloud authorization
passwordless Account support
canonical DANTE Account/AuthSession authority
```

MFA remains deferred unless separately promoted.

### M6 — Native Mobile Access

**Status:** `NOT STARTED`

Materialize Access on the existing Expo/React Native/Expo Router foundation using the same canonical Auth backend and native-appropriate secure credential transport/storage.

### M7 — Security Hardening + Authenticated Handoff + Vertical Closure

**Status:** `NOT STARTED`

Whole-vertical proof:

```text
threat/security review
rate/resource abuse
replay/race/concurrency
session management
provider/passkey collisions
privacy/legal destinations
accessibility/responsive/native proof
client/schema drift
CI/release posture
authenticated handoff into the next product vertical
manual user acceptance
```

Only then may the **whole Access/Auth vertical** be declared closed.

---

## 4. M3 reusable foundations for later phases

M4–M7 must reuse rather than replace:

```text
Account security root
AuthSession semantics
runtime Principal
same-origin Web security posture
RFC9457 machine error contract
deterministic OpenAPI/client generation
Web remote/application boundary
TanStack Query remote lifecycle
Router-first critical session bootstrap
real PostgreSQL acceptance harness
real HTTPS Chromium/Firefox/WebKit Auth harness
```

Do not build parallel Auth/session stacks for signup, providers, passkeys or Native.

---

## 5. Persistent Web rules after M3

```text
backend + PostgreSQL own canonical accepted effect
REQUEST_* != SERVER_* authoritative result
unknown/loading != signed-out/empty
route code imports feature public API, not deep internals
TanStack Query owns remote lifecycle, not canonical Auth truth
no persisted browser Auth cache
mutation retry disabled unless a future exact operation proves it safe
background refetch must not destroy resolved UI
production code never imports prototypes
```

The accepted browser hard-refresh may have a brief document repaint; that is not a reason to reintroduce false Auth states or unstable placeholders.

---

## 6. Capability-triggered implementation

Specialist components activate only when a real consumer exists:

```text
PowerSync + encrypted SQLite
→ real offline/multi-device implementation

PostgreSQL transactional outbox
→ concrete Class-A async requirement

R2
→ real ContentArtifact byte flow

OR-Tools
→ solver-backed capability

Restate
→ first concrete Class-B durable workflow

PgBouncer
→ measured connection-management need

pgBackRest + AWS S3
→ recovery/production boundary or rehearsal
```

Selected architecture is not equivalent to activated runtime.

---

## 7. Branch / worktree roadmap rule

Continue Access/Auth on:

```text
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not create a new branch merely because M4 begins. Do not use `/home/mattia/projects/dante-frontend` for this vertical. Do not merge/rebase/force-push/history-rewrite or write to protected `main` without an explicit user gate.

A new chat does not change any of these rules.

---

## 8. Immediate sequence

```text
1. accept M3 closure documentation/readback
2. keep feature/access-auth active
3. begin M4 by closing the exact signup/verification/recovery/reset/reauth contract
4. materialize only M4 persistence justified by that contract
5. implement backend → OpenAPI → generated client → Web as one vertical slice
6. prove race/replay/security behavior on real PostgreSQL
7. prove critical Web behavior in the real HTTPS browser harness
8. reconcile durable docs at each closure
9. proceed to M5, M6, M7 on the same vertical unless explicitly re-gated
10. merge to protected main only under a separate user gate
```

Do not reopen M3 to redesign already accepted foundations unless new direct evidence demonstrates a real defect or an M4+ requirement cannot be met without an explicit bounded reopen.
