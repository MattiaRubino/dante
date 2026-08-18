# TypeDB CE 3.12.3 — PM-03 Semantic Preflight v1

- Candidate: TypeDB CE 3.12.3 / self-hosted single-node / driver 3.12.3
- Mapping: `PM02-TDB-001`
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

TypeDB remains the strongest semantic-relation fit in PM-03, but its exact transaction semantics make consequential concurrency the main unresolved blocker.

## 2. HG-01 — PASS-CONDITIONAL

Concrete entity/relation types, explicit owner keys and owner-specific material-state types preserve the Logical owner census.

TypeDB's implementation type system is not allowed to become a new LifeOS semantic superclass.

Reject any later generic `object`/`thing` supertype if it becomes the owner of common Domain properties or generic relation semantics.

## 3. HG-02 — PASS-CONDITIONAL

The mapping reconstructs references from:

```text
concrete target type
+ explicit key family
+ containing role / Reference Contract
```

`native-id`, `scoped-record-id`, `material-state-id` and provider-scoped external keys remain distinct. TypeDB IID and transaction snapshot are explicitly non-semantic.

Direct proof must verify wrong-type role players and wrong address families are rejected.

## 4. HG-03 — PASS-CONDITIONAL

This is the candidate's strongest structural result.

Current TypeDB 3.x documentation confirms:

- first-class relation types;
- named roles;
- arbitrary n-ary role sets;
- cardinality constraints on `relates`, `plays` and `owns`;
- key/unique constraints for entities and relations.

Agreement can therefore remain one common-ground relation/context with common terms material state rather than pairwise edge reconstruction.

Executable proof still required for update/history semantics and all representative relation families.

## 5. HG-04 — HOLD

The mapping correctly matches exact current `material-state-id` before consequential mutation.

However TypeDB documents ACID guarantees **up to snapshot isolation**. Snapshot isolation does not, by itself, prove absence of predicate/write-skew anomalies across disjoint semantic objects.

PM-02 adds a narrow technical `consistency-guard` that every operation in one invariant boundary mutates.

This is plausible but not yet proof.

Required PM-05 experiment:

```text
T1 reads invariant basis S1
T2 reads same basis S1
T1 updates semantic owner A + guard G
T2 updates semantic owner B + same guard G

EXPECTED
at most one incompatible transaction commits;
other conflicts/retries/revalidates
```

Also run a negative control without guard to demonstrate why the guard is required.

## 6. HG-05 — HOLD

One TypeDB write transaction can contain multiple co-located semantic changes, and schema constraints cover local structural integrity.

The unresolved question is multi-owner predicate consistency under snapshot isolation. The same guard proof from HG-04 is mandatory before atomicity can be called truthful for representative invariant-spanning operations.

Provider/external effects remain staged and reconciled outside the local transaction.

## 7. HG-06 — PASS-CONDITIONAL

Explicit material-state types, `current-state-of-*` bindings and typed correction/provenance relations preserve current/history distinction without event replay.

Direct history oracle must pressure:

- correction without false rewrite;
- historical common-ground Agreement;
- historical Authority/Consent/Visibility basis;
- provider-state reconciliation.

## 8. HG-07 — PASS-CONDITIONAL

Canonical owner types, material-state types, provider records and derived projection records remain distinguishable. TypeDB graph connectivity does not make those layers semantically equivalent.

## 9. HG-08 — PASS-CONDITIONAL

TypeDB's typed relation/role structure can encode semantic governance precisely, but it does not itself prove technical selective-disclosure/non-interference.

The mapping correctly leaves technical AuthZ replaceable and recipient projection separate from canonical state.

PM-05 must test hidden relation existence, counts, role traversal, inferred cardinality, errors and derived result exposure.

## 10. HG-09 — HOLD

The mapping can retain minimal key/tombstone objects while removing sensitive attributes/relations where policy permits, but destructive restore and anti-resurrection have not run.

TypeDB deletion semantics and actual backup/restore behavior must be tested with the exact self-hosted subject.

## 11. HG-10 — PASS-CONDITIONAL

Temporal meaning is stored as explicit semantic structures rather than relying on one engine timestamp. Recurrence families, named-zone intent, historical resolution basis and lazy Occurrence remain distinct.

TypeDB does not need native temporal-table semantics to preserve the Logical contract if the explicit structures remain queryable and evolvable.

## 12. HG-11 — HOLD

TypeDB has a schema language and schema transactions, but PM-03 does not equate schema capability with successful historical migration.

V1 -> V2 must prove:

- explicit IDs survive;
- relation roles/cardinalities migrate safely;
- old material states retain old meaning;
- historical references remain resolvable;
- rollback/recovery is credible.

## 13. HG-12 — HOLD

No deployed subject, host freeze, backup, destructive restore or semantic post-restore suite exists yet.

TypeDB operational documentation remains capability evidence only.

## 14. Destructive mutations

```text
TDB-M01 universal semantic entity supertype                 REJECTED BY MAPPING
TDB-M02 generic relation(from,type,to)                     REJECTED BY MAPPING
TDB-M03 IID becomes NativeRef/MaterialStateRef             INVALID
TDB-M04 current state inferred from latest insertion       INVALID
TDB-M05 snapshot-isolation write-skew with no guard        MUST FAIL NEGATIVE CONTROL
TDB-M06 guard not shared across same invariant boundary    INVALID IMPLEMENTATION
TDB-M07 Agreement flattened to pairwise relations          MUST FAIL ORACLE
TDB-M08 no row -> false/non-member                         MUST FAIL ORACLE
TDB-M09 technical allow relation becomes Authority         INVALID
TDB-M10 restore loses tombstone/redaction truth            HOLD UNTIL PM-07
```

## 15. PM-04/05 priority pack

1. implement concrete typed relation/role/cardinality corpus;
2. implement wrong-player/wrong-address rejection;
3. execute same-base conflict and write-skew negative control;
4. execute shared-guard positive control;
5. execute n-ary Agreement amendment/history;
6. execute selective-disclosure inference pressure;
7. execute current/history and temporal/lazy-Occurrence queries;
8. later execute schema evolution and destructive restore.

## 16. Official capability evidence

- Transactions / snapshot isolation: `https://typedb.com/docs/core-concepts/typedb/transactions/`
- Driver transaction behavior: `https://typedb.com/docs/core-concepts/drivers/transactions/`
- Cardinality constraints: `https://typedb.com/docs/core-concepts/typeql/constraining-data/`
- `@key`: `https://typedb.com/docs/typeql-reference/annotations/key/`
- `@card`: `https://typedb.com/docs/typeql-reference/annotations/card/`
- relation/role model: `https://typedb.com/docs/core-concepts/typeql/entities-relations-attributes/`

Official docs prove capability shape only. The concurrency guard and LifeOS semantics remain unexecuted.
