<!-- LIFEOS-CANONICAL-CONTINUATION document="responsibility.md" follows="responsibility-part-3.md" -->
> **Canonical continuation of the logical Responsibility v0 document.** Earlier parts remain preserved. This continuation records Resource Requirement / Allocation integration only.

# 2026-08-15 — Resource Allocation boundary

Resource Requirement / Allocation v0 confirms that selecting a provider does not establish Responsibility.

```text
Resource Allocation
= which provider/supply/capacity source is designated in the plan

Responsibility
= who is accountable for ensuring the bounded commitment is appropriately handled
```

Therefore:

```text
Allocation != Responsibility
allocated provider != responsible Actor automatically
```

Example:

```text
Requirement: qualified interpreter
Allocation: Anna
Responsibility: Luca
```

is valid when Luca remains accountable for ensuring the commitment is handled while Anna is the selected provider.

Likewise:

```text
Allocation: Anna
```

does not imply that Anna accepted a Responsibility hand-off, claimed accountability, acknowledged the plan, consented, or actually performed the work.

A Decision/Authority/policy may establish both an Allocation and a Responsibility transition in the same workflow, but they remain separate effects owned by their respective semantic families.

Reallocation does not automatically transfer Responsibility, and Responsibility transfer does not automatically reallocate a Resource.

The existing `Assignment`, `Claim` and `Hand-off` discipline remains unchanged: role-specific operations must name the role they affect. `ResourceAssignment` is not accepted as a universal kernel primitive.

Responsibility v0 remains **PASS WITH HARDENING, REOPEN = 0**.

Normative downstream reference: `../checkpoints/resource-requirement-allocation-v0-validation.md`.