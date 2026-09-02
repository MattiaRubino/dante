# DANTE AI-04 — Whole-Phase Destructive Acceptance

- **Status:** CLOSED / STRUCTURALLY ACCEPTED / WP-01..WP-22
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-04 — Productionization Architecture
- **Closure PRE-SCOPE:** `57d9b6b325d0873e46efbe88eee646f994027d2d`
- **Upstream:** AI-02.1 CLOSED / AI-03 CLOSED
- **AI-04A:** CLOSED / STRUCTURALLY ACCEPTED / A01..A30 / EV01..EV20 / DIRECT PROVIDER EVIDENCE NOT EXECUTED
- **AI-04B:** CLOSED / STRUCTURALLY ACCEPTED / RT-01..RT-31
- **AI-04C:** CLOSED / STRUCTURALLY ACCEPTED / PA-01..PA-61
- **Provider/model selection:** OPEN / EVIDENCE-DRIVEN
- **Implementation claim:** NONE
- **Database change:** NONE

This document is the final structural acceptance authority for AI-04.

It does not claim that a provider, model, SDK, eval runner, runtime implementation, commercial plan, cloud control plane, guardrail product, sandbox or database materialization has been selected or implemented.

AI-04 closes the **responsibility architecture** required to make later production choices without allowing provider/runtime/economic convenience to redefine DANTE semantics.

---

# 1. Acceptance objective

The whole-phase review asks a stronger question than whether AI-04A, AI-04B and AI-04C are individually coherent.

It asks whether they compose without contradiction:

```text
AI-04A
workload / eval / model / provider / economics

+

AI-04B
runtime / tools / streaming / retry / failover /
background / protocols / execution environment

+

AI-04C
security / privacy / control plane / credentials /
budgets / rollout / observability / incidents / SRE

=

one production responsibility architecture
that still obeys DANTE semantic authority
```

A local PASS in one sub-phase is insufficient if its assumptions fail at a boundary with another sub-phase.

---

# 2. Binding upstream authority

Whole-phase acceptance preserves, at minimum:

```text
PostgreSQL = sole canonical persistence/material-history authority
MODEL OUTPUT != PUBLISHABLE OUTPUT
MODEL CAPABILITY != AUTHORITY
DISPLAY NAME != EFFECT TARGET
Interaction Session != Run != Worker
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
CANCEL RUN != UNDO ALREADY-DISPATCHED EFFECTS
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
Context != Retrieval != Memory
ConsumerContext != ContextManifest != BasisManifest
APPROXIMATE != COMPLETE
Observation != Actual
Schedule != Actual
absence != false
Authority != Visibility
processing eligibility != retention eligibility != future-reuse eligibility
provider state != canonical DANTE state
DEFAULT NONCANONICAL PERSISTENCE = NO
semantic obligation != technical execution/audit evidence
```

Whole-phase acceptance did not reopen Product, Domain, Whole Logical, Physical, PostgreSQL Constitution, AI-02 or AI-03.

---

# 3. Accepted AI-04 authority stack

Durable authority remains split deliberately:

```text
docs/architecture/dante-ai-04-productionization-architecture.md

docs/architecture/dante-ai-04a-direct-eval-specification.md
  A01..A30
  EV01..EV20

docs/architecture/dante-ai-04b-concrete-runtime-capability-architecture.md
  RT-01..RT-31

docs/architecture/dante-ai-04c-production-assurance-control-plane-operations.md
  PA-01..PA-61

this document
  WP-01..WP-22
  whole-phase composition acceptance
```

The sub-phase documents own their detailed local contracts.
This document owns the cross-phase composition rules and final AI-04 structural verdict.

---

# 4. Acceptance chronology

The chronology is intentionally preserved.

