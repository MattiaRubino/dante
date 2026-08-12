# LifeOS Domain Atlas

**Status:** In progress  
**Started:** 2026-08-10  
**Current revision:** 2026-08-12 — Quantity accepted; Register kernel candidate rejected; Subject next  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

The Domain Atlas is the working source for re-evaluating and defining LifeOS domain concepts before broad persistence or backend implementation.

Its job is to produce the strongest current domain model justified by product intent, real-world scenarios, external evidence, implementation constraints and explicit reasoning — not to preserve earlier terminology by inertia.

## Decision rule

**Accepted means current best decision, not immutable decision.**

A concept may be reopened when later scenarios, implementation pressure, external evidence, safety/privacy requirements or stronger abstractions expose a real contradiction. Changes must be deliberate and historical reasoning must not be silently erased.

Earlier product documents, simulations, glossaries, ADRs, prototypes and conversation history are evidence inputs, not automatic truth.

A roadmap item is a **candidate for validation**, not a checklist item that must survive. Candidate rejection is a valid and desirable result when the useful behavior is preserved more cleanly without an additional primitive.

---

# Mandatory concept-review protocol

All new concepts use **Domain Validation Methodology v3** and its mandatory execution template.

```text
A. Evidence + candidate formation
        ↓
B. Core Semantic Validation Gate
        ↓
C. Multi-Actor Compatibility Gate
        ↓
D. Cross-Concept Consistency Gate
        ↓
E. Adjacent Dependency Sweep
        ↓
Concept verdict
```

Dependency closure classes are operational, not concept verdicts:

```text
RESOLVED
SAFE DEFERRED
REOPEN
```

A `SAFE DEFERRED` dependency must identify why it does not block the current concept, who/what future concept or stage owns it, the exact reopening trigger, and which tests must be rerun. `Review later` without an owner/trigger is not accepted.

Every completed cluster then passes:

```text
Cluster Integration Gate
        ↓
Cluster Multi-Actor Stress Gate
        ↓
Cluster verdict
```

Data / Subjects is the one transition cluster because it began before the Adjacent Dependency Sweep was established. Its sequence is:

```text
finish Data / Subjects candidate reviews
        ↓
Data / Subjects cluster integration + multi-actor stress
        ↓
Deferred Dependency Closure — clusters 1–4
        ↓
RESOLVED / SAFE DEFERRED / REOPEN for every material open boundary
        ↓
Cross-Cluster Validation v4 — clusters 1–4
        ↓
only after PASS: Relationships / Reasoning
```

From Relationships / Reasoning onward, the Adjacent Dependency Sweep is mandatory before every concept verdict instead of accumulating unresolved adjacency until cluster end.

Before broad persistence/API stabilization:

```text
Whole-domain semantic regression
        ↓
Whole-domain multi-actor regression
        ↓
Persistence / API pressure test
        ↓
Implementation-readiness verdict
```

Canonical references:

- [`Validation Methodology v3`](validation-methodology-v3.md)
- [`Validation Execution Template v3`](validation-execution-template-v3.md)
- [`Multi-Actor Readiness v1`](multi-actor-readiness-v1.md)
- [`Domain & Product Language Map`](language-map.md)

Validation Methodology v2 and its multi-actor addendum remain historical audit/evolution evidence.

Allowed concept/cluster verdicts remain:

```text
PASS
PASS WITH HARDENING
REOPEN
DEFERRED DEPENDENCY
```

The objective is the smallest model that survives real life without losing semantic truth, history, queryability, extensibility, privacy or usability.

---

# External benchmark and interoperability rule

External standards, products, APIs and schemas are **benchmark evidence, not design authorities**.

Preferred direction:

```text
LifeOS semantics
        ↓
strong internal model
        ↓
optional adapters / mappings
        ↓
external standards/providers
```

Mature apps/products are also useful evidence because they expose product and workflow lessons accumulated through real usage. Their patterns may be borrowed, adapted, rejected, or deliberately contradicted when LifeOS has different semantics.

Provider identifiers/status taxonomies and lossless external mapping are not kernel invariants by default.

