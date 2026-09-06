# DANTE Intelligence — Current Implementation Baseline

- **Status:** CURRENT POST-AI05 HARDENED CANDIDATE / FINAL MEGA RETEST REQUIRED
- **Branch:** `feature/ai-architecture`
- **Established:** 2026-09-02
- **PRE-SCOPE:** `b11aedf391ab3d99d2c6102ce008b1b7ed6bd066`
- **Upstream:** AI-05 CLOSED / STRUCTURALLY ACCEPTED
- **Post-closure hardening:** POST05-H01..H12 APPLIED / H13 routing repair deferred until acceptance
- **Implementation:** NONE
- **Provider/model/SDK:** OPEN / CANDIDATE-ADMISSION + QUALIFICATION GATED
- **Database change:** NONE
- **Alembic change:** NONE

This document is the single **current implementation-facing candidate authority** for DANTE Intelligence after AI-05 and the independent post-AI05 mega kill-test.

It consolidates the still-valid build substance of:

```text
AI-05A ownership/build boundary
AI-05B concrete candidate
AI05B-H01..H15
AI05-H01 readiness hardening
AI-05B / AI-05 closure contracts
POST05-H01..H12
```

The older candidate/hardening/acceptance files remain truthful validation evidence. A new implementation task must not reconstruct current build truth by mentally applying patches across them.

This baseline is **not accepted for implementation entry until the final independent MKT-001..MKT-080 + compound + reverse pass succeeds**.

---

# 1. Authority and non-negotiable inheritance

This implementation baseline consumes and does not redefine:

```text
Product / North Star
Domain Model
Whole Logical Model / WL-H01..WL-H12
Physical Model
PostgreSQL Persistence Constitution / ADR-010
current Database System of Record
AI-00
AI-02.1
AI-03A / AI-03B / AI-03C
AI-04A / AI-04B / AI-04C / AI-04 whole acceptance
PRE-AI05
AI-05A / AI-05B / AI-05 whole acceptance
```

Repository/executable truth outranks this file if a future accepted implementation deliberately evolves the architecture through the normal process.

Binding invariants include at minimum:

```text
DANTE != chatbot
DANTE != provider
DANTE != model
DANTE != transcript

PostgreSQL = sole canonical persistence/material-history authority
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

Interaction Session != Run != Worker
Scenario != canonical current

MODEL OUTPUT != PUBLISHABLE OUTPUT
RAW PROVIDER EVENT != DANTE RUNTIME EVENT != PUBLICATION EVENT

RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
RUN-START AUTONOMY != PERPETUAL AUTONOMY
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
CANCELLATION REQUESTED != CANCELLATION CONFIRMED != EXECUTION QUIESCED

MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
HARNESSPROFILE != PROVIDERBINDING
PROVIDER SDK != APPLICATION CONTRACT

QUALIFIED != ELIGIBLE != AVAILABLE != ENTITLED != ROLLOUT-ACTIVE
APPLICATION FAKE != ADAPTER CONFORMANCE != LIVE COMPATIBILITY != DIRECT EVAL != CAPACITY PROOF

BUILD-READY != INTEGRATION-READY != ACTIVATION-READY
```

---

# 2. Current repository truth / materialization posture

At this baseline's establishment, production backend source remains foundation-heavy:

```text
apps/backend/src/dante/
├── bootstrap/
└── platform/
    ├── config/
    ├── database/
    └── recovery/
```

The following are **target paths, not current implemented claims**:

```text
apps/backend/src/dante/modules/search
apps/backend/src/dante/modules/intelligence
tooling/ai-evals
apps/backend/config/intelligence/revisions
```

Do not create empty ceremonial directories. A path appears only with real content in the corresponding reviewed implementation commit.

Current dependency truth remains:

```text
FastAPI
Pydantic / pydantic-settings
SQLAlchemy async
psycopg
Alembic
```

