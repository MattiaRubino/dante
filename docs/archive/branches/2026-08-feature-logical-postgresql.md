# Branch history — feature/logical-postgresql

> Historical branch record. **NON-AUTHORITATIVE for current project state.**
> Current truth lives in the repository's current status, architecture, database System of Record, code, migrations and tests.

## Identity

- Repository: `MattiaRubino/dante`
- Branch: `feature/logical-postgresql`
- Workstream: Backend CP6 — Concrete PostgreSQL Database
- Final feature HEAD before merge: `9297b64c7c912c2cc8e344a6617beb5c91457bbb`
- Accepted implementation candidate: `22bbc078391d52c43665474bf465593d6225106e`
- Closure-documentation anchor before protected-main alignment: `8c33c897ff57cfff9130fe00db1854470aa06bb5`
- Protected-main alignment merge commit: `2c8a047eb9056257fc6e2ed92b00ffd981bf16f1`
- Integration PR: #42 — `feat: integrate closed CP6 PostgreSQL database`
- Protected-main merge commit: `117360b9333fd1a8a62d0dfeb0398a4d5811e393`
- Merged: 2026-08-26

## Purpose

The branch converted the already accepted Domain, Logical and Physical persistence model into the concrete DANTE PostgreSQL database, including executable schema history, SQLAlchemy mapping, database dictionary, security posture, direct PostgreSQL proof and persistent LOCAL verification.

The workstream deliberately separated architecture/design gates from materialization and final direct QA. Temporary live/session handoffs were used only for cross-chat continuity while the branch was active; they are not retained as current documentation after branch closure.

## Milestone sequence

```text
CP6-00  COMPLETE
CP6-01  CLOSED / GATE 01 PASS
CP6-02  CLOSED / GATE 02 PASS
CP6-03  CLOSED / GATE 03 PASS
CP6-04  CLOSED / MATERIALIZATION PASS
CP6-05  CLOSED / DIRECT QA PASS
CP6     CLOSED / CONCRETE POSTGRESQL DATABASE PASS
```

### CP6-01 — concrete persistence coverage

Established coverage from accepted semantic owners to concrete persistence obligations and closed the first gate before detailed PostgreSQL design.

Retained evidence:

- `docs/development/backend-cp6-01-concrete-persistence-coverage.md`
- `docs/development/backend-cp6-01-concrete-persistence-coverage-part-2.md`
- `docs/development/backend-cp6-01-concrete-persistence-coverage-closure.md`

### CP6-02 — PostgreSQL persistence constitution

Froze the cross-cutting persistence doctrine used by later database design and implementation, including identity/addressing, current/history semantics, constraints, transaction/concurrency posture, migration/evolution rules and owner/migrator/runtime privilege separation.

Retained authority/evidence:

- `docs/development/backend-cp6-02-postgresql-persistence-constitution.md`
- `docs/development/backend-cp6-02-postgresql-persistence-constitution-closure.md`
- `docs/decisions/ADR-010-postgresql-persistence-constitution.md`

### CP6-03 — whole-database blueprint and Gate 03

Derived and audited the full concrete PostgreSQL object model before materialization. The phase froze the actual object inventory, naming, indexes, privilege matrix, migration/materialization DAG, SQLAlchemy mapping plan, Database Dictionary readiness and direct-proof obligations.

Important audit/rework history preserved by retained evidence includes:

- final actual PostgreSQL object inventory freeze;
- exact object naming closure;
- structural/query index reconciliation;
- exact object-level runtime privilege matrix;
- migration/materialization DAG freeze;
- SQLAlchemy mapping-plan freeze;
- Database Dictionary readiness;
- implementation-determinism/direct-proof hardening;
- repeated tombstone audits rather than treating the first pass as final;
- repair of recurrence selector/phase/range determinism;
- repair of generated-coordinate duplicate defense;
- repair of NULL-unsafe CHECK expressions;
- repair of governing-Recurrence membership validation;
- repair of current/history lifecycle enforcement before Gate 03 closure.

Retained evidence:

- `docs/development/backend-cp6-03-gate-03-closure.md`
- `docs/development/backend-cp6-03-gate-03-ratification-2026-08-25.md`
- `docs/database/dante-postgresql-database*.md` until/documentation cleanup replaces that physical layout losslessly
- `docs/database/dictionary/`

### CP6-04 — materialization

