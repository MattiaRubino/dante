# DANTE Roadmap

- **Status:** CURRENT
- **Last reconciled:** 2026-09-04
- **Protected `main`:** integrated source authority; read the live Git ref for the current SHA
- **Branch-local AI implementation overlay:** `feature/ai-implementation`

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
feature/ai-implementation       active AI implementation; I0-I2 CLOSED/PASS
                                I3/C3 deferred pending owner data/seams
                                C6+C7+C8 CLOSED
                                C9 OPEN / PRE-LIVE READY
feature/ai-architecture         AI architecture design CLOSED / retained authority/evidence
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

Applied migrations are immutable. AI architecture and I0-I2/C6/C7/C8/C9 pre-live produced no DB/Alembic change.

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

Current C8 provider admission evidence:

```text
docs/workstreams/ai-provider-candidate-admission-2026-09.md
```

Current C9 pre-live evidence:

```text
docs/workstreams/ai-c9-pre-live-checkpoint-2026-09.md
```

Final mega acceptance:

```text
docs/architecture/dante-ai-post05-final-mega-acceptance.md
```

## 7. AI implementation roadmap — architectural stages and execution overlay

The baseline stage identifiers remain authoritative architectural labels; they are **not** redefined merely because one conditional integration lane is not ready yet.

Accepted stage map:

```text
I0  repository/application ownership + architecture-test skeleton
    CLOSED / PASS

I1  Search public contracts / eligibility / family registry / deterministic shell
    CLOSED / PASS

I2  Intelligence pure request-local contracts + deterministic fakes
    Work / Execution / Context / Reference Resolution /
    Semantic Query / Retrieval
    CLOSED / PASS

I3  real deterministic Search / structured families
    only when owning product data/seams are integration-ready
    DEFERRED / WAITING OWNER DATA + SEAMS

I4  provider candidate admission + inactive adapter candidate

I5  adapter conformance + live compatibility + direct DANTE qualification

I6  read-only Ask DANTE

I7  production hardening / observability / privacy / audit /
    resource / rollout / capacity

I8  scenario/planning proposal vertical

I9  first bounded consequential Effect vertical

I10 proactive/background/durable/external-agent capabilities
    only on their real triggers
```

### 7.1 Current executable lane

The implementation blueprint separates the Search lane from the Intelligence/provider-preparation lane. Because I3 is conditional on real owner data/seams, execution continues without fabricating a Search family:

```text
C6  Policy / Resource / Verification / Publication /
    Effect / Egress / Evidence contracts
    CLOSED / PASS
    ↓
C7  route-config identity / loader / content digest snapshot
    CLOSED / PASS
    ↓
C8 / P0-P1
    provider shortlist + candidate-admission decision
    CLOSED
    OpenAI native Responses API + gpt-5.6-terra
    ADMITTED FOR QUALIFICATION ONLY
    ↓
CURRENT
C9  OPEN / PRE-LIVE READY
    inactive provider adapter/binding           MATERIALIZED
    OpenAI SDK 3.7.0                            LOCKED
    deterministic + material SDK conformance    PASS
    P4 pre-live                                 PASS
    final deterministic + PostgreSQL regression PASS
    P4 real provider compatibility              NOT RUN
    blocker: no user-owned qualification API credential provisioned
    ↓
C10
    direct DANTE qualification
    ↓
C11
    qualification/promotion decision
```

C8 admits a qualification candidate only. C9 now materializes the SDK/private inactive adapter and deterministic proof surface, but no real provider live call, production qualification or private-data eligibility is claimed.

### 7.2 Deferred deterministic/Search lane

```text
I3 / C3
bounded PostgreSQL Search adapter + first real family proof
```

remains open and must resume only when a real owner/data seam can truthfully supply the family. Current CP6 PostgreSQL materialization is a strong persistence substrate, but persistence rows alone do not create a complete product/application query seam.

I3 readiness requires, as applicable:

```text
real owner/product data semantics
safe display/projection fields
current/history behavior
owner/source scope
permission/disclosure basis
bounded query semantics
truthful guarantee/currentness/basis mapping
family tests
PSV-06 / SC-017 protected non-interference proof when applicable
```

