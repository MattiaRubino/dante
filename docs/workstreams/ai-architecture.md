# DANTE AI Architecture Workstream

- **Status:** ACTIVE / BRANCH-LOCAL DURABLE WORKSTREAM RECORD
- **Branch:** `feature/ai-architecture`
- **Current phase:** AI-04 — Productionization Architecture
- **AI-04A:** CANDIDATE MATERIALIZED / DIRECT EVAL DESIGN CURRENT
- **AI-03 overall:** CLOSED / STRUCTURALLY ACCEPTED
- **AI-03A:** CLOSED / C01..C33
- **AI-03B:** CLOSED / B01..B35
- **AI-03C:** CLOSED / MAT-01..MAT-15
- **Implementation claim:** NONE
- **Provider/model selection:** OPEN / EVIDENCE-DRIVEN
- **Merge status:** UNMERGED

This document is the durable branch-local continuation record for the DANTE AI architecture workstream. It describes current branch scope, accepted architecture checkpoints, what must not be casually reopened, the current roadmap and the exact next design boundary.

It is not a chat transcript and must not duplicate all evidence already preserved in architecture/checkpoint documents.

---

## 1. Branch identity

```text
repository  MattiaRubino/dante
branch      feature/ai-architecture
```

Protected `main` remains integrated authority for closed shared foundations and the current PostgreSQL baseline. This workstream owns only its bounded newer AI architecture truth until normal protected-main integration.

A new chat/session does not create a new AI branch. Continue this real workstream on this branch unless explicitly deciding otherwise.

---

## 2. Mandatory reading order for continuation

Before making architecture or repository changes in this workstream, read:

```text
README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md

docs/development/agent-operating-manual.md
docs/development/operating-rules.md
docs/development/documentation-and-handoff.md
docs/development/documentation-lifecycle-policy.md
docs/development/branching-and-environments.md
docs/development/repository-engineering-safety.md

this file

docs/workstreams/ai-architecture-live-handoff.md
  only while it exists on the active branch

current AI architecture sources relevant to the phase
current branch/ref and relation to protected main
```

For AI-04, accepted/current AI authority includes:

```text
docs/architecture/dante-ai-foundation.md
docs/architecture/ai-production-engineering-state-of-the-art-2026.md
docs/architecture/dante-ai-02-1-intelligence-reengineering.md
docs/architecture/dante-ai-03-context-retrieval-memory.md
docs/architecture/dante-ai-03a-full-context-architecture.md
docs/architecture/dante-ai-03b-retrieval-memory-architecture.md
docs/architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md
docs/architecture/dante-ai-04-productionization-architecture.md
```

Repository truth beats conversation memory.

---

## 3. Accepted upstream foundation

AI work consumes, rather than reinterprets casually:

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL
CLOSED

LOGICAL MODEL
CLOSED / 57 OF 57
WL-H01..WL-H12 BINDING

PHYSICAL MODEL
CLOSED / ACCEPTED
PostgreSQL 18 major family
sole canonical persistence + material-history authority

BACKEND CP1–CP5
CLOSED / INTEGRATED

CP6 CONCRETE POSTGRESQL DATABASE
CLOSED / INTEGRATED

CURRENT POSTGRESQL
18.6
Alembic 20260830_09
69 tables / 5 views / 15 routines / 76 triggers /
97 indexes / 69 FKs / 123 CHECKs

POSTGRESQL LOCAL RECOVERY
CP01–CP07 LOCAL PASS / CLOSED / INTEGRATED
remote backup provider TBD / NOT ACTIVATED
production/cloud recovery NOT CLAIMED
```

No AI convenience may create a second canonical database, universal Entity/Fact/Memory ontology or generic semantic root around these accepted contracts.

---

## 4. Current AI roadmap

The old exploratory AI-00..AI-12 decomposition is no longer current routing. Git/evidence preserve its historical planning value.

Current compact roadmap:

```text
AI-00 — SEMANTIC & PRODUCT FOUNDATION
COMPLETE

AI-01 — PRODUCT FORM + PRODUCTION ENGINEERING RESEARCH
COMPLETE

AI-02 — INTELLIGENCE RUNTIME ARCHITECTURE
COMPLETE / STRUCTURALLY ACCEPTED
AI-02.1 v0.5

