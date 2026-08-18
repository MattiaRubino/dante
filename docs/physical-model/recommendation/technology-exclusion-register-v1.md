# Technology Exclusion Register v1

- Status: **PM-10 CURRENT EXCLUSION REGISTER**
- Meaning: these technologies/mechanisms are not part of the recommended LifeOS Physical Model. Reintroduction requires a later explicit architecture decision based on a material requirement/evidence change.

| Technology / mechanism | Current PM-10 disposition | Reason |
|---|---|---|
| TypeDB as primary | NO | semantic runner-up; whole-system score and sensitivity favor PostgreSQL |
| XTDB as primary | NO | bitemporal advantage does not outweigh primary integrity/topology costs |
| SurrealDB as primary | NO | no decisive whole-system advantage over PostgreSQL |
| Neo4j | NO | no accepted traversal workload justifies second graph persistence/service |
| Qdrant | NO | pgvector sufficient as first-line accepted vector mechanism |
| OpenSearch | NO | PostgreSQL FTS/pg_trgm sufficient as first-line accepted lexical search |
| TimescaleDB | NO | no accepted workload requires it over PostgreSQL native time/range/partition capabilities |
| Redis / Valkey | NO | no accepted canonical/cache/queue need justifies a new in-memory service |
| Kafka | NO | no accepted event-stream/data-platform workload justifies it |
| RabbitMQ | NO | bounded outbox + Restate cover accepted async classes |
| NATS | NO | no distinct accepted need |
| Debezium | NO | no general CDC platform required in accepted stack |
| Dedicated event store | NO | universal event sourcing rejected; material history remains owner-specific |
| Universal event sourcing | NO | contradicts accepted Logical representation discipline |
| Temporal | NO | strong challenger, but larger platform commitment without enough advantage over Restate |
| DBOS | NO | PostgreSQL coupling attractive, but Restate remains stronger Class-B fit |
| Celery + broker | NO | adds broker/worker topology while Restate + bounded PG worker cover accepted classes |
| Zero sync | NO | current offline-write fit insufficient for LifeOS operation-specific offline mutation |
| Electric as full LifeOS sync engine | NO | current read-path posture does not replace governed server mutation path |
| CRDT/local-first canonical authority | NO | conflicts with server canonical authority and operation-specific conflict semantics |
| MongoDB for PowerSync | NO | PostgreSQL bucket storage avoids an unnecessary database |
| Large bytea as standard object store | NO | raw large binary object role belongs to object storage |
| Public R2 bucket | NO | conflicts with bounded authorization/privacy posture |
| Private-object CDN caching by default | NO | adds stale/deletion propagation surface without accepted need |
| Separate vector DB | NO | no current requirement defeats pgvector enough to earn service complexity |
| Separate graph DB | NO | no current requirement defeats primary traversal enough to earn service complexity |
| Separate search engine | NO | no current requirement defeats PostgreSQL FTS enough to earn service complexity |
| Data lake / Spark / Hudi | NO | no accepted scale/analytics workload justifies it |
| pg_cron as LifeOS workflow system | NO | scheduling extension is not durable governed workflow semantics |
| Object Lock Compliance as default | NO | can conflict with policy-driven deletion/retention flexibility |

## Interpretation

`NO` here is stronger than PM-08 `DEFER`: the final recommendation intentionally excludes the mechanism from the accepted stack being proposed to PM-11.

It does not claim the technology is bad or can never be used. A later architecture change must explicitly prove why the accepted stack no longer satisfies a material LifeOS requirement.

## Guardrail

Do not silently reintroduce an excluded engine because a library/framework makes it convenient.
