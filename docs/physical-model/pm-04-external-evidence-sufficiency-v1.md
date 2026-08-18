# PM-04A External Evidence Sufficiency v1

- Status: **PM-04A COMPLETE / PM-04B NOT ADMITTED**
- Workstream: `feature/physical-model`
- PM-04A PRE-SCOPE: `0e4212909bd94de076c9074302a79296d474e53f`
- Scope: primary-candidate external evidence sufficiency and residual-gap analysis
- Direct database execution: **NOT RUN**
- Local/server benchmark: **NOT RUN / NOT REQUIRED BY PM-04A**
- Harness/fixtures: **NOT STARTED**
- Technology selection: **NONE**

## 1. Purpose

PM-04A prevents LifeOS from manufacturing local benchmark work for questions already answered well enough by authoritative engine documentation, formal database guarantees, reproducible public evidence or real production experience.

The sequence remains `PM-00 -> ... -> PM-14`. PM-04 is refined into:

```text
PM-04A
external evidence exhaustion
+ LifeOS mapping reasoning
+ residual-gap analysis

        ↓ only if justified

PM-04B
targeted fixture / oracle / harness
for decision-relevant unresolved questions only
```

This is an execution-minimization rule, not a weakening of Phase-10 correctness requirements.

## 2. Non-negotiable evidence separation

```text
OFFICIAL ENGINE GUARANTEE
!=
LIFEOS DIRECT EXECUTION

PUBLIC BENCHMARK
!=
LIFEOS BENCHMARK

PRODUCTION CASE STUDY
!=
PROOF OF OUR MAPPING

REASONED MAPPING SUFFICIENCY
!=
EXECUTED HARD-GATE PASS
```

Accordingly, all direct `HG-01..HG-12` execution slots remain `NOT RUN` after PM-04A.

PM-04A asks a different question:

> Is additional LifeOS-specific execution currently necessary to make a responsible comparative decision, or would it merely repeat settled engine properties?

## 3. Evidence classes

PM-04A uses the following evidence-sufficiency classifications.

### `EXT-SUFFICIENT`

Authoritative product documentation or an equivalent primary source establishes the relevant engine capability/limitation strongly enough for current comparative reasoning.

### `MAP-SUFFICIENT`

The PM-02 mapping plus documented engine guarantees are sufficient to establish a credible LifeOS implementation path without a decision-relevant direct test now.

### `KNOWN-STRUCTURAL-COST`

The uncertainty has resolved into a known limitation or operational/design burden. A small local test would not remove the structural cost.

### `DEFER-FINALIST`

The question is real and may require direct LifeOS operational rehearsal before final acceptance, but testing all four candidates now is disproportionate. It should be revisited only for a finalist or if it becomes ranking-critical.

### `RESIDUAL-GAP`

Evidence remains materially incomplete.

### `EXECUTION-WORTHY`

A residual gap is both unresolved and capable of materially changing the recommendation. Only this class may open PM-04B without a new methodology revision.

## 4. Source-quality rule

Evidence is ranked approximately as:

```text
version-specific official documentation / release notes
formal documented consistency / transaction / constraint semantics
official operational documentation
reproducible public benchmark with disclosed method/raw implementation
production engineering evidence
vendor case study / vendor benchmark
independent secondary commentary
```

Lower classes may support a conclusion but do not override contradictory primary documentation.

Vendor benchmark and vendor case-study evidence is explicitly marked supporting; it is not treated as neutral proof.

## 5. Cross-candidate PM-04A evidence-sufficiency matrix

This matrix is **not** an executed hard-gate matrix and is **not** a score.

