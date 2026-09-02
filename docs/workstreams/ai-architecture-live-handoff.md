# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Workstream:** DANTE AI architecture
- **Current phase:** AI-04 — Productionization Architecture
- **AI-04A:** DIRECT EVAL SPECIFICATION MATERIALIZED / TOOLING SPIKE NEXT
- **AI-03A:** CLOSED / C01..C33
- **AI-03B:** CLOSED / B01..B35
- **AI-03C:** CLOSED / MAT-01..MAT-15
- **AI-03 overall:** CLOSED / STRUCTURALLY ACCEPTED
- **Refreshed:** 2026-09-02
- **Current gate PRE-SCOPE:** `f5ee7e1fc86c1f2e5675ee860bbbadfbc6bde68a`
- **AI-04A direct-eval spec commit:** `8fee6562a5301ecd5b69cc03ee2d5ad76ac4e14e`
- **Current branch HEAD:** FETCH LIVE before every write

This file exists only to survive chat/session/context saturation while `feature/ai-architecture` is active. Durable architecture truth lives in architecture/current-status sources.

Repository truth outranks this handoff.

---

# 1. Resume rule

```text
repository  MattiaRubino/dante
branch      feature/ai-architecture
workstream  DANTE AI architecture
current     AI-04 Productionization Architecture
next        AI-04A First Executable Eval Tooling Spike
```

Closed upstream:

```text
AI-02.1        CLOSED / STRUCTURALLY ACCEPTED
AI-03A         CLOSED / C01..C33
AI-03B         CLOSED / B01..B35
AI-03C         CLOSED / MAT-01..MAT-15
AI-03 overall  CLOSED / STRUCTURALLY ACCEPTED
```

Do not restart generic Context/Retrieval/Memory research without concrete contradictory downstream evidence.

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
```

For any AI-04 conclusion touching semantics/persistence, inspect Product/North Star, Domain, Whole Logical/WL-H01..H12, Physical, CP6/PostgreSQL Constitution, current DB/Alembic/SQLAlchemy truth, Recovery and PSV/benchmark obligations directly.

---

# 3. Closed project state

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN
CLOSED

LOGICAL
CLOSED / 57 OF 57 / WL-H01..WL-H12

PHYSICAL
CLOSED
PostgreSQL 18 major family accepted
PostgreSQL = sole canonical persistence/material-history authority

BACKEND CP1–CP5
CLOSED / integrated

CP6 DATABASE
CLOSED / integrated

CURRENT PostgreSQL
18.6
Alembic 20260830_09
69 tables / 5 views / 15 routines / 76 triggers /
97 indexes / 69 FKs / 123 CHECKs

RECOVERY
CP01–CP07 LOCAL PASS / CLOSED / integrated
material_state_retirement materialized
remote backup provider TBD / NOT ACTIVATED
production/cloud recovery NOT CLAIMED
```

No model/provider/eval framework may redefine these contracts.

---

# 4. Current compact roadmap

```text
AI-00  COMPLETE
AI-01  COMPLETE
AI-02  CLOSED / STRUCTURALLY ACCEPTED
AI-03  CLOSED / STRUCTURALLY ACCEPTED

AI-04  PRODUCTIONIZATION ARCHITECTURE — CURRENT
  AI-04A eval/model/provider/economics
    provider boundary candidate            MATERIALIZED
    DANTE-E01..E13 workload taxonomy       MATERIALIZED
    direct executable eval specification  MATERIALIZED
    first eval tooling spike               NEXT
  concrete runtime/capabilities            FUTURE IN AI-04
  security/privacy/control-plane/ops       FUTURE IN AI-04

AI-05  WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT — FUTURE
THEN   ACTUAL AI IMPLEMENTATION WORKSTREAM(S)
```

---

# 5. AI-04A current durable authority

```text
docs/architecture/dante-ai-04-productionization-architecture.md
docs/architecture/dante-ai-04a-direct-eval-specification.md
```

