<!-- LIFEOS-CANONICAL-CONTINUATION document="README.md" follows="README-part-4.md" -->
> **Canonical continuation of the LifeOS Domain Atlas README.** Earlier parts remain preserved. This continuation records Resource Requirement / Allocation v0 integration. Physical split != new logical document.

# 2026-08-15 — Resource Requirement / Allocation v0 integration amendment

Relationships / Reasoning now includes accepted Resource Requirement / Allocation v0 semantics under Domain Validation Methodology v3.

Current canonical decomposition:

```text
Resource Requirement
= what a bounded planning/execution context needs

Candidate Set
= contextual/derived eligibility projection

Resource Allocation
= planned designation/selection of provider/supply/capacity source

Capacity Reservation / Claim
= existing Time / Availability & Capacity semantics for schedulable capacity held/protected

Actual resource use / consumption
= realized reality; not Allocation
```

Critical non-collapse:

```text
Requirement != Resource / Request / Criterion / Allocation
Candidate Set != primitive
Allocation != Capacity Claim / Responsibility / Participation / Authority / Decision / Schedule / Actual
```

The possible sequence `Requirement → Candidate → Allocation → Capacity Claim → Actual` is not a universal state machine. Requirement may exist without candidates/allocation; Allocation may exist without Capacity Claim; Actual use may exist without prior Allocation.

A material Requirement change does not silently carry prior Allocation forward. Reallocation/substitution and correction preserve material history; external/provider disagreement may require Reconciliation rather than overwrite.

No universal Reservation primitive is accepted. Schedulable Capacity Claim remains canonical Time semantics; stock/inventory holds remain future inventory/supply semantics.

Multi-actor hardening remains mandatory: allocating a Person does not create Responsibility, Participation, Agreement, Consent, Acknowledgement or Actual performance. Allocation result visibility may be separated from private eligibility/ranking basis.

AI may discover/rank candidates and propose/perform bounded Allocation under applicable policy/Authority, but recommendation/proposal/ranking does not itself create effective Allocation or Authority.

## Status

```text
RESOURCE REQUIREMENT / ALLOCATION v0
PASS WITH HARDENING

CORE PASS WITH HARDENING
MA PASS WITH HARDENING
XCON PASS WITH HARDENING
ADS COMPLETE
REOPEN 0
UNCLASSIFIED 0
```

Current canonical concept specs:

- `concepts/resource-requirement.md`;
- `concepts/resource-allocation.md`.

Validation checkpoint:

- `checkpoints/resource-requirement-allocation-v0-validation.md`.

This integration does not authorize SQL/API/backend/auth/frontend work, Trigger/policy, inventory/supply reservation, Group/quorum or logical/physical design.

After final post-write propagation QA closes this milestone, the next semantic action is a **fresh Relationships / Reasoning candidate re-score** from the new accepted baseline. No next candidate is preselected here.