# LifeOS Domain Atlas

**Status:** In progress  
**Started:** 2026-08-10  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

The Domain Atlas is the working source for re-evaluating and defining LifeOS domain concepts before broad persistence or backend implementation.

Its job is to produce the strongest current domain model justified by product intent, real-world scenarios, external evidence, implementation constraints and explicit reasoning — not to preserve earlier terminology by inertia.

## Decision rule

**Accepted means current best decision, not immutable decision.**

A concept may be reopened when later scenarios, implementation pressure, external evidence, safety/privacy requirements or stronger abstractions expose a real contradiction. Changes must be deliberate and historical reasoning must not be silently erased.

Earlier product documents, simulations, glossaries, ADRs, prototypes and conversation history are evidence inputs, not automatic truth.

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
- [`Domain & Product Language Map`](language-map.md)

Validation Methodology v2 and its multi-actor addendum remain historical audit/evolution evidence.

Allowed verdicts:

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

## Cross-cluster validation — VALIDATED CURRENT BASELINE

- [`Cross-Cluster Validation v2`](checkpoints/cross-cluster-validation-v2.md)

All twelve initial concepts were retained; no justified merge/removal or universal hierarchy was found.

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

**Status:** IN PROGRESS — all individual concept reviews complete; cluster-level gates are next.

Accepted concepts:

1. [`Actual v0`](concepts/actual.md) — [`validation`](checkpoints/actual-v0-validation.md) — **PASS WITH HARDENING**;
2. [`Outcome v0`](concepts/outcome.md) — [`validation`](checkpoints/outcome-v0-validation.md) — **PASS WITH HARDENING**;
3. [`Observation v0`](concepts/observation.md) — [`validation`](checkpoints/observation-v0-validation.md) — **PASS WITH HARDENING**;
4. [`Confirmation v0`](concepts/confirmation.md) — [`validation`](checkpoints/confirmation-v0-validation.md) — **PASS WITH HARDENING**;
5. [`Evidence v0`](concepts/evidence.md) — [`validation`](checkpoints/evidence-v0-validation.md) — **PASS WITH HARDENING**;
6. [`Provenance v0`](concepts/provenance.md) — [`validation`](checkpoints/provenance-v0-validation.md) — **PASS WITH HARDENING**.

No individual concept currently requires structural reopening of the previous clusters.

## Current semantic topology

```text
Activity / Event / Occurrence / other expectation
                  ↓
               Actual
   how that expectation was realized
          ┌───────┴────────┐
          ↓                ↓
       Outcome       Observation(s)
 result/disposition  measured/asserted facts
          │                │
          └───────┬────────┘
                  ↓
           Confirmation
 optional contextual affirmation
                  │
                  ↓
Evidence role may connect eligible information
into a specific evaluation context

Provenance cuts across records/material versions
and explains how each came to exist/change.
```

This is not a mandatory parent/child chain and not a persistence schema.

Observation may exist independently without Actual or planning context. Evidence may use any eligible source information without duplicating it. Confirmation is optional. Provenance is cross-cutting lineage rather than a universal wrapper.

## Canonical boundaries

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

Outcome != lifecycle/operational state
Outcome != Observation
Outcome != Confirmation
Outcome != Evidence
Outcome != Provenance

Observation != Quantity
Observation != Register
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
- may exist without prior intention/Actual/Goal/Register;
- effective time/context != recorded/ingested time;
- missing Observation != explicit negative != failed measurement;
- subjective/conflicting Observations may coexist;
- derived Observations preserve traceability;
- chart/query aggregates do not automatically become persisted Observations;
- high-frequency sampling does not imply row-per-tick persistence;
- subject != observer != recorder != source/provider/device != authority != viewer.

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

# Immediate next work — cluster closure gates

All six individual concept reviews are complete. **Do not start Data / Subjects yet.**

Run:

```text
Observed Reality & Evidence Cluster Integration Gate
        ↓
Observed Reality & Evidence Multi-Actor Stress Gate
        ↓
cluster verdict
```

The integrated checkpoint must re-test at minimum:

- Actual ↔ Session / Outcome / Observation;
- Outcome ↔ Milestone / lifecycle state;
- Observation ↔ Confirmation / Evidence / Provenance;
- Confirmation ↔ Evidence / Provenance / future Authority/Version;
- Evidence ↔ GoalCriterion / Milestone / Provenance;
- Provenance ↔ Version / Audit / Authority boundaries;
- conflicting sources/assertions/confirmations/evidence;
- correction and historical reconstruction;
- shared reality + actor-specific participation;
- assisted participation/source attribution;
- selective disclosure and provenance/evidence privacy;
- external/non-LifeOS participants/providers;
- AI extraction/inference/confirmation/disclosure boundaries;
- deletion/retention;
- high-volume import and scale;
- simple-user vs high-consequence UX.

Only a cluster PASS/PASS WITH HARDENING permits moving on.

---

# Provisional next cluster — Data / Subjects

**Not started.**

Likely topics:

- Register;
- Quantity;
- Asset;
- Subject;
- Person/Actor review;
- Resource.

Inherited mandatory re-tests:

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

- semantic Relationship;
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

Mandatory inherited re-tests include:

- Evidence as semantic role vs typed Relationship representation;
- Provenance lineage vs Version/Decision/Audit;
- Confirmation vs Authority/Acknowledgement/Acceptance;
- competing assertions and canonical decision policy.

---

# Relationship to historical product documentation

Older V1 documents remain preserved as product/history evidence.

Current known terminology refinements include:

- Project/Program are Plan product profiles unless future evidence justifies separate primitives;
- Task is Activity-facing UI language;
- Calendar Block is product/UI vocabulary, not mandatory time primitive;
- Deadline is latest-bound Temporal Constraint semantics;
- Actual is contextual realization, not generic actual-value storage;
- Outcome is contextual result/disposition, not universal completion/status;
- Observation is bounded measurement/simple assertion, not universal data row;
- Confirmation is contextual attestation, not one `confirmed` boolean;
- Evidence is evaluative use/relationship, not duplicated source data;
- Provenance is bounded lineage, not merely `source`, truth, Authority or Audit;
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
```

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
Cross-Cluster Validation v2     — PASS
Multi-Actor Evidence Synthesis  — PASS WITH HARDENING
Validation Methodology v3       — ACTIVE MANDATORY STANDARD
Actual v0                       — ACCEPTED
Outcome v0                      — ACCEPTED
Observation v0                  — ACCEPTED
Confirmation v0                 — ACCEPTED
Evidence v0                     — ACCEPTED
Provenance v0                   — ACCEPTED

↓ NOW
Observed Reality & Evidence Cluster Integration Gate
↓
Observed Reality & Evidence Multi-Actor Stress Gate
↓
cluster verdict
↓ only after PASS
select/start Data / Subjects
```

---

# Reopen watchlist

Deliberately revisit later:

- Actual/Outcome/Observation/Confirmation/Evidence ↔ Provenance under integrated stress;
- Observation vs Quantity/Register;
- Confirmation target-version semantics vs future Version model;
- Confirmation vs Authority/Acknowledgement/Acceptance;
- Evidence vs GoalCriterion/typed Relationship/Decision/Version;
- Provenance vs Version/Decision/Audit/Authority/source precedence;
- Provenance privacy/retention/deletion;
- subject vs observer/recorder/source/transformer semantics;
- Milestone vs Outcome vs GoalCriterion;
- competing contextual assertions under Authority/Decision rules;
- collaborative Session vs actor-scoped Actual participation;
- Availability/Capacity vs Resource;
- Person/Actor/Subject/Account/Principal boundaries;
- Responsibility/Assignment/Hand-off/Stewardship;
- Authority vs Visibility/governance;
- AI context selection/inference/disclosure boundaries.

These are watch items, not current failures.

---

# Final validation rule

A final whole-domain stress test remains mandatory before broad persistence implementation.

Cluster PASS does not prevent later reopening when another cluster, physical data model, integration, implementation evidence, safety requirement or stronger real-world evidence exposes a genuine contradiction.