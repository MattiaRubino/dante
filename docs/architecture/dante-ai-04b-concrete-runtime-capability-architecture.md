# DANTE AI-04B — Concrete Runtime + Capability Architecture

- **Status:** CLOSED / STRUCTURALLY ACCEPTED / FINAL INDEPENDENT VALIDATION COMPLETE
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-04 — Productionization Architecture
- **Sub-phase:** AI-04B — Concrete Runtime + Capability Architecture
- **Initial PRE-SCOPE:** `cef3105aafc7adbbe77f60a578a1e450e5cad5d3`
- **Independent-validation PRE-SCOPE:** `221cb9473df8f7b3264d3cef2f3bc6a3ab145430`
- **Upstream:** AI-02.1 CLOSED / AI-03 CLOSED / AI-04A candidate materialized
- **Final runtime hardenings:** `RT-01..RT-31`
- **Provider/model selection:** OPEN / EVIDENCE-DRIVEN
- **Provider SDK selection:** OPEN
- **Implementation claim:** NONE
- **Database change:** NONE

This document converts the accepted DANTE intelligence responsibilities into a concrete provider-neutral runtime architecture without selecting a concrete provider, SDK, client transport, sandbox product or production deployment topology.

It is a **runtime responsibility and failure-semantics specification**, not implementation code, not a persistence schema and not a microservice map.

The validation chronology is intentionally preserved:

```text
RESEARCH / CURRENT PROVIDER-PROTOCOL VERIFICATION
→ FIRST RUNTIME CANDIDATE
→ FIRST DESTRUCTIVE KILL-TEST FAIL
→ RT-01..RT-20
→ COMPOUND RETEST PASS CANDIDATE
→ FRESH INDEPENDENT VALIDATION FAIL
→ RT-21..RT-31
→ FINAL COMPOUND RETEST PASS
→ AI-04B CLOSED / STRUCTURALLY ACCEPTED
```

No historical FAIL is rewritten as an earlier PASS.

---

# 1. Objective

AI-04B defines how DANTE executes intelligence work when real models, streams, tools, external effects, background execution, external protocols and isolated execution environments are involved.

Target:

```text
one DANTE semantic runtime
+ replaceable model/provider bindings
+ explicit capability/effect governance
+ explicit failure/cancellation/reconciliation semantics
+ bounded provider-native features
+ protocol adapters that never become DANTE ontology
+ no implementation convenience that weakens accepted semantics
```

The runtime remains compatible with the accepted capability-first modular-monolith backend posture unless future measured evidence justifies extraction.

---

# 2. Binding upstream authority

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
ConsumerContext != ContextManifest != BasisManifest
provider state != canonical DANTE state
ProviderBinding != Domain identity
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
FEATURE AVAILABLE != FEATURE ELIGIBLE
PROVIDER FAILOVER != BLIND REQUEST REPLAY
DEFAULT NONCANONICAL PERSISTENCE = NO
semantic obligation != technical execution/audit evidence
```

AI-04B does **not** reopen Product, Domain, Logical, Physical, PostgreSQL Constitution, AI-02 or AI-03 merely because a provider exposes a different API or protocol shape.

---

# 3. Runtime responsibility map

```text
Interaction Edge / Session
        ↓
Work Intake
        ↓
WorkContract
        ↓
Execution Kernel
        │
        ├─ Deterministic Compute
        ├─ Solver
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

These are logical responsibilities. They do not imply one deployment, service, table, queue or worker class per box.

---

# 4. Run, ModelInvocation and ProviderAttempt

```text
Run
= one bounded DANTE execution responsibility/objective

ModelInvocation
= one logical request for model cognition inside a Run

ProviderAttempt
= one concrete attempt to execute a ModelInvocation against one ProviderBinding
```

Binding:

```text
RUN != MODEL INVOCATION != PROVIDER ATTEMPT
```

A ProviderAttempt may fail while the logical ModelInvocation or Run remains recoverable.

A Run may contain zero model invocations when deterministic compute or a solver is sufficient.

Provider identity belongs at binding/attempt level, not in DANTE work semantics.

