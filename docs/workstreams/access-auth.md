# DANTE — Access/Auth Full-Stack Vertical Workstream

- **Status:** ACTIVE / BRANCH-LOCAL DURABLE WORKSTREAM RECORD
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Created from protected `main`:** `f011e252b6a294a12c38927ef2d528244ea1fee6`
- **M2.1–M2.8 documentation PRE-SCOPE:** `e969b47ca9c57c5ffa34fb3eeb0145f40ea7efba`
- **M2 closure documentation PRE-SCOPE:** `1d685dc43dd68916afa34ec84b7f45df20c890b0`
- **M3-A production gate PRE-SCOPE:** `ea75bb33e88bd256018c73ae444cff48a510af63`
- **Current macro-phase:** `M3 — Email/Password Signin + AuthSession Spine` — ACTIVE / DB FOUNDATION MATERIALIZED + DIRECT DB PROOF PASS / AUTH RUNTIME NOT YET
- **Last closed macro-phase:** `M2 — Auth Architecture Freeze` — CLOSED / M2.1–M2.11 ACCEPTED / DOCUMENTED / READBACK QA PASS
- **Purpose:** operational save-game, authority map, roadmap, decision register, evidence boundaries and Git/write safety for the production Access/Auth vertical.

> This file is the branch-local operational continuation authority while `feature/access-auth` is active. Durable architecture/security/API/testing truth belongs in the subject-oriented contracts and ADR-011. Do not turn this file into the sole Auth specification or a chat diary.

---

## 1. Mandatory new-session bootstrap

A new chat, agent or context window does **not** create a new project, branch or worktree.

Continue:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

The separate worktree `/home/mattia/projects/dante-frontend` may host independent frontend work such as Home, but Access/Auth frontend changes required by this vertical remain on `feature/access-auth` unless explicitly re-gated.

At the start of each session:

1. read root `README.md`;
2. read `docs/README.md`;
3. read `docs/PROJECT-STATUS.md`;
4. read `docs/ROADMAP.md`;
5. read `docs/development/agent-operating-manual.md`;
6. read current safety/branching/documentation-lifecycle rules;
7. read this file completely;
8. read `docs/frontend/access.md`;
9. read current Access/Auth durable authorities:
   - `docs/architecture/access-auth-architecture.md`;
   - `docs/architecture/access-auth-security-contract.md`;
   - `docs/architecture/access-auth-api-contract.md`;
   - `docs/architecture/access-auth-testing-contract.md`;
   - `docs/decisions/ADR-011-access-auth-architecture.md`;
10. inspect current backend/database/frontend authorities relevant to the active slice, including `docs/database/README.md`, the whole-DB current reference and `docs/database/access-auth.md`;
11. verify remote branch HEAD and local worktree before any write.

Local verification minimum:

```bash
pwd
git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
git rev-parse origin/feature/access-auth
git worktree list --porcelain
```

Repository truth beats conversation memory.

---

## 2. Authority order

Use the strictest applicable current source:

```text
protected-main implementation / migrations / tests
+ accepted Domain / Logical / Physical / architecture decisions
↓
current durable subsystem/product/database docs
↓
current branch-local Access/Auth architecture/security/API/testing contracts + ADR-011
↓
current branch-local DB migration/mapping/Dictionary/reference candidate where newer and explicitly scoped
↓
this active workstream for operational state/newer unresolved slice decisions
↓
current feature/access-auth implementation
↓
historical CP6 / Access-frontend evidence
↓
conversation memory
```

Important sources include:

- `docs/frontend/access.md`;
- the four `docs/architecture/access-auth-*.md` contracts;
- `docs/decisions/ADR-011-access-auth-architecture.md`;
- frontend production-readiness contracts/gates;
- `docs/database/README.md` + whole-DB current/evolving reference + Database Dictionary;
- `docs/database/access-auth.md` for detailed current Access/Auth DB semantics;
- ADR-007 / ADR-008 / ADR-009 / ADR-010;
- PostgreSQL CP3/CP6 persistence/QA evidence;
- current backend mappings/migrations/tests;
- current Access state machine/UI/release tests.

Historical records remain evidence, never newer authority.

### Current-reference lifecycle rule

`docs/development/documentation-lifecycle-policy.md` now makes this permanent across DANTE:

```text
CURRENT / EVOLVING REFERENCE
→ must track accepted present truth
→ a deferred/open claim is reconciled when its trigger fires

FROZEN EVIDENCE / HISTORY
→ preserves exact historical context
→ is not rewritten to pretend later knowledge existed earlier
```

For database evolution specifically:

```text
structural DB change
→ migration
→ mapping
→ Dictionary
→ whole-DB current reference
→ subject/vertical DB reference when applicable
→ tests/proof
→ audit of prior DEFERRED/OPEN/TBD claims whose trigger was satisfied
```

