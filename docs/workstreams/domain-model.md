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

Asset v0 is accepted only as the current scoped baseline and carries a **mandatory terminology-neutral re-review before final Cluster-4 consolidation** because the term itself may bias the abstraction toward asset-management conventions.

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
29. [`../domain/concepts/resource.md`](../domain/concepts/resource.md)
30. [`../domain/checkpoints/resource-v0-validation.md`](../domain/checkpoints/resource-v0-validation.md)
31. [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md)
32. [`../product/multi-actor-collaboration-discovery-simulation-2026-08.md`](../product/multi-actor-collaboration-discovery-simulation-2026-08.md)
33. [`../product/multi-actor-collaboration-research-2026-08.md`](../product/multi-actor-collaboration-research-2026-08.md)
34. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
35. accepted architecture/DB ADRs.

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
- Preserve Person / Asset native identity versus Subject / Actor / Resource contextual-role distinctions.
- Do not make `Asset` a universal managed-object root.
- Do not make `Resource` a universal provider/entity root or generic FK merely for scheduling convenience.
- Keep Resource Requirement, candidate eligibility, Allocation, Reservation/Claim and actual use/consumption semantically distinguishable.
- Do not fabricate historical intention, allocation, identity or earlier knowledge from later relevance/resolution.
- Do not create one table/entity per life topic.
- Do not collapse semantics into arbitrary JSON or one universal graph/reality/fact/subject/actor/asset/resource object.
- Do not let AI inference become confirmed/canonical truth, Person identity, Subject attribution, Asset identity/ownership, Resource allocation or Authority automatically.
- Preserve progressive disclosure.
- Run the dedicated Multi-Actor Compatibility Gate after the Core Semantic Gate.
- New primitives require materially distinct identity/lifecycle/authority/invariants/query behavior.
- Run Cluster Integration + Cluster Multi-Actor Stress before declaring a cluster complete.
- Do not leave material neighboring questions as generic `TBD`/`review later`; every applicable closure point must classify them.
- A `SAFE DEFERRED` item must identify why it is non-blocking, its owner/future stage, exact reopening trigger and tests to rerun.
- Re-run prior clusters together when a new cluster resolves old deferred boundaries.
- Finish Data / Subjects, then perform the dedicated clusters 1–4 deferred-dependency closure and Cross-Cluster Validation v4 before Relationships / Reasoning.
- During that closure, execute the terminology-neutral Asset managed/tracked-referent review recorded in `asset-v0-validation.md`.
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
Resource v0                     PASS WITH HARDENING / ACCEPTED PLANNING-EXECUTION ROLE
Account boundary                ACCEPTED / DETAILED MODEL DEFERRED

User universal domain root      REJECTED
Register kernel candidate       REJECTED
Universal RegisterEntry         REJECTED
Universal Subject entity/root   REJECTED
Universal Actor entity/root     REJECTED
Universal managed-object Asset  REJECTED
Universal Resource entity/root  REJECTED
```

First-three-cluster regression result remains:

```text
18 accepted concepts retained before Cluster 4
0 structural reopenings
0 concept removals
0 justified concept merges
0 mandatory new primitives
```

Existing cross-cluster hardenings remain:

1. reported/asserted reality != established Actual;
2. Milestone attainment is Evidence/evaluation-backed and must not duplicate underlying reality.

Cluster-4-specific mandatory revisit:

3. Asset scope must be re-tested terminology-neutrally before final Cluster-4 consolidation.

Cluster 4 has completed its planned **first-pass candidate reviews**, but this is **not yet a Cluster PASS**. Integration and multi-actor cluster gates are next.

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

Identity/role boundary:

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
= contextual planning/execution eligibility/capability over native providers

Principal
= deferred security/authorization identity
```

A Person or Asset may play Resource role without being re-identified as a Resource. A Person may play Actor/Subject/Resource roles independently. Resource candidacy does not imply Responsibility, consent, Performer status or allocation Authority.

No universal Actor/User/Subject/Resource/managed-object root, Team/Organization/ACL/Stewardship primitive, or `persons.id = accounts.id` schema is pre-approved.

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
Resource       -> canonical planning/execution eligibility role; not entity
Account        -> platform/access identity boundary; detailed security model deferred
User           -> product/implementation term only
Register       -> possible product/UI label for longitudinal capability, not kernel primitive
Tracker/History/Progress -> product/query views over native records
```

Product labels such as `Car`, `Camera`, `Gear`, `Device`, `Equipment`, `Room`, `Who's available?` or `Inventory` do not automatically create or broaden kernel types.

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

