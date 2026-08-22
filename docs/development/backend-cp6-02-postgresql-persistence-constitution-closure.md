# Backend CP6-02 — PostgreSQL Persistence Constitution — Closure

- **Status:** CLOSED / GATE 02 PASS
- **Date:** 2026-08-22
- **Branch:** `feature/logical-postgresql`
- **Closure PRE-SCOPE:** `8b2d00b993c0cb9b40df64a85909c792a7e057ea`
- **Checkpoint:** CP6-02 — PostgreSQL Persistence Constitution
- **Closed Constitution:** `docs/development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Next checkpoint at closure time:** CP6-03 — Concrete Relational Topology + Implementation Dependency DAG + Vertical Decomposition
- **Business implementation at Gate 02:** NOT AUTHORIZED / NOT STARTED

## 1. Closure purpose

This record closes CP6-02 after the reusable PostgreSQL persistence doctrine was reconstructed, researched, benchmarked, hardened, directly re-proved at the applicable technical foundation boundary and independently reviewed.

Gate 02 closes **global reusable PostgreSQL persistence rules**. It does not create business schema, does not implement a business vertical and does not convert future business-semantic or destructive-recovery obligations into direct PASS.

The closed Constitution is consumed by CP6-03 and later CP6 checkpoints. A future reopen requires concrete contradictory evidence, not implementation convenience.

## 2. Upstream authority consumed without reopen

```text
Domain Model                              CLOSED
Whole Logical Model                       CLOSED / 57 OF 57 CLASSIFIED
WL-H01..WL-H12                            ACTIVE / PRESERVED
Physical Model                            CLOSED / SELECTED / ACCEPTED
PostgreSQL architecture                   major 18 / sole canonical persistence
Physical phase-time exact patch           18.4 / historical
CP1–CP5 backend scaffold                  CLOSED / DIRECT QA PASS
CP6-01                                    CLOSED / GATE 01 PASS
CP3 transaction/migration/privilege model PRESERVED
```

No Domain owner, Logical representation family or selected Physical technology was reclassified by CP6-02.

## 3. Technology lifecycle and PostgreSQL 18.6 evidence

CP6-02 distinguished architectural authority from maintenance-patch lifecycle:

```text
PostgreSQL architecture family          18
Physical exact phase-time patch         18.4
CP2 / CP3 original direct patch         18.4 / historical exact evidence
current CP6 technical patch             18.6
```

The repository-controlled technical envelope was refreshed from PostgreSQL 18.4 to 18.6 without changing the selected major family, PostgreSQL extension choices, business schema or Alembic history.

Direct remote evidence:

```text
Backend CI run                         32568664940
workflow event                         workflow_dispatch
executed HEAD                          ec3dc795b5e044daa3a77723c94a1b4b5b92865c
PostgreSQL base                        postgres:18.6-trixie
base OCI index digest                  sha256:ae6c78831cbc35fa3a4aaf4d763ddacf6183d6004774cc2dc28b3920410d1d1a
PostGIS                                3.6.4 PASS
pgvector                               0.8.6 PASS
Backend Quality                        SUCCESS
fast test lane                         32 / 32 PASS
Backend PostgreSQL                     SUCCESS
real PostgreSQL lane                   18 / 18 PASS
Backend CI Gate                        SUCCESS
current test corpus                    50 / 50 covered across mandatory lanes
```

The PostgreSQL lane directly covered the existing technical foundation, including:

```text
Alembic fresh database → single head        PASS
Alembic head → base → head                  PASS
Alembic schema drift check                  PASS
owner/migrator/runtime posture              PASS
explicit SET ROLE                           PASS
runtime privilege rejection                 PASS
runtime identity/search_path                PASS
pool_pre_ping stale-connection recovery     PASS
DB outage/readiness recovery                PASS
readiness detail redaction                  PASS
engine disposal                             PASS
autobegin=False                             PASS
real commit persistence                     PASS
whole-transaction rollback                  PASS
flush != commit                             PASS
SAVEPOINT outer-transaction preservation    PASS
```

The 50-test corpus was covered across the two mandatory CI lanes and is not misreported as one single `pytest` invocation.

PostgreSQL 18.6 release-note impact review:

```text
PASS / NO CURRENT POST-UPGRADE ACTION
```

The currently materialized DANTE foundation has no custom logical-decoding output plugin, `pgcrypto`, business GIN index, `btree_gist` or `ltree` object requiring an 18.6-specific action. Future PowerSync/logical-replication activation remains responsible for reviewing then-current logical-decoding restrictions, including `output_plugin_libraries`, and all applicable maintenance requirements.

## 4. External benchmark / standards review

CP6-02 compared DANTE's candidate doctrine against current primary-source technology/standards and public large-system engineering evidence, including:

```text
PostgreSQL official documentation / release notes
RFC 9562 UUID
Python 3.14 UUIDv7
IANA TZDB
ISO 4217
Stripe idempotency / online migration practice
GitLab migration discipline
Linear local-first behavior / destructive CASCADE incident
Notion PostgreSQL scaling / sharding evidence
Alembic explicit autocommit boundary
```

External evidence was used as pressure-test evidence only. It did not replace Domain/Logical/Physical authority.

Key dispositions retained by the closed Constitution include:

```text
UUIDv7 stable DANTE identity                     ADOPT / BOUNDED
PostgreSQL native uuid storage                   ADOPT
UUIDv7 order as semantic chronology              REJECT
homogeneous NativeRef direct FK                  ADOPT
heterogeneous NativeRef bounded anchor           ADOPT / REQUIRED
one-of-N FK for one heterogeneous NativeRef      REJECT
bounded MaterialStateRef address/control         ADOPT / REQUIRED
kind+uuid without DB referential integrity       REJECT
ON DELETE NO ACTION default                      ADOPT
CASCADE default                                  REJECT
PostgreSQL ENUM everywhere                       REJECT
PostgreSQL money for MonetaryAmount              REJECT
declarative constraints first                    ADOPT
global SERIALIZABLE                              REJECT
whole-transaction retry where applicable         ADOPT
RLS as Domain governance                         REJECT
RLS as defense-in-depth                          MAY
speculative sharding/partitioning                REJECT
expand/backfill/cutover/contract migration       ADOPT
fake destructive downgrade                       REJECT
isolated non-transactional PostgreSQL DDL        ADOPT WHEN REQUIRED
```

## 5. Closed Constitution families

The final Constitution closes the following reusable rule families:

```text
TECH  technology lifecycle
ID    physical identity
REF   reference addressing
MAT   material state/current truth
HIST  historical truth
TIM   temporal truth
MISS  missing/unknown/negative semantics
LIFE  lifecycle/retention/tombstone
TYP   PostgreSQL type doctrine
REL   relation doctrine
CON   constraint doctrine
IDX   index doctrine
TX    transaction/concurrency doctrine
IDEM  idempotency doctrine
PROV  consequential provenance
CAP   PostgreSQL capability boundaries
MIG   migration/evolution doctrine
SEC   ownership/privilege doctrine
QA    direct persistence acceptance doctrine
```

Final family result:

```text
TECH  PASS
ID    PASS
REF   PASS
MAT   PASS
HIST  PASS
TIM   PASS
MISS  PASS
LIFE  PASS
TYP   PASS
REL   PASS
CON   PASS
IDX   PASS
TX    PASS
IDEM  PASS
PROV  PASS
CAP   PASS
MIG   PASS
SEC   PASS
QA    PASS
```

## 6. Independent review and repair

The independent whole-Constitution review intentionally attempted to find contradictions, ambiguous implementation paths and under-specified global decisions.

It found six bounded hardenings rather than an upstream architecture failure:

```text
IR-01 idempotency uniqueness ambiguity
IR-02 heterogeneous NativeRef alternate one-of-N FK path
IR-03 MaterialStateRef address/control mechanism left optional
IR-04 UUID persistence/index posture insufficiently explicit
IR-05 operational timeout/error taxonomy missing
IR-06 PostgreSQL non-transactional migration DDL boundary missing
```

All were repaired before closure.

### IR-01 — Idempotency

Closed rule:

```text
UNIQUE(operation_scope, idempotency_key)
material-operation fingerprint = immutable comparison field
same key + same fingerprint      → replay/observe established result
same key + different fingerprint → conflict/reject
```

For an entirely PostgreSQL-local canonical effect, idempotency reservation, canonical effect and retained result binding are transactionally coordinated. External effects remain explicitly staged/provider-idempotent/reconciled as applicable.

### IR-02 — NativeRef

Closed rule:

```text
homogeneous NativeRef contract
→ direct FK