These runtime concepts do not automatically require durable rows or new persistence owners.

---

# 5. Model Access Runtime

Owns:

```text
qualified binding resolution
routing / entitlement / budget inputs
HarnessProfile selection
provider-neutral invocation intent
ProviderAdapter invocation
provider event/result/error normalization
timeout / cancellation / retry / fallback supervision
usage/cost evidence
runtime evidence for verification/observability
```

Does not own:

```text
Domain truth
Authority
canonical Context/Memory semantics
Effect authorization
publication permission
provider-specific business meaning
```

---

# 6. ProviderAdapter

Owns only provider/SDK/protocol mechanics:

```text
request serialization
provider authentication transport
stream connection/reconnection mechanics
raw provider event decoding
structured-output transport
tool/function-call transport
provider-native built-in-tool transport
provider continuation/background locators
usage extraction
provider error normalization
provider cancellation mechanics
provider response/tool/event IDs
```

It does not decide which data may leave DANTE, whether a capability/effect is authorized, whether a refusal should be bypassed, whether output is publishable or whether provider state is memory/truth.

---

# 7. Three event planes

```text
RAW PROVIDER EVENT
        ↓ ProviderAdapter
DANTE RUNTIME EVENT
        ↓ verification / disclosure / result maturity
DANTE PUBLICATION EVENT
```

Binding:

```text
RAW PROVIDER EVENT
!= DANTE RUNTIME EVENT
!= DANTE PUBLICATION EVENT
```

Provider sequence/event IDs may support transport reconnection and deduplication but never become DANTE semantic event identity.

Candidate runtime event families may later include invocation lifecycle, output deltas, finalized structured output, tool request lifecycle, usage updates and provider-attempt outcomes. Exact implementation names remain open.

---

# 8. Streaming and publication

Streaming is transport/presentation optimization, not semantic authority.

```text
provider stream
→ normalized runtime stream
→ maturity / disclosure / verification
→ recipient-safe publication stream
```

For consequential work:

```text
STREAMED PROPOSAL != EXECUTED EFFECT
```

For structured output/tool calls:

```text
PARTIAL DELTA != FINALIZED VALUE
```

Backpressure/buffering must be bounded. Slow or disconnected clients do not automatically own cancellation semantics for the underlying Run.

Independent validation adds a stronger publication rule:

```text
PUBLISHED DELTA = EXTERNALIZATION
```

Once recipient-visible bytes leave DANTE they cannot be assumed retractable. Required disclosure/result-maturity checks therefore occur **before** irreversible publication of protected or consequential claims.

DANTE publication sequencing is DANTE-owned and independent from provider stream sequence numbers.

---

# 9. Reconnect, replay and deduplication

Provider replay cursors/event IDs are bounded transport state.

```text
replayed provider event
→ transport/runtime deduplication
→ no repeated finalized capability/effect dispatch
→ no duplicate DANTE publication semantic event
```

Binding:

```text
PROVIDER EVENT SEQUENCE / REPLAY
!= DANTE SEMANTIC EVENT IDENTITY
```

If replay safety cannot be established, reconcile against provider/current application state rather than guessing.

---

# 10. Cancellation scopes

Keep distinct:

```text
client disconnect
output stream stop
ProviderAttempt cancel request
ModelInvocation cancel
future Run-work cancel
Class-B workflow cancellation
supersession
effect rollback / compensation / reconciliation
```

Binding:

```text
CLIENT DISCONNECT
!= STREAM STOP
!= INVOCATION CANCEL
!= RUN CANCEL
!= EFFECT ROLLBACK
```

Candidate stop path:

```text
request stop
→ stop scheduling optional future work
→ stop publication where applicable
→ request provider/local cancellation where safe
→ propagate cancellation to attached children where semantics permit
→ preserve verification/reconciliation for dispatched or uncertain effects
```

Independent validation adds:

```text
CANCELLATION REQUESTED
!= CANCELLATION CONFIRMED
!= EXECUTION QUIESCED
```

Late provider/tool/background events remain eligible for correlation/reconciliation until the runtime has evidence of the actual outcome.

