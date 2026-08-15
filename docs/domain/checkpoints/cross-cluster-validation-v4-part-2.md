<!-- LIFEOS-CANONICAL-CONTINUATION document="cross-cluster-validation-v4.md" follows="cross-cluster-validation-v4.md" -->
> **Canonical continuation of `cross-cluster-validation-v4.md`.** The original Clusters 1–4 cross-cluster validation remains preserved. This continuation records downstream Resource Requirement / Allocation regression only.

# Cross-Cluster Validation v4 — Resource Requirement / Allocation regression

**Date:** 2026-08-15  
**Prior Clusters 1–4 verdicts:** unchanged  
**Structural reopenings:** 0

Resource Requirement / Allocation v0 was regressed against all accepted cluster boundaries.

## Cluster 1 — Intention / Execution

```text
Goal / Plan / Activity / Event identity
!= Resource Requirement
!= Resource Allocation
```

Plan/Activity/Event may own or contextualize a Requirement, but provider selection/reallocation does not redefine their identity automatically.

**PASS.**

## Cluster 2 — Time

```text
Allocation != Schedule
Allocation != Availability / Capacity
Allocation != Capacity Reservation / Claim
Capacity Claim != Actual use
```

Capacity Claim remains schedulable-capacity semantics only. Inventory hold is not generalized into Time.

**PASS WITH HARDENING.**

## Cluster 3 — Observed Reality / Evidence

```text
Allocation != Actual
Allocation != Outcome
candidate/evaluation data != Evidence truth automatically
correction != overwrite
```

Actual provider/use may differ from Allocation or occur without it. Provenance/Reconciliation preserve material correction history.

**PASS WITH HARDENING.**

## Cluster 4 — Data / Subjects

```text
Resource role != provider identity
Requirement != Resource
Candidate Set != primitive
Allocation != Resource identity
Person allocated != Responsibility / Participation / Agreement / Consent
```

Quantity, Person, Asset, Actor, Subject and Resource boundaries remain intact. Consumable supply still requires no synthetic per-unit identity.

**PASS WITH HARDENING.**

## Cross-cluster chronology regression

The following remain independently reconstructible where consequential:

```text
what was required
what candidates were known/derived
what provider was allocated
what schedulable capacity was held
what changed materially
what was actually used
what was later corrected/reconciled
```

No candidate computation is required to be persisted universally.

## Destructive regression

Rejected without reopening prior clusters:

- Requirement = Resource;
- Requirement = Request;
- Requirement = Criterion;
- Allocation = Resource;
- Allocation = Capacity Claim;
- Allocation = Responsibility;
- Allocation = Participation;
- Allocation = Actual;
- Candidate Set root;
- universal Reservation;
- ResourcePlan / Booking / ResourceAssignment mega-root;
- mandatory end-to-end state machine.

## Result

```text
CROSS-CLUSTER RRA REGRESSION
PASS WITH HARDENING

Clusters 1–4 structural REOPEN = 0
RRA REOPEN                    = 0
UNCLASSIFIED                  = 0
```

Normative reference: `resource-requirement-allocation-v0-validation.md`.