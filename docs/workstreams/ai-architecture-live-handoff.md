# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Workstream:** DANTE AI architecture
- **Current phase:** AI-04 — Productionization Architecture
- **AI-04A:** MATERIALIZED / DIRECT PROVIDER EVIDENCE DEFERRED UNTIL DECISION-CRITICAL
- **AI-04B:** CLOSED / STRUCTURALLY ACCEPTED / RT-01..RT-31
- **AI-04C:** CANDIDATE MATERIALIZED / PA-01..PA-38 / FRESH INDEPENDENT VALIDATION CURRENT
- **AI-03A:** CLOSED / C01..C33
- **AI-03B:** CLOSED / B01..B35
- **AI-03C:** CLOSED / MAT-01..MAT-15
- **AI-03 overall:** CLOSED / STRUCTURALLY ACCEPTED
- **Refreshed:** 2026-09-02
- **AI-04C gate PRE-SCOPE:** `c89f751de9b4190d47eb9c1230facb02a0f009ba`
- **AI-04C candidate commit:** `dd1dcaed39d1eee7d5cbf2b4cf8dd9cb5505d1a1`
- **Current branch HEAD:** FETCH LIVE before every write

This file exists only to survive chat/session/context saturation while `feature/ai-architecture` is active. Durable architecture truth lives in architecture/current workstream sources.

Repository truth outranks this handoff.

---

# 1. Resume rule

```text
repository  MattiaRubino/dante
branch      feature/ai-architecture
workstream  DANTE AI architecture
current     AI-04C Fresh Independent Production-Assurance Validation
next        AI-04 whole-phase destructive acceptance only after AI-04C closure
```

Closed upstream:

```text
AI-02.1        CLOSED / STRUCTURALLY ACCEPTED
AI-03A         CLOSED / C01..C33
AI-03B         CLOSED / B01..B35
AI-03C         CLOSED / MAT-01..MAT-15
AI-03 overall  CLOSED / STRUCTURALLY ACCEPTED
AI-04B         CLOSED / STRUCTURALLY ACCEPTED / RT-01..RT-31
```

Do not restart generic AI-02/AI-03/AI-04B redesign without concrete contradictory downstream evidence.

---

# 2. Mandatory reading order

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

docs/workstreams/ai-architecture.md
this live handoff

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

For AI-04C conclusions touching semantics/persistence, inspect Product/North Star, Domain, Whole Logical/WL-H01..H12, Physical, CP6/PostgreSQL Constitution, current DB/Alembic truth, Recovery and PSV obligations directly.

---

# 3. Current project truth

```text
PRODUCT / NORTH STAR       CURRENT
DOMAIN                     CLOSED
LOGICAL                    CLOSED / 57 OF 57 / WL-H01..WL-H12
PHYSICAL                   CLOSED
PostgreSQL                 18.6 / sole canonical persistence + material-history authority
Alembic                    20260830_09
DB topology                69 tables / 5 views / 15 routines / 76 triggers /
                           97 indexes / 69 FKs / 123 CHECKs
RECOVERY                   CP01–CP07 LOCAL PASS / CLOSED / integrated
remote backup provider     TBD / NOT ACTIVATED
production/cloud recovery  NOT CLAIMED
```

No AI provider/runtime/control-plane convenience may redefine these contracts.

---

# 4. Current compact roadmap

```text
AI-00 COMPLETE
AI-01 COMPLETE
AI-02 CLOSED / STRUCTURALLY ACCEPTED
AI-03 CLOSED / STRUCTURALLY ACCEPTED

AI-04 PRODUCTIONIZATION ARCHITECTURE — CURRENT
  AI-04A eval/model/provider/economics
    MATERIALIZED
    direct provider/model evidence DEFERRED UNTIL DECISION-CRITICAL

  AI-04B concrete runtime/capabilities
    CLOSED / STRUCTURALLY ACCEPTED / RT-01..RT-31

  AI-04C production assurance/security/privacy/control-plane/operations
    CANDIDATE MATERIALIZED
    first destructive kill-test FAIL
    PA-01..PA-38
    first compound retest PASS CANDIDATE
    fresh independent validation CURRENT

AI-05 WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT — FUTURE
THEN ACTUAL AI IMPLEMENTATION WORKSTREAM(S)
```

---

