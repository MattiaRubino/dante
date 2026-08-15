# Dependency v0

**Status:** Current accepted semantic baseline — propagation pending  
**Accepted:** 2026-08-15  
**Meaning of accepted:** best current semantic decision; reopenable with stronger evidence  
**Workstream:** Core Domain Model v0 — Relationships / Reasoning

## Canonical definition

> **A Dependency is a contextual directional relation through which a defined state, transition, progression or satisfiability condition of one bounded target is materially contingent on a specified state, result or condition of another bounded target within a defined purpose and context.**

Dependency answers the question:

> **Which prerequisite state, result or condition must hold for this specific dependent state, transition or condition to be admissible or satisfied in this context?**

The canonical shape is:

```text
prerequisite target + materially relevant state/result/condition
                         ↓
                    Dependency
                         ↓
dependent target + materially relevant state/transition/condition
```

The endpoints retain their own native identity. Playing prerequisite or dependent roles does not transform an Activity, Event, Milestone, Plan, Resource, Requirement, Allocation, Person, Asset or other accepted concept into a generic workflow node.

---

## Why this concept exists

LifeOS must coordinate situations where one planned step or state genuinely depends on another without collapsing that semantics into temporal order, hierarchy, evaluation, automation or resource planning.

Representative cases include:

- release submission depends on an approved master;
- deployment depends on a required test result;
- a visa application depends on a valid passport state;
- final assembly depends on a required component/result being available;
- a Plan transition may depend on a Milestone or other bounded prerequisite state;
- a downstream Activity may be inadmissible under the current Plan while its prerequisite state is not satisfied.

The relationship is meaningful even when no Schedule exists and even when the dependent target never executes.

A generic `related_to` edge is too weak because it does not preserve which side is prerequisite, which dependent facet is affected, or what prerequisite condition matters.

---

# Core semantic boundaries

## Dependency != generic Relationship

A generic association says that two targets are connected.

Dependency carries specific directional contingency semantics.

```text
A related to B
```

is insufficient to mean:

```text
B.transition X depends on A.state S
```

Therefore:

> **Dependency is a specific relation family, not a universal Relationship root.**

The accepted relationship-model rule remains: use the most specific truthful relation, and qualify that relation only when its own context/state/history is materially consequential.

---

## Dependency != hierarchy / containment

Containment, composition or broader/narrower structure does not establish prerequisite semantics.

```text
Plan contains Activity B
```

is not equivalent to:

```text
Activity B depends on Activity A reaching state S
```

Likewise parent/child, phase membership and grouping must not be used as dependency shortcuts.

---

## Dependency != Temporal Constraint

Temporal Constraint owns temporal admissibility, boundaries, spacing and relative temporal geometry.

Dependency owns contingency on a materially relevant prerequisite state/result/condition.

These statements are different:

```text
B must happen after A
```

```text
B may proceed only if A has produced result R
```

The first may be purely temporal. The second is Dependency.

A true Dependency may imply temporal consequences, but those consequences do not move lead/lag/spacing semantics into Dependency.

Therefore:

```text
Dependency != before/after ordering
Dependency != lag/lead
Dependency != spacing
```

Those remain Time / Temporal Constraint semantics where applicable.

---

## Dependency != Schedule

Dependency satisfaction does not create an accepted temporal assignment.

A target can be dependency-satisfied and unscheduled.

A target can also retain a historical/current Schedule even when a newly discovered or corrected Dependency makes that planned placement infeasible or inconsistent.

The system may diagnose and replan, but must not silently erase or rewrite Schedule history.

---

## Dependency != Trigger / Conditional Policy

Dependency constrains admissibility/satisfaction/progression.

Trigger or conditional-policy semantics determine whether a condition causes or initiates an action, generation, notification, transition or automation.

Example:

```text
Dependency
Deployment may proceed only after required tests pass.
```

is not equivalent to:

```text
Trigger
When required tests pass, automatically deploy.
```

Prerequisite satisfaction therefore never implies automatic execution.

Trigger / Conditional Policy remains a separately owned candidate.

---

## Dependency != Criterion / Evaluation

Criterion defines an evaluative specification. Evaluation applies it to relevant Evidence under context.

Dependency defines a prerequisite contingency between bounded targets/states.

A test result may be evaluated by a Criterion and that evaluated state may be the prerequisite condition for a Dependency, but the Evaluation rule and Dependency relation remain distinct.

---

