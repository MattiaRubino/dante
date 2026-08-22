# DANTE — Project Status

- Status: **CURRENT TRUTH**
- Product: **DANTE**
- Protected-main truth anchor: `fd3bc8dd918cf6aadeff4572221af68612c3cb42`
- Backend integration PR `#24`: **MERGED**
- Backend CP6 branch: `feature/logical-postgresql`
- Frontend materialization branch: `feature/frontend-materialization`

## 1. Executive state

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL
CLOSED / SEMANTICALLY COMPLETE FOR CURRENT SCOPE

LOGICAL MODEL
CLOSED
57 / 57 CLASSIFIED
WL-H01..WL-H12 ACTIVE

PRE-PHYSICAL COHERENCE
CLOSED / FINAL QA PASS

PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED
PostgreSQL 18 major family
sole canonical persistence / material-history authority
Physical phase-time exact patch 18.4

ENGINEERING FOUNDATION v0
CLOSED / ACCEPTED

FRONTEND ENGINEERING FOUNDATION
CLOSED / ACCEPTED / INTEGRATED VIA PR #22

FRONTEND MATERIALIZATION
ACTIVE ON feature/frontend-materialization
DIRECT PASS ONLY AS EARNED BY THAT WORKSTREAM

PRODUCTION BACKEND SCAFFOLD
INTEGRATED IN PROTECTED main / DIRECT QA PASS
CP1 CLOSED / DIRECT QA PASS
CP2 CLOSED / DIRECT QA PASS — PostgreSQL 18.4 historical exact evidence
CP3 CLOSED / DIRECT QA PASS — PostgreSQL 18.4 historical exact evidence
CP4 CLOSED / DIRECT REMOTE QA PASS
CP5 CLOSED / DIRECT INTEGRATED QA PASS
PR #24 MERGED / POST-MERGE BACKEND CI PASS

CP6 — CONCRETE POSTGRESQL DATABASE
ACTIVE ON feature/logical-postgresql
CP6-00 COMPLETE
CP6-01 CLOSED / GATE 01 PASS
CP6-02 CLOSED / GATE 02 PASS
CP6-03 NEXT / NOT STARTED — WHOLE DANTE DATABASE BLUEPRINT

CURRENT POSTGRESQL TECHNICAL PATCH
18.6
CONFIGURATION REFRESH APPLIED
DIRECT REMOTE FOUNDATION REGRESSION PASS
RUN 32568664940
HEAD ec3dc795b5e044daa3a77723c94a1b4b5b92865c

CURRENT DANTE BUSINESS DATABASE
NOT YET MATERIALIZED

FIRST PRODUCT VERTICAL
POST-CP6 / NOT STARTED
```

Architecture/design closure never implies direct implementation PASS. PostgreSQL 18.4 remains the exact historical Physical/CP2/CP3 patch; current CP6 technical patch is 18.6. Neither technical result retroactively discharges business-semantic HG/PSV obligations.

## 2. CP6 execution boundary — authoritative

CP6 is not a generic persistence-foundation exercise and it is not the first application vertical.

It turns the closed Domain + Logical + Physical model into the concrete PostgreSQL database of DANTE.

Current remaining sequence:

```text
CP6-03
WHOLE DANTE DATABASE BLUEPRINT
concrete tables/families/columns/types/relations/history/constraints/indexes
+ implementation/migration dependency DAG
+ SQLAlchemy mapping plan
+ direct-test plan
        ↓
CP6-04
WHOLE DANTE DATABASE MATERIALIZATION
real Alembic business-schema migrations
real DANTE tables / constraints / indexes
real SQLAlchemy mappings
real privilege/grant posture
real PostgreSQL database tests
        ↓
CP6-05
WHOLE DATABASE DIRECT QA + CLEAN-ROOM REVIEW
        ↓
CP6 CLOSED
DANTE DATABASE BLUEPRINT COMPLETE
MATERIALIZED TO MAXIMUM NON-SPECULATIVE EXTENT
MIGRATED / MAPPED / DIRECTLY TESTED
        ↓
