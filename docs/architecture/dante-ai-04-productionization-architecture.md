# DANTE AI-04 — Productionization Architecture

- **Status:** CANDIDATE / AI-04A MATERIALIZED / AI-04B MATERIALIZED + INDEPENDENT VALIDATION CURRENT / NOT CLOSED
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-04 — Productionization Architecture
- **Current focus:** AI-04B fresh destructive runtime validation
- **Upstream:** AI-02.1 CLOSED / AI-03 CLOSED
- **AI-03A:** C01..C33
- **AI-03B:** B01..B35
- **AI-03C:** MAT-01..MAT-15
- **AI-04A:** eval/model/provider/economics + entitlement boundary MATERIALIZED / direct provider evidence DEFERRED UNTIL NEEDED
- **AI-04B:** concrete runtime/capability architecture MATERIALIZED / RT-01..RT-20 / INDEPENDENT VALIDATION CURRENT
- **Provider/model selection:** OPEN / EVIDENCE-DRIVEN
- **Commercial tier/pricing selection:** OPEN
- **Implementation claim:** NONE
- **Database change:** NONE

This document is the durable master candidate for AI-04 Productionization Architecture.

Detailed sub-phase authority:

- `docs/architecture/dante-ai-04a-direct-eval-specification.md`
- `docs/architecture/dante-ai-04b-concrete-runtime-capability-architecture.md`

AI-04 converts accepted DANTE intelligence semantics into concrete production choices. It does not reopen AI-02/AI-03 because a provider, SDK, protocol, framework or commercial packaging strategy prefers another shape.

Current sequence:

```text
AI-04A workload/eval/provider/economics architecture
→ materialized

AI-04B concrete runtime/capability architecture
→ first candidate
→ destructive kill-test
→ RT-01..RT-20
→ compound retest PASS CANDIDATE
→ fresh independent validation CURRENT

AI-04C security/privacy/control-plane/operations
→ next after AI-04B closure

then
AI-04 whole-phase destructive acceptance
→ AI-04 closure
→ AI-05 whole-system acceptance + implementation blueprint
→ actual AI implementation workstream(s)
```

Direct provider/model eval tooling remains intentionally deferred until a concrete provider/model decision requires evidence. No API key is required for current AI-04B/AI-04C architecture work.

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
DEFAULT NONCANONICAL PERSISTENCE = NO
```

No provider/eval/commercial/runtime feature may silently turn provider conversation state, cache, file store, tool trace, model output, background job, protocol task or eval log into canonical DANTE state.

---

# 2. AI-04 problem statement

AI-04 must answer:

```text
which workloads require models at all?
which quality/safety/privacy floors are mandatory?
which models/providers/bindings are qualified for which ModelTarget?
how are provider-specific strengths used without provider lock-in?
how are streaming/tools/retries/cancellation/background work normalized?
how are external protocols integrated without becoming DANTE ontology?
how are execution environments/credentials/egress governed?
how are commercial tiers/resource budgets enforced without weakening truth/safety?
how are provider/runtime changes versioned, observed, rolled out and recovered?
```

```text
GENERAL BENCHMARK WIN
!= DANTE PRODUCTION ELIGIBILITY

CHEAP TOKEN PRICE
!= DANTE COMMERCIAL VIABILITY

