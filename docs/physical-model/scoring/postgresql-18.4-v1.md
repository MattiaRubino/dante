# PostgreSQL 18.4 — PM-09 Evidence-Weighted Score v1

- Candidate: `P0 PostgreSQL 18.4`
- Role: primary canonical persistence finalist
- Score type: **EVIDENCE-WEIGHTED DECISION SCORE**
- Verified-run score: **NOT AVAILABLE**
- Direct HG PASS count: `0`
- Base score: **89.25 / 100**
- PM-09 disposition: **ROBUST LEADER / ADVANCE TO PM-10 / NOT PREFERRED / NOT SELECTED**

## Dimension record

| Dimension | Weight | Grade /10 | Weighted points |
|---|---:|---:|---:|
| Semantic mapping simplicity / evolvability | 20 | 8.5 | 17.00 |
| Transaction / concurrency ergonomics | 15 | 9.5 | 14.25 |
| Query / reporting / traversal | 15 | 9.0 | 13.50 |
| History + current-state efficiency | 10 | 8.5 | 8.50 |
| Operations / backup / restore / HA | 15 | 9.5 | 14.25 |
| Schema evolution / migration | 10 | 9.0 | 9.00 |
| Performance / resource efficiency | 10 | 8.0 | 8.00 |
| Python / tooling / cost / exit risk | 5 | 9.5 | 4.75 |
| **Total** | **100** |  | **89.25** |

## Rationale

### Semantic mapping — 8.5

The accepted PM-02 relational/hybrid mapping preserves LifeOS owner, relation, reference-family, material-state and history semantics without a universal ontology root. It is less semantically direct than TypeDB for relation/role/n-ary structures and therefore does not receive the top grade.

Primary evidence:

- `docs/physical-model/pm-02-primary-mapping-overview-v1.md`
- `docs/physical-model/mappings/postgresql-18.4-v1.md`
- `docs/physical-model/preflight/postgresql-18.4-v1.md`
- `docs/physical-model/evidence/postgresql-18.4-v1.md`
- `docs/physical-model/qualification/postgresql-18.4-v1.md`

### Transaction / concurrency — 9.5

Strong transaction boundaries, explicit locking/Serializable options and expected-state implementation ergonomics fit consequential LifeOS writes with less persistent hardening machinery than the TypeDB consistency-guard path.

### Query / reporting / traversal — 9.0

Broad structured/reporting capability, recursive traversal, history querying and PM-08 search consolidation provide a strong aggregate query envelope. TypeDB remains stronger for relationship-native semantics, preventing a perfect score.

### History/current efficiency — 8.5

The PM-02 explicit material/current-history strategy is viable and does not require lifetime replay for normal current reads. No direct deep-history benchmark exists, so no speculative 9+ performance claim is made.

### Operations / recovery / HA — 9.5

PM-07 established the strongest finalist posture: WAL/PITR, full/incremental base-backup paths, physical/logical replication, standby/failover primitives and mature upgrade/migration options for the self-hosted zero-license-cost subject.

### Schema evolution / migration — 9.0

Multiple mature controlled evolution paths exist. Actual LifeOS V1→V2 preservation remains a post-selection implementation proof under `SC-030` and is not declared executed.

### Performance / resource efficiency — 8.0

Intentional neutral viable grade. PM-06 found no ranking-critical performance uncertainty but did not run LOW/BASE/HIGH LifeOS tiers. No invented throughput advantage is awarded.

### Python / tooling / cost / exit — 9.5

Strong Python tooling/ecosystem, PostgreSQL License, broad operational tooling and low exit/migration coupling. PM-08 also showed a credible minimum-server path using native FTS plus conditional pgvector rather than requiring a separate search/vector server initially.

## Sensitivity result

PostgreSQL leads every accepted sensitivity scenario, including the strongly TypeDB-friendly `40% semantic / 20% query` case.

```text
BASE                         89.25 vs 80.00
SEMANTIC-HEAVY               88.75 vs 83.00
EARLY SINGLE-NODE            88.75 vs 81.50
OPERATIONS/RECOVERY-HEAVY    90.00 vs 77.50
STRONGLY TYPEDB-FRIENDLY     88.00 vs 85.25
```

The ranking is therefore `ROBUST`, not `SENSITIVITY-DEPENDENT`.

## Conditions carried forward

This score does not waive:

- SC-011 anti-resurrection;
- SC-030 actual LifeOS evolution;
- SC-031 semantic restore verification;
- SC-032 capacity/backpressure;
- WL-H12 system-level non-interference;
- search/vector/local implementation validation where those mechanisms become active.

## Verdict

```text
EVIDENCE-WEIGHTED SCORE 89.25
CURRENT ROBUST LEADER
ADVANCE PM-10
PREFERRED NONE
SELECTED NONE
VERIFIED-RUN SCORE NOT AVAILABLE
```