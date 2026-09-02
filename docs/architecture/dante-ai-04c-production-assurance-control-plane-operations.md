# DANTE AI-04C — Production Assurance / Security / Privacy / Control Plane / Operations

- **Status:** CANDIDATE / STATE-OF-THE-ART RESEARCH MATERIALIZED / FIRST DESTRUCTIVE KILL-TEST HARDENED / INDEPENDENT VALIDATION NEXT / NOT CLOSED
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-04 — Productionization Architecture
- **Sub-phase:** AI-04C — Production Assurance / Security / Privacy / Control Plane / Operations
- **PRE-SCOPE:** `c89f751de9b4190d47eb9c1230facb02a0f009ba`
- **Upstream:** AI-02.1 CLOSED / AI-03 CLOSED / AI-04A MATERIALIZED / AI-04B CLOSED RT-01..RT-31
- **Provider/model selection:** OPEN / EVIDENCE-DRIVEN
- **Commercial package selection:** OPEN
- **Implementation claim:** NONE
- **Database change:** NONE

This document defines the first AI-04C production-assurance candidate for DANTE. It consumes the accepted semantic, context, persistence and runtime boundaries and defines how production AI configuration, provider/data eligibility, security controls, credentials, observability, budgets, rollout and incidents are governed.

It is architecture and operating semantics, not implementation code, cloud-product selection or a claim that production controls are already deployed.

---

# 1. Objective

AI-04C must make DANTE operable as a public, multi-user AI product without creating a second authority model, a provider-shaped control plane, hidden cost failure modes, unsafe rollout behavior or privacy-hostile observability.

The target is:

```text
accepted DANTE semantics
+ provider/model replaceability
+ current authorization and data eligibility
+ versioned control-plane configuration
+ enforceable runtime policy
+ least-privilege credentials
+ privacy-safe evidence
+ bounded resource economics
+ SRE-grade overload/failure behavior
+ progressive rollout / rollback
+ incident/revocation/reconciliation capability
```

Maximum production quality does not mean copying hyperscaler infrastructure. DANTE should adopt the strongest reusable principles and implement only the machinery justified by its scale and activated workload.

---

# 2. Binding upstream authority

AI-04C inherits without weakening:

```text
PostgreSQL = sole canonical persistence/material-history authority
MODEL OUTPUT != PUBLISHABLE OUTPUT
MODEL CAPABILITY != AUTHORITY
DISPLAY NAME != EFFECT TARGET
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
CANCEL RUN != UNDO ALREADY-DISPATCHED EFFECTS
Context != Retrieval != Memory
processing eligibility != retention eligibility != future-reuse eligibility
provider state != canonical DANTE state
DEFAULT NONCANONICAL PERSISTENCE = NO
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
FEATURE AVAILABLE != FEATURE ELIGIBLE
PROVIDER FAILOVER != BLIND REQUEST REPLAY
COMMERCIAL SUBSCRIPTION / SERVICE TIER != DANTE DOMAIN Plan
COMMERCIAL TIER != MODEL / PROVIDER / DEPLOYMENT
semantic obligation != technical execution/audit evidence
```

AI-04B RT-01..RT-31 remain binding. AI-04C may harden operational enforcement but does not silently reinterpret those runtime semantics.

---

# 3. What AI-04C must not become

Rejected shapes:

```text
one mega AI gateway that becomes semantic authority
one admin JSON blob edited directly in production
provider SDK configuration scattered through feature code
commercial plan hardcoded to one model/provider
full prompt/response logs by default
model-generated code holding broad service credentials
provider health alone defining DANTE health
retry at every layer
shadow traffic treated as free/non-disclosure
feature flag == authorization
security guardrail == Authority
provider delete request == immediate physical purge proof
```

AI-04C defines control-plane responsibilities, not a requirement for one additional microservice per concern.

---

# 4. State-of-the-art evidence method

This pass uses current public documentation to identify patterns proven useful by large AI/application platforms. The evidence is classified as:

```text
VERIFIED PUBLIC BEHAVIOR
explicitly documented behavior of a named platform

DANTE ARCHITECTURAL INFERENCE
a reusable principle inferred from one or more documented patterns

DANTE DECISION
an architecture rule accepted for this candidate
```

A public vendor pattern is not automatically a DANTE requirement. A large vendor may operate at a scale, compliance scope or infrastructure budget that DANTE does not need.

Provider/platform facts are time-sensitive and must be rechecked before implementation or qualification.

---

# 5. External pattern: reuse the application's permission model

Verified public patterns:

- Microsoft 365 Copilot documents that existing identity, permissions, sensitivity labels and retention policies apply to Copilot; Copilot does not grant new source permissions.
- Notion Enterprise Search documents permission checks at query time in addition to indexing/synchronization behavior.
- GitHub Copilot exposes enterprise/organization policy controls for AI features and models rather than giving every AI surface unconditional access.

DANTE inference:

```text
AI SECURITY MODEL
!= PARALLEL APPLICATION AUTHORIZATION MODEL
```

DANTE decision:

```text
existing Authority / AuthZ / Consent / Visibility / purpose rules
→ consumed by AI policy enforcement
→ rechecked at material boundaries
```

The AI layer may add stricter eligibility rules; it may not widen source or effect permissions.

---

# 6. External pattern: query-time eligibility beats index-time trust

Notion publicly documents query-time permission checking and that deleted source content becomes unsearchable before physical derivative deletion necessarily completes.

DANTE inference:

```text
INDEXED / CACHED / EMBEDDED
!= CURRENTLY ELIGIBLE TO SERVE
```

DANTE decision:

```text
current serving eligibility
must be checked independently of derivative physical presence
```

This directly preserves AI-03 source-lifecycle/anti-resurrection doctrine.

---

# 7. External pattern: AI features inherit existing data protection where possible

Microsoft 365 Copilot documents use of existing sensitivity labels, encryption rights, retention and audit/compliance controls. Slack documents multilayer AI guardrails on top of underlying model protections. Salesforce documents a Trust Layer with grounding, sensitive-data masking, toxicity checks, audit/feedback and provider zero-retention agreements.

