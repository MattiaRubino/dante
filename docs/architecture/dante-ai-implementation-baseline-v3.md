# DANTE Intelligence — Current Implementation Baseline v3

- **Status:** CURRENT POST-AI05 HARDENED CANDIDATE / FRESH MKT-001..MKT-100 REQUIRED
- **Branch:** `feature/ai-architecture`
- **Established:** 2026-09-02
- **PRE-SCOPE:** `3dcb29cc475a75b571395b931b4650589bbbe36c`
- **Upstream:** AI-05 CLOSED / STRUCTURALLY ACCEPTED
- **Post-closure hardening:** POST05-H01..H25 APPLIED
- **Implementation:** NONE
- **Provider/model/SDK:** OPEN / CANDIDATE-ADMISSION + QUALIFICATION GATED
- **Database change:** NONE
- **Alembic change:** NONE
- **Implementation entry:** HOLD UNTIL FINAL MEGA PASS

This file is the third consolidated implementation-facing candidate authority for DANTE Intelligence.

It incorporates all still-valid build substance from:

```text
AI-05A ownership/build boundary
AI-05B concrete implementation blueprint
AI05B-H01..H15
AI05-H01 readiness hardening
AI-05B / AI-05 closure contracts
POST05-H01..H25
```

Historical candidate/hardening/acceptance files remain truthful evidence of how the architecture evolved, but an implementation task must not reconstruct current build truth by patch algebra.

This file is not accepted for implementation entry until it survives:

```text
MKT-001..MKT-100 from zero
+ compound collision suite
+ reverse authority pass
+ representative Product/simulation replay
+ routing/current-truth reconciliation
```

Until then:

```text
IMPLEMENTATION I0 = HOLD
```

---

# 1. Authority and non-negotiable inheritance

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

Repository/executable truth outranks this file if future accepted implementation deliberately evolves the architecture through the normal process.

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
MASKING / REDACTION != SEMANTIC EQUIVALENCE

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

SEARCH RESULT / CURSOR / TARGET REF
!= AUTHORIZATION TOKEN

AUXILIARY MODEL INFERENCE
!= FREE PROVIDER CALL
```

---

# 2. Current repository/materialization truth

At v3 establishment, backend source remains foundation-heavy:

```text
apps/backend/src/dante/
├── bootstrap/
└── platform/
    ├── config/
    ├── database/
    └── recovery/
```

Target paths are not implementation claims:

```text
apps/backend/src/dante/modules/search
apps/backend/src/dante/modules/intelligence
tooling/ai-evals
apps/backend/config/intelligence/revisions
```

Do not create empty ceremonial directories.

Current backend dependency truth:

```text
FastAPI
Pydantic / pydantic-settings
SQLAlchemy async
psycopg
Alembic
```

No AI/provider SDK is currently accepted as a dependency.

Current database:

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

No Search/AI convenience is sufficient evidence to reopen Domain/Logical/Physical/PostgreSQL.

---

# 3. Capability ownership

## 3.1 Search

Target owner:

```text
apps/backend/src/dante/modules/search
```

Search owns:

```text
Global Search/discovery application contract
structured filters for discovery
keyword/lexical discovery when activated
current/history discovery semantics
permission-safe eligible result universe
safe snippets/facets/counts/rank/pagination
canonical/source navigation refs
SearchFamilyRegistry
bounded cross-capability read projection for Search only
Search-specific read/query scope
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

Intelligence owns orchestration for:

```text
WorkContract execution
request-local ExecutionStatus
Context planning/readiness
Reference/Target Resolution orchestration
Semantic Query / Projection orchestration
Retrieval orchestration
qualified deterministic/model route consumption
verification
ResultMaturity
Effect consumer boundary
safe publication
request-local egress exposure accounting
runtime evidence emission
```

Intelligence does not own:

```text
canonical capability/business state
Search private persistence
cross-capability arbitrary SQL
Auth/AuthZ/Consent/Visibility truth
commercial subscription/shared accounting truth
provider SDK semantics
conversation database
```

## 3.3 Provider

Provider SDK/protocol code exists only inside an admitted private outbound binding adapter.

Candidate placement:

```text
apps/backend/src/dante/modules/intelligence/adapters/outbound/models/<binding>/
```

No provider SDK type appears in public/application contracts.

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

Candidate first-vertical end-state:

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

Intelligence does not own a `search_access.py` adapter to Search private persistence. It consumes Search's public protocol.

No monolithic generic `core`, `ai`, `common`, `entity`, `repository`, `memory`, `run` or provider-owned application layer is authorized.

---

# 5. Search public contract

`modules/search/public.py` owns the Search public application protocol.

Conceptual surface:

```text
class SearchService(Protocol):
    async def search(SearchExecutionRequest) -> SearchResult: ...
    async def resolve_navigation(NavigationExecutionRequest) -> NavigationResult: ...
```

`SearchExecutionRequest` is trusted/server-constructed and carries only:

```text
user query/filter projection
SearchEligibilityEnvelope
requested SearchFamilyIds after active/eligible intersection
current/history intent
bounded page/cursor
requested guarantee
route-owned purpose/surface
Runtime Interpretation Frame where meaning requires it
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

`SearchHit` uses `SearchTargetRef`, never universal `entity_id`.

Search miss means only:

```text
NO ELIGIBLE RESULT FOUND UNDER THIS QUERY + ACCESS + GUARANTEE
```

It does not prove canonical nonexistence.

---

# 6. SearchEligibilityEnvelope and non-interference

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
practical latency/error oracle where material
```

---

# 7. Search publication/currentness, cursor and navigation

Search has a real publication/response boundary even when no model is involved.

```text
QUERY ELIGIBLE AT T1
!= AUTOMATICALLY PUBLISHABLE AT T2
```

Before emitting material private Search data, revalidate current access/source/currentness according to family/consequence requirements.

A page cursor:

```text
!= AuthZ token
!= frozen permission snapshot
!= permission to reveal rows that became ineligible
```

Each paged request constructs fresh current access/eligibility.

Cursor implementation is minimized and integrity-protected enough to prevent caller tampering from changing family/query/sort/version semantics. It must not embed hidden row content, privileged policy state or become a reusable authorization capability.

