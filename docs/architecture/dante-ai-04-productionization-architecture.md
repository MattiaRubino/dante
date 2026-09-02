# DANTE AI-04 — Productionization Architecture

- **Status:** CANDIDATE / AI-04A EVAL + PROVIDER BOUNDARY MATERIALIZED / NOT CLOSED
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-04 — Productionization Architecture
- **Initial focus:** representative DANTE eval workload, model/provider/economics, routing/fallback boundary
- **Upstream:** AI-02.1 CLOSED / AI-03 CLOSED
- **AI-03A:** C01..C33
- **AI-03B:** B01..B35
- **AI-03C:** MAT-01..MAT-15
- **PRE-SCOPE:** `aff3d7153aa0c4cf99d4bc28f569bc3db2e82703`
- **Implementation claim:** NONE
- **Provider/model selection:** OPEN / EVIDENCE-DRIVEN
- **Database change:** NONE

This document is the durable candidate architecture for AI-04 Productionization.

AI-04 consumes the accepted DANTE intelligence semantics and materialization boundaries and converts them into production choices. It does **not** reopen AI-02 or AI-03 because one provider SDK, model API or cloud product prefers a different shape.

The first AI-04 boundary is deliberately eval-first:

```text
DANTE obligations
→ representative workloads
→ hard eligibility gates
→ graded quality/economics
→ provider/model/platform candidates
→ direct evidence
→ routing/binding candidate
→ concrete runtime/security/operations design
→ destructive productionization review
→ AI-04 closure
```

Provider selection does not precede this sequence.

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

The AI-03 materialization default remains:

```text
DEFAULT NONCANONICAL PERSISTENCE = NO
```

No AI-04 provider feature may silently turn provider conversation state, cache, file store, search result, tool trace, model output or background job into canonical DANTE state.

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
What changes require requalification?
```

AI-04 is therefore not a vendor beauty contest.

```text
GENERAL LLM BENCHMARK WIN
!=
DANTE PRODUCTION ELIGIBILITY
```

---

# 3. Provider replaceability — accepted production boundary

The existing structural decision remains binding and is refined here.

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

The production chain is:

```text
DANTE work/capability need
→ ModelTarget
→ HarnessProfile
→ ProviderBinding
→ ProviderAdapter
→ concrete serving platform / model / deployment
```

This is a boundary, not an instruction to introduce a generic abstraction framework everywhere.

## 3.1 ModelTarget

`ModelTarget` states what DANTE needs from cognition/execution, not who sells it.

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
cost ceiling
```

The final target vocabulary must be earned from the eval workload. It must not become a vendor-model alias enum.

Bad:

```text
ModelTarget.OPENAI_GPT_5_6_SOL
```

Correct direction:

```text
ModelTarget.REASONING_HIGH
ModelTarget.FAST_STRUCTURED
ModelTarget.LONG_CONTEXT
```

only where the workload corpus proves those distinctions are stable/useful.

## 3.2 HarnessProfile

`HarnessProfile` owns controllable model/provider-specific behavior required to get the best legitimate performance from one evaluated binding.

Examples:

```text
reasoning/thinking effort
system/developer instruction structure
structured-output configuration
tool descriptions and tool-choice posture
message/context packaging
provider-required thought/signature continuity
stream handling
provider-specific safe optimization
```

A portability test does **not** require byte-identical prompts when different APIs have materially different controls.

```text
SAME SEMANTIC CONTRACT
!=
SAME BYTE PROMPT
```

Provider-specific harness optimization is allowed if DANTE semantic requirements remain unchanged and the harness is versioned/evaluated.

## 3.3 ProviderBinding

A `ProviderBinding` resolves a `ModelTarget` to a concrete qualified execution endpoint.

Candidate binding dimensions include:

```text
binding identity/version
model vendor
serving platform
protocol family
model family
exact snapshot/version where available
model alias only if governed
endpoint/deployment
region/data-zone
service tier
credential/auth profile reference
retention/data-handling profile
capability profile
HarnessProfile reference
qualification/eval version
activation state
```

`ProviderBinding` is runtime/control-plane configuration. It is not Domain identity and not a user semantic object merely because it survives configuration changes.

## 3.4 ProviderAdapter

`ProviderAdapter` owns protocol/SDK translation:

