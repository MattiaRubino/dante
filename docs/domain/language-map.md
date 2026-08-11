# LifeOS Domain & Product Language Map

**Status:** Canonical terminology reference for the active Domain Atlas  
**Established:** 2026-08-11  
**Current revision:** 2026-08-11 — Actual v0 promoted after Methodology v3 validation  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

This is the fast canonical reference for LifeOS vocabulary.

It prevents four layers from drifting apart:

```text
DOMAIN LANGUAGE
what a concept means canonically
        ↓
PRODUCT LANGUAGE
how LifeOS may package/present the meaning
        ↓
UI LANGUAGE
what users actually read and manipulate
        ↓
IMPLEMENTATION LANGUAGE
API / schema / code names once designed
```

The layers are related but are **not one-to-one**.

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
Outcome
Observation
Evidence
Confirmation
Provenance
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

Multi-actor:

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

Product profiles may include Plan, Project, Program, Study plan, Training plan, Release plan, Trip plan, Rehabilitation plan.

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

Product/UI aliases may include Task, Action, Workout, Study item, Maintenance action, Checklist item, Preparation step.

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

### Domain meaning

A persistent contextual realization record representing whether and how a specific intended or expected domain subject was realized in reality.

Actual provides the reconciliation bridge between expectation and realized reality without becoming a container for every fact produced by that reality.

```text
Activity / Event / Occurrence
          ↓
        Actual
how that expectation was realized
```

### Not the same as

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

### Core guardrails

- Actual is contextual, not a universal reality object;
- spontaneous reality may exist without Actual when no expectation is being reconciled;
- absence of Actual does not mean failed/skipped/missed/not performed;
- known non-realization is distinct from unknown and may have a valid Actual;
- passage of time does not establish Actual;
- one Activity/Occurrence may use multiple Sessions while retaining one broader realization context;
- ordinary Event occurrence may have Actual without a redundant Session;
- measurements remain Observation/specialist facts rather than duplicated Actual fields;
- correction may change current accepted Actual while relevant provenance/assertion history remains;
- provider identity does not define LifeOS Actual identity.

### Multi-actor

```text
shared Actual
!= actor-specific participation reality
```

Subject, recorder, responsible actor, expected performer and actual performer may differ.

Private Actual may support an authorized derived projection without disclosing its source facts. AI/system access to Actual does not create disclosure permission.

### Typical UI presentation

Users will usually see consequences rather than the word `Actual`, for example:

- Completed / Partial / Skipped;
- Actual time 10:08-11:23;
- 3.8 km completed;
- Attended / Did not attend;
- What actually happened?;
- execution/history detail.

The UI does not need a generic `Create Actual` surface.

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

Do not infer a universal `planning_items` aggregate/table from historical wording.

## Reminder

**Status:** PRODUCT CAPABILITY / DOMAIN REVIEW DEFERRED

Reminder is not automatically Activity. Reminder/Trigger/notification semantics still require dedicated review.

## Calendar / Life Area

**Status:** PRODUCT ORGANIZATION CONTEXT — dedicated domain status not yet reviewed

Organization/filtering context does not automatically establish ownership, Goal semantics or sharing scope.

## Module

**Status:** PRODUCT/ARCHITECTURE TERM, NOT DOMAIN PRIMITIVE

A domain-specific capability area such as training, nutrition, learning, travel, finance or creative work.

Modules may add specialist UI/rules/integrations without replacing common Goal/Plan/Activity/Time/History semantics.

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

Where information came from: user entry, file, provider, email, external system, AI proposal, etc.

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

Who/what information/action/observation is about.

```text
caregiver acts -> older adult subject
parent acts -> child subject
technician acts -> vehicle subject
```

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

## Outcome

**Status:** DEFERRED — ACTIVE NEXT REVIEW

Working purpose: what resulted from execution/occurrence. Must be tested against Actual, Milestone, Activity/Occurrence completion, Observation, Confirmation and Evidence.

## Observation

**Status:** DEFERRED

Observed fact about reality that may exist without prior intention or Actual wrapper.

## Evidence

**Status:** DEFERRED

Information used in a particular evaluation context. Evidence is not automatically identical to source fact, positive contribution or universal proof.

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
source != truth
authority != source by default
```

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

Potential relations such as `supports`, `conflicts_with`, `depends_on`, `prepares_for`, `replaces`, `evidence_for` must not collapse prematurely into semantic-free `related_to` if behavior/query meaning differs.

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
Temporal Constraint != Availability
Recurrence != Trigger
Availability != empty-gap cache
Capacity != universal busy/free boolean
Milestone != Outcome
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
Goal optional
+ Plan
+ Activities
+ Events
+ Milestones

Product
Project

UI
Website Redesign
Overview / Tasks / Timeline / Milestones
```

## Recurring team meeting

```text
Domain
Event + Recurrence + Occurrences + Schedule + actor-scoped participation

UI
Weekly Team Meeting
Every Monday · 10:00
Yes / Maybe / No
```

## Realized meeting

```text
Domain
Event + Schedule + Actual + actor-scoped participation reality

UI
Project review
Planned 10:00-11:00
Actually 10:08-11:23
Luca left at 10:45
```

One shared Actual does not imply identical attendance.

## Private availability

```text
Private source
Event + Actual: medical appointment occurred

Authorized projection
Unavailable 18:00-20:00

Shared UI
Sara is unavailable
```

The private reason need not be exposed.

## Household chore rotation

```text
Domain
Routine
+ Recurrence
+ Occurrences
+ future responsibility relations

UI
Take recycling out
Every Thursday
This week: Luca
```

Responsibility rotation does not require duplicate Routines.

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
UI: What happened? / Completed / Actual time / Result details
```

Reverse rule:

> **A UX label does not automatically create a backend/domain type.**

---

# 15. Implementation-language rule

Physical/API terminology remains intentionally incomplete until logical/physical data modeling.

Do not infer table/class names from this map.

Examples:

```text
Canonical: Plan
```

does not yet imply:

```text
plans
projects
programs
```

Likewise Actor, Participant, Responsibility, Subject, Resource, Authority, Visibility and Actual must not be translated prematurely into final SQL table/cardinality choices before the logical model is reviewed.

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