# DANTE AI-04B — Concrete Runtime + Capability Architecture

- **Status:** CANDIDATE / FIRST DESTRUCTIVE KILL-TEST HARDENED / INDEPENDENT VALIDATION NEXT / NOT CLOSED
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-04 — Productionization Architecture
- **Sub-phase:** AI-04B — Concrete Runtime + Capability Architecture
- **PRE-SCOPE:** `cef3105aafc7adbbe77f60a578a1e450e5cad5d3`
- **Upstream:** AI-02.1 CLOSED / AI-03 CLOSED / AI-04A candidate materialized
- **Provider/model selection:** OPEN / EVIDENCE-DRIVEN
- **Provider SDK selection:** OPEN
- **Implementation claim:** NONE
- **Database change:** NONE

This document converts the accepted DANTE intelligence responsibilities into a concrete provider-neutral runtime architecture without selecting a concrete provider, SDK, transport, sandbox product or production deployment topology.

It is intentionally a **runtime responsibility and failure-semantics specification**, not implementation code and not a microservice map.

---

# 1. Objective

AI-04B must answer how DANTE executes intelligence work when real providers, streams, tools, external effects, background work, external protocols and isolated execution environments are involved.

The target is:

```text
one DANTE semantic runtime
+ replaceable model/provider bindings
+ explicit capability/effect governance
+ explicit failure/cancellation/reconciliation semantics
+ bounded use of provider-native features
+ no provider protocol becoming DANTE ontology
```

The runtime must remain compatible with the accepted capability-first modular-monolith backend posture unless later measured evidence justifies extraction.

---

# 2. Binding upstream invariants

AI-04B inherits without weakening:

```text
PostgreSQL = sole canonical persistence/material-history authority
Interaction Session != Run != Worker
MODEL OUTPUT != PUBLISHABLE OUTPUT
INTERNAL STREAM != RECIPIENT STREAM
DISPLAY NAME != EFFECT TARGET
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
CANCEL RUN != UNDO ALREADY-DISPATCHED EFFECTS
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
Context != Retrieval != Memory
provider state != canonical DANTE state
ProviderBinding != Domain identity
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
FEATURE AVAILABLE != FEATURE ELIGIBLE
PROVIDER FAILOVER != BLIND REQUEST REPLAY
DEFAULT NONCANONICAL PERSISTENCE = NO
semantic obligation != technical execution/audit evidence
```

AI-04B does not reopen Domain, Logical, Physical, PostgreSQL Constitution, AI-02 or AI-03 merely because a provider exposes a different API shape.

---

# 3. Runtime responsibility map

Candidate production responsibility flow:

```text
Interaction Edge / Session
        ↓
Work Intake
        ↓
WorkContract
        ↓
Execution Kernel
        │
        ├─ deterministic compute
        ├─ solver
        │
        ├─ Context Engine / Semantic Query boundary
        │
        ├─ Model Access Runtime
        │     ↓
        │   ModelTarget
        │     ↓
        │   Routing Policy
        │     ↓
        │   HarnessProfile
        │     ↓
        │   ProviderBinding
        │     ↓
        │   ProviderAdapter
        │     ↓
        │   ProviderAttempt
        │
        ├─ Capability Runtime
        │     ├ registry
        │     ├ discovery
        │     ├ validation
        │     ├ policy enforcement
        │     ├ dispatch
        │     └ receipt/result normalization
        │
        ├─ Execution Environment Broker
        │
        └─ Async / Durable Supervisor
              ├ inline
              ├ bounded async
              ├ eligible provider-background execution
              └ Class-B durable execution when triggered

        ↓
Verifier
        ↓
ChangeSet / EffectGraph / Effect Runtime
        ↓
Result Maturity / Disclosure / Safe Publication
```

These are responsibilities. They do not imply one service, table, queue or deployment per box.

---

# 4. Run, ModelInvocation and ProviderAttempt

The runtime must not collapse the lifetime of DANTE work into one external API call.

```text
Run
= one bounded DANTE execution responsibility/objective

ModelInvocation
= one logical request for model cognition inside a Run

ProviderAttempt
= one concrete attempt to execute a ModelInvocation against one ProviderBinding
```

Example:

