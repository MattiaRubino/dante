# LifeOS Domain Atlas

**Status:** In progress — Clusters 1–4 validated together; Relationships / Reasoning in progress  
**Started:** 2026-08-10  
**Current revision:** 2026-08-12 — Relationship review PASS WITH HARDENING; universal Relationship root rejected; Responsibility family next  
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

A terminology-neutral review may also confirm that a concept is useful while leaving its exact noun renameable. Asset v0 currently follows this rule.

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

The special Data / Subjects transition has now been executed in full:

```text
candidate reviews
        ↓
Data / Subjects integration + multi-actor stress
        ↓
terminology-neutral Asset re-review
        ↓
Deferred Dependency Closure — clusters 1–4
        ↓
Cross-Cluster Validation v4
        ↓
Relationships / Reasoning may begin
```

From Relationships / Reasoning onward, the Adjacent Dependency Sweep is mandatory before **every** concept verdict instead of accumulating unresolved adjacency until cluster end.

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

Transition/current checkpoint references include:

- [`Data / Subjects Cluster v0`](checkpoints/data-subjects-v0.md)
- [`Deferred Dependency Closure — Clusters 1–4 v0`](checkpoints/deferred-dependency-closure-clusters-1-4-v0.md)
- [`Cross-Cluster Validation v4`](checkpoints/cross-cluster-validation-v4.md)
- [`Relationship v0 validation`](checkpoints/relationship-v0-validation.md)

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

Mature apps/products are useful evidence because they expose product and workflow lessons accumulated through real usage. Their patterns may be borrowed, adapted, rejected, or deliberately contradicted when LifeOS has different semantics.

The benchmark must not become terminology-led. In particular, a product calling something `Asset`, `Device`, `Resource`, `Account`, `Record`, `Relationship`, or `Entity` does not make that noun authoritative for LifeOS.

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

Cross-cutting modeling rules that reject a universal primitive but materially constrain future concepts may also be retained as checkpoints rather than being forced into a fake concept spec. `Relationship v0` follows this rule.

---

# Current validated baselines

## Intention & Execution — PASS

Accepted:

- Goal;
- Plan;
- Activity;
- Event;
- Routine;
- Milestone.

Checkpoint:

- [`Intention & Execution Cluster v0`](checkpoints/intention-execution-v0.md)

## Time — PASS

Accepted:

- Occurrence;
- Schedule;
- Session;
- Temporal Constraint;
- Recurrence;
- Availability & Capacity.

Checkpoint:

- [`Time Cluster v0`](checkpoints/time-v0.md)

Resource v0 closes the previously deferred meaning of `schedulable resource`: a provider playing contextual Resource role where time-dependent Capacity/Availability matters; no Resource entity/root is introduced.

## Observed Reality & Evidence — PASS

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

## Data / Subjects — PASS WITH HARDENING

Accepted current baselines:

1. [`Quantity v0`](concepts/quantity.md) — reusable scalar value semantics;
2. [`Subject v0`](concepts/subject.md) — contextual aboutness role, no Subject entity/root;
3. [`Person v0`](concepts/person.md) — native human identity;
4. [`Actor v0`](concepts/actor.md) — contextual agency semantics, specific-role precedence, no Actor entity/root;
5. `Account` conceptual platform/access boundary — detailed model deferred;
6. [`Asset v0`](concepts/asset.md) — current scoped physical-object native identity;
7. [`Resource v0`](concepts/resource.md) — contextual planning/execution role/capability, no Resource entity/root.

Rejected kernel candidates:

- [`Register / RegisterEntry`](checkpoints/register-v0-validation.md) — longitudinal product/query capability retained;
- universal Subject entity/root;
- universal Actor entity/root;
- universal Resource entity/root;
- universal User root;
- universal ManagedObject root.

Cluster checkpoint:

- [`Data / Subjects Cluster v0`](checkpoints/data-subjects-v0.md) — **PASS WITH HARDENING**.

Key cluster hardenings:

- Actor semantics do not replace specific relations such as `performed_by`, `recorded_by`, `confirmed_by`, `proposed_by`;
- Resource does not manufacture identity; the provider retains whatever native identity/value/pool/supply/service semantics it independently has;
- Requirement → candidate → Allocation → Reservation/Claim → Actual use/consumption remain distinguishable;
- Register/Tracker/History stays a projection over native source records;
- Asset terminology-neutral review rejected a universal ManagedObject root while retaining the physical-item identity need; the exact noun `Asset` remains renameable.

