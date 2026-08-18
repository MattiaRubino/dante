# PM-01 Technology Landscape and Candidate Freeze v1

- Status: **CURRENT — PM-01 READ-ONLY RESULT / PASS-CONDITIONAL**
- Workstream: `feature/physical-model`
- Research date: 2026-08-18
- Research PRE-SCOPE: `622767d5435d59766459bb25a57e5afeb7dd7336`
- Mapping execution: **NOT STARTED**
- Benchmark execution: **NOT STARTED**
- Technology selection: **NONE**
- Benchmark host freeze: **HOLD**

## 1. Purpose

Record the complete read-only PM-01 outcome before any Physical mapping, schema, harness, database deployment or technology selection is authorized.

PM-01 combines:

1. broad technology-family discovery;
2. candidate admission screening;
3. exact product/version/edition/deployment/client freeze where evidence is sufficient;
4. licensing/cost/operations/backup/evolution review;
5. public architecture reconnaissance from products with directly similar or structurally adjacent problems;
6. explicit unresolved environment conditions.

This record is **admission evidence**, not benchmark evidence.

```text
OFFICIAL CLAIM != EXECUTED PROOF
ADMIT != PASS HG-01..HG-12
ADMIT != PREFERRED
PREFERRED != SELECTED
```

## 2. Upstream authority preserved

PM-01 does not reopen Domain, Logical or Phase-10 semantics.

The admitted candidates must still preserve all applicable accepted distinctions, including:

- semantic owner versus implementation mechanism;
- `NativeRef`, `ScopedRecordRef`, `MaterialStateRef`, `ExternalRef`;
- canonical/material/derived/external/unresolved/runtime state separation;
- unknown/absence semantics;
- expected-state consequential concurrency;
- multi-owner consistency;
- material history/correction/reconciliation;
- Authority/Consent/Visibility/Representation separation;
- retention/redaction/tombstone/restore integrity;
- recurrence/timezone/DST meaning;
- provider/index/vector/runtime state not becoming canonical truth.

A product used successfully elsewhere is not allowed to weaken these invariants.

## 3. Discovery breadth

The read-only scan covered relevant families rather than only previously named products:

```text
relational / hybrid SQL
typed semantic / relation-centric
bitemporal / immutable-history relational
multimodel document+graph
system-versioned / application-time relational
distributed SQL
graph primary / graph projection
document stores
immutable/EAV-style systems
versioned-data databases
embedded/local stores
search/vector specialists
local-first / CRDT synchronization architectures
```

Discovery breadth is intentionally wider than benchmark breadth.

## 4. PM-01 primary admission result

| ID | Candidate | Frozen PM-01 subject | PM-01 disposition | Distinct hypothesis |
|---|---|---|---|---|
| P0 | PostgreSQL | PostgreSQL **18.4**, self-hosted single-node qualification topology; psycopg **3.3.4** | **ADMIT** | Explicit relational/hybrid model with highest operational maturity/control baseline |
| P1 | TypeDB | TypeDB **CE 3.12.3**, self-hosted single-node; official driver **3.12.3** | **ADMIT** | Strong typed entity/relation semantics may reduce mapping impedance |
| P2 | XTDB | XTDB **2.1.0**, self-hosted qualification subject through Postgres wire protocol | **ADMIT / PRODUCTION-TOPOLOGY HOLD** | Native bitemporal system-time + valid-time may fit LifeOS history/correction/knowledge chronology unusually well |
| P3 | SurrealDB | SurrealDB **Community 3.2.3**, self-hosted single-node **RocksDB**; Python SDK **2.0.0** | **ADMIT-CONDITIONAL** | Multimodel document/graph/relational capabilities may reduce bounded specialist-store pressure |

No row above is selected or preferred by PM-01.

## 5. P0 — PostgreSQL 18.4

### Frozen subject

```text
product       PostgreSQL
version       18.4
edition       community/open-source PostgreSQL distribution
qualification self-hosted single-node
Python client psycopg 3.3.4
selection     NONE
```

### Official evidence

