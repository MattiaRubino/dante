<!-- LIFEOS-CANONICAL-SPLIT document="README.md" part="2" total="3" -->
> **Canonical document split — Part 2 of 3.** Parts 1–3 together form one authoritative document; this is a physical split only, not a summary/reference hierarchy. The payload preserves the full pre-compaction baseline first and later downstream amendments in sequence; later explicit amendments override stale status/deferral wording without deleting the earlier rationale. Navigation: [Part 1](README.md) · **Part 2** · [Part 3](README-part-3.md)

<!-- LIFEOS-CANONICAL-PAYLOAD -->
# Canonical non-collapse rules — current cross-cluster baseline

```text
Actual != Session / Outcome / Observation / Confirmation / Evidence / Provenance
shared Actual != identical actor-specific Actual Participation
reported/asserted reality != established Actual

Outcome != lifecycle state / Observation / Confirmation / Evidence / Provenance / Milestone
Milestone attainment != duplicate Actual/Outcome/Observation truth

Observation != Quantity / universal RegisterEntry / Evidence / Confirmation / Provenance

Subject entity/root = rejected
Subject != Person / Actor / Account / Principal / Asset / Resource
Subject != observer / recorder / source / transformer / authority / viewer

Person != Actor / Resource / Participant / Account / Principal / User / Asset

Actor entity/root = rejected
Actor != Resource / Account / Principal / Responsibility / Participation / Authority
Actor != specific performer/recorder/observer/confirmer/proposer/responsible/participant relation
specific action role > generic actor edge when known

Account != Person / Actor / Subject / Participant / Principal by default

Asset != Subject / Resource / Person
Asset identity != owner / holder / custodian / steward / model definition
physical thing != Asset automatically
managed thing != Asset automatically
universal ManagedObject root = rejected

Resource entity/root = rejected
Resource != Requirement / candidate set / Allocation / Reservation / actual use
Resource != Responsibility / Performer / Participant / Participation
Resource role != provider identity
Resource reservation != Participation
Money/Budget != Resource by default

universal Relationship entity/root/supertype = rejected
semantic-free related_to as kernel truth = rejected
specific relation meaning > generic edge
qualified relation structure != independent entity automatically
queryability/cardinality/database row id != domain identity
relation orientation/symmetry/transitivity/inverse rules are family-specific

Responsibility != requester / expected performer / actual performer
Responsibility != Participation / Resource / Authority / Visibility / Stewardship
unknown Responsibility != explicitly open/unassigned
Assignment / Claim / Hand-off != standalone universal primitives
hand-off request != effective transfer by default
Responsibility transfer != Activity identity change

Participant entity/root = rejected
Participation != Responsibility / Performer / Resource / Organizer / Authority / Visibility / Session
Invitation != Acceptance / Actual Participation
Participation response != Actual Participation
accepted != attended
declined != proved absent
no response != declined
no attendance evidence != proved absence
Attendance universal primitive = rejected

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
physical-object identity need         RETAINED
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

Resource role preserves independently justified provider semantics and does not create identity, Responsibility or Participation.

---

# Relationships / Reasoning — ACTIVE DOMAIN REVIEW SPACE

**Status:** IN PROGRESS.

Completed so far:

- [`Relationship v0 validation`](checkpoints/relationship-v0-validation.md) — **PASS WITH HARDENING**;
- [`Responsibility v0`](concepts/responsibility.md) — [`validation`](checkpoints/responsibility-v0-validation.md) — **PASS WITH HARDENING**;
- [`Participation v0`](concepts/participation.md) — [`validation`](checkpoints/participation-v0-validation.md) — **PASS WITH HARDENING**;
- universal Relationship primitive/root rejected;
- direct-vs-specific-qualified relation discipline accepted;
- no generic `related_to` kernel truth;
- no universal symmetry/transitivity/inverse reasoning rules;
- Assignment/Claim/Hand-off as standalone universal primitives rejected;
- Responsibility vs Stewardship semantic boundary resolved;
- universal Participant/member/social-graph root rejected;
- Invitation/Attendance as standalone universal primitives rejected;
- intended/response Participation separated from Actual Participation.

Remaining candidate space based on demonstrated dependencies includes:

- Authority / Visibility;
- Acknowledgement / Acceptance / Agreement / Verification where concrete workflows require them;
- Principal / delegation / on-behalf-of security/authority semantics;
- Dependency;
- Stewardship standalone primitive question when concrete product pressure requires it;
- Contribution;
- Goal relationships / GoalCriterion;
- Evidence/Criterion relationships;
- Resource Requirement / Allocation / substitution where justified;
- Decision;
- Version;
- AI Proposal;
- focus/context relationships;
- Trigger/policy semantics including fallback/conditional Responsibility;
- group/collective actor semantics where future cases require them.

These remain **candidates**, not a checklist of primitives that must survive.

The next review must be selected by dependency leverage. Responsibility and Participation now both expose the same common-ground/governance pressure: Authority, Visibility, Acceptance/Acknowledgement, delegation/on-behalf-of and reconciliation. This cluster of boundaries currently deserves re-scoring before selecting the next candidate; none is pre-accepted.

From this stage onward the Adjacent Dependency Sweep remains mandatory before every concept verdict.

Mandatory inherited re-tests include:

- Evidence as semantic role vs specific qualified relation representation;
- Provenance lineage vs Version/Decision/Audit;
- Confirmation vs Authority/Acknowledgement/Acceptance;
- competing assertions and canonical decision policy;
- Milestone attainment/evaluation relationship;
- collaborative Session/Actual attribution;
- Participation response vs Actual Participation/evidence threshold;
- Subject vs focus/context/Visibility;
- Person/Actor specific roles vs Participation/Responsibility/Stewardship;
- Resource Requirement/Allocation/Reservation versus Responsibility/Performer/Participation;
- Account/Principal/Authority/delegation boundaries;
- Asset ownership/possession/custody/stewardship/location/Visibility;
- historical Person/Actor/Asset/resource-allocation/Responsibility/Participation attribution after Account or relationship changes;
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
Responsibility v0 review        — PASS WITH HARDENING
Participation v0 review         — PASS WITH HARDENING

0 structural reopenings
0 unclassified material dependencies

↓ CURRENT
Relationships / Reasoning
  next candidate: reselect by dependency leverage
  strongest current pressure area: Authority / Visibility / Acceptance-Acknowledgement / delegation
  none pre-accepted
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

The authoritative Clusters 1–4 dependency register remains:

- [`Deferred Dependency Closure — Clusters 1–4 v0`](checkpoints/deferred-dependency-closure-clusters-1-4-v0.md).

Cluster-5 specific closures/reopening triggers are additionally recorded in:

- [`Relationship v0 validation`](checkpoints/relationship-v0-validation.md);
- [`Responsibility v0 validation`](checkpoints/responsibility-v0-validation.md);
- [`Participation v0 validation`](checkpoints/participation-v0-validation.md).

Responsibility v0 resolves the previous broad Activity ↔ Responsibility/Assignment/Hand-off boundary at the semantic level.

Participation v0 resolves the previous Event/Session/Actual ↔ Participation boundary at the semantic level.

Still SAFE DEFERRED around Responsibility/Participation are:

- Authority/delegation;
- Acceptance/Acknowledgement;
- Visibility;
- Provenance/Version/Decision/reconciliation mechanics;
- standalone coordination Stewardship;
- collective/joint/fallback Responsibility;
- participant role taxonomy;
- collective/group Participation;
- recurring-series Participation inheritance/override;
- provider attendance reconciliation/evidence threshold;
- retention/deletion/privacy;
- exact qualified Responsibility/Participation identity/persistence.

Other high-value groups include:

- Milestone / GoalCriterion / Evidence / Decision;
- Confirmation / Authority / Acknowledgement / Acceptance / Verification;
- Provenance / Version / Decision / Audit / retention;
- Actual establishment / Authority / reconciliation;
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

Current result:

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
- Responsibility is a specific accountability relation family independent of requester/performer/Resource/Authority/Participation;
- Assignment/Claim/Hand-off are role-specific operations/workflows rather than universal primitives;
- explicit open/unassigned Responsibility != unknown Responsibility;
- coordination Stewardship is distinct from Responsibility but standalone primitive remains deferred;
- Participation is a specific involvement relation family, not Participant identity or universal membership;
- Invitation is participation proposal/request semantics, not universal primitive;
- Participation response != Actual Participation; accepted != attended; declined/no response/no telemetry are not proofs of Actual absence;
- Attendance is Event-facing Actual Participation semantics, not universal primitive or Session;
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
Responsibility (specific semantic relation family; not universal entity/root)
Participation (specific semantic relation family; not entity/root)
```

