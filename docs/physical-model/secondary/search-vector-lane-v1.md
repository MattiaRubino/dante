# PM-08 Search / Vector Lane v1

- Status: **COMPLETE — POSTGRESQL FTS BASELINE ADVANCES / PGVECTOR ADMIT-CONDITIONAL**
- Workstream: `feature/physical-model`
- Direct execution: **NOT RUN**
- Selection: **NONE**

## Question

What is the minimum search/vector architecture that preserves LifeOS scope, Visibility, freshness and deletion semantics without adding a dedicated service before it is justified?

## PostgreSQL lexical baseline

PostgreSQL 18 provides native full-text search with `tsvector`, `tsquery`, indexing, parsing, ranking and text-search configuration.

Verdict:

```text
POSTGRESQL NATIVE FTS
ADVANCE AS P0 LEXICAL BASELINE
```

This baseline keeps ordinary lexical retrieval inside the canonical database boundary when PostgreSQL is primary.

## pgvector

Frozen PM-08 subject:

```text
pgvector 0.8.6
PostgreSQL extension
PostgreSQL License
PostgreSQL 18 supported
```

Capabilities relevant to LifeOS include exact vector similarity plus HNSW and IVFFlat approximate indexes.

Architectural advantage:

```text
canonical structured predicates
+
scope / Visibility predicates
+
vector similarity

can remain inside PostgreSQL
```

Embedding/vector state remains derived/projection state. It never becomes NativeRef, MaterialStateRef or canonical semantic truth.

### Filtered ANN sensitivity

Approximate vector retrieval with restrictive filters can require iterative scans, partial indexes, partitioning or other tuning to preserve useful recall/latency.

LifeOS therefore retains the rule:

```text
VECTOR QUALITY
must be judged after real scope / Visibility filtering
```

This is implementation/performance pressure, not permission to weaken security filtering.

Verdict:

```text
PGVECTOR 0.8.6
ADMIT-CONDITIONAL

CONDITIONS
PostgreSQL selected primary
AND
accepted semantic/vector retrieval requirement exists

DEDICATED VECTOR SERVICE INITIAL REQUIREMENT
NO
```

## Qdrant

Frozen PM-08 subject:

```text
Qdrant 1.18.2
Apache-2.0
```

Relevant capabilities include dense and sparse vector search, payload filtering, hybrid retrieval, rank fusion and multi-stage query flows.

Qdrant is a credible specialist but another service would add:

```text
separate persistence
projection pipeline
backup/recovery
monitoring
security surface
scope/Visibility propagation
redaction/deletion propagation
freshness/reconciliation
```

Verdict:

```text
QDRANT 1.18.2
DEFER / NOT REJECTED
SPECIALIST TRIGGER ONLY
```

Reopen triggers include:

```text
very large vector corpus
filtered ANN quality/scale failure in pgvector
independent vector scaling becomes material
multi-vector / dense+sparse / reranking becomes core product capability
vector workload materially interferes with canonical PostgreSQL workload
TypeDB selected primary and accepted search/vector capability requires a separate projection
```

## OpenSearch

Frozen PM-08 subject:

```text
OpenSearch 3.7
```

Relevant capabilities include dedicated lexical search, relevance tooling, vector/hybrid search and search/observability infrastructure.

Verdict:

```text
OPENSEARCH 3.7
DEFER / NOT REJECTED
SPECIALIST TRIGGER ONLY
```

Reopen triggers include:

```text
large document/search corpus
advanced faceting/relevance engineering
heavy lexical + vector hybrid search
search analytics becomes first-class
search workload requires independent scale/isolation
```

## TypeDB implication

PM-08 does not establish a TypeDB-native equivalent to the combined PostgreSQL FTS + pgvector path.

Therefore, if TypeDB wins the primary selection, an accepted lexical/vector capability is more likely to require a bounded external projection/service.

Current trigger candidate:

```text
Qdrant
credible combined vector/hybrid specialist
NOT SELECTED
NOT ADMITTED NOW
```

This probable additional service is a PM-09 operations/TCO/topology input.

## Secondary truth/freshness contract

Any search/vector mechanism must retain:

```text
source canonical/material basis
projection revision
freshness/lag state
Visibility/scope enforcement
redaction/deletion propagation
repair/rebuild path
stale-result handling
```

Search/vector results may inform derived/candidate state; they cannot silently authorize consequential effects as current canonical truth.

## Scenario carry-forward

```text
SC-017 hidden-result non-interference
POST-SELECTION SEARCH/SYSTEM VALIDATION

SC-018 FTS mixed filter/query
POST-SELECTION SEARCH IMPLEMENTATION VALIDATION

SC-019 vector recall after security filter
REOPEN BEFORE SELECTION only if vector path becomes ranking/performance-sensitive;
otherwise post-selection implementation validation

SC-020 stale index source
POST-SELECTION PROJECTION VALIDATION when projection exists

SC-021 deletion propagation
POST-SELECTION PROJECTION VALIDATION when projection exists
```

None is a direct PASS.

## Direct execution decision

```text
PGVECTOR BENCHMARK
NOT ADMITTED NOW

QDRANT BENCHMARK
NOT ADMITTED

OPENSEARCH BENCHMARK
NOT ADMITTED

PM-08 EXECUTION-WORTHY SEARCH/VECTOR GAP
0
```

## Source ledger

- PostgreSQL 18 Full Text Search documentation.
- pgvector repository/changelog for 0.8.6, PostgreSQL 18 support and index behavior.
- Qdrant 1.18.2 repository/release evidence and official search/filter/hybrid documentation.
- OpenSearch 3.7 official release documentation.

## Closure

```text
P0 LEXICAL BASELINE
PostgreSQL native FTS

PGVECTOR
ADMIT-CONDITIONAL

QDRANT
DEFER / TRIGGER ONLY

OPENSEARCH
DEFER / TRIGGER ONLY

PREFERRED
NONE
SELECTED
NONE
```