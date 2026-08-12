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

Earlier product terminology is evidence, not automatic truth. Concepts are revalidated through real-world workflows, mature-product/standard benchmarks, adversarial reduction, history/correction tests, explicit multi-actor stress and cross-concept consistency.

**Accepted means current best decision, not immutable decision.**

A roadmap concept is a candidate to validate, not an object that must survive. Rejection is the correct result when the product capability can be preserved without an additional kernel primitive.

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
10. [`../domain/checkpoints/observed-reality-evidence-v0.md`](../domain/checkpoints/observed-reality-evidence-v0.md)
11. [`../domain/checkpoints/cross-cluster-validation-v3.md`](../domain/checkpoints/cross-cluster-validation-v3.md)
12. [`../domain/checkpoints/cross-cluster-validation-v2.md`](../domain/checkpoints/cross-cluster-validation-v2.md) — historical predecessor
13. [`../domain/checkpoints/multi-actor-evidence-synthesis-v0.md`](../domain/checkpoints/multi-actor-evidence-synthesis-v0.md)
14. [`../domain/concepts/actual.md`](../domain/concepts/actual.md)
15. [`../domain/checkpoints/actual-v0-validation.md`](../domain/checkpoints/actual-v0-validation.md)
16. [`../domain/concepts/outcome.md`](../domain/concepts/outcome.md)
17. [`../domain/checkpoints/outcome-v0-validation.md`](../domain/checkpoints/outcome-v0-validation.md)
18. [`../domain/concepts/observation.md`](../domain/concepts/observation.md)
19. [`../domain/checkpoints/observation-v0-validation.md`](../domain/checkpoints/observation-v0-validation.md)
20. [`../domain/concepts/confirmation.md`](../domain/concepts/confirmation.md)
21. [`../domain/checkpoints/confirmation-v0-validation.md`](../domain/checkpoints/confirmation-v0-validation.md)
22. [`../domain/concepts/evidence.md`](../domain/concepts/evidence.md)
23. [`../domain/checkpoints/evidence-v0-validation.md`](../domain/checkpoints/evidence-v0-validation.md)
24. [`../domain/concepts/provenance.md`](../domain/concepts/provenance.md)
25. [`../domain/checkpoints/provenance-v0-validation.md`](../domain/checkpoints/provenance-v0-validation.md)
26. [`../domain/concepts/quantity.md`](../domain/concepts/quantity.md)
27. [`../domain/checkpoints/quantity-v0-validation.md`](../domain/checkpoints/quantity-v0-validation.md)
28. [`../domain/checkpoints/register-v0-validation.md`](../domain/checkpoints/register-v0-validation.md)
29. [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md)
30. [`../product/multi-actor-collaboration-discovery-simulation-2026-08.md`](../product/multi-actor-collaboration-discovery-simulation-2026-08.md)
31. [`../product/multi-actor-collaboration-research-2026-08.md`](../product/multi-actor-collaboration-research-2026-08.md)
32. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
33. accepted architecture/DB ADRs.

Validation Methodology v2 and its multi-actor addendum are historical audit sources only. v3 is the mandatory active standard.

---

# Operating rules

- Revalidate candidates one at a time, then run cluster-level integration.
- Use Methodology v3 for every concept/cluster checkpoint.
- Treat mature apps, specialist systems, standards and APIs as evidence, never as automatic design authority.
- Benchmark broadly when another domain has likely learned hard product/semantic lessons already.
- Record test IDs, evidence, result, hardening/dependency and justified `N/A`.
- Allowed concept/cluster verdicts: `PASS`, `PASS WITH HARDENING`, `REOPEN`, `DEFERRED DEPENDENCY`.
- Dependency closure classes are `RESOLVED`, `SAFE DEFERRED`, `REOPEN`; they are not additional concept verdicts.
- Candidate rejection is valid when no distinct identity/lifecycle/authority/invariant/query behavior justifies the primitive.
- Preserve the useful product capability even when a historical kernel candidate is rejected.
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
- Do not leave material neighboring questions as generic `TBD`/`review later`; every applicable closure point must classify them.
- A `SAFE DEFERRED` item must identify why it is non-blocking, its owner/future stage, exact reopening trigger and tests to rerun.
- Re-run prior clusters together when a new cluster resolves old deferred boundaries.
- Finish Data / Subjects, then perform the dedicated clusters 1–4 deferred-dependency closure and Cross-Cluster Validation v4 before Relationships / Reasoning.
- From Relationships / Reasoning onward, run the Adjacent Dependency Sweep before every concept verdict.
- Run final whole-domain regression, multi-actor and persistence/API pressure before broad implementation is treated as stable.