```text
Run R17
  └ ModelInvocation M4
       ├ ProviderAttempt P1 → timeout before accepted outcome known
       └ ProviderAttempt P2 → alternate eligible binding → completed
```

A ProviderAttempt may fail while the ModelInvocation or Run remains recoverable.

A Run may complete without any ModelInvocation when deterministic compute or a solver is sufficient.

These names are runtime concepts, not automatic persistence/table requirements.

---

# 5. Model Access Runtime

The Model Access Runtime owns orchestration around provider-neutral model execution.

Responsibilities include:

```text
resolve qualified candidate bindings
apply routing/budget/entitlement policy
select HarnessProfile
construct provider-neutral invocation intent
invoke ProviderAdapter
normalize provider events/results/errors
supervise timeout/cancellation/retry/fallback
account usage/cost
surface evidence to Verifier and observability
```

It must not own:

```text
Domain truth
Authority
canonical Context/Memory semantics
Effect authorization
publication permission
provider-specific business logic
```

---

# 6. ProviderAdapter boundary

A ProviderAdapter owns protocol/SDK mechanics only.

Candidate responsibilities:

```text
request serialization
provider auth transport
stream connection mechanics
provider event decoding
structured-output transport
function/tool-call transport
provider-native built-in-tool transport
provider continuation/background locators
usage accounting extraction
provider error normalization
provider cancellation API
provider response/receipt IDs
```

It must not decide:

```text
which user data may leave DANTE
whether a tool is authorized
whether an effect may execute
whether a provider refusal should be bypassed
whether output is publishable
whether provider state is canonical memory
```

---

# 7. Three event planes

DANTE must separate provider wire events from runtime semantics and publication semantics.

```text
RAW PROVIDER EVENT
        ↓ ProviderAdapter
DANTE RUNTIME EVENT
        ↓ verification / disclosure / publication
DANTE PUBLICATION EVENT
```

Examples of raw provider events include provider-specific text deltas, function-argument deltas, reasoning metadata, tool lifecycle events, sequence numbers or background status changes.

Candidate normalized runtime event families may include:

```text
InvocationStarted
OutputDelta
StructuredOutputCandidate
ToolRequestPartial
ToolRequestFinalized
ToolExecutionStarted
ToolExecutionFinished
ProviderUsageUpdated
ProviderAttemptFailed
ProviderAttemptCancelled
InvocationCompleted
InvocationIncomplete
InvocationRefused
```

Exact names remain implementation-detail candidates.

Important:

```text
RAW PROVIDER EVENT IDENTITY
!= DANTE SEMANTIC EVENT IDENTITY
```

Provider event sequence numbers may be used to reconnect/deduplicate transport but do not become canonical DANTE history.

---

# 8. Streaming semantics

Streaming is a transport/presentation optimization, not semantic authority.

A model may stream text while DANTE still withholds publication of claims/effects that require verification or disclosure checks.

```text
model stream
→ normalized runtime stream
→ maturity/disclosure checks
→ client-safe stream
```

For consequential work:

```text
STREAMED PROPOSAL
!= EXECUTED EFFECT
```

For structured output/tool calls:

```text
PARTIAL DELTA
!= FINALIZED VALUE
```

Backpressure and bounded buffering must be explicit so a slow/disconnected client does not force unbounded memory growth or implicitly cancel all underlying work.

---

# 9. Reconnect and replay

Providers may expose reconnect/replay primitives such as sequence numbers or event IDs.

DANTE may use them as transport state when current eligibility allows it.

Requirements:

```text
replayed raw event
→ deduplicate at transport/runtime boundary
→ do not repeat a finalized tool/effect dispatch
→ do not duplicate client-visible semantic events
```

A provider reconnect cursor is bounded technical state, not DANTE memory.

If replay safety cannot be established, DANTE must reconcile from provider/current state rather than guessing.

---

# 10. Cancellation scopes

Cancellation must be explicit by scope.

```text
CLIENT DISCONNECT
!= OUTPUT STREAM STOP
!= MODEL INVOCATION CANCEL
!= PROVIDER ATTEMPT CANCEL
!= FUTURE RUN-WORK CANCEL
!= DURABLE WORKFLOW CANCEL
!= EFFECT ROLLBACK
```

