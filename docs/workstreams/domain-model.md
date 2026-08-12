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

Earlier product terminology is evidence, not automatic truth. Candidates are revalidated through real-world workflows, mature-product/standard benchmarks, adversarial reduction, history/correction tests, explicit multi-actor stress and cross-concept consistency.

**Accepted means current best decision, not immutable decision.**

A roadmap concept is a candidate to validate, not an object that must survive. Rejection is correct when the capability can be preserved more cleanly without an additional kernel primitive.

Asset v0 is accepted only as the current scoped baseline and carries a **mandatory terminology-neutral re-review before final Cluster-4 closure** because the term itself may bias the abstraction toward asset-management conventions.

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
12. [`../domain/checkpoints/multi-actor-evidence-synthesis-v0.md`](../domain/checkpoints/multi-actor-evidence-synthesis-v0.md)
13. [`../domain/concepts/actual.md`](../domain/concepts/actual.md)
14. [`../domain/concepts/outcome.md`](../domain/concepts/outcome.md)
15. [`../domain/concepts/observation.md`](../domain/concepts/observation.md)
16. [`../domain/concepts/confirmation.md`](../domain/concepts/confirmation.md)
17. [`../domain/concepts/evidence.md`](../domain/concepts/evidence.md)
18. [`../domain/concepts/provenance.md`](../domain/concepts/provenance.md)
19. [`../domain/concepts/quantity.md`](../domain/concepts/quantity.md)
20. [`../domain/checkpoints/quantity-v0-validation.md`](../domain/checkpoints/quantity-v0-validation.md)
21. [`../domain/checkpoints/register-v0-validation.md`](../domain/checkpoints/register-v0-validation.md)
22. [`../domain/concepts/subject.md`](../domain/concepts/subject.md)
23. [`../domain/checkpoints/subject-v0-validation.md`](../domain/checkpoints/subject-v0-validation.md)
24. [`../domain/concepts/person.md`](../domain/concepts/person.md)
25. [`../domain/concepts/actor.md`](../domain/concepts/actor.md)
26. [`../domain/checkpoints/person-actor-account-v0-validation.md`](../domain/checkpoints/person-actor-account-v0-validation.md)
27. [`../domain/concepts/asset.md`](../domain/concepts/asset.md)
28. [`../domain/checkpoints/asset-v0-validation.md`](../domain/checkpoints/asset-v0-validation.md)
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
- Benchmark **behavior, identity, lifecycle, relationships and failure modes**, not merely vocabulary; competitor terminology is not ontology.
- Record test IDs, evidence, result, hardening/dependency and justified `N/A`.
- Allowed concept/cluster verdicts: `PASS`, `PASS WITH HARDENING`, `REOPEN`, `DEFERRED DEPENDENCY`.
- Dependency closure classes are `RESOLVED`, `SAFE DEFERRED`, `REOPEN`; they are not additional concept verdicts.
- Candidate rejection is valid when no distinct identity/lifecycle/authority/invariant/query behavior justifies the primitive.
- Preserve useful product capability even when a historical kernel candidate is rejected.
- Preserve planned/current/actual/history distinctions.
- Preserve source/provenance/confirmation/evidence/authority distinctions.
- Preserve Person / Actor / Account / Principal distinctions; do not build the domain around `users.id`.
- Preserve Asset / Subject / Resource / ownership distinctions; do not make `Asset` a universal managed-object root.
- Do not fabricate historical intention or earlier knowledge from later relevance/resolution.
- Do not create one table/entity per life topic.
- Do not collapse semantics into arbitrary JSON or one universal graph/reality/fact/subject/actor/asset object.
- Do not let AI inference become confirmed/canonical truth, Person identity, Subject attribution, Asset identity/ownership or Authority automatically.
- Preserve progressive disclosure.
- Run the dedicated Multi-Actor Compatibility Gate after the Core Semantic Gate.
- New primitives require materially distinct identity/lifecycle/authority/invariants/query behavior.
- Run Cluster Integration + Cluster Multi-Actor Stress before declaring a cluster complete.
- Do not leave material neighboring questions as generic `TBD`/`review later`; every applicable closure point must classify them.
- A `SAFE DEFERRED` item must identify why it is non-blocking, its owner/future stage, exact reopening trigger and tests to rerun.
- Re-run prior clusters together when a new cluster resolves old deferred boundaries.
- Finish Data / Subjects, then perform the dedicated clusters 1–4 deferred-dependency closure and Cross-Cluster Validation v4 before Relationships / Reasoning.
- Before final Data / Subjects closure, execute the terminology-neutral Asset managed-referent review recorded in `asset-v0-validation.md`.
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
Subject v0                      PASS WITH HARDENING / ACCEPTED SEMANTIC ROLE
Person v0                       PASS WITH HARDENING / ACCEPTED NATIVE ENTITY
Actor v0                        PASS WITH HARDENING / ACCEPTED AGENCY ROLE
Asset v0                        PASS WITH HARDENING / ACCEPTED CURRENT SCOPED NATIVE ENTITY
Account boundary                ACCEPTED / DETAILED MODEL DEFERRED
User universal domain root      REJECTED
Register kernel candidate       REJECTED
Universal RegisterEntry         REJECTED
Universal Subject entity/root   REJECTED
Universal Actor entity/root     REJECTED
Universal managed-object Asset  REJECTED
```

First-three-cluster regression result remains:

```text
18 accepted concepts retained before Cluster 4
0 structural reopenings
0 concept removals
0 justified concept merges
0 mandatory new primitives
```

The two existing cross-cluster hardenings remain:

1. reported/asserted reality != established Actual;
2. Milestone attainment is Evidence/evaluation-backed and must not duplicate underlying reality.

Cluster-4-specific mandatory revisit now added:

3. Asset scope must be re-tested terminology-neutrally before final Cluster-4 closure.

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
shared canonical fact / native object identity
+
actor-scoped personal state
```

