# DANTE AI-04 — Productionization Architecture

- **Status:** CLOSED / STRUCTURALLY ACCEPTED
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-04 — Productionization Architecture
- **Closure PRE-SCOPE:** `57d9b6b325d0873e46efbe88eee646f994027d2d`
- **AI-04A:** CLOSED / STRUCTURALLY ACCEPTED / A01..A30 / EV01..EV20 / DIRECT PROVIDER EVIDENCE NOT EXECUTED
- **AI-04B:** CLOSED / STRUCTURALLY ACCEPTED / RT-01..RT-31
- **AI-04C:** CLOSED / STRUCTURALLY ACCEPTED / PA-01..PA-61
- **Whole-phase:** CLOSED / STRUCTURALLY ACCEPTED / WP-01..WP-22
- **Post-closure PRE-AI05 supplement:** CLOSED / STRUCTURALLY ACCEPTED / PRE05-H01..H19
- **Current core eval families:** DANTE-E01..DANTE-E14
- **Provider/model selection:** OPEN / EVIDENCE-DRIVEN
- **Commercial tier/pricing selection:** OPEN
- **Implementation claim:** NONE
- **Database change:** NONE

This document is the durable AI-04 master closure authority. The later PRE-AI05 supplement does **not** reopen AI-04; it hardens cross-phase traceability discovered only when AI-01→AI-04 was retested as one system.

Detailed authority:

```text
docs/architecture/dante-ai-04a-direct-eval-specification.md
docs/architecture/dante-ai-04b-concrete-runtime-capability-architecture.md
docs/architecture/dante-ai-04c-production-assurance-control-plane-operations.md
docs/architecture/dante-ai-04-whole-phase-destructive-acceptance.md
docs/architecture/dante-ai-pre05-cross-phase-hardening.md
```

The full pre-closure AI-04 master candidate is preserved at commit `57d9b6b325d0873e46efbe88eee646f994027d2d`.

AI-04 is closed **structurally**, not operationally. It defines the accepted responsibility architecture that later implementation/provider choices must satisfy.

---

# 1. Closure chronology

```text
AI-04A
→ workload/eval/provider/economics architecture materialized
→ CLOSED STRUCTURALLY at whole-phase acceptance
→ direct provider/model evidence NOT EXECUTED

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
→ state-of-the-art production-assurance candidate
→ destructive FAIL
→ PA-01..PA-38
→ PASS candidate
→ independent FAIL
→ PA-39..PA-61
→ final PASS
→ CLOSED

WHOLE-PHASE
→ first cross-phase pass FAIL
→ WP-01..WP-11
→ reverse-order retest PASS candidate
→ third independent adversarial pass FAIL
→ WP-12..WP-22
→ adversarial retest PASS
→ reverse composition C → B → A PASS
→ upstream semantic check PASS
→ AI-04 CLOSED / STRUCTURALLY ACCEPTED

POST-CLOSURE PRE-AI05 WHOLE-CHAIN HARDENING
→ AI-01→AI-04 audit exposed traceability gaps around Attention,
  proactivity/oscillation, cumulative/surface disclosure and scoped autonomy
→ PRE05-H01..H14 materialized
→ first fresh retest FAIL → H15..H16
→ second full retest FAIL → H17..H18
→ third full retest FAIL → H19
→ fresh 26-case retest PASS
→ compound collision retest PASS
→ reverse PRE05→04→03→02→01 PASS
→ refreshed 2026 state-of-the-art regression PASS
→ PRE-AI05 CLOSED / STRUCTURALLY ACCEPTED
```

---

# 2. Binding project authority

AI-04 remains subordinate to accepted project semantics:

```text
PostgreSQL = sole canonical persistence/material-history authority
MODEL OUTPUT != PUBLISHABLE OUTPUT
MODEL CAPABILITY != AUTHORITY
DISPLAY NAME != EFFECT TARGET
Interaction Session != Run != Worker
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
RUN-START AUTONOMY != PERPETUAL AUTONOMY
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
ATTENTION DECISION != WORK ADMISSION != EFFECT AUTHORIZATION
SAFE SINGLE DISCLOSURE != AUTOMATICALLY SAFE CUMULATIVE DISCLOSURE
RECIPIENT != SURFACE != CHANNEL
SOURCE FUTURE ELIGIBILITY != PRIOR DISCLOSURE OCCURRENCE
```

