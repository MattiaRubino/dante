# DANTE Documentation Index

- **Status:** CURRENT NAVIGATION / AUTHORITY INDEX
- **Last reconciled:** 2026-09-02

This directory is the durable documentation surface for DANTE. Current specifications describe the present directly; historical evidence, phase-time continuations and completed workstream records do not silently override current truth.

## 1. Authority order

When sources conflict, use this order unless a narrower accepted authority explicitly governs the subject:

```text
1. current protected-main executable truth
   code / migrations / tests / generated governed artifacts

2. accepted semantic + architectural authority
   Product / Domain / Logical / Physical / ADRs / current architecture

3. current durable subsystem reference
   Database System of Record / frontend contracts / engineering contracts

4. current project status + roadmap

5. active unmerged branch-local workstream truth
   only for that branch's bounded scope

6. retained evidence / branch history / archive

7. Git / PR chronology

8. conversation memory
```

An unmerged branch may contain newer truth for its own scope, but it is not protected-main authority until integration.

## 2. Current lifecycle

```text
PRODUCT / NORTH STAR                  CURRENT
DOMAIN MODEL                          CLOSED
LOGICAL MODEL                         CLOSED / 57 OF 57 / REMOTE QA PASS
PRE-PHYSICAL COHERENCE                CLOSED / FINAL QA PASS
PHYSICAL TARGET                       CLOSED / ACCEPTED
ENGINEERING FOUNDATION                CLOSED / ACCEPTED
FRONTEND ENGINEERING FOUNDATION       CLOSED / INTEGRATED VIA PR #22
FRONTEND MATERIALIZATION              CLOSED / PASS / INTEGRATED VIA PR #28
BACKEND CP1–CP5 SCAFFOLD              CLOSED / DIRECT QA / INTEGRATED VIA PR #24
BACKEND CP6 DATABASE                  CLOSED / DIRECT QA / INTEGRATED VIA PR #42
CURRENT POSTGRESQL                    18.6
HISTORICAL PRE-RECOVERY ALEMBIC       20260826_08
HISTORICAL PRE-RECOVERY DB TOPOLOGY   68/5/14/75/95/68/120
CURRENT PROTECTED-MAIN ALEMBIC        20260830_09
CURRENT PROTECTED-MAIN DB TOPOLOGY    69/5/15/76/97/69/123
POSTGRESQL LOCAL RECOVERY             CP01–CP07 LOCAL PASS / CLOSED / INTEGRATED VIA PR #47
REMOTE BACKUP PROVIDER                TBD / NOT ACTIVATED
PRODUCTION/CLOUD RECOVERY             NOT CLAIMED
ACCESS PRE-BACKEND FRONTEND           CLOSED / ACCEPTED / RELEASE-HARDENED
FULL ACCESS/AUTH PRODUCT VERTICAL     ACTIVE UNMERGED WORKSTREAM
AI-00 FOUNDATION                      COMPLETE
AI-01 PRODUCT/PRODUCTION RESEARCH     COMPLETE
AI-02.1 RUNTIME ARCHITECTURE          v0.5 CLOSED / STRUCTURALLY ACCEPTED
AI-02 PRESSURE/MEGA TEST PROGRAM      COMPLETE
AI-02 TARGETED v0.5 VERIFICATION      COMPLETE
AI-03 CONTEXT/RETRIEVAL/MEMORY        CLOSED / STRUCTURALLY ACCEPTED
AI-03A FULL CONTEXT ARCHITECTURE      CLOSED / C01..C33
AI-03B RETRIEVAL + MEMORY             CLOSED / B01..B35
AI-03C MATERIALIZATION BLUEPRINT      CLOSED / MAT-01..MAT-15
AI-04 PRODUCTIONIZATION               CLOSED / STRUCTURALLY ACCEPTED
AI-04A                                CLOSED / A01..A30 / EV01..EV20
AI-04B                                CLOSED / RT-01..RT-31
AI-04C                                CLOSED / PA-01..PA-61
AI-04 WHOLE-PHASE                     CLOSED / WP-01..WP-22
PRE-AI05 CROSS-PHASE HARDENING        CLOSED / PRE05-H01..H19
CURRENT CORE AI EVAL                  DANTE-E01..DANTE-E14
AI-05 CURRENT MACRO-PHASE             WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT
AI BACKEND/DB/PROVIDER IMPLEMENTATION NOT CLAIMED
```

