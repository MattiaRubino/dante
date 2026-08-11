# LifeOS Domain & Product Language Map

**Status:** Canonical terminology reference for the active Domain Atlas  
**Established:** 2026-08-11  
**Current revision:** 2026-08-11 — Evidence v0 promoted after Methodology v3 validation  
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

This map records decisions; it does not create primitives.

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
Confirmation
Evidence
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
Acknowledgement
Acceptance / Agreement
```

## DEFERRED

A demonstrated semantic area intentionally postponed to later review.

Current examples:

```text
Provenance
Quantity
Register
Subject
Resource
Relationship
Principal
Trigger
Verification
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

Persistent representation of an intentionally desired outcome, condition, change or behavioral pattern.

```text
Goal != Plan
Goal != Activity
Goal != Milestone
Goal != Evidence
Goal identity != governor/stakeholder/contributor/subject/account
```

Possible UI: Goal, Objective, context-appropriate Target.

## Plan

**Status:** CANONICAL  
**Source:** `concepts/plan.md`  
**Question:** How is a purpose intended to be pursued/organized?  
**UI exposure:** DIRECT / CONTEXTUAL

Persistent revisable structure coordinating work, behaviors, milestones, rules, stages or other execution elements.

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
Activity identity != requester/creator/responsible actor/assignee/performer
```

Possible UI: Task, Action, Workout, Study item, Maintenance action, Checklist item.

## Event

**Status:** CANONICAL  
**Source:** `concepts/event.md`  
**Question:** What occurrence-centred thing is expected to happen?  
**UI exposure:** DIRECT

```text
Event != Activity
Event != Schedule
Event != participant response
Event != attendance
Event != Milestone
```

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
Milestone != Deadline
Milestone != Phase
```

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
```

Accepted Schedule does not mean every participant accepted participation.

## Session

**Status:** CANONICAL  
**Source:** `concepts/session.md`  
**Question:** Which logically continuous bounded episode of actual execution occurred?  
**UI exposure:** CONTEXTUAL / ADVANCED

```text
Session != Schedule
Session != Activity
Session != Occurrence
Session != Event attendance
Session != broader Actual/Outcome
```

Session identity follows logical execution continuity, not performer count.

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
**Question:** When may a schedulable resource's capacity be used?  
**UI exposure:** DIRECT / CONFIGURATION / DERIVED

Availability is resource-oriented. Subject-specific timing rules remain Temporal Constraints.

## Capacity

**Status:** CANONICAL semantic capability  
**Source:** `concepts/availability-capacity.md`  
**Question:** How much / what kind of compatible commitment can a schedulable resource sustain?  
**UI exposure:** HIDDEN / DERIVED / ADVANCED

```text
scheduled != capacity consumed
overlap != universal conflict
Capacity != universal busy/free boolean
Capacity != universal scalar percentage
```

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
```

Core guardrails: contextual rather than universal; absence does not imply failure; passage of time does not establish Actual; shared Actual does not imply identical actor participation.

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
**Question:** What was observed, measured, reported, or calculated about this subject, and to what time/context does it apply?  
**UI exposure:** CONTEXTUAL / HIDDEN / ADVANCED

A persistent contextual record of a measured, perceived, reported, or explicitly derived property, state, value, rating, or simple assertion about a subject.

```text
Observation != Actual
Observation != Outcome
Observation != Quantity
Observation != Register
Observation != Evidence
Observation != Confirmation
Observation != Provenance
```

Core guardrails:

- not a universal fact/blob primitive;
- may exist without prior intention/Actual/Goal/Register;
- effective time/context != recorded/ingested time;
- missing Observation != observed negative != failed measurement;
- subjective/conflicting Observations can coexist;
- query aggregates do not automatically become persisted Observations;
- high-frequency streams do not imply row-per-sample persistence.

Boundary:

```text
Quantity   = reusable value + unit semantics
Observation= contextual record using a value
Register   = longitudinal organization/analysis of records
```

## Confirmation

**Status:** CANONICAL  
**Source:** `concepts/confirmation.md`  
**Validation:** `checkpoints/confirmation-v0-validation.md` — PASS WITH HARDENING  
**Question:** Who or what explicitly affirms this specific version of this target, for which purpose and context?  
**UI exposure:** CONTEXTUAL / HIDDEN / ADVANCED

