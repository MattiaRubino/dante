# PM-08 Secondary / Specialist Lane Qualification v1

- Status: **PM-08 COMPLETE — EVIDENCE-FIRST / NO DIRECT EXECUTION**
- Workstream: `feature/physical-model`
- PRE-SCOPE: `1e19793fdb9f51ba510f00ac4c927a6907e28c4b`
- Primary finalists entering PM-08: **PostgreSQL 18.4 / TypeDB CE 3.12.3**
- Preferred primary: **NONE**
- Selected primary: **NONE**
- Local/server specialist execution: **NOT RUN / NOT REQUIRED BY PM-08**

## Purpose

Determine which secondary technologies, if any, add enough bounded LifeOS value to justify another engine, service, persistence surface, recovery path and projection/reconciliation obligation.

PM-08 does not choose the primary. It evaluates specialist lanes under the rule:

```text
EXTRA TECHNOLOGY
must create material net value
>
complexity + operations + security + recovery + freshness + deletion propagation cost
```

No specialist may compensate for a weakness in canonical correctness.

## Result summary

```text
GRAPH
G0 primary-store baseline            ADVANCE
Neo4j                                DEFER / NOT REJECTED
initial graph specialist             NO

SEARCH / VECTOR
PostgreSQL native FTS                ADVANCE as P0 baseline
pgvector 0.8.6                       ADMIT-CONDITIONAL when PostgreSQL primary + vector need exists
Qdrant 1.18.2                        DEFER / SPECIALIST TRIGGER ONLY
OpenSearch 3.7                       DEFER / SPECIALIST TRIGGER ONLY

LOCAL / OFFLINE
SQLite 3.53.4                        ADMIT as bounded local/offline candidate
canonical authority                  NO

OBJECT / BLOB
new engine admission                 NO
status                               DEFER / TRIGGER ONLY

DIRECT EXECUTION
0 execution-worthy PM-08 gaps
```

## Architectural conclusion

If PostgreSQL becomes primary, the minimum credible initial server stack is:

```text
PostgreSQL 18.4
canonical truth
+ native full-text search
+ pgvector 0.8.6 only when semantic/vector retrieval is actually required

SQLite 3.53.4
bounded client/local/offline state where required

NO initial Neo4j
NO initial Qdrant
NO initial OpenSearch
```

If TypeDB becomes primary, its semantic relationship strength remains real, but search/vector specialization is more likely to require an external projection/service. That additional topology/operations burden is a PM-09 comparison input, not an automatic TypeDB rejection.

## Lane principles

### Secondary truth rule

```text
canonical primary
=
authoritative LifeOS state

secondary/search/vector/graph/local state
=
bounded state with explicit authority, freshness and reconciliation semantics
```

A projection never becomes canonical merely because a query is faster there.

### Rebuildability rule

Where a secondary dataset is derived from canonical truth, its accepted architecture must define:

```text
source material/basis
projection revision
freshness/lag observability
delete/redaction propagation
Visibility/scope propagation
rebuild/reconciliation path
failure/degraded behavior
```

### Local/offline rule

Local state can contain cached material, local drafts, pending mutations and device-local projection, but:

```text
LOCAL != CANONICAL
OFFLINE != CURRENT SERVER TRUTH
SYNC SUCCESS != SEMANTIC ACCEPTANCE
LAST WRITE WINS != DEFAULT LIFEOS CONFLICT POLICY
```

## Graph lane result

PostgreSQL 18 already provides recursive CTE traversal plus `SEARCH` breadth/depth ordering and `CYCLE` detection. TypeDB already provides a relationship-native semantic query model.

Neo4j remains a strong graph specialist, but PM-08 found no accepted LifeOS workload that currently justifies:

```text
canonical primary
+
second graph persistence
+
projection pipeline
+
freshness/deletion/Visibility propagation
+
second backup/operations surface
```

Neo4j Community is a single-instance product; clustering and online backup are Enterprise capabilities. This increases the initial complexity/cost burden of a production specialist lane.

