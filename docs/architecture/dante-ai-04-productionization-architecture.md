# DANTE AI-04 — Productionization Architecture

- **Status:** CANDIDATE / AI-04A MATERIALIZED / AI-04B CLOSED / AI-04C CLOSED / WHOLE-PHASE DESTRUCTIVE ACCEPTANCE CURRENT / NOT CLOSED
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-04 — Productionization Architecture
- **Current focus:** AI-04 Whole-Phase Destructive Acceptance
- **Upstream:** AI-02.1 CLOSED / AI-03 CLOSED
- **AI-04A:** MATERIALIZED / A01..A30 / EV01..EV20 / direct provider evidence DEFERRED UNTIL DECISION-CRITICAL
- **AI-04B:** CLOSED / STRUCTURALLY ACCEPTED / RT-01..RT-31
- **AI-04C:** CLOSED / STRUCTURALLY ACCEPTED / PA-01..PA-61
- **Provider/model selection:** OPEN / EVIDENCE-DRIVEN
- **Commercial tier/pricing selection:** OPEN
- **Implementation claim:** NONE
- **Database change:** NONE

This document is the durable master for AI-04 Productionization Architecture.

Detailed authority:

```text
docs/architecture/dante-ai-04a-direct-eval-specification.md
docs/architecture/dante-ai-04b-concrete-runtime-capability-architecture.md
docs/architecture/dante-ai-04c-production-assurance-control-plane-operations.md
```

AI-04 converts accepted DANTE intelligence semantics into a production-ready responsibility architecture while keeping concrete provider/model/cloud/runtime-product choices evidence-driven.

---

# 1. Current sequence

```text
AI-04A — EVAL / MODEL / PROVIDER / ECONOMICS
MATERIALIZED
A01..A30 / EV01..EV20
→ direct provider/model proof deferred until decision-critical

AI-04B — CONCRETE RUNTIME + CAPABILITIES
first candidate
→ destructive FAIL
→ RT-01..RT-20
→ PASS CANDIDATE
→ fresh independent FAIL
→ RT-21..RT-31
→ final compound PASS
→ CLOSED / STRUCTURALLY ACCEPTED

AI-04C — PRODUCTION ASSURANCE / SECURITY / PRIVACY /
CONTROL PLANE / OPERATIONS
state-of-the-art research + candidate
→ destructive FAIL
→ PA-01..PA-38
→ PASS CANDIDATE
→ fresh independent FAIL
→ PA-39..PA-61
→ final compound PASS
→ CLOSED / STRUCTURALLY ACCEPTED

AI-04 WHOLE-PHASE DESTRUCTIVE ACCEPTANCE
→ CURRENT

then
AI-04 closure
→ AI-05 whole-system acceptance + implementation blueprint
→ actual AI implementation workstream(s)
```

No API key is required for the current whole-phase architecture acceptance.

---

# 2. Binding upstream authority

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

No AI provider/eval/commercial/runtime/security feature may silently create a second source of canonical truth or bypass accepted Domain/Logical/Physical authority.

---

# 3. AI-04A — provider/eval/economics authority

Representative workload families:

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

Core provider boundary:

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY
DANTE FEATURE/BUSINESS CODE != CONCRETE PROVIDER SDK
PROVIDER REPLACEABLE != PROVIDERS IDENTICAL
PROVIDER REPLACEABLE != LOWEST-COMMON-DENOMINATOR PROVIDER USAGE
```

Production chain:

```text
DANTE need
→ ModelTarget
→ HarnessProfile
→ ProviderBinding
→ ProviderAdapter
→ qualified serving platform / model / deployment / feature mode
```

DANTE owns eval semantics.

```text
OUTCOME/ENVIRONMENT STATE > MODEL SELF-REPORT
HARD FAILURE CANNOT BE AVERAGED AWAY
REPEATED RELIABILITY IS FIRST-CLASS
```

Concrete provider/model selection remains open until direct DANTE workload evidence is needed.

---

# 4. Commercial/service-tier boundary

DANTE already owns Domain `Plan`.

```text
COMMERCIAL SUBSCRIPTION / SERVICE TIER
!= DANTE DOMAIN Plan
```

Accepted architectural chain:

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
```

