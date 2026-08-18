# SurrealDB Community 3.2.3 — PM-03 Semantic Preflight v1

- Candidate: SurrealDB Community 3.2.3 / single-node RocksDB / Python SDK 2.0.0
- Mapping: `PM02-SDB-001`
- Status: **STATIC PREFLIGHT COMPLETE / EXECUTED HG NOT RUN**
- Selection: **NONE**

## 1. Verdict

```text
PASS-CONDITIONAL  HG-01 HG-02 HG-03 HG-06 HG-07 HG-08 HG-10
HOLD              HG-04 HG-05 HG-09 HG-11 HG-12
REJECT            none

ADVANCEMENT
YES — WITH CONCURRENCY HOLD
```

SurrealDB survives the static preflight only because PM-02 deliberately constrains its multimodel flexibility. The main unresolved issue is write-skew under snapshot isolation, not graph/document expressiveness.

## 2. HG-01 — PASS-CONDITIONAL

Canonical tables remain `SCHEMAFULL`, owner-specific and semantically typed. Flexible nested content is bounded to already-permitted provider/low-consequence/specialist use.

Any later fallback to a canonical SCHEMALESS object/property bag would invalidate this result.

## 3. HG-02 — PASS-CONDITIONAL

Homogeneous references use typed record fields. Heterogeneous references use bounded typed record unions/links or separate narrow address records where native/scoped/material/external spaces differ.

Direct proof must show a generic record reference cannot accept an ineligible table/family and that material/external IDs do not collapse into ordinary owner record IDs semantically.

## 4. HG-03 — PASS-CONDITIONAL

SurrealDB relation tables are binary `in`/`out` structures, so PM-02 correctly limits graph edges to true binary relation families.

N-ary/material Agreement uses a normal contextual record plus party-assent structures bound to one common terms MaterialStateRef.

This avoids the generic graph trap while still using candidate-native relation traversal where appropriate.

## 5. HG-04 — HOLD

SurrealDB documents snapshot isolation with write-write conflict detection. That does not alone establish predicate serializability.

PM-02 introduces a narrow `consistency_guard` record that all transactions sharing one invariant boundary must mutate.

Required proof:

```text
negative control
T1 and T2 update disjoint semantic records under same predicate without guard
-> demonstrate anomaly can be detected/represented by oracle if allowed

positive control
same invariant but both mutate guard G
-> incompatible pair cannot both silently commit
```

Until this is executed on Community 3.2.3/RocksDB, HG-04 remains HOLD.

## 6. HG-05 — HOLD

SurrealDB supports multi-statement transactions with rollback on failure, so obvious co-located atomic updates are plausible.

The unresolved part is predicate/write-skew consistency across disjoint owners under snapshot isolation. The same guard proof is mandatory before representative multi-owner invariants receive credit.

External/provider effects remain staged/reconciled.

## 7. HG-06 — PASS-CONDITIONAL

Explicit material-state records and current-state links preserve semantic history independent of changefeeds. Changefeeds are intentionally limited to propagation/sync/observability roles.

This is essential because bounded operational change history must not become LifeOS material truth by accident.

SC-010/013/014 remain direct proof obligations.

## 8. HG-07 — PASS-CONDITIONAL

Canonical, material history, provider, projection and runtime/security roles remain explicitly separated even when co-located in one SurrealDB database.

Record links do not imply semantic equivalence of those layers.

## 9. HG-08 — PASS-CONDITIONAL

SurrealDB table/field permissions provide useful enforcement primitives, but PM-03 does not equate them with Domain Authority/Consent/Visibility.

The mapping preserves richer disclosure semantics in canonical state and treats database permissions as one possible technical enforcement layer.

Direct pressure must include:

- hidden edge existence;
- graph traversal leakage;
- count/ranking differences;
- field/source leakage;
- system-user path versus record-user permission behavior;
- stale materialized projection after access change.

## 10. HG-09 — HOLD

Explicit tombstone/material-history records can prevent automatic graph-edge cleanup from falsifying consequential history, but destructive restore/anti-resurrection has not run.

PM-07 must verify deleted/redacted payload does not silently return after restoring an older snapshot while still retaining only permitted minimal reference continuity.

## 11. HG-10 — PASS-CONDITIONAL

The mapping does not rely on database datetime alone. Date-only, floating wall-clock, named-zone wall-clock, accepted historical resolution, instant, interval, duration and recurrence families remain explicit structures.

Graph relations and datetime functions do not redefine recurrence or Occurrence identity.

## 12. HG-11 — HOLD

`SCHEMAFULL` provides an explicit evolution surface, but actual V1 -> V2 migration with historical/reference integrity has not been executed.

The candidate must prove it can evolve without switching canonical tables to flexible fallback.

## 13. HG-12 — HOLD

No exact executable deployment, host freeze, backup, destructive restore or semantic verification exists yet.

Community single-node gets no credit for Enterprise/Cloud distributed HA capability.

## 14. Permission-model caution

Official SurrealDB documentation states table permissions are evaluated for record users/guests, while system users at root/namespace/database level are governed by roles instead.

Therefore a future backend using privileged system credentials cannot claim WL-H12 merely because table permissions exist. LifeOS enforcement architecture must intentionally choose where recipient-context filtering occurs and test that trust boundary.

This is a hardening condition, not a current REJECT.

## 15. Destructive mutations

```text
SDB-M01 canonical SCHEMALESS object root                 REJECTED BY MAPPING
SDB-M02 universal graph edge(type,payload)              REJECTED BY MAPPING
SDB-M03 binary edge used to infer n-ary Agreement       MUST FAIL ORACLE
SDB-M04 record/version metadata becomes MaterialStateRef INVALID
SDB-M05 changefeed becomes canonical material history   INVALID
SDB-M06 snapshot write-skew without guard               MUST FAIL NEGATIVE CONTROL
SDB-M07 same invariant guard omitted on one writer      INVALID IMPLEMENTATION
SDB-M08 record permission becomes Domain Authority      INVALID
SDB-M09 missing edge -> false/nonexistent               MUST FAIL ORACLE
SDB-M10 automatic edge deletion erases required history MUST FAIL ORACLE
```

## 16. PM-04/05 priority pack

1. implement SCHEMAFULL owner/reference subset;
2. prove invalid typed record union/reference rejection;
3. prove binary relation versus n-ary Agreement distinction;
4. run write-skew negative control and guard positive control;
5. run current/history/changefeed-separation tests;
6. run selective disclosure through record/system-user trust boundaries;
7. run temporal/lazy Occurrence tests;
8. later run V1->V2 and destructive restore.

## 17. Official capability evidence

- architecture/isolation/topology: `https://surrealdb.com/docs/architecture`
- SCHEMAFULL + permissions: `https://surrealdb.com/docs/reference/query-language/statements/define/table`
- binary relation tables / typed endpoints: `https://surrealdb.com/docs/reference/query-language/statements/relate`
- transactions: `https://surrealdb.com/docs/learn/querying/concepts-and-guides/transactions`

Official docs establish feature shape only. The guard and LifeOS disclosure/history behavior remain unexecuted.