Verdict:

```text
G0 PRIMARY-STORE BASELINE
ADVANCE

NEO4J
DEFER / NOT REJECTED
NO INITIAL ADMISSION
```

Reopen only if a concrete graph workload becomes decision-relevant, for example large/deep path traversal, graph recommendation/pathfinding or graph analytics whose quality/latency materially fails the primary baseline.

## Search / vector lane result

### PostgreSQL FTS baseline

PostgreSQL 18 has native full-text search with `tsvector`, `tsquery`, indexing, parsing and result ranking.

Verdict:

```text
POSTGRESQL FTS
ADVANCE AS PRIMARY-NATIVE LEXICAL BASELINE
```

### pgvector

Frozen PM-08 candidate:

```text
pgvector 0.8.6
PostgreSQL extension
PostgreSQL License
PostgreSQL 18 supported
```

It supports exact vector similarity plus HNSW/IVFFlat approximate indexing and remains inside the same PostgreSQL transactional/query boundary.

This is particularly valuable to LifeOS because structured scope/Visibility predicates and vector retrieval can remain in one database rather than requiring projection to another service.

However vector/embedding state remains derived state, never canonical identity/material state.

Filtered ANN quality remains a known sensitivity: the accepted search benchmark must judge recall/ranking after real scope/Visibility filtering. Iterative scans, partial indexes or partitioning are implementation levers, not semantic waivers.

Verdict:

```text
PGVECTOR 0.8.6
ADMIT-CONDITIONAL

CONDITIONS
PostgreSQL is selected primary
AND
an accepted semantic/vector retrieval requirement exists

INITIAL DEDICATED VECTOR SERVICE
NOT REQUIRED
```

### Qdrant

Frozen PM-08 evidence subject:

```text
Qdrant 1.18.2
Apache-2.0
```

Qdrant offers strong dense/sparse vector search, payload filtering, hybrid retrieval and multi-stage/reranking mechanisms. It is a credible future specialist.

It is not admitted to the initial stack because its present value does not yet exceed the additional service, persistence, backup, monitoring, security, projection, redaction and freshness burden versus PostgreSQL + pgvector.

Verdict:

```text
QDRANT 1.18.2
DEFER / NOT REJECTED
SPECIALIST TRIGGER ONLY
```

Reopen on a concrete condition such as very large vector corpus, filtered-ANN quality/scale failure in pgvector, independent vector scaling need, or vector/hybrid retrieval becoming a major product capability.

### OpenSearch

Frozen PM-08 evidence subject:

```text
OpenSearch 3.7
```

OpenSearch is a strong dedicated search/relevance/observability platform with full-text, vector and hybrid-search capabilities.

It is not admitted because LifeOS has no accepted requirement today that justifies another distributed/search service over PostgreSQL FTS + conditional pgvector.

Verdict:

```text
OPENSEARCH 3.7
DEFER / NOT REJECTED
SPECIALIST TRIGGER ONLY
```

Reopen on a concrete large-scale lexical/faceted/relevance/search-analytics requirement or when search isolation from canonical workload becomes materially necessary.

## TypeDB specialist implication

PM-08 does not find evidence sufficient to treat TypeDB CE as a replacement for a dedicated lexical/vector retrieval stack.

Therefore the likely topology if TypeDB wins is:

```text
TypeDB canonical primary
+
search/vector specialist when required
```

Qdrant is currently the most credible bounded trigger candidate for a combined semantic/vector/hybrid retrieval projection, but it is not selected or admitted now.

This probable extra server technology is a real PM-09 architecture/operations/cost input.

## Local / offline lane result

Frozen PM-08 candidate:

```text
SQLite 3.53.4
public domain
```

SQLite earns a bounded lane because it solves a problem distinct from canonical server persistence:

```text
device-local persistence
offline availability
local cache/projection
local drafts
pending-operation staging
sync/reconciliation support
```