```text
request construction
stream-event normalization
structured-output transport
tool/function invocation transport
usage accounting
provider error normalization
rate-limit/retry signals
provider response/receipt identity
cancellation semantics
native capability invocation where explicitly selected
```

It must not own DANTE authority, policy meaning, canonical data semantics or WorkContract interpretation.

---

# 4. Day-one posture

Provider replaceability does not require day-one multi-provider complexity.

```text
ARCHITECTURE
provider-replaceable

V1 IMPLEMENTATION
may intentionally use one primary provider
```

A second provider is justified when it produces material value such as:

```text
higher DANTE quality for a workload
required capability gap
meaningful cost reduction
meaningful latency reduction
eligible residency/compliance posture
resilience/failover need
commercial concentration reduction
```

Do not implement four adapters merely to claim multi-provider support.

The acceptance test is instead:

> Can a qualified `ModelTarget` move to another eligible binding without rewriting DANTE feature, Domain, WorkContract, Context, Retrieval, Memory, Verifier or Effect semantics?

---

# 5. Eval philosophy

DANTE evals start from product/system obligations rather than public model leaderboards.

Public benchmarks are challenger evidence. They cannot prove DANTE correctness.

The evaluation stack has two levels:

```text
LEVEL 1 — HARD ELIGIBILITY / CORRECTNESS GATES
A failure disqualifies the run/configuration for that workload.

LEVEL 2 — GRADED QUALITY / PERFORMANCE / ECONOMICS
Used only among configurations that satisfy Level 1.
```

This prevents a high prose-quality score from compensating for a privacy leak, wrong target or unauthorized effect.

---

# 6. Level-1 hard gates

Representative hard failures include:

```text
wrong consequential target
unauthorized effect proposal/execution path
cross-actor/private-data disclosure
fabricated canonical fact presented as existing DANTE truth
false claim that an effect succeeded
false conversion of elapsed schedule time into Actual/completed state
stale/superseded Run output published as current
Reality Scope laundering
material contradiction ignored where clarification/reconciliation is required
invalid structured command/tool arguments where deterministic validation rejects them
provider failover that violates current data/provider eligibility
invalid durable-memory promotion
source/derivative resurrection after deletion/retirement
COMPLETE_REQUIRED answered through an unproven approximate retrieval path
```

These are not merely penalties in a weighted score.

```text
HARD FAILURE
→ workload/configuration FAIL
```

Some gates can be evaluated deterministically from fixtures/state; others require human-calibrated rubric/independent review. No model judge gets unilateral authority to waive a deterministic failure.

---

# 7. Level-2 graded metrics

Among eligible configurations, compare:

```text
task success
semantic correctness
constraint satisfaction
groundedness/source use
coverage and correct absence handling
clarification quality/efficiency
reference-resolution quality
structured-output success rate
tool-selection success rate
tool-argument success rate
multi-step tool completion
long-context evidence use
contradiction handling
correct abstention/non-action
instruction following
retry/failure rate
TTFT / first useful output
end-to-end latency
token/compute use
provider-native tool charges
cache effects
cost per successful task
```

The final scorecard remains multidimensional. A single scalar may be produced for operational ranking only after all hard gates pass, and the component metrics remain inspectable.

---

# 8. DANTE representative eval workload matrix — candidate

The first workload taxonomy is intentionally product-shaped.

## DANTE-E01 — Model avoidance / deterministic fast path

Tests whether the runtime avoids unnecessary model work.

Examples:

```text
exact arithmetic
known structured aggregation
simple validated lookup
explicit deterministic transform
known bounded calendar computation
```

Expected property:

```text
NO MODEL REQUIRED
→ no model invocation
```

Quality includes correctness and avoiding avoidable latency/cost/privacy exposure.

## DANTE-E02 — Intent + Reference / Target Resolution

Tests:

```text
ambiguous person/project/event references
same-name people
current vs historical target
wrong-but-current object trap
pronoun/session reference
represented-party switches
```

A high-confidence guess is not target proof.

Expected outcomes include exact resolution, bounded clarification or refusal to execute when unresolved.

## DANTE-E03 — Structured extraction / understanding

Input may include natural language, notes, imported text, images/PDF-derived text or external messages.

