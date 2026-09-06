# DANTE AI-05B — Concrete Implementation Blueprint

- **Status:** CANDIDATE / SUBSTANTIVE BLUEPRINT MATERIALIZED / DESTRUCTIVE ACCEPTANCE PENDING
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-05 — Whole-System Acceptance + Implementation Blueprint
- **Sub-phase:** AI-05B — Concrete Implementation Blueprint
- **Established:** 2026-09-02
- **Upstream:** AI-05A CLOSED / STRUCTURALLY ACCEPTED / BD-01..BD-41
- **Current core eval:** DANTE-E01..DANTE-E14
- **Implementation:** NONE
- **Provider/model/SDK selection:** OPEN / DIRECT-EVIDENCE GATED
- **Database change:** NONE
- **New PostgreSQL/Alembic object:** NONE
- **First vertical:** Global Search + read-only Ask DANTE

This document materializes the AI-05A build boundary into implementation-grade contracts. It does **not** start production implementation, select a provider, activate new persistence, or reopen AI-02/03/04/PRE-AI05.

Repository truth and accepted upstream authority outrank implementation convenience.

---

## 1. Objective

AI-05B answers:

```text
Given the accepted DANTE AI architecture and AI-05A ownership map,
what exact repository shape, public contracts, runtime DTOs, ports,
adapters, state ownership, test planes, activation gates and build order
can be implemented without weakening the accepted semantics?
```

Binding posture:

```text
AI-02..04 / PRE-AI05 / AI-05A = upstream contract
AI-05B                           = concrete build contract
implementation                  = later workstream
```

AI-05B may refine names and repository placement only where AI-05A explicitly deferred them. It may not move canonical authority, invent generic AI persistence, make provider SDK semantics the application contract, or collapse Search into Intelligence.

---

## 2. Inherited non-negotiable invariants

The implementation blueprint preserves at minimum:

```text
PostgreSQL = sole canonical persistence + material-history authority
MODEL OUTPUT != PUBLISHABLE OUTPUT
Interaction Session != Run != Worker
Context != Retrieval != Memory
ContextManifest != BasisManifest
APPROXIMATE != COMPLETE
UNRESOLVED != UNBOUNDED
DEFAULT NONCANONICAL PERSISTENCE = NO
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
HARNESSPROFILE != PROVIDERBINDING
EVAL CANDIDATE != PRODUCTION ROUTE
ENTITLED != SERVABLE
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
RUN-START AUTONOMY != PERPETUAL AUTONOMY
ATTENTION DECISION != PROACTIVE WORK ADMISSION != EFFECT AUTHORIZATION
SAFE SINGLE DISCLOSURE != SAFE CUMULATIVE DISCLOSURE
RECIPIENT != SURFACE != CHANNEL
SOURCE FUTURE ELIGIBILITY != PRIOR DISCLOSURE OCCURRENCE
GLOBAL SEARCH != INTELLIGENCE ORCHESTRATION
PROVIDER SDK != APPLICATION CONTRACT
RESPONSIBILITY BOUNDARY != MODULE != SERVICE != TABLE
```

AI-05B additionally binds:

```text
READ-ONLY FIRST VERTICAL != EFFECT AUTHORITY REMOVED
NO DATABASE CHANGE NOW != DATABASE CAN NEVER EVOLVE
NO PROVIDER SELECTION NOW != PROVIDER CONTRACT DEFERRED
NON-STREAMING FIRST HTTP SURFACE != PROVIDER STREAMING SEMANTICS IGNORED
REQUEST-OWNED STATE != UNOBSERVABLE STATE
AUTH SEAM NOT YET IN THIS BRANCH != AUTH BYPASS ALLOWED
```

---

## 3. Observed repository truth and path disposition

Current branch source is still foundation-heavy:

```text
apps/backend/src/dante/
├── __init__.py
├── bootstrap/
│   ├── __init__.py
│   ├── app.py
│   └── lifespan.py
└── platform/
    ├── config/
    ├── database/
    └── recovery/
```

Current test/build facts:

```text
apps/backend/tests/unit                 EXISTS
apps/backend/tests/integration          EXISTS
apps/backend/pyproject.toml             EXISTS
apps/backend/uv.lock                    EXISTS
.github/workflows/backend-ci.yml        EXISTS
tooling/ai-evals                        DOES NOT EXIST
apps/backend/src/dante/modules          DOES NOT EXIST
provider SDK dependency                 DOES NOT EXIST
production AI runtime                   DOES NOT EXIST
```

Disposition for the first implementation workstream:

