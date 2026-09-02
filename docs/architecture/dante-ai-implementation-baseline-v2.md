# DANTE Intelligence — Current Implementation Baseline v2

- **Status:** CURRENT POST-AI05 HARDENED CANDIDATE / FRESH MKT-001..MKT-090 REQUIRED
- **Branch:** `feature/ai-architecture`
- **Established:** 2026-09-02
- **PRE-SCOPE:** `d7784da59251a25d6ff72ffee6e230e082a831dc`
- **Upstream:** AI-05 CLOSED / STRUCTURALLY ACCEPTED
- **Post-closure hardening:** POST05-H01..H18 APPLIED
- **Implementation:** NONE
- **Provider/model/SDK:** OPEN / CANDIDATE-ADMISSION + QUALIFICATION GATED
- **Database change:** NONE
- **Alembic change:** NONE
- **Implementation entry:** HOLD UNTIL FINAL MEGA PASS

This file is the second consolidated implementation-facing candidate authority for DANTE Intelligence.

It exists because the first post-AI05 baseline survived most of the independent attack but still failed five bounded areas. Those failures are preserved in:

```text
docs/architecture/dante-ai-post05-preimplementation-mega-kill-test.md
→ POST05-H01..H13 discovery/evidence

docs/architecture/dante-ai-post05-second-hardening.md
→ POST05-H14..H18 discovery/evidence

docs/architecture/dante-ai-implementation-baseline.md
→ first consolidated candidate / pre-v2 evidence
```

This v2 baseline directly incorporates all still-valid build substance of:

```text
AI-05A ownership/build boundary
AI-05B concrete implementation blueprint
AI05B-H01..H15
AI05-H01 readiness hardening
AI-05B / AI-05 closure contracts
POST05-H01..H18
```

A new implementation task must not reconstruct current build truth by applying historical hardening documents mentally.

The older files remain truthful validation evidence. This file becomes accepted current implementation authority only after:

```text
MKT-001..MKT-090 PASS
+ compound collision suite PASS
+ reverse authority pass PASS
+ representative product/simulation replay PASS
+ current routing reconciliation PASS
```

Until then:

```text
IMPLEMENTATION I0 = HOLD
```

---

# 1. Authority stack and non-negotiable inheritance

This baseline consumes and does not redefine:

```text
Product / North Star
Domain Model
Whole Logical Model / WL-H01..WL-H12
Physical Model
PostgreSQL Persistence Constitution / ADR-010
current Database System of Record
AI-00 DANTE AI Foundation
AI-02.1 Intelligence Runtime Architecture
AI-03A Full Context Architecture
AI-03B Retrieval + Memory Architecture
AI-03C Materialization Blueprint
AI-04A Eval / Provider / Economics
AI-04B Runtime / Capability Architecture
AI-04C Production Assurance / Control Plane / Operations
AI-04 Whole-Phase Acceptance
PRE-AI05 Cross-Phase Hardening
AI-05A Build Boundary / Ownership Map
AI-05B Concrete Implementation Blueprint
AI-05 Whole-System Closure
```

Repository/executable truth outranks this file if a future accepted implementation deliberately evolves architecture through the normal project process.

Binding invariants include at minimum:

```text
DANTE != chatbot
DANTE != provider
DANTE != model
DANTE != transcript

PostgreSQL = sole canonical persistence + material-history authority
CANONICAL != DERIVED != PROVIDER != RUNTIME

Person != Account != Principal != Actor
Authority != AuthZ
Consent != Authority
Visibility != Authority

Possibility != Goal != Proposal != Decision != Plan != Activity
Routine != Occurrence
Occurrence != Schedule != Session != Actual
Actual != Observation != Outcome

NativeRef != ScopedRecordRef != MaterialStateRef != ExternalRef
MaterialStateRef != provider revision / ETag / MVCC token

AI inference != confirmed fact
model confidence != Confirmation
search rank != truth
vector similarity != truth
summary != source
embedding != source
cache != source

absence / unknown != false
current != historical
schedule/time passage != completion

Context != Retrieval != Memory
ConsumerContext != ContextManifest != BasisManifest
RetrievalCandidate != ContextFragment
Context access != disclosure permission
DATA != INSTRUCTION
USER CONTENT != CURRENT USER INSTRUCTION AUTOMATICALLY

Interaction Session != Run != Worker
Scenario != canonical current

MODEL OUTPUT != PUBLISHABLE OUTPUT
RAW PROVIDER EVENT != DANTE RUNTIME EVENT != PUBLICATION EVENT
PROVIDER ATTEMPT FAILED != DISCLOSURE DID NOT HAPPEN

RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
RUN-START AUTONOMY != PERPETUAL AUTONOMY
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
CANCELLATION REQUESTED != CANCELLATION CONFIRMED != EXECUTION QUIESCED

MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
HARNESSPROFILE != PROVIDERBINDING
PROVIDER SDK != APPLICATION CONTRACT

QUALIFIED != ELIGIBLE != AVAILABLE != ENTITLED != ROLLOUT-ACTIVE
APPLICATION FAKE != ADAPTER CONFORMANCE != LIVE COMPATIBILITY != DIRECT EVAL != CAPACITY PROOF
CANDIDATE ADMISSION != PRODUCTION QUALIFICATION

BUILD-READY != INTEGRATION-READY != ACTIVATION-READY

SAFE DISCLOSURE TO PROVIDER A
+
SAFE DISCLOSURE TO PROVIDER B
!= AUTOMATICALLY SAFE COMBINED DISCLOSURE
```

---

# 2. Current repository/materialization truth

At v2 establishment, backend source remains foundation-heavy:

```text
apps/backend/src/dante/
├── bootstrap/
└── platform/
    ├── config/
    ├── database/
    └── recovery/
```

The following are target paths only; they are not implemented claims:

```text
apps/backend/src/dante/modules/search
apps/backend/src/dante/modules/intelligence
tooling/ai-evals
apps/backend/config/intelligence/revisions
```

Do not create empty ceremonial directories. A path appears only when the current reviewed implementation step has real content.

Current backend dependency truth remains:

```text
FastAPI
Pydantic / pydantic-settings
SQLAlchemy async
psycopg
Alembic
```

No AI/provider SDK is currently accepted as a dependency.

Current database remains:

```text
PostgreSQL          18.6
schema              dante
Alembic             20260830_09
69 tables
5 views
15 routines
76 triggers
97 indexes
69 FKs
123 CHECK constraints
```

```text
DATABASE CHANGE = NONE
ALEMBIC CHANGE  = NONE
```

No Search/AI implementation convenience is sufficient evidence to reopen the current Domain/Logical/Physical/PostgreSQL shape.

---

# 3. Final capability ownership

## 3.1 Search

Target owner:

```text
apps/backend/src/dante/modules/search
```

Search owns:

```text
Global Search / discovery application contract
structured filters for discovery
keyword/lexical discovery when activated
current/history discovery semantics
permission-safe eligible result universe
safe snippets/facets/counts/rank/pagination
canonical/source navigation refs
SearchFamilyRegistry
bounded cross-capability read projection for Search only
Search-specific query/read transaction scope
```

Search does not own:

```text
canonical business semantics
arbitrary structured analytics
all semantic queries
mutation/effects
authorization truth
provider/model routing
universal entity identity
```

Binding:

```text
GLOBAL SEARCH != INTELLIGENCE
SEARCH != SEMANTIC QUERY FOR EVERY DANTE QUESTION
SEARCH RESULT != CANONICAL TRUTH
SEARCH FAMILY != TABLE
```

## 3.2 Intelligence

Target owner:

```text
apps/backend/src/dante/modules/intelligence
```

Intelligence owns application/runtime orchestration for:

```text
WorkContract execution
Context planning/readiness
Reference/Target Resolution orchestration
Semantic Query / Projection orchestration
Retrieval orchestration
qualified deterministic/model route consumption
verification
Result Maturity
Effect consumer boundary
safe publication
request-local egress exposure accounting
runtime evidence emission
```

Intelligence does not own:

```text
canonical calendar/goals/people/work/health semantics
Search private persistence
Auth/AuthZ/Consent/Visibility truth
commercial subscription/shared accounting truth
provider SDK semantics
conversation database
```

## 3.3 Provider

Concrete provider SDK/protocol code exists only inside an admitted private outbound binding adapter.

Candidate physical placement:

```text
apps/backend/src/dante/modules/intelligence/adapters/outbound/models/<binding>/
```

No provider SDK type appears in public Search/Intelligence/application contracts.

## 3.4 Bootstrap / platform / tooling

```text
bootstrap
→ composition + lifecycle + inbound registration only

platform
→ genuinely shared technical infrastructure only

platform/config
→ deployment-only settings/secret refs/active config selector

platform/observability
→ shared telemetry mechanics when materialized

tooling/ai-evals
→ engineering qualification outside ordinary production request path
```

Production code never imports `tooling/ai-evals`.

---

# 4. Target repository shape

Create only files required by the current implementation step.

Candidate end-state for the first bounded vertical:

```text
apps/backend/src/dante/modules/
├── search/
│   ├── __init__.py
│   ├── public.py
│   ├── contracts.py
│   ├── application.py
│   ├── ports/
│   │   └── query.py
│   └── adapters/
│       └── outbound/
│           └── persistence/
│               └── postgres.py
│
└── intelligence/
    ├── __init__.py
    ├── public.py
    ├── contracts/
    │   ├── work.py
    │   ├── context.py
    │   ├── retrieval.py
    │   ├── references.py
    │   ├── model.py
    │   ├── provider.py
    │   ├── verification.py
    │   ├── publication.py
    │   ├── effects.py
    │   └── evidence.py
    ├── application/
    │   ├── ask.py
    │   ├── context.py
    │   ├── semantic_query.py
    │   ├── reference_resolution.py
    │   ├── retrieval.py
    │   ├── routing.py
    │   ├── verification.py
    │   └── publication.py
    ├── ports/
    │   ├── model_access.py
    │   ├── capability_query.py
    │   ├── policy.py
    │   ├── resource_control.py
    │   ├── effect.py
    │   └── runtime_evidence.py
    └── adapters/
        ├── inbound/
        │   └── http.py
        └── outbound/
            └── models/
                └── <binding>/
```

This is not permission to create one file/class per architecture noun mechanically.

The previously proposed Intelligence-owned `search_access.py` remains rejected. Intelligence consumes Search through the Search-owned public protocol.

No monolithic generic `core`, `ai`, `common`, `entity`, `repository`, `memory`, `run` or provider-owned application layer is authorized.

---

# 5. Search public contract

`modules/search/public.py` owns the only Search public application protocol.

Conceptual surface:

```text
class SearchService(Protocol):
    async def search(SearchExecutionRequest) -> SearchResult: ...
    async def resolve_navigation(NavigationExecutionRequest) -> NavigationResult: ...
```

`SearchExecutionRequest` is trusted application input and carries only:

```text
user query/filter projection
SearchEligibilityEnvelope
requested SearchFamilyIds after active/eligible intersection
current/history intent
bounded page/cursor
requested guarantee
route-owned purpose/surface
Runtime Interpretation Frame where Search meaning requires it
```

It cannot carry:

```text
raw SQL
ORM classes
table names
caller-created Authority/AuthZ decisions
provider/model route
Effect authorization
```

`SearchResult` preserves:

```text
safe hits
safe facets/counts when non-interference/coherence permits
pagination
achieved guarantee
limitations/unresolved classification
source/currentness/basis-safe metadata
```

`SearchHit` uses `SearchTargetRef`, never a universal `entity_id`.

Search miss means only:

```text
NO ELIGIBLE RESULT FOUND UNDER THIS QUERY + ACCESS + GUARANTEE
```

It does not prove canonical nonexistence.

---

# 6. SearchEligibilityEnvelope and hidden-result non-interference

`SearchEligibilityEnvelope` is an immutable request-scoped projection of current authoritative access/disclosure decisions.

Minimum semantics:

```text
principal / represented-party binding
purpose
recipient
surface
Authority/AuthZ/Visibility/Consent basis identities as applicable
current/history eligibility
permitted SearchFamilyIds
family-specific source/owner scope
permitted projection fields
snippet eligibility
facet/count eligibility
sensitivity/disclosure ceiling
source lifecycle exclusions
explicit negative/excluded scopes
revalidation condition
```

It does not own authority.

For protected Search:

```text
ELIGIBILITY CONSTRAINS THE CANDIDATE UNIVERSE
BEFORE OBSERVABLE RANK/COUNT/FACET/PAGINATION SEMANTICS.
```

Rejected as sole permission proof:

```text
query all private rows
→ rank/count/facet
→ post-filter hidden rows
```

Unauthorized/ineligible records may not influence externally visible:

```text
hit presence
snippet
count
facet
rank/order
cursor/page exhaustion
navigation target
latency/error wording where it becomes an existence oracle
```

---

# 7. SearchFamilyRegistry

`SearchFamilyId`, `SearchFamilyRegistration` and `SearchFamilyRegistry` are application/static contracts, not Domain identities or tables.

Each family registration freezes at least:

```text
family_id
owning capability/product boundary
canonical/source semantics
supported public query modes
current/history/source-reread support
maximum truthful guarantee
safe result projection schema
SearchEligibilityEnvelope requirements
concrete bounded query implementation identity
source/material-basis/currentness mapping
coherence/snapshot requirement
activation evidence reference
applicable direct-proof identifiers
```

```text
SEARCH FAMILY ID != TABLE NAME
SEARCH REGISTRY != DATABASE CATALOG
SEARCH REGISTRY != GENERIC REPOSITORY
```

A family activates only when:

```text
real useful product data exists
source/current/history semantics are known
eligible universe is permission-safe
bounded query behavior is implemented
coherence/guarantee is truthful
applicable direct proofs pass
```

The current 69-table schema is not automatically one useful Search universe.

---

# 8. SearchTargetRef / navigation

Search navigation preserves accepted DANTE references:

```text
SearchTargetRef
= NativeTargetRef(NativeRef, native_owner_kind)
| ScopedTargetRef(ScopedRecordRef, scoped_record_kind)
| MaterialStateTargetRef(MaterialStateRef, material_facet)
| ExternalTargetRef(ExternalRef, source_kind)
```

```text
SearchTargetRef != Domain identity
SearchTargetRef != universal EntityRef
SearchTargetRef != table+UUID wrapper
```

Navigation dispatches through owning capability/application semantics where available.

---

# 9. Semantic Query / Projection Gateway

Search discovery is not sufficient for all structured DANTE questions.

Intelligence preserves an application-level `SemanticQueryGateway` responsibility for stable, permission-aware structured meaning.

Conceptual surface:

```text
SemanticQueryGateway.execute(
    InformationNeed,
    ContextStrategy,
    TrustedRequestContext,
) -> SemanticQueryOutcome
```

The gateway composes:

```text
owning capability public query contracts
or
bounded approved typed query handlers
```

It cannot accept:

```text
raw SQL
ORM classes
table names
model-generated predicates with direct execution authority
```

`SemanticQueryOutcome` preserves as applicable:

```text
status
structured typed payload
achieved guarantee
source/reference bindings
currentness
basis/dependency evidence
coherence evidence/limitation
source standing/provenance
limitations
```

Representative statuses:

```text
RESOLVED
EMPTY_IN_DECLARED_BOUNDED_UNIVERSE
AMBIGUOUS
CONFLICTED
STALE
POLICY_BLOCKED
SOURCE_UNAVAILABLE
UNSUPPORTED
```

The payload remains capability/query-family specific, never one universal property bag.

Correct deterministic path:

```text
question
→ bounded semantic interpretation
→ InformationNeed
→ ContextStrategy.DETERMINISTIC_AGGREGATION / STRUCTURED_CURRENT_QUERY / ...
→ SemanticQueryGateway
→ owning capability query
→ typed result
→ verification
→ direct safe answer
```

