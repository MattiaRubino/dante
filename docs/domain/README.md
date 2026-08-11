# LifeOS Domain Atlas

**Status:** In progress  
**Started:** 2026-08-10  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

The Domain Atlas is the working source for re-evaluating and defining LifeOS domain concepts before broad persistence or backend implementation.

Its job is not to preserve earlier terminology by inertia. Its job is to produce the strongest current domain model justified by product intent, real-world scenarios, external evidence, implementation constraints and explicit reasoning.

## Decision rule

**Accepted means current best decision, not immutable decision.**

A concept may be reopened when new scenarios, evidence, implementation constraints, contradictions or stronger abstractions emerge. Changes must be deliberate and documented; prior reasoning must not be silently overwritten.

Earlier product documents, simulations, glossaries, ADRs, prototypes and conversation history are inputs to re-evaluate, not automatic truth.

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
Concept verdict
```

Every completed cluster then passes:

```text
Cluster Integration Gate
        ↓
Cluster Multi-Actor Stress Gate
        ↓
Cluster verdict
```

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

Validation Methodology v2 and its multi-actor addendum remain preserved under `history/` as audit/evolution evidence.

Allowed verdicts:

```text
PASS
PASS WITH HARDENING
REOPEN
DEFERRED DEPENDENCY
```

The goal is not the largest ontology. It is the smallest model that survives real life without losing semantic meaning, history, queryability, extensibility, privacy or usability.

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

not:

```text
external schema
        ↓
LifeOS kernel must imitate it
```

Provider identifiers, recurrence/status taxonomies and lossless external mapping are not kernel invariants by default. Adapters absorb provider-specific compromise where practical.

---

# Documentation standard

Canonical Domain Atlas documentation is written in **English**.

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
- persistence/API implications without prematurely fixing physical tables.

Checkpoint documents record the v3 test matrix, failures/hardenings, dependencies, regression scenarios and verdict.

---

# Domain & Product Language Map

Canonical quick-reference terminology:

- [`Domain & Product Language Map`](language-map.md)

It separates:

```text
DOMAIN LANGUAGE
PRODUCT LANGUAGE
UI LANGUAGE
IMPLEMENTATION LANGUAGE
```

Core rule:

> **Domain concept != mandatory UI object, and UI label != mandatory domain primitive.**

The older `docs/product/v1-core-domain-glossary.md` remains product-history evidence but is not authoritative where current Domain Atlas decisions differ.

---

# Current validated clusters

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

Key retained hardenings:

- quota Recurrence preserves an explicit-enough period frame where boundary semantics matter;
- materially changing long-horizon progression tends toward Plan rather than one mega-Routine;
- Event identity/history may survive temporary absence of current Schedule after postponement/TBD.

## Cross-cluster validation — VALIDATED CURRENT BASELINE

- [`Cross-Cluster Validation v2`](checkpoints/cross-cluster-validation-v2.md)

Result: all twelve initial concepts retained; no justified merge/removal or universal hierarchy.

## Multi-Actor Evidence Synthesis — VALIDATED CURRENT BASELINE

References:

- [`Multi-Actor Readiness v1`](multi-actor-readiness-v1.md)
- [`Multi-Actor Evidence Synthesis v0`](checkpoints/multi-actor-evidence-synthesis-v0.md)
- [`Discovery Simulation`](../product/multi-actor-collaboration-discovery-simulation-2026-08.md)
- [`External Deep Research`](../product/multi-actor-collaboration-research-2026-08.md)

Result:

```text
Intention & Execution v0 — PASS
Time v0                 — PASS
Multi-Actor Readiness   — PASS WITH EVIDENCE-BACKED HARDENING

Structural reopenings    — 0
Concept removals          — 0
Concept merges            — 0
Mandatory new primitives — 0
```

---

# Active cluster — Observed Reality & Evidence

**Status:** IN PROGRESS.

Current accepted concepts:

- [`Actual v0`](concepts/actual.md);
- [`Outcome v0`](concepts/outcome.md);
- [`Observation v0`](concepts/observation.md);
- [`Confirmation v0`](concepts/confirmation.md);
- [`Evidence v0`](concepts/evidence.md).

Validation records:

- [`Actual v0 Validation`](checkpoints/actual-v0-validation.md) — **PASS WITH HARDENING**;
- [`Outcome v0 Validation`](checkpoints/outcome-v0-validation.md) — **PASS WITH HARDENING**;
- [`Observation v0 Validation`](checkpoints/observation-v0-validation.md) — **PASS WITH HARDENING**;
- [`Confirmation v0 Validation`](checkpoints/confirmation-v0-validation.md) — **PASS WITH HARDENING**;
- [`Evidence v0 Validation`](checkpoints/evidence-v0-validation.md) — **PASS WITH HARDENING**.

## Current semantic boundaries

```text
Actual
= how a specific intention/expectation was realized

