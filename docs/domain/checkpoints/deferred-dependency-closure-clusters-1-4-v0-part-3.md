<!-- LIFEOS-CANONICAL-CONTINUATION document="deferred-dependency-closure-clusters-1-4-v0.md" follows="deferred-dependency-closure-clusters-1-4-v0-part-2.md" -->
> **Canonical continuation of the logical Deferred Dependency Closure — Clusters 1–4 checkpoint.** Earlier parts remain preserved. This continuation records downstream Resource Requirement / Allocation resolution only.

# 2026-08-15 — Resource Requirement / Allocation dependency closure

Resource v0 and Cluster-4 integration previously left Resource Requirement, candidate eligibility, Allocation, reservation/claim detail and actual-use boundaries as explicit SAFE DEFERRED dependencies.

Resource Requirement / Allocation v0 now resolves the reusable semantic boundaries:

```text
Resource Requirement                       RESOLVED
Requirement ↔ Resource                     RESOLVED
Requirement ↔ Request                      RESOLVED
Requirement ↔ Criterion / Quantity / Time  RESOLVED at semantic boundary
Candidate Set                              RESOLVED as DERIVED / CONTEXTUAL
Resource Allocation                        RESOLVED
Allocation ↔ Resource                      RESOLVED
Allocation ↔ schedulable Capacity Claim    RESOLVED
Allocation ↔ Schedule                      RESOLVED
Allocation ↔ Responsibility                RESOLVED
Allocation ↔ Participation                 RESOLVED
Allocation ↔ Authority / Visibility        RESOLVED
Allocation ↔ Decision                      RESOLVED
Allocation ↔ Proposal / Request            RESOLVED
Allocation ↔ Version                       RESOLVED
Allocation ↔ Provenance / Reconciliation   RESOLVED
Allocation ↔ Actual use                    RESOLVED
```

Accepted distinction:

```text
Requirement
→ Candidate
→ Allocation
→ Capacity Claim
→ Actual
```

is a possible composition, not a required workflow/state machine.

## Capacity Reservation / Claim closure

The Time cluster's existing Capacity Reservation / Claim semantics remain the owner for **schedulable capacity held/protected**.

```text
schedulable Capacity Claim                 RESOLVED
universal Reservation primitive            REJECTED
non-temporal inventory/stock reservation   SAFE DEFERRED
```

## Remaining SAFE DEFERRED owners

| Dependency | Owner | Reopening trigger |
|---|---|---|
| Requirement `all/any/alternatives` composition | planning/logical model | ordinary flows cannot express alternatives/cumulative satisfaction |
| candidate matching/ranking expression | planning + Criterion/Evaluation | eligibility computation requires changing Requirement semantics |
| pool/late-binding mechanics | logical Resource model | pool allocation needs independent semantics outside accepted boundary |
| non-temporal inventory reservation | inventory/supply | stock/consumable holds cannot compose without universalizing Capacity Claim |
| actual inventory movement/consumption | inventory + Actual | consumption history cannot be reconstructed |
| Place/Service/Skill native semantics | future domain reviews | repeated workflows require stronger native identities/concepts |
| exact Allocation lifecycle/cardinality | logical model | direct and rich/history cases cannot coexist coherently |
| automatic fallback/reallocation | Trigger/policy | conditional automation must be embedded in Allocation to work |
| collective/group allocation | collective/group review | ordinary workflows require Group/quorum semantics |
| specialist booking/source-of-record behavior | integration/specialist adapters | authoritative external state cannot reconcile safely |
| retention/audit | privacy/retention | required history conflicts with minimization/deletion |
| SQL/API representation | logical/physical/API stage | implementation pressure exposes semantic contradiction |

No material dependency remains unclassified.

```text
REOPEN       0
UNCLASSIFIED 0
```

Normative reference: `resource-requirement-allocation-v0-validation.md`.