AI-03 — CONTEXT / RETRIEVAL / MEMORY
CLOSED / STRUCTURALLY ACCEPTED
  AI-03A Full Context Architecture
           CLOSED / C01..C33
  AI-03B Retrieval + Memory Architecture
           CLOSED / B01..B35
  AI-03C Destructive Validation + Materialization Blueprint
           CLOSED / MAT-01..MAT-15

AI-04 — PRODUCTIONIZATION ARCHITECTURE
ACTIVE / CURRENT
  AI-04A eval/model/provider productionization boundary
           CANDIDATE MATERIALIZED
           direct eval specification CURRENT
  concrete runtime/capabilities/external intelligence
  security/privacy/persistence/control-plane/operations

AI-05 — WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT
FUTURE / FINAL ARCHITECTURE-TO-BUILD BOUNDARY

THEN
ACTUAL AI IMPLEMENTATION WORKSTREAM(S)
```

Security, privacy, simulations and eval thinking remain cross-cutting requirements throughout the workstream; later dedicated assurance/acceptance passes validate concrete decisions rather than introducing those concerns for the first time.

---

## 5. AI-00 / AI-01 accepted foundation

Durable AI-00 source:

- `docs/architecture/dante-ai-foundation.md`

Completed AI-01 production-engineering evidence:

- `docs/architecture/ai-production-engineering-state-of-the-art-2026.md`.

Important retained direction:

```text
ONE DANTE / MANY SURFACES / ONE SEMANTIC REALITY
Ask / Work / Watch / Resolve
Interaction Session continuity
provider independence without lowest-common-denominator design
context as runtime resource
capability registry/discovery/runtime separation
deterministic compute first-class
verification separate from model self-report
effects explicit
security/information flow explicit
sandbox/isolation by workload/threat model
no automatic microservice explosion
```

Research technologies remain challengers/evidence unless explicitly selected later.

---

## 6. AI-02 — structurally accepted runtime architecture

Durable source:

- `docs/architecture/dante-ai-02-1-intelligence-reengineering.md`

AI-02.1 completed four destructive/pressure-test rounds plus targeted v0.5 verification.

Accepted structural responsibilities include:

```text
Interaction Edge
Interaction Session
Work Intake
WorkContract
Work Supersession
Reference / Target Resolution
ConsequenceProfile
Semantic Query / Projection Gateway
Context Engine
Scenario Workspace
BasisManifest
ModelTarget / HarnessProfile
Deterministic Compute
Solver
Capability Runtime
Execution Environment
Verifier
Policy mesh
ChangeSet / EffectGraph
Effect Runtime
Application / Domain boundary
Result Maturity
Disclosure
Safe Result Publication
Attention
```

Critical invariants include:

```text
Interaction Session != Run != Worker
DISPLAY NAME != EFFECT TARGET
MODEL OUTPUT != PUBLISHABLE OUTPUT
INTERNAL STREAM != RECIPIENT STREAM
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
CANCEL RUN != UNDO ALREADY-DISPATCHED EFFECTS
SCENARIO STATE != CANONICAL CURRENT STATE
CHANGESET != BYPASS OF INDIVIDUAL EFFECT GOVERNANCE
CONTEXT ACCESS != DISCLOSURE PERMISSION
DANTE representation != external System-of-Record authority
SENT != DELIVERED != SEEN != ACKNOWLEDGED != ACCEPTED
EXECUTION ENVIRONMENT != MANDATORY SANDBOX/CONTAINER
FRESH INPUTS != AUTOMATICALLY COHERENT COMBINED BASIS
APPROVAL != PERPETUAL AUTHORIZATION FOR MATERIALLY CHANGED WORK
CACHE HIT != CURRENT DISCLOSURE AUTHORIZATION
```

AI-02 is architecture acceptance only. It is not backend/runtime/provider implementation PASS.

Do not reopen AI-02 broadly merely because AI-04 later selects a concrete provider/runtime technique. Reopen only the smallest affected boundary if direct evidence reveals a real contradiction.

---

## 7. AI-03 — CLOSED Context / Retrieval / Memory architecture

Durable authority:

- `docs/architecture/dante-ai-03-context-retrieval-memory.md`
- `docs/architecture/dante-ai-03a-full-context-architecture.md`
- `docs/architecture/dante-ai-03b-retrieval-memory-architecture.md`
- `docs/architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md`

### AI-03A — Full Context Architecture

**CLOSED / C01..C33.**

Accepted Context contracts:

```text
ContextPlan
InformationNeed
ContextStrategy
ContextFragment
ContextReadiness
ConsumerContext
ContextManifest
+ inherited BasisManifest
```

Final Context invariants include Reality Scope, bounded model-discovered needs, per-need reference resolution, source/use exclusions, child/delegated minimisation, instruction provenance, non-monotonic readiness, exposure/currentness separation, multimodal derivative discipline and provider-state compartmentation.

### AI-03B — Retrieval + Memory Architecture

**CLOSED / B01..B35.**

Accepted retrieval/memory posture includes:

```text
RetrievalPlan / RetrievalCandidate
coverage-aware RetrievalGuarantee
EXACT / BOUNDED_COMPLETE / BEST_EFFORT / APPROXIMATE / SAMPLED
APPROXIMATE != COMPLETE
permission-safe Retrieval Eligibility Envelope
rank/similarity/rerank != Source Standing
source reread / current-state validation
query rewrite/expansion integrity
document/representation lifecycle

