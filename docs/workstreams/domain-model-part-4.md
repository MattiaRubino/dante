<!-- LIFEOS-CANONICAL-CONTINUATION document="domain-model.md" follows="domain-model-part-3.md" -->
> **Canonical continuation of the Core Domain Model workstream handoff.** Earlier parts remain preserved. This continuation records Resource Requirement / Allocation v0 propagation state and the exact next semantic action.

# Core Domain Model v0 — Resource Requirement / Allocation milestone

**Date:** 2026-08-15  
**Branch:** `feature/domain-model`  
**Approved pre-scope:** `c6c324ff5a5806f9c99c793d7db587f9ce0e4822`

## Accepted semantic milestone

```text
RESOURCE REQUIREMENT / ALLOCATION v0
+ SCHEDULABLE CAPACITY CLAIM INTEGRATION

PASS WITH HARDENING

CORE PASS WITH HARDENING
MA PASS WITH HARDENING
XCON PASS WITH HARDENING
ADS COMPLETE
REOPEN       0
UNCLASSIFIED 0
```

Accepted minimum:

```text
Resource Requirement
= contextual need of bounded planning/execution context

Candidate Set
= contextual/derived eligibility projection

Resource Allocation
= planned provider/supply/capacity designation

Capacity Reservation / Claim
= existing Time/Availability & Capacity semantics for schedulable capacity held/protected

Actual resource use / consumption
= realized reality, not Allocation
```

Rejected universalizations:

```text
universal Requirement root/table
universal Allocation root/table
universal Reservation primitive
CandidateSet entity/root
ResourcePlan mega-root
Booking mega-root
ResourceAssignment mega-root
mandatory Requirement→Candidate→Allocation→Reservation→Actual state machine
```

Critical current barriers:

```text
Requirement != Resource / Request / Criterion / Allocation
Candidate Set != primitive
Allocation != Capacity Claim
Allocation != Responsibility / Participation / Agreement / Consent
Allocation != Authority / Decision / Schedule
Allocation != Actual use
material Requirement change != automatic Allocation carry-forward
```

Person-as-Resource, private matching, AI authority, history/correction and Reconciliation hardenings are mandatory.

## Remaining independently SAFE DEFERRED areas

- Requirement composition all/any/alternatives;
- candidate matching/ranking expression;
- pool/late-binding mechanics;
- non-temporal stock/inventory reservation;
- inventory movement/consumption;
- Place/Service/Skill native semantics;
- exact Allocation lifecycle/cardinality;
- Trigger/policy fallback/reallocation;
- Collective/Group/quorum;
- specialist booking/source-of-record behavior;
- retention/audit;
- logical/physical/API representation.

No item above authorizes implementation work.

## Explicitly out of scope for this milestone

```text
main synchronization
SQL / migrations
physical PostgreSQL
API contracts
backend implementation
auth / Principal implementation
prototype / frontend
Trigger / conditional policy
inventory / stock implementation
Group / quorum
Verification / comprehension
docs/domain/concepts/relationship.md
```

## Current workstream position

After final remote post-write QA of this approved 33-path propagation scope:

```text
1. Resource Requirement / Allocation v0 milestone → CLOSED only if QA PASS
2. fresh re-score remaining Relationships / Reasoning candidate space
3. select exactly ONE candidate/family
4. execute full Methodology v3 read-only
5. continue until Relationships / Reasoning candidate space is complete
6. then Cluster-5 integration / multi-actor stress / deferred-dependency closure
7. only later whole-domain validation and logical model
```

No next candidate is preselected by this milestone.

## Git discipline

This continuation does not declare closure on its own. Closure requires remote evidence that:

- branch is `feature/domain-model`;
- compare against approved pre-scope shows exactly the approved 33 CREATE paths;
- UPDATE = 0;
- DELETE = 0;
- unexpected paths = 0;
- continuation/history preservation is intact;
- REOPEN = 0;
- UNCLASSIFIED = 0;
- no main/backend/API/auth/frontend scope was touched.

Only after that evidence may Resource Requirement / Allocation v0 be called **POST-WRITE QA PASS / CLOSED**.