# DANTE — Access/Auth Full-Stack Vertical Workstream

- **Status:** ACTIVE / BRANCH-LOCAL DURABLE WORKSTREAM RECORD
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Created from protected `main`:** `f011e252b6a294a12c38927ef2d528244ea1fee6`
- **M2.1–M2.8 documentation checkpoint PRE-SCOPE:** `e969b47ca9c57c5ffa34fb3eeb0145f40ea7efba`
- **Current macro-phase:** `M2 — Auth Architecture Freeze`
- **Last closed macro-phase:** `M1 — Access Visual / UX Freeze`
- **First production-code target after M2:** `M3 — Email/Password Signin + AuthSession Spine`
- **Purpose:** operational save-game, authority map, decision register, gated roadmap and quality bar for the production Access/Auth vertical.

> This file is the current branch-local continuation authority while `feature/access-auth` is active. It records current workstream state and gates; durable accepted architecture/security/API truth belongs in the subject-oriented current docs referenced below. Do not turn this file into a chronological chat diary or the sole Auth specification.

---

## 1. Mandatory new-session bootstrap

A new chat, agent or context window does **not** create a new project, branch or worktree.

Continue the same real workstream:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

The separate worktree `/home/mattia/projects/dante-frontend` may host independent frontend work such as Home, but Access/Auth frontend changes required by this vertical stay on `feature/access-auth`.

At the beginning of every new session:

1. read root `README.md`;
2. read `docs/README.md`;
3. read `docs/PROJECT-STATUS.md`;
4. read `docs/ROADMAP.md`;
5. read `docs/development/agent-operating-manual.md`;
6. read current development safety/branching/documentation-lifecycle rules;
7. read this file completely;
8. read `docs/frontend/access.md`;
9. read current Access/Auth durable authorities:
   - `docs/architecture/access-auth-architecture.md`;
   - `docs/architecture/access-auth-security-contract.md`;
   - `docs/architecture/access-auth-api-contract.md`;
   - `docs/decisions/ADR-011-access-auth-architecture.md`;
10. inspect current backend/database/frontend authorities relevant to the active macro-phase;
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

Use the strictest current applicable source:

```text
protected-main implementation / migrations / tests
+ accepted Domain / Logical / Physical / architecture decisions
↓
current durable subsystem/product/database docs
↓
current branch-local Access/Auth architecture/security/API contracts + ADR-011
↓
this active branch-local workstream record for operational state/newer unresolved decisions
↓
current feature/access-auth implementation
↓
historical CP6 / Access-frontend evidence
↓
conversation memory
```

Important current sources include, as applicable:

- `docs/frontend/access.md`;
- `docs/architecture/access-auth-architecture.md`;
- `docs/architecture/access-auth-security-contract.md`;
- `docs/architecture/access-auth-api-contract.md`;
- `docs/decisions/ADR-011-access-auth-architecture.md`;
- frontend production-readiness contracts/gates;
- `docs/database/README.md` and Database Dictionary/reference artifacts;
- ADR-007 and ADR-010 / PostgreSQL persistence constitution;
- CP6 PostgreSQL closure/QA material where persistence invariants matter;
- current backend bootstrap/mappings/migrations/tests;
- current Access state machine/UI/release tests.

Historical records are evidence, never newer authority.

---

## 3. Foundations already closed before this vertical

### Domain / Logical / Physical

The core model and physical target are accepted foundations. Preserve:

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
- provisioning/runtime roles and ACL work;
- persistence mappings;
- whole-database materialization;
- PostgreSQL acceptance/integrity/runtime tests;
- backend CI.

CP6 deliberately did not invent speculative Account/Principal/Auth persistence. Access/Auth is the vertical allowed to justify those concepts.

### Frontend foundation

Already integrated:

- Web Access shell and accepted visual direction;
- desktop/tablet/mobile-Web responsive behavior;
- IT/EN;
- Access state graph;
- signup/recovery/provider/linking/reauth/setup surfaces;
- local validation;
- accessibility/reduced-motion treatment;
- Playwright release matrix;
- frontend CI;
- explicit refusal to fake backend-authoritative success.

The existing Web Access implementation is production UI/state foundation, not disposable mock code.

### Mobile foundation

Already materialized in `apps/mobile`:

```text
Expo 57
React Native 0.86.x
Expo Router
React 19.2.x
```

Native Mobile Access is not implemented yet, but the technology choice and mobile runtime foundation already exist. Mobile design authority remains the previously accepted mobile Access direction; Mobile Access is a later macro-phase in this same vertical.

---

## 4. Current implementation reality

### Backend

No dedicated production Access/Auth capability, account/session implementation or real Auth API has been completed yet.

### Database

No production Account / EmailIdentity / PasswordCredential / ExternalIdentity / PasskeyCredential / AuthSession schema has been materialized yet. This is deliberate vertical deferral, not a CP6 defect.

### Web frontend

The accepted Access UI/state model exists, but real backend/session wiring, generated client integration and authenticated Home handoff do not.