No model is required merely to calculate a deterministic answer DANTE already owns.

A model may propose a bounded typed query intent for NL interpretation, but application validation/capability semantics own the actual query and result.

---

# 10. Reference / Target Resolution

Material referents are resolved explicitly before any answer/effect that requires unique/exact binding.

Conceptual contract:

```text
ReferenceResolutionRequest
ReferenceResolutionResult
```

Input preserves:

```text
unresolved expression / candidate clue
required resolution strength
permitted source/search families
subject/actor/represented-party context where material
Reality Scope
Runtime Interpretation Frame
purpose + security ceiling
eligible candidate universe/basis
```

Outcomes:

```text
RESOLVED
AMBIGUOUS
UNRESOLVED
NOT_FOUND_IN_DECLARED_BOUNDED_UNIVERSE
POLICY_BLOCKED
SOURCE_UNAVAILABLE
```

`RESOLVED` carries accepted DANTE refs only.

Resolution may consume Search/owning capability public seams and bounded model assistance, but:

```text
MODEL CONFIDENCE != REFERENCE RESOLUTION
DISPLAY NAME != CANONICAL TARGET
```

## 10.1 Reference-resolution non-interference

Reference resolution is a disclosure surface.

Candidate generation/resolution operates over the **eligible** candidate universe before externally observable:

```text
RESOLVED
AMBIGUOUS
NOT_FOUND
candidate count
candidate labels
clarification options
rank/confidence clue
```

Example:

```text
visible Marco A
hidden Marco B
```

must not become:

```text
AMBIGUOUS because Marco B exists privately
```

when the eligible universe contains only Marco A.

```text
AMBIGUOUS IN ALL DATA
!= AMBIGUOUS IN ELIGIBLE DATA
```

Hidden-result direct proof coverage therefore applies to material reference-resolution families too.

---

# 11. WorkContract / request ownership

First-vertical `WorkContract` is immutable and request-owned.

Minimum semantics:

```text
work_id / revision
objective
purpose
principal/actor/represented-party context ref as applicable
resolved target bindings when known
protected constraints
ConsequenceProfile
recipient + surface
requested capabilities
approval conditions
execution deadline
supersession/current-work relationship where applicable
```

Material relaxation creates a new/derived/superseding contract.

First vertical:

```text
ConsequenceProfile = READ_ONLY
approval conditions = NONE for ordinary read-only work
no durable Work/Run persistence
```

`RequestExecutionScope` owns request-local technical state:

```text
deadline
attached tasks
CancellationSignal
active ProviderAttemptIds
request-local EgressAttempts/exposure state
publication-open/closed
bounded cleanup state
```

Client disconnect may close publication while bounded in-process cleanup/correlation continues until deadline/outcome/cancel state permits termination.

Survival across process crash is a separate durability trigger.

---

# 12. Full Context contract projection

The build contract preserves all seven AI-03A Context contracts:

```text
ContextPlan
InformationNeed
ContextStrategy
ContextFragment
ContextReadiness
ConsumerContext
ContextManifest
```

plus `BasisManifest`.

## 12.1 ContextPlan

Preserves as applicable:

```text
WorkContract ref/revision
objective/purpose
Principal/Actor/represented party
Reality Scope
Runtime Interpretation Frame
known target bindings
reference-resolution requirements still unresolved
protected InformationNeeds
explicit exclusions / forbidden source/use
security/privacy compartment
resource constraints
InformationNeed set
```

## 12.2 InformationNeed

Preserves as applicable:

```text
requirement
origin: USER_EXPLICIT | WORK_CONTRACT | POLICY_REQUIRED | CAPABILITY_REQUIRED |
        MODEL_DISCOVERED | SOLVER_REQUIRED | VERIFIER_REQUIRED
scope / target / subject / temporal scope
Reality Scope
Runtime Interpretation Frame
purpose
reference-resolution requirement
criticality
coverage requirement
acceptable source semantics
freshness/currentness
coherence
representation/fidelity
consumer constraints
status
```

Important statuses:

```text
SATISFIED
PARTIAL
MISSING
CONFLICTED
STALE
POLICY_BLOCKED
SOURCE_UNAVAILABLE
SOURCE_RETIRED
AMBIGUOUS_TARGET
AMBIGUOUS_INTERPRETATION
```

Binding:

```text
UNRESOLVED != UNBOUNDED
MODEL_DISCOVERED NEED != PURPOSE/SCOPE EXPANSION
```

## 12.3 ContextStrategy

Strategy is explicit per InformationNeed and selects the least-complex route that can satisfy the required semantics.

Relevant strategy families include:

```text
STRUCTURED_CURRENT_QUERY
MATERIAL_HISTORY_QUERY
RELATION_TRAVERSAL
DERIVED_PROJECTION
DETERMINISTIC_AGGREGATION
SEARCH_DISCOVERY
DIRECT_SOURCE_READ
LEXICAL/FUZZY RETRIEVAL when activated
SEMANTIC/HYBRID RETRIEVAL when activated
DIRECT_LONG_CONTEXT when justified
INTERACTION/RUN CONTEXT when activated
SCENARIO_CONTEXT when activated
OPEN_WORLD/JIT when activated
```

The first vertical activates only the subset real workloads need.

## 12.4 Reality Scope

Preserve:

```text
CANONICAL_CURRENT
MATERIAL_HISTORICAL / AS_OF
SCENARIO <workspace> when activated
OPEN_WORLD_ASSERTION when activated
explicit MIXED only when legitimate
```

No cross-frame laundering.

## 12.5 Runtime Interpretation Frame

Where meaning depends on it, preserve:

```text
reference instant
applicable timezone/offset
source/target timezone where distinct
calendar/day-boundary semantics
DST resolution when ambiguous
locale/unit/calendar interpretation
spatial anchor/source/time/precision where material
```

Relative language such as `last month`, `today`, `next week`, `before Friday` cannot be resolved from server-local wall-clock assumptions.

---

# 13. Retrieval contract

When acquisition/discovery is required:

```text
InformationNeed
→ ContextStrategy
→ RetrievalPlan
→ acquisition route
→ RetrievalCandidate
→ validation
→ ContextFragment
```

## 13.1 RetrievalPlan

Preserves at least:

```text
InformationNeed refs/revisions
WorkContract/ContextPlan binding
consumer/step
purpose
Actor/represented party/Subject where material
Reality Scope
Runtime Interpretation Frame
reference-resolution requirement
eligible source classes/set
explicit exclusions
required retrieval guarantee
freshness/currentness
coherence
representation/fidelity
permitted transformations
resource/latency/cost budget
stopping criteria
bounded refinement ceiling
```

Query rewriting/translation/decomposition cannot change purpose/security/reference semantics.

## 13.2 Retrieval guarantees

```text
EXACT
BOUNDED_COMPLETE
BEST_EFFORT
APPROXIMATE
SAMPLED
```

```text
candidate count != coverage proof
APPROXIMATE != COMPLETE
```

## 13.3 RetrievalCandidate

A candidate is runtime discovery state, not Context/truth/evidence merely by rank.

It preserves enough to validate:

```text
InformationNeed/RetrievalPlan binding
source locator/class
NativeRef/ScopedRecordRef/MaterialStateRef/ExternalRef where real
retrieval representation/version
mechanism + rank/score metadata
retrieved_at
Reality Scope
Runtime Interpretation Frame applicability
source lifecycle hint
security/purpose scope
lineage
currentness hint
```

Candidate validation states include:

```text
ELIGIBLE_CURRENT
ELIGIBLE_HISTORICAL
ELIGIBLE_WITH_LIMITATION
STALE
CONFLICTED
SOURCE_RETIRED
SOURCE_REDACTED
POLICY_BLOCKED
NOT_CURRENTLY_VISIBLE
SOURCE_UNAVAILABLE
AMBIGUOUS_TARGET
AMBIGUOUS_INTERPRETATION
INVALID_DERIVATIVE
```

Only surviving candidate material becomes `ContextFragment`.

---

# 14. Source standing / instruction provenance