| Gate | PostgreSQL 18.4 | TypeDB CE 3.12.3 | XTDB 2.1.0 | SurrealDB CE 3.2.3 |
|---|---|---|---|---|
| HG-01 semantic ownership | MAP-SUFFICIENT | MAP-SUFFICIENT | MAP-SUFFICIENT | MAP-SUFFICIENT |
| HG-02 reference-family integrity | EXT+MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | KNOWN-STRUCTURAL-COST | EXT+MAP-SUFFICIENT |
| HG-03 typed/n-ary relation fidelity | EXT+MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | KNOWN-STRUCTURAL-COST | EXT+MAP-SUFFICIENT |
| HG-04 expected-state concurrency | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / guard condition | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / guard condition |
| HG-05 multi-owner consistency | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / KNOWN COST | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / KNOWN COST |
| HG-06 history/correction/reconciliation | MAP-SUFFICIENT | MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / KNOWN COST |
| HG-07 state-layer separation | MAP-SUFFICIENT | MAP-SUFFICIENT | MAP-SUFFICIENT | MAP-SUFFICIENT |
| HG-08 governance/selective disclosure | MAP-SUFFICIENT / DEFER-FINALIST system proof | MAP-SUFFICIENT / DEFER-FINALIST system proof | MAP-SUFFICIENT / DEFER-FINALIST system proof | MAP-SUFFICIENT / DEFER-FINALIST system proof |
| HG-09 retention/redaction/restore | DEFER-FINALIST | DEFER-FINALIST / KNOWN OPS COST | DEFER-FINALIST | DEFER-FINALIST |
| HG-10 temporal/recurrence/timezone | EXT+MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT |
| HG-11 schema/data evolution | DEFER-FINALIST | EXT+DEFER-FINALIST | KNOWN-STRUCTURAL-COST + DEFER-FINALIST | EXT+DEFER-FINALIST |
| HG-12 recoverability/evidence | EXT+DEFER-FINALIST | KNOWN OPS COST + DEFER-FINALIST | KNOWN OPS/TOPOLOGY COST + DEFER-FINALIST | EXT+DEFER-FINALIST |

### PM-04A totals that matter

```text
EXECUTION-WORTHY gaps now     0
FULL LOCAL BENCHMARK admitted  0
PM-04B harness admitted        NO
DIRECT HG PASS created         0
SELECTION created              NONE
```

## 6. Candidate conclusions

### P0 — PostgreSQL 18.4

Current evidence confidence: **HIGH** for engine fundamentals / **MEDIUM-HIGH** for the LifeOS mapping before concrete schema implementation.

The engine side of transactions, referential integrity, constraints, backup/PITR and controlled upgrade paths is mature and strongly documented. The remaining LifeOS questions are primarily mapping discipline: keeping heterogeneous address anchors technical, choosing the correct transaction strength per operation and enforcing disclosure without treating RLS as the complete WL-H12 solution.

A local CRUD/performance benchmark would add little decision value now.

Disposition:

```text
CURRENT COMPARATIVE LEADER
NOT SCORED
NOT PREFERRED BY PM-09
NOT SELECTED
PM-04B NOT REQUIRED NOW
```

### P1 — TypeDB CE 3.12.3

Current evidence confidence: **MEDIUM-HIGH**.

TypeDB remains the strongest semantic relation/role challenger. Its documented schema model directly supports typed relation roles, relation-owned attributes and cardinality/key constraints.

The PM-03 concurrency HOLD is narrowed materially. TypeDB documents snapshot isolation and concurrent write conflicts when transactions update the same piece of data. Therefore the PM-02 narrow `consistency-guard` pattern is conditionally sound: every transaction sharing a write-skew-sensitive invariant boundary must mutate the same guard, deliberately converting disjoint semantic writes into a shared write conflict.

This is a reasoned conditional proof, not direct execution. The remaining issue is guard **coverage and complexity**, not an unknown database primitive. A single local race test cannot prove that every future LifeOS write path scopes guards correctly.

Disposition:

```text
PRINCIPAL SEMANTIC CHALLENGER
CONCURRENCY RISK -> KNOWN DESIGN CONDITION
NO EXECUTION-WORTHY GAP NOW
NOT SELECTED
```

### P2 — XTDB 2.1.0

Current evidence confidence: **MEDIUM-HIGH on chronology/concurrency / MEDIUM on primary-store integrity ergonomics**.

XTDB documents serialized DML transactions through a totally ordered log, serializable write semantics and transaction `ASSERT` support. This is strong external evidence for expected-state and co-located multi-owner consistency.

XTDB also documents the exact structural weakness PM-03 identified: no native foreign keys and no uniqueness constraints beyond `_id`; referential integrity can be implemented atomically but must be modeled manually. The question is therefore no longer “does XTDB secretly enforce this?” It is a known architectural burden.

