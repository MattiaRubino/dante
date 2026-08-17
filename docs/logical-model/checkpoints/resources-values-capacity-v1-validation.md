# Slice E — Resources / Values / Capacity — Validation Checkpoint v1

**Status:** Local validation complete — remote QA pending  
**Date:** 2026-08-17  
**Validation standard:** Logical Validation Methodology v1 + Stage-0H hardening

## 1. Scope verdict

Preferred candidate:

> **Layered Typed Resource Feasibility & Allocation Model**

Local verdict:

```text
PASS WITH HARDENING
DOMAIN REOPEN REQUIRED      0
NEW DOMAIN OWNER REQUIRED   0
A+B+C+D REGRESSION FAILURE  0
LOGICAL STRUCTURAL BLOCKER  0
```

This checkpoint is not remote-active until exact Git QA closure succeeds.

## 2. Candidate set reviewed

The following materially different candidates were compared:

### E-A — Universal Resource entity

```text
Resource(id, kind, amount, unit, available, allocated, reserved, status)
```

Rejected because it collapses native identity, Resource role, Requirement, Allocation, Claim and Actual-use distinctions.

### E-B — Fully owner-specific resource structures

Separate requirement/allocation/capacity structures for Asset, Person, Place, etc.

Rejected as the best logical baseline because it duplicates cross-domain planning semantics. Retained as a possible physical ingredient where strong typed FK/storage benefits justify it.

### E-C — Universal Capacity / Claim Ledger

Everything represented as capacity buckets and claims.

Rejected as the complete kernel because qualification, eligibility, capability and non-quantitative Requirement semantics do not reduce safely to capacity dimensions. Retained as a bounded technical mechanism.

### E-D — Solver-first canonical model

Variables, constraints and solver solution treated as source truth.

Rejected because optimization representation is replaceable computation infrastructure rather than stable domain truth.

### E-E — ERP / Inventory kernel

Stock, lots, movements and reservations generalized to all LifeOS resources.

Rejected because people, places, attention, money and general planning are not warehouse inventory. Retained as LR-13 specialist direction.

### E-F — Layered Typed Resource Feasibility & Allocation

Accepted preferred candidate because it preserves typed native identity while sharing bounded planning semantics.

## 3. Required query corpus

The candidate must answer or support reconstruction of at least:

1. What providers can satisfy Requirement R under current authorized context?
2. Which provider is currently allocated, and which was previously allocated?
3. Did Allocation ever exist without an effective Capacity Claim?
4. Was capacity claimed before concrete provider allocation in a late-binding pool case?
5. What capacity was actually protected at time T?
6. What was the effective free compatible capacity at time T?
7. Why was a candidate infeasible or ranked lower?
8. Which Availability rule/override materially affected a historical scheduling decision?
9. What provider was actually used versus planned?
10. Which candidate sets were derived versus explicitly materialized?
11. Does a specific serialized Asset remain distinct from fungible supply?
12. What Quantity/source representation was used before normalization?
13. Which FX basis produced a consequential converted MonetaryAmount?
14. Can current free/busy be exposed without disclosing private source reasons?
15. Can contradictory/overcommitted states remain representable and explainable?

## 4. Falsification scenarios

```text
E-T01 owned Asset unavailable due to repair                  PASS
E-T02 allocated Asset possessed by another actor             PASS
E-T03 allocated Person does not imply Consent/Agreement      PASS
E-T04 Requirement with no candidate                          PASS
E-T05 candidate change without Requirement revision          PASS
E-T06 Allocation without Capacity Claim                      PASS
E-T07 pool Claim before concrete Allocation                  PASS
E-T08 failed Claim preserves prior Allocation history        PASS
E-T09 planned provider differs from Actual use               PASS
E-T10 Actual use without prior Allocation                    PASS
E-T11 all-day Schedule without all-day capacity blocking     PASS
E-T12 scheduled non-blocking item                            PASS
E-T13 compatible overlap                                     PASS
E-T14 incompatible overlap                                   PASS
E-T15 contradictory imported commitments remain stored       PASS
E-T16 count capacity / equivalent pool                       PASS
E-T17 fungible supply without per-unit Asset IDs             PASS
E-T18 serialized Asset identity retained                     PASS
E-T19 on-hand/reserved/forecasted specialist distinction     PASS
E-T20 stable Quantity unit conversion                        PASS
E-T21 cross-currency conversion requires basis               PASS
E-T22 current FX cannot rewrite historical conversion        PASS
E-T23 provider free/busy remains evidence/projection         PASS
E-T24 private health state may reduce capacity privately     PASS
E-T25 resolved temporary limitation stops current effect     PASS
E-T26 Requirement material-state change reevaluates Allocation PASS
E-T27 solver ranking does not create Allocation              PASS
E-T28 very large candidate universe need not be canonical    PASS
E-T29 long availability horizon need not persist free slots  PASS
E-T30 truthful overcommitment must remain representable      PASS
```

## 5. Mutation / destructive tests

The candidate must fail any mutation that introduces the following:

```text
MUT-E01 universal Resource identity root
MUT-E02 retyping native Asset/Person/Place into Resource
MUT-E03 Resource role manufactures identity
MUT-E04 mandatory persisted Requirement row for every simple use
MUT-E05 canonical Candidate Set by default
MUT-E06 candidate change mutates Requirement
MUT-E07 Allocation implies capacity held
MUT-E08 Allocation implies Actual use
MUT-E09 Person Allocation implies Consent/Agreement
MUT-E10 Schedule implies Capacity Claim
MUT-E11 any timestamp overlap implies conflict
MUT-E12 free-slot grid becomes canonical Availability source
MUT-E13 provider free/busy becomes LifeOS truth automatically
MUT-E14 Capacity becomes one universal percentage
MUT-E15 Capacity collapses into Quantity
MUT-E16 Claim collapses into Allocation
MUT-E17 Claim collapses into Actual utilization
MUT-E18 stock reservation collapses into Capacity Claim universally
MUT-E19 fungible units receive unnecessary Asset identity
MUT-E20 serialized Asset collapses into stock quantity
MUT-E21 Quantity collapses into Observation
MUT-E22 MonetaryAmount collapses into Quantity
MUT-E23 FX treated as stable unit conversion
MUT-E24 current FX rewrites old derived amount
MUT-E25 Ownership implies Availability
MUT-E26 Possession implies Allocation
MUT-E27 solver result becomes canonical Allocation
MUT-E28 AI ranking implies Authority
MUT-E29 provider reservation ID becomes LifeOS identity
MUT-E30 database globally prohibits overlapping claims/schedules
MUT-E31 free-capacity cache becomes source truth
MUT-E32 one claim ledger owns all resource semantics
MUT-E33 Actual use fabricates retrospective Allocation
MUT-E34 Requirement change silently carries Allocation forward
```

All mutations are rejected by the preferred candidate.

## 6. Counterfactual pairs

The candidate must preserve different outcomes for near-identical cases:

```text
owned vs available
possessed vs allocated
candidate vs selected
allocated vs capacity held
capacity held vs actually used
Schedule present vs capacity consumed
free interval vs enough compatible capacity for this commitment
pool of 3 equivalent rooms vs Room A17 specifically allocated
500 ml fungible oil vs individually tracked camera
Quantity conversion vs FX conversion
current Availability vs historical Availability used by old decision
solver candidate vs authorized Allocation
```

Result: PASS.

## 7. Historical replay

Required replay:

```text
T0 baseline Availability / Capacity
T1 temporary limitation changes effective capacity
T2 planner creates schedule/allocation under T1 assumptions
T3 limitation resolves
T4 current capacity returns
```

The model must answer both:

- what is applicable now?
- why did LifeOS make the historical planning decision at T2?

This is satisfied through owner-specific material state plus MaterialStateRef/Version/Provenance from Slice D, not by retaining obsolete current flags.

## 8. Multi-actor / privacy pressure

PASS with the following hardening:

- Resource role does not grant Visibility;
- free/busy projection may be visible while private source reason remains hidden;
- candidate matching may use authorized private facts without exposing them;
- Allocation result visibility is separable from eligibility rationale visibility;
- allocation Authority is independent from provider identity/ownership/possession;
- solver access to authorized inputs is not disclosure permission.

## 9. Scale / evolution pressure

PASS under the following assumptions:

- Candidate Set is derived/cacheable and not required as canonical row explosion;
- Effective Availability/free capacity is derived/cacheable;
- native provider references remain typed and stable;
- high-cardinality specialist inventory is isolated from general kernel;
- optimization engines remain replaceable;
- physical schemas may use owner-specific typed structures where performance requires them.

No current evidence requires a universal graph, Resource root, Reservation root or event-sourced capacity ledger.

## 10. LM gate results

```text
LM-01 Semantic owner coverage                 PASS
LM-02 Identity/reference preservation          PASS
LM-03 Lifecycle/state separation               PASS WITH HARDENING
LM-04 Historical reconstruction / WD-03        PASS WITH HARDENING
LM-05 Relation/governance specificity          PASS
LM-06 Multi-actor/selective visibility         PASS WITH HARDENING
LM-07 Provenance/reconciliation                PASS
LM-08 Simple-case compactness                  PASS
LM-09 Specialist boundary                      PASS
LM-10 No semantic-free fallback                PASS
LM-11 Reverse mapping                          PASS
LM-12 High-value query feasibility             PASS
LM-13 Evolution/obsolescence resilience        PASS
LM-14 Scale/concurrency plausibility           PASS WITH HARDENING
LM-15 External benchmark/anti-pattern mining   PASS
LM-16 Persistence/API pressure / WD-05         PASS WITH HARDENING
```

## 11. Hardening retained

1. No ResourceRef/universal Resource root.
2. Candidate Set derived by default.
3. Effective Availability/free capacity derived by default.
4. Allocation / Claim / Actual-use separation is mandatory.
5. Schedulable Capacity Claim is not universal stock reservation.
6. Capacity may be multidimensional and contextual.
7. Quantity and MonetaryAmount may share scalar machinery but not semantics.
8. Solver/AI remains computation, not source truth.
9. Material historical feasibility inputs remain reconstructible where consequential.
10. Physical owner-specific structures remain allowed without semantic collapse.

## 12. Reverse mapping

The logical candidate maps back unambiguously to Domain owners:

```text
NativeRef(Asset/Person/Place/...) -> native provider identity
Resource-role reference           -> Resource
Requirement record/specification  -> Resource Requirement
Candidate projection              -> Candidate Set
qualified allocation record       -> Resource Allocation
Availability rule/fact            -> Availability
capacity dimensions/policy        -> Capacity
qualified capacity commitment     -> Capacity Claim
scalar measurement value          -> Quantity
currency-bearing scalar value     -> MonetaryAmount
actual use record                  -> Actual / specialist realization semantics
```

No generic semantic-free fallback is required.

## 13. Final local verdict

```text
SLICE E
PASS WITH HARDENING

REOPEN = 0
UNCLASSIFIED = 0
UNRESOLVED STRUCTURAL = 0

REMOTE QA
PENDING
```
