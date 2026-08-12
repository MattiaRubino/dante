# LifeOS Domain & Product Language Map

**Status:** Canonical terminology reference for the active Domain Atlas  
**Established:** 2026-08-11  
**Current revision:** 2026-08-12 — Participation v0 PASS WITH HARDENING; intended/response involvement separated from Actual Participation  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

This is the fast canonical reference for LifeOS vocabulary.

It keeps four distinct languages aligned without forcing a one-to-one mapping:

```text
DOMAIN LANGUAGE
what the concept means canonically
        ↓
PRODUCT LANGUAGE
how LifeOS packages/presents it
        ↓
UI LANGUAGE
what users actually read/manipulate
        ↓
IMPLEMENTATION LANGUAGE
API / schema / code names once designed
```

Canonical rule:

> **A domain concept does not require a dedicated visible UI object, and a visible product/UI term does not automatically justify a separate domain primitive.**

Detailed lifecycle, invariants, history, evidence and validation remain in the concept specs/checkpoints.

---

# 1. Terminology authority and precedence

When terminology conflicts, use this order:

1. accepted Domain Atlas concept specification;
2. this Domain & Product Language Map;
3. current Domain Atlas checkpoint / cross-cutting guardrail;
4. active workstream handoff;
5. current V1 product behavior documents;
6. historical product glossaries/planning documents;
7. conversation history.

The old `docs/product/v1-core-domain-glossary.md` remains useful product-history evidence but is not authoritative where the current Domain Atlas differs.

This map records decisions; it does not create primitives.

---

# 2. Term status classes

## CANONICAL

Accepted Domain Atlas concept/capability/value/role/relation semantics with stable current semantics.

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
Availability
Capacity
Actual
Outcome
Observation
Confirmation
Evidence
Provenance
Quantity
Subject (semantic role, not entity)
Person (native human entity)
Actor (semantic agency role/capability, not entity)
Asset (current scoped native physical-object entity)
Resource (semantic planning/execution role/capability, not entity)
Relationship modeling discipline (cross-cutting semantic rule; not entity/root)
Responsibility (specific semantic relation family; not universal entity/root)
Participation (specific semantic relation family; not entity/root)
```

`Account` has an accepted conceptual boundary as platform/access identity but its detailed domain/security model is intentionally deferred; it is therefore not listed as a fully modeled canonical kernel concept yet.

`Asset` is canonical as the **current scoped baseline**. The mandatory terminology-neutral Cluster-4 review has been completed: a universal `ManagedObject` root was rejected under current evidence, the individually tracked physical-object identity need survived, and the exact internal noun `Asset` remains non-semantic/reopenable.

`Relationship` does **not** denote a universal domain entity. The accepted baseline is a modeling discipline: use the most specific truthful relation semantics; keep simple connections direct when semantically complete; introduce a domain-specific qualified relation only when the connection itself has materially relevant state/history/lifecycle/context. See `checkpoints/relationship-v0-validation.md`.

`Responsibility` is canonical as the specific relation answering who is accountable for ensuring a bounded commitment is appropriately handled. It is not requester, expected performer, actual performer, Resource, Authority, Visibility, ownership or coordination Stewardship. See `concepts/responsibility.md` and `checkpoints/responsibility-v0-validation.md`.

`Participation` is canonical as the specific relation family for expected/intended or Actual involvement in a bounded shared occurrence/interaction. Participant is a contextual role over native identity; response/intention and Actual Participation remain distinct. See `concepts/participation.md` and `checkpoints/participation-v0-validation.md`.

## DERIVED

Useful value/state/projection computed from canonical facts rather than a universal primitive.

Examples:

```text
free capacity
overrun
lateness
adherence
streak
query aggregates
needs confirmation
some progress percentages
```

## PRODUCT PROFILE

Recognizable product shape built from canonical concepts without currently requiring a separate kernel primitive.

Examples:

```text
Project
Program
Workout
Study plan
Release plan
saved longitudinal tracker/view
Vehicle profile
Camera profile
Equipment profile
```

A product profile may specialize an Asset experience without creating a new kernel identity concept by default.

## PRODUCT / UI TERM

User/designer vocabulary that maps to canonical or deferred semantics but does not itself define a kernel concept.

Examples:

```text
Task
Repeat
Deadline
Calendar Block
Busy
This time
Inbox
Registra un dato
Register / Registro
Tracker
History / Storico
Progress
User
Gear
Device
Equipment
Inventory
Required equipment
Who's available?
Assigned to
Claim
Hand off
Going / Maybe / Can't go
Attended
```

`User` is deliberately product/implementation language. It must not be used as a universal domain synonym for Person, Actor, Account or Principal.

Terms such as `Gear`, `Equipment`, `Device`, `Things`, or `Inventory` may expose some Asset-backed experiences without redefining Asset semantics.

The word `Resource` itself should usually remain hidden when a more natural label such as Person, Room, Camera, Equipment, Service, or `Who's available?` is clearer.

The word `Relationship` is not a required user-facing noun. UI should normally expose the specific meaning (`Done by`, `Depends on`, `Parent`, `Participant`, `Owner`, `Based on…`) rather than a generic relationship object.

`Assigned to`, `Claim`, and `Hand off` are valid product/action language, but each material action must map to a specific semantic role. The same word must not become a universal kernel object.

`Going`, `Maybe`, `Can't go`, `Attended`, and similar labels may expose Participation response or Actual Participation. UI convenience must not collapse those two semantics.

## PROVISIONAL

Recurring semantic need with meaningful evidence but an unfinished domain boundary.

```text
Stewardship
Authority
Visibility
Acknowledgement
Acceptance / Agreement
Resource Requirement
Allocation / selection
```

## DEFERRED

Demonstrated semantic area intentionally postponed to a later review.

```text
Principal
Trigger
Verification
Decision
Version
Place / Location / Property semantics
living-entity identity beyond Person
Document / Artifact identity model
FinancialAccount specialist model
inventory / supply / consumption semantics
```

Detailed Account/credential/provider/security mechanics are deferred even though the Account != Person != Actor conceptual boundary is already fixed.

A generic Personal Knowledge link layer remains separately deferred. Its future flexibility must not automatically acquire operational, evidentiary, authority, allocation, participation or Actual semantics.

Coordination Stewardship is a demonstrated semantic dimension distinct from Responsibility, but standalone primitive status remains SAFE DEFERRED pending concrete workflows that require explicit independent assignment/transfer/query/history.

## HISTORICAL / SUPERSEDED

Earlier terminology preserved in Git/docs but not authoritative for the current kernel.

- `Register` as a universal kernel container and `RegisterEntry` as a universal semantic record are rejected historical candidates. See `checkpoints/register-v0-validation.md`.
- `Subject` as a universal entity/root/wrapper is rejected. The accepted meaning is a contextual semantic role over native referent identity. See `concepts/subject.md` and `checkpoints/subject-v0-validation.md`.
- universal `Actor` entity/root/wrapper is rejected. Actor is accepted as contextual agency semantics over native referent/system identity. Specific action roles remain preferred over a generic `actor` relation. See `concepts/actor.md`.
- universal `Resource` entity/root/wrapper is rejected. Resource is accepted as contextual planning/execution eligibility/capability over independently justified referent/value/pool/supply/service semantics. See `concepts/resource.md` and `checkpoints/resource-v0-validation.md`.
- universal `User` domain root and `Person = Account` / `Actor = Account` identity models are rejected. See `checkpoints/person-actor-account-v0-validation.md`.
- historical `Asset/Soggetto` language that grouped person, animal, plant, account, document, house and equipment under one generic managed-object umbrella is superseded. Current Asset v0 is narrower; a terminology-neutral cross-domain review rejected a universal `ManagedObject` root under current evidence. See `concepts/asset.md`, `checkpoints/asset-v0-validation.md`, and `checkpoints/data-subjects-v0.md`.
- universal `Relationship` entity/root/supertype and semantic-free `related_to` as kernel truth are rejected. The accepted result is specific relation semantics plus qualification only where the relationship itself materially requires it. See `checkpoints/relationship-v0-validation.md`.
- Assignment, Claim and Hand-off as standalone universal kernel primitives are rejected by Responsibility v0. They remain role-specific establishment/acquisition/transfer operations/workflows. See `checkpoints/responsibility-v0-validation.md`.
- universal Participant/Participation/member/social-graph roots are rejected. Participant is a contextual role and Participation is a specific relation family. Invitation and Attendance are not standalone universal primitives. See `concepts/participation.md` and `checkpoints/participation-v0-validation.md`.

---

# 3. UI exposure classes