Every `ContextFragment`/`ConsumerContext` projection preserves enough metadata to keep distinct:

```text
source provenance
source standing
integrity
canonicality
sensitivity / derived sensitivity
source lifecycle
Reality Scope
Runtime Interpretation Frame applicability
instruction provenance / trust role
contradiction/conflict
```

Retrieved/imported/external/user-authored source text is DATA by default.

```text
DATA != INSTRUCTION
USER CONTENT != CURRENT USER INSTRUCTION AUTOMATICALLY
TRANSFORMED DATA != TRUSTED INSTRUCTION AUTOMATICALLY
```

Source content cannot create:

```text
new WorkContract purpose
new Authority/AuthZ/Consent
new InformationNeed outside accepted ceiling
provider/tool capability
Effect authorization
recipient disclosure permission
```

Harness/provider projection preserves role separation rather than flattening all text into one undifferentiated instruction channel.

Untrusted instruction provenance survives summaries/transforms where material.

---

# 15. ContextReadiness / ConsumerContext / ContextManifest / BasisManifest

`ContextReadiness` asks whether required needs are sufficiently covered/coherent/current for the current consumer step.

Legitimate outcomes include:

```text
READY
PARTIAL_WITH_DECLARED_LIMITATION
NEEDS_ACQUISITION
NEEDS_CLARIFICATION
CONFLICTED
STALE
POLICY_BLOCKED
INSUFFICIENT
```

`ConsumerContext` is consumer-specific minimized context.

```text
CONSUMER CONTEXT != ALL RETRIEVED DATA
```

`ContextManifest` records established or conservatively possible consumer/provider exposure at the material send boundary according to evidence.

It does **not** require a successful provider completion before exposure exists.

`BasisManifest` tracks material dependencies/currentness/coherence used to justify the result.

```text
ContextManifest != BasisManifest
```

First vertical does not persist either as a generic product row.

---

# 16. Request-local provider egress / exposure accounting

Every material outbound provider attempt creates request-local `EgressAttempt` state before/at the send boundary.

Conceptual fields:

```text
egress_attempt_id
work_id / invocation_id
ProviderAttemptId
recipient/provider binding
purpose
ConsumerContext projection identity
Disclosure/egress policy basis
material send state
acceptance certainty where knowable
exposure occurrence: NOT_SENT | POSSIBLE | ESTABLISHED
provider outcome state
```

Binding:

```text
provider result timeout/failure
!= exposure did not occur
```

Examples:

```text
connection failed before bytes left DANTE
→ exposure = NOT_SENT

request handed to transport / provider may have accepted
→ exposure = POSSIBLE or ESTABLISHED according to evidence

provider completed
→ exposure = ESTABLISHED
```

Exact transport evidence is adapter/protocol specific and normalized into DANTE semantics.

This state is request-local in the first vertical. It does not create durable cross-Run prior-disclosure storage by itself.

---

# 17. Intelligence public contract

`modules/intelligence/public.py` owns:

```text
class IntelligenceService(Protocol):
    async def ask(AskExecutionRequest) -> AskResult: ...
```

`AskExecutionRequest` is trusted/server-constructed and includes:

```text
WorkContract
trusted RequestContext
user question/scope projection
execution deadline
```

It cannot accept caller-selected provider/model/route/Effect authority.

`AskResult` is constructed only after verification + safe publication approval.

It may expose:

```text
safe work correlation
answer or declared limitation/abstention
safe sources/provenance
safe currentness/basis summary
model-assisted boolean
```

It is never the raw provider result.

---

# 18. HTTP trust boundary

Public inbound DTOs are untrusted transport objects.

```text
HTTP JSON
→ structural validation
→ authentication
→ route-owned purpose/surface
→ current Authority/AuthZ/Visibility/Consent projection
→ trusted RequestContext / SearchEligibilityEnvelope
→ WorkContract / application request
```

The client cannot supply authority-bearing values such as:

```text
principal override
represented-party authority
Authority/AuthZ/Consent basis
purpose escalation
SearchEligibilityEnvelope authority
provider/model/route
HarnessProfile
RouteConfigIdentity override
ConsequenceProfile upgrade
Effect authorization
resource/commercial entitlement
raw table/model/SQL
```

```text
Pydantic-valid != authorized
```

Candidate inbound routes:

```text
POST /api/v1/search
POST /api/v1/ask
```

Public private-data route activation waits for authoritative integrated Auth/AuthZ.

---

# 19. First-vertical execution routes

## 19.1 Deterministic Search

```text
HTTP Search
→ trusted SearchExecutionRequest
→ SearchService
→ eligible Search family
→ bounded PostgreSQL/read source
→ guarantee/coherence/source/currentness projection
→ safe SearchResult
```

No model/provider dependency.

## 19.2 Deterministic semantic question

```text
HTTP Ask
→ WorkContract
→ ContextPlan / InformationNeed
→ ReferenceResolution where required
→ ContextStrategy = structured/deterministic
→ SemanticQueryGateway
→ typed deterministic result
→ VerificationResult
→ EffectBoundary = NO_EFFECT
→ publication revalidation
→ AskResult
```

No model/provider call when unnecessary.

## 19.3 Model-assisted read-only Ask

```text
HTTP Ask
→ WorkContract
→ ContextPlan
→ InformationNeed(s)
→ ReferenceResolution where required
→ ContextStrategy per need
→ SemanticQuery and/or RetrievalPlan
→ RetrievalCandidate validation / ContextFragment
→ ContextReadiness
→ ConsumerContext
→ context/provider egress policy
→ eligible qualified route
→ Resource admission
→ request-local cumulative-disclosure/egress evaluation
→ ModelAccessPort
→ EgressAttempt + ContextManifest exposure evidence
→ VerificationResult
→ ResultMaturity
→ EffectBoundary = NO_EFFECT
→ Basis/currentness revalidation
→ PublicationDecision
→ AskResult
```

---

# 20. ModelAccessPort / ModelAccessRuntime

Application-owned port:

```text
ModelAccessPort.invoke(ModelInvocationRequest, CancellationSignal)
    -> ModelInvocationResult

ModelAccessPort.stream(ModelInvocationRequest, CancellationSignal)
    -> AsyncIterator[ModelEvent]
```

The first public Ask surface is non-streaming. Internal provider streaming remains behind verification/publication.

`ModelInvocationRequest` binds DANTE requirements:

```text
Work/Invocation identity
ModelTarget
ConsumerContext projection
HarnessProfile requirement
feature mode/capability projection
structured-output requirement where used
execution deadline
RouteConfigIdentity/snapshot
security/data eligibility basis
```

Provider background/stored/continuation/tool modes are OFF for the first slice unless separately qualified.

---

# 21. Private ProviderAdapter

`ModelAccessRuntime` resolves one eligible qualified route and allocates a DANTE `ProviderAttemptId` before dispatch.

Private contract:

```text
ProviderAdapter.invoke(ProviderAttemptRequest) -> ProviderAttemptResult
ProviderAdapter.stream(ProviderAttemptRequest) -> AsyncIterator[ProviderRuntimeEvent]
ProviderAdapter.cancel(ProviderAttemptId) -> CancellationOutcome
```

`ProviderAttemptRequest` includes only resolved private mechanics:

```text
attempt_id
provider binding/model/deployment locator
feature mode
normalized input projection
structured-output/tool transport projection when applicable
deadline / cancellation mechanism
route-config material identity
HarnessProfile identity
```

The adapter does not own:

```text
routing
Auth/AuthZ/Consent/Visibility
provider egress authorization
Effects
DB access
commercial entitlement
```

Normalized result/evidence distinguishes:

```text
completed
refused
pre-acceptance failure
ambiguous acceptance / outcome unknown
cancel requested
cancel confirmed
execution quiesced
usage known
usage estimated
usage unknown
late usage evidence
```

Provider IDs are correlation/evidence only.

---

# 22. Provider/application error taxonomy

## 22.1 Application-level taxonomy

At minimum:

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

## 22.2 Provider-adapter taxonomy

