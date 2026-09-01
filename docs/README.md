# DANTE Documentation Index

- **Status:** CURRENT NAVIGATION / AUTHORITY INDEX
- **Last reconciled:** 2026-09-01

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

An unmerged branch may contain newer truth for its own scope, but it is not protected-main authority until integration. Once merged, CURRENT documentation must describe the protected-main state rather than continuing to present the integrated branch as a candidate.

## 2. Current lifecycle

```text
PRODUCT / NORTH STAR                 CURRENT
DOMAIN MODEL                         CLOSED
LOGICAL MODEL                        CLOSED / 57 OF 57 / REMOTE QA PASS
PRE-PHYSICAL COHERENCE               CLOSED / FINAL QA PASS
PHYSICAL TARGET                      CLOSED / ACCEPTED
ENGINEERING FOUNDATION               CLOSED / ACCEPTED
FRONTEND ENGINEERING FOUNDATION      CLOSED / INTEGRATED VIA PR #22
FRONTEND MATERIALIZATION             CLOSED / PASS / INTEGRATED VIA PR #28
BACKEND CP1–CP5 SCAFFOLD             CLOSED / DIRECT QA / INTEGRATED VIA PR #24
BACKEND CP6 DATABASE                 CLOSED / DIRECT QA / INTEGRATED VIA PR #42
CURRENT POSTGRESQL                   18.6
HISTORICAL PRE-RECOVERY ALEMBIC      20260826_08
HISTORICAL PRE-RECOVERY DB TOPOLOGY  68/5/14/75/95/68/120
CURRENT PROTECTED-MAIN ALEMBIC       20260830_09
CURRENT PROTECTED-MAIN DB TOPOLOGY   69/5/15/76/97/69/123
POSTGRESQL LOCAL RECOVERY            CP01–CP07 LOCAL PASS / CLOSED / INTEGRATED VIA PR #47
REMOTE BACKUP PROVIDER               TBD / NOT ACTIVATED
PRODUCTION/CLOUD RECOVERY            NOT CLAIMED
ACCESS PRE-BACKEND FRONTEND          CLOSED / ACCEPTED / RELEASE-HARDENED
FULL ACCESS/AUTH PRODUCT VERTICAL    ACTIVE UNMERGED WORKSTREAM / NOT CLAIMED CLOSED
AI ARCHITECTURE                      ACTIVE / AI-02.1 v0.4 REENGINEERING / NO IMPLEMENTATION CLAIM
AI-03 CONTEXT/RETRIEVAL/MEMORY       NOT STARTED / BLOCKED UNTIL AI-02.1 ACCEPTANCE
```

For exact current state, read `PROJECT-STATUS.md` rather than reconstructing status from historical workstream/checkpoint files.

## 3. Mandatory project entry points

Read in this order for general project continuation:

1. `../README.md`
2. `README.md` — this index
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

## 4. Documentation lifecycle

Current documentation is not an append-only diary.