# ACTIVE TASK — Data / Subjects Cluster Integration

The first three clusters are validated together. Data / Subjects has completed the planned first-pass candidate reviews.

**Active task now:** run the Data / Subjects **Cluster Integration Gate + Cluster Multi-Actor Stress Gate** in read-only mode before any new canonical write scope.

Do not jump to SQL/API design or Relationships / Reasoning yet.

## Cluster-4 candidate result

```text
Quantity         ACCEPTED — canonical value semantics
Register         REJECTED as kernel primitive; longitudinal capability retained
RegisterEntry    REJECTED as universal semantic record
Subject          ACCEPTED — canonical semantic role; entity/root rejected
Person           ACCEPTED — canonical native human entity
Actor            ACCEPTED — canonical agency role/capability; entity/root rejected
Account boundary ACCEPTED — platform/access identity; detailed auth model deferred
User root        REJECTED — product/implementation term only
Asset            ACCEPTED — current scoped native entity; mandatory terminology-neutral revisit
Resource         ACCEPTED — canonical planning/execution role; entity/root rejected
```

No additional primitive should be invented merely because candidate review is complete. The integration gate must first determine whether the set is coherent, redundant, insufficient, or over-modeled.

---

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

---

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

The integration gate must verify that rejecting Register/Entry still reconstructs representative long-term history, quick-capture and trend workflows without hidden duplication.

---

## Subject v0

> Contextual semantic role played by the native referent a descriptive record primarily concerns.

```text
Subject entity/root = rejected
Subject != Person / Actor / Account / Principal / Asset / Resource
Subject != observer / recorder / source / transformer / Authority / Visibility
```

Person and Asset may play Subject role while retaining native identity. Resource role remains a different contextual question.

Checkpoint: [`Subject v0 Validation`](../domain/checkpoints/subject-v0-validation.md).

---

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
- Person may play Subject, Actor/specific action and Resource roles without identity change;
- Actor is agency semantics, not a wrapper identity and not a replacement for performer/recorder/observer/confirmer/proposer roles;
- Actor != Resource/Responsibility/Authority/ownership;
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

---

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
Resource role = candidate/allocated for photo shoot
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

During the dedicated post-Cluster-4 dependency closure, compare how mature products model managed/tracked referents across:

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

---

## Resource v0

> Resource is the contextual planning/execution role through which a native referent, service, pool, supply, or other eligible capability-bearing thing is considered able to satisfy an execution requirement by providing usable availability, capacity, access, capability, or consumable supply.

Accepted classification:

```text
RESOURCE
CANONICAL SEMANTIC PLANNING / EXECUTION ROLE-CAPABILITY
NOT ENTITY / ROOT
```

Core planning separation:

```text
Requirement
what is needed
        ↓
Candidate
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

Critical guardrails:

```text
Resource != Person
Resource != Asset
Resource != Subject
Resource != Actor
Resource != Requirement
Resource != candidate set
Resource != Allocation
Resource != Reservation / Capacity Claim
Resource != actual use / consumption
Resource != Responsibility / Performer / Participant
Money/Budget != Resource by default
```

Allowed composition:

```text
Person may play Resource role
Asset may play Resource role
future Place/service/pool/supply may play Resource role where justified
```

Availability/Capacity alignment:

```text
native referent / supply
        ↓ Resource role
schedulable subset
        ↓
Availability + Capacity
        ↓
Reservation / Claim
```

A schedulable Resource is only a Resource-role case whose time-dependent capacity matters. Not every Resource needs a calendar or capacity profile.

Files:

- [`Resource v0`](../domain/concepts/resource.md)
- [`Resource v0 Validation`](../domain/checkpoints/resource-v0-validation.md)
- aligned [`Availability & Capacity v0`](../domain/concepts/availability-capacity.md)

---

# First-pass Cluster-4 boundaries now resolved

The following inherited questions are no longer unclassified at the current first-pass baseline:

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
Subject vs Resource — RESOLVED
Person vs Actor — RESOLVED
Person vs Account — RESOLVED at conceptual level
Person vs Asset — RESOLVED at current baseline
Person vs Resource — RESOLVED
Actor vs Account — RESOLVED at conceptual level
Actor vs Resource — RESOLVED
Asset vs fungible stock — RESOLVED conceptually
Asset identity vs ownership — RESOLVED at identity level
Asset vs Resource — RESOLVED at current baseline
Availability/Capacity vs Resource — RESOLVED
User universal kernel identity — REJECTED
Resource universal entity/root — REJECTED
```