Candidate cancellation path:

```text
user/client requests stop
→ stop scheduling optional future work
→ stop publication stream where applicable
→ request cancellation of current eligible ProviderAttempt
→ cancel bounded local/sandbox work where safe
→ propagate cancellation to durable children where semantics permit
→ preserve verification/reconciliation for already-dispatched effects
```

If an external effect may already have been accepted, cancellation cannot replace reconciliation.

---

# 11. Supersession is not cancellation

A new user instruction may supersede prior work without implying that all prior side effects disappear.

```text
new WorkContract
→ supersedes remaining objective of old Run
→ stop obsolete future reasoning where possible
→ retain already materialized consequences/evidence
→ reconcile unresolved attempts/effects
```

The runtime must make stale/superseded output ineligible for current publication when appropriate.

---

# 12. Provider outcome taxonomy

Provider/API outcomes must be normalized without pretending every failure is equivalent.

Candidate classes:

```text
completed
incomplete
refused
cancelled
invalid_request
invalid_configuration
auth_failure
rate_limited
overloaded
provider_unavailable
network_failure
timeout_before_acceptance_known
timeout_after_acceptance_possible
context_exhausted
structured_output_invalid
tool_transport_failure
provider_background_unknown
unknown
```

Exact implementation enum remains open.

The distinction between failure-before-acceptance and outcome-unknown-after-possible-acceptance is critical for safe retry behavior.

---

# 13. Retry policy

Retry is an evidence-driven operation, not a generic `for attempt in range(3)`.

```text
safe transient failure before side effect / before provider acceptance
→ bounded retry may be allowed

possible accepted provider/tool/effect state but response lost
→ outcome unknown
→ retrieve/reconcile before replay
```

Retry decisions consider:

```text
operation purity
provider idempotency guarantees
idempotency key/scope
effect state
attempt evidence
remaining budget
current provider eligibility
current WorkContract/supersession state
```

---

# 14. Refusal is not infrastructure failure

Provider/model refusal is a semantic output class, not automatically an outage.

Rejected:

```text
provider A refuses
→ provider B refuses
→ provider C maybe agrees
```

as a generic fallback algorithm.

```text
REFUSAL
!= INFRASTRUCTURE FAILURE
```

DANTE routing/fallback may not become safety-arbitrage or policy shopping.

A refusal may trigger bounded clarification, safe alternative behavior or escalation according to DANTE policy, not blind vendor hopping.

---

# 15. Routing policy

Baseline routing should be deterministic/inspectable from minimum necessary metadata.

Candidate input dimensions:

```text
required capability
quality floor
latency class
context envelope
structured-output/tool requirements
consequence class
data/provider eligibility
region/residency constraints
EntitlementProfile
ResourceBudget
qualified binding health
current price/cost policy
rollout/canary state
```

The router should not require sending private full task context to a separate LLM merely to decide which provider is allowed to receive it.

```text
ROUTING DECISION
SHOULD USE MINIMUM NECESSARY INFORMATION
```

A learned/model router remains a future optimization only if direct eval proves value without weakening privacy/inspectability.

---

# 16. Provider failover

Failover chain:

```text
primary ProviderAttempt fails
→ classify failure
→ determine whether failover is semantically allowed
→ re-evaluate alternate binding qualification
→ re-evaluate current provider/data eligibility
→ rebuild/minimize ConsumerContext where required
→ apply alternate HarnessProfile
→ create new ProviderAttempt
```

Rejected:

```text
primary fails
→ copy identical serialized payload to another provider
```

The alternate provider may have different retention, state, tooling or context behavior.

Provider server-side fallback features may be used only as a bounded optimization if DANTE can still prove the resulting binding remains within its routing/eligibility policy.

```text
PROVIDER SERVER-SIDE FALLBACK
!= DANTE ROUTING AUTHORITY
```

---

# 17. Hedged requests

Sending the same task to multiple providers concurrently can reduce tail latency but also multiplies cost and data exposure.

Default:

```text
HEDGED MULTI-PROVIDER REQUESTS
DISABLED
```

A future exception requires direct evidence and at least:

```text
read-only/pure workload
all providers independently eligible
no consequential tool/effect path
bounded duplicate state exposure
measured tail-latency benefit
measured economic benefit
explicit deduplication semantics
```

---

# 18. Provider continuation state

Provider-native continuation artifacts may include response IDs, interaction IDs, conversation IDs, cache handles, encrypted reasoning/continuation blocks, background job IDs or provider environment IDs.

They are classified as bounded technical/provider state.

```text
PROVIDER CONTINUATION STATE
!= Interaction Session
!= ConsumerContext
!= ContextManifest
!= BasisManifest
!= DANTE Memory
!= canonical history
```

If retained, they require:

```text
binding/provider identity
purpose
eligibility
retention/expiry
source Run/Invocation linkage
safe deletion/revocation posture
```

Cross-provider failover reconstructs DANTE context rather than attempting to translate opaque provider memory.

---

# 19. Provider background execution

Provider-native background execution can be useful for long model operations, but it is not DANTE durable execution.

```text
PROVIDER BACKGROUND JOB
!= DANTE DURABLE RUN
```

Candidate execution modes:

```text
INLINE
ordinary interactive request

BOUNDED ASYNC
short/retryable work whose durability semantics are simple

PROVIDER BACKGROUND
provider-owned continued execution only when state/retention/data eligibility permits

CLASS-B DURABLE
DANTE durable workflow when crash/wait/callback/human-approval/reconciliation semantics require it
```

Provider background state may be orchestrated by a durable DANTE workflow when a real consumer requires both.

---

# 20. Class-A and Class-B remain binding

Accepted project decision remains:

```text
Class A
PostgreSQL transactional outbox + bounded worker

Class B
Restate selected but dormant until first real Class-B durable workflow
```

AI-04B does not reactivate the selection debate because providers now expose background APIs.

```text
BACKGROUND CAPABILITY
!= DURABILITY SEMANTICS
```

Restate activation still requires a real qualifying consumer and its existing privacy/recovery proof obligations.

---

# 21. Structured output

Structured generation has multiple correctness layers:

```text
provider constrained generation
→ structural/schema validation
→ semantic/application validation
→ grounding/evidence validation
```

Valid JSON does not prove a valid DANTE action or fact.

Provider-specific structured-output mechanics live in HarnessProfile/ProviderAdapter; DANTE semantic schema/invariants do not.

---

# 22. Tool request lifecycle

A model tool request is a proposal to invoke a capability, not authority to execute it.

Required flow:

```text
model emits tool request/deltas
→ wait for finalized arguments
→ transport parse
→ schema/type validation
→ semantic validation
→ resolve capability version
→ Capability PEP / eligibility
→ Effect PEP when consequential
→ dispatch
→ receipt
→ verification/reconciliation where required
→ normalized tool result
→ model continuation / result maturity
```

Critical:

```text
PARTIAL TOOL ARGUMENTS
!= EXECUTABLE TOOL REQUEST
```

Provider streaming may expose function-call argument deltas before a final argument object exists. Those deltas are never dispatched.

---

# 23. Capability registry, discovery and runtime

Keep separate:

```text
Capability Registry
= identity/version/contract/policy metadata

Capability Discovery
= select the small relevant capability subset

Capability Runtime
= validate/authorize/dispatch/observe/reconcile
```

The model receives only a bounded projection of capability metadata necessary for current work.

A large global tool catalog should not be injected into every prompt merely because it exists.

Lazy discovery/search is preferred when capability cardinality grows.

---

# 24. Parallel tool calls

Providers may emit multiple tool calls in parallel.

That does not authorize DANTE to run consequential effects concurrently.

```text
PROVIDER PARALLEL TOOL CALL
!= EFFECTGRAPH PARALLEL AUTHORIZATION
```

Independent read-only operations may execute concurrently when policy/resource limits permit.

Consequential operations obey ChangeSet/EffectGraph dependencies, target state, approval and verification regardless of provider emission order.

---

# 25. Provider-native tools

Built-in provider tools such as search, file search, code execution or computer use are provider capabilities, not DANTE semantic capabilities by definition.

```text
PROVIDER TOOL
!= DANTE CAPABILITY
```

Use requires:

```text
WorkContract fit
provider/data eligibility
source standing/currentness treatment
retention/state review
cost/resource budget
security/injection review
result normalization
verification where consequential
```

Native-tool quality belongs to the AI-04A augmentation track, not core portability proof.

---

# 26. MCP boundary

MCP is an external protocol adapter, not DANTE's internal capability ontology.

Preferred direction:

```text
DANTE Capability Registry / Runtime
        ↓
MCP client/server adapter
        ↓
external MCP ecosystem
```

not:

```text
MCP tool schema
= DANTE canonical capability definition
```

Binding rules:

```text
MCP TOOL DISCOVERY != TRUST
MCP TOOL DESCRIPTION != INSTRUCTION AUTHORITY
MCP SERVER CLAIM != DANTE AUTHORITY
MCP TASK != DANTE RUN
MCP ELICITATION != DANTE APPROVAL
```

A remote MCP server may supply data or requests; DANTE still owns identity/delegation, policy, capability/effect governance and result truth.

---

# 27. MCP 2026-07-28 implications

Current MCP `2026-07-28` moved the protocol core to stateless request/response semantics, made requests self-describing, introduced header-based routing/cacheable list results, strengthened authorization and moved Tasks into an extension.

DANTE implications:

```text
protocol session state is not required for DANTE continuity
cached tool discovery requires current trust/eligibility revalidation
MCP Tasks extension does not become DANTE durable execution automatically
MRTR/input-required behavior does not become DANTE approval automatically
protocol authorization does not replace application Authority
```

Legacy MCP transport/session assumptions must not leak into DANTE architecture.

---

# 28. Provider-native MCP

Some model platforms can connect directly to remote MCP servers.

Default DANTE posture remains:

```text
model
→ DANTE Capability Runtime / controlled MCP gateway
→ registered external MCP server
```

Provider-native MCP is an optional augmentation only when DANTE can still govern:

```text
server identity/registration
credentials/scopes
purpose/data eligibility
retention/third-party exposure
capability set
effect policy
observability/evidence
revocation
```

No provider-native MCP feature may bypass DANTE capability/effect enforcement.

---

# 29. A2A boundary

A2A is for interoperating with independent agent systems.

Candidate direction:

```text
External Agent
      ↓ A2A
DANTE A2A Adapter
      ↓
Principal / delegation / represented-party resolution
      ↓
Work Intake / WorkContract
      ↓
normal DANTE runtime
```

Binding rules:

```text
A2A AGENT CARD / CAPABILITY CLAIM != TRUST
A2A TASK != DANTE RUN
A2A TASK STATUS != DANTE CANONICAL STATE
A2A AUTHENTICATION != DANTE AUTHORITY
```

Do not decompose DANTE internally into artificial “Calendar Agent / Goal Agent / Memory Agent” services merely to use A2A.

---

# 30. External-agent delegation

External agents create a confused-deputy risk.

Runtime must preserve enough context to distinguish:

```text
technical Principal
initiating Actor where applicable
represented party
external client/application
external agent identity
delegation/scopes
purpose
recipient
```

An authenticated external agent must not silently inherit all Authority of a represented human.

DANTE credentials must not be blindly forwarded downstream.

---

# 31. Execution Environment boundary

`Execution Environment` is an AI-02 responsibility activated only for workloads that actually need an execution environment.

Typical cases:

```text
model-generated code
browser/computer automation
repository/file manipulation
complex artifact transformation
untrusted third-party tooling
```

Ordinary conversation/reasoning does not require creating a sandbox.

Candidate environment manifest dimensions:

```text
environment identity/version
workspace lifecycle
inspection surfaces
allowed capabilities
filesystem/mount policy
network/egress policy
resource limits
timeouts
artifact locations
verification/test commands
```

---

# 32. Provider-hosted execution vs DANTE environment

Provider-hosted code/computer/sandbox features may be useful but remain provider environments.

```text
PROVIDER-HOSTED EXECUTION
!= DANTE Execution Environment
```

They may be used for eligible bounded computation/file analysis where DANTE does not need to grant broad trusted credentials.

They must not silently receive:

```text
PostgreSQL owner/runtime credentials
secret-manager credentials
broad service tokens
unbounded user delegation
high-value application secrets
```

