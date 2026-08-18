# PM-08 Specialist Trigger Register v1

- Status: **CURRENT — PM-08 COMPLETE**
- Workstream: `feature/physical-model`
- Purpose: prevent premature specialist infrastructure while preserving explicit reopen conditions.

## Rule

A deferred specialist is not rejected forever. It reopens only when a concrete accepted requirement makes its net value decision-relevant.

```text
NO TRIGGER
=> NO EXTRA ENGINE

TRIGGER APPEARS
=> fresh evidence/admission gate
=> compare against current primary-native/bounded baseline
=> execution only if remaining uncertainty is decision-relevant
```

## Graph

### Neo4j

```text
CURRENT
DEFER / NOT REJECTED
NO INITIAL ADMISSION
```

Reopen on one or more accepted conditions:

- deep/large variable-length traversal is a major product capability;
- shortest/path-finding becomes material;
- graph recommendation or graph analytics becomes core;
- primary-store traversal latency/resource interference becomes unacceptable;
- graph-native query ergonomics materially blocks an accepted capability.

Required reopen evidence:

- workload definition;
- canonical-to-graph projection contract;
- freshness/deletion/Visibility propagation;
- rebuild/reconciliation;
- edition/topology/cost boundary;
- net benefit over PostgreSQL/TypeDB baseline.

## Vector / hybrid search

### Qdrant 1.18.2

```text
CURRENT
DEFER / NOT REJECTED
```

Reopen on:

- vector corpus/traffic materially exceeds bounded PostgreSQL + pgvector path;
- filtered ANN recall/latency cannot satisfy accepted product requirements;
- vector workload needs independent scaling/isolation;
- dense+sparse/multi-vector/reranking becomes first-class product capability;
- TypeDB becomes primary and accepted search/vector capability requires an external projection.

### pgvector 0.8.6

```text
CURRENT
ADMIT-CONDITIONAL
```

Activation conditions:

- PostgreSQL is selected primary;
- semantic/vector retrieval becomes an accepted requirement.

Reopen dedicated-service comparison only when pgvector limitations become material.

## Search platform

### OpenSearch 3.7

```text
CURRENT
DEFER / NOT REJECTED
```

Reopen on:

- very large lexical/document corpus;
- advanced faceting/relevance engineering is required;
- heavy lexical+vector hybrid search becomes core;
- search analytics/observability requires a dedicated platform;
- search scale/isolation materially conflicts with canonical workload.

## Local / offline

### SQLite 3.53.4

```text
CURRENT
ADMIT BOUNDED ROLE
NOT CANONICAL
```

Exact client implementation reopens when a concrete mobile/web/desktop architecture is designed.

Specific browser/WASM execution is warranted only if the product decision depends on a concrete VFS/OPFS/concurrency configuration.

## Object / blob storage

```text
CURRENT
NO ENGINE ADMITTED
DEFER / TRIGGER ONLY
```

Reopen when accepted requirements define enough of:

```text
binary object classes
expected object sizes
volume/growth
download/upload access pattern
retention/deletion semantics
privacy/encryption requirements
replication/durability requirements
CDN/publication needs
cost constraints
```

At that point compare S3-compatible/self-hosted/managed options rather than preselecting one now.

## Other specialists

A new specialist not named above requires:

1. concrete accepted LifeOS gap;
2. proof that primary/bounded current mechanisms do not responsibly cover it;
3. meaningful net benefit;
4. explicit authority/rebuild/freshness boundary;
5. current version/edition/license/topology evidence;
6. fresh PM scope gate.

No technology is admitted because it is fashionable or because another application uses it.

## Current count

```text
INITIAL EXTRA SERVER ENGINES ADMITTED BY PM-08
0

CONDITIONAL IN-PRIMARY EXTENSION
pgvector 0.8.6

BOUNDED LOCAL CANDIDATE
SQLite 3.53.4

DEFERRED SERVER SPECIALISTS
Neo4j
Qdrant 1.18.2
OpenSearch 3.7
object/blob engine TBD
```
