# DANTE — Access/Auth M4–M7 Execution Plan

- **Status:** CURRENT EXECUTION PLAN / M4 NEXT / M5–M7 PLANNED
- **Vertical:** Access/Auth
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **Prerequisite:** M1–M3 CLOSED; M3 engineering gate PASS; user acceptance ACCEPTED
- **Observability rule:** quick feasibility before M4; implement early only if bounded/non-invasive, otherwise defer full baseline to M7
- **Purpose:** remove ambiguity for future chats/engineers, preserve M3 lessons, and define the safe production-quality sequence from the accepted AuthSession spine to whole-vertical closure.

> This plan does not reopen M1–M3 and does not authorize a new branch/worktree. Repository truth and accepted Access/Auth architecture/security/API/testing contracts remain binding.

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

Never infer that a new chat means a new branch/worktree.

---

## 2. M3 frozen foundations — reuse, do not replace

M4–M7 build on:

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
ambiguous-commit reconciliation only where explicitly designed
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

## 3. Permanent M3 lessons / regression guards

### 3.1 Unknown remote truth is not a business state

```text
unknown/loading
!= signed-out
!= signed-in
!= empty
!= error
```

If first-screen correctness depends on remote state, resolve/coordinate it at the route/bootstrap boundary. Do not paint a false business state and repair it later.

### 3.2 Router-first Auth bootstrap remains canonical

```text
hard load
→ route loader resolves/prefetches /auth/session
→ Query cache ready
→ AccessPage mounts
→ first business render is authoritative
```

Do not reintroduce login-first + effect repair, `visibility:hidden` sign-in geometry, or persisted client Auth cache.

### 3.3 Feature boundaries are real architecture

Routes consume Access through its public API. Presentation/model code does not reach raw generated transport internals. Platform Web code owns browser transport policy. Generated code is never hand-edited.

### 3.4 Real degraded/race/replay proof is mandatory

Happy path alone is insufficient for security-sensitive slices. Use real PostgreSQL and real product boundaries where practical. Do not expose public production `/test/*` endpoints merely to make E2E easy.

### 3.5 Tooling/documentation discipline

Pure Prettier/Ruff drift uses repo formatters. Lockfiles/generated artifacts are not hand-edited. A capability is not closed until code, generated contracts, DB artifacts where applicable, docs and executable evidence agree.

---

# 4. Observability quick-feasibility decision

## 4.1 Intent

Observability is useful before verification/recovery/provider complexity, but it must **not** become an early infrastructure programme that delays M4.

Before M4 implementation, perform only a bounded architecture/readback and determine whether a useful baseline is genuinely small and isolated.

## 4.2 Quick-path scope

Suitable for implementation before M4 only if the work can stay roughly within:

```text
structured privacy-safe backend logs
request_id correlation
trace_id/span_id correlation where available
minimal OpenTelemetry traces/metrics
small disposable local collector/backend path
one representative Auth query/dashboard path
secret-redaction/leakage proof
```

Application instrumentation remains vendor-neutral.

Candidate technologies may include:

```text
OpenTelemetry
Grafana
Grafana Alloy
Loki
Tempo
Prometheus or Mimir
```

These are candidates, not mandatory brands.

## 4.3 Early-stop conditions

Do **not** implement full observability before M4 if it requires any meaningful combination of:

```text
new product/domain persistence
invasive M3 Auth refactor
large permanent infrastructure subsystem
new cross-service business architecture
production deployment/on-call design
CI/release redesign
retention/alerting/platform operations project
significant operational ownership before a real deployment exists
```

Decision rule:

```text
small / isolated / immediately useful
→ implement + prove before M4

scope expands materially
→ document DEFERRED TO M7
→ start M4
```

No guilt and no scope creep when deferring.

## 4.4 Security rules regardless of timing

Never emit:

```text
passwords
session/cookie/token values
CSRF secrets
verification/recovery/reset raw proof secrets
OAuth authorization codes/access/refresh tokens
passkey private material
password hashes/pepper
secret-link full URLs
sensitive request/response bodies by default
unbounded provider payloads
```

Never use raw email/account/session/request identifiers or arbitrary error strings as metric labels.

If full observability is deferred, M4–M6 still require safe logs/errors and leakage tests around new secret-bearing flows.

