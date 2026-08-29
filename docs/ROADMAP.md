# DANTE Roadmap

- **Status:** CURRENT FOR `feature/access-auth`
- **Last reconciled:** 2026-08-29
- **Protected `main`:** integrated source authority; current Access/Auth branch work is not yet merged
- **Active vertical:** Access/Auth
- **Immediate decision:** quick observability feasibility check; complete before M4 only if bounded, otherwise defer to M7
- **Next product macro-phase:** M4 — Signup + Verification + Recovery + Reset + Reauth
- **Detailed execution authority:** `workstreams/access-auth-m4-m7-execution-plan.md`

## 1. Completed foundations and forward sequence

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
Physical Model / PostgreSQL 18
        CLOSED
          ↓
Engineering + Frontend + Backend CP1–CP6
        CLOSED / ACCEPTED
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
Observability quick-feasibility decision
        DO NOW ONLY IF BOUNDED
        OTHERWISE DEFER TO M7
          ↓
Access/Auth M4 — Signup + Verification + Recovery + Reset + Reauth
        NEXT
          ↓
Access/Auth M5 — Google + Apple + Passkeys + Explicit Linking
        PLANNED
          ↓
Access/Auth M6 — Native Mobile Access
        PLANNED
          ↓
Access/Auth M7 — Security Hardening + Authenticated Handoff + Vertical Closure
        PLANNED / FINAL GATE
        FULL OBSERVABILITY MANDATORY HERE IF NOT CLOSED EARLIER
```

M3 is closed. The whole Access/Auth vertical is not.

The observability work is intentionally **conditional before M4**. DANTE must not lose momentum by turning a useful logging/metrics improvement into an early infrastructure programme. The next chat performs a bounded readback first; if the useful baseline is small and isolated, do it. If not, record the deferral and continue directly to M4.

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

Permanent same-change rule for structural DB evolution:

```text
Alembic
≈ SQLAlchemy
≈ Database Dictionary
≈ current human DB reference
≈ real PostgreSQL
≈ direct tests
```

Applied historical revisions remain immutable. Current references evolve with accepted later truth.

---

## 3. Closed Access/Auth foundations

### M1 — Access Visual / UX Freeze

**Status:** `CLOSED`

Accepted the existing Web Access composition. No redesign-from-zero. Backend-authoritative success may never be fabricated.

### M2 — Auth Architecture Freeze

**Status:** `CLOSED / M2.1–M2.11 ACCEPTED`

Frozen foundations include:

```text
same-origin browser topology
opaque server-side AuthSession
cookie / CSRF / Origin / Fetch Metadata posture
Account / EmailIdentity / PasswordCredential / Principal semantics
multiple sessions normal
Argon2id / HIBP / email normalization
/api/v1 + RFC9457
READ COMMITTED + targeted locking
Account security serialization point
OpenAPI → Orval Fetch → governed client
real PostgreSQL + real browser proof contract
```

### M3 — Email/Password Signin + AuthSession Spine

**Status:** `CLOSED / ENGINEERING GATE PASS / USER ACCEPTANCE ACCEPTED`

Implemented and accepted:

```text
Account / EmailIdentity / PasswordCredential / AuthSession persistence
email/password signin
server-authoritative session bootstrap
current-session logout
runtime Principal
FastAPI Auth API
RFC9457 problems
same-origin cookie / CSRF / Origin / Fetch Metadata enforcement
deterministic OpenAPI 3.1
Orval Fetch + Zod + @dante/api-client
Web Auth remote boundary
TanStack Query remote lifecycle
TanStack Router critical session bootstrap
real HTTPS full-stack harness
```

Evidence:

```text
backend fast tests                     73 / 73 PASS
real PostgreSQL marked suite           83 / 83 PASS
real Auth API integration              4 / 4 PASS
Web unit                               25 / 25 PASS
TypeScript / ESLint / architecture     PASS
generated drift / build / formatting   PASS
browser full-stack                     21 / 21 PASS
Chromium / Firefox / WebKit            7 / 7 each
manual UAT                             ACCEPTED
```

Permanent M3 regression rules:

```text
unknown/loading != signed-out/signed-in
critical session state resolves at Router boundary
no login-first + useEffect repair
no hidden sign-in geometry placeholder
route consumes Access public API only
no persisted browser Auth cache
no fake frontend Auth success
```

---

## 4. Observability decision before M4

**Status:** `CONDITIONAL QUICK GATE`

Do **not** automatically implement a complete Grafana/OTel stack before M4.

First determine whether a useful baseline fits within this bounded shape:

```text
safe structured logs
request_id / trace correlation
minimal OpenTelemetry traces/metrics
small disposable local collector/backend path
one representative Auth dashboard/query path
secret-redaction proof
```

It is suitable for PRE-M4 only if it does **not** require:

```text
new product/domain persistence
invasive Auth refactor
large permanent infrastructure subsystem
production deployment/on-call design
CI/release redesign
new cross-service business architecture
significant operational ownership before a deployment exists
```

Candidate technologies remain:

```text
OpenTelemetry instrumentation contract
Grafana
Grafana Alloy
Loki
Tempo
Prometheus or Mimir
```

The application boundary stays vendor-neutral. Never emit passwords, session/CSRF secrets, verification/recovery/reset proofs, OAuth codes/tokens, passkey private material, password hashes/pepper, full secret links or sensitive bodies.

### Decision rule

```text
bounded + isolated + directly useful
→ implement and close before M4

