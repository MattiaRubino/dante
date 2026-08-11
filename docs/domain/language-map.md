# LifeOS Domain & Product Language Map

**Status:** Canonical terminology reference for the active Domain Atlas  
**Established:** 2026-08-11  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

This document is the fast, canonical reference for LifeOS terminology.

It exists to prevent four different languages from drifting apart:

```text
DOMAIN LANGUAGE
what the concept means canonically
        ↓
PRODUCT LANGUAGE
how LifeOS may describe that meaning to users
        ↓
UI LANGUAGE
what may actually appear on screen
        ↓
IMPLEMENTATION LANGUAGE
API / schema / code names once designed
```

The four layers are related but are **not required to map one-to-one**.

Canonical rule:

> **A domain concept does not require a dedicated visible UI object, and a visible product/UI term does not automatically justify a separate domain primitive.**

Examples:

- `Occurrence` is a canonical domain concept but will usually remain hidden behind UI language such as `this time` or `this occurrence`;
- `Project` can be a powerful product/UI profile while the current kernel uses `Plan` rather than a separate Project primitive;
- `Task`, `Workout`, `Study item`, and `Maintenance action` can all be contextual presentations of `Activity` without four parallel execution models;
- `Calendar Block` remains useful product/UI language even though the current kernel represents its underlying meaning through Schedule, Availability, Capacity and reservations/claims.

This document is a map and governance reference. Detailed semantics remain in the linked concept specifications and checkpoints.

---

# 1. Terminology authority and precedence

When terminology conflicts, use this order:

1. accepted Domain Atlas concept specification;
2. this Domain & Product Language Map;
3. current Domain Atlas checkpoint / cross-cutting guardrail;
4. active workstream handoff;
5. current V1 product documents;
6. historical product glossaries and earlier planning documents;
7. conversation history.

The older `docs/product/v1-core-domain-glossary.md` remains valuable product-history evidence but is no longer the authority for kernel terminology where Domain Atlas decisions differ.

This map must not silently redefine an accepted concept. When a concept changes, the concept review happens first and this map is then updated to reflect the accepted result.

---

# 2. Official term status classes

Every important term belongs to one of the following statuses.

## CANONICAL

An accepted Domain Atlas concept with stable current semantics and a dedicated specification or accepted cross-cutting definition.

Examples: `Goal`, `Plan`, `Activity`, `Event`, `Routine`, `Milestone`, `Occurrence`, `Schedule`, `Session`, `Temporal Constraint`, `Recurrence`, `Availability`, `Capacity`.

## DERIVED

A useful value/state/projection computed from canonical facts rather than a universal primitive.

Examples may include `free capacity`, `overrun`, `lateness`, `streak`, `adherence`, or some progress percentages where meaningful.

## PRODUCT PROFILE

A user-facing specialization or recognizable product shape built from one or more canonical concepts without currently requiring a separate kernel primitive.

Examples: `Project`, `Program`, `Workout`, `Study plan`.

## PRODUCT / UI TERM

Useful language visible to users or designers that does not itself define a kernel concept.

Examples: `Task`, `Repeat`, `Deadline`, `Calendar Block`, `Busy`, `This time`.

## PROVISIONAL

A recurring semantic need with enough evidence to track explicitly, but whose exact concept boundary has not yet passed Domain Atlas review.

Examples may include `Actor`, `Participation`, `Responsibility`, `Stewardship`, `Authority`, or `Visibility` until their dedicated reviews are complete.

## DEFERRED

A demonstrated problem or semantic dimension whose final model is intentionally postponed to a later cluster.

Examples currently include final `Actual`, `Evidence`, `Subject`, `Resource`, `Relationship`, `Principal`, and authorization structures.

## HISTORICAL / SUPERSEDED

Earlier canonical/product terminology that remains in repository history but is not authoritative for the current kernel.

A historical term is not deleted merely to make documentation look cleaner. Its current mapping is made explicit instead.

---

# 3. UI exposure classes

Domain precision must not force ontology vocabulary into the user interface.

Each concept can be classified as:

- **DIRECT** — the term may naturally appear as a primary user-facing noun;
- **CONTEXTUAL** — the concept is user-visible, but the label usually changes with context;
- **CONFIGURATION** — the concept appears mainly through settings/rules rather than as an object noun;
- **ADVANCED** — normally hidden in simple flows but useful in detail/history/power-user surfaces;
- **HIDDEN** — primarily internal semantics; UI exposes actions or consequences rather than the domain noun.