## 4.5 If the quick path is taken

Minimum proof:

```text
real Auth request correlates request_id ↔ safe log ↔ trace
basic HTTP/Auth metrics visible
signin success/failure visible without secrets
real PostgreSQL outage observable
collector/backend outage does not fail Auth correctness
redaction/leakage tests PASS
one local dashboard/query path usable
format/lint/type/build gates PASS
operational docs current
```

If that proof cannot be reached without expanding scope, stop and defer.

---

# 5. M4 — Signup + Verification + Recovery + Reset + Reauth

**Status:** `NEXT / NOT STARTED`

## 5.1 Goal

Complete the first-party Account lifecycle around the accepted M3 signin/AuthSession spine without creating parallel security roots.

## 5.2 M4.1 Account establishment / signup contract

Close before code/schema:

```text
when Account is created
when EmailIdentity is created
verified vs unverified semantics
password establishment path
normalization/collision behavior
whether unverified Account may sign in and with what authority
abandoned-signup cleanup/expiry if any
concurrent duplicate signup behavior
```

`Person != Account` remains binding. Signup must not silently create Person without an accepted product contract.

## 5.3 M4.2 Verification proof lifecycle

Close:

```text
secret entropy / encoding
stored verifier/digest shape
purpose binding
Account / EmailIdentity binding
issued / expires / consumed semantics
single-use behavior
reissue / supersession / invalidation
concurrent double-consume
ambiguous commit behavior
safe public response
```

Verification success is backend-authoritative. Clicking a link is not frontend authority.

Do not begin with a generic `auth_token(type,payload,status)` table.

## 5.4 M4.3 Email delivery boundary

Introduce a provider-independent port/adapter boundary.

Close:

```text
message purpose/template identity
recipient contract
secret-link construction at safe boundary
provider message identifier where useful
send attempt/result semantics
local deterministic protocol-faithful substitute
provider unavailable/degraded behavior
```

Do not fake successful delivery in production code.

Transactional outbox activates only if the real delivery/effect contract proves it is required. Do not activate it ceremonially.

## 5.5 M4.4 Recovery initiation

Public initiation must resist account enumeration.

Close:

```text
known vs unknown email external equivalence
bounded rate/resource limits
proof issuance/replacement semantics
email dependency unavailable behavior
request_id / diagnostics behavior
no Account-existence disclosure
```

## 5.6 M4.5 Password reset

Close:

```text
proof validation/consumption
M3 password policy + HIBP + KDF reuse
Account security serialization
PasswordCredential replacement
session revocation policy
current session/request behavior
ambiguous commit reconciliation
notification/audit requirement if any
```

No blind retry of reset mutation.

## 5.7 M4.6 Reauthentication / recent-auth

Represent real server-side assurance/freshness, not a UI boolean.

Close:

```text
which operations require recent Auth
what methods satisfy reauth
freshness duration
server-side representation/session binding
failure/lock/rate-limit behavior
step-up vs initial signin distinction
```

Password may be the first method while the model stays compatible with passkey/provider reauth in M5.

## 5.8 M4 persistence discipline

Derive exact DB objects from the closed lifecycle. Every structural change updates together:

```text
Alembic
SQLAlchemy
Database Dictionary
current whole-DB reference
Access/Auth DB reference
direct tests
```

Use declarative PostgreSQL constraints first. Use Account serialization only for Account-wide security races.

## 5.9 M4 API/client/Web chain

For each vertical slice:

```text
FastAPI/Pydantic
→ RFC9457 problems
→ deterministic OpenAPI
→ Orval Fetch generation
→ governed @dante/api-client
→ Web remote/application boundary
→ TanStack Query lifecycle
→ authoritative Access transition only on backend result
```

No parallel hand-written client and no raw generated operation imports from presentation code.

## 5.10 M4 real proof matrix

At minimum:

```text
signup happy path
normalized duplicate/collision
verification valid
verification expired
verification replay
verification concurrent double-consume
email dependency unavailable
recovery known/unknown externally neutral
recovery rate limit
reset valid
reset expired/replayed
reset concurrent consume
password policy/HIBP failure
post-reset session revocation
reauth success/failure/freshness expiry
PostgreSQL unavailable
no false frontend success
no secret leakage in logs/errors/telemetry if active
```

