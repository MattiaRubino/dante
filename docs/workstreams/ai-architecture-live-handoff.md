# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Workstream:** DANTE AI architecture
- **Current phase:** PRE-AI05 CROSS-PHASE HARDENING + WHOLE-CHAIN RETEST
- **AI-04 overall:** CLOSED / STRUCTURALLY ACCEPTED
- **AI-04A:** CLOSED / A01..A30 / EV01..EV20 / DIRECT PROVIDER EVIDENCE NOT EXECUTED
- **AI-04B:** CLOSED / RT-01..RT-31
- **AI-04C:** CLOSED / PA-01..PA-61
- **AI-04 whole-phase:** CLOSED / WP-01..WP-22
- **PRE-AI05 hardening:** CANDIDATE / PRE05-H01..H14 / RETEST NOT YET EXECUTED AFTER MATERIALIZATION
- **AI-03 overall:** CLOSED / STRUCTURALLY ACCEPTED
- **AI-05:** NEXT ONLY AFTER PRE-AI05 RETEST + CURRENT-TRUTH RECONCILIATION
- **Refreshed:** 2026-09-02
- **Current branch HEAD:** FETCH LIVE before every write

This file exists only to survive chat/session/context saturation while `feature/ai-architecture` remains active.

Repository truth outranks this handoff.

---

# 1. Resume rule

```text
repository  MattiaRubino/dante
branch      feature/ai-architecture
workstream  DANTE AI architecture
current     PRE-AI05 CROSS-PHASE HARDENING + WHOLE-CHAIN RETEST
next        global current-truth reconciliation if retest PASS
then        AI-05 Whole-System Acceptance + Implementation Blueprint
then        actual AI implementation workstream(s)
```

Closed architecture:

```text
AI-02.1        CLOSED / STRUCTURALLY ACCEPTED
AI-03A         CLOSED / C01..C33
AI-03B         CLOSED / B01..B35
AI-03C         CLOSED / MAT-01..MAT-15
AI-03 overall  CLOSED / STRUCTURALLY ACCEPTED
AI-04A         CLOSED / A01..A30 / EV01..EV20
AI-04B         CLOSED / RT-01..RT-31
AI-04C         CLOSED / PA-01..PA-61
AI-04 whole    CLOSED / WP-01..WP-22
AI-04 overall  CLOSED / STRUCTURALLY ACCEPTED
```

Current bounded candidate:

```text
PRE05-H01..PRE05-H14
```

Do not restart AI-02/03/04 redesign without concrete contradictory downstream evidence.

---

# 2. Mandatory AI authority

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
docs/architecture/dante-ai-pre05-cross-phase-hardening.md   CURRENT CANDIDATE SUPPLEMENT
```

For the current retest, use Product/North Star and accepted Domain/Logical/Physical/PostgreSQL contracts only as semantic/upstream requirements. Do not audit unrelated active branch topology.

---

# 3. Why PRE-AI05 hardening exists

The whole AI-01→AI-04 review found no missing mega-layer and no reason to reopen Context/Memory/Effects/provider/control-plane architecture.

It found bounded downstream traceability gaps around responsibilities already present in AI-02:

```text
proactivity / Attention
AttentionBudget vs ResourceBudget
causal-loop / oscillation guard
cumulative / cross-query disclosure
recipient/surface/channel-aware publication
scoped autonomy vs Authority/AuthZ/approval
current-tree eval detail
historical terminology/authority precedence
```

The materialized candidate is:

```text
docs/architecture/dante-ai-pre05-cross-phase-hardening.md
```

---

# 4. PRE05-H01..H14 compact truth

```text
H01 AttentionBudget != ResourceBudget != commercial/provider quota
H02 trigger fired != material change / current work eligibility
H03 causal-loop / oscillation guard is production-critical
H04 DANTE-E14 proactivity / Attention / causal-loop safety is core eval family
H05 cumulative disclosure is a trajectory property
H06 recipient != surface != channel
H07 autonomy policy != Authority != AuthZ != approval
H08 evaluate unsafe autonomy and unnecessary approval separately
H09 current-tree executable eval detail covers E01..E14
H10 AI-01 old ModelTarget shorthand is superseded terminology
H11 WP route composition outranks older AI-04B local sequence
H12 old pre-Physical AI/context boundary is historical in current navigation
H13 formal IFC / leakage-budget / ACS mechanisms remain challengers
H14 commercial tier cannot buy weaker attention/autonomy/privacy safety
```

No candidate hardening is accepted until post-materialization retest PASS.

---

# 5. Retest requirements

Run from current tree, not conversation memory.

Minimum required composition:

```text
AI-01
→ AI-02 / 02.1
→ AI-03A/B/C
→ AI-04A/B/C
→ AI-04 whole-phase
→ PRE05-H01..H14 candidate
```

Required hostile cases include:

```text
own-effect self-trigger loop
own-effect + genuine later external change
attention storm / quiet hours / urgent exception
sequential privacy inference across safe-looking answers
same recipient across private/lock/shared/voice surfaces
AUTO_WITHIN_SCOPE then Authority/AuthZ revoked
PROPOSE_ONLY despite available mutation capability
stale callback after supersession
provider continuation after Harness/tool/policy change
provider failover with context/capability contraction
memory/cache after deletion/revocation
quota exhausted before/after consequential ambiguity
auxiliary router/verifier/judge as governed recipient
model outage while deterministic route remains valid
```

Required result classes:

```text
PASS
GAP
CONTRADICTION
OVER-ABSTRACTION
INTENTIONAL OPEN GATE
HISTORICAL / SUPERSEDED ONLY
```

Retest PASS requires no unexplained responsibility/authority gap.

---

# 6. State-of-the-art posture used for the hardening

Strong current patterns:

```text
background/event-triggered agents with explicit access + activity/version controls
preview/staging before compound live effects
monitoring that only interrupts on meaningful change
risk-scoped human approval rather than universal approval
per-action least privilege and current authorization
runtime loop/step/cost limits
multi-turn outcome/trajectory/repeated evals
```

Emerging challengers:

```text
formal information-flow control
cross-task private-data flow tracking
posterior/inference-leakage budgets
portable agent-control middleware standards
```

DANTE adopts the responsibility/proof boundary now and keeps implementation technology evidence-gated.

---

# 7. Provider / commercial truth remains unchanged

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY
HARNESSPROFILE != PROVIDERBINDING
COMMERCIAL SUBSCRIPTION / SERVICE TIER != DANTE DOMAIN Plan
COMMERCIAL TIER != MODEL / PROVIDER / DEPLOYMENT
ENTITLED != SERVABLE
```

