# LifeOS Domain & Product Language Map

**Status:** Canonical terminology reference for the active Domain Atlas  
**Established:** 2026-08-11  
**Current revision:** 2026-08-11 — Observation v0 promoted after Methodology v3 validation  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

This is the fast canonical reference for LifeOS vocabulary.

It keeps four distinct languages aligned without forcing them into a one-to-one mapping:

```text
DOMAIN LANGUAGE
what a concept means canonically
        ↓
PRODUCT LANGUAGE
how LifeOS packages/presents that meaning
        ↓
UI LANGUAGE
what users actually read and manipulate
        ↓
IMPLEMENTATION LANGUAGE
API / schema / code names once designed
```

Canonical rule:

> **A domain concept does not require a dedicated visible UI object, and a visible product/UI term does not automatically justify a separate domain primitive.**

This document is a navigation/governance layer. Detailed lifecycle, invariants, history, evidence and stress tests remain in concept specs/checkpoints.

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

The old `docs/product/v1-core-domain-glossary.md` remains valuable product-history evidence. It is **not** authoritative for kernel terminology where current Domain Atlas decisions differ.

This map records accepted decisions; it must not create a primitive by terminology alone.

---

# 2. Official term status classes

## CANONICAL

Accepted Domain Atlas concept/capability with stable current semantics.