A persistent contextual attestation that a specific confirmer affirms a specific version of a confirmable target as sufficiently accepted for a defined purpose at that time.

```text
Confirmation != Actual
Confirmation != Outcome
Confirmation != Observation
Confirmation != Provenance
Confirmation != Acknowledgement
Confirmation != Acceptance/Agreement
Confirmation != Verification
Confirmation != Authority
```

Core guardrails:

- contextual and optional, not universal;
- no Confirmation does not mean false/rejected/incorrect/not performed;
- Confirmation targets a material target version;
- material target correction does not silently inherit previous Confirmation;
- `awaiting confirmation` is derived workflow state;
- imported/inferred/automatic/corrected are not Confirmation types;
- automation/AI must not fabricate human Confirmation;
- Confirmation by one actor does not imply Confirmation by another;
- subject, confirmer, recorder, observer, performer and authority actor may differ;
- conflicting Confirmations must be representable;
- purpose/context may limit where a Confirmation is sufficient.

Typical UI: Confirm, Looks correct, Yes this happened, Review and confirm, Needs confirmation.

## Evidence

**Status:** CANONICAL semantic role / relationship  
**Source:** `concepts/evidence.md`  
**Validation:** `checkpoints/evidence-v0-validation.md` — PASS WITH HARDENING  
**Question:** What information materially bears on this evaluation, in what direction and context, and on what basis is it being used?  
**UI exposure:** HIDDEN / ADVANCED / CONTEXTUAL

Evidence is the contextual evaluative role played by source information when it is used to support, contradict, qualify, or otherwise materially inform a specific evaluation target.

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
- Evidence may support, contradict, qualify, or otherwise inform;
- Evidence existence does not establish target truth by itself;
- no Evidence != Evidence against;
- no LifeOS record != proof of non-occurrence unless an explicit completeness/evaluation rule justifies that inference;
- later-discovered Evidence relevance does not rewrite historical source purpose/intention;
- one source can serve several evaluations without duplication;
- evidentiary strength/certainty is contextual rather than one universal scalar;
- conflicting Evidence can coexist;
- private Evidence use does not create disclosure permission;
- AI discovery/use does not create authority or disclosure permission;
- Evidence semantics do not imply one persisted entity/edge for every evaluative use.

Typical UI: Why is this progressing?, Based on…, Supporting data, Conflicting data, Why did LifeOS conclude this?, Review evidence.

---

# 7. Product/profile terms that are not independent kernel primitives

## Task

**Status:** PRODUCT / UI TERM  
**Maps to:** Activity

Use when completion of a defined work unit is the dominant UI meaning.

## Project

**Status:** PRODUCT PROFILE / HISTORICAL KERNEL TERM  
**Current mapping:** Plan profile, optionally connected to Goal(s), Milestones, Activities, Events, dependencies, etc.

## Program

**Status:** PRODUCT PROFILE / HISTORICAL KERNEL TERM  
**Current mapping:** Plan profile emphasizing structured progression, stages, repeated policies, reviews or adaptation.

## Calendar Block

**Status:** PRODUCT / UI TERM  
**Current mapping:** calendar-shaped representation whose underlying meaning is generally Schedule + Capacity Reservation/Claim or Availability override, depending on purpose.

## Deadline

**Status:** PRODUCT/UI TERM + semantic specialization  
**Maps to:** latest-bound Temporal Constraint.

## Window

**Status:** RANGE SHAPE / PRODUCT TERM

The same interval geometry may represent Constraint, Availability, Schedule or target-window semantics; geometry does not define meaning.

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

No universal Planning Item kernel primitive has been accepted.

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

Current mapping usually uses explicit Activity/Event + future Person/Relationship semantics. The other person does not need a LifeOS Account and the item is not automatically shared.

## Shared Item

**Status:** PRODUCT PHRASE, NOT UNIVERSAL PRIMITIVE

Preferred direction:

```text
shared canonical object
+
actor-scoped state/personal overlay
```

## Source

**Status:** IMPORTANT DEFERRED PROVENANCE DIMENSION

Where information came from: user entry, file, provider, email, external system, device, AI proposal, etc.

Source != truth != authority.

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

# 9. Multi-actor terminology — tracked but not prematurely canonized

## Actor