Accepted boundary but not yet a fully modeled concept:

```text
Account != Person != Actor
```

Rejected historical/current candidates are not counted as accepted concepts.

---

# Final validation rule

A final whole-domain stress test remains mandatory before broad persistence implementation.

Cross-Cluster v4 and the current Relationship/Responsibility/Participation reviews do not prevent later reopening when subsequent Relationships / Reasoning candidates, the logical/physical data model, integrations, safety/privacy requirements, or stronger real-world evidence expose a genuine contradiction.

Do not jump directly from the current semantic review to SQL/API stabilization.

---

# 2026-08-13/14 — Downstream current-state consolidation amendment

This amendment is part of the same canonical document. It preserves downstream current-state sections without deleting the full pre-compaction baseline above. A current section is retained in full whenever it contains material text not already present verbatim in the baseline, so heading/list/example context is preserved. Where a later status, closure, or repository-state statement conflicts with an earlier one, the later amendment is authoritative; earlier rationale, examples, rejected alternatives, tests, and boundary detail remain preserved unless explicitly superseded.


**Status:** Active design authority for the LifeOS core domain model  
**Current workstream:** [`../workstreams/domain-model.md`](../workstreams/domain-model.md)  
**Validation standard:** [`validation-methodology-v3.md`](validation-methodology-v3.md)