These resolutions remain reopenable if integration or the mandatory Asset re-review exposes a contradiction.

---

# Current SAFE DEFERRED / transition obligations

Cluster integration must actively pressure these; the dedicated post-Cluster-4 closure must then classify every still-material item as `RESOLVED`, `SAFE DEFERRED`, or `REOPEN` with owner/trigger/tests.

Current material items include:

## Identity / managed referents

- Asset scope vs terminology-neutral managed/tracked-referent model — **MANDATORY REVISIT**;
- Asset vs Place/Location/Property;
- Asset vs living-entity identity;
- Asset vs Document/Artifact/FinancialAccount/service;
- Asset model/type/profile semantics;
- Asset identity reconciliation/merge/split;
- Person reconciliation/merge/split and identity-history persistence;
- heterogeneous Subject/Actor/Resource/native-referent persistence.

## Resource planning

- Resource Requirement / candidate / Allocation semantics;
- Resource Reservation/Claim physical and relationship representation;
- planned Resource versus actual use/consumption;
- pool/interchangeable capacity semantics;
- consumable supply / inventory / movement semantics if concrete workflows justify them;
- Resource vs future Place/service/capability/skill native concepts;
- Resource allocation Authority / Visibility / access.

## Authority / collaboration

- Principal/security identity and Account credential/provider mechanics;
- delegated/on-behalf-of Actor semantics;
- Subject vs focus/context/typed Relationship;
- Subject/Person/Actor/Asset/Resource association privacy vs Visibility;
- Responsibility/Assignment/Hand-off/Stewardship;
- Participation and actor-scoped Actual participation;
- Authority vs Visibility/governance.

## Reality / evidence / reasoning

- Actual establishment under Authority/Decision/reconciliation semantics;
- Confirmation vs Authority/Acknowledgement/Acceptance/Version;
- Evidence vs GoalCriterion/Relationship/Decision/Version;
- Milestone attainment vs Evidence/GoalCriterion/Decision;
- Provenance vs Version/Decision/Audit/Authority;
- provenance retention/privacy/deletion;
- contextual competing assertions under Authority rules;
- AI Context Builder inference/disclosure boundaries.

## Time / value / data

- Recurrence vs Trigger;
- Quantity vs Money/MonetaryAmount;
- Quantity vs ratings/scales/ratio/percentage/count semantics;
- Quantity vs custom unit-definition semantics;
- Quantity vs elapsed duration/calendar-relative time;
- Quantity vs Range/Threshold/comparator semantics;
- Quantity decimal/unit physical representation;
- sampled-series physical representation;
- longitudinal query/materialization/saved-view implementation;
- aggregate visibility vs source-record visibility;
- future transaction/movement/snapshot semantics only when concrete workflow evidence requires them.

Nothing in this list authorizes prematurely adding a primitive.

---

# ACTIVE NEXT REVIEW — Data / Subjects Cluster Integration Gate

The next review is **not another concept candidate**.

It must stress the whole Cluster-4 result together:

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

The minimum cluster registry is:

```text
CL-01 representative reconstruction
CL-02 deep chronology
CL-03 redundancy / destructive remove-merge-split
CL-04 top-down traceability
CL-05 bottom-up reconstruction
CL-06 lateral propagation
CL-07 history / correction / reconciliation
CL-08 scale / product complexity
+
Cluster Multi-Actor Stress Gate
```

Mandatory representative/adversarial scenarios should include at least:

- personal weight/health Observation with Quantity and implicit self UI;
- caregiver recording about a non-account Person;
- same Person later gaining/changing/losing Account access;
- shared Asset with owner/holder/steward/visibility differences;
- Asset observed as Subject and separately used as Resource;
- abstract Resource Requirement with late binding and substitution;
- Person as Resource candidate while Performer/Responsibility remain separate;
- room/place-like Resource without forcing Place into Asset;
- consumable supply without per-unit Asset/Resource identity;
- longitudinal tracker/history after Register rejection;
- conflicting or corrected Subject/Person/Asset attribution;
- provider identity mismatch/duplicate reconciliation;
- private availability/free-busy projection without source disclosure;
- AI proposes identity/resource matches but lacks Authority;
- scale pressure from many Observations, Assets, candidates, pools, provider mappings and historical corrections;
- simple-user regression where internal vocabulary remains hidden.

