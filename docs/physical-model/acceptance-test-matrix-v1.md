# Physical Model Acceptance Test Matrix v1

- Status: **CURRENT — BOOTSTRAP**
- Workstream: `feature/physical-model`
- Execution status: **NOT STARTED**
- Purpose: convert Phase-10 hard gates, corpus families and scenarios into an auditable execution ledger

## Rule

This matrix is an execution index, not a substitute for the full Phase-10 specification/corpus. Scenario meaning and semantic assertions remain authoritative there.

```text
EMPTY / NOT RUN
!= PASS
```

Every material PASS must point to reproducible evidence.

# 1. Primary hard gates

| Gate | Meaning | PostgreSQL | TypeDB | Evidence requirement |
|---|---|---|---|---|
| HG-01 | Semantic ownership preservation | NOT RUN | NOT RUN | mapping review + representative executable proof |
| HG-02 | Reference-family integrity | NOT RUN | NOT RUN | NativeRef/ScopedRecordRef/MaterialStateRef/ExternalRef tests |
| HG-03 | Typed/n-ary relation fidelity | NOT RUN | NOT RUN | typed-role/cardinality/query/history proof |
| HG-04 | Expected-state consequential concurrency | NOT RUN | NOT RUN | stale-base race + explicit conflict evidence |
| HG-05 | Multi-owner consistency truthfulness | NOT RUN | NOT RUN | atomic/staged failure evidence |
| HG-06 | History/correction/reconciliation reconstructibility | NOT RUN | NOT RUN | current + as-of/history oracle comparison |
| HG-07 | State-layer separation | NOT RUN | NOT RUN | canonical/history/derived/provider/candidate separation proof |
| HG-08 | Governance/selective disclosure | NOT RUN | NOT RUN | authorization/disclosure/non-interference corpus |
| HG-09 | Retention/redaction/tombstone/restore integrity | NOT RUN | NOT RUN | redaction + old-backup restore anti-resurrection proof |
| HG-10 | Temporal/recurrence/timezone fidelity | NOT RUN | NOT RUN | DST/recurrence/history scenarios |
| HG-11 | Schema/data evolution integrity | NOT RUN | NOT RUN | V1→V2 migration with history/ref proof |
| HG-12 | Recoverability/evidence quality | NOT RUN | NOT RUN | destructive restore + semantic verification |

Allowed result: `PASS`, `PASS-CONDITIONAL`, `HOLD`, `REJECT`, `NOT-APPLICABLE` with rationale.

# 2. Cross-lane hard gates

| Gate | G0 | Neo4j | S0 | pgvector | Evidence requirement |
|---|---|---|---|---|---|
| CG-01 Secondary state not canonical truth | NOT RUN | NOT RUN | NOT RUN | NOT RUN | rebuild/source-of-truth proof |
| CG-02 Deletion/correction/access propagation | NOT RUN | NOT RUN | NOT RUN | NOT RUN | propagation/invalidation evidence |
| CG-03 Non-interference under filtering/ranking | NOT RUN | NOT RUN | NOT RUN | NOT RUN | hidden-result/count/ranking/timing pressure |
| CG-04 Freshness/material basis | NOT RUN | NOT RUN | NOT RUN | NOT RUN | stale projection/material-basis proof |

# 3. Corpus-family coverage

| Corpus | Purpose | PostgreSQL | TypeDB | G lane | S lane | Required before recommendation |
|---|---|---|---|---|---|---|
| C0 | semantic correctness | NOT RUN | NOT RUN | conditional | conditional | YES primary |
| C1 | deep personal history | NOT RUN | NOT RUN | conditional | conditional | YES primary |
| C2 | population/concurrency | NOT RUN | NOT RUN | conditional | conditional | YES primary |
| C3 | governance/disclosure | NOT RUN | NOT RUN | YES when lane executed | YES when lane executed | YES applicable |
| C4 | integration/provider | NOT RUN | NOT RUN | conditional | conditional | YES primary |
| C5 | temporal/calendar | NOT RUN | NOT RUN | conditional | conditional | YES primary |
| C6 | search/retrieval | baseline portion | baseline portion | conditional | NOT RUN | YES S lane if executed |
| C7 | recovery/evolution | NOT RUN | NOT RUN | rebuild/recovery applicable | rebuild applicable | YES primary |

