<!-- LIFEOS-CANONICAL-CONTINUATION document="multi-actor-readiness-v1.md" follows="multi-actor-readiness-v1-part-3.md" -->
> **Canonical continuation of the logical Multi-Actor Readiness v1 document.** Earlier parts remain preserved. This continuation records Resource Requirement / Allocation integration only.

# 2026-08-15 — Resource Requirement / Allocation multi-actor amendment

Resource Requirement / Allocation v0 completed all MA-01..20 tests with **PASS WITH HARDENING** and no REOPEN.

The accepted multi-actor decomposition is:

```text
shared Resource Requirement
!= one identical candidate view for every Actor

Candidate Set / ranking
= contextual/derived and may depend on actor-private information

Resource Allocation
= planned provider/supply/capacity designation

Allocation
!= Responsibility
!= Participation
!= Agreement
!= Consent
!= Authority
!= Actual use
```

A Person selected as Resource provider remains a Person with independent Participation, Responsibility, Agreement/Consent, Acknowledgement and Actual performer semantics.

One shared Requirement or Allocation may coexist with actor-scoped:

- candidate visibility;
- private constraints/qualifications;
- preferences/rankings;
- proposal/request/acknowledgement state;
- Responsibility;
- Participation;
- Consent/Agreement;
- Authority;
- visibility into rationale/history.

External/accountless Persons and providers remain representable without synthetic Accounts.

Selective-disclosure rule:

```text
authorized Allocation result
may be visible
while private matching basis remains hidden
```

AI may reason over authorized private context but cannot disclose that basis, manufacture Authority, or turn recommendation/proposal into human Allocation/Agreement/Consent/Responsibility/Participation.

Capacity Claim remains schedulable-capacity semantics. Non-temporal inventory holds remain independently deferred and do not become a multi-actor universal Reservation primitive.

The personal-first multi-actor architecture remains intact. **REOPEN = 0.**

Normative reference: `checkpoints/resource-requirement-allocation-v0-validation.md`.