For exact current state, read `PROJECT-STATUS.md` rather than reconstructing status from historical workstream/checkpoint files.

## 3. Mandatory project entry points

Read in this order for general project continuation:

1. `../README.md`
2. `README.md`
3. `PROJECT-STATUS.md`
4. `ROADMAP.md`
5. `development/agent-operating-manual.md`
6. `development/operating-rules.md`
7. `development/documentation-and-handoff.md`
8. `development/documentation-lifecycle-policy.md`
9. `development/branching-and-environments.md`
10. `development/repository-engineering-safety.md`
11. the current subsystem/workstream sources relevant to the task
12. current branch/ref and its relation to protected `main`

Repository truth beats incomplete conversation memory.

For the active AI workstream, branch-local continuation additionally uses:

- `workstreams/ai-architecture.md` — durable active-workstream record and current AI-05 routing;
- `workstreams/ai-architecture-live-handoff.md` — TEMPORARY branch-operational handoff while the branch is active; MUST NOT MERGE TO `main`;
- `architecture/dante-ai-04-productionization-architecture.md` — closed AI-04 master authority;
- `architecture/dante-ai-04a-direct-eval-specification.md` — closed AI-04A eval/provider/economics authority with current DANTE-E01..E14 coverage;
- `architecture/dante-ai-04b-concrete-runtime-capability-architecture.md` — closed AI-04B runtime/capability authority, RT-01..RT-31;
- `architecture/dante-ai-04c-production-assurance-control-plane-operations.md` — closed AI-04C production-assurance authority, PA-01..PA-61;
- `architecture/dante-ai-04-whole-phase-destructive-acceptance.md` — closed AI-04 whole-phase authority, WP-01..WP-22;
- `architecture/dante-ai-pre05-cross-phase-hardening.md` — closed PRE-AI05 cross-phase hardening authority, PRE05-H01..H19;
- `architecture/dante-ai-03-context-retrieval-memory.md` — closed AI-03 Context/Retrieval/Memory authority;
- `architecture/dante-ai-03a-full-context-architecture.md` — closed AI-03A Context authority, C01..C33;
- `architecture/dante-ai-03b-retrieval-memory-architecture.md` — closed AI-03B Retrieval/Memory authority, B01..B35;
- `architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md` — closed AI-03C materialization authority, MAT-01..MAT-15.

`architecture/ai-context-runtime-boundaries.md` is **HISTORICAL / PRE-PHYSICAL REFERENCE**. Its old `CURRENT — Phase 6` header is not current AI runtime authority.

## 4. Documentation lifecycle

Current documentation is not an append-only diary.

Temporary branch-operational files such as live/session/resume handoffs may exist while a branch is active, but they must not merge into protected `main`. Before branch integration:

```text
temporary handoffs
→ knowledge coverage
→ current truth propagated to current docs
→ rationale/evidence propagated to durable owners
→ optional ONE branch history record
→ temporary handoffs removed
```

After integration:

```text
verify exact protected-main merge
→ reconcile candidate/branch-local wording to protected-main truth
→ repair links to deliberately removed workstream overlays
→ keep archive history non-authoritative
```

Normative lifecycle source: `development/documentation-lifecycle-policy.md`.

`docs/archive/` is selective non-authoritative history, not a backup mirror. Git remains the complete recoverable history.

Frozen/read-only split specifications may be recomposed only through **lossless knowledge coverage**. Do not summarize away requirements, invariants, rationale, assumptions, counterexamples or important evidence merely to reduce file count.

## 5. Product

Entry point:

- `product/README.md`

Key durable sources include:

- `product/product-identity-and-north-star.md`
- `product/scope.md`
- accepted `product/v1-*.md` specifications
- `product/feature-discovery-simulation-2026-08.md`
- `product/multi-actor-collaboration-discovery-simulation-2026-08.md`
- `product/multi-actor-collaboration-research-2026-08.md`

Research/simulation material is evidence, not automatic current Domain truth.

## 6. Domain Model

Entry point:

- `domain/README.md`

The Domain Model is **CLOSED / semantically complete for current accepted scope**.

Current concept semantics live under `domain/concepts/`. Historical `README-part-N.md` validation/checkpoint continuations remain evidence according to their explicit role and do not override the current Domain Atlas.

Do not infer a semantic kernel primitive merely from UI, product, AI or persistence naming.

## 7. Logical Model

Entry point:

- `logical-model/README.md`

The Logical Model is **CLOSED / 57 of 57 classified / REMOTE QA PASS**.

Primary integrated authority/evidence:

- `logical-model/whole-logical-model-v1.md`
- `logical-model/checkpoints/whole-logical-v1-validation.md`
- `logical-model/checkpoints/whole-logical-v1-remote-qa.md`

Binding hardenings `WL-H01..WL-H12` remain implementation regression contracts unless deliberately superseded by higher accepted authority.

## 8. Physical Model

Entry point:

- `physical-model/README.md`

Current selected target:

```text
PostgreSQL 18 major family
sole canonical persistence + material-history authority
```

PostgreSQL 18.4 remains historical exact Physical/CP2/CP3 evidence. Current repository/database patch is 18.6. The accepted LOCAL Recovery evolution is integrated via PR #47. Remote backup/cloud recovery remains a separate unactivated boundary.

## 9. Architecture and decisions

Entry points:

- `architecture/README.md`
- `architecture/system-overview.md`
- `architecture/technical-decisions.md`
- `decisions/`

AI authority on `feature/ai-architecture` is layered:

```text
architecture/dante-ai-foundation.md
→ AI-00 semantic / architectural baseline

architecture/ai-production-engineering-state-of-the-art-2026.md
→ production engineering research / TECHNOLOGY LANDSCAPE / NON-DANTE-DECISION

architecture/dante-ai-02-1-intelligence-reengineering.md
→ AI-02.1 v0.5 CLOSED / STRUCTURALLY ACCEPTED

architecture/dante-ai-03-context-retrieval-memory.md
→ AI-03 CLOSED / STRUCTURALLY ACCEPTED

architecture/dante-ai-03a-full-context-architecture.md
→ AI-03A CLOSED / C01..C33

architecture/dante-ai-03b-retrieval-memory-architecture.md
→ AI-03B CLOSED / B01..B35

architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md
→ AI-03C CLOSED / MAT-01..MAT-15

architecture/dante-ai-04-productionization-architecture.md
→ AI-04 CLOSED / STRUCTURALLY ACCEPTED

architecture/dante-ai-04a-direct-eval-specification.md
→ AI-04A CLOSED / A01..A30 / EV01..EV20 / DANTE-E01..E14 current

architecture/dante-ai-04b-concrete-runtime-capability-architecture.md
→ AI-04B CLOSED / RT-01..RT-31

architecture/dante-ai-04c-production-assurance-control-plane-operations.md
→ AI-04C CLOSED / PA-01..PA-61

architecture/dante-ai-04-whole-phase-destructive-acceptance.md
→ AI-04 whole-phase CLOSED / WP-01..WP-22

architecture/dante-ai-pre05-cross-phase-hardening.md
→ PRE-AI05 CLOSED / PRE05-H01..H19

workstreams/ai-architecture.md
→ current branch-local routing: AI-05 Whole-System Acceptance + Implementation Blueprint
```

AI-00 remains semantically binding for its inherited/derived baseline. Its original `AI-01 next step` sequencing is historical; later product-form/research/reengineering work has already occurred.

The production-engineering thesis is evidence rather than a normative provider/runtime selection.

### Current compact AI roadmap