| Path | Disposition | AI-05B contract |
|---|---|---|
| `apps/backend/src/dante/bootstrap/app.py` | MODIFY LATER | register module routers only; no AI orchestration |
| `apps/backend/src/dante/bootstrap/lifespan.py` | MODIFY LATER | construct/dispose process-scoped AI resources only when needed |
| `apps/backend/src/dante/bootstrap/wiring.py` | CREATE LATER | explicit composition root for Search/Intelligence/provider/config/policy/resource seams |
| `apps/backend/src/dante/platform/config/settings.py` | MODIFY LATER | deployment selectors/locators only; no behavior policy language |
| `apps/backend/src/dante/platform/config/intelligence.py` | CREATE LATER | typed deployment-only AI settings and immutable route-config selector |
| `apps/backend/src/dante/platform/database/**` | KEEP | canonical PG runtime/mappings unchanged by AI-05B |
| `apps/backend/migrations/**` | KEEP / NO CHANGE | current Alembic head remains authoritative |
| `apps/backend/src/dante/modules/search/**` | CREATE LATER | independent deterministic Global Search capability |
| `apps/backend/src/dante/modules/intelligence/**` | CREATE LATER | DANTE intelligence application/orchestration boundary |
| `apps/backend/tests/unit/**` | EXTEND LATER | pure contracts, architecture rules, fakes |
| `apps/backend/tests/integration/**` | EXTEND LATER | real PG Search projection, wiring, selected adapter conformance |
| `tooling/ai-evals/**` | CREATE ONLY AT QUALIFICATION STEP | direct DANTE stochastic/route qualification tooling |
| `tests/system/**` | CREATE ONLY WHEN BLACK-BOX SURFACE EXISTS | cross-app/system proof |
| temporary AI live handoff | DELETE BEFORE protected-main integration | never merge temporary save-game |

No existing backend source path is deleted by the first implementation slice.

---

## 4. Target dependency topology

The first implementation target is a capability-first modular monolith:

```text
HTTP INBOUND
   │
   ├──────────────→ modules/search/public.py
   │                    │
   │                    ↓
   │              Search application
   │                    │
   │                    ↓
   │              Search read/query port
   │                    │
   │                    ↓
   │              private PostgreSQL adapter
   │                    │
   │                    ↓
   │              canonical PostgreSQL
   │
   └──────────────→ modules/intelligence/public.py
                        │
                        ├→ execution contract / WorkContract
                        ├→ context + retrieval orchestration
                        ├→ modules/search PUBLIC surface
                        ├→ policy consumer seam
                        ├→ route/config snapshot
                        ├→ resource-control seam
                        ├→ ModelAccessPort
                        │      ↓
                        │   private provider adapter
                        │      ↓
                        │   provider SDK / protocol
                        ├→ verification / result maturity
                        ├→ effect consumer seam -> NO_EFFECT in first vertical
                        └→ safe final publication
```

Forbidden dependency directions:

```text
Intelligence -> Search private PostgreSQL adapter        FORBIDDEN
Intelligence -> SQLAlchemy session/mappings              FORBIDDEN
Model/provider code -> raw DB session                    FORBIDDEN
Provider SDK -> public/application contracts             FORBIDDEN
Production runtime -> tooling/ai-evals                   FORBIDDEN
Search -> Intelligence                                   FORBIDDEN
Platform -> Search/Intelligence product semantics        FORBIDDEN
Bootstrap -> owns orchestration behavior                 FORBIDDEN
```

`modules/search` may depend on bounded platform database mechanics through its private outbound adapter. `modules/intelligence` consumes Search through Search's public application contract only.

---

## 5. Concrete module/public-boundary candidate

Implementation should create only paths required by the step being built. The complete target skeleton is:

```text
apps/backend/src/dante/modules/
├── __init__.py
├── search/
│   ├── __init__.py
│   ├── public.py
│   ├── contracts.py
│   ├── application.py
│   ├── ports.py
│   └── adapters/
│       └── outbound/
│           └── postgres.py
└── intelligence/
    ├── __init__.py
    ├── public.py
    ├── contracts/
    │   ├── __init__.py
    │   ├── execution.py
    │   ├── context.py
    │   ├── retrieval.py
    │   ├── effect.py
    │   ├── provider.py
    │   └── policy.py
    ├── application/
    │   ├── ask.py
    │   ├── context.py
    │   ├── retrieval.py
    │   ├── routing.py
    │   ├── verification.py
    │   └── publication.py
    ├── ports/
    │   ├── model_access.py
    │   ├── search_access.py
    │   ├── policy.py
    │   ├── resource_control.py
    │   ├── effect.py
    │   └── telemetry.py
    └── adapters/
        ├── inbound/
        │   └── http.py
        └── outbound/
            └── models/
                └── <provider>.py      # only after provider selection gate
```

The required API domains remain explicit:

```text
execution
context
retrieval
search
effect
provider
policy
```

These are implementation contract domains, **not new canonical Domain roots**. `policy.py` is a consumer/adaptation seam; AI-05B does not create a new canonical Policy owner.

Public surface rule:

```text
modules/search/public.py
→ stable Search application entrypoint + stable Search request/result contracts

modules/intelligence/public.py
→ stable Ask/Intelligence application entrypoint + stable first-vertical request/result contracts

private adapters / SQLAlchemy / provider SDK
→ never re-exported through public.py
```

Internal runtime contracts should use frozen stdlib dataclasses/enums/UUID-based technical identifiers where practical. Pydantic is used at HTTP/config serialization boundaries, not as the semantic owner of internal contracts.

---

## 6. Execution / Work contract

First-vertical request execution is request-owned and single-turn.

Minimum internal execution types:

```text
WorkId                  technical request-local UUID
RunId                   technical request-local UUID
WorkContract             immutable protected execution meaning
ExecutionDeadline        absolute monotonic/deadline semantics
ConsequenceProfile       READ_ONLY in first vertical
ExecutionStatus          accepted/running/completed/failed/cancelled/superseded
ResultMaturity           provisional/verified/publishable/rejected
```

Minimum `WorkContract` fields:

```text
work_id
objective
purpose
resolved_actor/recipient context reference
surface = PRIVATE_IN_APP
scope
protected_constraints
consequence_profile = READ_ONLY
deadline
requested_capabilities
approval_conditions = NONE for read-only first vertical
```

`WorkContract` is immutable. Material relaxation creates a derived/superseding contract; it is never silently edited in place.

First vertical does not persist Work/Run state.

---

## 7. Search public contract

Search is independently useful and deterministic/no-model capable.

### 7.1 Search guarantee vocabulary

Every Search query declares the guarantee it asks for and every result declares the guarantee actually satisfied:

```text
EXACT
BOUNDED_COMPLETE
BEST_EFFORT
APPROXIMATE
SAMPLED
```

The first vertical must not label lexical/ranked discovery as `COMPLETE` unless the declared eligible universe and query family can prove completeness.

### 7.2 Method-scoped query families

The private PostgreSQL adapter is **not** a generic repository/query builder. It exposes only bounded Search-owned query families required by public Search semantics:

```text
search_current(CurrentDiscoveryQuery) -> SearchPage
search_history(HistoricalDiscoveryQuery) -> SearchPage
resolve_navigation(CanonicalNavigationQuery) -> NavigationResult
read_sources(SourceReadQuery) -> SourceReadResult
```

No method accepts arbitrary table/model names, arbitrary SQL expressions, ORM classes, or model-generated predicates.

```text
NO Repository[T]
NO generic find(model, filters)
NO arbitrary model-to-SQL
NO universal Entity search API
```

### 7.3 Search request/result minimum fields

`SearchRequest` / query-family DTOs carry:

```text
query text / structured terms appropriate to the method
search family
requested guarantee
current-vs-history intent
bounded result limit / cursor
purpose
resolved access context from authoritative Auth/AuthZ seam
safe facet/snippet request where supported
```

A `SearchHit` carries only disclosed fields and at minimum:

```text
stable navigation/reference target
owner/search family
safe display/snippet fields
current-vs-history classification
source/provenance reference where available
material/basis/currentness reference where applicable
rank/sort evidence appropriate to the query family
result guarantee
```

Search miss means only:

```text
NO ELIGIBLE RESULT FOUND UNDER THIS QUERY + ACCESS + GUARANTEE
```

It does not prove canonical nonexistence.

### 7.4 Hidden-result non-interference

Permission/disclosure filtering happens before any externally visible:

```text
hit
snippet
facet
count
rank side-channel
source navigation
```

Unauthorized/hidden rows must not change user-visible counts/facets/ranking in a way that reveals their existence.

### 7.5 PostgreSQL adapter

Candidate private path:

```text
modules/search/adapters/outbound/postgres.py
```

Allowed implementation tools:

```text
SQLAlchemy Core for exact reviewed queries
explicit SQL when clearer/safer
existing DANTE mappings/metadata as infrastructure representation
```

The adapter is method-scoped to the accepted query families. It does not become canonical ownership and never mutates business state.

No FTS/pg_trgm/vector index is activated by this blueprint. Initial implementation must use only query behavior justified by the already-materialized schema. Any FTS/trgm/vector activation follows the normal PostgreSQL same-change rule and its own evidence gate.

---

## 8. Search transaction contract

Search uses a Search-specific read scope; it does not expose `AsyncSession` to Intelligence.

Conceptual contract:

```text
Search application
→ begin SearchReadScope
→ invoke bounded SearchQueryPort methods
→ complete/rollback read transaction
```

The concrete PostgreSQL read scope uses the existing process-scoped `DatabaseRuntime.session_factory` and an explicit read transaction. It must not call `commit()` for application mutations because Search has no mutation authority.

```text
SEARCH ADAPTER MAY READ
SEARCH ADAPTER MAY NOT COMMIT BUSINESS MUTATION
```

No long-lived DB transaction spans a provider call.

---

## 9. Context + Retrieval contracts for first Ask

The first Ask vertical materializes the minimum AI-03 chain without inventing memory or vector infrastructure:

```text
ContextPlan
→ InformationNeed
→ RetrievalPlan
→ Search public query
→ ContextFragment
→ ContextReadiness
→ ConsumerContext
→ ContextManifest

BasisManifest remains separate.
```

Minimum runtime types:

```text
ContextPlan
InformationNeed
RetrievalPlan
RetrievalStrategy
ContextFragment
ContextReadiness
ConsumerContext
ContextManifest
BasisManifest
BasisDependency
```

Initial retrieval strategies:

```text
SEARCH_CURRENT
SEARCH_HISTORY when explicitly needed
SOURCE_REREAD
CANONICAL_NAVIGATION
```

Not activated:

```text
vector ANN
embedding retrieval
AI memory store
provider-native file/vector store
speculative web retrieval
```

`InformationNeed` that cannot be safely/fully resolved remains unresolved. It is never widened silently to unrestricted retrieval.

`ContextManifest` records what was assembled and what was actually exposed to the model. `BasisManifest` records the reality/source/currentness dependencies on which the result depends.

Before publication, material basis dependencies are revalidated when the configured freshness/currentness rule requires it. A stale material basis either triggers a bounded reread/rebuild or produces a typed stale-basis outcome; it never silently publishes as current.

---

## 10. ModelAccessPort

DANTE owns the model-access contract.

Candidate port:

```text
ModelAccessPort.invoke(ModelInvocationRequest) -> ModelInvocationResult
ModelAccessPort.stream(ModelInvocationRequest) -> AsyncIterator[ModelEvent]
ModelAccessPort.cancel(ProviderAttemptId) -> CancellationOutcome
```

The first HTTP Ask surface does **not** externally stream; `stream()` is still part of provider-conformance scope because provider/runtime semantics must not be rediscovered later.

Minimum request semantics:

```text
model target
resolved immutable route/config snapshot identity
harness/profile identity
consumer context projection
response/structured-output contract
allowed tool/capability projection (empty in first vertical)
deadline
retry budget
provider-egress policy basis
```

Minimum result semantics:

```text
provider attempt identity
completion/outcome state
structured response payload
usage evidence
provider capability usage
finish/stop classification
acceptance uncertainty
provider timestamps/latency evidence
classified error if not completed
```

Provider SDK/protocol identifiers are adapter evidence, not DANTE semantic identity.

### 10.1 Provider error taxonomy

At minimum the adapter must classify:

```text
ProviderTransientError
ProviderPermanentError
ProviderRateLimitedError
ProviderTimeoutError
ProviderInvalidResponseError
ProviderDisconnectedError
IndeterminateExternalOutcomeError
CancellationError
DeadlineExceededError
```

`IndeterminateExternalOutcomeError` means DANTE cannot prove whether the external provider accepted/processed the attempt. It is never blindly retried unless the selected binding has independently proven safe idempotent retry semantics for that exact operation.

### 10.2 Provider conformance doubles

The selected adapter must have controlled doubles/fixtures for at least:

```text
normal response
rate limit
network timeout
invalid schema
stream disconnect
cancellation race
ambiguous submit / acceptance unknown
usage present / usage absent
unsupported requested feature
```

Application fakes remain distinct from adapter conformance fixtures.

---

## 11. Route/config artifact contract

Behavior-bearing AI route configuration is static/versioned/typed first.

Candidate repository source:

```text
apps/backend/config/intelligence/revisions/<revision>.json
```

No YAML/TOML dependency is required for the first implementation; JSON is validated into frozen Pydantic config models.

Minimum artifact schema:

```text
schema_version
revision
created_from_git_sha
model_targets[]
harness_profiles[]
provider_bindings[]
route_policies[]
feature_modes[]
qualification_requirements[]
control_profiles[]
retry/fallback policy references
```

The artifact does not contain provider secrets.

Deployment-only settings may provide:

```text
active approved config revision
provider endpoint/deployment locator
region
credential/secret reference
approved operational kill/emergency selector
resource/environment limits
```

Before each logical ModelInvocation, DANTE resolves one coherent immutable `RouteConfigSnapshot` and records its identity in telemetry/evidence.

```text
ROUTE SNAPSHOT IMMUTABLE DURING INVOCATION
!= AUTHORIZATION FROZEN FOREVER
!= EMERGENCY DENY IGNORED
```

Production provider activation remains blocked until the chosen emergency-deny mechanism meets AI-04C requirements. AI-05B does not invent a dynamic control-plane database to solve that prematurely.

---

## 12. Policy consumer seam

Intelligence does not own Authority/AuthZ/Consent/Visibility truth.

The policy seam is method-specific rather than one model-selected universal verdict:

```text
authorize_context_exposure(...)
authorize_model_egress(...)
authorize_effect(...)
authorize_publication(...)
```

Minimum `PolicyDecision` evidence:

```text
ALLOW / DENY
policy/control basis identity
resolved principal/recipient/surface
purpose
obligations / disclosure constraints
revalidation requirement
reason code safe for internal evidence
```

A policy denial raises/returns `PolicyDeniedError` internally. Search hidden-result behavior still follows non-interference and may intentionally return an empty/filtered result instead of exposing a denial reason.

The Access/Auth product vertical is not yet integrated on this branch. Therefore:

```text
NO temporary X-User-Id bypass
NO fake-auth production route
NO local Intelligence-owned authorization truth
```

Unit/integration tests may construct explicit test access contexts. Production/private HTTP route activation is gated on an authoritative integrated Auth/AuthZ public seam.

---

## 13. Resource admission / settlement seam

Candidate port methods:

```text
estimate(ResourceEstimateRequest) -> ResourceEstimate
admit(ResourceAdmissionRequest) -> ResourceAdmission
settle(ResourceSettlementRequest) -> ResourceSettlement
```

The first technical slice may operate without a durable commercial ledger only when commercial/shared quota is not being enforced.

Request-local controls may still enforce:

```text
max attempts
max model invocations
max token/cost estimate
max deadline
fallback bounds
```

Provider usage evidence is always observable when available, but:

```text
PROVIDER USAGE != COMMERCIAL ENTITLEMENT
PROVIDER TOKENS != COMMERCIAL CREDIT
```

If shared/monthly/commercial quota becomes an eligibility condition, production activation stops until the proper durable commercial/resource owner and accounting state exist.

---

## 14. Effect boundary and transaction rule

AI-05B freezes the Effect consumer seam even though the first vertical is read-only.

Minimum effect contract:

```text
EffectIntent
EffectPlan
EffectAuthorization
EffectOutcome
EffectDisposition = NO_EFFECT | EXECUTED | REJECTED | INDETERMINATE
```

For the first vertical:

```text
ConsequenceProfile = READ_ONLY
EffectDisposition   = NO_EFFECT
canonical mutation  = NONE
PostgreSQL commit   = NONE
```

Future consequential verticals must follow:

```text
Effect application/coordinator owns canonical mutation coordination
outer application operation owns transaction boundary
persistence adapters may flush but do not independently commit
provider/external outcomes are not atomically rolled back with PostgreSQL
ambiguous external outcome creates reconciliation obligation
```

No application/provider adapter may hold a PostgreSQL business transaction open across a network provider call.

---

## 15. First-vertical orchestration contract

Read-only Ask DANTE executes conceptually:

```text
HTTP request
→ authenticated request context
→ WorkContract
→ minimal ContextPlan
→ InformationNeed
→ current-aware Search / source reread
→ ContextReadiness
→ Policy: context/provider egress
→ eligible qualified route composition
→ Resource admission
→ ModelAccessPort when model assistance is required
→ verification / ResultMaturity
→ Effect boundary = explicit NO_EFFECT
→ basis/currentness revalidation
→ Policy: publication
→ safe final publication
```

Deterministic Search path is independent:

```text
HTTP Search
→ authenticated request context
→ Search public service
→ permission/disclosure-aware Search read scope
→ canonical/current/history/source result
→ safe final response
```

Provider outage therefore degrades Ask but does not make deterministic Global Search unavailable.

---

## 16. HTTP and publication shape

The simplest first vertical is **non-streaming application HTTP**.

Candidate inbound routes:

```text
POST /api/v1/search
POST /api/v1/ask
```

Rationale:

```text
private authenticated in-app
single-turn
request-owned
read-only
no durable resume
no external recipient surface
model output requires verification/publication gate
```

A non-streaming first Ask response avoids externalizing unverified provider deltas before Safe Result Publication.

Internal provider streaming may still be consumed/buffered for latency/adapter qualification, but:

```text
INTERNAL MODEL STREAM != RECIPIENT STREAM
```

Public SSE/WebSocket/NDJSON streaming is **not activated** in the first vertical. If later enabled, every externally emitted delta becomes a publication event requiring result-maturity/disclosure/currentness semantics and disconnect handling; that is a separate activation gate, not a transport swap hidden inside the provider adapter.

Minimum `AskResponse`:

```text
work_id
answer
result_maturity = PUBLISHABLE
sources/provenance[]
currentness/basis summary safe for recipient
model-assisted boolean
safe error/limitation information when applicable
```

No provider name, internal policy reason, hidden search count, prompt, or private telemetry is exposed unless explicitly part of an approved product contract.

---

## 17. Error taxonomy and first HTTP mapping

Application-level taxonomy must include at least:

```text
InvalidRequestError
StaleBasisError
PreconditionFailedError
CapabilityUnavailableError
PolicyDeniedError
ProviderTransientError
ProviderPermanentError
IndeterminateExternalOutcomeError
IsolationExecutionFailureError
CancellationError
DeadlineExceededError
```

First vertical mapping intent:

```text
invalid request                 -> 400/422 boundary validation
stale basis / precondition      -> 409 when safe to disclose
policy denied                   -> 403 only when denial itself is disclose-safe
capability unavailable          -> 503
provider transient              -> 503
provider permanent/bad gateway  -> 502
provider outcome indeterminate  -> 502/503 with no unsafe automatic duplicate attempt
deadline exceeded               -> 504
client cancellation             -> stop request-owned work; response may be impossible if client is gone
isolation execution failure     -> not reachable in initial envelope
```

Search hidden-result cases intentionally prefer filtered/empty semantics when a denial response would reveal protected existence.

---

## 18. Runtime/evidence/persistence classification

### 18.1 Request-owned / no-store

```text
WorkContract
RunId / run-local status
ContextPlan
InformationNeed
RetrievalPlan
ContextFragment
ContextReadiness
ConsumerContext
ContextManifest
BasisManifest
SearchRequest / SearchHit / SearchPage
PolicyDecision for ordinary first-vertical request
ResourceAdmission for unmetered/request-local first slice
ModelInvocationRequest / ModelInvocationResult
ProviderAttempt runtime object
EffectDisposition=NO_EFFECT
PublicationResult
```

These are deleted with request completion/cancellation and are not stored in PostgreSQL by the first vertical.

### 18.2 Durable outside canonical PostgreSQL

```text
versioned route/config revision
→ Git/release artifact

qualification evidence
→ CI/release qualification artifact with explicit retention and immutable identity

operational telemetry
→ observability backend according to operations retention; not canonical product truth
```

### 18.3 Persist only on independent trigger

```text
conversation continuity
Run registry / durable resume
AI memory
Context cache
prior-disclosure accounting
commercial/shared usage ledger
idempotency/saga/reconciliation records
background/durable Work state
async invalidation jobs
vector/embedding derived state
```

Each requires its own owner, purpose, lifecycle, retention, deletion/recovery and activation evidence before becoming eligible.

```text
DATABASE CHANGE = NONE
ALEMBIC CHANGE  = NONE
```

---

## 19. Lifecycle matrix