A document is not frozen merely because it was created during CP6. The whole-DB Database Architecture & Reference is current/evolving; CP6 migrations, CP6 acceptance evidence and Git history remain the historical record.

---

## 3. Foundations closed before this vertical

### Domain / Logical / Physical

Preserve:

```text
Possibility / Proposal != Decision != Plan != Action != Actual != Outcome != Progress
Person != Account != Principal != Actor
Responsibility != Participation != Authority
```

### Backend / PostgreSQL CP1–CP6

Already integrated:

- FastAPI/Python backend foundation;
- PostgreSQL canonical persistence;
- async SQLAlchemy;
- Alembic forward migration discipline;
- owner/migrator/runtime roles and ACL;
- persistence mappings;
- whole-database materialization;
- PostgreSQL acceptance/integrity/runtime tests;
- backend CI.

CP6 intentionally did not invent speculative Account/Principal/Auth persistence because the Access/Auth trigger had not yet closed.

Protected-main CP6 baseline before M3 Auth migration:

```text
PostgreSQL          18.6
Alembic head        20260826_08
68 tables
5 views
14 routines
75 triggers
95 physical indexes
68 foreign keys
120 CHECK constraints
```

That CP6 deferral was correct historically. It is not current unresolved truth on `feature/access-auth` after M2 closure and M3-A DB materialization.

### Frontend foundation

Already integrated/materialized:

- Web Access shell and accepted visual direction;
- responsive desktop/tablet/mobile-Web behavior;
- IT/EN;
- Access state graph;
- signup/recovery/provider/linking/reauth/setup surfaces;
- local validation;
- accessibility/reduced-motion treatment;
- Playwright release matrix;
- frontend CI;
- explicit refusal to fake server-authoritative success.

The existing Web Access implementation is production UI/state foundation, not disposable mock code.

### Mobile foundation

Already materialized:

```text
Expo 57
React Native 0.86.x
Expo Router
React 19.2.x
```

Native Mobile Access remains M6, but technology/foundation are not open choices.

---

## 4. Current implementation reality

### Backend

No dedicated production Access/Auth application service, password runtime, session middleware/Principal derivation or real Auth HTTP API exists yet.

### Database

The M3-A database foundation **source is materialized on this branch** at Alembic `20260827_09`:

```text
dante.account
dante.email_identity
dante.password_credential
dante.auth_session
```

Aligned source representations currently exist across:

```text
Alembic 20260827_09
SQLAlchemy mappings + MAPPED_TABLES
Database Dictionary v1
whole-DB current reference routing
docs/database/access-auth.md
migration/current-catalog tests
```

Current branch inventory encoded by the source/Dictionary candidate is:

```text
72 tables
5 views
14 routines
75 triggers
104 physical indexes
71 foreign keys
137 CHECK constraints
```

**Direct real PostgreSQL proof is complete.** The targeted disposable PostgreSQL 18.6 suite proved the current 72-table branch catalog, frozen CP6 baseline isolation, migration round-trip/Alembic drift contract and exact M3-A Auth runtime ACLs. This closes the database-foundation proof only; M3 runtime/full-stack proof remains open.

Not yet materialized:

```text
ExternalIdentity
PasskeyCredential
verification/recovery proof persistence
provider state
MFA persistence
Principal table (deliberately not selected)
```

### Web

Accepted UI/state model exists. Real backend/session/generated-client wiring and authenticated next-route handoff do not.

### Mobile

Foundation exists; Native Access does not.

### OpenAPI/generated client

M2 selected the contract/tooling boundary, but no Auth OpenAPI snapshot, Orval package, `@dante/api-client` or TanStack Query Auth integration has been materialized yet.

### Test harness

M2 selected the proof contract. The first M3-A database proof has now executed successfully against the disposable PostgreSQL 18.6 harness:

```text
ruff format --check .                                               PASS
ruff check .                                                        PASS
mypy                                                                PASS / 42 source files
migration / CP6 baseline / current catalog targeted suite           PASS / 7 of 7
```

The Access/Auth cross-stack CI/full-stack HTTPS browser harness does not exist yet.

These are M3 executable obligations, not missing M2 architecture work.

---

## 5. M2 durable authority map

M2.1–M2.11 accepted truth is now durably organized by stable subject:

```text
docs/architecture/access-auth-architecture.md
→ Account/identity/authenticator/session/Web-Native/transaction/client architecture

docs/architecture/access-auth-security-contract.md
→ session/CSRF/password/email/provider/passkey/revocation/security behavior

docs/architecture/access-auth-api-contract.md
→ /api/v1 / RFC9457 / naming / OpenAPI / Orval / generated-client contract

docs/architecture/access-auth-testing-contract.md
→ PostgreSQL/API/generated/browser/full-stack/CI proof contract

docs/decisions/ADR-011-access-auth-architecture.md
→ accepted rationale, consequences and rejected alternatives
```

