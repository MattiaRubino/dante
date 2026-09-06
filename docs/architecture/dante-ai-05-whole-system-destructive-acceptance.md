# DANTE AI-05 — Whole-System Destructive Acceptance

- **Status:** CLOSED / STRUCTURALLY ACCEPTED
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-05 — Whole-System Acceptance + Implementation Blueprint
- **Closed:** 2026-09-02
- **AI-05A:** CLOSED / STRUCTURALLY ACCEPTED / BD-01..BD-41
- **AI-05B:** CLOSED / STRUCTURALLY ACCEPTED / AI05B-H01..H15 / B05-01..B05-50
- **Whole-system hardening:** AI05-H01
- **Whole-system retest:** W05-01..W05-10 PASS
- **Compound collision suite:** PASS
- **Reverse pass:** Product→Domain→Logical→Physical→PostgreSQL→AI-02→AI-03→AI-04→PRE-AI05→AI-05A→AI-05B PASS
- **Implementation:** NONE
- **Provider/model/SDK selection:** OPEN / DIRECT-EVIDENCE GATED
- **Database change:** NONE
- **Alembic change:** NONE

This document is the durable closure authority for AI-05 and the final architecture-to-build boundary for the current DANTE Intelligence design workstream.

AI-05 closure means the accepted system has a buildable implementation contract and survived destructive cross-subphase review. It does **not** mean that Search, Ask DANTE, provider integration, production controls, Access/Auth integration, observability, direct evals or any AI runtime are already implemented or production-active.

---

# 1. Closure chronology

```text
AI-05A ownership/build boundary
→ candidate
→ bounded hardening BD-31..BD-41
→ destructive T01..T26 + compounds + reverse PASS
→ CLOSED

AI-05B concrete implementation blueprint
→ candidate materialized
→ first destructive FAIL BOUNDED / H01..H07
→ fresh retest FAIL BOUNDED / H08..H12
→ full retest FAIL BOUNDED / H13..H15
→ final B05-01..B05-50 + compounds + reverse PASS
→ CLOSED

AI-05 whole-system composition
→ destructive composition FAIL BOUNDED
→ AI05-H01 BUILD-READY != INTEGRATION-READY != ACTIVATION-READY
→ W05-01..W05-10 + compounds PASS
→ reverse authority pass PASS
→ AI-05 CLOSED / STRUCTURALLY ACCEPTED
```

No historical bounded failure is rewritten as an earlier PASS.

---

# 2. Final accepted architecture-to-build shape

```text
HTTP / PRODUCT EDGE
        ↓
trusted application request construction
        ↓
SearchService and/or IntelligenceService
        ↓
WorkContract / Context / Retrieval / Policy
        ↓
Search public query boundary
        ↓
SearchFamilyRegistry + bounded permission-safe query adapter
        ↓
canonical PostgreSQL / accepted owning sources

and when a qualified model route is justified:

IntelligenceService
        ↓
ModelAccessPort
        ↓
ModelAccessRuntime
        ↓
private ProviderAdapter
        ↓
provider SDK / HTTP protocol
        ↓
verification / Result Maturity
        ↓
explicit Effect boundary
        ↓
safe publication
```

Binding separations remain:

```text
GLOBAL SEARCH != INTELLIGENCE ORCHESTRATION
MODEL ACCESS PORT != PROVIDER ADAPTER
MODEL OUTPUT != PUBLISHABLE OUTPUT
HTTP DTO != TRUSTED APPLICATION REQUEST
READ_ONLY != EFFECT BOUNDARY ABSENT
SEARCH TARGET != UNIVERSAL ENTITY ID
CONFORMANCE != DIRECT QUALIFICATION
BUILD-READY != INTEGRATION-READY != ACTIVATION-READY
```

---

# 3. Repository ownership accepted for implementation