Critical race/replay tests must not be mocks only.

## 5.11 M4 closure gate

M4 closes only when:

```text
contract + persistence + runtime complete
security/code review PASS
OpenAPI/generated-client drift PASS
real PostgreSQL race/replay proof PASS
critical Chromium/Firefox/WebKit proof PASS
manual UAT PASS
current docs reconciled
user explicitly accepts M4
```

Full Grafana/OTel observability is **not** an M4 blocker if explicitly deferred by the quick-feasibility decision.

---

# 6. M5 — Google + Apple + Passkeys + Explicit Linking

**Status:** `PLANNED / AFTER M4`

## 6.1 Goal

Add external/passwordless authentication without weakening DANTE Account identity or silently merging Accounts.

## 6.2 Current-spec gate

Before coding, verify current official Google, Apple and WebAuthn/FIDO documentation. Do not implement provider flows from stale memory.

Preserve:

```text
ExternalIdentity key = issuer + subject
provider email is evidence/attribute, not an automatic link key
provider authentication != provider-data integration authorization
provider token != DANTE AuthSession
DANTE creates its own AuthSession after successful provider authentication
```

## 6.3 Explicit linking/collision state machine

Design before implementation:

```text
new provider subject / no collision
existing linked subject
same email on existing Account but no link
already-authenticated user adding provider
subject already linked to another Account
link confirmation / recent-auth requirement
unlink constraints / Account lockout prevention
concurrent linking races
```

Silent provider-email merge is forbidden.

## 6.4 Google + Apple

Prove as applicable:

```text
state / nonce / PKCE
redirect/callback integrity
issuer / audience / subject validation
clock/skew handling
provider key rotation
cancel/error paths
replay resistance
linking collisions
provider outage/degradation
```

Do not store provider access/refresh tokens merely for login if not required. Gmail/Calendar/iCloud authorization is a separate integration capability.

## 6.5 WebAuthn / passkeys

Close before persistence:

```text
RP ID / origin policy
credential ID uniqueness
public-key storage
user handle strategy
UV requirement
attestation posture
resident/discoverable credential posture
multiple passkeys per Account
registration recent-auth
rename/delete/revoke lifecycle
lost-device recovery interaction
```

Passkey private keys never exist on DANTE servers.

## 6.6 M5 proof matrix

```text
Google happy/cancel/error/collision/link/replay
Apple happy/cancel/error/collision/link/replay
provider-email change/mismatch never silently relinks
passkey registration/authentication
multiple passkeys
challenge expiry/replay
wrong RP/origin
credential removal + remaining Account access
passwordless Account
password + provider + passkey combinations
session issuance remains DANTE AuthSession
no provider token/code/passkey secret leakage
```

Cross-browser/platform support is proved honestly; do not fake universal compatibility.

## 6.7 M5 closure

Current-spec review + security review + direct integration/replay/collision concurrency proof + platform/browser UAT + docs + explicit user acceptance.

---

# 7. M6 — Native Mobile Access

**Status:** `PLANNED / AFTER M5 UNLESS EXPLICITLY RE-GATED`

## 7.1 Goal

Materialize Access on the existing Expo / React Native / Expo Router foundation while preserving one canonical backend Auth model and using native-appropriate security.

## 7.2 Native architecture gate

Do not copy browser cookie/storage mechanics blindly.

Close:

```text
native transport/session credential representation
SecureStore / Keychain / Keystore usage
CSRF applicability
refresh/reissue semantics if required
app restart/background lifecycle
multiple-device sessions
logout/revoke
uninstall/reinstall semantics
verification/recovery/provider deep links
passkey platform APIs
```

If Native needs a different transport credential representation, it still maps to the same server-side AuthSession authority and revocation model.

## 7.3 Native UX