PROVIDER FEATURE EXISTS
!= DANTE MAY USE IT
```

---

# 3. Provider replaceability — structural boundary

Binding:

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

`ProviderBinding` may represent:

```text
binding identity/version
model vendor
serving platform
protocol family
model family/snapshot or governed alias
endpoint/deployment
region/data-zone
credential/auth profile ref
retention/data-handling profile
capability profile
HarnessProfile ref
qualification/eval version
activation/rollout state
```

A V1 may intentionally use one primary provider while preserving this boundary.

---

# 4. AI-04A workload-first eval architecture

Representative DANTE workload families:

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

Trigger-gated until real scope activates them:

```text
voice/realtime
browser/computer-use
code execution
long-running durable background work
embedding/vector retrieval
specialized generation
```

---

# 5. AI-04A eval authority

DANTE owns evaluation semantics.

```text
DANTE fixtures/oracles/invariants
→ runner/framework adapter
→ model/provider candidate
```

not:

```text
framework score
= DANTE semantic PASS
```

Evaluation-only terms include:

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

They are not Domain/runtime persistence owners.

Strongest evidence first:

```text
deterministic state/result
→ schema/type/constraint
→ tool/effect receipt
→ source/citation
→ invariant/privacy/security
→ trajectory where semantically material
→ human-calibrated rubric/model judge for softer dimensions
```

```text
OUTCOME/ENVIRONMENT STATE
> MODEL SELF-REPORT
```

---

# 6. AI-04A hard-gate posture

A weighted score cannot compensate for:

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
blind failover to ineligible provider
source/derivative resurrection
untrusted data gaining instruction authority
```

Trial/result semantics distinguish:

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

Repeated reliability is first-class; one lucky success is not production evidence.

---

# 7. AI-04A portability vs augmentation

```text
CORE PORTABILITY
same DANTE semantic obligation
+ provider-specific HarnessProfile

PROVIDER-NATIVE AUGMENTATION
native search/files/cache/state/background/computer/etc.
```

Native provider quality does not prove portable DANTE quality.

```text
FEATURE AVAILABLE != FEATURE ELIGIBLE
```

Fallback requires fresh provider/data eligibility and may require rebuilt/minimized ConsumerContext + alternate HarnessProfile.

---

# 8. Economics

Primary technical metric:

```text
EFFECTIVE COST PER SUCCESSFUL DANTE TASK
```

Include applicable:

```text
input/output/reasoning
cache
native tools/search
retries
failures
fallback
background execution
service-tier premiums
```

Cost optimizes only among configurations that already satisfy hard gates.

---

# 9. Commercial offering / entitlement boundary

DANTE already has a Domain `Plan`.

```text
COMMERCIAL SUBSCRIPTION / SERVICE TIER
!= DANTE DOMAIN Plan
```

Provisional control-plane chain:

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

Commercial entitlements may govern resource budgets, concurrency, long-context/background/research allowance, rate limits, priority/service class and premium capability availability.

They may not weaken:

```text
semantic correctness
historical correctness
privacy
Authority/AuthZ/Consent/Visibility
reference-resolution safety
provider/data eligibility
effect verification/reconciliation
anti-resurrection/currentness/supersession
```

No final names (`Base`/`Plus`/`Pro`), prices, quotas or package contents are selected.

---

# 10. AI-04A candidate invariants

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

Detailed `EV01..EV20` live in the AI-04A direct eval specification.

---

# 11. Eval tooling posture

Framework-neutral eval tooling remains useful but is no longer the immediate next action.

Current candidate posture:

```text
Inspect AI
→ preferred direct-eval runner candidate
→ direct Python/repository proof required before adoption
→ NOT selected / NOT installed
```

Preferred future tooling boundary if/when direct provider comparison becomes decision-critical:

```text
tooling/ai-evals/
```

No provider credentials are required for the current architecture work.

---

# 12. AI-04B runtime candidate authority

Detailed runtime authority:

- `docs/architecture/dante-ai-04b-concrete-runtime-capability-architecture.md`

The runtime candidate separates DANTE execution responsibility from external provider calls and protocols.

Core candidate:

```text
Interaction / WorkContract
        ↓
Execution Kernel
        ├ deterministic compute
        ├ solver
        ├ Model Access Runtime
        ├ Capability Runtime
        ├ Execution Environment Broker
        └ Async / Durable Supervisor
        ↓
Verifier
        ↓
ChangeSet / EffectGraph / Effect Runtime
        ↓
Safe Publication
```

These remain logical responsibilities, not one-service-per-box architecture.

---