Temporary branch-operational files such as live/session/resume handoffs may exist while a branch is active, but they **must not merge into protected `main`**. Before branch integration:

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
→ repair links to any deliberately removed workstream overlays
→ keep archive history non-authoritative
```

Normative lifecycle source:

- `development/documentation-lifecycle-policy.md`

Archive boundary:

- `archive/README.md`

`docs/archive/` is selective non-authoritative history, not a backup mirror. Git remains the complete recoverable history.

Frozen/read-only split documents may be recomposed only through **lossless knowledge coverage**. Do not summarize away requirements, invariants, accepted decisions, continuing rationale, assumptions, counterexamples or important evidence merely to reduce file count.

## 5. Product

Entry point:

- `product/README.md`

Key durable product-definition sources include:

- `product/product-identity-and-north-star.md`
- `product/scope.md`
- accepted `product/v1-*.md` specifications where still current

Research/simulation material is evidence, not automatic current product truth.

## 6. Domain Model

Current entry point:

- `domain/README.md`

The Domain Model is **CLOSED / semantically complete for current accepted scope**.

Current concept-level semantics remain under:

- `domain/concepts/`

Validation methodology/evidence remains under the Domain directory and its checkpoints/history.

Important current rule:

```text
domain/README-part-2.md ... domain/README-part-20.md
= HISTORICAL / EVIDENCE ONLY
```

They preserve evolution and closure chronology; they are no longer required to determine current Domain status.

Other Domain `*-part-N.md` families are classified by purpose:

- concept/reference continuations may contain durable specification payload and remain part of that logical specification until proven safe to compact;
- validation/checkpoint continuations are evidence/history unless explicitly owned as a current contract;
- chronology alone does not create higher authority.

Do not infer a semantic kernel primitive merely from UI, product or persistence naming.

## 7. Logical Model

Current entry point:

- `logical-model/README.md`

The Logical Model is **CLOSED / 57 of 57 classified / REMOTE QA PASS**.

Primary integrated contract/evidence:

- `logical-model/whole-logical-model-v1.md`
- `logical-model/checkpoints/whole-logical-v1-validation.md`
- `logical-model/checkpoints/whole-logical-v1-remote-qa.md`

The Whole content file was written before its separate remote-QA activation, so any embedded `PENDING`/`CLEARANCE READY` banner is phase-time state. The later remote-QA closure owns the final activation status.

Binding hardenings `WL-H01..WL-H12` remain implementation regression contracts unless deliberately superseded.

Logical split registers/ledgers such as decision/assumption, representation, test-corpus and traceability continuations are retained because they contain detailed rationale, assumptions, rejected alternatives and tests not safely reducible to the Whole summary.

## 8. Physical Model

Entry point:

- `physical-model/README.md`

Current selected target:

```text
PostgreSQL 18 major family
sole canonical persistence + material-history authority
```

PostgreSQL 18.4 remains historical exact phase-time Physical/CP2/CP3 evidence. Current repository/database patch is 18.6. Patch maintenance inside major line 18 does not reopen the architecture.

The accepted LOCAL Recovery evolution is integrated into protected `main` via PR #47. Remote backup/cloud recovery remains a separate unactivated boundary.

Specialist capability activation remains trigger-based and direct-validation-specific.

## 9. Architecture and decisions

Entry points:

- `architecture/README.md`
- `architecture/system-overview.md`
- `architecture/dante-ai-foundation.md` — branch-local AI-00 consolidated semantic/architectural baseline; inherited constraints remain active
- `architecture/ai-production-engineering-state-of-the-art-2026.md` — branch-local production AI/agent engineering research thesis; state-of-the-art evidence plus explicit DANTE applicability boundary, **not** the final DANTE Intelligence Architecture
- `architecture/dante-ai-02-1-intelligence-reengineering.md` — **current active AI-02.1 checkpoint**; v0.4 after three official pressure-test rounds, **NOT CLOSED** pending one last mega stress-test and the remaining pre-AI-03 acceptance
- `architecture/technical-decisions.md`
- `architecture/domain-model-logical-readiness.md`
- `decisions/`

Current architecture docs state current post-CP6 architecture directly. Phase reviews/QA/readiness continuations are evidence according to their explicit lifecycle role.

The AI foundation consumes current Product / Domain / Logical / Physical / Database authority and separates inherited constraints, derived implications and intentionally open AI-specific choices. It does not authorize database evolution or implementation.

The production-engineering thesis is research evidence rather than a normative DANTE design. It records current industry techniques, technology challengers, failure models and DANTE-specific applicability constraints such as API-first frontier intelligence and no foundation-model-training / no large always-on self-hosted frontier baseline. Exact provider/model/SDK/runtime selection remains deferred to later evidence-driven architecture work.

AI-02.1 owns the active branch-local reengineering checkpoint.

Round I introduced:

```text
Interaction Session
Semantic Query / Projection Gateway
Context Engine separation
Simulation Workspace
ChangeSet / EffectGraph
Verifier/Auditor
Proactivity/Attention
recipient-aware Disclosure Projection
mixed DANTE-native/open-world intelligence
ModelTarget + HarnessProfile
```

Round II hardened that model with:

```text
cumulative / cross-query disclosure protection
causal-loop / oscillation guard
Work Supersession
BasisManifest + dependency-aware invalidation
revocable active-Run validity
Attention budgeting
cancel Run != undo already-dispatched effects
```

The Final Kill-Test then added the v0.4 requirements:

```text
Reference / Target Resolution Gate
Policy Composition / Precedence
ConsequenceProfile
Safe Result Publication / Streaming Gate
BasisManifest temporal validity
DANTE representation != external institutional System-of-Record authority
sent != delivered != seen != acknowledged != accepted
```

These are responsibility boundaries/contracts, not automatic services, Domain owners or database tables. The three completed rounds found no evidence sufficient to reopen Domain, Logical, Physical or PostgreSQL.

Important persistence ADRs:

- `decisions/ADR-007-domain-model-informed-persistence-boundaries.md`
- `decisions/ADR-010-postgresql-persistence-constitution.md`
- `decisions/ADR-003-primary-database.md` for historical PostgreSQL-selection rationale where explicitly historical

Important frontend ADRs:

- `decisions/ADR-008-frontend-engineering-stack.md`
- `decisions/ADR-009-frontend-architecture-boundaries.md`

## 10. Database System of Record

Start here:

- `database/README.md`
- `database/dictionary/README.md`
- `database/dictionary/scope.json`

Current protected-main database contract:

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

The pre-recovery CP6 baseline `20260826_08 / 68|5|14|75|95|68|120` is historical. PR #47 integrated the `20260830_09` Recovery evolution into protected `main`.

The machine-readable Dictionary is reconciled to the current `20260830_09` contract.

Permanent consistency invariant:

```text
Database Architecture & Reference
≈ Database Dictionary
≈ SQLAlchemy metadata / mappings
≈ Alembic head
≈ real PostgreSQL schema
```

The human-readable Database Architecture & Reference remains one frozen logical payload physically split across `database/dante-postgresql-database.md` and its continuation parts. It may be reorganized only through lossless content-equivalence/knowledge-coverage QA.

CP6 final acceptance:

- `development/backend-cp6-05-whole-database-qa.md`

Current Recovery operation:

- `operations/postgres-recovery-runbook.md`
- executable harnesses under `../infra/local/postgres/recovery/`

Historical branch records:

- `archive/branches/2026-08-feature-logical-postgresql.md` — NON-AUTHORITATIVE
- `archive/branches/2026-08-feature-postgres-recovery.md` — NON-AUTHORITATIVE

## 11. Backend

Application documentation:

- `../apps/backend/README.md`

Durable backend contracts include:

- `development/backend-cp1-contract.md`
- `development/backend-cp2-postgres-contract.md`
- `development/backend-cp3-persistence-contract.md`
- `development/backend-cp4-ci-contract.md`
- `development/backend-cp6-01-concrete-persistence-coverage.md`
- `development/backend-cp6-01-concrete-persistence-coverage-part-2.md`
- `development/backend-cp6-01-concrete-persistence-coverage-closure.md`
- `development/backend-cp6-02-postgresql-persistence-constitution.md`
- `development/backend-cp6-02-postgresql-persistence-constitution-closure.md`
- `development/backend-cp6-03-gate-03-closure.md`
- `development/backend-cp6-05-whole-database-qa.md`

CP1–CP6 are closed. Text saying CP6-03 is active, Gate 03 is unearned, CP6-04 is next or protected-main integration is pending is historical unless explicitly scoped to the phase-time record.

Post-CP6 backend work is active on bounded unmerged workstreams where authorized; `feature/access-auth` is one such current branch. Branch-local authority owns its exact state until integration.

The AI architecture branch remains documentation/design/reengineering only. AI-00, the production-engineering research and AI-02.1 are architecture/evidence artifacts; no AI backend implementation, provider integration, persistence schema or runtime activation is claimed by this index.

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

Generic frontend engineering foundation/materialization is closed/integrated.

### Access frontend baseline

The completed pre-backend Access frontend materialization is the accepted Web baseline for the active full-stack Access/Auth product vertical.

Accepted checkpoints:

```text
AF-01D  shell completion / professional polish      PASS
AF-02A  complete pre-backend frontend state graph   PASS
AF-02B  downstream surface hardening                PASS
AF-03A  release-hardening viewport matrix           PASS
```

Current authority:

- `frontend/access.md`
- current `../apps/web/src/features/access/` implementation/tests

The whole Access/Auth product vertical is **not claimed closed by this index**. A real unmerged `feature/access-auth` workstream is active; use its branch-local durable docs/code/tests for its exact implementation state.

Historical branch narrative:

- `archive/branches/2026-08-feature-access-frontend.md` — NON-AUTHORITATIVE

No Access live/session handoff is current authority after branch closure.

## 13. Workstream records

Entry point:

- `workstreams/README.md`

On protected `main`, workstream files are durable records/evidence, not active chat handoffs.

Closed records include Domain, Logical, Pre-Physical, Physical, Engineering Foundation, Frontend Foundation/Materialization, backend scaffold/CP6 and PostgreSQL Recovery as applicable.

PostgreSQL Recovery is closed and integrated through PR #47; its current operational authority is Database SoR + operator runbook + executable harnesses, while `archive/branches/2026-08-feature-postgres-recovery.md` retains the single non-authoritative branch history.

Active unmerged workstream records remain branch-local until integration.

At the 2026-09-01 reconciliation, bounded unmerged work includes `feature/access-auth`, `feature/home-react`, `feature/platform-observability` and `feature/ai-architecture`; additional live refs may exist and remain authoritative for their own later changes. The AI branch is documentation/design/reengineering-only with AI-02.1 v0.4 active and not closed.

## 14. Development governance

Primary sources:

- `development/agent-operating-manual.md`
- `development/operating-rules.md`
- `development/documentation-and-handoff.md`
- `development/documentation-lifecycle-policy.md`
- `development/branching-and-environments.md`
- `development/repository-engineering-safety.md`
- `development/local-backend-workstation-bootstrap.md`
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

## 15. Protected-main integration truth

Effective protected-main policy requires normal PR-based integration and repository-enforced current checks.

Current required contexts:

```text
Backend CI Gate
Dependency Review
Frontend CI Gate
```

Current repository rules, not an outdated prose snapshot, are effective enforcement. Do not use squash/rebase/force-push or ruleset weakening to bypass integration policy.

## 16. Evidence and current claims

Executable truth beats documentation claims.

Historical successful runs remain evidence for the exact commit/environment on which they executed; later patch/runtime/schema claims require evidence appropriate to the later state.

No blanket semantic/direct-pass claim is inferred merely because a technology was selected or a workflow exists.

AI follows the same rule: a provider feature page, SDK capability or written architecture does not prove DANTE AI behavior until the relevant implementation and scenarios are directly tested. A research classification such as `STRONG DEFAULT`, `CHALLENGER`, `WATCH` or `ANTI-DEFAULT` is not an implementation status or accepted technology selection.

AI-02.1 Round I, Round II and the Final Kill-Test are architecture evidence only. The v0.4 fixes remain subject to one last mega stress-test; `v0.4` is not a runtime PASS and does not close the phase.

## 17. Brand / UX / prototypes

Brand:

- `brand/README.md`

UX:

- `ux/README.md`

Prototypes live outside production runtime authority. Prototype/UI exploration does not automatically define production architecture, Domain semantics or backend behavior.

## 18. Historical material

Use:

- `archive/README.md`

Everything under `archive/` is non-authoritative unless a current source explicitly references it for historical evidence.

Do not copy current files into archive as backups. Git already preserves exact old payloads.

## 19. Current AI continuation

The current branch-local AI sequence is intentionally explicit:

```text
AI-00
semantic / architectural foundation
        ↓