**Status:** PROVISIONAL / DEFERRED

Entity capable of acting, participating, holding responsibility or exercising authority. Do not equate Actor with `users.id`.

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

Authenticated/acting identity semantics remain open.

## Participant / Participation

**Status:** PROVISIONAL

Actor-scoped involvement/state around a shared object. No universal participation enum accepted.

## Responsibility

**Status:** PROVISIONAL — STRONG EVIDENCE

Must be richer than one `assigned_to` field and may need accountability, expected performer, open/claimable responsibility, substitution and hand-off.

## Stewardship / Coordination Responsibility

**Status:** PROVISIONAL / RESEARCH-BACKED QUESTION

Execution assignment can move while anticipation, reminding, monitoring and repair burden remain elsewhere.

## Performer

**Status:** RELATIONSHIP ROLE — exact model deferred

Who actually performed work; not automatically requester/responsible actor/planned assignee.

## Subject

**Status:** DEFERRED — DATA/SUBJECT REVIEW

Who/what information/action/Observation is about.

## Resource

**Status:** DEFERRED — DATA/SUBJECT REVIEW

Something whose availability/capacity/access may constrain execution/scheduling.

Actor and Resource can overlap but are not synonyms.

## Owner / Governor / Steward

**Status:** DEFERRED RELATIONSHIP/AUTHORITY SEMANTICS

Do not use casually as synonyms for creator, participant, viewer, responsible actor or performer.

## Authority

**Status:** DEFERRED — STRONG CROSS-CUTTING DIMENSION

Who/what may establish, approve, change or override canonical state in context.

```text
Authority != Visibility
Authority != Confirmation
```

## Visibility / Access

**Status:** DEFERRED

What an actor/principal may inspect/receive/use. Current access and historical attribution are distinct.

## Acknowledgement

**Status:** PROVISIONAL / DEFERRED

Grounding/receipt/recognition semantics where consequence requires them.

```text
Acknowledgement != Confirmation
Acknowledgement != Acceptance
```

## Acceptance / Agreement

**Status:** PROVISIONAL / DEFERRED

Willingness/participation/proposal/responsibility semantics.

```text
Acceptance != Confirmation
Acceptance != Actual
```

---

# 10. Reality/Evidence terms still under review

## Provenance

**Status:** DEFERRED — FINAL INDIVIDUAL CLUSTER REVIEW

How a fact/value/decision/change entered LifeOS and what source/agent/process/assertion/correction history affected it.

```text
Provenance != Actual
Provenance != Outcome
Provenance != Observation
Provenance != Confirmation
Provenance != Evidence
source != truth
source != authority by default
```

## Verification

**Status:** DEFERRED

Process/basis used to check a claim or record.

```text
Verification != Confirmation
Verification != Evidence by default
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

Typed/directional semantics are likely needed. Do not collapse meaningful relations into semantic-free `related_to` if behavior/query meaning differs.

Evidence may ultimately use typed Relationship machinery physically/logically; that does not make Evidence semantically redundant.

## Dependency

**Status:** DEFERRED / likely Relationship specialization or typed semantic

Represents coordination dependency where justified: producer/consumer, prerequisite, simultaneity, resource, blocking, etc.

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
Event != attendance
Routine != Recurrence
Routine != observed habit
Occurrence != Schedule
Occurrence != Session
Schedule != Temporal Constraint
Schedule != Availability
Schedule != Capacity Reservation
Schedule != Session/Actual
Session != Actual
Actual != Outcome
Actual != Observation
Actual != Confirmation
Actual != Evidence
Actual != Provenance
Outcome != lifecycle/operational state
Outcome != Observation
Outcome != Confirmation
Outcome != Provenance
Outcome != Evidence
Observation != Quantity
Observation != Register
Observation != Confirmation
Observation != Evidence
Observation != Provenance
Confirmation != Acknowledgement
Confirmation != Acceptance/Agreement
Confirmation != Verification
Confirmation != Authority
Confirmation != Provenance
Confirmation != Evidence
Evidence != source information
Evidence != Provenance
Evidence != GoalCriterion
Evidence != Milestone
missing Observation != observed negative
no Confirmation != false/rejected/incorrect
no Evidence != Evidence against
no LifeOS record != proof of non-occurrence
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
Confirmation by A != Confirmation by B
Evidence source != evaluator/confirmer/authority/viewer
conflicting Observation != automatic overwrite/average
conflicting Confirmation != automatic canonical truth
conflicting Evidence != automatic canonical conclusion
Schedule acceptance != participant acceptance
Delivery != acknowledgement
Acknowledgement != agreement
Agreement != authority
Authority != Actual
Authority != Confirmation
AI knowledge != disclosure permission
AI inference != Confirmation
AI discovery of Evidence != authority/disclosure permission
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
Needs confirmation != Confirmation object by itself
Evidence use != mandatory persisted Evidence entity/edge
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

UI
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

## Exam result

```text
Domain
Event
+ Actual
+ Observation: score = 78/100
+ Outcome: passed
+ optional Confirmation of the imported/recorded result
+ Evidence uses toward Goal/Milestone evaluation
+ optional Milestone