Commercial packaging may bound resources, concurrency, premium capabilities and priority, but cannot weaken semantic correctness, privacy, Authority, target safety, provider/data eligibility or effect reconciliation.

No Base/Plus/Pro names, prices, quotas or packages are final.

---

# 5. AI-04B — accepted runtime shape

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

Core accepted separations include:

```text
RUN != MODEL INVOCATION != PROVIDER ATTEMPT
RAW PROVIDER EVENT != DANTE RUNTIME EVENT != PUBLICATION EVENT
CANCELLATION REQUESTED != CANCELLATION CONFIRMED != EXECUTION QUIESCED
PARTIAL TOOL ARGUMENTS != EXECUTABLE TOOL REQUEST
PROVIDER PARALLEL TOOL CALL != EFFECTGRAPH AUTHORIZATION
PROVIDER BACKGROUND != DANTE DURABLE EXECUTION
PROVIDER CONTINUATION != DANTE SESSION/CONTEXT/MEMORY
CONTINUATION HANDLE != CURRENT HARNESS/POLICY/TOOLS/CAPABILITIES
REFUSAL != INFRASTRUCTURE FAILURE
SERVER-SIDE FALLBACK != DANTE ROUTING AUTHORITY
PROVIDER TOOL != DANTE CAPABILITY
PROVIDER-HOSTED EXECUTION != DANTE Execution Environment
PROVIDER CALL ID != DANTE SEMANTIC IDEMPOTENCY IDENTITY
FROZEN EXECUTION CONFIG != PERPETUAL CURRENT AUTHORIZATION
REMOTE CALLBACK != CURRENT RUN ELIGIBILITY
ATTACHED CHILD != DETACHED CHILD
BUDGET ADMISSION != FINAL COST / GUARANTEED PROVIDER STOP
```

Full RT-01..RT-31 wording lives in AI-04B.

---

# 6. Routing / failover / continuation

Baseline routing uses minimum necessary metadata and current qualification/eligibility/entitlement/health.

```text
classify work/failure
→ determine qualified current routes
→ current provider/data/feature-mode eligibility
→ current entitlement/resource envelope
→ select HarnessProfile / ProviderBinding
→ invoke ProviderAttempt
```

Failover is not blind serialized-payload replay and cannot become refusal/safety shopping.

Provider continuation/background state is bounded technical state, never DANTE memory or canonical continuity.

Provider-state reuse is locally suppressed immediately after DANTE revocation even if external purge remains pending.

---

# 7. Tools / MCP / A2A / execution environment

A model tool request is a proposal, not execution authority.

```text
finalized model proposal
→ parse/schema
→ semantic validation
→ current capability/version
→ Capability PEP
→ Effect PEP where consequential
→ dispatch
→ receipt
→ verify/reconcile
```

MCP and A2A remain protocol adapters, not DANTE ontology or Authority.

```text
MCP DISCOVERY/DESCRIPTION != TRUST/AUTHORITY
MCP ELICITATION / INPUT_REQUIRED != DANTE APPROVAL
MCP TASK != DANTE RUN
A2A AGENT CARD != TRUST
A2A TASK/STATUS != DANTE RUN/CANONICAL STATE/AUTHORITY
```

Provider-hosted code/computer execution remains distinct from DANTE Execution Environment.

Privileged execution uses trusted capability/credential brokerage rather than broad secrets in untrusted environments.

---

# 8. Durability

Accepted project decision remains:

```text
Class A
→ PostgreSQL transactional outbox + bounded worker

Class B
→ Restate selected / dormant until first real qualifying consumer
```

Provider background execution does not replace DANTE durability semantics.

Restate activation remains subject to its existing direct proof/privacy/recovery obligations.

---

# 9. AI-04C — accepted production assurance

Accepted control-plane/data-plane principle:

```text
CENTRALIZE POLICY RESPONSIBILITY
WITHOUT CENTRALIZING DOMAIN TRUTH.
```

and:

```text
CONFIGURE CENTRALLY
ENFORCE AT THE MATERIAL BOUNDARY
REVALIDATE WHEN REALITY CAN CHANGE.
```

Production routing eligibility distinguishes:

```text
QUALIFIED
!= ELIGIBLE
!= AVAILABLE
!= ENTITLED
!= ROLLOUT-ACTIVE
```

Control-plane configuration is versioned; active pointers and immutable revisions are distinct.

New material models/providers/feature modes are inactive until governed qualification and rollout.

---

# 10. AI-04C security/privacy posture

Application/DANTE Authority remains authoritative; AI never widens access.

Guardrails/security scanners are signals/PEP adapters, not Authority.

```text
GUARDRAIL RESULT != DANTE AUTHORITY
SECURITY SIGNAL DISAGREEMENT != MODEL ARBITRATION
```

A guard/security service is itself a governed recipient.

Instruction/source lineage survives transformation.

```text
MASKING / REDACTION != SEMANTIC EQUIVALENCE
WITHHELD / SECURITY-INELIGIBLE != ABSENT / FALSE
```

Post-generation material transformations require renewed result/disclosure validity where meaning can change.

Provider ineligibility after data egress does not undo prior disclosure; it triggers stop/suppress/purge/reconcile/investigate behavior as applicable.

---

# 11. Credentials / privileged control

Prefer workload identity / short-lived credentials where supported.

```text
ADMIN CREDENTIAL
!= INFERENCE CREDENTIAL
!= USER-DELEGATED CREDENTIAL
!= SANDBOX CREDENTIAL
```

Control-plane write authority is security-sensitive.

Break-glass access, if used, is scoped, time-bound, attributable, audited and auto-expiring; it cannot bypass irreducible truth/privacy/effect-safety floors.

Credential issuance/lease does not replace current DANTE authorization.

---

# 12. Evidence / observability

Keep distinct:

```text
CANONICAL DOMAIN TRUTH
AUDIT / EXECUTION EVIDENCE
OPERATIONAL TELEMETRY
EVAL EVIDENCE
```

Full prompt/context/response telemetry is OFF by default.

Required consequential/security audit evidence does not depend solely on sampled telemetry or provider log retention and requires integrity protection appropriate to purpose.

Best-effort telemetry failure/backpressure is bounded and isolated; required audit has distinct failure semantics.

High-cardinality/private data must not accidentally enter metric labels; cardinality overflow must be observable.

---

# 13. Budget / accounting

```text
COMMERCIAL CREDIT != PROVIDER TOKEN != ACTUAL PROVIDER COST
ADMISSION ESTIMATE != RESERVATION != SETTLEMENT
BUDGET RESERVATION != SPEND
PROVIDER METERING != DANTE COMMERCIAL SETTLEMENT AUTHORITY
```

Commercial usage requires DANTE-owned usage identity, idempotency, late settlement, adjustment/correction, price/mapping revision and auditability.

Shared-budget admission is atomic at its authority boundary.

Crash/unknown-cost cases must converge without unsafe early reservation release.

Commercial exhaustion cannot starve reconciliation/security cleanup already required.

---

# 14. Reliability / rollout

Operational patterns include bounded retries, retry budgets, backoff+jitter, circuit breakers, load shedding, capacity-aware failover and graceful degradation.

Provider health is scoped to material binding/region/feature mode rather than treated as one global boolean.

Shadow traffic is real disclosure and independently eligible.

Shadow output is not production output/evidence unless explicitly promoted through normal qualification/verification/publication.

Mandatory security controls cannot silently fail open.

Rollback target must still be currently qualified/eligible/not emergency-denied.

Reliability/security incident state may freeze non-essential rollout.

Critical degraded/recovery paths require risk-proportionate exercise; declared fallback is not proof of operability.

---

# 15. AI-04C closure chronology

```text
state-of-the-art research
→ candidate materialized
→ first destructive FAIL
→ PA-01..PA-38
→ compound PASS CANDIDATE
→ fresh independent FAIL
→ PA-39..PA-61
→ final compound PASS
→ CLOSED / STRUCTURALLY ACCEPTED
```

Full PA-01..PA-61 wording and evidence ledger live in AI-04C.

---

# 16. Whole-phase acceptance problem

AI-04 sub-phases can each be locally coherent while still contradicting one another.

The whole-phase review must attack at least:

```text
A provider/model can win eval but be operationally ineligible.
An entitlement can allow a capability whose only qualified route is privacy-ineligible.
A fallback can satisfy runtime semantics but violate economics/residency.
A rollout can preserve provider qualification but invalidate HarnessProfile evidence.
A guardrail can alter output enough to invalidate model-quality eval assumptions.
A budget policy can choose a cheaper route below the workload quality floor.
A control-plane config can select a ModelTarget with no currently qualified binding.
A provider feature mode can alter retention and invalidate previously accepted eval evidence.
A failover after partial provider work can break cost/idempotency/reconciliation assumptions.
Shadow/canary data can violate eval-data/purpose restrictions.
Telemetry/audit design can leak hidden eval oracle or private context.
Commercial downgrade can collide with active reservation/durable/reconciliation work.
A security kill switch can make the only model route unavailable while deterministic fallback remains possible.
All-provider outage can expose whether deterministic/read-only DANTE remains useful and truthful.
```

The review must distinguish a structural contradiction from a decision that merely needs future direct benchmark/implementation evidence.

---

# 17. Direct proof / implementation obligations remain distinct

Architecture acceptance does not execute existing Physical/Recovery proofs.

Still unexecuted where applicable include:

```text
PSV-06 / SC-017 hidden-result non-interference
PSV-07 / SC-018 FTS mixed filter/query
PSV-08 / SC-019 vector recall after filtering
PSV-09 / SC-020 projection freshness/material basis
PSV-10 / SC-021 deletion/redaction propagation
PSV-21..28B durable execution / Restate / journal privacy / recovery
PSV-37 pgvector source/model/freshness provenance
```

No implementation or direct provider benchmark PASS is claimed.

---

# 18. Decisions still open

```text
actual provider/model set
primary/fallback bindings
provider SDK(s)
exact ModelTarget vocabulary
actual direct benchmark results
final eval runner
exact routing algorithm
normalized implementation event/error schemas
client streaming transport
voice/realtime transport
provider-native background/files/cache/MCP activation
MCP/A2A implementation
Execution Environment technology
control-plane physical topology/storage
configuration-signing implementation
feature-flag/rollout product
AI gateway product
security/guardrail product
secret manager/KMS
commercial tier names/prices/quotas
billing/credit vendor
budget persistence/accounting mechanism
rate-limit/fairness algorithms
retry/circuit thresholds
SLO/error-budget targets
audit retention/implementation
production regions/residency mappings
embedding/vector/FTS activation
Restate activation
R2 activation
```

---

# 19. Explicit non-claims

```text
AI-04 CLOSED                         NO
AI-04 WHOLE-PHASE PASS                NO
AI-04A DIRECT PROVIDER EVAL PASS      NO
AI-04B CLOSED                        YES / STRUCTURAL
AI-04C CLOSED                        YES / STRUCTURAL
PROVIDER SELECTED                    NO
MODEL DEFAULT SELECTED               NO
PROVIDER SDK SELECTED                NO
API CREDENTIALS USED                 NO
PAID MODEL API EXECUTED              NO
COMMERCIAL TIER NAMES/PRICES SET     NO
CONTROL PLANE IMPLEMENTED            NO
AI GATEWAY / GUARDRAIL VENDOR SET    NO
PRODUCTION AI BACKEND IMPLEMENTED    NO
POSTGRESQL/ALEMBIC CHANGED           NO
NEW AI TABLE/INDEX                   NO
PGVECTOR/ANN/FTS ACTIVATED           NO
RESTATE/R2 ACTIVATED                 NO
MCP/A2A ACTIVATED                    NO
EXECUTION ENVIRONMENT IMPLEMENTED    NO
SC/PSV DIRECT PROOFS EXECUTED        NO
AI-05 STARTED                        NO
```

---

# 20. Exact next action

```text
AI-04 — WHOLE-PHASE DESTRUCTIVE ACCEPTANCE
```

Method:

```text
reconstruct A/B/C independently
→ generate cross-phase attacks before reading local conclusions
→ compare against A01..A30 / EV01..EV20 / RT-01..RT-31 / PA-01..PA-61
→ separate structural gaps from deferred evidence/product choices
→ harden only real structural contradictions
→ final whole-phase retest
→ close AI-04 only if coherent
```

After AI-04 closure:

```text
AI-05 — WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT
```