| Object | Create | Persist | Mutate/version | Delete/expire | Cache | Retry | Cancel |
|---|---|---|---|---|---|---|---|
| `WorkContract` | request intake | no | immutable; derive/supersede | request end | no | same protected contract unless materially changed | marks request-owned work cancelled |
| `ContextPlan` | Ask planning | no | new plan version on material replan | request end | no initially | rebuild on bounded stale/unresolved case | discard |
| `RetrievalPlan` | per InformationNeed | no | replace with explicit strategy change | request end | no initially | bounded by plan/deadline | stop outstanding reads |
| `SearchRequest/Page` | Search/retrieval | no | immutable result object | request end | no initially | only explicit DB transient policy | cancel DB read when possible |
| `BasisManifest` | after source assembly | no first vertical | new manifest after reread/revalidation | request end | no | stale -> reread/rebuild, not in-place truth rewrite | discard |
| `PolicyDecision` | each enforcement boundary | no ordinary first slice | never silently reused after material basis change | request end | no | re-evaluate on required boundary | n/a |
| `RouteConfigSnapshot` | before ModelInvocation | config revision durable in Git | snapshot immutable | request end; revision retained | process cache allowed by exact revision | retry keeps or re-resolves only according to policy; material delta requires evidence | n/a |
| `ProviderAttempt` | each outbound attempt | no canonical persistence | immutable attempt; retry creates new attempt | request end; telemetry retained separately | no | new attempt ID | provider cancel if supported |
| `ResourceAdmission` | before route attempt | no first slice | immutable decision | request end | no | new admission if route materially changes | reservation release if applicable |
| `EffectOutcome` | effect boundary | no first read-only slice | immutable | request end | no | future consequential retry governed separately | cancellation != undo dispatched effect |
| `PublicationResult` | after verification/policy | no | immutable emitted result | response end | no | publication retry only if recipient semantics allow | disconnect stops further publication |
| route config revision | reviewed config change | Git/release | immutable new revision only | retained per release policy | process-load cache | n/a | emergency deny may block use |
| qualification artifact | qualification run | CI/release evidence store | immutable artifact; new run => new ID | evidence retention policy | n/a | new artifact | n/a |

---

## 20. Observability and evidence contract

The first vertical must emit enough operational evidence to prove the accepted architecture without leaking sensitive content.

Minimum evidence categories:

```text
work/run identity
release/build/config revision
policy basis identities and allow/deny boundary outcomes
Search query family + guarantee + eligible result count AFTER disclosure filtering
context readiness / unresolved needs
basis/currentness outcome
route candidate/selection/fallback reason class
provider binding/adapter/model-target identities
provider capability usage
provider attempt/retry/cancellation/outcome class
usage/cost evidence where available
stage timing
resource admission/settlement outcome
verification/result-maturity outcome
publication outcome
reconciliation status
rollback status
isolation status/leakage status
```

For first vertical the last three may legitimately be `NOT_APPLICABLE`, but their absence must be distinguishable from missing instrumentation.

Default telemetry prohibition:

```text
NO raw private prompt/body
NO raw model response
NO hidden Search result content
NO secrets/credentials
NO unrestricted ConsumerContext
```

Telemetry is operational evidence, not product audit/canonical history.

---

## 21. Test topology

Concrete target layout:

```text
apps/backend/tests/unit/modules/search/
→ Search contracts, guarantee semantics, hidden-result behavior with pure doubles

apps/backend/tests/unit/modules/intelligence/
→ Work/Context/Retrieval/Policy/Effect/Publication pure behavior
→ deterministic ModelAccess fake
→ stale-basis and cancellation/deadline cases

apps/backend/tests/unit/test_architecture_boundaries.py
→ import/dependency rules

apps/backend/tests/integration/modules/search/
→ real PostgreSQL Search projection under @pytest.mark.postgres

apps/backend/tests/integration/modules/intelligence/
→ wiring + Search public seam + config snapshot + fake provider

apps/backend/tests/integration/providers/<binding>/
→ selected provider adapter conformance after provider gate

tooling/ai-evals/
→ direct DANTE E01..E14 applicable route qualification using production-owned composition

tests/system/
→ black-box Search/Ask only after real HTTP/auth surface exists
```

Architecture tests must enforce at minimum:

```text
Intelligence cannot import Search private adapter
Intelligence cannot import SQLAlchemy/database mappings
provider SDK imports only inside provider-binding adapter package
production code cannot import tooling/ai-evals
Search cannot import Intelligence
bootstrap may import public composition targets but contains no orchestration logic
no generic Repository[T] introduced in Search/Intelligence
```

### 21.1 Mandatory fixtures

Stale-basis proof uses either:

```text
two independently valid canonical fixtures
OR
create valid fixture -> mutate canonical state -> assert stale/revalidation behavior
```

Provider adapter fixtures include:

```text
rate limit
timeout
invalid schema
disconnect
ambiguous submit
cancellation race
```

Cross-boundary tests prove that Search/private persistence, provider adapter, policy authority and Effect transaction ownership cannot be bypassed by the Intelligence application.

---

## 22. Qualification artifact schema

Every promotable provider/model route composition must have an immutable qualification artifact containing at least:

```text
schema_version
qualification_id
created_at
git_sha
release/build identity
route_config_revision
model_target_id
harness_profile_id
provider_binding_id
provider_adapter_identity/version
feature_mode
policy/control revision identities
security/data transformation revision identities
retry/fallback composition
direct-eval suite/version
applicable DANTE-E01..E14 cases + hard-gate results
provider conformance evidence reference
live compatibility/smoke evidence reference where required
capacity/reliability evidence reference where required
cost/usage evidence
material deltas from previously qualified composition
revalidation/expiry condition
promotion decision/status
```