---

# Documentation standard

Canonical Domain Atlas documentation is written in English.

Each accepted concept should document where relevant:

- canonical definition;
- why the concept exists;
- validation basis;
- nearest semantic boundaries;
- identity and actor/context implications;
- lifecycle/temporal/history semantics;
- evidence/provenance implications;
- multi-actor implications;
- representative/adversarial examples;
- invariants;
- rejected alternatives;
- deliberately deferred questions;
- persistence/API implications without prematurely fixing tables.

Rejected candidates should receive a durable checkpoint when their historical presence or future reintroduction risk is material.

---

# Current validated baselines

## Intention & Execution — VALIDATED CURRENT BASELINE

Accepted:

- Goal;
- Plan;
- Activity;
- Event;
- Routine;
- Milestone.

Checkpoint:

- [`Intention & Execution Cluster v0`](checkpoints/intention-execution-v0.md)

## Time — VALIDATED CURRENT BASELINE

Accepted:

- Occurrence;
- Schedule;
- Session;
- Temporal Constraint;
- Recurrence;
- Availability & Capacity.

Checkpoint:

- [`Time Cluster v0`](checkpoints/time-v0.md)

Retained hardenings include explicit quota-period semantics, Plan/Routine progression boundaries, and Event identity/history surviving temporary absence of a current Schedule.

## Observed Reality & Evidence — VALIDATED CURRENT BASELINE

Accepted:

1. [`Actual v0`](concepts/actual.md) — [`validation`](checkpoints/actual-v0-validation.md);
2. [`Outcome v0`](concepts/outcome.md) — [`validation`](checkpoints/outcome-v0-validation.md);
3. [`Observation v0`](concepts/observation.md) — [`validation`](checkpoints/observation-v0-validation.md);
4. [`Confirmation v0`](concepts/confirmation.md) — [`validation`](checkpoints/confirmation-v0-validation.md);
5. [`Evidence v0`](concepts/evidence.md) — [`validation`](checkpoints/evidence-v0-validation.md);
6. [`Provenance v0`](concepts/provenance.md) — [`validation`](checkpoints/provenance-v0-validation.md).

Cluster checkpoint:

- [`Observed Reality & Evidence Cluster v0`](checkpoints/observed-reality-evidence-v0.md) — **PASS**.

Integrated hardenings:

- reported/asserted reality != established Actual;
- Milestone attainment is Evidence/evaluation-backed checkpoint state, not duplicate reality storage.

## Cross-cluster validation — VALIDATED CURRENT BASELINE

Current checkpoint:

- [`Cross-Cluster Validation v3`](checkpoints/cross-cluster-validation-v3.md) — **PASS**.

Historical predecessor:

- [`Cross-Cluster Validation v2`](checkpoints/cross-cluster-validation-v2.md) — retained as audit/history evidence.

Current result:

```text
Intention & Execution v0        PASS
Time v0                         PASS
Observed Reality & Evidence v0  PASS
Cross-Cluster Validation v3     PASS

18 accepted concepts retained before Cluster 4
0 structural reopenings
0 concept removals
0 justified concept merges
0 mandatory new primitives
```

## Multi-Actor Evidence Synthesis — VALIDATED CURRENT BASELINE

References:

- [`Multi-Actor Readiness v1`](multi-actor-readiness-v1.md)
- [`Multi-Actor Evidence Synthesis v0`](checkpoints/multi-actor-evidence-synthesis-v0.md)
- [`Discovery Simulation`](../product/multi-actor-collaboration-discovery-simulation-2026-08.md)
- [`External Deep Research`](../product/multi-actor-collaboration-research-2026-08.md)

The first three clusters remain compatible with the personal-first, structurally multi-actor-ready direction.

---

# Current semantic topology

```text
INTENTION / STRATEGY
Goal
Plan
Activity / Event / Routine / Milestone

TEMPORAL EXPECTATION / PLACEMENT
Recurrence
Occurrence
Temporal Constraint
Availability / Capacity
Schedule

EXECUTION / REALITY
Session
Actual
Outcome
Observation

EPISTEMIC / EVALUATION
Confirmation
Evidence
Provenance

REUSABLE DATA VALUE SEMANTICS
Quantity
```

