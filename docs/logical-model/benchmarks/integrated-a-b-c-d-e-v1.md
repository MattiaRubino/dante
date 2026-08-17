# External Benchmark — Integrated A+B+C+D+E v1

**Status:** cumulative benchmark / mechanism-reconsideration evidence  
**Date:** 2026-08-17  
**Policy:** external systems are evidence and anti-pattern sources, never LifeOS ontology authority.

## 1. Objective

The cumulative checkpoint asks a narrower question than the individual slice benchmarks:

> After Identity, Intention/Execution, Time/Reality, Evidence/Knowledge/History and Resources/Capacity have been combined, does a different technical/logical architecture now dominate strongly enough to justify replacing the layered typed model before Slice F?

The benchmark therefore focuses on:

```text
historical effect reproducibility
solver / planner replaceability
candidate-universe history
state drift / stale plans
rule/specification reuse without ontology collapse
capacity/claim accounting boundaries
simple-case compactness vs high-consequence auditability
```

## 2. Terraform saved-plan principle

### SOURCE
HashiCorp Terraform official planning/apply documentation and saved-plan behavior.

### PROBLEM
A computed plan is reviewed against a particular configuration/state basis and later applied. The surrounding state may drift after the plan was produced.

### MECHANISM / LESSON
A saved plan preserves the exact planned actions calculated from a material input basis. A previously generated plan may become stale/inapplicable when the real state no longer matches the assumptions against which it was calculated.

### LIFEOS INVARIANT ADAPTED

```text
consequential computed effect
must remain attributable to the material basis used then

current state
!= historical computation basis automatically
```

This supports:

- `MaterialStateRef` binding for consequential Requirement/Availability/Capacity inputs;
- historical Schedule basis for Capacity Claims;
- consequence-sensitive capture of solver/model configuration;
- explicit stale/re-evaluation semantics rather than silent reinterpretation.

### WHAT LIFEOS DOES NOT COPY

LifeOS does not treat a Terraform plan file, infrastructure state model or resource graph as a universal domain structure.

### DISPOSITION
ADAPT principle only.

## 3. Google OR-Tools solver-family principle

### SOURCE
Google OR-Tools official optimization documentation.

### PROBLEM
Represent assignment, scheduling and constrained optimization problems using different solver families and problem formulations.

### MECHANISM / LESSON
Variables, constraints, objective functions, feasible solutions and solver outputs are computational artifacts. Different solver families can solve materially similar business problems with different internal representations.

### LIFEOS INVARIANT ADAPTED

```text
solver representation
!= canonical LifeOS semantic representation

solver result
!= effective Allocation automatically

solver engine/version
may change without changing domain identity
```

This strongly rejects a solver-first canonical model and supports consequence-sensitive audit/replay metadata instead.

### DISPOSITION
RETAIN computation-layer boundary.

## 4. Kubernetes / Nomad resource-scheduling pattern

### SOURCES
Kubernetes and HashiCorp Nomad official scheduling/resource documentation.

### PROBLEM
Match declared requirements against constrained capacity, filter/rank candidates and establish allocations.

### MECHANISM / LESSON
Mature schedulers keep meaningful distinctions among:

```text
requirement/request
capacity
feasibility
candidate/ranking
allocation
runtime use
```

Nomad further provides a strong example of feasibility/ranking preceding Allocation without requiring the ranking representation to become canonical business identity.

### LIFEOS INVARIANT ADAPTED

The cumulative feasibility ladder remains separate:

```text
eligible
candidate
available
feasible
sufficient capacity
allocated
claimed
realized use
```

### LIMITATION
Machine schedulers have narrower, more numeric resource vocabularies and do not carry LifeOS Person/Asset/Place, privacy, Authority, intention or knowledge semantics.

### DISPOSITION
ADAPT separation, reject ontology copying.

## 5. Cloud capacity-reservation pattern

### SOURCES
AWS EC2, Microsoft Azure and Google Cloud official capacity-reservation documentation.

### PROBLEM
Hold scarce capacity for later use while separating reservation, quota, actual infrastructure capacity and utilization.

### LESSON

```text
capacity
!= quota
!= reservation/claim
!= allocation/selection
!= utilization
```

This remains consistent with Slice E and provides no evidence for a universal Resource/Reservation root.

### DISPOSITION
RETAIN bounded Capacity Claim/accounting mechanism only.

## 6. Google Calendar FreeBusy projection pattern

### SOURCE
Google Calendar API official Freebusy documentation.

### PROBLEM
Answer effective busy/availability queries without treating every free interval as an independent authoritative record.

### LESSON

```text
effective free/busy projection
can be derived from richer source state
```

This supports `LR-08` for effective Availability/free-capacity views and argues against a giant canonical free-slot ledger.

