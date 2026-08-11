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
18. [`../domain/concepts/confirmation.md`](../domain/concepts/confirmation.md)
19. [`../domain/checkpoints/confirmation-v0-validation.md`](../domain/checkpoints/confirmation-v0-validation.md)
20. [`../domain/concepts/evidence.md`](../domain/concepts/evidence.md)
21. [`../domain/checkpoints/evidence-v0-validation.md`](../domain/checkpoints/evidence-v0-validation.md)
22. [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md)
23. [`../product/multi-actor-collaboration-discovery-simulation-2026-08.md`](../product/multi-actor-collaboration-discovery-simulation-2026-08.md)
24. [`../product/multi-actor-collaboration-research-2026-08.md`](../product/multi-actor-collaboration-research-2026-08.md)
25. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
26. accepted architecture/DB ADRs.

Validation Methodology v2 and its multi-actor addendum are historical audit sources only. v3 is the mandatory active standard.

---

# Operating rules

- Revalidate concepts one at a time.
- Use Methodology v3 for every new concept and cluster checkpoint.
- Record test IDs, evidence, result, hardening/dependency and justified `N/A`.
- Use only `PASS`, `PASS WITH HARDENING`, `REOPEN`, or `DEFERRED DEPENDENCY` as verdicts.
- Do not inherit terminology by inertia.
- Keep external standards/products as evidence, not design authorities.
- Preserve planned/current/actual/history distinctions.
- Preserve provenance/source/assertion/authority distinctions.
- Do not fabricate historical intention from later relevance.
- Do not create one table/entity per life topic.
- Do not collapse core semantics into arbitrary JSON or one universal graph/reality/fact object.
- Do not let AI inference become confirmed/canonical truth automatically.
- Preserve progressive disclosure.
- Run the dedicated Multi-Actor Compatibility Gate after the Core Semantic Gate.
- New primitives require materially distinct identity/lifecycle/authority/invariants/query behavior.
- Run cluster integration + cluster multi-actor stress before declaring a cluster complete.
- Run final whole-domain regression, multi-actor and persistence/API pressure gates before broad implementation is treated as stable.

---

# Current validated baseline

```text
Intention & Execution v0        PASS
Time v0                         PASS
Cross-Cluster Validation v2     PASS
Multi-Actor Evidence Synthesis  PASS WITH HARDENING
Actual v0                       PASS WITH HARDENING / ACCEPTED
Outcome v0                      PASS WITH HARDENING / ACCEPTED
Observation v0                  PASS WITH HARDENING / ACCEPTED
Confirmation v0                 PASS WITH HARDENING / ACCEPTED
Evidence v0                     PASS WITH HARDENING / ACCEPTED
```

No current structural reopening is required.

---

# Validation standard — v3

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

Before persistence/API stabilization:

```text
Whole-domain regression
        ↓
Whole-domain multi-actor gate
        ↓
Persistence/API/implementation pressure
```

`MA-20 Actor-Scoped Reality Attribution` remains mandatory where reality/execution/participation semantics are involved.

---

# Multi-Actor foundation

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

Important mappings:

```text
Task           -> Activity product/UI term
Project        -> Plan product profile
Program        -> Plan product profile
Deadline       -> latest-bound Temporal Constraint
Calendar Block -> product/UI temporal/capacity representation
Occurrence     -> canonical, usually hidden
Actual         -> canonical contextual realization
Outcome        -> canonical contextual result/disposition
Observation    -> canonical measurement/simple assertion
Confirmation   -> canonical contextual attestation
Evidence       -> canonical contextual evaluative role/relationship
```

---

# Active cluster — Observed Reality & Evidence

**Status:** IN PROGRESS.

## Accepted concepts

### Actual v0

```text
Actual
= how a specific intention/expectation was realized
```

Boundaries:

```text
Actual != Session
Actual != Outcome
Actual != Observation
Actual != Confirmation
Actual != Evidence
Actual != Provenance
```

### Outcome v0

```text
Outcome
= contextual result/disposition of an Actual realization
```

Boundaries:

```text
Outcome != lifecycle/operational state
Outcome != Observation
Outcome != artifact/output
Outcome != Milestone
Outcome != Confirmation
Outcome != Provenance
Outcome != Evidence
```

### Observation v0

Canonical definition:

> An Observation is a persistent contextual record of a measured, perceived, reported, or explicitly derived property, state, value, rating, or simple assertion about a subject at an effective time or context.

Boundaries:

```text
Observation != Actual
Observation != Outcome
Observation != Quantity
Observation != Register
Observation != Evidence
Observation != Confirmation
Observation != Provenance
```

Critical hardenings include effective-time vs recorded-time separation, missing != negative, subjective/conflicting observations, derivation traceability, non-row-per-tick scale semantics and subject/observer/recorder/source/authority separation.

### Confirmation v0

Canonical definition:

> A Confirmation is a persistent contextual attestation that a specific confirmer affirms a specific version of an assertion, realization, result, observation, or other confirmable target as sufficiently accepted for a defined purpose at that time. Confirmation records the affirmation; it does not by itself prove universal truth, grant authority, replace Provenance, or change the semantic meaning of the target.

Boundaries:

```text
Confirmation != Actual
Confirmation != Outcome
Confirmation != Observation
Confirmation != Provenance
Confirmation != Evidence
Confirmation != Acknowledgement
Confirmation != Acceptance/Agreement
Confirmation != Verification
Confirmation != Authority
```

Critical hardenings:

- Confirmation is contextual/optional, not universal;
- no Confirmation != false/rejected/incorrect/not performed;
- targets a specific material target version/context/purpose;
- materially changed target does not inherit old Confirmation silently;
- `awaiting confirmation` is derived workflow state;
- imported/inferred/automatic/corrected are not Confirmation types;
- automation/AI must not fabricate human Confirmation;
- one actor's Confirmation does not become group truth;
- conflicting Confirmations remain representable;
- Confirmation does not create Authority;
- current access and historical attribution remain distinct.

Mandatory future re-tests:

- Confirmation vs Provenance;
- target-version semantics vs Version model;
- Confirmation vs Authority/Acknowledgement/Acceptance;
- persistence pressure around generic target references.

### Evidence v0

Canonical definition:

> Evidence is the contextual evaluative role played by information when that information is used to support, contradict, qualify, or otherwise materially inform the evaluation of a specific claim, criterion, checkpoint, decision, or other evaluative target. Evidence represents the relationship between source information and an evaluation context; it does not duplicate the source information, establish truth by itself, or imply that the information was originally created for that evaluation.

Boundaries:

```text
Evidence != source information itself
Evidence != Observation
Evidence != Actual
Evidence != Outcome
Evidence != Confirmation
Evidence != Provenance
Evidence != GoalCriterion
Evidence != Milestone
```

Critical hardenings:

- information is not Evidence merely because it exists;
- Evidence does not duplicate source data/identity;
- Evidence can support, contradict, qualify or otherwise materially inform;
- Evidence existence does not establish target truth by itself;
- no Evidence != Evidence against;
- no LifeOS record != proof of non-occurrence without a justified completeness/evaluation rule;
- later Evidence relevance does not rewrite historical source purpose/intention;
- one source can serve multiple evaluations without duplication;
- evidentiary strength/certainty is contextual rather than one universal scalar;
- conflicting Evidence remains representable;
- private Evidence use does not create disclosure permission;
- AI discovery/use does not create authority or disclosure permission;
- Evidence semantics do not pre-approve a persisted entity/edge for every use.

Mandatory future re-tests:

- Evidence vs Provenance;
- Evidence vs GoalCriterion;
- Evidence vs typed Relationship semantics;
- Evidence vs Decision/Version;
- private Evidence vs Authority/Visibility;
- persistence pressure around explicit/derived/materialized Evidence use.

---

# Remaining work before this cluster can close

The active cluster is **not yet ready to close**.

One individual v3 review remains:

1. **Provenance** — next/final individual concept.

Then the complete cluster must pass:

```text
Observed Reality & Evidence Cluster Integration Gate
        ↓
Observed Reality & Evidence Multi-Actor Stress Gate
        ↓
cluster verdict
```

A concept-level PASS does not substitute for this integrated cluster gate.

---

# Next cluster — not started

The provisional next cluster remains **Data / Subjects**.

Likely topics:

- Register;
- Quantity;
- Asset;
- Subject;
- Person/Actor boundary;
- Resource.

Inherited re-tests:

```text
Observation vs Quantity
Observation vs Register/RegisterEntry
Subject vs observer/recorder/source
sampled-series physical representation
Actor vs Subject vs Resource vs Account/Principal
```

We do **not** begin this cluster until Observed Reality & Evidence has received an integrated PASS.

---

# Later Relationships / Reasoning review space

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

Evidence v0 must be re-tested here: a typed Relationship implementation may carry its physical/logical representation, but Evidence semantics must remain distinguishable from generic relationship meaning.

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

Confirmation
= contextual affirmation of specific target/version/purpose

Evidence
= contextual evaluative use of existing information

Provenance
= final remaining cluster boundary under review
```

Observation may also exist independently with no Actual/planning context. Confirmation is optional and may target eligible records/assertions without becoming a universal wrapper. Evidence can later bind any eligible source information into an evaluation without duplicating that source.

Multi-actor relationships cut across this topology rather than forming a duplicate domain model.

---

# Reopen watchlist

Explicit future boundary tests:

- Actual/Outcome/Observation/Confirmation/Evidence vs Provenance;
- Evidence vs GoalCriterion/Relationship/Decision/Version;
- Observation vs Quantity/Register;
- Confirmation vs Authority/Acknowledgement/Acceptance/Version;
- subject vs observer/recorder/source semantics;
- Milestone vs Outcome vs GoalCriterion;
- contextual competing assertions/Evidence under Authority rules;
- collaborative Session vs broader Actual/actor attribution;
- Responsibility vs Assignment vs Hand-off vs Stewardship;
- Person vs Actor vs Subject vs Account/Principal;
- Resource vs Actor;
- Authority vs Visibility/governance;
- completion-relative Recurrence vs Trigger/relative Constraint;
- typed/directional Relationship vocabulary;
- AI Context Builder inference/disclosure boundaries.

These are watch items, not current failures.

---

# Current task / sequencing

```text
Actual v0 accepted
        ↓
Outcome v0 accepted
        ↓
Observation v0 accepted
        ↓
Confirmation v0 accepted
        ↓
Evidence v0 accepted
        ↓
Provenance review — NEXT / FINAL INDIVIDUAL CONCEPT
        ↓
Observed Reality & Evidence Cluster Integration Gate
        ↓
Observed Reality & Evidence Multi-Actor Stress Gate
        ↓
cluster verdict
        ↓ only after PASS
start/select next cluster
```

Do not skip directly to Data/Subjects or SQL/API design.

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

# Git / branch handoff

- active branch: `feature/domain-model`;
- `main` remains the integrated repository source of truth for merged work;
- multi-actor discovery/research from PR #6 is integrated through merge commit `08595f9526e08db53d9b446b8a7a76cd46adcd55`;
- no PR for the domain branch yet;
- backend implementation not changed here;
- Phase 4 prototype branch not changed by this workstream.

Continue from Methodology v3 + Language Map + accepted concept specs. Do not create a parallel validation standard, terminology tree or collaboration ontology.