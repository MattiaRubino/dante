<!-- LIFEOS-CANONICAL-CONTINUATION document="actual.md" follows="actual.md" -->
> **Canonical continuation of `actual.md`.** The accepted Actual v0 specification remains preserved. This amendment records Resource Requirement / Allocation integration only.

# 2026-08-15 — Resource Allocation vs Actual use

Resource Requirement / Allocation v0 closes a previously deferred planning/reality boundary without reopening Actual.

Canonical rule:

```text
Resource Allocation
= planned provider/supply/capacity designation

Actual resource use / consumption
= what was really used/consumed
```

Therefore:

```text
Allocation != Actual use
```

Examples:

```text
planned Allocation: A18
Actual provider: Rental Z
```

and:

```text
allocated quantity: 500 ml
actual consumed:    430 ml
```

must not be normalized into one fact merely because later reality is known.

Actual use may legitimately occur without a prior effective Allocation. LifeOS must not fabricate a retrospective Allocation in order to make the history look orderly.

Where a later substitution truly created a new planned designation, a later Allocation may be represented. Where no such planning act occurred, Actual use alone remains truthful.

Correction also remains distinct:

```text
wrong recorded Allocation
!= Actual use
!= corrected current understanding of the Allocation
```

Provenance/Reconciliation may correct planning history while Actual preserves realized reality according to its own semantics.

Requirement withdrawal or reallocation never erases truthful Actual history.

Actual v0 remains **PASS WITH HARDENING, REOPEN = 0**.

Normative downstream references:

- `resource-requirement.md`;
- `resource-allocation.md`;
- `../checkpoints/resource-requirement-allocation-v0-validation.md`.