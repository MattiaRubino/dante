# Physical Model Result Register v1

- Status: **CURRENT — PM-01 READ-ONLY PASS-CONDITIONAL / PM-02 NOT AUTHORIZED**
- Workstream: `feature/physical-model`
- Benchmark execution: **NOT STARTED**
- Technology selection: **NONE**
- Every executable candidate result remains `NOT RUN`.
- PM-01 evidence: `pm-01-technology-landscape-v1.md`

## Rule

This file records current Physical execution/disposition state. It does not override Domain/Logical authority, the Phase-10 benchmark method, or create selection by prose.

```text
OFFICIAL CLAIM != EXECUTED PROOF
ADMIT != HARD-GATE PASS
NOT RUN != PASS
PREFERRED != SELECTED
```

A benchmark result changes only after evidence is remotely written/linked and the corresponding gate is QA-verified.

# PM-01 status

```text
TECHNOLOGY DISCOVERY                 PASS
APPLICATION ARCHITECTURE RECON       PASS
PRIMARY ADMISSION                    PASS
EXACT SUBJECT FREEZE                 PASS for P0/P1/P2/P3 qualification subjects
LICENSE/COST REVIEW                  PASS-CONDITIONAL
PYTHON/CLIENT REVIEW                 PASS
BACKUP/EVOLUTION REVIEW              PASS-CONDITIONAL
HA/PRODUCTION-TOPOLOGY REVIEW        PASS-CONDITIONAL
BENCHMARK HOST FREEZE                HOLD

PM-01 OVERALL
PASS-CONDITIONAL

MAPPING
NOT STARTED

BENCHMARK
NOT STARTED

SELECTED
NONE
```

The host HOLD does not invalidate the read-only technology/admission result. It must be closed before executable harness/benchmark evidence begins.

# Lane P — Primary canonical persistence

## P0 — PostgreSQL hybrid

```text
REGISTERED ROLE
mandatory preferred baseline

PM-01 DISPOSITION
ADMIT

EXACT SUBJECT
PostgreSQL 18.4
self-hosted single-node qualification topology
psycopg 3.3.4

MAPPING
NOT STARTED

HG-01..HG-12
NOT RUN

CORRECTNESS / DESTRUCTIVE
NOT RUN

LOW
NOT RUN

BASE
NOT RUN

HIGH
NOT RUN

RECOVERY / EVOLUTION
NOT RUN

WEIGHTED SCORE
NOT RUN

SENSITIVITY
NOT RUN

CURRENT DISPOSITION
ADMIT / PREFERRED-BASELINE / NOT SELECTED
```

Conditions/caveats:

- pre-existing `PREFERRED` label remains a baseline posture only;
- PostgreSQL must not be rescued with generic JSONB/property-bag/meta-root semantics;
- explicit history/reference/governance/evolution mapping complexity is evidence, not a reason to weaken LifeOS semantics.

Evidence: `pm-01-technology-landscape-v1.md`.

## P1 — TypeDB

```text
REGISTERED ROLE
mandatory semantic challenger

PM-01 DISPOSITION
ADMIT

EXACT SUBJECT
TypeDB CE 3.12.3
self-hosted single-node qualification topology
official typedb-driver 3.12.3

MAPPING
NOT STARTED

HG-01..HG-12
NOT RUN

CORRECTNESS / DESTRUCTIVE
NOT RUN

LOW
NOT RUN

BASE
NOT RUN

HIGH
NOT RUN

RECOVERY / EVOLUTION
NOT RUN

WEIGHTED SCORE
NOT RUN

SENSITIVITY
NOT RUN

CURRENT DISPOSITION
ADMIT / NOT SELECTED
```

Conditions/caveats:

- transactions document ACID up to snapshot isolation;
- WL-H05 expected-state and WL-H07 multi-owner consistency require explicit PM-02/03 proof;
- self-hosted backup responsibility and non-incremental recommended paths remain operational evidence conditions;
- TypeDB 3.x cluster is experimental/alpha and receives no production HA credit in this subject.

Evidence: `pm-01-technology-landscape-v1.md`.

## P2 — XTDB