genuinely heterogeneous NativeRef contract
→ bounded native-address anchor
```

The database must enforce address existence, concrete owner existence, owner family and consuming Reference Contract eligibility. A `type + uuid` pair checked only by application code is insufficient.

### IR-03 — MaterialStateRef

Closed rule requires a bounded material-state address/control family:

```text
stable UUIDv7 MaterialStateRef
+ exact semantic owner address
+ exact facet/purpose
+ bounded technical address/control metadata
+ owner-specific material-state semantic row
+ explicit current accepted-state binding where required
```

The shared address/control layer is not a universal `Fact`, `Version` or generic semantic payload table.

### IR-04 — UUID persistence/indexing

Closed rule:

```text
native PostgreSQL uuid storage
ordinary PK/UNIQUE B-tree default
no redundant PK/UNIQUE index
UUIDv7 ordering/locality != semantic chronology
```

### IR-05 — Runtime time/error posture

Closed doctrine distinguishes applicable PostgreSQL operational budgets such as statement/transaction/lock/idle-in-transaction timeouts without inventing one global magic value.

It also preserves distinct handling for:

```text
expected-state mismatch
unique/exclusion/invariant conflict
serialization failure
deadlock
timeout
known pre-commit connection failure
ambiguous commit outcome
```

Timeout/ambiguous outcome never authorizes blind retry.

### IR-06 — Non-transactional migration DDL

PostgreSQL DDL that cannot execute inside a normal transaction block, such as `CREATE INDEX CONCURRENTLY`, is an explicit isolated boundary. Alembic autocommit execution is used only where required; unrelated DDL is not mixed into that boundary; failure/INVALID-artifact cleanup and post-operation verification are required.

The existing CP3 migrator posture remains preserved: dedicated migrator authentication + explicit `SET ROLE dante_owner` + least-privilege runtime separation.

## 7. Targeted post-repair verification

The repaired Constitution was read back remotely and targeted against the accepted Physical mapping, Whole-Logical hardenings, PostgreSQL risk lanes and CP3 foundation.

Result:

```text
ID       CLEAN
REF      CLEAN
MAT      CLEAN
TX       CLEAN
IDEM     CLEAN
MIG      CLEAN
QA       CLEAN

