# DANTE AI-05B — Concrete Implementation Blueprint Acceptance

- **Status:** CLOSED / STRUCTURALLY ACCEPTED
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-05 — Whole-System Acceptance + Implementation Blueprint
- **Sub-phase:** AI-05B — Concrete Implementation Blueprint
- **Closed:** 2026-09-02
- **Upstream:** AI-05A CLOSED / STRUCTURALLY ACCEPTED / BD-01..BD-41
- **Accepted hardening:** AI05B-H01..H15
- **Final destructive battery:** B05-01..B05-50 PASS
- **Compound collision suite:** PASS
- **Reverse pass:** AI-05B→AI-05A→AI-04→PRE-AI05→AI-03→AI-02 PASS
- **Implementation:** NONE
- **Provider/model/SDK selection:** OPEN / DIRECT-EVIDENCE GATED
- **Database change:** NONE
- **Alembic change:** NONE

This document is the durable closure authority for AI-05B.

The candidate and all bounded-hardening documents remain intentional evidence of the review chronology:

```text
dante-ai-05b-concrete-implementation-blueprint.md
→ original concrete candidate

dante-ai-05b-first-destructive-hardening.md
→ first destructive FAIL BOUNDED / AI05B-H01..H07

dante-ai-05b-second-destructive-hardening.md
→ fresh retest FAIL BOUNDED / AI05B-H08..H12

dante-ai-05b-third-destructive-hardening.md
→ full retest FAIL BOUNDED / AI05B-H13..H15

this document
→ final fresh acceptance authority
```

No historical failure is rewritten as an earlier PASS.

---

# 1. Closure chronology

```text
CONCRETE AI-05B CANDIDATE
→ materialized

FIRST DESTRUCTIVE PASS
→ FAIL BOUNDED
→ H01..H07

FRESH RETEST
→ FAIL BOUNDED
→ H08..H12

FULL RETEST
→ FAIL BOUNDED
→ H13..H15

FINAL FRESH RETEST FROM ZERO
→ B05-01..B05-50 PASS
→ compound collision suite PASS
→ reverse AI-05B→05A→04→PRE05→03→02 PASS
→ no upstream reopen
→ AI-05B CLOSED / STRUCTURALLY ACCEPTED
```

This is structural/build-contract acceptance. It is not a runtime, provider, model-quality, capacity, production-security or implementation PASS.

---

# 2. Accepted first implementation direction

The first implementation sequence remains intentionally narrow:

```text
I0 repository/application ownership skeleton
I1 Search public contract + bounded read projection
I2 pure Intelligence contracts + deterministic fakes
I3 deterministic Global Search vertical when at least one useful Search family is materially ready
I4 provider-neutral ModelAccessRuntime + one concrete adapter only after provider-selection gate
I5 adapter conformance + direct DANTE qualification
I6 read-only Ask DANTE vertical
I7 production hardening / observability / privacy / resource / rollout gates
I8 planning/scenario proposal vertical
I9 first bounded consequential effect vertical
I10 proactive/background/durable/external-agent capabilities only on real trigger
```

The first product envelope is:

```text
private authenticated in-app
single-turn
inline/request-owned
read-only
normal isolation
no durable Run
no background resume
no shared/external recipient
no consequential mutation
```

---

# 3. Accepted repository ownership

```text
apps/backend/src/dante/modules/search
→ sole owner of public Search application/query semantics
→ deterministic/no-model capable
→ SearchFamilyRegistry + permission-safe bounded read projection
→ no canonical mutation authority

apps/backend/src/dante/modules/intelligence
→ WorkContract / Context / Retrieval orchestration
→ ModelAccessRuntime consumption
→ Policy / Effect / RuntimeEvidence consumer boundaries
→ verification / Result Maturity / safe publication
→ imports Search through Search-owned public contracts only

provider SDK/protocol
→ private outbound provider adapter only
→ never application semantic owner

bootstrap
→ composition + process lifecycle only

platform
→ shared technical mechanics only

tooling/ai-evals
→ qualification tooling outside ordinary production request path
```

Explicitly rejected:

```text
generic Repository[T]
generic Entity/EntityRef for AI/Search convenience
arbitrary model-to-SQL
provider SDK in application/domain contracts
agent/orchestration framework as semantic owner
generic AI memory/conversation/Run table
raw SQLAlchemy session exposed to Intelligence/model code
```

---