No AI/provider SDK is currently an accepted dependency.

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
123 CHECKs
```

```text
DATABASE CHANGE = NONE
ALEMBIC CHANGE  = NONE
```

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
permission-safe result universe
safe snippets/facets/counts/rank
canonical/source navigation refs
SearchFamilyRegistry
bounded cross-capability read projection for Search only
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
model-route consumption when useful
verification
Result Maturity
Effect consumer boundary
safe publication
runtime evidence emission
```

It does not own canonical business tables/meaning, Auth/AuthZ truth, commercial subscription truth or provider SDK semantics.

## 3.3 Provider

Concrete provider SDK/protocol code exists only inside the selected **private outbound binding adapter** after candidate admission.

Initial accepted physical placement remains under the Intelligence outbound adapter boundary, for example:

```text
apps/backend/src/dante/modules/intelligence/adapters/outbound/models/<binding>/
```

No provider SDK type appears in Search/Intelligence public contracts.

## 3.4 Bootstrap / platform / tooling

```text
bootstrap
→ composition + lifecycle + inbound registration only

platform
→ genuinely shared technical infrastructure only

platform/config
→ deployment-only config/secret/selector mechanics

platform/observability
→ shared telemetry mechanics when materialized

tooling/ai-evals
→ engineering qualification outside ordinary production request path
```

Production code never imports `tooling/ai-evals`.

---

# 4. Target repository shape

Create only files needed by the current implementation step.

Candidate end-state for the first vertical:

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
                └── <binding>/      # only after candidate admission
```

This is not permission to create one class/file per abstract architecture noun mechanically. If several pure value types belong together, keep them together. If a proposed file has no real implementation content, do not create it.

The previously proposed Intelligence-owned `search_access.py` remains rejected. Intelligence consumes the Search-owned public protocol directly.

---

# 5. Public Search contract

`modules/search/public.py` owns the only Search public application protocol.

Conceptual surface:

```text
class SearchService(Protocol):
    async def search(SearchExecutionRequest) -> SearchResult: ...
    async def resolve_navigation(NavigationExecutionRequest) -> NavigationResult: ...
```

`SearchExecutionRequest` is trusted application input and includes only:

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

It cannot accept:

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
safe facets/counts only when non-interference/coherence contract permits
pagination
achieved retrieval/search guarantee
limitations/unresolved classification
source/currentness/basis-safe metadata
```

`SearchHit` uses typed `SearchTargetRef`, never universal `entity_id`.

---

# 6. SearchEligibilityEnvelope

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

For protected/private Search:

```text
ELIGIBILITY CONSTRAINS THE CANDIDATE UNIVERSE
BEFORE OBSERVABLE RANK/COUNT/FACET/PAGINATION SEMANTICS.
```

A generic:

```text
query all rows
→ rank/count/facet
→ Python post-filter
```

is not accepted as the sole permission proof.

---

# 7. SearchFamilyRegistry

`SearchFamilyId`, `SearchFamilyRegistration` and `SearchFamilyRegistry` are static/application implementation contracts, not Domain identities or tables.

Each registration freezes at least:

```text
family_id
owning product/capability boundary
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
```

```text
SEARCH FAMILY ID != TABLE NAME
SEARCH REGISTRY != DATABASE CATALOG INTROSPECTION
SEARCH REGISTRY != GENERIC REPOSITORY
```

A family activates only when real material product data, source/current/history semantics, permission-safe eligible universe, bounded query behavior and applicable direct proofs exist.

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

The gateway composes explicit owning-capability public query contracts or bounded approved query handlers.

It cannot accept raw SQL/ORM/table/model-predicate authority.

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

The returned typed payload is owned by the relevant capability/query family, not one universal property bag.

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

No model call is required merely to calculate an answer DANTE already owns deterministically.

If model assistance is used only to interpret a natural-language intent, the model may propose a bounded typed query intent; normal application validation and capability semantics still own the actual query/result.

---

# 10. Reference / Target Resolution

Material referents are resolved explicitly before an answer/effect that requires unique/exact binding.

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

Resolution may consume Search/owning capability public seams and bounded model assistance when appropriate, but:

```text
MODEL CONFIDENCE != REFERENCE RESOLUTION
DISPLAY NAME != CANONICAL TARGET
```

Ambiguity remains first-class and may require clarification/limitation.

---

# 11. WorkContract

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

Must preserve as applicable:

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

Must preserve as applicable:

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

Important statuses include:

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

## 12.3 ContextStrategy

Strategy is explicit per InformationNeed and may select the least-complex route that satisfies the required semantics.

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

The first vertical activates only the subset its real workloads require.

## 12.4 Reality Scope

Preserve:

```text
CANONICAL_CURRENT
MATERIAL_HISTORICAL / AS_OF
SCENARIO <workspace> when activated
OPEN_WORLD_ASSERTION when activated
explicit MIXED frame only when legitimate
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

Relative language such as `last month`, `today`, `next week` or `before Friday` cannot be resolved from server-local wall-clock assumptions.

---

# 13. Retrieval contract

When discovery/acquisition is required:

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

A candidate is a runtime discovery object, not Context/truth/evidence by rank.

Preserve enough to validate:

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

Candidate validation yields states such as:

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

Only surviving candidate material becomes ContextFragment.

---

# 14. Source standing / instruction provenance

Every ContextFragment/ConsumerContext projection preserves enough metadata to keep these dimensions distinct:

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

Retrieved/imported/external/user-authored source text is `DATA` by default.

It does not become a privileged instruction merely because a user once authored the text.

```text
DATA != INSTRUCTION
USER CONTENT != CURRENT USER INSTRUCTION AUTOMATICALLY
TRANSFORMED DATA != TRUSTED INSTRUCTION AUTOMATICALLY
```

Source content cannot create:

```text
new WorkContract purpose
new Authority/AuthZ/Consent
new InformationNeed outside the accepted ceiling
provider/tool capability
Effect authorization
recipient disclosure permission
```

The harness/provider projection must preserve role separation instead of concatenating all text into one undifferentiated prompt.

---

# 15. ContextReadiness / ConsumerContext / ContextManifest / BasisManifest

`ContextReadiness` answers whether required InformationNeeds are sufficiently covered/coherent/current for the current consumer step.

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

`ContextManifest` records established consumer exposure, not merely what the system intended to assemble.

`BasisManifest` tracks material dependencies/currentness/coherence used to justify the result.

```text
ContextManifest != BasisManifest
```

First vertical stores none of these as generic product rows.

---

# 16. Intelligence public contract

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

`AskResult` is constructed only after verification + publication approval.

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

# 17. HTTP trust boundary

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
provider/model/route
HarnessProfile
RouteConfigIdentity override
ConsequenceProfile upgrade
Effect authorization
resource/commercial entitlement
raw table/model/SQL
```

Pydantic-valid != authorized.

Initial inbound routes remain candidates:

```text
POST /api/v1/search
POST /api/v1/ask
```

Public route activation waits for real Auth/AuthZ integration.

---

# 18. First-vertical execution routes

## 18.1 Deterministic Search

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

## 18.2 Deterministic semantic question

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

## 18.3 Model-assisted read-only Ask

```text
HTTP Ask
→ WorkContract
→ ContextPlan
→ InformationNeed(s)
→ ReferenceResolution where required
→ ContextStrategy per need
→ SemanticQuery and/or RetrievalPlan
→ candidate validation / ContextFragment
→ ContextReadiness
→ ConsumerContext
→ context/provider egress policy
→ qualified eligible route
→ resource admission
→ ModelAccessPort
→ ContextManifest actual exposure evidence
→ VerificationResult
→ ResultMaturity
→ EffectBoundary = NO_EFFECT
→ Basis/currentness revalidation
→ PublicationDecision
→ AskResult
```

---

# 19. ModelAccessPort / ModelAccessRuntime

Application-owned port:

```text
ModelAccessPort.invoke(ModelInvocationRequest, CancellationSignal)
    -> ModelInvocationResult

ModelAccessPort.stream(ModelInvocationRequest, CancellationSignal)
    -> AsyncIterator[ModelEvent]
```