```text
apps/backend/src/dante/modules/search
→ Search public protocol/contracts
→ SearchFamilyRegistry
→ bounded cross-capability read/query adapter
→ deterministic/no-provider capability
→ no canonical mutation authority

apps/backend/src/dante/modules/intelligence
→ WorkContract / Context / Retrieval orchestration
→ Policy / Resource / Effect / RuntimeEvidence consumer seams
→ ModelAccessRuntime
→ verification + Result Maturity + safe publication
→ consumes Search through Search-owned public surface

apps/backend/src/dante/bootstrap
→ composition and lifecycle only

apps/backend/src/dante/platform
→ genuinely shared technical mechanics only

provider SDK/protocol
→ private selected adapter implementation only

tooling/ai-evals
→ qualification tooling outside production request path
```

No monolithic generic `core`, `ai`, `common`, `entity`, `repository`, `memory`, `run` or provider-owned application layer is authorized by AI-05.

---

# 4. First implementation workstream

The implementation order is accepted as:

```text
I0  repository/application ownership skeleton
I1  Search public contract + bounded adapter shell
I2  pure Intelligence contracts + deterministic fakes
I3  deterministic Global Search when at least one useful Search family is materially ready
I4  one concrete provider adapter only after provider-selection evidence gate
I5  provider adapter conformance + direct DANTE qualification
I6  read-only Ask DANTE
I7  production hardening / privacy / observability / resource / rollout
I8  planning/scenario proposal vertical
I9  first bounded consequential Effect vertical
I10 proactivity/background/durable/external-agent capabilities only on real trigger
```

The first implementation workstream may begin with I0/I1/I2 immediately after AI-05 closure, subject to normal repository engineering gates.

That does not make the public first vertical activation-ready.

---

# 5. Readiness classes

```text
BUILD-READY
= implementation/testing of accepted contracts may begin

INTEGRATION-READY
= real owning seams/data/capabilities exist and may be wired

ACTIVATION-READY
= user-visible/production path passed every applicable policy,
  privacy, security, qualification, operational and release gate
```

Examples:

```text
Search module shell
→ BUILD-READY

Global Search product route
→ requires at least one useful permission-safe Search family
  + authoritative current eligibility/Auth seam

Ask application contracts
→ BUILD-READY

real model-assisted Ask
→ requires selected/eligible provider binding
  + adapter conformance
  + direct DANTE qualification
  + material config identity
  + current Auth/AuthZ
  + safe publication/resource/rollout gates
```

No temporary production authority, fake Search family or preference-based provider selection is permitted to bridge a readiness gap.

---

# 6. Search closure

Search remains a shared product capability independent from model availability.

Accepted implementation concepts:

```text
SearchService
SearchExecutionRequest
SearchEligibilityEnvelope
SearchFamilyRegistry
SearchFamilyRegistration
SearchResult
SearchTargetRef
bounded PostgresSearchQueryAdapter
```

Search family activation is explicit and capability-driven.

```text
SEARCH FAMILY ID != TABLE NAME
GLOBAL SEARCH != DATABASE CATALOG SEARCH
```

Current PostgreSQL identity shells do not gain generic title/text/search columns for AI convenience.

Hidden/ineligible records may not affect visible rank/count/facet/pagination semantics where this would leak their existence.

Search references preserve:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

No universal `EntityRef`, `entity_id`, table-name+UUID or model-guessed owner type is introduced.

---

# 7. Provider / runtime closure

Concrete provider/model/SDK choice remains open.

A future selected route must preserve:

```text
ModelTarget != Provider != Model != Deployment
HarnessProfile != ProviderBinding
ProviderAttemptId = DANTE-owned technical attempt identity
provider IDs = correlation/evidence only
```

Provider adapter failures distinguish pre-acceptance transient failure from indeterminate/possibly accepted outcomes.

```text
OUTCOME UNKNOWN
→ no blind replay
→ reconcile/reread where applicable
```

Cancellation remains:

```text
requested != confirmed != quiesced
```

Request-local cleanup may outlive the HTTP socket within the bounded process/request deadline, without inventing durable Run persistence.

A later requirement to survive process crash is an independent durability trigger.