The gate must ask both directions:

```text
Can every required workflow be reconstructed from accepted concepts?
```

and:

```text
Can any accepted concept be removed/merged without losing semantic truth?
```

The cluster integration verdict is **provisional for transition purposes** until deferred-dependency closure and Cross-Cluster v4 pass.

The integration analysis is read-only until a later exact Git write scope is stated and approved.

---

# TRANSITION GATE — after Cluster-4 integration

Before Relationships / Reasoning begins, execute exactly:

```text
Data / Subjects cluster integration
        ↓
Data / Subjects multi-actor stress
        ↓
provisional cluster verdict
        ↓
DEFERRED DEPENDENCY CLOSURE — clusters 1–4
  includes MANDATORY terminology-neutral Asset re-review
        ↓
RESOLVED / SAFE DEFERRED / REOPEN for every material open boundary
        ↓
Cross-Cluster Validation v4 — clusters 1–4
        ↓ only after PASS
Relationships / Reasoning
```

The dependency closure must revisit inherited issues from the first three clusters as well as Cluster-4 findings. Nothing material may remain as unowned limbo.

Cluster 4 must not be called definitively consolidated before the Asset scope re-review, dependency closure and Cross-Cluster v4.

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
- Resource Requirement / Allocation / substitution where justified;
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
- Resource Requirement/Allocation/Reservation versus Responsibility/Performer;
- Account/Principal/Authority/delegation boundaries;
- Asset ownership/possession/custody/stewardship/location/Visibility;
- historical Person/Actor/Asset/resource-allocation attribution after Account/relationship changes.

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
Resource Requirements where execution needs something
        ↓
native Person / Asset / future Place / service / pool / supply
        ↓ contextual Resource role / eligibility
Availability / Capacity where schedulable
existing claims / reservations
        ↓
feasibility + candidate evaluation
        ↓
Allocation / selection where required
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
  └─ may play Resource role

Asset
= current scoped native physical-object identity
  ├─ may play Subject role
  └─ may play Resource role

Actor
= agency semantics over native identity

Account
= platform/access identity context; not Person/Actor

Resource
= contextual planning/execution role; not identity/root

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

Active/current items include the SAFE DEFERRED / transition obligations listed above.

Resolved at current first-pass baseline:

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
- Subject vs Resource;
- Person vs Actor;
- Person vs Account at conceptual level;
- Person vs Asset at current baseline;
- Person vs Resource;
- Actor vs Account at conceptual level;
- Actor vs Resource;
- Asset vs fungible stock at conceptual level;
- Asset identity vs ownership at identity level;
- Asset vs Resource at current baseline;
- Availability/Capacity vs Resource;
- User as universal kernel identity;
- universal Resource entity/root.

The mandatory Asset scope re-review may reopen Asset-related resolved items if the current physical/durable boundary proves terminology-driven. Cluster integration may reopen any first-pass concept if a real contradiction appears.

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
Data / Subjects first-pass candidate reviews COMPLETE
  Quantity v0 accepted
  Register candidate rejected
  Subject v0 accepted as semantic role
  Person v0 accepted
  Actor v0 accepted as agency role
  Account boundary accepted / detailed model deferred
  Asset v0 accepted as current scoped native entity
  Resource v0 accepted as planning/execution role
↓ NOW
Data / Subjects Cluster Integration Gate + Multi-Actor Stress — READ ONLY
↓
provisional Cluster-4 verdict
↓
Deferred Dependency Closure — clusters 1–4
  + mandatory Asset terminology-neutral managed/tracked-referent review
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

Continue from Methodology v3 + Execution Template v3 + Language Map + accepted Quantity/Subject/Person/Actor/Asset/Resource baselines + Register rejection checkpoint + Person/Actor/Account checkpoint + Asset checkpoint + Resource checkpoint + the three validated cluster checkpoints.

**Active next action:** execute the **Data / Subjects Cluster Integration Gate and Cluster Multi-Actor Stress Gate in read-only mode**. Do not create the cluster checkpoint or modify Git until a later exact write scope is stated and explicitly approved.

The current Asset scope is not to be treated as final until the mandatory terminology-neutral managed/tracked-referent review is executed during the dedicated post-Cluster-4 dependency closure. Do not create a parallel validation standard, terminology tree, universal actor/user/subject/asset/resource root or collaboration ontology.