When generated code needs privileged DANTE/external operations, use a DANTE-controlled capability/credential broker.

---

# 33. Isolation posture

AI-04B retains threat-model-driven isolation rather than choosing one technology now.

Candidate tiers remain:

```text
T0 trusted deterministic compute
T1 WASM/WASI where workload fits
T2 hardened container / syscall-isolated environment
T3 microVM/VM for stronger arbitrary-code isolation
```

Technology selection remains open and must be benchmarked against real workload compatibility, startup latency, isolation strength, resource controls and operational burden.

---

# 34. Credential and egress broker

Untrusted/model-generated execution should not hold high-value credentials directly.

Preferred shape:

```text
Execution Environment
(no broad secret material)
        ↓ typed capability request
Trusted Broker / Capability Runtime
        ├ identity/delegation
        ├ policy
        ├ credential acquisition
        ├ target restriction
        ├ egress restriction
        └ evidence/audit
        ↓
DANTE / external system
```

Network egress should be deny-by-default or capability-bounded for untrusted environments where feasible.

---

# 35. Browser and computer-use hierarchy

Prefer the least fragile interface that expresses the required operation:

```text
1 DANTE/native semantic capability
2 external provider/application API
3 accessibility/DOM/OS semantic automation
4 visual/pixel computer use
```

Moving down the hierarchy generally increases fragility, latency, security surface and verification burden.

Computer use remains trigger-gated, not baseline runtime.

---

# 36. Multi-agent topology

Default:

```text
one logical DANTE orchestration responsibility
+ deterministic tools
+ selective parallel workers when evidence justifies them
```

Multi-agent decomposition is justified only for real independent subproblems, isolation, specialization, latency or scale benefits.

Do not mirror product domains into permanent agent identities by default.

Parallel workers do not gain independent Authority merely because they are separate agents.

---

# 37. Resource and entitlement integration

Runtime routing consumes the commercial/resource boundary defined in AI-04A.

```text
WorkContract
+ ConsequenceProfile
+ EntitlementProfile
+ ResourceBudget
+ required quality floor
+ provider/data eligibility
        ↓
qualified execution routes
```

Commercial entitlement can govern future optional resource use, not truth/safety floors.

```text
ENTITLEMENT AT RUN START
!= PERPETUAL ENTITLEMENT FOR ALL FUTURE WORK
```

An upgrade/downgrade or quota change may affect future model/tool/background work.

It cannot erase already-created effect, verification or reconciliation obligations.

---

# 38. Resource accounting

Budgeting includes more than tokens:

```text
model calls
input/output/reasoning tokens
money
native tool/search charges
tool/external calls
DB work where meaningful
sandbox CPU/RAM/disk
network egress
parallel workers
active compute time
```

Waiting calendar time is distinct from active compute.

Backpressure/degradation policy may reduce optional work, model tier or parallelism only while preserving the applicable quality/safety floor.

---

# 39. Operational evidence boundary

AI-04B produces runtime evidence for later AI-04C observability/audit/control-plane design.

At minimum the runtime must make it possible to distinguish:

```text
Run identity
ModelInvocation identity
ProviderAttempt/binding identity
routing reason/version
provider result/error class
usage/cost
capability/tool requests
cancellation/fallback/retry events
provider continuation/background locator refs
verification/effect/reconciliation refs
```

This does not decide physical telemetry/audit persistence.

```text
TELEMETRY != AUDIT != CANONICAL DOMAIN TRUTH
```

---

# 40. Current official-source evidence ledger

AI-04B used current provider/protocol documentation only to validate runtime boundary assumptions, not to select a vendor.

Current evidence includes:

```text
OpenAI Responses API
- response status includes completed/failed/in_progress/cancelled/queued/incomplete
- response cancellation endpoint exists
- streaming events carry provider sequence numbers
- function/custom-tool inputs can arrive as partial delta events before done/final events
- background execution is an available request mode
- retrieval can resume streaming from a provider sequence position

Gemini Interactions API
- background execution returns an interaction identity
- clients can poll/stream/reconnect
- stream reconnect can use event_id / last_event_id
- provider continuation can use previous_interaction_id
- provider-managed execution/environment state exists for some workloads

MCP 2026-07-28
- stateless protocol core
- self-describing requests / header-based routing
- cacheable ordered list responses
- MRTR/input-required flow
- Tasks moved to extension
- authorization hardening

A2A
- current released specification 1.0.0
- intended for communication between independent agent systems
```