SEPARATE FIRST PRODUCT VERTICAL PHASE
```

Earlier CP6 planning language that prohibited all business schema/migrations/mappings anywhere inside CP6 is superseded by the current workstream execution boundary.

That old prohibition remains true only for the bounded CP6-01 and CP6-02 checkpoints themselves: those stages correctly closed coverage and global PostgreSQL doctrine before business-schema materialization began.

### CP6 may implement

After exact stage/write gates, CP6 may implement everything already determinable from the closed model, including where applicable:

```text
DANTE business tables
owner-specific canonical tables
specific relation tables
bounded NativeRef / ScopedRecordRef / MaterialStateRef control structures
owner-specific material-state/history tables
explicit current-state bindings
provider/integration and derived DB structures already required by the closed model
PostgreSQL native types
PK / FK / UNIQUE / CHECK / EXCLUDE / range constraints
structural indexes
Alembic business-schema revisions
SQLAlchemy database mappings
object ownership / grants / runtime privilege posture
real PostgreSQL acceptance tests
```

### CP6 still does not implement

```text
first-product-vertical application use cases
first-product-vertical application services
product persistence adapters that encode application behavior
business API routes
frontend behavior
product workflow orchestration
AuthN/AuthZ product behavior
specialist runtime activation merely because selected
production deployment
```

The first product vertical therefore starts **after CP6**, over a database already derived/materialized from the earlier Domain/Logical/Physical work.

## 3. Current persistence authority

### CP6-01

```text
docs/development/backend-cp6-01-concrete-persistence-coverage.md
docs/development/backend-cp6-01-concrete-persistence-coverage-part-2.md
docs/development/backend-cp6-01-concrete-persistence-coverage-closure.md
```

Gate 01 result:

```text
57 / 57 concepts accounted                       PASS
15 / 15 LR-01 native owners                      PASS
LR-01..LR-13                                     PASS
WL-H01..WL-H12                                   PASS
PG-R01..PG-R10                                   PASS
HG / SC / PSV carry-forward                      COMPLETE / TRUTHFUL
semantic owner reclassification                  0
generic semantic fallback                        0
business DDL at Gate 01                          0
```

`business DDL = 0` is historical Gate-01 scope truth, not a whole-CP6 prohibition.

### CP6-02

```text
docs/development/backend-cp6-02-postgresql-persistence-constitution.md
docs/development/backend-cp6-02-postgresql-persistence-constitution-closure.md
```

```text
CP6-02
CLOSED / GATE 02 PASS
```

Closed rule families:

```text
TECH ID REF MAT HIST TIM MISS LIFE TYP REL CON IDX
TX IDEM PROV CAP MIG SEC QA
```

Gate 02 closed global PostgreSQL doctrine and correctly created no business schema itself. Its technical rules remain closed; only superseded process/staging language about later CP6 business-database materialization is no longer current execution authority.

Current CP6 execution authority:

`docs/workstreams/logical-postgresql.md`

## 4. Logical / Physical invariants that remain binding

```text
Person != Account != Principal != Actor
Person != Living Referent != Asset
Subject != Resource != native identity
Possibility != Goal != Proposal != Decision != Plan != Activity
Routine != Recurrence != Occurrence
Occurrence != Schedule != Session != Actual
Actual != Observation != Outcome
Evidence != Provenance
Version != Reconciliation
Authority != Visibility
Agreement != Consent
Ownership != Possession
provider state != canonical DANTE state
derived projection != canonical truth
absence/unknown != false
MaterialStateRef != ETag/MVCC/provider revision
idempotency != semantic identity
client local state != canonical accepted effect
```

Accepted PostgreSQL mapping thesis:

```text
owner-specific canonical families
+ owner-specific material-state/history families
+ specific typed relation families
+ bounded technical address/control structures only where genuinely heterogeneous addressing requires them
+ separate provider/derived/runtime concerns
```

Forbidden shortcuts remain:

```text
universal Entity / Thing
universal Relationship / generic edge
canonical EAV/property bag
universal event ontology
universal Fact/Version semantic payload root
JSONB required-semantic escape hatch
```

## 5. Reference / material-state baseline

Reference families remain distinct:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

Closed physical direction:

```text
homogeneous NativeRef
→ direct FK

genuinely heterogeneous NativeRef
→ bounded native-address anchor

MaterialStateRef
→ UUIDv7 stable address
→ bounded material-state address/control
→ exact owner + facet
→ owner-specific material-state row
→ explicit current accepted-state binding where required
```

No application-only `type + uuid` polymorphic integrity.

## 6. Backend technical foundation

Frozen CP3 posture:

```text
schema                              dante
SQLAlchemy                          async 2.0 stable line
psycopg                             3
Alembic                             one environment / one DAG / one head
one AsyncEngine per process
one async_sessionmaker per process
one AsyncSession per app operation
autobegin=False
autoflush=True
expire_on_commit=False
outer application operation owns transaction
adapter may flush / never implicit commit
READ COMMITTED default