Current examples:

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
```

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
```

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
```

## PROVISIONAL

A recurring semantic need with sufficient evidence to track explicitly, but whose exact domain boundary has not passed dedicated review.

Examples:

```text
Actor
Participation
Responsibility
Stewardship
Authority
Visibility
```

## DEFERRED

A demonstrated semantic area intentionally postponed to a later concept review.

Current examples:

```text
Evidence
Confirmation
Provenance
Quantity
Register
Subject
Resource
Relationship
Principal
Trigger
```

## HISTORICAL / SUPERSEDED

Earlier terminology preserved in Git/docs but not authoritative for the current kernel.

Historical language is mapped, not silently deleted or recycled.

---

# 3. UI exposure classes

- **DIRECT** — natural primary user-facing noun;
- **CONTEXTUAL** — visible, usually under a context-specific label;
- **CONFIGURATION** — exposed primarily through rules/settings/actions;
- **ADVANCED** — useful in detail/history/power-user surfaces;
- **HIDDEN** — primarily internal semantics; UI exposes consequences/actions instead.

Kernel sophistication must not force ontology vocabulary into simple UI.

---

# 4. Canonical Intention & Execution concepts

## Goal

**Status:** CANONICAL  
**Source:** `concepts/goal.md`  
**Question:** What outcome/condition/change/pattern is intentionally desired?  
**UI exposure:** DIRECT

Persistent representation of an outcome, condition, change or behavioral pattern intentionally adopted as desired.

```text
Goal != Plan
Goal != Activity
Goal != Milestone
Goal != Evidence
```

Possible UI language: Goal, Objective, context-appropriate Target.

```text
Goal identity
!= governor/owner
!= stakeholder
!= contributor
!= subject
!= account
```

---

## Plan

**Status:** CANONICAL  
**Source:** `concepts/plan.md`  
**Question:** How is a purpose intended to be pursued/organized?  
**UI exposure:** DIRECT / CONTEXTUAL

Persistent revisable structure coordinating work, behaviors, milestones, rules, stages or other execution elements in pursuit of a purpose.

```text
Plan != Goal
Plan != Activity
Plan != Routine
Plan != Schedule
Plan != Actual
```

Product profiles may include Plan, Project, Program, Study plan, Training plan, Release plan, Trip plan and Rehabilitation plan.

`Project` and `Program` are currently product profiles, not separate kernel primitives.

Plan identity is independent from coordinator, contributor and responsibility relationships.

---

## Activity

**Status:** CANONICAL  
**Source:** `concepts/activity.md`  
**Question:** What actionable work/behavior is intended to be performed?  
**UI exposure:** DIRECT / CONTEXTUAL

Persistent actionable intention whose actor responsibility, Schedule, actual execution and Outcome remain separable.

```text
Activity != Event
Activity != Plan
Activity != Session
Activity != Actual
Activity != assignee
```

Product/UI aliases may include Task, Action, Workout, Study item, Maintenance action, Checklist item and Preparation step.

```text
Activity identity
!= requester
!= creator
!= responsible actor / assignee
!= performer
```

---

## Event

**Status:** CANONICAL  
**Source:** `concepts/event.md`  
**Question:** What occurrence-centred thing is expected to happen?  
**UI exposure:** DIRECT

Persistent expected occurrence for which temporal placement is intrinsic to meaning.

Typical product language includes Meeting, Appointment, Lesson, Exam, Concert, Flight, Shift, Interview, Race and Ceremony.

```text
Event != Activity
Event != Schedule
Event != participant response
Event != attendance
Event != Milestone
```

One shared Event should normally coexist with actor-scoped participation state rather than per-user copies.

---

## Routine

**Status:** CANONICAL  
**Source:** `concepts/routine.md`  
**Question:** What behavioral/execution policy is intentionally expected to repeat?  
**UI exposure:** DIRECT

Persistent reusable policy expressing repeated behavioral/execution expectation.

```text
Routine != Recurrence
Routine != Event series
Routine != Plan
Routine != observed habit
```

Routine identity is independent from performer; responsibility may vary per Occurrence.

---

## Milestone

**Status:** CANONICAL  
**Source:** `concepts/milestone.md`  
**Question:** What meaningful contextual checkpoint matters inside Goal/Plan?  
**UI exposure:** DIRECT / ADVANCED

Persistent contextual checkpoint representing meaningful state, achievement, decision, delivery or transition.

```text
Milestone != Goal
Milestone != GoalCriterion
Milestone != Activity
Milestone != Event
Milestone != Outcome
Milestone != Deadline
Milestone != Phase
```

Approver/stakeholder/governor relationships do not define Milestone identity.

---

# 5. Canonical Time concepts

## Occurrence

**Status:** CANONICAL  
**Source:** `concepts/occurrence.md`  
**Question:** Which expected instance from a recurring/generative source is this?  
**UI exposure:** HIDDEN / ADVANCED

Stable logical identity for one generated expected instance.

Typical UI language: This time, This workout, This meeting, Only this one, This and future occurrences.

```text
Occurrence != Recurrence
Occurrence != Routine/Event source
Occurrence != Schedule
Occurrence != Session
Occurrence != Actual
```

Occurrence identity is independent from assigned/responsible actor.

---

## Schedule

**Status:** CANONICAL  
**Source:** `concepts/schedule.md`  
**Question:** When is this schedulable subject currently accepted/intended/expected to happen?  
**UI exposure:** HIDDEN / CONFIGURATION

Typical UI language: When, Date/time, Scheduled for, Move to..., Add to calendar, Tuesday afternoon.

```text
Schedule != Temporal Constraint
Schedule != deadline/target
Schedule != Recurrence
Schedule != Availability
Schedule != Capacity claim
Schedule != Session/Actual
```

Accepted Schedule is canonical temporal assignment under relevant authority/context; it does not mean every participant accepted participation.

---

## Session

**Status:** CANONICAL  
**Source:** `concepts/session.md`  
**Question:** Which logically continuous bounded episode of actual execution occurred?  
**UI exposure:** CONTEXTUAL / ADVANCED

Typical UI language: Start, Pause, Resume, Stop, Work session, Study session, Workout, Tracked time, Execution history.

```text
Session != Schedule
Session != Activity
Session != Occurrence
Session != Event attendance
Session != broader Actual/Outcome
```

Session identity follows logical execution continuity, not performer count. Actor-specific participation may cover only part of a shared Session envelope.

---

## Temporal Constraint

**Status:** CANONICAL  
**Source:** `concepts/temporal-constraint.md`  
**Question:** Where/when is placement/duration/temporal relation allowed, required, bounded or preferred?  
**UI exposure:** CONFIGURATION

Typical UI language: Deadline, Not before, Not after, Preferred time, Allowed window, Avoid this time, Minimum/maximum duration, Recovery/spacing.

```text
Temporal Constraint != Schedule
Temporal Constraint != Availability
Temporal Constraint != target/review date by default
Temporal Constraint != Movement Policy
Temporal Constraint != Actual
```

`Deadline` is latest-bound Temporal Constraint semantics, not a separate kernel primitive.

---

## Recurrence

**Status:** CANONICAL  
**Source:** `concepts/recurrence.md`  
**Question:** How does a temporal/generative pattern repeat?  
**UI exposure:** CONFIGURATION

Typical UI language: Repeat, Every Monday, 3 times/week, Every 12 hours, After completion, Custom repeat.

```text
Recurrence != Routine
Recurrence != Event-series meaning
Recurrence != Occurrence
Recurrence != Schedule
Recurrence != Trigger
Recurrence != responsibility rotation
```

---

## Availability

**Status:** CANONICAL semantic capability  
**Source:** `concepts/availability-capacity.md`  
**Question:** When may a schedulable resource's capacity be used?  
**UI exposure:** DIRECT / CONFIGURATION / DERIVED

Typical UI language: Available, Unavailable, Working hours, Free/busy, Availability for others, Out of office, Exception.

Availability is resource-oriented. Subject-specific timing rules remain Temporal Constraints.

Authorized availability projections can be shared without exposing private source events.

---

## Capacity

**Status:** CANONICAL semantic capability  
**Source:** `concepts/availability-capacity.md`  
**Question:** How much / what kind of compatible commitment can a schedulable resource sustain?  
**UI exposure:** HIDDEN / DERIVED / ADVANCED

Typical UI language: Busy, Block my time, Can overlap, Focus time, Capacity remaining, Room/resource unavailable.

```text
scheduled != capacity consumed
overlap != universal conflict
Capacity != universal busy/free boolean
Capacity != universal scalar percentage
```

---

# 6. Canonical Reality concepts

## Actual

**Status:** CANONICAL  
**Source:** `concepts/actual.md`  
**Validation:** `checkpoints/actual-v0-validation.md` — PASS WITH HARDENING  
**Question:** How did this specific intention or expectation resolve in reality?  
**UI exposure:** HIDDEN / ADVANCED / CONTEXTUAL

A persistent contextual realization record representing whether and how a specific intended or expected domain subject was realized in reality.

```text
Actual != Activity/Event/Occurrence
Actual != Schedule
Actual != Session
Actual != Outcome
Actual != Observation
Actual != Evidence
Actual != Confirmation
Actual != Provenance
```

Core guardrails:

- contextual, not a universal reality object;
- spontaneous reality may exist without Actual;
- absence of Actual does not mean failed/skipped/missed;
- known non-realization is distinct from unknown;
- passage of time does not establish Actual;
- one realization may use multiple Sessions;
- corrections preserve relevant assertion/provenance history;
- shared Actual does not imply identical actor participation.

Typical UI: What happened?, actual time, performed/not performed, attendance/history detail.

---

## Outcome

**Status:** CANONICAL  
**Source:** `concepts/outcome.md`  
**Validation:** `checkpoints/outcome-v0-validation.md` — PASS WITH HARDENING  
**Question:** What result or disposition followed from this realization in the relevant context?  
**UI exposure:** CONTEXTUAL / HIDDEN / ADVANCED

A contextual representation of the result or disposition established for a specific Actual realization.

```text
Outcome != Actual
Outcome != lifecycle/operational state
Outcome != Observation
Outcome != produced artifact/output
Outcome != Milestone
Outcome != Confirmation
Outcome != Provenance
Outcome != Evidence
```

Core guardrails:

- optional/contextual rather than mandatory;
- no universal Outcome enum;
- absence of Outcome does not mean failure;
- `unconfirmed` is epistemic/Confirmation semantics;
- measurements and artifacts remain separate;
- shared Outcome does not imply identical actor-specific consequences.

Typical UI: Completed/Partial, Passed/Failed, Approved/Changes requested, Decision deferred, Result details.

---

## Observation

**Status:** CANONICAL  
**Source:** `concepts/observation.md`  
**Validation:** `checkpoints/observation-v0-validation.md` — PASS WITH HARDENING  
**Question:** What was observed, measured, reported, or calculated about this subject, and to what time/context does it apply?  
**UI exposure:** CONTEXTUAL / HIDDEN / ADVANCED

### Domain meaning

A persistent contextual record of a measured, perceived, reported, or explicitly derived property, state, value, rating, or simple assertion about a subject at an effective time or context.

Examples:

```text
weight = 66.4 kg
mood = 2/5
pain = 4/10
exam score = 78/100
odometer = 84,220 km
room temperature = 21.6 °C
```

### Not the same as

```text
Observation != Actual
Observation != Outcome
Observation != Quantity
Observation != Register
Observation != Evidence
Observation != Confirmation
Observation != Provenance
```

### Core guardrails

- Observation is a measurement/simple-assertion concept, not a universal fact/event/blob primitive;
- may exist without prior intention, Actual, Outcome, Goal, Session, or Register;
- stable identity is not `subject + type + time + value`;
- correction of the same observational act normally preserves identity; re-observation normally creates a new Observation;
- effective time/context is distinct from recorded/ingested time;
- missing Observation != observed negative != failed/unavailable measurement;
- subjective Observations are valid when perspective/source/context are preserved;
- conflicting Observations may coexist and are not silently averaged/overwritten;
- derived Observations preserve traceability to source facts;
- query/chart aggregates do not automatically become persisted Observations;
- high-frequency sensor semantics do not require one SQL row per sample.

### Quantity/Register boundary

```text
Quantity
= reusable value + unit semantics