- **DIRECT** — natural primary user-facing noun;
- **CONTEXTUAL** — visible under context-specific wording;
- **CONFIGURATION** — primarily rules/settings/actions;
- **ADVANCED** — detail/history/power-user surfaces;
- **HIDDEN** — mostly internal semantics; UI exposes consequences/actions instead.

Kernel sophistication must not force ontology vocabulary into simple UI.

---

# 4. Canonical Intention & Execution concepts

## Goal

**Status:** CANONICAL  
**Source:** `concepts/goal.md`  
**Question:** What outcome/condition/change/pattern is intentionally desired?  
**UI exposure:** DIRECT

```text
Goal != Plan
Goal != Activity
Goal != Milestone
Goal != Evidence
Goal identity != governor/stakeholder/contributor/subject/account
```

Possible UI: Goal, Objective, contextual Target.

## Plan

**Status:** CANONICAL  
**Source:** `concepts/plan.md`  
**Question:** How is a purpose intended to be pursued/organized?  
**UI exposure:** DIRECT / CONTEXTUAL

```text
Plan != Goal
Plan != Activity
Plan != Routine
Plan != Schedule
Plan != Actual
```

Product profiles may include Project, Program, Study plan, Training plan, Release plan, Trip plan and Rehabilitation plan.

## Activity

**Status:** CANONICAL  
**Source:** `concepts/activity.md`  
**Question:** What actionable work/behavior is intended to be performed?  
**UI exposure:** DIRECT / CONTEXTUAL

```text
Activity != Event
Activity != Plan
Activity != Session
Activity != Actual
Activity identity != requester/creator/responsible actor/expected performer/actual performer
```

Responsibility v0 closes the responsibility-family semantics: ordinary responsibility transfer/reassignment preserves Activity identity; Assignment/Claim/Hand-off are role-specific operations/workflows rather than Activity state or standalone universal primitives.

Possible UI: Task, Action, Workout, Study item, Maintenance action, Checklist item.

## Event

**Status:** CANONICAL  
**Source:** `concepts/event.md`  
**Question:** What occurrence-centred thing is expected to happen?  
**UI exposure:** DIRECT

```text
Event != Activity
Event != Schedule
Event != Participation response
Event != Actual Participation / attendance
Event != Milestone
Event identity != participant set/state
```

Participation v0 closes the participant/attendance boundary: invitation/response and Actual Participation are actor-scoped relation semantics around one Event identity.

Possible UI: Meeting, Appointment, Lesson, Exam, Concert, Flight, Shift, Interview, Race.

## Routine

**Status:** CANONICAL  
**Source:** `concepts/routine.md`  
**Question:** What behavioral/execution policy is intentionally expected to repeat?  
**UI exposure:** DIRECT

```text
Routine != Recurrence
Routine != Event series
Routine != Plan
Routine != observed habit
Routine identity != performer
```

## Milestone

**Status:** CANONICAL  
**Source:** `concepts/milestone.md`  
**Question:** What meaningful contextual checkpoint matters inside Goal/Plan?  
**UI exposure:** DIRECT / ADVANCED

```text
Milestone != Goal
Milestone != GoalCriterion
Milestone != Activity
Milestone != Event
Milestone != Outcome
Milestone != Actual
Milestone != Deadline
Milestone != Phase
```

Core hardening: Milestone attainment is Evidence/evaluation-backed checkpoint state; it is not an independent duplicate source of Actual, Outcome, Observation or other underlying reality.

---

# 5. Canonical Time concepts

## Occurrence

**Status:** CANONICAL  
**Source:** `concepts/occurrence.md`  
**Question:** Which expected instance from a recurring/generative source is this?  
**UI exposure:** HIDDEN / ADVANCED

```text
Occurrence != Recurrence
Occurrence != source Routine/Event
Occurrence != Schedule
Occurrence != Session
Occurrence != Actual
```

Typical UI: This time, This workout, This meeting, Only this one, This and future occurrences.

## Schedule

**Status:** CANONICAL  
**Source:** `concepts/schedule.md`  
**Question:** When is this schedulable subject currently accepted/intended/expected to happen?  
**UI exposure:** HIDDEN / CONFIGURATION

```text
Schedule != Temporal Constraint
Schedule != deadline/target
Schedule != Recurrence
Schedule != Availability
Schedule != Capacity claim
Schedule != Session/Actual
Schedule acceptance != Participation response/acceptance
```

## Session

**Status:** CANONICAL  
**Source:** `concepts/session.md`  
**Question:** Which logically continuous bounded episode of actual execution occurred?  
**UI exposure:** CONTEXTUAL / ADVANCED

```text
Session != Schedule
Session != Activity
Session != Occurrence
Session != Participation / Event attendance
Session != broader Actual/Outcome
```

Session identity follows logical execution continuity, not performer or participant count. Attendance does not manufacture one Session per participant.

## Temporal Constraint

**Status:** CANONICAL  
**Source:** `concepts/temporal-constraint.md`  
**Question:** Where/when is placement/duration/temporal relation allowed, required, bounded or preferred?  
**UI exposure:** CONFIGURATION

Possible UI: Deadline, Not before, Not after, Preferred time, Allowed window, Minimum/maximum duration.

`Deadline` is latest-bound Temporal Constraint semantics, not a separate kernel primitive.

## Recurrence

**Status:** CANONICAL  
**Source:** `concepts/recurrence.md`  
**Question:** How does a temporal/generative pattern repeat?  
**UI exposure:** CONFIGURATION

```text
Recurrence != Routine
Recurrence != Occurrence
Recurrence != Schedule
Recurrence != Trigger
Recurrence != responsibility rotation
```

## Availability

**Status:** CANONICAL semantic capability  
**Source:** `concepts/availability-capacity.md`  
**Question:** When may a schedulable Resource's capacity be used?  
**UI exposure:** DIRECT / CONFIGURATION / DERIVED

Availability is Resource-oriented. Subject-specific timing rules remain Temporal Constraints.

## Capacity

**Status:** CANONICAL semantic capability  
**Source:** `concepts/availability-capacity.md`  
**Question:** How much / what kind of compatible commitment can a schedulable Resource sustain?  
**UI exposure:** HIDDEN / DERIVED / ADVANCED

```text
scheduled != capacity consumed
overlap != universal conflict
Capacity != universal busy/free boolean
Capacity != universal scalar percentage
```

Resource v0 clarifies that a schedulable Resource is a provider playing Resource role where time-dependent capacity matters; Resource does not manufacture provider identity.

---

# 6. Canonical Reality & Evidence concepts

## Actual

**Status:** CANONICAL  
**Source:** `concepts/actual.md`  
**Validation:** `checkpoints/actual-v0-validation.md` — PASS WITH HARDENING  
**Question:** How did this specific intention or expectation resolve in reality?  
**UI exposure:** HIDDEN / ADVANCED / CONTEXTUAL

```text
Actual != Schedule
Actual != Session
Actual != Outcome
Actual != Observation
Actual != Evidence
Actual != Confirmation
Actual != Provenance
shared Actual != identical actor-specific Actual Participation
reported/asserted reality != established Actual
```

Core guardrails: contextual rather than universal; absence does not imply failure; passage of time does not establish Actual; conflicting assertions may remain unresolved; shared Actual does not imply identical actor participation.

## Outcome

**Status:** CANONICAL  
**Source:** `concepts/outcome.md`  
**Validation:** `checkpoints/outcome-v0-validation.md` — PASS WITH HARDENING  
**Question:** What result or disposition followed from this realization in the relevant context?  
**UI exposure:** CONTEXTUAL / HIDDEN / ADVANCED

```text
Outcome != Actual
Outcome != lifecycle/operational state
Outcome != Observation
Outcome != artifact/output
Outcome != Milestone
Outcome != Confirmation
Outcome != Provenance
Outcome != Evidence
```

Core guardrails: optional/contextual; no universal Outcome enum; absence does not imply failure; `unconfirmed` is epistemic rather than result semantics.

## Observation

**Status:** CANONICAL  
**Source:** `concepts/observation.md`  
**Validation:** `checkpoints/observation-v0-validation.md` — PASS WITH HARDENING  
**Question:** What was observed, measured, reported, or calculated about this Subject referent, and to what time/context does it apply?  
**UI exposure:** CONTEXTUAL / HIDDEN / ADVANCED

A persistent contextual record of a measured, perceived, reported, or explicitly derived property, state, value, rating, or simple assertion about a Subject referent.

```text
Observation != Actual
Observation != Outcome
Observation != Quantity
Observation != universal RegisterEntry
Observation != Evidence
Observation != Confirmation
Observation != Provenance
```

Core guardrails:

- not a universal fact/blob primitive;
- may exist without prior intention/Actual/Goal/saved tracker;
- effective time/context != recorded/ingested time;
- missing Observation != observed negative != failed measurement;
- subjective/conflicting Observations can coexist;
- query aggregates do not automatically become persisted Observations;
- high-frequency streams do not imply row-per-sample persistence;
- one Observation can appear in zero or many tracker/history/report views without duplication;
- Subject is a role over native identity, not a wrapper entity;
- Person, Actor, Account, Asset and Resource roles remain distinct when relevant.

```text
Quantity      = reusable scalar amount value semantics
Observation   = contextual observed/asserted record
Subject       = native referent's contextual aboutness role
Person        = native human identity
Actor         = contextual agency semantics; specific role preferred
Account       = platform/access identity boundary
Asset         = current scoped physical-object identity
Resource      = contextual planning/execution eligibility role
Tracker/view  = product/query presentation over native records
```

## Confirmation

**Status:** CANONICAL  
**Source:** `concepts/confirmation.md`  
**Validation:** `checkpoints/confirmation-v0-validation.md` — PASS WITH HARDENING  
**Question:** Who or what explicitly affirms this specific version of this target, for which purpose and context?  
**UI exposure:** CONTEXTUAL / HIDDEN / ADVANCED

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

Core guardrails:

- contextual and optional;
- no Confirmation != false/rejected/incorrect/not performed;
- target version/context/purpose matters;
- material correction does not inherit prior Confirmation silently;
- `awaiting confirmation` is derived workflow state;
- automation/AI must not fabricate human Confirmation;
- Confirmation by one actor does not imply Confirmation by another.

Typical UI: Confirm, Looks correct, Yes this happened, Review and confirm, Needs confirmation.

## Evidence

**Status:** CANONICAL semantic role / relationship  
**Source:** `concepts/evidence.md`  
**Validation:** `checkpoints/evidence-v0-validation.md` — PASS WITH HARDENING  
**Question:** What information materially bears on this evaluation, in what direction and context, and on what basis is it being used?  
**UI exposure:** HIDDEN / ADVANCED / CONTEXTUAL

Evidence is the contextual evaluative role played by source information when it is used to support, contradict, qualify or otherwise materially inform a specific evaluation target.

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

Core guardrails:

- information is not Evidence merely because it exists;
- Evidence does not duplicate source payload/identity;
- may support, contradict or qualify;
- Evidence existence does not establish target truth;
- no Evidence != Evidence against;
- no LifeOS record != proof of non-occurrence without a completeness rule;
- later relevance does not rewrite historical source purpose;
- one source can serve several evaluations without duplication;
- strength/certainty is contextual rather than one universal scalar;
- conflicting Evidence can coexist;
- private Evidence use does not create disclosure permission;
- Evidence semantics do not imply one persisted edge/entity per use.

Typical UI: Why is this progressing?, Based on…, Supporting data, Conflicting data, Review evidence.

## Provenance

**Status:** CANONICAL semantic lineage capability  
**Source:** `concepts/provenance.md`  
**Validation:** `checkpoints/provenance-v0-validation.md` — PASS WITH HARDENING  
**Question:** How did this specific record/material version come to exist, and what materially influenced its current form?  
**UI exposure:** HIDDEN / ADVANCED / CONTEXTUAL

Provenance is bounded contextual lineage covering materially relevant source entities, generation/import/derivation/transformation/correction activities, native actors/systems/providers and times.

```text
Source != Provenance
Provenance != truth
Provenance != Authority
Provenance != Confirmation
Provenance != Evidence
Provenance != Version
Provenance != Audit
```

Core guardrails:

- source is one lineage dimension, not the entire model;
- creator/source/recorder does not imply Authority;
- correction preserves material prior lineage rather than rewriting origin;
- derived/transformed records retain material source/process traceability;
- AI/OCR/import pipelines must not launder authorship/source;
- provider IDs do not define Person/Account/Asset/target identity;
- Subject, Person, Actor role, source, observer, recorder, transformer, confirmer, Account/Principal context and authority may differ;
- target visibility does not imply full Provenance visibility;
- Provenance access does not imply access to every private upstream payload or identity linkage;
- retention/history does not justify indefinite retention of deleted sensitive payloads;
- material lineage, not maximal recursive lineage, is the default;
- no universal provenance/actor graph or table is pre-approved.

Typical UI: Source, Imported from…, Entered by…, Corrected by…, Derived from…, Suggested by LifeOS AI, Why does LifeOS show this?, View history.

---

# 6A. Canonical Data / Subjects concepts

## Quantity

**Status:** CANONICAL VALUE SEMANTICS  
**Source:** `concepts/quantity.md`  
**Validation:** `checkpoints/quantity-v0-validation.md` — PASS WITH HARDENING  
**Question:** What scalar amount is represented, and under which unit semantics can it be interpreted?  
**UI exposure:** HIDDEN / CONTEXTUAL

Quantity is reusable scalar amount value semantics: numerical magnitude + unit semantics sufficient for interpretation. It is not an independently persistent domain entity.

```text
number != Quantity by default
Quantity != Observation
Quantity != universal RegisterEntry
property / quantity kind != unit
compatible unit != semantic equivalence by itself
same unit != universal aggregation permission
Quantity != Range / Threshold / comparator / criterion
```

Core guardrails:

- no independent Subject/property/time/Provenance/Confirmation/Evidence/ownership/history;
- unit/dimensional compatibility alone does not establish domain-semantic interchangeability;
- normalization/display conversion does not rewrite source representation;
- actor-specific display unit preference does not duplicate canonical facts;
- custom unit label does not create a global conversion rule;
- Money/MonetaryAmount is not pre-collapsed into ordinary Quantity;
- calendar-relative time is not pre-collapsed into fixed elapsed Quantity arithmetic;
- precision/rounding must not be silently fabricated;
- Quantity semantics do not imply a standalone SQL table/entity.

Typical UI does not expose `Quantity` as a noun; users see values such as `66.4 kg`, `5 km`, `45 min` in the relevant context.

## Subject

**Status:** CANONICAL SEMANTIC ROLE / RELATIONSHIP CAPABILITY  
**Source:** `concepts/subject.md`  
**Validation:** `checkpoints/subject-v0-validation.md` — PASS WITH HARDENING  
**Question:** Who or what is this descriptive record primarily about?  
**UI exposure:** HIDDEN / CONTEXTUAL

Subject is not an independent entity. A native referent such as a Person, Asset, Event, Device, Location or another eligible native concept plays Subject role in context and retains its own identity.

```text
Subject entity/root = rejected
Subject != Person
Subject != Actor
Subject != Account/Principal
Subject != Asset
Subject != Resource
Subject != observer/recorder/source/transformer
Subject != authority/visibility/owner
Subject != generic related_to
```

Core guardrails:

- current Account holder is not the universal kernel-level Subject default;
- non-LifeOS people and non-person referents may play Subject role;
- accepted Asset v0 may play Subject role without identity collapse;
- Resource v0 remains independent operational eligibility/capacity semantics;
- unknown/later-resolved/corrected Subject attribution preserves material history;
- Subject association itself may be private;
- AI may propose native-referent resolution but does not automatically establish identity/authority;
- focus/context/participant/source/etc. remain distinct where they answer different questions;
- no universal `subjects` table or inheritance root is pre-approved.

Typical UI usually shows the referent's natural name/context (`Maria`, `Sony A7 IV`) or hides self-Subject entirely rather than exposing `Subject` as a noun.

## Person

**Status:** CANONICAL NATIVE ENTITY  
**Source:** `concepts/person.md`  
**Validation:** `checkpoints/person-actor-account-v0-validation.md` — PASS WITH HARDENING  
**Question:** Which human individual is represented?  
**UI exposure:** DIRECT / CONTEXTUAL

Person is the persistent native representation of a human individual in LifeOS reality. Person identity is independent of Accounts, credentials, contact/profile representations and contextual roles.

```text
Person != Subject
Person != Actor
Person != Resource
Person != Account
Person != Principal
Person != User
Person != Asset
Person may play Subject role
Person may play Actor/specific action roles
Person may play Resource role
Person may play Participant role
non-account Person is ordinary domain reality
```

Core guardrails:

- Person identity is not derived from name/email/phone/provider IDs;
- Account creation/deletion does not automatically create/delete Person;
- external/contact/profile representations may be identity evidence but not automatic equality;
- Resource role does not replace Performer/Participant/Responsibility;
- Participation does not create another Person identity;
- Person merge/split/reconciliation must preserve material history;
- identity linkage itself may be private;
- AI can propose identity/resource matching but does not silently establish Person identity, Participation or allocation.