## Purpose

The Domain Atlas defines the semantic kernel LifeOS must preserve before logical data modeling, PostgreSQL persistence, API contracts, backend packages, or product-specific projections are fixed.

The Atlas is intentionally stricter than ordinary product documentation.

It answers questions such as:

- what has independent semantic identity;
- what is contextual relation/capability;
- what is derived/projection only;
- what is product/UI language rather than kernel truth;
- what history must remain reconstructible;
- where Person, Actor, Account, Subject, Resource, Authority, Visibility, Agreement, Consent, Version, Reconciliation, Evidence, Actual, and other dimensions must remain separate;
- what may be safely deferred to logical/security/specialist design.

The objective is not to maximize ontology size. The objective is the **smallest model that survives reality without losing identity, history, truth, multi-actor separation, privacy, Authority, queryability, extensibility, and simple product usability**.

---


## Product compass
LifeOS is an adaptive personal operating system connecting:

```text
goals / intentions
        ↓
plans / routines / projects
        ↓
real calendar time
        ↓
realistic capacity / constraints
        ↓
observed / confirmed reality
        ↓
progress / outcomes / evidence
        ↓
adaptive future planning
```

Its defining value is not merely recording tasks or events. It is understanding the user's current situation, coordinating competing commitments, preserving history, and adapting future planning under user control.

Product principles inherited by the Domain Atlas:

- personal-first, not enterprise-collaboration-first;
- structurally multi-actor-ready without forcing collaborative UX into V1;
- modules contribute activities, constraints, observations, evidence, progress and context rather than creating semantic silos;
- external providers are optional normalized sources, not ontology authorities;
- AI produces structured proposals/reasoning under Authority/Visibility/privacy constraints rather than unchecked truth or writes;
- kernel precision should normally remain hidden behind simple user-facing language.

The accepted product identity / North Star on `main` may provide product-direction evidence, but this Domain Atlas remains authoritative for kernel terminology and semantic boundaries.

---


## Source authority
When sources conflict, use this order:

1. current main code/migrations/tests/accepted ADRs;
2. current durable product/architecture docs on main;
3. active workstream handoff for scoped unmerged work;
4. other current active-branch files;
5. historical branches/merged PRs/checkpoints;
6. chat/remembered context.

The active workstream may be newer than main **only inside its explicitly scoped unmerged work**. It cannot silently override unrelated current main truth.

---


## Operating rules
Required repository process is defined by:

- [`../development/operating-rules.md`](../development/operating-rules.md);
- [`../development/documentation-and-handoff.md`](../development/documentation-and-handoff.md);
- [`../development/branching-and-environments.md`](../development/branching-and-environments.md).

The workstream handoff is a live `save game`, not an optional summary.

Before any new Git write scope on the active Domain Model branch:

```text
state exact branch
state exact pre-scope commit
state exact path scope
wait for explicit approval
write only approved scope
QA against pre-scope
```

Historical validation/checkpoint records are preserved. Later semantic resolutions are appended as explicit downstream closures rather than silently rewriting what earlier work knew.

---


