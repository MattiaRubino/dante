<!-- LIFEOS-CANONICAL-CONTINUATION document="availability-capacity.md" follows="availability-capacity.md" -->
> **Canonical continuation of `availability-capacity.md`.** The accepted Availability & Capacity v0 specification remains preserved. This amendment records Resource Requirement / Allocation integration only.

# 2026-08-15 — Resource Requirement / Allocation integration

Availability & Capacity continues to own schedulable-resource feasibility and Capacity Reservation / Claim semantics.

Resource Requirement / Allocation v0 clarifies the surrounding planning chain:

```text
Resource Requirement
→ candidate eligibility
→ Resource Allocation
→ optional schedulable Capacity Reservation / Claim
→ Actual use
```

This sequence is possible, not mandatory.

Canonical separation:

```text
Resource Allocation
= planned designation/selection

Capacity Reservation / Claim
= schedulable capacity actually held/protected

Schedule
= accepted temporal assignment of a schedulable subject

Actual use
= realized utilization/execution
```

Therefore:

```text
Allocation != Capacity Claim
Allocation != Schedule
Capacity Claim != Actual use
Schedule != Capacity Claim
```

Allocation may exist while no Capacity Claim is effective. A failed/cancelled Claim does not erase the Allocation that preceded it. In legitimate pool/late-binding cases, schedulable capacity may be claimed before a concrete provider Allocation is selected.

A material Requirement change does not automatically carry an earlier Allocation or Capacity Claim forward. Applicability must be re-evaluated according to the owning Requirement, Version/material-state and applicable policy.

No universal Reservation concept is introduced. Inventory hold, stock reservation and non-temporal supply commitment remain outside Availability & Capacity unless later inventory/supply review proves a shared semantic boundary.

AI may evaluate candidates/capacity and propose allocation/reservation, but recommendation/proposal does not create effective Allocation, Capacity Claim or Authority.

Availability & Capacity remains **CANONICAL / PASS**, with no REOPEN caused by this integration.

Normative references:

- `resource-requirement.md`;
- `resource-allocation.md`;
- `../checkpoints/resource-requirement-allocation-v0-validation.md`.