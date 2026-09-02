# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Current phase:** AI-05A — WHOLE-SYSTEM BUILD BOUNDARY / OWNERSHIP MAP
- **AI-05A:** CANDIDATE / FIRST T01..T26 PASS FAIL BOUNDED / BD-31..BD-40 MATERIALIZED
- **Fresh retest after hardening:** NOT YET EXECUTED
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
→ AI-05A hardened candidate
→ read docs/architecture/dante-ai-05a-whole-system-build-boundary.md
→ restart T01..T26 from zero
→ run compound collisions
→ reverse-check against AI-04/PRE-AI05/AI-03/AI-02
→ if FAIL: harden smallest boundary
→ if clean: close AI-05A
→ then AI-05B concrete implementation blueprint
```

## 2. First-pass hardening

The first destructive pass did not accept the original candidate.

Binding additions:

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
```

## 3. Candidate first-build ownership

```text
modules/search
→ shared deterministic permission-aware Search/read projection
→ may use reviewed SQL/Core in its private search persistence adapter
→ no canonical ownership / no mutation / no model-SQL

modules/intelligence
→ Work/Context/routing/model-assisted orchestration/verification/publication
→ consumes Search/public capabilities

provider SDK
→ private outbound adapter behind DANTE ModelAccess port

resource/commercial authority
→ shared/commercial quota/metering truth
→ consumed by Intelligence through admission/settlement boundary

bootstrap
→ wiring/lifecycle

platform
→ shared technical mechanics only

tooling/ai-evals
→ direct provider/model qualification tooling
```

## 4. First vertical envelope

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

## 5. Retest pressure

Run the same `T01..T26` plus compounds:

```text
Search + Intelligence + provider outage
Search hidden result + model synthesis
static config rollout + invocation snapshot + emergency deny
quota admission + retry/failover + settlement
inline stream + disconnect + no durable Run
cumulative disclosure + zero-persistence envelope
```

No changed exam: prior FAIL cases must pass under the new boundaries.

## 6. Current non-claims

```text
AI-05A PASS/CLOSED                NO
modules/search implemented        NO
modules/intelligence implemented  NO
provider/model/SDK selected       NO
direct provider eval              NO
stream transport selected         NO
new PostgreSQL/Alembic change     NO
new AI table/index                NO
FTS/vector/pgvector activation    NO
conversation persistence          NO
control-plane persistence         NO
commercial/resource ledger        NO
Restate/R2/MCP/A2A activation     NO
Execution Environment             NO
```

## 7. Git discipline

Before every remote write: exact BRANCH / PRE-SCOPE / CREATE / UPDATE / DELETE / PURPOSE / OUT-OF-SCOPE gate, then refetch HEAD. After writes compare PRE-SCOPE..HEAD and prove path scope.

## 8. Handoff lifecycle

This file is temporary and MUST NOT merge to protected `main`. Before integration: propagate durable truth → verify coverage → DELETE this file.