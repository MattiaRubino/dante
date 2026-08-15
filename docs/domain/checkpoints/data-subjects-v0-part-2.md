<!-- LIFEOS-CANONICAL-CONTINUATION document="data-subjects-v0.md" follows="data-subjects-v0.md" -->
> **Canonical continuation of `data-subjects-v0.md`.** The accepted Cluster-4 integration remains preserved. This continuation records downstream closure of its Resource Requirement / Allocation dependency.

# Data / Subjects v0 — Resource Requirement / Allocation amendment

**Date:** 2026-08-15  
**Cluster verdict:** unchanged — PASS WITH HARDENING  
**REOPEN:** 0

Cluster 4 previously hardened the sequence:

```text
Requirement
→ candidate(s)
→ allocation
→ reservation / claim
→ actual use / consumption
```

while deferring the exact reusable Requirement/Allocation semantics.

Resource Requirement / Allocation v0 now resolves that boundary as:

```text
Resource Requirement
= contextual need specification

Candidate Set
= derived/contextual eligibility projection

Resource Allocation
= contextual planned provider/supply/capacity designation

Capacity Reservation / Claim
= existing schedulable-capacity commitment semantics

Actual use / consumption
= realized reality
```

This downstream closure preserves all Cluster-4 identity rules:

- Resource remains a contextual role/capability, not entity/root;
- Person and Asset keep native identity while playing Resource role;
- supplies/pools need no synthetic Resource identity;
- Quantity may describe need/capacity without becoming Requirement;
- Subject/Actor/Account remain independent;
- Register/Tracker remains projection/product capability;
- no universal ManagedObject/Resource/Requirement/Allocation root is introduced.

Additional hardening:

```text
candidate-set change != Requirement revision automatically
material Requirement change != automatic Allocation carry-forward
Allocation != Capacity Claim
Allocation != Actual use
non-temporal inventory reservation != Capacity Claim automatically
```

Inventory/supply reservation and consumption remain independently SAFE DEFERRED. No Cluster-4 concept is reopened.

Normative downstream reference: `resource-requirement-allocation-v0-validation.md`.