If permissions/source/currentness/query-version changes invalidate safe cursor semantics, DANTE restarts/rebases/fails safely rather than pretending continuity.

A `SearchTargetRef` is an address/navigation hint only.

Opening a canonical target re-resolves current owning-capability authorization/visibility.

```text
SEARCH RESULT ONCE VISIBLE
!= PERPETUAL NAVIGATION AUTHORITY
```

Source retirement/deletion between query and response follows family currentness/revalidation; stale data is not published as current.

---

# 8. SearchFamilyRegistry

`SearchFamilyId`, `SearchFamilyRegistration`, `SearchFamilyRegistry` are application/static contracts, not Domain identities/tables.

Each registration freezes at least:

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
publication/currentness revalidation requirement
activation evidence reference
applicable direct-proof identifiers
```

```text
SEARCH FAMILY ID != TABLE NAME
SEARCH REGISTRY != DATABASE CATALOG
SEARCH REGISTRY != GENERIC REPOSITORY
```

A family activates only when real useful product data, semantics, permission-safe universe, bounded behavior, truthful coherence/guarantee and applicable direct proof exist.

The current 69-table schema is not automatically one Search universe.

---

# 9. SearchTargetRef / navigation

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
SearchTargetRef != authorization token
```

Navigation dispatches through current owning capability semantics.

---

# 10. Semantic Query / Projection Gateway

Search discovery is not sufficient for structured DANTE questions.

Intelligence preserves `SemanticQueryGateway` as orchestration only.

Conceptual surface:

```text
SemanticQueryGateway.execute(
    InformationNeed,
    ContextStrategy,
    TrustedRequestContext,
) -> SemanticQueryOutcome
```

Allowed sources:

```text
owning capability public typed query contract
or
explicitly accepted capability-owned read projection
```

Search's cross-capability read projection is Search/discovery-specific and is not an analytics backdoor.

`SemanticQueryGateway` cannot accept or own:

```text
raw SQL
ORM classes
table names
arbitrary model predicates
AsyncSession/database mappings
cross-capability private persistence adapters
```

If no owning/public typed query seam exists:

```text
SemanticQueryOutcome = UNSUPPORTED / NOT_INTEGRATION_READY
```

not a direct DB bypass.

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

Correct deterministic path:

```text
question
→ bounded semantic interpretation
→ InformationNeed
→ ContextStrategy.DETERMINISTIC_AGGREGATION / STRUCTURED_CURRENT_QUERY / ...
→ SemanticQueryGateway
→ owning capability query
→ typed result
→ VerificationResult
→ safe publication
```

No model is required merely to calculate a deterministic answer DANTE already owns.

If model assistance is used for interpretation, it is a first-class governed model invocation through the normal ModelAccess path; it does not receive SQL authority.

---

# 11. Reference / Target Resolution

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

```text
MODEL CONFIDENCE != REFERENCE RESOLUTION
DISPLAY NAME != CANONICAL TARGET
```

## 11.1 Reference-resolution non-interference

Candidate generation/resolution operates over the eligible universe before externally observable:

```text
RESOLVED
AMBIGUOUS
NOT_FOUND
candidate count
candidate labels
clarification options
rank/confidence clue
```

Hidden candidates do not create visible ambiguity.

```text
AMBIGUOUS IN ALL DATA
!= AMBIGUOUS IN ELIGIBLE DATA
```

Direct hidden-result proof coverage applies to material resolver families.

If model assistance is used for resolution, it is routed through the same governed ModelAccess/egress/resource/eval contracts as any other model inference.

---

# 12. WorkContract / ExecutionStatus / ResultMaturity

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

Request-local `ExecutionStatus` includes at least:

```text
ACCEPTED
RUNNING
COMPLETED
FAILED
CANCELLATION_REQUESTED
CANCELLED
SUPERSEDED
```

These are runtime states, not Domain Actual/Outcome.

`ResultMaturity` includes at least:

```text
PROVISIONAL
VERIFIED
PUBLISHABLE
REJECTED
```

```text
PROVIDER COMPLETED
!= VERIFIED
!= PUBLISHABLE
```

`PUBLISHABLE` is reached only after applicable verification/currentness/disclosure/publication checks.

`RequestExecutionScope` owns:

```text
deadline
attached tasks
CancellationSignal
active ProviderAttemptIds
request-local EgressAttempts/exposure state
publication-open/closed
bounded cleanup state
```

Client disconnect may close publication while bounded in-process cleanup/correlation continues to the execution deadline.

Process-crash survival is a separate durability trigger.

---

# 13. Full Context contract projection

Preserve all seven AI-03A Context contracts:

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

## 13.1 ContextPlan

Preserves as applicable:

```text
WorkContract ref/revision
objective/purpose
Principal/Actor/represented party
Reality Scope
Runtime Interpretation Frame
known target bindings
reference-resolution requirements unresolved
protected InformationNeeds
explicit exclusions / forbidden source/use
security/privacy compartment
resource constraints
InformationNeed set
```

## 13.2 InformationNeed

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

Statuses include:

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

```text
UNRESOLVED != UNBOUNDED
MODEL_DISCOVERED NEED != PURPOSE/SCOPE EXPANSION
```

## 13.3 ContextStrategy

Strategy is explicit per need and selects the least-complex valid route.

Relevant strategy families:

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

Only required first-vertical subsets activate.

## 13.4 Reality Scope

```text
CANONICAL_CURRENT
MATERIAL_HISTORICAL / AS_OF
SCENARIO <workspace> when activated
OPEN_WORLD_ASSERTION when activated
explicit MIXED only when legitimate
```

No cross-frame laundering.

## 13.5 Runtime Interpretation Frame

Where meaning depends on it:

```text
reference instant
applicable timezone/offset
source/target timezone where distinct
calendar/day-boundary semantics
DST resolution when ambiguous
locale/unit/calendar interpretation
spatial anchor/source/time/precision where material
```

Relative language cannot use accidental server-local wall-clock assumptions.

---

# 14. Retrieval contract

When acquisition is required:

```text
InformationNeed
→ ContextStrategy
→ RetrievalPlan
→ acquisition route
→ RetrievalCandidate
→ validation
→ ContextFragment
```

## 14.1 RetrievalPlan

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

Any model-based rewrite/decomposition is an auxiliary governed model call.