## Deferred Dependency Closure — PASS

Checkpoint:

- [`Deferred Dependency Closure — Clusters 1–4 v0`](checkpoints/deferred-dependency-closure-clusters-1-4-v0.md)

Result:

```text
REOPEN                         0
unclassified material items    0
```

Every still-material deferred item is now either RESOLVED or SAFE DEFERRED with an explicit owner, safety reason, reopening trigger, and regression tests.

## Cross-cluster validation — v4 CURRENT BASELINE

Current checkpoint:

- [`Cross-Cluster Validation v4`](checkpoints/cross-cluster-validation-v4.md) — **PASS WITH HARDENING**.

Historical predecessors:

- [`Cross-Cluster Validation v3`](checkpoints/cross-cluster-validation-v3.md) — previous Clusters 1–3 baseline;
- [`Cross-Cluster Validation v2`](checkpoints/cross-cluster-validation-v2.md) — retained as audit/history evidence.

Current result:

```text
Intention & Execution v0        PASS
Time v0                         PASS
Observed Reality & Evidence v0  PASS
Data / Subjects v0              PASS WITH HARDENING
Deferred Dependency Closure     PASS
Cross-Cluster Validation v4     PASS WITH HARDENING

structural reopenings           0
unclassified material debt      0
mandatory new primitives in v4  0
```

## Relationships / Reasoning — IN PROGRESS

First completed review:

- [`Relationship v0 validation`](checkpoints/relationship-v0-validation.md) — **PASS WITH HARDENING**.

Current result:

```text
universal Relationship entity/root/supertype   REJECTED
semantic-free related_to as kernel truth        REJECTED
specific direct relation semantics              ACCEPTED DISCIPLINE
specific qualified relation families            ALLOWED WHEN JUSTIFIED
universal relation symmetry/transitivity rules  REJECTED
```

Canonical modeling rule:

> Use the most specific truthful relation semantics. Keep a connection direct when that completely represents its domain meaning. When the relationship itself has materially relevant state, lifecycle, history, temporal scope, authority, provenance, privacy, actor-scoped state or domain invariants, model a **specific qualified relation family** rather than a universal Relationship wrapper.

Important hardenings:

- orientation must be semantically explicit, but not every relation is directional;
- structured/qualified relation != independent entity automatically;
- queryability, cardinality, graph traversal or SQL row identity do not create domain identity;
- binary representation is not mandatory when it destroys the context of a naturally richer relation;
- symmetry, inverse, transitivity and propagation belong to each specific relation family;
- existing rich semantics such as Subject, Evidence, Confirmation, Provenance, Actor roles and Resource stages must not be demoted into generic relation types;
- generic Personal Knowledge links remain separately SAFE DEFERRED and must not silently acquire operational/evidentiary/authority semantics.

Next high-leverage review family:

```text
Responsibility
Assignment
Claim
Hand-off
Stewardship / coordination burden
```

This is an **area of review**, not a list of pre-approved primitives. The purpose is to determine which distinctions are real and which are state/role/product language within a smaller semantic model.

## Multi-Actor Evidence Synthesis — VALIDATED CURRENT BASELINE

References:

- [`Multi-Actor Readiness v1`](multi-actor-readiness-v1.md)
- [`Multi-Actor Evidence Synthesis v0`](checkpoints/multi-actor-evidence-synthesis-v0.md)
- [`Discovery Simulation`](../product/multi-actor-collaboration-discovery-simulation-2026-08.md)
- [`External Deep Research`](../product/multi-actor-collaboration-research-2026-08.md)

All four completed clusters and the current Relationship modeling discipline remain compatible with the personal-first, structurally multi-actor-ready direction.

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

CONTEXTUAL ABOUTNESS ROLE
Subject

NATIVE HUMAN IDENTITY
Person

CONTEXTUAL AGENCY
Actor

PLATFORM ACCESS IDENTITY BOUNDARY
Account

CURRENT SCOPED NATIVE PHYSICAL-OBJECT IDENTITY
Asset

