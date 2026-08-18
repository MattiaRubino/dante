# PM-06 Scale / Performance Evidence v1

- Status: **COMPLETE — EVIDENCE QUALIFIED / DIRECT PERFORMANCE NOT RUN**
- Finalists: PostgreSQL 18.4, TypeDB CE 3.12.3
- Local benchmark: **NOT ADMITTED**

## Question

Can scale/performance/resource evidence materially reverse the current primary-finalist ordering?

## Result

```text
POSTGRESQL 18.4
SCALE/PERFORMANCE VIABLE
confidence HIGH

TYPEDB CE 3.12.3
SCALE/PERFORMANCE VIABLE
confidence MEDIUM-HIGH

LOW / BASE / HIGH
NOT RUN

LOCAL CRUD BENCHMARK
NOT ADMITTED

PERFORMANCE REVERSAL SIGNAL
NONE FOUND
```

## PostgreSQL evidence

PostgreSQL has extensive production-scale evidence and mature mechanisms for indexing, partitioning, concurrency, replication/read scaling and operational tuning. PM-06 does not treat popularity or unrelated production scale as proof of LifeOS latency, but it is strong evidence against an unknown viability risk.

The accepted LifeOS mapping uses owner-specific relational tables, direct foreign keys where homogeneous, bounded technical anchors only for heterogeneous addressability, and explicit material-state/history. PM-06 found no engine-level scale mechanism that forces semantic weakening.

No evidence justifies generating synthetic LOW/BASE/HIGH locally merely to obtain laptop-specific latency numbers before product SLAs exist.

## TypeDB evidence

TypeDB documentation states:

- each query is currently single-threaded;
- increased CPU/memory utilization is achieved through concurrent queries/transactions;
- RocksDB cache defaults and per-transaction working memory materially affect sizing;
- at least roughly 5% of data size in memory is recommended for index accessibility/performance;
- automatic schema-derived indexes add documented disk overhead;
- CE supports single-node deployment;
- horizontal read scaling and cluster HA belong to Cloud/Enterprise.

These are not rejection conditions. They are resource/topology costs that matter when comparing a zero-cost self-hosted canonical primary.

Published TypeDB benchmark evidence supports serious viability but does not constitute LifeOS execution and does not prove exact 3.12.3 concurrent performance. It is sufficient to avoid a false “unknown performance” penalty while preserving the topology/resource caveats.

## SC-013 treatment

```text
SC-013 DEEP-HISTORY CURRENT-STATE SCALE
DIRECT RUN NOT ADMITTED
```

Reason:

1. both finalists have credible paths to current-state queries without full-lifetime replay;
2. no accepted SLA exists that would make a small measured difference decisive;
3. laptop measurements would be host-specific;
4. PM-09 can reopen SC-013 only if its sensitivity model becomes genuinely performance-dependent.

## Qualification tiers

```text
LOW   NOT RUN
BASE  NOT RUN
HIGH  NOT RUN
```

This is intentional. No tier is called verified.

## Load profiles

```text
LP-01 NOT RUN
LP-02 NOT RUN
LP-03 NOT RUN
LP-04 NOT RUN
LP-05 NOT RUN
```

Published/architectural evidence may support comparative scoring later, but no p50/p95/p99 or throughput figure may be presented as a LifeOS measurement.

## Comparative pressure

### PostgreSQL

Strengths:

- broad workload maturity;
- strong concurrency/integrity primitives;
- flexible indexing/query-planning ecosystem;
- scaling paths do not require changing the accepted semantic model;
- no edition boundary for basic self-hosted primary/standby capabilities.

Costs:

- relational history/heterogeneous-reference mapping requires disciplined schema design;
- semantic relation expression is less native than TypeDB.

### TypeDB

Strengths:

- strong semantic query/model alignment;
- relation/role/n-ary traversal can reduce application/query translation burden;
- concurrent transaction workloads can exploit host resources.

Costs/conditions:

- individual query single-threading;
- CE single-node topology;
- documented memory/index sizing pressure;
- horizontal scaling requires non-CE topology;
- concurrency-guard discipline remains part of consequential writes.

## PM-06 conclusion

```text
NO CANDIDATE FAILS PERFORMANCE VIABILITY
NO DIRECT PERFORMANCE RUN IS DECISION-WORTHY
NO PERFORMANCE EVIDENCE REVERSES THE CURRENT ORDER
```

PostgreSQL retains the stronger overall position. TypeDB's route to winning remains semantic simplicity/evolvability, not a demonstrated need for superior raw throughput.

## Reopen triggers

Reopen direct performance qualification only if one of these becomes true:

- accepted LifeOS SLA/scale target makes the finalists plausibly diverge;
- PM-09 ranking is unstable specifically because of scale/history efficiency;
- TypeDB/PostgreSQL architecture changes materially;
- a selected deployment topology imposes a concrete capacity constraint;
- production implementation produces evidence inconsistent with this qualification.

## Sources

- PostgreSQL 18 documentation: backup/HA/replication and general exact-version docs under `https://www.postgresql.org/docs/18/`.
- TypeDB vertical scaling: `https://typedb.com/docs/core-concepts/typedb/vertical-scaling/`.
- TypeDB horizontal scaling: `https://typedb.com/docs/core-concepts/typedb/horizontal-scaling/`.

Vendor benchmark evidence remains supporting context only, never direct LifeOS measurement.