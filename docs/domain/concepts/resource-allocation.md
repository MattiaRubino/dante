# Resource Allocation v0

**Status:** ACCEPTED v0 — PASS WITH HARDENING  
**Accepted:** 2026-08-15  
**Cluster:** Relationships / Reasoning  
**Validation:** `../checkpoints/resource-requirement-allocation-v0-validation.md`

## Definition

> **Resource Allocation is the contextual planned designation or selection of one or more eligible providers, supplies or capacity sources intended to satisfy a bounded Resource Requirement.**

It answers:

> **Which provider/supply/capacity source is currently designated in the plan to satisfy this Requirement, under which materially relevant context?**

Allocation is planning semantics. It does not manufacture provider identity and does not prove that capacity was held, that the provider agreed, that execution occurred, or that the selected provider was ultimately used.

---

## 1. Canonical non-collapse

```text
Resource Allocation != Resource
Resource Allocation != Candidate Set
Resource Allocation != Capacity Reservation / Claim
Resource Allocation != Schedule
Resource Allocation != Responsibility
Resource Allocation != Participation
Resource Allocation != Agreement
Resource Allocation != Consent
Resource Allocation != Authority
Resource Allocation != Decision
Resource Allocation != Proposal
Resource Allocation != Request
Resource Allocation != Actual use / consumption
```

A Decision may select an Allocation. A Proposal may propose it. A Request may ask for it. Applicable Authority/policy may govern whether it becomes effective in a shared context. None of those semantics is the Allocation itself.

---

## 2. Allocation and Capacity Claim

For schedulable capacity:

```text
Allocation
= what the plan designates

Capacity Reservation / Claim
= what schedulable capacity is actually held/protected
```

They may coincide operationally in simple flows but remain semantically distinct.

Valid states include:

```text
Allocation = A17
Capacity Claim = none
```

and, in legitimate pool/late-binding flows:

```text
Capacity Claim = pool capacity held
concrete Allocation = later
```

Cancelling or failing a Capacity Claim does not automatically erase the Allocation that led to it.

The accepted Time/Availability & Capacity semantics apply only to schedulable capacity. Non-temporal inventory/stock holds remain independently deferred and must not be forced into a universal Reservation concept.

---

## 3. Allocation and Actual use

```text
planned Allocation
!= Actual use
```

Actual use may differ from the plan:

```text
Allocation: A18
Actual use: Rental Z
```

This does not require rewriting the historical Allocation.

Actual use may also occur without a prior effective Allocation. LifeOS must not invent a retrospective Allocation merely to make the history look orderly.

For quantities:

```text
allocated quantity = 500 ml
actual consumed     = 430 ml
```

Both facts remain independently reconstructible where material.

---

## 4. Material Requirement change

Allocation binds to the materially relevant Requirement state where consequence requires it.

```text
Requirement state S1
→ Allocation A1 = A17

Requirement materially changes to S2
```

A1 does not automatically apply to S2.

The prior Allocation remains historically true for S1 and may need reevaluation, replacement or supersession.

Canonical rule:

```text
material Requirement change
!= automatic Allocation carry-forward
```

---

## 5. Reallocation and substitution

A later Allocation does not rewrite a materially relevant earlier Allocation.

```text
S1 → A17
S2 → A18
```

must not collapse into:

```text
Requirement always → A18
```

Last-minute substitution may be represented by a later effective Allocation when one truly occurred, or only by Actual use when reality changed without a formal/planned reallocation.

---

## 6. Correction and Reconciliation

A recorded Allocation may later prove wrong.

Example:

```text
earlier recorded assertion: Room A
later reliable correction: Room B was actually selected
```

Where material, LifeOS preserves:

- the earlier assertion;
- the later corrected current understanding;
- materially relevant Provenance;
- the reconciliation/correction basis.

Correction is not silent overwrite.

Allocation may also temporarily disagree with external/provider state, for example when LifeOS removes an Allocation while an external reservation remains active. Such inconsistency may require Reconciliation/corrective action; Allocation does not own provider reservation truth.

---

## 7. Person as allocated Resource

When a Person is selected as Resource provider:

```text
Allocation: Anna
```

does not imply:

```text
Anna agreed
Anna consented
Anna participates
Anna is responsible
Anna has acknowledged it
Anna is actual performer
```

Those states belong to their own semantic families.

Account presence is not required for allocation semantics.

---

## 8. Authority, Visibility and Representation

Allocation itself does not grant Authority.

A shared/canonical Allocation may require applicable Authority/policy to become effective. The Actor who chooses, records, proposes, requests or executes an Allocation may differ from the represented party and from the Authority holder.

Visibility remains independently governed:

- Allocation result visibility;
- candidate-list visibility;
- private matching/qualification basis;
- Requirement details;
- provider identity/details;
- history/rationale.

An authorized bounded result may be exposed while private eligibility evidence remains hidden.

---

## 9. AI boundary

AI may:

- discover candidates;
- evaluate compatibility;
- rank candidates;
- propose an Allocation;
- perform an Allocation under explicit bounded authorized policy.

Canonical barriers:

```text
AI ranking != Allocation
AI proposal != effective Allocation
AI optimization != Authority
AI access to private eligibility data != disclosure permission
```

Where an AI/system is the actual Actor, attribution and applicable policy/Authority basis remain truthful where material.

---

## 10. Persistence guardrail

Allocation is canonical contextual relation/state semantics, not a universal root/table/workflow.

Simple direct representation may be sufficient when history/lifecycle/qualification is immaterial. Rich qualified representation may be needed when there is:

- material Requirement version binding;
- reallocation/substitution history;
- multi-provider allocation;
- quantity/capacity detail;
- governance;
- reconciliation;
- privacy;
- provenance;
- consequential queryability.

Qualified structure does not by itself establish independent domain identity.

---

## 11. Canonical invariants

```text
Allocation != Candidate
Allocation != Capacity Reservation / Claim
Allocation != Actual use
Allocation may exist without Reservation
Actual use may exist without prior Allocation
schedulable Capacity Claim may precede concrete Allocation in legitimate late-binding cases
non-temporal inventory reservation != Capacity Claim automatically
material Requirement change != automatic Allocation carry-forward
reallocation/substitution preserves material prior history
failed/cancelled reservation != erase Allocation
correction preserves Provenance/history where material
provider/external disagreement may require Reconciliation, not overwrite
allocating Person != Responsibility / Participation / Agreement / Consent
Proposal/Request for Allocation != effective Allocation
Allocation requires applicable Authority/policy where governed effect requires it
provider identity is never manufactured by Allocation
no universal Allocation/ResourcePlan/Booking/ResourceAssignment root
no mandatory Requirement→Candidate→Allocation→Reservation→Actual state machine
persistence/materialization is consequence-sensitive
```

---

## 12. SAFE DEFERRED neighbors

Independently owned future work remains:

- exact Allocation lifecycle/cardinality;
- pool/late-binding physical/logical mechanics;
- automatic fallback/reallocation under Trigger/policy;
- collective/group allocation mechanics;
- specialist booking/source-of-record behavior;
- inventory/supply reservation and consumption;
- retention/audit implementation;
- logical/physical/API representation.

Reopen only if one of those areas proves that the accepted semantic distinction cannot be preserved.