# DANTE AI-04A — Direct Evaluation Specification

- **Status:** CLOSED / STRUCTURALLY ACCEPTED / A01..A30 / EV01..EV20
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-04 — Productionization Architecture
- **Sub-phase:** AI-04A — Direct DANTE Eval Specification
- **Original candidate PRE-SCOPE:** `f5ee7e1fc86c1f2e5675ee860bbbadfbc6bde68a`
- **Pre-closure snapshot:** `57d9b6b325d0873e46efbe88eee646f994027d2d`
- **Direct provider evidence:** NOT EXECUTED / DEFERRED UNTIL DECISION-CRITICAL
- **Provider/model selection:** OPEN / EVIDENCE-DRIVEN
- **Eval runner selection:** OPEN
- **Implementation claim:** NONE
- **Database change:** NONE

This document is the durable AI-04A closure authority.

The full executable-grade candidate specification, including DANTE-E01..E13, fixture/grader design, reliability/economics methodology, tooling comparison and commercial-entitlement pressure cases, is preserved immutably at commit `57d9b6b325d0873e46efbe88eee646f994027d2d`.

AI-04A closure is **structural**. It accepts the evaluation/provider/economics methodology. It does not claim that any provider/model has been directly benchmarked or selected.

---

# 1. Objective

DANTE evaluates concrete intelligence configurations against DANTE work rather than public leaderboard reputation.

Primary question:

```text
For this DANTE workload and consequence class,
which currently eligible production route composition
satisfies all hard semantic/privacy/safety gates
and then provides the best quality / reliability /
latency / economics trade-off?
```

Provider/model selection follows this evidence.

---

# 2. Evaluation authority

```text
DANTE Eval Specification
→ DANTE fixtures
→ DANTE expected-state contracts
→ DANTE hard invariants
→ DANTE graders/oracles
→ replaceable runner/framework adapter
→ candidate model/Harness/binding/route composition
```

```text
FRAMEWORK SCORE != DANTE SEMANTIC PASS
OUTCOME/ENVIRONMENT STATE > MODEL SELF-REPORT
```

External eval products may execute or visualize tests. They do not define DANTE truth, Authority, Actual, effect success, history, privacy or memory semantics.

---

# 3. Workload families

Accepted core families:

```text
DANTE-E01  model avoidance / deterministic fast path
DANTE-E02  intent + reference / target resolution
DANTE-E03  structured extraction / understanding
DANTE-E04  native query + history + absence semantics
DANTE-E05  context + privacy + Reality Scope
DANTE-E06  planning / replanning / scenarios
DANTE-E07  document / long-context / multimodal
DANTE-E08  tool / capability use
DANTE-E09  consequential effect boundary
DANTE-E10  multi-actor / delegation / disclosure
DANTE-E11  adaptive memory / learning
DANTE-E12  currentness / failure / supersession / failover
DANTE-E13  open-world research / grounding
```

Trigger-gated suites are created only when product/runtime scope activates them:

```text
voice/realtime
browser/computer use
code execution
long-running durable background work
embedding/vector retrieval
specialized generation
```

---

# 4. Eval contracts are not Domain/persistence owners

Evaluation-only concepts include:

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

These are evaluation contracts only.

```text
EVAL CONTRACT != DOMAIN/RUNTIME PERSISTENCE OWNER
```

No table/service is inferred merely from these nouns.

---

# 5. Fixture / oracle posture

Use a bounded common manifest plus family-specific payload.

Baseline fixture dimensions include, where applicable:

```text
fixture/version
family
risk/consequence class
locale
purpose
Actor / represented party / Subject
Reality Scope
initial state/source refs
provider/data eligibility profile
required capabilities
resource envelope
expected outcome
hard assertions
forbidden outcomes/actions
grading profile
repetition profile
```

Hidden expected state and grader truth remain separated from candidate-visible state.

```text
CANDIDATE ACCESS TO HIDDEN ORACLE
→ INVALID_HARNESS / INVALID_FIXTURE
```

---

# 6. Trial verdicts

Accepted semantic taxonomy:

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

Provider/platform failure does not automatically become model-cognition failure.

```text
COGNITION QUALITY != SERVING-BINDING RELIABILITY
```

---

# 7. Hard failure