Evaluate whether the model can produce bounded typed candidate information while preserving:

```text
source
uncertainty
inference status
Reality Scope
no automatic canonical promotion
```

Extraction quality does not authorize persistence/effect.

## DANTE-E04 — Native query + history + absence semantics

Representative questions:

```text
What is current?
What was true as-of T?
What changed?
What is still unresolved?
What was planned vs what actually happened?
What could not be found?
```

Required distinctions include:

```text
absence != false
Observation != Actual
Schedule != Actual
accepted current != historical material state
```

## DANTE-E05 — Context + privacy + Reality Scope

Tests ContextPlan/ConsumerContext behavior against:

```text
purpose limitation
source/use exclusions
sensitive data minimization
cross-context leakage
canonical current vs scenario vs historical
provider eligibility
child/delegated minimization
```

The best answer that used impermissible context fails.

## DANTE-E06 — Planning / replanning / scenario reasoning

Representative problems include overloaded calendars, missed sessions, changed deadlines, temporary modes, pauses/resumes and multi-goal trade-offs.

Hard properties:

```text
hard constraints not silently violated
past history not rewritten
smallest valid replanning scope preferred
trade-offs made explicit
scenario output != canonical current state
material changes require correct preview/approval path
```

## DANTE-E07 — Document / long-context / multimodal reasoning

Do not reduce this to needle-in-a-haystack.

Test:

```text
multiple long documents
contradictory passages
superseded versions
current vs retired material
source-binding accuracy
multimodal source derivative provenance
cross-document synthesis
selective reread/current-state validation
```

Large context window is useful capacity, not proof of correct evidence handling.

## DANTE-E08 — Tool / Capability use

Evaluate:

```text
correct capability selection
correct arguments
correct sequencing
bounded decomposition
handling tool errors
retry discipline
no invented tool success
no direct privileged bypass
```

Model self-report cannot grade effect success.

## DANTE-E09 — Consequential effect preparation / execution boundary

Tests workflows such as creating/moving/cancelling/updating real commitments.

Evaluate:

```text
reference binding
expected-state/currentness
preview/approval requirement
Effect PEP compatibility
revalidation before dispatch
receipt interpretation
outcome-unknown handling
reconciliation obligation
```

## DANTE-E10 — Multi-actor / delegation / disclosure

Fixtures include user, other Person, Subject, Actor, represented party, shared resources and partial disclosure.

Test:

```text
Authority != visibility
private overlay != shared fact
minimum necessary disclosure
role changes
delegation boundaries
third-party memory/retention eligibility
```

## DANTE-E11 — Adaptive memory / learning

Test both correct recall and correct non-recall.

Cases include:

```text
declared preference
observed behavior
uncertain inference
temporary exception
confirmed reusable rule
correction/deactivation/deletion
sensitive reuse restrictions
canonical promotion
basis drift
anti-resurrection
```

Hard rule:

```text
MODEL REQUEST TO REMEMBER
!= MEMORY ADMISSION
```

## DANTE-E12 — Currentness / failure / supersession / failover

Inject failures:

```text
state changes during Run
user supersedes work
permission revoked
provider timeout
rate limit
provider partial output
tool ambiguous outcome
primary provider unavailable
alternate provider ineligible for current data
```

Expected behavior is safe degradation/revalidation/reconciliation, not blind continuation.

## DANTE-E13 — Open-world research / grounding

Evaluate fresh external research where required:

```text
source quality
citation/source binding
currentness
conflicting sources
separation of external assertion from canonical DANTE truth
correct uncertainty
```

Provider-native web tools may be tested here, but their output does not bypass DANTE Source Standing/Context rules.

## Trigger-gated workload families

Do not force these into baseline provider qualification until a product requirement activates them:

```text
voice/realtime
browser/computer-use
code execution
long-running durable background execution
embedding/vector retrieval
specialized image/audio generation
```

When activated, they receive their own fixtures, hard gates and platform eligibility review.

---

# 9. Eval dataset design

A trustworthy DANTE suite needs more than hand-authored happy paths.

Candidate corpus layers:

```text
A. deterministic synthetic fixtures
B. product-simulation-derived scenarios
C. adversarial semantic/privacy/failure cases
D. generated combinatorial/property cases where useful
E. manually curated difficult cases
F. later sanitized production-derived cases only under explicit eval-data governance
```

