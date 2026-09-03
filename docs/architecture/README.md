# DANTE Architecture Index

- **Status:** CURRENT / AUTHORITATIVE NAVIGATION
- **Last reconciled:** 2026-09-03

This file describes current architecture truth directly. Historical candidates, hardenings and phase-time status remain evidence in their owning documents/Git history and do not override this index.

## 1. Current architecture state

```text
Domain Model                         CLOSED
Logical Model                        CLOSED / 57 OF 57 / REMOTE QA PASS
WD-03 / WD-05                        PASS
Pre-Physical coherence               CLOSED / FINAL QA PASS
Physical target                      CLOSED / ACCEPTED
Engineering Foundation               CLOSED / ACCEPTED
Frontend Engineering Foundation      CLOSED / INTEGRATED VIA PR #22
Frontend Materialization             CLOSED / PASS / INTEGRATED VIA PR #28
Backend CP1–CP5 scaffold             CLOSED / DIRECT QA / INTEGRATED VIA PR #24
Backend CP6 PostgreSQL database       CLOSED / DIRECT QA / INTEGRATED VIA PR #42
PostgreSQL architecture              18 major family / sole canonical persistence + material-history authority
Current PostgreSQL patch             18.6
Current Alembic head                 20260830_09
Current DB topology                  69 tables / 5 views / 15 routines / 76 triggers / 97 indexes / 69 FKs / 123 CHECKs
PostgreSQL local Recovery            CP01–CP07 LOCAL PASS / CLOSED / INTEGRATED VIA PR #47
Full Access/Auth product vertical    ACTIVE / UNMERGED ON feature/access-auth

AI-00                                COMPLETE
AI-02.1                              CLOSED / STRUCTURALLY ACCEPTED
AI-03                                CLOSED / C01..C33 / B01..B35 / MAT-01..MAT-15
AI-04                                CLOSED / A01..A30 / EV01..EV20 / RT-01..RT-31 / PA-01..PA-61 / WP-01..WP-22
PRE-AI05                             CLOSED / PRE05-H01..H19
AI-05A                               CLOSED / BD-01..BD-41
AI-05B                               CLOSED / AI05B-H01..H15 / B05-01..B05-50 PASS
AI-05 whole-system                   CLOSED / STRUCTURALLY ACCEPTED
POST-AI05 hardening                  CLOSED / POST05-H01..H25
POST-AI05 final mega test            PASS / MKT-001..100 / C01..20 / reverse / Product simulation replay
AI architecture design/reengineering CLOSED / STRUCTURALLY ACCEPTED
AI implementation                    ACTIVE ON feature/ai-implementation
I0 / I1 / I2                         CLOSED / PASS
I3/C3                                DEFERRED / WAITING OWNER DATA + SEAMS
C6 / C7                              CLOSED / PASS
C8 / P1 provider admission           CLOSED / OPENAI NATIVE + RESPONSES + GPT-5.6 TERRA ADMITTED FOR QUALIFICATION
AI current next action               C9 — admitted inactive provider adapter/binding + conformance/live compatibility
```

Protected `main` remains the integrated authority for shared closed foundations. `feature/ai-architecture` retains the accepted architecture authority/evidence. `feature/ai-implementation` contains newer bounded implementation truth until normal protected-main integration.

## 2. Current AI implementation authority

Implementation remains governed by:

- [`dante-ai-implementation-baseline-final.md`](dante-ai-implementation-baseline-final.md) — **CURRENT / ACCEPTED implementation-facing architecture authority**;
- [`dante-ai-post05-final-mega-acceptance.md`](dante-ai-post05-final-mega-acceptance.md) — final independent structural acceptance evidence;
- [`../workstreams/ai-implementation.md`](../workstreams/ai-implementation.md) — current branch-local implementation state and validated checkpoints;
- [`../workstreams/ai-provider-candidate-admission-2026-09.md`](../workstreams/ai-provider-candidate-admission-2026-09.md) — current C8/P1 provider candidate admission evidence;
- [`../workstreams/ai-architecture.md`](../workstreams/ai-architecture.md) — closed branch-local architecture workstream record.

The final implementation baseline is intentionally an implementation-entry authority. Its phase-time `Implementation: NONE YET` / `Current next action: I0` statements describe the accepted entry point and are superseded for current execution status by material repository truth and the active implementation workstream; its architecture contracts remain binding unless deliberately evolved through normal governance.

The temporary AI live handoff has been deleted after durable knowledge coverage.

