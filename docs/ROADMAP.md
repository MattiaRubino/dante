# DANTE Roadmap

- **Status:** CURRENT
- **Last reconciled:** 2026-09-05
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
feature/ai-implementation       AI low-level foundation closure candidate
                                I0-I2 CLOSED/PASS
                                I3 Search deferred pending real owner data/seams
                                C6+C7 CLOSED/PASS
                                development binding decision = Gemini 3.8 Flash
                                native ModelAccess foundation materialized
                                final deterministic gate + 1 native smoke pending
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

Applied migrations are immutable. The AI architecture/implementation work described here introduces no DB/Alembic change.

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
FINAL FRESH PASS
→ POST05-H01..H25 historical hardening retained
→ MKT-001..MKT-100 PASS
→ C01..C20 PASS
→ reverse authority PASS
→ Product/simulation replay PASS
        ↓
AI ARCHITECTURE DESIGN / REENGINEERING
CLOSED / STRUCTURALLY ACCEPTED
```

Current implementation-facing architecture authority:

```text
docs/architecture/dante-ai-implementation-baseline-final.md
docs/architecture/dante-ai-search-intelligence-boundary-amendment-2026-09.md
```

Current low-level foundation decision/closure records:

```text
docs/workstreams/ai-runtime-model-target-closure-acceptance-2026-09-05.md
docs/workstreams/ai-foundation-closure-2026-09-05.md
```

Historical OpenAI/Terra admission and C9 pre-live records remain evidence, not the current provider blocker.

## 7. AI implementation roadmap — current disposition

The I0-I10 names remain architecture-stage labels. They are not forced into a fake linear implementation order when a real owner/product seam does not yet exist.

```text
I0  repository/application ownership + architecture boundary skeleton
    CLOSED / PASS

I1  Search public contracts / eligibility / family registry / deterministic shell
    CLOSED / PASS

I2  Intelligence pure request-local contracts + deterministic fakes
    CLOSED / PASS

I3  first real deterministic Search / structured owner family
    DEFERRED / REAL OWNER-DATA-SEAM GATE

I4  provider candidate / binding foundation
    CLOSED FOR DEVELOPMENT FOUNDATION

I5  adapter conformance / direct provider evidence
    DEVELOPMENT FOUNDATION CLOSURE CANDIDATE
    remaining now:
      - regenerate lock after explicit Gemini HTTP runtime dependency
      - deterministic/full backend gate
      - one guarded native Gemini Interactions smoke through ModelAccessRuntime
    production qualification remains FUTURE

I6  first real read-only Ask DANTE integration
    DEFERRED / PRODUCT-READINESS GATE
    do not manufacture an Ask vertical merely to prove an AI call

I7  production hardening / observability / privacy / audit / resource / rollout / capacity
    PARTIALLY FRONT-LOADED ONLY FOR MODELACCESS-LOCAL FOUNDATION
    full production stage FUTURE

I8  scenario/planning proposal vertical
    FUTURE / REAL PRODUCT-SEAM TRIGGER

I9  first bounded consequential Effect vertical
    FUTURE / REAL CAPABILITY-EFFECT TRIGGER

I10 proactive/background/durable/external-agent capabilities
    FUTURE / TRIGGER-GATED
```

### 7.1 Development model/binding decision

Direct evidence now supports the development foundation decision:

```text
STRUCTURED_INTERPRETATION -> Gemini 3.8 Flash
GENERAL_REASONING         -> Gemini 3.8 Flash
DEEP_REASONING            -> dormant / no binding
```

Accepted runtime protocol direction:

```text
Google Gemini Developer API
native Interactions API v1beta
OpenAI-compatible Gemini surface = evaluation history only
```

Initial development harness:

```text
reasoning level            low
streaming                  off
background                 off
provider continuation      off
provider-native tools      off
provider storage           off / store=false
fallback                   off
DANTE retry                off for foundation
private-data eligibility   no
production activation      off
```

### 7.2 Old C6-C11 overlay reconciliation

```text
C6  governance/resource/evidence contracts              CLOSED / retained
C7  immutable route-config identity                      CLOSED / extended to typed v2
C8  OpenAI/Terra admission                               HISTORICAL PASS / retained evidence
C9  OpenAI/Terra live-compatibility blocker              SUPERSEDED AS CURRENT PATH
C10 development model evidence                           COMPLETE
C11 development binding decision                         COMPLETE / Gemini 3.8 Flash
production qualification/promotion                       NOT COMPLETE / NOT CLAIMED
```

This does not claim OpenAI/Terra failed. It means the old unexecuted Terra live call no longer blocks the accepted development route after direct GPT-4.1/Gemini evidence and the owner decision.

### 7.3 Low-level ModelAccess foundation materialized

Current branch now contains:

```text
application-owned ModelAccessPort
ModelTarget / ModelInvocation contracts
ProviderAttempt / acceptance / error taxonomy
detailed usage evidence including reasoning/cached/tool-use tokens
typed immutable route config v2
deterministic champion routing
champion/challenger/fallback configuration slots
Gemini native Interactions adapter
private HTTP transport
provider-independent structured-output validation
deadline/timeout bounding
no blind retry/fallback
minimized route/provider runtime evidence
unit tests + guarded native smoke tooling
```

The caller does not need to know that Google is the development champion.

## 8. Search and real Intelligence integration boundary

Global Search remains independent:

```text
Search contracts / eligibility / registry
→ real Search families only when owner seams exist
→ deterministic discovery/navigation
```

I3 remains open but deliberately deferred. Persistence rows alone do not manufacture a useful Search family.

The first real Intelligence integration is also deliberately deferred until DANTE has a real owning application capability with:

```text
real source/query seam
safe projection/display semantics
current/history semantics
Auth/AuthZ/Visibility/Consent/disclosure
source/provenance/basis/currentness
verification/publication behavior
```

A typed owning-capability query may satisfy an Intelligence need directly. Search is required only when the selected workload genuinely requires discovery.

## 9. Provider / activation gates after foundation freeze

Development foundation closure is not production qualification.

Future production/private-data activation still requires applicable evidence for:

```text
privacy / retention / regional posture
security
reliability
capacity
latency
cost per successful DANTE task
rollout / rollback
operational observability/audit
real product source/query semantics
publication/disclosure/currentness
```

A second provider, failover, local model or deep-reasoning physical binding activates only from evidence of a material need.

## 10. Current exact next action

```text
feature/ai-implementation
→ finish low-level foundation closure only
→ regenerate uv.lock for explicit httpx2 runtime dependency
→ full deterministic/backend regression
→ native Gemini smoke dry-run
→ exactly one synthetic native Gemini Interactions smoke through ModelAccessRuntime
→ if PASS: mark ai-foundation-closure checkpoint CLOSED / PASS and freeze branch
```

After that:

```text
leave feature/ai-implementation
return to the broader DANTE roadmap / main-oriented work
no forced Ask DANTE vertical
no additional broad model benchmarking
```

Current non-claims:

```text
production qualification              NO
private-data Gemini eligibility        NO
production Search                      NO
production Ask                         NO
first real Intelligence vertical       NOT YET SELECTED
new PostgreSQL/Alembic change          NO
new generic AI persistence             NO
FTS/vector activation                  NO
Restate/R2/MCP/A2A activation          NO
Execution Environment activation       NO
```
