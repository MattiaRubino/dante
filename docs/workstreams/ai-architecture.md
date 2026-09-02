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
- **PRE-AI05:** CLOSED / STRUCTURALLY ACCEPTED / PRE05-H01..H19
- **Current core eval:** DANTE-E01..DANTE-E14
- **AI-05:** ACTIVE / CURRENT
- **AI-05A:** CANDIDATE / FIRST T01..T26 PASS FAIL BOUNDED / BD-31..BD-40 MATERIALIZED / FRESH RETEST REQUIRED
- **Implementation claim:** NONE
- **Provider/model selection:** OPEN / EVIDENCE-DRIVEN
- **Merge status:** UNMERGED

Repository truth outranks conversation memory.

## 1. Current roadmap

```text
AI-00 COMPLETE
AI-01 COMPLETE
AI-02 CLOSED / STRUCTURALLY ACCEPTED
AI-03 CLOSED / STRUCTURALLY ACCEPTED
AI-04 CLOSED / STRUCTURALLY ACCEPTED
PRE-AI05 CLOSED / H01..H19
GLOBAL CURRENT-TRUTH RECONCILIATION COMPLETE

AI-05 ACTIVE / CURRENT
  └ AI-05A WHOLE-SYSTEM BUILD BOUNDARY
       FIRST DESTRUCTIVE PASS FAIL BOUNDED
       BD-31..BD-40 HARDENED
       FRESH RETEST REQUIRED

THEN
AI-05B CONCRETE IMPLEMENTATION BLUEPRINT
→ AI-05 whole-system acceptance/closure
→ actual AI implementation workstream(s)
```

## 2. Mandatory current AI authority

```text
docs/architecture/dante-ai-foundation.md
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

`ai-production-engineering-state-of-the-art-2026.md` remains current research evidence / NON-DANTE-DECISION.
Temporary live handoff MUST NOT merge to protected `main`.

## 3. Retained upstream invariants

```text
PostgreSQL = sole canonical persistence/material-history authority
MODEL OUTPUT != PUBLISHABLE OUTPUT
Interaction Session != Run != Worker
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
RUN-START AUTONOMY != PERPETUAL AUTONOMY
Context != Retrieval != Memory
APPROXIMATE != COMPLETE
DEFAULT NONCANONICAL PERSISTENCE = NO
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
HARNESSPROFILE != PROVIDERBINDING
EVAL CANDIDATE != PRODUCTION ROUTE
ENTITLED != SERVABLE
ATTENTION DECISION != PROACTIVE WORK ADMISSION != EFFECT AUTHORIZATION
SAFE SINGLE DISCLOSURE != SAFE CUMULATIVE DISCLOSURE
RECIPIENT != SURFACE != CHANNEL
SOURCE FUTURE ELIGIBILITY != PRIOR DISCLOSURE OCCURRENCE
```

## 4. AI-05A observed repository baseline

```text
apps/backend/src/dante/
├ bootstrap/
└ platform/

kernel/                  NOT MATERIALIZED
modules/                 NOT MATERIALIZED
provider AI SDK          NONE
tooling/ai-evals         NONE
production AI runtime    NONE
```

AI-05A is an architecture-to-build candidate only.

## 5. AI-05A ownership candidate after first destructive pass

```text
modules/search
→ shared permission/disclosure-aware read/search capability
→ deterministic structured/search path
→ bounded cross-capability read projection
→ DOES NOT own searched canonical semantics or mutations

modules/intelligence
→ DANTE intelligence application/orchestration semantics
→ consumes Search/public capabilities
→ provider-neutral Work/Context/routing/verification/publication

provider SDK/protocol
→ private outbound adapter behind DANTE-owned ModelAccessPort

resource/commercial authority
→ owns applicable shared/commercial quota/metering truth
→ Intelligence consumes admission/reservation/settlement boundary

platform
→ shared technical mechanics only

bootstrap
→ composition/lifecycle

tooling/ai-evals
→ direct eval tooling outside ordinary runtime
```

## 6. First destructive pass findings

```text
T01 FAIL BOUNDED → Search separated from Intelligence / god-module pressure
T03 FAIL BOUNDED → explicit Search cross-capability read projection
T04 FAIL BOUNDED → deterministic Search independent of model runtime
T06 FAIL BOUNDED → behavior config / snapshot / lifecycle hardening
T08 FAIL BOUNDED → fake model != adapter conformance != direct qualification
T13 FAIL BOUNDED → explicit resource admission/settlement ownership
T14 FAIL BOUNDED → zero-persistence envelope must gate H19 cases
T17 FAIL BOUNDED under original ownership → deterministic Search restores outage independence
```

Other T-cases were PASS candidates or only PASS within the explicit first-vertical envelope. Any FAIL prevented closure.

## 7. BD-31..BD-40 hardening

```text
BD-31 Global Search != Intelligence orchestration.
BD-32 Search may own bounded cross-capability read projection, not canonical semantics/mutation.
BD-33 Deterministic Search independent of model/provider route availability.
BD-34 Resource admission/reservation/settlement is explicit consumed boundary; Intelligence does not own ledger truth.
BD-35 Behavior-bearing route/Harness/policy config != scattered env variables.
BD-36 Static-first config still needs immutable revision, approved active selection, coherent invocation snapshot and emergency deny before production.
BD-37 Zero-persistence first vertical limited to inline/single-turn/private-in-app/read-only envelope.
BD-38 H19/durable-audit/resume/background needs gate expansion until minimum state exists.
BD-39 Application fake != provider adapter conformance != direct eval != production capacity proof.
BD-40 Chat-like UI / inline stream != generic conversation or Run persistence required.
```

## 8. First vertical candidate

```text
GLOBAL SEARCH
→ deterministic shared read/search capability
→ canonical navigation + source/currentness

ASK DANTE
→ optional governed model-assisted synthesis over Search/public capability results
→ source/provenance/currentness
→ no consequential mutation
```

Initial envelope:

```text
private authenticated in-app
single-turn
inline/request-owned
read-only
normal isolation
no background/durable resume
no shared/lock/voice/external recipient
no case requiring H19 durable prior-exposure accounting
```

No new generic AI table is justified by this envelope.

## 9. Open decisions / non-claims

```text
AI-05A PASS/CLOSED                     NO
modules/search implemented             NO
modules/intelligence implemented       NO
provider/model/SDK selected            NO
direct provider eval                   NO
stream transport selected              NO
new PostgreSQL/Alembic change          NO
new AI table/index                     NO
FTS/vector/pgvector activation         NO
conversation persistence               NO
control-plane persistence              NO
commercial/resource ledger             NO
Restate/R2/MCP/A2A activation          NO
Execution Environment                  NO
```

## 10. Current exact action

```text
READ BACK HARDENED AI-05A
→ restart T01..T26 from zero
→ run compound Search/Intelligence/outage/hidden-result/config/resource/disclosure cases
→ reverse-check AI-05A → AI-04 → PRE-AI05 → AI-03 → AI-02
→ harden only demonstrated gaps
```

No AI-05A closure before a clean fresh retest.

## 11. Handoff policy

Temporary live handoff must be deleted before protected-main integration.