# DANTE — Access/Auth Full-Stack Vertical Workstream

- **Status:** ACTIVE / BRANCH-LOCAL DURABLE WORKSTREAM RECORD
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Created from protected `main`:** `f011e252b6a294a12c38927ef2d528244ea1fee6`
- **Initial verified remote HEAD:** `f011e252b6a294a12c38927ef2d528244ea1fee6`
- **Purpose:** single operational save-game, authority map, roadmap and quality gate for the first production full-stack Access/Auth vertical.

> This file is intentionally branch-local while the vertical is active. It must be updated after meaningful milestones, not after every chat message. Before integration it must pass the documentation lifecycle/knowledge-coverage gate; durable truth is propagated to current sources, important evidence/rationale is retained in the right place, and temporary branch-only continuation material is removed or consolidated.

---

## 1. Mandatory new-session bootstrap

A new chat, agent or context window does **not** create a new project, branch or worktree.

Continue the same real workstream:

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

The old frontend worktree `/home/mattia/projects/dante-frontend` remains a separate operational worktree for independent frontend activity only. Access/Auth frontend changes that are semantically required by this full-stack vertical belong to this `feature/access-auth` workstream and must not be split into a competing `feature/access-*` branch.

At the beginning of every new session:

1. read root `README.md`;
2. read `docs/README.md`;
3. read `docs/PROJECT-STATUS.md`;
4. read `docs/ROADMAP.md`;
5. read `docs/development/agent-operating-manual.md`;
6. read `docs/development/operating-rules.md`;
7. read `docs/development/documentation-and-handoff.md`;
8. read `docs/development/documentation-lifecycle-policy.md`;
9. read `docs/development/branching-and-environments.md`;
10. read `docs/development/repository-engineering-safety.md`;
11. read this file completely;
12. read current Access/frontend/database/architecture sources relevant to the next slice;
13. inspect relevant implementation/tests/migrations;
14. verify current remote branch HEAD and relation to `main`;
15. verify the local worktree before any local write.

Local verification minimum:

```bash
pwd
git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
git rev-parse origin/feature/access-auth
git worktree list --porcelain
```

Expected intended local path is `/home/mattia/projects/dante`. If branch/path/HEAD/worktree state is not what the active scope expects, STOP before write and reconcile explicitly.

Repository truth beats conversation memory.

---

## 2. Authority order for this workstream

Use the strictest current applicable source. The practical order is:

```text
protected-main implementation / migrations / tests
+ current accepted Domain / Logical / Physical / architecture decisions
↓
current durable product / architecture / database sources
↓
this active branch workstream record for bounded newer unmerged decisions/state
↓
current implementation on feature/access-auth
↓
historical CP6 / Access-frontend evidence and closed branch history
↓
conversation memory
```

Important current sources include, as applicable:

- `docs/frontend/access.md` — current durable pre-backend Access frontend contract;
- `docs/frontend/production-readiness/backend-integration-contract.md`;
- `docs/frontend/production-readiness/quality-gates.md`;
- `docs/database/README.md` and Database Dictionary/reference artifacts;
- accepted architecture/technical-decision documentation;
- CP6 PostgreSQL constitution/closure/QA documents where persistence invariants are relevant;
- current backend bootstrap, mappings, migrations and tests;
- current frontend Access state machine, UI and release tests.

Historical archives are evidence, never newer authority.

---

## 3. Baseline already closed before this vertical

### 3.1 Domain / Logical / Physical

The core Domain Model, Logical Model, pre-Physical coherence and Physical target are closed/accepted foundations. This vertical consumes them; it does not casually reopen them.

Carry-forward semantic invariants include:

```text
Possibility / Proposal != Decision != Plan != Action != Actual != Outcome != Progress
Person != Account != Principal != Actor
Responsibility != Participation != Authority
```

Any apparent need to violate an accepted semantic distinction is a reopen trigger, not permission for an implementation shortcut.

### 3.2 Backend / PostgreSQL CP1–CP6

Already integrated:

- FastAPI/Python backend foundation;
- PostgreSQL as canonical persistence authority;
- async SQLAlchemy;
- Alembic forward migration discipline;
- provisioning/runtime DB roles and ACL work;
- persistence mappings;
- whole-database materialization;
- migration/integrity/runtime/PostgreSQL acceptance tests;
- backend CI.

CP6 deliberately did **not** invent vertical-specific security concepts merely to make the schema look complete. In particular, Account/Principal/security-context persistence was left for the vertical that could justify exact semantics. Access/Auth is that vertical.

Therefore:

```text
adding justified Access/Auth persistence now
!= reworking CP6
```

but every new structural database change still inherits the same-change Database System-of-Record obligations.

### 3.3 Access pre-backend frontend

Already integrated before this branch:

- production Access shell;
- desktop/tablet/mobile web layouts;
- approved DANTE visual direction;
- IT/EN;
- Access state graph;
- signup/recovery/provider/linking/reauth/setup surfaces;
- local validation;
- accessibility and reduced-motion treatment;
- Playwright release matrix;
- component/unit tests;
- frontend CI;
- deliberate refusal to fake backend-authoritative success.

The frontend is therefore not a mock to discard. It is a production UI/state foundation that must now be connected to real application/backend authority without breaking its semantics.

---

## 4. Current implementation reality at workstream start

### Backend

At workstream bootstrap, the backend has infrastructure/bootstrap/platform/database foundations but no dedicated production Access/Auth capability module and no product Auth HTTP API beyond existing non-product bootstrap/health behavior.

### Database

The current canonical DB does not yet contain an Access/Auth persistence model such as Account, password credential, external provider identity or auth-session tables. That absence is deliberate vertical deferral, not an implementation defect in CP6.

### Frontend

The Access frontend already has a rich reducer/state model and explicit distinction between request intents and server-authoritative events. It currently does **not** have the real full-stack application/data boundary, generated API client/session bootstrap or authenticated Home handoff needed to complete the vertical.

### Contract generation

No Access/Auth OpenAPI-to-generated-TypeScript client path is considered complete yet.

---

## 5. Vertical boundary

### In scope

The vertical owns, when justified by gated slices:

- `Account` lifecycle and status;
- email identity;
- password credential;
- email signup;
- email verification;
- email/password signin;
- backend-authoritative authentication sessions;
- session bootstrap/lifecycle/logout/revocation;
- password recovery/reset;
- reauthentication / recent-auth proof;
- Google authentication;
- Apple authentication;
- external provider identity mapping;
- collision handling and explicit account linking;
- authenticated return routing;
- minimal setup/Home handoff boundary required to prove Access completion;
- Access/Auth HTTP API;
- OpenAPI contract;
- generated TypeScript client;
- frontend application/data-source wiring;
- required PostgreSQL migrations, mappings, dictionary/reference changes;
- security, rate-limit, replay, race/concurrency handling;
- unit, integration and full-stack browser E2E acceptance.

### Explicitly out of scope unless separately gated

- full Home/Today product implementation;
- unrelated frontend polish/pages;
- Gmail/Calendar data integrations;
- Google/Apple integrations that are not authentication;
- native mobile Access implementation;
- generic platform-wide RBAC redesign;
- refactoring accepted CP1–CP6 foundations merely for style;
- semantic collapse of Person/Account/Principal/Actor;
- treating the existing DANTE business `Session` as an authentication session;
- broad legal-content production work;
- incidental cleanup;
- extra branches/worktrees;
- direct work on `main`;
- merge/rebase/history rewrite without explicit gate.

A minimal protected `/home`-like destination may be introduced only to prove authenticated handoff. It must not silently become the Home vertical.

---

## 6. Semantic constitution for Access/Auth

These distinctions are mandatory unless explicitly reopened by higher-authority design work:

### 6.1 Person != Account

`Person` is a DANTE domain concept. `Account` is an access/security lifecycle concept. A person may be related to an account, but neither is an alias for the other.

### 6.2 Account != Principal

`Account` is durable account state. `Principal` is the security identity/context under which a request is authenticated/authorized. Do not persist a Principal table merely because the word exists; persistence requires evidence.

Current design direction: Principal should initially be a runtime security context derived from authoritative authentication/session/account state unless a later slice proves durable Principal persistence is required.

