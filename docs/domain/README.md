# LifeOS Domain Atlas

**Status:** In progress  
**Started:** 2026-08-10  
**Current revision:** 2026-08-12 — Data / Subjects candidate reviews complete through Resource v0; Cluster-4 integration is next  
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

A concept may also be accepted with an explicit mandatory re-review when the chosen terminology or benchmark family may itself bias the abstraction. `Asset v0` currently carries that obligation.

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
provisional cluster verdict for transition purposes
        ↓
Deferred Dependency Closure — clusters 1–4
(including mandatory terminology-neutral Asset revisit)
        ↓
RESOLVED / SAFE DEFERRED / REOPEN for every material open boundary
        ↓
Cross-Cluster Validation v4 — clusters 1–4
        ↓
only after PASS: Relationships / Reasoning
```

For Asset specifically, the deferred-dependency closure must include a **terminology-neutral managed/tracked-referent benchmark** before the Cluster-4 baseline can be treated as consolidated.

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

Mature apps/products are useful evidence because they expose product and workflow lessons accumulated through real usage. Their patterns may be borrowed, adapted, rejected, or deliberately contradicted when LifeOS has different semantics.

The benchmark must not become terminology-led. In particular, a product calling something `Asset`, `Device`, `Resource`, `Account`, `Record`, or `Entity` does not make that noun authoritative for LifeOS.

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

Retained hardenings include explicit quota-period semantics, Plan/Routine progression boundaries, Event identity/history surviving temporary absence of a current Schedule, and `scheduled != capacity consumed`.

Resource v0 now closes the previously deferred meaning of `schedulable resource`: a native referent/supply playing contextual Resource role where time-dependent Capacity/Availability matters; no Resource entity/root is introduced.

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
```

Key interpretations:

- Subject is a semantic role over native referent identity, not a universal entity/root;
- Person is canonical native human identity;
- Actor is contextual agency semantics, not a wrapper entity/root;
- Account is a distinct platform/access identity boundary whose detailed security model remains deferred;
- Asset is currently a native identity for individually tracked non-human physical objects whose distinct identity/history materially matter;
- Asset's physical/durable scope is explicitly subject to terminology-neutral re-review before final Cluster-4 closure;
- Resource is contextual planning/execution eligibility/capacity over native referents/supplies, not a Resource identity/root.

This topology is not a mandatory processing chain, parent tree or persistence schema.

Examples of valid minimal shapes:

```text
Person P17 --Subject role--> Observation(weight = Quantity(66.4 kg))
Person Anna --recorder/Actor role--> Observation about Person Maria
Account Anna-A1 authenticates access without becoming Person or Actor identity
Asset A17 --Subject role--> Observation(shutter count = 32,411)
Asset A17 --Resource role--> photo-shoot Activity requirement/allocation context
Person Anna --Resource role--> staffing/scheduling context without losing Person identity
spontaneous work -> Session
ordinary meeting -> Event + Schedule + Actual
longitudinal weight screen -> query over native Observations
full goal workflow -> uses only the layers that add real meaning
```

---

# Canonical boundaries — current cross-cluster baseline

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

Quantity
= reusable scalar amount value semantics

Subject
= contextual role identifying the native referent a descriptive record primarily concerns

Person
= persistent native human identity

Actor
= contextual semantic agency role/capability over native identity

Account
= platform/access identity boundary; detailed auth/security model deferred

Asset
= current scoped identity of an individually tracked non-human physical object whose identity/history materially matter