is preferred over per-user semantic duplication.

Current non-collapse rules include:

```text
native referent/object identity
!= Account
!= Participant
!= Responsibility
!= Performer
!= Subject role
!= Actor role
!= Resource role
!= ownership/possession/stewardship
!= Authority
!= Visibility
```

Identity/agency/object boundary:

```text
Person
= native human identity

Subject
= contextual aboutness role

Actor
= contextual agency role/capability

Account
= platform/access identity

Asset
= current scoped individually tracked non-human physical-object identity

Resource
= next review; entity vs role not pre-decided

Principal
= deferred security/authorization identity
```

No universal Actor/User/Subject/managed-object root, Team/Organization/ACL/Stewardship primitive, or `persons.id = accounts.id` schema is pre-approved.

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
Subject        -> canonical contextual aboutness role; not entity
Person         -> canonical native human identity
Actor          -> canonical contextual agency semantics; not entity
Asset          -> current scoped native physical-object identity; terminology-neutral re-review mandatory
Account        -> platform/access identity boundary; detailed security model deferred
User           -> product/implementation term only
Register       -> possible product/UI label for longitudinal capability, not kernel primitive
Tracker/History/Progress -> product/query views over native records
```

Product labels such as `Car`, `Camera`, `Gear`, `Device`, `Equipment` or `Inventory` do not automatically create or broaden kernel types.

---

# Closed cluster — Observed Reality & Evidence

**Status:** PASS — current validated cluster baseline.

## Actual v0

```text
Actual = how a specific intention/expectation was established as realized
Actual != Session / Outcome / Observation / Confirmation / Evidence / Provenance
reported/asserted reality != established Actual
```

## Outcome v0

```text
Outcome = contextual result/disposition of an Actual realization
```

## Observation v0

> A persistent contextual record of a measured, perceived, reported, or explicitly derived property, state, value, rating, or simple assertion about a Subject referent at an effective time or context.

Observation composes with native identity/roles without owning them:

```text
Person Maria     = native human identity
Subject role     = Observation is about Maria
Person Anna      = native recorder identity
Actor semantics  = Anna acts as recorder
Account Anna-A1  = authentication/access context

Asset A17        = native physical-object identity
Subject role     = Observation is about A17
```

None of those layers replaces the others.

## Confirmation v0

> A persistent contextual attestation that a specific confirmer affirms a specific version of a confirmable target as sufficiently accepted for a defined purpose at that time.

## Evidence v0

> Evidence is the contextual evaluative role played by information when that information materially bears on a specific claim, criterion, checkpoint, decision or other evaluation target.

## Provenance v0

> Provenance is bounded contextual lineage describing how a specific domain record/material version came to exist or change, including materially relevant source entities, activities, native actors/systems/providers and times.

Provenance preserves native identity and role separation and does not treat authentication/provider identifiers as Person/Actor/Asset identity, truth or Authority.

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
Quantity         ACCEPTED — canonical value semantics
Register         REJECTED as kernel primitive
RegisterEntry    REJECTED as universal semantic record
Subject          ACCEPTED — canonical semantic role; entity/root rejected
Person           ACCEPTED — canonical native human entity
Actor            ACCEPTED — canonical agency role/capability; entity/root rejected
Account boundary ACCEPTED — platform/access identity; detailed auth model deferred
User root        REJECTED — product/implementation term only
Asset            ACCEPTED — current scoped native entity; mandatory terminology-neutral revisit
Resource         ACTIVE NEXT REVIEW
```