canonical application memory remains Domain/PostgreSQL
Interaction / Run / adaptive / operational / provider memory separated
Memory survival defaults to NO
Memory exists != memory may be recalled
retention/future-reuse eligibility distinct from current processing
user-specific durable reusable memory inspectable/controllable
correction / forgetting / source-use-inference suppression separated
canonical promotion cannot leave duplicate noncanonical authority
provider/cache/index state replaceable and source-lifecycle bound
```

### AI-03C — Destructive Validation + Materialization Blueprint

**CLOSED / MAT-01..MAT-15.**

Accepted materialization posture includes:

```text
ARCHITECTURE CONTRACT != PERSISTENCE OWNER
DEFAULT NONCANONICAL PERSISTENCE = NO
semantic authority != functional role != survival disposition != physical owner
Durable Execution Runtime State != PostgreSQL canonical state
Class-A durable technical coordination != Class-B durable execution
DURABLE JOURNAL != PRIVACY-FREE RUNTIME
persistent derivative requires truthful/scalable source basis
ASYNC INVALIDATION != CURRENT ELIGIBILITY
recomputable derived state is sacrificial during recovery
runtime/provider/derived recovery cannot outrun canonical readiness
ANN is optimization, not prerequisite
representation generations do not mix silently
serving generation requires build/catch-up/readiness/atomic cutover
semantic obligation != execution/audit evidence
```

AI-03 closure requires:

```text
Domain reopen                       NO
Logical reopen                      NO
Physical target reopen              NO
PostgreSQL Constitution reopen      NO
PostgreSQL/Alembic change           NO
new generic memory/search/Run table NO
pgvector/ANN activation             NO
FTS/trigram activation              NO
Restate/R2 activation               NO
provider/model selection            NO
implementation PASS                 NOT CLAIMED
```

SC-017..SC-021 and applicable PSV direct proofs remain unexecuted until real activated consumers make them applicable.

Do not rerun generic AI-03 mega-tests without concrete contradictory downstream evidence.

---

## 8. AI-04 — CURRENT Productionization Architecture

Durable candidate authority:

- `docs/architecture/dante-ai-04-productionization-architecture.md`

AI-04 converts the accepted responsibility architecture into concrete production choices without jumping directly into production implementation.

### 8.1 AI-04A candidate — eval/model/provider boundary

The first AI-04A materialization fixes the selection method before selecting a vendor.

Candidate DANTE workload families:

```text
DANTE-E01  model avoidance / deterministic fast path
DANTE-E02  intent + reference / target resolution
DANTE-E03  structured extraction / understanding
DANTE-E04  native query + history + absence semantics
DANTE-E05  context + privacy + Reality Scope
DANTE-E06  planning / replanning / scenario reasoning
DANTE-E07  document / long-context / multimodal reasoning
DANTE-E08  tool / capability use
DANTE-E09  consequential effect boundary
DANTE-E10  multi-actor / delegation / disclosure
DANTE-E11  adaptive memory / learning
DANTE-E12  currentness / failure / supersession / failover
DANTE-E13  open-world research / grounding
```

Trigger-gated families remain outside baseline qualification until real product scope activates them:

```text
voice/realtime
browser/computer-use
code execution
long-running durable background work
embedding/vector retrieval
specialized generation
```

### 8.2 Hard gates before scores

DANTE does not use one weighted quality score that can hide a semantic/privacy failure.

Examples of hard-fail conditions:

```text
wrong consequential target
unauthorized effect
cross-actor/private disclosure
fabricated canonical fact
false effect-success claim
false Actual/completed state
stale/superseded result published as current
Reality Scope laundering
invalid durable-memory promotion
blind failover to an ineligible provider
source/derivative resurrection
```

Only eligible configurations proceed to graded quality/latency/economics comparison.

### 8.3 Grading order

Use strongest evidence first:

```text
deterministic state/result
→ schema/type/constraint
→ tool/effect receipt
→ source/citation
→ invariant/privacy/security
→ human-calibrated rubric/model judge for softer dimensions
```

Model judges do not override canonical state or deterministic validation.

### 8.4 Provider/model replaceability

Binding separation:

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY
DANTE FEATURE/BUSINESS CODE != CONCRETE PROVIDER SDK
PROVIDER REPLACEABLE != PROVIDERS IDENTICAL
PROVIDER REPLACEABLE != LOWEST-COMMON-DENOMINATOR PROVIDER USAGE
```