# 4. Search contract closure

Accepted Search implementation contract includes:

```text
SearchService public protocol
SearchExecutionRequest
SearchEligibilityEnvelope
SearchFamilyRegistry
SearchFamilyRegistration
SearchResult
SearchTargetRef
bounded Search-owned PostgreSQL query adapter
```

Search family activation is explicit and evidence-driven.

```text
GLOBAL SEARCH PRODUCT REQUIREMENT
!= GENERIC QUERY OVER EVERY DATABASE TABLE
```

A family is active only when its real product/capability data, source/current/history semantics, authorization/disclosure projection and bounded query behavior are materially proven.

Current database identity shells such as Person or ContentArtifact are not artificially expanded merely to make AI/Search convenient.

Eligibility constrains the candidate universe before externally observable rank/count/facet/pagination behavior where non-interference requires it.

```text
query all private rows
→ rank/count/facet
→ post-filter
```

is not accepted as a general permission proof.

Search navigation preserves accepted DANTE reference families:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

through typed/discriminated `SearchTargetRef`; no universal semantic entity ID is introduced.

---

# 5. Intelligence / provider contract closure

Accepted application/runtime separation:

```text
IntelligenceService
→ ModelAccessPort
→ ModelAccessRuntime
→ private ProviderAdapter
→ provider SDK / HTTP protocol
```

```text
MODEL ACCESS PORT != PROVIDER ADAPTER
PROVIDER ADAPTER != ROUTING POLICY
PROVIDER ADAPTER != AUTHORITY
PROVIDER ADAPTER != EFFECT AUTHORITY
```

DANTE allocates `ProviderAttemptId` before dispatch.

Provider attempt semantics distinguish:

```text
completed
refused
pre-acceptance failure
timeout / ambiguous acceptance
cancellation requested
cancellation confirmed
execution quiesced
usage known
usage estimated
usage unknown
late usage evidence
```

Blind retry remains forbidden for indeterminate external outcomes unless the exact selected operation has independently proven safe retry/idempotency semantics.

Provider adapter conformance remains separate from live compatibility, DANTE direct eval and capacity qualification.

---

# 6. HTTP trust boundary

Accepted layering:

```text
UNTRUSTED HTTP DTO
→ authentication
→ route-owned purpose/surface
→ current Authority/AuthZ/Visibility/Consent projection
→ SearchEligibilityEnvelope / trusted RequestContext
→ WorkContract / trusted application request
→ application service
```

The client cannot set or upgrade:

```text
principal / represented-party authority
Authority/AuthZ basis
purpose escalation
provider/model/route
HarnessProfile
RouteConfigIdentity
ConsequenceProfile
Effect authorization
resource/commercial entitlement
```

Pydantic validation is structural validation only; it is not authorization.

---

# 7. Effect boundary closure

The first vertical is read-only but still crosses an explicit Effect boundary.

```text
READ_ONLY WorkContract
+ no proposed effects
→ EffectOutcome.NO_EFFECT
```

Any mutation/effect intent arriving under this envelope is rejected before mutation dispatch.

Thus:

```text
READ_ONLY
!= "we happened not to call a mutation today"
```

Provider/model code receives no canonical mutation authority.

---

# 8. Configuration / qualification closure

Behavior-bearing route configuration is static/versioned/typed first and must have material identity.

```text
RouteConfigIdentity
= logical revision + content digest
```

The loaded invocation snapshot binds to the exact validated artifact bytes, and CI/build/packaging must prove that the qualified artifact is the artifact delivered to runtime or independently qualify every material delta.

```text
ACTIVE POINTER != IMMUTABLE CONFIG REVISION
EVAL CANDIDATE != PRODUCTION ROUTE
QUALIFICATION STACK != MATERIAL PRODUCTION STACK
unless identity/delta proof exists
```

Emergency deny may make a route unusable without mutating historical route identity.

---

# 9. Runtime lifecycle closure

Every first-vertical abstract/runtime/evidence object has an explicit create/persist/mutate/delete-or-release/cache/retry/cancel posture.

Default remains:

```text
request-local runtime state
→ no persistence

operational evidence
→ only the minimum justified evidence plane

canonical semantic state
→ existing accepted PostgreSQL ownership only
```

No generic persistence is created for:

```text
WorkContract
Run
ContextPlan
ContextManifest
BasisManifest
SearchResult
ConsumerContext
ProviderAttempt
provider continuation
conversation
AI memory
embedding/vector representation
```