---

# 11. Supersession

```text
new WorkContract
→ supersedes obsolete remaining objective
→ stop obsolete future reasoning where possible
→ retain already materialized consequence/evidence
→ reconcile unresolved effects/provider attempts
→ prevent stale superseded output from current publication
```

```text
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
```

---

# 12. Provider outcome taxonomy

Provider outcomes require materially distinct normalized classes such as:

```text
completed
incomplete
refused
cancel requested / cancel observed
invalid request/configuration
auth failure
rate limited
overloaded
provider unavailable
network failure
timeout before acceptance known
timeout after acceptance possible
context exhausted
structured-output failure
tool transport failure
provider-background unknown
unknown
```

Exact enums remain implementation-detail work.

The architecture requires distinction between safe pre-acceptance failure and uncertainty after possible acceptance/side effect.

---

# 13. Retry

Retry is evidence-driven, never generic fixed repetition.

```text
safe transient failure before acceptance/side effect
→ bounded retry MAY be allowed

possible accepted provider/tool/effect state with lost response
→ OUTCOME UNKNOWN
→ retrieve/reread/reconcile before replay
```

Retry considers:

```text
operation purity
provider idempotency guarantees
DANTE semantic idempotency scope
current effect state
attempt evidence
current WorkContract/supersession
current eligibility
remaining resource envelope
```

---

# 14. Provider IDs vs DANTE idempotency

Independent validation found a critical gap:

```text
PROVIDER TOOL/CALL/RESPONSE ID
!= DANTE CAPABILITY/EFFECT IDEMPOTENCY IDENTITY
```

Provider IDs are attempt-level correlation/evidence only. Retry/replay/failover may produce different provider IDs for the same intended DANTE operation.

DANTE semantic effect identity/idempotency must bind to DANTE-owned operation scope such as bounded work/effect intent, resolved target, normalized operation/arguments, expected state and permit/idempotency scope.

A provider call ID must never be the sole duplicate-effect barrier.

---

# 15. Refusal

```text
REFUSAL != INFRASTRUCTURE FAILURE
```

Rejected generic policy:

```text
provider A refuses
→ provider B
→ provider C
→ use whoever eventually complies
```

Failover cannot become safety-arbitrage or refusal shopping. Refusal may instead lead to safe alternative behavior, clarification or governed escalation.

---

# 16. Routing

Baseline routing is deterministic/inspectable using minimum necessary information.

Inputs may include:

```text
required capability
quality floor
latency/context class
structured-output/tool requirements
consequence class
provider/data eligibility
region/residency
EntitlementProfile
ResourceBudget
qualified binding health
cost policy
rollout/canary state
```

```text
ROUTING SHOULD USE MINIMUM NECESSARY INFORMATION
```

Do not disclose a full private task to an auxiliary routing model merely to decide which provider may receive the task.

Learned/model routing remains optional and benchmark-gated.

---

# 17. Failover

```text
primary attempt fails
→ classify failure
→ establish whether failover is semantically allowed
→ qualify alternate binding now
→ re-evaluate current provider/data eligibility
→ rebuild/minimize ConsumerContext where required
→ bind current alternate HarnessProfile
→ create new ProviderAttempt
```

Rejected:

```text
primary fails
→ replay identical serialized provider request to another vendor
```

```text
PROVIDER SERVER-SIDE FALLBACK != DANTE ROUTING AUTHORITY
```

Any server-side fallback facility is usable only if DANTE can prove all resulting bindings/features remain inside current qualification and eligibility policy.

---

# 18. Hedged execution

Default:

```text
HEDGED MULTI-PROVIDER EXECUTION = DISABLED
```

Future exception requires direct evidence and at least pure/read-only workload, independent eligibility for every recipient, no consequential effect path, bounded duplicate exposure, explicit deduplication and measured latency/economic value.

---

# 19. Provider continuation state

Provider continuation artifacts may include response/interaction/conversation IDs, cache handles, encrypted continuation blocks, background IDs or provider environment IDs.

They are bounded provider/technical state only.

