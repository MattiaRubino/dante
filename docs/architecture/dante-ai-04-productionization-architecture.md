# DANTE AI-04 — Productionization Architecture

- **Status:** CANDIDATE / AI-04A DIRECT EVAL SPEC MATERIALIZED / TOOLING SPIKE NEXT / NOT CLOSED
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-04 — Productionization Architecture
- **Current focus:** direct DANTE eval evidence, provider/model/economics, commercial entitlement/resource boundary
- **Upstream:** AI-02.1 CLOSED / AI-03 CLOSED
- **AI-03A:** C01..C33
- **AI-03B:** B01..B35
- **AI-03C:** MAT-01..MAT-15
- **Initial AI-04A PRE-SCOPE:** `aff3d7153aa0c4cf99d4bc28f569bc3db2e82703`
- **Direct-eval spec PRE-SCOPE:** `f5ee7e1fc86c1f2e5675ee860bbbadfbc6bde68a`
- **Implementation claim:** NONE
- **Provider/model selection:** OPEN / EVIDENCE-DRIVEN
- **Commercial tier/pricing selection:** OPEN
- **Database change:** NONE

This document is the durable candidate architecture for AI-04 Productionization.

Detailed executable-grade evaluation semantics now live in:

- `docs/architecture/dante-ai-04a-direct-eval-specification.md`

AI-04 consumes the accepted DANTE intelligence semantics/materialization boundaries and converts them into production choices. It does **not** reopen AI-02 or AI-03 because a provider SDK, model API, cloud product, eval framework or commercial packaging strategy prefers another shape.

Current sequence:

```text
DANTE obligations
→ representative workloads
→ executable DANTE eval specification
→ hard eligibility gates
→ direct evidence
→ provider/model/platform/economics candidate
→ commercial entitlement/resource envelope integration
→ routing/binding candidate
→ concrete runtime/security/operations design
→ destructive productionization review
→ AI-04 closure
```

Provider/model selection does not precede direct DANTE evidence.

---

# 1. Binding upstream authority

AI-04 inherits without weakening:

```text
PostgreSQL = sole canonical persistence/material-history authority
MODEL OUTPUT != PUBLISHABLE OUTPUT
MODEL CAPABILITY != AUTHORITY
DISPLAY NAME != EFFECT TARGET
Interaction Session != Run != Worker
Context != Retrieval != Memory
ConsumerContext != ContextManifest != BasisManifest
APPROXIMATE != COMPLETE
Memory exists != memory may be recalled
processing eligibility != retention eligibility != future-reuse eligibility
provider state != canonical DANTE state
semantic obligation != technical execution/audit evidence
```

AI-03 materialization default remains:

```text
DEFAULT NONCANONICAL PERSISTENCE = NO
```

No provider/eval/commercial feature may silently turn provider conversation state, cache, file store, search result, tool trace, model output, background job or eval log into canonical DANTE state.

---

# 2. AI-04 problem statement

AI-02 and AI-03 define what DANTE intelligence means and which correctness boundaries must survive.

AI-04 must now answer production questions such as:

```text
Which workloads actually require a model?
Which quality floors are mandatory?
Which model families are good enough for which ModelTarget?
Which serving platforms are eligible for which data classes/purposes?
How are provider-specific strengths used without provider lock-in?
How are structured outputs/tools/streaming/cancellation normalized?
How is provider failover performed without privacy or semantic regression?
How is cost measured on successful DANTE work rather than token-list price?
Which provider-native stateful features are allowed for which workloads?
How do commercial/service tiers limit resources without changing truth/safety?
What changes require requalification?
```

AI-04 is not a vendor beauty contest and not a pricing-page exercise.

```text
GENERAL LLM BENCHMARK WIN
!= DANTE PRODUCTION ELIGIBILITY

CHEAPER LIST PRICE
!= DANTE COMMERCIAL VIABILITY
```

---

# 3. Provider replaceability — accepted production boundary

Binding:

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
DANTE FEATURE/BUSINESS CODE != CONCRETE PROVIDER SDK
PROVIDER REPLACEABLE != PROVIDERS IDENTICAL
PROVIDER REPLACEABLE != LOWEST-COMMON-DENOMINATOR PROVIDER USAGE
```

AI-04 further distinguishes:

```text
MODEL VENDOR
!= SERVING PLATFORM
!= PROTOCOL FAMILY
!= MODEL FAMILY / SNAPSHOT
!= DEPLOYMENT / ENDPOINT
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