### Mobile

Foundation/runtime exists; Native Mobile Access does not.

### Contract generation

No production Auth OpenAPI → generated TypeScript client path is complete yet.

### M2 architecture documentation

M2.1–M2.8 accepted decisions are now durably materialized by subject in:

```text
docs/architecture/access-auth-architecture.md
docs/architecture/access-auth-security-contract.md
docs/architecture/access-auth-api-contract.md
docs/decisions/ADR-011-access-auth-architecture.md
```

These documents state current accepted architecture directly and include diagrams, consequences, rejected shortcuts and reopen discipline. This workstream no longer needs to duplicate their full normative payload.

---

## 5. Product/security semantic constitution

These distinctions are mandatory unless explicitly reopened by stronger evidence:

```text
Person != Account
Account != Principal
Principal != Actor
AuthSession != DANTE Session
signin != provider-data integration authorization
provider state != DANTE canonical state
verification != profile/setup completion
reauthentication != initial signin
client/device signal != identity
frontend request/success != backend-authoritative success
```

Current accepted architecture additionally fixes:

```text
Account = durable Access/security root
EmailIdentity != Account
PasswordCredential is optional
Account may be passwordless
ExternalIdentity key = issuer + subject
provider email never silently links Accounts
Account may have 0..N PasskeyCredential
Principal remains runtime-only absent stronger evidence
AuthSession belongs to Account, not to one authenticator
method != factor != assurance
passkey != MFA by definition
```

Detailed authority: `docs/architecture/access-auth-architecture.md`.

---

## 6. Vertical boundary

### In scope

When justified by the roadmap, this vertical owns:

- Account lifecycle/status;
- EmailIdentity;
- PasswordCredential;
- email/password signin;
- email signup and verification;
- recovery/reset;
- reauthentication/recent-auth;
- backend-authoritative AuthSession lifecycle;
- concurrent multi-device/multi-session use;
- logout, individual revocation, revoke-all-others and logout-everywhere capability;
- Google authentication;
- Apple authentication;
- ExternalIdentity mapping;
- passkeys / WebAuthn capability;
- provider/account collision handling and explicit linking;
- Auth API/OpenAPI/generated client;
- Web Access real wiring;
- Native Mobile Access real wiring;
- required DB migrations/mappings/Dictionary/reference;
- security, rate-limit, replay, race/concurrency behavior;
- full-stack QA and authenticated handoff into the next product vertical.

### Deferred but architecture-aware

- optional MFA enrollment;
- TOTP/authenticator-app support;
- recovery codes;
- step-up MFA for selected sensitive operations;
- policy-driven mandatory MFA for future roles/accounts if later justified.

MFA is intentionally **not** part of the first Access/Auth release scope, but current data/session/authenticator modeling must not make a future MFA implementation awkward or require semantic rewrites.

### Explicitly out of scope unless separately gated

- full Home/Today implementation;
- unrelated frontend pages/polish;
- Gmail/Calendar provider-data integrations;
- generic platform-wide RBAC redesign;
- rewriting accepted CP1–CP6 foundations for style;
- extra branches/worktrees;
- direct work on `main`;
- merge/rebase/history rewrite without explicit gate.

A minimal protected destination may be used only to prove authenticated handoff.

---

## 7. Mandatory engineering method

Implement by vertical slice, not backend-first batching and not fake frontend success:

```text
product need/state
→ contract
→ domain/application behavior
→ persistence/security
→ endpoint
→ OpenAPI
→ generated client
→ Web/Mobile application boundary as applicable
→ real UI transition
→ tests
→ real full-stack proof
→ QA
→ documentation closure
```

Do not create generic `BaseService`, `GenericRepository`, giant `AuthManager`, speculative UoW wrappers or other convenience abstraction without concrete need.

Application transaction boundaries remain explicit; adapters may flush but do not own hidden commits.

---

## 8. Database and transaction constitution

PostgreSQL remains canonical DANTE persistence authority.

### Slice-driven schema

Do not create a speculative mega-migration. Concepts appear only when a slice justifies exact semantics.

Likely concepts include:

- Account;
- EmailIdentity;
- PasswordCredential;
- AuthSession;
- verification/recovery proof/challenge state;
- ExternalIdentity;
- PasskeyCredential or equivalent WebAuthn credential state;
- linking/collision transaction state only if the protocol requires durable state.

These are conceptual names, not pre-approved SQL table names.

### Same-change database system-of-record rule

A structural DB change is incomplete unless all applicable artifacts move together:

```text
semantic design
Alembic migration
SQLAlchemy mapping/metadata
mapping registry where applicable
Database Dictionary
human-readable DB reference
constraints
justified indexes
least-privilege ACL
unit/direct tests
catalog/schema parity
real PostgreSQL proof
concurrency/negative tests where relevant
```

### Forward-only

Normal migration history is forward-only. Do not rewrite integrated history for convenience.

### Constraints arbitrate races

