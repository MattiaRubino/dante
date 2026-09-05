# DANTE AI-05A — Whole-System Build Boundary Acceptance

- **Status:** CLOSED / STRUCTURALLY ACCEPTED
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-05 — Whole-System Acceptance + Implementation Blueprint
- **Sub-phase:** AI-05A — Whole-System Build Boundary / Ownership Map
- **Closed:** 2026-09-02
- **Upstream:** AI-02.1 / AI-03 / AI-04 / PRE-AI05 CLOSED / STRUCTURALLY ACCEPTED
- **Current core eval:** DANTE-E01..DANTE-E14
- **Accepted build hardening:** BD-01..BD-41
- **Implementation:** NONE
- **Provider/model/SDK selection:** OPEN
- **Database change:** NONE

This document is the durable AI-05A closure authority.

Pre-closure evidence remains intentionally separate and truthful:

```text
docs/architecture/dante-ai-05a-whole-system-build-boundary.md
→ original candidate + first destructive-pass evidence + BD-31..BD-40

docs/architecture/dante-ai-05a-eval-production-composition-hardening.md
→ second-pass bounded failure + BD-41
```

Those files remain evidence of how the boundary was tested. This acceptance document owns current AI-05A status.

---

## 1. Closure chronology

```text
INITIAL AI-05A CANDIDATE
→ T01..T26 destructive pass
→ FAIL BOUNDED
→ Search/Intelligence ownership, read projection, resource seam,
  config lifecycle, zero-persistence envelope and test-plane gaps found
→ BD-31..BD-40 materialized

SECOND PASS
→ T01..T26 individual cases PASS candidate
→ compound/reverse qualification seam FAIL BOUNDED
→ eval tooling could otherwise qualify a materially different stack
→ BD-41 materialized

FINAL FRESH PASS
→ T01..T26 rerun from zero PASS
→ compound collision suite PASS
→ direct-eval/material-production-composition case PASS
→ reverse AI-05A→AI-04→PRE-AI05→AI-03→AI-02 PASS
→ no new generic owner / persistence root / provider lock-in found
→ AI-05A CLOSED / STRUCTURALLY ACCEPTED
```

No failure was erased from history and no PASS was inferred from documentation alone before the final retest.

---

## 2. Accepted repository ownership map

AI-05A accepts the following implementation direction for the first buildable slice.

```text
apps/backend/src/dante/modules/search
→ shared Global Search / discovery capability
→ deterministic/no-model capable
→ permission/disclosure/current/history/source semantics
→ bounded cross-capability read projection where necessary
→ no canonical business ownership
→ no mutation authority

apps/backend/src/dante/modules/intelligence
→ DANTE intelligence application/orchestration boundary
→ WorkContract / Context / route consumption / model-assisted orchestration
→ verification / Result Maturity / safe publication coordination
→ consumes Search and owning capability public seams
→ no whole-product canonical ownership

provider SDK / protocol
→ private outbound adapter behind DANTE-owned ModelAccessPort

bootstrap
→ composition / lifecycle only

platform
→ genuinely shared technical mechanics only

resource/commercial authority
→ owns shared/commercial quota/metering truth when activated
→ Intelligence consumes admission/reservation/settlement

tooling/ai-evals
→ engineering qualification tooling outside ordinary production request path
```

```text
RESPONSIBILITY BOUNDARY != MODULE != SERVICE != TABLE
```

Folders/classes are created only when implementation requires them.

---

## 3. Search remains independent from Intelligence

Binding:

```text
GLOBAL SEARCH / DISCOVERY
!= INTELLIGENCE ORCHESTRATION
```

Search is a separately useful V1 product capability and must remain available for deterministic structured/current/history discovery and canonical navigation without model/provider initialization.

A bounded Search-owned cross-capability read adapter may query accepted PostgreSQL structures directly for search/discovery when owning capability modules/public read contracts do not yet exist.

```text
SEARCH CROSS-CAPABILITY READ PROJECTION
!= CANONICAL OWNER
!= GENERIC Repository[T]
!= UNIVERSAL Entity API
!= MODEL-TO-SQL
!= MUTATION BYPASS
```

