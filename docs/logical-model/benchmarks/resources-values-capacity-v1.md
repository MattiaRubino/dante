# External Benchmark — Resources / Values / Capacity v1

**Status:** Current benchmark evidence for Slice E  
**Date:** 2026-08-17  
**Policy:** External systems are evidence, not LifeOS ontology authority.

## 1. Benchmark objective

The benchmark tests whether LifeOS should collapse or preserve distinctions among:

- requirement;
- candidate feasibility;
- allocation;
- capacity;
- availability;
- reservation/claim;
- actual use;
- fungible stock;
- individually tracked identity;
- scalar quantity;
- monetary amount.

The benchmark deliberately includes systems far from personal productivity so that common mechanisms are pressure-tested rather than copied.

## 2. Kubernetes resource management

### SOURCE
Kubernetes official documentation — resource requests and limits.

### PROBLEM
Schedule workloads against finite CPU/memory capacity while preserving runtime resource constraints and observed usage.

### MECHANISM
Kubernetes separates resource request, limit, node capacity/allocatable resources and actual runtime consumption. The scheduler reasons primarily from requests rather than treating actual use as the same state.

### INVARIANT / INSIGHT

```text
requested capacity
!= resource limit
!= node capacity
!= actual utilization
```

A planned/declared demand is not actual consumption.

### LIMITATION / ANTI-PATTERN
CPU/memory scheduling is much more uniform than heterogeneous human/physical/service eligibility in LifeOS. It does not justify reducing all requirements to numeric capacity.

### LIFEOS DISPOSITION
RETAIN separation of Requirement, Capacity, Claim/commitment and Actual use. Do not import Kubernetes resource ontology as a universal model.

### REOPEN IMPACT
None.

## 3. HashiCorp Nomad scheduling

### SOURCE
Nomad official scheduling/resources documentation.

### PROBLEM
Match task requirements to feasible nodes/devices, rank placements, then create allocations.

### MECHANISM
Nomad evaluates CPU/memory/device/network requirements, feasibility filters, ranking and resulting allocations as distinct stages/mechanisms.

### INVARIANT / INSIGHT

```text
requirements / constraints
-> feasibility
-> ranking
-> allocation
```

The optimization stage does not itself define the semantic identity of resources.

### LIMITATION / ANTI-PATTERN
Infrastructure schedulers operate on narrower machine-resource vocabularies and cannot represent LifeOS governance, privacy, Person/Asset/Place semantics or subjective preferences without additional domain owners.

### LIFEOS DISPOSITION
Support replaceable solver/feasibility computation over canonical domain state; solver result remains proposal/candidate until effective Allocation semantics are satisfied.

### REOPEN IMPACT
None.

## 4. Google OR-Tools

### SOURCE
Google OR-Tools official optimization documentation.

### PROBLEM
Solve assignment/scheduling/resource-allocation problems under constraints and objectives.

### MECHANISM
Variables, constraints, objective functions, feasible solutions and solver results are computational constructs. Different solvers may represent the same business problem differently.

### INVARIANT / INSIGHT
Optimization representation is replaceable and should not become the canonical business/domain state model.

### LIMITATION / ANTI-PATTERN
A solver model can tempt implementers to persist solver variables/solution structures as if they were semantic truth.

### LIFEOS DISPOSITION
REJECT solver-first canonical model. RETAIN solver as derived computation layer that may propose candidates/allocations.

### REOPEN IMPACT
None.

## 5. AWS EC2 Capacity Reservations

### SOURCE
AWS official EC2 Capacity Reservation documentation.

### PROBLEM
Reserve compute capacity independently from immediate utilization.

### MECHANISM
Capacity may be reserved and remain unused. Reservation state and utilization are distinguishable; quotas also constrain what can be reserved.

### INVARIANT / INSIGHT

```text
capacity available
!= quota
!= reservation/claim
!= actual use
```

### LIMITATION / ANTI-PATTERN
Cloud compute reservations are domain-specific and usually simpler than LifeOS compatibility/Authority/Visibility semantics.

### LIFEOS DISPOSITION
RETAIN Availability/Capacity/Claim/Actual separation. Do not generalize cloud reservation identity to all LifeOS resources.

### REOPEN IMPACT
None.

## 6. Azure Capacity Reservation

### SOURCE
Microsoft Azure official capacity-reservation documentation.

### PROBLEM
Reserve VM capacity subject to both quota and real infrastructure capacity.

### MECHANISM
Reservation creation can fail because quota is insufficient or because required physical capacity is unavailable.

### INVARIANT / INSIGHT
Quota and effective capacity are separate dimensions.

### LIFEOS DISPOSITION
Reinforces that Capacity is contextual and potentially multidimensional; a single universal `available=true` or percentage is insufficient.

### REOPEN IMPACT
None.

## 7. Google Cloud reservations

### SOURCE
Google Cloud official Compute Engine reservations documentation.

### PROBLEM
Reserve VM capacity for later use.

### MECHANISM
Capacity availability is checked at reservation creation; reservation and quota are separate constraints.

### INVARIANT / INSIGHT
Reservation is a commitment over capacity, not the same thing as capacity itself or actual consumption.

### LIFEOS DISPOSITION
Supports bounded Capacity Claim semantics without universalizing reservation across all domains.

### REOPEN IMPACT
None.

## 8. Google Calendar FreeBusy

