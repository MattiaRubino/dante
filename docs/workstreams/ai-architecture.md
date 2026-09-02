# DANTE AI Architecture Workstream

- **Status:** ACTIVE / BRANCH-LOCAL DURABLE WORKSTREAM RECORD
- **Branch:** `feature/ai-architecture`
- **Current phase:** AI-04 — Productionization Architecture
- **AI-04A:** MATERIALIZED / DIRECT PROVIDER EVIDENCE DEFERRED UNTIL DECISION-CRITICAL
- **AI-04B:** CLOSED / STRUCTURALLY ACCEPTED / RT-01..RT-31
- **AI-04C:** CANDIDATE MATERIALIZED / PA-01..PA-38 / INDEPENDENT VALIDATION CURRENT
- **AI-03 overall:** CLOSED / STRUCTURALLY ACCEPTED
- **AI-03A:** CLOSED / C01..C33
- **AI-03B:** CLOSED / B01..B35
- **AI-03C:** CLOSED / MAT-01..MAT-15
- **Implementation claim:** NONE
- **Provider/model selection:** OPEN / EVIDENCE-DRIVEN
- **Commercial packaging:** OPEN / ARCHITECTURAL ENTITLEMENT + RESOURCE BOUNDARY ONLY
- **Merge status:** UNMERGED

This document is the durable branch-local continuation record for the DANTE AI architecture workstream. Repository truth outranks conversation memory.

---

## 1. Branch identity

```text
repository  MattiaRubino/dante
branch      feature/ai-architecture
```

Protected `main` remains integrated authority for closed shared foundations and the current PostgreSQL baseline. This branch owns only bounded newer AI architecture truth until protected-main integration.

A new chat/session does not create a new AI workstream.

---

## 2. Mandatory reading order

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
docs/workstreams/ai-architecture-live-handoff.md  # only while active

current AI architecture sources
current branch/ref + relation to protected main
```

Current AI authority includes:

```text
docs/architecture/dante-ai-foundation.md
docs/architecture/ai-production-engineering-state-of-the-art-2026.md
docs/architecture/dante-ai-02-1-intelligence-reengineering.md
docs/architecture/dante-ai-03-context-retrieval-memory.md
docs/architecture/dante-ai-03a-full-context-architecture.md
docs/architecture/dante-ai-03b-retrieval-memory-architecture.md
docs/architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md
docs/architecture/dante-ai-04-productionization-architecture.md
docs/architecture/dante-ai-04a-direct-eval-specification.md
docs/architecture/dante-ai-04b-concrete-runtime-capability-architecture.md
docs/architecture/dante-ai-04c-production-assurance-control-plane-operations.md
```

For AI-04 conclusions touching semantics/persistence, inspect Product/North Star, Domain, Whole Logical/WL-H01..H12, Physical, CP6/PostgreSQL Constitution, current DB/Alembic truth, Recovery and PSV obligations directly.

---

## 3. Accepted upstream project foundation

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN
CLOSED

LOGICAL
CLOSED / 57 OF 57 / WL-H01..WL-H12

PHYSICAL
CLOSED
PostgreSQL 18 major family
sole canonical persistence + material-history authority

BACKEND CP1–CP5
CLOSED / INTEGRATED

CP6 DATABASE
CLOSED / INTEGRATED

CURRENT PostgreSQL
18.6
Alembic 20260830_09
69 tables / 5 views / 15 routines / 76 triggers /
97 indexes / 69 FKs / 123 CHECKs

RECOVERY
CP01–CP07 LOCAL PASS / CLOSED / INTEGRATED
remote backup provider TBD / NOT ACTIVATED
production/cloud recovery NOT CLAIMED
```

No AI convenience may create a second canonical database, generic Fact/Memory ontology or universal semantic root.

---

## 4. Current compact AI roadmap