This is not a mandatory processing chain, parent tree or persistence schema.

Examples of valid minimal shapes:

```text
weight measurement -> Observation using Quantity(66.4 kg)
spontaneous work -> Session
ordinary meeting -> Event + Schedule + Actual
longitudinal weight screen -> query over native Observations
full goal workflow -> uses only the layers that add real meaning
```

---

# Canonical boundaries — Observed Reality & Evidence

```text
Actual
= contextual realization of a specific intention/expectation

Outcome
= contextual result/disposition of that realization

Observation
= contextual measurement/perception/report/derived simple assertion

Confirmation
= contextual attestation toward a specific target/material version/purpose

Evidence
= contextual evaluative role/use of existing information

Provenance
= bounded contextual lineage of how a record/material version came to exist/change
```

Critical non-collapse rules:

```text
Actual != Session
Actual != Outcome
Actual != Observation
Actual != Confirmation
Actual != Evidence
Actual != Provenance
reported/asserted reality != established Actual

Outcome != lifecycle/operational state
Outcome != Observation
Outcome != Confirmation
Outcome != Evidence
Outcome != Provenance
Outcome != Milestone

Milestone attainment != duplicate Actual/Outcome/Observation truth

Observation != Quantity
Observation != universal RegisterEntry
Observation != Evidence
Observation != Confirmation
Observation != Provenance

Confirmation != Actual
Confirmation != Outcome
Confirmation != Observation
Confirmation != Evidence
Confirmation != Provenance
Confirmation != Acknowledgement
Confirmation != Acceptance/Agreement
Confirmation != Verification
Confirmation != Authority

Evidence != source information
Evidence != Observation
Evidence != Actual
Evidence != Outcome
Evidence != Confirmation
Evidence != Provenance
Evidence != GoalCriterion
Evidence != Milestone

Source != Provenance
Provenance != truth
Provenance != Authority
Provenance != Confirmation
Provenance != Evidence
Provenance != Version
Provenance != Audit
```

## Actual invariants

- contextual realization, not universal reality object;
- spontaneous reality may exist without Actual;
- no Actual does not mean failed/skipped/missed;
- known non-realization != unknown;
- passage of time does not establish Actual;
- reported/asserted reality does not automatically establish Actual;
- conflicting assertions may remain unresolved;
- shared Actual does not imply identical actor participation;
- correction preserves material assertion/provenance history.

## Outcome invariants

- optional/contextual;
- no universal Outcome enum;
- lifecycle state remains separate;
- absence of Outcome is not negative Outcome;
- `unconfirmed` is epistemic, not Outcome semantics;
- shared Outcome does not imply identical actor consequences.

## Observation invariants

- measurement/simple-assertion concept, not universal fact/blob;
- may exist without prior intention/Actual/Goal/saved tracker;
- effective time/context != recorded/ingested time;
- missing Observation != explicit negative != failed measurement;
- subjective/conflicting Observations may coexist;
- derived Observations preserve traceability;
- chart/query aggregates do not automatically become persisted Observations;
- high-frequency sampling does not imply row-per-tick persistence;
- subject != observer != recorder != source/provider/device != authority != viewer;
- one Observation may surface in multiple longitudinal views without duplication.

## Confirmation invariants

- contextual and optional;
- no Confirmation != false/rejected/incorrect/not performed;
- target material version/context/purpose matters;
- corrected target does not inherit prior Confirmation silently;
- `awaiting confirmation` is derived workflow state;
- imported/inferred/automatic/corrected are not Confirmation types;
- automation/AI must not fabricate human Confirmation;
- Confirmation by one actor does not imply Confirmation by another;
- Confirmation does not create Authority.

## Evidence invariants

