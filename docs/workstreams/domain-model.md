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

Earlier product terminology is evidence, not automatic truth. Concepts are revalidated through real-world workflows, external benchmark/research, adversarial reduction, history/correction tests, explicit multi-actor stress and cross-concept consistency.

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
22. [`../domain/concepts/provenance.md`](../domain/concepts/provenance.md)
23. [`../domain/checkpoints/provenance-v0-validation.md`](../domain/checkpoints/provenance-v0-validation.md)
24. [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md)
25. [`../product/multi-actor-collaboration-discovery-simulation-2026-08.md`](../product/multi-actor-collaboration-discovery-simulation-2026-08.md)
26. [`../product/multi-actor-collaboration-research-2026-08.md`](../product/multi-actor-collaboration-research-2026-08.md)
27. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
28. accepted architecture/DB ADRs.

Validation Methodology v2 and its multi-actor addendum are historical audit sources only. v3 is the mandatory active standard.

---

# Operating rules

- Revalidate concepts one at a time, then run cluster-level integration.
- Use Methodology v3 for every concept/cluster checkpoint.
- Record test IDs, evidence, result, hardening/dependency and justified `N/A`.
- Allowed verdicts: `PASS`, `PASS WITH HARDENING`, `REOPEN`, `DEFERRED DEPENDENCY`.
- Keep external standards/products as evidence, not design authorities.
- Preserve planned/current/actual/history distinctions.
- Preserve source/provenance/confirmation/evidence/authority distinctions.
- Do not fabricate historical intention from later relevance.
- Do not create one table/entity per life topic.
- Do not collapse semantics into arbitrary JSON or one universal graph/reality/fact object.
- Do not let AI inference become confirmed/canonical truth automatically.
- Preserve progressive disclosure.
- Run the dedicated Multi-Actor Compatibility Gate after the Core Semantic Gate.
- New primitives require materially distinct identity/lifecycle/authority/invariants/query behavior.
- Run Cluster Integration + Cluster Multi-Actor Stress before declaring a cluster complete.
- Run final whole-domain regression, multi-actor and persistence/API pressure before broad implementation is treated as stable.

---

# Current validated baseline

```text
Intention & Execution v0        PASS
Time v0                         PASS
Cross-Cluster Validation v2     PASS
Multi-Actor Evidence Synthesis  PASS WITH HARDENING
Validation Methodology v3       ACTIVE MANDATORY STANDARD

Actual v0                       PASS WITH HARDENING / ACCEPTED
Outcome v0                      PASS WITH HARDENING / ACCEPTED
Observation v0                  PASS WITH HARDENING / ACCEPTED
Confirmation v0                 PASS WITH HARDENING / ACCEPTED
Evidence v0                     PASS WITH HARDENING / ACCEPTED
Provenance v0                   PASS WITH HARDENING / ACCEPTED
```

No current individual-concept structural reopening is required.

---

# Multi-Actor foundation

Normative reference:

- [`Multi-Actor Readiness v1`](../domain/multi-actor-readiness-v1.md)

Core direction:

```text
personal-first product
+
multi-actor-ready domain kernel
```

When actors coordinate around one real object:

```text
shared canonical fact
+
actor-scoped personal state
```

is preferred over per-user semantic duplication.

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

No Actor/Team/Organization/ACL/Stewardship primitive is pre-approved.

---

# Terminology architecture

Canonical quick reference:

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
Provenance     -> canonical bounded contextual lineage capability
```

---

# Active cluster — Observed Reality & Evidence

**Status:** IN PROGRESS — individual concept reviews complete; integrated gates are now the active task.

## Actual v0

```text
Actual = how a specific intention/expectation was realized
```

```text
Actual != Session
Actual != Outcome
Actual != Observation
Actual != Confirmation
Actual != Evidence
Actual != Provenance
```

## Outcome v0

```text
Outcome = contextual result/disposition of an Actual realization
```

```text
Outcome != lifecycle/operational state
Outcome != Observation
Outcome != artifact/output
Outcome != Milestone
Outcome != Confirmation
Outcome != Provenance
Outcome != Evidence
```

## Observation v0

> A persistent contextual record of a measured, perceived, reported, or explicitly derived property, state, value, rating, or simple assertion about a subject at an effective time or context.

```text
Observation != Actual
Observation != Outcome
Observation != Quantity
Observation != Register
Observation != Evidence
Observation != Confirmation
Observation != Provenance
```

## Confirmation v0

> A persistent contextual attestation that a specific confirmer affirms a specific version of a confirmable target as sufficiently accepted for a defined purpose at that time.

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

## Evidence v0

> Evidence is the contextual evaluative role played by information when that information materially bears on a specific claim, criterion, checkpoint, decision or other evaluation target.

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

## Provenance v0

> Provenance is bounded contextual lineage describing how a specific domain record/material version came to exist or change, including materially relevant source entities, activities, actors/systems/providers and times.

```text
Source != Provenance
Provenance != truth
Provenance != Authority
Provenance != Confirmation
Provenance != Evidence
Provenance != Version
Provenance != Audit
```

Critical hardenings:

- source is one provenance dimension;
- correction does not rewrite historical origin;
- derived/transformed information preserves material source/process lineage;
- provider ID != LifeOS identity;
- AI/OCR/import lineage must not launder authorship/source;
- subject/source/observer/recorder/transformer/confirmer/authority may differ;
- target visibility != Provenance visibility;
- Provenance access != all upstream payload access;
- retention/history != keep deleted sensitive payload forever;
- material lineage != maximal infinite lineage;
- no universal physical provenance graph/table is pre-approved.

---

# ACTIVE TASK — Reality/Evidence Cluster Integration

All individual concepts are now accepted provisionally as one set. The cluster itself is **not yet validated**.

Run, in order:

```text
Observed Reality & Evidence Cluster Integration Gate
        ↓