Consequential actions originating from a Search result leave Search and enter the owning application/effect boundary.

---

## 4. Intelligence application boundary

`modules/intelligence` is accepted as the initial application/orchestration owner for replaceable intelligence behavior, not a new canonical Domain root.

It may own runtime/application contracts required for:

```text
Work intake / WorkContract execution
run-local orchestration
Context planning/readiness orchestration
ModelTarget / deterministic-vs-model route request
qualified route-composition consumption
model-assisted capability orchestration
verification
result maturity
publication coordination
Attention/proactivity orchestration only when later activated
```

It does not own:

```text
calendar/goals/people/health/work canonical state
Global Search canonical/read ownership
whole-product SQLAlchemy persistence
Auth/Authority truth
commercial subscription truth
provider SDK semantics
conversation database
```

AI-specific nouns do not enter `kernel/` merely because many AI files use them.

---

## 5. Provider seam

Binding direction:

```text
DANTE intelligence application
→ DANTE-owned ModelAccessPort
→ provider adapter
→ provider SDK / HTTP protocol
```

The port represents DANTE requirements and is not forced into a lowest-common-denominator `generate(prompt) -> str` abstraction.

```text
PROVIDER SDK != APPLICATION CONTRACT
```

No provider gateway, LiteLLM, Portkey, LangGraph or agent framework is mandatory before direct evidence demonstrates value.

One-primary-provider V1 remains compatible with later provider replacement.

---

## 6. Route/config/control boundary

Accepted route composition remains upstream AI-04 authority:

```text
WorkContract + current consequence/eligibility
→ ModelTarget / deterministic need
→ eligible qualified route compositions
→ Routing Policy
→ compatible HarnessProfile + ProviderBinding + feature/control composition
→ route-specific resource admission
→ current egress authorization
→ provider adapter
```

Initial control posture:

```text
STATIC / VERSIONED / TYPED FIRST
DYNAMIC CONTROL-PLANE STORAGE ONLY WHEN OPERATIONAL NEED PROVES IT
```

Behavior-bearing route/Harness/policy configuration requires immutable/versioned identity and reviewable approved selection.

```text
BEHAVIOR-BEARING CONFIG != SCATTERED ENV VARS
COHERENT INVOCATION CONFIG != PERPETUAL AUTHORIZATION
COHERENT INVOCATION CONFIG != IMMUNITY FROM EMERGENCY DENY
```

A dynamic control-plane database/admin surface is activated only when safe production operation cannot be met by the simpler versioned mechanism.

---

## 7. Resource/commercial seam

Binding:

```text
INTELLIGENCE
→ estimate / admission / reservation / settlement requests

RESOURCE / COMMERCIAL AUTHORITY
→ shared/commercial durable quota/metering truth when activated

PROVIDER ADAPTER
→ provider usage evidence
→ no entitlement decision
```

```text
COMMERCIAL QUOTA != PROVIDER QUOTA != PLATFORM CAPACITY
PROVIDER TOKEN COUNT != COMMERCIAL CREDIT
```

The first technical slice may operate without production commercial metering. Once cross-request/shared/commercial quota is enforced, its minimum durable accounting must exist under the proper owner.

---

## 8. Persistence acceptance

AI-03C remains binding:

```text
DEFAULT NONCANONICAL PERSISTENCE = NO
ARCHITECTURE CONTRACT != PERSISTENCE OWNER
```

For the initial bounded slice, default runtime state remains ephemeral/request-owned:

```text
WorkContract
inline Run state
ContextPlan / InformationNeed
ContextFragment / ContextReadiness
ConsumerContext
```

Evidence/config state remains explicitly classified rather than automatically persisted.

No generic persistence is justified now for:

```text
conversation history
InteractionSession
Run registry
AI memory
Context
Search results
embeddings/vector state
Attention state
```

unless a later product/security/durability requirement triggers the minimum justified state.

```text
ZERO NEW GENERIC AI TABLES
!= ZERO DURABLE TECHNICAL STATE FOREVER
```

