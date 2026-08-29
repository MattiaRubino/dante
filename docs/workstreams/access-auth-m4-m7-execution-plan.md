# DANTE — Access/Auth PRE-M4 + M4–M7 Execution Plan

- **Status:** CURRENT EXECUTION PLAN / PRE-M4 NEXT / M4–M7 PLANNED
- **Vertical:** Access/Auth
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **Prerequisite:** M1–M3 CLOSED; M3 engineering gate PASS; user acceptance ACCEPTED
- **Purpose:** remove ambiguity for future chats/engineers, preserve lessons from M3, and define the highest-quality safe sequence from the accepted AuthSession spine to whole-vertical closure.

> This plan refines the macro-roadmap. It does not reopen M1–M3 and does not authorize a new branch/worktree. Repository truth and the accepted Access/Auth architecture/security/API/testing contracts remain binding.

---

## 1. Mandatory continuation rules

Continue exactly:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Before writing:

```bash
pwd
git status --short --branch
git rev-parse HEAD
git rev-parse origin/feature/access-auth
git rev-parse origin/main
git worktree list --porcelain
```

Read, in this order:

1. `docs/PROJECT-STATUS.md`;
2. `docs/ROADMAP.md`;
3. `docs/workstreams/access-auth.md`;
4. this file;
5. `docs/architecture/access-auth-architecture.md`;
6. `docs/architecture/access-auth-security-contract.md`;
7. `docs/architecture/access-auth-api-contract.md`;
8. `docs/architecture/access-auth-testing-contract.md`;
9. `docs/decisions/ADR-011-access-auth-architecture.md`;
10. `docs/frontend/access.md`;
11. `docs/database/README.md` + `docs/database/access-auth.md` when persistence is touched;
12. `docs/development/agent-operating-manual.md` and documentation lifecycle policy.

Never infer that a new chat means a new phase topology. Never create a new `feature/access-*` branch/worktree without explicit user authorization.

---

## 2. M3 frozen foundations — reuse, do not replace

M4–M7 build on these accepted foundations:

```text
Account = durable access/security root
EmailIdentity separate from Account
PasswordCredential optional
Principal runtime-derived
opaque PostgreSQL-backed AuthSession
multiple independent AuthSessions normal
same-origin Web Auth topology
__Host-dante-session Secure/HttpOnly/Path=/SameSite=Lax
session-bound CSRF
Origin + Fetch Metadata + X-Dante-Client Web ingress
/api/v1 + RFC9457 problem contract
Account security serialization point
READ COMMITTED + targeted locking
no blind mutation retry
ambiguous-commit reconciliation where explicitly designed
FastAPI/Pydantic → deterministic OpenAPI → Orval Fetch → governed @dante/api-client
TanStack Query remote lifecycle
TanStack Router critical-session bootstrap
real PostgreSQL proof
real HTTPS Chromium + Firefox + WebKit proof
```

Do not reopen without direct evidence and an explicit bounded architecture decision:

```text
JWT/localStorage browser Auth
Redis/JWT as session authority
Principal persistence table
silent provider-email account merge
Account advisory-lock replacement
Axios
Orval-generated React Query hooks as app boundary
wide credentialed CORS
frontend fake Auth success
persisted browser Auth cache
hidden sign-in form as bootstrap placeholder
route deep-import of Access application internals
```

---

## 3. Permanent M3 lessons / regression-prevention rules

These are not optional style preferences. They were learned through direct implementation/UAT and must survive later phases.

### 3.1 Unknown remote truth is not a business state

```text
unknown/loading
!= signed-out
!= signed-in
!= empty
!= error
```

If first-screen correctness depends on remote state, coordinate that state at the route/bootstrap boundary. Do not paint a false business state and repair it after an effect.

### 3.2 Router-first Auth bootstrap remains canonical

```text
hard load
→ route loader resolves/prefetches /auth/session
→ Query cache ready
→ AccessPage mounts
→ first business render is authoritative
```

Do not reintroduce:

```text
initial SIGN_IN reducer default during unknown session
login flash then effect repair
visibility:hidden sign-in geometry placeholder
persisted client Auth cache
```

