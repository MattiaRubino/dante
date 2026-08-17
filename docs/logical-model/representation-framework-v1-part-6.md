<!-- LIFEOS-CANONICAL-CONTINUATION document="representation-framework-v1.md" follows="representation-framework-v1-part-5.md" -->
> **Canonical continuation of the single Logical Representation Framework v1 document.** Earlier representation roles and rules remain authoritative. This continuation records Slice E only.

# Slice E integration — Resources / Values / Capacity

## E.1 Resource-role addressing

`Resource` remains a contextual role and does not receive an independent ReferenceAddress family.

```text
native provider ReferenceAddress
+ bounded Resource role/context
-> resource-capable reference
```

Examples:

```text
NativeRef(Person)
NativeRef(Asset)
NativeRef(Place)
```

retain their native identity when used for resource matching/allocation.

Forbidden:

```text
ResourceRef wrapping NativeRef
universal resources root
provider/resource re-identification merely for planning
```

## E.2 Resource Requirement

Default logical role:

```text
LR-05 Rule / policy / specification semantics
```

Escalate to:

```text
LR-02 Dependent semantic record
+ ScopedRecordRef
```

only when history, version binding, governance, reconciliation, alternatives/late binding or consequential queryability require a material record.

Simple-case compactness remains mandatory.

## E.3 Candidate Set

```text
Candidate Set
-> LR-08 Derived projection / read model
```

Candidate projection may be recomputed, cached or materialized for performance without becoming canonical source truth.

A candidate-set change does not itself imply Requirement revision.

## E.4 Resource Allocation

Default logical role:

```text
LR-03 Typed association / relation record
```

Escalate to:

```text
LR-02 + ScopedRecordRef
```

where material history, reallocation, quantity detail, governance, reconciliation or provenance makes the qualified relation independently addressable.

Allocation remains separate from Capacity Claim and Actual use.

## E.5 Availability

Reusable baseline/rule:

```text
LR-05
```

Material override/fact:

```text
LR-02 where persistence/history is required
```

Effective free/busy/availability result:

```text
LR-08
```

Do not persist a derived free-slot grid as canonical source merely because it is convenient for reads.

## E.6 Capacity

Capacity is contextual capability/state rather than independent identity.

Use:

```text
LR-04 for typed scalar/count/amount dimensions
LR-05 for compatibility / policy / rule semantics
LR-02 for bounded material contextual state where consequence requires history/addressability
LR-08 for effective remaining capacity projections
```

No universal `CapacityRef` is introduced.

## E.7 Capacity Claim

Capacity Reservation / Claim is a qualified commitment over schedulable capacity.

Default:

```text
LR-03
```

Escalate to:

```text
LR-02 + ScopedRecordRef
```

when the claim itself has material lifecycle/history or is a standalone capacity-only subject.

Do not infer a universal stock/inventory Reservation semantic root from this mechanism.

## E.8 Quantity and MonetaryAmount

```text
Quantity       -> LR-04
MonetaryAmount -> LR-04
```

They may share physical scalar infrastructure but remain distinct semantic families.

```text
MonetaryAmount != Quantity
FX conversion != ordinary unit conversion
```

## E.9 Specialist resource extensions

Inventory, stock movements, lots/serials, financial accounts/transactions and specialist booking systems remain:

```text
LR-13 Specialist extension records
```

where concrete product scope justifies them.

They may reuse common technical infrastructure without becoming kernel superclasses.

## E.10 Solver boundary

Solver/AI representations are not new logical role families.

Use them as computation over canonical/authorized state, producing:

```text
LR-08 candidate/feasibility/ranking projections
```

until a domain-owned Proposal/Decision/Allocation/Claim transition makes an effect canonical under applicable Authority.

## E.11 Slice-E representation invariants

```text
shared logical machinery != shared semantic superclass
role reference != duplicate identity
candidate projection != canonical state
allocation != claim
claim != actual use
availability projection != source truth
capacity != one universal scalar
fungible supply != per-unit identity
Quantity != MonetaryAmount
solver output != canonical effect
```

Slice E introduces no new universal ReferenceAddress kind and no semantic-free fallback.