UI
Exam result
78/100 · Passed
Based on official result
[Confirm result] when policy requires it
```

## Weight log and Goal evidence

```text
Domain
Observation O-1
property: body weight
value: Quantity(66.4 kg)
effective: 08:00
recorded: 18:00

Criterion C-1
65 kg <= weight <= 67 kg

Evidence use
O-1 supports evaluation of C-1

Possible Product
Weight Register + Goal progress

UI
Weight
66.4 kg
Today · 08:00

Goal
In target range
Based on today's weight
```

The Observation is not duplicated into the Goal.

## Confirmation after correction

```text
Observation v1
value X
└ Confirmation A

Observation v2 after material correction
value Y
└ no inherited Confirmation
```

UI may simply show `Needs confirmation` for v2 when policy requires it.

## Conflicting Evidence

```text
Claim
Run >= 5 km

Watch Observation
5.1 km
└ Evidence supports

Phone Observation
4.7 km
└ Evidence contradicts
```

LifeOS preserves the conflict; it does not manufacture a truth by averaging unless an explicit evaluation rule says to do so.

## Private availability

```text
private source context / Evidence
↓
authorized evaluation / projection
Unavailable 18:00-20:00

shared UI
Sara is unavailable
```

The private reason/evidence need not be exposed.

---

# 14. Frontend rule

Frontend may choose the clearest language without changing kernel semantics.

Prefer plain language, progressive disclosure, contextual labels and actions/consequences over internal nouns when clearer.

Examples:

```text
Internal: Occurrence
UI: This time

Internal: Temporal Constraint
UI: Deadline / Preferred time / Not before

Internal: Actual
UI: What happened? / Actual time / Performed / Not performed

Internal: Outcome
UI: Passed / Partial / Approved / Result details

Internal: Observation
UI: Weight / Mood / Score / Odometer / Registra un dato

Internal: Confirmation
UI: Confirm / Looks correct / Review and confirm / Needs confirmation

Internal: Evidence
UI: Based on… / Supporting data / Conflicting data / Why this result?
```

Reverse rule:

> **A UX label does not automatically create a backend/domain type.**

---

# 15. Implementation-language rule

Physical/API terminology remains intentionally incomplete until logical/physical data modeling.

Do not infer table/class names from this map.

In particular Actor, Participant, Responsibility, Subject, Resource, Authority, Visibility, Actual, Outcome, Observation, Confirmation and Evidence must not be translated prematurely into final SQL table/cardinality choices.

Specific guardrails:

- Observation does not imply one generic fact table or one row per raw sensor tick;
- Confirmation does not imply one universal polymorphic `confirmations` table;
- Evidence does not imply one universal `evidence` table, one persisted edge per evaluative use, or one global evidence-strength scalar;
- product aliases do not create duplicate persistence models;
- provider/source identifiers do not define LifeOS identity.

When implementation names eventually differ from canonical language for good technical reasons, document the mapping here.

---

# 16. Terminology change policy

A term may enter when at least one holds:

1. it is an accepted Domain Atlas concept;
2. it is recurring product/UI language with clear mapping;
3. omitting it creates material ambiguity across domain/product/frontend/AI work;
4. a demonstrated semantic need must be tracked explicitly as PROVISIONAL/DEFERRED.

A term does **not** become canonical because a competitor uses it, one database design would be convenient, one mockup contains it, one scenario might theoretically need it, an AI suggested it, or the architecture sounds more complete with it.

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