# DANTE Intelligence — Final Implementation Baseline

- **Status:** CURRENT / ACCEPTED FOR IMPLEMENTATION ENTRY
- **Branch:** `feature/ai-architecture`
- **Accepted:** 2026-09-02
- **Acceptance authority:** `dante-ai-post05-final-mega-acceptance.md`
- **Post-AI05 hardening:** POST05-H01..H25
- **Fresh destructive battery:** MKT-001..MKT-100 PASS
- **Compound suite:** C01..C20 PASS
- **Reverse authority pass:** PASS
- **Product/simulation replay:** PASS
- **Implementation:** NONE YET
- **Provider/model/SDK:** OPEN / EVIDENCE-DRIVEN
- **Database change:** NONE
- **Alembic change:** NONE
- **Current next action:** I0 — repository/application ownership + architecture-test skeleton

This is the single current implementation-facing authority for DANTE Intelligence.

Historical AI-05 candidates, AI-05B hardenings, post-AI05 baseline v1/v2/v3 files and kill-test documents remain evidence. They must not override this baseline.

The implementation workstream may begin at I0, but build-ready does not mean integration-ready or activation-ready.

---

# 1. Authority stack

This baseline consumes without redefining:

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
post-AI05 final mega acceptance
```

Repository/executable truth outranks this file if a later accepted implementation deliberately evolves architecture through normal project governance.

Binding invariants include:

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
SEARCH RESULT / CURSOR / TARGET REF != AUTHORIZATION TOKEN
AUXILIARY MODEL INFERENCE != FREE PROVIDER CALL
```

---

# 2. Repository and database truth at implementation entry

Current backend source remains foundation-heavy:

```text
apps/backend/src/dante/
├── bootstrap/
└── platform/
    ├── config/
    ├── database/
    └── recovery/
```

Target paths are not pre-existing implementation claims:

```text
apps/backend/src/dante/modules/search
apps/backend/src/dante/modules/intelligence
tooling/ai-evals
apps/backend/config/intelligence/revisions
```

Create paths only when the corresponding implementation step has real content.

Current dependencies remain:

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

A later real product capability may justify normal forward database evolution through the existing same-change process. AI convenience alone does not.

---

# 3. Capability ownership

## Search

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
```

## Intelligence

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

Intelligence does not own canonical capability state, Auth/AuthZ truth, commercial accounting, raw SQLAlchemy authority or provider SDK semantics.

## Provider

Concrete provider SDK/protocol code may exist only inside an admitted private outbound binding adapter.

Candidate placement:

```text
apps/backend/src/dante/modules/intelligence/adapters/outbound/models/<binding>/
```

No provider SDK types appear in public/application contracts.

## Bootstrap / platform / tooling

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

This is not a mandate for one file/class per architecture noun.

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

Trusted `SearchExecutionRequest` carries only:

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

It cannot carry raw SQL, ORM classes, table names, caller-created authority decisions, provider/model route or Effect authorization.

`SearchResult` preserves:

```text
safe hits
safe facets/counts when allowed
pagination
achieved guarantee
limitations/unresolved classification
source/currentness/basis-safe metadata
```

`SearchHit` uses typed `SearchTargetRef`, never universal `entity_id`.

Search miss means:

```text
NO ELIGIBLE RESULT FOUND UNDER THIS QUERY + ACCESS + GUARANTEE
```

not canonical nonexistence.

---

# 6. Search eligibility, non-interference and publication

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

Unauthorized/ineligible rows may not affect externally visible hit presence, snippet, count, facet, rank/order, page exhaustion, navigation or practical hidden-state oracle behavior.

Search has a real response/publication boundary:

```text
QUERY ELIGIBLE AT T1
!= AUTOMATICALLY PUBLISHABLE AT T2
```

Before emitting material private Search data, revalidate access/source/currentness according to the family's requirements.

A cursor:

```text
!= AuthZ token
!= frozen permission snapshot
```

Every paged request constructs current eligibility. Cursor data is minimized/integrity-protected and must not embed hidden content or privileged policy state.

A `SearchTargetRef` is an address/navigation hint only. Opening the target rechecks current owning-capability authorization/visibility.

Source retirement/deletion between query and response cannot be silently published as current.

---

# 7. SearchFamilyRegistry and references

Each `SearchFamilyRegistration` freezes at least:

```text
family_id
owning capability/product boundary
canonical/source semantics
supported public query modes
current/history/source-reread support
maximum truthful guarantee
safe result projection schema
SearchEligibilityEnvelope requirements
bounded query implementation identity
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

