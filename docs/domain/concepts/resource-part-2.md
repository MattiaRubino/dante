<!-- LIFEOS-CANONICAL-CONTINUATION document="resource.md" follows="resource.md" -->
> **Canonical continuation of `resource.md`.** The base Resource v0 specification remains preserved. This continuation records the downstream closure of Resource Requirement / Allocation v0. Physical split != new logical document.

# 2026-08-15 — Resource Requirement / Allocation downstream closure

Resource v0 originally established the separation:

```text
Requirement
→ Candidate
→ Allocation
→ Reservation / Capacity Claim
→ Actual use / consumption
```

while leaving Requirement/Allocation/Reservation details SAFE DEFERRED. Resource Requirement / Allocation v0 now closes the reusable Requirement and Allocation boundary without reopening Resource.

Current canonical decomposition:

```text
Resource
= contextual provider eligibility/capability role

Resource Requirement
= what a bounded planning/execution context needs

Candidate Set
= contextual/derived eligibility projection

Resource Allocation
= planned designation/selection of provider/supply/capacity source

Capacity Reservation / Claim
= accepted schedulable-capacity commitment semantics

Actual use / consumption
= realized reality; not Allocation
```

Mandatory non-collapse:

```text
Resource != Requirement
Resource != Candidate Set
Resource != Allocation
Resource != Capacity Claim
Resource != Actual use
```

Resource/provider identity is never manufactured by Requirement or Allocation. A Person, Asset, future Place/service, pool or supply retains its independently justified semantics while playing Resource role.

A Candidate Set is not a new primitive. Candidate-set change does not automatically revise Requirement identity.

Allocation may exist without Capacity Claim; Actual use may exist without prior Allocation; schedulable Capacity Claim may legitimately precede concrete Allocation in late-binding/pool cases.

Non-temporal inventory/stock reservation remains independently SAFE DEFERRED. It is not automatically the Time cluster's Capacity Reservation / Claim.

Material Requirement change does not silently carry prior Allocation forward. Reallocation/substitution and correction preserve material history and Provenance; external/provider disagreement may require Reconciliation rather than overwrite.

Resource v0 remains **PASS WITH HARDENING, REOPEN = 0**.

Normative downstream references:

- `resource-requirement.md`;
- `resource-allocation.md`;
- `../checkpoints/resource-requirement-allocation-v0-validation.md`.