## Dependency != Resource Requirement / Allocation / Capacity Claim

A Resource Requirement states what a bounded context needs from eligible providers/supply.

A Resource Allocation designates a provider/supply/capacity source in the plan.

A Capacity Claim protects schedulable capacity.

None of these is Dependency merely because a plan cannot proceed without the relevant resource state.

Where a real prerequisite exists, LifeOS may relate a dependent transition to the appropriate requirement/allocation/claim state without collapsing those concepts.

---

## Dependency != Responsibility / Participation / Authority

Dependency establishes no accountability, involvement or governance power.

```text
B depends on A
```

never means:

```text
actor X is responsible for B
actor X participates in B
actor X may govern B
```

Those meanings remain owned by Responsibility, Participation and Authority.

---

## Dependency != Proposal / Request / Decision / Agreement / Consent

A Dependency may be proposed, requested, decided, agreed to or changed under applicable governance, but those acts are not the Dependency itself.

Likewise, one Actor seeing or accepting a dependency-related proposal does not manufacture shared Agreement or Consent.

---

## Dependency != causality

Prerequisite relation does not prove causal explanation.

```text
Payment authorization must exist before fulfillment may proceed
```

expresses an operational dependency.

It does not establish that authorization caused the fulfillment outcome in a scientific or explanatory sense.

LifeOS must not infer causality from Dependency alone.

---

# Prerequisite and dependent roles

`Prerequisite` is accepted as a semantic role inside Dependency, not as a standalone universal root.

`Dependent`, `predecessor` and `successor` may be useful orientation vocabulary, but they do not introduce independent kernel identities.

The relation must preserve direction explicitly enough that reversing the endpoints does not silently preserve the same meaning.

No universal inverse rule is assumed beyond the explicit orientation of the same Dependency assertion.

---

# Material facet / state binding

A bare endpoint pair may be insufficient when materially different prerequisite or dependent facets exist.

Example:

```text
Prerequisite target
Design review

Relevant prerequisite state
approved

Dependent target
Production order

Relevant dependent transition
release to production
```

The Dependency is not necessarily a claim that every state of the Production order depends on every state of the Design review.

Where consequence requires precision, the relation must bind to the materially relevant prerequisite state/result/condition and dependent state/transition/condition.

Where one obvious bounded relation is semantically complete, a simpler direct representation remains valid.

This is a semantic requirement, not a prescribed database shape.

---

# Current satisfaction and blocking are derived

Dependency itself is the relation/rule assertion.

Current labels such as:

```text
blocked
unblocked
prerequisite satisfied
dependency satisfied
```

should normally be derived from:

- the applicable Dependency state;
- the materially relevant prerequisite state/result;
- the dependent facet being evaluated;
- context/time/version where relevant.

They are not universal independent entities or immutable truth fields.

Unknown prerequisite state must remain distinguishable from known-unsatisfied state.

> **No data != prerequisite failed.**

---

# Chronology and history

Dependency must preserve planned/current/actual/history separation.

Representative chronology:

```text
T0
A and B exist independently.

T1
D1: B.transition X depends on A.state S.

T2
A has not reached S.
B may be derived as blocked for X.
B identity is unchanged.

T3
A reaches S.
D1 is currently satisfied.
B does not automatically execute and no Schedule is manufactured.

T4
B receives or changes Schedule.
Dependency remains distinct from Schedule.

T5
A.state is corrected or reconciled.
Dependency satisfaction is reevaluated under the applicable material states.
Historical assertions are not silently rewritten.

T6
D1 materially changes.
Prior satisfaction does not automatically carry into the new material Dependency state.

T7
D1 is removed, waived or replaced under legitimate governance.
Future applicability changes; consequential prior history remains reconstructible.

T8
B actually executes despite an unsatisfied effective Dependency.
Actual is recorded as reality.
LifeOS may record/derive a violation or inconsistency but does not rewrite reality.
```

Therefore:

```text
current != historical
planned Dependency != Actual
correction != silent overwrite
material change != automatic carry-forward
```

---

# Actual may violate Dependency

A Dependency can be hard for planning or progression while reality still violates it.

Example:

```text
Dependency
Do not deploy until tests pass.

Actual
Deployment occurred while tests were failing/unknown.
```

LifeOS must preserve the deployment Actual if sufficiently established.

It may derive or record a dependency violation under appropriate semantics, but must never fabricate prerequisite satisfaction merely to make history consistent with the plan.

---