H19 prior-disclosure accounting, durable audit, commercial metering, resume/background work and similar cases independently trigger their required survival state before those cases become eligible.

---

## 9. First implementation vertical

Accepted first vertical composition:

```text
GLOBAL SEARCH
DETERMINISTIC / READ-ONLY / CANONICAL NAVIGATION

+

ASK DANTE
READ-ONLY MODEL-ASSISTED SYNTHESIS WHEN NEEDED
+ SOURCE / PROVENANCE / CURRENTNESS
+ NO CONSEQUENTIAL MUTATION
```

Initial activation envelope:

```text
surface          private authenticated in-app
recipient        current resolved user/Actor context
interaction      single-turn
runtime          inline / request-owned
effect           read-only
reasoning        deterministic OR bounded model-assisted
topology         single / bounded sequential
isolation        normal
background       none
durable resume   none
external effects none
shared/lock/voice/external recipient surfaces OUT OF INITIAL ENVELOPE
H19-required cross-Run accounting cases       OUT UNTIL MINIMUM STATE EXISTS
```

```text
INLINE STREAM != DURABLE RUN REGISTRY REQUIRED
CHAT-LIKE UI != GENERIC CONVERSATION DATABASE REQUIRED
```

Provider outage must not take deterministic Global Search down.

---

## 10. Subsequent vertical order

Accepted direction after the read-only slice:

```text
1. Global Search deterministic baseline
2. Ask DANTE read-only
3. production hardening / direct qualification
4. planning / replanning / Scenario proposal
5. bounded consequential effect
6. proactivity / background / durability / external-agent / isolation
   only on their real triggers
```

Planning/scenario precedes broad autonomous mutation.

Scenario runtime remains no-store by default; accepted durable state promotes to the appropriate existing DANTE owner rather than becoming a generic AI scenario database.

---

## 11. Eval / production composition boundary — BD-41

Eval tooling remains outside the ordinary product request path, but qualification cannot test a materially different provider stack and then promote the result to production.

Binding:

```text
QUALIFICATION EVIDENCE MUST EXERCISE THE SAME MATERIAL PRODUCTION
COMPOSITION THAT WILL BE PROMOTED, OR EVERY MATERIAL DELTA MUST BE
INDEPENDENTLY QUALIFIED BEFORE PROMOTION.
```

Material composition includes, where applicable:

```text
ModelTarget
HarnessProfile
ProviderBinding
ProviderAdapter / protocol translation
feature mode
structured-output/tool projection
security/guard/data transformations
retry/fallback behavior material to the route
```

```text
SAME MATERIAL COMPOSITION != SAME PUBLIC HTTP ENTRYPOINT
EVAL TOOLING OUTSIDE REQUEST PATH != SECOND PROVIDER INTEGRATION STACK
```

`tooling/ai-evals` may depend on or invoke production-owned route components through a bounded qualification seam. Production application/runtime modules must not depend on eval tooling.

Any material production delta requires independent evidence before promotion.

Qualification artifacts identify the exact material route composition and material-delta evidence they support.

---

## 12. Evidence planes

The following remain distinct:

```text
APPLICATION FAKE
!= PROVIDER ADAPTER CONFORMANCE
!= LIVE PROVIDER SMOKE / COMPATIBILITY PROOF
!= DIRECT DANTE MODEL/ROUTE EVAL
!= PRODUCTION CAPACITY QUALIFICATION
```

Purpose:

```text
application fake
→ deterministic application behavior

adapter conformance
→ provider protocol / translation behavior

live smoke
→ current endpoint / feature compatibility

direct DANTE eval
→ workload quality + hard semantic/privacy/safety gates

production capacity qualification
→ intended service envelope / reliability / operational viability
```

No evidence plane inherits another plane's proof claim.

---

## 13. Testing/build placement direction

Candidate build placement accepted for AI-05B refinement:

```text
apps/backend/tests/unit
→ pure Search/Intelligence application contracts

apps/backend/tests/integration
→ Search read projection with real PostgreSQL where applicable
→ wiring
→ provider adapter conformance after selection

tooling/ai-evals
→ DANTE-E01..E14 direct/stochastic qualification

tests/system
→ real cross-app black-box surfaces once materialized
```