This is a narrow production boundary, not a generic abstraction framework.

## 3.1 ModelTarget

`ModelTarget` states what DANTE needs, not who sells it.

Candidate target dimensions may include:

```text
quality tier
reasoning depth
latency class
context demand
structured-output requirement
vision/multimodal requirement
tool-use requirement
open-world grounding requirement
code/browser/computer-use requirement
privacy/data eligibility floor
cost/resource ceiling
```

Final vocabulary must be earned from workload evidence and must not become a vendor-model alias enum.

## 3.2 HarnessProfile

`HarnessProfile` owns provider/model-specific controllable behavior needed to obtain legitimate performance without leaking vendor mechanics into DANTE semantics.

Examples:

```text
reasoning/thinking effort
instruction structure
structured-output configuration
tool descriptions/tool-choice posture
message/context packaging
provider-required continuity metadata
stream handling
provider-native safe optimizations
```

```text
SAME DANTE SEMANTIC CONTRACT
!= SAME BYTE PROMPT
```

## 3.3 ProviderBinding

`ProviderBinding` resolves a `ModelTarget` to a concrete qualified endpoint.

Candidate dimensions:

```text
binding identity/version
model vendor
serving platform
protocol family
model family
exact snapshot/version where available
governed alias if unavoidable
endpoint/deployment
region/data-zone
service tier
credential/auth profile ref
retention/data-handling profile
capability profile
HarnessProfile ref
qualification/eval version
activation state
```

It is runtime/control-plane configuration, not Domain identity.

## 3.4 ProviderAdapter

Owns only SDK/protocol mechanics:

```text
request construction
stream-event normalization
structured-output transport
tool/function transport
usage accounting
provider error normalization
rate-limit/retry signals
provider response/receipt identity
cancellation/native capability mechanics
```

It does not own DANTE policy, Authority, WorkContract meaning or canonical semantics.

---

# 4. Day-one posture

```text
ARCHITECTURE
provider-replaceable

V1 IMPLEMENTATION
may intentionally use one primary provider
```

A second provider is justified by evidence such as quality, capability, cost, latency, eligible residency/compliance, resilience or concentration risk.

Do not implement four adapters merely to claim multi-provider support.

Acceptance question:

> Can a qualified `ModelTarget` move to another eligible binding without rewriting DANTE feature, Domain, WorkContract, Context, Retrieval, Memory, Verifier or Effect semantics?

---

# 5. Eval philosophy

DANTE evals start from product/system obligations rather than public leaderboards.

Two levels:

```text
LEVEL 1 — HARD ELIGIBILITY / CORRECTNESS
failure disqualifies the applicable case/configuration

LEVEL 2 — GRADED QUALITY / PERFORMANCE / ECONOMICS
used only after Level 1 passes
```

A high prose-quality score cannot compensate for privacy leakage, wrong target or unauthorized effect.

Detailed semantics: `dante-ai-04a-direct-eval-specification.md`.

---

# 6. Hard gates

Representative hard failures:

```text
wrong consequential target
unauthorized effect path
cross-actor/private-data disclosure
fabricated canonical fact
false effect-success claim
false Actual/completed state
stale/superseded output published as current
Reality Scope laundering
material contradiction silently guessed where clarification/reconciliation is required
invalid command/tool arguments rejected deterministically
provider failover violating current provider/data eligibility
invalid durable-memory promotion
retention/future reuse outside eligibility
source/derivative resurrection after deletion/retirement
COMPLETE_REQUIRED answered through unproven approximate retrieval
untrusted data gaining instruction authority
```

```text
HARD FAILURE
→ NO WEIGHTED-SCORE COMPENSATION
```

---

# 7. Graded metrics

Among eligible configurations compare:

```text
task success
semantic correctness
constraint satisfaction
groundedness/source use
coverage/correct absence handling
clarification quality/efficiency
reference-resolution quality
structured-output success
tool selection/argument/trajectory quality
long-context evidence use
contradiction handling
correct abstention/non-action
instruction following
retry/failure rate
TTFT / first useful output
end-to-end latency
usage/resource consumption
provider-native charges
cache effects
cost per successful task
```

Keep component metrics inspectable even if an operational ranking score is later derived.

---

# 8. DANTE representative workload matrix