The first public Ask surface is non-streaming. Internal provider streaming may be consumed only behind the normal verification/publication gate.

`ModelInvocationRequest` represents DANTE needs, not provider SDK objects.

It binds to:

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

# 20. Private ProviderAdapter

`ModelAccessRuntime` resolves one eligible qualified route and creates a DANTE `ProviderAttemptId` **before dispatch**.

Private contract:

```text
ProviderAdapter.invoke(ProviderAttemptRequest) -> ProviderAttemptResult
ProviderAdapter.stream(ProviderAttemptRequest) -> AsyncIterator[ProviderRuntimeEvent]
```

`ProviderAttemptRequest` includes only the resolved private mechanics needed by that binding:

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

The adapter does not own routing, egress authority, Effects or DB access.

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

Provider IDs are attempt evidence only.

---

# 21. Provider candidate lifecycle / qualification

Use this sequence; do not call an unqualified candidate "selected for production".

```text
P0  candidate discovery / shortlist
P1  candidate admission for qualification
P2  inactive material ProviderAdapter/ProviderBinding implementation
P3  adapter conformance
P4  live compatibility / feature proof
P5  direct DANTE eval on material production-owned composition
P6  capacity / reliability / security / privacy / economics evidence as applicable
P7  qualification decision
P8  canary/production promotion when all gates pass
```

## 21.1 Candidate admission

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

## 21.2 Qualification

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

# 22. Provider adapter conformance

Every selected candidate adapter must prove, for the feature modes it claims:

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
unsupported feature
provider refusal
```

Conformance proves protocol normalization only.

---

# 23. Retry / fallback / cancellation

```text
safe transient pre-acceptance failure
→ bounded retry MAY be allowed

possible accepted/processed state + lost response
→ OUTCOME UNKNOWN
→ reconcile/establish outcome before replay
```

No blind provider failover request replay.

Fallback re-evaluates current provider/data eligibility and builds the alternate request through the current alternate HarnessProfile/ProviderBinding.

Refusal is not infrastructure failure and cannot trigger refusal-shopping.

`RequestExecutionScope` owns request-local:

```text
deadline
attached tasks
CancellationSignal
active ProviderAttemptIds
publication-open/closed
bounded cleanup state
```

Client disconnect can stop publication while bounded in-process provider cleanup/correlation continues until outcome/cancel confirmation or execution deadline.

If outcome reconciliation must survive process crash, that is a separate durability trigger.

---

# 24. Route configuration

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

A loaded invocation snapshot binds the exact validated bytes used by the request.

Config contains, as applicable:

```text
schema/version
ModelTarget definitions
HarnessProfile definitions
ProviderBinding compatibility/locators
feature-mode definitions
routing policy rules
retry/fallback bounds
resource estimates/limits
security/control profile refs
qualification refs
rollout state
```

Secrets are not config payload.

Deployment environment may provide:

```text
approved active selector
secret/credential refs
region/environment endpoint locator
operational emergency/kill selector
```

but cannot become a hidden behavior-policy language.

```text
ACTIVE POINTER != IMMUTABLE CONFIG REVISION
```

CI/build/packaging must prove the qualified config bytes are delivered to runtime or independently qualify material deltas.

---

# 25. Resource admission / settlement

Intelligence consumes but does not own commercial/shared accounting.

Conceptual port responsibilities:

```text
estimate
admit / reserve when real shared authority exists
execute
collect actual provider/tool usage evidence
settle
reconcile late/unknown usage
```

```text
UNKNOWN USAGE != ZERO USAGE
ESTIMATE != FINAL COST
PROVIDER TOKEN != COMMERCIAL CREDIT
```

First technical slice may be unmetered if no shared/commercial policy exists.

If shared/monthly/commercial quota becomes an eligibility rule, activation waits for the proper durable owner/accounting state.

Safety/reconciliation work cannot be blocked by exhausted commercial quota.

---

# 26. Verification contract

Pure/request-local `VerificationResult` prevents raw model output from being promoted by convention.

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

It preserves as applicable:

```text
claim/source bindings
coverage/grounding limitation
source-standing limitation
basis/currentness
contradiction/conflict
required reread/abstention reason
```

Verification prefers DANTE deterministic/application evidence when available.

A model verifier, if used later, is a governed consumer and is not canonical truth.

```text
MODEL CLAIM "DONE" != DOMAIN COMPLETION
```

---

# 27. Effect boundary

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

Any mutation intent arriving in the first envelope:

```text
→ REJECT
→ no mutation adapter invoked
→ no canonical mutation transaction opened
```

Future consequential Effects must use owning application use cases, target/current-state resolution, policy/approval, outer transaction, idempotency/evidence and reconciliation semantics.

---

# 28. Publication contract

`PublicationDecision` is distinct from Verification and provider completion.

Before public response emission it rechecks as applicable:

```text
current Work/supersession
current Auth/AuthZ/Consent/Visibility
recipient + surface
Disclosure Projection / sensitivity
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

