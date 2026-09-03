# DANTE Documentation Index

- **Status:** CURRENT NAVIGATION / AUTHORITY INDEX
- **Last reconciled:** 2026-09-03

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

5. active or closed unmerged branch-local durable truth
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
CURRENT PROTECTED-MAIN ALEMBIC        20260830_09
CURRENT PROTECTED-MAIN DB TOPOLOGY    69/5/15/76/97/69/123
POSTGRESQL LOCAL RECOVERY             CP01–CP07 LOCAL PASS / CLOSED / PR #47
REMOTE BACKUP PROVIDER                TBD / NOT ACTIVATED
PRODUCTION/CLOUD RECOVERY             NOT CLAIMED
ACCESS PRE-BACKEND FRONTEND           CLOSED / ACCEPTED / RELEASE-HARDENED
FULL ACCESS/AUTH PRODUCT VERTICAL     ACTIVE UNMERGED WORKSTREAM

AI-00 FOUNDATION                      COMPLETE
AI-01 PRODUCT/PRODUCTION RESEARCH     COMPLETE
AI-02.1 RUNTIME ARCHITECTURE          CLOSED / STRUCTURALLY ACCEPTED
AI-03 CONTEXT/RETRIEVAL/MEMORY        CLOSED / C01..C33 / B01..B35 / MAT-01..MAT-15
AI-04 PRODUCTIONIZATION               CLOSED / A01..A30 / EV01..EV20 / RT-01..RT-31 / PA-01..PA-61 / WP-01..WP-22
PRE-AI05                              CLOSED / PRE05-H01..H19
AI-05A                                CLOSED / BD-01..BD-41
AI-05B                                CLOSED / AI05B-H01..H15 / B05-01..B05-50 PASS
AI-05 WHOLE-SYSTEM                    CLOSED / STRUCTURALLY ACCEPTED
POST-AI05 HARDENING                   CLOSED / POST05-H01..H25
POST-AI05 MEGA TEST                   PASS / MKT-001..100 / C01..20 / reverse / simulations
AI ARCHITECTURE DESIGN                CLOSED / STRUCTURALLY ACCEPTED

AI IMPLEMENTATION BRANCH              feature/ai-implementation
I0                                    CLOSED / PASS
I1                                    CLOSED / PASS
I2                                    CLOSED / PASS
I3/C3                                 DEFERRED / WAITING OWNER DATA + SEAMS
C6 CONTROL/SAFETY/PUBLICATION         CLOSED / PASS
C7 ROUTE-CONFIG IDENTITY/LOADER       CLOSED / PASS
AI NEXT EXECUTABLE                    C8/I4 provider candidate admission
```

For exact current project state, read `PROJECT-STATUS.md`.

## 3. Mandatory project entry points

General continuation order:

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
11. current subsystem/workstream sources relevant to the task
12. current branch/ref and relation to protected `main`

Repository truth beats conversation memory.

## 4. Current AI continuation

For AI implementation on `feature/ai-implementation`, read in this order:

1. `architecture/dante-ai-implementation-baseline-final.md` — **CURRENT / ACCEPTED implementation-facing authority**;
2. `workstreams/ai-implementation.md` — current branch-local implementation state, validated checkpoints and next executable gate;
3. `ROADMAP.md` — current execution overlay and cross-workstream convergence;
4. `PROJECT-STATUS.md` — project-level current state;
5. `architecture/dante-ai-post05-final-mega-acceptance.md` — final independent acceptance evidence;
6. `workstreams/ai-architecture.md` — closed architecture workstream record and handoff evidence;
7. upstream AI-02/03/04/PRE05/AI-05 authorities only when changing or validating those contracts.

The temporary `workstreams/ai-architecture-live-handoff.md` has been deleted after durable knowledge coverage.

Current branch-local implementation state:

```text
I0 CLOSED / PASS
I1 CLOSED / PASS
I2 CLOSED / PASS
I3/C3 DEFERRED / WAITING OWNER DATA + SEAMS
C6 CLOSED / PASS
C7 CLOSED / PASS