```text
PROVIDER CONTINUATION STATE
!= Interaction Session
!= ConsumerContext
!= ContextManifest
!= BasisManifest
!= DANTE Memory
!= canonical history
```

If retained, bind at least provider/binding identity, purpose, source Run/Invocation, eligibility, expiry/retention and deletion/revocation posture.

Cross-provider failover rebuilds DANTE context instead of translating opaque provider memory.

Independent validation strengthens this boundary:

```text
PROVIDER CONTINUATION HANDLE
!= HARNESS / POLICY / TOOL / CAPABILITY CONTINUITY
```

A continued provider interaction must bind the **current qualified HarnessProfile, current capability projection and current applicable policy**. Provider history reuse must not silently freeze old tools, instructions, policy or delegation.

---

# 20. Feature-mode qualification

Provider qualification is not a blanket approval for every feature exposed by that provider.

```text
PROVIDER/BINDING ELIGIBLE
!= EVERY INVOCATION FEATURE MODE ELIGIBLE
```

Material feature modes include, where applicable:

```text
stored vs non-stored invocation
provider conversation/continuation
background mode
provider-native search/file state
provider-native MCP
provider code/computer execution
extended prompt/cache state
provider server-side fallback
```

Each material mode can change retention, third-party exposure, continuity, deletion, regional or security behavior and therefore belongs to binding/runtime qualification.

Feature-mode choice is not an innocent arbitrary request flag.

---

# 21. Provider background execution

```text
PROVIDER BACKGROUND JOB != DANTE DURABLE RUN
```

Execution modes:

```text
INLINE
BOUNDED ASYNC
ELIGIBLE PROVIDER BACKGROUND
CLASS-B DURABLE
```

Provider background work is permitted only when its storage/retention/data feature mode is currently eligible.

A Class-B DANTE workflow may orchestrate a provider background job by storing only bounded technical locators when justified, then polling/resuming/reconciling rather than blindly replaying after crash.

---

# 22. Class-A and Class-B

Accepted project decision remains:

```text
Class A
PostgreSQL transactional outbox + bounded worker

Class B
Restate selected / dormant until first real qualifying Class-B workflow
```

```text
BACKGROUND CAPABILITY != DURABILITY SEMANTICS
```

Provider background APIs do not reopen this architecture decision.

Restate activation remains trigger-based and still requires applicable privacy/recovery/direct-proof obligations.

---

# 23. Attached vs detached child work

Independent validation found another necessary distinction:

```text
ATTACHED CHILD WORK != DETACHED CHILD WORK
```

Attached child work may inherit parent cancellation/lifecycle semantics.

Detached/one-way/delayed work can outlive its initiator and therefore must be explicit, with clear lifecycle owner, purpose, current eligibility and reconciliation responsibility.

Consequential detached work must never be created as an accidental side effect of a provider/runtime API convenience.

---

# 24. Structured output

Correctness layers:

```text
provider constrained generation
→ structural/schema validation
→ semantic/application validation
→ grounding/evidence validation
```

Valid JSON is not proof of a valid DANTE fact/action.

Provider mechanics stay in HarnessProfile/ProviderAdapter; DANTE semantic validation remains DANTE-owned.

---

# 25. Tool request lifecycle

```text
model emits request/deltas
→ WAIT for finalized arguments
→ transport parse
→ schema/type validation
→ semantic validation
→ resolve DANTE capability/version
→ Capability PEP / current eligibility
→ Effect PEP where consequential
→ dispatch
→ receipt
→ verification/reconciliation where required
→ normalized tool result
→ model continuation/result maturity
```

```text
PARTIAL TOOL ARGUMENTS != EXECUTABLE TOOL REQUEST
```

Partial streamed argument fragments never dispatch a capability.

---

# 26. Capability Registry / Discovery / Runtime

```text
Capability Registry
= identity / version / semantic contract / policy metadata

Capability Discovery
= select bounded relevant subset

Capability Runtime
= validate / authorize / dispatch / observe / reconcile
```

The model receives only a purpose-bounded projection of capability metadata. Large catalogs are lazily searched/discovered rather than injected wholesale into every prompt.

