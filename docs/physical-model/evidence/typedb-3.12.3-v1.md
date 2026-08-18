# TypeDB CE 3.12.3 — PM-04A Evidence Sufficiency v1

- Candidate: TypeDB CE 3.12.3 / self-hosted single-node / official driver 3.12.3
- Mapping: `PM02-TDB-001`
- Status: **EXTERNAL EVIDENCE REVIEW COMPLETE / DIRECT EXECUTION NOT RUN**
- Selection: **NONE**
- Evidence confidence: **MEDIUM-HIGH**

## 1. PM-04A conclusion

TypeDB remains the principal semantic challenger because its type/relation/role model maps naturally to LifeOS's explicit relation semantics and n-ary structures.

The PM-03 `HG-04/HG-05` uncertainty is narrowed from an unknown engine behavior to a documented design condition. TypeDB documents snapshot isolation and conflict when concurrent transactions update the same piece of data. Therefore PM-02's narrow `consistency-guard` is a credible hardening pattern **if every operation sharing a write-skew-sensitive invariant mutates the same guard**.

The remaining cost is guard coverage, ergonomics and operational discipline. A one-off local race test would not prove future coverage across all LifeOS operations.

```text
EXECUTION-WORTHY GAP NOW
0

PM-04B REQUIRED NOW
NO

DIRECT HG PASS CREATED
NO
```

## 2. Primary source ledger

| Topic | Source | Evidence use |
|---|---|---|
| transactions | https://typedb.com/docs/core-concepts/typedb/transactions/ | snapshot isolation, commit/conflict semantics |
| constraining data | https://typedb.com/docs/core-concepts/typeql/constraining-data/ | schema constraint model |
| `@key` | https://typedb.com/docs/typeql-reference/annotations/key/ | keyed identity constraints |
| `@unique` | https://typedb.com/docs/typeql-reference/annotations/unique/ | uniqueness capability |
| `@card` | https://typedb.com/docs/typeql-reference/annotations/card/ | cardinality capability |
| entities/relations/attributes | https://typedb.com/docs/core-concepts/typeql/entities-relations-attributes/ | relation/role semantics |
| `plays` | https://typedb.com/docs/typeql-reference/statements/plays/ | role eligibility |
| timezone-aware datetime | https://typedb.com/docs/typeql-reference/values/datetimetz/ | HG-10 temporal primitive |
| duration | https://typedb.com/docs/typeql-reference/values/duration/ | HG-10 duration primitive |
| self-hosted backups | https://typedb.com/docs/maintenance-operation/typedb-backups/ | HG-09/HG-12 operational capability/limits |
| export/import | https://typedb.com/docs/maintenance-operation/database-export-import/ | recovery/evolution support |
| upgrades | https://typedb.com/docs/maintenance-operation/typedb-upgrades/ | operational evolution |

## 3. Supporting benchmark / production evidence

Supporting only; vendor-owned evidence is not treated as neutral benchmark authority.

| Evidence | Source | Relevance |
|---|---|---|
| TypeDB 3 benchmark | https://typedb.com/blog/first-look-at-typedb-3-benchmarks | demonstrates substantial relation-heavy dataset/query viability; published methodology is single-threaded, so not concurrency proof |
| Origin Sciences case study | https://typedb.com/blog/typedb-helps-origin-sciences-build-a-cancer-research-platform-that-finds-what-conventional-pipelines-miss | real relation-rich scientific usage and explicit multi-technology architecture |

The published benchmark is useful viability evidence but does not establish exact TypeDB 3.12.3 LifeOS performance and is not used for HG-04/HG-05.

## 4. Gate-by-gate sufficiency