---

# 8. Trust / policy / effect closure

The public HTTP client cannot forge:

```text
principal / represented-party authority
Authority/AuthZ basis
purpose escalation
SearchEligibilityEnvelope
provider/model/route
HarnessProfile / RouteConfigIdentity
ConsequenceProfile
Effect authorization
resource entitlement
```

Trusted application context is server-owned after authentication/current authorization resolution.

The first vertical explicitly finalizes through Effect:

```text
READ_ONLY + no proposed effect
→ EffectOutcome.NO_EFFECT
```

Any mutation intent under that envelope is rejected before dispatch.

Later consequential effects must reuse owning application mutation semantics and outer transaction ownership; provider/model code never owns canonical mutation.

---

# 9. Configuration / evidence / qualification closure

Behavior-bearing route configuration is versioned, typed and material-identity bound:

```text
RouteConfigIdentity = revision + digest
```

Qualification must identify the material route composition it proves.

```text
APPLICATION FAKE
!= PROVIDER ADAPTER CONFORMANCE
!= LIVE PROVIDER COMPATIBILITY
!= DANTE DIRECT EVAL
!= PRODUCTION CAPACITY QUALIFICATION
```

The production composition must equal the qualified composition or every material delta must be independently qualified.

Operational evidence uses typed minimized runtime events. Canonical truth, audit/execution evidence, telemetry and eval evidence remain separate planes.

---

# 10. Persistence / transaction closure

Current answer remains:

```text
DATABASE CHANGE = NONE
ALEMBIC CHANGE = NONE
```

No generic persistence is introduced for:

```text
conversation
Run
WorkContract
Context
ContextManifest
BasisManifest
SearchResult
ProviderAttempt
AI memory
embedding/vector index
Attention
```

Search SQL/SQLAlchemy mechanics remain private to the Search adapter/read-scope boundary.

No PostgreSQL transaction spans provider execution.

Persistence adapters in later consequential flows may flush; outer application/effect transaction owns commit/rollback.

External/provider outcomes are not atomically rollbackable with PostgreSQL.

A real later product vertical may justify normal forward database evolution through the existing PostgreSQL same-change process without reopening AI-05.

---

# 11. Whole-system destructive acceptance

Final whole-system cases:

```text
W05-01..W05-10
→ PASS / 10 OF 10
```

Accepted compound cases include:

```text
I0-I2 implementation while Access/Auth integration is unavailable
Search module exists while zero useful Search families are ready
provider fake/conformance exists before any provider is selected
provider selected but direct route qualification missing
valid HTTP request arrives without authoritative current Auth seam
future product Search capability requires legitimate schema evolution
```

Correct outcomes preserve readiness gates rather than inventing shortcuts.

---

# 12. Final reverse authority check

Reverse/authority reconciliation result:

```text
Product / North Star
→ Domain
→ Whole Logical
→ Physical
→ PostgreSQL Constitution + current database
→ AI-02.1
→ AI-03
→ AI-04
→ PRE-AI05
→ AI-05A
→ AI-05B
→ AI-05 whole-system closure

PASS
```

No new universal semantic root, canonical owner, generic persistence layer, provider ontology, shadow authorization model or database exception was required.

---

# 13. Final verdict

```text
AI-05 — WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT
→ CLOSED / STRUCTURALLY ACCEPTED
```

Current AI architecture design/reengineering workstream is therefore structurally complete through the architecture-to-build boundary.

Next:

```text
ACTUAL AI IMPLEMENTATION WORKSTREAM
→ begin I0
→ then I1
→ then I2
→ advance later steps only when their integration/activation prerequisites become real
```

Still open and not claimed by this closure:

```text
runtime/backend implementation
Search implementation
Intelligence implementation
provider/model/SDK selection
live provider tests
direct DANTE eval
capacity qualification
production AI activation
Access/Auth integration
production observability/control plane
commercial/resource authority
new AI persistence
new PostgreSQL/Alembic change
```