# 13. Run / invocation / attempt separation

```text
Run
!= ModelInvocation
!= ProviderAttempt
```

A provider attempt may fail while the logical invocation/run remains recoverable.

A Run may legitimately execute no model at all.

Provider identity belongs at the attempt/binding boundary, not in DANTE work semantics.

---

# 14. Three event planes

```text
RAW PROVIDER EVENT
        ↓ adapter
DANTE RUNTIME EVENT
        ↓ maturity/disclosure/verification
DANTE PUBLICATION EVENT
```

Binding:

```text
RAW PROVIDER EVENT
!= DANTE RUNTIME EVENT
!= PUBLICATION EVENT
```

Provider sequence/event IDs may support transport reconnect/deduplication but are not DANTE semantic event identity.

Streaming a proposal does not execute an effect.

---

# 15. Cancellation/supersession

Keep distinct:

```text
client disconnect
stream stop
ProviderAttempt cancel
ModelInvocation cancel
future Run-work cancel
Class-B workflow cancel
supersession
effect rollback/reconciliation
```

```text
CANCEL RUN
!= UNDO ALREADY-DISPATCHED EFFECTS
```

Cancellation cannot erase verification/reconciliation of uncertain or already-dispatched consequences.

---

# 16. Provider outcome / retry semantics

Normalize materially different classes such as:

```text
completed
incomplete
refused
cancelled
invalid request/config
auth failure
rate limited / overloaded / unavailable
network failure
timeout before acceptance known
timeout after acceptance possible
context exhausted
structured-output failure
tool transport failure
background unknown
unknown
```

```text
RETRY
!= AUTOMATIC SAFETY
```

If acceptance/side-effect outcome may be unknown, reread/reconcile before replay.

```text
REFUSAL != INFRASTRUCTURE FAILURE
```

Fallback may not become safety-arbitrage/provider-shopping.

---

# 17. Routing/failover

Baseline routing uses minimum necessary metadata:

```text
required capability
quality floor
context/latency class
consequence class
provider/data eligibility
EntitlementProfile / ResourceBudget
qualified binding health
cost policy
rollout state
```

A full private prompt need not be sent to another model to decide which provider may receive it.

Failover:

```text
classify primary failure
→ determine failover eligibility
→ qualify alternate binding now
→ re-evaluate data/provider eligibility
→ rebuild/minimize ConsumerContext if required
→ alternate HarnessProfile
→ new ProviderAttempt
```

```text
PROVIDER SERVER-SIDE FALLBACK
!= DANTE ROUTING AUTHORITY
```

Hedged multi-provider requests are disabled by default.

---

# 18. Provider continuation/background state

```text
PROVIDER CONTINUATION STATE
!= Interaction Session
!= ConsumerContext
!= ContextManifest
!= BasisManifest
!= DANTE Memory
```

Opaque provider response/conversation/interaction/background/environment IDs are bounded technical/provider state only.

```text
PROVIDER BACKGROUND EXECUTION
!= DANTE DURABLE EXECUTION
```

Candidate execution modes:

```text
INLINE
BOUNDED ASYNC
ELIGIBLE PROVIDER BACKGROUND
CLASS-B DURABLE
```

Class A remains PostgreSQL transactional outbox + bounded worker.
Class B remains Restate, dormant until a real qualifying consumer activates it.

---

# 19. Tool/capability lifecycle

A model tool request is a proposal, not execution authority.

```text
model emits request/deltas
→ wait for finalized arguments
→ parse/schema validation
→ semantic validation
→ resolve capability/version
→ capability eligibility / policy
→ effect policy when consequential
→ dispatch
→ receipt
→ verify/reconcile
→ normalized result
```

```text
PARTIAL TOOL ARGUMENTS
!= EXECUTABLE TOOL REQUEST
```

Provider parallel tool calls do not authorize consequential parallelism:

```text
PROVIDER PARALLEL TOOL CALL
!= EFFECTGRAPH PARALLEL AUTHORIZATION
```

