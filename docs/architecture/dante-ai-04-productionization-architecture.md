# DANTE AI-04 — Productionization Architecture

- **Status:** CANDIDATE / AI-04A MATERIALIZED / AI-04B CLOSED / AI-04C MATERIALIZED + INDEPENDENT VALIDATION CURRENT / NOT CLOSED
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-04 — Productionization Architecture
- **Current focus:** AI-04C — Fresh Independent Production-Assurance Validation
- **Upstream:** AI-02.1 CLOSED / AI-03 CLOSED
- **AI-03A:** C01..C33
- **AI-03B:** B01..B35
- **AI-03C:** MAT-01..MAT-15
- **AI-04A:** workload/eval/provider/economics + commercial entitlement boundary MATERIALIZED / direct provider evidence DEFERRED UNTIL DECISION-CRITICAL
- **AI-04B:** CLOSED / STRUCTURALLY ACCEPTED / RT-01..RT-31
- **AI-04C:** CANDIDATE MATERIALIZED / PA-01..PA-38 / FIRST COMPOUND RETEST PASS CANDIDATE / INDEPENDENT VALIDATION CURRENT
- **Provider/model selection:** OPEN / EVIDENCE-DRIVEN
- **Commercial tier/pricing selection:** OPEN
- **Implementation claim:** NONE
- **Database change:** NONE

This document is the durable master for AI-04 Productionization Architecture.

Detailed authority:

- `docs/architecture/dante-ai-04a-direct-eval-specification.md`
- `docs/architecture/dante-ai-04b-concrete-runtime-capability-architecture.md`
- `docs/architecture/dante-ai-04c-production-assurance-control-plane-operations.md`

AI-04 converts accepted DANTE semantics into production choices without allowing a provider, SDK, commercial package, control-plane product or cloud platform to redefine Domain/Logical/Physical/AI-02/AI-03 truth.

Current sequence:

```text
AI-04A — workload / eval / provider / economics
MATERIALIZED
→ direct provider/model evidence deferred until a concrete decision requires it

AI-04B — concrete runtime / capabilities
first destructive FAIL
→ RT-01..RT-20
→ PASS CANDIDATE
→ fresh independent FAIL
→ RT-21..RT-31
→ final compound retest PASS
→ CLOSED / STRUCTURALLY ACCEPTED

AI-04C — production assurance / security / privacy / control plane / operations
state-of-the-art research
→ first candidate
→ destructive FAIL
→ PA-01..PA-38
→ first compound retest PASS CANDIDATE
→ FRESH INDEPENDENT VALIDATION CURRENT

then
AI-04 whole-phase destructive acceptance
→ direct provider/model proof only where a concrete decision is blocked on evidence
→ AI-04 closure
→ AI-05 whole-system acceptance + implementation blueprint
→ actual AI implementation workstream(s)
```

No API key is required for current AI-04C validation.

---

# 1. Binding upstream authority

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

No provider/eval/commercial/runtime/security/control-plane feature may silently turn provider conversation state, cache, file store, tool trace, model output, background job, protocol task, telemetry, audit log or eval artifact into canonical DANTE state.

---