Application pre-checks improve UX but never replace canonical DB uniqueness/integrity constraints.

### Transactions

Operations that must succeed/fail together require explicit transaction boundaries. Examples include:

- password reset + credential replacement + required session revocation;
- provider/account linking + uniqueness state;
- single-use proof consume + authoritative state transition.

Do not hold long DB transactions across external network waits.

Carry-forward contract:

```text
one AsyncSession per application operation/task
autobegin=False
outer application operation owns transaction
adapters may flush, not hidden-commit
READ COMMITTED default
locking/stronger isolation only for concrete invariant
no blind retry of ambiguous/non-idempotent security mutations
```

M2.9 closes the exact M3 transaction/concurrency/session-expiry behavior without inventing a second persistence philosophy.

---

## 9. Accepted M2.1–M2.8 security/transport checkpoint

Detailed authority: `docs/architecture/access-auth-security-contract.md`.

Current accepted posture includes:

```text
NORMAL WEB BOUNDARY
same-origin browser API via edge/ingress
/api/v1/* browser path
CORS disabled/no ACAO by default
trusted forwarded headers only from trusted edge

WEB SESSION
opaque 256-bit CSPRNG secret
raw secret never persisted
SHA-256 indexed server verifier
__Host-dante-session
Secure + HttpOnly + Path=/ + SameSite=Lax
Domain absent
browser storage auth token forbidden
30-day default maximum/inactive-session policy
background polling does not reset user inactivity

CSRF
synchronizer token bound to AuthSession
exact Origin validation
Fetch Metadata validation
no state-changing GET
pre-auth login protected by same-origin JSON/request contract

MULTI-SESSION
independent session per client
current logout
specific remote revoke
revoke all others
log out everywhere
account disable revokes all
old sessions never resurrect

PASSWORD
minimum 15 Unicode code points
NFC
no composition rules
paste/password-manager first-class
Argon2id explicit 64 MiB / t=3 / p=4 policy
HMAC-SHA-256 server pepper before Argon2id
HIBP k-anonymity breach screening
bounded KDF concurrency
rehash-on-auth with authoritative race recheck

RECOVERY / CHANGE
recovery reset revokes all sessions + fresh sign-in
normal authenticated password change revokes other sessions and rotates current secret
email change uses pending/verified atomic transition and revokes other sessions

PASSKEY READY
0..N per Account
passwordless Account valid
userVerification required direction
discoverable credential direction
random opaque 32-byte non-PII userHandle
narrow stable RP ID security principle
synced/device-bound supported
consumer mandatory attestation not selected
signature counter anomaly = risk signal, not automatic lockout

MFA
implementation deferred
assurance/evidence-aware architecture required
mfa_enabled Boolean not accepted as complete model
```

---

## 10. Verification, recovery and proof rules

Proof/challenge flows must explicitly define:

- strong generation;
- verifier/digest storage where possible;
- expiry;
- single-use semantics;
- replay resistance;
- consume-only-if-valid-and-unused behavior;
- resend/replace behavior;
- concurrent consume races;
- anti-enumeration where account existence must not leak;
- delivery-port abstraction;
- failure/retry behavior that does not duplicate authoritative transitions.

Recovery/reset effects on existing sessions are now fixed by the security contract: successful account recovery/password reset revokes all pre-existing AuthSessions and requires normal fresh sign-in.

---

## 11. Concurrency, replay and idempotency

Treat these as normal requirements:

- concurrent signup for same canonical email;
- concurrent proof consumption;
- reset racing with signin/session use;
- repeated logout/revoke;
- provider callback replay/duplication;
- unique provider `(issuer, subject)` identity;
- concurrent linking attempts;
- unsafe mutation retry;
- partial external activity + DB rollback;
- session create/revoke races;
- passkey registration/authentication replay/counter/credential uniqueness behavior according to WebAuthn semantics.

Do not blindly retry non-idempotent security mutations.

Account is the current natural serialization point for account-wide security mutations when M3/M4 requires row locking; M2.9 must convert that principle into the exact first-slice behavior and proof obligations.

---

## 12. API and naming contract — M2.8 ACCEPTED

Detailed authority: `docs/architecture/access-auth-api-contract.md`.

Current accepted contract:

```text
base product namespace           /api/v1
version meaning                  major compatibility generation
health endpoints                 outside product versioning
API shape                        application intents, not Auth-table CRUD
success envelope                 no universal wrapper
problem standard                 RFC 9457 application/problem+json
machine code                     stable namespace.snake_case
category                         stable broad fallback
request_id                       server-authoritative on every request
validation                       bounded stable errors[], no Pydantic internals
anti-enumeration                 explicit end-to-end behavior
Retry-After                      standard header where applicable
retryable                        never implies blind mutation auto-retry
OpenAPI operationId              explicit/stable/unique
human detail/title               never parsed as machine logic
```

Naming is layer-appropriate but semantically aligned:

```text
HTTP paths                stable lowercase intent/resource naming
OpenAPI operationId       namespaced snake_case
JSON/RFC9457 extensions   snake_case
machine error code        namespace.snake_case
Python                    repository Python convention
TypeScript                generated-client idiom, not handwritten duplicate contract
PostgreSQL                DANTE DB naming constitution
```

M2.10 owns generator/tooling/file-ownership details without reopening these API semantics.

---

## 13. Web and Mobile integration boundary

### Web target layering

```text
Access presentation/state machine
→ Access application boundary
→ session + remote mutations/state
→ data-source port
→ generated DANTE API client
```

Global session/bootstrap lifecycle is separate from one form reducer lifecycle.

Preserve:

```text
REQUEST_* = user intent
SERVER_*  = authoritative backend result
```

### Native Mobile target layering

Mobile consumes the same canonical backend/application semantics but uses native-safe credential/session transport and storage.

```text
Account / AuthSession / Principal semantics
                ↓
        application Auth contract
             /        \
        Web transport  Native transport
        secure cookie  secure native storage/credential path
```

Do not make browser cookies part of the domain/application contract.

---

## 14. Testing constitution

Use the strongest practical proof at each layer.

### Unit/domain/application

Deterministic business/security rules without transport noise.

### PostgreSQL integration

Real PostgreSQL for constraints, transactions, mappings, migrations and race-sensitive behavior.

### API integration

Real FastAPI/HTTP/cookie/header behavior against canonical DB state.

### Generated client

OpenAPI/client drift must be detectable. Generated source is not hand-maintained substitute truth.

### Web full-stack E2E

Ultimately prove:

```text
real browser
→ real frontend
→ application/generated-client boundary
→ real FastAPI HTTP
→ real Web session transport
→ real PostgreSQL
```

### Native runtime/E2E

When M6 is active, prove the real mobile client against the same backend semantics and a production-representative native runtime/device/emulator path.

### External providers/mail

Protocol-faithful deterministic adapters may be used in CI where direct third-party dependency would be unreliable, but DANTE's internal path may not be faked.

### Regression obligations

Preserve:

- accessibility/WCAG 2.2 AA-quality behavior;
- keyboard/focus;
- responsive release matrix;
- IT/EN;
- reduced motion;
- password manager/autofill behavior;
- offline/degraded-state correctness;
- no fake backend-authoritative success.

M2.11 will turn these principles into the exact M3 test/harness matrix.

---

## 15. Definition of Done for any executable slice

A slice is CLOSED only when all applicable items pass:

```text
[ ] product states/intents explicit
[ ] semantic invariants preserved
[ ] architecture decisions ratified
[ ] persistence justified/minimal
[ ] migration/mapping/Dictionary/reference aligned
[ ] security/threat cases handled
[ ] transaction boundaries explicit
[ ] concurrency/replay/idempotency considered and tested
[ ] HTTP/API contract stable
[ ] machine error semantics stable
[ ] OpenAPI reflects implementation
[ ] generated client updated from contract
[ ] Web/Mobile consumes through intended boundary
[ ] frontend never invents authoritative success
[ ] unit tests PASS
[ ] PostgreSQL integration tests PASS
[ ] API integration tests PASS
[ ] full-stack E2E/runtime proof PASS
[ ] accessibility/responsive/i18n regression PASS
[ ] no secrets leaked in logs/docs/tests
[ ] documentation/current workstream record updated
[ ] exact write-scope QA PASS
```

“Happy path works” is not a closure criterion.

---

# 16. Definitive roadmap — 7 macro-phases

This section supersedes the earlier R0–R7 breakdown. The intent is fewer, clearer macro-phases with detailed internal gates, not a 200-step task list.

## M1 — Access Visual / UX Freeze

**Status:** `CLOSED / PASS WITH DEFERRED INTEGRATION CHECKS`

### Goal

Confirm that the accepted Web Access experience has a coherent product-grade visual system and sufficient surface/state coverage before backend integration.

### Closed decisions

- current visual direction is accepted; no redesign-from-zero;
- desktop composition, responsive strategy and interaction language are locked as the baseline;
- Web Access is a production UI/state foundation, not disposable mock UI;
- geometry must remain systematic rather than ad-hoc: content bounds, panel widths, spacing scale, control heights, radii hierarchy, typography and breakpoints must stay governed by semantic/design-system rules when touched;
- mobile is not a scaled desktop; previously accepted Mobile Access design authority remains separate;
- backend-authoritative transitions remain impossible to fake locally;
- Google/Apple production integration must use current official provider mechanisms/assets/guidelines rather than assuming the current pre-backend custom marks/buttons are final provider compliance;
- final Terms/Privacy destinations are required before vertical closure;
- final backend-state visual QA happens after real integration, not by inventing fake success now.

### Deferred integration checks

- real loading/pending/error/rate-limit/server-unavailable states;
- password manager/autofill with real backend flow;
- provider official rendering/integration behavior;
- final Terms/Privacy links/content destination;
- final cross-browser/responsive/accessibility review after backend wiring.