```text
AI-00  Semantic & Product Foundation
       COMPLETE

AI-01  Product Form + Production Engineering Research
       COMPLETE

AI-02  Intelligence Runtime Architecture
       COMPLETE / STRUCTURALLY ACCEPTED

AI-03  Context / Retrieval / Memory
       CLOSED / STRUCTURALLY ACCEPTED
       ├ AI-03A Full Context Architecture
       │        CLOSED / C01..C33
       ├ AI-03B Retrieval + Memory Architecture
       │        CLOSED / B01..B35
       └ AI-03C Destructive Validation + Materialization Blueprint
                CLOSED / MAT-01..MAT-15

AI-04  Productionization Architecture
       CLOSED / STRUCTURALLY ACCEPTED
       ├ AI-04A A01..A30 / EV01..EV20
       ├ AI-04B RT-01..RT-31
       ├ AI-04C PA-01..PA-61
       └ Whole-Phase WP-01..WP-22

PRE-AI05  Cross-Phase Hardening
          CLOSED / PRE05-H01..H19
          current core eval DANTE-E01..DANTE-E14

AI-05  Whole-System Acceptance + Implementation Blueprint
       ACTIVE / CURRENT / FINAL ARCHITECTURE-TO-BUILD BOUNDARY

THEN
actual AI implementation workstream(s)
```

The earlier longer AI-00..AI-12 decomposition is historical planning only, not current routing.

### AI-02.1 v0.5 accepted structural architecture

The completed pressure-test program progressed through:

```text
Round I
→ Interaction Session
→ Semantic Query / Projection Gateway
→ Context Engine separation
→ Scenario Workspace
→ ChangeSet / EffectGraph
→ Verifier
→ Attention boundary
→ Context Projection != Disclosure Projection
→ mixed DANTE-native/open-world intelligence
→ ModelTarget + HarnessProfile

Round II
→ cumulative/cross-query disclosure protection
→ causal-loop / oscillation guard
→ Work Supersession
→ BasisManifest + dependency-aware invalidation
→ revocable active-Run validity
→ Attention budgeting
→ cancel Run != undo already-dispatched effects

Final Kill-Test
→ Reference / Target Resolution
→ Policy Composition / Precedence
→ ConsequenceProfile
→ Safe Result Publication
→ temporal Basis validity
→ DANTE representation != external System-of-Record authority
→ sent != delivered != seen != acknowledged != accepted

Last Mega Stress-Test
→ Execution Environment / Isolation boundary
→ WorkContract propagation
→ approval rebinding
→ Basis coherence
→ publication currentness
→ external-agent effect containment
→ mandatory reconciliation survives resource exhaustion
→ surface-aware disclosure / realtime authenticity hardening
→ telemetry/eval purpose/privacy hardening
```

Targeted v0.5 consistency verification covers the new boundary and hardenings and found no additional fundamental responsibility gap.

These are responsibility/runtime contracts, not automatic services, Domain owners or database tables. All completed rounds found no evidence sufficient to reopen Domain, Logical, Physical or PostgreSQL.

AI-02.1 is **CLOSED / STRUCTURALLY ACCEPTED**. That closure does not claim runtime/backend/provider/database implementation PASS.

### AI-03 structurally accepted Context / Retrieval / Memory boundary

AI-03 is closed at the structural architecture level.

Durable sources:

- `architecture/dante-ai-03-context-retrieval-memory.md`;
- `architecture/dante-ai-03a-full-context-architecture.md`;
- `architecture/dante-ai-03b-retrieval-memory-architecture.md`;
- `architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md`.

Accepted closure:

```text
AI-03A Context                         C01..C33
AI-03B Retrieval + Memory              B01..B35
AI-03C Materialization                 MAT-01..MAT-15

Domain/Logical/Physical reopen         NO
PostgreSQL/Alembic change              NO
provider/model selection               NO
runtime/backend implementation         NOT CLAIMED
SC/PSV direct proof                    NOT CLAIMED
```

The accepted Context runtime contracts remain:

```text
ContextPlan
InformationNeed
ContextStrategy
ContextFragment
ContextReadiness
ConsumerContext
ContextManifest
+ inherited BasisManifest
```

