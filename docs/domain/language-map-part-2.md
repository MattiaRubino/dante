<!-- LIFEOS-CANONICAL-SPLIT document="language-map.md" part="2" total="5" -->
> **Canonical document split — Part 2 of 5.** Parts 1–5 together form one authoritative document; this is a physical split only, not a summary/reference hierarchy. The payload preserves the full pre-compaction baseline first and later downstream amendments in sequence; later explicit amendments override stale status/deferral wording without deleting the earlier rationale. Navigation: [Part 1](language-map.md) · **Part 2** · [Part 3](language-map-part-3.md) · [Part 4](language-map-part-4.md) · [Part 5](language-map-part-5.md)

<!-- LIFEOS-CANONICAL-PAYLOAD -->
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