This workstream references those authorities rather than duplicating every normative detail.

---

## 6. Product/security semantic constitution

Mandatory unless reopened by stronger evidence:

```text
Person != Account
Account != Principal
Principal != Actor
AuthSession != DANTE Session
signin != provider-data integration authorization
provider state != DANTE canonical state
verification != setup completion
reauthentication != initial signin
client/device signal != identity
frontend request/success != backend-authoritative success
method != factor != assurance
```

Accepted Account/authenticator model:

```text
Account = durable Access/security root
EmailIdentity != Account
PasswordCredential optional
Account may be passwordless
ExternalIdentity key = issuer + subject
provider email never silently links Accounts
Account may have 0..N PasskeyCredential
Principal remains runtime-only absent stronger evidence
AuthSession belongs to Account, not to one authenticator
multiple independent sessions are normal
```

Database consequence now explicit:

```text
DB-U09 Account persistence
→ RESOLVED / M3-A MATERIALIZED ON BRANCH

DB-U10 Principal/security persistence
→ RESOLVED WITHOUT PERSISTENCE
→ runtime Principal only
```

---

## 7. Vertical boundary

### In scope across M3–M7

- Account lifecycle/status;
- EmailIdentity;
- PasswordCredential;
- email/password signin;
- signup + verification;
- recovery/reset;
- reauthentication/recent-auth;
- AuthSession lifecycle/multi-session;
- logout, specific revoke, revoke-all-others, logout-everywhere;
- Google authentication;
- Apple authentication;
- ExternalIdentity;
- passkeys/WebAuthn;
- provider/account collision and explicit linking;
- stable Auth API/OpenAPI/generated client;
- Web Access real wiring;
- Native Mobile Access;
- required DB migrations/mappings/Dictionary/reference;
- rate-limit/replay/race/concurrency behavior;
- full-stack/security QA and authenticated handoff to the next vertical.

### Deferred but architecture-aware

- TOTP/authenticator-app MFA;
- recovery codes;
- optional/mandatory MFA policy;
- future high-security profile.

### Explicitly out of scope unless separately gated

- full Home/Today implementation;
- unrelated frontend pages/polish;
- Gmail/Calendar/iCloud data integrations;
- generic platform-wide RBAC redesign;
- CP1–CP6 rewrites for style;
- third-party public developer platform/SDK lifecycle without product requirement;
- extra branches/worktrees;
- direct work on main;
- merge/rebase/history rewrite without explicit gate.

A minimal protected destination is allowed only to prove authenticated handoff.

---

## 8. Mandatory engineering method

After M2, implement complete vertical slices:

```text
product need/state
→ exact contract
→ domain/application behavior
→ persistence/security
→ FastAPI endpoint
→ OpenAPI
→ generated client
→ Web/Mobile application boundary as applicable
→ real UI transition
→ layered tests
→ real full-stack proof
→ QA
→ durable documentation
```

Do not create generic `BaseService`, `GenericRepository`, giant `AuthManager`, speculative UoW wrappers or mega Auth schema without concrete slice need.

---

## 9. Database / transaction constitution carried into M3

PostgreSQL remains canonical authority.

Every structural Auth change must move applicable artifacts together:

```text
semantic design
Alembic migration
SQLAlchemy mapping/metadata
mapping registry as applicable
Database Dictionary
whole-DB current/evolving reference
subject/vertical human DB reference
prior deferred/open-item reconciliation when trigger satisfied
constraints
justified indexes
least-privilege ACL
direct tests
catalog/schema parity
real PostgreSQL proof
concurrency/negative tests
```

Normal migration history remains forward-only. Applied migrations/history are not rewritten to fake later knowledge, while current references must evolve with accepted current truth.

Transaction carry-forward:

```text
one AsyncSession per application operation/task
autobegin=False
outer operation owns transaction
adapters may flush, never hidden-commit
READ COMMITTED default
narrowest truthful concurrency mechanism
no hidden retry
no blind ambiguous-commit retry
no network/human wait inside DB transaction
```

M2.9 additionally fixes for the first Auth spine:

```text
normal session admission           no Account lock
account-wide security mutation     Account row = serialization point
lock order                         Account → credential/identity → session as needed
advisory Account lock              NOT SELECTED
SKIP LOCKED on security state       NOT SELECTED
signin Argon2/HIBP                  outside authoritative DB mutation
final signin transaction           lock + re-read Account/Credential
stale verified credential          cannot create session
two valid concurrent signins       may create two sessions
simple current logout              conditional idempotent session revoke
revocation barrier                 COMMIT
ambiguous AuthSession commit        reconcile by pre-generated auth_session_ref
Set-Cookie                          only after commit/reconciliation
M3 Redis/JWT session cache          NOT SELECTED
```