Official references used during this pass:

- `https://developers.openai.com/api/reference/cli/resources/beta/subresources/responses`
- `https://developers.openai.com/api/reference/cli/resources/responses/methods/create`
- `https://developers.openai.com/api/reference/cli/resources/responses/methods/retrieve`
- `https://ai.google.dev/gemini-api/docs/background-execution`
- `https://blog.modelcontextprotocol.io/posts/2026-07-28/`
- `https://a2a-protocol.org/dev/specification/`

Provider facts are time-sensitive and must be rechecked before implementation/qualification.

---

# 41. First destructive runtime kill-test

The initial AI-04B candidate was attacked with compound cases including:

```text
client disconnect during stream
user STOP while model call remains active
STOP after external effect dispatch
partial streamed tool arguments
parallel read and consequential write calls
provider 429 / overload / outage
provider refusal followed by alternate provider
provider timeout after native tool/effect-like work
OpenAI-direct → cloud-hosted/alternate binding failover
provider background task + DANTE process crash
provider background state + later deletion/revocation
provider background requiring storage on a no-retention workload
active Run + commercial tier downgrade
provider continuation reused after Actor/represented-party switch
MCP catalog cached across authorization/trust change
malicious MCP tool description
MCP input-required/elicitation mistaken for approval
provider-native MCP with broad credential
A2A Agent Card capability/authority overclaim
A2A task outliving DANTE Run semantics
provider-hosted code requesting DANTE secret
sandbox timeout after external dispatch
routing requiring full private context
hedged two-provider request
stream replay duplicating events/tool call
context window exhaustion mid-Run
untrusted search/web result carrying instructions
opaque provider continuation/reasoning state
provider server-side fallback changing binding
budget exhausted while external outcome is UNKNOWN
```

The first candidate **FAILED** these combined pressures until the RT hardenings below were made explicit.

---

# 42. AI-04B runtime invariants

```text
RT-01
RUN != MODEL INVOCATION != PROVIDER ATTEMPT.

RT-02
RAW PROVIDER EVENT != DANTE RUNTIME EVENT
!= PUBLICATION EVENT.

RT-03
CLIENT DISCONNECT != STREAM STOP != INVOCATION CANCEL
!= RUN CANCEL != EFFECT ROLLBACK.

RT-04
PARTIAL TOOL ARGUMENTS != EXECUTABLE TOOL REQUEST.

RT-05
PROVIDER PARALLEL TOOL CALL
!= EFFECTGRAPH PARALLEL AUTHORIZATION.

RT-06
PROVIDER BACKGROUND EXECUTION
!= DANTE DURABLE EXECUTION.

RT-07
PROVIDER-STORED CONTINUATION STATE
!= DANTE SESSION / CONTEXT / MEMORY.

RT-08
RETRY CLASSIFICATION MUST ACCOUNT FOR
ACCEPTANCE AND SIDE-EFFECT UNCERTAINTY.

RT-09
REFUSAL != INFRASTRUCTURE FAILURE.
NO SAFETY-ARBITRAGE FALLBACK.

RT-10
SERVER-SIDE PROVIDER FALLBACK
!= DANTE ROUTING AUTHORITY.

RT-11
ROUTING MUST USE MINIMUM NECESSARY INFORMATION
AND SELECT ONLY QUALIFIED CURRENT BINDINGS.

RT-12
HEDGED MULTI-PROVIDER EXECUTION IS NOT A SAFE DEFAULT.

RT-13
PROVIDER TOOL != DANTE CAPABILITY.
NATIVE TOOLS DO NOT BYPASS SOURCE/EFFECT GOVERNANCE.

RT-14
MCP DISCOVERY / DESCRIPTION != TRUST / AUTHORITY.

RT-15
MCP ELICITATION != DANTE APPROVAL.
MCP TASK != DANTE RUN.

RT-16
A2A DISCOVERY / TASK STATUS
!= DANTE AUTHORITY / CANONICAL STATE / RUN.

RT-17
PROVIDER-HOSTED EXECUTION
!= DANTE EXECUTION ENVIRONMENT.

RT-18
PROVIDER EVENT SEQUENCE / REPLAY
!= DANTE SEMANTIC EVENT IDENTITY.

RT-19
ENTITLEMENT/BUDGET CHANGE MAY GOVERN FUTURE WORK
BUT CANNOT ERASE EFFECT/RECONCILIATION OBLIGATIONS.

RT-20
NO MODEL/PROVIDER FEATURE MAY SILENTLY
REDEFINE DANTE RUNTIME SEMANTICS.
```