At minimum:

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

`IndeterminateExternalOutcomeError` means DANTE cannot prove whether the provider accepted/processed the attempt.

It is never blindly retried unless the exact selected operation has independently proven safe idempotent retry semantics.

## 22.3 First HTTP mapping posture

```text
invalid request                 -> 400/422 boundary validation
stale basis / precondition      -> 409 when safe to disclose
policy denied                   -> 403 only when denial itself is disclose-safe
capability unavailable          -> 503
provider transient/rate-limit   -> 503 or bounded mapped service error
provider permanent/bad gateway  -> 502
provider outcome indeterminate  -> 502/503 with no unsafe duplicate attempt
deadline exceeded               -> 504
client cancellation             -> publication may be impossible if client is gone
isolation execution failure     -> unreachable in first envelope
```

Hidden/existence-sensitive cases may intentionally return filtered/empty semantics instead of a revealing denial/error.

---

# 23. Provider candidate lifecycle / qualification

Do not call an unqualified candidate “selected for production”.

Sequence:

```text
P0 candidate discovery / shortlist
P1 candidate admission for qualification
P2 inactive material ProviderAdapter/ProviderBinding implementation
P3 adapter conformance
P4 live compatibility / feature proof
P5 direct DANTE eval using production-owned material composition
P6 capacity/reliability/security/privacy/economics evidence as applicable
P7 qualification decision
P8 canary/production promotion when all gates pass
```

## 23.1 Candidate admission

A reviewed candidate-admission artifact may justify adding one SDK/protocol dependency for qualification based on:

```text
current API/SDK compatibility
required feature semantics
preliminary data/region/retention eligibility
preliminary economics
adapter complexity
explicit direct-eval plan
known unsupported behavior
```

Candidate admission is not route eligibility.

## 23.2 Qualification traffic is real disclosure

A provider candidate is a real external data recipient whenever payload crosses its boundary.

```text
"ONLY AN EVAL"
!= FREE DISCLOSURE
```

Before private/sensitive data eligibility is established, use:

```text
synthetic fixtures
public/non-sensitive fixtures
purpose-built minimized fixtures
provider sample payloads
```

for adapter live compatibility and direct DANTE quality work where sufficient.

Real private/sensitive data may be used only after the applicable legitimate purpose, processor/data-flow, security/privacy, consent/legal-basis and audit/evidence gates are satisfied.

Shadow/canary traffic is also real disclosure.

## 23.3 Production qualification

Promotion requires the same material composition intended for production or independent proof for every material delta.

Required evidence includes as applicable:

```text
adapter conformance
live compatibility
DANTE-E applicable direct evals
security/privacy/data eligibility
capacity/reliability
usage/cost evidence
route/config identity
retry/fallback composition
```

Direct eval failure blocks promotion.

---

# 24. Provider adapter conformance

Every admitted adapter proves, for claimed feature modes:

```text
normal finalized response
rate limit
pre-acceptance network failure
timeout before acceptance known
timeout after acceptance possible / ambiguous submit
invalid structured response
stream disconnect
cancel before dispatch
cancel in flight
cancel/completion race
usage present
usage absent
unsupported requested feature
provider refusal
```

Application fakes remain distinct from provider conformance fixtures.

Conformance proves protocol normalization only; it does not prove model quality, production data eligibility or production capacity.

---

# 25. Retry / fallback / cancellation / cumulative disclosure

## 25.1 Safe retry

```text
safe transient pre-acceptance failure
→ bounded retry MAY be allowed

possible accepted/processed state + lost response
→ OUTCOME UNKNOWN
→ establish/reconcile before replay
```

No blind provider failover request replay.

Provider refusal is not infrastructure failure and cannot trigger refusal-shopping.

## 25.2 Alternate route rebuild

Fallback re-evaluates:

```text
current provider/data eligibility
current Work/purpose/currentness
alternate HarnessProfile/ProviderBinding compatibility
alternate capability/context envelope
request-local prior EgressAttempts/exposure occurrences
cumulative disclosure to known recipients/sinks
resource admission
retry/fallback qualification
```

The alternate route rebuilds/minimizes `ConsumerContext`; it does not replay the previous provider request blob blindly.

## 25.3 Hedging

Server-side multi-provider hedging is OFF by default for the first route.

```text
MULTI-PROVIDER HEDGING
!= LATENCY-ONLY OPTIMIZATION
```

It requires explicit privacy/security/cost/operational/qualification evidence because it can intentionally disclose one Work to multiple recipients.

## 25.4 Cancellation

```text
cancel requested
!= cancel confirmed
!= execution quiesced
```

Client disconnect closes recipient publication but does not rewrite already-crossed egress or provider-attempt truth.

---

# 26. Route configuration / material identity

Behavior-bearing route configuration is static/versioned/typed first.

Target source:

```text
apps/backend/config/intelligence/revisions/<revision>.json
```

Validated into frozen typed config models.

`RouteConfigIdentity` binds:

```text
logical revision
content digest
```

