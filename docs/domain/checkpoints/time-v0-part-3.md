<!-- LIFEOS-CANONICAL-CONTINUATION document="time-v0.md" follows="time-v0-part-2.md" -->
> **Canonical continuation of the logical Time v0 checkpoint.** `time-v0.md` + `time-v0-part-2.md` + this part remain one logical document. This continuation records only the downstream Resource Requirement / Allocation integration.

# Time v0 — Resource Requirement / Allocation downstream closure

**Date:** 2026-08-15  
**Time verdict:** unchanged — PASS  
**REOPEN:** 0

Resource Requirement / Allocation v0 confirms the Time cluster's existing separation:

```text
Schedule
!= Availability / Capacity
!= Capacity Reservation / Claim
!= Session / Actual
```

It adds the neighboring planning distinction:

```text
Resource Requirement
= what the bounded context needs

Resource Allocation
= which provider/supply/capacity source is designated in the plan

Capacity Reservation / Claim
= what schedulable capacity is actually held/protected
```

Consequences:

- Allocation does not create Schedule.
- Allocation does not prove schedulable capacity is held.
- cancelling/failing a Capacity Claim does not erase the prior Allocation.
- a legitimate pool/late-binding Capacity Claim may precede concrete Allocation.
- material Requirement change does not silently carry prior Allocation/Claim applicability forward.
- Actual use remains reality, not a Time or Allocation rewrite.

The Time cluster's Capacity Claim semantics remain bounded to schedulable capacity. They are **not** generalized into stock/inventory reservation, warehouse commitment or universal Reservation semantics.

No Time identity, recurrence, occurrence, schedule, session, availability or capacity invariant is reopened.

Normative downstream reference: `resource-requirement-allocation-v0-validation.md`.