---

## 10. Accepted Web/session/security posture

Detailed authority: `docs/architecture/access-auth-security-contract.md`.

```text
WEB TOPOLOGY
same-origin browser path through edge/ingress
/api/v1/*
normal browser CORS off/no ACAO
trusted forwarded headers only from trusted edge

SESSION
opaque 256-bit CSPRNG secret
raw secret never persisted
SHA-256 indexed verifier
__Host-dante-session
Secure + HttpOnly + Path=/ + SameSite=Lax
Domain absent
browser storage auth token forbidden
30-day overall + 30-day inactivity default
background polling != user activity
server-side expiry/revocation authority

CSRF
session-bound synchronizer token
exact Origin
Fetch Metadata
no state-changing GET
pre-auth signin protected by same-origin JSON/request contract

PASSWORD
minimum 15 Unicode code points
NFC
no composition rules
paste/password-manager first-class
Argon2id v19 64 MiB / t=3 / p=4
HMAC-SHA-256 separate pepper
HIBP k-anonymity
bounded KDF concurrency
rehash-on-auth with current-credential recheck

RECOVERY / CHANGE
recovery reset revokes all + fresh signin
normal password change revokes others + rotates current
email change pending/verified/atomic + revokes others

PASSKEY READY
0..N
passwordless Account valid
userVerification required
discoverable credential direction
32-byte opaque userHandle
narrow RP-ID principle
synced/device-bound supported
consumer attestation not mandatory
counter anomaly = risk signal

MFA
implementation deferred
assurance/evidence-aware architecture
mfa_enabled Boolean not full model

CACHE/LOG
sensitive Auth/session responses Cache-Control: no-store
secret-bearing logs forbidden
```

---

## 11. Email identity policy

Detailed authority: architecture/security contracts.

```text
delivery/display address
!= comparison key

local comparison   NFC + Unicode casefold
domain comparison  UTS #46 / IDNA ASCII lowercase
PostgreSQL          final uniqueness arbiter
```

Do not globally remove Gmail dots, strip plus-tags or encode provider-specific alias rules.

Provider verified email may establish new-account email control under policy when no collision exists, but provider email never becomes canonical federated identity or silent-link authority.

Standard consumer Account currently maintains a verified recovery/contact EmailIdentity.

---

## 12. API and generated-client contract

Detailed authority: `docs/architecture/access-auth-api-contract.md`.

Accepted API:

```text
base product namespace           /api/v1
version meaning                  major compatibility generation
API shape                        application intents, not table CRUD
success envelope                 none globally
problem standard                 RFC 9457 application/problem+json
machine code                     namespace.snake_case
category                         broad forward fallback
request_id                       server-authoritative every request
validation                       stable bounded errors[]
anti-enumeration                 end-to-end behavior
Retry-After                      standard header where applicable
retryable                        never blind-mutation permission
operationId                      explicit/stable/unique
human detail/title               never parsed by clients
JSON wire naming                 snake_case
```

M2.10 generated-client path:

```text
FastAPI/Pydantic declarations
→ deterministic committed OpenAPI 3.1 snapshot
→ Orval Fetch
→ framework-neutral @dante/api-client
→ Web/Native transport adapter
→ Access application/data-source boundary
→ UI
```

Selected/not selected:

```text
Orval family                     FIXED
Fetch client                     FIXED
exact Orval patch                qualify/pin during M3
Axios                            NOT SELECTED
Orval React Query hooks          NOT SELECTED
generated file hand editing      FORBIDDEN
remote DEV OpenAPI as CI source  FORBIDDEN
hardcoded PROD base URL          FORBIDDEN
runtime Zod validation           REQUIRED
```

Web adapter owns same-origin credentials + CSRF injection; Native later owns native credential/origin integration.

TanStack Query activates for Web remote request/cache lifecycle in M3, but canonical Auth state remains server-side and Access product/UI state remains separate.

---

## 13. Testing / proof constitution

Detailed authority: `docs/architecture/access-auth-testing-contract.md`.

Required layered proof:

```text
unit/pure application
real PostgreSQL 18.6
real FastAPI HTTP
OpenAPI → Orval → TypeScript/Zod
Web application boundary
same-origin HTTPS browser full stack
```

M3 critical browser spine:

```text
Chromium
Firefox
WebKit
```

Core scenarios include:

```text
real signin
reload/bootstrap
logout
multiple independent BrowserContexts/sessions
expiry
server-side revoke
wrong credentials
degraded/rate-limited failure
```

PostgreSQL race scenarios include two independent real sessions/connections and deterministic barriers, not timing sleeps.