### 6.3 Principal != Actor

Authentication identity does not automatically equal the DANTE domain `Actor` concept. Authorization/acting context must not be inferred by naming convenience.

### 6.4 AuthSession != DANTE Session

DANTE already has a domain/business `Session` concept. Authentication session state must use an explicit security name such as `AuthSession` at conceptual/code level to avoid semantic collision.

### 6.5 Signin != integration authorization

Google/Apple authentication is not the same thing as authorizing Gmail, Calendar or another provider API integration. Provider login credentials/tokens/scopes must not silently become integration credentials.

### 6.6 Provider state != DANTE canonical state

External providers are evidence/inputs. DANTE PostgreSQL remains canonical for DANTE account/session/linking state.

### 6.7 Verification != profile

Email verification proves a bounded claim about an email/control flow. It does not by itself define a complete Person/profile/account model.

### 6.8 Reauthentication != initial signin

A currently authenticated user proving fresh control for a sensitive action is a distinct state/flow from initial sign-in.

### 6.9 Client integrity != identity

A browser/device/client signal must not be treated as proof of user identity.

### 6.10 Frontend success != authoritative success

The frontend may represent pending/requested/local-validation state. It must never invent backend-authoritative verification, signup, signin, reset, link or session success.

---

## 7. Mandatory engineering method

Do **not** implement the vertical as “finish backend, then wire frontend later”. Do **not** satisfy tests by faking frontend success.

Each production slice follows:

```text
product need/state
→ contract
→ domain/application behavior
→ persistence/security
→ endpoint
→ OpenAPI
→ generated TypeScript client
→ frontend application/data-source adapter
→ real UI/state transition
→ tests
→ full-stack E2E
→ QA
→ slice closed
```

A slice is not closed because one layer passes.

Architecture layers should remain explicit:

```text
modules/access/
  domain/
  application/
  ports/
  adapters/
    inbound/http/
    outbound/...
```

Exact physical layout is subject to the architecture gate and existing backend structure; do not create generic `BaseService`, `GenericRepository`, giant `AuthManager` or other premature abstraction merely for symmetry.

---

## 8. Persistence and database rules

PostgreSQL remains canonical.

### 8.1 Slice-driven schema

Do not create one giant speculative Auth migration. Tables/constraints/indexes appear only when a slice justifies them and their semantics are understood.

Conceptual candidates include:

- Account;
- EmailIdentity;
- PasswordCredential;
- AuthSession;
- verification/recovery proof/challenge state;
- ExternalIdentity;
- linking/collision transaction state if required.

These are conceptual candidates, not pre-approved SQL names or table layouts.

### 8.2 Same-change Database System-of-Record rule

A structural DB change is incomplete unless all applicable artifacts remain aligned in the same reviewed change:

```text
Alembic migration
SQLAlchemy mapping/metadata
Database Dictionary
human-readable Database Architecture & Reference
generated schema artifacts/diagrams where applicable
direct database tests
```

A new table without required Dictionary/reference treatment is incomplete.

### 8.3 Forward-only migrations

Normal migration history is forward-only. Do not rewrite already-integrated migration history for convenience.

### 8.4 Constraints are race arbiters

Application checks improve UX but do not replace canonical database uniqueness/integrity constraints. Email identity, provider subject and other uniqueness invariants must survive concurrent requests.

### 8.5 Transactions are explicit

State transitions that must succeed/fail together use explicit transaction boundaries. Examples include password reset + required session revocation or account linking + uniqueness enforcement.

---

## 9. Security constitution and open decisions

Security-sensitive choices must be ratified before implementation rather than discovered accidentally in code.

### 9.1 Session model — RECOMMENDED / ARCHITECTURE GATE REQUIRED

Current recommended direction:

- opaque cryptographically-random session secret;
- browser receives it only in a secure cookie;
- `HttpOnly`;
- `Secure` in deployed HTTPS environments;
- DB stores a digest/derived verifier, never the raw secret;
- backend/PostgreSQL authoritative session state;
- revocable;
- explicit absolute expiry;
- controlled idle expiry if adopted;
- rotation where the threat model/lifecycle requires it.

