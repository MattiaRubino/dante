<!-- LIFEOS-CANONICAL-CONTINUATION document="temporal-constraint.md" follows="temporal-constraint.md" -->
> **Canonical continuation of `temporal-constraint.md`.** This file is Part 2 of the same logical Temporal Constraint document. It records only the downstream Dependency v0 boundary; the historical base remains unchanged.

# 2026-08-15 — Dependency v0 downstream amendment

Dependency v0 closes a neighboring relation family that Temporal Constraint must remain distinct from.

Canonical separation:

```text
Dependency
= a dependent state/transition/condition is materially contingent on a specified prerequisite state/result/condition

Temporal Constraint
= a rule restricting or preferring temporal placement, duration or temporal relationship
```

Therefore:

```text
B must occur after A
```

may be a Temporal Constraint even when no Dependency exists.

By contrast:

```text
B may proceed only if A has reached state S
```

is Dependency semantics even when no exact times are known.

The two concepts may compose:

```text
Dependency
B requires A.approved

Temporal Constraint
B.start >= A.approved_at + 24h
```

but they do not merge.

Consequences:

- lead, lag, spacing, minimum/maximum separation and before/after temporal geometry remain Time / Temporal Constraint semantics;
- Dependency does not own a generic `lag` or `offset` merely because some project-management systems combine them;
- satisfying a Dependency does not create a Schedule;
- violating a Temporal Constraint does not automatically mean the underlying prerequisite condition failed;
- violating a Dependency does not imply one specific temporal violation unless a separate temporal rule exists;
- pure sequencing is insufficient evidence for Dependency;
- a causal relationship is not inferred from either temporal order or Dependency alone;
- no provider task-link enum is adopted as canonical ontology.

The accepted Temporal Constraint invariant remains:

```text
Temporal Constraint != Schedule != Actual
```

and now gains the explicit neighboring invariant:

```text
Temporal Constraint != Dependency
```

Normative downstream references:

- `dependency.md`;
- `../checkpoints/dependency-v0-validation.md`.

Temporal Constraint remains a **Current accepted baseline** with no structural reopen.