Search navigation preserves:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

through typed/discriminated `SearchTargetRef`.

No universal `EntityRef`, table+UUID wrapper or model-guessed owner identity is introduced.

---

# 8. Semantic Query / Projection Gateway

Search discovery is not sufficient for all structured DANTE questions.

`SemanticQueryGateway` is an orchestration responsibility only.

Conceptual surface:

```text
SemanticQueryGateway.execute(
    InformationNeed,
    ContextStrategy,
    TrustedRequestContext,
) -> SemanticQueryOutcome
```

Allowed sources are:

```text
owning capability public typed query contract
or
explicitly accepted capability-owned read projection
```

Search's cross-capability read projection remains Search/discovery-specific.

`SemanticQueryGateway` cannot own raw SQL, ORM classes, AsyncSession, table names, arbitrary model predicates or cross-capability private persistence adapters.

If no owning/public typed query seam exists:

```text
SemanticQueryOutcome = UNSUPPORTED / NOT_INTEGRATION_READY
```

not a direct DB bypass.

`SemanticQueryOutcome` preserves typed payload, achieved guarantee, source/reference bindings, currentness, basis/coherence evidence, source standing and limitations.

Correct deterministic path:

```text
question
→ bounded semantic interpretation
→ InformationNeed
→ structured/deterministic ContextStrategy
→ SemanticQueryGateway
→ owning capability query
→ typed result
→ verification
→ safe publication
```

No model is required merely to calculate a deterministic answer DANTE already owns.

---

# 9. Reference / Target Resolution

Material referents are resolved explicitly where unique/exact binding is required.

Conceptual outcomes:

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

Reference resolution operates over the eligible candidate universe before externally visible ambiguity/count/label/clarification behavior.

Hidden same-name candidates must not create visible ambiguity.

Any model-assisted resolver call uses the ordinary governed ModelAccess/egress/resource/eval path.

---

# 10. Work / execution / result maturity

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

Request-local `ExecutionStatus` includes:

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

`ResultMaturity` includes:

```text
PROVISIONAL
VERIFIED
PUBLISHABLE
REJECTED
```

```text
PROVIDER COMPLETED != VERIFIED != PUBLISHABLE
```

`RequestExecutionScope` owns deadline, attached tasks, cancellation signal, active provider attempts, request-local egress state, publication-open/closed and bounded cleanup state.

Process-crash survival is a separate durability trigger.

---

# 11. Full Context contract

Preserve all seven AI-03A contracts:

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

`ContextPlan` preserves Work binding, purpose, Actor/represented party, Reality Scope, Runtime Interpretation Frame, known targets, unresolved resolution requirements, protected needs, exclusions, privacy compartment and resource constraints.

`InformationNeed` preserves requirement/origin/scope, target/subject/time, Reality Scope, interpretation frame, purpose, reference-resolution requirement, criticality, coverage, acceptable source semantics, freshness/coherence/fidelity and status.

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

Relevant `ContextStrategy` families include:

```text
STRUCTURED_CURRENT_QUERY
MATERIAL_HISTORY_QUERY
RELATION_TRAVERSAL
DERIVED_PROJECTION
DETERMINISTIC_AGGREGATION
SEARCH_DISCOVERY
DIRECT_SOURCE_READ
LEXICAL/FUZZY when activated
SEMANTIC/HYBRID when activated
DIRECT_LONG_CONTEXT when justified
INTERACTION/RUN context when activated
SCENARIO_CONTEXT when activated
OPEN_WORLD/JIT when activated
```

Reality Scope remains explicit:

```text
CANONICAL_CURRENT
MATERIAL_HISTORICAL / AS_OF
SCENARIO when activated
OPEN_WORLD_ASSERTION when activated
explicit MIXED only when legitimate
```

Runtime Interpretation Frame preserves reference instant, timezone/offset, day/calendar/DST semantics, locale/units and spatial anchor where material.

---

# 12. Retrieval contract