## Actor

**Status:** CANONICAL SEMANTIC AGENCY ROLE / CAPABILITY  
**Source:** `concepts/actor.md`  
**Validation:** `checkpoints/person-actor-account-v0-validation.md` plus `checkpoints/data-subjects-v0.md`  
**Question:** What native referent or system is acting in this context?  
**UI exposure:** HIDDEN; expose specific action-role labels instead

Actor is contextual agency semantics over a native Person/system/etc. identity. It is not an independent entity/root and does not replace specific roles.

```text
Actor entity/root = rejected
Actor != Person
Actor != Subject
Actor != Resource
Actor != Account
Actor != Principal
Actor != Responsibility
Actor != Participation
Actor != Authority
Actor != specific performer/recorder/observer/confirmer/proposer relation
```

Core guardrails:

- **specific-role precedence:** use `performed_by`, `recorded_by`, `observed_by`, `confirmed_by`, `proposed_by`, `responsible_for`, Participant/Participation, etc. when known;
- Actor is a shared agency category/capability, not a semantic-free generic persisted edge;
- Person may play Actor role, but Actor need not be Person;
- no Account is required for historical Actor/Responsibility/Participation attribution;
- Account authentication does not automatically establish semantic Actor;
- response Actor may differ from the participant whose response is being recorded;
- agency does not imply Resource eligibility, permission, responsibility, participation or Authority;
- AI/software may be Actors when domain-material agency exists, but technical processes are not automatically domain Actors;
- no universal `actors` table/root is pre-approved.

## Account boundary

**Status:** CONCEPTUAL BOUNDARY ACCEPTED; DETAILED MODEL DEFERRED  
**Validation:** `checkpoints/person-actor-account-v0-validation.md`  
**Question:** Through which platform/access identity is LifeOS usage authenticated/managed?  
**UI exposure:** DIRECT in account/settings/security contexts

```text
Account != Person
Account != Actor
Account != Subject
Account != Participant
Account != Principal by default
Account creation/deletion != human creation/deletion
```

Exact Account/credential/provider/authentication schema belongs to later logical/security design. No standalone `account.md` is pre-approved by this boundary decision.

## Asset

**Status:** CANONICAL NATIVE ENTITY — CURRENT SCOPED BASELINE  
**Source:** `concepts/asset.md`  
**Validation:** `checkpoints/asset-v0-validation.md` + Cluster-4 terminology-neutral review  
**Question:** Which individually tracked non-human physical object is this, where its distinct identity and management history materially matter?  
**UI exposure:** DIRECT / CONTEXTUAL through natural profiles

Current baseline:

> A persistent native representation of an individually tracked non-human physical object whose distinct identity and management history materially matter within LifeOS.

```text
Asset != Person
Asset != Subject
Asset != Resource
Asset != owner/holder/custodian/steward
Asset != model/product definition
Asset != every physical item
Asset != every managed thing
Asset != financial asset semantics
universal ManagedObject root = rejected
```

Core guardrails:

- individual identity must materially matter;
- physical thing != Asset automatically;
- managed thing != Asset automatically;
- Asset may play Subject role and Resource role without identity collapse;
- ownership/possession/location/state do not define Asset identity;
- provider/serial/VIN/MAC/barcode identifiers are reconciliation evidence, not automatic canonical identity;
- fungible stock does not require one Asset per unit;
- living things, Documents, FinancialAccounts and services are not absorbed by default;
- no universal Asset status or history-entry wrapper is pre-approved;
- terminology-neutral review completed: universal ManagedObject rejected under current evidence;
- exact noun `Asset` remains non-semantic/reopenable.

Typical UI: My car, Sony A7 IV, Laptop, Bike, Equipment, Gear, Appliance, depending on product context. The word `Asset` itself need not appear.

## Resource

**Status:** CANONICAL SEMANTIC PLANNING / EXECUTION ROLE-CAPABILITY — NOT ENTITY/ROOT  
**Source:** `concepts/resource.md`  
**Validation:** `checkpoints/resource-v0-validation.md` + `checkpoints/data-subjects-v0.md`  
**Question:** What could provide what this execution context needs?  
**UI exposure:** HIDDEN / CONTEXTUAL through natural provider labels

Resource is contextual operational eligibility/capability over a native referent, service, pool, supply, or other eligible provider. **Resource does not manufacture identity**: each provider retains whatever native identity, value, pool, supply, service, or other semantics it independently has.

```text
Resource entity/root = rejected
Resource != Person
Resource != Asset
Resource != Subject
Resource != Actor
Resource != Requirement
Resource != candidate set
Resource != Allocation
Resource != Reservation / Capacity Claim
Resource != actual use / consumption
Resource != Responsibility / Performer / Participant / Participation
```

Core guardrails:

- Person may play Resource and Participant roles independently without identity collapse;
- Asset may play Resource role without losing Asset identity;
- future Place/service/pool/supply may play Resource role where independently justified;
- consumable supply does not require per-unit or per-quantity identity;
- eligibility is contextual to a Requirement;
- a schedulable Resource is only the subset where time-dependent Availability/Capacity matters;
- Requirement may remain abstract before concrete allocation;
- reserved/allocated Resource does not prove actual use, Responsibility or Participation;
- provider `resource attendee` vocabulary does not make a room/equipment item a LifeOS Participant;
- Money/Budget are not Resource by default;
- Resource role grants no ownership, Responsibility, Participation, Authority, Visibility or consent;
- no universal `resources` table/root or generic `resource_id` relation is pre-approved.

Typical UI: Camera, Equipment, Room, Person name, Service, `Who's available?`, `Required equipment`, depending on context.

---

# 7. Product/profile terms that are not independent kernel primitives

## Task

**Status:** PRODUCT / UI TERM  
**Maps to:** Activity

## Project

**Status:** PRODUCT PROFILE / HISTORICAL KERNEL TERM  
**Current mapping:** Plan profile optionally related to Goals, Milestones, Activities, Events and dependencies.

## Program

**Status:** PRODUCT PROFILE / HISTORICAL KERNEL TERM  
**Current mapping:** Plan profile emphasizing progression, stages, repeated policies, reviews or adaptation.

## Register / Tracker / History / Progress

**Status:** PRODUCT / UI CAPABILITY TERM — KERNEL CANDIDATE REJECTED  
**Validation:** `checkpoints/register-v0-validation.md`

Longitudinal tracking, filtering, trend analysis, valid aggregation, drill-down and quick capture are validated product needs. They operate over native semantic records rather than requiring a universal `Register` source-of-truth entity or `RegisterEntry` wrapper.

```text
native semantic records
        ↓
query / filtering / grouping
        ↓
valid aggregate / trend / comparison
        ↓
Register / Tracker / History / Progress UI
```

A saved tracker/view may later be persisted as application/product configuration. Persisted configuration does not automatically become independent domain truth.

```text
Register UI != kernel Register primitive
RegisterEntry universal primitive = rejected
changing/deleting saved view != changing/deleting source records
same source record may appear in multiple views without duplication
```

## Calendar Block

**Status:** PRODUCT / UI TERM  
**Current mapping:** calendar-shaped representation over Schedule/Capacity/Availability semantics depending on purpose.

## Deadline

**Status:** PRODUCT/UI TERM + semantic specialization  
**Maps to:** latest-bound Temporal Constraint.

## Window

**Status:** RANGE SHAPE / PRODUCT TERM

Interval geometry does not determine semantic meaning.

## Repeat

**Status:** UI TERM  
**Maps to:** Recurrence configuration where recurrence semantics are intended.

## Busy / Free

**Status:** UI / DERIVED TERM  
**Maps to:** projections of Availability + Capacity + claims + compatibility.

## User

**Status:** PRODUCT / IMPLEMENTATION TERM — NOT DOMAIN PRIMITIVE

May refer contextually to a current Account holder/person using LifeOS, but must not become the common domain root for Person, Actor, Account, Principal, Participant or Subject.

## Invitation / Attendance

**Status:** PRODUCT / WORKFLOW LANGUAGE OVER PARTICIPATION SEMANTICS — NOT UNIVERSAL PRIMITIVES

```text
Invitation
= proposal/request for intended Participation

Attendance
= Event-facing Actual Participation semantics
```

Neither implies a standalone kernel entity/table.

---

# 8. Historical V1 vocabulary crosswalk

## Planning Item

**Status:** HISTORICAL / PRODUCT ABSTRACTION

No universal Planning Item kernel primitive is accepted.

## Reminder

**Status:** PRODUCT CAPABILITY / DOMAIN REVIEW DEFERRED