### Exit evidence

Manual review of the current Web Access baseline plus current code/contracts found no architectural need for a visual redesign. Remaining items are integration/closure obligations, not blockers to M2.

---

## M2 — Auth Architecture Freeze

**Status:** `ACTIVE / M2.1–M2.8 ACCEPTED AND DURABLY DOCUMENTED`

### Goal

Ratify the security/application/persistence/API contract needed to build the first executable Auth slice without speculative schema or transport choices.

### Decision sequence / current state

```text
1. deployment origin topology                                  ACCEPTED
2. browser session / cookie / CSRF / CORS model               ACCEPTED
3. Account / EmailIdentity / PasswordCredential /
   AuthSession / Principal semantics                           ACCEPTED
4. multi-session lifecycle and revoke/logout policy            ACCEPTED
5. password hashing + breach-policy implementation             ACCEPTED
6. passkey-ready authenticator + MFA compatibility boundary    ACCEPTED
7. email normalization/comparison model                        ACCEPTED
8. API namespace + machine error/naming contract               ACCEPTED
9. M3 transaction/concurrency/session-expiry behavior           OPEN / NEXT
10. OpenAPI → generated client → Web application boundary      OPEN
11. M3 test matrix / full-stack harness                         OPEN
12. documentation reconciliation + first production-code gate  PENDING
```

### Durable M2.1–M2.8 owners

```text
docs/architecture/access-auth-architecture.md
docs/architecture/access-auth-security-contract.md
docs/architecture/access-auth-api-contract.md
docs/decisions/ADR-011-access-auth-architecture.md
```

### Explicitly not done in M2

- no production Auth tables merely to “get started”;
- no Auth endpoints;
- no generated Auth client;
- no real provider integration;
- no Mobile Access implementation.

### Exit gate

No unresolved decision remains that would force speculative M3 account/password/session code or require foreseeable semantic rewrites. Durable docs state current truth directly, M3 test/contract boundaries are explicit, and a separate exact production-code write gate is approved.

### Immediate next action

Close M2.9: exact first-slice transaction/concurrency/session-expiry behavior.

---

## M3 — Email/Password Signin + AuthSession Spine

**Status:** `NOT STARTED`

### Goal

Create the first real production full-stack authenticated path and the reusable Account/AuthSession spine.

### Required scope

- slice-justified Account/EmailIdentity/PasswordCredential/AuthSession persistence;
- exact DB constraints/indexes/ACL/mappings/Dictionary/reference;
- password verification and rehash-on-auth policy where applicable;
- authoritative AuthSession creation;
- secure Web transport;
- session bootstrap after reload;
- runtime Principal derivation;
- minimal protected authenticated boundary;
- current-session logout/revocation;
- capability for multiple concurrent AuthSessions on one Account;
- stable Auth API/OpenAPI;
- generated TypeScript client;
- Web Access signin wiring through application/data-source boundary;
- real PostgreSQL + FastAPI + Firefox/browser E2E.

### Negative/security scope

- bad password;
- unknown account with anti-enumeration-safe semantics;
- disabled/restricted account state as ratified;
- expired/revoked session;
- duplicate/replayed logout/revoke behavior;
- session-create failure/rollback;
- concurrent session creation/use;
- reload/bootstrap with valid/invalid session;
- server-unavailable/rate-limited UI semantics as applicable.

### Exit gate

A real browser signs in against real FastAPI/PostgreSQL, receives a real authoritative session, survives reload, reaches the protected boundary, and logs out so access is removed. Multiple allowed sessions do not overwrite each other.

---

## M4 — Account Lifecycle: Signup, Verification, Recovery, Reset, Reauth

**Status:** `NOT STARTED`

### Goal

Complete the first-party account lifecycle around the M3 session spine.

### Scope

#### Signup + verification

- Account/email/password creation semantics;
- email uniqueness/race handling;
- verification challenge/proof lifecycle;
- delivery port;
- resend/replace semantics;
- expiry/single-use/replay;
- verification consume;
- setup/session transition according to ratified semantics.

#### Recovery/reset

- neutral account-existence response;
- recovery proof lifecycle;
- expiry/single-use/replay;
- password replacement;
- required session revocation according to security policy;
- atomicity for credential/session changes;
- reset completion and next-signin semantics.

#### Reauthentication / recent-auth

- distinguish valid session from fresh proof;
- server-side freshness/assurance policy;
- sensitive-operation guard;
- expiry/negative cases;
- no accidental second signin/session model.

### Exit gate

A real user can create, verify, recover/reset and reauthenticate through authoritative backend state, including race/replay/negative cases, without account enumeration or unsafe session leftovers.

---

## M5 — Federated Auth + Passkeys + Explicit Linking

**Status:** `NOT STARTED`

### Goal

Add modern non-password authentication while preserving DANTE canonical identity/session authority.

### Google + Apple