AI-03B closes governed retrieval, retrieval guarantees, source standing/currentness, document/large-corpus representation, memory classes/admission/reuse/correction/forgetting/anti-resurrection and provider/cache/index boundaries without creating generic memory authority.

AI-03C closes the physical survival/materialization discipline. In particular:

```text
ARCHITECTURE CONTRACT != PERSISTENCE OWNER
DEFAULT NONCANONICAL PERSISTENCE = NO
SEMANTIC AUTHORITY != FUNCTIONAL ROLE != SURVIVAL != PHYSICAL OWNER
Class-A technical coordination != Class-B durable execution
persistent derivative requires truthful/scalable source basis
derived state may be sacrificial in recovery
async invalidation != current eligibility
ANN is optimization, not prerequisite
derived representation generations do not mix silently
semantic obligation != execution/audit evidence
```

Direct Physical obligations such as SC-017..SC-021 and their PSV counterparts remain unexecuted until a real activated consumer requires them.

### AI-04 closed productionization boundary + PRE-AI05 acceptance

AI-04 is **CLOSED / STRUCTURALLY ACCEPTED**. Its accepted authority includes:

```text
AI-04A  A01..A30 / EV01..EV20
AI-04B  RT-01..RT-31
AI-04C  PA-01..PA-61
WHOLE   WP-01..WP-22
```

The post-closure PRE-AI05 whole-chain audit adds binding `PRE05-H01..H19` without reopening AI-04. It makes Attention/proactivity/causal-loop safety, cumulative cross-work disclosure, recipient/surface/channel publication, scoped-autonomy revalidation, communication-state truth and source-lifecycle-vs-prior-disclosure distinctions explicit through current production/eval traceability.

Current core eval coverage is `DANTE-E01..DANTE-E14`.

Provider/model selection remains evidence-driven. Provider replaceability is binding:

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY
HARNESSPROFILE != PROVIDERBINDING
DANTE FEATURE/BUSINESS CODE != CONCRETE PROVIDER SDK
PROVIDER REPLACEABLE != PROVIDERS IDENTICAL
PROVIDER REPLACEABLE != LOWEST-COMMON-DENOMINATOR PROVIDER USAGE
```

Current route composition is:

```text
DANTE work/capability need
→ ModelTarget / deterministic need
→ eligible qualified route compositions
→ Routing Policy
→ compatible qualified:
   HarnessProfile
   + ProviderBinding
   + feature mode
   + capability projection
   + security/control profile