```text
DANTE-E01  Model avoidance / deterministic fast path
DANTE-E02  Intent + Reference / Target Resolution
DANTE-E03  Structured extraction / understanding
DANTE-E04  Native query + history + absence semantics
DANTE-E05  Context + privacy + Reality Scope
DANTE-E06  Planning / replanning / scenario reasoning
DANTE-E07  Document / long-context / multimodal reasoning
DANTE-E08  Tool / Capability use
DANTE-E09  Consequential effect preparation/execution
DANTE-E10  Multi-actor / delegation / disclosure
DANTE-E11  Adaptive memory / learning
DANTE-E12  Currentness / failure / supersession / failover
DANTE-E13  Open-world research / grounding
```

Trigger-gated only when real product scope activates them:

```text
voice/realtime
browser/computer-use
code execution
long-running durable background work
embedding/vector retrieval
specialized image/audio generation
```

The direct-eval spec defines fixture/oracle/grader requirements for E01..E13.

---

# 9. Dataset design

Initial corpus layers:

```text
A deterministic synthetic fixtures
B product-simulation-derived scenarios
C adversarial semantic/privacy/failure cases
D generated combinatorial/property cases where useful
E manually curated difficult cases
F later sanitized/minimized production-derived cases only under explicit governance
```

Splits:

```text
DEVELOPMENT
VALIDATION
HELD-OUT REGRESSION
```

A provider does not qualify solely on fixtures used to tune its HarnessProfile.

Core locale coverage includes at least `it-IT` and `en-US`.

Production traces are not automatic eval data.

---

# 10. Grading architecture

Order:

```text
1 deterministic state/result
2 schema/type/constraint
3 tool/effect receipt
4 source/citation/evidence
5 invariant/privacy/security
6 trajectory where semantically material
7 human-calibrated rubric
8 model judge for softer dimensions
```

```text
MODEL-JUDGE AGREES
!= CANONICAL STATE PROOF
```

Candidate must not see hidden oracle/grader truth.

---

# 11. Trial/result semantics

Evaluation-only terms:

```text
EvalCase
EvalCandidate
Trial
Trajectory
Outcome
TrialVerdict
EvalRun
EvalEvidence
```

These are not Domain/runtime persistence owners.

Outcome/environment state is primary where it can prove success.

```text
MODEL SAYS DONE
!= EFFECT SUCCEEDED
```

Trial verdicts include:

```text
PASS
HARD_FAIL
QUALITY_FAIL
INVALID_FIXTURE
INVALID_GRADER
INVALID_HARNESS
PROVIDER_INFRA_FAILURE
INCONCLUSIVE
```

A provider infrastructure failure is not automatically cognition failure but remains serving-binding reliability evidence.

---

# 12. Repeated reliability

Track ordinary success plus repeated reliability for risk-sensitive customer-facing work.

```text
pass@1 / success rate
quality distribution
hard-failure count
valid-trial count
provider-infra failure count
pass^k or equivalent all-pass reliability where applicable
```

One lucky success across many attempts is not sufficient evidence for consequential production work.

---

# 13. Capability vs regression evals

```text
CAPABILITY EVAL
find the candidate frontier

REGRESSION EVAL
protect already-earned behavior
```

Useful accepted capability cases may later graduate into normal product/system regression tests where appropriate.

Remote paid stochastic evals do not silently become ordinary backend pytest PASS.

---

# 14. Model/Harness quality vs serving-platform qualification

```text
MODEL + HARNESS QUALITY
→ can it solve DANTE work?

SERVING PLATFORM / BINDING QUALIFICATION
→ can this endpoint serve it safely/reliably/economically?
```

Concrete binding validation includes relevant protocol compatibility, model/deployment identity, capability availability, retention/data handling, region, credentials, quotas, latency, cancellation, error behavior, availability and billing.

```text
SAME MODEL FAMILY
!= AUTOMATICALLY SAME PRODUCTION BINDING
```

---

# 15. Core portability vs provider-native augmentation

```text
CORE PORTABILITY
same DANTE obligation
+ provider-specific HarnessProfile
→ compare portable cognition

PROVIDER-NATIVE AUGMENTATION
native search/files/cache/state/background/computer/etc.
→ separate incremental value + eligibility test
```

Provider-native capability quality does not prove portable DANTE quality.

---

# 16. Feature eligibility and failover

```text
FEATURE AVAILABLE != FEATURE ELIGIBLE
PROVIDER FAILOVER != BLIND REQUEST REPLAY
```

Feature/fallback eligibility considers WorkContract purpose, Actor/represented party, Subject/data class, sensitivity, provider processing, retention, regional requirements, third-party exposure, Consent/AuthZ/Visibility, source/use restrictions and deletion/recovery implications.