- PostgreSQL 18.4 is the current minor release in the supported PostgreSQL 18 line as of this research date.
- PostgreSQL recommends running the current minor release for a supported major line.
- Major 18 is supported through November 2030.
- PostgreSQL uses the permissive PostgreSQL License.
- psycopg 3.3.4 is the current Psycopg 3 release captured for the Python qualification subject.

### PM-01 rationale

PostgreSQL remains the mandatory baseline because it provides a mature transactional relational substrate, mature backup/recovery/evolution tooling and a very broad Python/operations ecosystem without requiring a proprietary edition for the single-node qualification subject.

PM-02 must not rescue PostgreSQL by collapsing LifeOS into generic JSONB/property bags or a universal meta-model. Mapping complexity is evidence.

### PM-02/03 pressure

- explicit representation of the accepted identity/reference families;
- n-ary and consequence-sensitive relation representation without universal edge semantics;
- material state/history without universal event sourcing;
- expected-state and multi-owner transaction ergonomics;
- current-state performance without lifetime replay;
- schema evolution while retaining historical meaning.

## 6. P1 — TypeDB CE 3.12.3

### Frozen subject

```text
product       TypeDB
version       3.12.3
edition       Community Edition
qualification self-hosted single-node
Python client official typedb-driver 3.12.3
selection     NONE
```

### Official evidence

- TypeDB is available as a free/open-source Community Edition.
- The repository version captured for both TypeDB and its official driver is 3.12.3.
- The official Python driver is installed as `typedb-driver`.
- TypeDB transactions provide ACID guarantees up to **snapshot isolation**.
- Self-hosted backup implementation is the operator's responsibility; recommended disk snapshots and export/import are not incremental.
- TypeDB 3.x clustered operation is explicitly experimental/alpha and is documented as unsuitable for production today.
- Export/import is designed as a version-independent migration path across incompatible TypeDB data formats.

### PM-01 rationale

TypeDB remains a mandatory semantic challenger because first-class typed entities, relations and attributes may map significant parts of the closed Logical Model directly rather than emulating them through generic records.

### PM-02/03 pressure

The strongest concern is not expressiveness but consequential write semantics:

```text
snapshot isolation
vs
WL-H05 expected-state conflict detection
WL-H07 multi-owner consistency
```

PM-02 must prove the exact mechanisms rather than treating TypeDB's semantic expressiveness as sufficient evidence.

Cluster/HA cannot receive production-maturity credit from the current experimental 3.x cluster implementation.

## 7. P2 — XTDB 2.1.0

### Frozen subject

```text
product       XTDB
version       2.1.0 stable
edition       open-source distribution
qualification local/self-hosted qualification subject
client        Postgres wire protocol; PostgreSQL-compatible clients including psycopg are applicable
production topology
              HOLD — standalone Docker is explicitly non-production/non-distributed
selection     NONE
```

### Official evidence

- XTDB 2.1.0 is the latest stable release captured; 2.2.0-rc0 is a pre-release and is not the PM-01 benchmark subject.
- Every XTDB table is bitemporal.
- `SYSTEM_TIME` represents when information entered the system; `VALID_TIME` represents when data is considered valid in the application/world.
- DML transactions are non-interactive: they may contain DML and `ASSERT`, but cannot mix result-returning `SELECT` statements with DML in the same write transaction.
- DML writes are serialized through a totally ordered durable log and are described as serializable.
- The simple standalone Docker setup is explicitly described as non-production and non-distributed.

### PM-01 rationale

XTDB is the most materially new candidate discovered during PM-01 because its two temporal dimensions align closely enough with accepted LifeOS distinctions around effective/world time, knowledge chronology, correction and historical reconstruction to justify real PM-02 mapping work.

This apparent fit must not be assumed to be a win. The write/transaction model may impose unacceptable complexity on governed, consequential, multi-owner effects.

### PM-02/03 pressure

- `SYSTEM_TIME` must not be assumed equal to every LifeOS material-history concept;
- `VALID_TIME` must not swallow recurrence, planned/future state or all temporal semantics;
- `ASSERT`/non-interactive writes must preserve expected-state and multi-owner invariants ergonomically;
- production topology and its operational dependencies remain separate from the single-node qualification mapping;
- dynamic/sparse row support must not become a generic property-bag canonical kernel.

## 8. P3 — SurrealDB Community 3.2.3

