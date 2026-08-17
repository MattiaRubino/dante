<!-- LIFEOS-CANONICAL-CONTINUATION document="request.md" follows="request.md" -->
> **Canonical continuation of `request.md`.** The accepted Request v0 specification remains preserved. This amendment closes the previously SAFE DEFERRED Resource Requirement / Allocation boundary.

# 2026-08-15 — Resource planning request boundary

Request v0 already established:

```text
Request for a Resource/capability
!= Resource Requirement universally
!= Allocation
!= Reservation / Capacity Claim
!= Actual use
```

Resource Requirement / Allocation v0 now resolves the neighboring semantics.

Canonical decomposition:

```text
Resource Requirement
= what the bounded planning/execution context needs

Request
= an Actor asks recipient(s) for action/information/response/change

Resource Allocation
= the provider/supply/capacity source designated in the plan
```

Therefore:

```text
Request to provide a Resource
!= Resource Requirement automatically

Request to allocate A17
!= effective Allocation

Request to reserve capacity
!= effective Capacity Claim

Request fulfilled
!= Actual use universally
```

The affected domain family owns the resulting state/effect.

Withdrawal/expiry of a Request does not erase a Requirement, Allocation, Capacity Claim or Actual use that independently exists. Conversely, Requirement withdrawal does not automatically erase Request history.

AI/system Requests preserve actual attribution and do not manufacture Allocation Authority.

Request v0 remains **PASS WITH HARDENING, REOPEN = 0**. Its former Resource Requirement / Allocation / Reservation SAFE DEFERRED dependency is now RESOLVED at the semantic boundary; inventory/supply reservation remains separately deferred.

Normative downstream reference: `../checkpoints/resource-requirement-allocation-v0-validation.md`.