### CUMULATIVE HARDENING
A current free/busy recomputation cannot be substituted for the historical Availability basis used by an earlier consequential planner/Decision unless that basis is reconstructible.

### DISPOSITION
RETAIN derived projection + material historical input binding where consequential.

## 7. Odoo inventory / serial / lot pattern

### SOURCE
Odoo official Inventory documentation.

### PROBLEM
Track fungible stock, reservations, forecast quantities and individually tracked items.

### LESSON

```text
fungible quantity
!= individually tracked identity

stock reservation
!= generic schedulable capacity claim automatically
```

This continues to support LR-13 specialist inventory boundaries.

### DISPOSITION
No cumulative architecture change.

## 8. UCUM / FHIR Quantity-Money / Stripe pattern

### SOURCES
UCUM official specification, HL7 FHIR R5 datatype documentation, Stripe official currency documentation.

### LESSON
Reusable scalar/unit infrastructure can be shared while preserving distinct semantic value families.

```text
shared representation machinery
!= shared semantic owner
```

This principle generalizes beyond values and directly supports ABCDE-H05:

```text
shared LR-05 predicate/rule machinery
!= universal Rule ontology root
```

### DISPOSITION
ADAPT mechanism/semantic-owner separation.

## 9. Cross-system synthesis

The strongest cumulative external pattern is not a universal graph or ledger. It is **layering**:

```text
stable domain identity / source state
+
typed specifications / requirements / constraints
+
derived computation / candidate evaluation
+
explicit consequential effect
+
historical input/result attribution where needed
```

Across mature systems, optimization and projection are frequently replaceable while consequential state must remain attributable to the material basis that produced it.

This aligns with:

```text
ReferenceAddress
MaterialStateRef
LR-05 owner-specific specifications
LR-08 derived projections
LR-03/LR-02 consequential Allocation/Claim
owner-specific history/provenance
```

without requiring a universal semantic superclass.

## 10. Architectures reopened

### A — Layered typed model + bounded historical input bindings

**Strengths:** preserves owner semantics, simple-case compactness, historical explainability and solver replaceability.

**Verdict:** `RETAIN + HARDEN`.

### B — Universal Resource / Requirement / Constraint graph

**Attraction:** uniform traversal and generic solver integration.

**Failure:** turns technical commonality into semantic root; weakens reverse mapping and owner-specific invariants.

**Verdict:** `REJECT`.

### C — Universal Capacity / Claim / Reservation ledger

**Attraction:** strong accounting/concurrency mechanics.

**Failure:** not expressive enough for heterogeneous eligibility/Requirement semantics and collapses specialist stock vs schedulable capacity.

**Verdict:** `REJECT AS WHOLE KERNEL`; retain bounded mechanism.

### D — Fully owner-specific logical structures

**Attraction:** direct semantics and strong FK-style typing.

**Failure as logical baseline:** duplicates cross-domain addressability/history/rule/solver mechanisms and makes extension harder.

**Verdict:** `RETAIN AS PHYSICAL INGREDIENT`.

### E — Universal bitemporal/event-sourced planning ledger

**Attraction:** excellent chronology/replay properties.

**Failure as ontology:** valid/transaction time or immutable events do not define semantic owner, identity, Authority, visibility, applicability or resource meaning.

**Verdict:** `REJECT AS LOGICAL REQUIREMENT`; retain as serious Physical Model technique.

### F — Snapshot every solver run completely

**Attraction:** maximal replayability.

**Failure:** high storage/operational cost, solver lock-in and violation of simple-case compactness; captures computation trivia rather than only material business basis.

**Verdict:** `REJECT`.

### G — Solver-first canonical model

**Attraction:** direct optimization implementation.

**Failure:** solver variables/constraints are replaceable computational artifacts and cannot own LifeOS semantic truth.

**Verdict:** `REJECT`.

## 11. Benchmark impact on cumulative hardening

```text
ABCDE-H01 supported by heterogeneous resource/specialist patterns
ABCDE-H02 strongly supported by saved-plan/material-basis principle
ABCDE-H03 supported by state/candidate drift across planning systems
ABCDE-H04 supported by execution-vs-observation/specialist owner separation
ABCDE-H05 supported by shared-mechanism != shared-owner patterns
ABCDE-H06 follows consequence-sensitive materialization principle
ABCDE-H07 supported by plan/state drift and historical basis preservation
ABCDE-H08 strongly supported by solver replaceability + saved-plan reproducibility
```

## 12. Benchmark verdict

```text
EXTERNAL CUMULATIVE BENCHMARK
PASS

PREFERRED DIRECTION
Layered Typed Logical Model
+ ReferenceAddress
+ MaterialStateRef
+ consequence-sensitive historical input bindings

TECHNOLOGY RECONSIDERATION
RETAIN + HARDEN

DOMAIN REOPEN IMPACT
0

STRUCTURAL REDESIGN REQUIRED
0
```
