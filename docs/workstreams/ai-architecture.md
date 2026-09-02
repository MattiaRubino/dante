# DANTE AI Architecture Workstream

- **Status:** ACTIVE / BRANCH-LOCAL DURABLE WORKSTREAM RECORD
- **Branch:** `feature/ai-architecture`
- **Current phase:** AI-05A — WHOLE-SYSTEM BUILD BOUNDARY / OWNERSHIP MAP
- **Global current-truth reconciliation:** COMPLETE / QA PASS
- **AI-02.1:** CLOSED / STRUCTURALLY ACCEPTED
- **AI-03:** CLOSED / STRUCTURALLY ACCEPTED / C01..C33 / B01..B35 / MAT-01..MAT-15
- **AI-04:** CLOSED / STRUCTURALLY ACCEPTED
- **AI-04A:** CLOSED / A01..A30 / EV01..EV20 / DIRECT PROVIDER EVIDENCE NOT EXECUTED
- **AI-04B:** CLOSED / RT-01..RT-31
- **AI-04C:** CLOSED / PA-01..PA-61
- **AI-04 whole-phase:** CLOSED / WP-01..WP-22
- **PRE-AI05 hardening:** CLOSED / STRUCTURALLY ACCEPTED / PRE05-H01..H19
- **Current core eval families:** DANTE-E01..DANTE-E14
- **AI-05:** ACTIVE / CURRENT / FINAL ARCHITECTURE-TO-BUILD BOUNDARY
- **AI-05A:** CANDIDATE / BD-01..BD-30 / DESTRUCTIVE ACCEPTANCE PENDING
- **Implementation claim:** NONE
- **Provider/model selection:** OPEN / EVIDENCE-DRIVEN
- **Commercial packaging:** OPEN / ENTITLEMENT BOUNDARY ONLY
- **Merge status:** UNMERGED

Repository truth outranks conversation memory.

## 1. Roadmap

```text
AI-00 COMPLETE
AI-01 COMPLETE
AI-02 CLOSED / STRUCTURALLY ACCEPTED
AI-03 CLOSED / STRUCTURALLY ACCEPTED
AI-04 CLOSED / STRUCTURALLY ACCEPTED
PRE-AI05 CLOSED / H01..H19
GLOBAL CURRENT-TRUTH RECONCILIATION COMPLETE / QA PASS

AI-05 ACTIVE / CURRENT
  └ AI-05A WHOLE-SYSTEM BUILD BOUNDARY
    CANDIDATE / DESTRUCTIVE ACCEPTANCE PENDING

THEN
AI-05B CONCRETE IMPLEMENTATION BLUEPRINT
→ AI-05 whole-system acceptance/closure
→ actual AI implementation workstream(s)
```

The AI-05A/AI-05B labels are internal decomposition of the already-current AI-05 macro-phase; they do not add implementation claims.

## 2. Mandatory AI authority

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
docs/architecture/dante-ai-04-whole-phase-destructive-acceptance.md
docs/architecture/dante-ai-pre05-cross-phase-hardening.md
docs/architecture/dante-ai-05a-whole-system-build-boundary.md
```

Temporary live handoff MUST NOT merge to protected `main`.

## 3. Retained semantic/runtime invariants

```text
PostgreSQL = sole canonical persistence/material-history authority
MODEL OUTPUT != PUBLISHABLE OUTPUT
Interaction Session != Run != Worker
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
RUN-START AUTONOMY != PERPETUAL AUTONOMY
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
Context != Retrieval != Memory
APPROXIMATE != COMPLETE
processing != retention != future reuse
CACHE HIT != CURRENT DISCLOSURE AUTHORIZATION
SAFE SINGLE DISCLOSURE != SAFE CUMULATIVE DISCLOSURE
AUTONOMY != AUTHORITY != AUTHZ != APPROVAL
ATTENTION DECISION != PROACTIVE WORK ADMISSION != EFFECT AUTHORIZATION
RECIPIENT != SURFACE != CHANNEL
SOURCE FUTURE ELIGIBILITY != PRIOR DISCLOSURE OCCURRENCE
```

## 4. Closed upstream AI architecture

```text
AI-03A       C01..C33
AI-03B       B01..B35
AI-03C       MAT-01..MAT-15
AI-04A       A01..A30 / EV01..EV20
AI-04B       RT-01..RT-31
AI-04C       PA-01..PA-61
AI-04 whole  WP-01..WP-22
PRE-AI05     H01..H19
```

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY
HARNESSPROFILE != PROVIDERBINDING
EVAL CANDIDATE != PRODUCTION ROUTE
ENTITLED != SERVABLE
```