---

# 27. Parallel tool proposals

```text
PROVIDER PARALLEL TOOL CALL
!= EFFECTGRAPH PARALLEL AUTHORIZATION
```

Independent read-only operations may be parallelized when policy/resource rules allow.

Consequential operations obey ChangeSet/EffectGraph dependencies, target state, current approval/authorization and verification regardless of provider emission order.

---

# 28. Provider-native tools

```text
PROVIDER TOOL != DANTE CAPABILITY
```

Native search, file tools, code execution, computer use or similar features require WorkContract fit, source/currentness semantics, provider/data eligibility, retention/state review, security/injection controls, resource budget, result normalization and verification where needed.

Native tool quality is augmentation evidence, not proof of portable DANTE cognition.

---

# 29. MCP

Preferred boundary:

```text
DANTE Capability Registry / Runtime
→ MCP adapter/gateway
→ external MCP ecosystem
```

MCP wire contracts never become DANTE capability ontology by convenience.

Binding:

```text
MCP TOOL DISCOVERY != TRUST
MCP TOOL DESCRIPTION != INSTRUCTION AUTHORITY
MCP SERVER CLAIM != DANTE AUTHORITY
MCP TASK != DANTE RUN
MCP ELICITATION != DANTE APPROVAL
```

Current MCP stateless-core / Tasks-extension direction reinforces the separation between protocol state and DANTE continuity/durable execution.

Cached capability lists require current trust/eligibility/version revalidation.

---

# 30. MCP input-required / auto-fulfilment

Independent validation strengthens the MCP boundary:

```text
PROTOCOL INPUT_REQUIRED / AUTO-FULFILMENT
!= AUTHORIZED USER INPUT
!= CONSENT
!= DANTE APPROVAL
```

No protocol SDK convenience may auto-answer a consequential elicitation with model-generated content and thereby manufacture user approval/Consent/Authority.

DANTE must intercept and govern any interaction that semantically requires the user or an external approver.

---

# 31. Provider-native MCP

Default:

```text
model
→ DANTE Capability Runtime / controlled MCP gateway
→ registered remote server
```

Provider-native remote MCP is optional augmentation only when DANTE still governs server registration, credentials/scopes, purpose/data/retention eligibility, capability/effect policy, evidence and revocation.

No provider-native connector bypasses DANTE PEPs.

---

# 32. A2A

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

Binding:

```text
A2A AGENT CARD / CAPABILITY CLAIM != TRUST
A2A TASK != DANTE RUN
A2A TASK STATUS != DANTE CANONICAL STATE
A2A AUTHENTICATION != DANTE AUTHORITY
```

DANTE does not decompose itself into permanent Calendar/Goal/Memory agents merely because an inter-agent protocol exists.

---

# 33. Late remote callbacks and task updates

Independent validation adds:

```text
REMOTE CALLBACK / TASK UPDATE
!= CURRENT DANTE RUN ELIGIBILITY
```

A late provider/MCP/A2A/background callback must be correlated to the original bounded work and then checked against current:

```text
Run lifecycle
supersession
Actor / represented-party / delegation
purpose/eligibility
expected target/material state
applicability
```

It may require verification/reconciliation. A remote `completed` status does not automatically mutate DANTE canonical state or resurrect superseded work.

---

# 34. Delegated identity / confused deputy

Runtime preserves enough context to distinguish:

```text
technical Principal
initiating Actor when applicable
represented party
external client/application
external agent identity
delegation basis/scopes
purpose
recipient
```

Authentication of an external agent does not grant full Authority of the represented human.

DANTE credentials are never blindly forwarded downstream.

---

# 35. Execution Environment

Activated only where a real execution surface is needed, such as generated code, browser/computer automation, repository/file manipulation, complex artifact transformation or untrusted tooling.

Ordinary conversation/reasoning does not require a sandbox.

Candidate manifest dimensions remain:

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

# 36. Provider-hosted execution

```text
PROVIDER-HOSTED EXECUTION != DANTE Execution Environment
```

