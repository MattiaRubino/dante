<!-- LIFEOS-CANONICAL-CONTINUATION document="logical-model.md" follows="logical-model-part-5.md" -->
> **Canonical continuation of the Logical Model workstream record.** Earlier history remains preserved. This continuation records Slice E local acceptance and its activation gate.

# 2026-08-17 — Slice E: Resources / Values / Capacity

## Current branch at pre-scope

```text
branch
feature/logical-model

pre-scope
3a4f59f2716588584081f9a7cb2b98bb8a80c2fa
```

## Entry condition

Integrated A+B+C+D was already remote-QA closed before Slice E began.

Slice E was developed read-only first under the hardened Logical Validation Methodology.

## Slice E scope

Reviewed:

```text
Asset / Resource role
Resource Requirement
Candidate Set
Resource Allocation
Availability
Capacity
Capacity Reservation / Claim
Quantity
MonetaryAmount
Ownership / Possession pressure
fungible supply / pools
inventory specialist boundary
solver / optimization pressure
```

## Preferred architecture

```text
Layered Typed Resource Feasibility & Allocation Model
```

Core result:

```text
native provider identity
-> contextual Resource role
-> Requirement
-> derived candidates
-> planned Allocation
-> optional Capacity Claim
-> Actual use
```

with Availability/Capacity/compatibility/policy feeding feasibility and derived effective-capacity views.

The sequence is not a mandatory state machine.

## Accepted logical dispositions

```text
Asset
-> LR-01 / NativeRef

Resource
-> contextual role; no ResourceRef

Resource Requirement
-> LR-05
-> LR-02 + ScopedRecordRef when material

Candidate Set
-> LR-08

Resource Allocation
-> LR-03
-> LR-02 + ScopedRecordRef when material

Availability rule
-> LR-05

Availability override/material fact
-> LR-02 where required

Effective Availability
-> LR-08

Capacity
-> contextual capability/state
-> LR-04 dimensions + LR-05 policy + bounded LR-02 where material

Effective Free Capacity
-> LR-08

Capacity Claim
-> LR-03
-> LR-02 + ScopedRecordRef when material

Quantity
-> LR-04

MonetaryAmount
-> separate LR-04 family
```

## Key hardening

```text
Resource role != identity
Candidate Set derived by default
Allocation != Capacity Claim
Allocation != Actual use
Schedule != Capacity Claim
Capacity not universally binary/scalar
free-slot grid != canonical Availability source
stock reservation != Capacity Claim automatically
fungible supply != per-unit Asset identity
Quantity != MonetaryAmount
FX != ordinary unit conversion
solver output != canonical Allocation
private feasibility input != disclosure permission
```

## Candidate architectures reviewed

```text
Universal Resource entity                  REJECTED
Fully owner-specific logical resource model REJECTED as baseline; physical ingredient retained
Universal Capacity/Claim Ledger            REJECTED as complete kernel; bounded mechanism retained
Solver-first canonical model               REJECTED
ERP/Inventory kernel                        REJECTED as general kernel; LR-13 retained
Layered Typed model                         PREFERRED
```

## Validation result

```text
E0 canonical reconstruction                       DONE
E1 high-value query corpus                         DONE
E2 candidate architectures                         DONE
E3 identity / role / fungibility                   DONE
E4 Quantity / MonetaryAmount                       DONE
E5 Requirement / Candidate / Allocation            DONE
E6 Availability / Capacity / Claim                 DONE
E7 inventory / pool / specialist pressure          DONE
E8 external benchmark / scale / evolution          DONE
E9 mutation / counterfactual / history             DONE
E10 A+B+C+D regression + technology reconsideration DONE READ-ONLY
```

Local verdict:

```text
PASS WITH HARDENING
DOMAIN REOPEN REQUIRED      0
NEW DOMAIN OWNER REQUIRED   0
A+B+C+D REGRESSION FAILURE  0
LOGICAL STRUCTURAL BLOCKER  0
```

## Exact Stage E write scope

```text
CREATE 8
UPDATE 0
DELETE 0
```

Created paths are the Slice E specification, validation checkpoint, benchmark, framework continuation, corpus continuation, traceability continuation, decision/assumption continuation and this workstream continuation.

No Domain, SQL, migration, API/backend, auth, frontend or main-branch change is authorized by Slice E.

## Activation rule

Slice E must not be called ACTIVE/CLOSED until:

1. the branch still equals the exact PRE-SCOPE immediately before ref movement;
2. one atomic commit contains exactly the eight approved CREATE paths;
3. compare reports `8 added / 0 modified / 0 deleted / 0 unexpected`;
4. all eight remote payloads read back with matching blob SHA;
5. `main` remains unchanged;
6. a separately gated remote-QA closure record is created and verified.

## Next required checkpoint

After Slice E remote activation:

```text
Integrated A+B+C+D+E
```

must run before Slice F.

It must replay touched permanent invariants, Slice E tests, history/material-state behavior, multi-actor/privacy pressure and technology/mechanism reconsideration.

Slice F — Relationships / Multi-Actor / Governance — must not become active before that cumulative checkpoint closes.