## 14.2 Retrieval guarantees

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

## 14.3 RetrievalCandidate

Candidate discovery state preserves enough to validate:

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

Validation states include:

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

Only surviving material becomes `ContextFragment`.

---

# 15. Source standing / instruction provenance / transformations

Every Context representation preserves enough metadata to keep distinct:

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

Harness/provider projection preserves role separation instead of flattening all text into one instruction channel.

Instruction provenance survives transformations where material.

## 15.1 Masking/redaction/output transformation

```text
MASKING / REDACTION
!= SEMANTIC EQUIVALENCE
```

If an input transformation changes materially relevant target/reference/context meaning, ContextReadiness/verification must consume the transformed semantics actually sent to the provider rather than pretending the original and transformed payload are equivalent.

If output DLP/redaction/transformation materially changes a verified result, the final recipient representation must be rechecked for meaning/currentness/disclosure and may require re-verification/limitation.

```text
VERIFY ORIGINAL MODEL TEXT
→ MATERIAL OUTPUT TRANSFORM
→ PUBLISH WITHOUT RECHECK
```

is not accepted.

An external guard/security/DLP service is itself a governed data recipient and must be eligible for the data it receives.

```text
GUARDRAIL RESULT != DANTE AUTHORITY
```

---

# 16. ContextReadiness / ConsumerContext / ContextManifest / BasisManifest

`ContextReadiness` outcomes include:

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

`ConsumerContext` is minimized consumer-specific context.

```text
CONSUMER CONTEXT != ALL RETRIEVED DATA
```

`ContextManifest` records established or conservatively possible consumer/provider exposure at the material send boundary according to evidence.

Provider success is not required for exposure to exist.

`BasisManifest` tracks material dependencies/currentness/coherence used to justify the result.

```text
ContextManifest != BasisManifest
```

No generic persistence is created for either in the first vertical.

---

# 17. Request-local provider egress / exposure accounting

Every material outbound provider/helper/guard model attempt creates request-local `EgressAttempt` state before/at the send boundary.

Conceptual fields:

```text
egress_attempt_id
work_id / invocation_id
ProviderAttemptId
recipient/provider binding
purpose
ConsumerContext/projection identity
Disclosure/egress policy basis
material send state
acceptance certainty where knowable
exposure occurrence: NOT_SENT | POSSIBLE | ESTABLISHED
provider outcome state
```

Examples:

```text
connection fails before data leaves DANTE
→ exposure = NOT_SENT

request handed to transport/provider may have accepted
→ exposure = POSSIBLE or ESTABLISHED according to evidence

provider completed
→ exposure = ESTABLISHED
```

```text
provider result timeout/failure
!= exposure did not occur
```

Exact send evidence is adapter/protocol specific but normalized into DANTE semantics.

State is request-local for the first vertical; it is not cross-Run prior-disclosure persistence.

---

# 18. Intelligence public contract

`modules/intelligence/public.py` owns:

```text
class IntelligenceService(Protocol):
    async def ask(AskExecutionRequest) -> AskResult: ...
```

`AskExecutionRequest` is trusted/server-constructed:

```text
WorkContract
trusted RequestContext
user question/scope projection
execution deadline
```

It cannot accept caller-selected provider/model/route/Effect authority.

`AskResult` exists only after verification + safe publication.

It may expose:

```text
safe work correlation
answer or declared limitation/abstention
safe sources/provenance
safe currentness/basis summary
model-assisted boolean
```

It is never the raw provider result and does not expose raw provider/security/policy internals merely because they exist.

---

# 19. HTTP trust boundary

```text
HTTP JSON
→ structural validation
→ authentication
→ route-owned purpose/surface
→ current Authority/AuthZ/Visibility/Consent projection
→ trusted RequestContext / SearchEligibilityEnvelope
→ WorkContract / application request
```

Client cannot supply:

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

Candidate routes:

```text
POST /api/v1/search
POST /api/v1/ask
```

Private-data activation waits for authoritative integrated Auth/AuthZ.

---

# 20. First-vertical execution routes

## 20.1 Deterministic Search

```text
HTTP Search
→ trusted SearchExecutionRequest
→ SearchService
→ eligible Search family
→ bounded PostgreSQL/read source
→ guarantee/coherence/source/currentness projection
→ final Search publication/current-access revalidation as required
→ safe SearchResult
```

No model/provider dependency.

## 20.2 Deterministic semantic question

```text
HTTP Ask
→ WorkContract
→ ContextPlan / InformationNeed
→ ReferenceResolution where required
→ ContextStrategy = structured/deterministic
→ SemanticQueryGateway
→ owning capability typed query
→ typed deterministic result
→ VerificationResult
→ EffectBoundary = NO_EFFECT
→ publication/currentness revalidation
→ AskResult
```

No model/provider call when unnecessary.

## 20.3 Model-assisted read-only Ask

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
→ current context/provider egress policy
→ eligible qualified route
→ Resource admission
→ request-local cumulative-disclosure/egress evaluation
→ ModelAccessPort
→ EgressAttempt + ContextManifest exposure evidence
→ VerificationResult
→ ResultMaturity
→ EffectBoundary = NO_EFFECT
→ Basis/currentness revalidation
→ output transformation/DLP if any + semantic recheck
→ PublicationDecision
→ AskResult
```

---

# 21. ModelAccessPort / ModelAccessRuntime

Application-owned port:

```text
ModelAccessPort.invoke(ModelInvocationRequest, CancellationSignal)
    -> ModelInvocationResult

ModelAccessPort.stream(ModelInvocationRequest, CancellationSignal)
    -> AsyncIterator[ModelEvent]

ModelAccessPort.cancel(ProviderAttemptId)
    -> CancellationOutcome