Provider-hosted code/computer environments may be useful for eligible bounded computation or file analysis but do not silently receive broad DANTE/database/service secrets.

Privileged operations go through DANTE-controlled typed capability/credential brokerage.

---

# 37. Isolation and credential/egress broker

Technology remains trigger/evidence-driven:

```text
T0 trusted deterministic compute
T1 WASM/WASI where workload fits
T2 hardened container/syscall-isolated execution
T3 microVM/VM when stronger arbitrary-code isolation is required
```

Preferred privileged path:

```text
isolated environment
(no broad high-value credentials)
→ typed capability request
→ trusted broker / Capability Runtime
   ├ identity/delegation
   ├ current policy
   ├ scoped credential acquisition
   ├ target restrictions
   ├ egress restrictions
   └ evidence
→ DANTE / external system
```

Deny-by-default or capability-bounded network egress is preferred for untrusted execution where workload compatibility permits.

No sandbox product is selected by AI-04B.

---

# 38. Browser/computer-use hierarchy

Prefer the least fragile interface that expresses the required operation:

```text
1 DANTE/native semantic capability
2 external application/provider API
3 accessibility/DOM/OS semantic automation
4 visual/pixel computer use
```

Moving downward generally increases fragility, latency, security surface and verification burden.

Computer use remains trigger-gated.

---

# 39. Multi-agent topology

Default:

```text
one logical DANTE orchestration responsibility
+ deterministic tools
+ selective parallel workers where evidence justifies them
```

Multi-agent decomposition requires real independent subproblems, isolation/specialization/latency/scale value.

Parallel agents do not acquire independent Authority by existing.

No permanent domain-agent taxonomy is accepted.

---

# 40. Entitlement / ResourceBudget integration

```text
WorkContract
+ ConsequenceProfile
+ EntitlementProfile
+ ResourceBudget
+ required quality floor
+ provider/data eligibility
→ qualified execution routes
```

```text
ENTITLEMENT AT RUN START != PERPETUAL ENTITLEMENT
```

Upgrade/downgrade/quota changes can govern future optional work but cannot erase effect, verification or reconciliation obligations already created.

---

# 41. Budget admission and metering

Resource governance includes more than model tokens:

```text
model calls/tokens/money
native tools/search
external calls
DB work where meaningful
sandbox CPU/RAM/disk
network egress
parallel workers
active compute
```

Independent validation adds:

```text
BUDGET ADMISSION
!= FINAL METERED COST
!= GUARANTEED IMMEDIATE PROVIDER STOP
```

A provider may consume additional billable work between a local budget decision and actual cancellation/quiescence; final usage can arrive after execution.

AI-04C owns concrete reservation/settlement/overshoot/rate-limit mechanics. AI-04B only binds the semantic requirement that quota exhaustion must not be treated as proof that external work stopped or that unresolved consequences disappeared.

---

# 42. Frozen configuration vs current authorization

Stable configuration references are required for reproducibility, but independent validation found a critical distinction:

```text
FROZEN EXECUTION CONFIGURATION
!= PERPETUAL CURRENT AUTHORIZATION
```

A Run may record stable references to model target, HarnessProfile, routing/capability/security policy versions and environment specification.

Consequential boundaries still re-evaluate current Authority/AuthZ/Consent/provider eligibility/target MaterialState/entitlement where required by accepted DANTE semantics.

Reproducibility and current authorization are complementary responsibilities, not alternatives.

---

# 43. Provider-state revocation and deletion

Provider deletion can be asynchronous or unavailable for a time.

DANTE suppression/revocation must therefore take effect locally before physical external deletion is confirmed:

```text
DANTE forget/revoke/suppress
→ immediately mark provider continuation/cache/background state INELIGIBLE FOR REUSE
→ request provider deletion/cancellation where supported
→ track/reconcile external purge/expiry as needed
```

Binding:

```text
PHYSICALLY STILL PRESENT AT PROVIDER
!= CURRENTLY ELIGIBLE FOR DANTE REUSE
```

This extends AI-03 anti-resurrection/source-lifecycle rules into runtime provider state.

