# Physical Model Acceptance Test Matrix v1

- Status: **CURRENT — PM-04A EVIDENCE SUFFICIENCY COMPLETE / DIRECT EXECUTION NOT STARTED**
- Workstream: `feature/physical-model`
- Primary candidates: P0 PostgreSQL 18.4, P1 TypeDB CE 3.12.3, P2 XTDB 2.1.0, P3 SurrealDB Community 3.2.3
- PM-04A evidence review: **COMPLETE**
- PM-04B fixture/harness: **NOT ADMITTED / NOT STARTED**
- Database execution: **NOT STARTED**
- Technology selection: **NONE**

## 1. Result-layer rule

This matrix separates three evidence layers.

```text
PM-03 STATIC PREFLIGHT
PASS-CONDITIONAL | HOLD | REJECT

PM-04A EVIDENCE SUFFICIENCY
EXT-SUFFICIENT | MAP-SUFFICIENT | KNOWN-STRUCTURAL-COST |
DEFER-FINALIST | RESIDUAL-GAP | EXECUTION-WORTHY

DIRECT EXECUTION
NOT RUN until a direct scenario/run actually exists
```

These layers must never be collapsed.

```text
PM-04A MAP-SUFFICIENT
!= EXECUTED HG PASS

PUBLIC BENCHMARK
!= LIFEOS BENCHMARK

NOT RUN
!= PASS
```

## 2. PM-03 static preflight matrix

| Gate | Meaning | P0 PostgreSQL | P1 TypeDB | P2 XTDB | P3 SurrealDB |
|---|---|---|---|---|---|
| HG-01 | Semantic ownership preservation | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-02 | Reference-family integrity | PASS-CONDITIONAL | PASS-CONDITIONAL | HOLD | PASS-CONDITIONAL |
| HG-03 | Typed/n-ary relation fidelity | PASS-CONDITIONAL | PASS-CONDITIONAL | HOLD | PASS-CONDITIONAL |
| HG-04 | Expected-state consequential concurrency | PASS-CONDITIONAL | HOLD | PASS-CONDITIONAL | HOLD |
| HG-05 | Multi-owner consistency truthfulness | PASS-CONDITIONAL | HOLD | PASS-CONDITIONAL | HOLD |
| HG-06 | History/correction/reconciliation | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-07 | State-layer separation | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-08 | Governance/selective disclosure | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-09 | Retention/redaction/tombstone/restore | HOLD | HOLD | HOLD | HOLD |
| HG-10 | Temporal/recurrence/timezone fidelity | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-11 | Schema/data evolution integrity | HOLD | HOLD | HOLD | HOLD |
| HG-12 | Recoverability/evidence quality | HOLD | HOLD | HOLD | HOLD |

PM-03 evidence:

- `pm-03-semantic-hard-gate-preflight-v1.md`;
- `preflight/postgresql-18.4-v1.md`;
- `preflight/typedb-3.12.3-v1.md`;
- `preflight/xtdb-2.1.0-v1.md`;
- `preflight/surrealdb-3.2.3-v1.md`.

## 3. PM-04A evidence-sufficiency matrix

This is a comparative sufficiency matrix, not a direct test result.