Cover:

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
keyboard/focus/accessibility
```

Native is not scaled-down Web.

## 7.4 Native proof

```text
no Auth secret in AsyncStorage/plaintext
secure credential persistence
app restart/session restoration
logout/revoke convergence
expired/revoked session
deep-link tampering
provider callback integrity
lost/invalid local credential
network loss/retry behavior
multiple-device independence
no native log/telemetry secret leakage
```

Critical native-only semantics require emulator/device proof.

## 7.5 M6 closure

Accepted native architecture/security contract + implementation + platform tests/UAT + shared backend regression + docs + explicit user acceptance.

---

# 8. M7 — Security Hardening + Authenticated Handoff + Whole-Vertical Closure

**Status:** `PLANNED / FINAL ACCESS-AUTH MACRO-PHASE`

## 8.1 Goal

Prove the entire Access/Auth vertical as one coherent production-grade system and hand an authenticated Principal/session safely into the next DANTE product vertical.

M7 is not a dumping ground for known M4–M6 correctness/security defects. Earlier phases still close their own scope.

## 8.2 Whole-vertical threat review

Re-test:

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
native credential theft/device-loss
```

Every finding becomes: fixed, bounded accepted risk with rationale, or explicit deferred owner/trigger. No vague TODOs.

## 8.3 Session/account management

Implement only product-required surfaces such as:

```text
active session/device listing if selected
revoke one session
revoke other sessions
security-change invalidation
credential/passkey/provider inventory if selected
Account recovery safety
```

No ceremonial settings just because other products have them.

## 8.4 Authenticated handoff

Close:

```text
real next route/shell
minimum Principal/session data it may consume
first-run/setup distinction
authorization boundary
loading/degraded behavior
Home workstream integration ownership
no Access internals leaking into unrelated features
```

Coordinate with the separate Home/frontend worktree only through an explicit integration gate.

## 8.5 Observability release gate

If the quick pre-M4 path was deferred, M7 must now close a production-credible baseline. At minimum:

```text
privacy-safe structured logs
request_id ↔ trace correlation
OpenTelemetry traces/metrics or explicitly superior current equivalent
collector/backend topology
low-cardinality service/Auth metrics
representative logs/trace/metrics queries or dashboards
secret-redaction tests
telemetry-outage non-fatal behavior
operational documentation
```

Technology choice is current-spec/evidence based. Grafana/Alloy/Loki/Tempo/Prometheus/Mimir remain candidates, not mandatory brands.

## 8.6 Release/operational gate

At minimum:

```text
static/type/lint/architecture/generated/build PASS
full backend suite PASS
real PostgreSQL suite PASS
migration/drift proof PASS
real HTTPS browser regression PASS
Native regression PASS where supported
observability gate PASS
secret-leakage review PASS
rate/dependency/outage behavior PASS
accessibility/responsive PASS
privacy/legal destinations current where required
supply-chain/dependency review
CI/release configuration truthful
backup/recovery requirements assessed against actual deployment stage
```

## 8.7 Manual whole-vertical UAT

User exercises release-intended journey:

```text
new Account
verification
signin
recovery/reset
reauth-sensitive operation
provider/passkey paths
multiple sessions/devices where applicable
logout/revoke
Native path where applicable
authenticated handoff
```

Issues are fixed and re-proved before acceptance.

## 8.8 Whole-vertical closure formula

```text
M1 CLOSED
+ M2 CLOSED
+ M3 CLOSED
+ M4 CLOSED
+ M5 CLOSED
+ M6 CLOSED
+ observability baseline CLOSED either early or in M7
+ M7 whole-vertical review/handoff PASS
+ user explicit whole-vertical acceptance
= ACCESS/AUTH VERTICAL CLOSED
```

Do not claim whole Access/Auth closure before this formula is true.

---

## 9. Cross-phase engineering gate

Every M4–M7 code slice follows:

```text
contract/authority readback
→ smallest production-complete slice
→ schema only if semantically required
→ backend implementation
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

No phase is done because code compiles or the happy path passes.

---

## 10. Documentation/handoff rule

At each macro closure update at minimum:

```text
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/access-auth.md
this execution plan when sequencing changes
docs/frontend/access.md when Access contract changes
architecture/security/API/testing docs when authority changes
docs/database/* + Dictionary when persistence changes
```

A future chat must be able to determine without conversation history:

```text
what is closed
what is next
which branch/worktree to use
which decisions are frozen
which mistakes are forbidden
what proof is required
what gate closes the phase
```

---

## 11. Merge/history rule

The vertical stays on `feature/access-auth` unless explicitly re-gated. Do not merge to `main`, rebase, squash, force-push or rewrite connector-polluted history without explicit user approval.

Before eventual merge, ask whether the user wants a clean squash/history rewrite. Tree correctness and evidence come first.