A browser-owned hard-reload blank frame is not solved by displaying false Auth state.

### 3.3 Feature boundaries are real architecture

Routes consume Access only through its public API. Presentation/model code must not reach generated transport internals. Platform Web code owns browser transport policy. Generated code is never hand-edited.

### 3.4 Real degraded-path proof is mandatory

M3 proved that happy-path-only browser tests are insufficient. Later phases must include deterministic degraded/race/replay cases using real product boundaries where practical, without public `/test/*` production APIs.

### 3.5 Formatter/tooling discipline

For pure Prettier/Ruff drift, use the repository formatter. Do not guess formatting manually. Do not hand-edit lockfiles/generated artifacts.

### 3.6 Documentation discipline

A closed capability is not complete until current docs, code, generated contracts, DB Dictionary where applicable, and executable evidence agree. Historical evidence remains historical; current references evolve.

---

# PRE-M4 — Operational Observability Baseline

## 4. Why this gate exists before M4

M3 now gives DANTE a real security-sensitive runtime. M4 adds verification/recovery/reset/reauth and email side effects; M5 adds external identity providers/passkeys. Entering those phases without a governed observability baseline would make race/replay/provider/email failures unnecessarily hard to diagnose and could encourage unsafe ad-hoc logging of secrets.

PRE-M4 therefore establishes observability **before** lifecycle complexity expands.

**Status:** `NEXT / NOT STARTED`

This is a bounded engineering gate, not a new product vertical and not a reason to create a new branch.

## 5. PRE-M4 architecture target

Application observability contract must remain vendor-neutral at instrumentation boundaries:

```text
application
→ structured safe logs
→ OpenTelemetry traces + metrics
→ stable correlation/resource attributes
→ collector/forwarder boundary
→ selected local/production backend(s)
→ Grafana-class query/dashboard/alert surface
```

Preferred candidate stack for evaluation:

```text
Grafana            visualization / exploration / dashboards
Grafana Alloy      stable collector/forwarder candidate
Loki               logs
Tempo              traces
Prometheus or Mimir metrics
OpenTelemetry      application instrumentation contract
```

Selection is not final merely because these names appear here. PRE-M4 must explicitly close local-development and future-production topology, retention, resource cost and operational ownership.

Do not couple application business code directly to Loki/Tempo/Grafana APIs.

## 6. PRE-M4 signal contract

### Logs

Required:

```text
structured machine-readable application logs
UTC timestamp
level
service/component
environment
request_id
trace_id/span_id when available
stable event name/category
safe machine error code where relevant
bounded context fields
```

Forbidden in logs/telemetry:

```text
passwords
session tokens/cookie values
CSRF secrets
verification/recovery/reset proof secrets
passkey private material
OAuth authorization codes/tokens
email message secret links
password hashes/pepper
full sensitive request/response bodies
unbounded provider payloads
```

Email/identity values require a deliberate privacy policy; do not scatter raw addresses through logs by convenience. Prefer stable opaque/hashed correlation only where genuinely needed and privacy-reviewed.

### Metrics

At minimum define low-cardinality service and Auth metrics for:

```text
HTTP request rate / duration / status class
readiness/liveness state where useful
DB pool/connection pressure where measurable
Auth signin outcomes by safe category
rate-limit events
session bootstrap success/error category
verification/recovery/reset outcome category once M4 exists
external dependency latency/failure once dependencies exist
```

Never use raw email, account UUID, session UUID, request ID or arbitrary error strings as metric labels.

### Traces

At minimum:

```text
HTTP server spans
DB spans at a safe abstraction level
external dependency spans (HIBP, later email/provider)
request_id ↔ trace correlation
error/status recording without secret payloads
```

Trace instrumentation must not change transaction ownership, retry behavior or product semantics.

## 7. PRE-M4 implementation posture

Current 2026 direction:

- OpenTelemetry traces/metrics are acceptable instrumentation foundations;
- structured application logging remains independently governed rather than requiring the Python OpenTelemetry Logs SDK;
- if Grafana Alloy is selected, use its stable/default supported pipeline unless a later explicit gate accepts an experimental engine;
- local observability must be reproducible and disposable, preferably through repository-governed container configuration;
- production topology may remain trigger-bound if no production environment exists yet, but the instrumentation/semantic contract must already be production-credible.

Do not create a giant monitoring platform merely to look enterprise. Start with the smallest complete path that can answer:

```text
what request failed?
where did it fail?
how long did it take?
was PostgreSQL/external dependency involved?
what safe machine error category occurred?
can we correlate logs ↔ trace ↔ request_id?
are error/latency/rate-limit rates changing?
```

## 8. PRE-M4 security/privacy gate

Before declaring PRE-M4 closed, prove:

```text
no Auth secret leakage in logs
no sensitive body capture by default
no high-cardinality user/session labels in metrics
trace attributes are allowlisted/bounded
telemetry endpoints are not publicly writable by default
local dashboard/collector ports have explicit development-only exposure
production credentials are environment/secret supplied, never committed
telemetry failure cannot break core Auth correctness
```

## 9. PRE-M4 proof / closure gate

Expected evidence:

```text
unit/static tests for log redaction/context helpers
real backend request produces correlated request_id + trace
metrics endpoint/collector path proven
real signin success and failure visible without secret leakage
real PostgreSQL outage observable and still semantically correct
collector/backend outage does not fail Auth requests
local dashboard can traverse representative logs/trace/metrics
format/lint/type/build gates green
operational docs current
```

PRE-M4 closes only after technical review + direct local proof. It is not necessary to build alert paging/on-call infrastructure before a production deployment exists; alert rules can be staged to the first real deployment boundary while metric semantics are fixed now.

---

# M4 — Signup + Verification + Recovery + Reset + Reauth

## 10. M4 goal

Complete the **first-party account lifecycle** around the accepted M3 signin/AuthSession spine without creating parallel security roots.

**Status:** `PLANNED / START ONLY AFTER PRE-M4`

## 11. M4 contract-first subphases

Do not begin with tables or screens. Close semantics in this order.

### M4.1 Account establishment / signup contract

Decide and document exactly:

```text
when Account is created
when EmailIdentity is created
verified vs unverified state semantics
password establishment path
normalization/collision behavior
whether an unverified Account can sign in and with what capability
expiry/cleanup policy for abandoned signup if any
concurrent duplicate signup behavior
```

Do not create Person automatically unless the accepted product contract explicitly requires that semantic transition. `Person != Account` remains binding.

### M4.2 Verification proof lifecycle

Close:

```text
proof secret entropy/encoding/storage representation
server stores verifier/digest, not reusable raw secret where avoidable
purpose binding
Account/EmailIdentity binding
issued/expires/consumed semantics
single-use behavior
new-proof invalidation/supersession policy
concurrent consume behavior
ambiguous commit behavior
safe public response
```

Verification success is backend-authoritative. Clicking a link does not grant frontend authority by itself.

### M4.3 Email delivery boundary

Introduce an application port/adaptor boundary, not provider calls in domain/application code.

Need:

```text
message purpose/template identity
recipient contract
secret-link construction at safe boundary
provider message identifier where useful
send attempt/result semantics
local deterministic protocol-faithful substitute
no production secret/token in committed config
```

Do not fake successful delivery in production code. Decide whether delivery requires transactional outbox only when a real Class-A async/effect contract proves it; do not activate outbox ceremonially.

### M4.4 Recovery initiation

Public initiation must be neutral enough to avoid account enumeration.

Close:

```text
known vs unknown email external equivalence
rate/resource limits
proof issuance/replacement semantics
email delivery failure semantics
request id / observability behavior
no disclosure that an Account exists
```

### M4.5 Password reset

Close exact mutation semantics:

```text
proof validation
password policy + HIBP + KDF reuse from M3
Account security serialization
consume proof + replace PasswordCredential atomically where possible
session revocation policy
current request/session behavior
ambiguous commit reconciliation
notification/audit requirements
```

No blind retry of password-reset mutation.

### M4.6 Reauthentication / recent-auth

