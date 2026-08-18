# Physical Model Result Register v1

- Status: **CURRENT — PM-02 DESIGN COMPLETE / PM-03 NOT RUN**
- Workstream: `feature/physical-model`
- PM-01: **PASS-CONDITIONAL**
- PM-02: **DESIGN COMPLETE**
- Benchmark execution: **NOT STARTED**
- Technology selection: **NONE**
- Every hard-gate/executable candidate result remains `NOT RUN`.
- PM-01 evidence: `pm-01-technology-landscape-v1.md`
- PM-02 evidence: `pm-02-primary-mapping-overview-v1.md` + `mappings/*.md`

## Rule

This file records current Physical disposition/execution state. It does not override Domain/Logical authority, the Phase-10 benchmark method, or create selection by prose.

```text
OFFICIAL CLAIM != EXECUTED PROOF
ADMIT != HARD-GATE PASS
MAPPING DESIGNED != HARD-GATE PASS
NOT RUN != PASS
PREFERRED != SELECTED
```

A hard-gate/benchmark result changes only after evidence is remotely written/linked and the corresponding gate is QA-verified.

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

SELECTED
NONE
```

The host HOLD must close before executable benchmark evidence; it does not block static mapping/hard-gate design review.

# PM-02 status

```text
PM-02 PRE-SCOPE
fac3b5baf1813f886c4773594e6234810e5ba8c6

P0 PostgreSQL mapping
PM02-PG-001
DESIGN COMPLETE

P1 TypeDB mapping
PM02-TDB-001
DESIGN COMPLETE

P2 XTDB mapping
PM02-XT-001
DESIGN COMPLETE

P3 SurrealDB mapping
PM02-SDB-001
DESIGN COMPLETE

HG-01..HG-12
NOT RUN

EXECUTABLE SCHEMA / DATABASE
NOT STARTED

BENCHMARK
NOT STARTED

SELECTION
NONE
```

The mappings are candidate-native designs against the same semantic oracle. PM-03 must challenge them before any benchmark harness/database deployment proceeds.

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
PM02-PG-001
docs/physical-model/mappings/postgresql-18.4-v1.md
DESIGN COMPLETE

MAPPING THESIS
owner-specific relational tables
+ direct FKs for homogeneous references
+ bounded technical address/state anchors for heterogeneous addressability
+ explicit material-state/history records
+ transaction/locking/SERIALIZABLE hardening where required

HG-01..HG-12
NOT RUN

CORRECTNESS / DESTRUCTIVE
NOT RUN

LOW / BASE / HIGH
NOT RUN

RECOVERY / EVOLUTION
NOT RUN

WEIGHTED SCORE
NOT RUN

SENSITIVITY
NOT RUN

CURRENT DISPOSITION
ADMIT / PRE-EXISTING PREFERRED-BASELINE / NOT SELECTED
```

PM-03 pressure:

- technical anchors must not become universal Entity/Thing;
- heterogeneous Reference Contracts must reject wrong-family/dangling targets;
- expected-state and multi-owner concurrent operations must be proven;
- owner-specific history must remain manageable without generic-state fallback;
- selective disclosure/non-interference and tombstone/restore integrity remain unproven.

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
PM02-TDB-001
docs/physical-model/mappings/typedb-3.12.3-v1.md
DESIGN COMPLETE

MAPPING THESIS
concrete entity types for native owners
+ first-class specific relation types/named roles
+ role eligibility as Reference Contract enforcement
+ explicit owner-specific material-state objects
+ narrow technical consistency guards for write-skew-sensitive invariant sets

HG-01..HG-12
NOT RUN

CORRECTNESS / DESTRUCTIVE
NOT RUN

LOW / BASE / HIGH
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

PM-03 pressure:

- shared type/interface machinery must not become generic ontology;
- TypeDB IID/snapshot cannot become NativeRef/MaterialStateRef;
- explicit material history and reverse mapping must remain practical;
- snapshot-isolation write-skew must be closed by exact-state + bounded consistency-guard design where applicable;
- n-ary Agreement, deletion/tombstone and selective-disclosure inference remain unproven.

