<!-- LIFEOS-CANONICAL-CONTINUATION document="plan.md" follows="plan.md" -->
> **Canonical continuation of `plan.md`.** This file is Part 2 of the same logical Plan document. The historical payload in `plan.md` remains authoritative for its earlier decisions; this continuation records only the downstream Dependency v0 integration. Physical split != additional logical document.

# 2026-08-15 — Dependency v0 downstream closure

Plan v0 already identified `dependencies` as one possible structural capability of a Plan while deferring their exact semantic boundary. Dependency v0 now closes that boundary without changing Plan identity.

Canonical separation:

```text
Plan
= persistent revisable execution strategy / coordination structure

Dependency
= specific directional contingency between bounded target states/results/transitions

Temporal Constraint
= temporal admissibility / spacing / relative temporal geometry

Schedule
= current accepted temporal assignment
```

Consequences for Plan:

- a Plan may coordinate zero or more Dependencies;
- Plan identity is not defined by the presence, count or topology of Dependencies;
- adding/removing one Dependency does not automatically create a new Plan identity;
- a materially different dependency structure may contribute to a material Plan revision or replacement decision, but no universal threshold is introduced;
- Activity, Event, Milestone, Routine, Resource Requirement, Allocation or other targets retain native identity when they play prerequisite/dependent roles;
- Dependency does not create parent-child containment or ownership;
- Plan containment/decomposition does not itself prove Dependency;
- pure sequence or spacing remains Time/Temporal Constraint unless a true prerequisite contingency exists;
- satisfying a Dependency does not automatically Schedule or execute the dependent target;
- a Dependency violation in reality does not rewrite Plan history or Actual;
- `blocked` / `dependency satisfied` are normally derived from applicable Dependency plus relevant states rather than stored as independent Plan truth;
- no universal DAG requirement is imposed on Plan; circular dependency states may need to be represented and diagnosed;
- no universal WorkflowNode/WorkflowGraph abstraction is introduced.

Material-state discipline remains unchanged:

```text
ordinary dependency edit
!= automatic Plan replacement

materially different execution strategy
may justify Plan replacement

technical storage revision
!= semantic material change
```

The exact logical/physical representation of Dependencies inside or alongside Plan remains deferred to later logical-model work.

Normative downstream references:

- `dependency.md`;
- `../checkpoints/dependency-v0-validation.md`.

Plan remains a **Current accepted baseline**; Dependency v0 closes one previously deferred structural capability without reopening Plan's core identity.