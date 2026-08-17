<!-- LIFEOS-CANONICAL-CONTINUATION document="criterion-evaluation.md" follows="criterion-evaluation.md" -->
> **Canonical continuation of `criterion-evaluation.md`.** The accepted Criterion / Evaluation v0 specification remains preserved. This amendment records Resource Requirement / Allocation integration only.

# 2026-08-15 — Requirement matching boundary

Resource Requirement / Allocation v0 confirms that Criterion/Evaluation may participate in eligibility and matching without becoming the Requirement or Allocation.

```text
Resource Requirement
= what the bounded planning/execution context needs

Criterion
= evaluative specification used to assess suitability/conditions

Evaluation
= application of Criterion to relevant Evidence/context

Candidate Set
= contextual/derived eligibility projection

Resource Allocation
= planned designation/selection
```

Therefore:

```text
Requirement != Criterion
candidate matching != Allocation
Evaluation result != Allocation
```

A Requirement may contain or reference capability, qualification, Quantity, temporal/capacity or other conditions, but the reusable Criterion family remains distinct whenever evaluative rule identity/state/history matters.

Candidate Set and ranking are derived/contextual by default. Their exact expression remains SAFE DEFERRED to planning + Criterion/Evaluation logical design. Reopen only if eligibility cannot be computed without changing accepted Requirement semantics.

Private Evidence/criteria may influence an authorized candidate/ranking result without granting visibility to the underlying private basis.

AI may evaluate/rank candidates, but:

```text
AI Evaluation / ranking != Resource Allocation
```

Criterion / Evaluation v0 remains **PASS WITH HARDENING, REOPEN = 0**.

Normative downstream reference: `../checkpoints/resource-requirement-allocation-v0-validation.md`.