# 2. Provider replaceability

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
→ qualified serving platform / model / deployment / feature mode
```

A V1 may intentionally use one primary provider while preserving the boundary.

`ProviderBinding` must be able to represent model vendor, serving platform, protocol, model/snapshot or governed alias, endpoint/deployment, region/data zone, auth/credential ref, retention/data profile, feature-mode/capability profile, HarnessProfile, qualification evidence and rollout state.

---

# 3. AI-04A retained workload/eval authority

Representative DANTE workloads remain:

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

DANTE owns eval fixtures/oracles/invariants. Eval frameworks are runners, not semantic authorities.

```text
OUTCOME/ENVIRONMENT STATE > MODEL SELF-REPORT
HARD FAILURE CANNOT BE AVERAGED AWAY
INVALID FIXTURE/GRADER/HARNESS != MODEL COGNITION FAILURE
COGNITION QUALITY != SERVING-BINDING RELIABILITY
REPEATED RELIABILITY IS FIRST-CLASS
PRODUCTION TRACE != AUTOMATIC EVAL DATA
```

Direct provider/model eval tooling remains deferred until a concrete provider decision requires evidence.

---

# 4. AI-04A commercial / entitlement boundary

DANTE already owns Domain `Plan`.

```text
COMMERCIAL SUBSCRIPTION / SERVICE TIER != DANTE DOMAIN Plan
```

Candidate commercial/resource chain:

```text
CommercialOffering / ServiceTier
→ EntitlementProfile
→ capability + quota + resource envelope
→ Budget / Routing Policy
→ ModelTarget eligibility
→ ProviderBinding
```

```text
COMMERCIAL TIER != MODEL
COMMERCIAL TIER != PROVIDER
COMMERCIAL TIER != DEPLOYMENT
COMMERCIAL TIER != HARNESSPROFILE
```

Commercial tiers may limit resources, concurrency, background/research allowance, long-context envelope, rate limits, priority and premium capability availability.

They may not weaken semantic/historical correctness, privacy, Authority/AuthZ/Consent/Visibility, target safety, provider/data eligibility, effect verification/reconciliation or anti-resurrection/currentness.

No final tier names (`Base`/`Plus`/`Pro`), prices, quotas or package contents are accepted.

---

# 5. AI-04A invariants

Detailed `EV01..EV20` remain in the direct-eval specification.

Binding master invariants:

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

# 6. AI-04B accepted runtime shape

Durable authority: `docs/architecture/dante-ai-04b-concrete-runtime-capability-architecture.md`.

```text
Interaction / WorkContract
        ↓
Execution Kernel
        ├ deterministic compute
        ├ solver
        ├ Context / Semantic Query boundary
        ├ Model Access Runtime
        ├ Capability Runtime
        ├ Execution Environment Broker
        └ Async / Durable Supervisor
        ↓
Verifier
        ↓
ChangeSet / EffectGraph / Effect Runtime
        ↓
Result Maturity / Disclosure / Safe Publication
```

Responsibilities do not imply microservices/tables.

Closure chronology:

```text
first candidate
→ destructive FAIL
→ RT-01..RT-20
→ PASS CANDIDATE
→ fresh independent FAIL
→ RT-21..RT-31
→ final compound retest PASS
→ CLOSED / STRUCTURALLY ACCEPTED
```

---

# 7. AI-04B RT-01..RT-31

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

# 8. AI-04B consequences carried into AI-04C

AI-04C must preserve:

```text
current provider/data/feature-mode eligibility
DANTE-owned semantic idempotency
current authorization despite frozen config
local suppression before provider purge confirmation
late event/callback correlation and reconciliation
attached vs detached child work
admission vs final settlement/overshoot
DANTE-owned publication sequencing
provider continuation rebinding to current Harness/capabilities/policy
```

Accepted durability remains:

```text
Class A → PostgreSQL transactional outbox + bounded worker
Class B → Restate selected / dormant until first real qualifying consumer
```

Provider background execution does not replace Class-B semantics.

---

# 9. AI-04C durable authority

Detailed candidate:

- `docs/architecture/dante-ai-04c-production-assurance-control-plane-operations.md`

AI-04C used current public evidence from Microsoft 365 Copilot, Notion AI/Enterprise Search, Slack AI, GitHub Copilot, Salesforce Trust Layer, Azure AI Gateway/API Management, Amazon Bedrock Guardrails, Google Model Armor, OpenTelemetry GenAI conventions, guarded rollout tooling and established Google SRE guidance.

Evidence is used to validate reusable production patterns, not to select those vendors/products for DANTE.

Verified external behavior is explicitly separated from DANTE architectural inference in the durable AI-04C document.

---

# 10. AI-04C control-plane / runtime separation

Candidate shape:

```text
DANTE AI CONTROL PLANE
  provider/model qualification
  provider + feature-mode eligibility
  HarnessProfile registry
  capability/effect/security policy configuration
  routing policy
  Entitlement/Budget policy
  environment/egress policy
  rollout/canary/kill switches
  requalification/incident state
        ↓ approved/versioned configuration
RUNTIME DATA PLANE
  admission
  current Authority/AuthZ/Consent/Visibility
  current provider/data eligibility
  budget reservation
  Context/Egress PEP
  Model Access Runtime
  Capability/Effect PEP
  verification/reconciliation
  safe publication
  usage settlement