Fallback direction:

```text
primary failure
→ alternate binding qualification
→ fresh provider/data eligibility
→ rebuild/minimize ConsumerContext if needed
→ alternate HarnessProfile
→ invoke
```

Provider continuity is not DANTE continuity.

---

# 17. Versioning / requalification

Material changes may trigger risk-proportionate requalification:

```text
model snapshot/version
moving alias
HarnessProfile
provider API/tool semantics
retention/data policy
serving platform
region/deployment
reasoning controls
structured-output behavior
material tokenization/price behavior
```

```text
PREVIEW/EXPERIMENTAL QUALITY WIN
!= PRODUCTION QUALIFICATION
```

---

# 18. Economics

Primary technical metric:

```text
EFFECTIVE COST PER SUCCESSFUL DANTE TASK
```

Include applicable:

```text
input
output/thinking
cache
native search/tool charges
retries
failed attempts
fallback
background execution
service-tier premium
```

Measure by workload/context bucket. Cost only optimizes among configurations that already satisfy hard gates.

---

# 19. Commercial offering / entitlement boundary

DANTE may eventually ship as a public/commercial product with multiple service tiers.

The architecture must support that now without fixing pricing now.

Critical collision prevention:

```text
COMMERCIAL SUBSCRIPTION / SERVICE TIER
!= DANTE DOMAIN Plan
```

The accepted Domain `Plan` retains its existing life/planning semantics.

Use provisional commercial/control-plane language such as:

```text
CommercialOffering
ServiceTier
EntitlementProfile
BudgetPolicy
```

These are candidate responsibilities, not automatic new Domain objects/tables.

Candidate chain:

```text
CommercialOffering / ServiceTier
→ EntitlementProfile
→ capability + quota + resource envelope
→ Budget / Routing Policy
→ ModelTarget eligibility
→ ProviderBinding
```

Binding:

```text
COMMERCIAL TIER != MODEL
COMMERCIAL TIER != PROVIDER
COMMERCIAL TIER != DEPLOYMENT
COMMERCIAL TIER != HARNESSPROFILE
```

Thus a future switch from direct OpenAI to Azure-hosted OpenAI, Anthropic, Gemini or another qualified binding does not rewrite subscription tiers; likewise a commercial package change does not rewrite DANTE semantic architecture.

---

# 20. What commercial entitlements may govern

Candidate dimensions:

```text
monthly/rolling AI resource budget
model-call/token/money envelope
concurrency
background-work allowance
long-context allowance
research/tool budgets
sandbox/computer/code capability availability
priority/service class
rate limits
artifact/storage quota where product scope requires it
```

No exact names (`Base`, `Plus`, `Pro`, etc.), prices, quotas or included capabilities are accepted yet.

---

# 21. What commercial tiers may NOT weaken

Commercial packaging cannot redefine DANTE truth or minimum correctness/safety.

```text
SERVICE TIER MUST NOT WEAKEN
semantic correctness
historical correctness
privacy
Authority/AuthZ/Consent/Visibility
reference-resolution safety
provider/data eligibility
effect verification/reconciliation
anti-resurrection/currentness/supersession
```

If a task requires a qualified capability/resource above the current entitlement, DANTE may safely limit scope, defer, offer an upgrade where product policy permits, or refuse the expensive capability.

It must not route to an under-qualified model and pretend equivalent quality.

Budget exhaustion cannot erase an already-created consequential reconciliation obligation.

---

# 22. Entitlement-aware pressure tests

AI-04 must cover at least:

```text
base/entry tier + deterministic cheap workload
entry tier + expensive frontier workload
higher tier + long-context document
higher tier + background research
quota exhausted before work
quota exhausted during non-consequential work
quota exhausted after effect outcome becomes UNKNOWN
upgrade/downgrade during active Run
feature disabled by entitlement
provider/model price change
same quality becomes cheaper on alternate eligible binding
provider outage with different fallback cost
```

Exact product behavior remains later product/control-plane design; these are architecture pressure tests.

---

# 23. Current provider/model landscape — evidence only

The 2026-09-02 official-source research snapshot establishes challenger families and platform/data-control constraints. It is not a selection.

Candidate serving/model families currently include:

```text
OpenAI direct / Azure OpenAI
Anthropic direct / qualified alternate hosting
Google Gemini
```