# 5. AI-04A retained boundary

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY
DANTE FEATURE/BUSINESS CODE != CONCRETE PROVIDER SDK
PROVIDER REPLACEABLE != PROVIDERS IDENTICAL
```

```text
DANTE need
→ ModelTarget
→ HarnessProfile
→ ProviderBinding
→ ProviderAdapter
→ qualified serving platform/model/deployment/feature mode
```

DANTE owns eval semantics. Hard semantic/privacy/safety failure cannot be averaged away.

Commercial boundary:

```text
COMMERCIAL SUBSCRIPTION / SERVICE TIER != DANTE DOMAIN Plan
COMMERCIAL TIER != MODEL / PROVIDER / DEPLOYMENT
```

No provider/model/default or tier names/prices/quotas are selected.

---

# 6. AI-04B retained runtime truth

AI-04B is CLOSED / STRUCTURALLY ACCEPTED / RT-01..RT-31.

Key separations:

```text
RUN != MODEL INVOCATION != PROVIDER ATTEMPT
RAW PROVIDER EVENT != DANTE RUNTIME EVENT != PUBLICATION EVENT
CANCEL REQUESTED != CANCEL CONFIRMED != EXECUTION QUIESCED
PROVIDER BACKGROUND != DANTE DURABLE EXECUTION
PROVIDER CONTINUATION != DANTE SESSION/CONTEXT/MEMORY
CONTINUATION HANDLE != CURRENT HARNESS/POLICY/TOOLS
PROVIDER CALL ID != DANTE SEMANTIC IDEMPOTENCY ID
FROZEN CONFIG != PERPETUAL CURRENT AUTHORIZATION
PUBLISHED DELTA = EXTERNALIZATION
REMOTE CALLBACK != CURRENT RUN ELIGIBILITY
ATTACHED CHILD != DETACHED CHILD
BUDGET ADMISSION != FINAL METERED COST
MCP INPUT_REQUIRED/AUTO-FULFIL != USER INPUT/CONSENT/APPROVAL
```

Accepted durability remains:

```text
Class A → PostgreSQL transactional outbox + bounded worker
Class B → Restate selected / dormant until first real qualifying consumer
```

---

# 7. AI-04C durable authority

```text
docs/architecture/dante-ai-04c-production-assurance-control-plane-operations.md
```

Current chronology:

```text
2026 state-of-the-art research COMPLETE ENOUGH
→ candidate BUILT
→ first destructive kill-test FAIL
→ PA-01..PA-38
→ first compound retest PASS CANDIDATE
→ fresh independent validation CURRENT
```

Public pattern sources included Microsoft 365 Copilot, Notion, Slack, GitHub Copilot, Salesforce Trust Layer, Azure AI Gateway/API Management, AWS Bedrock Guardrails, Google Model Armor, OpenTelemetry, guarded rollout systems and Google SRE.

These are evidence/pattern sources only; DANTE has not selected those technologies.

---

# 8. AI-04C core architecture

```text
CONTROL PLANE
→ qualification / eligibility
→ Harness/security/routing/budget/environment policy
→ rollout / kill switches / requalification

RUNTIME DATA PLANE
→ admission
→ current Authority/AuthZ/Consent/Visibility
→ current provider/data/feature eligibility
→ budget reservation
→ Context/Egress PEP
→ Model Access Runtime
→ Capability/Effect PEP
→ verification/reconciliation
→ Safe Publication
→ usage settlement
```

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

New provider/model/material feature mode defaults to inactive until qualified and rolled out.

---

# 9. AI-04C config/security/credential boundaries

```text
ACTIVE POINTER != IMMUTABLE CONFIG REVISION
CONTROL-PLANE WRITE = PRIVILEGED SECURITY CAPABILITY
CONTROL-PLANE OUTAGE != UNBOUNDED ALLOW
KILL NEW WORK != ABANDON RECONCILIATION
GUARDRAIL RESULT != DANTE AUTHORITY
SECURITY SERVICE AVAILABLE != ELIGIBLE DATA RECIPIENT
MASKING/REDACTION != SEMANTIC EQUIVALENCE
SECRETS != RUNTIME CONFIG
ADMIN CREDENTIAL != INFERENCE CREDENTIAL != DELEGATED USER CREDENTIAL
MODEL/SANDBOX gets no broad high-value credentials
```

Workload identity / short-lived credentials are preferred where supported.

No gateway/guardrail/flag/KMS product is selected.

---

# 10. AI-04C evidence/budget/SRE boundaries

```text
TELEMETRY != AUDIT != EVAL EVIDENCE != CANONICAL TRUTH
FULL PROMPT/RESPONSE/CONTEXT TELEMETRY = OFF BY DEFAULT
COMMERCIAL CREDIT != PROVIDER TOKEN != ACTUAL PROVIDER COST
ADMISSION ESTIMATE != RESERVATION != SETTLEMENT
COMMERCIAL QUOTA != ABUSE RATE LIMIT != PROVIDER QUOTA != PLATFORM CAPACITY
```

Shared budget admission requires an atomic authority boundary.

Commercial exhaustion cannot starve reconciliation/security cleanup.

Retry budgets prevent multiplicative hidden retries.

Graceful degradation may reduce optional resource use but not safety/privacy/semantic floors.

DANTE SLOs measure user-safe DANTE outcomes, not raw provider uptime.

Privacy/security hard failures are incidents, not ordinary error-budget consumption.

---

# 11. AI-04C rollout/requalification boundaries

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
```

