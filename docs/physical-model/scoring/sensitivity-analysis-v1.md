# PM-09 Sensitivity Analysis v1

- Status: **COMPLETE — RANKING ROBUST / NOT SENSITIVITY-DEPENDENT**
- Finalists: PostgreSQL 18.4 / TypeDB CE 3.12.3
- Score type: evidence-weighted decision score
- Direct benchmark tiers: NOT RUN
- SC-013 deep-history scale: NOT REOPENED

## Base grades

| Dimension | PostgreSQL | TypeDB |
|---|---:|---:|
| Semantic mapping | 8.5 | 9.5 |
| Transaction/concurrency | 9.5 | 7.0 |
| Query/report/traversal | 9.0 | 8.5 |
| History/current | 8.5 | 8.5 |
| Operations/recovery/HA | 9.5 | 6.5 |
| Evolution/migration | 9.0 | 8.0 |
| Performance/resources | 8.0 | 8.0 |
| Python/tooling/cost/exit | 9.5 | 7.0 |

## Accepted sensitivity matrix

| Scenario | Semantic | Tx | Query | History | Ops | Evolution | Perf | Tooling | PostgreSQL | TypeDB | Winner |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| S0 Phase-10 base | 20 | 15 | 15 | 10 | 15 | 10 | 10 | 5 | 89.25 | 80.00 | PostgreSQL +9.25 |
| S1 semantic-heavy | 30 | 10 | 20 | 10 | 10 | 10 | 5 | 5 | 88.75 | 83.00 | PostgreSQL +5.75 |
| S2 early single-node / semantic-friendly | 25 | 15 | 15 | 10 | 10 | 10 | 10 | 5 | 88.75 | 81.50 | PostgreSQL +7.25 |
| S3 operations/recovery-heavy | 15 | 15 | 10 | 10 | 25 | 10 | 10 | 5 | 90.00 | 77.50 | PostgreSQL +12.50 |
| S4 strongly TypeDB-friendly accepted stress | 40 | 10 | 20 | 10 | 5 | 5 | 5 | 5 | 88.00 | 85.25 | PostgreSQL +2.75 |

Every accepted scenario keeps PostgreSQL first.

## Why S4 matters

S4 doubles the original semantic weight from 20% to 40%, increases query weight to 20%, and reduces operations/recovery from 15% to 5%.

That is intentionally favorable to TypeDB, yet PostgreSQL still leads by `2.75` points.

This demonstrates that the base result is not merely an artifact of operational weighting.

## Adversarial boundary scenario

This scenario is intentionally outside the accepted LifeOS priority distribution:

| Semantic | Tx | Query | History | Ops | Evolution | Perf | Tooling |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 50 | 5 | 20 | 10 | 5 | 5 | 2.5 | 2.5 |

Result:

```text
PostgreSQL 87.375
TypeDB      87.500
TypeDB lead 0.125
```

This is recorded only as a comparative boundary because it effectively collapses the weight of consistency, recovery, evolution, resource and tooling concerns that the accepted LifeOS architecture policy explicitly keeps material.

## Continuous semantic break-even

Let semantic weight vary while all seven non-semantic Phase-10 dimensions retain their original relative proportions.

The TypeDB/PostgreSQL break-even occurs at approximately:

```text
semantic mapping weight = 58.441558%
```

Below that boundary PostgreSQL remains ahead under this proportional family. Above it TypeDB can overtake because its only large positive grade delta is semantic mapping.

This boundary is not an accepted default weighting; it quantifies how dominant semantic-model elegance would have to become to reverse the current result.

## Performance sensitivity

The performance/resource grade is tied at `8.0 / 8.0` because no LOW/BASE/HIGH LifeOS benchmark was executed.

Therefore:

```text
PM-09 RANKING
NOT PERFORMANCE-DEPENDENT
```

No finalist receives unmeasured throughput/latency points.

`SC-013` remains closed pre-selection because even a reasonable performance shift cannot explain the current base delta without evidence that performance is in fact decision-dominant.

Reopen trigger remains:

```text
accepted PM-09/PM-10 decision becomes materially dependent on deep-history performance
+
existing evidence cannot resolve it
+
controlled SC-013 execution can change the recommendation
```

Current trigger state: `FALSE`.

## Specialist sensitivity

PM-08 architecture implications are included qualitatively in tooling/cost/exit and query/report/traversal grades:

```text
PostgreSQL path
primary + native FTS + conditional pgvector
likely 0 extra initial search/vector server engines

TypeDB path
primary + likely external search/vector specialist when advanced retrieval is accepted
```

If a future accepted requirement proves that no external search/vector specialist is necessary for the TypeDB architecture, its tooling/topology burden may be rescored. The current base ranking is still not close enough for that single change to create an accepted sensitivity reversal.

## Verdict

```text
RANKING ROBUST
SENSITIVITY-DEPENDENT NO
PERFORMANCE-DEPENDENT NO
SC-013 REOPEN NO
PM-04B REOPEN NO
```

PM-10 may consume this sensitivity record as evidence for recommendation, while keeping `PREFERRED != SELECTED` and preserving all unexecuted implementation proofs.