Provider boundary remains:

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY
DANTE FEATURE/BUSINESS CODE != CONCRETE PROVIDER SDK
PROVIDER REPLACEABLE != PROVIDERS IDENTICAL
PROVIDER REPLACEABLE != LOWEST-COMMON-DENOMINATOR PROVIDER USAGE
```

Production chain:

```text
DANTE work/capability need
→ ModelTarget
→ HarnessProfile
→ ProviderBinding
→ ProviderAdapter
→ serving platform / model / deployment
```

No concrete provider/model/default is selected.

---

# 6. Direct eval specification

Workload families:

```text
DANTE-E01  model avoidance / deterministic fast path
DANTE-E02  intent + reference / target resolution
DANTE-E03  structured extraction / understanding
DANTE-E04  native query + history + absence semantics
DANTE-E05  context + privacy + Reality Scope
DANTE-E06  planning / replanning / scenario reasoning
DANTE-E07  document / long-context / multimodal reasoning
DANTE-E08  tool / capability use
DANTE-E09  consequential effect boundary
DANTE-E10  multi-actor / delegation / disclosure
DANTE-E11  adaptive memory / learning
DANTE-E12  currentness / failure / supersession / failover
DANTE-E13  open-world research / grounding
```

Core eval rules:

```text
DANTE OWNS EVAL SEMANTICS
OUTCOME/ENVIRONMENT STATE > MODEL SELF-REPORT
HARD FAILURES ARE NOT AVERAGED AWAY
HIDDEN ORACLE STATE MUST NOT LEAK
ONE EXACT TRAJECTORY ONLY WHEN SEMANTICS REQUIRE IT
INVALID FIXTURE/GRADER/HARNESS != MODEL FAILURE
COGNITION QUALITY != SERVING-BINDING RELIABILITY
REPEATED RELIABILITY IS FIRST-CLASS
CAPABILITY EVAL != REGRESSION EVAL
PRODUCTION TRACE != AUTOMATIC EVAL DATA
EVAL/JUDGE DATA FLOW IS GOVERNED
IT-IT + EN-US CORE COVERAGE
```

Trial verdicts include PASS, HARD_FAIL, QUALITY_FAIL, INVALID_FIXTURE, INVALID_GRADER, INVALID_HARNESS, PROVIDER_INFRA_FAILURE and INCONCLUSIVE.

---

# 7. Commercial/service-tier boundary added to AI-04

DANTE already has a Domain `Plan`. Do **not** reuse that word as the unqualified commercial subscription concept.

```text
COMMERCIAL SUBSCRIPTION / SERVICE TIER
!= DANTE DOMAIN Plan
```

Provisional control/commercial boundary:

```text
CommercialOffering / ServiceTier
→ EntitlementProfile
→ capability + quota + resource envelope
→ Budget / Routing Policy
→ ModelTarget eligibility
→ ProviderBinding
```

Binding:

```text
COMMERCIAL TIER != MODEL
COMMERCIAL TIER != PROVIDER
COMMERCIAL TIER != DEPLOYMENT
```

Commercial tiers may govern resource budgets, concurrency, background/research allowances, long-context envelope, rate limits and premium capability availability.

They may **not** weaken semantic correctness, privacy, Authority/AuthZ/Consent/Visibility, target safety, effect verification, anti-resurrection or provider/data eligibility.

No names (`Base`, `Plus`, `Pro`, etc.), prices, quotas or final product packaging are selected yet.

---

# 8. Eval tooling posture

Current preferred candidate only:

```text
Inspect AI
→ PREFERRED DIRECT-EVAL RUNNER CANDIDATE
→ DIRECT TOOLING / PYTHON-3.14 PROOF REQUIRED
→ NOT SELECTED
→ NOT INSTALLED
```

Other secondary/challenger tools remain possible, including provider-native eval products, LangSmith/Braintrust-style experiment systems and Promptfoo-class red-team tooling.

DANTE eval semantics remain framework-neutral.

Preferred future boundary if the spike passes:

```text
tooling/ai-evals/
```

not uncontrolled paid/stochastic API calls inside ordinary backend pytest.

---

# 9. Exact next action

```text
AI-04A — FIRST EXECUTABLE EVAL TOOLING SPIKE
```

Bounded sequence:

```text
1. prove isolated eval-tooling project boundary;
2. test preferred runner candidate under repository/Python constraints;
3. implement synthetic no-network fixture runner first;
4. cover a tiny representative set:
   E01 deterministic/no-model
   E02 target ambiguity
   E08 tool call
   E09 UNKNOWN consequential effect
   E10 privacy/multi-actor
   entitlement/quota case;
5. implement deterministic DANTE verdict semantics;
6. verify repeated-trial evidence and artifact export;
7. only then gate provider SDKs/credentials/paid API calls;
8. freeze exact model/binding/HarnessProfile before comparative runs.
```

No production backend implementation starts from this spike.

---

# 10. Current non-claims

```text
AI-04 CLOSED                         NO
AI-04A CLOSED                        NO
DIRECT PROVIDER EVAL PASS            NO
PROVIDER SELECTED                    NO
MODEL DEFAULT SELECTED               NO
PROVIDER SDK SELECTED                NO
EVAL RUNNER SELECTED                 NO
INSPECT AI INSTALLED                 NO
PAID API CALL EXECUTED               NO
COMMERCIAL TIER NAMES/PRICES SET     NO
AI BACKEND IMPLEMENTED               NO
POSTGRESQL/ALEMBIC CHANGED           NO
NEW AI TABLE/INDEX                   NO
PGVECTOR/ANN ACTIVATED               NO
FTS/PG_TRGM ACTIVATED                NO
RESTATE/R2 ACTIVATED                 NO
MCP/A2A IMPLEMENTED                  NO
EXECUTION ENVIRONMENT IMPLEMENTED    NO
SC/PSV DIRECT PROOFS EXECUTED        NO
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