CONTEXTUAL PLANNING / EXECUTION ELIGIBILITY
Resource

CROSS-CUTTING RELATION MODELING DISCIPLINE
specific direct relation
or specific qualified relation when materially justified
(no universal Relationship root)
```

Key interpretations:

- Subject is a semantic role over native referent identity, not a universal entity/root;
- Person is canonical native human identity;
- Actor is contextual agency semantics, not a wrapper entity/root and not a generic replacement for specific action roles;
- Account is a distinct platform/access identity boundary whose detailed security model remains deferred;
- Asset is the current scoped physical-object identity baseline; the universal ManagedObject alternative was rejected after terminology-neutral testing;
- Resource is contextual planning/execution eligibility/capability, not a Resource identity/root, and does not manufacture identity for supplies/pools/services;
- Relationship is a modeling discipline, not an identity-bearing common node/edge object.

This topology is not a mandatory processing chain, parent tree or persistence schema.

Examples of valid minimal shapes:

```text
Person P17 --Subject role--> Observation(weight = Quantity(66.4 kg))
Person Anna --recorded_by--> Observation about Person Maria
Account Anna-A1 authenticates access without becoming Person or Actor identity
Asset A17 --Subject role--> Observation(shutter count = 32,411)
Asset A17 --Resource role--> photo-shoot requirement/allocation context
500 ml oil --supply semantics + Resource role--> maintenance requirement, no synthetic identity
Activity B --depends_on--> Activity A when simple Dependency semantics suffice
future rich Responsibility/Participation -> specific qualified relation family if validation proves it
spontaneous work -> Session
ordinary meeting -> Event + Schedule + Actual
longitudinal weight screen -> query over native Observations
full goal workflow -> uses only the layers that add real meaning
```

---

# Canonical non-collapse rules — current cross-cluster baseline

```text
Actual != Session / Outcome / Observation / Confirmation / Evidence / Provenance
reported/asserted reality != established Actual

Outcome != lifecycle state / Observation / Confirmation / Evidence / Provenance / Milestone
Milestone attainment != duplicate Actual/Outcome/Observation truth

Observation != Quantity / universal RegisterEntry / Evidence / Confirmation / Provenance

Subject entity/root = rejected
Subject != Person / Actor / Account / Principal / Asset / Resource
Subject != observer / recorder / source / transformer / authority / viewer

Person != Actor / Resource / Account / Principal / User / Asset

Actor entity/root = rejected
Actor != Resource / Account / Principal / Responsibility / Authority
Actor != specific performer/recorder/observer/confirmer/proposer relation
specific action role > generic actor edge when known

Account != Person / Actor / Subject / Principal by default

Asset != Subject / Resource / Person
Asset identity != owner / holder / custodian / steward / model definition
physical thing != Asset automatically
managed thing != Asset automatically
universal ManagedObject root = rejected

Resource entity/root = rejected
Resource != Requirement / candidate set / Allocation / Reservation / actual use
Resource != Responsibility / Performer / Participant
Resource role != provider identity
Money/Budget != Resource by default

universal Relationship entity/root/supertype = rejected
semantic-free related_to as kernel truth = rejected
specific relation meaning > generic edge
qualified relation structure != independent entity automatically
queryability/cardinality/database row id != domain identity
relation orientation/symmetry/transitivity/inverse rules are family-specific

User = product/implementation term, not domain root
Register/Tracker = product/query capability, not source-truth container

Confirmation != Acknowledgement / Acceptance / Verification / Authority
Evidence != source information / Provenance / GoalCriterion
Provenance != Source / truth / Authority / Version / Audit
```

---

# Data / Subjects integration notes

## Quantity

```text
Quantity
= reusable scalar amount value semantics
= magnitude + unit semantics sufficient for interpretation
!= independent entity / Observation / universal numeric wrapper
```

SAFE DEFERRED neighbors include Money, Rating/Scale, Ratio/Percentage/Count, custom units, elapsed Duration vs calendar period, Range/Threshold/comparator, and physical decimal/unit representation. Exact ownership/triggers are in the dependency-closure checkpoint.

## Register rejection

```text
native semantic records
        ↓
query / filtering / grouping
        ↓
valid aggregation / trend / comparison
        ↓