```

First public Ask is non-streaming. Internal provider streaming remains behind verification/publication.

`ModelInvocationRequest` binds:

```text
Work/Invocation identity
ModelTarget
ConsumerContext projection
HarnessProfile requirement
feature mode/capability projection
structured-output requirement where used
execution deadline
retry budget
RouteConfigIdentity/snapshot
security/data eligibility basis
```

`ModelInvocationResult` preserves:

```text
ProviderAttemptId / attempt summary
completion/outcome state
structured response payload
usage evidence
provider capability usage
finish/stop classification
acceptance uncertainty
provider timestamps/latency evidence
classified error when not completed
```

Provider SDK/protocol IDs remain correlation/evidence, not DANTE semantic identity.

Provider background/stored/continuation/native-tool/cache modes are OFF for the first slice unless separately qualified.

---

# 22. Auxiliary model inference

Every model inference is first-class governed inference, including:

```text
NL intent interpreter
reference resolver helper
query rewrite/decomposition model
router model
reranker model
summarizer
verifier/judge
advisor/sub-inference
```

If activated, every such call uses:

```text
bounded WorkContract/derived work meaning
consumer-specific Context/ConsumerContext
current provider/data eligibility
ModelAccessPort / ModelAccessRuntime
RouteConfigIdentity
Resource admission
EgressAttempt / exposure accounting
ProviderAttempt evidence
applicable direct-eval/qualification evidence
```

No helper imports/calls provider SDK directly.

```text
"ONLY A ROUTER / VERIFIER / REWRITE MODEL"
!= FREE PROVIDER CALL
```

The first implementation may keep all helper-model features OFF and use deterministic/application logic.

---

# 23. Private ProviderAdapter

`ModelAccessRuntime` resolves one eligible qualified route and allocates DANTE `ProviderAttemptId` before dispatch.

Private contract:

```text
ProviderAdapter.invoke(ProviderAttemptRequest) -> ProviderAttemptResult
ProviderAdapter.stream(ProviderAttemptRequest) -> AsyncIterator[ProviderRuntimeEvent]
ProviderAdapter.cancel(ProviderAttemptId) -> CancellationOutcome
```

Request includes only resolved private mechanics:

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

Adapter does not own routing, Authority/AuthZ/Consent/Visibility, egress authorization, Effects, DB access or commercial entitlement.

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

---

# 24. Error taxonomy

## 24.1 Application-level

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

## 24.2 Provider-adapter

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

`IndeterminateExternalOutcomeError` means DANTE cannot prove whether provider accepted/processed the attempt.

No blind retry unless exact safe idempotent semantics are proven.

## 24.3 First HTTP mapping posture

```text
invalid request                 -> 400/422
stale basis / precondition      -> 409 when disclose-safe
policy denied                   -> 403 only when disclose-safe
capability unavailable          -> 503
provider transient/rate-limit   -> 503 or bounded mapped service error
provider permanent/bad gateway  -> 502
indeterminate external outcome  -> 502/503 without unsafe duplicate attempt
deadline                        -> 504
client cancellation             -> response may be impossible if client is gone
isolation failure               -> unreachable in initial envelope
```

Hidden/existence-sensitive cases may intentionally return filtered/empty/safe limitation semantics rather than revealing internal denial reason.

---

# 25. Provider candidate lifecycle / qualification

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

## 25.1 Candidate admission

Reviewed admission artifact may justify one SDK/protocol dependency for qualification based on:

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

## 25.2 Qualification traffic is real disclosure

Before private/sensitive data eligibility, use:

```text
synthetic fixtures
public/non-sensitive fixtures
purpose-built minimized fixtures
provider sample payloads
```

for live compatibility/direct quality work where sufficient.

Real private/sensitive data requires applicable legitimate purpose, processor/data-flow, security/privacy, consent/legal-basis and audit/evidence gates.

Shadow/canary traffic is real disclosure.

## 25.3 Production qualification

Promotion requires same material production composition or independent proof for each material delta.

Required evidence includes as applicable:

```text
adapter conformance
live compatibility
DANTE-E applicable direct evals
security/privacy/data eligibility
capacity/reliability
usage/cost evidence
route/config identity
retry/fallback/hedging composition
```

Direct eval failure blocks promotion.

---

# 26. Provider adapter conformance

Every admitted adapter proves claimed feature modes across at least:

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

Application fakes remain distinct from adapter conformance fixtures.

Conformance proves protocol normalization only.

---

# 27. Retry / fallback / cancellation / cumulative disclosure

## 27.1 DANTE owns effective retry budget

SDK/gateway/application retries must not multiply invisibly.

Adapter integration either:

```text
disables SDK/gateway automatic retries
```

or makes every material wire/provider attempt visible/accounted under DANTE attempt/resource/disclosure/evidence semantics.

Every resource-consuming new attempt requires current admission.

Every data-egress new attempt creates/evaluates an egress exposure event.

Hidden retry after indeterminate acceptance is forbidden without exact safe retry proof.

## 27.2 Safe retry

```text
safe transient pre-acceptance failure
→ bounded retry MAY be allowed