---

# 4. Canonical concepts — Intention & Execution

## Goal

**Status:** CANONICAL  
**Canonical source:** `concepts/goal.md`  
**Domain question:** What outcome, condition, change, or behavioral pattern is intentionally desired?  
**UI exposure:** DIRECT

### Domain meaning

A persistent representation of something intentionally adopted as desired: an outcome, condition, change, or behavioral pattern to reach, produce, improve, reduce, maintain, avoid, or sustain.

### Plain-language meaning

Something a person, shared context, team, or other authorized context wants to become true or remain true.

### Not the same as

- Plan — how a purpose is pursued or organized;
- Activity — concrete intended action;
- Milestone — contextual meaningful checkpoint;
- Evidence — information used to evaluate the Goal.

### Product/UI language

Possible direct labels:

- Goal;
- Objective;
- Target, only where the product meaning is clearly outcome-oriented.

### Typical frontend surfaces

- Goals overview;
- Goal detail;
- Today/Home progress summary;
- review/check-in surfaces;
- search;
- AI planning/review context.

### Multi-actor note

Goal identity is independent from owner/governor, subject, stakeholder and contributor relationships.

---

## Plan

**Status:** CANONICAL  
**Canonical source:** `concepts/plan.md`  
**Domain question:** How is a purpose intended to be pursued or organized?  
**UI exposure:** DIRECT / CONTEXTUAL

### Domain meaning

A persistent revisable structure coordinating work, behaviors, milestones, rules or other execution elements in pursuit of a purpose.

### Plain-language meaning

The organized way LifeOS expects something to be pursued.

### Not the same as

- Goal — desired result/condition;
- Activity — one actionable unit;
- Routine — recurring behavioral/execution policy;
- Schedule — temporal placement;
- Actual — reality/history.

### Product profiles / aliases

Depending on semantics and UX, Plan may be presented as:

- Plan;
- Project;
- Program;
- Study plan;
- Training plan;
- Release plan;
- Trip plan;
- Rehabilitation plan.

`Project` and `Program` are **not currently separate kernel primitives**. They remain product-profile candidates unless later review demonstrates materially distinct identity, lifecycle, authority or invariants.

### Typical frontend surfaces

- Projects/Plans area;
- Goal detail;
- phased roadmap;
- timeline;
- board/list;
- review screen.

### Multi-actor note

Plan identity is independent from coordinator, contributor and responsible actor relationships.

---

## Activity

**Status:** CANONICAL  
**Canonical source:** `concepts/activity.md`  
**Domain question:** What actionable work or behavior is intended to be performed?  
**UI exposure:** DIRECT / CONTEXTUAL

### Domain meaning

A persistent actionable intention: a unit of work or behavior intended to be performed, while responsibility, Schedule, actual execution and Outcome remain separable.

### Plain-language meaning

Something that is meant to be done.

### Not the same as

- Event — occurrence-centred expectation;
- Session — actual execution episode;
- Plan — broader coordination structure;
- Actual — what actually happened.

### Product/UI aliases

Depending on context:

- Task;
- Action;
- Workout;
- Study item;
- Maintenance action;
- Checklist item;
- Preparation step.

These aliases do not require separate execution primitives.

### Typical frontend surfaces

- task/action list;
- Today timeline;
- Plan detail;
- Routine occurrence detail;
- specialist module view;
- execution history.

### Multi-actor note

Activity identity is independent from requester, creator, assignee/responsible actor and eventual performer.

---

## Event

**Status:** CANONICAL  
**Canonical source:** `concepts/event.md`  
**Domain question:** What expected occurrence is intrinsically time-centred in meaning?  
**UI exposure:** DIRECT

### Domain meaning

A persistent expected occurrence for which temporal placement is intrinsic to meaning.

### Plain-language meaning

Something expected to happen: meeting, appointment, concert, flight, lesson, interview, shift, race, ceremony, etc.

### Not the same as

- Activity — action-centred intention;
- Schedule — accepted temporal assignment;
- participant response — actor-specific participation intention;
- attendance — what actually happened;
- Milestone — checkpoint/state becoming true.

### Typical frontend surfaces

- calendar;
- timeline;
- event detail;
- invitations/participation surfaces;
- provider integration views.