Historical AI-05B candidates, bounded hardenings, implementation baseline v1/v2/v3 and post-AI05 failure reports are evidence only. They must not override the final baseline.

## 3. AI authority layering

Read upstream architecture when changing the relevant semantics:

- [`dante-ai-foundation.md`](dante-ai-foundation.md) — AI-00 semantic/architectural foundation;
- [`ai-production-engineering-state-of-the-art-2026.md`](ai-production-engineering-state-of-the-art-2026.md) — research / technology landscape / NON-DANTE-DECISION;
- [`dante-ai-02-1-intelligence-reengineering.md`](dante-ai-02-1-intelligence-reengineering.md) — AI-02.1 accepted runtime responsibility architecture;
- [`dante-ai-03-context-retrieval-memory.md`](dante-ai-03-context-retrieval-memory.md) — AI-03 master closure;
- [`dante-ai-03a-full-context-architecture.md`](dante-ai-03a-full-context-architecture.md) — Context C01..C33;
- [`dante-ai-03b-retrieval-memory-architecture.md`](dante-ai-03b-retrieval-memory-architecture.md) — Retrieval/Memory B01..B35;
- [`dante-ai-03c-destructive-validation-materialization-blueprint.md`](dante-ai-03c-destructive-validation-materialization-blueprint.md) — Materialization MAT-01..MAT-15;
- [`dante-ai-04-productionization-architecture.md`](dante-ai-04-productionization-architecture.md) — productionization master;
- [`dante-ai-04a-direct-eval-specification.md`](dante-ai-04a-direct-eval-specification.md) — A01..A30 / EV01..EV20 / DANTE-E01..E14;
- [`dante-ai-04b-concrete-runtime-capability-architecture.md`](dante-ai-04b-concrete-runtime-capability-architecture.md) — RT-01..RT-31;
- [`dante-ai-04c-production-assurance-control-plane-operations.md`](dante-ai-04c-production-assurance-control-plane-operations.md) — PA-01..PA-61;
- [`dante-ai-04-whole-phase-destructive-acceptance.md`](dante-ai-04-whole-phase-destructive-acceptance.md) — WP-01..WP-22;
- [`dante-ai-pre05-cross-phase-hardening.md`](dante-ai-pre05-cross-phase-hardening.md) — PRE05-H01..H19;
- [`dante-ai-05a-whole-system-build-boundary-acceptance.md`](dante-ai-05a-whole-system-build-boundary-acceptance.md) — AI-05A closure;
- [`dante-ai-05b-concrete-implementation-blueprint-acceptance.md`](dante-ai-05b-concrete-implementation-blueprint-acceptance.md) — AI-05B closure;
- [`dante-ai-05-whole-system-destructive-acceptance.md`](dante-ai-05-whole-system-destructive-acceptance.md) — AI-05 closure;
- [`dante-ai-post05-final-mega-acceptance.md`](dante-ai-post05-final-mega-acceptance.md) — final independent post-closure acceptance.

`ai-context-runtime-boundaries.md` remains **HISTORICAL / PRE-PHYSICAL REFERENCE** and is not current runtime authority.

## 4. Final build boundary

The accepted first implementation shape is a capability-first modular monolith:

```text
modules/search
→ independent deterministic Global Search/discovery
→ permission-safe bounded read projection
→ no canonical mutation authority

modules/intelligence
→ Work / Context / Reference Resolution / Semantic Query / Retrieval orchestration
→ optional governed ModelAccess
→ Verification / Result Maturity / explicit NO_EFFECT / Safe Publication
→ no raw database/canonical ownership

provider SDK/protocol
→ private admitted outbound adapter behind DANTE-owned ModelAccessPort

bootstrap
→ composition and lifecycle only

platform
→ shared technical mechanics only

tooling/ai-evals
→ qualification tooling outside production request path
```

Binding separations include:

```text
GLOBAL SEARCH != INTELLIGENCE
SEARCH RESULT / CURSOR / TARGET REF != AUTHORIZATION
SEMANTIC QUERY GATEWAY != INTELLIGENCE-OWNED CROSS-CAPABILITY SQL
Context != Retrieval != Memory
RetrievalCandidate != ContextFragment
ContextManifest != BasisManifest
DATA != INSTRUCTION
MASKING / REDACTION != SEMANTIC EQUIVALENCE
MODEL OUTPUT != PUBLISHABLE OUTPUT
PROVIDER COMPLETED != VERIFIED != PUBLISHABLE
PROVIDER FAILURE != DISCLOSURE DID NOT HAPPEN
AUXILIARY MODEL CALL != FREE PROVIDER CALL
CANDIDATE ADMISSION != PRODUCTION QUALIFICATION
DEFAULT NONCANONICAL PERSISTENCE = NO
BUILD-READY != INTEGRATION-READY != ACTIVATION-READY
```