- information is not Evidence merely because it exists;
- Evidence does not duplicate source identity/payload;
- may support, contradict or qualify an evaluation;
- Evidence existence does not establish truth;
- no Evidence != Evidence against;
- no LifeOS record != proof of non-occurrence without a justified completeness rule;
- later relevance does not rewrite historical source purpose;
- one source can serve several evaluations without duplication;
- strength/certainty is contextual rather than one universal scalar;
- conflicting Evidence remains representable;
- private Evidence use does not create disclosure permission;
- Evidence semantics do not pre-approve one persisted edge/entity per use.

## Provenance invariants

- source is one lineage dimension, not the whole concept;
- Provenance != truth/Authority/Confirmation/Evidence/Version/Audit;
- provider ID does not define LifeOS identity;
- corrections preserve materially relevant prior lineage;
- derived/transformed records retain material source/process traceability;
- AI/OCR/import chains do not launder authorship/source;
- subject/source/observer/recorder/transformer/confirmer/authority roles remain distinguishable;
- external/non-account actors can be provenance sources/agents;
- target visibility != full Provenance visibility;
- Provenance access != access to all upstream private payloads;
- retention/history does not justify keeping deleted sensitive payloads forever;
- material lineage, not maximal recursive lineage, is the default;
- no universal provenance graph/table is pre-approved.

---

# Active cluster — Data / Subjects

**Status:** IN PROGRESS — `Quantity v0` accepted; historical `Register` kernel candidate evaluated and rejected; `Subject` is the next read-only review.

Accepted in this cluster:

1. [`Quantity v0`](concepts/quantity.md) — [`validation`](checkpoints/quantity-v0-validation.md) — **PASS WITH HARDENING**.

Rejected candidate with validated product need:

2. [`Register Candidate v0`](checkpoints/register-v0-validation.md) — **KERNEL CANDIDATE REJECTED; longitudinal product/query capability retained**.

Remaining candidate topics:

- Subject;
- Person / Actor boundary;
- Asset;
- Resource.

The exact review order remains reopenable if concept evidence exposes a stronger dependency. None of these candidates is guaranteed to survive merely because it appears in the roadmap.

## Quantity current baseline

```text
Quantity
= reusable scalar amount value semantics
= magnitude + unit semantics sufficient for interpretation
!= independent entity / Observation / universal numeric wrapper
```

Core hardenings:

- number != Quantity by default;
- property/quantity-kind != unit;
- compatible units do not prove domain-semantic equivalence;
- same/compatible unit does not grant universal aggregation semantics;
- source representation != normalized/display representation;
- actor display preference != canonical data mutation;
- custom unit label != conversion rule;
- Money/MonetaryAmount is not pre-collapsed into ordinary Quantity;
- calendar-relative time is not pre-collapsed into fixed elapsed Quantity arithmetic;
- Range/Threshold/comparator semantics remain outside basic Quantity;
- Quantity does not imply a standalone SQL table/entity.

Current Quantity dependency obligations include Money/MonetaryAmount, ratings/scales, percentages/ratios/counts, custom units, elapsed-duration versus calendar time, Range/Threshold semantics, and final decimal/unit persistence. They are explicitly registered for the post-Cluster-4 closure unless resolved earlier.

## Register candidate conclusion

Historical proposal:

```text
Register + universal RegisterEntry
```

Current conclusion:

```text
native semantic records
        ↓
query / filtering / grouping
        ↓
valid aggregation / trend / comparison
        ↓
Register / Tracker / History / Progress product UI
```

Guardrails:

- no universal RegisterEntry;
- Register is not a kernel source-of-truth container;
- source records can appear in multiple views without duplication;
- deleting/changing a view does not change source history;
- valid aggregation follows the source metric/record semantics, not same-unit coincidence;
- quick capture through a tracker creates the native semantic record;
- saved tracker/view configuration may exist as product/application configuration without becoming independent domain truth;
- `Transaction`, `Movement`, `Snapshot`, or other future native record types are **not pre-approved** merely because historical Register examples mentioned them.

## Mandatory inherited re-tests