Define a real assurance/freshness contract, not a boolean UI flag.

Close:

```text
which future operations require recent Auth
what counts as acceptable reauth method
freshness duration
how recent-auth fact is represented server-side
session binding
failure/lock/rate-limit behavior
step-up vs normal signin distinction
```

M4 may implement password reauth first while keeping the model ready for passkey/provider reauth in M5.

## 12. M4 persistence discipline

Before migration, derive exact objects from the closed proof lifecycle. Avoid a generic `auth_token(type,payload,status)` god-table.

Every structural DB change must update together:

```text
Alembic
SQLAlchemy
Database Dictionary
current whole-DB reference
Access/Auth DB reference
direct tests
```

Use declarative PostgreSQL constraints first. Use Account serialization only for Account-wide security races. Do not lock unrelated rows globally.

## 13. M4 API/client/Web path

For each vertical slice:

```text
FastAPI/Pydantic contract
→ RFC9457 errors
→ deterministic OpenAPI snapshot
→ Orval Fetch generation
→ governed @dante/api-client
→ Web remote/application boundary
→ TanStack Query lifecycle
→ Access state transition only on authoritative response
```

No hand-written parallel client and no raw generated operation imports from presentation code.

## 14. M4 browser/DB proof

At minimum prove on real PostgreSQL and real HTTPS browser stack:

```text
signup happy path
normalized duplicate/collision path
verification valid
verification expired
verification replay
verification concurrent double-consume
recovery known/unknown externally neutral
recovery rate limit
reset valid
reset expired/replayed
reset concurrent consume
password policy/breach failure
post-reset session revocation behavior
reauth success/failure/freshness expiry
email dependency unavailable
PostgreSQL unavailable
no false frontend success
no secret leakage in observability
```

Critical race/replay tests must not rely only on mocks.

## 15. M4 closure gate

M4 closes only when:

```text
contract + persistence + runtime implementation complete
security/code review PASS
OpenAPI/generated-client drift PASS
real PostgreSQL race/replay proof PASS
Chromium/Firefox/WebKit critical browser proof PASS
observability safe/usable for M4 flows
manual UAT PASS
current docs reconciled
user explicitly accepts M4
```

---

# M5 — Google + Apple + Passkeys + Explicit Linking

## 16. M5 goal

Add passwordless/external authentication mechanisms **without weakening DANTE Account identity or silently merging people/accounts**.

**Status:** `PLANNED / AFTER M4`

## 17. M5.1 Provider architecture revalidation

Before coding, verify official current Google/Apple flows and platform requirements. Provider specifications change; use current first-party documentation during implementation.

Preserve:

```text
ExternalIdentity key = issuer + subject
provider email is an attribute/evidence, not Account identity key for linking
provider authentication != provider-data integration authorization
provider token != DANTE AuthSession
DANTE creates its own AuthSession after successful provider authentication
```

## 18. M5.2 Explicit collision/linking state machine

Design first:

```text
new provider subject / no collision
existing linked subject
same email on an existing Account but no link
already-authenticated user adding provider
provider subject already linked to another Account
link confirmation / recent-auth requirement
unlink constraints / account lockout prevention
```

Never silently merge based on matching provider email.

Account linking is a security-sensitive Account-wide mutation and must use the accepted serialization/concurrency strategy.

## 19. M5.3 Google + Apple

Implement separately behind a common Auth mechanism boundary only where semantics genuinely align.

Prove:

```text
state/nonce/PKCE as applicable
redirect/callback integrity
issuer/audience/subject validation
clock/skew handling
provider key rotation behavior
cancel/error paths
replay resistance
explicit linking collisions
provider outage/degradation
```

Do not store provider access/refresh tokens merely for login if not required. Gmail/Calendar/iCloud integration authorization belongs to a separate integration capability.

## 20. M5.4 WebAuthn/passkeys

Close before persistence:

```text
RP ID / origin policy
credential ID uniqueness
public key + sign counter/metadata semantics
user handle strategy
attestation posture
resident/discoverable credential posture
UV requirement
registration recent-auth requirement
multiple passkeys per Account
rename/delete/revoke lifecycle
lost-device recovery interaction
```