No provider/model is selected.

No Base/Plus/Pro names, prices or quotas are fixed.

Commercial tiers may not weaken correctness/privacy/Authority/target safety/provider-data eligibility/reconciliation/scoped-autonomy/attention-disclosure floors.

---

# 8. Direct proof obligations remain distinct

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

No implementation or provider PASS may be inferred from the architecture retest.

---

# 9. Current exact action

```text
READ BACK MATERIALIZED PRE05-H01..H14
→ WHOLE AI-01→AI-04 FORWARD DESTRUCTIVE RETEST
→ REVERSE-ORDER RETEST
→ REFRESHED STATE-OF-THE-ART REGRESSION CHECK
```

If PASS:

```text
mark PRE-AI05 hardening accepted
→ reconcile global/current navigation
→ set AI-05 current
```

If FAIL:

```text
reopen only the smallest affected boundary
```

---

# 10. Current non-claims

```text
PRE-AI05 HARDENING MATERIALIZED       YES
PRE-AI05 RETEST PASS                  NO
AI-05 STARTED                         NO
DIRECT PROVIDER EVAL PASS             NO
PROVIDER SELECTED                     NO
MODEL DEFAULT SELECTED                NO
PROVIDER SDK SELECTED                 NO
EVAL RUNNER SELECTED                  NO
API CREDENTIALS USED                  NO
PAID API CALL EXECUTED                NO
PRODUCTION CAPACITY PASS              NO
AI BACKEND IMPLEMENTED                NO
FRONTEND AI IMPLEMENTED               NO
CONTROL PLANE IMPLEMENTED             NO
FORMAL IFC IMPLEMENTED                NO
ATTENTION ENGINE IMPLEMENTED          NO
COMMERCIAL TIER NAMES/PRICES SET      NO
POSTGRESQL/ALEMBIC CHANGED            NO
NEW AI TABLE/INDEX                    NO
PGVECTOR/ANN/FTS ACTIVATED            NO
RESTATE/R2 ACTIVATED                  NO
MCP/A2A ACTIVATED                     NO
EXECUTION ENVIRONMENT IMPLEMENTED     NO
SC/PSV DIRECT PROOFS EXECUTED         NO
```

---

# 11. Git write-gate discipline

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

# 12. Handoff lifecycle

This file is temporary and **MUST NOT MERGE TO PROTECTED `main`**.

Before branch integration:

```text
classify meaningful handoff content
→ propagate durable truth/rationale/evidence
→ verify knowledge coverage
→ DELETE THIS FILE
```

Temporary handoff count entering protected main must be zero.