- current official provider integration mechanism/assets;
- provider-specific protocol adapter;
- state/nonce/PKCE where applicable;
- callback/assertion validation;
- issuer/audience/signature/subject checks;
- known/new/collision outcomes;
- AuthSession creation through canonical DANTE application behavior;
- replay/error/cancellation handling;
- no provider-data integration token leakage into Auth semantics.

### Collision/linking

```text
provider/account collision
→ prove control of existing DANTE account
→ explicit user link decision
→ backend-authoritative transactional link
```

Requirements:

- never silently merge by email coincidence;
- uniqueness constraints arbitrate races;
- replay/concurrent link attempts are safe;
- cancellation/recovery path exists;
- unlink rules prevent accidental loss of all valid authenticators.

### Passkeys

Implement production passkey/WebAuthn registration and authentication with current standards/provider/browser/platform behavior while preserving the M2 accepted WebAuthn security boundary.

Must cover at least:

- credential registration challenge;
- origin/RP/credential validation;
- credential uniqueness;
- authenticator metadata/state required by the selected implementation;
- authentication challenge;
- replay protection;
- add/remove credential lifecycle;
- account recovery interaction;
- reauth/recent-auth semantics where relevant;
- Web and later Mobile compatibility.

### MFA

Still deferred unless an explicit new gate promotes it.

### Exit gate

Google, Apple and passkeys authenticate/link through DANTE canonical Account/AuthSession semantics, with no email-coincidence account takeover and no provider-specific shortcut that bypasses the core application model.

---

## M6 — Native Mobile Access

**Status:** `NOT STARTED`

### Goal

Materialize Native Mobile Access on the existing Expo/React Native/Expo Router foundation against the already-stable canonical Auth backend.

### Scope

- native Access UI from accepted mobile design authority;
- signin/signup/recovery/reauth/provider/passkey flows as supported by the platform and current M3–M5 contracts;
- native-safe session/credential transport and secure storage;
- app bootstrap/restart authenticated-state reconstruction;
- concurrent Web + Mobile sessions;
- logout/current-session revocation;
- logout-all/revocation reaction;
- deep-link/provider callback handling where required;
- lifecycle/background/foreground behavior;
- native accessibility/i18n;
- real emulator/device runtime proof against real backend/PostgreSQL.

### Fixed rule

Mobile does not get a separate Auth domain model or convenience backend. It consumes the same Account/AuthSession/Principal semantics with client-appropriate transport.

### Exit gate

A real Native Mobile client can authenticate, restart, coexist with Web sessions, revoke/logout correctly and follow the same canonical security/account rules as Web.

---

## M7 — Security Hardening + Authenticated Home Handoff + Closure

**Status:** `NOT STARTED`

### Goal

Prove the entire Access/Auth vertical is production-ready and hand off cleanly into the next product vertical.

### Hardening scope

- threat-model review;
- session expiry/rotation/revocation review;
- active-session/device-management readiness;
- credential stuffing/brute-force/rate-limit controls;
- abuse/degraded-service behavior;
- provider/mail failure behavior;
- security-event/audit observability as justified;
- password reset/account disable/recovery revocation rules;
- concurrency/race/replay suite;
- restart/bootstrap behavior;
- secret/log/telemetry review;
- OpenAPI/generated-client drift check;
- PostgreSQL schema/catalog/ACL/mapping/Dictionary parity;
- Web accessibility/responsive/i18n/autofill/password-manager regression;
- Native runtime/accessibility/i18n regression;
- hosted CI;
- final Terms/Privacy destinations;
- minimal real authenticated Home/next-route handoff without implementing full Home.

### Closure documentation

Before declaring Access/Auth closed:

- propagate durable architecture/security/product truth to current subsystem docs/ADRs;
- update this workstream record with final status/evidence;
- remove/consolidate temporary branch-only continuation material according to documentation lifecycle policy;
- retain only useful branch history/evidence;
- verify no newer truth exists only in chat memory.

### Exit gate

The whole Access/Auth vertical is production-ready across backend/PostgreSQL/Web/Native, CI is green, documentation is consolidated, and merge to protected `main` happens only after explicit user gate.

---

## 17. Decision register

Use labels strictly:

- **FIXED:** accepted invariant/current authority; do not reopen casually.
- **RECOMMENDED:** strong current direction; must be ratified before security/contract-sensitive implementation.
- **OPEN:** unresolved; must not be guessed in code.
- **DEFERRED:** intentionally postponed with a reopen trigger.
- **NOT SELECTED / NOT JUSTIFIED:** explicitly rejected or unsupported at current evidence level.

