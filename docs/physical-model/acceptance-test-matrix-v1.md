# Physical Model Acceptance Test Matrix v1

- Status: **CURRENT — PM-03 STATIC PREFLIGHT COMPLETE / EXECUTION NOT STARTED**
- Workstream: `feature/physical-model`
- Primary candidates: P0 PostgreSQL 18.4, P1 TypeDB CE 3.12.3, P2 XTDB 2.1.0, P3 SurrealDB Community 3.2.3
- Database/harness execution: **NOT STARTED**
- Technology selection: **NONE**

## 1. Result-layer rule

This matrix separates static mapping review from executable hard-gate evidence.

```text
PM-03 PREFLIGHT
PASS-CONDITIONAL | HOLD | REJECT

!=

EXECUTED HARD-GATE RESULT
NOT RUN until direct scenario evidence exists
```

A preflight PASS-CONDITIONAL never authorizes performance scoring.

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

Preflight evidence:

- `pm-03-semantic-hard-gate-preflight-v1.md`;
- `preflight/postgresql-18.4-v1.md`;
- `preflight/typedb-3.12.3-v1.md`;
- `preflight/xtdb-2.1.0-v1.md`;
- `preflight/surrealdb-3.2.3-v1.md`.

## 3. Executed primary hard-gate matrix

No candidate has executed the mandatory correctness/destructive corpus yet.

| Gate | P0 PostgreSQL | P1 TypeDB | P2 XTDB | P3 SurrealDB | Required direct evidence |
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

## 4. Candidate-specific executable priorities

### P0 PostgreSQL

```text
wrong-family/dangling heterogeneous anchor
same-base race
predicate write-skew
Read-Committed negative control
Serializable/locking positive control
RLS/query leakage where applicable
```

### P1 TypeDB

```text
wrong role/player/address family
same-base race
snapshot write-skew negative control
shared consistency-guard positive control
relation/cardinality history
```

### P2 XTDB

```text
missing/wrong-family reference
cardinality/uniqueness race
incomplete ASSERT negative control
expected-state ASSERT race
complex non-interactive governed mutation
```

### P3 SurrealDB

```text
invalid typed record union/reference
binary relation vs n-ary Agreement
snapshot write-skew negative control
shared consistency-guard positive control
record-user/system-user disclosure boundary
```

## 5. Cross-lane hard gates

Secondary lanes remain deferred to PM-08.

| Gate | G0 | Neo4j | S0 | pgvector/dedicated search | Status |
|---|---|---|---|---|---|
| CG-01 secondary not canonical truth | NOT RUN | NOT RUN | NOT RUN | NOT RUN | future |
| CG-02 deletion/correction/access propagation | NOT RUN | NOT RUN | NOT RUN | NOT RUN | future |
| CG-03 non-interference filtering/ranking | NOT RUN | NOT RUN | NOT RUN | NOT RUN | future |
| CG-04 freshness/material basis | NOT RUN | NOT RUN | NOT RUN | NOT RUN | future |

## 6. Corpus-family execution register

| Corpus | Purpose | P0 | P1 | P2 | P3 | Required before recommendation |
|---|---|---|---|---|---|---|
| C0 | semantic correctness | NOT RUN | NOT RUN | NOT RUN | NOT RUN | YES |
| C1 | deep personal history | NOT RUN | NOT RUN | NOT RUN | NOT RUN | YES |
| C2 | population/concurrency | NOT RUN | NOT RUN | NOT RUN | NOT RUN | YES |
| C3 | governance/disclosure | NOT RUN | NOT RUN | NOT RUN | NOT RUN | YES |
| C4 | integration/provider | NOT RUN | NOT RUN | NOT RUN | NOT RUN | YES |
| C5 | temporal/calendar | NOT RUN | NOT RUN | NOT RUN | NOT RUN | YES |
| C6 | search/retrieval primary baseline | NOT RUN | NOT RUN | NOT RUN | NOT RUN | primary portion |
| C7 | recovery/evolution | NOT RUN | NOT RUN | NOT RUN | NOT RUN | YES |

## 7. Core scenario execution register

All scenarios remain `NOT RUN`.

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

## 8. Qualification tiers

| Tier | P0 | P1 | P2 | P3 |
|---|---|---|---|---|
| LOW | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| BASE | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HIGH | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

No tier label may be called verified without actual materialized counts and raw run evidence.

## 9. Load profiles

| Profile | P0 | P1 | P2 | P3 |
|---|---|---|---|---|
| LP-01 read-heavy current state | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| LP-02 mixed interactive | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| LP-03 write/conflict burst | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| LP-04 history/reporting | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| LP-05 projection/search churn | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

## 10. Operational/recovery register

| Check | P0 | P1 | P2 | P3 |
|---|---|---|---|---|
| exact qualification subject pinned | YES PM-01 | YES PM-01 | YES PM-01 / production topology HOLD | YES PM-01 |
| benchmark host frozen | HOLD | HOLD | HOLD | HOLD |
| database deployed | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| backup created | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| destructive restore | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| semantic post-restore suite | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| redaction anti-resurrection | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| V1 -> V2 evolution | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| failure injection | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| exact HA/failover topology | HOLD | HOLD | HOLD | HOLD / Community single-node subject only |

## 11. Evidence quality checklist

Before any candidate hard-gate PASS or recommendation:

```text
[ ] benchmark host/runtime frozen
[ ] LifeOS/Phase-10/mapping commits recorded
[ ] exact candidate version/edition/deployment recorded
[ ] fixture generator + seed recorded
[ ] actual dataset counts recorded
[ ] raw assertion output retained
[ ] concurrency negative and positive controls retained
[ ] backup/restore evidence retained
[ ] evolution evidence retained
[ ] failure-injection evidence retained
[ ] manual tuning disclosed
[ ] raw artifact hashes/locations recorded
[ ] no real personal data/secrets in fixtures
```

## 12. PM-03 advancement state

```text
P0 PostgreSQL
ADVANCE

P1 TypeDB
ADVANCE WITH CONCURRENCY HOLD

P2 XTDB
ADVANCE WITH REFERENCE/CONSTRAINT HOLD
production topology HOLD

P3 SurrealDB
ADVANCE WITH CONCURRENCY HOLD

STATIC REJECTS
0

EXECUTED HG PASS
0

SELECTION
NONE
```

The next executable phase must resolve uncertainty through evidence rather than converting these preflight dispositions into paper PASS.