A local negative/positive test could prove one implementation path but would not eliminate the long-term requirement that all consequential writers preserve the manual integrity contract. The burden therefore counts against the candidate directly instead of forcing a local test.

Production-topology/single-writer sensitivity remains a separate HOLD/condition and is not resolvable by a laptop benchmark.

Disposition:

```text
TEMPORAL / BITEMPORAL CHALLENGER
REFERENCE/CARDINALITY RISK -> KNOWN STRUCTURAL COST
PRODUCTION TOPOLOGY HOLD REMAINS
NO EXECUTION-WORTHY GAP NOW
NOT SELECTED
```

### P3 — SurrealDB Community 3.2.3

Current evidence confidence: **MEDIUM-HIGH on documented capability / MEDIUM on net LifeOS primary advantage**.

SurrealDB documents SCHEMAFULL tables, typed record/relation structures and snapshot-isolated transactions with write-write conflict detection. PM-02 already avoids collapsing n-ary/material semantics into generic graph edges.

As with TypeDB, a narrow consistency guard that every transaction in the same invariant boundary mutates creates a common write-conflict point. That reduces the PM-03 concurrency uncertainty to a known architecture condition/complexity cost.

Explicit LifeOS material history remains necessary; bounded changefeeds are not accepted as canonical long-term history. The candidate therefore survives but has not yet shown a unique primary-store advantage large enough to outweigh its additional maturity/semantic-discipline questions versus the current leader.

Disposition:

```text
MULTIMODEL CHALLENGER
CONCURRENCY RISK -> KNOWN DESIGN CONDITION
NO EXECUTION-WORTHY GAP NOW
NOT SELECTED
```

## 7. Residual-gap register

### RG-01 — WL-H12 system-level non-interference

Applies: all candidates.

The database can contribute primitives, but hidden counts, ranking, errors, relation existence, explanation surfaces and timing are system/query-policy concerns. A database-only local benchmark cannot prove the full disclosure contract.

```text
CLASS
DEFER-FINALIST / downstream system proof

CURRENT RANKING IMPACT
low as primary differentiator
```

### RG-02 — old-backup anti-resurrection

Applies: all candidates.

All four require a LifeOS restore/reconciliation policy, not merely a backup command. Rehearse it for the finalist before final Physical acceptance if still required by Phase-10 closure.

```text
CLASS
DEFER-FINALIST
```

### RG-03 — LifeOS V1 -> V2 semantic evolution

Applies: all candidates.

Engine migration capabilities are externally assessable; preservation of actual LifeOS identities/material-state bindings can only be tested after a concrete executable mapping exists. Running four speculative migrations now is disproportionate.

```text
CLASS
DEFER-FINALIST
```

### RG-04 — semantic post-restore verification

Applies: all candidates.

Operational recovery capability can be compared now from authoritative documentation. LifeOS semantic restore rehearsal is finalist evidence.

```text
CLASS
DEFER-FINALIST
```

### RG-05 — TypeDB consistency-guard completeness

The engine guarantees needed by the guard pattern are documented. Correct guard scoping remains a mapping/application obligation.

```text
CLASS
MAP-SUFFICIENT / KNOWN DESIGN COST
EXECUTION-WORTHY NOW
NO
REOPEN TRIGGER
a later TypeDB/PostgreSQL ranking tie materially depends on concurrency ergonomics
```

### RG-06 — XTDB manual referential/cardinality integrity

The limitation is documented and persistent by architecture. A local test cannot turn “manual enforcement required” into “native enforcement exists”.

```text
CLASS
KNOWN-STRUCTURAL-COST
EXECUTION-WORTHY NOW
NO
```

### RG-07 — SurrealDB consistency-guard completeness

Same logic as RG-05: documented write-write conflict support makes the guard pattern credible; coverage remains system design burden.

```text
CLASS
MAP-SUFFICIENT / KNOWN DESIGN COST
EXECUTION-WORTHY NOW
NO
```

### RG-08 — PostgreSQL heterogeneous-address anchor complexity

This is a mapping complexity/evolvability issue, not an unknown engine behavior. PM-02 already constrains the anchor to technical addressability only.

```text
CLASS
MAP-SUFFICIENT
EXECUTION-WORTHY NOW
NO
REOPEN TRIGGER
concrete schema design demonstrates anchor leakage or unmaintainable contract enforcement
```