Observation
= contextual record using a value

Register
= longitudinal organization/analysis of records
```

The exact Quantity and Register models remain deferred and must re-test this boundary in the Data/Subjects cluster.

### Multi-actor

```text
Observation subject
!= observer
!= recorder
!= source/provider/device
!= confirmer/authority
!= viewer
```

A shared Event/Goal/Plan does not automatically make related Observations shared. Private Observations may support authorized derived projections without raw-source disclosure.

### Typical UI presentation

Users usually see domain language rather than `Observation`:

- Weight — 66.4 kg;
- Mood — Low;
- Odometer — 84,220 km;
- Exam score — 78/100;
- `Registra un dato`;
- source/history details in advanced views.

---

# 7. Product/profile terms that are not independent kernel primitives

## Task

**Status:** PRODUCT / UI TERM  
**Maps to:** Activity

Use when completion of a defined work unit is the dominant UI meaning. Do not create a second Task lifecycle/history model beside Activity.

## Project

**Status:** PRODUCT PROFILE / HISTORICAL KERNEL TERM  
**Current mapping:** Plan profile, optionally connected to Goal(s), Milestones, Activities, Events, dependencies, etc.

A finite coordinated body of work can remain first-class UX without a separate strategy kernel.

## Program

**Status:** PRODUCT PROFILE / HISTORICAL KERNEL TERM  
**Current mapping:** Plan profile emphasizing structured progression, stages, repeated policies, reviews or adaptation.

## Calendar Block

**Status:** PRODUCT / UI TERM  
**Current mapping:** calendar-shaped representation whose underlying meaning is generally Schedule + Capacity Reservation/Claim or Availability override, depending on purpose.

Do not clone every scheduled Activity/Event into a second Calendar Block entity.

## Deadline

**Status:** PRODUCT/UI TERM + semantic specialization  
**Maps to:** latest-bound Temporal Constraint.

## Window

**Status:** RANGE SHAPE / PRODUCT TERM

An interval may represent hard/soft Temporal Constraint, Availability, accepted coarse Schedule or Goal/Milestone target window. Identical geometry does not imply identical meaning.

## Repeat

**Status:** UI TERM  
**Maps to:** Recurrence configuration where recurrence semantics are intended.

## Busy / Free

**Status:** UI / DERIVED TERM  
**Maps to:** projections of Availability + Capacity + claims + compatibility.

---

# 8. Historical V1 vocabulary crosswalk

## Planning Item

**Status:** HISTORICAL / PRODUCT ABSTRACTION

No universal Planning Item kernel primitive has been accepted. Shared capabilities are composed around explicit concepts such as Activity, Event, Schedule and Temporal Constraint.

## Reminder

**Status:** PRODUCT CAPABILITY / DOMAIN REVIEW DEFERRED

Reminder is not automatically Activity. Reminder/Trigger/notification semantics still require dedicated review.

## Calendar / Life Area

**Status:** PRODUCT ORGANIZATION CONTEXT — dedicated domain status not yet reviewed

Organization/filtering context does not automatically establish ownership, Goal semantics or sharing scope.

## Module

**Status:** PRODUCT/ARCHITECTURE TERM, NOT DOMAIN PRIMITIVE

A domain-specific capability area such as training, nutrition, learning, travel, finance or creative work.

## Tag

**Status:** PRODUCT METADATA TERM — exact persistence deferred

Lightweight label/filtering concept. Tag must not establish ownership, authority, lifecycle, scheduling or canonical hierarchy.

## Person-related commitment

**Status:** HISTORICAL PRODUCT PHRASE

Current mapping usually uses explicit Activity/Event + future Person/Relationship semantics. The other person does not need a LifeOS Account and the item is not automatically shared.

## Shared Item

**Status:** PRODUCT PHRASE, NOT UNIVERSAL PRIMITIVE

Current direction:

```text
shared canonical object
+
actor-scoped state/personal overlay
```

rather than one generic SharedItem wrapper.

## Source

**Status:** IMPORTANT DEFERRED PROVENANCE DIMENSION

Where information came from: user entry, file, provider, email, external system, device, AI proposal, etc.

Source is not local organization, object type, truth, authority or sharing state.

## Temporary Mode

**Status:** PROVISIONAL CROSS-CUTTING CONCEPT

Time-bounded context/policy temporarily changing planning/availability/capacity behavior without rewriting stable baseline.

## Inbox Item

**Status:** PRODUCT CAPTURE STATE/PROFILE, NOT YET KERNEL PRIMITIVE

Captured information awaiting classification. Resolution may become Activity, Event, Goal, Plan, note, document, Observation, etc.

## Decision Record

**Status:** PRODUCT/HISTORICAL TERM -> FUTURE `Decision` REVIEW

Need remains valid; final Decision/Version model belongs to Relationships/Reasoning review.

---

# 9. Multi-actor terminology — tracked but not prematurely canonized

## Actor

**Status:** PROVISIONAL / DEFERRED

Entity capable of acting, participating, holding responsibility or exercising authority in domain reality. Do not equate Actor with `users.id`.

## Person

**Status:** DEFERRED

Human represented in LifeOS domain reality. Person may exist without LifeOS Account.

## Account

**Status:** PRODUCT/IDENTITY CONCEPT — final boundary deferred

```text
Account != Person != Participant != Subject
```

## Principal

**Status:** DEFERRED TECHNICAL/AUTHORITY CONCEPT

Likely authenticated identity acting in system. Exact relation to Account/Actor/delegated AI remains open.

## Participant / Participation

**Status:** PROVISIONAL

Actor-scoped involvement/state around a shared object. No universal participation enum accepted.

## Responsibility

**Status:** PROVISIONAL — STRONG EVIDENCE

Future model must be richer than one `assigned_to` field and may need accountability, expected performer, open/claimable responsibility, approval, substitution and hand-off.

## Stewardship / Coordination Responsibility

**Status:** PROVISIONAL / RESEARCH-BACKED QUESTION

Execution assignment can move while anticipation, reminding, monitoring and repair burden remain elsewhere. Exact model remains intentionally undecided.

## Performer

**Status:** RELATIONSHIP ROLE — exact model deferred

Who actually performed work. Not automatically requester/responsible actor/planned assignee.

## Subject

**Status:** DEFERRED — DATA/SUBJECT REVIEW

Who/what information/action/Observation is about.

## Resource

**Status:** DEFERRED — DATA/SUBJECT REVIEW

Something whose availability/capacity/access may constrain execution/scheduling: people in schedulable roles, rooms, vehicles, equipment, devices, stock, facilities, etc.

Actor and Resource can overlap in scenarios but are not synonyms.

## Owner / Governor / Steward

**Status:** DEFERRED RELATIONSHIP/AUTHORITY SEMANTICS

Do not use casually as synonyms for creator, participant, viewer, responsible actor or performer.

## Authority

**Status:** DEFERRED — STRONG CROSS-CUTTING DIMENSION

Who/what may establish, approve, change or override canonical state in context. Authority is not inferred merely from creation, visibility or participation.

## Visibility / Access

**Status:** DEFERRED

What an actor/principal may inspect/receive/use.

```text
Visibility != Authority
```

Future design must cover purpose, context, revocation, historical attribution and inferred/derived disclosure.

---

# 10. Reality/Evidence terms still under review

## Evidence

**Status:** DEFERRED — UPCOMING REVIEW

Information used in a particular evaluation context. Evidence is not automatically identical to the source fact, positive contribution or universal proof.

Observation is a likely source of Evidence but is not Evidence merely by existing.

## Confirmation / Acknowledgement / Acceptance

**Status:** DEFERRED — IMPORTANT DISTINCTIONS

Where consequence requires it:

```text
sent
!= delivered
!= seen
!= understood
!= acknowledged
!= accepted/agreed
!= authoritative/confirmed
!= acted upon
!= Actual
```

Not every UI needs every stage.

## Provenance

**Status:** DEFERRED FUTURE CONCEPT

How a fact/value/decision/change entered LifeOS and under what source/assertion/confirmation/authority context.

```text
Provenance != Actual
Provenance != Outcome
Provenance != Observation
source != truth
authority != source by default
```

## Quantity

**Status:** DEFERRED — DATA/SUBJECT REVIEW

Reusable measurement value + unit semantics. Observation v0 requires Quantity to remain separable from observation identity/context.

## Register

**Status:** DEFERRED — DATA/SUBJECT REVIEW

Longitudinal organization/analysis capability for records over time. Register may organize Observations and specialist records without becoming their source identity.

---

# 11. Other high-value deferred terms

## Trigger

**Status:** DEFERRED

Detects qualifying event/state/threshold and may cause action/notification/rule evaluation.

```text
Trigger != Recurrence
Trigger != Routine
```

## Relationship

**Status:** DEFERRED — STRONG FUTURE NEED

Cross-domain evidence indicates typed/directional semantics are likely needed.

Potential relations such as `supports`, `conflicts_with`, `depends_on`, `prepares_for`, `replaces`, `evidence_for`, `derived_from` must not collapse prematurely into semantic-free `related_to` if behavior/query meaning differs.

## Dependency

**Status:** DEFERRED / likely Relationship specialization or typed semantic

Represents producer/consumer, prerequisite, simultaneity, resource, blocking or other coordination dependency where justified.

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
Event != participant response
Event != attendance
Routine != Recurrence
Routine != observed habit
Occurrence != Schedule
Occurrence != Session
Schedule != Temporal Constraint
Schedule != Availability
Schedule != Capacity Reservation
Schedule != Session / Actual
Session != Actual
Actual != Outcome
Actual != Observation
Actual != Evidence
Actual != Provenance
Outcome != lifecycle/operational state
Outcome != Observation
Outcome != produced artifact/output
Outcome != Milestone
Outcome != Confirmation
Outcome != Provenance
Outcome != Evidence
Observation != Quantity
Observation != Register
Observation != Evidence
Observation != Confirmation
Observation != Provenance
missing Observation != observed negative
recorded time != Observation effective time
Temporal Constraint != Availability
Recurrence != Trigger
Availability != empty-gap cache
Capacity != universal busy/free boolean
```