WL-H05   PRESERVED
WL-H06   PRESERVED
WL-H07   PRESERVED

PG-R01   PROOF PATH COMPLETE / STAGED
PG-R02   PROOF PATH COMPLETE / STAGED
PG-R03   PROOF PATH COMPLETE / STAGED
PG-R04   PROOF PATH COMPLETE / STAGED
PG-R05   PROOF PATH COMPLETE / STAGED

CP3 contradiction                0
Logical contradiction            0
Physical contradiction           0
semantic owner reopen            0
generic semantic root            0
business DDL                     0
business migration               0
business SQLAlchemy mapping      0
persistence adapter              0
false HG / PSV PASS              0
unstaged new proof obligation    0

POST-REPAIR REVIEW
CLEAN
```

## 8. Gate 02 result

Formal Gate 02 contract:

```text
all genuinely global concrete decisions closed        PASS
all inherited decisions traceable                     PASS
all remaining decisions explicitly vertical-specific  PASS
all direct-proof obligations have stage/owner         PASS

universal Entity root                                 0
universal Relationship root                           0
generic canonical EAV                                 0
generic history/event ontology                        0
provider token == MaterialStateRef                     0
NULL-as-universal-negative                             0
silent consequential LWW                              0
implicit ORM schema authority                          0

CP3 contradiction                                      0
Logical contradiction                                  0
Physical contradiction                                 0