Outcome
= what result/disposition followed from that realization where result meaning matters

Observation
= what was measured/perceived/reported/derived about a subject/context

Confirmation
= who/what explicitly affirms a specific target version for a defined purpose/context

Evidence
= how existing information materially bears on a specific evaluation
```

Critical non-collapse rules:

```text
Actual != Session
Actual != Outcome
Actual != Observation
Actual != Confirmation
Actual != Evidence

Outcome != lifecycle/operational state
Outcome != Observation
Outcome != Confirmation
Outcome != Evidence

Observation != Quantity
Observation != Register
Observation != Evidence
Observation != Confirmation
Observation != Provenance

Confirmation != Actual
Confirmation != Outcome
Confirmation != Observation
Confirmation != Provenance
Confirmation != Evidence
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
```

## Actual invariants

- contextual realization concept, not universal reality mega-object;
- spontaneous reality may exist without Actual;
- no Actual does not mean failed/skipped/missed;
- known non-realization is distinct from unknown;
- passage of time does not establish Actual;
- shared Actual does not imply identical actor participation;
- correction preserves relevant assertion/provenance history.

## Outcome invariants

- optional and contextual;
- no universal Outcome enum;
- lifecycle state is distinct;
- absence of Outcome is not negative Outcome;
- `unconfirmed` belongs to epistemic semantics;
- shared Outcome does not imply identical actor consequences;
- one actor/provider assertion does not automatically establish universal canonical Outcome.

## Observation invariants

- measurement/simple-assertion concept, not universal data/fact/blob primitive;
- may exist without prior intention/Actual/Goal/Register;
- effective time/context != recorded/ingested time;
- missing Observation != explicit negative != failed/unavailable measurement;
- subjective/conflicting Observations may coexist;
- derived Observations preserve traceability;
- chart/query aggregates do not automatically become persisted Observations;
- high-frequency sampling does not imply one physical row per tick;
- subject != observer != recorder != source/provider/device != authority != viewer.

## Confirmation invariants

- contextual and optional, not a universal truth flag;
- no Confirmation != false/rejected/incorrect/not performed;
- targets a specific material target version/context/purpose;
- materially corrected target does not silently inherit prior Confirmation;
- `awaiting confirmation` is derived workflow state;
- imported/inferred/automatic/corrected are not Confirmation types;
- automation/AI must not fabricate human Confirmation;
- Confirmation by one actor does not imply Confirmation by another;
- subject, confirmer, recorder, observer, performer and authority actor may differ;
- conflicting Confirmations remain representable;
- Confirmation does not grant Authority.

## Evidence invariants

- Evidence is contextual evaluative role/use, not intrinsic source-data type;
- information is not Evidence merely because it exists;
- source information retains its own identity and is not duplicated by default;
- Evidence can support, contradict, qualify or otherwise materially inform an evaluation;
- Evidence existence does not itself establish target truth;
- no Evidence != Evidence against;
- no LifeOS record != proof of non-occurrence without a justified completeness/evaluation rule;
- later relevance does not rewrite historical source purpose/intention;
- one source may serve several evaluations without duplication;
- evidentiary strength/certainty is contextual, not one universal scalar;
- conflicting Evidence can coexist;
- private Evidence use does not create disclosure permission;
- AI discovery/use does not create authority or disclosure permission;
- Evidence semantics do not pre-approve one persisted entity/edge per use.

## Remaining cluster work

The cluster is **not complete** yet.

One individual candidate review remains:

1. **Provenance**.

After Provenance is reviewed under Methodology v3, the completed cluster must pass:

```text
Observed Reality & Evidence Cluster Integration Gate
        ↓
Observed Reality & Evidence Multi-Actor Stress Gate
        ↓
