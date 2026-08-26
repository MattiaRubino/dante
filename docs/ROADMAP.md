# DANTE Roadmap

- **Status:** CURRENT
- **Last reconciled:** 2026-08-26
- **Protected `main`:** `117360b9333fd1a8a62d0dfeb0398a4d5811e393`

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
        exact Physical phase-time patch 18.4 / historical
          ↓
Engineering Foundation v0
        CLOSED / ACCEPTED
          ↓
Frontend Engineering Foundation
        CLOSED / ACCEPTED / INTEGRATED VIA PR #22
          ↓
Frontend Production Materialization
        CLOSED / PASS / INTEGRATED VIA PR #28
          ↓
Backend CP1–CP5 Scaffold
        CLOSED / DIRECT QA PASS / INTEGRATED VIA PR #24
          ↓
Backend CP6 Concrete PostgreSQL Database
        CLOSED / DIRECT QA PASS / INTEGRATED VIA PR #42
```

Architecture closure remains distinct from product/runtime completion. PostgreSQL patch maintenance inside accepted major line 18 does not reopen the Physical selection or rewrite historical 18.4 execution evidence.

## 2. CP6 is complete

CP6 converted the closed Domain + Logical + Physical model into the concrete DANTE PostgreSQL database.

Final lifecycle:

```text
CP6-00  Authority Reconstruction & Scope Freeze
         COMPLETE

CP6-01  Concrete Persistence Coverage Map
         CLOSED / GATE 01 PASS

CP6-02  PostgreSQL Persistence Constitution
         CLOSED / GATE 02 PASS

CP6-03  Whole DANTE Database Blueprint
         CLOSED / GATE 03 PASS

CP6-04  Whole DANTE Database Materialization
         CLOSED / MATERIALIZATION PASS

CP6-05  Whole Database Direct QA
         CLOSED / DIRECT QA PASS

CP6      CLOSED / CONCRETE POSTGRESQL DATABASE PASS
         INTEGRATED VIA PR #42
```

Current materialized baseline:

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

CP6 is historical implementation/acceptance work now. Do not route new work through old `Gate 03`, `DB-U* open`, `CP6-04 next` or protected-main-alignment steps.

Current database authority:

- `database/README.md`
- `database/dictionary/`
- `development/backend-cp6-02-postgresql-persistence-constitution.md`
- `decisions/ADR-010-postgresql-persistence-constitution.md`
- `development/backend-cp6-05-whole-database-qa.md`

Historical branch record:

- `archive/branches/2026-08-feature-logical-postgresql.md`

## 3. Current active product work — Access frontend

The active product implementation workstream is currently:

```text
feature/access-frontend
```

Current branch-local accepted frontend checkpoints:

```text
AF-01D  shell completion / professional polish     PASS
AF-02A  complete pre-backend frontend state graph  PASS
AF-02B  downstream surface hardening               PASS
```

Access is **not closed**. The frontend has intentionally stopped backend-authoritative transitions instead of fabricating authentication success.

Remaining closure pressure includes, as required by the final backend/product contract:

```text
real backend Auth boundary
account creation / credential authentication
verification + recovery proof handling
provider transaction validation
secure account linking
session lifecycle
reauthentication
server rate-limit/error mapping
stable Auth OpenAPI
generated typed client
frontend/backend integration
full-stack isolated E2E
final authenticated Home handoff
release/legal/mobile gates where applicable
```

`feature/access-frontend` is unmerged and currently diverged from protected `main`. Before its final integration it must be reconciled with current `main`, including the newly integrated CP6 backend/database and this documentation lifecycle baseline, without discarding its accepted Access work.

Temporary Access live handoffs may remain branch-local while the workstream is active. They must not merge into `main`; before integration they are consolidated/removed according to `development/documentation-lifecycle-policy.md`.

## 4. Next backend implementation boundary

The next backend implementation phase is **post-CP6 product behavior**, not more generic database design.

No dedicated post-CP6 backend product branch is currently recorded as started in protected `main`.

When explicitly started, it must branch from current `main` and consume the already-materialized database rather than redesigning persistence from scratch.

The active Access frontend creates a concrete demand for a real authentication/account/session backend boundary. That makes Access/Auth a likely consuming boundary, but roadmap text does not itself authorize or invent a backend branch. The exact backend workstream begins only when explicitly created/scoped.

Expected post-CP6 vertical responsibilities include as applicable:

```text
application use cases
capability-specific persistence adapters
commands / queries
backend governance/orchestration
API contracts
AuthN/AuthZ behavior where the vertical owns it
frontend/mobile consumption
full-stack semantic scenarios
vertical-specific HG / PSV evidence
```

A vertical may reveal a genuine database evolution need. That becomes a reviewed forward Alembic migration plus synchronized SQLAlchemy/Dictionary/reference/tests; it does not reopen CP6.

## 5. Database evolution after CP6

Permanent same-change rule:

```text
real structural database change
→ Alembic forward migration
→ SQLAlchemy mapping/metadata update
→ Database Dictionary update
→ human-readable reference update when meaning/topology changes
→ generated artifacts/diagrams where governed
→ direct tests
```

Applied revisions are immutable. No structural change is complete while current documentation or Dictionary describes the old schema.

## 6. Capability-triggered implementation

Selected specialist components activate only at real product/operational triggers:

```text
PowerSync + encrypted SQLite
→ real offline/multi-device implementation

