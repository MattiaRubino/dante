# DANTE Roadmap

- **Status:** CURRENT
- **Last reconciled:** 2026-08-31
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
          ↓
Access Pre-Backend Web Materialization
        CLOSED / ACCEPTED / RELEASE-HARDENED
        AF-01D / AF-02A / AF-02B / AF-03A PASS
```

Architecture closure remains distinct from product/runtime completion. Closing the pre-backend Access frontend does not close the real full-stack Access/Auth product vertical.

## 2. CP6 is complete

CP6 converted the closed Domain + Logical + Physical model into the concrete DANTE PostgreSQL database.

```text
CP6-00  COMPLETE
CP6-01  CLOSED / GATE 01 PASS
CP6-02  CLOSED / GATE 02 PASS
CP6-03  CLOSED / GATE 03 PASS
CP6-04  CLOSED / MATERIALIZATION PASS
CP6-05  CLOSED / DIRECT QA PASS
CP6      CLOSED / CONCRETE POSTGRESQL DATABASE PASS
         INTEGRATED VIA PR #42
```

Pre-recovery protected-main CP6 baseline:

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

Post-CP6 recovery evolution in this tree:

```text
Alembic             20260830_09
69 tables
5 views
15 routines
76 triggers
97 physical indexes
69 foreign keys
123 CHECK constraints
CP01–CP07           LOCAL PASS / CLOSED
```

The newer database/recovery contract remains branch-local until integrated; live Git refs determine protected-main state.

CP6 is historical implementation/acceptance work now. Do not route new work through old Gate 03, DB-U*, CP6-04 or protected-main-alignment steps.

Current database authority:

- `database/README.md`
- `database/dictionary/`
- `development/backend-cp6-02-postgresql-persistence-constitution.md`
- `decisions/ADR-010-postgresql-persistence-constitution.md`
- `development/backend-cp6-05-whole-database-qa.md`

Historical branch record:

- `archive/branches/2026-08-feature-logical-postgresql.md`

## 3. Access frontend materialization is closed

The pre-backend Access Web workstream completed:

```text
AF-01D  shell completion / professional polish      PASS
AF-02A  complete pre-backend frontend state graph   PASS
AF-02B  downstream surface hardening                PASS
AF-03A  release-hardening viewport matrix           PASS
```

It intentionally stops backend-authoritative transitions instead of fabricating authentication success. Current frontend truth is `frontend/access.md` plus current code/tests. The closed branch history is `archive/branches/2026-08-feature-access-frontend.md`.

Closing this workstream does not mean real Access/Auth is complete.

## 4. Active bounded unmerged workstreams

The project is no longer waiting to start its first post-CP6 vertical. At the 2026-08-31 reconciliation, bounded unmerged work includes:

```text
feature/access-auth             active full-stack product work
feature/home-react              active frontend work
feature/platform-observability  active platform work
feature/postgres-recovery       CP01–CP07 LOCAL PASS / CLOSED / integration candidate
```

These branches are intentionally independent and own only their bounded truth until integration. Do not collapse them into a single mega-branch and do not rewrite protected-main truth from an unmerged branch.

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

Applied revisions are immutable. A product vertical may reveal a legitimate schema evolution need; that becomes a normal reviewed forward change and does not reopen CP6.

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

pgBackRest LOCAL recovery
→ implemented and directly rehearsed

remote backup provider
→ TBD; trigger only at a real production deployment boundary
```

A selected component is not implemented merely because it appears in architecture.

## 7. Persistent frontend direction

The generic frontend engineering foundation, production materialization and pre-backend Access Web materialization are closed. Future frontend work is vertical/product work rather than another generic foundation phase.

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

## 8. Infrastructure / release boundaries still deferred

Do not prematurely materialize infrastructure merely to complete a diagram.

Still trigger-bound/not currently complete:

```text
production backend compute provider / sizing
IaC engine and production infrastructure rollout
production registry/release pipeline where not yet required
remote-provider production recovery/retention acceptance
real V1→V2 business-schema evolution rehearsal
PowerSync product activation
Restate product activation
production deployment
```

When these become real workstreams, current evidence must replace design-time assumptions.

## 9. Documentation lifecycle baseline

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
- `docs/README.md`

Fewer files is not a success criterion by itself. Remove/compact only after knowledge coverage.

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

```text
1. finish and integrate each active bounded workstream only after its own acceptance gate
2. treat feature/postgres-recovery as a closed LOCAL recovery integration candidate
3. continue feature/access-auth, feature/home-react and feature/platform-observability independently
4. evolve the database only through same-change forward migrations when a real vertical requires it
5. keep remote backup/cloud recovery deferred until production deployment creates a real need
6. apply documentation lifecycle cleanup before each branch integration
7. use live Git refs and branch-local authority rather than stale global assumptions
```

This roadmap intentionally does not pre-create future branches, migrations, APIs or infrastructure before their concrete scope is authorized.