A loaded invocation snapshot binds exact validated bytes.

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
resource estimate/limit definitions where applicable
security/control profile references
rollout state / qualification refs where applicable
```

Secrets are not config payload.

Deployment settings may provide only appropriate deployment concerns:

```text
approved active config selector
provider endpoint/deployment locator
region/environment endpoint
credential/secret reference
approved emergency/kill selector
resource/environment limits
```

They cannot become a hidden behavior-policy language.

```text
ACTIVE POINTER != IMMUTABLE CONFIG REVISION
COHERENT INVOCATION CONFIG != PERPETUAL AUTHORIZATION
COHERENT INVOCATION CONFIG != IMMUNITY FROM EMERGENCY DENY
```

CI/build/packaging must prove the qualified config bytes are the bytes delivered to runtime or independently qualify material deltas.

---

# 27. Policy consumer seam

Intelligence does not own Authority/AuthZ/Consent/Visibility truth.

Method-specific consumer seam:

```text
authorize_context_exposure(...)
authorize_model_egress(...)
authorize_effect(...)
authorize_publication(...)
```

`PolicyDecision` preserves:

```text
ALLOW / DENY
policy/control basis identity
resolved principal/recipient/surface
purpose
obligations/disclosure constraints
revalidation requirement
internal reason code
```

A policy denial may be internally typed while the external surface returns a non-revealing result where disclosure safety requires it.

The Access/Auth product vertical is not integrated on this branch, therefore:

```text
NO X-User-Id temporary production bypass
NO fake-auth public route
NO Intelligence-owned parallel authorization truth
```

Tests may construct explicit synthetic trusted contexts. Production private-data activation waits for authoritative integrated Auth/AuthZ.

---

# 28. Resource admission / settlement seam

Candidate consumer methods:

```text
estimate(ResourceEstimateRequest) -> ResourceEstimate
admit(ResourceAdmissionRequest) -> ResourceAdmission
settle(ResourceSettlementRequest) -> ResourceSettlement
```

Intelligence requests resource decisions; it does not own shared/commercial durable accounting.

Flow:

```text
estimate bounded route exposure
→ admit/reserve where a real shared authority exists
→ execute
→ collect actual usage evidence
→ settle/reconcile late or unknown usage
```

Binding:

```text
UNKNOWN USAGE != ZERO USAGE
ESTIMATE != FINAL COST
PROVIDER TOKEN != COMMERCIAL CREDIT
COMMERCIAL QUOTA != PROVIDER QUOTA != PLATFORM CAPACITY
```

First technical slice may be unmetered only when no shared/commercial policy exists.

If shared/monthly/commercial quota becomes an eligibility condition, activation waits for the proper durable owner/accounting state.

Safety/reconciliation work already required cannot be blocked merely because optional commercial quota is exhausted.

---

# 29. Verification contract

Pure/request-local `VerificationResult` prevents raw model output from becoming publishable by convention.

Conceptual statuses:

```text
VERIFIED
LIMITED
CONFLICTED
STALE
REJECTED
INSUFFICIENT_EVIDENCE
NEEDS_REREAD
```

Preserves as applicable:

```text
claim/source bindings
coverage/grounding limitation
source-standing limitation
basis/currentness
contradiction/conflict
required reread/abstention reason
```

Verification prefers deterministic/application evidence when available.

A model verifier, if activated later, is a governed consumer/data recipient and is not canonical truth.

```text
MODEL CLAIM "DONE" != DOMAIN COMPLETION
```

---

# 30. Effect boundary / transaction rule

Application-owned consumer contract:

```text
EffectBoundary.finalize(
    WorkContract,
    proposed_effects,
    current_policy_basis,
) -> EffectOutcome
```

First vertical:

```text
WorkContract.ConsequenceProfile = READ_ONLY
proposed_effects = []
→ EffectOutcome.NO_EFFECT
```

Any mutation intent in this envelope:

```text
→ REJECT
→ no mutation adapter invoked
→ no canonical mutation transaction opened
```

Future consequential effects must reuse owning application mutation semantics and outer transaction ownership.

```text
outer application/effect operation owns commit/rollback
persistence adapters may flush, never implicit commit
no PostgreSQL business transaction spans provider/network execution
provider/external outcome not atomically rollbackable with PostgreSQL
ambiguous consequential external outcome creates reconciliation obligation
```

---

# 31. Publication contract

`PublicationDecision` is distinct from Verification and provider completion.

Immediately before public response emission it rechecks as applicable:

```text
current Work/supersession
current Auth/AuthZ/Consent/Visibility
recipient + surface
Disclosure Projection / sensitivity
request-local cumulative disclosure when material
ResultMaturity
VerificationResult
Basis/currentness
policy / emergency deny
```

Conceptual outcomes:

```text
ALLOW
ALLOW_WITH_LIMITATION
DENY
STALE_SUPPRESSED
NOT_CURRENT
```

`AskResult` is created only after safe publication.

First public Ask is non-streaming.

If external streaming is later activated, every emitted delta is a publication event and receives its own proof gate.

---

# 32. RuntimeEvidencePort / audit / evidence planes

Typed `RuntimeEvidencePort` accepts a closed/typed event union for the materialized vertical.

Minimum event families may include:

```text
WorkLifecycleEvidence
SearchEvidence
SemanticQueryEvidence
ReferenceResolutionEvidence
ContextReadinessEvidence
BasisRevalidationEvidence
PolicyBoundaryEvidence
RouteDecisionEvidence
ResourceEvidence
ProviderAttemptEvidence
EgressExposureEvidence
VerificationEvidence
EffectBoundaryEvidence
PublicationEvidence
```

Default operational telemetry excludes:

```text
raw private prompt/body
raw ConsumerContext
raw hidden Search content
raw model response
secrets/credentials
```

Evidence planes remain distinct:

```text
CANONICAL DOMAIN DATA
!= AUDIT/EXECUTION EVIDENCE
!= OPERATIONAL TELEMETRY
!= EVAL/QUALIFICATION EVIDENCE
```

If a sensitive access/provider-egress case requires durable audit under current Product/security/privacy policy, that production case remains ineligible until a proper durable audit owner/integrity/retention/access contract is materialized.

Telemetry is never silently promoted to audit.

---

# 33. Query coherence / PostgreSQL isolation

Database default remains `READ COMMITTED`.

Every Search/semantic query family declares:

```text
maximum truthful guarantee
coherence requirement
snapshot requirement
currentness rule
```

For a guarantee requiring one coherent snapshot across multiple values, use the least-complex valid method:

```text
single SQL statement / CTE
or
explicit per-operation stronger isolation such as REPEATABLE READ
or
another accepted owner/material-basis mechanism proving coherence
```

No global isolation escalation is authorized by AI.

A family unable to establish required coherence downgrades/labels the guarantee.

Permission-safe eligibility is applied before protected aggregate/rank/count/facet semantics.

---

# 34. Runtime / persistence classification

## 34.1 Request-local / no-store by default

```text
WorkContract
RunId/request execution state
ContextPlan
InformationNeed
ContextStrategy
ReferenceResolution request/result
SemanticQuery runtime request/outcome
RetrievalPlan
RetrievalCandidate
ContextFragment
ContextReadiness
ConsumerContext
ContextManifest
BasisManifest
Search request/result/page
PolicyDecision ordinary read request
ResourceAdmission unmetered/request-local
ModelInvocation request/result
ProviderAttempt runtime
EgressAttempt/request-local exposure accounting
VerificationResult
EffectOutcome.NO_EFFECT
PublicationDecision/Result
```

## 34.2 Durable noncanonical evidence/artifact when justified

```text
route/config revisions → Git/release artifact
qualification evidence → CI/release evidence store
operational telemetry → observability backend
security/audit evidence → only when independently required with own retention/integrity
```

## 34.3 Persist only on independent trigger

```text
conversation/session continuity
Run registry/durable resume
AI memory
Context cache
cross-Run prior-disclosure accounting
commercial/shared usage ledger
idempotency/saga/reconciliation state
background/durable Work
async invalidation jobs
vector/embedding representations
```

No generic AI persistence is justified by this baseline.

---

# 35. Lifecycle matrix

| Object | Create | Persist first vertical | Mutate/version | Release/expire | Cache/reuse | Retry/cancel |
|---|---|---|---|---|---|---|
| `WorkContract` | trusted request intake | no | immutable; derive/supersede on material change | request end | no cross-request default | same protected contract only when still current |
| `ContextPlan` | Ask planning | no | explicit new version/replan | request end | no initially | rebuild on bounded stale/unresolved case |
| `InformationNeed` | ContextPlan/work/policy/capability | no | explicit status transition/new need under ceiling | request end | no | reacquire/clarify according to state |
| `ContextStrategy` | per need | no | replace by explicit new strategy | request end | no | bounded strategy replan |
| `ReferenceResolutionResult` | per resolution need | no | immutable | request end | no stale reuse | rerun after material source/authority change |
| `SemanticQueryOutcome` | per structured query | no | immutable | consumer/request end | no semantic cache default | DB/source retry only under policy |
| `RetrievalPlan` | per need | no | explicit replacement | request end | no | bounded by plan/deadline |
| `RetrievalCandidate` | acquisition | no | immutable | after validation/request end | no | reacquire after stale/source change |
| `ContextFragment` | after candidate/source validation | no | immutable representation | request end | no default | reacquire/revalidate rather than mutate truth |
| `ContextReadiness` | after coverage/coherence check | no | recompute after plan/context change | request end | no | recompute |
| `ConsumerContext` | before one consumer call | no | new projection on material change | consumer/request end | no provider-independent reuse by default | rebuild for alternate route |
| `ContextManifest` | at/after material consumer exposure | no | append/update request-local exposure evidence as needed | request end | no | not retry authority |
| `BasisManifest` | while assembling material dependencies | no | new manifest/revision after reread | request end | no | stale -> reread/rebuild |
| `PolicyDecision` | each enforcement boundary | no ordinary first slice | immutable | request end | never reuse after material change | re-evaluate |
| `RouteConfigSnapshot` | before invocation | config revision durable externally | immutable snapshot | request end; revision retained | exact-revision process cache permitted | material delta requires qualification |
| `ProviderAttempt` | each outbound attempt | no canonical persistence | immutable attempt state/evidence | request end; telemetry separate | no | retry creates new attempt id; cancel states explicit |
| `EgressAttempt` | each material provider send | no first vertical | request-local state transition | request end | no | every retry/fallback creates/evaluates new egress attempt |
| `ResourceAdmission` | before resource-consuming attempt | no first unmetered slice | immutable decision | request end | no | new admission for material route attempt |
| `VerificationResult` | per candidate answer/result | no | immutable | request end | no | reverify after material basis change |
| `EffectOutcome` | effect boundary | no read-only slice | immutable | request end | no | future consequential retry governed independently |
| `PublicationDecision` | immediately before publication | no | immutable | response end | no | reevaluate, never replay authority |
| route config revision | reviewed change | Git/release artifact | immutable new revision | retention policy | exact identity only | n/a |
| qualification artifact | qualification run | evidence store | immutable artifact/new run => new id | evidence retention | n/a | n/a |

Any future survival proposal re-enters AI-03C materiality/lifecycle rules.

---

# 36. Pending direct-proof register

The implementation/release evidence ledger preserves pending obligations.

| Proof | Trigger | Initial status |
|---|---|---|
| PSV-06 / SC-017 hidden-result non-interference | first protected Search/structured query/reference-resolution family | PENDING when applicable |
| PSV-07 / SC-018 FTS mixed filter/query | PostgreSQL FTS/pg_trgm serving | N/A until activated |
| PSV-08 / SC-019 vector filtered recall/relevance | ANN/vector serving | N/A until activated |
| PSV-09 / SC-020 projection freshness/material basis | served derived/current projection | PENDING when applicable |
| PSV-10 / SC-021 deletion/redaction propagation | surviving derived representation/index | PENDING when applicable |
| PSV-21..28B durable/Restate proofs | Class-B durable execution | N/A until activated |
| PSV-37 pgvector provenance | pgvector/embedding serving | N/A until activated |

`N/A` requires an explicit absent capability/feature-mode reason.

```text
missing evidence != N/A
```

Provider/eval evidence remains separately required.

---

# 37. Qualification artifact schema

Every promotable route composition has immutable qualification evidence containing at least:

```text
schema_version
qualification_id
created_at
git_sha
release/build identity
route_config_revision + digest
ModelTarget identity
HarnessProfile identity
ProviderBinding identity
ProviderAdapter identity/version
feature mode
policy/control revisions
security/data transformation revisions
retry/fallback/hedging composition
DANTE eval suite/version
applicable DANTE-E01..E14 cases + hard-gate results
SC/PSV applicability/status register for activated mechanisms
provider conformance evidence ref
live compatibility evidence ref where required
qualification-fixture/data-class disclosure classification
capacity/reliability evidence ref where required
privacy/security/data eligibility evidence
cost/usage evidence
material deltas from prior qualification
revalidation/expiry conditions
qualification decision
promotion status
```

No blanket `PASS` may hide skipped applicable cases.

Qualification artifacts distinguish:

```text
candidate admission
qualification pass/fail
production promotion status
```

---

# 38. Test topology

Target tests extend the existing backend gate.

```text
apps/backend/tests/unit/modules/search/
→ Search contracts/registry/guarantees/non-interference pure cases

