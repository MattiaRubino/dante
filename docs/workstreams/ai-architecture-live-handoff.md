# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Current phase:** AI-05A — WHOLE-SYSTEM BUILD BOUNDARY / OWNERSHIP MAP
- **Global current-truth reconciliation:** COMPLETE / QA PASS
- **AI-02.1 / AI-03 / AI-04:** CLOSED / STRUCTURALLY ACCEPTED
- **PRE-AI05:** CLOSED / STRUCTURALLY ACCEPTED / PRE05-H01..H19
- **Current core eval families:** DANTE-E01..DANTE-E14
- **AI-05:** ACTIVE / CURRENT
- **AI-05A:** CANDIDATE / BD-01..BD-30 / T01..T26 PENDING
- **Implementation:** NONE
- **Provider/model/SDK:** OPEN
- **Refreshed:** 2026-09-02
- **Current branch HEAD:** FETCH LIVE before every write

Repository truth outranks this temporary handoff.

## 1. Resume sequence

```text
feature/ai-architecture
→ AI-02 / AI-03 / AI-04 CLOSED
→ PRE-AI05 H01..H19 CLOSED
→ global current-truth reconciliation COMPLETE
→ AI-05 CURRENT
→ AI-05A candidate materialized
→ run T01..T26 destructive buildability/minimality tests
→ harden smallest demonstrated gaps
→ close AI-05A only after clean retest
→ then AI-05B concrete implementation blueprint
```

Do not restart upstream architecture without concrete contradictory evidence.

## 2. Current AI-05A authority

`docs/architecture/dante-ai-05a-whole-system-build-boundary.md`

Observed repository baseline:

```text
apps/backend/src/dante/
├ bootstrap/
└ platform/

kernel/                 not materialized
modules/                not materialized
provider AI SDK         none
tooling/ai-evals        none
AI runtime              none
```

Candidate ownership:

```text
modules/intelligence
→ DANTE intelligence application/orchestration semantics

provider SDK/protocol
→ private outbound adapter behind DANTE-owned ModelAccessPort

platform
→ shared technical mechanics only

bootstrap
→ composition/lifecycle

tooling/ai-evals
→ direct eval tooling outside ordinary runtime
```

No folder is claimed implemented merely because the blueprint names it.

## 3. Current first-vertical candidate

```text
GLOBAL SEARCH / ASK DANTE
READ-ONLY
+ CANONICAL NAVIGATION
+ SOURCE / PROVENANCE / CURRENTNESS
+ DETERMINISTIC FAST PATH
+ MODEL-ASSISTED PATH WHERE NEEDED

NO CONSEQUENTIAL MUTATION
NO GENERIC CONVERSATION PERSISTENCE
NO VECTOR/FTS ACTIVATION BY DEFAULT
NO BACKGROUND AGENT
```

Product basis: Global Search and Command is an accepted shared product capability; natural language never bypasses backend validation and missing records must not be fabricated.

## 4. Persistence posture

```text
DEFAULT NONCANONICAL AI PERSISTENCE = NO
```

Initial candidate expects first read-only vertical to add **zero new AI tables** unless destructive acceptance proves a real evidence/survival requirement.

Runtime contracts such as WorkContract, ContextPlan, ContextFragment, ConsumerContext and inline Run state remain ephemeral by default. Provider/Harness/Binding definitions start as static/versioned typed control configuration. Dynamic control-plane persistence is trigger-gated.

## 5. Provider/control posture

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
HARNESSPROFILE != PROVIDERBINDING
EVAL CANDIDATE != PRODUCTION ROUTE
```

Current implementation candidate prefers thin native provider adapters and one primary provider if direct DANTE evidence later supports it. No gateway/framework is selected merely to prepare for hypothetical multi-provider use.

## 6. Destructive test focus

Run all `T01..T26` from AI-05A, including:

```text
god-module risk
module vs platform vs kernel ownership
raw business-table bypass pressure
no-model fast path
one-provider simplicity vs future replaceability
static config vs hidden env business logic
zero-new-persistence claim
stream/cancel/Run-registry pressure
conversation persistence pressure
commercial entitlement ownership
cumulative-disclosure accounting need
sensitive/shared surface scope
provider outage
planning/Scenario persistence
future effect reuse of owning application use cases
eval artifact home
observability privacy
voice/MCP/A2A/background extensibility
architecture import enforcement
noun→table/service overmaterialization
```

## 7. Closed upstream truth

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

## 8. Current non-claims

```text
AI-05A PASS/CLOSED                NO
modules/intelligence IMPLEMENTED  NO
provider/model/SDK selected       NO
direct provider eval              NO
stream transport selected         NO
new PostgreSQL/Alembic change     NO
new AI table/index                NO
conversation persistence          NO
control-plane persistence         NO
FTS/vector/pgvector activation    NO
Restate/R2/MCP/A2A activation     NO
Execution Environment selected    NO
commercial billing                NO
```

## 9. Git discipline

Before every remote write: exact BRANCH / PRE-SCOPE / CREATE / UPDATE / DELETE / PURPOSE / OUT-OF-SCOPE gate, then refetch HEAD. After writes compare PRE-SCOPE..HEAD and prove path scope.

## 10. Handoff lifecycle

This file is temporary and MUST NOT merge to protected `main`. Before integration: propagate durable truth → verify coverage → DELETE this file.