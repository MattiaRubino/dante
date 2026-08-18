# PostgreSQL 18.4 — PM-05 Correctness Evidence Qualification v1

- Candidate: PostgreSQL 18.4 / self-hosted single-node / psycopg 3.3.4
- Mapping: `PM02-PG-001`
- PM-05 disposition: **PRIMARY FINALIST / ADVANCE TO PM-06/07 JOINT**
- Direct LifeOS execution: **NOT RUN**
- Selection: **NONE**

## 1. Qualification thesis

PostgreSQL remains the lowest-risk primary-store candidate after PM-05 because the scenarios that matter most for canonical correctness map onto mature native integrity and transaction primitives without requiring a generic ontology or application-wide consistency emulation layer.

PM-05 does not claim a direct scenario PASS. It concludes that no local PM-05 proof is currently likely to change PostgreSQL's comparative position enough to justify broad execution.

## 2. Primary semantic scenario coverage

### SC-001 / SC-009 — stale-base consequential writes

Evidence path:

```text
explicit MaterialStateRef current pointer
+ expected-state predicate
+ row locking / conditional mutation
+ SERIALIZABLE where predicate invariants require it
```

Classification:

```text
PRIMARY-EVIDENCE-SUFFICIENT
```

### SC-003 — atomic multi-owner mutation

Co-located canonical mutations can share one PostgreSQL transaction. Deferrable constraints and Serializable isolation remain available where the accepted invariant spans multiple rows/tables.

Classification: `PRIMARY-EVIDENCE-SUFFICIENT`.

### SC-010 / SC-014 — correction and historical reconstruction

Stable owner identity + explicit material-state history preserves correction chronology without equating database MVCC metadata with `MaterialStateRef`.

Classification: `PRIMARY-EVIDENCE-SUFFICIENT`.

### SC-012 — NativeRef non-reuse

Owner-specific keys/address anchors are stable and not reused by mapping rule; deletion/redaction retains the minimum permitted tombstone/address continuity where required.

Classification: `PRIMARY-EVIDENCE-SUFFICIENT`, with anti-resurrection deferred to PM-07 finalist qualification.

### SC-015 — typed n-ary relation fidelity

Specific relation/context tables plus explicit Agreement/party-assent structures preserve roles, common terms and material binding. No generic edge root is required.

Classification: `PRIMARY-EVIDENCE-SUFFICIENT`.

### SC-016 — selective disclosure

The mapping supports facet/relation/source-aware disclosure, but database RLS is not treated as complete WL-H12 proof.

Classification:

```text
PRIMARY-EVIDENCE-SUFFICIENT at persistence layer
SYSTEM/FINALIST proof may remain
```

### SC-022 / 023 / 024 — recurrence / timezone / occurrence override

LifeOS temporal semantics remain explicit rather than collapsed to UTC timestamps. PostgreSQL typed temporal/range primitives are supporting mechanisms, not ontology.

Classification: `PRIMARY-EVIDENCE-SUFFICIENT`.

## 3. Known costs

```text
heterogeneous ReferenceAddress needs bounded technical anchors
explicit application history is required
transaction isolation/locking strength must be chosen per invariant
RLS does not automatically solve inference leakage
```

These are mapping/engineering costs, not unknown engine behavior requiring a PM-05 local test.

## 4. PM-06/07 finalist obligations

Carry forward:

```text
SC-011 old-backup anti-resurrection
SC-013 deep-history current-state scale
SC-030 V1 -> V2 mapping evolution
SC-031 destructive restore + semantic verification
SC-032 capacity/backpressure
```

No direct execution is admitted yet. PM-06/07 must first exhaust authoritative scale/recovery/evolution evidence.

## 5. Disposition

```text
PRIMARY FINALIST
YES

ADVANCE
PM-06/07 JOINT FINALIST QUALIFICATION

PM-05 EXECUTION-WORTHY GAP
0

DIRECT HG
NOT RUN

PREFERRED
NO

SELECTED
NO
```
