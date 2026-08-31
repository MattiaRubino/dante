# DANTE Documentation Index

- **Status:** CURRENT NAVIGATION / AUTHORITY INDEX
- **Last reconciled:** 2026-08-31

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
PRE-RECOVERY MAIN ALEMBIC BASELINE   20260826_08
PRE-RECOVERY MAIN DB TOPOLOGY        68/5/14/75/95/68/120
RECOVERY EVOLUTION IN THIS TREE      20260830_09 / 69/5/15/76/97/69/123
POSTGRESQL LOCAL RECOVERY            CP01–CP07 LOCAL PASS / CLOSED
REMOTE BACKUP PROVIDER               TBD / NOT ACTIVATED
ACCESS PRE-BACKEND FRONTEND          CLOSED / ACCEPTED / RELEASE-HARDENED
FULL ACCESS/AUTH PRODUCT VERTICAL    ACTIVE UNMERGED WORKSTREAM / NOT CLAIMED CLOSED
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

Specialist capability activation remains trigger-based and direct-validation-specific.

## 9. Architecture and decisions

Entry points:

- `architecture/README.md`
- `architecture/system-overview.md`
- `architecture/technical-decisions.md`
- `architecture/domain-model-logical-readiness.md`
- `decisions/`

Current architecture docs state current post-CP6 architecture directly. Phase reviews/QA/readiness continuations are evidence according to their explicit lifecycle role.

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

Current database contract in this tree:

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

The pre-recovery protected-main CP6 baseline was `20260826_08 / 68|5|14|75|95|68|120`. Integration status is determined by live Git refs.

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

Historical CP6 branch record:

- `archive/branches/2026-08-feature-logical-postgresql.md` — NON-AUTHORITATIVE

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

Post-CP6 backend work is already active on bounded unmerged workstreams where authorized; `feature/access-auth` is one such current branch. Branch-local authority owns its exact state until integration.

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

The completed pre-backend Access frontend materialization is the accepted Web baseline for the next full-stack Access/Auth product vertical.

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

Closed records include Domain, Logical, Pre-Physical, Physical, Engineering Foundation, Frontend Foundation/Materialization and backend scaffold/CP6 history as applicable.

Active unmerged workstream records remain branch-local until integration.

At the 2026-08-31 reconciliation, bounded unmerged work includes `feature/access-auth`, `feature/home-react`, `feature/platform-observability`, while `feature/postgres-recovery` has completed CP01–CP07 locally and is an integration candidate. Live Git refs are authoritative for later changes.

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

## 19. Current continuation rule

Before modifying a subsystem:

```text
read current global status
→ read current subsystem entry point/authority
→ verify current branch/ref + relation to main
→ inspect relevant executable truth
→ use branch-local handoff only if the branch is active and one is genuinely needed
→ update durable current docs when behavior/architecture changes
→ remove temporary handoffs before integration
```

Current truth should be easy to find without archaeological reconstruction of obsolete overlays.
