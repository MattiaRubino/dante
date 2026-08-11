# Workstream — Core Domain Model v0

- Status: **IN PROGRESS**
- Active branch: `feature/domain-model`
- Current upstream baseline: `main` integrated through `c5120ff463e027c42f4a26fc613d0917596ca738`
- Main-to-domain merge commit: `08595f9526e08db53d9b446b8a7a76cd46adcd55`
- PR: none yet
- Work type: domain modeling / invariants / persistence preparation
- Backend implementation: not started in this branch

## Purpose

Turn LifeOS product requirements into an implementation-ready domain model without prematurely fixing specialist modules, collaboration infrastructure, API shapes or final SQL tables.

Earlier product terminology is evidence, not automatic truth. Concepts are revalidated through real-world workflows, external benchmark/research, adversarial reduction, history/correction tests, multi-actor stress and cross-concept consistency.

**Accepted means current best decision, not immutable decision.**

---

# Required reading

1. [`../PROJECT-STATUS.md`](../PROJECT-STATUS.md)
2. [`../development/operating-rules.md`](../development/operating-rules.md)
3. [`../domain/README.md`](../domain/README.md)
4. [`../domain/language-map.md`](../domain/language-map.md)
5. [`../domain/validation-methodology-v3.md`](../domain/validation-methodology-v3.md)
6. [`../domain/validation-execution-template-v3.md`](../domain/validation-execution-template-v3.md)
7. [`../domain/multi-actor-readiness-v1.md`](../domain/multi-actor-readiness-v1.md)
8. [`../domain/checkpoints/intention-execution-v0.md`](../domain/checkpoints/intention-execution-v0.md)
9. [`../domain/checkpoints/time-v0.md`](../domain/checkpoints/time-v0.md)
10. [`../domain/checkpoints/cross-cluster-validation-v2.md`](../domain/checkpoints/cross-cluster-validation-v2.md)
11. [`../domain/checkpoints/multi-actor-evidence-synthesis-v0.md`](../domain/checkpoints/multi-actor-evidence-synthesis-v0.md)
12. [`../domain/concepts/actual.md`](../domain/concepts/actual.md)
13. [`../domain/checkpoints/actual-v0-validation.md`](../domain/checkpoints/actual-v0-validation.md)
14. [`../domain/concepts/outcome.md`](../domain/concepts/outcome.md)
15. [`../domain/checkpoints/outcome-v0-validation.md`](../domain/checkpoints/outcome-v0-validation.md)
16. accepted concept specs under [`../domain/concepts/`](../domain/concepts/)
17. [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md)
18. [`../product/multi-actor-collaboration-discovery-simulation-2026-08.md`](../product/multi-actor-collaboration-discovery-simulation-2026-08.md)
19. [`../product/multi-actor-collaboration-research-2026-08.md`](../product/multi-actor-collaboration-research-2026-08.md)
20. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
21. accepted DB/architecture ADRs.

Validation Methodology v2 and its multi-actor addendum are historical audit sources only. v3 is the mandatory active standard.

The old V1 glossary remains historical/product evidence. Current kernel terminology is defined by accepted Domain Atlas concepts + Language Map.

---

# Operating rules

- Revalidate concepts one at a time.
- Use Methodology v3 for every new concept and cluster checkpoint.
- Record test IDs, evidence, result, hardening/dependency and justified `N/A` rather than relying on informal discussion.
- Use only `PASS`, `PASS WITH HARDENING`, `REOPEN`, or `DEFERRED DEPENDENCY` as validation verdicts.
- Do not inherit terminology by inertia.
- Keep external standards/products as evidence, not design authorities.
- Preserve planned/current/actual/history distinctions.
- Preserve provenance/source/assertion/authority distinctions.
- Do not fabricate historical intention from later relevance.
- Do not create one table/entity per life topic.
- Do not collapse core semantics into arbitrary JSON or one universal graph/reality object.
- Do not let AI inference become confirmed/canonical truth automatically.
- Preserve progressive disclosure: kernel precision must not become UI bureaucracy.
- Run the dedicated Multi-Actor Compatibility Gate after the Core Semantic Gate.
- New primitives require materially distinct identity/lifecycle/authority/invariants/query behavior.
- Run cluster integration + cluster multi-actor stress before declaring a cluster complete.
- Run final whole-domain regression, multi-actor and persistence/API pressure gates before broad implementation is treated as stable.

---

# Current validated baseline

```text
Intention & Execution v0        PASS
Time v0                         PASS
Cross-Cluster Validation v2    PASS
Multi-Actor Evidence Synthesis PASS WITH HARDENING
Actual v0                       PASS WITH HARDENING / ACCEPTED
Outcome v0                      PASS WITH HARDENING / ACCEPTED
```

No current structural reopening is required.

## Intention & Execution

Accepted concepts:

- Goal;
- Plan;
- Activity;
- Event;
- Routine;
- Milestone.

Key actor-neutral hardenings:

```text
Goal identity       != governor / stakeholder / subject
Plan identity       != coordinator / contributor
Activity identity   != requester / assignee / performer
Event identity      != organizer / participant / response
Routine identity    != performer
Milestone identity  != stakeholder / approver
```

