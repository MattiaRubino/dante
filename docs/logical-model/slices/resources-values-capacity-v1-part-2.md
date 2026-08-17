<!-- LIFEOS-CANONICAL-CONTINUATION document="resources-values-capacity-v1.md" follows="resources-values-capacity-v1.md" -->
> **Canonical continuation of Slice E — Resources / Values / Capacity v1.** The base Slice E specification remains authoritative. This continuation records cumulative A+B+C+D+E hardening only; it does not reopen Slice E or change its selected architecture.

# Slice E — Cumulative Hardening after Integrated A+B+C+D+E Replay

**Status:** hardening accepted locally; remote activation pending  
**Date:** 2026-08-17

## E-H1 — Resource-target addressability is not NativeRef-only

`Resource` remains a contextual role.

A resource-capable target may be:

```text
NativeRef(Person / Asset / Place / other justified native owner)
OR
bounded dependent / value / service / pool / supply / specialist representation
```

according to the containing Reference Contract.

Do not create synthetic native identity merely because something can satisfy a Resource Requirement.

```text
resource target eligibility
!= native identity requirement
```

This preserves Slice A's rule that addressability/role eligibility does not manufacture a universal Entity or Resource root.

## E-H2 — Consequential Allocation / Claim requires reconstructible material basis

Where a Resource Allocation or Capacity Claim is consequential, LifeOS must be able to reconstruct the materially applicable basis used when it became effective or was selected.

Potential basis includes, where relevant:

```text
Resource Requirement MaterialStateRef
Schedule / temporal-footprint MaterialStateRef
Availability basis
Capacity basis
compatibility / policy state
Decision / Authority / Provenance
```

This is not a mandate to duplicate all source state onto the Allocation/Claim record.

Canonical rule:

```text
current input state
!= historical effect basis automatically
```

## E-H3 — Historical Candidate Set is not today's recomputation

Candidate Set remains:

```text
LR-08
```

and is derived/cacheable by default.

However, a current candidate query must never be presented as the exact historical candidate universe considered by an earlier Decision/Allocation unless that equivalence is actually reconstructible.

Where exact historical candidacy is consequential, preserve enough input/evaluation state or a bounded candidate snapshot to reproduce/explain the historical result.

Do not snapshot every transient candidate universe by default.

## E-H4 — `Actual use` wording is narrowed

Slice E's earlier shorthand:

```text
Actual use
```

must be read as:

> **realized resource use / consumption semantics under the appropriate reality owner.**

The Domain concept `Actual` is used only when a prior intended/expected subject is being reconciled with realized reality.

Therefore:

```text
planned A17 -> actually used B
```

may participate in an Actual reconciliation, while spontaneous use with no prior expectation may instead be represented by Session, Observation, Transaction, Inventory Movement or another specialist reality owner.

No retrospective Allocation or fake expectation is manufactured.

## E-H5 — Shared LR-05 machinery does not create one `Rule` owner

The following may all use LR-05 representation mechanics:

```text
Resource Requirement
Criterion
Temporal Constraint
Availability rule/baseline
Conditional Policy
other reviewed bounded specifications
```

but remain separate semantic owners.

Shared technical/logical support may include:

```text
predicate AST / expression machinery
comparison operators
unit-aware conditions
composition helpers
versioning primitives
validation infrastructure
```

where safe.

Forbidden:

```text
Rule(id,type,payload)
as a semantic escape hatch for all specifications
```

Reverse mapping must recover the exact owner and meaning.

## E-H6 — Implicit Requirement becomes material when consequence requires it

Simple-case compactness remains mandatory.

A direct resource use may remain implicit when no independent Requirement lifecycle/history matters.

But once a Requirement materially explains or governs:

```text
Allocation
Claim
Decision
Proposal
historical explanation
governance
reconciliation
correction
```

its applicable state must become reconstructible.

Valid representation may be:

```text
explicit LR-02 + ScopedRecordRef
OR
MaterialStateRef through the containing owner
OR
another typed reconstructible owner-preserving form
```

The historical Requirement cannot be inferred from whatever mutable current fields exist later.

## E-H7 — Capacity Claim history survives Schedule movement

A subordinate Capacity Claim may operationally follow the current accepted Schedule.

Historical truth still requires the previous temporal basis to remain reconstructible.

Where material, use either:

```text
Claim -> Schedule MaterialStateRef
```

or:

```text
Claim-owned accepted temporal footprint/basis
```

No implementation may make all historical claims appear to have always occupied the current Schedule placement.

## E-H8 — Solver / AI reproducibility is consequence-sensitive

Solver/AI remains replaceable computation.

For ordinary transient search/ranking, no durable full solver snapshot is required.

For consequential selection/effect, preserve or reconstruct enough material basis to explain the result, including where relevant:

```text
target / Requirement material state
constraints / criteria / policy
Availability / Capacity states
candidate/source boundary
solver/model/rule version or configuration
selected result
material rationale / score / trade-off
Decision / Authority / Provenance
```

Forbidden extremes:

```text
persist every search node forever
```

and:

```text
opaque solver/AI result with no reconstructible basis
```

## E-H9 — Feasibility ladder remains semantically distinct

The cumulative replay reaffirms:

```text
eligible in principle
!= candidate under current context
!= currently available
!= currently feasible
!= sufficient compatible capacity
!= selected / allocated
!= claimed / reserved
!= realized use / consumption
```

UI/API projections may compress these distinctions only when the underlying semantics remain recoverable.

A universal `available=true/false` must not silently stand in for the entire ladder.

## Technology / mechanism reconsideration

The selected architecture was explicitly re-tested against:

```text
universal Resource/Requirement/Constraint graph
universal Capacity/Claim ledger
fully owner-specific logical model
universal bitemporal/event-sourced planning ledger
snapshot-everything solver audit model
solver-first canonical model
```

Verdict:

```text
Layered Typed Resource Feasibility & Allocation
RETAIN + HARDEN
```

Reusable technical mechanisms remain allowed without semantic unification:

```text
ReferenceAddress
MaterialStateRef
bounded predicate/rule machinery
bounded claim/capacity accounting
owner-specific physical structures
bitemporal/event-history techniques
cache/materialized projections
consequence-sensitive solver input snapshots
specialist inventory/finance extensions
```

## Cumulative Slice E verdict

```text
SLICE E
PASS WITH HARDENING

DOMAIN REOPEN REQUIRED      0
NEW DOMAIN OWNER REQUIRED   0
STRUCTURAL REDESIGN         0
```

This continuation becomes active only when the Integrated A+B+C+D+E package and its remote-QA closure pass.