| Gate | Meaning | P0 PostgreSQL | P1 TypeDB | P2 XTDB | P3 SurrealDB |
|---|---|---|---|---|---|
| HG-01 | Semantic ownership preservation | MAP-SUFFICIENT | MAP-SUFFICIENT | MAP-SUFFICIENT | MAP-SUFFICIENT |
| HG-02 | Reference-family integrity | EXT+MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | KNOWN-STRUCTURAL-COST | EXT+MAP-SUFFICIENT |
| HG-03 | Typed/n-ary relation fidelity | EXT+MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | KNOWN-STRUCTURAL-COST | EXT+MAP-SUFFICIENT |
| HG-04 | Expected-state consequential concurrency | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / guard condition | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / guard condition |
| HG-05 | Multi-owner consistency truthfulness | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / KNOWN COST | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / KNOWN COST |
| HG-06 | History/correction/reconciliation | MAP-SUFFICIENT | MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / KNOWN COST |
| HG-07 | State-layer separation | MAP-SUFFICIENT | MAP-SUFFICIENT | MAP-SUFFICIENT | MAP-SUFFICIENT |
| HG-08 | Governance/selective disclosure | MAP-SUFFICIENT / DEFER-FINALIST system proof | MAP-SUFFICIENT / DEFER-FINALIST system proof | MAP-SUFFICIENT / DEFER-FINALIST system proof | MAP-SUFFICIENT / DEFER-FINALIST system proof |
| HG-09 | Retention/redaction/tombstone/restore | DEFER-FINALIST | DEFER-FINALIST / KNOWN OPS COST | DEFER-FINALIST | DEFER-FINALIST |
| HG-10 | Temporal/recurrence/timezone fidelity | EXT+MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT |
| HG-11 | Schema/data evolution integrity | DEFER-FINALIST | EXT+DEFER-FINALIST | KNOWN-STRUCTURAL-COST + DEFER-FINALIST | EXT+DEFER-FINALIST |
| HG-12 | Recoverability/evidence quality | EXT+DEFER-FINALIST | KNOWN OPS COST + DEFER-FINALIST | KNOWN OPS/TOPOLOGY COST + DEFER-FINALIST | EXT+DEFER-FINALIST |

PM-04A evidence:

- `pm-04-external-evidence-sufficiency-v1.md`;
- `evidence/postgresql-18.4-v1.md`;
- `evidence/typedb-3.12.3-v1.md`;
- `evidence/xtdb-2.1.0-v1.md`;
- `evidence/surrealdb-3.2.3-v1.md`.

### PM-04A execution admission

```text
EXECUTION-WORTHY gaps       0
FULL LOCAL BENCHMARK        NOT ADMITTED
TARGETED LOCAL PROOFS       0 ADMITTED
PM-04B HARNESS              NOT ADMITTED / NOT STARTED
BENCHMARK HOST              HOLD / DORMANT
SELECTION                   NONE
```

`HOLD / DORMANT` means the host requirement still exists before a direct run, but it does not block evidence-only work.

## 4. Direct primary hard-gate matrix

No candidate has executed a direct LifeOS correctness/destructive corpus yet.

| Gate | P0 PostgreSQL | P1 TypeDB | P2 XTDB | P3 SurrealDB | Direct evidence if later admitted |
|---|---|---|---|---|---|
| HG-01 | NOT RUN | NOT RUN | NOT RUN | NOT RUN | C0 reverse mapping / owner reconstruction |
| HG-02 | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NativeRef/ScopedRecordRef/MaterialStateRef/ExternalRef negative tests |
| HG-03 | NOT RUN | NOT RUN | NOT RUN | NOT RUN | role/cardinality/n-ary relation oracle |
| HG-04 | NOT RUN | NOT RUN | NOT RUN | NOT RUN | stale-base race + explicit conflict evidence |
| HG-05 | NOT RUN | NOT RUN | NOT RUN | NOT RUN | atomic/staged multi-owner failure evidence |
| HG-06 | NOT RUN | NOT RUN | NOT RUN | NOT RUN | current + historical oracle |
| HG-07 | NOT RUN | NOT RUN | NOT RUN | NOT RUN | canonical/history/derived/provider separation |
| HG-08 | NOT RUN | NOT RUN | NOT RUN | NOT RUN | governance/disclosure/non-interference corpus |
| HG-09 | NOT RUN | NOT RUN | NOT RUN | NOT RUN | redaction + old-backup anti-resurrection |
| HG-10 | NOT RUN | NOT RUN | NOT RUN | NOT RUN | DST/recurrence/lazy-Occurrence corpus |
| HG-11 | NOT RUN | NOT RUN | NOT RUN | NOT RUN | V1 -> V2 migration with historical refs |
| HG-12 | NOT RUN | NOT RUN | NOT RUN | NOT RUN | destructive restore + semantic verification |

Direct execution remains available as last-mile evidence if a later gate admits it. PM-04A does not erase Phase-10 scenarios; it prevents unnecessary execution breadth.

## 5. Candidate-specific residual pressure

These are **not automatically executable priorities** after PM-04A.

### P0 PostgreSQL

```text
heterogeneous-anchor mapping complexity
transaction-strength selection per consequential operation
RLS/query/system non-interference boundary
finalist restore/evolution rehearsal if required
```

PM-04A: no execution-worthy PostgreSQL gap now.