Passkey private keys never exist on DANTE servers.

Use current WebAuthn/FIDO guidance during implementation; do not freeze browser/platform assumptions from old knowledge.

## 21. M5 proof matrix

Real-browser/device-capable proof where available:

```text
Google happy/cancel/error/collision/link/replay
Apple happy/cancel/error/collision/link/replay
provider-email mismatch/change does not silently relink
passkey registration/authentication
multiple passkeys
credential replay/challenge expiry
wrong RP/origin
credential removal + remaining-account-access rule
passwordless Account
Account with password + provider + passkey combinations
session issuance remains DANTE AuthSession
observability contains no provider token/authorization code/passkey secret
```

Cross-browser coverage must include browser/platform limits honestly; do not fake support where the environment cannot execute it.

## 22. M5 closure gate

Security review + current provider/WebAuthn spec verification + direct integration proof + collision/linking concurrency proof + manual UAT + docs + explicit user acceptance.

---

# M6 — Native Mobile Access

## 23. M6 goal

Materialize Access on the existing Expo / React Native / Expo Router foundation while preserving one canonical backend Auth model and using **native-appropriate** credential/session handling.

**Status:** `PLANNED / AFTER M5 UNLESS EXPLICITLY RE-GATED`

## 24. M6 architecture gate

Do not copy browser cookie/storage mechanics blindly into Native.

Close current native security topology first:

```text
transport/session credential shape
SecureStore/Keychain/Keystore use
CSRF applicability vs native client model
refresh/reissue semantics if required
app lifecycle/background behavior
multiple device sessions
logout/revoke
uninstall/reinstall semantics
universal/deep link handling for verification/recovery/provider callbacks
passkey platform APIs
```

Backend canonical Account/AuthSession semantics remain shared. If Native requires a different transport credential representation, it must still map to the same server-side session authority and revocation model.

## 25. M6 UX/materialization

Reuse semantic Access states but design platform-appropriate native composition. Mobile Native is not scaled-down Web.

Must cover:

```text
signin
signup
verification/deep link
recovery/reset/deep link
reauth
Google/Apple where platform-appropriate
passkeys
linking/collision flows
loading/offline/background transitions
accessible keyboard/focus/error behavior
```

## 26. M6 security/proof

At minimum:

```text
no secrets in AsyncStorage/plaintext storage
secure credential persistence proof
app restart/session restoration
logout/revoke convergence
expired/revoked session
deep-link tampering
provider callback integrity
lost/invalid local credential
network loss/retry behavior
multiple-device session independence
native logs/telemetry redaction
```

Use real device/emulator platform proof for critical native-only semantics. Browser tests do not prove Native security/storage.

## 27. M6 closure gate

Native architecture/security contract accepted, implementation complete, platform tests/UAT complete, shared backend regression green, docs current, user explicitly accepts M6.

---

# M7 — Security Hardening + Authenticated Handoff + Whole-Vertical Closure

## 28. M7 goal

Prove the **entire Access/Auth vertical** as one coherent production-grade system and hand an authenticated Principal/session safely into the next DANTE product vertical.

**Status:** `PLANNED / FINAL ACCESS-AUTH MACRO-PHASE`

M7 is not a bucket for work we knowingly skipped earlier. Each M4–M6 slice must meet its own quality bar first.

## 29. M7.1 Whole-vertical threat review

Re-run threat analysis over the implemented system, including:

```text
credential stuffing / password spraying
user enumeration
rate/resource exhaustion
session fixation/theft/replay
CSRF/origin/fetch-metadata bypass
verification/recovery/reset replay
email compromise implications
provider/OIDC replay/collision/linking
WebAuthn challenge/origin/RP mistakes
Account lockout/recovery traps
concurrent security mutations
ambiguous commits
logging/telemetry secret leakage
native credential theft/device-loss cases
```

Every finding gets one of: fix, accepted bounded risk with rationale, or explicitly deferred owner/trigger. No vague TODOs.

## 30. M7.2 Session/account management

Close any product-required management surface such as:

```text
list active sessions/devices if selected
revoke one session
revoke other sessions
security-change session invalidation
credential/passkey/provider inventory where selected
account recovery safety
```

Do not add dashboards/settings merely because other apps have them; implement what the accepted DANTE product contract requires.

## 31. M7.3 Authenticated handoff

The Access vertical must end in a real server-authoritative handoff, not a mock Home transition.

Close:

```text
what route/shell receives authenticated user
what minimum Principal/session data it may consume
first-run/setup distinction
authorization boundary
loading/degraded behavior
Home workstream integration ownership
no Access feature leakage into unrelated product features
```

Coordinate with the separate Home/frontend workstream under an explicit integration gate. Do not merge or rewrite that worktree implicitly.

## 32. M7.4 Operational/security release gate

At minimum:

```text
static/type/lint/architecture/generated/build PASS
full backend suite PASS
real PostgreSQL suite PASS
migration upgrade/downgrade/drift PASS as applicable
real HTTPS browser regression PASS
Native regression PASS where supported
observability dashboards/queries prove critical paths
no secret leakage review
rate/dependency/outage behavior PASS
accessibility/responsive checks PASS
privacy/legal destination links/content real and current where required
supply-chain/dependency review
CI/release configuration truthful
backup/recovery requirements triggered by deployment stage assessed
```

Dependabot/security findings are evaluated deliberately at M7 or earlier if they affect an active dependency/security path; never disable controls merely to get green CI.

## 33. M7 manual acceptance

User must actually exercise the complete Access/Auth journey that is intended for release:

```text
new account
verification
signin
recovery/reset
reauth-sensitive operation
provider/passkey path(s)
multiple sessions/devices where applicable
logout/revoke
native path where applicable
authenticated handoff
```

Issues found in UAT are fixed and re-proved before acceptance.

## 34. Whole-vertical closure formula

```text
M1 CLOSED
+ M2 CLOSED
+ M3 CLOSED
+ PRE-M4 observability baseline CLOSED
+ M4 CLOSED
+ M5 CLOSED
+ M6 CLOSED
+ M7 whole-vertical review/handoff PASS
+ user explicit whole-vertical acceptance
= ACCESS/AUTH VERTICAL CLOSED
```

Do not claim whole Access/Auth closure before this formula is true.

---

## 35. Cross-phase engineering gates

Every M4–M7 code slice should follow:

```text
contract/authority readback
→ smallest production-complete slice
→ schema only if semantically required
→ backend application/domain/adapter implementation
→ OpenAPI
→ generated client
→ platform integration
→ static/unit tests
→ real PostgreSQL/integration proof
→ real platform/browser proof for critical behavior
→ degradation/race/replay tests
→ manual UAT when user-visible
→ documentation reconciliation
→ explicit macro-phase gate
```

No phase is “done” because code compiles or happy-path tests pass.

---

## 36. Observability across M4–M7

Once PRE-M4 closes, every security-sensitive new capability must add safe telemetry at the same time as implementation:

```text
stable event names
safe machine outcome categories
trace spans across external dependencies
low-cardinality metrics
request/trace correlation
redaction tests
```

Telemetry is evidence/debugging support, never canonical product truth and never a substitute for database history/audit semantics.

---

## 37. Documentation/handoff rule

At each macro closure update at minimum:

```text
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/access-auth.md
this execution plan when future sequencing changes
docs/frontend/access.md when Web/Native Access contract changes
Access/Auth architecture/security/API/testing docs when their authority changes
docs/database/* + Dictionary when persistence changes
```

A future chat should not need conversation history to know:

```text
what is closed
what is next
which branch/worktree to use
which decisions are frozen
which mistakes are forbidden
what proof is required
what exact gate closes the phase
```

---

## 38. Merge/history rule

The whole vertical stays on `feature/access-auth` unless explicitly re-gated. Do not merge to `main`, rebase, squash, force-push or rewrite the connector-polluted branch history without explicit user approval.

Before eventual merge, review whether the user wants a clean squash/history rewrite. Tree correctness and evidence come first; history aesthetics never justify an unauthorized force rewrite.