### Frozen subject

```text
product       SurrealDB
version       3.2.3
edition       Community Edition
qualification self-hosted single-node
storage       RocksDB
Python SDK    2.0.0
selection     NONE
```

### Official evidence

- SurrealDB 3.2.3 is the latest stable patch in the 3.2 line captured for PM-01.
- The Python SDK 2.0.0 supports Python 3.10+ and documents compatibility through SurrealDB 3.2.3.
- SurrealDB transactions operate under snapshot isolation with write-write conflict detection on commit.
- RocksDB is the documented recommended engine for self-hosted single-node production.
- Distributed multi-node SurrealDS is a Cloud Scale / self-hosted Enterprise topology rather than the Community single-node qualification subject.
- The Community license/cost boundary must remain visible in later TCO/exit analysis; PM-01 does not treat Community availability as proof that all future HA capability is zero-cost.

### PM-01 rationale

SurrealDB earns PM-02 admission because it represents a genuinely different physical hypothesis: records/documents, graph relationships, permissions/query facilities and multiple storage/deployment modes in one engine may remove some need for extra specialist stores.

### PM-02/03 pressure

- multimodel flexibility must not recreate the rejected universal Thing/edge/property-bag model;
- snapshot isolation must be tested against expected-state and multi-owner consequential writes;
- field/table permission machinery must remain technical enforcement rather than Domain governance authority;
- Enterprise/HA capability cannot be credited to the Community single-node subject;
- any embedded/local capability is a separate future role, not evidence that the server canonical role is solved.

## 9. Deferred / reserve candidates

| Candidate/family | PM-01 disposition | Rationale |
|---|---|---|
| MariaDB 11.8 LTS | **DEFER — first reserve** | Real system-versioned + application-time/bitemporal capability is relevant, but overlaps heavily with the relational lane and carries important history/schema-evolution caveats that must justify a fifth primary mapping before admission |
| Gel 7 | **DEFER** | Strong schema/query/migration ideas, but current service-continuity/operational context creates enough uncertainty that it does not displace the four admitted hypotheses |
| CockroachDB | **DEFER** | Reopen if distributed SQL, geographic availability or multi-region requirements become real rather than hypothetical |
| YugabyteDB | **DEFER** | Same: structural value is mainly distributed SQL/HA rather than a distinct current semantic hypothesis |
| Neo4j | **DEFER → PM-08 G lane** | Serious graph/read-projection challenger; not admitted as canonical primary merely because graph traversal is convenient |
| pgvector | **DEFER → PM-08 S lane** | Registered bounded vector candidate if PostgreSQL remains applicable |
| Qdrant / OpenSearch | **DEFER → specialist trigger only** | Separate infrastructure requires a measured retrieval/search gap or structural benefit |
| SQLite | **DEFER → local/offline/client role** | Very strong bounded local-store candidate; not the current server canonical primary subject |

## 10. Rejected from the current primary benchmark

The following are not global product rejections. They are rejected from the **current canonical-primary PM-02 benchmark** because they either add insufficiently distinct information versus admitted candidates or conflict with an accepted structural direction.

| Candidate | PM-01 disposition | Primary reason |
|---|---|---|
| MongoDB | **REJECT-FROM-BENCHMARK primary** | Document flexibility does not currently justify a separate canonical-primary mapping beyond the admitted multimodel and relational hypotheses |
| ArangoDB | **REJECT-FROM-BENCHMARK primary** | Multimodel proposition overlaps the SurrealDB hypothesis without enough distinct LifeOS value to justify another primary mapping now |
| Dgraph | **REJECT-FROM-BENCHMARK primary** | Graph-centric value belongs in the bounded graph lane; Neo4j already supplies the registered serious graph challenger |
| FoundationDB | **REJECT-FROM-BENCHMARK primary** | Key-value substrate is too low-level for the current canonical mapping objective and would transfer excessive semantic machinery to LifeOS application code |
| Datomic | **REJECT-FROM-BENCHMARK primary** | Strong history ideas, but its generic entity/attribute/value orientation conflicts too directly with the closed rejection of a canonical generic EAV/meta-model root |
| Dolt / Doltgres | **REJECT-FROM-BENCHMARK primary** | Git-like data versioning/branching is not equivalent to LifeOS material history, correction and knowledge chronology |