## Time

Accepted concepts:

- Occurrence;
- Schedule;
- Session;
- Temporal Constraint;
- Recurrence;
- Availability & Capacity.

Critical invariants retained:

```text
Schedule != Actual
Schedule != Capacity
Constraint != Schedule
Recurrence != Routine
Occurrence identity != timestamp
passage of time != completion
```

Time hardenings also retain quota-period semantics, Event-without-current-Schedule history and the Plan-vs-mega-Routine progression guardrail.

---

# Validation standard — v3

Current mandatory pipeline:

```text
Evidence + candidate formation
        ↓
Core Semantic Validation Gate
        ↓
Multi-Actor Compatibility Gate
        ↓
Cross-Concept Consistency Gate
        ↓
Concept verdict
```

Completed clusters then run:

```text
Cluster Integration Gate
        ↓
Cluster Multi-Actor Stress Gate
        ↓
Cluster verdict
```

Before broad persistence/API stabilization:

```text
Whole-domain regression
        ↓
Whole-domain multi-actor gate
        ↓
Persistence/API/implementation pressure
```

The v3 registry includes stable `CORE-*`, `MA-*`, `XCON-*`, and cluster test IDs. `MA-20 Actor-Scoped Reality Attribution` is mandatory where reality/execution/participation semantics are involved.

---

# Multi-Actor foundation — current state

Current normative reference:

- [`Multi-Actor Readiness v1`](../domain/multi-actor-readiness-v1.md)

Core direction:

```text
personal-first product
+
multi-actor-ready domain kernel
```

When actors genuinely coordinate around one real object:

```text
shared canonical fact
+
actor-scoped personal state
```

is preferred over per-user semantic copies.

Non-collapse rules:

```text
object identity
!= account
!= participant
!= responsibility
!= performer
!= subject
!= authority
!= visibility
```

Evidence-backed requirements include open/claimable responsibility, hand-off, stewardship/mental-load distinction, selective disclosure, inference privacy, external/assisted participation, relationship revocation, high-conflict scenarios, unequal power, per-actor coordination burden and bounded AI authority.

No Actor/Team/Organization/ACL/Stewardship primitive is pre-approved.

---

# Terminology architecture

Current canonical quick reference:

- [`Domain & Product Language Map`](../domain/language-map.md)

Four terminology layers:

```text
DOMAIN
PRODUCT
UI
IMPLEMENTATION
```

Important mappings:

```text
Task           -> Activity product/UI term
Project        -> Plan product profile
Program        -> Plan product profile
Deadline       -> latest-bound Temporal Constraint meaning
Calendar Block -> product/UI representation of temporal/capacity semantics
Occurrence     -> canonical domain concept, usually hidden in simple UI
Actual         -> canonical contextual realization concept, usually hidden/advanced
Outcome        -> canonical contextual result/disposition concept, usually contextual/hidden
```

---

# Active cluster — Observed Reality & Evidence

Status: **IN PROGRESS**.

## Actual v0 — accepted

Canonical source:

- [`Actual v0`](../domain/concepts/actual.md)

Validation:

- [`Actual v0 Validation`](../domain/checkpoints/actual-v0-validation.md)

Verdict:

```text
PASS WITH HARDENING
```

Canonical definition:

> An Actual is a persistent contextual realization record representing whether and how a specific intended or expected domain subject was realized in reality. It preserves the realized truth of that expectation without replacing the Sessions, Observations, Outcomes, participation records, Confirmations, or Provenance that describe particular facets of what happened or how LifeOS knows it.

Critical boundaries:

```text
Actual != Session
Actual != Outcome
Actual != Observation
Actual != Evidence
Actual != Confirmation
Actual != Provenance
```

Critical hardenings:

- Actual is contextual, not a universal reality mega-object;
- spontaneous Session/Observation/etc. may exist without Actual when no expectation is being reconciled;
- no established Actual != known non-realization;
- passage of time does not establish Actual;
- known non-realization can be a valid Actual;
- one Activity realization may use multiple Sessions;
- ordinary Event occurrence can have Actual without a fake Session;
- Actual does not duplicate measurements/facts owned by Observation or specialist records;
- corrections preserve relevant assertion/provenance history;
- provider ID/source does not define LifeOS Actual identity;
- shared Actual != identical actor-specific participation;
- subject, recorder, responsible actor, expected performer and actual performer may differ;
- AI/system knowledge of private Actual does not grant disclosure authority.

## Outcome v0 — accepted

Canonical source:

- [`Outcome v0`](../domain/concepts/outcome.md)

Validation:

- [`Outcome v0 Validation`](../domain/checkpoints/outcome-v0-validation.md)

Verdict:

```text
PASS WITH HARDENING
```

Canonical definition:

> An Outcome is a contextual representation of the result or disposition established for a specific Actual realization, describing what that realization achieved, produced, satisfied, failed to satisfy, or otherwise resolved in the relevant evaluation context. Outcome does not replace lifecycle/operational state, Observations or measurements, produced artifacts, Milestone attainment, Confirmation, Provenance, or actor-specific participation facts.