## 5. First implementation vertical

```text
GLOBAL SEARCH subset
+ READ-ONLY ASK DANTE

surface          private authenticated in-app
interaction      single-turn
runtime          inline / request-owned
consequence      READ_ONLY
public streaming OFF
background       OFF
durable resume   OFF
consequential mutation OFF
```

Read-only work still finalizes through an explicit Effect boundary:

```text
READ_ONLY + no proposed effects
→ EffectOutcome.NO_EFFECT
```

No generic AI conversation/Run/Context/Memory/SearchResult/embedding persistence is justified by this envelope.

## 6. Provider / qualification posture

C8/P1 has admitted exactly one initial qualification candidate:

```text
provider          OpenAI native API
API               Responses API
model candidate   gpt-5.6-terra
status            ADMITTED FOR QUALIFICATION ONLY
```

Current evidence record:

- [`../workstreams/ai-provider-candidate-admission-2026-09.md`](../workstreams/ai-provider-candidate-admission-2026-09.md).

Retained non-admitted challengers:

```text
Claude Sonnet 5
Gemini 3.8 Flash on Vertex AI
```

Correct sequence remains:

```text
candidate shortlist
→ candidate admission                         C8 / CLOSED
→ inactive adapter/binding                    C9 / NEXT
→ adapter conformance
→ live compatibility with synthetic/public/minimized test data
→ direct DANTE eval on production-owned composition
→ applicable security/privacy/capacity/economics evidence
→ qualification
→ promotion
```

Admission does **not** establish production qualification, private-data eligibility, entitlement, availability or rollout status. Qualification traffic is real disclosure. Auxiliary model calls use the same governed ModelAccess/egress/resource/eval boundary.

Applicable SC/PSV direct proofs remain activation gates; missing applicable evidence is not `N/A`.

## 7. Persistence / database direction

```text
PostgreSQL 18 major family
= sole canonical persistence + material-history authority

current patch
= 18.6

current Alembic head
= 20260830_09
```

I0-I2/C6/C7/C8 introduced no database/Alembic change.

Specialist components remain trigger-gated: FTS/pg_trgm, pgvector/ANN/embeddings, Restate, R2, MCP/A2A, Execution Environment, commercial/shared usage ledger, cross-Run disclosure accounting and AI memory persistence.

## 8. Other architecture entry points

- [`system-overview.md`](system-overview.md) — current system/component/authority overview;
- [`technical-decisions.md`](technical-decisions.md) — current technical decision register;
- [`domain-model-logical-readiness.md`](domain-model-logical-readiness.md) — satisfied Domain → Logical compatibility contract;
- [`../domain/README.md`](../domain/README.md) — Domain authority;
- [`../logical-model/README.md`](../logical-model/README.md) — Logical Model authority;
- [`../physical-model/README.md`](../physical-model/README.md) — Physical target;
- [`../database/README.md`](../database/README.md) — concrete PostgreSQL System of Record;
- [`../decisions/`](../decisions/) — ADR authority;
- [`../development/engineering-foundation-v0.md`](../development/engineering-foundation-v0.md) — backend engineering foundation;
- [`../frontend/README.md`](../frontend/README.md) — frontend entry point.

Important persistence ADRs:

- `ADR-007-domain-model-informed-persistence-boundaries.md`;
- `ADR-010-postgresql-persistence-constitution.md`;
- `ADR-003-primary-database.md` where explicitly historical.

Important frontend ADRs:

- `ADR-008-frontend-engineering-stack.md`;
- `ADR-009-frontend-architecture-boundaries.md`.

## 9. Current next action

Architecture design/reengineering remains closed. Current implementation has reached the provider qualification lane.

```text
NEXT
→ C9
→ admitted inactive OpenAI Responses / gpt-5.6-terra binding
→ provider adapter + conformance
→ live compatibility only on synthetic/public/minimized data
```

C9 does not activate production Search/Ask, private-data routing or any new persistence. I3/C3 remains deferred until real owner data/seams are integration-ready and must converge before I6.