---

# Current validated baseline

```text
Intention & Execution v0        PASS
Time v0                         PASS
Observed Reality & Evidence v0  PASS
Cross-Cluster Validation v3     PASS
Multi-Actor Evidence Synthesis  PASS WITH HARDENING
Validation Methodology v3       ACTIVE MANDATORY STANDARD

Actual v0                       ACCEPTED
Outcome v0                      ACCEPTED
Observation v0                  ACCEPTED
Confirmation v0                 ACCEPTED
Evidence v0                     ACCEPTED
Provenance v0                   ACCEPTED
Quantity v0                     PASS WITH HARDENING / ACCEPTED
Register kernel candidate       REJECTED
Universal RegisterEntry         REJECTED
```

First-three-cluster regression result:

```text
18 accepted concepts retained before Cluster 4
0 structural reopenings
0 concept removals
0 justified concept merges
0 mandatory new primitives
```

The two current cross-cluster hardenings are:

1. reported/asserted reality != established Actual;
2. Milestone attainment is Evidence/evaluation-backed and must not duplicate underlying reality.

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
Quantity       -> canonical reusable scalar amount value semantics
Register       -> possible product/UI label for longitudinal capability, not kernel primitive
Tracker/History/Progress -> product/query views over native records
```

---

# Closed cluster — Observed Reality & Evidence

**Status:** PASS — current validated cluster baseline.

## Actual v0

```text
Actual = how a specific intention/expectation was established as realized
```

```text
Actual != Session
Actual != Outcome
Actual != Observation
Actual != Confirmation
Actual != Evidence
Actual != Provenance
reported/asserted reality != established Actual
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
Observation != universal RegisterEntry
Observation != Evidence
Observation != Confirmation
Observation != Provenance
```

Longitudinal tracker/history/report views query native Observations and other native records without duplicating them into a universal entry layer.

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

Cluster checkpoint:

- [`Observed Reality & Evidence Cluster v0`](../domain/checkpoints/observed-reality-evidence-v0.md)

Cross-cluster checkpoint:

- [`Cross-Cluster Validation v3`](../domain/checkpoints/cross-cluster-validation-v3.md)

---

# ACTIVE TASK — Data / Subjects

The first three clusters are validated together. **Data / Subjects is the active domain cluster.**

Do not jump to SQL/API design yet.

## Candidate status

```text
Quantity       ACCEPTED — canonical value semantics
Register       REJECTED as kernel primitive
RegisterEntry  REJECTED as universal semantic record
Subject        ACTIVE NEXT REVIEW
Person / Actor PENDING CANDIDATE
Asset          PENDING CANDIDATE
Resource       PENDING CANDIDATE
```

None of the pending candidates is guaranteed to survive.

## Accepted concept — Quantity v0

> A Quantity is reusable scalar value semantics representing an amount through a numerical magnitude together with unit semantics sufficient to interpret that amount. It has no independent subject, property, time, identity, provenance, intention, observation history, or evaluative meaning.

```text
Quantity != entity
number != Quantity by default
Quantity != Observation
property / quantity kind != unit
compatible unit != semantic equivalence by itself
same unit != universal aggregation permission
Quantity != Range / Threshold / comparator / criterion
```

Critical hardenings:

- source representation != normalized/display representation;
- actor-specific display unit preference does not duplicate canonical facts;
- custom unit label != global conversion rule;
- Money/MonetaryAmount is not pre-collapsed into ordinary Quantity;
- calendar-relative time is not pre-collapsed into fixed elapsed Quantity arithmetic;
- precision/rounding must not be silently fabricated;
- no standalone Quantity SQL table/entity is pre-approved.

Checkpoint:

- [`Quantity v0 Validation`](../domain/checkpoints/quantity-v0-validation.md) — **PASS WITH HARDENING**.

## Rejected candidate — Register

Historical discovery proposed a universal `Register + RegisterEntry` structure.

Current validation rejects that kernel design while preserving the user-facing need:

```text
native semantic records
        ↓