### P1 TypeDB

```text
snapshot isolation remains engine model
shared consistency-guard coverage/scoping is mandatory
self-hosted backup/operations burden
finalist restore/evolution rehearsal if required
```

PM-04A: guard primitive path is reasoned/documented sufficiently for current comparison; execution may reopen only if ranking becomes dependent on it.

### P2 XTDB

```text
no native FK
no uniqueness beyond _id
manual ASSERT/ID integrity discipline
non-interactive transaction ergonomics
production topology/single-writer sensitivity
finalist restore/evolution rehearsal if required
```

PM-04A: these are known structural costs. A local test cannot remove them.

### P3 SurrealDB

```text
snapshot isolation remains engine model
shared consistency-guard coverage/scoping is mandatory
explicit material history remains required
system disclosure boundary
finalist restore/evolution rehearsal if required
```

PM-04A: no execution-worthy SurrealDB gap now.

## 6. Cross-lane hard gates

Secondary lanes remain deferred to PM-08.

| Gate | G0 | Neo4j | S0 | pgvector/dedicated search | Status |
|---|---|---|---|---|---|
| CG-01 secondary not canonical truth | NOT RUN | NOT RUN | NOT RUN | NOT RUN | future |
| CG-02 deletion/correction/access propagation | NOT RUN | NOT RUN | NOT RUN | NOT RUN | future |
| CG-03 non-interference filtering/ranking | NOT RUN | NOT RUN | NOT RUN | NOT RUN | future |
| CG-04 freshness/material basis | NOT RUN | NOT RUN | NOT RUN | NOT RUN | future |

## 7. Corpus-family direct execution register

External/mapping evidence is tracked separately; this table records direct execution only.

| Corpus | Purpose | P0 | P1 | P2 | P3 | Qualification obligation |
|---|---|---|---|---|---|---|
| C0 | semantic correctness | NOT RUN | NOT RUN | NOT RUN | NOT RUN | evidence-qualified in PM-05; direct only if needed |
| C1 | deep personal history | NOT RUN | NOT RUN | NOT RUN | NOT RUN | evidence-qualified in PM-05; direct only if needed |
| C2 | population/concurrency | NOT RUN | NOT RUN | NOT RUN | NOT RUN | evidence-qualified in PM-05; direct only if decision-relevant |
| C3 | governance/disclosure | NOT RUN | NOT RUN | NOT RUN | NOT RUN | system/finalist proof may remain |
| C4 | integration/provider | NOT RUN | NOT RUN | NOT RUN | NOT RUN | evidence-qualified in PM-05 |
| C5 | temporal/calendar | NOT RUN | NOT RUN | NOT RUN | NOT RUN | evidence-qualified in PM-05 |
| C6 | search/retrieval primary baseline | NOT RUN | NOT RUN | NOT RUN | NOT RUN | primary portion; secondary PM-08 |
| C7 | recovery/evolution | NOT RUN | NOT RUN | NOT RUN | NOT RUN | finalist direct obligations may remain |

## 8. Core scenario direct execution register

All scenarios remain `NOT RUN` because no direct execution has occurred.

| ID | Purpose | Key gate(s) | P0 | P1 | P2 | P3 |
|---|---|---|---|---|---|---|
| SC-001 | same-base consequential race | HG-04/06 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-002 | idempotency conflicting reuse | HG-04/06 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-003 | atomic multi-owner mutation | HG-05 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-004 | provider partial outcome | HG-05/07 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-005 | provider timeout unknown outcome | HG-06/07 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-006 | duplicate/out-of-order callback | HG-06/07 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-007 | governance revoked during delayed execution | HG-08 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-008 | stale derived consequential basis | HG-07/08 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-009 | web/mobile offline divergence | HG-04/06 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-010 | correction without false rewrite | HG-06 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-011 | redaction then old-backup restore | HG-09/12 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-012 | NativeRef non-reuse | HG-02/09 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-013 | deep-history current-state query | HG-06 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-014 | historical reconstruction | HG-06 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-015 | typed n-ary relation fidelity | HG-03 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-016 | selective disclosure without source leakage | HG-08 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-022 | recurrence DST spring gap | HG-10 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-023 | recurrence DST fall fold | HG-10 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-024 | individual recurrence override | HG-10 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-025 | provider calendar rebaseline | HG-02/06/10 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-026 | stale solver candidate | HG-07/08 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-027 | solver UNKNOWN vs INFEASIBLE | HG-07 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-028 | crash commit -> external publication | HG-05/06/12 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-029 | durable in-flight version change | HG-06/11 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-030 | mapping evolution with historical refs | HG-11 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-031 | backup/restore operational verification | HG-12 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-032 | capacity/backpressure | HG-12/operability | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-033 | older effect-contract version | HG-08/11 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| SC-034 | provider/derived/search unavailable | HG-07 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

