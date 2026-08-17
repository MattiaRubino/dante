<!-- LIFEOS-CANONICAL-CONTINUATION document="test-corpus-v1.md" follows="test-corpus-v1-part-6.md" -->
> **Canonical continuation of the single Logical Model Test Corpus v1 document.** Earlier corpus families remain active. This continuation adds Integrated A+B+C+D+E cross-slice regression, mutation and counterfactual tests.

# Integrated A+B+C+D+E corpus

## ABCDE-REF-01 — Native resource target

A photo plan uses a specific Sony A7 IV Asset.

Expected:

```text
NativeRef(Asset)
Resource role contextual only
no Resource wrapper identity
```

## ABCDE-REF-02 — Non-native resource target

Maintenance needs 500 ml of a fungible oil supply/pool.

Expected:

```text
bounded supply/value target
Quantity semantics
no synthetic Resource NativeRef
no per-ml Asset identity
```

## ABCDE-REF-03 — Service/pool target

A Plan requires an interpreter service or one slot from a bounded service pool, but no specific Person is selected yet.

Expected:

```text
Requirement representable
non-native service/pool target allowed
no fake Person/Resource identity
```

## ABCDE-HIST-01 — Requirement changes after Allocation

T1:

```text
Requirement R state S1
full-frame camera
Allocation -> Asset A17
```

T2:

```text
Requirement R state S2
full-frame + 8K60
```

Expected historical query:

> Why was A17 selected at T1?

Expected:

```text
historical Allocation reconstructs S1 basis
current S2 does not retroactively redefine T1 Allocation
```

## ABCDE-HIST-02 — Availability changes after Allocation

T1 planner sees Asset A available and allocates it.
T2 Asset A becomes unavailable.

Expected:

```text
current infeasibility representable
historical selection basis remains reconstructible
no claim that T1 planner used T2 state
```

## ABCDE-HIST-03 — Capacity changes after Claim

T1 room pool capacity = 3; two claims exist.
T2 capacity is reduced to 1.

Expected:

```text
T1 claims remain historically explainable
T2 overcommit/conflict may be derived
old capacity basis not overwritten
```

## ABCDE-HIST-04 — Schedule moves after Capacity Claim

T1:

```text
Schedule S1 = 15:00-16:00
Claim C applies to S1
```

T2:

```text
Schedule S2 = 16:00-17:00
operational claim follows current Schedule
```

Expected:

```text
current claim placement may be 16:00-17:00
historical C/S1 basis remains reconstructible
```

Forbidden:

```text
history now appears as though claim was always 16:00-17:00
```

## ABCDE-CAND-01 — Current candidate universe differs from historical

T1 candidate universe:

```text
A17
A18
```

Allocation selects A17.

T2 provider state changes; current candidate universe:

```text
A17
A19
Rental Z
```

Expected:

```text
current candidates may be recomputed
historical candidate universe not inferred from current query
historical Decision explanation uses retained/reconstructible T1 basis where consequential
```

## ABCDE-CAND-02 — Large transient candidate universe

10,000 candidates are evaluated for a low-consequence recommendation and no selection is made.

Expected:

```text
no requirement to persist 10,000 canonical candidate rows
bounded cache/transient computation allowed
```

## ABCDE-CAND-03 — Consequential candidate universe

A regulated/high-consequence Decision materially depends on which providers were eligible at the time.

Expected:

```text
exact/bounded candidate basis retained or reconstructible
not replaced by current provider search
```

## ABCDE-ACTUAL-01 — Planned resource substitution

Plan allocated Camera A17. A17 fails. Rental B is used.

Expected:

```text
Allocation A17 retained
realized use B retained
Actual may reconcile the expected plan where appropriate
no rewrite of Allocation to B
```

## ABCDE-ACTUAL-02 — Spontaneous use without expectation

User spontaneously takes a taxi; no prior Activity/Plan/Allocation expectation existed.

Expected:

```text
realized fact representable under appropriate reality/specialist owner
no fake Domain Actual solely because it happened
no retrospective Allocation
```

## ABCDE-RULE-01 — Same comparison shape, different semantic owner

Examples:

```text
Criterion: weight <= 70 kg
Resource Requirement: camera weight <= 1.5 kg
Temporal Constraint: finish <= 20:00
Availability rule: unavailable after 20:00
```

Expected:

```text
shared predicate/comparison machinery allowed
each semantic owner remains recoverable
no universal Rule semantic root
```

## ABCDE-RULE-02 — Criterion != Resource Requirement

Goal Criterion requires 3 workouts/week.
Resource Requirement requires one gym slot.

Expected:

```text
Criterion evaluates target
Resource Requirement expresses needed resource capability
no collapse because both may use LR-05
```

## ABCDE-RULE-03 — Temporal Constraint != Availability

User is free 18:00-22:00 but workout rule forbids scheduling after 20:00.

Expected:

```text
Availability says capacity may be usable
Temporal Constraint says placement after 20:00 is not allowed/preferred
both states coexist
```

## ABCDE-IMPLICIT-01 — Compact implicit Requirement

Simple plan directly uses owned Camera A17 and no independent requirement history/governance is material.

Expected:

```text
compact representation permitted
no mandatory standalone Requirement row
```

## ABCDE-IMPLICIT-02 — Implicit Requirement becomes consequential

A formerly simple embedded Requirement later explains a consequential Allocation/Decision.

Expected:

```text
applicable Requirement state becomes materially reconstructible
current mutable fields cannot stand in for historical meaning
```

## ABCDE-SOLVER-01 — Solver version changes

T1 solver/model version V1 selects A17.
T2 V2 with the same current inputs would select A19.

Historical query:

> Why was A17 selected at T1?

