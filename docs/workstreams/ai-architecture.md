# DANTE AI Architecture Workstream

- **Status:** ACTIVE / BRANCH-LOCAL DURABLE WORKSTREAM RECORD
- **Branch:** `feature/ai-architecture`
- **Current phase:** AI-05B — CONCRETE IMPLEMENTATION BLUEPRINT
- **Global current-truth reconciliation:** COMPLETE / QA PASS
- **AI-02.1:** CLOSED / STRUCTURALLY ACCEPTED
- **AI-03:** CLOSED / STRUCTURALLY ACCEPTED / C01..C33 / B01..B35 / MAT-01..MAT-15
- **AI-04:** CLOSED / STRUCTURALLY ACCEPTED
- **AI-04A:** CLOSED / A01..A30 / EV01..EV20 / DIRECT PROVIDER EVIDENCE NOT EXECUTED
- **AI-04B:** CLOSED / RT-01..RT-31
- **AI-04C:** CLOSED / PA-01..PA-61
- **AI-04 whole-phase:** CLOSED / WP-01..WP-22
- **PRE-AI05:** CLOSED / STRUCTURALLY ACCEPTED / PRE05-H01..H19
- **AI-05A:** CLOSED / STRUCTURALLY ACCEPTED / BD-01..BD-41
- **Current core eval:** DANTE-E01..DANTE-E14
- **AI-05:** ACTIVE / CURRENT
- **AI-05B:** ACTIVE / CURRENT NEXT SUB-PHASE / SUBSTANTIVE DESIGN NOT YET MATERIALIZED
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
  ├ AI-05A WHOLE-SYSTEM BUILD BOUNDARY
  │    CLOSED / STRUCTURALLY ACCEPTED / BD-01..BD-41
  │
  └ AI-05B CONCRETE IMPLEMENTATION BLUEPRINT
       CURRENT / NEXT SUB-PHASE
       substantive blueprint not yet materialized

THEN
AI-05 whole-system destructive acceptance / closure
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
docs/architecture/dante-ai-05a-eval-production-composition-hardening.md
docs/architecture/dante-ai-05a-whole-system-build-boundary-acceptance.md
```

Current AI-05A status is owned by the acceptance document. The original candidate and BD-41 supplement remain truthful pre-closure evidence.

`ai-production-engineering-state-of-the-art-2026.md` remains research evidence / NON-DANTE-DECISION.
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

## 4. AI-05A accepted ownership map

```text
modules/search
→ separate Global Search / discovery capability
→ deterministic/no-model capable
→ bounded permission/disclosure/current/history/source read projection
→ no canonical business ownership / no mutation authority

modules/intelligence
→ DANTE intelligence application/orchestration boundary
→ Work/Context/route/model-assisted orchestration/verification/publication
→ consumes Search and owning capability public seams

provider SDK/protocol
→ private outbound adapter behind DANTE-owned ModelAccessPort

resource/commercial authority
→ owns shared/commercial quota/metering truth when activated
→ Intelligence consumes admission/reservation/settlement

bootstrap
→ composition/lifecycle only

platform
→ genuinely shared technical mechanics only

tooling/ai-evals
→ outside ordinary production request path
→ qualification uses same material production composition or independently qualifies material deltas
```

## 5. AI-05A final hardening / acceptance

Accepted build invariants are `BD-01..BD-41`.

Key late hardenings:

```text
BD-31 Global Search != Intelligence orchestration.
BD-32 Search may own bounded cross-capability read projection, not canonical semantics/mutation.
BD-33 Deterministic Search independent of model/provider route availability.
BD-34 Resource admission/reservation/settlement explicit; Intelligence does not own ledger truth.
BD-35 Behavior-bearing route/Harness/policy config != scattered env variables.
BD-36 Static-first config still needs immutable revision, approved active selection, coherent invocation snapshot and emergency deny before production.
BD-37 First zero-persistence envelope = inline/single-turn/private-in-app/read-only.
BD-38 H19/audit/resume/background durability gates expansion until minimum justified state exists.
BD-39 Application fake != provider adapter conformance != direct eval != production capacity proof.
BD-40 Chat-like UI / inline stream != generic conversation or Run persistence required.
BD-41 Qualification evidence must exercise the same material production composition or independently qualify every material delta before promotion.
```

Final acceptance evidence:

```text
T01..T26                                      PASS / 26 OF 26
Search + Intelligence + provider outage       PASS
Search hidden-result + Ask synthesis          PASS
config rollout + invocation + emergency deny  PASS
quota + retry/failover + settlement            PASS
inline stream + disconnect / no durable Run   PASS
cumulative privacy + zero-persistence gate     PASS
direct eval + production composition/deltas    PASS
reverse AI-05A→04→PRE05→03→02                 PASS
```

## 6. First vertical accepted direction

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

## 7. Evidence planes remain separate

```text
APPLICATION FAKE
!= PROVIDER ADAPTER CONFORMANCE
!= LIVE PROVIDER SMOKE / COMPATIBILITY PROOF
!= DIRECT DANTE MODEL/ROUTE EVAL
!= PRODUCTION CAPACITY QUALIFICATION
```

Qualification evidence must identify the exact material route composition it supports and any separately qualified material delta.

## 8. AI-05B exact scope

AI-05B must translate the accepted AI-05A ownership map into concrete build contracts without starting implementation.

It must freeze, as far as architecture evidence permits:

```text
module public boundaries
ports + runtime DTO/types
Search read/query contracts
ModelAccessPort contract
provider adapter conformance contract
route/config artifact schemas
resource admission/settlement seams
HTTP + streaming/publication shape for first vertical
runtime-only vs evidence/persistence ownership
exact unit/integration/eval/system test layout
qualification artifact schema + promotion evidence
feature/activation gates
implementation dependency graph
first build gates / commit sequence
```

Provider/model/SDK selection remains direct-evidence gated. If a concrete selection cannot be made responsibly without API evidence, AI-05B must specify the exact proof gate rather than guess.

## 9. Open decisions / non-claims

```text
AI-05A PASS/CLOSED                     YES / STRUCTURAL
AI-05 WHOLE PHASE CLOSED               NO
AI-05B SUBSTANTIVE BLUEPRINT           NOT YET MATERIALIZED
modules/search implemented             NO
modules/intelligence implemented       NO
provider/model/SDK selected            NO
direct provider eval                   NO
production capacity qualification      NO
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
AI-05B
→ inspect accepted AI-05A ownership + first-vertical envelope
→ define concrete module public APIs / ports / DTO/runtime types
→ define Search query/read contracts
→ define ModelAccessPort + provider adapter conformance contract
→ define route/config artifact schemas and resource-control seams
→ decide simplest first-vertical HTTP/streaming shape
→ classify exact runtime/evidence/persistence state
→ define qualification artifacts + test topology
→ produce implementation dependency graph and build gates
→ destructively test AI-05B before whole AI-05 closure
```

Do not start provider/backend implementation simply because AI-05A is closed.

## 11. Handoff policy

Temporary live handoff must be deleted before protected-main integration.