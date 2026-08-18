# Physical Model Acceptance Test Matrix v1

- Status: **CURRENT — PM-05 COMPLETE / PM-06+PM-07 JOINT NEXT**
- Workstream: `feature/physical-model`
- Primary finalists: **P0 PostgreSQL 18.4 / P1 TypeDB CE 3.12.3**
- Deferred primary challengers: **P2 XTDB 2.1.0 / P3 SurrealDB Community 3.2.3 — NOT REJECTED**
- PM-04B fixture/harness: **NOT ADMITTED / NOT STARTED**
- Direct database execution: **NOT STARTED**
- Technology selection: **NONE**

## 1. Evidence layers

Never collapse these layers:

```text
PM-03 STATIC PREFLIGHT
PASS-CONDITIONAL | HOLD | REJECT

PM-04A EVIDENCE SUFFICIENCY
EXT-SUFFICIENT | MAP-SUFFICIENT | KNOWN-STRUCTURAL-COST |
DEFER-FINALIST | RESIDUAL-GAP | EXECUTION-WORTHY

PM-05 SCENARIO QUALIFICATION
PRIMARY-EVIDENCE-SUFFICIENT | PRIMARY-KNOWN-COST |
SYSTEM-BOUNDARY | PM-06/07-FINALIST | PM-08-SECONDARY |
EXECUTION-WORTHY

DIRECT EXECUTION
NOT RUN until a direct LifeOS run actually exists
```

```text
EVIDENCE-SUFFICIENT != DIRECT PASS
PUBLIC BENCHMARK != LIFEOS BENCHMARK
FINALIST != PREFERRED != SELECTED
DEFER != REJECT
```

## 2. PM-03 static preflight matrix

| Gate | P0 PostgreSQL | P1 TypeDB | P2 XTDB | P3 SurrealDB |
|---|---|---|---|---|
| HG-01 ownership | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-02 reference integrity | PASS-CONDITIONAL | PASS-CONDITIONAL | HOLD | PASS-CONDITIONAL |
| HG-03 typed/n-ary relations | PASS-CONDITIONAL | PASS-CONDITIONAL | HOLD | PASS-CONDITIONAL |
| HG-04 expected-state concurrency | PASS-CONDITIONAL | HOLD | PASS-CONDITIONAL | HOLD |
| HG-05 multi-owner consistency | PASS-CONDITIONAL | HOLD | PASS-CONDITIONAL | HOLD |
| HG-06 history/correction | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-07 state-layer separation | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-08 governance/disclosure | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-09 retention/restore | HOLD | HOLD | HOLD | HOLD |
| HG-10 temporal/recurrence | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-11 evolution | HOLD | HOLD | HOLD | HOLD |
| HG-12 recovery/evidence | HOLD | HOLD | HOLD | HOLD |

Historical evidence: PM-03 overview + candidate preflight records.

## 3. PM-04A evidence-sufficiency matrix

| Gate | P0 PostgreSQL | P1 TypeDB | P2 XTDB | P3 SurrealDB |
|---|---|---|---|---|
| HG-01 | MAP-SUFFICIENT | MAP-SUFFICIENT | MAP-SUFFICIENT | MAP-SUFFICIENT |
| HG-02 | EXT+MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | KNOWN-STRUCTURAL-COST | EXT+MAP-SUFFICIENT |
| HG-03 | EXT+MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | KNOWN-STRUCTURAL-COST | EXT+MAP-SUFFICIENT |
| HG-04 | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / guard condition | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / guard condition |
| HG-05 | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / KNOWN COST | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / KNOWN COST |
| HG-06 | MAP-SUFFICIENT | MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / KNOWN COST |
| HG-07 | MAP-SUFFICIENT | MAP-SUFFICIENT | MAP-SUFFICIENT | MAP-SUFFICIENT |
| HG-08 | MAP-SUFFICIENT / DEFER-FINALIST | MAP-SUFFICIENT / DEFER-FINALIST | MAP-SUFFICIENT / DEFER-FINALIST | MAP-SUFFICIENT / DEFER-FINALIST |
| HG-09 | DEFER-FINALIST | DEFER-FINALIST / KNOWN OPS COST | DEFER-FINALIST | DEFER-FINALIST |
| HG-10 | EXT+MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT |
| HG-11 | DEFER-FINALIST | EXT+DEFER-FINALIST | KNOWN-STRUCTURAL-COST + DEFER-FINALIST | EXT+DEFER-FINALIST |
| HG-12 | EXT+DEFER-FINALIST | KNOWN OPS COST + DEFER-FINALIST | KNOWN OPS/TOPOLOGY COST + DEFER-FINALIST | EXT+DEFER-FINALIST |

PM-04A result:

```text
48/48 cells classified
EXECUTION-WORTHY gaps 0
PM-04B NOT ADMITTED
```

## 4. PM-05 corpus qualification

| Corpus | Disposition |
|---|---|
| C0 semantic correctness | PRIMARY-EVIDENCE-SUFFICIENT |
| C1 deep personal history | PRIMARY-EVIDENCE-SUFFICIENT + PM-06/07-FINALIST for scale |
| C2 population/concurrency | PRIMARY-EVIDENCE-SUFFICIENT + candidate known costs |
| C3 governance/disclosure | persistence layer sufficient / full WL-H12 SYSTEM-BOUNDARY |
| C4 integration/provider | SYSTEM-BOUNDARY |
| C5 temporal/calendar | PRIMARY-EVIDENCE-SUFFICIENT |
| C6 search/retrieval | primary baseline only / PM-08 secondary specialization |
| C7 recovery/evolution | PM-06/07-FINALIST |