### RG-09 — XTDB production topology / single-writer sensitivity

This is an operational/topology sensitivity question. A local single-machine benchmark cannot settle future HA/geographic/TCO implications.

```text
CLASS
KNOWN-STRUCTURAL/TOPOLOGY CONDITION
HOLD REMAINS
```

## 8. Public benchmark treatment

Public performance evidence is useful for detecting obvious viability problems and understanding published scale behavior, but PM-04A does not rank candidates by vendor throughput charts.

Examples reviewed include:

- TypeDB's published TPC-C-derived benchmark: useful scale/query evidence, but single-threaded and on an earlier TypeDB 3.x point release, therefore not concurrency proof or exact 3.12.3 performance evidence;
- SurrealDB's open `crud-bench`: useful as disclosed reproducible CRUD/load evidence, but vendor-owned and not a LifeOS semantic workload;
- production engineering evidence such as Notion's PostgreSQL architecture: strong maturity/scale evidence, not proof of the LifeOS mapping;
- XTDB production bitemporal case studies: strong evidence that the temporal model solves real audit/knowledge-time problems, not a primary-store integrity benchmark.

PM-06 must not invent new local throughput work unless performance remains capable of changing the recommendation after correctness/operability evidence.

## 9. Non-scored comparative ordering after PM-04A

This is decision pressure only. It is **not PM-09 scoring**, `PREFERRED` or `SELECTED`.

```text
1. PostgreSQL
   current overall leader
   confidence HIGH

2. TypeDB
   principal semantic challenger
   confidence MEDIUM-HIGH

3. XTDB
   distinctive temporal challenger
   confidence MEDIUM-HIGH on temporal core / MEDIUM overall primary fit

4. SurrealDB
   credible multimodel challenger
   confidence MEDIUM
```

Why the order is currently stable:

- PostgreSQL combines the lowest primary-store structural risk with mature integrity/concurrency/recovery tooling and a mapping that preserves LifeOS semantics without requiring a generic ontology.
- TypeDB offers the cleanest relation/role semantics, but snapshot-isolation hardening and self-hosted operational burden remain material costs.
- XTDB's bitemporality is unusually relevant to LifeOS history, but the no-FK/no-general-uniqueness model shifts too much primary integrity into disciplined application/transaction design.
- SurrealDB is capable and compact, but PM-04A has not found a primary-store advantage decisive enough to overtake the first three under LifeOS's correctness-first priorities.

## 10. PM-04B admission decision

```text
FULL FOUR-CANDIDATE LOCAL BENCHMARK
NOT ADMITTED

TARGETED LOCAL PROOFS
0 ADMITTED

FIXTURE GENERATOR
NOT STARTED

HARNESS
NOT STARTED

DATABASE DEPLOYMENT
NOT STARTED

BENCHMARK HOST
HOLD / DORMANT
not blocking PM-04A or evidence-only work
becomes blocking only if direct execution is separately admitted
```

If a later phase produces a genuinely ranking-critical residual gap, PM-04B may be reopened through a fresh exact write/execution gate.

## 11. Next phase interpretation

PM-05 remains the correctness/destructive qualification phase, but it begins evidence-first rather than assuming every scenario must be re-executed locally across all four products.

PM-05 should:

1. map `C0..C7` / `SC-001..SC-035` to already-sufficient external/mapping evidence;
2. preserve direct execution status as `NOT RUN` unless a direct run occurs;
3. identify any remaining mandatory finalist/direct-proof obligations;
4. admit direct execution only when the unresolved evidence is material and cannot be resolved responsibly otherwise;
5. never convert public evidence into fictional LifeOS run artifacts.

## 12. Candidate evidence records

- `evidence/postgresql-18.4-v1.md`
- `evidence/typedb-3.12.3-v1.md`
- `evidence/xtdb-2.1.0-v1.md`
- `evidence/surrealdb-3.2.3-v1.md`

## 13. PM-04A closure rule

PM-04A is complete when:

```text
all 48 candidate × hard-gate cells classified
source class disclosed
residual gaps explicit
execution-worthy gaps counted
PM-04B admission explicit
executed HG state preserved truthfully
selection remains NONE
remote path/readback QA passes
```

At content completion, those conditions are satisfied subject to remote Git QA of this write scope.