### Multi-actor note

Event identity is independent from organizer, participant, participant response and attendance. One shared Event should normally coexist with actor-scoped participation state rather than being duplicated per person.

---

## Routine

**Status:** CANONICAL  
**Canonical source:** `concepts/routine.md`  
**Domain question:** What recurring behavioral or execution policy is intended to repeat?  
**UI exposure:** DIRECT

### Domain meaning

A persistent reusable policy expressing a pattern of behavior or execution intended to repeat over time.

### Plain-language meaning

A recurring behavior/rule such as training three times a week, taking medication every twelve hours, or doing a weekly review.

### Not the same as

- Recurrence — repeating/generative pattern mechanics;
- observed habit — behavior noticed in reality but not intentionally adopted as policy;
- Event series — recurring occurrence-centred semantics;
- Plan — broader progression/strategy.

### Typical frontend surfaces

- Routines area;
- repeat configuration;
- Today generated expectation;
- adherence/review view;
- specialist module.

### Multi-actor note

Routine identity is independent from performer. Responsibility may vary by Occurrence without duplicating the Routine.

---

## Milestone

**Status:** CANONICAL  
**Canonical source:** `concepts/milestone.md`  
**Domain question:** What meaningful contextual checkpoint matters inside a broader Goal or Plan?  
**UI exposure:** DIRECT / ADVANCED

### Domain meaning

A persistent contextual checkpoint representing a meaningful state, achievement, decision, delivery or transition.

### Plain-language meaning

A significant checkpoint such as `design approved`, `B1 reached`, or `release live`.

### Not the same as

- Goal;
- Goal criterion;
- Activity;
- Event;
- Outcome;
- Deadline;
- Phase.

### Typical frontend surfaces

- Plan/Goal timeline;
- roadmap;
- progress/review;
- release/project-style views.

### Multi-actor note

Stakeholders, approvers and governors do not define Milestone identity.

---

# 5. Canonical concepts — Time

## Occurrence

**Status:** CANONICAL  
**Canonical source:** `concepts/occurrence.md`  
**Domain question:** Which individual expected instance from a recurring/generative source is being discussed?  
**UI exposure:** HIDDEN / ADVANCED

### Domain meaning

Stable logical identity for one expected instance generated by a recurring/generative source.

### Typical UI language

Users will more often see:

- This time;
- This workout;
- This meeting;
- This occurrence;
- Only this one;
- This and future occurrences.

### Not the same as

- Recurrence;
- Routine/Event source;
- Schedule;
- Session;
- Actual.

### Multi-actor note

Occurrence identity is independent from assigned/responsible actor.

---

## Schedule

**Status:** CANONICAL  
**Canonical source:** `concepts/schedule.md`  
**Domain question:** When is this schedulable subject currently accepted/intended/expected to happen?  
**UI exposure:** HIDDEN / CONFIGURATION

### Typical UI language

- When;
- Date;
- Time;
- Move to...;
- Add to calendar;
- Scheduled for;
- Tuesday afternoon.

### Not the same as

- Temporal Constraint;
- deadline/target;
- Recurrence;
- Availability;
- capacity reservation;
- Session/Actual.

### Multi-actor note

Accepted Schedule means the canonical temporal assignment according to the relevant governing authority/context. It does **not** mean every participant accepted participation.

---

## Session

**Status:** CANONICAL  
**Canonical source:** `concepts/session.md`  
**Domain question:** Which logically continuous bounded episode of actual execution took place?  
**UI exposure:** CONTEXTUAL / ADVANCED

### Typical UI language

- Start;
- Pause;
- Resume;
- Stop;
- Work session;
- Study session;
- Workout;
- Tracked time;
- Execution history.

### Not the same as

- Schedule;
- Activity;
- Occurrence;
- Event attendance;
- broader Actual/Outcome.

### Multi-actor note

Session identity follows logical execution continuity, not number of performers. Actor-specific participation may cover only part of a collaborative Session envelope.

---

## Temporal Constraint

**Status:** CANONICAL  
**Canonical source:** `concepts/temporal-constraint.md`  
**Domain question:** Where/when is temporal placement permitted, required, bounded or preferred?  
**UI exposure:** CONFIGURATION

### Typical UI language

- Deadline;
- Not before;
- Not after;
- Preferred time;
- Allowed window;
- Avoid this time;
- Minimum duration;
- Maximum duration;
- Recovery/spacing.