```text
InformationNeed
→ ContextStrategy
→ RetrievalPlan
→ acquisition route
→ RetrievalCandidate
→ validation
→ ContextFragment
```

`RetrievalPlan` preserves source set/classes, exclusions, guarantee, currentness/coherence/fidelity, permitted transformations, budget, stopping criteria and refinement ceiling.

Retrieval guarantees remain:

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

A `RetrievalCandidate` is runtime candidate state, not Context/truth by rank. It preserves source/lineage/representation/mechanism/currentness/reality/security metadata required for validation.

Only validated candidate material becomes `ContextFragment`.

Any model-based query rewrite/decomposition is an auxiliary governed model call and cannot widen purpose/security/reference scope.

---

# 13. Source standing, instruction provenance and transforms

Context representations preserve source provenance, standing, integrity, canonicality, sensitivity/derived sensitivity, lifecycle, Reality Scope, interpretation applicability, instruction provenance and contradiction/conflict.

```text
DATA != INSTRUCTION
USER CONTENT != CURRENT USER INSTRUCTION AUTOMATICALLY
TRANSFORMED DATA != TRUSTED INSTRUCTION AUTOMATICALLY
```

Source content cannot create new purpose, Authority/AuthZ/Consent, InformationNeed outside scope, provider/tool capability, Effect authorization or disclosure permission.

Harness/provider projection preserves role separation.

```text
MASKING / REDACTION != SEMANTIC EQUIVALENCE
```

If an input transformation materially changes target/context meaning, the transformed semantics actually sent to the provider govern readiness/verification.

If output DLP/redaction materially changes a verified result, the final recipient representation is rechecked and may require re-verification/limitation.

External guard/security/DLP services are governed data recipients.

```text
GUARDRAIL RESULT != DANTE AUTHORITY
```

---

# 14. Context readiness / exposure / basis

`ContextReadiness` may be:

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

`ContextManifest` records actual or conservatively possible consumer/provider exposure at the material send boundary according to available evidence.

Provider success is not required for exposure to exist.

`BasisManifest` tracks material dependencies/currentness/coherence used to justify the result.

```text
ContextManifest != BasisManifest
```

No generic persistence is created for either in the first vertical.

---

# 15. Request-local egress / cumulative disclosure

Every material provider/helper/guard attempt creates request-local `EgressAttempt` state.

Conceptual fields include:

```text
egress_attempt_id
work/invocation/ProviderAttempt binding
recipient/provider binding
purpose
ConsumerContext/projection identity
egress/disclosure policy basis
send state
acceptance certainty where knowable
exposure occurrence: NOT_SENT | POSSIBLE | ESTABLISHED
provider outcome state
```

```text
provider timeout/failure != exposure did not occur
```

Every retry/failover/new provider attempt re-evaluates current provider/data eligibility, Work/currentness, alternate context, request-local prior exposures, cumulative disclosure, resource admission and route qualification.

Server-side multi-provider hedging is OFF by default.

Cross-Run prior-disclosure persistence remains OFF until H19's real trigger exists.

---

# 16. Intelligence and HTTP public boundary

`modules/intelligence/public.py` owns:

```text
class IntelligenceService(Protocol):
    async def ask(AskExecutionRequest) -> AskResult: ...
```

`AskExecutionRequest` is trusted/server-constructed and cannot carry caller-selected provider/model/route/Effect authority.

`AskResult` exists only after verification + safe publication and may expose only safe answer/limitation, safe sources/provenance, safe currentness/basis summary and model-assisted indicator.

HTTP layering:

```text
untrusted HTTP DTO
→ structural validation
→ authentication
→ route-owned purpose/surface
→ current Authority/AuthZ/Visibility/Consent projection
→ trusted RequestContext / SearchEligibilityEnvelope
→ WorkContract/application request
```

Client cannot forge principal/represented-party authority, policy basis, purpose escalation, provider/model/route, HarnessProfile, RouteConfigIdentity, ConsequenceProfile, Effect authorization, resource entitlement or SQL/model/table authority.

Candidate routes:

```text
POST /api/v1/search
POST /api/v1/ask
```

Private-data activation waits for authoritative integrated Auth/AuthZ.

---

# 17. First-vertical routes

Deterministic Search:

```text
HTTP Search
→ trusted request
→ SearchService
→ eligible family
→ bounded read source
→ guarantee/coherence/currentness
→ final current-access publication check
→ safe SearchResult
```

Deterministic semantic Ask:

```text
HTTP Ask
→ WorkContract
→ ContextPlan / InformationNeed
→ ReferenceResolution when needed
→ structured ContextStrategy
→ SemanticQueryGateway
→ owning capability typed query
→ VerificationResult
→ Effect NO_EFFECT
→ publication/currentness
→ AskResult
```

Model-assisted Ask:

```text
HTTP Ask
→ WorkContract / Context / retrieval
→ validated ContextFragments
→ ContextReadiness
→ ConsumerContext
→ current egress policy
→ eligible qualified route
→ Resource admission
→ request-local cumulative-disclosure check
→ ModelAccessPort
→ EgressAttempt + ContextManifest
→ VerificationResult
→ ResultMaturity
→ Effect NO_EFFECT
→ Basis/currentness revalidation
→ output transform recheck if any
→ PublicationDecision
→ AskResult
```

---

# 18. ModelAccessPort and auxiliary inference

Application-owned port:

```text
ModelAccessPort.invoke(ModelInvocationRequest, CancellationSignal)
    -> ModelInvocationResult
ModelAccessPort.stream(ModelInvocationRequest, CancellationSignal)
    -> AsyncIterator[ModelEvent]
ModelAccessPort.cancel(ProviderAttemptId)
    -> CancellationOutcome
```

First public Ask is non-streaming.

`ModelInvocationRequest` binds Work/Invocation identity, ModelTarget, ConsumerContext, HarnessProfile requirement, feature/capability projection, structured-output need, deadline/retry budget, RouteConfigIdentity and security/data-eligibility basis.

`ModelInvocationResult` preserves attempt summary, completion/outcome, structured payload, usage evidence, capability usage, finish/stop classification, acceptance uncertainty, latency/timestamps and classified error.

Provider background/stored/continuation/native-tool/cache modes remain OFF unless separately qualified.

Every auxiliary inference—intent parser, reference resolver helper, query rewrite, router, reranker, summarizer, verifier/judge, advisor—uses the same governed ModelAccess/egress/resource/eval path.

No helper imports provider SDK directly.

---

# 19. Provider adapter and error semantics

`ModelAccessRuntime` allocates DANTE `ProviderAttemptId` before dispatch.

Private adapter:

```text
ProviderAdapter.invoke(...)
ProviderAdapter.stream(...)
ProviderAdapter.cancel(...)
```

The adapter owns protocol translation only; it does not own routing, authority, egress policy, Effects, DB access or commercial entitlement.

Normalized state distinguishes completed/refused/pre-acceptance failure/ambiguous acceptance, cancellation states and usage known/estimated/unknown/late.

Application error taxonomy includes:

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

Provider-adapter taxonomy includes rate-limit/timeout/invalid-response/disconnect/indeterminate/cancellation/deadline distinctions.

First HTTP mapping remains disclose-safe: hidden/existence-sensitive cases may return filtered/empty/limitation behavior instead of revealing internal denial reason.

---

# 20. Candidate admission / qualification / conformance

Provider lifecycle:

```text
P0 discovery/shortlist
P1 candidate admission for qualification
P2 inactive material adapter/binding
P3 adapter conformance
P4 live compatibility/feature proof
P5 direct DANTE eval using production-owned material composition
P6 capacity/reliability/security/privacy/economics evidence as applicable
P7 qualification decision
P8 canary/production promotion
```

Candidate admission is not production eligibility.

Before private/sensitive data eligibility, live qualification uses synthetic/public/minimized fixtures where sufficient.

Shadow/canary traffic is real disclosure.

Production promotion requires the same material composition intended for production or independent proof for every material delta.

Adapter conformance covers normal response, rate limit, pre-acceptance failure, ambiguous timeout, invalid structured response, stream disconnect, cancellation races, usage present/absent, unsupported feature and refusal.

Conformance proves protocol normalization only.

---

# 21. Retry / fallback / cancellation

DANTE owns the effective retry budget.

Provider SDK/gateway automatic retries are disabled or every material wire/provider attempt is visible/accounted under DANTE attempt/resource/disclosure/evidence semantics.