---

# 43. Compound retest after RT-01..RT-20

After incorporating RT-01..RT-20, the candidate survives the first compound runtime retest at the **architecture level**:

```text
provider swap does not redefine DANTE Run
stream reconnect cannot authorize duplicate effect
cancel does not pretend rollback
partial tool args cannot dispatch
parallel model proposals remain EffectGraph-governed
background provider work does not become durability authority
provider state remains replaceable technical state
refusal cannot be bypassed through provider shopping
MCP/A2A claims do not create Authority
provider sandbox does not inherit trusted credentials
commercial downgrade cannot erase reconciliation
```

This is **PASS CANDIDATE**, not closure.

AI-04B requires a fresh independent destructive validation before it may become CLOSED / STRUCTURALLY ACCEPTED.

---

# 44. Decisions intentionally still open

```text
concrete provider/model set
provider SDK choice
exact ModelTarget vocabulary
exact routing algorithm
exact normalized event type names/schema
exact error enum
exact retry limits/backoff
exact failover ordering
exact client-edge transport: SSE/WebSocket/etc.
voice/realtime transport
provider background feature activation
Restate activation for first AI Class-B consumer
MCP client/server implementation
provider-native MCP activation
A2A implementation
browser/computer-use implementation
Execution Environment technology
WASM/gVisor/microVM/container selection
credential broker implementation technology
physical Run/Invocation/Attempt evidence storage
commercial tier names/prices/quotas
```

These require later AI-04 evidence and/or AI-05 implementation blueprint decisions.

---

# 45. Explicit non-claims

```text
AI-04 CLOSED                         NO
AI-04B CLOSED                        NO
AI-04B FINAL INDEPENDENT PASS         NO
PROVIDER SELECTED                    NO
MODEL DEFAULT SELECTED               NO
PROVIDER SDK SELECTED                NO
API CREDENTIALS USED                 NO
PAID MODEL API CALL EXECUTED         NO
PRODUCTION AI BACKEND IMPLEMENTED    NO
FRONTEND STREAMING IMPLEMENTED       NO
RESTATE ACTIVATED                    NO
MCP ACTIVATED                        NO
A2A ACTIVATED                        NO
EXECUTION ENVIRONMENT IMPLEMENTED    NO
SANDBOX TECHNOLOGY SELECTED          NO
POSTGRESQL/ALEMBIC CHANGED           NO
NEW AI TABLE/INDEX                   NO
PGVECTOR/FTS ACTIVATED               NO
R2 ACTIVATED                         NO
AI-05 STARTED                        NO
```

---

# 46. Exact next action

```text
AI-04B — FRESH INDEPENDENT DESTRUCTIVE RUNTIME VALIDATION
```

The independent pass must attempt to break the candidate without assuming RT-01..RT-20 are sufficient.

At minimum retest:

```text
stream reconnect + duplicate tool/effect prevention
cancel + supersession + outcome-unknown interaction
provider failover after partial output/tool state
provider background + crash + deletion/revocation
commercial downgrade/quota exhaustion mid-effect
MCP catalog/cache/trust drift
MCP input-required vs user approval
A2A delegation/confused-deputy cases
provider-native tools + prompt injection + egress
provider-hosted execution + credential boundary
multi-agent parallelism + Authority
retry/idempotency/reconciliation interaction
```

If a fresh structural contradiction appears, harden the smallest affected boundary and rerun the compound set.

Only after independent AI-04B closure should routing move to AI-04C security/privacy/control-plane/operations architecture.

No provider/model/API key is required for this architecture validation.