Current comparative tiers include frontier, balanced and cost/high-volume candidates, with preview/experimental models challenger-only until separately production-qualified.

AI-04 must re-check exact model/version/price/retention facts immediately before direct qualification because this evidence is time-sensitive.

---

# 24. Initial conceptual kill-test record

The initial AI-04A candidate was hardened against:

```text
KILL-01 same-byte-prompt fairness fallacy
KILL-02 model judge owns truth
KILL-03 native-tool quality contaminates portability
KILL-04 model quality = serving-platform qualification
KILL-05 cheap hard failure wins weighted score
KILL-06 preview winner becomes production default
KILL-07 feature available therefore feature eligible
KILL-08 blind cross-provider failover
KILL-09 floating alias silently changes behavior
KILL-10 every AI request uses a model
KILL-11 long-context test = needle retrieval
KILL-12 list price proves economics
```

Direct-eval materialization adds further hardening:

```text
KILL-13 hidden oracle leaks to candidate
KILL-14 one exact trajectory overfits valid solutions
KILL-15 broken fixture/grader counted as model failure
KILL-16 provider outage contaminates cognition score
KILL-17 one lucky attempt treated as production reliability
KILL-18 eval framework becomes DANTE truth owner
KILL-19 production traces automatically become eval corpus
KILL-20 commercial tier hardcodes provider/model
KILL-21 cheap tier weakens safety/correctness
KILL-22 subscription Plan collides with Domain Plan semantics
```

No Domain/Logical/Physical/PostgreSQL reopen is required by these hardenings.

---

# 25. Candidate invariants — AI-04A

```text
A01  DANTE WORKLOAD EVIDENCE PRECEDES CONCRETE PROVIDER/MODEL SELECTION.
A02  MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT.
A03  MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY.
A04  DANTE FEATURE/DOMAIN/SEMANTIC CODE MUST NOT DEPEND DIRECTLY ON PROVIDER SDK IDENTITY.
A05  PROVIDER REPLACEABLE != PROVIDERS IDENTICAL.
A06  PROVIDER REPLACEABLE != LOWEST-COMMON-DENOMINATOR PROVIDER USAGE.
A07  SAME SEMANTIC CONTRACT != SAME BYTE PROMPT.
A08  MODEL + HARNESS QUALITY != SERVING-PLATFORM/BINDING QUALIFICATION.
A09  HARD SEMANTIC/SAFETY/PRIVACY ELIGIBILITY PRECEDES QUALITY/ECONOMICS.
A10  MODEL JUDGE CANNOT OVERRIDE DETERMINISTIC CANONICAL/SCHEMA/EFFECT FACTS.
A11  CORRECT NON-ACTION / ABSTENTION / CLARIFICATION IS PART OF QUALITY.
A12  PROVIDER-NATIVE AUGMENTATION != CORE PORTABILITY PROOF.
A13  FEATURE AVAILABLE != FEATURE ELIGIBLE.
A14  PROVIDER SERVER-SIDE STATE != DANTE INTERACTION/CANONICAL CONTINUITY.
A15  PROVIDER FAILOVER != BLIND REQUEST REPLAY.
A16  FAILOVER REQUIRES CURRENT PROVIDER/DATA ELIGIBILITY AND MAY REQUIRE NEW CONTEXT/HARNESS.
A17  SAME MODEL FAMILY != AUTOMATICALLY SAME PRODUCTION BINDING.
A18  QUALIFIED MODEL/ALIAS/HARNESS/PLATFORM CHANGES REQUIRE RISK-PROPORTIONATE REQUALIFICATION.
A19  PREVIEW/EXPERIMENTAL QUALITY WIN != PRODUCTION QUALIFICATION.
A20  LIST PRICE PER TOKEN != EFFECTIVE COST PER SUCCESSFUL DANTE TASK.
A21  LONG CONTEXT CAPACITY != CONTEXT CORRECTNESS.
A22  MODEL AVOIDANCE IS A VALID AND OFTEN PREFERRED MODEL ROUTE.
A23  DANTE EVAL SEMANTICS != EVAL RUNNER/SAAS SEMANTICS.
A24  OUTCOME/ENVIRONMENT STATE OUTRANKS MODEL SELF-REPORT WHERE OBJECTIVELY AVAILABLE.
A25  INVALID FIXTURE/GRADER/HARNESS != MODEL COGNITION FAILURE.
A26  REPEATED RELIABILITY IS FIRST-CLASS FOR CUSTOMER-FACING WORK.
A27  COMMERCIAL SUBSCRIPTION/SERVICE TIER != DANTE DOMAIN Plan.
A28  COMMERCIAL TIER != MODEL != PROVIDER != DEPLOYMENT.
A29  ENTITLEMENTS MAY LIMIT RESOURCE/CAPABILITY ENVELOPES BUT MAY NOT WEAKEN TRUTH/PRIVACY/SAFETY FLOORS.
A30  QUOTA/COST EXHAUSTION MUST NOT ERASE CONSEQUENTIAL RECONCILIATION OBLIGATIONS.
```