production AI / agent engineering research
external evidence + applicability boundary
        ↓
AI-02.1
ACTIVE — DANTE Intelligence Reengineering
v0.4 current checkpoint
Round I complete
Round II complete
Final Kill-Test complete
ONE LAST mega stress-test required
future-extensibility acceptance still required
        ↓
AI-03
Context / Retrieval / Memory
BLOCKED until AI-02.1 structural acceptance
```

AI-02.1 does not choose a model/provider first. It tests the intelligence architecture against what DANTE must actually be able to do, including real simulations, multi-actor/privacy/Authority boundaries, durability/effects, proactivity, external-AI integration and the accepted Domain/Logical/Physical/database contracts.

The current v0.4 checkpoint preserves all earlier fixes and adds Reference/Target Resolution, deterministic Policy Composition/Precedence, ConsequenceProfile, Safe Result Publication/Streaming, temporal Basis validity, the explicit external institutional System-of-Record boundary and non-collapsed communication acknowledgement states.

The future-extensibility test remains explicit: a later much richer integrated conversational intelligence, new frontier provider or new specialist intelligence must be addable without transferring canonical truth, durable memory, Authority or effect ownership to the model/provider, without bypassing safe publication and without requiring a fundamental architecture rewrite.

AI-03 owns detailed Context / Retrieval / Memory design only after the one last AI-02.1 mega stress-test and other required pre-AI-03 acceptance work.

## 20. General continuation rule

Before modifying a subsystem:

```text
read current global status
→ read current subsystem entry point/authority
→ verify current branch/ref + relation to main
→ inspect relevant executable truth
→ use branch-local handoff only if the branch is active and one is genuinely needed
→ update durable current docs when behavior/architecture changes
→ remove temporary handoffs before integration
→ reconcile candidate-state wording after merge
```

Current truth should be easy to find without archaeological reconstruction of obsolete overlays.
