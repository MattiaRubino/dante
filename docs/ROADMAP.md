# DANTE Roadmap

- **Status:** CURRENT FOR `feature/access-auth`
- **Last reconciled:** 2026-08-29
- **Protected `main`:** integrated source authority; current Access/Auth branch work is not yet merged
- **Active vertical:** Access/Auth
- **Current gate:** PRE-M4 — Operational Observability Baseline
- **Next product macro-phase:** M4 — Signup + Verification + Recovery + Reset + Reauth
- **Detailed execution authority:** `workstreams/access-auth-m4-m7-execution-plan.md`

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
PRE-M4 — Operational Observability Baseline
        NEXT
          ↓
Access/Auth M4 — Signup + Verification + Recovery + Reset + Reauth
        PLANNED
          ↓
Access/Auth M5 — Google + Apple + Passkeys + Explicit Linking
        PLANNED
          ↓
Access/Auth M6 — Native Mobile Access
        PLANNED
          ↓
Access/Auth M7 — Security Hardening + Authenticated Handoff + Vertical Closure
        PLANNED / FINAL GATE
```

Architecture closure, a closed macro-phase and whole-product closure are different claims. M3 is closed; the complete Access/Auth vertical is not.

PRE-M4 is an engineering prerequisite inserted before M4 because M4/M5 add security-sensitive asynchronous/external flows whose diagnosis must not depend on ad-hoc logging.

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

M3 added Account/Auth persistence and the narrow Account-security lock capability without reopening CP6 doctrine.

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

M3 UAT permanently established:

```text
critical Auth unresolved
→ NEVER render signed-out as placeholder
→ route loader resolves /auth/session
→ Query cache ready
→ AccessPage mounts directly into authoritative state
```

Rejected regressions:

```text
login-first then useEffect repair
hidden sign-in form used as bootstrap geometry placeholder
route deep-import into Access application internals
persisted browser Auth cache
```

---

# 4. PRE-M4 — Operational Observability Baseline

**Status:** `NEXT / NOT STARTED`

## Purpose

Establish a production-credible, privacy-safe observability foundation before verification/recovery/email/provider/passkey complexity expands.

Mandatory semantic outcome:

```text
structured safe logs
+ request_id correlation
+ trace correlation
+ OpenTelemetry traces/metrics
+ low-cardinality operational/Auth metrics
+ collector/forwarder boundary
+ local query/dashboard path
+ redaction/leakage tests
```

Candidate ecosystem to evaluate:

```text
OpenTelemetry instrumentation contract
Grafana
Grafana Alloy
Loki
Tempo
Prometheus or Mimir
```

The application instrumentation boundary stays vendor-neutral. Grafana/Loki/Tempo APIs do not enter business/domain code.

## PRE-M4 decision points

Close explicitly:

```text
local stack topology
collector choice/config mode
logs ingestion path
metrics backend
trace backend
resource/service naming
request_id ↔ trace_id correlation
redaction/PII policy
retention for local/future production
cardinality budgets
telemetry failure behavior
future production deployment trigger
```

Do not overbuild an enterprise monitoring platform before a production environment exists. The baseline must be able to answer concrete debugging/health questions while remaining safe and cheap.

## PRE-M4 security rules

Never emit:

```text
passwords
session cookie/token values
CSRF secrets
verification/recovery/reset raw proof secrets
OAuth authorization codes/access/refresh tokens
passkey private material
password hashes/pepper
secret-link full URLs
sensitive request/response bodies by default
```

Raw email/account/session values must not become high-cardinality metric labels. Trace/log attributes are bounded and privacy-reviewed.

## PRE-M4 proof

At minimum:

```text
real Auth request correlated across request_id/log/trace
HTTP/Auth metrics visible
real signin success/failure observable safely
real PostgreSQL outage observable
collector/backend outage does not fail Auth correctness
secret/redaction tests PASS
local dashboard/query path usable
lint/type/format/build gates PASS
operational docs current
```

PRE-M4 closes through technical review + direct proof. It does not require production on-call/paging before a real production deployment exists.

Detailed contract: `docs/workstreams/access-auth-m4-m7-execution-plan.md`.

---

# 5. M4 — Signup + Verification + Recovery + Reset + Reauth

**Status:** `PLANNED / START AFTER PRE-M4`

## Objective

Complete the first-party Account lifecycle around the M3 session spine.

## Contract-first sequence

### M4.1 Signup / Account establishment

Close exact Account + EmailIdentity + PasswordCredential creation boundary, verification state, normalization/collisions, abandoned-signup behavior and concurrent duplicate signup semantics.

`Person != Account` remains binding; signup must not silently manufacture a Person unless a separately accepted product contract requires it.

### M4.2 Verification proof lifecycle

Define entropy, storage/verifier shape, purpose/subject binding, expiry, single-use consumption, supersession/reissue, concurrent consume, ambiguous commit and safe public responses before migration design.

No generic token god-table by convenience.

### M4.3 Email delivery boundary

Add provider-independent port/adapter + deterministic local substitute. No fake production delivery success. Transactional outbox activates only if the real effect contract proves it is required.

### M4.4 Recovery initiation

Known/unknown account requests must remain externally neutral enough to resist enumeration. Add bounded rate/resource controls and explicit email-dependency behavior.

### M4.5 Password reset

Reuse M3 password policy/KDF/HIBP and Account serialization. Close proof consumption, password replacement, session revocation and ambiguous-outcome semantics. No blind mutation retry.

### M4.6 Reauthentication / recent-auth

Represent real server-side assurance freshness, not a client boolean. Define accepted method(s), freshness duration, session binding and failure/rate-limit behavior. Password reauth may be the first implementation while the model remains compatible with M5 methods.

## M4 implementation chain

```text
closed lifecycle contract
→ exact DB objects only if required
→ Alembic + SQLAlchemy + Dictionary + DB docs
→ FastAPI/Pydantic + RFC9457
→ deterministic OpenAPI
→ Orval Fetch + governed client
→ Web remote/application integration
→ Access reducer/server-authoritative transitions
→ observability
→ real PostgreSQL race/replay proof
→ real HTTPS browser proof
```

## M4 minimum degraded/race matrix

```text
normalized duplicate signup
verification expired/replayed/concurrent-consume
verification email dependency unavailable
recovery known vs unknown externally neutral
recovery rate limit
reset expired/replayed/concurrent-consume
password policy/HIBP failure
post-reset session revocation
reauth success/failure/freshness expiry
PostgreSQL unavailable
no secret telemetry leakage
no fake frontend success
```

## M4 closure

Security/code review, static/generated/build gates, real PostgreSQL proof, critical Chromium/Firefox/WebKit proof, observability proof, manual UAT, current docs and explicit user acceptance.

---

# 6. M5 — Google + Apple + Passkeys + Explicit Linking

**Status:** `PLANNED / AFTER M4`

## Objective

Add external/passwordless authenticators without weakening Account identity.

Permanent rules:

```text
ExternalIdentity key = issuer + subject
provider email != automatic Account link key
provider login != Gmail/Calendar/iCloud authorization
provider token != DANTE AuthSession
DANTE AuthSession remains canonical server session
```

## M5.1 Current-spec gate

Re-read current official Google, Apple and WebAuthn/FIDO documentation before coding. These integrations are not implemented from stale memory.

## M5.2 Explicit linking/collision state machine

Prove behavior for:

```text
new subject/no collision
already-linked subject
same provider email but unlinked existing Account
signed-in user adds provider
subject linked to another Account
link confirmation/recent-auth
unlink without Account lockout
concurrent linking races
```

Silent provider-email merge remains forbidden.

## M5.3 Google / Apple

Validate state/nonce/PKCE where applicable, issuer/audience/subject, provider key rotation, cancel/error/replay/outage and linking collisions. Do not retain provider access/refresh tokens merely for authentication if not needed.

## M5.4 Passkeys/WebAuthn

Close RP ID/origin, credential identity/public-key storage, user handle, UV, attestation posture, discoverable credential posture, multiple passkeys, registration recent-auth and revoke/lost-device behavior.

Passkey private key never exists on DANTE servers.

## M5 proof

Provider/passkey success + error + cancellation + replay + collision + linking + passwordless Account + mixed-authenticator combinations + session issuance + telemetry redaction. Browser/platform support is proved honestly rather than mocked as universal compatibility.

## M5 closure

Current-spec review + security review + real integration/collision concurrency proof + platform/browser UAT + current docs + explicit user acceptance.

---

# 7. M6 — Native Mobile Access

**Status:** `PLANNED / AFTER M5 UNLESS EXPLICITLY RE-GATED`

## Objective

Materialize Access on the existing Expo/React Native/Expo Router foundation using the same canonical backend Account/AuthSession model with native-appropriate security.

## Native architecture gate

Do not copy browser cookie/storage mechanics blindly.

Close:

```text
native transport/session credential representation
SecureStore / Keychain / Keystore use
CSRF applicability
app restart/background lifecycle
logout/revocation
multi-device behavior
verification/recovery/provider deep links
passkey platform APIs
uninstall/reinstall semantics
```

If Native uses a different transport credential, it still maps to the same server-side AuthSession authority and revocation semantics.

## Native UX

Materialize signin/signup/verification/recovery/reset/reauth/providers/passkeys/linking with platform-appropriate layout, keyboard/focus/accessibility/offline/background behavior. Native is not scaled Web.

## Native proof

```text
no plaintext/AsyncStorage Auth secret
secure credential persistence
restart restoration
revoke/logout convergence
expired/revoked session
deep-link tampering
provider callback integrity
network loss/retry
multiple-device independence
native telemetry redaction
```

Critical native-only semantics require emulator/device proof. Browser proof is not sufficient.

## M6 closure

Accepted native architecture/security contract + implementation + platform tests/UAT + shared backend regression + docs + explicit user acceptance.

---

# 8. M7 — Security Hardening + Authenticated Handoff + Vertical Closure

**Status:** `PLANNED / FINAL ACCESS-AUTH GATE`

## Objective

Prove the complete Access/Auth system and hand an authenticated Principal/session into the next real DANTE product vertical.

M7 is not a dumping ground for known deficiencies from M4–M6. Earlier phases must close their own scope first.

## M7.1 Whole-vertical threat review

Re-test:

```text
credential stuffing / password spraying
enumeration
rate/resource exhaustion
session fixation/theft/replay
CSRF/origin/fetch-metadata bypass
verification/recovery/reset replay
email compromise implications
provider collision/link replay
WebAuthn challenge/origin/RP errors
Account recovery/lockout failure modes
concurrent security mutations
ambiguous commits
telemetry secret leakage
native device-loss/credential risks
```

Every finding is fixed, explicitly accepted with bounded rationale, or deferred with exact owner/trigger.

## M7.2 Session/account management

Implement only product-required management: session/device listing/revocation, credential/provider/passkey inventory and security-change invalidation as accepted by the product contract. No ceremonial settings screens.

## M7.3 Authenticated handoff

Close the real handoff contract into the next product route/shell, minimum Principal/session information, setup/first-run distinction, authorization boundary and degraded behavior.

Coordinate with the separate Home/frontend workstream only through an explicit integration gate. Do not silently merge/rebase that worktree.

## M7.4 Release/operational gate

At minimum:

```text
static/type/lint/architecture/generated/build PASS
full backend + PostgreSQL PASS
migration/drift proof PASS
cross-browser Auth regression PASS
Native regression PASS where supported
observability critical-path queries/dashboards usable
secret-leakage review PASS
rate/dependency/outage behavior PASS
accessibility/responsive PASS
privacy/legal destinations real/current where required
supply-chain/dependency review
CI/release posture truthful
backup/recovery requirements assessed against actual deployment stage
```

## M7.5 Manual whole-vertical UAT

User exercises the release-intended journey: new Account, verification, signin, recovery/reset, reauth, provider/passkey paths, multiple sessions/devices where applicable, logout/revoke, Native path where applicable and authenticated handoff.

## Whole-vertical closure formula

```text
M1 CLOSED
+ M2 CLOSED
+ M3 CLOSED
+ PRE-M4 CLOSED
+ M4 CLOSED
+ M5 CLOSED
+ M6 CLOSED
+ M7 PASS
+ user explicit whole-vertical acceptance
= ACCESS/AUTH VERTICAL CLOSED
```

---

## 9. M3 reusable foundations for later phases

PRE-M4 and M4–M7 must reuse rather than replace:

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

## 10. Persistent Web rules after M3

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

## 11. Observability rule after PRE-M4

Every later security-sensitive slice adds telemetry with the capability itself:

```text
stable safe event names
request/trace correlation
low-cardinality metrics
external dependency spans
bounded allowlisted attributes
redaction/leakage tests
```

Telemetry is operational evidence, not canonical DANTE product history.

---

## 12. Capability-triggered implementation

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

Observability is now the explicit exception in sequencing: a bounded baseline is intentionally activated before M4 because a real Auth runtime exists and the next phases introduce asynchronous/external security-critical flows.

---

## 13. Branch / worktree roadmap rule

Continue Access/Auth on:

```text
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not create a new branch merely because PRE-M4 or M4 begins. Do not use `/home/mattia/projects/dante-frontend` for this vertical. Do not merge/rebase/force-push/history-rewrite or write to protected `main` without an explicit user gate.

A new chat does not change any of these rules.

---

## 14. Immediate sequence

```text
1. M3 remains CLOSED; do not reopen it without direct defect evidence
2. execute PRE-M4 observability decision + local baseline on feature/access-auth
3. prove correlation/redaction/degraded telemetry behavior
4. close PRE-M4 and reconcile docs
5. start M4 contract-first, not table-first
6. materialize only M4 persistence justified by the closed lifecycle contract
7. implement backend → OpenAPI → generated client → Web as one vertical slice
8. prove race/replay/degradation on real PostgreSQL/browser boundaries
9. close M4 with manual user acceptance
10. repeat the same standard for M5
11. materialize Native in M6 under its own security gate
12. run whole-vertical M7 threat/release/handoff/UAT gate
13. merge to protected main only under a separate explicit user gate
```

Do not reopen M3 to redesign already accepted foundations unless new direct evidence demonstrates a real defect or a later requirement cannot be met without an explicit bounded reopen.