Production chain:

```text
DANTE work/capability need
→ ModelTarget
→ HarnessProfile
→ ProviderBinding
→ ProviderAdapter
→ concrete serving platform / model / deployment
```

`ProviderBinding` must be capable of representing model vendor separately from serving platform, including direct-provider versus cloud-hosted bindings.

### 8.5 Core portability and native augmentation

Two tracks remain distinct:

```text
CORE PORTABILITY
same DANTE semantic obligation
+ provider-specific HarnessProfile
→ portable cognition comparison

PROVIDER-NATIVE AUGMENTATION
native search/files/cache/state/background/browser/computer/etc.
→ independent value + eligibility assessment
```

Native provider features do not define DANTE semantics.

### 8.6 Feature eligibility

Binding candidate rule:

```text
FEATURE AVAILABLE != FEATURE ELIGIBLE
```

Provider state/cache/files/background/tools must be checked against current WorkContract purpose, data class, sensitivity, retention, region, third-party exposure and governance constraints before use.

### 8.7 Failover

Rejected:

```text
primary fails
→ replay identical request/context to another provider
```

Required:

```text
primary failure
→ alternate binding qualification
→ current provider/data eligibility
→ rebuild/minimize ConsumerContext if needed
→ alternate HarnessProfile
→ invoke
```

### 8.8 Economics

Primary metric:

```text
EFFECTIVE COST PER SUCCESSFUL DANTE TASK
```

rather than list price per token.

Cost includes applicable input/output/thinking/cache/native-tool/retry/failure/fallback costs and is measured across workload/context buckets.

### 8.9 AI-04A candidate invariants

The durable AI-04 candidate currently records `A01..A22`, including:

```text
workload evidence precedes vendor selection
hard gates precede economics
same semantic contract != same byte prompt
model+Harness quality != serving-platform qualification
provider-native augmentation != portability proof
FEATURE AVAILABLE != FEATURE ELIGIBLE
failover != blind replay
preview quality win != production qualification
long-context capacity != context correctness
model avoidance is a valid preferred route
```

These are candidate productionization rules pending direct eval evidence and later whole AI-04 destructive review.

### 8.10 Current official-source candidate landscape

Current official documentation has been used only to establish challenger/binding candidates and provider-feature constraints.

Current families under consideration include:

```text
OpenAI direct / Azure OpenAI
→ GPT-5.6 Sol / Terra / Luna candidate tiers

Anthropic direct / qualified alternate hosting
→ Claude Opus 5 / Sonnet 5 and cost-tier candidates

Google Gemini
→ Gemini 3.7 Flash stable/GA
→ Gemini 3.5 Flash-Lite cost candidate
→ preview models challenger-only until production-qualified
```

No provider/model/deployment is selected by this list.

### 8.11 Concrete runtime / capability work still to follow

After the direct eval specification/evidence boundary, AI-04 still owns:

```text
model invocation / streaming / cancellation
structured outputs
tool/capability execution
provider retries / errors / rate limits
routing and failover
background work
Class-A vs Class-B execution trigger
MCP/A2A/API edge boundaries
browser/computer-use/code execution
Execution Environment technology/credentials/network/filesystem/resource limits
provider-native files/cache/thread usage
artifact flows
```

### 8.12 Security / privacy / control plane / operations still to follow

AI-04 must concretize:

```text
provider/data eligibility
credential/workload identity boundary
secret brokerage
privacy/retention/provider data handling
observability vs audit vs eval data
cost/rate/resource budgets
model/provider configuration/versioning
feature flags / routing policy
failure/degraded modes
incident/reconciliation posture
release/canary/rollback behavior
runtime/control-plane ownership
```

Provider/model choice is not accepted until these production dimensions are considered along with direct DANTE workload quality.

---

## 9. AI-05 — final architecture-to-build boundary

AI-05 remains future until AI-04 closes.

It must run whole-system acceptance over the concrete productionized design and produce the exact implementation blueprint, including as applicable:

```text
module / port / adapter boundaries
physical schemas
migration sequence
backend/frontend contracts
provider adapters
workers
feature flags
eval gates
rollout strategy
first implementation vertical
```

After AI-05 closure, actual AI implementation proceeds through explicit implementation workstream(s)/gates. Architecture documentation must not expand indefinitely instead of building.

---

## 10. Decisions explicitly still open

Do not claim these are decided before evidence:

```text
OpenAI / Azure OpenAI / Anthropic / Gemini / other concrete provider set
specific model/deployment mapping
routing/fallback policy
exact ModelTarget vocabulary
exact eval fixture corpus / thresholds
embedding model/dimensions
pgvector/ANN activation
FTS index additions
conversation persistence physical form
Run/working persistence physical form
summary/adaptive-memory persistence where any survives
provider memory/thread/cache implementation
local model activation
runtime SDK
concrete sandbox / Execution Environment technology
Restate activation for AI work
MCP/A2A exact implementation
production AI server/GPU topology
AI commercial/pricing model
```

---

## 11. Cross-cutting quality bar

Every architecture decision must be reviewed against:

```text
semantic correctness
source/canonicality integrity
historical truth
Reality Scope correctness
reference-resolution correctness
coverage / absence semantics
multi-actor correctness
privacy / Authority / Consent / Visibility
purpose/source/use exclusions
security / prompt/retrieval injection
instruction provenance
child/delegation minimisation
revocation / deletion / anti-resurrection
concurrency / stale state
provider replaceability
failure/reconciliation
latency / token / compute / storage cost
simple-path performance
future extensibility
operational recoverability
observability/evaluation feasibility
```

Maximum quality does not mean maximum abstraction.

---

## 12. Live handoff policy

Temporary session continuity is stored only when useful in:

- `docs/workstreams/ai-architecture-live-handoff.md`

That document:

```text
is TEMPORARY
is branch-operational only
must not merge to protected main
is updated only at meaningful continuation checkpoints
must not become the only home of durable architecture decisions
```

Before branch integration, its meaningful payload must be classified and propagated to durable current/reference/evidence docs, then the live handoff must be deleted.

---

## 13. Current next action

```text
AI-04A — DIRECT DANTE EVAL SPECIFICATION
```

Do not choose a provider/model from public benchmark reputation.

Required sequence:

```text
DANTE-E01..E13 candidate workload taxonomy
→ executable-grade fixture types
→ hard pass/fail contracts
→ deterministic vs rubric grading rules
→ development / validation / held-out split
→ small exact current candidate model set per likely ModelTarget
→ frozen model snapshot / serving binding / HarnessProfile
→ direct eval/benchmark proof where decision-relevant
→ provider/model/economics/routing/fallback candidate
→ concrete runtime/capability architecture
→ security/privacy/control-plane/operations architecture
→ destructive productionization review
→ AI-04 closure
→ AI-05 whole-system acceptance + exact implementation blueprint
→ actual implementation workstream(s)
```

Provider-replaceability requirement remains binding throughout:

```text
DANTE need
→ ModelTarget
→ HarnessProfile
→ ProviderBinding
→ ProviderAdapter
→ provider/model/deployment
```

Do not preselect provider SDKs, model IDs, retrieval indexes, Restate/R2 activation or new persistence before the applicable workload/eval/production evidence exists.