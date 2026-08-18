# XTDB 2.1.0 — PM-03 Semantic Preflight v1

- Candidate: XTDB 2.1.0 / self-hosted qualification subject
- Mapping: `PM02-XT-001`
- Status: **STATIC PREFLIGHT COMPLETE / EXECUTED HG NOT RUN**
- Production topology: **HOLD**
- Selection: **NONE**

## 1. Verdict

```text
PASS-CONDITIONAL  HG-01 HG-04 HG-05 HG-06 HG-07 HG-08 HG-10
HOLD              HG-02 HG-03 HG-09 HG-11 HG-12
REJECT            none

ADVANCEMENT
YES — WITH REFERENCE/CONSTRAINT HOLD
```

XTDB remains structurally attractive for chronology and serialized write semantics, but PM-03 identifies database-enforced reference/cardinality integrity as its main primary-store risk.

## 2. HG-01 — PASS-CONDITIONAL

Owner-specific tables plus four segregated address spaces preserve semantic ownership. Native bitemporality is used as a physical history substrate, not as a universal Fact ontology.

Reject if dynamic row flexibility becomes a generic canonical property store.

## 3. HG-02 — HOLD

The mapping correctly separates:

```text
native_address
scoped_address
material_state_address
external_address
```

and explicitly rejects a universal `TypedRef(kind,id)`.

The material issue is enforcement: the exact candidate does not provide ordinary SQL foreign keys for these canonical references. Consequential writes therefore depend on `ASSERT` predicates plus controlled writer discipline.

Direct proof must establish that every canonical reference-creation path rejects:

- missing target;
- wrong address space;
- wrong owner/family for the Reference Contract;
- invalid retired/tombstoned target;
- stale material-state binding.

Until that mutation pack exists, HG-02 remains HOLD.

## 4. HG-03 — HOLD

Specific relation-family tables and one-record-plus-party-assent Agreement mapping preserve relation meaning statically.

The unresolved issue is enforcing role/cardinality/uniqueness constraints without conventional FK/cardinality constraints.

XTDB's serialized writes + `ASSERT` make a viable path plausible, but the benchmark must prove concurrent attempts cannot create invalid cardinality or duplicate canonical relation state.

## 5. HG-04 — PASS-CONDITIONAL

XTDB documentation states that DML transactions are serialized through a totally ordered log and are serializable. `ASSERT` can roll back a transaction when a predicate is false.

The mapping therefore has a strong candidate-native mechanism:

```text
ASSERT current MaterialStateRef == expected
ASSERT required reference/invariant predicates
apply all writes in same DML transaction
```

Direct SC-001 proof is still required. The result is not a final hard-gate PASS.

## 6. HG-05 — PASS-CONDITIONAL

One submitted DML transaction is atomic for co-located changes and write transactions are serialized.

The main risk is completeness/ergonomics rather than write-skew: every material invariant must be expressible as transaction-local DML/`ASSERT` because the transaction is non-interactive.

PM-05 must prove a complex governed multi-owner operation can be expressed without splitting one semantic transaction into weaker client-side steps.

External/provider effects remain staged/reconciled.

## 7. HG-06 — PASS-CONDITIONAL

XTDB provides the strongest native temporal substrate in the admitted set, but PM-03 preserves a strict barrier:

```text
SYSTEM_TIME != MaterialStateRef
VALID_TIME  != MaterialStateRef
transaction token != MaterialStateRef
```

Explicit material-state rows still own semantic state identity. Native temporal axes are used only where they truthfully correspond to recorded/system chronology or world/effective validity.

Direct proof must test correction without false rewrite and current-state access without accidental lifetime-history logic.

## 8. HG-07 — PASS-CONDITIONAL

Canonical owner rows, explicit semantic material states, external/provider structures and projection tables remain distinguishable. Technical transaction tokens may support freshness only.

## 9. HG-08 — PASS-CONDITIONAL