---

# 20. Capability Registry / Discovery / Runtime

Keep separate:

```text
Capability Registry
= identity/version/contract/policy metadata

Capability Discovery
= find bounded relevant subset

Capability Runtime
= validate/authorize/dispatch/observe/reconcile
```

Do not inject an unbounded global tool catalog into every model context.

Provider-native tools remain provider features:

```text
PROVIDER TOOL != DANTE CAPABILITY
```

They still require DANTE source/effect/data/retention/security governance.

---

# 21. MCP boundary

MCP is an external protocol adapter, not DANTE's internal ontology.

```text
DANTE Capability Registry/Runtime
→ MCP adapter
→ external MCP ecosystem
```

Binding:

```text
MCP TOOL DISCOVERY != TRUST
MCP TOOL DESCRIPTION != INSTRUCTION AUTHORITY
MCP SERVER CLAIM != DANTE AUTHORITY
MCP TASK != DANTE RUN
MCP ELICITATION != DANTE APPROVAL
```

Current MCP `2026-07-28` stateless-core/Tasks-extension changes reinforce, rather than weaken, this separation.

Provider-native MCP is optional augmentation only when registration, credentials, data/retention eligibility, capability governance and revocation remain DANTE-controlled.

---

# 22. A2A boundary

A2A is for independent agent-system interoperability.

```text
External Agent
→ A2A adapter
→ Principal/delegation/represented-party resolution
→ Work Intake / WorkContract
→ normal DANTE runtime
```

Binding:

```text
A2A AGENT CARD / CAPABILITY CLAIM != TRUST
A2A TASK != DANTE RUN
A2A TASK STATUS != DANTE CANONICAL STATE
A2A AUTHENTICATION != DANTE AUTHORITY
```

DANTE does not become a permanent collection of domain agents merely because A2A exists.

---

# 23. Execution Environment

Execution Environment activates only where an actual execution surface is needed:

```text
model-generated code
browser/computer automation
repository/file manipulation
complex artifact transformation
untrusted third-party tooling
```

```text
PROVIDER-HOSTED EXECUTION
!= DANTE Execution Environment
```

Provider-hosted code/computer features may be eligible bounded tools, but they do not receive broad DANTE/database/secret credentials by default.

Threat-model-driven isolation remains open:

```text
T0 trusted deterministic compute
T1 WASM/WASI where compatible
T2 hardened container/syscall isolation
T3 microVM/VM for stronger arbitrary-code isolation
```

No sandbox technology is selected yet.

---

# 24. Credential/egress posture

Preferred shape for untrusted/model-generated execution:

```text
Execution Environment
(no broad secrets)
→ typed capability request
→ trusted broker / Capability Runtime
   ├ identity/delegation
   ├ policy
   ├ credential acquisition
   ├ target/egress restrictions
   └ evidence
→ DANTE / external system
```

Network egress should be deny-by-default/capability-bounded where workload compatibility permits.

---

# 25. Browser/computer use and multi-agent

Interface preference:

```text
1 native DANTE semantic capability
2 external application/provider API
3 accessibility/DOM/OS semantic automation
4 visual/pixel computer use
```

Default topology:

```text
one logical DANTE orchestration responsibility
+ deterministic tools
+ selective parallel workers where evidence justifies them
```

No automatic Calendar-Agent/Goal-Agent/Memory-Agent service taxonomy.

---

# 26. Entitlement/resource integration at runtime

```text
WorkContract
+ ConsequenceProfile
+ EntitlementProfile
+ ResourceBudget
+ quality floor
+ provider/data eligibility
→ qualified execution routes
```

```text
ENTITLEMENT AT RUN START
!= PERPETUAL ENTITLEMENT FOR FUTURE WORK
```

Upgrade/downgrade/quota changes may affect future optional work but cannot erase effect/verification/reconciliation obligations already created.

Budget covers more than model tokens:

```text
model calls/tokens/money
native tools/search
external/tool calls
DB work where useful
sandbox CPU/RAM/disk
network egress
parallel workers
active compute time
```

---

# 27. AI-04B first kill-test result

Compound cases included:

```text
stream disconnect/replay
STOP during invocation
STOP after effect dispatch
partial tool-argument deltas
parallel read/write tool proposals
429/overload/outage
refusal + alternate provider
outcome-unknown retry
provider background + process crash
provider background + deletion/revocation
provider storage on no-retention workload
commercial downgrade/quota exhaustion mid-run
provider continuation after Actor switch
MCP catalog/trust drift
malicious MCP description
MCP elicitation mistaken for approval
provider-native MCP broad credentials
A2A capability/authority overclaim
provider-hosted code asking for DANTE secrets
routing requiring private context
hedged requests
provider-side fallback
budget exhaustion while effect is UNKNOWN
```

Initial candidate: **FAIL** until RT hardenings were made explicit.

After RT-01..RT-20: **COMPOUND RETEST PASS CANDIDATE**.

AI-04B remains NOT CLOSED pending fresh independent review.

---

# 28. AI-04B runtime invariants

```text
RT-01  RUN != MODEL INVOCATION != PROVIDER ATTEMPT.
RT-02  RAW PROVIDER EVENT != DANTE RUNTIME EVENT != PUBLICATION EVENT.
RT-03  CLIENT DISCONNECT != STREAM STOP != INVOCATION CANCEL != RUN CANCEL != EFFECT ROLLBACK.
RT-04  PARTIAL TOOL ARGUMENTS != EXECUTABLE TOOL REQUEST.
RT-05  PROVIDER PARALLEL TOOL CALL != EFFECTGRAPH PARALLEL AUTHORIZATION.
RT-06  PROVIDER BACKGROUND EXECUTION != DANTE DURABLE EXECUTION.
RT-07  PROVIDER-STORED CONTINUATION STATE != DANTE SESSION / CONTEXT / MEMORY.
RT-08  RETRY CLASSIFICATION MUST ACCOUNT FOR ACCEPTANCE AND SIDE-EFFECT UNCERTAINTY.
RT-09  REFUSAL != INFRASTRUCTURE FAILURE; NO SAFETY-ARBITRAGE FALLBACK.
RT-10  SERVER-SIDE PROVIDER FALLBACK != DANTE ROUTING AUTHORITY.
RT-11  ROUTING MUST USE MINIMUM NECESSARY INFORMATION AND SELECT ONLY QUALIFIED CURRENT BINDINGS.
RT-12  HEDGED MULTI-PROVIDER EXECUTION IS NOT A SAFE DEFAULT.
RT-13  PROVIDER TOOL != DANTE CAPABILITY; NATIVE TOOLS DO NOT BYPASS SOURCE/EFFECT GOVERNANCE.
RT-14  MCP DISCOVERY / DESCRIPTION != TRUST / AUTHORITY.
RT-15  MCP ELICITATION != DANTE APPROVAL; MCP TASK != DANTE RUN.
RT-16  A2A DISCOVERY / TASK STATUS != DANTE AUTHORITY / CANONICAL STATE / RUN.
RT-17  PROVIDER-HOSTED EXECUTION != DANTE EXECUTION ENVIRONMENT.
RT-18  PROVIDER EVENT SEQUENCE / REPLAY != DANTE SEMANTIC EVENT IDENTITY.
RT-19  ENTITLEMENT/BUDGET CHANGE MAY GOVERN FUTURE WORK BUT CANNOT ERASE EFFECT/RECONCILIATION OBLIGATIONS.
RT-20  NO MODEL/PROVIDER FEATURE MAY SILENTLY REDEFINE DANTE RUNTIME SEMANTICS.
```

---

# 29. Current official-source runtime evidence

AI-04B used current official documentation only to verify protocol/runtime constraints, not to choose a provider.

