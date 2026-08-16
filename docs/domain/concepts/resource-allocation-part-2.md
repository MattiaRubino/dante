<!-- LIFEOS-CANONICAL-CONTINUATION document="resource-allocation.md" follows="resource-allocation.md" -->
> **Canonical continuation of the single logical Resource Allocation document.** Earlier Allocation semantics remain preserved; this physical continuation records Possession integration only.

# 2026-08-16 — Possession versus Allocation

Resource Allocation is planned designation/selection. Possession is actual physical holding/control.

```text
Resource Allocation != Possession
```

Examples:

```text
camera allocated to Sara for tomorrow
camera currently held by Luca
→ Allocation: Sara
→ Possession: Luca

camera returned to owner without changing tomorrow's Allocation
→ Possession changes
→ Allocation need not
```

Allocation also remains distinct from Ownership, Custody and Actual use. Neither Allocation nor Capacity Claim transfers Ownership or establishes current Possession by itself.

Material change/correction of Possession does not silently rewrite a truthful Allocation record, and reallocation does not silently rewrite possession history.

Resource Allocation v0 remains **PASS WITH HARDENING, REOPEN = 0**.

Normative reference: `../checkpoints/ownership-possession-custody-v0-validation.md`.