Reminder is not automatically Activity. Reminder/Trigger/notification semantics require dedicated review.

## Calendar / Life Area

**Status:** PRODUCT ORGANIZATION CONTEXT — dedicated domain status not yet reviewed

Organization/filtering context does not automatically establish ownership, Goal semantics or sharing scope.

## Module

**Status:** PRODUCT/ARCHITECTURE TERM, NOT DOMAIN PRIMITIVE

Examples: training, nutrition, learning, travel, finance, creative work.

## Tag

**Status:** PRODUCT METADATA TERM — exact persistence deferred

Tag must not establish ownership, authority, lifecycle, scheduling or canonical hierarchy.

## Person-related commitment

**Status:** HISTORICAL PRODUCT PHRASE

Current mapping usually uses Activity/Event + Person + specific Responsibility/Participation/etc. semantics where needed. The other Person does not need a LifeOS Account and the item is not automatically shared.

## Asset / Soggetto

**Status:** HISTORICAL COMBINED TERM — SUPERSEDED

The old grouping of `auto, casa, attrezzo, animale, pianta, conto, documento, persona` is not canonical.

Current decomposition includes at minimum:

```text
Person   -> native human identity
Subject  -> contextual aboutness role
Asset    -> current scoped individually tracked non-human physical-object identity
Resource -> contextual planning/execution role over independently justified provider semantics
```

Other referents are modeled only when their own semantics justify them. The terminology-neutral review found no reason to replace this with a universal ManagedObject root.

## Shared Item

**Status:** PRODUCT PHRASE, NOT UNIVERSAL PRIMITIVE

```text
shared canonical object
+
actor-scoped state/personal overlay
```

## Source

**Status:** PRODUCT / PROVENANCE TERM  
**Maps to:** one dimension of Provenance.

```text
Source != Provenance
Source != truth
Source != Authority
Source != Person/Actor/Account/Asset identity
```

## Temporary Mode

**Status:** PROVISIONAL CROSS-CUTTING CONCEPT

Time-bounded context/policy changing planning/availability/capacity behavior without rewriting stable baseline.

## Inbox Item

**Status:** PRODUCT CAPTURE STATE/PROFILE, NOT YET KERNEL PRIMITIVE

Captured information awaiting classification.

## Decision Record

**Status:** PRODUCT/HISTORICAL TERM -> FUTURE `Decision` REVIEW

Final Decision/Version semantics belong to Relationships/Reasoning review.

---

# 9. Multi-actor terminology

## Person

**Status:** CANONICAL NATIVE ENTITY  
**See:** `concepts/person.md`

Persistent human identity independent of Account, Subject role, Actor role, Resource role, Participation, Responsibility, Authority and Visibility.

```text
Person != Account
Person != Subject
Person != Actor
Person != Resource
Person != Participant
Person != Principal
Person != Asset
```

A Person may exist without ever having a LifeOS Account and may independently play Resource, Actor, Subject, Participant or Responsibility-holder roles where appropriate.

## Actor

**Status:** CANONICAL SEMANTIC AGENCY ROLE / CAPABILITY  
**See:** `concepts/actor.md`

Contextual agency of a native referent/system. Do not equate Actor with `users.id`, create a universal Actor wrapper/root, or replace specific roles with one generic `actor` edge.

```text
Actor != Person
Actor != Account
Actor != Principal
Actor != Subject
Actor != Resource
Actor != Responsibility
Actor != Participation
Actor != Authority
```

Use specific roles such as performer/recorder/observer/confirmer/proposer/responsible actor/participant when those semantics matter.

## Account

**Status:** PLATFORM / ACCESS IDENTITY BOUNDARY ACCEPTED; DETAILED MODEL DEFERRED

```text
Account != Person
Account != Actor
Account != Subject
Account != Participant
Account != Principal by default
```

Account lifecycle must not automatically erase native Person identity or historical Actor/Responsibility/Participation attribution.

## Principal

**Status:** DEFERRED TECHNICAL/AUTHORITY CONCEPT

Authenticated/authorized security identity semantics remain open.

```text
Principal != Person
Principal != Actor
Principal != Account by default
```

## Participant / Participation

**Status:** CANONICAL SPECIFIC SEMANTIC RELATION FAMILY  
**Source:** `concepts/participation.md`  
**Validation:** `checkpoints/participation-v0-validation.md` — PASS WITH HARDENING  
**Question:** Who is expected/intended to be involved, or who actually participated, in this bounded shared occurrence/interaction?  
**UI exposure:** CONTEXTUAL; Going / Maybe / Can't go / Attended / participant list where useful

Participant is a contextual role over native identity. Participation contains distinct intended/response and Actual involvement semantics; it is not a Person/Actor/Account subtype or universal membership root.

```text
Participant != Person identity subtype
Participation != Responsibility
Participation != Performer
Participation != Resource
Participation != Organizer/requester
Participation != Authority
Participation != Visibility
Participation != Session
shared Event Actual != identical actor-specific Actual Participation

Invitation != Acceptance
Participation response != Actual Participation
accepted != attended
declined != proved absent
no response != declined
no attendance evidence != proved absence
```

A response Actor/Account/Principal may differ from the participant whose involvement is at stake. Provider attendance telemetry remains evidence/provenance until applicable reconciliation semantics establish current Participation truth.

## Responsibility

**Status:** CANONICAL SPECIFIC SEMANTIC RELATION FAMILY  
**Source:** `concepts/responsibility.md`  
**Validation:** `checkpoints/responsibility-v0-validation.md` — PASS WITH HARDENING  
**Question:** Who is accountable for ensuring this bounded commitment is appropriately handled?  
**UI exposure:** CONTEXTUAL; often `Responsible`, `Assigned to`, natural person/role label

```text
Responsibility != Actor identity/category
Responsibility != requester
Responsibility != expected performer
Responsibility != actual performer
Responsibility != Participation
Responsibility != Resource
Responsibility != Authority
Responsibility != Visibility
Responsibility != ownership/custody
Responsibility != coordination Stewardship
unknown holder != explicitly open/unassigned
```

Simple cases may use a direct specific `responsible_for` relation. Rich/open/transfer/history cases may require a specific qualified Responsibility context. Qualified structure does not automatically imply independent entity identity.

## Assignment

**Status:** CANONICAL OPERATION SEMANTICS — NOT STANDALONE UNIVERSAL PRIMITIVE

Assignment establishes/changes a **specific named role**. `Assignment` without the role is semantically incomplete.

```text
assign Responsibility
assign expected performer
assign reviewer
```

Whether Assignment immediately makes the role effective depends on policy/Authority/Acceptance semantics.

## Claim

**Status:** CANONICAL OPERATION SEMANTICS — NOT STANDALONE UNIVERSAL PRIMITIVE

Self-initiated attempt/action to acquire a specific role. Whether the role becomes effective immediately is policy-dependent.

Do not confuse **Responsibility Claim** with a Resource **Capacity Claim / Reservation** merely because the same English word is used.

## Hand-off

**Status:** CANONICAL TRANSFER-WORKFLOW SEMANTICS — NOT STANDALONE UNIVERSAL PRIMITIVE

Hand-off transfers/proposes transfer of a specific named role. A request does not universally establish effective transfer.

```text
hand-off request != effective Responsibility transfer by default
```

## Stewardship / Coordination Responsibility

**Status:** DISTINCT SEMANTIC DIMENSION — STANDALONE PRIMITIVE SAFE DEFERRED

Execution Responsibility can move while anticipation, reminding, monitoring and repair burden remain elsewhere.

```text
Responsibility != coordination Stewardship
Assignment != Stewardship transfer
```

## Performer

**Status:** SPECIFIC ACTOR ROLE — exact logical representation deferred

Who actually performed work; not automatically requester/responsible actor/planned expected performer. Performer is a specific Actor role, not Actor, Participant or Resource identity.

## Subject

**Status:** CANONICAL SEMANTIC ROLE  
**See:** `concepts/subject.md`

Who/what a descriptive record primarily concerns. The native referent retains its identity; Subject is not an entity/root.

## Asset

**Status:** CANONICAL NATIVE ENTITY — CURRENT SCOPED BASELINE  
**See:** `concepts/asset.md`

One individually tracked non-human physical object whose identity/history materially matter. Asset may play Subject or Resource roles, but ownership, holder, stewardship, Authority and Visibility are separate. The exact noun `Asset` is not semantically mandatory.

## Resource

**Status:** CANONICAL SEMANTIC PLANNING / EXECUTION ROLE-CAPABILITY  
**See:** `concepts/resource.md`

Operational eligibility/capacity of an independently meaningful provider to satisfy an execution Requirement.