Critical Auth E2E starts unauthenticated rather than using a shared committed Playwright authenticated `storageState`.

Mandatory CI uses synthetic ephemeral accounts/secrets and protocol-faithful local substitutes for external services. No real user/UAT/PROD credential.

Existing Backend CI Gate and Frontend CI Gate remain owners of their lanes. M3 adds an Access/Auth cross-stack gate rather than duplicating all existing jobs.

---

## 14. Definition of Done for executable slices

A slice closes only when all applicable obligations pass:

```text
[ ] product states/intents explicit
[ ] semantic/security invariants preserved
[ ] persistence justified/minimal
[ ] migration/mapping/Dictionary/whole-reference/subject-reference aligned
[ ] resolved former deferrals reconciled in current reference
[ ] DB constraints/indexes/ACL proved
[ ] transaction boundaries explicit
[ ] race/replay/idempotency considered and tested
[ ] HTTP/problem/machine contract stable
[ ] OpenAPI reflects implementation
[ ] generated client deterministic/current
[ ] Web/Mobile consumes intended boundary
[ ] frontend never invents authoritative success
[ ] unit/application tests pass
[ ] real PostgreSQL tests pass
[ ] API integration tests pass
[ ] critical full-stack runtime/browser proof passes
[ ] accessibility/responsive/i18n regressions applicable to changed surface pass
[ ] no known secret canary leakage
[ ] applicable CI gates green
[ ] durable docs/workstream reconciled
[ ] exact write-scope/readback QA passes
```

Happy-path success or high line coverage alone is never a closure criterion.

---

# 15. Definitive roadmap — seven macro-phases

## M1 — Access Visual / UX Freeze

**Status:** `CLOSED / PASS WITH DEFERRED INTEGRATION CHECKS`

Accepted current Web design baseline; no redesign-from-zero. Mobile remains separate platform-appropriate UI. Backend-authoritative transitions may not be faked. Final real-backend/provider/legal/accessibility checks remain vertical-closure obligations.

---

## M2 — Auth Architecture Freeze

**Status:** `CLOSED / M2.1–M2.11 ACCEPTED / DURABLY DOCUMENTED / READBACK QA PASS`

Decision sequence:

```text
1. deployment origin topology                                  CLOSED
2. browser session / cookie / CSRF / CORS                     CLOSED
3. Account / EmailIdentity / PasswordCredential /
   AuthSession / Principal semantics                           CLOSED
4. multi-session lifecycle and revoke/logout policy            CLOSED
5. password hashing + breach-policy implementation             CLOSED
6. passkey-ready authenticator + MFA compatibility             CLOSED
7. email normalization/comparison                              CLOSED
8. API namespace + machine error/naming                        CLOSED
9. M3 transaction/concurrency/session-expiry                   CLOSED
10. OpenAPI → generated client → Web boundary                  CLOSED
11. M3 test matrix / full-stack harness                         CLOSED
12. documentation reconciliation/whole-M2 closure              CLOSED / QA PASS
```

M2 implemented no production Auth runtime. Its output is the constitution under which M3 can build without foreseeable cross-cutting semantic/security rewrite.

---

## M3 — Email/Password Signin + AuthSession Spine

**Status:** `ACTIVE / M3-A DB FOUNDATION MATERIALIZED + DIRECT DB PROOF PASS / AUTH RUNTIME NOT YET`

Goal: first real production authenticated path and reusable Account/AuthSession spine.

Current accomplished source work:

```text
Alembic 20260827_09
Account / EmailIdentity / PasswordCredential / AuthSession
SQLAlchemy mapping + registry
Dictionary v1 post-CP6 evolution + 4 entries
whole-DB/reference lifecycle reconciliation
docs/database/access-auth.md
current migration/catalog/ACL test source
```

The M3-A database foundation is now directly proved against PostgreSQL 18.6. This does not close M3 or the end-to-end M3-A Authenticated Spine.

Remaining required scope:
- password verification/dummy path/rehash policy;
- authoritative multi-session creation;
- secure Web cookie/CSRF/session bootstrap;
- runtime Principal derivation;
- minimal protected authenticated destination;
- current-session logout/revocation;
- `/api/v1` Auth operations + RFC9457;
- deterministic OpenAPI snapshot;
- Orval Fetch + `@dante/api-client`;
- TanStack Query remote session state/application boundary;
- Access signin UI real wiring;
- real PostgreSQL/API/browser full-stack proof;
- Backend + Frontend + Access/Auth CI gates as applicable.

Required negative/race scope includes:

```text
wrong password / unknown-account anti-enumeration
disabled Account
expired/revoked session
repeat logout
session-create rollback/ambiguous outcome
two concurrent signins
signin vs credential replacement/reset/disable
reload/bootstrap valid/invalid
CSRF/Origin/Fetch Metadata
server unavailable / rate limited
HIBP degradation policy
secret redaction
```