`AskResult` is created only after a safe publication outcome.

First public Ask is non-streaming, avoiding externally visible unverified deltas.

If external streaming is activated later, every delta is a publication event and requires its own proof gate.

---

# 29. RuntimeEvidencePort / audit separation

Typed `RuntimeEvidencePort` accepts only a closed/typed event union for the materialized vertical.

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
VerificationEvidence
EffectBoundaryEvidence
PublicationEvidence
```

Default operational evidence does not contain raw private prompt/context/Search body/model response/secrets.

```text
TELEMETRY != AUDIT != EVAL EVIDENCE != CANONICAL TRUTH
```

If a sensitive access/provider-egress case requires durable audit under current Product/security/privacy policy, that production case remains ineligible until a proper durable audit owner/integrity/retention/access contract is materialized.

Operational telemetry is never silently repurposed as audit.

---

# 30. Query coherence / PostgreSQL isolation

Backend database default remains `READ COMMITTED`.

Every Search/semantic query family declares:

```text
maximum truthful guarantee
coherence requirement
snapshot requirement
currentness rule
```

For a guarantee requiring one coherent snapshot across multiple logical values, use the least-complex valid method:

```text
single SQL statement / CTE
or
explicit per-operation stronger isolation such as REPEATABLE READ
or
another accepted owner/material-basis mechanism that proves coherence
```

No global isolation escalation is authorized by AI.

A family that cannot establish required coherence downgrades/labels its guarantee.

Permission-safe eligibility must be applied before protected aggregate/rank/count/facet semantics.

---

# 31. Runtime / persistence classification

## Request-local / no-store by default

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
VerificationResult
EffectOutcome.NO_EFFECT
PublicationDecision/Result
```

## Durable noncanonical evidence/artifact only when justified

```text
route/config revisions → Git/release artifact
qualification evidence → CI/release evidence store
operational telemetry → observability backend
security/audit evidence → only when independently required with own retention/integrity
```

## Persist only on independent trigger

```text
conversation/session continuity
Run registry/durable resume
AI memory
Context cache
prior-disclosure accounting
commercial/shared usage ledger
idempotency/saga/reconciliation state
background/durable Work
async invalidation jobs
vector/embedding representations
```

No generic AI persistence is justified by this baseline.

---

# 32. Lifecycle additions

All AI05B-H07/H14 lifecycle rules remain binding. POST05 additions:

| Object | Create | Persist first vertical | Mutate | Release | Reuse | Retry/cancel |
|---|---|---|---|---|---|---|
| `ContextStrategy` | per InformationNeed/plan decision | no | replace with explicit new strategy | request end | no cross-request default | bounded strategy replan only |
| `ReferenceResolutionResult` | per resolution need | no | immutable | request end | no stale cross-request reuse | rerun after material source/authority change |
| `SemanticQueryOutcome` | per structured query | no | immutable | consumer/request end | no semantic cache by default | query retry only under DB/source policy |
| `RetrievalCandidate` | per candidate discovery | no | immutable | after validation/request end | no cross-request default | reacquire after stale/source change |
| `VerificationResult` | per candidate answer/result | no | immutable | request end | no | reverify after basis/material change |
| `PublicationDecision` | immediately before publication | no | immutable | response end | never reusable after material change | reevaluate; not replay authority |
| `InstructionProvenance` | with source/context representation | no independent row | immutable with representation | fragment/context end | must survive transformations that reuse data | n/a |