→ route-specific resource admission
→ current egress authorization
→ Provider Adapter when a model route is selected
→ concrete provider/model/deployment
```

The post-H19 PRE-AI05 acceptance passed 26/26 structural hostile cases, compound collisions, reverse-order composition and refreshed 2026 state-of-the-art regression. It does **not** claim direct provider benchmark, provider selection, production capacity, backend/runtime implementation or database materialization.

### AI-05 current whole-system acceptance + implementation blueprint

AI-05 is now the **ACTIVE / CURRENT** architecture-to-build phase.

Its job is to translate the accepted AI semantics/architecture into exact implementation boundaries and decision-specific proof gates without reopening accepted upstream semantics for convenience. It remains architecture/blueprint work until explicit implementation gates begin.

## 10. Database System of Record

Start here:

- `database/README.md`
- `database/dictionary/README.md`
- `database/dictionary/scope.json`

Current protected-main contract:

```text
PostgreSQL          18.6
Alembic             20260830_09
69 tables
5 views
15 routines
76 triggers
97 physical indexes
69 foreign keys
123 CHECK constraints
```

The pre-Recovery `20260826_08 / 68|5|14|75|95|68|120` baseline is historical.

Permanent consistency invariant:

```text
Database Architecture & Reference
≈ Database Dictionary
≈ SQLAlchemy metadata / mappings
≈ Alembic head
≈ real PostgreSQL schema
```

Current Recovery operation:

- `operations/postgres-recovery-runbook.md`
- executable harnesses under `../infra/local/postgres/recovery/`

## 11. Backend

Application entry point:

- `../apps/backend/README.md`

CP1–CP6 are closed. Post-CP6 backend work proceeds through bounded product/platform workstreams and normal reviewed forward schema evolution when genuinely required.

`feature/access-auth` is a current unmerged full-stack product vertical. The AI architecture branch remains documentation/design/reengineering only; no AI backend implementation, provider integration, persistence schema or runtime activation is claimed here.

## 12. Frontend

Current protected-main frontend documentation:

- `frontend/README.md`
- `frontend/access.md`
- `frontend/design-tokens.md`
- `frontend/localization.md`
- `frontend/terminology.md`
- `frontend/ui-registry.md`
- `frontend/home/`
- `frontend/production-readiness/`

Generic frontend engineering foundation/materialization and pre-backend Access frontend are closed. The whole Access/Auth product vertical remains active on its own bounded branch.

## 13. Active unmerged workstreams

At the 2026-09-01 reconciliation, bounded unmerged work includes:

```text
feature/access-auth             active full-stack product work
feature/home-react              active frontend work
feature/platform-observability  active platform work
feature/ai-architecture         active AI architecture design/reengineering work
```

Additional live refs may exist; live Git refs and each branch's bounded durable truth remain authoritative for later movement.

## 14. Development governance

Primary sources:

- `development/agent-operating-manual.md`
- `development/operating-rules.md`
- `development/documentation-and-handoff.md`
- `development/documentation-lifecycle-policy.md`
- `development/branching-and-environments.md`
- `development/repository-engineering-safety.md`
- `development/testing-and-ci-v0.md`
- `development/toolchain-and-dx-v0.md`

Environment vocabulary remains exactly:

```text
LOCAL
DEV
UAT
PROD
```

Environment != Git branch.

## 15. Persistent truth rules

```text
SELECTED ARCHITECTURE != IMPLEMENTED COMPONENT
DOCUMENTATION PASS != DIRECT IMPLEMENTATION PASS
UNMERGED BRANCH TRUTH != PROTECTED-main TRUTH
HISTORICAL 18.4 EVIDENCE != CURRENT 18.6 EXECUTION CLAIM
CLIENT LOCAL STATE != CANONICAL ACCEPTED EFFECT
DATABASE MATERIALIZATION != PRODUCT APPLICATION IMPLEMENTATION
RESEARCH TECHNOLOGY != DANTE IMPLEMENTATION SELECTION
MODEL/PROVIDER OUTPUT != CANONICAL EFFECT
MODEL OUTPUT != PUBLISHABLE OUTPUT
DISPLAY NAME != EFFECT TARGET
SCENARIO STATE != CANONICAL CURRENT STATE
INTERACTION SESSION != RUN != WORKER
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
RUN-START AUTONOMY != PERPETUAL AUTONOMY
DANTE REPRESENTATION != EXTERNAL SYSTEM-OF-RECORD AUTHORITY
EXECUTION ENVIRONMENT != MANDATORY SANDBOX/CONTAINER
CONSUMER CONTEXT != CONTEXT MANIFEST
CONTEXT MANIFEST != BASIS MANIFEST
SOURCE STANDING != DOMAIN AUTHORITY
MODEL-DISCOVERED NEED != SCOPE EXPANSION
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
HARNESSPROFILE != PROVIDERBINDING
DANTE FEATURE/BUSINESS CODE != CONCRETE PROVIDER SDK
PROVIDER REPLACEABLE != LOWEST-COMMON-DENOMINATOR PROVIDER USAGE
ATTENTION DECISION != PROACTIVE WORK ADMISSION != EFFECT AUTHORIZATION
RECIPIENT != SURFACE != CHANNEL
SAFE SINGLE DISCLOSURE != AUTOMATICALLY SAFE CUMULATIVE DISCLOSURE
SOURCE FUTURE ELIGIBILITY != PRIOR DISCLOSURE OCCURRENCE
ENVIRONMENT != GIT BRANCH
TEMPORARY HANDOFF != DURABLE DOCUMENTATION
```

The goal is a repository a new developer or agent can understand from current sources without reconstructing obsolete operational chronology.