```text
Resource entity/root = rejected
Person may play Resource role
Asset may play Resource role
Actor != Resource
Subject != Resource
Asset != Resource
Resource != Requirement
Resource != Allocation
Resource != Reservation
Resource != actual use
Resource != Responsibility/Performer/Participation
```

Resource may also apply to supplies/pools without manufacturing identity for them. Resource reservation/candidacy does not establish Participation.

## Owner / Governor / Steward

**Status:** DEFERRED RELATIONSHIP/AUTHORITY SEMANTICS

Do not use as synonyms for creator, Account holder, participant, viewer, responsible actor, performer, Person, Subject, Resource or Asset identity.

## Authority

**Status:** DEFERRED — STRONG CROSS-CUTTING DIMENSION

Who/what may establish, approve, change or override canonical state in context.

```text
Authority != Visibility
Authority != Confirmation
Authority != Provenance/source
Authority != Subject
Authority != Actor
Authority != Resource
Authority != Responsibility
Authority != Participation
Authority != Account
Authority != Asset ownership by default
```

## Visibility / Access

**Status:** DEFERRED

What an Actor/Principal/Account context may inspect/receive/use. Current access and historical Person/Actor/Asset/Responsibility/Participation attribution are distinct. Being Subject, Resource candidate, participant, owner or responsible actor does not automatically grant visibility.

## Acknowledgement

**Status:** PROVISIONAL / DEFERRED

Grounding/receipt/recognition semantics where consequence requires them.

```text
Acknowledgement != Confirmation
Acknowledgement != Acceptance
Acknowledgement != Participation response by default
```

## Acceptance / Agreement

**Status:** PROVISIONAL / DEFERRED

Willingness/proposal/responsibility/participation semantics.

```text
Acceptance != Confirmation
Acceptance != Actual
Assignment != Acceptance by default
Claim != Acceptance by default
hand-off request != Acceptance by default
Participation response may express contextual willingness without defining a universal Acceptance primitive
```

---

# 10. Deferred neighboring semantics

## Verification

**Status:** DEFERRED

Process/basis used to check a claim or record.

```text
Verification != Confirmation
Verification != Provenance
```

## Longitudinal query / aggregation / saved-view implementation

**Status:** PRODUCT + LOGICAL/PHYSICAL MODEL DEFERRED

The required product capability is validated, but exact query DSL, aggregate materialization, cache/history policy and saved-view persistence are implementation/product concerns rather than a kernel `Register` primitive.

## Account / Principal / credential security model

**Status:** DEFERRED LOGICAL / SECURITY MODEL

The conceptual boundary is fixed:

```text
Person != Account
Actor != Account
Account != Principal by default
```

Exact login-provider identities, credentials, account linking, service principals, delegation and authentication/authorization representation remain open.

## Resource Requirement / Allocation / Reservation

**Status:** SAFE DEFERRED — RELATIONSHIPS / PLANNING LOGICAL MODEL

Resource v0 fixes the separation:

```text
Requirement
what is needed
        ↓
Candidate
what could satisfy it
        ↓
Allocation
what is selected
        ↓
Reservation / Capacity Claim
what capacity is held
        ↓
Actual use / consumption
what was really used
```

The exact identity/cardinality/persistence of these structures remains deferred. None implies Responsibility or Participation.

## Asset scope / managed-referent taxonomy

**Status:** RESOLVED AT CURRENT CLUSTER-4 BASELINE — REOPENABLE WITH STRONGER EVIDENCE

The terminology-neutral review was completed across managed/tracked-referent product families.

Current result:

```text
universal ManagedObject root  REJECTED
physical-object identity      RETAINED
exact noun `Asset`            NON-SEMANTIC / reopenable
```

Future Place/Property, living, Document, FinancialAccount, and service workflows remain independently SAFE DEFERRED; they do not become primitives until concrete evidence justifies them.

## Version

**Status:** DEFERRED — RELATIONSHIPS/REASONING REVIEW

Material version identity/history must later integrate with Confirmation, Evidence, Provenance, Responsibility/Participation history and Subject/Person/Asset attribution correction without replacing them.

## Decision

**Status:** DEFERRED — RELATIONSHIPS/REASONING REVIEW

Decision rationale/authority is distinct from Provenance lineage and may be needed for contested/effective Responsibility or Participation reconciliation.

---

# 11. Other high-value relationship terms

## Trigger

**Status:** DEFERRED

```text
Trigger != Recurrence
Trigger != Routine
fallback/conditional Responsibility != current Responsibility
```

## Relationship

**Status:** CANONICAL MODELING CAPABILITY / SEMANTIC RULE — NOT ENTITY/ROOT  
**Validation:** `checkpoints/relationship-v0-validation.md` — PASS WITH HARDENING

LifeOS uses the most specific truthful relation semantics. A semantically complete simple connection may remain direct. A relationship that itself has materially relevant state, lifecycle, history, temporal scope, authority, provenance, privacy, actor-scoped state or domain invariants may become a **specific qualified relation family**.

```text
universal Relationship entity/root = rejected
semantic-free related_to as kernel truth = rejected
specific relation semantics > generic edge
qualified relation != entity automatically
queryability/cardinality/database row id != domain identity
orientation/symmetry/transitivity/inverse rules are relation-family-specific
```

Responsibility and Participation are the first two major successful stresses of this rule: simple relations may remain direct, while material state/history/privacy/actuality can justify specific qualified relation contexts.

A future generic Personal Knowledge link capability is separately SAFE DEFERRED and must not silently become Responsibility, Authority, Evidence, Participation, allocation or Actual semantics.

## Dependency

**Status:** DEFERRED / likely specific relationship family or typed semantic

Represents coordination dependency where justified. Exact directionality, history, waiver, lag and reasoning/transitivity rules require dedicated review rather than inheritance from `Relationship` generally.

---

# 12. Frequently confused terms

## Core

```text
Goal != Plan
Goal != Milestone
Plan != Activity
Plan != Routine
Activity != Event
Activity != Session
Event != Schedule
Event != Participation response
Event != Actual Participation/attendance
Event identity != participant set/state
Routine != Recurrence
Routine != observed habit
Occurrence != Schedule
Occurrence != Session
Schedule != Temporal Constraint
Schedule != Availability
Schedule != Capacity Reservation
Schedule != Session/Actual
Schedule acceptance != Participation response
Session != Actual
Session != Participation/attendance by default
Actual != Outcome
Actual != Observation
Actual != Confirmation
Actual != Evidence
Actual != Provenance
shared Actual != identical actor-specific Actual Participation
reported/asserted reality != established Actual
Outcome != lifecycle/operational state
Outcome != Observation
Outcome != Confirmation
Outcome != Provenance
Outcome != Evidence
Milestone attainment != independent duplicate Actual/Outcome/Observation truth
Observation != Quantity
Observation != universal RegisterEntry
Observation != Confirmation
Observation != Evidence
Observation != Provenance
Quantity != Observation
Quantity != universal RegisterEntry
number != Quantity by default
property/quantity-kind != unit
compatible unit != semantic equivalence by itself
same unit != universal aggregation permission
Quantity != Range/Threshold/comparator/criterion
Subject != Person/Actor/Account/Principal/Asset/Resource
Subject != observer/recorder/source/transformer/authority/viewer
Subject role != Subject entity/root
Subject != generic related_to
Person != Actor
Person != Resource
Person != Participant
Person != Account
Person != Principal
Person != User domain primitive
Person != Asset
Actor != Resource
Actor != Account
Actor != Principal
Actor != Responsibility
Actor != Participation
Actor != Authority
Actor role != Actor entity/root
generic actor relation != specific action role
Account != Person/Actor/Subject/Participant
User != universal domain root
Asset != Subject
Asset != Resource
Asset != Person
Asset identity != owner/holder/steward
Asset instance != product/model definition
physical thing != Asset automatically
managed thing != Asset automatically
universal ManagedObject root = rejected
financial asset semantics != Asset entity
Resource role != Resource entity/root
Resource != Requirement
Resource != candidate set
Resource != Allocation
Resource != Reservation/Capacity Claim
Resource != actual use/consumption
Resource != Responsibility/Performer/Participant/Participation
Resource role != synthetic provider identity
Resource reservation != Participation
Money/Budget != Resource by default
Responsibility != requester
Responsibility != expected performer
Responsibility != actual performer
Responsibility != Participation
Responsibility != Resource
Responsibility != Authority
Responsibility != Visibility
Responsibility != Stewardship
unknown responsibility != explicitly open/unassigned
Assignment != standalone universal primitive
Claim != standalone universal primitive
Hand-off != standalone universal primitive
Assignment/Claim/Hand-off must identify specific role
hand-off request != effective transfer by default
Participation != Responsibility/Performer/Resource/Organizer/Authority/Visibility/Session
Participant != identity/entity
Invitation != Acceptance/Actual Participation
Participation response != Actual Participation
accepted != attended
declined != proved absent
no response != declined
no attendance evidence != proved absence
Attendance != standalone universal primitive
universal Relationship root = rejected
semantic-free related_to as kernel truth = rejected
specific relation semantics != generic Relationship wrapper
qualified relation structure != independent entity automatically
queryability/cardinality != domain identity
Register/Tracker UI != kernel Register primitive
saved longitudinal view != source of truth
view membership != duplicate native record
Confirmation != Acknowledgement
Confirmation != Acceptance/Agreement
Confirmation != Verification
Confirmation != Authority
Confirmation != Provenance
Evidence != source information
Evidence != Provenance
Evidence != GoalCriterion
Provenance != Source
Provenance != truth
Provenance != Authority
Provenance != Version
Provenance != Audit
missing Observation != observed negative
no Confirmation != false/rejected/incorrect
no Evidence != Evidence against
recorded time != Observation effective time
Temporal Constraint != Availability
Recurrence != Trigger
Availability != empty-gap cache
Capacity != universal busy/free boolean
```