## Multi-actor

```text
Person != Account
Account != Participant
Actor != Subject
Actor != Resource
Participant != Responsible actor
Responsible actor != Performer
Creator != Owner/Governor
Visibility != Authority
Sharing != ownership
Assignment != Activity identity
Participation response != Actual participation
shared Actual != identical actor participation
shared Outcome != identical actor consequence
Observation subject != observer/recorder/source/authority/viewer
conflicting Observation != automatic overwrite/average
Schedule acceptance != participant acceptance
Delivery != acknowledgement
Acknowledgement != agreement
Agreement != authority
Authority != Actual
AI knowledge != disclosure permission
AI suggestion != canonical authority
future access revocation != deletion of historical attribution
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
Register view != mandatory duplicate source record
```

---

# 13. Domain -> Product -> UI examples

## Buy milk

```text
Domain
Activity

Product
Task

UI
Buy milk
[ ]
Tomorrow
```

## Gym 3x/week

```text
Domain
Routine + Recurrence + Occurrences + optional Schedules

Product
Routine / Workout routine

Simple UI
Gym
3 times per week
```

## Website redesign

```text
Domain
Goal optional + Plan + Activities + Events + Milestones

Product
Project

UI
Website Redesign
Overview / Tasks / Timeline / Milestones
```

## Realized meeting with result