```text
AI-04A
→ eval/provider/economics candidate materialized

AI-04B
→ first candidate
→ destructive FAIL
→ RT-01..RT-20
→ PASS candidate
→ independent FAIL
→ RT-21..RT-31
→ final PASS
→ CLOSED

AI-04C
→ state-of-the-art research + candidate
→ destructive FAIL
→ PA-01..PA-38
→ PASS candidate
→ independent FAIL
→ PA-39..PA-61
→ final PASS
→ CLOSED

AI-04 WHOLE-PHASE PASS #1
→ reconstruct A/B/C as independent authorities
→ FAIL
→ WP-01..WP-11
→ reverse-order retest PASS candidate

AI-04 WHOLE-PHASE PASS #2 / THIRD ADVERSARIAL ROUND
→ attack composition through new failure classes
→ FAIL
→ WP-12..WP-22
→ adversarial retest PASS
→ reverse composition C → B → A PASS
→ upstream semantic check PASS

FINAL STRUCTURAL VERDICT
→ AI-04 CLOSED / STRUCTURALLY ACCEPTED
```

No historical FAIL is rewritten as an earlier PASS.

---

# 5. Whole-phase candidate route

The accepted conceptual production path is:

```text
WorkContract
+ ConsequenceProfile
+ current Actor / represented-party context
+ current Authority / AuthZ / Consent / Visibility
+ current EntitlementProfile / ResourceBudget
+ current provider/data/feature eligibility
        ↓
ModelTarget or deterministic/no-model route
        ↓
qualified candidate route compositions
        ↓
Routing Policy
        ↓
selected compatible:
  HarnessProfile
  + ProviderBinding
  + feature mode
  + capability projection
  + applicable security/control profile
        ↓
route-specific resource admission
        ↓
current egress/data eligibility at send boundary
        ↓
ProviderAdapter / Capability Runtime / deterministic runtime
        ↓
Verifier / effect governance / reconciliation
        ↓
Result Maturity / Disclosure / Safe Publication
        ↓
usage settlement / evidence / telemetry
```

This is a responsibility chain, not a mandatory service topology.

---

# 6. Provider replaceability after whole-phase acceptance

Provider replaceability means more than having one adapter interface.

The following remain separated and independently governable:

```text
ModelTarget
HarnessProfile
ProviderBinding
serving platform
protocol family
model snapshot / deployment
feature mode
provider continuation/cache state
security/guard profile
capability projection
routing policy
commercial entitlement
resource admission
rollout state
operational health
production capacity evidence
```