Exit gate:

```text
real browser
→ real production-built Web
→ same-origin HTTPS
→ real FastAPI
→ real PostgreSQL 18.6
→ real authoritative AuthSession
→ survives reload
→ protected boundary
→ logout removes current access
→ independent second session survives current logout
```

---

## M4 — Signup + Verification + Recovery + Reset + Reauth

**Status:** `NOT STARTED`

Complete first-party lifecycle around M3 session spine with single-use/replay/race-safe proof state, email delivery port, neutral recovery initiation, reset revocation, fresh signin and assurance-aware reauthentication.

---

## M5 — Google + Apple + Passkeys + Explicit Linking

**Status:** `NOT STARTED`

Implement official current provider mechanisms and WebAuthn while preserving issuer+subject identity, explicit collision linking and canonical DANTE Account/AuthSession semantics.

MFA remains deferred unless explicitly promoted.

---

## M6 — Native Mobile Access

**Status:** `NOT STARTED`

Materialize Access on existing Expo/React Native/Expo Router foundation using the same canonical Auth backend with native-safe credential transport/storage, restart bootstrap, provider/passkey platform integration and real emulator/device proof.

---

## M7 — Security Hardening + Authenticated Handoff + Closure

**Status:** `NOT STARTED`

Whole-vertical threat/rate/replay/concurrency/security-event/session-management/privacy/legal/accessibility/native/CI/database/client-drift proof and minimal authenticated handoff into the next product vertical.

Merge to protected `main` requires a separate explicit user gate.

---

## 16. Decision register

| Topic | State | Current position / reopen trigger |
|---|---|---|
| Person != Account | FIXED | Preserve Domain/security boundary. |
| Account != Principal | FIXED | Principal runtime-only absent concrete durable need. |
| Principal != Actor | FIXED | Auth identity does not collapse Domain agency. |
| AuthSession != DANTE Session | FIXED | Explicit security/session naming. |
| Provider auth != data integration | FIXED | Never share semantics/tokens by convenience. |
| PostgreSQL canonical authority | FIXED | Inherited from CP6/ADR-010. |
| Current/evolving reference lifecycle | FIXED | Current references evolve with accepted truth; historical evidence stays historical. |
| Resolved deferred-item reconciliation | REQUIRED | Structural/product evolution audits prior current DEFERRED/OPEN/TBD claims whose trigger fired. |
| DB-U09 Account persistence | RESOLVED / M3-A MATERIALIZED | CP6 deferral trigger satisfied; detailed authority `docs/database/access-auth.md`. |
| DB-U10 Principal persistence | RESOLVED WITHOUT PERSISTENCE | Runtime-derived Principal; no Principal table selected. |
| Frontend fake authoritative success | FORBIDDEN | Server state owns auth/verification/recovery/link/session success. |
| M1 | CLOSED | Accepted Web baseline; integration checks deferred. |
| M2 | CLOSED / QA PASS | M2.1–M2.11 accepted/documented; no runtime proof claimed. |
| M3 | ACTIVE | M3-A DB foundation materialized + direct PostgreSQL 18.6 proof PASS; Auth runtime not yet built. |
| Browser topology | FIXED | Same-origin `/api/v1/*` through edge; services may be physically independent. |
| Browser session | FIXED | Opaque DB-backed server-authoritative session + host-only HttpOnly cookie. |
| JWT/localStorage browser auth | NOT SELECTED | Requires concrete reopen evidence. |
| CSRF/CORS | FIXED | Synchronizer + Origin + Fetch Metadata; normal browser CORS off. |
| Session lifetime | FIXED POLICY | 30d overall + 30d inactive; background polling not activity. |
| Multiple sessions | FIXED | Independent AuthSessions per client. |
| Current logout | FIXED | Conditional idempotent current-session revoke. |
| Revoke all others / everywhere | FIXED | Separate intents protected by policy/recent auth. |
| Account security root | FIXED | Not Person/profile/email/password/global role/device. |
| Password optional | FIXED | Provider/passkey/passwordless Account valid. |
| Provider identity | FIXED | issuer + subject. |
| Silent provider-email merge | NOT SELECTED | Proof + explicit consent + transactional link. |
| Password policy | FIXED | 15 min; 1024/4096 max resource bounds; NFC; no composition; no truncation. |
| Password storage | FIXED | Argon2id v19 64MiB/t3/p4 + HMAC-SHA256 pepper. |
| Breach screening | FIXED | HIBP range; establish fail-closed; existing-login outage fail-open telemetry. |
| KDF concurrency | FIXED PRINCIPLE | Bounded; exact capacity benchmarked at implementation/deployment. |
| Passkey-ready | FIXED | 0..N; passwordless; UV required; discoverable direction; opaque userHandle. |
| Consumer attestation | NOT SELECTED | Future high-security policy may reopen. |
| MFA implementation | DEFERRED | Architecture compatible; no `mfa_enabled` god-flag. |
| Email comparison | FIXED | NFC+casefold local; IDNA ASCII lowercase domain; separate display/delivery. |
| Gmail dot/+ canonicalization | NOT SELECTED | Provider-specific alias behavior not canonical identity. |
| Verified recovery/contact email | FIXED PRODUCT INVARIANT | Standard consumer Account retains one verified EmailIdentity. |
| API namespace | FIXED | `/api/v1`; compatibility generation. |
| API problem format | FIXED | RFC9457 + code/category/request_id/retryable/errors. |
| Machine codes | FIXED | `namespace.snake_case`; human text never parsed. |
| Transaction isolation | FIXED | READ COMMITTED default; targeted locks. |
| Account security serialization | FIXED | Account row for account-wide mutation. |
| Account lock every request | NOT SELECTED | Session admission is read path. |
| Advisory Account lock | NOT SELECTED | Canonical row lock exists. |
| Ambiguous commit blind retry | FORBIDDEN | Reconcile or fail safely. |
| Signin persistent generic idempotency | NOT SELECTED | Raw session secret intentionally not retained. |
| OpenAPI source | FIXED | FastAPI/Pydantic declaration → generated committed snapshot. |
| Generated client | FIXED | Orval Fetch → framework-neutral `@dante/api-client`. |
| Axios for generated client | NOT SELECTED | No need. |
| Generated React Query hooks | NOT SELECTED | Query/application policy remains separate. |
| Runtime API validation | FIXED | Zod at generated/normalization boundary. |
| TanStack Query | ACTIVATE M3 | Remote request/cache lifecycle only. |
| Auth query-cache persistence | NOT SELECTED | No browser storage auth cache. |
| Full-stack proof | FIXED | Real PG/FastAPI/same-origin HTTPS/browser. |
| Critical browser engines | FIXED M3 PROOF | Chromium + Firefox + WebKit. |
| Auth E2E shared storageState | NOT SELECTED | Critical Auth spine traverses real signin. |
| Exact remaining Auth SQL beyond M3-A | OPEN BY SLICE | Later slices materialize only justified shape. |
| Exact KDF worker/DB timeout numbers | OPEN OPERATIONAL | Benchmark/configure in implementation without semantic reopen. |
| Native credential transport | DEFERRED TO M6 | Same canonical AuthSession semantics. |
| Full Home implementation | DEFERRED | Separate product vertical. |

