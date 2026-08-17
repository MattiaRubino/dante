# Slice E — Resources / Values / Capacity v1

**Status:** Local logical candidate — PASS WITH HARDENING, pending remote QA closure  
**Date:** 2026-08-17  
**Workstream:** Logical Model  
**Slice:** E — Resources / Values / Capacity

## 1. Scope

This slice maps the accepted Domain semantics around:

- Asset / Resource role;
- Resource Requirement;
- Candidate Set;
- Resource Allocation;
- Availability / Capacity;
- Capacity Reservation / Claim;
- Quantity;
- MonetaryAmount;
- Ownership / Possession boundaries;
- fungible supply / pool pressure;
- specialist inventory and finance boundaries.

This slice does not authorize SQL, migrations, APIs, backend implementation, solver selection, inventory engines, FX providers, unit libraries, or frontend work.

## 2. Preferred logical architecture

The accepted candidate is a **Layered Typed Resource Feasibility & Allocation Model**.

```text
NATIVE PROVIDER
Person / Asset / Place / specialist supply / pool ...
        |
        | may play
        v
RESOURCE ROLE
        |
        v
RESOURCE REQUIREMENT
        |
        v
CANDIDATE SET                derived
        |
        v
RESOURCE ALLOCATION          planned designation
        |
        +------------------+
        v                  |
CAPACITY CLAIM              |
when capacity is held       |
        |                  |
        v                  |
ACTUAL USE  <--------------+
what really happened

Availability / Capacity / compatibility / policy
feed feasibility and remaining-capacity projections.
```

The sequence is possible, not mandatory.

Valid states include:

```text
Requirement without candidates
Allocation without Capacity Claim
pool Capacity Claim before concrete Allocation
Actual use without prior Allocation
```

No mandatory `Requirement -> Candidate -> Allocation -> Reservation -> Actual` state machine is introduced.

## 3. Resource does not create identity

`Resource` remains a contextual planning/execution role and not a native identity/root.

```text
Asset != Resource
Person != Resource
Place != Resource
```

A native referent retains its own ReferenceAddress while playing Resource role.

Therefore:

```text
no ResourceRef
no universal resources root
no wrapper identity around Person / Asset / Place
```

Examples:

```text
NativeRef(Asset A17)  -> Resource role for a photo shoot
NativeRef(Person P3)  -> Resource role for an interpreting need
NativeRef(Place L8)   -> Resource role for a workshop
```

## 4. Resource Requirement

Resource Requirement represents what a bounded planning/execution context needs.

Logical disposition:

```text
Resource Requirement
-> LR-05 rule/specification semantics
-> LR-02 + ScopedRecordRef only when material persistence/history/addressability is required
```

Requirement may describe capability, qualification, compatibility, quantity, location, temporal need, capacity need or supply characteristics without manufacturing provider identity.

Simple flows may remain compact where consequence does not require an independently materialized Requirement record.

## 5. Candidate Set

Candidate Set is contextual/derived by default.

```text
Candidate Set
-> LR-08 derived projection
```

Candidate-set change does not revise Requirement identity automatically.

Candidate computation may use private facts, Availability/Capacity, Criterion/Evaluation, qualifications, provider data and policy, but the resulting candidate projection does not become canonical source truth merely because a solver produced it.

## 6. Resource Allocation

Resource Allocation is planned designation/selection of one or more providers, supplies or capacity sources intended to satisfy a Requirement.

Logical disposition:

```text
Resource Allocation
-> LR-03 qualified typed association
-> LR-02 + ScopedRecordRef when material history/governance/reconciliation requires a material record
```

Mandatory separation:

```text
Allocation != Candidate
Allocation != Capacity Claim
Allocation != Schedule
Allocation != Possession
Allocation != Ownership
Allocation != Agreement / Consent / Participation / Responsibility
Allocation != Actual use
```

Reallocation/substitution preserves material prior history. Material Requirement change does not silently carry an earlier Allocation forward.

## 7. Availability

Availability is a time-dependent rule or fact about when schedulable capacity may be used.

Logical disposition:

```text
baseline / reusable Availability rule
-> LR-05

explicit material override/fact
-> LR-02 where history/consequence requires it

Effective Availability
-> LR-08
```

LifeOS must not persist a giant free-slot grid as canonical truth when free intervals are merely derived from baseline rules, overrides, claims and compatibility.

Provider free/busy remains external evidence/projection, not automatic canonical Availability.

## 8. Capacity

Capacity is contextual ability to accept compatible commitments. It is not a universal binary or one global percentage.

Possible dimensions include exclusive attention, count capacity, quantitative capacity and domain-specific compatibility dimensions.

Logical disposition:

```text
Capacity
-> contextual capability/state
-> LR-04 typed value dimensions where numeric
-> LR-05 compatibility/policy semantics
-> LR-02 material contextual state only where consequence requires it

Effective remaining/free capacity
-> LR-08
```

Capacity does not receive NativeRef merely because a quantitative representation exists.

## 9. Capacity Reservation / Claim

Capacity Claim represents schedulable capacity actually committed, occupied, protected or held for a purpose during an accepted temporal placement.

Logical disposition:

```text
Capacity Claim
-> LR-03 qualified commitment relation
-> LR-02 + ScopedRecordRef where materially persistent/addressable
```

For ordinary Event/Activity flows, capacity impact may remain compact/reconstructible rather than forcing a first-class aggregate. A standalone capacity-only subject such as protected focus may justify its own material record.

Mandatory separation:

```text
Schedule != Capacity Claim
Allocation != Capacity Claim
Capacity Claim != Actual utilization
```

Timestamp overlap alone does not universally imply conflict. Compatibility/capacity semantics decide feasibility; contradictory or overcommitted real states must remain representable.

## 10. No universal Reservation root

Schedulable Capacity Claim must not be generalized automatically into a universal reservation concept for stock, money, inventory, persons and time.

```text
Capacity Claim
!= inventory / stock hold automatically
```

A future specialist inventory model may share technical claim/accounting machinery where useful, but shared mechanism does not establish a shared semantic superclass.

## 11. Fungible supply versus native identity

Individual identity is preserved only where materially justified.

```text
specific camera body / serial
-> Asset NativeRef

500 ml oil
-> fungible Quantity/supply semantics
-> no per-unit Asset identities
```

Lots, batches, serials and inventory movements remain specialist semantics when concrete workflows require them.

## 12. Quantity

```text
Quantity
-> LR-04 reusable scalar value semantics
```

Quantity preserves magnitude plus interpretable unit semantics, while subject, property, time, provenance, lifecycle and evaluative meaning remain owned by the containing concept.

```text
Quantity != Observation
number != Quantity automatically
```

Unit normalization/conversion must not rewrite material source representation or fabricate precision.

## 13. MonetaryAmount

```text
MonetaryAmount
-> LR-04 reusable monetary value semantics
```

Quantity and MonetaryAmount may share scalar/decimal infrastructure but remain separate semantic families.

```text
MonetaryAmount != Quantity
Currency != ordinary Quantity unit semantics
```

Cross-currency derivation requires an applicable conversion basis, such as rate, source and effective time/context. Derived conversion never mutates the source amount.

## 14. Solver / AI boundary

A solver or AI may compute:

- candidates;
- feasibility;
- ranking;
- proposed Allocation;
- proposed Claim;
- substitutions;
- conflict explanations.

But:

```text
solver result != canonical Allocation
AI ranking != Allocation
AI optimization != Authority
private eligibility input != disclosure permission
```

The solver is replaceable computation infrastructure, not a source-of-truth owner.

## 15. Specialist boundary

General LifeOS kernel does not absorb specialist inventory or finance engines.

Allowed future specialist extensions include:

- inventory stock/hold/movement;
- lot/serial tracking;
- warehouse forecasting;
- financial accounts/transactions/ledger;
- specialist booking/source-of-record behavior.

These may reuse ReferenceAddress, MaterialStateRef, Version/Provenance and typed technical mechanisms without becoming universal roots.

## 16. Accepted logical dispositions

```text
Asset
-> LR-01 / NativeRef

Resource
-> contextual role over existing ReferenceAddress

Resource Requirement
-> LR-05
-> LR-02 + ScopedRecordRef when material

Candidate Set
-> LR-08

Resource Allocation
-> LR-03
-> LR-02 + ScopedRecordRef when material

Availability rule
-> LR-05

Availability override / material fact
-> LR-02 where required

Effective Availability
-> LR-08

Capacity
-> contextual capability/state
-> LR-04 + LR-05 + bounded LR-02 where required

Effective Free Capacity
-> LR-08

Capacity Claim
-> LR-03
-> LR-02 + ScopedRecordRef when material

Quantity
-> LR-04

MonetaryAmount
-> LR-04 separate semantic family
```

## 17. Core invariants

1. Resource is role, not identity.
2. Native provider identity remains owned by its semantic owner.
3. Requirement does not manufacture provider identity.
4. Candidate Set is derived by default.
5. Candidate-set change does not revise Requirement automatically.
6. Allocation is planned designation, not reservation or actual use.
7. Capacity Claim is schedulable capacity held/protected, not universal reservation.
8. Schedule does not imply Capacity Claim.
9. Timestamp overlap does not imply conflict universally.
10. Effective Availability/Free Capacity are derived views.
11. Capacity is not universally binary or one percentage.
12. Fungible supply does not require per-unit Asset identity.
13. Quantity and MonetaryAmount remain separate semantic families.
14. FX conversion requires an applicable basis and does not mutate source amount.
15. Solver/AI output does not become canonical without applicable semantic transition/Authority.
16. Specialist inventory/finance semantics remain bounded.
17. Historical allocation/capacity assumptions remain reconstructible where consequential.
18. No SQL/API/persistence shape is accepted by this slice.

## 18. Verdict

```text
SLICE E — RESOURCES / VALUES / CAPACITY
PREFERRED: Layered Typed Resource Feasibility & Allocation Model

LOCAL VERDICT
PASS WITH HARDENING

DOMAIN REOPEN REQUIRED      0
NEW DOMAIN OWNER REQUIRED   0
A+B+C+D REGRESSION FAILURE  0
LOGICAL STRUCTURAL BLOCKER  0
```

Canonical activation still requires exact remote Git QA and closure.