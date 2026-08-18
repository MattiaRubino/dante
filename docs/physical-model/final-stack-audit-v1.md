# Final Stack Audit v1

- Status: **PM-10 SUPPORTING EVIDENCE — COMPLETE**
- Purpose: re-evaluate the full LifeOS physical capability surface before final recommendation.

## Audit inputs

The audit rechecked:

- accepted Product Identity / North Star;
- whole Logical Model and `WL-H01..WL-H12`;
- Phase-5 multi-device/recovery, consistency/side-effect and security/privacy requirements;
- Phase-7 durable-execution benchmark;
- feature-discovery and multi-actor simulation pressure;
- PM-01..PM-09 Physical evidence;
- current primary-source technology/version/topology facts.

## Capability conclusion

The final architecture needs distinct mechanisms for the following concerns, but not distinct canonical databases:

```text
canonical semantic persistence
material history
geospatial queries
lexical and semantic retrieval
offline/multi-device bounded operation
bounded background work
long-running durable process
binary object storage
backup/recovery
planning/constraint solving
observability
```

## Core audit result

| Capability | Recommended mechanism | Separate canonical authority? |
|---|---|---|
| Canonical semantics/history | PostgreSQL 18.4 | YES — sole canonical persistence |
| Geospatial | PostGIS 3.6.4 | NO |
| Lexical search | PostgreSQL FTS + pg_trgm + unaccent | NO |
| Vector retrieval | pgvector 0.8.6 | NO — derived index |
| Graph traversal | PostgreSQL relational mappings + recursive SQL | NO |
| Local/offline | encrypted SQLite + PowerSync 1.25.0 | NO |
| Bounded async | PG transactional outbox + worker | NO |
| Durable Class-B process | Restate | NO — runtime state only |
| Raw object bytes | Cloudflare R2 | NO — bytes only |
| PostgreSQL backup | pgBackRest -> S3 | NO |
| Object backup | R2 -> separate S3 bucket | NO |
| Solver | OR-Tools CP-SAT | NO — candidate output |
| Observability | OTel + Alloy + Grafana + pg_stat_statements | NO |

## Why no infrastructure zoo

The audit explicitly rejected adding infrastructure merely because a specialist exists.

No initial Neo4j/Qdrant/OpenSearch/Redis/Kafka/NATS/RabbitMQ is justified because accepted LifeOS workloads can be satisfied without paying the synchronization, deletion-propagation, security, backup and operations burden of another general server engine.

Restate and PowerSync are exceptions because they solve boundaries PostgreSQL should not pretend to own:

- crash-resumable long waits/external callbacks/human steps;
- bounded local/offline device state and synchronization.

R2 is an exception because large raw binary objects are not canonical relational payloads.

## Offline conclusion

Offline support is required but remains operation-specific.

Accepted physical rule:

```text
LOCAL SQLITE
bounded encrypted working copy

POWERSYNC
transport/projection synchronization

LIFEOS BACKEND
semantic conflict/governance/expected-state authority

POSTGRESQL
canonical truth
```

No global last-write-wins rule is accepted.

## Search/vector conclusion

Advanced retrieval is an accepted product capability, so PostgreSQL-native FTS and pgvector are included in the recommended stack rather than left as an unspecified future branch.

Security and relevance are evaluated in the correct order: retrieval quality must remain valid under actual visibility/user/scope filtering.

## Object conclusion

`ContentArtifact` remains canonical in PostgreSQL while raw bytes live in private object storage. Object storage is therefore a companion persistence class, not a second semantic database.

## Durable execution conclusion

Two async classes remain separate:

```text
CLASS A
short/reconstructible/bounded
-> PostgreSQL outbox + worker

CLASS B
long-running/material recovery coordination
-> Restate
```

This preserves simplicity without rebuilding a workflow engine in application tables.

## Final audit verdict

```text
MATERIAL CAPABILITY HOLES              0
UNJUSTIFIED GENERAL SERVER ENGINES     0
SECOND CANONICAL AUTHORITY              0
OFFLINE CANONICAL AUTHORITY             0
UNIVERSAL LWW                            0
UNIVERSAL EVENT STORE                    0

STACK RECOMMENDATION
READY FOR PM-10
```