## P2 — XTDB

```text
REGISTERED ROLE
PM-01-admitted temporal/bitemporal primary challenger

PM-01 DISPOSITION
ADMIT / PRODUCTION-TOPOLOGY HOLD

EXACT SUBJECT
XTDB 2.1.0
self-hosted qualification subject
Postgres-wire compatible client path

MAPPING
PM02-XT-001
docs/physical-model/mappings/xtdb-2.1.0-v1.md
DESIGN COMPLETE

MAPPING THESIS
owner-specific tables
+ four separated technical address spaces
+ explicit MaterialStateRef records
+ native bitemporal history only where semantically truthful
+ ASSERT-based reference/expected-state enforcement
+ one serialized non-interactive DML transaction for co-located multi-owner effects

HG-01..HG-12
NOT RUN

CORRECTNESS / DESTRUCTIVE
NOT RUN

LOW / BASE / HIGH
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

PM-03 pressure:

- absent native FK/general uniqueness requires explicit integrity proof;
- address anchors must stay technical and segregated;
- system/valid time and transaction tokens must remain distinct from MaterialStateRef;
- bitemporal axes must match semantic chronology only where truthful;
- non-interactive DML + ASSERT must express representative governed operations cleanly;
- dynamic schema must not become semantic drift;
- production topology remains HOLD and gets no HA credit.

## P3 — SurrealDB

```text
REGISTERED ROLE
PM-01-admitted multimodel primary challenger

PM-01 DISPOSITION
ADMIT-CONDITIONAL

EXACT SUBJECT
SurrealDB Community 3.2.3
single-node RocksDB qualification topology
Python SDK 2.0.0

MAPPING
PM02-SDB-001
docs/physical-model/mappings/surrealdb-3.2.3-v1.md
DESIGN COMPLETE

MAPPING THESIS
SCHEMAFULL owner-specific tables
+ typed record links
+ specific binary relation tables only where semantics are truly binary
+ contextual records for n-ary/material relations
+ explicit material-state history
+ narrow technical consistency guards for write-skew-sensitive invariant sets

HG-01..HG-12
NOT RUN

CORRECTNESS / DESTRUCTIVE
NOT RUN

LOW / BASE / HIGH
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

PM-03 pressure:

- SCHEMAFULL/typed records must prevent document/meta-model fallback;
- graph edge machinery must not become universal Relationship ontology;
- n-ary Agreement must remain contextual/common-ground structure;
- explicit MaterialStateRef/history must not depend on changefeed/version metadata;
- snapshot-isolation write-skew must be closed by expected-state + consistency guard;
- deletion/edge behavior and selective-disclosure traversal leakage remain unproven;
- Community subject receives no Enterprise/SurrealDS HA credit.

# Cross-candidate PM-02 mapping comparison

| Concern | PostgreSQL | TypeDB | XTDB | SurrealDB |
|---|---|---|---|---|
| Native owners | concrete relational tables | concrete entity types | concrete owner tables | concrete SCHEMAFULL tables |
| Heterogeneous refs | bounded technical anchors | role eligibility + explicit key family | four separated address tables + ASSERT | typed record unions/links; bounded anchor if needed |
| Specific binary relations | specific association tables | relation types/named roles | specific relation tables | typed links or specific relation tables |
| N-ary/material relations | contextual record + role rows | native n-ary relation/context | contextual record + role rows | contextual record + participant rows/links |
| MaterialStateRef | explicit state anchor/rows | explicit state objects + key | explicit state rows; bitemporal substrate separate | explicit state records |
| History | explicit owner material history | explicit state/lineage objects | native bitemporal + semantic state records | explicit state history; changefeed bounded only |
| Expected state | current state + tx/lock | state match + guard where needed | ASSERT | conditional state + guard where needed |
| Multi-owner | one tx; SERIALIZABLE/locks as needed | one write tx + bounded guard | one serialized DML tx | one tx + bounded guard |
| Primary design risk | anchor/history complexity | snapshot isolation/history verbosity | missing FK/schema/non-interactive DML | write-skew/graph+document escape hatch |