| Topic | State | Current position / reopen trigger |
|---|---|---|
| Person != Account | FIXED | Preserve Domain/security boundary. |
| Account != Principal | FIXED | Principal is runtime security context unless durable need is proved. |
| Principal != Actor | FIXED | Authentication identity does not collapse Domain agency. |
| AuthSession != DANTE Session | FIXED | Explicit security naming required. |
| Provider auth != provider-data integration | FIXED | Never share semantics/tokens by convenience. |
| PostgreSQL canonical authority | FIXED | Inherited from backend/CP6/ADR-010. |
| Frontend cannot fake authoritative success | FIXED | Server state owns auth/verification/recovery/link/session success. |
| Seven-macro-phase roadmap | FIXED FOR THIS WORKSTREAM | Supersedes earlier R0–R7 breakdown. |
| M1 Access Visual/UX Freeze | CLOSED | Baseline accepted; integration checks deferred to real wiring/closure. |
| M2 Auth Architecture Freeze | ACTIVE | M2.1–M2.8 accepted/documented; M2.9–M2.11 remain. |
| First executable production slice | FIXED | M3 email/password signin + AuthSession spine. |
| Deployment/browser topology | FIXED | Same-origin browser boundary through edge; `/api/v1/*`; physical service independence preserved. |
| Browser session model | FIXED | Opaque DB-backed server-authoritative session; secure host-only HttpOnly cookie. |
| JWT/localStorage browser auth | NOT SELECTED | Requires concrete evidence to reopen. |
| CSRF/CORS | FIXED | Synchronizer token + Origin + Fetch Metadata; normal browser CORS off. |
| Session lifetime default | FIXED POLICY | 30-day maximum/default inactive-session policy; background polling not user activity. |
| Concurrent Web/Mobile use | FIXED | Same Account may have multiple independent AuthSessions. |
| Multiple concurrent AuthSessions | FIXED | Session-per-client, independent expiry/revocation. |
| Logout current session | FIXED | Revoke current AuthSession. |
| Revoke all others | FIXED | Current survives after recent-auth-protected remote revocation. |
| Logout everywhere | FIXED | Revoke all sessions including current. |
| Device metadata = identity | NOT SELECTED | Device/IP/UA are metadata/risk signals only. |
| Account security root | FIXED | Account is not Person/profile/email/password/global role. |
| Password optional | FIXED | Account may authenticate via provider/passkey without PasswordCredential. |
| External provider identity | FIXED | Stable issuer + subject; provider email not canonical identity key. |
| Silent provider-email account merge | NOT SELECTED | Collision requires existing-account proof + consent + transactional link. |
| Password minimum | FIXED | 15 Unicode code points; >=64 supported; no composition rules. |
| Password maximum/resource bound | FIXED POLICY | 1024 code points / 4096 normalized UTF-8 bytes; no truncation. |
| Password manager/paste | FIXED | First-class supported behavior. |
| Password hashing | FIXED POLICY | Argon2id v19, 64 MiB, t=3, p=4, explicit params; maintained library proof required at dependency admission. |
| Password pepper | FIXED | HMAC-SHA-256 pre-hash with separate 256-bit server secret/key versioning. |
| Breached-password screening | FIXED | HIBP range/k-anonymity initial adapter; establish credential fail-closed, existing-login outage fail-open with telemetry. |
| Passkey-ready architecture | FIXED | 0..N passkeys; passwordless valid; authenticator does not own separate session architecture. |
| Passkey implementation | PLANNED M5 | Production WebAuthn registration/authentication in M5. |
| WebAuthn user verification | FIXED PRINCIPLE | Required for DANTE passkey class. |
| WebAuthn userHandle | FIXED PRINCIPLE | Random opaque 32-byte non-PII value per Account. |
| Consumer mandatory attestation | NOT SELECTED | Future high-security policy may justify separately. |
| MFA implementation | DEFERRED | TOTP/recovery codes/step-up/mandatory MFA later; architecture remains compatible. |
| `mfa_enabled` as full security model | NOT SELECTED | Use evidence/assurance-aware policy. |
| Email comparison | FIXED POLICY | NFC+casefold local part; IDNA canonical lowercase domain; separate display/delivery address. |
| Gmail dot/+tag canonicalization | NOT SELECTED | Provider-specific alias rules are not DANTE canonical identity rules. |
| Standard consumer verified email | FIXED PRODUCT INVARIANT | Maintain verified recovery/contact EmailIdentity, including provider/passkey accounts. |
| Provider email as canonical identity | NOT SELECTED | Never silently merge/link by email alone. |
| Google/Apple official provider integration | FIXED REQUIREMENT | Final implementation follows current official mechanisms/assets. |
| API namespace | FIXED | `/api/v1`; major compatibility generation, not release number. |
| API failure format | FIXED | RFC 9457 `application/problem+json` + stable DANTE extensions. |
| Machine error codes | FIXED | `namespace.snake_case`; client never parses human text. |
| Request correlation | FIXED | Server-authoritative `request_id` on every request/response. |
| Exact Auth SQL/table names | OPEN | Resolve slice-by-slice; no speculative mega migration. |
| M3 transaction/concurrency/session-expiry details | OPEN / NEXT | M2.9. |
| Generated-client tooling/boundary details | OPEN | M2.10. |
| M3 exact test matrix/harness | OPEN | M2.11. |
| Native mobile technology | FIXED | Existing Expo + React Native + Expo Router foundation. |
| Native Mobile Access | PLANNED M6 | Implement after canonical backend contracts are stable. |
| Full Home implementation | DEFERRED | Separate vertical after Access/Auth handoff. |