query / filtering / grouping
        ↓
valid aggregation / trend / comparison
        ↓
Register / Tracker / History / Progress product UI
```

Rules:

- no universal RegisterEntry;
- no Register source-of-truth container;
- one native record may appear in several views without duplication;
- view deletion/filter changes do not modify source facts/history;
- aggregation validity comes from source metric/record/evaluation semantics;
- quick capture creates the native semantic record;
- saved tracker configuration is product/application configuration unless future evidence proves distinct domain truth;
- `Transaction`, `Movement`, `Snapshot`, or similar concepts are not pre-approved by examples from the old Register proposal.

Checkpoint:

- [`Register Candidate v0 Validation`](../domain/checkpoints/register-v0-validation.md) — **KERNEL CANDIDATE REJECTED / PRODUCT NEED RETAINED**.

## ACTIVE NEXT REVIEW — Subject

Subject must be tested from first principles rather than inherited from Observation wording or old `Asset/Soggetto` discovery language.

Primary questions:

```text
Subject as entity vs semantic role
Subject vs Person
Subject vs Actor
Subject vs Asset
Subject vs Resource
Subject vs Account / Principal
subject/focus/context distinctions
one record with multiple possible subjects/foci
non-LifeOS person as subject
animal/plant/object/account/location/document as possible subject
subject identity/history when the same real thing changes roles
privacy/authority: being the subject != owning/entering/viewing/authorizing the record
```

Required external/product benchmark families where useful:

- FHIR subject/focus/reference patterns;
- contact/person/account systems;
- asset/device/CMMS or inventory systems;
- health/fitness apps representing people/devices;
- knowledge systems using subject/topic/focus;
- other mature products only where they expose a real semantic problem.

External shapes are evidence only. LifeOS should not create a universal Subject wrapper simply because another schema uses references.

## Mandatory inherited re-tests

```text
Observation vs Quantity — RESOLVED by Quantity v0
Observation vs Register/RegisterEntry — RESOLVED by Register rejection
Quantity vs Register aggregation — RESOLVED at kernel level
Subject vs observer/recorder/source/transformer — ACTIVE
sampled-series physical representation — SAFE implementation dependency
Availability/Capacity vs Resource
Actor vs Subject vs Resource vs Account/Principal
Provenance source/actor roles vs Subject/Person/Account
```

The Subject review is read-only until it passes Methodology v3 and a separately stated Git write scope is explicitly approved.

---

# TRANSITION GATE — after Data / Subjects

Before Relationships / Reasoning begins, execute:

```text
Data / Subjects cluster integration
        ↓
Data / Subjects multi-actor stress
        ↓
cluster verdict
        ↓
DEFERRED DEPENDENCY CLOSURE — clusters 1–4
        ↓
RESOLVED / SAFE DEFERRED / REOPEN for every material open boundary
        ↓
Cross-Cluster Validation v4 — clusters 1–4
        ↓ only after PASS