The mapping can represent Authority/Consent/Visibility/Representation and disclosure surfaces separately, but enforcement is primarily query/application architecture rather than an assumed database-native security ontology.

PM-05 must pressure:

- bitemporal/history access leakage;
- hidden relation existence;
- counts/ranking/errors;
- provider/source disclosure;
- stale projection basis.

## 10. HG-09 — HOLD

XTDB explicitly distinguishes temporal deletion from `ERASE`, which can irreversibly remove all versions of a document. That is useful but dangerous if used without preserving legally/permissibly required non-sensitive reference continuity.

The mapping therefore separates sensitive payload erasure from minimal tombstone/address continuity.

Old-backup anti-resurrection remains entirely unexecuted and holds the gate.

## 11. HG-10 — PASS-CONDITIONAL

XTDB valid/system time is deliberately not used as a substitute for Recurrence, Schedule, Actual, Occurrence identity or timezone semantics.

The mapping preserves original date/floating/named-zone/instant/range/duration forms and accepted historical resolution basis explicitly.

Its bitemporal feature is therefore an advantage only where semantics align, not a semantic shortcut.

## 12. HG-11 — HOLD

XTDB's flexible/dynamic row model makes coexistence of mapping revisions possible, but `schema flexibility` is explicitly not accepted as an evolution result.

SC-030 must prove:

- readers/writers interpret V1/V2 correctly;
- address anchors and MaterialStateRefs survive;
- old history is not reinterpreted retroactively;
- tombstone/redaction behavior survives migration.

## 13. HG-12 — HOLD

No executable benchmark host/deployment or destructive recovery evidence exists. Production topology also remains separately HOLD from PM-01.

The qualification subject may still proceed to semantic/correctness execution without claiming production HA/recovery fitness.

## 14. Non-interactive transaction pressure

XTDB DML transactions may contain DML and `ASSERT` statements and are not an arbitrary client read/branch/write conversation.

PM-03 found no closed LifeOS semantic requirement that inherently requires an interactive transaction API, because consequential preconditions/effects can in principle be submitted declaratively.

This is **not yet proof**. PM-05 must include a representative complex governed operation whose:

- expected material state;
- reference validity;
- governance basis;
- multi-owner invariant;
- idempotency;
- resulting writes

all fit one transaction without semantic weakening.

If that cannot be expressed cleanly, the candidate may fail later despite serializable ordering.

## 15. Destructive mutations

```text
XT-M01 universal bitemporal Fact table                  REJECTED BY MAPPING
XT-M02 SYSTEM_TIME becomes MaterialStateRef             INVALID
XT-M03 VALID_TIME absorbs Schedule/Actual/Recurrence    INVALID
XT-M04 generic typed_ref collapses address spaces       REJECTED BY MAPPING
XT-M05 reference written without ASSERT                 INVALID CANONICAL WRITE
XT-M06 wrong-family reference accepted                  MUST FAIL TEST
XT-M07 duplicate/cardinality race                       MUST FAIL TEST
XT-M08 split invariant across separate transactions     INVALID WHEN ATOMICITY REQUIRED
XT-M09 provider revision becomes semantic state         INVALID
XT-M10 ERASE destroys required reference continuity     MUST FAIL POLICY ORACLE
```

## 16. PM-04/05 priority pack

1. implement canonical reference-creation API with complete ASSERT pack;
2. run wrong-family/missing-target/tombstone negative tests;
3. run cardinality/uniqueness concurrent races;
4. run SC-001 expected-state race;
5. run complex non-interactive governed mutation;
6. run bitemporal correction/current-history oracle;
7. run DST/lazy Occurrence cases;
8. later run V1->V2 and destructive restore.

## 17. Official capability evidence

- transaction consistency: `https://docs.xtdb.com/about/txs-in-xtdb.html`
- SQL DML / `ASSERT` / `ERASE`: `https://docs.xtdb.com/reference/main/sql/txs.html`

Official docs support serialized DML/ASSERT feasibility only. LifeOS referential/cardinality correctness remains unexecuted.