# Version / correction / reconciliation

Where a Dependency materially changes, historical satisfaction or acknowledgement must not silently carry forward unless the owning semantics explicitly justify it.

Correction of a wrongly recorded Dependency preserves prior assertion/history where that prior assertion mattered.

Competing Dependency assertions may coexist temporarily. Reconciliation may select, qualify, supersede or leave the conflict unresolved according to the accepted reconciliation discipline.

There is no universal newest-wins, provider-wins, manager-wins, AI-confidence-wins or last-write-wins rule.

---

# Multi-Actor semantics

A shared Dependency does not imply shared Agreement, shared Authority or universal Visibility.

Different actors may legitimately have:

- different views of whether a dependency is believed/proposed/current;
- different Authority to establish, waive or replace it;
- different visibility into its rationale/evidence;
- private prerequisite details that yield only a bounded shared result such as `not currently eligible to proceed`.

Private reasons must not be leaked merely because their effect influences shared planning.

Accountless Persons and external actors remain supported; Dependency never requires Account identity.

AI may infer or propose a Dependency, but:

```text
AI inference != established shared Dependency
AI capability != Authority
AI proposal != human will / Agreement / Decision
```

---

# Cycles and graph semantics

Dependency is directional, but LifeOS does **not** impose a universal acyclic graph invariant.

A cycle such as:

```text
A depends on B
B depends on A
```

may represent:

- a real deadlock;
- an unsatisfiable plan;
- a modeling error;
- a specialist-domain circular dependency that must be surfaced.

The system must be able to preserve and diagnose such a state rather than erase it because a generic DAG engine would reject it.

Therefore:

```text
Dependency graph != universal DAG
```

No universal `WorkflowNode`, `DependencyGraph` or `WorkflowGraph` kernel primitive is accepted.

---

# Transitivity and indirect closure

No universal transitivity rule is accepted.

From:

```text
B depends on A
C depends on B
```

LifeOS may derive useful indirect planning consequences in a particular reasoning context, but must not universally assert a semantically equivalent direct Dependency `C depends on A`.

Direct relation and derived graph reachability are different claims.

Persisted transitive closure is a later reasoning/logical-model question, not part of Dependency v0.

---

# Alternative / composite prerequisite logic

Real cases may require:

- all prerequisites;
- any one of several prerequisites;
- threshold/quorum-like satisfaction;
- alternatives or fallback paths;
- conditional applicability.

Dependency v0 does not force one universal expression language or boolean tree into the kernel.

Such composition remains safely deferred until concrete workflows prove the minimum reusable semantics. It must not be smuggled in as arbitrary metadata that destroys invariants.

---

# Persistence consequence rule

Dependency is accepted as a canonical **specific contextual relation family/capability**, not as a mandatory universal entity/root.

A simple relation may be represented directly when the connection is semantically complete and has no material independent state/history/context.

A qualified Dependency relation is justified when the connection itself needs consequential state such as:

- materially specific prerequisite/dependent facets;
- validity/effective context;
- history/versioning/correction;
- provenance;
- governance/visibility distinctions;
- specialist semantics that belong to the relation rather than either endpoint.

A row ID, M:N cardinality, query frequency or graph traversal requirement does not by itself create independent domain identity.

Physical persistence is deferred.

---

# Canonical hardenings

1. `Dependency` is specific directional semantics, not generic association.
2. It binds a dependent facet/state/transition where that distinction matters.
3. It binds the materially relevant prerequisite state/result where consequential.
4. `Dependency != Temporal Constraint`.
5. Pure before/after ordering does not prove Dependency.
6. Lag/lead/spacing remain Time / Temporal Constraint semantics.
7. `Dependency != Trigger / automatic action`.
8. Prerequisite satisfaction does not execute the dependent target.
9. `Dependency != Criterion / Evaluation`.
10. `Dependency != Resource Requirement / Allocation / Capacity Claim`.
11. `Dependency != Responsibility / Participation`.
12. Dependency does not establish Authority.
13. Dependency existence does not imply Agreement, Consent or Acknowledgement.
14. `Dependency != causality`.
15. Actual may violate an effective planned Dependency.
16. Violation never rewrites Actual to make the plan appear correct.
17. Removing, waiving or replacing a Dependency does not erase consequential history.
18. Material Dependency change does not silently inherit prior satisfaction.
19. `blocked` / `satisfied` are normally derived from Dependency plus applicable states.
20. No universal transitivity.
21. No universal symmetry/inverse semantics beyond explicit orientation.
22. No universal acyclic-DAG requirement.
23. AI inference/proposal does not establish shared Dependency.
24. Simple direct or specifically qualified representation is allowed; no universal Dependency root/entity is required.