turns into real infrastructure workstream
→ document DEFERRED TO M7
→ begin M4 immediately
```

If deferred, M4–M6 still require safe logging/redaction discipline. Full correlation/metrics/traces/dashboard/release observability becomes an explicit M7 closure requirement.

---

## 5. M4 — Signup + Verification + Recovery + Reset + Reauth

**Status:** `NEXT / NOT STARTED`

Objective: complete the first-party Account lifecycle around the accepted M3 session spine.

### M4.1 Signup / Account establishment

Close before implementation:

```text
when Account and EmailIdentity are created
verified vs unverified semantics
password establishment
normalization/collision behavior
abandoned-signup policy if any
concurrent duplicate signup
whether unverified Accounts may sign in and with what authority
```

`Person != Account` remains binding.

### M4.2 Verification proof lifecycle

Define:

```text
entropy / encoding / stored verifier shape
purpose + Account/EmailIdentity binding
issued / expiry / consumed semantics
single use
reissue/supersession
concurrent double-consume
ambiguous commit
safe public result
```

No generic `auth_token(type,payload,status)` god-table by convenience.

### M4.3 Email delivery boundary

Provider-independent port/adapter + deterministic local substitute. No fake delivery success. Activate transactional outbox only if the real effect contract proves it necessary.

### M4.4 Recovery initiation

Known vs unknown Accounts must remain externally neutral enough to resist enumeration. Close rate/resource limits, proof issuance and email-dependency degradation.

### M4.5 Password reset

Reuse M3 password policy/KDF/HIBP + Account serialization. Close proof consumption, password replacement, session revocation and ambiguous-outcome semantics. No blind mutation retry.

### M4.6 Reauthentication / recent-auth

Represent server-side assurance freshness, not a client boolean. Define accepted method, freshness window, session binding, expiry, failure and rate-limit semantics. Keep the model compatible with M5 passkeys/providers.

### M4 implementation chain

```text
closed contract
→ exact persistence only if required
→ Alembic + SQLAlchemy + Dictionary + DB docs
→ FastAPI/Pydantic + RFC9457
→ deterministic OpenAPI
→ Orval Fetch + governed client
→ Web remote/application integration
→ authoritative Access transitions
→ real PostgreSQL race/replay proof
→ real HTTPS browser proof
→ docs + manual UAT
```

If the observability quick gate was deferred, do not make full Grafana/OTel infrastructure an M4 closure blocker. Still prove that logs/errors do not leak M4 secrets.

Minimum degraded/race matrix:

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
no secret leakage
no fake frontend success
```

M4 closes only through technical/security review, real DB/browser proof, current docs, manual UAT and explicit user acceptance.

---

## 6. M5 — Google + Apple + Passkeys + Explicit Linking

**Status:** `PLANNED / AFTER M4`

Before coding, re-read current official Google, Apple and WebAuthn/FIDO documentation.

Permanent identity rules:

```text
ExternalIdentity = issuer + subject
provider email != automatic Account link key
provider login != provider-data integration authorization
provider token != DANTE AuthSession
DANTE AuthSession remains canonical
```

Design explicit collision/linking state machine first:

```text
new subject / no collision
already-linked subject
same provider email but unlinked existing Account
signed-in user adds provider
subject linked to another Account
link confirmation / recent-auth
unlink without Account lockout
concurrent linking races
```

Google/Apple proof must cover state/nonce/PKCE where applicable, issuer/audience/subject, cancel/error/replay/outage/key rotation and linking collisions.

Passkey/WebAuthn gate must close RP ID/origin, credential ID/public key, user handle, UV/attestation posture, discoverable credentials, multiple passkeys, recent-auth for registration, revoke/lost-device behavior and passwordless Account support.

Passkey private keys never exist on DANTE servers.

M5 closes with current-spec review, security review, real collision/replay proof, platform/browser UAT, docs and explicit user acceptance.

---

## 7. M6 — Native Mobile Access

