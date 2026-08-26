# DANTE Backend CP6-05 — Whole Database Direct QA / Final Closure

**Status:** CLOSED / DIRECT QA PASS  
**Branch:** `feature/logical-postgresql`  
**Final accepted implementation HEAD:** `22bbc078391d52c43665474bf465593d6225106e`  
**CP6-05 implementation PRE-SCOPE:** `6972852d0b62066f2e00f20f6e24a0f2e1cbd8da`  
**Accepted materialization before CP6-05:** CP6-M01..M07 + persistent LOCAL PostgreSQL 18.6  
**Final persistent LOCAL revision:** `20260826_08`  

## Purpose

CP6-05 is the mandatory whole-database clean-room gate. It does not add product semantics. It reconciles the final accepted database across architecture/reference, Dictionary, SQLAlchemy, Alembic, real PostgreSQL and executable proof.

## Audit disposition

```text
DB topology defect                           0
ACL topology defect                          0
Role-13 concurrency-defense defect           1 → repaired by 20260826_08
historical stage-scope test defect           1 → repaired stage-relatively
mapping filename documentation drift         1 → narrowly superseded by Part 19
Dictionary final proof-trace gap              occurrence-generation family → final QA proof added
whole-head cross-representation proof gap     → test_cp6_final.py
```

The historical defects and failed runs remain part of the evidence record. Closure does not rewrite them as first-pass green.

## Corrective revision

`20260826_08_cp6_final_qa_hardening.py` is forward-only from M7 and changes no frozen object count. It replaces only the body of existing `dante.enforce_occurrence_generation_integrity()` so Role-13 independently acquires the exact occurrence-generation advisory lock before final validation.

The advisory digest is changed at the technical lock-key layer from the pre-closure BLAKE2b planning contract to the cross-language SHA-256 v2 contract frozen by Part 19. No persisted identifier or business data changes.

## Final proof composition

Existing P0/M1..M7 tests remain required. `test_cp6_final.py` and `test_cp6_final_catalog.py` add final-head evidence for:

- exact PostgreSQL 18.6 environment and zero forbidden object families;
- exact `68/5/14/75/95/68/120` topology;
- semantic Dictionary internal integrity;
- Dictionary ↔ SQLAlchemy mapping import/symbol reconciliation;
- Dictionary ↔ Alembic revision/head reconciliation;
- Dictionary ↔ live PostgreSQL relation/column/constraint/index/trigger reconciliation;
- Python ↔ PostgreSQL advisory golden vectors for namespaces 1..7;
- real AsyncSession transaction-lock acquisition/release and deduplication;
- Role-13 final definition proof;
- real two-connection quota race without application locks;
- real two-connection elapsed duplicate race without application locks.

Draft 2020-12 structural validation is intentionally test-tool-only and uses pinned `check-jsonschema==0.37.4`; it is not an application dependency.

## Final user-executed direct acceptance — 2026-08-26

The exact accepted candidate was:

```text
22bbc078391d52c43665474bf465593d6225106e
```

The final full acceptance was executed on the canonical WSL/Linux workstation against repository-controlled PostgreSQL 18.6.

Observed non-PostgreSQL quality evidence:

```text
candidate / remote exact SHA                PASS
uv                                          0.12.5
locked environment                          PASS
ruff format --check                         PASS — 44 files already formatted
ruff check                                  PASS
mypy strict                                 PASS — 40 source files
pytest -m "not postgres"                    PASS — 37 / 37
uv build                                    PASS — sdist + wheel
```

Observed canonical PostgreSQL image evidence:

```text
image                                        dante-postgres-local:18.6
server                                       PostgreSQL 18.6
image build                                  PASS
```

Observed disposable real-PostgreSQL acceptance:

```text
113 collected
37 deselected
76 selected
76 passed
0 failed
54.89s
coverage 95.40% evidence only
```

The 76-test run includes final lock-contract/concurrency proof, M1..M7 stage proofs, migration fresh/head/base round trips, Alembic drift, exact security/ACL posture, runtime outage/recovery and transaction semantics.

## Persistent LOCAL materialization and closure evidence

Only after the disposable suite passed, the ordinary persistent LOCAL PostgreSQL cluster was reconciled and upgraded.

Observed progression:

```text
LOCAL pre-revision                            20260826_07
P0 provisioning/security reconciliation       PASS
runtime credential/config synchronization     PASS
Alembic upgrade                               20260826_07 → 20260826_08
Alembic current                               20260826_08 (head)
Alembic check                                 No new upgrade operations detected
```

Observed final topology:

```text
tables              68
views                5
routines            14
triggers            75
physical indexes    95
foreign keys        68
check constraints  120
```

Observed final security posture:

```text
expected DANTE roles                          3 / 3
expected owner→migrator membership            1 / 1
all DANTE role-membership edges               1
owner password                                NULL
runtime SELECT on dante.alembic_version       denied
```

The persistent compose cluster was then stopped and recreated **without deleting volumes**. After restart:

```text
Dictionary JSON-Schema validation             PASS
postgres-data volume                          retained
revision                                      20260826_08
final topology                                68|5|14|75|95|68|120
GET /health/live                              200 {"status":"ok"}
GET /health/ready                             200 {"status":"ready"}
repository/candidate guard                    PASS
```

Initial connection-refused curl attempts while Uvicorn was still starting are startup polling noise; the required final live/ready responses were both observed as HTTP 200.

## Final closure disposition

The closure condition is satisfied on exact implementation HEAD `22bbc078391d52c43665474bf465593d6225106e`.

```text
CP6-03  CLOSED / GATE 03 PASS
CP6-04  CLOSED / MATERIALIZATION PASS
CP6-05  CLOSED / DIRECT QA PASS

CP6
CLOSED / CONCRETE POSTGRESQL DATABASE PASS

DANTE DATABASE
BLUEPRINT COMPLETE
MATERIALIZED TO MAXIMUM NON-SPECULATIVE EXTENT
MIGRATED TO 20260826_08
MAPPED
DICTIONARY-RECONCILED
DIRECTLY TESTED
PERSISTENT LOCAL VERIFIED
QA CLEAN
```

First product-vertical application behavior remains post-CP6 work. No protected-`main` integration is authorized by this closure document; branch-to-main alignment/merge requires its own explicit user gate and protected repository path.