Avoid defaulting to bearer JWT in browser `localStorage` merely because it is common. DANTE needs reliable revocation, lifecycle, reauth, linking and canonical DB authority; JWT is not prohibited in every context, but it requires explicit evidence.

### 9.2 Deployment boundary — OPEN / BLOCKS COOKIE-CSRF-CORS FINALIZATION

Before finalizing auth transport, decide the deployed web/API topology:

- same-origin;
- same-site API subdomain;
- genuinely cross-origin.

That decision controls cookie `SameSite`, `Secure`, `Domain`, credentialed requests, CORS, CSRF strategy and provider redirect URIs.

### 9.3 Password storage/policy — RECOMMENDED / GATE REQUIRED

Current direction:

- evaluate maintained Argon2id support;
- explicit/versioned parameters;
- transparent rehash policy;
- no plaintext/reversible password storage;
- no logging passwords;
- no arbitrary composition rules unless evidence demands them;
- no silent truncation;
- support password managers/paste;
- generous user-facing maximum with a bounded server-side maximum to prevent resource abuse;
- server-side common/breached-password policy when an appropriate production mechanism is selected.

Exact library, parameters and breach-check mechanism remain architecture/security decisions, not assumptions.

### 9.4 Email normalization — FIXED PRINCIPLE / DETAILS TO DESIGN

Normalize conservatively. Do not globally remove Gmail dots, strip `+tags`, or apply provider-specific mailbox equivalence rules to all email addresses.

Database constraints remain the concurrency arbiter for whatever canonical comparison representation is selected.

### 9.5 Provider identity — FIXED PRINCIPLE

Provider subject/issuer and a validated provider assertion are identity evidence. Provider email alone is not canonical identity.

Do not retain provider access/refresh tokens unless DANTE authentication actually requires them. Authentication remains distinct from later provider-data integrations.

### 9.6 Secrets/logging — FIXED PRINCIPLE

Never persist or log raw passwords, raw session secrets, raw recovery/verification proofs, OAuth client secrets, provider tokens or other authentication secrets unless a reviewed protocol explicitly requires bounded protected storage.

Logs/telemetry must use non-secret correlation identifiers and safe machine semantics.

---

## 10. Verification, recovery and proof rules

Flows that issue a proof/challenge must design for:

- cryptographically strong generation;
- safe storage (normally verifier/digest rather than raw proof);
- explicit expiry;
- single-use semantics where required;
- replay resistance;
- consume-only-if-valid-and-unused behavior;
- resend/replace semantics;
- concurrent-consume races;
- neutral/anti-enumeration responses where user existence must not leak;
- safe delivery-port abstraction;
- failure/retry semantics that do not duplicate authoritative state transitions.

Recovery/reset must explicitly decide what happens to existing sessions and perform required password/session changes atomically where the security policy demands it.

---

## 11. Concurrency, replay and idempotency

Treat these as normal design requirements, not exotic edge cases.

At minimum reason about:

- concurrent signup for the same canonical email;
- concurrent verification/recovery proof consumption;
- reset racing with signin/session use;
- repeated logout/revoke requests;
- provider callback replay;
- unique `(provider, subject)` external identity;
- linking collisions;
- two concurrent link attempts;
- network retry of unsafe mutations;
- duplicate provider callbacks;
- transaction rollback after partial external activity.

Do not blindly auto-retry non-idempotent security mutations.

---

## 12. API and error-contract rules

The API models application intents, not CRUD access to Auth tables.

Before generated-client integration, define stable error semantics including as applicable:

- machine-readable error code;
- safe user-facing semantic category;
- HTTP status;
- retryability;
- bounded field errors;
- non-secret request/correlation id.

Frontend behavior must not parse English error strings such as `message.includes("password")`.

A versioned API namespace such as `/api/v1/...` is a candidate; exact topology is an architecture decision and must be ratified before endpoint proliferation.

Rate-limit and anti-abuse semantics belong to the API/application design for login, signup, verification, recovery and provider callbacks.

---

## 13. Frontend integration boundary

Do not bury remote authentication behavior inside the existing Access reducer/state graph.

Target layering:

```text
Access presentation/state machine
→ Access application boundary
→ session + mutations / remote state
→ data-source port
→ generated DANTE API client
```