Resource
= contextual planning/execution role under which a native referent/supply may satisfy an execution requirement
```

Critical non-collapse rules now include:

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

Subject entity/root = rejected
Subject != Person
Subject != Actor
Subject != Account/Principal
Subject != Asset
Subject != Resource
Subject != observer/recorder/source/transformer/authority/viewer
Subject != generic related_to

Person != Actor
Person != Resource
Person != Account
Person != Principal
Person != User domain primitive
Person != Asset

Actor entity/root = rejected
Actor != Resource
Actor != Account
Actor != Principal
Actor != Responsibility
Actor != Authority
Actor != specific performer/recorder/observer/confirmer/proposer relation

Account != Person
Account != Actor
Account != Subject
Account != Principal by default

Asset != Subject
Asset != Resource
Asset != Person
Asset identity != owner/holder/custodian/steward
Asset instance != product/model definition
physical thing != Asset automatically
managed thing != Asset automatically
financial asset semantics != Asset entity

Resource entity/root = rejected
Resource != Requirement
Resource != candidate set
Resource != Allocation
Resource != Reservation/Capacity Claim
Resource != actual use/consumption
Resource != Responsibility/Performer/Participant
Money/Budget != Resource by default

User = product/implementation term, not domain root

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

## Subject invariants accepted

- Subject is a contextual semantic role, not independent identity;
- native Person/Asset/etc. identity remains authoritative for the referent;
- current Account is not the universal Subject default;
- non-LifeOS people and non-person referents may play Subject role;
- being Subject does not imply source, observer, recorder, owner, authority, visibility, participation, responsibility, Resource eligibility or benefit;
- unknown/later-resolved/corrected Subject attribution preserves material history;
- Subject must not become a universal `related_to` catch-all;
- Subject association itself can be privacy-sensitive;
- AI may propose native-referent resolution but does not automatically establish identity/authority;
- no universal `subjects` table/root is pre-approved.

## Person / Actor / Account invariants accepted

- Person is native persistent human identity;
- Person may exist without Account and may predate/outlive Account access;
- Person may play Subject, Actor/specific action, or Resource roles without identity change;
- Actor is contextual agency semantics, not independent identity/root;
- Actor does not replace precise roles such as performer, recorder, observer, confirmer, proposer or responsible actor;
- Actor != Responsibility/Authority/ownership/Resource;
- Account authentication/access identity does not define Person or semantic Actor;
- current Account access != historical Person/Actor attribution;
- provider/auth/contact identifiers are reconciliation/access evidence, not canonical Person identity by default;
- User is not a kernel domain primitive;
- Principal remains a distinct deferred security/Authority concept;
- AI/software may be Actors where agency is materially relevant without becoming Person or Authority;
- no universal `actors` table/root or `Person.id = Account.id` is pre-approved.

## Asset invariants accepted — current scoped baseline

- Asset is native persistent identity, not a contextual role;
- current scope is an individually tracked non-human physical object whose identity/history materially matter;
- physical thing != Asset automatically;
- managed thing != Asset automatically;
- Person != Asset;
- Asset may play Subject or Resource roles without becoming either;
- ownership, possession, custody, stewardship, location and state do not define Asset identity;
- provider/serial/VIN/MAC/barcode identifiers are reconciliation evidence, not canonical identity by default;
- fungible stock does not require one Asset per unit;
- living things, Documents, FinancialAccounts and services are not absorbed by default;
- no universal Asset status/history wrapper/table hierarchy is pre-approved;
- the Asset scope must be re-tested terminology-neutrally before final Cluster-4 closure.

## Resource invariants accepted

- Resource is contextual planning/execution role/capability, not independent identity/root;
- native Person/Asset/Place/service/supply semantics remain authoritative;
- Person and Asset may play Resource role without identity collapse;
- Resource != Subject/Actor;
- Resource != Requirement/candidate set/Allocation/Reservation/actual use;
- Resource != Responsibility/Performer/Participant;
- schedulable Resource means a Resource-role case whose time-dependent Availability/Capacity matters;
- Requirement may remain abstract until later candidate selection/allocation;
- allocated/reserved Resource != proof of actual use;
- consumable supply may satisfy Resource semantics without per-unit identity;
- Resource role grants no ownership, consent, Responsibility, Authority or Visibility;
- no universal `resources` table/root or generic `resource_id` shortcut is pre-approved.

---

# Active cluster — Data / Subjects

**Status:** CANDIDATE REVIEWS COMPLETE — Cluster Integration Gate is next. This is not yet a cluster PASS.

Accepted in this cluster:

1. [`Quantity v0`](concepts/quantity.md) — [`validation`](checkpoints/quantity-v0-validation.md) — **PASS WITH HARDENING**.
2. [`Subject v0`](concepts/subject.md) — [`validation`](checkpoints/subject-v0-validation.md) — **PASS WITH HARDENING; canonical semantic role, no Subject entity/root**.
3. [`Person v0`](concepts/person.md) — [`Person / Actor / Account validation`](checkpoints/person-actor-account-v0-validation.md) — **PASS WITH HARDENING; canonical native human entity**.
4. [`Actor v0`](concepts/actor.md) — [`Person / Actor / Account validation`](checkpoints/person-actor-account-v0-validation.md) — **PASS WITH HARDENING; canonical agency role/capability, no Actor entity/root**.
5. [`Asset v0`](concepts/asset.md) — [`validation`](checkpoints/asset-v0-validation.md) — **PASS WITH HARDENING; current scoped native physical-object entity; mandatory terminology-neutral re-review**.
6. [`Resource v0`](concepts/resource.md) — [`validation`](checkpoints/resource-v0-validation.md) — **PASS WITH HARDENING; canonical planning/execution role/capability, no Resource entity/root**.

Accepted conceptual boundary, detailed model deferred:

- `Account != Person != Actor`; Account is platform/access identity. Exact credential/provider/Principal/security modeling is deferred.

Rejected candidate with validated product need:

- [`Register Candidate v0`](checkpoints/register-v0-validation.md) — **KERNEL CANDIDATE REJECTED; longitudinal product/query capability retained**.

No remaining planned concept candidate is waiting for first-pass review in Cluster 4. The next step is integration, not another primitive by default.

## Quantity current baseline

```text
Quantity
= reusable scalar amount value semantics
= magnitude + unit semantics sufficient for interpretation
!= independent entity / Observation / universal numeric wrapper
```

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
- valid aggregation follows source metric/record semantics;
- quick capture creates the native semantic record;
- saved tracker/view configuration may exist as product/application configuration without becoming independent domain truth;
- `Transaction`, `Movement`, `Snapshot`, or other future native record types are **not pre-approved** merely because historical Register examples mentioned them.

## Subject current baseline

```text
native referent
Person / Asset / future Location / other eligible concept
        ↑
     Subject role
        │