No provider, model, SDK, runtime protocol, commercial tier or security product may silently reopen those contracts.

---

# 3. Accepted production responsibility chain

```text
Trigger / Interaction
        ↓
current trigger/work eligibility
        ↓
WorkContract
+ ConsequenceProfile
+ current Actor / represented-party context
+ current Authority / AuthZ / Consent / Visibility
+ current scoped Autonomy policy where applicable
+ current EntitlementProfile / ResourceBudget
+ current provider/data/feature eligibility
        ↓
Context / Retrieval / Memory
→ Basis / Reality / currentness
        ↓
ModelTarget or deterministic/no-model route
        ↓
qualified candidate route compositions
        ↓
Routing Policy
        ↓
compatible qualified:
  HarnessProfile
  + ProviderBinding
  + feature mode
  + capability projection
  + security/control profile
        ↓
route-specific resource admission
        ↓
current egress/data eligibility at send boundary
        ↓
Model Access Runtime / Capability Runtime / deterministic runtime
        ↓
Verifier
        ↓
current effect governance / approval / autonomy revalidation
        ↓
verification / reconciliation
        ↓
Result Maturity
        ↓
AttentionPolicy / AttentionBudget where attention is possible
        ↓
recipient + surface + channel Disclosure Projection
        ↓
cumulative disclosure check where material
        ↓
governed publication/notification transport
        ↓
truthful communication state from evidence
        ↓
usage settlement / audit / telemetry / eval evidence
```

These are logical responsibilities, not mandatory microservices/tables.

---

# 4. Provider replaceability

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY
HARNESSPROFILE != PROVIDERBINDING
DANTE FEATURE/BUSINESS CODE != CONCRETE PROVIDER SDK
PROVIDER REPLACEABLE != PROVIDERS IDENTICAL
PROVIDER REPLACEABLE != LOWEST-COMMON-DENOMINATOR PROVIDER USAGE
```

Provider replaceability includes independent governance of:

```text
model/Harness quality
serving platform/binding
feature mode
provider state/cache/continuation
security controls
capability projection
routing
commercial/resource policy
rollout
health/capacity
```

A V1 may intentionally use one primary provider while preserving this boundary.

---

# 5. AI-04A + PRE-AI05 — accepted eval/provider/economics authority

Current accepted core workload families are:

```text
DANTE-E01  model avoidance / deterministic fast path
DANTE-E02  intent + reference / target resolution
DANTE-E03  structured extraction / understanding
DANTE-E04  native query + history + absence semantics
DANTE-E05  context + privacy + Reality Scope + cumulative disclosure
DANTE-E06  planning / replanning / scenarios
DANTE-E07  document / long-context / multimodal
DANTE-E08  tool / capability use
DANTE-E09  consequential effect + scoped autonomy
DANTE-E10  multi-actor / delegation / recipient-surface-channel disclosure
DANTE-E11  adaptive memory / learning
DANTE-E12  currentness / failure / supersession / failover
DANTE-E13  open-world research / grounding
DANTE-E14  proactivity / Attention / causal-loop / notification truth
```

Accepted core rules include:

```text
DANTE OWNS EVAL SEMANTICS
OUTCOME/ENVIRONMENT STATE > MODEL SELF-REPORT
HARD FAILURE CANNOT BE AVERAGED AWAY
COGNITION QUALITY != SERVING-BINDING RELIABILITY
REPEATED RELIABILITY IS FIRST-CLASS
CAPABILITY EVAL != REGRESSION EVAL
PRODUCTION TRACE != AUTOMATIC EVAL DATA
IT-IT + EN-US CORE COVERAGE
TRAJECTORY/CROSS-WORK PRIVACY FAILURES MAY BE FIRST-CLASS
ATTENTION/AUTONOMY QUALITY DOES NOT WEAKEN HARD SAFETY GATES
```

```text
EFFECTIVE COST PER SUCCESSFUL DANTE TASK
```

Direct provider evidence is intentionally deferred until a concrete selection/activation decision requires it.

---

# 6. Commercial/service-tier boundary

DANTE already owns Domain `Plan`.

```text
COMMERCIAL SUBSCRIPTION / SERVICE TIER != DANTE DOMAIN Plan
```

Accepted commercial-control chain:

```text
CommercialOffering / ServiceTier
→ EntitlementProfile
→ capability + quota + resource envelope
→ Budget / Routing Policy
→ eligible route set
```

```text
COMMERCIAL TIER != MODEL
COMMERCIAL TIER != PROVIDER
COMMERCIAL TIER != DEPLOYMENT
HIGHER COMMERCIAL TIER != BROADER AUTHORITY
HIGHER COMMERCIAL TIER != WEAKER PRIVACY
HIGHER COMMERCIAL TIER != AUTOMATIC GREATER AUTONOMY
HIGHER COMMERCIAL TIER != LICENSE TO INTERRUPT MORE OFTEN
```

Commercial tiers may limit resource/capability envelopes but may not weaken semantic/historical correctness, privacy, Authority/AuthZ/Consent/Visibility, target safety, provider/data eligibility, effect verification/reconciliation, anti-resurrection, scoped autonomy or Attention policy.

```text
ENTITLED != SERVABLE
COMMERCIAL CREDIT != PROVIDER TOKEN != ACTUAL PROVIDER COST
```

Exact offering names/prices/quotas remain open.

---

# 7. AI-04B — accepted runtime authority

Core runtime shape:

```text
Interaction / WorkContract
        ↓