No column is a score or recommendation.

# Common material-state rule

```text
PostgreSQL xmin/xid       != MaterialStateRef
TypeDB IID/transaction    != MaterialStateRef
XTDB system/valid time    != MaterialStateRef
SurrealDB change metadata != MaterialStateRef
```

Every candidate uses an explicit stable material-state address where consequential semantic binding requires it.

# Common lazy-Occurrence rule

```text
before persistent differentiation
source + governing MaterialStateRef + recurrence family + semantic coordinate where available
= bounded occurrence locator

when individually distinguished/addressable
-> same semantic Occurrence receives NativeRef
```

No candidate may manufacture arbitrary IDs for indistinguishable quota slots simply for storage convenience.

# Common expected-state / multi-owner rule

A consequential operation must:

1. bind/check expected semantic material state;
2. reject stale mismatch;
3. enforce all-or-nothing co-located invariant changes;
4. expose staged/partial/reconciliation state where external atomicity is impossible;
5. keep storage/transaction tokens separate from semantic MaterialStateRef.

Candidate-specific enforcement remains PM-03 proof obligation.

# Primary reserves / non-admitted current candidates

| Candidate | PM-01 disposition | Current reason |
|---|---|---|
| MariaDB 11.8 LTS | DEFER — first reserve | Relevant temporal capability, but strong relational-lane overlap plus history/evolution caveats; must justify fifth mapping |
| Gel 7 | DEFER | Interesting schema/query/migration direction but current continuity/operational uncertainty does not displace admitted set |
| CockroachDB | DEFER | Reopen on real distributed/geographic HA requirement |
| YugabyteDB | DEFER | Reopen on real distributed/geographic HA requirement |
| MongoDB | REJECT-FROM-BENCHMARK primary | No sufficiently distinct canonical-primary hypothesis |
| ArangoDB | REJECT-FROM-BENCHMARK primary | Multimodel hypothesis overlaps P3 without enough distinct value now |
| Dgraph | REJECT-FROM-BENCHMARK primary | Graph specialization belongs in bounded G lane |
| FoundationDB | REJECT-FROM-BENCHMARK primary | Too low-level for current canonical mapping objective |
| Datomic | REJECT-FROM-BENCHMARK primary | Generic entity/attribute/value orientation conflicts with generic-EAV/meta-model rejection |
| Dolt / Doltgres | REJECT-FROM-BENCHMARK primary | Git-like versioning is not LifeOS material history/correction/knowledge chronology |

`REJECT-FROM-BENCHMARK` is scoped to the current primary benchmark and remains reopenable by materially new requirements/evidence.

# Lane G — Secondary graph / traversal

```text
G0 no specialized graph store
BASELINE / NOT RUN

G1 Neo4j
DEFER TO PM-08
EXACT SUBJECT NOT FROZEN
CG-01..CG-04 NOT RUN
NOT SELECTED
```

No graph product becomes canonical truth by winning traversal performance.

# Lane S — Search / semantic retrieval

```text
S0 structured + lexical/full-text baseline
BASELINE / NOT RUN

S1 pgvector
DEFER TO PM-08 when PostgreSQL survives/applicable
NOT FROZEN
CG-01..CG-04 NOT RUN
NOT SELECTED

Qdrant / OpenSearch
DEFER — specialist trigger required
```

Vector/search quality is judged after scope/Visibility filtering and propagation correctness, not unfiltered top-k latency.

# Local / offline bounded lane

```text
SQLite
DEFER — future local/offline/client role
NOT current canonical server primary
```

Application reconnaissance supports keeping local/offline/sync as an explicit later architecture dimension without selecting CRDT/offline multi-master semantics today.

# Lane E/D — bounded event/document mechanisms

```text
ED0 bounded native mechanisms
BASELINE CLASS
NOT RUN

ED-SPECIALIZED
NONE ADMITTED
```

A named specialist requires a future bounded admission trigger.

# Durable-runtime coupling