Observed Reality & Evidence Multi-Actor Stress Gate
        ↓
cluster verdict
```

## Required integration scenarios

At minimum stress:

1. planned Activity → multi-session Actual → Observation(s) → partial Outcome → Confirmation → Evidence → Provenance;
2. Event occurred but participant attendance differs per actor;
3. expected Occurrence passes with no information: unknown remains unknown;
4. explicit known non-performance distinguished from absent Actual;
5. conflicting device/provider Observations;
6. one actor confirms one version, then target is corrected;
7. same source supports one criterion and contradicts another;
8. historical information becomes Evidence later without rewriting original intent;
9. imported source → transformation → AI extraction → user correction lineage;
10. derived value recomputed after source correction without rewriting historical computation;
11. caregiver/assisted participation with subject/source/recorder/observer/confirmer separation;
12. shared target with private Evidence/Provenance sources;
13. external/non-LifeOS participant/provider;
14. high-conflict competing assertions/confirmations;
15. Authority differs from source/creator/confirmer;
16. AI can reason from private data but cannot disclose it or fabricate Confirmation;
17. deletion/retention of sensitive upstream data with bounded lineage;
18. high-volume imports/series without provenance/evidence row explosion;
19. simple-user interaction vs high-consequence inspection/audit;
20. historical reconstruction: what LifeOS believed then, why, and what changed later.

## Required pairwise regression

```text
Session ↔ Actual
Actual ↔ Outcome
Actual ↔ Observation
Outcome ↔ Observation
Outcome ↔ Milestone
Observation ↔ Confirmation
Observation ↔ Evidence
Observation ↔ Provenance
Confirmation ↔ Evidence
Confirmation ↔ Provenance
Evidence ↔ Provenance
Evidence ↔ GoalCriterion
Provenance ↔ future Version/Audit/Authority boundary
```

## Multi-actor mandatory questions

- shared reality != identical actor reality/participation;
- source actor != subject != recorder != observer != confirmer != authority;
- conflicting assertions can coexist;
- one actor's Confirmation != group truth;
- target visibility != Evidence/Provenance visibility;
- private source use != disclosure permission;
- external participants/providers do not require accounts;
- access revocation != deletion of historical attribution;
- AI authority <= acting principal/policy authority;
- total coordination burden must not increase just to maintain epistemic metadata.

A concept-level PASS does not substitute for this integrated gate.

---

# Next cluster — NOT STARTED

The provisional next cluster is **Data / Subjects** and must not start before an integrated Reality/Evidence PASS.

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
Provenance source/actor roles vs Subject/Person/Account
```

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

Mandatory inherited re-tests:

- Evidence vs typed Relationship semantics;
- Provenance vs Version / Decision / Audit;
- Confirmation vs Authority / Acknowledgement / Acceptance;
- competing assertions and canonical decision policy.

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
= bounded lineage explaining how records/material versions came to exist/change
```

This is not a mandatory parent/child chain and not a persistence schema.

---

# Reopen watchlist

Explicit future boundary tests:

- integrated Actual/Outcome/Observation/Confirmation/Evidence/Provenance semantics;
- Observation vs Quantity/Register;
- Confirmation vs Authority/Acknowledgement/Acceptance/Version;
- Evidence vs GoalCriterion/Relationship/Decision/Version;
- Provenance vs Version/Decision/Audit/Authority;
- provenance retention/privacy/deletion;
- subject vs observer/recorder/source/transformer;
- Milestone vs Outcome vs GoalCriterion;
- contextual competing assertions under Authority rules;
- collaborative Session vs actor-scoped Actual participation;
- Responsibility vs Assignment vs Hand-off vs Stewardship;
- Person vs Actor vs Subject vs Account/Principal;
- Resource vs Actor;
- Authority vs Visibility/governance;
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
- relationship map;
- provenance/confirmation/evidence rules;
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
Confirmation v0 accepted
↓
Evidence v0 accepted
↓
Provenance v0 accepted
↓
Reality/Evidence Cluster Integration — ACTIVE
↓
Reality/Evidence Multi-Actor Stress
↓
cluster verdict
↓ only after PASS
Data / Subjects
```

Do not skip directly to Data/Subjects or SQL/API design.

---

# Git / branch handoff

- active branch: `feature/domain-model`;
- `main` remains the integrated repository source of truth for merged work;
- multi-actor discovery/research is integrated into this branch through merge commit `08595f9526e08db53d9b446b8a7a76cd46adcd55`;
- no PR for the domain branch yet;
- backend implementation not changed here;
- Phase 4 prototype branch not changed by this workstream.

Continue from Methodology v3 + Language Map + accepted concept specs. Do not create a parallel validation standard, terminology tree or collaboration ontology.