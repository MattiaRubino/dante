# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Current phase:** AI-05B — CONCRETE IMPLEMENTATION BLUEPRINT
- **AI-05A:** CLOSED / STRUCTURALLY ACCEPTED / BD-01..BD-41
- **Fresh AI-05A retest:** PASS / T01..T26 + compounds + reverse
- **Upstream AI-02/03/04/PRE-AI05:** CLOSED / STRUCTURALLY ACCEPTED
- **Current core eval:** DANTE-E01..DANTE-E14
- **Implementation:** NONE
- **Provider/model/SDK:** OPEN
- **Refreshed:** 2026-09-02
- **Current branch HEAD:** FETCH LIVE before every write

Repository truth outranks this temporary handoff.

## 1. Resume sequence

```text
feature/ai-architecture
→ read docs/architecture/dante-ai-05a-whole-system-build-boundary-acceptance.md
→ treat original AI-05A candidate + BD-41 supplement as pre-closure evidence
→ read current workstream record
→ begin AI-05B concrete implementation blueprint
→ do NOT start production implementation
```

## 2. AI-05A accepted ownership

```text
modules/search
→ separate Global Search / discovery capability
→ deterministic/no-model capable
→ bounded permission/disclosure/current/history/source read projection
→ no canonical ownership / no mutation / no model-SQL

modules/intelligence
→ WorkContract / Context / routing / model-assisted orchestration / verification / publication
→ consumes Search and owning capability public seams

provider SDK
→ private outbound adapter behind DANTE-owned ModelAccessPort

resource/commercial authority
→ shared/commercial quota/metering truth when activated
→ Intelligence consumes admission/reservation/settlement

bootstrap
→ wiring/lifecycle

platform
→ shared technical mechanics only

tooling/ai-evals
→ outside ordinary production request path
→ must qualify same material production composition or independently qualify material deltas
```

## 3. AI-05A late hardening

```text
BD-31 Global Search != Intelligence orchestration.
BD-32 Search cross-capability read projection != canonical owner/mutation.
BD-33 deterministic Search independent of model/provider route availability.
BD-34 resource admission/reservation/settlement explicit; Intelligence does not own ledger truth.
BD-35 behavior-bearing route/Harness/policy config != scattered env variables.
BD-36 static-first config still needs immutable revision, approved active selection, coherent invocation snapshot and emergency deny.
BD-37 first zero-persistence envelope = inline/single-turn/private-in-app/read-only.
BD-38 H19/audit/resume/background durability gates expansion until minimum justified state exists.
BD-39 application fake != provider adapter conformance != direct eval != production capacity proof.
BD-40 chat-like UI / inline stream != generic conversation or Run persistence required.
BD-41 qualification evidence must exercise the same material production composition or independently qualify every material delta before promotion.
```

## 4. Final AI-05A acceptance evidence

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

No new canonical owner, generic persistence root, provider lock-in or upstream reopen was required.

## 5. First vertical envelope

```text
GLOBAL SEARCH
+ ASK DANTE read-only

surface       private authenticated in-app
interaction   single-turn
runtime       inline/request-owned
effect        read-only
isolation     normal
provider      optional for Ask; not required for deterministic Search
background    none
durable resume none
shared/lock/voice/external surfaces none
H19-required cross-Run accounting cases not eligible until minimum state exists
```

## 6. Evidence-plane distinctions

```text
APPLICATION FAKE
!= PROVIDER ADAPTER CONFORMANCE
!= LIVE PROVIDER SMOKE / COMPATIBILITY PROOF
!= DIRECT DANTE MODEL/ROUTE EVAL
!= PRODUCTION CAPACITY QUALIFICATION
```

`tooling/ai-evals` may invoke production-owned route components through a bounded qualification seam; production code must never depend on eval tooling.

## 7. AI-05B exact next work

AI-05B must freeze concrete build contracts, not implement them.

Required outputs:

```text
1 module public boundaries
2 ports + runtime DTO/types
3 Search read/query contracts
4 ModelAccessPort contract
5 provider adapter conformance contract
6 route/config artifact schemas
7 resource admission/settlement seams
8 first-vertical HTTP + streaming/publication shape
9 runtime-only vs evidence/persistence classification
10 exact unit/integration/eval/system test topology
11 qualification artifact + promotion evidence schema
12 feature/activation gates
13 implementation dependency graph
14 first build gates / commit sequence
15 destructive AI-05B acceptance before whole AI-05 closure
```

Provider/model/SDK selection remains OPEN. If a concrete selection requires live API evidence, AI-05B records the exact gate and proof instead of guessing.

## 8. Current non-claims

```text
AI-05A CLOSED / STRUCTURAL          YES
AI-05 WHOLE PHASE CLOSED            NO
AI-05B SUBSTANTIVE DESIGN           NOT YET MATERIALIZED
modules/search implemented          NO
modules/intelligence implemented    NO
provider/model/SDK selected         NO
direct provider eval                NO
production capacity pass            NO
stream transport selected           NO
new PostgreSQL/Alembic change       NO
new AI table/index                  NO
FTS/vector/pgvector activation      NO
conversation persistence            NO
control-plane persistence           NO
commercial/resource ledger          NO
Restate/R2/MCP/A2A activation       NO
Execution Environment               NO
```

## 9. Git discipline

Before every remote write:

```text
BRANCH
PRE-SCOPE
CREATE
UPDATE
DELETE
PURPOSE
EXPLICITLY OUT OF SCOPE
```

Then refetch the live branch HEAD before the first write. If it moved, STOP/re-gate. After writes compare PRE-SCOPE..HEAD and prove exact path scope/readback/status.

## 10. Handoff lifecycle

This file is temporary and MUST NOT merge to protected `main`. Before integration: propagate durable truth → verify coverage → DELETE this file.