DANTE inference:

```text
AI-specific controls should compose with application security,
not replace it.
```

DANTE decision:

```text
DANTE security/privacy truth remains application-owned;
provider/cloud guardrails are adapters/signals/enforcement helpers.
```

---

# 8. External pattern: control-plane policy is distinct from runtime traffic

GitHub Copilot documents organization/enterprise AI controls for feature/model access and audit of policy changes. Azure AI gateway patterns expose centralized policy, identity, rate-limit and backend governance independently of application feature semantics.

DANTE inference:

```text
CONTROL PLANE
!= RUNTIME DATA PLANE
```

This is a responsibility separation, not necessarily a service boundary.

---

# 9. Candidate control-plane / data-plane shape

```text
                 DANTE AI CONTROL PLANE
┌────────────────────────────────────────────────────────┐
│ Provider / Model Qualification                         │
│ Provider + Feature-Mode Eligibility                    │
│ HarnessProfile Registry                                │
│ Capability / Effect Policy Configuration               │
│ Security / Guard Profiles                              │
│ Routing Policy                                         │
│ Commercial Entitlement / Budget Policy                 │
│ Environment / Egress Policy                            │
│ Rollout / Canary / Kill-Switch Policy                  │
│ Requalification / Incident State                       │
└──────────────────────────┬─────────────────────────────┘
                           │ versioned approved config
                           ▼
                    RUNTIME DATA PLANE
┌────────────────────────────────────────────────────────┐
│ admission                                               │
│ current Actor/Authority/Consent/Visibility              │
│ current provider/data/feature-mode eligibility          │
│ resource reservation                                   │
│ Context / Egress PEP                                    │
│ Model Access Runtime                                    │
│ Capability / Effect PEP                                 │
│ Verification / Reconciliation                           │
│ Disclosure / Safe Publication                          │
│ usage settlement                                       │
└────────────────────────────────────────────────────────┘
```

The control plane configures what may be attempted. Runtime enforcement remains necessary because authorization, data, provider health, entitlements and state can change after configuration publication.

---

# 10. Qualification, eligibility, availability, entitlement

Core distinction:

```text
QUALIFIED
candidate passed applicable DANTE evidence/eval requirements

ELIGIBLE
candidate may process this WorkContract/data/purpose now

AVAILABLE
candidate is operationally usable now

ENTITLED
current account/user/service tier may consume the resource/capability

ROLLOUT-ACTIVE
candidate is enabled for this environment/cohort according to approved rollout
```

Routing eligibility requires intersection, not substitution:

```text
ROUTABLE
=
QUALIFIED
∩ ELIGIBLE
∩ AVAILABLE
∩ ENTITLED
∩ ROLLOUT-ACTIVE
```

A failure in one dimension is not compensated by another.

---

# 11. Provider feature-mode qualification

AI-04B already established that provider/binding qualification includes material invocation feature mode.

AI-04C makes this operational.

A qualification/eligibility profile may need to distinguish:

```text
ordinary inference
stored response/conversation mode
provider background mode
native file storage
prompt cache
native search
native MCP connector
provider-hosted code/computer environment
regional/global routing mode
batch mode
```

Because retention, data path, regional processing, supported controls or third-party exposure may differ materially.

```text
PROVIDER QUALIFIED
!= EVERY PROVIDER FEATURE QUALIFIED
```

---

# 12. New model/provider/feature activation default

Large platforms increasingly expose model/feature policy controls rather than making every newly available capability automatically usable.

DANTE candidate lifecycle:

```text
DISCOVERED
→ REGISTERED
→ EVIDENCE_PENDING
→ QUALIFIED
→ ROLLOUT_READY
→ CANARY/ACTIVE
→ DRAINING
→ RETIRED

material risk event
→ SUSPENDED / EMERGENCY_DISABLED
```

Default for a materially new provider/model/feature mode:

```text
NOT ACTIVE
```

Discovery from a provider API or catalog does not activate it.

---

# 13. Immutable config revisions and active pointers

Production AI behavior can change through configuration without application code changes.

Therefore DANTE should separate:

```text
immutable/versioned configuration revision
!= active environment/cohort pointer
```

Configuration subject examples:

```text
ProviderBinding
HarnessProfile
RoutingPolicy
GuardProfile
Capability projection/version
EntitlementProfile
BudgetPolicy
EnvironmentPolicy
RolloutPolicy
```

The exact physical representation remains AI-05/implementation work.

Required properties:

```text
stable revision identity
created/approved metadata
reason/change description
activation state
rollback target where relevant
source evidence/requalification link
```

---

# 14. Control-plane write privilege

Changing AI control-plane configuration can redirect sensitive data, change model behavior, alter capability access, widen egress or disable safety controls.

Therefore:

```text
CAN EDIT AI CONTROL PLANE
= PRIVILEGED SECURITY CAPABILITY
```

Control-plane writes need least privilege and auditability.

For risk-sensitive changes, policy may require review/approval before activation.

Examples:

```text
provider endpoint / region
credential ref
retention/feature mode
new MCP server
new consequential capability
security guard profile
routing policy
commercial/budget policy
emergency override
```

No exact human-approval workflow is selected yet.

---

# 15. Control-plane availability and stale configuration

Control-plane outage must not mean:

```text
cannot load policy
→ allow everything
```

Preferred semantics:

```text
runtime uses last-known approved immutable configuration
+ bounded freshness/expiry semantics where needed
+ local emergency deny/suppress capability
```

If the current requirement cannot be proven, fail/degrade safely.

A stale control-plane revision must not silently restore revoked provider/data/capability eligibility.

---

# 16. Emergency controls

DANTE requires emergency ability to prevent new exposure/work when a provider, model, feature, capability, endpoint or security component becomes unsafe.

Candidate scopes:

```text
global AI admission
provider
ProviderBinding
model/version
feature mode
capability/effect family
MCP/A2A integration
Execution Environment class
commercial optional workload
```

But:

```text
KILL NEW WORK
!= ABANDON IN-FLIGHT RECONCILIATION
```

Emergency controls must preserve enough protected execution capacity to:

```text
reconcile outcome-unknown effects
process late receipts/callbacks
revoke/suppress provider state
complete security cleanup
record required audit evidence
```

---

# 17. Layered security / information-flow path

Candidate flow:

```text
USER / EXTERNAL INPUT
→ abuse/request validation
→ instruction/source lineage
→ Context acquisition + current access eligibility
→ prompt/retrieval/tool-injection controls
→ provider egress/data eligibility/minimization
→ MODEL / PROVIDER TOOL
→ finalized tool proposal
→ current Capability PEP
→ current Effect PEP
→ external execution
→ receipt/verification
→ output security/DLP/disclosure
→ Safe Publication
```

No single moderation or guardrail decision replaces the chain.

---

# 18. Guardrail engines are adapters, not Authority

Candidate external guardrail classes include provider moderation, cloud guardrail products, injection classifiers, DLP/malware/URL services and DANTE-owned deterministic checks.

Binding:

```text
GUARDRAIL RESULT
!= DANTE Authority
!= DANTE Source Standing
!= EFFECT AUTHORIZATION
```

A guardrail can contribute a signal or enforce a mandatory policy at an edge, but cannot invent Authority or override canonical state.

---

# 19. Guardrail services are governed data recipients

Sending content to a separate security service is still processing/disclosure to another component/provider.

Therefore:

```text
SECURITY SERVICE AVAILABLE
!= SECURITY SERVICE ELIGIBLE FOR THIS DATA
```

Eligibility considers:

```text
purpose
content class/sensitivity
region/residency
retention
processor/subprocessor path
contractual restrictions
source/use exclusions
```

Where external guardrail processing is ineligible, use an eligible local/provider-integrated/deterministic path or fail safely according to workload consequence.

---

# 20. Guardrail versioning

Google Model Armor publicly documents versioned filters and aliases such as Stable/Latest/Legacy, including automatic alias movement.

DANTE inference:

```text
GUARDRAIL ENGINE / MODEL / THRESHOLD CHANGE
CAN CHANGE PRODUCTION BEHAVIOR
```

Candidate:

```text
GuardProfile revision
→ explicit engine/version/alias posture
→ thresholds/modes
→ data-eligibility requirements
→ eval evidence
→ rollout state
```

A moving `Stable`/`Latest` alias is not equivalent to an immutable configuration revision.

Material security-filter changes require risk-proportionate requalification.

---

# 21. Prompt / retrieval / tool injection

DANTE already tracks instruction provenance from AI-03.

AI-04C operationalizes it:

```text
user instruction
system/developer instruction
DANTE policy
retrieved source content
web content
tool output
MCP description
external agent payload
```

must not collapse into one instruction authority class.

Security filtering may identify suspected injection, but lineage must survive normalization/summarization/transformation sufficiently for downstream policy.

```text
TRANSFORMED UNTRUSTED CONTENT
!= TRUSTED INSTRUCTION
```

---

# 22. Masking / redaction semantics

Salesforce and other enterprise AI platforms publicly use sensitive-data masking as one protection layer.

For DANTE:

```text
MASKED INPUT
!= SEMANTICALLY EQUIVALENT INPUT
```

Masking can break:

```text
target resolution
identity matching
date/amount semantics
cross-record joins
source citations
policy decisions
```

Therefore masking/redaction is workload-aware. If a required semantic distinction is removed, the runtime must not pretend the same quality/verification guarantee still holds.

---

# 23. Credentials and workload identity

Preferred production order:

```text
workload identity / federation / short-lived token
> scoped runtime secret from secret manager
> long-lived static key only where provider requires it
```

Never embed raw secrets in:

```text
feature code
model context
tool schema
telemetry
sandbox image
provider continuation state
client application
```

ProviderBinding should reference credential/auth policy, not store the raw secret value.

---

# 24. Credential-class separation

Binding:

```text
ADMIN CREDENTIAL
!= INFERENCE RUNTIME CREDENTIAL
!= DELEGATED USER CREDENTIAL
!= SANDBOX/EXECUTION CREDENTIAL
```

Examples:

```text
admin key capable of changing provider/project configuration
must not be the ordinary inference key

user OAuth delegation
must not become a general service credential

sandbox
must not receive database-owner or broad secret-manager credentials
```

Where providers require static keys, store/rotate/revoke them through trusted runtime secret handling and expose only to the provider adapter process boundary that needs them.

---

# 25. Secret broker posture

For generated/untrusted execution:

```text
Execution Environment
(no broad secrets)
→ typed capability request
→ trusted broker / Capability Runtime
→ current identity/delegation
→ policy
→ narrowly scoped credential or server-side action
→ target restriction
→ egress restriction
→ evidence
```

The exact KMS/secret-manager technology remains open.

---

# 26. Four evidence planes

DANTE must preserve four conceptually separate evidence/data planes:

```text
1. CANONICAL DOMAIN / APPLICATION DATA
   PostgreSQL truth/material history

2. AUDIT / EXECUTION EVIDENCE
   security-sensitive changes, approvals, effect receipts,
   consequential routing/effect/reconciliation evidence

3. OPERATIONAL TELEMETRY
   traces, metrics, latency, errors, usage, cost, queueing

4. EVAL EVIDENCE
   fixtures, candidate outputs, graders, benchmark artifacts
```

Binding:

```text
TELEMETRY != AUDIT != EVAL EVIDENCE != CANONICAL TRUTH
```

They may correlate by IDs, but one must not be used as a hidden substitute for another.

---

# 27. Privacy-safe observability

OpenTelemetry GenAI conventions publicly support model/token/latency metadata while prompt/response/tool content capture is opt-in and acknowledged as sensitive.

DANTE default telemetry should include metadata such as:

```text
Run / ModelInvocation / ProviderAttempt correlation
provider / binding / model / feature mode
routing revision/reason class
latency / TTFT / completion time
input/output/reasoning token counts where exposed
usage/cost estimate/settled cost class
retry/fallback/circuit state
capability/tool identity/version
outcome/refusal/error class
queue/concurrency/backpressure signals
```

Default should exclude raw:

```text
full ConsumerContext
full user prompt
system instructions
private source documents
full tool arguments/results
full generated response
secrets/tokens
```

Content capture, if ever activated for a bounded debugging/eval purpose, is a separately governed data flow with retention and recipient controls.

---

# 28. Audit posture

Audit evidence exists to answer security/accountability questions such as:

```text
who changed the active provider binding?
which config revision routed this consequential attempt?
who approved the risky policy change?
which effect was dispatched with which current authorization basis?
when was a provider/feature emergency-disabled?
was provider-state deletion/suppression requested and reconciled?
```

Audit must not depend solely on:

```text
sampled tracing
provider-side log retention
best-effort application debug logs
```

Exact audit retention/storage remains AI-05/implementation work.

---

# 29. Model/provider logging posture

Provider-native request logging can be useful but is not the only evidence source.

DANTE must classify separately:

```text
provider billing/usage logs
provider admin/audit logs
provider prompt/response logs
DANTE runtime telemetry
DANTE security/audit evidence
```

Provider logs can expire, be unavailable, or have different privacy/retention semantics.

```text
PROVIDER LOG EXISTS
!= DANTE MAY RELY ON IT AS SOLE AUDIT AUTHORITY
```

---

# 30. Commercial/service-tier control model

AI-04A established:

```text
COMMERCIAL SUBSCRIPTION / SERVICE TIER
!= DANTE DOMAIN Plan

COMMERCIAL TIER
!= MODEL / PROVIDER / DEPLOYMENT
```

AI-04C candidate resource chain:

```text
CommercialOffering / ServiceTier
→ EntitlementProfile
→ included capability/resource envelope
→ optional shared/purchased/overage pool where product permits
→ BudgetPolicy
→ runtime admission/reservation/settlement
```

No exact tier names, prices or quotas are selected.

---

# 31. Commercial credit, provider usage and cost are distinct

Binding:

```text
COMMERCIAL CREDIT
!= PROVIDER TOKEN
!= ACTUAL PROVIDER COST
```

A future product may expose user-friendly credits/usage units while providers bill in different token/tool/request/compute dimensions.

The mapping must be versioned and economically inspectable.

---

# 32. Admission, reservation and settlement

AI-04B RT-30 established that admission is not final cost.

AI-04C candidate:

```text
estimate bounded resource exposure
→ atomically reserve applicable budget envelope
→ execute
→ collect actual usage/cost evidence
→ settle actual usage
→ release unused reservation
→ record overshoot/unknown amount when exact settlement is delayed
```

Binding:

```text
ADMISSION ESTIMATE
!= RESERVED AMOUNT
!= SETTLED USAGE
```

For a promised hard financial cap, admission must account for a defensible upper bound. If only an estimate is possible, product semantics must call it a soft target/alert rather than a guaranteed hard cap.

---

# 33. Atomic shared-budget admission

Multiple Runs may compete for the same account/workspace/user budget.

Therefore reservation cannot be:

```text
read remaining = 10
Run A sees 10
Run B sees 10
A reserves 8
B reserves 8
```

Shared budget admission requires an atomic authority boundary.

The exact PostgreSQL/control-plane physical mechanism is intentionally not selected here.

This requirement does not imply a new database table during AI-04C.

---

# 34. Quota classes remain distinct

```text
COMMERCIAL QUOTA
!= ABUSE / FAIRNESS RATE LIMIT
!= PROVIDER QUOTA
!= PLATFORM CAPACITY
```

Candidate dimensions can include:

```text
platform-global capacity
workspace/account
group/service tier
user/Actor
ProviderBinding
ModelTarget
capability/tool
background work
sandbox
external downstream API
```

The V1 should implement only dimensions justified by actual product scope, while preserving the semantic distinction.

---

# 35. Protected reconciliation capacity

Commercial exhaustion cannot prevent DANTE from resolving consequential uncertainty it already created.

Protected capacity may be required for:

```text
outcome-unknown effect verification
late receipt/callback processing
compensation/reconciliation
provider-state revocation/deletion
security cleanup
required audit finalization
```

```text
USER HAS NO OPTIONAL AI BUDGET LEFT
!= DANTE MAY ABANDON SAFETY OBLIGATIONS
```

---

# 36. Retry ownership and retry budgets

Google SRE documents how layered retries can amplify failures and recommends bounded retries with exponential backoff/jitter and overload protection.

DANTE must avoid:

```text
provider SDK retries × gateway retries × runtime retries × durable workflow retries
```

without a shared policy/visibility boundary.

Candidate:

```text
one logical operation retry responsibility
→ bounded retry budget
→ reason-aware attempts
→ exponential backoff + jitter where appropriate
→ current deadline/budget/eligibility checks
```

Provider SDK automatic retries must be known/configured when material to semantics/cost.

---

# 37. Circuit breaker and provider health

A `ProviderBinding` can be qualified but temporarily unhealthy.

Operational health may include:

```text
latency
5xx/unavailable rate
rate-limit pressure
capacity/quota
invalid-output rate
provider status
cost anomaly
security incident state
```

Circuit-breaker/open state is operational evidence, not proof the provider is permanently unqualified.

Failover still requires alternate current eligibility and capacity.

---

# 38. Fallback capacity and cascading failure

Rejected:

```text
provider A fails
→ send 100% to B
→ B overloads
→ send 100% to C
```

Fallback policy considers:

```text
alternate binding health/capacity
rate limits
remaining budget
quality floor
provider/data eligibility
commercial entitlement
current rollout status
```

If no safe alternate exists, degrade/fail explicitly rather than cause a cascading outage or privacy regression.

---

# 39. Graceful degradation

Google SRE explicitly recommends intentional degraded modes and load shedding rather than letting overload destroy the service.

DANTE candidate degradation ladder:

```text
NORMAL
→ disable optional enrichment
→ reduce safe parallelism
→ use cheaper/faster qualified ModelTarget where quality floor permits
→ defer optional background work
→ deterministic/read-only capability mode where possible
→ safe unavailable / explicit deferral
```

Binding:

```text
DEGRADED PERFORMANCE / RESOURCE USE MAY BE ALLOWED
DEGRADED SAFETY / PRIVACY / AUTHORIZATION / RECONCILIATION IS NOT
```

Degraded paths must be exercised in tests/operations; a never-used emergency path is not trustworthy merely because it exists in documentation.

---

# 40. Queueing and backpressure

Unbounded queues hide overload and convert capacity problems into latency/memory incidents.

Candidate principles:

```text
bounded queue / admission
explicit deadlines
cancel obsolete work
fairness policy
priority only where product/obligation justifies it
backpressure before resource exhaustion
```

Commercial priority may affect service class, but must not starve reconciliation/security obligations.

---

# 41. SLOs from the DANTE user-safe outcome

Google SRE recommends SLOs measured from the user perspective rather than raw server health.

Candidate DANTE SLI/SLO families:

```text
INTERACTIVE ASSIST
 time to first SAFE useful output
 completion success/quality floor

READ / QUERY
 correct/current bounded result within latency target

GOVERNED EFFECT
 verified success OR explicit unresolved outcome within target

BACKGROUND
 completion/notification within declared service window

RECONCILIATION
 time from UNKNOWN → resolved/escalated
```

Provider uptime alone is not a DANTE SLO.

---

# 42. Error budgets and hard failures

Operational availability/latency errors may consume an SRE error budget.

But:

```text
privacy leak
unauthorized consequential effect
cross-actor disclosure
truth/safety hard failure
```

must not be normalized into:

```text
acceptable 0.1% error budget
```

For those classes DANTE uses zero-observed-failure qualification targets and security/quality incident handling if observed.

---

# 43. Release lifecycle for AI configuration

AI behavior can change via model, prompt/HarnessProfile, guardrail, tools and routing without application binary changes.

Candidate lifecycle:

```text
DRAFT
→ VALIDATED
→ APPROVED
→ SHADOW when eligible
→ CANARY
→ PROGRESSIVE
→ ACTIVE
→ DRAINING
→ RETIRED

material regression/security event
→ PAUSE / ROLLBACK CONFIG / EMERGENCY_DISABLE
```

Exact percentages and rollout vendor remain open.

---

# 44. Guarded rollout pattern

LaunchDarkly publicly documents guarded rollouts for AI configs/prompts/models and automated pause/rollback on metric regression.

DANTE inference:

```text
MODEL/HARNESS/ROUTING/GUARD CHANGE
SHOULD BE TREATED AS A RELEASE
```

Candidate rollout metrics include:

```text
hard-failure count
quality floor failures
invalid structured/tool outputs
refusal change
latency / TTFT
provider error rate
cost per successful task
tool/effect error rate
security-filter false positive/negative evidence where measurable
```

Automated rollback is allowed only for future configuration selection; it does not undo already-materialized external effects.

---

# 45. Shadow traffic is disclosure

Shadow comparison can duplicate private content to another model/provider.

Binding:

```text
SHADOW TRAFFIC
= REAL PROCESSING / DISCLOSURE
```

A shadow candidate must be independently eligible for the data/purpose/region/retention path.

For consequential workloads:

```text
SHADOW CANDIDATE
MUST NOT DISPATCH UNCONTROLLED EFFECTS
```

Prefer replay against governed synthetic/eval data when production shadow disclosure is unnecessary.

---

# 46. Canary continuity

A rollout change applies to routing/config selection for future material attempts according to defined semantics.

It must not silently mutate an in-flight ProviderAttempt.

A long Run may re-evaluate current authorization/eligibility for new work while retaining the exact configuration/evidence for already-executed attempts.

```text
NEW ACTIVE CONFIG
!= RETROACTIVE REWRITE OF PRIOR ATTEMPT
```

---

# 47. Configuration rollback vs effect rollback

Binding:

```text
ROLLBACK CONFIGURATION
→ affects future eligible work

!=
UNDO ALREADY-MATERIALIZED EFFECT
```

Existing external effects remain subject to normal verification/reconciliation/compensation semantics.

---

# 48. Feature-flag targeting privacy

Rollout targeting systems should receive only the minimum information needed to choose a configuration.

Do not send full prompts/private context merely to decide a feature flag or canary cohort.

Candidate targeting dimensions:

```text
environment
workspace/account pseudonymous ID where needed
service tier
workload/risk class
region
stable rollout bucket
```

Sensitive semantic content should not be used unless genuinely necessary and separately governed.

---

# 49. Requalification triggers

Material changes that may stale qualification include:

```text
model snapshot / moving alias
ProviderBinding endpoint/deployment/region
provider retention/data policy
provider/subprocessor path
feature mode
HarnessProfile
structured-output/tool semantics
guardrail engine/version/threshold
provider SDK behavior materially affecting retries/state
routing policy
critical capability contract
material price/tokenization behavior
security incident
residency commitment
```

Response is risk-proportionate:

```text
monitor only
partial requalification
shadow/canary
full relevant eval suite
emergency suspend
```

No universal full benchmark is required for every harmless metadata change.

---

# 50. Provider/subprocessor lifecycle

Provider eligibility is not permanent.

The control plane needs evidence sufficient to answer:

```text
which processor/provider path is used?
for what feature mode?
what retention/residency constraints apply?
what qualification evidence is current?
what material policy/processor change occurred?
```

A material provider/subprocessor/retention/residency change can make a previously qualified binding stale or ineligible until reviewed.

---

# 51. Feedback and model-improvement data

User feedback, product analytics, eval data and provider model-improvement sharing are separate purposes.

Binding:

```text
USER CLICKS THUMBS DOWN
!= AUTOMATIC CONSENT TO EXPORT FULL PRIVATE CONVERSATION
```

DANTE should default to minimal feedback metadata and require explicit, governed product decisions for sharing richer content with eval/model-improvement pipelines.

Provider training/feedback opt-in or opt-out settings are part of ProviderBinding/feature-mode governance when material.

---

# 52. Incident classes

Candidate incident categories:

```text
provider availability/capacity
provider security/privacy policy change
credential compromise
control-plane unauthorized change
prompt/retrieval/tool injection exploit
cross-actor disclosure
unauthorized effect
provider-state deletion/revocation failure
cost runaway / retry storm
observability/audit pipeline failure
bad rollout / quality regression
external tool/MCP/A2A compromise
```

Exact incident severity taxonomy remains operational implementation work.

---

# 53. Security incident response shape

For a provider/data-path security concern:

```text
detect / report
→ identify affected bindings/feature modes/cohorts
→ suppress new eligible use
→ preserve reconciliation/security cleanup path
→ rotate/revoke credentials if required
→ suppress provider-state reuse locally
→ request provider deletion/cancel where applicable
→ audit affected attempts/effects/disclosures
→ communicate/remediate according to product/legal obligations
→ requalify before reactivation
```

Do not wait for provider-side physical deletion to make DANTE state ineligible for reuse.

---

# 54. Audit/telemetry pipeline failure

Observability system outage should not automatically stop all low-risk AI work, but consequential evidence requirements may impose stricter behavior.

Candidate principle:

```text
TELEMETRY OPTIONALITY
CAN VARY BY WORKLOAD

REQUIRED CONSEQUENTAL AUDIT/EFFECT EVIDENCE
CANNOT BE SILENTLY DROPPED
```

If required evidence cannot be durably established, high-consequence work may need to fail closed/defer rather than execute unaudited.

Exact evidence durability belongs to AI-05/implementation design.

---

# 55. Recovery ordering

AI-03C established that provider/derived/runtime recovery cannot outrun canonical PostgreSQL readiness.

AI-04C adds operational ordering:

```text
canonical application recovery ready
→ current control-plane approved configuration available
→ credentials/identity healthy
→ provider eligibility/health revalidated
→ derived/provider continuation state reconsidered
→ optional traffic restored progressively
```

Do not replay historical provider work blindly after recovery.

Outcome-unknown consequential work receives reconciliation priority.

---

# 56. Multi-region / residency posture

DANTE does not select multi-region deployment here.

If a ProviderBinding or future cloud path spans regions, DANTE must distinguish:

```text
endpoint region
processing region/zone where known
data-at-rest location
provider global/geographic routing behavior
third-party tool/search egress
```

A region label on an endpoint alone does not prove every feature path is region-bound.

Exact production region policy remains open until provider/platform selection.

---

# 57. Large-platform patterns adopted vs rejected

Adopt as principles:

```text
reuse existing permissions
query-time eligibility
control-plane policy
versioned model/guard/config changes
least-privilege/workload identity
multilayer security
privacy-safe telemetry
separate audit
rate/admission controls
progressive rollout
SRE overload/degraded-mode discipline
provider/subprocessor requalification
```

Do not automatically copy:

```text
hyperscaler-scale AI gateway deployment
separate vector database because a large app uses one
one KMS hierarchy per customer by default
multi-region GPU fleets
many agent microservices
hosting every third-party model inside DANTE infrastructure
enterprise compliance machinery before product scope requires it
```

Architecture is principle-driven, scale-proportionate.

---

# 58. Current public evidence ledger — verified behavior

## Microsoft 365 Copilot

Public documentation states that Copilot respects existing identity/permissions, sensitivity labels and retention policies, and supports audit/compliance within Microsoft 365.

References:

- https://learn.microsoft.com/en-us/microsoft-365/copilot/enterprise-data-protection
- https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-architecture-data-protection-auditing

## Notion Enterprise Search

Public documentation states that connector search respects source permissions, permissions are checked at query time, deleted source content becomes unsearchable before derivative deletion necessarily completes, and connector/provider retention differs by plan/feature.

Reference:

- https://www.notion.com/help/enterprise-search-security-and-privacy-practices

## Slack AI

Public documentation describes multilayer guardrails including prompt-side safety, context engineering against prompt injection, URL filtering, output validation and content safety filters.

Reference:

- https://slack.com/help/articles/53359847722131-Guide-to-the-Slack-AI-Guardrails

## GitHub Copilot

Public documentation exposes enterprise/organization AI policies controlling feature/model availability and recommends audit monitoring to prevent policy drift.

Reference:

- https://docs.github.com/en/copilot/concepts/policies

## Salesforce Trust Layer

Public documentation describes grounding, sensitive-data masking, toxicity checks, audit/feedback and zero-data-retention agreements as layers around LLM use.

Reference:

- https://developer.salesforce.com/docs/ai/agentforce/guide/trust.html

## Azure AI Gateway / API Management

Public documentation describes token/request rate limits, quota controls and centralized policy enforcement; blocked requests can be stopped before backend invocation.

References:

- https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities
- https://learn.microsoft.com/it-it/azure/api-management/ai-gateway-govern-secure-assets

## Amazon Bedrock Guardrails

Public documentation shows IAM can explicitly deny model inference that does not include an approved guardrail identifier/version for supported APIs.

Reference:

- https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-permissions-id.html

## Google Model Armor

Public documentation exposes versioned filters and aliases such as Latest/Stable/Legacy, with `v3` promoted to Stable on 2026-08-31, illustrating that guard behavior itself is versioned production configuration.

References:

- https://docs.cloud.google.com/model-armor/release-notes
- https://docs.cloud.google.com/model-armor/set-filter-version

## OpenTelemetry GenAI

Public OpenTelemetry guidance exposes standardized GenAI metadata such as model, token usage and latency while noting that full prompt/response/tool content capture is opt-in and sensitive.

Reference:

- https://opentelemetry.io/blog/2026/genai-observability/

## Guarded rollout systems

LaunchDarkly publicly documents progressive/guarded rollouts for AI configs, prompts and models, metric monitoring and automated pause/rollback on regression.

References:

- https://launchdarkly.com/docs/home/agentcontrol/target
- https://launchdarkly.com/docs/home/releases/guarded-rollouts

## Google SRE

Public SRE guidance recommends user-centered SLOs, error budgets, bounded retries with backoff/jitter, intentional graceful degradation, load shedding and overload testing.

References:

- https://sre.google/sre-book/service-best-practices/
- https://sre.google/sre-book/addressing-cascading-failures/

---

