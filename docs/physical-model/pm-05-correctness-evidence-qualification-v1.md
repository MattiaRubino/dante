# PM-05 Correctness / Destructive Evidence Qualification v1

- Status: **PM-05 COMPLETE / DIRECT EXECUTION NOT RUN**
- Workstream: `feature/physical-model`
- PM-05 PRE-SCOPE: `44d331f12951e2844186e6f5f885e1bcf1559a3b`
- Direct database execution: **NOT RUN**
- Local/server benchmark: **NOT RUN / NOT REQUIRED BY PM-05**
- PM-04B harness: **NOT ADMITTED / NOT STARTED**
- Technology selection: **NONE**

## Purpose

Qualify Phase-10 correctness/destructive scenarios using PM-04A external evidence plus PM-02 mapping reasoning, and carry only decision-relevant unresolved work forward.

```text
EVIDENCE-QUALIFIED != DIRECT PASS
DEFER != REJECT
FINALIST != PREFERRED != SELECTED
```

## Scenario classes

- `PRIMARY-EVIDENCE-SUFFICIENT` — primary-store semantics sufficiently established for current comparison.
- `PRIMARY-KNOWN-COST` — structural burden already known; a local test cannot remove it.
- `SYSTEM-BOUNDARY` — end-to-end invariant belongs above the database-only layer.
- `PM-06/07-FINALIST` — scale/recovery/evolution evidence belongs only to finalists.
- `PM-08-SECONDARY` — specialist search/vector/graph scenario.
- `EXECUTION-WORTHY` — unresolved, ranking-critical and directly test-resolvable.

## Corpus qualification

| Corpus | Disposition |
|---|---|
| C0 semantic correctness | PRIMARY-EVIDENCE-SUFFICIENT |
| C1 deep history | PRIMARY-EVIDENCE-SUFFICIENT + PM-06/07-FINALIST for scale |
| C2 population/concurrency | PRIMARY-EVIDENCE-SUFFICIENT + known candidate costs |
| C3 governance/disclosure | persistence evidence sufficient; full WL-H12 SYSTEM-BOUNDARY |
| C4 integration/provider | SYSTEM-BOUNDARY |
| C5 temporal/calendar | PRIMARY-EVIDENCE-SUFFICIENT |
| C6 search/retrieval | primary baseline only; specialist work PM-08 |
| C7 recovery/evolution | PM-06/07-FINALIST |

## Scenario qualification

### Primary semantic set

```text
SC-001 SC-002 SC-003 SC-009 SC-010 SC-012
SC-014 SC-015 SC-016 SC-022 SC-023 SC-024
```

Disposition: `PRIMARY-EVIDENCE-SUFFICIENT`; execution-worthy now: **NO**.

### System/runtime/provider set

```text
SC-004 SC-005 SC-006 SC-007 SC-008
SC-025 SC-026 SC-027 SC-028 SC-029 SC-033 SC-034
```

Disposition: `SYSTEM-BOUNDARY`; primary-store requirements remain, but four-engine local DB testing is not justified.

### PM-06/07 finalist set

```text
SC-011 redaction + old backup
SC-013 deep-history current-state scale
SC-030 V1 -> V2 evolution
SC-031 backup/restore semantic verification
SC-032 capacity/backpressure
```

Disposition: `PM-06/07-FINALIST`; direct execution now: **NOT ADMITTED**.

### PM-08 secondary set

```text
SC-017 SC-018 SC-019 SC-020 SC-021 SC-035
```

Disposition: `PM-08-SECONDARY`.

## Candidate disposition

### P0 PostgreSQL 18.4

```text
PRIMARY FINALIST
ADVANCE TO PM-06/07 JOINT
NOT PREFERRED
NOT SELECTED
```

No candidate-specific semantic uncertainty remains sufficiently material to justify PM-05 local execution. Remaining work is finalist scale/recovery/evolution qualification.

### P1 TypeDB CE 3.12.3

```text
PRIMARY FINALIST
ADVANCE TO PM-06/07 JOINT
CONDITION: narrow consistency-guard coverage remains required
NOT PREFERRED
NOT SELECTED
```

TypeDB's relation/role/n-ary fit remains a genuine comparative strength. Snapshot-isolation hardening is now a known design/operability cost rather than an unknown primitive.

### P2 XTDB 2.1.0

```text
DEFER FROM PRIMARY FINALIST SET
NOT REJECTED
NOT SELECTED
```

Native bitemporality remains valuable, but no-FK/no-general-uniqueness, manual integrity discipline, non-interactive transaction ergonomics and production-topology sensitivity create enough primary-store burden that no PM-05 local test is likely to reverse the aggregate comparison.

Reopen if native bitemporality becomes decision-dominant, PostgreSQL/TypeDB exposes a material temporal weakness, or XTDB integrity/topology capabilities materially change.

### P3 SurrealDB Community 3.2.3

```text
DEFER FROM PRIMARY FINALIST SET
NOT REJECTED
NOT SELECTED
```

Multimodel consolidation is credible, but no unique primary-store benefit currently offsets its guard/history/operational discipline strongly enough to justify finalist scope.

Reopen if multimodel consolidation becomes decision-changing, PostgreSQL/TypeDB exposes a material capability gap, or relevant engine capabilities materially change.

## Primary finalist set

```text
P0 PostgreSQL 18.4
P1 TypeDB CE 3.12.3

DEFERRED / NOT REJECTED
P2 XTDB 2.1.0
P3 SurrealDB Community 3.2.3
```

## Execution admission

```text
PM-05 EXECUTION-WORTHY GAPS  0
PM-04B                        NOT REOPENED
DATABASE/HARNESS              NOT STARTED
BENCHMARK HOST                HOLD / DORMANT
DIRECT HG PASS                0
```

## PM-06 + PM-07 Joint Finalist Qualification

PM-06 and PM-07 remain separate result layers but are operated as one evidence campaign:

```text
PM-06
scale / performance / resource / saturation

PM-07
recovery / restore / evolution / failure / operations
```

Shared evidence collection is allowed where sources/topology/workload overlap. Performance may never compensate for a recovery/evolution failure.

Default order remains evidence-first; targeted direct proof is admitted only if a residual question can materially change the recommendation.

## Next

```text
PM-05 COMPLETE subject to remote QA
PRIMARY FINALISTS PostgreSQL + TypeDB
PM-06/07 JOINT NEXT after fresh exact gate
PM-08+ NOT STARTED
SELECTION NONE
```