descriptive record / Observation
```

Resolved:

```text
Subject entity/root rejected
Subject vs observer/recorder/source/transformer separated
Subject vs Person separated
Subject vs Actor separated
Subject vs Account separated at conceptual level
Subject vs Asset separated at current Asset v0 baseline
Subject vs Resource separated
```

Remaining retest owners:

```text
Subject vs Principal/Authority/Visibility -> Relationships / Reasoning
Subject vs focus/context        -> Relationships / Reasoning
Person/Asset identity reconciliation -> logical model + Provenance/Version/Decision
heterogeneous reference mechanics -> logical data model
```

## Person / Actor / Account current baseline

```text
PERSON
CANONICAL NATIVE ENTITY

ACTOR
CANONICAL SEMANTIC AGENCY ROLE / CAPABILITY
NOT ENTITY / ROOT

ACCOUNT
REAL PLATFORM / ACCESS IDENTITY BOUNDARY
DETAILED AUTH MODEL DEFERRED

USER
PRODUCT / IMPLEMENTATION TERM ONLY
NO DOMAIN PRIMITIVE

PRINCIPAL
SAFE DEFERRED
AUTHORITY / SECURITY MODEL
```

Representative shape:

```text
Person Maria
    ↑ Subject role
Observation 38.2 °C
    ↑ observed/recorded by
Person Anna
    ↓ Actor semantics through specific roles
Account Anna-A1
    ↓ authentication context