Every resource-consuming attempt requires current admission. Every data-egress attempt creates/evaluates corresponding egress exposure.

```text
safe pre-acceptance transient failure
→ bounded retry MAY be allowed

possible accepted/processed state + lost response
→ OUTCOME UNKNOWN
→ no blind replay
```

Provider refusal cannot trigger refusal-shopping.

Fallback re-evaluates current eligibility, Work/currentness, alternate Harness/Binding/capability/context, cumulative disclosure, resource admission and qualification. Alternate context is rebuilt/minimized; request bytes are not blindly replayed.

```text
cancel requested != cancel confirmed != execution quiesced
```

---

# 22. Route/config identity

Behavior-bearing config is static/versioned/typed first.

Target source:

```text
apps/backend/config/intelligence/revisions/<revision>.json
```

`RouteConfigIdentity` = logical revision + content digest.

Minimum artifact includes ModelTargets, HarnessProfiles, ProviderBindings, route policies, feature modes, qualification requirements, control profiles, retry/fallback references and applicable resource/security/rollout references.

Secrets are not config payload.

Deployment settings may supply approved active selector, endpoint/deployment locator, region, credential ref, emergency selector and environment limits, but cannot become hidden behavior policy.

```text
ACTIVE POINTER != IMMUTABLE CONFIG REVISION
COHERENT INVOCATION CONFIG != PERPETUAL AUTHORIZATION
```

CI/build/packaging proves qualified config bytes are delivered or independently qualifies material deltas.

---

# 23. Policy and resource seams

Policy consumer methods:

```text
authorize_context_exposure(...)
authorize_model_egress(...)
authorize_effect(...)
authorize_publication(...)
```

Policy decisions preserve basis identity, principal/recipient/surface, purpose, obligations, revalidation requirement and internal reason code.

No temporary X-User-Id/fake-auth production bypass is allowed.

Resource consumer methods:

```text
estimate(...)
admit(...)
settle(...)
```

```text
UNKNOWN USAGE != ZERO USAGE
ESTIMATE != FINAL COST
PROVIDER TOKEN != COMMERCIAL CREDIT
COMMERCIAL QUOTA != PROVIDER QUOTA != PLATFORM CAPACITY
```

Shared/commercial accounting is activated only with a real durable owner/requirement.

---

# 24. Verification / Effect / publication

`VerificationResult` statuses include:

```text
VERIFIED
LIMITED
CONFLICTED
STALE
REJECTED
INSUFFICIENT_EVIDENCE
NEEDS_REREAD
```

Verification prefers deterministic/application evidence where available.

First Effect boundary:

```text
READ_ONLY + proposed_effects=[]
→ EffectOutcome.NO_EFFECT
```

Mutation intent is rejected before any mutation adapter/transaction.

Future effects reuse owning application mutation semantics and outer transaction ownership; no PostgreSQL business transaction spans provider/network execution.

`PublicationDecision` rechecks current Work/supersession, Auth/AuthZ/Consent/Visibility, recipient/surface, disclosure, cumulative exposure where material, ResultMaturity, Verification, Basis/currentness, policy/emergency deny and final transformed representation.

First public Ask is non-streaming.

---

# 25. Operational non-interference and evidence

Protected state must not become a practical oracle through error, fallback, provider identity exposure, latency class, counts/limits, resource behavior or retry behavior where material.

Raw provider/security/policy errors do not flow directly to recipients when they reveal protected state/internal policy.

`RuntimeEvidencePort` uses typed minimized events for Work, Search, semantic query, reference resolution, context readiness, basis, policy, route, resource, provider attempts, egress exposure, verification, Effect and publication.

Default telemetry excludes raw private request body, ConsumerContext, hidden Search candidates/counts, model response, source content and secrets.

```text
CANONICAL DATA
!= AUDIT/EXECUTION EVIDENCE
!= OPERATIONAL TELEMETRY
!= EVAL/QUALIFICATION EVIDENCE
```

Ordinary telemetry exporter failure is operational degradation; it does not create canonical failure or permission to weaken safety/privacy.

Mandatory security/audit/effect evidence is a distinct plane and may fail closed according to its owner.