possible accepted/processed state + lost response
→ OUTCOME UNKNOWN
→ establish/reconcile before replay
```

Provider refusal is not infrastructure failure and cannot trigger refusal-shopping.

## 27.3 Alternate route rebuild

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

Alternate route rebuilds/minimizes `ConsumerContext`; it does not blindly replay prior provider request bytes.

## 27.4 Hedging

Server-side multi-provider hedging is OFF by default.

```text
MULTI-PROVIDER HEDGING
!= LATENCY-ONLY OPTIMIZATION
```

It requires explicit privacy/security/cost/operational/qualification evidence.

## 27.5 Cancellation

```text
cancel requested
!= cancel confirmed
!= execution quiesced
```

Disconnect closes recipient publication but does not rewrite already-crossed egress/provider truth.

---

# 28. Route configuration / material identity

Behavior-bearing route config is static/versioned/typed first.

Target source:

```text
apps/backend/config/intelligence/revisions/<revision>.json
```

`RouteConfigIdentity` binds:

```text
logical revision
content digest
```

Loaded invocation snapshot binds exact validated bytes.

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

Deployment settings may provide:

```text
approved active config selector
provider endpoint/deployment locator
region/environment endpoint
credential/secret reference
approved emergency/kill selector
resource/environment limits
```

They cannot become hidden behavior-policy language.

```text
ACTIVE POINTER != IMMUTABLE CONFIG REVISION
COHERENT INVOCATION CONFIG != PERPETUAL AUTHORIZATION
COHERENT INVOCATION CONFIG != IMMUNITY FROM EMERGENCY DENY
```

CI/build/packaging proves qualified config bytes are delivered to runtime or independently qualifies material deltas.

---

# 29. Policy consumer seam

Intelligence consumes current policy/authority; it does not own it.

Method-specific seam:

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

External surfaces expose only disclose-safe reason/limitation semantics.

No temporary production identity bypass:

```text
NO X-User-Id bypass
NO fake-auth public route
NO Intelligence-owned parallel Auth truth
```

Tests may construct synthetic trusted contexts. Production private-data activation waits for real integrated Auth/AuthZ.

---

# 30. Resource admission / settlement

Consumer methods:

```text
estimate(ResourceEstimateRequest) -> ResourceEstimate
admit(ResourceAdmissionRequest) -> ResourceAdmission
settle(ResourceSettlementRequest) -> ResourceSettlement
```

Flow:

```text
estimate bounded route exposure
→ admit/reserve when real shared authority exists
→ execute
→ collect actual usage evidence
→ settle/reconcile late or unknown usage
```

```text
UNKNOWN USAGE != ZERO USAGE
ESTIMATE != FINAL COST
PROVIDER TOKEN != COMMERCIAL CREDIT
COMMERCIAL QUOTA != PROVIDER QUOTA != PLATFORM CAPACITY
```

First technical slice may be unmetered only when no shared/commercial policy exists.

If shared/commercial quota becomes eligibility, activation waits for proper durable accounting owner.

Safety/reconciliation work already required cannot be blocked by optional commercial quota exhaustion.

---

# 31. Verification contract

`VerificationResult` prevents provider output from becoming publishable by convention.

Statuses:

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

Verification prefers deterministic/application evidence where available.

Any model verifier is an auxiliary governed model inference, not canonical truth.

```text
MODEL CLAIM "DONE" != DOMAIN COMPLETION
```

---

# 32. Effect boundary / transaction rule

```text
EffectBoundary.finalize(
    WorkContract,
    proposed_effects,
    current_policy_basis,
) -> EffectOutcome
```

First vertical:

```text
ConsequenceProfile = READ_ONLY
proposed_effects = []
→ EffectOutcome.NO_EFFECT
```

Any mutation intent:

```text
→ REJECT
→ no mutation adapter
→ no canonical mutation transaction
```

Future consequential work follows:

```text
owning application mutation semantics
current target/state resolution
policy/approval/autonomy
outer application/effect transaction owns commit/rollback
persistence adapters may flush, never implicit commit
no PostgreSQL business transaction spans provider/network execution
provider/external outcomes not atomically rollbackable with PostgreSQL
ambiguous consequential external outcome -> reconciliation obligation
```

---

# 33. Publication / output representation

`PublicationDecision` is distinct from Verification/provider completion.

Before recipient emission recheck as applicable:

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
final transformed output semantics
```

Outcomes:

```text
ALLOW
ALLOW_WITH_LIMITATION
DENY
STALE_SUPPRESSED
NOT_CURRENT
```

`AskResult` exists only after safe publication.

First public Ask is non-streaming.

If output is materially redacted/transformed after verification, final representation is rechecked and may require re-verification/limitation.

If external streaming activates later, every emitted delta is a publication event with its own proof gate.

---

# 34. Operational non-interference

Protected/withheld state must not become a practical oracle through operational behavior.

Review externally observable:

```text
error class/message
fallback behavior
provider identity exposure
latency/timing class where material
counts/limits
resource behavior
retry behavior
```

Raw provider/security/policy errors do not flow directly to recipients when they reveal protected context/internal policy.

Architecture does not claim perfect elimination of all timing channels. It requires bounded threat-model-aware non-interference tests where hidden state could create a practical observable oracle.

---

# 35. RuntimeEvidencePort / audit / exporter failure

Typed `RuntimeEvidencePort` accepts a closed event union.

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

Default operational telemetry excludes raw:

```text
private request body
ConsumerContext
hidden Search candidates/counts
model response
source content
credentials/secrets
```

Search telemetry uses disclosed/eligible aggregate metadata only.

```text
CANONICAL DATA
!= AUDIT/EXECUTION EVIDENCE
!= OPERATIONAL TELEMETRY
!= EVAL/QUALIFICATION EVIDENCE
```

Operational telemetry exporter/backpressure failure:

```text
!= canonical transaction failure automatically
!= permission to weaken safety/privacy
!= permission to dump raw content for debugging
```

Ordinary non-mandatory telemetry failure is operational degradation/incident state and must not fabricate product truth.

Where a mandatory security/audit/effect evidence write is a precondition, that is a different evidence plane and may fail closed under its owning contract.

Sensitive access/provider-egress cases requiring durable audit stay ineligible until a real durable audit owner/integrity/retention/access contract exists.

Telemetry is never silently promoted to audit.

---

# 36. Query coherence / PostgreSQL isolation

Database default remains `READ COMMITTED`.

Every Search/semantic query family declares:

```text
maximum truthful guarantee
coherence requirement
snapshot requirement
currentness rule
```

For required coherent snapshots use least-complex valid method:

```text
single SQL statement / CTE
or
explicit per-operation stronger isolation such as REPEATABLE READ
or
another accepted owner/material-basis mechanism proving coherence
```

No global isolation escalation is authorized by AI.

If coherence cannot be established, downgrade/label the guarantee.

Permission-safe eligibility is applied before protected aggregate/rank/count/facet semantics.

---

# 37. Runtime / persistence classification

## Request-local / no-store by default

```text
WorkContract
ExecutionStatus / RunId/request execution state
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
Search request/result/page/cursor state
PolicyDecision ordinary read request
ResourceAdmission unmetered/request-local
ModelInvocation request/result
ProviderAttempt runtime
EgressAttempt/request-local exposure accounting
VerificationResult
ResultMaturity
EffectOutcome.NO_EFFECT
PublicationDecision/Result
```

## Durable noncanonical evidence/artifact when justified

```text
route/config revisions -> Git/release artifact
qualification evidence -> CI/release evidence store
operational telemetry -> observability backend
security/audit evidence -> independent owner when required
```

## Persist only on independent trigger

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

No generic AI persistence is justified now.

---

# 38. Lifecycle matrix