future Principal/Authority semantics
```

No layer is allowed to launder the semantics of another.

## Asset current baseline

```text
ASSET
CANONICAL NATIVE ENTITY — CURRENT SCOPED BASELINE

scope:
individually tracked
non-human physical object
identity/history materially matter
```

Representative shape:

```text
Asset A17
Sony A7 IV
        ↑ Subject role
Observation: shutter count = 32,411

Activity: photo shoot
Resource Requirement: suitable camera
Candidate / allocated Resource role: Asset A17
```

Current exclusions are deliberate, not permanent ontology claims:

```text
Person
living subject by default
Document / Artifact
FinancialAccount
service/subscription
financial-asset semantics
fungible stock unit by default
```

Identity guardrails:

```text
Asset != owner
Asset != holder
Asset != steward
Asset != Resource
Asset != Subject
Asset != model/catalog definition
provider identifier != canonical Asset identity automatically
```

### Mandatory Asset re-review

During the dedicated post-Cluster-4 dependency closure, perform a terminology-neutral comparison of how mature products represent **managed/tracked referents**, focusing on what they persist and relate rather than what they call it.

Required benchmark families include at least:

- personal possessions / personal information managers;
- equipment / IT asset / inventory;
- smart home / devices;
- property / place;
- document / credential management;
- finance / accounts;
- pet/plant/living tracking;
- services/subscriptions.

Reopen Asset if a broader or different identity abstraction explains LifeOS workflows with fewer arbitrary exclusions and no semantic loss.

## Resource current baseline

```text
RESOURCE
CANONICAL SEMANTIC PLANNING / EXECUTION ROLE-CAPABILITY
NOT ENTITY / ROOT
```

Representative planning flow:

```text
Requirement
what is needed
        ↓
Candidate Resource-role providers
what could satisfy it
        ↓
Allocation / selection
what is chosen
        ↓
Reservation / Capacity Claim
what capacity is held
        ↓
Actual use / consumption
what really happened
```

Guardrails:

```text
Resource != Person / Asset / Subject / Actor
Person may play Resource role
Asset may play Resource role
Resource != Requirement
Resource != candidate set
Resource != Allocation
Resource != Reservation
Resource != Actual use
Resource != Responsibility / Performer / Participant
```

Availability/Capacity now composes with Resource explicitly:

```text
native referent / supply
        ↓ Resource role
schedulable subset
        ↓
Availability + Capacity
        ↓
Reservation / Claim
```

The exact Requirement/Allocation/Reservation/pool/supply representation remains SAFE DEFERRED; no universal `resources` root/table is pre-approved.

## Mandatory inherited re-tests now resolved by first-pass Cluster-4 concepts

```text
Observation vs Quantity — RESOLVED
Observation vs Register/RegisterEntry — RESOLVED
Quantity vs Register aggregation — RESOLVED at kernel level
Subject entity vs semantic role — RESOLVED
Subject vs observer/recorder/source/transformer — RESOLVED
Subject vs Person — RESOLVED
Subject vs Actor — RESOLVED
Subject vs Account — RESOLVED at conceptual level
Person vs Actor — RESOLVED
Person vs Account — RESOLVED at conceptual level
Actor vs Account — RESOLVED at conceptual level
User universal kernel identity — REJECTED
Subject vs Asset — RESOLVED at current Asset v0 baseline
Person vs Asset — RESOLVED at current baseline
Asset vs fungible stock — RESOLVED conceptually
Asset vs Resource — RESOLVED at current baseline
Subject vs Resource — RESOLVED
Person vs Resource — RESOLVED
Actor vs Resource — RESOLVED
Availability/Capacity vs Resource — RESOLVED
Resource universal entity/root — REJECTED
```

These resolutions remain subject to cluster integration and the mandatory Asset re-review where specifically noted.

## Next step — Data / Subjects Cluster Integration Gate

Do not invent another candidate merely because the roadmap looks short.

The next review must stress the accepted/rejected Cluster-4 results together:

```text
Quantity
Register rejection / longitudinal capability
Subject
Person
Actor
Account boundary
Asset
Resource
```

Required pressure includes:

- representative workflow reconstruction;
- deep chronology;
- remove/merge/split reductio;
- top-down traceability;
- bottom-up reconstruction;
- lateral propagation;
- history/correction/reconciliation;
- multi-actor identity/authority/privacy;
- simple-user regression;
- scale/performance pressure;
- specialist-system boundary;
- AI proposal/authority boundaries;
- Resource Requirement / allocation / reservation pressure without prematurely modeling them;
- Asset terminology-neutral scope pressure as a registered dependency, not hidden assumption.

The cluster integration result is provisional for transition purposes until the dedicated dependency closure and Cross-Cluster v4 pass.

---

# Mandatory closure after Data / Subjects

The required transition is now:

```text
Data / Subjects cluster integration
        ↓
