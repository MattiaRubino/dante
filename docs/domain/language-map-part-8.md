<!-- LIFEOS-CANONICAL-CONTINUATION document="language-map.md" follows="language-map-part-7.md" -->
> **Canonical continuation of the logical Domain Language Map.** Earlier vocabulary decisions remain unchanged; this part records only Dependency v0 terminology and boundaries.

# 2026-08-15 — Dependency v0 language closure

## Canonical term: Dependency

**Domain meaning:**

> A specific contextual directional relation in which a materially relevant state, transition or condition of one bounded target is contingent on a specified state, result or condition of another bounded target.

Preferred canonical use:

```text
Dependency
```

Use when there is genuine prerequisite contingency, not merely association, ordering, hierarchy or correlation.

## Prerequisite

**Status:** accepted semantic role within Dependency; not an independent universal primitive/root.

Use for the endpoint/state/result whose satisfaction is required by the dependent facet under the relevant Dependency.

## Dependent

**Status:** orientation role within Dependency; not an independent root.

Use for the endpoint/state/transition whose admissibility/satisfaction is contingent on the prerequisite condition.

## Blocked / unblocked / dependency satisfied

**Status:** normally derived contextual projections, not foundational independent entities or universal stored truth.

Derived from:

```text
applicable Dependency
+ prerequisite material state/result
+ dependent facet/context
```

Unknown prerequisite state must not be translated automatically into `blocked because failed` or `satisfied`.

## Predecessor / Successor

**Status:** acceptable orientation/product vocabulary where useful; not independent kernel primitives.

Do not assume every predecessor/successor relation is a Dependency unless prerequisite contingency exists.

## Before / After

**Primary owner:** Time / Temporal Constraint when the meaning is temporal ordering.

```text
B happens after A
```

must not be normalized automatically to Dependency.

## Lead / Lag / Spacing

**Owner:** Time / Temporal Constraint.

Not canonical Dependency fields merely because external project-management systems pair them with task links.

## Trigger

**Status:** separate candidate/family.

```text
Dependency
= what a dependent state/transition is contingent on

Trigger / Conditional Policy
= what condition initiates/causes a downstream action or automation response
```

Do not use `Dependency` to mean `when X then automatically do Y`.

## Causality

Dependency must not be used as a synonym for causal explanation.

```text
required prerequisite
!= proven cause
```

## Relationship hierarchy

Canonical relationship discipline remains:

```text
specific truthful relation > generic related_to
```

Dependency does not introduce a universal Relationship/Edge/WorkflowNode vocabulary.

## Graph vocabulary

These are **not** accepted canonical kernel primitives by Dependency v0:

```text
DependencyGraph
WorkflowGraph
WorkflowNode
Blocker entity
Prerequisite entity
```

A graph can be a representation/query view without becoming domain ontology.

## Cycle / deadlock

A circular set of Dependencies may be described as a cycle/deadlock/infeasible planning state where appropriate. LifeOS does not normalize the domain into an acyclic graph merely for engine convenience.

## Transitive / indirect dependency

Do not automatically promote graph reachability into canonical direct Dependency.

```text
B depends on A
C depends on B
```

may support an indirect reasoning result, but does not universally create the stored semantic assertion:

```text
C depends directly on A
```

Normative references:

- `concepts/dependency.md`;
- `checkpoints/dependency-v0-validation.md`.