`Temporal Constraint` should normally remain an internal/advanced term rather than primary consumer UI copy.

### Not the same as

- Schedule;
- Availability;
- target date/window;
- Movement Policy;
- Actual.

### Product specialization

`Deadline` is a latest-bound Temporal Constraint meaning, not a parallel kernel primitive.

---

## Recurrence

**Status:** CANONICAL  
**Canonical source:** `concepts/recurrence.md`  
**Domain question:** How does a temporal/generative pattern repeat?  
**UI exposure:** CONFIGURATION

### Typical UI language

- Repeat;
- Every Monday;
- Three times per week;
- Every 12 hours;
- After completion;
- Every second week;
- Custom repeat.

### Not the same as

- Routine;
- Event series identity;
- Occurrence;
- Schedule;
- Trigger/automation;
- responsibility rotation.

---

## Availability

**Status:** CANONICAL semantic capability  
**Canonical source:** `concepts/availability-capacity.md`  
**Domain question:** When may a schedulable resource's capacity be used?  
**UI exposure:** DIRECT / CONFIGURATION / DERIVED

### Typical UI language

- Available;
- Unavailable;
- Working hours;
- Free/busy;
- Availability for others;
- Exception;
- Out of office.

### Important boundary

Availability is about resource capacity. A subject-specific rule such as `never schedule this workout after 20:00` is a Temporal Constraint.

### Multi-actor note

Useful availability may be shared as an authorized derived consequence without disclosing private source events.

---

## Capacity

**Status:** CANONICAL semantic capability  
**Canonical source:** `concepts/availability-capacity.md`  
**Domain question:** How much / what kind of compatible commitment can a schedulable resource sustain?  
**UI exposure:** HIDDEN / DERIVED / ADVANCED

### Typical UI language

- Busy;
- Block my time;
- Can overlap;
- Focus time;
- Capacity remaining;
- Room available;
- Resource unavailable.

### Important boundaries

- scheduled does not automatically mean capacity consumed;
- Capacity is not universally binary;
- Capacity is not universally one percentage;
- timestamp overlap alone is not universal conflict.

---

# 6. Current product/profile terms that are not independent kernel primitives

## Task

**Status:** PRODUCT / UI TERM  
**Maps to:** Activity

Use when completion of a defined piece of work is the dominant user-facing meaning.

Do not create a second Task execution/history model beside Activity.

## Project

**Status:** PRODUCT PROFILE / HISTORICAL KERNEL TERM  
**Current mapping:** Plan profile, optionally linked to Goal(s), Milestones, Activities, Events, dependencies and other structures.

A finite coordinated body of work can still be presented as a Project. Current Domain Atlas evidence does not require Project to be a separate primitive from Plan.

## Program

**Status:** PRODUCT PROFILE / HISTORICAL KERNEL TERM  
**Current mapping:** Plan profile with structured progression, stages, repeated policies, reviews or adaptation.

A training program or language program remains natural product language without requiring a second strategy primitive.

## Calendar Block

**Status:** PRODUCT / UI TERM  
**Current mapping:** a calendar-shaped representation whose underlying semantics are normally Schedule + Capacity Reservation/Claim or Availability override, depending on purpose.

Do not automatically duplicate every scheduled Activity/Event into a Calendar Block entity.

## Deadline

**Status:** PRODUCT / UI TERM / semantic specialization  
**Maps to:** latest-bound Temporal Constraint.

## Window

**Status:** SHAPE / PRODUCT TERM, not one universal primitive

The same interval/range shape may mean:

- valid Temporal Constraint;
- preferred Temporal Constraint;
- Availability;
- accepted coarse Schedule;
- Goal/Milestone target window.

Meaning must come from context.

## Repeat

**Status:** UI TERM  
**Maps to:** Recurrence configuration where recurrence semantics are actually intended.

## Busy / Free

**Status:** UI / DERIVED TERMS  
**Maps to:** projections from Availability, Capacity, reservations/claims and compatibility rules.

Binary free/busy is not the universal Capacity ontology.

---

# 7. Multi-actor terminology — tracked but not prematurely canonized

The multi-actor discovery simulation and external research prove that the following dimensions are real. Their exact primitive/value-object/relationship boundaries remain subject to later Domain Atlas review.

## Actor

**Status:** PROVISIONAL / DEFERRED TO SUBJECT-RELATIONSHIP REVIEW