A rejected candidate can be reopened only by new evidence or a new requirement that materially changes its value proposition.

## 11. Cost / licensing posture

The current PM-01 qualification topologies do **not** require buying a database license before mapping/benchmark qualification.

```text
P0 PostgreSQL       zero direct license cost for qualification
P1 TypeDB CE        zero direct license cost for qualification
P2 XTDB             zero direct license cost for qualification
P3 SurrealDB CE     zero direct license cost for the admitted Community qualification subject
```

This does not mean future production TCO is zero.

Potential future costs include:

- compute/storage/backup infrastructure;
- managed service premiums;
- HA/distributed topology dependencies;
- operational labor and observability;
- proprietary/Enterprise capability where a winning candidate requires it.

If a paid topology later becomes materially superior or required, it remains eligible and must be compared explicitly rather than silently discarded.

## 12. Application architecture reconnaissance

### Rule

Public architecture choices in other products are **supporting evidence only**.

```text
USED BY A SUCCESSFUL PRODUCT != CORRECT FOR LIFEOS
POPULAR TECHNOLOGY != SELECTED
```

The purpose is to learn from comparable structural problems: personal knowledge, task/project state, offline/local state, synchronization, history, recovery, scheduling, media/personal archives, AI/search projections and bounded specialist infrastructure.

### 12.1 Notion — knowledge/productivity at large scale

Public engineering material shows:

- PostgreSQL remained the online source-of-truth foundation while Notion grew from a single large database into a sharded fleet;
- sharding was delayed until concrete scale/maintenance pressure justified its complexity;
- workspace-local partitioning was chosen to preserve locality and transactionality;
- direct naive double-writes were considered too inconsistency-prone for critical datastore migration;
- offline/client acceleration evolved through SQLite local storage;
- modern offline operation required stronger local persistence and conflict-resolution semantics;
- offline analytics/ML workloads were separated from the online Postgres authority through a dedicated data-lake pipeline.

**LifeOS lesson:** mature PostgreSQL can scale far beyond our present qualification needs, but that does not prove semantic fit. More importantly, do not prepay distributed complexity. Local client storage and analytical/derived infrastructure can remain bounded roles rather than forcing the canonical store to do everything.

**Caution:** Notion's universal `block` model is not a LifeOS precedent to copy. LifeOS explicitly rejected a universal Thing/Entity/meta-root as canonical semantics.

### 12.2 Linear — task/project state, realtime sync and recovery

Public Linear engineering/postmortem material shows:

- PostgreSQL is the canonical production database behind a local-client-cache and sync-engine architecture;
- direct database mutation during the 2024 incident bypassed sync-packet application logic, leaving caches/clients temporarily inconsistent with canonical storage;
- nominal recovery capability and actually rehearsed recovery are different: the incident emphasizes why tested restore paths matter;
- Linear evaluated dedicated vector databases and selected PostgreSQL + pgvector after finding cost/operations/scaling drawbacks in specialist options;
- Linear's access-control incident in 2026 also demonstrates that projection/query filtering can become a disclosure boundary and must not be treated casually.

**LifeOS lesson:** canonical writes must preserve governed mutation/effect semantics and projection propagation. PM-07 must test recovery, not merely cite product backup features. Search/vector specialization should prove net benefit over a bounded Postgres extension when PostgreSQL is present.

### 12.3 Anytype / any-sync — local-first personal knowledge and collaboration

Public any-sync documentation shows:

- local-first operation with the primary copy of a space on user devices;
- background multi-device synchronization using CRDTs;
- offline operation and optional network connectivity;
- encrypted/signed change history and creator-controlled keys;
- explicit sync/file/consensus/coordinator infrastructure roles.

**LifeOS lesson:** offline/local-first is a genuine architecture dimension, but a sync protocol is not a canonical database recommendation. If LifeOS later requires offline multi-writer operation, local state, sync coordination, conflict convergence, encryption and server canonical authority must be designed as explicit roles instead of collapsed into one database choice.

### 12.4 AppFlowy — open-source collaborative productivity stack

The current public self-host compose shows a composable stack including:

```text
PostgreSQL + pgvector
Redis
MinIO/S3-compatible object storage
application/auth/worker/search/AI services
```

**LifeOS lesson:** a general canonical relational store can coexist with bounded queue/cache, object-storage and vector/search mechanisms. That pattern supports our existing rule that specialist infrastructure must justify itself and must not become canonical truth merely because it serves a feature.

### 12.5 Immich — personal digital archive, jobs and machine learning

Immich's public architecture separates:

```text
PostgreSQL     persistent metadata/access/sharing authority
filesystem     media assets
Redis/BullMQ   background job queue
ML service     derived machine-learning work
```

Its machine-learning service is separately deployable/disableable rather than embedded into canonical persistence.

**LifeOS lesson:** canonical user state, large binary/file storage, runtime jobs and derived AI work benefit from explicit boundaries. This is strong supporting evidence for the existing LifeOS state-layer and provider/runtime separation, not evidence that we should copy Immich's exact stack.

### 12.6 Home Assistant Recorder — history and database portability caution

Home Assistant publicly supports SQLite, MariaDB, MySQL and PostgreSQL through SQLAlchemy, but its own documentation warns that behavior/features differ among engines and database migration is not supported.

**LifeOS lesson:** an ORM abstraction does not make databases semantically interchangeable and does not create a real migration strategy. This directly supports the Physical rule:

```text
no lowest-common-denominator portability abstraction
candidate-native where materially better
migration evidence must be real
```

It also shows that SQLite can be the right bounded/default answer under suitable local workloads, which is why SQLite remains relevant for a future local/offline lane even though it is not the current server primary challenger.

### 12.7 Cal.com — scheduling and schema evolution

Cal.com's self-host documentation requires explicit Prisma migrations and warns that careless schema changes can damage/delete production data.

**LifeOS lesson:** scheduling software does not remove the need for deliberate schema evolution. Physical migration/evolution evidence must be reproducible and reviewed rather than trusting automatic schema synchronization.

## 13. Cross-application structural findings

The reconnaissance produces the following evidence-backed structural pressures for LifeOS:

### A. Do not introduce distributed topology early

Notion's history is a concrete example of staying on PostgreSQL until actual scale forced sharding. Distributed SQL/HA candidates therefore remain reserves until LifeOS requirements make their benefit real.

### B. Separate canonical state from local/offline state

Notion and Anytype independently show the value of local storage/sync, but through very different designs. This argues for an explicit future client/offline lane, not for changing the server canonical candidate by assumption.

### C. Sync/cache/projection state is not canonical truth

Linear demonstrates the operational danger directly: mutating the database outside the application sync path can leave caches and clients inconsistent.

### D. Rehearsed recovery outranks feature-list recovery

Linear's incident supports the existing PM-07 requirement for destructive restore and semantic verification. `PITR supported` or `backup exists` is not closure evidence.

### E. Bounded specialization is a real industry pattern

Linear, AppFlowy and Immich show variants of keeping a mature canonical store while introducing pgvector, Redis/jobs, object storage or ML only for bounded responsibilities.

### F. Generic portability is often fake portability

Home Assistant explicitly documents different behavior across SQLAlchemy-supported databases and no supported migration between them. LifeOS should preserve cheap portability where useful but not force each candidate into the same lowest-common-denominator schema.

### G. Flexible universal roots are not automatically a virtue

Notion's universal block model works for Notion, but directly illustrates why successful product architecture cannot be imported without checking semantic fit. LifeOS's closed Logical Model remains authority.

## 14. Evidence effect on candidate admission

Application reconnaissance does **not** select PostgreSQL.

It changes PM-01 evidence in narrower ways:

- strengthens confidence that PostgreSQL is a credible operational baseline rather than only a familiar default;
- strengthens the case for keeping pgvector/search specialization bounded until a measured gap exists;
- strengthens the case for a future local SQLite/offline/sync lane separate from server canonical persistence;
- strengthens PM-07 recovery/rehearsal requirements;
- strengthens projection/disclosure/non-interference testing;
- does not remove the need to benchmark TypeDB, XTDB or SurrealDB against LifeOS semantics;
- does not authorize CRDT/local-first semantics that the Product/Domain requirements have not yet required.