---

## 17. M1 closure record — 2026-08-27

M1 closed after live review of the existing Web Access surface and code/contracts.

Accepted:

- visual composition coherent; no novelty redesign;
- geometry/design tokens remain systematic;
- Web Access surface inventory sufficient to proceed;
- mobile is not scaled desktop;
- provider buttons before real integration are not final provider-compliance authority;
- Terms/Privacy and real-backend visual QA remain later closure obligations.

M1 closure did not claim full integrated Auth UX.

---

## 18. M2 documentation checkpoints and closure — 2026-08-27

### First checkpoint

M2.1–M2.8 were moved from chat-only state into:

```text
access-auth-architecture.md
access-auth-security-contract.md
access-auth-api-contract.md
ADR-011
```

### Final closure checkpoint

M2.9–M2.11 were reconciled into those authorities and:

```text
docs/architecture/access-auth-testing-contract.md
```

Navigation was reconciled in `docs/architecture/README.md` and `docs/README.md`.

Post-write audit against closure PRE-SCOPE `1d685dc43dd68916afa34ec84b7f45df20c890b0` observed:

```text
branch relation        ahead
changed paths           exactly approved documentation paths
production code paths   0
DB/migration paths      0
runtime/CI paths        0
```

Readback directly confirmed current M2-closed status in architecture/security/API/testing/workstream authorities and no remaining M2.9/M2.10/M2.11 OPEN state in those current owners.

Closure result:

```text
M2.1–M2.11 accepted
subject-oriented durable documentation complete
whole-M2 documentation/readback/path QA PASS
production runtime implementation none
```

M2 closure means architecture/security/API/testing readiness, not executable Auth PASS.

---

## 19. M3-A database foundation checkpoint — 2026-08-27

Approved production gate PRE-SCOPE:

```text
ea75bb33e88bd256018c73ae444cff48a510af63
```

Source materialized so far:

```text
Alembic 20260827_09
SQLAlchemy Auth mappings
MAPPED_TABLES current registry
Database Dictionary v1 post-CP6 evolution
4 Auth table entries
current catalog/migration/ACL test source
docs/database/access-auth.md
Database System-of-Record reconciliation
```