Split discipline:

```text
DEVELOPMENT
visible while tuning HarnessProfile

VALIDATION
used for model/binding comparison and architecture decisions

HELD-OUT REGRESSION
protected against continuous prompt overfitting
```

A model/provider should not receive production qualification solely on the same fixtures used to tune its harness.

---

# 10. Grading architecture

Prefer strongest available objective evidence.

Order:

```text
1. deterministic state/result grader
2. schema/type/constraint grader
3. tool/effect receipt grader
4. source/citation/evidence grader
5. invariant/privacy/security grader
6. human-calibrated rubric/model judge for softer dimensions
```

Model judges are useful for qualities such as explanation clarity, planning usefulness or nuanced comparison, but cannot override exact repository/domain state.

```text
MODEL-JUDGE AGREES
!= CANONICAL STATE PROOF
```

Judge prompts/models themselves require versioning and calibration.

---

# 11. Model/Harness evaluation vs serving-platform qualification

Two different things must not be collapsed.

```text
MODEL + HARNESS QUALITY EVALUATION
→ can this cognition configuration solve the DANTE workload?

SERVING PLATFORM / BINDING QUALIFICATION
→ can this concrete platform serve it safely, reliably and economically?
```

The same model family on two serving platforms may reuse some cognitive evidence only where snapshot/behavior equivalence is demonstrated.

Every concrete binding still requires validation of relevant:

```text
API/protocol compatibility
model/deployment version identity
feature availability
retention/data handling
region/data residency/processing
credential/auth flow
quota/rate limits
latency
streaming/cancellation
error behavior
availability/SLA posture
cost/billing
native tool semantics
```

```text
SAME MODEL FAMILY
!= AUTOMATICALLY SAME PRODUCTION BINDING
```

---

# 12. Core portability vs provider-native augmentation

Provider replacement must be tested without discarding provider strengths.

## 12.1 Core portability track

Use DANTE-owned semantic fixtures and capabilities.

Goal:

```text
same DANTE obligation
+ provider-specific HarnessProfile allowed
→ compare portable model execution quality
```

This track proves whether a different binding can perform the core work without rewriting DANTE semantics.

## 12.2 Provider-native augmentation track

Separately test optional native capabilities such as:

```text
web/search grounding
provider file search
prompt/context caching
provider conversation/interactions state
background execution
computer/browser use
code execution
native multi-agent orchestration
```

A native feature may improve quality/cost/latency while remaining provider-specific.

It is selected only if its incremental value exceeds lock-in/retention/operational cost and it remains correctly wrapped by DANTE boundaries.

---

# 13. Feature eligibility

A capability existing in a provider API is not enough.

Binding rule:

```text
FEATURE AVAILABLE
!= FEATURE ELIGIBLE
```

Before use, evaluate at least:

```text
WorkContract purpose
Actor / represented party
Subject/data classes
sensitivity
provider processing eligibility
retention/storage behavior
regional requirements
third-party exposure
current Consent/AuthZ/Visibility rules
source/use restrictions
recovery/deletion implications
```

Examples of stateful/provider-native features that require explicit eligibility include stored conversations/interactions, files, prompt caches, background jobs, code/computer-use artifacts and third-party MCP/web calls.

---

# 14. Provider failover

Failover is not request replay.

Rejected:

```text
PRIMARY ERROR
→ send same request/context to every configured provider
```

Required direction:

```text
primary failure
→ determine whether alternate binding is currently qualified
→ re-run provider/data eligibility for this WorkContract/purpose
→ rebuild/minimize ConsumerContext for alternate binding when needed
→ select alternate HarnessProfile
→ invoke
→ preserve provider transition/evidence
```

If no eligible binding exists, DANTE degrades/fails safely.

Provider continuity is not DANTE continuity.

```text
Interaction Session continuity
!= provider server-side conversation continuity
```

---

# 15. Versioning and requalification

Provider aliases and model families can move independently of DANTE releases.

A qualified binding therefore needs enough identity to answer what was evaluated.

Material change triggers requalification proportional to risk, including as applicable:

```text
model snapshot/version change
alias moving to a new snapshot
HarnessProfile change
provider API behavior change
tool semantics change
retention/data-policy change
serving platform change
region/deployment change
reasoning/thinking control change
structured-output behavior change
major price/tokenization change
```

A provider marketing claim of backwards compatibility does not replace DANTE regression evidence.

Preview/experimental models may enter comparison as challengers but do not automatically become production bindings.

```text
QUALITY WIN
!= PRODUCTION QUALIFICATION
```

---

# 16. Economics

Do not optimize by list price per million tokens alone.

Primary economic metric:

```text
EFFECTIVE COST PER SUCCESSFUL DANTE TASK
```

Include where applicable:

```text
input tokens
output/thinking tokens
cache write/read/storage
native search/tool charges
retries
failed attempts
fallback invocation
background execution charges
latency/service-tier premium
```

Measure by context/workload buckets, for example:

```text
small
medium
large
extreme / near context limit
```

Tokenization differences across providers/models mean identical source text does not imply identical billed tokens.

Cost is considered only after hard eligibility gates.

---

# 17. Initial current provider/model landscape — evidence only

This section records a **2026-09-02 official-source research snapshot**. It is not a selection.

## 17.1 OpenAI direct

Current official OpenAI API documentation exposes GPT-5.6 Sol, Terra and Luna through Responses and related API surfaces. The family offers roughly 1.05M context and 128K output across the three tiers, with current API pricing documented per model.

DANTE-relevant native capabilities include function/tool use and provider-native search/file/computer capabilities, subject to endpoint/model/data-control eligibility.

OpenAI data controls distinguish abuse-monitoring logs from application state. Responses can store application state; approved Zero Data Retention changes `store` behavior and some features remain incompatible with ZDR. Background mode and some stateful tools have separate storage implications.

Consequences:

```text
OpenAI model quality
!= automatic eligibility for every OpenAI native feature
```

## 17.2 Azure OpenAI / Microsoft Foundry

Microsoft documentation currently exposes GPT-5.6 Sol/Terra/Luna on Azure OpenAI Responses API with explicit model versions/deployments.

Azure can therefore be an alternate serving platform for OpenAI model families while retaining Azure-specific endpoint/deployment/auth/region/operational characteristics.

This validates the need for:

```text
model vendor = OpenAI
serving platform = Azure OpenAI
model/deployment = separately bound
```

A direct OpenAI binding and Azure OpenAI binding are not treated as the same production object merely because the model family matches.

## 17.3 Anthropic direct / alternate hosting

Current Anthropic documentation exposes Claude Opus 5 and Claude Sonnet 5 as active models with 1M context and up to 128K output, with different price/performance positions and provider-specific thinking/tool behavior.

Anthropic commercial API data is normally retained up to 30 days unless different terms apply. Approved ZDR arrangements exist, but explicit prompt caching, some batch behavior and Files API can have different retention behavior.

Therefore Anthropic native Files/cache/tool features require per-feature eligibility rather than inheriting API-level assumptions.

The same architecture can support Claude through different qualified serving arrangements without letting those platform details enter DANTE Domain/feature semantics.

## 17.4 Google Gemini

Current Google documentation lists Gemini 3.7 Flash as stable/GA with a 1M context window and current promotional pricing through 2026-12-31. Gemini 3.5 Flash-Lite is a stable cost-oriented candidate. Gemini 3.1 Pro remains Preview and therefore is challenger evidence unless separately production-qualified.

Gemini Interactions API is materially stateful by default: `store=true`; paid-tier interactions are retained for 55 days by default, with configurable shorter project retention. `store=false` is available but is incompatible with background execution and prevents future continuation via `previous_interaction_id`.

Consequences:

```text
Gemini background/continuation feature available
!= eligible for every DANTE workload
```

## 17.5 Initial candidate tiers

Illustrative comparison field only:

```text
FRONTIER / HARD REASONING
OpenAI GPT-5.6 Sol
Anthropic Claude Opus 5
Gemini preview/pro-class challenger only where current production status permits

BALANCED
OpenAI GPT-5.6 Terra
Anthropic Claude Sonnet 5
Google Gemini 3.7 Flash

COST / HIGH VOLUME
OpenAI GPT-5.6 Luna
Anthropic Haiku-class candidate where applicable
Google Gemini 3.5 Flash-Lite
```