Architecture tests must enforce at least:

```text
Domain/application does not depend directly on provider SDK
Intelligence does not import Search private persistence adapter
model-facing code never receives raw DB session/SQLAlchemy authority
production code does not depend on tooling/ai-evals
module public-boundary dependency rules remain acyclic
```

---

## 14. Direct activation gates remain open

AI-05A does not activate any of these:

```text
provider/model/SDK
direct paid provider eval
production provider route
FTS / pg_trgm
pgvector / ANN
embedding model
Restate
R2
MCP
A2A
Execution Environment
dynamic control-plane persistence
commercial/shared usage ledger
conversation persistence
prior-disclosure persistence
```

They remain evidence/trigger gated under AI-03/04/PRE-AI05.

---

## 15. Final destructive acceptance result

Final retest after BD-41:

```text
T01..T26                                      PASS / 26 OF 26
Search + Intelligence + provider outage       PASS
Search hidden-result + Ask synthesis          PASS
config rollout + invocation + emergency deny  PASS
quota + retry/failover + settlement            PASS
inline stream + disconnect / no durable Run   PASS
cumulative privacy + zero-persistence gate     PASS
direct eval + production composition/deltas    PASS
reverse AI-05A→04→PRE05→03→02                 PASS
```

Acceptance interpretation:

```text
unexplained ownership gap      NONE
hidden mutation/data bypass    NONE FOUND
fake zero-persistence claim    NONE AFTER ENVELOPE GATING
provider lock-in               NONE REQUIRED
new canonical AI owner         NONE
new generic persistence root   NONE
broad upstream reopen          NONE
```

This is a structural/documentation acceptance, not runtime proof.

---

## 16. AI-05A accepted invariants

`BD-01..BD-40` from the original candidate remain accepted, plus:

```text
BD-41
QUALIFICATION EVIDENCE MUST EXERCISE THE SAME MATERIAL PRODUCTION
COMPOSITION THAT WILL BE PROMOTED, OR EVERY MATERIAL DELTA MUST BE
INDEPENDENTLY QUALIFIED BEFORE PROMOTION.
```

Where this closure document is stronger than the original candidate status/next-action wording, this closure document governs current AI-05A truth.

---

## 17. Explicit non-claims

```text
AI-05A CLOSED / STRUCTURALLY ACCEPTED      YES
AI-05 WHOLE PHASE CLOSED                   NO
AI-05B STARTED                             NO
modules/search IMPLEMENTED                 NO
modules/intelligence IMPLEMENTED           NO
kernel CREATED                             NO
provider/model/SDK SELECTED                NO
direct provider eval EXECUTED              NO
production capacity PASS                   NO
API/stream transport SELECTED              NO
AI backend/frontend IMPLEMENTED            NO
PostgreSQL/Alembic CHANGED                 NO
new AI table/index                         NO
conversation persistence SELECTED          NO
control-plane persistence SELECTED         NO
commercial/resource ledger IMPLEMENTED     NO
FTS/vector/pgvector ACTIVATED              NO
Restate/R2/MCP/A2A ACTIVATED               NO
Execution Environment SELECTED             NO
commercial pricing/billing IMPLEMENTED     NO
```

---

## 18. Next phase — AI-05B

AI-05B is now the exact next sub-phase.

It must freeze the buildable implementation contracts without starting production implementation:

```text
concrete module public boundaries
ports and runtime DTO/types
Search read/query contracts
ModelAccessPort contract
provider adapter conformance contract
route/config artifact schemas
resource admission/settlement seams
HTTP + streaming/publication shape for first vertical
runtime-only vs evidence/persistence ownership
exact test layout
qualification artifact schema
feature/activation gates
implementation dependency graph
first build gates / commit sequence
```

AI-05B must use the AI-05A accepted ownership map rather than reopening it for implementation convenience.

Provider/model selection remains direct-evidence gated. If a concrete API choice cannot responsibly be frozen without live proof, AI-05B identifies the exact decision gate and proof artifact instead of guessing.
