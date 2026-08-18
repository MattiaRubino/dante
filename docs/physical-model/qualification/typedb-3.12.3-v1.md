# TypeDB CE 3.12.3 — PM-05 Correctness Evidence Qualification v1

- Candidate: TypeDB CE 3.12.3 / self-hosted single-node / driver 3.12.3
- Mapping: `PM02-TDB-001`
- PM-05 disposition: **PRIMARY FINALIST / ADVANCE TO PM-06/07 JOINT WITH GUARD CONDITION**
- Direct LifeOS execution: **NOT RUN**
- Selection: **NONE**

## 1. Qualification thesis

TypeDB remains the principal semantic challenger because typed relations, named roles, role eligibility and n-ary relation modeling align unusually well with LifeOS relation semantics. PM-05 does not eliminate the concurrency cost identified earlier; it classifies that cost as known and explicit rather than as an unknown requiring a broad local lab now.

## 2. Primary semantic scenario coverage

### SC-001 / SC-009 — stale-base consequential writes

Expected-state remains explicit through MaterialStateRef. Snapshot isolation is not upgraded by assertion. Where a shared invariant can otherwise write-skew, every consequential transaction in that invariant scope must mutate the same narrow technical consistency guard.

```text
snapshot isolation
+ same-data write conflict
+ common guard write
→ credible conflict point
```

Classification:

```text
PRIMARY-EVIDENCE-SUFFICIENT
KNOWN DESIGN CONDITION
```

### SC-003 — atomic multi-owner mutation

One TypeDB write transaction can atomically mutate co-located typed entities/relations. Predicate invariants spanning disjoint records require the same bounded guard discipline.

Classification: `PRIMARY-EVIDENCE-SUFFICIENT / KNOWN DESIGN COST`.

### SC-010 / SC-014 — correction/history

Owner-specific explicit material-state types retain semantic state identity independently of transaction metadata. Historical reconstruction remains explicit rather than relying on an engine temporal history feature.

Classification: `PRIMARY-EVIDENCE-SUFFICIENT`.

### SC-012 — NativeRef non-reuse

Stable explicit owner keys and tombstone/minimum continuity policy preserve non-reuse. Final restore/anti-resurrection remains PM-07 finalist evidence.

### SC-015 — typed n-ary relation fidelity

This is TypeDB's strongest comparative area. Named roles, typed players and n-ary relations directly preserve Agreement/common-ground semantics without pairwise-edge inference.

Classification: `PRIMARY-EVIDENCE-SUFFICIENT / COMPARATIVE STRENGTH`.

### SC-016 — selective disclosure

The type/role model can represent the required semantic surface, but full non-interference remains a system/finalist proof rather than a database-only claim.

### SC-022 / 023 / 024 — temporal/recurrence

Temporal semantics remain explicit LifeOS objects/attributes; recurrence and lazy Occurrence are not inferred from a generic Rule or engine time primitive.

Classification: `PRIMARY-EVIDENCE-SUFFICIENT`.

## 3. Known costs

```text
snapshot isolation rather than native serializable execution
mandatory correct consistency-guard scoping for write-skew-sensitive invariants
explicit material-state/history structures
smaller operational/tooling ecosystem than PostgreSQL
self-hosted backup/recovery/evolution burden remains material
```

These costs remain active in PM-06/07 and PM-09. They are not erased by the semantic elegance of the model.

## 4. PM-06/07 finalist obligations

Carry forward:

```text
SC-011 old-backup anti-resurrection
SC-013 deep-history/current-state efficiency
SC-030 V1 -> V2 schema/data evolution
SC-031 backup/restore + semantic verification
SC-032 capacity/backpressure
consistency-guard operational burden/sensitivity
```

No direct execution is admitted yet. Reopen a targeted guard proof only if the PostgreSQL/TypeDB ranking materially depends on it after joint qualification.

## 5. Disposition

```text
PRIMARY FINALIST
YES

ADVANCE
PM-06/07 JOINT FINALIST QUALIFICATION

CONDITION
NARROW CONSISTENCY-GUARD COVERAGE REQUIRED

PM-05 EXECUTION-WORTHY GAP
0

DIRECT HG
NOT RUN

PREFERRED
NO

SELECTED
NO
```