# 4. Scenario execution register

The exact setup/assertions live in `docs/architecture/physical-benchmark-scenario-corpus.md`.

| ID | Short purpose | Primary | G | S | Key gate(s) | PostgreSQL | TypeDB | Secondary result/evidence |
|---|---|---:|---:|---:|---|---|---|---|
| SC-001 | same-base consequential race | M | | | HG-04, HG-06 | NOT RUN | NOT RUN | |
| SC-002 | idempotency conflicting reuse | M | | | HG-04/06 pressure | NOT RUN | NOT RUN | |
| SC-003 | atomic multi-owner mutation | M | | | HG-05 | NOT RUN | NOT RUN | |
| SC-004 | provider partial outcome | M | | | HG-05/07 | NOT RUN | NOT RUN | |
| SC-005 | provider timeout unknown outcome | M | | | HG-06/07 | NOT RUN | NOT RUN | |
| SC-006 | duplicate/out-of-order callback | M | | | HG-06/07 | NOT RUN | NOT RUN | |
| SC-007 | governance revoked during delayed execution | M | | | HG-08 | NOT RUN | NOT RUN | |
| SC-008 | stale derived consequential basis | M | | S | HG-07/08, CG-04 | NOT RUN | NOT RUN | |
| SC-009 | web/mobile offline divergence | M | | | HG-04/06 | NOT RUN | NOT RUN | |
| SC-010 | correction without false rewrite | M | | | HG-06 | NOT RUN | NOT RUN | |
| SC-011 | redaction then old-backup restore | M | | | HG-09, HG-12 | NOT RUN | NOT RUN | |
| SC-012 | NativeRef non-reuse | M | | | HG-02/09 | NOT RUN | NOT RUN | |
| SC-013 | deep-history current-state query | M | | | HG-06 | NOT RUN | NOT RUN | |
| SC-014 | historical reconstruction | M | | | HG-06 | NOT RUN | NOT RUN | |
| SC-015 | typed n-ary relation fidelity | M | G | | HG-03 | NOT RUN | NOT RUN | |
| SC-016 | selective disclosure without source leakage | M | G | S | HG-08, CG-03 | NOT RUN | NOT RUN | |
| SC-017 | search hidden-result non-interference | | | M | CG-03 | | | NOT RUN |
| SC-018 | FTS mixed filter/query | P baseline | | M | CG-03/04 | NOT RUN | NOT RUN | NOT RUN |
| SC-019 | vector recall after security filter | | | M | CG-03/04 | | | NOT RUN |
| SC-020 | stale search/index source | | G | M | CG-02/04 | | | NOT RUN |
| SC-021 | index deletion propagation | | G | M | CG-02/03 | | | NOT RUN |
| SC-022 | recurrence DST spring gap | M | | | HG-10 | NOT RUN | NOT RUN | |
| SC-023 | recurrence DST fall fold | M | | | HG-10 | NOT RUN | NOT RUN | |
| SC-024 | individual recurrence override | M | | | HG-10 | NOT RUN | NOT RUN | |
| SC-025 | provider calendar rebaseline | M | | | HG-02/06/10 | NOT RUN | NOT RUN | |
| SC-026 | stale solver candidate | M | | | HG-07/08 | NOT RUN | NOT RUN | |
| SC-027 | solver UNKNOWN vs INFEASIBLE | representation pressure | | | HG-07 | NOT RUN | NOT RUN | |
| SC-028 | crash commit→external publication | M | | | HG-05/06/12 | NOT RUN | NOT RUN | |
| SC-029 | durable in-flight version change | representation/runtime pressure | | | HG-06/11 | NOT RUN | NOT RUN | |
| SC-030 | mapping evolution with historical refs | M | | | HG-11 | NOT RUN | NOT RUN | |
| SC-031 | backup/restore operational verification | M | | | HG-12 | NOT RUN | NOT RUN | |
| SC-032 | capacity/backpressure | M | G | S | HG-12/operability | NOT RUN | NOT RUN | NOT RUN |
| SC-033 | older effect contract version | M | | | HG-08/11 | NOT RUN | NOT RUN | |
| SC-034 | provider/derived/search unavailable | M | G | S | HG-07, CG-04 | NOT RUN | NOT RUN | NOT RUN |
| SC-035 | graph projection divergence/rebuild | | M | | CG-01..04 | | | NOT RUN |