NEXT EXECUTABLE
C8 / I4 provider candidate-admission decision

I3/C3 remains a parallel conditional lane and must converge before I6
when the first vertical requires its real deterministic source/query path.
```

No provider/model/SDK is admitted merely by architecture closure or by I0-I2/C6/C7 completion.

## 5. Product

Entry point:

- `product/README.md`

Key durable sources include:

- `product/product-identity-and-north-star.md`;
- `product/scope.md`;
- accepted `product/v1-*.md` specifications;
- `product/feature-discovery-simulation-2026-08.md`;
- `product/multi-actor-collaboration-discovery-simulation-2026-08.md`;
- `product/multi-actor-collaboration-research-2026-08.md`.

Research/simulation material is evidence and product-discovery authority where stated; it is not automatic Domain schema authority.

## 6. Domain Model

Entry point:

- `domain/README.md`

The Domain Model is **CLOSED / semantically complete for current accepted scope**. Current concept semantics live under `domain/concepts/`. Historical validation continuations remain evidence only.

## 7. Logical Model

Entry point:

- `logical-model/README.md`

The Logical Model is **CLOSED / 57 of 57 classified / REMOTE QA PASS**. Binding `WL-H01..WL-H12` remain implementation regression contracts unless deliberately superseded.

## 8. Physical Model / Database

Physical entry point:

- `physical-model/README.md`

Database entry point:

- `database/README.md`
- `database/dictionary/`

Current selected target:

```text
PostgreSQL 18 major family
sole canonical persistence + material-history authority
current patch 18.6
current Alembic head 20260830_09
```

A structural DB change follows the permanent same-change rule: migration + mappings + Dictionary + human reference + tests + governed generated/operational artifacts.

## 9. Architecture / AI

Architecture entry points:

- `architecture/README.md`;
- `architecture/system-overview.md`;
- `architecture/technical-decisions.md`;
- `decisions/`.

Current AI implementation authority:

- `architecture/dante-ai-implementation-baseline-final.md`.

Current AI implementation workstream:

- `workstreams/ai-implementation.md`.

Final post-AI05 acceptance:

- `architecture/dante-ai-post05-final-mega-acceptance.md`.

Important implementation separations include:

```text
GLOBAL SEARCH != INTELLIGENCE
SEMANTIC QUERY GATEWAY != INTELLIGENCE-OWNED CROSS-CAPABILITY SQL
SEARCH RESULT / CURSOR / TARGET REF != AUTHORIZATION
Context != Retrieval != Memory
RetrievalCandidate != ContextFragment
DATA != INSTRUCTION
MODEL OUTPUT != PUBLISHABLE OUTPUT
PROVIDER COMPLETED != VERIFIED != PUBLISHABLE
CANDIDATE ADMISSION != PRODUCTION QUALIFICATION
DEFAULT NONCANONICAL PERSISTENCE = NO
BUILD-READY != INTEGRATION-READY != ACTIVATION-READY
```

## 10. Frontend

Entry point:

- `frontend/README.md`

Frontend Foundation and Materialization are closed/integrated. The full Access/Auth product vertical remains a separate active unmerged workstream.

## 11. Workstreams

Entry point:

- `workstreams/README.md`

Current bounded branch state includes active Access/Auth, Home React, platform observability and AI implementation work. `feature/ai-architecture` remains closed architecture authority/evidence; `feature/ai-implementation` owns newer branch-local AI implementation truth.

## 12. Documentation lifecycle

Current specifications contain current truth. Historical failure/pass chronology belongs in explicit evidence/archive/Git history. Temporary live/session handoffs do not merge to protected `main`.

Normative lifecycle sources:

- `development/documentation-and-handoff.md`;
- `development/documentation-lifecycle-policy.md`;
- `development/repository-engineering-safety.md`.

```text
SELECTED != IMPLEMENTED
IMPLEMENTED != PROVEN
ARCHITECTURE PASS != RUNTIME PASS
UNMERGED BRANCH TRUTH != PROTECTED-main TRUTH
TEMPORARY HANDOFF != DURABLE DOCUMENTATION
```