Binding:

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY
HARNESSPROFILE != PROVIDERBINDING
DANTE FEATURE/BUSINESS CODE != CONCRETE PROVIDER SDK
PROVIDER REPLACEABLE != PROVIDERS IDENTICAL
PROVIDER REPLACEABLE != LOWEST-COMMON-DENOMINATOR PROVIDER USAGE
```

A V1 may intentionally use one primary provider.
That does not remove the replaceability boundary.

---

# 7. Whole-phase hardening WP-01..WP-22

## WP-01 — eval qualification is not current routability

```text
EVAL PASS / QUALIFIED MODEL
!= CURRENT ROUTABLE PRODUCTION ROUTE.
```

A route must still satisfy all current production qualification, eligibility, availability, entitlement and rollout gates.

---

## WP-02 — effective production-route quality

```text
RAW MODEL/HARNESS QUALITY
!= EFFECTIVE PRODUCTION-ROUTE QUALITY.
```

Mandatory provider behavior, guardrails, DLP/redaction, capability projection, feature mode and publication controls may materially change the effective result.

The final production route must still satisfy the workload quality floor after mandatory production transformations.

---

## WP-03 — HarnessProfile and ProviderBinding compose without collapsing

```text
HARNESSPROFILE != PROVIDERBINDING
```

but routing selects a **qualified compatible HarnessProfile + ProviderBinding composition**.

Rejected assumption:

```text
choose one universal Harness first
→ attach arbitrary provider later
```

Provider/model-specific Harness tuning is allowed while DANTE semantics remain provider-neutral.

---

## WP-04 — fallback has independent qualification

```text
FALLBACK DOES NOT INHERIT PRIMARY QUALIFICATION.
```

Every alternate route independently satisfies applicable:

```text
hard semantic/privacy/safety gates
quality floor
provider/data eligibility
feature-mode compatibility
Harness compatibility
operational qualification
resource policy
```

---

## WP-05 — coherent in-flight invocation configuration

One logical ModelInvocation uses one coherent material configuration snapshot.

```text
IN-FLIGHT INVOCATION CONFIGURATION
MUST NOT BE MUTATED HALF-WAY BY ROLLOUT.
```

However:

```text
FROZEN EXECUTION CONFIGURATION
!= CURRENT AUTHORIZATION
!= CURRENT REVOCATION / EMERGENCY DENY.
```

Reproducibility never creates perpetual authorization.

---

## WP-06 — continuation compatibility

```text
PROVIDER CONTINUATION REUSE
REQUIRES CURRENT CONFIGURATION COMPATIBILITY.
```

If HarnessProfile, feature mode, capability projection or security configuration changes materially, provider continuation may become ineligible.

Then DANTE rebuilds from governed DANTE context/state rather than pretending opaque provider continuation is still equivalent.

---

## WP-07 — new attempts require new/current resource admission

Every new resource-consuming attempt requires current resource policy evaluation.

This includes:

```text
retry
failover
new ProviderAttempt
expensive provider-native tool
new background attempt
```

```text
PRIMARY ATTEMPT RESERVATION
!= UNLIMITED RETRY/FAILOVER PERMISSION.
```

---

## WP-08 — emergency disable preserves reconciliation

Provider/route ineligibility after dispatch blocks new uncontrolled user-data egress and new ordinary work.

It does **not** erase bounded incident/reconciliation responsibilities needed for already-dispatched or outcome-unknown work.

```text
EMERGENCY DISABLE
!= ABANDON RECONCILIATION.
```

---

## WP-09 — qualification can stale independently by dimension

Qualification state is multi-dimensional.

At least these dimensions can stale independently:

```text
model/cognition quality
Harness compatibility
serving-binding reliability
privacy/security eligibility
retention/residency/processors
feature-mode compatibility
guard/control compatibility
economics/price
production capacity
```

```text
CURRENT ROUTABILITY
REQUIRES EVERY APPLICABLE DIMENSION TO REMAIN VALID.
```

---

## WP-10 — entitled is not servable

```text
ENTITLED != CURRENTLY SERVABLE.
```

A commercial offering may grant access to a capability while no currently safe/qualified route is available.

DANTE then degrades, defers, limits scope or refuses safely.
It does not route to an under-qualified model merely because the customer paid for the entitlement.

---

## WP-11 — provider outage is not whole-product outage

```text
MODEL/PROVIDER CONTROL-PLANE FAILURE
MUST NOT UNNECESSARILY DISABLE
DANTE-NATIVE / DETERMINISTIC CAPABILITIES.
```

If a valid DANTE capability does not require the failed external AI surface, it remains independently operable subject to its own dependencies.

---

## WP-12 — evaluated composition vs production composition

```text
EVAL CANDIDATE PASS
!= PRODUCTION ROUTE QUALIFIED
```

unless the material production composition is equivalent to the evaluated composition or the production delta has its own qualification evidence.

Material deltas can include:

```text
serving platform
model snapshot/deployment
HarnessProfile
tool/capability projection
feature mode
prompt/provider cache behavior
GuardProfile / DLP / output transform
routing/retry/fallback policy
context/egress policy
```

---

## WP-13 — auxiliary model inference is first-class

Every auxiliary or secondary model inference is a real governed inference and data recipient.

Examples:

```text
router model
verifier model
judge model
reranker/summarizer model
advisor/sub-inference
provider-native hidden/utility model where materially involved
```

Applicable qualification, data eligibility, budget, evidence and security policy still apply.

```text
"ONLY A VERIFIER/ROUTER"
!= FREE DATA RECIPIENT.
```

---

## WP-14 — route selection is not egress authorization

```text
ROUTE SELECTION
!= EGRESS AUTHORIZATION.

CONTEXT ASSEMBLY
!= EGRESS AUTHORIZATION.
```

Every material externalization must satisfy current data/egress eligibility at the material send boundary.

This includes externalization to:

```text
model provider
secondary model/judge
security/guard service
web/search provider
MCP/A2A recipient
external capability/tool
provider-hosted execution
```

---

## WP-15 — fallback capability contraction

A fallback with a smaller context window, weaker tool set, different modality support or other capability contraction may not silently truncate or compact previously qualified context.

Required behavior:

```text
alternate route capability differs
→ rebuild/reassess ConsumerContext
→ reassess coverage / ContextReadiness
→ satisfy workload quality floor
→ execute