Legend:

```text
M = mandatory when role/candidate applies
P baseline = primary-store baseline contributes to scenario
conditional = execute if lane is admitted/executed
```

# 5. Qualification tiers

Actual executed counts must be recorded separately from nominal tier labels.

| Tier | PostgreSQL | TypeDB | G lane | S lane | Status rule |
|---|---|---|---|---|---|
| LOW | NOT RUN | NOT RUN | NOT RUN | NOT RUN | must record actual counts |
| BASE | NOT RUN | NOT RUN | NOT RUN | NOT RUN | must record actual counts |
| HIGH | NOT RUN | NOT RUN | NOT RUN | NOT RUN | unexecuted != VERIFIED-RUN |

# 6. Load profiles

| Profile | PostgreSQL | TypeDB | G/S where applicable | Notes |
|---|---|---|---|---|
| LP-01 read-heavy current state | NOT RUN | NOT RUN | NOT RUN | |
| LP-02 mixed interactive | NOT RUN | NOT RUN | NOT RUN | |
| LP-03 write/conflict burst | NOT RUN | NOT RUN | conditional | |
| LP-04 history/reporting | NOT RUN | NOT RUN | conditional | concurrent bounded interactive load |
| LP-05 projection/search churn | primary source pressure | primary source pressure | NOT RUN | deletion/access propagation required |

# 7. Operational / recovery coverage

| Check | PostgreSQL | TypeDB | Neo4j if executed | pgvector/S0 if executed |
|---|---|---|---|---|
| exact version/edition pinned | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| backup created | NOT RUN | NOT RUN | NOT RUN | primary-dependent |
| destructive restore executed | NOT RUN | NOT RUN | NOT RUN | rebuild/primary-dependent |
| semantic post-restore suite | NOT RUN | NOT RUN | projection checks | projection checks |
| redaction anti-resurrection | NOT RUN | NOT RUN | propagation/rebuild | propagation/rebuild |
| V1→V2 evolution | NOT RUN | NOT RUN | projection evolution if material | index rebuild if material |
| failure injection | NOT RUN | NOT RUN | conditional | conditional |
| HA/failover exact topology | HOLD until PM-01 pinning | HOLD until PM-01 pinning | HOLD until PM-01 pinning | primary-dependent |

# 8. Evidence quality checklist

A candidate cannot receive a final recommendation while applicable items are missing without explicitly carrying `HOLD`/conditions.

```text
[ ] LifeOS source commit recorded
[ ] Phase-10 source commits recorded
[ ] exact candidate version/edition/deployment recorded
[ ] hardware/runtime recorded
[ ] mapping revision recorded
[ ] fixture generator + seed recorded
[ ] actual dataset counts recorded
[ ] raw assertion output retained/referenced
[ ] latency/resource raw data retained/referenced
[ ] backup/restore evidence retained/referenced
[ ] migration/evolution evidence retained/referenced
[ ] failure-injection evidence retained/referenced
[ ] manual tuning disclosed
[ ] caveats disclosed
[ ] raw artifacts locations/hashes recorded
[ ] no secret/personal production data committed
```

# 9. Recommendation readiness gate

Before PM-10 recommendation for a primary candidate:

```text
all applicable HG-01..HG-12 resolved
+ mandatory correctness scenarios resolved
+ executed scale/performance evidence honestly labeled
+ recovery/evolution evidence resolved
+ exact subject pinned
+ sensitivity review complete
+ evidence traceable
```

If not, disposition remains `HOLD` or bounded `PASS-CONDITIONAL` as justified.

# 10. Selection readiness

This matrix can support `PREFERRED`; it cannot itself create `SELECTED`.

Selection requires PM-11 explicit user-approved gate and durable result/Physical authority update.