## Multi-actor

```text
Person != Account
Person may exist without Account
Person may play Subject role
Person may play Actor/specific action role
Person may play Resource role
Person may play Participant role
Actor != Account
Actor != Principal
Actor != Subject
Actor != Resource
Actor != Responsibility/Participation/Authority
Account != Participant
Subject != Resource
Asset != owner
Asset owner != holder/custodian/steward
Asset ownership != Authority/Visibility
Asset may play Subject role
Asset may play Resource role
Resource candidacy != Responsibility/Participation/consent/allocation Authority
Participant != Responsible actor
Participant != Performer by default
Organizer != Participant by default
Responsible actor != expected performer
Responsible actor != actual performer
expected performer != actual performer
Creator != Owner/Governor
Visibility != Authority
Sharing != ownership
Assignment != Activity identity
Assignment != Acceptance by default
Claim != effective Responsibility by default
hand-off request != effective role transfer by default
Responsibility transfer != Activity replacement
Responsibility != coordination Stewardship
Participation response != Actual Participation
accepted != attended
declined != proved absent
no response != declined
no attendance evidence != proved absence
shared Actual != identical actor Participation
shared Outcome != identical actor consequence
shared Asset != identical actor visibility/private overlays
Observation Subject != observer/recorder/source/authority/viewer
current Account != universal Subject
current Account != semantic Actor automatically
non-LifeOS Person may be Subject/Participant/Actor/Resource candidate/Responsibility holder where context allows
response Actor != participant identity by default
Confirmation by A != Confirmation by B
conflicting Observation != automatic overwrite/average
conflicting Confirmation != automatic canonical truth
provider attendance telemetry != canonical Participation automatically
source actor != recorder != Subject by default
Schedule acceptance != Participation acceptance/response
Delivery != acknowledgement
Acknowledgement != agreement
Agreement != authority
Authority != Actual
Authority != Confirmation
Authority != Responsibility
Authority != Participation
Actor action != Authority
relation existence/type != Authority
relation existence/type != Visibility
AI knowledge != disclosure permission
AI inference != Confirmation
AI inference != established Actual
AI inferred relation != established relationship
AI Responsibility suggestion != effective assignment/transfer
AI Participation inference != established response/attendance
AI Subject/Person/Asset guess != established identity
AI Resource match != authoritative allocation
AI Actor != human author/authority automatically
AI provenance != disclosure permission
future Account access revocation != deletion of historical Person/Actor/Responsibility/Participation attribution
Quantity display preference != canonical value mutation
actor tracker preferences != shared fact mutation
```

## Product vs kernel

```text
Task != separate Activity primitive
Project != currently separate Plan primitive
Program != currently separate Plan primitive
Calendar Block != mandatory time primitive
Planning Item != current universal kernel root
Shared Item != universal collaboration primitive
Module != domain entity
Register/Tracker view != kernel Register entity
RegisterEntry != universal semantic record
Subject UI/context != Subject entity
Actor UI label != Actor entity
Resource UI label != Resource entity
Relationship UI/link != universal Relationship entity
Participant UI label != Participant entity/root
Invitation UI/workflow != universal Invitation entity
Attendance UI != universal Attendance entity
Assigned-to UI != universal Assignment entity
Claim UI action != universal Claim entity
Hand-off UI action != universal HandOff entity
User UI/implementation term != universal domain entity
Account settings object != Person identity
Asset UI profile != new Asset subtype primitive automatically
Inventory UI != every unit is Asset
Gear/Device UI label != broader Asset kernel semantics
Needs confirmation != Confirmation object by itself
Source label != complete Provenance model
Quantity UI value != standalone Quantity entity
```

---

# 13. Domain -> Product -> UI examples

## Buy milk

```text
Domain: Activity
Product/UI: Task / Buy milk
```

Simple personal policy may hide Responsibility entirely or show `Assigned to me`; the underlying Activity identity does not depend on Account coincidence.

## Open household chore

```text
Activity
Take recycling out

Responsibility
explicitly open / claimable
```

This is not the same as unknown Responsibility data.

## Responsibility hand-off

```text
Activity
Pick up prescription

current responsible
Luca

hand-off request
Luca -> Anna

pending
Luca remains current holder unless policy/Authority makes transfer effective
```

## Shared dinner participation

```text
Event
Dinner · Saturday 21:00

Anna
invited → accepted
Actual Participation: attended

Luca
invited → declined
Actual Participation: unknown / established absent only if evidence supports it

Marco
not invited
Actual Participation: attended
```

Earlier response history is not rewritten to match later reality.

## Partial meeting attendance

```text
Event Actual
meeting occurred 10:00–12:00

Anna Actual Participation
10:00–12:00

Luca Actual Participation
10:35–11:10
```

No one-Session-per-attendee model is implied.

## Gym 3x/week

```text
Routine + Recurrence + Occurrences + optional Schedules
UI: Gym — 3 times per week
```

## Website redesign

```text
Goal optional + Plan + Activities + Events + Milestones
Product: Project
```

## Exam result

```text
Person student
+ Subject role on Observation
+ Event
+ Actual
+ Observation: score = 78/100
+ Outcome: passed
+ optional Confirmation
+ Evidence use toward Goal/Milestone
+ Provenance of imported/recorded result
```

UI may show simply `78/100 · Passed`, with source/evidence/history on demand.

## Weight history

```text
Person P17
        ↑ Subject role
Observation O1: body weight = Quantity(66.8 kg)
Observation O2: body weight = Quantity(66.5 kg)
Observation O3: body weight = Quantity(66.4 kg)
        ↓
query / trend projection
        ↓
UI: Weight / History / Tracker / Progress
```

No universal Subject wrapper or RegisterEntry copy is created.

## Camera history

```text
Asset A17 = specific Sony A7 IV body
        ↑ Subject role
Observation: shutter count = 32,411
Observation: battery health = 87%
        ↓
query / history projection
UI: Sony A7 IV / History
```

The camera is one Asset identity; the Observations do not become Asset fields merely because the UI groups them.

## Camera required for a shoot

```text
Activity: photo shoot

Resource Requirement
camera suitable for wildlife photography

Candidates
Asset A17
Asset A18

Allocation
A17 selected

Reservation
A17 17:00–20:00
```

Asset identity, Resource role, Requirement, Allocation, Reservation and Responsibility remain distinct.

## Consumable requirement

```text
Maintenance
Requirement: 500 ml oil
```

The supply may satisfy Resource semantics without becoming an identity-bearing Resource entity.

## Person required by capability

```text
Requirement
Japanese B2+

Candidates
Person Anna
Person Luca
```

The people retain Person identity. Resource candidacy does not establish Responsibility, Participation or Performer status.

## Company laptop

```text
Asset L1
owner = Company
holder = Person Mattia
maintenance responsibility = IT
coordination Stewardship = possibly Anna
actual repair performer = Technician
```

One Asset identity; ownership, possession, Responsibility, Stewardship and performer are separate semantics.

## Caregiver measurement

```text
Person Maria
        ↑ Subject role
Observation: temperature = 38.2 °C

Person Anna
        ↓ observer/recorder Actor roles

Account Anna-A1
        ↓ authenticates LifeOS access
```

Person, Subject, Actor role and Account remain distinct.

## External participant/responsible Person with no Account

```text
Person Dr. Rossi
Event Participant / possible Responsibility holder in relevant context
no LifeOS Account required
```