# 59. First destructive AI-04C kill-test

The first production-assurance candidate was attacked with compound cases including:

```text
provider changes retention policy
provider introduces new subprocessor
new model appears behind moving alias
security guard Stable alias changes behavior
control-plane node serves stale configuration
unauthorized admin redirects ProviderBinding to unsafe endpoint
control-plane/identity editor can indirectly access privileged identity
control-plane store temporarily unavailable
guardrail service unavailable
guardrail service itself is data-ineligible
shadow traffic duplicates private content to another provider
shadow model attempts tool/effect execution
masking removes identity needed for correct target resolution
permission revoked while derivative remains physically present
OTel exporter captures ConsumerContext or secrets
provider-side logs expire before investigation
required audit sink unavailable during consequential effect
two concurrent Runs oversubscribe one shared budget
provider actual cost exceeds reservation
SDK + gateway + runtime + workflow retries multiply
primary provider outage floods fallback provider
commercial quota blocks outcome-unknown reconciliation
kill switch stops cleanup/revocation/reconciliation
feature-flag service receives private semantic content for targeting
canary changes provider while a Run remains active
configuration rollback treated as undo of completed effect
feedback event exports full private conversation
security incident requires immediate local provider-state suppression
all external model providers unavailable
provider endpoint region differs from actual feature processing path
```

The initial candidate **FAILED** until the PA hardenings below were made explicit.

---

# 60. AI-04C production-assurance invariants — PA-01..PA-38

```text
PA-01
APPLICATION/DANTE AUTHORITY REMAINS AUTHORITATIVE;
AI DOES NOT WIDEN SOURCE PERMISSIONS.

PA-02
QUALIFIED != ELIGIBLE != AVAILABLE != ENTITLED.

PA-03
ROUTABLE REQUIRES ALL APPLICABLE QUALIFICATION,
ELIGIBILITY, HEALTH, ENTITLEMENT AND ROLLOUT GATES.

PA-04
PROVIDER ELIGIBILITY INCLUDES MATERIAL FEATURE MODE,
RETENTION, RESIDENCY, PURPOSE AND PROCESSOR PATH.

PA-05
NEW MODEL / PROVIDER / MATERIAL FEATURE MODE
IS NOT ACTIVE BY DISCOVERY ALONE.

PA-06
CONTROL-PLANE CONFIGURATION IS VERSIONED;
ACTIVE POINTER != IMMUTABLE CONFIG REVISION.

PA-07
FROZEN CONFIGURATION != CURRENT AUTHORIZATION.

PA-08
CONTROL-PLANE WRITE AUTHORITY IS PRIVILEGED
SECURITY AUTHORITY AND MUST BE AUDITABLE.

PA-09
CONTROL-PLANE OUTAGE MUST NOT FALL BACK
TO UNBOUNDED ALLOW.

PA-10
EMERGENCY DISABLE OF NEW WORK
!= ABANDON IN-FLIGHT RECONCILIATION.

PA-11
MANDATORY PROVIDER / CAPABILITY / EFFECT /
EGRESS CONTROLS MUST NOT BE BYPASSABLE BY FEATURE CODE.

PA-12
GUARDRAIL RESULT != DANTE AUTHORITY.

PA-13
A SECURITY/GUARDRAIL SERVICE IS ITSELF
A GOVERNED DATA RECIPIENT.

PA-14
UNTRUSTED SOURCE / INSTRUCTION LINEAGE
MUST SURVIVE TRANSFORMATION.

PA-15
MASKING / REDACTION != SEMANTIC EQUIVALENCE.

PA-16
GUARD PROFILE VERSION / THRESHOLD /
ENGINE CHANGE REQUIRES CONTROLLED REQUALIFICATION.

PA-17
SECRETS != RUNTIME CONFIGURATION.

PA-18
ADMIN CREDENTIAL != INFERENCE CREDENTIAL
!= DELEGATED USER CREDENTIAL.

PA-19
WORKLOAD IDENTITY / SHORT-LIVED CREDENTIALS
ARE PREFERRED WHERE SUPPORTED.

PA-20
MODEL / SANDBOX DOES NOT RECEIVE
BROAD HIGH-VALUE CREDENTIALS.

PA-21
TELEMETRY != AUDIT != EVAL EVIDENCE
!= CANONICAL TRUTH.

PA-22
FULL PROMPT / RESPONSE / CONTEXT TELEMETRY
IS OFF BY DEFAULT.

PA-23
SECURITY / CONSEQUENTIAL AUDIT EVIDENCE
MUST NOT DEPEND SOLELY ON SAMPLED TELEMETRY
OR PROVIDER LOG RETENTION.

PA-24
COMMERCIAL CREDIT != PROVIDER TOKEN
!= ACTUAL PROVIDER COST.

PA-25
ADMISSION ESTIMATE != RESERVATION != SETTLEMENT.

PA-26
SHARED BUDGET ADMISSION MUST BE ATOMIC
AT ITS AUTHORITY BOUNDARY.

PA-27
COMMERCIAL QUOTA != ABUSE RATE LIMIT
!= PROVIDER QUOTA != PLATFORM CAPACITY.

PA-28
RETRY BUDGET MUST PREVENT
MULTIPLICATIVE HIDDEN RETRIES.

PA-29
RECONCILIATION / SAFETY-CRITICAL WORK
MUST NOT BE STARVED BY COMMERCIAL EXHAUSTION.

PA-30
GRACEFUL DEGRADATION MAY REDUCE RESOURCE COST
BUT NOT SAFETY / PRIVACY / SEMANTIC FLOORS.

PA-31
SHADOW TRAFFIC IS A REAL DATA DISCLOSURE
AND MUST BE INDEPENDENTLY ELIGIBLE.

PA-32
SHADOW/CANARY WORK MUST NOT CREATE
UNCONTROLLED CONSEQUENTIAL EFFECTS.

PA-33
ROLLBACK OF CONFIGURATION
!= ROLLBACK OF MATERIALIZED EFFECTS.

PA-34
SLOs MEASURE USER-SAFE DANTE OUTCOMES,
NOT RAW PROVIDER UPTIME.

PA-35
SECURITY/PRIVACY HARD FAILURE
IS NOT AN ORDINARY ERROR-BUDGET CONSUMPTION.

PA-36
PROVIDER / SUBPROCESSOR / RETENTION /
RESIDENCY MATERIAL CHANGE TRIGGERS REQUALIFICATION.

PA-37
FLAG / ROLLOUT TARGETING USES
MINIMUM NECESSARY NON-SENSITIVE CONTEXT.

PA-38
FEEDBACK / MODEL-IMPROVEMENT DATA SHARING
IS EXPLICITLY SEPARATE FROM NORMAL TELEMETRY/EVAL.
```