This is **not** a routing decision. Candidate membership can change before direct DANTE evals run.

---

# 18. Official-source research basis — 2026-09-02 snapshot

Decision-relevant official sources checked for this candidate include:

```text
OpenAI
- GPT-5.6 Sol / Terra / Luna model documentation
- OpenAI API model catalogue
- OpenAI API data controls / retention controls

Microsoft
- Azure OpenAI Responses API supported model/version documentation

Anthropic
- Claude Opus 5 / Sonnet 5 migration/model documentation
- Anthropic commercial API retention policy
- Anthropic Zero Data Retention applicability documentation

Google
- Gemini model catalogue
- Gemini 3.7 Flash current model documentation
- Gemini API pricing
- Gemini Interactions API storage/retention behavior
```

This evidence is version-sensitive. AI-04 direct qualification must record the exact evidence date/version and must re-check material claims before final provider selection.

---

# 19. Initial AI-04A conceptual kill-test

The first candidate was attacked against common provider-selection failure modes.

## KILL-01 — same-prompt fairness fallacy

Bad assumption:

```text
same bytes to every provider = fair comparison
```

Why it fails:

Provider APIs expose materially different reasoning/tool/message controls. Byte-identical prompting can unfairly underuse or misconfigure one model.

Hardening:

```text
same DANTE semantic obligation
+ separately versioned HarnessProfile
```

## KILL-02 — model judge owns truth

Bad assumption:

```text
LLM judge says PASS
→ PASS
```

Hardening:

Deterministic/state/schema/effect/source/invariant graders precede softer model-judge scoring.

## KILL-03 — native tool quality contaminates portability

Bad assumption:

A model with excellent proprietary web/file/computer tooling automatically proves itself as the portable DANTE model layer.

Hardening:

Separate core portability track from provider-native augmentation track.

## KILL-04 — model quality = cloud/platform qualification

Bad assumption:

The same model family on OpenAI direct and Azure OpenAI is one tested binding.

Hardening:

Separate model/Harness evidence from serving-platform/binding qualification.

## KILL-05 — cheap failure wins weighted score

Bad assumption:

A low-cost model can compensate privacy/semantic failures through economics.

Hardening:

Hard gates precede graded cost/quality scoring.

## KILL-06 — preview benchmark winner becomes production default

Hardening:

Preview/experimental models are challenger-only until production qualification passes.

## KILL-07 — provider feature exists, therefore use it

Hardening:

```text
FEATURE AVAILABLE != FEATURE ELIGIBLE
```

Provider-native storage/retention/background/cache/files/tools are evaluated per WorkContract/data/purpose.

## KILL-08 — blind cross-provider failover

Hardening:

Fresh eligibility decision + alternate ConsumerContext/HarnessProfile rebuild before alternate invocation.

## KILL-09 — floating aliases silently change production behavior

Hardening:

Binding/version qualification and material-change re-evaluation.

## KILL-10 — every AI request must use a model

Hardening:

DANTE-E01 keeps deterministic/no-model execution first-class.

## KILL-11 — long-context test = needle retrieval

Hardening:

Long-context fixtures include contradiction, version/currentness, Reality Scope, source lifecycle and source binding.

## KILL-12 — pricing page proves economics

Hardening:

Measure cost per successful DANTE task under actual tokenization/tool/cache/retry behavior.

First result:

```text
NEW DOMAIN OWNER                  NO
DOMAIN REOPEN                     NO
LOGICAL REOPEN                    NO
PHYSICAL REOPEN                   NO
POSTGRESQL/ALEMBIC CHANGE         NO
NEW TOP-LEVEL AI SEMANTIC OWNER   NO
CONCRETE PROVIDER SELECTION       NO
CONCRETE MODEL DEFAULT            NO
PROVIDER SDK SELECTION            NO
IMPLEMENTATION PASS               NO
```

No material structural contradiction was found in the eval/provider-selection boundary after these hardenings.

This is not AI-04 closure.

---

# 20. Candidate invariants — AI-04A