Data / Subjects multi-actor stress
        ↓
provisional cluster verdict
        ↓
Deferred Dependency Closure — clusters 1–4
  includes mandatory Asset terminology-neutral re-review
        ↓
RESOLVED / SAFE DEFERRED / REOPEN for every material open boundary
        ↓
Cross-Cluster Validation v4 — clusters 1–4
        ↓
only after PASS: Relationships / Reasoning
```

Cluster 4 is not treated as definitively consolidated before dependency cleanup and Cross-Cluster v4.

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
- Resource Requirement / Allocation / substitution where justified;
- Authority / Visibility;
- Decision;
- Version;
- AI Proposal;
- Principal / delegation / on-behalf-of where those semantics are primarily security/authority rather than human identity.

Strong evidence indicates typed/directional semantics will likely be necessary; one universal semantic-free `related_to` is insufficient.

Mandatory inherited re-tests include:

- Evidence as semantic role vs typed Relationship representation;
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
- historical Person/Actor/Asset/resource-allocation attribution after Account or relationship changes.

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
- Subject is a canonical role over native identity, not an `Asset/Soggetto` universal wrapper/root;
- Person is canonical native human identity independent of Account;
- Actor is canonical contextual agency semantics, not a universal entity/root;
- Account is conceptually separate platform/access identity; detailed auth/security modeling is deferred;
- User remains product/implementation language, not a domain root;
- historical `Asset/Soggetto` broad grouping is superseded;
- Asset v0 currently means individually tracked non-human physical-object identity, not every managed thing, and remains explicitly reopenable after terminology-neutral review;
- Resource is canonical contextual planning/execution role/capability, not a universal Resource entity/root;
- Resource Requirement, allocation, reservation and actual use remain distinct semantics;
- Milestone attainment is evaluation-backed checkpoint state rather than duplicate reality storage;
- older V1 `confirmation state` labels such as imported/inferred/automatic/corrected are redistributed into Provenance, automation/inference, Version and workflow semantics.

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
```

Accepted boundary but not yet a fully modeled concept:

```text
Account != Person != Actor
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
Resource     -> what native provider/supply may satisfy an execution need in context
Availability -> when schedulable Resource capacity may be used
Capacity     -> compatible commitments a schedulable Resource can sustain
Schedule     -> current accepted temporal assignment
Session      -> bounded actual execution episode
Actual       -> realization of a specific expectation
Outcome      -> result/disposition of realization
Observation  -> measurement/simple assertion about Subject/context
Confirmation -> contextual affirmation of target/version/purpose
Evidence     -> contextual evaluative use of information
Provenance   -> bounded origin/evolution lineage
Quantity     -> reusable scalar amount value semantics
Subject      -> contextual aboutness role over native referent identity
Person       -> persistent native human identity
Actor        -> contextual agency role/capability over native identity
Account      -> platform/access identity boundary, detailed model deferred
Asset        -> current scoped individually tracked non-human physical-object identity
```

Cross-cutting multi-actor direction:

```text
shared canonical fact / native object identity
+
actor-scoped personal state

native identity
!= account
!= participation
!= responsibility
!= performer
!= Subject role
!= Actor role
!= ownership
!= Resource role
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
Subject v0                      — ACCEPTED SEMANTIC ROLE
Subject universal entity/root   — REJECTED
Person v0                       — ACCEPTED NATIVE ENTITY
Actor v0                        — ACCEPTED SEMANTIC AGENCY ROLE
Actor universal entity/root     — REJECTED
Account boundary                — ACCEPTED / DETAILED MODEL DEFERRED
User universal domain root      — REJECTED
Asset v0                        — ACCEPTED CURRENT SCOPED NATIVE ENTITY
Asset broad managed-object root — REJECTED
Resource v0                     — ACCEPTED SEMANTIC PLANNING/EXECUTION ROLE
Resource universal entity/root  — REJECTED

↓ NOW
Data / Subjects cluster integration + multi-actor stress
↓
provisional Cluster-4 verdict
↓
Deferred Dependency Closure — clusters 1–4
  + mandatory terminology-neutral Asset re-review
↓
Cross-Cluster Validation v4 — clusters 1–4
↓ only after PASS
Relationships / Reasoning
```

---

# Reopen / deferred-dependency watchlist

The following are executable obligations, not generic reminders. The post-Cluster-4 dependency closure must classify every still-material item as `RESOLVED`, `SAFE DEFERRED`, or `REOPEN` and give SAFE DEFERRED items an explicit owner/reopening trigger.

Known inherited/current items include:

- Asset scope vs terminology-neutral managed/tracked-referent model — **mandatory revisit**;
- Asset vs Place/Location/Property;
- Asset vs living-entity identity;
- Asset vs Document/Artifact/FinancialAccount/service;
- Asset model/type/profile semantics;
- Asset ownership/stewardship/possession/Authority semantics;
- Asset identity reconciliation/merge/split;
- Resource Requirement / candidate / Allocation semantics;
- Resource Reservation/Claim physical and relationship representation;
- planned Resource vs actual use/consumption;
- Resource pool / consumable supply / inventory semantics;
- Resource vs Place/service/capability/skill future native concepts;
- Resource allocation Authority / Visibility;
- Principal/security identity and Account credential/provider mechanics;
- delegated/on-behalf-of Actor semantics;
- Person reconciliation/merge/split and identity-history persistence;
- Subject vs focus/context/typed Relationship;
- Subject/Person/Actor/Asset/Resource association privacy vs Visibility;
- heterogeneous Subject/Actor/Resource-reference persistence;
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

Resolved and removed from limbo at the current first-pass baseline:

- Observation vs Register/RegisterEntry;
- Register as a kernel primitive;
- universal RegisterEntry;
- Quantity vs generic Register aggregation at kernel level;
- Subject entity vs semantic role;
- Subject vs observer/recorder/source/transformer;
- Subject vs Person;
- Subject vs Actor;
- Subject vs Account at conceptual level;
- Person vs Actor;
- Person vs Account at conceptual level;
- Actor vs Account at conceptual level;
- User as universal kernel identity;
- Subject vs Asset at current Asset v0 baseline;
- Person vs Asset at current baseline;
- Asset vs fungible stock at conceptual level;
- Asset identity vs ownership at conceptual level;
- Asset vs Resource at current baseline;
- Subject vs Resource;
- Person vs Resource;
- Actor vs Resource;
- Availability/Capacity vs Resource;
- universal Resource entity/root.

The Asset terminology-neutral re-review can reopen current Asset-related resolved items if it materially changes Asset scope. Cluster integration may likewise expose new contradictions and must be allowed to reopen any first-pass concept.

---

# Final validation rule

A final whole-domain stress test remains mandatory before broad persistence implementation.

Cluster PASS and Cross-Cluster v4 do not prevent later reopening when another cluster, physical data model, integration, implementation evidence, safety requirement or stronger real-world evidence exposes a genuine contradiction.