```text
Domain
Event + Schedule + Actual + Outcome + actor-scoped participation

UI
Project review
Planned 10:00-11:00
Actually 10:08-11:23
Result: Decision deferred
Luca left at 10:45
```

## Exam

```text
Domain
Event
+ Actual
+ Observation: score = 78/100
+ Outcome: passed
+ optional Milestone: certification checkpoint reached

UI
Exam result
78/100 · Passed
```

The score Observation and Outcome remain semantically distinct.

## Weight log

```text
Domain
Observation
property: body weight
value: Quantity(66.4 kg)
effective: 08:00
recorded: 18:00

Possible Product
Weight Register

UI
Weight
66.4 kg
Today · 08:00
```

The Register view does not create a duplicate Observation.

## Conflicting subjective observations

```text
Meeting context

Mattia Observation
usefulness = 4/5

Luca Observation
usefulness = 2/5
```

Both perspectives can remain valid assertions without manufactured averaging.

## Private availability

```text
Private source context/Observation
        ↓
authorized projection
Unavailable 18:00-20:00

Shared UI
Sara is unavailable
```

The private reason need not be exposed.

---

# 14. Frontend rule

Frontend may choose the clearest language without changing kernel semantics.

Prefer plain language, progressive disclosure, contextual labels, specialist terminology only where users expect it and actions/consequences over internal nouns when clearer.

