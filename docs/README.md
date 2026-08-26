# DANTE Documentation Index

- **Status:** CURRENT NAVIGATION / AUTHORITY INDEX
- **Last reconciled:** 2026-08-26

This directory is the durable documentation surface for DANTE. Current specifications must describe the present directly; historical evidence, completed workstream records and Git history must not silently override current truth.

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
LOGICAL MODEL                        CLOSED / 57 OF 57
PRE-PHYSICAL COHERENCE               CLOSED / FINAL QA PASS
PHYSICAL TARGET                      CLOSED / ACCEPTED
ENGINEERING FOUNDATION               CLOSED / ACCEPTED
FRONTEND ENGINEERING FOUNDATION      CLOSED / INTEGRATED VIA PR #22
FRONTEND MATERIALIZATION             CLOSED / PASS / INTEGRATED VIA PR #28
BACKEND CP1–CP5 SCAFFOLD             CLOSED / DIRECT QA / INTEGRATED VIA PR #24
BACKEND CP6 DATABASE                 CLOSED / DIRECT QA / INTEGRATED VIA PR #42
CURRENT POSTGRESQL                   18.6
CURRENT ALEMBIC HEAD                 20260826_08
CURRENT DATABASE TOPOLOGY            68/5/14/75/95/68/120
ACCESS FRONTEND                      ACTIVE / UNMERGED ON feature/access-frontend
FIRST POST-CP6 BACKEND VERTICAL      NOT STARTED ON A DEDICATED BRANCH
```

For exact current state, read `PROJECT-STATUS.md` rather than reconstructing status from historical workstream files.

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

Use:

- `development/documentation-lifecycle-policy.md` — normative lifecycle/compaction rules
- `archive/README.md` — archive authority boundary

`docs/archive/` is selective non-authoritative history, not a backup mirror. Git remains the complete recoverable history.

Frozen/read-only split documents may be recomposed into fewer files only through **lossless knowledge coverage**. Do not summarize away requirements, invariants, accepted decisions, continuing rationale or important evidence merely to reduce file count.

## 5. Product

Entry point:

- `product/README.md`

Key durable current/product-definition sources include:

- `product/product-identity-and-north-star.md`
- `product/scope.md`
- the accepted `product/v1-*.md` specifications where still current

Research/simulation material is evidence, not automatic current product truth. The documentation cleanup may later reorganize dated research/simulation files into clearer evidence locations without changing accepted product semantics.

## 6. Domain Model

Entry point:

- `domain/README.md` and its currently retained canonical continuations

The Domain Model is **CLOSED / semantically complete for current scope**.

Canonical terminology and accepted concepts/checkpoints remain under `domain/`.

Important rule during this cleanup: the current Domain README family contains historical chronological continuations as well as substantive current material. It must not be compacted by summary. Any future reorganization requires statement-level knowledge coverage across concepts, checkpoints, language governance, deferred-dependency closure and final Whole-Domain evidence.

Do not infer a semantic kernel primitive merely from UI or persistence naming.

## 7. Logical Model

Entry point:

- `logical-model/`

The Logical Model is **CLOSED / 57 of 57 classified**.

The Whole-Logical content snapshot and later remote-QA closure/evidence must be interpreted according to their explicit lifecycle labels. Historical phase-time headers are not rewritten merely to look current, but they also must not override later closure records.

Binding hardenings remain `WL-H01..WL-H12` unless deliberately superseded by later accepted authority.

## 8. Physical Model

Entry point:

- `physical-model/README.md`

Current selected target:

```text
PostgreSQL 18 major family
sole canonical persistence + material-history authority
```

PostgreSQL 18.4 remains historical exact Physical/CP2/CP3 execution evidence where those phases ran on 18.4. Current repository/database patch is 18.6. Patch maintenance inside major line 18 does not reopen the architecture.

Specialist capability activation remains trigger-based and direct-validation-specific.

## 9. Architecture and decisions

Entry points:

- `architecture/README.md`
- `architecture/system-overview.md`
- `architecture/technical-decisions.md`
- `decisions/`

Important persistence ADRs:

- `decisions/ADR-003-primary-database.md` — historical PostgreSQL-selection rationale where explicitly historical
- `decisions/ADR-007-domain-model-informed-persistence-boundaries.md` — semantic persistence guardrails
- `decisions/ADR-010-postgresql-persistence-constitution.md` — current cross-cutting PostgreSQL persistence doctrine

Important frontend ADRs:

- `decisions/ADR-008-frontend-engineering-stack.md`
- `decisions/ADR-009-frontend-architecture-boundaries.md`

Current architecture documents must state current architecture directly; phase reviews/QA records are evidence and should be classified accordingly during cleanup.

## 10. Database System of Record

Start here:

- `database/README.md`
- `database/dictionary/README.md`
- `database/dictionary/scope.json`

Current baseline:

```text
PostgreSQL          18.6
Alembic             20260826_08
68 tables
5 views
14 routines
75 triggers
95 physical indexes
68 foreign keys
120 CHECK constraints
```

The machine-readable Dictionary is **materialized** with:

```text
68 table entries
5 view entries
14 routine entries
87 standalone entries
```

Permanent consistency invariant:

```text
Database Architecture & Reference
≈ Database Dictionary
≈ SQLAlchemy metadata / mappings
≈ Alembic head
≈ real PostgreSQL schema
```

The human-readable Database Architecture & Reference is currently one logical frozen payload physically stored as:

```text
database/dante-postgresql-database.md
+ database/dante-postgresql-database-part-2.md
...
+ database/dante-postgresql-database-part-19.md
```

It may later be reorganized into fewer/topic-based read-only reference files, but only through lossless content-equivalence/knowledge-coverage QA.

CP6 final acceptance:

- `development/backend-cp6-05-whole-database-qa.md`

Historical CP6 branch record:

- `archive/branches/2026-08-feature-logical-postgresql.md` — NON-AUTHORITATIVE

## 11. Backend

Application documentation:

- `../apps/backend/README.md`

Durable backend contracts:

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

CP1–CP6 are closed. Old text that says CP6-03 is active, Gate 03 is not earned, CP6-04 is next, or protected-main alignment is pending is historical and not current routing.

The next backend implementation is a new post-CP6 product vertical started from current `main` under an explicit bounded branch. No generic permanent `feature/backend` branch is implied.

## 12. Frontend

Current protected-main frontend documentation:

- `frontend/README.md`
- `frontend/design-tokens.md`
- `frontend/localization.md`
- `frontend/terminology.md`
- `frontend/ui-registry.md`
- `frontend/home/`
- `frontend/production-readiness/`

Engineering-foundation sources:

- `architecture/frontend-engineering-foundation.md`
- `architecture/frontend-engineering-foundation-part-2.md`
- `architecture/frontend-engineering-foundation-final-review.md`
- `architecture/frontend-engineering-foundation-post-closure-qa.md`

Generic frontend foundation/materialization is closed/integrated.

### Active Access work

The currently active product frontend branch is:

```text
feature/access-frontend
```

Its branch-local record is:

```text
docs/workstreams/access-frontend.md
```

Current branch-local accepted checkpoints include AF-01D, AF-02A and AF-02B PASS, but the Access vertical is not closed until the real backend-auth/full-stack/release boundaries are satisfied.

`feature/access-frontend` is unmerged and currently diverged from protected `main`; its branch-local docs/code do not become protected-main authority until reconciliation and merge.

Any temporary `access-frontend-live-handoff.md` is branch-operational only and must be consolidated/removed before that branch merges.

## 13. Workstream records

Entry point:

- `workstreams/README.md`

On protected `main`, workstream files are durable **records**, not active chat handoffs. Completed workstreams may preserve one useful closure/integration record or other durable evidence; temporary live/session handoffs belong only on active branches and are removed before merge.

Closed records include Domain, Logical, Pre-Physical, Physical, Engineering Foundation, Frontend Foundation/Materialization and Backend scaffold/CP6 history as applicable.

Active unmerged branch workstream records remain branch-local until integration.

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

Effective repository ruleset `lifeos-main-safety` currently requires:

```text
PR integration
normal merge commit only
branch up-to-date with main
review threads resolved
no non-fast-forward update
no branch-rule bypass

required checks:
Backend CI Gate
Dependency Review
Frontend CI Gate
```

The live ruleset, not an outdated prose snapshot, is effective repository enforcement.

Do not use squash/rebase/force-push to bypass integration policy.

## 16. CI / executable truth

Backend workflows and tests remain executable evidence, not documentation claims.

Current protected-main required status contexts are:

```text
Backend CI Gate
Dependency Review
Frontend CI Gate
```

No arbitrary coverage threshold is inferred merely because coverage is measured.

Historical successful runs remain evidence for the exact commit/environment on which they executed; later patch/runtime claims require current evidence.

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
→ read current subsystem authority
→ verify current branch/ref + relation to main
→ inspect relevant executable truth
→ use branch-local handoff only if the branch is active and one is genuinely needed
→ update durable current docs when behavior/architecture changes
→ remove temporary handoffs before integration
```

Current truth should be easy to find without archaeological reconstruction of obsolete overlays.