| Object | Create | Persist first vertical | Mutate/version | Release/expire | Cache/reuse | Retry/cancel |
|---|---|---|---|---|---|---|
| `WorkContract` | trusted intake | no | immutable; derive/supersede | request end | no cross-request default | same protected contract only while current |
| `ExecutionStatus` | request/work start | no | controlled runtime transition | request end | no | cancellation/supersession explicit |
| `ContextPlan` | Ask planning | no | explicit new version/replan | request end | no | rebuild on bounded stale/unresolved |
| `InformationNeed` | plan/work/policy/capability | no | explicit status/new need under ceiling | request end | no | reacquire/clarify |
| `ContextStrategy` | per need | no | replace explicitly | request end | no | bounded replan |
| `ReferenceResolutionResult` | resolution need | no | immutable | request end | no stale reuse | rerun after material change |
| `SemanticQueryOutcome` | structured query | no | immutable | request end | no semantic cache default | source/DB retry only under policy |
| `RetrievalPlan` | per need | no | explicit replacement | request end | no | bounded by plan/deadline |
| `RetrievalCandidate` | acquisition | no | immutable | after validation/request | no | reacquire after stale/source change |
| `ContextFragment` | validated source material | no | immutable representation | request end | no default | reacquire/revalidate |
| `ContextReadiness` | coverage/coherence check | no | recompute | request end | no | recompute |
| `ConsumerContext` | before one consumer | no | new projection on material change | consumer/request end | no generic reuse | rebuild alternate route |
| `ContextManifest` | material exposure | no | request-local exposure accumulation | request end | no | not retry authority |
| `BasisManifest` | source/dependency assembly | no | new manifest after reread | request end | no | stale -> reread/rebuild |
| `PolicyDecision` | each enforcement boundary | no ordinary slice | immutable | request end | no material reuse | re-evaluate |
| `RouteConfigSnapshot` | before invocation | revision durable externally | immutable | request end | exact-revision process cache | material delta needs qualification |
| `ProviderAttempt` | every outbound attempt | no canonical persistence | explicit attempt state | request end | no | new attempt id; cancel states explicit |
| `EgressAttempt` | every material send | no first vertical | request-local state transition | request end | no | every retry/fallback creates/evaluates new egress |
| `ResourceAdmission` | before resource attempt | no first unmetered slice | immutable | request end | no | new admission per resource-consuming attempt |
| `VerificationResult` | candidate result | no | immutable | request end | no | reverify after material change |
| `ResultMaturity` | result lifecycle | no | controlled transition to no stronger than evidence | request end | no | n/a |
| `EffectOutcome` | effect boundary | no read-only slice | immutable | request end | no | future effect retry separate |
| `PublicationDecision` | immediately before publication | no | immutable | response end | no | reevaluate; never replay authority |
| route config revision | reviewed change | Git/release | immutable new revision | retention policy | exact identity | n/a |
| qualification artifact | qualification run | evidence store | immutable/new id | retention policy | n/a | n/a |

Any future survival proposal re-enters AI-03C materiality/lifecycle rules.

---

# 39. Pending direct-proof register

| Proof | Trigger | Initial status |
|---|---|---|
| PSV-06 / SC-017 hidden-result non-interference | first protected Search/semantic/reference family | PENDING when applicable |
| PSV-07 / SC-018 FTS mixed filter/query | FTS/pg_trgm serving | N/A until activated |
| PSV-08 / SC-019 vector filtered recall/relevance | ANN/vector serving | N/A until activated |
| PSV-09 / SC-020 projection freshness/material basis | served derived/current projection | PENDING when applicable |
| PSV-10 / SC-021 deletion/redaction propagation | surviving derived representation/index | PENDING when applicable |
| PSV-21..28B durable/Restate proofs | Class-B durable execution | N/A until activated |
| PSV-37 pgvector provenance | pgvector/embedding serving | N/A until activated |

`N/A` requires explicit absent capability/feature-mode reason.

```text
missing evidence != N/A
```

Provider/eval evidence remains separately required.

---

# 40. Qualification artifact schema

Every promotable route composition has immutable evidence containing at least:

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
SDK/gateway retry configuration
DANTE eval suite/version
applicable DANTE-E01..E14 cases + hard-gate results
SC/PSV applicability/status register
provider conformance evidence ref
live compatibility evidence ref where required
qualification fixture/data-class disclosure classification
capacity/reliability evidence ref where required
privacy/security/data eligibility evidence
cost/usage evidence
material deltas from prior qualification
revalidation/expiry conditions
qualification decision
promotion status
```

No blanket PASS may hide skipped applicable cases.

Qualification distinguishes candidate admission, qualification and promotion.

---

# 41. Test topology

```text
apps/backend/tests/unit/modules/search/
→ Search contracts/registry/guarantees/non-interference
→ cursor/publication/navigation currentness

apps/backend/tests/unit/modules/intelligence/
→ WorkContract / ExecutionStatus / ResultMaturity
→ ContextPlan/InformationNeed/ContextStrategy
→ RealityScope/RuntimeInterpretationFrame
→ ReferenceResolution + non-interference
→ SemanticQueryGateway ownership/unsupported behavior
→ RetrievalPlan/RetrievalCandidate validation
→ DATA != INSTRUCTION
→ transform semantic-equivalence checks
→ ContextReadiness/ConsumerContext/ContextManifest/BasisManifest
→ Policy/Resource/Effect
→ Verification/Publication
→ EgressAttempt/cumulative disclosure
→ auxiliary-inference ModelAccess enforcement
→ cancellation/deadline/error taxonomy

apps/backend/tests/unit/test_architecture_boundaries.py
→ import/dependency/provider/eval/DB authority boundaries

apps/backend/tests/integration/modules/search/
→ real PostgreSQL Search family tests
→ permission non-interference
→ guarantee/coherence/isolation
→ revocation between query and response

apps/backend/tests/integration/modules/intelligence/
→ Search public seam
→ real capability semantic query seams as they exist
→ reference resolution hidden candidates
→ stale basis/Auth change/source retirement
→ fake ModelAccess composition
→ route-config snapshot
→ retry/fallback/request-local exposure
→ telemetry exporter failure posture

apps/backend/tests/integration/providers/<binding>/
→ adapter conformance after candidate admission
→ hidden SDK retry behavior controlled/accounted

tooling/ai-evals/
→ direct qualification using production-owned composition
→ synthetic/minimized fixtures until real-data eligibility