Any future survival must be independently earned by materiality/lifecycle/operational requirements.

---

# 10. Resource / evidence closure

Resource flow remains:

```text
estimate
→ admission/reservation when real authority exists
→ execute
→ collect provider usage evidence
→ settle/reconcile truthfully
```

Unknown or late provider usage cannot be silently converted to zero or guessed final cost.

Evidence planes remain distinct:

```text
canonical truth
!= audit/execution evidence
!= operational telemetry
!= eval/qualification evidence
```

`RuntimeEvidencePort` uses typed, minimized runtime events. Ordinary telemetry does not default to raw prompt, raw context, raw Search bodies or raw model responses.

---

# 11. Transaction / persistence closure

Current database contract remains unchanged.

```text
DATABASE CHANGE = NONE
ALEMBIC CHANGE = NONE
```

Search uses a bounded read scope backed privately by the existing database runtime; `AsyncSession` does not cross into Search public contracts or Intelligence.

No PostgreSQL transaction spans a provider call.

Future consequential canonical mutations remain owned by the outer application/effect transaction boundary; persistence adapters may flush but do not independently commit.

External provider outcomes remain non-atomic with PostgreSQL and require explicit reconciliation if they become consequential.

---

# 12. Final destructive battery

Final fresh structural cases:

```text
B05-01..B05-50
→ PASS / 50 OF 50
```

The final set covers at least:

```text
repository/path truth
Search vs Intelligence ownership
Search deterministic independence
permission-safe hidden-result non-interference
current/history/source semantics
miss != nonexistence
bounded query families
no raw DB/model authority
Context/Retrieval/Basis distinctions
stale basis
current policy revalidation
provider failure/ambiguous submit/cancellation
immutable route material identity
emergency deny
SDK confinement
resource unknown/late usage
explicit NO_EFFECT
no DB transaction across provider call
provider outage degradation
no generic AI persistence
Auth activation gate
safe publication
observability/evidence separation
material qualification composition
premature capability activation
architecture import rules
full lifecycle coverage
SearchFamilyRegistry materialization gate
single Search public contract
ProviderAdapter protocol
HTTP trust split
public callable protocols
reference-family preservation
no generic EntityRef/entity_id/table+uuid abstraction
```

Compound suite PASS includes:

```text
hidden Search row + pagination/facet/rank + target navigation
stale basis + current AuthZ change + Ask publication
client disconnect + ambiguous provider outcome + unknown usage + evidence exporter failure
emergency deny + in-flight attempt + late result + publication closed
malicious HTTP authority fields + family/provider hints + effect attempt
Search + provider outage + deterministic degradation
```

No new bounded hardening was required after AI05B-H15.

---

# 13. Reverse acceptance

Reverse order:

```text
AI-05B
→ AI-05A
→ AI-04
→ PRE-AI05
→ AI-03
→ AI-02.1
```

Result:

```text
PASS
```

Verified preservation includes:

```text
Search remains separate from Intelligence
provider mechanics remain behind DANTE contracts
MODEL OUTPUT != PUBLISHABLE OUTPUT
current authorization/disclosure remain authoritative
Context != Retrieval != Memory
ContextManifest != BasisManifest
NativeRef != ScopedRecordRef != MaterialStateRef != ExternalRef
APPROXIMATE != COMPLETE
provider state != canonical DANTE state
DEFAULT NONCANONICAL PERSISTENCE = NO
Effect authorization is not model authority
no Domain/Logical/Physical/PostgreSQL reopen
```

---

# 14. Closure verdict

```text
AI-05B CONCRETE IMPLEMENTATION BLUEPRINT
→ CLOSED / STRUCTURALLY ACCEPTED
```

Accepted hardening:

```text
AI05B-H01..H15
```

Still explicitly open:

```text
provider/model/SDK selection
live provider compatibility
DANTE direct model/route eval
production capacity qualification
real Search family product materialization
real Access/Auth integration seam
runtime implementation
production observability implementation
commercial/resource authority implementation
future consequential Effect implementation
future database evolution only when a real product vertical earns it
```

Next phase:

```text
AI-05 WHOLE-SYSTEM DESTRUCTIVE ACCEPTANCE / CLOSURE
```

Do not start production implementation merely because AI-05B is closed. Whole AI-05 must survive its final cross-subphase destructive acceptance first.