---

# 44. Operational evidence boundary

AI-04B requires enough runtime evidence for later AI-04C observability/audit/control-plane design to distinguish at least:

```text
Run identity
ModelInvocation identity
ProviderAttempt + binding + feature mode
routing reason/version
provider result/error/cancellation state
usage/cost evidence
capability/tool requests
DANTE semantic idempotency identity
retry/failover/reconnect events
provider continuation/background locator refs
late callback/task correlation
verification/effect/reconciliation refs
publication sequencing refs where needed
```

This does not choose physical evidence storage.

```text
TELEMETRY != AUDIT != CANONICAL DOMAIN TRUTH
```

---

# 45. Official-source runtime evidence posture

AI-04B used current provider/protocol documentation only to validate runtime boundary assumptions, never to select a vendor.

Evidence checked during the candidate and independent pass included materially different behavior around:

```text
provider response/background/cancellation/replay
partial streamed tool/function arguments
provider continuation IDs and interaction-scoped settings
provider feature-specific storage/retention eligibility
MCP stateless core / Tasks / input-required semantics
A2A independent task lifecycle
Restate cancellation propagation / detached work behavior
```

Provider/protocol facts are time-sensitive and MUST be rechecked immediately before implementation/qualification.

---

# 46. First destructive kill-test record

The first candidate was attacked with compound cases including:

```text
client disconnect during stream
STOP while provider call remains active
STOP after external effect dispatch
partial streamed tool arguments
parallel read + consequential write calls
provider rate limit / overload / outage
provider refusal + alternate provider
outcome-unknown retry
provider background + process crash
provider background + deletion/revocation
provider storage on no-retention workload
commercial downgrade/quota exhaustion mid-run
provider continuation after Actor switch
MCP catalog/cache/trust drift
malicious MCP descriptions
MCP elicitation mistaken for approval
provider-native MCP broad credentials
A2A authority/capability overclaim
provider-hosted execution requesting DANTE secrets
routing requiring full private context
hedged multi-provider execution
stream replay duplicating tool/effect
provider-side fallback
budget exhaustion while effect outcome UNKNOWN
```

Result:

```text
FIRST CANDIDATE → FAIL
RT-01..RT-20 ADDED
FIRST COMPOUND RETEST → PASS CANDIDATE
```

---

# 47. Fresh independent validation record

A fresh review was then performed **without assuming RT-01..RT-20 were sufficient**.

New compound failures found:

```text
cancel requested but provider/runtime still running
provider continuation reused while tools/system/HarnessProfile changed
provider generally eligible but specific stored/background/native mode ineligible
DANTE forget while provider physical state remains present
retry/failover changes provider call ID for same semantic effect
frozen Run configuration mistakenly treated as perpetual authorization
recipient stream publishes bytes before final disclosure maturity
late MCP/A2A/provider callback arrives after cancellation/supersession
one-way/detached child survives parent lifecycle unexpectedly
quota admission assumed to equal exact final bill/instant stop
MCP input-required/SDK auto-fulfilment manufactures apparent user input/approval
```

Result:

```text
FRESH INDEPENDENT VALIDATION → FAIL
11 NEW HARDENINGS REQUIRED
RT-21..RT-31 ADDED
```

No Domain/Logical/Physical/PostgreSQL reopen was required.

---