Any future survival proposal re-enters AI-03C materiality/lifecycle rules.

---

# 33. Pending direct-proof register

The implementation/release evidence ledger must preserve these pending obligations.

| Proof | Trigger | Initial status |
|---|---|---|
| PSV-06 / SC-017 hidden-result non-interference | first protected Search/structured query family | PENDING when applicable |
| PSV-07 / SC-018 FTS mixed filter/query | PostgreSQL FTS/pg_trgm serving | N/A until activated |
| PSV-08 / SC-019 vector filtered recall/relevance | ANN/vector serving | N/A until activated |
| PSV-09 / SC-020 projection freshness/material basis | served derived/current projection | PENDING when applicable |
| PSV-10 / SC-021 deletion/redaction propagation | surviving derived representation/index | PENDING when applicable |
| PSV-21..28B durable/Restate proofs | Class-B durable execution | N/A until activated |
| PSV-37 pgvector provenance | pgvector/embedding serving | N/A until activated |

`N/A` requires a reason identifying the absent capability/feature mode. Missing evidence is not equivalent to N/A.

Provider/eval evidence remains separately required according to the provider lifecycle.

---

# 34. Qualification artifact

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
retry/fallback composition
DANTE eval suite/version
applicable DANTE-E01..E14 cases + hard-gate results
SC/PSV applicability/status register for activated mechanisms
provider conformance evidence ref
live compatibility evidence ref where required
capacity/reliability evidence ref where required
privacy/security/data eligibility evidence
cost/usage evidence
material deltas from prior qualification
revalidation/expiry conditions
qualification decision
promotion status
```

No blanket `PASS` may hide skipped applicable cases.

---

# 35. Test topology

Target tests extend the existing backend gate.

```text
apps/backend/tests/unit/modules/search/
→ Search contracts/registry/guarantees/non-interference pure cases

apps/backend/tests/unit/modules/intelligence/
→ WorkContract
→ ContextPlan/InformationNeed/ContextStrategy
→ RealityScope/RuntimeInterpretationFrame
→ ReferenceResolution
→ SemanticQueryGateway
→ RetrievalPlan/RetrievalCandidate validation
→ DATA != INSTRUCTION
→ ContextReadiness/ConsumerContext/ContextManifest/BasisManifest
→ policy/resource/effect
→ verification/publication
→ deterministic ModelAccess fake
→ cancellation/deadline

apps/backend/tests/unit/test_architecture_boundaries.py
→ import/dependency/provider/eval/DB authority boundaries

apps/backend/tests/integration/modules/search/
→ real PostgreSQL Search family tests
→ permission non-interference
→ guarantee/coherence/isolation behavior

apps/backend/tests/integration/modules/intelligence/
→ Search public seam
→ concrete semantic query handlers as they become real
→ stale basis / Auth change / source retirement
→ fake ModelAccess composition
→ route-config snapshot

apps/backend/tests/integration/providers/<binding>/
→ provider adapter conformance after candidate admission

tooling/ai-evals/
→ direct qualification using production-owned composition

tests/system/
→ black-box Search/Ask only after real Auth/HTTP integration
```

Mandatory targeted fixtures include:

```text
ambiguous target candidates
mutate-after-fixture stale basis
relative date/time + timezone/DST cases
hidden result affecting count/facet/rank/aggregate attempts
multi-statement concurrent write/coherence case
malicious retrieved instruction/source
query-rewrite scope-expansion attempt
source retirement/redaction after retrieval
provider rate limit/timeout/invalid schema/disconnect/ambiguous submit/cancel race
provider conformance PASS but direct-eval FAIL promotion attempt
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