No pending concept is guaranteed to survive.

## Quantity v0

> Reusable scalar amount value semantics: magnitude + unit semantics sufficient for interpretation.

Critical boundaries:

```text
Quantity != entity
number != Quantity by default
Quantity != Observation
property / quantity kind != unit
compatible unit != semantic equivalence by itself
same unit != universal aggregation permission
Quantity != Range / Threshold / comparator / criterion
```

Checkpoint: [`Quantity v0 Validation`](../domain/checkpoints/quantity-v0-validation.md) — **PASS WITH HARDENING**.

## Register candidate

Historical `Register + RegisterEntry` kernel structure is rejected. Longitudinal product behavior remains:

```text
native semantic records
↓
query / filtering / grouping
↓
valid aggregation / trend / comparison
↓
Register / Tracker / History / Progress UI
```

Checkpoint: [`Register Candidate v0 Validation`](../domain/checkpoints/register-v0-validation.md).

## Subject v0

> Contextual semantic role played by the native referent a descriptive record primarily concerns.

```text
Subject entity/root = rejected
Subject != Person / Actor / Account / Principal / Asset / Resource
Subject != observer / recorder / source / transformer / Authority / Visibility
```

Asset v0 may play Subject role while retaining its own identity.

Checkpoint: [`Subject v0 Validation`](../domain/checkpoints/subject-v0-validation.md).

## Person / Actor / Account v0 boundary

Accepted baseline:

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

Key guardrails:

- a Person may exist before, without, or after LifeOS Account access;
- Person identity is not name/email/phone/provider/account identity;
- Person may play Subject and Actor/specific action roles without identity change;
- Actor is agency semantics, not a wrapper identity and not a replacement for performer/recorder/observer/confirmer/proposer roles;
- Actor != Responsibility/Authority/ownership;
- Account authentication context != semantic Actor or Person identity;
- current Account access != historical Person/Actor attribution;
- external/non-account people and material software/AI actors are ordinary supported reality;
- AI/service agency does not launder human authorship, Confirmation, Authority or responsibility;
- Person merge/split/reconciliation must preserve material identity history;
- no universal `actors` table/root, `User` root, synthetic Account requirement, or `Person.id = Account.id` is pre-approved.

Files:

- [`Person v0`](../domain/concepts/person.md)
- [`Actor v0`](../domain/concepts/actor.md)
- [`Person / Actor / Account v0 Validation`](../domain/checkpoints/person-actor-account-v0-validation.md)

## Asset v0 — current scoped baseline

> An Asset is a persistent native representation of an individually tracked non-human physical object whose distinct identity and management history materially matter within LifeOS.

Current rules:

```text
Asset != Person
Asset != Subject
Asset != Resource
Asset != owner/holder/custodian/steward
Asset instance != product/model definition
physical thing != Asset automatically
managed thing != Asset automatically
financial asset semantics != Asset entity
```

Representative workflows:

```text
Asset A17 = specific camera body
Observation = shutter count
future Resource role = used for photo shoot
owner / holder / maintenance responsible = separate relationships
```

```text
Asset L1 = company laptop
owner = Company
holder = Person Mattia
maintenance responsibility = IT
```

Current exclusions by default:

- Person;
- living entities such as pet/plant;
- Document/Artifact;
- FinancialAccount;
- services/subscriptions;
- financial-asset/liability meaning;
- fungible stock units when individual identity does not matter.

Those exclusions are not final claims that those referents need separate primitives; they prevent Asset from becoming a generic dumping ground before evidence exists.

### Mandatory terminology-neutral Asset re-review

Before final Cluster-4 closure, compare how mature products model managed/tracked referents across:

- personal possessions/PIM;
- inventory/equipment/IT assets;
- smart-home/device systems;
- property/place management;
- documents/credentials;
- finance/accounts;
- pet/plant/living tracking;
- services/subscriptions.

The comparison must ask:

```text
what has native identity?
what lifecycle survives?
what is only a role?
what is a profile/category?
what is separately owned/located/held?
what is fungible vs individually tracked?
what relationships are first-class?
what is derived UI rather than source truth?
```

Do **not** start from whether another product calls the thing `Asset`, `Device`, `Item`, `Account`, `Object`, or something else.

Reopen Asset if a broader/different abstraction explains LifeOS workflows with fewer exceptions and no semantic loss.