Register / Tracker / History / Progress UI
```

Guardrails:

- no universal RegisterEntry;
- Register is not a kernel source-of-truth container;
- source records can appear in multiple views without duplication;
- deleting/changing a view does not change source history;
- quick capture creates the native semantic record;
- `Transaction`, `Movement`, `Snapshot` are not pre-approved merely because historical examples mentioned them.

## Subject

```text
native referent
Person / Asset / future eligible concept
        ↑
     Subject role
        │
descriptive record / Observation
```

Subject ↔ Person/Actor/Account/Asset/Resource boundaries are resolved at current baseline. Focus/context and Visibility remain SAFE DEFERRED.

## Person / Actor / Account

```text
PERSON
CANONICAL NATIVE ENTITY

ACTOR
CANONICAL AGENCY SEMANTICS
NOT ENTITY / ROOT
SPECIFIC ACTION ROLE PRECEDENCE

ACCOUNT
PLATFORM / ACCESS IDENTITY BOUNDARY
DETAILED AUTH MODEL DEFERRED

USER
PRODUCT / IMPLEMENTATION TERM ONLY

PRINCIPAL
SAFE DEFERRED SECURITY/AUTHORITY CONCEPT
```

## Asset

```text
ASSET
CURRENT SCOPED NATIVE ENTITY

scope:
individually tracked
non-human physical object
identity/history materially matter
```

Terminology-neutral Cluster-4 result:

```text
universal ManagedObject abstraction  REJECTED
physical-item identity need           RETAINED
exact noun `Asset`                    NON-SEMANTIC / reopenable
```

Place/Property, living entity, Document/Artifact, FinancialAccount/service, Asset type/profile, and identity reconciliation remain SAFE DEFERRED under explicit owners/triggers.

## Resource

```text
RESOURCE
CANONICAL SEMANTIC PLANNING / EXECUTION ROLE-CAPABILITY
NOT ENTITY / ROOT
```

Planning stages remain separate:

```text
Requirement
→ candidate(s)
→ Allocation
→ Reservation / Capacity Claim
→ Actual use / consumption
```

Resource role preserves independently justified provider semantics and does not create identity.

---

# Relationships / Reasoning — ACTIVE DOMAIN REVIEW SPACE

**Status:** IN PROGRESS.

Completed so far:

- [`Relationship v0 validation`](checkpoints/relationship-v0-validation.md) — **PASS WITH HARDENING**;
- universal Relationship primitive/root rejected;
- direct-vs-specific-qualified relation discipline accepted;
- no generic `related_to` kernel truth;
- no universal symmetry/transitivity/inverse reasoning rules.

Remaining candidate space based on demonstrated dependencies includes:

- Dependency;
- Responsibility / Assignment / Claim / Hand-off / Stewardship;
- Contribution;
- Goal relationships / GoalCriterion;
- Evidence/Criterion relationships;
- Participation;
- Resource Requirement / Allocation / substitution where justified;
- Authority / Visibility;
- Acknowledgement / Acceptance / Agreement / Verification where concrete workflows require them;
- Decision;
- Version;
- AI Proposal;
- Principal / delegation / on-behalf-of security/authority semantics;
- focus/context relationships.

These remain **candidates**, not a checklist of primitives that must survive.

The next review is the Responsibility / Assignment / Claim / Hand-off / Stewardship family because it most directly stresses relation state, transfer, acceptance, coordination burden and expected-vs-actual performer semantics.

From this stage onward the Adjacent Dependency Sweep remains mandatory before every concept verdict.

Mandatory inherited re-tests include:

- Evidence as semantic role vs specific qualified relation representation;
- Provenance lineage vs Version/Decision/Audit;
- Confirmation vs Authority/Acknowledgement/Acceptance;
- competing assertions and canonical decision policy;
- Milestone attainment/evaluation relationship;
- collaborative Session/Actual attribution;
- Subject vs focus/context/Visibility;
- Person/Actor specific roles vs Participation/Responsibility/Stewardship;
- Resource Requirement/Allocation/Reservation versus Responsibility/Performer;
- Account/Principal/Authority/delegation boundaries;
- Asset ownership/possession/custody/stewardship/location/Visibility;
- historical Person/Actor/Asset/resource-allocation attribution after Account or relationship changes;
- direct-vs-qualified threshold for every material relationship family.

Do not begin SQL/API design yet.

---

# Current modeling sequence

```text
Intention & Execution v0        — PASS
Time v0                         — PASS
Observed Reality & Evidence v0  — PASS
Data / Subjects v0              — PASS WITH HARDENING
Deferred Dependency Closure     — PASS
Cross-Cluster Validation v4     — PASS WITH HARDENING
Relationship v0 review          — PASS WITH HARDENING