tests/system/
→ black-box Search/Ask after real Auth/HTTP integration
```

Mandatory fixtures include:

```text
ambiguous and hidden same-name targets
permission revoked after Search query before response
cursor reused after Auth/source change
navigation ref after permission revocation
mutate-after-fixture stale basis
relative date/time + timezone/DST
hidden result affecting count/facet/rank/aggregate
multi-statement concurrent write/coherence
malicious retrieved instruction/source
query-rewrite scope expansion
source retirement/redaction after retrieval
material input/output redaction changing meaning
provider rate limit/timeout/invalid schema/disconnect/ambiguous submit/cancel race
provider timeout after material send
provider completed but verification rejects
provider conformance PASS but direct-eval FAIL
live qualification before private-data eligibility uses synthetic fixture
fallback after prior possible exposure
alternate-provider context rebuild
multi-provider hedging disabled
auxiliary model helper cannot bypass ModelAccess
SDK hidden retry multiplication
telemetry exporter failure
hidden-sensitive state route/error practical-oracle attempt
sensitive request missing mandatory durable audit
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

Provider/direct-eval/capacity/privacy evidence adds to normal CI.

---

# 42. Architecture test obligations

Automated architecture checks prove at least:

```text
Search does not import Intelligence
Intelligence imports Search only via public Search surface
Intelligence does not import Search private PostgreSQL adapter
Intelligence/application does not import SQLAlchemy/DB mappings
SemanticQueryGateway cannot expose raw SQL/table/ORM authority
SemanticQueryGateway cannot implement Intelligence-owned cross-capability SQL
ReferenceResolver cannot query unrestricted hidden universe then leak ambiguity
provider SDK imports only inside admitted private binding adapter
auxiliary model helpers cannot import provider SDK directly
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

# 43. Dependency / framework lock

Allowed initial direction:

```text
FastAPI/Pydantic existing inbound/config boundaries
SQLAlchemy/psycopg existing PostgreSQL infrastructure
stdlib internal contracts/orchestration where sufficient
one admitted provider SDK/protocol only inside private adapter after P1
```

Forbidden without independent evidence:

```text
LangChain/LangGraph-style orchestration ownership
agent framework as semantic owner
provider gateway as mandatory data path
MCP framework for ordinary first vertical
new vector/search database
generic Repository/UoW framework
ORM/model-to-SQL tool
unreviewed dynamic control-plane database
```

MCP/A2A/client SDKs later remain adapters, never core application semantics.

---

# 44. Feature / activation gates

| Capability | Build posture | Activation requirement |
|---|---|---|
| Search contracts/shell | BUILD-READY after final mega PASS | no public activation claim |
| protected Search family | conditional | real data + Auth/disclosure + PSV-06/SC-017 + family tests |
| protected reference-resolution family | conditional | eligible-universe/non-interference proof + typed resolver tests |
| Search HTTP | gated | authoritative integrated Auth/AuthZ + publication-currentness behavior |
| structured semantic query family | conditional | owning capability/public query seam + permission/coherence proof + typed tests |
| FTS/pg_trgm | OFF | measured need + DB same-change + PSV-07/SC-018 |
| vector/pgvector | OFF | eval need + lifecycle + PSV-08/SC-019 + PSV-37 + applicable freshness/deletion proofs |
| ModelAccess fake | test only | no production claim |
| provider qualification candidate | OFF | reviewed candidate admission |
| live compatibility synthetic/minimized | OFF | admitted adapter + safe test-data posture |
| live private-data provider route | OFF | processor/data/security/privacy eligibility + conformance/live/direct eval/capacity as applicable |
| auxiliary model inference | OFF unless explicitly needed | same ModelAccess/qualification/egress/resource evidence as material inference |
| production Ask | OFF | Auth + source/query path + qualified model route when used + verification/publication + evidence/audit/privacy |
| sensitive audit-required Search/Ask | OFF | minimum durable audit plane exists |
| external streaming | OFF | delta-level publication/disconnect/cumulative-disclosure proof |
| server-side multi-provider hedging | OFF | explicit privacy/security/cost/operational qualification |
| consequential Effect | OFF | I9 target/policy/approval/transaction/idempotency/reconciliation proof |
| commercial/shared ledger | OFF | real enforcement requirement |
| durable Run/Restate | OFF | real workflow trigger + PSV-21..28B |
| AI memory | OFF | explicit owner/purpose/lifecycle trigger |
| cross-Run prior-disclosure accounting | OFF | H19 real trigger |
| MCP/A2A | OFF | real integration trigger |
| Execution Environment | OFF | generated/untrusted code/browser/computer-use threat-model trigger |

---

# 45. Readiness classes

```text
BUILD-READY
= accepted contracts may be implemented with fakes/synthetic trusted contexts

INTEGRATION-READY
= required real owning seams/data/capabilities exist

ACTIVATION-READY
= user-visible path passed every applicable security/privacy/proof/ops/release gate
```

Implementation stages after final acceptance:

```text
I0 repository/application ownership + architecture-test skeleton
I1 Search public contracts/registry/application shell
I2 Intelligence pure contracts:
   Work/Execution/ContextStrategy/ReferenceResolution/SemanticQuery/RetrievalCandidate/
   Policy/Resource/Effect/Verification/Publication/EgressAttempt + deterministic fakes
I3 real deterministic Search/structured query families only when owning data/seams are materially ready
I4 provider candidate admission + inactive concrete adapter candidate
I5 conformance/live compatibility + direct DANTE qualification
I6 read-only Ask DANTE
I7 production hardening / observability / privacy / resource / rollout / audit as applicable
I8 scenario/planning proposal vertical
I9 first bounded consequential Effect vertical
I10 proactive/background/durable/external-agent capabilities only on real trigger
```

I0-I2 do not require production Auth/provider availability.

Public private-data Search/Ask do.

---

# 46. Implementation dependency graph

```text
B0  architecture boundary tests + pure contracts

B1  Search public contracts + SearchFamilyRegistry + pure application
    ↓
B2  bounded PostgreSQL Search adapter + real PG/non-interference/coherence tests
    ↓
B3  Search inbound adapter/wiring behind Auth activation gate

