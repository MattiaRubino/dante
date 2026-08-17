<!-- LIFEOS-CANONICAL-CONTINUATION document="actual-v0-validation.md" follows="actual-v0-validation.md" -->
> **Canonical continuation of `actual-v0-validation.md`.** The original validation remains preserved. This continuation closes the downstream Resource Allocation / Actual-use boundary.

# Actual v0 — downstream closure: Resource Requirement / Allocation

**Date:** 2026-08-15  
**Actual verdict:** unchanged — PASS WITH HARDENING  
**REOPEN:** 0

Resource Requirement / Allocation v0 confirms:

```text
planned Allocation != Actual resource use / consumption
```

The distinction survives chronology, substitution, partial use and correction:

- planned A18 / actually used Rental Z is valid;
- allocated 500 ml / consumed 430 ml is valid;
- Actual use may occur without prior Allocation;
- a later Actual must not rewrite the historical plan;
- a corrected Allocation assertion does not alter Actual merely because planning history changed;
- Requirement withdrawal does not erase realized use.

Where actual provider/use differs from planned Allocation, LifeOS may preserve both and derive the deviation. It must not invent a retrospective Allocation unless a real later planning designation occurred.

This closure strengthens the existing Actual rule that reality may exist independently from planning wrappers and that correction/history must remain attributable.

Inventory movement/consumption semantics remain independently SAFE DEFERRED where ordinary Actual semantics are insufficient for stock accounting. This does not justify a universal inventory or Resource-use primitive now.

No Actual invariant failed. **Actual v0 remains PASS WITH HARDENING; REOPEN = 0.**

Normative reference: `resource-requirement-allocation-v0-validation.md`.