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
16. [`../domain/concepts/observation.md`](../domain/concepts/observation.md)
17. [`../domain/checkpoints/observation-v0-validation.md`](../domain/checkpoints/observation-v0-validation.md)
18. accepted concept specs under [`../domain/concepts/`](../domain/concepts/)
19. [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md)
20. [`../product/multi-actor-collaboration-discovery-simulation-2026-08.md`](../product/multi-actor-collaboration-discovery-simulation-2026-08.md)
21. [`../product/multi-actor-collaboration-research-2026-08.md`](../product/multi-actor-collaboration-research-2026-08.md)
22. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
23. accepted DB/architecture ADRs.

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
- Do not collapse core semantics into arbitrary JSON or one universal graph/reality/fact object.
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
Observation v0                  PASS WITH HARDENING / ACCEPTED
```

No current structural reopening is required.

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
Observation    -> canonical measurement/simple-assertion concept, usually contextual/hidden
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

Canonical boundary:

```text
Actual
= how a specific intention/expectation was realized

Actual != Session
Actual != Outcome
Actual != Observation
Actual != Evidence
Actual != Confirmation
Actual != Provenance
```

Critical hardenings include contextual rather than universal scope, unknown != known non-realization, passage-of-time neutrality, correction history, multi-session realization, actor-specific participation separation and bounded AI authority/disclosure.

## Outcome v0 — accepted

Canonical source:

- [`Outcome v0`](../domain/concepts/outcome.md)

Validation:

- [`Outcome v0 Validation`](../domain/checkpoints/outcome-v0-validation.md)

Verdict:

```text
PASS WITH HARDENING
```

Canonical boundary:

```text
Outcome
= contextual result/disposition of an Actual realization

Outcome != lifecycle/operational state
Outcome != Observation
Outcome != produced artifact/output
Outcome != Milestone
Outcome != Confirmation
Outcome != Provenance
Outcome != Evidence
```

Critical hardenings include optional/contextual Outcome, no universal result enum, absence != failure, `unconfirmed` as epistemic rather than result semantics, shared Outcome != identical actor consequence and preservation of competing assertions/history.

## Observation v0 — accepted

Canonical source:

- [`Observation v0`](../domain/concepts/observation.md)

Validation:

- [`Observation v0 Validation`](../domain/checkpoints/observation-v0-validation.md)

Verdict:

```text
PASS WITH HARDENING
```

Canonical definition:

> An Observation is a persistent contextual record of a measured, perceived, reported, or explicitly derived property, state, value, rating, or simple assertion about a subject at an effective time or context. It preserves what was observed or asserted without by itself establishing universal truth, authority, confirmation, Outcome, or evidentiary relevance.

Critical boundaries:

```text
Observation != Actual
Observation != Outcome
Observation != Quantity
Observation != Register
Observation != Evidence
Observation != Confirmation
Observation != Provenance
```

Critical hardenings:

- measurement/simple-assertion scope; no universal fact/blob primitive;
- Observation may exist without prior intention/Actual/Goal/Register;
- stable identity not derived from current value/timestamp fields;
- correction of the same observational act != new re-observation;
- effective time/context != recorded/ingested time;
- missing != explicit negative != failed/unavailable measurement;
- subjective observations preserve perspective rather than pretending universal objectivity;
- conflicting observations may coexist without silent averaging/overwrite;
- derived observations preserve traceability;
- chart/query aggregates are not automatically persisted;
- high-frequency streams do not imply row-per-sample persistence;
- subject != observer != recorder != source/provider/device != authority != viewer;
- shared context does not force Observation visibility;
- AI inference does not automatically establish authoritative Observation.

Mandatory re-tests:

- Observation vs Quantity;
- Observation vs Register/RegisterEntry;
- Observation vs Evidence;
- Observation vs Confirmation/Provenance;
- Subject/observer/recorder/source semantics;
- high-volume persistence pressure.

## Next concept — Confirmation

Confirmation is now the active **read-only** review target.

It must justify a bounded domain role against:

- acknowledgement;
- acceptance/agreement;
- authority/canonical decision;
- source assertion;
- Observation validity;
- Actual/Outcome truth;
- Provenance;
- participant response;
- simple-user confirmation UX.

Primary risk:

> creating one generic `confirmed=true/false` field that collapses several materially different epistemic, social, workflow and authority states.

Likely remaining cluster candidates after Confirmation:

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

Mandatory inherited re-tests from Observation v0:

```text
Observation vs Quantity
Observation vs Register/RegisterEntry
Subject vs observer/recorder/source
sampled-series physical representation
```

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
        ├─ Outcome where result/disposition matters
        └─ Observation(s) describing measured/asserted reality

Confirmation / Evidence / Provenance
        boundaries under review
```

This is not a mandatory parent/child chain and not a persistence schema.

Observation may also exist independently, with no Actual or planning context.

Multi-actor relationships cut across this topology rather than forming a duplicate domain model.

---

# Reopen watchlist

Explicit future boundary tests:

- Actual vs Confirmation/Provenance;
- Outcome vs Confirmation/Provenance;
- Observation vs Evidence;
- Observation vs Confirmation/Provenance;
- Observation vs Quantity;
- Observation vs Register/RegisterEntry;
- subject vs observer/recorder/source semantics;
- Milestone vs Outcome vs GoalCriterion;
- contextual competing Outcome/Observation assertions under authority rules;
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
Observation v0 accepted
        ↓
Confirmation review — ACTIVE READ-ONLY
        ↓
Evidence / Provenance reviews
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