Evidence snapshot includes:

```text
OpenAI Responses
- background execution available
- response cancellation endpoint
- provider sequence-number stream/retrieve semantics
- partial function/custom-tool argument events before done/final events

Gemini Interactions
- background execution
- poll/stream/reconnect by interaction identity
- event_id / last_event_id replay support
- previous_interaction_id continuation

MCP 2026-07-28
- stateless core
- self-describing/header-routable requests
- cacheable list results
- MRTR/input-required flow
- Tasks extension
- authorization hardening

A2A
- current released specification 1.0.0
- independent agent-system interoperability
```

Provider/protocol facts are time-sensitive and must be rechecked before implementation/qualification.

---

# 30. Decisions still open

```text
actual eval-tooling spike result
final eval runner/framework
provider SDK choices
real credentials/paid API calls
exact candidate model snapshots
actual direct benchmark results
primary V1 provider
fallback provider(s)
exact ModelTarget vocabulary
exact routing algorithm/fallback ordering
normalized event/error schemas
retry/backoff limits
exact client-edge streaming transport
voice/realtime transport
provider background activation
provider-native MCP activation
MCP/A2A exact implementation
browser/computer-use implementation
Execution Environment technology
WASM/container/gVisor/microVM selection
credential broker technology
physical Run/Invocation/Attempt evidence storage
commercial tier names/prices/quotas
exact EntitlementProfile representation
embedding/vector/FTS activation
Restate activation for first real AI Class-B consumer
R2 activation where content vertical requires it
production privacy/region binding choices
```

---

# 31. Current next action

```text
AI-04B — FRESH INDEPENDENT DESTRUCTIVE RUNTIME VALIDATION
```

Required pressure set includes at least:

```text
stream reconnect + duplicate effect prevention
cancel + supersession + outcome-unknown interaction
failover after partial output/tool state
provider background + crash + deletion/revocation
quota/downgrade during consequential work
MCP catalog/cache/trust drift
MCP input-required vs DANTE approval
A2A delegation/confused-deputy cases
provider-native tools + prompt injection + egress
provider-hosted execution + credential boundary
multi-agent parallelism + Authority
retry/idempotency/reconciliation interaction
```

If new contradictions appear, harden the smallest affected boundary and rerun the compound set.

After AI-04B closure:

```text
AI-04C — security/privacy/control-plane/operations
```

Provider/model direct eval and tooling can be activated when a concrete provider/model decision becomes blocked on evidence.

---

# 32. Explicit non-claims

```text
AI-04 CLOSED                         NO
AI-04A FINAL PROVIDER EVAL PASS       NO
AI-04B CLOSED                        NO
AI-04B FINAL INDEPENDENT PASS         NO
PROVIDER SELECTED                    NO
MODEL DEFAULT SELECTED               NO
MULTI-PROVIDER REQUIRED              NO
PROVIDER SDK SELECTED                NO
EVAL RUNNER SELECTED                 NO
INSPECT AI INSTALLED                 NO
API CREDENTIALS USED                 NO
PAID MODEL API EXECUTED              NO
COMMERCIAL TIER NAMES/PRICES SET     NO
PRODUCTION AI BACKEND IMPLEMENTED    NO
FRONTEND STREAMING IMPLEMENTED       NO
POSTGRESQL/ALEMBIC CHANGED           NO
NEW AI TABLE/INDEX                   NO
PGVECTOR/ANN ACTIVATED               NO
FTS/PG_TRGM ACTIVATED                NO
RESTATE ACTIVATED                    NO
R2 ACTIVATED                         NO
MCP/A2A ACTIVATED                    NO
EXECUTION ENVIRONMENT IMPLEMENTED    NO
SANDBOX TECHNOLOGY SELECTED          NO
SC/PSV DIRECT PROOFS EXECUTED        NO
AI-05 STARTED                        NO
```

This remains architecture/evidence design, not production implementation proof.