**Status:** `PLANNED / AFTER M5 UNLESS EXPLICITLY RE-GATED`

Use the existing Expo / React Native / Expo Router foundation and the same canonical backend Account/AuthSession authority.

Do not copy browser cookie/storage mechanics blindly. Close first:

```text
native session credential transport
SecureStore / Keychain / Keystore
CSRF applicability
app restart/background lifecycle
logout/revoke
multi-device behavior
verification/recovery/provider deep links
passkey platform APIs
uninstall/reinstall semantics
```

Native UX covers signin/signup/verification/recovery/reset/reauth/providers/passkeys/linking with platform-appropriate layout, focus, keyboard and accessibility.

Proof must include secure credential persistence, restart restoration, expiry/revoke convergence, deep-link tampering, provider callback integrity, network loss and multiple-device independence. Critical native semantics require emulator/device proof.

M6 closes with accepted native architecture/security contract, implementation, platform UAT, shared backend regression, docs and explicit user acceptance.

---

## 8. M7 — Security Hardening + Authenticated Handoff + Vertical Closure

**Status:** `PLANNED / FINAL ACCESS-AUTH GATE`

M7 proves the complete vertical and performs the real authenticated handoff to the next DANTE product surface.

Whole-vertical threat review covers at least:

```text
credential stuffing / spraying
enumeration
rate/resource exhaustion
session fixation/theft/replay
CSRF/origin/fetch-metadata bypass
verification/recovery/reset replay
email compromise implications
provider collision/link replay
WebAuthn challenge/origin/RP mistakes
concurrent security mutations
ambiguous commits
native credential/device-loss risk
telemetry secret leakage
```

Implement only product-required session/account management. Do not add ceremonial settings screens.

Authenticated handoff must close the real next route/shell, minimum Principal/session data, setup/first-run distinction, authorization boundary and degraded behavior. Coordinate with the separate Home/frontend worktree only through an explicit integration gate.

### Observability at M7

If not completed before M4, M7 must now close a production-credible observability baseline:

```text
privacy-safe structured logs
request_id ↔ trace correlation
OpenTelemetry traces/metrics or an explicitly superior current equivalent
collector/backend topology
low-cardinality service/Auth metrics
representative dashboards/queries
secret-redaction tests
telemetry-outage non-fatal behavior
operational documentation
```

Technology selection remains current-spec/evidence based; Grafana/Alloy/Loki/Tempo/Prometheus/Mimir are candidates, not mandatory brands.

M7 release gate additionally requires static/type/lint/architecture/generated/build, backend/PostgreSQL, migration/drift, cross-browser, Native where applicable, accessibility/responsive, privacy/legal, dependency/supply-chain and release configuration review.

Manual whole-vertical UAT exercises new Account, verification, signin, recovery/reset, reauth, providers/passkeys, multiple sessions/devices where applicable, logout/revoke, Native path where applicable and authenticated handoff.

Whole vertical closes only after explicit final user acceptance.

---

## 9. Reusable M3 foundations for M4–M7

Reuse rather than replace:

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

## 10. Persistent engineering rules

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
formatter handles pure formatter drift
generated code and lockfiles are not hand-edited
```

The accepted browser hard-refresh may have a brief document repaint; that is not a reason to reintroduce false Auth states or unstable placeholders.

---

## 11. Capability-triggered implementation

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

Observability follows the same principle: implement the useful bounded baseline early only if it stays cheap/isolated; otherwise close it when the release/operational boundary actually requires it.

---

## 12. Branch / worktree rule

Continue Access/Auth on:

```text
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not create a new branch merely because the quick observability decision or M4 begins. Do not use `/home/mattia/projects/dante-frontend` for this vertical. Do not merge/rebase/force-push/history-rewrite or write to protected `main` without an explicit user gate.

A new chat does not change these rules.

---

## 13. Immediate sequence

```text
1. M3 remains CLOSED
2. perform a bounded observability feasibility/readback only
3. if the useful baseline is genuinely small/isolated → implement + close it
4. if it expands into infrastructure work → record DEFERRED TO M7, no guilt/no scope creep
5. begin M4 contract-first
6. materialize only justified M4 persistence
7. backend → OpenAPI → generated client → Web per slice
8. prove race/replay/degradation on real PostgreSQL/browser boundaries
9. close M4 with manual user acceptance
10. repeat the same standard for M5
11. materialize Native in M6 under its own security gate
12. run M7 whole-vertical threat/release/observability-if-needed/handoff/UAT gate
13. merge to protected main only under a separate explicit user gate
```

Do not reopen M3 unless new direct evidence demonstrates a real defect or a later requirement cannot be met without an explicit bounded reopen.