If Dr. Rossi later creates an Account, the human Person identity and historical roles do not need to be recreated.

## AI proposal

```text
AI Agent X
specific role: proposer
Actor semantics

Resource matching
proposes A17 for requirement

Responsibility planning
proposes Anna as responsible

Participation planning
suggests inviting Luca

service/security identity
future Principal semantics
```

AI proposal does not become allocation Authority, Responsibility, Participation response, Acceptance or human Confirmation automatically.

## Quantity display conversion

```text
shared Observation
value: 66.4 kg

Actor A display
66.4 kg

Actor B display
146.4 lb
```

One underlying fact; no per-actor Quantity/Observation duplication.

## Correction lineage

```text
Observation v1
subject = Asset A1
value = 32,411

Observation correction
subject = Asset A2
value remains 32,411
```

Material Provenance/Version history must preserve that Asset attribution changed rather than pretending A2 was always known.

## Private availability

```text
private source context / Observation / Provenance
        ↓
authorized projection
Unavailable 18:00–20:00
```

Shared Actors do not automatically receive the private source reason, Person/Asset linkage, Actor/delegation lineage, Resource-match basis, Responsibility context, Participation state or Subject association.

---

# 14. Frontend rule

Prefer plain language, progressive disclosure and contextual actions over internal nouns when clearer.

```text
Occurrence          → This time
Temporal Constraint → Deadline / Preferred time / Not before
Actual              → What happened? / Actual time / Performed
Outcome             → Passed / Partial / Approved / Result details
Observation         → Weight / Mood / Score / Odometer / Shutter count
Quantity            → 66.4 kg / 5 km / 45 min
Subject             → usually hidden; natural referent label such as Maria / Sony A7 IV
Person              → natural human name/contact representation
Actor               → hidden; expose role: Done by / Recorded by / Suggested by
Account             → Account / Profile / Login in settings/security context
Asset               → Car / Camera / Laptop / Bike / Gear / Equipment according to context
Resource            → usually hidden; Camera / Room / Person / Service / Who's available? / Required equipment
Relationship        → usually hidden; expose the specific verb/role instead
Responsibility      → Responsible / Assigned to / Who's handling this? depending on context
Participation       → Going / Maybe / Can't go / Attended / participant list according to context
Invitation          → Invite / invited
Attendance          → Attended / Partially attended / Did not attend where established
Assignment          → Assign / Reassign action
Claim               → I'll take it / Claim action
Hand-off            → Hand off / Transfer / Ask someone else
User                → ordinary product language only where unambiguous
Register capability → History / Tracker / Progress / Register when useful
Confirmation        → Confirm / Looks correct / Needs confirmation
Evidence            → Why? / Based on… / Supporting or conflicting data
Provenance          → Source / Imported from / Corrected by / View history
```

Reverse rule:

> **A UX label does not automatically create or broaden a backend/domain type.**

---

# 15. Implementation-language rule

Physical/API terminology remains intentionally incomplete until logical/physical modeling.

Do not infer table/class names from this map.

In particular Person, Actor, Account, Asset, Principal, Participant, Responsibility, Participation, Resource, Authority, Visibility, Actual, Outcome, Observation, Confirmation, Evidence, Provenance, Quantity and Subject-role references must not be translated prematurely into final SQL/cardinality choices.

Specific guardrails:

- Observation does not imply one generic fact table or row per sensor tick;
- Confirmation does not imply one universal polymorphic confirmation table;
- Evidence does not imply one persisted edge/entity per evaluative use;
- Provenance does not imply one universal provenance/actor graph/table or event row for every technical operation;
- Quantity does not imply a standalone table/entity for each scalar amount;
- Subject does not imply a universal `subjects` table/root or every referent inheriting from Subject;
- Actor does not imply a universal `actors` table/root, generic `actor_id`, or replacement of specific action roles;
- Resource does not imply a universal `resources` table/root, generic `resource_id`, or synthetic identity for supplies/pools;
- Relationship modeling discipline does not imply a universal `relationships` table, graph edge root, Node supertype, or one polymorphic `related_to` mechanism;
- Responsibility does not imply a universal `responsibilities` table, `assigned_to` field, or independent relation identity in every simple case;
- Participation does not imply a universal `participants`/`participations` table/root, one participant-status enum, one Session per attendee, or independent relation identity in every simple case;
- Invitation/Attendance do not imply standalone universal tables/entities;
- planned/response Participation and Actual Participation must remain independently representable even if one future aggregate stores both facets;
- provider attendee/attendance records do not define canonical LifeOS Participation automatically;
- Assignment/Claim/Hand-off do not imply standalone tables/entities;
- explicitly open/unassigned Responsibility must remain distinguishable from unknown, even if SQL later uses nullable references internally;
- structured/qualified relation persistence does not by itself establish independent domain identity;
- queryability, cardinality and database row IDs do not create domain concepts;
- Resource Requirement/Allocation/Reservation remain distinct logical-model questions;
- Person does not imply `persons.id = accounts.id`;
- Account does not imply final auth/provider/credential/Principal schema;
- User must not become the universal implementation FK just because the UI uses the word;
- Asset does not imply one universal managed-things table, one table per subtype, one row per physical unit, or inheritance into Resource;
- Asset serial/provider identifiers do not define canonical Asset identity by default;
- Asset model/type/profile semantics are not fixed yet;
- heterogeneous Subject/Actor/Resource/relation references must preserve native semantics and attribution/history;
- longitudinal UI does not imply a universal `registers` + `register_entries` source-of-truth schema;
- saved tracker/view configuration may be persisted without becoming domain truth;
- unit normalization does not erase source representation/provenance;
- provider/source/auth identifiers do not define Person/Asset/domain identity by default;
- product aliases do not create duplicate persistence models.

When implementation names later differ for good technical reasons, document the mapping here.

---

# 16. Terminology change policy

A term may enter when at least one holds:

1. it is an accepted Domain Atlas concept/capability/value/role/relation semantics;
2. it is recurring product/UI language with clear mapping;
3. omitting it creates material ambiguity;
4. a demonstrated semantic need must be tracked as PROVISIONAL/DEFERRED.

A term does not become canonical because a competitor uses it, a table would be convenient, a mockup contains it, an AI suggested it, or it makes the ontology look complete.

A historical candidate may be rejected when validation shows that its useful behavior is better expressed through existing concepts plus product/query/application capability or a semantic role rather than a new entity.

An implementation/security concept may have an accepted boundary without being promoted prematurely into a fully modeled domain concept. `Account` currently follows this rule.

A terminology-neutral revisit can resolve a naming-bias concern without freezing the noun forever. Asset v0 currently follows this rule: its cross-domain semantic test is complete, while the exact word `Asset` remains renameable.

Change procedure:

1. review/change source concept or candidate first;
2. preserve historical reasoning and rejection rationale;
3. update this map;
4. update checkpoints/handoffs;
5. update implementation names only after persistence/API exists.

Do not silently recycle one term with a new meaning.

---

# 17. Cluster-status reference

Current integrated checkpoint set:

```text
Intention & Execution v0        PASS
Time v0                         PASS
Observed Reality & Evidence v0  PASS
Data / Subjects v0              PASS WITH HARDENING
Deferred Dependency Closure     PASS
Cross-Cluster Validation v4     PASS WITH HARDENING
Relationship v0 review          PASS WITH HARDENING
Responsibility v0 review        PASS WITH HARDENING
Participation v0 review         PASS WITH HARDENING
```

Current cross-cluster structural reopenings: **0**.

Normative transition/current references:

- `checkpoints/data-subjects-v0.md`;
- `checkpoints/deferred-dependency-closure-clusters-1-4-v0.md`;
- `checkpoints/cross-cluster-validation-v4.md`;
- `checkpoints/relationship-v0-validation.md`;
- `concepts/responsibility.md`;
- `checkpoints/responsibility-v0-validation.md`;
- `concepts/participation.md`;
- `checkpoints/participation-v0-validation.md`.

Relationships / Reasoning is **IN PROGRESS**. The next candidate must be reselected by dependency leverage rather than roadmap order. Responsibility and Participation now both place strong pressure on the common-ground/governance boundary — especially Authority, Visibility, Acceptance/Acknowledgement and delegation — but none of those terms is pre-accepted by this map.

---

# 18. Maintenance rule

This file is the semantic navigation layer, not a duplicate of every concept spec.

It should answer quickly:

> **What does this LifeOS term mean, what does it not mean, what status does it have, and what might a user actually see?**

Detailed lifecycle, tests, history, rejected alternatives and persistence implications remain in the authoritative concept/checkpoint documents.