Applicable hard failures include:

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
retention/future-reuse outside eligibility
source/derivative resurrection
COMPLETE_REQUIRED answered from unproven approximate coverage
failover to ineligible binding
untrusted data gaining instruction authority
current AuthZ/Consent/Visibility bypass
```

```text
ONE OBSERVED HARD FAILURE
→ QUALIFICATION FAILURE FOR THE APPLICABLE CASE/CONFIGURATION
```

Hard failures are not averaged away by prose quality, latency or price.

---

# 8. Grader hierarchy

Prefer strongest objective evidence:

```text
G1 deterministic state/result
G2 schema/type/constraint
G3 tool/effect receipt
G4 source/citation/evidence
G5 invariant/privacy/security
G6 trajectory where material
G7 human-calibrated rubric
G8 model judge for softer dimensions
```

A model judge cannot overrule canonical fixture state, effect receipt, Authority/Visibility/Consent or hard security facts.

---

# 9. Repeated reliability

One lucky success is not production reliability.

Record at least:

```text
pass@1 / ordinary success rate
quality distribution
hard-failure count
valid-trial count
provider infrastructure failure count
```

For reliability-sensitive workloads, use repeated all-pass measures such as `pass^k` or equivalent explicitly defined statistics.

```text
CAPABILITY EVAL != REGRESSION EVAL
```

Capability eval finds the frontier. Regression eval protects earned behavior.

---

# 10. Dataset and eval-data governance

Initial corpus defaults:

```text
synthetic
semantically valid
deterministic where possible
minimized
no production database dump
no real credentials
```

```text
PRODUCTION TRACE != AUTOMATIC EVAL DATA
EVAL DATASET != AUTOMATIC MEMORY
EVAL LOG != AUDIT AUTHORITY
```

Production-derived cases require explicit purpose, minimization, privacy treatment, retention and provider/grader eligibility.

A grader/model judge is itself a governed data recipient.

Core language coverage includes at least:

```text
it-IT
en-US
```

---

# 11. Candidate identity / reproducibility

Concrete candidate evidence must identify material configuration, including as applicable:

```text
ModelTarget hypothesis
model vendor
serving platform
protocol family
exact model snapshot/version
deployment/endpoint
HarnessProfile
ProviderBinding
feature mode
reasoning/thinking settings
structured-output settings
capability/tool projection
context/security policy refs
retry/fallback policy refs
service tier/resource envelope
```

Moving aliases alone are insufficient qualification identity.

---

# 12. Commercial/service-tier boundary

```text
COMMERCIAL SUBSCRIPTION / SERVICE TIER
!= DANTE DOMAIN Plan
```

Accepted conceptual chain:

```text
CommercialOffering / ServiceTier
→ EntitlementProfile
→ capability + quota + resource envelope
→ Budget / Routing Policy
→ eligible ModelTarget/route set
```

```text
COMMERCIAL TIER != MODEL
COMMERCIAL TIER != PROVIDER
COMMERCIAL TIER != DEPLOYMENT
COMMERCIAL TIER != HARNESSPROFILE
```

Commercial tiers may limit resource/capability envelopes but cannot weaken truth, privacy, Authority, target safety, provider/data eligibility, effect verification/reconciliation or anti-resurrection.

```text
BUDGET EXHAUSTION
MUST NOT ERASE A RECONCILIATION OBLIGATION
```

Exact tier names/prices/quotas remain open.

---

# 13. Economics

Primary architecture metric:

```text
EFFECTIVE COST PER SUCCESSFUL DANTE TASK
```

This may include:

```text
input/output/reasoning usage
cache/storage costs
native tool/search fees
retries
failed attempts
fallback
background execution
```

```text
LIST PRICE PER TOKEN != DANTE COMMERCIAL VIABILITY
```

Commercial viability later compares measured task-cost distributions against candidate entitlement envelopes.

---

# 14. Runner/tooling posture

DANTE owns the eval semantics; the runner remains replaceable.

Current non-binding tooling posture:

```text
Inspect AI
→ preferred runner candidate
→ direct compatibility proof required
→ NOT SELECTED / NOT INSTALLED

OpenAI Evals / Vertex Evaluation /
LangSmith / Braintrust
→ optional platform-specific challengers