```text
Observation vs Quantity — RESOLVED by Quantity v0
Observation vs Register/RegisterEntry — RESOLVED: Register kernel candidate and universal RegisterEntry rejected
Quantity vs Register aggregation — RESOLVED at kernel level: aggregation validity is source/metric contextual
Subject vs observer/recorder/source/transformer — NEXT
sampled-series physical representation — safe implementation dependency, retain for pressure test
Availability/Capacity vs Resource
Actor vs Subject vs Resource vs Account/Principal
Provenance source/actor roles vs Subject/Person/Account
```

## Next candidate — Subject

Subject must be evaluated independently rather than assumed necessary because Observation currently uses the word `subject`.

Initial questions:

```text
Is Subject a true entity/identity?
Is Subject only a semantic role played by Person/Asset/other domain objects?
Does a universal Subject wrapper duplicate heterogeneous entities?
Can one record have primary subject plus focus/context without a new root?
Can non-account people, animals, places, assets, accounts or abstract things be subjects naturally?
Subject vs Actor vs Resource vs Account/Principal
Subject identity/history/privacy implications
```

Benchmark evidence should include mature health/knowledge/asset/contact systems where useful, but external schemas remain evidence rather than authorities.

## Mandatory closure after Data / Subjects

Before Relationships / Reasoning starts, perform one dedicated closure pass across all open dependencies from clusters 1–4.

Every material item must become:

```text
RESOLVED
or
SAFE DEFERRED with exact owner + reopening trigger
or
REOPEN
```

Then execute **Cross-Cluster Validation v4** across Intention & Execution + Time + Observed Reality & Evidence + Data / Subjects. Only a passing combined baseline permits the next cluster.

---

# Later Relationships / Reasoning review space

Likely topics:

- semantic Relationship;
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

Strong evidence indicates typed/directional semantics will likely be necessary; one universal semantic-free `related_to` is insufficient.

Mandatory inherited re-tests include:

- Evidence as semantic role vs typed Relationship representation;
- Provenance lineage vs Version/Decision/Audit;
- Confirmation vs Authority/Acknowledgement/Acceptance;
- competing assertions and canonical decision policy;
- Milestone attainment/evaluation relationship;
- collaborative Session/Actual attribution.

From this cluster onward the Adjacent Dependency Sweep is mandatory before each concept verdict.

---

# Relationship to historical product documentation

Older V1 documents remain preserved as product/history evidence.

Current known terminology refinements include:

- Project/Program are Plan product profiles unless future evidence justifies separate primitives;
- Task is Activity-facing UI language;
- Calendar Block is product/UI vocabulary, not mandatory time primitive;
- Deadline is latest-bound Temporal Constraint semantics;
- Actual is contextual realization, not generic actual-value storage;
- reported/asserted reality is not automatically established Actual;
- Outcome is contextual result/disposition, not universal completion/status;
- Observation is bounded measurement/simple assertion, not universal data row;
- Confirmation is contextual attestation, not one `confirmed` boolean;
- Evidence is evaluative use/relationship, not duplicated source data;
- Provenance is bounded lineage, not merely `source`, truth, Authority or Audit;
- Quantity is bounded scalar value semantics, not a measurement entity or universal number wrapper;
- historical `Register + RegisterEntry` is not a canonical kernel structure; longitudinal tracking remains a product/query capability over native records;
- Milestone attainment is evaluation-backed checkpoint state rather than duplicate reality storage;
- older V1 `confirmation state` labels such as imported/inferred/automatic/corrected are redistributed into Provenance, automation/inference, Version and workflow semantics.

Historical docs should not be silently rewritten merely for vocabulary uniformity. Current Domain Atlas + Language Map establish kernel precedence.

---

# Current accepted concepts

```text
Goal
Plan
Activity
Event
Routine
Milestone
Occurrence
Schedule
Session
Temporal Constraint
Recurrence
Availability & Capacity
Actual
Outcome
Observation
Confirmation
Evidence
Provenance
Quantity
```

Rejected historical/current candidates are not counted as accepted concepts.

---

# Current structural direction