No durable runtime is selected by the Physical workstream.

```text
Restate   NOT SELECTED
Temporal  NOT SELECTED
DBOS      NOT SELECTED
```

Runtime coupling/cost may become Physical evidence, but runtime preference cannot select primary persistence.

# Solver / AI / provider interaction

```text
solver output != accepted canonical effect
AI eval/result != canonical LifeOS truth
provider revision != MaterialStateRef
runtime workflow completion != Actual automatically
```

No model/provider/solver/runtime product is selected here.

# Evidence checkpoints

## PM-00 Bootstrap

```text
PRE-SCOPE
main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79

CREATE CHECKPOINT
6d76bc150dfd7b3cefe56c6e05c96404e7494626

CONTENT-QA CHECKPOINT
8549e1c95bef2e354bd47028259e6816bf5e9272

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
```

## PM-02 Primary mapping design

```text
PRE-SCOPE
fac3b5baf1813f886c4773594e6234810e5ba8c6

EVIDENCE
pm-02-primary-mapping-overview-v1.md
mappings/postgresql-18.4-v1.md
mappings/typedb-3.12.3-v1.md
mappings/xtdb-2.1.0-v1.md
mappings/surrealdb-3.2.3-v1.md

STATUS
DESIGN COMPLETE

HG-01..HG-12
NOT RUN

BENCHMARK
NOT STARTED

SELECTION
NONE
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
BENCHMARK HOST HOLD MUST CLOSE FIRST
```

## PM-05+ Execution

```text
STATUS
NOT STARTED
```

# Recommendation ledger

| Lane | Candidate | Exact subject | Admission | Mapping | Hard-gate result | Score | Selected? |
|---|---|---|---|---|---|---|---|
| P | PostgreSQL | 18.4 / self-host / psycopg 3.3.4 | ADMIT | PM02-PG-001 COMPLETE | NOT RUN | NOT RUN | NO |
| P | TypeDB | CE 3.12.3 / self-host / driver 3.12.3 | ADMIT | PM02-TDB-001 COMPLETE | NOT RUN | NOT RUN | NO |
| P | XTDB | 2.1.0 / qualification subject | ADMIT / topology HOLD | PM02-XT-001 COMPLETE | NOT RUN | NOT RUN | NO |
| P | SurrealDB | CE 3.2.3 / single-node RocksDB / SDK 2.0.0 | ADMIT-CONDITIONAL | PM02-SDB-001 COMPLETE | NOT RUN | NOT RUN | NO |
| G | G0 | future primary-dependent | BASELINE | future | NOT RUN | NOT RUN | NO |
| G | Neo4j | NOT FROZEN | DEFER PM-08 | NOT STARTED | NOT RUN | NOT RUN | NO |
| S | S0 | future primary-dependent | BASELINE | future | NOT RUN | NOT RUN | NO |
| S | pgvector | conditional / NOT FROZEN | DEFER PM-08 | NOT STARTED | NOT RUN | NOT RUN | NO |
| E/D | bounded native | future primary/runtime-dependent | BASELINE CLASS | future | applicable checks NOT RUN | N/A | NO |

# Result mutation protocol

Before changing any candidate hard-gate/execution result from `NOT RUN`:

1. identify exact evidence record/path/artifact;
2. verify candidate subject/version/edition/topology;
3. verify mapping revision and scenario/contract;
4. update only applicable result fields;
5. preserve unresolved items as `HOLD`/`NOT RUN` rather than inferring completion;
6. remote-read back the register;
7. record checkpoint in `docs/workstreams/physical-model.md`.

Before writing a new `PREFERRED`, PM-09/10 evidence must exist.

Before writing `SELECTED`, PM-11 explicit selection gate and user approval are mandatory.

# Current next step

```text
PM-02
DESIGN COMPLETE / FINAL REMOTE QA REQUIRED

PM-03
NEXT
semantic mapping hard-gate preflight

BENCHMARK HOST HOLD
must close before executable PM-04/05 benchmark evidence

NO technology selection
NO production backend
```