Search/secondary-only scenarios SC-017..SC-021 and SC-035 remain deferred until applicable PM-08 lanes are admitted.

## 9. Qualification tiers

| Tier | P0 | P1 | P2 | P3 |
|---|---|---|---|---|
| LOW | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| BASE | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HIGH | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

No tier label may be called verified without actual materialized counts and raw run evidence. PM-06 may leave these `NOT RUN` if external evidence is sufficient and a local performance comparison cannot materially change the recommendation.

## 10. Load profiles

| Profile | P0 | P1 | P2 | P3 |
|---|---|---|---|---|
| LP-01 read-heavy current state | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| LP-02 mixed interactive | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| LP-03 write/conflict burst | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| LP-04 history/reporting | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| LP-05 projection/search churn | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

## 11. Operational/recovery register

| Check | P0 | P1 | P2 | P3 |
|---|---|---|---|---|
| exact qualification subject pinned | YES PM-01 | YES PM-01 | YES PM-01 / production topology HOLD | YES PM-01 |
| authoritative recovery/evolution docs reviewed | YES PM-04A | YES PM-04A | YES PM-04A | YES PM-04A |
| benchmark host frozen | HOLD / DORMANT | HOLD / DORMANT | HOLD / DORMANT | HOLD / DORMANT |
| database deployed | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| backup created by LifeOS benchmark | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| destructive restore | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| semantic post-restore suite | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| redaction anti-resurrection | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| V1 -> V2 LifeOS evolution | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| failure injection | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| exact production HA/failover topology | future sensitivity | future sensitivity | HOLD | Community single-node current subject |

## 12. Evidence quality checklist

For an external/mapping evidence claim:

```text
[x] exact candidate subject identified
[x] source class disclosed
[x] official/current primary sources preferred
[x] vendor benchmark/case study not treated as neutral direct proof
[x] structural limitation retained as cost/condition
[x] external evidence kept separate from direct execution state
```

Before any **direct** hard-gate PASS or measured benchmark claim:

```text
[ ] benchmark host/runtime frozen
[ ] LifeOS/Phase-10/mapping commits recorded
[ ] exact candidate version/edition/deployment recorded
[ ] fixture generator + seed recorded where applicable
[ ] actual dataset counts recorded where applicable
[ ] raw assertion output retained
[ ] concurrency negative and positive controls retained where applicable
[ ] backup/restore evidence retained where applicable
[ ] evolution evidence retained where applicable
[ ] failure-injection evidence retained where applicable
[ ] manual tuning disclosed
[ ] raw artifact hashes/locations recorded
[ ] no real personal data/secrets in fixtures
```

## 13. Current advancement state

```text
P0 PostgreSQL
CURRENT COMPARATIVE LEADER
NO EXECUTION-WORTHY GAP

P1 TypeDB
PRINCIPAL SEMANTIC CHALLENGER
CONCURRENCY UNKNOWN NARROWED TO DOCUMENTED GUARD CONDITION/COST
NO EXECUTION-WORTHY GAP

P2 XTDB
TEMPORAL CHALLENGER
REFERENCE/CARDINALITY UNKNOWN NARROWED TO KNOWN STRUCTURAL COST
PRODUCTION TOPOLOGY HOLD
NO EXECUTION-WORTHY GAP

P3 SurrealDB
MULTIMODEL CHALLENGER
CONCURRENCY UNKNOWN NARROWED TO DOCUMENTED GUARD CONDITION/COST
NO EXECUTION-WORTHY GAP

PM-04B
NOT ADMITTED

DIRECT HG PASS
0

SELECTION
NONE
```

Counts/classes are not PM-09 scores. The next phase must qualify scenario/corpus evidence without manufacturing local runs that cannot change the decision.