Examples:

```text
Internal: Occurrence
UI: This time
```

```text
Internal: Temporal Constraint
UI: Deadline / Preferred time / Not before
```

```text
Internal: Actual
UI: What happened? / Actual time / Performed / Not performed
```

```text
Internal: Outcome
UI: Passed / Partial / Approved / Decision deferred / Result details
```

```text
Internal: Observation
UI: Weight / Mood / Score / Odometer / Registra un dato
```

Reverse rule:

> **A UX label does not automatically create a backend/domain type.**

---

# 15. Implementation-language rule

Physical/API terminology remains intentionally incomplete until logical/physical data modeling.

Do not infer table/class names from this map.

Canonical domain terms do not automatically imply identically named tables, and product aliases do not create parallel persistence models.

In particular Actor, Participant, Responsibility, Subject, Resource, Authority, Visibility, Actual, Outcome and Observation must not be translated prematurely into final SQL table/cardinality choices before the logical model is reviewed.

Observation v0 specifically does **not** imply:

- one generic fact table for the whole domain;
- one row per raw sensor sample;
- one arbitrary JSON value shape;
- one duplicated record per Register/dashboard/Goal use.

When implementation names eventually differ from canonical language for good technical reasons, document the mapping here.

---

# 16. Terminology change policy

The map is designed for long-term stability. Stability does not mean freezing mistakes.

A term may enter only when at least one holds:

1. it is an accepted Domain Atlas concept;
2. it is recurring product/UI language with clear mapping;
3. omitting it creates material ambiguity across domain/product/frontend/AI work;
4. a demonstrated semantic need must be tracked explicitly as PROVISIONAL/DEFERRED.

A term does **not** become canonical because a competitor uses it, one database design would be convenient, one mockup contains it, one scenario might theoretically need it, an AI suggested it or the architecture sounds more complete with it.

Change procedure:

1. review/change source concept/decision first;
2. preserve historical reasoning;
3. update this map;
4. update checkpoints/handoffs;
5. update implementation names only after persistence/API exists.

Do not silently recycle one term with a new meaning.

---

# 17. Maintenance rule

This file is the semantic navigation layer, not a duplicate of every concept spec.

Detailed specs remain authoritative for lifecycle, full invariants, edge/adversarial cases, evidence, history, rejected alternatives and persistence implications.

This map should remain capable of answering quickly:

> **What does this LifeOS term mean, what does it not mean, what status does it have, and what might a user actually see?**

without requiring a reader to reconstruct the ontology from dozens of documents.