Materialized the accepted blueprint through repository-owned PostgreSQL provisioning/security work plus a reviewed linear Alembic sequence and SQLAlchemy mappings. The final CP6 migration head became `20260826_08` after CP6-05 hardening.

Retained implementation/evidence documents include:

- `docs/development/backend-cp6-04-p0-provisioning-security.md`
- `docs/development/backend-cp6-04-m1-native-identity-address.md`
- `docs/development/backend-cp6-04-m2-scoped-material-control.md`
- `docs/development/backend-cp6-04-m3-schedule-actual-session.md`
- `docs/development/backend-cp6-04-m4-recurrence.md`
- `docs/development/backend-cp6-04-m5-core-integrity-current-views.md`
- `docs/development/backend-cp6-04-m6-occurrence-generation.md`
- `docs/development/backend-cp6-04-m7-runtime-acl-activation.md`

These files are evidence of reviewed materialization stages, not active branch handoffs.

### CP6-05 — whole-database direct QA and closure

Performed final cross-representation reconciliation and real-PostgreSQL proof. One remaining concurrency-defense defect in occurrence-generation validation was repaired by forward-only revision `20260826_08`; final QA also closed mapping/documentation/proof-trace gaps without changing the frozen object counts.

Retained final closure authority/evidence:

- `docs/development/backend-cp6-05-whole-database-qa.md`

## Final accepted database state

```text
PostgreSQL patch     18.6
Alembic head         20260826_08

tables               68
views                 5
routines             14
triggers              75
physical indexes     95
foreign keys          68
CHECK constraints    120

custom enum/domain     0
sequences              0
materialized views     0
RLS policies           0
```

Security posture verified at closure included the expected three DANTE roles, owner-to-migrator membership, null owner password and denial of runtime access to the Alembic version table.

## Final direct acceptance

The final accepted candidate passed:

```text
uv / locked environment               PASS
Ruff format check                     PASS
Ruff lint                             PASS
mypy strict                           PASS
non-PostgreSQL pytest                 37 / 37 PASS
build                                 PASS
real PostgreSQL selected tests        76 / 76 PASS
Dictionary JSON-Schema validation     PASS
Alembic current/check                 PASS
persistent LOCAL upgrade              20260826_07 -> 20260826_08
persistent restart without -v         PASS
final topology/security               PASS
GET /health/live                      200
GET /health/ready                     200
```

## Protected-main integration

Before final integration, protected `main` was merged normally into the feature branch to reconcile already-integrated frontend work. The alignment used no rebase and no force push and preserved main-only frontend artifacts while keeping the closed CP6 backend/database tree intact.

PR #42 then integrated the branch through the repository-required merge-commit path after the required checks were green on the correct PR head. The resulting protected-main merge commit is:

```text
117360b9333fd1a8a62d0dfeb0398a4d5811e393
```

The PR records the exact final branch state, acceptance evidence and integration policy.

## Temporary handoff disposition

The following files existed only to resume an active chat/session and are intentionally removed by the documentation cleanup after branch closure:

- `docs/development/backend-cp6-03-live-handoff.md`
- `docs/development/backend-cp6-03-live-handoff-2026-08-25.md`
- `docs/development/backend-cp6-03-session-handoff-2026-08-22.md`
- `docs/development/backend-cp6-03-session-handoff-2026-08-23.md`
- `docs/development/backend-cp6-04-live-handoff-2026-08-25.md`
- `docs/development/backend-cp6-04-live-handoff-2026-08-26.md`
- `docs/development/backend-cp6-05-live-handoff-2026-08-26.md`

Their detailed payload remains recoverable through Git history. Durable semantics, important design rationale, material defects/repairs, final topology, QA and integration evidence remain represented by the retained authority/evidence files above and this branch-level historical index.

## Knowledge-coverage disposition

```text
current truth                 -> current status/database/code/tests
accepted persistence doctrine -> CP6-02 + ADR-010
Gate 03 design evidence       -> CP6-03 closure/ratification + database reference
materialization evidence      -> CP6-04 P0/M1..M7 records + migrations/code/tests
final acceptance evidence     -> CP6-05 whole-database QA
branch integration evidence   -> PR #42 + merge commit
cross-chat resume mechanics   -> Git history only
superseded next-step prose    -> discarded from current tree
```

No live/session handoff is an authority after branch closure.