```text
REGISTERED ROLE
PM-01-admitted temporal/bitemporal primary challenger

PM-01 DISPOSITION
ADMIT / PRODUCTION-TOPOLOGY HOLD

EXACT SUBJECT
XTDB 2.1.0 stable
local/self-hosted qualification subject
Postgres wire protocol / compatible client path

MAPPING
NOT STARTED

HG-01..HG-12
NOT RUN

CORRECTNESS / DESTRUCTIVE
NOT RUN

LOW
NOT RUN

BASE
NOT RUN

HIGH
NOT RUN

RECOVERY / EVOLUTION
NOT RUN

WEIGHTED SCORE
NOT RUN

SENSITIVITY
NOT RUN

CURRENT DISPOSITION
ADMIT / PRODUCTION-TOPOLOGY HOLD / NOT SELECTED
```

Conditions/caveats:

- every table is bitemporal, but XTDB system/valid time must not automatically become every LifeOS historical/temporal semantic;
- DML transactions are non-interactive and use DML/`ASSERT` rather than mixing result-returning `SELECT` with writes;
- write transactions are serialized through a totally ordered log;
- standalone Docker is explicitly non-production/non-distributed;
- production topology/dependencies remain HOLD until a separately frozen execution subject is justified.

Evidence: `pm-01-technology-landscape-v1.md`.

## P3 — SurrealDB

```text
REGISTERED ROLE
PM-01-admitted multimodel primary challenger

PM-01 DISPOSITION
ADMIT-CONDITIONAL

EXACT SUBJECT
SurrealDB Community 3.2.3
self-hosted single-node qualification topology
RocksDB storage
Python SDK 2.0.0

MAPPING
NOT STARTED

HG-01..HG-12
NOT RUN

CORRECTNESS / DESTRUCTIVE
NOT RUN

LOW
NOT RUN

BASE
NOT RUN

HIGH
NOT RUN

RECOVERY / EVOLUTION
NOT RUN

WEIGHTED SCORE
NOT RUN

SENSITIVITY
NOT RUN

CURRENT DISPOSITION
ADMIT-CONDITIONAL / NOT SELECTED
```

Conditions/caveats:

- transactions use snapshot isolation with write-write conflict detection;
- multimodel flexibility must not become a universal Thing/edge/property-bag semantic root;
- Community single-node capability is the frozen qualification subject;
- SurrealDS multi-node HA is a Cloud Scale/self-hosted Enterprise topology and receives no Community-subject credit;
- license/TCO/exit conditions remain explicit if Enterprise/distributed capability becomes materially required.

Evidence: `pm-01-technology-landscape-v1.md`.

# Primary reserves / non-admitted current candidates

| Candidate | PM-01 disposition | Current reason |
|---|---|---|
| MariaDB 11.8 LTS | DEFER — first reserve | Relevant temporal capability, but heavy relational-lane overlap plus history/evolution caveats; must justify fifth mapping |
| Gel 7 | DEFER | Interesting schema/query/migration direction but current continuity/operational uncertainty does not displace admitted set |
| CockroachDB | DEFER | Reopen on real distributed/geographic HA requirement |
| YugabyteDB | DEFER | Reopen on real distributed/geographic HA requirement |
| MongoDB | REJECT-FROM-BENCHMARK primary | No sufficiently distinct current canonical-primary hypothesis |
| ArangoDB | REJECT-FROM-BENCHMARK primary | Multimodel hypothesis overlaps admitted P3 without enough distinct value now |
| Dgraph | REJECT-FROM-BENCHMARK primary | Graph specialization belongs in bounded G lane |
| FoundationDB | REJECT-FROM-BENCHMARK primary | Too low-level for current canonical mapping objective |
| Datomic | REJECT-FROM-BENCHMARK primary | Generic entity/attribute/value orientation conflicts with closed generic-EAV/meta-model rejection |
| Dolt / Doltgres | REJECT-FROM-BENCHMARK primary | Git-like versioning is not LifeOS material history/correction/knowledge chronology |

`REJECT-FROM-BENCHMARK` is scoped to the current primary benchmark and may be reopened by materially new requirements/evidence.

# Lane G — Secondary graph / traversal

## G0 — no specialized graph store

```text
SUBJECT
primary-store query/projection baseline after primary mapping exists

EXECUTION
NOT RUN

CG-01..CG-04
NOT RUN where applicable

G-LANE SCORE
NOT RUN

CURRENT DISPOSITION
BASELINE / NOT RUN
```