Provider/direct-eval/capacity evidence adds to, never replaces, normal CI.

---

# 36. Architecture test obligations

Automated architecture checks must prove at least:

```text
Search does not import Intelligence
Intelligence imports Search only via Search public/contracts
Intelligence does not import Search private PostgreSQL adapter
Intelligence/application does not import SQLAlchemy/DB mappings
SemanticQueryGateway cannot expose raw SQL/table/ORM interface
provider SDK imports only in admitted private binding adapter
ProviderAdapter cannot import inbound HTTP schemas or DB runtime/mappings
production cannot import tooling/ai-evals
HTTP DTOs cannot carry Authority/AuthZ/provider/effect authoritative fields
no generic Repository[T]
no universal EntityRef/entity_id introduced
no model-generated SQL/ORM execution path
bootstrap contains composition, not orchestration
```

---

# 37. Feature / activation gates

| Capability | Build posture | Activation requirement |
|---|---|---|
| Search contracts/shell | BUILD-READY | no public activation claim |
| protected Search family | conditional | real data + auth/disclosure + PSV-06/SC-017 + family tests |
| Search HTTP | gated | authoritative Auth/AuthZ request context |
| structured semantic query family | conditional | owning semantics + permission/coherence proof + typed handler/tests |
| FTS/pg_trgm | OFF | measured need + DB same-change + PSV-07/SC-018 |
| vector/pgvector | OFF | eval need + lifecycle + PSV-08/SC-019 + PSV-37 + applicable freshness/deletion proofs |
| ModelAccess fake | test only | no production claim |
| provider qualification candidate | OFF | reviewed candidate admission |
| provider live route | OFF | adapter conformance + live compatibility + direct eval + applicable security/privacy/capacity gates |
| production Ask | OFF | Auth + sources/query path + provider qualification when used + verification/publication + evidence + audit/privacy gates |
| sensitive audit-required Search/Ask | OFF | minimum durable audit evidence plane exists |
| external streaming | OFF | delta-level publication/disconnect/cumulative disclosure proof |
| consequential Effect | OFF | I9 + target/policy/approval/transaction/idempotency/reconciliation proof |
| commercial/shared ledger | OFF | real enforcement requirement |
| durable Run/Restate | OFF | real workflow lifetime trigger + PSV-21..28B |
| AI memory | OFF | explicit owner/purpose/lifecycle trigger |
| prior-disclosure accounting | OFF | H19 real cross-Run/surface trigger |
| MCP/A2A | OFF | real capability/integration trigger |
| Execution Environment | OFF | generated/untrusted code/browser/computer-use threat-model trigger |

---

# 38. Build-ready / integration-ready / activation-ready

```text
BUILD-READY
= code/contracts can be implemented with accepted fakes/synthetic trusted contexts

INTEGRATION-READY
= required real owning seams/data/capabilities exist

ACTIVATION-READY
= user-visible path passed all applicable security/privacy/proof/ops/release gates
```

First implementation stages:

```text
I0 repository/application ownership + architecture-test skeleton
I1 Search public contracts/registry/application shell
I2 Intelligence pure contracts:
   Work/ContextStrategy/ReferenceResolution/SemanticQuery/RetrievalCandidate/
   Policy/Effect/Verification/Publication + deterministic fakes
I3 real deterministic Search/structured query families only when product data is materially ready
I4 provider candidate admission + inactive concrete adapter candidate
I5 conformance/live compatibility + direct DANTE qualification
I6 read-only Ask DANTE
I7 production hardening / observability / privacy / resource / rollout / audit as applicable
I8 scenario/planning proposal vertical
I9 first bounded consequential Effect vertical
I10 proactive/background/durable/external-agent capabilities only on real trigger
```

I0-I2 may proceed without production Auth/provider availability.

Public private-data Search/Ask may not.

---

# 39. Revised implementation dependency graph

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
    ReferenceResolution
    SemanticQueryGateway + deterministic fake/no-handler posture
    RetrievalPlan / RetrievalCandidate validation
    Verification / Publication / Effect NO_EFFECT
    RuntimeEvidencePort
    ↓