Files:

- [`Asset v0`](../domain/concepts/asset.md)
- [`Asset v0 Validation`](../domain/checkpoints/asset-v0-validation.md)

## ACTIVE NEXT REVIEW — Resource

Resource must be tested against accepted Availability & Capacity plus the new Person/Asset identity boundaries.

Do not begin from a universal `resources` table or assume Resource is an entity.

Primary questions:

```text
Is Resource a native entity or contextual role/capability?
Can Person play Resource role without identity change?
Can Asset play Resource role without identity change?
Can room/place/service/capacity pool be Resource?
Does Resource exist independently from being needed/used/scheduled?
Resource vs Subject
Resource vs Actor
Resource vs Asset
Resource vs Availability
Resource vs Capacity
Resource vs Reservation/Claim
reusable Resource vs consumable input
capacity-bearing Resource vs simple dependency/input
exclusive vs shareable/parallel capacity
resource group/pool vs native referent
is a generic Resource concept semantic or merely a common FK?
```

Mandatory scenarios:

- Person scheduled for meeting/work;
- camera Asset required for photo shoot;
- room required for event;
- external car/equipment not owned by current user;
- software/service/API quota;
- consumable material;
- two simultaneous commitments compatible for same Resource;
- Asset unavailable/broken but identity remains;
- Resource requirement satisfied by one of several alternatives;
- shared Resource whose capacity/availability differs from visibility/ownership.

Mandatory reductio:

> If Resource is only a contextual role played by native referents when capacity/access/use matters, reject a universal Resource entity/root even if scheduling products commonly expose one.

Resource is the final planned Cluster-4 candidate before integration.

## Mandatory inherited re-tests

```text
Observation vs Quantity — RESOLVED
Observation vs Register/RegisterEntry — RESOLVED
Quantity vs Register aggregation — RESOLVED at kernel level
Subject entity vs semantic role — RESOLVED
Subject vs observer/recorder/source/transformer — RESOLVED
Subject vs Person — RESOLVED
Subject vs Actor — RESOLVED
Subject vs Account — RESOLVED at conceptual level
Subject vs Asset — RESOLVED at current Asset v0 baseline
Person vs Actor — RESOLVED
Person vs Account — RESOLVED at conceptual level
Actor vs Account — RESOLVED at conceptual level
Person vs Asset — RESOLVED at current baseline
Asset vs fungible stock — RESOLVED conceptually
Asset identity vs ownership — RESOLVED at conceptual level
User universal kernel identity — REJECTED
Principal/security identity — SAFE DEFERRED
Person/Asset merge/split/reconciliation — SAFE DEFERRED
Asset scope vs terminology-neutral managed-referent model — SAFE DEFERRED / MANDATORY REVISIT
Subject vs Resource — ACTIVE NEXT
Asset vs Resource — ACTIVE NEXT
Availability/Capacity vs Resource — ACTIVE NEXT
sampled-series physical representation — SAFE implementation dependency
```

The Resource review is read-only until Methodology v3 passes and a separately stated Git write scope is explicitly approved.

---

# TRANSITION GATE — after Data / Subjects

Before Relationships / Reasoning begins, execute:

```text
Resource review
        ↓
Data / Subjects cluster integration
        ↓
Data / Subjects multi-actor stress
        ↓
provisional cluster verdict
        ↓
MANDATORY terminology-neutral Asset re-review
        ↓
DEFERRED DEPENDENCY CLOSURE — clusters 1–4
        ↓
RESOLVED / SAFE DEFERRED / REOPEN for every material open boundary
        ↓
Cross-Cluster Validation v4 — clusters 1–4
        ↓ only after PASS
Relationships / Reasoning
```

The dependency closure must revisit inherited issues from the first three clusters as well as Cluster-4 findings. Nothing material may remain as unowned limbo.

Cluster 4 must not be called definitively closed before the Asset scope re-review and deferred-dependency cleanup.

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
- AI Proposal;
- Principal / delegation / on-behalf-of security/authority semantics.

Mandatory inherited re-tests include:

- Evidence vs typed Relationship semantics;
- Milestone attainment vs Evidence/GoalCriterion/Decision;
- Provenance vs Version / Decision / Audit;
- Confirmation vs Authority / Acknowledgement / Acceptance;
- competing assertions and canonical decision/reconciliation policy;
- collaborative Session/Actual attribution;
- Subject vs focus/context/Visibility;
- Person/Actor specific roles vs Participation/Responsibility/Stewardship;
- Account/Principal/Authority/delegation boundaries;
- Asset ownership/possession/custody/stewardship/location/Visibility;
- historical Person/Actor/Asset attribution after Account/relationship changes.

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
        └─ Observation(s)
             ├─ may use Quantity value semantics
             └─ references native referent playing Subject role