Sensitive audit-required cases remain activation-gated until a durable audit owner/integrity/retention/access contract exists.

---

# 26. PostgreSQL query coherence

Database default remains `READ COMMITTED`.

Every Search/semantic family declares maximum truthful guarantee, coherence requirement, snapshot requirement and currentness rule.

Where one coherent snapshot is required, use the least-complex valid method:

```text
single statement / CTE
or
explicit per-operation stronger isolation such as REPEATABLE READ
or
another accepted owner/material-basis mechanism
```

No global isolation escalation is authorized by AI.

If required coherence cannot be established, downgrade/label the guarantee.

---

# 27. Runtime/persistence classification

Request-local/no-store by default:

```text
WorkContract / ExecutionStatus
ContextPlan / InformationNeed / ContextStrategy
ReferenceResolution request/result
SemanticQuery request/outcome
RetrievalPlan / RetrievalCandidate
ContextFragment / ContextReadiness / ConsumerContext
ContextManifest / BasisManifest
Search request/result/page/cursor state
ordinary PolicyDecision
request-local ResourceAdmission
ModelInvocation request/result
ProviderAttempt / EgressAttempt
VerificationResult / ResultMaturity
EffectOutcome.NO_EFFECT
PublicationDecision/Result
```

Durable noncanonical evidence/artifacts only when justified:

```text
route/config revisions
qualification evidence
operational telemetry
security/audit evidence when independently required
```

Independent trigger required for:

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

# 28. Lifecycle rules

Every materialized first-vertical object has explicit creation, request-local persistence/no-store, immutable/versioned mutation rules, release/expiry, cache/reuse and retry/cancel semantics.

Key rules:

```text
WorkContract immutable; material relaxation -> derived/superseding Work
ContextPlan/Strategy explicit replan, not silent mutation
ReferenceResolution/SemanticQuery/RetrievalCandidate results immutable
ConsumerContext rebuilt on material route/context change
ContextManifest records exposure and is not retry authority
BasisManifest rebuilt after reread/revalidation
PolicyDecision re-evaluated after material change
RouteConfigSnapshot immutable per invocation
retry -> new ProviderAttemptId
retry/fallback -> new/current ResourceAdmission + EgressAttempt
VerificationResult/PublicationDecision immutable per evaluated representation
```

Any future survival proposal re-enters AI-03C materiality/lifecycle rules.

---

# 29. Pending direct-proof register

| Proof | Trigger | Initial status |
|---|---|---|
| PSV-06 / SC-017 hidden-result non-interference | first protected Search/semantic/reference family | PENDING when applicable |
| PSV-07 / SC-018 FTS mixed filter/query | FTS/pg_trgm serving | N/A until activated |
| PSV-08 / SC-019 vector filtered recall/relevance | ANN/vector serving | N/A until activated |
| PSV-09 / SC-020 projection freshness/material basis | served derived/current projection | PENDING when applicable |
| PSV-10 / SC-021 deletion/redaction propagation | surviving derived representation/index | PENDING when applicable |
| PSV-21..28B durable/Restate proofs | Class-B durable execution | N/A until activated |
| PSV-37 pgvector provenance | pgvector/embedding serving | N/A until activated |

`N/A` requires an explicit absent capability/feature-mode reason.

Missing evidence is not N/A.

---

# 30. Qualification artifact

Every promotable route composition has immutable evidence containing at least:

```text
schema_version
qualification_id
created_at
git_sha
release/build identity
route_config_revision + digest
ModelTarget / HarnessProfile / ProviderBinding identities
ProviderAdapter identity/version
feature mode
policy/control revisions
security/data transformation revisions
retry/fallback/hedging composition
SDK/gateway retry configuration
DANTE eval suite/version + applicable hard-gate results
SC/PSV applicability/status register
provider conformance evidence
live compatibility evidence when required
qualification fixture/data-class disclosure classification
capacity/reliability evidence when required
privacy/security/data eligibility evidence
cost/usage evidence
material deltas from prior qualification
revalidation/expiry conditions
qualification decision
promotion status
```

No blanket PASS may hide skipped applicable cases.

---

# 31. Test topology and architecture checks

Target tests:

```text
apps/backend/tests/unit/modules/search/
apps/backend/tests/unit/modules/intelligence/
apps/backend/tests/unit/test_architecture_boundaries.py
apps/backend/tests/integration/modules/search/
apps/backend/tests/integration/modules/intelligence/
apps/backend/tests/integration/providers/<binding>/
tooling/ai-evals/
tests/system/
```

Mandatory implementation checks include:

```text
Search does not import Intelligence
Intelligence imports Search only via public Search surface
Intelligence does not import Search private PostgreSQL adapter
Intelligence/application does not import SQLAlchemy/DB mappings
SemanticQueryGateway cannot own cross-capability SQL
ReferenceResolver cannot leak hidden candidate ambiguity
provider SDK imports only inside admitted private binding adapter
auxiliary model helpers cannot import provider SDK directly
ProviderAdapter cannot import inbound HTTP schemas or DB mappings
production cannot import tooling/ai-evals
HTTP DTOs cannot carry authority/provider/effect authoritative fields
no generic Repository[T]
no universal EntityRef/entity_id
no model-generated SQL/ORM execution
bootstrap contains composition, not orchestration
telemetry cannot masquerade as audit
```

Existing backend CI remains binding:

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

# 32. Dependency/framework lock

Allowed initial direction:

```text
existing FastAPI/Pydantic inbound/config
existing SQLAlchemy/psycopg PostgreSQL infrastructure
stdlib internal contracts/orchestration where sufficient
one admitted provider SDK/protocol only inside private adapter after candidate admission
```

Forbidden without independent evidence:

```text
LangChain/LangGraph-style semantic ownership
agent framework as DANTE owner
mandatory provider gateway
MCP framework for ordinary first vertical
new vector/search database
generic Repository/UoW framework
ORM/model-to-SQL tool
unreviewed dynamic control-plane database
```

---

# 33. Activation gates

| Capability | Activation requirement |
|---|---|
| Search shell/contracts | buildable now; no public activation claim |
| protected Search family | real data + Auth/disclosure + PSV-06/SC-017 + family tests |
| protected reference resolution | eligible-universe/non-interference proof + typed tests |
| Search HTTP | authoritative Auth/AuthZ + final currentness behavior |
| structured semantic query | owning public query seam + permission/coherence proof |
| FTS/pg_trgm | measured need + DB same-change + PSV-07/SC-018 |
| vector/pgvector | eval need + lifecycle + PSV-08/SC-019 + PSV-37 + freshness/deletion proofs |
| ModelAccess fake | tests only |
| provider candidate | reviewed candidate admission |
| live private provider route | processor/data/security/privacy + conformance + live/direct eval + capacity as applicable |
| auxiliary model inference | same governance/qualification as material inference |
| production Ask | Auth + source/query path + qualified route when used + verification/publication/evidence/audit/privacy |
| sensitive audit-required case | minimum durable audit plane |
| external streaming | delta-level publication/disconnect/cumulative-disclosure proof |
| multi-provider hedging | explicit privacy/security/cost/operational qualification |
| consequential Effect | later I9 proof set |
| durable Run/Restate | real Class-B trigger + PSV-21..28B |
| AI memory | explicit owner/purpose/lifecycle trigger |
| cross-Run disclosure accounting | H19 real trigger |
| MCP/A2A | real integration trigger |
| Execution Environment | generated/untrusted code/browser/computer-use trigger |

---

# 34. Readiness classes and implementation order

```text
BUILD-READY
= accepted contracts may be coded/tested with fakes/synthetic trusted contexts

INTEGRATION-READY
= required real owning seams/data/capabilities exist

ACTIVATION-READY
= user-visible path passed every applicable security/privacy/proof/ops/release gate
```

Implementation order:

```text
I0 repository/application ownership + architecture-test skeleton
I1 Search public contracts/registry/application shell
I2 Intelligence pure contracts + deterministic fakes
I3 real deterministic Search/structured families only when owning data/seams are ready
I4 provider candidate admission + inactive adapter candidate
I5 conformance/live compatibility + direct DANTE qualification
I6 read-only Ask DANTE
I7 production hardening / observability / privacy / resource / rollout / audit
I8 scenario/planning proposal vertical
I9 first bounded consequential Effect vertical
I10 proactive/background/durable/external-agent capabilities only on real trigger
```

I0-I2 may begin without production Auth/provider availability.