| Gate | PM-04A class | Rationale |
|---|---|---|
| HG-01 | MAP-SUFFICIENT | concrete entity/relation/state types preserve owner census without a semantic generic root |
| HG-02 | EXT+MAP-SUFFICIENT | typed roles/player eligibility plus explicit key families preserve bounded Reference Contracts |
| HG-03 | EXT+MAP-SUFFICIENT | first-class named roles, n-ary relations and cardinality constraints are a direct semantic strength |
| HG-04 | MAP-SUFFICIENT / CONDITION | expected material-state matching + shared guard for write-skew-sensitive boundary gives explicit conflict path |
| HG-05 | MAP-SUFFICIENT / KNOWN DESIGN COST | one write transaction plus shared guard can coordinate co-located invariants; snapshot isolation makes correct guard scoping mandatory |
| HG-06 | MAP-SUFFICIENT | explicit material-state objects/current-state relations retain history without event replay |
| HG-07 | MAP-SUFFICIENT | concrete provider/projection/state structures remain separate by type/role |
| HG-08 | MAP-SUFFICIENT / DEFER-FINALIST | rich query/schema semantics help, but non-interference is a system disclosure contract |
| HG-09 | DEFER-FINALIST / KNOWN OPS COST | self-hosted backup is operator responsibility; LifeOS anti-resurrection still needs finalist rehearsal |
| HG-10 | EXT+MAP-SUFFICIENT | temporal primitives plus explicit LifeOS temporal structures preserve named-zone/floating/recurrence meaning |
| HG-11 | EXT+DEFER-FINALIST | schema evolution/export/import paths exist; actual LifeOS historical interpretation needs concrete finalist mapping |
| HG-12 | KNOWN OPS COST + DEFER-FINALIST | backup/export paths exist but self-hosted operational burden is materially higher than PostgreSQL's mature ecosystem |

## 5. Snapshot isolation and consistency guard

TypeDB does not document full serializable isolation for ordinary transactions; the accepted subject is treated as snapshot-isolated.

General write-skew pressure therefore remains real for disjoint writes. PM-02 introduced a bounded technical guard:

```text
invariant boundary I

T1 writes semantic object A + guard(I)
T2 writes semantic object B + guard(I)

both transactions now contend on the same guard data
```

Because TypeDB documents conflict when concurrent transactions update the same piece of data, this pattern is conditionally credible.

What this proves by reasoning:

```text
IF every relevant operation mutates the same correctly scoped guard
THEN disjoint semantic writes no longer remain disjoint at the physical conflict point
```

What it does **not** prove:

```text
that every future LifeOS operation chose the correct guard boundary
that a global guard is acceptable
that snapshot isolation itself became serializable
```

Those are architecture discipline concerns and count against ergonomics/complexity rather than forcing a local PM-04 benchmark.

## 6. Relation-semantic advantage

TypeDB has a genuine structural advantage for LifeOS relation-heavy semantics:

```text
relation types
named roles
role eligibility
relation-owned attributes
n-ary relations
cardinality/key/unique constraints
```

This makes Agreement, Representation and other qualified relations more directly expressible than in ordinary relational tables.

PM-04A preserves that as a real benefit; it does not automatically make TypeDB the better overall canonical store because operability, concurrency model and ecosystem remain separate decision dimensions.

## 7. Backup/evolution operational posture

For self-hosted TypeDB, official guidance places meaningful backup responsibility on the operator and includes snapshot/export-import approaches.

PM-04A therefore records:

```text
CAPABILITY
present

OPERABILITY COST
material

OLD-BACKUP ANTI-RESURRECTION
DEFER-FINALIST

LIFEOS V1 -> V2 SEMANTIC CONTINUITY
DEFER-FINALIST
```

This is a comparative cost, not a reason to manufacture four local restore labs now.

## 8. Multi-technology evidence

The Origin Sciences case is useful architecturally because it does not force TypeDB to own every workload: relation-rich semantic structure is handled separately from dense numeric data using other technologies.

LifeOS may likewise use a primary canonical store plus bounded specialists, but TypeDB must still earn the canonical-primary role on its own merits; a specialist cannot compensate for a primary hard-gate failure.

## 9. Current disposition

```text
P1 TYPEDB CE 3.12.3
PRINCIPAL SEMANTIC CHALLENGER
HG-04/HG-05 UNKNOWN -> NARROWED TO DOCUMENTED DESIGN CONDITION
NO PM-04B EXECUTION ADMITTED
EXECUTED HG STILL NOT RUN
NO SCORE
NO SELECTION
```

Reopen targeted concurrency execution only if later comparative scoring is close enough that guard behavior/ergonomics could materially change the recommendation.