```text
AI-00 — SEMANTIC & PRODUCT FOUNDATION
COMPLETE

AI-01 — PRODUCT FORM + PRODUCTION ENGINEERING RESEARCH
COMPLETE

AI-02 — INTELLIGENCE RUNTIME ARCHITECTURE
CLOSED / STRUCTURALLY ACCEPTED
AI-02.1 v0.5

AI-03 — CONTEXT / RETRIEVAL / MEMORY
CLOSED / STRUCTURALLY ACCEPTED
  AI-03A CLOSED / C01..C33
  AI-03B CLOSED / B01..B35
  AI-03C CLOSED / MAT-01..MAT-15

AI-04 — PRODUCTIONIZATION ARCHITECTURE
ACTIVE / CURRENT

  AI-04A — EVAL / MODEL / PROVIDER / ECONOMICS
  MATERIALIZED
  direct provider/model evidence deferred until decision-critical

  AI-04B — CONCRETE RUNTIME + CAPABILITIES
  CLOSED / STRUCTURALLY ACCEPTED / RT-01..RT-31

  AI-04C — PRODUCTION ASSURANCE / SECURITY / PRIVACY / CONTROL PLANE / OPERATIONS
  CANDIDATE MATERIALIZED
  PA-01..PA-38
  first compound retest PASS CANDIDATE
  fresh independent destructive validation CURRENT

AI-05 — WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT
FUTURE / FINAL ARCHITECTURE-TO-BUILD BOUNDARY

THEN
ACTUAL AI IMPLEMENTATION WORKSTREAM(S)
```

AI-04 may use proof/benchmark code only where a production decision cannot responsibly be made from architecture/current evidence alone. That is not production backend implementation.

---

## 5. AI-02 accepted runtime baseline

Durable source: `docs/architecture/dante-ai-02-1-intelligence-reengineering.md`.

Accepted responsibilities include:

```text
Interaction Edge / Interaction Session
Work Intake / WorkContract / Supersession
Reference / Target Resolution
ConsequenceProfile
Semantic Query / Projection Gateway
Context Engine
Scenario Workspace
BasisManifest
ModelTarget / HarnessProfile
Deterministic Compute / Solver
Capability Runtime
Execution Environment
Verifier
Policy mesh
ChangeSet / EffectGraph
Effect Runtime
Application / Domain
Result Maturity
Disclosure / Safe Publication
Attention
```

Critical retained rules:

```text
Interaction Session != Run != Worker
DISPLAY NAME != EFFECT TARGET
MODEL OUTPUT != PUBLISHABLE OUTPUT
INTERNAL STREAM != RECIPIENT STREAM
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
CANCEL RUN != UNDO ALREADY-DISPATCHED EFFECTS
SCENARIO STATE != CANONICAL CURRENT STATE
CONTEXT ACCESS != DISCLOSURE PERMISSION
APPROVAL != PERPETUAL AUTHORIZATION FOR MATERIALLY CHANGED WORK
CACHE HIT != CURRENT DISCLOSURE AUTHORIZATION
```

Do not reopen AI-02 broadly because a production technology prefers another shape.

---

## 6. AI-03 closure

Durable authority:

```text
docs/architecture/dante-ai-03-context-retrieval-memory.md
docs/architecture/dante-ai-03a-full-context-architecture.md
docs/architecture/dante-ai-03b-retrieval-memory-architecture.md
docs/architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md
```

AI-03A: **CLOSED / C01..C33**.
AI-03B: **CLOSED / B01..B35**.
AI-03C: **CLOSED / MAT-01..MAT-15**.

Binding materialization posture includes:

```text
ARCHITECTURE CONTRACT != PERSISTENCE OWNER
DEFAULT NONCANONICAL PERSISTENCE = NO
semantic authority != functional role != survival disposition != physical owner != eligibility
Class-A durable technical coordination != Class-B durable execution
DURABLE JOURNAL != PRIVACY-FREE RUNTIME
ASYNC INVALIDATION != CURRENT ELIGIBILITY
recomputable derivatives are sacrificial during recovery
runtime/provider/derived recovery cannot outrun canonical readiness
ANN is optimization, not prerequisite
representation generations do not mix silently
semantic obligation != execution/audit evidence
```

No PostgreSQL/Alembic change or provider/model selection came from AI-03 closure.

---

## 7. AI-04A retained authority

Durable sources:

```text
docs/architecture/dante-ai-04-productionization-architecture.md
docs/architecture/dante-ai-04a-direct-eval-specification.md
```

Workloads: `DANTE-E01..E13`.

Evaluation principles:

```text
DANTE OWNS EVAL SEMANTICS
OUTCOME/ENVIRONMENT STATE > MODEL SELF-REPORT
HARD FAILURE CANNOT BE AVERAGED AWAY
HIDDEN ORACLE STATE MUST NOT LEAK
INVALID FIXTURE/GRADER/HARNESS != MODEL COGNITION FAILURE
COGNITION QUALITY != SERVING-BINDING RELIABILITY
REPEATED RELIABILITY IS FIRST-CLASS
CAPABILITY EVAL != REGRESSION EVAL
PRODUCTION TRACE != AUTOMATIC EVAL DATA
IT-IT + EN-US CORE COVERAGE
```