apps/backend/tests/unit/modules/intelligence/
→ WorkContract
→ ContextPlan/InformationNeed/ContextStrategy
→ RealityScope/RuntimeInterpretationFrame
→ ReferenceResolution + non-interference
→ SemanticQueryGateway
→ RetrievalPlan/RetrievalCandidate validation
→ DATA != INSTRUCTION
→ ContextReadiness/ConsumerContext/ContextManifest/BasisManifest
→ Policy/Resource/Effect
→ Verification/Publication
→ request-local EgressAttempt/cumulative disclosure
→ deterministic ModelAccess fake
→ cancellation/deadline/error taxonomy

apps/backend/tests/unit/test_architecture_boundaries.py
→ import/dependency/provider/eval/DB authority boundaries

apps/backend/tests/integration/modules/search/
→ real PostgreSQL Search family tests
→ permission non-interference
→ guarantee/coherence/isolation behavior

apps/backend/tests/integration/modules/intelligence/
→ Search public seam
→ real semantic query handlers as they become real
→ reference resolution with hidden candidates
→ stale basis / Auth change / source retirement
→ fake ModelAccess composition
→ route-config snapshot
→ retry/fallback/request-local exposure accounting

apps/backend/tests/integration/providers/<binding>/
→ adapter conformance after candidate admission

tooling/ai-evals/
→ direct qualification using production-owned composition
→ synthetic/minimized fixtures until real-data eligibility exists

tests/system/
→ black-box Search/Ask only after real Auth/HTTP integration
```

Mandatory targeted fixtures include:

```text
ambiguous target candidates
hidden same-name target candidate
mutate-after-fixture stale basis
relative date/time + timezone/DST
hidden result affecting count/facet/rank/aggregate
multi-statement concurrent write/coherence
malicious retrieved instruction/source
query-rewrite scope expansion
source retirement/redaction after retrieval
provider rate limit/timeout/invalid schema/disconnect/ambiguous submit/cancel race
provider timeout after material send with exposure independent from completion
provider conformance PASS but direct-eval FAIL promotion attempt
live qualification before private-data eligibility uses synthetic/minimized fixture
fallback after prior possible provider exposure
alternate-provider context contraction/rebuild
multi-provider hedging disabled
sensitive request with missing durable audit capability
```

Existing CI remains:

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

Provider/direct-eval/capacity/privacy evidence adds to, never replaces, normal CI.

---

# 39. Architecture test obligations

Automated architecture checks must prove at least:

```text
Search does not import Intelligence
Intelligence imports Search only via Search public/contracts
Intelligence does not import Search private PostgreSQL adapter
Intelligence/application does not import SQLAlchemy/DB mappings
SemanticQueryGateway cannot expose raw SQL/table/ORM authority
ReferenceResolver cannot query unrestricted hidden universe then leak ambiguity
provider SDK imports only in admitted private binding adapter
ProviderAdapter cannot import inbound HTTP schemas or DB runtime/mappings
production cannot import tooling/ai-evals
HTTP DTOs cannot carry Authority/AuthZ/provider/effect authoritative fields
no generic Repository[T]
no universal EntityRef/entity_id
no model-generated SQL/ORM execution path
bootstrap contains composition, not orchestration
runtime telemetry cannot masquerade as audit
```

---

# 40. Dependency / framework lock

Initial allowed dependency direction:

```text
FastAPI/Pydantic existing inbound/config boundaries
SQLAlchemy/psycopg existing PostgreSQL infrastructure
stdlib internal contracts/orchestration where sufficient
one admitted provider SDK/protocol only inside private provider adapter after P1
```

Forbidden unless explicitly reopened by evidence:

```text
LangChain/LangGraph-style orchestration ownership
agent framework as DANTE semantic owner
provider gateway as mandatory data path
MCP framework for ordinary first vertical
new vector/search database
generic Repository/UoW framework
ORM/model-to-SQL tool
unreviewed dynamic control-plane database
```

MCP/A2A/client SDKs, when later activated, remain inside corresponding capability/infrastructure adapters and never become core application semantics.

---

# 41. Feature / activation gates

| Capability | Build posture | Activation requirement |
|---|---|---|
| Search contracts/shell | BUILD-READY after final mega PASS | no public activation claim |
| protected Search family | conditional | real data + Auth/disclosure + PSV-06/SC-017 + family tests |
| reference-resolution family over protected data | conditional | same eligible-universe/non-interference proof + typed resolver tests |
| Search HTTP | gated | authoritative integrated Auth/AuthZ context |
| structured semantic query family | conditional | owning semantics + permission/coherence proof + typed handler/tests |
| FTS/pg_trgm | OFF | measured need + DB same-change + PSV-07/SC-018 |
| vector/pgvector | OFF | eval need + lifecycle + PSV-08/SC-019 + PSV-37 + applicable freshness/deletion proofs |
| ModelAccess fake | test only | no production claim |
| provider qualification candidate | OFF | reviewed candidate admission |
| live compatibility with synthetic/minimized payload | OFF | admitted adapter + safe test-data posture |
| live private-data provider route | OFF | processor/data/security/privacy eligibility + adapter conformance/live compatibility/direct eval/capacity as applicable |
| production Ask | OFF | Auth + source/query path + provider qualification when used + verification/publication + evidence/audit/privacy gates |
| sensitive audit-required Search/Ask | OFF | minimum durable audit evidence plane exists |
| external streaming | OFF | delta-level publication/disconnect/cumulative-disclosure proof |
| server-side multi-provider hedging | OFF | explicit privacy/security/cost/operational qualification |
| consequential Effect | OFF | I9 + target/policy/approval/transaction/idempotency/reconciliation proof |
| commercial/shared ledger | OFF | real enforcement requirement |
| durable Run/Restate | OFF | real workflow lifetime trigger + PSV-21..28B |
| AI memory | OFF | explicit owner/purpose/lifecycle trigger |
| cross-Run prior-disclosure accounting | OFF | H19 real trigger |
| MCP/A2A | OFF | real capability/integration trigger |
| Execution Environment | OFF | generated/untrusted code/browser/computer-use threat-model trigger |

---

# 42. Build-ready / integration-ready / activation-ready

```text
BUILD-READY
= accepted code/contracts can be implemented with fakes/synthetic trusted contexts