0 structural reopenings
0 unclassified material dependencies

↓ CURRENT
Relationships / Reasoning
  next: Responsibility / Assignment / Claim / Hand-off / Stewardship review family
  Adjacent Dependency Sweep mandatory per verdict
↓
whole-domain semantic regression
↓
whole-domain multi-actor regression
↓
persistence/API pressure
↓
logical data model
↓
physical PostgreSQL model
↓
API contracts / backend packages / implementation
```

---

# Reopen / deferred-dependency watchlist

The authoritative dependency register remains:

- [`Deferred Dependency Closure — Clusters 1–4 v0`](checkpoints/deferred-dependency-closure-clusters-1-4-v0.md).

Relationship-specific closures and reopening triggers are now additionally recorded in:

- [`Relationship v0 validation`](checkpoints/relationship-v0-validation.md).

High-value groups include:

- Milestone / GoalCriterion / Evidence / Decision;
- Confirmation / Authority / Acknowledgement / Acceptance / Verification;
- Provenance / Version / Decision / Audit / retention;
- Actual establishment / Authority / reconciliation;
- Session/Actual / Participation / actor-scoped consequences;
- Activity / Responsibility / Assignment / Hand-off / Stewardship / Performer;
- Recurrence / Trigger;
- Account / Principal / credentials / delegation;
- Person/Asset reconciliation;
- Subject / focus / Visibility / heterogeneous references;
- Asset / Place / living entities / Document / FinancialAccount / service / model/profile;
- Resource Requirement / eligibility / Allocation / Reservation / actual use / pools / supply / skill;
- Quantity / Money / Scale / Ratio / UnitDefinition / Duration / Range;
- longitudinal materialization / aggregate visibility;
- generic Personal Knowledge links;
- AI context/inference/disclosure/Authority;
- retention/deletion/anonymization.

Current transition result:

```text
REOPEN = 0
unclassified material dependency = 0
```

No item may be silently converted from SAFE DEFERRED to implementation assumption.

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
- historical `Register + RegisterEntry` is rejected as canonical kernel structure;
- Subject is a role over native identity, not an `Asset/Soggetto` universal wrapper/root;
- Person is native human identity independent of Account;
- Actor is contextual agency semantics with specific-role precedence, not a universal entity/root;
- Account is separate platform/access identity; detailed auth/security modeling is deferred;
- User remains product/implementation language, not a domain root;
- historical broad `Asset/Soggetto` grouping and universal ManagedObject root are rejected;
- Asset v0 currently means individually tracked non-human physical-object identity; exact noun remains reopenable;
- Resource is contextual planning/execution role/capability and does not manufacture identity;
- Requirement, allocation, reservation and actual use remain distinct;
- universal Relationship root / semantic-free `related_to` are rejected;
- specific direct/qualified relation semantics are the accepted modeling discipline;
- Milestone attainment is evaluation-backed checkpoint state rather than duplicate reality storage.

Historical docs should not be silently rewritten merely for vocabulary uniformity. Current Domain Atlas + Language Map establish kernel precedence.

---

# Current accepted concepts / capabilities

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
Subject (semantic role)
Person (native entity)
Actor (semantic agency role/capability)
Asset (current scoped native entity)
Resource (semantic planning/execution role/capability)
Relationship modeling discipline (cross-cutting semantic rule; not entity/root)
```

Accepted boundary but not yet a fully modeled concept:

```text
Account != Person != Actor
```

Rejected historical/current candidates are not counted as accepted concepts.

---

# Final validation rule

A final whole-domain stress test remains mandatory before broad persistence implementation.

Cross-Cluster v4 and the current Relationship review do not prevent later reopening when subsequent Relationships / Reasoning candidates, the logical/physical data model, integrations, safety/privacy requirements, or stronger real-world evidence expose a genuine contradiction.

Do not jump directly from the current semantic review to SQL/API stabilization.