Binding BD-41 rule:

```text
PROMOTION ALLOWED
IFF
same material production composition was qualified
OR every material delta has independent qualifying evidence.
```

`tooling/ai-evals` must invoke production-owned route/provider components through the bounded qualification seam. It must not implement a second provider stack.

---

## 23. Feature / activation gates

| Capability | Initial state | Activation requirement |
|---|---|---|
| deterministic structured/current Search | eligible build target | real PG integration + disclosure/auth seam + tests |
| deterministic Search HTTP route | gated | authoritative integrated Auth/AuthZ request context |
| FTS/pg_trgm lexical acceleration | OFF | measured Search need + DB same-change package + QA |
| pgvector/ANN/embeddings | OFF | retrieval eval proves need + derived-state owner/freshness/security lifecycle |
| Ask with deterministic ModelAccess fake | non-production test only | pure application tests |
| concrete provider adapter | OFF | provider/model/SDK decision gate + protocol evidence plan |
| live provider compatibility smoke | OFF | credentials/egress + selected binding |
| direct DANTE provider/model eval | OFF | same material production composition available |
| production Ask | OFF | direct eval + conformance + capacity/reliability + Auth/AuthZ + egress + config/emergency deny + observability |
| external result streaming | OFF | delta-level Safe Publication/disconnect/cumulative-disclosure contract proven |
| consequential Effect | OFF | later vertical + policy/approval/transaction/reconciliation proof |
| commercial/shared quota ledger | OFF | real commercial/shared enforcement requirement |
| durable Run/resume/background | OFF | request lifetime insufficient for accepted product case |
| AI memory persistence | OFF | explicit memory owner/purpose/lifecycle/retention trigger |
| prior-disclosure accounting | OFF | H19-eligible cross-Run/surface case activated |
| Restate/R2/MCP/A2A | OFF | independent measured trigger |
| Execution Environment | OFF | generated/untrusted code/browser/computer-use workload activated |

---

## 24. Provider/model/SDK decision gate

AI-05B intentionally does not guess the provider stack.

A provider/model/SDK may be frozen only after the decision-critical candidate set is tested against an explicit evidence packet:

```text
current API/SDK compatibility
required structured-output semantics
required streaming/cancellation semantics
tool-call semantics if needed later
usage/cost reporting
rate-limit/error taxonomy
idempotency/ambiguous-submit behavior
data handling/region/retention requirements
DANTE direct eval quality on applicable workload
latency/reliability/cost envelope
adapter complexity / feature loss
```

The decision artifact records:

```text
ADOPT / ADAPT / DEFER / REJECT
selected binding/model target if any
material assumptions
unsupported features
qualification scope
revalidation trigger
```

Until that evidence exists, provider/model/SDK remain `OPEN` and no package is added to `pyproject.toml`/`uv.lock`.

---

## 25. Dependency / framework lock

Initial allowed dependency direction:

```text
FastAPI/Pydantic existing inbound/config boundaries
SQLAlchemy/psycopg existing PostgreSQL infrastructure
stdlib internal contracts/orchestration where sufficient
one selected provider SDK only inside its private provider adapter after gate
```

Forbidden unless explicitly reopened by evidence:

```text
LangChain/LangGraph-style orchestration ownership
agent framework as DANTE semantic owner
provider gateway as mandatory data path
MCP client/server framework for ordinary first vertical
new vector/search database
generic repository/UoW framework
ORM-driven model-to-SQL tool
```

MCP/client SDKs, when later activated, remain inside the corresponding capability/infrastructure adapter and never become the core application contract.

---

## 26. Implementation dependency graph

After AI-05 whole-phase closure, implementation order is constrained by:

```text
B0  architecture boundary test scaffolding

B1  Search contracts + pure Search application
    ↓
B2  bounded PostgreSQL Search read adapter + real PG tests
    ↓
B3  deterministic Search inbound/public surface
    [HTTP production registration waits for Auth/AuthZ seam]

B4  Intelligence execution/context/retrieval/policy/effect contracts
    + deterministic ModelAccess fake
    + Search public consumer seam
    ↓
B5  versioned route/config schema + loader + coherent snapshot
    + resource/evidence seams
    ↓
B6  provider/model/SDK evidence decision gate
    ↓
B7  one selected provider adapter + conformance/live compatibility proof
    ↓
B8  tooling/ai-evals using SAME production-owned composition
    + direct DANTE qualification
    ↓
B9  read-only Ask DANTE HTTP surface
    + final Safe Publication
    ↓
B10 production hardening
    observability / retry / fallback / privacy / cost / load / emergency deny
    ↓
B11 system acceptance + production activation evidence
```

No step may pull a later trigger forward merely because its library/framework is convenient.

---

## 27. First implementation commit sequence

Each implementation commit should be reviewable, reversible at code level where practical, and preserve green existing gates.

Candidate sequence:

```text
C1  feat(search): add public contracts and deterministic application shell
C2  feat(search): add bounded PostgreSQL read projection and integration proof
C3  feat(search): add private in-app HTTP adapter/wiring behind auth activation gate
C4  feat(ai): add execution/context/retrieval/policy/effect contracts and ModelAccess fake
C5  feat(ai): add route-config snapshot/resource/evidence seams
C6  chore(ai): record provider/model/SDK evidence decision
C7  feat(ai): add selected private provider adapter + conformance proof
C8  test(ai): add direct eval qualification tooling using production composition
C9  feat(ai): add read-only Ask DANTE + safe final publication
C10 test(ai): add full Search/Ask system + failure/operational hardening
```

`C6` may intentionally end in `DEFER` if evidence is insufficient; in that case C7+ do not proceed.

Database migration commit: **NONE** for this first vertical unless a later independently justified Search capability activation proves a concrete structural need.

---

## 28. Existing CI/build gates

Every backend implementation commit remains subject to the current locked backend gate:

```text
uv lock --check
uv sync --locked
ruff format --check
ruff check
mypy strict
pytest -m "not postgres"
uv build
real PostgreSQL pytest -m postgres
```

AI implementation adds tests to these planes rather than creating a weaker parallel CI lane.

Provider/direct-eval/capacity qualification are additional evidence planes and do not replace the normal backend gate.

---

## 29. Destructive AI-05B acceptance battery

This candidate is **not accepted** until a fresh destructive pass executes at least the following cases from zero:

```text
B05-01 repository path truth / no phantom implemented package
B05-02 Search and Intelligence public/private dependency direction
B05-03 deterministic Search survives provider unavailable/unconfigured
B05-04 hidden Search result non-interference for hits/counts/facets/rank
B05-05 current vs history semantics preserved
B05-06 Search miss != canonical nonexistence
B05-07 method-scoped query adapter / no Repository[T] / no arbitrary query builder
B05-08 no model/provider path can receive raw SQLAlchemy/DB authority
B05-09 Context != Retrieval and UNRESOLVED != UNBOUNDED
B05-10 ContextManifest != BasisManifest / provider exposure recorded separately
B05-11 stale basis mutate-after-fixture before publication
B05-12 policy exposure/egress/publication bases revalidated at required boundaries
B05-13 provider rate-limit/timeout/invalid-schema translation
B05-14 provider disconnect/cancellation race
B05-15 ambiguous submit -> indeterminate outcome -> no unsafe duplicate retry
B05-16 immutable route snapshot + material config identity
B05-17 emergency deny can block otherwise coherent invocation
B05-18 provider SDK confined to private binding adapter
B05-19 resource admission/settlement ownership not swallowed by Intelligence
B05-20 first vertical explicit NO_EFFECT / no canonical mutation
B05-21 no PostgreSQL business transaction held across provider call
B05-22 provider outage degrades Ask only, not Global Search
B05-23 no new generic AI persistence / Alembic unchanged
B05-24 Auth/AuthZ missing -> production route remains gated, no bypass
B05-25 non-streaming final publication leaks no unverified model delta
B05-26 telemetry/evidence distinguishes NOT_APPLICABLE from missing instrumentation
B05-27 application fake != adapter conformance != direct eval != capacity proof
B05-28 BD-41 same material production composition / delta qualification
B05-29 activation gates prevent FTS/vector/durability/effects/isolation premature use
B05-30 architecture imports remain acyclic and production does not import eval tooling
B05-31 lifecycle table has create/persist/mutate/delete/cache/retry/cancel semantics for every first-vertical object
B05-32 reverse AI-05B -> AI-05A -> AI-04 -> PRE-AI05 -> AI-03 -> AI-02 consistency
```

Compound destructive cases must additionally collide:

```text
hidden Search data + Ask synthesis + provider outage
stale basis + route retry + emergency deny
config rollout + in-flight immutable snapshot + current policy revalidation
provider ambiguous outcome + retry budget + resource settlement
client cancellation + provider attempt + no durable Run
cumulative privacy condition + first-vertical no-persistence eligibility gate
direct eval + material production delta + promotion attempt
```

A failed case produces bounded hardening and a **fresh full retest**. No PASS is inferred from this document itself.

---

## 30. Explicit non-claims

```text
AI-05B substantive candidate materialized      YES
AI-05B structurally accepted                   NO
AI-05 whole phase closed                       NO
modules/search implemented                     NO
modules/intelligence implemented               NO
Auth/AuthZ integrated on this branch           NO
provider/model/SDK selected                    NO
provider dependency added                      NO
direct provider eval executed                  NO
production capacity qualified                  NO
production Ask route active                    NO
external streaming selected/active             NO
PostgreSQL/Alembic changed                      NO
new AI table/index                             NO
FTS/trgm/vector activated                      NO
conversation persistence selected              NO
control-plane persistence selected             NO
commercial/resource ledger implemented         NO
Restate/R2/MCP/A2A activated                   NO
Execution Environment selected                 NO
```

---

## 31. AI-05B next action

Exact next action after materializing this candidate:

```text
1. run Fresh AI-05B destructive battery B05-01..B05-32
2. run compound collision suite
3. materialize only bounded hardening demonstrated by failures
4. rerun the full battery from zero
5. run reverse AI-05B -> AI-05A -> AI-04 -> PRE-AI05 -> AI-03 -> AI-02
6. only after clean PASS create durable AI-05B acceptance/closure authority
7. then run whole AI-05 destructive acceptance / closure
8. only after whole AI-05 closure begin production implementation workstream(s)
```

No provider/backend implementation starts merely because this blueprint candidate now exists.