Critical boundaries:

```text
Outcome != Actual
Outcome != lifecycle/operational state
Outcome != Observation
Outcome != produced artifact/output
Outcome != Milestone
Outcome != Confirmation
Outcome != Provenance
Outcome != Evidence
```

Critical hardenings:

- Outcome is optional/contextual rather than mandatory for every Actual;
- one global completion/result enum is rejected;
- absence of Outcome != failure/missed/not-completed;
- `unconfirmed` belongs to epistemic/Confirmation semantics;
- measurements and artifacts remain separate;
- partial result does not universally mean failure;
- replacement preserves history/relationship semantics;
- shared Outcome != identical actor-specific consequences;
- one actor/provider assertion != universal canonical Outcome;
- AI inference does not create authority or disclosure permission;
- corrections preserve relevant earlier assertion/provenance history.

Mandatory re-tests:

- Outcome vs Observation;
- Outcome vs Confirmation/Provenance;
- Outcome vs Milestone at cluster level;
- contextual competing Outcomes under future authority rules;
- Evidence usage;
- logical/persistence pressure gate.

## Next concept — Observation

Observation is now the active **read-only** review target.

It must justify a distinct domain boundary against:

- Actual;
- Outcome;
- raw measurement/value;
- Register/Quantity semantics;
- Event/Session facts;
- Confirmation;
- Evidence;
- Provenance;
- subject/source/actor attribution.

No Observation primitive is accepted until it passes the full v3 pipeline.

Likely remaining cluster candidates after Observation:

- Confirmation;
- Evidence;
- Provenance.

Cluster membership can change if redundancy/merge tests demonstrate a stronger model.

---

# Later review space

## Data / Subjects

Likely topics:

- Register;
- Quantity;
- Asset;
- Subject;
- Person/Actor boundary;
- Resource.

## Relationships / Reasoning

Likely topics:

- Relationship;
- Dependency;
- Responsibility / Assignment / Hand-off;
- Contribution;
- Goal relationships;
- Evidence/Criterion relationships;
- Authority / Visibility;
- Decision;
- Version;
- AI Proposal.

Strong evidence indicates typed/directional semantics will likely be necessary; one universal semantic-free `related_to` is insufficient.

---

# Current conceptual topology

```text
Goal
↓ optional
Plan
↓ optional
Routine / Activity / Event / Milestone
↓ where recurring
Recurrence -> Occurrence

Temporal Constraints
Availability / Capacity
existing commitments
        ↓
feasibility evaluation
        ↕
Schedule
        ↓
Session where executable episode exists
        ↓
Actual realization context
        ↓
Outcome where result/disposition matters
        ↓
Observation / Evidence / Confirmation / Provenance
        (remaining boundaries under review)
```

This is not a mandatory parent/child chain and not a persistence schema.

Multi-actor relationships cut across the topology rather than forming a duplicate domain model.

---

# Reopen watchlist

Explicit future boundary tests:

- Actual vs Observation/Evidence;
- Actual vs Confirmation/Provenance;
- Outcome vs Observation;
- Outcome vs Confirmation/Provenance;
- Milestone vs Outcome vs GoalCriterion;
- contextual competing Outcomes under authority rules;
- Plan vs Routine under complex progression;
- collaborative Session vs broader Actual/actor attribution;
- Event participation vs personal commitment/delegation;
- Responsibility vs Assignment vs Hand-off vs Stewardship;
- Person vs Actor vs Subject vs Account/Principal;
- Resource vs Actor;
- Authority vs Visibility vs governance;
- completion-relative Recurrence vs Trigger/relative Constraint;
- typed/directional Relationship vocabulary;
- AI Context Builder inference/disclosure boundaries.

These are watch items, not current failures.

---

# Before broad persistence/backend implementation

The full Domain Atlas must eventually establish:

- conceptual model;
- entity/value-object/relationship boundaries;
- identity/invariants;
- actor/context/authority model;
- lifecycle/state distinctions;
- structural + semantic relationship map;
- provenance/confirmation rules;
- AI authority/proposal boundaries;
- logical data model;
- physical PostgreSQL model;
- API contracts;
- backend package boundaries;
- final whole-domain stress result.

Only after the domain is coherent should production persistence be treated as stable.

---

# Current task / sequencing

```text
Actual v0 accepted
        ↓
Outcome v0 accepted
        ↓
Observation review — ACTIVE READ-ONLY
        ↓
remaining Reality/Evidence concepts
        ↓
Reality/Evidence cluster integration
        ↓
Reality/Evidence Multi-Actor Stress Gate
```

Do not skip directly to SQL/API design.

---

# Git / branch handoff

- active branch: `feature/domain-model`;
- `main` remains the integrated repository source of truth for merged work;
- multi-actor discovery/research from PR #6 is integrated into this branch through merge commit `08595f9526e08db53d9b446b8a7a76cd46adcd55`;
- no PR for the domain branch yet;
- backend implementation not changed here;
- Phase 4 prototype branch not changed by this workstream.

Continue from Methodology v3 + Language Map + accepted concept specs. Do not create a parallel validation standard, terminology tree or collaboration ontology.