## 5. Current eval contract

```text
E01 deterministic/model avoidance
E02 target resolution
E03 extraction
E04 query/history/absence
E05 context/privacy/Reality Scope/cumulative disclosure
E06 planning/replanning/scenario
E07 document/long-context/multimodal
E08 tool/capability use
E09 consequential effect/scoped autonomy
E10 multi-actor/delegation/surface disclosure
E11 adaptive memory/learning
E12 failure/currentness/supersession/failover
E13 open-world research/grounding
E14 proactivity/Attention/causal-loop/notification truth
```

Hard failures remain non-averageable.

## 6. PRE-AI05 acceptance evidence

```text
fresh full AI-01→AI-04 + H01..H19 retest     PASS / 26 OF 26
compound collision retest                    PASS
reverse PRE05→04→03→02→01                   PASS
refreshed 2026 state-of-the-art regression   PASS
global current-truth reconciliation          PASS / exact current-doc scope
```

Structural/documentation evidence only; no provider/runtime/product-capacity proof.

## 7. AI-05A build-boundary candidate

Durable candidate:

`docs/architecture/dante-ai-05a-whole-system-build-boundary.md`

Current thesis:

```text
capability-first modular monolith remains
modules/intelligence = candidate DANTE intelligence application/orchestration owner
provider SDKs = outbound adapters behind DANTE-owned port
bootstrap = concrete wiring/lifecycle
platform = shared technical mechanics only
tooling/ai-evals = direct eval boundary, outside ordinary runtime
kernel = no AI-specific promotion without proven stable cross-capability value
DEFAULT NONCANONICAL AI PERSISTENCE = NO
```

Current first-vertical candidate:

```text
GLOBAL SEARCH / ASK DANTE
READ-ONLY + CANONICAL NAVIGATION + PROVENANCE
NO CONSEQUENTIAL MUTATION
```

This remains a candidate until destructive acceptance passes.

## 8. Commercial boundary

```text
COMMERCIAL SUBSCRIPTION / SERVICE TIER != DANTE DOMAIN Plan
```

Commercial tiers can bound compute/concurrency/capability envelopes but cannot weaken truth, privacy, Authority, target safety, provider/data eligibility, reconciliation, scoped autonomy, Attention or disclosure floors. Names/prices/quotas remain OPEN.

## 9. Direct proof obligations remain distinct

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

Concrete provider/model direct DANTE eval and production-capacity qualification remain unexecuted.

## 10. Current exact action

```text
READ BACK AI-05A CANDIDATE
→ run T01..T26 destructive buildability/minimality tests
→ reverse-check against AI-04/PRE-AI05/AI-03/AI-02
→ pressure-test first-vertical zero-persistence claim
→ pressure-test module/platform/kernel ownership
→ pressure-test provider adapter + static-control-config posture
→ harden only demonstrated gaps
```

No AI-05A PASS claim exists before that retest.

## 11. Open decisions

Provider/model/SDK/eval runner, exact ModelAccessPort/API classes, streaming transport, concrete runtime implementation, Attention implementation, cumulative-disclosure mechanism/storage, formal IFC/leakage-budget/ACS adoption, dynamic control-plane topology, commercial packaging/billing, gateway/security products, MCP/A2A, Execution Environment, Restate/R2/vector/search activation and production-region mappings remain evidence-gated.

AI-05A may constrain ownership; AI-05B may freeze implementation contracts. Neither may fabricate direct provider/prod evidence.

## 12. Handoff policy

Temporary live handoff must be deleted before protected-main integration.