B4  Intelligence core:
    WorkContract / ExecutionStatus / ResultMaturity
    ContextPlan / InformationNeed / ContextStrategy
    ReferenceResolution + non-interference
    SemanticQueryGateway + unsupported-without-owner posture
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
B6  inactive ProviderAdapter/ProviderBinding + dependency
    ↓
B7  conformance + live compatibility on safe/minimized qualification data
    ↓
B8  tooling/ai-evals using SAME production-owned composition
    + direct DANTE qualification
    + applicable capacity/security/privacy/economic proof
    ↓
B9  qualification/promotion decision
    ↓
B10 read-only Ask HTTP + safe publication
    ↓
B11 production hardening/system acceptance/activation evidence
```

Candidate rejection at P1/B7/B8/B9 does not change DANTE application semantics.

---

# 47. Candidate commit sequence

```text
C1  test(ai): architecture boundary checks
C2  feat(search): public contracts, eligibility, family registry, deterministic shell
C3  feat(search): bounded PostgreSQL adapter + PG proof for first family
C4  feat(search): inbound adapter/wiring behind Auth gate
C5  feat(ai): Work/Execution/ContextStrategy/ReferenceResolution/SemanticQuery/Retrieval contracts + fakes
C6  feat(ai): Policy/Resource/Verification/Publication/Effect/EgressAttempt/RuntimeEvidence contracts
C7  feat(ai): route-config identity/loader/digest snapshot
C8  chore(ai): provider candidate-admission decision
C9  feat(ai): admitted inactive provider adapter + conformance/live compatibility
C10 test(ai): direct DANTE qualification using production-owned composition
C11 chore(ai): qualification/promotion decision
C12 feat(ai): read-only Ask DANTE + safe final publication
C13 test(ai): Search/Ask system/failure/privacy/operational hardening
```

C8 `DEFER/REJECT` stops provider work.

C10/C11 failure prevents production route use.

No database migration commit is planned.

---

# 48. Deferred responsibility ledger

```text
Interaction Session / rich continuity
→ future real multi-turn need
→ no generic conversation persistence

Work Supersession across requests
→ real continuing Work lifecycle

Scenario Workspace / Solver
→ I8
→ runtime/no-store default
→ OR-Tools only on real solver trigger

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
→ adapter/capability trigger

AI memory persistence
→ explicit memory owner/purpose/retention/lifecycle trigger

H19 cross-Run prior-disclosure survival
→ real cross-Run/surface cumulative-disclosure trigger

FTS/vector representations
→ measured retrieval need + direct proofs
```

---

# 49. Product completeness / launch boundary

Initial technical vertical:

```text
Global Search subset
+ read-only Ask DANTE
```

```text
I6 COMPLETE
!= V1 GLOBAL SEARCH & COMMAND COMPLETE
```

Accepted Product V1 later includes where scoped:

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

# 50. Explicit non-claims

```text
V3 BASELINE ACCEPTED AFTER FINAL MEGA RETEST        NO / RETEST REQUIRED
AI-05 STRUCTURALLY CLOSED                          YES
modules/search implemented                         NO
modules/intelligence implemented                   NO
SemanticQueryGateway implemented                   NO
Auth/AuthZ integrated on this branch               NO
provider candidate admitted                        NO
provider/model/SDK production-qualified            NO
provider dependency added                          NO
direct provider eval executed                      NO
production capacity qualified                      NO
production Ask active                              NO
external streaming active                          NO
PostgreSQL/Alembic changed                         NO
new AI table/index                                 NO
FTS/trgm/vector activated                          NO
conversation persistence selected                  NO
control-plane persistence selected                 NO
commercial/resource ledger implemented             NO
Restate/R2/MCP/A2A activated                       NO
Execution Environment selected                     NO
```

---

# 51. Final fresh mega battery

Before acceptance, rerun from zero:

```text
MKT-001..MKT-100
```

Coverage families:

```text
001..010 repository/path/ownership/dependency truth
011..020 Search eligibility/non-interference/currentness/navigation
021..030 Semantic Query/reference resolution/typed-owner boundaries
031..040 Context/Retrieval/Reality/interpretation/instruction provenance
041..050 Auth/policy/currentness/verification/publication/Effect
051..060 provider attempts/errors/cancellation/egress/fallback/retries
061..070 provider qualification/config/resource/evidence/audit
071..080 persistence/lifecycle/direct-proof/activation/deferred boundaries
081..090 H14..H18 qualification/exposure/cumulative-disclosure regression
091..100 H19..H25 publication/ownership/aux-inference/retry/non-interference regression
```

Required compounds include at least:

```text
C01 hidden Search row + rank/count/facet/page + permission revocation before response
C02 cursor reuse + source retirement + navigation attempt
C03 ambiguous same-name target + one hidden candidate + clarification UI
C04 relative-time query + DST boundary + structured aggregate + concurrent write
C05 malicious source instruction + query rewrite helper + provider egress
C06 source deleted after provider exposure before answer publication
C07 provider timeout after possible send + retry budget + alternate provider candidate
C08 alternate provider context contraction + cumulative disclosure + resource admission
C09 SDK hidden retry + ambiguous acceptance + usage unknown
C10 emergency deny + in-flight invocation + late result + publication closed
C11 provider completed + output DLP changes meaning + verification/publication
C12 telemetry exporter failure + safe response path
C13 mandatory audit missing + sensitive request
C14 provider conformance PASS + direct DANTE eval FAIL + promotion attempt
C15 no capability semantic-query owner + model offers SQL shortcut
C16 hidden sensitive state changes internal route/error/latency behavior
C17 provider outage + deterministic Search/semantic path remains valid
C18 client disconnect + possible provider exposure + no durable Run
C19 H19 cross-Run cumulative-disclosure scenario attempted while durable accounting OFF
C20 future consequential command accidentally enters read-only first envelope
```

Reverse authority pass:

```text
v3
→ AI-05
→ AI-05A / AI-05B
→ AI-04 / PRE-AI05
→ AI-03
→ AI-02.1
→ PostgreSQL / Physical / Logical / Domain
→ Product / simulations
```

Acceptance requires no unexplained contradiction, no dropped applicable proof, no new generic owner, no provider preselection and no hidden persistence/effect/authorization shortcut.

Until that pass succeeds:

```text
IMPLEMENTATION I0 = HOLD
```