Public private-data Search/Ask may not.

---

# 35. Implementation dependency graph / commit sequence

Dependency graph:

```text
B0 architecture tests
→ B1 Search contracts/registry
→ B2 bounded PostgreSQL Search adapter + PG proof
→ B3 Search inbound behind Auth gate

B4 Intelligence pure contracts
→ B5 config/policy/resource/evidence seams
→ P0 provider shortlist
→ P1 candidate admission
→ B6 inactive adapter/binding
→ B7 conformance + live compatibility on safe data
→ B8 production-owned direct eval + applicable qualification
→ B9 qualification/promotion decision
→ B10 read-only Ask HTTP
→ B11 production hardening/system acceptance
```

Candidate commit sequence:

```text
C1  test(ai): architecture boundary checks
C2  feat(search): public contracts/eligibility/registry/shell
C3  feat(search): bounded PostgreSQL adapter + first family proof
C4  feat(search): inbound/wiring behind Auth gate
C5  feat(ai): Work/Execution/Context/Reference/SemanticQuery/Retrieval contracts + fakes
C6  feat(ai): Policy/Resource/Verification/Publication/Effect/Egress/Evidence contracts
C7  feat(ai): route-config identity/loader/digest snapshot
C8  chore(ai): provider candidate-admission decision
C9  feat(ai): admitted inactive provider adapter + conformance/live compatibility
C10 test(ai): direct DANTE qualification
C11 chore(ai): qualification/promotion decision
C12 feat(ai): read-only Ask DANTE + safe publication
C13 test(ai): Search/Ask system/failure/privacy/operational hardening
```

No database migration commit is planned for this baseline.

---

# 36. Deferred responsibility ledger

Inactive responsibilities remain explicit:

```text
Interaction Session / rich continuity
→ future real multi-turn need

Work Supersession across requests
→ real continuing Work lifecycle

Scenario Workspace / Solver
→ I8 / no-store default / OR-Tools only on trigger

Capability Runtime / ChangeSet / EffectGraph
→ I9 consequential work

Attention / proactivity / notification
→ I10 trigger-gated

Class-B durable / Restate
→ request lifetime insufficient + direct durable proofs

Execution Environment
→ generated/untrusted code/browser/computer-use threat model

MCP / A2A / external agents
→ real adapter/capability trigger

AI memory persistence
→ explicit owner/purpose/retention/lifecycle trigger

cross-Run prior-disclosure state
→ H19 real trigger

FTS/vector representations
→ measured need + direct proof
```

---

# 37. Product completeness / launch boundary

Initial technical vertical:

```text
Global Search subset
+ read-only Ask DANTE
```

```text
I6 COMPLETE != V1 GLOBAL SEARCH & COMMAND COMPLETE
```

Accepted Product V1 later includes creation/modification commands, preview/validation, provenance/rationale, undo/recovery where supported, scenario proposal/approval and consequential effect governance.

For public/other-user processing, Product privacy/legal release obligations remain applicable, including DPIA/governance, processor/DPA/subprocessor posture, retention/data-flow inventory, special-category legal basis/Consent, transfer/residency safeguards, privacy notice/terms/user controls, medical-purpose boundary and qualified privacy/legal review where required by Product authority.

---

# 38. Final non-claims

```text
IMPLEMENTATION BASELINE ACCEPTED             YES
POST-AI05 MEGA PASS                          YES / STRUCTURAL
I0 BUILD ENTRY                               AUTHORIZED
modules/search implemented                   NO
modules/intelligence implemented             NO
Auth/AuthZ integrated on this branch         NO
provider candidate admitted                  NO
provider/model/SDK production-qualified      NO
direct provider eval executed                NO
production capacity qualified                NO
production Search/Ask active                 NO
external streaming active                    NO
PostgreSQL/Alembic changed                   NO
new AI table/index                           NO
FTS/trgm/vector activated                    NO
conversation persistence selected            NO
control-plane persistence selected           NO
commercial/resource ledger implemented       NO
Restate/R2/MCP/A2A activated                 NO
Execution Environment selected               NO
```

Current next action:

```text
ACTUAL AI IMPLEMENTATION WORKSTREAM
→ I0
→ repository/application ownership + architecture-test skeleton
```
