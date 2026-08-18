# PostgreSQL 18.4 — PM-03 Semantic Preflight v1

- Candidate: PostgreSQL 18.4 / self-hosted single-node / psycopg 3.3.4
- Mapping: `PM02-PG-001`
- Status: **STATIC PREFLIGHT COMPLETE / EXECUTED HG NOT RUN**
- Selection: **NONE**

## 1. Verdict

```text
PASS-CONDITIONAL  HG-01 HG-02 HG-03 HG-04 HG-05 HG-06 HG-07 HG-08 HG-10
HOLD              HG-09 HG-11 HG-12
REJECT            none

ADVANCEMENT
YES — executable proof required
```

The candidate has no static semantic blocker. Its principal PM-03 risk is not lack of database primitives but accidental over-generalization of technical address anchors or under-specification of heterogeneous-reference enforcement.

## 2. HG-01 — PASS-CONDITIONAL

Owner-specific canonical tables, owner-specific material state and specific relation tables preserve reverse mapping. `native_address_anchor`, `scoped_address_anchor` and material-state infrastructure are explicitly technical.

Reject if implementation later adds generic Domain properties/lifecycle to an anchor or routes all canonical semantics through it.

## 3. HG-02 — PASS-CONDITIONAL

Strong path:

```text
homogeneous contract -> direct FK
heterogeneous contract -> bounded address anchor + family eligibility
material state -> explicit MaterialStateRef
external identity -> separate provider-scoped structures
```

PM-05 proof must show:

- invalid family cannot be bound;
- dangling anchor/owner relation cannot survive;
- deletion/tombstone preserves address truth;
- MVCC/xmin/ETag never becomes MaterialStateRef.

## 4. HG-03 — PASS-CONDITIONAL

Dedicated relation tables plus qualified contextual records support binary and n-ary structures. Agreement mapping preserves one common terms state with N party assent bindings.

Negative control: pairwise `agreed_with` rows without common terms binding must fail semantic oracle.

## 5. HG-04 — PASS-CONDITIONAL

Expected `MaterialStateRef` is explicit. PostgreSQL supports conditional writes, row locking and Serializable isolation. Serializable is candidate-native protection against serialization anomalies but requires retry on serialization failure.

Direct proof required:

```text
SC-001 same-base race
SC-009 stale offline write
Read-Committed negative control
stronger transaction/locking positive control
```

Default Read Committed is not accepted as universal consequential-write policy.

## 6. HG-05 — PASS-CONDITIONAL

Co-located owner/state/relation changes can share one transaction. FK/UNIQUE/CHECK/exclusion/locking/Serializable mechanisms may be selected per invariant.

External provider effects remain explicit staged/pending/reconciliation state.

Direct proof must include a predicate/write-skew case, not only two rows updated in one obvious transaction.

## 7. HG-06 — PASS-CONDITIONAL

Stable owner + explicit current material-state binding + retained owner-specific historical state preserves current and historical access without lifetime replay.

Risk: implementation pressure could create a universal history table or mutable-current-only shortcut. Both remain forbidden.

## 8. HG-07 — PASS-CONDITIONAL

Canonical/history/integration/projection/technical structures are physically distinguishable. Namespace separation is organizational only; semantic layer remains explicit in contracts.

## 9. HG-08 — PASS-CONDITIONAL

Shared canonical reality plus application/policy projection and optional RLS can support bounded disclosure. PostgreSQL RLS is not treated as Domain Visibility/Authority.

Important official caveat: referential integrity checks bypass row security, and PostgreSQL documentation warns of covert-channel considerations. PM-05 disclosure tests must therefore pressure errors/constraints/counts as well as ordinary SELECT output.

## 10. HG-09 — HOLD

Tombstone/redaction design is plausible but old-backup anti-resurrection has not run.

Required later:

```text
backup B0
redaction/deletion D1
restore B0
reapply/reconcile D1
verify forbidden payload absent
verify NativeRef non-reuse
```

## 11. HG-10 — PASS-CONDITIONAL

The mapping preserves date-only, floating wall-clock, named zone, accepted historical resolution, instant, interval, duration and recurrence families explicitly.

PostgreSQL types are implementation aids; UTC normalization and calendar-provider formats do not define semantic truth.

## 12. HG-11 — HOLD

Migration strategy is credible but not executed. SC-030 must prove V1 -> V2 while preserving NativeRef/ScopedRecordRef/MaterialStateRef, history, governance and tombstone semantics.

## 13. HG-12 — HOLD

No benchmark host, database deployment, backup or destructive restore exists yet. Operational maturity is not a substitute for direct evidence.

## 14. Destructive mutations

```text
PG-M01 universal Entity table                          REJECTED BY MAPPING
PG-M02 generic Relationship table                    REJECTED BY MAPPING
PG-M03 canonical JSONB property bag                  REJECTED BY MAPPING
PG-M04 anchor carries generic Domain fields          INVALID IMPLEMENTATION
PG-M05 xmin/updated_at becomes MaterialStateRef      INVALID
PG-M06 Read-Committed silent stale overwrite         MUST FAIL TEST
PG-M07 pairwise Agreement without common terms state MUST FAIL ORACLE
PG-M08 provider revision overwrites canonical state  MUST FAIL ORACLE
PG-M09 UTC-only recurrence semantics                 MUST FAIL ORACLE
PG-M10 restore resurrects redacted payload           HOLD UNTIL PM-07
```

## 15. PM-04/05 priority pack

1. implement anchor/ref integrity negative controls;
2. implement SC-001 and predicate write-skew race;
3. implement n-ary Agreement/history oracle;
4. implement current-vs-history queries;
5. implement selective-disclosure leak checks;
6. implement DST/lazy Occurrence fixtures;
7. later execute V1->V2 and destructive restore.

## 16. Official capability evidence

- PostgreSQL Serializable isolation: `https://www.postgresql.org/docs/18/transaction-iso.html`
- SQL integrity/transaction feature support: `https://www.postgresql.org/docs/18/features-sql-standard.html`
- Row Security caveats: `https://www.postgresql.org/docs/18/ddl-rowsecurity.html`

Official docs support feasibility only. Executed LifeOS evidence remains `NOT RUN`.
