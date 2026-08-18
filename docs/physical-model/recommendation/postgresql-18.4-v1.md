# PostgreSQL 18.4 Recommendation Record v1

- Status: **PM-10 PREFERRED PRIMARY / PASS-CONDITIONAL**
- Candidate: PostgreSQL 18.4
- Selection: **NOT SELECTED**

## Final disposition

```text
PREFERRED PRIMARY
PostgreSQL 18.4

EVIDENCE-WEIGHTED SCORE
89.25 / 100

RANKING
ROBUST

DIRECT HG PASS
0

VERIFIED-RUN SCORE
NOT AVAILABLE
```

## Accepted physical role

PostgreSQL owns:

- all canonical LifeOS owner identities and canonical state;
- explicit material-state/history records and current bindings;
- typed relation/contextual records according to PM-02 mapping;
- integration/provider reconciliation state that belongs to LifeOS;
- technical address anchors required by bounded heterogeneous references;
- transactional outbox/idempotency/invariant-control state where applicable;
- rebuildable search/vector/sync projection source data.

## PostgreSQL capability package

Recommended PostgreSQL-side components:

```text
PostGIS 3.6.4
pgvector 0.8.6
native FTS
pg_trgm
unaccent
pg_stat_statements
PgBouncer 1.25.2 for ordinary pooled traffic
```

### PostGIS

Used for `Place` coordinate/geography storage and distance/proximity/geospatial queries. It does not create Place identity or Domain location semantics.

### pgvector

Used for derived semantic/vector retrieval. Embeddings are projections and must carry enough source/model/material/freshness information for safe use. Vector quality must be tested under actual security/scope filters.

### FTS / pg_trgm / unaccent

Used as the first-line lexical/fuzzy search stack. No initial OpenSearch service is recommended.

### pg_stat_statements

Used for query-performance observability under a least-privilege operational role. It is not an audit/history mechanism.

### PgBouncer

Ordinary short-lived API traffic may use transaction pooling. Session-sensitive replication/admin paths, including PowerSync logical replication and privileged backup/administration, use appropriate direct/session-preserving connections.

## Why TypeDB is not preferred

TypeDB keeps a semantic advantage for direct relation/role/n-ary modeling, but PostgreSQL wins under accepted LifeOS priorities because of:

- stronger transaction/concurrency ergonomics without permanent shared-guard discipline;
- richer self-hosted backup/recovery/HA primitives;
- multiple mature upgrade/migration paths;
- stronger reporting/query/tooling ecosystem;
- lower operational and exit risk;
- ability to consolidate search/vector/geospatial capabilities without adding mandatory server databases.

## Conditions before accepted implementation

Mandatory validation remains:

```text
SC-011 old-backup anti-resurrection
SC-030 actual mapping evolution
SC-031 destructive restore + semantic verification
SC-032 capacity/backpressure
WL-H12 system-level non-interference
SC-017/018 search non-interference
SC-019 filtered vector recall
SC-020/021 projection freshness/deletion propagation
```

Additionally validate chosen extension/pooling interactions under the actual deployment topology.

## Verdict

```text
PM-10
PREFERRED / PASS-CONDITIONAL

PM-11
EXPLICIT SELECTION REQUIRED
```