## G1 — Neo4j

```text
PM-01 DISPOSITION
DEFER TO PM-08 / registered graph challenger

EXACT SUBJECT
NOT FROZEN — only when G lane execution is admitted

EXECUTION
NOT RUN

CG-01..CG-04
NOT RUN

LOW / BASE / HIGH
NOT RUN

G-LANE SCORE
NOT RUN

NET BENEFIT
NOT RUN

CURRENT DISPOSITION
DEFER / NOT RUN / NOT SELECTED
```

No graph product becomes canonical truth by winning a traversal benchmark.

# Lane S — Search / semantic retrieval

## S0 — structured + lexical/full-text baseline

```text
SUBJECT
accepted primary architecture native/bounded baseline

EXECUTION
NOT RUN

SEARCH CORRECTNESS
NOT RUN

DISCLOSURE / PROPAGATION
NOT RUN

LOW / BASE / HIGH
NOT RUN

CURRENT DISPOSITION
BASELINE / NOT RUN
```

## S1 — pgvector

```text
PM-01 DISPOSITION
DEFER TO PM-08 / registered vector candidate

ADMISSION CONDITION
PostgreSQL present/applicable in accepted benchmark architecture

EXACT SUBJECT
NOT FROZEN

EXECUTION
NOT RUN

CG-01..CG-04
NOT RUN

RECALL / PRECISION
NOT RUN

FILTERED RECALL
NOT RUN

LOW / BASE / HIGH
NOT RUN

CURRENT DISPOSITION
DEFER / NOT RUN / NOT SELECTED
```

Vector quality is judged after applicable scope/Visibility filtering, not from unfiltered top-k latency alone.

PM-01 application reconnaissance adds supporting evidence that products such as Linear and AppFlowy have used PostgreSQL/pgvector instead of immediately introducing a dedicated vector datastore. This does not create a LifeOS selection.

## Other search/vector specialists

```text
Qdrant / OpenSearch
DEFER
admit only on measured specialist trigger / structural benefit
```

# Local / offline bounded lane observation

```text
SQLite
DEFER — future local/offline/client role
NOT admitted as current server canonical primary
```

PM-01 application reconnaissance found materially relevant local-first/local-store patterns in Notion, Anytype and Home Assistant. These support keeping a future local/offline lane explicit; they do not authorize offline multi-master/CRDT semantics today.

# Lane E/D — Event / document bounded mechanisms

## ED0 — bounded native mechanisms

```text
STATUS
BASELINE CLASS

EXECUTION
NOT RUN / assessed only where Physical scenarios require it
```

## ED-SPECIALIZED

```text
ADMISSION
NONE

CANDIDATE
NONE

STATUS
NOT ADMITTED
```

A named specialized product requires a separate admission record/gate proving a concrete accepted gap or structural benefit.

# Durable-runtime coupling observations

No durable runtime is selected by the Physical workstream.

```text
Restate   NOT SELECTED
Temporal  NOT SELECTED
DBOS      NOT SELECTED
```

Physical evidence may change relative infrastructure coupling/operational economics, but persistence benchmark points cannot be awarded to a runtime and runtime preference cannot select primary persistence.

Known Phase-7 posture remains:

```text
DBOS local/bounded Python        SQLite-capable
DBOS production guidance         PostgreSQL-recommended
DBOS distributed multi-server    PostgreSQL-coupled
```

# Application architecture reconnaissance — registered implications

The complete evidence is in `pm-01-technology-landscape-v1.md`.

Current implications only:

```text
successful-product usage != LifeOS selection
PostgreSQL industry maturity     supporting baseline evidence only
local SQLite/CRDT patterns       future bounded local/offline pressure
sync/cache/projection divergence must remain explicit
rehearsed restore                PM-07 requirement strengthened
pgvector-before-new-vector-DB    bounded-specialization evidence only
jobs/files/AI                    separate roles, not canonical truth
generic ORM portability          not a real migration guarantee
```

No competitor architecture overrides Domain/Logical semantics.

# Solver / AI / provider interaction

Physical tests may need to persist candidate/derived/provider/runtime-related state, but:

```text
solver output != accepted canonical effect
AI eval/result != canonical LifeOS truth
provider revision != MaterialStateRef
runtime workflow completion != Actual automatically
```

No model/provider/solver/runtime product is selected by this register.

# Evidence checkpoints

## PM-00 Bootstrap

```text
PRE-SCOPE
main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79

CREATE CHECKPOINT
6d76bc150dfd7b3cefe56c6e05c96404e7494626
6 added / 0 modified / behind 0

CONTENT-QA CHECKPOINT
8549e1c95bef2e354bd47028259e6816bf5e9272
22 unique paths
6 added
16 modified
0 deleted
0 unexpected
behind 0
main unchanged

STATUS
QA PASS
```

## PM-01 Technology discovery / candidate freeze

```text
RESEARCH PRE-SCOPE
622767d5435d59766459bb25a57e5afeb7dd7336

EVIDENCE
pm-01-technology-landscape-v1.md

STATUS
PASS-CONDITIONAL

BENCHMARK HOST
HOLD

MAPPING
NOT STARTED

BENCHMARK
NOT STARTED

SELECTION
NONE
```

The PM-01 evidence record includes technology-family discovery, exact subject/admission results, cost/license posture and public application-architecture reconnaissance.

## PM-02 Primary mapping

```text
STATUS
NOT STARTED / NOT AUTHORIZED
```

## PM-03 Hard-gate preflight

```text
STATUS
NOT STARTED
```

## PM-04 Harness/fixtures

```text
STATUS
NOT STARTED
```

## PM-05+ Execution

```text
STATUS
NOT STARTED
```

# Recommendation ledger

| Lane | Candidate | Exact subject | PM-01 admission | Hard-gate result | Score | Sensitivity | Selected? |
|---|---|---|---|---|---|---|---|
| P | PostgreSQL hybrid | 18.4 / self-host single-node / psycopg 3.3.4 | ADMIT | NOT RUN | NOT RUN | NOT RUN | NO |
| P | TypeDB | CE 3.12.3 / self-host single-node / driver 3.12.3 | ADMIT | NOT RUN | NOT RUN | NOT RUN | NO |
| P | XTDB | 2.1.0 / qualification subject / pgwire | ADMIT / topology HOLD | NOT RUN | NOT RUN | NOT RUN | NO |
| P | SurrealDB | CE 3.2.3 / single-node RocksDB / Python SDK 2.0.0 | ADMIT-CONDITIONAL | NOT RUN | NOT RUN | NOT RUN | NO |
| G | G0 no-specialized-store | future primary-dependent | BASELINE | NOT RUN | NOT RUN | NOT RUN | NO |
| G | Neo4j | NOT FROZEN | DEFER PM-08 | NOT RUN | NOT RUN | NOT RUN | NO |
| S | S0 structured/FTS | future primary-dependent | BASELINE | NOT RUN | NOT RUN | NOT RUN | NO |
| S | pgvector | conditional / NOT FROZEN | DEFER PM-08 | NOT RUN | NOT RUN | NOT RUN | NO |
| E/D | ED0 bounded native | future primary/runtime-dependent | BASELINE CLASS | applicable checks NOT RUN | N/A | NOT RUN | NO |
| E/D | specialized | NONE | NOT ADMITTED | N/A | N/A | N/A | NO |

# Result mutation protocol

Before changing any candidate hard-gate/execution result from `NOT RUN`:

1. identify exact evidence record/path/artifact;
2. verify candidate subject/version/edition/topology;
3. verify scenario/mapping revision;
4. update only the applicable result fields;
5. preserve unresolved items as `HOLD`/`NOT RUN` rather than inferring completion;
6. remote-read back the register;
7. record checkpoint in `docs/workstreams/physical-model.md`.

Before writing a new `PREFERRED`, PM-09/10 evidence must exist.

Before writing `SELECTED`, PM-11 explicit selection gate and user approval are mandatory.

# Current next step

```text
PM-01
PASS-CONDITIONAL / READ-ONLY RESULT RECORDED

PM-02
NOT STARTED / NOT AUTHORIZED

NEXT
present explicit PM-02 mapping-design write gate only after PM-01 remote QA

HOST HOLD
must close before executable PM-04/05 benchmark execution

NO mapping/schema/harness/database write yet
NO technology selection
```