Working meaning: an entity that can act, participate, hold responsibility, exercise authority, contribute or otherwise occupy an active role in domain reality.

Do not currently equate Actor with `users.id`.

## Person

**Status:** DEFERRED

Working meaning: a human represented in LifeOS domain reality.

A Person may exist without a LifeOS Account.

## Account

**Status:** PRODUCT/IDENTITY CONCEPT — final domain boundary deferred

Working meaning: LifeOS account/login relationship.

Canonical non-collapse rule:

> Account != Person != Participant != Subject.

## Principal

**Status:** DEFERRED TECHNICAL/AUTHORITY CONCEPT

Likely represents an authenticated identity acting in the system. Final relationship to Account, Actor and delegated AI remains open.

## Participant / Participation

**Status:** PROVISIONAL

Working meaning: actor-scoped relationship/state describing involvement in a particular shared Event, Activity, Plan or other supported object.

Participation may include invitation/response/actual-participation semantics, but one universal state machine is not assumed.

## Responsibility

**Status:** PROVISIONAL — STRONG EVIDENCE

A repeated cross-domain need richer than one `assigned_to` field.

Potential dimensions include:

- accountability;
- execution responsibility;
- claimable/open responsibility;
- approval responsibility;
- substitution;
- hand-off.

Do not prematurely flatten all of these into one enum.

## Stewardship / Coordination responsibility

**Status:** PROVISIONAL / RESEARCH-BACKED QUESTION

External research shows that execution assignment can move while anticipation, reminding, monitoring and repair burden remain with another person.

The phenomenon is real; whether it becomes a dedicated domain concept, relationship, derived metric or product-evaluation dimension remains deliberately open.

## Performer

**Status:** RELATIONSHIP ROLE — exact model deferred

Who actually performed work. Performer is not automatically Activity owner/responsible actor and may differ from the planned assignee.

## Subject

**Status:** DEFERRED — UPCOMING DATA/SUBJECT REVIEW

Who or what information/action/observation is about.

Examples expose why Subject may differ from Actor:

- caregiver acts, older person is subject;
- clinician acts, patient is subject;
- parent coordinates, child is subject;
- technician acts, vehicle is subject.

## Resource

**Status:** DEFERRED — UPCOMING DATA/SUBJECT REVIEW

Something whose availability/capacity/access may constrain action or scheduling.

Potential examples include people in schedulable roles, rooms, vehicles, devices, equipment, stock or facilities.

`Actor` and `Resource` may overlap in a scenario but are not synonyms.

## Owner / Governor / Steward

**Status:** DEFERRED RELATIONSHIP/AUTHORITY SEMANTICS

These words must not be used casually as synonyms for creator, participant or person who can see an object.

## Authority

**Status:** DEFERRED — STRONG CROSS-CUTTING DIMENSION

Who/what may establish, approve, change or override canonical state in a given context.

Authority is not inferred merely from visibility, participation or item creation.

## Visibility / Access

**Status:** DEFERRED

What an actor/principal may inspect or receive.

Visibility is distinct from authority.

Future design must account for purpose, context, revocation, historical attribution and derived/inferred disclosure.

## Provenance

**Status:** DEFERRED CANONICAL FUTURE CONCEPT

How a fact/value/change entered LifeOS, from whom/what, under what confidence/confirmation/authority context.

Already required by accepted concepts; detailed model belongs to the Observed Reality/Evidence cluster.

---

# 8. Future reality/evidence terms — do not fake final semantics yet

## Actual

**Status:** DEFERRED — NEXT-LAYER CONCEPT

Working purpose: broader representation of what actually happened, distinct from intention, Schedule and Session.

Do not use `Actual` as a generic dumping ground before its dedicated review.

## Outcome

**Status:** DEFERRED

Working purpose: what resulted from execution/occurrence. Must be tested against Actual, Milestone, Confirmation and Evidence.

## Observation

**Status:** DEFERRED

Working purpose: observed fact about reality that may exist with or without prior intention.

## Evidence

**Status:** DEFERRED

Working purpose: information used in a particular evaluation/context. Evidence is not automatically equivalent to source fact, positive contribution, or proof of universal truth.

## Confirmation / Acknowledgement / Acceptance

**Status:** DEFERRED — IMPORTANT DISTINCTIONS

Multi-actor research establishes that these words cannot be collapsed casually.

