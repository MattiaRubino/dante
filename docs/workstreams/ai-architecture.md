# DANTE AI Architecture Workstream

- **Status:** ACTIVE / BRANCH-LOCAL DURABLE WORKSTREAM RECORD
- **Branch:** `feature/ai-architecture`
- **Current phase:** PRE-AI05 CROSS-PHASE HARDENING + WHOLE-CHAIN RETEST
- **AI-02.1:** CLOSED / STRUCTURALLY ACCEPTED
- **AI-03:** CLOSED / STRUCTURALLY ACCEPTED / C01..C33 / B01..B35 / MAT-01..MAT-15
- **AI-04:** CLOSED / STRUCTURALLY ACCEPTED
- **AI-04A:** CLOSED / A01..A30 / EV01..EV20 / DIRECT PROVIDER EVIDENCE NOT EXECUTED
- **AI-04B:** CLOSED / RT-01..RT-31
- **AI-04C:** CLOSED / PA-01..PA-61
- **AI-04 whole-phase:** CLOSED / WP-01..WP-22
- **PRE-AI05 hardening:** CANDIDATE / PRE05-H01..H19
- **Retest history:** first FAIL bounded → H15-H16; second full FAIL bounded → H17-H18; third full FAIL bounded → H19
- **Fresh retest after H19:** NOT YET EXECUTED
- **AI-05:** FUTURE / NEXT ONLY AFTER PRE-AI05 PASS + CURRENT-TRUTH RECONCILIATION
- **Implementation claim:** NONE
- **Provider/model selection:** OPEN / EVIDENCE-DRIVEN
- **Commercial packaging:** OPEN / ENTITLEMENT BOUNDARY ONLY
- **Merge status:** UNMERGED

Repository truth outranks conversation memory.

## 1. Roadmap

```text
AI-00 COMPLETE
AI-01 COMPLETE
AI-02 CLOSED
AI-03 CLOSED
AI-04 CLOSED STRUCTURALLY

CURRENT
PRE-AI05 CROSS-PHASE HARDENING + WHOLE-CHAIN RETEST
  H01..H19 candidate
  fresh retest required

IF PASS
GLOBAL CURRENT-TRUTH RECONCILIATION
→ AI-05 Whole-System Acceptance + Implementation Blueprint
→ actual AI implementation workstream(s)
```

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
```

Temporary live handoff MUST NOT merge to protected `main`.

## 3. Retained invariants

```text
PostgreSQL = sole canonical persistence/material-history authority
MODEL OUTPUT != PUBLISHABLE OUTPUT
Interaction Session != Run != Worker
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
Context != Retrieval != Memory
APPROXIMATE != COMPLETE
processing != retention != future reuse
CACHE HIT != CURRENT DISCLOSURE AUTHORIZATION
SAFE SINGLE DISCLOSURE != SAFE CUMULATIVE DISCLOSURE
AUTONOMY != AUTHORITY != AUTHZ != APPROVAL
```

AI-02 also owns Attention, causal-loop safety, surface-aware disclosure and communication-state integrity.

## 4. AI-04 closure truth

```text
AI-04A  DANTE-E01..E13 / A01..A30 / EV01..EV20
AI-04B  RT-01..RT-31
AI-04C  PA-01..PA-61
WHOLE   WP-01..WP-22
```

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY
HARNESSPROFILE != PROVIDERBINDING
EVAL CANDIDATE != PRODUCTION ROUTE
ENTITLED != SERVABLE
```

## 5. PRE05-H01..H19 candidate

```text
H01 AttentionBudget != ResourceBudget != commercial/provider quota
H02 trigger fired != material change/current work eligibility
H03 causal-loop / oscillation safety is production-critical
H04 DANTE-E14 proactive/Attention/loop safety is core eval
H05 cumulative disclosure may span related work
H06 recipient != surface != channel
H07 scoped autonomy is policy ceiling, not Authority/AuthZ/approval
H08 unsafe autonomy and excessive over-asking are graded separately
H09 current-tree executable eval coverage E01..E14
H10 AI-01 old ModelTarget shorthand is historical terminology
H11 WP route composition outranks older AI-04B local sequence
H12 old pre-Physical AI/context boundary is historical in current navigation
H13 formal IFC/leakage-budget/ACS mechanisms remain challengers
H14 commercial tier cannot buy weaker attention/autonomy/privacy safety
H15 AttentionDecision != proactive Work Admission != Effect authorization
H16 cumulative disclosure may span Runs/Interactions/surfaces/known related sinks
H17 RUN-START AUTONOMY != PERPETUAL AUTONOMY
H18 Attention/Notify decision != SENT != DELIVERED != SEEN != ACKNOWLEDGED != ACCEPTED
H19 SOURCE CONTENT/LIFECYCLE != PRIOR DISCLOSURE OCCURRENCE; minimum prior-exposure safety state has independent purpose/lifecycle and cannot resurrect source content
```

No PRE-AI05 PASS claim yet.

## 6. Current eval contract

```text
E01 deterministic/model avoidance
E02 target resolution
E03 extraction
E04 query/history/absence
E05 context/privacy/cumulative disclosure
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

## 7. Commercial boundary

```text
COMMERCIAL SUBSCRIPTION / SERVICE TIER != DANTE DOMAIN Plan
```

Commercial tiers cannot weaken truth, privacy, Authority, target safety, provider/data eligibility, reconciliation, scoped autonomy, attention or disclosure floors. Names/prices/quotas remain OPEN.

## 8. Direct proof obligations remain distinct

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

## 9. Current exact action

```text
READ BACK H19
→ RESTART FULL AI-01→AI-04 DESTRUCTIVE RETEST FROM ZERO
→ reverse-order retest
→ refreshed state-of-the-art regression check
```

Special compound pressure includes privacy + prior disclosure + source deletion + stale cache/restore + new Run, with prior-exposure accounting allowed only as minimum non-content security state under independent purpose/lifecycle.

If PASS: mark PRE-AI05 accepted → global current-truth reconciliation → AI-05 current.
If FAIL: reopen only the smallest affected boundary.

## 10. Open decisions

Provider/model/SDK/eval runner, concrete implementation, Attention implementation, cumulative-disclosure mechanism/storage, formal IFC/leakage-budget/ACS adoption, control-plane topology, commercial packaging/billing, gateway/security products, MCP/A2A, Execution Environment, Restate/R2/vector/search activation and production region mappings remain evidence-gated.

## 11. Handoff policy

Temporary live handoff must be deleted before protected-main integration.