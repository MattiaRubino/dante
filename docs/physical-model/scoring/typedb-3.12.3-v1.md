# TypeDB CE 3.12.3 — PM-09 Evidence-Weighted Score v1

- Candidate: `P1 TypeDB CE 3.12.3`
- Role: primary canonical persistence finalist
- Score type: **EVIDENCE-WEIGHTED DECISION SCORE**
- Verified-run score: **NOT AVAILABLE**
- Direct HG PASS count: `0`
- Base score: **80.00 / 100**
- PM-09 disposition: **PRINCIPAL SEMANTIC CHALLENGER / ADVANCE TO PM-10 COMPARATIVE RECORD / NOT PREFERRED / NOT SELECTED**

## Dimension record

| Dimension | Weight | Grade /10 | Weighted points |
|---|---:|---:|---:|
| Semantic mapping simplicity / evolvability | 20 | 9.5 | 19.00 |
| Transaction / concurrency ergonomics | 15 | 7.0 | 10.50 |
| Query / reporting / traversal | 15 | 8.5 | 12.75 |
| History + current-state efficiency | 10 | 8.5 | 8.50 |
| Operations / backup / restore / HA | 15 | 6.5 | 9.75 |
| Schema evolution / migration | 10 | 8.0 | 8.00 |
| Performance / resource efficiency | 10 | 8.0 | 8.00 |
| Python / tooling / cost / exit risk | 5 | 7.0 | 3.50 |
| **Total** | **100** |  | **80.00** |

## Rationale

### Semantic mapping — 9.5

TypeDB wins the strongest semantic dimension. Concrete entity/relation types, named roles, cardinality constraints and first-class n-ary relations align particularly well with accepted LifeOS relation/governance structures while preserving explicit material-state ownership.

Primary evidence:

- `docs/physical-model/pm-02-primary-mapping-overview-v1.md`
- `docs/physical-model/mappings/typedb-3.12.3-v1.md`
- `docs/physical-model/preflight/typedb-3.12.3-v1.md`
- `docs/physical-model/evidence/typedb-3.12.3-v1.md`
- `docs/physical-model/qualification/typedb-3.12.3-v1.md`

### Transaction / concurrency — 7.0

TypeDB remains viable but its snapshot-isolation model requires correctly scoped shared consistency guards for consequential invariants that could otherwise write-skew. The guard mechanism is evidence-grounded, but complete guard coverage is additional persistent implementation and review burden.

### Query / reporting / traversal — 8.5

Relationship-native semantic queries are a major strength. The score remains below PostgreSQL's aggregate query envelope because general reporting/search integration is less consolidated, and PM-08 found no verified TypeDB-native equivalent to PostgreSQL FTS + conditional pgvector.

### History/current efficiency — 8.5

The explicit PM-02 current/material-state history strategy is viable. No direct deep-history LifeOS benchmark exists, so no speculative superiority is awarded.

### Operations / recovery / HA — 6.5

PM-07 established viability but also a material exact-edition burden: CE is single-node; self-hosted backup implementation is LifeOS-owned; documented self-hosted backup paths are snapshots or export/import and are non-incremental; cluster/HA/horizontal read scaling belongs outside the frozen CE subject.

### Schema evolution / migration — 8.0

Schema redefine and cross-version export/import provide a credible evolution path. The operational surface remains larger than PostgreSQL's finalist path, and actual LifeOS V1→V2 preservation remains unexecuted post-selection validation.

### Performance / resource efficiency — 8.0

Intentional neutral viable grade. PM-06 found credible viability but no direct LOW/BASE/HIGH LifeOS run. Each query currently being single-threaded and CE's single-node topology remain conditions, but no invented performance penalty beyond the evidence is applied.

### Python / tooling / cost / exit — 7.0

The CE subject has zero direct license cost and a supported Python driver, but has a smaller operational/tooling ecosystem, greater product-specific modeling coupling and more likely external search/vector topology once advanced retrieval becomes accepted.

## Sensitivity result

TypeDB closes the gap when semantic/query weights are increased substantially, but does not win any accepted sensitivity scenario.

```text
BASE                         80.00 vs 89.25
SEMANTIC-HEAVY               83.00 vs 88.75
EARLY SINGLE-NODE            81.50 vs 88.75
OPERATIONS/RECOVERY-HEAVY    77.50 vs 90.00
STRONGLY TYPEDB-FRIENDLY     85.25 vs 88.00
```

A deliberately adversarial weighting with semantic mapping at 50% produces only a 0.125 TypeDB lead and is not accepted because it suppresses consistency/operations/recovery/evolution/tooling priorities already frozen by LifeOS.

Keeping the original non-semantic weights proportional, semantic mapping must rise to approximately `58.44%` of total decision weight before TypeDB reaches break-even.

## Conditions carried forward

If TypeDB were later reconsidered or selected, the following remain material:

- consistency-guard completeness;
- CE single-node topology;
- self-hosted backup orchestration;
- likely external search/vector specialist when advanced retrieval is accepted;
- SC-011/030/031/032 post-selection implementation validation;
- WL-H12 and search/projection non-interference obligations.

## Verdict

```text
EVIDENCE-WEIGHTED SCORE 80.00
PRINCIPAL SEMANTIC CHALLENGER
NOT SENSITIVITY WINNER
ADVANCE PM-10 COMPARATIVE RECORD
PREFERRED NONE
SELECTED NONE
VERIFIED-RUN SCORE NOT AVAILABLE
```