SQLite provides WAL and FTS capabilities and official WASM/OPFS options for browser-class environments. Browser/WASM concurrency has important VFS/locking caveats, so PM-08 selects only the semantic role, not one universal client runtime/configuration.

Verdict:

```text
SQLITE 3.53.4
ADMIT
BOUNDED LOCAL/OFFLINE CANDIDATE

CANONICAL AUTHORITY
NO

EXACT MOBILE/WEB/DESKTOP ADAPTER
DEFER TO CLIENT IMPLEMENTATION DESIGN
```

## Object/blob lane

PM-08 found no already-accepted physical requirement specific enough to admit S3/R2/MinIO or another object engine now.

Content Artifact may later create such a need, but admission requires concrete evidence such as binary volume/object-size/distribution/retention/upload/security requirements.

Verdict:

```text
OBJECT/BLOB SPECIALIST
NO ADMISSION NOW
DEFER / TRIGGER ONLY
```

This is not a claim that PostgreSQL should store arbitrary large media forever. It is a refusal to select infrastructure before the requirement exists.

## Scenario disposition

```text
SC-017 search hidden-result non-interference
SYSTEM / SEARCH IMPLEMENTATION VALIDATION

SC-018 FTS mixed filter/query
POST-SELECTION SEARCH IMPLEMENTATION VALIDATION

SC-019 vector recall after security filter
REOPEN if vector path becomes selection/performance sensitive; otherwise implementation validation

SC-020 stale index source
POST-SELECTION PROJECTION VALIDATION when secondary projection exists

SC-021 deletion propagation
POST-SELECTION PROJECTION VALIDATION when secondary projection exists

SC-035 graph projection divergence/rebuild
NOT APPLICABLE initially because no graph specialist is admitted;
reopen if graph lane is later activated
```

None is a direct PASS.

## Execution admission

```text
PM-08 EXECUTION-WORTHY GAPS    0
PM-04B REOPENED                NO
LOCAL DATABASE TEST            NOT ADMITTED
GRAPH BENCHMARK                NOT ADMITTED
VECTOR BENCHMARK               NOT ADMITTED NOW
SEARCH BENCHMARK               NOT ADMITTED NOW
SQLITE BENCHMARK               NOT ADMITTED NOW
BENCHMARK HOST                 HOLD / DORMANT
```

## PM-09 carry-forward

PM-09 must score/sensitize the primary finalists with the specialist implications included.

Key pressure:

```text
POSTGRESQL PATH
canonical + lexical search can remain in PostgreSQL
vector can likely remain bounded in PostgreSQL through pgvector
fewer server technologies initially

TYPEDB PATH
semantic relation model remains superior
but search/vector likely requires another service when those capabilities become required
```

This is an architecture/TCO/operability difference, not a semantic hard-gate failure.

## Source ledger

Primary sources reviewed include:

- PostgreSQL 18 recursive CTE / SEARCH / CYCLE documentation;
- PostgreSQL 18 Full Text Search documentation;
- pgvector changelog/repository documentation for 0.8.6 and PostgreSQL 18 support;
- Neo4j Operations Manual edition boundaries;
- Qdrant documentation/repository for 1.18.2, filtering and hybrid search;
- OpenSearch 3.7 release documentation;
- SQLite 3.53.4 release history and WASM/OPFS persistence documentation.

## Closure

```text
PM-08
COMPLETE subject to remote QA

INITIAL GRAPH SPECIALIST
NONE

POSTGRESQL SEARCH BASELINE
NATIVE FTS

PGVECTOR
ADMIT-CONDITIONAL

QDRANT / OPENSEARCH / NEO4J
DEFER / NOT REJECTED / TRIGGER ONLY

SQLITE
ADMIT BOUNDED LOCAL/OFFLINE CANDIDATE

OBJECT/BLOB
DEFER / TRIGGER ONLY

DIRECT EXECUTION
NOT RUN

PREFERRED
NONE

SELECTED
NONE

NEXT
PM-09 scoring + sensitivity after fresh gate
```