# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Current phase:** AI-05A — WHOLE-SYSTEM BUILD BOUNDARY / OWNERSHIP MAP
- **AI-05A:** CANDIDATE / FIRST PASS FAIL → BD-31..BD-40 / SECOND INDIVIDUAL PASS + COMPOUND FAIL → BD-41
- **Fresh retest after BD-41:** NOT YET EXECUTED
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
→ read docs/architecture/dante-ai-05a-whole-system-build-boundary.md
→ read docs/architecture/dante-ai-05a-eval-production-composition-hardening.md
→ restart T01..T26 from zero
→ rerun compound collisions including exact production-composition qualification
→ reverse-check against AI-04/PRE-AI05/AI-03/AI-02
→ if FAIL: harden smallest demonstrated boundary
→ if clean: close AI-05A
→ then AI-05B concrete implementation blueprint
```

## 2. AI-05A hardening state

First destructive pass additions:

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

Second-pass compound finding:

```text
BD-41
QUALIFICATION EVIDENCE MUST EXERCISE THE SAME MATERIAL PRODUCTION
COMPOSITION THAT WILL BE PROMOTED, OR EVERY MATERIAL DELTA MUST BE
INDEPENDENTLY QUALIFIED BEFORE PROMOTION.
```

The eval runner stays outside the ordinary production request path, but it must not create a second materially different provider stack and then promote that result as production qualification.

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
→ outside ordinary production request path
→ qualifies same material HarnessProfile + ProviderBinding + ProviderAdapter + feature/control composition
→ or independently qualifies material deltas
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
direct eval + exact material production composition / independently qualified deltas
```

Then reverse:

```text
AI-05A
→ AI-04
→ PRE-AI05
→ AI-03
→ AI-02
```

No changed exam: prior FAIL cases must pass under the hardened boundaries.

## 6. Evidence-plane distinctions

```text
APPLICATION FAKE
!= PROVIDER ADAPTER CONFORMANCE
!= LIVE PROVIDER SMOKE / COMPATIBILITY PROOF
!= DIRECT DANTE MODEL/ROUTE EVAL
!= PRODUCTION CAPACITY QUALIFICATION
```

Qualification artifacts must identify the exact material route composition they support and any separately qualified material delta.

## 7. Current non-claims

```text
AI-05A PASS/CLOSED                NO
AI-05B STARTED                    NO
modules/search implemented        NO
modules/intelligence implemented  NO
provider/model/SDK selected       NO
direct provider eval              NO
production capacity pass          NO
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

## 8. Git discipline

Before every remote write: exact BRANCH / PRE-SCOPE / CREATE / UPDATE / DELETE / PURPOSE / OUT-OF-SCOPE gate, then refetch HEAD. After writes compare PRE-SCOPE..HEAD and prove path scope.

## 9. Handoff lifecycle

This file is temporary and MUST NOT merge to protected `main`. Before integration: propagate durable truth → verify coverage → DELETE this file.