Relationships / Reasoning
```

The dependency closure must revisit inherited issues from the first three clusters as well as new Cluster 4 findings. Nothing material may remain as unowned limbo.

---

# Later Relationships / Reasoning review space

Likely topics:

- Relationship;
- Dependency;
- Responsibility / Assignment / Hand-off;
- Contribution;
- Goal relationships;
- Evidence/Criterion relationships;
- Participation;
- Authority / Visibility;
- Decision;
- Version;
- AI Proposal.

Mandatory inherited re-tests:

- Evidence vs typed Relationship semantics;
- Milestone attainment vs Evidence/GoalCriterion/Decision;
- Provenance vs Version / Decision / Audit;
- Confirmation vs Authority / Acknowledgement / Acceptance;
- competing assertions and canonical decision/reconciliation policy;
- collaborative Session/Actual attribution.

From this cluster onward, the Adjacent Dependency Sweep is mandatory before each concept verdict.

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
             └─ may use Quantity value semantics

Confirmation
= contextual affirmation of specific target/version/purpose

Evidence
= contextual evaluative use of existing information

Provenance
= bounded lineage explaining how records/material versions came to exist/change

Quantity
= reusable scalar amount value semantics also usable outside Observation

Longitudinal product views
= queries/projections over native records, not a separate truth layer
```

This is not a mandatory parent/child chain and not a persistence schema.

---

# Reopen / deferred-dependency watchlist

The post-Cluster-4 closure pass must turn every still-material item into `RESOLVED`, `SAFE DEFERRED`, or `REOPEN`.

Known inherited items include:

- Subject vs observer/recorder/source/transformer;
- Person vs Actor vs Subject vs Account/Principal;
- Availability/Capacity vs Resource;
- Actual establishment under Authority/Decision/reconciliation semantics;
- Confirmation vs Authority/Acknowledgement/Acceptance/Version;
- Evidence vs GoalCriterion/Relationship/Decision/Version;
- Milestone attainment vs Evidence/GoalCriterion/Decision;
- Provenance vs Version/Decision/Audit/Authority;
- provenance retention/privacy/deletion;
- contextual competing assertions under Authority rules;
- collaborative Session vs actor-scoped Actual participation;
- Responsibility vs Assignment vs Hand-off vs Stewardship;
- Resource vs Actor;
- Authority vs Visibility/governance;
- AI Context Builder inference/disclosure boundaries;
- Recurrence vs Trigger;
- Quantity vs Money/MonetaryAmount;
- Quantity vs ratings/scales/ratio/percentage/count semantics;
- Quantity vs custom unit-definition semantics;
- Quantity vs elapsed duration/calendar-relative time;
- Quantity vs Range/Threshold/comparator semantics;
- Quantity decimal/unit physical representation;
- longitudinal query/materialization/saved-view implementation;
- aggregate visibility vs source-record visibility;
- future transaction/movement/snapshot semantics only when concrete workflow evidence requires them.

Resolved:

- Observation vs Register/RegisterEntry;
- Register as kernel primitive;
- universal RegisterEntry;
- Quantity vs generic Register aggregation at kernel level.

These are executable obligations, not generic `later` notes.

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
Intention & Execution v0 accepted
↓
Time v0 accepted
↓
Observed Reality & Evidence v0 accepted
↓
Cross-Cluster Validation v3 PASS
↓
Data / Subjects — ACTIVE
  Quantity v0 accepted
  Register candidate rejected
  Subject read-only review now
↓
remaining Data / Subjects candidates
↓
Data / Subjects cluster integration + multi-actor stress
↓
Deferred Dependency Closure — clusters 1–4
↓
Cross-Cluster Validation v4
↓ only after PASS
Relationships / Reasoning
↓
final whole-domain gates
↓
logical/physical persistence and API stabilization
```

---

# Git / branch handoff

- active branch: `feature/domain-model`;
- `main` remains the integrated repository source of truth for merged work;
- no PR for the domain branch yet;
- backend implementation not changed here;
- Phase 4 prototype branch not changed by this workstream;
- repository visibility does not change the branch/write-scope operating rules.

Continue from Methodology v3 + Execution Template v3 + Language Map + accepted Quantity v0 + Register rejection checkpoint + the three validated cluster checkpoints. The active next candidate is `Subject` in read-only mode. Do not create a parallel validation standard, terminology tree or collaboration ontology.