---

## 18. Access Visual/UX closure record — 2026-08-27

M1 closed after live local review of the existing Web Access surface and code/contract inspection.

Accepted:

- visual composition is coherent and should not be redesigned merely for novelty;
- current layout already uses deliberate grid/bounds/control sizing/responsive rules;
- future changes must preserve systematic geometry/design-token discipline;
- current Web Access surface inventory is sufficient to proceed to architecture/integration;
- visual polish remains allowed when integration proves a concrete defect or mismatch;
- provider buttons shown before real provider integration are not final provider-compliance authority;
- Terms/Privacy and final real-backend state QA remain closure obligations.

This closure does **not** claim the complete Access/Auth UX is production-proven before backend/provider/mobile integration.

---

## 19. M2.1–M2.8 documentation checkpoint — 2026-08-27

Accepted decisions from M2.1–M2.8 were moved out of chat-only/workstream-only state into durable subject-oriented current documentation.

Created:

```text
docs/architecture/access-auth-architecture.md
docs/architecture/access-auth-security-contract.md
docs/architecture/access-auth-api-contract.md
docs/decisions/ADR-011-access-auth-architecture.md
```

Navigation updated in:

```text
docs/architecture/README.md
docs/README.md
```

This checkpoint does **not** close M2 and does not claim runtime proof. It prevents accepted architecture from depending on conversation memory while M2.9–M2.11 continue.

Documentation structure deliberately follows DANTE lifecycle policy:

```text
architecture/security/API current truth → subject-oriented durable contracts
architectural rationale/rejected alternatives → ADR-011
operational state/gates/roadmap → this workstream
Git chronology → Git
```

---

## 20. Current known operational incidents

During the initial workstream bootstrap an accidental branch `__noop_should_not_create__` was created at the old baseline SHA. It did not modify `main` or `feature/access-auth`. Deletion was previously requested manually because the connector at that time did not expose delete-branch capability; cleanup has not been reconfirmed in this record.

During the 2026-08-27 roadmap-documentation gate, the ref-update action was accidentally invoked as a no-op targeting the already-current `feature/access-auth` SHA. Readback confirmed the branch SHA did not move and no commit/history change resulted. This is operational evidence only; no ref manipulation is part of the approved workstream method.

Do not repeat either pattern. File writes must stay within exact approved paths.

---

## 21. Git/write safety

Every repository write follows:

```text
fresh remote HEAD
→ exact WRITE GATE
→ exact CREATE / UPDATE / DELETE paths
→ purpose + explicit exclusions
→ explicit user authorization
→ re-fetch HEAD immediately before first write
→ write only approved scope
→ readback
→ compare/path audit
→ QA verdict
```

If HEAD changes from approved PRE-SCOPE before the first actual scoped write: STOP.

Separate explicit gate is required for force push, rebase, destructive reset, history rewrite, merge to `main`, extra branch/worktree, incidental cleanup or other destructive/out-of-scope action.

New chat != new branch.

---

## 22. Macro-phase closure protocol

A macro-phase is not considered CLOSED merely because discussion/code appears complete.

Before marking any macro-phase closed, update in the same bounded documentation step as applicable:

```text
roadmap phase status
+ decisions accepted during the phase
+ decision register
+ durable subsystem docs/ADRs affected
+ QA/evidence already proved
+ deferred items and reopen triggers
+ current branch/head handoff state
+ exact next active macro-phase / safe action
```

Minimum closure record must answer:

1. What exactly was decided?
2. What was implemented, if anything?
3. What was directly proved?
4. What remains deferred/open?
5. What would reopen the phase?
6. What is the next safe action?

Do not let a closed phase depend on chat memory for any durable decision.

---

## 23. Immediate next action

Current active macro-phase is:

```text
M2 — Auth Architecture Freeze
```

Do **not** start migrations/endpoints yet.

Current sequence:

```text
1. deployment origin topology                                  ACCEPTED
2. browser session / cookie / CSRF / CORS model               ACCEPTED
3. Account / EmailIdentity / PasswordCredential /
   AuthSession / Principal semantics                           ACCEPTED
4. multi-session lifecycle and revoke/logout-all policy        ACCEPTED
5. password hashing + breach-policy implementation             ACCEPTED
6. passkey-ready authenticator boundary + MFA compatibility    ACCEPTED
7. email normalization/comparison model                        ACCEPTED
8. API namespace + machine error/naming contract               ACCEPTED
9. M3 transaction/concurrency/session-expiry behavior           NEXT
10. OpenAPI → generated client → Web application boundary      AFTER M2.9
11. M3 test matrix / full-stack harness                         AFTER M2.10
12. M2 documentation/QA closure + WRITE GATE for M3 code       LAST
```

Only after all remaining M2 items are ratified and M2 is formally closed should M3 production implementation begin.