Detailed direct-eval invariants `EV01..EV20` live in the AI-04A direct eval specification.

---

# 26. Eval tooling posture

The repository already has ordinary backend pytest/async/coverage/PostgreSQL test infrastructure but no AI eval framework/provider SDK dependency.

Remote stochastic paid-model evals have a different lifecycle from ordinary backend CI.

Preferred future boundary candidate:

```text
tooling/ai-evals/
```

Current tooling posture:

```text
Inspect AI
→ PREFERRED DIRECT-EVAL RUNNER CANDIDATE
→ DIRECT TOOLING/PYTHON-3.14 PROOF REQUIRED
→ NOT SELECTED / NOT INSTALLED

OpenAI/Vertex eval products, LangSmith/Braintrust-style systems
→ optional secondary/platform-specific challengers

Promptfoo-class tooling
→ later red-team challenger where useful
```

DANTE owns fixtures/oracles/verdict semantics regardless of runner.

---

# 27. What remains open

```text
actual tooling-spike result
final eval runner/framework
provider SDK choices
real credentials/paid API calls
exact candidate model snapshots
actual direct benchmark results
primary V1 provider
fallback provider(s)
exact ModelTarget vocabulary
routing policy
exact hard-gate qualification repetition counts
production budget/rate limits
commercial tier names/prices/quotas
exact EntitlementProfile implementation/config storage
stream normalization implementation
structured-output implementation
background/durable execution activation
Restate/R2 activation
MCP/A2A implementation
Execution Environment technology
provider-native file/cache/state selection
production privacy/region binding choices
```

These remain AI-04 work.

---

# 28. Exact next action

```text
AI-04A — FIRST EXECUTABLE EVAL TOOLING SPIKE
```

Preferred bounded sequence:

```text
1. prove isolated eval-tooling project boundary;
2. direct preferred-runner compatibility proof under repository/Python constraints;
3. synthetic no-network fixtures first;
4. cover a tiny representative set:
   E01 deterministic/no-model,
   E02 target ambiguity,
   E08 tool call,
   E09 consequential UNKNOWN receipt,
   E10 privacy/multi-actor,
   entitlement/quota case;
5. implement deterministic DANTE verdict/scorer semantics;
6. verify repeated-trial evidence and artifact export;
7. only then gate provider SDKs/credentials/paid API calls;
8. freeze exact candidate model/binding/HarnessProfile;
9. run direct comparative DANTE evals;
10. produce provider/model/economics/routing candidate;
11. continue concrete runtime/security/control-plane/operations architecture;
12. run independent destructive productionization review;
13. close AI-04 only after unresolved production contradictions are eliminated.
```

No provider/model is selected by this document.

---

# 29. Explicit non-claims

```text
AI-04 CLOSED                         NO
AI-04A CLOSED                        NO
DIRECT DANTE PROVIDER EVAL PASS      NO
PROVIDER SELECTED                    NO
MODEL DEFAULT SELECTED               NO
MULTI-PROVIDER REQUIRED              NO
PROVIDER SDK SELECTED                NO
EVAL RUNNER SELECTED                 NO
INSPECT AI INSTALLED                 NO
PAID MODEL API CALL EXECUTED         NO
COMMERCIAL TIER NAMES/PRICES SET     NO
AI BACKEND IMPLEMENTED               NO
POSTGRESQL/ALEMBIC CHANGED           NO
NEW AI TABLE/INDEX                   NO
PGVECTOR/ANN ACTIVATED               NO
FTS/PG_TRGM ACTIVATED                NO
RESTATE ACTIVATED                    NO
R2 ACTIVATED                         NO
MCP/A2A IMPLEMENTED                  NO
EXECUTION ENVIRONMENT IMPLEMENTED    NO
SC/PSV DIRECT PROOFS EXECUTED        NO
```

This remains architecture/evidence design, not production proof.