Provider boundary:

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY
DANTE FEATURE/BUSINESS CODE != CONCRETE PROVIDER SDK
PROVIDER REPLACEABLE != PROVIDERS IDENTICAL
PROVIDER REPLACEABLE != LOWEST-COMMON-DENOMINATOR PROVIDER USAGE
```

```text
DANTE need
→ ModelTarget
→ HarnessProfile
→ ProviderBinding
→ ProviderAdapter
→ qualified serving platform/model/deployment/feature mode
```

Primary economics metric:

```text
EFFECTIVE COST PER SUCCESSFUL DANTE TASK
```

No concrete provider/model is selected. Direct eval tooling remains deferred until decision-critical.

---

## 8. Commercial/service-tier boundary

```text
COMMERCIAL SUBSCRIPTION / SERVICE TIER != DANTE DOMAIN Plan
```

```text
CommercialOffering / ServiceTier
→ EntitlementProfile
→ capability + quota + resource envelope
→ Budget / Routing Policy
→ ModelTarget eligibility
→ ProviderBinding
```

```text
COMMERCIAL TIER != MODEL / PROVIDER / DEPLOYMENT
```

Commercial tiers may limit resource/capability envelopes but may not weaken truth, privacy, Authority, target safety, provider/data eligibility, effect verification/reconciliation or anti-resurrection/currentness.

No names/prices/quotas/package contents are final.

---

## 9. AI-04B closure

Durable authority:

- `docs/architecture/dante-ai-04b-concrete-runtime-capability-architecture.md`

Closure chronology:

```text
first candidate
→ first destructive kill-test FAIL
→ RT-01..RT-20
→ compound retest PASS CANDIDATE
→ fresh independent validation FAIL
→ RT-21..RT-31
→ final compound retest PASS
→ CLOSED / STRUCTURALLY ACCEPTED
```

No Domain/Logical/Physical/PostgreSQL reopen was required.

---

## 10. AI-04B accepted runtime shape

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
Result Maturity / Disclosure / Safe Publication
```

Responsibilities do not imply microservices/tables.

---

## 11. AI-04B RT-01..RT-31

Full normative wording lives in the AI-04B durable document.

Key retained separations:

```text
RUN != MODEL INVOCATION != PROVIDER ATTEMPT
RAW PROVIDER EVENT != DANTE RUNTIME EVENT != PUBLICATION EVENT
CLIENT DISCONNECT != STREAM STOP != INVOCATION CANCEL != RUN CANCEL != EFFECT ROLLBACK
CANCELLATION REQUESTED != CANCELLATION CONFIRMED != EXECUTION QUIESCED
PARTIAL TOOL ARGUMENTS != EXECUTABLE TOOL REQUEST
PROVIDER PARALLEL TOOL CALL != EFFECTGRAPH PARALLEL AUTHORIZATION
PROVIDER BACKGROUND EXECUTION != DANTE DURABLE EXECUTION
PROVIDER CONTINUATION STATE != DANTE SESSION / CONTEXT / MEMORY
CONTINUATION HANDLE != CURRENT HARNESS/POLICY/TOOLS/CAPABILITIES
REFUSAL != INFRASTRUCTURE FAILURE
PROVIDER SERVER-SIDE FALLBACK != DANTE ROUTING AUTHORITY
PROVIDER TOOL != DANTE CAPABILITY
MCP/A2A DISCOVERY/TASK STATE != DANTE TRUST/AUTHORITY/RUN TRUTH
PROVIDER-HOSTED EXECUTION != DANTE EXECUTION ENVIRONMENT
PROVIDER CALL ID != DANTE SEMANTIC IDEMPOTENCY IDENTITY
FROZEN EXECUTION CONFIG != PERPETUAL CURRENT AUTHORIZATION
PUBLISHED DELTA = EXTERNALIZATION
REMOTE CALLBACK != CURRENT RUN ELIGIBILITY
ATTACHED CHILD != DETACHED CHILD
BUDGET ADMISSION != FINAL COST / GUARANTEED PROVIDER STOP
MCP INPUT_REQUIRED/AUTO-FULFIL != USER INPUT/CONSENT/APPROVAL
```

---

## 12. Class-A / Class-B durability

```text
Class A → PostgreSQL transactional outbox + bounded worker
Class B → Restate selected / dormant until first real qualifying consumer
```

Provider background execution does not replace Class-B semantics.

Restate activation still requires applicable direct proof/privacy/recovery obligations.

---

## 13. AI-04C durable authority

```text
docs/architecture/dante-ai-04c-production-assurance-control-plane-operations.md
```

Current status:

```text
current 2026 production-pattern research COMPLETE ENOUGH
first production-assurance candidate BUILT
first destructive kill-test FAIL
PA-01..PA-38 incorporated
first compound retest PASS CANDIDATE
fresh independent destructive validation CURRENT
```

AI-04C researched current public patterns from Microsoft 365 Copilot, Notion, Slack, GitHub Copilot, Salesforce Trust Layer, Azure AI Gateway/API Management, AWS Bedrock Guardrails, Google Model Armor, OpenTelemetry, guarded rollout tooling and Google SRE.

Public behavior is evidence; named external products remain challengers/pattern sources, not DANTE technology selections.

---

## 14. AI-04C core control-plane posture

```text
CONTROL PLANE
  qualification / eligibility
  Harness/security/routing/budget/environment policy
  rollout / kill switches / requalification

!=

RUNTIME DATA PLANE
  admission
  current Authority/AuthZ/Consent/Visibility
  current provider/data eligibility
  resource reservation
  Context/Egress PEP
  Model Access Runtime
  Capability/Effect PEP
  verification/reconciliation
  Safe Publication
  usage settlement
```

Responsibilities do not imply separate microservices.

Binding:

```text
QUALIFIED != ELIGIBLE != AVAILABLE != ENTITLED
```

```text
ROUTABLE
=
QUALIFIED
∩ ELIGIBLE
∩ AVAILABLE
∩ ENTITLED
∩ ROLLOUT-ACTIVE
```

New model/provider/material feature mode defaults to inactive until qualified and rolled out.

---

## 15. AI-04C config / security / credential posture

```text
ACTIVE POINTER != IMMUTABLE CONFIG REVISION
FROZEN CONFIG != CURRENT AUTHORIZATION
CONTROL-PLANE WRITE = PRIVILEGED SECURITY CAPABILITY
CONTROL-PLANE OUTAGE != UNBOUNDED ALLOW
KILL NEW WORK != ABANDON RECONCILIATION
```

Existing DANTE Authority/AuthZ/Consent/Visibility remains authoritative.

Guardrails are layered security adapters/signals, not Authority.

```text
GUARDRAIL RESULT != DANTE AUTHORITY
SECURITY SERVICE AVAILABLE != ELIGIBLE DATA RECIPIENT
MASKING/REDACTION != SEMANTIC EQUIVALENCE
```

Credential posture:

```text
workload identity / short-lived credentials preferred where supported
ADMIN CREDENTIAL != INFERENCE CREDENTIAL != DELEGATED USER CREDENTIAL
SECRETS != RUNTIME CONFIG
MODEL/SANDBOX gets no broad high-value credentials
```

No secret-manager/KMS/guardrail/gateway vendor is selected.

---

## 16. AI-04C evidence / telemetry posture

Keep separate:

```text
CANONICAL DOMAIN/APPLICATION DATA
AUDIT / EXECUTION EVIDENCE
OPERATIONAL TELEMETRY
EVAL EVIDENCE
```

```text
TELEMETRY != AUDIT != EVAL EVIDENCE != CANONICAL TRUTH
```

Full prompt/response/ConsumerContext/tool-content telemetry is OFF by default.

Required consequential/security audit cannot rely solely on sampled traces or provider log retention.

---

## 17. AI-04C budget / SRE posture

```text
COMMERCIAL CREDIT != PROVIDER TOKEN != ACTUAL PROVIDER COST
ADMISSION ESTIMATE != RESERVATION != SETTLEMENT
COMMERCIAL QUOTA != ABUSE RATE LIMIT != PROVIDER QUOTA != PLATFORM CAPACITY
```

Shared budget admission requires an atomic authority boundary.

Commercial exhaustion cannot starve effect verification/reconciliation/security cleanup/provider-state revocation.

Retry ownership must prevent SDK × gateway × runtime × durable-workflow amplification.

Graceful degradation may reduce optional cost/performance but not safety/privacy/semantic floors.

DANTE SLOs measure user-safe DANTE outcomes, not raw provider uptime.

Security/privacy hard failures are incidents, not ordinary error-budget consumption.

---

## 18. AI-04C rollout / requalification posture

AI config behavior is treated as a release:

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

