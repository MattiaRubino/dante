<!-- LIFEOS-CANONICAL-CONTINUATION document="language-map.md" follows="language-map-part-6.md" -->
> **Canonical continuation of the LifeOS Domain & Product Language Map.** Earlier parts remain preserved historical/current payload. This continuation records accepted Resource Requirement / Allocation v0 terminology. Physical split != new logical document.

# 2026-08-15 — Resource Requirement / Allocation language-map amendment

## Canonical terms

### Resource Requirement

**Status:** CANONICAL CONTEXTUAL SEMANTIC FAMILY / CAPABILITY

Use Resource Requirement for what a bounded planning/execution context needs from Resource-capable providers, capacity, services, pools or supply.

```text
Resource Requirement != Request
Resource Requirement != Resource
Resource Requirement != Criterion
Resource Requirement != Quantity
Resource Requirement != Temporal Constraint
Resource Requirement != Allocation
```

Requirement may be explicit or implicit/reconstructible according to consequence. Canonical does not imply a universal entity/table.

### Resource Allocation

**Status:** CANONICAL CONTEXTUAL PLANNED RELATION / STATE

Use Resource Allocation for the provider/supply/capacity source currently designated in the plan to satisfy a bounded Resource Requirement.

```text
Allocation != Candidate Set
Allocation != Capacity Reservation / Claim
Allocation != Responsibility
Allocation != Participation
Allocation != Agreement / Consent
Allocation != Authority
Allocation != Decision
Allocation != Schedule
Allocation != Actual use
```

Simple direct or richer qualified representation may be used later according to history/lifecycle/query needs; neither implies a universal Allocation root.

### Candidate Set

**Status:** DERIVED / CONTEXTUAL PROJECTION

Represents currently eligible/considered providers under the Requirement and available evidence/context.

```text
Candidate Set != primitive
candidate-set change != Requirement revision automatically
```

### Capacity Reservation / Claim

**Status:** EXISTING CANONICAL SCHEDULABLE-CAPACITY SEMANTICS

Owned by Time / Availability & Capacity when capacity is actually held/protected.

Do not generalize it into universal stock/inventory reservation.

### Actual resource use / consumption

**Status:** REALITY / EXECUTION / FUTURE INVENTORY SEMANTICS

```text
Actual use != Allocation
```

Actual use may differ from planned Allocation or occur without one.

## Mandatory sequence boundary

```text
Requirement
→ Candidate
→ Allocation
→ Capacity Claim
→ Actual
```

is a possible workflow, **not** a mandatory state machine.

## Product/UI wording

Natural UI may use terms such as:

- Required equipment;
- Need;
- Suitable options;
- Choose / Assign / Use;
- Reserved;
- Actually used;
- Substitute.

UI wording does not create kernel primitives. In particular `Assigned`, `Booked`, `Reserved` and `Resource` must be mapped to the actual semantic family rather than reused as universal states.

## Rejected universal nouns

Do not canonize:

```text
Universal Requirement root
Universal Allocation root
Universal Reservation root
ResourcePlan mega-root
Booking mega-root
ResourceAssignment mega-root
CandidateSet entity/root
```

## History/materiality

```text
material Requirement change
!= automatic Allocation carry-forward

reallocation/substitution
!= rewrite prior Allocation history

correction
!= silent overwrite
```

Version/Reconciliation/Provenance remain separate.

## Multi-actor/privacy

```text
allocated Person
!= responsible Actor
!= participant
!= Agreement / Consent
!= actual performer

Allocation visible
!= private eligibility/ranking basis visible
```

## SAFE DEFERRED vocabulary

Still deferred:

- Requirement composition all/any/alternatives;
- pool/late-binding mechanics;
- non-temporal inventory/stock reservation;
- inventory movement/consumption;
- Trigger/policy fallback/reallocation;
- collective/group allocation;
- exact logical/physical/API representation.

Normative references:

- `concepts/resource-requirement.md`;
- `concepts/resource-allocation.md`;
- `checkpoints/resource-requirement-allocation-v0-validation.md`.