---

# Explicitly rejected designs

Dependency v0 rejects:

- universal `Relationship` root used as a typed-edge dumping ground;
- universal `Dependency` aggregate root merely because many domains can depend on one another;
- `WorkflowNode` as a universal supertype;
- universal `DependencyGraph` / `WorkflowGraph` kernel;
- mandatory DAG topology;
- universal transitive closure as canonical stored fact;
- `blocked=true` as foundational state independent from prerequisite evidence/state;
- merging Dependency into Temporal Constraint;
- merging Dependency into Trigger/automation;
- treating prerequisite relation as causality;
- treating parent/child or ordering as dependency by default.

---

# Safe deferred register

## Trigger / Conditional Policy

**Why safe:** dependency satisfaction and automatic downstream action remain distinguishable.  
**Owner:** Trigger / Conditional Policy review.  
**Reopen trigger:** ordinary automation cannot be modeled without making Dependency itself initiate action.  
**Rerun:** CORE-03, CORE-04, CORE-13, MA-06, MA-17, XCON-02, XCON-04.

## all/any/alternative prerequisite composition

**Why safe:** core directional contingency remains valid without fixing a universal boolean expression language.  
**Owner:** Dependency logical/reasoning model.  
**Reopen trigger:** common cases require changing Dependency identity/boundary rather than extending expression/qualification.  
**Rerun:** CORE-03, CORE-10, CORE-13, MA-16, MA-18, XCON-04.

## transitive / indirect closure

**Why safe:** direct Dependency and derived graph reachability remain separable.  
**Owner:** reasoning/query layer.  
**Reopen trigger:** required reasoning cannot preserve truthful direct semantics without stored universal closure.  
**Rerun:** CORE-03, CORE-10, CORE-13, XCON-04.

## cycle / deadlock feasibility analysis

**Why safe:** cycles can be represented without fixing diagnostic algorithms.  
**Owner:** reasoning/planning.  
**Reopen trigger:** unsatisfiable planning cannot be detected without changing Dependency semantics.  
**Rerun:** CORE-02, CORE-10, CORE-13, XCON-03, XCON-04.

## Contribution / support relation

**Why safe:** `helps/supports/contributes to` does not have to be falsely represented as prerequisite.  
**Owner:** Contribution review.  
**Reopen trigger:** ordinary contribution semantics cannot remain separate from Dependency.  
**Rerun:** CORE-03, CORE-04, CORE-05, XCON-04.

## Collective / Group / quorum

**Why safe:** Dependency does not require a group identity merely to exist.  
**Owner:** collective semantics review.  
**Reopen trigger:** establishing/waiving Dependency requires irreducible group/quorum semantics.  
**Rerun:** MA-02, MA-05, MA-06, MA-13, MA-19.

## specialist workflow mapping

**Owner:** specialist-domain adapters.  
**Reopen trigger:** a concrete specialist workflow requires semantics contradictory to the canonical boundary.  
**Rerun:** relevant CORE/MA/XCON tests.

## retention / audit

**Owner:** privacy/retention/security.  
**Reopen trigger:** required historical traceability cannot coexist with retention/privacy obligations under current separation.  
**Rerun:** CORE-09, MA-07, MA-11, MA-13.

## logical / physical / API representation

**Owner:** later logical-model stage.  
**Reopen trigger:** no implementation can preserve the accepted semantics without introducing a stronger domain abstraction.  
**Rerun:** CORE-10, CORE-13, XCON-01, XCON-04.

---

## Current verdict

```text
DEPENDENCY v0

PASS WITH HARDENING

canonical specific contextual relation family   ACCEPTED
Prerequisite as semantic role                   ACCEPTED
blocked/satisfied as derived projection          ACCEPTED
universal Dependency root/entity                REJECTED
universal DAG/workflow graph                     REJECTED
universal transitivity                           REJECTED
Dependency = Temporal Constraint                 REJECTED
Dependency = Trigger                             REJECTED
Dependency = causality                           REJECTED

REOPEN       0
UNCLASSIFIED 0
```

This is the accepted semantic baseline. Repository-wide propagation and post-write QA are tracked separately; this document must not be read as proof that propagation is already closed.