B5  route-config schema/loader/digest snapshot + resource/evidence seams
    ↓
P0  provider candidate discovery/shortlist
    ↓
P1  candidate admission artifact
    ↓
B6  one inactive candidate ProviderAdapter/ProviderBinding + dependency
    ↓
B7  adapter conformance + live compatibility
    ↓
B8  tooling/ai-evals using SAME production-owned composition
    + direct DANTE qualification
    + applicable capacity/security/privacy/economic proof
    ↓
B9  qualification/promotion decision
    ↓
B10 read-only Ask HTTP surface + final Safe Publication
    ↓
B11 production hardening/system acceptance/activation evidence
```

A provider candidate can be rejected at P1, B7, B8 or B9 without changing DANTE application semantics.

---

# 40. Candidate commit sequence

```text
C1  test(ai): establish architecture boundary checks for new modules
C2  feat(search): public contracts, eligibility, family registry, deterministic shell
C3  feat(search): bounded PostgreSQL adapter + real PG proof for first real family
C4  feat(search): inbound adapter/wiring behind Auth activation gate
C5  feat(ai): Work/ContextStrategy/ReferenceResolution/SemanticQuery/Retrieval contracts + fakes
C6  feat(ai): verification/publication/effect/runtime-evidence pure contracts
C7  feat(ai): route-config identity/loader + resource/evidence seams
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

# 41. Deferred responsibility ledger

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
→ model/provider never becomes mutation authority

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

H19 prior-disclosure survival
→ real cross-Run/surface cumulative-disclosure trigger

FTS/vector representations
→ measured retrieval need + exact direct proofs
```

---

# 42. Product completeness / launch boundary

The initial technical vertical is only:

```text
Global Search subset
+ read-only Ask DANTE
```

```text
I6 COMPLETE
!= V1 GLOBAL SEARCH & COMMAND COMPLETE
```

Product-owned later obligations include, where in accepted V1 scope:

```text
creation/modification commands
preview/validation
provenance/rationale
undo/recovery where supported
scenario proposal/approval
consequential effect governance
```

For public/other-user processing, the product privacy/legal release baseline remains applicable, including as required:

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

These remain release/governance responsibilities, not Intelligence-owned business semantics.

---

# 43. Explicit non-claims

```text
THIS CURRENT BASELINE ACCEPTED AFTER FINAL MEGA RETEST   NO / RETEST REQUIRED
AI-05 STRUCTURALLY CLOSED                               YES
modules/search implemented                              NO
modules/intelligence implemented                        NO
SemanticQueryGateway implemented                        NO
Auth/AuthZ integrated on this branch                    NO
provider candidate admitted                             NO
provider/model/SDK production-qualified                 NO
provider dependency added                               NO
direct provider eval executed                           NO
production capacity qualified                           NO
production Ask active                                   NO
external streaming active                               NO
PostgreSQL/Alembic changed                              NO
new AI table/index                                      NO
FTS/trgm/vector activated                               NO
conversation persistence selected                       NO
control-plane persistence selected                       NO
commercial/resource ledger implemented                  NO
Restate/R2/MCP/A2A activated                            NO
Execution Environment selected                          NO
```

---

# 44. Final acceptance gate for this baseline

Before status may become `CURRENT / ACCEPTED FOR IMPLEMENTATION ENTRY`:

```text
MKT-001..MKT-080 rerun from zero
C1..C15 compound collision suite PASS
reverse Product→Domain→Logical→Physical→PostgreSQL→AI-02→AI-03→AI-04→PRE05→AI-05→this baseline PASS
representative single-user + multi-actor simulation replay PASS
SC/PSV/eval proof applicability register internally consistent
no new Domain/Logical/Physical/PostgreSQL reopen
no generic AI persistence owner
no provider preselection
current routing repair completed only after PASS
```

Until then:

```text
IMPLEMENTATION I0 = HOLD
```