## 5. PM-05 scenario qualification

### Primary semantic scenarios

| Scenario | Disposition |
|---|---|
| SC-001 same-base race | PRIMARY-EVIDENCE-SUFFICIENT |
| SC-002 idempotency conflicting reuse | PRIMARY-EVIDENCE-SUFFICIENT |
| SC-003 atomic multi-owner mutation | PRIMARY-EVIDENCE-SUFFICIENT |
| SC-009 stale/offline divergence | PRIMARY-EVIDENCE-SUFFICIENT |
| SC-010 correction without false rewrite | PRIMARY-EVIDENCE-SUFFICIENT |
| SC-012 NativeRef non-reuse | PRIMARY-EVIDENCE-SUFFICIENT |
| SC-014 historical reconstruction | PRIMARY-EVIDENCE-SUFFICIENT |
| SC-015 typed n-ary relation | PRIMARY-EVIDENCE-SUFFICIENT |
| SC-016 selective disclosure | persistence sufficient / SYSTEM-FINALIST remainder |
| SC-022 DST spring gap | PRIMARY-EVIDENCE-SUFFICIENT |
| SC-023 DST fall fold | PRIMARY-EVIDENCE-SUFFICIENT |
| SC-024 occurrence override | PRIMARY-EVIDENCE-SUFFICIENT |

### System/runtime/provider scenarios

```text
SC-004 SC-005 SC-006 SC-007 SC-008
SC-025 SC-026 SC-027 SC-028 SC-029 SC-033 SC-034
```

Disposition: `SYSTEM-BOUNDARY`.

### PM-06/07 finalist scenarios

```text
SC-011 old-backup anti-resurrection
SC-013 deep-history current-state scale
SC-030 mapping/schema evolution
SC-031 destructive restore + semantic verification
SC-032 capacity/backpressure
```

Disposition: `PM-06/07-FINALIST`.

### PM-08 secondary scenarios

```text
SC-017 SC-018 SC-019 SC-020 SC-021 SC-035
```

Disposition: `PM-08-SECONDARY`.

## 6. Primary finalist disposition

### P0 PostgreSQL

```text
PRIMARY FINALIST
ADVANCE PM-06/07 JOINT
PM-05 EXECUTION-WORTHY GAP 0
```

### P1 TypeDB

```text
PRIMARY FINALIST
ADVANCE PM-06/07 JOINT
CONDITION narrow consistency-guard coverage required
PM-05 EXECUTION-WORTHY GAP 0
```

### P2 XTDB

```text
DEFER FROM PRIMARY FINALIST SET
NOT REJECTED
production topology HOLD remains
```

Reopen on documented temporal-dominance, finalist temporal weakness, or material engine/topology change.

### P3 SurrealDB

```text
DEFER FROM PRIMARY FINALIST SET
NOT REJECTED
```

Reopen on demonstrated decision-changing multimodel value, finalist capability gap, or material engine capability change.

## 7. Direct hard-gate matrix

No direct LifeOS correctness/destructive execution has occurred.

| Gate | P0 PostgreSQL | P1 TypeDB | P2 XTDB | P3 SurrealDB |
|---|---|---|---|---|
| HG-01 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-02 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-03 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-04 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-05 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-06 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-07 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-08 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-09 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-10 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-11 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-12 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

## 8. Direct scenario/tier ledger

All direct Phase-10 scenario executions remain `NOT RUN`.

Search/secondary scenarios remain deferred to PM-08.

Qualification tiers:

| Tier | PostgreSQL | TypeDB | XTDB | SurrealDB |
|---|---|---|---|---|
| LOW | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| BASE | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HIGH | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

No tier becomes VERIFIED-RUN without actual materialized counts/raw evidence.

## 9. Operational/recovery ledger

| Item | PostgreSQL | TypeDB | XTDB | SurrealDB |
|---|---|---|---|---|
| exact PM-01 subject | YES | YES | YES / topology HOLD | YES |
| authoritative operations evidence | YES PM-04A | YES PM-04A | YES PM-04A | YES PM-04A |
| benchmark host | HOLD/DORMANT | HOLD/DORMANT | HOLD/DORMANT | HOLD/DORMANT |
| DB deployed by LifeOS benchmark | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| backup created by LifeOS benchmark | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| destructive restore | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| anti-resurrection | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| V1->V2 LifeOS evolution | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| failure injection | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

## 10. PM-06/07 Joint Finalist Qualification acceptance

Finalists:

```text
PostgreSQL 18.4
TypeDB CE 3.12.3
```

PM-06 and PM-07 are collected jointly but scored/reported separately.

PM-06 must cover evidence for:

```text
scale/history efficiency
resource/performance behavior
contention/throughput sensitivity
topology/resource cliffs
```

PM-07 must cover evidence for:

```text
backup/restore
anti-resurrection
schema/data evolution
failure/backpressure
operations/HA/topology conditions
```

Before any direct result:

```text
[ ] residual question is execution-worthy or closure-mandatory
[ ] fresh exact gate approved
[ ] benchmark host frozen
[ ] exact mapping/harness revision frozen
[ ] raw evidence retained
```

## 11. Current state

```text
PM-05 COMPLETE subject to remote QA
PRIMARY FINALISTS PostgreSQL + TypeDB
PM-06/07 JOINT NEXT
PM-04B NOT REOPENED
PM-05 EXECUTION-WORTHY gaps 0
DIRECT HG PASS 0
SELECTION NONE
```