Global session bootstrap/lifecycle is not the same thing as a single form reducer lifecycle.

The existing distinction between `REQUEST_*` and `SERVER_*` events is valuable and should be preserved: user intent may initiate a request, while authoritative transitions occur only from validated backend results.

Transport details should remain behind the data-source/application boundary so the UI does not become coupled directly to raw `fetch` semantics or generated-client response shapes.

---

## 14. Testing constitution

A production slice must use the strongest practical proof at each layer.

### Unit/domain/application

Prove deterministic business/security rules without transport noise.

### Persistence/integration

Use real PostgreSQL for constraints, transactions, migrations, race-sensitive behavior and repository/mapping semantics.

### API integration

Use real FastAPI application behavior, HTTP semantics, cookies/headers and canonical DB state.

### Generated client

OpenAPI/client drift must be detectable. Generated artifacts are not hand-maintained substitutes for the contract.

### Full-stack browser E2E

For the Access vertical, the release path must ultimately prove:

```text
real browser
→ real frontend
→ generated client/application adapter
→ real HTTP/FastAPI
→ real cookie/session behavior
→ real PostgreSQL
```

External systems such as mail delivery or Google/Apple may use deterministic protocol-faithful test adapters when direct third-party dependency would make CI unreliable. The internal DANTE path may not be replaced by fake frontend success.

### Regression obligations

Preserve accessibility, responsive behavior, IT/EN, reduced motion and the existing Access release matrix while adding real backend integration.

---

## 15. Definition of Done for every slice

A slice is CLOSED only when all applicable items pass:

```text
[ ] product states/intents are explicit
[ ] semantic invariants preserved
[ ] architecture decision(s) ratified
[ ] persistence justified and minimal
[ ] migration/mapping/Dictionary/reference aligned
[ ] security/threat cases handled
[ ] transaction boundaries explicit
[ ] concurrency/replay/idempotency considered and tested
[ ] HTTP/API contract stable
[ ] machine error semantics stable
[ ] OpenAPI reflects implementation
[ ] generated TypeScript client updated from contract
[ ] frontend consumes through intended boundary
[ ] frontend never invents authoritative success
[ ] unit tests PASS
[ ] PostgreSQL integration tests PASS
[ ] API integration tests PASS
[ ] full-stack E2E proves the real vertical path
[ ] accessibility/responsive/i18n regression PASS
[ ] no secrets/sensitive values leaked in logs/docs/tests
[ ] documentation/current workstream record updated
[ ] exact write-scope QA PASS
```

“Happy path works” is not a slice closure criterion.

---

## 16. Roadmap — gated vertical slices

The roadmap is intentionally vertical and evidence-driven. A later stage may be reordered only by an explicit architecture/product decision recorded here or in a higher authority.

### R0 — Workstream bootstrap and architecture lock

**Goal:** establish safe continuation, exact vertical boundary and ratify the cross-cutting decisions that the first executable slice needs.

**Includes:**

- this workstream record and index routing;
- verify current branch/worktree state;
- inspect current Access/backend/database foundations;
- ratify naming/semantics for Account, runtime Principal and AuthSession;
- decide deployment origin topology;
- decide session/cookie/CSRF/CORS model;
- decide password hashing/policy implementation;
- decide API namespace/error envelope;
- define Slice 1 persistence/API/frontend/test acceptance before code.

**Exit gate:** no unresolved decision that would force speculative session/signin code.

**Status at file creation:** documentation bootstrap in progress; production Auth implementation not started.

### R1 — Existing-account email/password signin + AuthSession spine

**Goal:** prove the first real end-to-end authenticated session before signup complexity.

**Why first:** it creates the reusable account credential/session/security/API/client/frontend/E2E spine without simultaneously adding email delivery and verification lifecycle.

**Required path:**

- real account fixture/setup through application/DB test infrastructure;
- password verification;
- authoritative AuthSession creation;
- secure browser session transport;
- session bootstrap after reload;
- runtime Principal derivation;
- protected minimal authenticated destination;
- logout/revocation;
- OpenAPI/generated client;
- real Access frontend signin wiring;
- real PostgreSQL/FastAPI/browser E2E.