dante_owner                         NOLOGIN
dante_migrator                      LOGIN NOINHERIT + bounded SET ROLE
dante_runtime                       LOGIN NOINHERIT / runtime DML posture
```

No generic Repository/UoW/BaseService architecture is introduced merely for uniformity.

## 7. PostgreSQL version truth

```text
POSTGRESQL ARCHITECTURE
major 18

PHYSICAL PHASE-TIME EXACT PATCH
18.4

CP2 / CP3 ORIGINAL DIRECT EVIDENCE
18.4 / historical exact

CURRENT CP6 TECHNICAL PATCH
18.6
```

Direct 18.6 evidence:

```text
Backend CI run                         32568664940
workflow event                         workflow_dispatch
executed HEAD                          ec3dc795b5e044daa3a77723c94a1b4b5b92865c
PostGIS                                3.6.4 PASS
pgvector                               0.8.6 PASS
Backend Quality                        SUCCESS / 32 fast tests PASS
Backend PostgreSQL                     SUCCESS / 18 PostgreSQL tests PASS
Backend CI Gate                        SUCCESS
current test corpus                    50 / 50 covered across mandatory lanes
18.6 release-note impact               PASS / NO CURRENT POST-UPGRADE ACTION
```

This is technical-foundation evidence. It does not prove the not-yet-materialized DANTE business schema or business semantic scenarios.

## 8. Direct-validation non-claims

Current truthful non-claims include:

```text
DANTE BUSINESS DATABASE MATERIALIZATION    NOT STARTED
FIRST PRODUCT VERTICAL                     NOT STARTED
DIRECT BUSINESS HG-01..HG-12               NOT BLANKET-PASSED
RESTORE/PITR REHEARSAL                     NOT RUN
REAL V1→V2 BUSINESS-SCHEMA EVOLUTION       NOT RUN
POWERSYNC DIRECT TEST                      NOT RUN
RESTATE DIRECT TEST                        NOT RUN
PRODUCTION DEPLOYMENT                      NOT STARTED
```

As CP6-04 materializes database structures, direct database evidence will replace the applicable `NOT STARTED` entries. Application-semantic evidence remains staged until the relevant application subject exists.

## 9. Active branches / workstreams

```text
feature/logical-postgresql
→ ACTIVE CP6
→ CP6-00 COMPLETE
→ CP6-01 CLOSED / GATE 01 PASS
→ CP6-02 CLOSED / GATE 02 PASS
→ CP6-03 NEXT / WHOLE DANTE DATABASE BLUEPRINT

feature/frontend-materialization
→ independent frontend materialization workstream
```

Frontend/backend may progress independently. Shared current docs must preserve the newest reconciled truth.

## 10. Exact current backend action

```text
1. Treat Product/Domain/Logical/Physical and CP1–CP5 as closed accepted authority.
2. Treat CP6-01 and CP6-02 as CLOSED; do not redo their discovery/design work.
3. Read the full 57/57 coverage and closed PostgreSQL Constitution.
4. Start CP6-03 as WHOLE DANTE DATABASE BLUEPRINT.
5. Derive every database structure already determinable from closed authority.
6. Do not hide determinable schema behind a generic “vertical-specific” label.
7. Do not invent unresolved product semantics merely to fill a table.
8. Produce the implementation/migration DAG and mapping/test plan.
9. After Gate 03, CP6-04 materially implements the approved DANTE database.
10. CP6-05 directly validates the materialized database and closes CP6.
11. Only after CP6 closure does the first product vertical application phase begin.
```

## 11. Durable pointers

Current truth / navigation:

```text
README.md
docs/README.md
docs/ROADMAP.md
docs/workstreams/logical-postgresql.md
```

Closed upstream workstreams:

```text
docs/workstreams/domain-model.md
docs/workstreams/logical-model.md
docs/workstreams/pre-physical-coherence.md
docs/workstreams/physical-model.md
docs/workstreams/engineering-foundation.md
docs/workstreams/backend-scaffold.md
```

CP6 current execution details are owned by `docs/workstreams/logical-postgresql.md`.