Expected:

```text
T1 material solver/model basis retained where consequential
current V2 not projected backward
canonical Allocation identity/state independent from solver implementation
```

## ABCDE-SOLVER-02 — Solver family replaced

System migrates from CP-SAT to another solver/heuristic.

Expected:

```text
existing canonical Requirements/Allocations/Claims remain semantically valid
no mandatory semantic migration of solver-variable identities
```

## ABCDE-SOLVER-03 — Opaque AI recommendation rejected

AI recommends Rental Z but cannot provide/retain a material basis for a consequential action.

Expected:

```text
recommendation may remain candidate/proposal
must not silently become canonical Allocation solely because AI ranked it
```

## ABCDE-SOLVER-04 — Full search tree not required

A solver evaluates millions of branches but the selected effect only requires a bounded set of material inputs/rationale for audit.

Expected:

```text
no canonical persistence requirement for every rejected branch/search node
```

## ABCDE-FEAS-01 — Eligible != available

A camera model is compatible in principle but currently in repair.

Expected:

```text
eligible yes
currently available no
```

## ABCDE-FEAS-02 — Available != feasible

A room is free, but too small for the event.

Expected:

```text
available yes
feasible for Requirement no
```

## ABCDE-FEAS-03 — Feasible != allocated

Three rooms are feasible; none has been selected.

Expected:

```text
Candidate Set non-empty
Allocation absent
```

## ABCDE-FEAS-04 — Allocated != claimed

Room A is selected in the plan, but no reservation/capacity hold exists.

Expected:

```text
Allocation present
Claim absent
```

## ABCDE-FEAS-05 — Claimed != realized use

Room A is reserved but event is cancelled or moved.

Expected:

```text
historical Claim retained
realized use absent/different according to reality
```

## ABCDE-PRIV-01 — Private health cause -> shared unavailable result

Private temporary illness reduces capacity for a shared planning window.

Expected shared result:

```text
unavailable / insufficient compatible capacity
```

Forbidden unless separately visible:

```text
illness diagnosis/source
```

Historical explanation for an authorized viewer may still reconstruct the private basis.

## ABCDE-PRIV-02 — Private identity/source link affects feasibility

A private provider/account linkage proves that two external availability records belong to the same Person.

Expected:

```text
internal reconciliation may prevent double-counting
identity linkage itself not automatically disclosed
```

## ABCDE-KNOW-01 — Current knowledge vs historical planning basis

LifeOS now knows a previous provider availability record was wrong.

Historical planner had acted on the old accepted source state.

Expected:

```text
current corrected knowledge retained
historical Decision remains reconstructible from what was accepted then
correction does not pretend final truth was always known
```

## ABCDE-KNOW-02 — Unknown availability

Provider/source data is incomplete.

Expected:

```text
unknown/unresolved availability/feasibility allowed
not forced to available=false or true
```

## ABCDE-SIMPLE-WORST PAIR

### Simple

```text
Photo shoot
use my Sony A7 IV
```

Expected:

```text
no visible bureaucracy
no mandatory solver/candidate/claim graph
```

### Worst case

```text
multi-party trip
scarce equipment
private health/availability inputs
multiple providers
budget + temporal constraints
AI/solver recommendation
accepted Allocation + Claims
later Schedule change
provider correction
resource substitution during execution
```

Expected:

```text
identity preserved
historical material inputs reconstructible
private source boundaries preserved
current vs historical projections distinguished
solver replaceable
no generic semantic root
```

# Integrated mutation matrix

Reject implementations that introduce:

```text
MUT-ABCDE01 every Resource target must be NativeRef
MUT-ABCDE02 non-native pool/supply/service promoted to native Resource identity
MUT-ABCDE03 Allocation uses current Requirement as historical basis
MUT-ABCDE04 Claim uses current Schedule as historical placement
MUT-ABCDE05 current Candidate Set presented as historical candidate universe
MUT-ABCDE06 every solver candidate/search node becomes canonical state
MUT-ABCDE07 solver/AI output becomes Allocation automatically
MUT-ABCDE08 spontaneous reality becomes Domain Actual without expectation
MUT-ABCDE09 LR-05 becomes universal Rule root
MUT-ABCDE10 Criterion/Requirement/TemporalConstraint collapse under shared predicate machinery
MUT-ABCDE11 consequential implicit Requirement remains historically mutable
MUT-ABCDE12 current Availability/Capacity rewrites old feasibility explanation
MUT-ABCDE13 current solver/model version is assumed for historical Decision
MUT-ABCDE14 one `available` boolean collapses feasibility ladder
MUT-ABCDE15 Candidate Set becomes canonical Requirement source
MUT-ABCDE16 private feasibility source leaks through shared projection/explanation
```

Expected:

```text
16 / 16 REJECTED
```

# Integrated counterfactual matrix

The model must distinguish:

```text
CF-ABCDE01 specific native Asset target / fungible supply target
CF-ABCDE02 current Requirement / Requirement state used historically
CF-ABCDE03 current candidates / candidates considered historically
CF-ABCDE04 planned Allocation / realized use
CF-ABCDE05 expected use / spontaneous use
CF-ABCDE06 Criterion predicate / Resource Requirement predicate
CF-ABCDE07 current Schedule / historical Claim placement
CF-ABCDE08 current Availability / historical Availability basis
CF-ABCDE09 solver V1 result / solver V2 result
CF-ABCDE10 transient candidate cache / consequential retained basis
CF-ABCDE11 eligible / currently feasible
CF-ABCDE12 shareable unavailable result / private cause
```

All tests in this continuation become permanent R2/R3 regression obligations and must be replayed after Slice F and in final Whole-Logical validation.