<!-- LIFEOS-CANONICAL-CONTINUATION document="README.md" follows="README-part-5.md" -->
> **Canonical continuation of the logical Domain Atlas README.** Earlier Atlas decisions remain unchanged; this part records only Dependency v0 integration.

# 2026-08-15 — Dependency v0 Domain Atlas integration

## Accepted Relationships / Reasoning family

Dependency v0 is accepted as a canonical **specific contextual directional relation family/capability**.

Canonical definition:

> **A Dependency is the contextual directional relation through which a defined state, transition, progression or satisfiability condition of one bounded target is materially contingent on a specified state, result or condition of another bounded target within a defined purpose and context.**

Core topology:

```text
prerequisite target/material state
              ↓
          Dependency
              ↓
dependent target/state/transition
```

Endpoint concepts keep their own identity.

## Atlas invariants added

```text
Dependency != generic Relationship
Dependency != hierarchy / containment
Dependency != Temporal Constraint
Dependency != Schedule
Dependency != Trigger / Conditional Policy
Dependency != Criterion / Evaluation
Dependency != Resource Requirement / Allocation / Capacity Claim
Dependency != Responsibility / Participation
Dependency != Authority
Dependency != Decision
Dependency != Agreement / Consent / Acknowledgement
Dependency != causality
Dependency != Actual
```

Additional rules:

- `Prerequisite` is a semantic role, not a universal root;
- `blocked` / `dependency satisfied` are normally derived contextual projections;
- lead/lag/spacing stay in Time / Temporal Constraint;
- satisfaction does not execute or Schedule the dependent target;
- Actual may violate a planned Dependency and must remain truthful;
- material Dependency changes do not silently inherit prior satisfaction;
- correction does not destructively erase consequential prior history;
- no universal transitivity;
- no universal acyclic-DAG requirement;
- cycles/deadlocks remain representable for diagnosis;
- no WorkflowNode / WorkflowGraph / DependencyGraph kernel primitive;
- AI inference/proposal does not establish shared Dependency or Authority;
- a direct specific relation is enough when semantically complete; qualify the relation only when its own state/history/context is material.

## Cross-cluster integration

Dependency v0 closes prior structural pressure from Plan/Relationship reasoning while preserving:

```text
Intention / Plan identity
Time geometry and Schedule
Actual reality
Data / Subject native identities
Multi-Actor Authority / Visibility / Agreement boundaries
```

No accepted Cluster 1–4 primitive is reopened.

## Still separately owned

Dependency v0 does not resolve these future families/questions:

```text
Trigger / Conditional Policy
Contribution
Coordination Stewardship
Verification / comprehension
Collective / Group / quorum
Subject focus/context relations
all/any/alternative prerequisite composition
transitive-closure implementation
cycle/deadlock algorithms
logical/physical/API representation
```

These remain subject to fresh candidate scoring and their own Domain Validation Methodology v3 gates.

Normative references:

- `concepts/dependency.md`;
- `checkpoints/dependency-v0-validation.md`;
- `checkpoints/relationship-v0-validation-part-2.md`;
- `checkpoints/cross-cluster-validation-v4-part-3.md`.

Dependency's semantic verdict is **PASS WITH HARDENING** with `REOPEN 0` and `UNCLASSIFIED 0`. Final repository closure is recorded only after propagation QA.