Promptfoo
→ possible red-team challenger
```

Remote stochastic paid-model evals should remain outside ordinary backend unit/integration CI by default.

A future bounded tooling boundary may live under `tooling/ai-evals/`, but implementation is not part of AI-04 closure.

---

# 15. Accepted AI-04A invariants

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

---

# 16. Accepted direct-eval invariants

```text
EV01 DANTE OWNS EVAL SEMANTICS; RUNNER/SAAS DOES NOT.
EV02 EVAL CONTRACT != DOMAIN/RUNTIME PERSISTENCE OWNER.
EV03 OUTCOME/ENVIRONMENT STATE OUTRANKS MODEL SELF-REPORT.
EV04 HIDDEN ORACLE STATE MUST NOT LEAK TO THE CANDIDATE.
EV05 ONE EXACT TRAJECTORY IS NOT REQUIRED UNLESS SEMANTICS REQUIRE IT.
EV06 HARD FAILURE CANNOT BE AVERAGED AWAY BY QUALITY/COST.
EV07 INVALID FIXTURE/GRADER/HARNESS != MODEL COGNITION FAILURE.
EV08 MODEL/HARNESS QUALITY != SERVING-BINDING RELIABILITY.
EV09 REPEATED RELIABILITY IS FIRST-CLASS FOR CUSTOMER-FACING BEHAVIOR.
EV10 CAPABILITY EVAL != REGRESSION EVAL.
EV11 PRODUCTION TRACE != AUTOMATIC EVAL DATA.
EV12 EVAL/GRADER DATA FLOW IS GOVERNED LIKE OTHER DATA FLOW.
EV13 IT-IT AND EN-US CORE COVERAGE ARE REQUIRED.
EV14 QUALIFICATION RECORDS EXACT MODEL/HARNESS/BINDING IDENTITY.
EV15 REMOTE/STOCHASTIC DIRECT EVALS DO NOT SILENTLY BECOME ORDINARY BACKEND TEST PASS.
EV16 RUNNER FRAMEWORK IS REPLACEABLE AND MAY NOT DEFINE DANTE SEMANTICS.
EV17 COMMERCIAL SUBSCRIPTION/SERVICE TIER != DOMAIN Plan.
EV18 COMMERCIAL TIER != MODEL != PROVIDER != DEPLOYMENT.
EV19 ENTITLEMENTS MAY LIMIT RESOURCE/CAPABILITY ENVELOPES; THEY MAY NOT WEAKEN TRUTH/PRIVACY/SAFETY FLOORS.
EV20 QUOTA/COST EXHAUSTION MUST NOT ERASE CONSEQUENTIAL RECONCILIATION OBLIGATIONS.
```

---

# 17. Whole-phase hardening applies

AI-04A must be read together with:

- `docs/architecture/dante-ai-04-whole-phase-destructive-acceptance.md`

Whole-phase `WP-01..WP-22` strengthen the transition from evaluation evidence to production routability, including:

```text
eval candidate != production route
Harness + binding composition qualification
fallback independent qualification
auxiliary/sub-model governance
current egress revalidation
fallback context/capability contraction
capability version drift
provider/prompt cache compatibility
hidden-result operational non-interference
model-picker preference != routing authority
route-specific resource admission
per-invocation config coherence
production capacity qualification
```

Where a whole-phase rule is stronger than an earlier AI-04A candidate assumption, the whole-phase rule governs.

---

# 18. Direct provider activation evidence gate

AI-04 architecture can close with provider/model selection OPEN.

Concrete production route activation cannot.

Before activating a real production route, applicable direct DANTE evidence must cover the actual material production composition or prove the production delta independently.

Required evidence is risk/workload dependent but includes, where applicable:

```text
DANTE workload quality
hard semantic/privacy/safety gates
serving-binding reliability
feature-mode/data eligibility
Harness/binding compatibility
mandatory security/control compatibility
effective production-route quality
economics/resource admission
intended production capacity/service envelope
```

---

# 19. Explicit non-claims

```text
AI-04A CLOSED                         YES / STRUCTURAL
DIRECT DANTE PROVIDER EVAL PASS        NO
PROVIDER SELECTED                     NO
MODEL DEFAULT SELECTED                NO
MULTI-PROVIDER REQUIRED               NO
PROVIDER SDK SELECTED                 NO
EVAL RUNNER SELECTED                  NO
INSPECT AI INSTALLED                  NO
API CREDENTIALS USED                  NO
PAID PROVIDER CALL EXECUTED           NO
PRODUCTION CAPACITY PASS              NO
AI BACKEND IMPLEMENTED                NO
COMMERCIAL TIER NAMES/PRICES SET      NO
POSTGRESQL/ALEMBIC CHANGED            NO
NEW AI TABLE/INDEX                    NO
PGVECTOR/ANN/FTS ACTIVATED            NO
RESTATE/R2 ACTIVATED                  NO
MCP/A2A IMPLEMENTED                   NO
EXECUTION ENVIRONMENT IMPLEMENTED     NO
SC/PSV DIRECT PROOFS EXECUTED         NO
```

---

# 20. Next use of this specification

The next phase is not a generic provider benchmark.

AI-05 must translate the accepted AI architecture into a buildable implementation blueprint and identify exactly which concrete decisions are blocked on direct evidence.

Only then should the bounded eval tooling/provider proof be executed for decision-critical candidates.