regression/security event
→ PAUSE / ROLLBACK CONFIG / EMERGENCY_DISABLE
```

Shadow traffic is real disclosure and must be independently eligible.

Shadow/canary must not create uncontrolled consequential effects.

Config rollback affects future selection; it does not undo existing effects.

Provider/subprocessor/retention/residency/model/guard/Harness material changes trigger risk-proportionate requalification.

Feedback/model-improvement sharing is separate from normal telemetry/eval.

---

## 19. AI-04C PA-01..PA-38

Full normative wording lives in the durable AI-04C document.

Core set covers:

```text
application Authority reuse
qualification/eligibility/availability/entitlement intersection
feature-mode + retention/residency/processor eligibility
new-capability default-off
versioned control plane
privileged/audited control-plane writes
fail-safe control-plane outage
kill-switch reconciliation survival
non-bypassable PEP/egress enforcement
guardrail authority/data-recipient/version boundaries
instruction lineage and masking semantics
credential class separation / workload identity
telemetry/audit/eval/canonical separation
content telemetry default-off
commercial credit/token/cost separation
admission/reservation/settlement
atomic shared-budget admission
quota/rate/provider/platform distinctions
retry budgets
protected reconciliation capacity
graceful degradation floors
shadow disclosure/effect isolation
rollback != effect undo
user-safe SLOs
hard security/privacy incident semantics
provider/subprocessor requalification
privacy-minimal rollout targeting
feedback/model-improvement separation
```

---

## 20. Current independent AI-04C validation

Required pressure includes at least:

```text
control-plane stale/read partition/tamper
control-plane authorization escalation
configuration integrity/signing assumptions
kill-switch race with in-flight work
provider/data eligibility cache drift
credential rotation during Run
secret-manager outage
security scanner false positives/negatives
transformed prompt/tool injection
telemetry cardinality/cost/backpressure
required audit durability failure
budget reservation leak after crash
unknown provider settlement
shared-pool fairness/starvation
retry budget across SDK/gateway/DANTE/Restate
fallback capacity/circuit interaction
shadow/canary privacy + effect isolation
bad automatic rollback
upgrade/downgrade during reservation
all-provider outage + deterministic degraded mode
incident recovery + requalification
```

If a contradiction appears, harden the smallest affected boundary and rerun the compound set.

---

## 21. Direct proof obligations remain distinct

Architecture acceptance does not execute existing Physical/Recovery proofs.

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

## 22. Decisions explicitly still open

```text
concrete provider/model set
specific model/deployment mapping
provider SDK
actual direct benchmark results
final eval runner
routing/fallback algorithm/order
runtime event/error implementation schema
client streaming / voice transport
provider background/native features
MCP/A2A implementation
Execution Environment technology
control-plane physical topology/storage
configuration integrity/signing mechanism
admin approval workflow
feature-flag/rollout vendor
AI gateway product
security/guardrail product
secret-manager/KMS product
commercial tier names/prices/quotas
billing/credit provider
budget persistence/reservation mechanism
rate-limit/fairness/retry/circuit values
SLO/error-budget values
audit retention
telemetry field/cardinality budgets
production regions/residency mappings
pgvector/ANN/FTS activation
Restate/R2 activation
local-model activation
production AI compute topology
```

---

## 23. Cross-cutting quality bar

Every decision is reviewed against:

```text
semantic correctness
source/canonicality integrity
historical truth
Reality Scope
reference resolution
coverage / absence semantics
multi-actor correctness
privacy / Authority / Consent / Visibility
purpose/source/use exclusions
prompt/retrieval/tool injection
instruction provenance
revocation / deletion / anti-resurrection
concurrency / stale state
provider replaceability
failure / cancellation / reconciliation
latency / token / compute / storage cost
commercial/resource-budget compatibility
simple-path performance
future extensibility
operational recoverability
observability/evaluation feasibility
```

Maximum quality does not mean maximum abstraction or maximum infrastructure.

---

## 24. Live handoff policy

Temporary session continuity lives only in `docs/workstreams/ai-architecture-live-handoff.md`.

It is branch-operational, MUST NOT merge to protected `main`, and must be deleted after meaningful payload is propagated before integration.

---

## 25. Current next action

```text
AI-04C — FRESH INDEPENDENT DESTRUCTIVE PRODUCTION-ASSURANCE VALIDATION
```

Then, only if AI-04C closes:

```text
AI-04 WHOLE-PHASE DESTRUCTIVE ACCEPTANCE
→ reconcile AI-04A + AI-04B + AI-04C
→ activate direct provider/model proof where a concrete decision is blocked on evidence
→ AI-04 closure
→ AI-05 whole-system acceptance + exact implementation blueprint
→ actual AI implementation workstream(s)
```

Do not preselect provider SDKs, model IDs, commercial prices, gateway/guardrail/flag vendors, retrieval indexes, Restate/R2 activation or new persistence before applicable evidence exists.