PG-R01..PG-R10 concrete proof path                    complete
applicable PSV ownership/stage                         complete
```

Additional implementation counters:

```text
business table/schema design                           0
business Alembic migration                             0
business SQLAlchemy mapping                            0
persistence adapter                                    0
application use case                                   0
business API                                           0
Vertical #1 implementation                             0
Physical Model reopen                                  0
```

Verdict:

```text
CP6-02
CLOSED / GATE 02 PASS

POSTGRESQL PERSISTENCE CONSTITUTION
CLOSED / ACCEPTED
```

## 9. Direct-proof truth preserved

Gate 02 closes doctrine and staging; it does **not** falsify future evidence.

In particular:

```text
HG-09 retention/redaction/tombstone/restore
HOLD until destructive proof

HG-11 schema/data evolution
HOLD until real V1 → V2 proof

HG-12 recoverability/evidence quality
HOLD until destructive recovery proof
```

PSV items remain at their exact CP6-01 assigned stages. Business-semantic HG/SC/PSV scenarios remain unpassed until an actual qualifying subject exists and executes.

The PostgreSQL 18.6 regression is direct **technical foundation** evidence only.

## 10. Closure write scope

Approved closure PRE-SCOPE:

```text
8b2d00b993c0cb9b40df64a85909c792a7e057ea
```

Approved closure paths:

```text
CREATE
docs/development/backend-cp6-02-postgresql-persistence-constitution-closure.md

UPDATE
docs/development/backend-cp6-02-postgresql-persistence-constitution.md
docs/workstreams/logical-postgresql.md
README.md
apps/backend/README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/architecture/system-overview.md
docs/physical-model/README.md
docs/development/local-backend-workstation-bootstrap.md

DELETE
NONE
```

The closure scope is documentation/status reconciliation only. No business implementation or unrelated code/infra mutation is authorized by this write.

## 11. Next checkpoint at closure time

```text
CP6-03
Concrete Relational Topology
+ Implementation Dependency DAG
+ Vertical Decomposition
NEXT / NOT STARTED
```

At Gate-02 closure time, CP6-03 was defined as read/research/design-first and Gate 02 itself did not authorize business DDL. This is exact historical closure-time scope truth.

## 12. Post-closure editorial / authority maintenance — 2026-08-22

A later independent editor/architecture review found that the Gate-02 closure's statement that current-truth reconciliation was complete had been too broad as an **editorial-current-state claim**.

The technical CP6-02 review and Gate-02 result remain valid. However, several files marked `CURRENT` outside the immediate closure entrypoint set still contained stale pre-Physical/pre-scaffold language, including architecture index/technical-decision wording and historical ADR sections labelled as current.

Post-closure maintenance therefore corrected those current-authority surfaces and added ADR-010 as the durable architectural acceptance record for the Constitution.

This maintenance explicitly distinguishes:

```text
CP6-02 TECHNICAL CONSTITUTION / GATE 02
CLOSED / PASS / NOT REOPENED

ORIGINAL CURRENT-TRUTH RECONCILIATION CLAIM
editorially incomplete outside the immediate closure surfaces

LATER EDITORIAL REPAIR
repairs CURRENT architecture/decision wording
qualifies historical ADR posture
adds ADR-010
hardens Gate 03 cross-cutting coverage
```

No Domain/Logical/Physical decision was changed. No CP6-02 technical rule was changed. No business schema/migration/mapping was introduced by this maintenance.

The active CP6 workstream now supersedes the old process/staging interpretation that prohibited business database materialization throughout all of CP6. That later execution-boundary repair does **not** retroactively alter the fact that CP6-02 itself correctly closed with zero business DDL.

The current CP6-03 contract is now:

```text
WHOLE DANTE DATABASE BLUEPRINT
= maximum non-speculative persistence derivable from closed authority

coverage requirement
= 57 / 57 Domain concepts
+ 100% CP6-01 Part-2 cross-cutting/non-owner persistence constructs accounted

first product vertical
= POST-CP6
```

Current execution authority for CP6-03 and later stages is `docs/workstreams/logical-postgresql.md`.