OR

safe degrade / defer / clarify / fail
```

```text
SILENT CONTEXT TRUNCATION
!= VALID FAILOVER.
```

---

## WP-16 — capability contract version survives model reasoning latency

The capability/tool contract exposed to a model remains identifiable through execution.

```text
MODEL REQUEST AGAINST CAPABILITY VERSION N
!= AUTOMATICALLY VALID REQUEST AGAINST VERSION N+1.
```

A material version change requires compatibility proof, revalidation/adaptation under explicit rules, or replanning/reinvocation.

No best-effort coercion may manufacture equivalence.

---

## WP-17 — cache reuse is not semantic continuity

Provider/prompt cache reuse must be compatible with the current material configuration generation and current data eligibility.

```text
CACHE HIT
!= HARNESS CONTINUITY
!= TOOL CONTINUITY
!= SECURITY CONTINUITY
!= AUTHORIZATION
!= FRESHNESS.
```

Material changes to system/developer instructions, HarnessProfile, schema, capability projection, security policy, data eligibility or revocation can make prior cache state ineligible for semantic reuse even if the provider can technically hit the cache.

---

## WP-18 — operational side channels preserve non-interference

Routing, fallback, latency, error wording, cost behavior, provider availability and security behavior must not become an unauthorized hidden-information oracle.

```text
PROTECTED / WITHHELD / INELIGIBLE INFORMATION
!= SAFE TO REVEAL INDIRECTLY.
```

Raw provider/security errors do not flow directly to recipients when they can reveal protected context or internal policy detail.

This architecture rule does not claim execution of the existing direct hidden-result non-interference proof obligations.

---

## WP-19 — model picker is preference, not Authority

User/admin model preference may constrain or rank the currently eligible route set.

It may not force an ineligible route.

```text
MODEL PICKER / USER PREFERENCE
!= ROUTING AUTHORITY.
```

Any selected model remains subject to current:

```text
qualification
eligibility
availability
entitlement
rollout activation
resource admission
```

---

## WP-20 — route selection and budget admission are coherent

Resource admission is route-specific enough to bound the selected execution exposure.

Conceptually:

```text
eligible candidate routes
→ route-specific bounded cost/resource estimate
→ affordability/entitlement check
→ select route
→ atomic/bounded reservation where required
→ material external execution
```

```text
GENERIC "AI BUDGET RESERVED"
!= PERMISSION FOR ANY ROUTE.
```

Fallback/retry follows WP-07 and requires current admission for the new attempt.

---

## WP-21 — invocation snapshot is not whole-Run immutability

```text
COHERENT INVOCATION CONFIG SNAPSHOT
!= WHOLE-RUN CONFIGURATION IMMUTABILITY.
```

A long Run may cross approved configuration revisions between logical invocations.

Every transition must preserve:

```text
reproducibility/evidence lineage
continuation compatibility
current authorization/data eligibility
context validity
capability/tool compatibility
resource admission
```

If not compatible, DANTE rebuilds/replans rather than silently mixing configurations.

---

## WP-22 — direct eval is not production capacity qualification

```text
SINGLE-TRIAL / DIRECT EVAL SUCCESS
!= PRODUCTION CAPACITY QUALIFICATION.
```

Before a concrete production route is activated for an intended service envelope, evidence must be proportionate to expected:

```text
concurrency
provider quotas
request/token throughput
queue/backpressure behavior
regional/feature capacity
rate limiting
circuit-breaker/fallback behavior
degraded-mode behavior
```

Architecture can close without those concrete provider load tests.
Production route activation cannot pretend they happened.

---

# 8. Final route activation gate

AI-04 closes with concrete provider/model selection still OPEN.

A production ProviderBinding/route cannot be activated merely because:

```text
provider is popular
model leads a public benchmark
list price is cheap
SDK is convenient
provider documentation says enterprise-ready
one direct call worked
```

Before concrete production activation, applicable evidence must establish at least:

```text
DANTE workload/model/Harness quality
hard semantic/privacy/safety gates
serving-binding reliability
feature-mode compatibility
provider/data/retention/residency eligibility
route-composition compatibility
mandatory guard/control compatibility
effective production-route quality
resource/economic viability
intended capacity/service-envelope viability
```

```text
ARCHITECTURE ACCEPTANCE
!= CONCRETE PROVIDER ACTIVATION.
```

---

# 9. AI-04A closure interpretation

AI-04A is structurally accepted.

This means the workload/eval/provider/economics methodology is accepted as the gate for later concrete selection.

It does **not** mean:

```text
OpenAI tested          NO
Azure tested           NO
Anthropic tested       NO
Gemini tested          NO
provider selected      NO
model default selected NO
eval runner selected   NO
paid API called        NO
```

The direct-eval implementation and provider trials are intentionally deferred until a concrete selection or activation decision requires them.

```text
AI-04A CLOSED STRUCTURALLY
+
DIRECT PROVIDER EVIDENCE NOT EXECUTED
```

is the accepted truthful state.

---

# 10. Commercial/service-tier consequence

Accepted commercial separation remains:

```text
COMMERCIAL SUBSCRIPTION / SERVICE TIER
!= DANTE DOMAIN Plan
```

and:

```text
CommercialOffering / ServiceTier
→ EntitlementProfile
→ resource/capability envelope
→ Budget / Routing Policy
→ eligible route set
```

Commercial tier does not hardcode one provider/model/deployment.

Commercial entitlements may bound resources/capabilities but may not weaken truth, privacy, Authority, target safety, provider/data eligibility, effect verification/reconciliation, anti-resurrection or currentness.

```text
ENTITLED != SERVABLE
COMMERCIAL CREDIT != PROVIDER TOKEN != ACTUAL PROVIDER COST
```

Exact names/prices/quotas remain product/business work, not AI-04 closure truth.

---

# 11. Runtime consequence

AI-04B remains accepted unchanged except where WP rules clarify cross-phase composition.

In particular:

```text
RUN != MODEL INVOCATION != PROVIDER ATTEMPT
RAW PROVIDER EVENT != DANTE RUNTIME EVENT != PUBLICATION EVENT
CANCELLATION REQUESTED != CONFIRMED != QUIESCED
PROVIDER CONTINUATION != DANTE CONTEXT/MEMORY
PROVIDER TOOL != DANTE CAPABILITY
PROVIDER CALL ID != DANTE SEMANTIC IDEMPOTENCY
PROVIDER BACKGROUND != DANTE DURABLE RUN
PROVIDER-HOSTED EXECUTION != DANTE Execution Environment
```

Provider adapters remain mechanics, not semantic authorities.

---

# 12. Production-assurance consequence

AI-04C remains accepted unchanged except where WP rules clarify cross-phase composition.

At production time:

```text
QUALIFIED != ELIGIBLE != AVAILABLE != ENTITLED
```

and routability is the intersection of all applicable current gates.

Control-plane policy is versioned and auditable.
Runtime enforcement occurs at material boundaries.
Mandatory security controls do not silently fail open.
Telemetry, audit, eval evidence and canonical truth remain separate evidence planes.
Commercial exhaustion does not erase reconciliation obligations.
Rollback of configuration is not rollback of already-materialized effects.

---

# 13. Deterministic-first operation

AI-04 whole-phase acceptance strengthens model avoidance as a production property.

```text
MODEL OUTAGE
!= DANTE OUTAGE
```

where the requested work is legitimately satisfiable by:

```text
PostgreSQL native query
validated application logic
deterministic computation
solver
already-accepted non-model capability
```

This protects:

```text
correctness
latency
privacy
cost
availability
provider independence
```

No-model execution remains an actual route, not merely a benchmark baseline.

---

# 14. Evidence and non-interference

AI-04 architecture requires operational evidence sufficient to debug/qualify production behavior without turning telemetry into a second truth store or privacy sink.

Accepted separation:

```text
CANONICAL DOMAIN/MATERIAL STATE
!= REQUIRED AUDIT/EFFECT EVIDENCE
!= OPERATIONAL TELEMETRY
!= EVAL EVIDENCE
```

The architecture also requires preservation of hidden-result/non-interference semantics across operational behavior.

Direct SC/PSV proof execution remains distinct and unclaimed.

---

# 15. Decisions intentionally open after AI-04

```text
concrete primary/fallback provider(s)
concrete model snapshots/defaults
provider SDKs
exact ModelTarget vocabulary
actual direct provider benchmark results
final eval runner
exact runtime modules/classes/APIs
physical control-plane storage/topology
AI gateway product
feature flag/rollout implementation
security/guardrail product
secret manager/KMS implementation
exact IAM/workload identity implementation
exact commercial offering names/prices/quotas
billing/credit vendor and ledger implementation
exact budget reservation/settlement implementation
exact rate-limit/retry/circuit-breaker values
exact SLO/error-budget targets
client streaming transport
voice/realtime transport
provider background/native tool activation
MCP/A2A activation
Execution Environment technology
Restate activation for first qualifying Class-B consumer
R2 activation
pgvector/ANN/FTS activation
embedding model/dimensions
production regions/residency mappings
```

These are implementation/selection questions governed by the accepted architecture and future evidence.

---

# 16. Explicit non-claims

```text
AI-04 CLOSED                              YES / STRUCTURAL
AI-04A CLOSED                             YES / STRUCTURAL
AI-04A DIRECT PROVIDER EVIDENCE PASS       NO
AI-04B CLOSED                             YES / STRUCTURAL
AI-04C CLOSED                             YES / STRUCTURAL
WHOLE-PHASE STRUCTURAL ACCEPTANCE          YES
PROVIDER SELECTED                         NO
MODEL DEFAULT SELECTED                    NO
PROVIDER SDK SELECTED                     NO
EVAL RUNNER SELECTED                      NO
API CREDENTIALS USED                      NO
PAID PROVIDER CALL EXECUTED               NO
PRODUCTION ROUTE CAPACITY PASS             NO
PRODUCTION AI BACKEND IMPLEMENTED         NO
FRONTEND AI IMPLEMENTED                   NO
CONTROL PLANE IMPLEMENTED                 NO
COMMERCIAL TIER NAMES/PRICES SET          NO
BILLING IMPLEMENTED                       NO
POSTGRESQL/ALEMBIC CHANGED                NO
NEW AI TABLE/INDEX                        NO
PGVECTOR/ANN/FTS ACTIVATED                NO
RESTATE/R2 ACTIVATED                      NO
MCP/A2A ACTIVATED                         NO
EXECUTION ENVIRONMENT IMPLEMENTED         NO
SC/PSV DIRECT PROOFS EXECUTED             NO
AI-05 IMPLEMENTED                         NO
```

---

# 17. Final structural verdict

After three whole-phase adversarial/composition rounds, including reverse composition and upstream semantic checks:

```text
AI-04A local authority        PASS / STRUCTURAL
AI-04B local authority        PASS / CLOSED
AI-04C local authority        PASS / CLOSED
A ↔ B composition             PASS after WP hardening
A ↔ C composition             PASS after WP hardening
B ↔ C composition             PASS after WP hardening
C → B → A reverse composition PASS
upstream semantic authority   NO REOPEN REQUIRED
```

Final verdict:

```text
AI-04 — PRODUCTIONIZATION ARCHITECTURE
CLOSED / STRUCTURALLY ACCEPTED

A01..A30
EV01..EV20
RT-01..RT-31
PA-01..PA-61
WP-01..WP-22
```

---

# 18. Next phase boundary

AI-04 closure is not permission to begin coding arbitrary provider integrations.

Next sequence:

```text
GLOBAL CURRENT-TRUTH RECONCILIATION
→ mark AI-04 CLOSED across current project navigation/status docs
→ route AI work to AI-05

then

AI-05 — WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT
→ reconcile Product / Domain / Logical / Physical / DB / Access / Home /
  AI-02 / AI-03 / AI-04 into buildable implementation boundaries
→ define concrete module/port/adapter/config/evidence/vertical plan
→ identify which remaining concrete decisions require direct proofs

then

actual AI implementation workstream(s)
```

Concrete provider/model activation remains gated by applicable direct DANTE evidence.