Shadow traffic is real disclosure and must be independently eligible.

Shadow/canary work cannot dispatch uncontrolled consequential effects.

Config rollback affects future routing; it does not undo existing effects.

Provider/subprocessor/retention/residency/model/guard/Harness material changes trigger risk-proportionate requalification.

Feedback/model-improvement sharing is separate from normal telemetry/eval.

---

# 12. PA-01..PA-38 compact summary

```text
Authority reuse / no AI permission widening
qualification/eligibility/availability/entitlement intersection
feature-mode + retention/residency/processor eligibility
new capability default-off
versioned control plane / privileged writes / fail-safe outage
kill-switch reconciliation survival
non-bypassable provider/capability/effect/egress controls
guardrail authority/data-recipient/version separation
instruction lineage / masking semantic limits
credential class separation / workload identity
telemetry-audit-eval-canonical separation
content telemetry default-off
commercial credit-token-cost separation
admission-reservation-settlement
atomic shared-budget admission
quota/rate/provider/platform distinctions
retry budgets
protected reconciliation capacity
graceful-degradation safety floors
shadow disclosure/effect isolation
rollback != effect undo
user-safe SLOs / hard incident semantics
provider/subprocessor requalification
privacy-minimal rollout targeting
feedback/model-improvement separation
```

Full normative wording is in the AI-04C durable document.

---

# 13. Exact current action

```text
AI-04C — FRESH INDEPENDENT DESTRUCTIVE PRODUCTION-ASSURANCE VALIDATION
```

Pressure at least:

```text
control-plane stale/read partition/tamper
control-plane authorization escalation
configuration integrity/signing assumptions
kill-switch race with in-flight work
provider/data eligibility cache drift
credential rotation + secret-manager outage
security scanner false positive/negative behavior
transformed prompt/tool injection
telemetry cardinality/cost/backpressure
required audit durability failure
budget reservation leak / unknown settlement
shared-pool fairness/starvation
retry budget across SDK/gateway/DANTE/Restate
fallback circuit/capacity interaction
shadow/canary privacy + effect isolation
bad automatic rollback
upgrade/downgrade during reservation
all-provider outage + deterministic degraded mode
incident recovery + requalification
```

If a structural contradiction appears, harden only the smallest affected boundary and rerun the compound set.

Only after AI-04C closure route to AI-04 whole-phase destructive acceptance.

---

# 14. Current non-claims

```text
AI-04 CLOSED                           NO
AI-04B CLOSED                          YES / STRUCTURAL
AI-04C CLOSED                          NO
AI-04C FINAL INDEPENDENT PASS          NO
DIRECT PROVIDER EVAL PASS              NO
PROVIDER SELECTED                      NO
MODEL DEFAULT SELECTED                 NO
PROVIDER SDK SELECTED                  NO
CONTROL-PLANE IMPLEMENTED              NO
AI GATEWAY SELECTED/DEPLOYED           NO
GUARDRAIL PRODUCT SELECTED             NO
SECRET MANAGER/KMS SELECTED            NO
EVAL RUNNER SELECTED                   NO
API CREDENTIALS USED                   NO
PAID API CALL EXECUTED                 NO
COMMERCIAL TIER NAMES/PRICES SET       NO
BILLING/CREDIT SYSTEM IMPLEMENTED      NO
AI BACKEND IMPLEMENTED                 NO
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

# 15. Git write-gate discipline

Before every new remote write:

```text
BRANCH
<exact branch>

PRE-SCOPE
<exact current SHA>

CREATE
<exact paths>

UPDATE
<exact paths>

DELETE
<exact paths>

PURPOSE
<bounded purpose>

EXPLICITLY OUT OF SCOPE
<out of scope>
```

Re-fetch HEAD immediately before first write. If it differs, STOP and re-gate.

After writes compare PRE-SCOPE..HEAD and prove exact path classification/no scope creep.

---

# 16. Handoff lifecycle

This file is temporary and **MUST NOT MERGE TO PROTECTED `main`**.

Before branch integration:

```text
classify meaningful handoff content
→ propagate durable truth/rationale/evidence
→ verify knowledge coverage
→ DELETE THIS FILE
```

Temporary handoff count entering protected main must be zero.