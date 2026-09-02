# DANTE Roadmap

- **Status:** CURRENT
- **Last reconciled:** 2026-09-02
- **Protected `main`:** integrated source authority; read the live Git ref for the current SHA

## 1. Completed foundations

```text
Product / North Star
        CURRENT
          ↓
Domain Model
        CLOSED
          ↓
Logical Model
        CLOSED / 57 OF 57 / WL-H01..WL-H12
          ↓
Pre-Physical Repository & Architecture Coherence
        CLOSED / FINAL QA PASS
          ↓
Physical Model / Target Selection
        CLOSED / SELECTED / ACCEPTED
        PostgreSQL 18 major family canonical
          ↓
Engineering Foundation v0
        CLOSED / ACCEPTED
          ↓
Frontend Engineering Foundation
        CLOSED / INTEGRATED VIA PR #22
          ↓
Frontend Production Materialization
        CLOSED / PASS / INTEGRATED VIA PR #28
          ↓
Backend CP1–CP5 Scaffold
        CLOSED / DIRECT QA PASS / INTEGRATED VIA PR #24
          ↓
Backend CP6 Concrete PostgreSQL Database
        CLOSED / DIRECT QA PASS / INTEGRATED VIA PR #42
          ↓
PostgreSQL LOCAL Recovery
        CP01–CP07 CLOSED / LOCAL PASS / INTEGRATED VIA PR #47
          ↓
Access Pre-Backend Web Materialization
        CLOSED / ACCEPTED / RELEASE-HARDENED
```

Architecture/design closure remains distinct from product/runtime completion.

## 2. Current PostgreSQL / Recovery baseline

Historical pre-Recovery CP6 baseline:

```text
PostgreSQL          18.6
Alembic             20260826_08
68 tables / 5 views / 14 routines / 75 triggers /
95 indexes / 68 FKs / 120 CHECK constraints
```

Current protected-main database / Recovery baseline:

```text
PostgreSQL          18.6
Alembic             20260830_09
69 tables / 5 views / 15 routines / 76 triggers /
97 indexes / 69 FKs / 123 CHECK constraints
CP01–CP07           LOCAL PASS / CLOSED
Recovery            INTEGRATED VIA PR #47
remote provider     TBD / NOT ACTIVATED
cloud recovery      NOT CLAIMED
```

Current authority begins at `database/README.md`, the Dictionary, PostgreSQL Recovery runbook, CP6 persistence constitution and ADR-010.

## 3. Current bounded unmerged workstreams

```text
feature/access-auth             active full-stack product work
feature/home-react              active frontend work
feature/platform-observability  active platform work
feature/ai-architecture         AI architecture design CLOSED / implementation handoff ready
```

Each branch owns only its bounded newer truth until protected-main integration.

## 4. Database evolution after CP6 / Recovery

Permanent same-change rule:

```text
real structural database change
→ forward Alembic migration
→ SQLAlchemy mapping/metadata update
→ Database Dictionary update
→ human-readable reference update when applicable
→ generated artifacts/diagrams where governed
→ direct tests
→ affected recovery/operational assertions updated
```

Applied migrations are immutable. AI architecture closure produced no DB/Alembic change.

## 5. Capability-triggered implementation

Specialist components activate only at real triggers:

```text
PowerSync + encrypted SQLite
→ real offline/multi-device requirement

PostgreSQL transactional outbox
→ real Class-A async requirement

R2
→ real ContentArtifact byte flow

OR-Tools
→ solver-backed capability

Restate
→ first real Class-B durable workflow + applicable direct proofs

PgBouncer
→ concrete connection-management need + validation

AI FTS / pg_trgm
→ measured Search need + same-change DB package + direct proof

pgvector / ANN / embeddings
→ retrieval evaluation proves need + lifecycle/security/freshness/provenance proof

AI Execution Environment
→ generated/untrusted code/browser/computer-use threat-model trigger

MCP / A2A
→ real external capability/integration trigger

cross-Run prior-disclosure accounting
→ real H19 cumulative-disclosure trigger
```

Selected capability != activated implementation.

## 6. AI architecture roadmap — CLOSED

The exploratory AI-00..AI-12 decomposition is historical planning only.

The completed compact architecture sequence is:

```text
AI-00 — SEMANTIC & PRODUCT FOUNDATION
COMPLETE
        ↓
AI-01 — PRODUCT FORM + PRODUCTION ENGINEERING RESEARCH
COMPLETE
        ↓
AI-02 — INTELLIGENCE RUNTIME ARCHITECTURE
CLOSED / STRUCTURALLY ACCEPTED
AI-02.1 v0.5
        ↓
AI-03 — CONTEXT / RETRIEVAL / MEMORY
CLOSED / STRUCTURALLY ACCEPTED
C01..C33 / B01..B35 / MAT-01..MAT-15
        ↓
AI-04 — PRODUCTIONIZATION ARCHITECTURE
CLOSED / STRUCTURALLY ACCEPTED
A01..A30 / EV01..EV20 / RT-01..RT-31 / PA-01..PA-61 / WP-01..WP-22
        ↓
PRE-AI05 — CROSS-PHASE HARDENING
CLOSED / PRE05-H01..H19
DANTE-E01..DANTE-E14 current eval families
        ↓
AI-05A — WHOLE-SYSTEM BUILD BOUNDARY
CLOSED / BD-01..BD-41
        ↓
AI-05B — CONCRETE IMPLEMENTATION BLUEPRINT
CLOSED / AI05B-H01..H15 / B05-01..B05-50 PASS
        ↓
AI-05 WHOLE-SYSTEM ACCEPTANCE
CLOSED / STRUCTURALLY ACCEPTED
        ↓
POST-AI05 INDEPENDENT PRE-IMPLEMENTATION MEGA TEST
FIRST PASS FAIL BOUNDED
→ POST05-H01..H13
SECOND PASS FAIL BOUNDED
→ POST05-H14..H18
THIRD PASS FAIL BOUNDED
→ POST05-H19..H25
FINAL FRESH PASS
→ MKT-001..MKT-100 PASS
→ C01..C20 PASS
→ reverse authority PASS
→ Product/simulation replay PASS
        ↓
AI ARCHITECTURE DESIGN / REENGINEERING
CLOSED / STRUCTURALLY ACCEPTED
```

Current implementation authority:

```text
docs/architecture/dante-ai-implementation-baseline-final.md
```

Final mega acceptance:

```text
docs/architecture/dante-ai-post05-final-mega-acceptance.md
```

## 7. Current AI implementation roadmap

Architecture is now an upstream contract. The current sequence is implementation:

```text
I0  repository/application ownership + architecture-test skeleton
    ↓
I1  Search public contracts / eligibility / family registry / deterministic shell
    ↓
I2  Intelligence pure contracts + deterministic fakes
    Work / Execution / Context / Reference Resolution /
    Semantic Query / Retrieval / Policy / Resource /
    Verification / Publication / Effect / Egress evidence
    ↓
I3  first real deterministic Search / structured query families
    only when owning product data/seams are integration-ready
    ↓
I4  provider candidate admission + inactive adapter candidate
    ↓
I5  adapter conformance + live compatibility + direct DANTE qualification
    ↓
I6  read-only Ask DANTE
    ↓
I7  production hardening / observability / privacy / audit /
    resource / rollout / capacity
    ↓
I8  scenario/planning proposal vertical
    ↓
I9  first bounded consequential Effect vertical
    ↓
I10 proactive/background/durable/external-agent capabilities
    only on their real triggers
```

Current exact next action:

```text
I0
→ establish modules/search and modules/intelligence ownership only as needed
→ establish executable architecture-boundary tests
→ preserve green existing backend gates
→ no provider dependency
→ no database migration
→ no production activation
```

## 8. First implementation vertical boundary

Target:

```text
GLOBAL SEARCH subset
+ READ-ONLY ASK DANTE
```

Initial envelope:

```text
private authenticated in-app
single-turn
inline/request-owned
READ_ONLY
public streaming OFF
background/durable resume OFF
consequential mutation OFF
```

Search is deterministic/no-model capable. Structured DANTE questions use owning capability typed query seams; no raw model-to-SQL or Intelligence-owned cross-capability SQL is permitted.

## 9. Provider / activation gates

Provider/model/SDK remains OPEN / evidence-driven.

```text
candidate shortlist
→ candidate admission
→ inactive adapter
→ conformance
→ live compatibility on eligible/minimized data
→ direct DANTE eval using production-owned composition
→ security/privacy/capacity/economics evidence
→ qualification
→ promotion
```

Build-ready is not activation-ready. Private-data Search/Ask requires real Auth/AuthZ, source/query semantics, applicable SC/PSV proofs, safe publication, evidence/privacy/audit and provider qualification when a model route is used.

## 10. Current non-claims

```text
AI architecture design closed          YES
post-AI05 structural mega pass         YES
implementation baseline accepted       YES
I0 started                              NO
Search implemented                     NO
Intelligence implemented               NO
provider/model/SDK selected            NO
production Search/Ask active           NO
new PostgreSQL/Alembic change          NO
new generic AI persistence             NO
FTS/vector activated                   NO
Restate/R2/MCP/A2A activated           NO
Execution Environment selected         NO
```