## 15. Benchmark environment freeze

The only material PM-01 freeze item still unresolved is the exact benchmark host/runtime.

```text
CPU / RAM available to benchmark      HOLD
OS/runtime exact build                HOLD
Docker/native execution availability  HOLD
filesystem/storage details            HOLD
available disk budget                 HOLD
network/topology constraints          HOLD
resource-limit policy                 HOLD
```

Do not invent these values from a remembered workstation profile or conversation context. They must be measured/verified on the actual execution host before executable benchmark evidence begins.

This HOLD does not authorize different hosts per candidate. Comparability requires the execution environment to be frozen before PM-04/05 execution.

## 16. PM-01 final disposition

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

P0 PostgreSQL 18.4    ADMIT
P1 TypeDB CE 3.12.3  ADMIT
P2 XTDB 2.1.0        ADMIT / production topology HOLD
P3 SurrealDB CE 3.2.3
                      ADMIT-CONDITIONAL

MAPPING
NOT STARTED

BENCHMARK
NOT STARTED

PREFERRED
PostgreSQL retains only its pre-existing preferred-baseline label

SELECTED
NONE
```

PM-02 may be proposed as a separate explicit mapping write gate. The benchmark-host HOLD must be closed before executable benchmark/harness execution claims.

## 17. Official primary-source inventory

### PostgreSQL / Psycopg

- https://www.postgresql.org/docs/release/18.4/
- https://www.postgresql.org/support/versioning/
- https://www.postgresql.org/about/licence/
- https://www.psycopg.org/download/

### TypeDB

- https://typedb.com/docs/home/what-is-typedb/
- https://typedb.com/docs/home/install/ce/
- https://typedb.com/docs/home/install/drivers/
- https://typedb.com/docs/core-concepts/typedb/transactions/
- https://typedb.com/docs/maintenance-operation/typedb-backups/
- https://typedb.com/docs/maintenance-operation/database-export-import/
- https://typedb.com/docs/reference/typedb-cluster/
- repository version evidence: TypeDB server `VERSION=3.12.3`; TypeDB driver `VERSION=3.12.3`

### XTDB

- https://github.com/xtdb/xtdb/releases
- https://docs.xtdb.com/about/time-in-xtdb.html
- https://docs.xtdb.com/about/txs-in-xtdb.html
- https://docs.xtdb.com/intro/installation-via-docker.html
- https://docs.xtdb.com/intro/what-is-xtdb.html

### SurrealDB

- https://surrealdb.com/releases/3.2
- https://surrealdb.com/docs/architecture
- https://surrealdb.com/docs/build/deployment
- https://surrealdb.com/docs/reference/python
- https://surrealdb.com/docs/reference/query-language/language-primitives/transactions

### Application architecture reconnaissance

- Notion: https://www.notion.com/blog/sharding-postgres-at-notion
- Notion: https://www.notion.com/blog/the-great-re-shard
- Notion: https://www.notion.com/blog/data-model-behind-notion
- Notion: https://www.notion.com/blog/how-we-made-notion-available-offline
- Notion: https://www.notion.com/blog/building-and-scaling-notions-data-lake
- Linear: https://linear.app/now/linear-incident-on-jan-24th-2024
- Linear: https://linear.app/now/using-ai-to-detect-similar-issues
- Linear: https://linear.app/now/linear-incident-on-mar-24th-2026
- Anytype/any-sync: https://tech.anytype.io/any-sync/overview
- AppFlowy Cloud: https://github.com/AppFlowy-IO/AppFlowy-Cloud/blob/main/docker-compose.yml
- Immich: https://immich.app/docs/developer/architecture
- Home Assistant Recorder: https://www.home-assistant.io/integrations/recorder/
- Cal.com: https://cal.com/docs/self-hosting/database-migrations

## 18. Non-authorizations

This PM-01 record does not authorize:

```text
Physical candidate mapping files
SQL / TypeQL / SurrealQL / XTDB SQL schema implementation
benchmark harness
fixture generator
database/container deployment
performance execution
hard-gate PASS claims
primary or secondary selection
backend/API/Auth/provider implementation
main write / PR / merge
```