**Exit gate:** browser can sign in against real backend/PostgreSQL, reconstruct session after reload, reach the protected boundary, then log out and lose access. No fake success.

### R2 — Email signup + verification

**Goal:** create an account/email/password identity and prove email control before the accepted account/setup transition.

**Includes:**

- account/email/password creation semantics;
- uniqueness/race behavior;
- verification challenge/proof;
- delivery port;
- resend/expiry/single-use/replay;
- anti-enumeration where applicable;
- verification consume;
- session/setup entry according to ratified product semantics;
- full frontend/API/client/E2E path.

**Exit gate:** all authoritative transitions derive from real backend state and proof consumption; concurrent duplicate signup/verification races are safe.

### R3 — Recovery + password reset

**Goal:** recover account control without leaking account existence or leaving unsafe sessions behind.

**Includes:** neutral request semantics, recovery delivery/proof, expiry/single-use/replay, password replacement, required session revocation, reset completion/signin behavior and full-stack UI path.

**Exit gate:** old credentials/session state behave exactly according to security policy after reset, including concurrency tests.

### R4 — Reauthentication / recent-auth

**Goal:** distinguish a valid existing session from fresh proof required for sensitive operations.

**Includes:** reauth challenge, recent-auth timestamp/proof semantics, server-side freshness policy, frontend state and negative/expiry cases.

**Exit gate:** sensitive boundary rejects stale authentication and accepts only valid fresh proof without creating a second accidental signin model.

### R5 — Google and Apple authentication

**Goal:** add external authentication while preserving DANTE canonical account/session authority.

**Provider requirements:** state, nonce, PKCE where applicable, callback validation, issuer/audience/signature checks, provider subject mapping, new/known/collision outcomes, session creation and error/replay behavior.

Google and Apple should share the canonical DANTE application contract where semantics are common while retaining provider-specific protocol adapters.

**Exit gate:** both providers can complete known/new account paths through protocol-faithful validation without using provider email as canonical identity and without conflating authentication with data integrations.

### R6 — Collision handling + explicit account linking

**Goal:** safely resolve cases where provider evidence collides with an existing DANTE account/identity.

**Includes:** collision state, proof of existing account control, explicit consent, transactional linking, uniqueness, replay/race handling, cancellation/recovery and frontend state.

**Exit gate:** linking cannot silently merge accounts, cannot be won by email coincidence alone, and remains safe under concurrent/replayed attempts.

### R7 — Setup persistence, definitive handoff and vertical hardening/closure

**Goal:** finish Access-specific setup state and prove the authenticated handoff into the next product vertical without implementing Home itself.

**Includes as required:** setup fields/state owned by Access, authenticated return, minimal protected Home/next-route boundary, session expiry/revocation hardening, rate limits/abuse cases, degraded backend behavior, mail/provider failures, generated-client drift, accessibility/responsive/i18n regression, hosted CI and documentation closure.

**Closure gate:** the complete Access/Auth vertical is production-ready, current documentation is consolidated, temporary branch-only continuation material is classified/removed, optional historical evidence is bounded, PR/hosted CI is clean, and merge to `main` occurs only after explicit user gate.

---

## 17. Decision register

Use these labels strictly:

- **FIXED:** accepted invariant/current authority; do not reopen casually.
- **RECOMMENDED:** current design direction with strong rationale, still requires architecture gate before implementation if security/contract-sensitive.
- **OPEN:** unresolved and must not be guessed in code.
- **HYPOTHESIS:** useful idea/evidence, not a requirement.
- **DEFERRED:** intentionally postponed with an owner/reopen trigger.

Current register:

| Topic | State | Current position / reopen trigger |
|---|---|---|
| Person != Account | FIXED | Preserve domain/security boundary. |
| Account != Principal | FIXED | Principal is not automatically durable account state. |
| Principal != Actor | FIXED | Security identity does not collapse domain actor semantics. |
| AuthSession != DANTE Session | FIXED | Explicit naming required to avoid semantic collision. |
| Provider auth != provider-data integration | FIXED | Never share semantics/tokens by convenience. |
| PostgreSQL canonical authority | FIXED | Inherited from backend/CP6. |
| Frontend cannot fake authoritative success | FIXED | Inherited from Access contract. |
| Slice-based full-stack implementation | FIXED FOR THIS WORKSTREAM | Do not batch backend then retrofit UI. |
| First executable slice = signin/session spine | RECOMMENDED | Reopen only if R0 evidence proves another slice reduces risk materially. |
| Opaque DB-backed browser session | RECOMMENDED | Ratify after origin/deployment/security review. |
| JWT/localStorage browser auth | NOT SELECTED | Requires explicit evidence to overturn current direction. |
| Principal persistence table | NOT JUSTIFIED | Add only if a later slice proves durable identity-context semantics. |
| Deployment origin topology | OPEN | Must resolve before cookie/CORS/CSRF finalization. |
| Exact password hashing library/params | OPEN | Select maintained Argon2id-capable implementation or document superior evidence. |
| Exact API namespace/error envelope | OPEN | Resolve before endpoint/client proliferation. |
| Exact SQL/table names for Auth concepts | OPEN | Resolve slice-by-slice; no speculative mega migration. |
| Native mobile Access | DEFERRED | Reopen after web vertical contracts/state/API are stable enough to reuse. |
| Full Home implementation | DEFERRED | Separate vertical after authenticated handoff is proven. |

---

## 18. Lessons carried forward from prior work

1. Do not confuse selected design with implemented/validated behavior.
2. Do not create ontology/schema merely because a generic architecture template suggests it.
3. Database semantics require direct PostgreSQL evidence, not only ORM confidence.
4. Migrations, mappings and Dictionary/reference must move together.
5. Constraints are the final concurrency arbiter; application pre-checks alone are insufficient.
6. Explicit transaction/locking/replay analysis belongs in design, not post-bug hardening.
7. Historical handoffs must not become competing current truth.
8. Frontend state names and UX can be production-grade before backend exists; wiring must preserve that work rather than replace it with transport-driven components.
9. Provider protocols are adapters around DANTE application semantics, not the domain model itself.
10. Security values must not leak through logs, telemetry, tests, fixtures or documentation.
11. A successful click path is not enough: negative, expiry, replay, race, degraded-service and restart/bootstrap paths are first-class acceptance cases.
12. Tool/context limits never justify truncating current authority or claiming QA that was not actually run.

---

## 19. Git/write safety for this branch

Every repository write uses:

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

If HEAD changed from approved PRE-SCOPE: STOP.

Separate explicit gate is required for force push, rebase, destructive reset, history rewrite, merge to `main`, extra branch/worktree, incidental cleanup or other destructive/out-of-scope action.

New chat != new branch.

This branch remains the full-stack Access/Auth workstream until genuinely production-ready and closed unless an explicit architectural decision changes that.

---

## 20. How to maintain this record

Update this file after a meaningful milestone, accepted architectural decision, materially changed roadmap, blocker/tool incident that affects safe continuation, or completed gated slice.

Do not append an endless chronological diary. Keep current sections current.

At each update record at minimum:

- current verified branch HEAD;
- last closed roadmap stage/slice;
- exact active stage;
- accepted decisions since previous update;
- remaining OPEN decisions that block implementation;
- QA already proved;
- blockers/incidents that materially affect continuation;
- next safe action;
- any changed out-of-scope boundary.

If a temporary chat-specific handoff is ever truly required, it is secondary to this durable workstream record and must not become the only location of a durable decision.

---

## 21. Immediate next action after R0 documentation bootstrap

Do **not** jump directly into migrations or endpoints.

Next architectural task is to close the R0 blockers needed by R1, in this order:

```text
1. deployment origin topology
2. browser session / cookie / CSRF / CORS model
3. Account / EmailIdentity / PasswordCredential / AuthSession Slice-1 semantics
4. password hashing/policy implementation
5. API namespace + machine error contract
6. exact R1 transaction/concurrency/session-expiry behavior
7. exact OpenAPI → generated client → frontend application boundary
8. exact R1 test matrix and full-stack harness
9. WRITE GATE for the first production-code slice
```

Only after those decisions are ratified should R1 production implementation begin.