Person
= native human identity
  ├─ may play Subject role
  ├─ may play Actor/specific action roles
  └─ may potentially play Resource role

Asset
= current scoped native physical-object identity
  ├─ may play Subject role
  └─ may potentially play Resource role

Actor
= agency semantics over native identity

Account
= platform/access identity context; not Person/Actor

Resource
= NEXT — entity vs role/capability unresolved

Confirmation
= contextual affirmation of specific target/version/purpose

Evidence
= contextual evaluative use of existing information

Provenance
= bounded lineage preserving native identity + specific Actor/source roles

Longitudinal product views
= queries/projections over native records, not a separate truth layer
```

This is not a mandatory parent/child chain and not a persistence schema.

---

# Reopen / deferred-dependency watchlist

The post-Cluster-4 closure pass must turn every still-material item into `RESOLVED`, `SAFE DEFERRED`, or `REOPEN`.

Active/current items:

- Subject vs Resource;
- Asset vs Resource;
- Availability/Capacity vs Resource;
- Person as Resource role vs Person identity;
- Asset scope vs terminology-neutral managed/tracked-referent model — **MANDATORY REVISIT**;
- Asset vs Place/Location/Property;
- Asset vs living-entity identity;
- Asset vs Document/Artifact/FinancialAccount/service;
- Asset model/type/profile semantics;
- Asset ownership/stewardship/possession/Authority semantics;
- Asset identity reconciliation/merge/split;
- Principal/security identity and Account credential/provider mechanics;
- delegated/on-behalf-of Actor semantics;
- Person reconciliation/merge/split and identity-history persistence;
- Subject vs focus/context/typed Relationship;
- Subject/Person/Actor/Asset association privacy vs Visibility;
- heterogeneous Subject/Actor/Asset/Resource-reference persistence;
- Actual establishment under Authority/Decision/reconciliation semantics;
- Confirmation vs Authority/Acknowledgement/Acceptance/Version;
- Evidence vs GoalCriterion/Relationship/Decision/Version;
- Milestone attainment vs Evidence/GoalCriterion/Decision;
- Provenance vs Version/Decision/Audit/Authority;
- provenance retention/privacy/deletion;
- contextual competing assertions under Authority rules;
- collaborative Session vs actor-scoped Actual participation;
- Responsibility vs Assignment vs Hand-off vs Stewardship;
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

Resolved at current baseline:

- Observation vs Register/RegisterEntry;
- Register as kernel primitive;
- universal RegisterEntry;
- Quantity vs generic Register aggregation at kernel level;
- Subject entity vs semantic role;
- Subject vs observer/recorder/source/transformer;
- Subject vs Person;
- Subject vs Actor;
- Subject vs Account at conceptual level;
- Subject vs Asset at current Asset v0 baseline;
- Person vs Actor;
- Person vs Account at conceptual level;
- Actor vs Account at conceptual level;
- Person vs Asset at current baseline;
- Asset vs fungible stock at conceptual level;
- Asset identity vs ownership at conceptual level;
- User as universal kernel identity.

The mandatory Asset scope re-review may reopen Asset-related resolved items if the current physical/durable boundary proves terminology-driven.

These are executable obligations, not generic `later` notes.

---

# Before broad persistence/backend implementation

The full Domain Atlas must eventually establish:

- conceptual model;
- entity/value-object/semantic-role/relationship boundaries;
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
  Subject v0 accepted as semantic role
  Person v0 accepted
  Actor v0 accepted as agency role
  Account boundary accepted / detailed model deferred
  Asset v0 accepted as current scoped native entity
  Asset terminology-neutral re-review mandatory before final cluster closure
  Resource read-only review now
↓
Data / Subjects cluster integration + multi-actor stress
↓
Asset terminology-neutral re-review + Deferred Dependency Closure — clusters 1–4
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

Continue from Methodology v3 + Execution Template v3 + Language Map + accepted Quantity/Subject/Person/Actor/Asset baselines + Register rejection checkpoint + Person/Actor/Account checkpoint + Asset checkpoint + the three validated cluster checkpoints.

The active next candidate is **Resource in read-only mode**. The current Asset scope is not to be treated as final until the mandatory terminology-neutral managed/tracked-referent review is executed during Cluster-4 closure. Do not create a parallel validation standard, terminology tree, universal actor/user/subject/asset root or collaboration ontology.