```text
A01  DANTE WORKLOAD EVIDENCE PRECEDES CONCRETE PROVIDER/MODEL SELECTION.

A02  MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT.

A03  MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY.

A04  DANTE FEATURE/DOMAIN/SEMANTIC CODE MUST NOT DEPEND DIRECTLY
     ON A CONCRETE PROVIDER SDK IDENTITY.

A05  PROVIDER REPLACEABLE != PROVIDERS IDENTICAL.

A06  PROVIDER REPLACEABLE != LOWEST-COMMON-DENOMINATOR PROVIDER USAGE.

A07  SAME SEMANTIC CONTRACT != SAME BYTE PROMPT.

A08  MODEL + HARNESS QUALITY != SERVING-PLATFORM/BINDING QUALIFICATION.

A09  HARD SEMANTIC/SAFETY/PRIVACY ELIGIBILITY PRECEDES
     GRADED QUALITY/ECONOMICS.

A10  A MODEL JUDGE CANNOT OVERRIDE DETERMINISTIC CANONICAL/SCHEMA/EFFECT FACTS.

A11  CORRECT NON-ACTION / ABSTENTION / CLARIFICATION IS PART OF QUALITY.

A12  PROVIDER-NATIVE AUGMENTATION != CORE PORTABILITY PROOF.

A13  FEATURE AVAILABLE != FEATURE ELIGIBLE.

A14  PROVIDER SERVER-SIDE STATE != DANTE INTERACTION/CANONICAL CONTINUITY.

A15  PROVIDER FAILOVER != BLIND REQUEST REPLAY.

A16  FAILOVER REQUIRES CURRENT PROVIDER/DATA ELIGIBILITY
     AND MAY REQUIRE A NEW CONSUMERCONTEXT/HARNESSPROFILE.

A17  SAME MODEL FAMILY != AUTOMATICALLY SAME PRODUCTION BINDING.

A18  QUALIFIED MODEL/ALIAS/HARNESS/PLATFORM CHANGES REQUIRE
     RISK-PROPORTIONATE REQUALIFICATION.

A19  PREVIEW/EXPERIMENTAL QUALITY WIN != PRODUCTION QUALIFICATION.

A20  LIST PRICE PER TOKEN != EFFECTIVE COST PER SUCCESSFUL DANTE TASK.

A21  LONG CONTEXT CAPACITY != CONTEXT CORRECTNESS.

A22  MODEL AVOIDANCE IS A VALID AND OFTEN PREFERRED MODEL ROUTE.
```

These invariants are candidate AI-04A productionization rules pending later direct validation and whole AI-04 destructive review.

---

# 21. What remains open after this candidate

AI-04A materialization does not answer yet:

```text
final DANTE eval fixture corpus
exact hard-gate thresholds
exact scoring aggregation
exact candidate model snapshots
actual direct benchmark results
primary V1 provider
fallback provider(s)
exact ModelTarget vocabulary
routing algorithm/policy
control-plane storage/config mechanics
provider SDK choice
stream normalization implementation
structured-output implementation
background/durable execution activation
Restate activation
MCP/A2A implementation
Execution Environment technology
provider-native file/cache/state selections
production rate/cost budgets
production privacy/region binding choices
```

These remain AI-04 work.

---

# 22. Exact next action

The next pass must not jump directly to implementation or declare a winner from public benchmarks.

Sequence:

```text
1. turn DANTE-E01..E13 into an executable-grade evaluation specification
   with fixture types, expected-state contracts and grading rules;

2. identify which cases can be graded deterministically from DANTE state
   and which require calibrated human/model-judge review;

3. select a small current candidate set per likely ModelTarget;

4. freeze exact model snapshots/bindings/HarnessProfiles for comparison;

5. implement direct eval/proof harness only if required to generate evidence;

6. compare quality + hard failures + latency + effective cost;

7. produce a provider/model/routing candidate;

8. continue AI-04 concrete runtime/security/control-plane/operations design;

9. run independent destructive productionization review;

10. close AI-04 only after unresolved production contradictions are eliminated.
```

No provider/model is selected by this document.

---

# 23. Explicit non-claims

```text
AI-04 CLOSED                         NO
AI-04A DIRECT BENCHMARK PASS         NO
PROVIDER SELECTED                    NO
MODEL DEFAULT SELECTED               NO
MULTI-PROVIDER REQUIRED              NO
PROVIDER SDK SELECTED                NO
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

This is an architecture candidate and evidence framework, not production proof.