The Database Dictionary now separates:

```text
expected_baseline
→ CP6 68/5/14 + 75/95 + 68/120 benchmark

current_materialization
→ M3-A branch candidate 72/5/14 + 75/104 + 71/137
```

Current evidence boundary:

```text
source/schema/docs materialized      YES
remote path audit against PRE-SCOPE  PASS for the DB-foundation write set
local real PostgreSQL 18.6 execution PASS
Ruff format/check                    PASS
mypy                                 PASS / 42 source files
targeted DB integration suite        PASS / 7 of 7
M3-A database foundation             MATERIALIZED + PROVEN
Auth runtime                         NOT YET
whole M3-A / M3 exit gate            NOT YET
```

During `scope.json` reconciliation, one update attempt used a stale/incorrect blob SHA and GitHub returned `409`; no change was applied by that rejected attempt. The file was re-read and the subsequent exact-SHA update succeeded. This did not move any unrelated path or ref.

Documentation-model hardening discovered during the same slice:

```text
whole DB reference != frozen CP6 artifact
current/evolving reference must track later accepted DB truth
CP6 migration/QA/Git evidence remains historical
resolved DB deferrals must be reconciled when their trigger fires
```

That rule is now normative in `docs/development/documentation-lifecycle-policy.md` and applied to the Database System of Record.

---

## 20. Current known operational incidents

### Historical accidental branch

During initial workstream bootstrap, an accidental remote branch `__noop_should_not_create__` was created at an old baseline. It did not modify `main` or `feature/access-auth`. Deletion was previously requested manually; cleanup remains unconfirmed in this record.

### Historical no-op ref update

During the 2026-08-27 roadmap documentation gate, a ref-update action was accidentally invoked targeting the already-current `feature/access-auth` SHA. Readback confirmed no movement/commit/history change.

### M2 closure gate duplicate create-branch attempts

During the 2026-08-27 M2 closure documentation gate, the branch-create action was accidentally invoked twice with:

```text
branch_name = feature/access-auth
base_ref    = feature/access-auth
```

GitHub rejected both attempts with:

```text
422 Reference already exists
```

Observed effect:

```text
new branch created     NO
existing ref moved     NO
commit created         NO
history changed        NO
```

The mistake was disclosed immediately during execution. File tooling was then explicitly reloaded before continuing. Do not repeat this pattern.

---

## 21. Git/write safety

Every repository write follows:

```text
fresh remote HEAD
→ exact WRITE GATE
→ exact CREATE / UPDATE / DELETE paths
→ purpose + explicit exclusions
→ explicit user authorization
→ re-fetch HEAD immediately before first scoped write
→ write only approved files
→ readback
→ compare/path audit
→ QA verdict
```

If HEAD changes from approved PRE-SCOPE before first actual scoped write: STOP / re-gate.

Separate explicit gate required for:

```text
force push
rebase
destructive reset
history rewrite
merge to main
extra branch/worktree
incidental cleanup
destructive/out-of-scope action
```

New chat != new branch.

---

## 22. Macro-phase closure protocol

A macro-phase is not CLOSED merely because discussion/code appears complete.

Closure updates as applicable:

```text
roadmap phase status
+ decisions
+ decision register
+ durable subsystem docs/ADRs
+ QA/evidence actually proved
+ deferred/open items + reopen triggers
+ branch/head handoff state
+ next safe phase/action
```

Minimum closure record answers:

1. What was decided?
2. What was implemented?
3. What was directly proved?
4. What remains deferred/open?
5. What would reopen the phase?
6. What is the next safe action?

No closed phase may depend on chat memory for durable truth.

---

## 23. Immediate next action

Current phase:

```text
M3 — Email/Password Signin + AuthSession Spine
ACTIVE

M3-A DB FOUNDATION
MATERIALIZED + DIRECTLY PROVEN

AUTH RUNTIME / API / CLIENT / WEB SPINE
NOT YET
```

Immediate next safe action:

1. continue the same approved M3-A vertical into email/password runtime and bounded password/KDF execution;
2. materialize real FastAPI signin/session/logout plus runtime Principal derivation and server-authoritative AuthSession admission;
3. generate/verify deterministic OpenAPI → Orval `@dante/api-client` and Web transport/application boundary;
4. wire Access signin/bootstrap/logout into the production-shaped `AuthenticatedAppShell` without creating a fake Home;
5. earn real API + same-origin HTTPS Chromium/Firefox/WebKit proof before claiming whole M3-A/M3 PASS.

Do **not** start a second unrelated Auth migration or fake Home. The M3-A goal remains one bounded end-to-end spine that moves required DB/backend/API/generated-client/Web/test/docs artifacts together and earns real PostgreSQL + browser proof.