No fake title from UUIDs, Intelligence-owned cross-capability SQL, generic Repository/UoW, model-to-SQL or premature FTS/vector activation is allowed to manufacture readiness.

### 7.3 Mandatory join before I6

Provider qualification and the deferred deterministic lane may progress independently, but **I6 cannot activate the accepted first vertical until the required real source/query path is ready**.

Operational convergence:

```text
C9 → C10 → C11
             \
              +→ JOIN GATE → I6 READ-ONLY ASK
             /
I3/C3 when owner seams become ready
```

The join gate requires the real Search/structured source path needed by the selected first vertical, authoritative Auth/AuthZ/disclosure integration, currentness/publication behavior and every applicable direct proof.

### 7.4 Current exact next action

```text
C9 P4 — REAL PROVIDER LIVE COMPATIBILITY

admitted candidate:
provider          OpenAI native API
API               Responses API
model             gpt-5.6-terra
SDK               openai 3.7.0
status            ADMITTED FOR QUALIFICATION ONLY
binding           INACTIVE / PRODUCTION OFF

already proven:
P2/P3 contracts + inactive adapter       PASS
SDK materialization + lock               PASS
material SDK conformance                 PASS
P4 pre-live                              PASS
final deterministic + PostgreSQL gate    PASS

remaining:
P4 live compatibility                    NOT RUN
credential                               user-owned qualification API key required
traffic                                  synthetic/public/minimized only

mandatory initial feature profile:
public streaming          OFF
background mode           OFF
provider conversation     OFF
previous_response_id      OFF
provider built-in tools   OFF
web/file search           OFF
code/shell/computer use   OFF
MCP/external tools        OFF
provider memory           OFF
store                     false
SDK automatic retries     OFF / max_retries=0
reasoning effort          medium
reasoning context         current_turn
service tier              default
truncation                disabled
production activation     OFF

C9 MUST NOT claim direct DANTE qualification or production eligibility
NO database/Alembic change
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

Current admission state:

```text
OpenAI native Responses API + gpt-5.6-terra
ADMITTED FOR QUALIFICATION ONLY
C9 PRE-LIVE READY
```

Correct progression:

```text
candidate shortlist                         COMPLETE
→ candidate admission                       C8 / COMPLETE
→ inactive adapter + SDK                    C9 / MATERIALIZED
→ deterministic/material conformance        C9 / PASS
→ P4 pre-live                               C9 / PASS
→ final deterministic + PostgreSQL gate     C9 / PASS
→ live compatibility on synthetic/public/minimized data C9 / NOT RUN
→ direct DANTE eval                         C10
→ security/privacy/capacity/economics evidence
→ qualification
→ promotion decision                        C11
```

Candidate admission and pre-live PASS are not production eligibility. Build-ready is not activation-ready. Private-data Search/Ask requires real Auth/AuthZ, source/query semantics, applicable SC/PSV proofs, safe publication, evidence/privacy/audit and provider qualification when a model route is used.

## 10. Current implementation state / non-claims

```text
AI architecture design closed          YES
post-AI05 structural mega pass         YES
implementation baseline accepted       YES
AI implementation started              YES
I0 closed / pass                       YES
I1 closed / pass                       YES
I2 closed / pass                       YES
Search shell/contracts implemented     YES
Intelligence C5 contracts/fakes        YES
I3 real family / PG adapter            NO / DEFERRED
C6 control contracts                   YES / CLOSED-PASS
C7 route-config loader                 YES / CLOSED-PASS
C8/P1 provider candidate admission     YES / CLOSED
admitted qualification candidate       OpenAI Responses / gpt-5.6-terra
provider SDK installed                 YES / openai 3.7.0 / locked
provider adapter                       YES / INACTIVE / QUALIFICATION-ONLY
C9 deterministic/material conformance  PASS
C9 P4 pre-live                         PASS
C9 final deterministic + PG regression PASS
live provider call                     NO / NOT RUN
C9 overall                             OPEN / PRE-LIVE READY
production qualification              NO
private-data eligibility               NO
production Search/Ask active           NO
new PostgreSQL/Alembic change          NO
new generic AI persistence             NO
FTS/vector activated                   NO
Restate/R2/MCP/A2A activated           NO
Execution Environment selected         NO
```