INTEGRATION-READY
= required real owning seams/data/capabilities exist

ACTIVATION-READY
= user-visible path passed all applicable security/privacy/proof/ops/release gates
```

First implementation stages after final mega acceptance:

```text
I0 repository/application ownership + architecture-test skeleton
I1 Search public contracts/registry/application shell
I2 Intelligence pure contracts:
   Work/ContextStrategy/ReferenceResolution/SemanticQuery/RetrievalCandidate/
   Policy/Resource/Effect/Verification/Publication/EgressAttempt + deterministic fakes
I3 real deterministic Search/structured query families only when product data is materially ready
I4 provider candidate admission + inactive concrete adapter candidate
I5 conformance/live compatibility + direct DANTE qualification
I6 read-only Ask DANTE
I7 production hardening / observability / privacy / resource / rollout / audit as applicable
I8 scenario/planning proposal vertical
I9 first bounded consequential Effect vertical
I10 proactive/background/durable/external-agent capabilities only on real trigger
```

I0-I2 do not require production provider/Auth availability.

Public private-data Search/Ask do.

---

# 43. Implementation dependency graph

```text
B0  architecture boundary tests + pure shared value contracts needed by I0

B1  Search public contracts + SearchFamilyRegistry + pure application
    ↓
B2  bounded PostgreSQL Search adapter + real PG/non-interference/coherence tests
    ↓
B3  Search inbound adapter/wiring behind Auth activation gate

B4  Intelligence core:
    WorkContract
    ContextPlan / InformationNeed / ContextStrategy
    ReferenceResolution + non-interference
    SemanticQueryGateway + deterministic fake/no-handler posture
    RetrievalPlan / RetrievalCandidate validation
    Verification / Publication / Effect NO_EFFECT
    RuntimeEvidencePort / request-local EgressAttempt
    ↓
B5  route-config schema/loader/digest snapshot + Policy/Resource/Evidence seams
    ↓
P0  provider candidate discovery/shortlist
    ↓
P1  candidate admission artifact
    ↓
B6  one inactive candidate ProviderAdapter/ProviderBinding + dependency
    ↓
B7  adapter conformance + live compatibility on safe/minimized qualification data
    ↓
B8  tooling/ai-evals using SAME production-owned composition
    + direct DANTE qualification
    + applicable capacity/security/privacy/economic proof
    ↓
B9  qualification/promotion decision
    ↓
B10 read-only Ask HTTP surface + safe final publication
    ↓
B11 production hardening/system acceptance/activation evidence
```

A provider candidate may be rejected at P1, B7, B8 or B9 without changing DANTE application semantics.

---

# 44. Candidate commit sequence

```text
C1  test(ai): establish architecture boundary checks
C2  feat(search): public contracts, eligibility, family registry, deterministic shell
C3  feat(search): bounded PostgreSQL adapter + real PG proof for first family
C4  feat(search): inbound adapter/wiring behind Auth activation gate
C5  feat(ai): Work/ContextStrategy/ReferenceResolution/SemanticQuery/Retrieval contracts + fakes
C6  feat(ai): Policy/Resource/Verification/Publication/Effect/EgressAttempt/RuntimeEvidence contracts
C7  feat(ai): route-config identity/loader/digest snapshot
C8  chore(ai): record provider candidate-admission decision
C9  feat(ai): add admitted inactive provider adapter + conformance/live compatibility
C10 test(ai): direct DANTE qualification using production-owned composition
C11 chore(ai): record qualification/promotion decision
C12 feat(ai): read-only Ask DANTE + safe final publication
C13 test(ai): full Search/Ask system/failure/privacy/operational hardening
```

If C8 returns `DEFER/REJECT`, C9+ provider work does not proceed.

If C10/C11 fail qualification, production Ask cannot rely on that route.

No database migration commit is planned for this baseline.

---

# 45. Deferred responsibility ledger

Inactive does not mean forgotten.

```text
Interaction Session / rich continuity
→ future real multi-turn/session need
→ no generic conversation persistence now

Work Supersession across requests
→ activate with real continuing Work lifecycle

Scenario Workspace / Solver
→ I8
→ runtime/no-store default
→ OR-Tools only for real solver-backed need

Capability Runtime / ChangeSet / EffectGraph
→ I9 consequential work
→ model/provider never mutation authority

Attention / proactivity / notification
→ I10 trigger-gated
→ AttentionDecision != WorkAdmission != EffectAuthorization

Class-B durable / Restate
→ request lifetime insufficient for accepted workflow
→ PSV-21..28B required

Execution Environment
→ generated/untrusted code/browser/computer-use threat model

MCP / A2A / external-agent protocols
→ adapter/capability trigger only

AI memory persistence
→ explicit memory owner/purpose/retention/lifecycle trigger

H19 cross-Run prior-disclosure survival
→ real cross-Run/surface cumulative-disclosure trigger

FTS/vector representations
→ measured retrieval need + direct proofs
```

---

# 46. Product completeness / launch boundary

The initial technical vertical is only:

```text
Global Search subset
+ read-only Ask DANTE
```

```text
I6 COMPLETE
!= V1 GLOBAL SEARCH & COMMAND COMPLETE
```

Accepted Product V1 later includes, where scoped:

```text
creation/modification commands
preview/validation
provenance/rationale
undo/recovery where supported
scenario proposal/approval
consequential effect governance
```

For public/other-user processing, Product privacy/legal release baseline remains applicable, including as required:

```text
DPIA/governance review
processor/DPA/subprocessor posture
retention/data-flow inventory
special-category legal basis/Consent
transfer/residency safeguards
privacy notice/terms/user controls
medical-purpose boundary review
qualified privacy/legal review required by Product baseline
```

These are release/governance responsibilities, not Intelligence-owned canonical business semantics.

---

# 47. Explicit non-claims

```text
THIS V2 BASELINE ACCEPTED AFTER FINAL MEGA RETEST    NO / RETEST REQUIRED
AI-05 STRUCTURALLY CLOSED                           YES
modules/search implemented                          NO
modules/intelligence implemented                    NO
SemanticQueryGateway implemented                    NO
Auth/AuthZ integrated on this branch                NO
provider candidate admitted                         NO
provider/model/SDK production-qualified             NO
provider dependency added                           NO
direct provider eval executed                       NO
production capacity qualified                       NO
production Ask active                               NO
external streaming active                           NO
PostgreSQL/Alembic changed                          NO
new AI table/index                                  NO
FTS/trgm/vector activated                           NO
conversation persistence selected                   NO
control-plane persistence selected                  NO
commercial/resource ledger implemented              NO
Restate/R2/MCP/A2A activated                        NO
Execution Environment selected                      NO
```

---

# 48. Final acceptance gate for v2

Before this file may become `CURRENT / ACCEPTED FOR IMPLEMENTATION ENTRY`:

```text
MKT-001..MKT-090 rerun from zero
compound collision suite PASS
reverse Product→Domain→Logical→Physical→PostgreSQL→AI-02→AI-03→AI-04→PRE05→AI-05→v2 PASS
representative single-user + multi-actor simulation replay PASS
SC/PSV/eval proof applicability register internally consistent
no new Domain/Logical/Physical/PostgreSQL reopen
no generic AI persistence owner
no provider preselection
no privacy/evidence shortcut
current routing repair completed only after PASS
```

Until then:

```text
IMPLEMENTATION I0 = HOLD
```