At high consequence:

```text
sent
!= delivered
!= seen
!= understood
!= acknowledged
!= accepted/agreed
!= authoritative/confirmed
!= acted upon
!= actually happened
```

Not every product flow should expose every stage. The semantics must remain available where consequence justifies them.

---

# 9. Frequently confused terms

Use this section as the first diagnostic when terminology becomes ambiguous.

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
Temporal Constraint != Availability
Recurrence != Trigger
Availability != empty-gap cache
Capacity != universal busy/free boolean
Milestone != Outcome
```

Multi-actor:

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
Participation response != actual participation
Schedule acceptance != participant acceptance
Delivery != acknowledgement
Acknowledgement != agreement
Agreement != authority
Authority != Actual
AI knowledge != disclosure permission
AI suggestion != canonical authority
Revocation of future access != deletion of historical attribution
```

---

# 10. Domain-to-product-to-UI examples

## Example — buy milk

```text
Domain
Activity

Product profile
Task

UI
Buy milk
[ ]

Schedule UI
Tomorrow
```

No separate Task primitive is required.

## Example — gym 3x/week

```text
Domain
Routine
+ Recurrence
+ Occurrences
+ optional Schedules

Product
Routine / Workout plan

Simple UI
Gym
3 times per week
```

The simple user does not need to see `quota recurrence`, `period frame` or `Occurrence` terminology.

## Example — website redesign

```text
Domain
Goal (optional)
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

`Project` can therefore remain first-class UX without becoming a second strategy kernel.

## Example — recurring team meeting

```text
Domain
Event semantics
+ Recurrence
+ Occurrences
+ Schedule
+ actor-scoped participation

UI
Weekly Team Meeting
Every Monday · 10:00
Accepted / Tentative / Declined
```

## Example — private availability

```text
Private domain source
Event: medical appointment

Derived authorized projection
Unavailable 18:00-20:00

Shared UI
Sara is unavailable
```

The UI must not reveal the private source merely because LifeOS used it for reasoning.

---

# 11. Terminology change policy

The language map is intended to remain stable. Stability does **not** mean freezing mistakes.

A new term may enter this canonical map only when at least one condition holds:

1. it is an accepted Domain Atlas concept;
2. it is a recurring product/UI term with a clear mapping to accepted semantics;
3. omitting the distinction creates material ambiguity across domain/product/frontend/AI work;
4. a demonstrated semantic need must be tracked explicitly as PROVISIONAL or DEFERRED.

A term must **not** become canonical merely because:

- another product uses it;
- a database table name would be convenient;
- one UI mockup contains it;
- one scenario could theoretically use it;
- an AI suggested it;
- it sounds architecturally complete.

When a term changes:

1. change the source concept/decision first;
2. preserve historical reasoning;
3. update this map;
4. update affected checkpoints/handoffs;
5. update implementation names only when the persistence/API model actually exists.

Do not silently recycle one term with a different meaning.

---

# 12. Frontend rule

Frontend design may choose the most understandable user language without changing kernel semantics.

The frontend should prefer:

- plain language;
- progressive disclosure;
- contextual labels;
- specialist terminology only where users expect it;
- actions/consequences instead of internal nouns when clearer.

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
Internal: Capacity Reservation
UI: Block my time / Focus time
```

The reverse rule also applies:

> **A UX label does not automatically create a backend/domain type.**

---

# 13. Implementation-language rule

Physical/API terminology remains intentionally incomplete until logical and physical data modeling.

Do not infer future table names from this map.

For example:

```text
Canonical concept: Plan
```

currently does **not** imply a final schema choice such as:

```text
plans
projects
programs
```

Likewise `Actor`, `Participant`, `Responsibility`, and `Visibility` must not be translated prematurely into tables/ACL structures before their dedicated reviews.

Once APIs/persistence are designed, implementation names should either match canonical language or document an explicit mapping here.

---

# 14. Maintenance rule

This file is a navigation/reference layer, not a duplicate of every concept specification.

Detailed concept documents remain authoritative for:

- lifecycle;
- edge cases;
- full invariants;
- validation evidence;
- historical decisions;
- rejected alternatives;
- persistence implications.

This map should remain concise enough to answer:

> **What does this LifeOS term mean, what does it not mean, and what might the user actually see?**

without requiring a reader to reconstruct the ontology from dozens of files.