---

# 61. Compound retest after PA-01..PA-38

After incorporating PA-01..PA-38, the candidate survives the first compound production-assurance retest at the architecture level:

```text
stale control plane cannot widen access by default
provider/feature routing requires current eligibility intersection
new model/feature cannot auto-activate
control-plane change is attributable/versioned
kill switch preserves reconciliation path
guardrail cannot become Authority
guardrail data exposure is governed
moving guard/version aliases cannot silently redefine stable config
model/sandbox never inherits broad admin/runtime secrets
metadata telemetry can remain useful without full private content
required audit is separate from sampled traces
concurrent budget admission cannot intentionally oversubscribe by design
retry layers cannot independently multiply attempts
provider outage can degrade safely rather than cascade
commercial exhaustion cannot stop reconciliation
shadow traffic requires independent disclosure eligibility
rollout rollback changes future config, not historical effects
provider/subprocessor policy change stales applicable qualification
feedback cannot silently become training/eval export
```

Result:

```text
FIRST COMPOUND RETEST
→ PASS CANDIDATE
```

This is not AI-04C closure.

A fresh independent destructive validation must attempt to find contradictions not assumed by PA-01..PA-38.

---

# 62. Independent validation requirements

The independent AI-04C pass must pressure at least:

```text
control-plane stale/read-partition behavior
control-plane authorization escalation
configuration signing/integrity/tamper assumptions
kill-switch race with in-flight work
provider/data eligibility cache drift
provider processor/region change
credential rotation during active Run
secret-manager outage
security scanner false-positive/false-negative interaction
prompt-injection through transformed summaries/tool outputs
telemetry cardinality/cost explosion
telemetry exporter outage/backpressure
required audit durability failure
budget reservation leak after crashed Run
unknown provider billing settlement
shared-pool fairness/starvation
retry budget across provider SDK + gateway + DANTE + Restate
fallback capacity/circuit-breaker interaction
shadow/canary cohort privacy and effect isolation
bad automatic rollback decision
commercial upgrade/downgrade during reservation
all-provider outage / deterministic degraded mode
incident recovery and requalification
```

If a real structural contradiction appears, harden the smallest affected boundary and rerun the compound set.

---

# 63. Decisions intentionally still open

```text
concrete provider/model set
provider SDK choice
exact model snapshots/defaults
exact ModelTarget vocabulary
actual direct benchmark results
final eval runner
exact control-plane physical topology/storage
exact configuration schema/table/file representation
configuration signing technology
exact admin approval workflow
feature-flag/rollout vendor
AI gateway product selection
security/guardrail product selection
secret-manager/KMS product
cloud workload-identity implementation
exact commercial tier names/prices/quotas
billing/credit vendor
exact budget accounting persistence
exact atomic reservation mechanism
exact rate-limit algorithms/values
exact queue/fairness strategy
exact retry counts/backoff
exact circuit-breaker thresholds
exact SLO targets/error-budget windows
exact audit/evidence retention
exact telemetry backend fields/cardinality budgets
production regions/residency mappings
provider background/native tool activation
MCP/A2A activation
Execution Environment technology
Restate activation
R2 activation
pgvector/FTS activation
```

These are not required to accept the responsibility architecture candidate.

---

# 64. Explicit non-claims

```text
AI-04 CLOSED                           NO
AI-04C CLOSED                          NO
AI-04C FINAL INDEPENDENT PASS          NO
PROVIDER SELECTED                      NO
MODEL DEFAULT SELECTED                 NO
PROVIDER SDK SELECTED                  NO
CONTROL-PLANE IMPLEMENTED              NO
AI GATEWAY SELECTED/DEPLOYED           NO
GUARDRAIL PRODUCT SELECTED             NO
SECRET MANAGER/KMS SELECTED            NO
COMMERCIAL TIER NAMES/PRICES SET       NO
BILLING/CREDIT SYSTEM IMPLEMENTED      NO
PRODUCTION AI BACKEND IMPLEMENTED      NO
FRONTEND AI STREAMING IMPLEMENTED      NO
API CREDENTIALS USED                   NO
PAID MODEL API CALL EXECUTED           NO
POSTGRESQL/ALEMBIC CHANGED             NO
NEW AI TABLE/INDEX                     NO
PGVECTOR/ANN/FTS ACTIVATED             NO
RESTATE/R2 ACTIVATED                   NO
MCP/A2A ACTIVATED                      NO
EXECUTION ENVIRONMENT IMPLEMENTED      NO
SC/PSV DIRECT PROOFS EXECUTED          NO
AI-05 STARTED                          NO
```

---

# 65. Exact next action

```text
AI-04C — FRESH INDEPENDENT DESTRUCTIVE PRODUCTION-ASSURANCE VALIDATION
```

Required sequence:

```text
reconstruct candidate independently
→ attack control-plane/security/privacy/credentials/economics/ops
→ compare against PA-01..PA-38 only after attack generation
→ record any new failures
→ harden smallest affected boundary
→ rerun compound set
→ close AI-04C only if no structural contradiction remains
```

After AI-04C closure:

```text
AI-04 WHOLE-PHASE DESTRUCTIVE ACCEPTANCE
→ reconcile AI-04A + AI-04B + AI-04C
→ direct provider/model proof only where a concrete decision is blocked on evidence
→ AI-04 closure
→ AI-05 whole-system acceptance + implementation blueprint
```

No API key or provider selection is required for the independent architecture validation.