PostgreSQL transactional outbox
→ real Class-A async requirement

R2
→ real ContentArtifact byte flow

OR-Tools
→ solver-backed capability

Restate
→ first real Class-B durable workflow

PgBouncer
→ concrete connection-management need + direct validation

pgBackRest + AWS S3
→ recovery/production boundary or real recovery rehearsal
```

A selected component is not implemented merely because it appears in architecture.

## 7. Frontend direction after foundation/materialization

The generic frontend engineering foundation and production materialization are closed/integrated. Future frontend work is vertical/product work on bounded branches rather than another generic foundation phase.

Persistent rules remain:

```text
backend + PostgreSQL own canonical accepted effect
Web baseline online-first
Mobile local/offline state remains noncanonical
identity-scoped local data
feature-first app boundaries
route/navigation adapters remain thin
shared packages require real multi-consumer value
production never imports prototypes
current design tokens / i18n / time contracts remain governed
```

Access is the current active frontend vertical.

## 8. Infrastructure / release boundaries still deferred

Do not prematurely materialize infrastructure merely to complete a diagram.

Still trigger-bound/not currently complete:

```text
production backend compute provider / sizing
IaC engine and production infrastructure rollout
production registry/release pipeline where not yet required
recovery/PITR rehearsal
real V1→V2 business-schema evolution rehearsal
PowerSync product activation
Restate product activation
production deployment
```

When these become real workstreams, current evidence must replace design-time assumptions.

## 9. Documentation lifecycle baseline

The documentation knowledge/lifecycle cleanup has established the durable repository policy and current routing baseline:

```text
current specifications state current truth directly
temporary live/session handoffs do not enter protected main
completed branch history is retained only when materially useful
historical evidence is explicitly non-authoritative
frozen split documents are compacted only when lossless knowledge coverage is proven
Git remains the complete recoverable chronology
```

Current authority:

- `development/documentation-lifecycle-policy.md`
- `development/documentation-and-handoff.md`
- `development/branching-and-environments.md`
- `development/operating-rules.md`
- `docs/README.md` for navigation/authority order

The cleanup intentionally retained large Domain/Logical/Database split references where unique rationale, tests, assumptions or detailed reference content make destructive compaction unsafe. Fewer files is not a success criterion by itself.

Future documentation maintenance follows the same knowledge-coverage gate rather than reopening a permanent cleanup phase.

## 10. Persistent engineering rules

```text
SELECTED ARCHITECTURE != IMPLEMENTED COMPONENT
DOCUMENTATION PASS != DIRECT IMPLEMENTATION PASS
HISTORICAL 18.4 EVIDENCE != CURRENT 18.6 RUNTIME CLAIM
POSTGRESQL PATCH REFRESH != PHYSICAL ARCHITECTURE REOPEN
CLIENT LOCAL STATE != CANONICAL EFFECT AUTHORITY
ENVIRONMENT != GIT BRANCH
UNMERGED BRANCH TRUTH != PROTECTED-main TRUTH
DATABASE MATERIALIZATION != PRODUCT APPLICATION IMPLEMENTATION
DETERMINABLE SCHEMA EVOLUTION != SPECULATIVE PRE-MATERIALIZATION
TEMPORARY HANDOFF != DURABLE main DOCUMENTATION
```

## 11. Immediate sequence

Current practical sequence is:

```text
1. preserve and continue active Access work on feature/access-frontend
2. start the next bounded backend product vertical only under explicit scope
3. reconcile Access with current main before protected-main integration
4. integrate real backend/frontend contracts only after direct full-stack evidence
5. activate specialist/runtime capabilities only at their real trigger
6. apply the documentation lifecycle policy continuously instead of accumulating cleanup debt
```

This roadmap intentionally does not pre-create future branches, migrations, APIs or infrastructure that do not yet have an authorized concrete subject.