```

This is responsibility separation, not a forced new service topology.

---

# 11. AI-04C routing intersection

Binding:

```text
QUALIFIED != ELIGIBLE != AVAILABLE != ENTITLED
```

Candidate routing predicate:

```text
ROUTABLE
=
QUALIFIED
∩ current DATA/FEATURE ELIGIBILITY
∩ AVAILABLE/HEALTHY
∩ ENTITLED/BUDGET-ADMISSIBLE
∩ ROLLOUT-ACTIVE
```

Provider qualification includes material feature mode, retention, residency/purpose and processor path where applicable.

New models/providers/material feature modes are default inactive until registered/qualified/rolled out.

---

# 12. AI-04C configuration lifecycle

Production AI configuration is treated as releasable behavior.

```text
immutable/versioned revision
!= active environment/cohort pointer
```

Candidate lifecycle:

```text
DRAFT
→ VALIDATED
→ APPROVED
→ SHADOW when independently eligible
→ CANARY
→ PROGRESSIVE
→ ACTIVE
→ DRAINING
→ RETIRED

material incident/regression
→ PAUSE / ROLLBACK CONFIG / EMERGENCY_DISABLE
```

Configuration rollback affects future selection and does not undo already-materialized effects.

Control-plane write authority is security-sensitive and must be least-privilege/auditable.

Control-plane failure must not fall back to unbounded allow.

---

# 13. AI-04C security / guard posture

DANTE does not create an independent AI permission model.

Existing application Authority/AuthZ/Consent/Visibility remains authoritative.

Layered security may include:

```text
request/abuse controls
source/instruction provenance
query-time access eligibility
prompt/retrieval/tool injection checks
provider egress minimization
provider/cloud guardrail signals
Capability PEP
Effect PEP
verification
output DLP/disclosure
Safe Publication
```

Binding:

```text
GUARDRAIL RESULT != DANTE AUTHORITY
SECURITY SERVICE AVAILABLE != ELIGIBLE DATA RECIPIENT
MASKING / REDACTION != SEMANTIC EQUIVALENCE
```

Guard engines/versions/thresholds are production configuration and material changes require controlled requalification.

---

# 14. AI-04C credentials / secrets

Preferred order:

```text
workload identity / federation / short-lived credential
> scoped runtime secret from trusted secret manager
> long-lived provider key only where unavoidable
```

Binding:

```text
SECRETS != RUNTIME CONFIGURATION
ADMIN CREDENTIAL != INFERENCE CREDENTIAL != DELEGATED USER CREDENTIAL
```

Model context, tool schemas, telemetry and untrusted sandboxes do not receive broad high-value secrets.

Privileged generated-code path remains:

```text
isolated environment without broad secrets
→ typed capability request
→ trusted broker / Capability Runtime
→ current identity/policy + scoped credential/target/egress
→ target
```

No KMS/secret-manager product is selected.

---

# 15. AI-04C evidence / observability

Keep distinct:

```text
CANONICAL DOMAIN/APPLICATION DATA
AUDIT / EXECUTION EVIDENCE
OPERATIONAL TELEMETRY
EVAL EVIDENCE
```

```text
TELEMETRY != AUDIT != EVAL EVIDENCE != CANONICAL TRUTH
```

Default GenAI telemetry should favor metadata such as provider/model, IDs, latency, token counts, usage/cost class, retry/fallback/error/tool identity.

Default full prompt/response/ConsumerContext/tool-content capture is OFF.

Required consequential/security audit cannot depend solely on sampled telemetry or provider-side log retention.

---

# 16. AI-04C budget / commercial operations

Binding:

```text
COMMERCIAL CREDIT != PROVIDER TOKEN != ACTUAL PROVIDER COST
ADMISSION ESTIMATE != RESERVATION != SETTLEMENT
COMMERCIAL QUOTA != ABUSE RATE LIMIT != PROVIDER QUOTA != PLATFORM CAPACITY
```

Candidate flow:

```text
bounded exposure estimate
→ atomic budget reservation
→ execute
→ collect actual usage
→ settle
→ release unused reserve
→ record delayed/unknown settlement where applicable
```

A promised hard cap requires defensible upper-bound admission; otherwise the product must describe the control as a soft target/alert.

Commercial exhaustion cannot starve effect verification, reconciliation, provider-state revocation, security cleanup or required audit finalization.

---

# 17. AI-04C SRE / overload posture

Avoid multiplicative retries across SDK/gateway/runtime/durable workflow.

Candidate:

```text
one logical retry responsibility/budget
+ reason-aware attempts
+ exponential backoff/jitter where applicable
+ current deadline/budget/eligibility checks
```

Provider health/circuit state is operational evidence, not permanent qualification truth.

Fallback must consider alternate capacity and can safely degrade rather than cascade.

Candidate degradation ladder:

```text
NORMAL
→ optional enrichment off
→ reduced safe parallelism
→ cheaper/faster qualified target if quality floor permits
→ defer optional background work
→ deterministic/read-only mode where possible
→ safe unavailable/deferred
```

```text
DEGRADED PERFORMANCE MAY BE ALLOWED
DEGRADED SAFETY/PRIVACY/AUTHORIZATION/RECONCILIATION IS NOT
```

---

# 18. AI-04C SLO / incident posture

DANTE measures user-safe outcomes rather than raw provider uptime.

Candidate SLO families:

```text
interactive: time to first SAFE useful output
query: correct/current result within latency target
effect: verified success OR explicit unresolved state
background: completion within declared service window
reconciliation: UNKNOWN → resolved/escalated within target
```

Operational availability/latency can use SRE error budgets.

Privacy leaks, unauthorized effects and cross-actor disclosure are hard incidents, not acceptable ordinary error-budget consumption.

Emergency disable of new work preserves in-flight reconciliation/security cleanup capacity.

---

# 19. AI-04C rollout / shadow posture

Shadow traffic is real data processing/disclosure and requires independent eligibility.

Consequential shadow/canary work cannot dispatch uncontrolled effects.

Rollout/flag targeting uses minimum necessary non-sensitive context.

A new active config does not retroactively rewrite prior attempts or their evidence.

Material model/provider/subprocessor/retention/residency/guard/Harness changes trigger risk-proportionate requalification.

---

# 20. AI-04C PA-01..PA-38

```text
PA-01  APPLICATION/DANTE AUTHORITY REMAINS AUTHORITATIVE; AI DOES NOT WIDEN SOURCE PERMISSIONS.
PA-02  QUALIFIED != ELIGIBLE != AVAILABLE != ENTITLED.
PA-03  ROUTABLE REQUIRES ALL APPLICABLE QUALIFICATION, ELIGIBILITY, HEALTH, ENTITLEMENT AND ROLLOUT GATES.
PA-04  PROVIDER ELIGIBILITY INCLUDES MATERIAL FEATURE MODE, RETENTION, RESIDENCY, PURPOSE AND PROCESSOR PATH.
PA-05  NEW MODEL / PROVIDER / MATERIAL FEATURE MODE IS NOT ACTIVE BY DISCOVERY ALONE.
PA-06  CONTROL-PLANE CONFIGURATION IS VERSIONED; ACTIVE POINTER != IMMUTABLE CONFIG REVISION.
PA-07  FROZEN CONFIGURATION != CURRENT AUTHORIZATION.
PA-08  CONTROL-PLANE WRITE AUTHORITY IS PRIVILEGED SECURITY AUTHORITY AND MUST BE AUDITABLE.
PA-09  CONTROL-PLANE OUTAGE MUST NOT FALL BACK TO UNBOUNDED ALLOW.
PA-10  EMERGENCY DISABLE OF NEW WORK != ABANDON IN-FLIGHT RECONCILIATION.
PA-11  MANDATORY PROVIDER / CAPABILITY / EFFECT / EGRESS CONTROLS MUST NOT BE BYPASSABLE BY FEATURE CODE.
PA-12  GUARDRAIL RESULT != DANTE AUTHORITY.
PA-13  A SECURITY/GUARDRAIL SERVICE IS ITSELF A GOVERNED DATA RECIPIENT.
PA-14  UNTRUSTED SOURCE / INSTRUCTION LINEAGE MUST SURVIVE TRANSFORMATION.
PA-15  MASKING / REDACTION != SEMANTIC EQUIVALENCE.
PA-16  GUARD PROFILE VERSION / THRESHOLD / ENGINE CHANGE REQUIRES CONTROLLED REQUALIFICATION.
PA-17  SECRETS != RUNTIME CONFIGURATION.
PA-18  ADMIN CREDENTIAL != INFERENCE CREDENTIAL != DELEGATED USER CREDENTIAL.
PA-19  WORKLOAD IDENTITY / SHORT-LIVED CREDENTIALS ARE PREFERRED WHERE SUPPORTED.
PA-20  MODEL / SANDBOX DOES NOT RECEIVE BROAD HIGH-VALUE CREDENTIALS.
PA-21  TELEMETRY != AUDIT != EVAL EVIDENCE != CANONICAL TRUTH.
PA-22  FULL PROMPT / RESPONSE / CONTEXT TELEMETRY IS OFF BY DEFAULT.
PA-23  SECURITY / CONSEQUENTIAL AUDIT EVIDENCE MUST NOT DEPEND SOLELY ON SAMPLED TELEMETRY OR PROVIDER LOG RETENTION.
PA-24  COMMERCIAL CREDIT != PROVIDER TOKEN != ACTUAL PROVIDER COST.
PA-25  ADMISSION ESTIMATE != RESERVATION != SETTLEMENT.
PA-26  SHARED BUDGET ADMISSION MUST BE ATOMIC AT ITS AUTHORITY BOUNDARY.
PA-27  COMMERCIAL QUOTA != ABUSE RATE LIMIT != PROVIDER QUOTA != PLATFORM CAPACITY.
PA-28  RETRY BUDGET MUST PREVENT MULTIPLICATIVE HIDDEN RETRIES.
PA-29  RECONCILIATION / SAFETY-CRITICAL WORK MUST NOT BE STARVED BY COMMERCIAL EXHAUSTION.
PA-30  GRACEFUL DEGRADATION MAY REDUCE RESOURCE COST BUT NOT SAFETY / PRIVACY / SEMANTIC FLOORS.
PA-31  SHADOW TRAFFIC IS A REAL DATA DISCLOSURE AND MUST BE INDEPENDENTLY ELIGIBLE.
PA-32  SHADOW/CANARY WORK MUST NOT CREATE UNCONTROLLED CONSEQUENTIAL EFFECTS.
PA-33  ROLLBACK OF CONFIGURATION != ROLLBACK OF MATERIALIZED EFFECTS.
PA-34  SLOs MEASURE USER-SAFE DANTE OUTCOMES, NOT RAW PROVIDER UPTIME.
PA-35  SECURITY/PRIVACY HARD FAILURE IS NOT AN ORDINARY ERROR-BUDGET CONSUMPTION.
PA-36  PROVIDER / SUBPROCESSOR / RETENTION / RESIDENCY MATERIAL CHANGE TRIGGERS REQUALIFICATION.
PA-37  FLAG / ROLLOUT TARGETING USES MINIMUM NECESSARY NON-SENSITIVE CONTEXT.
PA-38  FEEDBACK / MODEL-IMPROVEMENT DATA SHARING IS EXPLICITLY SEPARATE FROM NORMAL TELEMETRY/EVAL.
```

---

# 21. AI-04C first kill-test result

The first candidate was attacked against stale/tampered control-plane state, unsafe admin redirect, provider/subprocessor/retention changes, guard-service outage/eligibility, shadow disclosure/effects, masking-induced semantic loss, permission-revoked derivatives, telemetry leakage, audit outage, concurrent budget oversubscription, settlement overshoot, multiplicative retries, fallback overload, quota-blocked reconciliation, kill-switch cleanup loss, privacy-hostile flag targeting, canary continuity, rollback-vs-effect confusion, feedback export and all-provider outage.

Initial candidate:

```text
FAIL
```

After PA-01..PA-38:

```text
FIRST COMPOUND RETEST
→ PASS CANDIDATE
```

This is not closure.

---

# 22. Independent AI-04C validation current

Fresh independent validation must attack without assuming PA-01..PA-38 are complete.

Minimum pressure set:

```text
control-plane read partition / stale config / tamper
control-plane authorization escalation
configuration integrity/signing assumptions
kill-switch race with in-flight work
provider/data eligibility cache drift
credential rotation during active Run
secret-manager outage
security scanner false positives/negatives
transformed prompt/tool injection
telemetry cardinality/cost explosion
telemetry exporter backpressure/outage
required audit durability failure
budget reservation leak after crashed Run
unknown provider billing settlement
shared-pool fairness/starvation
retry budget across SDK + gateway + DANTE + Restate
fallback circuit/capacity interaction
shadow/canary privacy + effect isolation
bad automatic rollback
upgrade/downgrade during reservation
all-provider outage + deterministic degraded mode
incident recovery + requalification
```

If a structural contradiction appears, harden only the smallest affected boundary and rerun the compound set.

---

# 23. Direct proof obligations remain distinct

AI-04 architecture acceptance does not execute existing Physical/Recovery proofs.

Still unexecuted where applicable:

```text
PSV-06 / SC-017 hidden-result non-interference
PSV-07 / SC-018 FTS mixed filter/query
PSV-08 / SC-019 vector recall after filtering
PSV-09 / SC-020 projection freshness/material basis
PSV-10 / SC-021 deletion/redaction propagation
PSV-21..28B durable execution / Restate / journal privacy / recovery
PSV-37 pgvector source/model/freshness provenance
```

No production implementation PASS is claimed.

---

# 24. Decisions explicitly still open

```text
OpenAI / Azure OpenAI / Anthropic / Gemini / other concrete provider set
specific model/deployment mapping
provider SDK
exact ModelTarget vocabulary
actual direct benchmark results
final eval runner
routing/fallback algorithm/order
runtime event/error implementation schemas
client-edge streaming transport
voice/realtime transport
provider background/native state/tool activation
MCP/A2A implementation
Execution Environment technology
control-plane physical topology/storage
configuration signing mechanism
admin approval workflow
feature-flag/rollout vendor
AI gateway product
security/guardrail product
secret-manager/KMS product
credential broker implementation
commercial tier names/prices/quotas
billing/credit provider
budget persistence/reservation mechanism
rate-limit algorithms/values
queue/fairness strategy
retry/backoff/circuit thresholds
SLO values/error-budget windows
audit/evidence retention
telemetry field/cardinality budgets
production region/residency mappings
pgvector/ANN/FTS activation
Restate activation
R2 activation
local model activation
production AI compute topology
```

---

# 25. Explicit non-claims

```text
AI-04 CLOSED                           NO
AI-04A DIRECT PROVIDER EVAL PASS       NO
AI-04B CLOSED                          YES / STRUCTURAL
AI-04C CLOSED                          NO
AI-04C FINAL INDEPENDENT PASS          NO
PROVIDER SELECTED                      NO
MODEL DEFAULT SELECTED                 NO
MULTI-PROVIDER REQUIRED                NO
PROVIDER SDK SELECTED                  NO
CONTROL-PLANE IMPLEMENTED              NO
AI GATEWAY SELECTED/DEPLOYED           NO
GUARDRAIL PRODUCT SELECTED             NO
SECRET MANAGER/KMS SELECTED            NO
EVAL RUNNER SELECTED                   NO
API CREDENTIALS USED                   NO
PAID MODEL API EXECUTED                NO
COMMERCIAL TIER NAMES/PRICES SET       NO
BILLING/CREDIT SYSTEM IMPLEMENTED      NO
PRODUCTION AI BACKEND IMPLEMENTED      NO
FRONTEND AI STREAMING IMPLEMENTED      NO
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

# 26. Exact next action

```text
AI-04C — FRESH INDEPENDENT DESTRUCTIVE PRODUCTION-ASSURANCE VALIDATION
```

Then, only if AI-04C closes:

```text
AI-04 WHOLE-PHASE DESTRUCTIVE ACCEPTANCE
→ reconcile AI-04A + AI-04B + AI-04C
→ execute direct provider/model proof only where a concrete decision is blocked on evidence
→ close AI-04
→ AI-05 whole-system acceptance + exact implementation blueprint
→ actual AI implementation workstream(s)
```

No provider/model/API key is required for the current independent architecture validation.