# 48. Final AI-04B invariants — RT-01..RT-31

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
RT-21  CANCELLATION REQUESTED != CANCELLATION CONFIRMED != EXECUTION QUIESCED.
RT-22  PROVIDER CONTINUATION HANDLE != HARNESS / POLICY / TOOL / CAPABILITY CONTINUITY.
RT-23  PROVIDER/BINDING QUALIFICATION MUST INCLUDE MATERIAL INVOCATION FEATURE MODE.
RT-24  LOCAL DANTE REVOCATION/SUPPRESSION TAKES EFFECT BEFORE EXTERNAL DELETION CONFIRMATION.
RT-25  PROVIDER TOOL/CALL/RESPONSE ID != DANTE CAPABILITY/EFFECT IDEMPOTENCY IDENTITY.
RT-26  FROZEN EXECUTION CONFIGURATION != PERPETUAL CURRENT AUTHORIZATION.
RT-27  PUBLISHED DELTA IS AN EXTERNALIZATION; DISCLOSURE/MATURITY PRECEDES IRREVERSIBLE PUBLICATION.
RT-28  REMOTE CALLBACK / TASK UPDATE != CURRENT DANTE RUN ELIGIBILITY.
RT-29  ATTACHED CHILD WORK != DETACHED CHILD WORK.
RT-30  BUDGET ADMISSION != FINAL METERED COST != GUARANTEED IMMEDIATE PROVIDER STOP.
RT-31  PROTOCOL INPUT_REQUIRED / AUTO-FULFILMENT != AUTHORIZED USER INPUT / CONSENT / DANTE APPROVAL.
```

---

# 49. Final compound retest

The complete runtime candidate with `RT-01..RT-31` was retested against both the original and fresh-independent pressure sets:

```text
stream reconnect / replay / duplicate-effect prevention
cancel requested vs confirmed vs late provider events
cancel + supersession + outcome-unknown reconciliation
failover after partial provider/tool state
semantic idempotency across provider attempts
provider continuation after Harness/capability/policy change
provider background + crash + deletion/revocation
feature-mode retention/storage restrictions
commercial downgrade/quota exhaustion mid-effect
budget overshoot after admission/cancel
MCP catalog/cache/trust drift
MCP input-required / auto-fulfilment vs DANTE approval
late MCP/A2A/background callbacks
A2A delegation / confused deputy
provider-native tools + prompt injection + egress
provider-hosted execution + credential boundary
attached vs detached child work
multi-agent parallelism + Authority
current authorization vs frozen reproducibility config
recipient publication irreversibility
retry/idempotency/reconciliation interaction
```

Final architecture result:

```text
FINAL COMPOUND RETEST → PASS
STRUCTURAL CONTRADICTION REMAINING IN AI-04B → NONE FOUND
```

This is an **architecture closure**, not implementation or direct-provider PASS.

---

# 50. Decisions intentionally still open

```text
concrete provider/model set
provider SDK choice
exact ModelTarget vocabulary
exact routing algorithm/fallback ordering
exact normalized runtime event/error schemas
retry/backoff numeric limits
exact client-edge SSE/WebSocket/etc. transport
voice/realtime transport
provider-background feature activation
Restate activation for first AI Class-B consumer
MCP client/server implementation
provider-native MCP activation
A2A implementation
browser/computer-use implementation
Execution Environment technology
WASM/gVisor/container/microVM product selection
credential broker implementation technology
physical Run/Invocation/Attempt/evidence storage
concrete budget reservation/settlement mechanics
commercial tier names/prices/quotas
```

These are downstream AI-04C, direct-evidence or AI-05 implementation-blueprint decisions.

---

# 51. Explicit non-claims

```text
AI-04 CLOSED                         NO
AI-04B CLOSED                        YES / STRUCTURALLY ACCEPTED
AI-04B FINAL INDEPENDENT PASS         YES / ARCHITECTURE LEVEL
DIRECT PROVIDER EVAL PASS            NO
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

# 52. Exact next action

```text
AI-04C — SECURITY / PRIVACY / CONTROL PLANE / OPERATIONS ARCHITECTURE
```

AI-04C must consume — not reopen casually — `RT-01..RT-31` while resolving:

```text
provider/data/feature-mode eligibility
credential and workload identity
secret brokerage and key lifecycle
information-flow / prompt-injection containment
control-plane registry/version/rollout ownership
commercial entitlement + budget reservation/settlement
rate limits / backpressure / fairness
observability vs audit vs eval data
privacy-safe tracing/logging
provider incident/degraded mode
release/shadow/canary/rollback
configuration promotion / emergency kill switches
runtime evidence retention
security/reliability SLOs
operational recovery and reconciliation
```

Direct provider/model eval remains activation-on-need when a concrete production choice is blocked on evidence.

No provider/model/API key is required to begin AI-04C architecture work.