### SOURCE
Google Calendar API official Freebusy documentation.

### PROBLEM
Answer availability/busy queries across calendars.

### MECHANISM
Freebusy is exposed as query output rather than a durable canonical object for every free interval.

### INVARIANT / INSIGHT
Effective availability can be a projection over richer source events/state rather than persisted as a giant slot ledger.

### LIMITATION / ANTI-PATTERN
Binary busy/free is lossy relative to LifeOS compatible-capacity semantics and does not express private-reason governance by itself.

### LIFEOS DISPOSITION
RETAIN effective Availability/free capacity as LR-08 derived projection by default.

### REOPEN IMPACT
None.

## 9. Odoo Inventory forecasting/reservations

### SOURCE
Odoo official Inventory documentation.

### PROBLEM
Track on-hand quantities, incoming/outgoing stock, reservations and forecasted availability.

### MECHANISM
Inventory distinguishes on-hand, reserved, incoming, outgoing and forecasted quantities rather than treating them as one `available` value.

### INVARIANT / INSIGHT

```text
on hand
!= reserved
!= forecasted
!= incoming/outgoing movement
```

### LIMITATION / ANTI-PATTERN
Warehouse stock semantics are specialist. Treating people, attention, rooms and services as warehouse inventory would be a semantic collapse.

### LIFEOS DISPOSITION
RETAIN specialist LR-13 inventory boundary. Do not collapse stock reservation into schedulable Capacity Claim universally.

### REOPEN IMPACT
None.

## 10. Odoo serial and lot tracking

### SOURCE
Odoo official serial-number and lot-tracking documentation.

### PROBLEM
Distinguish individually tracked items from batches/fungible stock.

### MECHANISM
Serial numbers identify specific items; lot/batch tracking groups quantities without requiring every physical unit to receive an independent identity.

### INVARIANT / INSIGHT

```text
individual tracked identity
!= fungible quantity
```

### LIFEOS DISPOSITION
Supports Asset NativeRef for individually tracked objects while keeping bulk/consumable supply quantity-based unless specialist identity is justified.

### REOPEN IMPACT
None.

## 11. UCUM

### SOURCE
Unified Code for Units of Measure official specification.

### PROBLEM
Represent units in a computable, unambiguous way.

### MECHANISM
Standardized unit symbols and algebra support conversions while leaving the measured domain property outside the unit token.

### INVARIANT / INSIGHT
Unit semantics can be reusable value machinery without making units or quantities independent domain roots.

### LIMITATION / ANTI-PATTERN
Dimensional compatibility does not prove full domain-semantic comparability or valid aggregation.

### LIFEOS DISPOSITION
RETAIN Quantity as LR-04; use standards as vocabulary/technical support, not ontology authority.

### REOPEN IMPACT
None.

## 12. HL7 FHIR Quantity / Money

### SOURCE
HL7 FHIR R5 official datatype documentation.

### PROBLEM
Represent measured quantities and monetary values accurately across clinical/administrative contexts.

### MECHANISM
FHIR exposes Quantity-like value types and Money separately, acknowledging currency-bearing values as distinct from ordinary physical-unit quantities.

### INVARIANT / INSIGHT
Shared numeric infrastructure need not imply semantic collapse between Quantity and MonetaryAmount.

### LIMITATION / ANTI-PATTERN
FHIR is a healthcare interoperability model and is not LifeOS domain authority.

### LIFEOS DISPOSITION
RETAIN separate LR-04 families for Quantity and MonetaryAmount.

### REOPEN IMPACT
None.

## 13. Stripe currency representation

### SOURCE
Stripe official currency documentation.

### PROBLEM
Represent monetary values across currencies with different minor-unit rules.

### MECHANISM
Currency code and currency-specific amount conventions are required for correct API-level representation.

### INVARIANT / INSIGHT
Currency is intrinsic to monetary value representation and cannot safely be treated as an arbitrary ordinary unit string.

### LIMITATION / ANTI-PATTERN
Payment API encoding rules do not define LifeOS financial ontology.

### LIFEOS DISPOSITION
Supports MonetaryAmount separation and later currency-aware physical implementation.

### REOPEN IMPACT
None.

## 14. Cross-source synthesis

The strongest shared pattern is not a universal `Resource` table. It is a sequence of separable concerns:

```text
need / requirement
-> feasibility / candidate evaluation
-> selection / allocation
-> commitment / claim where applicable
-> actual utilization / movement / consumption
```

Across mature systems:

- demand is not actual use;
- reservation is not capacity;
- capacity is not quota;
- free/busy is often derived;
- inventory stock and schedulable capacity have different specialist semantics;
- individually tracked identity differs from fungible quantity;
- optimization models are replaceable computation;
- value infrastructure may be shared without semantic unification.

## 15. Anti-patterns rejected for LifeOS

```text
universal Resource identity root
one available/busy flag for all capacity
persist every derived free slot as source truth
one Reservation semantic root for time and stock
solver output as canonical truth
provider IDs as LifeOS identity
per-unit Asset identity for fungible supply
one number+unit wrapper for both Quantity and Money
current FX silently rewriting historical conversions
```

## 16. Benchmark verdict

```text
EXTERNAL BENCHMARK
PASS

PREFERRED LIFEOS DIRECTION
Layered Typed Resource Feasibility & Allocation

DOMAIN REOPEN IMPACT
0
```
