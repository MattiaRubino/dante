<!-- LIFEOS-CANONICAL-CONTINUATION document="version.md" follows="version.md" -->
> **Canonical continuation of `version.md`.** The accepted Version / Material-State v0 specification remains preserved. This amendment records Resource Requirement / Allocation integration only.

# 2026-08-15 — Requirement / Allocation material-state boundary

Resource Requirement / Allocation v0 applies the existing Version discipline directly to resource planning.

Canonical rules:

```text
Requirement identity
!= materially relevant Requirement state

Allocation applicability
= bound to materially relevant Requirement state where consequence requires it
```

Therefore:

```text
material Requirement change
!= automatic carry-forward of prior Allocation
```

Example:

```text
Requirement S1: camera >= X
Allocation A1: A17

Requirement S2: camera >= X + underwater capability
```

A1 remains historical truth about S1. It is not silently applicable to S2.

Version does not decide whether S2 is a materially revised state of the same Requirement or a new Requirement identity. That identity decision belongs to the owning context; Version must not hide semantic replacement.

Candidate-set changes alone do not constitute Requirement material revision automatically.

Where Allocation itself changes materially, earlier Allocation states remain reconstructible when consequence/history warrants it. Technical/provider revisions, ETags or storage row versions do not determine semantic materiality.

Version v0 remains **PASS WITH HARDENING, REOPEN = 0**.

Normative downstream reference: `../checkpoints/resource-requirement-allocation-v0-validation.md`.