```text
Goal         -> what is wanted
Plan         -> how it is pursued/organized
Activity     -> actionable intended work/behavior
Event        -> expected occurrence-centred thing
Routine      -> intended repeated execution/behavior policy
Milestone    -> meaningful contextual checkpoint
Recurrence   -> repeated/generative pattern
Occurrence   -> expected generated-instance identity
Constraint   -> where/when placement is allowed/required/preferred
Availability -> when schedulable capacity may be used
Capacity     -> compatible commitments a resource can sustain
Schedule     -> current accepted temporal assignment
Session      -> bounded actual execution episode
Actual       -> realization of a specific expectation
Outcome      -> result/disposition of realization
Observation  -> measurement/simple assertion about subject/context
Confirmation -> contextual affirmation of target/version/purpose
Evidence     -> contextual evaluative use of information
Provenance   -> bounded origin/evolution lineage
Quantity     -> reusable scalar amount value semantics
```

Cross-cutting multi-actor direction:

```text
shared canonical fact
+
actor-scoped personal state

object identity
!= account
!= participation
!= responsibility
!= performer
!= subject
!= authority
!= visibility
```

This is domain direction, not a persistence schema.

---

# Current modeling sequence

```text
Intention & Execution v0        — PASS
Time v0                         — PASS
Observed Reality & Evidence v0  — PASS
Cross-Cluster Validation v3     — PASS
Multi-Actor Evidence Synthesis  — PASS WITH HARDENING
Validation Methodology v3       — ACTIVE MANDATORY STANDARD
Quantity v0                     — ACCEPTED
Register kernel candidate       — REJECTED
RegisterEntry universal         — REJECTED

↓ NOW
Subject read-only review
↓
remaining Data / Subjects candidates
↓
Data / Subjects cluster integration + multi-actor stress
↓
Deferred Dependency Closure — clusters 1–4
↓
Cross-Cluster Validation v4 — clusters 1–4
↓ only after PASS
Relationships / Reasoning
```

---

# Reopen / deferred-dependency watchlist

The following are executable obligations, not generic reminders. The post-Cluster-4 dependency closure must classify every still-material item as `RESOLVED`, `SAFE DEFERRED`, or `REOPEN` and give SAFE DEFERRED items an explicit owner/reopening trigger.

Known inherited items include:

- Subject vs observer/recorder/source/transformer semantics;
- Person/Actor/Subject/Account/Principal boundaries;
- Availability/Capacity vs Resource;
- Actual establishment under future Authority/Decision/reconciliation rules;
- Confirmation target-version semantics vs future Version model;
- Confirmation vs Authority/Acknowledgement/Acceptance;
- Evidence vs GoalCriterion/typed Relationship/Decision/Version;
- Milestone attainment vs Evidence/GoalCriterion/Decision;
- Provenance vs Version/Decision/Audit/Authority/source precedence;
- Provenance privacy/retention/deletion;
- competing contextual assertions under Authority/Decision rules;
- collaborative Session vs actor-scoped Actual participation;
- Responsibility/Assignment/Hand-off/Stewardship;
- Authority vs Visibility/governance;
- AI context selection/inference/disclosure boundaries;
- Recurrence vs Trigger where Actual/fact anchors or arbitrary conditions meet;
- Quantity vs Money/MonetaryAmount;
- Quantity vs rating/scale/ratio/percentage/count semantics;
- Quantity vs custom unit-definition semantics;
- Quantity vs elapsed duration/calendar-relative time;
- Quantity vs Range/Threshold/comparison semantics;
- Quantity decimal/unit physical representation;
- longitudinal query/materialization and saved-view implementation;
- aggregate visibility vs source-record visibility;
- future native transaction/movement/snapshot semantics only if concrete workflow evidence justifies them.

Resolved and removed from limbo:

- Observation vs Register/RegisterEntry;
- Register as a kernel primitive;
- universal RegisterEntry;
- Quantity vs generic Register aggregation at the kernel level.

The list is expected to evolve during Data / Subjects, but nothing may remain unclassified at the scheduled closure point.

---

# Final validation rule

A final whole-domain stress test remains mandatory before broad persistence implementation.

Cluster PASS and Cross-Cluster v4 do not prevent later reopening when another cluster, physical data model, integration, implementation evidence, safety requirement or stronger real-world evidence exposes a genuine contradiction.