# LifeOS Domain Atlas

**Status:** In progress  
**Started:** 2026-08-10  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

The Domain Atlas is the working source for re-evaluating and defining LifeOS domain concepts before broad persistence or backend implementation.

Its job is not to preserve earlier terminology by inertia. Its job is to produce the strongest current domain model we can justify from product intent, real-world scenarios, external patterns, implementation constraints, and explicit reasoning.

## Decision rule

In this workstream, **accepted means current best decision, not immutable decision**.

A concept may be reopened when new scenarios, evidence, implementation constraints, contradictions, or better abstractions emerge. Changes must be deliberate and documented; prior reasoning must not be silently overwritten.

Earlier product documents, simulations, glossaries, ADRs, prototypes, and conversation history are inputs to re-evaluate. They are not automatically treated as correct merely because they were written earlier.

Where an accepted ADR defines a broader architectural constraint, this workstream should respect it unless new evidence is strong enough to justify an explicit ADR change.

## Working method

Concepts are reviewed one at a time.

For each concept we aim to establish:

1. canonical definition;
2. what the concept is and is not;
3. identity and ownership;
4. lifecycle and temporal semantics;
5. invariants;
6. relationships to other concepts;
7. evidence, provenance, and derived state where relevant;
8. real-world and edge-case coverage;
9. alternatives considered and why they are not preferred;
10. open questions intentionally deferred;
11. implications for future persistence and APIs without prematurely designing tables.

A concept is saved when it is coherent enough to be the current baseline. Saving it does not make it permanently closed.

## Validation approach

Definitions should be stress-tested against multiple classes of use rather than one productivity workflow. Relevant evidence includes:

- existing LifeOS product simulations and requirements;
- everyday personal planning;
- study and learning;
- work and professional deadlines;
- health and fitness;
- finance and resource tracking;
- home, travel, assets, and maintenance;
- creative work;
- caregiving and subject-based tracking;
- temporary disruptions and unusual schedules;
- patterns from mature external systems where they solve a comparable problem.

We should prefer a small set of strong primitives over many overlapping nouns. A new domain entity should exist because it has materially different identity, lifecycle, invariants, or behavior—not merely because another productivity product uses that label.

## Relationship to existing documentation

Existing product documents remain preserved as historical and product-definition inputs while this pass is underway.

When a Domain Atlas concept conflicts with an older definition, the conflict must be made explicit. The older document should not be silently rewritten until the impact is understood and the newer domain decision is ready to propagate.

Current known example:

- existing documentation treats `Goal`, `Program`, and `Project` as distinct canonical concepts;
- the Goal review has shown that `Project` as an independent domain primitive requires revalidation rather than automatic inheritance.

## Current concepts

- [`Goal v0`](concepts/goal.md) — current baseline accepted on 2026-08-10.

## Open modeling sequence

The next concept is intentionally not fixed here until the current concept is reviewed and accepted. The workstream proceeds one concept at a time so later concepts can be shaped by already-established invariants instead of producing a large speculative taxonomy.