cluster verdict
```

Only after that verdict do we consider moving to the next cluster.

---

# Provisional next cluster — Data / Subjects

Likely topics:

- Register;
- Quantity;
- Asset;
- Subject;
- Person/Actor review;
- Resource.

Inherited mandatory re-tests include:

```text
Observation vs Quantity
Observation vs Register/RegisterEntry
Subject vs observer/recorder/source
sampled-series physical representation
Actor vs Subject vs Resource vs Account/Principal
```

This cluster has **not started**.

---

# Later Relationships / Reasoning review space

Likely topics:

- semantic Relationship;
- Dependency;
- Responsibility / Assignment / Hand-off;
- Contribution;
- Goal-to-Goal relationships;
- Evidence-to-Criterion relationships;
- Authority / Visibility;
- Decision;
- Version;
- AI Proposal.

Strong evidence indicates typed/directional semantics will likely be necessary; one universal semantic-free `related_to` is insufficient.

Evidence v0 creates a mandatory future re-test of whether its physical/logical representation should reuse typed Relationship machinery while preserving distinct evaluative semantics.

---

# Relationship to historical product documentation

Older V1 documents remain preserved as product/history evidence.

Current known differences include:

- Project/Program are current Plan product profiles rather than separate kernel primitives;
- Task is Activity-facing UI language;
- Calendar Block is product/UI vocabulary rather than mandatory time primitive;
- Deadline is latest-bound Temporal Constraint semantics;
- Actual is contextual realization, not Session or generic actual-value storage;
- Outcome is contextual result/disposition, not universal completion/status;
- Observation is bounded measurement/simple assertion, not universal data row;
- Confirmation is contextual attestation, not one universal `confirmed` flag;
- Evidence is contextual evaluative role/use, not a duplicate source record or universal proof object;
- older V1 `confirmation state` labels such as imported/inferred/automatic/corrected are reinterpreted through Provenance, automation/inference, Version and workflow semantics rather than Confirmation types.

Do not silently rewrite historical product documents solely for wording uniformity; current navigation/terminology establishes precedence.

---

# Current concepts

Accepted concept specs:

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
```

---

# Current structural direction

```text
Goal         -> what is wanted
Plan         -> how it is pursued/organized
Activity     -> what actionable work/behavior is intended
Event        -> what occurrence-centred thing is expected
Routine      -> what repeated behavioral/execution policy is intended
Milestone    -> what meaningful contextual checkpoint matters
Recurrence   -> how a repeated/generative pattern repeats
Occurrence   -> which expected generated instance exists
Constraint   -> where/when placement is allowed/required/preferred
Availability -> when schedulable capacity may be used
Capacity     -> compatible commitments a resource can sustain
Schedule     -> when execution/occurrence is currently accepted
Session      -> bounded actual execution episode
Actual       -> realization of a specific expectation
Outcome      -> result/disposition of realization
Observation  -> measurement/simple assertion about subject/context
Confirmation -> contextual affirmation of a specific target/version/purpose
Evidence     -> contextual evaluative use of existing information
Provenance   -> source/agent/process/assertion history (remaining review)
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

This is domain direction, not persistence schema.

---

# Current modeling sequence

```text
Intention & Execution v0        — PASS
Time v0                         — PASS
Cross-Cluster Validation v2     — PASS
Multi-Actor Evidence Synthesis  — PASS WITH HARDENING
Validation Methodology v3       — ACTIVE MANDATORY STANDARD
Actual v0                       — PASS WITH HARDENING / ACCEPTED
Outcome v0                      — PASS WITH HARDENING / ACCEPTED
Observation v0                  — PASS WITH HARDENING / ACCEPTED
Confirmation v0                 — PASS WITH HARDENING / ACCEPTED
Evidence v0                     — PASS WITH HARDENING / ACCEPTED

↓
Provenance review
↓
Observed Reality & Evidence cluster integration
↓
Observed Reality & Evidence Multi-Actor Stress Gate
↓
cluster verdict
↓ only after PASS
select/start next cluster
```

---

# Reopen watchlist

Deliberately revisit later:

- Actual/Outcome/Observation/Confirmation/Evidence vs Provenance;
- Evidence vs GoalCriterion/Relationship/Decision/Version;
- Confirmation target-version semantics vs future Version model;
- Confirmation vs Authority/Acknowledgement/Acceptance;
- Observation vs Quantity/Register;
- subject vs observer/recorder/source semantics;
- Milestone vs Outcome vs GoalCriterion;
- competing contextual assertions/Evidence under Authority/Decision rules;
- collaborative Session vs actor-scoped Actual participation;
- Availability/Capacity vs Resource;
- Person/Actor/Subject/Account/Principal boundaries;
- Responsibility/Assignment/Hand-off/Stewardship;
- Authority vs Visibility/governance;
- typed/directional Relationship semantics;
- AI context selection/inference/privacy/disclosure boundaries.

These are watch items, not current failures.

---

# Final validation rule

A final whole-domain stress test remains mandatory before broad persistence implementation.

Cluster PASS does not prevent later reopening when another cluster, physical data model, integration, implementation evidence, safety requirement or stronger real-world evidence exposes a genuine contradiction.