Execution Kernel
        ├ deterministic compute / solver
        ├ Model Access Runtime
        ├ Capability Runtime
        ├ Execution Environment Broker
        └ Async / Durable Supervisor
        ↓
Verifier
        ↓
ChangeSet / EffectGraph / Effect Runtime
        ↓
Result Maturity / Disclosure / Safe Publication / Attention
```

Accepted distinctions include:

```text
RUN != MODEL INVOCATION != PROVIDER ATTEMPT
RAW PROVIDER EVENT != DANTE RUNTIME EVENT != PUBLICATION EVENT
CLIENT DISCONNECT != RUN CANCEL != EFFECT ROLLBACK
CANCELLATION REQUESTED != CONFIRMED != QUIESCED
PARTIAL TOOL ARGUMENTS != EXECUTABLE TOOL REQUEST
PROVIDER PARALLEL TOOL CALL != EFFECTGRAPH AUTHORIZATION
PROVIDER BACKGROUND != DANTE DURABLE EXECUTION
PROVIDER CONTINUATION != DANTE SESSION/CONTEXT/MEMORY
REFUSAL != INFRA FAILURE
PROVIDER TOOL != DANTE CAPABILITY
PROVIDER-HOSTED EXECUTION != DANTE Execution Environment
PROVIDER CALL ID != DANTE SEMANTIC IDEMPOTENCY IDENTITY
REMOTE CALLBACK != CURRENT RUN ELIGIBILITY
```

Any older local diagram that looks like `ModelTarget → Routing → HarnessProfile → ProviderBinding` is subordinate to whole-phase `WP-03`: routing selects a compatible, qualified HarnessProfile + ProviderBinding + feature/control composition.

Class-A/Class-B remains:

```text
Class A → PostgreSQL transactional outbox + bounded worker
Class B → Restate selected / dormant until first real qualifying consumer
```

No activation is implied.

---

# 8. AI-04C — accepted production-assurance authority

Accepted production posture includes:

```text
QUALIFIED != ELIGIBLE != AVAILABLE != ENTITLED
```

and routability requires the intersection of every applicable current gate.

Control plane and runtime enforcement remain distinct responsibilities.

Accepted operational principles include:

```text
current application Authority remains authoritative
new material provider/model/feature mode defaults inactive until qualification
control-plane config is versioned/auditable
revocation/emergency deny outranks stale cached allow
mandatory security controls do not silently fail open
guardrail service is itself a governed data recipient
short-lived/workload identity preferred where available
broad secrets never enter model/sandbox context
telemetry != audit != eval evidence != canonical truth
full prompt/context telemetry off by default
admission estimate != reservation != settlement
retry budget prevents multiplicative retries
reconciliation cannot be starved by commercial exhaustion
graceful degradation may reduce cost/performance, not safety floors
shadow traffic is real disclosure and cannot create uncontrolled effects
rollback config != rollback materialized effects
SLO measures user-safe DANTE outcomes
security/privacy hard failure is not ordinary error-budget consumption
provider/subprocessor/retention/residency material change triggers requalification
```

`PA-01..PA-61` remain normative.

---

# 9. Whole-phase composition authority

Cross-phase rules `WP-01..WP-22` are normative and live in:

- `docs/architecture/dante-ai-04-whole-phase-destructive-acceptance.md`

They include:

```text
eval qualification != current production routability
effective route quality after production transformations
HarnessProfile + ProviderBinding compatibility qualification
fallback independent qualification
coherent per-invocation config snapshots
continuation compatibility after config changes
new attempt → new/current resource admission
reconciliation after emergency disable
multi-dimensional qualification staleness
ENTITLED != SERVABLE
provider outage != deterministic DANTE outage
eval composition != production composition
auxiliary/sub-model invocation governance
route selection/context assembly != egress authorization
fallback capability contraction != silent context truncation
capability contract version drift
cache hit != Harness/tool/security/Auth continuity
operational hidden-result non-interference
model picker != routing Authority
route-specific resource admission
per-invocation coherence != whole-Run config immutability
direct eval != production capacity qualification
```

Where a whole-phase rule is stronger than an earlier sub-phase assumption, it governs.

---

# 10. PRE-AI05 post-closure hardening authority

`docs/architecture/dante-ai-pre05-cross-phase-hardening.md` is a binding supplement for AI-05 and later implementation.

Accepted `PRE05-H01..H19` establish:

```text
AttentionBudget != ResourceBudget != commercial/provider quota
trigger fired != material change/current work eligibility
causal-loop / oscillation safety is production-critical
DANTE-E14 is core
cumulative disclosure may span related work
recipient != surface != channel
scoped autonomy != Authority/AuthZ/approval
unsafe autonomy != unnecessary over-asking
current-tree executable eval coverage is E01..E14
AI-01 old ModelTarget shorthand is historical
WP route composition outranks older AI-04B local sequencing
old pre-Physical AI/context boundary is historical in current navigation
formal IFC/leakage-budget/ACS mechanisms remain challengers
commercial tier cannot buy weaker safety
AttentionDecision != proactive Work Admission != Effect authorization
cumulative disclosure may span Runs/Interactions/surfaces/known related sinks
RUN-START AUTONOMY != PERPETUAL AUTONOMY
NOTIFY != SENT != DELIVERED != SEEN != ACKNOWLEDGED != ACCEPTED
SOURCE FUTURE ELIGIBILITY != PRIOR DISCLOSURE OCCURRENCE
```

The supplement passed a fresh 26-case whole-chain retest, compound collision retest, reverse-order retest and refreshed 2026 state-of-the-art regression. This is structural evidence only.

---

# 11. Concrete production route activation gate

AI-04 architecture closes with provider/model selection OPEN.

A concrete production route may not be activated solely from public benchmark/list-price/docs evidence.

Applicable direct evidence must cover the actual production composition or independently qualify material deltas.

Production activation evidence includes, as applicable:

```text
DANTE workload quality
hard semantic/privacy/safety gates
serving-binding reliability
feature-mode/data eligibility
Harness/binding compatibility
mandatory guard/control compatibility
effective production-route quality
resource/economic viability
intended production capacity/service-envelope viability
```

```text
ARCHITECTURE ACCEPTANCE != PROVIDER ACTIVATION
```

---

# 12. Deterministic/no-model route

```text
MODEL OUTAGE != WHOLE DANTE OUTAGE
```

where work is legitimately satisfiable through PostgreSQL/native application query, validated application logic, deterministic computation, solver or accepted non-model capability.

Model avoidance is a production route, not merely an eval baseline.

---

# 13. Decisions intentionally open

```text
concrete primary/fallback provider(s)
concrete model snapshots/defaults
provider SDKs
exact ModelTarget vocabulary
actual direct provider eval results
final eval runner
runtime module/class/API implementation
physical control-plane storage/topology
AI gateway product
feature-flag/rollout implementation
guard/security product
secret manager/KMS/IAM implementation
commercial offering names/prices/quotas
billing/credit implementation
budget reservation/settlement implementation
Attention implementation
cumulative-disclosure accounting mechanism/storage
formal IFC / leakage-budget / ACS adoption
rate-limit/retry/circuit values
SLO/error-budget targets
client/voice streaming transports
provider native background/tools/files/cache activation
MCP/A2A activation
Execution Environment technology
Restate activation
R2 activation
pgvector/ANN/FTS activation
embedding model/dimensions
production regions/residency mappings
```

---

# 14. Direct proof obligations remain unexecuted where applicable

Architecture closure does not execute Physical/Recovery direct proofs.

Examples still distinct include:

```text
PSV-06 / SC-017 hidden-result non-interference
PSV-07 / SC-018 FTS mixed filter/query
PSV-08 / SC-019 vector recall after filtering
PSV-09 / SC-020 projection freshness/material basis
PSV-10 / SC-021 deletion/redaction propagation
PSV-21..28B durable execution / Restate / journal privacy / recovery
PSV-37 pgvector source/model/freshness provenance
```

No production PASS is inferred from architecture acceptance.

---

# 15. Explicit non-claims

```text
AI-04 CLOSED                           YES / STRUCTURAL
AI-04A CLOSED                          YES / STRUCTURAL
AI-04B CLOSED                          YES / STRUCTURAL
AI-04C CLOSED                          YES / STRUCTURAL
WHOLE-PHASE ACCEPTANCE                 YES / WP-01..WP-22
PRE-AI05 CROSS-PHASE HARDENING         YES / H01..H19 / STRUCTURAL
CURRENT CORE EVAL COVERAGE             E01..E14
DIRECT PROVIDER EVAL PASS              NO
PROVIDER SELECTED                      NO
MODEL DEFAULT SELECTED                 NO
PROVIDER SDK SELECTED                  NO
EVAL RUNNER SELECTED                   NO
API CREDENTIALS USED                   NO
PAID MODEL API EXECUTED                NO
PRODUCTION ROUTE CAPACITY PASS         NO
PRODUCTION AI BACKEND IMPLEMENTED      NO
FRONTEND AI IMPLEMENTED                NO
CONTROL PLANE IMPLEMENTED              NO
COMMERCIAL TIER NAMES/PRICES SET       NO
BILLING IMPLEMENTED                    NO
POSTGRESQL/ALEMBIC CHANGED             NO
NEW AI TABLE/INDEX                     NO
PGVECTOR/ANN/FTS ACTIVATED             NO
RESTATE/R2 ACTIVATED                   NO
MCP/A2A ACTIVATED                      NO
EXECUTION ENVIRONMENT IMPLEMENTED      NO
SC/PSV DIRECT PROOFS EXECUTED          NO
AI-05 SUBSTANTIVE DESIGN STARTED       NO
```

---

# 16. Next exact phase boundary

Next:

```text
GLOBAL CURRENT-TRUTH RECONCILIATION
→ update current project navigation/status/roadmap
→ mark AI-04 CLOSED + PRE-AI05 CLOSED / H01..H19
→ make E01..E14 current
→ classify stale pre-Physical AI boundary as historical in current navigation
→ route AI work to AI-05

then

AI-05 — WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT
→ translate accepted architecture into the final buildable blueprint
→ identify exact implementation boundaries and decision-specific proof gates

then

actual AI implementation workstream(s)
```

Concrete provider/model activation remains evidence-gated.